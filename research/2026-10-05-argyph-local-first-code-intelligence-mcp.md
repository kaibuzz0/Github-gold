# Argyph — local-first code intelligence MCP server

- **Repository:** https://github.com/Ezzy1630/argyph
- **Author / Org:** Ezzy1630
- **Category:** developer tooling / MCP / local-first AI / code intelligence / semantic search / Rust
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29/30 — S
  - Utility 5
  - Working Evidence 5
  - Reusability 5
  - Novelty 4
  - Documentation 5
  - Maintenance 5
- **Discovery:** GitHub-first discovery, 2026-10-05.

## Why it matters

Argyph is a read-only, local-first MCP server for giving coding agents bounded codebase context without requiring a cloud vector database or remote embedding API. It combines grep-style text retrieval, tree-sitter symbol intelligence, structural lookup for non-code files, hybrid semantic search, repository packing, and persistent local memory behind one MCP endpoint.

Its strongest design feature is progressive indexing: useful filesystem/text tools come online first, symbol and structural indexes follow, and embeddings can build in the background. That architecture is reusable for agent systems that need fast cold-start retrieval over large repositories.

## High-value components

- three-tier progressive index: filesystem inventory → symbol/structural graph → embeddings
- tree-sitter definition/reference/caller/callee/import graph
- structural indexing for Markdown, JSON, YAML, TOML and CSV
- hybrid BM25 + vector retrieval backed by embedded LanceDB
- bundled local embedding path with no API key required for core semantic functionality
- ask routing layer selecting structural, symbol or semantic retrieval
- bounded Span response model with context budgets and expiring expansion handles
- token-budgeted repository packing
- incremental content-addressed updates with filesystem watching
- local FTS5-backed agent memory
- optional bounded locate_smart retrieval subagent
- modular Rust workspace separating parse, graph, embed, store, locate, pack, MCP, CLI and memory crates

## Platforms / requirements

Current workspace version inspected: **1.0.4**, Rust edition 2021, minimum Rust **1.88**. Upstream documents npm/npx, Cargo, Homebrew, DXT and prebuilt GitHub-release installation paths. Intel macOS lacks the normal prebuilt ONNX Runtime path and is documented as a source-build case.

## Evidence inspected

Repository-native evidence inspected on 2026-10-05 includes README, workspace manifest, architecture documentation, both root licenses and CI workflow.

The workspace contains twelve focused implementation crates plus benchmarks. Workspace policy forbids unsafe Rust and denies Clippy unwrap_used.

CI runs formatting, a source-file size/modularity gate, Clippy with warnings denied, cargo test across the workspace, Linux/macOS/Windows matrices, and an opt-in live-provider E2E job for the smart retrieval feature.

The README reports current release **v1.0.4** across multiple distribution channels. Architecture documentation explicitly records limitations, including best-effort rather than LSP-precise cross-file symbol resolution.

## Evidence boundary

GitHub Gold did **not** compile Argyph, execute its tests or benchmarks, install its release artifacts, index a large repository, reproduce claimed indexing times, measure retrieval quality, verify npm/crates/Homebrew packages independently, or audit its dependency/security posture.

Performance figures such as sub-second Tier-0 indexing on a 1M-LOC repository are treated as upstream claims, not independently reproduced measurements.

VERIFIED means concrete implementation structure, tests/CI, packaging, licenses and detailed architecture evidence were inspected; it is not independent performance certification.

## License

Workspace license: **MIT OR Apache-2.0**, with both license texts present. No upstream source was copied into GitHub Gold. Dependencies, bundled models and distribution artifacts should still be checked individually before extracting or redistributing components.

## Caveats / risks

- Cross-file symbol resolution is explicitly heuristic/best-effort rather than LSP-precise.
- Windows test/clippy jobs are currently advisory because upstream documents an ONNX Runtime/MSVC CRT linkage mismatch in dev/test profiles.
- The optional locate_smart feature can use remote OpenAI/Anthropic providers; local-first does not imply every optional configuration is offline.
- Semantic retrieval quality and advertised indexing timings require independent benchmark reproduction.
- Bundled embedding/runtime artifacts add supply-chain and platform-specific dependency considerations.

## Follow-up queue

1. Build v1.0.4 from source on Linux and run the full workspace test suite.
2. Reproduce Tier 0/1/2 indexing measurements on small, medium and ~1M-LOC repositories.
3. Compare symbol resolution against language-server ground truth across Rust, Python, TypeScript and Go.
4. Measure ask routing precision and bounded-span usefulness on representative coding-agent tasks.
5. Inspect incremental invalidation/content-addressing under rename, delete and branch-switch workloads.
6. Test index corruption/recovery and abrupt process termination.
7. Audit bundled embedding model/runtime provenance and release/package checksums.
8. Compare retrieval quality and resource use with Serena, repomix, GitNexus/CodeGraphContext and other local code-context systems.
9. Exercise FTS5 memory scoping, deletion and persistence behavior.
10. Reassess score after independent performance and retrieval-quality measurements.
