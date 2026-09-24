# idb-tree — async page-store B-tree for browser persistence

- **Upstream:** https://github.com/garden-co/jazz/tree/main/crates/idb-tree
- **Author / organization:** Garden Computing (`garden-co`)
- **Category:** local-first storage / browser persistence / reusable Rust component
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 — S tier
  - Utility 5/5
  - Working evidence 5/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- **Version inspected:** 0.1.0
- **Language:** Rust (edition 2024), with wasm32 bindings
- **License:** MIT OR Apache-2.0 at the crate level
- **Discovery:** recursive follow-up from the Jazz v2 / Groove IVM research thread

## What it is

`idb-tree` is a standalone Rust crate inside `garden-co/jazz` described upstream as an **async page-store B-tree for Jazz browser persistence**. The tree owns B-tree structure, page residency, dirty generations and split/reclamation behavior while delegating durable page I/O to a deliberately small asynchronous `PageStore` abstraction.

The browser implementation uses IndexedDB as the backing page store. Upstream's design explicitly relies on IndexedDB to atomically replace a set of pages plus current-root metadata, so the B-tree itself does not implement a WAL/checkpoint phase.

## Why it matters

This is more interesting than a Jazz-specific persistence helper because the core engine is separated from its storage backend. `PageStore` exposes metadata load, page read and atomic commit operations; an in-memory implementation exists for deterministic contract tests, while wasm32 builds expose `IndexedDbPageStore`.

That makes the component a useful design reference for browser-resident databases that want a conventional ordered tree above an asynchronous transactional object store without forcing IndexedDB semantics throughout the query/database layer.

## Useful components

### `src/lib.rs`

Core asynchronous B-tree implementation. Notable design points include:

- configurable fixed page sizing (16 KiB default; minimum 1 KiB),
- byte-balanced page splitting rather than naïve count-midpoint splitting, important for variable-sized keys/values,
- generation-conflict and in-flight-commit error handling,
- explicit page residency/dirty-generation ownership,
- overflow/value-page handling and corruption checks,
- wasm32-specific export of the IndexedDB backend.

### `src/store.rs`

Defines the reusable storage boundary:

- `Metadata` tracks page size, generation, root page and next page ID,
- `Commit` carries expected generation, replacement metadata, page writes and deleted-page IDs,
- `PageStore` abstracts metadata/page reads and atomic commits,
- `MemoryPageStore` provides deterministic in-memory behavior for engine contract testing,
- optional `TreeOwnership`/reclamation hooks enforce the safety precondition for reclaiming obsolete pages.

The in-memory store rejects a commit when its expected generation differs from the current generation, then atomically applies page additions/deletions and advances the generation.

### `src/page.rs`

Page encoding/decoding and value-cell representation. This is part of the on-disk/browser persistence format and therefore should be treated as compatibility-sensitive rather than copied casually.

### `src/web.rs`

wasm32 IndexedDB page-store implementation used to bridge the generic B-tree to browser persistence.

## Working evidence

The crate is a first-class Cargo workspace member and is consumed by both Groove and Jazz's wasm layer. Its dedicated integration tests currently include:

- `byte_splits.rs` — variable-size/page-split behavior,
- `point_read_allocations.rs` — point-read allocation behavior,
- `reclamation.rs` — obsolete-page reclamation and ownership safety.

The source also contains deterministic `MemoryPageStore` support specifically so the same engine can exercise resident and genuinely pending-I/O behavior through the storage contract.

Repository-level realistic benchmark tooling recognizes `idb-tree-indexeddb-page-store` as a storage engine, giving additional upstream evidence that this is exercised as part of the broader Jazz/Groove performance work rather than being an orphaned experiment.

## Runtime / platform requirements

Core code is Rust. The IndexedDB backend is compiled for `wasm32` and pulls `js-sys`, `wasm-bindgen`, and `wasm-bindgen-futures`. The crate itself has a small native dependency surface (`thiserror`, `xxhash-rust`) plus `futures` for development/tests.

## Licensing

The crate manifest declares **MIT OR Apache-2.0**. No upstream implementation source is copied into GitHub Gold. Any future adaptation should preserve the applicable upstream notices and re-check the exact files/version being reused.

## Caveats / boundaries

- Current crate version is **0.1.0**; API and persistence-format stability should not be assumed.
- The design is optimized around an atomic page-store commit primitive. Porting to a backend without equivalent atomicity would require additional durability/recovery design.
- Safe obsolete-page reclamation has an explicit exclusivity contract: independent trees sharing a store cannot blindly reclaim pages while another handle may retain an older root.
- The browser backend is wasm32/IndexedDB-specific even though the core `PageStore` abstraction is generic.
- GitHub Gold did **not** compile the crate, execute its tests, run browser/IndexedDB persistence, inject failures, verify crash recovery, benchmark allocations/throughput, or independently validate page-format correctness. Test and benchmark references above are upstream evidence only.

## Verification performed

Repository-native inspection covered the crate manifest, source layout, core B-tree documentation/code, `PageStore` contract and in-memory implementation, dedicated test inventory, workspace/dependency references, and broader benchmark references. This is sufficient for **VERIFIED** evidence of a substantial implemented component, not independent runtime verification.

## Related projects

- `garden-co/jazz` — parent local-first database/runtime.
- `crates/groove` — incremental-view-maintenance engine that depends on `idb-tree`.
- Jazz wasm/browser persistence — direct consumer of the IndexedDB page-store path.

## Follow-up

The Jazz/Groove recursive thread has now yielded three substantial layers: Jazz v2, Groove IVM and `idb-tree`. Further expansion in this ecosystem should require a materially distinct component. The next research pass should rotate to another category rather than continuing to split the same stack into progressively smaller dossiers.