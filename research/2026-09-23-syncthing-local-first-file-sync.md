# Syncthing — local-first continuous file synchronization

- **Repository:** https://github.com/syncthing/syncthing
- **Author / Org:** Syncthing
- **Category:** local-first / file synchronization / peer-to-peer infrastructure / offline-capable systems
- **Evidence:** VERIFIED
- **Gold score:** 29 / 30
- **Tier:** S
- **Discovery source:** GitHub-first category rotation after completing the PMTiles/Planetiler/Tippecanoe mapping research chain.

## What it does

Syncthing is a continuous file synchronization system for synchronizing files between two or more computers. Its stated priorities put protection from data loss and security against unauthorized access first, followed by ease of use, automation, broad availability, and individual user control.

## Why it matters

Syncthing is a strong reference implementation for user-controlled synchronization that does not make a hosted cloud storage service the conceptual center of the system. It is useful both as a complete tool and as a research target for peer discovery, NAT traversal, transport, filesystem abstraction, synchronization semantics, conflict/version handling, monitoring, and cross-platform service integration.

## Concrete working evidence inspected

- The upstream README documents a direct source build path using `go run build.go`, Docker support, multiple GUI implementations, signed release binaries, and an automatic upgrade mechanism whose updates use a compiled-in ECDSA signature.
- The repository has integration tests. `test/sync_test.go` explicitly exercises synchronization back and forth between three cluster members and includes arbitrary/non-ASCII folder identifiers.
- Filesystem-specific tests cover invalid Windows filenames, case-sensitive/case-insensitive real-case behavior, fake filesystem behavior, basic filesystem naming, and mtime handling.
- Recent default-branch commits on 2026-09-22 include a Windows detached-console logging fix with a targeted Go test, HTTP connection-management changes, and GUI accessibility work. This is active maintenance rather than a dormant historical project.
- The latest inspected GitHub release is **v2.1.5**, published **2026-09-08**, with signed checksum material and platform-specific binary archives.

These are upstream/repository-native evidence signals. GitHub Gold did not execute the test suite or perform a live synchronization test.

## Useful components / research targets

- continuous synchronization engine and cluster behavior
- filesystem abstraction and platform edge-case handling
- discovery / NAT traversal / connectivity stack
- QUIC transport dependency (`quic-go`)
- local database/storage layers
- monitoring and metrics infrastructure, including Prometheus client dependencies
- service/background-run examples under `etc/`
- signed release and automatic-update architecture
- cross-platform GUI/API integration surfaces

## Runtime / build requirements

The inspected default branch declares **Go 1.26.2** in `go.mod`. Upstream documents building with `go run build.go`. Prebuilt releases are also distributed for multiple operating-system/architecture combinations.

## Platforms

Upstream's goal is availability on common computers. Current release artifacts include multiple OS/architecture builds; README specifically references GUI implementations for Windows, macOS and Linux and documents Docker operation.

## License

**Mozilla Public License 2.0 (MPL-2.0).**

This is file-level copyleft. If covered Syncthing source files are modified and distributed, MPL obligations apply to those covered files. A larger work can contain separately licensed material subject to MPL requirements for the covered software. GitHub Gold copied no Syncthing implementation source.

## Maintenance signals

- Not archived at inspection time.
- Release v2.1.5 published 2026-09-08.
- Default-branch commits observed through 2026-09-22.
- Repository contains unit/integration tests and explicit testing notes in recent fixes.
- Signed release/checksum infrastructure is documented upstream.

## Verification performed

Inspected repository metadata, README, LICENSE, `go.mod`, test search results, latest release metadata, and recent commit history. Confirmed concrete integration/unit-test presence and active 2026 maintenance from repository-native evidence.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- build Syncthing;
- execute its tests;
- run two or more nodes;
- verify discovery/NAT traversal on a live network;
- measure synchronization performance or bandwidth use;
- test conflicts, versioning, corruption recovery, or interrupted transfers;
- independently audit its cryptography or update-signing implementation;
- verify every platform artifact.

## Caveats / risks

- Synchronization is not the same thing as backup: synchronized deletion or unwanted modification can propagate depending on configuration. Users requiring backup semantics should separately design retention/versioning and independent backup layers.
- Filesystem semantics differ substantially across Windows, macOS, Linux and network filesystems; the extensive filesystem test surface is evidence that these edge cases are material.
- NAT traversal, relays and discovery behavior depend on network topology and configuration; no live-network verification was performed here.
- MPL-2.0 obligations must be respected before copying/adapting covered source.

## Score rationale

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Solves a common, concrete file synchronization problem without requiring a conventional hosted storage service as the primary architecture. |
| Working Evidence | 5 | Releases, signed artifacts, integration tests, filesystem tests and active fixes provide strong repository-native evidence. |
| Reusability | 5 | Valuable as a complete tool and as a source of architectural patterns/components across transport, filesystems, discovery and monitoring. |
| Novelty | 4 | Peer-to-peer synchronization is established technology, but the mature user-controlled architecture remains technically valuable. |
| Documentation | 5 | README, documentation site, build instructions, goals, Docker guidance and protocol documentation are exposed upstream. |
| Maintenance | 5 | Current release and default-branch activity observed in September 2026. |

**Total: 29 / 30 — S tier.**

## Related / recursive leads

1. `syncthing/docs` — inspect the Block Exchange Protocol and discovery/relay specifications as reusable protocol references.
2. Syncthing relay/discovery infrastructure — map what can be self-hosted and what remains optional for LAN/offline operation.
3. `syncthing/syncthing-android` or current Android ecosystem — determine current Android status and viable Termux/mobile integration paths rather than assuming desktop behavior maps directly to Android.
4. Compare with local-first synchronization engines such as LocalSend, Unison, Mutagen, and CRDT-oriented systems, but avoid adding them until repository-native evidence meets the same bar.
