# OpenThread, ArduPilot and Renode maintenance — 2026-10-25 CDT (2026-10-26 UTC)

## Provenance and catalog hygiene
- Continued existing open draft PR #7 on `agent/research-ladybird-browser-engine`, parent `42b04289e7920fddf701fafd77ac19016f197570`, after checking README, MASTER_LIST, tools.json, candidate_queue.json (empty), recent research, current PR and branch state.
- Started with 92 unique catalog entries. No OpenThread or ArduPilot aliases or repository URLs in catalog/queue. Two entries added; Renode evidence promoted using independently inspected **downstream** execution; Open MCT failure status refreshed. No third-party source or assets copied.
- GitHub-first discovery. Playlist seed IDs remain recorded in `sources/youtube_playlists.md`; no new transcript access was established, so no video provenance claimed.

## OpenThread — VERIFIED (upstream CI), S/29
- Repo: https://github.com/openthread/openthread; release v2026.10.0 published 2026-10-01. Six factors: utility 5, working 5, reuse 5, novelty 4, documentation 5, maintenance 5.
- Inspected README, BSD-3-Clause LICENSE, CMakeLists, `src/core/thread/mesh_forwarder.cpp`, `src/core/thread/key_manager.cpp`, `tests/`, and `.github/workflows/unit.yml`. Related repositories: `openthread/ot-br-posix` and `openthread/ot-ns`, both active and BSD-3-Clause.
- 2026-10-25 upstream main push SHA `13984b46b7e13a713ace30d183be33dcccab40ea`: [Build 40228441197](https://github.com/openthread/openthread/actions/runs/40228441197) 54/54 jobs success, [Unit 40228441160](https://github.com/openthread/openthread/actions/runs/40228441160) 3/3, [POSIX 40228441091](https://github.com/openthread/openthread/actions/runs/40228441091) 10/10, [Simulation 40228441202](https://github.com/openthread/openthread/actions/runs/40228441202) 6/6, [Border Router 40228441070](https://github.com/openthread/openthread/actions/runs/40228441070) 4/4. New untrusted pull-request workflows marked `action_required` were not treated as code-test failures.
- Useful components: 6LoWPAN forwarding, MLE/routing, key management, platform HAL, POSIX/Border Router interfaces, simulation and fuzz tests. Requirements: CMake/GN host toolchain or board-specific embedded toolchain; actual Thread network requires 802.15.4 hardware. License: BSD-3-Clause at root/inspected source; review `third_party/` before reuse.
- Caveats: no independent build, RF/commissioning test, certification or security audit. Next: review key persistence, border-router privileges, multi-vendor Thread commissioning and fuzz coverage.

## ArduPilot — VERIFIED (upstream CI), S/28
- Repo: https://github.com/ArduPilot/ardupilot; vehicle-specific stable 4.7.2 releases published 2026-10-14. Six factors: utility 5, working 5, reuse 5, novelty 3, docs 5, maintenance 5.
- Inspected README, GPL-3.0 COPYING.txt, BUILD.md, `libraries/AP_NavEKF3/AP_NavEKF3.cpp`, `libraries/AC_AttitudeControl/AC_AttitudeControl.cpp`, `libraries/AP_HAL_SITL/`, Copter workflow and `Tools/renode/`. Waf + Python and recursive submodules for builds; SITL or supported ChibiOS flight hardware.
- 2026-10-25 upstream PR workflows: [unit/SITL build 40231792309](https://github.com/ArduPilot/ardupilot/actions/runs/40231792309) 8/8, [Copter 40231792304](https://github.com/ArduPilot/ardupilot/actions/runs/40231792304) 12/12, [Plane 40231792276](https://github.com/ArduPilot/ardupilot/actions/runs/40231792276) 7/7. [Renode integration 40231792336](https://github.com/ArduPilot/ardupilot/actions/runs/40231792336) successful CubeOrangePlus quadplane mission and Renode unit tests (job 121284892561; steps confirmed successful).
- Useful components: EKF3 navigation, attitude control, MAVLink, hardware abstractions, mission planning, simulated sensors and board-level Renode integration. GPL-3.0 core; submodules/file headers may differ. Related: `mavlink/mavlink`, `ArduPilot/pymavlink`, `ArduPilot/MAVProxy`.
- Caveats: CI/SITL is not evidence of safe real flight. No independent builds, flight, hardware flashing or safety/security audit. Follow EKF failure modes, failsafes, GPS loss, mission safety and MAVLink trust.

## Renode — PROMISING/26 -> VERIFIED (downstream patched integration)/27
- Prior `renode/renode` stable v1.17.0, upstream core passing CI unconfirmed. A new concrete **downstream** runtime signal was inspected, not assumed from Renode's own CI.
- ArduPilot `.github/workflows/test_renode.yml` uses `Tools/renode/tests/fetch_renode.sh` to download a custom Renode package from an ArduPilot-hosted manifest, checks SHA-256 and source revision, then executes Python emulator unit tests and a CubeOrangePlus quadplane mission. [Run 40231792336](https://github.com/ArduPilot/ardupilot/actions/runs/40231792336), job 121284892561, succeeded at both test steps on 2026-10-25. `Tools/renode/README.md` and `run.py` describe generated STM32 board models and patched Renode.
- This justifies evidence VERIFIED for the **observed patched downstream use case** and working-evidence 3->4, score 26->27 (tier remains S). It does **not** verify stock upstream Renode v1.17.0, all CPU/peripheral models, unmodified hardware behavior or independent testing. MIT core with separately licensed dependencies. No source copied.

## Open MCT — maintenance refresh, still PROMISING/A25
- [e2e-full 40250211098](https://github.com/nasa/openmct/actions/runs/40250211098) 2026-10-26 UTC failed: Ubuntu failure and Windows cancelled. e2e-perf 40248391927 and pr-platform 40247907640 also failed. Earlier workflow Node 18 vs package Node >=24.14.1 mismatch is a hypothesis; no new root-cause verification. Keep existing score and classification.
- Next: inspect npm ci logs and align CI Node engine, then require passing e2e before promotion.

## Validation and licensing
- No third-party implementation code, binaries or assets copied. All reported builds and tests are **upstream or downstream GitHub Actions evidence**; GitHub Gold did not independently execute builds, firmware, flights, radios or security tests.
- Canonical catalog and master list must contain 94 unique matching entries, 94 six-factor score sums, no duplicate URLs; repository CI audit to confirm after publishing.
