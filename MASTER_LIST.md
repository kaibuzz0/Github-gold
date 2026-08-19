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

### OpenDroneID Core C

- **Repository:** https://github.com/opendroneid/opendroneid-core-c
- **Author / Org:** OpenDroneID
- **Category:** C library / Remote ID / protocol encoding / embedded interoperability
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Core C library for packing and unpacking Open Drone ID messages defined by ASTM F3411 and ASD-STAN Direct Remote ID specifications, with MAVLink conversion helpers and reference Wi-Fi code.
- **Why it is valuable:** This is the standards-focused core used by other Remote ID implementations rather than a device-specific wrapper. It exposes compact encode/decode APIs, data structures, tests, memory-reduction options, MAVLink adapters, and reference broadcast code suitable for embedded or Linux integrations.
- **Useful code/components:** `libopendroneid/opendroneid.h`; message encoders/decoders for Basic ID, Location, Authentication, Self ID, System, Operator ID, and MessagePack; `libmav2odid` conversion layer; Wi-Fi beacon/NaN reference code; CMake build; unit tests; low-memory compile options.
- **Install / runtime:** CMake build on Linux; upstream documents dependencies and commands for building the shared library, sample app, and tests.
- **Platforms:** Portable C library; Linux reference tooling; embedded integrations through downstream projects.
- **License:** Apache-2.0.
- **Maintenance signals:** Commits observed on 2026-08-01 updating protocol validation/documentation and adding GB 46750-2025 work; README documents CI and tests.
- **Verification performed:** Inspected README, root Apache-2.0 LICENSE, build/test documentation, public API description, and recent commit history. GitHub Gold did not execute the test suite in this pass.
- **Source discovery:** Follow-up from `esp-remoteid` and the OpenDroneID ecosystem.
- **Related projects:** opendroneid/receiver-android; opendroneid/wireshark-dissector; opendroneid/transmitter-linux; ArduPilot/ArduRemoteID; peinser/esp-remoteid.
- **Caveats / risks:** Standards and jurisdictional compliance can change; dependency licenses and specification requirements still need review for any redistributed integrated product.
- **Research notes:** Strong component-level Gold. Prefer consuming or adapting this core with preserved Apache notices instead of reimplementing Remote ID packing logic from scratch.

### LocalSend

- **Repository:** https://github.com/localsend/localsend
- **Author / Org:** LocalSend
- **Category:** local-first / offline file transfer / cross-platform / privacy
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Cross-platform local-network file and message transfer without cloud infrastructure or an internet connection. Devices discover and communicate locally using a documented REST/HTTPS protocol.
- **Why it is valuable:** Mature example of a user-controlled, serverless local workflow with Android, iOS, macOS, Windows, Linux, and Fire OS distribution. It combines local discovery, encrypted transfers, portable mode, cross-platform packaging, and a separately documented protocol.
- **Useful code/components:** local peer discovery; HTTPS certificate generation; REST-based transfer flow; file/message transfer logic; portable configuration mode; cross-platform packaging; companion `localsend/protocol` specification.
- **Install / runtime:** Distributed through major app stores/package managers; source build uses Flutter, Rust, FVM, and platform-specific packaging steps.
- **Platforms:** Android, iOS, macOS, Windows, Linux, Fire OS.
- **License:** Apache-2.0.
- **Maintenance signals:** Same-day commit activity observed on 2026-08-19; release 1.18.2 observed on 2026-08-17; README exposes CI and broad distribution channels.
- **Verification performed:** Inspected README, root Apache-2.0 LICENSE, build documentation, protocol description, and recent commit history. No local transfer test performed by GitHub Gold.
- **Source discovery:** Independent local-first/offline software pass.
- **Related projects:** localsend/protocol; localsend/web; community protocol implementations.
- **Caveats / risks:** Local-network reachability depends on firewall/router configuration and AP isolation. Dependency licenses must be reviewed before extracting bundled implementation pieces.
- **Research notes:** Excellent reference for offline-first device-to-device workflows and for projects that need a simple LAN transfer/control plane without external infrastructure.

### scrcpy

- **Repository:** https://github.com/Genymobile/scrcpy
- **Author / Org:** Genymobile / Romain Vimont
- **Category:** Android / device control / screen mirroring / USB / media streaming
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29
- **What it does:** Mirrors and controls Android devices from Linux, Windows, or macOS over USB or TCP/IP without root or a permanently installed Android app. It supports video/audio forwarding, recording, virtual displays, camera capture, HID input, OTG mode, gamepads, and V4L2 webcam output.
- **Why it is valuable:** Highly developed native Android interoperability architecture with low-latency streaming and a clean temporary server/client model. Its developer documentation exposes concrete reusable patterns rather than only end-user features.
- **Useful code/components:** temporary Android `app_process` server; ADB reverse/forward tunnel setup; separate video/audio/control sockets; MediaCodec screen and audio encoders; SDL/FFmpeg host pipeline; demux/decoder/recorder flow; bidirectional clipboard/control protocol; Android hidden-API wrappers; UHID/OTG input handling; V4L2 sink.
- **Install / runtime:** Official binaries/packages for Linux, Windows, and macOS; Android target requires API 21+ for core mirroring and USB debugging for normal control, with OTG mode available for some control without USB debugging.
- **Platforms:** Android target; Linux, Windows, and macOS hosts.
- **License:** Apache-2.0.
- **Maintenance signals:** Version 4.1 released in July 2026 with dependency upgrades and current documentation; repository remains active and unarchived.
- **Verification performed:** Inspected README, developer architecture documentation, root Apache-2.0 LICENSE, and recent commit history. No device mirroring/control session executed by GitHub Gold.
- **Source discovery:** Independent Android interoperability pass.
- **Related projects:** ADB/platform-tools; SDL; FFmpeg; community frontends and integrations.
- **Caveats / risks:** The internal client/server protocol is explicitly version-coupled and may change; Android hidden APIs vary by OS version. Review dependency licenses when extracting host-side pieces.
- **Research notes:** One of the strongest architecture-study candidates in the catalog for Android host/device communication, low-latency streaming, and temporary on-device services.

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
