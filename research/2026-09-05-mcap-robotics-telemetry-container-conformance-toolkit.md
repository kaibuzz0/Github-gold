# MCAP — robotics telemetry container, multi-language libraries, and conformance toolkit

- Upstream: https://github.com/foxglove/mcap
- Project: MCAP
- Research date: 2026-09-05
- Category: robotics / telemetry / logging / binary file formats / data tooling / interoperability
- Evidence level: VERIFIED
- Provisional Gold score: S / 29
- License: MIT
- Primary repository language: Rust; maintained implementations also exist for C++, Go, Python, TypeScript/JavaScript, Swift, and Rust
- Discovery source: GitHub-first rotation into an underrepresented robotics/scientific-data category

## Executive finding

`foxglove/mcap` is both a serialization-agnostic telemetry/log container format and a mature multi-language implementation ecosystem. It is aimed heavily at robotics and pub/sub data, but the architecture is broadly reusable anywhere large time-ordered streams need schemas, channel metadata, compression, indexing, random access, attachments, metadata, and durable file interchange.

Its strongest Gold value is not simply the file extension. The repository contains a formal format specification, maintained readers/writers in six languages, a cross-language conformance corpus, ROS integration packages, a production CLI, compression/indexing support, corruption-recovery tooling, and fixtures that exercise multiple layout combinations.

The result is a strong reference implementation for designing durable binary event containers and a practical toolchain for robotics telemetry archives.

## Why it matters

Robotics systems frequently produce multiple asynchronous streams: camera frames, IMU data, transforms, control state, GPS, actuator telemetry, logs, annotations, and arbitrary application messages. A useful archive format has to preserve more than a byte stream.

MCAP provides explicit records for schemas, channels, messages, chunks, message indexes, chunk indexes, attachments, metadata, statistics, and summary offsets. Implementations can therefore support both sequential streaming and indexed access without coupling the container to one message serialization system.

This makes the project useful for:

- robot and autonomous-system log capture;
- offline telemetry analysis;
- sensor-fusion datasets;
- ROS 1 / ROS 2 data interchange;
- long-lived binary archive design;
- compressed event streams with random-access indexes;
- multi-language tooling around one on-disk format;
- recovery and diagnostics for damaged telemetry files.

## Multi-language implementation surface

The root documentation identifies maintained libraries for:

- C++;
- Go;
- Python;
- JavaScript / TypeScript;
- Swift;
- Rust.

Package distribution surfaces include Conan, PyPI, npm, crates.io, Go modules, Swift Package Manager-style integration, and release artifacts where applicable.

This is a major reusability signal: the format is not dependent on a single runtime or robotics framework.

## Format architecture

The codebase exposes the same core record model across implementations. Inspected type definitions include records such as:

- `Schema`;
- `Channel`;
- `Message`;
- `Chunk`;
- `MessageIndex`;
- `ChunkIndex`;
- `Attachment` / `AttachmentIndex`;
- `Metadata` / `MetadataIndex`;
- `Statistics`;
- `SummaryOffset`.

The presence of both data records and explicit summary/index records is technically important. It supports a design where writers can append time-series data while readers later use summary structures for targeted access instead of requiring a full sequential scan.

The repository also includes a Kaitai Struct definition for the file format, which is useful as an independent machine-readable description and for cross-language inspection/generation workflows.

## Conformance infrastructure

The cross-language conformance system is one of the strongest reusable components in the repository.

Search of the current tree shows conformance readers/writers or harnesses in multiple implementations, including Go, Rust, Swift, and TypeScript-oriented test infrastructure. Shared conformance data is stored under `tests/conformance/data/` and is reused by implementation-specific tests.

The Swift conformance executable explicitly supports operations such as `read-streamed`, `read-indexed`, and `write`, while the Rust tree includes conformance reader/writer examples. Go has dedicated `test-read-conformance` and `test-write-conformance` modules.

This is stronger evidence than six independent implementations that merely claim compatibility: the repository has an explicit mechanism for testing implementations against common data and behavior.

## CLI as a standalone working tool

The MCAP CLI is independently useful even for users who never link one of the libraries.

Current CLI documentation exposes operations including:

- `doctor` — validate/check MCAP structure;
- `recover` — attempt data recovery from a potentially corrupt file;
- `merge` — combine MCAP files;
- `sort` — rewrite with reordered messages;
- `compress` / `decompress`;
- `du` — compute byte-usage statistics;
- inspection and filtering-related workflows documented by the CLI.

This moves MCAP beyond a format specification into an operational archive-maintenance toolkit.

## ROS and serialization ecosystem

The Python publishing workflow includes separate packages for:

- base `mcap`;
- Protobuf support;
- ROS 1 support;
- ROS 2 support.

That separation is a good architectural signal: the core container is serialization-agnostic while framework/serialization adapters remain layered around it.

The TypeScript examples also include format conversion and writer examples, including bag-to-MCAP and other application-specific conversions.

## Working evidence

The current CI workflow is unusually broad.

### C++

- GCC and Clang Linux builds;
- format checks;
- host unit tests;
- example compilation and execution;
- separate Windows unit-test path.

### Go

- linting;
- tests;
- conformance tests through the Go workspace;
- release-version consistency checks.

### Python

- linting;
- tests;
- examples;
- package builds;
- publication paths for base MCAP, Protobuf, ROS 1, and ROS 2 packages.

### Rust

- rustfmt and Clippy;
- workspace builds/tests;
- feature-matrix checks for compression and Tokio combinations;
- WASM target build/check;
- declared minimum-supported-Rust-version verification;
- `cargo publish --dry-run`.

### Swift

- SwiftLint / SwiftFormat;
- build and test;
- release-version consistency checking.

### TypeScript / JavaScript

- immutable dependency installation;
- dedupe/format/lint/build steps across core/support/node/browser packages;
- tests;
- example type-checking/testing;
- npm publication with provenance enabled for release paths.

### CLI

The inspected workflow defines release builds across Linux, macOS, and Windows architectures, including Linux amd64/arm64/arm and macOS amd64/arm64.

This cross-language CI depth is a major reason for the 5/5 Working Evidence score.

## Release and maintenance evidence

GitHub repository metadata showed the project active and non-archived, with the repository updated on **2026-09-04** and the default branch showing recent maintenance through **2026-09-01** during this inspection.

The latest release returned by the repository release feed during this run was **MCAP CLI v0.3.0, published July 15, 2026**. Its GitHub release assets include SHA-256 digest metadata for multiple platform binaries, including Linux, macOS, and Windows builds.

The repository uses independently versioned package/release lines, so a single global semantic version should not be assumed to describe every language implementation.

## Supply-chain / reproducibility notes

The CI is strong functionally, but GitHub Action references in the inspected workflow are mostly major-version or release-tag references such as `actions/checkout@v7`, `actions/setup-go@v7`, `actions/setup-node@v7`, `astral-sh/setup-uv@v10.0.1`, and `pypa/gh-action-pypi-publish@release/v1` rather than immutable commit SHAs.

That is normal for many active projects but weaker than workflows that pin every third-party Action to a commit digest.

Positive signals include:

- immutable package lock/install behavior in the TypeScript path;
- explicit MSRV checking for Rust;
- package-version vs release-tag consistency checks;
- npm provenance publishing;
- PyPI trusted-publishing style OIDC permissions in the Python job;
- release assets carrying GitHub-provided SHA-256 digest metadata.

## Licensing

Repository metadata and the root README identify MCAP as MIT licensed.

No MCAP source code was copied into GitHub Gold. The project is cataloged and linked for reuse subject to its upstream license and notices.

## Gold score

Provisional score: **29 / 30 — S tier**

- Utility: **5/5** — solves a concrete telemetry/logging problem across robotics and general event-stream archives.
- Working Evidence: **5/5** — extensive multi-language CI, conformance fixtures, tests, examples, packaging, and release binaries.
- Reusability: **5/5** — format specification plus six maintained implementation languages, CLI, adapters, and conformance infrastructure.
- Novelty: **4/5** — binary log containers and indexed telemetry formats are established ideas, but MCAP's serialization-agnostic, multi-language, robotics-focused execution is unusually strong.
- Documentation: **5/5** — specification, reference matrix, language docs, CLI docs, evaluation material, and Kaitai definition.
- Maintenance: **5/5** — active 2026 maintenance and fresh CLI release evidence.

## Verification performed in this run

Inspected directly:

- repository metadata and maintenance state;
- root README;
- language/support matrix;
- current GitHub Actions workflow inventory and primary CI workflow;
- repository release feed and CLI v0.3.0 assets/digests;
- recent commit history;
- code search for conformance infrastructure;
- cross-language record/index types;
- CLI documentation for doctor/recover/merge/sort/compression functionality;
- existing GitHub Gold catalog search to avoid duplication.

## Verification boundary

I did **not**:

- compile any MCAP library;
- run the repository CI locally;
- execute conformance tests;
- generate or parse an MCAP file;
- convert a ROS bag;
- run `mcap doctor`, `recover`, `merge`, `sort`, or compression commands;
- corrupt a file and measure recovery behavior;
- benchmark throughput, compression ratio, indexing cost, or memory usage;
- independently hash release binaries;
- verify every language implementation against every conformance fixture;
- conduct a security audit or parser-fuzzing campaign.

Claims above are limited to direct repository/source/workflow/release inspection or clearly identified upstream evidence.

## Risks and limitations

- A binary parser exposed to untrusted files remains a security-sensitive input surface; broad conformance coverage does not substitute for a parser security audit.
- Multi-language implementations can drift unless the shared conformance corpus remains comprehensive.
- Random-access performance depends on how writers configure chunks, compression, message indexes, and summary data.
- Recovery tools can recover structurally discoverable data but should not be assumed to reconstruct information that was never durably written.
- Compression support adds native/library dependencies and CPU tradeoffs.
- Independently versioned language packages require users to track compatibility per implementation rather than relying on one repository-wide version.
- GitHub Actions are not comprehensively pinned to immutable SHAs in the inspected CI workflow.

## Strongest follow-up leads

1. Inspect `tests/conformance` as a standalone format-verification corpus and map exactly which record/layout combinations it covers.
2. Trace chunk writing, CRC handling, message indexes, summary offsets, and random-access reader behavior across two independent implementations.
3. Inspect the Rust CLI `recover` and `doctor` paths for corruption-resynchronization and validation invariants.
4. Compare MCAP with ROS bag2/SQLite storage and Parquet-oriented robotics telemetry pipelines for workload-specific tradeoffs.
5. Inspect Foxglove's ROS/MCAP conversion tools and ecosystem integrations for additional reusable components.
6. Evaluate parser fuzzing and malformed-file regression coverage as a potential maintenance/security improvement area.