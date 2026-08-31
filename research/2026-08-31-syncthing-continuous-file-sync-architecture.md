# Syncthing — continuous file synchronization architecture

Date: 2026-08-31

## Candidate summary

- **Repository:** https://github.com/syncthing/syncthing
- **Author / organization:** Syncthing contributors / syncthing organization
- **Category:** local-first file synchronization / peer-to-peer data movement / discovery / relay / cross-platform systems software
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30**
- **Provisional tier:** **S**
- **License:** Mozilla Public License 2.0 (MPL-2.0)
- **Discovery source:** independent GitHub-first discovery; intentionally broadens the current research batch away from Python package provenance
- **Code reuse status:** catalog/reference first. No upstream source copied into GitHub Gold.

## Gold scoring

| Dimension | Score | Notes |
| --- | ---: | --- |
| Utility | 5 | Directly useful continuous file synchronization across user-controlled devices without requiring centralized cloud storage. |
| Working evidence | 5 | Current signed releases, large cross-platform CI/build matrix, extensive package-level tests, protocol benchmarks/tests, active infrastructure and release tooling. |
| Reusability | 5 | Repository contains separable protocol, discovery, connection, NAT, filesystem, model, ignore, events, relay/discovery-server and API components. |
| Novelty | 4 | The overall problem is established, but Syncthing's mature decentralized device-identity, block-exchange, discovery and conflict-handling architecture remains technically valuable. |
| Documentation | 5 | README, dedicated documentation repository/site, protocol specification, build documentation, goals, service examples and operational documentation. |
| Maintenance | 5 | v2.1.3 released 2026-08-05; repository activity continued through 2026-08-24 in the inspected history. |

**Total: 29 / 30 — S tier.**

The score reflects repository evidence, not an independent benchmark, deployment review or security audit.

## What the project does

Syncthing is a continuous file synchronization system. The upstream README describes synchronization between two or more computers and explicitly prioritizes prevention of data loss, resistance to unauthorized eavesdropping/modification, ease of use, automatic operation and broad platform availability.

The architecture is useful to GitHub Gold because it is more than a desktop application. The repository contains a substantial collection of reusable systems components for:

- authenticated device-to-device synchronization;
- file metadata and block exchange;
- local/global peer discovery;
- connection establishment and connection selection;
- NAT traversal helpers;
- relay support;
- filesystem abstraction;
- ignore-rule evaluation;
- event propagation;
- configuration and API surfaces;
- standalone discovery and relay infrastructure;
- signed release/update handling.

## High-value components

### `lib/protocol`

The protocol package is one of the strongest reusable technical surfaces.

Current source includes implementation and tests around Syncthing's Block Exchange Protocol (BEP), including files such as:

- `bep_hello.go` / `bep_hello_test.go`;
- `bep_clusterconfig.go`;
- `bep_fileinfo.go` / `bep_fileinfo_test.go`;
- `bep_index_updates.go`;
- `bep_request_response.go`;
- protocol conflict tests;
- buffer-pool implementation/tests;
- protocol benchmarks.

This is evidence of a real protocol implementation and validation surface, not merely a README-level protocol claim.

The public protocol specification is separately documented by Syncthing at:

- https://docs.syncthing.net/specs/bep-v1.html

**Reuse value:** protocol framing, metadata representation, index synchronization, request/response handling, device handshake concepts, buffering strategies and compatibility tests.

### `lib/model`

The model layer is the high-level synchronization state machine and data-model area. It is a useful research target for:

- local/remote file-state reconciliation;
- folder/device state;
- synchronization decisions;
- conflict and availability handling;
- block request scheduling;
- interaction between the filesystem and network protocol layers.

This should be treated as architecture/reference material first because extracting isolated behavior from the model without its surrounding invariants can be error-prone.

### `lib/fs`

Syncthing carries a dedicated filesystem abstraction rather than scattering raw operating-system calls throughout synchronization logic.

**Reuse value:** cross-platform filesystem operations, path handling, metadata abstraction, atomic/safe file update patterns and testable filesystem boundaries.

### `lib/discover`

The discovery layer is valuable independently of file synchronization. It covers peer/device address discovery and the integration points for discovery services.

Related repository areas include the standalone discovery-server command (`stdiscosrv`) and local-network discovery primitives.

**Reuse value:** decentralized device discovery, address cache/lookup architecture, service integration and peer bootstrap patterns.

### `lib/connections`, `lib/dialer`, `lib/nat`, `lib/netutil`

These packages collectively expose reusable connection-management architecture.

They are strong recursive research targets for:

- candidate address handling;
- direct connection establishment;
- transport selection;
- NAT traversal;
- connection lifecycle management;
- relay/direct-path interaction;
- network utility abstractions.

This overlaps conceptually with prior GitHub Gold research on Tailscale, libp2p, Iroh/noq and WireGuard, but Syncthing applies those concerns specifically to durable data synchronization.

### `lib/ignore`

Ignore-pattern processing is a small but practical reusable component. Synchronization systems must apply ignore rules consistently across scans and remote state, so this package is worth component-level inspection rather than treating ignore behavior as UI-only configuration.

### `lib/events`

The event layer provides a structured way for synchronization state changes to reach API/UI/monitoring consumers.

**Reuse value:** decoupling long-running synchronization machinery from observers and user-interface surfaces.

### `lib/config` and `lib/api`

These provide configuration and API boundaries around the core engine. They are useful as examples of how a long-running local daemon exposes mutable configuration and operational state without embedding policy directly into the GUI.

### Standalone infrastructure

The repository also builds standalone infrastructure commands in addition to the primary `syncthing` binary. The current CI package workflow explicitly builds targets including:

- `syncthing`;
- `stdiscosrv`;
- `strelaysrv`.

This is important architectural evidence: discovery and relay functions are separable deployment components, not opaque hosted services required for the core program to exist.

## Build and test evidence

The upstream README documents a source build using:

```text
go run build.go
```

The current GitHub Actions workflow provides substantially stronger working evidence than that statement alone.

`build-syncthing.yaml` currently:

- runs on pull requests and normal pushes;
- uses a Windows / Ubuntu / macOS test matrix;
- tests with both Go 1.26 and Go 1.27 branches;
- builds before running the test suite;
- runs the project's `build.go test` path;
- requires matrix tests plus packaging, vulnerability checking, linting and metadata checks before the aggregate `basics` job succeeds;
- creates Windows packages for amd64, 386 and arm64 targets;
- includes platform-specific packaging for Linux, illumos, cross-platform/source, Debian and Windows in the aggregate gate;
- contains release-signing jobs for supported platforms.

The protocol source tree itself contains numerous `_test.go` files and benchmarks, including file-info, hello, conflict and buffer-pool tests.

**Verification boundary:** GitHub Gold inspected these workflow and source/test surfaces but did not execute them.

## Release and supply-chain evidence

The latest formal GitHub release inspected is:

- **v2.1.3**
- **published:** 2026-08-05
- release page/API includes platform artifacts plus signed checksum material.

The README states that release binaries are GPG signed. It also states that the built-in automatic upgrade mechanism uses a compiled-in ECDSA signature, and that macOS/Windows release binaries receive platform code signing.

The current CI configuration shows additional supply-chain care:

- release/signing jobs are separated from normal builds;
- privileged signing paths are restricted to the Syncthing repository and release refs;
- a workflow comment explicitly calls out the trust implications of third-party GitHub Actions in paths leading to packaged/signed code;
- Windows release signing currently uses a pinned Trusted Signing action revision;
- an August 18, 2026 repository commit added Docker-image signing.

This is strong operational evidence, but it is **not** an independent verification of the signatures, key custody, release reproducibility or update security.

## Maintenance evidence

The inspected recent history includes:

- **2026-08-24:** add a User-Agent to outgoing HTTP requests for troubleshooting/operational clarity;
- **2026-08-24:** documentation, translation and contributor updates;
- **2026-08-20:** dependency updates;
- **2026-08-19:** move builds to Go 1.27 while retaining Go 1.26 as the minimum tested version;
- **2026-08-18:** discovery-server behavior fixes and Docker-image signing work.

This supports a Maintenance score of 5 rather than relying on popularity or historical reputation.

## Platforms and runtime

Upstream describes Syncthing as broadly available across common computers and provides service/background examples and GUI wrappers.

The current CI directly provides evidence for at least:

- Windows;
- Linux;
- macOS;

and the release/package machinery covers additional operating systems/architectures.

Docker deployment is separately documented in `README-Docker.md`.

The project currently requires modern Go for source builds; the inspected CI tests Go 1.26 and 1.27.

## Languages and technologies

Primary implementation language: **Go**.

Other repository technologies include:

- web UI assets;
- shell/build/release automation;
- platform packaging;
- protocol definitions/serialization;
- container/release infrastructure.

## License and reuse caveat

The root `LICENSE` is **Mozilla Public License Version 2.0** and the README states that all code is licensed under MPLv2.

MPL-2.0 is file-level copyleft. It is generally more permissive for combining covered files with separately licensed files than whole-program copyleft licenses, but modifications to covered source files and distribution obligations must still be handled correctly.

GitHub Gold did not copy any Syncthing source. Before adapting a particular file or package, preserve notices and inspect:

- the exact file header;
- generated-code provenance;
- vendored or third-party dependencies;
- any separately licensed assets.

## Security and operational boundaries

Catalog inclusion is not a security audit.

Important boundaries include:

- peer/device identity and key management;
- local GUI/API exposure and authentication configuration;
- discovery services learning address metadata;
- relay services carrying encrypted traffic while still being an availability/metadata boundary;
- filesystem permissions and local account compromise;
- synchronization propagating accidental or malicious file changes;
- conflict resolution and deletion semantics;
- ignore-pattern mistakes;
- auto-upgrade/release-key trust;
- third-party GUI wrappers and packaging channels.

The upstream project's stated goal of being secure against attackers is a design objective, not independent proof of security.

## Why it qualifies as GitHub Gold

Syncthing clears the quality bar because several independent evidence classes line up:

1. current formal releases;
2. active August 2026 maintenance;
3. broad cross-platform build/test CI;
4. signed release/update infrastructure;
5. a documented protocol with source-level implementation/tests;
6. separable discovery, relay, filesystem, protocol, model, NAT, connection and API components;
7. mature documentation and operational packaging;
8. direct usefulness for local-first and user-controlled infrastructure.

The project is especially valuable as a technical treasure-map entry because useful material exists both at whole-application level and deep inside the repository.

## Verification performed by GitHub Gold

Inspected during this pass:

- repository metadata and default branch;
- upstream README;
- root MPL-2.0 license;
- latest GitHub release metadata for v2.1.3;
- recent commit history through 2026-08-24;
- `lib/` package structure;
- `lib/protocol` source/test/benchmark surface;
- `.github/workflows/` inventory;
- cross-platform `build-syncthing.yaml` build/test/package/signing workflow.

Not performed:

- local build;
- unit/integration test execution;
- multi-device synchronization session;
- block-level protocol capture;
- conflict/deletion experiment;
- discovery-server deployment;
- relay deployment;
- NAT traversal experiment;
- throughput or memory benchmark;
- filesystem fault injection;
- release-signature validation;
- reproducible-build verification;
- security or cryptographic audit.

## Related ecosystem / recursive leads

High-value follow-ups:

1. **BEP v1 protocol deep dive** — map handshake, cluster configuration, indexes, requests, compression/framing and compatibility rules from spec to source.
2. **Connection path architecture** — trace direct TCP/QUIC/relay selection and reconnect behavior across `lib/connections`, `lib/dialer` and relay code.
3. **Discovery privacy boundary** — compare local discovery, global discovery and static addressing, including what metadata each path reveals.
4. **Filesystem safety** — inspect atomic replacement, temporary files, rename semantics, permission propagation and crash consistency in `lib/fs` plus model/folder code.
5. **Conflict/version vectors** — isolate how Syncthing detects concurrent edits and creates conflict copies.
6. **Block reuse and hashing** — inspect chunk/block selection, hashing, pull scheduling and deduplication opportunities.
7. **Untrusted/encrypted folders** — inspect current receive-encrypted / untrusted-device architecture and its exact metadata/content confidentiality boundaries.
8. **Standalone relay (`strelaysrv`)** — compare relay resource controls and trust boundaries with prior Tailscale DERP and Iroh relay research.
9. **Standalone discovery (`stdiscosrv`)** — inspect rate limiting, persistence/cache behavior, address validation and abuse controls.
10. **Android ecosystem** — inspect current supported Android wrappers/ports separately rather than assuming the desktop daemon maps cleanly to Android background-process constraints.

## Promotion recommendation

**VERIFIED / promotion-ready at provisional S / 29.**

Because the current branch is still a draft research batch and the repository has historically kept canonical catalog promotion atomic, this pass adds the dossier only. It does not partially rewrite `MASTER_LIST.md`, `catalog/tools.json`, or `catalog/candidate_queue.json`.