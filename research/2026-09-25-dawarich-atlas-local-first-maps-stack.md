# Dawarich Atlas — local-first self-hosted maps stack

- **Upstream:** https://github.com/dawarich-app/atlas
- **Author/org:** dawarich-app
- **Category:** offline maps / self-hosting / geospatial infrastructure / local-first
- **Evidence:** VERIFIED (primary-source inspection; not independently executed)
- **Gold score:** **28/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 5/5
  - Maintenance 4/5
- **License:** AGPL-3.0; bundled/upstream geospatial components retain their own licenses
- **Discovery:** independent GitHub-first rotation after closing the MeshSat research thread

## Why it matters

Dawarich Atlas packages a complete self-hostable mapping backend around OpenStreetMap and established FOSS geospatial components. Its stated runtime goal is zero outbound API calls after required regional data is installed. That makes it unusually relevant for local-first deployments, private infrastructure, disconnected networks, field systems, homelabs, and applications that need maps/search/routing without depending on commercial mapping APIs.

This is not just a map UI. Atlas exposes public/admin APIs and orchestrates multiple data/services for geocoding, routing, map matching, POIs and transit. The current application is Phoenix/Elixir and controls its Compose services directly through the Docker socket.

## Useful architecture/components

Upstream currently documents or integrates:

- **MapLibre / Protomaps** for map presentation and basemap infrastructure.
- **Photon** for local geocoding/search.
- **Valhalla** for routing and map matching.
- **Overpass** for POI data.
- **MOTIS / OpenTripPlanner** options for public-transit workflows.
- **osmium** for regional OSM data processing/merging.
- Region presets and multi-region ingestion.
- A public API plus administrative API.
- A control plane that downloads regional data, applies configuration and restarts ingest services.
- `GET /api/v1/coverage` in v0.6.1 for reporting readiness and installed coverage for geocoding, routing, map matching, POIs and transit.

The separation into familiar upstream geospatial engines is valuable: Atlas is primarily integration/orchestration rather than an opaque proprietary routing stack.

## Runtime / installation

The documented quickstart is Docker Compose. A fresh checkout can boot with `docker compose up -d`; Atlas generates its own `SECRET_KEY_BASE`, persists application state locally, and exposes the UI on port 8484. Regional data can then be selected and installed from the settings UI.

Operational caveats matter:

- The Phoenix control plane accesses the host Docker socket and therefore needs the correct Docker group ID.
- Persistent-directory UID/GID ownership may require adjustment on NAS platforms.
- Dataset scale is material: upstream characterizes city ingest as minutes, country ingest as hours and planet-scale ingest as days.
- Completely disconnected operation still requires the desired datasets/images to have been obtained beforehand; "zero outbound API calls at runtime" should not be confused with zero network dependency during initial provisioning.

## Working evidence inspected

Primary-source evidence inspected on 2026-09-25:

1. The README documents the Compose quickstart, local SQLite persistence, regional ingestion, service topology, API surfaces, architecture/docs links and release/image process.
2. The repository contains dedicated GitHub Actions workflows for Phoenix tests, configuration/deployment checks, legacy Rails parity, image builds, releases and region-catalog refresh.
3. `test-phoenix.yml` compiles with warnings treated as errors, runs strict Credo and formatting gates, runs catalog-generation checks, executes ExUnit with parity/catalog-artifact gates, and tests the Docker entrypoint.
4. The parity gate is explicitly documented as byte-diff comparison against committed Rails goldens, reducing migration drift while Phoenix replaces the legacy Rails implementation.
5. Stable release **v0.6.1** was published **2026-09-22**. Its release notes add streamed region-processing logs and the coverage/readiness API.
6. Default-branch commits continued on **2026-09-22**, including external Valhalla region coverage support after the release-preparation commit.

This supports VERIFIED status as repository evidence. It does **not** mean GitHub Gold independently reproduced the deployment.

## License / reuse caveats

Atlas itself is **AGPL-3.0**. Network-service modifications can therefore trigger AGPL source-availability obligations; do not lift implementation code into permissively licensed projects without reviewing compatibility and obligations.

The stack also combines separately licensed upstream software/data. The README identifies examples including OSM data under ODbL, Protomaps/MapLibre under BSD-3, Valhalla under MIT, and Photon/Overpass/OpenTripPlanner under LGPL-3.0 or AGPL-3.0. Reusers need to preserve the applicable upstream terms and data attribution.

No Atlas implementation code was copied into GitHub Gold.

## Limitations / risks

- Atlas is young: current stable version is 0.6.1, so operational interfaces may still move.
- A Docker-socket-backed control plane expands the trust boundary of the application container and deserves explicit hardening in exposed deployments.
- Planet-scale storage/ingestion is operationally expensive relative to city or regional deployments.
- Quality and freshness ultimately depend on the installed OSM/transit datasets and the behavior of the integrated upstream engines.
- The project is an orchestrated stack; debugging may cross Phoenix, Compose and several geospatial services rather than one binary.

## What GitHub Gold did not verify

GitHub Gold did **not**:

- run `docker compose up`,
- ingest OSM/GTFS datasets,
- exercise Photon, Valhalla, Overpass, MOTIS or OTP,
- reproduce routing/geocoding/map-matching results,
- run the upstream test suite or CI locally,
- test disconnected operation,
- benchmark city/country/planet ingestion,
- audit Docker-socket privilege boundaries, or
- independently validate map/data licensing compliance.

## Strong recursive leads

1. **Region ingest/control plane** — inspect how Atlas safely downloads, merges, activates and rolls back datasets.
2. **Coverage API** — potentially reusable pattern for capability-aware offline clients that need to know exactly which geographic functions are locally available.
3. **Transit engine abstraction** — compare MOTIS and OTP integration and graceful degradation when transit data is absent.
4. **Dawarich integration** — determine how the parent location-history application consumes Atlas and whether its API provides reusable local-first geospatial primitives.
5. **Offline deployment hardening** — inspect image pinning, update/rollback strategy and whether a fully air-gapped bundle can be prepared reproducibly.

## Verdict

**VERIFIED — S / 28.** Atlas meets the quality bar because it combines high practical utility with concrete CI/release evidence, strong documentation, an API-oriented architecture and active maintenance. Its largest caveats are early version maturity, AGPL obligations, substantial data/storage requirements at large geographic scales, and the privileged Docker control-plane boundary.