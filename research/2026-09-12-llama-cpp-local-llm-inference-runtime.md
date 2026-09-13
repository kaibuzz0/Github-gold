# llama.cpp — Local LLM/VLM Inference Runtime

- **Repository:** https://github.com/ggml-org/llama.cpp
- **Author / Org:** ggml-org
- **Category:** local AI / LLM inference / multimodal / C++ / accelerator backends / API server
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
- **Discovery:** GitHub-first discovery; no YouTube-derived claim used in this dossier.

## Why it matters

`llama.cpp` is a dependency-light C/C++ runtime for running large language models and vision-language models locally or on servers across unusually broad hardware. It combines a reusable inference library, quantized model support, command-line tools, an OpenAI-compatible HTTP server, model conversion/quantization tooling, multimodal support, multiple accelerator backends, and cross-platform release engineering in one actively maintained codebase.

The main value for GitHub Gold is not merely “run a chatbot locally.” The repository is a dense source of reusable systems work around tensor backends, quantization, heterogeneous CPU/GPU execution, model loading, tokenization, sampling, grammar-constrained generation, KV/cache management, HTTP inference serving, model conversion, benchmark tooling, and portable deployment.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Enables local/offline LLM and VLM inference plus reusable library/server/tooling surfaces. |
| Working evidence | 5 | Extensive upstream CI builds/tests CPU paths and numerous hardware/backend/platform configurations; frequent automated releases. |
| Reusability | 5 | MIT-licensed core, C/C++ API, tools, server, GGUF ecosystem, multiple build/deployment targets. |
| Novelty | 4 | Quantized local inference is now a broad ecosystem, but llama.cpp remains technically distinctive in portability and backend breadth. |
| Documentation | 5 | Strong README plus dedicated build/backend/server/Android/multi-GPU/model/release documentation. |
| Maintenance | 5 | Multiple substantive commits and automated release builds observed on 2026-09-12. |

## Repository-native evidence

The README states the project targets LLM/VLM inference with minimal setup across local and cloud hardware. It documents CPU optimizations for Apple Silicon, x86 and RISC-V; low-bit quantization; custom CUDA kernels; HIP, Vulkan, SYCL and other accelerator paths; CPU+GPU hybrid inference; Android support; multi-GPU use; and an OpenAI-compatible `llama serve` interface.

Current backend documentation lists BLAS/BLIS, CANN, CUDA, HIP, Hexagon/Snapdragon, IBM zDNN, MUSA, Metal, OpenCL/Adreno, OpenVINO work, RPC, SYCL, VirtGPU, Vulkan, WebGPU and ZenDNN surfaces.

Upstream CPU CI builds x64 and arm64 Linux targets and Windows x64/arm64 variants, enables fatal warnings and RPC, runs `ctest -L main`, and performs an end-to-end llama2c conversion followed by text generation from the resulting GGUF model. The repository also carries dedicated workflows for Android, Apple platforms, Snapdragon, CUDA Linux/Windows, cross-compilation, CANN, IBM and additional backend/release paths.

## Useful components to revisit

- `src/` and public llama API — model loading, inference, context/KV state and sampling integration.
- `ggml/` — tensor runtime and CPU/accelerator backend machinery.
- `tools/server/` — OpenAI-compatible inference server, routing, model lifecycle and web UI integration.
- `tools/cli/` / completion tooling — direct local inference surfaces.
- `tools/rpc/` — distributed/remote backend execution surface.
- GGUF/model conversion and quantization utilities.
- `grammars/` — GBNF grammar-constrained generation.
- backend-specific CUDA, HIP, Metal, Vulkan, SYCL, OpenCL, Hexagon and other implementations.
- benchmark/performance tooling and model-format utilities.

## Platforms / requirements

The project builds on Linux, Windows, macOS and Android, with Apple XCFramework packaging and many architecture/backend-specific paths. Exact requirements depend heavily on selected backend: CPU-only builds can remain relatively simple, while CUDA/HIP/SYCL/OpenCL/Metal/etc. require the corresponding vendor SDK/toolchain.

Models are separate artifacts and carry their own licenses and usage restrictions. The MIT license of llama.cpp does **not** grant rights to arbitrary model weights.

## Licensing

- **Repository root:** MIT License.
- Copyright notice and permission text must be retained when copying substantial portions.
- Bundled/acknowledged third-party components include separately licensed dependencies such as `cpp-httplib`, `stb`, `nlohmann/json`, `miniaudio`, and `subprocess.h`; component-level license review remains required before extraction.
- Model weights, tokenizers and externally downloaded assets require their own license review.

No third-party source, binaries or model weights were copied into GitHub Gold during this run.

## Maintenance signals

Recent inspected commits on **2026-09-12** included server model-download lifecycle fixes, AMD GCN/HIP configuration work, server header corrections, a `cpp-httplib` vendor update, graceful SYCL handling for unsupported quantization, RPC static-link fixes, and router state-command framing fixes.

Automated prerelease build **b10931** was published on **2026-09-12**. Its release notes expose platform artifacts for macOS arm64/x64, iOS XCFramework, Ubuntu x64/arm64/s390x, Vulkan, ROCm, OpenVINO, SYCL, Android arm64, multiple Windows CPU/CUDA/Vulkan/OpenVINO/SYCL/ROCm variants, and supply-chain attestations.

## Verification performed

GitHub Gold inspected the upstream README, root MIT license, workflow inventory, CPU build/test workflow, current release metadata and recent commit history.

**Not performed:** GitHub Gold did not compile or execute llama.cpp, download or run model weights, execute upstream tests, benchmark inference, validate output correctness, exercise GPU/NPU backends, run the HTTP server, audit model parsers, reproduce release binaries, verify attestations independently, or conduct a security audit.

Upstream CI/release evidence is therefore recorded as **upstream working evidence**, not as independent local execution by GitHub Gold.

## Caveats / risks

- Hardware/backend support quality varies; a listed backend does not imply identical feature/performance maturity.
- Model memory requirements can be substantial even with quantization.
- Quantization trades memory/performance against model quality.
- `llama-server` is network-facing software and should be deployed with normal access-control, patching and exposure precautions.
- Model licenses and acceptable-use conditions are independent of llama.cpp's MIT license.
- Fast development means APIs, model support and backend behavior can change quickly.

## Related ecosystem

- `ggml-org/ggml` — underlying tensor library/runtime.
- GGUF model ecosystem and Hugging Face-hosted compatible weights.
- bindings and applications built around the llama C API / server API.
- accelerator backend ecosystems such as CUDA, HIP, Metal, Vulkan, SYCL and OpenCL.

## Follow-up research

1. Map the public `libllama` API and ABI stability guarantees.
2. Inspect GGUF parser/model-loader validation and malformed-model hardening.
3. Separate reusable quantization kernels and conversion utilities from application-layer tools.
4. Inspect KV-cache architecture, cache reuse and long-context memory behavior.
5. Study speculative decoding, batching, continuous batching and scheduler behavior.
6. Review `llama-server` auth, model-download, routing and network-exposure boundaries.
7. Compare backend feature parity and fallback behavior across CPU/CUDA/HIP/Metal/Vulkan/SYCL/OpenCL.
8. Inspect release attestations and reproducibility story.
9. Follow `ggml-org/ggml` independently as a likely Gold-level reusable core.
