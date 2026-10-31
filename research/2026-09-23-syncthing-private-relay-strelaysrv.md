# Syncthing `strelaysrv`: self-hosted private relay infrastructure

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `cmd/strelaysrv`, `lib/relay/protocol`, `lib/relay/client`
- **Category:** local-first / synchronization / networking / self-hosting / relay infrastructure
- **Evidence:** VERIFIED (source/documentation evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** **29 / 30 — S**
  - Utility: 5
  - Working evidence: 5
  - Reusability: 5
  - Novelty: 4
  - Documentation: 5
  - Maintenance: 5
- **License:** MPL-2.0
- **Discovery:** recursive follow-up from the Syncthing and private-discovery dossiers

## What it is

`strelaysrv` is the relay server shipped in the main Syncthing repository. It provides an intermediate transport path for Syncthing peers that cannot establish a usable direct connection. This is distinct from `stdiscosrv`: discovery tells peers where another device can be reached; a relay can carry the peer-to-peer connection when direct reachability fails.

The implementation and README explicitly support private operation. The important default is also explicit: an unmodified relay server joins Syncthing's default public relay pool. Operators who want a private relay must opt out of pool registration, for example with `-pools=""`.

## Private-operation controls verified in source

Current `cmd/strelaysrv/main.go` exposes:

- `-listen` for the relay protocol listener (default `:22067`);
- `-status-srv` for the optional HTTP status service (default `:22070`, blank disables it);
- `-pools` for relay-pool registration;
- `-token` for restricting relay access; source states that setting a token also disables joining pools;
- `-ext-address` to advertise an externally forwarded address/port;
- `-per-session-rate` and `-global-rate` bandwidth controls;
- network, ping and message timeouts;
- optional UPnP/NAT-PMP external port mapping;
- protocol selection for TCP/IPv4/IPv6;
- optional profiling on the status service;
- network-buffer sizing.

If `cert.pem` and `key.pem` cannot be loaded, the server generates an X.509 keypair. It derives the relay device ID from that certificate and includes the ID plus operational parameters in the advertised `relay://` URI.

## Public-pool safety behavior

The source has a conspicuous runtime warning when the default public pool is selected, explaining that the relay will be available for public use and instructing operators to use `-pools=""` for private operation. The README repeats the same warning.

This is operationally important: simply launching `strelaysrv` with defaults is not equivalent to creating a private relay.

When `-token` is non-empty, source clears `poolAddrs`, so token-restricted operation cannot simultaneously register into the configured relay pools through this path.

## Client integration

The upstream README documents a private-relay workflow:

1. start `strelaysrv`;
2. obtain the generated `relay://...` URI;
3. replace/define the host with the externally reachable relay address where needed;
4. add that relay URI to Syncthing's **Sync Protocol Listen Address** configuration.

The full URI can carry the relay certificate-derived ID, which supports certificate pinning. The README also shows a shortened host-only relay URI, but explicitly describes certificate pinning as the more secure option.

## Reachability and status surface

For an internet-facing private relay, the README documents TCP port 22067 as the relay service port and notes that NAT/firewall forwarding may be necessary. The optional status endpoint defaults to port 22070 and reports operational metrics such as transfer rates and connection/session counts; it can be disabled with `-status-srv=""`.

The relay server also has resource controls in source: it attempts to raise the open-file limit, tracks active connections/proxies, refuses or drops idle/new work when descriptor pressure exceeds its calculated limit, and can apply global/per-session byte-rate limits.

## Useful reusable components

- `cmd/strelaysrv` — deployable relay server and operational control surface.
- `lib/relay/protocol` — relay protocol definitions used by the server.
- `lib/relay/client` — relay client implementation used by upstream relay test tooling.
- relay `testutil` — documented connectivity utility for joining two certificate-backed test endpoints through a relay.
- NAT service integration — optional UPnP/NAT-PMP mapping path.
- status/metrics surface — useful for relay observability and capacity monitoring.

## Why it matters for GitHub Gold

Together with Syncthing's static/local discovery and self-hosted `stdiscosrv`, `strelaysrv` completes the major infrastructure pieces needed to understand a privately controlled Syncthing topology. A deployment can avoid dependence on the public relay pool by explicitly configuring private relay URIs and disabling pool registration.

This does **not** mean a relay is always required. Reachable peers can communicate directly; the relay is an alternate transport path for cases where direct connectivity is unavailable or unsuitable.

## License / reuse

Syncthing is MPL-2.0. Covered source files and modifications distributed in source form remain subject to MPL-2.0 obligations, and notices must be preserved. No upstream implementation code was copied into GitHub Gold; this dossier records architecture and exact upstream locations.

## Verification performed

GitHub Gold inspected:

- current upstream `cmd/strelaysrv/main.go`;
- current upstream `cmd/strelaysrv/README.md`;
- current repository license;
- repository search evidence for the relay test utility and client configuration path.

These sources directly support the existence of private/public pool controls, token restriction, generated certificates, rate limiting, NAT options, status service, relay URI generation, client configuration, and the documented relay connectivity test utility.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- compile or execute `strelaysrv`;
- run the relay test utility;
- establish two Syncthing peers through a private relay;
- inspect live relay traffic;
- validate NAT-PMP/UPnP behavior;
- benchmark throughput, latency, descriptor limits, memory use or rate limiting;
- independently audit TLS, certificate pinning, relay protocol security or cryptography.

All working claims above are therefore source/upstream-documentation evidence, not an independent runtime validation.

## Caveats

- **Default launch is public-pool oriented.** A private operator must deliberately disable pool registration or use token-restricted operation.
- A relay adds another network hop and therefore capacity/availability requirements; direct peer connectivity remains preferable where practical.
- Internet-facing deployments require correct firewall/NAT exposure and normal server-hardening practices.
- The README contains historical example output; current behavior should be taken from current source/`-help` rather than assuming every old example field remains unchanged.
- MPL-2.0 obligations apply to covered source reuse/modification.

## Strongest follow-up

The Syncthing infrastructure thread is now sufficiently mapped: direct/static addressing, local/global discovery, self-hosted `stdiscosrv`, BEP synchronization, and private/public relay behavior have all been inspected. Future work should rotate into a different category unless materially new upstream evidence changes this architecture.