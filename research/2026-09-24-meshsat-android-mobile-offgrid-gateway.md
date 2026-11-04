# MeshSat Android — mobile off-grid multi-bearer gateway

- Repository: https://github.com/meshsat/meshsat-android
- Author/organization: MeshSat
- Category: Android / off-grid communications / mesh / satellite / emergency communications
- Evidence: VERIFIED (repository/upstream evidence; not independently field-tested by GitHub Gold)
- Provisional Gold score: 28/30 — S tier
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 4/5
- License: GPL-3.0; upstream says this choice is required in part because Meshtastic protobuf definitions included by the app are GPL-3.0. Third-party notices remain separately applicable.
- Primary language/runtime: Kotlin 2.1, Jetpack Compose; Android 8.0+; JDK 17 + Android SDK (compile SDK 35) for source builds.
- Discovery: recursive lead from the MeshSat and MeshSat Field Kit dossiers.

## Why it matters

MeshSat Android turns an Android handset into a field gateway rather than merely a companion UI. Upstream documents direct bridging among Meshtastic over BLE, Iridium SBD through a MeshSat node, phone-SIM SMS, APRS, MQTT/Hub connectivity, TCP peers, and a Reticulum transport-node role. It also exposes a loopback API for automation, runs its gateway as an Android foreground service, and includes an offline country-level map plus local satellite-pass prediction.

This is useful because a commodity phone supplies battery, display, GPS, BLE, cellular/SMS and a mature application runtime while external radios/modems provide paths that survive normal IP-network loss.

## Useful components and architecture

- Meshtastic BLE integration using official protobufs: text, position, telemetry, waypoints, node information, traceroute and radio configuration.
- Iridium 9603 SBD path with queued/retried delivery and inbound-message handling during a session.
- RockBLOCK 9704 IMT path over Bluetooth serial exists in code, but upstream explicitly marks hardware validation incomplete.
- SMS through the handset SIM, with optional per-conversation AES-256-GCM according to upstream documentation.
- APRS via KISS-over-TCP or APRS-IS.
- Reticulum transport-node functionality relaying among mesh, Iridium, MQTT and TCP peers.
- MQTT client-certificate connection to the optional MeshSat Hub; the Hub is not required for basic off-grid operation.
- Local API on 127.0.0.1:6051 for testing/automation.
- Message queue, routing rules, config import/export, offline satellite-pass prediction, foreground-service operation and optional boot restart.
- Safety workflows: multi-route SOS, cancellation, check-in timer and geofenced zones. These are technically interesting but must not be represented as emergency-certified functionality.

## Upstream working evidence inspected

The README maintains an unusually explicit verification matrix rather than treating implemented code as field-proven behavior. As of the inspected September 2026 state, upstream reports:

- Mesh through a MeshSat node over Bluetooth verified on a Pixel 9a on 2026-09-19.
- Three satellite messages transmitted through the node and received at the Hub on 2026-09-19.
- Satellite receive verified on 2026-09-19.
- Offline pass prediction verified on 2026-09-19.
- Hub bridge connection verified on 2026-09-19.
- Recovery after restarting the node mid-session verified on 2026-09-20, with the app reporting the link down and reacquiring the modem.
- Delivery receipts from the Hub verified on four messages on 2026-09-20.
- SMS and boot-start fixes verified in an Android 11 emulator.
- SOS-to-SMS/cancel flow verified in an emulator, while other SOS paths remain explicitly unexercised.

The repository publishes signed APK releases for multiple ABIs plus a universal APK. Release v2.19.1 was published on 2026-09-25 with SHA-256 digests in GitHub release metadata. Recent commits also address reproducible-build details for F-Droid and CI-test behavior, providing a strong current-maintenance signal.

## Maturity boundaries and caveats

Upstream calls the application **pre-release** and states that it has never been deployed to a real end user or used in an actual emergency. Preserve that distinction.

Known upstream boundaries include:

- RockBLOCK 9704 IMT code exists but has not been tested on hardware.
- Satellite SOS framing matches the Bridge in tests but had not been sent through the Hub because doing so would trigger the on-call chain.
- Mesh/online-Hub SOS and the phone Test Alarm path were not yet exercised in the inspected verification matrix.
- Contact-card QR handling had been shown/read/stored on one phone but not yet exchanged between two phones.
- Detailed offline map tiles are not bundled; offline fallback is country-level.
- Android background-service behavior can vary by device vendor.
- The Google Play flavor excludes SMS because of Play policy; the full GitHub/F-Droid flavor includes it.

Do not infer life-safety reliability from unit tests, emulator checks, or a small number of successful field transmissions.

## Licensing

Repository license is GPL-3.0. Upstream states the app is GPLv3 because it includes Meshtastic protobuf definitions under GPL-3.0 and points to THIRD_PARTY_NOTICES.md / NOTICE for other material. No implementation source was copied into Github-gold. Any later source reuse must preserve GPL and applicable third-party obligations.

## GitHub Gold verification performed

Inspected repository metadata, README/verification matrix, release metadata, recent commits and LICENSE. Confirmed current public release artifacts and active development through 2026-09-25.

GitHub Gold did **not** build the APK, run Gradle tests, install the app, inspect APK signatures independently, pair a Meshtastic device, attach Iridium/APRS hardware, transmit SMS/satellite/LoRa traffic, reproduce the field checks, test the local API, validate encryption, or audit the emergency/SOS implementation.

## Related projects / follow-up

- https://github.com/meshsat/meshsat — Raspberry Pi multi-bearer bridge already cataloged.
- https://github.com/meshsat/meshsat-fieldkit — physical field-kit hardware already cataloged.
- Meshtastic Android is a useful comparison for mature mesh-client behavior, but MeshSat Android's differentiator is its multi-bearer gateway/Reticulum role.

This completes the immediate MeshSat recursive research chain. Rotate the next discovery pass into another category unless new field evidence materially changes this project's maturity assessment.
