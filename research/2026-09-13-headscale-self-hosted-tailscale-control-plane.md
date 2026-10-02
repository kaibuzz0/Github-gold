# Headscale — self-hosted Tailscale-compatible control plane

- **Repository:** https://github.com/juanfont/headscale
- **Author / Org:** Juan Font / Headscale contributors
- **Category:** self-hosting / mesh networking / WireGuard coordination / identity / policy / DNS / DERP
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **Discovery source:** Recursive follow-up from `tailscale/tailscale`
- **Research date:** 2026-09-13

## Score

| Dimension | Score | Notes |
| --- | ---: | --- |
| Utility | 5 | Makes a Tailscale-compatible coordination plane self-hostable for personal, lab, and small-organization use. |
| Working evidence | 5 | Stable releases plus substantial integration testing against Headscale and real Tailscale client images. |
| Reusability | 5 | Control-plane, policy, OIDC, DNS, registration, routing, DERP, state, database, and integration-test components are separable research targets. |
| Novelty | 4 | Reimplements a proprietary hosted control-plane role against an evolving external client ecosystem. |
| Documentation | 5 | Strong stable/development docs, compatibility matrix, example configuration, build/test guidance, and changelog. |
| Maintenance | 4 | Active September 2026 development; latest stable release inspected is from July 2026. |

**Total: 28 / 30 — S tier.**

## What it is

Headscale is an open-source, self-hosted implementation of the control-server role used by Tailscale clients. It does not replace WireGuard packet transport itself. Instead, it handles coordination functions such as node registration, identity, address assignment, policy-derived visibility, routes, DNS configuration, and distribution of peer/network state to compatible clients.

Upstream explicitly scopes Headscale toward self-hosters, hobbyists, labs, and a single tailnet/small organization rather than claiming feature-for-feature equivalence with Tailscale's commercial hosted control service.

That scope distinction matters: Headscale is valuable precisely because it exposes an independently maintained implementation of an otherwise hosted coordination-plane problem while remaining honest about unsupported features and compatibility boundaries.

## Why it qualifies as GitHub Gold

Headscale is a strong research target for control-plane design, protocol compatibility, identity integration, network-policy evaluation, and realistic cross-version integration testing.

Useful component surfaces include:

- `hscontrol/` — core server/control-plane implementation;
- `hscontrol/state/` — node/network state and change propagation;
- policy/ACL/Grants evaluation and peer-visibility calculation;
- node registration and pre-authenticated key flows;
- OIDC authentication and profile synchronization;
- MagicDNS, split DNS, search domains, and custom DNS records;
- subnet-route and exit-node management;
- embedded DERP support and peer-relay integration;
- database/storage abstractions, including SQLite/PostgreSQL paths visible in integration infrastructure;
- generated protobuf/API surfaces;
- integration harnesses that exercise real Tailscale client images against Headscale.

This is especially useful beside the `tailscale/tailscale` dossier: Tailscale supplies most of the open-source client/networking stack, while Headscale independently implements the coordination layer needed for a self-hosted deployment.

## Feature/compatibility evidence

The current upstream feature matrix documents support for:

- base Tailscale functionality;
- web and pre-authenticated-key node registration;
- MagicDNS, split DNS, search domains, and additional DNS records;
- Taildrive and Taildrop;
- tags;
- subnet routers and exit nodes;
- route filtering using `via`;
- IPv4/IPv6 dual stack;
- ephemeral nodes;
- an embedded DERP server;
- peer relays;
- ACLs and Grants;
- selected autogroups;
- route/exit-node auto-approvers;
- Tailscale SSH policy;
- node attributes;
- policy tests and SSH tests;
- OIDC registration and identity-provider profile updates.

The same document explicitly marks important gaps rather than implying complete parity. At inspection time, OIDC groups could not be used directly in ACLs, and Funnel, Serve, and network flow logs were still unsupported.

That explicit compatibility accounting is positive evidence for the project's maturity and makes the repository easier to evaluate than projects that only advertise success cases.

## Working evidence inspected

### Release evidence

GitHub's latest-release API reports **v0.29.3**, published **2026-07-29**, as the latest non-prerelease release at inspection time.

The release publishes checksums, source archives, and platform artifacts including Linux, macOS, FreeBSD, and package formats. GitHub exposes SHA-256 digest metadata for release assets. This supports the narrower claim that the project maintains a real packaged release process; GitHub Gold did not independently reproduce those binaries.

### Integration testing

The current reusable integration-test workflow is unusually strong evidence because it does not only run unit tests against mocks.

The workflow:

- builds/loads a Headscale image;
- loads a Tailscale `HEAD` client image;
- loads released Tailscale client images;
- optionally loads PostgreSQL for database-specific runs;
- executes named integration tests through the project's `hi` integration-test runner;
- sets explicit memory limits for Tailscale and Headscale test containers;
- preserves logs and other test artifacts;
- supports debugging through an authenticated Tailscale network when CI secrets are available;
- contains special environment setup for tests such as the Kubernetes operator path.

Testing Headscale against both current-development and released Tailscale client images is particularly valuable because protocol compatibility is the core product requirement.

The repository workflow inventory also includes build checks, generated-code checks, test checks, documentation tests, Nix checks/module tests, container builds, integration workflow generation, and release automation.

This dossier does **not** claim every workflow was independently executed by GitHub Gold or that every historical CI run passed.

## Maintenance evidence

Recent inspected commits through **2026-09-10** show active work in state propagation and runtime hardening.

Examples include:

- reducing map-request broadcasts to the narrowest justified update rather than resending complete node state;
- avoiding unnecessary state snapshots for unchanged node-health cycles;
- reusing immutable peer-adjacency data when visibility cannot change;
- ensuring changed peers are filtered through recipient adjacency so policy-hidden nodes are not delivered;
- adding integration coverage that pins which Hostinfo changes should propagate to peers;
- changing container runtime handling so `/tmp` is backed by tmpfs in relevant deployments.

This is substantive maintenance in scalability, policy correctness, state-diff behavior, integration coverage, and deployment semantics rather than cosmetic repository churn.

## Architecture and trust boundaries

Headscale is security-sensitive infrastructure because it determines which nodes learn about which other nodes and distributes network configuration used by clients.

Important study surfaces include:

- node identity and registration;
- pre-authenticated keys;
- OIDC authorization and account mapping;
- policy/ACL/Grant evaluation;
- peer-visibility adjacency and incremental state updates;
- route and exit-node approval;
- DNS configuration distribution;
- embedded DERP operation;
- API authorization;
- database migrations and consistency;
- compatibility with changing Tailscale client protocol behavior.

A flaw in these layers can affect confidentiality, reachability, routing, or policy isolation even though the underlying WireGuard cryptography lives primarily in the client/networking stack.

## Install / runtime requirements

Upstream recommends using Nix for a reproducible development environment. Contributing/building currently requires Go, Buf, and protobuf tooling.

Documented development commands include:

- `nix develop`;
- `make generate` when protobuf definitions change;
- `make test`;
- `make build`.

Operational deployment guidance should be taken from the documentation matching the exact release tag. The README explicitly warns that `main` may contain unreleased configuration changes.

Upstream also currently says reverse-proxy and container deployments are not supported or encouraged as the preferred operating model, even though container-related build/test infrastructure exists. That deployment caveat should not be silently ignored by downstream users.

## Platforms and language

- **Primary language:** Go
- **Server environment:** primarily Linux/server-oriented self-hosting, with release artifacts for additional platforms
- **Client ecosystem:** Tailscale clients on supported operating systems connect to Headscale rather than Headscale shipping its own full replacement client stack
- **Storage paths:** SQLite and PostgreSQL are represented in project/integration infrastructure
- **Build tooling:** Go, Nix, Buf/Protobuf, Make

## License

The repository root is **BSD 3-Clause**, copyright Juan Font.

This is favorable for study and reuse subject to attribution/notice requirements and dependency-level license review.

No Headscale source code was copied into GitHub Gold during this run.

## Important compatibility caveats

Headscale is **not** a drop-in open-source copy of every hosted Tailscale feature.

Upstream explicitly targets a narrower use case and publishes a live feature matrix showing both implemented and missing capabilities. At inspection time notable missing/incomplete items included:

- OIDC groups usable directly in ACLs;
- Funnel;
- Serve;
- network flow logs.

Compatibility also depends on changes in the upstream Tailscale client/control protocol. This is why Headscale's strategy of integration testing against both Tailscale HEAD and released client versions is significant.

## Verification performed by GitHub Gold

Inspected:

- current repository metadata/default branch;
- README and stated design scope;
- root BSD-3-Clause license;
- current feature/compatibility matrix;
- workflow inventory;
- reusable integration-test workflow internals;
- latest GitHub release metadata and asset digests;
- recent commit history through 2026-09-10;
- existing GitHub Gold master catalog and active PR changed-file set for duplicate avoidance;
- related Tailscale dossier to avoid conflating client/network stack and control-plane roles.

GitHub Gold did **not**:

- compile Headscale;
- execute unit or integration tests;
- deploy a Headscale server;
- connect real Tailscale clients;
- test OIDC providers;
- exercise ACL/Grant isolation on a live network;
- run the embedded DERP server;
- test subnet routers or exit nodes;
- validate SQLite/PostgreSQL migration behavior;
- benchmark large-tailnet scale;
- reproduce release binaries;
- independently security-audit the control protocol or server.

## Evidence boundary

**VERIFIED** here means repository-native evidence strongly supports that Headscale is actively maintained, released, and tested for compatibility against real Tailscale client images. It does not mean GitHub Gold independently operated a production Headscale deployment.

## Related projects / recursive leads

- `tailscale/tailscale` — open-source client/networking implementation and protocol counterpart already cataloged in this research branch;
- Tailscale DERP implementation — useful for comparing embedded Headscale relay behavior with upstream components;
- Headscale web/admin UIs — should be evaluated separately because they may have different maintainers, security boundaries, and licenses;
- identity-provider integrations — OIDC behavior deserves provider-specific compatibility/security study;
- Kubernetes operator integration tests — interesting as an orchestration/control-plane reuse lead.

## Strongest next research targets

1. **Map/state delta machinery** — how Headscale translates state changes into full or incremental client updates and where policy changes force recomputation.
2. **Policy engine** — ACL/Grant/autogroup semantics, visibility adjacency, route auto-approval, and regression coverage.
3. **Protocol compatibility testing** — inspect the `hi` runner and version matrix to understand how client regressions are detected.
4. **OIDC/session security** — authentication caches, callback handling, account linking, profile synchronization, expiry, and replay boundaries.
5. **DERP/peer relay behavior** — determine what is reused from Tailscale versus independently configured/implemented.
6. **Database correctness** — SQLite/PostgreSQL consistency, migrations, transaction boundaries, and backup/restore behavior.
7. **Large-tailnet behavior** — evaluate incremental map updates, adjacency memory, database pressure, and reconnect storms at scale.

## Curator verdict

**KEEP — VERIFIED — S / 28.**

Headscale is high-value GitHub Gold because it exposes a practical, independently maintained implementation of a modern encrypted-mesh coordination plane and backs compatibility claims with meaningful integration testing against real upstream Tailscale client images. Its main caveat is also one of its strengths as a research artifact: it does not pretend to reproduce every commercial Tailscale feature, and its documented compatibility matrix should be treated as part of the technical contract.