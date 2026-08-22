# Self-Hosted Control Plane Research — 2026-08-21

## Candidate: Headscale

- **Repository:** https://github.com/juanfont/headscale
- **Author / Org:** Juan Font / Headscale contributors
- **Category:** self-hosted networking / Tailscale control plane / WireGuard coordination
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 28
- **License:** BSD-3-Clause

## What it does

Headscale is an open-source, self-hosted implementation of the Tailscale control server. It coordinates a single tailnet for personal, lab, or small-organization use by exchanging node public keys, assigning addresses, managing users and node registration, distributing routes and policy state, and speaking the control protocol used by Tailscale clients.

## Why it is valuable

Headscale is unusually useful as both a deployable self-hosting project and a reference implementation for private-network control-plane architecture. The Tailscale data plane remains WireGuard/peer-to-peer where possible; Headscale covers the coordination layer that the main Tailscale repository does not provide as an open hosted-service implementation.

The project also provides a concrete example of reimplementing an evolving external control protocol with integration testing, versioned configuration, policy handling, authentication, route distribution, and compatibility work across multiple client operating systems.

## High-value components / study targets

- `hscontrol` control-server and state-management layers
- node registration, re-registration, authentication, and follow-up flows
- pre-auth keys and tag authorization
- policy / ACL evaluation and distribution
- route and advertised-route coordination
- ephemeral-node lifecycle and garbage collection
- control-protocol polling / map-response handling
- OIDC and user authentication integrations
- DERP configuration / relay coordination interfaces
- API / CLI management surfaces
- protobuf definitions and generated API bindings
- configuration loading and versioned example configuration
- Nix development environment and Make-based build/test workflow
- integration-test infrastructure

## Verification performed

- inspected official README
- inspected root BSD-3-Clause license
- inspected repository metadata and current default branch
- located CI and integration-test workflows
- inspected recent upstream commit history and correctness fixes
- observed documented `make test`, `make build`, `make generate`, linting, formatting, and Nix development workflow
- did **not** independently deploy a Headscale server or tailnet
- did **not** run the test/integration suite
- did **not** benchmark control-plane scale or latency
- did **not** perform a security audit or compatibility matrix test

## Maintenance evidence

Recent upstream maintenance includes release 0.29.3 work and correctness fixes in late July 2026. Examples inspected include:

- authentication follow-up race handling that could turn a completed registration into a spurious 401 timeout
- preserving ephemeral-node garbage-collection timers when reconnect attempts fail before a successful connection
- authorization of re-authentication tags against the authenticating user
- applying new pre-auth-key tags correctly during re-registration
- development-shell test configuration fixes

These are substantive control/state correctness changes rather than documentation-only activity.

## Licensing and reuse

The root repository is BSD-3-Clause licensed, allowing modification and redistribution with copyright/license retention and the usual non-endorsement condition. Client binaries, Tailscale repositories, external identity providers, container bases, dependencies, and separately maintained integrations should be checked independently before reuse or redistribution.

## Caveats

Headscale intentionally targets a narrower scope than Tailscale's hosted service: one self-hosted tailnet suitable for personal use, labs, enthusiasts, or small open-source organizations. It is not an official Tailscale project and compatibility follows an external protocol that can evolve. The project README also explicitly says the maintainers do not support or encourage reverse proxies and containers as the preferred way to run Headscale, so deployment assumptions should follow current upstream documentation rather than generic self-hosting patterns.

## Relationship to existing Gold candidates

Headscale is complementary to the queued Tailscale entry rather than a duplicate. Tailscale provides the client/data-plane stack, userspace WireGuard integration, NAT traversal, DERP, and `tsnet`; Headscale provides a self-hosted control-plane implementation and therefore exposes different reusable architecture and operational patterns.

## Promotion recommendation

**READY — VERIFIED, provisional S / 28.** Promote as a distinct control-plane/self-hosting entry while cross-linking it to Tailscale.

## Strong recursive leads

- Headscale policy/ACL implementation details
- integration-test harness and client compatibility strategy
- OIDC/user lifecycle implementation
- DERP and route-distribution interactions
- Tailscale control-protocol types used by Headscale
- Headplane and other Headscale administration UIs, with separate license/quality review
