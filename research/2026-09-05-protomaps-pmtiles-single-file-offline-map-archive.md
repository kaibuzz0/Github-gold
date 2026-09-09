# Protomaps PMTiles — single-file offline/serverless map archive and range-read toolkit

- Upstream: https://github.com/protomaps/PMTiles
- Companion CLI: https://github.com/protomaps/go-pmtiles
- Project: PMTiles
- Research date: 2026-09-05
- Category: offline systems / mapping / geospatial / static storage / tile archives / MapLibre / field infrastructure
- Evidence level: VERIFIED
- Provisional Gold score: S / 28
- Reference implementation license: BSD-3-Clause
- Specification license: public domain / CC0 where applicable
- Primary implementations in repository: TypeScript/JavaScript, Python, C++, OpenLayers integration, AWS Lambda and Cloudflare Workers examples
- Discovery source: recursive GitHub-first follow-up from Organic Maps and MapLibre Native offline-mapping research

## Executive finding

`protomaps/PMTiles` is the reference repository for PMTiles, a single-file archive format for pyramids of map tiles. Its core architectural value is that a map archive can live as one ordinary object on local storage or commodity HTTP object storage and be accessed through byte-range reads instead of requiring a database-backed tile server.

For GitHub Gold, PMTiles is valuable at three layers at once:

1. a compact, openly specified tile archive format;
2. reusable browser/Node/Python/C++ readers and mapping adapters;
3. an ecosystem path from offline local files to static object storage, MapLibre/Leaflet/OpenLayers clients, and the separate `go-pmtiles` operational CLI.

That combination makes it unusually relevant to disconnected field mapping, self-hosted basemaps, low-maintenance static map delivery, archival datasets, and applications that need to move a whole tiled dataset as a single file.

## Why it matters

Traditional tiled-map deployments often involve very large collections of small files or a database plus an application server. PMTiles instead places tile data, directory/index information, and metadata into one seekable archive.

The Version 3 specification requires a fixed 127-byte header and requires the root directory to be fully contained within the first 16 KiB. That is an important latency-oriented invariant: a range-capable client can fetch the beginning of the archive and obtain the root index needed to find later directory or tile ranges without downloading the whole dataset.

This design is useful both online and offline. The same `.pmtiles` file can be read locally or exposed through ordinary range-capable HTTP/object storage, reducing the operational difference between a portable field dataset and a serverless hosted map.

## Reusable component families

### Version 3 archive specification

`spec/v3/spec.md` defines the current PMTiles format. A Version 3 archive contains:

- a fixed 127-byte header;
- a root directory;
- JSON metadata;
- optional leaf directories;
- tile data.

The header records offsets and lengths for root directories, metadata, leaf directories, and tile data, plus tile counts, clustering status, compression, tile type, zoom range, bounds, and center metadata.

The format supports internal compression values for none, gzip, Brotli, and Zstandard, and tile types including MVT, PNG, JPEG, WebP, AVIF, and MapLibre Vector Tile.

The requirement that the root directory fit within the first 16,384 bytes is especially reusable as a design pattern for cloud/local optimized seekable archives: put enough routing/index state near the front of the object to minimize high-latency round trips.

### Browser and Node reader

`js/src/` contains the TypeScript implementation used by the `pmtiles` package. The documented API exposes a `PMTiles` reader plus adapters for mapping libraries.

The MapLibre integration registers a `pmtiles://` protocol handler, allowing a MapLibre source to point directly at a remote or local PMTiles archive instead of a conventional tile endpoint. Leaflet raster integration is also documented, and OpenLayers support lives in a separate repository directory.

Recent upstream work in August 2026 added cancellation of pending directory fetches when all dependent tile requests are cancelled, explicitly to reduce outstanding work during rapid map zooming. This is a useful client-side invariant for range-read applications: index/directory requests should share work but must also become cancellable once no consumer remains.

### Python, C++, OpenLayers, and serverless implementations

The repository contains additional implementations and integration surfaces under:

- `python/pmtiles`;
- `python/rio-pmtiles`;
- `cpp/`;
- `openlayers/`;
- `serverless/aws/`;
- `serverless/cloudflare/`.

This is important evidence that PMTiles is a format/ecosystem rather than a single JavaScript library. The serverless examples demonstrate how a static archive can also sit behind lightweight edge/serverless adapters where an application needs HTTP behavior beyond direct object storage.

### Companion `go-pmtiles` CLI

The main README directs users to `protomaps/go-pmtiles` for the operational CLI. Documented commands include converting MBTiles into PMTiles and uploading archives to S3-compatible object storage.

The latest stable companion CLI release inspected is **v1.31.2**, published **2026-07-22**. GitHub release metadata provides SHA-256 digests for Linux, macOS, and Windows binaries across x86_64 and ARM64 variants. That release fixed `Content-Length` handling for tile responses, including gzipped tiles.

The companion CLI should be treated as a related Gold component rather than silently conflated with the reference-format repository.

## Working evidence

Working evidence is strong and extends beyond README claims.

The current CI workflow:

- builds the JavaScript package;
- builds and checks the PMTiles web viewer/application;
- compiles the AWS Lambda package and CloudFormation output;
- type-checks and lint-checks the Cloudflare worker;
- generates TypeDoc documentation;
- type-checks the OpenLayers package;
- runs JavaScript tests;
- runs JavaScript formatting/lint checks;
- runs Python `pmtiles` unit tests;
- installs and runs `rio-pmtiles` pytest coverage;
- compiles the C++ implementation;
- runs Cloudflare worker tests.

This cross-implementation CI is meaningful evidence for a file-format project because multiple readers/adapters are kept buildable against the same repository and specification.

## Maintenance and release evidence

The PMTiles repository is active and not archived.

Recent inspected commits include:

- **2026-08-19:** update the application to PMTiles JS 4.5 and refresh dependencies;
- **2026-08-19:** upgrade MapLibre GL integration to v6 and update its Vite web-worker setup;
- **2026-08-10:** PMTiles JS v4.5.0 work adding cancellation of unnecessary pending directory fetches.

The main `protomaps/PMTiles` repository currently exposes no GitHub Releases through the GitHub Releases API. Distribution is instead split across npm/PyPI packages and the separate `go-pmtiles` repository for CLI binaries. That is not a functionality problem, but it lowers release-hygiene clarity compared with projects that publish one canonical, immutable release surface from the same repository.

The latest inspected `go-pmtiles` release is **v1.31.2 from 2026-07-22**, with GitHub-provided SHA-256 digest metadata for all inspected platform archives.

## Supply-chain/build caveats

The CI is broad but its GitHub Actions references are not pinned to immutable commit SHAs. The inspected workflow uses mutable major-version references including:

- `actions/checkout@v3`;
- `actions/setup-node@v3`;
- `peaceiris/actions-gh-pages@v3`.

That is weaker than strict immutable-SHA workflow hygiene.

The repository also installs dependencies from npm and Python package indexes as part of CI. Lockfiles and package-manager integrity controls help, but any consumer seeking highly reproducible builds should review the complete dependency/bootstrap chain rather than treating CI success as a full supply-chain guarantee.

## Licensing

The root `LICENSE` explicitly states that the reference implementations in this repository are licensed under **BSD 3-Clause**.

The same file separately states that the PMTiles specification itself is public domain, or CC0 where applicable. Sample tilesets are subject to their own license terms.

This separation matters: code reuse, specification reuse, and redistribution of sample or generated map datasets are distinct licensing questions. Map data may carry OpenStreetMap or other source attribution obligations independent of PMTiles' code license.

No PMTiles source code or map data was copied into GitHub Gold.

## Gold score

Provisional score: **28 / 30 — S tier**

- Utility: **5/5** — immediately useful for offline maps, portable geospatial archives, static hosting, and serverless tile delivery.
- Working Evidence: **5/5** — CI exercises JavaScript, Python, C++, OpenLayers, viewer/serverless builds, and multiple test suites; companion CLI publishes platform binaries.
- Reusability: **5/5** — open specification, permissive reference code, multiple language implementations, and simple file/object-storage deployment model.
- Novelty: **5/5** — the single-file, range-readable tile pyramid plus front-loaded root-directory design is technically distinctive and operationally useful.
- Documentation: **5/5** — formal Version 3 specification, implementation READMEs, examples, typed docs, recipes, and serverless integration guidance.
- Maintenance: **3/5** — active 2026 development and current packages, but the main repository has no GitHub Release surface and CI Action pinning is dated/mutable.

## Verification performed in this run

Inspected directly:

- current GitHub Gold research branch and PR to avoid duplicate catalog work;
- PMTiles root README;
- root BSD-3-Clause/specification licensing boundary;
- Version 3 archive specification and root-directory placement invariant;
- repository CI workflow and cross-language build/test surface;
- JavaScript usage documentation and MapLibre/Leaflet integration;
- JavaScript source-tree organization;
- recent PMTiles commit history through 2026-08-19;
- main-repository GitHub Releases API result;
- latest `go-pmtiles` companion CLI release metadata and published SHA-256 digests.

## Verification boundary

I did **not**:

- build any PMTiles implementation;
- run JavaScript, Python, C++, rio-pmtiles, or serverless tests;
- create or convert a `.pmtiles` archive;
- serve a PMTiles file over HTTP range requests;
- load a PMTiles archive in MapLibre, Leaflet, or OpenLayers;
- test offline/local-file operation;
- run the `go-pmtiles` CLI;
- upload data to S3/R2 or another object store;
- independently hash released CLI binaries;
- fuzz malformed PMTiles archives;
- benchmark directory lookup, range-request count, latency, or cache behavior.

Claims above are limited to direct source/specification/workflow/release/history inspection and explicitly identified upstream evidence.

## Risks and limitations

- A range-based web deployment depends on correct HTTP byte-range and CORS behavior from the storage/CDN layer.
- A single large archive changes failure and update semantics: replacing or corrupting one object can affect the whole map dataset even though reads are granular.
- Map-data licensing and attribution remain separate from PMTiles code/spec licensing.
- The main repository distributes components through multiple package ecosystems rather than one canonical GitHub Release surface.
- Current GitHub Actions use mutable version tags rather than immutable commit SHAs.
- Clients parsing untrusted remote archives should treat offsets, lengths, compression metadata, directories, and JSON metadata as untrusted input; parser hardening was not independently audited in this run.

## Strongest follow-up leads

1. Inspect directory serialization, tile-ID ordering, run-length encoding, and leaf-directory lookup in the Version 3 specification and implementations.
2. Trace the JavaScript cache and in-flight request coalescing/cancellation logic, especially around rapid pan/zoom behavior.
3. Evaluate malformed-archive and integer/offset bounds handling across JavaScript, Python, C++, and Go implementations.
4. Research `protomaps/go-pmtiles` as a separate operational Gold candidate: `convert`, `extract`, `serve`, `upload`, verification and cloud-storage behavior.
5. Evaluate `maplibre-ext/protomaps-basemaps` / Protomaps Basemaps as a separate reproducible OpenStreetMap-to-PMTiles generation pipeline.
6. Compare PMTiles with MBTiles and Cloud Optimized GeoTIFFs specifically on disconnected-field use, streaming/range behavior, update mechanics, and corruption recovery.
7. Build a future end-to-end field-mapping stack dossier connecting PMTiles + MapLibre Native + Organic Maps-style offline datasets + static local HTTP serving.