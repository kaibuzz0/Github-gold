# MeshSat — multi-bearer off-grid communications gateway

- **Repository:** https://github.com/meshsat/meshsat
- **Organization:** meshsat
- **Category:** Emergency communications / mesh gateways / DTN / radio interoperability
- **Evidence:** VERIFIED (upstream repository evidence; no first-party GitHub Gold runtime test)
- **Provisional Gold score:** **29/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **Primary language/runtime:** Go 1.24+, Linux, Docker; Vue 3 dashboard
- **License:** GPL-3.0
- **Hardware:** ARM64/x86_64 Linux host; reference hardware includes Raspberry Pi 4/5, Meshtastic radios, Iridium 9603/9704, cellular modems, KISS/APRS equipment, and CC2652P ZigBee adapters.

## Why it matters

MeshSat is unusually broad infrastructure for keeping messages moving when ordinary IP connectivity is unavailable. It bridges heterogeneous bearers instead of treating LoRa, satellite, cellular, packet radio, BLE, ZigBee and TCP as isolated systems. The project currently describes Meshtastic LoRa, Iridium SBD and IMT, cellular SMS, APRS/AX.25, ZigBee, BLE and TCP transports, with TAK, MQTT and webhooks as routing destinations. A Reticulum-compatible routing layer supplies path selection and the project is designed to run locally as a Docker container rather than requiring a vendor cloud account.

The strongest reason to catalog it is not feature count but evidence discipline. Upstream explicitly separates what has been exercised on hardware from what is only implemented, lightly exposed, unvalidated or still specification work. That is rare and makes the repository substantially easier to assess than projects that present every implemented path as production-proven.

## Working evidence inspected

The current README states that Meshtastic serial, Iridium 9603 SBD, cellular SMS and APRS/AX.25 are working on hardware; Iridium 9704 IMT was verified over a real satellite link in March 2026; Reticulum interoperability passes against upstream Python RNS 1.1.4; and a three-bearer HeMB test across LoRa, TCP and SMS completed in April 2026 with zero failures. It simultaneously records important negatives: paid-satellite HeMB is not validated, mixed free/paid allocation is undefined, RTL-SDR jamming detection has never been tested against a real jammer, ZigBee has limited field exposure, and the project has never been used by an emergency service or in an actual disaster.

Upstream reports **1,628 test functions across 203 files** and says the suite gates deployments. This is strong upstream working evidence, but it is not equivalent to GitHub Gold independently running those tests.

A public GitHub release exists (`v0.1.0`, 2026-03-04) with documented Docker startup, tested hardware and the initial Meshtastic/Iridium bridge. The current README labels the project **pre-release**, so release existence should not be mistaken for production maturity.

Default-branch commits were active through 2026-09-21. Recent commits include fixes derived from live kit behavior: power-state reporting, Iridium 9704/JSPR session handling, APRS booth-state correction and field/runbook updates. These are useful maintenance signals because they describe concrete observed hardware behavior rather than cosmetic churn.

## Valuable reusable components / patterns

- Multi-bearer transport abstraction spanning low-bandwidth RF, satellite, cellular and IP links.
- Reticulum interoperability layer for routing across heterogeneous interfaces.
- Meshtastic protobuf/serial gateway.
- Iridium 9603 SBD and 9704 IMT/JSPR gateway paths.
- Cellular AT/SMS gateway.
- APRS/AX.25 path with KISS TNC support and bundled Direwolf supervision.
- USB VID:PID plus protocol-probe device detection.
- Persistent delivery queue/dead-letter and retry concepts for intermittent links.
- Cost-aware bearer selection, including explicit documentation of the present free-first allocator limitation.
- TAK/CoT, MQTT and webhook integration points.
- Embedded Vue dashboard, REST API, SSE event stream and Prometheus metrics.
- Companion field-kit and Android repositories are strong recursive research leads.

## Install / runtime notes

Upstream documents a Docker deployment on Raspberry Pi/Linux using privileged device access, host networking and `/dev` plus `/sys` mounts. It also documents source builds via `make build-with-web`. Missing hardware is intended to degrade to warnings rather than preventing startup.

Because several bearers involve radio or satellite/cellular hardware, successful software startup does not prove end-to-end communications. Frequency allocation, amateur-radio rules, modem service plans, antenna installation, credentials/SIMs and local regulation remain deployment concerns.

## License and reuse caveat

The repository root carries **GNU GPL v3.0**. Do not copy implementation source into GitHub Gold as if it were permissively licensed. Catalog and link to the upstream implementation unless a downstream use is deliberately GPL-compatible and all corresponding obligations are understood. Preserve upstream copyright, notices and third-party notices.

No MeshSat source code was copied into this repository by this research pass.

## Verification boundary

GitHub Gold inspected repository metadata, the current README, license, release metadata and recent commit history. GitHub Gold **did not** build MeshSat, pull/run its container, execute the 1,628-test suite, attach radio/modem hardware, transmit over LoRa/APRS/SMS/Iridium, validate Reticulum interoperability, reproduce HeMB field tests, inspect RF compliance, or independently audit its security/cryptography.

Therefore `VERIFIED` means the repository contains strong, internally consistent primary-source evidence for the architecture, tests and stated hardware work. It does **not** mean GitHub Gold has certified it for emergency or life-safety use.

## Risks / limitations

- Explicitly pre-release and not yet deployed to a real end user.
- Never used in an actual disaster; do not treat it as certified emergency infrastructure.
- Some transport paths have materially less field exposure than others.
- Paid-bearer HeMB behavior and mixed free/paid allocation remain incomplete/unvalidated.
- Hardware and carrier dependencies can dominate real deployment reliability and cost.
- GPL-3.0 constrains redistribution/integration choices compared with permissive libraries.
- Broad hardware access in the documented Docker configuration deserves normal host-security scrutiny.

## Discovery provenance

Independent GitHub-first discovery after intentionally rotating away from the prior Jazz/Groove local-first database thread. The repository was not already present in the GitHub Gold code-search index under `meshsat` when checked.

## Related / recursive leads

1. `meshsat/meshsat-fieldkit` — CAD, carrier boards and physical deployment design.
2. `meshsat/meshsat-android` — standalone mobile gateway with BLE mesh, Iridium SPP and SMS.
3. Reticulum/RNS interoperability — inspect exactly which wire/protocol surfaces MeshSat implements and how conformance is tested.
4. HeMB multi-bearer bonding — investigate its coding/allocation design, measurement evidence and failure semantics without promoting unvalidated paid-satellite claims.
5. Delivery-ledger DTN work — custody transfer and fragmentation are roadmap items, not shipped evidence yet.

## Steward verdict

**Keep. High-value Gold candidate.** MeshSat earns a provisional S/29 because it combines unusual cross-bearer utility, strong documentation, concrete hardware evidence, a large upstream test surface and unusually candid limitation reporting. Maintenance is scored 4 rather than 5 because the project itself remains pre-release and has no real emergency-service deployment history. Revisit the score when the project reaches a more mature release or publishes independent field/deployment evidence.