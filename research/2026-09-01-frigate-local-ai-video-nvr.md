# Frigate — local AI video/NVR pipeline

- **Repository:** https://github.com/blakeblackshear/frigate
- **Author / Org:** Frigate, Inc. / Blake Blackshear and contributors
- **Category:** self-hosting / edge AI / video analytics / NVR / IP cameras / Home Assistant / embedded accelerators
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28 / 30 (S)**
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **License:** MIT for repository code/configuration/docs; Frigate name/logo are separately protected trademarks.
- **Discovery:** GitHub-first broad-category research. No playlist-derived technical claim is used in this dossier.

## Why this is Gold

Frigate is a local-first network video recorder designed around realtime computer vision rather than a cloud camera service. It combines IP-camera ingest, motion gating, local object detection, recording/retention, MQTT integration, low-latency live viewing, camera access control, enrichment/search features, and multiple hardware-accelerated inference backends in one actively maintained system.

The main architectural pattern is valuable beyond surveillance: use a very cheap first-stage signal (motion) to decide when to spend scarce accelerator/GPU resources on expensive inference. Upstream explicitly describes low-overhead motion detection as the gate for object detection and runs TensorFlow/object detection in separate processes with a realtime bias rather than attempting to process every frame.

That makes Frigate a useful reference for edge-AI systems where video ingest, multiprocessing, accelerator scheduling, event creation, storage, search, and realtime UI must coexist on constrained local hardware.

## Inspected evidence

### Application behavior and system design

The current upstream README describes:

- fully local AI object detection for IP cameras;
- OpenCV/TensorFlow-based realtime detection;
- heavy multiprocessing;
- low-overhead motion detection used to decide where object inference runs;
- object-detection work isolated into separate processes;
- MQTT integration;
- object-aware retention plus 24/7 recording;
- RTSP restreaming to reduce camera connection count;
- WebRTC and MSE low-latency live viewing;
- a companion Home Assistant integration.

Upstream strongly recommends a GPU or dedicated AI accelerator for serious deployments.

### Reusable internal surfaces

The current `frigate/` source tree exposes separable subsystems including:

- `api/` — HTTP/API boundary;
- `camera/` — camera runtime handling;
- `comms/` — internal/external communication paths;
- `config/` — typed/configuration infrastructure;
- `data_processing/` — post-capture processing;
- `db/` — persistent data layer;
- `detectors/` — detector abstraction, worker/runners and configuration;
- `embeddings/` — vector/semantic-search infrastructure;
- `events/` — event lifecycle;
- `genai/` — generative-AI providers and orchestration;
- `debug_replay.py` — replaying recorded footage through detection/motion processing;
- `ffmpeg_presets.py` — FFmpeg-oriented ingest/transcode presets.

The detector layer is especially reusable as an architecture reference. The repository separates detector API/configuration/runners from hardware-specific plugins. The currently inspected plugin directory includes adapters for CPU TensorFlow Lite, EdgeTPU, Hailo, MemryX, ONNX, OpenVINO, Rockchip RKNN, Synaptics, TensorRT, AXEngine and ZMQ IPC, alongside a deprecated DeepStack path. This is strong evidence that hardware acceleration is implemented as a modular backend boundary rather than hard-wired to one accelerator vendor.

The 0.18 release-candidate notes also state that the DeGirum detector was removed after that vendor ceased operations and that DeepStack is deprecated for removal in 0.19. That is useful maintenance behavior: stale accelerator integrations are being retired rather than indefinitely presented as supported.

### CI and tests

The current pull-request workflow includes:

- web linting and i18n consistency checks;
- production web build;
- Playwright Chromium end-to-end tests with failure artifacts;
- Ruff format/lint checks for Python;
- devcontainer construction;
- `mypy` static checking;
- API-spec consistency verification;
- Python unit tests executed with `python3 -u -m unittest` inside the devcontainer.

The main CI separately builds multiple deployment images/targets, including standard AMD64 and ARM64, Raspberry Pi, NVIDIA TensorRT/Jetson, AMD ROCm, Rockchip, and Synaptics variants. This provides upstream build evidence across a materially heterogeneous hardware matrix.

One supply-chain detail is mixed: inspected workflows use `persist-credentials: false` for checkout, and some actions are pinned to immutable commit SHAs, while several others are still referenced by version tags such as `actions/checkout@v6` and `docker/build-push-action@v7`.

## Releases and maintenance

The latest stable GitHub release inspected is **v0.17.2**, published **2026-06-28**. It ships through several container-image variants including standard ARM64, TensorRT, Rockchip, ROCm, JetPack 6 and Synaptics builds.

A newer **v0.18.0-rc1** was published **2026-08-30**. Its release notes document substantial active work including complete UI-based configuration, profiles, expanded GenAI provider support, local `llama.cpp` integration, semantic-search embedding offload, motion search/review, debug replay, FFmpeg 8 migration, GPU-stat changes, and multiple security fixes.

Recent `dev` history inspected reaches **2026-08-31**, including an iOS HLS fix backport, so the repository is clearly active immediately before this research pass.

## Security / trust boundaries

Frigate deserves a high score, but its security history should be treated as important operational evidence rather than ignored.

The v0.17.2 release explicitly documents fixes for several serious issues affecting exposed or role-restricted installations, including access-control bypasses, arbitrary host-file read, go2rtc configuration paths reaching code execution/container escape, RTSP credential leakage, and WebSocket authorization failures. The same release notes also listed additional viewer-role information/access-control issues that were still planned for later fixes at that time.

The newer 0.18 release candidate records additional hardening such as sanitizing user-controlled path components, restricting review-summary reports to users with access to all cameras, validating WebPush endpoints, and rate-limiting password changes.

**Operational conclusion:** Frigate should not be treated as a safe unauthenticated service to expose directly to the public internet merely because it is self-hosted. Authentication, camera ACLs, proxy boundaries, network segmentation, timely upgrades, configuration review and backup of the database/configuration are meaningful parts of deployment security.

The rapid security-fix cadence is a positive maintenance signal, but the number and severity of recent advisories are also a real caveat for internet-facing or multi-tenant use.

## Requirements / platforms

Typical deployment is containerized Linux with IP cameras and storage. Serious realtime workloads benefit strongly from hardware acceleration. Current upstream build/release surfaces cover AMD64, ARM64/Raspberry Pi, NVIDIA TensorRT/Jetson, AMD ROCm, Rockchip and Synaptics variants, while detector code contains additional accelerator backends.

Main implementation technologies observed include Python, TypeScript/JavaScript web code, Docker/build infrastructure, FFmpeg, OpenCV and ML-runtime integrations.

## Licensing / reuse

The root license is MIT and permits use, modification and redistribution with preservation of the copyright/license notice.

However, the upstream README separately states that the **Frigate**, **Frigate NVR** name and logo are trademarks and are not covered by the MIT software license. Reuse of code and reuse of branding are therefore different questions.

Frigate also integrates substantial external runtimes, models, media libraries and accelerator SDKs. Any attempt to extract a specific detector integration, bundled dependency, model or container component should inspect that dependency's own license before copying it elsewhere.

No Frigate source code was copied into GitHub Gold during this pass.

## Verification boundary

GitHub Gold inspected current upstream repository structure, README, root license, selected detector/plugin surfaces, GitHub Actions workflows, stable/release-candidate metadata and recent commit history.

GitHub Gold did **not**:

- build Frigate locally;
- run its unit, Playwright or container tests;
- connect a camera;
- record or restream video;
- execute object detection;
- test any GPU/NPU/TPU accelerator;
- exercise Home Assistant or MQTT integration;
- benchmark CPU/GPU/storage use;
- test authentication or camera ACLs;
- reproduce any CVE/GHSA;
- perform penetration testing;
- validate container-image signatures or provenance;
- independently audit FFmpeg, go2rtc, ML models or accelerator SDKs.

Claims above are therefore source/release/workflow evidence, not GitHub Gold runtime verification.

## Strong reusable components / patterns

1. **Motion-gated inference pipeline** — cheap motion analysis selects when/where expensive object detection runs.
2. **Detector backend abstraction** — common detector API with heterogeneous accelerator plugins.
3. **Multiprocess realtime pipeline** — inference isolation and realtime prioritization rather than every-frame processing.
4. **RTSP restream fan-out** — reduce direct connection pressure on cameras while serving downstream consumers.
5. **Debug replay** — feed recorded media back through detection/motion logic for reproducible tuning.
6. **Semantic search / embeddings** — bridge event metadata and visual embeddings for local media retrieval.
7. **MQTT integration** — expose camera/event state into generic automation systems.
8. **Hardware-specific container targets** — practical packaging patterns for CUDA/TensorRT, ROCm, Rockchip, Raspberry Pi and other edge accelerators.

## Related / recursive research leads

- `blakeblackshear/frigate-hass-integration` — Home Assistant integration and camera/control boundary;
- `AlexxIT/go2rtc` — RTSP/WebRTC/restream transport layer used in the Frigate ecosystem;
- Frigate detector plugin internals, particularly ONNX/OpenVINO/TensorRT/RKNN/Hailo;
- `frigate/embeddings` semantic-search architecture;
- `frigate/debug_replay.py` as a reproducible video-pipeline testing/tuning component;
- recent GHSA remediation commits to map authorization boundaries and regression tests;
- the 0.18 local `llama.cpp` provider and GenAI tool-calling boundary.

## Follow-up questions

- How are camera frames shared between ingest, motion, detector and recording processes without unnecessary copying?
- What exact detector plugin interface is stable enough to support third-party accelerators?
- Which security advisories now have explicit regression tests, and which authorization paths still depend heavily on nginx/go2rtc configuration?
- How does Debug Replay reproduce timestamps, motion state and detector scheduling compared with a live stream?
- How are semantic-search embeddings indexed and invalidated when events/recordings are deleted or permissions change?

## Verdict

**VERIFIED — S / 28.**

Frigate is unusually valuable because it combines a real production-oriented local video pipeline with modular accelerator support, local-first storage/search, extensive hardware packaging, automation integration, and active tests/releases. The strongest Gold value is not just the complete NVR; it is the architecture for building resource-aware edge-AI video systems.

The score stops short of 29–30 because component reuse is coupled to a large multimedia/ML stack and because the recent security-advisory history materially raises the deployment-review burden for exposed or role-separated installations.