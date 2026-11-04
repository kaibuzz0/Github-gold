# Jazz v2: local-first relational database and query-driven sync

- **Upstream:** https://github.com/garden-co/jazz
- **Author / Org:** Garden Computing / garden-co
- **Category:** local-first / distributed database / synchronization / reactive data / developer infrastructure
- **Evidence:** VERIFIED (repository/source/spec/release evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** **28 / 30 — S**
  - Utility: 5
  - Working evidence: 5
  - Reusability: 5
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 3
- **License:** MIT, except bundled webfonts under `docs/public/fonts/`, which retain separate upstream terms
- **Discovery:** GitHub-first category rotation after completing the Syncthing infrastructure thread

## What it is

Jazz v2 is an actively developed local-first relational database spanning frontend and backend runtimes. Its current README describes partial-table synchronization, durable streams and files, while the normative Rust-side architecture specification defines a distributed real-time database with edit history, row-level-security-authorized sync, mergeable eventually-consistent transactions, and serializable exclusive transactions.

This is a materially different architecture from the file-oriented synchronization systems previously cataloged. Jazz is application data infrastructure: queries, transactions, authorization, synchronization, local persistence and incremental view maintenance are designed as one system.

## Architecture evidence

The authoritative `crates/jazz/SPEC/` tree is unusually detailed. The introduction explicitly distinguishes normative numbered chapters from implementation-guidance appendices and maps contracts for:

- data model and identity;
- transactions and durability;
- history, domination and merging;
- reads and snapshots;
- queries and query-driven sync;
- row-level authorization;
- sync protocol;
- Core, clients and local persistence relays;
- schema evolution/migrations;
- time-travel/branch views;
- the high-level database API;
- lowering to the `groove` incremental-view-maintenance engine;
- maintained subscription views;
- representation boundaries and large-value handling.

The spec states that Jazz has one query substrate: application concepts lower onto `groove`, rather than maintaining a separate synchronization query engine. It also specifies Core as the authority for read/write authorization and final transaction fate, while local relays provide persistence/transport rather than becoming an independent authority tier.

## Working and maintenance evidence

The repository provides a concrete source build/test path using pnpm plus Rust/WASM tooling, including `pnpm build` and `pnpm test`. Server builds use RocksDB and require a C/C++ toolchain plus libclang. The README also documents correctness-artifact production/verification for WASM/NAPI consumers and separate React Native acceptance gates.

The GitHub Actions tree contains dedicated CI, Rust shadow CI, package builds, benchmark workflows, continuous simulation/soak testing, release previews, documentation builds, platform receipts and package publishing workflows.

Development is extremely active as of 2026-09-24. Multiple commits landed on that date, including React Native contract tests and CI changes. The latest inspected release is `v2.0.0-alpha.56`, published 2026-09-21.

That release documents substantial performance work, transport multiplexing, fail-closed permission changes, schema/relationship API changes, migration validation, ARM64 synchronization fixes and a sync protocol v3 transition. These are strong engineering signals, but they also reinforce the primary caveat: this is alpha software with a moving protocol/API surface.

## Useful reusable components and ideas

- `crates/jazz/` — core relational/distributed database implementation and normative contracts.
- `crates/jazz/SPEC/` — unusually detailed architecture/specification corpus useful for studying local-first database semantics.
- `crates/groove/` — incremental-view-maintenance/query substrate beneath Jazz.
- query-driven synchronization and maintained subscription-view architecture.
- mergeable vs exclusive transaction model.
- row-level-security policies integrated into synchronization.
- local persistence relay architecture.
- WASM, NAPI and React Native bindings/tooling.
- correctness artifact sealing/verification and cross-runtime consumer testing.
- continuous simulation/soak and benchmark CI patterns.
- schema migration and stored-identity validation tooling.

## Platforms / runtime

Current project tooling spans TypeScript/JavaScript and Rust, with browser/WASM, Node/NAPI and React Native integration paths. The README lists Node LTS, pnpm 10+, Rust/rustup and wasm-pack among development prerequisites. Server builds additionally require C/C++ tooling and libclang because RocksDB is compiled from source.

The README currently warns that Jazz 2.0 is an alpha with an entirely new API. It specifically notes that persistent/device-supported memory runtimes are not yet available for the Expo binding scaffold in this alpha.

## License / reuse

The repository is MIT licensed. The license explicitly excludes webfont files bundled under `docs/public/fonts/`; those remain under their upstream license terms. This makes most implementation concepts/source permissively reusable with preservation of the MIT copyright and permission notice, while the font exception must not be silently treated as MIT.

No upstream source was copied into GitHub Gold.

## Verification performed

GitHub Gold inspected:

- current upstream README;
- repository license;
- recent commit history;
- recent release metadata/changelog;
- `.github/workflows/` inventory;
- the authoritative `crates/jazz/SPEC/` inventory;
- the normative introduction/specification chapter.

This supports the repository's build/test paths, architecture claims, active maintenance, release state, licensing and existence of substantial CI/specification infrastructure.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- install dependencies or build Jazz;
- execute `pnpm test` or Rust tests;
- run the continuous simulation/soak workflows;
- operate a Core server or self-hosted deployment;
- verify offline conflict behavior with multiple live clients;
- benchmark query/sync performance;
- reproduce the release's performance claims;
- validate React Native, NAPI or WASM artifacts;
- independently audit authorization, synchronization correctness or cryptography/security boundaries.

Upstream benchmark numbers and runtime claims are therefore recorded as upstream evidence, not independent GitHub Gold measurements.

## Caveats

- **Alpha maturity:** v2 is explicitly alpha and the API is new.
- **Protocol churn:** alpha.56 includes a breaking sync-protocol transition requiring compatible clients/server deployment.
- **Operational complexity:** source builds span Rust, WASM, Node tooling, RocksDB and native toolchains.
- **Mobile limitation:** the current README identifies missing persistent/device-supported memory runtimes for the Expo scaffold.
- **Authority model:** local-first does not mean fully peer-authoritative; the normative architecture assigns authorization and final transaction fate to Core.
- **License exception:** bundled webfonts are not covered by the repository MIT license.

## Why it matters for GitHub Gold

Jazz v2 is valuable less as a generic 'database link' than as a concentrated reference implementation for modern local-first application architecture: relational data, reactive queries, authorization-aware synchronization, incremental view maintenance, local persistence, multiple transaction semantics and cross-runtime bindings are being developed together with unusually explicit specifications and CI discipline.

Its alpha status prevents treating it as low-risk production infrastructure, but the technical depth, active engineering and reusable architectural ideas justify a high-confidence S-tier research entry.

## Strongest follow-up

Inspect `crates/groove` as a separate component-level candidate. The incremental-view-maintenance engine may be independently valuable beyond Jazz and should be scored on its own evidence rather than inheriting Jazz's ranking.