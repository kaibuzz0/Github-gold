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

### Termux Tools

- **Repository:** https://github.com/termux/termux-tools
- **Author / Org:** Termux
- **Category:** Android / Termux / shell utilities / package infrastructure
- **Evidence:** VERIFIED
- **Tier / Score:** A / 25
- **What it does:** Official collection of scripts and small programs shipped in Termux's core `termux-tools` package, including package/mirror plumbing and Termux environment utilities.
- **Why it is valuable:** It is upstream infrastructure rather than a third-party wrapper, making it a strong reference for portable Android shell patterns, package tooling, mirror selection, environment setup, and small utilities that are known to live inside the Termux ecosystem.
- **Useful code/components:** `scripts/` utilities; `src/` programs; mirror metadata and selection infrastructure; Termux properties initialization; login/environment helpers.
- **Install / runtime:** Distributed as part of Termux package infrastructure; source includes autotools build files.
- **Platforms:** Android / Termux.
- **License:** GNU GPL-3.0.
- **Maintenance signals:** Upstream Termux organization; repository history and active issue/PR surface observed during discovery.
- **Verification performed:** Inspected official README and COPYING file. No local Android execution performed by GitHub Gold.
- **Source discovery:** Independent Termux ecosystem pass.
- **Related projects:** termux/termux-app; termux/termux-packages; termux/termux-api.
- **Caveats / risks:** GPL-3.0 obligations apply to copied/modified covered code. Prefer linking or clearly separated compliant reuse rather than casually vendoring pieces.
- **Research notes:** High-value source for future component-level mapping of tiny, battle-tested Android/Termux utilities.

### termux-adb

- **Repository:** https://github.com/nohajc/termux-adb
- **Author / Org:** nohajc
- **Category:** Android / Termux / ADB / Fastboot / USB interoperability
- **Evidence:** VERIFIED
- **Tier / Score:** A / 23
- **What it does:** Patches ADB and Fastboot so one Android device can debug another over USB from Termux without root, using `termux-usb` to obtain user-approved USB file descriptors.
- **Why it is valuable:** Solves a concrete Android limitation with a clever reusable interoperability pattern: Android's USB permission API plus Unix-domain-socket file-descriptor passing into otherwise conventional native tooling.
- **Useful code/components:** patched ADB/Fastboot USB enumeration; `termux-usb` integration; Unix-domain-socket file-descriptor transfer; install repository bootstrap; Termux package build adaptations.
- **Install / runtime:** Requires Termux and Termux:API; upstream provides an install script and apt repository. USB device access requires Android user approval.
- **Platforms:** Android / Termux; target devices accessed through USB/OTG.
- **License:** MIT for this repository; bundled/submodule upstream Android tools may carry their own licenses and must be reviewed separately before extraction.
- **Maintenance signals:** Repository contains substantial history and documented current limitations rather than presenting the patch as magic.
- **Verification performed:** Inspected README and root MIT LICENSE. No device-to-device ADB test performed by GitHub Gold.
- **Source discovery:** Independent Termux ecosystem pass.
- **Related projects:** termux/termux-api; termux/termux-packages; Android platform-tools.
- **Caveats / risks:** Installation command pipes a remote script into a shell; inspect before execution. Fastboot enumeration can be slow. Component licensing must account for upstream Android code, not only the repository's root MIT license.
- **Research notes:** Strong candidate for architecture notes explaining Android USB FD bridging without copying the large Android-tools codebase.

### ESP32-S3 Remote ID Add-on (`esp-remoteid`)

- **Repository:** https://github.com/peinser/esp-remoteid
- **Author / Org:** Peinser BV / peinser
- **Category:** ESP32-S3 / OpenDroneID / embedded firmware / interoperability
- **Evidence:** PROMISING
- **Tier / Score:** A / 24
- **What it does:** ESP-IDF firmware for broadcasting standards-based OpenDroneID / ASTM F3411 Remote ID messages over BLE and Wi-Fi, with configuration for identity, position, transports, indicators, and MAVLink input.
- **Why it is valuable:** Well-documented standards implementation built around the official `opendroneid-core-c` library, with clear transport behavior, ESP-IDF configuration, devcontainer tooling, and integration paths for flight-controller telemetry.
- **Useful code/components:** OpenDroneID state/transport integration; BLE Remote ID advertisements; Wi-Fi beacon/NAN transport; Kconfig configuration; MAVLink OpenDroneID ingestion; readiness gating; status indicators; devcontainer build workflow.
- **Install / runtime:** ESP-IDF environment with recursive git submodules; upstream documents build/flash/monitor workflow.
- **Platforms:** ESP32-S3 plus compatible host development environment.
- **License:** Apache-2.0 at repository root; dependency/submodule licenses must also be preserved.
- **Maintenance signals:** 2026 project with extensive current documentation and active feature TODOs.
- **Verification performed:** Inspected upstream README and Apache-2.0 LICENSE. No firmware build or RF hardware test performed by GitHub Gold.
- **Source discovery:** Remote ID ecosystem branch from the ESP32/OUI-SPY research direction.
- **Related projects:** opendroneid/opendroneid-core-c; opendroneid/receiver-android; ArduPilot/ArduRemoteID.
- **Caveats / risks:** Regulatory compliance depends on jurisdiction and configuration. Catalog for legitimate Remote ID implementation, interoperability, education, and receiver testing; do not treat documentation claims as independent certification.
- **Research notes:** Apache licensing and modular design make this a particularly useful candidate for deeper source-level study after dependency-license review.

## Rejected / Deferred Leads

- **PeterJBurke/esp32-c3-remote-id:** deferred because its own README explicitly states it is broken after an ESP development-stack upgrade and may be deleted. Keep as historical lead only; do not promote as working Gold.
- **colonelpanichacks/Remote-ID-Spoofer:** not promoted. Although technically related, its primary purpose is Remote ID spoofing; outside this catalog's preferred defensive/interoperability quality bar.

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
