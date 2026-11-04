# Dora and Asterics AAC — upstream evidence and promotion (2026-10-23)

## Provenance and hygiene
Independent GitHub-first category rotation across robotics and accessibility, informed by existing deep-research dossiers. Before promotion: 68 canonical projects, 68 matching master headings, 68 complete score breakdowns, empty candidate queue, neither project already cataloged. Continue existing draft PR #7 on `agent/research-ladybird-browser-engine`; no parallel branch or unrelated deletions. All six exact playlist IDs from `sources/youtube_playlists.md` were searched publicly on 2026-10-23, with no usable results or transcripts; neither project is attributed to YouTube.

## Dora — VERIFIED upstream, S / 29
- Repository: https://github.com/dora-rs/dora
- Prior dossier: `research/2026-09-26-dora-real-time-robotics-dataflow.md`.
- License: Apache-2.0 root `LICENSE`; third-party libraries, models and Node Hub packages have independent licensing.
- Release: v1.1.0 stable, published 2026-10-08, 14 assets. Cargo workspace version 1.1.0, `rust-version = "1.95.0"`; CI Rust 1.97.1.
- Source inspected: `binaries/coordinator/src/` for liveness/scheduling/topology; `binaries/daemon/` for execution; `libraries/arrow-convert/`; `binaries/record-node/src/main.rs`; `binaries/replay-node/src/main.rs`; `libraries/recording/src/lib.rs`; `apis/`; `tests/` with fault-tolerance and daemon reconnect E2E tests.
- **Source-level limitation:** `libraries/recording/src/lib.rs` explicitly states it is **internal, not a public stable API**, even though published to crates.io; `.drec` current `FORMAT_VERSION` is 2, and `MAX_RECORD_BYTES` is 64 MiB with reader/writer size checks. Do not advertise as a stable standalone format library.
- CI: 2026-10-22 main push https://github.com/dora-rs/dora/actions/runs/39797929129 passed **13/13 jobs**, including Linux tests, E2E, semantic contracts, benchmark regression, audit and license checks. A separate 2026-10-24 PR check https://github.com/dora-rs/dora/actions/runs/40058412440 passed 9 static jobs but skipped 4 expensive tests; do not misrepresent PR check as an E2E run.
- Maintenance: October 22 commits improve record-node IPC encoding and runtime/Arrow conversions. README performance and zero-copy comparisons remain upstream claims.
- Score: utility 5, working 5, reuse 5, novelty 4, docs 5, maintenance 5 = **29/30**.
- Not performed: independent build, dataflow run, ROS2/Zenoh interoperability, network fault injection, benchmark reproduction, robot hardware or security audit. Soft real-time is not safety certification.
- Next: backpressure/failure behavior, coordinator restart recovery, `.drec` version migration; follow `dora-rs/dora-hub`, Zenoh, `Ekumen-OS/andino-rs`.

## Asterics AAC — VERIFIED upstream, S / 28
- Repository: https://github.com/asterics/Asterics-AAC
- Prior dossier: `research/2026-09-25-asterics-aac-offline-accessibility-platform.md`.
- License: AGPL-3.0 source (`LICENSE`, `package.json`); README states CC BY-SA 4.0 for documentation/non-source. External symbols, fonts, voices and services need separate rights review.
- Release: `release-2026-10-21-12.10/+0200` published 2026-10-21; fixes word-form retention, navigation and imports. No attached release binaries; hosted stable/beta deployments documented.
- Source inspected: `src/js/input/scanning.js` supports auto/binary/linear switch scanning; `inputEventHandler.js` handles input events; `src/js/service/predictionService.js`, `speechService.js`, `actionService.js`; `src/js/service/data/pouchDbService.js`, `pouchDbAdapter.js`, `encryptionService.js` and `encryptionService.test.js`. `serviceWorker.js` imports bundled Workbox 7.4.0 and precache paths.
- CI: 2026-10-23 PR Beta release - Build https://github.com/asterics/Asterics-AAC/actions/runs/39950169970 succeeded. Its workflow executes `npm run build`; `package.json` defines this as `jest && webpack --config webpack.config.js --env production && node scripts/getServiceWorkerCachePaths.js`. Thus upstream automated Jest and build succeeded. Deployment run 39950355651 succeeded but is not a browser/assistive hardware test.
- Maintenance: 2026-10-21 release and source commits; Node 22 workflow, Vue 2.7.15 remains a modernization consideration.
- Score: utility 5, working 4, reuse 5, novelty 4, docs 5, maintenance 5 = **28/30**; discount for no independent UI/offline/hardware evidence.
- Not performed: PWA installation, fresh-install offline test, switch/eye gaze input, TTS device matrix, user usability study, cloud sync or encryption audit. Optional HTTP actions, Matrix and cloud sync increase network/privacy surface.
- Next: verify offline cold-start and cached symbols, switch scanning, `asterics/predictionary`, `asterics/FabiWare` and sensor bridges.

## Validation and code handling
Promote 68 → 70 canonical entries with complete six-factor scoring, two matching master headings and no duplicate URLs or names. Preserve candidate queue and existing dossiers. No third-party source or assets copied. Check new Catalog Audit runs after publication before reporting CI success.
