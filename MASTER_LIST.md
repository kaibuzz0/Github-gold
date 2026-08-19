# GitHub Gold Master List

This is the human-readable catalog of high-value repositories, tools, reusable code, and research leads.

## Ranking

Each item is scored from 0–5 on:

- Utility
- Working evidence
- Reusability
- Novelty
- Documentation
- Maintenance

**Gold score:** sum out of 30.

Suggested tiers:

- **S — 26–30:** exceptional, immediately useful
- **A — 21–25:** high-value
- **B — 16–20:** useful with caveats
- **C — 10–15:** research lead
- **D — under 10:** weak, obsolete, or unverified

## Catalog

### Meshtastic Firmware

- **Repository:** https://github.com/meshtastic/firmware
- **Author / Org:** Meshtastic
- **Category:** LoRa / mesh networking / embedded firmware / off-grid communications
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Official firmware for the Meshtastic decentralized LoRa mesh network. Supports text messaging, location sharing, telemetry, and communication without cellular or internet infrastructure.
- **Why it is valuable:** Mature multi-platform firmware with active development, build instructions, flashing instructions, tests/CI signals, and support for ESP32, nRF52, RP2040/RP2350, and Linux-class targets.
- **Useful code/components:** mesh routing logic; LoRa transport; position/location modules; packet handling; node database; telemetry; Wi-Fi and HTTP/TLS support; hardware variants; modular device support.
- **Install / runtime:** Build from source or flash supported hardware using official Meshtastic tooling.
- **Platforms:** ESP32, nRF52, RP2040/RP2350, Linux and supported Meshtastic boards.
- **License:** GNU GPL-3.0.
- **Maintenance signals:** Multiple commits observed on 2026-08-18/19 fixing routing, position-channel behavior, device builds, and TLS memory recovery; project README exposes CI status.
- **Verification performed:** Inspected official README, license, and latest commit history. Not hardware-tested by GitHub Gold yet.
- **Source discovery:** GitHub-first discovery pass.
- **Related projects:** meshtastic/Meshtastic-Android; meshtastic/python; meshtastic/web; meshtastic/protobufs; ShakataGaNai/awesome-meshtastic.
- **Caveats / risks:** GPL-3.0 is copyleft; copied/modified covered code must be handled under its license obligations. Radio operation must comply with applicable local rules.
- **Research notes:** Strong candidate for deeper component-level extraction analysis rather than wholesale duplication.

### OUI-SPY Unified Blue

- **Repository:** https://github.com/colonelpanichacks/oui-spy-unified-blue
- **Author / Org:** colonelpanichacks
- **Category:** ESP32-S3 / passive radio observation / BLE / Wi-Fi / PCAP / drone Remote ID
- **Evidence:** PROMISING
- **Tier / Score:** A / 24
- **What it does:** Multi-mode firmware for the Seeed Studio XIAO ESP32-S3. The README documents six modes: configurable BLE target detection, RSSI foxhunting, passive Flock-oriented Wi-Fi observation, Wi-Fi PCAP capture, FAA Remote ID drone monitoring, and passive BLE advertising capture.
- **Why it is valuable:** Combines several reusable embedded-radio ideas behind one small device and exposes browser flashing, on-device dashboards, USB-CDC command protocols, packet capture, persistence, and modular firmware selection.
- **Useful code/components:** boot firmware selector; BLE signature matching; RSSI proximity feedback; Wi-Fi promiscuous capture; PCAP streaming; Wireshark extcap helpers; Open Drone ID parsing; BLE advertisement PCAP; USB-CDC command protocol; SPIFFS persistence; browser flasher.
- **Install / runtime:** README documents browser flashing plus Python/esptool flashing for Seeed Studio XIAO ESP32-S3.
- **Platforms:** Seeed Studio XIAO ESP32-S3; desktop browser/Python tools for flashing; companion host tooling referenced by upstream.
- **License:** UNKNOWN — no root LICENSE file found during this pass.
- **Maintenance signals:** Active commits observed on 2026-08-18, including fixes to BLE SNIFF rendering and flasher updates for newly integrated modes.
- **Verification performed:** Inspected upstream README and recent commit history. Root LICENSE lookup returned 404. No hardware test performed by GitHub Gold yet.
- **Source discovery:** GitHub-first discovery pass; matches the broader hardware/tool research direction.
- **Related projects:** colonelpanichacks/flock-you; colonelpanichacks/ouispy-pcap; colonelpanichacks/ouispy-blesniff; colonelpanichacks/Oui-Spy-UniPwn.
- **Caveats / risks:** Do not copy or redistribute source into GitHub Gold until licensing/permission is established. Some modes concern surveillance-device detection; catalog for defensive, interoperability, research, and personal situational-awareness use.
- **Research notes:** High-priority repository to map at file/component level once license status is resolved.

## Entry format

### Project / Tool Name

- **Repository:**
- **Author / Org:**
- **Category:**
- **Evidence:** VERIFIED / PROMISING / LEAD / ARCHIVED
- **Tier / Score:**
- **What it does:**
- **Why it is valuable:**
- **Useful code/components:**
- **Install / runtime:**
- **Platforms:**
- **License:**
- **Maintenance signals:**
- **Verification performed:**
- **Source discovery:**
- **Related projects:**
- **Caveats / risks:**
- **Research notes:**
