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
- **Why it is valuable:** Mature multi-platform firmware with active development, build/flashing instructions, tests/CI signals, and support for ESP32, nRF52, RP2040/RP2350, and Linux-class targets.
- **Useful code/components:** mesh routing; LoRa transport; position modules; packet handling; node database; telemetry; Wi-Fi/HTTP/TLS support; hardware variants.
- **Install / runtime:** Build from source or flash supported hardware with official Meshtastic tooling.
- **Platforms:** ESP32, nRF52, RP2040/RP2350, Linux.
- **License:** GPL-3.0.
- **Maintenance signals:** Multiple commits observed on 2026-08-18/19 fixing routing, position-channel behavior, device builds, and TLS memory recovery; README exposes CI status.
- **Verification performed:** README, license, and recent commit history inspected. Not hardware-tested by GitHub Gold.
- **Source discovery:** GitHub-first discovery.
- **Related projects:** meshtastic/Meshtastic-Android; meshtastic/python; meshtastic/web; meshtastic/protobufs; ShakataGaNai/awesome-meshtastic.
- **Caveats / risks:** GPL-3.0 copyleft obligations apply to covered reused code. Radio operation must comply with local rules.
- **Research notes:** Strong candidate for deeper component-level study rather than wholesale duplication.

### OUI-SPY Unified Blue

- **Repository:** https://github.com/colonelpanichacks/oui-spy-unified-blue
- **Author / Org:** colonelpanichacks
- **Category:** ESP32-S3 / passive radio observation / BLE / Wi-Fi / PCAP / drone Remote ID
- **Evidence:** PROMISING
- **Tier / Score:** A / 24
- **What it does:** Multi-mode firmware for the Seeed Studio XIAO ESP32-S3. Its README documents BLE target detection, RSSI foxhunting, passive Wi-Fi observation, Wi-Fi PCAP, Remote ID monitoring, and passive BLE advertising capture.
- **Why it is valuable:** Combines several reusable embedded-radio ideas behind one small device and exposes browser flashing, dashboards, USB-CDC command protocols, packet capture, persistence, and modular firmware selection.
- **Useful code/components:** boot selector; BLE signature matching; RSSI proximity feedback; Wi-Fi promiscuous capture; PCAP streaming; Wireshark helpers; Open Drone ID parsing; USB-CDC protocol; SPIFFS persistence; browser flasher.
- **Install / runtime:** Browser flashing plus Python/esptool flashing are documented upstream.
- **Platforms:** Seeed Studio XIAO ESP32-S3 plus desktop/browser companion tooling.
- **License:** UNKNOWN — no root LICENSE found during inspection.
- **Maintenance signals:** Active commits observed on 2026-08-18, including BLE SNIFF fixes and flasher updates.
- **Verification performed:** README and recent history inspected; root LICENSE lookup returned 404. No hardware test performed.
- **Source discovery:** GitHub-first discovery.
- **Related projects:** colonelpanichacks/flock-you; colonelpanichacks/ouispy-pcap; colonelpanichacks/ouispy-blesniff; colonelpanichacks/Oui-Spy-UniPwn.
- **Caveats / risks:** Do not copy or redistribute source into GitHub Gold until licensing/permission is established. Cataloged for defensive, interoperability, research, and situational-awareness use.
- **Research notes:** High-priority component map once license status is resolved.

### Termux Tools

- **Repository:** https://github.com/termux/termux-tools
- **Author / Org:** Termux
- **Category:** Android / Termux / shell utilities / package infrastructure
- **Evidence:** VERIFIED
- **Tier / Score:** A / 25
- **What it does:** Official scripts and small programs shipped in Termux's core `termux-tools` package.
- **Why it is valuable:** Upstream infrastructure and a strong reference for Android shell patterns, package tooling, mirror selection, environment setup, and compact utilities.
- **Useful code/components:** `scripts/`; `src/`; mirror selection infrastructure; properties initialization; login/environment helpers.
- **Install / runtime:** Distributed through Termux package infrastructure; source includes build files.
- **Platforms:** Android / Termux.
- **License:** GPL-3.0.
- **Maintenance signals:** Official Termux organization with active repository/issue surface.
- **Verification performed:** Official README and COPYING inspected. No Android execution performed by GitHub Gold.
- **Source discovery:** Termux ecosystem pass.
- **Related projects:** termux/termux-app; termux/termux-packages; termux/termux-api.
- **Caveats / risks:** GPL obligations apply to covered copied/modified code.
- **Research notes:** High-value source for future mapping of small battle-tested Android utilities.

### termux-adb

- **Repository:** https://github.com/nohajc/termux-adb
- **Author / Org:** nohajc
- **Category:** Android / Termux / ADB / Fastboot / USB interoperability
- **Evidence:** VERIFIED
- **Tier / Score:** A / 23
- **What it does:** Patches ADB and Fastboot so one Android device can debug another over USB from Termux without root using user-approved USB file descriptors.
- **Why it is valuable:** Demonstrates a reusable interoperability pattern combining Android USB permission APIs with Unix-domain-socket file-descriptor passing.
- **Useful code/components:** `termux-usb` integration; USB FD bridging; Unix-socket FD transfer; patched ADB/Fastboot enumeration; package adaptations.
- **Install / runtime:** Requires Termux and Termux:API; upstream provides an install flow and apt repository.
- **Platforms:** Android / Termux.
- **License:** MIT at repository root; upstream Android tools/submodules have separate licenses.
- **Maintenance signals:** Substantial history and documented limitations.
- **Verification performed:** README and root MIT license inspected. No device-to-device ADB test performed.
- **Source discovery:** Termux ecosystem pass.
- **Related projects:** termux/termux-api; termux/termux-packages; Android platform-tools.
- **Caveats / risks:** Inspect remote install scripts before execution. Review component licenses before extraction.
- **Research notes:** Strong architecture reference for non-root Android USB FD bridging.

### ESP32-S3 Remote ID Add-on (`esp-remoteid`)

- **Repository:** https://github.com/peinser/esp-remoteid
- **Author / Org:** Peinser BV / peinser
- **Category:** ESP32-S3 / OpenDroneID / embedded firmware / interoperability
- **Evidence:** PROMISING
- **Tier / Score:** A / 24
- **What it does:** ESP-IDF firmware for standards-based OpenDroneID / ASTM F3411 Remote ID broadcast over BLE and Wi-Fi with MAVLink input.
- **Why it is valuable:** Well-documented standards implementation built around `opendroneid-core-c`, with explicit transport behavior and flight-controller integration paths.
- **Useful code/components:** OpenDroneID state/transport integration; BLE advertisements; Wi-Fi beacon/NAN transport; Kconfig; MAVLink ingestion; readiness gating; indicators.
- **Install / runtime:** ESP-IDF environment with recursive submodules; build/flash/monitor workflow documented upstream.
- **Platforms:** ESP32-S3.
- **License:** Apache-2.0 at root; dependency licenses must also be preserved.
- **Maintenance signals:** Current 2026 project with extensive documentation and active TODOs.
- **Verification performed:** README and root license inspected. No firmware build or RF hardware test performed.
- **Source discovery:** OpenDroneID ecosystem branch.
- **Related projects:** opendroneid/opendroneid-core-c; opendroneid/receiver-android; ArduPilot/ArduRemoteID.
- **Caveats / risks:** Regulatory compliance depends on jurisdiction and configuration.
- **Research notes:** Good candidate for deeper source-level study after dependency-license review.

### OpenDroneID Core C

- **Repository:** https://github.com/opendroneid/opendroneid-core-c
- **Author / Org:** OpenDroneID
- **Category:** C library / Remote ID / protocol encoding / embedded interoperability
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Core C library for packing and unpacking Open Drone ID messages defined by ASTM F3411 and ASD-STAN specifications, with MAVLink conversion and Wi-Fi reference code.
- **Why it is valuable:** Standards-focused, portable core with compact APIs, tests, memory-reduction options, adapters, and reference broadcast code.
- **Useful code/components:** `libopendroneid`; Basic ID/Location/Auth/Self ID/System/Operator ID encoders and decoders; `libmav2odid`; Wi-Fi reference code; unit tests; low-memory compile options.
- **Install / runtime:** CMake build on Linux; upstream documents sample and test builds.
- **Platforms:** Portable C / Linux / embedded downstream integrations.
- **License:** Apache-2.0.
- **Maintenance signals:** August 2026 protocol-validation/documentation work; README documents CI and tests.
- **Verification performed:** README, license, public API, build/test docs, and recent history inspected. Tests not executed by GitHub Gold.
- **Source discovery:** OpenDroneID ecosystem follow-up.
- **Related projects:** opendroneid/receiver-android; opendroneid/wireshark-dissector; opendroneid/transmitter-linux; ArduPilot/ArduRemoteID; peinser/esp-remoteid.
- **Caveats / risks:** Standards and jurisdictional requirements can change.
- **Research notes:** Strong component-level Gold; prefer standards-core reuse with required notices over reimplementation.

### LocalSend

- **Repository:** https://github.com/localsend/localsend
- **Author / Org:** LocalSend
- **Category:** local-first / offline file transfer / cross-platform / privacy
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Cross-platform LAN file/message transfer without cloud infrastructure or internet access.
- **Why it is valuable:** Mature serverless local workflow spanning Android, iOS, macOS, Windows, Linux, and Fire OS with a documented protocol.
- **Useful code/components:** peer discovery; HTTPS certificate generation; REST transfer flow; file/message transfer; portable configuration; packaging; companion protocol spec.
- **Install / runtime:** Distributed through major package channels; source build uses Flutter/Rust and platform tooling.
- **Platforms:** Android, iOS, macOS, Windows, Linux, Fire OS.
- **License:** Apache-2.0.
- **Maintenance signals:** Same-day activity observed 2026-08-19; release 1.18.2 observed 2026-08-17.
- **Verification performed:** README, license, build docs, protocol description, and recent history inspected. No transfer test performed by GitHub Gold.
- **Source discovery:** Local-first/offline software pass.
- **Related projects:** localsend/protocol; localsend/web; community protocol implementations.
- **Caveats / risks:** LAN firewall/router/AP isolation can affect discovery and transfer.
- **Research notes:** Excellent reference for offline-first device-to-device control and transfer planes.

### scrcpy

- **Repository:** https://github.com/Genymobile/scrcpy
- **Author / Org:** Genymobile / Romain Vimont
- **Category:** Android / device control / screen mirroring / USB / media streaming
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29
- **What it does:** Mirrors and controls Android devices from desktop hosts over USB or TCP/IP without root or a permanently installed Android app.
- **Why it is valuable:** Highly developed native Android interoperability architecture with low-latency streaming and a temporary server/client model.
- **Useful code/components:** temporary `app_process` server; ADB tunnels; video/audio/control sockets; MediaCodec; SDL/FFmpeg host pipeline; control/clipboard protocol; hidden-API wrappers; UHID/OTG; V4L2 sink.
- **Install / runtime:** Official binaries/packages on Linux, Windows, and macOS; normal control uses USB debugging.
- **Platforms:** Android target; Linux, Windows, macOS hosts.
- **License:** Apache-2.0.
- **Maintenance signals:** Version 4.1 released July 2026; active and unarchived.
- **Verification performed:** README, developer architecture docs, license, and recent history inspected. No mirroring session executed by GitHub Gold.
- **Source discovery:** Android interoperability pass.
- **Related projects:** ADB/platform-tools; SDL; FFmpeg.
- **Caveats / risks:** Internal protocol is version-coupled; hidden APIs vary across Android versions.
- **Research notes:** One of the strongest Android host/device architecture references in the catalog.

### ZIM Tools

- **Repository:** https://github.com/openzim/zim-tools
- **Author / Org:** openZIM
- **Category:** offline knowledge / archival / ZIM / CLI tools / content packaging
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **What it does:** Provides command-line tooling for creating, validating, inspecting, extracting, and splitting ZIM offline-content archives used by the Kiwix/openZIM ecosystem.
- **Why it is valuable:** It is infrastructure for turning web-style content into portable offline archives and validating those archives rather than merely a reader application.
- **Useful code/components:** `zimcheck` validation; `zimdump` inspection/extraction; `zimsplit` chunking; `zimwriterfs` HTML-directory-to-ZIM packaging; Meson build; automated tests; official container image.
- **Install / runtime:** Meson/Ninja build with libzim and documented dependencies; official container image also available.
- **Platforms:** Linux and other supported Unix-like build environments; containerized deployment.
- **License:** GPL-3.0-or-later.
- **Maintenance signals:** Version 3.8.0 release merged 2026-08-13; additional code modernization merged 2026-08-15; README exposes CI/codecov/release signals.
- **Verification performed:** README, build/test instructions, license declaration, and recent release/commit history inspected. GitHub Gold did not execute the tools.
- **Source discovery:** Independent offline-knowledge/archival pass.
- **Related projects:** openzim/libzim; Kiwix readers; kiwix/kiwix-android; kiwix/kiwix-desktop; kiwix/kiwix-js.
- **Caveats / risks:** GPL copyleft obligations apply to covered reused code; `zimwriterfs` has multiple third-party dependencies that require separate license review.
- **Research notes:** High-value foundation for portable offline libraries, disaster/off-grid reference collections, and archival pipelines.

### ntfy

- **Repository:** https://github.com/binwiederhier/ntfy
- **Author / Org:** Philipp C. Heckel / binwiederhier
- **Category:** self-hosting / notifications / HTTP API / pub-sub / automation
- **Evidence:** VERIFIED
- **Tier / Score:** S / 27
- **What it does:** Simple HTTP-based publish/subscribe notification service that accepts PUT/POST messages and can be self-hosted, with web and mobile clients in the ecosystem.
- **Why it is valuable:** Extremely composable automation primitive: shell scripts, CI jobs, servers, sensors, and personal tools can publish notifications through a minimal HTTP interface without building a custom push stack.
- **Useful code/components:** HTTP PUT/POST publish API; topic pub-sub model; self-hosted server; CLI/automation integrations; web client; Docker/release build machinery.
- **Install / runtime:** Self-hosted server packages/containers or the hosted service; Android/iOS clients are maintained in related repositories.
- **Platforms:** Linux/server, Docker, web; mobile clients via related repositories.
- **License:** Root `LICENSE` is Apache-2.0; repository also contains a secondary GPLv2 license file, so component-level licensing must be checked before code extraction.
- **Maintenance signals:** Recent commits observed through 2026-08-04; README exposes release, tests, Go report, and coverage signals.
- **Verification performed:** README, root license, repository root, and recent commit history inspected. No server/client session executed by GitHub Gold.
- **Source discovery:** Independent self-hosting/automation pass.
- **Related projects:** binwiederhier/ntfy-android; binwiederhier/ntfy-ios; community integrations.
- **Caveats / risks:** Authentication, topic privacy, TLS, and internet exposure must be configured appropriately when self-hosting. Review the secondary license and component notices before copying code.
- **Research notes:** Strong candidate for alerting/automation glue in user-controlled systems because the publish surface is intentionally small.

### OpenObserve

- **Repository:** https://github.com/openobserve/openobserve
- **Author / Org:** OpenObserve
- **Category:** observability / logs / metrics / traces / OpenTelemetry / self-hosting
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29
- **What it does:** Rust-based observability platform unifying logs, metrics, traces, dashboards, alerts, pipelines, real-user monitoring, and related analytics with OpenTelemetry ingestion.
- **Why it is valuable:** Demonstrates a modern self-hostable observability architecture around a single binary, columnar Parquet storage, object-store/S3 design, SQL/PromQL querying, and multi-signal workflows.
- **Useful code/components:** single-binary Rust server; OpenTelemetry ingestion; Parquet storage; S3-native persistence architecture; SQL/PromQL paths; logs/metrics/traces UI; alerting; pipelines/stream processing; multi-tenancy.
- **Install / runtime:** Upstream documents a single Docker command for local startup plus HA/cloud-native deployment paths.
- **Platforms:** Linux, Docker, Kubernetes/cloud-native environments.
- **License:** AGPL-3.0.
- **Maintenance signals:** Heavy same-day activity observed on 2026-08-19, including search/queue fixes, compactor fixes, CI work, and test changes; upstream commit messages include specific build/test validation evidence.
- **Verification performed:** README, root AGPL-3.0 license, and same-day commit history inspected. GitHub Gold did not deploy or benchmark it; performance/cost claims in upstream README remain upstream claims, not independent verification.
- **Source discovery:** Independent observability pass.
- **Related projects:** OpenTelemetry ecosystem; Parquet/object-storage tooling; OpenObserve deployment integrations.
- **Caveats / risks:** AGPL-3.0 has network-use source-sharing implications for modified covered software; do not casually vendor code into differently licensed projects. Some enterprise features are separate from the open-source edition.
- **Research notes:** Excellent architecture-study candidate; particularly valuable for self-hosted telemetry ingestion, object-store design, and unified signal pipelines.

### Syncthing

- **Repository:** https://github.com/syncthing/syncthing
- **Author / Org:** Syncthing
- **Category:** local-first / continuous synchronization / peer-to-peer / data replication
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29
- **What it does:** Continuously synchronizes folders between two or more computers while prioritizing data safety, security, automation, and user control.
- **Why it is valuable:** Mature decentralized replication architecture with a documented wire protocol, automatic device discovery, relay infrastructure, conflict handling, signed releases, and straightforward source builds.
- **Useful code/components:** Block Exchange Protocol; folder reconciliation; device discovery; relaying; conflict handling; filesystem watcher integration; versioning; signed automatic upgrades; API/web GUI.
- **Install / runtime:** Native releases, packages, or Docker; source builds with `go run build.go`.
- **Platforms:** Linux, Windows, macOS, BSD and other supported Go targets.
- **License:** MPL-2.0.
- **Maintenance signals:** Same-day commit observed 2026-08-19 updating the Go toolchain, plus 2026-08-18 discovery-server/infrastructure fixes and Docker-signing work.
- **Verification performed:** README, license declaration, build instructions, signed-release notes, and recent commits inspected. No live synchronization test performed by GitHub Gold.
- **Source discovery:** Independent resilient-data/local-first pass.
- **Related projects:** syncthing/docs; GUI wrappers; discovery and relay infrastructure.
- **Caveats / risks:** MPL-2.0 is file-level copyleft; modifications to covered files require license compliance. Operational deployments should review discovery/relay exposure and versioning behavior.
- **Research notes:** Excellent complement to LocalSend: continuous state replication rather than ad-hoc transfer.

### rclone

- **Repository:** https://github.com/rclone/rclone
- **Author / Org:** rclone
- **Category:** data movement / cloud storage / synchronization / filesystem abstraction
- **Evidence:** VERIFIED
- **Tier / Score:** S / 27
- **What it does:** A cross-platform command-line data-movement engine supporting a very large set of cloud, object-storage, network, and local backends plus virtual backends layered on top of them.
- **Why it is valuable:** The backend abstraction is unusually reusable: one command surface spans S3, WebDAV, SFTP, SMB, cloud drives, object stores, local filesystems, encryption, chunking, unions, FUSE mounts, and serving protocols.
- **Useful code/components:** storage-backend interface; `copy`, `sync`, `bisync`, and `check`; Crypt; Chunker; Union/Combine; FUSE mount; hash verification; HTTP/WebDAV/FTP/SFTP/DLNA serving; remote-control API and GUI.
- **Install / runtime:** Native binaries/packages, Docker, or source builds; broad Go-supported platform coverage.
- **Platforms:** Linux, Windows, macOS, BSD and other Go targets.
- **License:** MIT.
- **Maintenance signals:** Same-day activity observed 2026-08-19 and 2026-08-18, including GUI maintenance, transform fixes, and security-advisory documentation.
- **Verification performed:** README, MIT license declaration, CI/build signals, recent commits, and security-advisory documentation inspected. GitHub Gold did not execute transfers.
- **Source discovery:** Independent resilient-data/data-movement pass.
- **Related projects:** restic (rclone backend integration); cloud/object-store ecosystems; FUSE.
- **Caveats / risks:** Recent v1.75.0 advisories document multiple assigned CVEs involving `serve restic` path traversal, proxy CONNECT memory exhaustion, FTP/SFTP command injection, and local filename handling. Use patched releases and review exposed serving/backend features.
- **Research notes:** Gold is primarily the backend abstraction and composable virtual-filesystem layers, not merely the CLI surface.

### restic

- **Repository:** https://github.com/restic/restic
- **Author / Org:** restic
- **Category:** backup / encrypted storage / deduplication / snapshots / data integrity
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29
- **What it does:** Fast, efficient, encrypted backup software designed around verifiability, untrusted storage backends, deduplication, snapshots, restore, and reproducible builds.
- **Why it is valuable:** Provides a compact reference architecture for secure content-addressed backup repositories, incremental snapshots, repository verification, and portable storage-backend integration.
- **Useful code/components:** encrypted repository format; deduplication; snapshots; restore; FUSE browsing; repository verification; SFTP/REST/S3/B2/Azure/GCS backends; rclone integration; reproducible build pipeline.
- **Install / runtime:** Native binaries/packages across major desktop/server OSes; documented CLI workflow and backend setup.
- **Platforms:** Linux, Windows, macOS, FreeBSD, OpenBSD.
- **License:** BSD-2-Clause.
- **Maintenance signals:** Dependency and CI maintenance observed through 2026-08-01; README exposes active test workflow and reproducible-build documentation.
- **Verification performed:** README, license declaration, backend list, design principles, reproducible-build notes, and recent maintenance commits inspected. No backup/restore cycle executed by GitHub Gold.
- **Source discovery:** Independent resilient-data/backup pass.
- **Related projects:** restic/rest-server; restic/builder; rclone; S3-compatible storage systems.
- **Caveats / risks:** Password loss makes encrypted repositories unrecoverable by design; backup quality depends on actually testing restores and repository checks.
- **Research notes:** Particularly strong for studying integrity-first encrypted backup architecture and deduplicated snapshot design.

## Rejected / Deferred Leads

- **PeterJBurke/esp32-c3-remote-id:** deferred because its own README explicitly states it is broken after an ESP development-stack upgrade and may be deleted. Keep as historical lead only; do not promote as working Gold.
- **colonelpanichacks/Remote-ID-Spoofer:** not promoted. Its primary purpose is Remote ID spoofing, outside this catalog's preferred defensive/interoperability scope.

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