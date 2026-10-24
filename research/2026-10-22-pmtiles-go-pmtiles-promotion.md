# PMTiles + go-pmtiles: canonical promotions and current evidence

Research date: 2026-10-22. GitHub-first discovery from offline-mapping research. These are distinct canonical projects: a format/reference-implementation ecosystem and an operational Go CLI/library. Existing in-depth dossiers: [PMTiles](2026-09-05-protomaps-pmtiles-single-file-offline-map-archive.md) and [go-pmtiles](2026-09-06-go-pmtiles-operational-cli-range-sync-server.md).

## PMTiles — VERIFIED, S/28

- Upstream: https://github.com/protomaps/PMTiles
- Primary files: [README](https://github.com/protomaps/PMTiles/blob/main/README.md), [LICENSE](https://github.com/protomaps/PMTiles/blob/main/LICENSE), [Version 3 spec](https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md), [CI workflow](https://github.com/protomaps/PMTiles/blob/main/.github/workflows/actions.yml).
- Core reusable components: `js/src/index.ts` (range reader and cache), `js/src/adapters.ts` (mapping adapters), `python/pmtiles`, `python/rio-pmtiles`, `cpp/`, `openlayers/`, `serverless/aws/`, `serverless/cloudflare/`.
- Format evidence: fixed 127-byte header, root directory in first 16 KiB, optional leaf directories, tile and metadata ranges. Useful for offline, static HTTP and object-storage map delivery.
- Upstream PR CI on 2026-10-19 [run 39281511827](https://github.com/protomaps/PMTiles/actions/runs/39281511827) passed `build_app` and `test`. Workflow builds JS, viewer, OpenLayers, AWS and Cloudflare adapters; tests JS, Python, rio-pmtiles, C++ compilation and Cloudflare.
- Latest inspected main commit 2026-09-16 updated Python pmtiles to 3.8.1. No GitHub Releases surfaced in root repository; distribution is via package registries and companion CLI.
- Score: Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 3 = **28/S**.
- Licensing: BSD-3-Clause reference implementations; specification public domain/CC0; map tiles/sample datasets separately licensed.
- Caveats: HTTP Range and CORS behavior are deployment requirements; archive metadata and decompression are untrusted inputs; CI Actions use mutable version tags.

## go-pmtiles — VERIFIED, S/28

- Upstream: https://github.com/protomaps/go-pmtiles
- Primary files: [main.go](https://github.com/protomaps/go-pmtiles/blob/main/main.go), [verify.go](https://github.com/protomaps/go-pmtiles/blob/main/pmtiles/verify.go), [sync.go](https://github.com/protomaps/go-pmtiles/blob/main/pmtiles/sync.go), [LICENSE](https://github.com/protomaps/go-pmtiles/blob/main/LICENSE), [test workflow](https://github.com/protomaps/go-pmtiles/blob/main/.github/workflows/test.yml).
- Reusable CLI commands: `show`, `tile`, `cluster`, `edit`, `extract`, `merge`, `convert`, `verify`, `serve`, `upload`; hidden `makesync/sync` are experimental. Package includes directory and tile-ID encoders, region extraction, cloud/local bucket adapters, server/cache, and structural verifier.
- Upstream stable release [v1.31.2](https://github.com/protomaps/go-pmtiles/releases/tag/v1.31.2) on 2026-07-22 fixes `Content-Length` handling for tile responses including gzip.
- Upstream PR CI on 2026-10-06 [test run 37488026517](https://github.com/protomaps/go-pmtiles/actions/runs/37488026517) passed Ubuntu, Windows and fmt/vet/lint jobs. Parallel [Docker publish run 37488026722](https://github.com/protomaps/go-pmtiles/actions/runs/37488026722) failed; publishing and testing are separate signals.
- Source-level limitation: `verify.go` does structural verification, not individual tile-content or cryptographic integrity; some out-of-bounds/ordering checks log instead of returning errors. `sync.go` warns explicitly that differential sync is experimental and unsuitable for production.
- Operational caveats: `serve` defaults to binding `0.0.0.0`; require deliberate exposure and TLS/auth boundaries. Cloud provider range behavior and credentials must be verified.
- Score: Utility 5, Working Evidence 4, Reusability 5, Novelty 5, Documentation 4, Maintenance 5 = **28/S**.
- License: BSD-3-Clause; archive contents separately licensed.

## Verification boundaries and follow-ups

This run inspected upstream source, README, licenses, specifications, workflow definitions, release and CI job conclusions. It did **not** build, run tests, convert an archive, render a map, test object storage, exercise HTTP ranges, validate released binary hashes or perform a security audit. No upstream implementation source was copied.

Next: test malformed archives across JS/Python/C++/Go, investigate go-pmtiles verifier logged anomalies and remote input behavior, inspect the October large-file extract PR, evaluate range caching and cancellation, and keep experimental sync in research-only status pending interrupted-update and integrity tests.

YouTube: two seed playlist IDs were searched but returned no usable indexed video/transcript evidence; no discoveries are attributed to YouTube.
