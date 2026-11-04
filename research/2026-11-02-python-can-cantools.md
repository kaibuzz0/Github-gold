# Research dossier — python-can and cantools (2026-11-02)

## Method and provenance
GitHub-first recursive research of CAN transport and database tooling. Inspected upstream README, source and test trees, stable manifests, licenses, releases and GitHub Actions job conclusions. Exact-ID YouTube searches for `PLMI6SBmd587c` and `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr` returned no indexed transcripts; no findings attributed to videos. No third-party implementation code copied.

## python-can — VERIFIED upstream, S27 (5/4/5/4/5/4)
- Repository: https://github.com/hardbyte/python-can; LGPL-3.0-only root LICENSE.txt and tagged/main manifest. Before reuse review license notices, linking and redistribution requirements.
- [v4.6.1](https://github.com/hardbyte/python-can/releases/tag/v4.6.1) published **2025-08-12**; tagged manifest Python >=3.9; main Python >=3.10. Stable and development requirements differ.
- Reusable modules: `can/bus.py` BusABC; `can/interfaces/virtual.py` in-memory bus; `can/interfaces/socketcan/` Linux backend; `can/notifier.py`/`can/listener.py` asynchronous dispatch; `can/io/` log formats; `can/broadcastmanager.py` periodic sends; logger/player/bridge/viewer CLIs.
- `test/test_interface_virtual.py` tests two in-memory buses and timestamp preservation; this is source-level test evidence.
- [2026-10-25 PR Tests workflow](https://github.com/hardbyte/python-can/actions/runs/40224110111): **25 successful jobs, one skipped PyPI release**, Python 3.10–3.14, PyPy, Linux/macOS/Windows, docs, lint and packaging. This is **upstream PR CI**, not stable-tag testing or hardware verification. Numerous newer PR workflows report `action_required` rather than passing tests.
- Stable optional `serial` and `seeedstudio` extras declare pySerial; it is **not** a core dependency. Cantools is a downstream consumer.
- Risks: CAN traffic may control physical equipment. Restrict to virtual or authorized isolated networks; device-specific drivers, permissions and vendor protocol support vary.
- Follow-up: install in disposable environment, run virtual-bus message and log round-trips, compare stable/main APIs and investigate action_required CI causes.

## cantools — VERIFIED upstream, S28 (5/5/5/4/5/4)
- Repository: https://github.com/cantools/cantools; root MIT license (Erik Moqvist 2015–2019), preserve notice.
- [v45.1.2](https://github.com/cantools/cantools/releases/tag/45.1.2) published **2026-10-29**; tagged manifest Python >=3.10 and direct `python-can>=4.6.0`, bitstruct, textparser, argparse_addons and crccheck. Plotting optional via matplotlib.
- Reusable modules: `src/cantools/database/can/formats/dbc/`, `arxml/`, `kcd.py`, `sym.py`; diagnostics DID codecs; signal encoding/multiplexing; `src/cantools/subparsers/` decode/dump/plot/codegen; `src/cantools/tester.py`; comprehensive test fixtures.
- README shows DBC parse -> encode -> python-can SocketCAN send -> receive/decode, and `candump` processing. Documentation examples are **not independently executed**.
- [2026-10-29 main push CI](https://github.com/cantools/cantools/actions/runs/40835067598): **18 successful jobs, one skipped release**, including codegen, lint, build, docs and cross-platform Python 3.10/3.14/PyPy tests.
- Caveats: proprietary DBC/ARXML schema rights; generated C and live bus operations require independent safety/compatibility validation.
- Follow-up: offline fixture parsing, malformed/multiplexed frame tests, generated C compilation and virtual CAN integration.

## Deferred and maintenance findings
- [Bluetooth-Devices/uart-devices](https://github.com/Bluetooth-Devices/uart-devices): MIT, [v0.1.1](https://github.com/Bluetooth-Devices/uart-devices/releases/tag/v0.1.1) published 2025-02-22. [2026-10-26 PR CI](https://github.com/Bluetooth-Devices/uart-devices/actions/runs/40377719072) 18 successful jobs, one skipped release. But `tests/test_init.py` tests only construction and invalid IDs; it does not cover Linux sysfs symlink resolution or `uevent` parsing in `src/uart_devices/__init__.py`. README sparse, manifest says Pre-Alpha. Deferred pending meaningful sysfs fixture tests.
- [stac-utils/stac-check](https://github.com/stac-utils/stac-check): remains deferred; v1.14.0 2026-05-02, August dependency-update CI failure and `stac-valid` compatibility unresolved.
- Existing pySerial entry cross-linked to python-can **optional** stable serial transport; not represented as a core dependency.

## Verification boundary
VERIFIED means inspected upstream source, release and tests/CI evidence, not independent installation, hardware operation, CAN validation, generated C compilation or security review. Scores are Utility, Working Evidence, Reusability, Novelty, Documentation, Maintenance (0–5 each).
