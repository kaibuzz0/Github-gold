# GitHub Gold research — Joplin, KiCad, Open MCT (2026-10-26 CDT)

## Provenance
GitHub-first inspection of upstream README, licensing, source trees, test structure, releases and CI. Two seed YouTube playlist pages were attempted and throttled; no transcript findings attributed. No third-party implementation code copied.

## Joplin — VERIFIED (upstream), S/27
Repo: https://github.com/laurent22/joplin
Stable v3.7.21 released 2026-09-25.
Reusable code: `packages/lib/services/synchronizer/` (conflicts/E2EE/revisions tests), `packages/lib/services/e2ee/EncryptionService.ts`, `crypto.ts`, `packages/lib/services/interop/` (ENEX, Markdown, Obsidian, OneNote, JEX), `packages/lib/services/search/SearchEngine.ts`, `packages/app-cli/`, `packages/app-mobile/`.
Upstream CI: https://github.com/laurent22/joplin/actions/runs/40406257789 passed 7/7 jobs 2026-10-26 21:39 UTC. UI https://github.com/laurent22/joplin/actions/runs/40423856061 passed 3/3 and Android APK https://github.com/laurent22/joplin/actions/runs/40423856058 passed 2026-10-27 UTC. Newer CI https://github.com/laurent22/joplin/actions/runs/40423856055 failed macOS Intel, 4 other jobs passed, 2 cancelled. Job 121924626656 logs show `packages/utils/ipc.test.ts:67` expected pong but received `[]`; 10 other utils suites passed. Cause unknown.
License: root AGPL-3.0-or-later except per-directory overrides. `packages/server/LICENSE.md` is Joplin Server Personal Use License, not default AGPL. Logos/icons reserved. Review exact directory before reuse.
No local installation, E2EE audit, note sync or Android execution. Follow IPC test reliability, plugin trust, sync conflicts and optional MCP/API exposure.

## KiCad Source Mirror — PROMISING, A/25
Mirror: https://github.com/KiCad/kicad-source-mirror
Canonical development: https://gitlab.com/kicad/code/kicad
Official 10.0.7 release announcement 2026-10-07: https://www.kicad.org/blog/2026/10/KiCad-10.0.7-Release/ ; GitHub release artifacts 2026-10-16. 10.0.8 RC1 announced 2026-10-22.
Reusable code inspected: `eeschema/connection_graph.cpp`, `eeschema/erc/`, `pcbnew/board.cpp`, `pcbnew/board_loader.cpp`, `pcbnew/autorouter/` footprint placement, `api/proto/board/`, `api/proto/schematic/`, `qa/tests/pcbnew/`, `qa/tests/eeschema/`, `gerbview/`.
`.gitlab-ci.yml` defines build/test stages for Linux, Windows and macOS, but no passing GitLab application test run inspected. GitHub mirror Actions are dependency/redirect workflows, not KiCad application build/test evidence.
`LICENSE.README`: majority GPL-3.0-or-later; separate MIT/BSD/Apache/Boost/ISC components. No code copied. Follow GitLab CI, untrusted archive/file-format parser safety, Gerber/DRC correctness and LibrePCB/FreeCAD ecosystem.

## Open MCT maintenance — PROMISING A/25 unchanged
2026-10-27 UTC https://github.com/nasa/openmct/actions/runs/40427389616 e2e-full failed at Ubuntu npm ci; Windows cancelled. https://github.com/nasa/openmct/actions/runs/40424992380 e2e-perf also failed at npm ci. Prior 2026-10-26 job logs confirmed Node 18.20.8 vs package requirement >=24.14.1 caused EBADENGINE; exact new-run log root cause not rechecked. No Playwright e2e success; no promotion. Next: update CI runtime and rerun e2e.

## Verification boundary
All checks are upstream code/release/workflow inspection. No independent builds, runtime tests, security audits, firmware/hardware tests or cryptographic validation.
