# Loomabase — offline-first SQLite/PostgreSQL sync engine

- **Upstream:** https://github.com/JustVugg/loomabase
- **Author:** JustVugg / Loomabase contributors
- **Category:** local-first software / databases / synchronization / CRDTs
- **Evidence:** VERIFIED (source-level/upstream-test evidence; not independently executed by GitHub Gold)
- **Gold score:** 27/30 — provisional S tier
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 3/5
- **License:** Apache-2.0
- **Languages/surfaces:** Rust core; SQLite client; PostgreSQL adapter; TypeScript/JavaScript SDK preview; optional C ABI
- **Discovery:** independent GitHub-first discovery after rotating away from emergency-mesh research

## What it is

Loomabase is an alpha offline-first synchronization engine for applications that keep SQLite replicas on clients and synchronize against PostgreSQL. Its notable design choice is **column-level LWW CRDT state** rather than row/document-level conflict resolution. Each synchronized cell carries a Lamport clock and device ID, so concurrent offline edits to different columns can survive independently.

The upstream project is explicit that it is alpha: the public API and wire protocol are pre-1.0, the JS SDK is not yet published to npm, and production users should understand the conflict semantics rather than treat it as a hosted BaaS.

## Why it matters

This is useful GitHub Gold because it is both a whole project and a collection of reusable synchronization patterns:

1. **Column-granular deterministic merge** — `(row_id, column_name)` CRDT cells avoid unrelated field updates overwriting one another.
2. **SQLite change capture** — local writes are captured through SQLite-side machinery and emitted as synchronization deltas.
3. **Explicit transactional boundaries** — client and PostgreSQL paths use transactions rather than treating sync as an eventually-consistent collection of ad-hoc writes.
4. **Bounded anti-entropy** — the protocol exposes cursors and bounded response sizes rather than assuming unbounded full-state transfer.
5. **Partial replicas and authorization boundaries** — upstream includes scoped replicas, authenticated device attribution, tenant-aware PostgreSQL paths, RLS support, policy hooks, rejected-cell reporting, and audit-log support.
6. **Multiple integration surfaces** — Rust, a JS/TS preview SDK, runnable examples, browser demo, Supabase integration material, and an optional C ABI.

## Concrete working evidence inspected

The repository contains a substantial `tests/` surface rather than relying only on README claims. Inspected repository contents include dedicated tests for anti-entropy, authentication, CRDT laws, delete lifecycle, HTTP server behavior, model convergence, multi-table operation, multi-tenancy, offline convergence, partial replicas, PostgreSQL integration, RLS, and schema migration.

`tests/crdt_laws.rs` directly checks:

- commutativity of cell merges;
- convergence across all delivery orders for three payloads;
- atomic rollback when a merge fails;
- bounded change feeds;
- cursor continuation;
- rejection/reset behavior when another device attempts to reuse a device-bound cursor.

`tests/offline_convergence.rs` constructs two in-memory SQLite clients plus a CRDT server, synchronizes a baseline, performs different-column edits while the devices are logically offline, reconnects them, and asserts that both replicas converge with both edits preserved. It also checks idempotence of repeated delivery and deterministic device-ID tie-breaking for equal Lamport clocks, including rejection of spoofed device attribution.

Upstream documents a runnable phone/desktop reconnect smoke test and local verification commands for the Rust workspace and JS package. GitHub Gold did **not** execute those commands in this pass.

## Maintenance signal

The latest inspected upstream commit is `2ed0f0a9c7569f372e25a239d89d12e79deae2fb` from **2026-06-28** (`Simplify README for alpha release`). The same development burst added the JS SDK, demos, FFI, fuzzing, benchmarks, deployment/Supabase tooling, architecture/security documentation and CI.

A material caveat is that upstream then committed `Disable GitHub Actions workflows` on 2026-06-28. The presence of tests is strong source-level evidence, but disabled hosted CI reduces current continuous-verification confidence and is why Maintenance is held to 3/5 rather than scored as top-tier.

## Requirements / deployment notes

- Rust toolchain for the core engine/examples.
- SQLite client replicas (`rusqlite` in the Rust implementation).
- PostgreSQL for the server adapter / PostgreSQL integration path.
- Node/npm for the preview JS/TS SDK and browser/phone-desktop examples.
- PostgreSQL integration tests require an explicit `LOOMABASE_TEST_DATABASE_URL`.
- Public API and wire format remain pre-1.0.

## Licensing

Root source is Apache License 2.0. That is favorable for reuse, but downstream dependencies and deployment integrations retain their own licenses/notices. No upstream source was copied into GitHub Gold.

## Verification boundary

GitHub Gold inspected repository-native documentation, test files, repository structure, license and recent commit history. It did **not**:

- compile the Rust workspace;
- execute the Rust/JS test suites;
- run the offline reconnect demo;
- provision PostgreSQL or Supabase;
- fuzz the protocol;
- benchmark throughput/storage overhead;
- test crash recovery or migrations;
- perform a security review;
- independently validate production readiness.

Accordingly, **VERIFIED** here means concrete implementation plus upstream repository-native test evidence was inspected, not that GitHub Gold independently ran the software.

## Caveats / risks

- Alpha project; API and wire compatibility are not frozen.
- JS package is a preview and is not yet published to npm.
- Latest inspected activity is June 2026 rather than current-week development.
- Hosted GitHub Actions were explicitly disabled, weakening ongoing regression evidence.
- LWW CRDTs provide deterministic convergence but do not automatically encode application-specific semantic conflict resolution.
- Production multi-tenant/RLS correctness should be independently threat-modeled and integration-tested before relying on it as a security boundary.

## Strong follow-up leads

- Inspect `partial_replica.rs` and the scoped anti-entropy design in depth.
- Trace SQLite trigger/change-capture and Lamport-clock persistence behavior through crashes/restarts.
- Inspect protocol fuzz targets and whether malformed/oversized payload boundaries are comprehensively defended.
- Compare its column-level LWW semantics against established local-first systems and identify cases where row lifecycle/delete semantics become surprising.
- Investigate why CI was disabled and whether a later branch/release restores continuous verification.
