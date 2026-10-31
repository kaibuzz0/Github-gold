# LighthouseReckoning v1.3.0 maintenance review — 2026-10-18

- Upstream: https://github.com/TidalImpact/LighthouseReckoning
- Release: https://github.com/TidalImpact/LighthouseReckoning/releases/tag/v1.3.0 (published 2026-10-16)
- Evidence: VERIFIED from upstream release notes, changelog, source, README, license and compile-workflow configuration. No independent build or hardware execution.
- Provisional Gold: S / 28 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5).
- License: MIT root; dependency licenses separately apply.

## Changes verified against source

- `src/LighthouseReckoning.cpp`: `getNextUpdateInMs()` supports power-aware wake scheduling.
- `src/LHR_RamConfig.h`: compile-time switch for a single queued locally originated packet (~248 bytes). Additional local packets can return `LHR_ERR_BUSY`; relay packets are not queued.
- `examples/ESP32/SleepyNode` and `examples/RP2040/SleepyNode`: new sleep-aware examples.
- ESP32 encryption detection updated in v1.3.0.

## Evidence and risk boundaries

- `.github/workflows/compile.yml` lists ESP32 and RP2040 compile jobs but does not list new SleepyNode sketches. A successful workflow run was not independently checked.
- The earlier 2026-08-09 forced-hop test documents approximately 1h53m of physically close, deliberately forced routing and three estimated losses; it does not demonstrate long-range RF performance or independently verify v1.3.0.
- AES-128-CCM is hop-by-hop with a network-wide key. Replay protection is not implemented.
- Global retry tracking and one local queue slot remain limitations.
- No third-party implementation source was copied.

## Next checks

Independently parse the committed field-test log; compile v1.3.0 SleepyNode sketches; test wake-up scheduling and queue behavior on RP2040/ESP32; audit nonce persistence and replay risks.
