# WireGuard Userspace Research — 2026-08-21

## Candidate

### WireGuard/wireguard-go

- **Repository:** https://github.com/WireGuard/wireguard-go
- **Author / Org:** WireGuard LLC / WireGuard contributors
- **Category:** userspace VPN / encrypted networking / Go networking / TUN interface
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 28
- **License:** permissive MIT-style license embedded in the upstream README and root LICENSE

## What it does

`wireguard-go` is the official Go userspace implementation of WireGuard. It exposes a WireGuard interface without requiring the Linux kernel implementation and supports Linux, macOS, Windows, FreeBSD, and OpenBSD, with platform-specific TUN/utun integration.

Upstream explicitly recommends the kernel implementation on Linux when available because it is faster and better integrated, which is an important boundary for how this project should be evaluated: its strongest value is portability, embeddability, userspace integration, and reference implementation work rather than replacing the kernel path everywhere.

## Why it is GitHub Gold

The repository is small enough to study directly yet contains unusually high-value networking primitives used by real production software. It is also directly relevant to the current Tailscale research branch: Tailscale maintains its own fork while upstream WireGuard remains the canonical implementation lineage.

The project is valuable both as a working userspace VPN implementation and as a reference for building secure packet-processing software around a virtual network interface.

## High-value components

- `device/` — WireGuard protocol engine, handshake state, peer lifecycle, encryption/decryption pipeline, packet queues, AllowedIPs handling, replay protection integration, timers, and device configuration logic.
- `conn/` — UDP endpoint and socket abstraction, bind logic, batching/vectorized I/O, platform-specific networking behavior, and GRO/GSO-related handling.
- `tun/` — TUN device interfaces plus platform-specific virtual-interface plumbing and packet offload/batching support.
- `ipc/` — userspace control interface compatible with standard WireGuard tooling.
- `ratelimiter/` — handshake-rate limiting primitives.
- `replay/` — anti-replay window logic.
- `rwcancel/` — cancellable file-descriptor I/O helpers.
- `tai64n/` — timestamp representation used by the protocol.
- `tests/` and package test files — implementation correctness and regression surfaces.
- `main.go` / platform entry points — compact example of composing the protocol engine, TUN interface, IPC control path, and lifecycle management.

## Verification performed

- Official upstream README inspected.
- Root repository structure inspected, including protocol, connection, TUN, IPC, replay, rate-limiter, cancellation, timestamp, and test areas.
- Upstream licensing text inspected.
- Recent commit history inspected.
- A May 22, 2026 upstream fix for Linux vectorized I/O / TUN header cleanup was observed.
- May 2025 upstream work was inspected covering UDP GRO compatibility, message encoding/decoding performance, AllowedIPs configuration, handshake allocation reduction, and poll-event correctness.

GitHub Gold did **not** independently build, fuzz, benchmark, deploy, cryptographically audit, or interoperability-test `wireguard-go` in this pass.

## Maintenance observations

The project is not high-churn application software; maintenance is lower-frequency and protocol/infrastructure-focused. The latest inspected 2026 commit fixed invalid `virtioNetHdr` state when removing entries from the TCP GRO table after vectorized Linux I/O work. Earlier inspected commits include careful kernel-version compatibility handling and measured allocation/encoding optimizations.

The relatively sparse commit cadence should therefore not automatically be interpreted as abandonment. It is a mature protocol implementation with concentrated correctness and performance changes.

## Licensing and reuse

The upstream project uses a permissive MIT-style license. Any reused source must preserve the copyright and permission notice.

Cryptographic/networking code should not be copied casually merely because the license permits it. Prefer depending on maintained upstream packages or studying architecture unless there is a concrete, tested reason to extract code.

## Caveats

- Linux users should generally prefer the kernel WireGuard implementation when available, per upstream guidance.
- Catalog inclusion is not a security or cryptographic audit.
- Platform-specific TUN behavior differs across operating systems.
- Downstream forks such as Tailscale's `wireguard-go` can contain meaningful divergence; their code and licensing should be inspected independently before reuse.
- Production VPN deployments require careful routing, DNS, firewall, key-management, privilege, and platform integration beyond the protocol engine itself.

## Related projects / recursive leads

- https://github.com/tailscale/wireguard-go — Tailscale-maintained fork; compare production-specific divergence.
- https://github.com/tailscale/tailscale — userspace overlay stack already in the current queue.
- WireGuard tools and platform clients — configuration and control ecosystem.
- gVisor netstack / Tailscale netstack integration — userspace packet-processing path above the encrypted tunnel.

## Promotion recommendation

**READY — VERIFIED, provisional S / 28.** Promote only through the normal synchronized canonical-catalog path after candidate-queue validation and Catalog Audit.