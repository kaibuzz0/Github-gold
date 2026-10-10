# go-pmtiles — production CLI and reusable PMTiles toolchain

- **Repository:** https://github.com/protomaps/go-pmtiles
- **Author / Org:** Protomaps
- **Category:** offline maps / geospatial / CLI / static hosting / data extraction / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 4
  - Documentation: 5
  - Maintenance: 5
- **Discovery:** Recursive follow-up from the verified Protomaps PMTiles dossier.

## What it is

`go-pmtiles` is the Go implementation and production command-line tool for creating, inspecting, transforming, extracting, serving, validating, and uploading PMTiles archives. It turns the PMTiles format from a useful storage specification into a practical field/server/data-engineering toolchain.

The repository README documents prebuilt releases for supported OS/architecture combinations, Go package API documentation, and a repository-native test command (`go test ./pmtiles`).

## Concrete reusable capabilities

The current CLI source exposes commands for:

- `show` — inspect local or remote archive metadata/header/TileJSON;
- `tile` — fetch a single Z/X/Y tile from local or remote storage;
- `extract` — create a smaller archive by zoom range, bounding box, or GeoJSON Polygon/MultiPolygon region;
- `cluster` — optimize archive size/layout and optionally deduplicate tiles;
- `convert` — convert MBTiles to PMTiles;
- `merge` — combine disjoint archives;
- `verify` — validate archive structure (explicitly not individual tile contents);
- `edit` — edit metadata/header fields;
- `serve` — expose Z/X/Y HTTP tiles from local or remote PMTiles, with configurable cache/CORS and optional Prometheus metrics endpoint;
- `upload` — upload a local archive to remote object storage;
- hidden `makesync` / `sync` operations for block-oriented incremental synchronization.

Remote storage support is wired through Go Cloud blob drivers for Azure Blob, local files, Google Cloud Storage, and S3-compatible storage.

## High-value component: range-efficient regional extraction

`pmtiles/extract.go` is particularly valuable. Rather than blindly downloading an entire remote archive before clipping it, extraction:

1. range-reads the V3 header;
2. requires a clustered source archive;
3. converts a requested bbox/GeoJSON region and zoom bounds into a relevance bitmap;
4. range-reads relevant root/leaf directory sections;
5. determines the tile byte ranges actually required;
6. merges nearby ranges under a configurable **overfetch budget** to reduce request count;
7. rebuilds header/directories and streams the selected tile data into a new archive.

The CLI exposes download-thread count, dry-run mode, and an `overfetch` ratio (default 0.05). This is a strong reusable pattern for extracting local/offline field-map packages from a much larger remotely hosted archive without transferring the whole source.

Recent source also contains explicit antimeridian handling for bbox extraction.

## Working evidence

Repository-native tests cover extraction primitives including relevant-entry filtering, run-length handling, leaf selection, deduplicated offset re-encoding, contiguous range coalescing, and overfetch range merging. Additional test files are present for bucket access, clustering, conversion, directory handling, editing, and other package components.

GitHub Gold did **not** execute these tests; their existence and inspected assertions are upstream evidence only.

The project publishes binary releases. The current release observed in this run is **v1.31.2**, published **2026-07-22**, with Darwin, Linux, and Windows assets for x86-64 and ARM64. The same July 22 change added a tested `Content-Length` fix for gzipped tile responses. Other 2026 maintenance includes an allocation reduction in directory deserialization, antimeridian extraction support, dependency/CVE maintenance, and MapLibre vector-tile MIME fixes.

## Install / runtime / platforms

- Prebuilt release binaries: macOS/Darwin, Linux, Windows; x86-64 and ARM64 assets observed for v1.31.2.
- Development: Go toolchain (`go run main.go`, `go test ./pmtiles`).
- Remote archive/storage workflows can use Azure Blob, GCS, S3-compatible storage, or local file blobs through the included Go Cloud drivers.
- `serve` can run as an HTTP tile proxy and optionally expose Prometheus metrics on a separate admin port.

## License

BSD-3-Clause. Redistribution/modification are permitted subject to retaining the copyright/license/disclaimer conditions and the non-endorsement clause.

No upstream implementation code was copied into GitHub Gold.

## Why it matters for GitHub Gold

This is more than a format converter. It is a compact geospatial operations toolkit with unusually good composability for:

- downloading only a region needed for an offline/emergency map kit;
- converting legacy MBTiles datasets;
- validating and inspecting archives;
- static/object-storage map deployment;
- local tile serving;
- archive optimization/deduplication;
- programmatic Go integration;
- incremental/sparse data-transfer experiments via the sync machinery.

The regional range-extraction implementation is the standout subcomponent because it directly combines PMTiles' single-file/range-addressable design with practical bandwidth reduction.

## Caveats

- `verify` validates archive structure, not semantic correctness of every tile payload.
- `Extract` currently rejects non-clustered source archives and source comments note no support for leaf directory level 2+ in the inspected path.
- Source contains a TODO noting directory construction can consume too much RAM; planet-scale extraction should not be assumed memory-light without benchmarking.
- Object-store behavior, egress costs, authentication and HTTP range semantics remain deployment-specific.
- Map data licenses/attribution remain separate from the BSD software license.
- GitHub Gold did not benchmark extraction throughput, request reduction, RAM, archive sizes, object-store costs, or sync behavior.

## Verification performed

Inspected repository metadata, README, BSD license, current CLI dispatch/source, extraction implementation, extraction tests, package file layout, recent commits, and current release metadata. No binary was downloaded or executed; no Go package was built; no test suite was run; no PMTiles archive was converted, extracted, served, uploaded, or synchronized by GitHub Gold.

## Strongest next leads

1. **protomaps/basemaps** — evaluate the complete OSM/Natural Earth → Planetiler → PMTiles production pipeline and style assets.
2. **felt/tippecanoe** — evaluate high-volume vector-tile generation as a separate reusable component.
3. **go-pmtiles sync/makesync** — deeper inspection if incremental archive updating becomes relevant; these commands are currently hidden and should not be treated as a stable public interface without further evidence.
4. **Caddy integration** — inspect the repository's Caddy package/plugin for simple self-hosted PMTiles deployment.

## Verdict

**VERIFIED / S / 29.** `go-pmtiles` is a mature, permissively licensed, cross-platform CLI/library that operationalizes PMTiles with conversion, validation, regional range extraction, serving and object-storage workflows. Its range-efficient extractor is particularly strong GitHub Gold material for offline/local-first map systems.