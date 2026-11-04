# MeshSat Field Kit — auditable off-grid communications hardware

- **Repository:** https://github.com/meshsat/meshsat-fieldkit
- **Author / Org:** MeshSat
- **Category:** open hardware / emergency communications / Raspberry Pi / radio gateway / field systems
- **Evidence:** VERIFIED
- **Gold score:** 27 / 30
- **Tier:** S
- **Discovery:** recursive follow-up from the MeshSat gateway dossier, 2026-09-27
- **License:** CERN-OHL-S-2.0 (vendor material excluded)

## Summary

MeshSat Field Kit is the hardware counterpart to the MeshSat multi-bearer gateway. It is valuable less as a single finished product than as an unusually well-recorded progression from two physically built V1 go-boxes to a much more ambitious V2 carrier-board architecture whose unverified state is documented explicitly.

V1 consists of two Raspberry Pi 5 field kits, `tesseract` and `parallax`, built in April 2026. They combine UPS/battery power, Iridium satellite modem, Meshtastic LoRa, cellular, APRS, RTL-SDR, ZigBee, GPS, DCF77 and operator display hardware in an IP67 case. Upstream provides a concrete BOM, wiring/pinout corrections, plate geometry, case-hole schedule, harness details, provisioning steps and commissioning checks.

V2 is architecturally interesting but must not be mistaken for proven hardware. It proposes seven KiCad boards around three Compute Module 5 slots, switched USB peripheral banks, multiple radio paths, a custom 4S battery, sensor/panel controllers, RF blind mates and redundant compute/power concepts. Upstream states clearly that the V2 foundations remain incomplete, zero boards are ready for layout, corrected schematics have not propagated into layouts, and no V2 board has been fabricated, ordered or physically verified.

## Score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Concrete reference for integrating heterogeneous off-grid radios, compute, power and operator I/O into portable field hardware. |
| Working evidence | 4 | Two V1 units are documented as physically built and used on bench/demos; V2 is explicitly unbuilt. |
| Reusability | 5 | BOMs, harnesses, CAD, KiCad sources, generators, interface records and build procedures expose many reusable patterns. |
| Novelty | 5 | The V2 concept combines triple CM5 compute, switchable peripheral ownership, multi-bearer RF and field-service packaging in an unusual architecture. |
| Documentation | 5 | Extensive build records, evidence/status documents, engineering handover material, fabrication sources and explicit supersession notes. |
| Maintenance | 3 | Extremely active September 2026 engineering/documentation work, but V2 remains pre-layout/pre-fabrication and the repository itself warns against ordering current board outputs. |

**Total: 27 / 30 — S**

## Concrete useful surfaces

### V1 build record

`v1/BUILD.md` is unusually practical source material. It records the as-built April 2026 kit, including a 33-line parts list, case preparation, HDPE plate stack, antenna bulkheads, radio/modem wiring, power path, provisioning and verification. It also preserves later corrections rather than silently rewriting history—for example the original UV-K5/AIOC APRS chain was superseded by PicoAPRS V4 hardware in September 2026.

Reusable ideas include:

- portable multi-radio Pi 5 integration
- external antenna/bulkhead planning
- UPS and DC field-power integration
- deterministic USB/device identification
- radio-specific harness and GPIO documentation
- mechanical plate-stack CAD and cut-file generation
- explicit post-change link verification rather than assuming a reconnected RF chain still performs correctly

### V2 modular carrier architecture

The V2 tree describes seven boards: power/I/O, triple-CM5 compute, panel backer, VHF/APRS, dock strip, dock block and pack BMS. Notable architectural ideas include:

- three Compute Module 5 slots
- per-slot PCIe switch/NVMe/card paths
- USB hub banks intended to transfer peripheral ownership after compute failure
- hardware supervisors voting two-of-three
- separately gated radio/amplifier rails
- removable electronics stack docking into case-floor power/sensor/RF interfaces
- panel and sensor RP2040 controllers
- custom 4S battery/BMS design
- explicit interface contracts and engineering evidence records

These are research leads, not validated implementation recommendations.

### Reproducibility and handover discipline

Recent upstream commits show unusually rigorous configuration/evidence bookkeeping for an experimental hardware repository: definition baselines, requirements records, interface readings, generated constraint sheets, snapshot/handover tooling and checks that distinguish stale evidence from current evidence. The project repeatedly labels AI checks as non-qualified engineering review and preserves the statement that the prototype remains unbuilt.

That evidence discipline is itself reusable as a project-management pattern for hardware repositories.

## Runtime / tooling / hardware

V1 centers on Raspberry Pi 5 and off-the-shelf radio/modem modules. The repository uses FreeCAD/CAD assets and build scripts for the mechanical stack.

V2 uses KiCad 9 plus generator/validation scripts and includes manufacturing/handover material. Upstream states that KiCad, Freerouting and generator scripts are used headlessly on a build host. Third-party vendor reference files are kept separately under `v2/vendor/`.

## Upstream verification evidence

Confirmed from repository-native documentation:

- two V1 kits were physically built in April 2026
- V1 build instructions were audited against the actual kits and subsequently corrected as hardware changed
- V1 is described as operating on bench/demos, not as disaster-field proven
- recent September 2026 records include live APRS-chain troubleshooting and as-built device identification
- V2 has detailed schematics/CAD/docs and active validation tooling
- upstream explicitly says V2 has zero boards ready for layout and zero physically verified boards

The latest inspected commit activity on 2026-09-27 continues definition/handover/evidence work and repeatedly states that no V2 board has been fabricated, ordered, assembled, powered or measured.

## Important caveats

- **V1 is prototype hardware.** Upstream says it has not been through a real deployment.
- **V2 is not build-ready.** Do not treat current renders, release folders or older layouts as fabrication-ready output.
- Several V2 circuit corrections exist in schematics but not in board layouts.
- Some V1 documentation intentionally retains superseded historical configuration alongside explicit replacement notes; readers must follow the current-state warnings.
- RF, electrical safety, battery, thermal, EMC and environmental claims require qualified review and physical validation before operational use.

## License and reuse

The repository states that its hardware design, documentation and generator scripts are released under **CERN Open Hardware Licence v2 — Strongly Reciprocal (CERN-OHL-S-2.0)**. Third-party files under `v2/vendor/` remain under vendor-specific terms and are not covered by the repository license.

No upstream design or implementation source was copied into GitHub Gold. Any future adaptation should preserve notices and comply with the strong-reciprocal source obligations. Vendor assets require separate license review.

## Verification performed by GitHub Gold

Performed in this pass:

- inspected repository README and its explicit V1/V2 evidence boundaries
- inspected the V1 build record
- inspected the root CERN-OHL-S-2.0 license
- inspected recent commit history through 2026-09-27
- checked GitHub Gold for an existing `meshsat-fieldkit` dossier; none was found
- compared claims against the companion MeshSat gateway dossier

Not performed:

- no physical build or teardown
- no KiCad/ERC/DRC execution
- no generator/test execution
- no fabrication-file validation
- no electrical, thermal, RF, EMC or environmental measurement
- no battery-pack safety review
- no field/disaster deployment
- no qualified engineering review

Physical V1 and engineering-process statements above are therefore upstream evidence unless explicitly described as repository inspection.

## Related ecosystem

- https://github.com/meshsat/meshsat — gateway software
- https://github.com/meshsat/meshsat-android — mobile companion/gateway lead
- Meshtastic, Reticulum/LXMF and APRS ecosystems
- Raspberry Pi 5 / Compute Module 5

## Follow-up research

1. Inspect `meshsat-android` as a separate portable gateway/client candidate.
2. Isolate the fieldkit's handover/evidence-validation tooling if it is sufficiently generic and licensed for reuse.
3. Revisit V2 only after upstream reaches a fabricated-board milestone; update the evidence score rather than assuming design maturity from documentation volume.
4. Inspect the V1 provisioning and hardware-check scripts for reusable defensive diagnostics.
5. Track whether the current V2 schematics propagate into routed layouts and whether physical bring-up produces measurements matching the design records.

## Verdict

**VERIFIED — S / 27.** MeshSat Field Kit earns catalog inclusion because V1 has concrete as-built evidence and unusually detailed reproducibility records, while V2 offers a technically interesting but explicitly unverified architecture. The project's strongest quality is that it makes this distinction visible instead of presenting generated hardware as proven hardware.