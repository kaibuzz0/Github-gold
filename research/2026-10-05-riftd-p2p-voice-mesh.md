# riftd — serverless Rust P2P voice/text mesh and reusable protocol stack

- **Repository:** https://github.com/infinityabundance/riftd
- **Author:** infinityabundance / Riaan de Beer
- **Category:** P2P communications / NAT traversal / voice / Rust / local-first networking
- **Evidence:** VERIFIED
- **Provisional Gold score:** **26/30 — S**
  - Utility: 4
  - Working Evidence: 5
  - Reusability: 5
  - Novelty: 5
  - Documentation: 4
  - Maintenance: 3
- **Primary language:** Rust
- **License:** Apache-2.0 at root; README also advertises MIT/Apache-2.0, so file/component-level licensing should be checked before extraction.
- **Discovery:** GitHub-first discovery, 2026-10-05.

## Executive finding

riftd is a compact serverless P2P voice and text stack intended as a pragmatic alternative to heavyweight WebRTC deployments. The repository combines LAN discovery, invite/DHT discovery, UDP hole punching, STUN/TURN paths, peer relay fallback, pairwise encrypted chat/voice, Opus media, a terminal client, native Qt clients, Android JNI bindings, a reusable protocol crate, a Rust SDK, a browser experiment, and an experimental trackerless torrent rendezvous layer.

Its strongest GitHub Gold value is the decomposition into reusable crates rather than the finished chat application alone.

## High-value components

The workspace separates:

- `rift-core` — common core primitives;
- `rift-discovery` — discovery;
- `rift-mesh` — mesh behavior;
- `rift-media` — media/voice;
- `rift-protocol` — versioned wire protocol;
- `rift-nat` — NAT traversal;
- `rift-rndzv` and `rndzv-sim` — rendezvous logic and simulation;
- `rift-sdk` — reusable SDK/FFI surface;
- `rift-dht` — DHT discovery;
- `rift-metrics` — metrics;
- `rift-e2e` — integration/E2E validation;
- `rift-wasm` and `rift-web-chat` — browser/WASM experiments;
- `rift-torrent` — torrent/rendezvous experiment;
- `rift-ws-relay` — WebSocket relay.

Native client surfaces include a Qt6/QML desktop application and a Kotlin/Jetpack Compose Android application using JNI bindings to the Rust SDK.

## Working evidence inspected

The current CI is substantive rather than badge-only. On pushes and pull requests it:

- runs `cargo fmt --all -- --check`;
- runs Clippy across the workspace with warnings denied;
- runs `cargo test --workspace`;
- runs the `rift-e2e` crate;
- builds the Rust SDK for Android and assembles a debug APK;
- builds the Rust SDK plus Qt client on Windows;
- builds universal x86_64/aarch64 macOS Rust libraries and the Qt client.

The E2E documentation explicitly identifies two tests that are intentionally ignored in normal CI because they require external networking infrastructure:

1. restrictive-NAT TURN fallback, requiring a TURN server plus NAT simulation;
2. public-STUN server-reflexive connectivity.

That distinction is useful evidence hygiene: ordinary CI coverage should not be confused with validation of real restrictive-NAT environments.

The repository contains a versioned wire protocol and reusable SDK rather than only application UI code.

## Maintenance assessment

The repository was created in February 2026. The latest default-branch commit observed in this pass is dated **2026-05-25**. That is materially older than the current 2026-10-05 inspection date, so Maintenance is scored 3/5 rather than treating repository breadth as current activity.

The project remains technically valuable, but a future pass should determine whether development moved elsewhere, paused, or is expected to resume.

## Novelty / research value

Upstream documents a “Predictive Rendezvous” design intended to derive deterministic peer-coordination schedules without conventional infrastructure. The repository also applies this concept experimentally to torrent peer discovery via `rift-torrent`.

These are interesting research directions, but GitHub Gold did not independently validate the associated paper, prove rendezvous success under realistic clock/NAT conditions, or establish superiority to DHT/tracker/STUN approaches.

## License

The inspected root `LICENSE` is Apache-2.0. The README badge describes the project as MIT/Apache-2.0 and links an MIT license path, but the exact dual-license file/component state should be resolved before copying source.

No upstream source was copied into Github-gold.

## Evidence boundary

GitHub Gold did **not**:

- compile riftd;
- execute unit or E2E tests;
- establish a LAN or WAN mesh;
- reproduce UDP hole punching;
- operate STUN or TURN infrastructure;
- inspect packet captures;
- test relay-to-direct upgrades;
- validate encryption or key handling;
- make a voice call or measure Opus quality;
- build the Qt or Android clients;
- reproduce Predictive Rendezvous results;
- validate trackerless torrent discovery;
- perform a security audit.

VERIFIED here means concrete repository-native implementation, CI, test, client, and protocol evidence was inspected. It is not independent operational or security certification.

## Caveats

- The strongest real-network NAT/STUN E2E tests are explicitly excluded from ordinary CI because they need external infrastructure.
- Repository activity appears paused or reduced after May 2026.
- Full-mesh topology has scaling limits as peer count rises.
- NAT traversal reliability varies substantially across carrier-grade NAT, symmetric NAT, firewalls, and UDP-restricted networks.
- Browser support is described as an early text-only WebSocket-relay prototype rather than parity with native clients.
- Security-sensitive claims require independent protocol and implementation review.
- The root-license/README dual-license presentation should be reconciled before component extraction.

## Gold rationale

**Utility — 4/5:** useful communications stack and SDK, though not yet established as a mature production communications platform.

**Working Evidence — 5/5:** workspace tests, dedicated E2E crate, Android build, and native Qt builds are wired into CI, with external-infrastructure test boundaries documented.

**Reusability — 5/5:** unusually modular crates for protocol, NAT, discovery, mesh, media, SDK, DHT and rendezvous.

**Novelty — 5/5:** Predictive Rendezvous plus its application to infrastructure-minimized peer/torrent discovery is technically distinctive.

**Documentation — 4/5:** good README/build/E2E documentation, but production/security/operational evidence remains incomplete.

**Maintenance — 3/5:** latest observed default-branch activity is 2026-05-25.

**Provisional total: 26/30 — S tier.**

## Follow-up queue

1. Run `cargo test --workspace` and `cargo test -p rift-e2e` independently.
2. Execute STUN and TURN ignored tests in controlled network namespaces.
3. Trace identity establishment, key exchange, replay protection and pairwise encryption.
4. Test relay fallback followed by automatic direct-path upgrade.
5. Benchmark mesh behavior at 2, 5, 10 and 25 peers.
6. Reproduce voice jitter/loss/QoS behavior under netem impairment.
7. Inspect the versioned protocol for compatibility and malformed-packet handling.
8. Validate Predictive Rendezvous under clock skew, packet loss and NAT diversity.
9. Compare the NAT/media stack with libp2p, WebRTC and Iroh/noq approaches.
10. Resolve the apparent maintenance pause and exact dual-license boundary before promotion.
