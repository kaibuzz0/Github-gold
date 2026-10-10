# Tippecanoe — large-dataset vector-tile generation and generalization toolkit

- **Repository:** https://github.com/felt/tippecanoe
- **Author / Org:** Felt; actively maintained by Erica Fischer; historical upstream from Mapbox
- **Category:** geospatial / vector tiles / data processing / offline maps / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 4
  - Documentation: 5
  - Maintenance: 5
- **Discovery:** Recursive follow-up from Planetiler and the PMTiles/Protomaps mapping toolchain.

## What it is

Tippecanoe is a C++ command-line toolkit for building vector tilesets from large or small collections of GeoJSON, FlatGeobuf, or CSV features. Its central design goal is scale-independent visualization: preserve the density and texture of a dataset across zoom levels instead of reducing low zooms to only a few supposedly important features.

The primary CLI writes MBTiles and accepts files or streamed GeoJSON on standard input. The repository also includes companion utilities such as `tile-join`, decoding/inspection tools, overzoom processing, JSON tooling, and filtering/attribute machinery.

## Concrete reusable capabilities

- GeoJSON, FlatGeobuf, and CSV ingestion.
- Streaming GeoJSON input rather than requiring a monolithic FeatureCollection.
- Automatic maxzoom selection with `-zg`.
- Density-aware feature dropping when tiles exceed practical size.
- Coalescing of dense polygon features.
- Zoom extension when high-zoom tiles still need feature dropping.
- Point clustering with attribute accumulation such as sums.
- Multi-layer and merged-layer generation from multiple sources.
- `tile-join` composition/filtering for merging tilesets and selectively replacing data.
- Feature filtering and attribute control.
- Variable-depth tile pyramids and overzoom/deduplication machinery.
- Large-data sorting paths including an external/radix path for constrained memory situations.

This makes Tippecanoe particularly valuable for arbitrary observational or analytical datasets—GPS traces, points, boundaries, buildings, events, measurements—where the problem is not simply converting a basemap schema but deciding how dense source geometry should survive across zoom levels.

## Planetiler comparison

Tippecanoe and Planetiler overlap but are not substitutes in every workflow.

**Tippecanoe** is especially direct for existing GeoJSON/FlatGeobuf/CSV datasets and exposes extensive command-line controls for density, clustering, coalescing, filtering, zoom behavior, and tileset composition.

**Planetiler** is stronger as a programmable source-to-schema production engine: OSM PBF and other source ingestion, declarative YAML profiles, Java profiles, and direct MBTiles/PMTiles generation.

A practical stack can use both: Planetiler for repeatable basemap/source processing and Tippecanoe for custom overlays, arbitrary feature collections, density-aware visualization, or post-production composition.

## Working evidence

The repository has a broad regression-test corpus covering many independent behaviors. The inspected `tests/` tree includes dedicated cases for accumulation, attributes, CSV, dateline handling, EPSG:3857, feature filters, FlatGeobuf, geometry, coalescing and numerous historical crash/regression cases.

Recent upstream commits provide unusually concrete maintenance evidence. August 2026 work fixed and added regression coverage for radix-sort corruption/recursion failures, variable-depth pyramid consistency, compiler-warning-exposed integer/initialization defects, JSON parser ownership and Unicode bugs, and documentation reproducibility. Several commit messages explicitly document tests that fail under the previous implementation and pass after the fix.

GitHub Gold did **not** execute these tests; this is upstream repository-native evidence.

## Maintenance and releases

The repository is unarchived and actively maintained. The newest inspected default-branch commit is from **2026-08-14** and includes a substantial JSON parser ownership/performance rewrite plus regression tests and bug fixes.

The latest GitHub Release object inspected is **2.79.0**, published **2025-07-24**. Default-branch development has advanced beyond that release: August 2026 commits include changelog/version preparation for 2.81.0. This distinction matters—current source activity is newer than the latest published GitHub Release.

## Licensing

The repository's `LICENSE.md` is a permissive BSD-style license requiring preservation of copyright/license notices in source and binary redistribution. It carries copyright notices for Protomaps LLC and Mapbox Inc.

No upstream implementation source was copied into GitHub Gold. Input datasets and generated tiles can carry separate licensing/attribution requirements; the software license does not grant rights to source geodata.

## Runtime / platforms

Upstream documents Homebrew installation on macOS and source builds on Ubuntu using `make`; the project is primarily C++. Practical use of the command-line tools is desktop/server oriented. Large datasets can require substantial temporary storage, CPU, and memory even though the implementation contains external/radix sorting and density-management mechanisms intended to keep large jobs tractable.

## Why it matters for GitHub Gold

Tippecanoe is Gold because it is more than a format converter. It exposes mature, reusable strategies for converting dense real-world feature collections into multiscale vector representations:

- turn large GPS/event/sensor datasets into navigable offline tiles;
- preserve visual density at low zooms without blindly retaining every feature;
- cluster points while aggregating attributes;
- merge, filter, replace, and compose independently generated tilesets;
- process streaming feature data;
- study practical geometry simplification, tile-size pressure, external sorting, deduplication and variable-depth pyramid behavior;
- pair custom overlays with PMTiles/MapLibre/Protomaps/Planetiler workflows.

## Caveats

- The primary documented output path is MBTiles; PMTiles-native production is a stronger fit for Planetiler/go-pmtiles when single-file range-addressed archives are the target.
- The option surface is very large. High-quality output requires understanding the tradeoffs among dropping, coalescing, clustering, simplification, tile-size limits, zoom selection and attribute retention.
- Density-preserving visualization is a design objective, not a guarantee that every analytical use preserves statistically meaningful semantics after feature dropping/generalization.
- Large jobs remain resource intensive.
- The latest GitHub Release is older than current default-branch development, so release users and source users may observe different feature/fix sets.
- GitHub Gold did not compile Tippecanoe, run `make`, execute tests, generate tiles, decode outputs, or benchmark memory/CPU behavior.

## Verification performed

Inspected repository metadata, README and documented examples, license, current test tree, latest GitHub Release metadata, and recent default-branch commits. Verification is repository/source evidence only.

## Strongest next leads

1. Rotate out of mapping as planned; the PMTiles → go-pmtiles → Protomaps Basemaps → Planetiler → Tippecanoe chain is now sufficiently mature.
2. Search a different high-value category such as local-first/offline data synchronization, embedded observability, scientific tooling, or user-controlled automation.
3. Revisit Tippecanoe only when a materially new release lands or a specific reusable subcomponent warrants a focused dossier.

## Verdict

**VERIFIED / S / 29.** Tippecanoe is a mature, actively maintained, permissively licensed vector-tile toolkit with unusually deep controls for density-aware generalization, clustering, filtering, composition and large-dataset processing. Repository-native regression coverage and current bug-fix activity support a high working-evidence score. Its strongest niche relative to Planetiler is direct transformation of arbitrary feature datasets and fine-grained multiscale visualization control.