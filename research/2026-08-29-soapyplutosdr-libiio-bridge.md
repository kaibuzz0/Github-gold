# SoapyPlutoSDR ↔ libiio interoperability research — 2026-08-29

## Candidate

- **Repository:** https://github.com/pothosware/SoapyPlutoSDR
- **Author / Org:** Pothosware / community contributors
- **Category:** SDR / SoapySDR plugin / libiio / ADALM-Pluto / RF interoperability
- **Evidence:** VERIFIED
- **Provisional Gold score:** **A / 24**
- **License:** LGPL-2.1
- **Discovery:** recursive follow-up from the libiio hardware-interoperability research branch

## Executive finding

SoapyPlutoSDR is a compact but strategically useful interoperability layer between the generic SoapySDR device API and Analog Devices' libiio/libad9361 stack used by ADALM-Pluto-class radios.

Its value is not that it replaces libiio. Instead, it translates a Pluto's libiio control/discovery/streaming surfaces into the SoapySDR abstraction consumed by applications such as SDR front ends, decoders and GNU Radio integrations that prefer Soapy's common device API.

The project is therefore useful as both a working driver/plugin and a reference implementation of an **adapter architecture**:

`SDR application → SoapySDR API → SoapyPlutoSDR → libiio / libad9361 → Pluto IIO devices`

That makes it a strong companion entry to libiio in GitHub Gold.

## Score rationale — 24/30

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Utility | 5 | Bridges a widely used SDR API to Pluto-class IIO hardware and enables reuse across Soapy-aware applications. |
| Working evidence | 4 | Active upstream project, cross-platform CI build checks, current user reports and recent streaming fixes; GitHub Gold did not attach hardware or execute the plugin. |
| Reusability | 5 | Small C++ adapter layer with clear registration, settings and streaming boundaries; useful as an interoperability design reference. |
| Novelty | 3 | Primarily a well-targeted adapter rather than a new DSP or transport protocol. |
| Documentation | 3 | README/wiki/install guidance are useful but concise; several behavioral boundaries are learned from source/issues. |
| Maintenance | 4 | Meaningful 2026 commits including full-duplex streaming/buffer fixes and device-discovery cleanup. |

## Architecture

The repository is unusually compact. The main implementation is split into three high-value surfaces:

- `PlutoSDR_Registration.cpp` — device discovery and SoapySDR registration;
- `PlutoSDR_Settings.cpp` — device controls and parameter translation;
- `PlutoSDR_Streaming.cpp` — RX/TX streaming implementation;
- `SoapyPlutoSDR.hpp` — class/API boundary.

This narrow structure is useful for GitHub Gold because the adapter logic is not buried inside a large application.

## Discovery path: SoapySDR → libiio

The registration layer registers the driver name `plutosdr` through `SoapySDR::Registry` and then discovers potential hardware through libiio.

Current source scans the following libiio backend forms individually:

- `local`;
- filtered Pluto USB discovery using `usb=0456:b673`;
- `ip`.

When discovery returns an IIO context, the plugin does not accept every IIO device. It verifies that the context exposes the expected Pluto hardware graph:

- `ad9361-phy`;
- `cf-ad9361-lpc`;
- `cf-ad9361-dds-core-lpc`.

Only matching contexts become SoapySDR `plutosdr` candidates.

That is a useful reusable pattern: use a broad lower-level discovery API, then validate an expected hardware topology before exposing a higher-level driver.

## USB-enumeration coexistence logic

The registration code contains a particularly interesting compatibility workaround for older libiio behavior.

Before running the Pluto USB IIO scan, optional libusb code checks the cached USB device list for Analog Devices VID:PID `0456:b673` without opening the device. If no matching Pluto is present, the plugin can avoid entering the IIO USB scan path.

The source comments explain the goal: reduce interference/races with other USB drivers during enumeration on libiio versions before the filtered USB backend behavior was available. A 500 ms defer is also retained around this path, with an explicit source comment that the exact delay was not firmly established.

This is valuable engineering evidence because it shows that hardware-driver interoperability sometimes depends as much on **coexistence during discovery** as on data-plane correctness.

It is also a caveat: this is compatibility behavior with historical context, not a generic recommendation that other applications should copy the same delay.

## Dependency boundary

The build requires:

- SoapySDR;
- libiio (minimum requested version 0.9 in current CMake);
- C++11.

It optionally integrates:

- libad9361, enabling AD9361-specific support when found;
- libusb, enabling the USB pre-scan/coexistence path described above.

The current upstream README presents libiio, libad9361 and SoapySDR as the primary project dependencies.

## Cross-platform build evidence

The current GitHub Actions build workflow checks:

- Ubuntu 22.04;
- Ubuntu 24.04;
- macOS 14 through MacPorts.

The Linux jobs install distro packages for SoapySDR, libusb, libiio and libad9361 and then configure/build the plugin with CMake/Ninja.

Two additional macOS/Homebrew jobs remain in the workflow but are explicitly disabled because their taps are considered too old. That is useful evidence of maintenance realism: the repository is not presenting disabled/stale package paths as working CI coverage.

GitHub Gold did **not** execute these workflows itself; the claim here is limited to upstream CI configuration and repository evidence.

## Current maintenance evidence

Recent commits inspected include:

- **2026-06-07** — fix TX streamer use of the `bufflen` kwarg and set RX streamer MTU;
- **2026-05-18** — remove the device cache from discovery;
- **2026-03-27** — dynamically size the TX streaming buffer based on sample rate after a contributor reported/testing full-duplex operation at 2 Msps;
- 2025 maintenance updating CI and newer CMake compatibility.

These are substantive driver/data-path changes rather than only documentation churn.

## Multi-channel Pluto+/AD9361 caveat

A current open issue shows an important scope boundary for modified Pluto-class hardware.

A user with a Pluto+ exposing 2 RX / 2 TX reported that the normal driver path still presented one RX and one TX channel. Maintainer discussion points to an experimental `feat-multichn` branch as an initial multi-channel implementation that still needs testing/debugging.

The same issue contains a user report that the experimental branch worked sufficiently to expose additional functionality through OpenWebRX+, but RF port switching remained constrained and part of that behavior was traced to the target firmware/device-tree configuration rather than solely to the Soapy plugin.

GitHub Gold therefore should not summarize current `master` as generic 2x2 AD9361/Pluto+ support. The mature core target is the ordinary Pluto abstraction, while multi-channel variants remain an active/experimental boundary.

## Release-state caveat

The GitHub releases API currently returns no release objects for this repository. The project has current source/CI/commit activity, but GitHub Gold should not invent a formal release-version history from that.

Users should distinguish:

- actively maintained `master` source;
- distribution/package versions;
- any downstream/fork builds;
- experimental branches such as multi-channel support.

## Licensing boundary

The root README and LICENSE identify the project as **GNU LGPL version 2.1**.

No third-party source code was copied into GitHub Gold in this pass. If a specific adapter implementation is later extracted or adapted, preserve the LGPL requirements and separately inspect the licenses of SoapySDR, libiio, libad9361 and any copied dependency-side code.

## Verification performed by GitHub Gold

Inspected:

- repository metadata and current `master` tree;
- README and declared dependencies/license;
- CMake dependency/build logic;
- current GitHub Actions build matrix;
- `PlutoSDR_Registration.cpp` discovery and hardware-validation path;
- recent 2026 commit history;
- current Pluto+ multi-channel issue and maintainer/user discussion;
- GitHub release collection.

Not performed:

- no local build;
- no ADALM-Pluto or Pluto+ hardware test;
- no USB/IP discovery execution;
- no SoapySDRUtil probe executed by GitHub Gold;
- no RX/TX throughput or latency benchmark;
- no full-duplex stress test;
- no GNU Radio/OpenWebRX/SDR++ integration test;
- no RF calibration or regulatory validation.

## Why it belongs in GitHub Gold

SoapyPlutoSDR is valuable less as a giant standalone project than as a **high-quality adapter reference** connecting two important ecosystems.

Reusable ideas/components include:

1. SoapySDR plugin registration and device factory structure;
2. libiio backend discovery mapped into a higher-level generic SDR API;
3. hardware-topology validation before claiming a discovered device;
4. USB-driver coexistence handling during discovery;
5. separation between registration, settings/control and streaming data planes;
6. Soapy-facing reuse of libiio's USB/local/network reach;
7. AD9361-specific optional enhancement through libad9361.

This entry also makes the existing libiio research more navigable: libiio is the lower-level IIO abstraction/transport layer, while SoapyPlutoSDR demonstrates how application-facing SDR ecosystems can consume it.

## Recursive ecosystem leads

Strong follow-ups now include:

1. **pothosware/SoapySDR** — map the driver ABI/registry and stream contract that SoapyPlutoSDR implements.
2. **analogdevicesinc/libad9361-iio** — isolate the RF-specific helper layer that sits above libiio and below this plugin.
3. **GNU Radio `gr-soapy`** — verify how a GNU Radio flowgraph reaches Pluto through the generic Soapy driver boundary.
4. **OpenWebRX+ / Soapy connector** — inspect how remote/browser-facing SDR systems consume the same driver without Pluto-specific application code.
5. **SoapyPlutoSDR `feat-multichn`** — track whether multi-channel support becomes stable enough to promote from experimental evidence.
6. **SDRangel direct IIO plugins** — compare direct-libIIO integration against the Soapy adapter approach.
7. **libiio v1 transition** — current SoapyPlutoSDR CMake asks for the legacy-compatible libiio API surface; study what will be required as distributions move toward libiio v1.

## Promotion recommendation

**VERIFIED / provisional A / 24.**

High-value catalog candidate because it is an actively maintained, compact bridge between SoapySDR and libiio/AD9361 hardware. Keep three mandatory caveats attached:

1. GitHub Gold has not performed a hardware/build/runtime verification itself;
2. current `master` should not be described as generic stable 2x2 Pluto+/AD9361 support;
3. the project has active source and CI evidence but no GitHub release objects in the inspected release collection.