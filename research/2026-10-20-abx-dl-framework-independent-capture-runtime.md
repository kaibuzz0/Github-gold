# abx-dl — framework-independent capture runtime (2026-10-20)

**Upstream:** https://github.com/ArchiveBox/abx-dl  
**Owner:** ArchiveBox / Nick Sweeting  
**Discovery:** GitHub-first recursive lead from the already-cataloged ArchiveBox project.  
**Evidence:** VERIFIED (upstream implementation, release and CI; no independent local execution)  
**Gold score:** S / 28 — Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 5; Maintenance 4.  
**License:** MIT (root LICENSE, Copyright 2024 Nick Sweeting). No upstream source copied.

## What is useful
A standalone Python CLI and embeddable capture runtime that coordinates URL extraction plugins without requiring ArchiveBox's Django database or web application. It emits typed crawl, snapshot, process and archive-result events and writes ordinary capture files plus an `index.jsonl` output ledger.

Specific inspected modules:
- [`abx_dl/catalog.py`](https://github.com/ArchiveBox/abx-dl/blob/main/abx_dl/catalog.py): `PluginCatalog` discovers manifests/executable hooks and resolves transitive plugin dependencies; `PluginConfigResolver` handles configuration.
- [`abx_dl/orchestrator.py`](https://github.com/ArchiveBox/abx-dl/blob/main/abx_dl/orchestrator.py): `download()`, `parse_input()`, `create_bus()`; separates installation, crawl setup, snapshot execution and cleanup. `parse_input` processes pasted text/bookmark/feed imports through opted-in hooks.
- [`abx_dl/execution.py`](https://github.com/ArchiveBox/abx-dl/blob/main/abx_dl/execution.py): `execute_hook()`, `iter_plugin_command()`, timeouts, subprocess stdout streaming and process-group cleanup.
- [`abx_dl/events.py`](https://github.com/ArchiveBox/abx-dl/blob/main/abx_dl/events.py): typed event contracts and lifecycle ordering.
- [`abx_dl/services/`](https://github.com/ArchiveBox/abx-dl/tree/main/abx_dl/services): process, binary, crawl, snapshot, tag and result services.
- [`abx_dl/output_files.py`](https://github.com/ArchiveBox/abx-dl/blob/main/abx_dl/output_files.py): `OutputManifest` with file metadata, MIME classification and output scanning.
- [`tests/`](https://github.com/ArchiveBox/abx-dl/tree/main/tests): executor, installation, output, permission, CLI, packaging and process lifecycle tests.

## Reproducibility and maintenance evidence
- [`pyproject.toml`](https://github.com/ArchiveBox/abx-dl/blob/main/pyproject.toml) declares version **1.13.242**, Python **>=3.12,<3.15**, beta classification, and pinned direct dependencies `abxbus==2.5.77`, `abxpkg==1.13.58`, `abx-plugins==1.13.474`. `uv.lock` exists.
- [v1.13.242](https://github.com/ArchiveBox/abx-dl/releases/tag/v1.13.242) published **2026-10-20 15:34:37 UTC** as a non-prerelease. Its release notes link to a changelog comparison rather than asserting new functionality.
- [CI run 39448373304](https://github.com/ArchiveBox/abx-dl/actions/runs/39448373304) completed successfully for [commit `367d06dc`](https://github.com/ArchiveBox/abx-dl/commit/367d06dc3e4f67f6a7e9c42b0b909dce36da1291) on 2026-10-20. Its 19 returned jobs were **18 success / 1 skipped**; successful jobs include Python tests, all-plugins integration and amd64/arm64 Docker build-and-test. The skipped scheduled-input job was not counted as success.
- CI tests use `uv sync --locked`, pytest and a test matrix covering supported Python versions; this is upstream CI evidence, not locally reproduced.
- `README.md` contains CLI examples and output assertions, including wget/title and browser-dependent screenshot/PDF/readability paths. Their presence is not proof that each example was independently run here.

## Runtime / deployment
`uvx abx-dl 'https://example.com'`, `uv tool install abx-dl`, or upstream Docker images. CLI supports `--plugins=...`, `--output=...`, `--dir=...`, `--timeout=...`, and `--no-install`. Plugins can require browsers, wget, yt-dlp and other system tools. Docker CI builds Linux amd64 and arm64; do not assume Android/Termux support without verification.

## Risks, limits and licensing
- By default, plugins may install missing binaries. Treat automatic installers and plugin hook subprocesses as an execution/supply-chain boundary. Use `--no-install` when controlling dependencies is important.
- Crawling untrusted URLs can download active or hostile content; isolate capture workers and browser profiles. Authenticated browser personas may expose cookies or tokens.
- Root MIT license does **not** cover all plugin implementations, external executables or captured third-party content. The companion [abx-plugins](https://github.com/ArchiveBox/abx-plugins), [abxpkg](https://github.com/ArchiveBox/abxpkg), and [abxbus](https://github.com/ArchiveBox/abxbus) currently each expose a separate MIT root LICENSE, but per-file and transitive licenses require review.
- Rapid patch releases may indicate healthy maintenance but also interface churn. Pin a tested version for downstream reuse.
- No local build, install, crawl, Docker run, plugin execution, fuzzing or security audit was performed.

## Recursive leads for next run
1. `ArchiveBox/abx-plugins`: inspect real hook implementations, binary requirements and per-plugin licenses; catalog high-value individual extractors only after code-level evidence.
2. `ArchiveBox/abxpkg`: inspect provider selection, binary provenance, caching and isolation.
3. `ArchiveBox/abxbus`: inspect event deadline/cancellation semantics and typed event composition.
4. Independently test a pinned abx-dl release with local fixtures and network isolation; evaluate malicious URL/redirect and plugin manifest edge cases.

## YouTube seed status
All six playlist URLs from `sources/youtube_playlists.md` were attempted through web access on 2026-10-20. The first three returned fetch throttling; the remaining three returned disabled access. Search results did not identify attributable video/transcript content. No transcript-derived claim was made; research continued GitHub-first.

## Repository integration
Proposed synchronized promotion of this standalone repository to `MASTER_LIST.md` and `catalog/tools.json`, preserving ArchiveBox as a distinct canonical entry. The research branch is the existing draft PR #7. Do not merge automatically.
