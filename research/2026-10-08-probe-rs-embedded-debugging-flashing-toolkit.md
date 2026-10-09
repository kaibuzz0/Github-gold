# probe-rs — modular embedded debugging, flashing, and probe transport toolkit

- **Upstream:** https://github.com/probe-rs/probe-rs
- **Maintainer:** probe-rs organization and contributors
- **Research date:** 2026-10-08
- **Category:** Embedded debugging / firmware flashing / SWD-JTAG / Rust libraries / developer tooling / hardware-in-the-loop
- **Evidence:** VERIFIED — concrete upstream implementation, releases, CI, and hardware-test infrastructure; no independent hardware execution
- **Provisional Gold ranking:** **S / 28 of 30** (Utility 5; Working Evidence 4; Reusability 5; Novelty 4; Documentation 5; Maintenance 5)
- **License:** `MIT OR Apache-2.0` at workspace level; per-crate and external device packs/flash algorithms require review
- **Discovery:** Independent GitHub-first search; no YouTube transcript attribution. Attempts to fetch seed playlists `PLMI6SBmd587c` and `PLfidXW0BixTc` on 2026-10-08 were throttled; no transcript claims were made.

## What it does and why it matters

probe-rs is a Rust workspace for interacting with embedded debug probes and MCU targets. It supports SWD/JTAG and Arm, RISC-V, and Xtensa targets; debugger transports include CMSIS-DAP, ST-Link, J-Link, FTDI, WLink, Black Magic and others. The library and CLI support memory inspection, halt/step/breakpoints, flashing ELF/BIN/IHEX with target flash algorithms, RTT/defmt logging, GDB and editor Debug Adapter Protocol (DAP) integration. Actual capabilities vary by probe, MCU and architecture.

The key value is **component-level reuse**, not only the end-user CLI: probe transports, target metadata, flash programming, debug adapters, Linux GPIO/SPI SWD adapters, remote RPC, and a dedicated hardware smoke-test harness can be researched and adopted separately.

## Specific reusable components

| Component | Upstream location | Reuse value |
| --- | --- | --- |
| Core library, sessions and memory APIs | [probe-rs/src](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src) | Embeddable debug sessions, core control, memory I/O |
| Debug-probe backends | [probe-rs/src/probe](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/probe) | CMSIS-DAP, ST-Link, J-Link, FTDI, WLink, Black Magic, GPIO/SPI and other transports |
| Target architecture support | [probe-rs/src/architecture](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/architecture) | Arm, RISC-V, Xtensa debug abstractions |
| Flash algorithm/loader | [probe-rs/src/flashing](https://github.com/probe-rs/probe-rs/tree/master/probe-rs/src/flashing) | Erase/program/verify orchestration, flash memory regions and progress |
| Target definitions and generators | [probe-rs-target](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-target), [target-gen](https://github.com/probe-rs/probe-rs/tree/master/target-gen) | Chip metadata, memory maps, flash algorithms, target generation |
| CLI and Cargo tools | [probe-rs-tools/src/bin](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-tools/src/bin) | `probe-rs`, `cargo-flash`, `cargo-embed`; prefer `probe-rs run` for new projects per README |
| DAP debugging | [probe-rs-debug](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-debug) | Editor-facing Debug Adapter Protocol implementation |
| Remote-control interfaces | [probe-rs-rpc](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-rpc), [probe-rs-rpc-client](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-rpc-client) | Client/server debug operations, including memory, flash, core and RTT endpoints |
| Linux software SWD probes | [probe-rs-linux](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-linux) | GPIO character-device bit-banging and spidev SWD on Raspberry Pi/Linux |
| Hardware smoke-test harness | [smoke-tester](https://github.com/probe-rs/probe-rs/tree/master/smoke-tester) | Declarative board/probe inventory and automated target validation |
| Espressif and Zephyr integrations | [probe-rs-espressif](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-espressif), [probe-rs-zephyr](https://github.com/probe-rs/probe-rs/tree/master/probe-rs-zephyr) | Platform-specific target support and integrations |

## Build, runtime, and platform requirements

The [workspace Cargo.toml](https://github.com/probe-rs/probe-rs/blob/master/Cargo.toml) pins edition 2024, workspace version `0.32.0`, and **Rust 1.95 minimum**. Upstream distributes CLI assets for x86_64 Linux/Windows/macOS and aarch64 Linux/macOS in the [v0.32.0 release](https://github.com/probe-rs/probe-rs/releases/tag/v0.32.0). Hardware debugging generally needs a supported physical debug probe and target MCU. The Linux-only `probe-rs-linux` backend can use Linux GPIO character devices or spidev SWD instead of a dedicated USB debug probe, but requires deliberate wiring, appropriate electrical levels, device permissions, and target compatibility. Its README documents a Raspberry Pi Zero W to STM32F439ZI test; that is **an upstream claim**, not an independently repeated experiment.

## Primary-source evidence and maintenance

1. [README](https://github.com/probe-rs/probe-rs/blob/master/README.md): supported transports, architectures, CLI, GDB/DAP, usage examples, and a warning that `cargo-embed` is expected to be phased out in favor of `probe-rs run` for new projects.
2. [Cargo workspace](https://github.com/probe-rs/probe-rs/blob/master/Cargo.toml): explicit modular crate list, Rust 1.95 minimum, `MIT OR Apache-2.0` licensing; root [MIT](https://github.com/probe-rs/probe-rs/blob/master/LICENSE-MIT) and [Apache-2.0](https://github.com/probe-rs/probe-rs/blob/master/LICENSE-APACHE) files.
3. [Release v0.32.0](https://github.com/probe-rs/probe-rs/releases/tag/v0.32.0): published **2026-07-22**, includes tagged release assets and SHA256 sidecars for several platforms. Asset presence is not independent verification of installer safety or reproducibility.
4. [CI workflow](https://github.com/probe-rs/probe-rs/blob/master/.github/workflows/ci.yml): `cargo check` across Linux/Windows/macOS; `cargo nextest run --all-features --locked --profile ci-unit` on Linux/Windows; formatting, Clippy with `-D warnings`, `cargo deny`, docs, minimum-Rust checks, and dependency checks. Workflow definition is evidence of intended checks, **not proof of current successful runs**.
5. [Hardware smoke-test workflow](https://github.com/probe-rs/probe-rs/blob/master/.github/workflows/smoketest.yml): builds ARM64 smoke-test archives and runs them on two named self-hosted ARM64 hardware runners; an embedded-test job uses a configured runner. Hardware availability and per-run results were not independently checked.
6. [Smoke tester README](https://github.com/probe-rs/probe-rs/blob/master/smoke-tester/README.md): chip and probe selectors, TOML device-under-test definitions, optional ELF flash-test binary.
7. [Linux probe driver README](https://github.com/probe-rs/probe-rs/blob/master/probe-rs-linux/README.md): concrete `linuxgpiod` and `linuxspidevswd` adapters, synthetic probe selectors, Raspberry Pi wiring, cross-build commands, and remote server usage. For safety `probe-rs list` only auto-exposes explicitly named `/dev/spidev_swd*` links, not arbitrary spidev devices.
8. [Recent commits](https://github.com/probe-rs/probe-rs/commits/master/) inspected **2026-10-08**: `ceec5ad` makes CMSIS-DAP v1 optionally removable from the binary; `81855b4` adds GD32H737VG support; `b94a85c` reports complete JTAG-chain info; `04f7ef1` rebases an ICDI probe backend. Active source work is visible after the last release.
9. [Open issues](https://github.com/probe-rs/probe-rs/issues) on **2026-10-08** include a Windows 11/STLINK-V3MINIE slow-flashing report (#4418) and an STM32H7RS overlapping flash-algorithm definition (#4422); these are reports, not independently reproduced defects.

## Caveats and boundaries

- **Potentially destructive operations:** flashing, erase, option bytes and chip-specific debug commands can brick hardware or erase data. Use only on devices under user control, with backups and board-specific voltage/wiring precautions.
- **Target coverage is uneven:** transport support, debug trace, multicore behavior and flash algorithms vary. Do not infer complete target support from a family name.
- **Remote RPC exposes powerful operations:** authenticate, restrict interfaces to trusted networks, protect tokens and threat-model memory/flash/core operations. A documented token option is not a security audit.
- **Third-party pack licensing:** chip descriptions, CMSIS-Packs, flash algorithms, SDKs and external data may have terms different from the workspace's MIT/Apache-2.0 code. Review provenance before extracting any artifacts.
- **No upstream source was copied into GitHub Gold.**

## Verification boundary

**Performed:** Read primary-source README, workspace manifest, root licenses, release metadata, source tree layout, CI and hardware smoke-test workflow, Linux adapter documentation, recent commits and issue metadata.

**Not performed:** compiling, running tests, flashing, connecting to a physical probe, validating SWD electrical operation, executing HIL smoke tests, measuring flashing speed, reproducing issue reports, verifying binary signatures or auditing remote RPC security. `VERIFIED` here means strong upstream implementation and test/release infrastructure evidence, **not independent hardware certification**.

## Strong next investigations

1. Independently run unit tests and the smoke-tester on a known supported probe/MCU pair; record exact versions and board configuration.
2. Validate the Linux GPIO/spidev SWD plugin on Raspberry Pi hardware; measure transfer speed and errors at increasing clocks and during disconnects.
3. Map which target definitions and flash algorithms originate in external packs and whether each can legally be reused.
4. Test the remote RPC auth, token handling and exposure of erase/flash/memory operations in a private lab.
5. Compare probe-rs's DAP/GDB implementation and target support against OpenOCD and pyOCD; look for reusable interoperability tests.
6. Verify whether the October 8 JTAG-chain and ICDI changes are covered by hardware regression tests.

## Catalog hygiene

The GitHub Gold draft research branch contained no `probe-rs` dossier in its 2026-10-08 file listing, and GitHub Gold code search returned no `probe-rs` results. This is a **dossier-first research addition** intended for the existing draft PR #7 branch. Canonical `MASTER_LIST.md` and `catalog/tools.json` remain unchanged until a coordinated promotion that preserves schema and human/machine consistency.