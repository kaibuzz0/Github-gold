# SoapySDR — vendor-neutral software-defined-radio hardware abstraction

- **Repository:** https://github.com/pothosware/SoapySDR
- **Organization:** Pothosware
- **Category:** SDR / radio hardware abstraction / device drivers / signal-processing infrastructure / interoperability
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **26/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 3/5
- **Primary language:** C++ with C, Python/SWIG, and LuaJIT binding surfaces
- **License:** Boost Software License 1.0
- **Discovery source:** GitHub-first category rotation into SDR/radio infrastructure
- **Inspection date:** 2026-09-11

## Executive finding

SoapySDR is a vendor- and platform-neutral software-defined-radio hardware abstraction layer. Rather than forcing applications to target each SDR vendor SDK independently, it exposes a common device API and a loadable-module model that hardware-specific plugins can implement.

This makes it valuable to GitHub Gold both as a practical interoperability layer and as an architecture reference for plugin-driven hardware abstraction. Its core public surface includes device discovery and construction, channel configuration, sample formats and conversion, streaming, clocks/timing, gain/frequency/sample-rate control, sensors, registers, GPIO, I2C/SPI-style device access where provided, logging, module loading, and capability queries.

The repository also ships `SoapySDRUtil`, bindings, an example driver, unit tests, and CMake integration intended to make third-party driver modules first-class participants rather than private forks of the core library.

## Why it matters

SDR software ecosystems are highly fragmented by hardware vendor, transport, FPGA/firmware stack, driver API, and operating system. A neutral API reduces that coupling.

Operational and research uses include:

- writing one SDR application against a common API rather than individual vendor SDKs;
- swapping or comparing different radio front ends with less application-level code churn;
- exposing vendor hardware through a consistent discovery/configuration/streaming model;
- building portable test tools and radio applications;
- integrating SDR hardware into Python or Lua-based analysis workflows;
- creating out-of-tree hardware plugins without modifying the core project;
- remote or distributed SDR architectures through companion projects such as `pothosware/SoapyRemote`;
- legitimate spectrum monitoring, digital-radio experimentation, RF prototyping, satellite/telemetry work, amateur-radio research, protocol interoperability, and defensive RF analysis.

SoapySDR is infrastructure rather than a full signal-processing application. That distinction is useful: GNU Radio, SDR++, Gqrx, custom DSP pipelines, and other applications can sit above a hardware-neutral layer instead of each reproducing hardware-specific access logic.

## High-value components and patterns

### Device API

`include/SoapySDR/Device.hpp` and the parallel C API in `Device.h` are the central abstraction surfaces.

The API is broad enough to represent heterogeneous SDR hardware while allowing callers to discover what a specific implementation actually supports. Important capability families include:

- device enumeration and construction;
- receive/transmit channel discovery;
- antenna selection;
- frontend correction controls;
- gain and gain-element handling;
- frequency tuning and ranges;
- sample-rate and bandwidth configuration;
- clock/time sources;
- hardware-time access;
- stream setup, activation, read/write and status handling;
- sensors and generic settings;
- register interfaces;
- GPIO and peripheral-style access where supported.

This capability-driven interface is more reusable than assuming every radio exposes identical hardware.

### Loadable driver/module architecture

SoapySDR is designed around loadable hardware modules. The core library performs module discovery and exposes registration/factory machinery so vendor or community drivers can live outside the main repository.

The repository includes `ExampleDriver/`, and current CI actually builds and installs that example module before checking that it registers successfully with `SoapySDRUtil`.

That is strong evidence that third-party driver integration is part of the tested architecture, not merely a documentation claim.

A recursive ecosystem pass should inspect representative modules such as RTL-SDR, HackRF, LimeSDR, SDRplay, Airspy, UHD/USRP, PlutoSDR and other adapters, while treating each module's license and maintenance state independently.

### `SoapySDRUtil`

The repository ships a command-line utility used for environment, module and device inspection.

Current CI executes:

- `SoapySDRUtil --info`;
- a null-driver check;
- null-device construction.

The utility is useful both operationally and as a compact reference for exercising the discovery/factory layer without writing a full SDR application.

### Sample-format conversion registry

The public headers contain converter primitives, converter APIs, format definitions, and a converter registry.

This is a notable reusable subcomponent because SDR devices frequently expose different native integer/complex sample formats than applications want to process. Centralizing conversion registration and lookup prevents every driver/application pair from inventing its own conversion path.

Strong follow-up targets include SIMD behavior, scaling semantics, saturation/rounding behavior, endianness assumptions, and benchmark coverage.

### C and C++ APIs

The repository exposes native C++ interfaces and a substantial C wrapper surface. This improves reuse from languages and runtimes that can interface with a stable C ABI more easily than C++.

The 0.8 series changelog also documents ABI/API-oriented fixes and explicit ABI checking in the Python module.

### Python/SWIG bindings

Python bindings are generated through SWIG. Current CI imports the Python module and exercises API version, ABI version, errors, and null-device construction on Linux, macOS, and supported Windows configurations.

A January 2, 2026 commit specifically fixed SWIG handling of parallel `Device::make()` overloads, showing that the binding layer remains maintained even though formal tagged releases have not kept the same cadence.

### LuaJIT bindings

SoapySDR also contains LuaJIT support. Current Linux, macOS, and Windows CI performs binding-level smoke checks including module loading, version constants, error mapping, and null-device creation.

This is useful evidence of language-binding portability beyond a single Python wrapper.

### CMake package/module support

The root build system installs headers and CMake package helpers and provides utilities for building SoapySDR modules.

The project currently requires C++11 and uses CMake as its primary build/integration system. The root configuration builds the library, apps, tests, docs, SWIG support, and optional LuaJIT integration.

For downstream driver authors, the CMake helper layer is a high-value interoperability component because plugin discovery only works well if third-party modules can be built and installed consistently.

## Working evidence

SoapySDR has strong repository-native working evidence.

### Cross-platform CI

The inspected GitHub Actions workflow builds both Release and Debug configurations across a broad compiler/OS matrix.

Linux coverage includes multiple GCC and Clang versions on Ubuntu 22.04 and 24.04. macOS coverage includes multiple compiler configurations. Windows coverage includes Visual Studio 2022 with 32-bit and 64-bit targets across Windows runner generations.

The workflow does more than compile. It:

1. builds the core project;
2. installs it;
3. runs `ctest --output-on-failure`;
4. executes `SoapySDRUtil` smoke checks;
5. exercises Python bindings;
6. exercises LuaJIT bindings;
7. builds and installs the example driver;
8. verifies module registration.

This is unusually strong upstream evidence for a hardware abstraction library even though CI cannot validate every real SDR device.

### Recent successful workflow run

GitHub Actions metadata inspected for commit `1551ea0d39ce546b32a15808b9b1241018a89fc8` shows the main CI and cross-compile workflows completed successfully on January 2, 2026 after the SWIG overload fix.

GitHub Gold did not execute those workflows itself.

### Null driver

The CI's null-device path is useful because it permits construction, API and module-system checks without physical SDR hardware. It does not prove vendor-specific hardware drivers work, but it makes the core abstraction testable in ordinary CI.

### Example driver

CI builds a separate example driver tree and then verifies that the resulting module is discoverable. This directly tests the extension mechanism that gives SoapySDR much of its reuse value.

## Release and maintenance evidence

The maintenance picture is mixed and should be represented accurately.

The current changelog's newest formal release entry is **0.8.1, dated 2021-07-25**. The GitHub `releases/latest` endpoint returned no current GitHub Release object during this inspection, so GitHub Gold does not claim a newer formal stable release.

However, the repository itself is not abandoned. Recent inspected commits include:

- **2026-01-02** — fix SWIG parallel `Device::make()` overloads;
- **2025-12-27** — replace alternative operator representations;
- **2025-12-13** — remove an obsolete `iso646.h` include;
- **2025-10-14** — CMake install-libdir and macOS rpath fixes;
- **2025-08-30** — SWIG/CMake compatibility work;
- **2025-08-25** — Windows and macOS GitHub Actions updates;
- **2025-05-22** — Ubuntu 24.04 CI updates.

The January 2026 head commit also has successful CI.

This justifies calling the project maintained, but not awarding a 5/5 Maintenance score: there is a significant difference between current source maintenance and a current formal release cadence.

## Ecosystem and recursive value

The Soapy model becomes more valuable when treated as an ecosystem rather than a single repository.

A confirmed companion repository is:

- `pothosware/SoapyRemote` — remote-device support built around the Soapy model.

Additional recursive work should map:

- hardware-specific Soapy modules;
- applications that consume the Soapy API;
- remote/network transports;
- packaging in Linux distributions and SDR suites;
- ABI compatibility across module generations;
- plugin discovery/search-path behavior;
- driver-specific threading and stream semantics.

This ecosystem-level compatibility surface is one of the project's strongest reasons for inclusion.

## Security, safety, and trust boundaries

SoapySDR is a legitimate hardware-abstraction library, but SDR systems can interact with regulated spectrum and externally supplied drivers/devices.

Important boundaries include:

- third-party loadable modules execute native code in the host process;
- vendor SDKs and USB/network device transports have independent trust and update chains;
- malformed device or network-driver data may cross into native C/C++ parsing paths;
- remote SDR use introduces network authentication, exposure and transport-security questions that belong to the companion implementation rather than the core API alone;
- transmit-capable radios must be operated within applicable frequency, power, licensing and equipment rules;
- API-level portability does not imply identical RF behavior, calibration, timestamping, sample loss or latency across hardware;
- a successful null-driver test does not prove a specific hardware plugin is correct.

GitHub Gold catalogs SoapySDR for interoperability, research, defensive RF analysis and lawful radio development. No offensive RF workflow is added by this dossier.

## Reusability assessment

SoapySDR receives **5/5 for Reusability**.

Reasons:

- permissive Boost Software License 1.0;
- clear hardware-neutral API boundary;
- C and C++ interfaces;
- Python and LuaJIT bindings;
- loadable out-of-tree module architecture;
- CMake package helpers;
- example driver;
- null driver for non-hardware testing;
- sample-format conversion subsystem;
- companion network/remote ecosystem.

High-value study/reuse targets include:

1. `include/SoapySDR/Device.hpp` / `Device.h` — device capability abstraction.
2. module registration/factory code — plugin discovery and lifecycle.
3. converter primitives/registry — sample-format conversion infrastructure.
4. `SoapySDRUtil` — environment and device inspection patterns.
5. `ExampleDriver/` — minimum viable third-party module pattern.
6. SWIG Python layer — language binding strategy.
7. LuaJIT layer — lightweight runtime binding strategy.
8. CMake helpers — downstream module integration.
9. null driver/testing machinery — hardware-independent verification.

Prefer linking to upstream components rather than copying them unless a concrete integration requires source reuse.

## License

The project README states that use, modification and distribution are subject to the **Boost Software License, Version 1.0**, with `LICENSE_1_0.txt` at repository root.

The Boost license is permissive and generally favorable for reuse, but third-party hardware modules, vendor SDKs, linked libraries, packaged drivers and companion repositories require separate license review.

No SoapySDR source, binaries, vendor SDKs, driver modules, firmware, RF captures, or third-party code were copied into GitHub Gold in this run.

## Verification performed by GitHub Gold

This run inspected:

- repository metadata and archive state;
- root README;
- root license declaration;
- repository root structure;
- public include/API surface;
- root CMake configuration;
- current GitHub Actions CI definition;
- latest available Actions run metadata;
- changelog and formal release history;
- recent commit history;
- presence of the `ExampleDriver` extension surface;
- companion `pothosware/SoapyRemote` repository;
- GitHub Gold duplicate search for `SoapySDR` before addition.

## Verification not performed

GitHub Gold did **not**:

- build or install SoapySDR locally;
- run `ctest`;
- execute `SoapySDRUtil`;
- import the Python or LuaJIT bindings locally;
- attach or operate physical SDR hardware;
- receive or transmit RF signals;
- build a third-party hardware module;
- benchmark sample conversion or stream throughput;
- test timestamp, overflow, underflow or disconnect behavior;
- test `SoapyRemote`;
- audit third-party driver/module security;
- verify hardware-vendor SDK licenses;
- independently reproduce CI results;
- perform fuzzing or native-memory-safety review.

## Why VERIFIED

VERIFIED means the inspected upstream repository contains concrete, current evidence that the core software works as designed at the abstraction/module level:

- cross-platform Release/Debug builds;
- unit tests executed by CI;
- CLI smoke tests;
- Python binding smoke tests;
- LuaJIT binding smoke tests;
- example-driver build and module-registration test;
- successful January 2026 CI on the current inspected head;
- active maintenance into 2026.

It does **not** mean GitHub Gold independently validated physical-radio behavior or every hardware plugin.

## Score rationale

### Utility — 5/5

A common SDR hardware API is immediately useful for portable radio applications, test systems and heterogeneous SDR environments.

### Working Evidence — 5/5

The CI matrix compiles, installs, runs unit tests, exercises CLI/bindings, and verifies the example module system across Linux, macOS and Windows.

### Reusability — 5/5

Permissive licensing, clear native APIs, language bindings, plugin architecture, CMake helpers and a null/example driver create unusually strong reuse surfaces.

### Novelty — 4/5

Hardware abstraction and plugins are established patterns, but applying them coherently across a fragmented SDR hardware ecosystem remains technically distinctive and high-value.

### Documentation — 4/5

The root README is intentionally sparse, but generated/API documentation, wiki material, public headers, example driver, changelog and build integration provide substantial technical guidance.

### Maintenance — 3/5

Source and CI maintenance continued into January 2026, but the latest formal changelog release remains 0.8.1 from July 25, 2021. The score deliberately distinguishes active maintenance from current release cadence.

## Strongest recursive leads

1. **`pothosware/SoapyRemote`** — remote SDR transport, discovery, trust model, latency and stream semantics.
2. **Hardware-module ecosystem** — compare RTL-SDR, HackRF, LimeSDR, SDRplay, Airspy, UHD/USRP and Pluto-class adapters for maintenance, licensing and capability mapping.
3. **Module loader/factory internals** — ABI versioning, module search paths, unload behavior, duplicate drivers and failure isolation.
4. **Streaming contract** — timeout/overflow/underflow/status behavior, MTU semantics, hardware timestamps and multichannel synchronization.
5. **Converter registry** — supported formats, scaling rules, SIMD paths and correctness/performance testing.
6. **C ABI** — stability, error propagation and suitability for bindings outside SWIG.
7. **Python/Lua bindings** — ownership/lifetime handling, GIL/threading behavior and API parity.
8. **CI cross-compilation** — inspect `.github/workflows/cross-ci.yml` and platform packaging depth.
9. **Application consumers** — identify high-quality projects that use SoapySDR as a portability layer and compare their assumptions.

## Provenance

This dossier is GitHub-first research. The six registered YouTube playlists were not required for this candidate and no video-derived technical claim is used here.

Primary inspected upstream sources:

- https://github.com/pothosware/SoapySDR
- https://github.com/pothosware/SoapySDR/blob/master/README.md
- https://github.com/pothosware/SoapySDR/blob/master/LICENSE_1_0.txt
- https://github.com/pothosware/SoapySDR/blob/master/CMakeLists.txt
- https://github.com/pothosware/SoapySDR/blob/master/Changelog.txt
- https://github.com/pothosware/SoapySDR/blob/master/.github/workflows/ci.yml
- https://github.com/pothosware/SoapySDR/tree/master/include/SoapySDR
- https://github.com/pothosware/SoapySDR/tree/master/ExampleDriver
- https://github.com/pothosware/SoapyRemote

## Next-run recommendation

Recurse one level into `pothosware/SoapyRemote` or a representative Soapy hardware module, then rotate to another underrepresented category such as observability, mapping, accessibility, scientific computing, robotics or emergency communications rather than turning the catalog into an SDR-only list.
