# Litestream — SQLite continuous backup and recovery engine

- **Repository:** https://github.com/benbjohnson/litestream
- **Author / Org:** Ben Johnson / Litestream contributors
- **Category:** SQLite / continuous backup / disaster recovery / storage abstraction / local-first infrastructure
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
- **Score breakdown:** Utility 5 / Working Evidence 5 / Reusability 5 / Novelty 5 / Documentation 5 / Maintenance 4
- **License:** Apache-2.0
- **Discovery:** GitHub-first category rotation after the Automerge local-first pass. No reliable YouTube transcript evidence was used for this candidate.

## What it does

Litestream is a standalone disaster-recovery system for SQLite. Upstream describes it as a background process that incrementally replicates database changes while interacting with SQLite through the SQLite API rather than by mutating database internals directly.

Current source is broader than a simple `sqlite -> S3` backup utility. The repository contains a layered replication/recovery engine with:

- WAL monitoring and coordinated checkpoint handling;
- transaction-oriented LTX files;
- replication-position tracking;
- point-in-time restore support;
- compaction and retention;
- a storage-backend abstraction (`ReplicaClient`);
- S3, Google Cloud Storage, Azure Blob Storage, SFTP, file, NATS and other backend implementations;
- resumable range-based reads during restore;
- Unix-socket runtime control;
- distributed leasing support;
- a developing SQLite VFS surface;
- CLI and library integration paths.

## Why it is Gold

SQLite is embedded and operationally simple, but a single database file creates a very different durability model from a managed replicated database service. Litestream supplies a focused replication/recovery layer without requiring applications to migrate away from SQLite.

Its highest-value reusable ideas are architectural rather than product-specific:

1. **WAL-aware replication without application integration** — the database manager monitors SQLite WAL activity and coordinates checkpoints while tracking replication state.
2. **Transaction-range LTX files** — replication is represented as ordered transaction ranges rather than opaque whole-database snapshots.
3. **Storage-backend abstraction** — the replication core is isolated from S3/GCS/Azure/SFTP/file/NATS transport details behind a common client interface.
4. **Resumable restore reads** — backend implementations are expected to support offset/range reads so interrupted restores can reopen a stream from the last successful byte position.
5. **Compaction and retention** — small incremental files can be compacted into higher levels while retention policy remains part of the replication system.
6. **Recovery-first test design** — upstream CI includes unit tests, backend tests, LTX behavioral gates, integration workflows, upgrade tests and nightly stability work.

## Concrete reusable components

### `db.go` — SQLite/WAL coordination

The `DB` component owns a SQLite connection, WAL monitoring, page/transaction state, checkpoint synchronization, background lifecycle and replication notifications. Upstream architecture documentation identifies methods for WAL checks, checkpointing, WAL readers, sync and compaction.

A subtle operational detail is the `_litestream_lock` table. Current README documentation says Litestream creates this table in the source database to acquire SQLite's write lock while coordinating synchronization around WAL checkpoints. Lock writes are performed in rolled-back transactions, but creation of the table modifies the source schema, so a database under Litestream should not be expected to remain byte-identical to its pre-Litestream state.

### `replica.go` — destination synchronization

`Replica` tracks the database's replication position and coordinates synchronization to a configured destination. Current source represents position using transaction ID, page number and a running checksum.

This separation is useful for systems that need a storage-neutral replication core: database state progression is independent from a particular cloud provider.

### `replica_client.go` + backend implementations

The `ReplicaClient` interface is the main storage abstraction. Current repository implementations include S3, Google Cloud Storage, Azure Blob Storage, SFTP, file and NATS-related paths, with additional provider-specific logic isolated from the core engine.

The repository's replica-client documentation specifies an important recovery contract: `OpenLTXFile` must honor an `offset` argument for range reads. `internal/resumable_reader.go` can reopen an interrupted restore stream from the last successful byte offset. A backend that ignores the offset contract can break restore behavior.

### LTX format and compaction

The repository documents LTX as a transaction-oriented replication format whose file names encode minimum and maximum transaction IDs. The current architecture layers incremental LTX generation, compaction and retention rather than continuously shipping complete SQLite database images.

This is one of the strongest component-level research targets because it captures a reusable pattern for durable incremental state transfer, ordering and point-in-time recovery.

### Restore path

`cmd/litestream/restore.go` reconstructs database state from LTX data. Current code and documentation distinguish normal metadata enumeration from metadata-heavy point-in-time lookup, and the restore path relies on ordered transaction ranges plus resumable remote reads.

Recent source history includes a 2026-08-31 fix for safely sorting v3 WAL offsets, which is evidence that restore ordering receives direct maintenance attention rather than being treated as a static legacy path.

### VFS

Current `vfs.go` exposes a SQLite VFS-oriented layer backed by `ReplicaClient`; source comments indicate an optional write-enabled path with periodic synchronization. CI explicitly builds VFS shared libraries on macOS and Linux. A 2026-08-29 commit added a thread-safe per-database VFS configuration registry.

This is an important follow-up target because it potentially changes Litestream from an external recovery daemon into a more directly embeddable remote-backed SQLite storage primitive. It should be evaluated separately from the mature backup/restore path rather than assuming equal maturity.

## Working evidence inspected

The main commit workflow currently includes:

- workflow-script tests;
- Go formatting/static analysis tooling;
- macOS VFS shared-library build verification;
- Linux VFS shared-library build verification;
- Windows cross-build validation;
- default and hardened Docker-image smoke tests;
- validation that the hardened image runs as UID 65532/nonroot;
- validation that the hardened image contains no shell;
- Go builds plus unit tests across the root, internal package, Azure, file, GCS, NATS, S3, SFTP and CLI packages;
- example-library builds/tests;
- a 32-bit regression test for v0.3 WAL segment ordering;
- an LTX behavioral integration gate;
- S3 mock testing.

The repository also has separate integration, manual integration, nightly stability, pre-release checklist, release, Docker release and upgrade-test workflows.

This is strong upstream working evidence. GitHub Gold did **not** execute those workflows itself.

## Maintenance

The latest stable GitHub release inspected is **v0.5.17**, published **2026-08-31**. Release assets include checksums and platform-specific binaries/packages; SBOM JSON artifacts are also published for release builds.

Recent commits through 2026-08-31 include:

- an `x/crypto` dependency bump specifically associated with `govulncheck`;
- S3 signing compatibility work;
- Tigris multipart-upload tuning;
- a restore-ordering correctness fix;
- duplicate database-path configuration validation;
- documentation of the internal SQLite lock table;
- the VFS per-database configuration registry.

Maintenance is scored 4/5 rather than 5/5 because the README still presents the project with a beta status badge and several newer surfaces, especially the VFS and evolving LTX generations, deserve version/migration scrutiny even though development is active.

## Supply-chain observations

The inspected main CI currently references common GitHub Actions using mutable version tags such as `actions/checkout@v4`, `actions/setup-go@v5`, Docker Actions major tags and `pre-commit/action@v3.0.0`, rather than pinning every third-party Action to an immutable commit SHA.

Release artifacts expose SHA-256 digests and checksum material, and current releases include SBOM artifacts. GitHub Gold did not independently verify the release signatures/digests or reproduce the build.

## License and reuse boundary

The repository root is **Apache License 2.0**. No upstream source was copied into GitHub Gold.

Apache-2.0 permits reuse subject to its attribution, notice, modification-notice and license requirements. Any extracted subcomponent should still be checked for third-party files or dependencies with separate terms before reuse.

## Operational caveats

- Litestream is disaster-recovery infrastructure, not a substitute for testing restores. A replica that is never restored in practice is not proven recoverable.
- The project modifies the source SQLite schema by creating `_litestream_lock`; byte identity with the original pre-Litestream database should not be assumed.
- Do not remove `_litestream_lock` while Litestream is running; upstream says synchronization around checkpoints can fail until the database state is reinitialized/restarted.
- Point-in-time restore depends on correct transaction ordering, metadata and retention. Aggressive retention can eliminate desired restore points.
- Remote storage credentials remain high-value secrets. Backup data confidentiality depends on the storage/security configuration used around Litestream; continuous replication is not itself an encryption boundary.
- Provider compatibility matters. S3-compatible services can differ in signing, multipart behavior, range semantics and consistency characteristics.
- A custom `ReplicaClient` must honor the interface's ordering/range-read semantics or recovery can be incorrect.
- VFS behavior should be treated as a separate maturity/security/performance surface until independently tested.

## Verification boundary

GitHub Gold inspected upstream README, root license, architecture documentation, source-search results, current CI/workflow structure, current release metadata and recent commit history.

GitHub Gold did **not**:

- build Litestream;
- run unit, integration, upgrade or nightly stability tests;
- create or mutate a SQLite database under Litestream;
- replicate to S3/GCS/Azure/SFTP/NATS/file storage;
- interrupt and resume a restore;
- perform point-in-time recovery;
- validate LTX checksums or compaction behavior;
- reproduce the v3 WAL ordering bug/fix;
- test WAL checkpoint locking;
- load or exercise the VFS shared library;
- independently verify release checksums or SBOM provenance;
- benchmark recovery point objective, recovery time, throughput or storage overhead;
- perform a security audit.

All functional claims above are limited to inspected upstream source, documentation, releases and workflow evidence.

## Provisional score rationale

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Solves a concrete SQLite durability/recovery problem with minimal application coupling. |
| Working evidence | 5 | Broad unit/backend/integration/stability/upgrade CI plus frequent releases and recovery-specific regression tests. |
| Reusability | 5 | Clear DB/Replica/ReplicaClient/LTX/VFS boundaries and library examples. |
| Novelty | 5 | WAL-to-LTX continuous replication, compaction and storage-neutral point-in-time recovery are technically distinctive. |
| Documentation | 5 | README plus architecture, format, backend and testing documentation. |
| Maintenance | 4 | Very active, but still beta-labeled and newer VFS/LTX evolution warrants conservative maturity scoring. |

**Total: 29 / 30 — provisional S tier.**

## Strongest next research leads

1. **LTX file format** — checksum chain, transaction range invariants, compaction levels and corruption detection.
2. **`internal/resumable_reader.go`** — failure/retry semantics and exact range-read contract.
3. **Point-in-time restore** — timestamp resolution, metadata consistency and retention edge cases.
4. **VFS implementation** — read path, write-enabled mode, cache/sync semantics, crash recovery and thread safety.
5. **Distributed leasing** — ownership/failover semantics and split-brain prevention for replicas.
6. **Backend conformance** — compare S3/GCS/Azure/SFTP/NATS implementations against a common behavioral contract.
7. **Upgrade compatibility** — v0.3 WAL history, LTX generations and migration guarantees across releases.
8. **Restore drills** — design a GitHub Gold test harness that creates randomized SQLite workloads, continuously replicates, injects process/network interruption, restores at multiple points and runs `PRAGMA integrity_check` plus application-level checks.

## Related ecosystem

- SQLite WAL and VFS APIs
- `superfly/ltx` transaction-file library
- S3-compatible object stores
- Fly.io / SQLite deployment patterns
- `rqlite/rqlite` and `tursodatabase/libsql` as architecturally different approaches to distributed/remote SQLite

Litestream should remain distinct from consensus databases or multi-writer distributed SQLite systems: its primary value is **continuous recovery and replica durability**, not transparent multi-node write consensus.