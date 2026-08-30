# libad9361-iio — AD936x RF helper layer above libiio

- **Repository:** https://github.com/analogdevicesinc/libad9361-iio
- **Author / Org:** Analog Devices
- **Category:** SDR / RF / AD9361 / libiio / filter design / multi-chip synchronization
- **Evidence:** VERIFIED
- **Provisional Gold score:** 24 / 30
- **Provisional tier:** A
- **License:** LGPL-2.1-or-later for the inspected library/header source
- **Discovery source:** Recursive follow-up from libiio → SoapyPlutoSDR → SoapySDR research
- **Inspection date:** 2026-08-30

## Executive assessment

`libad9361-iio` is a focused userspace helper library for AD936x-class RF hardware that sits above libiio. It is not a generic SDR abstraction like SoapySDR and it is not the transport/device-discovery layer supplied by libiio. Its value is the RF-specific logic it packages: AD9361 clock-chain calculations, baseband-rate configuration, FIR generation, multi-chip synchronization, and FMCOMMS5 phase synchronization.

The project remains technically useful and is still maintained in 2026, but it currently has an important ecosystem boundary: the upstream README states that `main` does not support libiio's v1.0 API and directs users who need a buildable combination to the `libad9361-iio-v0` branch together with libiio v0.x. This prevents treating current `main` as a drop-in helper for the newest libiio architecture.

**Provisional classification: VERIFIED — A / 24.**

## Why it matters

The repository isolates several pieces of RF-specific engineering that otherwise have to be reimplemented in every AD936x host application:

1. AD9361/AD936x programmable FIR design and tap generation;
2. baseband sample-rate selection and associated analog/digital filter configuration;
3. RX/TX RF clock-chain calculation;
4. multi-chip synchronization of master/slave AD9361 devices;
5. FMCOMMS5-specific multi-chip and phase synchronization;
6. a small public C API suitable for reuse by higher layers such as SDR applications and hardware plugins.

This makes the project a useful example of a **hardware-family helper layer** between a generic I/O substrate (`libiio`) and application/device adapters such as SoapyPlutoSDR.

## Public API surfaces inspected

The current `ad9361.h` exposes the following notable operations:

- `ad9361_multichip_sync()` — master/slave multi-chip synchronization;
- `ad9361_fmcomms5_multichip_sync()` — FMCOMMS5-specific MCS helper;
- `ad9361_set_bb_rate()` — baseband-rate configuration using generic filters;
- `ad9361_set_trx_fir_enable()` / `ad9361_get_trx_fir_enable()` — simultaneous TX/RX FIR control;
- `ad9361_generate_fir_taps()` — generate programmable FIR coefficients from filter-design criteria;
- `ad9361_calculate_rf_clock_chain()` — calculate the RX/TX clock path for a requested sample rate;
- `ad9361_calculate_rf_clock_chain_fdp()` — derive clock-chain and default filter-design parameters;
- `ad9361_set_bb_rate_custom_filter_auto()` — automatically generate/filter a requested baseband rate;
- `ad9361_set_bb_rate_custom_filter_manual()` — apply manual pass/stop/bandwidth constraints;
- `ad9361_fmcomms5_phase_sync()` — synchronize TX/RX channel phases on FMCOMMS5.

The public filter-design structure contains parameters for data rate, pass/stop edges, FIR decimation/interpolation, half-band stages, converter and PLL rates, passband ripple, stopband attenuation, analog RF bandwidth, maximum tap count, and phase-equalization behavior.

Upstream source:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361.h

## Exact reusable components

### `ad9361_design_taps.c`

Implements the AD936x-specific FIR design path used to produce programmable filter taps from higher-level design parameters.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361_design_taps.c

### `filterdesigner/`

Contains the lower-level filter-design implementation used by the public tap-generation API. This subtree is worth separate algorithm-level review before any extraction or adaptation.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/tree/main/filterdesigner

### `ad9361_calculate_rf_clock_chain.c`

Calculates the AD9361 RX/TX clock chain for a requested sample rate and feeds the automatic filter/rate path.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361_calculate_rf_clock_chain.c

### `ad9361_baseband_auto_rate.c`

Provides baseband-rate configuration logic and coordinates the generated FIR/rate configuration with the libiio-facing AD9361 device.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361_baseband_auto_rate.c

### `ad9361_multichip_sync.c`

Encapsulates AD9361 multi-device synchronization and optional sample-rate/interface-timing checks.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361_multichip_sync.c

### `ad9361_fmcomms5_phase_sync.c`

FMCOMMS5-specific synchronization/calibration helper. The public API documents that synchronization can be invalidated when LO frequency, sample rate, or gain is changed. It also documents side effects during calibration, so callers must treat this as stateful hardware configuration rather than a pure calculation routine.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/ad9361_fmcomms5_phase_sync.c

## Tests and working evidence

The top-level CMake configuration enables tests by default (`BUILD_TESTS=ON`) and adds the `test/` subtree. The current test configuration defines:

- `FilterDesignerTest`
- `GenerateRatesTest`
- `FilterDesignerHardwareTest`
- `FMComms5SyncTest`
- `AutoRateTest`

This is meaningful evidence because the project contains both hardware-independent algorithm/rate tests and hardware-oriented integration tests. However, GitHub Gold did **not** execute these tests and does not claim that the hardware-oriented tests currently pass against every supported board/firmware combination.

The test directory also carries known tap/reference files for several RX/TX rates, providing fixtures for filter/rate validation.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/test/CMakeLists.txt
- https://github.com/analogdevicesinc/libad9361-iio/tree/main/test

## Build and binding surfaces

The current CMake project identifies the library development version as **0.4** and builds a shared `ad9361` library from the synchronization, baseband-rate, filter-design, clock-chain, and FMCOMMS5 sources plus the filter designer subtree.

Optional Python and MATLAB binding directories are present. The current source tree also contains packaging and CI infrastructure for multiple platforms.

Upstream:
- https://github.com/analogdevicesinc/libad9361-iio/blob/main/CMakeLists.txt
- https://github.com/analogdevicesinc/libad9361-iio/tree/main/bindings

## Maintenance and release evidence

The repository is not archived. The current `main` head inspected for this run is commit `aae5a07da3676ed8f359d3a6cef982f508aba598` from **2026-07-29**, which fixes Doxygen/Sphinx documentation build warnings and updates CMake minimum-version compatibility. Additional 2026 commits include Python-binding CMake compatibility work and a source version increase to 0.4.

The most recent formal GitHub release located is **v0.3**, published **2023-05-25**, with packaged artifacts for several Ubuntu architectures and macOS. Therefore source maintenance is much newer than the latest formal release.

This release/source gap should remain explicit.

## Critical compatibility caveat: libiio v1

The upstream README currently states:

- `main` does **not** support the new libiio v1.0 API;
- users wanting to build libad9361-iio should use the `libad9361-iio-v0` branch;
- that branch is intended for libiio's v0.x API (`libiio-v0`).

This is the most important operational caveat found during this pass. The wider GitHub Gold SDR research has already established that current libiio `main` is developing the 1.x architecture. Consequently, this repository presently represents an **API-generation split** in the stack rather than a clean current-main-to-current-main dependency chain.

Do not document the chain as:

`current libad9361-iio main → current libiio v1 main`

without additional upstream changes or evidence.

## Architecture position in the researched SDR stack

The work completed so far now resolves these layers:

`GNU Radio`

→ `gr-soapy` application adapter

→ `SoapySDR` generic SDR device API

→ `SoapyPlutoSDR` Pluto-specific Soapy plugin

→ `libiio` generic Industrial I/O transport/device abstraction

→ `libad9361-iio` **AD936x RF-specific helper algorithms and synchronization** (where used, subject to the current libiio API-generation compatibility caveat)

→ AD9361-class RF hardware / FPGA / kernel IIO drivers

This distinction matters: `libad9361-iio` is not the hardware transport. It is the RF-family helper logic layered around libiio-visible devices.

## License boundary

The inspected public header explicitly states **GNU Lesser General Public License version 2.1 or, at the user's option, any later version**. The root repository also carries `LICENSE` / `COPYING.txt` license material.

No third-party source was copied into GitHub Gold during this run. Before adapting any individual file, re-check its own header and the licenses of relevant dependencies.

## Provisional Gold scoring

| Axis | Score | Rationale |
| --- | ---: | --- |
| Utility | 4/5 | Valuable for AD936x applications but hardware-family-specific. |
| Working evidence | 4/5 | CMake/CTest test surfaces, hardware tests, packaged historical release, and maintained source. |
| Reusability | 4/5 | Small C API and separable algorithms; currently constrained by libiio API generation. |
| Novelty | 4/5 | Useful specialized RF clock/filter/synchronization logic. |
| Documentation | 4/5 | Public Doxygen API, README, comments, examples/tests; compatibility state is explicitly documented. |
| Maintenance | 4/5 | Active 2026 source maintenance, but latest formal release located is from 2023 and v1 libiio support is unresolved on `main`. |
| **Total** | **24/30** | **A** |

## Verification boundary

GitHub Gold inspected repository-native README material, public headers, source-tree organization, CMake configuration, tests, current commits, release metadata, and licensing statements.

GitHub Gold did **not**:

- build the library;
- execute CTest;
- connect AD9361 hardware;
- execute FMCOMMS5 synchronization;
- generate or measure FIR frequency responses;
- validate clock chains on hardware;
- test libiio v0/v1 interoperability;
- validate Python or MATLAB bindings;
- perform RF phase/noise/throughput measurements.

Any claim stronger than the inspected upstream evidence should remain deferred until one of those actions is actually performed.

## Strong follow-up leads

1. Inspect `filterdesigner/` at algorithm level and identify whether it is broadly reusable outside the AD936x wrapper.
2. Inspect the `libad9361-iio-v0` branch versus `main` to determine exactly where current development diverged.
3. Search open issues/PRs for libiio v1 migration status rather than assuming the incompatibility will persist.
4. Trace SoapyPlutoSDR's optional libad9361 use to the exact API calls and features it gains when the dependency is present.
5. Compare AD936x helper functionality with `pyadi-iio` to distinguish low-level reusable algorithms from high-level convenience APIs.
6. Monitor for a formal 0.4 release or a libiio-v1-compatible branch before promoting above A-tier.
