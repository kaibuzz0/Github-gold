# Planetiler — planet-scale vector-tile generation and PMTiles/MBTiles build pipeline

- Upstream: https://github.com/onthegomap/planetiler
- Research date: 2026-09-06
- Category: mapping / geospatial / offline systems / OpenStreetMap / vector tiles / PMTiles / data pipelines
- Evidence level: VERIFIED
- Provisional Gold score: S / 29
- License: Apache-2.0 for Planetiler source; bundled/adapted components and generated map data carry separate notices/attribution obligations
- Language: Java
- Discovery source: recursive GitHub-first follow-up from the PMTiles / go-pmtiles research chain

## Executive finding

`onthegomap/planetiler` is a high-performance vector-tile generation engine designed to transform large geospatial datasets—especially OpenStreetMap—into portable MBTiles or PMTiles archives on a single machine without requiring an external spatial database.

For GitHub Gold, its strongest value is not just the end-user CLI. Planetiler exposes a reusable tile-generation architecture: input readers, profile-driven feature transformation, geometry clipping/simplification, external merge sorting, tile batching/encoding, archive writers, YAML-defined custom maps, and Java APIs that can be embedded into larger geospatial workflows.

This completes an important part of the current offline-mapping chain already represented in GitHub Gold: raw OSM/geospatial inputs → Planetiler processing → PMTiles/MBTiles archive → go-pmtiles/PMTiles serving and lifecycle tooling → MapLibre/Organic Maps-style clients.

## Why it matters

Planetiler is specifically engineered around the difficult part of large-scale map production: taking huge unordered geospatial inputs and converting them into tile-addressed, compressed vector archives efficiently enough to run on one machine.

The README states that it aims to build a world map in a few hours on a single machine. Upstream publishes concrete benchmark logs rather than only making a performance claim. Current README examples include a 2026 planet-scale run over a roughly 92 GB OSM PBF producing an approximately 81 GB PMTiles archive in about 19 minutes on a 192-CPU / 720 GB machine, plus several earlier lower-resource runs. These figures are upstream benchmark evidence, not independently reproduced results.

Planetiler can emit both MBTiles and PMTiles, which makes it useful as a bridge between conventional SQLite tile archives and newer range-readable static archives.

## Core architecture

The upstream architecture document describes three main phases:

1. process input files according to a profile and write intermediate encoded vector-tile features;
2. externally sort those features by tile ID;
3. iterate through sorted features, group them by tile, encode/compress them, and write the final archive.

This is a strong reusable systems pattern for datasets too large to keep fully in memory.

### OSM two-pass reconstruction

For `.osm.pbf` data, Planetiler performs two passes so it can reconstruct ways and multipolygon relations from node/relation state.

The first pass stores node coordinates and relevant relation membership. The second pass emits nodes, reconstructs way geometry from stored node coordinates, tracks multipolygon members, and reconstructs multipolygon relations when possible.

The implementation uses specialized structures such as `LongLongMap` and `LongLongMultimap` so callers can trade memory/disk behavior against large input sizes.

### Profile-driven feature transformation

User-defined Java profiles implement `Profile` to determine:

- which vector-tile features are emitted;
- what relation information must be retained;
- feature attributes and zoom behavior;
- tile-level post-processing.

For simpler use cases, `planetiler-custommap` provides a YAML-configured profile system. This is especially valuable because it lets operators define custom map schemas and overlays without writing Java code.

### Geometry slicing and repair

Planetiler's render path scales/simplifies geometry per zoom level and slices geometry into tile-sized pieces using `TiledGeometry`, whose stripe-clipping approach is derived from `geojson-vt`.

It explicitly handles longitude wrapping across ±180 degrees and uses JTS-based polygon repair after coordinate rounding when simplification/snap-to-tile precision creates topology errors.

That topology-repair step matters operationally: invalid polygons can render incorrectly in clients such as MapLibre, so the pipeline does not assume that geometries remain valid after clipping/rounding.

### External merge sort

Planetiler writes intermediate encoded features into chunk files and then performs an external merge sort by a compact sortable key containing zoom/X/Y/layer/sort information.

Each chunk can be sorted independently and the final stream is produced by a k-way merge. This architecture enables datasets much larger than available RAM while still producing tiles in deterministic tile order.

### Tile batching, deduplication and archive emission

During final emission, sorted features are grouped into tiles and then variable-size batches. Complex tiles can be isolated so worker utilization remains high rather than blocking a single writer path.

Before encoding a tile, the pipeline checks whether it has the same contents as the previous tile to avoid unnecessary re-encoding for repeated large-area content such as oceans.

Tiles are encoded as vector tiles, gzip-compressed, and then written to the selected archive backend.

## Reusable component families

Strong components worth tracking independently include:

- `OsmReader` and associated OSM PBF parsers/reconstruction logic;
- `FeatureCollector` and `Profile` abstractions;
- `TiledGeometry` tile slicing;
- `GeoUtils` geometry normalization/topology repair;
- `ExternalMergeSort` for large intermediate feature sets;
- `WorkQueue` worker coordination;
- `FeatureGroup` compact intermediate feature encoding/grouping;
- `TileArchiveWriter` and archive backends;
- MBTiles and PMTiles output implementations;
- `planetiler-custommap` YAML-driven map generation;
- `planetiler-examples` as reusable integration/project templates.

The project can also be consumed as a Maven/Gradle dependency (`planetiler-core`) rather than only as the bundled CLI/JAR.

## Input/output and deployment model

Current documentation supports:

- OpenStreetMap `.osm.pbf` inputs;
- additional geographic datasets including Natural Earth and shapefile-oriented sources;
- declarative YAML map definitions;
- Java profile implementations;
- MBTiles output;
- PMTiles output;
- direct Java execution via release JAR;
- Docker execution;
- library embedding through Maven/Gradle.

The quickstart supports automatic data acquisition for configured areas. The README's example `--area=monaco --download` workflow downloads source material and produces a local archive, while users can point directly at existing local OSM PBF files for controlled/offline build pipelines.

## Working evidence

The repository contains substantial CI rather than only compile checks.

The current main CI workflow:

- checks formatting with Spotless;
- builds/verifies across Ubuntu, macOS and Windows;
- tests both JDK 21 and JDK 25;
- builds container images/tar output through Jib;
- builds and runs the standalone example project;
- generates an example MBTiles archive from a Monaco OSM PBF fixture and verifies that archive;
- builds the branch JAR/container path;
- exercises data-download paths;
- runs the release-test script;
- runs the quickstart through build, JAR and Docker modes and checks the resulting Monaco archive.

This is unusually useful evidence because it tests a real miniature map-generation workflow in addition to unit/build verification.

A caveat: many GitHub Actions in the inspected workflow use mutable major-version tags such as `actions/checkout@v7`, `actions/setup-java@v5`, and `actions/upload-artifact@v7`, although the retry Action used for network-sensitive downloads is pinned to a full commit SHA. The workflow therefore has good functional breadth but not uniformly strict immutable supply-chain pinning.

## Maintenance and release evidence

The repository is active and not archived.

Latest inspected stable release: **v0.10.2**, published **2026-03-29**.

The release added zoom-16 support, STAC-based selective Overture downloading, examples/overlays, bug fixes and dependency updates. Its `planetiler.jar` release asset includes GitHub-provided SHA-256 digest metadata, and upstream also publishes a separate `.sha256` file.

Recent source maintenance observed through **2026-08-05** includes Maven plugin and dependency updates; other July 2026 updates include SQLite JDBC, GeoTools, MessagePack, JUnit and GitHub Actions dependency refreshes.

The repository metadata itself was updated on September 4, 2026, while the latest observed code commit in this pass is August 5, 2026. The maintenance score reflects active 2026 development but does not treat repository metadata updates as code activity.

## Benchmark evidence

Planetiler keeps benchmark logs in the repository and documents planet-scale runs with machine specification, input size, runtime, CPU usage and output size.

This is stronger than an unqualified performance claim, but GitHub Gold should preserve the distinction: the published figures are upstream benchmarks under specific hardware/configuration and were not reproduced in this run.

The architecture also makes clear why performance is plausible: parallel profile processing, disk-backed chunking, external sorting, geometry-specific optimizations, batching and avoiding repeated encoding for duplicate adjacent tile contents.

## Licensing and data-attribution boundary

The root source license is **Apache License 2.0**.

Planetiler also ships a detailed `NOTICE.md` that identifies third-party dependencies and adapted code under several compatible/separate licenses, including Apache, MIT, BSD, EDL, LGPL, ISC, ICU and public-domain components.

The repository additionally includes the `planetiler-openmaptiles` submodule under BSD-3-Clause, while the OpenMapTiles cartography/schema design carries CC-BY 4.0 attribution requirements.

Generated and bundled map data is a separate licensing layer. The notice identifies, among others:

- OpenStreetMap-derived data: ODbL;
- Natural Earth: public domain;
- OSM water/lakeline-derived datasets with OSM attribution obligations;
- Wikidata translations: CC0;
- Overture Maps data: source-specific/various attribution terms.

Therefore, copying Planetiler source under Apache-2.0 does **not** grant blanket rights to redistribute every generated basemap or bundled source dataset without preserving its own attribution/license obligations.

No upstream source or map data was copied into GitHub Gold.

## Gold score

Provisional score: **29 / 30 — S tier**

- Utility: **5/5** — complete raw-geodata→vector-tile archive generation pipeline with PMTiles/MBTiles outputs.
- Working Evidence: **5/5** — multi-OS/JDK CI, unit/build verification, example project execution, quickstart/JAR/Docker real-fixture generation and archive verification.
- Reusability: **5/5** — Apache-2.0 core, standalone JAR/Docker, Maven/Gradle library, Java profiles and YAML configuration.
- Novelty: **5/5** — single-machine planet-scale tiling pipeline with disk-backed external sorting and specialized geometry/tile batching optimizations.
- Documentation: **5/5** — README, dedicated architecture document, benchmark logs, examples, quickstart and clear library/custom-map guidance.
- Maintenance: **4/5** — active 2026 development and dependency maintenance, but latest stable release is March and latest observed source commit is August rather than September.

## Verification performed in this run

Inspected directly:

- current GitHub Gold PR/branch state to avoid duplicate or parallel work;
- Planetiler repository metadata and non-archived status;
- root README and documented requirements/usage;
- `ARCHITECTURE.md` pipeline design;
- current Maven CI workflow;
- root Apache-2.0 license;
- `NOTICE.md` third-party/adapted-code and dataset licensing boundaries;
- latest stable GitHub release metadata and GitHub-provided digest information;
- recent repository commits through 2026-08-05.

## Verification boundary

I did **not**:

- build Planetiler;
- run Maven tests or Spotless;
- run the quickstart or Docker image;
- download OSM/Natural Earth/Overture data;
- generate MBTiles or PMTiles locally;
- independently verify the Monaco fixture output;
- reproduce any planet-scale benchmark;
- profile CPU, memory, disk or network behavior;
- validate geometry topology repair against real pathological inputs;
- independently hash the release JAR;
- verify Maven artifact signatures/provenance;
- audit parsers or decompression paths for security vulnerabilities;
- validate every third-party license or generated-map redistribution scenario.

Claims above are limited to direct source/document/workflow/release/history inspection and explicitly identified upstream evidence.

## Risks and limitations

- Planet-scale builds remain hardware-intensive even though the architecture is optimized for a single machine.
- Data generation can require substantial temporary SSD capacity relative to the input PBF size.
- Output correctness depends on profile/schema logic and source-data quality, not only the core engine.
- Geometry repair and high-zoom/complex building processing can be expensive.
- Map-data and OpenMapTiles schema attribution obligations are separate from the Apache-2.0 engine license.
- CI uses several mutable major-version GitHub Action references rather than immutable SHAs.
- A successful published build is not evidence of fully reproducible builds or independently verified artifact provenance.
- Large downloads in `--download` workflows introduce external availability/integrity assumptions that should be examined separately for high-assurance offline pipelines.

## Strongest follow-up leads

1. Inspect Planetiler's PMTiles archive writer and compare its output invariants against `protomaps/PMTiles` and `go-pmtiles verify`.
2. Audit `ExternalMergeSort`, disk chunk format and crash/restart behavior as a reusable large-data processing primitive.
3. Inspect `TiledGeometry`, antimeridian wrapping and polygon-repair test corpus for malformed/pathological geometries.
4. Evaluate `planetiler-custommap` YAML expression/schema engine as a standalone low-code geospatial transformation component.
5. Inspect source-download integrity/caching behavior for Geofabrik, Natural Earth, Overture and other automatic inputs.
6. Evaluate Protomaps Basemaps and `planetiler-openmaptiles` as schema/profile layers on top of the core engine.
7. Build a future end-to-end evidence chain: small OSM fixture → Planetiler PMTiles output → `go-pmtiles verify` → MapLibre local rendering, with exact hashes and resource measurements.
