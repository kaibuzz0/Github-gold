# ripgrep, Tauri and Immich CI maintenance — 2026-10-28 UTC

GitHub-first investigation; no accessible YouTube transcript was used as evidence. Both additions were absent from the 118-entry canonical catalog and empty candidate queue before this batch. No upstream source code or binaries were copied. No independent build, deployment, hardware test, fuzzing or security audit was performed.

## ripgrep — VERIFIED (upstream) / S29

**Upstream:** https://github.com/BurntSushi/ripgrep ; author Andrew Gallant; MIT OR Unlicense (inspected root LICENSE-MIT and per-crate licenses). Stable [15.2.0](https://github.com/BurntSushi/ripgrep/releases/tag/15.2.0) published 2026-07-15. `Cargo.toml` declares Rust 1.96 and 2024 edition. [Master CI run 40612963042](https://github.com/BurntSushi/ripgrep/actions/runs/40612963042) passed 23/23 jobs on 2026-10-28: Linux/macOS/Windows, ARM, RISC-V, s390x, WASM, docs, benchmark tests and compilation of fuzz targets. Fuzz-target compilation is NOT evidence that fuzzing was run.

**Reusable components (verified source paths):** `crates/ignore/src/walk.rs` implements parallel directory traversal; `crates/ignore/src/gitignore.rs` handles ignore matching; `crates/globset/src/glob.rs` handles glob expressions; `crates/searcher/src/searcher/` provides line-oriented scanning/mmap; `crates/regex/src/matcher.rs` and `crates/pcre2/src/matcher.rs` are matcher backends; `crates/printer/src/json.rs` emits structured results; `crates/core/search.rs` orchestrates CLI search; `tests/tests.rs` is the integration harness. `crates/ignore/README.md` includes a runnable library example, not executed here.

**Caveats:** Hidden, binary and ignore-filtered paths are skipped by default; `rg -uuu` changes that behavior. Do not assume upstream benchmarks generalize to other corpora. PCRE2 and untrusted regex/resource limits merit review. Dependency licenses separate. Ecosystem leads: BurntSushi/regex-automata, BurntSushi/aho-corasick, sharkdp/fd.

## Tauri — VERIFIED (upstream PR core tests) / S27

**Upstream:** https://github.com/tauri-apps/tauri ; MIT OR Apache-2.0 (Cargo workspace and inspected `crates/tauri/LICENSE-MIT`), separate dependencies and plugin licenses. Monorepo release [tauri-v2.12.5](https://github.com/tauri-apps/tauri/releases/tag/tauri-v2.12.5) published 2026-10-21. Current dev `Cargo.toml` specifies Rust 1.90. System webviews: WRY and TAO; Linux v2 needs WebKitGTK 4.1; mobile needs native SDKs.

**Reusable components (verified source paths):** `crates/tauri/src/ipc/authority.rs` and `protocol.rs` define IPC trust boundaries; `crates/tauri-utils/src/acl/` handles capability resolution; `crates/tauri-runtime-wry/src/webview.rs` wraps system webviews; `crates/tauri/src/plugin.rs` supports plugins; `crates/tauri-bundler/src/bundle/` builds installers; `crates/tauri-codegen/` embeds assets; `packages/api/` provides frontend JS/TS bridge. E2E fixtures in `packages/api-e2e/test/specs/`.

**Positive upstream evidence:** [PR branch ipc-introspection core CI 40530165720](https://github.com/tauri-apps/tauri/actions/runs/40530165720) on 2026-10-27: 10/10 jobs passed; Linux/Windows/macOS Rust tests and Android/iOS cross-builds. Not dev-branch core CI and not physical mobile execution.

**Negative upstream evidence:** [dev Audit 40609767411](https://github.com/tauri-apps/tauri/actions/runs/40609767411) on 2026-10-28: `audit-rust` passed, `audit-js` failed. Job log shows a single LOW-severity `deepmerge` 4.2.0–4.3.1 advisory ([GHSA-gcqx-w48m-w2h4](https://github.com/advisories/GHSA-gcqx-w48m-w2h4)) in `examples/api > @sveltejs/vite-plugin-svelte > deepmerge`; `pnpm audit` exited 1. This is an example dependency path; do not misstate as a demonstrated exploitable flaw in Tauri runtime.

**Risks and follow-ups:** Test restrictive capability configurations, cross-origin IPC, updater signatures, plugin permissions, desktop packaging and actual Android/iOS runtime. Related: tauri-apps/wry, tauri-apps/tao, tauri-apps/create-tauri-app, tauri-apps/tauri-action, tauri-apps/plugins-workspace.

## Existing catalog maintenance: Immich remains PROMISING / A25

[2026-10-28 mobile passkey PR Test 40653312777](https://github.com/immich-app/immich/actions/runs/40653312777) and [Test 40653532254](https://github.com/immich-app/immich/actions/runs/40653532254) both concluded success, but job inspection shows only mobile unit, OpenAPI client, SQL schema and shell checks ran. Web/server/ML end-to-end jobs and server medium tests were **skipped**. The green `End-to-End Tests Success` gate is not evidence those E2E suites executed. Preserve PROMISING/A25 pending complete integration execution and successful backup/restore validation. Prior main integration run 40492780438 failed during GHCR image pulls (rate limiting), not established application failure.

## Next research

1. Follow ripgrep `ignore` and `globset` standalone crate versions and edge-case tests (symlinks, ignore precedence, Unicode).
2. Tauri: reproduce/triage `deepmerge` dependency advisory, review ACL/IPC tests and signed updater verification, then inspect WRY/TAO separately.
3. Immich: find full, non-skipped end-to-end/server integration CI and evaluate backup restoration.
