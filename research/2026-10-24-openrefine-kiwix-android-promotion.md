# OpenRefine and Kiwix Android — source evidence and promotion (2026-10-24)

## Repository hygiene and provenance
- Continued draft PR #7 on `agent/research-ladybird-browser-engine` from head `7040e2d77b7d627f9155ef0d937ef67033dd5739`; no parallel branch.
- Pre-change: 70 canonical entries, 70 master headings, no queued candidates. Checked both repository URLs and names for duplicates. No third-party implementation source copied.
- Category rotation: local-first data curation and Android offline-knowledge distribution. Kiwix Android was followed recursively from existing libzim/ZIM Tools entries; added reciprocal libzim catalog/master reference.
- Three playlist identifiers (`PLMI6SBmd587c`, `PLfidXW0BixTc`, `PLI99ObbYUvDn_0tkbXsOYB4ApTyHFQxSi`) searched by exact ID on 2026-10-24; search returned no usable playlist or transcript material. Other seeds remain recorded in `sources/youtube_playlists.md`. Neither project is attributed to YouTube.

## OpenRefine — VERIFIED (upstream), S / 28
- URL: https://github.com/OpenRefine/OpenRefine
- Purpose: Java-based local data-cleaning, reconciliation, clustering and transformation workbench with browser interface.
- Root `LICENSE.txt` and Maven `pom.xml` identify BSD-3-Clause. README explicitly directs reviewers to per-extension and bundled third-party license folders. Do not copy without required notices.
- Source inspected 2026-10-24: `modules/grel/src/main/java/com/google/refine/grel/Parser.java` (GREL parser and expression AST); `main/src/com/google/refine/importers/` (CSV/JSON/XML/RDF/Excel etc.); `main/src/com/google/refine/clustering/`; `extensions/wikibase/`; `server/src/com/google/refine/ValidateHostHandler.java` (Host header checks against DNS rebinding); `main/tests/cypress/`.
- Stable 3.10.1 published 2026-03-04. Latest inspected master commits dated 2026-10-23 fix path-prefixed command URLs and macOS code signing.
- Upstream snapshot CI 2026-10-23: https://github.com/OpenRefine/OpenRefine/actions/runs/40010351064 — **12 successful jobs**: matrix preparation, seven Cypress E2E groups, unit tests, Windows installer, and two macOS package jobs. Workflow source at `.github/workflows/pull_request_e2e.yml` shows Java 21, Node, Maven, PostgreSQL/MySQL test services.
- Build inconsistency: README claims JDK 11+ source support, while current root `pom.xml` declares `java.minversion=21`; CI uses Java 21. Do not assert JDK 11 works on current master.
- Score: utility 5 + working 5 + reuse 5 + novelty 4 + documentation 5 + maintenance 4 = **28**. The CI result is upstream evidence, not a local test.
- No independent build, browser deployment, data import, reconciliation, benchmark or security audit. Local host validation is not a proof of security; extensions may execute third-party code.
- Next: confirm release-tag toolchain, test malformed input/reconciliation failure cases, inspect extension permissions and host validation tests.

## Kiwix Android — VERIFIED (upstream), S / 27
- URL: https://github.com/kiwix/kiwix-android
- Purpose: offline Android ZIM archive reader, content library manager, local HTTP sharing and Wi-Fi Direct transfers.
- Root `COPYING` and Kotlin source headers: GPL-3.0-or-later; ZIM archive content, images, native libraries and branding may have independent terms. Do not copy source or assets.
- Inspected source: `app/src/main/java/org/kiwix/kiwixmobile/webserver/KiwixServer.kt` wraps `java-libkiwix` `Library`/`Server` and `libzim` `Archive`; `app/src/main/java/org/kiwix/kiwixmobile/localFileTransfer/WifiDirectManager.kt` uses Android Wi-Fi P2P APIs; `app/src/main/java/org/kiwix/kiwixmobile/zimManager/Fat32Checker.kt` tracks large-file write capability and free space; `core/.../reader/` and `core/.../downloader/` contain reusable offline reader/download interfaces.
- Stable v3.14.1 released 2026-05-14. Current `buildSrc/src/main/kotlin/Config.kt` specifies `minSdk=25`, `targetSdk=36`, JDK 21 and development version 4.0.0. Do not confuse development manifest version with latest published stable tag.
- Upstream `.github/workflows/ci.yml` runs standard/Play Store/branded/tablet emulator matrices on API 25/30/33/34/35/36. Main run 2026-10-22 https://github.com/kiwix/kiwix-android/actions/runs/39790121822 **failed** standard-app API 25 job; multiple other emulator jobs, lint, assemble and Detekt passed, and several standard-app jobs were cancelled after failure. A subsequent main CI run was cancelled; October 24 CD https://github.com/kiwix/kiwix-android/actions/runs/40043494095 passed but is not a clean runtime test.
- README distinguishes Play Store and full variants; Android scoped-storage rules limit ZIM file access in Play Store version. Warn that uninstalling can delete files under app-specific directories. FAT32 cannot store individual files over 4 GiB.
- Score: utility 5 + working 3 + reuse 5 + novelty 4 + documentation 5 + maintenance 5 = **27**; working-evidence discount reflects CI failure and no real-device tests.
- No independent APK build, emulator/device execution, ZIM file verification, offline cold-start, Wi-Fi Direct transfer or local-server security test.
- Related: `kiwix/java-libkiwix`, `openzim/libzim`, `openzim/zim-tools`, `kiwix/kiwix-android-branded`.
- Next: inspect Android API 25 regression and follow-up fixes, test ZIM file persistence on uninstall/upgrade, verify Wi-Fi Direct handshake and local HTTP binding/authentication, review native library licensing.

## Validation plan
Expected 72 canonical entries and 72 master headings, six-factor scoring valid and no duplicate URLs/names. Run the repository's Catalog Audit after publishing; do not claim passing Actions until observed. No third-party implementation code or assets copied.
