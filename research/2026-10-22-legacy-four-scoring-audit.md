# Legacy scoring audit — 2026-10-22

Four previously canonical projects were reviewed against primary upstream source, releases, CI and licensing. These are **not new promotions**. Scores are factor assessments, not claims of independent execution. No third-party code copied. All six YouTube playlist pages were retried, but retrieval was throttled or disabled; no transcript evidence used.

## OUI-SPY Unified Blue — PROMISING, A/24

Repository: https://github.com/colonelpanichacks/oui-spy-unified-blue

Utility 5 + Working Evidence 2 + Reusability 4 + Novelty 5 + Documentation 5 + Maintenance 3 = **24**.

**Inspected:** [README](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/README.md), [PlatformIO configuration](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/platformio.ini), [mode manager](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/src/mode_manager.cpp), [BLE detector](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/src/mode_detector.cpp), [Wi-Fi observation](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/src/mode_flockyou_promiscious.cpp), [BLE capture](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/src/mode_blesniff.cpp), [PCAP](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/src/mode_pcap.cpp). Arduino/PlatformIO target is XIAO ESP32-S3; dependencies include NimBLE-Arduino, Async WebServer, NeoPixel, ArduinoJson and TinyGPSPlus.

**Maintenance/evidence:** Source commit [6e5e282](https://github.com/colonelpanichacks/oui-spy-unified-blue/commit/6e5e282954) (2026-10-11) rebuilt Mode 7 binary and web flasher. [Actions 38178185526](https://github.com/colonelpanichacks/oui-spy-unified-blue/actions/runs/38178185526) passed **Pages deployment only**, not firmware compilation. Prebuilt firmware exists but was not independently validated. No latest tagged release or root license found.

**Risk:** UNKNOWN licensing prohibits copying; passive signatures and RSSI can produce false positives. No device testing, radio measurements, or firmware build performed. **Follow-up:** licensing clarification, reproduce build, inspect detection logic, compare companion `colonelpanichacks/flock-you`.

## termux-adb — VERIFIED (upstream release/source), A/23

Repository: https://github.com/nohajc/termux-adb

Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 3 + Maintenance 3 = **23**.

**Inspected:** [README](https://github.com/nohajc/termux-adb/blob/master/README.md), [install.sh](https://github.com/nohajc/termux-adb/blob/master/install.sh), root MIT license, and pinned [vendor-adb-patched submodule](https://github.com/nohajc/vendor-adb-patched). Architecture bridges Android `termux-usb` permission-granted descriptors into patched ADB/Fastboot using Unix-domain-socket FD passing. Requires Termux, Termux:API, Android and a USB data connection.

**Maintenance/evidence:** [v0.2.3](https://github.com/nohajc/termux-adb/releases/tag/v0.2.3) (2025-09-09); last inspected commit 2026-03-13. No GitHub Actions runs found. Upstream describes functional behavior, but no independent device test or automated test evidence was found.

**Supply-chain caveat:** README pipes remote script to Bash; installer adds third-party APT source and downloads a key without a pinned fingerprint. Review/authenticate before installation. Root MIT does not supersede Android-tools submodule licenses. **Follow-up:** inspect USB enumeration patches, package signing and test on two owned Android devices.

## ESP32-S3 Remote ID Add-on — PROMISING, A/24

Repository: https://github.com/peinser/esp-remoteid

Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 3 + Documentation 5 + Maintenance 3 = **24**.

**Inspected:** [README](https://github.com/peinser/esp-remoteid/blob/main/README.md), [src/remoteid](https://github.com/peinser/esp-remoteid/tree/main/src/remoteid), [OpenDroneID/Monocypher components](https://github.com/peinser/esp-remoteid/tree/main/components), [tests](https://github.com/peinser/esp-remoteid/tree/main/tests), [firmware workflow](https://github.com/peinser/esp-remoteid/blob/main/.github/workflows/firmware.yml), Apache-2.0 license. ESP-IDF v5.5 build for esp32s3 includes `idf.py set-target`, `build`, `size`. Firmware integrates BLE/Wi-Fi OpenDroneID and MAVLink.

**Maintenance/evidence:** [v1.0.0](https://github.com/peinser/esp-remoteid/releases/tag/v1.0.0) (2026-05-15), main commit 2026-06-29. [Firmware CI 28357049701](https://github.com/peinser/esp-remoteid/actions/runs/28357049701) passed 2026-06-29. The workflow does **not** run `tests/remoteid_test.py` or RF interoperability tests.

**Risk:** Build success does not prove ASTM F3411/EU compliance, receiver interoperability, message timing or regulatory legality. Review submodule licenses. No independent build or radio test. **Follow-up:** add protocol/identity CI, receiver tests and measured on-air behavior.

## App Manager — VERIFIED (upstream), S/27

Repository: https://github.com/MuntashirAkon/AppManager

Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5 = **27**.

**Inspected:** [README](https://github.com/MuntashirAkon/AppManager/blob/master/README.md), [BUILDING.rst](https://github.com/MuntashirAkon/AppManager/blob/master/BUILDING.rst), Java [source tree](https://github.com/MuntashirAkon/AppManager/tree/master/app/src/main/java/io/github/muntashirakon/AppManager), [test workflow](https://github.com/MuntashirAkon/AppManager/blob/master/.github/workflows/tests.yml), REUSE/SPDX license metadata. Reusable components: `apk/`, `backup/`, `scanner/`, `adb/`, `profiles/`, `logcat/`, `crypto/`. Build instructions require JDK/Gradle, Linux/macOS/WSL and substantial resources.

**Maintenance/evidence:** [v4.1.1](https://github.com/MuntashirAkon/AppManager/releases/tag/v4.1.1) (2026-09-04), commits through 2026-10-19. Upstream [Gradle tests 39186829907](https://github.com/MuntashirAkon/AppManager/actions/runs/39186829907), [lint 39186829863](https://github.com/MuntashirAkon/AppManager/actions/runs/39186829863) and [CodeQL 39186829827](https://github.com/MuntashirAkon/AppManager/actions/runs/39186829827) passed 2026-10-19.

**License/risk:** Primary GPL-3.0-or-later with file-level REUSE/SPDX differences. No independent Android build, backup/restore or privileged-device test. **Follow-up:** reproducible APK build, encrypted-backup recovery tests, ADB/root privilege boundary audit.

## Verification and provenance

GitHub Gold inspected upstream files, release metadata, commit history and CI reports, but did not execute third-party code, flash devices, perform Android USB tests or test radio reception. The prior four records retain their evidence levels and total scores; this pass adds transparent six-factor breakdowns and corrects maintenance/evidence caveats. No code copied; no new canonical entries.
