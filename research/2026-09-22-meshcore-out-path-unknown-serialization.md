# MeshCore `OUT_PATH_UNKNOWN` contact serialization

**Evidence:** VERIFIED  
**Provisional Gold score:** 28/30 (S)  
**Upstream:** https://github.com/meshcore-dev/MeshCore  
**Upstream revision inspected:** `e94125987ed87497e706a0b54d1e80c709343980`  
**License:** MIT (project-level licensing previously verified in the MeshCore dossier)

## Question

When companion-radio resets a stale contact route to `OUT_PATH_UNKNOWN`, what concrete representation is written to persistent contact storage, and is the same value restored on load?

## Finding

The inspected source confirms a direct one-byte round trip for the route-state sentinel.

`src/helpers/ContactInfo.h` defines `OUT_PATH_UNKNOWN` as `0xFF`. In `examples/companion_radio/DataStore.cpp`, `DataStore::saveContacts()` opens `/contacts3` and writes each saved contact as a fixed field sequence. The route length is written directly from `c.out_path_len` as exactly one byte, followed later by the full 64-byte `c.out_path` buffer.

The corresponding contact loader reads exactly one byte from the same record position directly back into `c.out_path_len`, then reads the 64-byte path buffer. There is no serialization transform, normalization, or special-case conversion around this field in the inspected save/load code.

Therefore, when `CMD_RESET_PATH` has changed `out_path_len` to `OUT_PATH_UNKNOWN`, a completed `saveContacts()` writes the sentinel byte `0xFF` into `/contacts3`. Loading that record restores `0xFF` to `out_path_len`, which the routing code interprets as unknown/flood state.

## Important nuance: path bytes remain present

The persistence format always writes the full 64-byte `out_path` array even when `out_path_len == 0xFF`. The reset operation's semantic invalidation is therefore carried by the length/state byte, not by requiring the old path buffer to be erased.

This is useful for implementation review: stale bytes in the stored 64-byte path field do not by themselves mean a stale route is active. Consumers must honor `out_path_len`; `0xFF` marks the route unknown.

## Storage behavior

The contact file is `/contacts3`. The inspected implementation writes fields directly through the platform filesystem abstraction and closes the file after the contact loop. On nRF52/STM32 builds, repository code also contains migration logic that copies an existing `/contacts3` byte stream to the secondary filesystem when appropriate.

This confirms representation and source-level save/load symmetry. It does not establish atomicity or crash consistency of the filesystem write itself.

## Recovery implication

Combined with the prior reset-persistence dossier, the source-supported lifecycle is now:

1. host requests path reset;
2. firmware sets `out_path_len = 0xFF` (`OUT_PATH_UNKNOWN`);
3. firmware schedules the contact store write;
4. `saveContacts()` writes that one-byte sentinel into `/contacts3`;
5. a later load reads the sentinel back unchanged;
6. routing code sees the contact as lacking a known direct path and can use flood routing;
7. later path learning can replace `0xFF` with a concrete path length and schedule another save.

## Verification performed

Inspected upstream source for:

- the `OUT_PATH_UNKNOWN` constant;
- `/contacts3` save format;
- the exact one-byte `out_path_len` write;
- the matching one-byte load;
- the 64-byte path-buffer write/read;
- filesystem migration handling for `/contacts3`.

No upstream implementation source was copied into GitHub Gold.

## Not verified

GitHub Gold did **not**:

- compile or flash MeshCore;
- execute upstream tests;
- inspect bytes from a physical device filesystem;
- issue a live reset command;
- power-cycle hardware;
- test filesystem atomicity, corruption, partial writes, brownouts, or wear behavior;
- prove that every supported filesystem backend has identical crash semantics.

## Follow-up leads

- consolidate the completed MeshCore route-recovery work into a Meshtastic / MeshCore / Reticulum recovery-policy comparison;
- inspect whether contact-file writes use any platform-specific atomic replacement or truncation behavior worth documenting;
- rotate discovery into a different technical category after consolidation to preserve GitHub Gold breadth.
