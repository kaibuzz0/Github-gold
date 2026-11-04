# SDRoxide — native and remotely operated Rust SDR workstation

- **Repository:** https://github.com/dividebysandwich/sdroxide
- **Author:** dividebysandwich
- **Category:** software-defined radio / amateur radio / DSP / digital modes / remote station / Rust / WASM
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29/30 — S**
  - Utility: 5
  - Working evidence: 5
  - Reusability: 5
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 4
- **License:** GPL-3.0 (root repository; vendored/submodule components carry their own compatible terms)
- **Discovery:** GitHub-first discovery, inspected 2026-10-07.

## Summary

SDRoxide is a broad Rust SDR transceiver/workstation that can run as a native desktop application, as a server with a WASM browser UI, or as a native remote client. It combines radio backends, DSP, waterfall/spectrum UI, logging, remote operation, accessibility, digital modes and protocol decoders in one workspace.

The repository is unusually component-rich. Upstream documents support for CAT/audio rigs, TCI, OpenHPSDR, SoapySDR, RTL-SDR, RX-888, SDRplay, Icom LAN and several experimental/native backends. Digital and receive modes include FT8/FT4/FT2, JS8, PSK31, RTTY, Olivia, THOR, FSQ, WSPR, SSTV, APRS/AX.25-related components, ADS-B, VDL2, ACARS, HFDL, NAVTEX and others.

## Valuable components

- modular crates workspace separating radio backends, DSP and protocol/mode implementations;
- sdroxide-dsp signal-processing primitives;
- sdroxide-digi digital-mode infrastructure;
- dedicated ADS-B, AIS, APRS, AX.25 and other protocol crates;
- native RTL-SDR and multiple hardware/backend integrations;
- native/server/remote-client architecture with browser WASM UI;
- hardware-free signal-generator and raw-IQ-file sources useful for testing;
- integrated Hamlib rigctld and TCI interoperability;
- local accessibility announcements and screen-reader exposure;
- external T/R relay sequencing and band-decoder control;
- provenance-controlled rtl_433 embedding with an explicit compatibility/update checklist.

## Evidence inspected

GitHub Gold inspected repository metadata, README/user-facing capability documentation, root license, recent commits, releases, workflow inventory, crate layout, and the rtl_433 provenance document.

The repository was created 2026-07-20 and had 237 stars and 39 forks when inspected. The latest default-branch commit observed was 2026-10-03. Stable release v1.6.9 was published 2026-09-28 with automated release artifacts including Linux x86_64/aarch64 packages; repository documentation also describes Windows MSI and macOS DMG distribution.

The release workflow is large and cross-platform. This dossier treats successful release artifacts and the extensive repository structure as strong upstream working evidence, but GitHub Gold did not independently reproduce the builds.

A particularly strong curation signal is crates/sdroxide-ism/PROVENANCE.md. It records the exact rtl_433 upstream commit, explains why that post-release commit is pinned, documents build flags and license interaction, identifies mirrored/fatal-path assumptions that must be rechecked on updates, and points to a weak-signal regression test guarding a load-bearing auto-level setting.

## Caveats

Breadth is not uniform maturity. Upstream explicitly labels several radio backends experimental and some transmit paths unmeasured. Planned transports/features must not be cataloged as implemented merely because related UI or protocol code exists.

Radio transmission is regulated and hardware-dependent. This catalog entry is for legitimate amateur-radio, interoperability, receiving, research and authorized operation; it does not imply permission to transmit on any frequency.

GitHub Gold did not compile SDRoxide, run its tests, install release packages, attach SDR hardware, transmit RF, verify every listed decoder/mode, reproduce performance claims, or audit remote-server authentication/security.

## License and provenance

The repository root is GPL-3.0. No upstream implementation code was copied into GitHub Gold.

Component provenance needs to be preserved if code is ever extracted. For example, the default sdroxide-ism build embeds rtl_433 as a pinned git submodule under GPL-2.0-or-later, while its native clean-room decoders remain separate. The provenance file explains the compatibility implications and update procedure. Other vendored codecs/models/submodules should be checked individually before reuse.

## Follow-up

1. Build the workspace and run tests on Linux without SDR hardware using signal-generator/file inputs.
2. Inventory crates by maturity and test coverage instead of treating the application as one monolith.
3. Compare native RTL-SDR receive behavior against rtl_tcp/Soapy paths using identical IQ captures.
4. Validate remote native/browser operation under loss, jitter and reconnects.
5. Reproduce a small set of protocol decoders against published golden IQ/audio fixtures.
6. Inspect authentication and authorization around remote station control and transmit actions.
7. Audit T/R relay sequencing and TX-range lockout failure behavior with mocked hardware.
8. Trace license/provenance boundaries for RADE, rtl_433, DeepCW and bundled models.
9. Evaluate the modular protocol crates as standalone reusable components for future GitHub Gold entries.
