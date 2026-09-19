# Syncthing `strelaysrv` — Relay Server

- **Upstream:** https://github.com/syncthing/syncthing/tree/main/cmd/strelaysrv
- **Author / Org:** Syncthing Project
- **Category:** peer-to-peer infrastructure / NAT traversal / relay / self-hosting / networking
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27 / 30 — S
- **Scoring:** Utility 5; Working Evidence 5; Reusability 4; Novelty 4; Documentation 4; Maintenance 5
- **Discovery:** recursive follow-up from the Syncthing and `stdiscosrv` dossiers.

## What it is

`strelaysrv` is Syncthing's standalone relay server. It provides an intermediary data path when two Syncthing devices cannot establish a direct connection. It is distinct from global discovery: discovery helps devices find addresses, while the relay forwards traffic for a session.

Upstream documentation describes both public-pool and private operation. By default the server joins Syncthing's public relay pool and therefore may consume operator bandwidth for other users. Supplying an empty pool list disables that behavior. The normal protocol listener is port 22067; a separate status HTTP endpoint defaults to port 22070 and can be disabled.

## Valuable components and architecture

The current `cmd/strelaysrv` tree contains dedicated listener, session, pool and status implementations plus a relay test utility. The relay protocol definition lives under `lib/relay/protocol`; a relay client implementation used by the test utility lives under `lib/relay/client`.

Current server options expose:

- per-session and global byte-rate limiting;
- network, ping and message timeouts;
- an optional access token that prevents public-pool joining;
- external-address advertisement;
- TCP / TCP4 / TCP6 listener selection;
- optional UPnP / NAT-PMP mapping;
- configurable network buffers;
- optional status and pprof service;
- relay-pool registration;
- provider metadata.

The server attempts to raise its open-file limit and reserves a safety margin before deriving a connection limit. It generates a long-lived X.509 key pair when one is absent. Current TLS configuration requests client certificates, disables session tickets, advertises the Syncthing relay protocol via ALPN, and requires TLS 1.2 or newer.

The generated relay URI can include the server certificate-derived ID and operating parameters. Upstream documentation notes that omitting the ID gives up certificate pinning, so private deployments should retain the identity parameter when practical.

## Working evidence

Evidence inspected rather than merely relying on project claims:

- the current repository contains the complete relay implementation (`listener.go`, `session.go`, `pool.go`, `status.go`, `main.go`);
- the tree contains `testutil`, documented as a two-party connectivity test for a relay server;
- upstream documents a concrete public-pool and private-relay deployment workflow;
- the relay is maintained inside the actively developed Syncthing monorepo, whose recent commits continue through September 2026.

This supports **VERIFIED** at the repository-evidence level. GitHub Gold did not independently run the relay.

## Deployment / runtime

Go-based component distributed as part of the Syncthing source tree. Public operation normally requires TCP 22067 reachable from the internet. The optional status service defaults to 22070. NAT traversal support can use UPnP/NAT-PMP when explicitly enabled.

A private server can be configured in Syncthing using its `relay://...` URI rather than joining the public pool.

## License

`cmd/strelaysrv/LICENSE` is a dedicated **MIT License**, copyright the Syncthing Project. This is an important component-level distinction from the broader Syncthing repository's MPL-2.0 licensing. Any extraction should preserve the MIT copyright and permission notice, while dependencies imported from elsewhere in the monorepo must still be reviewed under their own applicable licensing.

No upstream source was copied into GitHub Gold.

## Caveats / risks

- Default operation joins the public relay pool and can consume significant bandwidth; private operators should deliberately configure pool behavior.
- Internet-facing relay and status endpoints require normal server hardening, firewalling, monitoring and update practices.
- Relaying is a fallback transport path, not a discovery service and not persistent file storage.
- Certificate pinning is weakened if operators use a relay URI without its identity parameter.
- Rate limits, descriptor limits, buffers and timeouts materially affect capacity and resource consumption.
- The README contains historical example output; current source is a better authority for current implementation details.

## Verification boundary

GitHub Gold inspected current upstream source-tree structure, README, component license, main server configuration/TLS setup and recent monorepo maintenance signals. It did **not** compile or execute `strelaysrv`, run `testutil`, proxy real Syncthing traffic, join the public pool, benchmark bandwidth/concurrency, test NAT traversal, inspect live TLS traffic, or independently audit the relay protocol/security implementation.

## Why it is Gold

The value is not merely "another server." `strelaysrv` is a mature example of a self-hostable rendezvous-assisted relay: identity-bearing relay URIs, certificate-aware transport, session brokerage, bandwidth controls, connection/resource accounting, NAT mapping, public-pool federation and observable status. Together with `stdiscosrv`, it gives GitHub Gold a concrete discovery-versus-relay architecture pair for resilient peer-to-peer systems.

## Strong next leads

1. Map `lib/relay/protocol` message framing and session state machine.
2. Inspect `lib/relay/client` and the connection negotiation boundary used by Syncthing proper.
3. Trace rate limiting and backpressure through `session.go` and `listener.go`.
4. Inspect pool admission/health checks and how relay selection consumes advertised metrics.
5. Compare direct, global-discovery-assisted and relay-assisted connection paths.
6. Examine the dedicated test utility and any relay-related CI/tests for failure-mode coverage.
7. Build a concise `stdiscosrv` vs `strelaysrv` deployment/privacy/threat-model matrix.