# Organic Maps — privacy-first offline navigation and mapping engine

- **Repository:** https://github.com/organicmaps/organicmaps
- **Organization:** Organic Maps
- **Category:** offline maps / navigation / OpenStreetMap / routing / geospatial / local-first / mobile
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **Primary languages:** C++ core with Android/Kotlin/Java, iOS/Swift/Objective-C, Python/build tooling, Qt desktop surfaces
- **Source-code license:** Apache-2.0 at repository root; NOTICE/REUSE metadata and third-party component notices must be preserved
- **Binary map/data license:** separate Organic Maps Binary Data License with upstream OpenStreetMap/ODbL, Wikipedia/CC BY-SA and other data-source obligations
- **Discovery source:** GitHub-first category rotation into mapping/offline navigation
- **Inspection date:** 2026-09-11

## Executive finding

Organic Maps is a privacy-first offline map and GPS/navigation application built on OpenStreetMap data. It supports downloadable regional maps, offline search, turn-by-turn walking/cycling/driving navigation, hiking and cycling trails, elevation/contour information, public-transport map data, bookmarks and tracks, and KML/KMZ/GPX/GeoJSON import/export.

For GitHub Gold, the value is broader than the end-user app. The repository contains a large reusable geospatial stack: map generation and compact map storage, search, routing, rendering, elevation, bookmark/track handling, OSM editing, platform abstraction, mobile clients, a Qt desktop application, tests, build/release automation, and data-generation tooling.

The project is particularly relevant to local-first and emergency/off-grid use because core map viewing, search, and navigation are designed to work without a persistent network connection once map data is downloaded.

## Why it matters

Offline navigation is a difficult systems problem spanning geospatial data ingestion, compression, indexing, rendering, routing graphs, search, localization, GPS/location handling, mobile lifecycle behavior, and update delivery. Organic Maps packages those concerns into a mature open-source system rather than relying on a hosted map API for every query.

High-value uses and study areas include:

- offline navigation on phones where cellular service is absent, unreliable, expensive, or intentionally disabled;
- local-first travel, hiking, cycling and emergency-reference workflows;
- OpenStreetMap data processing and region generation;
- compact map-file design and incremental map distribution;
- offline geocoding/search and category search;
- pedestrian, bicycle and automobile routing;
- route/elevation visualization;
- bookmark, track and GPX/KML/GeoJSON interoperability;
- privacy-conscious location tooling;
- cross-platform geospatial UI architecture;
- Android Auto / mobile navigation integration;
- reproducible map-generation and validation pipelines.

## High-value components and patterns

### Offline map/data pipeline

Organic Maps consumes OpenStreetMap and other geographic datasets and produces binary map data used by the clients. The repository contains generator, storage, coding and index-related components rather than treating maps as an opaque hosted service.

This makes the project useful as a reference for:

- converting large public geographic datasets into compact regional artifacts;
- type/tag normalization and backward-compatible map semantics;
- search/routing index construction;
- region packaging and download/update management;
- validating generated map data.

Recent September 2026 commits demonstrate active maintenance in the generator layer, including normalization of deprecated OSM water-area tags and fixes for deprecated vineyard/orchard/embassy mappings.

### Routing engine

The codebase includes dedicated routing infrastructure and route-quality/integration test surfaces. Organic Maps exposes walking, cycling and car navigation to users, with turn-by-turn guidance and route/elevation presentation.

Strong recursive targets include graph construction, vehicle models, turn restrictions, route weighting, altitude/elevation integration, cross-region routing, route reconstruction, and failure behavior when map regions are incomplete.

### Offline search

Fast offline search is a headline feature and the repository contains a substantial search subsystem and search-quality tests. This is a high-value area for studying compact local indexes, multilingual names, tokenization, category search, ranking, address/place matching and low-resource query execution.

### Rendering / `drape`

Organic Maps includes its own rendering infrastructure. Current CMake CI explicitly runs rendering-related test presets separately with offscreen rendering support, indicating that rendering correctness is a first-class tested subsystem rather than UI-only glue.

Useful study targets include style generation, tile/feature rendering, symbol placement, text shaping, GPU abstraction, offscreen rendering, map interaction, and performance/memory tradeoffs on mobile hardware.

### Bookmarks, tracks and interchange formats

The application supports KML, KMZ, GPX and GeoJSON import/export. Recent release work added multi-selection and per-track visibility controls.

This creates reusable examples for:

- local track storage;
- map annotations/bookmarks;
- format conversion;
- path/track rendering;
- sharing portable geographic data without a proprietary cloud account.

### OSM editing and data feedback loop

Organic Maps includes OpenStreetMap editing support, giving the project value as both a consumer and contributor to open geographic data. This creates an architectural bridge between offline map use, user edits, and upstream map data.

### Cross-platform architecture

The repository includes Android, iOS, desktop/Qt and shared native C++ code. Upstream build documentation covers Android/iOS/mobile development and a desktop build on Linux/macOS, with Windows work occurring but native Windows support described as less actively maintained.

A large shared native core with thin platform-specific clients is a useful reference for projects that need the same offline algorithms and data model across multiple UI stacks.

## Working evidence

Organic Maps has unusually strong repository-native evidence.

### CMake build and test matrix

The inspected `.github/workflows/build-cmake.yaml` compiles Debug and Release configurations across:

- Ubuntu 24.04 with Clang 19;
- Ubuntu 24.04 with GCC 14;
- Ubuntu 24.04 with GCC 13;
- macOS 26 / Xcode toolchains;
- a non-unity Linux configuration to catch build assumptions hidden by unity builds.

The workflow initializes recursive submodules, configures with CMake presets, builds the project and runs `ctest` test presets. It also runs rendering/drape tests separately with offscreen rendering support.

The workflow documents why certain large or integration-heavy suites are excluded from the normal CI preset, including generator/routing integration and real-map-download storage tests. This is useful transparency: the project has broad testing, but not every test is executed in every CI job.

### Additional workflows

The repository exposes many additional workflows covering Android checks/releases/betas, metadata validation, Android SDK packaging, appstream/desktop metadata, CMake builds, style checks and platform-specific quality gates.

GitHub Gold did not execute those workflows; their definitions were inspected as upstream evidence.

### Windows test work

A September 9, 2026 commit fixed a broad set of Windows-specific unit-test failures: portable time handling, path separator behavior, open-file deletion semantics, test fixture line endings, rendering test gating and crash/assert behavior for unattended CI. This is meaningful maintenance evidence because it improves test portability rather than merely changing UI content.

## Current release and maintenance evidence

The latest GitHub Release inspected is **`2026.08.27-18-android`, published August 27, 2026**.

The release provides an Android APK plus a `.sha256sum` file, and GitHub exposes SHA-256 digest metadata for the uploaded APK. Release notes include:

- OSM data as of August 26;
- bookmark/track multi-selection;
- individual track visibility;
- additional Wikipedia languages;
- Android Auto fixes;
- routing-stop fixes;
- opening-hours fixes;
- search-panel improvements;
- OSM-editor fixes;
- elevation-chart fixes;
- crash/freeze fixes.

Maintenance continued after that release. Recent inspected commits include:

- **2026-09-11** — generator fixes for deprecated vineyard/orchard/embassy tags;
- **2026-09-10** — normalization of legacy water-area tagging;
- **2026-09-10** — removal of obsolete experimental GTFS-in-MWM support superseded by a newer transit schedule/CDN architecture;
- **2026-09-09** — broad Windows unit-test/build portability fixes;
- **2026-09-09** — Android Wear modules rewritten in Kotlin;
- **2026-09-08** — iOS track-editor visibility support.

This is clear active-maintenance evidence.

## Install / runtime requirements

For end users, Organic Maps distributes mobile builds through major app stores, F-Droid, GitHub/Obtainium and other channels.

For source builds, upstream documentation states:

- at least 4 GB RAM generally;
- recursive submodules;
- CMake 3.22.1+ for desktop;
- Qt 6 and platform dependencies for desktop;
- about 20 GB free disk recommended for desktop development;
- Linux/macOS as the actively supported desktop build environments;
- Android and iOS have their own platform toolchains;
- native Windows builds are possible but not described as actively maintained; WSL is an alternative.

The repository is very large, and upstream explicitly documents partial/shallow clone strategies for constrained bandwidth or storage.

## Licensing and provenance boundaries

The root source code is licensed under **Apache-2.0** and the project explicitly points to `LICENSE`, `NOTICE`, `data/copyright.html` and `.reuse/dep5` for attribution and component metadata.

That does **not** mean every data artifact can be treated as Apache-2.0.

Organic Maps has a separate **Binary Data License** for `.mwm`, `packed_polygons.bin` and other compiled data. Those files incorporate data from sources including:

- OpenStreetMap under ODbL;
- Wikipedia under CC BY-SA 4.0;
- elevation datasets;
- UK postcode/open-government datasets;
- US Census TIGER data.

The binary-data license requires visible Organic Maps and OpenStreetMap attribution and places explicit conditions on redistribution/white-labeling. Therefore GitHub Gold should never copy map binaries into this repository merely because the source-code license is permissive.

The source tree also uses numerous submodules and third-party libraries. Each dependency's license and notice requirements must be reviewed before extracting or adapting component code.

No Organic Maps source, binaries, `.mwm` map data, APKs, datasets or third-party components were copied into GitHub Gold in this run.

## Security, privacy and operational boundaries

Organic Maps presents itself as privacy-first and documents no ads, tracking, mandatory registration or routine data collection. GitHub Gold treats those as upstream project claims supported by the project's architecture/documentation, not as an independent privacy audit.

Important boundaries include:

- downloaded map packages and update servers remain part of the supply chain;
- routing/search correctness depends on source map quality and generated indexes;
- offline maps can become stale and should not be treated as authoritative for hazards, closures or emergency orders;
- GPS/location accuracy is hardware- and environment-dependent;
- navigation should not replace official aviation/marine/safety systems or emergency instructions;
- user-created tracks/bookmarks can expose sensitive locations if exported or shared;
- third-party platform stores and mobile OS services have privacy/security properties outside the repository's control.

## Reusability assessment

Organic Maps receives **4/5 for Reusability**.

Positive factors:

- Apache-2.0 root source license;
- substantial shared C++ core;
- modular generator/search/routing/rendering/storage subsystems;
- documented build process;
- broad automated testing;
- standards/open-data orientation;
- file-format interoperability;
- mature mobile applications and desktop build surface.

The score is intentionally not 5/5 because:

- the codebase is very large and tightly integrated;
- many third-party submodules have independent licenses;
- compiled map data has a separate license and attribution requirements;
- extracting individual subsystems may require substantial dependency untangling;
- mobile platform integrations have their own toolchain and runtime constraints.

High-value study/reuse targets include:

1. map generator and OSM-tag normalization pipeline;
2. routing graph and vehicle-model architecture;
3. offline search/index/ranking subsystem;
4. compact `.mwm` format readers/writers and storage layer;
5. rendering (`drape`) architecture;
6. GPX/KML/KMZ/GeoJSON import/export and track handling;
7. map-region download/update management;
8. platform abstraction and location handling;
9. style generation and validation tooling;
10. OSM editing/data upload pipeline.

Prefer linking to upstream implementations instead of copying them unless a concrete integration justifies source reuse and all notices/dependency licenses have been checked.

## Verification performed by GitHub Gold

This run inspected:

- GitHub Gold current README and staged research workflow;
- open draft PR #7 and current research branch;
- duplicate search in GitHub Gold for Organic Maps;
- Organic Maps repository metadata and archive state;
- root README;
- root Apache-2.0 license;
- separate `DATA_LICENSE.txt`;
- source/build installation documentation;
- repository workflow directory;
- the principal CMake build/test workflow;
- current GitHub Release metadata and release-artifact hashes exposed by GitHub;
- recent upstream commit history through September 11, 2026.

## Verification not performed

GitHub Gold did **not**:

- build Organic Maps;
- run its unit/integration tests;
- install the Android/iOS/desktop applications;
- download or validate map regions;
- execute routing or search queries;
- compare generated routes against another engine;
- run the map generator;
- validate `.mwm` binary compatibility;
- verify map-data attribution in every application surface;
- audit privacy/network behavior dynamically;
- independently reproduce release hashes or signatures;
- test GPS, Android Auto, Wear OS or iOS integrations;
- audit all third-party dependency licenses;
- perform a security review of parsers, map packages or update infrastructure.

## Why VERIFIED

VERIFIED here means the repository contains concrete upstream evidence that the system is real, maintained and exercised:

- current production releases;
- large multi-platform application source;
- active September 2026 development;
- CMake builds across multiple compilers and operating systems;
- automated unit/test presets and dedicated rendering tests;
- additional Android/release/metadata workflows;
- documented source-build procedures;
- explicit code and data licensing;
- a mature feature surface with millions of reported installs.

It does **not** mean GitHub Gold independently validated navigation accuracy, privacy behavior or every platform build.

## Score rationale

### Utility — 5/5

Offline maps, local search and navigation are immediately useful in travel, low-connectivity, privacy-sensitive and emergency/off-grid contexts.

### Working Evidence — 5/5

Current releases, broad CI, multi-compiler CMake builds, test presets, rendering tests and platform workflows provide strong repository-native evidence.

### Reusability — 4/5

The Apache-2.0 source license and modular native core are favorable, but the project's size, submodule graph and separate data licensing create meaningful extraction/integration overhead.

### Novelty — 4/5

Offline routing/maps are an established class of software, but Organic Maps combines generator, compact data, search, routing, rendering, editing and mobile clients in a mature privacy-first open stack.

### Documentation — 5/5

The project documents build requirements, contribution paths, privacy goals, release distribution, licensing, data licensing and platform-specific setup in substantial detail.

### Maintenance — 5/5

The project had a stable release on August 27, 2026 and meaningful generator, test, transit, Android and iOS work through September 11, 2026.

## Strongest recursive leads

1. **`.mwm` format and storage subsystem** — compact layout, indexes, versioning, corruption behavior and backwards compatibility.
2. **Routing engine** — graph generation, restrictions, weighting, multimodal assumptions and route-quality tests.
3. **Offline search** — index construction, multilingual matching, ranking, categories and memory/latency characteristics.
4. **Generator pipeline** — OSM ingestion, tag normalization, region cutting, validation and reproducibility.
5. **Rendering (`drape`)** — GPU abstraction, text shaping, symbol collision, styles and offscreen test coverage.
6. **Map update/distribution architecture** — differential/full region updates, CDN behavior, integrity and rollback semantics.
7. **Transit roadmap** — inspect the newer schedule-service/CDN architecture that superseded the removed GTFS-in-MWM experiment.
8. **Track/bookmark interchange** — KML/KMZ/GPX/GeoJSON correctness and metadata preservation.
9. **OSM editor** — offline edit queueing, validation, conflict/failure behavior and upload trust boundaries.
10. **Open-source offline mapping comparison** — compare Organic Maps with OsmAnd, CoMaps, Valhalla, GraphHopper, OSRM and Marble by component rather than popularity.

## Provenance

This dossier is GitHub-first research. The six registered YouTube playlists were not required for this candidate and no video-derived technical claim is used here.

Primary inspected upstream sources:

- https://github.com/organicmaps/organicmaps
- https://github.com/organicmaps/organicmaps/blob/master/README.md
- https://github.com/organicmaps/organicmaps/blob/master/LICENSE
- https://github.com/organicmaps/organicmaps/blob/master/DATA_LICENSE.txt
- https://github.com/organicmaps/organicmaps/blob/master/docs/INSTALL.md
- https://github.com/organicmaps/organicmaps/blob/master/.github/workflows/build-cmake.yaml
- https://github.com/organicmaps/organicmaps/releases/latest
- recent `master` commit history inspected through 2026-09-11
