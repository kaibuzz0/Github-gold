# LibrePCB and Xournal++ — GitHub Gold research, 2026-10-24 (CDT)

## Scope and provenance
GitHub-first discovery across electronic design automation and offline document/stylus software. The existing draft PR #7 branch contained 80 canonical projects; neither new URL nor name was present. The six saved YouTube playlists remain unverified as transcript sources; no video-derived finding or third-party code import is claimed.

## LibrePCB — VERIFIED (upstream), S / 28
**Repository:** https://github.com/LibrePCB/LibrePCB

**Score:** Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.

**Primary evidence inspected:** README, GPLv3 LICENSE.txt, LICENSES/ (multiple license texts), apps/, libs/librepcb/core/, libs/librepcb/kicadimport/, libs/librepcb/eagleimport/, tests/README.md, workflows, releases and recent commits. `libs/librepcb/core/` contains geometry, rulecheck, serialization, 3D, export, project and library models; `kicadlibraryconverter.cpp` and `kicadtypeconverter.cpp` support KiCad library import; `apps/librepcb-cli/commandlineinterface.cpp` is a headless automation entry point. Tests are divided into unit/integration, CLI system, GUI functional and UI groups.

**Releases and CI:** Latest inspected stable GitHub release [2.1.1](https://github.com/LibrePCB/LibrePCB/releases/tag/2.1.1), published **2026-06-12**. Master commit `b1f683c` dated **2026-10-20** merges a fix for a possible interactive BOM crash on unconnected footprint pads. [CI run 40072270629](https://github.com/LibrePCB/LibrePCB/actions/runs/40072270629), created **2026-10-24**, passed all 9 jobs (Linux GCC/Clang, Windows, macOS x86_64/ARM64, Doxygen, clang-tidy, stylecheck). Earlier Oct 22 runs 39853944608, 39850133589 and 39842588997 failed; do not claim uniformly green historical CI. These are upstream checks, not independent PCB correctness tests.

**Runtime and licensing:** C++20 compiler, Rust >=1.92 GNU, Qt >=6.2, CMake >=3.22, OpenSSL; OpenCASCADE optional. Windows uses MinGW GNU, not MSVC. README warns master is **unstable and can break workspaces/projects**; use stable builds for real boards. Root GPL-3.0, but REUSE metadata and submodules require file-level license checks before extraction. No source code copied.

**Next checks:** KiCad/EAGLE import geometry fidelity, CLI export determinism, DRC rule coverage, fabrication Gerber/assembly output, and cross-version project migrations.

## Xournal++ — VERIFIED (upstream), S / 27
**Repository:** https://github.com/xournalpp/xournalpp

**Score:** Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.

**Primary evidence inspected:** README, LICENSE (GPLv2 text), Debian `copyright.txt` (core GPL-2+ with GPL-3+, ISC, CC-BY-SA assets), `src/core/model/`, `src/core/pdf/`, `src/core/plugin/`, `src/core/audio/`, `plugins/`, `test/README.md`, `test/unit_tests/`, `test/gtk_tests/`, workflows and releases. Reusable components include `Stroke.cpp`, `Document.cpp`, `Layer.cpp`, `Snapping.cpp` for ink and layered document models, PDF integrations, Xournal file handlers, and a Lua plugin framework with example plugins.

**Releases and CI:** Latest inspected stable GitHub release [v1.3.8](https://github.com/xournalpp/xournalpp/releases/tag/v1.3.8), published **2026-09-26**. The `nightly` tag is prerelease and should not be treated as newer stable. Master commit `b2ef631` on **2026-10-24** fixes clipboard paste dispatch; nearby commits address audio setup, Windows DLL packaging and invalid display DPI. [Build run 40072649214](https://github.com/xournalpp/xournalpp/actions/runs/40072649214), created **2026-10-24**, passed 7/7 jobs on Ubuntu x86_64/ARM, Windows x86_64/ARM, and macOS x64/ARM. Workflow defines GoogleTest unit tests, locale-specific runs and GTK integration tests. Later PR runs marked `action_required` were not counted as passing or failing execution.

**Runtime and licensing:** Offline GUI for Linux, Windows and macOS, with AppImage/Flatpak/distribution packages. Pen tablet support depends on host hardware and drivers. LaTeX needs external TeX installation. GPL-2.0-or-later core per `copyright.txt`; multiple asset licenses, including GPL-3.0+ and CC-BY-SA-4.0, require separate attribution/reuse analysis. Lua plugins are executable extensions; no sandbox guarantees were verified.

**Next checks:** Malformed `.xopp` and embedded PDF handling, import/export fidelity, stylus pressure and latency, plugin trust boundaries, autosave and backup recovery.

## Maintenance and boundaries
Existing ZMK entry records a 2026-10-24 `proton_c` scheduled-build failure. A new 2026-10-25 UTC scheduled build (40162399914) was in progress during this research pass, so its outcome is **not** asserted. No preexisting score or tier was altered. No code was built, installed, flashed, executed or independently security-tested. Upstream CI is explicitly labeled upstream evidence. No third-party implementation code or assets copied.
