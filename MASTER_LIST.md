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
- **Tier / Score:** A / 25 (Utility 5, Working Evidence 4, Reusability 5, Novelty 3, Documentation 4, Maintenance 4)
- **What it does:** Official scripts and small programs shipped in Termux's core `termux-tools` package.
- **Why it is valuable:** Upstream infrastructure and a strong reference for Android shell patterns, package tooling, mirror selection, environment setup, and compact utilities.
- **Useful code/components:** `scripts/pkg.in`, `scripts/termux-change-repo.in`, `scripts/termux-backup.in`, `scripts/termux-restore.in`, `scripts/termux-fix-shebang.in`, `src/cmd.c`, `mirrors/`
- **Install / runtime:** Distributed through Termux package infrastructure; source includes build files.
- **Platforms:** Android / Termux.
- **License:** GPL-3.0.
- **Maintenance signals:** Stable v1.48.0 released 2025-11-29; latest inspected master commit 05c857ee (2026-10-16) adds South American mirror. Upstream build CI 38838597990 passed its single Autotools build/install job (2026-10-16); mirror-update workflow success is not software test evidence.
- **Verification performed:** 2026-10-21 inspected README, COPYING, scripts/pkg.in, scripts/termux-change-repo.in, source layout, release, commit and CI workflow; no independent Android device testing.
- **Source discovery:** Termux ecosystem pass.
- **Related projects:** termux/termux-app; termux/termux-packages; termux/termux-api.
- **Caveats / risks:** GPL-3.0 obligations apply to copied code; Linux CI build does not verify Android runtime.
- **Research notes:** See `research/2026-10-21-termux-esptool-reticulum-maintenance.md` for source evidence and verification boundaries.

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
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 4, Maintenance 4)
- **What it does:** Core C library for packing and unpacking Open Drone ID messages defined by ASTM F3411 and ASD-STAN specifications, with MAVLink conversion and Wi-Fi reference code.
- **Why it is valuable:** Standards-focused, portable core with compact APIs, tests, memory-reduction options, adapters, and reference broadcast code.
- **Useful code/components:** `libopendroneid`; Basic ID/Location/Auth/Self ID/System/Operator ID encoders and decoders; `libmav2odid`; Wi-Fi reference code; unit tests; low-memory compile options.
- **Install / runtime:** CMake build on Linux; upstream documents sample and test builds.
- **Platforms:** Portable C / Linux / embedded downstream integrations.
- **License:** Apache-2.0.
- **Maintenance signals:** v2.0 (2022-04-06); master CMake 37671876169 succeeded 1/1 job (2026-10-07). 2026-10-07 master merged a MAVLink Basic ID cycling index fix with regression test; newer than the latest tagged release.
- **Verification performed:** 2026-10-21 inspected README, license, source/build layout, release metadata and upstream CI. Do not assume master fixes are in v2.0; no independent packet, hardware or regulatory-conformance test.
- **Source discovery:** OpenDroneID ecosystem follow-up.
- **Related projects:** opendroneid/receiver-android; opendroneid/wireshark-dissector; opendroneid/transmitter-linux; ArduPilot/ArduRemoteID; peinser/esp-remoteid.
- **Caveats / risks:** Standards and jurisdictional requirements can change.
- **Research notes:** research/2026-10-21-rclone-opendroneid-zim-tools-maintenance.md. Do not assume master fixes are in v2.0; no independent packet, hardware or regulatory-conformance test.

### LocalSend

- **Repository:** https://github.com/localsend/localsend
- **Author / Org:** LocalSend
- **Category:** local-first / offline file transfer / cross-platform / privacy
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Cross-platform LAN file/message transfer without cloud infrastructure or internet access.
- **Why it is valuable:** Mature serverless local workflow spanning Android, iOS, macOS, Windows, Linux, and Fire OS with a documented protocol.
- **Useful code/components:** peer discovery; HTTPS certificate generation; REST transfer flow; file/message transfer; portable configuration; packaging; companion protocol spec.
- **Install / runtime:** Distributed through major package channels; source build uses Flutter/Rust and platform tooling.
- **Platforms:** Android, iOS, macOS, Windows, Linux, Fire OS.
- **License:** Apache-2.0.
- **Maintenance signals:** Stable v1.18.2 published 2026-08-21 (correcting earlier 2026-08-17 date); main-branch CI 38703786899 passed all four jobs on 2026-10-15 (test, packaging, rust, format).
- **Verification performed:** README, Apache-2.0 license, Flutter/Rust project trees, network providers, release assets and upstream CI inspected 2026-10-20. Upstream v1.17.0 notes a path-traversal fix; v1.18.2 includes compatibility/security fixes. No transfer test or independent security audit performed.
- **Source discovery:** Local-first/offline software pass.
- **Related projects:** localsend/protocol; localsend/web; community protocol implementations.
- **Caveats / risks:** LAN firewall/router/AP isolation can affect discovery and transfer.
- **Research notes:** Excellent reference for offline-first device-to-device control and transfer planes.

### scrcpy

- **Repository:** https://github.com/Genymobile/scrcpy
- **Author / Org:** Genymobile / Romain Vimont
- **Category:** Android / device control / screen mirroring / USB / media streaming
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 4)
- **What it does:** Mirrors and controls Android devices from desktop hosts over USB or TCP/IP without root or a permanently installed Android app.
- **Why it is valuable:** Highly developed native Android interoperability architecture with low-latency streaming and a temporary server/client model.
- **Useful code/components:** `server/` temporary Android app_process server; `app/` desktop client; ADB tunnels; video/audio/control sockets; MediaCodec capture/encoding; SDL/FFmpeg rendering and v5 GPU decoding; clipboard/control protocol; hidden API wrappers; UHID/OTG; V4L2.
- **Install / runtime:** Official binaries/packages on Linux, Windows, and macOS; normal control uses USB debugging.
- **Platforms:** Android target; Linux, Windows, macOS hosts.
- **License:** Apache-2.0.
- **Maintenance signals:** Stable v5.0.1 published 2026-10-08 (supersedes July v4.1); fixes VA-API/GPU selection, NVIDIA chroma-plane compatibility, Windows H.265 decoding and EGL handling. Release CI 37737030700: all 17 jobs succeeded, including server/client tests and cross-platform builds/packages.
- **Verification performed:** README, Apache-2.0 LICENSE, release notes, source layout and CI job conclusions inspected 2026-10-21. Upstream CI only; no independent build, device connection, screen mirroring or GPU test.
- **Source discovery:** Android interoperability pass.
- **Related projects:** ADB/platform-tools; SDL; FFmpeg.
- **Caveats / risks:** Internal protocol is version-coupled; hidden APIs vary across Android versions.
- **Research notes:** `research/2026-10-21-scrcpy-syncthing-ntfy-maintenance.md`. Hardware decoding varies by GPU/driver; server/client protocol is version-coupled.

### ZIM Tools

- **Repository:** https://github.com/openzim/zim-tools
- **Author / Org:** openZIM
- **Category:** offline knowledge / archival / ZIM / CLI tools / content packaging
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Provides command-line tooling for creating, validating, inspecting, extracting, and splitting ZIM offline-content archives used by the Kiwix/openZIM ecosystem.
- **Why it is valuable:** It is infrastructure for turning web-style content into portable offline archives and validating those archives rather than merely a reader application.
- **Useful code/components:** `zimcheck` validation; `zimdump` inspection/extraction; `zimsplit` chunking; `zimwriterfs` HTML-directory-to-ZIM packaging; Meson build; automated tests; official container image.
- **Install / runtime:** Meson/Ninja build with libzim and documented dependencies; official container image also available.
- **Platforms:** Linux and other supported Unix-like build environments; containerized deployment.
- **License:** GPL-3.0-or-later.
- **Maintenance signals:** 3.8.0 (2026-08-13); main CI 39216346633 succeeded 5/5 cross-platform jobs (2026-10-19). Version 3.8.0 improved zimcheck link/metadata validation, zimsplit sizing and zimwriterfs URL parsing.
- **Verification performed:** 2026-10-21 inspected README, license, source/build layout, release metadata and upstream CI. GPL-3.0-or-later and third-party dependencies need license review; no independent archive build/validation.
- **Source discovery:** Independent offline-knowledge/archival pass.
- **Related projects:** openzim/libzim; Kiwix readers; kiwix/kiwix-android; kiwix/kiwix-desktop; kiwix/kiwix-js.
- **Caveats / risks:** GPL copyleft obligations apply to covered reused code; `zimwriterfs` has multiple third-party dependencies that require separate license review.
- **Research notes:** research/2026-10-21-rclone-opendroneid-zim-tools-maintenance.md. GPL-3.0-or-later and third-party dependencies need license review; no independent archive build/validation.

### ntfy

- **Repository:** https://github.com/binwiederhier/ntfy
- **Author / Org:** Philipp C. Heckel / binwiederhier
- **Category:** self-hosting / notifications / HTTP API / pub-sub / automation
- **Evidence:** VERIFIED
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Simple HTTP-based publish/subscribe notification service that accepts PUT/POST messages and can be self-hosted, with web and mobile clients in the ecosystem.
- **Why it is valuable:** Extremely composable automation primitive: shell scripts, CI jobs, servers, sensors, and personal tools can publish notifications through a minimal HTTP interface without building a custom push stack.
- **Useful code/components:** `server/` HTTP publish/subscription; `server/server_auth.go` authorization; `server/server_cluster.go` experimental cluster; `server/server_webpush.go` Web Push; `client/`; `db/`; `web/`; topic handlers and server test suite; minimal PUT/POST pub-sub API.
- **Install / runtime:** Self-hosted server packages/containers or the hosted service; Android/iOS clients are maintained in related repositories.
- **Platforms:** Linux/server, Docker, web; mobile clients via related repositories.
- **License:** Root `LICENSE` is Apache-2.0; repository also contains a secondary GPLv2 license file, so component-level licensing must be checked before code extraction.
- **Maintenance signals:** Stable v2.32.0 published 2026-10-18; RFC 10036 `Incremental: ?1` header for streaming subscribers, experimental passive-cluster housekeeping and database-version guards. Main-branch test workflow 39182637748 passed 2026-10-19; clustering remains experimental.
- **Verification performed:** README, Apache-2.0 LICENSE, secondary LICENSE.GPLv2, server/test tree, release notes and upstream main-branch test job inspected 2026-10-21. No independent deployment, streaming, or failover test.
- **Source discovery:** Independent self-hosting/automation pass.
- **Related projects:** binwiederhier/ntfy-android; binwiederhier/ntfy-ios; community integrations.
- **Caveats / risks:** Authentication, topic privacy, TLS, and internet exposure must be configured appropriately when self-hosting. Review the secondary license and component notices before copying code.
- **Research notes:** `research/2026-10-21-scrcpy-syncthing-ntfy-maintenance.md`. Review component licensing and streaming reverse-proxy buffering; experimental clustering not production-verified.

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
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 4)
- **What it does:** Continuously synchronizes folders between two or more computers while prioritizing data safety, security, automation, and user control.
- **Why it is valuable:** Mature decentralized replication architecture with a documented wire protocol, automatic device discovery, relay infrastructure, conflict handling, signed releases, and straightforward source builds.
- **Useful code/components:** `lib/protocol/` Block Exchange Protocol; `lib/model/` reconciliation; `lib/discover/` discovery; `lib/relay/` relay; `lib/scanner/` block scanner; `lib/versioner/` versioning; `lib/api/` REST API; `lib/fs/` filesystem abstraction; conflict and watcher integrations.
- **Install / runtime:** Native releases, packages, or Docker; source builds with `go run build.go`.
- **Platforms:** Linux, Windows, macOS, BSD and other supported Go targets.
- **License:** MPL-2.0.
- **Maintenance signals:** Stable v2.1.7 published 2026-10-21 with receive-only reconciliation, SQLite and malformed-protocol-input fixes plus incoming-message validation. Main-branch CI 39487469482 on 2026-10-20 passed Linux/macOS/Windows build/tests and govulncheck; several lint/signing/release jobs were skipped.
- **Verification performed:** README, MPL-2.0 LICENSE, `lib/` tree, v2.1.7 release notes and main-branch CI job conclusions inspected 2026-10-21. No independent sync, filesystem fault or security test.
- **Source discovery:** Independent resilient-data/local-first pass.
- **Related projects:** syncthing/docs; GUI wrappers; discovery and relay infrastructure.
- **Caveats / risks:** MPL-2.0 is file-level copyleft; modifications to covered files require license compliance. Operational deployments should review discovery/relay exposure and versioning behavior.
- **Research notes:** `research/2026-10-21-scrcpy-syncthing-ntfy-maintenance.md`. Validate deletion and receive-only semantics for critical data.

### rclone

- **Repository:** https://github.com/rclone/rclone
- **Author / Org:** rclone
- **Category:** data movement / cloud storage / synchronization / filesystem abstraction
- **Evidence:** VERIFIED
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 4, Maintenance 4)
- **What it does:** A cross-platform command-line data-movement engine supporting a very large set of cloud, object-storage, network, and local backends plus virtual backends layered on top of them.
- **Why it is valuable:** The backend abstraction is unusually reusable: one command surface spans S3, WebDAV, SFTP, SMB, cloud drives, object stores, local filesystems, encryption, chunking, unions, FUSE mounts, and serving protocols.
- **Useful code/components:** storage-backend interface; `copy`, `sync`, `bisync`, and `check`; Crypt; Chunker; Union/Combine; FUSE mount; hash verification; HTTP/WebDAV/FTP/SFTP/DLNA serving; remote-control API and GUI.
- **Install / runtime:** Native binaries/packages, Docker, or source builds; broad Go-supported platform coverage.
- **Platforms:** Linux, Windows, macOS, BSD and other Go targets.
- **License:** MIT.
- **Maintenance signals:** v1.75.2 (2026-10-09); master build 39406871189 succeeded 9/9 jobs (2026-10-20). 2026-10-20 master fixes corrected S3 Last-Modified caching and rejected overflowing duration arguments.
- **Verification performed:** 2026-10-21 inspected README, license, source/build layout, release metadata and upstream CI. Review security advisories and patched versions before exposing serving protocols; no transfer or mount test performed.
- **Source discovery:** Independent resilient-data/data-movement pass.
- **Related projects:** restic (rclone backend integration); cloud/object-store ecosystems; FUSE.
- **Caveats / risks:** Recent v1.75.0 advisories document multiple assigned CVEs involving `serve restic` path traversal, proxy CONNECT memory exhaustion, FTP/SFTP command injection, and local filename handling. Use patched releases and review exposed serving/backend features.
- **Research notes:** research/2026-10-21-rclone-opendroneid-zim-tools-maintenance.md. Review security advisories and patched versions before exposing serving protocols; no transfer or mount test performed.

### restic

- **Repository:** https://github.com/restic/restic
- **Author / Org:** restic
- **Category:** backup / encrypted storage / deduplication / snapshots / data integrity
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- **What it does:** Fast, efficient, encrypted backup software designed around verifiability, untrusted storage backends, deduplication, snapshots, restore, and reproducible builds.
- **Why it is valuable:** Provides a compact reference architecture for secure content-addressed backup repositories, incremental snapshots, repository verification, and portable storage-backend integration.
- **Useful code/components:** encrypted repository format; deduplication; snapshots; restore; FUSE browsing; repository verification; SFTP/REST/S3/B2/Azure/GCS backends; rclone integration; reproducible build pipeline.
- **Install / runtime:** Native binaries/packages across major desktop/server OSes; documented CLI workflow and backend setup.
- **Platforms:** Linux, Windows, macOS, FreeBSD, OpenBSD.
- **License:** BSD-2-Clause.
- **Maintenance signals:** Stable v0.19.1 published 2026-07-05; master CI on 2026-10-18 failed in the Swift cloud-backend test because the remote authentication endpoint's TLS certificate expired 2026-10-01. Linux Go 1.26, macOS Go 1.27, cross-compiles, lint and Docker jobs passed; the red aggregate must not be reported as passing.
- **Verification performed:** README, BSD-2-Clause license, internal/repository, internal/archiver, internal/restorer and backend trees, release and failing CI job logs inspected 2026-10-20. Failure appears external to core backup logic but is not resolved. No independent backup/restore or repository integrity test executed.
- **Source discovery:** Independent resilient-data/backup pass.
- **Related projects:** restic/rest-server; restic/builder; rclone; S3-compatible storage systems.
- **Caveats / risks:** Password loss makes encrypted repositories unrecoverable by design; backup quality depends on actually testing restores and repository checks.
- **Research notes:** Particularly strong for studying integrity-first encrypted backup architecture and deduplicated snapshot design.

### Organic Maps

- **Repository:** https://github.com/organicmaps/organicmaps
- **Author / Org:** Organic Maps
- **Category:** offline maps / navigation / OpenStreetMap / privacy / mobile
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 4)
- **What it does:** Privacy-focused offline navigation using downloadable OpenStreetMap-derived maps, routing, search, bookmarks/tracks, and elevation-related data.
- **Why it is valuable:** Strong offline-first architecture spanning map generation, compact local map storage, rendering, routing, geocoding/search, and mobile navigation without a required cloud backend.
- **Useful code/components:** `libs/routing/`, `libs/search/`, `libs/storage/`, `libs/mwm_diff/`, `libs/kml/`, `generator/`, `android/`, `iphone/`
- **Install / runtime:** Native Android/iOS applications with repository build tooling and map-generation infrastructure.
- **Platforms:** Android, iOS, desktop/build tooling.
- **License:** Apache-2.0 for code; binary map/data artifacts use a separate license.
- **Maintenance signals:** Android release 2026.09.29-32-android (2026-09-29); master Android/iOS navigation updates 2026-10-21; main Android Check, Android Beta, iOS Check, CMake and translation workflows succeeded 2026-10-21. One feature-branch Android Check failed; this is not a main-branch failure.
- **Verification performed:** 2026-10-21 upstream release, code tree, license and CI reviewed. Source is Apache-2.0; binary map/data use separate DATA_LICENSE.txt including ODbL/CC BY-SA upstream terms. No on-device navigation, route accuracy, or map-generation test.
- **Source discovery:** Offline/resilient systems pass.
- **Related projects:** OpenStreetMap ecosystem; map-generation and routing tooling.
- **Caveats / risks:** Treat code and generated map/data licensing separately; do not assume Apache-2.0 covers binary map artifacts.
- **Research notes:** `research/2026-10-21-organicmaps-kopia-age-maintenance.md`. Source is Apache-2.0; binary map/data use separate DATA_LICENSE.txt including ODbL/CC BY-SA upstream terms. No on-device navigation, route accuracy, or map-generation test.

### Kopia

- **Repository:** https://github.com/kopia/kopia
- **Author / Org:** Kopia
- **Category:** backup / encrypted snapshots / deduplication / storage abstraction / self-hosting
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Encrypted, compressed, deduplicated snapshot backup system with local, cloud, network, and repository-server modes plus CLI and GUI clients.
- **Why it is valuable:** Combines content-addressed encrypted repositories, multiple storage backends, snapshot policy, error correction, and a server mode in a composable Go codebase.
- **Useful code/components:** `repo/content/`, `repo/blob/`, `repo/encryption/`, `repo/compression/`, `repo/ecc/`, `repo/splitter/`, `snapshot/`, `cli/`, `repo/api_server_repository.go`
- **Install / runtime:** Native binaries/packages and container/server workflows documented upstream.
- **Platforms:** Linux, Windows, macOS and Go/Electron-supported environments.
- **License:** Apache-2.0.
- **Maintenance signals:** v0.23.1 (2026-06-16) fixes a rare epoch-compaction index race that may cause data loss (#5371); upstream recommends upgrade. 2026-10-21 master stress/endurance workflows succeeded. Providers - Core workflow failed: Azure PIT tests got nil version IDs; S3 MinIO integration tests could not pull minio/minio Docker image.
- **Verification performed:** 2026-10-21 upstream release, code tree, license and CI reviewed. Root license Apache-2.0. No independently performed backup/restore or regression test. Provider CI is not all green; check Azure versioning and MinIO test infrastructure.
- **Source discovery:** Offline/resilient systems pass.
- **Related projects:** rclone; cloud/object-storage backends; snapshot/backup ecosystems.
- **Caveats / risks:** Operational confidence requires restore testing and repository verification; dependency/backend behavior varies by deployment.
- **Research notes:** `research/2026-10-21-organicmaps-kopia-age-maintenance.md`. Root license Apache-2.0. No independently performed backup/restore or regression test. Provider CI is not all green; check Azure versioning and MinIO test infrastructure.

### Reticulum Network Stack

- **Repository:** https://github.com/markqvist/Reticulum
- **Author / Org:** markqvist
- **Category:** off-grid networking / delay-tolerant networking / cryptographic routing / heterogeneous transports
- **Evidence:** VERIFIED
- **Tier / Score:** A / 24 (Utility 5, Working Evidence 4, Reusability 3, Novelty 5, Documentation 5, Maintenance 2)
- **What it does:** Networking stack designed to carry encrypted communication across very-low-bandwidth and heterogeneous transports including LoRa/RNode, packet radio, serial links, TCP/UDP/IP, pipes, and custom interfaces.
- **Why it is valuable:** Provides a transport-agnostic path-discovery and cryptographic-routing model for disconnected, intermittent, and unconventional networks rather than assuming conventional internet infrastructure.
- **Useful code/components:** `RNS/Interfaces/` (RNode, KISS, TCP, UDP, serial, backbone), `RNS/Transport.py`, `RNS/Link.py`, `RNS/Identity.py`, `RNS/Channel.py`, `RNS/Buffer.py`, `RNS/Resource.py`, `tests/`, `Examples/`
- **Install / runtime:** Python 3 systems plus supported radio/network interfaces.
- **Platforms:** Python systems, LoRa/RNode, packet radio, serial, TCP/UDP/IP, custom interfaces.
- **License:** Custom Reticulum License; protocol is stated upstream as public domain.
- **Maintenance signals:** Stable 1.5.5 released 2026-09-29; latest inspected master mirror commit e40191b (2026-09-30). Upstream CI 36723645574 passed `make test` (one job); tag-only packaging skipped. `MIRROR.md` says this is a public mirror, development elsewhere, no public support/issue responses and no predictable update schedule; maintenance score lowered.
- **Verification performed:** 2026-10-21 inspected README, custom LICENSE, MIRROR.md, setup.py, interface and test trees, release and CI; no independent live network, radio or cryptographic tests.
- **Source discovery:** Offline/resilient systems pass.
- **Related projects:** LXMF, Sideband, RNode and broader Reticulum ecosystem projects.
- **Caveats / risks:** Custom Reticulum License prohibits harmful systems and AI/ML training datasets; not OSI-standard. Do not copy/adapt without legal review or permission. Public-domain protocol claim does not replace source license; upstream support withdrawn.
- **Research notes:** See `research/2026-10-21-termux-esptool-reticulum-maintenance.md` for source evidence and verification boundaries.

### Espressif esptool

- **Repository:** https://github.com/espressif/esptool
- **Author / Org:** Espressif
- **Category:** embedded tooling / ESP32 / flashing / provisioning / serial protocol
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Official Python tooling for communicating with Espressif ROM bootloaders and flasher stubs to identify chips, read/write/erase flash, inspect images, and perform provisioning-related operations.
- **Why it is valuable:** Mature host-side reference implementation for Espressif serial bootloader protocols and cross-platform flashing workflows.
- **Useful code/components:** `esptool/loader.py`, `esptool/bin_image.py`, `esptool/cmds.py`, `esptool/targets/`, `espefuse/`, `espsecure/`; companion `espressif/esp-flasher-stub`
- **Install / runtime:** Python >=3.10 on Linux/macOS/Windows, pyserial and cryptography dependencies; compatible Espressif device via USB/serial.
- **Platforms:** Python hosts; Espressif SoCs.
- **License:** GPL-2.0-or-later.
- **Maintenance signals:** Stable v5.6.0 released 2026-10-15. Master commit 93477ace (2026-10-20) adds --encrypt-files alignment validation, not necessarily in v5.6.0. Upstream CI 39435542641 passed 7/7 host test/stub-check jobs (Python 3.10-3.15); build CI 39435542027 passed six platform builds, release step skipped.
- **Verification performed:** 2026-10-21 inspected README, LICENSE, pyproject.toml, loader/image source, commits, release and CI; no independent flash, provisioning or runtime test.
- **Source discovery:** Embedded/Android tooling pass.
- **Related projects:** ESP-IDF; Espressif flasher stubs and provisioning tooling.
- **Caveats / risks:** GPL-2.0-or-later; check bundled stub/dependency licenses. Host CI is not hardware validation; eFuse/provisioning can be irreversible.
- **Research notes:** See `research/2026-10-21-termux-esptool-reticulum-maintenance.md` for source evidence and verification boundaries.

### App Manager

- **Repository:** https://github.com/MuntashirAkon/AppManager
- **Author / Org:** MuntashirAkon
- **Category:** Android / package inspection / app management / diagnostics / backup
- **Evidence:** VERIFIED
- **Tier / Score:** S / 27
- **What it does:** Advanced Android package-management and diagnostics suite covering package/component inspection, manifests/signatures, tracker/library scanning, APK bundle workflows, backups, logcat, profiles, files, and terminal functionality.
- **Why it is valuable:** Consolidates many Android package-analysis and device-management capabilities behind explicit privilege layers, making it a useful architecture reference for non-root, ADB-assisted, and root-enhanced workflows.
- **Useful code/components:** package/component inspection; manifest/signature analysis; APK bundle installation; tracker/library scanning; logcat tools; profiles/batch operations; encrypted backup/restore; ADB/root capability layers; file manager; terminal integration.
- **Install / runtime:** Android application with optional ADB/root-enhanced capabilities.
- **Platforms:** Android.
- **License:** REUSE/SPDX model; primary application is documented GPL-3.0-or-later with additional file-level licenses.
- **Maintenance signals:** Recent commits were inspected during the research pass.
- **Verification performed:** README, REUSE/license metadata, and recent commits inspected. No Android execution performed by GitHub Gold.
- **Source discovery:** Embedded/Android tooling pass.
- **Related projects:** Android package manager APIs, ADB, APK analysis and backup ecosystems.
- **Caveats / risks:** Perform file-level SPDX/license review before code reuse; powerful package/device operations should be used only on devices the operator controls.
- **Research notes:** Particularly strong as a map of Android package metadata, privilege abstraction, and diagnostics workflows.

### Caddy

- **Repository:** https://github.com/caddyserver/caddy
- **Author / Org:** CaddyServer
- **Category:** web server / reverse proxy / automatic HTTPS / self-hosting / server platform
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- **What it does:** Modular Go web server and reverse proxy with automatic HTTPS, dynamic configuration, HTTP/1.1/2/3, internal PKI support, and a broad plugin ecosystem.
- **Why it is valuable:** Combines production-grade serving/proxying with an API-driven configuration model and reusable TLS automation, making it a strong self-hosting and infrastructure reference.
- **Useful code/components:** automatic HTTPS; native JSON configuration; dynamic configuration API; config adapters; reverse proxy; HTTP/1.1 HTTP/2 HTTP/3; modular Go app/plugin architecture; local CA; cluster-aware TLS coordination; xcaddy custom builds.
- **Install / runtime:** Native Go binaries/packages and containerized deployments.
- **Platforms:** Linux, Windows, macOS, BSD and other Go-supported systems.
- **License:** Apache-2.0.
- **Maintenance signals:** Stable v2.11.7 (2026-10-03) fixed v2.11.6 HTTP/2 proxy panic and streaming cutoffs. Main commit f355b868 (2026-10-21) improves forward-proxy-wrapped dial retries; not established in stable. Upstream Tests run 39594833694 passed 3 platform jobs (2 optional skipped).
- **Verification performed:** 2026-10-21: README, Apache-2.0 LICENSE, reverseproxy.go, release notes, recent commits and upstream CI jobs inspected; no independent deployment or security testing.
- **Source discovery:** TLS/self-hosting pass.
- **Related projects:** caddyserver/certmagic; xcaddy; config adapters; libdns ecosystem.
- **Caveats / risks:** Review exposed admin/config API and proxy trust boundaries. v2.11.6 had regressions fixed in v2.11.7; main-branch changes are not necessarily released.
- **Research notes:** research/2026-10-21-caddy-certmagic-duckdb-maintenance.md; upstream CI is not independent verification.

### CertMagic

- **Repository:** https://github.com/caddyserver/certmagic
- **Author / Org:** CaddyServer
- **Category:** Go library / TLS automation / ACME / certificate management / reusable infrastructure
- **Evidence:** VERIFIED
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- **What it does:** Go library for automated certificate issuance, renewal, caching, storage, OCSP, ACME challenges, on-demand issuance, and `tls.Config` integration.
- **Why it is valuable:** Extracts Caddy's certificate-management capabilities into a reusable library that can be embedded into other Go applications.
- **Useful code/components:** certificate issuance/renewal; ACME HTTP/TLS-ALPN/DNS challenges; multiple issuers; pluggable storage; distributed challenge locking; certificate cache; OCSP stapling; on-demand issuance controls; retry/backoff; event hooks; `tls.Config` integration; libdns interoperability.
- **Install / runtime:** Go library embedded in Go applications and services.
- **Platforms:** Go-supported systems including Linux, Windows, macOS, BSD, and Android targets where dependencies permit.
- **License:** Apache-2.0.
- **Maintenance signals:** Stable v0.25.6 (2026-09-30) upgraded ZeroSSL dependency for Authorization: ApiKey header. Latest master commit cfd20205 (2026-10-01) fixes README link. Upstream Tests run 36915271739 passed 6/6 Ubuntu/macOS/Windows Go 1.25/1.26 jobs.
- **Verification performed:** 2026-10-21: README, Apache-2.0 LICENSE.txt, certmagic.go, release, recent commits and upstream CI jobs inspected; no independent ACME issuance or TLS audit.
- **Source discovery:** TLS/self-hosting pass.
- **Related projects:** Caddy; libdns providers; ACME issuers; storage backends.
- **Caveats / risks:** ACME issuance depends on CA availability, challenge routing, permissions, storage locks and on-demand controls. Review external DNS/storage provider licenses.
- **Research notes:** research/2026-10-21-caddy-certmagic-duckdb-maintenance.md; upstream CI is not independent verification.

### whisper.cpp

- **Repository:** https://github.com/ggml-org/whisper.cpp
- **Author / Org:** ggml-org
- **Category:** local AI / speech recognition / embedded inference
- **Evidence:** VERIFIED (upstream code, release and CI evidence; not independently executed)
- **Tier / Score:** S / 29 (provisional)
- **What it does:** Local cross-platform speech recognition implementation in C/C++.
- **Why it is valuable:** Embeddable C API and CPU/GPU backends for offline transcription.
- **Useful code/components:** include/whisper.h C API; src/whisper.cpp inference core; CLI and streaming examples; VAD and quantization tooling; Android iOS WASM Java and Docker examples; GPU and accelerator backend integrations; talk-llama speech-to-LLM example.
- **Install / runtime:** Build with CMake; obtain separately licensed model weights; run whisper-cli or link the C API.
- **Platforms:** Linux, Windows, macOS, Android, iOS, WebAssembly.
- **License:** MIT for the inspected root repository; third-party code and assets may differ.
- **Maintenance signals:** Upstream stable release v1.9.5 published 2026-10-06; CI workflows cover multiple platforms.
- **Verification performed:** README, license, upstream release and CI definitions inspected. No independent build, runtime test, or benchmark.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-local-ai-crdt.md
- **Related projects:** ggml-org/ggml and Whisper model ecosystem.
- **Caveats / risks:** MIT source licensing is permissive, but model weights and third-party dependencies/backends may have separate terms.
- **Research notes:** Promoted from READY queue; scoring remains provisional.

### Loro

- **Repository:** https://github.com/loro-dev/loro
- **Author / Org:** loro-dev
- **Category:** local-first / CRDT / collaborative state infrastructure
- **Evidence:** VERIFIED (upstream code, release and CI evidence; not independently executed)
- **Tier / Score:** S / 28 (provisional)
- **What it does:** Conflict-free replicated data types for local-first collaborative application state.
- **Why it is valuable:** Reusable mergeable text, rich-text, tree, list and map structures, with delta synchronization and history.
- **Useful code/components:** Rust CRDT core; JavaScript/WASM loro-crdt package; Swift support; Fugue text and rich-text CRDTs; moveable tree and list CRDTs; delta synchronization APIs; shallow snapshots and time travel; Loro Inspector.
- **Install / runtime:** Use the Rust crates, JavaScript/WASM package, or documented Swift integration.
- **Platforms:** Rust, JavaScript/WebAssembly, Swift.
- **License:** MIT for the inspected root repository; third-party code and assets may differ.
- **Maintenance signals:** Upstream loro-crdt@1.16.4 published 2026-09-30; Rust CI and release workflows present.
- **Verification performed:** README, license, upstream release and CI definitions inspected. No independent build, runtime test, or benchmark.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-local-ai-crdt.md
- **Related projects:** loro-dev ecosystem, local-first applications, CRDT research.
- **Caveats / risks:** Root project is MIT licensed; optional ecosystem repositories and bindings should be checked separately before code reuse.
- **Research notes:** Promoted from READY queue; scoring remains provisional.

### DuckDB

- **Repository:** https://github.com/duckdb/duckdb
- **Author / Org:** duckdb
- **Category:** embedded analytics / SQL / data tooling / columnar processing
- **Evidence:** VERIFIED (upstream implementation, documentation and maintenance evidence; not independently executed)
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 4, Reusability 5, Novelty 5, Documentation 5, Maintenance 4)
- **What it does:** Embeddable analytical SQL database with vectorized execution and local CSV/Parquet processing.
- **Why it is valuable:** Reusable in-process analytics engine and C API for local-first data pipelines and scripts.
- **Useful code/components:** embeddable analytical SQL engine; public version-targeted C API; CSV and Parquet readers; query planner and optimizer; vectorized execution engine; storage and transaction layers; extension architecture; CLI and language-client integration points; unit-test and benchmark infrastructure.
- **Install / runtime:** Use a supported DuckDB CLI, language package, or documented native C/C++ interface; extension compatibility depends on versions.
- **Platforms:** Linux, Windows, macOS, other supported native and language-binding targets.
- **License:** MIT at upstream root; dependencies/extensions require separate review.
- **Maintenance signals:** Stable v2.0.0 (2026-10-21) published 28 assets. Main commit c15a232a (2026-10-21) fixes window-aggregate memory-limit livelock but is not established in v2.0.0. On Tag 39602672912 failed staging download; SwiftRelease 39602672833 failed push; Oct 19 Main 39259831957 passed many core tests but failed parser benchmark and cloud-extension builds.
- **Verification performed:** 2026-10-21: README, MIT LICENSE, generated C API header, v2.0.0 release, recent commit and selected upstream CI jobs inspected; no independent build, query, benchmark or extension test.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-embedded-analytics.md
- **Related projects:** DuckDB extensions, Arrow, Parquet and embedded analytics tooling.
- **Caveats / risks:** Major-version API/extension compatibility needs review. Release/integration CI failures do not prove core SQL malfunction. Check optional extension licenses.
- **Research notes:** research/2026-10-21-caddy-certmagic-duckdb-maintenance.md; upstream CI is not independent verification.

### go-libp2p

- **Repository:** https://github.com/libp2p/go-libp2p
- **Author / Org:** libp2p
- **Category:** peer-to-peer networking / protocol stack / NAT traversal / distributed systems
- **Evidence:** VERIFIED (upstream implementation, documentation and maintenance evidence; not independently executed)
- **Tier / Score:** S / 29 (provisional)
- **What it does:** Composable Go implementation of the libp2p peer-to-peer networking stack.
- **Why it is valuable:** Reusable transport, peer identity, discovery and NAT traversal layers for resilient distributed applications.
- **Useful code/components:** host and network abstractions; transport composition; NAT traversal and hole punching; reachability and AutoNAT logic; peer identity and secure channel layers; stream multiplexing; protocol negotiation; connection management; examples; Grafana production dashboards.
- **Install / runtime:** Go module embedded in Go applications; network behavior depends on transport, NAT and deployment environment.
- **Platforms:** Go-supported systems, Linux, Windows, macOS.
- **License:** MIT at upstream root; dependencies/extensions require separate review.
- **Maintenance signals:** 2026-09-21 v0.50.0 release commit; 2026-09-19 oversized opaque HTTP auth input correction and QUIC/WebTransport dependency updates.
- **Verification performed:** README, root license and upstream commits inspected; no independent build, runtime, network, performance or security tests.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-p2p-networking.md
- **Related projects:** libp2p specifications, go-libp2p examples, QUIC, WebTransport and AutoNAT.
- **Caveats / risks:** Root repository is MIT licensed, but dependencies, integrations, protocol implementations, and downstream projects may carry separate licenses and operational constraints.
- **Research notes:** Promoted from READY queue on 2026-10-14; score remains provisional. No third-party source copied.

### uv

- **Repository:** https://github.com/astral-sh/uv
- **Author / Org:** Astral
- **Category:** Python tooling / dependency management / Rust CLI
- **Evidence:** VERIFIED (upstream evidence; not independently executed)
- **Tier / Score:** S / 29 (provisional; Utility + Working Evidence + Reusability + Novelty + Documentation + Maintenance = 5+5+5+4+5+5)
- **What it does:** Fast Rust-based Python package and project manager supporting lockfiles, interpreters, workspaces, tools, scripts, caching and pip-compatible commands.
- **Why it is valuable:** A reusable dependency resolver, package installation stack and environment manager with extensive upstream tests and cross-platform distribution.
- **Useful code/components:** `crates/uv-resolver/src/pubgrub/` dependency solver; `crates/uv-lock/` lockfiles; `crates/uv-cache/` cache; `crates/uv-install-wheel/` wheel installation; `crates/uv-python-discovery/` interpreter discovery; `crates/uv-virtualenv/` environments; `crates/uv-build-backend/` builds.
- **Install / runtime:** Standalone installers or PyPI; Rust toolchain for source builds; some operations access package indexes or download interpreters.
- **Platforms:** Linux, macOS, Windows.
- **License:** Apache-2.0 OR MIT; inspect dependency and component terms before copying.
- **Maintenance signals:** Upstream v0.13.1 published 2026-10-14; same-day commits; CI, integration, smoke and release workflows.
- **Verification performed:** README, MIT and Apache-2.0 root licenses inspected; uv-resolver source tree and GitHub Actions test workflows inspected; v0.13.1 upstream release published 2026-10-14 inspected; No independent build, install or benchmark.
- **Source discovery:** GitHub-first; research/2026-08-21-python-tooling.md
- **Related projects:** Astral Ruff, ty; Python packaging standards.
- **Caveats / risks:** Upstream 10–100x speed claims not independently benchmarked. Downloaded interpreters, packages and third-party dependencies have separate licenses and supply-chain risks.
- **Research notes:** Promoted from READY queue on 2026-10-14. No upstream code copied.

### age

- **Repository:** https://github.com/FiloSottile/age
- **Author / Org:** Filippo Valsorda and contributors
- **Category:** File encryption / Go cryptography / CLI / interoperability
- **Evidence:** VERIFIED (upstream evidence; not independently executed)
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Interoperable encrypted-file format, Go library and command-line tools supporting recipients, identities, passphrases, plugins and hybrid post-quantum options.
- **Why it is valuable:** Small composable encryption interfaces, documented format and independent implementations enable secure file-exchange applications.
- **Useful code/components:** `age.go`, `x25519.go`, `scrypt.go`, `pq.go`, `plugin/`, `cmd/age/`, `cmd/age-keygen/`, `cmd/age-inspect/`, `age_test.go`
- **Install / runtime:** Prebuilt CLI or Go module `filippo.io/age`; source go.mod specifies Go 1.25 and toolchain Go 1.27.
- **Platforms:** Linux, macOS, Windows, BSD.
- **License:** BSD 3-Clause-style; inspect dependency and component terms before copying.
- **Maintenance signals:** v1.3.2 (2026-08-29) adds parser/input hardening and new binary/platform coverage. Main Go tests passed 2026-10-21; earlier main tests failed October 10–12, with later successful runs. Feature-branch checks are not counted as main evidence.
- **Verification performed:** 2026-10-21 upstream release, code tree, license and CI reviewed. Root BSD 3-Clause-style license requires notices; plugin/dependency terms vary. No independent cryptographic audit, interoperability, fuzzing, CLI encryption or decryption test.
- **Source discovery:** GitHub-first; research/2026-08-21-file-encryption.md
- **Related projects:** str4d/rage; FiloSottile/typage; str4d/age-plugin-yubikey; age C2SP format.
- **Caveats / risks:** Catalog inclusion is not a cryptographic audit. Plugins and dependencies require separate review. v1.3.2 rejects some formerly accepted malformed or oversized inputs.
- **Research notes:** `research/2026-10-21-organicmaps-kopia-age-maintenance.md`. Root BSD 3-Clause-style license requires notices; plugin/dependency terms vary. No independent cryptographic audit, interoperability, fuzzing, CLI encryption or decryption test.

### Tailscale

- **Repository:** https://github.com/tailscale/tailscale
- **Author / Org:** Tailscale Inc. and contributors
- **Category:** overlay networking / WireGuard / NAT traversal / embedded networking / private networks
- **Evidence:** VERIFIED (upstream release, implementation, test and CI evidence; no independent runtime test).
- **Tier / Score:** S / 29; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it does:** WireGuard-based private overlay networking with NAT traversal and relay fallback; tsnet embeds an authenticated tailnet node into Go programs.
- **Why it is valuable:** Reusable networking infrastructure with documented architecture, active maintenance and upstream test coverage.
- **Useful code/components:** `tsnet/tsnet.go: embedded tailnet server`; `tsnet/example/: examples`; `wgengine/: userspace networking engine`; `wgengine/magicsock/: NAT traversal`; `wgengine/netstack/: gVisor userspace TCP/IP`; `tailcfg/: control protocol types`; `tailscaled and CLI`.
- **Install / runtime:** Official client packages, or Go module tailscale.com/tsnet; tailnet enrollment required.
- **Platforms:** Linux, Windows, macOS, selected BSD, Go embedded services.
- **License:** BSD-3-Clause; review third-party notices and component licenses before extraction.
- **Maintenance signals:** Upstream release v1.104.1 (2026-10-07); recent commits 2026-10-14; source tests and GitHub Actions workflows inspected.
- **Verification performed:** README and BSD-3-Clause LICENSE inspected on 2026-10-14; tsnet README/source and tests, wgengine directory and CI workflows inspected; upstream stable release v1.104.1 published 2026-10-07; upstream commits 2026-10-14 inspected; no independent build or deployment.
- **Source discovery:** GitHub-first; research/2026-08-21-overlay-networking.md
- **Related projects:** juanfont/headscale; WireGuard/wireguard-go; tailscale/tailscale-android.
- **Caveats / risks:** Hosted control plane and some proprietary GUI code are not included; check dependency notices, device enrollment and ACL configuration. No upstream code copied or independent security audit performed.
- **Research notes:** Promoted from READY queue on 2026-10-14. Inspect exact upstream paths in the source tree before reuse.

### Headscale

- **Repository:** https://github.com/juanfont/headscale
- **Author / Org:** Juan Font / Headscale contributors
- **Category:** self-hosted networking / Tailscale control plane / WireGuard coordination
- **Evidence:** VERIFIED (upstream release, implementation, test and CI evidence; no independent runtime test).
- **Tier / Score:** S / 28; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **What it does:** Self-hosted coordination server for Tailscale-compatible clients, with enrollment, policy, node management and route distribution.
- **Why it is valuable:** Reusable networking infrastructure with documented architecture, active maintenance and upstream test coverage.
- **Useful code/components:** `hscontrol/: control server`; `hscontrol/api/: management API`; `integration/: integration tests`; `registration and pre-auth keys`; `OIDC authorization`; `ACL and policy evaluation`; `DERP and route coordination`.
- **Install / runtime:** Deploy the Go server with release-tag-matched configuration; requires compatible clients.
- **Platforms:** Linux server, Go source, Nix-supported hosts.
- **License:** BSD-3-Clause; review third-party notices and component licenses before extraction.
- **Maintenance signals:** Upstream release v0.29.5 (2026-10-13); recent commits 2026-10-13; source tests and GitHub Actions workflows inspected.
- **Verification performed:** README and BSD-3-Clause LICENSE inspected on 2026-10-14; hscontrol and integration source trees and CI workflows inspected; upstream v0.29.5 published 2026-10-13 with policy and route fixes; 2026-10-13 commits inspected; no independent deployment or interoperability test.
- **Source discovery:** Recursive Tailscale research; research/2026-08-21-self-hosted-control-plane.md
- **Related projects:** tailscale/tailscale; WireGuard/wireguard-go.
- **Caveats / risks:** Self-hosted tailnet coordination, not feature parity with hosted Tailscale. Follow configuration/docs matching the installed release tag; security-sensitive policies require review. No upstream code copied or independent security audit performed.
- **Research notes:** Promoted from READY queue on 2026-10-14. Inspect exact upstream paths in the source tree before reuse.

### wireguard-go

- **Repository:** https://github.com/WireGuard/wireguard-go
- **Author / Org:** WireGuard LLC / WireGuard contributors
- **Category:** userspace VPN / encrypted networking / Go networking / TUN interface
- **Evidence:** VERIFIED (upstream source, release and maintenance evidence; not independently executed)
- **Tier / Score:** S / 28; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **What it does:** Go implementation of the WireGuard userspace VPN tunnel.
- **Why it is valuable:** Portable userspace WireGuard implementation and reusable networking abstractions.
- **Useful code/components:** device/: WireGuard protocol, handshake and packet pipeline; conn/: UDP endpoint and batching; tun/: cross-platform TUN integration; ipc/: control interface; replay/: anti-replay logic; ratelimiter/: handshake limiting; rwcancel/: cancellable descriptor I/O; tai64n/: timestamps.
- **Install / runtime:** Go 1.23.1 (go.mod); kernel WireGuard is preferred on supported Linux systems.
- **Platforms:** Linux, Windows, macOS, BSD and other Go-supported targets where TUN support exists.
- **License:** MIT; preserve upstream copyright and dependency notices before code reuse.
- **Maintenance signals:** No GitHub releases; latest inspected commit 2026-10-06 corrects handshake-response state (2631ce99).
- **Verification performed:** official upstream README inspected; root repository structure inspected; upstream licensing text inspected; recent commit history inspected; 2026-05-22 Linux vectorized-I/O/TUN header correctness fix observed; not independently built, fuzzed, benchmarked, deployed, cryptographically audited, or interoperability-tested by GitHub Gold; 2026-10-16 root license, release and commit surfaces rechecked. No independent build, deployment, benchmark or security audit.
- **Source discovery:** Recursive networking research; research/2026-08-21-wireguard-userspace.md
- **Related projects:** tailscale/tailscale (userspace engine fork); WireGuard kernel implementation.
- **Caveats / risks:** Upstream recommends the kernel WireGuard implementation on Linux when available. Catalog inclusion is not a cryptographic audit, and downstream forks such as Tailscale's may contain meaningful divergence. No third-party implementation code copied.
- **Research notes:** Promoted from READY queue on 2026-10-16; source evidence is not a runtime test.

### Nebula

- **Repository:** https://github.com/slackhq/nebula
- **Author / Org:** Slack Technologies / slackhq contributors
- **Category:** overlay networking / peer-to-peer SDN / NAT traversal / private networking
- **Evidence:** VERIFIED (upstream source, release and maintenance evidence; not independently executed)
- **Tier / Score:** S / 28; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **What it does:** Peer-to-peer encrypted overlay network with lighthouse discovery, certificates, and firewall policies.
- **Why it is valuable:** Self-hosted encrypted overlay network with explicit identity, policy and peer discovery.
- **Useful code/components:** handshake/: authenticated Noise handshakes; lighthouse.go: peer discovery; hostmap.go: peer state; punchy.go: UDP hole punching; cert/: certificate identities; firewall.go: group-aware firewall; overlay/: TUN and platform adapters; e2e/: end-to-end tests.
- **Install / runtime:** Go 1.27.2 (current go.mod); nebula and nebula-cert executables.
- **Platforms:** Linux, Windows, macOS, BSD.
- **License:** MIT; preserve upstream copyright and dependency notices before code reuse.
- **Maintenance signals:** Stable v1.11.2 published 2026-09-22; commits on 2026-10-16 add tunnel framing tests and certificate validation fixes.
- **Verification performed:** repository metadata inspected; official README inspected; root license metadata inspected; recent maintenance commits inspected; 2026-08-21 native Go fips140 support observed; 2026-08-21 TUN offload work observed; 2026-08-20 fail-closed IPv6 parsing fix observed; 2026-08-20 32-bit CA command memory-safety fix observed; not independently deployed, built, tested, benchmarked, fuzzed, cryptographically audited, or FIPS-validated by GitHub Gold; 2026-10-16 root license, release and commit surfaces rechecked. No independent build, deployment, benchmark or security audit.
- **Source discovery:** GitHub-first and recursive networking research; research/2026-08-22-nebula-overlay-networking.md
- **Related projects:** Defined Networking mobile clients; WireGuard and Tailscale as architectural comparisons.
- **Caveats / risks:** Private-network infrastructure is security-sensitive; catalog inclusion is not an audit. Direct paths depend on NAT/firewall topology, CA key handling is critical, companion mobile code is separate, and FIPS build support is not blanket deployment compliance. No third-party implementation code copied.
- **Research notes:** Promoted from READY queue on 2026-10-16; source evidence is not a runtime test.

### Nushell

- **Repository:** https://github.com/nushell/nushell
- **Author / Org:** Nushell Project
- **Category:** developer tooling / shell / structured data pipelines / cross-platform automation
- **Evidence:** VERIFIED (upstream source, release and maintenance evidence; not independently executed)
- **Tier / Score:** S / 28; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **What it does:** Cross-platform shell that treats pipeline data as typed values rather than only text.
- **Why it is valuable:** Structured data pipelines and reusable shell/parser/plugin components.
- **Useful code/components:** crates/nu-protocol/: typed values and pipelines; crates/nu-parser/: language parsing; crates/nu-engine/: execution engine; crates/nu-command/: built-in commands; crates/nu-plugin/: plugin APIs; structured file and process-stream integration.
- **Install / runtime:** Prebuilt nu releases or Rust toolchain for source builds.
- **Platforms:** Linux, Windows, macOS.
- **License:** MIT; preserve upstream copyright and dependency notices before code reuse.
- **Maintenance signals:** Stable 0.116.1 published 2026-10-04; 2026-10-16 commits correct plugin-input lifetime, MCP visibility and number formatting.
- **Verification performed:** official README inspected; root MIT license inspected; repository metadata inspected; CI/nightly and release surfaces inspected; 0.114.1 release dated 2026-07-11 observed upstream; August 2026 ecosystem maintenance observed; not independently built, benchmarked, or cross-platform tested by GitHub Gold; 2026-10-16 root license, release and commit surfaces rechecked. No independent build, deployment, benchmark or security audit.
- **Source discovery:** GitHub-first discovery; research/2026-08-22-structured-shell.md
- **Related projects:** nushell/reedline; nushell/nushell.github.io.
- **Caveats / risks:** Nushell semantics differ materially from POSIX shells and some commands/design details may evolve. Plugins, packages, integrations, and separately maintained ecosystem repositories require independent license checks. No third-party implementation code copied.
- **Research notes:** Promoted from READY queue on 2026-10-16; source evidence is not a runtime test.

### Reedline

- **Repository:** https://github.com/nushell/reedline
- **Author / Org:** Nushell Project
- **Category:** developer tooling / interactive CLI / line editor / Rust library
- **Evidence:** VERIFIED (upstream source, release and maintenance evidence; not independently executed)
- **Tier / Score:** S / 28; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **What it does:** Rust readline-like line editor with completion, history, highlighting and multiple editing modes.
- **Why it is valuable:** Reusable interactive terminal input engine independent of a full shell.
- **Useful code/components:** src/engine.rs: editor engine; completion and menu interfaces; highlighter, hinter, validator traits; file and SQLite-backed history; Emacs, Vi and Helix keybinding modes; Unicode/grapheme-aware editing; examples/: integration samples.
- **Install / runtime:** Rust >=1.95.0 (current Cargo.toml); crossterm and optional feature dependencies.
- **Platforms:** Linux, Windows, macOS terminals.
- **License:** MIT; preserve upstream copyright and dependency notices before code reuse.
- **Maintenance signals:** Stable v0.52.1 published 2026-10-04; 2026-10-10 commits add opt-in paste hooks and improve editor state handling.
- **Verification performed:** official README inspected; root MIT license inspected; Cargo.toml and feature definitions inspected; current manifest version 0.50.0 observed; recent commits through 2026-08-21 inspected; correctness fixes and RustSec-driven dependency maintenance observed; not independently built, fuzzed, benchmarked, terminal-matrix tested, or security-audited by GitHub Gold; 2026-10-16 root license, release and commit surfaces rechecked. No independent build, deployment, benchmark or security audit.
- **Source discovery:** Recursive Nushell ecosystem research; research/2026-08-22-line-editor.md
- **Related projects:** nushell/nushell; crossterm.
- **Caveats / risks:** Upstream lists complex Unicode scripts, expensive completion/prompt handling, and full-duplex concurrent output as areas needing further improvement. Optional dependencies and downstream integrations retain separate licenses. No third-party implementation code copied.
- **Research notes:** Promoted from READY queue on 2026-10-16; source evidence is not a runtime test.


### MCAP

- **Repository:** https://github.com/foxglove/mcap
- **Author / Org:** Foxglove Technologies / foxglove
- **Category:** Robotics / telemetry / indexed binary log formats / cross-language data interchange
- **Evidence:** VERIFIED (upstream source, CI, conformance and release evidence; not independently executed)
- **Tier / Score:** S / 29; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it does:** Serialization-agnostic container format and multi-language libraries for timestamped messages, schemas, chunks, indexes, metadata and attachments.
- **Why it is valuable:** Durable telemetry interchange with streaming and indexed readers, six language implementations, conformance tests and CLI utilities.
- **Useful code/components:** `typescript/core/src/McapStreamReader.ts`; `typescript/core/src/McapIndexedReader.ts`; `typescript/core/src/McapWriter.ts`; `rust/mcap/src/read.rs`; `rust/mcap/src/write.rs`; `rust/cli/src/commands/`; `tests/conformance/`; `website/docs/spec/mcap.ksy`.
- **Install / runtime:** Language-specific packages/toolchains (C++, Go, Python, Rust, TypeScript/JavaScript, Swift); packaged MCAP CLI binaries or Homebrew.
- **Platforms:** Linux, macOS, Windows; runtime support varies by implementation.
- **License:** MIT at repository root; review dependency notices for reused components.
- **Maintenance signals:** MCAP CLI v0.4.0 released 2026-10-16; Rust CLI features include CSV/NDJSON export and timestamp formatting changes.
- **Verification performed:** README, root LICENSE, implementation directories, CI/conformance directory, recent commits and release feed inspected 2026-10-17. No independent build, tests, benchmark or parser security audit.
- **Source discovery:** GitHub-first; `research/2026-09-05-mcap-robotics-telemetry-container-conformance-toolkit.md` and `research/2026-09-09-mcap-robotics-telemetry-log-format.md`.
- **Related projects:** ROS 1/ROS 2 integrations, Foxglove SDK, Kaitai Struct, MCAP conformance tools.
- **Caveats / risks:** CLI v0.4.0 changes default timestamp output; automation expecting integer nanoseconds may break. Parsing untrusted files remains security-sensitive.
- **Research notes:** Promoted from existing research dossiers on 2026-10-17; no third-party implementation code copied.

### sherpa-onnx

- **Repository:** https://github.com/k2-fsa/sherpa-onnx
- **Author / Org:** k2-fsa
- **Category:** Offline AI / speech recognition / speech synthesis / Android / Termux
- **Evidence:** VERIFIED (upstream source, CI and release evidence; not independently executed)
- **Tier / Score:** S / 29; Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it does:** Local inference toolkit for ASR, TTS, VAD, speaker diarization/identification, keyword spotting and other audio tasks.
- **Why it is valuable:** Cross-platform offline speech stack with C++ core, C API, Python and Rust bindings, mobile integration and extensive build workflows.
- **Useful code/components:** `sherpa-onnx/csrc/`; `sherpa-onnx/c-api/c-api.h`; `sherpa-onnx/c-api/c-api.cc`; `sherpa-onnx/python/`; `sherpa-onnx/rust/`; Android build workflows; VAD and streaming/offline recognizers.
- **Install / runtime:** Model files and platform-specific inference binaries or build toolchain; native Android Termux/Python-in-Termux paths documented in v1.13.8.
- **Platforms:** Android/Termux, Linux, Windows, macOS, iOS, WebAssembly; architecture/backend support varies.
- **License:** Apache-2.0 at repository root; separately review model weights, dependencies and accelerator SDKs.
- **Maintenance signals:** Stable v1.13.8 published 2026-09-10; C API exception-handling PR #4044 merged 2026-10-14; Rust zip dependency advisory fix committed 2026-10-17.
- **Verification performed:** README, root LICENSE, C API and C++ source directories, multi-platform CI, release notes, security-fix commit and PR inspected 2026-10-17. No independent model execution, build, benchmark or audit.
- **Source discovery:** GitHub-first and offline AI ecosystem; `research/2026-10-17-sherpa-onnx-termux-c-api-safety.md`.
- **Related projects:** k2-fsa speech ecosystem; ONNX Runtime; Termux; Android audio applications.
- **Caveats / risks:** The October C API and Rust dependency fixes postdate stable v1.13.8; do not assume stable builds contain them. Models and dependencies may have separate licenses and RAM/storage requirements.
- **Research notes:** Promoted 2026-10-17; upstream build and release evidence does not equal an independent performance or security test.


### pyOCD

- **Repository:** https://github.com/pyocd/pyOCD
- **Author / Org:** pyocd contributors
- **Category:** Embedded debugging / Arm Cortex-M / firmware programming / Python automation / debug probes
- **Evidence:** VERIFIED (upstream source, tests, CI configuration and release evidence; not independently executed)
- **Tier / Score:** S / 28; Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it does:** Python CLI and library for programming, inspecting, and debugging Arm Cortex-M devices through supported probes.
- **Why it is valuable:** Reusable CMSIS-DAP, ST-Link, J-Link, GDB server, CMSIS-Pack target support, flash loading, RTOS-aware debugging, and SWV tracing.
- **Useful code/components:** `pyocd/probe/cmsis_dap_probe.py`; `pyocd/probe/stlink_probe.py`; `pyocd/probe/jlink_probe.py`; `pyocd/gdbserver/gdbserver.py`; `pyocd/flash/loader.py`; `pyocd/target/pack/`; `pyocd/rtos/`; `pyocd/trace/swv.py`; `test/unit/`.
- **Install / runtime:** Python 3.9+, libusb or suitable USB backend, supported probe and Cortex-M target for hardware operations; PyPI package available.
- **Platforms:** Linux, Windows, macOS, FreeBSD; MCU support depends on probe and target.
- **License:** Apache-2.0 at root; verify separate documentation, vendor device-pack, and dependency terms.
- **Maintenance signals:** v0.45.1 released 2026-07-21; v0.45 series adds debug sequences and RTT/SWV file capture; CI declares three OSes and Python 3.9–3.14 with pytest, lint and package checks.
- **Verification performed:** README, license, packaging, security and remote-probe guides, CI workflow, and official releases inspected 2026-10-18. No independent install, test execution, flashing, benchmark or security audit.
- **Source discovery:** GitHub-first, recursive follow-up to existing probe-rs dossier.
- **Related projects:** probe-rs/probe-rs; CMSIS-DAP; Open-CMSIS-Pack; DAPLink.
- **Caveats / risks:** Auto-unlock can mass-erase protected targets; exposing remote probe access permits device control. Upstream describes beta quality and possible 1.0 API changes.
- **Research notes:** `research/2026-10-18-pyocd-cortexm-debugging-flashing-evidence.md`. Score reflects upstream evidence, not independently reproduced hardware tests. No third-party code copied.



### FlatGeobuf

- **Repository:** https://github.com/flatgeobuf/flatgeobuf
- **Author / Org:** Björn Harrtell and FlatGeobuf contributors
- **Category:** Geospatial binary features / packed Hilbert R-tree / HTTP byte ranges
- **Evidence:** VERIFIED (upstream source, tests and CI definitions; not independently executed)
- **Tier / Score:** S / 29 — Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 5.
- **What it does:** Static FlatBuffers-based geographic feature format with optional packed R-tree, bounding-box filtering, streaming and byte-range access.
- **Why it is valuable:** Enables selective retrieval of large vector datasets for offline-first maps and geospatial tools without requiring a database server.
- **Useful code/components:** `src/ts/http-reader.ts`, `src/ts/packedrtree.ts`, `src/ts/packedrtree.spec.ts`, `src/ts/seekable-zstd.ts`, `src/ts/geojson.ts`, `src/fbs/header.fbs`, `src/fbs/feature.fbs`, `src/rust/src/`, `src/go/`.
- **Install / runtime:** Language-specific packages; TypeScript CI uses Node 22/24 and pnpm 12; Rust crate manifest requires Rust 1.85+. HTTP filtering requires Range and CORS support.
- **Platforms:** Browser/Node, Rust, C++, Go, Java, .NET, local files and servers.
- **License:** Root BSD-2-Clause; package.json BSD-3-Clause; `src/ts/LICENSE` ISC; Rust manifest BSD-2-Clause. Review component notices before reuse.
- **Maintenance signals:** 2026-10-07 TypeScript R-tree boundary/duplicate regression fix; cross-language CI configuration.
- **Verification performed:** Inspected upstream source, test, license files and CI 2026-10-18. No independent execution or audit.
- **Source discovery:** GitHub-first; `research/2026-10-18-spatial-stack-interoperability-maintenance.md`.
- **Related projects:** DuckDB Spatial, PMTiles, MapLibre, GDAL, geozero.
- **Caveats / risks:** Static feature format, not a tile renderer or in-place random-write database; mixed license declarations; range-request latency and version-specific APIs.
- **Research notes:** No upstream implementation code copied.

### DuckDB Spatial

- **Repository:** https://github.com/duckdb/duckdb-spatial
- **Author / Org:** DuckDB Foundation and contributors
- **Category:** Geospatial SQL / R-tree / GDAL / vector tiles / offline analytics
- **Evidence:** VERIFIED (upstream implementation and regression-test source; not independently executed)
- **Tier / Score:** S / 27 — Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 4, Maintenance 5.
- **What it does:** DuckDB extension providing geometry types, spatial SQL, R-tree indexing, geographic file I/O, CRS transforms, OSM PBF processing and Mapbox Vector Tile output.
- **Why it is valuable:** Composable local geospatial analytics, conversion and map-data preparation with SQL rather than a separate geospatial server.
- **Useful code/components:** `src/spatial/index/rtree/`, `test/sql/index/rtree_basic.test`, `src/spatial/modules/gdal/`, `src/spatial/modules/mvt/`, `src/spatial/modules/osm/`, `src/spatial/modules/proj/`, `src/spatial/modules/geos/`, `test/sql/mvt/st_asmvt.test`.
- **Install / runtime:** Compatible DuckDB binary and spatial extension (`INSTALL spatial; LOAD spatial;`); source builds use CMake, C++ toolchain, OpenSSL and bundled dependencies.
- **Platforms:** Platforms with matching DuckDB extension builds; pin binary and extension versions.
- **License:** MIT root; third-party GDAL, GEOS, PROJ and bundled notices must be reviewed separately.
- **Maintenance signals:** 2026-10-18 upstream GDAL JSON patch correction; SQL regression tests and distribution CI.
- **Verification performed:** Inspected README, source/test paths, LICENSE and CI on 2026-10-18; no local SQL execution, build or benchmark.
- **Source discovery:** GitHub-first; `research/2026-10-18-spatial-stack-interoperability-maintenance.md`.
- **Related projects:** DuckDB, FlatGeobuf, PMTiles, MapLibre, GDAL.
- **Caveats / risks:** README still says spatial indexing unsupported although R-tree code/tests exist; feature support is version-dependent; geometry storage described upstream as work in progress.
- **Research notes:** `RTREE_INDEX_SCAN` appears in test source, not a locally observed successful run. No third-party implementation code copied.


### TinyUSB

- **Repository:** https://github.com/hathach/tinyusb
- **Author / Org:** Ha Thach and contributors
- **Category:** Embedded USB / MCU host-device stacks / firmware / protocol drivers
- **Evidence:** VERIFIED (upstream source, tests and CI configuration; not independently run)
- **Tier / Score:** S / 27 — Utility 5, Working Evidence 4, Reusability 5, Novelty 3, Documentation 5, Maintenance 5.
- **What it does:** Portable C USB host/device stack for embedded controllers with USB class drivers, board examples, and bare-metal/RTOS integrations.
- **Why it is valuable:** Reusable USB enumeration, endpoint handling, class-driver and controller-backend implementations across many microcontroller families.
- **Useful code/components:** `src/host/usbh.c`; `src/device/`; `src/class/`; `src/portable/`; `src/portable/raspberrypi/rp2040/hcd_rp2040.c`; `src/osal/`; `examples/`; `test/unit-test/project.yml`; `test/fuzz/`; `test/hil/`.
- **Install / runtime:** Integrate with supported board SDK/toolchain, `tusb_config.h`, descriptor callbacks and host/device task processing; consult official board-specific examples. Host/device roles vary by MCU.
- **Platforms:** Embedded C, 50+ MCU families claimed upstream, bare metal, FreeRTOS, RT-Thread and Mynewt; verify exact controller support.
- **License:** MIT root; inspect separately licensed vendor SDKs and `lib/` dependencies before extracting code.
- **Maintenance signals:** Official 0.21.0 release published 2026-06-30; upstream commits through 2026-10-18; test and fuzz infrastructure.
- **Verification performed:** Inspected README.rst, LICENSE, host source, class directories, Ceedling configuration and pre-commit workflow 2026-10-18. Unit-test invocation is commented out in that workflow; fuzz harnesses are configured but not run by GitHub Gold.
- **Source discovery:** GitHub-first; `research/2026-10-08-tinyusb-embedded-usb-host-device-stack.md`.
- **Related projects:** Raspberry Pi Pico SDK, ESP-IDF, FreeRTOS, Adafruit TinyUSB integrations.
- **Caveats / risks:** Static allocation is not a formal memory-safety guarantee for C. USB host/device availability differs by target; DFU mode, video and PD3 are partly WIP. October 18 HIL recovery tooling changes do not prove stack correctness.
- **Research notes:** No third-party code copied; no independent firmware build, test execution, fuzzing, hardware enumeration, or security audit.


### LighthouseReckoning

- **Repository:** https://github.com/TidalImpact/LighthouseReckoning
- **Author / Org:** Fynn Jannis Schulz / TidalImpact
- **Category:** LoRa / embedded routing / off-grid sensor telemetry
- **Evidence:** VERIFIED — upstream source, field-test and release evidence, not independently executed
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- **What it does:** Small RadioLib-based C++ library routing LoRa sensor data through confirmed hops toward one Home node.
- **Why it is valuable:** Compact packet protocol, many-to-one routing, retries, raw field-test logs, sleep-aware scheduling, and tunable RAM use.
- **Useful code/components:** `src/LHR_Routing.*` (routes); `src/LHR_Tx.*` and `LHR_Rx.*` (retries/receive); `src/LHR_Packet.h` (framing); `src/LHR_DutyCycle.*` (airtime); `src/LHR_Encryption*.*` (per-hop crypto); `src/LighthouseReckoning.cpp` (sleep scheduling and local queue); `src/LHR_RamConfig.h` (~248-byte buffer toggle); `examples/`; `fieldtests/2026-08-09_forced-chain-test/`.
- **Install / runtime:** Arduino or PlatformIO plus RadioLib and suitable LoRa hardware; configure regional radio limits.
- **Platforms:** RP2040 and ESP32 upstream tested; SX126x CAD/interrupt behavior validated; other RadioLib chips need verification.
- **License:** MIT root; review RadioLib and vendor SDK licensing separately.
- **Maintenance signals:** v1.3.0 released 2026-10-16; adds `getNextUpdateInMs()`, one local-data queue slot, RAM toggle and ESP32 encryption detection fix. Upstream compile workflow excludes new SleepyNode sketches.
- **Verification performed:** Inspected source, release, README, changelog, license, CI configuration and upstream 1h53m forced-chain field test with raw log. No independent build, RF test, log parsing or security audit.
- **Source discovery:** GitHub-first; `research/2026-09-30-lighthouse-reckoning-lora-mesh-routing.md` and `research/2026-10-18-lighthouse-reckoning-v13-maintenance.md`.
- **Related projects:** jgromes/RadioLib; Meshtastic; MeshCore; Reticulum.
- **Caveats / risks:** Single-sink only; no end-to-end ACK. Shared-key AES-128-CCM is hop-by-hop with no replay protection. One queued local packet and one global retry cycle. Forced chain was physically close, not a long-range RF test.
- **Research notes:** Independently parse raw log and test v1.3 sleep/queue behavior on hardware before stronger claims.


### RadioLib

- **Repository:** https://github.com/jgromes/RadioLib
- **Author / Org:** Jan Gromeš / jgromes
- **Category:** Embedded radio / LoRa / LoRaWAN / radio drivers / digital modes
- **Evidence:** VERIFIED — upstream source, release and CI evidence; no independent execution
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 5)
- **What it does:** C++ radio abstraction and protocol library spanning LoRa, FSK/OOK, LoRaWAN and amateur-radio digital modes.
- **Why it is valuable:** Reusable transceiver drivers, hardware abstraction, cross-platform examples and radio-protocol implementations underpin multiple embedded and off-grid projects, including LighthouseReckoning.
- **Useful code/components:** `src/Hal.h` and `src/hal/` (GPIO/SPI/time abstraction); `src/modules/SX126x/SX126x.cpp` and `src/modules/` (radio chip drivers); `src/protocols/LoRaWAN/LoRaWAN.cpp` (LoRaWAN); `src/protocols/AX25/`, `APRS/`, `RTTY/`, `SSTV/`, `Pager/` (digital modes); `src/utils/`; `examples/NonArduino/`; `extras/test/unit/` and `extras/test/fuzz/`; `extras/SX126x_Spectrum_Scan/`.
- **Install / runtime:** Arduino Library Manager, PlatformIO or ESP-IDF component; CMake/non-Arduino integration documented upstream. Requires compatible radio chip, GPIO/SPI wiring and board-specific platform setup.
- **Platforms:** Arduino AVR (constrained), ESP32/ESP8266, RP2040, STM32, nRF52, Teensy and selected non-Arduino C++ targets; exact support varies by chip and mode.
- **License:** MIT (`license.txt`); preserve notice and check SDK, dependencies and hardware support files individually.
- **Maintenance signals:** Upstream 7.8.1 release 2026-09-28; master commit 9825002 dated 2026-10-18; compile matrix, unit, fuzz, static analysis and CodeQL workflows.
- **Verification performed:** Inspected README, license, metadata, HAL, SX126x and LoRaWAN sources, CI/test workflows, releases and recent commits. Observed CI/unit/fuzz/CodeQL success on a PR revision with Cppcheck failure on that same revision; did not run tests.
- **Source discovery:** GitHub-first, recursively followed from LighthouseReckoning; `research/2026-10-18-radiolib-radio-drivers-protocols.md`.
- **Related projects:** TidalImpact/LighthouseReckoning, Meshtastic, RadioShield, Semtech SX126x/LR11x0 radio ecosystems.
- **Caveats / risks:** Upstream LoRaWAN Class A/C and pre-certification claims are not independent verification. Radio/board compatibility and regulatory duty cycle/power limits vary. v7.7 introduced configuration-struct `begin` APIs; positional overloads are deprecated ahead of 8.0.0. AVR ATmega328 boards are discouraged upstream due to memory constraints.
- **Research notes:** Source and CI evidence support cataloging, not hardware or security certification. No upstream code copied.

### Termux:API Android App

- **Repository:** https://github.com/termux/termux-api
- **Author / Org:** Termux
- **Category:** Android / Termux / device APIs / local automation / IPC
- **Evidence:** VERIFIED — upstream implementation and APK build workflow; not independently executed
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 4, Maintenance 5)
- **What it does:** Android plugin exposing permission-gated device capabilities to Termux shell commands.
- **Why it is valuable:** Reusable mobile API dispatcher, permission boundary and response transport for scriptable Android automation.
- **Useful code/components:** `TermuxApiReceiver.java` (dispatch), `ResultReturner.java` (response lifecycle), `apis/LocationAPI.java`, `apis/SensorAPI.java`, `apis/UsbAPI.java`, `AndroidManifest.xml`.
- **Install / runtime:** Android Termux app and companion Termux:API plugin must have compatible signing keys; install CLI helper separately.
- **Platforms:** Android / Termux.
- **License:** GPLv3 stated in upstream README; no standalone root license established during inspection.
- **Maintenance signals:** September 2026 location and result-handling corrections; upstream Gradle APK build and artifact checks.
- **Verification performed:** Inspected README, source, manifest, build workflow and upstream commits; no APK build, install, instrumentation, hardware or security test.
- **Source discovery:** GitHub-first; `research/2026-09-08-termux-api-android-capability-cli-bridge.md` and `research/2026-10-19-termux-api-bridge-release-and-components.md`.
- **Related projects:** termux/termux-api-package; termux/termux-app; termux/termux-packages; termux/termux-boot.
- **Caveats / risks:** Broad Android permission surface; distribution signatures cannot be mixed freely; background-execution behavior varies by Android version and OEM. Review component-level notices before copying.
- **Research notes:** Source/CI evidence is not independent execution. No third-party source copied.

### Termux API CLI Package

- **Repository:** https://github.com/termux/termux-api-package
- **Author / Org:** Termux
- **Category:** Android / Termux / CLI / Unix-domain IPC
- **Evidence:** VERIFIED — upstream source, tagged release and downstream packaging; not independently executed
- **Tier / Score:** A / 23 (Utility 5, Working Evidence 3, Reusability 5, Novelty 4, Documentation 2, Maintenance 4)
- **What it does:** C runtime and CLI wrappers connecting Unix shell commands to Android-side Termux:API implementations.
- **Why it is valuable:** Compact, reusable local IPC pattern with authenticated peer checks, stdin/stdout transport and descriptor passing.
- **Useful code/components:** `termux-api.c` (Unix sockets, `SO_PEERCRED`, `SCM_RIGHTS`, Android 14+ fallback), `termux-api.h`, `CMakeLists.txt`, `scripts/`, `termux-callback.in`.
- **Install / runtime:** Termux `termux-api` package, compatible Android plugin, Bash, util-linux and termux-am.
- **Platforms:** Android / Termux.
- **License:** MIT root LICENSE; companion Android app separately GPLv3.
- **Maintenance signals:** Upstream v0.60.0 released 2026-09-16; official Termux packaging pins v0.60.0 with a SHA-256 source checksum.
- **Verification performed:** Inspected source, CMake, license, tag and downstream package recipe; no compilation, installation, socket fuzzing, device test or independent runtime verification.
- **Source discovery:** GitHub-first; `research/2026-09-08-termux-api-package-shell-android-bridge-runtime.md` and `research/2026-10-19-termux-api-bridge-release-and-components.md`.
- **Related projects:** termux/termux-api; termux/termux-packages; termux/termux-app.
- **Caveats / risks:** No repository-local CI/test matrix established; Android background restrictions and IPC lifecycle require device testing. Preserve MIT notice and review companion licensing.
- **Research notes:** Updates earlier v0.59.1 maintenance snapshot; Gold score raised from 22 to 23 based on current release evidence. No upstream code copied.


### MeshCore

- **Repository:** https://github.com/meshcore-dev/MeshCore
- **Author / Org:** meshcore-dev; MIT notice credits Scott Powell / rippleradios.com
- **Category:** LoRa / off-grid mesh / embedded C++ firmware
- **Evidence:** VERIFIED — upstream source, release and test evidence; no independent execution
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 4, Maintenance 5)
- **What it does:** Lightweight multi-hop packet-routing stack with companion-radio, repeater, room-server and sensor firmware.
- **Why it is valuable:** Reusable routing and serial interoperability components, published firmware artifacts and native tests.
- **Useful code/components:** `src/`, `include/`; `examples/companion_radio/`, `kiss_modem/`, `simple_repeater/`, `simple_room_server/`, `simple_secure_chat/`, `simple_sensor/`; `docs/kiss_modem_protocol.md`, `docs/companion_protocol.md`; `test/test_routing_policy/`, `test/test_kiss_modem/`, `test/test_mesh_tables/`.
- **Install / runtime:** PlatformIO/C++ or upstream firmware artifacts; compatible radio board.
- **Platforms:** Selected ESP32, nRF52, RP2040 and STM32 devices.
- **License:** MIT root; retain attribution and review third-party dependencies.
- **Maintenance signals:** Companion/repeater/room-server v1.18.0 releases dated 2026-10-15; native tests and board-build workflows, with successful feature-branch checks on 2026-10-19.
- **Verification performed:** Inspected source layout, README, license, workflows, test directories, release artifacts and commits; no independent build, RF test or security audit. Several newer PR checks required action.
- **Source discovery:** GitHub-first; `research/2026-09-20-meshcore-lightweight-packet-radio-mesh.md`; 2026-10-20 upstream release refresh.
- **Related projects:** Meshtastic, Reticulum, RadioLib, meshcore-dev/meshcore.js.
- **Caveats / risks:** Check firmware security configuration, licensing of dependencies, board support and regional RF rules; release artifacts alone do not establish field reliability.
- **Research notes:** No upstream code copied.

### Termux:Widget

- **Repository:** https://github.com/termux/termux-widget
- **Author / Org:** Termux
- **Category:** Android / Termux / launcher widgets / script shortcuts
- **Evidence:** PROMISING — source and build evidence; not independently executed
- **Tier / Score:** A / 24 (Utility 5, Working Evidence 3, Reusability 5, Novelty 3, Documentation 5, Maintenance 3)
- **What it does:** Launches user-controlled Termux scripts through Android widgets and launcher shortcuts.
- **Why it is valuable:** Reusable script discovery, shortcut creation and Android-to-Termux execution patterns.
- **Useful code/components:** `ShortcutUtils.java`, `ShortcutFile.java`, `TermuxWidgetProvider.java`, `TermuxLaunchShortcutActivity.java`, `TermuxWidgetService.java`, `AndroidManifest.xml`.
- **Install / runtime:** Termux and plugin signed with compatible keys; scripts in `~/.shortcuts/` and tasks in `~/.shortcuts/tasks/`.
- **Platforms:** Android / Termux.
- **License:** GPLv3-only (`LICENSE.md`); review dependencies.
- **Maintenance signals:** v0.15.0 released 2025-09-02; January 2026 build fix; upstream scheduled APK build passed 2026-09-01.
- **Verification performed:** Inspected README, source, manifest, license, release and workflow; no independent build, installation or security audit.
- **Source discovery:** GitHub-first from Termux:API; primary-source review 2026-10-20.
- **Related projects:** termux/termux-app, termux/termux-api, termux/termux-boot.
- **Caveats / risks:** Launcher permissions and shortcut handling need device-level validation; background execution and signing compatibility vary.
- **Research notes:** No upstream code copied.


### Glasgow Interface Explorer

- **Repository:** https://github.com/GlasgowEmbedded/glasgow
- **Author / Org:** GlasgowEmbedded contributors
- **Category:** Open hardware / FPGA gateware / protocol instrumentation / Python
- **Evidence:** PROMISING — inspected implementation, tests and passing upstream CI; no device execution
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 4, Reusability 5, Novelty 5, Documentation 4, Maintenance 4)
- **What it does:** USB-connected programmable interface explorer with Python host, FPGA gateware, firmware and protocol applets.
- **Why it is valuable:** Reusable protocol parsers, Amaranth gateware blocks and hardware-debugging workflows.
- **Useful code/components:** `software/glasgow/gateware/` (SPI, I2C, UART, JTAG, SWD, QSPI); `software/glasgow/protocol/sfdp.py` (JEDEC SFDP); `software/glasgow/applet/interface/`; `software/tests/gateware/`; `hardware/boards/glasgow/`; `firmware/`.
- **Install / runtime:** Python >=3.13,<3.16, PDM, Amaranth, libusb, optional YoWASP; Glasgow board needed for physical measurements.
- **Platforms:** Python host and Glasgow hardware.
- **License:** 0BSD OR Apache-2.0 for software; inspect firmware, hardware, vendor and submodule notices separately.
- **Maintenance signals:** 2026-10-20 commit `640848a9`; main-branch CI run `39421095221` succeeded; no GitHub Releases found; package declares alpha.
- **Verification performed:** Source, manifest, licenses, test tree, CI workflow and successful CI run inspected. No independent synthesis, tests or hardware measurements.
- **Source discovery:** GitHub-first; `research/2026-10-08-glasgow-interface-explorer.md`, refreshed 2026-10-20.
- **Related projects:** Amaranth HDL, YoWASP, libusb, flashrom (comparative lead).
- **Caveats / risks:** Hardware electrical limits; alpha applets; SFDP parser limited to base JESD216/JESD216A; lint omitted from required CI aggregate.
- **Research notes:** No source copied; upstream CI success is not physical device verification.

### ArchiveBox

- **Repository:** https://github.com/ArchiveBox/ArchiveBox
- **Author / Org:** ArchiveBox / Nick Sweeting
- **Category:** Web archiving / digital preservation / self-hosting / capture orchestration
- **Evidence:** VERIFIED — upstream release, source, tests and passing CI; not independently deployed
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Self-hosted capture platform preserving URLs as HTML, screenshots, PDF, WARC, media and metadata through CLI, web UI and API.
- **Why it is valuable:** Local ownership of durable archives and reusable heterogeneous capture pipelines.
- **Useful code/components:** `archivebox/cli/`, `archivebox/api/`, `archivebox/crawls/`, `archivebox/personas/`, `archivebox/mcp/`, `archivebox/plugins/`, `archivebox/tests/`; companion `ArchiveBox/abx-dl`.
- **Install / runtime:** Docker Compose or Python >=3.13 / uv; external Chromium, wget, yt-dlp and other tools.
- **Platforms:** Linux, macOS, Docker, self-hosted web/CLI.
- **License:** MIT root; third-party capture tools/plugins and archived content have separate licensing.
- **Maintenance signals:** Non-prerelease v0.9.73 published 2026-10-06; dev at 0.9.74rc327 on 2026-10-20; upstream CI success at `11e6dd31`.
- **Verification performed:** README, license, manifest, module tree, release notes, commits and successful CI metadata inspected. No independent capture or security testing.
- **Source discovery:** GitHub-first; `research/2026-09-02-archivebox-self-hosted-web-preservation-runtime.md`, refreshed 2026-10-20.
- **Related projects:** ArchiveBox/abx-dl, browser extension, Chromium, wget, yt-dlp, WARC.
- **Caveats / risks:** Prior v0.7.4 stable snapshot is outdated; untrusted page replay, downloads and authenticated browser cookies need isolation.
- **Research notes:** No third-party source copied. Distinguish non-prerelease v0.9.73 from newer development release candidates.


### abx-dl

- **Repository:** https://github.com/ArchiveBox/abx-dl
- **Author / Org:** ArchiveBox / Nick Sweeting
- **Category:** Web archiving / standalone capture runtime / Python CLI / plugin orchestration / digital preservation
- **Evidence:** VERIFIED — upstream release, implementation, tests and passing CI; not independently deployed
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Framework-independent URL downloader and plugin runner that captures pages, metadata, media and derived artifacts via the ArchiveBox plugin ecosystem.
- **Why it is valuable:** Reusable capture orchestration without a Django database, explicit event phases, plugin dependency resolution, typed events and durable JSONL output.
- **Useful code/components:** `abx_dl/catalog.py` (`PluginCatalog`, `PluginConfigResolver`); `abx_dl/orchestrator.py` (`download`, `parse_input`); `abx_dl/execution.py` (`execute_hook`, process-group cleanup); `abx_dl/events.py`; `abx_dl/services/`; `abx_dl/output_files.py` (`OutputManifest`); `abx_dl/cli.py`; `tests/`.
- **Install / runtime:** `uvx abx-dl` or `uv tool install abx-dl`; Python >=3.12,<3.15; `abx-plugins`, `abxpkg`, `abxbus`; optional external browser/downloader binaries and Docker.
- **Platforms:** Python on Linux/macOS; upstream Docker linux/amd64 and linux/arm64; other OS behavior not independently established.
- **License:** MIT root LICENSE (Nick Sweeting 2024); dependencies, plugin implementations, external binaries and captured content retain their own rights.
- **Maintenance signals:** v1.13.242 published 2026-10-20 15:34 UTC; upstream CI run `39448373304` succeeded at commit `367d06dc` with 18 successful jobs and one skipped, including Python tests, all-plugin tests and Docker builds on amd64/arm64.
- **Verification performed:** README, manifest, license, code, test cases, release and CI job conclusions inspected. No local install, test execution, live capture, container build or security audit.
- **Source discovery:** GitHub-first recursive lead from ArchiveBox; `research/2026-10-20-abx-dl-framework-independent-capture-runtime.md`.
- **Related projects:** ArchiveBox/ArchiveBox (already cataloged); ArchiveBox/abx-plugins, ArchiveBox/abxpkg, ArchiveBox/abxbus (recursive leads).
- **Caveats / risks:** Automatic dependency installation, third-party plugin execution and untrusted URL handling expand the attack surface; use `--no-install` where appropriate; browser cookies and downloaded files require isolation. Fast release cadence warrants version pinning.
- **Research notes:** The runtime is separate from ArchiveBox's Django UI/database. Upstream CI is not independent GitHub Gold testing. No third-party code copied.


### abxbus

- **Repository:** https://github.com/ArchiveBox/abxbus
- **Author / Org:** ArchiveBox / Nick Sweeting and contributors
- **Category:** Async event bus / cross-language automation / event-driven runtimes
- **Evidence:** VERIFIED — upstream release, source, tests and successful main CI; not independently executed
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Typed asynchronous event dispatch with nested event tracking, timeouts, concurrency controls and Python, TypeScript, Rust and Go implementations.
- **Why it is valuable:** Reusable event orchestration, structured results, cross-runtime contracts and optional IPC bridges independent of ArchiveBox.
- **Useful code/components:** `abxbus/event_bus.py`, `base_event.py`, `lock_manager.py`, `event_history.py`, `bridge_jsonl.py`, optional `bridge_{redis,nats,postgres,sqlite}.py`, `abxbus-ts/src/EventBus.ts`, `abxbus-rust/src/event_bus.rs`, `abxbus-go/event_bus.go`, cross-runtime tests.
- **Install / runtime:** Python >=3.11 (pip/uv); TypeScript Node/browser; Rust crate; Go >=1.25; optional backend extras.
- **Platforms:** Python, TypeScript Node/browser, Rust, Go.
- **License:** MIT root; review individual dependencies and optional transports.
- **Maintenance signals:** v2.5.77 released 2026-10-09; main CI run 37981912198 passed 120/120 jobs; docs CI passed 2026-10-20.
- **Verification performed:** README, license, source, tests, manifests, release and CI inspected. No independent build or execution.
- **Source discovery:** GitHub-first recursive lead from ArchiveBox/abx-dl.
- **Related projects:** ArchiveBox/abx-dl, ArchiveBox/abx-plugins, ArchiveBox/abxpkg, browser-use/bubus (historical origin).
- **Caveats / risks:** In-memory events are not durable by default; JSONL polling is not a transactional queue. Bridge reliability and cancellation require integration tests. Experimental `rust-core-ffi` branch CI failed 2026-10-12, distinct from passing main.
- **Research notes:** `research/2026-10-20-abxbus-cross-runtime-event-bus.md`. No upstream source copied.

### abxpkg

- **Repository:** https://github.com/ArchiveBox/abxpkg
- **Author / Org:** ArchiveBox / Nick Sweeting
- **Category:** Dependency management / package providers / Python CLI / binary-installation automation
- **Evidence:** VERIFIED — upstream release, source, tests and passing CI; not independently installed
- **Tier / Score:** S / 27 (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4)
- **What it does:** Python API and CLI that discovers, loads, installs, updates and executes binaries through multiple package-manager backends (env, apt, brew, pip, uv, npm, Docker and others).
- **Why it is valuable:** Reusable provider adapters, typed dependency declarations, version validation, cache/environment projection and package-installation lifecycle management across heterogeneous tools.
- **Useful code/components:** `abxpkg/binary.py` (Binary model); `abxpkg/binprovider.py` (provider abstraction and locks); `abxpkg/binprovider_{apt,brew,pip,uv,npm,docker,playwright,puppeteer,nix}.py` (adapters); `abxpkg/config.py` (cache identity); `abxpkg/semver.py`; `abxpkg/binary_service.py`; `abxpkg/cli.py`; `tests/test_security_controls.py`, `tests/test_provider_install_locks.py`.
- **Install / runtime:** `pip install abxpkg` or `uv tool install abxpkg`; Python >=3.12,<3.15; selected external package managers and optional privileges must exist for corresponding providers.
- **Platforms:** Linux/macOS; optional Docker and host package managers; Windows not established.
- **License:** MIT root LICENSE (Nick Sweeting 2024); installed third-party packages, providers and dependencies retain their own terms.
- **Maintenance signals:** Non-prerelease v1.13.58 published 2026-10-20; main Linux CI 39413598967 passed 30/30 jobs; scheduled macOS CI 39501442167 succeeded on its executed test jobs.
- **Verification performed:** README, license, manifest, provider modules, tests, workflow, release and job logs inspected. Earlier macOS CI 39444656035 failed one Deno test because Deno was missing; later scheduled Deno test passed. No independent installation, runtime test or supply-chain audit.
- **Source discovery:** GitHub-first recursive lead from ArchiveBox/abx-dl; `research/2026-10-20-abxpkg-provider-runtime-ci-failure-analysis.md`.
- **Related projects:** ArchiveBox/ArchiveBox, ArchiveBox/abx-dl, ArchiveBox/abx-plugins, ArchiveBox/abxbus.
- **Caveats / risks:** Runtime installers execute third-party code and may need elevated privileges; provider-specific `min_release_age` and `postinstall_scripts` controls **warn and continue** where unsupported, rather than fail closed. Pin, isolate and verify packages before deployment.
- **Research notes:** No upstream code copied. Upstream passing CI is not independent verification. Distinguish this package-provider runtime from abx-dl's capture orchestration.

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