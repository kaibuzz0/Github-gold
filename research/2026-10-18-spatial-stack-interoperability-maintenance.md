# FlatGeobuf + DuckDB Spatial — geospatial research and interoperability

**Date:** 2026-10-18  
**Source:** GitHub-first; no YouTube transcript evidence.  
**Evidence:** VERIFIED from upstream source/test/CI; neither project was independently installed, executed, built, benchmarked or security-audited.  
**Gold scores:** FlatGeobuf S/29 (5/5/5/4/5/5); DuckDB Spatial S/27 (5/4/5/4/4/5), ordered Utility, Working Evidence, Reusability, Novelty, Documentation, Maintenance.

## Architecture and component evidence

**FlatGeobuf** — https://github.com/flatgeobuf/flatgeobuf — uses FlatBuffers and an optional packed Hilbert R-tree for static geographic vector features. It supports streaming and HTTP byte-range bounding-box reads, but not random in-place writes. Reusable code: `src/ts/http-reader.ts` (range client), `src/ts/packedrtree.ts` (R-tree search), `src/ts/packedrtree.spec.ts` (regression tests), `src/ts/seekable-zstd.ts` (seekable compression), `src/ts/geojson.ts` (GeoJSON), `src/fbs/header.fbs` and `feature.fbs` (wire schemas), plus Rust and Go implementations. Upstream `.github/workflows/test.yml` defines a cross-language test matrix; this review did not execute it. TypeScript root package metadata reports 4.6.0 and Rust crate metadata reports 6.0.1; these are package versions, not confirmed GitHub releases.

**DuckDB Spatial** — https://github.com/duckdb/duckdb-spatial — is a spatial SQL extension. The source contains `src/spatial/index/rtree/` (index), `src/spatial/modules/gdal/` (file I/O), `mvt/` (vector tiles), `osm/` (OpenStreetMap PBF), `proj/` (CRS transforms), `geos/` (geometry operations). `test/sql/index/rtree_basic.test` creates an RTREE index and asserts an `RTREE_INDEX_SCAN` explain plan. `test/sql/mvt/st_asmvt.test` contains vector tile output tests. This is evidence from test source, not proof the tests passed during this review.

## Maintenance findings

- FlatGeobuf upstream commit `543346d6002384e11484d57c3a56384f170a1c73` (2026-10-07) modifies `packedrtree.ts` and its regression tests to address index boundary and duplicate-result cases: https://github.com/flatgeobuf/flatgeobuf/commit/543346d6002384e11484d57c3a56384f170a1c73
- DuckDB Spatial upstream commit `4e066c17e2d1f24625baff4c62430d68ceb4e41f` (2026-10-18) corrects a malformed GDAL JSON patch. This is maintenance evidence, not a security fix or a confirmed release: https://github.com/duckdb/duckdb-spatial/commit/4e066c17e2d1f24625baff4c62430d68ceb4e41f
- DuckDB Spatial README says spatial indexing is unsupported, while current R-tree source and SQL tests exist. Treat as a documentation/version discrepancy, not a guarantee of universal support. Upstream describes geometry storage as work in progress.

## Licenses and constraints

FlatGeobuf root LICENSE declares BSD-2-Clause, root package.json declares BSD-3-Clause, `src/ts/LICENSE` contains ISC, and Rust Cargo.toml declares BSD-2-Clause. These may reflect component-level notices; do not assume one license applies to every file. No source copied. HTTP Range and CORS configuration affect remote filtering.

DuckDB Spatial root LICENSE is MIT; its bundled GDAL/GEOS/PROJ and other third-party dependencies require separate notice review. Pin matching DuckDB/extension builds. Do not assume Android binaries or all experimental features are available.

## Composition and next tests

Potential workflow: use FlatGeobuf for static indexed feature storage and bbox retrieval, DuckDB Spatial for SQL/geometry transformations and MVT creation, then PMTiles/MapLibre for distribution and rendering. This architecture is a research hypothesis, not an independently verified end-to-end pipeline. Next: pin versions; compare FlatGeobuf import feature counts and geometry round trips; test R-tree persistence/query plans; measure HTTP requests, bytes, latency and peak memory; produce MVT tiles and test rendering; audit file-level licenses.

## Primary sources

- FlatGeobuf README/spec: https://github.com/flatgeobuf/flatgeobuf
- FlatGeobuf TS index test: https://github.com/flatgeobuf/flatgeobuf/blob/master/src/ts/packedrtree.spec.ts
- FlatGeobuf CI: https://github.com/flatgeobuf/flatgeobuf/blob/master/.github/workflows/test.yml
- FlatGeobuf root license: https://github.com/flatgeobuf/flatgeobuf/blob/master/LICENSE
- FlatGeobuf TypeScript license: https://github.com/flatgeobuf/flatgeobuf/blob/master/src/ts/LICENSE
- FlatGeobuf Rust manifest: https://github.com/flatgeobuf/flatgeobuf/blob/master/src/rust/Cargo.toml
- DuckDB Spatial R-tree SQL test: https://github.com/duckdb/duckdb-spatial/blob/v2.0-cyanoptera/test/sql/index/rtree_basic.test
- DuckDB Spatial MVT SQL test: https://github.com/duckdb/duckdb-spatial/blob/v2.0-cyanoptera/test/sql/mvt/st_asmvt.test
- DuckDB Spatial CI: https://github.com/duckdb/duckdb-spatial/blob/v2.0-cyanoptera/.github/workflows/MainDistributionPipeline.yml
- DuckDB Spatial license: https://github.com/duckdb/duckdb-spatial/blob/v2.0-cyanoptera/LICENSE
