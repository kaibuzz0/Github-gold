# HEARD — offline hiking safety mesh with firmware-in-the-loop digital twin

- **Repository:** https://github.com/luciobaiocchi/heard
- **Author:** Lucio Baiocchi
- **Category:** Off-grid communications / ESP32 / LoRa / GPS / embedded safety / simulation / open hardware
- **Evidence level:** VERIFIED (prototype scope only)
- **Provisional Gold score:** **26/30 — S tier**
  - Utility: 4/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 2/5
- **Primary languages:** C++ firmware, Python simulator, JavaScript web replay
- **License:** Apache-2.0
- **Discovery source:** GitHub-first breadth rotation; independent discovery
- **Inspection date:** 2026-09-28

## Executive finding

HEARD is a research prototype for infrastructure-free group hiking safety. ESP32/GPS/LoRa devices track a planned GPX route locally, classify members as in/out of a route corridor, and exchange group position state over a small multi-hop protocol. Its strongest GitHub Gold feature is not merely the radio concept: the repository compiles the real embedded `ConnectionManager` protocol code into a host-side Python module through pybind11, drives that firmware logic in a digital-twin simulator over GPX tracks, and replays runs in a MapLibre 3D viewer.

The project is unusually explicit about prototype boundaries. The Core is the demonstrated device; the standalone Node firmware remains incomplete, and the README states that the thesis goal was a first working demo, protocol, off-route detection, and firmware-in-the-loop simulator rather than a finished safety product.

## Why it matters

The firmware-in-the-loop pattern is broadly reusable for embedded and radio projects. Instead of maintaining a separate simulator implementation that can drift from device firmware, HEARD wraps the same protocol class used by the target firmware and supplies Arduino/FreeRTOS/LoRa mocks around it. That makes protocol regression tests and visual simulation materially more trustworthy than a disconnected model.

Useful application/research directions include:

- offline group tracking and search-and-rescue research;
- LoRa multi-hop protocol experimentation;
- route-corridor/geofencing algorithms;
- embedded protocol regression testing without physical radios;
- RF/terrain-aware digital twins;
- 3D protocol replay and debugging;
- open-hardware GNSS/LoRa experimentation.

## High-value components

### Shared ConnectionManager protocol

The documented wire model has three message classes: `REQ`, `WAIT`, and `POS`. The Core initiates polling, intermediate nodes can keep the Core timeout alive while relaying, and position responses can be aggregated and forwarded. Hop-list fingerprints suppress duplicate relays.

The value is the compact protocol architecture and its shared implementation between target firmware and simulation, not a claim that it is a production-grade mesh-routing protocol.

### Firmware-in-the-loop simulator

`code/simulator` builds real C++ protocol firmware into a Python extension with pybind11. Host mocks stand in for Arduino, FreeRTOS, and LoRa surfaces. Recorded runs can use real GPX tracks and a probabilistic radio model; optional terrain line-of-sight modeling is documented using DEM data and ITU-R P.526 knife-edge diffraction.

This is the strongest reusable engineering pattern in the repository.

### 3D replay viewer

The simulator emits runs that can be replayed in a MapLibre GL JS browser viewer showing planned route/corridor, devices, radio transmissions, protocol state, delivery metrics, and connectivity. The viewer deliberately has no application build step; CI syntax-checks its ES modules.

### Route/off-path detection

Each device is intended to hold the planned GPX route locally and classify its current position as `IN_PATH` or `OUT_PATH` against a configurable corridor. This keeps the basic safety signal independent of phone/cloud connectivity.

### Hardware assets

The repository contains PCB V1 manufacturing/design material, including Gerber/ODB++ outputs, schematics, BOM material, and RF/EM simulation files. The README describes a newer STM32WLE5 + u-blox MAX-M10M direction after the original ESP32 prototype.

Treat the newer PCB as alpha/open-hardware work requiring independent electrical/RF/manufacturing validation, not as equivalent evidence to the earlier demonstrated Core prototype.

## Working evidence

The repository has a real CI workflow with three independent gates:

1. **Simulator:** installs Python dependencies, builds `heard_sim` from firmware C++ through CMake/pybind11, then runs `pytest -v`.
2. **Firmware:** installs PlatformIO and builds both `code/core` and `code/node` target projects.
3. **Web:** syntax-checks the MapLibre replay viewer ES modules under Node 22.

The most recent default-branch CI run inspected for commit `26131b3f9f287cdc6eb39a92b75a5e18f8c9a8b5` completed successfully on **2026-08-08**. This is direct GitHub Actions evidence that the configured simulator tests, firmware compilation, and web syntax gate passed for that commit. GitHub Gold did not rerun those jobs.

The README also documents a physical Core prototype and upstream field measurements, including approximately 3 km open LoRa range and 300–400 m obstructed range. Those are upstream measurements only; they were not reproduced in this research run.

## Maintenance signal

The repository was created in June 2026 and the latest push observed was August 8, 2026. It therefore receives a conservative maintenance score despite meaningful recent development, because it has a short operating history and had not received a code push for roughly seven weeks at inspection time.

## License

GitHub repository metadata and the README identify **Apache License 2.0**. No upstream source, hardware design files, binaries, maps, or datasets were copied into GitHub Gold.

Third-party libraries, map/DEM data, component vendor material, and toolchain assets should still be checked under their own terms before redistribution.

## Caveats and limitations

- This is explicitly a research prototype, not a certified emergency or life-safety device.
- Standalone Node firmware is not yet implemented as the intended complete GPS/path-checking device; the repository currently describes a minimal receiver sketch plus shared protocol logic.
- A simulator passing protocol tests does not validate real-world RF propagation, battery life, GNSS behavior, weather resistance, human factors, or emergency reliability.
- The README reports physical measurements, but GitHub Gold did not reproduce them.
- PCB V1 is alpha hardware and upstream explicitly requests VNA/RF and physical prototype validation.
- The repository notes that simultaneous cross-talk/isolation simulations between active LoRa and GPS front ends have not yet been run.
- The project is exploring migration from the original ESP architecture toward STM32WL, so hardware/firmware architecture is still moving.

## Verification performed by GitHub Gold

This run inspected:

- current GitHub repository metadata;
- root README and explicit prototype-status statements;
- root license metadata;
- `.github/workflows/ci.yml`;
- recent GitHub Actions workflow-run metadata;
- existing `Github-gold` code search to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- compile the firmware;
- run pytest or the simulator;
- flash ESP32/STM32 hardware;
- transmit LoRa packets;
- reproduce range/GPS/path-deviation measurements;
- validate terrain propagation modeling;
- manufacture or electrically inspect PCB V1;
- run VNA/EMC/cross-talk measurements;
- test battery/runtime behavior;
- conduct an emergency field trial or safety certification review.

## Gold rationale

**Utility — 4/5:** useful for off-grid group-safety research and embedded/radio simulation, but not production safety equipment.

**Working Evidence — 5/5:** physical prototype evidence plus a CI pipeline that builds firmware, compiles real protocol code into the simulator, runs pytest, and syntax-checks the viewer; a successful default-branch run was inspected.

**Reusability — 5/5:** Apache-2.0, shared firmware/simulator architecture, PlatformIO/CMake/pybind11 components, GPX tooling, protocol simulation, and visual replay.

**Novelty — 5/5:** the combination of compact offline group tracking with the same embedded protocol code executing inside a terrain-aware digital twin is technically distinctive.

**Documentation — 5/5:** substantial README, project, roadmap, simulator, simulation, architecture, hardware and manufacturing documentation.

**Maintenance — 2/5:** active 2026 development but a young project with short history and no observed push after 2026-08-08 at inspection time.

**Provisional total: 26/30 — S tier.**

## Strong next leads

1. Inspect the simulator regression tests to map exactly which 1/2/3-hop and failure cases are proven.
2. Trace `ConnectionManager` timeout, duplicate suppression, aggregation and malformed-packet behavior.
3. Inspect the route-corridor algorithm and GPS-error assumptions.
4. Review the RF channel/terrain model against its cited propagation assumptions.
5. Inspect the STM32WL PCB files and firmware migration status separately from the original Core evidence.
6. Look for memory/power ceilings and long-duration protocol behavior.
