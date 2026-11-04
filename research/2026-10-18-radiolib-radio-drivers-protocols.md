# RadioLib — embedded radio drivers, protocols and test infrastructure

**Research date:** 2026-10-18  
**Upstream:** https://github.com/jgromes/RadioLib  
**Discovery:** Followed the RadioLib dependency from the canonical LighthouseReckoning entry.  
**Classification:** VERIFIED from upstream repository evidence; **S / 28 provisional** (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5).  
**Verification boundary:** No independent build, flash, unit/fuzz execution, RF measurements, LoRaWAN certification test, or security audit.

## Why it matters

RadioLib provides a consistent C++ interface across many embedded radio transceivers, including SX126x, SX127x, SX128x, CC1101, RF69, LR11x0, LR2021 and nRF24L01 families. Beyond packet transport, upstream exposes LoRaWAN, AX.25, APRS, RTTY, SSTV, Hellschreiber, Morse and paging functionality. It is a reusable infrastructure dependency for off-grid sensors and embedded communications rather than a complete mesh network on its own.

## Inspected primary evidence

- `README.md`: chip, protocol, board and integration matrix, including explicit warning against small ATmega328 boards. https://github.com/jgromes/RadioLib/blob/master/README.md
- `license.txt`: MIT grant and copyright notice (2018 Jan Gromeš). https://github.com/jgromes/RadioLib/blob/master/license.txt
- `library.properties`: version 7.8.1, maintainer, Arduino metadata. https://github.com/jgromes/RadioLib/blob/master/library.properties
- `src/RadioLib.h`: umbrella API and included driver/protocol classes. https://github.com/jgromes/RadioLib/blob/master/src/RadioLib.h
- `src/Hal.h`: abstract GPIO, timing, interrupts and cryptographic engine hooks. https://github.com/jgromes/RadioLib/blob/master/src/Hal.h
- `src/modules/SX126x/SX126x.cpp`: LoRa/GFSK radio configuration, IRQ mapping and packet setup. https://github.com/jgromes/RadioLib/blob/master/src/modules/SX126x/SX126x.cpp
- `src/protocols/LoRaWAN/LoRaWAN.cpp`: MAC command table, send/receive paths, channel and crypto wiring. https://github.com/jgromes/RadioLib/blob/master/src/protocols/LoRaWAN/LoRaWAN.cpp
- `.github/workflows/main.yml`: cross-platform Arduino compilation matrix with board-specific exclusions. https://github.com/jgromes/RadioLib/blob/master/.github/workflows/main.yml
- `.github/workflows/unit-test.yml`: explicitly invokes `extras/test/unit/test.sh` and `coverage.sh`; `.github/workflows/fuzz.yml` invokes `extras/test/fuzz/test.sh`. Workflow definitions were read, not run locally.
- `.github/workflows/codeql-analysis.yml`: C++ CodeQL workflow; cppcheck workflow also exists.
- Release 7.8.1, published **2026-09-28**, fixes LR2021 register handling and an RF69 recursive call: https://github.com/jgromes/RadioLib/releases/tag/7.8.1
- Default-branch commit `982500240306714017cd04c3bdd0b31b48386e8a` dated **2026-10-18**: cppcheck false-positive correction. https://github.com/jgromes/RadioLib/commit/982500240306714017cd04c3bdd0b31b48386e8a
- On a **separate PR head** `6c276919...`, observed GitHub Actions results dated **2026-10-18**: CI, unit test, fuzz, CodeQL and static-memory checks succeeded, while Cppcheck failed. These PR checks are not proof of default-branch health. See https://github.com/jgromes/RadioLib/actions/runs/39138646346 and https://github.com/jgromes/RadioLib/actions/runs/39138646231

## Reusable subcomponents

| Component | Exact upstream location | Reuse opportunity |
| --- | --- | --- |
| HAL and platform adapters | `src/Hal.h`, `src/hal/` | Portable GPIO, SPI, timing, interrupts and custom platform integration |
| LoRa transceiver drivers | `src/modules/SX126x/`, `SX127x/`, `SX128x/` | Radio initialization, modulation, IRQ and packet handling |
| Other radio drivers | `src/modules/CC1101/`, `RF69/`, `LR11x0/`, `LR2021/` | Chip-family interoperability |
| LoRaWAN stack | `src/protocols/LoRaWAN/` | MAC, channel plans, confirmed traffic, crypto and frame parsing |
| Digital modes | `src/protocols/AX25/`, `APRS/`, `RTTY/`, `SSTV/`, `Pager/` | Reusable encoding and radio-data services |
| Utilities | `src/utils/` | Common data and cryptographic support |
| Non-Arduino examples | `examples/NonArduino/` | Porting and embedded Linux/Pico integration leads |
| Test infrastructure | `extras/test/unit/`, `extras/test/fuzz/` | Test patterns, fuzz targets, coverage collection |
| Applied utilities | `extras/SX126x_Spectrum_Scan/`, `extras/ADSB_Monitor/` | Diagnostic/receiver tool leads |

## Deployment and limitations

Upstream supports Arduino Library Manager and PlatformIO; it also documents ESP-IDF and non-Arduino builds. Radio hardware and pin mappings are required for RF functionality. Platform compatibility does not imply that every chip supports every modulation or protocol. Respect local spectrum allocation, transmission-power and duty-cycle restrictions.

**API migration:** The 7.7.0 release introduced configuration-struct `begin()` APIs. Existing positional overloads are deprecated for removal in 8.0.0; integration code should pin a version and plan migration. See https://github.com/jgromes/RadioLib/releases

**License:** Root `license.txt` is MIT. Retain the copyright/permission notice if source is copied. Review external SDKs, board cores, linked libraries and examples separately. This research copies no implementation code.

**Security and assurance:** LoRaWAN Class A/C and Class A pre-certification are upstream claims; no independent interoperability, cryptographic, regulatory or hardware testing was performed. Workflow presence alone is not a passing test result. A recent PR showed a Cppcheck failure alongside other successful checks.

## Recursive leads

1. Compare RadioLib SX126x interrupt/CAD behavior against LighthouseReckoning's retry and sleep scheduling; independently compile its SleepyNode examples.
2. Inspect RadioLib's LoRaWAN nonce persistence and compatibility across 7.3+ format changes before recommending firmware upgrades.
3. Evaluate RadioLib HAL portability on RP2040 and ESP-IDF using a reproducible build matrix.
4. Examine `extras/SX126x_Spectrum_Scan/` as a component lead, not as evidence of independently verified spectrum measurements.

**YouTube:** No playlist transcript evidence used in this dossier. All findings derive from GitHub-first upstream research.
