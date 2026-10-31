# GitHub Gold research: HIDAPI and Datasette

Date: 2026-10-31 UTC. GitHub-first source and CI review. No upstream code copied, installed, built, executed, flashed or independently audited.

## 1. HIDAPI — VERIFIED (upstream) / S27

- **Repository:** https://github.com/libusb/hidapi; originated with Alan Ott. Published stable 0.15.0 (2025-05-18), while master `hidapi/hidapi.h` declares 0.16.0; do not treat that header version as a released tag.
- **Source inspected:** `README.md`, `BUILD.md`, `LICENSE.txt`, `LICENSE-bsd.txt`, `hidapi/hidapi.h`, `libusb/hid.c`, root source/test tree. Backend sources include `linux/hid.c`, `windows/hid.c`, `mac/hid.c`; `hidtest/test.c` is an example and `udev/69-hid.rules` documents non-root access. `libusb/hid.c` includes `libusb.h`, establishing an actual dependency, unlike mere ecosystem similarity.
- **Upstream CI:** 2026-08-14 master [GitHub Builds 31795529703](https://github.com/libusb/hidapi/actions/runs/31795529703) **9/9 jobs successful** (macOS CMake/Automake, Windows MSBuild/MSVC/MinGW, Ubuntu, Alpine, Arch, Fedora MinGW). 2026-10-25 master [Code checks 40183200642](https://github.com/libusb/hidapi/actions/runs/40183200642) passed; do not mislabel it a device test. Virtual-device test workflows on [PR #837](https://github.com/libusb/hidapi/pull/837) were skipped or action-required; PR remains **open/unmerged** and concerns input-report queue handling. No production fix is inferred.
- **Reuse:** portable HID enumeration/open/read/write/feature reports; choice of Linux hidraw (USB/Bluetooth) or libusb (USB only); native Windows/macOS implementations; CMake/Meson build integration. Linux libusb needs libusb development headers, hidraw uses libudev and udev rules. FOX test GUI is explicitly unmaintained.
- **License:** user may choose GPL-3.0, BSD-style three-clause (includes non-endorsement) or original HIDAPI license per `LICENSE.txt`; respect selected terms, copyright and separate backend dependency licensing. No copying done.
- **Score:** Utility 5, Working 4, Reuse 5, Novelty 4, Docs 5, Maintenance 4 = **27**. High-quality build evidence, but no physical USB/Bluetooth runtime evidence from this research.
- **Next:** exercise harmless HID read/feature reports on permitted devices; test hotplug and report queue behavior, backend parity and permissions; investigate PR #837 before claiming a fix.

## 2. Datasette — VERIFIED (upstream) / S28

- **Repository:** https://github.com/simonw/datasette. Published stable [0.65.5](https://github.com/simonw/datasette/releases/tag/0.65.5) on 2026-09-16; [1.0a41](https://github.com/simonw/datasette/releases/tag/1.0a41) on 2026-09-24 is **prerelease**.
- **Source inspected:** `README.md`, `LICENSE`, `pyproject.toml`, `datasette/app.py`, `database.py`, `permissions.py`, `plugins.py`, `hookspecs.py`, `datasette/` and `tests/` directory inventory (API, permissions, auth, CSRF, SQL, Playwright). Package requires **Python >=3.11** and explicitly declares **`sqlite-utils>=4.0`**. This is a direct manifest dependency, not a separately tested integration.
- **Upstream CI:** 2026-10-22 main [Test 39856323145](https://github.com/simonw/datasette/actions/runs/39856323145) passed **5/5** Python 3.11–3.15 jobs, [Playwright 39856323157](https://github.com/simonw/datasette/actions/runs/39856323157) **3/3** (Chromium, Firefox, WebKit), [SQLite versions 39856323220](https://github.com/simonw/datasette/actions/runs/39856323220) passed, and [Pyodide 39856323261](https://github.com/simonw/datasette/actions/runs/39856323261) passed. 2026-10-31 PR tests also passed but are not substituted for current-main evidence.
- **Reuse:** ASGI server lifecycle, SQLite database abstraction, JSON/HTML rendering, facets/filters, actors/permissions, CSRF and tokens, pluggy hooks, CLI/publishing adapters. `pip install datasette` then `datasette serve database.db` for local use; plugins may run Python code.
- **License:** Apache-2.0 in root and package metadata. Dependencies/plugins and served data may have independent licenses or disclosure restrictions. No source copied.
- **Score:** Utility 5, Working 5, Reuse 5, Novelty 4, Docs 5, Maintenance 4 = **28**. Upstream evidence only; no independent deployment or security assessment.
- **Next:** test SQLite import from sqlite-utils, read-only and restricted actor behavior, SQL limits, public exposure defaults, plugin trust and browser-side data leakage; compare stable 0.65 and 1.0 alpha interfaces.

## Maintenance / provenance

- Existing **libusb** entry now identifies HIDAPI's actual `libusb/hid.c` dependency rather than an uninspected related project. This does **not** establish HIDAPI hardware operation.
- Existing **sqlite-utils** entry now records Datasette's declared `sqlite-utils>=4.0` dependency; no runtime compatibility claim.
- Two YouTube seed playlist IDs (`PLMI6SBmd587c`, `PLfidXW0BixTc`) were searched exactly on 2026-10-31 without indexed transcript results. No discovery attributed to unavailable playlists. Other seeds not retried.
- No third-party code or data copied. No independent installation, builds, tests, device traffic or server execution. All CI claims explicitly upstream.
