# SQLite Disaster Recovery Research — 2026-08-21

## Candidate: Litestream

- **Repository:** https://github.com/benbjohnson/litestream
- **Author:** Ben Johnson / Litestream contributors
- **Category:** SQLite / disaster recovery / continuous replication / backup infrastructure
- **Evidence:** PROMISING
- **Provisional tier / score:** A / 25
- **Promotion status:** DEFERRED — monitor the next stable release and post-fix history before canonical promotion
- **License:** Apache-2.0

### What it does

Litestream is a standalone disaster-recovery system for SQLite. Upstream describes it as a background process that incrementally replicates SQLite changes to another file or S3-compatible storage while interacting with SQLite through SQLite APIs rather than modifying the database file out-of-band.

The project is unusually relevant to GitHub Gold because it turns an embedded, local-first database into something that can have continuous off-machine recovery without requiring a full client/server database migration.

### High-value components and architecture

Specific implementation and documentation surfaces worth studying include:

- `db.go` — database-side orchestration and SQLite integration
- `vfs.go` — SQLite VFS-related integration surface
- `replica.go` — replica orchestration
- replica-client abstraction plus provider implementations such as `s3/replica_client.go`
- `cmd/litestream/replicate.go` — replication command workflow
- `cmd/litestream/restore.go` — restore workflow
- `docs/ARCHITECTURE.md` — architecture documentation
- `docs/LTX_FORMAT.md` — LTX replication format documentation
- `docs/REPLICA_CLIENT_GUIDE.md` — provider/client extension guidance
- `tests/integration/` plus replica unit tests — correctness evidence and reusable test patterns
- Docker/release automation and operational patterns

Search also surfaced an MCP command implementation and project-maintained AI/agent guidance, which may be useful later as examples of exposing operational tooling to agents; these are secondary to the database-recovery architecture.

### Verification performed

GitHub Gold inspected:

- upstream repository metadata
- upstream README
- root `LICENSE`
- repository file structure and component locations
- recent commit history through 2026-08-19
- presence of unit/integration test surfaces

GitHub Gold did **not** independently run Litestream, restore a database, inject corruption, benchmark replication lag, validate object-store behavior, or reproduce upstream tests in this pass.

### Maintenance evidence

Recent upstream activity is strong and specific rather than cosmetic:

- **2026-08-19:** config fix allowing `l0-retention: 0` to disable retention
- **2026-08-19:** replica correctness fix to reject a truncated page index
- **2026-08-18:** dependency fix described upstream as removing a **release-blocking SQLite WAL-reset corruption exposure**
- **2026-08-18:** retention/snapshot-floor documentation clarification
- **2026-08-17:** restore fix for v3 WAL segments exceeding 4 GB
- **2026-08-15:** restore retry behavior for provider throttling
- **2026-08-14:** Go toolchain maintenance

This is evidence of active maintenance, but the corruption-related fix is also a material caution for a disaster-recovery product.

### Why promotion is deferred

Litestream meets many Gold criteria: focused utility, clear architecture, permissive licensing, real tests, documented extension points, active maintenance, and a compelling local-first use case.

However, a disaster-recovery tool has an unusually high correctness bar. A recent upstream commit explicitly describes removal of a release-blocking WAL-reset corruption exposure, followed immediately by additional restore and replica-index correctness fixes. That does not make the project bad; in fact, the fixes are evidence of serious maintenance. It does mean GitHub Gold should avoid labeling the current state as fully VERIFIED for recovery integrity without either:

1. observing a stable release that contains these fixes plus a reasonable post-release period, or
2. independently exercising replication and restore paths against corruption/failure scenarios.

For now the correct classification is **PROMISING / A 25 / DEFERRED** rather than READY.

### Licensing and reuse

The root repository is Apache-2.0. Covered source can generally be reused with required notices and attribution. Provider SDKs, cloud APIs, SQLite itself, containers, and other dependencies may carry their own terms and should still be checked at component level.

### Related ecosystem leads

- SQLite WAL and VFS internals
- LTX format and `superfly/ltx`
- S3-compatible object stores and provider-specific replica clients
- Fly.io deployment patterns
- PocketBase / SQLite application deployments using Litestream
- `liters` and other independent SQLite replication/recovery experiments
- disaster-recovery testing techniques for embedded databases

### Next verification trigger

Revisit when upstream publishes a stable release containing the August 17–19 correctness fixes. At that point inspect release notes, remaining open correctness issues, CI/tests, and any follow-up corruption/restore regressions. If evidence is clean, consider promotion to VERIFIED A/S tier and add to `catalog/candidate_queue.json`.
