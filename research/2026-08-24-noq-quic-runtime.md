# Research dossier — n0-computer/noq

**Repository:** https://github.com/n0-computer/noq  
**Category:** networking / QUIC / transport runtime  
**Evidence:** VERIFIED  
**Provisional Gold score:** 28 / 30  
**Provisional tier:** S  
**License:** MIT OR Apache-2.0

## Executive finding

`noq` is a general-purpose QUIC implementation in pure Rust. Its architecture is especially useful for GitHub Gold because the project separates a futures-friendly async transport API (`noq`) from a sans-I/O protocol implementation (`noq-proto`) and a lower-level UDP layer (`noq-udp`). This makes it relevant both as a complete QUIC stack and as reusable protocol/runtime architecture.

The project originated as a fork of Quinn, but current development explicitly targets additional QUIC work including multipath, QUIC Address Discovery, and QUIC NAT Traversal. It is also the QUIC foundation now used by the Iroh networking ecosystem, making it a meaningful recursive discovery rather than a duplicate entry.

## Upstream-documented capabilities

The upstream README documents:

- futures-based asynchronous client/server API;
- 0-RTT and 0.5-RTT data;
- ordered and unordered stream reads;
- custom and zero-length connection IDs;
- pluggable cryptography with Rustls integrations using ring or aws-lc-rs;
- Linux, Windows, macOS, Android, iOS, and WebAssembly support;
- core QUIC RFC 8999/9000/9001/9002 support;
- QUIC datagrams, compatible version negotiation, and QUIC-bit greasing;
- qlog support;
- experimental/draft multipath, address-discovery, and NAT-traversal extensions.

## Architecture and reusable components

### `noq`

High-level async QUIC API. Useful study areas include connection lifecycle, streams/datagrams, endpoint configuration, crypto-provider integration, async runtime boundaries, and client/server composition.

### `noq-proto`

Sans-I/O protocol core. This is the most reusable architectural layer because protocol state transitions are separated from actual socket I/O. Study targets include:

- QUIC packet and connection state machines;
- handshake and crypto integration boundaries;
- connection IDs and path state;
- loss detection and congestion control;
- multipath state and per-path timers;
- migration/path validation;
- NAT-traversal and address-discovery extensions;
- datagram processing and coalesced-packet handling;
- qlog/protocol observability.

### `noq-udp`

Platform UDP abstraction. Recent work shows support for Linux/Unix-family platforms, Windows, embedded targets, and `wasm32-wasip2`. This is relevant for portable transport implementations and for understanding UDP offload/timestamp/socket behavior across targets.

### Testing, fuzzing, benchmarks, and perf tools

The workspace includes `bench`, `perf`, and `fuzz` members in addition to the three runtime crates. Property-testing and fuzz-related dependencies are present in the workspace. These are useful references for transport-protocol correctness work.

## Maintenance evidence

Repository metadata inspected on August 24, 2026 shows the project was pushed the same day. The workspace reports version `1.2.0`, Rust edition 2024, and Rust 1.88.

Recent upstream commits include:

- **August 24, 2026:** release activity and removal of an explicitly unmaintained book rather than leaving stale documentation in place;
- **August 20, 2026:** CI/supply-chain hardening using locked Cargo dependencies, pinned Actions, Dependabot cooldown, zizmor, and pinact;
- **August 12, 2026:** synchronization of BBRv3 congestion-control work from Quinn;
- **August 10, 2026:** regression-tested fix preventing a panic when a coalesced datagram tail referenced a never-opened path;
- **July 29, 2026:** fixes to multipath per-path idle-timer semantics and a musl-related UDP timestamp issue;
- **July 27, 2026:** `wasm32-wasip2` UDP backend support, with the commit documenting passing WASI integration cases under Wasmtime.

This is substantive protocol-correctness, portability, congestion-control, and supply-chain maintenance rather than documentation-only activity.

## Licensing

The root README and workspace manifest both declare `MIT OR Apache-2.0`. Upstream provides both license paths. Reuse should preserve the selected license's notices and attribution requirements. No source code from `noq` was copied into GitHub Gold in this research pass.

## Verification performed by GitHub Gold

Inspected:

- repository metadata and current activity;
- upstream README;
- root workspace manifest;
- recent commit history and regression-test descriptions;
- workspace crate/component structure;
- declared license expression.

GitHub Gold did **not** independently build, fuzz, benchmark, interoperate-test, deploy, or cryptographically audit `noq`. Standards-compliance and performance claims remain upstream evidence unless separately tested later.

## Caveats and risks

- Several differentiating features are based on evolving QUIC drafts, especially multipath, address discovery, and NAT traversal. APIs and wire behavior may change as drafts evolve.
- The project originated from Quinn and continues to sync selected upstream work, so future audits should distinguish inherited Quinn behavior from N0-specific extensions.
- QUIC/TLS stacks are security-sensitive infrastructure. Catalog inclusion does not constitute an independent security review.
- A recently removed unmaintained documentation book is a positive hygiene signal, but it also means users should rely on current API docs/examples rather than old prose documentation.

## Why it is Gold

`noq` combines a modern QUIC implementation, clean sans-I/O protocol separation, portable UDP abstraction, active protocol-extension work, current regression testing, and permissive licensing. Its strongest reusable lesson is not simply "another QUIC library"; it is the separation between transport state machines and actual I/O, which is valuable for embedding, testing, simulation, alternate runtimes, and nonstandard network paths.

## Relationship to existing candidates

- **Iroh:** uses QUIC as an application-embedded P2P substrate and adds identity, NAT traversal coordination, relay fallback, and higher-level protocols.
- **noq:** lower-level QUIC transport/protocol implementation and extension laboratory.
- **go-libp2p:** broader modular P2P protocol stack with multiple transports and negotiation layers.
- **Tailscale / WireGuard / Nebula:** overlay/VPN-style networking rather than an application-level QUIC transport library.

## Strong recursive leads

1. Compare `noq-proto` sans-I/O architecture directly with Quinn's protocol core to isolate N0-specific multipath/NAT-traversal changes.
2. Inspect the QNT and QAD implementations used by Iroh's path-discovery and direct-connect logic.
3. Inspect congestion-control implementations, especially BBRv3 synchronization and per-path behavior under multipath.
4. Inspect `noq-udp` portability and offload code, especially WASIp2 and embedded backends.
5. Map `noq` integration points inside `n0-computer/iroh` to understand how low-level QUIC path capabilities are surfaced to application-level peer dialing.

## Promotion status

**Promotion-ready dossier.** Keep separate from Iroh because it represents a distinct reusable transport/protocol layer.