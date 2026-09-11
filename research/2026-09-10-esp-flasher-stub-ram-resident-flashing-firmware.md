# ESP Flasher Stub — RAM-resident flashing firmware for Espressif chips

- **Repository:** https://github.com/espressif/esp-flasher-stub
- **Author / organization:** Espressif Systems
- **Category:** embedded tooling / flashing / ROM-loader augmentation / ESP32 / ESP8266 / firmware infrastructure
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **Research date:** 2026-09-10
- **Discovery source:** Recursive follow-up from `espressif/esptool` and `espressif/esptool-js`

## Executive summary

`espressif/esp-flasher-stub` is the current standalone source repository for Espressif's RAM-resident flasher stubs. These are small firmware programs uploaded into an ESP chip's RAM by host tools such as `esptool` and `esp-serial-flasher`. Once running, the stub takes over communication from the chip's ROM bootloader and provides faster flash operations plus functionality that may not exist in the ROM loader.

Upstream states that this repository replaced the deprecated legacy esptool flasher-stub project and became the default flasher stub beginning with esptool v5.3.

This is unusually valuable as a reusable embedded-systems reference because it sits directly on the boundary between a host-side flashing tool, a chip ROM loader, transport framing, flash-controller operations, linker-controlled RAM placement, generated firmware metadata, and multi-target cross-compilation.

The project is not merely a collection of prebuilt blobs. Its source, build scripts, architecture documentation, host unit tests, target-test harness, release pipeline, JSON generation tools, plugin ABI, and cross-chip target definitions are all present upstream.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Core flashing infrastructure used by Espressif tooling; directly useful for ESP provisioning and development workflows. |
| Working Evidence | 5/5 | CI builds all supported stubs, publishes generated JSON artifacts, runs native host tests, documents target hardware tests, and has versioned releases consumed by related tooling. |
| Reusability | 5/5 | Modular transport, framing, command-dispatch, linker/build, JSON-generation, plugin, and target-abstraction pieces are broadly instructive for embedded tooling. |
| Novelty | 4/5 | RAM-resident loader stubs are an established pattern, but the multi-transport architecture, generated host-consumable format, plugin ABI, and broad target coverage are technically distinctive. |
| Documentation | 5/5 | README, architecture guide, development guide, plugin documentation, testing documentation, changelog, and release workflow are present. |
| Maintenance | 4/5 | Active 2026 maintenance and releases are evident, including v1.2.2 on 2026-08-19; current inspected history is several weeks behind this research date rather than same-day active. |
| **Total** | **28/30** | **S tier** |

## What it does

The flasher stub is uploaded by a host flashing program into volatile RAM on a supported Espressif SoC. It then initializes a transport, performs a handshake with the host, accepts framed commands, dispatches operations, and accesses flash or other low-level services through `esp-stub-lib`.

Upstream documents these main stages:

1. Upload the stub into chip RAM.
2. Initialize the selected transport.
3. Exchange an `OHAI` handshake with the host.
4. Enter a command-processing loop.
5. Execute flash, memory, register, SPI, and extension/plugin operations.

UART, USB-Serial-JTAG, and USB-OTG use SLIP-framed command streams. SDIO uses raw command frames.

## Supported chip families observed

The README currently lists:

### Xtensa

- ESP32
- ESP32-S2
- ESP32-S3

### RISC-V

- ESP32-C2
- ESP32-C3
- ESP32-C5
- ESP32-C6
- ESP32-C61
- ESP32-H2
- ESP32-H4
- ESP32-P4
- ESP32-P4 rev1
- ESP32-S31

### Xtensa LX106

- ESP8266

This is upstream-declared target support. GitHub Gold did not independently flash every target.

## Architecture

The documented architecture is small but cleanly layered:

- transport layer
- receive/frame buffering
- SLIP or SDIO framing
- command parsing and dispatch
- optional runtime-loaded plugin dispatch
- low-level `esp-stub-lib` hardware operations

Important source files described upstream include:

- `src/main.c` — entry point, BSS initialization, command loop
- `src/frame_buffer.c` / `.h` — shared double-buffered RX storage
- `src/slip.c` / `.h` — SLIP encoding/decoding
- `src/command_handler.c` / `.h` — command parsing, dispatch, response handling
- `src/commands.h` — command IDs and response codes
- `src/transport.c` / `.h` — transport detection, initialization, RX/TX abstraction
- `src/plugin_table.h` — plugin Function Pointer Table ABI
- `src/nand_plugin.c` — NAND plugin implementation
- `src/endian_utils.h` — byte-order helpers
- `src/ld/` — per-chip and common linker scripts

## Build and linker model

The firmware is a bare-metal C application built with CMake and Ninja. Target selection is explicit through `-DTARGET_CHIP=<chip>`.

The build system:

1. validates the target;
2. chooses the proper Xtensa or RISC-V compiler prefix;
3. applies architecture-specific compiler flags;
4. links against a target-specific RAM layout;
5. applies target-local size workarounds where required;
6. invokes `tools/elf2json.py` to convert build output into the JSON format consumed by host tools.

Per-chip linker scripts define instruction/data RAM placement and include a common linker description for `.text`, `.bss`, `.data`, and the `esp_main` entry point.

That makes the repository useful beyond ESP flashing: it is a compact reference for host-uploaded firmware, deterministic RAM placement, cross-target linker layouts, and post-link artifact generation.

## Plugin architecture

The stub has a runtime-loadable plugin mechanism built around a Function Pointer Table (FPT).

Upstream documents an opcode range of `0xD5` through `0xEF` for plugin-dispatched commands. Entries initially point to an unsupported-handler function. A host such as esptool can patch the relevant FPT entries and upload a plugin before transferring control.

Plugin handlers receive a command context containing the selected transport operations, which keeps plugin streaming code transport-independent.

For targets that currently support plugins, the plugin load address is derived from the base stub's final memory usage. The build chain therefore:

1. builds the base stub ELF;
2. calculates safe plugin addresses from that ELF;
3. emits linker data for the plugin;
4. builds/relinks the plugin;
5. embeds the plugin into the generated JSON stub artifact.

The README currently identifies NAND-flash support as a preview plugin path and the architecture guide describes ESP32-S3 as the currently supported target for that plugin.

## Useful reusable components and ideas

### Host-uploaded RAM firmware pattern

The overall design is a strong reference for temporarily extending a device ROM loader without permanently installing firmware.

### SLIP framing implementation

`src/slip.c` and related buffering logic are valuable references for compact byte-stream framing over UART and USB serial transports.

### Transport abstraction

`transport.c` separates UART, USB, and SDIO handling from command execution. This is a reusable embedded architecture pattern for code that must work across multiple physical/control transports.

### Command dispatcher

The command handler and ID definitions illustrate how a small loader can expose a constrained binary control protocol rather than a general shell.

### Linker-script organization

Per-target linker files plus a shared linker description are useful examples for maintaining RAM-only firmware across many SoCs.

### ELF-to-JSON generation

`tools/elf2json.py` converts linked output into a structured artifact that host-side tools can consume. This is a useful host/firmware packaging pattern.

### Plugin address computation

`tools/compute_plugin_addrs.py` derives extension placement from the base ELF. This is a particularly interesting technique for dynamically extending very small RAM-resident programs while avoiding overlap.

### Size-regression tooling

`tools/compare_sizes.py` and the PR size-report workflow show disciplined monitoring of constrained firmware size across changes.

### npm packaging of generated firmware assets

The project generates an npm package containing stub JSON artifacts, making the same low-level firmware consumable from JavaScript/TypeScript tooling such as browser-oriented flashing stacks.

## Build and runtime requirements

Upstream documents:

- CMake
- Ninja
- Espressif Xtensa/RISC-V cross toolchains
- ESP8266 Xtensa LX106 toolchain
- Python
- `pyelftools`
- recursive git submodules

Target tests additionally require esptool to convert/load target test binaries.

A convenience Linux AMD64 script downloads toolchains into a local `toolchains` directory, but consumers should inspect remote/download behavior and pin or validate toolchain provenance when reproducibility matters.

## Testing and verification evidence

### Automated all-target builds

The current `Build and release` GitHub Actions workflow:

- checks out recursive submodules;
- configures Python 3.13;
- installs `pyelftools`;
- installs the required cross toolchains;
- runs `tools/build_all_chips.sh`;
- uploads generated `esp*.json` stub artifacts;
- generates an npm package from the built stubs;
- produces per-PR stub-size reports;
- creates draft GitHub releases from tagged builds.

This is strong evidence that the checked-in source can be cross-built into consumable artifacts across the project's supported target matrix.

### Host unit tests

A separate `Host Tests` workflow runs on Ubuntu 24.04 and executes `unittests/host/run-tests.sh` after checking out submodules and installing the native build/test dependencies.

The testing documentation identifies Unity and CMock as the test framework/mocking stack and describes native host tests for logic such as SLIP handling.

### Target hardware tests

The repository also contains a target-test harness capable of cross-compiling Unity tests, loading them onto actual ESP hardware, and parsing the resulting test output.

This is an upstream capability and documented developer workflow. GitHub Gold did not run those hardware tests and did not verify that every current target is exercised by hosted CI hardware.

## Release and artifact evidence

The latest release inspected during this pass is:

- **v1.2.2**
- published **2026-08-19**

The release exposes per-chip JSON stub artifacts. GitHub's release metadata includes SHA-256 digest fields for uploaded artifacts.

Recent inspected history around that release includes:

- ESP32-P4 power/flash initialization correction through an `esp-stub-lib` update;
- ESP32-S31 support and 4-byte flash-addressing work;
- version bumps/releases through v1.2.2.

GitHub Gold did not independently download and hash every artifact.

## Maintenance signals

Positive signals:

- repository is not archived;
- current standalone architecture replaced the legacy esptool stub project;
- active 2026 releases;
- active target additions and silicon-specific fixes;
- CI builds all supported targets;
- host tests;
- generated release artifacts;
- changelog and formal release workflow;
- pre-commit enforcement;
- firmware-size regression reporting;
- npm publication path;
- detailed architecture and contributor documentation.

Maintenance is scored 4/5 rather than 5/5 because the latest inspected repository activity is 2026-08-19, several weeks before this research date.

## License

The repository README and source-header policy specify dual licensing:

- Apache-2.0 OR
- MIT

The root includes both `LICENSE-APACHE` and `LICENSE-MIT`.

However, this repository uses submodules:

- `espressif/esp-stub-lib`
- `ThrowTheSwitch/CMock`
- `ThrowTheSwitch/Unity`

Those dependencies retain their own upstream licensing and attribution requirements. Any source extraction or redistribution that includes submodule-derived material requires component-level license review.

No source, generated firmware, release artifact, toolchain, or submodule code was copied into GitHub Gold during this pass.

## Relationship to esptool

This repository is now the source-of-truth firmware side of an important host/device pair:

- `espressif/esptool` — Python host-side flashing/provisioning toolkit
- `espressif/esp-flasher-stub` — RAM-resident firmware executed on the target

Upstream states that this standalone stub became the default beginning with esptool v5.3.

The relationship is important because some capabilities commonly attributed to "esptool" are actually split across host logic, ROM functionality, and uploaded stub functionality.

## Relationship to esptool-js

The release process also produces assets suitable for npm packaging. This makes the same target-side stub architecture consumable from JavaScript/TypeScript host tooling.

A future cross-project audit should verify precisely how Python esptool and esptool-js select/version stub JSON files and whether both enforce equivalent chip/revision compatibility checks.

## Relationship to esp-serial-flasher

The README explicitly lists `esp-serial-flasher` as another host consumer. This makes the stub relevant beyond the Python and browser toolchains and suggests the on-device protocol is an ecosystem interface worth documenting carefully.

## Security and safety considerations

This is low-level device programming infrastructure. Flash, register, memory, and eFuse-related host workflows can permanently alter a target or render it unbootable if misused.

The stub itself runs in volatile RAM, which is useful from a recoverability perspective, but operations initiated through it can still modify persistent flash or other device state.

Important trust boundaries include:

- integrity of the host flashing tool;
- integrity/provenance of the selected stub JSON artifact;
- chip/revision detection;
- loader memory addresses and overlap checks;
- command length and frame validation;
- plugin load addresses and FPT patching;
- transport framing and malformed input handling;
- flash-size/address-mode handling;
- host-selected erase/write ranges;
- silicon-specific ROM workaround logic;
- supply-chain integrity of downloaded cross toolchains and submodules.

This dossier catalogs the project for legitimate development, recovery, interoperability, provisioning, and embedded research.

## Verification performed by GitHub Gold

GitHub Gold inspected:

- repository metadata;
- root tree;
- README;
- architecture documentation;
- development/testing documentation;
- GitHub Actions workflow definitions;
- unit-test documentation;
- submodule declarations;
- recent commit history;
- release metadata;
- license declarations.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- install the cross toolchains;
- build any flasher stub;
- run host unit tests;
- run target tests;
- connect to an ESP chip;
- upload a stub into RAM;
- flash, erase, or read a physical device;
- exercise UART, USB, or SDIO transports;
- exercise NAND plugin support;
- fuzz SLIP, command, plugin, or transport parsing;
- reproduce silicon-specific fixes;
- verify toolchain-download provenance;
- independently hash release artifacts;
- audit the complete `esp-stub-lib` implementation;
- verify every supported chip/revision combination.

Claims about those capabilities are therefore attributed to repository source, CI definitions, documentation, release artifacts, and upstream project history rather than local execution by GitHub Gold.

## Caveats and limitations

- Hardware support can be chip- and silicon-revision-specific.
- A successful cross-build is not equivalent to successful programming on every physical target.
- Some behavior is delegated into the `esp-stub-lib` submodule.
- Target hardware tests exist, but this pass did not establish a hosted hardware-in-loop matrix covering all targets.
- The NAND plugin is explicitly preview-level upstream.
- Runtime plugins increase the importance of load-address, ABI, bounds, and provenance validation.
- Downloaded toolchains are part of the build trust chain.
- Device-programming commands can be destructive even when the stub itself is RAM-resident.

## Strongest follow-up research

1. Deep-audit `espressif/esp-stub-lib`, including ROM wrapper boundaries and per-chip flash/security abstractions.
2. Compare the stub JSON format and version-selection behavior across Python esptool, esptool-js, and esp-serial-flasher.
3. Inspect whether release artifacts are reproducible from a tagged checkout and pinned toolchain set.
4. Map command IDs, argument validation, response formats, and malformed-frame behavior.
5. Inspect plugin FPT patching, plugin binary bounds, ABI versioning, and NAND-plugin isolation.
6. Review target-test coverage by chip and determine what is actually exercised on physical hardware in CI or internal infrastructure.
7. Review `tools/setup_toolchains.sh` for pinned versions, hashes, transport security, and reproducibility.
8. Rotate the next discovery run away from Espressif tooling to preserve catalog breadth.

## Verdict

**VERIFIED — S / 28.**

`espressif/esp-flasher-stub` is a high-value embedded-tooling project because it exposes the target-side half of modern Espressif flashing as auditable source rather than an opaque binary. Its combination of broad SoC support, all-target CI builds, native unit tests, documented target tests, RAM-only execution, transport abstraction, linker-controlled memory layouts, generated JSON artifacts, runtime extension architecture, and integration with several host flashing stacks makes it legitimate GitHub Gold.
