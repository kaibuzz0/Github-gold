# Protomaps PMTiles — single-file offline/serverless map archive

- **Repository:** https://github.com/protomaps/PMTiles
- **Author / Org:** Protomaps
- **Category:** offline maps / geospatial / archival format / static hosting / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 4
- **Discovery:** Independent GitHub-first breadth rotation after closing the mesh-routing research thread.

## What it is

PMTiles is a single-file archive format for tiled geospatial data. The repository contains the Version 3 specification plus reference implementations/integrations for JavaScript, Python, OpenLayers, and serverless environments, while the companion `protomaps/go-pmtiles` repository supplies the primary CLI for conversion/upload workflows.

The central architectural value is that a map does not require a conventional tile-server database/backend. A `.pmtiles` object can live on ordinary static/object storage and clients can retrieve only the portions they need. The same single-file property also makes the format useful for local/offline mapping workflows.

## Source-level evidence

### Concrete Version 3 format

The current V3 specification defines a PMTiles archive as:

1. a fixed **127-byte header**;
2. root directory;
3. JSON metadata;
4. optional leaf directories;
5. tile data.

The root directory must be contained in the first **16 KiB** of the archive so latency-optimized clients can retrieve it up front. The header records offsets/lengths, tile counts, compression, tile type, zoom range and geographic bounds. This is substantially stronger evidence than a README-only file-format claim: the repository contains a normative binary specification.

### Reusable implementations and adapters

The root README points to:

- JavaScript support for Leaflet and MapLibre GL JS;
- an OpenLayers integration;
- Python scripts/library usage;
- Go support via `go-pmtiles`;
- AWS Lambda and Cloudflare Workers serverless examples;
- conversion from MBTiles and upload to S3-compatible storage via the companion CLI.

This makes PMTiles useful both as a format and as an interoperability component rather than merely an application.

### Tests

Repository-native JavaScript tests exist for the V3 codec and directory/varint behavior, protocol/TileJSON adapter behavior, and request-abort/cancellation behavior. GitHub Gold did **not** execute those tests; their presence is upstream working evidence only.

### Current maintenance

Recent upstream commits observed during this run include:

- **2026-09-16:** Python `pmtiles` 3.8.1 release commit;
- **2026-09-16:** deterministic gzip mtime change with an added test;
- **2026-09-14:** Python package updates and a `rio-pmtiles` TIFF-overview fix;
- **2026-09-11:** MapLibre GL 6.9 update;
- **2026-08-19:** PMTiles JS 4.5 application update.

The repository is not archived.

## Why it matters for GitHub Gold

PMTiles is unusually reusable because the valuable artifact is not only an application: it is a documented storage primitive that can underpin offline field maps, emergency/disaster mapping kits, local-first applications, static websites, self-hosted map systems, research datasets, embedded/local-network map appliances, and cloud map delivery without a dedicated tile backend.

The strongest reusable concepts/components are:

- V3 binary archive specification;
- hierarchical root/leaf directory indexing;
- range-addressable single-file storage;
- JavaScript PMTiles protocol integration for MapLibre;
- Leaflet/OpenLayers adapters;
- Python reader/writer tooling;
- serverless/static-storage deployment patterns;
- MBTiles-to-PMTiles conversion ecosystem;
- interoperability with vector/raster tile payloads.

## Install / runtime / platforms

Consumption depends on the implementation: browser/Node.js for the JavaScript package, Python for Python tooling, or Go for the companion CLI. Static/object-storage deployment can use ordinary HTTP byte-range capable infrastructure. Local applications can consume local PMTiles archives where their renderer/runtime supports the format.

## License

The repository `LICENSE` states that the **reference implementations are BSD-3-Clause**. The **PMTiles specification itself is public domain or CC0 where applicable**. Sample tilesets can carry separate data licenses and must not be assumed to inherit the implementation license.

No third-party implementation code was copied into GitHub Gold.

## Caveats

- A permissive software/specification license does **not** remove attribution or redistribution obligations attached to map source data such as OpenStreetMap or other datasets.
- Hosting remote archives depends on correct HTTP range/CORS behavior.
- Archive size can still be very large; PMTiles changes packaging/access architecture rather than making planet-scale map data intrinsically small.
- Renderer support differs by environment; PMTiles itself is not a complete navigation application.
- GitHub Gold did not benchmark range-request latency, storage cost, archive generation time, memory usage, or very-large-archive behavior.

## Verification performed

Inspected upstream repository metadata, root README, root license, Version 3 specification, current code-search evidence for JavaScript tests, and recent commit history. No package was installed; no archive was created, converted, served, or rendered by GitHub Gold.

## Related ecosystem / strongest next leads

1. **protomaps/go-pmtiles** — inspect the production CLI's `extract`, `convert`, `serve`, `upload`, verification, and range-request behavior.
2. **protomaps/basemaps** — inspect the Planetiler-based OSM/Natural Earth pipeline that generates usable basemap PMTiles and the associated MapLibre styles.
3. **felt/tippecanoe** — active vector-tile generation tool referenced directly by PMTiles recipes; evaluate as a separate reusable geospatial component.
4. **MapLibre** integrations — determine current native/mobile PMTiles support and offline deployment constraints.

## Verdict

**VERIFIED / S / 29.** PMTiles meets the Gold bar as a compact, permissively licensed, actively maintained geospatial storage/interchange primitive with a normative specification, multiple implementations, tests, and direct offline/local-first value.