# Zigbee2MQTT and SDR++ discovery — 2026-10-25

## Method and provenance
Reviewed current draft PR #7 head, 86-entry canonical catalog, master list, schema/audit workflow and YouTube seed list before editing. Exact-ID web searches for two YouTube playlists produced no indexed metadata/transcripts; neither candidate is attributed to YouTube. No third-party code or assets copied. All execution evidence below is **upstream GitHub Actions**, not independent testing.

## Zigbee2MQTT — VERIFIED (upstream), S/28
- Repository: https://github.com/Koenkk/zigbee2mqtt
- Score: utility 5, working evidence 5, reusability 5, novelty 4, documentation 5, maintenance 4.
- Evidence inspected: README, root GPL-3.0 LICENSE, package.json (version 2.14.2, Node `^22.2.0 || ^24 || <=26.2`, pnpm 11.26.0), `.github/workflows/ci.yml`, `lib/`, `lib/extension/`, `test/`, `lib/extension/otaUpdate.ts`.
- Stable release 2.14.2 published 2026-10-01. 2026-10-25 upstream dev [CI run 40171469797](https://github.com/Koenkk/zigbee2mqtt/actions/runs/40171469797) **10/10 jobs successful**: check, build, Vitest coverage and Linux/Windows/macOS Node 22/24/26 matrix.
- Reusable modules: `lib/zigbee.ts`, `lib/mqtt.ts`, `lib/controller.ts`, `lib/extension/otaUpdate.ts`, `networkMap.ts`, `availability.ts`, `homeassistant.ts`, plus test suites.
- Ecosystem: `Koenkk/zigbee-herdsman` (MIT), `Koenkk/zigbee-herdsman-converters` (MIT), `zigbee2mqtt/hassio-zigbee2mqtt`.
- Requirements: Node/pnpm, MQTT broker and supported Zigbee coordinator; vendor-specific devices/firmware vary. Security: secure MQTT broker, web UI, coordinator pairing and network key. OTA validation needs hardware test. No coordinator, RF or broker execution performed.

## SDR++ — VERIFIED (upstream builds), S/26
- Repository: https://github.com/AlexandreRouma/SDRPlusPlus
- Score: utility 5, working evidence 4, reusability 5, novelty 4, documentation 4, maintenance 4.
- Evidence inspected: README, GPL-3.0 root license, CMakeLists.txt, `.github/workflows/build_all.yml`, `core/src/dsp/`, `core/src/signal_path/`, source/decoder module trees and Android project.
- 2026-10-23 upstream [Build Binaries run 39896187183](https://github.com/AlexandreRouma/SDRPlusPlus/actions/runs/39896187183) **22/22 jobs passed**, including Windows, macOS x86/ARM, Linux variants, Android APK build, spelling and formatting; no radio hardware or decoder correctness tests shown. Stable numbered GitHub release 1.0.4 dates to 2021-10-17; rolling nightly release object is older, despite active 2026 CI.
- Reusable components: DSP filters/streams/demodulators, IQ/VFO signal path, modular hardware inputs (Soapy, RTL-SDR, rtl_tcp), M17 decoder (optional codec2), Meteor demodulator, recorder and scanner.
- Requires C++17/CMake and platform DSP/audio libraries; vendor SDKs and SDR drivers vary. GPL-3.0 root; audit bundled `core/libcorrect` and vendor libraries separately before copying. No independent build, SDR reception, M17 interoperability or Android install.

## Existing catalog maintenance
- Updated SoapySDR related-project reference to the canonical SDR++ upstream repository.
- Cross-linked OpenRTX to SDR++'s optional M17 decoder; **not** evidence of interoperability.
- Rechecked NASA Open MCT: latest inspected 2026-10-25 e2e-full 40147454572 and e2e-perf 40145966359 still failed. No evidence sufficient to promote its existing PROMISING status.

## Next investigations
1. Zigbee2MQTT: pairing/network-key threat model, MQTT/frontend authentication, firmware OTA trust and converter compatibility.
2. SDR++: Soapy source-module interoperability, M17 decoder validation against OpenRTX, Android runtime behavior, libcorrect/vendor licensing.
3. Open MCT: diagnose npm CI installation failures, then rerun browser telemetry e2e.
