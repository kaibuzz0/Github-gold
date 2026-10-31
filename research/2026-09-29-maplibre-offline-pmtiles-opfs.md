# MapLibre Offline PMTiles — browser-native offline mapping via OPFS

- **Repository:** https://github.com/makinacorpus/maplibre-offline-pmtiles
- **Author / Org:** Makina Corpus
- **Category:** offline maps / MapLibre / PMTiles / PWA / browser storage
- **Evidence:** PROMISING
- **Provisional Gold score:** 24 / 30 — **A**
  - Utility: 5/5
  - Working Evidence: 3/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 3/5
- **Discovery:** GitHub-first breadth rotation; checked against Github-gold code search before addition.

## What it does

A TypeScript plugin for MapLibre GL JS that downloads PMTiles archives into the browser's Origin Private File System (OPFS), exposes them to MapLibre through a custom `offline-pmtiles://` protocol, and manages local map/style lifecycle and storage quota reporting. Upstream documents MVT and MapLibre Tile (MLT) support.

This is useful because it provides a relatively small, inspectable bridge between three composable primitives: MapLibre rendering, PMTiles single-file map archives, and browser-native persistent OPFS storage. That makes it relevant to PWAs, field tools, disaster/off-grid mapping, local-first applications, and other deployments where a conventional tile server is undesirable or unavailable.

## Evidence inspected

### Repository/source structure

Current `src/` contains four focused TypeScript files:

- `src/OfflinePlugin.ts` — main plugin and MapLibre integration (~20 KB at inspection time)
- `src/db.ts` — OPFS/storage handling
- `src/pmtiles_adapter.ts` — PMTiles adapter
- `src/index.ts` — public exports

The package declares `pmtiles`, `pbf`, and `pako` runtime dependencies and MapLibre GL JS v3-v6 as a peer dependency. It publishes ESM, UMD/CommonJS and TypeScript declaration outputs.

### Current release/maintenance evidence

`package.json` reports version **2.2.0**. On 2026-09-29 the default branch received commits `8d4b2a1` (`feat: support maplibre-gl v6`) and `7cc2f4c` (`2.2.0`). Earlier 2026 work migrated the project to TypeScript, added `AbortSignal` cancellation, moved map/style storage from IndexedDB to OPFS, and added clear-all storage behavior.

### Important negative evidence

The package currently has **no automated test command**: `npm test` is defined as an error (`Error: no test specified`). I therefore did not classify the project VERIFIED despite the published package/release history and concrete implementation. A future promotion should require either upstream automated tests/CI evidence or direct Github-gold execution against supported browsers.

## Useful components / patterns

1. **OPFS-backed PMTiles source** — compact pattern for serving a local PMTiles archive to MapLibre without a network tile server.
2. **Custom `offline-pmtiles://` MapLibre protocol** — reusable integration boundary between renderer and local archive.
3. **Download cancellation + cleanup** — `AbortSignal` support is valuable for large mobile downloads and interrupted field workflows.
4. **Storage quota reporting/error state** — exposes used/quota/percentage and a dedicated quota error state.
5. **Offline style persistence** — stores style JSON alongside map data.
6. **PWA-oriented example/build** — useful reference for browser-delivered offline mapping.

## Offline boundary

The README is appropriately explicit that storing the PMTiles archive and style JSON is not sufficient for a fully offline styled map. MapLibre may still fetch glyph/font PBFs and sprites referenced by a style. Upstream recommends packaging those assets locally and caching them through the application's service worker. This distinction should be preserved in downstream documentation: the plugin solves offline tile/archive storage, not every external style dependency automatically.

## Runtime / platforms

- Browser/PWA environment with OPFS support
- MapLibre GL JS v3, v4, v5, or v6 according to current peer dependency declaration
- JavaScript/TypeScript application
- Build tooling uses Vite

Browser compatibility, storage quotas, persistence policy, eviction behavior, private-browsing behavior, and very-large-file performance remain browser/platform dependent and should be tested on target devices.

## License

Root `LICENSE` is **MIT**. `package.json` also declares MIT. No upstream implementation code was copied into Github-gold. PMTiles, MapLibre, pako, pbf, map data, fonts, sprites and any third-party styles retain their own licenses/provenance requirements.

## Verification boundary

Github-gold inspected the README, package metadata, source-tree structure, root license, duplicate status, and recent commit history. Github-gold **did not** install the npm package, build the example, execute a browser, download a PMTiles archive, test OPFS quota/eviction behavior, test cancellation cleanup, verify MVT/MLT rendering, benchmark large archives, or validate behavior across Chrome/Firefox/Safari/mobile browsers.

The README's performance/storage statements are upstream guidance, not independently reproduced measurements.

## Caveats / risks

- No automated test script is presently defined, materially limiting working-evidence confidence.
- OPFS behavior and quota/persistence vary by browser and platform.
- A PMTiles archive plus style JSON does not automatically make external glyphs/sprites offline.
- Large regional/country archives can create substantial download and storage pressure even if random access is efficient.
- Web storage should not be treated as guaranteed permanent storage without understanding browser eviction/persistence semantics.

## Follow-up research

1. Inspect `OfflinePlugin.ts` and `db.ts` for atomicity and cleanup behavior during aborted/failed downloads.
2. Test partial download, quota exhaustion, restart/reload, deletion, and corrupted/truncated PMTiles cases in Chromium.
3. Determine current OPFS compatibility/fallback behavior across major desktop and Android browsers.
4. Verify MLT behavior separately from MVT.
5. Inspect whether range/chunked acquisition could support regional extraction rather than full-archive download.
6. Compare this approach with native MapLibre offline-region APIs and service-worker-only caching.
7. Trace Protomaps/PMTiles ecosystem components for additional reusable offline-map primitives.
