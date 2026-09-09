# Immich — self-hosted photo/video platform and reusable media-system architecture

- **Repository:** https://github.com/immich-app/immich
- **Author / organization:** Immich
- **Category:** self-hosting / photo and video management / mobile backup / media indexing / local AI / search / API platform
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **License:** AGPL-3.0
- **Discovery:** GitHub-first broadening pass after storage/synchronization research
- **Research date:** 2026-08-31

## Executive finding

Immich is a high-value self-hosted photo and video management platform that combines a Flutter mobile client, TypeScript/NestJS server, web application, Python machine-learning service, CLI, generated API surface, containerized deployment, and a large automated build/test/release system in one actively maintained monorepo.

It is worth cataloging both as a complete user-controlled replacement for cloud photo-library workflows and as a source of architectural patterns for media ingestion, mobile background backup, deduplication, metadata extraction, derivative generation, search, local machine-learning inference, multi-user media libraries, and cross-platform release engineering.

The project is **not** scored highly merely because it is popular. The VERIFIED classification here is based on inspected repository structure, current release artifacts, CI/workflow surfaces, integration-test directories, explicit platform support, and active source maintenance. GitHub Gold did not independently deploy or run Immich during this pass.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Solves a broad, practical self-hosted media-management and mobile-backup problem. |
| Working evidence | 5 | Current stable and prerelease artifacts, extensive CI, server/mobile tests, Docker release paths, and active maintenance. |
| Reusability | 4 | Many reusable architectural patterns and separable services, but the monorepo is complex and AGPL-3.0 materially constrains direct source reuse. |
| Novelty | 4 | Strong integration of self-hosting, mobile auto-backup, search, metadata, local ML, sharing, and media UX; individual primitives are not unique. |
| Documentation | 5 | Main documentation site, install guides, developer documentation, feature matrix, translated READMEs, and deployment material. |
| Maintenance | 5 | Active development through 2026-09-01 UTC, stable v3.1.0 release in July 2026, and v3.2.0 release candidates published August 31, 2026. |

**Total: 28 / 30 — provisional S tier.**

## What the project does

The upstream README describes Immich as a high-performance self-hosted photo and video management solution. The documented feature surface includes:

- photo and video upload from mobile and web;
- mobile automatic/background backup;
- duplicate prevention;
- selective album backup;
- multi-user libraries;
- normal and shared albums;
- RAW-format support;
- EXIF and map metadata views;
- search using metadata, detected objects, faces, and CLIP-style semantic embeddings;
- OAuth and API keys;
- Live Photo / Motion Photo handling;
- configurable storage organization;
- public and partner sharing;
- facial recognition and clustering;
- memories;
- mobile offline support;
- read-only gallery mode;
- stacked photos, tags, and folder views.

The README also explicitly warns users to maintain an independent **3-2-1 backup strategy** for important media. This is an important trust boundary: Immich is a photo-management and synchronization/backup workflow component, not a substitute for a separately designed disaster-recovery strategy.

## Repository architecture observed

The current repository is a large multi-runtime monorepo rather than a single web application.

### Server

`server/` contains the primary backend service and includes:

- a NestJS/TypeScript source tree under `server/src`;
- a dedicated `server/test` tree;
- server Dockerfiles;
- package/runtime manifests;
- linting and TypeScript configuration;
- security-related HTTP configuration such as `helmet.json`;
- build and development tooling.

This is useful as a reference for organizing a large API/backend domain around a generated client/API contract and multiple downstream clients.

### Mobile

`mobile/` is a Flutter application with:

- Android and iOS platform directories;
- application code under `mobile/lib`;
- `integration_test/`;
- local database/schema material under `drift_schemas`;
- build/configuration manifests and static analysis configuration.

The mobile feature set is especially relevant to GitHub Gold because upstream documents mobile automatic/background backup, selective backup, local download, offline support, and direct connection to a user-controlled Immich server.

### Machine learning

`machine-learning/` is a distinct Python service with its own:

- `pyproject.toml`;
- Dockerfile;
- `immich_ml` implementation package;
- tests/pytest configuration;
- ANN-related code;
- load-testing support via `locustfile.py`;
- development/runtime tooling.

This separation is architecturally valuable: computationally heavy inference can evolve and scale independently from the primary TypeScript application server.

The public product feature surface ties this service to object/face and semantic-search workflows, while the repository structure provides concrete evidence that ML is implemented as a separate maintained service rather than a documentation-only feature claim.

### Web / API / CLI / deployment surfaces

The repository root and workflow inventory show additional independent surfaces for:

- web application development;
- CLI build/test/release work;
- OpenAPI validation/generation;
- Docker image builds;
- documentation;
- mobile release builds;
- F-Droid-related packaging;
- deployment manifests and Docker Compose distributions.

These make the repository useful as a large-scale reference for keeping mobile, web, CLI, backend, ML and generated API clients aligned within one project.

## Working evidence

### Stable release

GitHub's current `releases/latest` endpoint reports **v3.1.0**, published **2026-07-29**.

The release includes concrete distribution artifacts such as architecture-specific Android APKs, a universal APK, and Docker Compose deployment files. GitHub records SHA-256 digests for the release assets.

This is stronger evidence than README claims alone: the project is producing versioned, downloadable application and deployment artifacts.

### Current prerelease activity

The release stream also contains **v3.2.0-rc.2**, published **2026-08-31**. The prerelease includes Android APK variants and Docker Compose deployment material.

A release candidate is not treated as the stable production baseline, but it demonstrates an active release pipeline beyond v3.1.0.

### Same-day source maintenance

GitHub repository metadata inspected during this pass reports:

- repository updated: **2026-09-01T04:23:18Z**;
- source pushed: **2026-09-01T03:51:33Z**.

That places active source work immediately adjacent to this research run rather than months behind it.

### CI and release engineering

The inspected `.github/workflows` directory contains dedicated workflows for, among other tasks:

- mobile builds;
- CLI checks/builds;
- OpenAPI consistency checks;
- CodeQL analysis;
- Docker builds;
- documentation builds/deployments;
- draft releases;
- F-Droid-related work;
- maintenance and repository automation.

The presence of purpose-specific workflows across distinct product surfaces is meaningful working evidence, although GitHub Gold did not execute these workflows independently.

### Test surfaces

Direct repository inspection confirms test/integration surfaces including:

- `server/test`;
- `mobile/integration_test`;
- Python ML test configuration and fixtures;
- repository-level CI and static-analysis workflows.

This pass does not claim full coverage or correctness of those tests; it records that nontrivial automated verification infrastructure exists.

## High-value reusable patterns/components

Because the repository is AGPL-3.0, these are primarily **architecture and upstream-linked component targets** unless a future reuse plan deliberately accepts the license obligations.

### 1. Mobile background media backup architecture

Immich is a strong reference for building a mobile client that:

- discovers local media;
- selects backup sources/albums;
- performs background synchronization;
- avoids duplicate uploads;
- maintains local application state;
- reconnects to a self-hosted server rather than a vendor cloud.

A focused future pass should identify the exact Flutter services, platform channels, worker/scheduler integrations, and deduplication identifiers involved.

### 2. Media ingestion and derivative pipeline

The backend is a strong lead for tracing an uploaded asset through:

1. upload/API admission;
2. persistence and metadata records;
3. EXIF extraction;
4. thumbnails / previews;
5. video transcoding where required;
6. machine-learning jobs;
7. indexing/search;
8. presentation to mobile/web clients.

The exact queue/job boundaries should be mapped in a later source-level pass before promoting individual modules as reusable components.

### 3. Local/self-hosted machine-learning service

`machine-learning/immich_ml` and the surrounding Docker/Python tooling are strong research targets for:

- image embeddings;
- face/object inference;
- model lifecycle and cache management;
- hardware-acceleration variants;
- batching and concurrency;
- local semantic search support;
- service-to-service inference APIs.

The presence of `locustfile.py` also makes performance/load-test methodology a concrete follow-up lead.

### 4. Generated API/client contract

The repository has an explicit OpenAPI workflow. That makes Immich a useful reference for maintaining a shared API contract across TypeScript server code, web clients, Flutter mobile clients, CLI tooling, and integrations.

### 5. Multi-client release engineering

The release/build infrastructure is itself valuable: one repository coordinates backend containers, deployment manifests, Android artifacts, documentation, CLI surfaces, and prerelease/stable release channels.

### 6. Self-hosted identity/sharing model

The documented support for multi-user accounts, OAuth, API keys, public sharing and partner sharing creates a useful future research area around authorization boundaries for personal-media systems.

## Deployment/runtime observations

Immich is not a tiny single-binary utility. Production use requires a server deployment and the associated data services described by upstream installation documentation, with optional mobile applications and machine-learning workload requirements.

The release artifacts provide Docker Compose deployment files, which materially lowers deployment friction, but operators still need to manage:

- persistent media storage;
- database/data-service persistence;
- host backups;
- network exposure/reverse proxy/TLS as appropriate;
- updates and migrations;
- compute requirements for media processing and ML;
- mobile client/server version compatibility.

Users should follow Immich's own warning that the system is not the sole copy of important media.

## Supported clients/platforms

From current repository and release evidence:

- self-hosted server via container-oriented deployment;
- browser/web client;
- Android;
- iOS;
- CLI/tooling surfaces;
- machine-learning service running alongside the server stack.

Current GitHub release assets include multiple Android CPU architecture variants.

## Languages / technologies observed

The repository's primary GitHub language is TypeScript. Major project surfaces also include:

- TypeScript / Node.js / NestJS server infrastructure;
- Flutter / Dart mobile application;
- Python machine-learning service;
- web frontend tooling;
- Docker / Docker Compose;
- OpenAPI tooling;
- platform-specific Android/iOS project material.

A later pass should record exact version requirements from the relevant manifests rather than infer them from ecosystem defaults.

## License and reuse boundary

GitHub reports the repository license as **GNU Affero General Public License v3.0 (AGPL-3.0)**, and the root README also displays AGPLv3 licensing.

This is a critical catalog note.

GitHub Gold did **not** copy source from Immich. Direct incorporation or modification of covered source into another program can create strong copyleft obligations, including network-use/source-availability implications characteristic of AGPL-3.0. Any future extraction/adaptation should therefore begin with an exact license review and preserve all required notices.

For projects unwilling to adopt those obligations, Immich remains extremely valuable as:

- an architecture reference;
- a protocol/API interoperability target;
- an upstream dependency/service;
- a source of implementation ideas that are reimplemented independently rather than copied.

## Security, privacy and operational boundaries

### Self-hosting does not automatically make a deployment private

The privacy value depends on operator configuration. Public exposure, reverse proxies, TLS termination, OAuth providers, API keys, sharing links, backups, logs and host compromise all create independent trust boundaries.

### Media is high-sensitivity data

Photo libraries can contain faces, precise timestamps, location metadata, family relationships and private events. A self-hosted deployment should be treated as a sensitive-data service, not as an ordinary low-value gallery.

### Machine learning creates additional data-processing surfaces

Face and semantic-search features intentionally process visual content. The self-hosted architecture can keep that processing under user control, but the exact model-download, telemetry/network and accelerator behavior should be audited separately before making stronger privacy claims.

### Application backup is not disaster recovery

Upstream's own README warns users to maintain a 3-2-1 backup plan. Deletion, database corruption, filesystem failure, administrative error, ransomware or host loss can still destroy a self-hosted library if storage is not independently protected.

### Public sharing changes the threat model

Public links and externally reachable endpoints intentionally cross the private-library boundary. Authentication, token lifetime, reverse-proxy handling and authorization tests are strong future source-level targets.

## Verification performed by GitHub Gold

This research pass inspected:

- repository metadata and current activity timestamps;
- the root README and feature matrix;
- repository licensing metadata;
- current stable release metadata and artifacts;
- current v3.2 release-candidate metadata;
- top-level repository structure;
- server structure and test directory;
- mobile structure and integration-test directory;
- machine-learning service structure;
- GitHub Actions workflow inventory;
- existing `Github-gold` catalog/research state for duplicate avoidance.

## Verification explicitly not performed

GitHub Gold did **not**:

- deploy Immich;
- run Docker Compose;
- upload or restore a photo/video library;
- install the Android or iOS application;
- test mobile background backup;
- build source;
- execute server, Flutter or Python tests;
- benchmark import/search/transcoding/ML performance;
- verify face-recognition accuracy;
- inspect every dependency license;
- test OAuth/API-key/public-sharing authorization;
- fuzz media parsers or API endpoints;
- validate release-asset digests independently;
- perform a penetration test or security audit;
- verify a disaster-recovery procedure.

All claims above are therefore limited to inspected upstream source/repository/release evidence.

## Maintenance signals

Strong:

- stable v3.1.0 published 2026-07-29;
- v3.2.0-rc.2 published 2026-08-31;
- source push observed 2026-09-01 UTC;
- large multi-surface CI/release workflow set;
- active server/mobile/ML code and test trees;
- extensive user/developer documentation and translated project READMEs.

No maintenance deduction is warranted in this pass.

## Why it belongs in GitHub Gold

Immich is unusually valuable because it demonstrates how to combine several difficult systems into one user-controlled product:

- mobile background synchronization;
- large personal-media storage;
- metadata extraction and media transformation;
- local machine learning;
- full-text/semantic/face-oriented search;
- multi-user authorization and sharing;
- browser and mobile UX;
- generated API clients;
- self-hosted deployment;
- coordinated multi-platform releases.

Even where AGPL-3.0 prevents casual source extraction, the architecture is rich enough to justify deep component-level research.

## Strongest recursive leads

1. **Mobile backup engine** — identify exact Dart/native components for media discovery, background execution, upload retry, deduplication and reconciliation.
2. **Job system / ingestion pipeline** — map asset upload through metadata extraction, derivatives, ML and indexing.
3. **`immich_ml`** — inspect model loading, embedding generation, face pipeline, inference providers, caching and hardware acceleration.
4. **Search/index architecture** — trace metadata, vector and face-search data flow into the database/query layer.
5. **OpenAPI/client generation** — map how API changes propagate across server, web, CLI and Flutter consumers.
6. **Authorization tests** — inspect API-key, OAuth, public-share and partner-share policy boundaries.
7. **External-library support** — understand how read-only/imported filesystem libraries are indexed without turning Immich into the authoritative storage copy.
8. **Release hardening** — inspect Docker/mobile artifact provenance, signing and dependency security workflows.

## Promotion recommendation

**VERIFIED — provisional S / 28 — promotion-ready as a whole-project catalog candidate.**

Do not copy Immich source into GitHub Gold as part of promotion. Catalog it by reference, preserve the AGPL-3.0 caveat, and treat individual component extraction as a separate license-aware research decision.
