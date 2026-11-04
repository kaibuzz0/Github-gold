# Mesh-Talk — serverless encrypted LAN messenger

- **Repository:** https://github.com/OctopusGarage/mesh-talk
- **Author / Org:** OctopusGarage
- **Category:** local-first communications / LAN P2P / privacy / Rust / Tauri
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29/30 — S
  - Utility 5
  - Working Evidence 5
  - Reusability 5
  - Novelty 4
  - Documentation 5
  - Maintenance 5
- **Discovery:** GitHub-first discovery, 2026-10-04.

## Why it matters

Mesh-Talk is a serverless desktop messenger for macOS, Windows, and Linux. It separates a UI-free Rust protocol core (`mesh-talk-core`) from the Tauri/React shell and exposes the same core through a headless `mesh-talk-node` CLI. Peers discover one another on a LAN, establish authenticated encrypted channels, replicate append-only conversation event logs, and can use an optional encrypted store-and-forward “post office” for temporarily offline peers.

This is unusually useful as both a complete application and a source of reusable design patterns for local-first communications.

## High-value components

- signed UDP multicast discovery plus announce/response and subnet-scan fallback
- Noise-encrypted direct TCP transport
- Ed25519 device identities and X25519 agreement
- Double Ratchet DMs and sender-key channel ratchets
- safety-number verification, TOFU and key-change warnings
- append-only replicated event logs with bounded synchronization rounds
- encrypted-at-rest keystores/message logs
- resumable, per-chunk encrypted large-file transfer
- multi-device identity/account linking
- optional store-and-forward encrypted relay
- headless node/relay CLI independent of Tauri
- diagnostics and cross-platform native desktop integration
- fuzzing, mutation testing, integration/E2E testing, supply-chain and release-validation machinery

## Platforms / requirements

Desktop targets documented upstream: Linux, macOS, Windows. Source builds require stable Rust/Cargo, Node.js 20+, Tauri CLI, and platform desktop dependencies. The protocol core itself is Rust and UI-independent.

## Evidence inspected

Repository-native evidence inspected on 2026-10-04 includes the current README/repository structure, license, recent commit history, and upstream-described CI/release gates.

The repository exposes dedicated core tests including multi-process integration tests using real UDP/TCP nodes. Upstream documents CI across Linux/macOS/Windows with formatting, Clippy with warnings denied, tests/coverage, frontend build/lint, cargo-deny, fuzzing, mutation testing, secret scanning, and OpenSSF Scorecard.

Recent commits on 2026-10-04 provide unusually strong maintenance evidence:
- `220c7bc...` strengthened evidence-based native health and release gates.
- `128a3d0...` added portable installer checksum validation and self-verification before signing.
- `5fc86a0...` shipped v0.1.5 privacy/desktop work with extensive native and protocol regression evidence, including disclosure gates, Noise admission, session revocation, restart persistence, and cross-platform diagnostics.

Upstream release documentation says release bundles include SHA-256 manifests, Sigstore/cosign signatures, and SLSA provenance attestations.

## Evidence boundary

GitHub Gold did **not** compile Mesh-Talk, run its tests/E2E suite, establish a two-peer LAN conversation, inspect packets, reproduce forward-secrecy behavior, verify release signatures/attestations, test relay recovery, test file-transfer resume, or independently audit its cryptographic protocol.

Accordingly, VERIFIED means concrete repository-native evidence exists for the relevant functionality; it is not an independent cryptographic/security certification.

The project is young and currently low-adoption by star/fork count. That is not treated as a quality proxy, but independent deployments and external security review would materially strengthen confidence.

## License

Root license: **MIT**. No upstream source was copied into GitHub Gold. Dependencies and bundled assets retain their own licenses and should be checked before component extraction.

## Caveats / risks

- LAN discovery depends on multicast or fallback probing and can be constrained by network/firewall policy.
- Desktop release artifacts are documented as unsigned at the OS code-signing layer, so Windows/macOS may display first-run warnings even though upstream also supplies checksum/signature/provenance material.
- Security-sensitive claims are supported here by upstream implementation/test evidence, not an independent audit.
- Store-and-forward, multi-device identity, ratchets, revocation, persistence and synchronization deserve adversarial testing before critical use.

## Follow-up queue

1. Run core unit and multi-process E2E suites independently.
2. Inspect the Noise handshake, identity pinning, ratchet state persistence and key-change handling.
3. Test two/three-node divergence → reconnect → event-log convergence.
4. Exercise post-office relay with offline recipients, duplicate delivery and restart/crash cases.
5. Test file-transfer interruption/resume and integrity failures.
6. Verify a published SHA256SUMS/cosign/SLSA release chain independently.
7. Inspect fuzz targets and mutation-test survivors.
8. Test discovery across multicast-disabled, multi-NIC, IPv4/IPv6 and restrictive-firewall environments.
9. Compare protocol/design tradeoffs with Briar, Jami, SimpleX/local relays and other LAN-first messengers.
10. Reassess score after external audit/adoption evidence emerges.
