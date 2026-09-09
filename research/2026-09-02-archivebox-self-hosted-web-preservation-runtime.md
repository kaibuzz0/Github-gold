# ArchiveBox: self-hosted web preservation and modular capture runtime

- **Repository:** https://github.com/ArchiveBox/ArchiveBox
- **Author / Org:** ArchiveBox / Nick Sweeting / contributors
- **Category:** web archiving / digital preservation / self-hosting / capture orchestration / archival automation
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28/30 (S)
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **License:** MIT
- **Discovery:** GitHub-first broad-category discovery; no YouTube transcript claim used

## What it is

ArchiveBox is a self-hosted web-preservation system designed to turn URLs into durable collections of ordinary files and metadata rather than a proprietary archive format. Upstream documents output across HTML, PNG, PDF, TXT, JSON, WARC, SQLite, media files, screenshots, extracted article text, source-code clones, and other formats depending on the capture path.

The project can be used through a CLI, web application, Python interfaces, REST/API surfaces, webhooks, a browser extension, and the underlying filesystem/SQLite collection. The important GitHub Gold finding is not merely that ArchiveBox can save webpages; it coordinates a large set of specialist capture tools while keeping the resulting archive readable with ordinary software.

## Why it qualifies as GitHub Gold

ArchiveBox combines several unusually useful properties:

- local ownership of archived data;
- multiple redundant capture representations instead of one fragile format;
- use of established external tools such as Chromium, wget, yt-dlp, SingleFile, git, and related extractors;
- ordinary filesystem and SQLite storage;
- scheduled and repeated collection;
- browser, CLI, API, and self-hosted UI entry points;
- preservation of source material in formats intended to remain independently readable;
- a current architectural move toward a framework-independent capture runtime and split plugin ecosystem.

The repository is therefore valuable both as deployable preservation infrastructure and as a reference for building a capture pipeline that orchestrates heterogeneous tools without forcing all captured material into one application-specific binary format.

## Durable-data design

Upstream's README explicitly emphasizes standard output formats and ordinary files/folders. It documents captures including:

- original page HTML/CSS/JS;
- self-contained SingleFile HTML;
- screenshots;
- PDF;
- WARC;
- title, headers, favicon, and article text;
- media, subtitles, metadata, and thumbnails;
- Git repository clones and associated project material;
- SQLite and JSON metadata.

This is a strong preservation characteristic because application failure does not automatically make the stored evidence unreadable. The archive can still be inspected with generic filesystem, browser, media, SQLite, JSON, WARC, and document tooling.

## Capture orchestration and tool composition

ArchiveBox does not attempt to reinvent every downloader internally. The project composes mature specialist tools for different content classes and capture strategies. That pattern is highly reusable: one orchestration layer can preserve the same target through multiple independent methods so a failure in one representation does not eliminate the whole snapshot.

The current v0.9 development architecture makes this separation even more explicit. Upstream's release-candidate notes state that extractor plugins are moving into a separate `abx-plugins` ecosystem and capture execution is moving through the standalone `ArchiveBox/abx-dl` runtime.

That split is significant for GitHub Gold because it reduces the value lock-in to the main Django application. The downloader/runtime and plugin model can become reusable independently of the full archival UI/database application.

## `abx-dl` recursive lead

The companion `ArchiveBox/abx-dl` repository was inspected enough to confirm that it is a real, separate framework-independent capture runtime rather than only a placeholder referenced by ArchiveBox documentation.

Its current README describes an all-in-one URL downloader that composes the shared ArchiveBox plugin library and exposes framework-independent interfaces including:

- `PluginCatalog` for plugin inventory;
- `PluginConfigResolver` for resolved configuration;
- typed event dispatch;
- `execute_hook()` for finite plugin-hook execution;
- `OutputManifest` for output metadata;
- `parse_input()` for pasted text and bookmark/feed-style import material;
- explicit crawl and lifecycle listener composition.

Its documented plugin execution phases separate dependency installation/resolution, crawl-scoped setup, and per-snapshot extraction. The README also contains executable/documented examples that assert expected output files for wget/title and richer screenshot/PDF/readability captures.

`abx-dl` deserves a dedicated future dossier rather than being silently folded into ArchiveBox's score.

## Current application/component structure

The current ArchiveBox `dev` tree exposes distinct application surfaces including:

- `archivebox/api`;
- `archivebox/cli`;
- `archivebox/config`;
- `archivebox/core`;
- `archivebox/crawls`;
- `archivebox/machine`;
- `archivebox/personas`;
- `archivebox/mcp`;
- web/admin and persistence-oriented modules;
- migration and service/orchestration code.

Recent development work also makes the orchestration boundary explicit: ArchiveBox owns crawl-to-snapshot lifecycle and database/application state while `abx-dl` increasingly owns snapshot-to-ArchiveResult execution.

That separation is architecturally useful because lifecycle, persistence, capture execution, and plugin/tool installation can evolve independently.

## Event-driven / append-only execution direction

The v0.9 release-candidate notes describe replacement of the older `pluggy`-style in-process architecture with an event-driven flow using append-only structured JSONL records for Crawls, Processes, Snapshots, and ArchiveResults.

Upstream states the motivation as cleaner resumability and auditability plus future support for browser-extension capture, distributed workers, and peer-to-peer synchronization.

This is promising design evidence, but it remains part of the active release-candidate line rather than the current stable v0.7.x line. GitHub Gold therefore treats the architecture as verified current source/upstream direction, not as stable-production certification.

## Snapshot replay and browser isolation

The current release-candidate architecture includes work to isolate snapshot replay and browser state more carefully. Upstream describes crawl-scoped browser sessions, cloned-profile cleanup after a crawl, and subdomain-oriented serving for public, admin/API, and isolated snapshot hosts.

This matters because archived pages can contain active or hostile HTML/JavaScript. A web archive that replays captured content inside the same trust origin as administrative controls creates a materially different risk than a static file store.

The isolation work is therefore a major positive architectural signal, but it should not be interpreted as a complete browser-security audit.

## CI and working evidence

The current repository contains dedicated GitHub Actions workflows for:

- CI orchestration;
- parallel test discovery/execution;
- ordinary tests;
- linting;
- CodeQL;
- Docker/image workflows;
- Python package workflows;
- documentation;
- release candidates;
- releases;
- public-site deployment;
- repository automation.

The parallel test workflow is particularly strong evidence. It programmatically discovers tests, validates that discovered test paths are unique, resolves optional build dependencies, installs from the locked environment, creates isolated test directories/personas, and runs pytest across the generated matrix.

The inspected workflow pins important Actions to immutable commit SHAs, including checkout, setup-python, and setup-uv, rather than relying only on mutable major tags. That is a positive supply-chain signal.

A recent upstream orchestration commit also records specific upstream verification totals for several focused suites and a real `https://sweeting.me` capture. Those numbers are upstream-reported verification attached to the commit; GitHub Gold did not reproduce them and does not present them as local testing.

## Release and maintenance state

The release situation needs to be preserved accurately.

The latest stable GitHub release inspected is **v0.7.4**, published **May 18, 2026**. That stable release primarily refreshed bundled/container dependencies including Chromium/Playwright, Node, gosu, yt-dlp, SingleFile, and other runtime packages.

The same day, upstream published **v0.9.31-rc** as a pre-release and explicitly warned that v0.9.x is a major architectural upgrade, that stable remains v0.7.4, and that testers should use backups before trying the release-candidate line.

Current development is substantially ahead of that RC tag. The `dev` branch showed commits through **September 3, 2026 UTC**, including a version bump to `0.9.35rc411`, snapshot-backfill orchestration fixes, new `abx-dl` integration, and ongoing maintenance of snapshot scheduling and migrations.

This is extremely active maintenance, but the 4/5 Maintenance score is intentional: the project is in the middle of a large architecture transition where the active development branch and current stable line differ significantly.

## License and reuse boundary

The root repository license is **MIT** with a 2026 Nick Sweeting copyright notice. No ArchiveBox or companion-project source code was copied into GitHub Gold during this pass.

Future reuse of individual plugins or external capture tools must still inspect those upstream projects' own licenses. ArchiveBox being MIT does not relicense Chromium, wget, yt-dlp, SingleFile, gallery-dl, or other external dependencies and plugins.

## Operational and security caveats

### Stable and development architectures differ

The current stable line is v0.7.4 while active `dev` work is deep into the v0.9 release-candidate architecture. Do not assume documentation or behavior from `dev` applies unchanged to a stable deployment.

### Web capture is an untrusted-content boundary

Archive targets can contain malicious HTML, JavaScript, redirects, downloads, media, or intentionally pathological content. Running browser and downloader processes against arbitrary URLs should be treated as processing untrusted input.

### Snapshot replay is a security-sensitive surface

Serving archived active content near administrative interfaces creates origin, cookie, script, and browser-isolation concerns. Upstream's current isolated snapshot-host direction is important, but GitHub Gold did not independently validate the full replay threat model.

### Authenticated-browser capture can expose sensitive state

ArchiveBox supports advanced workflows involving login/session/browser profiles. Any copied browser profile or authenticated capture environment can contain cookies, tokens, history, or other sensitive material and deserves separate storage and access controls.

### External tools expand the dependency and attack surface

A capture may invoke browsers, media downloaders, network clients, git, parsing libraries, and other executables. Security and reproducibility therefore depend partly on the versions and behavior of those external tools, not only ArchiveBox's Python source.

### Default Archive.org submission may be inappropriate for private evidence

Upstream documents optional submission to archive.org for redundancy and says it can be disabled for local-only/stealth use. Operators preserving private, legal, authenticated, confidential, or otherwise non-public material should understand this behavior before ingestion rather than assuming every capture remains local.

### Large archives require migration discipline

The v0.9 development line contains substantial data-layout and migration work. Upstream itself recommends backups when testing release candidates. Large evidence or research collections should therefore treat migrations, rollback, filesystem layout, database backup, and restoration as first-class operational concerns.

## Verification performed by GitHub Gold

This pass inspected:

- current ArchiveBox README on the active `dev` branch;
- root MIT license;
- current source/module tree;
- GitHub Actions workflow inventory;
- the parallel pytest workflow and its pinned Action references;
- latest stable and release-candidate GitHub release metadata;
- current commit history through September 3, 2026 UTC;
- upstream-reported verification attached to recent orchestration work;
- enough of the companion `ArchiveBox/abx-dl` README to confirm its independent runtime/plugin interfaces and make it a recursive lead;
- the existing GitHub Gold catalog/search surface to avoid adding a duplicate ArchiveBox dossier.

## Not verified locally

GitHub Gold did **not**:

- install or build ArchiveBox;
- run its pytest/CI suites;
- build Docker images;
- initialize or migrate a collection;
- capture a live webpage;
- invoke Chrome, wget, yt-dlp, SingleFile, git, gallery-dl, or other extractors;
- test authenticated-browser/profile capture;
- test WARC validity or replay compatibility;
- exercise the REST API, webhooks, browser extension, MCP surface, or scheduler;
- reproduce the upstream `sweeting.me` capture;
- test snapshot-origin isolation or hostile archived JavaScript;
- verify archive.org submission behavior;
- benchmark storage, indexing, crawl throughput, or large-collection migrations;
- independently audit the security model;
- verify external-tool or plugin licenses beyond the root ArchiveBox license.

Claims here are source/document/release/workflow/upstream-evidence claims, not local operational certification.

## Strong recursive leads

1. **`ArchiveBox/abx-dl`** — standalone framework-independent capture runtime, event model, hook execution, output manifests, and input parsing.
2. **`ArchiveBox/abx-plugins`** — plugin metadata, extractor hooks, per-plugin dependencies, and licensing boundaries.
3. **Append-only JSONL event model** — resumability, replay/auditability, crash recovery, and future distributed-worker behavior.
4. **Snapshot isolation/replay architecture** — origin separation, CSP/sandboxing, active-content handling, and authenticated archive safety.
5. **Browser persona/profile handling** — safe reuse of authenticated sessions and cleanup of cloned profiles.
6. **Migration engine** — keyset batching, `fs_version`, resumable upgrades, and preservation of legacy ArchiveResult/filesystem data.
7. **WARC pipeline** — standards compliance, metadata completeness, interoperability with independent replay/readers, and deduplication opportunities.
8. **Browser extension** — realtime capture/import path and whether it preserves more client-side state than server-side crawling.
9. **Sonic/search integration** — indexing architecture for large personal archives and the extent to which indexing can be swapped or rebuilt.
10. **Storage backends** — operational behavior on local disks, NFS/SMB, and object/cloud-backed filesystems.

## Promotion recommendation

**VERIFIED / S / provisional 28.**

Promote atomically into the synchronized catalog surfaces when the current draft research batch enters its promotion phase. ArchiveBox is strong Gold for durable local-first preservation and multi-tool capture orchestration. The score stays below 29/30 because the project is presently undergoing a large stable-to-v0.9 architecture transition; the active branch is exceptionally current, but the production-stable and development architectures should not be conflated.