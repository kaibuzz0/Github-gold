# ZLint Test Corpus — large certificate regression dataset for Web-PKI linting

- **Repository:** https://github.com/zmap/zlint-test-corpus
- **Organization:** ZMap
- **Category:** PKI / X.509 / testing / regression corpus / data infrastructure
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **22/30 — A tier**
  - Utility: 4/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 3/5
  - Documentation: 3/5
  - Maintenance: 3/5
- **Primary artifacts:** bzip2-compressed CSV certificate corpus plus corpus-generation SQL
- **License:** Apache-2.0 at repository root; dataset provenance/redistribution should still be reviewed separately before copying certificate material
- **Discovery source:** recursive research from `zmap/zlint`
- **Inspection date:** 2026-09-16

## Executive finding

`zmap/zlint-test-corpus` is the external large-scale certificate corpus used by ZLint's integration-test machinery. It is valuable less as a standalone application than as reproducible regression infrastructure: ZLint fetches representative certificate data from this repository, parses and lints the certificates, and compares aggregate lint results with committed expected values so behavior changes become visible in CI.

The corpus is intentionally stored outside the main ZLint repository because of its size. ZLint's current integration documentation says its default configuration consumes 60 corpus CSV files representing just under 600,000 certificates.

This makes the repository a useful example of a general engineering pattern: keep heavyweight real-world fixtures in a separate versioned corpus while the primary project stores test logic, expected summaries, filters, and CI orchestration.

## What the repository contains

The inspected root contains:

- `README.md` — explains corpus generation and its relationship to ZLint;
- `query.sql` — the historical Censys SQL used to select/export certificate records;
- `certificates/` — compressed certificate-data chunks;
- `LICENSE` — Apache License 2.0.

The repository README says exported data is split into files containing 5,000 certificates and compressed with bzip2.

## Corpus-generation method

The checked-in `query.sql` selects certificate subject/issuer information, raw certificate material and SHA-256 fingerprints from the Censys public certificates table. The query filters on NSS-valid certificates, ranks certificates by issuer/subject grouping, samples the result and joins back to retrieve full selected records.

The current ZLint integration README describes the corpus more conservatively as representative data collected from Censys using a query intended to select random samples of certificates chaining to a Mozilla-trusted root. The exact semantics of the historical query and current Censys schema should not be assumed to be identical without rerunning/revalidating it against the present dataset.

## Why it matters

### Real-world regression testing

Synthetic unit fixtures are good for checking precise edge cases, but they do not represent the distribution of structures found across hundreds of thousands of deployed certificates. ZLint uses this corpus to supplement targeted lint unit tests with broad empirical regression coverage.

ZLint's integration harness:

1. downloads configured corpus chunks;
2. caches them locally;
3. parses certificate rows;
4. runs selected/all lints;
5. counts lint outcomes;
6. compares actual counts against expected values committed in the ZLint integration configuration;
7. fails the integration test when those results diverge.

That is concrete upstream evidence that this corpus is operational test infrastructure rather than a dormant data dump.

### Debugging support

ZLint's integration tooling can filter by lint name, lint source and certificate fingerprint, print per-lint result summaries, and emit fingerprints for certificates producing findings. The documentation demonstrates using the corpus to expose a deliberately reintroduced lint regression and then narrowing the unexpected result set to individual certificate fingerprints for investigation.

This pattern is reusable beyond PKI: large real-world fixture corpus + deterministic summary expectations + targeted drill-down tools.

### External heavyweight fixture pattern

The corpus is deliberately separated from ZLint to avoid bloating the main repository. This is a strong architectural pattern for projects that need large packet captures, firmware images, document corpora, protocol traces, scientific samples or other expensive fixtures in CI without forcing every source checkout to contain them.

## Working evidence

The strongest evidence comes from the parent ZLint repository, not merely from this corpus repository's own commit frequency.

ZLint's current `v3/integration/README.md` states that GitHub Actions runs the integration suite via `make integration`. The process downloads configured data files, parses/lints the certificates, compares results to expected values, and fails on differences. It explicitly identifies `zmap/zlint-test-corpus` as the separate repository hosting those data files.

The same documentation says the default configuration uses 60 files representing just under 600,000 certificates and caches downloaded copies to avoid repeated transfers.

ZLint's integration configuration contains direct raw-file references into this repository, independently connecting the corpus to the active test harness.

## Maintenance signals

This repository is not maintained at the same cadence as ZLint itself, and that distinction matters.

The latest commit observed during this inspection is from **2023-08-20**, merging an expansion that added approximately **190,000 email-protection certificates**. The underlying addition commit touched many compressed corpus chunks.

Therefore Maintenance is scored 3/5 rather than inheriting ZLint's current maintenance score. The corpus remains actively referenced by ZLint's current integration infrastructure, but its own data refresh cadence is slow.

## Reusability assessment

Useful reusable ideas/components include:

- external versioned heavyweight fixture repositories;
- corpus chunking and compression;
- reproducible source-query provenance;
- cached CI downloads;
- aggregate expected-result regression checks;
- lint/fingerprint filtering for failure triage;
- representative real-world PKI data for parser/linter research.

The corpus can be valuable for defensive PKI research, certificate parser robustness work, lint regression analysis and standards implementation testing.

## License and provenance caveat

The repository root contains Apache-2.0. That is clear licensing evidence for the repository work as presented upstream, but GitHub Gold should not infer that a repository-level software license resolves every independent right or redistribution question associated with public certificates and data sourced through Censys.

No certificate data, compressed corpus chunks, SQL, or ZLint source was copied into GitHub Gold in this run. Catalog/link-first treatment is preferable unless a later extraction task separately confirms the provenance and redistribution requirements for the exact artifact involved.

## Caveats and limitations

- The corpus repository itself has sparse documentation.
- Its most recent observed corpus update is from 2023, so it should not be described as a current snapshot of the Web PKI.
- The historical `query.sql` references a Censys table/schema and sampling process that may not be directly reproducible unchanged today.
- Real-world corpus coverage does not guarantee coverage of every malformed ASN.1 construction, policy edge case, certificate profile or contemporary CA behavior.
- Aggregate expected-result testing can detect behavioral changes but does not by itself establish whether a changed result is correct; maintainers must vet intended expectation updates.
- Certificate validity filtering can bias the dataset away from malformed or invalid structures that are important for parser-hardening research.
- Large datasets create bandwidth/storage/runtime costs; ZLint mitigates this with caching and smaller configurable test sets.

## Verification performed by GitHub Gold

This run inspected:

- repository metadata and default branch;
- root README;
- root directory inventory;
- root Apache-2.0 license;
- corpus-generation SQL;
- recent commit history;
- the 2023 email-protection-certificate expansion commit;
- current ZLint integration documentation;
- current ZLint code-search references/configuration linking the integration suite to this corpus;
- the existing GitHub Gold branch to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- download or decompress corpus chunks;
- inspect individual certificates;
- run the Censys query;
- validate current Censys schema compatibility;
- run `make integration` in ZLint;
- independently reproduce the approximately 600k-certificate count;
- independently validate the email-protection subset;
- audit every certificate's provenance;
- determine whether every corpus artifact can be redistributed independently of repository-level licensing;
- benchmark corpus download, parsing or lint throughput.

## Gold rationale

**Utility — 4/5:** high-value real-world regression corpus for PKI/linter testing, but specialized rather than general-purpose.

**Working Evidence — 5/5:** the current parent ZLint integration system explicitly consumes the corpus in CI and documents failure/debugging behavior.

**Reusability — 4/5:** strong testing/data-infrastructure pattern and useful research corpus, constrained by size, specialization and provenance considerations.

**Novelty — 3/5:** external regression corpora are established practice, but this is a substantial real-world X.509 application of the pattern.

**Documentation — 3/5:** enough to understand generation and parent integration, but sparse at the corpus repository itself.

**Maintenance — 3/5:** current ZLint still consumes it, but the corpus's latest observed direct update is from 2023.

**Provisional total: 22/30 — A tier.**

## Strongest next leads

1. Map `v3/integration/config.json` expected summaries to corpus chunks and determine how expectation updates are reviewed.
2. Inspect the ZLint corpus loader for malformed-row/parser failure handling and bounded resource behavior.
3. Compare the large corpus with ZLint's targeted per-lint unit fixtures to identify coverage boundaries.
4. Investigate whether the email-protection subset is incorporated into current default/specialized integration configurations.
5. Evaluate reproducible modern corpus-refresh options without assuming the historical Censys query remains directly executable.
6. Research `zmap/zcertificate` as the next independent ZMap ecosystem candidate.
