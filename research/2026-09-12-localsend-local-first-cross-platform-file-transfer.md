# LocalSend — Local-First Cross-Platform File Transfer

- **Repository:** https://github.com/localsend/localsend
- **Author / Org:** LocalSend
- **Category:** local-first software / offline file transfer / cross-platform utility / LAN protocol / Flutter / Rust
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28 / 30 — S tier**
- **Discovery:** GitHub-first breadth rotation into local-first/offline utilities; no YouTube-derived technical claim used.

## Why it matters

LocalSend is a cross-platform file and message transfer application designed to operate directly over a local network without an internet connection or external coordination server. The project supports Windows, macOS, Linux, Android, iOS and Fire OS, with both GUI and headless/CLI-oriented surfaces.

For GitHub Gold, the strongest value is not merely the finished application. LocalSend combines a documented interoperable REST/HTTP(S) protocol, multicast discovery, direct-IP fallback, self-generated TLS certificates, parallel file-transfer endpoints, checksums, a Rust CLI, Flutter clients and reusable Rust packages in one actively maintained codebase. It is a strong reference architecture for user-controlled LAN applications that need to work across mobile and desktop operating systems without cloud dependency.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Practical offline/local-network file and message transfer across major desktop and mobile platforms. |
| Working evidence | 4 | CI performs Flutter analysis/tests plus Rust Clippy/tests/checks and packaging consistency checks; broad released binaries exist, but this run did not independently execute cross-device transfers. |
| Reusability | 5 | Apache-2.0 codebase, separately documented protocol, Rust CLI/core packages and clear REST endpoints. |
| Novelty | 4 | LAN transfer tools are not unique, but the serverless cross-platform protocol, reverse-download mode and clean interoperable architecture are distinctive. |
| Documentation | 5 | README, build instructions, CLI documentation and a separate protocol specification describe discovery and transfer behavior in detail. |
| Maintenance | 5 | Stable v1.18.2 release in August 2026 and active commits through 2026-09-12, including CI/signing and feature work. |

## Repository-native evidence

The README states that LocalSend transfers files and messages between nearby devices over the local network without requiring internet access or third-party servers. It documents Windows, macOS, Linux, Android, iOS and Fire OS distribution channels, portable desktop mode, firewall requirements, CLI usage and source-build instructions.

The current repository has distinct application, CLI and package surfaces. Particularly useful areas include:

- `app/` — Flutter desktop/mobile application;
- `cli/` — Rust command-line client implementing LocalSend Protocol v2 behavior;
- `packages/core/` — reusable Rust-side core functionality referenced by CI;
- `packages/localsend_isolates/` — Flutter/Rust integration package exercised separately in CI;
- `support/` — packaging/build assets and platform-specific release tooling;
- root Cargo workspace — shared Rust packages including the CLI and signaling/server components.

The README's CLI documentation confirms directory-recursive sends, interactive device discovery and direct destination selection by alias or IP address. Direct-IP mode probes HTTPS on the default LocalSend port, which is useful when multicast discovery is unavailable.

## Protocol architecture

The separately maintained `localsend/protocol` repository currently documents **LocalSend Protocol v2.2**. Its design goal is a simple REST protocol with no external server dependency.

Key protocol elements include:

- UDP multicast discovery on default port `53317` / multicast address `224.0.0.167`;
- HTTP/TCP service on default port `53317`;
- HTTPS mode using an on-device certificate, whose SHA-256 hash is used as the device fingerprint;
- HTTP registration fallback when multicast is not usable;
- metadata negotiation via `/prepare-upload`;
- per-file upload tokens and session IDs;
- parallel upload calls to `/upload`;
- optional SHA-256 file verification with a defined `422` checksum-mismatch response;
- explicit session cancellation;
- reverse-download mode in which the sender hosts files for browser-based retrieval;
- PIN-protected prepare operations;
- device-type values supporting mobile, desktop, web, headless and server implementations.

The protocol deliberately provides multiple discovery/transfer paths because multicast or inbound HTTP service may not be available on every network/device.

## Working evidence

The current `ci.yml` performs multiple independent checks on Ubuntu:

- Dart formatting enforcement for application code/tests;
- `flutter analyze`;
- application `flutter test`;
- separate tests for `localsend_isolates`;
- Rust `cargo clippy --features full --all-targets` for the core package;
- Rust `cargo test --features full` for the core package;
- Rust tests for the signaling server;
- `cargo check` for the Flutter Rust plugin crate and `localsend-cli`;
- release/package version consistency checks across Flutter metadata, Windows Inno Setup, the CLI Cargo manifest, MSIX metadata and AppImage recipes;
- copyright/license-year and Rust-toolchain consistency checks.

This provides strong upstream evidence that both Flutter and Rust layers are continuously checked. The inspected CI file is not, by itself, proof that every OS-specific binary or real two-device LAN transfer succeeds on every commit.

## Releases and maintenance

The latest stable GitHub release inspected was **v1.18.2**, published **2026-08-21**. The release exposes architecture/platform-specific artifacts including Android APKs and Linux packages, with GitHub-provided SHA-256 digest metadata on release assets.

Recent repository activity observed through **2026-09-12** included:

- feature work restoring hashtag behavior;
- Windows-on-ARM Flutter CI updates;
- Windows build/packaging CI repairs;
- Ubuntu runner updates;
- code-signing workflow improvements.

The README also states that Windows binaries are signed and links to a repository code-signing policy. LocalSend does not use an automatic in-app updater; upstream recommends app-store or package-manager distribution where possible.

## Useful components to revisit

- **LocalSend Protocol v2.2** — compact REST/UDP interoperability specification suitable for independent clients.
- **Device discovery** — multicast announcement plus HTTP/direct-IP fallback behavior.
- **Transfer session model** — metadata negotiation, session IDs, per-file tokens, parallel transfer and cancellation.
- **Checksum verification** — optional SHA-256 metadata plus receiver-side verification semantics.
- **Rust CLI** — headless terminal client for local transfer automation.
- **Rust core packages** — reusable networking/protocol/application primitives beneath the GUI integration.
- **Reverse-download API** — sender-hosted browser retrieval for environments where the receiver cannot run LocalSend.
- **Portable desktop mode** — settings-local execution pattern useful for removable/portable deployments.
- **Cross-platform packaging/signing** — release engineering across Windows, Linux, macOS, Android and iOS ecosystems.

## Platforms / requirements

Upstream documents these minimums or environments:

- Android 5.0+;
- iOS 12.0+;
- macOS 11 Big Sur+;
- Windows 10+ for current releases;
- Linux with desktop-portal dependencies depending on the desktop environment.

Source development currently requires Flutter plus Rust. LocalSend generally requires both peers to be on the same reachable local network. Firewalls, guest-network/AP isolation and VPN LAN-blocking can prevent discovery or direct transfer.

## Licensing

- **Repository root:** Apache License 2.0.
- The root license identifies copyright 2022–2026 Tien Do Nam.
- Apache-2.0 redistribution requirements, notices and modification marking must be preserved when applicable.
- Vendored packages, platform SDKs, app-store packaging assets and third-party dependencies may carry their own licenses and must be checked independently before extraction/reuse.

No upstream source code, binaries, certificates, package artifacts or third-party assets were copied into GitHub Gold during this run.

## Verification performed

GitHub Gold inspected:

- current upstream README;
- root Apache-2.0 license;
- current primary CI workflow;
- repository top-level structure;
- separate LocalSend Protocol v2.2 documentation;
- latest stable GitHub release metadata;
- recent commit history through 2026-09-12;
- existing GitHub Gold catalog/research search for duplicate LocalSend entries.

**Not performed:** GitHub Gold did not compile or execute LocalSend, run Flutter/Rust tests, transfer files between devices, inspect packet captures, validate multicast behavior, test every supported OS, validate reverse-download behavior in a browser, audit TLS/certificate handling, independently verify release artifacts, or perform a security review.

Repository evidence is therefore recorded as **upstream working evidence**, not independent local execution.

## Caveats / risks

- Same-LAN reachability is a core assumption; AP isolation, firewall rules, VPN policy and segmented networks can break discovery or transfer.
- The project's generated-certificate/fingerprint model is not the same trust model as publicly trusted PKI; a dedicated security review is required before making stronger authentication guarantees.
- The protocol permits HTTP when encryption is disabled and reverse browser downloads intentionally use unencrypted HTTP because browsers reject the self-signed certificate workflow.
- The README notes that disabling encryption can improve transfer speed, which is a security/performance tradeoff users must understand.
- Optional SHA-256 file metadata improves corruption/integrity checking only when supplied and verified; it should not be conflated with peer identity/authentication.
- Cross-platform behavior depends heavily on OS networking, sandbox and permission models.
- Flutter and Rust toolchain versions are pinned/managed; source builds may fail when using incompatible system versions.

## Related ecosystem

- `localsend/protocol` — protocol specification and interoperability contract.
- `localsend/web` — browser-oriented ecosystem project.
- package-manager integrations including F-Droid, Homebrew, Flathub, Winget, Scoop, Chocolatey, Nixpkgs, Snap and AUR.
- independent LocalSend-compatible implementations can be evaluated separately for protocol interoperability and license quality.

## Follow-up research

1. Trace certificate generation, fingerprint validation and first-contact trust semantics in the implementation.
2. Inspect Rust core networking boundaries and determine which components can be reused independently of Flutter.
3. Map protocol-v2 error handling, retry semantics, cancellation races and parallel-transfer behavior.
4. Inspect path sanitization, filename handling and directory traversal protections on receive paths.
5. Review checksum computation/verification behavior for large files and interrupted/resumed transfers.
6. Test multicast discovery versus direct-IP fallback across Android, Linux and Windows networks.
7. Inspect reverse-download HTTP server exposure, session controls and browser-facing security boundaries.
8. Evaluate the CLI as an automation primitive for headless Linux/Termux-style workflows.
9. Compare independent LocalSend protocol implementations for interoperability and reusable components.
