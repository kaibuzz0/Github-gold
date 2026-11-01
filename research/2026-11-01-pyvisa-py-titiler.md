# GitHub Gold — PyVISA-py and TiTiler research (2026-11-01)

## Scope and provenance
GitHub-first recursive investigation from existing PyVISA/PyVISA-sim and rio-tiler/Morecantile catalog entries. The first two YouTube seed playlist pages (PLMI6SBmd587c, PLfidXW0BixTc) were throttled on fetch; **no transcript claims or video-derived attribution**. Current draft PR #7 branch was inspected first. No upstream source code was copied.

## PyVISA-py — VERIFIED upstream / S27
- Repo: https://github.com/pyvisa/pyvisa-py
- Release: https://github.com/pyvisa/pyvisa-py/releases/tag/0.8.1 (2025-09-04); `CHANGES` labels 0.9.0 **unreleased**.
- MIT license: https://github.com/pyvisa/pyvisa-py/blob/main/LICENSE (retain copyright/permission notice).
- Manifest: https://github.com/pyvisa/pyvisa-py/blob/main/pyproject.toml — Python >=3.10; `pyvisa>=1.15.0`; optional `pyserial>=3.0`, `pyusb`, `libusb-package`, GPIB and discovery extras.
- Reusable components: [highlevel dispatcher](https://github.com/pyvisa/pyvisa-py/blob/main/pyvisa_py/highlevel.py), [USB/PyUSB bridge](https://github.com/pyvisa/pyvisa-py/blob/main/pyvisa_py/usb.py), `pyvisa_py/sessions.py`, `serial.py`, `tcpip.py`, `protocols/{usbtmc,usbraw,vxi11,hislip}.py`, `prologix.py`, `testsuite/`.
- Upstream evidence: [2026-08-18 main scheduled CI](https://github.com/pyvisa/pyvisa-py/actions/runs/32085356622) passed 14/14 jobs (12 OS/Python unit-test combinations + formatting + aggregate). This is **upstream** evidence; no local test or physical device session.
- Maintenance caution: 0.9.0 unreleased changelog contains USB RAW, VXI-11 and HiSLIP fixes. Do not assume fixes exist in stable 0.8.1. Optional driver/transport licensing and device access permissions are independent.
- Next: install in isolated environment; test backend discovery, simulated serial/network fixtures, then authorized hardware; compare stable vs main fixes.

## TiTiler — VERIFIED upstream / S28
- Repo: https://github.com/developmentseed/titiler
- Release: https://github.com/developmentseed/titiler/releases/tag/v2.4.0 (2026-09-21).
- MIT license: https://github.com/developmentseed/titiler/blob/main/LICENSE; separately assess GDAL/Rasterio/native dependencies.
- Crucial packaging correction: [README](https://github.com/developmentseed/titiler/blob/main/README.md) explicitly warns the `titiler` PyPI metapackage was dropped in late 2025. Install `titiler.application` or `titiler.core`, etc. Root `pyproject.toml` is a workspace manifest, not an instruction to install the obsolete PyPI metapackage.
- [Core manifest](https://github.com/developmentseed/titiler/blob/main/src/titiler/core/pyproject.toml) declares Python >=3.11, `rio-tiler>=9.1,<10.0`, Morecantile, Rasterio and FastAPI/Starlette.
- Reusable components: [core TilerFactory](https://github.com/developmentseed/titiler/blob/main/src/titiler/core/titiler/core/factory.py), [request dependencies](https://github.com/developmentseed/titiler/blob/main/src/titiler/core/titiler/core/dependencies.py), [application routers](https://github.com/developmentseed/titiler/blob/main/src/titiler/application/titiler/application/main.py), [mosaic factory](https://github.com/developmentseed/titiler/blob/main/src/titiler/mosaic/titiler/mosaic/factory.py), [xarray factory](https://github.com/developmentseed/titiler/blob/main/src/titiler/xarray/titiler/xarray/factory.py).
- Upstream evidence: [2026-09-18 main CI](https://github.com/developmentseed/titiler/actions/runs/35358292721) passed 4/4 Ubuntu Python 3.11–3.14 jobs. Later dependency changes exist; do not present this run as a current-head CI guarantee.
- [SECURITY.md](https://github.com/developmentseed/titiler/blob/main/SECURITY.md) documents GDAL/VRT local-file access, remote dataset host restrictions and expression attack surfaces; restrict dataset hosts, filesystem/network access and GDAL drivers. Nonroot container uid 65532 from v2.3.0.
- Next: local-only FastAPI smoke test with a synthetic COG, compare TileJSON output and Morecantile bounds, evaluate malicious URL/VRT defenses and resource ceilings before any public deployment.

## Existing entries maintained
- PyVISA: linked PyVISA-py as separately cataloged optional backend, not core dependency.
- rio-tiler: linked TiTiler as downstream consumer with directly declared `rio-tiler>=9.1,<10.0`; no executed integration claim.
- Both existing Gold scores retained. New entries scored by utility, working evidence, reusability, novelty, documentation and maintenance, each 0–5.

## Verification limits
Inspected source files, manifests, licenses, changelogs and upstream CI job conclusions. No third-party code copied. No independent builds, installs, firmware operations, hardware sessions, HTTP server runs, COG conversion, or security tests performed.
