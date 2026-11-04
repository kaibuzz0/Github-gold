# libzim — ZIM offline archive read/write library

- **Repository:** https://github.com/openzim/libzim
- **Organization:** openZIM
- **Category:** offline knowledge / archival / file-format library / search / content packaging
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Primary language:** C++
- **License:** GPL-2.0-or-later according to upstream README; root `COPYING` contains GPLv2 text
- **Discovery source:** Recursive follow-up from the existing openZIM / ZIM Tools catalog entry
- **Inspection date:** 2026-09-13

## Executive finding

`openzim/libzim` is the reference implementation of the ZIM file format and provides the reusable library layer for reading and writing portable offline-content archives. It is a stronger component-level catalog target than another end-user reader because it exposes the primitives that downstream archival, offline-knowledge, disaster-preparedness, education, and disconnected-computing applications can build on.

The upstream README explicitly describes libzim as the reference implementation for ZIM and as a library for reading and writing ZIM files across many systems and architectures.

For GitHub Gold, libzim is valuable as:

1. the core programmatic read/write layer beneath the ZIM ecosystem;
2. a reusable reference for compact offline content packaging and lookup;
3. a search-enabled archival library when built with Xapian;
4. a portability case study spanning desktop, mobile, musl, and WebAssembly-oriented builds;
5. the component foundation behind higher-level projects such as `openzim/zim-tools` and Kiwix readers.

## High-value components and APIs

The public include tree exposes dedicated interfaces including:

- `archive.h` — archive access and metadata-facing operations;
- `entry.h` and `item.h` — stored-entry and item abstractions;
- `blob.h` — binary payload access;
- `search.h` and `search_iterator.h` — full-text/search result interfaces when Xapian support is enabled;
- `suggestion.h` and `suggestion_iterator.h` — suggestion/autocomplete-style query surfaces;
- `illustration.h` — illustration metadata/content handling;
- `uuid.h` — archive identity primitives;
- `writer/` — writer-side APIs for producing ZIM archives.

These are upstream public surfaces observed during inspection. GitHub Gold did not independently validate the correctness or ABI stability of each interface.

## Build and runtime profile

The upstream README documents a Meson/Ninja build and identifies core dependencies including:

- LZMA;
- ICU;
- Zstd;
- optional Xapian for search;
- Google Test for testing;
- the separate `openzim/zim-testing-suite` reference data corpus.

Upstream documents both shared and static library builds. Search APIs are removed when built without Xapian, which is an important deployment distinction for constrained or minimal builds.

## Working evidence

Repository-native evidence is strong.

### Automated tests

The upstream README documents a real test workflow using:

- `ninja download_test_data`;
- the external ZIM testing suite;
- `meson test`;
- optional skipping of very high-memory tests through `SKIP_BIG_MEMORY_TEST=1`.

The project explicitly notes that some tests can require up to 16 GB of memory, indicating the suite exercises substantial archive workloads rather than only trivial compile checks.

GitHub Gold did not execute these tests in this run.

### Current CI matrix

The inspected `.github/workflows/ci.yml` compiles and/or tests a broad target matrix.

Observed targets include:

- macOS ARM64 and x86-64;
- iOS ARM64 and simulator builds;
- Windows x64;
- Linux x86-64 static and dynamic variants;
- Ubuntu generations used by upstream CI;
- Linux ARM64 and ARM64-musl;
- Android ARM and ARM64;
- WebAssembly;
- builds with and without Xapian;
- writer-enabled and writer-disabled configurations in selected jobs.

Native macOS, Windows, and multiple Linux configurations download reference test data and execute the Meson test suite. Coverage is generated for selected Linux jobs. The workflow also runs OpenSSF Scorecard analysis and uses pinned action revisions.

This is strong Working Evidence, while remaining upstream evidence rather than independent execution by GitHub Gold.

## Release and maintenance evidence

The latest stable GitHub release inspected was **9.8.2**, published **2026-08-13**. Its release note describes a focused output-pollution fix associated with `zimcheck` behavior.

Maintenance remains current. Recent inspected commits include:

- **2026-09-13:** batch title-listing serialization merged, buffering title indexes in batches up to 64 KiB to reduce blob construction and write overhead while preserving byte-for-byte output;
- **2026-09-11:** larger checksum buffers / checksum-generation speedup;
- **2026-09-11:** documentation clarification for media/article count APIs.

The title-listing optimization includes added coverage for full and partial batches according to the commit description. These commits are evidence of active performance and correctness-oriented maintenance, not merely dependency churn.

## Portability value

The current CI matrix is unusually broad for a native archival library. It provides evidence that upstream actively maintains build paths spanning conventional desktop systems, mobile targets, musl-based Linux, and WebAssembly-oriented builds.

This makes libzim relevant to projects that need portable offline reference collections rather than a server-dependent content stack.

## Licensing

The upstream README states **GPLv2 or later**, and the root `COPYING` file contains the GNU GPL version 2 text.

This is a material reuse constraint. GitHub Gold should not copy libzim source into permissively licensed components without a proper GPL compatibility and redistribution analysis. Linking/cataloging the upstream implementation is preferable unless a downstream project deliberately adopts compatible GPL obligations.

Dependencies such as Xapian, ICU, Zstd, LZMA, Google Test, and any packaging/build dependencies must also be reviewed independently before redistribution.

No third-party source code was copied into GitHub Gold during this run.

## Relationship to existing GitHub Gold entries

GitHub Gold already catalogs `openzim/zim-tools`, which provides end-user/CLI operations such as checking, dumping, splitting, and writing archives.

`libzim` is not a duplicate of that entry. It is the lower-level reusable library and reference implementation on which ZIM ecosystem tooling can build. The two entries should be treated as a layered ecosystem:

- **libzim:** programmatic archive format implementation and read/write/search library;
- **zim-tools:** operational CLI tooling built around ZIM archives and libzim.

Related ecosystem targets include Kiwix readers, the ZIM testing suite, `kiwix-build`, and format/specification documentation.

## Verification performed

GitHub Gold inspected:

- upstream repository metadata and default branch;
- README build, dependency, test, usage, and license documentation;
- root GPLv2 `COPYING` file;
- public include/API tree;
- current CI workflow and target matrix;
- latest stable GitHub release metadata;
- recent upstream commit history through 2026-09-13;
- the existing GitHub Gold master-list context to avoid a duplicate ZIM Tools entry.

## Verification boundaries

GitHub Gold did **not**:

- compile libzim;
- execute its Meson tests;
- download or validate the ZIM testing corpus;
- create or parse a ZIM archive;
- test search behavior with Xapian;
- benchmark title serialization or checksum improvements;
- test Android, iOS, WebAssembly, Windows, macOS, or Linux binaries;
- independently verify release tarballs;
- perform ABI compatibility testing;
- fuzz malformed ZIM archives;
- audit parser memory safety or decompression-bomb behavior.

Claims in this dossier therefore distinguish repository-native/upstream evidence from actions actually performed by GitHub Gold.

## Caveats and risks

- GPL-2.0-or-later obligations materially affect source reuse and redistribution.
- Search support depends on optional Xapian integration and disappears when built without it.
- Some upstream tests are explicitly high-memory, which may matter for constrained CI or embedded build environments.
- Archive parsers process potentially untrusted structured data; malformed-input robustness and decompression/resource-exhaustion behavior deserve dedicated security testing before hostile-input deployments.
- Broad platform build coverage does not imply that GitHub Gold independently validated every target.

## Strongest follow-up leads

1. ZIM format framing, cluster layout, compression and random-access behavior.
2. Writer pipeline and content-provider abstractions.
3. Xapian index construction/search and suggestion paths.
4. Checksum/integrity semantics and malformed-archive handling.
5. `openzim/zim-testing-suite` as a reusable format-conformance corpus.
6. Large-archive memory behavior and the tests requiring high RAM.
7. WebAssembly build constraints and browser-side offline reader integration.
8. Android/iOS read-only configurations and size reduction.
9. Kiwix reader usage of libzim and downstream API/ABI expectations.
10. Fuzzing, decompression limits, and resource-exhaustion protections for untrusted ZIM inputs.
