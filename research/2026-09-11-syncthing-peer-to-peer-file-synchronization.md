# Syncthing — peer-to-peer continuous file synchronization

- **Repository:** https://github.com/syncthing/syncthing
- **Organization:** Syncthing
- **Category:** local-first / peer-to-peer synchronization / offline networking / file replication / self-hosting
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary language:** Go
- **License:** MPL-2.0
- **Discovery source:** GitHub-first category rotation from the storage/backup branch
- **Inspection date:** 2026-09-11

## Executive finding

Syncthing is a mature continuous file-synchronization system for directly synchronizing files between two or more user-controlled devices. It is not merely a cloud-storage client: the core product includes a peer protocol, device identity model, connection management, filesystem scanning/watching, block-oriented transfer, conflict handling, discovery/relay infrastructure, a local administration/API surface, database/index machinery, and cross-platform packaging.

The project is especially valuable to GitHub Gold as a reference for local-first and intermittently connected systems. Its architecture shows how to build a replicated file system without requiring a central storage provider while still supporting discovery and relay services when direct device connectivity is difficult.

Upstream explicitly prioritizes protection against data loss and attackers, automatic operation, broad platform availability, and individual user control.

## Why it matters

Syncthing is useful operationally for:

- direct workstation-to-workstation synchronization;
- home-lab and self-hosted file replication;
- synchronization across LAN, internet, VPN, and intermittently connected environments;
- maintaining copies of working data across personally controlled devices;
- offline-first workflows where a cloud storage provider is undesirable;
- peer replication through direct connections with relay/discovery fallbacks;
- controlled folder sharing among known device identities.

It also provides strong reusable design references for:

- peer authentication and device identity;
- block-based synchronization;
- change detection and filesystem watching;
- conflict/version handling;
- transport negotiation;
- NAT traversal and relay fallback;
- peer discovery;
- metadata/index databases;
- local REST/control APIs;
- cross-platform service packaging;
- update and release-signing infrastructure.

Syncthing complements the existing GitHub Gold entries for LocalSend, rclone, and restic. LocalSend focuses on explicit one-shot LAN transfer, rclone on storage-provider transfer/sync abstraction, and restic on encrypted historical backups. Syncthing is a continuously converging peer-to-peer replication engine.

## High-value components and patterns

### Block Exchange Protocol

`lib/protocol` implements Syncthing's Block Exchange Protocol (BEP). The repository also contains generated/manual documentation for BEP v1 describing communication among devices participating in a cluster of shared folders.

This protocol layer is one of the strongest reusable research targets in the repository because it separates synchronization metadata and block exchange semantics from the higher-level UI.

Useful paths include:

- `lib/protocol/` — BEP implementation, message types, device identifiers, file/block metadata;
- `man/syncthing-bep.7` — protocol documentation;
- protocol serialization/generation machinery;
- connection-level Hello exchange and protocol negotiation.

GitHub Gold did not independently implement a BEP peer or verify protocol interoperability in this run.

### Block-oriented synchronization

Upstream documentation explains that files are segmented into blocks for transfer and synchronization. The block model permits useful patterns such as transferring only changed pieces and obtaining blocks from multiple peers rather than treating every file as an indivisible object.

The configuration documentation also exposes block-level reuse/indexing behavior, showing that the block index is a first-class architecture component rather than an incidental implementation detail.

This is valuable for studying content reuse and efficient replication independently of backup-specific semantics.

### Connection management and transport layer

`lib/connections` manages peer connectivity, including establishment and Hello exchange. The dependency set includes `quic-go`, STUN, NAT-PMP/gateway discovery libraries, and standard Go networking packages, showing that connectivity is designed around multiple network conditions rather than a single TCP-on-LAN assumption.

Strong follow-up targets include:

- direct TCP versus QUIC behavior;
- relay fallback;
- NAT traversal;
- transport selection and connection priority;
- connection limits/rate limiting;
- TLS/device-identity binding;
- malformed peer/protocol behavior.

### Discovery and relay infrastructure

The repository includes dedicated commands for supporting infrastructure, notably `stdiscosrv` and `strelaysrv`.

This separation is useful because Syncthing's architecture is peer-to-peer for file data while still allowing optional coordination services for locating peers or traversing difficult network topologies.

The distinction between control-plane assistance and actual peer data ownership is particularly relevant to resilient local-first systems.

### Filesystem abstraction, scanning, and watching

`lib/fs`, watcher/aggregation code, model code, and associated tests handle cross-platform filesystem differences and change observation.

The current source tree includes platform-specific filesystem tests and watcher tests, which is important evidence for a tool whose correctness depends heavily on filesystem edge cases.

Useful research targets include:

- filesystem event aggregation;
- case sensitivity differences;
- timestamp handling;
- permissions and metadata behavior;
- rename/delete races;
- temporary files and partial-transfer handling;
- filesystem watcher fallback and rescan logic.

### Model and database/index layer

`lib/model` coordinates synchronization state using device IDs, protocol indexes, configuration, events, and the database layer. The current repository also contains SQLite-backed internal database code and a substantial test surface.

This is a useful reference for translating peer index announcements and local filesystem state into synchronization actions while preserving conflict and consistency semantics.

### Local administration and API surface

Syncthing ships a local web GUI and API/control surface rather than requiring a hosted account. This makes the project a useful local-first service architecture example: the core daemon owns the state and sync engine while user-facing control remains locally addressable.

A future security pass should separately map API authentication, CSRF/browser boundaries, GUI exposure defaults, and remote-management risks.

### Automatic upgrade and release signing

The README documents a built-in automatic upgrade mechanism in channels where distributors have not disabled it. Upstream states that release binaries are GPG-signed, the built-in updater uses a compiled-in ECDSA signature mechanism, and macOS/Windows binaries are code-signed.

The current CI also contains dedicated Windows signing stages and comments explicitly recognizing third-party CI actions in release paths as a supply-chain trust boundary.

That release-engineering awareness is a useful pattern in its own right.

## Working evidence

Syncthing has unusually strong repository-native evidence.

### Cross-platform build and test matrix

The current `Build Syncthing` GitHub Actions workflow runs the build/test matrix on:

- `windows-latest`;
- `ubuntu-latest`;
- `macos-latest`.

It tests against both Go 1.26 and Go 1.27 families.

Each matrix member runs the project's build system and then executes the project test command. This is stronger evidence than a repository that merely checks formatting or compiles one platform.

### Packaging matrix

The same workflow contains explicit Windows packaging for amd64, 386, and arm64 and broader package jobs for Linux, illumos, source packages, Debian packages, and cross-platform outputs.

The release pipeline also packages companion server utilities such as discovery and relay components.

### Static/security checks

The workflow gate depends on jobs including `govulncheck`, `golangci`, metadata checks, platform package builds, and the test matrix.

GitHub Gold did not execute these CI workflows; these claims describe the inspected current workflow definition.

### Integration tests are present in-tree

The repository contains a dedicated `test/` integration test surface, including sync integration tests with the `integration` build tag. It also contains extensive unit/component tests across filesystem, model, protocol-adjacent, database, events, connection, and upgrade paths.

Presence of integration tests is upstream evidence of a serious verification strategy, but GitHub Gold did not execute them in this run.

## Platforms and toolchain

The project states the goal of broad availability across common computers, and the current CI directly tests Windows, Linux, and macOS.

The inspected `go.mod` declares Go **1.26.2**, while CI deliberately tests Go 1.26 and 1.27 families.

Notable dependency families include:

- QUIC through `quic-go`;
- SQLite implementations/drivers;
- STUN and NAT-PMP/gateway discovery;
- Prometheus metrics;
- LDAP;
- LZ4;
- cryptography/networking packages;
- filesystem notification support;
- YAML/protobuf tooling.

These dependencies reinforce that Syncthing is both a networking system and a filesystem/indexing system.

## Release evidence

The newest stable GitHub release inspected was **v2.1.5**, published **2026-09-08**.

The release publishes a broad multi-platform artifact set. GitHub release metadata exposes SHA-256 digest metadata for inspected assets, and the release contains signed checksum files such as `sha256sum.txt.asc`.

The root README additionally documents GPG-signed release binaries, updater signature verification, and native code signing for Windows/macOS artifacts.

GitHub Gold did not download, hash, signature-check, install, or execute v2.1.5.

## Current maintenance

The repository remained active immediately before inspection.

Recent commits on **2026-09-08** included:

- correcting the password passed to macOS key-partition-list signing setup;
- discovery-server diagnostic header work;
- upgrade-service asset URL templating.

Additional August 2026 commits updated dependencies and standardized User-Agent behavior on outgoing HTTP requests.

A stable release on September 8 plus same-day repository maintenance supports a 5/5 Maintenance score.

## Security and privacy considerations

Syncthing's local-first model removes the need for a central file-storage provider, but that does not eliminate security boundaries.

Important considerations include:

- peers intentionally receive shared data, so device authorization matters;
- compromised devices remain trusted peers until removed;
- relays/discovery infrastructure may learn connection metadata even when it does not become the authoritative file store;
- GUI/API exposure must be configured carefully when accessible beyond localhost or trusted networks;
- ignore rules, send-only/receive-only policies, conflict behavior, and deletion propagation should be understood before using synchronization as a substitute for backup;
- synchronization propagates unwanted changes and deletions by design, so Syncthing should not be treated as equivalent to a versioned disaster-recovery system;
- filesystem semantics differ across Windows, macOS, Linux, and other supported targets;
- automatic update and release-signing paths create a software supply-chain trust boundary;
- discovery, relay, TLS, QUIC, and BEP parsers are exposed to network-originated input and deserve protocol/fuzzing review.

GitHub Gold did not perform a cryptographic audit, protocol fuzzing, malicious-peer test, GUI/API penetration test, relay privacy analysis, or supply-chain audit in this run.

## Reusability assessment

Syncthing receives 4/5 for Reusability.

It is extremely useful as a complete application and as an architecture reference, but the MPL-2.0 file-level copyleft license and the degree of integration among protocol/model/database/filesystem layers make arbitrary extraction somewhat less frictionless than small permissively licensed libraries.

High-value reusable or study targets include:

1. `lib/protocol` — BEP and device/file/block protocol types.
2. `lib/connections` — multi-transport peer connection management.
3. `lib/fs` and watcher aggregation — cross-platform filesystem behavior.
4. `lib/model` — synchronization state orchestration.
5. database/index code — peer/local metadata persistence.
6. `cmd/stdiscosrv` — discovery service architecture.
7. `cmd/strelaysrv` — relay service architecture.
8. upgrade/signing pipeline — signed self-update and package release patterns.
9. local GUI/API architecture — daemon-controlled local administration.

Prefer linking to exact upstream files/packages rather than copying components without a specific integration need.

## License

The repository root is licensed under **Mozilla Public License 2.0**.

MPL-2.0 is a file-level copyleft license. Modified covered files generally remain subject to MPL source-availability and notice requirements, while MPL-covered files can be combined into larger works under other terms subject to the license conditions.

Dependencies and bundled/generated material still require normal component-level license review.

No Syncthing source, binaries, protocol-generated files, release artifacts, keys, certificates, or third-party dependency code were copied into GitHub Gold in this run.

## Verification performed by GitHub Gold

This run inspected:

- current upstream repository metadata;
- root README and project goals summary;
- root MPL-2.0 license;
- current GitHub Actions workflow inventory;
- the primary build/test/package workflow;
- `go.mod` toolchain and dependency metadata;
- BEP implementation/documentation evidence;
- representative filesystem/model/integration test paths;
- latest stable GitHub release metadata;
- recent upstream commits;
- GitHub Gold duplicate search for `syncthing` before addition.

## Verification not performed

GitHub Gold did **not**:

- compile Syncthing;
- execute Syncthing locally;
- run unit or integration tests;
- synchronize a folder between devices;
- verify conflict/deletion/versioning behavior;
- operate a discovery or relay server;
- test TCP, QUIC, relay, STUN, NAT traversal, or LAN discovery paths;
- implement or interoperate with BEP independently;
- inspect packet captures;
- fuzz BEP, discovery, relay, TLS, QUIC, REST, or GUI inputs;
- independently audit TLS/device identity or cryptographic primitives;
- verify updater signatures;
- download/hash/signature-check release artifacts;
- perform filesystem corruption, disconnect, partial-transfer, or concurrent-edit fault injection.

## Why VERIFIED

VERIFIED here means repository evidence strongly supports that the project and its core functionality are real and actively exercised upstream:

- mature source architecture exists for protocol, connections, filesystem, model, database, discovery, relay, and upgrade paths;
- cross-platform CI builds and executes tests on Windows, Linux, and macOS;
- dedicated integration tests exist;
- current release artifacts are published and signed;
- maintenance is active as of September 2026.

It does **not** mean GitHub Gold independently reproduced runtime behavior in this run.

## Score rationale

### Utility — 5/5

Immediately useful for decentralized, local-first continuous synchronization across personally controlled machines.

### Working Evidence — 5/5

Cross-platform build/test CI, integration-test code, mature releases, signed artifacts, and long-lived protocol/application architecture provide unusually strong upstream evidence.

### Reusability — 4/5

Excellent architecture and package-level study value, but integrated subsystems and MPL file-level copyleft make extraction somewhat less frictionless than permissively licensed standalone libraries.

### Novelty — 4/5

Peer-to-peer synchronization is not a new category, but Syncthing's combination of device identity, BEP, discovery/relay support, block synchronization, cross-platform filesystem handling, and user-controlled infrastructure remains technically distinctive.

### Documentation — 5/5

Strong README, user/developer documentation, protocol documentation, man pages, build instructions, and operational guidance.

### Maintenance — 5/5

Stable release v2.1.5 was published September 8, 2026, with repository activity on the same date.

## Strongest recursive leads

1. **`lib/protocol` / BEP v1** — message framing, indexes, requests/responses, block metadata, compatibility and malformed-peer behavior.
2. **Connection stack** — QUIC/TCP selection, TLS/device identity, STUN/NAT-PMP, relay fallback, connection prioritization.
3. **`cmd/strelaysrv`** — relay trust model, bandwidth controls, abuse resistance, metadata exposure.
4. **`cmd/stdiscosrv`** — discovery protocol, privacy characteristics, replication/storage model.
5. **Filesystem watcher + model pipeline** — event aggregation, rescan behavior, conflict/deletion races.
6. **Database/index layer** — SQLite migration, block indexes, durability and recovery semantics.
7. **Release updater** — ECDSA verification, GPG/checksum artifacts, Windows/macOS code-signing chain.
8. **Security history** — audit recent CVEs/advisories and map fixes to current trust boundaries.
9. **Companion ecosystem** — GUI wrappers, Android/community clients, Syncthing documentation/spec repositories.

## Provenance

This dossier is GitHub-first research. The previously registered YouTube playlists were not required for this candidate and no video-derived technical claim is used here.

Primary inspected upstream sources:

- https://github.com/syncthing/syncthing
- https://github.com/syncthing/syncthing/blob/main/README.md
- https://github.com/syncthing/syncthing/blob/main/LICENSE
- https://github.com/syncthing/syncthing/blob/main/.github/workflows/build-syncthing.yaml
- https://github.com/syncthing/syncthing/blob/main/go.mod
- https://github.com/syncthing/syncthing/tree/main/lib/protocol
- https://github.com/syncthing/syncthing/blob/main/man/syncthing-bep.7
- https://github.com/syncthing/syncthing/releases/tag/v2.1.5

## Next-run recommendation

Do not immediately add another generic synchronization or backup application. Either recurse into Syncthing's BEP/relay/discovery architecture for component-level Gold, or rotate to a different major category such as SDR, observability, scientific computing, accessibility, robotics, mapping, or emergency communications.