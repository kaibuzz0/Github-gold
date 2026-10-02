# Syncthing `stdiscosrv` — self-hostable global discovery service

- Upstream repository: https://github.com/syncthing/syncthing
- Component: `cmd/stdiscosrv`
- Author/organization: Syncthing Project
- Category: peer-to-peer infrastructure / discovery / self-hosting / resilient networking
- Evidence level: VERIFIED
- Provisional Gold score: 27/30 (S)
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- Discovery: recursive follow-up from the Syncthing dossier

## What it is

`stdiscosrv` is Syncthing's standalone global discovery server. It lets Syncthing devices announce reachable addresses and lets peers look those addresses up by Syncthing device ID. It is valuable as both deployable self-hosted infrastructure and a concrete reference implementation of discovery for certificate-identified peer-to-peer systems.

This is not a separate repository; GitHub Gold catalogs it as a high-value component inside `syncthing/syncthing` rather than creating a misleading independent-project record.

## Why it matters

Peer-to-peer systems still need a rendezvous mechanism when peers do not already know usable addresses. `stdiscosrv` provides that discovery layer while remaining separable from Syncthing's file-transfer engine. It can therefore be studied as a compact service architecture involving device identity, ephemeral address records, TLS, rate control, persistence, replication, observability, graceful shutdown, reverse-proxy operation and container/system-service deployment.

For GitHub Gold, this is exactly the kind of useful subcomponent that should not be lost when cataloging only whole repositories.

## Working evidence inspected

Current upstream source contains the complete `cmd/stdiscosrv` implementation, dedicated API tests, a generated man page, a component README, systemd service material, UFW configuration and a dedicated Dockerfile.

Syncthing's current build workflow explicitly packages `syncthing`, `stdiscosrv` and `strelaysrv`, including Windows packaging. The generated `stdiscosrv(1)` man page currently identifies Syncthing v2.1.0 and is dated September 10, 2026.

The API test suite includes an in-process discovery server backed by the component database and exercises the HTTP handler. This is stronger evidence than documentation alone.

The parent repository remains actively maintained in September 2026, with current commits through September 14 in the evidence inspected during this pass.

## Architecture / useful technical pieces

Current `main.go` shows a supervised service tree and exposes several reusable patterns:

- native TLS service or plain HTTP operation behind an HTTPS reverse proxy;
- generated X.509 keypair when a configured keypair is absent;
- Syncthing device ID derived from the server certificate;
- in-memory database service with a configurable persistence directory and flush interval;
- optional S3-compatible blob storage for database backups;
- optional AMQP replication;
- optional Prometheus `/metrics` endpoint;
- configurable discovery API rate targets;
- signal-driven graceful shutdown with optional delay;
- service supervision using `suture`.

The API layer requests client certificates when serving TLS, requires TLS 1.2 or newer, supports HTTP/2 and HTTP/1.1, constrains read/write timeouts and maximum header size, and exposes lookup/announcement behavior over HTTP methods.

Address records have a two-hour expiry constant. The implementation also maintains separate retry/rate behavior for unknown devices versus devices that were seen previously. This is useful defensive architecture for a public discovery endpoint because negative lookups can otherwise become a large uncontrolled workload.

When configured behind an HTTP reverse proxy, the service derives the apparent client IP from `X-Forwarded-For` and optionally `X-Client-Port`. That mode therefore requires a trusted proxy boundary; exposing it directly while trusting attacker-controlled forwarding headers would be a deployment mistake.

## Specific files / components worth revisiting

- `cmd/stdiscosrv/main.go` — service composition, TLS, persistence, replication, metrics and shutdown
- `cmd/stdiscosrv/apisrv.go` — discovery HTTP API, lookup/announcement handling, compression and rate/retry behavior
- `cmd/stdiscosrv/apisrv_test.go` — handler/API regression tests
- `cmd/stdiscosrv/database.go` and related generated database structures — address-record storage and persistence
- `cmd/stdiscosrv/replication.go` — optional replication path
- `Dockerfile.stdiscosrv` — container build/deployment
- `cmd/stdiscosrv/etc/linux-systemd/` — service deployment examples
- `cmd/stdiscosrv/etc/firewall-ufw/stdiscosrv` — firewall profile; documents TCP 8443
- `man/stdiscosrv.1` — generated operator reference

## Platforms / requirements

Implementation language: Go. The component is built from the Syncthing source tree through the project's build system. Upstream packaging evidence covers multiple operating systems as part of the parent project's release machinery. A public deployment needs reachable TCP service infrastructure and should use correctly managed TLS or a trusted HTTPS reverse proxy.

Optional features add S3-compatible object storage, AMQP and Prometheus-compatible metrics consumers, but they are not required for the basic discovery role.

## Licensing

The component is part of `syncthing/syncthing` and source files carry Mozilla Public License 2.0 notices. MPL-2.0 is file-level copyleft. GitHub Gold copied no Syncthing source or generated artifacts in this pass; it records paths and architectural findings only.

Any future source extraction or adaptation must preserve applicable MPL notices and obligations.

## Verification boundary

GitHub Gold inspected current upstream source, tests, packaging/build references, deployment files, parent-repository activity and licensing. GitHub Gold did **not** compile or run `stdiscosrv`, execute its tests, expose a discovery endpoint, announce or query real device addresses, configure AMQP/S3 replication, scrape Prometheus metrics, validate production scale, inspect live network traffic, or independently audit its TLS/security properties.

`VERIFIED` here means the component's existence, architecture, tests, current integration into upstream builds and maintenance evidence were verified from primary repository sources. It does not mean runtime or production-scale behavior was independently reproduced.

## Caveats / risks

- Discovery metadata can reveal device reachability/address information; operation should be treated as infrastructure with privacy implications.
- HTTP-behind-proxy mode trusts forwarding metadata and therefore depends on a correctly isolated/trusted proxy boundary.
- Running a public rendezvous service creates abuse, availability, logging and capacity responsibilities.
- Optional replication and backup features expand the operational attack surface and credential-management burden.
- `stdiscosrv` is tightly associated with Syncthing's discovery protocol and device identity model; its architecture is reusable as a reference, but it is not a drop-in generic service-discovery framework.
- Synchronization data itself is not the discovery server's purpose; this component should not be represented as a file relay or storage server.

## Recursive research leads

1. Inspect `strelaysrv` next as the companion data-relay infrastructure and clearly separate discovery from relaying.
2. Map the global discovery protocol request/response schema and certificate/device-ID validation boundary.
3. Inspect database expiry, persistence and replication consistency behavior under failure.
4. Study negative-lookup retry/rate control and whether it generalizes to other rendezvous services.
5. Inspect Prometheus metrics for operational SLO/abuse-monitoring value.
6. Compare self-hosted discovery with local discovery and static device addresses to document when each path is useful.
7. Map privacy exposure: exactly which address metadata is announced, retained and returned, without operating against third-party infrastructure.
