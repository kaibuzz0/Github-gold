# libiio hardware interoperability research — 2026-08-28

## Candidate

- **Repository:** https://github.com/analogdevicesinc/libiio
- **Author / Org:** Analog Devices Inc. / community contributors
- **Category:** hardware interoperability / Linux IIO / sensors / RF / embedded systems / remote device access
- **Evidence:** VERIFIED
- **Provisional Gold score:** **S / 27**
- **License:** library LGPL-2.1-or-later; examples/tests GPL-2.0-or-later; some files MIT — inspect file-level/component licensing before extraction
- **Discovery:** independent GitHub-first broadening pass after the SOPS research cluster

## Executive finding

libiio is a high-value hardware-abstraction and remote-I/O library around the Linux Industrial I/O subsystem. It is useful well beyond one Analog Devices board: upstream explicitly positions it as vendor-neutral infrastructure for ADCs, DACs, accelerometers, gyros, IMUs, pressure/light/temperature/magnetic sensors, DDS/PLL components, programmable gain devices, and RF transceivers.

The especially valuable architectural property is that the same higher-level API can target local Linux IIO devices or communicate with a remote IIO target over transports such as USB, Ethernet/network, or serial. That makes libiio relevant as a reusable boundary between applications and mixed local/remote sensor/RF hardware.

## Score rationale — 27/30

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Utility | 5 | Broad sensor, converter, timing and RF device classes; local and remote operation. |
| Working evidence | 4 | Mature released 0.x line, active v1.0 development, CI/test surfaces and production ecosystem; GitHub Gold did not execute it. |
| Reusability | 5 | C library, public API, multiple language bindings, backend abstraction, compatibility layer, utilities/daemon. |
| Novelty | 4 | Strong vendor/platform-neutral IIO abstraction and remote-device architecture rather than device-specific SDK code. |
| Documentation | 4 | README, API docs/wiki, examples, developer materials and migration guidance; some current v1.0 behavior is still development-branch material. |
| Maintenance | 5 | Active August 2026 main-branch work with API/binding tests and kernel-IIO synchronization. |

## What upstream currently supports

The upstream README describes libiio as the userspace library for Linux IIO and explicitly lists support for device families including:

- ADC and DAC devices;
- accelerometers, gyroscopes and IMUs;
- capacitance, pressure, light, color, proximity and temperature sensors;
- magnetometers;
- DDS and PLL components;
- variable/programable gain amplifiers;
- RF transceivers.

The same documentation states that a program can use libiio natively on an embedded Linux target or access an IIO target remotely from Linux, Windows or macOS hosts over USB, Ethernet or serial.

## Current v1.0 architecture transition

The repository's `main` branch is the v1.0 development line. Upstream warns that this API is incompatible with the legacy v0.25-and-older API while preserving a dedicated `libiio-v0` legacy branch and a compatibility layer intended to allow old v0.x binaries to continue operating against v1.x installations.

This is important for catalog use:

- new integrations should study the v1 API rather than blindly copying old 0.x examples;
- legacy compatibility is a real design surface worth studying separately;
- release maturity and `main`-branch maturity should not be conflated.

The current top-level CMake project declares version **1.0.0** and builds the core C library from separate attribute, backend, block, buffer, channel, context, device, event, mask, scan, stream, task and utility units.

## Reusable architecture and components

### 1. Public IIO object model

The public headers and source split expose reusable abstractions around:

- contexts;
- devices;
- channels;
- attributes;
- buffers and blocks;
- streams;
- events;
- scan/discovery;
- backend interfaces.

This is valuable as an example of keeping hardware discovery/control/streaming concerns separate while presenting a stable application-facing API.

### 2. Backend abstraction

Current build files expose a backend layer and optional dynamically loaded modules. The v1 CMake configuration includes a public backend header and can build backends into the library or as modules depending on configuration.

The USB backend is explicit in the current build and uses libusb. The source/build system also contains network/remote, serial and emulation-related paths. The architecture is more valuable than any one transport: applications can depend on the IIO object model while the transport/backend handles where the hardware actually lives.

### 3. Remote IIO / `iiod`

libiio includes the IIO daemon (`iiod`) and client-facing remote infrastructure. This creates a useful embedded/host split:

1. Linux target owns the kernel IIO devices;
2. `iiod` exposes them remotely;
3. a host-side libiio application can discover/control/stream without embedding board-specific kernel/device logic.

This is a strong pattern for lab equipment, SDR/RF front ends, industrial sensing, remote instrumentation and headless embedded hardware.

### 4. Language bindings

Current August 2026 maintenance explicitly updates version support across **Python, C# and C++ bindings**. The commit also updates tests to reflect the new semantic-version API.

The language-binding layer is therefore not merely historical documentation; it is actively maintained with the v1 API transition.

### 5. Legacy compatibility layer

Current CMake builds an optional `iio-compat` library for 0.x compatibility and contains separate Unix/Windows dynamic-loading paths. This is a particularly useful reference for ABI/API migration strategies where a new core API must coexist with an installed legacy ecosystem.

### 6. Embedded / non-desktop portability

The repository includes Zephyr build material in addition to normal POSIX/Windows/macOS-oriented configuration. This should be researched further before claiming a full target matrix, but it is a strong lead for MCU/RTOS interoperability around the same IIO concepts.

## Working and maintenance evidence

Fresh upstream commits inspected from **August 26–28, 2026** include:

- synchronization with a newly added upstream Linux kernel IIO channel type (`IIO_VOLUMEFLOW`), updating the C API plus Python and C# bindings;
- `iiod` startup-version output cleanup to report full semantic versioning;
- API tests updated for the patch-version field;
- Python, C# and C++ bindings updated to expose patch-version support.

This is meaningful maintenance because changes are crossing the core API, daemon, bindings and tests together rather than being documentation-only churn.

## Release-state caveat

The latest GitHub release returned by the repository API is **v0.26, published September 25, 2024**. Meanwhile `main` is actively developed as v1.0.0 in 2026.

GitHub Gold therefore should not claim that the current v1.0 main branch is equivalent to a stable v1.0 GitHub release. Users choosing production binaries should follow upstream's release guidance; researchers studying current architecture can inspect `main` while preserving the development-state caveat.

## Licensing boundary

The upstream README explicitly distinguishes:

- **core library:** LGPL-2.1-or-later;
- **tests/examples / iio-utils:** GPL-2.0-or-later;
- **certain files:** MIT.

Therefore component reuse cannot be summarized as one repository-wide permissive license. Before copying or adapting a specific utility, binding, test or source component, inspect its file-level license/header and applicable root license text.

No third-party source code was copied into GitHub Gold in this pass.

## Verification performed by GitHub Gold

Inspected:

- upstream repository metadata;
- current README and licensing declarations;
- current v1.0 CMake/build architecture;
- latest GitHub release metadata;
- recent August 2026 commits and their stated API/test/binding changes.

Not performed:

- no source build;
- no hardware connection;
- no `iiod` deployment;
- no USB/network/serial transport test;
- no throughput/latency benchmark;
- no binding execution;
- no ABI compatibility test;
- no security audit or fuzzing.

Claims above are therefore limited to inspected upstream source structure, documentation, release metadata and commit evidence.

## Why it belongs in GitHub Gold

libiio is useful as both a whole project and a component-level architecture reference:

- hardware-agnostic Linux IIO userspace API;
- remote embedded-device access model;
- backend/module abstraction;
- I/O buffers/blocks/streams;
- discovery and channel metadata;
- multi-language bindings;
- daemon/client split;
- legacy compatibility strategy;
- mixed Linux/Windows/macOS host workflows.

It is especially relevant to future SDR, sensor, robotics, instrumentation and embedded-system research because it provides a reusable bridge below application DSP/control software and above kernel/device drivers.

## Related / recursive leads

Strong follow-up branches:

1. **Analog Devices IIO Oscilloscope / libad9361 / pyadi-iio** — inspect how higher-level RF tooling consumes libiio.
2. **Linux IIO subsystem** — map kernel ABI assumptions and device-discovery semantics.
3. **SoapySDR interoperability** — determine where SoapySDR modules bridge onto IIO/libiio and compare their abstraction layers.
4. **GNU Radio IIO integration** — inspect reusable source/sink patterns for streaming RF/sensor samples through libiio.
5. **Zephyr support** — establish the exact supported subset and transport model before promoting embedded/RTOS claims.
6. **iiod protocol/security boundary** — map authentication/encryption assumptions before recommending remote deployment across untrusted networks.

## Promotion recommendation

**VERIFIED / provisional S / 27.**

Promotion-worthy as a deeply reusable hardware interoperability library, with two mandatory catalog caveats:

1. the v1.0 `main` API is an active development line while the latest GitHub release located is v0.26;
2. licensing varies by component, so copying code requires file/component-level review rather than assuming a single repository-wide license.
