# GitHub Gold research — PyVISA-sim and rio-tiler (2026-11-01)

## Scope and verification boundary

Inspected GitHub README, licenses, manifests at current main and stable tags, changelogs, source modules, test trees, GitHub Releases and Actions job steps. Two exact-ID YouTube playlist searches (`PLMI6SBmd587c`, `PLfidXW0BixTc`) yielded no indexed transcripts. No video-derived claims, independent installations, executed tests, physical devices, raster conversions, security audits or copied upstream implementation code.

## PyVISA-sim — VERIFIED upstream / S26 (5+4+5+4+4+4)

- Repository: https://github.com/pyvisa/pyvisa-sim. [MIT license](https://github.com/pyvisa/pyvisa-sim/blob/main/LICENSE.txt); preserve copyright and permission notices.
- Latest observed GitHub release: [0.8.1, 2025-09-04](https://github.com/pyvisa/pyvisa-sim/releases/tag/0.8.1). `CHANGES.rst` ends at 0.7.1 and lists unreleased changes; release and changelog are not synchronized.
- [2026-10-27 scheduled main CI](https://github.com/pyvisa/pyvisa-sim/actions/runs/40446315171): 14/14 successful jobs, including pytest on Linux/macOS/Windows, Python 3.10–3.13, format/lint/mypy and aggregate. Upstream tests only.
- [highlevel.py](https://github.com/pyvisa/pyvisa-sim/blob/main/pyvisa_sim/highlevel.py) implements `SimVisaLibrary`, resource and session dispatch. [parser.py](https://github.com/pyvisa/pyvisa-sim/blob/main/pyvisa_sim/parser.py) handles versioned YAML definitions. [devices.py](https://github.com/pyvisa/pyvisa-sim/blob/main/pyvisa_sim/devices.py), [component.py](https://github.com/pyvisa/pyvisa-sim/blob/main/pyvisa_sim/component.py) and [channels.py](https://github.com/pyvisa/pyvisa-sim/blob/main/pyvisa_sim/channels.py) model state, responses and channels.
- [sessions](https://github.com/pyvisa/pyvisa-sim/tree/main/pyvisa_sim/sessions) cover GPIB, serial, TCPIP and USB simulation. [testsuite](https://github.com/pyvisa/pyvisa-sim/tree/main/pyvisa_sim/testsuite) contains binary-dialogue, parser and serial regression tests.
- [Main manifest](https://github.com/pyvisa/pyvisa-sim/blob/main/pyproject.toml) and [0.8.1 manifest](https://github.com/pyvisa/pyvisa-sim/blob/0.8.1/pyproject.toml): Python >=3.10, pyvisa>=1.15.0, PyYAML, stringparser and typing-extensions. README still claims Python 3.8–3.11 and PyVISA 1.11+, which is stale.
- Related: [PyVISA](https://github.com/pyvisa/pyvisa) direct dependency; [PyVISA-Py](https://github.com/pyvisa/pyvisa-py) is an alternative hardware backend, not a dependency. Simulation cannot establish actual hardware timing, driver correctness or command safety.
- Next: independently run `ResourceManager("@sim")` with explicit YAML fixtures, test query/error/binary behaviors and compare stable versus main behavior.

## rio-tiler — VERIFIED upstream / S28 (5+5+5+4+5+4)

- Repository: https://github.com/cogeotiff/rio-tiler. [BSD-3-Clause](https://github.com/cogeotiff/rio-tiler/blob/main/LICENSE); preserve license, copyright and disclaimer. GDAL, Rasterio, codecs and datasets have independent licensing.
- Latest observed stable [9.4.12, 2026-10-08](https://github.com/cogeotiff/rio-tiler/releases/tag/9.4.12). [2026-10-31 main push CI](https://github.com/cogeotiff/rio-tiler/actions/runs/41243335207) passed 3/3 Python 3.12–3.14 pytest jobs; [2026-11-01 security-dependency PR CI](https://github.com/cogeotiff/rio-tiler/actions/runs/41259299838) also passed 3/3. Separate dependency-update automation failure is not a failed application test.
- [io/rasterio.py](https://github.com/cogeotiff/rio-tiler/blob/main/rio_tiler/io/rasterio.py): Rasterio-backed `Reader`, `tile`, `part`, `feature`, `point`, Morecantile grids and WarpedVRT. [io/stac.py](https://github.com/cogeotiff/rio-tiler/blob/main/rio_tiler/io/stac.py): STAC asset selection. [mosaic/reader.py](https://github.com/cogeotiff/rio-tiler/blob/main/rio_tiler/mosaic/reader.py): multi-asset mosaic and configurable concurrency/pixel selection. [models.py](https://github.com/cogeotiff/rio-tiler/blob/main/rio_tiler/models.py): ImageData/PointData. [tests](https://github.com/cogeotiff/rio-tiler/tree/main/tests): raster, STAC, mosaic, xarray and Zarr regression coverage.
- **Version-sensitive finding:** [stable 9.4.12 manifest](https://github.com/cogeotiff/rio-tiler/blob/9.4.12/pyproject.toml) requires Python >=3.11, Rasterio >=1.4.0 and Morecantile >=5,<8. [Development main](https://github.com/cogeotiff/rio-tiler/blob/main/pyproject.toml) requires Python >=3.12, Rasterio >=1.5.1 and affine >=3.0; [unreleased changelog](https://github.com/cogeotiff/rio-tiler/blob/main/CHANGES.md) describes breaking experimental N-D/Zarr behavior. Do not present these main-only changes as stable release requirements.
- Direct dependencies: [Rasterio](https://github.com/rasterio/rasterio), [Morecantile](https://github.com/developmentseed/morecantile). Complement: [rio-cogeo](https://github.com/cogeotiff/rio-cogeo), not a direct dependency. Downstream lead: [TiTiler](https://github.com/developmentseed/titiler).
- Risks: GDAL virtual filesystems and untrusted STAC URLs may fetch external content; large rasters and threaded mosaics can exhaust resources. No independent range-request, tile, offline or memory testing.
- Next: reproducible local COG-to-tile round-trip; controlled HTTP range test; stable/main Python dependency matrix and mosaic resource limits.

## Maintenance and deduplication

Inspected current PR #7 head, README, MASTER_LIST, catalog/tools.json, empty candidate queue, playlist source and audit script. Verified neither new repository was already cataloged among 167 canonical entries. Added two catalog and master-list entries; cross-linked existing PyVISA, Morecantile, Rasterio and rio-cogeo without score changes. Target 169 unique URLs and 169 canonical headings; no upstream implementation copied.
