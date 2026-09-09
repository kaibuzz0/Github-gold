# OpenRTX modular amateur-radio firmware and M17 stack

- **Repository:** https://github.com/OpenRTX/OpenRTX
- **Author / Org:** OpenRTX
- **Category:** embedded firmware / amateur radio / digital voice / M17 / hardware abstraction / off-grid communications
- **Evidence:** VERIFIED
- **Provisional Gold score:** **27 / 30 — S tier**
  - Utility: 4/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 4/5
- **Primary license:** GPL-3.0-or-later for OpenRTX sources, with multiple separately licensed bundled components and platform files documented through REUSE metadata.
- **Discovery source:** independent GitHub-first category rotation from mapping into embedded/off-grid radio infrastructure. No YouTube-derived technical claim is used in this dossier.

## Executive assessment

OpenRTX is a modular open-source firmware stack for digital amateur-radio devices. Upstream explicitly describes it as free/open-source radio firmware designed around modularity, flexibility, and performance, while also warning that it is **highly experimental** and still under development. That warning matters: this dossier treats OpenRTX as a technically strong firmware/research platform with unusually reusable radio-protocol and hardware-abstraction components, not as a claim that every supported radio/function is production-stable.

The project is especially valuable because it joins several normally separate concerns in one codebase: radio-specific board support, MCU/platform abstraction, display/UI logic, channel/contact storage, GPS, audio/DSP, programming/CPS support, multiple packaging/flashing formats, a Linux emulation/runtime target, and a substantial implementation of the open M17 digital-voice protocol.

The strongest GitHub Gold component is the **M17 protocol/DSP stack**. Current source contains dedicated frame encoder/decoder code plus modulation, demodulation/DSP, callsign handling, metadata text handling, Golay coding, puncturing, interleaving, decorrelation and related protocol primitives. The M17 operating-mode layer composes the protocol encoder/decoder into the radio runtime rather than leaving it as disconnected reference code.

## Why it matters

OpenRTX is useful in several ways beyond flashing alternative firmware onto one particular handheld radio:

1. **Open digital-radio reference implementation.** M17 is a libre digital voice/data protocol, and OpenRTX contains an end-to-end embedded implementation rather than only a desktop encoder/decoder.
2. **Cross-radio portability architecture.** The build system emits firmware for multiple radio families and also builds a Linux target, providing concrete examples of how a common radio application can be separated from platform- and device-specific code.
3. **Reusable DSP/FEC components.** The M17 source tree includes codecs/protocol framing, forward-error-correction primitives, modulation/demodulation support and associated tests.
4. **Embedded persistence and update primitives.** Recent maintenance touches include nonvolatile-memory handling and XMODEM transfer logic, both relevant to constrained-device design beyond radio.
5. **Off-grid communications research value.** In amateur-radio use, the firmware can support infrastructure-independent local communications, subject to radio regulations, band plans, equipment constraints and operator licensing requirements.

## Concrete components inspected

### M17 protocol stack

Repository code search shows a dedicated `openrtx/src/protocols/M17/` implementation including at least:

- `FrameEncoder.cpp`
- `FrameDecoder.cpp`
- `Modulator.cpp`
- `DSP.cpp`
- `Golay.cpp`
- `Callsign.cpp`
- `MetaText.cpp`

Corresponding headers expose the protocol pieces, while `openrtx/src/rtx/OpMode_M17.cpp` integrates them into the operational radio mode.

The implementation references distinct protocol transforms rather than treating M17 as one monolithic codec: frame encoding pulls in code puncturing, decorrelation and interleaving, while decoding pulls in Golay decoding, interleaving and decorrelation. That decomposition is useful for protocol study and component-level reuse, subject to GPL obligations.

### Multi-target build system

The main GitHub Actions workflow performs several layers of validation:

- configures a coverage-enabled Meson build;
- runs unit tests with `meson test`;
- generates coverage output;
- builds a Zephyr target for an ESP32-S3-oriented radio configuration;
- builds Linux firmware/runtime variants;
- cross-compiles multiple Cortex-M4 and Cortex-M7 radio targets;
- packages multiple output formats including `.bin`, `.dfu`, `.sgl`, wrapped firmware images and UF2 artifacts.

Targets visible in the current workflow include CS7000/CS7000P, DM1701, DM1801, MD-3x0, MD-9600, MD-UV3x0, MOD17, GD77, RT-4D and Linux builds. This is upstream CI evidence that the codebase is designed as a multi-device firmware platform rather than a single-board proof of concept.

### Unit-test surface

The repository uses Catch2 unit tests under `tests/unit/`, registered through the build system. Current source search exposes targeted tests for:

- M17 Golay encode/decode behavior;
- M17 Viterbi decoding with punctured convolutional encoding;
- M17 demodulator correlation behavior;
- root-raised-cosine filter behavior;
- M17 packet clearing/state behavior;
- callsign encode/decode behavior;
- M17 metadata text, including out-of-order blocks;
- CPS initialization/read-back and contact insertion/order;
- GPS/minmea coordinate conversion;
- DSP oversampling;
- Linux audio/input-stream behavior;
- UI standby/backlight timing.

This is stronger working evidence than documentation-only claims. GitHub Gold did not execute these tests in this research pass.

## Releases and maintenance

The latest release observed during this pass is **OpenRTX v0.4.4**, published **May 1, 2026** and marked prerelease by GitHub. It includes target-specific firmware images for multiple radios plus a Linux binary. GitHub currently exposes SHA-256 digest metadata for the inspected release assets.

Source maintenance is more recent than that release. The latest commits observed on **September 5, 2026** include fixes for:

- an XMODEM send-buffer overflow during padding;
- an emulated-EEPROM entry-list overflow in `swapBlock`;
- a buffer overflow in EEEP read handling.

An August 2026 change also added an RT-4D CPS driver. The presence of recent memory-safety fixes is both a positive maintenance signal and a reminder that this remains experimental embedded firmware.

## Licensing

The repository README summarizes the main firmware as GPLv3, while the repository's `REUSE.toml` is more precise and identifies OpenRTX sources as **GPL-3.0-or-later**.

The project is not license-homogeneous. REUSE annotations identify separately licensed material including, among others:

- Miosix sources under GPL-2.0-or-later;
- QDecoder code under MIT;
- CMSIS/platform material under Apache-2.0, BSD-3-Clause, BSD-3-Clause-Clear or vendor terms depending on subtree;
- STM32F4 USB material under ST's MCD-ST Liberty license;
- minmea under WTFPL;
- OpenOCD scripts under GPL-2.0-or-later;
- `dfu-convert.py` under LGPL-3.0-only;
- QRCode code under MIT.

**No OpenRTX source was copied into GitHub Gold.** Any future extraction/adaptation must identify the exact upstream file and preserve its applicable SPDX/license obligations rather than assuming every file inherits the same root license.

## Verification performed

GitHub Gold inspected:

- root README and upstream project claims/disclaimers;
- current GitHub Actions build/test workflow;
- release metadata and assets;
- recent commit history;
- REUSE licensing metadata;
- M17 source/component locations through repository code search;
- unit-test locations and representative test cases through repository code search.

This supports VERIFIED status for the existence and upstream continuous build/test evidence of the architecture described here.

## Verification boundary

GitHub Gold **did not**:

- build OpenRTX locally;
- execute its unit tests;
- flash firmware to any radio;
- transmit or receive RF;
- validate M17 interoperability over the air;
- verify radio-specific feature matrices;
- test GPS, CPS, display, audio, modem or codec hardware;
- reproduce the recent overflow bugs or confirm the fixes independently;
- independently hash release artifacts;
- validate Linux emulation/runtime behavior;
- test Zephyr output on ESP32-S3 hardware;
- perform a memory-safety, RF-compliance, security or regulatory audit.

Upstream's own warning that the firmware is highly experimental remains controlling context.

## Caveats and risks

- **Experimental firmware:** upstream explicitly says OpenRTX is highly experimental and may lack expected functionality.
- **Hardware-specific risk:** flashing unofficial firmware can make a device unusable or require recovery procedures.
- **Radio regulation:** legal transmit frequencies, power, emission modes, equipment restrictions, call-sign requirements and operator licensing vary by jurisdiction. Catalog inclusion is for legitimate amateur-radio, interoperability, education and emergency/off-grid research, not unauthorized transmission.
- **Mixed licensing:** exact-file license review is required before extraction or adaptation.
- **Mutable GitHub Actions references:** the inspected CI uses versioned action tags such as `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`, `mikepenz/action-junit-report@v6`, `devcontainers/ci@v0.3` and `zephyrproject-rtos/action-zephyr-setup@v1` rather than immutable commit SHAs. This is weaker supply-chain pinning than the strictest projects in GitHub Gold.
- **Recent overflow fixes:** current maintenance directly addresses buffer/entry-list overflows, so downstream users should track updates closely.

## Gold score rationale

### Utility — 4/5

Useful for alternative amateur-radio firmware, open digital voice, embedded-device research and off-grid communication stacks. Utility is reduced from 5 because hardware support/features vary and upstream still labels the firmware experimental.

### Working Evidence — 5/5

The repository has automated unit testing, coverage generation, multi-target cross-compilation, Linux builds, a Zephyr build path, packaged firmware artifacts and release binaries. This is strong upstream evidence even though GitHub Gold did not execute it independently.

### Reusability — 5/5

The decomposed M17 stack, DSP/FEC primitives, platform abstractions, CPS/persistence logic and Linux target provide unusually strong component-level research/reuse value. GPL and per-file license obligations constrain how reuse must be performed, not its technical value.

### Novelty — 5/5

A libre, multi-radio embedded firmware platform with an integrated M17 digital-voice stack is unusual and technically distinctive.

### Documentation — 4/5

The project has substantial website/documentation links, compilation/flashing guidance, development status, contribution guidance, a changelog and explicit disclaimers. Some important details live outside the repository README and the experimental status means device-specific expectations need careful checking.

### Maintenance — 4/5

Active fixes continued through September 5, 2026, including memory-safety work and new device/CPS support. The score is held at 4 because the latest inspected GitHub release is a prerelease from May and upstream still characterizes the firmware as experimental.

## Related projects and recursive leads

- **M17 Project / protocol ecosystem** — validate OpenRTX framing/modulation behavior against independent M17 implementations and specifications.
- **v0l/radio_tool** — firmware flashing/programming utility referenced directly by OpenRTX.
- **OpenRTX hardware documentation and development-status pages** — map exact support per radio and feature.
- **Zephyr-based TTWR Plus target** — inspect how OpenRTX is being adapted to a mainstream RTOS and ESP32-S3-class hardware.
- **Miosix kernel integration** — inspect scheduling, device abstractions and why some targets use Miosix versus newer Zephyr work.
- **CPS/codeplug subsystem** — contact/channel database formats, ordering, validation and radio-specific programming drivers.
- **XMODEM implementation** — inspect the September 2026 overflow fix and packet/padding invariants as a reusable serial-transfer primitive.
- **EEEP/emulated EEPROM subsystem** — inspect swap/recovery/wear behavior and the recent bounds fixes.
- **Linux target** — map which hardware services are simulated or abstracted and whether it can serve as a deterministic protocol/UI test harness.

## Recommended next pass

The best next OpenRTX-specific work is not another top-level summary. It is a component audit of **M17 FrameEncoder/FrameDecoder + their tests**, followed by the **XMODEM and EEEP overflow fixes** to capture concrete defensive embedded-programming invariants. After that, rotate independent discovery again rather than letting the catalog become radio-heavy.
