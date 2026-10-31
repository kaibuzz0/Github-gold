# Groove: embedded incremental-view-maintenance database engine

- **Upstream:** https://github.com/garden-co/jazz/tree/main/crates/groove
- **Author / Org:** Garden Computing / garden-co
- **Category:** embedded database / incremental view maintenance / reactive queries / Rust / database internals
- **Evidence:** VERIFIED (repository/source/spec/test/benchmark evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** **28 / 30 — S**
  - Utility: 5
  - Working evidence: 5
  - Reusability: 4
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 4
- **License:** MIT under the parent `garden-co/jazz` repository license; bundled homepage webfonts are separately licensed but are unrelated to this crate
- **Discovery:** recursive follow-up from the Jazz v2 dossier

## What it is

`groove` is an embedded Rust database engine built around incremental view maintenance (IVM). Its README describes the central model directly: instead of repeatedly executing queries against stored data, callers can subscribe to queries and receive the exact changes to their results as writes commit. The implementation is a small from-scratch engine inspired by the DBSP approach to incremental view maintenance.

The normative specification makes the separation from Jazz explicit: Groove is the local substrate beneath Jazz, but references to the Jazz specification are motivational rather than required to understand or validate Groove itself. That makes Groove worth cataloging as a component in its own right rather than merely as an internal Jazz detail.

## Architecture and useful components

The crate has a substantial standalone architecture:

- weighted record sets / Z-set-style deltas as the common data flowing through query graphs;
- maintained arrangements, effectively self-updating indexed copies of record sets shared across the query graph;
- subscriptions and one-shot queries over the same underlying engine;
- prepared query shapes whose bindings are represented as data;
- incremental commit ticks that propagate deltas through affected views;
- graph operators for filtering, projection, nullable unwrap, inner equi-join, anti-join, `UNION ALL`, `ArgMaxBy`, and non-nested recursion;
- a narrower SQL-lowering surface that deliberately rejects unsupported shapes rather than silently approximating them;
- asynchronous storage/evaluation contracts and large-value support in later specification chapters;
- an ordered key/value storage abstraction rather than a hard normative dependency on one storage implementation.

The source tree reflects those concepts with dedicated `ivm`, `db`, `storage`, records, query/schema, chunk, and large-value implementations. The current Cargo package is `groove` version `0.1.0`, Rust edition 2024. It depends on the sibling `idb-tree` crate and uses RocksDB through a workspace storage crate in development/benchmark paths.

## Correctness evidence

Groove's strongest feature for GitHub Gold is not simply that code exists; it has an unusually explicit correctness contract.

The normative correctness chapter defines an oracle property: at each successful commit/tick boundary, the initial snapshot plus consolidated subscription deltas must equal a fresh one-shot recomputation against current storage. One-shot reads must not perturb retained subscription streams, and persisted index reads must agree with a full-scan oracle.

The specification also defines a storage-atomicity boundary: base-table writes and durable index/view writes are staged and committed in one storage-atomic batch. If the final batch fails after runtime state has advanced, the `Database` instance must be poisoned instead of continuing from potentially torn state.

An out-of-band invariant registry maps stable `INV-*` specification identifiers to implementation/test receipts. A repository gate validates registry shape, duplicate IDs, cited tests, and covered-without-test mistakes. This is a strong code/spec/test traceability pattern worth reusing in other serious systems projects.

Repository code search confirms concrete Groove tests such as stable storage-key encoding, frozen manifest bytes, and oracle-based runtime/index checks. Upstream benchmark notes also report hundreds of Groove tests passing in recent development snapshots, but those counts are upstream records rather than GitHub Gold executions.

## Benchmark discipline

The benchmark specification is careful about separating correctness from speed. It provides two custom Cargo benchmark binaries:

- `scenario` for stateful workloads such as social feeds, recursive ACL evaluation, and one-shot operations;
- `micro` for local encode/decode, query-planning, and subscribe/unsubscribe overhead.

Scenario results are considered valid only if their maintained materialized state agrees with an oracle after the run. The documentation explicitly says a fast run that disagrees with recomputation is a failed run, not a benchmark result.

The harness records durability assumptions and separates noisy elapsed-time measurements from deterministic structural counters. The docs explicitly characterize retained developer-laptop timings as directional rather than performance promises.

## Scope and limitations

Groove is not a drop-in replacement for a full SQL database.

The graph execution layer is richer than its SQL lowering. The current SQL subset supports `SELECT … FROM`, supported predicates/projections, inner equi-joins, `UNION ALL`, and equality prepared parameters. The specification explicitly rejects unsupported SQL such as `SELECT DISTINCT`, aggregates/grouping, ordering/limit/offset, outer joins, derived tables, recursive CTEs, non-equality prepared parameters, and unsupported join keys.

Concurrency is also deliberately bounded: the current contract is a single writer with synchronous ticks and does not provide MVCC. Recursive support is intentionally constrained. These are important architectural boundaries, not minor omissions.

The crate is currently version `0.1.0` and lives inside the Jazz monorepo rather than presenting itself as a mature separately versioned database product. Its standalone reuse potential is therefore technically strong but operationally less proven than the architecture/specification quality might suggest.

## License / reuse

The parent repository is MIT licensed, with an exception only for bundled homepage webfonts under `docs/public/fonts/`. Groove source is therefore permissively reusable subject to preservation of the MIT copyright and permission notice.

No upstream source was copied into GitHub Gold.

## Verification performed

GitHub Gold inspected:

- `crates/groove/README.md`;
- `crates/groove/Cargo.toml`;
- the Groove source-tree inventory;
- the normative specification chapter map/introduction;
- the normative correctness/determinism/scope chapter;
- the invariant-registry documentation;
- the benchmark methodology;
- repository code-search evidence for Groove tests;
- the parent repository MIT license.

This verifies the existence and documented contracts of the embedded engine, its IVM architecture, explicit SQL/operator scope, benchmark harnesses, test/invariant infrastructure, crate metadata and licensing.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- compile the `groove` crate;
- execute its Rust tests, invariant gates or benchmarks;
- reproduce any upstream performance numbers;
- compare it experimentally with SQLite, DBSP or another IVM engine;
- exercise RocksDB or browser/IndexedDB storage paths;
- validate crash recovery or poisoned-database behavior;
- independently prove the oracle property or inspect every invariant receipt;
- deploy Groove outside the Jazz monorepo as an independent application dependency.

Upstream test counts and benchmark observations are therefore upstream evidence, not independent GitHub Gold measurements.

## Why it matters for GitHub Gold

Groove is unusually valuable as both implementation and research reference. It concentrates incremental query maintenance, maintained arrangements, prepared parameterized graphs, recursion, explicit correctness oracles, storage atomicity, deterministic regression counters, and spec-to-test invariant traceability in a relatively focused embedded engine.

The strongest reusable lesson may be its engineering discipline: correctness is stated as a recomputation equality, performance results are invalid unless that equality holds, and stable invariant IDs connect normative requirements to tests and implementation anchors.

Its young version number, monorepo coupling, deliberately narrow SQL surface and single-writer/no-MVCC model keep it below a perfect score despite excellent technical evidence.

## Strongest follow-up

Inspect the sibling `crates/idb-tree` storage component and Groove's storage abstraction to determine whether the browser/IndexedDB-oriented ordered key/value layer is independently reusable. After that, rotate out of the Jazz/Groove thread unless a materially stronger recursive lead appears.