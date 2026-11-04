# Renode and OpenDroneMap research + ZMK maintenance — 2026-10-25

GitHub-first discovery on draft PR #7 research branch (82 preexisting entries). No duplicate names/URLs. Two YouTube seed playlist IDs re-searched without indexed transcripts; no YouTube-derived findings. No third-party code or assets copied.

## Renode — PROMISING, S/26

Repository: https://github.com/renode/renode. Scores: {"utility":5,"working_evidence":3,"reusability":5,"novelty":5,"documentation":5,"maintenance":3}.

Useful components: src/Renode/PlatformDescription/: board descriptions; src/Renode/Network/ and Connectors/: virtual networks; src/Renode/RobotFrameworkEngine/: test keywords; tests/run_tests.py and tests/platforms/*.robot: Robot/NUnit regression harness; src/Plugins/CoSimulationPlugin/ and SystemCPlugin/: co-simulation; src/Renode/WebSockets/ and ws-api/: remote interfaces.

Verification: 2026-10-25: README, MIT LICENSE, source/test/platform trees and test runner inspected; Stable v1.17.0 published 2026-09-07 with binary assets and detailed architecture fixes; 2026-10-23 master commit 04cafbb adjusts CPU pause/halt synchronization; No passing current core emulator CI found; 2026-10-22 GitHub Actions success 39742143711 was dependency graph update only; No independent build, firmware boot, timing/hardware test or security audit.

Runtime: .NET >=6, prebuilt Windows/Linux/macOS packages or source; GTK2 for Linux portable GUI, Robot Framework/Python for tests.

License: MIT core; third-party libraries separately licensed. Caveats: Core test execution not verified; virtual timing differs from hardware; bundled licenses and remote API access require review.

Related: renode/renode-infrastructure, zephyrproject-rtos/zephyr, lowRISC/opentitan.

Next: PROMISING until actual emulator tests confirmed. .NET >=6; GTK2 for Linux portable GUI; Robot Framework/Python tests. Simulated peripheral/timing fidelity varies; secure remote APIs and check dependency licenses.

## OpenDroneMap — VERIFIED, S/27

Repository: https://github.com/OpenDroneMap/ODM. Scores: {"utility":5,"working_evidence":4,"reusability":5,"novelty":4,"documentation":5,"maintenance":4}.

Useful components: stages/run_opensfm.py, odm_meshing.py, odm_dem.py, odm_orthophoto.py: reconstruction stages; opendm/gcp.py and geo.py: ground-control/georeferencing; opendm/dem/: DEM and PDAL; opendm/orthophoto.py, cogeo.py, tiles/: orthophotos/GeoTIFF/tiles; opendm/multispectral.py and thermal.py: sensor data; opendm/remote.py and stages/splitmerge.py: remote processing; tests/test_gcp.py and tests/: regression fixtures.

Verification: 2026-10-25: README, AGPL LICENSE, stages/modules/tests, native/Docker workflows inspected; Stable v3.6.2 released 2026-08-12; master 77439b1 merged OpenSfM v110 on 2026-09-15; Upstream 2026-09-16 Native Builds 35092809957 passed 4/4 Linux/ARM/Windows/macOS jobs with Test, Smoke and Prod smoke steps; Upstream 2026-09-15 Docker CPU 34975847090 passed 5/5 jobs; 2026-09-15 Windows Setup publish 34975845646 failed; later October PR action_required is not test execution; No independent aerial reconstruction, GCP accuracy, GPU benchmark or installer testing.

Runtime: Docker CPU amd64/arm64, optional NVIDIA GPU image, or native pixi/SuperBuild; large datasets resource-intensive.

License: AGPL-3.0 root; native dependencies/assets separately licensed. Caveats: AGPL obligations; reconstruction accuracy depends on image overlap and georeferencing. Windows installer CI failure remains unresolved.

Related: OpenDroneMap/NodeODM, OpenDroneMap/WebODM, mapillary/OpenSfM.

Next: Docker or native pixi/SuperBuild; high CPU/RAM/disk demands. AGPL network copyleft and dependency licenses. Verify GCP residuals, reflectance/NoData, orthophoto repeatability, Windows packaging.

## ZMK follow-up

Oct 24 main Build https://github.com/zmkfirmware/zmk/actions/runs/40062805918 failed a proton_c job. Oct 25 main Build https://github.com/zmkfirmware/zmk/actions/runs/40162399914 passed 38 jobs (3 skipped), including proton_c. No root cause determined. Score and tier unchanged. No hardware flashed.

## Boundaries

No independent builds, installs, firmware execution, drone-image processing, performance tests or security audits. Upstream CI is labeled as upstream evidence; source/test presence alone is not execution proof.