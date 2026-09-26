# BorgBackup — deduplicating encrypted backup engine

- **Repository:** https://github.com/borgbackup/borg
- **Organization:** BorgBackup
- **Category:** backup / deduplication / encryption / archival / local-first infrastructure
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary languages:** Python / Cython / C
- **License:** BSD 3-Clause
- **Discovery source:** Independent GitHub-first breadth pass after duplicate checking the active research branch
- **Inspection date:** 2026-09-13

## Executive finding

`borgbackup/borg` is a mature deduplicating backup system with optional compression and client-side authenticated encryption. Its central technical value is content-defined chunking: files are split into variable-length chunks and only previously unseen chunks are stored, allowing efficient repeated backups even when large files shift or change slightly.

Borg is valuable to GitHub Gold as both a production-oriented backup architecture and a deep systems reference for chunking, deduplication, authenticated encryption, remote repositories, repository compaction/checking, mountable archives, multi-backend transport, cross-platform binary packaging, and corruption-aware backup maintenance.

A critical versioning caveat is explicit upstream: the current `master` branch is Borg 2 development/beta and upstream warns not to use Borg 2 master for production backups yet. The latest stable release inspected is from the Borg 1 line: **1.4.5**, published **2026-07-18**.

## Why it matters

Borg's architecture combines several high-value capabilities in one project:

1. content-defined chunking and repository-wide deduplication;
2. client-side authenticated encryption for untrusted storage targets;
3. optional compression with multiple codecs;
4. remote repositories over SSH/REST-style transport plus SFTP, S3, B2, and rclone-backed paths in Borg 2 development;
5. mountable backup archives for interactive restore workflows;
6. integrity checking, compaction, repository metadata, and archive lifecycle tooling;
7. single-file binary distribution across multiple desktop/server platforms;
8. substantial correctness, sanitizer, security, compatibility, and release CI.

This makes Borg especially relevant to offline-first systems, self-hosted infrastructure, disaster recovery, field computing, and bandwidth/storage-constrained archival workflows.

## High-value technical components

### Content-defined chunking

The current upstream README documents multiple chunkers, including:

- FastCDC (default in Borg 2 development);
- improved Buzhash variants;
- Toeplitz-AES;
- Rabin-AES;
- Goldilocks-AES;
- fixed-size chunking.

The keyed AES-based chunkers are specifically described as making chunk-boundary fingerprinting attacks harder.

The architecture is valuable because deduplication does not depend on stable file paths, complete-file identity, timestamps, or absolute chunk positions. A shifted region inside a large VM image or disk image can still preserve most chunk reuse.

### Encryption and authentication

Upstream documents client-side authenticated encryption options using AES-OCB or ChaCha20-Poly1305. Borg 2 development also documents authentication-only and non-encrypting modes plus HMAC-SHA256 and keyed BLAKE3 hashing choices.

This makes the repository a useful reference for designing backup repositories intended to live on storage that is not fully trusted.

### Compression

Documented compression choices include:

- LZ4;
- Zstandard;
- zlib;
- LZMA.

Performance-critical paths such as chunking, compression, and encryption are implemented in C/Cython, with SIMD paths documented for NEON, AVX2, and AVX-512 where beneficial.

### Remote repository and backend support

The Borg 2 development README documents remote/off-site support including:

- REST over SSH/stdin-stdout;
- HTTP(S) REST;
- SFTP;
- S3;
- Backblaze B2;
- rclone-backed repositories.

These capabilities deserve component-level follow-up because they separate backup semantics from storage transport and create useful patterns for self-hosted and heterogeneous archival systems.

### Mountable archives

Borg archives can be mounted as user-space filesystems for interactive inspection and restore. CI explicitly exercises multiple FUSE implementations/environments, making this more than a documentation-only feature surface.

## Working evidence

Repository-native evidence is unusually strong.

### Main CI

The current CI workflow includes:

- Ruff linting;
- Bandit security scanning over `src/borg`;
- AddressSanitizer and UndefinedBehaviorSanitizer builds for native C/Cython code;
- pytest runs under ASan/UBSan;
- native test matrices spanning multiple Python versions;
- Linux x86-64 and ARM64 runners;
- macOS ARM64 and x86-64 runners;
- multiple FUSE backends (`llfuse`, `pyfuse3`, `mfusepy`);
- mypy/static-type checking;
- coverage collection;
- binary packaging/verification paths;
- SFTP and remote-backend test setup;
- S3-compatible testing using MinIO.

The workflow also pins third-party GitHub Actions to exact commit hashes and deliberately disables caches on release tags where cached content could contaminate release binaries.

### Specialized CI

The workflow inventory includes dedicated jobs for:

- 32-bit testing;
- big-endian testing;
- canary testing;
- CodeQL analysis;
- PyPy;
- documentation;
- release generation.

This breadth is highly relevant for a backup format and native-extension project where portability, integer width, endianness, filesystem behavior, and memory safety all matter.

### Supply-chain and test-fixture maintenance

A September 12, 2026 change repaired S3 CI after MinIO stopped serving previous binary URLs. Upstream switched to pinned historical GitHub release binaries and verifies their SHA-256 sums before use.

That commit explicitly reports verification on both amd64 and arm64 containers, providing narrower upstream evidence for the fixed CI path.

GitHub Gold did not reproduce that verification independently.

## Release evidence

The latest stable GitHub release inspected is **Borg 1.4.5**, published **2026-07-18**.

Release assets include platform-specific standalone binaries and detached signature files. GitHub's release metadata exposes SHA-256 digests for inspected assets. Observed targets include FreeBSD, Linux x86-64, Linux ARM64 and additional platform artifacts.

This stable release should be distinguished from the repository's `master` branch, which currently documents itself as Borg 2 beta/development and warns users not to use it for production backups.

## Current maintenance

Development remained active through **2026-09-12**.

Recent inspected changes include:

- correcting `borg diff` byte accounting by sequence-aligning chunk lists rather than comparing only chunk-ID sets;
- pinning MinIO and MinIO client binaries used in S3 tests and verifying SHA-256 checksums;
- authenticating/validating repository gap objects before compaction discards their bytes;
- clarifying empty-passphrase security state and repository warnings.

These are correctness, integrity, security-communication, and CI supply-chain changes rather than superficial dependency churn.

## Useful architecture patterns

### Repository-wide deduplication

Chunks are deduplicated across files, machines, and backup generations inside a repository. This makes Borg useful as a reference for content-addressed backup systems where logical archive history can be much larger than physically stored unique content.

### Untrusted storage design

Client-side authenticated encryption allows backup storage to be treated as less trusted than the client generating the backup. This separation is highly relevant to rented servers, remote hosts, removable media, and third-party object storage.

### Integrity-aware maintenance

Recent compaction work explicitly validates/authenticates repository objects before discarding superseded bytes, illustrating a useful principle: space-reclamation code in backup systems must preserve integrity checks rather than optimizing around them.

### Performance-aware correctness

The recent chunk-list diff fix also documents a bounded fallback when sequence alignment could become quadratic on repetitive chunk lists such as sparse files or VM images. That tradeoff is a useful engineering example of maintaining correctness improvements without allowing pathological workloads to dominate runtime.

## Licensing

The root license is **BSD 3-Clause**, covering Borg itself with permissive redistribution and modification terms subject to attribution, disclaimer preservation, and non-endorsement conditions.

This is favorable for study and reuse, but specific bundled dependencies, generated code, codecs, libraries, or copied components still require file-level license review before extraction.

No Borg source code or binary artifacts were copied into GitHub Gold during this run.

## Relationship to existing GitHub Gold entries

Borg complements the existing `restic/restic` dossier rather than duplicating it.

Both are encrypted deduplicating backup systems, but Borg is especially valuable for:

- content-defined chunker experimentation and multiple chunking algorithms;
- C/Cython/SIMD performance work;
- detailed repository maintenance/compaction internals;
- mountable archives through multiple FUSE backends;
- Borg 2's expanding remote backend model.

The two projects should remain separate because they provide different implementation strategies and are strong candidates for comparative study.

## Verification performed

GitHub Gold inspected:

- repository metadata and branch state;
- current Borg 2 `master` README and production-use warning;
- deduplication, chunker, encryption, compression, remote backend, platform, and mount documentation;
- root BSD 3-Clause license;
- current workflow inventory;
- substantial portions of the main CI workflow;
- latest stable release metadata for 1.4.5;
- GitHub-provided release-asset SHA-256 metadata;
- recent commit history through 2026-09-12;
- active GitHub Gold branch state to avoid known duplicates.

## Verification boundaries

GitHub Gold did **not**:

- compile Borg;
- execute pytest or tox;
- run ASan/UBSan or CodeQL;
- create a backup repository;
- perform a restore;
- mount an archive;
- test deduplication ratios;
- benchmark chunkers or SIMD paths;
- verify encryption implementations;
- test SFTP/S3/B2/rclone repository backends;
- fuzz repository parsing;
- independently verify release signatures or hashes;
- test Borg 1 to Borg 2 migration behavior.

Claims above therefore distinguish upstream evidence from actions actually performed by GitHub Gold.

## Caveats and risks

- Current `master` is Borg 2 beta/development and upstream explicitly warns against using it for production backups.
- Borg 2 beta releases may intentionally break compatibility and currently may require recreating repositories between beta releases.
- Deduplicating encrypted backup repositories are complex stateful systems; corruption recovery and restore drills matter as much as successful backup creation.
- Synchronization is not the same as backup, and backup is not complete until restoration has been tested operationally.
- Remote backends have separate credentials, transport, dependency, and consistency assumptions.
- FUSE support varies by platform and backend.
- BSD licensing is permissive for Borg itself, but third-party dependencies still require separate review.

## Strongest follow-up leads

1. FastCDC versus Buzhash and keyed AES-based chunker implementations.
2. Chunk IDs, repository indexes, deduplication metadata, and cache behavior.
3. AES-OCB / ChaCha20-Poly1305 key hierarchy and nonce handling.
4. Repository integrity, segment/object validation, compaction, and corruption recovery.
5. Borg 1 versus Borg 2 repository-format differences and migration strategy.
6. S3/B2/rclone/SFTP backend consistency and retry semantics.
7. Mount/FUSE read paths and permission/metadata restoration.
8. Sparse-file, VM-image, and raw-disk behavior.
9. Release attestation/signature and reproducible-build opportunities.
10. Comparative study with restic: chunking, metadata, encryption, backends, recovery, and failure modes.