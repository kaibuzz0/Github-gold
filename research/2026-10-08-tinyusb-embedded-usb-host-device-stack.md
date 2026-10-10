# TinyUSB — embedded USB host/device stack and recovery components

- **Upstream:** https://github.com/hathach/tinyusb
- **Author:** Ha Thach and contributors
- **Research date:** 2026-10-10
- **Category:** embedded USB; device and host protocols; MCU portability; reliability testing
- **Evidence:** VERIFIED (repository-native source, test configuration, CI, and release evidence; no independent hardware execution)
- **Provisional score:** **27/30 (S)** — Utility 5, Working evidence 4, Reusability 5, Novelty 3, Documentation 5, Maintenance 5
- **License:** MIT at repository root; individual dependencies, vendor SDKs and imported files must be checked separately.
- **Discovery:** Independent GitHub-first investigation; not attributed to inaccessible YouTube transcripts.

## Why it matters

TinyUSB is a portable C USB host/device stack intended for embedded devices. Its design uses static allocation and defers USB interrupt processing into task context. Its breadth of controller backends, USB classes, example firmware and test infrastructure makes it a source of reusable implementation patterns, not merely a standalone application. Claims about memory safety should not be confused with formal memory safety of C.

## Valuable components and exact locations

| Component | Upstream location | Practical value |
| --- | --- | --- |
| Host enumeration, transfers and hub logic | [src/host](https://github.com/hathach/tinyusb/tree/master/src/host) | USB-host state machine, control transfers, hubs |
| Device-side USB stack | [src/device](https://github.com/hathach/tinyusb/tree/master/src/device) | Descriptors, endpoint management, enumeration |
| USB class drivers | [src/class](https://github.com/hathach/tinyusb/tree/master/src/class) | CDC, HID, MSC, MIDI, audio, DFU, networking and other class implementations; role/maturity vary |
| MCU controller backends | [src/portable](https://github.com/hathach/tinyusb/tree/master/src/portable) | Controller-specific IRQ, endpoint RAM and DMA integration |
| RP2040 host controller | [hcd_rp2040.c](https://github.com/hathach/tinyusb/blob/master/src/portable/raspberrypi/rp2040/hcd_rp2040.c) | Host endpoint allocation and interrupted-transfer recovery |
| RTOS/bare-metal abstraction | [src/osal](https://github.com/hathach/tinyusb/tree/master/src/osal) | Deferred tasks, synchronization portability |
| Device and host examples | [examples](https://github.com/hathach/tinyusb/tree/master/examples) | Buildable reference integrations for supported boards |
| Unit tests and fuzz harnesses | [test](https://github.com/hathach/tinyusb/tree/master/test) | Mocked C tests and protocol fuzzing |

## Installation and constraints

Upstream [getting started](https://github.com/hathach/tinyusb/blob/master/docs/getting_started.rst) and [integration documentation](https://github.com/hathach/tinyusb/blob/master/docs/integration.rst) describe dependency setup, board-specific builds, `tusb_config.h`, descriptor callbacks, IRQ forwarding, initialization and servicing `tud_task()`/`tuh_task()`. Toolchains depend on the target (e.g. Pico SDK for RP2040 and ESP-IDF for supported ESP32 configurations). Do **not** assume every MCU supports both host and device roles.

## Evidence inspected

1. [README](https://github.com/hathach/tinyusb/blob/master/README.rst) identifies host/device roles, portable architecture and MCU coverage.
2. [Root LICENSE](https://github.com/hathach/tinyusb/blob/master/LICENSE) explicitly grants MIT rights and requires preservation of notices.
3. [Ceedling project configuration](https://github.com/hathach/tinyusb/blob/master/test/unit-test/project.yml) defines mocked C tests with a `test:all` default task.
4. [Pre-commit workflow](https://github.com/hathach/tinyusb/blob/master/.github/workflows/pre-commit.yml) pins Ceedling 1.0.1 and builds fuzz harnesses, **but comments out** `ceedling test:all`. Thus the existence of tests is not proof they all run in that workflow.
5. [RP2040 host implementation](https://github.com/hathach/tinyusb/blob/master/src/portable/raspberrypi/rp2040/hcd_rp2040.c) contains endpoint allocation and host-controller logic, with conditional handling for RP2350.
6. [Release 0.21.0](https://github.com/hathach/tinyusb/releases/tag/0.21.0) is a published upstream release, reported June 30, 2026.
7. [October 8 RP2040 host recovery change](https://github.com/hathach/tinyusb/commit/e20482387575da72b11d84ed008b25a28e068a01) is a useful lead for studying buffer retirement after interrupted transfers. It was not independently reproduced.

## Caveats and verification boundary

- **Actually performed:** repository-native read of README, root MIT license, Ceedling configuration, pre-commit workflow and RP2040 host source; reviewed prior upstream research notes and exact commit/release references.
- **Not performed:** compiling, executing tests, fuzzing, flashing hardware, enumerating USB devices, stress testing disconnect/reconnect, measuring performance or auditing security.
- Hardware behavior varies by controller, board, cache/DMA setup, USB power and host/device configuration. No single driver fix establishes correctness across all ports.
- Root MIT license does not automatically establish licenses for third-party libraries or vendor SDKs.
- **No third-party implementation code copied into GitHub Gold.**

## Follow-up experiments

1. Pin a commit, execute Ceedling and device-side fuzz harnesses, and record reproducible results.
2. Build supported RP2040 host examples; inject disconnects and transfer timeouts to test endpoint buffer recovery.
3. Compare RP2040 endpoint-abort sequencing with Renesas RUSB2 recovery in upstream October 2026 changes.
4. Track host-class coverage and distinguish upstream CI configuration from successful job results.
5. Inspect downstream Pico SDK, ESP-IDF and Adafruit integrations for useful patches and separate licensing.

**Catalog workflow:** Dossier-first addition to draft PR #7. Promote into `MASTER_LIST.md` and `catalog/tools.json` together after score/schema review and deduplication.
