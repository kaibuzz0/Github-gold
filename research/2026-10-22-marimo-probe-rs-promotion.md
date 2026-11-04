# marimo and probe-rs — evidence-backed catalog promotion

- **Research date:** 2026-10-22 (America/Chicago)
- **Discovery:** GitHub-first and prior research dossiers. All six seed YouTube playlist pages were retried and returned throttled/disabled responses; no transcript-derived claims.
- **Scope:** Two existing research leads promoted atomically to canonical catalog; no third-party implementation code copied.

## marimo — reactive Python notebooks and reusable execution graph

- **Upstream:** https://github.com/marimo-team/marimo
- **Evidence / Gold:** VERIFIED (upstream) / S / **29** = Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it provides:** Reactive, pure-Python notebooks and deployable data apps. Dependency-aware cell execution, SQL integration, widgets, script export and browser/Pyodide execution are documented in README and backed by source directories.
- **Exact components:** [dataflow](https://github.com/marimo-team/marimo/tree/main/marimo/_runtime/dataflow), [executor](https://github.com/marimo-team/marimo/tree/main/marimo/_runtime/executor), [SQL](https://github.com/marimo-team/marimo/tree/main/marimo/_sql), [plugins](https://github.com/marimo-team/marimo/tree/main/marimo/_plugins), [export](https://github.com/marimo-team/marimo/tree/main/marimo/_export), [Pyodide](https://github.com/marimo-team/marimo/tree/main/marimo/_pyodide), [MCP](https://github.com/marimo-team/marimo/tree/main/marimo/_mcp).
- **Primary sources:** [README](https://github.com/marimo-team/marimo/blob/main/README.md), [pyproject.toml](https://github.com/marimo-team/marimo/blob/main/pyproject.toml), [Apache-2.0 license](https://github.com/marimo-team/marimo/blob/main/LICENSE), [release 0.25.2](https://github.com/marimo-team/marimo/releases/tag/0.25.2) published **2026-10-19**.
- **Working evidence:** 2026-10-22 main [backend workflow 39859957455](https://github.com/marimo-team/marimo/actions/runs/39859957455) passed 18 jobs (one docs job skipped), including Python 3.10–3.15 and Linux/Windows/macOS; [frontend 39859957465](https://github.com/marimo-team/marimo/actions/runs/39859957465) passed 4/4; [Playwright 39859957692](https://github.com/marimo-team/marimo/actions/runs/39859957692) passed 2/2. These are upstream executions, not ours.
- **Runtime:** Python >=3.10, `pip install marimo`; browser Pyodide and SQL require environment-dependent packages. The 0.25.2 manifest excludes the native `loro` dependency on Python 3.15 and Android/Emscripten, so some collaborative features may differ.
- **License and trust:** Apache-2.0 project, third-party notices/assets to be reviewed for copying. Interactive notebooks execute Python; untrusted notebooks and hosted execution require explicit isolation.
- **Related ecosystem:** marimo-lsp, vscode-marimo, DuckDB, uv and Loro.
- **Not performed:** install, notebook execution, browser test, SQL isolation test, security audit or independent CI replay.

## probe-rs — embedded debug transports and hardware validation

- **Upstream:** https://github.com/probe-rs/probe-rs
- **Evidence / Gold:** VERIFIED (upstream) / S / **29** = Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it provides:** Modular Rust embedded debugger, SWD/JTAG transports, flash loader, target definitions, GDB/DAP adapters, remote RPC and Linux GPIO/spidev SWD.
- **Exact components:** [probe transports](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/probe), [architectures](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/architecture), [flashing](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/flashing), [target definitions](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-target), [DAP](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-debug), [RPC](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-rpc), [Linux probes](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-linux), [smoke-tester](https://github.com/probe-rs/probe-rs/tree/master/smoke-tester).
- **Primary sources:** [README](https://github.com/probe-rs/probe-rs/blob/master/README.md), [Cargo.toml](https://github.com/probe-rs/probe-rs/blob/master/Cargo.toml), [MIT license](https://github.com/probe-rs/probe-rs/blob/master/LICENSE-MIT), [Apache license](https://github.com/probe-rs/probe-rs/blob/master/LICENSE-APACHE), [v0.32.0](https://github.com/probe-rs/probe-rs/releases/tag/v0.32.0) published **2026-07-22**.
- **Working evidence:** 2026-10-22 master [CI 39849611123](https://github.com/probe-rs/probe-rs/actions/runs/39849611123) passed **12/12** including cross-platform checks and Linux/Windows test suites; [hardware smoke test 39849610977](https://github.com/probe-rs/probe-rs/actions/runs/39849610977) passed **5/5** including two self-hosted hardware test jobs and embedded-test. These are upstream results, not our tests.
- **Runtime:** Rust 1.95 minimum; CLI binaries on major desktop OSes; hardware probe and MCU generally needed. Linux GPIO/spidev SWD is host- and wiring-specific.
- **License and trust:** Workspace MIT OR Apache-2.0; external CMSIS packs, chip metadata and flash algorithms require separate provenance review. Flashing/erase can destroy device data; remote RPC must be restricted.
- **Related ecosystem:** probe-rs/vscode, probe-rs/embedded-test, pyOCD, esptool, MCUboot.
- **Not performed:** build, device attach, flash, HIL replay, wiring test, binary integrity verification or RPC audit.

## Catalog consistency and next work

- Promoted only after checking canonical catalog for duplicate repository URLs and reviewing prior research.
- Preserve 30-point six-factor scoring and existing tier boundaries.
- Next: independent marimo reactive-graph/sandbox behavior checks; Python 3.15 Loro feature parity; probe-rs external pack license inventory, RPC exposure, and board-specific HIL comparison with pyOCD.
- **No third-party implementation code copied.**
