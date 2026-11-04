# Research dossier — pySerial and MapLibre GL JS (2026-10-31 UTC)

## Method and scope
GitHub-first inspection of official repositories, release metadata, source trees, dependency declarations, licenses and GitHub Actions. Exact-ID searches for YouTube seeds `PLMI6SBmd587c` and `PLfidXW0BixTc` yielded no usable indexed video or transcript material; **no findings attributed to YouTube**. No third-party code copied. No independent installation, execution, hardware testing or browser rendering.

## pySerial — VERIFIED (upstream) / S26
- Upstream: https://github.com/pyserial/pyserial ; author Chris Liechti; BSD-3-Clause at https://github.com/pyserial/pyserial/blob/master/LICENSE.txt .
- Native serial backends: `serial/serialposix.py`, `serial/serialwin32.py`; common settings and timeout logic: `serial/serialutil.py`; URL dispatch: `serial/__init__.py`.
- High-reuse pieces: `serial/urlhandler/protocol_loop.py` virtual serial transport; `serial/rfc2217.py` and `protocol_rfc2217.py` for RFC2217; `serial/tools/miniterm.py` CLI and `list_ports.py`; `examples/` serial bridges.
- Optional `serial/urlhandler/protocol_cp2110.py` imports Python `hid` (cython-hidapi) for Silicon Labs CP2110/CP2114 HID-to-UART. The file itself warns that hardware-flow-control signals, cancellation and model-specific baud validation are incomplete. This is not a direct dependency on the libusb/hidapi C repository.
- Runtime: `pip install pyserial`; master `pyproject.toml` declares Python >=3.10 and optional `cp2110 = ["hidapi"]`. Platform serial permissions and OS-specific device paths matter.
- Release caveat: GitHub `v3.5` release metadata says 2025-11-20 (https://github.com/pyserial/pyserial/releases/tag/v3.5), while `CHANGES.rst` dates version 3.5 to 2020-11-23 and master `serial.__version__` is 3.5. Do **not** treat GitHub publication metadata as evidence of a new 2025 feature version.
- Evidence: https://github.com/pyserial/pyserial/actions/runs/22471324995 (2026-02-27 master push): four successful tox jobs (Linux, macOS, Windows, Cygwin). Master last observed commit 2026-02-27. October PR workflows `action_required` do not validate master. CI is upstream evidence only; no real serial/HID devices tested here.
- Risks: network serial protocols may expose hardware controls if not access-controlled; optional `hid` dependency licensing and binary distribution need separate review.
- Follow-up: run loop:// tests and RFC2217 localhost round trip with explicit timeout; validate CP2110 hardware, USB permissions, Termux and Android USB FD behavior; review queued PR fixes before claiming they are released.

## MapLibre GL JS — VERIFIED (upstream) / S29
- Upstream: https://github.com/maplibre/maplibre-gl-js ; MapLibre organization. License https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt : BSD-3-Clause with inherited pre-1.14 Mapbox GL JS notices and additional bundled components. Preserve notices, audit map/data licensing separately.
- Source: `src/ui/map.ts` and `src/ui/camera.ts` manage map/camera; `src/source/vector_tile_source.ts` and `geojson_source.ts` ingest data; `src/source/worker_tile.ts` handles worker-side tile parsing; `src/tile/tile_manager.ts` handles tiles; `src/render/` and `src/shaders/` render through GPU; `src/style/` handles styles.
- Integration seam: https://github.com/maplibre/maplibre-gl-js/blob/main/src/source/protocol_crud.ts exposes `addProtocol` and links official PMTiles protocol example. https://github.com/protomaps/PMTiles documents JS MapLibre GL JS consumption. This supports a feasible Tippecanoe -> PMTiles -> MapLibre pipeline, **not a verified end-to-end run**.
- Runtime: npm `maplibre-gl`, CSS, WebGL-capable browser/WebView and Web Workers; Node toolchain for source builds. A fully offline application must host styles, vector/raster tiles, glyphs and sprites locally. README sample uses external CDN and demo tile service.
- Release: https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.16.0 (2026-10-25). Main `package.json` declares 6.16.0.
- Upstream test evidence: https://github.com/maplibre/maplibre-gl-js/actions/runs/40871400391 (2026-10-29 main push): 20 successful jobs (unit, Linux/Windows integration and render shards, builds, hygiene, benchmarks and coverage), one skipped bundle-size job. https://github.com/maplibre/maplibre-gl-js/actions/runs/41151201935 (2026-10-31 scheduled CodeQL): passed. CodeQL is not a full security audit. Last observed main commit 2026-10-30.
- Caveats: WebGL GPU/memory usage, browser/WebView support, CORS, untrusted large tile data, third-party font/sprite availability, data attribution and license boundaries. No independent rendering or PMTiles playback.
- Follow-up: build a tiny GeoJSON -> Tippecanoe -> PMTiles -> MapLibre GL JS reproducible demo; test network-disabled mode, cache invalidation, tile bounds, Android WebView and mobile performance; compare native and JS render behavior.

## Recursive catalog maintenance
- Existing HIDAPI now notes the optional Python `hid` bridge from pySerial CP2110, without falsely claiming direct C-library dependency.
- Existing PMTiles cross-links MapLibre GL JS `addProtocol`/PMTiles adapter.
- Existing Tippecanoe links the browser renderer without claiming a tested tile pipeline.
- Existing MapLibre Native links its separately implemented browser sibling.
- Both new projects and four existing relationships are synchronized in `MASTER_LIST.md` and `catalog/tools.json`; no upstream code copied.

## Verification boundaries
`VERIFIED` here means inspected primary-source structure and explicit upstream CI, not independent hardware/browser validation. Never describe tests or conversions as personally executed.
