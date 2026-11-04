# OpenROAD and ZMK Firmware — GitHub Gold research, 2026-10-24

## Scope and provenance
GitHub-first discovery in semiconductor electronic design automation and embedded programmable input. Existing research branch held 78 canonical entries; candidate queue was empty. Neither new canonical URL nor project name appeared in the existing catalog. Exact-ID web searches for three saved YouTube playlist identifiers yielded no usable indexed results; previous research notes document the other three IDs as inaccessible. No transcript-derived claims or third-party code imports.

## OpenROAD — VERIFIED (upstream), S / 27
**Repository:** https://github.com/The-OpenROAD-Project/OpenROAD

**Score:** Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.

Inspected upstream README, BSD-3-Clause LICENSE, `CMakeLists.txt`, `docs/user/Bazel.md`, `src/README.md`, `src/odb/README.md`, `src/drt/README.md`, `src/rsz/README.md`, source and test directory trees, workflows, recent commits, and GitHub releases. OpenDB provides C++ LEF/DEF and binary database interfaces (`src/odb/`). TritonRoute (`src/drt/`) supplies pin access, detailed routing and DRC. Gate resizing/timing repair (`src/rsz/`), placement (`src/gpl/`), clock tree (`src/cts/`) and power/global routing (`src/pdn/`, `src/grt/`) are reusable architectural leads. `test/` contains AES/GCD example designs and regression fixtures; the Tcl API is broader than the limited Python interface.

**Key maintenance finding:** `CMakeLists.txt` and `docs/user/Bazel.md` explicitly say CMake is deprecated and scheduled for removal **2026-11-01**; **Bazel is the supported build system**. Use `bazelisk test src/...` for focused regression and `bazelisk test ...` for wider integration, as upstream documents. GitHub releases returned only the historical 2020 `v0.9.0-beta` object; do not claim a current stable tagged release.

**Upstream evidence:** 2026-10-25 UTC master commits `fb59e23b` and `dca44bea` show ongoing work. [macOS build 40145237901](https://github.com/The-OpenROAD-Project/OpenROAD/actions/runs/40145237901) passed (1/1 job); [CodeQL 40145237910](https://github.com/The-OpenROAD-Project/OpenROAD/actions/runs/40145237910) passed (3/3); [expected-output freshness 40145237885](https://github.com/The-OpenROAD-Project/OpenROAD/actions/runs/40145237885) passed (1/1); [ODB generator check 40147387817](https://github.com/The-OpenROAD-Project/OpenROAD/actions/runs/40147387817) passed on master. These are specific upstream checks, **not proof of an independently executed RTL-to-GDSII flow**.

**Licensing and limitations:** BSD-3-Clause root; third-party subtrees/PDKs require separate checks. Build and toolchain resources can be substantial; Python API incomplete. No independent build, chip layout, PDK verification, silicon fabrication, or security audit. Next: investigate `The-OpenROAD-Project/OpenROAD-flow-scripts`, OpenDB API coverage, detailed-route determinism, and post-CMake migration.

## ZMK Firmware — VERIFIED (upstream), S / 26
**Repository:** https://github.com/zmkfirmware/zmk

**Score:** Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 3.

Inspected upstream README, MIT LICENSE, CHANGELOG, `app/west.yml`, `app/src/behaviors/`, `app/src/split/`, `app/src/pointing/`, `app/src/studio/`, `app/tests/` and test/BLE/build workflows. Strong reusable components include key-behavior state machines (hold-tap, sticky keys, macros, tap dance), USB/BLE HID transport, wired/BLE split-device support, pointing input processors, and ZMK Studio RPC/GATT/UART transport. These are useful for customizable input devices, but **accessibility performance has not been user-tested**.

**Dependency finding:** `app/west.yml` pins `zmkfirmware/zephyr` at `v4.1.0+zmk-fixes`, rather than current upstream Zephyr; track fork security updates and compatibility separately. Latest confirmed stable GitHub release `v0.3.0` was published **2025-08-01**. Main commits through **2026-10-09** include a split-queue deadlock fix and RP2040 board work.

**Upstream evidence:** [Tests 40030685287](https://github.com/zmkfirmware/zmk/actions/runs/40030685287) passed 25/25 jobs on 2026-10-23; [BLE tests 40030685316](https://github.com/zmkfirmware/zmk/actions/runs/40030685316) passed 4/4; [PR build 40030685289](https://github.com/zmkfirmware/zmk/actions/runs/40030685289) had 14 passes and 2 skips. [Scheduled main build 39901202810](https://github.com/zmkfirmware/zmk/actions/runs/39901202810) passed 38 jobs with 3 skips on 2026-10-23. **Counterevidence:** [scheduled main build 40062805918](https://github.com/zmkfirmware/zmk/actions/runs/40062805918) failed on 2026-10-24 because the `proton_c` matrix job failed; other board builds passed. Do not represent the latest matrix as green.

**Licensing and limitations:** MIT root; Zephyr fork, LVGL, HALs and other west dependencies separately licensed. No firmware was built, flashed or paired by GitHub Gold. Next: investigate `proton_c` build failure, split/BLE reliability, Studio RPC authorization, `zmkfirmware/zmk-studio`, and board-specific accessibility testing.

## Maintenance and follow-up
Existing Zephyr RTOS entry now cross-links ZMK and notes that ZMK pins a separate Zephyr fork. Catalog score/tier thresholds unchanged; no duplicates and no source code copied. Prior OpenSCAD release-age caveat and Rizin Capstone CI failures remain in their records. Next discovery should rotate to low-resource scientific/field tools or hardware design verification, while following these component-level leads.

**Execution boundary:** All CI results cited are upstream GitHub Actions. No independent builds, tests, hardware operations, or security audits were performed in this batch.
