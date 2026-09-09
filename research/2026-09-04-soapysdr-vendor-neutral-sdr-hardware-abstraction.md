# SoapySDR — vendor-neutral SDR hardware abstraction and plugin runtime

- Upstream: https://github.com/pothosware/SoapySDR
- Project: SoapySDR
- Research date: 2026-09-04
- Category: SDR / radio hardware abstraction / device drivers / interoperability / native library
- Evidence level: VERIFIED
- Provisional Gold score: S / 27
- License: Boost Software License 1.0 (BSL-1.0)
- Primary language: C++ with C API plus SWIG Python bindings and LuaJIT support
- Platforms evidenced in CI: Linux, macOS, Windows
- Discovery source: recursive follow-up from the rtl_433 dossier; GitHub-first verification

## Executive finding

`pothosware/SoapySDR` is a vendor- and platform-neutral software-defined-radio support library. Its main value is not a single radio implementation but a stable abstraction boundary between SDR applications and hardware-specific driver modules.

The inspected public API exposes device enumeration and construction, RX/TX channel discovery, stream-format negotiation, stream setup and operation, frequency/sample-rate/bandwidth/gain controls, clocks, time sources, sensors, settings, GPIO/register/I2C/SPI/UART-style device surfaces, and other capabilities through one common `SoapySDR::Device` interface.

A separate registry API lets dynamically loaded hardware modules register find/make functions under an ABI version. This is the core architectural Gold: applications can target one hardware-neutral interface while vendors and community projects supply independent modules for actual radios.

This is directly relevant to the preceding `rtl_433` research. rtl_433 can use SoapySDR as a hardware-access layer, allowing its protocol-analysis and decoding pipeline to operate beyond a single RTL-SDR backend.

## Why it matters

SDR software often faces a fragmented hardware ecosystem. Individual radios expose different vendor APIs, sample formats, tuning models, clock capabilities, channel counts, driver lifecycles, and platform constraints.

SoapySDR centralizes that variability behind an extensible driver ABI. The reusable design pattern is:

**application -> stable device/stream API -> runtime registry/module loader -> hardware-specific driver -> SDR hardware**

This makes it useful as:

- a common hardware abstraction for radio applications;
- a plugin architecture reference for native C/C++ systems;
- an interoperability layer for software such as rtl_433 and other SDR tools;
- a basis for testing applications against a null/example driver without physical hardware;
- a bridge into Python and LuaJIT while retaining a C++ core and C ABI.

## Core device abstraction

`include/SoapySDR/Device.hpp` defines the main transceiver abstraction.

The inspected interface includes static device enumeration and construction APIs:

- `Device::enumerate()`
- `Device::make()`
- `Device::unmake()`

Construction uses key/value argument dictionaries or markup strings. The implementation contract stores constructed devices in a table so repeated `make()` calls with the same arguments can resolve to the same device, with matched `unmake()` lifecycle calls expected.

The API also exposes parallel construction/destruction helpers that accept lists of device arguments. Upstream describes these as convenience parallel-for operations over `make()` and `unmake()`.

The current head commit inspected on 2026-09-04 is specifically a fix for SWIG handling of these parallel `Device::make()` overloads, showing that the multi-device API remains maintained even though the formal release cadence is slow.

## Streaming abstraction

The `Device` interface abstracts sample streaming separately from hardware discovery.

The inspected API exposes:

- available stream formats;
- native hardware stream format and full-scale value;
- stream argument metadata;
- setup of RX or TX streams;
- support for multi-channel streams;
- explicit format strings identifying complex/real and integer/floating-point sample representations.

The interface contract notes that multiple TX/RX streams are permitted by the API, while individual devices may impose stricter hardware limits. Unsupported combinations are expected to fail at the implementation boundary rather than forcing every application to know the hardware-specific topology in advance.

This is an important abstraction property: **capability discovery and error reporting remain part of the device contract rather than being hidden in per-application vendor branches.**

## Device identity and capability discovery

The interface distinguishes:

- driver identity (`getDriverKey()`);
- hardware identity (`getHardwareKey()`);
- arbitrary hardware metadata (`getHardwareInfo()`);
- channel count and channel metadata;
- duplex capability.

This allows applications to remain generic while still exposing hardware-specific information when useful.

## Plugin / registry architecture

`include/SoapySDR/Registry.hpp` defines a compact hardware-driver registration surface.

A module supplies:

- a `FindFunction` returning matching hardware descriptors;
- a `MakeFunction` constructing a `Device` implementation;
- a unique driver/module name;
- the ABI version expected by the registration object.

`SoapySDR::Registry` adds those functions to the global registry and removes the entry during cleanup. Static methods expose the currently loaded find/make function maps.

The constructor contract explicitly says the supplied ABI value must match `SOAPY_SDR_ABI_VERSION`.

This is one of the strongest reusable components in the repository because it separates four concerns cleanly:

1. hardware discovery;
2. hardware object construction;
3. application-facing API compatibility;
4. runtime module registration.

## Example driver as integration evidence

The repository contains an `ExampleDriver/` project rather than documenting the driver ABI only in prose.

Current CI builds SoapySDR, installs it, separately configures/builds the example driver as an external module, installs that module, and then runs:

`SoapySDRUtil --check=my_device`

That is valuable evidence that the module API is intended to be consumed independently rather than only by drivers built into the main source tree.

## Null-device test surface

CI also invokes:

- `SoapySDRUtil --info`
- `SoapySDRUtil --check=null`
- `SoapySDRUtil --make="driver=null"`

The null driver gives application/library tests a hardware-independent construction path. This is especially useful for projects that want to test discovery, bindings, object lifecycle, or general API integration in CI where physical SDR hardware is unavailable.

## Language bindings

The repository has SWIG and LuaJIT integration in addition to its C++ API.

Current CI exercises Python bindings by importing `SoapySDR`, reading API/ABI/error constants, converting error codes, and constructing a null device.

The same workflow separately loads the LuaJIT module, checks API/ABI/error values, and constructs a null device.

This is stronger evidence than merely shipping generated binding files: the bindings are exercised after the native library is built and installed.

## Cross-platform working evidence

The inspected `.github/workflows/ci.yml` runs both Debug and Release configurations.

### Linux

The matrix covers Ubuntu 22.04 and 24.04 across multiple GCC and Clang toolchains, including GCC 10-14 and Clang 13-18 in the current workflow.

For each configuration it:

- configures and builds SoapySDR with CMake;
- installs the library;
- runs `ctest --output-on-failure`;
- executes SoapySDRUtil against the null driver;
- exercises Python bindings;
- exercises LuaJIT bindings;
- independently builds/installs/tests the example driver module.

### macOS

The workflow covers macOS 14 and 15 with GCC/Clang configurations and repeats the build/install/unit-test/utility/bindings/example-driver checks.

### Windows

The workflow covers Visual Studio 2022 x86/x64 builds and Windows 2025 x64 in Debug and Release combinations. It installs the project, runs CTest, exercises SoapySDRUtil, tests Python bindings where enabled, and tests LuaJIT integration.

The breadth of this matrix is a major positive working-evidence signal.

## CI supply-chain caveat

The inspected workflow still uses mutable major-version GitHub Action references such as:

- `actions/checkout@v2`
- `actions/setup-python@v4`
- `ilammy/msvc-dev-cmd@v1`

It also clones LuaJIT and luaunit branches/tags during jobs rather than pinning every dependency to immutable commit SHAs.

This is a supply-chain hygiene weakness compared with the strongest repositories already cataloged in GitHub Gold. It does not invalidate the functional test evidence, but it reduces confidence in CI reproducibility/provenance and is part of the reason this dossier is not scored 29/30.

## Release and maintenance status

This repository has a notable split between formal releases and source maintenance.

The GitHub Releases page currently reports no GitHub Releases. The checked-in `Changelog.txt` identifies the latest formal release documented there as:

- **0.8.1 — 2021-07-25**

That is materially stale as a release boundary.

However, the source repository itself is not abandoned. The latest commit found during this inspection is:

- **2026-01-02 — `Fix SWIG parallel Device::make() overloads (#474)`**

Other late-2025 commits include compiler/portability and CMake fixes.

Therefore the maintenance assessment is deliberately split:

- active-enough source maintenance and current CI configuration;
- weak formal release/tag cadence and an open 2025 request for a newer release tag.

This costs points in the Maintenance and Working Evidence dimensions despite the architecture being mature and widely reusable.

## Versioning caveat

The lack of a recent formal release means downstream projects may consume distro snapshots, PothosSDR distributions, package-manager builds, or source commits that differ materially from the 0.8.1 changelog boundary.

For catalog consumers, the important rule is: **record the exact SoapySDR ABI/package/source revision used by a driver or application rather than assuming “SoapySDR 0.8.x” describes the current source tree.**

This matters because hardware modules are ABI-sensitive by design.

## Ecosystem significance

SoapySDR's value compounds through external modules.

Strong recursive leads include:

- `pothosware/SoapyRemote` — network-accessible SDR hardware through the Soapy API;
- `pothosware/SoapyMultiSDR` — wraps multiple supported devices as one logical device;
- vendor/device modules such as RTL-SDR, HackRF, LimeSDR, Airspy/HydraSDR, bladeRF and SDRplay bridges;
- applications such as rtl_433 that can use SoapySDR as one of several radio backends.

Each external module must be evaluated separately for maintenance, licensing, driver quality and device-specific limitations. SoapySDR being sound does not automatically make every plugin equally reliable.

## Licensing

The repository README explicitly identifies the project license as the Boost Software License, Version 1.0.

`LICENSE_1_0.txt` grants use, reproduction, distribution, execution, transmission and derivative-work rights subject to retaining the copyright notices and license statement in source/distributed covered material, with the license's executable-object exception.

Inspected public headers also carry `SPDX-License-Identifier: BSL-1.0`.

No upstream SoapySDR source was copied into GitHub Gold.

## Gold score

Provisional score: **27 / 30 — S tier**

- Utility: **5/5** — solves a fundamental hardware-fragmentation problem for SDR applications.
- Working Evidence: **5/5** — broad multi-OS CI, unit tests, utility checks, bindings checks and an external example-driver integration test.
- Reusability: **5/5** — purpose-built library/API/plugin boundary with C++, C, Python and LuaJIT surfaces.
- Novelty: **4/5** — hardware abstraction is a known pattern, but the breadth of SDR-driver interoperability and runtime module ABI is unusually useful.
- Documentation: **4/5** — public headers are heavily documented and a wiki exists, but the minimal root README and stale release documentation reduce clarity.
- Maintenance: **4/5** — meaningful source maintenance reached 2026-01-02 and the CI matrix targets current operating systems/toolchains, but the latest documented formal release is still 0.8.1 from 2021 and no GitHub Releases are published.

## Verification performed in this run

Inspected directly:

- repository metadata and current default branch;
- root README;
- Boost license file;
- `include/SoapySDR/Device.hpp`;
- `include/SoapySDR/Registry.hpp`;
- `.github/workflows/ci.yml`;
- `Changelog.txt`;
- recent commit history;
- GitHub release-page state.

Correlated the project with the previous rtl_433 dossier as a recursive SDR ecosystem lead.

## Verification boundary

I did **not**:

- build or install SoapySDR;
- run CTest;
- execute `SoapySDRUtil`;
- load or enumerate physical radio hardware;
- validate RX/TX streaming;
- test frequency/sample-rate/gain controls;
- compile an independent third-party driver against the ABI;
- execute the example or null driver locally;
- test Python or LuaJIT bindings;
- test Windows/macOS/Linux packages;
- inspect every device-control method in `Device.hpp`;
- audit dynamic-loader safety;
- fuzz driver arguments or stream buffers;
- verify every external Soapy module;
- independently reproduce CI results;
- conduct a security audit.

All claims above are limited to direct source/workflow/documentation inspection or clearly identified upstream evidence.

## Risks and limitations

- A vendor-neutral API cannot eliminate bugs or unsafe behavior in third-party hardware modules.
- Hardware capability semantics still vary; applications must query capabilities and handle unsupported combinations.
- ABI-sensitive driver modules require careful version alignment.
- A stalled vendor API can still block inside a driver even when the Soapy layer itself is sound.
- Formal release cadence is weak relative to ongoing source changes.
- Current CI dependency/action pinning is weaker than ideal for software-supply-chain reproducibility.
- Physical-radio behavior cannot be inferred solely from null-driver and CI success.

## Strongest follow-up leads

1. **SoapyRemote** — determine whether the network protocol, discovery, authentication/trust assumptions and stream transport deserve a separate Gold dossier.
2. **SoapyMultiSDR** — inspect multi-radio aggregation, synchronized streaming assumptions and failure isolation.
3. Trace `Device::make()` through enumeration, registry selection, module loading and object caching.
4. Inspect the module loader's ABI/version rejection behavior and search-path controls.
5. Map sample-format conversion infrastructure and identify reusable converter-registry components.
6. Verify how rtl_433 constructs/configures its SoapySDR source and where radio-specific settings cross the abstraction boundary.
7. Compare SoapySDR's plugin/ABI model against GNU Radio's hardware-source integrations and newer SDR abstraction layers.

## Steward verdict

**Keep as VERIFIED S-tier Gold, but do not hide the release-cadence weakness.**

SoapySDR clears the quality bar because its hardware-neutral API, runtime driver registry, broad cross-platform CI, bindings, null-device path and example-driver integration provide concrete evidence of a mature reusable interoperability layer. Its biggest weakness is not architecture but release hygiene: the source has continued changing while the documented formal release remains 0.8.1 from 2021.
