# Wisp Science — local-first AI research workbench

- Upstream: https://github.com/xuzhougeng/wisp-science
- Author: Zhou-Geng Xu / xuzhougeng
- Category: scientific computing / AI agents / reproducible research / local-first desktop
- Evidence: **VERIFIED** (repository-native evidence; not independently executed in this pass)
- Provisional Gold score: **29/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 5/5
  - Documentation 5/5
  - Maintenance 4/5
- License: **AGPL-3.0-only** at repository root; directories may declare exceptions. Review per-component licensing before extraction or reuse.

## Why it matters

Wisp Science is a local-first desktop research workbench that combines persistent Python/R scientific runtimes, literature/database access, agentic file/shell work, reusable skills, remote compute, reproducibility/provenance mechanisms, and project transfer/sync. It is unusually valuable as an architecture reference because it treats scientific work as a durable project with inspectable runs and evidence rather than only a chat transcript.

## Capabilities supported by upstream repository evidence

The README documents:

- persistent Python and R kernels with conversation-level isolation;
- local, WSL and SSH compute hosts, hardware probing and long-running jobs with live logs;
- model support through OpenAI-compatible/Anthropic providers and ACP-driven coding agents;
- bundled MCP access to PubMed, GEO and roughly 80 scientific databases;
- offline previews for notebooks, PDFs, Office documents and images;
- isolated exploration branches;
- a Publication Workspace that freezes manuscript revisions into verifiable Evidence Capsules;
- saved sessions, turn-level file-edit undo, reusable `SKILL.md` skills, project attachments and encrypted manual project sync/transfer;
- Windows, macOS and Linux desktop packaging.

These are upstream capability claims unless tied below to code/CI evidence; they were not independently exercised by Github-gold in this pass.

## Strong working evidence

The repository has a substantial GitHub Actions test workflow rather than release artifacts alone. Current CI includes:

- `cargo test --workspace` under both stable Rust and the declared Rust 1.90.0 toolchain;
- wasm UI `cargo check`;
- Playwright browser E2E tests;
- deterministic headless-agent evaluation on Ubuntu, macOS and Windows;
- Python worker and skill-helper tests on all three operating systems;
- MCP process-tree shutdown regression tests;
- project-storage startup/migration regressions;
- runtime-worker process-tree regressions;
- repeated Windows native-input reentrancy smoke tests;
- repeated macOS redraw/save-panel nested-loop regression tests.

This is particularly useful evidence because several tests exercise OS process lifecycle and native GUI/event-loop behavior that mocks alone would not establish.

The repository also maintains separate release/build workflows for Windows, macOS and Linux.

## Release / maintenance evidence

Stable **v1.15.0** was published **2026-09-26**. GitHub release metadata contains multiple platform artifacts and SHA-256 digests, including Linux aarch64/amd64 packages and macOS artifacts. The release is recent relative to this dossier and the project has an active test/release pipeline.

The repository README also links a Zenodo DOI for the software, adding a useful scientific citation/provenance surface.

## Reusable components / architecture leads

High-value pieces to inspect recursively:

1. **Headless agent evaluation harness** — deterministic evaluation with saved artifacts across three operating systems.
2. **Runtime process-tree ownership** — Python/R/other interpreter workers must terminate descendant processes reliably across Windows/macOS/Linux.
3. **Project-local storage and migration** — durable scientific project state with startup/migration regression coverage.
4. **Evidence Capsules / Publication Workspace** — provenance-oriented manuscript revision freezing.
5. **Exploration branches** — isolate speculative research changes from project mainline.
6. **MCP scientific database layer** — broad database access without stuffing every integration into the core agent context.
7. **Remote compute abstraction** — local/WSL/SSH execution with persistent scientific kernels and job logs.
8. **Encrypted manual sync/project transfer** — local-first collaboration/portability model that intentionally avoids opaque background synchronization.
9. **Skills and ACP delegation** — reusable instruction/tool bundles and external agent delegation.
10. **Native event-loop regression fixtures** — focused Windows/macOS tests for subtle reentrancy/process integration failures.

## Requirements / platforms

Upstream distributes Windows, macOS and Linux desktop packages. Building from source uses a Rust/Tauri workspace plus UI tooling; scientific execution can require Python/R and optional remote runtimes. Specific databases, model providers, SSH hosts and MCP services introduce their own credentials/runtime requirements.

## Caveats and risks

- Root license is strong copyleft **AGPL-3.0-only**. Do not copy implementation code into Github-gold without a deliberate compatibility/attribution review. Directory-level exceptions must be checked individually.
- Local-first does not mean every optional operation is offline: model APIs, literature/database queries, remote SSH compute and downloads can involve external services.
- Scientific correctness is distinct from software test coverage. Passing infrastructure tests does not establish correctness of an LLM-generated analysis, statistical method, database result or manuscript conclusion.
- External models, scientific databases, packages and services retain independent licenses/terms.
- Release signatures/digests were observed in upstream metadata but were not locally verified.

## Verification boundary

Github-gold inspected upstream README, root license, release metadata and CI workflow. It did **not** build or install Wisp Science, execute its tests, run Python/R analyses, connect an MCP database, connect an LLM or ACP agent, use SSH/WSL/GPU compute, reproduce an Evidence Capsule, test encrypted transfer/sync, or independently validate scientific results.

Therefore VERIFIED means the repository contains strong concrete implementation/release/test evidence for the relevant software surfaces; it is not a claim of independent execution or scientific validation by Github-gold.

## Discovery provenance

Independent GitHub-first discovery during breadth rotation into local-first scientific computing. YouTube transcripts were not required for this candidate and no transcript-derived technical claim is used here.

## Next research

- Inspect the Evidence Capsule data model and tamper/provenance semantics.
- Trace project storage migrations and backup/recovery behavior.
- Inspect the headless evaluation fixture design and determine which agent behaviors are deterministic versus provider-dependent.
- Map MCP scientific connectors and identify which are bundled, local, network-backed or credential-dependent.
- Audit encrypted project transfer/sync threat model and key lifecycle.
- Inspect remote runtime isolation, cancellation and artifact collection across SSH/WSL.
