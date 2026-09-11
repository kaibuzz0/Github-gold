# restic — encrypted, deduplicating, verifiable backup engine

- **Repository:** https://github.com/restic/restic
- **Organization:** restic
- **Category:** backup / encrypted storage / deduplication / archival / disaster recovery / data integrity
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary language:** Go
- **License:** BSD-2-Clause
- **Discovery source:** GitHub-first follow-up from the rclone/storage-infrastructure branch
- **Inspection date:** 2026-09-11

## Executive finding

Restic is a mature encrypted backup engine designed around content-addressed storage, deduplication, integrity verification, snapshotting, and multiple local/remote storage backends.

It is valuable to GitHub Gold both as an immediately useful backup tool and as a deep systems reference for encrypted repository formats, chunking, immutable content-addressed objects, backend abstraction, snapshot metadata, cross-platform filesystem handling, retention/pruning, restore verification, and reproducible release engineering.

The upstream README explicitly frames the project around five principles: easy operation, speed, verifiability, security against untrusted backup storage, and storage efficiency through deduplication.

## Why it matters

Backup software is only useful if restores are dependable. Restic's architecture is explicitly designed around recoverability and verification rather than merely copying files.

Useful operational roles include:

- workstation and server backups;
- encrypted backups to untrusted remote storage;
- disaster-recovery snapshots;
- off-site archival;
- backup to SFTP, object storage, cloud providers, local media, or the REST backend;
- storage through rclone when a native backend is unavailable;
- mount-and-browse recovery workflows;
- deduplicated historical snapshots;
- automated integrity checking and retention workflows.

This complements rather than duplicates `rclone/rclone`: rclone is primarily a generalized transfer/sync/storage-abstraction engine, whereas restic adds backup-specific repository semantics, snapshot history, encryption, deduplication, retention, pruning, and recovery verification.

## High-value components and patterns

### Content-addressed repository format

The upstream design document defines repository objects around SHA-256-derived storage IDs. Files in the repository are named from the SHA-256 hash of stored content, enabling integrity checks against accidental modification.

The format is designed around write-once repository objects. Upstream documents atomic writes so concurrent clients do not observe incomplete files; normal objects are not modified in place, while `prune` is the operation that removes obsolete data.

This is a strong reference architecture for append-oriented, content-addressed backup storage.

### Encryption and authentication

The inspected design document states that repository data, except key files, is encrypted using AES-256 in CTR mode and authenticated with Poly1305-AES. Encrypted objects use a per-object random IV and an authenticated structure of `IV || CIPHERTEXT || MAC`.

Pack files hold independently encrypted/authenticated blobs plus an encrypted/authenticated pack header. That organization permits indexing and repository reorganization without decrypting or rewriting each blob payload.

These are upstream format claims. GitHub Gold did not independently audit the cryptographic design or implementation.

### Pack/index architecture

Restic groups data and tree blobs into pack files. The encrypted pack header records blob type, size, plaintext hash, and related indexing information.

The header is placed at the end of the pack so blobs can be streamed during backup without rewriting the beginning of the file after final lengths are known.

This is a useful implementation pattern for streamed immutable object creation.

### Deduplication and chunking

Restic's design targets incremental storage efficiency: duplicate content should not be uploaded again, and later snapshots should consume storage primarily for new data.

The repository configuration carries a chunker polynomial used for content splitting. The project depends on `github.com/restic/chunker`, making its content-defined chunking implementation a strong recursive research target.

### Snapshot and restore model

The README demonstrates creating a repository with `restic init`, capturing data using `restic backup`, restoring through `restic restore`, and browsing repository snapshots through a FUSE mount.

The design document models a snapshot as a recorded filesystem state including content and metadata.

### Backend architecture

The inspected README documents native support for:

- local directories;
- SFTP;
- the restic REST protocol / `rest-server`;
- Amazon S3 and S3-compatible storage;
- OpenStack Swift;
- Backblaze B2;
- Azure Blob Storage;
- Google Cloud Storage;
- additional services through the rclone backend.

This makes the backend layer valuable both operationally and as a reference for normalizing different storage systems beneath one backup repository model.

### Repository format evolution

The design document explicitly versions the repository format and currently documents versions 1 and 2. Version 2 adds compression support including zstandard-compressed data/tree blobs and compressed metadata representation.

Versioned on-disk formats and migration/compatibility handling are important long-lived systems-engineering patterns.

## Working evidence

Restic has exceptionally strong repository-native verification evidence.

### Cross-platform CI

The current `.github/workflows/tests.yml` matrix includes:

- Windows with Go 1.26;
- macOS with Go 1.26;
- Linux with Go 1.26;
- Linux race-detector tests;
- Linux with Go 1.25.

The workflow does not stop at compilation.

### Real CLI smoke operation

CI builds restic and then performs an actual minimal backup workflow:

- `restic init` against a temporary repository;
- `restic backup .` against that repository.

That is direct upstream execution evidence for core repository creation and backup paths.

### Full Go test suite and race mode

CI runs `go test -cover ./...`, and a separate Linux matrix job adds `-race`.

FUSE testing is enabled on supported Linux jobs through `RESTIC_TEST_FUSE`.

### Backend integration tests

The upstream workflow provisions or downloads `rest-server`, MinIO, and rclone for integration work. On trusted upstream runs it executes backend tests for REST, SFTP, MinIO/S3, rclone, Swift, B2, Google Cloud Storage, and Azure.

The workflow uses `RESTIC_TEST_DISALLOW_SKIP` for a defined set of backend tests so those tests must actually execute rather than silently skip on the upstream credential-enabled job.

This is particularly strong working evidence for a storage tool whose correctness depends on heterogeneous remote backends.

### Cross-compilation

A separate CI job invokes the release-binary helper in multiple subsets and builds normal and debug variants across the project's supported platform matrix.

### Linting and changelog validation

Current CI also runs `golangci-lint` and validates changelog entries using the restic `calens` tool.

GitHub Gold did not execute these workflows; these statements describe inspected upstream CI definitions.

## Platforms and toolchain

The README explicitly identifies primary support for:

- Linux;
- macOS;
- Windows;
- FreeBSD;
- OpenBSD.

Current CI runs directly on Linux, macOS, and Windows and performs broader release cross-compilation.

The inspected `go.mod` declares Go 1.25.8 with toolchain `go1.25.10`, while CI tests against both current 1.26.x and 1.25.x toolchains.

Major dependency families include cloud provider SDKs, SFTP/SSH support, FUSE, compression, OAuth, crypto/network packages, S3/MinIO support, Swift, Backblaze B2, and the project's content-defined chunker.

## Release evidence

The newest stable GitHub release inspected was **restic 0.19.1**, published **2026-07-05**.

GitHub release metadata exposes a broad cross-platform artifact set and SHA-256 digest metadata on inspected assets. A signed source archive (`.asc`) is also published.

The README additionally states that released binaries have been reproducible beginning with restic 0.6.1 and points to `restic/builder` for reproduction instructions.

GitHub Gold did not independently rebuild, download, hash, or verify signatures for 0.19.1.

## Current maintenance

Maintenance remained substantive through late August 2026.

The newest inspected commit was **2026-08-29** and fixed a real secret-handling defect in the Swift backend: OpenStack Swift credentials could appear in clear text in debug logs when debug logging was enabled. The patch changed the API key/password field to the project's secret-string wrapper and unwraps it only at the backend call boundary.

Other commits from the same date fixed documentation contradictions/dead links, updated dependencies, and applied Go modernization work.

This supports a 5/5 Maintenance score even though the latest stable release predates the inspection date by roughly two months.

## Security and privacy considerations

Restic's threat model assumes the repository storage location itself may be untrusted, which is one of its strongest design characteristics.

Operational caveats remain important:

- losing the repository password can make encrypted backups unrecoverable;
- possession of encrypted backups does not remove the need to protect credentials, keys, environment variables, cache files, logs, and host endpoints;
- debug logging can expose sensitive values if redaction boundaries fail, as demonstrated by the August 2026 Swift fix;
- storage providers have different consistency, locking, timestamp, path, and failure semantics;
- pruning removes repository data and therefore deserves conservative automation and verification;
- a successful backup command is not equivalent to a tested disaster-recovery procedure;
- users should periodically run integrity checks and actual restores.

GitHub Gold did not perform a cryptographic audit, penetration test, restore drill, corruption simulation, credential-leak review, or backend threat analysis in this run.

## Reusability assessment

Restic receives 5/5 for Reusability because it is useful at multiple layers:

1. **Use the CLI directly** for encrypted deduplicated backup and recovery.
2. **Study the repository format** as a versioned content-addressed encrypted storage design.
3. **Study pack/index handling** for streaming immutable-object storage.
4. **Study chunking/deduplication** for incremental archival systems.
5. **Study backend abstractions** for local, SFTP, REST, cloud, and rclone-backed storage.
6. **Study snapshot/tree metadata** for filesystem-state capture.
7. **Study retention/check/prune logic** for lifecycle management.
8. **Study test infrastructure** for real cloud/backend integration testing.
9. **Study reproducible release engineering** through the companion builder repository.

The permissive BSD-2-Clause root license is favorable for reuse, but dependencies and copied individual files still require normal notice/license review.

## License

The root `LICENSE` is the BSD 2-Clause License with copyright attributed to Alexander Neumann beginning in 2014.

It permits source and binary redistribution with or without modification subject to preservation of the copyright notice, license conditions, and disclaimer.

No restic source code, binaries, repository data, keys, credentials, release artifacts, or dependency code were copied into GitHub Gold in this run.

## Verification performed by GitHub Gold

This run inspected:

- upstream repository metadata;
- root README;
- root BSD-2-Clause license;
- GitHub Actions workflow inventory;
- current primary test workflow;
- `go.mod` toolchain/dependency metadata;
- repository design documentation;
- latest stable GitHub release metadata;
- recent upstream commits, including the Swift secret-redaction fix;
- GitHub Gold duplicate search for `restic` before addition.

## Verification not performed

GitHub Gold did **not**:

- compile restic;
- execute restic locally;
- initialize a repository;
- perform a backup or restore;
- run `check` or `prune`;
- mount a repository with FUSE;
- run local/race/backend tests;
- connect to SFTP, S3, B2, Azure, GCS, Swift, REST, rclone, or other storage;
- test concurrent writers;
- corrupt repository objects and validate recovery behavior;
- independently audit AES/Poly1305, key derivation, nonce handling, chunking, deduplication, or repository locking;
- reproduce release builds;
- download/hash release artifacts;
- verify published signatures.

All working claims therefore derive from inspected upstream documentation, source/configuration, CI definitions, release metadata, and commit evidence unless stated otherwise.

## Gold score rationale

### Utility — 5/5

Directly useful for encrypted backup, snapshotting, remote/off-site storage, recovery, archival, and disaster-recovery workflows.

### Working Evidence — 5/5

Real CLI backup smoke testing, full Go tests, race tests, FUSE paths, credential-backed backend integration tests, linting, and broad cross-compilation.

### Reusability — 5/5

Strong CLI utility plus reusable architectural patterns in content-addressed storage, chunking, encryption, repository formats, backend abstraction, snapshots, integrity checking, and release engineering.

### Novelty — 4/5

Backup/deduplication are established fields, but restic's compact encrypted repository design and combination of content-addressing, immutable packs, cross-backend operation, and reproducible release practice are unusually strong.

### Documentation — 5/5

Extensive user documentation plus a detailed repository-format/design document and operational references.

### Maintenance — 5/5

Stable 0.19.1 release in July 2026 and substantive security/correctness maintenance through August 29, 2026.

## Strongest follow-up research

1. Inspect `restic/chunker` and the exact content-defined chunking/deduplication model.
2. Inspect repository key derivation, password handling, key rotation, and crypto implementation against the documented format.
3. Map `check`, `repair`, `prune`, and failure-recovery semantics.
4. Inspect repository locking and multi-client concurrency behavior.
5. Audit secret redaction/config parsing across all storage backends after the Swift fix.
6. Inspect `restic/rest-server` protocol implementation and append-only/security deployment modes.
7. Inspect `restic/builder` reproducible-build process and independently reproduce one release.
8. Compare restic with BorgBackup and Kopia, focusing on repository format, threat model, deduplication, pruning, and restore verification rather than surface feature lists.