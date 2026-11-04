# Syncthing — peer-to-peer continuous file synchronization

- **Upstream:** https://github.com/syncthing/syncthing
- **Category:** local-first / peer-to-peer synchronization / resilient networking
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29/30 — S tier
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 5/5
  - Maintenance 5/5
- **License:** MPL-2.0
- **Discovery:** GitHub-first breadth rotation; checked against the existing Github-gold catalog before addition and found no Syncthing entry.

## Why it is Gold

Syncthing is a mature continuous file synchronization engine for directly synchronizing files between user-controlled devices. It is particularly relevant to Github-gold's local-first/offline/resilient-infrastructure track because it does not require a central file-storage service: peers can discover and connect locally or across networks, with relay infrastructure available when direct connectivity is unavailable.

This is also a useful source of reusable architecture rather than merely an end-user application. The repository exposes protocol, model, filesystem, discovery, connection, database/index, event, REST/API, upgrade, and GUI surfaces, and maintains separate ecosystem projects for global discovery and relay infrastructure.

## Concrete evidence inspected

### Repository structure and engineering surface

The current repository contains `cmd`, `internal`, `lib`, `proto`, `test`, `gui`, build tooling, compatibility metadata, man pages, and multiple GitHub Actions workflows. The root README documents a source build through `go run build.go` and identifies safety from data loss and security against attackers as its first two project goals.

### Security model

Current upstream security documentation states that device-to-device traffic is protected by TLS. Device admission is tied to certificate fingerprints represented as Device IDs, rather than an unauthenticated open cluster. This is important evidence for its usefulness in user-controlled peer synchronization, but it is not an independent cryptographic audit by Github-gold.

### Networking and offline/local operation

Current networking documentation describes direct TCP/UDP synchronization, local discovery through broadcast/multicast, static addresses where discovery is unsuitable, NAT traversal/port forwarding, and relaying when direct connectivity cannot be established. Relays therefore improve reachability but are not the canonical storage authority for synchronized files.

### Automation/API surface

The v2.1.0 REST documentation exposes a JSON-oriented HTTP control interface used by the GUI and available to external processes. API-key or Bearer-token authentication is documented for authenticated endpoints. This makes Syncthing useful as a component behind automation, field systems, local-first applications and self-hosted orchestration rather than only as an interactive GUI program.

### Release and maintenance evidence

The latest stable release inspected is **v2.1.5**, published **2026-09-08**. GitHub's release record contains platform artifacts and published digest files including `sha256sum.txt.asc`; the README additionally documents GPG-signed release binaries, a signed automatic-upgrade path, and code signing for macOS/Windows binaries.

The Syncthing organization remained active in September 2026: the primary repository, discovery server and relay server all show current maintenance activity. The repository also contains a large GitHub Actions build workflow plus release/nightly/supporting workflows.

## Particularly valuable components / follow-up extraction targets

1. **Block Exchange Protocol (BEP)** — protocol and protobuf surfaces for peer file/index exchange.
2. **Connection/discovery stack** — local discovery, global discovery, direct TCP/QUIC-style connectivity surfaces and relay fallback are useful patterns for intermittently connected systems.
3. **Index/database model** — synchronization metadata and global/local file model are strong research targets for conflict handling and resumable replication.
4. **REST/event interfaces** — useful for embedding Syncthing behind other local-first software without reimplementing synchronization.
5. **`discosrv` / `relaysrv` ecosystem** — independently deployable discovery and relay services warrant component-level dossiers.
6. **Release integrity pipeline** — signed checksums, signed upgrades and multi-platform release production are useful supply-chain patterns.

## Requirements / platforms

The implementation is predominantly Go and is designed for common desktop/server operating systems, with platform-specific distribution/wrappers across the ecosystem. Exact supported targets should be taken from the release/build matrix for a particular version rather than inferred from historical packages.

## Licensing caveat

The root project is **Mozilla Public License 2.0**. MPL-2.0 is file-level copyleft: copying or modifying covered source requires preserving the applicable MPL obligations and notices. No Syncthing implementation code is copied into Github-gold by this dossier. Dependencies, wrappers and companion projects must be checked independently before extraction or redistribution.

## Evidence boundary

Github-gold **did not** build or run Syncthing during this pass, synchronize a test corpus, induce conflicts, interrupt/resume transfers, operate a relay/discovery server, packet-capture traffic, audit its cryptography, reproduce data-loss tests, or verify release signatures locally. `VERIFIED` here means there is unusually strong repository-native evidence of working functionality: a long-lived implementation, current releases, documented build path, test tree, CI/release workflows, active maintenance and production-oriented protocol/security documentation. Performance, security and reliability claims remain upstream evidence unless independently reproduced.

## Strong next research questions

- Inspect BEP framing, versioning, validation and resource-limit behavior.
- Trace conflict resolution and file-version semantics through the model tests.
- Inspect resumable block transfer and corrupted-block recovery tests.
- Map direct connection versus relay metadata exposure and trust boundaries.
- Inspect `discosrv` and `relaysrv` as standalone reusable infrastructure.
- Review current Android ecosystem status separately; do not infer Android support from third-party forks without checking their current maintenance and licensing.
