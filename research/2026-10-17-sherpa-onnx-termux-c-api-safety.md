# sherpa-onnx — offline speech, Termux integration and C API safety

- Repository: https://github.com/k2-fsa/sherpa-onnx
- Inspection date: 2026-10-17
- Discovery: GitHub-first offline speech ecosystem
- Evidence: VERIFIED (upstream source, CI, releases; not independently run)
- Provisional ranking at review: S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- License: Apache-2.0 at repository root; model, runtime, accelerator and dependency licenses require separate inspection.

## What makes it useful

This toolkit implements offline and streaming speech recognition, speech synthesis, voice activity detection, speaker diarization/identification, keyword spotting, and related local audio processing. The upstream README documents Android, iOS, desktop and WebAssembly targets and multiple language bindings. Android/Termux support is especially useful for offline, user-controlled mobile systems.

## Reusable components verified by repository inspection

- `sherpa-onnx/csrc/` — native inference and audio processing implementations; contains source and tests such as `circular-buffer-test.cc`.
- `sherpa-onnx/c-api/c-api.h` and `c-api.cc` — C ABI for use from other languages; security-sensitive model loading and object creation.
- `sherpa-onnx/python/` — Python bindings and test directory.
- `sherpa-onnx/rust/` — Rust wrappers, FFI and build scripts.
- `.github/workflows/android.yaml` and other Android/architecture workflows — upstream build evidence, not evidence that this run built an APK.

Upstream release **v1.13.8** was published **2026-09-10**. Its release notes explicitly cite native builds inside Termux, Python-in-Termux and Rust API examples on Termux (PRs #3916, #3922, #3942). This supports availability of integration paths, not a device benchmark.

## Security and compatibility maintenance

- **2026-10-14:** PR #4044, `c-api: catch C++ exceptions in SherpaOnnxCreate* and return NULL`, merged. It addresses C++ exceptions crossing the C ABI. This fix postdates v1.13.8 and must not be presumed included in that release.
- **2026-10-16:** Swift offline recognizer wrapper correction for a new C configuration field merged as PR #4005; another example of active binding maintenance.
- **2026-10-17:** commit `1a9d234ab95567eba8c2e89873a87d70b79633e2` upgraded the Rust build-time `zip` dependency to v9 to address RUSTSEC-2026-0367, -0368 and -0369. The commit reports `DOCS_RS=1 cargo check` with zip 9.0.4; this is **upstream-reported testing**, not independent verification. The fix also postdates v1.13.8.

## Requirements and risks

Exact model files, RAM and storage needs, and CPU/NPU backend requirements vary widely. Downloaded model weights, proprietary accelerator SDKs and transitive dependencies are not automatically covered by the root Apache-2.0 license. Validate downloaded models and select a version containing required fixes before embedding into other applications. A C API null-return change can require callers to handle failed initialization explicitly.

## Verification boundary

Inspected repository README, root LICENSE, native/C API/Python/Rust source directory listings, Android CI workflow inventory, release v1.13.8 notes, merged PR #4044 and current commits. **Did not** install packages, build the code, run tests, load models, measure recognition accuracy, benchmark ARM64 Termux or perform a security audit. No upstream implementation code was copied.

## Follow-up

Test the smallest offline ASR/VAD configuration on ARM64 Termux; record model size, peak RSS, CPU use, energy consumption, cold-start latency and recognition latency. Verify which tagged release first contains the C API and Rust zip fixes; check individual model licenses and compare with whisper.cpp for offline deployments.

Sources:
- https://github.com/k2-fsa/sherpa-onnx/releases/tag/v1.13.8
- https://github.com/k2-fsa/sherpa-onnx/pull/4044
- https://github.com/k2-fsa/sherpa-onnx/commit/1a9d234ab95567eba8c2e89873a87d70b79633e2
