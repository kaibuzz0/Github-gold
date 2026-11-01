# GitHub Gold research — rio-cogeo and espflash (2026-10-31)

## Method and verification boundary

GitHub-first recursive investigation of the existing Rasterio and ESP32/esptool/esp-hal ecosystems. Inspected upstream README, source files, manifests, licenses, changelogs, CI workflow definitions, releases and individual job conclusions. Two exact-ID web searches for seed playlists `PLMI6SBmd587c` and `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr` returned no indexed transcript evidence. No playlist viewing or transcript-derived attribution. No upstream code was copied. No independent builds, installs, flashing, raster conversions or hardware testing.

## rio-cogeo — VERIFIED / S27 (5+4+5+4+5+4)

- Upstream: https://github.com/cogeotiff/rio-cogeo
- License: BSD-3-Clause, https://github.com/cogeotiff/rio-cogeo/blob/main/LICENSE; separately inspect Rasterio/GDAL native components and input imagery rights.
- Release: [7.0.4, 2026-10-09](https://github.com/cogeotiff/rio-cogeo/releases/tag/7.0.4); changelog fixes no-data COG validation index errors.
- Verified upstream workflow: [2026-10-09 main CI run 37951388263](https://github.com/cogeotiff/rio-cogeo/actions/runs/37951388263) completed **4/4** successful Ubuntu Python 3.11–3.14 pytest jobs. This is upstream evidence, not an independent run.
- Source components: [cogeo.py](https://github.com/cogeotiff/rio-cogeo/blob/main/rio_cogeo/cogeo.py) (`cog_translate`, `cog_validate`, `cog_info`, temporary files, WarpedVRT); [profiles.py](https://github.com/cogeotiff/rio-cogeo/blob/main/rio_cogeo/profiles.py) (compression/tiling); [CLI](https://github.com/cogeotiff/rio-cogeo/blob/main/rio_cogeo/scripts/cli.py) (Rasterio plugin); [validation fixtures](https://github.com/cogeotiff/rio-cogeo/blob/main/tests/test_validate.py) (invalid overviews, sparse and zero-offset rasters).
- [pyproject.toml](https://github.com/cogeotiff/rio-cogeo/blob/main/pyproject.toml) requires Python >=3.11, Rasterio >=1.3.3, morecantile >=5,<8, Pydantic 2.x and Click >=7; `rasterio.rio_plugins` exposes `cogeo`.
- Limitations: CI only Ubuntu; no cloud HTTP range-request test, independent GDAL execution, resource exhaustion assessment or raster round trip. GDAL virtual filesystems can access remote endpoints. A successful local COG layout check does not prove efficient object-storage serving.
- Follow-up: generate tiny fixture GeoTIFF, convert with `cog_translate`, validate with `cog_validate`, inspect overview offsets and remote HTTP range behavior under constrained resources; investigate `developmentseed/morecantile` as a separate catalog candidate.

## espflash — VERIFIED / S28 (5+4+5+4+5+5)

- Upstream: https://github.com/esp-rs/espflash
- License: MIT OR Apache-2.0 ([MIT](https://github.com/esp-rs/espflash/blob/main/LICENSE-MIT), [Apache](https://github.com/esp-rs/espflash/blob/main/LICENSE-APACHE)); bundled bootloaders, flasher stubs and Rust crates need separate provenance/license review.
- Release: [v4.7.0, 2026-10-29](https://github.com/esp-rs/espflash/releases/tag/v4.7.0). [Changelog](https://github.com/esp-rs/espflash/blob/main/CHANGELOG.md) records RISC-V backtrace enhancements, USB serial monitor reconnects, flasher stub updates and QIO bootloader changes.
- Verified upstream workflow: [2026-10-29 merge-group CI run 40885355916](https://github.com/esp-rs/espflash/actions/runs/40885355916) completed **16/16** successful jobs across Linux/macOS/Windows host builds, library/MSRV checks, offline xtask tests, unit tests, Clippy and formatting. The [CI workflow](https://github.com/esp-rs/espflash/blob/main/.github/workflows/ci.yml) excludes main push events. Do not mislabel this as a main-push test.
- [HIL workflow](https://github.com/esp-rs/espflash/blob/main/.github/workflows/hil.yml) defines actual device access via authorized dispatch or merge queue; October 31 pull-request HIL 41151200468 was `action_required`, not evidence of successful flashing. No independently confirmed passing HIL run.
- Source components: [flasher/mod.rs](https://github.com/esp-rs/espflash/blob/main/espflash/src/flasher/mod.rs) (flash modes, size, transfers); `espflash/src/connection/` (serial/bootloader); `target/` (chip metadata); `image_format/` (ELF-to-image); `cargo-espflash/` (Cargo integration); `xtask/` (offline/HIL tests).
- [espflash/Cargo.toml](https://github.com/esp-rs/espflash/blob/main/espflash/Cargo.toml) declares Rust >=1.95.0 and optional serialport/CLI features. Default `update-check` performs a remote version check unless disabled; `serialport` feature is optional for library builds.
- Limitations: hardware functionality not established by host CI; chip-specific ROM protocol, serial permissions and USB enumeration vary. Flash erase/write can destroy device data; bootloader and stub provenance matter. Android/Termux support not demonstrated.
- Follow-up: review release binary provenance and bundled ESP-IDF bootloader/stub notices; verify offline image conversion, serial-port permission behavior and explicit HIL test outcomes. Compare feature gaps with existing `espressif/esptool` and `esp-rs/esp-hal`.

## Maintenance and deduplication

Existing canonical entries `Rasterio` and `Espressif esptool` were cross-linked to the new direct plugin and independent flasher respectively. Existing `esp-hal` already referenced espflash; no redundant update. Checked all 163 existing canonical repository URLs and empty candidate queue before adding. Catalog remains a research index, not a third-party code mirror.
