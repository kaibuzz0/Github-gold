# CivicMesh — walk-up emergency MeshCore portal

- **Repository:** https://github.com/rekab/CivicMesh
- **Author:** rekab
- **Category:** emergency communications / offline-first / LoRa mesh / Raspberry Pi
- **Evidence:** VERIFIED (repository-native implementation and bench/prototype evidence; not independently field-verified by GitHub Gold)
- **Provisional Gold score:** 27/30 — S tier
- **Score:** Utility 5 / Working Evidence 4 / Reusability 5 / Novelty 5 / Documentation 5 / Maintenance 3
- **License:** Apache-2.0
- **Discovery:** independent GitHub-first discovery, 2026-10-06

## What it is

CivicMesh turns a Raspberry Pi plus a MeshCore-compatible LoRa radio into an offline Wi-Fi captive portal for walk-up emergency communications. Ordinary phones can read and post to selected public mesh channels without installing an app, owning a radio, creating an account, or having internet access. Messages are stored locally in SQLite and queued onto MeshCore over USB serial; locally cached content remains readable when the radio or wider mesh is unavailable.

The project is explicitly aimed at Seattle Emergency Hubs and neighborhood-scale grid-down communications, but the architecture is reusable for other emergency hubs, mutual-aid sites, field camps, events, and disconnected community bulletin systems.

## Why it matters

The unusual value is the accessibility bridge. Most LoRa mesh systems still require every participant to possess compatible radio hardware and a companion application. CivicMesh places a browser-accessible Wi-Fi layer in front of that infrastructure so a single mesh node can serve many ordinary phones nearby.

It is also designed as a constrained appliance rather than a general-purpose internet gateway: no upstream internet, public channels only, local storage, rate limiting, operator CLI, explicit recovery states, and bounded store-and-forward behavior.

## Useful components and designs

- `web_server.py` — synchronous captive-portal HTTP service for local read/post/session/rate-limit behavior.
- `mesh_bot.py` — asynchronous MeshCore serial integration and outbox draining.
- `database.py` — shared SQLite/WAL state and durable message/outbox logic.
- `clock.py` + `docs/clock_consensus.md` — phone-assisted clock consensus for Pi nodes without RTC/NTP. Browsers contribute time observations; the service derives an offset rather than setting the host OS clock.
- `civicmesh.py` — operator CLI covering status, outbox/session management and operational diagnostics.
- `apply/` + configuration tooling — appliance deployment/rendering and systemd/network configuration paths.
- `external_display.py` and `inkplate/` — optional Inkplate e-paper bulletin display fed by compact JSON rather than framebuffer transport.
- Hub reference-library tooling — curated static emergency PDFs packaged for atomic install/rollback and offline phone download.
- radio recovery controller — detects prolonged radio unresponsiveness/outbox failure, resets the ESP32 via RTS, reconnects/verifies, then enters an explicit `NEEDS_HUMAN` state with bounded retry backoff when automatic recovery fails.
- optional Victron BMV battery telemetry path and on-node `power-test` diagnostic.

## Requirements / platform

Primary deployment target is a Raspberry Pi connected by USB serial to a MeshCore companion radio such as a Heltec V3. Walk-up clients need only a Wi-Fi-capable phone/browser. Optional hardware includes an Inkplate 6 e-paper display and a Victron BMV battery monitor.

The main application is Python and uses SQLite. Deployment also manages Linux networking/systemd components needed for the captive access point.

## Repository evidence inspected

- README architecture, scope, status, explicit non-goals, recovery behavior, offline document library, display design and clock-consensus description.
- Root source tree containing separate web, mesh, database, configuration, diagnostics, deployment, display and test surfaces.
- Large `tests/` tree covering outbox/admin/session behavior, API identity, apply ordering, document builds, migrations, CLI smoke behavior, clock handling and other subsystem paths.
- Recent commit history was inspected. The latest default-branch commit found is 2026-06-21 and includes deployment fixes for Bluetooth/power-monitor nodes plus regression tests. Nearby commits fix systemd restart-limit placement, diagnostic filesystem behavior, BLE MAC handling, dependency deployment and power-monitor UX.
- Root LICENSE is Apache License 2.0.

This is concrete repository-native evidence, but it is not equivalent to GitHub Gold independently reproducing a real emergency deployment.

## Evidence boundary and caveats

Upstream calls CivicMesh a **working prototype**. The README states that a few nodes run on the bench but none have been deployed in a real emergency or stress-tested by strangers at scale. Planned field validation includes hacker events and Seattle Emergency Hub drills.

Important limitations are deliberate and documented: no encrypted messaging, anonymity or direct messaging; public channels only; no internet gateway; and `sent-to-radio` means handed to the radio, not end-recipient delivery. HTTP-only captive-portal traffic should be treated as local-link visible. The system is not a replacement for licensed emergency/ACS traffic.

Maintenance is scored 3/5 because the last default-branch activity inspected was 2026-06-21, roughly three and a half months before this review. The repository is not archived and the implementation/test surface is substantial, but current cadence is lower than projects receiving a 4-5 maintenance score.

## Verification performed by GitHub Gold

GitHub Gold inspected repository-native documentation, source-tree structure, tests, license and commit history. It did **not** install CivicMesh, provision a Raspberry Pi, create a captive AP, run the test suite, attach a MeshCore radio, transmit LoRa traffic, test RTS recovery, validate phone-clock consensus under adversarial clocks, exercise an Inkplate, measure battery life, or conduct a real emergency/field drill.

Accordingly, VERIFIED means there is strong concrete upstream implementation and test evidence for the cataloged functionality; it is not independent operational certification.

## Reuse / licensing

Apache-2.0 permits broad reuse subject to its terms and preservation of notices. No upstream implementation code was copied into GitHub Gold. Reuse should retain the repository's LICENSE/NOTICE obligations and independently check licenses of bundled content, radio firmware, PDFs, dependencies and optional hardware-side components.

## Related ecosystem

- MeshCore — underlying LoRa mesh ecosystem and companion-mode serial interface.
- Heltec ESP32 LoRa boards — common radio hardware target.
- Inkplate — optional e-paper bulletin endpoint.
- Meshtastic — adjacent LoRa mesh ecosystem; CivicMesh currently favors MeshCore for companion-mode serial integration, channel semantics and regional adoption.

## Strong follow-up work

1. Run the full Python test suite and deployment/config golden tests in a clean Linux environment.
2. Bench a Pi + Heltec/MeshCore node with radio disconnects, USB resets, process crashes and power cuts while messages are queued.
3. Test SQLite/WAL durability and outbox idempotency across abrupt power loss and duplicate radio events.
4. Exercise the phone-clock consensus against skewed/malicious clients, low quorum and long no-client periods.
5. Load-test the captive portal with many simultaneous walk-up clients and rate-limit/session churn.
6. Measure radio airtime/backpressure behavior when Wi-Fi posting greatly exceeds LoRa capacity.
7. Verify hub-document atomic install/rollback and corrupted/incomplete package handling.
8. Test Inkplate stale-data, AP-loss and deep-sleep recovery behavior.
9. Conduct a controlled public drill with non-builder users and record usability, delivery latency, message loss and operator workload.
10. Compare the architecture with equivalent Meshtastic bridges and determine whether a backend abstraction could support both ecosystems without weakening the constrained appliance model.
