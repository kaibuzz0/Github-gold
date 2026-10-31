# Research dossier — PyUSB and Rasterio (2026-10-31 UTC)

## Scope and provenance
GitHub-first review of upstream README files, licenses, source directories, workflows, releases and job results. Exact-ID web searches for YouTube seed playlists `PLMI6SBmd587c` and `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr` yielded no indexed transcript material. No discoveries attributed to unavailable videos. No third-party source copied, built, installed, executed, flashed or security-audited.

## PyUSB — VERIFIED (upstream) / S26
- Upstream: https://github.com/pyusb/pyusb ; root BSD-3-Clause https://github.com/pyusb/pyusb/blob/master/LICENSE .
- Useful files: `usb/core.py` high-level device/descriptor/transfer abstractions; `usb/backend/libusb1.py` direct ctypes bindings to libusb 1.0; `usb/backend/libusb0.py` and `openusb.py` alternatives; `usb/control.py`, `usb/util.py`, `usb/libloader.py` helpers.
- Requirements: Python >=3.9, ctypes, installed compatible native USB backend; libusb 1.0 recommended; device access permissions and kernel driver ownership are platform-dependent. Windows may use separately licensed pyocd/libusb-package.
- Stable release: https://github.com/pyusb/pyusb/releases/tag/v1.3.1 (2025-01-08). Last master push observed 2026-02-12.
- Upstream CI: https://github.com/pyusb/pyusb/actions/runs/21952222286 (2026-02-12) passed 18/18 jobs across Windows/macOS/Linux × Python 3.9–3.14. `.github/workflows/run_tox.yml` runs tox; `tox.ini` invokes `tests/testall.py`. `tests/test_integration.py` expects a special device, so green generic CI is not evidence of real-device transfers. September PR successes are not master CI.
- License boundary: PyUSB BSD-3-Clause; libusb shared library LGPL-2.1-or-later with separate obligations. No code copied.
- Ecosystem: direct source-level link to cataloged libusb; HIDAPI is HID-specific and pySerial is serial-specific, neither a required PyUSB dependency.
- Follow-up: reproduce backend discovery and mocked transfers, validate USB permissions, evaluate Android UsbManager FD handoff/Termux and physical test fixture, and review untrusted descriptor handling.

## Rasterio — VERIFIED (upstream) / S28
- Upstream: https://github.com/rasterio/rasterio ; BSD-3-Clause https://github.com/rasterio/rasterio/blob/main/LICENSE.txt . Native GDAL/PROJ/etc and data licensing separate.
- Useful components: `rasterio/_io.pyx` and `io.py` (GDAL I/O, MemoryFile); `windows.py` (windowed I/O); `warp.py`/`_warp.pyx` (reprojection); `features.py` (rasterize/shapes); `merge.py` (first/last/min/max/sum/count pixel compositing); `vrt.py` (WarpedVRT); `rasterio/rio/` CLI.
- Runtime: Rasterio 1.5+ Python >=3.12, NumPy >=2, GDAL >=3.8. `pyproject.toml` lists source build Cython requirements; wheel-native dependencies may differ by release/platform.
- Stable release: https://github.com/rasterio/rasterio/releases/tag/1.5.2 (2026-09-30). Current development main `__version__` = 1.6.0.dev0; do not present as stable.
- Upstream test evidence: https://github.com/rasterio/rasterio/actions/runs/40157367304 (2026-10-25) 19/19 passed. https://github.com/rasterio/rasterio/actions/runs/40346438112 (2026-10-26) **failure**, with 18 success and one cancelled macOS ARM/Python 3.13 job; reason for cancellation not independently established. https://github.com/rasterio/rasterio/actions/runs/41231881794 (2026-10-31) successful *tag discovery* only, actual GDAL tag tests skipped. Do not call latest full matrix green.
- Recursive links: GDAL is a native runtime dependency; Tippecanoe handles vector rather than raster tiling; PMTiles/MapLibre could consume separately generated tiles but no direct Rasterio→PMTiles/MapLibre pipeline verified. SciPy is an adjacent numerical toolkit, not a declared runtime dependency.
- Risks: large or malicious raster data, GDAL drivers, remote virtual filesystem access, RAM/disk pressure, coordinate reference systems and source-data licensing. No independent I/O or geospatial conversion performed.
- Follow-up: synthetic GeoTIFF read/write and window round-trip, CRS reprojection accuracy, controlled GDAL driver whitelist, no-network operation, raster-to-tiles conversion using a separately reviewed tool; inspect cancellation on latest full CI.

## Maintenance
Updated existing libusb catalog and master list with source-verified PyUSB `usb/backend/libusb1.py` relationship. No claim of USB device runtime interoperability or license equivalence. Both new canonical entries use the existing six-factor score/tier model, with no code copied.
