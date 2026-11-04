# GitHub-first research — mise and hyperfine (2026-10-30 UTC)

## Scope and provenance
Inspected the canonical upstream README, manifest, licenses, source modules, GitHub Actions workflow definitions, tagged version manifests and dated upstream workflow run pages. No code copied, built, executed, installed or benchmarked by GitHub Gold. Scores describe upstream evidence, not an independent certification. Checked the existing 145-entry catalog and master list for both canonical URLs before adding them.

YouTube playlist `PLMI6SBmd587c` direct access was throttled on 2026-10-30; no video or transcript evidence was obtained. These are **GitHub-first** discoveries.

## 1. mise — VERIFIED (upstream), S27
- **Repository:** https://github.com/jdx/mise — author Jeff Dickey / jdx.
- **Function:** Rust CLI for per-project tool versions, environment variables, shell activation, task orchestration, machine bootstrap and lockfiles. See https://github.com/jdx/mise/blob/main/README.md and https://github.com/jdx/mise/blob/main/Cargo.toml.
- **Score:** utility 5, working evidence 4, reusability 5, novelty 3, documentation 5, maintenance 5 = **27/30**.
- **Source map:** `src/cli/` (install, exec, lock, trust, run, bootstrap), `crates/mise-config/` (configuration), `crates/mise-dotenv/` (environment parsing), `crates/mise-sigstore/` (signature/provenance helpers), `crates/mise-lsp/` (configuration LSP), `crates/mise-bootstrap/`, `crates/mise-shim/`, `crates/mise-cache-core/`. These are inspected source/manifests, not promises of stable library APIs; root manifest explicitly calls its lib non-public.
- **Release:** tag `v2026.10.24` resolves to a Cargo manifest declaring `2026.10.24`; CHANGELOG dates it **2026-10-30**. Current manifest declares Rust **1.95** minimum. Upstream offers macOS/Linux and Windows installation paths.
- **Working evidence:** https://github.com/jdx/mise/actions/runs/40394685264 — **2026-10-26 successful upstream release-branch test workflow** with Ubuntu/Windows builds, macOS/Windows unit and E2E, Linux E2E, lint and gating. This run predates `v2026.10.24`; no passing workflow on that exact tag was established.
- **License:** root MIT, https://github.com/jdx/mise/blob/main/LICENSE. Dependencies, backends, and downloaded tools have independent terms.
- **Security:** project configs, tasks, hooks, environment secrets and downloaded binaries are trust boundaries. The 2026.10.19 upstream release documents trust, artifact provenance and extraction hardening. Treat upstream claims as claims; do not assume every backend or tool has equivalent verification. Require deliberate `mise trust`, lock/pin versions and check download provenance.
- **Related:** https://github.com/jdx/mise-action (official companion), https://github.com/astral-sh/uv (complementary Python tooling), https://github.com/sharkdp/hyperfine (used in mise's v2026.10.11 release performance comparison).
- **Follow-up:** verify the exact v2026.10.24 CI matrix, try isolated installs with untrusted project config, check Termux compatibility and supply-chain enforcement by backend.

## 2. hyperfine — VERIFIED (upstream), S27
- **Repository:** https://github.com/sharkdp/hyperfine — author David Peter / sharkdp.
- **Function:** Rust CLI for statistical command benchmarking with warmups, setup/prepare hooks, outlier handling, parameter scans, and machine-readable exports. README: https://github.com/sharkdp/hyperfine/blob/master/README.md.
- **Score:** utility 5, working evidence 5, reusability 4, novelty 3, documentation 5, maintenance 5 = **27/30**.
- **Source map:** `src/benchmark/scheduler.rs` orchestrates raw/shell/mock executors and incremental exports; `src/benchmark/`, `src/timer/`, `src/metric/`, `src/outlier_detection/`, `src/parameter/`, `src/export/` and `src/shell_syntax/` provide reusable patterns. Source files are linked, not copied.
- **Release boundary:** latest confirmed published stable tag `v1.20.0` from **2025-11-18**, https://github.com/sharkdp/hyperfine/releases/tag/v1.20.0. Current master `Cargo.toml` declares **2.0.0** with Rust **1.97** minimum, but no released v2 tag established. Do not conflate a development manifest or CI artifacts with a published stable release.
- **Working evidence:** https://github.com/sharkdp/hyperfine/actions/runs/38224324422 — successful **2026-10-12** push workflow on master SHA `c516152`, 13 build matrix legs plus formatting and minimum Rust tests. This is upstream evidence, not an independent timing experiment.
- **License:** dual MIT OR Apache-2.0 in root manifest; both `LICENSE-MIT` and `LICENSE-APACHE` inspected. Dependencies have separate licenses.
- **Caveats:** runs arbitrary user-specified commands (including setup/cleanup); treat commands as executable code. Benchmark comparability depends on warmup, caching, CPU/thermal state, I/O, shell overhead, scheduling and environment; reports are not universal performance claims. CLI and JSON formats may change in v2.
- **Related:** mise release notes v2026.10.11 contain a hyperfine-based performance comparison; this is a documentation relationship, **not** a direct dependency.
- **Follow-up:** independently benchmark a deterministic fixture with pinned stable version, verify JSON export schema, assess shell-quoting and process-exit behavior, and test ARM/Termux where feasible.

## Existing-entry maintenance: MarkItDown
On 2026-10-30, checked https://github.com/microsoft/markitdown/pull/2296 and https://github.com/microsoft/markitdown/pull/2050. Both remained **open and unmerged**; no mitigation was treated as shipped. Its existing **PROMISING/A25** classification and ZIP decompression resource-exhaustion caveat remain unchanged. This check does not prove no other mitigation exists; no new current-main ZIP runtime test was performed.

## Research limitations and next leads
No independent build, command execution, performance benchmark, malware analysis or security audit was performed. For mise, verify backend-specific artifact integrity and untrusted-config behavior. For hyperfine, verify v2 release transition and reproducible timing/exit semantics. Broaden the next batch into non-developer areas (offline radio, embedded, mapping, accessibility, scientific tools) to avoid category concentration.
