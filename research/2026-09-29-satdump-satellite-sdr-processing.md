# SatDump — satellite SDR reception and data-processing stack

- **Repository:** https://github.com/SatDump/SatDump
- **Organization:** SatDump
- **Category:** SDR / satellite communications / scientific & weather data / offline processing
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- **License:** GPL-3.0
- **Discovery:** GitHub-first breadth rotation from SDR/radio discovery; also surfaced as an upstream decoder/tool in the NyxScope ecosystem. NyxScope itself was not promoted because its main application is proprietary.

## Why it matters

SatDump is a broad, reusable satellite data reception and processing stack rather than a single-purpose decoder. It can process previously recorded baseband/frame/symbol data, perform live reception directly from SDR hardware, and record baseband. It exposes both GUI and CLI operation and has a pipeline-oriented architecture covering many satellite protocols/products.

For Github-gold, its value is the combination of reusable DSP/data-processing components, hardware-source integrations, offline operation, cross-platform builds, satellite-specific pipelines, imagery/product generation, and a mature operational ecosystem.

## Useful surfaces and components

- `satdump pipeline` offline processing path for baseband, frames and soft-symbol inputs.
- Live processing and baseband recording paths.
- SDR abstraction/support spanning RTL-SDR, HackRF, Airspy/AirspyHF, ADALM-Pluto/AD9361-family hardware, bladeRF and other supported sources.
- Pipeline definitions and modules for satellite demodulation, decoding and downstream product generation.
- GUI plus CLI/headless-friendly workflows.
- Optional OpenCL acceleration and VOLK-backed DSP optimization.
- Satellite tracking/autotrack surfaces; recent upstream commits include fixes to CLI autotrack engagement and the autotrack window.
- Build/package machinery for multiple desktop architectures and Android.

## Platform / runtime notes

README build documentation covers Windows, macOS and numerous Linux families. The current GitHub Actions workflow builds Windows x64 and Windows ARM64 artifacts and contains an Android build job; upstream also documents macOS and Linux installation/build paths. Native SDR operation depends on the relevant device libraries/drivers. Optional functionality pulls in additional dependencies such as OpenCL, HDF5, PortAudio and Zstd.

## Evidence inspected

1. **README / operating paths** — upstream documents GUI processing, CLI offline processing, live SDR processing, recording, `sdr_probe`, supported baseband formats, build dependencies and source builds.
2. **Build CI** — `.github/workflows/all_build.yml` is a substantial build workflow. The inspected portion configures/builds Windows x64 and ARM64 with CMake/Ninja, packages installers and portable artifacts, uploads them, and defines an Android build job. This is direct build automation evidence, not merely a platform-support claim.
3. **Release artifacts** — latest non-prerelease GitHub release returned by the Releases API is **1.2.2**, published **2024-11-29**, with macOS Intel/Apple Silicon, Windows x64/ARM64 and Linux package assets. The old numbered stable release should not be confused with project inactivity: default-branch development continued actively in September 2026.
4. **Current maintenance** — inspected default-branch commits include work through **2026-09-21**, including fixes for autotrack CLI engagement/window lag and an invalid-projection overlay crash.
5. **License** — root `LICENSE` is GNU GPL version 3.

## Evidence boundary

`VERIFIED` here means repository-native evidence is strong: substantial source/build structure, documented operational workflows, cross-platform packaging, long-lived release history and current maintenance. Github-gold did **not** compile SatDump, attach SDR hardware, receive a satellite pass, execute a pipeline, reproduce imagery/products, test OpenCL acceleration, exercise autotracking, or independently validate decoder correctness during this pass.

The latest numbered stable GitHub release is older than the current development activity. Users wanting current capabilities should inspect current builds/nightlies and upstream documentation rather than assuming the 2024 stable tag represents the 2026 codebase.

## Licensing / reuse caveat

GPL-3.0 is strong copyleft. No SatDump implementation code was copied into Github-gold. Any later extraction, adaptation or redistribution must preserve GPL obligations. Hardware libraries, optional dependencies, satellite data/products and external datasets can have separate licensing or usage terms and need component-level review.

## Why 28 rather than 30

The project scores very highly on utility, evidence, reusability and maintenance. Two points are held back because the domain combines many established DSP techniques rather than being uniformly novel, and because the README itself points advanced users outward to detailed documentation while the current numbered stable release lags active development.

## Recursive leads

1. Inspect the pipeline/module architecture to identify independently reusable demodulator, decoder and product-generation boundaries.
2. Map supported satellites/protocols against pipeline test/sample evidence rather than treating configuration presence as decoder verification.
3. Inspect Android support and low-resource/off-grid viability.
4. Audit autotrack/rotator integration for portable ground-station use.
5. Inspect ZIQ compressed-IQ recording and whether it is useful as a general SDR archival component.
6. Examine OpenCL acceleration boundaries and CPU fallback behavior.
7. Trace weather-satellite product pipelines (NOAA/Meteor/GOES and related families) and output interoperability with GIS/scientific tooling.

## Steward note

This addition deliberately catalogs the open-source upstream project rather than promoting the proprietary NyxScope application that surfaced it. NyxScope was useful as a lead generator because its README identifies SatDump as an on-demand satellite decoder, but all substantive SatDump claims above were checked against SatDump's own repository-native evidence.