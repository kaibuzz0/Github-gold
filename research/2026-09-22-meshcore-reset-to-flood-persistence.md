# MeshCore reset-to-flood persistence

**Evidence:** VERIFIED  
**Provisional Gold score:** 28/30 (S)  
**Upstream:** https://github.com/meshcore-dev/MeshCore  
**Upstream revision inspected:** `e94125987ed87497e706a0b54d1e80c709343980`  
**License:** MIT (project-level licensing previously verified in the MeshCore dossier)

## Question

When a host resets a stale contact route to flood/unknown before retrying, is that reset merely an in-memory routing decision, or is it persisted to the companion radio's contact store before a replacement route is relearned?

## Finding

The companion-radio implementation makes the reset persistent, but through a deferred write rather than an immediate synchronous contact-store write.

`CMD_RESET_PATH` looks up the contact by its full public key and sets `recipient->out_path_len = OUT_PATH_UNKNOWN`. It then schedules `dirty_contacts_expiry = futureMillis(LAZY_CONTACTS_WRITE_DELAY)` and returns `RESP_CODE_OK`. `LAZY_CONTACTS_WRITE_DELAY` is 5000 ms in the inspected source.

The main `MyMesh::loop()` checks that dirty-contact deadline. Once it has elapsed it calls `saveContacts()` and clears the pending deadline. `saveContacts()` delegates to the configured `DataStore` contact persistence path.

The reboot command contains an additional durability guard: if a dirty contact write is still pending, it calls `saveContacts()` before invoking `board.reboot()`.

Therefore, after a normal `reset_path` command succeeds, the unknown/flood route state is intended to become persistent after roughly five seconds even if no replacement direct path has yet been learned. A normal command-driven reboot also flushes a pending reset before rebooting.

## Recovery implication

This completes another part of the stale-route lifecycle:

1. host retry policy detects repeated direct-send failure;
2. host sends `reset_path`;
3. companion firmware immediately changes the in-memory contact route to `OUT_PATH_UNKNOWN`;
4. firmware schedules the contact state for persistent storage;
5. subsequent message sending sees an unknown route and uses flood routing;
6. if a reciprocal path is later returned, normal path learning can replace the unknown route with a newly learned direct route and schedule another contact write.

This means a stale direct route is not necessarily resurrected merely because the radio restarts after the reset. Once the deferred contact write has completed—or the normal reboot path flushes it—the reset state should survive reload from storage.

## Important caveat: crash/power-loss window

The reset is **not synchronously durable at command acknowledgement**. There is an approximately five-second lazy-write window between `RESP_CODE_OK` and the scheduled `saveContacts()` call. An abrupt power loss, watchdog reset, hard crash, or other restart path that bypasses the normal reboot flush during that interval could leave the previously persisted route on storage.

This is a source-level durability observation, not a demonstrated failure. No power-cut test or storage fault injection was performed.

## Verification performed

Inspected upstream companion-radio source for:

- `CMD_RESET_PATH` handling;
- `OUT_PATH_UNKNOWN` assignment;
- `LAZY_CONTACTS_WRITE_DELAY`;
- dirty-contact scheduling;
- `saveContacts()`;
- the main-loop delayed write;
- the command-driven reboot flush.

No upstream implementation source was copied into GitHub Gold.

## Not verified

GitHub Gold did **not**:

- compile or flash MeshCore;
- execute upstream tests;
- issue `reset_path` to physical hardware;
- power-cycle hardware inside or outside the lazy-write window;
- inspect filesystem bytes before/after reset;
- inject filesystem write failures;
- test watchdog/brownout behavior;
- independently audit storage durability.

## Follow-up leads

- inspect the concrete `DataStore::saveContacts()` implementation and on-disk contact format to confirm how `OUT_PATH_UNKNOWN` is serialized;
- determine whether brownout/watchdog restart paths have any pending-write flush opportunity;
- consolidate the now-complete MeshCore stale-route lifecycle into a Meshtastic / MeshCore / Reticulum recovery-policy comparison;
- rotate subsequent discovery into a different GitHub Gold category to avoid over-concentration on one ecosystem.
