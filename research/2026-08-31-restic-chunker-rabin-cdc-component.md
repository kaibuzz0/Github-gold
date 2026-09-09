# restic/chunker — Rabin content-defined chunking component

- **Repository:** https://github.com/restic/chunker
- **Organization:** restic
- **Category:** storage primitives / deduplication / content-defined chunking / backup components
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 27 / 30
- **Provisional tier:** S
- **License:** BSD 2-Clause-style license
- **Primary language:** Go
- **Discovery source:** recursive follow-up from the Restic dossier
- **Research date:** 2026-08-31

## Executive summary

`restic/chunker` is a small, reusable Go implementation of content-defined chunking (CDC) built around rolling Rabin fingerprints. It is used by Restic, but the repository is intentionally separable from the larger backup engine and exposes a compact API for splitting arbitrary byte streams into content-dependent chunks.

This makes it valuable as a reusable storage primitive rather than merely as an internal Restic detail. CDC is useful anywhere a system wants chunk boundaries that remain comparatively stable when bytes are inserted or removed earlier in a file, which can improve deduplication behavior compared with fixed-size chunking.

The project has direct implementation evidence, tests, examples, CI, a permissive license, a current formal release, and recent maintenance. The strongest caveat is that its CI configuration currently targets older Go versions and older GitHub Action revisions even though the code itself received a new release in June 2026. That prevents a perfect score.

## Why it matters

Fixed-size chunking causes chunk boundaries after an insertion/deletion to shift, potentially changing the hashes of every subsequent block. CDC chooses boundaries from content instead. When the surrounding content is preserved, later boundaries can re-align, allowing unchanged regions to continue deduplicating.

`restic/chunker` provides that mechanism as a focused library with minimal external surface area. Potential uses include:

- backup systems;
- content-addressed storage;
- incremental replication;
- large-file synchronization;
- archival systems;
- binary delta/dedup pipelines;
- object packing and transfer systems;
- local-first applications that need block reuse.

It should be cataloged separately from `restic/restic`: Restic is the complete encrypted backup engine, while `restic/chunker` is a reusable algorithmic component.

## Core algorithm

Upstream describes the package as content-defined chunking based on a rolling Rabin checksum/fingerprint.

Source inspection shows a 64-byte sliding window and a rolling polynomial digest. For each incoming byte, the oldest byte's contribution is removed with a precomputed `out` table, the new byte is shifted into the digest, and modular reduction uses a second precomputed lookup table.

A chunk boundary is selected when either:

1. the rolling digest satisfies the configured split mask; or
2. the configured maximum chunk size has been reached.

The implementation will not emit a normal split before the configured minimum size.

Current defaults in source are:

- sliding window: **64 bytes**;
- minimum chunk size: **512 KiB**;
- maximum chunk size: **8 MiB**;
- average-bits setting: **20 bits**;
- intended average chunk size: approximately **1 MiB**;
- internal read buffer: **512 KiB**.

The public options allow callers to alter average split frequency, minimum/maximum boundaries, and the reusable buffer.

Primary source:

- https://github.com/restic/chunker/blob/master/chunker.go
- https://github.com/restic/chunker/blob/master/options.go

## Reusable interfaces

Two layers are notable.

### `BaseChunker`

`BaseChunker` exposes stateful split-point discovery over caller-provided byte slices through `NextSplitPoint`. This is the lower-level reusable primitive for applications that already own their buffering or streaming pipeline.

The split-point scanner maintains state across successive buffers until a boundary is found, so callers do not need to present an entire candidate chunk at once.

### `Chunker`

`Chunker` wraps the lower-level splitter around an `io.Reader` and manages buffering. Its `Next` method returns chunk metadata and data for successive chunks.

This separation is valuable because storage engines can either reuse the complete reader-oriented interface or embed only the boundary detector into an existing I/O architecture.

## Polynomial handling

The package documents and implements polynomial arithmetic for Rabin fingerprints rather than hiding the parameters as unexplained constants.

`RandomPolynomial()` is documented as generating random irreducible degree-53 polynomials. The documentation explains why degree 53 is used, how candidate bits are selected, how irreducibility is checked, the search limit, and the expected probability of selecting an irreducible candidate.

Upstream also documents that polynomial results were checked during development using GAP and provides background references to Rabin fingerprints, CRC/polynomial arithmetic, and irreducible-polynomial construction.

Primary source:

- https://github.com/restic/chunker/blob/master/doc.go
- https://github.com/restic/chunker/blob/master/polynomials.go

This is useful technical provenance: the project does not merely claim “Rabin chunking”; it exposes the polynomial machinery and explains the design basis.

## Performance-oriented implementation details

The implementation caches per-polynomial lookup tables in a synchronized global cache. Those tables precompute:

- the contribution of each possible outgoing byte across the window; and
- modular-reduction values for each possible high-byte state.

The current release history also records a throughput optimization specifically aimed at allowing the compiler to eliminate array-bound checks in the chunking hot path.

This matters for reuse because CDC often runs over every byte of large datasets; algorithmic correctness without attention to the inner loop would make the component much less attractive.

## Working evidence

The repository is small but not evidence-poor. It contains:

- `chunker.go` — streaming chunker and split-point implementation;
- `polynomials.go` — polynomial arithmetic;
- `options.go` — configurable boundaries and split frequency;
- `chunker_test.go` — chunking tests;
- `polynomials_test.go` — polynomial tests;
- `example_test.go` — public API example;
- `doc.go` — algorithm/design documentation;
- GitHub Actions CI.

The CI workflow runs `go test -cover ./...` across Windows, macOS, and Linux. Its configured matrix includes Go 1.15 through Go 1.19 and also runs a lint/go.mod check.

Primary source:

- https://github.com/restic/chunker/blob/master/.github/workflows/tests.yml

### CI caveat

The workflow itself is stale relative to current Go/GitHub Actions versions: it still names Go 1.19 as the newest matrix entry and uses older `actions/setup-go`, `actions/checkout`, and golangci-lint-action major versions.

That is a maintenance-quality deduction even though the project source and release activity are recent.

## Release and maintenance evidence

The latest formal release inspected is **v0.5.0**, published **2026-06-27**.

That release includes substantial changes rather than only metadata churn:

- GitHub Actions enablement/synchronization;
- public-interface example cleanup;
- separation of buffer management from split-point calculation;
- constructor options;
- chunk-throughput optimization;
- cleanup of the `NextSplitPoint` interface.

The current inspected `master` head is from **2026-06-20**, associated with the `NextSplitPoint` cleanup merged for v0.5.0.

Release:

- https://github.com/restic/chunker/releases/tag/v0.5.0

This is meaningful maintenance, but the project is intentionally small and changes far less frequently than the parent Restic repository. Low commit frequency here should not automatically be interpreted as abandonment because the component has a narrow, mature purpose.

## License

The repository contains a permissive two-condition BSD-style license allowing source and binary redistribution with or without modification, provided copyright/license conditions are retained.

Source:

- https://github.com/restic/chunker/blob/master/LICENSE

No source was copied into GitHub Gold during this research pass.

## Dependencies and runtime requirements

The module is intentionally minimal. The repository's `go.mod` contains the module declaration and Go version only; no third-party runtime dependency surface is evident from the inspected root module metadata.

This is an important reuse signal for an algorithmic library: consumers can adopt the chunker without importing a large storage framework.

## Verification performed in this run

GitHub Gold inspected:

- repository metadata;
- README;
- root source tree;
- `chunker.go`;
- `options.go`;
- `doc.go`;
- license;
- CI workflow;
- recent commits;
- formal releases.

GitHub Gold did **not**:

- run `go test`;
- execute benchmarks;
- compare chunk boundaries against Restic production repositories;
- validate deduplication ratios;
- reproduce the GAP polynomial checks;
- fuzz the rolling hash implementation;
- test adversarial or pathological byte sequences;
- independently prove the polynomial mathematics;
- perform a security audit.

Claims about testing and behavior above therefore distinguish upstream source/CI evidence from direct runtime verification.

## Caveats and boundaries

### CDC is not cryptographic integrity

The rolling Rabin fingerprint is used to choose chunk boundaries. It should not be confused with a cryptographic content hash or authentication primitive. Systems reusing this library still need an appropriate cryptographic hash/MAC/signature layer if they require integrity or authenticity.

### Chunker parameters are part of repository compatibility

Systems that persist chunk identities or expect deduplication compatibility must treat polynomial and chunking parameters as format-level data. Changing the polynomial, average-bit setting, or min/max boundaries can materially change boundary selection and therefore deduplication behavior.

This is particularly relevant to the parent Restic architecture, where repository chunker parameters must remain compatible for cross-repository deduplication behavior.

### Worst-case chunk size is explicit

The digest mask controls probabilistic/content-dependent boundaries, but `MaxSize` provides a hard upper bound. This avoids unbounded chunk growth when no natural boundary occurs for an extended region.

### API maturity versus semantic stability

The v0.x version means consumers should not assume semantic-versioning guarantees equivalent to a 1.x library. The 2026 release includes interface cleanup, demonstrating that API evolution is still possible.

## Gold scoring

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Fundamental primitive for deduplicated storage, backup, sync and archival systems. |
| Working Evidence | 5/5 | Production use in Restic plus tests, examples and CI. |
| Reusability | 5/5 | Small Go package, low dependency surface, both buffered and buffer-owner APIs. |
| Novelty | 4/5 | Rabin CDC is established rather than novel, but the implementation is technically strong and reusable. |
| Documentation | 4/5 | Good algorithm notes and API examples; README itself is brief. |
| Maintenance | 4/5 | v0.5.0 shipped June 2026 with meaningful work, but CI toolchain versions are stale. |
| **Total** | **27/30** | **Provisional S tier** |

## Evidence classification

**VERIFIED** means the repository's purpose and key implementation claims are supported by repository-native source, tests, CI, release history, and direct use by Restic.

It does **not** mean GitHub Gold independently executed or audited the algorithm.

## Relationship to existing GitHub Gold candidates

### `restic/restic`

Parent production consumer and the discovery source for this component. Restic contributes the complete backup/repository architecture; `restic/chunker` contributes a focused CDC primitive.

### Syncthing

Syncthing also performs block-oriented synchronization/deduplication, but it is not a duplicate candidate. Its replication protocol and block model solve a broader continuous-sync problem, whereas `restic/chunker` is a standalone content-boundary algorithm.

## Strong follow-up leads

1. Trace exactly how current Restic stores/derives the repository chunker polynomial and how compatibility is enforced during repository copy operations.
2. Inspect benchmark history and current throughput characteristics of `BaseChunker.NextSplitPoint` versus the reader-oriented `Chunker` path.
3. Compare this Rabin CDC implementation with modern FastCDC implementations on algorithm shape, minimum/average/maximum chunk behavior, dependency cost, and maintenance evidence.
4. Inspect `restic/rest-server` next for append-only authorization, authentication, connection/resource limits, and storage trust boundaries.
5. Broaden the batch afterward into a non-storage category to avoid over-clustering.

## Bottom line

`restic/chunker` qualifies as GitHub Gold because it extracts a difficult, performance-sensitive storage primitive into a compact and permissively licensed library with production provenance. The most valuable pieces are the stateful `BaseChunker` split-point API, the reader-oriented wrapper, configurable boundary controls, cached Rabin polynomial tables, and explicit polynomial utilities/documentation.

**Verdict: VERIFIED — provisional S / 27.**
