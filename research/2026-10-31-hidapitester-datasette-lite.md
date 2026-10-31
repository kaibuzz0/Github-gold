# GitHub Gold research — hidapitester, Datasette Lite and Datasette dependency correction
Date: 2026-10-31 (UTC)
Discovery: GitHub-first recursion from cataloged HIDAPI, Datasette and Pyodide. Exact-ID searches of YouTube seeds `PLMI6SBmd587c` and `PLfidXW0BixTc` returned no indexed metadata/transcripts. No video content was accessed or attributed.

## hidapitester — VERIFIED upstream, S27 (5/4/5/4/5/4)
Repository: https://github.com/todbot/hidapitester
Primary evidence: [README](https://github.com/todbot/hidapitester/blob/main/README.md), [C CLI](https://github.com/todbot/hidapitester/blob/main/hidapitester.c), [CMake](https://github.com/todbot/hidapitester/blob/main/CMakeLists.txt), [Makefile](https://github.com/todbot/hidapitester/blob/main/Makefile), [GPL-3.0 license](https://github.com/todbot/hidapitester/blob/main/LICENSE), [v0.7 release](https://github.com/todbot/hidapitester/releases/tag/v0.7) (2026-09-26).

Source-specific Gold: HID device enumeration/filtering, report descriptor inspection, input/output/feature report commands, JSON listing, portable C CLI and dedicated [no-hardware](https://github.com/todbot/hidapitester/blob/main/tests/test_nohardware.sh) and [hardware-in-loop](https://github.com/todbot/hidapitester/blob/main/tests/test_hardware.sh) test scripts. Test firmware includes `test_hardware/hidtest_tinyusb/` for RP2040/ESP32/SAMD-class boards. CMake `FetchContent` pins `libusb/hidapi` at `hidapi-0.15.0` (actual source dependency).

Upstream evidence: 2026-09-26 [Linux](https://github.com/todbot/hidapitester/actions/runs/36269273917), [macOS](https://github.com/todbot/hidapitester/actions/runs/36269273951), [Windows](https://github.com/todbot/hidapitester/actions/runs/36269273896), [Raspberry Pi](https://github.com/todbot/hidapitester/actions/runs/36269273927) CI runs passed. Inspected Linux/macOS job steps: Make/CMake builds and `--version`/`--list` commands passed; macOS signing/notarization steps passed. **These workflows do not establish hardware I/O or execution of the separate `make test` and `make test-hw` targets.** v0.7 has Linux x86_64/aarch64, macOS universal and Windows x86_64 ZIPs.

License: GPL-3.0 for the CLI. HIDAPI permits separate licensing choices; inspect backends and test firmware independently before redistribution. No third-party code copied.
Risk: feature/output reports can change a device's state; use on owned/authorized hardware. OS permission differences and report-length semantics require real-device testing.
Follow-up: test no-hardware script against v0.7, flash approved TinyUSB test board and run all report modes; verify report queue behavior against HIDAPI issue/PR status; inspect Windows/macOS signing provenance.

## Datasette Lite — PROMISING, A24 (5/3/5/4/4/3)
Repository: https://github.com/simonw/datasette-lite
Primary evidence: [README](https://github.com/simonw/datasette-lite/blob/main/README.md), [webworker.js](https://github.com/simonw/datasette-lite/blob/main/webworker.js), [index.html](https://github.com/simonw/datasette-lite/blob/main/index.html), [Playwright tests](https://github.com/simonw/datasette-lite/blob/main/tests/test_datasette_lite.py), [CI workflow](https://github.com/simonw/datasette-lite/blob/main/.github/workflows/test.yml), [Apache-2.0 LICENSE](https://github.com/simonw/datasette-lite/blob/main/LICENSE).

Source-specific Gold: browser Web Worker bootstraps Pyodide `v0.27.2`, loads Datasette and SQLite, uses Datasette ASGI test client to service browser navigation, supports multiple databases with duplicate-name disambiguation, CSV/JSON/JSONL/Parquet URL import, SQL initialization, metadata, and optional Python plugin installation.

Upstream evidence: last main commit `779b2d4` (2026-08-09). [Main Playwright Test](https://github.com/simonw/datasette-lite/actions/runs/31341071528) succeeded (one job, including pytest), [Pages deployment](https://github.com/simonw/datasette-lite/actions/runs/31341070505) succeeded. No tagged GitHub releases returned. 2026-10-20 PR test run `39417619053` was `action_required` and is not a failed main build. No independent browser execution or mobile/offline verification.

**Dependency drift and release-line correction:** Worker installs `sqlite-utils==3.28` for structured-data import, while Datasette's **current-main** [pyproject.toml](https://github.com/simonw/datasette/blob/main/pyproject.toml) declares `sqlite-utils>=4.0` and Python >=3.11. Crucially, the **stable 0.65.5** [setup.py](https://github.com/simonw/datasette/blob/0.65.5/setup.py) declares Python >=3.10 and does **not** declare sqlite-utils as a dependency. Prior GitHub Gold entries incorrectly generalized current-main requirements to stable 0.65.5. Both existing entries have been corrected. Compatibility of `?ref=pre` or newer Datasette versions with Lite's pinned import package remains untested, not proven broken.

Security and resource limits: `?install=` installs arbitrary Python packages; `?sql=` fetches and executes SQL; remote data and plugins may be untrusted. Default runtime requires CDN, package and dataset network access; a static site is not inherently offline. Large imports can exhaust browser memory. No code copied.
Follow-up: run pinned stable vs `?ref=pre` in Playwright, exercise CSV/JSON/Parquet import and plugin installation, measure memory and mobile behavior, test controlled offline caching and trust boundaries, pin dependencies if justified.

## Stewardship and verification scope
Added two canonical entries to `catalog/tools.json` and `MASTER_LIST.md`, cross-linked HIDAPI and Datasette, and corrected Datasette/sqlite-utils stable-versus-main dependency descriptions. All six scoring factors recorded; no third-party implementation copied. GitHub Gold did **not** build, install, flash, execute or security-test either candidate. The GitHub Actions results cited above are upstream evidence only.
