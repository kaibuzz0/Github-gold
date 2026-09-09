# go-pmtiles — operational PMTiles CLI, range server, conversion and differential-sync toolkit

- Upstream: https://github.com/protomaps/go-pmtiles
- Related format/reference repository: https://github.com/protomaps/PMTiles
- Research date: 2026-09-06
- Category: mapping / offline systems / geospatial / CLI tooling / static storage / object storage / HTTP range serving
- Evidence level: VERIFIED
- Provisional Gold score: S / 28
- License: BSD-3-Clause
- Language: Go
- Discovery source: recursive GitHub-first follow-up from the existing PMTiles dossier

## Executive finding

`protomaps/go-pmtiles` is the operational Go implementation around the PMTiles single-file map archive format. It is materially different from the `protomaps/PMTiles` reference/specification repository: this repository packages a practical command-line utility and reusable Go library for inspecting, extracting, converting, clustering, verifying, serving, editing, merging, uploading, and synchronizing PMTiles archives.

For GitHub Gold, the strongest value is the combination of three layers:

1. a standalone cross-platform CLI for real archive operations;
2. reusable Go packages for PMTiles directory/header/archive manipulation and HTTP serving;
3. range-oriented tooling that can operate on local files and cloud/object-storage backends without converting the archive into a conventional tile database.

It is especially relevant to disconnected field-map preparation, static/self-hosted map delivery, serverless/object-storage workflows, converting legacy MBTiles datasets, and building reproducible map-data maintenance pipelines.

## Why it matters

The PMTiles format is designed around one seekable archive rather than millions of loose files or a permanently running tile database. `go-pmtiles` is the practical system-administration layer for that design.

The current CLI exposes commands for:

- `show` — inspect archive/header/metadata/TileJSON state;
- `tile` — extract one Z/X/Y tile to stdout;
- `cluster` — rewrite an unclustered archive for locality and deduplication;
- `edit` — modify JSON metadata or selected header data;
- `extract` — create a smaller archive by zoom range, bounding box, or GeoJSON Polygon/MultiPolygon;
- `merge` — combine disjoint archives;
- `convert` — convert MBTiles to PMTiles;
- `verify` — inspect archive structural invariants;
- `serve` — expose archives as an HTTP Z/X/Y tile endpoint;
- `upload` — push a local archive to remote storage;
- experimental `makesync` / `sync` — generate/apply block-oriented differential updates.

This is substantially more useful than a simple format converter because it covers most of the archive lifecycle: ingestion, transformation, inspection, verification, distribution, serving, and incremental update research.

## Reusable component families

### Multi-backend local/object-storage abstraction

`main.go` imports Go Cloud blob drivers for local files, Azure Blob Storage, Google Cloud Storage, and S3-compatible storage. The command surface accepts remote buckets for inspection, tile reads, extraction, serving, and upload operations.

This is a useful implementation pattern for offline/serverless tooling: core archive logic is not hard-wired to one cloud vendor, and the same high-level archive operations can be expressed against a local filesystem or object-store backend.

### Archive inspection and one-tile extraction

The `show` command can emit metadata, selected header JSON, or TileJSON and can operate on local or remote archives. The separate `tile` command addresses an individual Z/X/Y tile and writes it to stdout.

These small surfaces are useful for diagnostics, shell pipelines, CI validation, and debugging an archive without opening a full map client.

### Geographic/zoom extraction

`extract` creates a new archive from a larger local or remote input using:

- minimum/maximum zoom levels;
- bounding boxes;
- GeoJSON Polygon or MultiPolygon regions;
- configurable download concurrency;
- configurable overfetch to trade extra bytes for fewer HTTP requests;
- dry-run analysis.

A July 7, 2026 upstream change explicitly added antimeridian support, which is meaningful evidence that the extraction implementation handles real geographic edge cases rather than only simple continental bounding boxes.

### MBTiles conversion, clustering and deduplication

The CLI can convert an existing MBTiles SQLite database to PMTiles and can cluster an unclustered PMTiles archive. Both conversion and clustering expose a switch to disable tile deduplication.

This makes `go-pmtiles` a migration bridge from a widely deployed database-backed tile format into PMTiles' single-file deployment model.

### Structural verification

`pmtiles/verify.go` performs concrete structural checks rather than simply attempting to open an archive.

Inspected checks include:

- required root/metadata/leaf/tile-data offsets must be non-zero;
- section lengths must remain inside the local file;
- total archive length must agree with header-derived length, including the supported 16 KiB padded layout;
- each directory entry must remain within tile-data bounds;
- clustered archives are checked for tile-content ordering;
- addressed-tile, tile-entry, and unique-content counts are recomputed and compared with header statistics;
- minimum zoom is checked against the minimum tile ID;
- center zoom must lie within the min/max range;
- geographic bounds must have positive area.

This is useful both as an end-user `verify` command and as a reference for PMTiles archive integrity invariants.

Important limitation: the CLI help and source explicitly frame this as archive-structure verification, not cryptographic integrity or semantic validation of every individual tile payload.

### HTTP tile serving

`serve` turns a local path or object-store prefix into an HTTP Z/X/Y tile endpoint. The command exposes:

- interface and port selection;
- a configurable cache size;
- CORS origin handling;
- a public URL used for TileJSON generation;
- a separate optional admin port exposing Prometheus metrics.

The latest release, v1.31.2, fixed `Content-Length` on tile responses, specifically including gzipped tiles. The upstream commit includes a test for the header's presence. This is a small but operationally important HTTP correctness fix because chunked transfer behavior can interact badly with compressed tile responses and downstream clients/CDNs.

### Differential archive synchronization — experimental

The repository includes hidden `makesync` and `sync` commands. `sync.go` labels the feature explicitly:

> WARNING: This is an experimental feature. Do not rely on this in production!

The implementation is nevertheless technically interesting.

It retrieves a `.sync` sidecar describing new archive blocks, hashes candidate blocks from the existing clustered archive with xxHash, separates reusable local blocks from changed blocks, combines contiguous ranges, batches HTTP multi-range requests, constructs a temporary new file, copies matching tile chunks locally, downloads only needed remote chunks, and finally renames the temporary file over the old archive.

The design is relevant as a reusable research pattern for distributing updated very-large immutable-ish archives without requiring a complete re-download.

It should remain a research component, not a production recommendation, until its failure handling, remote-server assumptions, authenticity model, and interrupted-update semantics are more deeply verified.

## Source-tree evidence

The repository is compact and purpose-focused. The current `pmtiles/` package contains dedicated implementation/test pairs for core operations including:

- bitmap handling;
- cloud/local bucket access;
- clustering;
- conversion;
- directory serialization;
- editing;
- geographic extraction;
- merging;
- region handling;
- serving;
- showing/reading;
- sync-file generation and synchronization;
- uploading;
- verification.

The repository also contains small binary PMTiles fixtures and an `examples/minimal.go` integration example.

This is strong evidence that the CLI is backed by reusable package-level components rather than being a monolithic command wrapper.

## Working evidence

The README documents direct development and test commands (`go run main.go`, `go test ./pmtiles`).

GitHub Actions currently runs the PMTiles Go test suite on both Ubuntu and Windows. A second job performs:

- `gofmt` cleanliness checks;
- `go vet` on the Caddy proxy integration;
- `go vet` on the CLI entrypoint;
- `go vet` across the `pmtiles` package;
- Revive linting.

The repository publishes cross-platform release binaries through GoReleaser.

This is solid working evidence, though not perfect: the inspected CI matrix does not include macOS even though release assets are published for macOS, and the workflow's third-party GitHub Actions are still referenced by mutable tags rather than immutable commit SHAs.

## Maintenance and release evidence

The repository is active and not archived.

Latest inspected stable release: **v1.31.2**, published **2026-07-22**.

GitHub release metadata includes SHA-256 digests for six inspected platform archives:

- macOS ARM64;
- macOS x86_64;
- Linux ARM64;
- Linux x86_64;
- Windows ARM64;
- Windows x86_64.

Recent inspected maintenance includes:

- **2026-07-22:** set `Content-Length` for tile responses and add a regression test, fixing chunked encoding behavior for gzipped tiles;
- **2026-07-13:** preallocate directory-entry decoding from the already-known entry count, with the upstream benchmark description reporting a large reduction in allocated bytes for a ~62k-entry planet leaf directory;
- **2026-07-07:** add antimeridian support to geographic extraction;
- **2026-05-28:** avoid emitting output when a requested tile is absent;
- **2026-04-22:** dependency/security refreshes including a commit explicitly described as resolving CVEs through updates to networking, Caddy, AWS SDK and gRPC dependencies.

The latest source commit observed is the same commit used by the v1.31.2 release, so maintenance is current to July 22, 2026 rather than September 2026. That is still recent enough for a high maintenance score, but it is less active than several S-tier projects already in the GitHub Gold batch.

## Supply-chain and operational caveats

The inspected CI uses mutable action references:

- `actions/checkout@v3`;
- `actions/setup-go@v3`;
- container tag `morphy/revive-action:v2`.

These are weaker than immutable-SHA pinning.

The code relies on a broad Go dependency graph, including cloud storage SDKs and HTTP/server integrations. Consumers seeking high-assurance reproducibility should review the exact module graph and build provenance rather than treating a successful GitHub release as a reproducible-build guarantee.

The `serve` command defaults to interface `0.0.0.0`. That is convenient for LAN/server use, but users should deliberately select network exposure, CORS policy, TLS termination, and any authentication/reverse-proxy boundary needed for their deployment. This research pass did not identify the CLI itself as an authenticated multi-tenant tile service.

The experimental sync path makes strong assumptions about the remote `.sync` sidecar and HTTP range/multipart behavior. Its source contains several places where response/error handling deserves deeper adversarial inspection before production use. The upstream warning is therefore appropriate and should be preserved in the catalog.

## Licensing

The repository's root `LICENSE` is the standard **BSD 3-Clause** license, copyright Protomaps LLC.

That permits source and binary redistribution with the stated notice/disclaimer and non-endorsement conditions.

The CLI's BSD-3-Clause license does not automatically govern map data placed inside PMTiles archives. OpenStreetMap-derived basemaps and other datasets may have separate attribution or redistribution obligations.

No upstream code or data was copied into GitHub Gold.

## Gold score

Provisional score: **28 / 30 — S tier**

- Utility: **5/5** — covers conversion, extraction, inspection, verification, serving, upload, merge, clustering, and operational archive management.
- Working Evidence: **4/5** — tests on Linux/Windows, vet/format/lint checks, concrete fixtures and published binaries; no independent run in this research pass and macOS is not in the inspected test matrix.
- Reusability: **5/5** — permissive license, compact Go package, local/cloud abstraction, standalone binary, straightforward library API.
- Novelty: **5/5** — operationalizes a range-readable single-file map format and includes an unusual differential range-sync experiment.
- Documentation: **4/5** — README and external CLI/package docs are clear, but much of the command detail lives outside the repository README and the experimental sync subsystem is intentionally under-documented.
- Maintenance: **5/5** — 2026 releases, security/dependency maintenance, performance work, geographic edge-case fixes, and current cross-platform binaries; latest observed code activity is July rather than September.

## Verification performed in this run

Inspected directly:

- current GitHub Gold branch/PR to avoid duplicate work and preserve the existing research workflow;
- `protomaps/go-pmtiles` repository metadata and non-archived status;
- root README and documented test/development instructions;
- root BSD-3-Clause license;
- CLI command definitions in `main.go`;
- package/source-tree organization and test/fixture presence;
- `pmtiles/verify.go` structural checks;
- `pmtiles/sync.go` experimental differential-update architecture;
- GitHub Actions test workflow;
- recent commit history through 2026-07-22;
- latest GitHub release metadata and GitHub-provided SHA-256 asset digests.

## Verification boundary

I did **not**:

- build the CLI;
- run `go test`, `go vet`, Revive, or GoReleaser;
- convert an MBTiles database;
- create, cluster, edit, merge, extract, upload, or verify a real PMTiles archive;
- start the HTTP tile server;
- test CORS, metrics, cache behavior, TLS/reverse-proxy deployment, or object-store integrations;
- test S3, GCS, Azure Blob, or filesystem bucket backends;
- test antimeridian extraction independently;
- reproduce the directory-allocation benchmark;
- independently confirm the stated CVEs fixed by the dependency update commit;
- generate or apply `.sync` sidecars;
- test interrupted sync, malformed multipart responses, hostile sync metadata, or range-server incompatibilities;
- independently hash release binaries;
- audit the code for security vulnerabilities.

Claims above are limited to direct source/workflow/release/history inspection and explicitly identified upstream evidence.

## Risks and limitations

- Archive structural verification is not cryptographic or full tile-payload verification.
- Object-store behavior depends on provider credentials, range support, consistency semantics, and correct HTTP metadata.
- Exposing `serve` on `0.0.0.0` requires intentional network/security configuration.
- The sync subsystem is explicitly experimental upstream and should not be cataloged as production-safe.
- GitHub Actions are pinned to mutable version tags rather than immutable SHAs.
- The dependency graph is large because cloud-provider and serving integrations are included.
- Map-data licensing remains independent from the BSD-licensed CLI.
- Large archive manipulation still requires appropriate temporary disk, bandwidth and memory planning; this pass did not benchmark resource use.

## Strongest follow-up leads

1. Audit `DeserializeHeader`, `DeserializeEntries`, TileID/run-length encoding, and integer/range bounds handling against malformed archives.
2. Inspect the `server.go` cache/range behavior, conditional responses, CORS handling, path normalization and remote bucket semantics.
3. Treat `sync.go` as a separate research component: verify `.sync` format assumptions, multipart range ordering, error propagation, temporary-file durability, authenticity, and interrupted-update recovery.
4. Inspect `bucket.go` and upload behavior across S3/GCS/Azure/local backends, especially multipart/range consistency.
5. Evaluate the Caddy integration as a reusable embedded PMTiles reverse-proxy/server component.
6. Connect `go-pmtiles` with Planetiler/Protomaps Basemaps as a complete reproducible OSM → PMTiles → offline/serverless delivery pipeline.
7. Compare `go-pmtiles verify` against independent PMTiles implementations to build a future malformed-archive interoperability corpus.
