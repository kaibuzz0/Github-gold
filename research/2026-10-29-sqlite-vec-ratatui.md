# GitHub Gold research — sqlite-vec and Ratatui (2026-10-29 UTC)

## Method and provenance
GitHub-first discovery, checked against the 132-entry existing catalog and draft PR #7. Read upstream README, licenses, architecture/source, build manifests, release metadata, Actions run jobs and selected tests. The six seeded YouTube playlists did not provide new accessible transcript evidence in this batch; no video-derived claims. No upstream code copied, no local builds or executions.

## sqlite-vec — PROMISING / A25
- Repository: https://github.com/asg017/sqlite-vec (Alex Garcia). Successor to https://github.com/asg017/sqlite-vss; related https://github.com/asg017/sqlite-rembed.
- Root licenses: https://github.com/asg017/sqlite-vec/blob/main/LICENSE-MIT and https://github.com/asg017/sqlite-vec/blob/main/LICENSE-APACHE; dual permissive, preserve notices, separately inspect bindings/dependencies.
- Source: https://github.com/asg017/sqlite-vec/blob/main/sqlite-vec.c implements SQLite loadable virtual table, float32/int8/bit vectors, distances and query planning. https://github.com/asg017/sqlite-vec/blob/main/ARCHITECTURE.md explains vec0 shadow tables and idxStr KNN plan; experimental IVF in sqlite-vec-ivf.c and sqlite-vec-ivf-kmeans.c, reranking in sqlite-vec-rescore.c. Tests include tests/test-knn-distance-constraints.py, tests/test-ivf*.py, tests/test-cache-finalize.py; Python/Rust/Go bindings.
- Stable https://github.com/asg017/sqlite-vec/releases/tag/v0.1.9 published **2026-03-31**; newer https://github.com/asg017/sqlite-vec/releases/tag/v0.1.10-alpha.4 is **prerelease**, published **2026-05-18**. Latest main commit observed 04d28bd on May 18; README warns pre-v1 breaking changes.
- Upstream https://github.com/asg017/sqlite-vec/actions/runs/26018140783 **2026-05-18** Test workflow: **16 success / 1 skipped**. Linux/macOS/Windows extension jobs run `make test-loadable` which invokes pytest against tests/test-*.py. Android 4 ABIs, iOS, wasm32 and Pyodide are **build artifacts**, not demonstrated device/browser execution. The intentionally skipped job is ncruces-go. No independent accuracy, memory, malicious-input or performance testing.
- Runtime: SQLite loadable extension (extension loading must be enabled), pip/npm/cargo/Go packages; compile flags and platform-specific binaries. Risks: untrusted SQL/native extension loading, unbounded KNN queries, experimental IVF accuracy/compatibility, alpha API instability.
- Score: Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 4, Maintenance 3 = **25 / A**. PROMISING due to pre-v1 compatibility and no production/runtime confirmation despite passing upstream tests.

## Ratatui — VERIFIED (upstream) / S29
- Repository: https://github.com/ratatui/ratatui. MIT root license https://github.com/ratatui/ratatui/blob/main/LICENSE; prior tui-rs lineage; dependencies separately licensed.
- Architecture: https://github.com/ratatui/ratatui/blob/main/ARCHITECTURE.md documents post-0.30 split. ratatui-core/src/buffer/, layout/, widgets/ provide reusable rendering, Cassowary/kasuari layout and widget contracts; ratatui-widgets/src/ implements tables/charts/lists; ratatui-crossterm/, ratatui-termion/, ratatui-termina/, ratatui-termwiz/ provide backends. ratatui-macros/ and examples/ provide composition and tutorials. `ratatui-core/src/lib.rs` explicitly `#![no_std]`.
- https://github.com/ratatui/ratatui/releases/tag/ratatui-v0.30.2 published **2026-06-19**. Latest inspected main commit cdcb0c0 on **2026-10-28** improves no_std layout-cache guidance. Workspace Cargo.toml Rust MSRV **1.88.0** and MIT.
- Upstream https://github.com/ratatui/ratatui/actions/runs/40630817143 on **2026-10-28**, same main commit: **34/34 successful**. Linux/macOS/Windows stable and MSRV checks, no_std build, backend tests, library/docs tests, formatting/clippy, cargo-deny license/advisory checks. Passing PR workflow 40657794625 separately observed but is not main evidence.
- Install `cargo add ratatui`. Default Crossterm backend on desktop. no_std: disable default features, select appropriate backend and consider layout-cache + critical-section; hardware use and Termux untested. Application caveats: terminal raw mode restoration, Unicode layout, malicious escape sequences and terminal-specific behavior.
- Score: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5 = **29 / S**. VERIFIED means concrete **upstream** build/test evidence; no GitHub Gold independent run.

## Existing entry maintenance — Pyodide
- https://github.com/pyodide/pyodide retains **PROMISING / A25**. sqlite-vec upstream Test CI 26018140783 has a successful `build-pyodide` job that creates a WebAssembly side-module. This is a real build relationship, **not** proof that the extension loads or passes queries in a Pyodide browser runtime.
- Latest inspected Pyodide main workflow https://github.com/pyodide/pyodide/actions/runs/40838830915 (2026-10-29) remains failed on macOS undefined `mpd_*` linker symbols, with downstream tests skipped. Separate green code-quality and push workflows are not substitutes for the failing core build.

## Next investigations
1. sqlite-vec: run reproducible v0.1.9 loadable-extension tests and bounded KNN benchmarks; test IVF edge cases and Pyodide/Android runtime explicitly; monitor alpha-to-stable transition.
2. Ratatui: test Rust 1.88 and Termux-compatible backend, terminal escape/unicode edge cases, no_std layout cache, and downstream Mousefood firmware examples.
3. Pyodide: wait for current-main macOS linker fix and non-skipped downstream browser integration tests before promotion.

**Verification boundary:** All CI/build/test statements are upstream workflow evidence. No local builds, device tests, runtime executions, or security audits; no third-party implementation code copied.
