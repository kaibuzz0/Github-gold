# Tailscale — WireGuard mesh networking stack

- **Repository:** https://github.com/tailscale/tailscale
- **Author / Org:** Tailscale Inc. / contributors
- **Category:** networking / VPN / WireGuard / NAT traversal / peer-to-peer / relay / DNS / remote access
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29 / 30
- **Provisional tier:** S
- **Discovery source:** GitHub-first breadth rotation
- **Research date:** 2026-09-13

## Score

| Dimension | Score | Notes |
| --- | ---: | --- |
| Utility | 5 | Practical encrypted connectivity across heterogeneous devices and networks. |
| Working evidence | 5 | Mature release stream plus extensive unit, integration, VM, NAT, security, and platform testing. |
| Reusability | 5 | Large set of separable networking packages: path selection, relay, DNS, netstack, NAT testing, control client, peer API, etc. |
| Novelty | 4 | Builds on WireGuard but adds substantial roaming, NAT traversal, relay, control, DNS, and userspace networking machinery. |
| Documentation | 5 | Clear repository overview, build instructions, public package structure, issue history, and extensive code comments/tests. |
| Maintenance | 5 | Active September 2026 development and current stable releases. |

**Total: 29 / 30 — S tier.**

## What it is

This repository contains most of Tailscale's open-source networking implementation, including the `tailscaled` daemon and `tailscale` CLI. Upstream documents daemon support for Linux, Windows, macOS, and varying support for FreeBSD/OpenBSD; the Android and iOS applications reuse code from this repository even though their GUI layers live elsewhere or are not fully open source.

At a high level, Tailscale turns WireGuard-based encrypted links into a practical roaming mesh by solving connectivity, peer discovery/control, NAT traversal, fallback relaying, DNS integration, route handling, and cross-platform host integration around the underlying tunnel.

## Why it qualifies as GitHub Gold

The repository is valuable less as a monolithic VPN application than as a collection of battle-tested networking components and test infrastructure.

Particularly strong research/reuse surfaces include:

- `wgengine/magicsock/` — adaptive transport/path-selection socket machinery. Its package documentation says it implements a socket that can change communication paths while in use and actively searches for the best way to communicate.
- `derp/` — implementation of Tailscale's Designated Encrypted Relay for Packets protocol. Upstream documents DERP as routing packets to clients using Curve25519 keys as addresses.
- `derp/derpserver/` and `derp/derphttp/` — relay server and HTTP/WebSocket-facing transport support.
- `control/controlclient/` — control-plane client/session logic.
- `net/dns/` — DNS configuration and resolver behavior across host environments.
- `wgengine/` — userspace networking engine and WireGuard integration.
- `net/netstack/` and related userspace-networking paths — useful for environments where kernel tunnel integration is not the desired model.
- `ipn/` / `ipn/ipnlocal/` — local node state, policy, routing, peer API, serving, and host integration.
- `tstest/natlab/` — virtualized NAT/network test laboratory.
- `tstest/integration/` — integration scenarios including VM and network behavior.
- `util/linuxfw/` — Linux firewall/routing support with namespace-aware tests for privileged paths.

These are useful references for mesh networking, changing-endpoint transport, NAT behavior, encrypted relays, DNS failure recovery, virtual networking, cross-platform tunnel integration, and realistic network test harnesses.

## Working evidence inspected

### Release evidence

GitHub releases show **v1.102.4** as a non-prerelease release published **2026-09-10**. Earlier 1.102.x and 1.98.x stable releases are also visible, indicating an active release train rather than a repository that only tracks unreleased development.

The GitHub release entries themselves contain source archives but point users to Tailscale's external changelog rather than attaching platform binaries to the GitHub release object. Therefore this dossier does **not** claim that GitHub release assets independently prove packaged desktop/mobile binaries.

### VM and NAT integration testing

The current `natlab-test` workflow is unusually strong evidence. Upstream explicitly states that it runs the full opt-in natlab/vmtest suite using QEMU VMs and vnet-driven networking scenarios.

The workflow:

- boots gokrazy, Ubuntu, and FreeBSD VM environments;
- runs on demand, on specifically labeled PRs, and every 12 hours;
- dynamically discovers test functions;
- prepares cloud VM images and a gokrazy VM image;
- enables KVM and installs QEMU in matrix jobs;
- runs each discovered test as its own job;
- maintains a separate basic NAT-lab canary workflow for ordinary PR coverage.

This is materially stronger than inferring working networking behavior from documentation alone.

### Broader testing/security signals

The workflow inventory also contains dedicated jobs for:

- CodeQL analysis;
- `golangci-lint`;
- `govulncheck`;
- NAT-lab basic and full testing;
- installer/build checks;
- pinned GitHub Actions policy checking.

Repository code search also exposes integration and privileged tests for VM execution, WebAssembly/browser paths, nftables rules in temporary network namespaces, DNS behavior, and large-tailnet benchmarking.

No claim is made here that every workflow is green on every commit; this pass inspected workflow definitions and test sources, not the complete historical CI result set.

## Maintenance evidence

Recent inspected commits from **2026-09-10 through 2026-09-11** include:

- tightening a local API development state-store endpoint so it requires local-admin authorization;
- adding `Retry-After` handling to control map sessions;
- DNS cache hardening so resolutions are persisted only after TLS verification;
- adding VM coverage for the `openresolv` Linux DNS backend;
- correcting peer-API address-family validation around masqueraded addresses;
- updating `x/crypto`, `x/mod`, and `x/tools` to incorporate 2026 vulnerability fixes;
- reducing retained WireGuard packet-buffer memory via an updated dependency.

These changes show active work in security boundaries, reliability, test coverage, memory behavior, and network edge cases.

## Install / runtime requirements

Upstream currently requires the latest Go release, documented as **Go 1.27** at inspection time. It states that the Tailscale-specific Go fork used for official releases is not required for ordinary builds.

The documented direct build route is effectively:

- build/install `tailscale.com/cmd/tailscale`;
- build/install `tailscale.com/cmd/tailscaled`.

Distribution packagers are directed to use `build_dist.sh` or equivalent logic so version/commit identifiers are embedded correctly.

Operational requirements vary by platform and by whether kernel TUN integration, userspace networking, subnet routing, exit-node behavior, DNS management, or containerized operation is used.

## Platforms and language

- **Primary language:** Go
- **Primary documented daemon platforms:** Linux, Windows, macOS
- **Additional documented support:** FreeBSD and OpenBSD to varying degrees
- **Mobile reuse:** repository code is used by Tailscale's Android and iOS applications
- **Special environments visible in repository/tests:** WebAssembly/browser-oriented code, VM test images, userspace networking

## License

The root repository license is **BSD 3-Clause**.

That is favorable for study and reuse, but file/dependency-level review is still required before extracting code because the repository depends on other components and separately maintained upstream projects such as WireGuard-related code.

No Tailscale source code was copied into GitHub Gold during this run.

## Important architectural caveat: open source does not equal the entire Tailscale service

The README explicitly says this repository contains the **majority** of Tailscale's open-source code and links to Tailscale's explanation of which parts are open source.

The macOS, iOS, and Windows products use this code but contain small GUI wrappers that are not all open source. The hosted coordination/control service is also not equivalent to this repository.

Therefore GitHub Gold should not describe `tailscale/tailscale` as a complete source drop of every component required to reproduce Tailscale's commercial hosted service.

For users interested in a fully self-hosted coordination plane, projects such as Headscale are a separate research lead and should be evaluated independently rather than conflated with upstream Tailscale.

## Security / trust notes

This is connectivity and remote-access infrastructure, so implementation mistakes can have significant consequences.

Useful security-sensitive study areas include:

- local API privilege checks;
- key and node identity handling;
- control-plane trust boundaries;
- DERP relay metadata and transport behavior;
- path-selection and endpoint discovery;
- DNS configuration/fallback behavior;
- subnet-router and exit-node filtering;
- peer API authorization;
- firewall/nftables/iptables integration;
- userspace netstack exposure;
- update/build supply-chain behavior.

The presence of CodeQL, `govulncheck`, security-related fixes, and extensive test infrastructure is positive evidence, but it is not equivalent to an independent security audit by GitHub Gold.

## Verification performed by GitHub Gold

Inspected:

- repository metadata and current default branch;
- current README/build/platform statements;
- root BSD-3-Clause license;
- current GitHub workflow inventory;
- the full NAT-lab VM-test workflow structure;
- package/source evidence for `magicsock` and DERP;
- representative test sources surfaced by repository search;
- latest GitHub release metadata;
- recent commit history through 2026-09-11;
- existing GitHub Gold default-branch catalog and current PR changed-file list for duplicate avoidance.

GitHub Gold did **not**:

- compile `tailscale` or `tailscaled`;
- execute unit, integration, NAT-lab, VM, browser, or firewall tests;
- create a tailnet;
- inspect encrypted packet captures;
- validate WireGuard cryptography;
- run a DERP server;
- test NAT traversal across real consumer routers/CGNAT networks;
- exercise subnet routing or exit nodes;
- audit the hosted control service;
- verify platform GUI wrappers;
- benchmark throughput, latency, roaming time, or relay performance;
- independently security-audit the codebase.

## Evidence boundary

**VERIFIED** here means that repository-native evidence strongly supports that the relevant software and major networking paths are actively built/tested and released. It does not mean GitHub Gold independently operated a production Tailscale network.

## Related projects / recursive leads

- `tailscale/wireguard-go` — WireGuard userspace implementation fork/dependency ecosystem.
- `tailscale/go` — release Go toolchain fork used upstream.
- `tailscale/tailscale-android` — Android application layer.
- `tailscale/tailscale-synology` — Synology packaging/integration.
- `tailscale/tailscale-qpkg` — QNAP packaging.
- `juanfont/headscale` — independently maintained open-source Tailscale-compatible coordination server; requires its own dossier and compatibility/security review.

## Strongest next research targets

1. **`wgengine/magicsock` path selection** — endpoint discovery, roaming, peer MTU, direct-vs-relay transition, rebind behavior, and failure recovery.
2. **DERP protocol/server** — framing, authentication/addressing, queue/backpressure behavior, WebSocket transport, abuse resistance, and relay observability.
3. **`tstest/natlab`** — extract the reusable ideas for deterministic NAT/topology simulation and cross-OS VM networking tests.
4. **Userspace netstack** — understand where Tailscale bridges WireGuard transport into userspace TCP/IP services and what can be reused independently.
5. **DNS resilience** — especially persisted resolution behavior, TLS-gated cache trust, split DNS, and bootstrapping when system DNS itself depends on the tunnel.
6. **Headscale comparison** — determine exactly which coordination functions are reproduced, compatibility boundaries, deployment maturity, migration risks, and license differences.
7. **Large-tailnet scaling** — inspect giant-tailnet benchmarks and memory/CPU behavior under large peer maps.

## Curator verdict

**KEEP — VERIFIED — S / 29.**

This is one of the strongest networking repositories for GitHub Gold because its value extends well beyond the end-user VPN product: it contains reusable examples of NAT traversal, roaming transport, encrypted relaying, host networking integration, DNS resilience, userspace networking, and unusually realistic network/VM testing. The principal caveat is architectural scope: the repository is not the entirety of Tailscale's hosted product or control plane.