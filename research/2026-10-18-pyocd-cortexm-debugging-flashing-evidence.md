# pyOCD — Cortex-M debugging, flashing, and probe integrations
**Research checked:** 2026-10-18  
**Upstream:** https://github.com/pyocd/pyOCD  
**Evidence:** VERIFIED from upstream source/release/test configuration, **not independently executed**.  
**Provisional Gold:** S / 28 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5).

## Why it matters
pyOCD provides a Python CLI and library for flashing and debugging Arm Cortex-M devices using CMSIS-DAP, ST-Link, J-Link, and other supported probes. It includes GDB remote debugging, CMSIS Device Family Pack support, RTOS-aware inspection, SWV trace capture, and automation APIs.

## Reusable upstream components
- [CMSIS-DAP probe](https://github.com/pyocd/pyOCD/blob/main/pyocd/probe/cmsis_dap_probe.py)
- [ST-Link probe](https://github.com/pyocd/pyOCD/blob/main/pyocd/probe/stlink_probe.py)
- [J-Link probe](https://github.com/pyocd/pyOCD/blob/main/pyocd/probe/jlink_probe.py)
- [GDB server](https://github.com/pyocd/pyOCD/blob/main/pyocd/gdbserver/gdbserver.py)
- [Flash loader](https://github.com/pyocd/pyOCD/blob/main/pyocd/flash/loader.py)
- [CMSIS packs](https://github.com/pyocd/pyOCD/tree/main/pyocd/target/pack)
- [RTOS support](https://github.com/pyocd/pyOCD/tree/main/pyocd/rtos)
- [SWV trace](https://github.com/pyocd/pyOCD/blob/main/pyocd/trace/swv.py)
- [Unit tests](https://github.com/pyocd/pyOCD/tree/main/test/unit)

## Evidence and maintenance
The official [v0.45.1 release](https://github.com/pyocd/pyOCD/releases/tag/v0.45.1) was published **2026-07-21**. The README documents Python 3.9+, Linux/macOS/Windows/FreeBSD, and supported probes. The [basic test workflow](https://github.com/pyocd/pyOCD/blob/main/.github/workflows/basic_test.yaml) declares flake8, pytest, module imports, wheel/sdist builds, and a three-OS Python 3.9–3.14 matrix. This is upstream CI configuration evidence; no independent execution or full historical CI-success audit was performed.

## Licensing
Root [LICENSE](https://github.com/pyocd/pyOCD/blob/main/LICENSE) is Apache-2.0. Documentation has separate CC BY 4.0 terms as described in the existing research package; review vendor CMSIS packs, dependencies, and probe drivers separately before redistribution. No implementation code was copied.

## Safety / limitations
- The upstream [security guide](https://github.com/pyocd/pyOCD/blob/main/docs/security.md) says automatic unlocking of some protected targets can **mass-erase memory**; the default is true for many commands, but Commander differs.
- The upstream [remote probe guide](https://github.com/pyocd/pyOCD/blob/main/docs/remote_probe_access.md) says remote network clients are disallowed by default. Explicitly allowing them without network controls exposes device-debug privileges.
- The upstream README describes the tool as **beta quality** and warns of future 1.0 API changes.
- Device packs and firmware-flash algorithms may carry independent licensing terms.

## Related work / next tests
Compare with [probe-rs](https://github.com/probe-rs/probe-rs) (existing `research/2026-10-08-probe-rs-embedded-debugging-flashing-toolkit.md`), and DAPLink. Next: safe dry-run probe discovery, API import checks, test suite execution, supported-device matrix, and an authorized spare-board flash test with backups. No hardware flashing, installation, build, benchmark, or security audit was performed in this review.

**Discovery provenance:** GitHub-first; prior October 16–17 research reviewed and updated 2026-10-18.
