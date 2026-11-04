# GitHub Gold — PySTAC and python-zeroconf research (2026-11-01)

## Provenance and scope
Independent GitHub-first research, extending the catalog's rio-tiler/TiTiler geospatial ecosystem and expanding into local-first LAN discovery. Exact-ID web searches for two YouTube seed playlists yielded no indexed results; no transcript or video attribution. All verification below is **upstream repository evidence** unless explicitly stated. No upstream implementation code copied.

## PySTAC — VERIFIED (upstream) / S28
- Repository: https://github.com/stac-utils/pystac ; license: https://github.com/stac-utils/pystac/blob/main/LICENSE (Apache-2.0, preserve license/notice).
- Stable release: https://github.com/stac-utils/pystac/releases/tag/v1.15.2 (2026-07-27). Stable tag manifest `pyproject.toml` requires Python >=3.10 and `pystac-core>=1.15.0,<2`. Main's manifest already uses `pystac-core>=1.15.2,<2`; do not conflate.
- README documents 2026 extension-package split: core API uses semantic versioning but extensions are **independently versioned**. `pystac` metapackage brings extension packages; review their separate licenses and version constraints.
- Useful code: `core/pystac/{catalog,collection,item,asset,stac_io,layout,link}.py`, `core/pystac/validation/`, `extensions/`; tests include `tests/test_stac_io.py`, `test_catalog.py`, `test_item.py`.
- Upstream CI: https://github.com/stac-utils/pystac/actions/runs/40940313953 — 2026-10-29 main push **16/16 jobs successful** (Python 3.10–3.13 on Linux/macOS/Windows, docs, coverage, benchmarks). Two Oct 30 dynamic dependency-update workflows failed, not the cited main test run.
- **Verified direct downstream dependency:** rio-tiler stable 9.4.12 `pyproject.toml` lists `pystac>=1.9,<2.0`; `rio_tiler/io/stac.py` directly imports `pystac`: https://github.com/cogeotiff/rio-tiler/blob/9.4.12/rio_tiler/io/stac.py .
- TiTiler current `src/titiler/extensions/titiler/extensions/stac.py` conditionally imports PySTAC and extensions test group lists `pystac[validation]`. **Not** a core TiTiler requirement. See https://github.com/developmentseed/titiler/blob/main/src/titiler/extensions/pyproject.toml .
- Caveats: remote STAC JSON/schema fetching needs URL trust controls; independent extension versions can change behavior. No local install, serialization, schema-validation or network test.
- Next: synthetic local STAC Item/Collection serialization and validation; verify stable rio-tiler STAC reader against a local COG; examine separate extension package compatibility.

## python-zeroconf — VERIFIED (upstream) / S28
- Repository: https://github.com/python-zeroconf/python-zeroconf .
- **Current license:** LGPL-2.1-or-later (https://github.com/python-zeroconf/python-zeroconf/blob/master/COPYING ; manifest confirms). https://github.com/python-zeroconf/python-zeroconf/blob/master/RELICENSING.md records contributor consent gathering for a *possible future* Apache-2.0 relicensing. Do not catalog or copy it as Apache-2.0.
- Stable release https://github.com/python-zeroconf/python-zeroconf/releases/tag/0.153.0 (2026-10-31). Current `pyproject.toml` and changelog confirm **Python >=3.11**; v0.153.0 drops Python 3.10. Earlier versions may support 3.10 but are not equivalent to current stable.
- Useful code: `src/zeroconf/_core.py`, `_dns.py`, `_protocol/`, `_cache.py`, `_services/{browser,info,registry}.py`, `_utils/net.py`, `asyncio.py`; optional Cython; tests include DNS, services, incoming-packet fuzzing.
- Upstream CI: https://github.com/python-zeroconf/python-zeroconf/actions/runs/41274832304 — 2026-11-01 dependency PR **35 successful, 3 skipped** jobs (OS/Python/Cython matrix, lint, benchmark, fuzz-related check). This is a PR run, not a proof that the latest release was independently installed or tested.
- README documents Bonjour/Avahi interoperability, IPv6 limitations and no D-Bus dependency. The library implements multicast DNS/DNS-SD; it is **not** an authentication layer. Service records may be spoofed, Wi-Fi multicast may be filtered, and some mobile environments restrict discovery.
- Next: local loopback/isolated LAN registration-discovery test, IPv4/IPv6 and interface restrictions, untrusted record parsing; monitor relicensing issue #1835 before any code reuse.

## Existing catalog maintenance
- **rio-tiler:** added direct PySTAC stable dependency evidence and source import, with no runtime interoperability claim; score unchanged.
- **TiTiler:** linked PySTAC only as optional STAC extension/test dependency, not core; score unchanged.

## Verification boundary
Source files, manifests, license files, changelogs, releases, test trees and GitHub Actions job conclusions inspected. No independent Python execution, network discovery, physical-device tests, COG rendering, builds, installs, or security audits. No third-party code copied.
