# GitHub Gold research — Morecantile and PyVISA (2026-10-31)

## Method and verification boundary

GitHub-first research across two distinct ecosystems: OGC tile-matrix grids and scientific instrument control. Read upstream README files, package manifests, licenses, changelogs, source modules, test trees, release metadata and individual GitHub Actions job conclusions. Exact-ID web searches for YouTube playlists `PLMI6SBmd587c` and `PLfidXW0BixTc` returned no indexed metadata or transcripts; neither project is attributed to a video. No third-party implementation code was copied. No independent installations, Python executions, coordinate computations, instrument connections or security audits were performed.

## Morecantile — VERIFIED / S27 (5+4+5+4+5+4)

- Repository: https://github.com/developmentseed/morecantile
- MIT license: https://github.com/developmentseed/morecantile/blob/main/LICENSE. `morecantile/scripts/cli.py` explicitly credits BSD-3 Mapbox mercantile code; preserve both sets of notices if adapting relevant source.
- Stable release: [7.1.0 (2026-09-16)](https://github.com/developmentseed/morecantile/releases/tag/7.1.0). [CHANGES.md](https://github.com/developmentseed/morecantile/blob/main/CHANGES.md) documents new `matrix_to_geojson`; 7.0.0 introduced bounds, validation, Python minimum and property-name breaking changes.
- Upstream CI: [2026-10-25 main push, run 40181168224](https://github.com/developmentseed/morecantile/actions/runs/40181168224) passed **4/4** Ubuntu Python 3.11–3.14 test jobs. Each job ran tests; 3.14 also ran pre-commit. [2026-10-26 PR CI 40309866338](https://github.com/developmentseed/morecantile/actions/runs/40309866338) succeeded. A 2026-10-28 dependency-bot update failure is not a failed application test.
- [models.py](https://github.com/developmentseed/morecantile/blob/main/morecantile/models.py): `TileMatrixSet`, `TileMatrix`, `tile`, `bounds`, `xy_bounds`, `tiles`, `quadkey`, `parent`, `children`, `is_valid`, `matrix_to_geojson`. OGC 2D TMS 2.0 data modeling and CRS conversions via pyproj/Pydantic.
- [defaults.py](https://github.com/developmentseed/morecantile/blob/main/morecantile/defaults.py): built-in and user-registered TileMatrixSets; `TILEMATRIXSET_DIRECTORY` allows custom JSON input.
- [CLI](https://github.com/developmentseed/morecantile/blob/main/morecantile/scripts/cli.py): coordinates, shapes, tiles, TMS inspection and GeoJSON conversion; see upstream BSD-3 source credit.
- [Tests](https://github.com/developmentseed/morecantile/tree/main/tests): grid conformability, variable-width matrices, models and CLI.
- Runtime: Python >=3.11; `pyproj>=3.1,<4.0`, `pydantic~=2.0`, attrs and Click; Rasterio optional extra. The already cataloged [rio-cogeo](https://github.com/cogeotiff/rio-cogeo/blob/main/pyproject.toml) declares `morecantile>=5,<8`, which accepts 7.1.0 **at manifest level only**.
- Risks: version-7 behavior changes, CRS assumptions, malformed custom TMS JSON, precision differences at tile boundaries; no independent raster or map integration tests.
- Recursive leads: `cogeotiff/rio-tiler`, `developmentseed/titiler`, `mapbox/mercantile`, OGC TMS specification and `developmentseed/supermorecado`.

## PyVISA — VERIFIED / S27 (5+4+5+4+5+4)

- Repository: https://github.com/pyvisa/pyvisa
- MIT license: https://github.com/pyvisa/pyvisa/blob/main/LICENSE. Vendor VISA libraries, instrument drivers, optional backend modules and any bundled third-party code require independent review.
- Latest GitHub release observed: [1.16.2 (published 2026-02-27)](https://github.com/pyvisa/pyvisa/releases/tag/1.16.2). [CHANGES](https://github.com/pyvisa/pyvisa/blob/main/CHANGES) separately lists 1.17.0 dated 2026-07-06 and duplicate unreleased headings; GitHub Releases did not establish a 1.17.0 publication. Do not equate changelog version headings with published releases.
- Upstream CI: [2026-10-27 scheduled main, run 40440465093](https://github.com/pyvisa/pyvisa/actions/runs/40440465093) passed **17/17** jobs: 15 pytest combinations on Linux/macOS/Windows and Python 3.10–3.14, one format/lint/type-check job and one aggregate result. [2026-10-26 main push CI 40313328536](https://github.com/pyvisa/pyvisa/actions/runs/40313328536) also passed. 2026-10-30/31 external PR workflows were `action_required`, not demonstrated test failures.
- [highlevel.py](https://github.com/pyvisa/pyvisa/blob/main/pyvisa/highlevel.py): `ResourceManager`, `VisaLibraryBase`, session/resource lifecycle and backend discovery.
- [messagebased.py](https://github.com/pyvisa/pyvisa/blob/main/pyvisa/resources/messagebased.py): `read_binary_values`, `write_binary_values`, `query`, termination handling and timeout semantics. Binary block parser robustness merits review before accepting arbitrary instrument data.
- [rname.py](https://github.com/pyvisa/pyvisa/blob/main/pyvisa/rname.py): canonical VISA resource-name parser and filters; TCPIP SOCKET port validation is listed in unreleased changes.
- [ctwrapper](https://github.com/pyvisa/pyvisa/tree/main/pyvisa/ctwrapper): vendor VISA shared-library bindings; [testsuite](https://github.com/pyvisa/pyvisa/tree/main/pyvisa/testsuite) covers high-level API, resource names and message parsing.
- Runtime: Python >=3.10, vendor VISA shared library or optional PyVISA-Py backend. [PyVISA-Py manifest](https://github.com/pyvisa/pyvisa-py/blob/main/pyproject.toml) requires `pyvisa>=1.15.0` and offers optional `pyserial>=3.0` and `pyusb` extras. **PyVISA core does not directly require either transport library.**
- Risks: physical instruments and vendor backends not exercised by inspected unit CI; commands can change device settings; restrict remote TCP/IP instrument access and use read-only test commands where possible.
- Recursive leads: `pyvisa/pyvisa-py` (separate catalog candidate), `pyvisa/pyvisa-sim` (simulation for repeatable tests), GPIB/USB/TCPIP transport compatibility and binary block parser tests.

## Maintenance and deduplication

Checked all 165 existing canonical URLs and empty candidate queue. Added two new canonical entries, updated rio-cogeo's Morecantile dependency relationship, and added accurate optional-backend cross-links to existing pySerial and PyUSB entries. No score inflation or unrelated entry changes. Human-readable and machine-readable records are synchronized.
