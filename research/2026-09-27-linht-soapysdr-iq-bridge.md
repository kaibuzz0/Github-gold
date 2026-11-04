# LinHT SoapySDR IQ bridge — SX1255/ZMQ interoperability component

- **Upstream:** https://github.com/M17-Project/LinHT-utils
- **Author / org:** M17-Project
- **Category:** SDR / embedded Linux / interoperability / radio tooling
- **Evidence:** PROMISING
- **Provisional Gold score:** **23 / 30 (A)**
  - Utility: 5
  - Working evidence: 3
  - Reusability: 4
  - Novelty: 4
  - Documentation: 4
  - Maintenance: 3
- **Discovery:** recursive follow-up from the LinHT hardware dossier.

## What it is

`LinHT-utils/tests/soapy_linht` contains a C++17 SoapySDR plugin prototype for the LinHT SX1255 baseband path. It subscribes to LinHT's internal ZeroMQ IQ stream (`ipc:///tmp/bsb_rx`) and exposes the receiver through the standard SoapySDR API.

The documented processing chain converts integer IQ to float complex samples, applies an SX1255 inverse-sinc FIR equalizer, removes DC offset, buffers samples through a FIFO, and serves CF32 or CS16 samples to Soapy clients. Hardware frequency and gain control is passed to the SX1255 control library.

## Why it is Gold

This is a useful interoperability boundary rather than a radio-specific UI. If matured, it lets the unusual LinHT direct-IQ hardware appear to ordinary SDR software as a conventional SoapySDR receiver. The upstream README explicitly targets GNU Radio, OpenWebRX, rtl_433 and SoapyRemote.

The pattern is reusable: keep board-specific capture/control behind a narrow adapter, transport baseband internally over a local IPC stream, normalize/equalize samples at the adapter boundary, and expose a standard SDR API to the rest of the ecosystem.

## Concrete implementation evidence

The repository contains:

- `tests/soapy_linht/main.cpp` — approximately 22 KB C++ implementation;
- `tests/soapy_linht/fir.cpp` / `fir.h` — inverse-sinc FIR support;
- `tests/soapy_linht/CMakeLists.txt` — build definition;
- `tests/soapy_linht/README.md` — build, discovery, SoapyRemote, OpenWebRX and rtl_433 usage examples.

The README documents CF32 and CS16 receive paths, 500 kSa/s operation, one RX stream, frequency tuning, LNA/PGA gain control, FIFO streaming, SoapyRemote operation and an RX-only limitation.

The same repository also contains `sx1255/sx1255-spi.c`, a separate command-line SX1255 control utility using `libsx1255`, `/dev/spidev0.0`, and GPIO. It exposes reset, 125/250/500 kHz sample-rate selection, RX/TX frequency, LNA/PGA/DAC/mixer gain, PLL bandwidth/lock flags, RX/TX enable, RF loopback and raw register access. This is a second useful component for hardware bring-up and diagnostics.

## Evidence boundary

This is classified PROMISING rather than VERIFIED because the Soapy implementation currently lives under a `tests/` tree, no automated CI/test evidence was established in this pass, and GitHub Gold did not build or run it. The upstream documentation is detailed and source is substantial, but documentation claims are not treated as independent runtime verification.

The repository's recent commits through 2026-05-31 include a TX/RX switch fix and prior PA/attenuator initialization changes, which show active hardware bring-up but also reinforce that this is evolving experimental software.

## Runtime / platform requirements

Documented Soapy bridge prerequisites:

- C++17 compiler
- CMake >= 3.10
- SoapySDR development headers
- ZeroMQ
- LinHT `libsx1255.so`
- LinHT baseband producer exposing `ipc:///tmp/bsb_rx`

The SX1255 CLI additionally assumes Linux spidev and GPIO character-device access.

## License caveat

**No root `LICENSE` file was found during this inspection.** The SoapyLinHT README does not state a license. Therefore the code must be treated as **license-unclear / all-rights-reserved by default until upstream clarifies licensing**.

Do not copy or adapt this implementation into GitHub Gold or another project based solely on repository visibility. Catalog/link only. Dependencies such as SoapySDR, ZeroMQ and the SX1255 library also retain their own licenses.

No upstream source was copied into GitHub Gold.

## Verification performed by GitHub Gold

Inspected:

- `LinHT-utils` top-level tree;
- `sx1255/sx1255-spi.c` interface and hardware assumptions;
- `tests/soapy_linht` file set;
- SoapyLinHT README and documented processing/interoperability model;
- recent upstream commit history through 2026-05-31;
- attempted root license lookup (no root `LICENSE` found).

GitHub Gold **did not** compile the plugin or CLI, load it with SoapySDR, connect LinHT hardware, inspect live ZMQ IQ frames, verify FIR response/DC removal, run GNU Radio/OpenWebRX/rtl_433, test SoapyRemote, measure throughput/dropouts, transmit RF, or independently validate the documented sample format.

## Related ecosystem / recursive leads

- https://github.com/M17-Project/LinHT-hw
- https://github.com/M17-Project/meta-linht-sdr
- https://github.com/M17-Project/meta-linht-hardware
- https://github.com/M17-Project/meta-linht-software
- SoapySDR / SoapyRemote
- GNU Radio
- OpenWebRX
- rtl_433

`meta-linht-sdr` is itself a LinHT-customized fork of `balister/meta-sdr` and supplies the Yocto GNU Radio/SDR layer. Its README says individual recipes may have their own licenses, so recipe-level license provenance should be inspected before promoting or extracting anything.

## Strongest next research

1. Identify the producer of `ipc:///tmp/bsb_rx` and document the exact IQ framing/sample contract.
2. Locate `libsx1255` upstream and establish its license, tests and hardware abstraction boundary.
3. Determine whether SoapyLinHT has moved from `tests/` into a packaged Yocto recipe or another repository.
4. Inspect `meta-linht-sdr` recipes for pinned revisions, reproducibility and recipe-level licensing.
5. Only promote this component to VERIFIED after stronger upstream runtime/build evidence or an actual controlled build/run.