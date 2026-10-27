# 2026-10-27: libarchive and Kiwix Tools — source and CI research

**Provenance:** GitHub-first. Two additional YouTube playlist IDs searched without indexed transcript results. No video viewed. No independent build, extraction, server deployment, ZIM search, fuzzing or security audit. No upstream code copied.

## libarchive — VERIFIED upstream, S28

- [Repository](https://github.com/libarchive/libarchive); [v3.8.10](https://github.com/libarchive/libarchive/releases/tag/v3.8.10) published 2026-10-14 (security/bugfix/minor features).
- Source inspected: `libarchive/archive_read_support_format_zip.c`, `archive_read_support_format_7zip.c`, `archive_read_support_format_tar.c`, `archive_read_support_filter_zstd.c`, `archive_entry.c`, `examples/minitar/`, `tar/`, `unzip/`, and `libarchive/test/`.
- [Master CI 40530777935](https://github.com/libarchive/libarchive/actions/runs/40530777935) passed 20/20 jobs on 2026-10-27, including test stages on Ubuntu, Alpine, Windows, macOS and FreeBSD. [CodeQL 40530777979](https://github.com/libarchive/libarchive/actions/runs/40530777979) passed. [CIFuzz workflow](https://github.com/libarchive/libarchive/blob/master/.github/workflows/cifuzz.yml) exists for pull requests; no local fuzz run.
- Root `COPYING` gives a permissive two-clause BSD-style notice for most source, explicitly excepting UC Regents three-clause portions, public-domain file, triple-licensed BLAKE2 and mixed build scripts. File headers control.
- Risks: malformed archive parsing, traversal/symlink extraction, decompression bombs. Follow-up: secure extraction defaults, fuzz corpus, advisories and parser resource limits.

## Kiwix Tools — VERIFIED upstream, S27

- [Repository](https://github.com/kiwix/kiwix-tools); [3.8.2](https://github.com/kiwix/kiwix-tools/releases/tag/3.8.2) published 2026-03-02.
- Source inspected: `src/server/kiwix-serve.cpp` (HTTP bind, connection options, ZIM serving), `src/searcher/kiwix-search.cpp` (full-text/suggestion/spelling), `src/manager/kiwix-manage.cpp` (XML/OPDS library), `meson.build` (C++17; libzim >=9,<10; libkiwix >=14.2,<15; docopt).
- [Main CI 36844685289](https://github.com/kiwix/kiwix-tools/actions/runs/36844685289) passed 3/3 jobs on 2026-10-01. Linux static/dynamic jobs compile; Windows job compiles and runs Meson tests. [Scheduled analysis 40272845437](https://github.com/kiwix/kiwix-tools/actions/runs/40272845437) passed 2026-10-26 but is Actions analysis, not runtime proof.
- Root COPYING GPLv3, inspected C++ source headers GPL-3.0-or-later. libkiwix, libzim, docopt and ZIM content rights need separate review.
- `kiwix-serve` defaults to HTTP port 80 on all interfaces; bind explicitly and isolate on trusted networks. No independent HTTP, ZIM, Docker or security test.
- Ecosystem: direct dependencies kiwix/libkiwix and openzim/libzim; complementary openzim/zim-tools and separate kiwix/kiwix-android. Added related-project references to existing libzim and ZIM Tools entries.
- Follow-up: LAN isolation, hostile ZIM resource limits, multi-device offline deployment and search accuracy.

## Hygiene

- Scores: libarchive 5/5/5/3/5/5 = 28; Kiwix Tools 5/4/5/4/5/4 = 27.
- Added two canonical entries, cross-referenced existing libzim and ZIM Tools, corrected an existing master-list punctuation error. No source copied.
