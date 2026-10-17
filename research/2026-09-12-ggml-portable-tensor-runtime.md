# ggml — Portable Tensor Runtime for Machine Learning

- **Repository:** https://github.com/ggml-org/ggml
- **Author / Org:** ggml-org
- **Category:** machine learning runtime / tensor library / C/C++ / quantization / heterogeneous accelerators / local AI infrastructure
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
- **Discovery:** GitHub-first recursive follow-up from the `ggml-org/llama.cpp` dossier; no YouTube-derived technical claim used.

## Why it matters

`ggml` is the reusable tensor/runtime layer underneath the broader ggml ecosystem. Upstream describes it as a dependency-light C/C++ tensor library designed for portable machine learning with minimal setup. The repository exposes tensor operations, graph execution, memory allocation, backend registration/loading, quantization, CPU kernels, GPU/NPU backends, RPC/distributed execution surfaces, examples, and a formal GGUF documentation surface.

For GitHub Gold, the value is architectural rather than application-specific. `ggml` demonstrates how a compact native runtime can target CPUs, GPUs, NPUs, browsers and multiple instruction-set families while retaining a common graph/tensor API. It is also a useful source of implementation patterns for low-bit quantization, backend capability dispatch, graph scheduling, device buffers, heterogeneous execution and low-dependency local inference.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Reusable tensor/runtime infrastructure for local ML inference and model implementations. |
| Working evidence | 5 | CPU CI builds/tests x64 and arm64 paths; self-hosted CI exercises CUDA, Vulkan and Metal; CI includes CTest and real GPT-2 generation paths. |
| Reusability | 5 | MIT-licensed C/C++ core with public headers, modular backends, examples and CMake packaging. |
| Novelty | 4 | Tensor runtimes are not unique, but ggml's low-dependency design, quantization focus and hardware breadth remain technically distinctive. |
| Documentation | 5 | Concise README, GGUF specification, examples, build files and release notes expose architecture and supported capabilities. |
| Maintenance | 5 | Formal v0.23.0 release on 2026-09-04 plus continuing sync/optimization/fix activity observed through 2026-09-09. |

## Repository-native evidence

The README states that `ggml` is implemented in plain C/C++ without mandatory external dependencies, targets x86, ARM, RISC-V, LoongArch, PowerPC, s390x and WebAssembly, provides SIMD-optimized kernels, supports CPU/GPU/NPU/browser backends, and includes 2- to 8-bit integer quantization plus MXFP4 and NVFP4 microscaling formats.

The `src/` tree separates core execution and backend infrastructure from architecture-specific implementations. Notable reusable areas include:

- `ggml-backend.cpp` — backend/device/buffer execution plumbing;
- `ggml-backend-reg.cpp` and `ggml-backend-dl.cpp` — backend registration and dynamic loading;
- `ggml-alloc.c` — graph/tensor allocation machinery;
- `ggml-common.h` — shared tensor/quantization implementation support;
- `ggml-cpu/` — CPU kernels and architecture-specific optimized paths;
- `ggml-cuda/` — CUDA/HIP-oriented accelerator implementation;
- `ggml-blas/`, `ggml-cann/`, `ggml-hexagon/`, `ggml-opencl/`, `ggml-openvino/`, `ggml-rpc/`, `ggml-sycl/`, `ggml-vulkan/`, `ggml-webgpu/` and additional backend directories present in the current source tree.

Upstream's README directs core `ggml` contributions through `llama.cpp`, noting that this gives changes greater visibility and broader testing before they are synchronized into the standalone `ggml` repository. This workflow is important when interpreting commit provenance: many standalone commits are synchronized from upstream work first reviewed in `llama.cpp`.

## Working evidence

The current `build-cpu.yml` workflow exercises both x64 and arm64 Linux runners in lower- and higher-performance configurations. All routes invoke the project's shared `ci/run.sh` harness.

That CI harness performs Debug and Release CMake builds and runs CTest. It also contains an end-to-end GPT-2 path that downloads an upstream model fixture and executes several generated binaries, including backend, scheduler and batched generation variants, to perform short text generation rather than only compilation.

The separate self-hosted workflow runs the same CI harness on physical/hosted accelerator configurations including:

- NVIDIA CUDA;
- NVIDIA Vulkan with and without cooperative-matrix-2 support;
- Apple Silicon Metal;
- Apple Silicon Vulkan.

This is strong upstream working evidence. GitHub Gold did not independently reproduce those runs.

## Releases and maintenance

The latest stable release inspected was **v0.23.0, published 2026-09-04**. Its release notes describe new operators and backend-scheduling APIs for sparse attention, asynchronous execution and allocation-dependency tracking, along with broad correctness/performance changes across CPU, CUDA/ROCm, Metal, Vulkan, SYCL, OpenCL, Hexagon, OpenVINO, RPC and WebGPU.

Recent standalone-repository history observed on **2026-09-09** included a synchronization from `llama.cpp` plus substantive backend changes such as:

- RDNA3 routed-MoE MMQ tile sizing;
- configurable CUDA flash-attention quantization combinations;
- a dedicated Vulkan IQ4_XS matrix-vector shader;
- Intel cooperative-matrix Vulkan pipeline/tile tuning;
- reduced test initialization threading;
- IQ-type handling for MoE;
- MSVC/Clang vector-load compatibility fixes;
- Metal IQ3_XXS dispatch fixes;
- OpenCL handling for non-contiguous Conv2D input;
- precision API updates.

Because the repository intentionally syncs core changes from `llama.cpp`, maintenance should be evaluated together with that upstream contribution path rather than from standalone commit cadence alone.

## Useful components to revisit

- **Backend registry/loading** — reusable plugin-style accelerator discovery and runtime backend selection.
- **Graph scheduler** — placement, execution ordering, cross-backend graph scheduling and asynchronous/event APIs.
- **Allocator** — graph-aware tensor/buffer allocation and dependency tracking.
- **CPU kernels** — architecture-specific SIMD and quantized operations across x86, ARM, RISC-V and other targets.
- **Quantization formats/kernels** — low-bit integer formats plus MXFP4/NVFP4 and IQ-family implementations.
- **CUDA/HIP backend** — matrix kernels, flash attention, MoE, device memory and multi-device execution.
- **Metal/Vulkan/SYCL/OpenCL/Hexagon/OpenVINO/WebGPU backends** — useful references for common tensor semantics across very different accelerator APIs.
- **RPC backend** — remote execution protocol, asynchronous events and distributed device abstraction.
- **GGUF documentation** — model/tensor container format used broadly across the ggml ecosystem.
- **CI harness** — one reusable pattern for validating the same graph/runtime behavior across multiple hardware backends.

## Platforms / requirements

The core library is intended to build with CMake and a C/C++ toolchain. CPU-only use is comparatively dependency-light. Accelerator builds require the relevant platform SDK/toolchain such as CUDA, Vulkan, Metal, SYCL, OpenCL, CANN or other vendor/runtime dependencies.

The README explicitly lists x86, ARM, RISC-V, LoongArch, PowerPC, s390x and WebAssembly among supported CPU/platform families. Backend support and operator parity can vary by device and backend.

## Licensing

- **Repository root:** MIT License.
- Copyright and permission notices must be preserved when substantial source is copied or redistributed.
- Accelerator/vendor SDKs, model weights, example assets and separately vendored components may carry independent terms.
- Model files and datasets are not licensed merely because the runtime itself is MIT.

No upstream source code, model data, binaries or artifacts were copied into GitHub Gold during this run.

## Verification performed

GitHub Gold inspected:

- current upstream README;
- root MIT license;
- current workflow inventory;
- CPU CI workflow;
- shared CI harness;
- self-hosted accelerator CI workflow;
- source-tree/backend layout;
- latest inspected release metadata and notes;
- recent commit history.

**Not performed:** GitHub Gold did not compile or execute `ggml`, run CTest, download/run the GPT-2 test model, test CUDA/Metal/Vulkan/SYCL/OpenCL/NPU backends, benchmark kernels, validate numerical correctness, fuzz graph/model inputs, inspect every backend's dependency license, reproduce release artifacts, or conduct a security audit.

Repository evidence is therefore recorded as **upstream working evidence**, not independent local execution.

## Caveats / risks

- Backend/operator support is heterogeneous; presence of a backend does not imply complete feature parity.
- Performance claims are hardware-, model- and kernel-dependent.
- Low-bit quantization trades memory/speed against numerical/model-quality characteristics.
- APIs and backend interfaces evolve quickly alongside `llama.cpp`.
- The standalone repository is partly a synchronized downstream view of core work landing through `llama.cpp`; provenance should be followed back to the originating PR when deep auditing matters.
- Model weights, datasets and vendor SDKs have separate licensing and security considerations.
- RPC/device backends increase trust-boundary and network-surface complexity compared with CPU-only local execution.

## Related ecosystem

- `ggml-org/llama.cpp` — primary application/runtime integration and contribution path for core ggml work.
- `ggml-org/whisper.cpp` — speech-recognition runtime using ggml infrastructure.
- GGUF-compatible model tooling and model-hosting ecosystems.
- accelerator APIs/ecosystems including CUDA, ROCm/HIP, Metal, Vulkan, SYCL, OpenCL, Hexagon and WebGPU.

## Follow-up research

1. Map the public backend API and assess ABI/API stability across releases.
2. Inspect graph scheduler placement, fallback and cross-device synchronization semantics.
3. Study allocator lifetime/dependency tracking and zero-runtime-allocation claims in representative paths.
4. Catalog quantization formats, conversion rules and per-backend kernel coverage.
5. Inspect GGUF parser validation, bounds checking and malformed-file behavior.
6. Review RPC protocol trust boundaries, authentication assumptions and remote-buffer semantics.
7. Compare numerical correctness tests across CPU, CUDA, Metal, Vulkan, SYCL and OpenCL.
8. Inspect backend dynamic loading/search paths and plugin trust boundaries.
9. Trace how core changes flow from `llama.cpp` into `ggml` releases and whether version synchronization is deterministic/reproducible.
