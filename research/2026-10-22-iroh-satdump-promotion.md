# Iroh and SatDump promotion — 2026-10-22

## Provenance
Both are GitHub-first discoveries with existing dossiers: [Iroh](2026-09-30-iroh-key-addressed-p2p-quic.md) and [SatDump](2026-09-29-satdump-satellite-sdr-processing.md). Existing catalog and master list checked for duplicate names, aliases and repository URLs. Two YouTube playlist IDs searched without usable metadata; no transcript-derived claims.

## Iroh — VERIFIED, S/29
**Upstream:** https://github.com/n0-computer/iroh — MIT OR Apache-2.0. README, workspace directories, both root license files, release notes and recent commits inspected.
**Release:** https://github.com/n0-computer/iroh/releases/tag/v1.4.1 published 2026-10-22. Includes CI timeout changes and rustls-webpki untrusted-SPKI dependency update.
**CI:** https://github.com/n0-computer/iroh/actions/runs/39805786602 — 2026-10-22 main: 28/28 jobs successful; inspected Android, Linux/Windows/macOS, Wasm, FreeBSD cross-build, netsim, docs and lint. Upstream evidence, not our own execution.
**Components:** `iroh/src/endpoint.rs`, `iroh/src/address_lookup/`, `iroh/src/portmapper.rs`, `iroh/src/protocol.rs`, `iroh-relay/`, `iroh-base/`, `iroh-dns-server/`. Rust >=1.91 in CI.
**Scoring:** utility 5, working evidence 5, reusability 5, novelty 5, docs 4, maintenance 5 = 29.
**Limitations:** no independent NAT traversal, relay, crypto or battery testing. Relay metadata exposure and upstream path-selection/high-concurrency reports warrant investigation. Related iroh-blobs, iroh-gossip, iroh-docs, iroh-ffi and noq require separate licensing/verification.

## SatDump — VERIFIED, S/27
**Upstream:** https://github.com/SatDump/SatDump — GPL-3.0. README, source directories, license, releases and commit history inspected.
**Release:** https://github.com/SatDump/SatDump/releases/tag/1.2.2 published 2024-11-29. Active master commit 2026-10-22 fixes IERS crash; numbered stable release is old.
**CI:** https://github.com/SatDump/SatDump/actions/runs/39809901226 — 2026-10-22 Build All: 5 successful (Android, Windows x64/ARM64, Ubuntu 22.04/24.04), 3 failed (ARM64, macOS Intel/Silicon), 1 skipped. Inspected failed job logs: ARM64 cc1plus killed during compile (possible resource exhaustion, not proven); macOS Intel downloaded 146-byte SDRPlay archive rejected by unzip. macOS Silicon also failed in dependency build, but exact cause not separately established.
**Components:** `src-core/dsp/`, `src-core/pipeline/`, `src-core/products/`, `src-core/image/`, `src-core/projection/`, `src-cli/`, `src-ui/`, `plugins/`, `src-testing/`.
**Scoring:** utility 5, working evidence 4 (CI not green), reusability 5, novelty 4, docs 4, maintenance 5 = 27.
**Limitations:** no independent compilation, radio reception, DSP pipeline execution, scientific validation or decoded imagery comparison. SDR drivers and satellite products may have separate licensing. Next: CI dependency reliability, ARM64 resource constraints, recorded-IQ regression fixtures.

## Steward controls
No third-party code, binaries or data copied. All claimed execution evidence is upstream CI. Canonical URLs, headings, score arithmetic and source provenance checked before publication.
