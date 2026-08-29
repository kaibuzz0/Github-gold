# GNU Radio `gr-soapy` integration — source-level research

Date: 2026-08-29

## Candidate

- **Upstream:** https://github.com/gnuradio/gnuradio
- **Component:** `gr-soapy`
- **Category:** SDR / signal processing / hardware abstraction / GNU Radio integration
- **Evidence:** VERIFIED
- **Provisional Gold tier / score:** S / 26
- **License:** GPL-3.0-or-later for the inspected `gr-soapy` source; GNU Radio root `COPYING` contains GPLv3
- **Discovery path:** recursive follow-up from SoapySDR → SoapyPlutoSDR → libiio research

## Executive finding

GNU Radio contains an in-tree `gr-soapy` component that converts the generic SoapySDR device contract into native GNU Radio source/sink blocks. This is the application-facing layer that completes the currently researched stack:

`GNU Radio flowgraph → gr-soapy → SoapySDR → hardware plugin → vendor/device stack`

For Pluto-class hardware, the researched path is:

`GNU Radio → gr-soapy → SoapySDR → SoapyPlutoSDR → libiio / libad9361 → Pluto SDR`

This is valuable because GNU Radio does not need a bespoke block implementation for every supported SoapySDR driver. `gr-soapy` consumes the generic Soapy device API and exposes that functionality to flowgraphs.

## Evidence inspected

### 1. `gr-soapy` is a first-class optional GNU Radio component

`gr-soapy/CMakeLists.txt` searches for SoapySDR 0.7.2 or newer, registers `gr-soapy` as a GNU Radio component, requires `gnuradio-runtime`, and conditionally installs public headers, the library, documentation, Python bindings, examples, and GRC definitions when the relevant GNU Radio build options are enabled.

This is not a detached example repository; it is integrated into the GNU Radio source/build tree.

### 2. Device construction and capability validation

`gr-soapy/lib/block_impl.cc` performs an explicit SoapySDR ABI check at block construction time. A mismatch between the build-time and runtime SoapySDR ABI produces a hard error with a rebuild/install guidance message.

The same constructor:

- converts GNU Radio sample types (`fc32`, `sc16`, `sc8`) into SoapySDR stream formats;
- builds device kwargs and calls `SoapySDR::Device::make()`;
- reapplies recognized device settings;
- checks the requested channel count against the hardware-reported channel count;
- validates stream arguments against `getStreamArgsInfo()`;
- validates tune arguments against `getFrequencyArgsInfo()`;
- validates and applies channel settings and named gains.

This is meaningful interoperability evidence: the adapter interrogates the device contract rather than blindly forwarding arbitrary configuration.

### 3. GNU Radio message commands map into live Soapy hardware controls

The common block registers a GNU Radio message input named `cmd` and maps command keys to SoapySDR control handlers. The inspected command surface includes frequency, gain, sample rate, bandwidth, antenna, gain mode, frequency correction, DC offset, IQ balance, master/reference clock rates, clock/time sources, hardware time, registers, settings, GPIO, GPIO direction, I2C, and UART.

That makes `gr-soapy` more than a sample pipe: it exposes a substantial portion of the generic Soapy device-control plane to a running GNU Radio graph.

### 4. Stream lifecycle is directly backed by the Soapy stream API

On `start()`, the block calls `setupStream()`, queries the stream MTU, adjusts the GNU Radio scheduler's maximum output chunk size to that MTU when available, and then activates the stream. On `stop()`, it deactivates and closes the Soapy stream.

The source block calls `readStream()` with a 0.5-second timeout. Successful reads become GNU Radio output; overflow is explicitly recognized and retried, while timeouts yield back to the scheduler. The source can also emit metadata tags for hardware time, sample rate, and tuned frequency.

The sink block calls `writeStream()`, recognizes Soapy underflow, and supports tagged-burst semantics by translating the end of a tagged burst into `SOAPY_SDR_END_BURST`.

These paths are strong source-level evidence that GNU Radio's scheduler and metadata model are deliberately bridged into SoapySDR streaming semantics.

### 5. Concurrency boundary

The inspected source/sink paths and control block share `d_device_mutex`. Streaming operations take that mutex, and comments explicitly note that command handlers do not run while a read or write is in progress.

This serialization simplifies device access but can also couple control responsiveness to a driver call. The source's finite 500 ms read timeout limits one obvious indefinite-read case; the inspected sink `writeStream()` call does not pass an explicit timeout argument in this wrapper path. This is recorded as an architecture/latency boundary, not a defect claim.

### 6. Python/GRC integration and tests

The `gr-soapy` tree contains Python bindings, GRC block definitions, examples, and `qa_soapy_types.py`. This establishes that the integration is intended to be consumable from normal GNU Radio Python/GRC workflows rather than only through C++.

The current repository CI includes GNU Radio's broader build/test workflows; current `gr-soapy` path history also shows 2026 changes reaching this subtree, including an August 24, 2026 commit that updated PyQt scoped-enum usage in examples/GUI-related code and a February 2026 cross-platform installer refactor touching component registration/build infrastructure.

GitHub Gold did **not** independently run the GNU Radio test suite or validate physical SDR hardware.

## Reusable components / patterns

- `gr-soapy/lib/block_impl.cc` — generic device creation, capability checking, control-command bridge, stream lifecycle, and Soapy ABI validation.
- `gr-soapy/lib/source_impl.cc` — Soapy RX → GNU Radio scheduler bridge, timeout/overflow handling, hardware-time/rate/frequency stream tags.
- `gr-soapy/lib/sink_impl.cc` — GNU Radio scheduler → Soapy TX bridge with tagged-burst/end-burst translation.
- `gr-soapy/include/gnuradio/soapy/block.h` — public generic control/capability surface.
- `gr-soapy/grc/` — graphical block definitions for flowgraph use.
- `gr-soapy/python/soapy/` — Python bindings and QA surface.

These are especially useful as reference architecture for adapting a broad hardware API into a graph/scheduler runtime without reimplementing each device-specific backend.

## Runtime/build requirements

- GNU Radio runtime and normal GNU Radio build dependencies.
- SoapySDR >= 0.7.2 according to current `gr-soapy/CMakeLists.txt`.
- A SoapySDR hardware module/plugin for the actual radio in use.
- Optional Python/GRC components depend on the corresponding GNU Radio build options.

Actual hardware requirements depend entirely on the selected Soapy plugin.

## License and reuse boundary

The inspected `gr-soapy` source files carry `SPDX-License-Identifier: GPL-3.0-or-later`; GNU Radio's root `COPYING` contains GPL version 3. Copying/adapting source into another project therefore requires GPL-compatible handling and preservation of notices. GitHub Gold copied no upstream source.

SoapySDR itself was previously researched as BSL-1.0, and individual Soapy hardware modules can use other licenses. The full stack therefore has component-specific license boundaries; permissive licensing at the Soapy core does not make GNU Radio `gr-soapy` permissively reusable source.

## Maintenance / release signals

- Upstream GNU Radio is not archived and uses `main` as the default branch.
- The latest GitHub release object inspected is GNU Radio v3.10.12.0, published 2025-02-20, with detached signature assets.
- `gr-soapy` path history includes changes merged in 2026, so the component is not merely historical even though the latest release object located predates those changes.

This dossier does not infer that every current `main` change is present in the latest formal release.

## Caveats

- No independent build, test-suite execution, RF test, throughput benchmark, latency measurement, device-compatibility matrix, or hardware timing validation was performed by GitHub Gold.
- Generic Soapy capabilities remain constrained by the actual hardware plugin. A control being exposed by `gr-soapy` does not prove that every Soapy device implements it.
- Device/plugin behavior and thread-safety assumptions can vary; `gr-soapy` serializes inspected stream/control access through a device mutex.
- GNU Radio is a much larger project than this dossier. The provisional score applies to the `gr-soapy` integration/component research, not a complete audit of every GNU Radio subsystem.

## Gold score rationale — 26 / 30

- **Utility: 5/5** — connects GNU Radio to a large generic SDR hardware ecosystem.
- **Working evidence: 4/5** — in-tree implementation, build integration, bindings/tests, and mature upstream; not independently executed here.
- **Reusability: 4/5** — excellent architectural reference and usable component, with GPL copyleft affecting direct source reuse.
- **Novelty: 4/5** — strong generic graph-runtime ↔ hardware-abstraction adapter design.
- **Documentation: 4/5** — public API/GRC/examples/build integration are substantial, though this pass did not find a single exhaustive component design document.
- **Maintenance: 5/5** — active parent project and 2026 subtree/build updates.

## Next recursive leads

1. **SoapyRemote** — inspect the network transport and remote-device trust/resource boundary.
2. **libad9361-iio** — map the RF-specific helper layer between Pluto-class applications and libiio.
3. Compare `gr-soapy` with native GNU Radio hardware integrations such as gr-uhd to identify what generic abstraction gives up or simplifies.
4. Trace one real flowgraph using `gr-soapy` + SoapyPlutoSDR to document the exact runtime discovery/configuration chain without claiming hardware validation.
5. Inspect QA/CI coverage that actually exercises a Soapy null/mock device, if present, rather than assuming generic GNU Radio CI validates hardware-facing behavior.