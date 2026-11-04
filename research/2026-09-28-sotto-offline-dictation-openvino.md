# Sotto — offline OpenVINO dictation and accessibility utility

- Upstream: https://github.com/smirk-dev/sotto
- Evidence level: VERIFIED (upstream evidence; not independently runtime-tested by GitHub Gold)
- Provisional Gold score: 26/30 — S tier
- Category: accessibility / offline speech-to-text / local-first productivity
- License: MIT for Sotto code; third-party components retain their own licenses
- Discovery: independent GitHub-first breadth rotation

## Why it matters

Sotto is a compact local dictation utility with unusually detailed engineering evidence for a small project. It provides press-to-talk and live dictation into arbitrary applications, with Windows and Linux paths, multilingual Whisper models, Hindi/Hinglish handling, local history, configurable hotkeys, noise gating and CPU/iGPU model selection. The useful research value is not merely the application: its repository documents practical failure modes and measured tradeoffs for OpenVINO Whisper inference, keyboard injection, streaming chunking, VAD/noise handling, packaged-model downloads and Intel integrated-GPU acceleration.

## Evidence inspected

The current README documents Windows packaged installation and Linux X11/Wayland operation. Windows uses low-level keyboard handling and Unicode input/clipboard fallback; Linux uses evdev for global hotkeys and xdotool/wtype for injection, with a documented GNOME-Wayland limitation and ydotool/X11 fallback.

`PROGRESS.md` is unusually valuable upstream verification material. It records on-machine benchmarks, rejected approaches, unit/integration tests and packaged-app tests. Upstream reports text-processing unit cases; Unicode injection round trips; hotkey/overlay tests; full-pipeline and streaming tests; microphone smoke tests; packaged `--selftest`; model-download failure/recovery testing; noise/VAD tests; and live app dictation into a real target. These are upstream claims backed by repository test artifacts and engineering notes, not GitHub Gold executions.

The latest inspected stable release is v1.4.0, published 2026-07-16. GitHub release metadata exposes a Windows x64 ZIP with a SHA-256 digest. Release notes report packaged-app measurements for `large-v3-turbo` on an i7-1360P/Iris Xe system, reducing warm hotkey-release-to-text latency from about 4.6 seconds on CPU to about 1.8 seconds on the iGPU, with CPU fallback when GPU execution is unavailable. The prior v1.3.1 release is also notable because upstream explicitly documents and fixes a packaged-release model-download bug that had prevented fresh installs from obtaining models.

## Gold scoring (provisional)

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Practical offline dictation/accessibility utility with press-to-talk and live typing. |
| Working evidence | 5 | Release artifact plus extensive upstream unit, integration, packaged-app and on-machine verification notes. |
| Reusability | 5 | Useful patterns for OpenVINO inference, hotkeys/input injection, VAD, streaming and model management. |
| Novelty | 4 | The product category is established, but the measured CPU/iGPU routing and Hindi/Hinglish robustness work are technically useful. |
| Documentation | 5 | README plus detailed engineering/benchmark log including rejected approaches and caveats. |
| Maintenance | 2 | Strong July 2026 development/release burst, but no newer inspected commits through this September 28 review. |
| **Total** | **26/30** | **S (provisional)** |

## Particularly useful components / leads

- per-model OpenVINO CPU/iGPU routing with graceful CPU fallback
- VAD/noise gate using energy plus spectral-flatness heuristics before transcription
- detect-then-correct language handling for English/Hindi/Hinglish and Urdu-script misclassification
- streaming chunk/overlap/dedup strategy designed around Whisper's fixed context window
- Windows low-level hotkey and Unicode `SendInput` path with clipboard fallback
- Linux evdev + xdotool/wtype injection abstraction across X11/Wayland
- packaged Hugging Face/OpenVINO model download integrity/completeness and resume handling
- engineering log of failed/rejected optimizations, useful for avoiding repeated dead ends

## Requirements / platforms

Windows 10/11 is the primary packaged target. Linux support is documented for X11 and Wayland, with Arch packaging available upstream. The implementation uses Python, PySide6, OpenVINO GenAI, sounddevice, NumPy, PyInstaller and Hugging Face model downloads. No discrete GPU is required; Intel integrated graphics are selectively useful for the largest inspected model.

## Licensing / provenance

Sotto's root license is MIT. The README explicitly states that bundled components retain their own licenses and points to `THIRD-PARTY-NOTICES.md`. Model licenses and third-party runtime licenses must therefore be reviewed independently before redistribution or extraction. No upstream implementation source was copied into GitHub Gold.

## Caveats

- GitHub Gold did not install, build or execute Sotto.
- GitHub Gold did not reproduce its latency, accuracy, VAD, injection, multilingual or GPU measurements.
- The published Windows executable is described upstream as unsigned; SmartScreen warnings are expected.
- Linux input-group access and synthetic input tools increase the importance of local permission review.
- GNOME Wayland has an upstream-documented virtual-keyboard limitation for the `wtype` path.
- Upstream Hindi/Hinglish measurements include synthetic/TTS-derived test material; they should not be generalized to all speakers or environments.
- v1.4.0 is the newest inspected release, dated 2026-07-16; no newer inspected commits were found during this pass.
- Release packaging and hashes establish artifact provenance/integrity metadata, not independent security or functional verification.

## Follow-up research

1. Inspect current test files and CI/workflow coverage to determine which upstream verification is automated versus manually recorded.
2. Audit `THIRD-PARTY-NOTICES.md` and exact licenses for OpenVINO model conversions and redistributed runtime components.
3. Trace the spectral-flatness VAD thresholds and malformed/noisy-input behavior for reusable defensive patterns.
4. Compare Sotto's Linux Wayland injection design with newer portal/virtual-keyboard approaches.
5. Compare its model-download completeness/resume checks with other local-model desktop applications.
6. Revisit maintenance status if development resumes or a post-v1.4 release appears.
