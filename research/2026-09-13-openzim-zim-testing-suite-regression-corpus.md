# OpenZIM ZIM Testing Suite — regression and malformed-archive corpus

- **Repository:** https://github.com/openzim/zim-testing-suite
- **Organization:** OpenZIM
- **Category:** Offline archives / test corpus / parser validation / interoperability / defensive robustness
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **23/30 — A tier**
  - Utility: 4/5
  - Working Evidence: 4/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 3/5
  - Maintenance: 4/5
- **Primary repository role:** Versioned ZIM test-data corpus plus generation/inspection scripts
- **License:** **No declared repository license detected** — catalog/link only; do not copy or redistribute corpus files or scripts without explicit permission or clarified licensing
- **Discovery source:** Recursive GitHub-first follow-up from `openzim/libzim`
- **Inspection date:** 2026-09-13

## Executive finding

`openzim/zim-testing-suite` is a specialized regression corpus used by libzim and other OpenZIM repositories. Its value is not as an application but as a collection of known-good, legacy, edge-case, split, and deliberately corrupted ZIM archives that exercise parser and validator behavior across format generations.

The upstream README states that libzim's test suite requires ZIM fixtures and instructs consumers to point `ZIM_TEST_DATA_DIR` at the repository's `data` directory. It also warns that the checked-in test ZIM files are intentionally stable artifacts and should not be regenerated casually.

For GitHub Gold, the repository is valuable as:

1. a conformance/regression corpus for ZIM readers and validators;
2. a source of concrete malformed-file cases for defensive parser testing;
3. a reproducibility reference showing how historical and derived fixtures were generated;
4. a companion validation asset for `openzim/libzim`, `openzim/zim-tools`, Kiwix readers, and independent ZIM implementations.

## Why it matters

Archive readers are often tested primarily against normal files. That leaves malformed offsets, corrupt index structures, invalid MIME metadata, broken checksum positions, legacy layout variants, split archives, and other structural edge cases under-tested.

This repository contains fixtures whose names explicitly encode such failure modes. During inspection, the `data/withns` corpus exposed examples including:

- `invalid.bad_mimetype_in_dirent.zim`;
- `invalid.bad_mimetype_list.zim`;
- `invalid.invalid_checksumpos.zim`;
- `invalid.invalid_mimelistpos.zim`;
- multiple `invalid.misaligned_offset_of_first_blob_in_cluster_*` fixtures;
- `invalid.nonsorted_dirent_table.zim`;
- `invalid.nonsorted_title_index.zim`;
- `invalid.offset_in_cluster.zim`;
- out-of-bounds cluster/directory pointer cases.

Those are high-value defensive fixtures because they can help detect parser assumptions, validation gaps, unsafe offset handling, and compatibility regressions without inventing malformed archives from scratch.

GitHub Gold did not execute these files against any parser in this run; the usefulness assessment is based on upstream organization, naming, generation history, and documented integration with libzim.

## Repository structure

The root currently contains:

- `data/` — versioned ZIM test fixtures;
- `scripts/` — fixture-generation, inspection, and checksum-maintenance utilities;
- `src/` — source material used to construct fixture archives;
- `.github/workflows/release.yml` — packaging automation;
- `README.md` — integration and regeneration guidance.

The `data/` tree is separated into format/history groupings including:

- `withns/`;
- `nons/`;
- `noTitleListingV0/`.

That organization is useful for testing behavior across historical namespace/title-listing transitions rather than treating every fixture as interchangeable.

## High-value components

### Malformed ZIM corpus

This is the primary asset.

The inspected corpus contains intentionally invalid archives targeting structural assumptions such as:

- MIME metadata placement/content;
- checksum position validity;
- MIME-list position validity;
- first-blob offsets inside clusters;
- sortedness assumptions in directory/title indexes;
- cluster pointer bounds;
- directory-entry pointer bounds;
- archive-layout compatibility differences.

These fixtures are potentially useful for:

- parser regression tests;
- fuzzing seed corpora;
- interoperability tests;
- validator development;
- secure archive-ingestion pipelines;
- differential testing between independent ZIM readers.

**Licensing caveat:** because the repository declares no license, GitHub Gold should link to these files upstream rather than copy them into this repository or redistribute them in a derived corpus.

### `scripts/create_test_zimfiles`

The repository contains a substantial fixture-generation script named `scripts/create_test_zimfiles`.

Recent commit messages show it being used to regenerate derived fixtures and to create corrupt first-blob-offset cases across multiple data families. This script is valuable as provenance documentation because it records how edge-case archives were produced.

It should not be copied into GitHub Gold while licensing remains unclear.

### `scripts/inspectzim`

The repository exposes an `inspectzim` helper script. This is a potentially useful low-level inspection aid for understanding archive structure and for fixture-development workflows.

GitHub Gold did not execute or audit the script in this run.

### `scripts/fix_zimfile_checksum`

A checksum-repair utility was added in July 2026. The associated maintenance work used it while applying targeted in-place modifications to old fixtures without fully regenerating them.

That pattern is notable because regression corpora often require preservation of historical byte/layout properties; wholesale regeneration can accidentally remove the behavior a test is intended to preserve.

## Working evidence

### Direct libzim integration

The README explicitly states that libzim tests need these ZIM files and documents the `ZIM_TEST_DATA_DIR` environment variable for locating them.

This is stronger evidence than an isolated sample-data repository: the corpus is maintained as part of the broader OpenZIM validation ecosystem.

GitHub Gold did not independently run libzim against this corpus, so the integration claim remains upstream-supported rather than independently reproduced.

### Release packaging

The current release workflow runs when a GitHub Release is published and builds both ZIP and tar.gz archives from the repository's `data/` tree using `git archive`, then uploads those assets to the release.

The latest stable release inspected was **0.10.0**, published **2026-08-01**.

Its release assets include:

- `zim-testing-suite-0.10.0.tar.gz`;
- `zim-testing-suite-0.10.0.zip`.

GitHub metadata exposes SHA-256 digests for both assets.

This demonstrates a repeatable distribution path for consumers that need a fixed fixture set without cloning the entire repository.

### Recent maintenance

The most recent source-data maintenance inspected was committed **2026-07-23**.

One change corrected a historical bad language code in old ZIM fixtures. The commit explains why blindly regenerating those archives was undesirable: regenerated output introduced unrelated differences, so maintainers instead patched specific Xapian language-code bytes in place and recalculated checksums.

Other 2026 commits added malformed test data for too-small, too-large, and misaligned first-blob offsets inside clusters.

That activity is particularly relevant because it shows the corpus evolving in response to real libzim validation work rather than receiving cosmetic updates only.

## Release evidence

The latest inspected stable release is **0.10.0** (published 2026-08-01).

The release note records the old-ZIM language-code correction. Release artifacts are generated automatically from the `data/` directory and GitHub exposes SHA-256 digest metadata for the packaged ZIP and tar.gz files.

GitHub Gold did not download, unpack, hash, or independently validate those release archives.

## License and reuse boundary

This repository requires a stricter-than-normal reuse rule.

During inspection:

- no root `LICENSE`/`COPYING` file was present in the repository listing;
- GitHub's repository metadata reported `license: null`;
- the README did not declare a license.

Therefore GitHub Gold should treat the repository as **link-and-study only** unless OpenZIM later adds an explicit license or provides another clear grant covering the fixture data and scripts.

Do **not** copy:

- ZIM fixture binaries;
- generation scripts;
- inspection utilities;
- source fixture material;
- packaged release archives

into GitHub Gold based solely on public accessibility.

This licensing caveat is the main reason the project scores below S tier despite its strong technical research value.

## Security and defensive-research value

The intentionally malformed archive set is useful for defensive engineering because archive parsers process attacker-controlled offsets, lengths, index structures, compression metadata, and embedded content.

Potential legitimate uses include:

- testing bounds checks;
- validating rejection of corrupt structures;
- regression testing after parser optimizations;
- differential testing of independent implementations;
- seeding fuzzers with known pathological structures;
- checking that error handling fails closed rather than crashing or reading unintended memory.

No exploitation workflow was developed or tested in this run.

## Relationship to existing GitHub Gold entries

This repository complements rather than duplicates the existing ZIM ecosystem entries:

- `openzim/libzim` — programmatic ZIM reader/writer library;
- `openzim/zim-tools` — CLI utilities around ZIM operations;
- `openzim/zim-testing-suite` — stable regression/compatibility/malformed-file corpus.

The three layers should be cross-linked when canonical promotion occurs.

## Verification performed

GitHub Gold inspected:

- repository metadata and root structure;
- README integration instructions;
- fixture directory organization;
- representative intentionally-invalid filenames;
- available helper scripts;
- current release workflow;
- latest release metadata and artifact digests;
- recent commit history and fixture-generation provenance;
- duplicate status inside `kaibuzz0/Github-gold`.

## Verification not performed

GitHub Gold did **not**:

- execute libzim against the corpus;
- parse or validate individual ZIM files;
- run the fixture-generation scripts;
- verify expected pass/fail results for each malformed archive;
- fuzz libzim or another reader;
- download and hash release assets independently;
- audit the scripts for safety;
- establish copyright ownership for every fixture;
- obtain a license grant for reuse.

Accordingly, VERIFIED means the repository's role, maintained corpus, release mechanism, malformed-file inventory, and documented libzim integration have concrete upstream evidence; it does not mean GitHub Gold independently reproduced every test outcome.

## Gold scoring rationale

### Utility — 4/5

Highly useful for ZIM parser/validator development and regression testing, but specialized to one archive ecosystem.

### Working Evidence — 4/5

Documented libzim integration, maintained fixtures, explicit generation history, and versioned release artifacts provide strong evidence. GitHub Gold did not execute the corpus itself.

### Reusability — 4/5

The fixture organization and malformed cases are broadly useful to ZIM implementations, but the missing license prevents safe copying/redistribution and therefore limits practical reuse.

### Novelty — 4/5

Curated binary regression corpora with preserved historical/invalid edge cases are technically more valuable than ordinary example-file repositories.

### Documentation — 3/5

The README explains integration and warns against casual regeneration, and commit history carries useful provenance, but there is no comprehensive manifest mapping every fixture to its expected behavior.

### Maintenance — 4/5

Updated in 2026 with new corruption cases and targeted compatibility fixes, with an automated release-packaging workflow. Activity is naturally less frequent than a core library because fixture updates are event-driven.

## Recommended follow-up research

1. Map malformed fixture names to the exact libzim tests that consume them.
2. Build a non-copying index of fixture purpose → upstream path → expected validation result.
3. Inspect `libzim` bounds-checking and validation code corresponding to first-blob-offset corruption cases.
4. Determine whether OpenZIM has organization-level licensing guidance that clearly covers this repository.
5. Investigate whether Kiwix or third-party ZIM readers consume the same corpus.
6. Evaluate the corpus as upstream-only seeds for authorized fuzzing and differential testing.
7. Inspect `scripts/create_test_zimfiles` for the complete mutation taxonomy without copying its source.
8. Track whether a future release adds newer format-version fixtures or explicit licensing.

## Final assessment

`openzim/zim-testing-suite` is genuine GitHub Gold for defensive archive-engineering research: a maintained, versioned corpus of real, legacy, and intentionally malformed ZIM files tied directly to the OpenZIM test ecosystem.

Its principal weakness is not technical but legal/reuse-related: **no explicit repository license was detected**. Keep it cataloged and linked, use it as an upstream regression resource, and do not copy its artifacts or scripts into GitHub Gold unless licensing is clarified.