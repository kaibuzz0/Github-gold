# OpenTelemetry Collector and OpenRTX — canonical promotion evidence (2026-10-23)

## Scope and provenance
Independent GitHub-first category rotation and refresh of earlier deep-research dossiers. Neither project was present in the 66-entry canonical JSON or master list at the start of this pass. The six YouTube playlist IDs remain in `sources/youtube_playlists.md`; public search for two IDs produced no usable playlist/transcript findings, so neither promotion is attributed to YouTube. This note records repository-native evidence, not a locally reproduced build or security certification.

## OpenTelemetry Collector — VERIFIED (upstream), S / 29
- Upstream: https://github.com/open-telemetry/opentelemetry-collector
- Earlier detailed dossier: `research/2026-09-01-opentelemetry-collector-modular-observability-pipeline.md`
- Latest inspected stable release: v0.163.0, published 2026-10-14 (GitHub releases API).
- License: Apache-2.0 root LICENSE; retain notices, check file-level headers and dependencies before adaptation.
- Platform and runtime: Go 1.26.0 in root `go.mod`. Its own comment says the root module is not the official binary build; official distribution manifests live in `open-telemetry/opentelemetry-collector-releases`.
- Source paths inspected: `receiver/`, `processor/`, `exporter/exporterhelper/`, `service/`, `config/`, `confmap/`, `pdata/`, `cmd/`.
- Reusable components: `exporter/exporterhelper/queue_batch.go`, `retry_sender.go`, request handling; service pipeline assembly; transport/configuration helpers; pluggable telemetry interfaces.
- Security source: https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md — no default embedded config, validate config before starting, encrypted connection defaults, avoid root and exposed sensitive extension data.
- CI: 2026-10-23 main push `build-and-test` https://github.com/open-telemetry/opentelemetry-collector/actions/runs/40012185839 completed successfully with 24 successful jobs and one skipped; coverage, unit test matrix, cross-build, lint and govulncheck jobs included. Additional main success: CodeQL https://github.com/open-telemetry/opentelemetry-collector/actions/runs/40012185757 ; ARM https://github.com/open-telemetry/opentelemetry-collector/actions/runs/40012185810 ; Windows https://github.com/open-telemetry/opentelemetry-collector/actions/runs/40012185622 ; builder integration https://github.com/open-telemetry/opentelemetry-collector/actions/runs/40012185787 .
- Score: utility 5, working evidence 5, reusability 5, novelty 4, documentation 5, maintenance 5 = 29. High scores reflect upstream modular source, comprehensive CI and active releases, **not** independent performance benchmarking.
- Caveats: untrusted receiver/exporter endpoints, secret/config serialization, exporter queue exhaustion, TLS policy and third-party extension trust need deployment-specific review. A successful cross-build is not a runtime test on each platform.
- Next: trace exporterhelper queue/batch state transitions and retry failure semantics; compare core vs contrib components; assess extension network exposure and resource caps.

## OpenRTX — VERIFIED (upstream), S / 26
- Upstream: https://github.com/OpenRTX/OpenRTX
- Earlier detailed dossier: `research/2026-09-06-openrtx-modular-amateur-radio-firmware-m17-stack.md`
- Latest inspected release: v0.4.5 published 2026-10-04 and marked **prerelease**. Do not call it stable.
- License: README states GPLv3; `REUSE.toml` gives GPL-3.0-or-later for project source and mixed exceptions, including GPL-2.0-or-later Miosix, MIT QDecoder, Apache-2.0/other vendor MCU code and MCD-ST Liberty licensed USB components. Root `LICENSES/` has SPDX texts. Do not copy without exact-file license review.
- Source paths inspected: `openrtx/src/protocols/M17/` contains `FrameEncoder.cpp`, `FrameDecoder.cpp`, `DSP.cpp`, `Golay.cpp`, `Modulator.cpp`, `Demodulator.cpp`, `Callsign.cpp`, `MetaText.cpp`. `openrtx/src/rtx/OpMode_M17.cpp` integrates M17 into radio runtime. `tests/unit/` includes M17 callsign, Golay, Viterbi, RRC, metadata and demodulator tests.
- Build inputs: `meson.build`, `CMakeLists.txt`, `requirements.txt`, `.github/workflows/main.yml`; cross-target builds, Linux variant, Zephyr ESP32-S3/T-TWR Plus and firmware packaging.
- CI: 2026-10-15 master push `Build and test` https://github.com/OpenRTX/OpenRTX/actions/runs/38790546561 completed successfully, all 13 jobs including unit-test, build-zephyr, build and 10 firmware packaging jobs. Distinct 2026-10-23 `Retevis-c62` PR-branch workflows https://github.com/OpenRTX/OpenRTX/actions/runs/40039127608 and https://github.com/OpenRTX/OpenRTX/actions/runs/40039127403 failed. The cause was not diagnosed here; do not attribute to mainline without evidence.
- Score: utility 4, working evidence 4, reusability 5, novelty 5, documentation 4, maintenance 4 = 26. Discount for experimental maturity, mixed licensing, device-specific risk and absence of independently reproduced hardware/radio operation.
- Caveats: upstream explicitly says highly experimental; firmware flashing can render a radio unusable, M17 support differs by hardware and can require modifications, and RF transmission is regulated. Successful firmware compilation is not evidence of radio interoperability.
- Next: investigate Retevis-c62 CI failures, inspect exact-file SPDX headers of M17 modules, test Linux emulation with recorded M17 frames and perform authorized on-air device interoperability testing.

## Verification boundary
Only GitHub API/source, release metadata, and upstream workflow results were inspected. No third-party source was copied. GitHub Gold did not compile or execute either project, run a collector, flash a radio, perform RF tests, reproduce CI or perform a security audit.

## Catalog maintenance
Canonical promotion: 66 → 68 entries, complete score breakdowns 66 → 68, one new human-readable section per project. All new URLs and names were checked against existing canonical entries. Preserve history and continue work on the existing draft research PR branch.
