# FreeCAD and OpenCPN — GitHub-first research (2026-10-26)

## Method and verification boundary
Inspected repository-native READMEs, licenses, security notes, source directories, tests, stable releases and CI job steps. **VERIFIED means explicit upstream build/test evidence**, not an independent installation, hardware test, chart rendering or mechanical precision validation. No third-party implementation code or assets copied. Two YouTube seed playlist pages (`PLMI6SBmd587c`, `PLfidXW0BixTc`) were directly requested on 2026-10-26 and throttled; no video or transcript claims. Remaining four seed playlists were not checked in this batch.

## FreeCAD — VERIFIED / S 28
- **Repository:** https://github.com/FreeCAD/FreeCAD
- **Scores:** utility 5, working evidence 5, reusability 5, novelty 4, documentation 5, maintenance 4.
- **Purpose:** History-based parametric 3D CAD, sketch constraints, technical drawings, automation and workbenches.
- **Exact reusable paths:** [Sketcher constraint engine](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/Sketcher/App/Constraint.cpp); [SketchObject](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/Sketcher/App/SketchObject.cpp); [Part B-rep wrappers](https://github.com/FreeCAD/FreeCAD/tree/main/src/Mod/Part/App); [OpenSCAD import](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/OpenSCAD/importCSG.py); [OpenSCAD export](https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/OpenSCAD/exportCSG.py); [TechDraw](https://github.com/FreeCAD/FreeCAD/tree/main/src/Mod/TechDraw); [tests](https://github.com/FreeCAD/FreeCAD/tree/main/tests/src).
- **Build/install:** Official Windows/macOS/Linux releases, or CMake >=3.22 source build with OpenCASCADE, Qt, Python and Coin3D. Python API available for macros and workbenches.
- **Release:** [1.1.4](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4), published 2026-09-28.
- **Working evidence:** 2026-10-26 [main FreeCAD CI primary 40346216527](https://github.com/FreeCAD/FreeCAD/actions/runs/40346216527) succeeded. Its Ubuntu build job steps explicitly include CMake configure/build, FreeCAD CLI/GUI tests, Coin snapshot visual tests, C++ tests and post-install tests. [CodeQL 40346215716](https://github.com/FreeCAD/FreeCAD/actions/runs/40346215716) succeeded. CI does not prove mechanical accuracy or plugin safety.
- **License:** Root [LICENSE](https://github.com/FreeCAD/FreeCAD/blob/main/LICENSE) contains LGPL 2.1; inspected [src/App/CMakeLists.txt](https://github.com/FreeCAD/FreeCAD/blob/main/src/App/CMakeLists.txt) SPDX is LGPL-2.1-or-later. Inspect each module, OCCT, Qt, Coin3D, assets and notices before adapting.
- **Risk/limits:** Untrusted macros and add-ons, malicious model files, geometric robustness, STEP/STL export accuracy and manufacturing tolerances.
- **Ecosystem:** [OpenSCAD](https://github.com/openscad/openscad) cross-reference updated, OpenCASCADE geometry engine, FreeCAD-Bundle.
- **Next:** Evaluate OpenSCAD roundtrip fidelity and regression corpus; test sketch solver and STEP/STL exports; review macro security boundary.

## OpenCPN — VERIFIED / S 27
- **Repository:** https://github.com/OpenCPN/OpenCPN
- **Scores:** utility 5, working evidence 4, reusability 5, novelty 4, documentation 5, maintenance 4.
- **Purpose:** Cross-platform marine chartplotter and vessel navigation using offline raster/vector charts and live telemetry.
- **Exact reusable paths:** [AIS decoder](https://github.com/OpenCPN/OpenCPN/blob/master/model/src/ais_decoder.cpp); [AIS state](https://github.com/OpenCPN/OpenCPN/blob/master/model/src/ais_target_data.cpp); [NMEA 0183 serial](https://github.com/OpenCPN/OpenCPN/blob/master/model/src/comm_drv_n0183_serial.cpp); [NMEA 2000 SocketCAN](https://github.com/OpenCPN/OpenCPN/blob/master/model/src/comm_drv_n2k_socketcan.cpp); [Signal K network](https://github.com/OpenCPN/OpenCPN/blob/master/model/src/comm_drv_signalk_net.cpp); [S57 charts](https://github.com/OpenCPN/OpenCPN/tree/master/libs/s57-charts); [GRIB plugin](https://github.com/OpenCPN/OpenCPN/tree/master/plugins/grib_pi); [protocol tests](https://github.com/OpenCPN/OpenCPN/tree/master/test).
- **Build/install:** Windows/macOS/Linux desktop releases, CMake/wxWidgets build, Android upstream-supported. Chart availability and interface support vary by system.
- **Release:** [5.14.2](https://github.com/OpenCPN/OpenCPN/releases/tag/Release_5.14.2), published 2026-09-28.
- **Working evidence:** 2026-10-15 [Linux build 38800150299](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150299) passed 3/3 jobs including AddressSanitizer and explicit Test steps; [macOS 38800150392](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150392) 2/2; [Windows 38800150288](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150288) 1/1. No chart rendering, GPS/AIS hardware or sea trial by GitHub Gold.
- **License:** [LICENSING](https://github.com/OpenCPN/OpenCPN/blob/master/LICENSING) says project-developed files GPLv2+; bundle includes GPLv3/LGPL/BSD/MIT/etc. Consult [data/copyright](https://github.com/OpenCPN/OpenCPN/blob/master/data/copyright) before copying any component.
- **Security:** [SECURITY.md](https://github.com/OpenCPN/OpenCPN/blob/master/SECURITY.md) warns plugins run with full user privileges; charts, plugins and sensor data may be untrusted. Navigation is safety-critical; verify chart currency and sensor integrity.
- **Ecosystem:** Signal K server, in-tree GRIB/dashboard plugins, AIS/NMEA transport libraries. No interoperability claims beyond inspected source paths.
- **Next:** Fuzz AIS and S-57 input paths, inspect network listener authentication, test plugin isolation and sensor failover.

## Existing-entry maintenance
OpenSCAD related projects now link FreeCAD's in-tree OpenSCAD workbench (importCSG.py/exportCSG.py). This is a source-level ecosystem relationship, **not an independently executed interoperability test**. OpenSCAD's S/26 score and VERIFIED evidence are unchanged.

## Deferred / not claimed
The two YouTube playlist pages were throttled; remaining four not attempted. No video-derived discoveries. No independent binary execution, model fabrication, marine hardware tests, vulnerability scans or fuzzing were performed.
