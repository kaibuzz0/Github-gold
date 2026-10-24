# GitHub Gold — NVDA and libzim promotion evidence
**Checked:** 2026-10-23 (America/Chicago)  
**Method:** GitHub-first, existing September research dossiers plus fresh upstream repository-native inspection.  
**Independent execution:** None; no third-party implementation code copied.

## NVDA — VERIFIED (upstream), S / 28
- **Repository:** https://github.com/nvaccess/nvda
- **Scope:** Windows screen reader; UIA/MSAA/Java accessibility integrations, accessible-object modeling, speech, braille, browser navigation, add-ons and remote client.
- **Specific source:** `source/UIAHandler/`, `source/IAccessibleHandler/`, `source/NVDAObjects/`, `source/speech/`, `source/braille/`, `source/brailleDisplayDrivers/`, `source/_remoteClient/`, `source/addonHandler/`, `tests/system/`.
- **Requirements:** `pyproject.toml` requires Python >=3.13,<3.14 for source builds; Windows-specific build and native dependencies. Official installer is separate from a source build.
- **Licensing:** `copying.txt` explicitly declares GPL-2.0-or-later with two project-specific exceptions and separately licensed components. Root GitHub metadata reports NOASSERTION; do not substitute it for the authoritative license file.
- **Stable release:** `release-2026.2` published 2026-08-31: https://github.com/nvaccess/nvda/releases/tag/release-2026.2
- **Maintenance:** master commit `40e2df64cd` dated 2026-10-21 adjusts running-copy detection. More recent PR activity does not equal a merged master change.
- **Upstream execution evidence:** https://github.com/nvaccess/nvda/actions/runs/39544741209 — master push CI on 2026-10-21: 41 jobs, 37 successful, 4 skipped. Includes x64 build, unit tests, Windows installer/startup tests, Chrome accessibility system tests, type analysis and dependency-license checks. A separate PR workflow https://github.com/nvaccess/nvda/actions/runs/39951086469 failed 2026-10-23; it is not the master run.
- **Scoring:** Utility 5 + Working Evidence 5 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5 = **28**. Working Evidence 5 is based on upstream execution of packaged app and system integration, **not** our own test.
- **Caveats:** Add-on loading and remote client trust boundaries, Windows API variability, driver/device-specific accessibility. Reuse requires GPL-exception and bundled-license review.
- **Prior dossier:** `research/2026-09-12-nvda-windows-screen-reader-accessibility-platform.md`.
- **Next:** Inspect remote client authentication, add-on signing/update trust, braille BLE reconnection, accessibility-event coalescing and reproducible Windows installer tests.

## libzim — VERIFIED (upstream), S / 28
- **Repository:** https://github.com/openzim/libzim
- **Scope:** C++ ZIM archive reader/writer and optional Xapian-backed search/suggestions. Complements the already canonical `openzim/zim-tools` CLI entry; it is a distinct reusable library.
- **Specific source:** `include/zim/archive.h`, `entry.h`, `item.h`, `blob.h`, `search.h`, `suggestion.h`, `writer/`; test fixtures and external `openzim/zim-testing-suite`.
- **Requirements:** `meson.build` declares C++17, liblzma, ICU, Zstd; Xapian optional. Cross-compiled Android/iOS/WASM configurations can disable writer/search and may not run target tests.
- **Licensing:** README states GPL-2.0-or-later and root COPYING contains GPLv2; `meson.build` declares GPL2. Reuse is copyleft-constrained; dependencies require separate checks.
- **Stable release:** 9.8.2 published 2026-08-13: https://github.com/openzim/libzim/releases/tag/9.8.2
- **Maintenance:** 2026-10-19 merge `ad888b4cdc` fixes off-by-one in random entry selection: https://github.com/openzim/libzim/commit/ad888b4cdc
- **Upstream execution evidence:** https://github.com/openzim/libzim/actions/runs/39279529888 — main push CI on 2026-10-19: **23/23 jobs successful** across Linux, macOS, Windows, Android, iOS and WASM build configurations. Some are cross-compilation only, not native execution on all platforms.
- **Scoring:** Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 5 = **28**. Based on upstream CI and mature test infrastructure, not independent archive operations.
- **Caveats:** Optional Xapian changes APIs; some tests require up to 16 GiB RAM; untrusted compressed archives need malformed-input and decompression-limit review; GPL obligations constrain embedding.
- **Prior dossier:** `research/2026-09-13-libzim-zim-offline-archive-library.md`.
- **Next:** Examine ZIM writer/reader round trips, malformed-cluster handling, memory ceilings, checksum behavior, optional-Xapian API differences and openzim/zim-testing-suite coverage.

## Deduplication, provenance and limits
- Checked the 64-entry canonical `catalog/tools.json` and empty `catalog/candidate_queue.json`; neither upstream URL was present. NVDA adds accessibility coverage; libzim adds library-level archival APIs distinct from ZIM Tools.
- Both promoted to canonical master list and structured catalog together. No unrelated entries were removed or rewritten.
- Six playlist seeds remain recorded in `sources/youtube_playlists.md`. No video/transcript evidence was accessible or used in this batch; both discoveries are GitHub-first.
- No independent Windows app install, unit test, screen-reader interaction, braille test, archive creation/parsing, fuzzing, security audit or benchmarking was performed. No upstream code copied.
