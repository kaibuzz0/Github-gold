# LighthouseReckoning — lightweight confirmed-hop LoRa mesh routing

- **Upstream:** https://github.com/TidalImpact/LighthouseReckoning
- **Author:** Fynn Jannis Schulz / TidalImpact
- **Category:** embedded systems / LoRa / off-grid networking / sensor telemetry
- **Evidence:** VERIFIED (repository-native implementation, releases, documentation, and published raw field-test evidence inspected; not independently executed by GitHub Gold)
- **Provisional Gold score:** **28/30 — S tier**
  - Utility 5/5
  - Working Evidence 4/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 5/5
  - Maintenance 5/5
- **License:** MIT
- **Primary language:** C++ / Arduino
- **Platforms:** Arduino-family MCUs; upstream specifically reports testing on RP2040 and ESP32; SX126x CAD/interrupt behavior is specifically validated upstream.
- **Core dependency:** RadioLib
- **Discovery:** independent GitHub-first search during GitHub Gold stewardship; not attributed to a YouTube transcript.

## Why it matters

LighthouseReckoning is a deliberately small routing/reliability layer for LoRa sensor networks where many field nodes need to deliver data toward one fixed Home node without Wi-Fi or Internet. Rather than maintaining a global topology, each node advertises its hop distance to Home and chooses a neighbor that moves traffic closer. Each radio hop is individually confirmed and retried.

This is useful as a reusable embedded component because the application-facing API remains small (`beginAsNode` / `beginAsHome`, `update`, `sendData`, receive callback), the implementation is non-blocking/interrupt-driven, and the library depends only on RadioLib.

## Evidence inspected

### Current upstream documentation and implementation claims

The README documents automatic neighbor discovery, multi-hop route selection toward Home, hop-by-hop confirmations, local retries, TTL/loop controls, optional regional duty-cycle budgeting, and a compact wire format. It documents a 16-byte DATA header without encryption and 23 bytes with encryption.

Upstream says RP2040 and ESP32 are tested platforms. SX126x Channel Activity Detection and the single-DIO1 interrupt design are specifically reported as validated; other RadioLib-supported radios are expected to handle basic send/receive but are not claimed as equivalently verified.

### Real field-test evidence

The repository contains `fieldtests/2026-08-09_forced-chain-test/RESULTS.md` and the accompanying ~50 KB raw serial log. The test deliberately forced four field nodes into a linear relay topology terminating at Home, despite all nodes being physically close enough to reach Home directly. It ran for about 1 hour 53 minutes at 868 MHz / 125 kHz / SF9 / CR 4/8 / 22 dBm.

The published results report expected TTL values throughout the run and three estimated packet losses total. The two shortest paths reported no loss. Upstream interprets the observed losses as consistent with channel contention, but the Home-side log cannot identify the exact failed relay segment; that causal explanation should therefore be treated as an upstream inference rather than a proven diagnosis.

The raw log being committed beside the analysis is unusually useful: later GitHub Gold work can independently parse it instead of relying solely on summary prose.

### Releases and maintenance

Stable `v1.2.0` was published 2026-09-24. Its release notes add internal locking for dual-core RP2040 and ESP32/FreeRTOS multi-task use while retaining the public API. `v1.1.0` added optional AES-128-CCM packet protection and persistent/batched nonce allocation. `v1.0.0` was published in August 2026. Default-branch commits continued through 2026-09-22.

The project also has a Zenodo DOI and documents use in the ZDIN water research sub-project Adam4EvesWine. This is useful provenance, but it is not substituted for implementation/field evidence in the score.

## Particularly reusable components / ideas

1. **Distance-to-Home routing** — small-state routing for sensor networks that only need many-to-one delivery rather than arbitrary peer-to-peer routing.
2. **Hop-by-hop DATA confirmation/retry state machine** — reliability without requiring Home to maintain reverse routes to every sensor.
3. **Non-blocking RadioLib integration** — `update()` plus DIO1 interrupt handling is suitable for constrained embedded applications.
4. **Compact packet framing** — useful reference for low-airtime telemetry protocols.
5. **Duty-cycle budgeting** — relevant to legally constrained ISM-band deployments.
6. **Forced-hop field-test technique** — `setMinimumAcceptedHops()` provides a practical way to exercise multi-hop behavior without needing kilometer-scale physical separation.
7. **Committed raw field logs** — a good evidence/provenance pattern for embedded networking projects.
8. **Cross-core/task locking added in v1.2.0** — relevant for RP2040 multicore and ESP32 FreeRTOS integrations.

## Security boundary

Optional encryption is AES-128-CCM with a network-wide pre-shared key and hop-by-hop decrypt/re-encrypt behavior. It is **not end-to-end encryption**: relay nodes possess the shared key and see plaintext while forwarding.

More importantly, the current README explicitly states that replay protection is not yet implemented. A captured valid encrypted packet can be retransmitted and still authenticate. This prevents treating the security layer as a complete hostile-environment messaging design.

Nonce persistence is supported on ESP32 and RP2040. Encryption is compiled out on unsupported targets such as classic AVR.

## Limitations / caveats

- Topology is intentionally many-to-one toward a single Home; it is not a general arbitrary-peer mesh.
- Hop-by-hop confirmation does not tell the originating node that Home ultimately received a packet.
- Current shared-key encryption trusts every relay and lacks replay protection.
- The field test deliberately forced the topology at short physical range, so it demonstrates routing/retry behavior but does not establish long-distance RF performance.
- The field test observed packet loss and cannot localize the failing relay hop from the Home log alone.
- Upstream says radios beyond the specifically validated SX126x behavior may work through RadioLib, but that broader hardware surface has not been equivalently verified.
- GitHub Gold did not independently build, flash, run, RF-test, cryptographically audit, or reproduce the field results in this pass.

## Verification boundary

This dossier's VERIFIED classification means concrete repository-native evidence was inspected: source-oriented documentation, stable releases, explicit platform constraints, a detailed real-hardware forced-chain test, and its committed raw serial log. It does **not** mean GitHub Gold independently executed the firmware or reproduced upstream measurements.

## Licensing

Root project license is MIT. No upstream source was copied into GitHub Gold. RadioLib and any application dependencies/hardware support packages retain their own licensing and should be reviewed before redistribution.

## Follow-up research

- Parse `raw_serial_log.txt` independently and reproduce the packet/TTL/loss counts.
- Inspect the retry/RFCN state machine and duplicate handling directly in `src/`.
- Inspect AES-CCM nonce reservation and power-loss behavior.
- Check whether replay protection lands in a later release and promote that security property only after evidence exists.
- Compare airtime/control overhead against Meshtastic, MeshCore and minimal flooding/tree-routing alternatives under identical PHY parameters.
- Look for longer-range, obstructed-path, mobility, power-consumption and larger-node-count field tests.
- Inspect RadioLib integration for portability to additional SX126x/SX127x targets.
