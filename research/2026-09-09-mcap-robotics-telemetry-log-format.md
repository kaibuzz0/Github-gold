# MCAP — polyglot robotics telemetry log format and tooling ecosystem

- **Repository:** https://github.com/foxglove/mcap
- **Organization:** Foxglove
- **Category:** Robotics / telemetry / binary log formats / data infrastructure / developer tooling
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary implementation languages:** C++, Go, Python, Rust, TypeScript/JavaScript, Swift
- **License:** MIT
- **Discovery source:** GitHub-first category rotation into robotics/telemetry infrastructure
- **Inspection date:** 2026-09-09

## Executive finding

MCAP is a serialization-agnostic container format and library ecosystem for recording timestamped pub/sub messages. It is particularly relevant to robotics and other telemetry-heavy systems because it is designed around large append-oriented logs, arbitrary message serialization, indexed/random access, streaming access, compression, attachments, metadata, and durability/resource constraints rather than one specific robotics middleware.

The repository is unusually strong as reusable infrastructure because it does not stop at a specification. It contains maintained implementations in C++, Go, Python, Rust, TypeScript/JavaScript, and Swift, a command-line tool, language-specific packages, cross-language conformance machinery, examples, benchmarks, a Kaitai Struct description, documentation, and release automation.

The highest-value finding is the combination of **format specification + polyglot implementations + conformance corpus + bounded-memory design rules**. That combination makes MCAP useful both as an operational logging layer and as a reference architecture for designing durable, portable telemetry containers.

## What upstream says it is

The root README describes MCAP as a logging library and file format commonly used in robotics and intended to work across different workloads, resource constraints, and durability requirements.

The development guide provides a more precise architectural description: MCAP is a modular container format for timestamped pub/sub messages with arbitrary serialization formats. The repository itself is a polyglot library/SDK monorepo rather than a running hosted service.

Upstream provides:

- a formal file-format specification;
- a Kaitai Struct definition;
- a support matrix;
- a motivation/evaluation document;
- language libraries;
- a CLI for inspecting, merging, and splitting files;
- development, testing, linting, benchmark, and release instructions.

## High-value components

### Format specification

The specification is the core long-term asset. It defines a serialization-agnostic log container rather than tying stored messages to one schema system. This allows systems to preserve ROS messages, Protobuf, JSON-like data, FlatBuffers, custom binary payloads, and other encodings while retaining a common outer log structure.

High-value concepts to inspect recursively include:

- file/header/footer structure;
- schemas and channels;
- timestamped message records;
- chunks and compression;
- indexes and summaries;
- statistics;
- attachments;
- metadata;
- data-end records and CRC behavior;
- streamed versus indexed readers;
- recovery/durability behavior for partially written files.

### Cross-language libraries

The root README documents maintained implementations for:

- C++;
- Go;
- Python;
- JavaScript/TypeScript;
- Swift;
- Rust.

This matters because a portable telemetry format is only practically useful if independent producers/consumers can interoperate. The repository's conformance setup provides evidence that the implementations are intended to agree at the byte-format and behavior level rather than merely share a name.

### CLI

The repository ships an MCAP CLI implemented in the Rust workspace. The README documents CLI use for inspecting, merging, and splitting MCAP files, with packaged binaries available from GitHub Releases and Homebrew installation documented upstream.

The CLI is independently valuable for:

- log inspection;
- stream extraction;
- file splitting;
- file merging;
- validation/debugging workflows;
- pipeline integration without writing application code.

### ROS integration

The Python workspace includes separate support packages for ROS 1 and ROS 2, and the Go workspace includes ROS-related tooling. This makes MCAP more than a generic binary container in practice: it has direct bridges into a major robotics ecosystem while keeping the base format serialization-agnostic.

### Conformance infrastructure

This is one of the strongest reusable components in the repository.

The development guide states that cross-language conformance tests are orchestrated through a TypeScript harness and use generated inputs plus pre-built target-language readers/writers. The repository also contains language-specific conformance runners, including Go, Swift, and Rust paths observed during inspection.

This provides a useful engineering pattern for any multi-language binary protocol: generate canonical cases, execute implementations independently, and compare observable behavior rather than relying on language-specific unit tests alone.

### Kaitai Struct definition

The root README links a Kaitai Struct definition for the MCAP format. This is valuable for independent inspection/tool generation and as a second machine-readable representation of the format beyond handwritten libraries.

## Bounded-memory design requirement

The inspected development guide explicitly establishes **bounded memory when reading** as a design principle.

Upstream states that readers and the CLI must not read or force consumers to read an entire MCAP file into memory because files can be many gigabytes. Reader memory is expected to scale with the current record/chunk rather than total file length.

Documented strategies include:

- memory mapping seekable local files where appropriate;
- seek plus bounded-range reads for random access;
- streaming for sequential scans;
- spooling non-seekable/random-access-required streams to temporary files rather than buffering the entire input in RAM.

This is strong architectural evidence that the project is designed for real telemetry workloads rather than toy log files.

## Working evidence

MCAP has strong repository-native working evidence.

### C++ CI

The current CI workflow tests C++ with both Clang and GCC on Linux. It runs formatting checks, compiler-specific builds, host tests, example tests, and example execution. A separate Windows job builds tests and runs the generated unit-test executable.

### Go CI

The Go job checks out Git LFS conformance data, installs a pinned `golangci-lint`, runs linting, and executes the workspace test target. The development guide identifies the workspace as containing the core library, ROS tooling, and conformance tests.

### Python CI

The Python job:

- installs the environment with `uv`;
- runs linting;
- runs tests;
- runs examples;
- builds packages;
- publishes eligible builds to TestPyPI;
- publishes tagged releases to PyPI.

The repository contains separate Python packages for core MCAP, Protobuf support, ROS 1 support, and ROS 2 support.

### Rust CI

The Rust job is particularly extensive. It runs:

- rustfmt;
- clippy over the workspace;
- clippy across multiple feature combinations;
- full-workspace builds;
- full-workspace tests;
- WebAssembly-target build/checks;
- minimum-supported-Rust-version verification with `cargo-msrv`;
- `cargo publish --dry-run` before tagged publishing.

The feature-specific checks include no-default-feature combinations with LZ4, Zstd, Tokio, and combinations of async/compression features.

### Swift CI

The Swift job verifies release-version consistency when tagged, pins a Swift setup path, runs SwiftLint and SwiftFormat checks, then performs `swift build` and `swift test`.

### TypeScript CI

The TypeScript job uses a pinned Node/Yarn setup and runs immutable dependency installation, dedupe checks, formatting, lint/build steps across the core/support/node/browser workspaces, and the TypeScript test suite.

Tagged npm publishing uses package provenance support.

### Example validation

The CI workflow separately lint-checks and type-checks TypeScript example projects, including validation, ROS bag conversion, basic writing, FlatBuffers writing, annotation-demo, and ULog conversion examples.

## Release evidence

The newest overall GitHub release inspected on 2026-09-09 was **MCAP CLI v0.3.0**, published 2026-07-15.

The release exposes prebuilt binaries for multiple host/architecture combinations including:

- Linux amd64;
- Linux arm;
- Linux arm64;
- macOS amd64;
- macOS arm64;
- Windows amd64;
- Windows arm64.

GitHub's release metadata exposes SHA-256 digests for inspected assets. This is useful artifact provenance metadata, but GitHub Gold did not independently download and hash the binaries in this run.

The repository also releases language packages through their respective package ecosystems rather than relying exclusively on GitHub binary releases.

## Current maintenance evidence

The repository was active immediately before inspection. The newest inspected `main` commit was dated **2026-09-07** and changed Rust writer summary serialization to preserve ordered writer IDs while avoiding temporary vectors/sorting. The commit description specifically frames the change around bounded record-at-a-time cloning behavior.

Another inspected 2026-09-07 commit bumped the TypeScript core package to 2.2.2 and summarized recent core changes.

This is direct evidence that maintenance includes implementation details and memory behavior, not only documentation or dependency churn.

## Build and runtime requirements

Requirements vary by implementation.

### TypeScript

- Node.js 18.12+ documented in the development guide;
- Corepack;
- repository-pinned Yarn 4.x.

### Python

- Python 3.10+ development baseline documented upstream;
- `uv` for the current development environment.

### Go

- Go version pinned through `go/go.work`;
- `golangci-lint` for development linting.

### Rust

- stable Rust toolchain for normal development;
- rustfmt/clippy;
- optional feature combinations for LZ4, Zstd, Tokio;
- WebAssembly target tested in CI.

### C++

- Conan 2;
- CMake;
- Docker is used by documented development/build flows.

### Swift

- Swift 5.5+ documented as the baseline in the development guide; CI currently uses a newer pinned setup.

### Shared test requirement

Git LFS is required for the conformance data under the documented test paths. Upstream explicitly warns that tests will fail if the repository was cloned without retrieving those LFS objects.

## Reusability assessment

MCAP is highly reusable because its important assets exist at several levels:

1. **Use the format as-is** for telemetry/logging.
2. **Use one of the maintained language libraries** rather than reimplementing the format.
3. **Use the CLI** for shell/data-pipeline workflows.
4. **Use the conformance harness pattern** as a reference for another multi-language protocol.
5. **Use the Kaitai description** for independent parsing/tool generation.
6. **Study bounded-memory reader/writer patterns** for very large append-oriented files.
7. **Study package/release automation** across multiple language ecosystems.

Because the root license is permissive, code extraction is legally simpler than many catalog candidates, but file-level dependency and generated-code notices should still be reviewed before copying specific components.

## License

The repository root uses the **MIT License**, copyright Foxglove Technologies Inc.

The license permits use, copying, modification, merging, publishing, distribution, sublicensing, and sale subject to preserving the copyright and permission notice in copies or substantial portions.

No MCAP source code, binaries, test corpus, or third-party data were copied into GitHub Gold during this pass.

## Gold score rationale

### Utility — 5/5

A broadly useful telemetry/logging primitive with direct robotics relevance, generic pub/sub applicability, CLI tooling, and multi-language support.

### Working Evidence — 5/5

Strong multi-language CI, tests, examples, conformance machinery, release artifacts, package publishing, feature-matrix checks, and active implementation-level commits.

### Reusability — 5/5

Permissive license, multiple language libraries, generic serialization model, CLI, formal spec, and machine-readable Kaitai definition.

### Novelty — 4/5

Binary log/container formats are not inherently novel, but MCAP's combination of robotics-oriented workloads, arbitrary serialization, indexing/chunking, polyglot implementations, and conformance infrastructure is technically distinctive.

### Documentation — 5/5

Specification, support matrix, implementation READMEs, development guide, CLI documentation, release guide, API documentation, examples, and motivation/evaluation material are all present.

### Maintenance — 5/5

Current September 2026 implementation work, active package versions, broad CI, automated publishing, and recent CLI releases indicate ongoing maintenance.

## Important caveats

1. **GitHub Gold did not execute MCAP locally.** No library or CLI command was run during this inspection.
2. **Conformance tests were not independently executed.** Their existence and invocation are upstream repository evidence.
3. **Artifact digests were not independently verified.** GitHub release metadata exposes SHA-256 values, but binaries were not downloaded and hashed here.
4. **Serialization payload safety is external.** MCAP is a container; application-specific schema/parser vulnerabilities can still exist in data codecs layered on top.
5. **Large-file durability was not failure-tested.** Power-loss, truncation, disk-full, corrupted-index, and partial-chunk behavior should be independently tested before adopting it for safety-critical logging.
6. **Compression adds dependency/attack surface.** LZ4/Zstd implementations and decompression limits require normal defensive review for untrusted input.
7. **Language feature parity can differ.** The support matrix should be consulted before assuming every implementation supports every optional format feature identically.
8. **ROS integrations are ecosystem-specific layers.** Do not conflate MCAP itself with ROS bag semantics.

## Verification performed by GitHub Gold

This dossier inspected upstream repository-native evidence including:

- repository metadata;
- root README;
- root MIT license;
- development guide;
- CI workflow;
- cross-language conformance source paths/search results;
- current releases and release asset metadata;
- recent commits on `main`.

GitHub Gold did **not**:

- clone the repository;
- build any MCAP implementation;
- run unit tests;
- run conformance tests;
- create/read an MCAP file;
- run the CLI;
- run benchmarks;
- test ROS 1 or ROS 2 integration;
- fuzz malformed MCAP files;
- independently verify release SHA-256 digests;
- reproduce large-file bounded-memory characteristics;
- test crash/power-loss recovery.

All working claims are therefore based on inspected code structure, explicit upstream documentation, CI configuration, release metadata, or recent upstream commit evidence.

## Related ecosystem leads

Strong next research targets include:

1. **MCAP specification internals** — exact record layout, indexes, CRC semantics, chunking, statistics, attachments, metadata, and summary recovery.
2. **Cross-language conformance harness** — generated case model, expected-result normalization, malformed-file corpus, and parity gaps.
3. **Rust implementation** — indexed reader, async/Tokio paths, writer memory behavior, compression feature boundaries, and WebAssembly build support.
4. **C++ implementation** — zero/copy behavior, mapped I/O, embedded suitability, and Conan packaging.
5. **Python ROS support** — ROS 1/ROS 2 schema handling and conversion boundaries.
6. **MCAP CLI** — streaming behavior, merge/split algorithms, validation paths, and failure handling.
7. **Kaitai Struct model** — whether it fully captures optional/indexed structures and how useful it is for independent tooling.
8. **Durability testing** — intentionally truncate files at each record/chunk boundary and measure what remains readable/recoverable.
9. **Foxglove SDK/bridge ecosystem** — identify which tools consume MCAP directly and which components are separately valuable.
10. **ROS 2 native MCAP storage plugins** — trace actual deployment integration and compare against SQLite3 bag storage tradeoffs.

## Next-action recommendation

Keep MCAP at **VERIFIED / provisional S 29**. The strongest follow-up is a focused specification/conformance pass rather than another broad project summary: map the exact durability/indexing model, inspect malformed/truncated-file behavior encoded by tests, and identify reusable conformance fixtures without copying third-party test data.