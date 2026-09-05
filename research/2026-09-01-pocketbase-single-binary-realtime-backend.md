# PocketBase — single-binary realtime backend and embeddable Go toolkit

- **Repository:** https://github.com/pocketbase/pocketbase
- **Author / organization:** PocketBase / Gani Georgiev
- **Category:** embedded backend / SQLite / realtime / authentication / file management / self-hosting / Go framework
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28 / 30 — S tier**
- **License:** MIT
- **Research date:** 2026-09-01
- **Discovery source:** GitHub-first independent discovery

## Executive assessment

PocketBase is a compact self-hosted backend that packages an embedded SQLite database, realtime subscriptions, authentication/user management, file handling, an admin UI, and a REST-style API into a portable Go executable. It can also be imported as a normal Go library and extended as an application framework rather than treated only as a prebuilt server.

The strongest GitHub Gold value is therefore not merely “small Firebase alternative.” The repository demonstrates a highly reusable pattern for shipping a substantial backend stack as one deployable binary while still exposing the underlying application lifecycle, hooks, routing, database/model layer, API handlers, forms, filesystem/storage logic, migrations, JavaScript extension support, and tests to Go applications.

**Verdict:** VERIFIED and promotion-ready as a research candidate. No source should be copied merely because the MIT license is permissive; useful modules should still be reviewed in their dependency and attribution context.

## Score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Provides database, auth, files, API, realtime, admin, backup and extensibility in a compact deployment model. |
| Working evidence | 5/5 | Formal releases, prebuilt multi-platform artifacts, repository tests and release CI that runs `go test ./...`. |
| Reusability | 5/5 | Usable both as a standalone binary and ordinary Go library/framework. Internal packages expose many separable architecture patterns. |
| Novelty | 4/5 | The individual primitives are familiar, but their cohesive single-binary/library design is unusually compact and practical. |
| Documentation | 5/5 | README plus dedicated documentation, examples, SDKs, testing guidance and changelogs. |
| Maintenance | 4/5 | Active current release line and recent source activity, but upstream explicitly warns that backward compatibility is not guaranteed before 1.0. |

**Total: 28 / 30.**

## What upstream currently says it provides

The current README describes PocketBase as an open-source Go backend containing:

- an embedded SQLite database;
- realtime subscriptions;
- built-in file management;
- built-in user management;
- an admin dashboard;
- and a REST-style API.

Upstream documents two primary deployment/reuse modes:

1. **Standalone executable:** download a release and run `pocketbase serve`.
2. **Go framework/toolkit:** import `github.com/pocketbase/pocketbase`, register application hooks/routes, and build an application-specific binary.

The prebuilt executable is based on `examples/base/main.go` and currently ships with the JavaScript VM plugin enabled, giving the binary a second extension path in addition to native Go embedding.

## Single-binary architecture

The most reusable design idea is the coupling of an embedded database/runtime with conventional application-framework extension points.

A minimal Go application can instantiate `pocketbase.New()`, bind lifecycle hooks such as `OnServe()`, register custom routes through the supplied router, and then call `app.Start()`. Upstream shows this being compiled into a statically linked executable with `CGO_ENABLED=0` on supported targets.

This matters because it keeps the operational deployment model simple while avoiding a closed appliance architecture: a project can start with the stock server and progressively move business logic into the same executable.

### Useful architectural surfaces observed in the source tree

The repository currently exposes major source areas including:

- `apis/` — HTTP/API behavior, collection operations, authentication-adjacent flows, realtime, batch APIs, backups, cron-related endpoints and extensive API tests;
- `core/` — application lifecycle, event/hook types, models, database-facing abstractions and request/realtime event state;
- `forms/` — higher-level operation/form logic;
- `cmd/` — command-line integration;
- `tools/` and supporting packages — reusable application facilities;
- `plugins/` — extension/plugin surfaces including the JavaScript VM path;
- `ui/` — embedded/admin dashboard source;
- `examples/` — executable/library usage patterns;
- migrations/storage helpers and test fixtures elsewhere in the tree.

This source layout makes PocketBase useful as a reference for building an embedded application platform, not just for consuming its API.

## Realtime subsystem

PocketBase’s realtime API is implemented as an actual server subsystem rather than a frontend convenience wrapper.

Current source includes `apis/realtime.go` and corresponding core event types. The admin-side API preview identifies the transport as **Server-Sent Events (SSE)** and shows the `/api/realtime` endpoint. Core code includes dedicated realtime connection/request events and connection state such as authenticated client context.

This is a valuable reusable pattern for applications that need database/event fanout while avoiding a separate websocket broker or message-queue service.

### Security-relevant realtime maintenance evidence

Recent changelog history includes fixes affecting authenticated realtime state, including forcing existing realtime connections to drop authentication state when a user token key changes. That is meaningful evidence that upstream treats long-lived connection authentication as a lifecycle/security concern rather than assuming credentials remain valid forever.

GitHub Gold did not independently exercise those transitions.

## API and operation surface

The current `apis/` tree is unusually broad for a compact backend. Files observed during inspection include dedicated implementations/tests for areas such as:

- backups;
- backup creation/upload;
- batch operations;
- collections and collection import;
- cron-facing endpoints;
- realtime;
- and the base API/router layer.

Large adjacent `*_test.go` files exist for several of these surfaces, including backup, batch and collection behavior. This is stronger evidence than a README-only feature claim.

The API architecture should be researched further for reusable authorization and request-rule patterns, especially where record rules, authenticated user state, file access and batch transactions intersect.

## Database and portability model

PocketBase uses SQLite as its embedded database foundation. The README currently documents building with Go 1.27+ and a pure-Go SQLite path that permits `CGO_ENABLED=0` builds.

The documented supported build target matrix includes multiple architectures across:

- Linux;
- macOS;
- Windows;
- FreeBSD;
- NetBSD;
- OpenBSD;
- and architectures including amd64, arm64, 386, ARM, LoongArch, PPC64LE, RISC-V and s390x where supported by the SQLite driver.

The practical value is a backend that can be distributed like a utility rather than an application stack requiring a separate SQL server.

This does not mean every PocketBase workload is appropriate for a single-node SQLite architecture. Capacity, write concurrency, replication, high availability and multi-region requirements must be evaluated separately.

## Extension model

PocketBase is unusually interesting because its standalone and framework modes converge.

### Go extension path

The README demonstrates direct Go embedding with application lifecycle events and custom routes. Projects can therefore add native business logic without maintaining a fork of the server.

### JavaScript extension path

The stock release executable currently includes the JavaScript VM plugin. That allows deployments to extend behavior without compiling Go for every customization.

This dual model is worth deeper research because it combines:

- a compiled core;
- native Go embedding;
- scriptable extension;
- embedded administration UI;
- and a single executable deployment artifact.

Future research should inspect the JavaScript VM trust boundary carefully. Extension scripts should not be assumed to be sandboxed merely because they are JavaScript.

## Official client ecosystem

Upstream identifies two official SDK repositories:

- `pocketbase/js-sdk` for browser, Node.js and React Native;
- `pocketbase/dart-sdk` for web, mobile, desktop and CLI use.

These are high-value recursive research leads because they expose the client-side authentication, realtime reconnect, file upload and API error semantics independently of the server implementation.

## Testing and release evidence

The README states the project has a mixture of unit and integration tests and documents the normal command:

```text
go test ./...
```

The current GitHub Actions release workflow provides stronger evidence: on pull requests and pushes it sets up Node.js and Go, rebuilds the admin UI, runs `go test ./...`, and invokes GoReleaser. This means the release/build path itself exercises the Go test suite rather than publishing binaries without a test gate.

The workflow currently uses:

- `actions/checkout@v6`;
- `actions/setup-node@v6`;
- `actions/setup-go@v7`;
- `goreleaser/goreleaser-action@v6`.

One supply-chain caveat is that these actions are referenced by version tags rather than immutable commit SHAs in the inspected workflow.

GitHub Gold did not execute this CI pipeline.

## Release and maintenance evidence

The latest formal release inspected is **v0.40.1**, published **2026-08-24**.

The release includes `checksums.txt` plus prebuilt archives for multiple operating systems and architectures. GitHub’s release metadata also exposes SHA-256 digests for release assets.

Repository metadata inspected on 2026-09-01 reports:

- the repository is not archived;
- primary language Go;
- MIT license metadata;
- source `pushed_at` 2026-08-28;
- roughly 60k stars and several thousand forks.

Popularity is not used as evidence for the Gold score, but the release/source timing is a strong maintenance signal.

The most recent default-branch commit returned in the inspected commit listing was dated 2026-08-24, including release-line fixes and application-version work. The separate repository `pushed_at` timestamp is later, so GitHub Gold does not infer a specific default-branch code change from that later timestamp without further inspection.

## Important maturity caveat

Upstream explicitly warns that PocketBase remains under active development and **full backward compatibility is not guaranteed before v1.0.0**.

This is not a reason to reject the project, but it materially changes how it should be used:

- pin versions in production;
- read migration/release notes before upgrading;
- avoid treating undocumented internals as stable APIs;
- design backups and rollback procedures before schema/application upgrades;
- and prefer documented extension surfaces when possible.

This caveat is the main reason the maintenance/stability dimension is not scored as perfect despite strong activity.

## Security and trust boundaries

PocketBase combines several sensitive responsibilities in one process:

- authentication;
- authorization/data-access rules;
- database access;
- file serving/storage;
- admin UI;
- realtime connections;
- optional JavaScript extension execution;
- backups;
- and custom user application code.

That compactness is operationally useful, but compromise of the process can therefore have a broad blast radius.

Upstream provides a security reporting policy and directs vulnerability reports privately.

A future security-oriented pass should inspect:

- auth token lifecycle and invalidation;
- record/collection access-rule evaluation;
- protected file authorization;
- admin/superuser boundaries;
- rate limiting;
- realtime subscription authorization and reconnect behavior;
- JavaScript VM capabilities;
- backup import/export boundaries;
- file upload validation;
- OAuth2 flows;
- and database transaction boundaries for batch operations.

## Deployment limitations and non-goals

PocketBase should not be automatically treated as a drop-in replacement for a horizontally distributed database/backend stack.

Questions that remain workload-dependent include:

- high write concurrency;
- active-active multi-node operation;
- database replication/failover;
- multi-region latency;
- very large data sets;
- storage durability;
- external object-storage semantics;
- and zero-downtime upgrade strategies.

The single-binary model is a feature, but it is also an architectural constraint.

## License review

The root `LICENSE.md` is the MIT License and grants broad permission to use, modify, redistribute, sublicense and sell copies, subject to preserving the copyright and permission notice in copies or substantial portions.

No PocketBase source was copied into GitHub Gold during this research pass.

Dependencies and embedded/generated frontend artifacts may have their own licensing requirements and should be reviewed before component extraction or redistribution.

## Verification performed by GitHub Gold

This pass inspected:

- repository metadata;
- README and documented build/test model;
- root MIT license;
- top-level source organization;
- the `apis/` source/test surface;
- realtime source/search evidence;
- current release metadata;
- recent commit metadata;
- and the GitHub Actions release/test workflow.

## Not independently verified

GitHub Gold did **not**:

- build PocketBase;
- run `go test ./...`;
- start the server;
- create a database;
- exercise collection rules;
- create/authenticate users;
- test OAuth2;
- upload/download files;
- open realtime SSE subscriptions;
- test auth invalidation on live connections;
- run the JavaScript VM plugin;
- perform backup/restore;
- benchmark SQLite concurrency;
- test multi-platform binaries;
- verify release asset checksums independently;
- fuzz API handlers;
- or perform a security audit.

Claims above are limited to inspected upstream source, documentation, release metadata and workflow evidence.

## High-value reusable components / ideas

1. **Single executable backend packaging** — useful reference for applications that need rich local/self-hosted services with minimal operational footprint.
2. **Go library + standalone server convergence** — a strong pattern for starting from an appliance-like binary and progressively embedding domain logic.
3. **Lifecycle/event hook architecture** — potentially reusable for extensible application frameworks.
4. **SSE realtime subsystem** — compact alternative pattern to a separate websocket/message-broker stack for many CRUD/event workloads.
5. **Collection/model rule system** — high-priority future source study for authorization-driven data APIs.
6. **Embedded admin UI packaging** — useful reference for shipping management surfaces in a single binary.
7. **Pure-Go SQLite deployment path** — useful for cross-platform, low-dependency server binaries.
8. **Go + JavaScript dual extension model** — potentially valuable for embedded products that need both compiled and scriptable customization.
9. **Backup/batch API implementations and tests** — useful candidates for deeper reliability/transaction research.
10. **Official SDK ecosystem** — useful for studying reconnect/auth/session semantics from the client side.

## Strong recursive leads

### `pocketbase/js-sdk`

Inspect authentication persistence, realtime SSE reconnect behavior, request cancellation, file upload handling and browser/Node/React Native portability.

### `pocketbase/dart-sdk`

Inspect equivalent mobile/desktop client semantics and offline/mobile lifecycle handling.

### JavaScript VM plugin

Map exactly what APIs/filesystem/network/process capabilities are available to server-side JavaScript and establish the real trust boundary.

### Record access rules

Trace a concrete request from authentication through collection/record rule evaluation to database query generation and response filtering.

### Realtime authorization

Trace subscription authorization, reconnect, token refresh/invalidation and record filtering end-to-end.

### Backup and batch transaction paths

Inspect atomicity, rollback, upload/import validation and failure recovery.

## Promotion recommendation

**VERIFIED — S / 28.**

PocketBase meets the GitHub Gold quality bar through concrete releases, active maintenance, broad tests, a permissive license, strong documentation, cross-platform binaries and an unusually reusable single-binary/library architecture.

The principal caveat is pre-1.0 API/backward-compatibility stability. Catalog wording should preserve that explicitly rather than presenting PocketBase as a frozen platform contract.
