# MeshSat Android — mobile multi-bearer off-grid gateway

- **Upstream:** https://github.com/meshsat/meshsat-android
- **Author/org:** MeshSat
- **Category:** Android / emergency communications / mesh / satellite / DTN / radio interoperability
- **Evidence:** VERIFIED (upstream evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** **29/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 5/5
  - Documentation 5/5
  - Maintenance 4/5
- **License:** GPL-3.0; third-party material separately noticed upstream
- **Discovery:** recursive follow-up from the MeshSat gateway and Field Kit dossiers

## Why it matters

MeshSat Android turns an Android phone into a standalone communications gateway rather than merely a UI for a radio. The phone can bridge Meshtastic over BLE, Iridium SBD through a MeshSat node, cellular SMS, APRS/KISS, MQTT/Hub connectivity and Reticulum routing while retaining useful offline behavior. This is a strong reference architecture for field communications where links are intermittent, heterogeneous, costly, or absent.

The design is particularly valuable because it treats bearers differently instead of pretending they are equivalent. Satellite sessions are credit-sensitive and queued; mesh is local and free; SMS uses the phone modem; Reticulum provides a routing layer; and the application exposes queue/routing state to the operator.

## Concrete upstream evidence

The upstream README explicitly labels the project **pre-release** and says it has never been deployed to a real end user or used in an actual emergency. That limitation is important and is preserved here.

Upstream reports physical testing on 19–20 September 2026 using a Pixel 9a and a MeshSat node. Reported verified paths include:

- Meshtastic mesh through the node over BLE;
- three outbound Iridium messages reaching the Hub;
- inbound Iridium reception;
- storing a message arriving during a satellite session (after a documented earlier loss bug);
- reconnecting after application restart and reacquiring the node modem;
- offline satellite-pass prediction;
- Hub bridge connectivity;
- recovery from a node restart during a modem session, with the app reporting recovery in about eight seconds;
- Hub delivery receipts for satellite messages.

Upstream separately marks RockBLOCK 9704 hardware, mesh/online-Hub SOS paths, two-phone contact-card exchange and real emergency deployment as unverified or not yet exercised. This explicit negative evidence materially increases confidence in the project's documentation discipline.

## Release / maintenance evidence

Stable release **v2.19.4** was published 27 September 2026. GitHub release assets include architecture-specific and universal APKs plus a Play AAB, with SHA-256 digests recorded by GitHub. The repository remained actively modified the same day, including a fix that refreshes live node satellite statistics while the health card is visible and documentation of a physically observed node reboot/reconnect behavior.

Release documentation states that APK releases are signed consistently and provides the expected signing-certificate digest. GitHub Gold has not independently downloaded or verified those signatures.

## Reusable technical surfaces

### Multi-bearer gateway service

`GatewayService` is a useful architecture reference for coordinating radio/modem transports from a long-running Android foreground service. The source search surface shows immediate storage of Iridium mobile-terminated data arriving during any satellite session, avoiding dependence on a later polling cycle.

### Reticulum transport node

The phone is designed to operate as a Reticulum transport node and relay among mesh, Iridium, MQTT and TCP paths. The repository's test strategy lists dedicated `RnsHdlcTest`, `RnsInterfaceTest` and `RnsTransportNodeTest` coverage.

### Delay/disruption-tolerant components

The test strategy exposes dedicated DTN surfaces including `BundleFragmenterTest`, `BundleReassemblerTest` and `CustodyManagerTest`, plus FEC/RLNC tests (`GaloisField256Test`, `RlncDecoderTest`, `ReedSolomonTest`). These are high-value follow-up components because they may be reusable beyond the application UI.

### Cost-aware satellite behavior

SBD sessions are deliberately not timer-polled merely to check mail because each session consumes a credit. Messages remain queued/retried, and the application can use pass prediction generated on-device from bundled/refreshed orbital data. This is a useful design pattern for metered intermittent transports.

### Safety fan-out

The SOS controller is designed to fan an alert across available satellite, mesh, SMS and Hub paths and retain per-route status until cancellation. Upstream carefully distinguishes emulator-tested, frame-tested and not-yet-exercised routes, so this should not be treated as field-proven emergency behavior.

### Local automation API

A loopback API is exposed on `127.0.0.1:6051`, making the gateway potentially composable with on-device automation without exposing that control surface directly to the network.

## Platform / build

Upstream requires Android 8.0+, JDK 17 and Android SDK compile SDK 35. The implementation uses Kotlin 2.1 / Jetpack Compose, Room, ONNX Runtime, osmdroid, Eclipse Paho MQTT, BouncyCastle and NanoHTTPD. The build exposes F-Droid/full and Google Play/no-SMS product flavors.

## Licensing

The root repository is GPL-3.0. Upstream states that Meshtastic protobuf definitions are GPL-3.0 and that additional third-party notices are tracked separately. **No upstream implementation source is copied into GitHub Gold.** Any future extraction/adaptation must preserve GPL obligations and review the relevant third-party notices.

## Verification boundary

GitHub Gold inspected repository-native documentation, release metadata, source-search results, test-strategy evidence, licensing and current commit activity. GitHub Gold did **not**:

- build or install the APK;
- execute JVM/instrumentation tests;
- pair a Meshtastic or MeshSat node;
- transmit LoRa, SMS, APRS or Iridium traffic;
- consume paid satellite credits;
- reproduce the reported Pixel hardware tests;
- verify release signatures locally;
- exercise SOS behavior;
- audit cryptography or authentication;
- benchmark battery use, background survival or radio throughput;
- validate behavior during an actual emergency.

Accordingly, VERIFIED means there is concrete upstream implementation/test/hardware/release evidence for the cataloged functionality, not that GitHub Gold independently field-tested the system.

## Caveats

- Pre-release prototype; never deployed to a real user or actual emergency according to upstream.
- RockBLOCK 9704 path exists but is not hardware-tested upstream.
- Some safety routes remain unexercised.
- OEM Android background-service behavior can affect reliability.
- Satellite operation has real monetary and environmental constraints.
- APRS/amateur-radio operation can carry licensing/regulatory requirements depending on jurisdiction and configuration.
- A 29/30 score reflects exceptional evidence and architecture, not production/emergency certification.

## Strong next leads

1. Inspect the DTN `BundleFragmenter` / `BundleReassembler` / `CustodyManager` implementation and tests as a standalone reusable component.
2. Inspect RLNC/Reed-Solomon implementation and provenance/licensing.
3. Trace the Reticulum transport-node implementation against upstream RNS interoperability assumptions.
4. Rotate the main discovery stream away from MeshSat after one component-level follow-up, to preserve catalog breadth.
