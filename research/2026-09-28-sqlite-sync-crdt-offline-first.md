# SQLite-Sync — offline-first CRDT synchronization for SQLite

- Upstream: https://github.com/sqliteai/sqlite-sync
- Organization: SQLite AI / SQLite Cloud, Inc.
- Category: local-first / databases / CRDT synchronization / edge
- Evidence: **VERIFIED** (repository-native evidence; not locally executed by GitHub Gold)
- Provisional Gold score: **27/30 — S tier**
  - Utility 5/5
  - Working evidence 5/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 5/5
  - Maintenance 4/5
- License: **Elastic License 2.0 with additional grant and Network Layer restriction — source-available, not ordinary permissive open source. Review before reuse.**

## What it is

SQLite-Sync is a multi-platform SQLite extension for offline-first replication. Local SQLite replicas can continue accepting writes while disconnected and later synchronize through CRDT merge semantics. Upstream documents SQLite Cloud, PostgreSQL, and self-hosted Supabase server paths, plus Linux, macOS, Windows, iOS, Android and WASM client surfaces.

The current feature surface includes Causal-Length Set, Delete-Wins, Add-Wins and Grow-Only Set algorithms, a line/block-oriented LWW mode intended for text/Markdown, built-in networking, and server-enforced row-level security for scoped synchronization.

## Why it is Gold

This is more than a conceptual local-first demo. The repository exposes a native SQLite extension, PostgreSQL implementation, packaging for multiple client ecosystems, explicit tests, current releases, and active correctness/performance maintenance. It is particularly interesting for field apps, edge devices and agents that already use SQLite and need disconnected operation without inventing a synchronization protocol.

The block-oriented text mode is also notable: instead of treating an entire text cell as one LWW value, it tracks blocks/lines so independent edits can survive synchronization. This is potentially useful for notes, Markdown knowledge bases and agent-memory stores, although its semantics should be evaluated against application requirements rather than assumed to provide general collaborative-text behavior.

## Repository-native working evidence

Upstream documents `make clean && make && make unittest` for the SQLite extension and a PostgreSQL Docker test path using `test/postgresql/full_test.sql`. The tree contains PostgreSQL smoke/full tests, network unit tests, Node-package tests, round-trip synchronization procedures, RLS round-trip procedures and stress-test material.

A stable **1.1.4** GitHub release was published **2026-09-21** with platform artifacts including Android AAR/ABI builds and Apple XCFramework packaging; GitHub records SHA-256 digests for release assets.

Maintenance is active. Recent commits through **2026-09-25** address bounded send windows after long offline backlogs, PostgreSQL transaction/db-version correctness, an SQLite chunk-resume performance bug reported to make a roughly 1 GB / 194-chunk drain drop from about 186 s to about 6.1 s in the upstream benchmark, and block-column replacement/tombstone correctness. These commit messages also describe added regression coverage. Treat those benchmark numbers as upstream evidence, not GitHub Gold measurements.

## Reusable surfaces

- SQLite extension and SQL API (`cloudsync_init`, network synchronization functions, UUID/helper surface).
- CRDT metadata/change capture around ordinary SQLite tables.
- Block-level text synchronization model.
- PostgreSQL synchronization extension and integration tests.
- Network chunking/resume and bounded-backlog send logic.
- Row-level-security synchronization model.
- Cross-platform packaging for native/mobile/WASM consumers.
- Test cases around rollback, duplicate delivery, tombstones, replacement cycles and PostgreSQL transaction boundaries.

## Requirements / platforms

The core is native code integrated as a SQLite extension, with PostgreSQL server support and wrappers/packages for Android, Apple platforms, Flutter, Expo/React Native and WASM documented upstream. Exact build prerequisites vary by target; consumers should follow the upstream installation documentation rather than assuming one portable binary.

## Licensing caveat — important

The repository's `LICENSE.md` is **Elastic License 2.0 with a project-specific additional grant**. It grants additional free use to OSI-licensed open-source projects, but expressly excludes modifying, replacing, bypassing, reimplementing or substituting the software's defined **Network Layer** from that additional grant. The file says such Network Layer work requires a commercial license, and commercial/non-open-source production use also requires a commercial license.

This substantially constrains extraction/reuse compared with Apache/MIT/BSD-style projects. **Do not copy or adapt implementation source into Github-gold.** Catalog and link to upstream. Any planned derivative, alternate transport/backend, managed service or commercial use needs a careful license review and potentially a commercial license from SQLite Cloud, Inc.

## Verification boundary

GitHub Gold inspected upstream README/documentation, repository test surfaces, recent commits, release metadata and the license. GitHub Gold **did not** compile the extension, execute tests, provision PostgreSQL/Supabase, install mobile artifacts, reproduce the 1 GB chunk benchmark, perform multi-device convergence testing, fuzz malformed sync payloads, audit RLS isolation, or conduct an independent security review.

Accordingly, VERIFIED here means there is strong repository-native evidence of a functioning maintained implementation; it does not mean independent runtime certification by this catalog.

## Discovery provenance

Independent GitHub-first discovery during category rotation after the MeshSat research sequence. No YouTube transcript claim is used as technical evidence for this entry.

## Related ecosystem / next leads

Upstream links a broader SQLite AI ecosystem including `sqlite-vector`, `sqlite-columnar`, `sqlite-js`, `sqlite-ai`, `sqlite-agent`, `sqlite-memory` and `sqlite-mcp`. These should be assessed separately rather than inheriting this project's score.

Strong follow-up research targets:

1. Inspect the CRDT algorithms and convergence/property-test coverage in detail.
2. Audit the block-level text algorithm's ordering, deletion and concurrent-edit semantics.
3. Trace the network chunk framing/resume/checkpoint model and hostile-payload bounds.
4. Verify exactly which self-hosted PostgreSQL/Supabase workflows remain permitted under the current Network Layer license wording.
5. Compare its correctness/evidence/licensing tradeoffs with Loomabase, Loro/Automerge-class libraries and other SQLite local-first systems.
