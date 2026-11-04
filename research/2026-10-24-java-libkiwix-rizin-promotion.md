# java-libkiwix and Rizin — evidence, promotion and maintenance (2026-10-24)

## Hygiene and source provenance
- Continued open draft PR #7 on `agent/research-ladybird-browser-engine`, starting from head `4dd0628ea0cab78abebd7f7f6c76680a5d4eab8e`. No parallel branch, merge or unrelated rewrite.
- Pre-change: 72 canonical entries, 72 master headings, empty promotion queue. Confirmed both new canonical URLs and names absent from catalog; no aliases/forks colliding.
- Source breadth: recursive Kiwix/libzim Android JNI binding investigation plus independent defensive reverse-engineering/tooling investigation. Added reciprocal `kiwix/java-libkiwix` relation to existing libzim entry.
- All six seed playlist IDs were searched by exact ID on 2026-10-24; search returned no usable playlist/transcript leads. No YouTube-derived claims.
- No upstream source, compiled binaries, assets or dependencies copied.

## java-libkiwix — VERIFIED (upstream), S / 27
- Repository: https://github.com/kiwix/java-libkiwix (owner Kiwix), Android Java/Kotlin JNI binding to libkiwix and libzim.
- 2026-10-21 stable release **2.7.0**: https://github.com/kiwix/java-libkiwix/releases/tag/2.7.0 . `CHANGELOG` adds `Archive.getLanguages`/`getMainLanguage`, `Book.getLanguages` and libzim 9.8.2; `lib/build.gradle` specifies libkiwix 14.2.1.
- Inspected `README.md`, `COPYING`, `LICENSE`, `CHANGELOG`, `lib/build.gradle`, `lib/src/main/java/org/kiwix/libzim/`, `lib/src/main/java/org/kiwix/libkiwix/`, `lib/src/main/cpp/libzim/`, `lib/src/main/cpp/libkiwix/`, `lib/src/test/`, `.github/workflows/ci.yml`. Key source locations: `Archive.java`, `Searcher.java`, `SuggestionSearcher.java`, `Library.java`, `Manager.java`, `Server.java`, JNI `archive.cpp`, `searcher.cpp`, `kiwixserver.cpp`.
- Upstream CI https://github.com/kiwix/java-libkiwix/actions/runs/39562805161 on 2026-10-21 **succeeded** (single Build & test source code job). Workflow installs dependencies, executes `./gradlew buildHeaders build`, creates coverage report. This is upstream build/test evidence, **not** a local Android runtime or hardware test.
- Runtime/build: README says JDK 17; Gradle `minSdk 24`, `compileSdk 34`, NDK `27.3.13750724` with flexible page-size support. AAR output; native ABI and linker dependencies must be matched.
- Licensing: README says GPLv3 or later; inspect native libkiwix/libzim and downloaded prebuilt binaries/dependency notices before redistribution. No code copied.
- Score: Utility **5**, Working Evidence **4**, Reusability **5**, Novelty **3**, Documentation **5**, Maintenance **5** = **27 / S**. Not 5 for working evidence because no independent device execution or untrusted-ZIM fuzzing.
- Next: malformed archive and JNI exception/ownership tests; 16KB-page devices, ABI matrix, embedded server bind/authentication boundaries; inspect native dependency licensing.

## Rizin — VERIFIED (upstream, mixed CI), A / 25
- Repository: https://github.com/rizinorg/rizin . Official `README.md` describes binary analysis, file formats, disassembly and scriptable CLI tools; `BUILDING.md` uses Meson/Ninja.
- Latest inspected stable release **v0.9.1** on 2026-06-29: https://github.com/rizinorg/rizin/releases/tag/v0.9.1 . Current `dev` `meson.build` declares `v0.10.0`; not a published stable release.
- Inspected `README.md`, `BUILDING.md`, `meson.build`, `COPYING.LESSER`, `REUSE.toml`, `LICENSES/`, `librz/bin/`, `librz/arch/`, `librz/diff/`, `test/README.md`, `.github/workflows/ci.yml`, recent commits and CI job outcomes. Reusable parts: `librz/bin/` format loaders, `librz/arch/il/` intermediate language, `librz/diff/fastcdc.c` content-defined chunking, `bytes_diff.c`/`lines_diff.c`, `librz/search/`, `binrz/` CLI tools, `test/db/` regression and `test/fuzz/` fuzz scaffolding.
- CI 2026-10-23: https://github.com/rizinorg/rizin/actions/runs/39999863129 and https://github.com/rizinorg/rizin/actions/runs/40000224650 both **failed**. Four `capstone-v4`, `capstone-v5`, `capstone-v6`, `capstone-sys` jobs failed at `Build with Meson`; Linux GCC/Clang, macOS Clang, ASAN, QEMU RISC-V and licensing checks passed. Do not report overall CI success or claim root cause beyond failed build step.
- License: Meson declares `LGPL-3.0-only` for core, but `REUSE.toml`, SPDX file headers and `LICENSES/` enumerate multiple license families. Example `librz/diff/fastcdc.c` SPDX is LGPL-3.0-only. Each extracted file and its dependencies require review.
- Score: Utility **5**, Working Evidence **3**, Reusability **5**, Novelty **4**, Documentation **4**, Maintenance **4** = **25 / A**. Capstone failures and no independent binary parser test cap score.
- Next: determine Capstone compatibility failure cause from upstream logs/patches; run format parser regression and fuzz corpus with permission and isolated test inputs; inspect `rizinorg/rz-pipe` and `rizinorg/rizin-testbins` licensing. Use only for authorized forensic/interoperability research.

## Verification boundary
- GitHub Gold did **not** build, install, execute, fuzz, flash, benchmark or security-audit either project.
- No local CI run has been claimed; only upstream GitHub Actions evidence is cited.
