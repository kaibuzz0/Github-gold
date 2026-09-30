# Iroh — key-addressed P2P QUIC and NAT-traversal substrate

- **Repository:** https://github.com/n0-computer/iroh
- **Organization:** n0-computer
- **Category:** P2P networking / QUIC / NAT traversal / edge and local-first infrastructure
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Primary language:** Rust
- **License:** MIT OR Apache-2.0
- **Discovery source:** Recursive research from GuardianDB's Iroh-backed synchronization layer; GitHub-first verification
- **Inspection date:** 2026-09-30

## Executive finding

Iroh is a reusable peer-to-peer networking substrate that lets applications address peers by public-key identity rather than depending on stable IP addresses. It combines QUIC transport, NAT traversal/hole punching, direct-path selection, and relay fallback behind an application-facing endpoint abstraction.

The current upstream README explicitly describes the model as dialing by public key, attempting direct hole-punched connectivity first, and falling back to public relay infrastructure when necessary. It also identifies `noq` as the QUIC implementation used by Iroh.

For GitHub Gold this is unusually valuable because it is not merely a complete application: it is infrastructure that can be embedded into local-first databases, synchronization systems, messaging, file transfer, edge systems, and other peer-to-peer software.

## High-value reusable surfaces

### Key-addressed endpoints

The core API exposes endpoints identified by cryptographic identity rather than requiring an application to treat an IP address as the durable identity of a peer. This is a strong building block for intermittently connected and mobile systems where addresses change frequently.

### NAT traversal and relay fallback

Upstream documents a direct-first model: Iroh attempts hole punching and can fall back to relay servers if a direct path cannot be established. The repository contains both relay client and relay server implementation (`iroh-relay`), and upstream states that the public relay service uses this code and that users can run it themselves.

### QUIC transport

Iroh uses `noq` to establish QUIC connections. Upstream highlights authenticated encryption, concurrent streams, stream priorities, datagrams, and avoidance of transport-level head-of-line blocking as inherited QUIC capabilities.

### Protocol composition

The README points to a wider protocol ecosystem built on Iroh:

- `iroh-blobs` — BLAKE3-addressed blob transfer;
- `iroh-gossip` — publish/subscribe overlay networking intended to operate within phone-class resource constraints;
- `iroh-docs` — eventually consistent key/value data built around Iroh blobs;
- `iroh-ffi` — bindings for non-Rust consumers;
- Iroh examples and experiments repositories.

These are recursive research targets rather than capabilities attributed to the core crate itself.

### Router / ALPN application composition

The documented Rust example exposes a small endpoint + router model where an application binds an endpoint, connects using an application protocol identifier, opens QUIC streams, and registers a protocol handler with the router. This is a useful composition pattern for applications that need multiple custom protocols over one P2P transport substrate.

## Repository architecture observed

The upstream README identifies the workspace components:

- `iroh` — core hole-punching and relay communication library;
- `iroh-relay` — relay client/server;
- `iroh-base` — common types including endpoint identity and relay URLs;
- `iroh-dns-server` — DNS/Pkarr address lookup infrastructure used for EndpointIds.

This decomposition makes Iroh valuable both as a complete dependency and as a systems reference for identity-addressed networking, relay architecture, path selection, DNS/Pkarr discovery, and QUIC integration.

## Working evidence

### Current release

GitHub release metadata inspected on 2026-09-30 shows stable **v1.3.0**, published **2026-09-28**.

The release contains multi-platform `iroh-dns-server` artifacts for targets including Apple Darwin, Linux GNU, Linux musl, Windows, x86-64 and AArch64. GitHub exposes SHA-256 digests for the inspected assets.

GitHub Gold did not download or independently hash these artifacts.

### Active maintenance

The repository remained active immediately after the v1.3.0 release. Recent commits inspected include:

- a 2026-09-28 documentation/deprecation-warning correction;
- the v1.3.0 release commit;
- lookup/resolver success-rate metrics work;
- a 2026-09-25 release-CI change moving release builds to ephemeral runners to reduce cross-instance contamination.

This is direct evidence of active product, observability, API and release-engineering work.

### CI depth

The current `ci.yml` is substantial rather than a badge-only workflow. Observed surfaces include:

- reusable main test suite;
- minimum-crate/version checks;
- FreeBSD cross-build;
- i686 Linux cross-test;
- Android builds for AArch64 and ARMv7;
- Android x86-64 emulator execution of workspace tests;
- browser/Wasm build-and-test path;
- warnings promoted to errors;
- pinned GitHub Action revisions;
- explicit Android NDK/toolchain handling;
- environment and networking setup for emulator integration tests.

The Android emulator path builds and runs tests for `iroh-base`, `iroh-dns`, `iroh-relay`, and `iroh` itself. This materially raises confidence beyond merely compiling an Android target.

GitHub Gold did not execute this CI locally.

## Evidence boundaries and known caveats

Strong evidence does not imply flawless networking behavior. Current upstream issue traffic is useful evidence of real-world edge cases and remaining engineering work.

Examples surfaced during research include:

- an open 2026 issue describing QUIC DATAGRAM burst behavior above roughly 30 realtime connections on one endpoint;
- an open report of suboptimal relay-versus-direct path selection on a local network;
- a previously fixed path-closure coordination issue related to multipath QUIC;
- a fixed panic involving a custom transport and zero-length packets.

These issue reports are not independently reproduced by GitHub Gold, and issue reports themselves are not proof that every reported diagnosis is correct. They are recorded because high-value networking infrastructure should retain known operational caveats rather than being scored only from README claims.

The wider ecosystem also needs separate evaluation. For example, an open 2026 `iroh-gossip` issue reports unreaped connection/state under sustained peer churn. That is a separate repository and should not be silently generalized to core Iroh, but it is relevant to future ecosystem testing.

## License

The root project is dual licensed at the user's option under **MIT OR Apache-2.0**.

No Iroh source code or release artifacts were copied into GitHub Gold during this run. Individual ecosystem repositories, dependencies, generated artifacts, and third-party components require their own license review before source extraction or redistribution.

## Verification performed by GitHub Gold

This run inspected:

- current repository metadata and default branch;
- current upstream README and architecture description;
- root licensing statement;
- current `ci.yml` and its Android/cross/Wasm test surfaces;
- current GitHub release metadata for v1.3.0 and representative SHA-256 asset digests;
- recent default-branch commit activity;
- current upstream issue evidence for operational caveats;
- the existing GitHub Gold branch/catalog search to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- compile Iroh;
- run its test suite;
- run the Android emulator suite;
- establish a direct Iroh connection;
- reproduce NAT traversal or hole punching;
- operate a relay or DNS/Pkarr server;
- packet-capture or cryptographically audit QUIC traffic;
- reproduce path migration or multipath behavior;
- benchmark latency, throughput, memory or battery use;
- reproduce the reported DATAGRAM/path-selection issues;
- independently verify release artifact hashes.

`VERIFIED` therefore means strong repository-native implementation, CI, release and maintenance evidence, not an independent networking or cryptographic certification.

## Why it matters for GitHub Gold

Iroh fits several catalog priorities simultaneously:

- local-first/offline-tolerant systems;
- mobile and edge networking;
- resilient peer-to-peer communications;
- reusable networking infrastructure;
- self-hostable relay components;
- Android/mobile support;
- composable Rust libraries;
- protocol experimentation;
- infrastructure useful to databases such as GuardianDB and future synchronization projects.

It is particularly strong as a reusable substrate: applications can build their own authenticated protocol over its endpoint/router model instead of reimplementing NAT traversal, relay fallback and QUIC path management.

## Gold rationale

**Utility — 5/5:** directly useful P2P connectivity layer for mobile, edge, sync, messaging and local-first applications.

**Working Evidence — 5/5:** current stable release, active development, substantial multi-platform CI and actual Android emulator test execution upstream.

**Reusability — 5/5:** library-first architecture, protocol router, relay server, ecosystem protocols and permissive dual license.

**Novelty — 5/5:** the combination of public-key dialing, NAT traversal, relay fallback and composable QUIC protocols is technically distinctive and broadly reusable.

**Documentation — 4/5:** strong README/docs/examples and clear architectural entry points; deep operational behavior still requires following multiple repositories and docs surfaces.

**Maintenance — 5/5:** v1.3.0 was released two days before inspection and default-branch activity continued immediately afterward.

**Provisional total: 29/30 — S tier.**

## Next research queue

1. Inspect `noq` as the underlying QUIC implementation, especially multipath and NAT-traversal design.
2. Deep-inspect `iroh-blobs` transfer verification, partial transfer/resume and BLAKE3/Bao architecture.
3. Inspect `iroh-gossip` topology, peer-churn behavior and resource ceilings.
4. Inspect `iroh-docs` / Willow convergence and live-index semantics, especially where GuardianDB depends on them.
5. Inspect `iroh-relay` trust boundaries, deployment model and metadata exposure.
6. Inspect DNS/Pkarr endpoint discovery and key lifecycle.
7. Inspect `iroh-ffi` for Android/iOS/non-Rust embedding surfaces.
8. Revisit open path-selection and high-concurrency DATAGRAM issues as upstream changes land.
