# Organic Maps — privacy-first offline navigation and field-mapping stack

- Upstream: https://github.com/organicmaps/organicmaps
- Project: Organic Maps
- Research date: 2026-09-05
- Category: offline systems / mapping / navigation / OpenStreetMap / mobile / field infrastructure / geospatial
- Evidence level: VERIFIED
- Provisional Gold score: S / 28
- Source-code license: Apache-2.0, with separate licensing/attribution requirements for compiled map data and other bundled assets
- Primary implementation: C++ core with Android and iOS platform layers
- Discovery source: GitHub-first rotation into emergency/field and offline infrastructure

## Executive finding

`organicmaps/organicmaps` is a mature privacy-first offline maps and GPS application built around OpenStreetMap data. It supports offline map storage, fast offline search, turn-by-turn routing, hiking/cycling/driving navigation, contour/elevation data, public transport, bookmarks/tracks, and KML/KMZ/GPX/GeoJSON interchange.

For GitHub Gold, the most valuable aspect is not simply the finished mobile app. The repository contains a substantial reusable offline geospatial stack: compact `.mwm` map data, map download/update storage management, offline search and routing engines, rendering, elevation/terrain support, track/bookmark interchange, OSM editing, and platform bindings for Android/iOS.

## Why it matters

Offline navigation is unusually valuable for field, travel, emergency, privacy-sensitive, and low-connectivity environments. A practical implementation has to solve several difficult problems together: compact regional map packaging, interrupted download/update handling, offline indexing and search, graph routing, map rendering, GPS/navigation state, localization, map-data freshness, and safe migration between map versions.

Organic Maps provides production implementations of these concerns rather than only a format or SDK demonstration. The root README explicitly documents offline maps, offline search, turn-by-turn navigation, public transport, contour/elevation data, Wikipedia content, and track/bookmark interchange.

## Reusable component families

### Storage and map-download subsystem

`libs/storage/` contains the map storage/download manager. `storage.hpp` exposes country/region state and aggregate download progress; `storage.cpp` handles map download/update flow. The repository also has dedicated `storage_tests` and `storage_integration_tests` covering download behavior, grouped downloads, HTTP paths, size calculation, and map-state transitions.

A useful current invariant appears directly in `storage_download_tests.cpp`: an up-to-date map already present on disk is not re-downloaded when `Storage::DownloadNode` is called.

This subsystem is valuable as a reference for resumable regional dataset management and offline content lifecycle handling.

### Compact `.mwm` offline map datasets

Organic Maps packages processed map content into `.mwm` files and related binary datasets. These are the operational offline assets consumed by search, routing, rendering, and navigation.

The binary data is **not** licensed identically to the Apache-2.0 source tree. `DATA_LICENSE.txt` identifies Organic Maps `.mwm` and `packed_polygons.bin` files as Produced Works derived from OpenStreetMap and other sources and imposes explicit attribution conditions. This distinction must remain visible in any catalog/reuse decision.

### Offline search, routing, and navigation

The application performs map search and route computation without requiring an online service after the relevant regional data is installed. The repository contains routing and search subsystems plus Android/iOS integration paths that connect route state to map-download requirements where necessary.

This makes the project useful for disconnected field applications where a remote routing/search API is unacceptable or unavailable.

### Import/export and user-controlled field data

The root feature set supports bookmarks and tracks through KML, KMZ, GPX, and GeoJSON. That is useful for interoperable field workflows because the application does not require all user-created geospatial information to remain trapped in a proprietary cloud account.

## Working evidence

Working evidence is strong and substantially exceeds README claims.

The current CMake workflow builds Debug and Release configurations on Ubuntu and macOS with multiple current GCC/Clang toolchains. It runs the repository's CTest suite and separate offscreen rendering tests. The workflow explicitly documents that storage integration tests which download real maps are excluded from the normal CI path because they require roughly 690 MB and around 28 minutes, while offline storage coverage remains in `storage_tests`.

Android CI separately:

- runs Android Lint;
- builds WebDebug and F-Droid variants;
- builds a Wear OS target;
- starts an Android emulator;
- executes app, SDK, Wear, protocol, and connected Android tests;
- publishes built APK artifacts for the workflow.

This is direct build/test evidence across the shared native core and Android application layers.

## Release and maintenance evidence

The latest stable GitHub release inspected is **2026.08.27-18-android**, published **2026-08-27**. It includes an Android APK plus an explicit `.sha256sum` file, while GitHub's release metadata also supplies a SHA-256 digest for the APK. The release notes state that its OSM data snapshot is from **2026-08-26**.

Development remains highly active through **2026-09-05**. Recent commits include Android Auto service work, iOS rendering/appearance fixes, removal of an unused ~50k-line AGG dependency and obsolete chart subsystem, bookmark localization fixes, and safer failure handling when creating new map POIs during map updates/removals.

## Supply-chain/build caveats

The CI is broad, but inspected workflows use version tags such as `actions/checkout@v6`, `actions/upload-artifact@v7`, `reactivecircus/android-emulator-runner@v2`, and `hendrikmuhs/ccache-action@v1.2` rather than immutable commit SHAs. This is weaker than strict SHA-pinned GitHub Actions supply-chain hygiene.

The repository also has a large submodule/third-party dependency surface and a very large data/tooling footprint, so reproducing a full build is materially more involved than compiling a small library.

## Licensing

The root source code is licensed under **Apache-2.0** and the repository uses REUSE metadata for licensing hygiene.

However, compiled map/data files are separately governed. `DATA_LICENSE.txt` identifies `.mwm`, `packed_polygons.bin`, and related binary files as processed works containing OpenStreetMap, Wikipedia, elevation, postcode, and other source datasets. Redistribution requires specific visible attribution, and the project states that white-labeling/rebranding requires written permission.

No Organic Maps source or binary data was copied into GitHub Gold.

## Gold score

Provisional score: **28 / 30 — S tier**

- Utility: **5/5** — directly useful offline navigation for travel, hiking, emergency, field, and privacy-sensitive use.
- Working Evidence: **5/5** — active releases, cross-platform native builds, Android builds/emulator tests, linting, storage tests, and rendering tests.
- Reusability: **4/5** — strong reusable subsystems, but the integrated architecture, platform layers, data pipeline, and data-license requirements complicate extraction.
- Novelty: **4/5** — offline maps/routing are established concepts, but the breadth and integration quality are unusually valuable.
- Documentation: **5/5** — install/contribution/governance docs, feature documentation, license/NOTICE/REUSE metadata, and explicit binary-data licensing.
- Maintenance: **5/5** — fresh August 2026 release and active development through September 5, 2026.

## Verification performed in this run

Inspected directly:

- repository metadata and archival state;
- root README and documented feature surface;
- Apache-2.0 root license;
- separate binary-data license;
- native CMake CI matrix and test exclusions;
- Android lint/build/emulator-test workflow;
- `libs/storage` download/update implementation locations and storage unit/integration tests;
- latest GitHub release metadata and published SHA-256 information;
- recent commit history through 2026-09-05;
- existing GitHub Gold research branch to avoid duplication.

## Verification boundary

I did **not**:

- compile Organic Maps;
- install or run the Android/iOS applications;
- execute CTest, Android unit tests, or emulator tests;
- download or generate `.mwm` maps;
- test offline routing/search accuracy;
- exercise interrupted downloads, map updates, or recovery locally;
- validate OSM editing against production services;
- independently hash the release APK;
- audit map/style/data parsers for security issues;
- benchmark battery, routing, rendering, or storage performance.

Claims above are limited to direct source/workflow/release/history inspection and clearly identified upstream evidence.

## Risks and limitations

- Source-code licensing and map-data licensing are distinct; Apache-2.0 alone does not describe reuse of distributed `.mwm` datasets.
- The application and data-generation ecosystem are large and complex, with significant third-party/submodule dependencies.
- Map correctness and route quality depend on upstream OpenStreetMap and processed data quality.
- Some storage integration tests requiring live map downloads are intentionally excluded from normal CI because of runtime/data cost.
- Version-tagged GitHub Actions are weaker supply-chain controls than immutable SHA-pinned actions.
- Offline operation still requires users to obtain and periodically refresh relevant regional datasets.

## Strongest follow-up leads

1. Trace `.mwm` format generation and versioning, including compatibility checks between app and map-data revisions.
2. Inspect the offline search index and ranking pipeline as a reusable embedded geospatial-search component.
3. Map the routing graph, cross-region routing, elevation weighting, and turn-instruction pipeline.
4. Inspect downloader integrity checks, partial-download recovery, update application, and storage cleanup invariants.
5. Evaluate the map generator and planet-data processing tooling as a separate Gold component family.
6. Inspect GPX/KML/KMZ/GeoJSON import/export implementation and malformed-input handling.
7. Compare Organic Maps with OsmAnd and CoMaps specifically on offline architecture, licensing, test evidence, and low-connectivity field use.