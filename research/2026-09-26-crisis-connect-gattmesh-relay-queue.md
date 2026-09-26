# Crisis Connect GATT mesh relay + resilient outbound queue

- **Upstream repository:** https://github.com/emirhan-duman/Crisis-Connect
- **Component:** Android `GattMeshForegroundService` + iOS `GattMeshProtocol` / `GattMeshManager`
- **Category:** emergency communications / BLE mesh / store-and-forward / resilient mobile transport
- **Evidence:** VERIFIED
- **Provisional Gold score:** **27 / 30 — S tier**
  - Utility: 5/5
  - Working evidence: 4/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Discovery:** recursive component pass from the Crisis Connect dossier. YouTube seed playlists were not used as technical evidence.

## Why this component is Gold

The GATT mesh implementation turns BLE into a bounded store-and-forward transport rather than treating a Bluetooth connection as a fragile point-to-point pipe. The Android and iOS implementations expose explicit packet IDs, hop counts, duplicate suppression, receipts, queue persistence/recovery, retry backoff, freshness bounds, packet-size limits, rate bounds and cross-platform protocol versioning.

The reusable engineering pattern is the combination of **bounded relay + persistent retry queue + transport-independent message identity**. That pattern is useful for disaster communications, field data collection, intermittent industrial links and other mobile software where peers disappear and reappear frequently.

## Evidence inspected

### Wire model and relay bounds

The iOS `GattMeshPacket` carries a stable message ID, sender label, timestamp, packet type, receipt metadata, hop count, protocol version, encryption metadata and optional authenticated-origin/blob fields. `GattMeshProtocol` defines a 4,096-byte packet ceiling, 1,024-character chat ceiling, 24-hour maximum message age, two-minute future-clock-skew allowance and a **maximum of four forwarding hops**. Decoding rejects invalid hop counts and malformed/stale packet fields.

`GattMeshManager.relayIfNeededLocked` only relays chat or receipt packets while `packet.hop < maxForwardHops`, then constructs the forwarded packet with the hop count advanced. This is concrete loop/range bounding rather than an unbounded rebroadcast design.

### Deduplication

Both platforms maintain seen-message state. iOS keeps `seenMessageIds` with timestamps and rejects a message ID that has already been observed. Android maintains bounded tracked-message IDs; the main GATT service caps this structure at 4,096 IDs, while the separate Wi-Fi Aware rescue mesh uses a bounded `LinkedHashSet` and evicts oldest IDs when its limit is exceeded.

Stable IDs plus hop limits are important together: hop bounds cap propagation depth, while deduplication prevents the same logical packet from repeatedly re-entering local delivery/relay paths.

### Persistent store-and-forward queue

The iOS manager persists a versioned pending-outbound queue containing packets plus retry state. Its inspected constants bound the queue at 200 packets, expire pending packets after two minutes, and use retry backoff beginning at 1.5 seconds and capped at 15 seconds. The queue is loaded during manager initialization and periodic flush/recovery work is scheduled.

Android exposes closely aligned limits: pending outbound packets are restored only within a two-minute age window, recovery runs on a one-second interval, and retry backoff is bounded from 1.5 to 15 seconds. This is materially stronger than simply retrying writes in memory until the process dies.

### Receipts and chat state

The protocol has explicit `delivered` and `read` receipt types. The iOS chat path marks remote messages read when the chat is opened and sends read receipts for the resulting message IDs. The Android/iOS UI/store models expose queued/sending/sent/delivered/read-style state rather than collapsing intermittent delivery into a single boolean.

### Cross-platform protocol evidence

The iOS protocol source explicitly labels image-blob v5 as wire-compatible with Android and carries a versioned family (`dcs-gattmesh-v1` through v5 surfaces inspected). The iOS test suite contains concrete protocol tests for encrypted chat encode/decode, receipt-ID round trips, v4 authenticated-origin fields, auth-challenge nonce round trips and stale/future timestamp rejection.

Android independently defines matching core transport limits including 4,096-byte packets, four forwarding hops, 24-hour message freshness, two-minute future skew, 40 receipt IDs and the same 1.5-to-15-second outbound retry window. This is good source-level interoperability evidence, but GitHub Gold did **not** find or execute a full Android↔iOS golden-vector or multi-device interoperability test in this pass.

### Congestion / abuse bounds

The Android service has explicit inbound rate limiting (180 packets per 10-second window), packet/text/encrypted-field ceilings, bounded tracked IDs and multiple connection/recovery grace windows. The project threat model calls out payload, queue, hop, freshness and rate bounds as mesh controls.

## Useful implementation surfaces

- `Android/app/src/main/java/com/auralis/crisisconnect/service/gattmesh/GattMeshForegroundService.kt` — main Android GATT mesh transport, relay, queue, limits and recovery.
- `iOS/Crisis Connect/Services/Connectivity/GattMeshProtocol.swift` — compact packet schema, versioning, validation, encryption fields, hop/freshness limits and receipts.
- `iOS/Crisis Connect/Services/Connectivity/GattMeshManager.swift` — CoreBluetooth runtime, duplicate tracking, persistent queue, retry/backoff, relay and blob transfer.
- `iOS/Crisis ConnectTests/Crisis_ConnectTests.swift` — protocol round-trip and freshness tests.
- `Android/app/src/main/java/com/auralis/crisisconnect/service/gattmesh/MeshLaneSelector.kt` — pure policy deciding when larger blobs should additionally use Wi-Fi-class acceleration while BLE remains the baseline; a dedicated unit test exists.
- `Android/app/src/main/java/com/auralis/crisisconnect/service/gattmesh/MeshAccelerator.kt` — abstraction for optional faster media/blob lanes without changing the logical mesh payload model.

## License

Repository root: **GNU AGPL-3.0**. Third-party mobile/Bluetooth/crypto/media dependencies retain their own terms. No Crisis Connect implementation source was copied into GitHub Gold.

## Caveats / limitations

- Source-level symmetry is not equivalent to proven Android↔iOS radio interoperability. No physical cross-platform mesh was exercised by GitHub Gold.
- The inspected iOS unit tests cover packet serialization/security/freshness primitives, but do not by themselves prove multi-hop delivery, dedup behavior under cycles, queue crash recovery, background execution or congestion behavior.
- A two-minute pending-queue expiry is a deliberate bounded-recovery policy; it may be too short for some disaster-network requirements and should not be generalized blindly.
- Four-hop forwarding is a fixed policy rather than adaptive routing. This is a bounded flooding/relay design, not a sophisticated route-discovery protocol.
- Bluetooth background behavior is platform-dependent and requires physical-device validation.
- Media/blob paths have additional single-hop and fast-lane constraints; do not assume every packet type receives identical multi-hop treatment.
- Emergency use requires field testing, battery/range characterization, hostile-peer testing and protocol review beyond repository inspection.

## Verification performed by GitHub Gold

Inspected the current upstream Android/iOS source, iOS protocol tests, Android transport limits, threat-model references and root AGPL-3.0 license. Compared core constants and semantics across Android and iOS at source level.

**Not performed:** Android/iOS build; test execution; BLE packet capture; physical multi-device test; Android↔iOS golden-vector execution; process-kill queue-recovery test; battery/range benchmark; congestion/failure injection; cryptographic audit; disaster field trial.

## Follow-up research

1. Search for or construct upstream-independent **cross-platform golden vectors** covering v1-v5 packet JSON, encrypted chat AAD, receipts, hop incrementing and malformed-frame rejection.
2. Inspect queue persistence semantics under app kill/reboot, especially whether receipt state and dedup state survive independently of outbound packets.
3. Trace the **MeshAccelerator / MeshLaneSelector / Wi-Fi Direct / Wi-Fi Aware fast-lane** path: it may be a reusable architecture for keeping BLE as a universal control plane while opportunistically moving large blobs onto faster local transports.
4. Verify how emergency/SOS priority interacts with ordinary queue congestion and whether priority inversion is possible.
