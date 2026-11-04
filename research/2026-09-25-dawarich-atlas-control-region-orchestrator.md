# Dawarich Atlas `atlas-control` — offline geodata orchestration sidecar

- **Upstream:** https://github.com/dawarich-app/atlas/tree/main/atlas-control
- **Parent project:** https://github.com/dawarich-app/atlas
- **Author/org:** dawarich-app
- **Category:** offline maps / geodata orchestration / Go sidecar / Docker Compose control plane
- **Evidence:** VERIFIED (primary-source inspection; not independently executed)
- **Gold score:** **27/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- **License:** AGPL-3.0 via parent repository
- **Discovery:** recursive component follow-up from the Dawarich Atlas dossier

## Why it matters

`atlas-control` is a small Go sidecar that turns a heterogeneous offline mapping stack into a stateful operational surface. Instead of requiring an administrator or client to understand Photon, Valhalla, Overpass and OTP build logs independently, the component normalizes service state, exposes control/status HTTP endpoints, stages regional OSM/GTFS data and performs data activation through safer partial-file/rename patterns.

The design is valuable beyond Atlas as a concrete pattern for offline appliances: a narrow local control service owns privileged container/data operations while the main application consumes a much smaller HTTP API.

## Concrete component map

The upstream README identifies:

- `internal/state/` — synchronized in-memory service state;
- `internal/parsers/` — service-specific log parsers producing normalized phase/progress/readiness results;
- `internal/dockerexec/` — Docker Compose wrapper behind a mockable `Runner` interface;
- `internal/osmium/` — `osmium-tool` merge/conversion wrapper;
- `internal/regions/` — region configuration parsing;
- `internal/server/` — chi-based HTTP control/status surface;
- `cmd/mock` plus scenario fixtures for development without real backing services.

The Go module targets Go 1.22 and has a deliberately small direct dependency surface: `go-chi/chi/v5` plus `yaml.v3`.

## Operational API

The current router exposes health, aggregate service status, bounded service logs, service enable/disable/update actions, asynchronous region application, tile download/status and update status. The sidecar therefore separates long-running geodata work from the UI/API process while still giving callers a stable status surface.

Service enablement is allowlisted to known Atlas services/profiles rather than passing arbitrary service names directly to Compose.

## Region-ingest pipeline

The inspected `runApplyRegions` implementation performs a useful sequence:

1. validates requested region names before acknowledging work;
2. asynchronously loads region definitions and downloads missing PBF sources;
3. optionally downloads GTFS data, treating transit download failure as non-fatal;
4. uses a relative symlink for a single PBF source or `osmium` merge for multiple sources;
5. writes multi-region merge output to `current.osm.pbf.partial` and renames it only after merge success;
6. converts PBF to the bzip2 OSM XML form expected by Overpass, again using a `.partial` file before rename;
7. stages OSM and available GTFS inputs for OpenTripPlanner and invalidates its previous `graph.obj`;
8. restarts Valhalla, Overpass and OTP after the new dataset has been materialized.

This is a stronger pattern than downloading directly onto the live target because downstream consumers are less likely to observe a half-written merged dataset.

## Progress normalization

`internal/parsers/` contains dedicated parsers and tests for multiple upstream services including Photon, Valhalla, Overpass, OTP and libpostal. For example, the Valhalla parser maps observed build-log phases such as relation parsing, admin DB construction, elevation processing and tile construction into normalized progress/readiness state; explicit tile-complete or serving signals mark the service ready.

This is operationally useful but also a maintenance boundary: log parsing is inherently coupled to upstream output text, so parser tests and updates are important when backing services change their logs.

## Tiles and atomic activation

The tile endpoint tracks URL, status, start/finish timestamps and byte progress. The implementation documents streaming into `<target>.partial` followed by an atomic rename on success so the serving layer does not receive a partially downloaded PMTiles file. This mirrors the safer activation strategy used by the OSM conversion path.

## Working evidence inspected

Primary-source inspection on 2026-09-25 found:

- a dedicated component README with local `go test ./...`, normal and mock-mode execution, image build instructions and architecture notes;
- source directories for state, parsers, Docker execution, osmium, regions and HTTP server;
- paired tests for server/log-follow/update behavior and multiple service parsers;
- mock scenario test data;
- a small explicit Go module dependency set;
- recent parent-repository activity through 2026-09-22, including the capability-coverage API and external-Valhalla coverage work.

This supports VERIFIED status as repository evidence. GitHub Gold did not execute the component.

## License / reuse caveat

The parent Atlas repository is AGPL-3.0. `atlas-control` sits inside that repository and no separate component license was found during this inspection, so treat it as AGPL-3.0-covered unless upstream states otherwise. The architectural patterns can be studied independently, but source reuse/modification/distribution must respect the applicable license. No upstream implementation code was copied into GitHub Gold.

## Limitations / risks

- The sidecar deliberately owns privileged Docker Compose execution, so compromise of this local control plane can have host/container consequences.
- Operational state is in memory; the README explicitly says persistence belongs to the main Atlas application.
- Log-derived readiness/progress can drift when upstream service log formats change.
- Region application currently runs in a background context that survives client disconnect; operators need external lifecycle/observability discipline for long jobs.
- Existing source files are reused when present, so integrity/freshness policy deserves deeper inspection before treating the pipeline as a content-verifying updater.
- This component is tailored to Atlas paths, profiles and service names rather than packaged as a generic library.

## What GitHub Gold did not verify

GitHub Gold did **not**:

- compile or run `atlas-control`;
- execute `go test ./...`;
- run mock scenarios;
- invoke Docker Compose or osmium;
- download/merge real PBF or GTFS datasets;
- test interrupted downloads or crash recovery;
- verify atomic-rename behavior across filesystems;
- test malicious/invalid region manifests or URLs;
- audit authentication/network exposure of the sidecar; or
- reproduce service progress/readiness parsing against live current service logs.

## Strong follow-up leads

1. Inspect the capability/coverage API separately from the ingest controller: it is a promising client-facing primitive for offline software that must reason about locally available geography/capabilities.
2. Check checksum/signature/freshness handling for downloaded PBF, GTFS and PMTiles artifacts; this is the clearest hardening opportunity exposed by the ingest design.
3. Then rotate away from Atlas/geospatial infrastructure unless a materially stronger component emerges.

## Verdict

**VERIFIED — S / 27.** `atlas-control` clears the component-level quality bar because it is a compact, tested, documented orchestration layer with useful reusable design patterns: mockable privileged execution, heterogeneous service-state normalization, asynchronous region ingestion, multi-source OSM materialization and partial-file/atomic activation. It scores below the full Atlas stack because it is tightly coupled to Atlas and its progress model depends on upstream log formats.