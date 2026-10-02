# rclone — multi-backend sync, transfer, mount, and storage abstraction engine

- **Repository:** https://github.com/rclone/rclone
- **Organization:** rclone
- **Category:** data transfer / synchronization / cloud storage / local-first tooling / backup / FUSE / automation
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary language:** Go
- **License:** MIT at repository root
- **Discovery source:** GitHub-first category rotation into portable data/sync infrastructure
- **Inspection date:** 2026-09-11

## Executive finding

Rclone is a mature, highly reusable file-transfer and synchronization engine that normalizes a very large number of local, cloud, object-storage, network-filesystem, and virtual-storage backends behind a common command-line and library-oriented architecture.

The project is often described upstream as "rsync for cloud storage," but its practical scope is broader than that shorthand. The inspected README documents one-way copy and sync, bidirectional synchronization, integrity checking, server-side transfers, optional chunking, transparent compression, transparent encryption, FUSE mounting, multi-threaded local downloads, and serving local or remote storage over HTTP, WebDAV, FTP, SFTP, and DLNA.

For GitHub Gold, rclone is valuable at several layers:

1. as an immediately useful operational tool for moving or synchronizing data;
2. as a large reference implementation for heterogeneous storage APIs;
3. as reusable backend and virtual-filesystem architecture;
4. as a cross-platform release/testing example for a substantial Go project;
5. as an automation primitive for backup, archival, migration, offline workflows, and self-hosted systems.

## Why it matters

Data portability is a recurring infrastructure problem. Different providers expose incompatible authentication models, APIs, metadata semantics, checksums, pagination behavior, rate limits, multipart upload rules, object naming conventions, timestamp precision, and filesystem-like capabilities.

Rclone's core value is that it absorbs much of that provider-specific complexity behind a common operational model.

The upstream README currently lists direct or protocol-based support for a broad set of systems including Amazon S3 and S3-compatible services, Google Drive, Google Cloud Storage, Microsoft OneDrive, Azure Blob and Azure Files, Dropbox, Backblaze B2, Box, SFTP, FTP, WebDAV, SMB/CIFS, OpenStack Swift, Internet Archive, Proton Drive, iCloud Drive, HDFS, Storj, local filesystems, and many other commercial or self-hosted services.

That breadth makes rclone useful in:

- backup and restore workflows;
- cloud-to-cloud migration;
- local-to-remote synchronization;
- remote-to-remote copying;
- archival pipelines;
- self-hosted storage operations;
- disaster-recovery workflows;
- scripted infrastructure tasks;
- portable/offline technical work where one executable must speak many storage protocols;
- data staging for analytical, ML, scientific, or media workflows.

## High-value components and patterns

### Storage backend abstraction

The repository's principal architectural value is its common storage abstraction across many fundamentally different provider APIs and protocols.

Strong recursive research targets include:

- backend registration and capability negotiation;
- filesystem/object interfaces;
- feature detection;
- provider-specific authentication;
- multipart/chunked transfer implementations;
- retry, pacing, and rate-limit handling;
- checksum and metadata normalization;
- server-side copy/move support;
- directory emulation for object stores;
- provider-specific test harnesses.

These are high-value engineering patterns because they show how to expose a stable common interface without pretending all storage systems have identical semantics.

### Virtual storage backends

The inspected README documents composable virtual providers including:

- **Alias** — remap an existing remote;
- **Archive** — read archive files;
- **Chunker** — split large files;
- **Combine** — combine remotes into a directory tree;
- **Compress** — transparent compression;
- **Crypt** — transparent encryption;
- **Hasher** — add/track hashes;
- **Union** — combine multiple remotes into one logical storage surface.

This is particularly valuable for GitHub Gold because these are not merely provider connectors. They demonstrate transform and composition layers that can wrap another storage implementation while preserving a common operational interface.

### Copy, sync, bisync, and check workflows

Upstream documents distinct operational modes rather than treating all replication as equivalent:

- `copy` copies new or changed data without deleting unrelated destination files;
- `sync` makes the destination match the source;
- `bisync` performs two-way synchronization;
- `check` compares file hashes/equality without necessarily transferring content.

The distinction matters operationally because sync semantics can be destructive when misused. Any automation consuming rclone should explicitly choose the intended replication model and test filters/dry-run behavior before production use.

### Integrity and metadata handling

The README states that MD5/SHA-1 hashes are checked where available and that timestamps are preserved on files. Provider capabilities differ, so exact hash and timestamp behavior remains backend-specific.

The project also exposes a virtual Hasher backend, making integrity metadata itself a composable storage concern.

### Mounting and serving

Rclone extends beyond batch file transfer. The inspected README documents:

- optional FUSE mounting through `rclone mount`;
- serving local or remote storage over HTTP;
- WebDAV serving;
- FTP serving;
- SFTP serving;
- DLNA serving.

This makes the codebase relevant to virtual filesystems, user-space mounts, protocol gateways, and storage interoperability—not only backup scripts.

### Library surfaces

Current CI explicitly runs `librclone` tests using both C and Python test paths. That is strong evidence that upstream maintains a library-facing surface in addition to the main CLI.

The library layer is a strong recursive target for applications that need rclone capabilities in-process rather than by spawning a command.

## Working evidence

Rclone has unusually strong repository-native working evidence.

### Cross-platform CI

The current `.github/workflows/build.yml` defines a build matrix including:

- Linux x86-64;
- Linux 386;
- macOS AMD64;
- macOS ARM64;
- Windows;
- an `other_os` cross-compilation path;
- a secondary supported Go-version job.

The workflow does materially more than compile one executable. Depending on the matrix job it:

- installs platform FUSE support;
- builds rclone;
- executes `rclone version` as a smoke test;
- runs `make quicktest`;
- runs race-enabled quick tests;
- runs C and Python `librclone` tests;
- runs compile-all architecture testing;
- prepares/deploys built binaries on eligible trusted runs.

GitHub Gold did not execute this CI. These are inspected upstream workflow definitions.

### Platform-specific mount dependencies

The CI installs:

- FUSE3/libfuse on Linux;
- macFUSE on macOS;
- WinFsp on Windows.

This provides direct upstream evidence that mount behavior is part of the actively built/tested cross-platform surface rather than an abandoned auxiliary feature.

### Go toolchain and dependency surface

The inspected `go.mod` declares:

- module `github.com/rclone/rclone`;
- Go 1.26.0 as the module language/toolchain baseline.

It also contains provider and systems dependencies spanning Azure, AWS S3, HDFS, FTP, SFTP, compression, FUSE, Prometheus, JWT, filesystem helpers, and numerous provider-specific SDKs.

This dependency breadth is expected for the project's scope, but it also expands the supply-chain and upgrade surface. Consumers should treat backend-specific dependencies as part of their threat and maintenance model.

## Release evidence

The newest stable GitHub release inspected was **rclone v1.75.1**, published **2026-09-04**.

The release contains a broad multi-OS/multi-architecture asset set. Inspected GitHub release metadata included packages for AIX, FreeBSD, Linux and additional targets, with GitHub-provided SHA-256 digest metadata on release assets. The release also publishes checksum files.

GitHub Gold did not download, execute, or independently hash those artifacts.

## Current maintenance

Maintenance is current through the inspection date.

Recent inspected commits include:

- **2026-09-11:** documentation correction for a broken bisync anchor;
- **2026-09-10:** OneDrive upload-cutoff handling corrected to permit the documented single-request size range;
- **2026-09-10:** size parsing changed to reject out-of-range values rather than silently disabling a limit;
- **2026-09-09:** gRPC dependency updated specifically to address **CVE-2026-84445**.

The recent history shows provider correctness, safety/validation, documentation, contributor maintenance, and dependency-security work—not merely release tagging.

## Reusability assessment

Rclone receives a 5/5 Reusability score because useful consumption exists at multiple levels:

1. **Use the CLI directly** for transfers, synchronization, checking, mounting, and serving.
2. **Use configuration and remote abstractions** to normalize heterogeneous storage endpoints.
3. **Use virtual backends** such as Crypt, Chunker, Compress, Hasher, Combine, and Union to compose storage behavior.
4. **Use `librclone`** where in-process integration is appropriate.
5. **Study provider backends** as references for robust API clients, retries, pagination, upload semantics, metadata normalization, and throttling.
6. **Study VFS/FUSE architecture** for presenting remote object storage through filesystem semantics.
7. **Study CI/release automation** for broad Go cross-platform delivery.

The MIT root license is favorable for reuse, but dependency and provider-SDK licensing must still be inspected for any code that would be copied or redistributed.

## Security, privacy, and operational caveats

Rclone frequently handles high-value credentials and data. This increases the importance of configuration hygiene.

Key caveats:

- remote credentials/tokens must be protected;
- sync operations can delete destination files by design;
- cloud-provider APIs have different metadata and consistency semantics;
- cryptographic or encrypted-backend use should be configured and backed up carefully;
- mounting remote storage introduces filesystem/network failure modes that local applications may not expect;
- serving remotes over network protocols creates an additional authentication and exposure boundary;
- provider SDKs and authentication flows expand the supply-chain surface;
- backend behavior can change as external providers alter APIs or limits.

GitHub Gold did not audit credential storage, token encryption, Crypt backend cryptography, OAuth flows, server authentication, VFS cache safety, or provider-specific API implementations in this run.

## License

The root `COPYING` file contains the MIT License and identifies copyright beginning in 2012 with Nick Craig-Wood.

The license permits use, copying, modification, distribution, sublicensing, and sale subject to preservation of the copyright and permission notice.

No rclone source code, binaries, configuration files, credentials, tokens, release assets, or provider SDK code were copied into GitHub Gold.

## Verification performed

This dossier inspected:

- upstream repository metadata and default branch;
- README and documented provider/feature surface;
- root MIT license;
- current GitHub Actions workflow inventory;
- main build/test workflow;
- current `go.mod` toolchain/dependency metadata;
- latest stable GitHub release metadata;
- recent upstream commit history;
- GitHub Gold duplicate search for `rclone` before addition.

## Verification not performed

GitHub Gold did **not**:

- compile rclone;
- execute the CLI;
- run quick tests or race tests;
- execute `librclone` C/Python tests;
- configure any real provider;
- authenticate to any cloud service;
- upload, download, sync, bisync, check, mount, encrypt, compress, chunk, hash, or serve files;
- validate FUSE/macFUSE/WinFsp behavior;
- test provider throttling/retry behavior;
- inspect every backend implementation;
- audit the Crypt backend;
- audit credential/config storage;
- independently verify release checksums or artifact provenance.

All working claims in this dossier are therefore based on inspected upstream source/configuration, CI definitions, documentation, release metadata, and commit history unless explicitly stated otherwise.

## Gold score rationale

### Utility — 5/5

Immediately useful across backup, transfer, sync, migration, archival, storage gateway, mount, and automation workflows.

### Working Evidence — 5/5

Substantial cross-platform CI, functional tests, race tests, library tests, compile-all coverage, active release automation, and current releases.

### Reusability — 5/5

Useful as a CLI, library surface, backend architecture, virtual-storage composition framework, VFS reference, and provider implementation corpus.

### Novelty — 4/5

File transfer and synchronization are not novel by themselves, but the breadth and composability of rclone's backend/virtual-backend architecture is unusually strong.

### Documentation — 5/5

Large maintained documentation surface, provider-specific docs, command docs, changelog, installation material, generated manuals, and contribution guidance.

### Maintenance — 5/5

Stable release on 2026-09-04 and substantive upstream commits continuing through 2026-09-11.

## Strongest follow-up research

1. Inspect the exact `fs` backend interfaces and capability-negotiation model.
2. Audit `backend/crypt` design, metadata leakage, filename handling, key derivation, and compatibility boundaries.
3. Map the VFS/FUSE layer, cache modes, writeback, conflict behavior, and offline/network-failure semantics.
4. Inspect `librclone` ABI/API stability and embedding constraints.
5. Compare `sync`, `bisync`, and check-file state models for failure recovery and destructive-edge-case handling.
6. Inspect OAuth/config-secret storage and redaction behavior.
7. Identify especially reusable pacing/retry, multipart-upload, checksum, and provider-test infrastructure.
8. Compare rclone with narrower tools such as restic, borg, syncthing, and native provider CLIs without treating them as interchangeable products.
