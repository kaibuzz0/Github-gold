# restic — encrypted, deduplicated, verifiable backup infrastructure

- **Repository:** https://github.com/restic/restic
- **Author / Org:** restic
- **Category:** backup / archival / encryption / deduplication / storage infrastructure
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29/30 — **S**
- **License:** BSD-2-Clause
- **Discovery:** GitHub-first discovery; followed up after RadioLib write was blocked
- **GitHub Gold execution boundary:** Repository-native evidence inspected. GitHub Gold did **not** install restic, create or restore a backup, execute tests, run `check`, reproduce release builds, benchmark deduplication, or audit cryptography.

## Why it matters

restic is mature backup infrastructure built around encrypted, content-deduplicated snapshots with explicit restore and integrity-verification workflows. It is useful as an end-user tool and as a source of reusable design ideas for archival systems: repository formats, pack/index/tree handling, content-defined chunking, backend abstraction, integrity checking, pruning, snapshot semantics and reproducible release engineering.

## Evidence inspected

The current README states support for Linux, macOS, Windows, FreeBSD and OpenBSD. Native backends include local storage, SFTP, REST, S3-compatible storage, OpenStack Swift, Backblaze B2, Azure Blob Storage and Google Cloud Storage, with additional services available through rclone.

The README documents the project's design principles as easy, fast, verifiable, secure and efficient. It explicitly treats backup storage as untrusted and uses cryptography for confidentiality and integrity. It also states that released binaries have been reproducible since version 0.6.1 and points to the separate `restic/builder` repository for reproduction instructions.

Current source reports `0.19.1-dev`; the changelog records **restic 0.19.1 on 2026-07-05**.

Integrity verification is implemented, not merely documented. `cmd/restic/cmd_check.go` states that `check` verifies structural consistency and integrity of snapshots, trees and pack files, with options to verify actual repository data. `internal/repository/checker.go` contains pack/blob integrity checking. Contributor documentation exposes in-memory repository test helpers and `checker.TestCheckRepo()`.

Deduplication has a concrete reusable boundary. `internal/restic/chunker.go` defines a variable-length Chunker interface; `internal/repository/chunker.go` uses the separate `github.com/restic/chunker` implementation. Repository configuration persists a chunker polynomial, and initialization supports copying chunker parameters when constructing a secondary repository.

## Particularly valuable components

- Repository pack/index/tree architecture and consistency checker.
- `restic check` structural and data-integrity verification paths.
- Content-defined chunking boundary and the separate `restic/chunker` dependency.
- Snapshot, restore, prune and repository-migration logic.
- Backend abstraction spanning local, SSH, REST and object-storage systems.
- `restic/rest-server` companion service and documented REST backend protocol.
- Reproducible release process via `restic/builder`.
- In-memory repository testing helpers for deterministic tests.

## Provisional score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | High-value backup and archival capability. |
| Working evidence | 5 | Mature implementation, integrity checker, tests/CI signals, releases and documentation. |
| Reusability | 5 | Clear internal boundaries plus companion chunker/server/builder projects. |
| Novelty | 4 | Backup/deduplication is established, but the integrated design and verification model are technically valuable. |
| Documentation | 5 | Extensive docs, README, commands, man pages and design guidance. |
| Maintenance | 5 | Current 0.19.x development and recent 2026 release history. |
| **Total** | **29/30** | **S** |

## Licensing and caveats

The root `LICENSE` is BSD-2-Clause. No upstream implementation was copied into GitHub Gold.

A backup tool's existence is not evidence that a particular deployment is recoverable. Operators still need independent restore drills, credential/password protection, backend durability and appropriate repository-integrity checks. The README explicitly warns that losing the repository password makes data irrecoverable.

Reproducible-build claims are upstream claims backed by a documented builder workflow; GitHub Gold did not independently reproduce a byte-identical release.

## Follow-up research

1. Map pack/index/tree format invariants and corruption recovery behavior.
2. Inspect `restic/chunker` algorithm, polynomial handling and compatibility constraints.
3. Trace encryption/authentication and key lifecycle without making unsupported security claims.
4. Inspect `check --read-data` and subset-check scheduling for large repositories.
5. Study prune/repack failure atomicity and interruption recovery.
6. Inspect `rest-server` authorization, append-only modes and failure model.
7. Reproduce a release through `restic/builder` in a future execution-capable verification pass.
