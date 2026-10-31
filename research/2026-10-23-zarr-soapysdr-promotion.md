# GitHub Gold — Zarr Python and SoapySDR promotion evidence
**Checked:** 2026-10-23 (America/Chicago)  
**Method:** GitHub-first, upstream README/source/manifests/licenses/releases/commits/Actions. Existing September dossiers revisited; no YouTube transcript findings claimed.  
**Independent execution:** None. No third-party implementation code copied.

## Zarr Python — VERIFIED, S/29
- **Repository:** https://github.com/zarr-developers/zarr-python
- **Evidence:** Root MIT license (https://github.com/zarr-developers/zarr-python/blob/main/LICENSE.txt); `pyproject.toml` currently requires Python >=3.12; package directories `src/zarr/core/`, `src/zarr/storage/`, `packages/zarr-indexing/`, `packages/zarr-http-server/`, `packages/zarr-metadata/` inspected.
- **Stable release:** v3.4.1 published **2026-10-08**, https://github.com/zarr-developers/zarr-python/releases/tag/v3.4.1. Release notes mention explicit runtime validation in place of assertions, sharding index codec restrictions, dtype round-trip fixes, and local/fsspec storage correctness fixes. Do not conflate release contents with subsequent main changes.
- **CI:** 2026-10-23 upstream **pull request** Test workflow https://github.com/zarr-developers/zarr-python/actions/runs/39892893049 passed **16/16** jobs; Slow Hypothesis https://github.com/zarr-developers/zarr-python/actions/runs/39892893145 passed **1/1**. These runs are on PR head `86728e0`, not necessarily main or v3.4.1. No tests run locally.
- **Reusable code:** `src/zarr/core/array.py` array operations; `src/zarr/core/codec_pipeline.py` codec processing; `src/zarr/core/chunk_grids.py` chunk indexing; `src/zarr/storage/_fsspec.py` and `_obstore.py` storage adapters; `packages/zarr-indexing/` independent NumPy-based lazy coordinate transforms; `packages/zarr-http-server/` ASGI store serving.
- **Security/correctness:** The HTTP package explicitly labels itself experimental. `store_app` exposes all store keys, reads are enabled by default, and enabling writes requires separate authorization. Core Zarr is not a transactional database. Test partial shard writes, codecs and backend consistency before production use.
- **License:** MIT, copyright/permission notice required. Separate dataset/codec/backend licenses may apply.
- **Scoring:** Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5 = **29/30**.
- **Ecosystem:** https://github.com/zarr-developers/zarr-specs (format, CC-BY-4.0), https://github.com/earth-mover/icechunk (versioned transactional Zarr storage, Apache-2.0), numcodecs, xarray, Dask. Icechunk was inspected as a related active repository, not promoted in this batch.
- **Prior dossier:** `research/2026-09-06-zarr-python-chunked-array-storage-indexing-stack.md`.
- **Next:** verify cross-runtime Zarr v3 interoperability; compare partial-shard write tests; evaluate experimental HTTP range/authorization behavior and Icechunk snapshot semantics.

## SoapySDR — VERIFIED, S/27
- **Repository:** https://github.com/pothosware/SoapySDR
- **Evidence:** Root Boost Software License 1.0 at https://github.com/pothosware/SoapySDR/blob/master/LICENSE_1_0.txt. CMake requires C++11 and parses project version from `Changelog.txt`. Public headers and CI workflow inspected.
- **Version nuance:** Changelog declares **Release 0.9.0 (2026-10-10)**; latest source commit `8b0970d` bumps version to 0.9.0. GitHub Releases API returned **no release objects**, so this is a source/changelog version claim, not proof of a published GitHub Release artifact.
- **CI:** Upstream 2026-10-10 CI https://github.com/pothosware/SoapySDR/actions/runs/38058033433 passed **36/36** jobs; cross-compile https://github.com/pothosware/SoapySDR/actions/runs/38058033417 passed **15/15**. Workflow includes `ctest`, `SoapySDRUtil --check=null`, null-device creation, Python and LuaJIT binding checks, example-driver build/registration. CI cannot verify real SDR front ends.
- **Reusable code:** `include/SoapySDR/Device.hpp`/ `Device.h` cross-language device APIs; `ConverterRegistry.hpp` sample-format conversion; `Registry.hpp` and `Modules.hpp` plugin loading; `ExampleDriver/` driver reference; `apps/` SoapySDRUtil; `swig/`, `luajit/` bindings.
- **License:** Boost-1.0 root license; keep notices where required. Plugins/vendor SDKs and device firmware have their own license and redistribution constraints.
- **Scoring:** Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4 = **27/30**. Formal GitHub Release absence and hardware test gap keep Maintenance below 5.
- **Ecosystem:** https://github.com/pothosware/SoapyRemote (active 2026-10-10, Boost-1.0, separate remote-device transport); GNU Radio; SatDump; Soapy driver ecosystem.
- **Prior dossier:** `research/2026-09-11-soapysdr-vendor-neutral-sdr-hardware-abstraction.md`.
- **Next:** inspect SoapyRemote access-control defaults and protocol; test converters against known IQ samples; run a controlled physical SDR capture with licensed equipment; verify 0.9.0 distribution/tag status.

## Research provenance and limitations
- GitHub-native metadata, source trees, CI job results, and release/changelog data were read on 2026-10-23. All positive test evidence is **upstream CI**, not GitHub Gold's independent verification.
- Playlist IDs in `sources/youtube_playlists.md` remain seeds; a search for playlist identifiers returned no usable result this pass. No transcript content or YouTube-derived technical claims were invented.
- No upstream code, firmware or assets copied. The canonical master list and machine-readable catalog were updated together; existing entries and scoring rules preserved.
