# whisper.cpp — offline speech recognition runtime and reusable audio inference stack

- **Repository:** https://github.com/ggml-org/whisper.cpp
- **Organization:** ggml-org
- **Category:** Local AI / speech recognition / offline transcription / audio inference / Android / edge computing
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 (S tier)**
- **Primary license:** MIT
- **Discovery source:** Recursive research from the verified `ggml-org/llama.cpp` and `ggml-org/ggml` ecosystem
- **Inspection date:** 2026-09-07

## Executive assessment

`ggml-org/whisper.cpp` is a compact C/C++ implementation of OpenAI Whisper inference designed for local, offline automatic speech recognition. It is independently valuable from both `llama.cpp` and `ggml` because it packages a complete speech-specific runtime: audio preprocessing, Whisper model inference, a C API, command-line transcription, voice activity detection, quantization, platform adapters, model conversion/download tooling, and examples spanning desktop, mobile, browser and embedded/edge scenarios.

The current README documents CPU-only inference, integer quantization, Vulkan, NVIDIA CUDA, AMD ROCm, OpenVINO, Apple Metal/Core ML, AMD Ryzen AI NPU, Ascend NPU and additional accelerator support. Supported platforms include macOS, iOS, Android, Java, Linux, FreeBSD, WebAssembly, Windows, Raspberry Pi and Docker.

For GitHub Gold, its strongest value is the combination of a small embeddable API, offline operation, broad platform portability, quantized models, VAD, and reproducible CI across CPU and Android targets.

## Why it matters

Speech recognition is unusually useful in low-connectivity and privacy-sensitive workflows because the input often contains personal or operationally sensitive audio. A local runtime removes the requirement to stream speech to a remote transcription service.

High-value use cases include:

- offline transcription;
- private local voice notes;
- accessibility tooling;
- voice-command interfaces;
- field/laptop transcription without dependable connectivity;
- Android and Raspberry Pi speech interfaces;
- local assistant pipelines;
- batch transcription;
- VAD-driven speech segmentation;
- low-memory deployments using quantized models;
- embedding ASR into native applications through a C API.

## Repository structure and reusable components

### `include/whisper.h` + `src/whisper.cpp`

Upstream states that the high-level model implementation is concentrated in these files, with the remaining tensor/runtime machinery supplied by GGML.

This gives downstream applications a relatively narrow integration boundary compared with larger framework-dependent ASR stacks.

### `whisper-cli`

The documented quick start builds `whisper-cli` via CMake and transcribes a 16-bit WAV file locally.

The CLI is useful both as a production-adjacent local tool and as an executable reference implementation for the lower-level library API.

### Voice Activity Detection

VAD is a first-class documented feature and has dedicated CI. The current `build-vad.yml` workflow builds the project and explicitly runs `ctest -R ^test-vad$` with verbose failure output.

That makes VAD stronger than a README-only claim and a useful independent component lead for speech segmentation and wake/speech pipeline work.

### Quantization

The project supports integer quantization of Whisper GGML models. Upstream documents quantized models as requiring less disk and memory and potentially running more efficiently depending on hardware.

The repository includes a `quantize` executable and dedicated quantization-oriented CI/workflow coverage.

### Android implementations

Current Android CI builds two Android examples:

- `examples/whisper.android`, including a second build using an external GGML tree;
- `examples/whisper.android.java`.

The workflow uses pinned commit SHAs for checkout, Java setup and Android SDK setup. This is particularly relevant to GitHub Gold's Android/Termux/offline-device focus.

### Apple / Core ML / Metal

The README documents Apple Silicon acceleration through Metal and optional Core ML execution of the encoder through Apple's Neural Engine.

This is valuable as an architectural example of keeping the same speech model/runtime surface while allowing platform-specific accelerator paths.

### WebAssembly and browser execution

The repository includes a WebAssembly example, making browser/offline-web ASR another reusable deployment pattern worth tracing separately.

### Model acquisition and conversion tooling

The quick-start path downloads a converted GGML Whisper model using repository scripts. Model files are runtime inputs rather than part of the MIT source license boundary and require separate provenance/licensing review.

## Working evidence

Repository-native evidence inspected in this pass includes:

1. Dedicated CPU CI with x86-64 and ARM64 low-performance and high-performance configurations.
2. CPU CI invokes the repository's `ci/run.sh` test path rather than only compiling.
3. ARM64 high-performance CI explicitly varies SVE/BF16-related feature configurations.
4. Dedicated VAD CI builds and runs the `test-vad` CTest target.
5. Dedicated Android CI builds two Android application examples.
6. Android CI separately builds the main Android example against an external GGML tree, which is useful integration evidence.
7. A broad workflow surface exists for GCC, Clang, macOS, Core ML, sanitizers, quantization, SYCL, FreeBSD, bindings and other targets.
8. Current commit history reaches 2026-09-04 and includes synchronization to GGML 0.23.0 plus backend correctness and robustness fixes.
9. Current release artifacts include platform binaries and an Apple XCFramework with GitHub-provided SHA-256 digest metadata.

This is sufficient for repository-level VERIFIED status. It does not mean every model, language, device, accelerator or transcription path has been independently validated by GitHub Gold.

## Release and maintenance evidence

The latest GitHub release returned by the repository API during this inspection is **`b4938`**, published **2026-08-20**. It is a build-number-style release rather than a semantic-versioned stable release.

Inspected assets include:

- Apple XCFramework output;
- Ubuntu ARM64 binary archive;
- Ubuntu x64 binary archive;
- Windows Win32/x64 binary archives;
- BLAS-enabled Windows binaries;
- additional platform artifacts in the release asset set.

GitHub provides SHA-256 digest metadata for the inspected assets. The release is not marked immutable.

Development continued after that release. Recent inspected commit history on **2026-09-04** includes synchronization to **GGML 0.23.0**, Metal tuning, build-version handling improvements, safer backend search-path handling and CPU correctness fixes inherited through the synchronized GGML layer.

## Supply-chain and security caveats

The current CPU workflow pins `actions/checkout` to an immutable commit SHA, but `ggml-org/ccache-action` is referenced by a mutable version tag (`v1.2.21`). Pinning quality should therefore be reviewed workflow-by-workflow rather than assumed globally.

The Android workflow is stronger: checkout, Java setup and Android SDK setup are all pinned to explicit commit SHAs in the inspected version.

Local/offline use substantially reduces network exposure, but hostile or malformed model/audio inputs still create parser and memory-safety boundaries. Model download scripts also introduce a remote-supply-chain boundary that should be reviewed independently for integrity verification.

## Model and data licensing boundary

The **whisper.cpp source is MIT licensed**, but Whisper model weights, converted GGML model files, downloaded audio samples and any third-party datasets remain separate licensing/provenance objects.

A model being loadable by whisper.cpp does not imply that the model may be redistributed under MIT terms.

No source code, model weights, audio data or binaries were copied into GitHub Gold.

## Install / runtime context

The documented basic build is:

- clone the repository;
- download or prepare a supported Whisper GGML model;
- configure/build with CMake;
- run `whisper-cli` against supported audio input.

The README notes that the current CLI path expects 16-bit WAV input and gives an FFmpeg conversion example for other audio formats.

Hardware requirements depend strongly on model size and backend. The README currently lists approximate memory requirements ranging from a few hundred MB for tiny/base models to several GB for large models.

## Platforms and languages

Primary implementation is C/C++ with build/test/tooling and examples spanning shell, Python, Java/Gradle/Android, Objective-C/Apple integrations, WebAssembly/browser code and accelerator-specific support.

Documented execution environments include macOS Intel/Apple Silicon, iOS, Android, Java, Linux, FreeBSD, Windows, WebAssembly, Raspberry Pi and Docker.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Practical offline/private transcription, accessibility, voice interfaces and local assistant pipelines. |
| Working Evidence | 5/5 | CPU test workflows, dedicated VAD CTest, Android builds, broad platform CI, current release artifacts. |
| Reusability | 5/5 | C API, CLI, VAD, quantization, Android/mobile examples, browser and accelerator paths. |
| Novelty | 4/5 | Offline ASR is established, but this implementation's portability and low-dependency architecture remain unusually useful. |
| Documentation | 5/5 | Strong README, platform/backend instructions, quantization, model and example guidance. |
| Maintenance | 5/5 | Current development through 2026-09-04 and recent release artifacts from 2026-08-20. |
| **Total** | **29/30** | **Provisional S tier** |

## Verification boundary

GitHub Gold performed **repository source/document/workflow/release/history inspection only**.

GitHub Gold did **not**:

- clone or build whisper.cpp;
- run `ci/run.sh`;
- execute CTest or `test-vad`;
- download a Whisper model;
- transcribe audio;
- quantify word-error rate or language accuracy;
- benchmark CPU/GPU/NPU inference;
- quantize a model;
- run Android/iOS/WebAssembly examples;
- test Core ML, Metal, CUDA, ROCm, Vulkan, OpenVINO, SYCL or other accelerator paths;
- test microphone/streaming behavior;
- fuzz audio/model parsers;
- independently verify release artifacts or model downloads;
- perform a security audit.

Claims above are restricted to observed upstream repository documentation, workflows, release metadata and commit history.

## Related projects and recursive leads

- **ggml-org/ggml** — already independently verified as the tensor/backend foundation.
- **ggml-org/llama.cpp** — already independently verified local LLM/VLM runtime in the same ecosystem.
- **OpenAI Whisper** — original model architecture/reference implementation and model provenance source.
- **VAD subsystem** — worth deeper component-level inspection.
- **WebAssembly example** — useful lead for offline browser transcription.
- **Android examples** — high-value lead for field/mobile deployment and Termux-adjacent research.

## Follow-up research

1. Trace the audio preprocessing -> mel spectrogram -> encoder -> decoder -> token/timestamp output pipeline.
2. Inspect VAD implementation and test vectors independently.
3. Inspect model-file parsing and malformed-model boundaries.
4. Check model download/conversion scripts for digest/signature/integrity behavior.
5. Compare quantized-model accuracy/memory tradeoffs using upstream evidence without assuming benchmark claims.
6. Inspect streaming/microphone examples for bounded-buffer and latency behavior.
7. Evaluate Android native integration versus Termux-native CLI builds.
8. Inspect WebAssembly/browser deployment, threading and memory constraints.
9. Compare whisper.cpp against other local ASR engines such as sherpa-onnx or Vosk in a later breadth pass.
10. Consider `whisper-cli`, VAD and model conversion/download tooling as independent component entries if evidence justifies them.

## Verdict

**VERIFIED — provisional S / 29.**

`whisper.cpp` is GitHub Gold because it turns a high-value AI capability—speech recognition—into a portable, offline, embeddable runtime with strong repository-native evidence across CPU, mobile and specialized execution paths. The most valuable next work is not copying the implementation but tracing its VAD, model-loading, Android and WebAssembly boundaries as reusable design patterns and independently verifiable components.
