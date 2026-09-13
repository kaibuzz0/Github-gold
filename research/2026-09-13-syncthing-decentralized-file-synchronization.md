# Syncthing — decentralized continuous file synchronization

- **Repository:** https://github.com/syncthing/syncthing
- **Organization:** Syncthing
- **Category:** local-first / peer-to-peer synchronization / offline systems / networking / data integrity
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary language:** Go
- **License:** Mozilla Public License 2.0 (MPL-2.0)
- **Discovery source:** Independent GitHub-first breadth pass; selected after duplicate check against the current GitHub Gold branch
- **Inspection date:** 2026-09-13

## Executive finding

`syncthing/syncthing` is a mature continuous file synchronization system that synchronizes folders directly between user-controlled devices. It is materially different from a one-shot LAN transfer tool such as LocalSend: Syncthing maintains replicated folder state, exchanges file indexes and content blocks, discovers peers, negotiates connections, handles version conflicts and continuous rescanning/watching, and can operate across local or routed networks without depending on a centralized storage provider.

Upstream explicitly prioritizes prevention of data loss and protection against unauthorized eavesdropping or modification before convenience goals. For GitHub Gold, the project is valuable both as a complete application and as a deep implementation reference for replicated-state synchronization, block transfer, device identity, discovery, relay connectivity, filesystem watching, conflict handling, and cross-platform packaging.

## Why it matters

Syncthing represents a high-value local-first architecture because its useful technical surface extends well beyond the user-facing application:

1. decentralized synchronization between user-controlled devices;
2. a documented Block Exchange Protocol (BEP) implementation;
3. content block hashing and reuse across files/folders;
4. local/global discovery infrastructure;
5. NAT traversal and relay connectivity support;
6. persistent index/database machinery and replicated folder models;
7. event, API, configuration, filesystem, ignore-pattern, and connection-management libraries;
8. signed cross-platform release and automatic-upgrade infrastructure.

This combination makes it useful for offline-first personal infrastructure, field systems, small private networks, self-hosted workflows, and as a reference architecture for resilient synchronization software.

## High-value components

The current `lib/` tree exposes reusable or research-worthy packages including:

- `lib/protocol` — Block Exchange Protocol implementation and device/file protocol structures;
- `lib/model` — replicated-folder/device state and synchronization model;
- `lib/connections` — connection lifecycle and transport coordination;
- `lib/discover` — peer/device discovery mechanisms;
- `lib/nat` — NAT traversal helpers;
- `lib/fs` — cross-platform filesystem abstraction;
- `lib/ignore` — ignore-pattern handling;
- `lib/events` — internal/event API plumbing;
- `lib/api` — API-layer support;
- `lib/config` — configuration model and persistence;
- `lib/netutil` and `lib/dialer` — reusable networking utilities;
- `cmd/stdiscosrv` — discovery server implementation;
- `cmd/strelaysrv` — relay server implementation;
- `cmd/syncthing` — primary daemon/application entry point.

The repository also includes manpages documenting the Block Exchange Protocol, configuration, operation, and behavior.

## Protocol architecture

The source package documentation explicitly states that `lib/protocol` implements the **Block Exchange Protocol**. The checked-in `syncthing-bep` manual describes BEP as the protocol used between two or more devices forming a cluster, with devices sharing one or more folders.

The project also documents a block-oriented transfer model: files are segmented into blocks so synchronization work can be distributed between devices, and optional block indexing can enable block reuse across files and folders.

These capabilities make Syncthing particularly interesting as a reference for chunked transfer, replicated metadata, and multi-peer synchronization rather than simple file copying.

## Build and runtime profile

The upstream README documents a source build using:

`go run build.go`

The current `go.mod` declares **Go 1.26.2** as the module language version, while current CI tests both the Go 1.26 and 1.27 release lines.

The dependency set indicates substantial networking and infrastructure support, including QUIC, STUN, NAT-PMP, SQLite/LevelDB, Prometheus instrumentation, LZ4, protobuf, cryptographic primitives, and platform-specific system packages.

Syncthing distributes native builds across major desktop/server operating systems and also documents Docker deployment. Release assets inspected for the current stable version include multiple architecture/OS combinations.

## Working evidence

Repository-native evidence is strong.

### Cross-platform build and test matrix

The current `Build Syncthing` GitHub Actions workflow runs a matrix on:

- Windows;
- Ubuntu/Linux;
- macOS;

against both:

- Go 1.26.x;
- Go 1.27.x.

For each matrix entry, upstream performs a real source build using `go run build.go` and then executes the project's test harness with `go run build.go test`.

The workflow's aggregate gate also depends on packaging and quality jobs rather than test compilation alone. Observed required jobs include:

- Linux packaging;
- illumos packaging;
- cross-platform packaging;
- source packaging;
- Debian packaging;
- Windows packaging;
- `govulncheck`;
- `golangci`;
- metadata/correctness checks.

The Windows packaging job cross-builds Syncthing, the discovery server, and the relay server for amd64, 386, and arm64 and archives the resulting packages.

GitHub Gold did not execute these workflows; this is upstream evidence.

### Security and release pipeline signals

The README states that release binaries are GPG-signed, that the built-in automatic updater uses a compiled-in ECDSA signature, and that macOS and Windows binaries are code-signed.

The inspected build workflow also contains explicit commentary about minimizing third-party action trust on paths leading to packaged/signed artifacts, demonstrating deliberate supply-chain consideration in the release process.

## Current release and maintenance evidence

The latest stable GitHub release inspected is **v2.1.5**, published **2026-09-08**.

The release exposes platform-specific binary archives plus signed checksum material. GitHub's release API also provides SHA-256 digest metadata for individual assets.

Development remains current through **2026-09-12**. Recent inspected commits include:

- a model correctness fix preventing introducer devices from adding themselves to folders they should not be able to vouch for;
- accessibility labels for device-editing controls;
- simplified security-reporting documentation;
- recent discovery-service and upgrade infrastructure maintenance.

The introducer fix is notable because it affects synchronization trust/authorization semantics rather than cosmetic maintenance.

## Useful architectural patterns

### Device identity and trust

Syncthing's model is device-centric rather than account-centric. This makes its identity and trust model useful for studying user-controlled systems that need persistent peer identities without relying on a central cloud account.

### Discovery plus direct/relay connectivity

The project separates discovery, connection establishment, and relay services rather than conflating synchronization logic with one fixed network path. That modularity is useful for intermittent, NAT-constrained, or mixed local/remote networks.

### Block-oriented synchronization

The documented block model allows the implementation to transfer only required data and reuse matching blocks, a pattern relevant to bandwidth-constrained replication and content-addressed synchronization designs.

### Cross-platform filesystem behavior

`lib/fs`, model code, scanning, ignore handling, and filesystem-specific test behavior provide a significant reference surface for applications that must synchronize files consistently across Windows, macOS, Linux, and other Unix-like systems.

## Licensing

The repository is licensed under **Mozilla Public License 2.0**.

MPL-2.0 is file-level copyleft. Covered source files and modifications to them carry MPL obligations when distributed, while MPL generally permits combination with separate files under different licenses subject to its terms.

GitHub Gold did not copy Syncthing source. Any later extraction or adaptation of individual components should preserve the MPL notices and evaluate dependency-specific licenses independently.

## Relationship to existing GitHub Gold entries

Syncthing complements, rather than duplicates, `localsend/localsend`.

- **LocalSend:** direct local-network file/message transfer, optimized for explicit send/receive workflows.
- **Syncthing:** persistent multi-device replicated-folder synchronization with indexes, block exchange, peer discovery, relay support, conflict/state handling, and continuous operation.

This distinction is important for the catalog taxonomy: both are local-first, but they solve different data-movement problems.

## Verification performed

GitHub Gold inspected:

- repository metadata and default branch;
- README goals, build instructions, security/release-signing notes, and license declaration;
- root MPL-2.0 license;
- current `go.mod`, Go version, and major dependency surface;
- `lib/` package organization;
- Block Exchange Protocol package/documentation references;
- current GitHub Actions workflow and build/test matrix;
- latest stable GitHub release metadata and asset digests;
- recent upstream commit history through 2026-09-12;
- current GitHub Gold branch for duplicate status.

## Verification boundaries

GitHub Gold did **not**:

- compile Syncthing;
- run its Go tests;
- synchronize files between devices;
- test conflict resolution;
- test local/global discovery;
- operate the discovery or relay servers;
- inspect live BEP traffic;
- benchmark block reuse or synchronization throughput;
- test NAT traversal or QUIC paths;
- perform a security audit of device identity, TLS, BEP, the REST API, or GUI;
- independently verify release signatures or reproduce release binaries;
- test upgrade rollback or failure behavior.

Claims in this dossier therefore distinguish upstream/repository-native evidence from actions actually performed by GitHub Gold.

## Caveats and risks

- A synchronization engine can propagate deletions or unwanted changes as well as desired changes; upstream's emphasis on data-loss safety does not replace backups.
- Complex filesystem semantics differ by operating system and can create edge cases around permissions, case sensitivity, links, metadata, or file locking.
- Exposing management/API surfaces beyond trusted interfaces requires careful configuration.
- Discovery/relay infrastructure improves reachability but adds network-facing components that should be assessed separately for hostile-network deployments.
- MPL-2.0 obligations apply to covered source reuse and modifications.
- Broad CI and signed releases are strong evidence, but they are not equivalent to independent reproducible-build verification by GitHub Gold.

## Strongest follow-up leads

1. `lib/protocol` BEP framing, index updates, block requests, compression, and compatibility behavior.
2. Device ID derivation and TLS/device-authentication trust semantics.
3. Folder index/version-vector and conflict-resolution logic.
4. Block hashing, block reuse, deduplication, and partial-file transfer behavior.
5. `lib/discover` local/global discovery protocol and privacy tradeoffs.
6. `strelaysrv` relay protocol, resource controls, and abuse resistance.
7. NAT traversal, QUIC, and connection-priority/fallback behavior.
8. Filesystem watcher/scanner consistency across Windows, macOS, Linux, BSD, and network filesystems.
9. Database/index corruption recovery and crash-consistency behavior.
10. Differential or fault-injection testing for interrupted synchronization, rename/delete races, and concurrent peer updates.