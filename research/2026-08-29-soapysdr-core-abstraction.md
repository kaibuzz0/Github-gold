# SoapySDR core abstraction research — 2026-08-29

## Candidate

- **Repository:** https://github.com/pothosware/SoapySDR
- **Author / Org:** Pothosware / community contributors
- **Category:** SDR / hardware abstraction / plugin architecture / RF interoperability / C++ library
- **Evidence:** VERIFIED
- **Provisional Gold score:** **S / 26**
- **License:** Boost Software License 1.0 (BSL-1.0)
- **Discovery:** recursive follow-up from the SoapyPlutoSDR ↔ libiio interoperability branch

## Executive finding

SoapySDR is the central vendor-neutral abstraction layer behind a large class of software-defined-radio integrations. Its value is architectural: applications can target one common device/control/streaming API while separately loaded driver modules translate that API into vendor- or transport-specific hardware operations.

The repository is therefore not just another SDR utility. It defines a reusable **plugin contract** that lets applications and hardware drivers evolve independently:

`SDR application → SoapySDR Device API → registered driver/module → vendor transport/library → RF hardware`

The previously researched `pothosware/SoapyPlutoSDR` project is a concrete example of this pattern, translating the SoapySDR API into libiio/libad9361 operations for Pluto-class radios.

## Score rationale — 26/30

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Utility | 5 | Provides a common control and streaming abstraction consumed by many SDR applications and hardware plugins. |
| Working evidence | 5 | Mature long-running project with cross-platform CI, unit tests, a null driver, a separately built example driver, bindings tests, and active source maintenance. |
| Reusability | 5 | The public device API, registry, module system, converters, utilities, bindings, and example driver are explicitly designed for reuse. |
| Novelty | 3 | The core idea is an abstraction/plugin layer rather than a novel RF algorithm, but its execution and ecosystem leverage are strong. |
| Documentation | 4 | Public headers are extensively documented and the project maintains wiki/Doxygen-oriented documentation, though the root README itself is intentionally minimal. |
| Maintenance | 4 | Maintenance continued into 2026 and CI targets current Linux/macOS/Windows toolchains, although the changelog's latest formal numbered release remains 0.8.1 from 2021. |

## Core architecture

The public `SoapySDR::Device` class is an abstraction for SDR transceiver configuration and streaming. It exposes static discovery/construction through `enumerate()` and `make()`, device identity queries, channel mapping and capabilities, stream format negotiation, stream setup/activation, RX/TX streaming, and broad hardware-control surfaces such as frequency, gain, antennas, clocks, timing, sensors, settings, GPIO, registers, I2C/SPI/UART-like access where a driver supports them.

The key design property is that applications program against this generic interface while hardware plugins subclass/implement the actual behavior.

This separates:

- application DSP/UI/business logic;
- hardware discovery;
- device construction;
- RF control semantics;
- sample streaming and wire formats;
- vendor libraries and transports.

That separation is one of the strongest reusable ideas in the SDR branch of GitHub Gold.

## Registry and driver factory contract

`include/SoapySDR/Registry.hpp` defines a compact driver-registration API built around two function types:

- a **find function** that returns device-description argument maps;
- a **make function** that constructs a `SoapySDR::Device` implementation.

A `SoapySDR::Registry` object registers those callbacks under a unique driver name together with the required ABI version. The core can then enumerate available registered find/make functions without hard-coding each hardware implementation into the central library.

This is a strong plugin pattern because the discovery result itself is a key/value argument map. Applications can filter by driver, serial, label, transport-specific values, or other implementation-defined keys without needing a new central API for every device family.

The registry/ABI boundary is exactly what projects such as SoapyPlutoSDR use to appear to higher-level applications as normal Soapy devices.

## Device lifecycle and caching

The documented `Device::make()` contract stores constructed device pointers in an internal table so repeated calls with matching arguments can return the same logical device; callers are expected to pair `make()` with `unmake()`.

The API also provides parallel convenience overloads that construct or release lists of devices. A January 2, 2026 upstream commit specifically fixed SWIG handling of the parallel `Device::make()` overloads, showing that this part of the cross-language API remains actively maintained.

This lifecycle model is useful for systems where multiple application components may request a hardware endpoint but should not accidentally instantiate conflicting independent driver objects for the same radio.

## Streaming contract

The stream API is intentionally generic but explicit enough to map onto heterogeneous SDR transports.

Drivers can expose:

- available stream formats;
- a native hardware/wire format;
- stream-specific arguments;
- one or more RX/TX channels;
- full- or half-duplex capability;
- stream setup/activation/deactivation;
- read/write operations;
- timing and status information;
- MTU/direct-buffer behavior where implemented.

The documented sample format syntax includes representations such as `CF32`, `CS16`, `CS12`, `CS4`, `S32`, and `U8`. This allows an application to request a convenient host format while a driver may separately expose a native wire representation.

The API explicitly allows multiple simultaneous TX/RX stream objects in principle while warning that many devices impose stricter hardware limits. Unsupported combinations are expected to fail at setup rather than being silently accepted.

This is an important abstraction discipline: the common API does not pretend every SDR has identical capabilities.

## Hardware capability model

The `Device` interface is broad enough to describe markedly different radios without forcing every implementation to support every operation.

Capabilities cover areas such as:

- RX/TX channel count and frontend mapping;
- antennas;
- DC offset/IQ balance;
- automatic/manual gain and named gain elements;
- frequency components and correction;
- sample rate and bandwidth;
- clock/reference source and rate;
- hardware time and timing sources;
- sensors;
- arbitrary named settings;
- GPIO and register access;
- I2C/SPI/UART-like peripheral access when relevant.

For GitHub Gold this is valuable as a reference for designing **capability-oriented hardware APIs**: the abstraction is wide, but individual drivers can report what they actually implement instead of making unsupported hardware look uniform.

## ExampleDriver as a reusable implementation template

The repository includes an `ExampleDriver/` directory containing:

- `MyDeviceSupport.cpp`;
- a standalone `CMakeLists.txt`;
- a short driver README.

The main CI pipeline builds this example as a separate project, installs it, and then asks `SoapySDRUtil` to check the resulting `my_device` registration.

That is particularly strong working evidence for the plugin boundary: the example is not merely documentation pseudocode; upstream CI treats it as a separately buildable registration/module test.

For reuse, this example is a safer starting point than copying a large production hardware driver because it isolates the minimum module/registration shape.

## `SoapySDRUtil` and null-driver verification surfaces

The project ships `SoapySDRUtil`, which CI exercises with operations including:

- `--info`;
- `--check=null`;
- `--make="driver=null"`.

The null driver provides a hardware-independent path for validating core construction and API behavior without requiring a physical radio on the CI runner.

This is a useful engineering pattern: maintain a deterministic synthetic backend so the abstraction layer, bindings, utilities, and plugin mechanics can be tested separately from USB, network, RF, firmware, or vendor-library availability.

## Cross-platform and binding evidence

The inspected GitHub Actions workflow builds Release and Debug configurations across a large compiler/OS matrix.

Linux coverage includes Ubuntu 22.04 and 24.04 with multiple GCC and Clang versions. macOS jobs cover macOS 14 and 15. Windows coverage includes Visual Studio 2022 x86/x64 builds and a Windows Server 2025 x64 runner configuration.

The workflow runs unit tests with `ctest`, exercises `SoapySDRUtil`, and tests Python 3 and LuaJIT bindings. It also builds and installs the standalone ExampleDriver module described above.

GitHub Gold did not execute these jobs itself. The evidence claim is limited to current upstream CI configuration and repository structure.

## Version/release-state caveat

The current build system derives `SOAPY_SDR_LIBVER` from the first numbered release in `Changelog.txt`. The inspected changelog currently begins with:

- **Release 0.8.1 — 2021-07-25**.

At the same time, the repository has continued receiving source maintenance, including a January 2, 2026 fix for SWIG parallel `Device::make()` overloads.

The GitHub releases API returned no release objects during this pass.

GitHub Gold should therefore distinguish between:

- the formal numbered version represented in the changelog/package ecosystem;
- current `master` development;
- downstream distro packages;
- plugin ABI/API compatibility.

Do not infer a newer formal GitHub release merely from recent commits.

## ABI compatibility is a first-class concern

The registry requires drivers to supply the SoapySDR ABI version when registering. This is important because the architecture depends on dynamically loaded modules crossing a C++ library boundary.

For GitHub Gold, the reusable lesson is that plugin systems should make binary compatibility explicit instead of assuming arbitrary modules built against different library generations are safe to load together.

This concern is also visible in the project's build, version-reporting, module-search, and bindings machinery.

## License

The root README and source headers identify the project as **Boost Software License 1.0 (BSL-1.0)**.

This is a permissive license and substantially easier to reuse than copyleft driver components elsewhere in the SDR stack. However, drivers loaded by SoapySDR can and do carry their own licenses, so reuse of a specific hardware plugin must be reviewed separately.

No third-party source code was copied into GitHub Gold in this pass.

## Verification performed by GitHub Gold

Inspected:

- repository metadata and current `master` tree;
- root README and BSL-1.0 declaration;
- `Device.hpp` public device/stream abstraction;
- `Registry.hpp` driver registration contract;
- `CMakeLists.txt` version/build handling;
- `Changelog.txt` formal version history;
- current GitHub Actions CI matrix;
- ExampleDriver directory structure;
- recent commit history;
- GitHub releases collection.

Not performed:

- no local build;
- no installation;
- no physical SDR enumeration;
- no driver-module loading outside upstream evidence;
- no RX/TX streaming test;
- no throughput/latency benchmark;
- no GNU Radio, SDR++, OpenWebRX, SDRangel, or other application integration test;
- no ABI compatibility experiment across multiple SoapySDR package versions.

## Why it belongs in GitHub Gold

SoapySDR is high-value because it is both a functioning SDR infrastructure project and a reusable architecture reference.

Particularly useful components/patterns include:

1. the generic `Device` capability interface;
2. find/make registry callbacks;
3. ABI-tagged dynamic driver registration;
4. key/value discovery and construction arguments;
5. host-vs-native stream format negotiation;
6. explicit capability querying rather than pretending all hardware is equivalent;
7. the null driver for hardware-independent validation;
8. `SoapySDRUtil` as a generic inspection/probe utility;
9. ExampleDriver as a minimal separately buildable plugin template;
10. Python and LuaJIT bindings over the same core device abstraction.

The project also turns the previous SoapyPlutoSDR dossier into a clearer ecosystem map:

`GNU Radio / SDR application → SoapySDR → SoapyPlutoSDR → libiio / libad9361 → Pluto hardware`

## Caveats

- The latest formal version visible at the top of the inspected changelog is 0.8.1 from 2021 even though source maintenance continued through 2026.
- The GitHub releases collection returned no release objects.
- Cross-platform CI demonstrates upstream build/test intent and automation, not GitHub Gold's own runtime verification.
- A broad abstraction inevitably exposes optional methods that individual hardware drivers may not implement uniformly; applications must query capabilities and handle unsupported operations.
- Plugin license and maintenance quality vary independently of the permissively licensed SoapySDR core.

## Recursive ecosystem leads

Strong next targets:

1. **GNU Radio `gr-soapy` / Soapy blocks** — verify the application-facing end of the abstraction and map a full flowgraph-to-driver data path.
2. **analogdevicesinc/libad9361-iio** — isolate the AD9361-specific RF helper layer used alongside libiio.
3. **SoapyRemote** — inspect how Soapy's device abstraction is transported across networks and identify trust/authentication boundaries.
4. **SoapyRTLSDR / SoapyHackRF / LimeSuite integration** — compare how very different radio stacks implement the same device contract.
5. **Pothosware module ecosystem** — identify additional compact plugins/utilities with high reuse value.
6. **ABI/module loading internals** — trace search paths, dynamic loading, unload behavior, and failure isolation.

## Promotion recommendation

**VERIFIED / provisional S / 26.**

SoapySDR meets the quality bar as a mature, permissively licensed, cross-platform hardware-abstraction library with concrete test/CI evidence and a large reusable API surface. Preserve the release-state caveat and distinguish upstream CI evidence from local hardware verification.