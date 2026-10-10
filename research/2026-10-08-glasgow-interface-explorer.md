# Glasgow Interface Explorer — programmable electronics interface workstation

- **Upstream:** https://github.com/GlasgowEmbedded/glasgow
- **Research date:** 2026-10-08
- **Author:** GlasgowEmbedded contributors (project metadata names Catherine / whitequark)
- **Category:** Embedded hardware / FPGA gateware / digital protocol instrumentation / developer tooling / open hardware
- **Evidence:** **PROMISING** — source implementation, extensive tests and build workflow, but no independent device execution or checked successful CI run.
- **Provisional Gold:** **S / 26** (Utility 5; Working Evidence 3; Reusability 5; Novelty 5; Documentation 4; Maintenance 4). Tier is provisional pending canonical promotion.
- **License:** software package declares `0BSD OR Apache-2.0`; root includes both licenses. Inspect each hardware design, firmware, vendored dependency, and individual file before reuse.
- **Discovery:** Independent GitHub-first discovery; no YouTube transcript attribution.

## What it does and why it matters

Glasgow is a programmable hardware/software interface explorer rather than a fixed-function logic analyzer. Its Python host, Amaranth HDL gateware, firmware and open hardware are designed to make many electrical/digital protocols inspectable and implementable through applets. The repository's software package labels itself **Development Status: 3 - Alpha**; do not infer production stability from its breadth. A physical Glasgow board is normally needed for actual interface measurements, although tests and gateware builds can be run without hardware.

## Reusable component inventory (exact upstream paths)

| Component | Upstream location | Reuse potential |
| --- | --- | --- |
| Gateware blocks | https://github.com/GlasgowEmbedded/glasgow/tree/main/software/glasgow/gateware | Amaranth SPI, I2C, UART, JTAG, SWD, QSPI, CRC, stream, analyzer and clock primitives |
| Protocol parsers | https://github.com/GlasgowEmbedded/glasgow/tree/main/software/glasgow/protocol | JEDEC SFDP, ONFI, JTAG SVF, BSDL, GDB remote, YMODEM and more |
| SPI flash SFDP parser | https://github.com/GlasgowEmbedded/glasgow/blob/main/software/glasgow/protocol/sfdp.py | Typed JEDEC parameter structures; source says base JESD216 and JESD216A only |
| Memory applets | https://github.com/GlasgowEmbedded/glasgow/tree/main/software/glasgow/applet/memory | 24x/25q flash, ONFI, PROM, floppy protocol workflows |
| Interface applets | https://github.com/GlasgowEmbedded/glasgow/tree/main/software/glasgow/applet/interface | UART, SPI, I2C, QSPI, JTAG, SWD and analyzer components |
| Host-side CLI/plugins | https://github.com/GlasgowEmbedded/glasgow/blob/main/software/pyproject.toml | Python entry-point applet registration, dependencies and runtime contracts |
| Simulation and gateware tests | https://github.com/GlasgowEmbedded/glasgow/tree/main/software/tests/gateware | Unit-level test patterns for stream, UART, SWD, SPI, I2C, QSPI, CRC and analyzer logic |
| Hardware design | https://github.com/GlasgowEmbedded/glasgow/tree/main/hardware/boards/glasgow | Open board design, hardware revisions and manufacturing files |
| FX2/STM32 firmware | https://github.com/GlasgowEmbedded/glasgow/tree/main/firmware | Firmware side of USB/hardware interface |

## Evidence, builds, and maintenance

1. [Repository root](https://github.com/GlasgowEmbedded/glasgow) contains `software`, `firmware`, `hardware`, `docs`, `examples`, and `vendor`. README points to the [manual](https://glasgow-embedded.org/).
2. [Software manifest](https://github.com/GlasgowEmbedded/glasgow/blob/main/software/pyproject.toml) requires **Python >=3.13**, Amaranth >=0.5.9 <0.6, libusb1 where applicable, and PDM; optional built-in toolchain uses YoWASP/Yosys/nextpnr. It declares alpha maturity and dual 0BSD/Apache-2.0 licensing.
3. [Main CI workflow](https://github.com/GlasgowEmbedded/glasgow/blob/main/.github/workflows/main.yml) defines Python 3.13, 3.14, PyPy 3.11 and experimental 3.15 test configurations; runs `glasgow --help`, builds revision C3 UART gateware, and executes software tests. It also builds firmware, docs and wheel artifacts. These are configured checks, **not observed passing results**.
4. **CI caveat:** `required` aggregates `test-software`, `build-firmware`, and `build-manual`, but `lint-software` is commented out of its `needs` list. Thus the required aggregate does not itself enforce lint success. Inspect branch protection separately before making stronger claims.
5. [Current commit history](https://github.com/GlasgowEmbedded/glasgow/commits/main/) shows 2026-10-05 work on 25q 8K erase blocks and `SFDPCollection.parse_bytes`, plus dependency and protocol maintenance. Repository metadata shows pushed 2026-10-05.
6. [GitHub Releases](https://github.com/GlasgowEmbedded/glasgow/releases) returned **no releases** in the inspected API query. The absence of GitHub Releases does not prove there are no distributed builds or published wheels elsewhere.
7. [Root 0BSD license](https://github.com/GlasgowEmbedded/glasgow/blob/main/LICENSE-0BSD.txt) and [Apache-2.0 license](https://github.com/GlasgowEmbedded/glasgow/blob/main/LICENSE-Apache-2.0.txt) are present. `.gitmodules` points to a Codeberg-hosted `libfx2` dependency and a GitHub-hosted docs archive; licenses for those sources require independent review.

## Boundaries and risks

- Hardware interface voltages, pin direction, current limits and timing are board-specific; do not connect to unknown devices without appropriate electrical protections.
- Many applets expose experimental/rare protocols; source existence does not establish compatibility with every target or robust recovery after disconnects.
- The SFDP parser explicitly implements base JESD216 and JESD216A, **not** every newer SFDP revision.
- The repository has no GitHub Releases in the inspected query; alpha status and hardware requirements justify a Working Evidence deduction.
- No source was copied into GitHub Gold. External submodules and hardware designs need per-component licensing checks.

## Verification boundary

**Performed:** inspected repository metadata, root and software manifests, software/firmware/hardware directory trees, exact protocol and gateware modules, source of SFDP parser, CI workflow, license texts, submodule declarations, and recent commit metadata.

**Not performed:** Python installation, gateware synthesis, unit tests, hardware flashing, physical signal capture, checking actual CI job results, independent protocol conformance, or security testing. **PROMISING** reflects these limits.

## Next research

1. Run `pdm run glasgow build --rev C3 uart` and the software test suite at a pinned commit; record toolchain and results.
2. Extract an inventory of all applets with hardware prerequisites, test coverage, maturity and exact licensing.
3. Differential-test `protocol/sfdp.py` on public JEDEC fixtures and corrupted/truncated tables; compare against flashrom and other primary implementations.
4. Inspect CI status and whether lint is a branch-protection requirement, then reconcile documentation.
5. Compare reusable FPGA/gateware interfaces with sigrok/PulseView, GreatFET and probe-rs without conflating distinct hardware roles.

## GitHub Gold catalog hygiene

Before integration, GitHub Gold's branch inventory and catalog checks found no Glasgow dossier or canonical entry. This research dossier was committed to the existing draft research branch on 2026-10-10. It is **not** yet a canonical catalog promotion. Update `MASTER_LIST.md` and `catalog/tools.json` together when promoting, and run `scripts/catalog_audit.py`.

## Component update — 2026-10-09

- Upstream commit [6e6d346](https://github.com/GlasgowEmbedded/glasgow/commit/6e6d34615f751606291dea053a195680f0a8db78) introduced `SFDPCollection.parse_bytes` in `software/glasgow/protocol/sfdp.py`. This provides a path for parsing previously captured JEDEC SFDP byte sequences without attached flash hardware. Standalone reuse still requires inspecting imports and compatibility.
- Latest upstream commits checked on 2026-10-10 were dated 2026-10-05; no newer commits were found in the inspected commit list.
- This update is source review only: no parser test, FPGA synthesis, firmware build, hardware connection, or passing CI run was independently performed.
