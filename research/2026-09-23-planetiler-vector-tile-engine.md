# Planetiler — high-throughput vector-tile generation engine

- **Repository:** https://github.com/onthegomap/planetiler
- **Author / Org:** onthegomap
- **Category:** geospatial / vector tiles / data pipeline / offline maps / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 4
  - Documentation: 5
  - Maintenance: 5
- **Discovery:** Recursive follow-up from the verified Protomaps Basemaps pipeline.

## What it is

Planetiler is a Java-based vector-tile generation engine designed to turn large geographic datasets such as OpenStreetMap into standard Mapbox Vector Tiles. It can package output directly as MBTiles or PMTiles, making it a production engine beneath multiple open basemap stacks rather than a Protomaps-specific component.

Upstream explicitly aims to build a world map in a few hours on one machine without an external database. That is an upstream performance objective/claim, not a GitHub Gold benchmark.

## Concrete reusable components

- High-throughput input → feature mapping → tile-ID sorting → vector-tile output pipeline.
- Direct MBTiles and PMTiles output.
- OpenStreetMap PBF ingestion and automated source downloads.
- Declarative YAML custom-map profiles for users who do not need to write Java.
- Java profile API for advanced feature, attribute, geometry and zoom processing.
- `planetiler-custommap` module and sample configurations.
- Docker distribution in addition to the standalone JAR.
- Architecture reusable by external basemap projects including Protomaps Basemaps and OpenMapTiles.

A particularly useful design point is that simple overlays/custom maps can be expressed in YAML while complex production pipelines can drop down to Java profiles. This gives the same engine both low-friction configuration and full programmable control.

## Runtime / resource path

Current upstream instructions require Java 21+ or Docker. For an OpenMapTiles-profile build, the README recommends at least 1 GB free SSD plus roughly 5–10x the input `.osm.pbf` size in working disk and approximately 0.5x the PBF size in free RAM. These are upstream guidance rather than GitHub Gold measurements.

The documented quick-start can download a release JAR and generate a Monaco extract. PMTiles output is selected simply by using an output filename ending in `.pmtiles`.

## Working evidence

Planetiler has a substantial repository-native JUnit test tree. Inspected search results include tests for YAML loading/merging, compression round trips, varint encoding, statistics/timing utilities and examples documenting both unit and integration tests. GitHub Gold did **not** execute these tests.

The project publishes release artifacts. The latest inspected release is **v0.10.2**, published **2026-03-29**, with a downloadable `planetiler.jar` and checksum artifacts. That release added zoom-level 16 support, STAC-based selective Overture downloading, and additional example profiles.

Maintenance is current beyond the release: the default branch received dependency updates through **2026-09-22**, including protobuf 4.36.2, with additional September 2026 Java/build dependency maintenance.

## Licensing

Planetiler is licensed under **Apache License 2.0**. No upstream implementation source was copied into GitHub Gold.

Input datasets and generated-map attribution remain a separate concern. OpenStreetMap, Natural Earth, Overture, OpenMapTiles schemas and other sources/profiles can impose their own attribution or licensing obligations. The Apache software license must not be mistaken for a blanket license over source geodata or generated datasets.

## Why it matters for GitHub Gold

Planetiler is the reusable production engine beneath the previously verified Protomaps Basemaps stack. Its Gold value is broader than any single basemap:

- build offline/self-hosted regional vector maps;
- create custom overlays without a spatial database;
- output PMTiles for static/range-addressed delivery;
- output MBTiles for conventional SQLite tile workflows;
- prototype declaratively in YAML and move to Java when processing becomes complex;
- study high-throughput external sorting and geometry/tile processing architecture;
- compose with MapLibre, PMTiles, Protomaps Basemaps and other open geospatial systems.

## Caveats

- Planet-scale generation remains compute/storage intensive even though the engine is optimized for a single machine.
- The world-map-in-hours statement is upstream positioning and hardware/workload dependent; GitHub Gold did not benchmark it.
- The default OpenMapTiles quick-start can download substantial auxiliary datasets even for a small region unless alternate small test sources are supplied.
- Java 21+/JVM resource requirements make the full production path a poor assumption for constrained Android/Termux devices.
- Software licensing and source-data/output attribution must be tracked separately.
- GitHub Gold did not run the JAR, Docker image, Maven build, tests, downloads, tile generation, rendering, or performance benchmarks.

## Verification performed

Inspected repository metadata, README/runtime documentation, current license, repository-native test search results, latest release metadata/artifacts, and recent default-branch commit history. Verification is repository/source evidence only.

## Strongest next leads

1. **felt/tippecanoe** — compare its GeoJSON-focused vector-tile generation and density/generalization model with Planetiler.
2. **planetiler-custommap** — deeper component-level analysis of the YAML expression/configuration engine if a reusable declarative geoprocessing primitive is needed.
3. Rotate into a non-mapping category after Tippecanoe to maintain catalog breadth.

## Verdict

**VERIFIED / S / 29.** Planetiler is a mature, actively maintained, permissively licensed vector-tile production engine with direct PMTiles/MBTiles output, declarative and programmable profile systems, release artifacts, extensive repository-native tests, and proven reuse by multiple basemap ecosystems. Its main caveats are resource intensity at planet scale and the need to track geodata licensing independently from the Apache-2.0 code.