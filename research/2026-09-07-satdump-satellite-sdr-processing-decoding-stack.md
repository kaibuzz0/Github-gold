# SatDump — satellite SDR processing and decoding stack

- **Repository:** https://github.com/SatDump/SatDump
- **Organization:** SatDump
- **Category:** SDR / satellite communications / scientific data processing / remote sensing
- **Evidence:** VERIFIED
- **Provisional Gold score:** **27/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 4/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 4/5
- **Primary license:** GPL-3.0
- **Discovery source:** GitHub-first independent discovery; no YouTube-derived technical claims used in this pass.

## What it is

SatDump is a general-purpose satellite data processing application and toolkit. It accepts recorded baseband/IQ, frames, or soft-symbol inputs, can acquire signals live from supported SDR hardware, and processes them through satellite-specific pipelines. Upstream exposes both GUI and CLI workflows.

The README documents offline pipeline processing, live SDR processing, baseband recording, selectable input levels and formats, and an `sdr_probe` command for enumerating SDR devices. The documented Linux build supports optional RTL-SDR, HackRF, Airspy/AirspyHF, AD9361/libiio devices, bladeRF, UHD, LimeSuite, OpenCL acceleration, HDF5, and other integrations.

## Why it matters

SatDump joins several layers that are often split across independent tools:

1. SDR device acquisition;
2. baseband/DSP processing;
3. modulation/demodulation and framing pipelines;
4. satellite/protocol-specific decoding;
5. image/product handling;
6. orbit/tracking-related infrastructure;
7. GUI visualization and CLI automation.

That makes it valuable not only as an end-user satellite decoder but also as an architecture/reference source for building reusable scientific SDR and telemetry systems.

## Reusable component surfaces

Current `src-core/` structure visibly separates major reusable concerns including:

- `dsp/` — DSP primitives and processing infrastructure;
- `image/` — image/product handling;
- `db/` — local data/database functionality;
- `core/` and `common/` — shared runtime infrastructure;
- `handlers/` — processing/event handling;
- `angelscript/` — scripting integration;
- `explorer/` — inspection/exploration functionality;
- `libs/` — embedded/support libraries.

The plugin/pipeline structure further separates satellite- and protocol-specific implementations from the common processing runtime. For GitHub Gold, the strongest component-level research targets are the pipeline execution model, DSP blocks, SDR source abstraction, framing/FEC/decoder modules, image/product processors, and orbit/tracking code.

## Platform and build evidence

The current GitHub Actions workflow performs release builds across a broad platform matrix:

- Windows x64;
- Windows ARM64;
- Android;
- Ubuntu 22.04;
- Ubuntu 24.04;
- Linux ARM64;
- macOS Intel;
- macOS Apple Silicon.

The workflow creates Windows installers and portable packages, Android APK artifacts, Ubuntu packages/AppImage output, ARM64 Linux packages, and macOS disk images. The nightly-release stage depends on the successful completion of all listed platform builds.

This is strong reproducible-build evidence, but the inspected workflow is primarily build/package validation rather than an extensive explicit unit/integration test suite. GitHub Gold therefore assigns **Working Evidence 4/5 rather than 5/5**.

## Maintenance evidence

The default `master` branch remained active through **2026-09-05**, including merges from the development branch and packaging/desktop integration work. The project is therefore actively maintained at the time of inspection.

The latest formal stable GitHub Release returned by the repository API is **1.2.2, published 2024-11-29**. It includes packaged macOS, Windows x64/ARM64, and Linux artifacts. Those older release assets do not expose GitHub digest metadata in the inspected API response, so no cryptographic artifact-verification claim is made.

The repository also maintains an automated nightly release/build flow on current `master`; formal stable-release age should therefore not be interpreted as repository inactivity.

## License and reuse boundary

The root `LICENSE` is **GNU GPL version 3**.

That permits inspection and reuse under GPL terms, but GitHub Gold should not lift arbitrary SatDump source into permissively licensed projects without understanding GPL compatibility and any separately licensed bundled dependencies/assets. This dossier catalogs the architecture and useful components; **no SatDump source code was copied**.

## Supply-chain caveats

The inspected workflow uses mutable major-version Action references such as `actions/checkout@v4`, `actions/cache@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4` rather than immutable commit-SHA pinning.

The Windows build also downloads an external Aaronia RTSA installer from `satdump.org` during CI. The inspected section did not show an explicit pinned checksum verification step before installation. That does not make the project unsafe, but it is a supply-chain-hardening opportunity worth recording.

## Verification performed

GitHub Gold inspected:

- the current README and documented GUI/CLI/live/recording workflows;
- platform and SDR dependency/build instructions;
- current `src-core` architecture/directory layout;
- the current all-platform GitHub Actions build workflow;
- root GPL-3.0 license text;
- latest formal GitHub Release metadata;
- recent `master` commit activity.

## Verification boundary

GitHub Gold **did not**:

- build or install SatDump;
- run it on desktop or Android;
- execute a satellite pipeline;
- connect an SDR;
- record or demodulate RF;
- decode satellite telemetry/images;
- independently validate protocol correctness;
- reproduce OpenCL acceleration behavior;
- test orbit prediction/tracking;
- run fuzzing or malformed-frame tests;
- independently hash release/nightly artifacts;
- perform a security, RF, or scientific-accuracy audit.

Upstream build automation and documentation are treated as upstream evidence, not as local verification.

## Gold assessment

**VERIFIED — provisional S / 27.**

SatDump has unusually high utility and novelty because it combines SDR acquisition, DSP, protocol decoding, satellite-specific processing, scientific product generation, GUI workflows, CLI automation, and broad platform support in one actively maintained codebase. Reuse potential is strong at the component and architecture level.

The score is held below 28–29 mainly because the inspected CI evidence is dominated by compilation/packaging rather than a clearly visible broad automated correctness-test suite, the latest formal stable GitHub release is old relative to current development, and supply-chain pinning can be improved.

## Recursive research leads

1. Inspect `src-core/dsp/` for reusable DSP block/threading/buffer architecture.
2. Map the SDR source abstraction and compare it with SoapySDR/libiio already cataloged by GitHub Gold.
3. Trace one complete satellite pipeline from baseband input through demodulation, synchronization/FEC, framing, telemetry decoding, and product/image output.
4. Inspect CCSDS-related framing/FEC implementations as standards/interoperability reference components.
5. Inspect orbit propagation, pass prediction, Doppler compensation, and rotator/tracking integration.
6. Review malformed-frame/image/product parsing boundaries for fuzzing opportunities.
7. Inspect the Android architecture and USB-SDR integration for portable offline field use.
8. Compare SatDump's direct SDR drivers with its network/source interfaces and determine whether SoapySDR can serve as a cleaner interoperability layer.
9. Review nightly artifact publication and external dependency acquisition for checksum/signature hardening.
10. Follow protocol/satellite-specific plugins into independent reusable decoder libraries where licensing and architecture permit.
