# Crisis Connect — opportunistic Wi-Fi fast lanes over a BLE baseline

- **Repository:** https://github.com/emirhan-duman/Crisis-Connect
- **Component:** Android `MeshAccelerator` / `MeshAcceleratorCoordinator` / `MeshLaneSelector`, Wi-Fi Aware and Wi-Fi Direct accelerators
- **Category:** Emergency communications / offline mesh / Android networking / resilient transport
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **27/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 4/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 4/5
- **Primary language:** Kotlin
- **License:** AGPL-3.0 at repository root; dependencies retain their own terms
- **Discovery source:** Recursive research from the previously cataloged Crisis Connect GATT mesh relay
- **Inspection date:** 2026-09-26

## Executive finding

Crisis Connect contains a useful resilient-transport pattern: keep BLE GATT as the universal delivery baseline, then opportunistically duplicate larger encrypted media blobs onto faster local Wi-Fi transports. The Android implementation abstracts these optional transports behind `MeshAccelerator`, coordinates them with `MeshAcceleratorCoordinator`, and uses a side-effect-free `MeshLaneSelector` policy to decide when the extra radio work is worthwhile.

The design is valuable because an accelerator is not required for correctness. If Wi-Fi Aware or Wi-Fi Direct is unsupported, unprovisioned, unavailable, or fails to connect, the baseline BLE path still carries the blob. Receivers deduplicate by blob ID, so the first copy to arrive wins and later copies can be discarded.

## Architecture

### `MeshAccelerator`

The interface defines a deliberately small transport contract:

- stable lane identifier;
- capability detection;
- start/stop lifecycle;
- fast-peer availability;
- fire-and-forget delivery of an already encrypted blob.

Its contract explicitly requires implementations to fail softly: unsupported/unprovisioned lanes should quietly decline to start, and `offerBlob` should be harmless when no fast peers are available.

This separation is reusable. The message-security and deduplication model lives outside the transport-specific radio implementation, allowing additional local transports to be added without making them mandatory dependencies of the mesh.

### `MeshAcceleratorCoordinator`

The coordinator starts every supported accelerator independently and wraps lifecycle and send calls with failure isolation. One lane failing to start or send therefore does not directly take down the others.

For blob delivery, the coordinator first applies `MeshLaneSelector`. Only payloads large enough to justify a fast path are offered to the Wi-Fi-class lanes. BLE remains outside the coordinator as the universal baseline.

### `MeshLaneSelector`

The current policy is intentionally simple and deterministic:

- blobs smaller than **16 KiB** use BLE alone;
- blobs at or above **16 KiB** are additionally offered to the fast lanes.

Upstream comments explain the tradeoff: duplicating tiny blobs onto another radio adds redundant work for little latency benefit, whereas larger payloads can benefit from Wi-Fi bandwidth. The policy is isolated as a pure function so it can be tested and later replaced by richer per-peer decisions.

The source itself identifies a useful future refinement: lane selection could incorporate measured BLE RSSI and fast-lane throughput instead of relying only on payload size.

## Concrete fast lanes

### Wi-Fi Aware

`AuthorityMeshAwareAccelerator` is identified by the interface documentation as the reference accelerator implementation. It provides the Aware lane when supported.

### Wi-Fi Direct

`WifiDirectAccelerator` is a broader-coverage fallback for Android devices without usable Wi-Fi Aware. The inspected implementation requires Android Q/API 29 or later and Wi-Fi Direct support. It deliberately defers to Aware where Aware is usable because the two mechanisms can be mutually exclusive on device radios.

The implementation documents a deterministic peer topology:

- authority peers advertise persisted node IDs through Wi-Fi Direct DNS-SD;
- the lowest node ID becomes group owner;
- group credentials are derived from the authority group key on API 29+;
- clients connect to the group owner and carry the same blob framing used by the fast-path receive/dedupe machinery.

The source explicitly calls the Wi-Fi Direct implementation a compiled, fail-soft first cut and warns that OEM Wi-Fi Direct/P2P behavior still requires on-device bring-up. This caveat materially limits the verification score.

## Security and resilience properties observed in source

The fast-lane abstraction transports the same group-key-encrypted blob rather than introducing a separate plaintext media representation. The Wi-Fi Direct source states that the payload remains group-key AES-GCM encrypted like the BLE and Aware lanes.

The useful resilience pattern is therefore:

1. create/encrypt a transport-independent blob;
2. send it on the always-available baseline path;
3. optionally race identical encrypted content over higher-bandwidth paths;
4. deduplicate at the receiver by stable blob identity;
5. allow optional lanes to fail without losing baseline delivery.

This is a strong architectural pattern for disaster communications, local-first synchronization, field robotics, opportunistic file transfer, and other systems where radio capabilities differ across peers.

## Working evidence

The repository includes a dedicated `MeshLaneSelectorTest` unit test. It verifies that zero-byte, 1 KiB, and just-below-threshold blobs remain on BLE alone, while blobs exactly at the 16 KiB threshold and a 400,000-byte payload select the additional Wi-Fi fast path.

This is direct test evidence for the lane-selection policy, not for end-to-end radio interoperability.

The implementation itself is concrete rather than pseudocode: the Wi-Fi Direct lane contains Android P2P/DNS-SD discovery, group-owner election, network setup, sockets, lifecycle cleanup, capability checks, permissions handling, and bounded blob-frame checks.

## Reusability assessment

The most reusable pieces are architectural rather than code to copy blindly:

1. **Optional accelerator interface** — separate correctness transport from performance transports.
2. **Race-and-dedupe delivery** — send the same encrypted object over multiple paths and accept the first arrival.
3. **Pure lane policy** — isolate transport-selection logic so it can be unit tested and replaced independently.
4. **Fail-soft coordinator** — one optional radio failing does not collapse baseline delivery.
5. **Capability-driven activation** — only start transports supported by the current device.
6. **Transport-independent encryption** — fast lanes do not require a second application security model.
7. **Fallback hierarchy** — Aware where suitable, Direct on Aware-less devices, BLE regardless.

Because the upstream project is AGPL-3.0, projects wishing to reuse implementation code must evaluate the license obligations carefully. Cataloging the pattern and linking upstream is safer than copying source into GitHub Gold.

## Caveats and limitations

- GitHub Gold did not build or install Crisis Connect.
- No Android devices were connected and no Wi-Fi Aware or Wi-Fi Direct session was created.
- The unit test proves only the size-selection policy.
- Physical Android↔Android or Android↔iOS fast-lane interoperability was not tested.
- The Wi-Fi Direct implementation itself warns that OEM behavior requires on-device bring-up.
- The fixed 16 KiB threshold is a heuristic, not a measured optimum across devices/radios.
- Racing copies consumes additional radio energy and airtime for large blobs.
- Aware/Direct mutual-exclusion behavior can be device-dependent.
- Security statements above are source/design observations, not an independent cryptographic audit.
- The group-owner election and credential derivation deserve adversarial and collision/failure testing.
- The fast-lane implementation is Android-specific; BLE remains the more universal cross-platform baseline in the inspected architecture.

## Verification performed by GitHub Gold

This run inspected:

- `MeshAccelerator.kt`;
- `MeshAcceleratorCoordinator.kt`;
- `MeshLaneSelector.kt`;
- `MeshLaneSelectorTest.kt`;
- the beginning and architecture documentation of `WifiDirectAccelerator.kt`;
- repository-root AGPL-3.0 licensing;
- existing GitHub Gold research to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- compile the Android project;
- execute the unit test;
- run an emulator or physical device;
- exercise Wi-Fi Aware;
- form a Wi-Fi Direct group;
- inspect radio packets;
- measure throughput, latency, range, battery cost, or reconnection time;
- test OEM-specific P2P behavior;
- perform fault injection;
- audit AES-GCM key management or credential derivation;
- verify end-to-end interoperability with iOS.

## Gold rationale

**Utility — 5/5:** directly relevant to resilient offline communications and transferable to other heterogeneous-radio systems.

**Working Evidence — 4/5:** concrete Android implementations and a unit-tested selection policy exist, but physical fast-lane operation was not independently verified and upstream flags Wi-Fi Direct as needing device bring-up.

**Reusability — 5/5:** interface/coordinator/policy separation and transport-independent encrypted blobs are broadly reusable patterns.

**Novelty — 5/5:** the always-on BLE correctness path combined with opportunistic racing over multiple Wi-Fi-class lanes is a strong, practical composition.

**Documentation — 4/5:** source-level documentation is unusually explanatory, but the component does not yet present itself as a standalone reusable library/specification.

**Maintenance — 4/5:** the component is part of the actively developed Crisis Connect tree inspected in the surrounding research batch, but its long-term API stability is not established.

**Provisional total: 27/30 — S tier.**

## Next research queue

1. Inspect `AuthorityMeshAwareAccelerator` and `BlobLink` framing in full.
2. Trace stable blob IDs and receiver-side cross-lane deduplication.
3. Determine whether iOS has an equivalent fast-lane implementation or remains BLE-only for this path.
4. Inspect tests around accelerator coordination, socket framing, and corrupted/oversized frames.
5. Model energy/latency tradeoffs for dynamic lane selection.
6. Evaluate per-peer policy using RSSI, measured throughput, queue pressure, and battery state.
7. Test failure cases conceptually: Aware loss mid-transfer, Direct group-owner disappearance, duplicate late arrival, and simultaneous lane recovery.
8. Rotate the next primary discovery pass into a different technical category after these component boundaries are documented.