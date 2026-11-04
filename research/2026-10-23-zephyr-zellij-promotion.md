# Zephyr RTOS and Zellij — promotion evidence (2026-10-23)

## Method and scope
Continued the existing GitHub-first dossiers instead of duplicating research or inventing YouTube-derived findings. Compared candidate names and canonical URLs with all 58 existing catalog entries and the empty candidate queue. Inspected current upstream repository metadata, source-tree organization, README files, root licenses, release metadata, recent commits and GitHub Actions. No local build, device flash, terminal session, browser access, WebAssembly plugin execution, or security testing was performed.

The six seed playlist IDs remain in `sources/youtube_playlists.md`. Searches for two IDs returned no usable results; no transcript finding is asserted.

## Zephyr RTOS — VERIFIED, S / 29
- **Repository:** https://github.com/zephyrproject-rtos/zephyr
- **Earlier detailed dossier:** `research/2026-09-07-zephyr-rtos-embedded-kernel-hardware-test-platform.md`.
- **Source evidence:** `README.rst` describes resource-constrained multi-architecture RTOS support. Root contains `kernel/`, `drivers/`, `subsys/`, `boards/`, `soc/`, `dts/`, `tests/`, `samples/`, `scripts/`, `west.yml` and `LICENSES/`. `west.yml` pins modules to revisions, includes BabbleSim-related repositories, and supports external manifests.
- **Release:** stable `v4.4.2`, published **2026-08-07**, https://github.com/zephyrproject-rtos/zephyr/releases/tag/v4.4.2 . Release notes explicitly include numerous CVEs affecting kernel, Bluetooth, filesystem, HTTP and drivers. The **2026-10-22** main commit `76280bce2a05` marks `v4.5.0-rc3` in source; it is not a confirmed stable GitHub release.
- **Working evidence:** main-branch push on **2026-10-22**: Twister https://github.com/zephyrproject-rtos/zephyr/actions/runs/39835122032 **success**; CodeQL https://github.com/zephyrproject-rtos/zephyr/actions/runs/39835121878 **success**; Documentation Build https://github.com/zephyrproject-rtos/zephyr/actions/runs/39835121990 **success**. These are upstream workflow conclusions, not independently reproduced test results.
- **High-value components:** `scripts/twister` and `scripts/pylib/twister/` (test-plan generation, sharding and reports); Kconfig + devicetree hardware composition; `kernel/` scheduling/memory; `drivers/` APIs; `subsys/` networking/USB/Bluetooth; west/CMake/sysbuild orchestration. Inspect the exact APIs before adapting.
- **Requirements/platforms:** west, SDK/toolchains, CMake/Python host tools, target-specific board configurations; Arm, RISC-V, x86, Xtensa, ARC and other upstream-documented targets.
- **Licensing:** Apache-2.0 project root. `README.license` clarifies REUSE `LICENSES/` is a license corpus, not a declaration that all source is identically licensed. Third-party HALs/modules and file-level SPDX require separate inspection before copying. **No source copied.**
- **Score:** Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5 = **29 (S)**.
- **Limitations:** a passing Twister workflow does not verify every board, driver, firmware image, safety-critical configuration or attack surface. Release security fixes are a reminder to use maintained branches.
- **Recursive leads:** west module manifests; BabbleSim simulated radio/network test harness; MCUboot integration; devicetree code generation; compare driver portability with ESPHome.

## Zellij — VERIFIED, S / 28
- **Repository:** https://github.com/zellij-org/zellij
- **Earlier detailed dossier:** `research/2026-09-09-zellij-terminal-workspace-wasm-plugin-platform.md`.
- **Source evidence:** README documents persistent sessions, layouts, Wasm plugins and a built-in web client. Workspace contains `zellij-client/`, `zellij-server/`, `zellij-utils/`, `zellij-tile/`, `zellij-tile-utils/`, `default-plugins/`, `zellij-integration-tests/`, `xtask/`, `assets/`, and `docs/`. Cargo workspace currently declares Rust **1.95**, workspace **0.46.0** development version and **MIT** license.
- **Release:** latest inspected stable **v0.45.1**, published **2026-08-28**: https://github.com/zellij-org/zellij/releases/tag/v0.45.1 . Do not confuse the 0.46.0 source manifest with a stable release.
- **Working evidence:** main Rust workflow https://github.com/zellij-org/zellij/actions/runs/39811852472 on **2026-10-22** passed **12/12** jobs (Linux/macOS/Windows build and test, integration, no-web, desktop smoke, formatting and assets). Main end-to-end workflow https://github.com/zellij-org/zellij/actions/runs/39811852673 passed **1/1** job. Upstream CI, not local testing.
- **Recent maintenance:** 2026-10-22 commits `c7c4ce42b866` (session rename in session mode) and `a28f3ca9c273` (desktop setup and flaky-test fixes); 2026-10-20 terminal grid memory optimizations.
- **High-value components:** Rust client/server IPC and session lifecycle, declarative layout parsing, Wasm plugin SDK and bundled plugins, SSH end-to-end testing, `web_server_capability` browser-client architecture.
- **Requirements/platforms:** prebuilt binaries or Rust/Cargo build; Linux/macOS/Windows CI; browser access when feature enabled.
- **Licensing:** MIT at `LICENSE.md` and workspace manifest. Review dependencies/assets independently. **No source copied.**
- **Score:** Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4 = **28 (S)**.
- **Limitations:** a terminal web server and shared sessions expose privileged command execution if improperly configured. No browser-auth, plugin capability, remote-session or release reproducibility audit was performed. Workflow currently references some mutable action tags.
- **Recursive leads:** WebAssembly plugin host permission model; SSH collaboration security; Rust terminal rendering; compare Nushell integration and tmux session isolation.

## Steward checks
Promotion only after canonical URL/name duplicate checks; preserve the 0–30 scoring model and existing tiers. Human-readable and machine-readable entries updated together, without copying third-party code. Verify exact file paths and licenses before any future implementation extraction.
