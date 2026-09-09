# MCUboot — secure boot and firmware update verification

- **Repository:** https://github.com/mcu-tools/mcuboot
- **Organization:** mcu-tools
- **Category:** Embedded systems / secure boot / firmware update / device security
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 (S tier)**
- **Primary license:** Apache-2.0; bundled TinyCrypt is BSD-3-Clause
- **Discovery source:** Recursive GitHub-first follow-up from the Zephyr dossier
- **Inspection date:** 2026-09-07

## Executive assessment

MCUboot is a portable secure bootloader and firmware-update foundation for 32-bit microcontrollers. It is unusually valuable for GitHub Gold because it separates the security-sensitive image verification and boot/update state machine from any one RTOS or board family, then supplies ports and integration layers for Zephyr, Apache Mynewt, Apache NuttX, RIOT, Mbed OS, Espressif, and Cypress/Infineon environments.

This is not merely a boot stub. The repository contains a reusable bootloader core (`boot/bootutil`), serial recovery/update support (`boot/boot_serial`), a firmware image signing/inspection tool (`imgtool`), multiple OS/hardware ports, and a simulator/regression framework (`sim`) that exercises many combinations of signing, encryption, multi-image boot, rollback protection, swap strategies, direct-XIP, RAM-load, and flash-layout behavior.

The project therefore fills a distinct place in the catalog: **device-root-of-trust and resilient firmware-update infrastructure**.

## Why it matters

Embedded update mechanisms are difficult to implement correctly because power loss, partially written images, multiple flash geometries, rollback rules, signature verification, encrypted images, image-slot transitions, recovery paths, and boot-time policy all interact.

MCUboot provides an established implementation of those mechanisms with evidence of active regression testing and maintenance across multiple ecosystems. Its core design can be studied independently from Zephyr and its tooling is reusable even when the final device integration differs.

Particularly valuable GitHub Gold themes include:

- secure firmware image validation before boot;
- signed-image metadata and TLV handling;
- rollback and downgrade controls;
- A/B-style or swap-based image upgrade strategies;
- overwrite-only, direct-XIP, RAM-load, and multi-image configurations;
- encrypted-image handling;
- serial recovery / DFU-style update paths;
- portable flash-area abstractions;
- host-side image signing and inspection;
- simulator-driven regression testing of boot/update state transitions.

## Repository structure and reusable components

### `boot/bootutil`

The core bootloader implementation. This is the most important reusable subsystem and contains the image-selection, validation, swap/update, trailer/state, flash-area, and boot decision logic that higher-level ports invoke.

The architectural value is the separation between **boot policy/state-machine logic** and platform-specific flash/hardware access.

### `boot/boot_serial`

Implements serial bootloader management and firmware-update/recovery behavior. Recent maintenance shows this path receives active correctness hardening rather than existing only as an example.

On 2026-09-03 upstream changes included:

- validation that a supplied image ID is valid;
- validation that a completed update is actually complete and originated from an upload before decryption handling;
- correction of serial DFU timeout accounting so the entire read-loop iteration is charged rather than only time inside the transport read.

The timeout fix included an upstream measurement on STM32C071 showing a no-activity boot dropping from 22.6 seconds to 6.0 seconds for a configured 5-second serial wait, against roughly 1 second of normal boot overhead. This benchmark is **upstream-reported and was not reproduced by GitHub Gold**.

### `scripts/imgtool.py` / `imgtool`

Host-side firmware image tooling used to securely sign MCUboot-compatible images and inspect their metadata.

The latest stable release, v2.4.0, added among other things:

- `--custom-tlv-file` for binary custom TLV content;
- `dumpinfo --format` with human/YAML/JSON output;
- Intel HEX input support for `dumpinfo`.

This makes `imgtool` independently useful as a build/release-pipeline component even when the bootloader itself is consumed through another ecosystem.

### `sim`

A host-side simulator and regression environment for bootloader behavior. The simulator CI is one of the strongest evidence sources in the repository because it covers combinations rather than merely proving compilation.

The current matrix explicitly exercises combinations involving:

- ECDSA, RSA/RSA-3072, Ed25519, and PSA-backed ECDSA;
- multiple encrypted-image modes including RSA, key-wrap, EC256/X25519 paths, and AES-256 variants;
- overwrite-only updates;
- swap-move and swap-offset;
- validate-primary-slot;
- bootstrap behavior;
- downgrade prevention and hardware rollback protection;
- RAM-load and direct-XIP;
- multi-image configurations;
- multiple alignment constraints;
- logical-sector abstractions at 4 KiB and 128 KiB;
- custom crypto and custom encryption backends;
- Mbed TLS 4.x-oriented PSA paths.

This is meaningful working evidence because bootloader failures often occur at the intersection of update strategy, flash geometry, cryptography, and image topology.

### Fault-injection hardening tests

The dedicated `FIH hardening` workflow runs a matrix across release/min-size builds, several instruction-skip sizes, signature-damage tests, and multiple configured FIH levels.

This does not prove resistance to every physical fault-injection technique, but it is stronger evidence than a project merely claiming fault-injection resistance without automated regression coverage.

### Platform integrations

The repository documents integrations/ports for:

- Zephyr;
- Apache Mynewt;
- Apache NuttX;
- RIOT (boot target support noted by upstream);
- Mbed OS;
- Espressif;
- Cypress/Infineon.

The value here is portability of the boot/update model rather than dependence on one embedded OS.

## Stable release and maintenance evidence

The latest stable GitHub release inspected is **MCUboot v2.4.0**, published **2026-04-23**.

Important v2.4.0 changes include:

- compiled-in key support for Zephyr builds;
- external PSA crypto backend support;
- selectable legacy Mbed TLS vs PSA RSA verification paths;
- ECDSA support in the Zephyr port using Mbed TLS;
- broader sysbuild support, including arbitrarily named and multiple MCUboot images;
- additional flash/devicetree layout support;
- external-flash chainloading support for a documented STM32H7 variant;
- multiple Espressif, Mbed, Mynewt, CMake, logging, image-validation, and swap correctness fixes;
- correction of image-size validation to include protected TLV size;
- correction of a swap-move bootstrap copy-size calculation that could otherwise over-copy when primary and secondary region sizing differed.

Development remained active through **2026-09-07**. Recent commits include a Zephyr runtime-source sample test fix and release-note maintenance; on 2026-09-03 several boot-path correctness fixes landed, including boot-serial validation, swap-state initialization, and timeout behavior.

## Working evidence

Evidence observed in upstream repository-native sources:

1. Dedicated GitHub Actions workflows for simulator tests, fault-injection-hardening tests, Zephyr builds, Espressif, Mynewt, `imgtool`, and Python linting.
2. Simulator CI uses a large feature-combination matrix covering signatures, encryption, update strategies, multiple image modes, rollback behavior, flash geometry, and alternate crypto backends.
3. Dedicated FIH regression matrix exercises signature-damage/instruction-skip scenarios across build types and hardening levels.
4. Stable v2.4.0 release with detailed correctness and portability changes.
5. Current maintenance through 2026-09-07.
6. Repository documentation identifies the bootloader core, serial updater, image tooling, simulator, and multiple platform ports explicitly.

### Supply-chain caveat

The inspected workflows use mutable Action tags such as `actions/checkout@v4`, `actions-rs/toolchain@v1`, and `docker/login-action@v3` rather than immutable commit-SHA pinning. That is a supply-chain hygiene weakness relative to projects whose CI dependencies are fully pinned.

The simulator also recursively checks out submodules, increasing the dependency/provenance surface that a downstream high-assurance build should inventory and pin deliberately.

## Security boundary and caveats

MCUboot is security-critical code. A high Gold score means the repository shows unusually strong utility, architecture, maintenance, testing, and reuse evidence; it does **not** mean every MCUboot configuration is secure or suitable for every threat model.

Important caveats:

- boot security depends on how signing keys are generated, stored, and provisioned;
- downgrade/rollback policy must be configured correctly for the product threat model;
- flash layout and boot/update strategy must match actual hardware erase/write semantics;
- encrypted firmware does not replace signature/authenticity verification;
- serial/USB recovery paths expand the pre-OS attack surface;
- hardware root-of-trust, immutable boot ROM behavior, debug-port policy, secure key storage, and anti-rollback counters are platform-specific;
- physical fault-injection resistance cannot be established solely by the repository's software FIH tests;
- third-party crypto libraries and platform HALs have their own security and update lifecycles.

Recent fixes to boot-serial validation, swap-state initialization, image-size checking, and copy sizing are positive maintenance signals but also demonstrate why boot/update state machines require continuing scrutiny.

## License

The repository root license is **Apache License 2.0**.

The root LICENSE additionally states that the product bundles **TinyCrypt**, which is licensed under the **3-clause BSD license**, with its own license under `ext/tinycrypt/LICENSE`.

No MCUboot, TinyCrypt, firmware, key material, or other upstream source was copied into GitHub Gold.

Any future source reuse should preserve Apache-2.0 notices and independently review the licenses of bundled/submodule/platform-specific components actually incorporated.

## Install / runtime context

MCUboot is primarily integrated as firmware source into a target's embedded build system rather than installed as a generic desktop application.

The host-side `imgtool` is a Python-distributed utility and is separately published on PyPI according to upstream README metadata.

Actual build prerequisites vary by selected platform port, crypto backend, target architecture, and RTOS/build system.

## Platforms and languages

Primary implementation is C with Python host tooling and build/test support around it. Supported integration targets span multiple 32-bit MCU ecosystems and operating systems rather than a single vendor family.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Solves secure boot and resilient firmware update, a foundational embedded requirement. |
| Working Evidence | 5/5 | Extensive simulator combination matrix, dedicated FIH tests, platform workflows, stable release history, active fixes. |
| Reusability | 5/5 | Portable boot core, flash abstraction, serial updater, Python image tool, simulator, multiple RTOS/vendor ports. |
| Novelty | 4/5 | Secure boot/update is established engineering, but MCUboot's portable multi-platform implementation and regression depth are unusually valuable. |
| Documentation | 5/5 | Clear architecture/component pointers, platform guides, simulator docs, release notes, and integration documentation. |
| Maintenance | 5/5 | Active through 2026-09-07 with security/correctness-sensitive maintenance. |
| **Total** | **29/30** | **Provisional S tier** |

## Verification boundary

GitHub Gold performed **source/document/workflow/release/history inspection only**.

GitHub Gold did **not**:

- clone or build MCUboot;
- run the simulator or FIH test suites;
- execute `imgtool`;
- generate/sign/verify a firmware image;
- compile or flash a target board;
- exercise A/B or swap-based updates on real flash;
- simulate power loss during update;
- test serial/USB DFU recovery;
- reproduce the STM32C071 timeout measurement;
- attempt fault injection;
- validate key provisioning or hardware anti-rollback mechanisms;
- fuzz image/TLV/serial parsers;
- audit the cryptographic implementations;
- independently verify release archives or submodule provenance.

Claims above are limited to evidence explicitly observed in upstream repository sources, workflows, release notes, and commit history.

## Related projects already in GitHub Gold

- **zephyrproject-rtos/zephyr** — primary embedded-RTOS ecosystem and recursive discovery source.
- **PX4/PX4-Autopilot** — safety/reliability-sensitive embedded robotics firmware that illustrates the broader need for controlled firmware lifecycle infrastructure.
- **sigstore/cosign / sigstore-go** — artifact-signing and verification infrastructure at a different software-supply-chain layer.

## Follow-up research

1. Trace MCUboot image format and TLV verification from `imgtool` output to boot-time validation.
2. Inspect trailer/swap-state invariants for power-loss recovery under swap-move and swap-offset.
3. Inspect anti-rollback state and hardware counter interfaces.
4. Inspect serial/USB DFU parser boundaries and recovery authorization assumptions.
5. Review the fault-injection-hardening implementation and what the automated FIH tests actually mutate/skip.
6. Compare TinyCrypt, Mbed TLS legacy, PSA, and custom crypto backend boundaries.
7. Inspect multi-image dependency/version semantics.
8. Evaluate whether `imgtool` merits its own component-level catalog entry after direct CLI/test inspection.
9. Inspect MCUboot's Zephyr sysbuild integration for multi-bootloader/multi-image deployments.
10. Consider a future power-loss/state-machine property-testing harness as a research idea rather than copied upstream code.

## Verdict

**VERIFIED — provisional S / 29.**

MCUboot is GitHub Gold because its value lies in a deeply reusable combination of secure image tooling, portable boot/update state machinery, multiple embedded integrations, simulator-driven regression coverage, and ongoing correctness maintenance. Its strongest lesson is architectural: firmware authenticity is only one part of the problem; trustworthy field updates also require carefully tested state transitions, flash-layout handling, rollback policy, recovery behavior, and platform boundaries.