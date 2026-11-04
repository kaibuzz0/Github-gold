# Crisis Connect — offline-first disaster communication mesh

- **Repository:** https://github.com/emirhan-duman/Crisis-Connect
- **Author:** emirhan-duman
- **Category:** emergency communications / offline-first / BLE mesh / Android / iOS / privacy
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **Discovery:** GitHub-first category rotation after Dora record/replay research. YouTube seed playlists were not used as technical evidence for this dossier.

## Why it is Gold

Crisis Connect is a substantial cross-platform disaster-communications system rather than a mesh-network mock-up. The repository documents and implements an offline-first Bluetooth path for Android and iOS, with local identities, direct and relayed communication, store-and-forward behavior, QR/SPAKE2 pairing, media transfer, SOS signaling, offline maps and emergency tooling. When connectivity returns, an independent internet transport extends the same conversation model with Signal Protocol messaging and WebRTC calling.

The particularly reusable idea is the **transport-independent conversation boundary**: local BLE and internet paths can carry the same contacts/conversations while queued messages drain over whichever transport becomes available. That architecture is relevant to resilient field software well beyond this application.

## Evidence inspected

### Repository / product evidence

The upstream README describes:

- Android and iOS clients;
- BLE advertising/scanning discovery;
- encrypted direct communication and GATT mesh relay;
- QR ECDH and SPAKE2 short-code pairing;
- chunked voice-message, image and file transfer;
- SOS broadcasts;
- store-and-forward queues;
- offline MapLibre maps;
- an optional online Signal Protocol transport;
- WebRTC calls when internet connectivity exists;
- offline rescue-role certificates and field-team workflows;
- an on-device emergency assistant/knowledge path.

The README is unusually explicit about security boundaries rather than calling every path E2E encrypted. The v1.1.9 release notes state that 1:1 internet calls use DTLS-SRTP without an additional application E2EE layer and that SOS reports delivered to an agency dashboard are transport-encrypted rather than end-to-end encrypted.

### Release evidence

Stable **v1.1.9** was published 2026-08-13. GitHub exposes a universal Android APK (~189 MB) with SHA-256 digest `f690576ab7a1dd5d6266247a469bd5893bfbd082307d994982d918d69c3124e8`; a Sigstore JSON bundle was added on 2026-09-11. Upstream release validation states Android debug builds and app/rescue unit tests passed locally and in GitHub Actions, an iOS generic Simulator Debug build passed, and APK signing/source-stamp checks were performed.

This is upstream evidence; GitHub Gold did not independently reproduce those validation steps.

### CI / supply-chain evidence

The repository contains dedicated workflows for Android CI, iOS CI, Firebase Functions CI, CodeQL, ClusterFuzzLite, OpenSSF Scorecard analysis and release-asset signing. Recent maintenance also added signed SBOM attestations.

Recent commits inspected through 2026-09-19 include explicit telemetry-consent enforcement, a data-retention standard, incident-response documentation, fail-closed attestation handling, Firestore authorization-boundary tests, iOS validation and Android PendingIntent hardening. These are stronger maintenance signals than cosmetic churn.

## Reusable components / patterns worth deeper study

1. **Dual-transport queue and conversation abstraction** — offline BLE and online delivery without forcing the UI/domain model to split into separate messengers.
2. **BLE GATT mesh relay** — hop-forwarding of encrypted application payloads across nearby phones.
3. **SPAKE2 nearby pairing** — short-code pairing without exposing a stable harvestable identifier.
4. **Chunked BLE transfer** — media/file delivery, progress tracking and receipts over a constrained transport.
5. **Offline role certificates** — short-lived ECDSA-signed responder credentials that can be verified without contacting the issuing service.
6. **SOS advertising path** — emergency signaling designed to survive ordinary connectivity loss.
7. **Cross-platform voice path** — Opus-oriented offline voice communication over local Bluetooth transports.
8. **Offline map-region management** and local emergency tooling.
9. **Supply-chain controls** — signed release assets/SBOM work, CodeQL, fuzzing and Scorecard workflows in a mobile emergency application.

## Platforms / requirements

- Android: upstream currently documents Android Studio Ladybug+, JDK 21 and Android SDK 36; release APK targets Android 7.0+ (`minSdk 24`).
- iOS: upstream documents Xcode 16+, iOS 17+ deployment target, macOS Sequoia+ and Rust tooling for vendored native libraries.
- BLE features require physical devices; simulators/emulators are not a substitute for radio validation.
- Online backend features use Firebase services; the offline Bluetooth layer is documented as independent of that backend.

## License

Repository root: **GNU AGPL-3.0**.

The project also consumes/vendors third-party components with their own obligations, including libsignal. Do not assume every dependency, model, map asset or bundled dataset is licensed under the repository root license. No Crisis Connect implementation source was copied into GitHub Gold.

## Caveats / limitations

- Emergency software deserves a higher validation bar than normal consumer software. Repository evidence is strong, but this dossier is not a field-safety certification.
- GitHub Gold did not independently validate radio range, multi-hop behavior, background execution reliability, cryptographic protocol composition, battery cost, congestion behavior or cross-platform BLE interoperability.
- Upstream explicitly documents weaker confidentiality boundaries for some online calling and agency-dashboard paths.
- The APK is large (~189 MB), which matters for constrained/off-grid distribution.
- Some features depend on online services even though the core BLE path does not.
- An on-device AI emergency assistant should be treated as advisory software, not authoritative medical/rescue instruction, without separate evaluation.

## Verification performed by GitHub Gold

Inspected repository metadata, README architecture/security claims, root AGPL-3.0 license, stable v1.1.9 release metadata/assets, CI workflow inventory and recent commit history. Checked the existing GitHub Gold branch for a duplicate Crisis Connect entry before adding this dossier.

**Not performed:** source build; APK installation; iOS build; test execution; BLE packet capture; cryptographic audit; fuzzing; multi-device mesh test; offline map test; Signal/WebRTC test; responder-role certificate verification; battery/range benchmark; disaster field trial.

## Follow-up research

Highest-value next component pass: trace the **BLE GATT mesh relay + transport-independent queue** from source to tests on both Android and iOS. Determine how message IDs, deduplication, TTL/hop limits, retry/backpressure, receipts, peer disappearance and reappearance are represented, and whether the two clients have protocol-level interoperability tests or golden vectors.

Secondary lead: inspect the SPAKE2 implementation and offline role-certificate verification boundary, focusing on replay resistance, identity binding, expiration/revocation semantics and test coverage.
