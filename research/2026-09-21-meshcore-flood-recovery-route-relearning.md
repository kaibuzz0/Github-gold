# MeshCore flood recovery — route relearning and persistence

- **Repositories:** https://github.com/meshcore-dev/MeshCore and https://github.com/meshcore-dev/meshcore_py
- **Organization:** meshcore-dev
- **Category:** Off-grid communications / MeshCore routing / recovery / persistence
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** MIT (upstream projects; no source copied into GitHub Gold)
- **Inspection date:** 2026-09-21
- **Discovery source:** recursive follow-up from the Python ACK retry/path-reset/flood recovery dossier

## Executive finding

Successful flood retry is not itself the event that immediately installs a replacement direct route. The Python retry helper resets the contact path to flood/unknown and waits for an ACK. A plain flood ACK can prove delivery, but the inspected firmware only updates a contact's `out_path` when it receives an authenticated path-return packet through `onContactPathRecv()`.

When such a path-return packet arrives, `BaseChatMesh` replaces the cached `out_path`, updates `lastmod`, and calls `onContactPathUpdated()`. In companion-radio firmware that callback emits `PUSH_CODE_PATH_UPDATED` to the host and schedules a lazy contacts write. The normal loop later calls `saveContacts()`, and `DataStore::saveContacts()` serializes both `out_path_len` and the 64-byte `out_path` field into `/contacts3`.

Therefore MeshCore can relearn and persist a new direct route after flood recovery, but the mechanism is **path-return driven**, not merely "ACK received over flood = route learned." This distinction matters when reasoning about convergence and host retry behavior.

## Python recovery boundary

`meshcore_py.send_msg_with_retry()` explicitly resets a stale path after the configured direct-attempt threshold. On successful reset it marks the local contact representation as flood/unknown (`out_path = ""`, `out_path_len = -1`) and continues sending. The helper correlates ACKs across attempts and treats a matching ACK as successful delivery.

The helper itself does not synthesize a replacement direct path after a flood ACK. Its job is delivery recovery and path invalidation/escalation.

## Firmware path learning

`BaseChatMesh::onContactPathRecv()` is the key route-learning point. Its default implementation:

1. replaces the current contact `out_path` with the received return path;
2. updates the contact modification timestamp;
3. calls `onContactPathUpdated()`;
4. optionally processes an encoded ACK or response carried with the path-return packet;
5. returns true so reciprocal-path handling can continue when appropriate.

The source explicitly notes that the current implementation replaces the route regardless of whether it is objectively "best" and suggests future multipath/best-path work. This matches the earlier GitHub Gold finding that MeshCore should not be described as metric-optimal routing.

A plain ACK takes a different path through `onAckRecv()`: it satisfies the pending ACK and can trigger `handleReturnPathRetry()` in an asymmetric case, but it does not itself copy `packet->path` into the contact's `out_path`.

## Explicit discovery is deliberately different

Companion-radio firmware overrides `onContactPathRecv()` for a response matching `pending_discovery`. It validates path sizes and reports `PUSH_CODE_PATH_DISCOVERY_RESPONSE` to the host, then returns `false` with an explicit `DON'T send reciprocal path` comment. That special transaction should not be conflated with the default unsolicited/normal path-return learning path.

## Host notification and persistence

In companion-radio firmware, `onContactPathUpdated()`:

- emits `PUSH_CODE_PATH_UPDATED` with the contact public key;
- schedules `dirty_contacts_expiry` using the lazy-contact-write delay.

The firmware loop checks that deadline and invokes `saveContacts()` when it expires. `saveContacts()` delegates to the data store, whose `/contacts3` record format includes `out_path_len` and the full 64-byte `out_path`; the corresponding load path restores those fields.

This is direct source evidence that a learned replacement path is intended to survive beyond the immediate RAM state for persisted contacts, subject to the lazy write completing successfully.

## Important qualification

The strongest defensible sequence is:

**dead cached route -> Python retries -> reset to flood -> flood delivery/ACK -> path-return exchange (when produced/received) -> firmware caches replacement direct route -> path-updated notification -> lazy persistence.**

It is too strong to state that every successful flood ACK automatically teaches a direct path. ACK success and route learning are separate protocol events in the inspected implementation.

## Reusable technical pieces

- separation of delivery recovery from route-learning state;
- host-side retry + firmware-side route ownership;
- path-return packets that can carry ACK/response data;
- route-change push notification to host applications;
- lazy persistence to reduce immediate flash writes;
- explicit on-disk route fields for reboot persistence;
- asymmetric-route repair through reciprocal-path retry.

## Caveats

- GitHub Gold did not execute the Python tests in this run or flash companion firmware.
- No live RF experiment confirmed timing between flood ACK and path-return reception.
- A matching flood ACK proves delivery but, by itself, is not source evidence of a newly cached direct route.
- Persistence is deferred; power loss or write failure before the lazy save can prevent the newest in-memory path from reaching storage.
- Current default path learning replaces the existing path rather than maintaining a metric-ranked multipath set.
- Explicit path discovery has special handling and does not use the exact same reciprocal behavior as ordinary path returns.

## Verification performed

Inspected current upstream source for:

- Python `send_msg_with_retry()` reset/flood behavior;
- `BaseChatMesh::onContactPathRecv()` route replacement;
- plain ACK handling and reciprocal-path retry;
- companion-radio explicit path-discovery override;
- `onContactPathUpdated()` host notification and lazy-write scheduling;
- delayed `saveContacts()` execution;
- `DataStore` contact serialization/deserialization of `out_path_len` and `out_path`.

## Verification NOT performed

GitHub Gold did **not**:

- install Python packages;
- execute pytest;
- compile or flash firmware;
- connect BLE/serial/TCP hardware;
- transmit LoRa packets;
- force a stale route on a physical mesh;
- power-cycle hardware to independently prove persisted route restoration;
- benchmark route-convergence time or airtime;
- independently security-audit path-return authentication;
- copy upstream implementation source.

## Gold rationale

**Utility — 5/5:** clarifies a practical recovery contract needed by applications relying on MeshCore delivery and route healing.

**Working Evidence — 5/5:** behavior is supported by concrete host and firmware source paths plus persistent record implementation.

**Reusability — 5/5:** clean separation between retry, route learning, notification, and persistence is useful to constrained-network designs; upstream is MIT licensed.

**Novelty — 4/5:** individual mechanisms are established networking patterns, but their compact embedded implementation and cross-layer composition are technically valuable.

**Documentation — 4/5:** upstream documentation is useful, while the exact recovery-to-persistence contract requires source tracing.

**Maintenance — 5/5:** active 2026 MeshCore ecosystem already established in the parent dossiers.

**Provisional total: 28/30 — S tier.**

## Next research queue

1. Trace path-return creation after flood text delivery to determine precisely when a receiver emits a new reciprocal path.
2. Inspect `reset_path` companion command handling and whether reset-to-flood is itself persisted before the next learned route.
3. Compare official mobile clients' retry/path-update semantics with Python and JavaScript.
4. Inspect MeshCore KISS framing/interoperability as a separate reusable component.
5. Build a Meshtastic / MeshCore / Reticulum recovery-policy comparison dossier.
