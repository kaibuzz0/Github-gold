# Syncthing — decentralized continuous file synchronization

- **Repository:** https://github.com/syncthing/syncthing
- **Organization:** Syncthing
- **Category:** local-first / peer-to-peer file synchronization / networking / self-hosting
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary language:** Go
- **License:** MPL-2.0
- **Discovery source:** GitHub-first category rotation into local-first resilient infrastructure
- **Inspection date:** 2026-10-01

## Executive finding

Syncthing is mature decentralized continuous file-synchronization infrastructure. Its practical value is direct device-to-device synchronization without requiring users to place their files in a central cloud service. The repository is also a strong systems reference for peer discovery, authenticated transport, block-level synchronization, conflict handling, filesystem watching, protocol evolution, release engineering and cross-platform networking.

## Why it matters

The upstream project explicitly prioritizes avoiding data loss and protecting synchronized data against unauthorized eavesdropping or modification. It is designed for individual-controlled synchronization and broad platform availability.

For GitHub Gold, the strongest value is not popularity but the combination of a long-lived production implementation, documented protocol, reproducible source build path, signed release machinery, substantial tests/build automation and active maintenance.

## High-value technical surfaces

- Block Exchange Protocol and synchronization state machinery.
- Device identity and authenticated peer connectivity.
- Local/global discovery and relay-assisted connectivity.
- Filesystem scanning, watching and change aggregation.
- Block hashing, reuse and transfer scheduling.
- Conflict/version handling and index exchange.
- REST/API and web-GUI integration.
- Service/background-process configurations.
- Cross-platform build and release infrastructure.
- Signed update/release mechanisms.

These are research surfaces observed from repository structure and upstream documentation; GitHub Gold did not independently validate every subsystem.

## Working and maintenance evidence

The README provides a direct source-build path using `go run build.go`.

The newest stable GitHub release observed was **v2.1.5**, published **2026-09-08**. GitHub release metadata exposes signed checksum files and numerous platform artifacts.

The repository remained active through **2026-09-30**. A recent merged fix corrected HTTP client handling so TLS advertising of HTTP/2 matched actual client behavior and removed an old insecure usage-reporting option. Another recent fix corrected floating-point duration conversion in the filesystem watch aggregator. These are concrete maintenance signals in networking and file-change handling.

The GitHub workflow inventory includes large build, release, nightly and infrastructure workflows. GitHub Gold did not execute them.

## Distribution and trust signals

The README states that release binaries are GPG signed. It also documents a built-in automatic-upgrade mechanism using a compiled-in ECDSA signature, with macOS and Windows binaries additionally code-signed.

Those are upstream-supported release properties. GitHub Gold did not independently verify signatures or the update chain.

## Licensing

The repository's root license is **Mozilla Public License 2.0 (MPL-2.0)**. MPL is file-level copyleft: copying or modifying covered source requires preserving applicable MPL obligations. No Syncthing source was copied into GitHub Gold in this run.

## Important caveats

- Synchronization is not a substitute for independent backups; deletion/corruption can propagate depending on configuration and versioning strategy.
- Connectivity may involve discovery and relay infrastructure depending on network topology/configuration.
- Security properties depend on correct device identity, configuration, software updates and endpoint security.
- Cross-platform filesystem semantics can differ for permissions, case sensitivity, special files and filename rules.
- The old official `syncthing-android` repository is archived; Android deployment should be treated as a separate ecosystem/support question rather than inferred from the core repository.
- Signed-release claims were inspected but not independently cryptographically verified.

## Verification performed by GitHub Gold

Inspected:
- repository metadata;
- README and stated project goals;
- root MPL-2.0 license;
- current release metadata and signed-checksum artifacts;
- recent commit history;
- GitHub Actions workflow inventory;
- existing Github-gold catalog/research search results to avoid duplication.

## Verification NOT performed

GitHub Gold did **not**:
- compile Syncthing;
- execute its tests;
- synchronize files between devices;
- induce conflicts or data-loss scenarios;
- test discovery/NAT traversal/relays;
- inspect packets;
- verify release signatures;
- test automatic upgrades;
- benchmark throughput or resource use;
- perform a security audit.

## Gold rationale

**Utility — 5/5:** highly practical user-controlled continuous file synchronization.

**Working Evidence — 5/5:** mature releases, build instructions, signed distribution, substantial automation and current fixes.

**Reusability — 5/5:** protocol, networking, filesystem, discovery, relay and synchronization machinery offer substantial reusable/reference value.

**Novelty — 4/5:** file synchronization is established, but Syncthing's decentralized architecture and mature protocol ecosystem remain technically distinctive.

**Documentation — 5/5:** extensive official docs, protocol specifications and build/operational guidance.

**Maintenance — 5/5:** v2.1.5 released 2026-09-08 with active code maintenance through 2026-09-30.

**Provisional total: 29/30 — S tier.**

## Recursive research queue

1. Inspect BEP v1 message/state semantics and compatibility strategy.
2. Trace device-ID generation, TLS identity and trust establishment.
3. Map local/global discovery and relay fallback behavior.
4. Inspect block selection, hashing and reuse algorithms.
5. Study conflict resolution and version-vector behavior.
6. Inspect filesystem watcher aggregation and cross-platform normalization.
7. Review release-signing and automatic-upgrade trust boundaries.
8. Map current Android/mobile ecosystem after archival of the old official Android repository.
