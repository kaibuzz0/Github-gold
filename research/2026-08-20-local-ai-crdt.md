# Research Dossier — Local AI and CRDT Infrastructure

Date: 2026-08-20

This dossier records two deeply inspected promotion candidates for GitHub Gold. These are research findings, not claims that GitHub Gold itself built or benchmarked the projects.

## ggml-org/whisper.cpp

- Repository: https://github.com/ggml-org/whisper.cpp
- Category: local AI / speech recognition / embedded inference
- Evidence: VERIFIED
- Provisional tier / score: S / 29
- License: MIT
- Languages: C, C++ with bindings and examples for additional runtimes
- Platforms documented upstream: macOS, iOS, Android, Java, Linux, FreeBSD, WebAssembly, Windows, Raspberry Pi, Docker

### What it does

A dependency-light C/C++ implementation of OpenAI Whisper inference designed for local and offline automatic speech recognition. Upstream documents CPU-only inference, architecture-specific SIMD acceleration, Metal/Core ML, CUDA, Vulkan, ROCm, OpenVINO, Ascend NPU support, integer quantization, a C API, and voice-activity detection.

### Why it is valuable

It provides a compact offline speech stack that can be embedded into phones, desktops, Raspberry Pi-class systems, browsers through WASM, and custom applications without requiring a hosted inference API. The high-level implementation is concentrated in `include/whisper.h` and `src/whisper.cpp`, making the architecture unusually inspectable.

### Useful components

- `include/whisper.h` — public C-style API
- `src/whisper.cpp` — high-level Whisper inference implementation
- `examples/cli` — command-line transcription reference
- real-time microphone streaming examples
- VAD support
- quantization tooling
- model conversion/download tooling under `models/`
- Android, iOS, WASM, Java, and Docker integration examples
- GPU/backend integration patterns via ggml
- release workflow with artifact attestations
- `talk-llama` example demonstrating speech-to-LLM composition

### Working / maintenance evidence

The README exposes CI status and a stable release. Upstream released v1.9.3 on 2026-08-20 and continued repository maintenance the same day. The v1.9.3 release work also updated release automation and added artifact attestation support. The README includes reproducible CMake build and CLI invocation instructions.

### Verification boundary

GitHub Gold inspected repository metadata, README documentation, root license, and recent commits. GitHub Gold did not compile models or run transcription benchmarks in this pass.

### Reuse caveats

MIT licensing permits broad reuse subject to preserving the copyright and permission notice. Whisper model weights and any third-party backend dependencies may have separate terms and should be checked independently before redistribution.

## loro-dev/loro

- Repository: https://github.com/loro-dev/loro
- Category: local-first / CRDT / collaborative state infrastructure
- Evidence: VERIFIED
- Provisional tier / score: S / 28
- License: MIT
- Core language: Rust, with JavaScript/WASM and Swift support documented upstream

### What it does

A CRDT library for collaborative and local-first applications. It supports peer-to-peer synchronization, automatic merging, local availability, delta updates, versioned history and time travel, plus multiple CRDT structures including text, rich text, moveable trees, moveable lists, and maps.

### Why it is valuable

Loro is useful below the application layer: instead of being a finished note app or sync service, it provides reusable replicated-data primitives that can be embedded into many local-first systems. Its combination of CRDT synchronization and version-control-like history makes it useful for editors, structured documents, offline applications, collaborative databases, and resilient peer synchronization.

### Useful components

- Rust CRDT core
- JavaScript/WASM package `loro-crdt`
- Swift support
- Fugue-based text editing
- rich-text CRDT
- moveable tree and list CRDTs
- LWW map and mergeable child containers
- delta export/import synchronization API
- shallow snapshots comparable to shallow clones
- fast time-travel/history APIs
- Loro Inspector for document-state/history inspection
- `loro-ffi` ecosystem for additional language bindings

### Working / maintenance evidence

The README includes a runnable synchronization example showing update export/import between documents. Recent August 2026 commits include correctness fixes for shallow-snapshot rich-text redaction, performance work on JavaScript text storage, and regression/performance tests around redundant text marks and styled reads.

### Verification boundary

GitHub Gold inspected the README, root license, repository metadata, and recent commits. It did not independently run the Rust or JavaScript test suites in this pass.

### Reuse caveats

The root project is MIT licensed. Individual optional ecosystem repositories, bindings, or integrations should still be checked for their own license terms before copying code.

## Promotion recommendation

Both projects meet the current promotion bar and should be promoted atomically into `MASTER_LIST.md` and `catalog/tools.json` in a later synchronized promotion batch after the catalog audit gate is applied.
