# Geogram — off-grid community platform

- Upstream: https://github.com/geograms/geogram
- Evidence level: VERIFIED (upstream evidence; not independently runtime-tested by GitHub Gold)
- Provisional Gold score: 27/30 — S tier
- Category: offline-first communications / community infrastructure / mapping / embedded
- License: Apache-2.0 (root source license)
- Discovery: independent GitHub-first breadth rotation

## Why it matters

Geogram is an unusually broad local-first communications stack spanning Android, Linux, ESP32, and additional less-tested targets. It combines direct device discovery and transport selection, signed messaging, local/station operation, offline map caching, community data applications, queued transfers, and optional local AI. The architecture is interesting less as a single chat app than as a reusable pattern for community infrastructure that can continue operating with intermittent or absent Internet access.

## Evidence inspected

The current README documents Wi-Fi/LAN, BLE, station relay and Internet paths; station operation on phones/laptops/Raspberry Pi; ESP32 station firmware; cached offline map tiles; signed messages; chat/blog/events/places/alerts/inventory/transfer/bot applications; and explicit platform status. It labels Android, Linux and ESP32 stable while Windows, macOS, iOS and Web are available but untested.

Repository-native technical material includes a transport priority table and implementation files for shared sync and Bluetooth transports. The tree also preserves BLE test/bring-up notes; notably, an older APRS/BLE test lives under `test/outdated_2026-03-07`, so it is historical evidence rather than current CI proof. Current source explicitly disables the Bluetooth Classic service in favor of pure BLE, an important qualification against older documentation that still lists Bluetooth Classic as a transport.

The latest inspected stable release is v1.39.2, published 2026-05-29. GitHub release metadata exposes CI-uploaded Android, Linux, macOS and iOS artifacts with SHA-256 digests. Release notes describe an update-center repair using a worker isolate, partial-download recovery/HTTP Range resume, cooperative cancellation and crash-hardening. Recent inspected commits align with those release notes.

## Gold scoring (provisional)

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Offline messaging, mapping, local publishing, alerts, inventory and file transfer form a useful field/community stack. |
| Working evidence | 4 | Stable-tagged release artifacts, implementation source and repository test/bring-up material; GitHub Gold did not run it. |
| Reusability | 5 | Multiple transports, human-readable app formats, station model, ESP32 firmware and documented architecture expose many reusable ideas/components. |
| Novelty | 5 | Combines local community apps, opportunistic transports, station infrastructure, offline maps and embedded nodes in one system. |
| Documentation | 5 | Large README plus technical and per-app format documentation. |
| Maintenance | 3 | Concrete 2026 release activity exists, but the latest inspected stable release/commit is May 29 and some transport docs/tests show drift. |
| **Total** | **27/30** | **S (provisional)** |

## Particularly useful components / leads

- transport abstraction and path prioritization across LAN, BLE, station and other interfaces
- `SharedSyncService` and reconnect/follow-up synchronization behavior
- offline map tile caching and station-assisted tile distribution
- transfer queue with priority, resume/retry and long-lived patient/offline-peer semantics
- ESP32 station firmware and Wi-Fi/BLE bridge design
- human-readable app data formats for chat, alerts, places, events and inventory
- verifiable-build design and deterministic release workflow
- update downloader worker-isolate + partial-file/Range-resume pattern

## Requirements / platforms

Primary upstream targets are Android, Linux and ESP32. Windows, macOS, iOS and Web are described as available but untested. The project uses Flutter/Dart with native/embedded components and bundles substantial local dependencies; published binaries are intentionally large. ESP32 support includes C3-mini, S3 ePaper and generic variants according to upstream documentation.

## Licensing / provenance

The repository root license is Apache-2.0. No upstream source has been copied into GitHub Gold. Any bundled models, map imagery/data, media runtimes, native libraries, firmware dependencies or other third-party assets need component-level license/provenance review before extraction or redistribution.

## Caveats

- GitHub Gold did not build, install or execute Geogram.
- No BLE/Wi-Fi/station synchronization was independently reproduced.
- No ESP32 firmware was built or flashed.
- Offline maps, cryptographic identity/signing, local AI and verifiable-build claims were not independently audited.
- Current source disables Bluetooth Classic while some documentation still lists it; treat BLE as the current Bluetooth path until reconciled upstream.
- An APRS/BLE test surfaced under an explicitly outdated test directory and must not be treated as current CI evidence.
- Published artifacts and digests establish release packaging, not functional correctness or security.

## Follow-up research

1. Trace the current BLE framing, discovery and reconnect state machine end-to-end and identify current tests.
2. Inspect `SharedSyncService` conflict/idempotency semantics and persistence across restart.
3. Audit map-tile provenance, cache format and peer/station transfer protocol.
4. Inspect ESP32 firmware license boundaries, OTA trust model and bridge protocol.
5. Inspect signed-message key lifecycle, replay handling and identity migration/revocation.
6. Verify the documented deterministic/verifiable-build procedure against a tagged release.
7. Reconcile transport documentation with the currently disabled Bluetooth Classic implementation.
