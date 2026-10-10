# Soma — local-first multimodal semantic search

- **Upstream:** https://github.com/AwesomeDog/soma
- **Author:** AwesomeDog
- **Category:** local-first search / offline AI / RAG / knowledge bases / multimodal indexing
- **Evidence:** VERIFIED (repository-native evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** **S / 27**
  - Utility: 5/5
  - Working evidence: 4/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **License:** MIT
- **Discovery:** GitHub-first breadth rotation after offline robotics research
- **Inspected:** 2026-09-28

## Why it matters

Soma is a local-first search engine that combines conventional lexical retrieval with local semantic retrieval and multimodal extraction while keeping the search/index path on the user's machine. The architecture is particularly useful as a reference for private RAG, air-gapped knowledge bases, agent retrieval backends, and cross-media desktop search.

Unlike a simple vector-search wrapper, the documented query path combines BM25 lexical search, dense vectors, HyDE, Reciprocal Rank Fusion, and a local reranker. Its ingestion path covers text/code, PDFs, Office/EPUB, images/screenshots, audio, and video, storing its index in SQLite with sqlite-vec.

## Useful surfaces

- Hybrid BM25 + vector + HyDE retrieval and RRF fusion.
- Local query expansion and reranking.
- CJK-aware lexical indexing using unigram/bigram handling plus Unicode normalization.
- PDF text/OCR extraction.
- Office/EPUB conversion through Pandoc.
- Image OCR plus local vision-model descriptions.
- Audio/video transcription through FFmpeg + Whisper tooling.
- SQLite + sqlite-vec local persistence.
- CLI, built-in Web UI, and HTTP API exposing a common command contract.
- Workspace-local `.soma/` mode for portable indexes.
- Air-gap model/tool export/import workflow.
- Machine-readable JSON/CSV/Markdown output suitable for agent/RAG integration.

## Repository-native evidence

The root repository contains implementation source, documentation, Maven/GraalVM build configuration, scripts, a dedicated `tests/e2e_tests.py` suite, and a GitHub Actions release workflow.

The release workflow builds native executables independently on macOS, Windows, and Linux using GraalVM Native Image. Each build is smoke-invoked with `--version` and `--help`, uploaded as an artifact, and release artifacts are attested before GitHub release creation. The workflow currently uses `-DskipTests`, so release-build success must not be represented as evidence that the E2E suite ran in CI.

Stable release **v0.10.1** was published on **2026-09-22** with Linux x64, macOS ARM64, and Windows x64 binaries. GitHub records SHA-256 digests for those release assets. The repository remained active through **2026-09-25**; recent history includes a code change intended to protect against large files plus documentation work.

The repository was created in July 2026, so despite strong engineering/documentation signals it has a short operating history and very small visible adoption footprint. That is why Maintenance and Working Evidence are not scored 5/5.

## Runtime / platform

- Windows x64
- macOS ARM64
- Linux x64
- Java/Maven source build with GraalVM native-image packaging
- Text-only search can run on modest hardware; upstream recommends substantially more RAM for multimedia model workloads.
- GPU is optional according to upstream; local models can run on CPU, with acceleration improving heavier extraction/model stages.
- Initial model/tool acquisition requires network access unless assets are prepared for an air-gapped import.

## License and provenance

Root source license: **MIT**, copyright 2026 AwesomeDog.

Soma also invokes or bundles/integrates third-party software and model assets including sqlite-vec, FFmpeg/Jellyfin FFmpeg, Pandoc, llama.cpp/llamafile-related tooling, Whisper-family assets, embedding/reranking models, and vision models. Those dependencies/assets retain their own licenses and provenance requirements. Do not assume the repository's MIT license relicenses downloaded models or external executables.

No upstream implementation code was copied into GitHub Gold during this pass.

## Verification boundary

GitHub Gold inspected repository metadata, README architecture/documentation, root licensing, release metadata/assets, the test-tree presence, release workflow, and recent commit history.

GitHub Gold **did not**:

- build Soma;
- run `tests/e2e_tests.py`;
- execute released binaries;
- download or inspect model weights;
- verify the claimed offline/network behavior with packet capture;
- index a real corpus;
- test OCR, vision, transcription, HyDE, ranking quality, CJK behavior, or HTTP API compatibility;
- reproduce performance/resource claims;
- independently audit the parser/model supply chain or security posture.

Accordingly, VERIFIED here means there is concrete repository-native evidence of a maintained, packaged implementation and release process, not independent functional certification by GitHub Gold.

## Caveats

1. The project is young (created July 2026) and has little visible adoption history.
2. The release workflow explicitly skips tests during native packaging; smoke execution is narrower evidence than a green E2E matrix.
3. Multimedia indexing can be resource-heavy and depends on a substantial external model/tool chain.
4. "100% offline" is an upstream architectural claim. The documented air-gap workflow is promising, but GitHub Gold has not independently captured network traffic.
5. Model licenses and external-tool licenses must be audited separately for redistribution or product embedding.

## Strong recursive leads

- Inspect `tests/e2e_tests.py` by capability and map exactly what is asserted versus mocked/skipped.
- Trace the BM25/vector/HyDE/RRF/reranking implementation boundaries and failure fallback behavior.
- Inspect CJK tokenizer/indexing implementation for reusable low-resource lexical-search patterns.
- Audit air-gap export/import and dependency integrity/provenance.
- Compare Soma's architecture against QMD, Lexa, Reflex, and other local retrieval engines without creating duplicate catalog entries.
