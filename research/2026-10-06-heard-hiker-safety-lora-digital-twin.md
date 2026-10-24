# HEARD — offline hiker group-safety mesh and firmware-in-the-loop simulator

- **Repository:** https://github.com/luciobaiocchi/heard
- **Author:** Lucio Baiocchi
- **Category:** LoRa / offline safety / embedded systems / GPS / mesh networking / simulation / open hardware
- **Evidence:** VERIFIED
- **Provisional Gold score:** **26/30 — S**
  - Utility: 5
  - Working evidence: 4
  - Reusability: 5
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 2
- **License:** Apache-2.0
- **Discovery:** GitHub-first discovery, inspected 2026-10-06.

## Summary

HEARD is an offline group-safety research system originating from a University of Bologna bachelor's thesis. ESP32/GPS/LoRa devices track hikers against a GPX route, classify route deviation, and exchange positions through a custom multi-hop polling/relay protocol. The Core device provides an e-ink group view.

Its most reusable feature is a firmware-in-the-loop digital twin. The real C++ ConnectionManager protocol code is compiled into Python with pybind11, driven along GPX tracks, passed through a deterministic radio/terrain model, and replayed in a MapLibre 3D viewer.

## Valuable components

- `code/core/`: PlatformIO ESP32/FreeRTOS firmware.
- `ConnectionManager`: group polling, relay and position aggregation logic.
- GPX route/path subsystem and IN_PATH / OUT_PATH classification.
- `code/path_loader/`: route preparation/upload tooling.
- `code/simulator/`: firmware-in-the-loop simulation.
- pybind11 shims for running embedded protocol code under a Python-controlled simulation.
- seeded distance-based radio model.
- optional DEM-backed terrain factor using ITU-R P.526 knife-edge diffraction.
- deterministic simulated `millis()` for firmware timeout behavior.
- MapLibre replay viewer for protocol/radio visualization.
- PCB V1 design artifacts and BOM.
- printable Core enclosure release.

## Evidence inspected

GitHub Gold inspected the README, project description, roadmap, simulator architecture/docs, CI workflow, license, releases, recent commits and open issues.

CI currently builds the firmware simulator and runs pytest, builds both Core and Node PlatformIO projects for ESP32, and syntax-checks the web viewer. Simulator documentation states that randomness is seeded and the real firmware ConnectionManager executes inside the simulation.

The latest default-branch commit observed was 2026-08-08, so maintenance is scored conservatively despite substantial earlier 2026 activity.

## Caveats

HEARD remains a research prototype, not certified safety equipment.

Upstream explicitly records important unfinished work: standalone Node firmware is incomplete; multi-hop chains need more real-world field testing; the documented SOS button is not implemented in firmware; battery/power budgeting is unfinished; duty-cycle enforcement is not implemented; the simulator radio model is not fitted to measured field data; and packet airtime/collisions are not yet modeled.

Upstream reports approximately 3 km open and 300–400 m obstructed LoRa measurements. GitHub Gold did not reproduce those figures.

GitHub Gold did not compile or flash the firmware, execute its tests, reproduce field measurements, manufacture the PCB, or independently validate safety behavior. VERIFIED means concrete repository-native implementation/build/test evidence, not independent field certification.

## License

The repository root is Apache-2.0. No upstream implementation code was copied into GitHub Gold.

## Follow-up

1. Execute the simulator tests independently.
2. Inspect exact multi-hop regression invariants and failure coverage.
3. Reproduce a three-device outdoor relay chain.
4. Add airtime/collision and battery models and compare predictions with measured traces.
5. Test reset/power-loss recovery during polling rounds.
6. Complete and test a standalone Node image.
7. Compare the same HEARD safety application over its custom protocol, MeshCore and Meshtastic.
8. Validate route-corridor behavior under poor GPS fixes and GPX edge cases.
9. Keep emergency-use claims conservative until controlled field drills exist.
