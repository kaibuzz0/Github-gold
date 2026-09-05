# Restic — encrypted, deduplicated backup engine and repository architecture

Research date: 2026-08-31

## Candidate

- Repository: https://github.com/restic/restic
- Organization: restic
- Category: backup / archival / storage / cryptography / content-defined chunking
- Evidence level: VERIFIED
- Provisional Gold score: 29/30
- Provisional tier: S
- License: BSD-2-Clause
- Primary language: Go
- Platforms documented upstream: Linux, macOS, Windows, FreeBSD, OpenBSD, plus release builds for additional Go-supported targets
- Discovery source: independent GitHub-first discovery; no reliable playlist transcript provenance claimed for this entry

## Executive assessment

Restic is a mature encrypted backup engine with unusually reusable storage architecture. It is more valuable to GitHub Gold than a simple backup-command entry because the repository exposes concrete design patterns for immutable content-addressed storage, authenticated encryption, content-defined chunking, deduplication, snapshot trees, backend abstraction, repository verification, locking, retention/pruning, caching, retry behavior, append-only operation, and reproducible release construction.

The project is actively maintained, has formal releases, extensive tests and integration-test surfaces, detailed repository-format documentation, multiple native storage backends, a separate REST server ecosystem, and a standalone content-defined chunker project maintained by the same organization.

This dossier does not treat popularity as evidence. The VERIFIED classification is based on inspected upstream source/documentation structure, formal releases, tests, repository-format documentation, licensing, and recent maintenance activity. GitHub Gold did not independently run Restic.

## Gold score

| Dimension | Score | Evidence summary |
|---|---:|---|
| Utility | 5/5 | Practical encrypted backup, restore, verification, retention, repository copy and multiple storage backends. |
| Working Evidence | 5/5 | Formal v0.19.1 release, broad release artifacts, test/integration-test tree, reproducible-build documentation, active issue/maintenance history. |
| Reusability | 5/5 | Strong backend interfaces, repository/storage primitives, content-defined chunking ecosystem, cache/retry layers, archiver/filesystem packages and documented repository format. |
| Novelty | 4/5 | Backup/deduplication is established technology, but Restic combines content-addressed immutable storage, encryption, pack indexing, backend portability and verification cleanly. |
| Documentation | 5/5 | Detailed user documentation plus repository-format/design documentation explaining pack, blob, snapshot, index, encryption and chunking semantics. |
| Maintenance | 5/5 | v0.19.1 released 2026-07-05; inspected master contains commits through 2026-08-29 including security-sensitive credential handling and dependency maintenance. |

Total: **29/30 — provisional S tier**.

## What it does

Restic creates encrypted point-in-time snapshots of files and directories and stores them in a repository that may live locally or on remote/object storage. Upstream documents native local, SFTP, REST, S3, Swift, Backblaze B2, Azure Blob and Google Cloud Storage backends, with additional services available through rclone.

The repository is designed around several useful primitives:

- blobs identified by plaintext SHA-256;
- pack files containing multiple independently encrypted/authenticated blobs;
- immutable repository objects that are written once rather than modified in place;
- indexes mapping blob identity to pack location;
- snapshots referring to filesystem tree state;
- content-defined chunking so unchanged file regions can reuse prior content;
- client-side authenticated encryption before untrusted storage sees repository data;
- repository checking and restoration as explicit first-class operations.

## Repository-format architecture

The upstream design document defines a storage ID as the SHA-256 hash of stored object content and states that repository files are written once and not subsequently modified. This makes immutable/object-style backends natural targets and reduces in-place mutation requirements.

Repository directories include:

- `config`
- `data/`
- `index/`
- `keys/`
- `locks/`
- `snapshots/`
- `tmp/`

Pack files aggregate encrypted blobs. Their header is placed at the end of the pack, allowing Restic to stream blob content while writing and later discover blob type, hash, offset and length from the authenticated header without reading every payload.

Repository format v2 supports zstd-compressed data and tree blobs.

### Reusable design idea: tail-indexed streaming packs

A particularly useful storage pattern is:

`EncryptedBlob1 || ... || EncryptedBlobN || EncryptedHeader || HeaderLength`

This allows streaming construction while retaining efficient later indexing. The individual blobs and header are independently authenticated/encrypted, so repository reorganization can operate at pack/blob boundaries without decrypting and rewriting every payload merely to inspect the pack index.

This pattern is potentially reusable in archival, object-store, offline bundle and deduplicated content systems, subject to BSD-2-Clause attribution requirements if source is copied/adapted.

## Cryptographic boundary

The inspected design documentation states that repository files other than key files are encrypted using AES-256 in CTR mode and authenticated with Poly1305-AES. The documented outer layout is:

`IV || CIPHERTEXT || MAC`

with a new random IV per encrypted file. Pack blobs and pack headers are encrypted/authenticated independently.

GitHub Gold records this as **upstream format evidence**, not as an independent cryptographic audit. No claim is made that GitHub Gold validated key derivation, nonce/IV behavior, side-channel resistance, implementation correctness, recovery properties, or resistance to a novel cryptanalytic attack.

The important architectural property is that the storage backend is intentionally treated as untrusted for confidentiality and integrity.

## Deduplication and content-defined chunking

Restic's config includes a repository-specific chunker polynomial used to split large files. Content-defined chunking lets unchanged regions remain reusable even when data is inserted or removed elsewhere in a file, avoiding the boundary-shift problem of fixed-size chunking.

The organization also maintains the standalone `restic/chunker` repository, which is a strong recursive follow-up target because it isolates this CDC logic from the larger backup application.

A useful operational caveat is that repository-to-repository copy can lose deduplication compatibility if the repositories were initialized with different chunker parameters. Current upstream documentation provides `init --from-repo --copy-chunker-params` specifically to preserve compatible splitting behavior for copied snapshots.

## Backend abstraction and reusable components

The source tree exposes a clear backend layer under `internal/backend`. Search inspection surfaced:

- `internal/backend/backend.go` — backend interface/core types;
- `internal/backend/cache/` — cached-backend behavior;
- `internal/backend/retry/` — retry wrapper and tests;
- `internal/backend/sema/` — concurrency/semaphore wrapper;
- `internal/backend/mem/` — in-memory backend useful for tests;
- `internal/backend/mock/` — mock backend;
- `internal/backend/test/` — reusable backend conformance-style test helpers.

Other valuable component areas include:

- `internal/archiver/` — filesystem scanning/tree creation and backup pipeline;
- `internal/repository/` — repository, pack, index and blob management;
- `internal/fs/` — cross-platform filesystem abstraction and metadata handling;
- `internal/filter/` — path/filter logic;
- `internal/bloblru/` — blob/cache behavior;
- `cmd/restic/` — CLI orchestration and integration-test surfaces.

These are catalog-worthy subcomponents even when their `internal/` package placement means they are not intended as stable external Go APIs. Reuse should therefore distinguish **architectural/reference value** from **drop-in library API stability**.

## Backup integrity and verification

Restic's upstream design principles explicitly treat verifiability as a core requirement and provide repository checking/restoration commands. Content and storage IDs are hash-based, while encrypted objects carry authentication data.

This makes Restic useful as a reference for separating:

1. storage-object integrity/authentication;
2. repository structure/index correctness;
3. snapshot/tree semantics;
4. actual restoration testing.

A backup being accepted into a repository is not equivalent to proving every future restore path. Operational users should still perform restores and periodic repository checks.

## Append-only / ransomware-resistance boundary

Upstream documentation describes append-only repository operation as a mitigation for compromised backup clients that might otherwise delete prior backups. This is an important threat-model distinction: encryption alone does not prevent a credentialed or compromised client from deleting encrypted backup objects.

Retention/pruning credentials and append-only upload credentials should therefore be treated as different privilege boundaries where the backend supports that design.

This dossier does **not** claim that Restic by itself makes arbitrary storage ransomware-proof. Backend authorization, immutability/object-lock policy, retention administration and credential separation remain deployment responsibilities.

## Storage backends and ecosystem

Native/documented backend surface includes:

- local filesystem;
- SFTP/SSH;
- Restic REST backend;
- Amazon S3 / S3-compatible storage;
- OpenStack Swift;
- Backblaze B2;
- Azure Blob Storage;
- Google Cloud Storage;
- rclone-backed services.

Strong recursive repositories/projects:

- `restic/rest-server` — dedicated REST backend server;
- `restic/chunker` — standalone content-defined chunking implementation;
- `restic/builder` — reproducible release build tooling;
- rclone `serve restic` — alternative REST-compatible service, but must be evaluated independently and should not inherit Restic's score/security assumptions;
- `resticprofile` — external profile/orchestration ecosystem candidate.

## Working evidence inspected

### Formal release

GitHub's release API showed **restic 0.19.1**, published **2026-07-05**, with source and numerous platform binaries plus signature/checksum-related release assets.

### Maintenance

Recent inspected `master` commits extend through **2026-08-29**. Examples include:

- Swift backend change storing API keys as a secret-string type to avoid debug-log leakage;
- documentation corrections concerning encryption statements;
- dependency updates;
- CI maintenance;
- Go migration/fix work.

The existence of active security-sensitive maintenance is a positive maintenance signal, not proof that no vulnerabilities exist.

### Tests

Repository search surfaces extensive unit and integration-test code across archiving, filesystem handling, backend wrappers, caches, tree processing, filters, mount behavior and other subsystems. Examples include:

- `cmd/restic/cmd_mount_integration_test.go`
- `internal/archiver/tree_test.go`
- `internal/archiver/scanner_test.go`
- `internal/backend/cache/backend_test.go`
- `internal/backend/retry/backend_retry_test.go`
- `internal/backend/sema/backend_test.go`
- `internal/backend/test/tests.go`
- platform-specific filesystem tests for Unix, Windows and Linux functionality.

This is upstream working evidence only. GitHub Gold did not execute the suite.

### Reproducible releases

The README states that release binaries have been reproducible since version 0.6.1 and points to `restic/builder` for reproduction instructions. This was not independently reproduced in this run.

## Current caveats and risk notes

### Backend behavior can fail independently

A backup engine can be correct while a cloud/backend API changes, stalls or applies unexpected semantics. Recent upstream issues demonstrate that backend-specific compatibility and timeout behavior are real operational concerns. Deployment guidance should therefore avoid treating every backend as equivalent merely because it implements the Restic interface.

### Remote REST implementations must be evaluated separately

The Restic repository format/protocol can be served by multiple implementations. Security properties of `rest-server`, rclone's Restic-serving mode, reverse proxies and object-storage gateways do not automatically inherit from the Restic client.

For example, a 2026 GitHub-reviewed advisory affected older `rclone serve restic` versions due to backend-root path validation. That was an rclone server issue, not evidence of the same flaw in `restic/restic`, but it illustrates why compatible backend implementations require their own evidence records.

### Password loss is unrecoverable

Upstream quick-start documentation explicitly warns that losing the repository password makes data irrecoverable. Key management and recovery procedures are therefore operationally critical.

### `internal/` packages are not stable public APIs

Many of the most interesting modules are Go `internal` packages. They are highly valuable as reference architecture and potentially adaptable code under BSD-2-Clause, but they should not be cataloged as promised stable external library APIs.

### Deduplication leaks equality at the client/repository logic level

Deduplication necessarily reasons about repeated content. GitHub Gold did not perform a leakage analysis of Restic's repository format, multi-user threat model, ciphertext/object-size metadata, snapshot traffic patterns or compromised-client scenarios.

## License and code-reuse rule

Root license: **BSD 2-Clause**.

This permits source and binary redistribution with or without modification subject to preservation of the copyright notice, license conditions and disclaimer requirements described in the license.

No Restic source code was copied into GitHub Gold during this run.

If future work adapts code such as backend wrappers or algorithms, preserve required notices and verify whether imported submodules/dependencies carry additional license obligations.

## Verification boundary for this run

Performed:

- inspected repository metadata;
- checked for duplicate Restic entries in GitHub Gold;
- inspected upstream README;
- inspected root license;
- inspected repository design/format documentation;
- inspected current release metadata;
- inspected recent commit activity;
- searched representative backend and test surfaces;
- inspected ecosystem relationships sufficiently to identify recursive leads.

Not performed:

- no local clone/build;
- no `go test` or integration-test execution;
- no backup or restore operation;
- no corruption/recovery exercise;
- no repository `check` execution;
- no cloud-backend test;
- no SFTP/REST server deployment;
- no append-only/ransomware simulation;
- no benchmark;
- no release-signature or reproducible-build reproduction;
- no independent cryptographic audit;
- no fuzzing or adversarial repository-format testing.

## Catalog positioning

Restic is **promotion-ready** as a VERIFIED candidate.

It should remain distinct from existing backup/storage entries such as Kopia rather than replacing them. Both may solve overlapping user problems while exposing different architecture, formats, implementation choices and ecosystem value.

Canonical catalog files are intentionally not modified in this dossier-only batch. Promotion should remain atomic across `MASTER_LIST.md` and the machine-readable catalog surfaces.

## Strongest next research leads

1. **`restic/chunker`** — isolate the content-defined chunking algorithm, polynomial selection, chunk-size bounds, tests and API reuse value.
2. **`restic/rest-server`** — inspect append-only mode, authentication, path validation, concurrency/resource controls and REST protocol semantics.
3. **Repository key format** — trace password KDF/key wrapping/master-key handling precisely from source rather than relying on high-level security language.
4. **Repository check/recovery** — map what `check`, `repair index`, `repair packs` and related recovery paths actually prove or reconstruct.
5. **Backend conformance framework** — inspect `internal/backend/test` to determine how reusable the storage-backend contract/test suite is.
6. **Kopia vs Restic architectural comparison** — compare chunking, encryption, repository mutation, snapshot metadata, maintenance and recovery without assuming either project is categorically superior.
7. **Object-lock/append-only strategies** — research how Restic interacts with immutable S3/object-store retention and what credentials must remain outside backup clients.

## Source pointers

- https://github.com/restic/restic
- https://github.com/restic/restic/blob/master/README.md
- https://github.com/restic/restic/blob/master/LICENSE
- https://github.com/restic/restic/blob/master/doc/design.rst
- https://github.com/restic/restic/releases/tag/v0.19.1
- https://github.com/restic/chunker
- https://github.com/restic/rest-server
- https://github.com/restic/builder
