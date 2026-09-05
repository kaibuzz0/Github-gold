# rtl_433 — SDR ISM-band protocol decoder and RF analysis toolkit

- **Repository:** https://github.com/merbanan/rtl_433
- **Maintainer/repository owner:** merbanan / rtl_433 contributors
- **Category:** Software-defined radio / RF protocol analysis / sensor telemetry / interoperability / embedded data collection
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **License:** GPL-2.0-or-later, based on the repository `COPYING` text and its application notice
- **Primary language/tooling:** portable C99, CMake, Python maintenance/test helpers
- **Primary platforms:** Linux including embedded systems, FreeBSD, macOS, Windows; common 32-bit and 64-bit CPU families
- **Radio/input ecosystem:** RTL-SDR directly; SoapySDR-backed devices including LimeSDR, PlutoSDR, HackRF One and SoapyRemote; file/replay inputs are also supported
- **Discovery path:** GitHub-first category rotation into SDR/RF interoperability. No YouTube-transcript claim is used in this dossier.

## Why it matters

`rtl_433` is a mature, practical RF decoding and analysis toolkit for low-cost sensors and devices that transmit in common ISM bands. Despite its name, upstream describes it as a generic data receiver used mainly around 433.92 MHz, 868 MHz, 315 MHz, 345 MHz and 915 MHz.

Its value is not limited to the large built-in protocol catalog. The repository contains reusable signal-processing, demodulation, bit-buffer, protocol-decoder, structured-output and replay/testing machinery. It can receive from inexpensive RTL2832-based dongles or broader SoapySDR hardware, decode known protocols, analyze unknown signals, replay captured samples, create custom decoders, and emit machine-readable data into MQTT, InfluxDB, syslog, HTTP, JSON, CSV and other outputs.

That makes the project useful as both a complete application and an engineering reference for legitimate RF interoperability, environmental telemetry, home automation, weather/soil sensing, TPMS research, protocol reverse engineering, archival signal analysis and offline data collection.

## Repository-native functionality

The current README documents:

- RTL-SDR and SoapySDR device support;
- multiple tunable frequencies and frequency hopping;
- configurable gain, sample rate and tuner settings;
- OOK/FSK demodulation controls;
- pulse analysis with `-A`;
- raw I/Q sample capture;
- file-based replay without a radio;
- selective protocol enable/disable with `-R`;
- general-purpose decoders with `-X`;
- structured outputs including JSON, CSV, MQTT, InfluxDB, syslog and HTTP;
- metadata for time, protocol, signal level, noise, statistics and raw bits;
- unit normalization and custom tags.

The README also states that the portable C99 codebase is known to build on Linux, FreeBSD, macOS and Windows, with low resource usage and few dependencies as explicit goals. Common architectures listed include amd64, arm64, armhf, i386, ppc64el, riscv64 and s390x.

Primary source:
- https://github.com/merbanan/rtl_433/blob/master/README.md

## Strongest reusable component: generic flex decoder

One of the most valuable internals is `src/devices/flex.c`, which implements a generic configurable decoder rather than requiring a new C module for every simple protocol.

Upstream documentation exposes this through `-X <spec>`. A user can disable built-in decoders with `-R 0`, inspect a signal, infer pulse timings/modulation, and supply a custom decoder specification. The current repository includes example `.conf` files built this way.

This is a strong GitHub Gold component because it separates basic RF framing/demodulation from device-specific semantics. It supports rapid protocol exploration and can serve as a bridge between raw pulse analysis and a fully maintained decoder implementation.

Relevant upstream locations:
- https://github.com/merbanan/rtl_433/blob/master/src/devices/flex.c
- https://github.com/merbanan/rtl_433/blob/master/docs/ANALYZE.md
- https://github.com/merbanan/rtl_433/blob/master/docs/OPERATION.md
- https://github.com/merbanan/rtl_433/tree/master/conf

Important caveat: upstream's primer explicitly describes flex-decoder suggestions as a statistical heuristic. Automatically suggested parameters are not proof that a protocol has been correctly identified.

## Built-in protocol corpus as executable knowledge

The repository's large `src/devices/` tree is effectively an executable corpus of documented RF protocol knowledge. Device modules cover weather sensors, temperature/humidity sensors, soil probes, tank monitors, energy monitors, TPMS devices, door/window sensors, leak detectors, remotes and other low-power transmitters.

This corpus is useful for studying recurring embedded-RF patterns such as:

- OOK pulse-position/pulse-width schemes;
- FSK variants;
- sync/preamble detection;
- repeated packets and majority/repetition handling;
- CRC/checksum/parity validation;
- field extraction and unit conversion;
- rejecting implausible decoded values to reduce false positives.

A recent August 27, 2026 commit is a good example of the project's validation discipline: the inFactory decoder gained a published sensor-range guard because its 4-bit CRC alone allowed unrelated RF traffic to occasionally form a stable false positive. Upstream constrained decoded temperature to the broadest documented device range instead of treating checksum success as sufficient semantic validation.

## Analysis and replay workflow

`rtl_433` supports a useful offline research loop:

1. capture raw I/Q samples from a receiver;
2. replay samples from a file using `-r`;
3. inspect pulse structure with the analyzer;
4. experiment with demodulation settings;
5. create a temporary flex decoder;
6. validate decoded bit rows and checksums;
7. only then promote a stable protocol into a dedicated decoder when warranted.

This separation between capture and replay is especially valuable for repeatable protocol research because hardware and RF conditions do not need to be recreated for every parser iteration.

GitHub Gold did not execute this workflow during this pass.

## Output and integration layer

The application is unusually useful as a telemetry bridge because the decoder pipeline is not tied to one UI. Current CLI output targets include:

- key/value text;
- JSON;
- CSV;
- MQTT;
- InfluxDB;
- syslog;
- HTTP;
- trigger and stream-oriented outputs.

The repository also includes examples for downstream automation. Recent 2026 work updated Home Assistant MQTT autodiscovery mapping for soil-probe conductivity data and corrected InfluxDB measurement handling.

This makes `rtl_433` a practical ingest component for local-first/self-hosted sensor systems rather than only an interactive SDR utility.

## Build, test and static-analysis evidence

The current GitHub Actions `check.yml` provides substantial repository-native working evidence.

### Cross-platform builds

macOS CI currently builds and tests on:

- macOS 14;
- macOS 15;
- macOS 26.

The macOS path installs SoapySDR and RTL-SDR dependencies, configures through CMake, builds, and executes the test target.

Linux CI exercises both:

- Unix Makefiles;
- Ninja;

across:

- Debug;
- Release.

It then runs the project's tests.

### Coverage and integration tests

A dedicated coverage job enables coverage instrumentation, runs CTest and explicitly notes inclusion of HTTP-server integration/dataflow/WebSocket tests before generating an HTML report artifact.

### Additional gates

The inspected workflow also performs:

- Doxygen documentation builds;
- code-style validation;
- generated/maintainer-update cleanliness checks;
- symbol-error checks;
- Clang static analysis across headers, core sources and `src/devices/*.c`.

The workflow therefore provides stronger evidence than merely checking that one Linux build compiles.

### Supply-chain caveat

The inspected workflow uses mutable major-version Action references such as `actions/checkout@v5` and `actions/upload-artifact@v4` rather than immutable commit SHAs. That is common but weaker than fully pinned workflow dependencies.

Primary workflow:
- https://github.com/merbanan/rtl_433/blob/master/.github/workflows/check.yml

## Release and maintenance evidence

The latest stable GitHub release returned by the Releases API during this pass is:

- **Release 25.12**, published **December 12, 2025**.

Its GitHub release assets expose SHA-256 digest metadata for packaged binaries, including macOS and multiple Linux variants.

Stable release cadence is not the best indicator of current maintenance here. Development is active and the project publishes nightly prerelease artifacts. A nightly release was published **September 1, 2026** with SHA-256 digest metadata and packages spanning Linux and macOS architectures and RTL-SDR/SoapySDR variants.

Recent commits inspected include:

- **September 3, 2026:** add an Etekcity ZAP 3F flex-decoder configuration;
- **September 1, 2026:** fix Windows LLP64 portability around `long` usage;
- **September 1, 2026:** fix unset InfluxDB `_measurement`;
- **September 1, 2026:** add macOS x86_64 binaries;
- **September 1, 2026:** extend ThermoPro decoding for the 915 MHz TX-2B variant using measured timing observations;
- **August 28, 2026:** fix DeltaDore X3D payload parsing;
- **August 27, 2026:** reject implausible inFactory temperatures to reduce checksum-valid false positives.

Maintenance is therefore current through September 3, 2026.

## License and reuse boundary

The repository contains the GNU GPL version 2 license text and its application guidance states redistribution/modification may be under GPL v2 or, at the user's option, a later GPL version. This dossier therefore records the project as **GPL-2.0-or-later**.

Because that is a copyleft license, direct copying or adaptation of source into distributed software needs compatible licensing and preservation of notices/source obligations. GitHub Gold does not copy decoder or DSP source here; it catalogs and links to the useful components.

No third-party source code was copied during this pass.

## Valuable components and follow-up targets

### 1. `src/devices/flex.c`

Map the flex specification grammar and determine exactly which modulation/framing families can be represented without writing a compiled decoder.

### 2. Pulse and bit-buffer pipeline

Trace samples from SDR input through amplitude/magnitude estimation, pulse detection, demodulation and `bitbuffer` representation. This is likely the cleanest reusable architectural path for understanding the project.

### 3. Protocol-test vectors

Inspect how decoder regression data is represented and how recorded/demodulated signals are turned into deterministic tests. A compact RF protocol corpus plus replay harness would itself be a valuable research pattern.

### 4. False-positive defenses

Survey decoder modules for CRC/checksum verification, repeated-row checks, reserved-bit checks, physical-range checks and other semantic validation. The August 27 inFactory fix is a concrete example of why checksum validation alone may be insufficient.

### 5. Output abstraction

Inspect the JSON/MQTT/InfluxDB/HTTP output layer and whether it cleanly separates normalized decoded events from transport-specific formatting.

### 6. SoapySDR boundary

Research `pothosware/SoapySDR` separately as a possible standalone Gold candidate. It is likely the more reusable hardware-abstraction layer beneath rtl_433's broad non-RTL radio support.

### 7. RTL-SDR ecosystem

Inspect the current RTL-SDR upstream and determine which tuner/device-control pieces remain useful as low-cost receive-only hardware primitives.

## Operational, privacy and legal caveats

- `rtl_433` is primarily a receiver/decoder. The fact that a signal is receivable does not automatically make every interception, recording or use lawful in every jurisdiction or context.
- Some decoded traffic can contain identifiers, occupancy-like signals, location-related telemetry or other sensitive metadata. Passive RF research still requires appropriate privacy handling.
- A decoded protocol result should not be treated as authenticated merely because its checksum/CRC is valid. Many low-cost ISM protocols are designed for error detection, not sender authentication.
- RF conditions, interference, gain, sample rate and decoder thresholds can affect results.
- Flex-decoder heuristics are research aids, not protocol-proof machinery.
- For TPMS, alarm/security sensors or other safety/security-adjacent devices, cataloging receive/analysis functionality does not imply operational authorization to interfere with systems.

## Verification boundary

GitHub Gold inspected repository-native README documentation, license text, current commits, release metadata, CI workflows, code-search evidence for the flex decoder, and analysis/operation documentation.

GitHub Gold **did not**:

- build rtl_433;
- run CMake/CTest or the coverage suite;
- connect an RTL-SDR, HackRF, LimeSDR, PlutoSDR or other receiver;
- capture or decode live RF traffic;
- replay an I/Q recording;
- verify a device protocol against physical hardware;
- validate protocol timing measurements;
- test MQTT, InfluxDB, HTTP or Home Assistant integration;
- benchmark CPU/memory use;
- audit every decoder for correctness or false positives;
- independently verify release hashes;
- transmit RF signals;
- perform a security or privacy audit.

**VERIFIED** here means that repository-native code, documentation, CI, release and maintenance evidence support the project's stated functionality. It does not mean GitHub Gold performed independent RF/hardware validation.

## Provisional score rationale

- **Utility — 5/5:** practical low-cost RF telemetry decoding, protocol analysis and offline/self-hosted sensor ingestion.
- **Working Evidence — 5/5:** stable releases, nightly artifacts, cross-platform build/test CI, coverage/integration tests and active decoder maintenance.
- **Reusability — 5/5:** generic flex decoder, replayable I/Q workflow, device-independent output layer, SDR abstraction and large protocol corpus.
- **Novelty — 4/5:** individual SDR techniques are established, but the breadth of protocol knowledge plus generic decoder/replay/integration tooling is unusually valuable.
- **Documentation — 5/5:** substantial README, operation, analysis, building and contribution documentation.
- **Maintenance — 5/5:** meaningful commits current through September 3, 2026 and nightly builds published in the same week.

**Total: 29/30 — provisional S tier.**

## Next-step research queue

1. Trace one captured pulse train from input samples through pulse detection, demodulation, `bitbuffer`, decoder callback and structured JSON output.
2. Reverse-map the `-X` flex grammar to `src/devices/flex.c` and catalog its supported modulation/framing/checksum features.
3. Inspect deterministic decoder test fixtures and replay tooling as a standalone RF regression-testing pattern.
4. Survey false-positive defenses across representative weather, TPMS, security-sensor and energy-monitor decoders.
5. Inspect MQTT/HTTP/InfluxDB output internals and the Home Assistant example integration.
6. Research `pothosware/SoapySDR` as the strongest recursive ecosystem candidate.
7. Compare rtl_433's receive/decode architecture with GNU Radio/Osmocom tooling without duplicating broad frameworks already well represented elsewhere.
