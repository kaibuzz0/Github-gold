# GitHub-first research — AccessKit and libkiwix (2026-10-30 UTC)

## Provenance and verification boundary
Both projects were found through GitHub-first exploration, with libkiwix followed from existing Kiwix Tools and libzim records. No usable transcript was obtained from the six YouTube seed playlists this run; no video claims are attributed to either project. Read repository-native README files, manifests, licenses, source layouts, tests and dated CI results. **No third-party source copied, built, installed, deployed, or independently tested.** VERIFIED means concrete upstream evidence, not a GitHub Gold security certification.

## AccessKit — VERIFIED (upstream), S28
- Repository: https://github.com/AccessKit/accesskit ; core crate manifest v0.25.2, per-crate `accesskit_winit` v0.34.2 released 2026-10-25. This workspace has **independently versioned crates**; do not report one global project release.
- Score: Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4 = **28/30**.
- Source: `accesskit/src/lib.rs` declares semantic `Role` types and `no_std` support; `accesskit_consumer/src/lib.rs` exports retained `Tree`, `NodeRef`, text ranges and contains test fixtures; `ARCHITECTURE.md` documents `TreeUpdate` and action requests; `adapters/` contains Android, iOS, macOS, Unix AT-SPI, Windows and winit adapters.
- Build/runtime: workspace Rust 1.87 minimum. Platform adapter and native accessibility runtime required; custom UI toolkit must publish stable node IDs, tree updates and handle action callbacks.
- Evidence: https://github.com/AccessKit/accesskit/actions/runs/40233340615 — 2026-10-25 main SHA `f302622`, **26/26 successful jobs** including cargo tests on Linux, macOS, Windows, Android and iOS Simulator, plus Clippy, docs, formatting and cargo-deny. These are upstream CI results, not live screen-reader user experience.
- License: workspace `MIT OR Apache-2.0`; `adapters/winit/Cargo.toml` declares Apache-2.0 only; `accesskit/src/lib.rs` credits Chromium-derived abstractions under `LICENSE.chromium` BSD-style terms. Preserve all applicable notices and inspect any crate-specific licenses before copying.
- Caveats: README acknowledges incomplete rich-text/hypertext support; architecture docs warn changed nodes must repeat complete properties; API semantic mapping is sparsely documented and must be tested with real assistive technology. Do not assume an NVDA integration from ecosystem proximity.
- Recursive leads: winit adapter, AT-SPI, Chromium-derived schema, NVDA as a complementary screen reader. Follow up with actual screen-reader focus, text input, nested trees and action-request integration.

## libkiwix — VERIFIED (upstream), S27
- Repository: https://github.com/kiwix/libkiwix ; stable [14.2.1](https://github.com/kiwix/libkiwix/releases/tag/14.2.1) published **2026-05-11**, while current `meson.build` declares **14.3.0 development**. These are not the same release.
- Score: Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4 = **27/30**.
- Source: `src/library.cpp` / `include/library.h` for library filtering; `src/manager.cpp` for catalog state; `src/server.cpp` / `include/server.h` for embedded HTTP server configuration; `src/server/internalServer.cpp` and `src/server/response.cpp` for request/response handling; `src/opds_catalog.cpp` and `src/opds_dumper.cpp` for OPDS; `src/search_renderer.cpp`, `src/spelling_correction.cpp` for search; `src/downloader.cpp` / `src/aria2.cpp` for downloads. `test/` contains server, library, search, catalog and manager tests.
- Build/runtime: Meson/Ninja C++17, ICU, libzim **>=9.4,<10** built with Xapian, pugixml, curl, microhttpd, zlib, Xapian, mustache header; aria2 at runtime. Linux/macOS/Windows plus Android/iOS cross-build targets.
- Evidence: https://github.com/kiwix/libkiwix/actions/runs/41027777528 — 2026-10-30 main SHA `73845de`, **11/11 successful jobs**. CI YAML runs tests for Linux desktop, macOS desktop and Windows; Android/iOS cross-build legs compile but skip runtime tests. **Separate packaging failure** https://github.com/kiwix/libkiwix/actions/runs/41027777537 — Debian-unstable failed its package-build step; Ubuntu Jammy/Noble packaging succeeded. No root cause asserted.
- License: GPLv3+ declared by Meson and C++ headers; `COPYING` contains GPLv3. Dependencies and included assets carry separate terms. Do not copy without compatibility review.
- Caveats: embedded HTTP server can listen on externally reachable interfaces; restrict bind/port, validate untrusted ZIM archives, review downloader integrity and resource limits. Build success does not prove network safety or physical-device compatibility.
- Recursive ecosystem: `kiwix/kiwix-tools` `meson.build` directly requires **libkiwix >=14.2,<15**, so 14.2.1 stable satisfies the declared range; `openzim/libzim` is a direct dependency; `kiwix/java-libkiwix`, `kiwix/kiwix-android`, `kiwix/kiwix-build` are related ports/tooling. No independent cross-project rebuild performed.

## Existing-entry maintenance
Updated Kiwix Tools' research note and JSON verification to distinguish **declared version compatibility** from **runtime interoperability**, and to record the libkiwix CI/packaging divergence. Its VERIFIED/S27 classification is unchanged.

## Next research
1. AccessKit: screen-reader integration with real UI trees, focus actions, text editing, and per-adapter licensing.
2. libkiwix: diagnose Debian-unstable packaging failure; test bounded HTTP/ZIM parsing, search and bind controls; confirm release-branch compatibility with kiwix-tools.
3. Broaden future batches into scientific instruments, offline mapping and embedded accessibility.