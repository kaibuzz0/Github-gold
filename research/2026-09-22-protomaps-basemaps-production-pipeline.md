# Protomaps Basemaps — OSM/Natural Earth to PMTiles production pipeline

- **Repository:** https://github.com/protomaps/basemaps
- **Author / Org:** Protomaps
- **Category:** offline maps / geospatial / vector tiles / cartography / data pipeline / MapLibre
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 4
  - Documentation: 5
  - Maintenance: 5
- **Discovery:** Recursive follow-up from the verified PMTiles and go-pmtiles dossiers.

## What it is

`protomaps/basemaps` is an end-to-end open basemap production stack. It combines a Planetiler build profile that turns OpenStreetMap plus Natural Earth and other open datasets into a PMTiles basemap, a TypeScript style package for MapLibre, and a browser application for inspecting/downloading builds.

The upstream README states that its `tiles/` profile can generate `planet.pmtiles` from OpenStreetMap and Natural Earth in roughly **2–3 hours on a modest computer**. This is an upstream performance claim, not a GitHub Gold benchmark.

## Concrete reusable components

- `tiles/` — Java/Planetiler basemap generation profile.
- Layer implementations for water, earth, landuse, boundaries, places, transit and other map features.
- Name/script handling and locale-specific road/network normalization.
- QRank-backed POI generalization support.
- `styles/` — TypeScript package that generates MapLibre GL styles across multiple themes and can be consumed through npm or exported to JSON.
- `app/` — browser frontend for viewing/downloading generated basemap builds.
- Companion `protomaps/basemaps-assets` repository for downloadable fonts and sprites.

The architecture is valuable because it covers the full path from raw/open geodata through vector-tile production to a browser-renderable map rather than supplying only one isolated stage.

## Build/runtime path

Upstream development instructions require **Java 21+** and Maven. The documented local workflow compiles the `tiles` JAR with Maven, then can use Planetiler's download/area machinery to generate a regional PMTiles file (the README uses Monaco as the example). The browser application uses Node/npm tooling and can load the locally generated archive.

## Working evidence

The repository contains a JUnit test suite rather than relying only on documentation. Inspected code-search evidence includes a `BasemapTest` integration test plus tests for layer behavior, scripts/names, locale-specific network handling, water, earth, places, landuse and other processing logic.

GitHub Gold did **not** execute these tests. Their presence and inspected test declarations are repository-native upstream evidence only.

Maintenance is current: commits observed in 2026 include migration away from a deprecated Planetiler Natural Earth API, locale-safe coordinate parsing, MapLibre GL v6 upgrades, dependency updates and a September 11, 2026 update to current basemap dependencies/source locations.

## Licensing and attribution

- Repository software: **BSD-3-Clause**.
- Basemap visual design: **CC0**.
- Tile schema includes adaptations from Tilezen under the notices documented in `LICENSE.md`.
- Generated tilesets based on OpenStreetMap are treated as Produced Works under the **ODbL** and require visible OpenStreetMap attribution in web/native map use.
- Natural Earth and any additional datasets have their own provenance/attribution conditions; the repository points to `LICENSE_DATA.md` for dataset-level details.
- Some styles can include MIT-licensed Mapzen/Tangram icon derivatives.

This distinction matters: permissive code licensing does **not** erase map-data attribution obligations.

No upstream implementation code was copied into GitHub Gold.

## Why it matters for GitHub Gold

This project provides a reproducible bridge between open geographic source data and the already-verified PMTiles offline/static-delivery ecosystem. High-value uses include:

- self-generated regional or planet-scale basemaps;
- offline/emergency map packages;
- self-hosted maps without a proprietary tile API;
- reusable Planetiler feature/layer processing patterns;
- customizable MapLibre style generation;
- multilingual/name-processing research;
- local-first mapping stacks paired with `go-pmtiles` regional extraction and serving.

The strongest component is not a single function but the composable pipeline: **OSM/Natural Earth → Planetiler profile → PMTiles → MapLibre styles/app**.

## Caveats

- The README's 2–3 hour planet-build statement is an upstream claim and depends heavily on machine, storage, memory, network and source-data conditions.
- A full planet build is materially heavier than the small-area example and should not be assumed suitable for low-resource Android/Termux hardware.
- Generated map data has licensing/attribution requirements distinct from the BSD source code.
- Data freshness depends on the source snapshot/build process; PMTiles packaging itself does not make the underlying map current.
- Styling, tile generation and asset hosting are separate moving parts even though they live in one ecosystem.
- GitHub Gold did not build the JAR, download OSM/Natural Earth data, generate a PMTiles archive, run the frontend, render a map or benchmark the pipeline.

## Verification performed

Inspected repository metadata, README/build instructions, code organization, core `Basemap`/layer search results, repository-native test locations, license text and recent commit history. Verification is source/repository evidence only; no local execution was performed.

## Strongest next leads

1. **felt/tippecanoe** — compare its high-volume vector-tile generation model with Planetiler and identify complementary use cases.
2. **onthegomap/planetiler** — inspect the underlying tile-production engine separately; it may merit its own high-value dossier independent of Protomaps.
3. **protomaps/basemaps-assets** — evaluate whether its fonts/sprites provide a clean fully offline rendering bundle and document licensing per asset.
4. Rotate into another technical category after one of these leads to preserve catalog breadth.

## Verdict

**VERIFIED / S / 29.** Protomaps Basemaps is a high-value open geospatial production pipeline: permissively licensed software, repository-native tests, active 2026 maintenance, reusable Planetiler processing logic, style generation, and direct integration with the PMTiles static/offline map stack. Its main operational caveat is that software licensing and generated-map data licensing must be tracked separately.