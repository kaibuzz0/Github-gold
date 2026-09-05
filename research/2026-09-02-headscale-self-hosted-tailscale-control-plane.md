# Headscale: self-hosted Tailscale coordination and control plane

- **Repository:** https://github.com/juanfont/headscale
- **Author / Org:** Juan Font / contributors
- **Category:** self-hosted networking control plane / WireGuard coordination / Tailscale-compatible control server / identity and policy distribution
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28/30 (S)
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **License:** BSD-3-Clause
- **Discovery:** recursive lead from the Tailscale dossier; GitHub-first verification; no YouTube transcript claim used

## What it is

Headscale is an open-source, self-hosted implementation of the Tailscale control server. Upstream describes the control-server role as the coordination point that exchanges WireGuard public keys, assigns client IP addresses, maintains user/network boundaries, enables machine sharing, and distributes advertised routes.

The project deliberately targets a narrower scope than Tailscale's hosted service: a single tailnet suitable for personal use, labs, hobbyists, and relatively small open-source organizations. That scope limitation is important and should not be hidden behind the phrase "self-hosted Tailscale."

Headscale does not replace the peer-to-peer encrypted data plane implemented by Tailscale clients. Its value is in making the coordination/control plane independently operable.

## Why it qualifies as GitHub Gold

Headscale is valuable as both deployable infrastructure and reference architecture for a network coordination service. The repository exposes distinct subsystems around:

- node enrollment and registration;
- API-key and pre-auth-key handling;
- user and device lifecycle;
- policy / ACL parsing and distribution;
- route advertisement and coordination;
- persistent node/network state;
- Tailscale protocol compatibility;
- Noise-based client/control communication;
- DERP-related configuration and coordination;
- metrics and health endpoints;
- CLI and API surfaces;
- database-backed state;
- integration-test orchestration against real Tailscale clients.

This makes the project technically useful beyond simply installing a binary. It is a concrete example of separating an overlay network's encrypted peer transport from the identity, enrollment, addressing, policy, and topology metadata needed to make that transport operational.

## Control-plane boundary

The repository README is explicit about the architectural boundary. Tailscale clients form the WireGuard-based overlay, while the control server exchanges peer keys, assigns addresses, represents users, exposes routes, and coordinates the network.

For GitHub Gold, that separation is the central finding: the data path remains with the clients, while Headscale controls membership and distributes the state needed for peers to find and authorize one another.

This is the natural recursive companion to the existing `tailscale/tailscale` dossier. Tailscale's `tsnet`, `magicsock`, WireGuard engine, DERP client, STUN, and NAT traversal components cover the node/data-plane side; Headscale provides an independently deployable coordination-plane implementation.

## Source and component structure

The current repository contains a substantial `hscontrol/` tree with dedicated API, database, policy, mapper, state, type, and utility surfaces plus extensive tests. The inspected tree includes explicit tests for:

- API-key management;
- authentication middleware;
- nodes/devices;
- users;
- pre-auth keys;
- policy / ACL behavior;
- OAuth flows;
- API v1 and v2 surfaces;
- database behavior;
- state persistence;
- polling / stream behavior;
- configuration-secret redaction;
- concurrency-sensitive policy behavior.

The existence of these separable packages and test surfaces makes Headscale more reusable as design/reference material than a thin compatibility shim.

## Integration testing is a first-class project concern

Headscale's own project material highlights integration testing as a core technique for reimplementing Tailscale behavior. The repository maintains a dedicated `integration/` tree and generated GitHub Actions integration-test machinery, not merely isolated unit tests.

The current code search also shows integration CLI tests split across users, nodes, API keys, pre-auth keys, auth, server, and policy behavior. A current HA property test explicitly notes the cost of performing real Noise handshakes during repeated reconnect checks, which is useful evidence that the test surface exercises protocol-level behavior rather than exclusively mocking it.

The working-evidence score therefore reflects source/test infrastructure and upstream CI intent, not GitHub stars.

## CI, build, and release infrastructure

The current GitHub Actions inventory includes separate workflows for:

- normal builds;
- generated-code consistency;
- test checks;
- container builds from `main`;
- documentation tests and deployment;
- Nix checks;
- Nix module tests;
- release generation;
- generated integration-test matrices;
- repository automation and maintenance tasks.

The README documents a reproducible development path using Nix and the standard project commands:

- `make generate`
- `make test`
- `make build`

It also documents required Go, Buf, and Protobuf tooling and specific formatting/linting rules for Go, Proto, docs, Markdown, and YAML.

This is strong working evidence even though GitHub Gold did not execute those commands locally during this pass.

## Release and maintenance state

The latest stable GitHub release inspected was **v0.29.3**, published **July 29, 2026**. The release includes a checksum manifest and multiple binary/package artifacts, including Linux, macOS, FreeBSD, and Debian package targets.

Development remains current through at least **September 2, 2026 UTC**. Recent commits include:

- documentation and setup fixes for current tvOS/Tailscale behavior;
- correction of HTTP metrics collection for ordinary non-OPTIONS traffic;
- adaptation to Tailscale protocol/type changes;
- an update to the `tailscale.com` dependency based on a 1.103 development snapshot;
- Go 1.27 toolchain compatibility work;
- Nix/toolchain maintenance.

The Tailscale dependency updates are especially important: compatibility with an independently evolving client/control protocol is an ongoing maintenance obligation, not a one-time reverse-engineering task.

## License and reuse boundary

The root repository license is **BSD 3-Clause**. Reuse or adaptation must preserve the copyright notice, license conditions, and disclaimer, and contributor names may not be used to imply endorsement.

No Headscale source code was copied into GitHub Gold during this research pass.

## Operational and architectural caveats

### Narrow scope by design

Upstream explicitly says Headscale targets one tailnet and is intended primarily for personal use, labs, hobbyists, and relatively small organizations. Do not assume feature or scale parity with the hosted Tailscale control service.

### Client compatibility is an external moving dependency

Headscale intentionally interoperates with Tailscale clients and imports the `tailscale.com` Go module. Changes in Tailscale protocols, capability types, registration behavior, or clients can therefore require corresponding Headscale updates.

### Versioned configuration matters

The README warns users to consult the example configuration from the same GitHub tag as the released version being deployed because `main` can contain unreleased configuration changes.

### Deployment guidance is opinionated

Upstream explicitly states that reverse proxies and containers are not supported or encouraged as the preferred way to run Headscale. This should be preserved rather than assuming a conventional "put every self-hosted service behind Docker + reverse proxy" deployment model.

### Control-plane compromise is high impact

Because the service controls node enrollment, addresses, peer metadata, routes, policy, and key-distribution metadata, compromise of the control plane can affect the trust and topology of the tailnet even though peer traffic is transported by Tailscale/WireGuard clients. Administrative APIs, pre-auth keys, OAuth/OIDC configuration, database access, TLS/Noise endpoints, and backups therefore deserve strong protection.

## Verification performed by GitHub Gold

This pass inspected:

- current repository README and stated design goal;
- root BSD-3-Clause license;
- current source-tree structure, especially `hscontrol/`;
- API/auth/policy/database/state test surfaces;
- current GitHub Actions workflow inventory;
- latest stable GitHub release metadata and checksum artifact presence;
- current upstream commit history through September 2, 2026;
- the existing Tailscale dossier to avoid treating Headscale as part of the Tailscale repository itself.

## Not verified locally

GitHub Gold did **not**:

- build Headscale;
- run `make test`, `make build`, or generated-code checks;
- deploy a Headscale server;
- enroll Tailscale clients;
- perform a real Noise handshake;
- test MagicDNS, ACLs, routes, exit nodes, DERP configuration, pre-auth keys, OIDC/OAuth, or API authentication;
- exercise SQLite/PostgreSQL persistence or migrations;
- run integration matrices against multiple Tailscale client versions;
- verify release checksums independently;
- benchmark scale, memory, latency, or database behavior;
- perform a security audit.

Claims here are therefore source/repository/upstream-evidence claims, not local operational certification.

## Strong recursive leads

1. **`hscontrol/mapper`** — how control-plane state becomes client network maps and incremental updates.
2. **Policy / ACL engine** — parser, validation, concurrency, rule expansion, and compatibility with Tailscale policy semantics.
3. **Noise control protocol** — client registration, authenticated control sessions, reconnect behavior, and key lifecycle.
4. **Integration test harness** — reusable infrastructure for testing a compatibility implementation against real Tailscale clients and versions.
5. **Database/state layer** — SQLite/PostgreSQL behavior, migrations, node expiry, routes, users, and persisted coordination state.
6. **Pre-auth/API/OAuth key handling** — scope, revocation, expiration, and secret-storage boundaries.
7. **DERP and route coordination** — what Headscale distributes versus what is executed by Tailscale clients.
8. **Client-version compatibility matrix** — determine exactly which Tailscale releases/platforms are currently supported and where incompatibilities appear.

## Promotion recommendation

**VERIFIED / S / provisional 28.**

Promote atomically into the synchronized catalog surfaces when the current draft research batch enters its catalog-promotion phase. Headscale is strong Gold as an independently maintained coordination/control-plane implementation, but its narrow single-tailnet scope and dependence on continued Tailscale protocol compatibility justify keeping its score below the existing Tailscale data-plane repository score.
