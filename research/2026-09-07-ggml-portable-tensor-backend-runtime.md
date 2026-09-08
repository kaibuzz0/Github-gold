# ggml: portable tensor and heterogeneous backend runtime

- **Repository:** https://github.com/ggml-org/ggml
- **Author / organization:** ggml-org
- **Category:** local AI, machine learning runtime, tensor library, heterogeneous compute
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 29 / 30
- **Provisional tier:** S
- **License:** MIT
- **Discovery source:** recursive research from the previously verified `ggml-org/llama.cpp` dossier

## Executive assessment

`ggml-org/ggml` is independently valuable enough to catalog apart from `llama.cpp`. It is a portable C/C++ tensor runtime focused on low-dependency local machine-learning execution, explicit graph/tensor construction, quantized numerical formats, runtime memory planning, and heterogeneous backends.

The upstream README describes a plain C/C++ implementation with no required dependencies, support across x86, ARM, RISC-V, LoongArch, PowerPC, s390x and WebAssembly, SIMD-optimized kernels, CPU/GPU/NPU/browser backends, 2- through 8-bit integer quantization plus MXFP4/NVFP4, and a runtime design intended to perform no memory allocations during graph execution.

Its strongest GitHub Gold value is not a single application but a set of reusable systems primitives: tensor graph representation, allocator/planner, backend registration and dynamic loading, device-buffer abstractions, graph scheduling, quantized kernels, architecture-specific CPU paths, GPU/accelerator backends, and RPC/distributed-backend machinery.

## Why it matters

`ggml` is useful as a compact reference architecture for local inference engines and other compute-heavy software that needs to remain portable across CPUs and heterogeneous accelerators. It is especially relevant for low-resource, offline, edge and user-controlled AI systems where a heavyweight framework is undesirable.

The project is also an ecosystem substrate rather than a one-model runtime. Its APIs and backend layer are reused by projects in the ggml organization, and upstream explicitly directs core-library contributions through `llama.cpp` so changes receive its broader testing/review surface.

## High-value components

### Core tensor / graph runtime

Important source areas include the core tensor implementation, graph construction/execution APIs, operation definitions and datatype/quantization primitives. This is the foundational layer from which model-specific runtimes build computation graphs.

### Runtime allocator and graph memory planning

`src/ggml-alloc.c` is a substantial standalone subsystem for graph/tensor allocation and buffer planning. Memory planning is particularly valuable in constrained inference because model runtimes need predictable reuse of large buffers and minimal allocation churn.

### Backend abstraction

The repository separates generic backend interfaces and implementation helpers from concrete devices. Current source includes substantial backend implementation/registration code such as:

- `src/ggml-backend.cpp`
- `src/ggml-backend-impl.h`
- `src/ggml-backend-reg.cpp`
- `src/ggml-backend-dl.cpp`
- `src/ggml-backend-meta.cpp`

This creates a reusable boundary between graph execution and device-specific kernels.

### Architecture and accelerator backends

The source tree contains dedicated backend directories including CPU, CUDA, BLAS and CANN, with additional backends represented elsewhere in the project/release history. The current release line documents active CUDA/ROCm, Metal, Vulkan, SYCL, OpenCL, Hexagon, OpenVINO, RPC and WebGPU development.

### Quantization and low-resource inference primitives

The project directly supports multiple low-bit formats. These are valuable not merely as compression utilities but as integrated tensor representations with backend-specific kernels, allowing models to run on lower-memory hardware.

### RPC backend

The current release documents RPC protocol 6.0.0, asynchronous/event APIs, Apple RDMA transport and work to avoid serializing remote buffers. This is technically interesting because it extends the same backend abstraction across process/machine boundaries.

Treat RPC as a widened trust boundary. It deserves separate security and failure-recovery inspection before being recommended for untrusted networks.

## Working evidence

The current `build-cpu` workflow runs the project's CI harness on Ubuntu x86-64 and ARM64 in both low-performance and higher-performance configurations. ARM64 testing includes alternative feature combinations such as no-SVE/no-BF16 paths and extra tests.

The workflow calls `ci/run.sh` rather than only compiling a trivial target, which is stronger evidence than build-only CI. It also shows active testing of portability paths rather than assuming one host architecture.

The inspected workflow uses mutable version/tag references such as `actions/checkout@v6` and `ggml-org/ccache-action@v1.2.16` rather than immutable commit-SHA pinning. Record this as a software-supply-chain caveat, not as evidence that the workflow is compromised.

## Release and maintenance evidence

The latest stable release inspected is **v0.23.0**, published **2026-09-04**. The release is not marked immutable and currently has no attached release assets; source tarball/zipball endpoints are provided by GitHub.

The v0.23.0 release documents major work in:

- sparse-attention APIs and kernels;
- asynchronous backend scheduling/event APIs;
- allocation-size/dependency tracking;
- CPU correctness fixes and architecture-specific kernels;
- CUDA/ROCm, Metal, Vulkan, SYCL and OpenCL optimization/correctness work;
- Hexagon NPU support;
- OpenVINO support;
- WebGPU correctness fixes;
- RPC 6.0.0 and Apple RDMA transport.

The repository reports a push date of **2026-09-04**, matching the latest release generation. The broader development path is unusually active because upstream core changes are commonly developed and reviewed in `llama.cpp` and synchronized into this repository.

## Scoring

| Dimension | Score | Notes |
| --- | ---: | --- |
| Utility | 5/5 | General tensor/inference substrate used across local-AI runtimes. |
| Working Evidence | 5/5 | Multi-architecture CI and an explicit CI test harness; broad downstream exercise through llama.cpp is additional upstream evidence. |
| Reusability | 5/5 | Clear C/C++ APIs, allocator, scheduler, backend abstraction and device implementations. |
| Novelty | 4/5 | Tensor runtimes are not novel as a category, but ggml's compact, low-dependency, quantization-first heterogeneous design is distinctive. |
| Documentation | 5/5 | Quickstart, GGUF documentation, examples, release notes and substantial ecosystem documentation. |
| Maintenance | 5/5 | Active 2026 release line and ongoing backend/core work. |

**Total: 29/30 — provisional S tier.**

## License and reuse boundary

The root project is licensed under the **MIT License**, copyright 2023-2026 The ggml authors. The license permits use, modification, distribution, sublicensing and sale subject to preservation of the copyright and permission notice.

No ggml source was copied into GitHub Gold during this research pass.

Model weights, tokenizers, datasets, compiler/runtime SDKs, vendor GPU/NPU libraries and other assets used with ggml can have independent licenses and terms. The root MIT license should not be generalized to those external components.

## Verification performed

This dossier is based on repository-native inspection of:

- repository metadata and maintenance state;
- `README.md`;
- the source-tree structure;
- the CPU CI workflow;
- the current release metadata/changelog;
- the root `LICENSE`.

This establishes source/document/workflow/release evidence only.

## Not independently verified

GitHub Gold did **not**:

- clone or build ggml;
- execute `ci/run.sh` or unit tests;
- run the simple matrix-multiplication example;
- load or execute a model;
- benchmark CPU/GPU/NPU/WebGPU performance;
- verify zero runtime allocations independently;
- validate numerical accuracy across quantized formats;
- test CUDA, ROCm, Metal, Vulkan, SYCL, OpenCL, Hexagon, OpenVINO, CANN or other accelerators;
- exercise RPC or RDMA;
- fuzz tensor shapes, graph construction, backend loading or RPC messages;
- perform a security audit.

## Caveats and risks

- The highest-value optimization paths are hardware-specific and cannot be inferred to work equally well on all devices from repository evidence alone.
- Numerical correctness and performance can vary substantially across quantization formats and backends.
- Dynamic backend loading expands the local trust boundary when arbitrary libraries can be loaded.
- RPC/distributed execution expands the network trust boundary and deserves protocol/authentication/resource-exhaustion review.
- The repository and `llama.cpp` are tightly coupled development-wise; users should understand version compatibility rather than mixing arbitrary snapshots.
- The inspected CPU workflow uses mutable Action/tag references rather than immutable SHA pinning.

## Related projects

- `ggml-org/llama.cpp` — already verified in GitHub Gold; model runtime/server/tooling built on ggml.
- Other ggml-org runtimes such as whisper.cpp are natural recursive research candidates.
- GGUF is a closely related file-format layer but should be evaluated separately from the compute runtime.

## Strong follow-up leads

1. Inspect `ggml-alloc` and scheduler invariants for buffer lifetime, aliasing and allocation-expansion behavior.
2. Trace backend registration/dynamic loading and the backend-device capability interface.
3. Evaluate quantization format definitions plus architecture-specific dequant/matmul kernels as reusable components.
4. Inspect RPC protocol 6.0.0 for authentication assumptions, malformed-message handling, resource limits and failure recovery.
5. Evaluate GGUF parsing/metadata validation as an independent component dossier.
6. Compare ggml's backend abstraction with ONNX Runtime, TensorStore-style execution abstractions and smaller embedded inference runtimes.
7. Inspect WebAssembly/WebGPU paths for browser/offline deployment.
8. Research `whisper.cpp` independently as an offline speech-recognition stack.
