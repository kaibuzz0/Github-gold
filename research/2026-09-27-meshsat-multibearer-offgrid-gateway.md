# MeshSat — multi-bearer off-grid communications gateway

- **Repository:** https://github.com/meshsat/meshsat
- **Author / Org:** MeshSat
- **Category:** emergency communications / off-grid networking / Reticulum / LoRa / satellite / APRS / embedded Linux
- **Evidence:** VERIFIED
- **Gold score:** 29 / 30
- **Tier:** S
- **Discovery:** independent GitHub-first discovery, 2026-09-27
- **License:** GPL-3.0

## Summary

MeshSat is a Linux gateway that bridges otherwise separate off-grid and degraded-network transports through a Reticulum/LXMF-aware routing fabric. The current upstream tree documents Meshtastic LoRa, Iridium SBD and IMT, cellular SMS, APRS/AX.25, ZigBee, BLE and TCP bearers, plus RNode, UDP, AutoInterface and raw KISS Reticulum interfaces. TAK, MQTT and webhooks are also exposed as routing destinations.

This is unusually strong GitHub Gold material because the project is not merely a protocol sketch: upstream records specific hardware and interoperability evidence, ships a Docker deployment path, maintains a large automated test suite, and explicitly documents what has *not* been proven.

## Score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Bridges several otherwise incompatible communications systems during degraded/off-grid operation. |
| Working evidence | 5 | Upstream reports physical tests across Meshtastic, Iridium SBD/IMT, SMS and APRS plus extensive software interoperability tests. |
| Reusability | 5 | Distinct gateway, routing, codec, device-supervision, delivery-ledger and API surfaces are reusable architectural references. |
| Novelty | 5 | Cost-aware multi-bearer routing across LoRa, satellite, SMS, packet radio and Reticulum is an unusual integration surface. |
| Documentation | 5 | README, deployment instructions, hardware matrix, API/docs links, explicit proven/not-proven table and detailed commit messages. |
| Maintenance | 4 | Very active September 2026 development, but upstream still calls the system pre-release and real-user/disaster deployment evidence is absent. |

**Total: 29 / 30 — S**

## Concrete capabilities and components

### Multi-bearer gateway fabric

Upstream documents eight principal bearer families:

- Meshtastic LoRa via official protobuf bindings
- Iridium 9603 SBD
- Iridium 9704 IMT
- cellular SMS
- APRS / AX.25 through KISS/Direwolf
- ZigBee using CC2652P / Z-Stack ZNP
- BLE GATT with segmentation
- TCP / Reticulum interoperability

Reticulum interfaces additionally include RNode, UDP, AutoInterface and raw KISS TNC support. The architecture is valuable as a reference for normalizing highly heterogeneous links with very different MTU, cost, latency and reliability characteristics.

### Reticulum and LXMF interoperability

Recent upstream work adds a native LXMF endpoint and Reticulum packet/link/resource machinery. The maintainers report interoperability testing against Python RNS 1.5.4 and LXMF 1.1.0, including announces, path requests, proofs, resources, LXMF messages, stamps, RNode, UDP, AutoInterface and KISS paths. Recent commits also add CrossTalk-compatible RNSI framing for Iridium IMT.

Reusable surfaces worth deeper study include:

- `internal/rns` transport/link/resource handling
- `internal/lxmf` message packing, signatures, stamps, dedup and delivery
- `internal/msgpack` byte-compatible encoding required by LXMF hashing
- `internal/kiss` framing
- `internal/rnode` host protocol
- routing interface manager and runtime interface CRUD
- delivery ledger and retry behavior

### Device and bearer abstraction

The system scans USB devices, identifies hardware by VID:PID plus protocol probing, and treats missing hardware as a degraded configuration rather than a fatal startup error. Multi-instance gateways allow multiple modems of one type to coexist with independent workers/configuration.

This is a useful pattern for field systems where available radios vary between deployments.

### Emerging HF codec/gateway

September 25 commits introduce a public 10 m HF codec and modem path: radix-40 callsigns, LXMF destination hashes, fragmentation, CRC-16-CCITT, LDPC(128,64), interleaving, CPFSK modulation/demodulation, timing/frequency-offset search and soft decoding. Upstream commit evidence reports decoding tests at multiple SNRs and frequency offsets and an end-to-end receive path against a fake `rtl_tcp` source.

Treat this as newer evidence than the more established LoRa/satellite/SMS paths. It should be independently inspected before being elevated into a separate component dossier.

## Runtime and platforms

- Go 1.24 module
- ARM64 or x86_64 Linux
- Docker deployment is the primary documented quick-start
- reference hosts include Raspberry Pi 4 and 5
- Vue 3 dashboard embedded in the binary
- SQLite persistence
- REST API, server-sent events and Prometheus metrics

The Go module currently depends on Meshtastic protobuf bindings, MQTT, Chi, D-Bus, UUID, WebSocket, sqlx, compression, Reed-Solomon, Prometheus, serial/GPIO libraries, x/crypto and modernc SQLite among other packages.

## Upstream verification evidence

The README explicitly reports:

- Meshtastic serial working on both field kits
- Iridium 9704 IMT MO/MT verified over a real satellite link in March 2026
- Iridium 9603 SBD working on hardware
- cellular SMS working in both directions
- APRS/AX.25 working on hardware
- Reticulum interoperability tested against RNS 1.5.4 / LXMF 1.1.0 and stock `rnsd`
- HeMB bonding across LoRa, TCP and SMS tested in a three-bearer April 2026 field test
- 1,628 test functions across 203 files, stated to gate deploys

Recent September 25 commits provide further test-oriented evidence for RNode, UDP, AutoInterface, KISS, LXMF, IMT framing and the emerging HF modem.

## Explicit upstream limitations

Upstream is unusually clear about boundaries:

- project status is **pre-release**
- no deployment to a real end user is claimed
- no actual-disaster use is claimed
- HeMB over a paid satellite bearer is not validated
- mixed free/paid HeMB capacity allocation remains undefined
- RTL-SDR jamming detection has only been tested against ambient noise, not an actual jammer
- ZigBee has limited field exposure
- one OOB management reply path remains unobserved
- Reticulum interoperability has not yet been exercised against Sideband/CrossTalk clients on real hardware

These caveats materially constrain operational trust despite the high software-evidence score.

## License and reuse

Root license is GNU GPL v3. No source was copied into GitHub Gold. Any future adaptation or redistribution of covered implementation code must preserve GPL-3.0 obligations and applicable notices. Dependencies, firmware and companion projects must be license-audited separately before code reuse.

## Verification performed by GitHub Gold

Performed in this research pass:

- inspected upstream README and its explicit proven/not-proven matrix
- inspected root GPL-3.0 license
- inspected `go.mod`
- inspected recent commit history through 2026-09-25
- confirmed active work around RNode, LXMF, Reticulum interfaces, Iridium framing and HF modem/codec
- checked the existing GitHub Gold catalog/research index for `meshsat`; no prior entry was found

Not performed:

- no build or test execution
- no Docker deployment
- no Raspberry Pi or radio hardware testing
- no Meshtastic/Iridium/SMS/APRS/ZigBee/BLE/HF field test
- no satellite airtime purchase or modem session
- no independent Reticulum/LXMF interoperability run
- no RF measurements
- no security audit
- no disaster/emergency operational validation

All hardware/interoperability claims above are therefore **upstream evidence**, not independent GitHub Gold reproduction.

## Related ecosystem

- https://github.com/meshsat/meshsat-android — mobile gateway companion
- https://github.com/meshsat/meshsat-fieldkit — field hardware / carrier boards / CAD
- Reticulum / LXMF ecosystem
- Meshtastic firmware and clients
- CrossTalk interoperability work

## Follow-up research

Highest-value next investigations:

1. Inspect the delivery ledger and cost policy, especially failure/retry semantics across paid and free bearers.
2. Audit the Reticulum/LXMF implementation boundaries against upstream Python RNS/LXMF behavior.
3. Inspect `meshsat-fieldkit` for reproducible carrier-board and power architecture.
4. Inspect `meshsat-android` for portable BLE/SMS/Iridium gateway components.
5. Isolate the new HF10m codec/modem as a possible component dossier only after checking tests, normative source/provenance and regulatory assumptions.
6. Review the security/trust model, key storage and management-frame authentication before recommending operational use.

## Verdict

**VERIFIED — S / 29.** MeshSat is one of the stronger emergency/off-grid communications discoveries in the catalog because it combines unusual multi-bearer architecture with concrete hardware evidence, explicit interoperability work, a large test surface and unusually candid limitations. Its pre-release status and lack of real-user/disaster deployment prevent treating it as operationally proven.