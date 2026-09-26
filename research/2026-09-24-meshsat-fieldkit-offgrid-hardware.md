# MeshSat Field Kit — reproducible off-grid communications hardware

- **Repository:** https://github.com/meshsat/meshsat-fieldkit
- **Organization:** meshsat
- **Category:** Open hardware / emergency communications / field systems / radio integration
- **Evidence:** VERIFIED (strong upstream design/build evidence; no GitHub Gold physical build)
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 3/5
- **License:** CERN-OHL-S-2.0 for the project's hardware design, documentation and generator scripts; third-party vendor material retains its own terms.
- **Primary tools/platforms:** Raspberry Pi 5 / Compute Module 5, KiCad 9, FreeCAD, Python/generator tooling; radio, satellite, cellular and sensor hardware.

## Why it matters

This is the physical companion to `meshsat/meshsat`: a reproducible field-kit design for carrying heterogeneous communications hardware into an IP67-style portable case. It is valuable independently of the Bridge software because it captures practical mechanical layout, BOMs, wiring, antenna bulkheads, power, pinouts, CAD, PCB design, assembly procedures and verification notes rather than presenting only a concept render.

The repository is unusually explicit about maturity. Two V1 kits (`tesseract` and `parallax`) were physically built in April 2026 and are used for bench/demo work. The much more ambitious V2 design is documented as designed/generated but **not fabricated or ordered**. GitHub Gold preserves that distinction.

## V1 — physically built evidence

Upstream documents two Raspberry Pi 5 kits that differ primarily in satellite modem: RockBLOCK 9603 SBD versus RockBLOCK 9704 IMT. The V1 build record includes a 33-line BOM, IP67-case drilling schedule, antenna/bulkhead assignments, HDPE plate geometry, GPIO harnesses, software provisioning and commissioning checks.

The hardware set spans satellite, Meshtastic LoRa, cellular, APRS, RTL-SDR receive monitoring, ZigBee, GPS, DCF77 time reception, UPS/battery power and a local touch display. The build documentation says the wiring was audited live on both kits on 19 April 2026 and records later hardware corrections rather than silently rewriting history.

A particularly useful maintenance pattern is the APRS change record: the original UV-K5/AIOC chain was replaced in September 2026 by PicoAPRS V4 units, with per-device USB serial identities, operating settings and observed link-quality troubleshooting retained in the build guide. This kind of as-built provenance is more valuable than a static schematic for field-system reuse.

## V2 — ambitious but unbuilt

V2 moves from hand-wired plates toward a multi-board Peli 1450 system with three Compute Module 5 slots, switched USB peripherals, k3s, redundant I/O-supervisor voting, power/solar management, a panel controller, VHF/APRS hardware, sensors, smart battery management and blind-mate RF paths.

The repository itself states that the V2 boards are designed/generated but none has been fabricated or ordered. Therefore GitHub Gold does **not** treat V2 CAD, routing or automated checks as physical proof. V2 is valuable as a design/research corpus and manufacturing pipeline, not yet as demonstrated field hardware.

Recent upstream engineering records reinforce that distinction: September 2026 commits describe board-analysis experiments, unrouted/open-net counts, current-capacity rules and local test-suite results while explicitly declining to adopt boards that fail the project's own gates.

## Valuable reusable components / patterns

- Real as-built V1 BOM, harness, pinout and commissioning records.
- IP67 portable-case mechanical integration patterns for mixed RF/digital hardware.
- Antenna bulkhead and internal RF-cabling layout.
- Raspberry Pi 5 UPS/power integration and practical USB-device budgeting.
- CAD plate generator and FreeCAD/DXF workflow.
- KiCad carrier-board generation and analysis workflow in V2.
- Multi-compute redundancy concept with switchable peripheral banks.
- RP2040 panel/sensor-controller architecture.
- Power, solar, smart-pack and rail-monitoring design work.
- Explicit design-decision and qualification records that separate measured, simulated, routed and physically built states.

## Maintenance signals

The repository was active through 23 September 2026. Recent commits include updates tying HF/modem design decisions back to hardware proven first on V1 and extensive board-A/E analysis. One recorded local suite reports 1,345 passing tests, 0 failed and 60 skipped for that development state. This is upstream evidence only; GitHub Gold did not reproduce it.

Maintenance receives 3/5 rather than a higher score because the repository is active and evidence-rich but the project explicitly remains a prototype, V1 has no real deployment history, and V2 is not fabricated.

## License and reuse caveat

The repository states that its hardware design, documentation and generator scripts use **CERN Open Hardware Licence v2 — Strongly Reciprocal (CERN-OHL-S-2.0)**. That is not a permissive copy-anything license. Modified Covered Source and conveyed Products can trigger source-location, notice and reciprocal Complete Source obligations. Third-party material under `v2/vendor/` is explicitly outside the project license and remains under vendor terms.

No upstream design files, code, CAD or vendor files were copied into GitHub Gold by this pass.

## Verification boundary

GitHub Gold inspected repository metadata, README/build documentation, license and recent commit history. GitHub Gold **did not** buy components, drill or assemble a case, build PCBs, flash devices, reproduce CAD/KiCad generation, run the project's test suite, transmit over any radio/satellite service, measure RF performance, validate environmental sealing, or verify V2 manufacturability.

`VERIFIED` therefore means the repository contains strong primary-source evidence and two explicitly documented built V1 units. It is not a certification of the field kit, V2 hardware or life-safety suitability.

## Risks / limitations

- Prototype project; upstream explicitly says V1 has not been through a real field deployment.
- V2 is unbuilt, so its redundancy, thermal, RF, power and mechanical behavior remain design claims until fabrication/testing.
- RF operation is jurisdiction/frequency/license dependent.
- Satellite/cellular functionality depends on service plans, credentials, coverage and antennas.
- Complex mixed-signal/RF/power integration creates failure modes that repository-level checks cannot eliminate.
- CERN-OHL-S strong reciprocity matters for downstream hardware/design redistribution.
- Vendor reference files have separate licensing terms.

## Discovery provenance

Recursive follow-up from the verified `meshsat/meshsat` dossier. GitHub Gold's own catalog search did not find an existing `meshsat-fieldkit` entry before addition.

## Related / next leads

1. `meshsat/meshsat-android` — determine whether it is independently useful as a mobile off-grid gateway.
2. V2 generator/rules tooling — inspect whether the PCB verification pipeline contains reusable standalone engineering tools rather than project-specific scripts.
3. Reticulum interoperability in the Bridge repository — evaluate protocol conformance separately from field-kit hardware.

## Steward verdict

**Keep. High-value Gold candidate.** The field-kit repository earns provisional S/28 because the V1 material is unusually concrete, reproducible and honest about as-built changes, while the V2 corpus contains technically interesting open-hardware engineering with explicit qualification boundaries. It does not receive a near-perfect score because V2 is unbuilt and the project has no real emergency deployment history.