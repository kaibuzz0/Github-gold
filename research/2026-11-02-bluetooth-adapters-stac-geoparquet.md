# GitHub Gold — Bluetooth Adapters and STAC-GeoParquet (2026-11-02)

## Provenance and verification boundary
GitHub-first recursive research: Bluetooth-Devices/bleak-retry-connector Linux dependency and stac-utils/pystac metadata ecosystem. Searched initial YouTube playlist identifiers (PLMI6SBmd587c, PLfidXW0BixTc, PLI99ObbYUvDn_0tkbXsOYB4ApTyHFQxSi); no indexed title/transcript results. No YouTube finding was used as evidence. All CI evidence below is **upstream GitHub Actions**, not tests run by GitHub Gold. No third-party source copied.

## Bluetooth Adapters — VERIFIED (upstream), A24
- Repository: https://github.com/Bluetooth-Devices/bluetooth-adapters; Apache-2.0 root LICENSE. Install `pip install bluetooth-adapters`; v2.4.0 published **2026-05-26**. Main last inspected commit ece711c8 (2026-05-27).
- Manifest: Python >=3.10 (<3.15 in Poetry constraints), Bleak>=3.0.2, Linux-only dbus-fast>=5.0.14, usb-devices>=0.4.5, aiooui>=0.1.1, uart-devices>=0.1.0. Latest dbus-fast v5.2.0 requires Python >=3.11: Python 3.10 Linux installations need a compatible resolution.
- Source: `src/bluetooth_adapters/adapters.py` abstract adapter contract; `systems/linux.py` BlueZ D-Bus + HCI + USB/UART vendor/product resolution; `systems/linux_hci.py`; `dbus.py`; `history.py`, `models.py`, `storage.py`; `systems/windows.py` and `macos.py` platform representations.
- Crucial caveat: Windows implementation returns a generic default adapter with placeholder values and powered/advertise booleans; do not advertise this as physical hardware enumeration on Windows.
- Upstream [2026-05-27 main push CI](https://github.com/Bluetooth-Devices/bluetooth-adapters/actions/runs/26489407596) **18/18 jobs successful**, including 15 Linux/macOS/Windows Python 3.10–3.14 tests. [2026-10-26 dependency-bot PR CI](https://github.com/Bluetooth-Devices/bluetooth-adapters/actions/runs/40377620756) **failed lint**; 15/15 platform test jobs succeeded, so separate code test results from overall PR conclusion. Scheduled Issue Manager/Hacktoberfest results are not software test evidence.
- Downstream: Bleak Retry Connector v4.7.1 declares bluetooth-adapters>=2.3.0 only on Linux; its existing catalog entry now references this verified dependency.
- Risks: Linux D-Bus privileges, stale adapter metadata, and BLE peer spoofing. No real hardware, Android/Termux or independent D-Bus test.
- Next: reproduce Linux BlueZ adapter discovery on a controlled test bus, verify Python 3.10 dependency lock, and compare macOS/Windows actual adapter values with documentation.

## STAC-GeoParquet — VERIFIED (upstream), S27
- Repository: https://github.com/stac-utils/stac-geoparquet; MIT root LICENSE (Tom Augspurger 2022). Stable **0.8.3 published 2026-10-21**; latest main commits inspected 2026-10-28.
- Manifest: Python >=3.10; PyArrow>=16,!=19.0.0, pystac, geopandas, pandas, pyproj, shapely, ciso8601, orjson. Optional `pgstac` (psycopg, pypgstac) and `deltalake` (<1) extras.
- Source: `stac_geoparquet/arrow/_api.py` converts STAC Item iterables to Arrow RecordBatchReaders and Parquet, with FullFile, FirstBatch and ChunksToDisk schema strategies; `arrow/_to_parquet.py` writes WKB geometry, GeoParquet 1.0/1.1 metadata, STAC collection metadata and streams batches; `arrow/_from_arrow.py` restores STAC property and bbox layouts; `json_reader.py`, `pgstac_reader.py`, `arrow/_delta_lake.py`; numerous test fixtures/cassettes.
- Upstream [2026-10-28 main CI](https://github.com/stac-utils/stac-geoparquet/actions/runs/40688846105): **5/5 Ubuntu Python 3.10–3.14 jobs successful**. Workflow executes uv sync, pre-commit, lint, pytest and strict MkDocs build. This does not establish performance, data fidelity on all inputs, or Windows/macOS builds.
- Compatibility caveats: FullFile schema inference may load entire dataset into memory; FirstBatch expects later batch schema consistency; ChunksToDisk requires existing temp directory and extra I/O. Test heterogeneous extension fields, CRS/WKB, 4D/6D bounding boxes and large datasets before production.
- Downstream/upstream: PySTAC is a direct declared dependency (catalog cross-link updated). STAC-GeoParquet spec and pgstac are companion ecosystem projects; DuckDB consumption is a research lead, not independently verified.
- License: MIT source; preserve notices. Data sources, schemas, optional native libraries and datasets can have distinct licensing.
- Next: build a local fixture round-trip STAC JSON→GeoParquet→STAC JSON; compare geometry/CRS and metadata; measure peak RSS for three schema strategies and document optional pgstac integration.

## Maintenance lead — stac-check (deferred, not rejected)
- https://github.com/stac-utils/stac-check v1.14.0 published **2026-05-02**, MIT license; `stac_check/lint.py` and CLI implement STAC best-practice and geometry linting.
- [2026-05-02 main Test Runner CI](https://github.com/stac-utils/stac-check/actions/runs/25250726363) **6/6 jobs passed** (Python 3.9–3.13, pre-commit). Later [2026-08-03 dependency-update PR CI](https://github.com/stac-utils/stac-check/actions/runs/30780981239) failed; failure root cause not established.
- Stable manifest pins `stac-valid~=4.2.2`; newer STAC Validator is 4.6.1, so do not assume compatibility. This is a credible A-tier research lead but remains deferred pending dependency-version tests. Preserve history rather than inventing a score.

## No independent execution
No package installation, conversion, Bluetooth hardware test, network probe, benchmark, security audit, or third-party source copy was performed in this run.
