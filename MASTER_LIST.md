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
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 4)
- **What it does:** Official firmware for the Meshtastic decentralized LoRa mesh network. Supports text messaging, location sharing, telemetry, and communication without cellular or internet infrastructure.
- **Why it is valuable:** Mature multi-platform firmware with active development, build/flashing instructions, tests/CI signals, and support for ESP32, nRF52, RP2040/RP2350, and Linux-class targets.
- **Useful code/components:** mesh routing; LoRa transport; position modules; packet handling; node database; telemetry; Wi-Fi/HTTP/TLS support; hardware variants.
- **Install / runtime:** Build from source or flash supported hardware with official Meshtastic tooling.
- **Platforms:** ESP32, nRF52, RP2040/RP2350, Linux.
- **License:** GPL-3.0.
- **Maintenance signals:** Latest GitHub non-prerelease v2.7.26.54e0d8d published 2026-06-24; develop CI succeeded 2026-10-21 (run 39633190319). A 2026-10-22 signing-policy commit postdates inspected CI.
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
- **Tier / Score:** A / 24 (Utility 5 + Working Evidence 2 + Reusability 4 + Novelty 5 + Documentation 5 + Maintenance 3)
- **What it does:** Multi-mode firmware for the Seeed Studio XIAO ESP32-S3. Its README documents BLE target detection, RSSI foxhunting, passive Wi-Fi observation, Wi-Fi PCAP, Remote ID monitoring, and passive BLE advertising capture.
- **Why it is valuable:** Combines several reusable embedded-radio ideas behind one small device and exposes browser flashing, dashboards, USB-CDC command protocols, packet capture, persistence, and modular firmware selection.
- **Useful code/components:** `src/mode_manager.cpp`, `src/mode_detector.cpp`, `src/mode_flockyou_promiscious.cpp`, `src/mode_blesniff.cpp`, `src/mode_pcap.cpp`
- **Install / runtime:** Browser flashing plus Python/esptool flashing are documented upstream.
- **Platforms:** Seeed Studio XIAO ESP32-S3 plus desktop/browser companion tooling.
- **License:** UNKNOWN — no root LICENSE found during inspection.
- **Maintenance signals:** Latest inspected source commit 2026-10-11 updated Mode 7 binary and web flasher. GitHub Pages deployment 38178185526 passed, but no firmware build/test workflow was found; no latest tagged release was available.
- **Verification performed:** Inspected README, PlatformIO manifest, src/ modes, shipped firmware, October commits, and Actions runs. No independent flashing or BLE/Wi-Fi test; passing Pages deployment does not verify firmware.
- **Source discovery:** GitHub-first discovery.
- **Related projects:** colonelpanichacks/flock-you; colonelpanichacks/ouispy-pcap; colonelpanichacks/ouispy-blesniff; colonelpanichacks/Oui-Spy-UniPwn.
- **Caveats / risks:** Root license UNKNOWN: do not copy source until permission is established. Device-identification signatures and RSSI can produce false positives; use only for authorized passive observation.
- **Research notes:** Upstream-only scoring audit: `research/2026-10-22-legacy-four-scoring-audit.md`. No third-party source copied.

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
- **Tier / Score:** A / 23 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 3 + Maintenance 3)
- **What it does:** Patches ADB and Fastboot so one Android device can debug another over USB from Termux without root using user-approved USB file descriptors.
- **Why it is valuable:** Demonstrates a reusable interoperability pattern combining Android USB permission APIs with Unix-domain-socket file-descriptor passing.
- **Useful code/components:** `install.sh` and `android-tools` submodule pointing to `nohajc/vendor-adb-patched` (USB FD bridging)
- **Install / runtime:** Requires Termux and Termux:API; upstream provides an install flow and apt repository.
- **Platforms:** Android / Termux.
- **License:** MIT at repository root; upstream Android tools/submodules have separate licenses.
- **Maintenance signals:** Latest inspected release v0.2.3 published 2025-09-09; latest commit 2026-03-13 modified install.sh. No GitHub Actions runs found.
- **Verification performed:** Inspected README, MIT root license, install.sh, android-tools submodule and release/commit history. No independent Android USB test or upstream automated test evidence found.
- **Source discovery:** Termux ecosystem pass.
- **Related projects:** termux/termux-api; termux/termux-packages; Android platform-tools.
- **Caveats / risks:** Documented curl-to-Bash installer adds a third-party APT repository and downloads its signing key without a pinned fingerprint in install.sh. Authenticate script and key before use; patched Android-tools submodule has separate licenses.
- **Research notes:** Upstream-only scoring audit: `research/2026-10-22-legacy-four-scoring-audit.md`. No third-party source copied.

### ESP32-S3 Remote ID Add-on (`esp-remoteid`)

- **Repository:** https://github.com/peinser/esp-remoteid
- **Author / Org:** Peinser BV / peinser
- **Category:** ESP32-S3 / OpenDroneID / embedded firmware / interoperability
- **Evidence:** PROMISING
- **Tier / Score:** A / 24 (Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 3 + Documentation 5 + Maintenance 3)
- **What it does:** ESP-IDF firmware for standards-based OpenDroneID / ASTM F3411 Remote ID broadcast over BLE and Wi-Fi with MAVLink input.
- **Why it is valuable:** Well-documented standards implementation built around `opendroneid-core-c`, with explicit transport behavior and flight-controller integration paths.
- **Useful code/components:** `src/remoteid/main.c`, `src/remoteid/remoteid/`, `tests/remoteid_test.py`, `components/opendroneid_core`, `.github/workflows/firmware.yml`
- **Install / runtime:** ESP-IDF environment with recursive submodules; build/flash/monitor workflow documented upstream.
- **Platforms:** ESP32-S3.
- **License:** Apache-2.0 at root; dependency licenses must also be preserved.
- **Maintenance signals:** v1.0.0 released 2026-05-15; main commit 2026-06-29. Upstream ESP-IDF v5.5 esp32s3 firmware-build CI run 28357049701 passed 2026-06-29; tests and RF operation were not exercised in that workflow.
- **Verification performed:** Inspected README, Apache-2.0 license, src/remoteid, components, tests and firmware.yml. Upstream compile succeeded; no independent build, receiver test or regulatory conformance test.
- **Source discovery:** OpenDroneID ecosystem branch.
- **Related projects:** opendroneid/opendroneid-core-c; opendroneid/receiver-android; ArduPilot/ArduRemoteID.
- **Caveats / risks:** Successful compilation does not establish ASTM F3411 radio interoperability, timing, identity correctness or legal compliance. Preserve dependency/submodule licenses and follow applicable aviation regulations.
- **Research notes:** Upstream-only scoring audit: `research/2026-10-22-legacy-four-scoring-audit.md`. No third-party source copied.

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
- **Related projects:** openzim/libzim; Kiwix readers; kiwix/kiwix-android; kiwix/kiwix-desktop; kiwix/kiwix-js; kiwix/kiwix-tools (offline search/serve/manage).
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
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Rust-based observability platform unifying logs, metrics, traces, dashboards, alerts, pipelines, real-user monitoring, and related analytics with OpenTelemetry ingestion.
- **Why it is valuable:** Demonstrates a modern self-hostable observability architecture around a single binary, columnar Parquet storage, object-store/S3 design, SQL/PromQL querying, and multi-signal workflows.
- **Useful code/components:** single-binary Rust server; OpenTelemetry ingestion; Parquet storage; S3-native persistence architecture; SQL/PromQL paths; logs/metrics/traces UI; alerting; pipelines/stream processing; multi-tenancy.
- **Inspected source paths:** `src/api/grpc/src/handler/grpc/request/otlp.rs`; `src/config/src/meta/otlp.rs`; `src/core/src/profiles/dictionary_compat.rs`.
- **Install / runtime:** Upstream documents a single Docker command for local startup plus HA/cloud-native deployment paths.
- **Platforms:** Linux, Docker, Kubernetes/cloud-native environments.
- **License:** AGPL-3.0.
- **Maintenance signals:** v1.1.2 released 2026-10-20 with upstream-reported PromQL, disk-cache, cluster-peer and Kubernetes query fixes. Inspected OTLP gRPC response handling and OTLP request-type unit tests. No independent deployment or benchmark.
- **Verification performed:** README, root AGPL-3.0 license, and same-day commit history inspected. GitHub Gold did not deploy or benchmark it; performance/cost claims in upstream README remain upstream claims, not independent verification.
- **Source discovery:** Independent observability pass.
- **Related projects:** OpenTelemetry ecosystem; Parquet/object-storage tooling; OpenObserve deployment integrations.
- **Caveats / risks:** AGPL-3.0 has network-use source-sharing implications for modified covered software; do not casually vendor code into differently licensed projects. Some enterprise features are separate from the open-source edition.
- **Research notes:** Prior provisional 29 reduced to 27: performance/cost claims not independently reproduced; AGPL and enterprise feature boundaries complicate reuse. See `research/2026-10-22-openobserve-loro-libp2p-maintenance.md`.

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
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Advanced Android package-management and diagnostics suite covering package/component inspection, manifests/signatures, tracker/library scanning, APK bundle workflows, backups, logcat, profiles, files, and terminal functionality.
- **Why it is valuable:** Consolidates many Android package-analysis and device-management capabilities behind explicit privilege layers, making it a useful architecture reference for non-root, ADB-assisted, and root-enhanced workflows.
- **Useful code/components:** `app/src/main/java/io/github/muntashirakon/AppManager/{apk,backup,scanner,adb,profiles,logcat,crypto}/`
- **Install / runtime:** Android application with optional ADB/root-enhanced capabilities.
- **Platforms:** Android.
- **License:** REUSE/SPDX model; primary application is documented GPL-3.0-or-later with additional file-level licenses.
- **Maintenance signals:** v4.1.1 published 2026-09-04; commits through 2026-10-19. Upstream Tests 39186829907, Lint 39186829863 and CodeQL 39186829827 all passed 2026-10-19.
- **Verification performed:** Inspected README, BUILDING.rst, REUSE/SPDX licensing, Java module tree and test workflow. Upstream Gradle unit tests, lint and CodeQL passed; no independent Android build, backup/restore or privileged-device test.
- **Source discovery:** Embedded/Android tooling pass.
- **Related projects:** Android package manager APIs, ADB, APK analysis and backup ecosystems.
- **Caveats / risks:** Primary app GPL-3.0-or-later with file-level SPDX exceptions; review each file and submodule before copying. Privileged operations can alter user data; use on owned devices with backups.
- **Research notes:** Upstream-only scoring audit: `research/2026-10-22-legacy-four-scoring-audit.md`. No third-party source copied.

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
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5; upstream evidence)
- **What it does:** Local cross-platform speech recognition implementation in C/C++.
- **Why it is valuable:** Embeddable C API and CPU/GPU backends for offline transcription.
- **Useful code/components:** include/whisper.h C API; src/whisper.cpp inference core; CLI and streaming examples; VAD and quantization tooling; Android iOS WASM Java and Docker examples; GPU and accelerator backend integrations; talk-llama speech-to-LLM example.
- **Install / runtime:** Build with CMake; obtain separately licensed model weights; run whisper-cli or link the C API.
- **Platforms:** Linux, Windows, macOS, Android, iOS, WebAssembly.
- **License:** MIT for the inspected root repository; third-party code and assets may differ.
- **Maintenance signals:** v1.9.5 published 2026-10-06; upstream CPU CI passed 5/5 jobs 2026-10-19 (run 39266836864). Android, Windows, WASM and VAD workflows also succeeded. A later model-vocabulary check is not assumed shipped in v1.9.5.
- **Verification performed:** README, license, upstream release and CI definitions inspected. No independent build, runtime test, or benchmark.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-local-ai-crdt.md
- **Related projects:** ggml-org/ggml; ggml-org/llama.cpp (shared ggml and talk-llama example); Whisper model ecosystem.
- **Caveats / risks:** MIT source licensing is permissive, but model weights and third-party dependencies/backends may have separate terms.
- **Research notes:** Promoted from READY queue; scoring remains provisional.

### Loro

- **Repository:** https://github.com/loro-dev/loro
- **Author / Org:** loro-dev
- **Category:** local-first / CRDT / collaborative state infrastructure
- **Evidence:** VERIFIED (upstream code, release and CI evidence; not independently executed)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 4)
- **What it does:** Conflict-free replicated data types for local-first collaborative application state.
- **Why it is valuable:** Reusable mergeable text, rich-text, tree, list and map structures, with delta synchronization and history.
- **Useful code/components:** Rust CRDT core; JavaScript/WASM loro-crdt package; Swift support; Fugue text and rich-text CRDTs; moveable tree and list CRDTs; delta synchronization APIs; shallow snapshots and time travel; Loro Inspector.
- **Inspected source paths:** `crates/loro-internal/src/container/richtext/fugue_span.rs`; `crates/loro/README.md`; `loro-js/README.md`.
- **Install / runtime:** Use the Rust crates, JavaScript/WASM package, or documented Swift integration.
- **Platforms:** Rust, JavaScript/WebAssembly, Swift.
- **License:** MIT for the inspected root repository; third-party code and assets may differ.
- **Maintenance signals:** Upstream loro-crdt@1.16.4 and experimental loro.js@0.3.0 released 2026-09-30. Source documents causally pending remote updates and convergence fixes; no independent cross-runtime tests.
- **Verification performed:** README, license, upstream release and CI definitions inspected. No independent build, runtime test, or benchmark.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-local-ai-crdt.md
- **Related projects:** loro-dev ecosystem, local-first applications, CRDT research.
- **Caveats / risks:** Root project is MIT licensed; optional ecosystem repositories and bindings should be checked separately before code reuse.
- **Research notes:** The pure TypeScript runtime is explicitly experimental; pending remote updates require careful checkpoint handling. See `research/2026-10-22-openobserve-loro-libp2p-maintenance.md`.

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
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 5)
- **What it does:** Composable Go implementation of the libp2p peer-to-peer networking stack.
- **Why it is valuable:** Reusable transport, peer identity, discovery and NAT traversal layers for resilient distributed applications.
- **Useful code/components:** host and network abstractions; transport composition; NAT traversal and hole punching; reachability and AutoNAT logic; peer identity and secure channel layers; stream multiplexing; protocol negotiation; connection management; examples; Grafana production dashboards.
- **Inspected source paths:** `p2p/protocol/holepunch/svc.go`; `p2p/host/autonat/autonat.go`; `p2p/protocol/autonatv2/autonat.go`.
- **Install / runtime:** Go module embedded in Go applications; network behavior depends on transport, NAT and deployment environment.
- **Platforms:** Go-supported systems, Linux, Windows, macOS.
- **License:** MIT at upstream root; dependencies/extensions require separate review.
- **Maintenance signals:** v0.50.0 released 2026-09-21 with upstream-reported reachability stress tests, hole-punch timeout fix and HTTP authentication hardening. Requires Go 1.26. No independent network test.
- **Verification performed:** README, root license and upstream commits inspected; no independent build, runtime, network, performance or security tests.
- **Source discovery:** GitHub-first discovery; research/2026-08-20-p2p-networking.md
- **Related projects:** libp2p specifications, go-libp2p examples, QUIC, WebTransport and AutoNAT.
- **Caveats / risks:** Root repository is MIT licensed, but dependencies, integrations, protocol implementations, and downstream projects may carry separate licenses and operational constraints.
- **Research notes:** NAT/firewall environments and relay availability affect actual connectivity; review transport dependency licenses. See `research/2026-10-22-openobserve-loro-libp2p-maintenance.md`.

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
- **Maintenance signals:** 0.13.5 published 2026-10-22 UTC (release notes dated 2026-10-21); updated managed CPython builds after 0.13.4 trust-root removal. Main CI succeeded 2026-10-22 (run 39720666204).
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
- **Related projects:** nushell/reedline; nushell/nushell.github.io; jqlang/jq (complementary JSON CLI; no integration asserted).
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

### SOPS

- **Repository:** https://github.com/getsops/sops
- **Author / Org:** getsops (CNCF Sandbox).
- **Category:** Structured encrypted configuration / GitOps / secrets management.
- **Evidence:** VERIFIED — upstream CI evidence; not independently security-audited.
- **Tier / Score:** S / 28 (Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 5; Maintenance 4).
- **What it does:** Encrypts YAML, JSON, ENV, INI and binary configuration using age, PGP and cloud key providers.
- **Why it is valuable:** Reusable format adapters, key-provider abstraction, multi-recipient policies and encrypted Git-friendly configuration.
- **Useful code/components:** `stores/` serialization adapters; `age/`, `pgp/` and KMS provider integrations; `keyservice/` gRPC; `shamir/` secret sharing; `audit/`.
- **Install / runtime:** Upstream binaries for Linux/macOS/Windows or Go source; supply keys or provider credentials.
- **Platforms:** Linux, macOS, Windows.
- **License:** MPL-2.0; file-level copyleft and attribution obligations.
- **Maintenance signals:** v3.13.3 released 2026-07-23; main CLI CI passed 17/17 jobs on 2026-10-20; recent commits through 2026-10-20.
- **Verification performed:** Inspected upstream README, license, source tree, release and GitHub Actions. No independent build, encryption/KMS test or security audit.
- **Source discovery:** GitHub-first; `research/2026-10-22-sops-mcuboot-promotion-evidence.md` and earlier SOPS component dossiers.
- **Related projects:** FiloSottile/age; getsops/community.
- **Caveats / risks:** Endpoint compromise, plaintext at runtime and cloud keyservice permissions remain relevant; CI does not prove cryptographic security.
- **Research notes:** No third-party implementation code copied.

### MCUboot

- **Repository:** https://github.com/mcu-tools/mcuboot
- **Author / Org:** mcu-tools.
- **Category:** Embedded secure boot / firmware signing / microcontroller updates.
- **Evidence:** VERIFIED — upstream simulator, firmware-tool and platform CI; not independently hardware-tested.
- **Tier / Score:** S / 29 (Utility 5; Working Evidence 5; Reusability 5; Novelty 5; Documentation 5; Maintenance 4).
- **What it does:** Portable authenticated bootloader and firmware-update framework for 32-bit microcontrollers.
- **Why it is valuable:** Security-sensitive image verification, update state machine, signing CLI and regression simulator are reusable across embedded platforms.
- **Useful code/components:** `boot/bootutil/` image verification and swap; `boot/boot_serial/` recovery; `scripts/imgtool.py` signing; `sim/` regression simulator; platform ports.
- **Install / runtime:** Integrate via board/RTOS bootloader support; configure flash layout, keys and update policy.
- **Platforms:** Zephyr, Mynewt, NuttX, Mbed, Espressif and Cypress/Infineon; RIOT boot target.
- **License:** Apache-2.0 plus NOTICE; review bundled cryptographic components separately.
- **Maintenance signals:** Stable v2.4.0 released 2026-04-23; source version bumped to 2.5.0 on 2026-10-22 but a new stable release was not confirmed. Main Sim CI passed 42/42 jobs 2026-10-22; imgtool, FIH, Zephyr and Espressif workflows passed.
- **Verification performed:** Inspected upstream README, license, NOTICE, source tree, release and Actions. No independent build, flashing, board-level testing or physical fault-injection audit.
- **Source discovery:** GitHub-first; `research/2026-10-22-sops-mcuboot-promotion-evidence.md` and earlier MCUboot dossier.
- **Related projects:** Zephyr, TinyCrypt, Mbed TLS.
- **Caveats / risks:** Trust anchors, anti-rollback, debug lock and flash geometry require board-specific validation. Feature-branch CI failures should not be conflated with main.
- **Research notes:** No third-party implementation code copied.

### PMTiles

- **Repository:** https://github.com/protomaps/PMTiles
- **Author / Org:** Protomaps
- **Category:** Offline mapping / geospatial / single-file tile archives / serverless maps
- **Evidence:** VERIFIED — upstream source/CI, not independent execution
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 3)
- **What it does:** Open Version 3 tile archive format and cross-runtime readers. The 127-byte header and root index within 16 KiB support efficient HTTP byte-range access.
- **Why it is valuable:** Enables offline or static-object-hosted maps without a dedicated tile database; provides formal spec and reusable JavaScript, Python, C++, OpenLayers and serverless implementations.
- **Useful code/components:** `spec/v3/spec.md`; `js/src/index.ts`; `js/src/adapters.ts`; `python/pmtiles`; `python/rio-pmtiles`; `cpp/`; `openlayers/`; `serverless/aws/`; `serverless/cloudflare/`.
- **Install / runtime:** Use npm/PyPI reference readers or companion go-pmtiles CLI; remote archives need HTTP Range and suitable CORS.
- **Platforms:** Browser/Node.js, Python, C++, OpenLayers, AWS Lambda, Cloudflare Workers.
- **License:** BSD-3-Clause implementation code; spec public domain/CC0; sample and generated map data separate.
- **Maintenance signals:** Latest inspected main commit 2026-09-16 (Python pmtiles 3.8.1); 2026-10-19 PR CI run 39281511827 passed build_app and test. No root GitHub Releases; packages published separately.
- **Verification performed:** README, LICENSE, V3 spec, CI and source structure inspected; upstream PR tests passed. No independent archive, range-read, browser or security tests.
- **Source discovery:** GitHub-first offline-mapping ecosystem; `research/2026-09-05-protomaps-pmtiles-single-file-offline-map-archive.md` and `research/2026-10-22-pmtiles-go-pmtiles-promotion.md`.
- **Related projects:** protomaps/go-pmtiles; MapLibre; Planetiler; Protomaps Basemaps.
- **Caveats / risks:** Range/CORS and untrusted archive parsing require validation. Large-object corruption or replacement affects a whole map. Map-data licenses independent. CI uses mutable Action tags.
- **Research notes:** No third-party implementation code or map data copied.

### go-pmtiles

- **Repository:** https://github.com/protomaps/go-pmtiles
- **Author / Org:** Protomaps
- **Category:** Offline mapping / Go CLI / archive conversion, verification, HTTP serving and cloud storage
- **Evidence:** VERIFIED — upstream source/CI, not independent execution
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 4 + Maintenance 5)
- **What it does:** Go CLI and package for inspecting, converting, extracting, clustering, verifying, serving and uploading PMTiles archives, with experimental differential sync.
- **Why it is valuable:** Practical local-to-cloud archive lifecycle for portable/offline maps and reproducible geospatial delivery.
- **Useful code/components:** `main.go` CLI; `pmtiles/verify.go` structural checks; `pmtiles/extract.go`, `region.go` geographic extraction; `pmtiles/server.go` HTTP; `pmtiles/bucket.go` storage abstraction; `pmtiles/directory.go` indexing; `pmtiles/sync.go` experimental range sync.
- **Install / runtime:** Download upstream binaries or build with Go; `go test ./pmtiles` is documented. Remote object stores need credentials and compatible range handling.
- **Platforms:** Linux, Windows, macOS binaries; Go library; S3, GCS, Azure and local storage.
- **License:** BSD-3-Clause; map archive contents independently licensed.
- **Maintenance signals:** Stable v1.31.2 published 2026-07-22, fixing Content-Length for tile responses. 2026-10-06 PR CI run 37488026517 passed Linux/Windows tests and lint; separate publish Docker workflow 37488026722 failed.
- **Verification performed:** Inspected README, LICENSE, main.go, verify.go, sync.go, tests and CI; no independent archive, server, object-storage or sync execution.
- **Source discovery:** Recursive PMTiles research; `research/2026-09-06-go-pmtiles-operational-cli-range-sync-server.md` and `research/2026-10-22-pmtiles-go-pmtiles-promotion.md`.
- **Related projects:** protomaps/PMTiles; Planetiler; MapLibre; Protomaps Basemaps.
- **Caveats / risks:** `verify` is structural, not cryptographic or payload integrity; some anomalies are logged without failing. `serve` defaults to `0.0.0.0`. Differential sync is explicitly experimental.
- **Research notes:** No third-party implementation code or map data copied.

### marimo

- **Repository:** https://github.com/marimo-team/marimo
- **Author / Org:** marimo-team
- **Category:** Reactive Python notebooks / scientific computing / interactive data apps / developer tooling
- **Evidence:** VERIFIED — upstream source, release and CI; no independent execution
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Reactive Python notebooks stored as executable, version-control-friendly Python files; automatically re-executes dependent cells or marks them stale and supports SQL, UI widgets, scripts, apps and browser/Pyodide execution.
- **Why it is valuable:** Reproducible, composable scientific and analytical workflows without opaque notebook JSON; reusable runtime, reactive graph, SQL, widget and export components.
- **Useful code/components:** `marimo/_runtime/dataflow/` dependency tracking; `marimo/_runtime/executor/` execution; `marimo/_sql/` SQL; `marimo/_plugins/` UI widgets; `marimo/_export/` exports; `marimo/_pyodide/` WASM; `marimo/_server/` HTTP service; `marimo/_mcp/` agent interfaces.
- **Install / runtime:** Python >=3.10; `pip install marimo` then `marimo tutorial intro`; SQL, sandbox and AI integrations have optional dependencies.
- **Platforms:** Linux, Windows, macOS, browser via Pyodide/WASM.
- **License:** Apache-2.0; review bundled third-party notices/assets before copying.
- **Maintenance signals:** v0.25.2 released 2026-10-19; main CI 2026-10-22: backend run 39859957455 passed 18 jobs (docs skipped), frontend 39859957465 passed 4/4, Playwright 39859957692 passed 2/2.
- **Verification performed:** Inspected README, pyproject, license, source layout, releases and upstream CI results; no independent notebook execution or security review.
- **Source discovery:** GitHub-first; `research/2026-09-30-marimo.md` and `research/2026-10-22-marimo-probe-rs-promotion.md`.
- **Related projects:** marimo-team/marimo-lsp; marimo-team/vscode-marimo; DuckDB; Loro; uv.
- **Caveats / risks:** Notebook execution runs arbitrary Python and needs normal trust boundaries. As of 2026-10, native Loro dependency excludes Python 3.15 in `pyproject.toml`; do not infer identical collaboration behavior on all supported interpreters. Third-party assets may carry separate notices.
- **Research notes:** No upstream code copied; prioritize runtime dependency graph, SQL isolation, and browser/native feature parity.

### probe-rs

- **Repository:** https://github.com/probe-rs/probe-rs
- **Author / Org:** probe-rs
- **Category:** Embedded debugging / SWD-JTAG / firmware flashing / Rust libraries / hardware test infrastructure
- **Evidence:** VERIFIED — upstream source, release, CI and hardware smoke-test jobs; no independent device test
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Rust libraries and CLI for embedded debug probes, MCU memory/register access, flashing, GDB and Debug Adapter Protocol integration across supported Arm, RISC-V and Xtensa targets.
- **Why it is valuable:** Modular transports, target descriptions, flashing engines, remote RPC and real hardware test infrastructure; useful for interoperability and authorized board development.
- **Useful code/components:** `probe-rs/src/probe/` transports; `probe-rs/src/architecture/` CPU support; `probe-rs/src/flashing/` loaders; `probe-rs-target/` chip metadata; `probe-rs-debug/` DAP; `probe-rs-rpc/` and `probe-rs-rpc-client/` remote API; `probe-rs-linux/` GPIO/spidev SWD; `smoke-tester/` hardware harness.
- **Install / runtime:** Upstream CLI binaries or Rust workspace (minimum Rust 1.95); physical probe and compatible MCU normally required; Linux GPIO/spidev backend is hardware-specific.
- **Platforms:** Linux, Windows, macOS hosts; Arm/RISC-V/Xtensa embedded targets where supported.
- **License:** MIT OR Apache-2.0 workspace; external CMSIS packs and flash algorithms may differ.
- **Maintenance signals:** Stable v0.32.0 published 2026-07-22; master 2026-10-22 Run CI 39849611123 passed 12/12 jobs; Run smoke test 39849610977 passed 5/5 including two named hardware-runner jobs and embedded-test.
- **Verification performed:** Inspected README, workspace manifest, MIT license, source tree, release and CI jobs. Upstream hardware tests are not independent GitHub Gold tests.
- **Source discovery:** GitHub-first; `research/2026-10-08-probe-rs-embedded-debugging-flashing-toolkit.md` and `research/2026-10-22-marimo-probe-rs-promotion.md`.
- **Related projects:** probe-rs/vscode; probe-rs/embedded-test; pyOCD; esptool; MCUboot.
- **Caveats / risks:** Flash erase can permanently overwrite data or brick targets. Probe and MCU support varies. Remote RPC can expose sensitive debug operations. Verify external target-pack/flash-algorithm licensing before reuse.
- **Research notes:** No upstream code copied; compare DAP/GDB behavior with pyOCD and independently validate supported boards before production claims.

### Iroh

- **Repository:** https://github.com/n0-computer/iroh
- **Author / Org:** n0-computer
- **Category:** P2P networking / QUIC / NAT traversal / Rust / local-first infrastructure
- **Evidence:** VERIFIED — upstream source, release and CI; not independently network-tested
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 5 + Documentation 4 + Maintenance 5)
- **What it does:** Public-key-addressed QUIC connections with direct path selection, hole punching, relay fallback and protocol composition.
- **Why it is valuable:** Reusable transport for sync, messaging, edge and mobile software; self-hostable relay and discovery components.
- **Useful code/components:** `iroh/src/endpoint.rs`, `endpoint/`, `address_lookup/`, `portmapper.rs`, `protocol.rs`, `net_report/`; `iroh-relay/`, `iroh-base/`, `iroh-dns-server/`.
- **Install / runtime:** Rust crate/workspace; upstream CI MSRV 1.91; configure discovery and relay policy.
- **Platforms:** Linux, Windows, macOS, Android, browser/Wasm build targets (feature parity not established).
- **License:** MIT OR Apache-2.0; ecosystem licenses need separate review.
- **Maintenance signals:** v1.4.1 published 2026-10-22; main CI 39805786602 passed 28/28 jobs (desktop, Android, Wasm, netsim and cross-build); recent relay handshake leak fix.
- **Verification performed:** README, licenses, source layout, releases, commits and upstream CI inspected. No independent NAT, relay, battery, performance or crypto testing.
- **Source discovery:** GitHub-first GuardianDB ecosystem; `research/2026-09-30-iroh-key-addressed-p2p-quic.md` and `research/2026-10-22-iroh-satdump-promotion.md`.
- **Related projects:** iroh-blobs; iroh-gossip; iroh-docs; iroh-ffi; noq; go-libp2p.
- **Caveats / risks:** Relays/discovery may expose metadata. Real NAT and datagram path behavior varies; upstream reports some edge cases.
- **Research notes:** No source copied. Investigate relay trust, NAT reliability and Android idle-power consumption.

### SatDump

- **Repository:** https://github.com/SatDump/SatDump
- **Author / Org:** SatDump
- **Category:** SDR / satellite data / offline DSP / weather imagery / scientific tools
- **Evidence:** VERIFIED — upstream source and partial CI success; no independent reception/decoder test
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 5)
- **What it does:** GUI/CLI pipeline system for live satellite SDR reception or offline baseband processing, decoding and image/data products.
- **Why it is valuable:** Broad modular DSP and decoder stack with offline use and cross-platform packaging.
- **Useful code/components:** `src-core/dsp/`, `src-core/pipeline/`, `src-core/products/`, `src-core/image/`, `src-core/projection/`, `src-cli/`, `src-ui/`, `plugins/`, `src-testing/`.
- **Install / runtime:** CMake and optional SDR/acceleration libraries; recorded input works without SDR hardware; live reception requires drivers/device.
- **Platforms:** Linux, Windows, macOS, Android.
- **License:** GPL-3.0; third-party drivers and satellite data may have separate terms.
- **Maintenance signals:** Latest numbered stable 1.2.2 (2024-11-29); active 2026-10-22 IERS fix. Build All 39809901226: 5 jobs succeeded, 3 failed, 1 skipped; macOS SDRPlay dependency download invalid ZIP, ARM64 compiler killed.
- **Verification performed:** README, license, source tree, release, commits, upstream CI and failing logs inspected. No independent build, radio, decoder or imagery tests.
- **Source discovery:** GitHub-first SDR ecosystem; `research/2026-09-29-satdump-satellite-sdr-processing.md` and `research/2026-10-22-iroh-satdump-promotion.md`.
- **Related projects:** GNU Radio; SoapySDR; RTL-SDR; HackRF; weather-satellite processing.
- **Caveats / risks:** CI partly failing; stable tag older than current development. Build success does not prove decoder correctness; radio operation and data use have separate obligations.
- **Research notes:** No source copied. Prioritize ARM64/macOS CI and recorded-IQ regression fixtures.

### Zephyr RTOS

- **Repository:** https://github.com/zephyrproject-rtos/zephyr
- **Author / Org:** Zephyr Project
- **Category:** Embedded RTOS / hardware abstraction / device drivers / Bluetooth / networking / test automation
- **Evidence:** VERIFIED — upstream release, source and passing CI; not independently hardware-tested
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Configurable real-time OS for resource-constrained devices, with multi-architecture kernel, board descriptions, drivers, protocol stacks and test infrastructure.
- **Why it is valuable:** Extensive reusable embedded architecture; Kconfig, devicetree, west, and Twister support portable and testable firmware across many targets.
- **Useful code/components:** `kernel/`, `drivers/`, `subsys/`, `include/zephyr/`, `boards/`, `soc/`, `dts/`, `scripts/twister`, `scripts/pylib/twister/`, `west.yml`, `samples/`, `tests/`.
- **Install / runtime:** west workspace and Zephyr SDK/toolchains; supported board, target-specific drivers and flashing/debug hardware as applicable.
- **Platforms:** Arm, RISC-V, x86, Xtensa, ARC and other documented architectures; host build support depends on SDK/toolchain.
- **License:** Apache-2.0 project; imported modules/HALs and some individually licensed files have separate SPDX terms.
- **Maintenance signals:** Stable v4.4.2 published 2026-08-07 with security fixes; 2026-10-22 main commit prepared v4.5.0-rc3 (not a stable release). 2026-10-22 main Twister 39835122032, CodeQL 39835121878 and docs 39835121990 completed successfully.
- **Verification performed:** Upstream README, source tree, west manifest, LICENSE, REUSE license guidance, release, commits and GitHub Actions inspected. No independent build, board flashing or security audit.
- **Source discovery:** GitHub-first; `research/2026-09-07-zephyr-rtos-embedded-kernel-hardware-test-platform.md` and `research/2026-10-23-zephyr-zellij-promotion.md`.
- **Related projects:** west; BabbleSim; MCUboot; ESPHome; RadioLib; probe-rs; `zmkfirmware/zmk` (ZMK pins a separate Zephyr fork).
- **Caveats / risks:** Security advisories affect multiple kernel/protocol paths; CI does not establish all board combinations work. Imported modules may not inherit the root license.
- **Research notes:** No third-party code copied. Prioritize Twister sharding and devicetree/driver generation as reusable architectural studies.

### Zellij

- **Repository:** https://github.com/zellij-org/zellij
- **Author / Org:** zellij-org
- **Category:** Terminal multiplexer / Rust / developer workspace / WebAssembly plugins / terminal automation
- **Evidence:** VERIFIED — upstream source, release and passing CI; no independent session or web-client testing
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Terminal workspace with persistent sessions, programmable layouts, pane management, collaboration, web client and Wasm plugins.
- **Why it is valuable:** Composable terminal operations, remote workspaces and a reusable Rust client/server plus WebAssembly plugin architecture.
- **Useful code/components:** `zellij-client/`, `zellij-server/`, `zellij-utils/`, `zellij-tile/`, `zellij-tile-utils/`, `default-plugins/`, `xtask/`, `zellij-integration-tests/`, layout assets.
- **Install / runtime:** Prebuilt release binaries or Cargo source build; main workspace Rust >=1.95. Browser-client availability depends on build/configuration.
- **Platforms:** Linux, macOS, Windows (upstream CI); browser client where enabled.
- **License:** MIT; review third-party assets and plugin dependencies separately.
- **Maintenance signals:** Stable v0.45.1 released 2026-08-28; main Cargo workspace v0.46.0 is development, not stable. 2026-10-22 main Rust CI 39811852472 passed 12/12 jobs; end-to-end 39811852673 passed 1/1. Main commits include session renaming and memory optimizations.
- **Verification performed:** README, MIT license, Cargo workspace, source layout, releases, commits, upstream CI jobs inspected. No independent install, terminal-session tests or plugin security audit.
- **Source discovery:** GitHub-first; `research/2026-09-09-zellij-terminal-workspace-wasm-plugin-platform.md` and `research/2026-10-23-zephyr-zellij-promotion.md`.
- **Related projects:** Rust Cargo; WebAssembly plugin ecosystem; tmux; SSH; Nushell.
- **Caveats / risks:** Browser terminal and collaborative sessions require careful authentication and network-exposure controls. Wasm plugins require capability-boundary review; CI contains some mutable action tags.
- **Research notes:** No third-party code copied. Next investigate plugin host permissions, web-client exposure defaults and reproducible release builds.



### Zarr Python

- **Repository:** https://github.com/zarr-developers/zarr-python
- **Author / Org:** Zarr Developers
- **Category:** Scientific computing / chunked array storage / object stores / Python / large datasets
- **Evidence:** VERIFIED — upstream source, release and CI; no independent execution
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Implements compressed, chunked N-dimensional arrays, Zarr metadata, storage backends, and optional separately packaged lazy indexing and HTTP serving.
- **Why it is valuable:** Fine-grained access to large arrays, reusable storage and codec abstractions, object-store interoperability, lazy indexing and modular scientific data services.
- **Useful code/components:** `src/zarr/core/array.py`, `src/zarr/core/codec_pipeline.py`, `src/zarr/core/chunk_grids.py`, `src/zarr/storage/_fsspec.py`, `src/zarr/storage/_obstore.py`, `packages/zarr-indexing/`, `packages/zarr-http-server/`, `packages/zarr-metadata/`.
- **Install / runtime:** Python >=3.12; install via Python package tooling; NumPy and numcodecs dependencies; optional fsspec/obstore and HTTP service dependencies.
- **Platforms:** Python on Linux, macOS, Windows; supported object stores with backend adapters.
- **License:** MIT (root and inspected indexing subpackage); inspect optional codec/backend/data licenses separately.
- **Maintenance signals:** Stable v3.4.1 published 2026-10-08; source activity 2026-10-22. Upstream 2026-10-23 Test workflow 39892893049 passed 16/16 jobs; Slow Hypothesis 39892893145 passed 1/1 (PR workflows, not independent tests).
- **Verification performed:** Inspected upstream README/package manifests, license, source layout, subpackage docs, release notes and workflow results; no local installation, dataset I/O, concurrency, cloud or security test.
- **Source discovery:** GitHub-first; `research/2026-09-06-zarr-python-chunked-array-storage-indexing-stack.md`.
- **Related projects:** earth-mover/icechunk; zarr-developers/zarr-specs; zarr-developers/numcodecs; xarray; Dask; TensorStore.
- **Caveats / risks:** Core Zarr is not a transactional database; chunk sizing, backend consistency and cloud costs matter. Experimental `zarr-http-server` is read-only by default; `store_app` exposes all keys and enabling writes requires independent access controls.
- **Research notes:** `research/2026-10-23-zarr-soapysdr-promotion.md`; no upstream code copied. Prioritize HTTP authorization boundaries and sharded partial-write correctness.

### SoapySDR

- **Repository:** https://github.com/pothosware/SoapySDR
- **Author / Org:** Pothosware
- **Category:** SDR / hardware abstraction / portable device APIs / C++ / interoperability
- **Evidence:** VERIFIED — upstream cross-platform build, null-device tests and plugin CI; no physical radio test
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** Vendor-neutral SDR device discovery, configuration and sample streaming through a C++ API, C wrapper and dynamically loadable hardware modules.
- **Why it is valuable:** Separates DSP applications from hardware SDKs and offers reusable device capabilities, stream APIs, sample converters, language bindings and driver plugin architecture.
- **Useful code/components:** `include/SoapySDR/Device.hpp`, `include/SoapySDR/Device.h`, `include/SoapySDR/ConverterRegistry.hpp`, `include/SoapySDR/Modules.hpp`, `include/SoapySDR/Registry.hpp`, `apps/`, `ExampleDriver/`, `swig/`, `luajit/`.
- **Install / runtime:** CMake and C++11; build from source or platform packages; optional SWIG/Python and LuaJIT bindings; hardware requires separately installed Soapy driver plugins and vendor libraries.
- **Platforms:** Linux, macOS, Windows (upstream CI); actual device support depends on drivers.
- **License:** Boost Software License 1.0; inspect individual drivers, vendor SDKs and firmware separately.
- **Maintenance signals:** Source Changelog declares 0.9.0 dated 2026-10-10 and CMake derives version from it; GitHub Releases API returned no published release object. Upstream CI 38058033433 passed 36/36 jobs and cross-compile CI 38058033417 passed 15/15 on 2026-10-10.
- **Verification performed:** Inspected source header tree, README, license, changelog, CMake and CI results. Null-device and example-driver tests are upstream evidence, not independent hardware streaming validation.
- **Source discovery:** GitHub-first; `research/2026-09-11-soapysdr-vendor-neutral-sdr-hardware-abstraction.md`.
- **Related projects:** pothosware/SoapyRemote; SoapyRTLSDR; `gnuradio/gnuradio` (in-tree `gr-soapy` adapter; no RF hardware validation); SatDump; `AlexandreRouma/SDRPlusPlus` (SDR++ Soapy source plugin); `merbanan/rtl_433` (SoapySDR receiver input; RF not independently tested).
- **Caveats / risks:** A passing null-device/plugin test does not prove any particular SDR device works. Vendor driver licenses and remote device access controls vary. GitHub Release metadata does not independently confirm the changelog's 0.9.0 label.
- **Research notes:** `research/2026-10-23-zarr-soapysdr-promotion.md`; no upstream code copied. Prioritize sample-format converter edge cases and SoapyRemote authentication/exposure review.

### Icechunk

- **Repository:** https://github.com/earth-mover/icechunk
- **Author / Org:** Earthmover
- **Category:** Scientific computing / transactional Zarr storage / object storage / data versioning / Rust / Python
- **Evidence:** VERIFIED — upstream Python tests and source-level inspection; no independent storage tests
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Transactional, versioned object-storage engine for Zarr arrays; provides atomic committed snapshots, branches, tags, concurrent-write conflict detection and virtual chunk references.
- **Why it is valuable:** Adds snapshot consistency and conflict-aware multi-writer updates to chunked scientific datasets, with reusable Rust storage/format crates and Python integration.
- **Useful code/components:** `icechunk-format/` snapshot/manifest encodings; `icechunk-storage/` storage traits; `icechunk-arrow-object-store/` and `icechunk-s3/` backends; `icechunk/src/repository.rs`, `session.rs`, `conflicts/`, `virtual_chunks.rs`, `cli/`; `icechunk-python/` PyO3 bindings; `icechunk-js/` client.
- **Install / runtime:** Python >=3.12 and Zarr Python >=3.1; Rust v2.3.0 requires Rust >=1.95 for source builds. Backend-specific cloud credentials and dependencies as applicable.
- **Platforms:** Python/Rust on supported Linux/macOS/Windows targets; local and cloud object stores.
- **License:** Apache-2.0 root; inspect dependencies and external datasets separately.
- **Maintenance signals:** v2.3.0 released 2026-10-06. Upstream Python Check 39895350092 succeeded 2026-10-23; separate Python CI/release 39898974564 failed on several legacy support/v1.x Python 3.15t wheel jobs.
- **Verification performed:** README, license, source structure, changelog, package requirements, release and CI job results inspected. No independent installation, storage transaction, concurrency or cloud test.
- **Source discovery:** GitHub-first recursive Zarr Python follow-up; existing `research/2026-09-06-icechunk-transactional-zarr-object-storage-versioning.md`.
- **Related projects:** zarr-developers/zarr-python; Apache Arrow object_store; xarray; Dask; Kerchunk.
- **Caveats / risks:** Serializable transaction guarantees require backend conditional-write semantics; garbage collection, branch reset and external virtual references need rigorous validation. Legacy wheel build failures limit packaging confidence.
- **Research notes:** `research/2026-10-23-icechunk-soapyremote-promotion.md`. No source copied. Prioritize conflict/GC state-model testing and cloud-backend conditional-write behavior.

### SoapyRemote

- **Repository:** https://github.com/pothosware/SoapyRemote
- **Author / Org:** Pothosware
- **Category:** Software-defined radio / remote device control / RPC / streaming / hardware interoperability
- **Evidence:** VERIFIED — upstream cross-platform build/module-registration CI; no end-to-end stream or radio test
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 3 + Maintenance 4)
- **What it does:** Exports SoapySDR-compatible devices across a network using a remote SoapySDR client plugin, control-plane RPC and configurable UDP/TCP sample streaming.
- **Why it is valuable:** Reuses the existing SoapySDR device API for headless receivers and LAN-attached SDR hardware; its separated RPC, discovery, transport and device-adapter layers are useful components.
- **Useful code/components:** `client/Streaming.cpp` sample format/MTU/window negotiation; `client/DiscoverServers.cpp` service discovery; `client/Registration.cpp` SoapySDR plugin; `server/ClientHandler.cpp` RPC dispatcher; `server/SoapyServer.cpp` and `ServerListener.cpp`; `common/SoapyRemoteDefs.hpp` protocol definitions; `common/` sockets and framing.
- **Install / runtime:** Build with CMake and compatible SoapySDR; remote server and client need network connectivity; hardware requires appropriate SoapySDR plugins/vendor libraries.
- **Platforms:** Linux, macOS, Windows and FreeBSD upstream build matrix.
- **License:** Boost Software License 1.0; driver and vendor SDK terms vary.
- **Maintenance signals:** 2026-09-29 remote-call safety fix, 2026-10-05 CI refresh, v0.5.3 in changelog dated 2026-10-10; upstream CI 38059816370 and 38059814840 succeeded. No GitHub Release object found.
- **Verification performed:** Inspected README, root license, changelog, source layout, RPC definitions and CI jobs. No independent SDR hardware, remote control, sample-stream or security tests.
- **Source discovery:** GitHub-first recursive follow-up from SoapySDR; existing `research/2026-09-05-soapyremote-network-transparent-sdr-transport.md`.
- **Related projects:** pothosware/SoapySDR; SoapyRTLSDR; GNU Radio; SatDump; SDR++.
- **Caveats / risks:** Default server port 55132; documented server binding may expose radio control beyond a trusted LAN. Inspected stock path did not establish TLS/client authentication; use external access controls. Passing module-registration CI does not prove sample transport works.
- **Research notes:** `research/2026-10-23-icechunk-soapyremote-promotion.md` and `research/2026-08-29-soapyremote-network-trust-boundary.md`. No source copied. Prioritize safe loopback streaming and RPC authorization boundaries.

### NVDA

- **Repository:** https://github.com/nvaccess/nvda
- **Author / Org:** NV Access
- **Category:** Accessibility / Windows screen reader / speech / braille / UI automation
- **Evidence:** VERIFIED — upstream Windows build, unit and system CI; no independent installation
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Open-source Windows screen reader with speech and braille output, browser accessibility, add-ons and application-specific accessibility adapters.
- **Why it is valuable:** Mature, tested interoperability architecture for Windows UI Automation, IAccessible, ARIA/browser navigation, braille hardware and speech drivers.
- **Useful code/components:** `source/UIAHandler/`, `source/IAccessibleHandler/`, `source/NVDAObjects/`, `source/speech/`, `source/braille/`, `source/brailleDisplayDrivers/`, `source/addonHandler/`, `source/_remoteClient/`, `tests/system/`.
- **Install / runtime:** Official Windows installer for end users; source build uses SCons/Windows toolchain and `pyproject.toml` requires Python >=3.13,<3.14. Windows-only.
- **Platforms:** Windows; upstream CI builds Windows x64 and runs installer/browser system tests.
- **License:** GPL-2.0-or-later with two special project exceptions in `copying.txt`; bundled libraries have separate licenses.
- **Maintenance signals:** Stable release `release-2026.2` published 2026-08-31; master commit `40e2df64cd` dated 2026-10-21. Upstream master CI 39544741209 passed 37 jobs with 4 skipped on 2026-10-21. A separate 2026-10-23 PR CI failed; do not generalize that failure to master.
- **Verification performed:** Inspected root license, Python requirements, source layout, release, commits and upstream CI job results. No independent screen-reader, braille, installer, accessibility or security tests.
- **Source discovery:** GitHub-first accessibility rotation; `research/2026-09-12-nvda-windows-screen-reader-accessibility-platform.md`.
- **Related projects:** Microsoft UI Automation, NVDA add-on ecosystem, Windows accessibility APIs.
- **Caveats / risks:** GPL exceptions and third-party licenses require file-level review; add-ons and remote-access components create separate trust boundaries. Windows-only; passing CI does not prove all applications are accessible.
- **Research notes:** `research/2026-10-23-nvda-libzim-promotion.md`. No third-party code copied.

### libzim

- **Repository:** https://github.com/openzim/libzim
- **Author / Org:** openZIM
- **Category:** Offline knowledge / ZIM archives / C++ library / search / content packaging
- **Evidence:** VERIFIED — upstream cross-platform CI and source inspection; no independent archive test
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 5)
- **What it does:** Reference C++ implementation for reading, writing and searching ZIM offline-content archives.
- **Why it is valuable:** Reusable archive-format APIs for offline reference libraries, education, disaster-preparedness and disconnected applications; complements existing operational `openzim/zim-tools` entry.
- **Useful code/components:** `include/zim/archive.h`, `entry.h`, `item.h`, `blob.h`, `search.h`, `suggestion.h`, `writer/`; `test/` and external `openzim/zim-testing-suite`.
- **Install / runtime:** C++17, Meson/Ninja, liblzma, ICU, Zstd; Xapian optional for search. Some test cases require high memory; cross-target builds have different feature flags.
- **Platforms:** Linux, macOS, Windows; upstream build matrix includes Android, iOS and WebAssembly targets.
- **License:** GPL-2.0-or-later per upstream README/COPYING; check individual dependencies and packaging obligations.
- **Maintenance signals:** Stable release 9.8.2 published 2026-08-13; 2026-10-19 merged random-entry off-by-one fix. Upstream main CI 39279529888 passed all 23 jobs on 2026-10-19; cross-compilation does not imply on-device runtime testing.
- **Verification performed:** Inspected README, root license declaration, Meson configuration, public headers, recent commits, release and upstream CI job outcomes. No independent parsing, writing, search, fuzz or performance tests.
- **Source discovery:** GitHub-first recursive research from existing `openzim/zim-tools`; `research/2026-09-13-libzim-zim-offline-archive-library.md`.
- **Related projects:** openzim/zim-tools, openzim/zim-testing-suite, Kiwix readers; `kiwix/java-libkiwix` (Android JNI binding); `kiwix/kiwix-tools` (offline ZIM search/serve/manage).
- **Caveats / risks:** GPL copyleft affects embedding; optional Xapian changes available APIs; hostile ZIM files may present parser/decompression/resource-exhaustion risks requiring further testing.
- **Research notes:** `research/2026-10-23-nvda-libzim-promotion.md`. No third-party code copied.


### OpenTelemetry Collector

- **Repository:** https://github.com/open-telemetry/opentelemetry-collector
- **Author / Org:** OpenTelemetry / CNCF ecosystem
- **Category:** Observability / Go / traces / metrics / logs / extensible telemetry pipelines
- **Evidence:** VERIFIED — upstream source and CI; no independent deployment
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Vendor-neutral, configurable receivers → processors → exporters pipeline for logs, metrics and traces.
- **Why it is valuable:** Modular Go framework for agents, gateways, custom collectors and resilient telemetry delivery; separates data-plane interfaces from runtime orchestration.
- **Useful code/components:** `receiver/`, `processor/`, `exporter/exporterhelper/` (queues, batching, retry), `service/pipelines/`, `confmap/`, `config/`, `pdata/`, `cmd/`.
- **Install / runtime:** Go 1.26.0 declared in core `go.mod`; official binary distribution is built using `open-telemetry/opentelemetry-collector-releases`, not the root module alone. Configuration is mandatory.
- **Platforms:** Go cross-builds cover Linux, macOS, Windows and several additional targets; successful cross-compilation is not runtime verification on every OS.
- **License:** Apache-2.0; retain notices and attribution for reused code.
- **Maintenance signals:** Latest inspected stable GitHub release v0.163.0 (2026-10-14). On 2026-10-23, upstream main `build-and-test` run 40012185839 passed 24 jobs, skipped one; main CodeQL, ARM, Windows and builder integration workflows also passed.
- **Verification performed:** Inspected README, LICENSE, `go.mod`, source trees, security guidance, release and CI job results. No independent Go build, telemetry capture, network test or security audit.
- **Source discovery:** GitHub-first observability research; prior dossier `research/2026-09-01-opentelemetry-collector-modular-observability-pipeline.md`.
- **Related projects:** `open-telemetry/opentelemetry-collector-contrib`; `open-telemetry/opentelemetry-collector-releases`; `open-telemetry/opentelemetry-proto`.
- **Caveats / risks:** Exporter queues/retries need capacity planning; configuration and extension exposure require security review. Core security guidance specifies validated config, secure connections and least privilege; no blanket guarantee that custom components follow these rules.
- **Research notes:** `research/2026-10-23-otel-collector-openrtx-promotion.md`. Next: queue batching semantics, TLS defaults, data leakage and resource exhaustion.

### OpenRTX

- **Repository:** https://github.com/OpenRTX/OpenRTX
- **Author / Org:** OpenRTX contributors
- **Category:** Embedded firmware / amateur radio / M17 digital voice / DSP / hardware abstraction
- **Evidence:** VERIFIED — upstream builds/tests; hardware and radio interoperability not independently tested
- **Tier / Score:** S / 26 (Utility 4 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 4 + Maintenance 4)
- **What it does:** Experimental modular open-source firmware for supported digital amateur radios, including an integrated M17 voice/data protocol implementation.
- **Why it is valuable:** End-to-end M17 encoding/decoding, DSP/FEC, device abstractions and multi-target firmware builds make it useful for legitimate radio interoperability and embedded research.
- **Useful code/components:** `openrtx/src/protocols/M17/{FrameEncoder,FrameDecoder,Golay,DSP,Modulator,Demodulator,Callsign,MetaText}.cpp`; `openrtx/src/rtx/OpMode_M17.cpp`; `platform/`; `tests/unit/M17_*.cpp`.
- **Install / runtime:** Meson/CMake, cross toolchains, libcodec2, Python build helpers; firmware images require exact supported radio hardware and safe flashing procedures. Linux emulation/runtime available; some M17 use requires radio modifications.
- **Platforms:** Linux; supported radio Cortex-M targets; Zephyr-based ESP32-S3/Lilygo T-TWR Plus target.
- **License:** Primary GPL-3.0-or-later; mixed file/subtree licenses tracked by `REUSE.toml`, including GPL-2.0-or-later, MIT, Apache-2.0 and vendor-specific terms. Review exact file before copying.
- **Maintenance signals:** Latest inspected GitHub release v0.4.5 (2026-10-04) is a prerelease. Master build-and-test run 38790546561 (2026-10-15) passed all 13 jobs, including unit tests, Zephyr and firmware builds. Retevis-c62 PR-branch build and devcontainer workflows failed 2026-10-23; these do not imply a failed master build.
- **Verification performed:** Inspected README, REUSE metadata, protocol source/test tree, requirements, workflow, release and run jobs. No local build, radio flash, RF reception/transmission, M17 interoperability or memory-safety audit.
- **Source discovery:** GitHub-first embedded/off-grid radio research; prior dossier `research/2026-09-06-openrtx-modular-amateur-radio-firmware-m17-stack.md`.
- **Related projects:** M17 Project, Zephyr RTOS, `travisgoodspeed/md380tools`, `v0l/radio_tool`, Codec2. `AlexandreRouma/SDRPlusPlus` provides an optional M17 decoder; interoperability untested.
- **Caveats / risks:** Upstream explicitly calls firmware highly experimental; flashing carries device risk and RF operation is regulated. Vendor SDK licensing differs from the main project. CI builds do not establish on-device functionality.
- **Research notes:** `research/2026-10-23-otel-collector-openrtx-promotion.md`. Follow failed PR builds and perform device-specific M17 interoperability tests before making operational claims.


### Dora

- **Repository:** https://github.com/dora-rs/dora
- **Author / Org:** dora-rs
- **Category:** Robotics / distributed AI dataflow / Rust / Arrow / ROS2 interoperability
- **Evidence:** VERIFIED — upstream
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Dataflow-oriented robotics/AI runtime with typed YAML graphs, Rust/Python/C/C++ nodes, Arrow messages, shared-memory/Zenoh transports, coordinator/daemon lifecycle and record/replay.
- **Why it is valuable:** Composable cross-language runtime, fault recovery, observability and concrete regression infrastructure, with current releases and substantial upstream CI.
- **Useful code/components:** `libraries/recording/src/lib.rs` (versioned `.drec` read/write); `binaries/record-node/src/main.rs`; `binaries/replay-node/src/main.rs`; `binaries/coordinator/src/` (scheduling/liveness); `binaries/daemon/`; `libraries/arrow-convert/`; `apis/rust/node/`; `tests/fault-tolerance-e2e.rs`.
- **Install / runtime:** Rust/Cargo CLI; Python/PyArrow or Rust/C/C++ node APIs; optional Zenoh networking and ROS2 dependencies. Cargo workspace minimum Rust 1.95.0, CI Rust 1.97.1.
- **Platforms:** Linux, macOS and Windows, with feature-specific platform limitations.
- **License:** Apache-2.0 root; inspect third-party dependencies and Node Hub packages individually. No source copied.
- **Maintenance signals:** Stable v1.1.0 published 2026-10-08 with 14 release assets. 2026-10-22 [main CI 39797929129](https://github.com/dora-rs/dora/actions/runs/39797929129) passed 13/13 jobs including Linux unit, E2E, semantic contracts, benchmarks and audits; Oct 22 commits update record-node and runtime code.
- **Verification performed:** Inspected README, LICENSE, Cargo workspace, implementation directories, `.drec` reader/writer, releases, CI jobs and tests. No independent build, dataflow, Zenoh/ROS2, benchmark or robot-hardware test.
- **Source discovery:** GitHub-first robotics category; `research/2026-09-26-dora-real-time-robotics-dataflow.md`.
- **Related projects:** `dora-rs/dora-hub`, Zenoh, Apache Arrow, ROS2 `rmw_zenoh`, `Ekumen-OS/andino-rs`.
- **Caveats / risks:** `dora_recording` explicitly declares itself **internal and outside the 1.0 API stability guarantee**; format v2 limits record bodies to 64 MiB. README latency claims not independently reproduced; soft real-time is not hard real-time certification.
- **Research notes:** `research/2026-10-23-dora-asterics-aac-promotion.md`. Investigate coordinator recovery, backpressure and `.drec` format compatibility.

### Asterics AAC

- **Repository:** https://github.com/asterics/Asterics-AAC
- **Author / Org:** asterics / AsTeRICS Foundation ecosystem
- **Category:** Accessibility / augmentative and alternative communication / offline-first PWA / alternate input
- **Evidence:** VERIFIED — upstream
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Customizable communication grids with speech, multilingual vocabulary, switch scanning, predictive text, optional messaging and smart-home actions; documented offline-capable PWA.
- **Why it is valuable:** Unifies assistive input, communication and actions across devices; source contains reusable scanning, local data, prediction, speech and grid-action components.
- **Useful code/components:** `src/js/input/scanning.js`, `inputEventHandler.js`; `src/js/service/predictionService.js`; `src/js/service/data/pouchDbService.js`, `encryptionService.js` and `encryptionService.test.js`; `src/js/service/speechService.js`, `actionService.js`, `openHABService.js`; `serviceWorker.js`.
- **Install / runtime:** Modern browser/PWA on mobile/desktop; developer build uses Node.js, npm/Yarn, Jest and Webpack. CI uses Node 22; `npm run build` runs Jest then Webpack and cache generation.
- **Platforms:** Android, iOS, Windows, Linux and macOS browsers.
- **License:** AGPL-3.0 source; CC BY-SA 4.0 documentation/non-source per README; symbol libraries, voices, fonts and media have separate terms. No code or assets copied.
- **Maintenance signals:** Stable release `release-2026-10-21-12.10/+0200` (2026-10-21) fixes word forms, navigation and imports. 2026-10-23 [PR Beta Build 39950169970](https://github.com/asterics/Asterics-AAC/actions/runs/39950169970) succeeded with Jest+Webpack; beta deployment success is not independent UI verification.
- **Verification performed:** Inspected README, LICENSE, package manifest, scanning and encryption source, service worker, Jest tests, release and CI workflow. No independent browser install, offline cold-start, switch/eye-gaze hardware, user study or cryptographic audit.
- **Source discovery:** GitHub-first accessibility category; `research/2026-09-25-asterics-aac-offline-accessibility-platform.md`.
- **Related projects:** `asterics/predictionary`, `asterics/AsTeRICS`, `asterics/FabiWare`, `asterics/FLipMouse`, ARASAAC.
- **Caveats / risks:** Offline use may require prior caching; cloud/Matrix/HTTP integrations need trust controls. Vue 2-era dependencies merit review. AAC suitability is user-specific and was not assessed.
- **Research notes:** `research/2026-10-23-dora-asterics-aac-promotion.md`. Test fresh-install offline behavior, physical switch scanning and external asset licensing.

### OpenRefine

- **Repository:** https://github.com/OpenRefine/OpenRefine
- **Author / Org:** OpenRefine community
- **Category:** Data cleaning / reconciliation / local-first data transformations / Java
- **Evidence:** VERIFIED (upstream source, release, unit/E2E CI; no independent execution)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Browser-based local data-cleaning workbench for importing, profiling, clustering, transforming, reconciling and exporting tabular/structured data.
- **Why it is valuable:** Reusable GREL parser, format importers, string-clustering strategies, reconciliation extensions and reproducible operations, supported by browser E2E and Java unit tests.
- **Useful code/components:** `modules/grel/src/main/java/com/google/refine/grel/Parser.java` and `Scanner.java`; `main/src/com/google/refine/importers/`; `main/src/com/google/refine/clustering/`; `extensions/wikibase/`; `server/src/com/google/refine/ValidateHostHandler.java`; `main/tests/cypress/`.
- **Install / runtime:** Official desktop packages; for source builds Maven, Node.js and Java. README says JDK 11+, but current root `pom.xml` declares Java minimum 21; follow the manifest/branch-specific build instructions.
- **Platforms:** Windows, macOS, Linux; Java server with local browser interface.
- **License:** BSD-3-Clause root; preserve notices and separately inspect extension/dependency licenses.
- **Maintenance signals:** Stable 3.10.1 released 2026-03-04; October 23 commits fix path-prefixed URLs and macOS signing. 2026-10-23 [upstream snapshot CI](https://github.com/OpenRefine/OpenRefine/actions/runs/40010351064) passed 12/12 jobs, including seven Cypress E2E groups, unit tests and packaging.
- **Verification performed:** README, LICENSE.txt, pom.xml, GREL parser, importers/clustering, server Host validation and CI workflow/job results inspected 2026-10-24. No independent install, transformations, performance tests or security audit.
- **Source discovery:** GitHub-first data-cleaning category.
- **Related projects:** Wikibase, Wikidata, OpenRefine reconciliation services, OpenRefine extensions.
- **Caveats / risks:** README and current build manifest disagree on Java minimum. The local HTTP interface's host-validation code does not establish full security. Third-party integrations and imported data require privacy/license review.
- **Research notes:** `research/2026-10-24-openrefine-kiwix-android-promotion.md`. Test release-specific Java requirements, import edge cases, reconciliation provenance and local HTTP trust boundaries.

### Kiwix Android

- **Repository:** https://github.com/kiwix/kiwix-android
- **Author / Org:** Kiwix
- **Category:** Android / offline knowledge / ZIM archives / Wi-Fi Direct content sharing
- **Evidence:** VERIFIED (upstream source, stable release, partial emulator CI; not independently run)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Offline Android reader for ZIM archives (including Wikipedia), with local library management, file transfer and local-network serving.
- **Why it is valuable:** Practical offline knowledge distribution with reusable Android storage handling, Wi-Fi Direct file exchange, ZIM-reader integration and optional local HTTP sharing.
- **Useful code/components:** `app/src/main/java/org/kiwix/kiwixmobile/webserver/KiwixServer.kt`; `localFileTransfer/WifiDirectManager.kt`; `zimManager/Fat32Checker.kt`; `core/src/main/java/org/kiwix/kiwixmobile/core/reader/`; `core/.../downloader/`; `app/.../zimManager/`.
- **Install / runtime:** Android 7.1+ (minSdk 25). Official full APK or restricted Play Store variant; source builds require Android Studio/Gradle with JDK 21.
- **Platforms:** Android phones and tablets; targetSdk 36 in current development source.
- **License:** GPL-3.0-or-later; separate rights apply to ZIM content, branding and dependencies.
- **Maintenance signals:** Stable v3.14.1 released 2026-05-14; October 22 source changes improve read-aloud and java-libkiwix integration. 2026-10-22 [main CI](https://github.com/kiwix/kiwix-android/actions/runs/39790121822) **failed** an Android API 25 standard-app test while other matrix jobs passed; 2026-10-24 CD succeeded but does not prove runtime correctness.
- **Verification performed:** README, COPYING, Gradle, Config.kt, Wi-Fi Direct manager, server, FAT32 checker, test matrix and CI job results inspected 2026-10-24. No independent Android build, real-device test, offline archive read, peer transfer or security audit.
- **Source discovery:** Recursive GitHub-first follow-up from libzim and ZIM Tools.
- **Related projects:** `openzim/libzim`, `openzim/zim-tools`, `kiwix/java-libkiwix`, `kiwix/kiwix-android-branded`, `kiwix/kiwix-desktop`.
- **Caveats / risks:** Play Store variant has Android scoped-storage restrictions; full variant permits broader file selection. Large ZIM files may exceed FAT32 limits; deleting the app can delete app-managed archives. Wi-Fi Direct and local server trust boundaries need review. Main's 4.0.0 version configuration is not a published stable release.
- **Research notes:** `research/2026-10-24-openrefine-kiwix-android-promotion.md`. Follow Android API 25 CI regression and test cold-start offline, network sharing and file integrity.


### java-libkiwix

- **Repository:** https://github.com/kiwix/java-libkiwix
- **Author / Org:** Kiwix
- **Category:** Android / JNI / Java-Kotlin / offline ZIM archives / embedded local HTTP serving
- **Evidence:** VERIFIED (upstream source, release and CI build/test; no independent Android runtime verification)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 5)
- **What it does:** Java/Kotlin Android bindings to native libkiwix and libzim for archive access, catalog management, full-text search, suggestions and local serving.
- **Why it is valuable:** Integrates reusable native ZIM components into Android applications, exposing archive readers, searchable offline libraries and HTTP serving without implementing the native format stack from scratch.
- **Useful code/components:** `lib/src/main/java/org/kiwix/libzim/Archive.java`, `Searcher.java`, `SuggestionSearcher.java`; `lib/src/main/java/org/kiwix/libkiwix/Library.java`, `Manager.java`, `Server.java`; JNI bridges `lib/src/main/cpp/libzim/archive.cpp`, `searcher.cpp`, `libkiwix/kiwixserver.cpp`; `lib/src/test/` ZIM fixtures and Java tests.
- **Install / runtime:** README specifies JDK 17, `./install_deps.sh`, `./gradlew buildHeaders build`; produces Android AAR. Current Gradle manifest: minSdk 24, compileSdk 34, NDK 27.3.13750724. Native libraries support multiple Android ABIs.
- **Platforms:** Android API 24+; Java/Kotlin apps with bundled native libraries.
- **License:** GPL-3.0-or-later per README/COPYING. Native libkiwix/libzim and third-party components require independent notice and licensing review.
- **Maintenance signals:** Stable 2.7.0 released 2026-10-21; adds ZIM language metadata and updates libzim 9.8.2. [Upstream CI 39562805161](https://github.com/kiwix/java-libkiwix/actions/runs/39562805161) succeeded 2026-10-21 (one build-and-test job).
- **Verification performed:** Inspected README, COPYING, CHANGELOG, Gradle manifest, Java/JNI module trees, test fixtures, CI workflow, release and job result on 2026-10-24. No local build, emulator/device run, malformed archive test or security audit.
- **Source discovery:** Recursive GitHub-first investigation from existing libzim and Kiwix Android entries.
- **Related projects:** `kiwix/kiwix-android`, `kiwix/libkiwix`, `openzim/libzim`, `openzim/zim-tools`.
- **Caveats / risks:** JNI ABI compatibility, native memory safety, 16KB page-size support and malicious ZIM parsing require further tests. CI success is not proof of Android device compatibility or safe local HTTP exposure.
- **Research notes:** `research/2026-10-24-java-libkiwix-rizin-promotion.md`. Test corrupted archives and network-serving boundaries; check transitive native licenses.

### Rizin

- **Repository:** https://github.com/rizinorg/rizin
- **Author / Org:** RizinOrg
- **Category:** Defensive reverse engineering / binary parsing / forensics / developer tools / C
- **Evidence:** VERIFIED (upstream source, release and partially passing CI; no independent binary-analysis tests)
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** Scriptable binary-analysis and debugging framework with disassemblers, file-format parsers, search/diff utilities and reusable C libraries.
- **Why it is valuable:** Exposes practical stand-alone binary-inspection CLIs and composable libraries for legitimate forensics, firmware interoperability, debugging and defensive program analysis.
- **Useful code/components:** `librz/bin/` loaders and parsers; `librz/arch/` disassembly/analysis; `librz/arch/il/` intermediate-language lifting; `librz/diff/fastcdc.c` content-defined chunking; `librz/diff/bytes_diff.c` and `lines_diff.c`; `librz/search/`; `binrz/` command-line tools; `test/db/`, `test/unit/`, `test/fuzz/` test infrastructure.
- **Install / runtime:** Meson/Ninja build (`meson setup build`, `meson compile -C build`); install via supported packages or source. C toolchain, Python build helpers and architecture/format dependencies vary by target.
- **Platforms:** Linux, macOS, Windows, BSD; additional targets including Android are documented upstream but were not independently tested.
- **License:** Core Meson project declares LGPL-3.0-only. `REUSE.toml`, file SPDX headers and `LICENSES/` show mixed licensing; inspect each reused file and dependency.
- **Maintenance signals:** Stable v0.9.1 released 2026-06-29; active dev commits 2026-10-23. Development `meson.build` reports v0.10.0, not a published stable release. [Upstream CI 39999863129](https://github.com/rizinorg/rizin/actions/runs/39999863129) and [rerun 40000224650](https://github.com/rizinorg/rizin/actions/runs/40000224650) failed four Capstone variant builds; several Linux/macOS, sanitizer and QEMU RISC-V jobs passed.
- **Verification performed:** Inspected README, BUILDING.md, Meson, LGPL text, REUSE licensing annotations, source/test trees, release metadata and CI job conclusions on 2026-10-24. No local compile, parser correctness tests, fuzzing or security audit.
- **Source discovery:** GitHub-first defensive binary-analysis category.
- **Related projects:** `rizinorg/rz-pipe`, `rizinorg/rizin-testbins`, `rizinorg/cutter`, `radareorg/radare2`; `NationalSecurityAgency/ghidra` (independent alternative).
- **Caveats / risks:** Current development CI is not green; Capstone dependency compatibility needs investigation. Untrusted binary formats present parser attack surface; do not assume LGPL covers all bundled files. Intended catalog use is authorized debugging, forensics and interoperability.
- **Research notes:** `research/2026-10-24-java-libkiwix-rizin-promotion.md`. Recheck Capstone matrix and evaluate FastCDC, RzIL and fuzz corpus independently.



### osm2pgsql

- **Repository:** https://github.com/osm2pgsql-dev/osm2pgsql
- **Author / Org:** osm2pgsql-dev
- **Category:** OpenStreetMap / geospatial ETL / PostgreSQL / PostGIS / incremental data import / Lua
- **Evidence:** VERIFIED (upstream source, release and CI; no independent database import)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Imports OSM, PBF and O5M geodata into PostgreSQL/PostGIS, with Lua-configurable geometry and table outputs and incremental replication diffs.
- **Why it is valuable:** Mature, well-tested ingestion and transformation pipeline for self-hosted maps, geocoding and geospatial analysis; valuable incremental tile-expiry and geometry code.
- **Useful code/components:** `src/input.cpp`, `src/osmdata.cpp` (ingestion); `src/output-flex.cpp`, `src/flex-lua-*.cpp` (Lua/PostGIS output); `src/geom-from-osm.cpp` (geometry); `src/expire-tiles.cpp`, `src/expire-output.cpp` (tile invalidation); `src/node-persistent-cache.cpp`, `src/middle-pgsql.cpp` (intermediate storage); `flex-config/*.lua` (public-domain examples); `tests/test-output-flex-update.cpp`, `tests/test-expire-tiles.cpp` and `tests/bdd/` (regressions).
- **Install / runtime:** Distribution packages or CMake/C++17 source build; requires PostgreSQL >=12 (14+ recommended) and PostGIS >=3.0; Lua and other build libraries; large-area imports need substantial storage and memory.
- **Platforms:** Linux, Windows, macOS; other Unix-like platforms with dependencies.
- **License:** GPL-2.0-or-later (README and SPDX); `flex-config/` examples are explicitly public domain. Bundled third-party libraries have separate licenses; OSM input data has separate ODbL obligations.
- **Maintenance signals:** Stable v2.3.1 released 2026-07-05, fixing a diff-expire segfault; 2026-10-15 master commit 5d821cce adds grouped-linemerge generalization. Upstream CI [38734399518](https://github.com/osm2pgsql-dev/osm2pgsql/actions/runs/38734399518) passed **20/20** jobs; installation CI [38734399525](https://github.com/osm2pgsql-dev/osm2pgsql/actions/runs/38734399525) passed **2/2**.
- **Verification performed:** Inspected README, COPYING, CMake requirements, source/test trees, flex configuration examples, release notes and workflow; upstream build-and-test action invokes `ctest` under PostgreSQL virtual environments. No local import, replication replay, benchmark or security audit.
- **Source discovery:** GitHub-first geospatial tooling pass.
- **Related projects:** `osm2pgsql-dev/osm2pgsql-themepark`, `osmcode/libosmium`, `mapbox/protozero`; `protomaps/PMTiles` and `onthegomap/planetiler` are adjacent map-pipeline alternatives, not dependencies.
- **Caveats / risks:** High resource demand for global imports; ensure PostgreSQL access control and validate incremental updates/dirty-tile calculations on real data. GPL and OSM dataset licenses are distinct.
- **Research notes:** `research/2026-10-24-osm2pgsql-rz-pipe-promotion.md`. Follow-up: replication-diff idempotency, multi-output expiry regression, Lua transformation correctness, geometry edge cases.

### rz-pipe

- **Repository:** https://github.com/rizinorg/rz-pipe
- **Author / Org:** rizinorg
- **Category:** Defensive binary analysis / Rizin automation / IPC / Python / Rust / Go / multi-language bindings
- **Evidence:** VERIFIED (upstream source and passing CI for supported components; no independent runtime tests)
- **Tier / Score:** A / 24 (Utility 4 + Working Evidence 4 + Reusability 5 + Novelty 3 + Documentation 4 + Maintenance 4)
- **What it does:** Exposes Rizin command execution and JSON output to Python, Go, Rust, Haskell, OCaml, Ruby and Racket through local subprocess/pipes and optional network transports.
- **Why it is valuable:** Reusable automation bridge for scripted, authorized firmware and binary inspection without embedding Rizin's internal C APIs.
- **Useful code/components:** `python/rzpipe/open_sync.py`, `open_async.py`, `open_base.py` (transport and command helpers); `python/tests/`; `go/rzpipe.go`, `go/native.go`, `go/rzpipe_test.go`; `rust/src/rzpipe.rs`, `rz.rs`, `errors.rs`; Racket, Ruby, OCaml and Haskell bindings.
- **Install / runtime:** Rizin CLI or compatible trusted remote endpoint; Python package `rzpipe` (`pip install rzpipe` documented), Go module or Rust Cargo build; other languages have separate package/build procedures.
- **Platforms:** Linux, macOS and Windows where corresponding language runtime and Rizin process/transport are supported; exact portability varies by binding.
- **License:** **Mixed by language:** Python/Haskell MIT; Rust MIT OR Apache-2.0. No root LICENSE; Go, Ruby, OCaml and Racket source licensing not established in this pass. **Do not copy unreviewed language code.**
- **Maintenance signals:** Master commit b2fa2dfd (2026-09-27) adds Racket binding; Python NUL-output fix 2026-09-27. Upstream CI [36352169977](https://github.com/rizinorg/rz-pipe/actions/runs/36352169977) passed **2/2** jobs; no GitHub Releases objects returned.
- **Verification performed:** Inspected README, language trees, Python and Rust manifests/licenses, Go tests, Python subprocess implementation and CI workflow. CI runs Python pytest and Go tests, builds Rust and exercises additional bindings; it does **not** run Rust unit tests. No independent installation, execution, transport-security testing or audit.
- **Source discovery:** Recursive investigation of the existing `rizinorg/rizin` entry.
- **Related projects:** `rizinorg/rizin`, `rizinorg/cutter`, `rizinorg/rizin-testbins`, `radareorg/radare2`.
- **Caveats / risks:** Plain HTTP/TCP remote command interfaces may lack authentication and transport encryption; do not expose publicly. Commands can manipulate Rizin analysis state and targets; use only on authorized files and trusted services. Python NUL-delimited output handling and polling deserve regression testing.
- **Research notes:** `research/2026-10-24-osm2pgsql-rz-pipe-promotion.md`. Follow-up: remote trust boundaries, per-language license audit, Windows and Rust runtime tests, malformed command/output behavior.


### Tesseract OCR

- **Repository:** https://github.com/tesseract-ocr/tesseract
- **Author / Org:** tesseract-ocr
- **Category:** offline-ocr / document-processing / computer-vision / c++ / c-api / text-extraction
- **Evidence:** VERIFIED (upstream code, releases and CI; no independent execution)
- **Tier / Score:** S / 28 (utility 5 + working evidence 5 + reusability 5 + novelty 3 + documentation 5 + maintenance 5)
- **What it does:** Offline LSTM and optional legacy OCR engine with CLI, C/C++ APIs and text/hOCR/ALTO/PAGE/TSV/searchable-PDF output.
- **Why it is valuable:** Reusable image-to-text pipeline, document renderers, page-layout algorithms, training utilities and cross-platform embedding.
- **Useful code/components:** `include/tesseract/baseapi.h; src/api/baseapi.cpp (C++ OCR API)`; `include/tesseract/capi.h; src/api/capi.cpp (C interface)`; `src/api/hocrrenderer.cpp, altorenderer.cpp, pdfrenderer.cpp (document outputs)`; `src/textord/ (page segmentation and text layout)`; `src/lstm/lstmrecognizer.cpp, recodebeam.cpp (neural recognition)`; `src/training/lstmtraining.cpp, text2image.cpp (training tools)`; `unittest/ (API, LSTM, page layout, sanitizer tests)`.
- **Install / runtime:** Use packages or CMake/Autotools C++ build with Leptonica and separate traineddata language models; preprocess PDF into images for input.
- **Platforms:** Linux, Windows, macOS, C++/Leptonica-supported environments.
- **License:** Apache-2.0 engine; Leptonica, language traineddata and other dependencies separately licensed. No third-party code copied.
- **Maintenance signals:** 2026-10-24 main commits fix Windows NSIS buffer and skip unit tests when traineddata absent; active multi-platform CI; stable 5.5.3 (2026-07-24).
- **Verification performed:** 2026-10-24: inspected README, LICENSE, VERSION, doc/tesseract.1.asc, source/API trees, unit tests, and CI workflows; Stable GitHub release 5.5.3 published 2026-07-24; VERSION matches; 2026-10-24 upstream Linux autotools CI 40128395434 passed 4/4; macOS autotools 40127924448 and Windows msys2 40114227579 succeeded; Upstream CMake CI 40025480669 passed 8/8; sanitizer unit tests 40042891468 passed 2/2; CodeQL 40091625811 succeeded; CI invokes sample OCR and make check; no independent build, OCR accuracy test or security audit.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `tesseract-ocr/tessdata`; `tesseract-ocr/tessdata_fast`; `tesseract-ocr/tessdata_best`; `DanBloomberg/leptonica`; `paperless-ngx/paperless-ngx` (downstream Tesseract/OCRmyPDF integration; source inspected 2026-10-27).; OCRmyPDF (downstream searchable-PDF pipeline).
- **Caveats / risks:** Untrusted-image parsing, model licensing, image quality and C API memory ownership require review; upstream CI does not prove accuracy or safety.
- **Research notes:** research/2026-10-24-tesseract-openscad-promotion.md. OCR engine accepts raster images, not PDFs directly; PDF output supported. Model availability, input image quality and page segmentation affect accuracy. No independent OCR accuracy benchmark. Check traineddata licenses and memory ownership before code extraction.

### OpenSCAD

- **Repository:** https://github.com/openscad/openscad
- **Author / Org:** openscad
- **Category:** parametric-cad / 3d-printing / geometry / c++ / design-automation / offline-tools
- **Evidence:** VERIFIED (upstream code, releases and CI; no independent execution)
- **Tier / Score:** S / 26 (utility 5 + working evidence 5 + reusability 5 + novelty 4 + documentation 4 + maintenance 3)
- **What it does:** Script-driven 3D CAD compiler for constructive solid geometry, parametric parts, extrusion and mesh export.
- **Why it is valuable:** Reproducible, version-controlled mechanical designs; reusable geometry and export components.
- **Useful code/components:** `src/core/AST.cc, Expression.cc (parametric language evaluation)`; `src/core/CSGTreeEvaluator.cc (constructive solid geometry tree)`; `src/geometry/GeometryEvaluator.cc, boolean_utils.cc (geometry operations)`; `src/geometry/linear_extrude.cc, rotate_extrude.cc (extrusion)`; `src/io/export_stl.cc, export_3mf_v2.cc, import_stl.cc (model interchange)`; `tests/regression/, tests/test_cmdline_tool.py, tests/stlexportsanitytest.py`; `libraries/MCAD (mechanical shapes, LGPL-2.1 submodule)`.
- **Install / runtime:** Desktop binary or C++17/CMake build with Qt, CGAL, OpenCSG, Eigen, Boost and other libraries; optional headless build.
- **Platforms:** Linux/Unix, Windows, macOS, headless CLI builds.
- **License:** GPL-2.0-or-later with CGAL linking exception; MCAD and other submodules have separate licenses. No third-party code copied.
- **Maintenance signals:** Active 2026-10-24 master commits and multi-OS green CI; last non-prerelease GitHub tag remains 2021.01 (2021-02-07).
- **Verification performed:** 2026-10-24: inspected README, COPYING, src/openscad.cc license header, .gitmodules, CMake, geometry/core/io source and regression tests; Latest GitHub stable release found openscad-2021.01 (2021-02-07); master commit bf28796b dated 2026-10-24; 2026-10-24 upstream Linux release build 40109445217, release tests 40109445203 and experimental tests 40109445087 succeeded; 2026-10-24 upstream macOS experimental 40109445085 and Windows msys2 40109445266 succeeded (Windows Qt5 and Qt6 jobs); Linux experimental CI invokes CTest, example tests and coverage; no independent geometry rendering, STL validation or 3D printing.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `openscad/MCAD`; `elalish/manifold`; `floriankirsch/OpenCSG`; `AngusJohnson/Clipper2`; `FreeCAD/FreeCAD` (OpenSCAD workbench; interoperability untested).
- **Caveats / risks:** Stable release is over five years old; active master differs. 3D geometry must be checked before physical fabrication; license exception does not cover all submodules.
- **Research notes:** research/2026-10-24-tesseract-openscad-promotion.md. S/26 discounts old stable release despite active development. CGAL, Qt, OpenCSG, Eigen, Boost and other dependencies required; submodule licenses differ. Verify manifold quality and nightly/stable differences before production use.

### OpenROAD

- **Repository:** https://github.com/The-OpenROAD-Project/OpenROAD
- **Author / Org:** The OpenROAD Project
- **Category:** Electronic design automation / ASIC physical design / OpenDB / C++ / Tcl / limited Python
- **Evidence:** VERIFIED (upstream code, build CI and regression fixtures; no independent execution)
- **Tier / Score:** S / 27 (utility 5 + working evidence 4 + reusability 5 + novelty 4 + documentation 5 + maintenance 4)
- **What it does:** Open-source ASIC physical-design application with floorplanning, placement, clock-tree synthesis, routing, timing repair and design database.
- **Why it is valuable:** Reusable LEF/DEF physical-design database, placement/routing engines, Tcl/Python control and example chip-design flows.
- **Useful code/components:** `src/odb/` (OpenDB LEF/DEF and binary DB); `src/drt/` (detailed routing/DRC); `src/rsz/` (timing and gate repair); `src/gpl/`, `src/cts/`, `src/pdn/`, `src/grt/` (placement/clock/power/global routing); `src/README.md` (API); `test/` and `src/*/test/` (regressions).
- **Install / runtime:** Bazelisk and Bazel-supported C++ build toolchain, with relevant physical-design libraries and PDK; Tcl interface, limited Python bindings. **CMake deprecated and scheduled for removal November 1, 2026.**
- **Platforms:** Linux primary; macOS upstream CI; other Bazel-supported hosts require confirmation.
- **License:** BSD-3-Clause root; review third-party/submodule SPDX and notices. No third-party code copied.
- **Maintenance signals:** 2026-10-25 UTC master commits; upstream macOS build 40145237901 passed, CodeQL 40145237910 passed, expected-output check 40145237885 passed. No current stable GitHub release verified (only old v0.9.0-beta object returned).
- **Verification performed:** README, LICENSE, Bazel/CMake docs, OpenDB/detailed-route/resizer documentation, source/test trees and GitHub Actions inspected. No independent build, end-to-end RTL-to-GDSII run, PDK integration, silicon or security audit.
- **Source discovery:** GitHub-first EDA research; no YouTube attribution.
- **Related projects:** `The-OpenROAD-Project/OpenROAD-flow-scripts`; OpenSTA; PDK toolchains.
- **Caveats / risks:** CMake deprecation, large build/PDK requirements, incomplete OpenDB API documentation, limited Python support; passing CI does not establish physical-design quality.
- **Research notes:** `research/2026-10-24-openroad-zmk-promotion.md`. Investigate OpenDB reuse, detailed-route reproducibility, PDK compatibility and Bazel transition.

### ZMK Firmware

- **Repository:** https://github.com/zmkfirmware/zmk
- **Author / Org:** zmkfirmware
- **Category:** Zephyr-based embedded keyboard firmware / BLE / USB HID / split keyboards / alternative input
- **Evidence:** VERIFIED (upstream source, tests and build CI; no independent hardware test)
- **Tier / Score:** S / 26 (utility 5 + working evidence 4 + reusability 5 + novelty 4 + documentation 5 + maintenance 3)
- **What it does:** Configurable low-power firmware for wired/wireless custom keyboards, split input devices, key layers, macros, pointing devices and Studio configuration.
- **Why it is valuable:** Reusable key-behavior engine and BLE/USB HID, split transport, programmable alternative-input capabilities.
- **Useful code/components:** `app/src/behaviors/` (hold-tap, sticky keys, tap dance, macros); `app/src/split/` (wired/BLE split); `app/src/pointing/` (input processors); `app/src/studio/` (RPC/transport); `app/src/ble.c`, `usb_hid.c`, `keymap.c`; `app/tests/` (behavior/BLE regressions).
- **Install / runtime:** Zephyr `west` workspace and board-specific firmware builds; supported MCU/shield and USB/BLE input hardware. `app/west.yml` pins `zmkfirmware/zephyr` `v4.1.0+zmk-fixes`.
- **Platforms:** Supported nRF52/nRF53, RP2040 and other listed boards; USB and BLE HID; Linux/macOS/Windows build hosts vary.
- **License:** MIT root; west modules and HALs retain their own licenses. No third-party code copied.
- **Maintenance signals:** Stable v0.3.0 (2025-08-01); master commits through 2026-10-09. Oct 23 Tests 40030685287 passed 25/25; BLE 40030685316 passed 4/4; Oct 24 scheduled Build 40062805918 failed one `proton_c` matrix job; Oct 25 main Build 40162399914 passed 38 jobs (3 skipped), including `proton_c`. Root cause unknown.
- **Verification performed:** README, LICENSE, changelog, west manifest, source/test directories, workflows, recent commits and CI job matrices inspected. No independent flash, BLE pairing, accessibility testing or security audit.
- **Source discovery:** GitHub-first embedded/alternative-input discovery; no YouTube attribution.
- **Related projects:** `zephyrproject-rtos/zephyr`; `zmkfirmware/zephyr`; `zmkfirmware/zmk-studio`.
- **Caveats / risks:** The Oct 24 `proton_c` failure was followed by an Oct 25 passing `proton_c` build; root cause unknown and board/shield combinations are not universally verified. BLE pairing, split reliability and Studio RPC need security testing. Customizable input is not itself proof of accessibility suitability.
- **Research notes:** `research/2026-10-24-openroad-zmk-promotion.md`. Follow the pinned Zephyr fork, investigate `proton_c` failure, Studio RPC and hardware compatibility.


### LibrePCB

- **Repository:** https://github.com/LibrePCB/LibrePCB
- **Author / Org:** LibrePCB
- **Category:** PCB EDA / schematic capture / circuit-board layout / C++ / Rust / Qt / CLI
- **Evidence:** VERIFIED (upstream source, release and CI; no independent build)
- **Tier / Score:** S / 28 (utility 5 + working evidence 4 + reusability 5 + novelty 4 + documentation 5 + maintenance 5)
- **What it does:** Cross-platform, open-source electronic design suite for schematic capture and PCB layout, with design libraries, importers and CLI automation.
- **Why it is valuable:** Working PCB engineering stack with reusable geometry, import, export, board model and rule-checking components, plus CLI and test fixtures.
- **Useful code/components:** `libs/librepcb/core/` (project/board models, serialization, geometry, rule checks); `libs/librepcb/kicadimport/` and `libs/librepcb/eagleimport/` (library converters); `apps/librepcb-cli/commandlineinterface.cpp` (automation); `tests/unittests/`, `tests/cli/`, `tests/funq/`, `tests/ui/` (tests).
- **Install / runtime:** Stable release recommended; source requires C++20, Rust >=1.92 GNU, Qt >=6.2, CMake >=3.22, OpenSSL; OpenCASCADE optional. Windows builds require MinGW GNU rather than MSVC.
- **Platforms:** Windows, Linux, macOS.
- **License:** GPL-3.0 root; REUSE metadata, third-party assets and submodules have distinct file-level obligations. No code copied.
- **Maintenance signals:** Stable release 2.1.1 on 2026-06-12; active master fix 2026-10-20; [upstream 2026-10-24 CI](https://github.com/LibrePCB/LibrePCB/actions/runs/40072270629) passed 9/9 jobs on Linux/macOS/Windows plus quality checks. Some Oct 22 CI runs failed before newer green runs.
- **Verification performed:** README, license/REUSE tree, source and test directories, CI job matrix, releases and commits inspected; no independent compilation, PCB fabrication, import/export validation or security testing.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** KiCad import ecosystem, LibrePCB libraries and EAGLE import.
- **Caveats / risks:** Master explicitly unstable and may break projects/workspaces; prefer stable builds. Verify imported library geometry, rule checks and fabrication exports before manufacturing; comply with copyleft and third-party licensing.
- **Research notes:** `research/2026-10-24-librepcb-xournalpp-promotion.md`. Follow up on KiCad/EAGLE import fidelity, CLI automation and rule-check regressions.

### Xournal++

- **Repository:** https://github.com/xournalpp/xournalpp
- **Author / Org:** xournalpp
- **Category:** Offline note-taking / stylus input / PDF annotation / Lua plugins / document processing
- **Evidence:** VERIFIED (upstream release and CI; no independent install)
- **Tier / Score:** S / 27 (utility 5 + working evidence 4 + reusability 5 + novelty 4 + documentation 5 + maintenance 4)
- **What it does:** Cross-platform handwriting and PDF-annotation application supporting pen tablets, layers, images, text, audio, and extensible Lua plugins.
- **Why it is valuable:** Offline document workflow with reusable stroke and layer models, PDF integration, Lua plugin hooks and multi-platform test coverage.
- **Useful code/components:** `src/core/model/Stroke.cpp`, `Document.cpp`, `Layer.cpp`, `Snapping.cpp` (ink/document); `src/core/pdf/` (PDF); `src/core/control/xojfile/` (native document I/O); `src/core/plugin/`, `plugins/` (Lua); `src/core/audio/`; `test/unit_tests/`, `test/gtk_tests/`.
- **Install / runtime:** Official release packages for Linux, Windows and macOS; Linux distribution packages, Flatpak and AppImage; source uses CMake/C++ and GTK stack. LaTeX tool requires separate TeX installation.
- **Platforms:** Linux, Windows, macOS; ChromeOS via Linux container. Mobile version is separate software.
- **License:** GPL-2.0-or-later core per `copyright.txt`; some icons/assets GPL-3.0+, ISC or CC-BY-SA-4.0. File-level review required; no code/assets copied.
- **Maintenance signals:** Stable v1.3.8 on 2026-09-26; commits through 2026-10-24; [upstream 2026-10-24 Build](https://github.com/xournalpp/xournalpp/actions/runs/40072649214) passed 7/7 cross-platform jobs. Some later PR checks show `action_required`, not passing verification.
- **Verification performed:** README, licenses and `copyright.txt`, plugin/model/PDF/test source trees, workflow and release metadata inspected. No independent pen, PDF, plugin, export, backup or security testing.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** Flathub packaging and Xournal++ Mobile (separate upstream).
- **Caveats / risks:** Lua plugins execute code; trust boundaries need review. Stylus compatibility and PDF round-trips vary by platform and file. File-level asset licenses differ.
- **Research notes:** `research/2026-10-24-librepcb-xournalpp-promotion.md`. Investigate document parser resilience, plugin security, stylus latency and backup recovery.

### Renode

- **Repository:** https://github.com/renode/renode
- **Author / Org:** renode
- **Category:** embedded-emulation / virtual-hardware / firmware-testing / robot-framework / co-simulation
- **Evidence:** VERIFIED (narrow downstream patched Renode execution; upstream core CI unconfirmed)
- **Tier / Score:** S / 27 (utility 5 + working evidence 4 + reusability 5 + novelty 5 + documentation 5 + maintenance 3)
- **What it does:** Emulates embedded CPUs, boards, peripherals and networks to run unmodified firmware without hardware.
- **Why it is valuable:** Multi-node virtual hardware and firmware regression automation; useful reusable test infrastructure.
- **Useful code/components:** src/Renode/PlatformDescription/: board descriptions; src/Renode/Network/ and Connectors/: virtual networks; src/Renode/RobotFrameworkEngine/: test keywords; tests/run_tests.py and tests/platforms/*.robot: Robot/NUnit regression harness; src/Plugins/CoSimulationPlugin/ and SystemCPlugin/: co-simulation; src/Renode/WebSockets/ and ws-api/: remote interfaces.
- **Install / runtime:** .NET >=6, prebuilt Windows/Linux/macOS packages or source; GTK2 for Linux portable GUI, Robot Framework/Python for tests.
- **Platforms:** Linux, Windows, macOS, virtual ARM/RISC-V/x86/SPARC/POWER/Xtensa/MSP430X.
- **License:** MIT core; third-party libraries separately licensed; no code copied.
- **Maintenance signals:** Stable v1.17.0 (2026-09-07), active source 2026-10-23; upstream core CI unconfirmed. [ArduPilot Renode run 40231792336](https://github.com/ArduPilot/ardupilot/actions/runs/40231792336) passed 2026-10-25 with emulator unit tests and CubeOrangePlus quadplane mission.
- **Verification performed:** 2026-10-25: README, MIT LICENSE, source/test/platform trees and test runner inspected; Stable v1.17.0 published 2026-09-07 with binary assets and detailed architecture fixes; 2026-10-23 master commit 04cafbb adjusts CPU pause/halt synchronization; No passing current core emulator CI found; 2026-10-22 GitHub Actions success 39742143711 was dependency graph update only; 2026-10-25 downstream ArduPilot job 121284892561 passed Renode unit tests and quadplane mission using an ArduPilot-hosted, checksum-verified custom Renode package. No independent build, upstream stock runtime test, physical hardware timing test or security audit.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** renode/renode-infrastructure; zephyrproject-rtos/zephyr; lowRISC/opentitan; ArduPilot/ardupilot (`Tools/renode/` downstream integration).
- **Caveats / risks:** Downstream patched Renode executed successfully, but unmodified upstream core tests and broad CPU/peripheral fidelity remain unverified; virtual timing differs from hardware; bundled licenses and remote API access require review.
- **Research notes:** `research/2026-10-25-renode-odm-maintenance.md`. VERIFIED narrowly via downstream patched Renode execution, not general stock upstream or hardware equivalence. See `research/2026-10-25-openthread-ardupilot-renode.md`. .NET >=6; GTK2 for Linux portable GUI; Robot Framework/Python tests. Simulated peripheral/timing fidelity varies; secure remote APIs and check dependency licenses.

### OpenDroneMap

- **Repository:** https://github.com/OpenDroneMap/ODM
- **Author / Org:** OpenDroneMap
- **Category:** photogrammetry / aerial-mapping / geospatial / point-clouds / orthophotos / 3d-reconstruction
- **Evidence:** VERIFIED (upstream evidence only)
- **Tier / Score:** S / 27 (utility 5 + working evidence 4 + reusability 5 + novelty 4 + documentation 5 + maintenance 4)
- **What it does:** Converts aerial photographs into georeferenced orthophotos, elevation models, point clouds and textured 3D meshes.
- **Why it is valuable:** Reusable open geospatial reconstruction with GCP, multispectral/thermal and map tiling components.
- **Useful code/components:** stages/run_opensfm.py, odm_meshing.py, odm_dem.py, odm_orthophoto.py: reconstruction stages; opendm/gcp.py and geo.py: ground-control/georeferencing; opendm/dem/: DEM and PDAL; opendm/orthophoto.py, cogeo.py, tiles/: orthophotos/GeoTIFF/tiles; opendm/multispectral.py and thermal.py: sensor data; opendm/remote.py and stages/splitmerge.py: remote processing; tests/test_gcp.py and tests/: regression fixtures.
- **Install / runtime:** Docker CPU amd64/arm64, optional NVIDIA GPU image, or native pixi/SuperBuild; large datasets resource-intensive.
- **Platforms:** Linux Docker amd64/arm64, Windows, macOS, optional NVIDIA GPU.
- **License:** AGPL-3.0 root; native dependencies/assets separately licensed; no code copied.
- **Maintenance signals:** Stable 3.6.2 on 2026-08-12; 2026-09-16 native CI 4/4 green; recurring Windows installer publishing failures.
- **Verification performed:** 2026-10-25: README, AGPL LICENSE, stages/modules/tests, native/Docker workflows inspected; Stable v3.6.2 released 2026-08-12; master 77439b1 merged OpenSfM v110 on 2026-09-15; Upstream 2026-09-16 Native Builds 35092809957 passed 4/4 Linux/ARM/Windows/macOS jobs with Test, Smoke and Prod smoke steps; Upstream 2026-09-15 Docker CPU 34975847090 passed 5/5 jobs; 2026-09-15 Windows Setup publish 34975845646 failed; later October PR action_required is not test execution; No independent aerial reconstruction, GCP accuracy, GPU benchmark or installer testing.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** OpenDroneMap/NodeODM; OpenDroneMap/WebODM; mapillary/OpenSfM.
- **Caveats / risks:** AGPL obligations; reconstruction accuracy depends on image overlap and georeferencing. Windows installer CI failure remains unresolved.
- **Research notes:** `research/2026-10-25-renode-odm-maintenance.md`. Docker or native pixi/SuperBuild; high CPU/RAM/disk demands. AGPL network copyleft and dependency licenses. Verify GCP residuals, reflectance/NoData, orthophoto repeatability, Windows packaging.


### Ghidra

- **Repository:** https://github.com/NationalSecurityAgency/ghidra
- **Author / Org:** National Security Agency Research Directorate
- **Category:** Defensive reverse engineering / decompilation / binary analysis / forensics
- **Evidence:** VERIFIED (upstream release and successful build; no independent runtime tests)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 4)
- **What it does:** Extensible disassembler, decompiler, debugger and binary-analysis platform supporting numerous processors and executable formats.
- **Why it is valuable:** Reusable SLEIGH/p-code processor semantics, decompiler API, headless automation and scripting for legitimate firmware analysis and interoperability.
- **Useful code/components:** `Ghidra/Features/Decompiler/src/main/java/ghidra/app/decompiler/DecompInterface.java`; `Ghidra/Features/Decompiler/src/decompile/cpp/sleigh.hh`; `Ghidra/Features/Base/src/main/java/ghidra/app/util/headless/AnalyzeHeadless.java`; `Ghidra/RuntimeScripts/support/analyzeHeadless`; `Ghidra/RuntimeScripts/support/sleigh`.
- **Install / runtime:** Official multi-platform ZIP, JDK 25 64-bit; source Gradle 9.1+, Python 3.9–3.15, native toolchains. Master declares 12.3 DEV, not a stable release.
- **Platforms:** Windows, macOS, Linux.
- **License:** Apache-2.0 core. `NOTICE` documents GPL-3 stand-alone support tools and module-specific third-party licensing; inspect `LICENSE.txt` before copying.
- **Maintenance signals:** [Stable 12.2](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build) released 2026-10-22; [upstream Ubuntu Gradle build 39747670372](https://github.com/NationalSecurityAgency/ghidra/actions/runs/39747670372) passed 2026-10-22. The build workflow does not establish a full regression suite.
- **Verification performed:** README, LICENSE, NOTICE, version manifest, Gradle workflow, SLEIGH/decompiler source, headless CLI and release inspected. No local build, binary processing, fuzzing or security audit.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `rizinorg/rizin` (independent alternative), `NationalSecurityAgency/ghidra-data`, `rizinorg/cutter`.
- **Caveats / risks:** Treat untrusted binaries as hostile. [Decompiler use-after-free](https://github.com/NationalSecurityAgency/ghidra/security/advisories/GHSA-8jqp-qv73-395r) and [Mach-O export-trie exhaustion](https://github.com/NationalSecurityAgency/ghidra/security/advisories/GHSA-wm33-9f68-3vjg) affected older versions and were patched in 12.1.
- **Research notes:** `research/2026-10-25-ghidra-openmct.md`. Next: SLEIGH, PyGhidra and parser fuzzing.

### Open MCT

- **Repository:** https://github.com/nasa/openmct
- **Author / Org:** NASA Ames Research Center
- **Category:** Telemetry visualization / mission control / browser dashboards / JavaScript
- **Evidence:** PROMISING (released project and test source, but current e2e run fails before tests)
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 3)
- **What it does:** Extensible browser framework for time-series telemetry, plots, timelines, status and operations planning.
- **Why it is valuable:** Composable telemetry providers/subscriptions, WebSocket batching, persistence and dashboard APIs for robotics, instrumentation and monitoring.
- **Useful code/components:** `src/api/telemetry/TelemetryAPI.js`, `BatchingWebSocket.js`, `TelemetryCollection.js`, `src/plugins/persistence/couch/`, `src/api/plan/PlanAPI.js`, `API.md`, `e2e/tests/`.
- **Install / runtime:** Node/npm/webpack and modern browser; `npm install`, `npm start`, `npm run build`. Current `package.json` requires Node >=24.14.1.
- **Platforms:** Browsers; Linux, macOS and Windows/WSL development hosts.
- **License:** Apache-2.0 core (`LICENSE.md`); dependency/asset licenses separate. Source headers mention `LICENSES.md`, not found at inspected root.
- **Maintenance signals:** [Stable v4.3.1](https://github.com/nasa/openmct/releases/tag/v4.3.1) released 2026-08-31; latest inspected master commit 2026-10-07. [e2e-full 40147454572](https://github.com/nasa/openmct/actions/runs/40147454572) FAILED 2026-10-25 at Ubuntu `npm ci`; Playwright tests skipped, Windows cancelled. Workflow uses Node `lts/hydrogen` (18) while package engine requires >=24.14.1. The 2026-10-26 [Ubuntu e2e-full job log](https://github.com/nasa/openmct/actions/runs/40250211098) confirms `npm ci` failed `EBADENGINE`: actual Node v18.20.8, required >=24.14.1. Other workflow failures remain undiagnosed. Subsequent 2026-10-26 UTC [e2e-full 40250211098](https://github.com/nasa/openmct/actions/runs/40250211098) also failed (Ubuntu failure, Windows cancelled); e2e-perf 40248391927 and pr-platform 40247907640 failed. 2026-10-27 [e2e-full 40427389616](https://github.com/nasa/openmct/actions/runs/40427389616) Ubuntu log confirms npm ci EBADENGINE (Node 18.20.8 vs required >=24.14.1); no Playwright run.
- **Verification performed:** README, LICENSE.md, package.json, API.md, telemetry source, e2e workflow and job steps inspected. No local install, browser test or telemetry execution.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `nasa/openmct-tutorial`, `nasa/openmct-map`, `akhenry/openmct-yamcs`; OpenTelemetry Collector is a conceptual neighbor, not confirmed integration.
- **Caveats / risks:** No passing current full e2e execution verified. Review plugin input sanitization, WebSocket reconnection, CouchDB permissions and packaged licenses.
- **Research notes:** `research/2026-10-25-ghidra-openmct.md`. 2026-10-27 UTC: [e2e-full 40427389616](https://github.com/nasa/openmct/actions/runs/40427389616) failed Ubuntu `npm ci` (Windows cancelled); [e2e-perf 40424992380](https://github.com/nasa/openmct/actions/runs/40424992380) failed at `npm ci`. Previous Node mismatch confirmed, latest exact failure cause not independently checked. Rechecked 2026-10-26 UTC: three scheduled workflows remain failed. Node mismatch confirmed by Ubuntu `EBADENGINE` log as the e2e-full `npm ci` cause. Keep PROMISING/25; update CI Node >=24.14.1 and require passing Playwright e2e before promotion.

### Zigbee2MQTT

- **Repository:** https://github.com/Koenkk/zigbee2mqtt
- **Author / Org:** Koen Kanters / Koenkk
- **Category:** Zigbee / MQTT / IoT / local-first automation / device interoperability
- **Evidence:** VERIFIED (upstream CI; no independent hardware test)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Bridges supported Zigbee devices into MQTT topics without a proprietary vendor gateway.
- **Why it is valuable:** Practical, modular local automation infrastructure with reusable Zigbee device state, event translation, firmware OTA handling, topology and MQTT integration.
- **Useful code/components:** `lib/zigbee.ts` Zigbee lifecycle; `lib/mqtt.ts` MQTT transport; `lib/controller.ts` orchestration; `lib/extension/otaUpdate.ts` OTA; `networkMap.ts` topology; `availability.ts` health; `homeassistant.ts` integration; `test/` Vitest tests.
- **Install / runtime:** Node.js as constrained by `package.json` (`^22.2.0 || ^24 || <=26.2`), pnpm 11, MQTT broker, compatible Zigbee USB/network coordinator; Docker packages available.
- **Platforms:** Linux, Windows, macOS, ARM/Docker hosts; Zigbee coordinator hardware required for radio use.
- **License:** GPL-3.0 root; `Koenkk/zigbee-herdsman` and `Koenkk/zigbee-herdsman-converters` are separately MIT licensed. Review dependency notices before extracting.
- **Maintenance signals:** Stable 2.14.2 released 2026-10-01; upstream dev [CI 40171469797](https://github.com/Koenkk/zigbee2mqtt/actions/runs/40171469797) passed 10/10 jobs on 2026-10-25 (Linux/Windows/macOS, Node 22/24/26; check/build/tests).
- **Verification performed:** README, license, package manifest, lib/extension tree, test suite and CI job steps inspected. No independent MQTT connection, coordinator pairing, firmware OTA, RF or security tests.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `Koenkk/zigbee-herdsman`, `Koenkk/zigbee-herdsman-converters`, `zigbee2mqtt/hassio-zigbee2mqtt`.
- **Caveats / risks:** Device support and OTA reliability vary. Secure MQTT credentials, Zigbee pairing and exposed web UI. GPL obligations for covered copied code; no source copied.
- **Research notes:** `research/2026-10-25-zigbee2mqtt-sdrpp.md`. Follow network-key handling, OTA validation and device-converter tests.

### SDR++

- **Repository:** https://github.com/AlexandreRouma/SDRPlusPlus
- **Author / Org:** Alexandre Rouma
- **Category:** SDR / digital signal processing / modular radio receivers / cross-platform
- **Evidence:** VERIFIED (upstream cross-platform build evidence; no independent RF reception)
- **Tier / Score:** S / 26 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** Cross-platform modular software-defined-radio receiver with hardware source plugins, waterfall display, multiple VFOs, demodulators and recording.
- **Why it is valuable:** Reusable C++ DSP blocks, IQ streaming, VFO management, plugin interfaces and optional decoders; complements the existing SoapySDR and OpenRTX entries.
- **Useful code/components:** `core/src/dsp/` filters/demodulators/streams; `core/src/signal_path/` IQ frontend and VFO; `core/src/module.{cpp,h}` plugin interfaces; `source_modules/soapy_source/`, `rtl_sdr_source/`, `rtl_tcp_source/`; `decoder_modules/m17_decoder/`, `meteor_demodulator/`; `misc_modules/` recorder/scanner.
- **Install / runtime:** C++17/CMake; system libraries including FFTW, GLFW and audio backends; radio hardware requires appropriate vendor drivers; Android build exists but runtime not validated.
- **Platforms:** Windows, Linux, macOS, BSD source builds, Android build target.
- **License:** GPL-3.0 root; bundled `core/libcorrect` and third-party SDR vendor SDKs/modules require separate license review before reuse.
- **Maintenance signals:** [Upstream Build Binaries 39896187183](https://github.com/AlexandreRouma/SDRPlusPlus/actions/runs/39896187183) passed 22/22 jobs on 2026-10-23, including Windows, macOS x86/ARM, Linux variants, Android APK build and formatting checks. Last confirmed numbered stable GitHub tag 1.0.4 dates to 2021-10-17; rolling nightly release is not a newly dated stable release.
- **Verification performed:** README, license, CMake build switches, DSP/signal-path/source/decoder trees, Android project and upstream CI jobs inspected. No independent build, device RF test, decoder verification or Android installation.
- **Source discovery:** GitHub-first; no YouTube attribution.
- **Related projects:** `pothosware/SoapySDR`, `pothosware/SoapyRemote`, `OpenRTX/OpenRTX` (M17 ecosystem only), `AlexandreRouma/libperseus-sdr`.
- **Caveats / risks:** CI compilation does not demonstrate device-specific RF correctness. Some optional decoders are disabled by default; drivers and vendor SDKs have independent licensing. Protect remote interfaces and comply with radio laws. No source copied.
- **Research notes:** `research/2026-10-25-zigbee2mqtt-sdrpp.md`. Follow M17 decoding and Soapy plugin compatibility, Android runtime and bundled-code licenses.


### CyberChef

- **Repository:** https://github.com/gchq/CyberChef
- **Author / Org:** GCHQ
- **Category:** Browser-based data transformation / encoding / decoding / forensics / local-first utilities
- **Evidence:** VERIFIED (upstream Node and browser CI; no independent execution)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Composable browser recipes for text and binary transformations, encoding/decoding, compression, hashes, parsing and data inspection.
- **Why it is valuable:** Reusable typed operation pipeline with a large collection of individual operations, a Node interface and browser UI; can run from a locally hosted build.
- **Useful code/components:** `src/core/Chef.mjs` recipe execution; `Recipe.mjs` sequencing; `Dish.mjs` typed data; `Operation.mjs` extension contract; `src/core/operations/` operation implementations; `src/node/` API; `tests/operations/`, `tests/node/`, `tests/browser/`.
- **Install / runtime:** Node.js 24 supported (26 CI tested); `npm ci`, `npm run build`, `npm test`; Docker image or local browser build. Browser/Node versions and dependency requirements should be checked for deployed versions.
- **Platforms:** Browser on desktop systems, Node.js and Docker; offline usage possible with locally built assets.
- **License:** Apache-2.0 root and core file headers. Bundled and npm dependencies retain their own licenses.
- **Maintenance signals:** Stable [v11.5.0](https://github.com/gchq/CyberChef/releases/tag/v11.5.0) released 2026-09-18; [upstream master CI 39942157083](https://github.com/gchq/CyberChef/actions/runs/39942157083) passed 2/2 Node 24/26 jobs on 2026-10-23, including lint, unit tests, production builds and browser UI tests.
- **Verification performed:** Inspected README, LICENSE, SECURITY.md, package.json, core operation architecture, test tree, workflow and upstream CI job steps. No independent build, browser recipe execution or cryptographic verification.
- **Source discovery:** GitHub-first; no usable YouTube transcript evidence.
- **Related projects:** Node consumer API; Tesseract.js dependency (not the native Tesseract engine).
- **Caveats / risks:** Upstream SECURITY.md explicitly warns cryptographic operations should not be relied on for security guarantees. Review individual dependencies and operation implementations before reuse. Handle confidential data and recipe URLs carefully. No third-party code copied.
- **Research notes:** `research/2026-10-25-cyberchef-rtl433.md`. Follow operation-level test coverage, input size limits, browser security and dependency licenses.

### rtl_433

- **Repository:** https://github.com/merbanan/rtl_433
- **Author / Org:** Benjamin Larsson and rtl_433 contributors / merbanan
- **Category:** SDR / ISM-band sensor decoding / RF signal processing / embedded C / local IoT telemetry
- **Evidence:** VERIFIED (upstream builds, unit/integration tests and static analysis; no independent RF test)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** Receives and decodes signals from compatible unlicensed-band sensors and devices using RTL-SDR or SoapySDR, or analyzes recorded sample files.
- **Why it is valuable:** Hundreds of device decoder source files, reusable pulse detection/bit parsing, low-resource C99 implementation and output bridges for MQTT, JSON, CSV and other sinks.
- **Useful code/components:** `src/pulse_detect.c`, `pulse_detect_fsk.c`, `pulse_slicer.c` for demodulation; `src/bitbuffer.c` bit parsing; `src/devices/` protocol decoders; `src/output_mqtt.c`, `output_influx.c`, `http_server.c`; `tests/` unit and HTTP integration suites.
- **Install / runtime:** C99/CMake or platform packages; supported RTL-SDR/SoapySDR hardware for live reception, or input IQ files for offline decoding.
- **Platforms:** Linux (including ARM/embedded), FreeBSD, macOS, Windows; device support depends on drivers.
- **License:** GPL-2.0-or-later in examined core source; COPYING contains GPL-2.0 text. Review vendored components and device files separately.
- **Maintenance signals:** Stable [25.12](https://github.com/merbanan/rtl_433/releases/tag/25.12) released 2025-12-12; [upstream CI 39967799370](https://github.com/merbanan/rtl_433/actions/runs/39967799370) passed 12/12 jobs on 2026-10-23 (Linux/macOS build/tests, coverage, Clang analysis, style, docs). A later [2026-10-24 run](https://github.com/merbanan/rtl_433/actions/runs/40144928023) concluded `action_required`; investigate before claiming all latest checks green.
- **Verification performed:** README, COPYING, source license headers, CMake, `src/`, `src/devices/`, `tests/`, workflow and CI job steps inspected. Linux matrix disables hardware backends; no live RF capture or decoder accuracy test performed.
- **Source discovery:** GitHub-first; no usable YouTube transcript evidence.
- **Related projects:** `pothosware/SoapySDR`, `osmocom/rtl-sdr`, `pothosware/SoapyRemote`, SDR++ (complementary SDR receiver, no direct integration confirmed).
- **Caveats / risks:** Device-specific decoders require representative capture testing. Secure MQTT, HTTP and remote receiver interfaces; sensor telemetry may reveal location or activity. RF use subject to applicable rules. GPL obligations and vendored code licenses apply; no code copied.
- **Research notes:** `research/2026-10-25-cyberchef-rtl433.md`. Follow decoder test coverage, malformed-packet robustness and SoapySDR hardware integration.


### ESPHome

- **Repository:** https://github.com/esphome/esphome
- **Author / Org:** ESPHome / Open Home Foundation ecosystem
- **Category:** Embedded firmware / ESP32 / ESP8266 / local-first home automation / YAML code generation / IoT
- **Evidence:** VERIFIED (upstream release and CI; no independent hardware or firmware test)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Generates configurable microcontroller firmware from declarative YAML for local sensors, controls, device integrations and automation.
- **Why it is valuable:** Reusable configuration-validation, code-generation and device-component architecture, with OTA recovery and native encrypted API; can operate locally without mandatory cloud services.
- **Useful code/components:** `esphome/config.py` YAML packages/substitutions/validation; `esphome/codegen.py` and `cpp_generator.py` C++ generation; `esphome/components/api/` native API and Noise configuration; `ota/` and `safe_mode/` firmware updates/recovery; `mqtt/`, `modbus/`, `esp32_ble/` integration modules; `tests/integration/` regression fixtures.
- **Install / runtime:** Python >=3.12,<3.16 per `pyproject.toml`, PlatformIO/ESP-IDF and appropriate toolchains for target boards; CLI or supported device-builder workflow; flashing requires appropriate hardware and drivers.
- **Platforms:** ESP32, ESP8266, RP2 and selected LibreTiny/Zephyr targets; Python development hosts. Verify each specific board/framework before use.
- **License:** **Split license:** Python and other non-C++ files MIT; C/C++ firmware/runtime files GPLv3 by root `LICENSE`. Dependencies and external components may have other licenses. Do not treat the entire repository as MIT based on package metadata.
- **Maintenance signals:** [Stable 2026.10.0](https://github.com/esphome/esphome/releases/tag/2026.10.0) released 2026-10-21; active 2026-10-25 development commits. [Upstream PR CI 40218426253](https://github.com/esphome/esphome/actions/runs/40218426253) completed **28 successful, 2 skipped** jobs on 2026-10-25 (integration tests, C++ tests, component builds, static checks).
- **Verification performed:** Inspected README, root license, Python manifest, configuration/codegen, API, OTA, safe-mode, MQTT source and CI workflow; inspected upstream CI job results. No independent build, flash, MQTT connection, OTA recovery or device security test.
- **Source discovery:** GitHub-first; no usable YouTube transcript evidence.
- **Related projects:** `home-assistant/core` (ecosystem); `Koenkk/zigbee2mqtt` (complementary local IoT bridge, not a direct integration); `esphome/esphome.io` documentation.
- **Caveats / risks:** YAML external components are executable build inputs; protect API encryption keys, OTA authentication and device credentials. Firmware reliability and resource use vary by board. GPLv3 obligations apply to C++ runtime reuse. No source copied.
- **Research notes:** `research/2026-10-25-esphome-gnuradio.md`. Investigate API Noise session handling, OTA rollback and external-component trust.

### GNU Radio

- **Repository:** https://github.com/gnuradio/gnuradio
- **Author / Org:** GNU Radio contributors / gnuradio
- **Category:** Software-defined radio / digital signal processing / C++ / Python / radio simulation / flowgraphs
- **Evidence:** VERIFIED (upstream multi-distro tests; no independent flowgraph or radio-hardware execution)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** C++/Python DSP block runtime and visual flowgraph toolkit for SDR receivers, digital communications, protocol research and offline signal processing.
- **Why it is valuable:** Mature composable DSP blocks, schedulers, modulation and channel models, visual graph construction, testing utilities and vendor-neutral SDR interfaces.
- **Useful code/components:** `gnuradio-runtime/lib/top_block_impl.cc` runtime; `gr-digital/lib/` OFDM/CRC/synchronization; `gr-filter/lib/` DSP filters; `gr-analog/`, `gr-fft/` signal generation/FFT; `gr-soapy/` SoapySDR adapter; `grc/core/FlowGraph.py` flowgraph model; `gr-utils/modtool/` block scaffolding; `gr-digital/python/digital/qa_ofdm_*.py` tests.
- **Install / runtime:** Debian/Ubuntu package `gnuradio` or platform-specific packages; source CMake build needs C++ compiler, Python and DSP/GUI dependencies (Boost, VOLK, optional Qt and SoapySDR).
- **Platforms:** Linux (multi-distro CI), Windows/macOS via supported packaging/build methods; live RF requires SDR hardware and compatible drivers, offline flowgraphs do not.
- **License:** GPL-3.0-or-later for examined core (`COPYING` and SPDX source headers); review dependencies and external modules individually.
- **Maintenance signals:** Latest inspected stable GitHub release [v3.10.12.0](https://github.com/gnuradio/gnuradio/releases/tag/v3.10.12.0) dates to **2025-02-20**; main development remains active in October 2026. [Upstream Make Test 39263827649](https://github.com/gnuradio/gnuradio/actions/runs/39263827649) on PR #8240 passed **10/10 jobs** (Ubuntu, Fedora, Debian, 32-bit and clang). Separate [Conda build 39263827623](https://github.com/gnuradio/gnuradio/actions/runs/39263827623) **failed 2/2 jobs**; do not call all CI green.
- **Verification performed:** Inspected README, COPYING, CMake, runtime, digital/filter sources, Soapy integration, GRC, module tooling and CI workflow; checked upstream jobs. No independent installation, DSP flowgraph execution, RF reception or security test.
- **Source discovery:** GitHub-first; no usable YouTube transcript evidence.
- **Related projects:** `pothosware/SoapySDR` (in-tree `gr-soapy` adapter); `gnuradio/gnuradio4` (separate next-generation C++23 codebase); SDR++; `merbanan/rtl_433` (complementary decoding).
- **Caveats / risks:** Conda packaging currently has failed upstream CI evidence. Recent 2026 DVB-T buffer-overflow and channel-model correctness fixes warrant review of parser boundaries and DSP test vectors. GNU Radio 4 is not assumed drop-in compatible. Comply with spectrum rules; no source copied.
- **Research notes:** `research/2026-10-25-esphome-gnuradio.md`. Follow Conda packaging, gr-soapy integration, malformed-stream testing and GNU Radio 4 migration.

### OpenThread

- **Repository:** https://github.com/openthread/openthread
- **Author / Org:** OpenThread (Google and contributors)
- **Category:** Thread IPv6 mesh / IEEE 802.15.4 / embedded networking / IoT / border routers
- **Evidence:** VERIFIED (upstream build, unit, POSIX, simulation and border-router CI)
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Portable implementation of the Thread mesh protocol with IPv6/6LoWPAN, link security, routing, commissioning and border-router support.
- **Why it is valuable:** Reusable standards-based low-power mesh stack, portable hardware abstraction and reproducible network simulation; complements rather than replaces Zigbee implementations.
- **Useful code/components:** `src/core/thread/mesh_forwarder.cpp` (6LoWPAN packet forwarding); `src/core/thread/key_manager.cpp` (security material); `src/core/thread/mle.cpp` and `router_table.cpp` (mesh establishment/routing); `src/core/net/`, `src/core/mac/`, `src/posix/`; `tests/unit/`, `tests/toranj/`, `tests/fuzz/`.
- **Install / runtime:** CMake/GN and C/C++ host toolchain; Thread-capable IEEE 802.15.4 hardware for real RF, or POSIX simulation without hardware. Board-specific builds and integration vary.
- **Platforms:** Embedded SoC/NCP/RCP; Linux/macOS POSIX development and simulation.
- **License:** BSD-3-Clause at root and inspected core files; preserve notices and review `third_party/` separately.
- **Maintenance signals:** Stable [v2026.10.0](https://github.com/openthread/openthread/releases/tag/v2026.10.0) published 2026-10-01; active main 2026-10-25. Upstream [Build 40228441197](https://github.com/openthread/openthread/actions/runs/40228441197) passed 54/54, [Unit 40228441160](https://github.com/openthread/openthread/actions/runs/40228441160) 3/3, [POSIX 40228441091](https://github.com/openthread/openthread/actions/runs/40228441091) 10/10, [Simulation 40228441202](https://github.com/openthread/openthread/actions/runs/40228441202) 6/6, [Border Router 40228441070](https://github.com/openthread/openthread/actions/runs/40228441070) 4/4 (2026-10-25).
- **Verification performed:** README, LICENSE, CMake, core forwarding/key-management source, tests tree and workflow inspected; upstream successful CI reviewed. No independent build, hardware, commissioning, RF or security test.
- **Source discovery:** GitHub-first; no accessible YouTube transcript attribution.
- **Related projects:** `openthread/ot-br-posix` (border router), `openthread/ot-ns` (network simulation), `zephyrproject-rtos/zephyr` (RTOS ecosystem); Zigbee2MQTT uses a distinct protocol.
- **Caveats / risks:** Mesh key storage and commissioning security require review; passing simulation is not physical radio reliability or Thread certification. Third-party licensing separate; no code copied.
- **Research notes:** `research/2026-10-25-openthread-ardupilot-renode.md`. Follow commissioning, border-router privileges, multi-vendor radio interoperability and fuzz harnesses.

### ArduPilot

- **Repository:** https://github.com/ArduPilot/ardupilot
- **Author / Org:** ArduPilot
- **Category:** Robotics / autopilot / embedded vehicle control / navigation / MAVLink / simulation
- **Evidence:** VERIFIED (upstream SITL, unit-build and downstream Renode integration CI)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 5)
- **What it does:** Open-source autopilot firmware and supporting libraries for copters, planes, rovers, submarines and other autonomous vehicles.
- **Why it is valuable:** Mature modular flight-control, sensor-fusion, hardware abstraction, navigation, safety/failsafe and software-in-the-loop test components.
- **Useful code/components:** `libraries/AP_NavEKF3/` (navigation EKF), `libraries/AC_AttitudeControl/` (attitude/rate loops), `libraries/AP_HAL_SITL/` and `Tools/autotest/` (simulation), `libraries/GCS_MAVLink/`, `libraries/AP_GPS/`, `libraries/AP_Avoidance/`, `Tools/renode/` (board-level emulator integration).
- **Install / runtime:** Git clone with recursive submodules, Python/Waf build toolchain; board-specific ChibiOS toolchains for embedded firmware or SITL development environment.
- **Platforms:** Supported flight controllers, Linux SBC and SITL; platform-specific desktop development.
- **License:** GPL-3.0 root `COPYING.txt`; individual files, submodules and bundled dependencies require separate checks.
- **Maintenance signals:** Vehicle-specific stable v4.7.2 releases published 2026-10-14. On 2026-10-25, upstream [unit/SITL build 40231792309](https://github.com/ArduPilot/ardupilot/actions/runs/40231792309) passed 8/8 jobs, [Copter 40231792304](https://github.com/ArduPilot/ardupilot/actions/runs/40231792304) 12/12, [Plane 40231792276](https://github.com/ArduPilot/ardupilot/actions/runs/40231792276) 7/7; [Renode integration 40231792336](https://github.com/ArduPilot/ardupilot/actions/runs/40231792336) passed a CubeOrangePlus quadplane mission and emulator unit tests.
- **Verification performed:** README, COPYING, BUILD.md, EKF/control source, SITL workflows, Renode integration scripts/tests and CI job steps inspected. No independent build, simulation, firmware flashing, flight or safety audit.
- **Source discovery:** GitHub-first; no accessible YouTube transcript attribution.
- **Related projects:** `renode/renode` (ArduPilot-patched downstream integration), `mavlink/mavlink`, `ArduPilot/pymavlink`, `ArduPilot/MAVProxy`, `PX4/PX4-Autopilot` (alternative ecosystem), `mavlink/MAVSDK` (SDK, integration untested).
- **Caveats / risks:** GPL copyleft; embedded hardware/sensor compatibility and aviation safety are not established by CI. Renode tests use an ArduPilot-hosted, checksum-verified custom Renode package, not necessarily upstream stock Renode. No code copied.
- **Research notes:** `research/2026-10-25-openthread-ardupilot-renode.md`. Investigate EKF failures, failsafes, GPS denial, mission regression, and MAVLink trust boundaries.

### OpenThread Border Router

- **Repository:** https://github.com/openthread/ot-br-posix
- **Author / Org:** openthread
- **Category:** thread-networking / ipv6-border-router / nat64 / dns-srp-mdns / iot / embedded-gateway
- **Evidence:** VERIFIED (upstream CI; no independent runtime/hardware test)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Connects Thread mesh networks to external IP networks using IPv6 routing, service discovery, DHCPv6 prefix delegation, NAT64 and commissioning.
- **Why it is valuable:** Practical Thread gateway with reusable service-discovery proxies, REST diagnostics, D-Bus interfaces, host firewall and routing regression tests.
- **Useful code/components:** `src/agent/application.cpp` — border router daemon; `src/border_agent/border_agent.cpp` — Thread border agent; `src/sdp_proxy/advertising_proxy.cpp and discovery_proxy.cpp` — SRP/mDNS bridging; `src/mdns/mdns_openthread.cpp and mdns_mdnssd.cpp` — mDNS backends; `src/dbus/server/dbus_agent.cpp` — D-Bus control plane; `src/rest/rest_web_server.cpp and src/rest/openapi.yaml` — commissioning and diagnostics HTTP API; `script/_firewall, script/_nat64 and src/agent/nftables-backend.in` — host firewall and NAT; `tests/scripts/thread-cert/border_router/` — simulated routing tests.
- **Install / runtime:** CMake/POSIX, Raspberry Pi, Docker or OpenWrt packaging; radio RCP/NCP and host networking privileges required for live Thread.
- **Platforms:** Linux; Raspberry Pi; OpenWrt; Docker amd64/arm64/armv7; macOS CI; IEEE 802.15.4 RCP/NCP hardware for live use.
- **License:** BSD-3-Clause (root LICENSE and inspected scripts); third-party dependencies separately licensed.
- **Maintenance signals:** v2026.10.0 (2026-10-01), active 2026-10-25; upstream [Border Router 7/7](https://github.com/openthread/ot-br-posix/actions/runs/40165604861), [Build 13/13](https://github.com/openthread/ot-br-posix/actions/runs/40165604824), [Docker 3 builds](https://github.com/openthread/ot-br-posix/actions/runs/40165604873) succeeded (merge skipped).
- **Verification performed:** 2026-10-26 inspected README, BSD-3-Clause LICENSE, REST API docs, NAT/firewall scripts, source tree, workflow and releases; Stable v2026.10.0 published 2026-10-01; 2026-10-25 Border Router 40165604861 passed 7/7; Build 40165604824 passed 13/13; Docker Border Router 40165604873 had 3 passed and 1 skipped; OpenWrt 40165604857, Raspbian 40165604829, macOS 40165604856 succeeded; No independent build, commissioning, radio, gateway deployment or security audit.
- **Source discovery:** GitHub-first; research/2026-10-26-otbr-open62541-maintenance.md; no YouTube transcript evidence.
- **Related projects:** openthread/openthread; openthread/ot-ns; zephyrproject-rtos/zephyr.
- **Caveats / risks:** Review commissioning/diagnostics REST authorization, D-Bus access, host firewall/nftables/pf and network-key protection. Upstream simulated tests do not verify radio interoperability.
- **Research notes:** `research/2026-10-26-otbr-open62541-maintenance.md`. BSD-3-Clause notices required; inspect third-party licensing. Research REST authentication and RCP compatibility. No code copied.


### open62541

- **Repository:** https://github.com/open62541/open62541
- **Author / Org:** open62541
- **Category:** industrial-automation / opc-ua / c-library / pubsub / embedded-networking / protocol-implementation
- **Evidence:** VERIFIED (upstream CI; no independent runtime/hardware test)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Portable C99 implementation of OPC UA (IEC 62541) clients, servers, subscriptions, PubSub and security plugins.
- **Why it is valuable:** Reusable industrial communication stack with Zephyr support, single-file amalgamation, upstream fuzzing and OpenSSL/mbedTLS interoperability tests.
- **Useful code/components:** `src/client/ua_client.c and ua_client_subscriptions.c` — client and subscription APIs; `src/server/ua_server.c and ua_services_securechannel.c` — server and secure channels; `src/pubsub/ua_pubsub_networkmessage_binary.c and ua_pubsub_networkmessage_json.c` — PubSub codecs; `src/pubsub/ua_pubsub_keystorage.c` — PubSub key storage; `plugins/crypto/openssl/ and plugins/crypto/mbedtls/` — security policy backends; `arch/zephyr/eventloop_zephyr.c` — Zephyr event loop; `tests/fuzz/fuzz_binary_message.cc` — parser fuzzing; `tests/interop/` — cross-SDK interoperability; `CMakeLists.txt UA_ENABLE_AMALGAMATION` — single-file C distribution.
- **Install / runtime:** C99 compiler, CMake and Python for generated definitions; optional OpenSSL/mbedTLS; UA_ENABLE_AMALGAMATION emits combined open62541.c/.h.
- **Platforms:** Linux; Windows; macOS; Zephyr; FreeRTOS/lwIP; C99/CMake/Python generator; OpenSSL or mbedTLS optional.
- **License:** MPL-2.0 core; select examples/plugins CC0; deps/README.md documents separately licensed MIT, BSD, Apache, Boost and MPL components.
- **Maintenance signals:** v1.5.9 (2026-10-04); [interop 2/2](https://github.com/open62541/open62541/actions/runs/40294086389), [CIFuzz 1/1](https://github.com/open62541/open62541/actions/runs/40294086435), [Windows 4/4](https://github.com/open62541/open62541/actions/runs/40294086561), Zephyr/macOS passed 2026-10-26. [CodeQL](https://github.com/open62541/open62541/actions/runs/40294086468) blocked by missing clang-tools-14; Linux still running.
- **Verification performed:** 2026-10-26 inspected README, FEATURES.md, MPL-2.0 LICENSE, deps/README.md, CMake, client/server/PubSub/Zephyr source and workflows; Stable v1.5.9 published 2026-10-04; 2026-10-26 upstream interop 40294086389 passed 2/2, CIFuzz 40294086435 passed 1/1, Windows 40294086561 passed 4/4; Zephyr 40294086507 and macOS 40294086387 succeeded; Linux 40294086564 had 18 successful and 12 in-progress jobs at inspection; no overall pass claimed; Code Scanning 40294086468 failed 2/2 before CodeQL analysis: job log reports missing apt package clang-tools-14; not evidence of code vulnerability; No independent build, OPC UA connection, fuzz run, industrial hardware or security audit.
- **Source discovery:** GitHub-first; research/2026-10-26-otbr-open62541-maintenance.md; no YouTube transcript evidence.
- **Related projects:** OPCFoundation/UA-.NETStandard; zephyrproject-rtos/zephyr.
- **Caveats / risks:** Certificate trust, legacy cryptography, PubSub SKS and exposed server defaults require review. CodeQL failure was dependency installation, not a scan finding.
- **Research notes:** `research/2026-10-26-otbr-open62541-maintenance.md`. MPL-2.0 file-level copyleft; CC0 only for specifically marked files. Upstream reports certification for a v1.4 example server, not arbitrary current deployments. No code copied.


### OpenWrt

- **Repository:** https://github.com/openwrt/openwrt
- **Author / Org:** OpenWrt
- **Category:** Embedded Linux / router firmware / firewall / network infrastructure / image building
- **Evidence:** VERIFIED (upstream build CI; no independent hardware testing)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Customizable Linux firmware and package/image build system for supported routers and embedded networking hardware.
- **Why it is valuable:** Reusable embedded build infrastructure, network configuration, firewall integration, reproducible image assembly and extensive device targeting.
- **Useful code/components:** `scripts/feeds` (feed management); `package/network/config/netifd/files/` (network configuration); `package/network/config/firewall4/` (nftables); `package/base-files/files/etc/` (init/hotplug); `target/imagebuilder/Makefile` (image builder); `scripts/gen_image_generic.sh` (reproducible image assembly); `target/linux/` and `toolchain/`.
- **Install / runtime:** Build with host toolchain on case-sensitive GNU/Linux/BSD/macOS; run `scripts/feeds update -a`, `scripts/feeds install -a`, `make menuconfig`, `make`. Flash only verified supported device/board images.
- **Platforms:** Supported embedded routers/network devices; Linux/BSD/macOS build hosts.
- **License:** GPL-2.0-only root COPYING; inspect third-party package, kernel and driver licenses separately.
- **Maintenance signals:** [v25.12.6](https://github.com/openwrt/openwrt/releases/tag/v25.12.6) 2026-10-18; active 2026-10-26. [Kernel 40231519176](https://github.com/openwrt/openwrt/actions/runs/40231519176) 29/29 and [core packages 40231388127](https://github.com/openwrt/openwrt/actions/runs/40231388127) 10/10 passed on 2026-10-25; toolchain workflow 40231388106 succeeded.
- **Verification performed:** Inspected README, COPYING, package/target/scripts source, APK Makefile, image builder and upstream workflows. No independent build, flash, network operation or security audit.
- **Source discovery:** GitHub-first 2026-10-26; YouTube playlist fetches throttled; no transcript-derived claims.
- **Related projects:** `openwrt/luci`, `openwrt/packages`, `openwrt/routing`, `openwrt/actions-shared-workflows`.
- **Caveats / risks:** Device-specific flashing can brick hardware. README references opkg, but current APK package and image builder support APK/OPKG configurations; verify target/release. Root GPL does not cover every dependency. No code copied.
- **Research notes:** `research/2026-10-26-openwrt-mavsdk.md`. Follow sysupgrade recovery, firewall tests, image reproducibility and package-manager transition.

### MAVSDK

- **Repository:** https://github.com/mavlink/MAVSDK
- **Author / Org:** MAVLink / MAVSDK
- **Category:** Robotics / MAVLink / telemetry / mission control / cross-platform SDK
- **Evidence:** VERIFIED (upstream CI; no independent simulator or vehicle test)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 4 + Maintenance 4)
- **What it does:** C++ MAVLink SDK with direct C, Python and Kotlin bindings, mission, telemetry, offboard-control and raw-message plugins.
- **Why it is valuable:** Reusable protocol clients and portable language bindings, examples, fuzz tests and broad platform support.
- **Useful code/components:** `cpp/src/mavsdk/core/mavsdk_impl.cpp`, `libmav_receiver.cpp`, `cpp/src/mavsdk/plugins/mission/`, `telemetry/`, `offboard/`, `mavlink_direct/`, `c/`, `py/mavsdk/`, `kt/`, `jni/`, `cpp/examples/`, optional `cpp/src/mavsdk_server/`.
- **Install / runtime:** CMake/C++ toolchain or packaged direct bindings; optional gRPC server for legacy clients; MAVLink vehicle or SITL needed for functional testing.
- **Platforms:** Linux, Windows, macOS, Android, iOS; C++, C, Python, Kotlin.
- **License:** BSD-3-Clause root LICENSE.md; proto submodule and third-party dependencies require separate review.
- **Maintenance signals:** [v4.0.6](https://github.com/mavlink/MAVSDK/releases/tag/v4.0.6) 2026-10-08. 2026-10-26 upstream [Linux 40313071240](https://github.com/mavlink/MAVSDK/actions/runs/40313071240) 30 jobs, [Windows 40313071239](https://github.com/mavlink/MAVSDK/actions/runs/40313071239) 14/14, [Kotlin 40313071246](https://github.com/mavlink/MAVSDK/actions/runs/40313071246) 9 passed/1 skipped, [fuzz 40313071314](https://github.com/mavlink/MAVSDK/actions/runs/40313071314) passed; macOS 40313071347 failed on x64 artifact upload (six jobs passed).
- **Verification performed:** Inspected README, LICENSE, SECURITY.md, py/README.md, core/plugins/examples, .gitmodules, release and CI. No independent compilation, protocol connection, simulator, vehicle or security test.
- **Source discovery:** GitHub-first 2026-10-26; YouTube playlist fetches throttled; no transcript-derived claims.
- **Related projects:** `mavlink/MAVSDK-Proto`, `mavlink/MAVSDK-Python`, `mavlink/mavlink`, `ArduPilot/ardupilot`, `PX4/PX4-Autopilot`.
- **Caveats / risks:** Upstream SECURITY.md says MAVLink signing is not implemented; optional `mavsdk_server` gRPC is unauthenticated/unencrypted and binds 0.0.0.0 by default, exposing connected vehicle control to reachable clients. Prefer direct v4 bindings and isolate/firewall legacy server. No code copied.
- **Research notes:** `research/2026-10-26-openwrt-mavsdk.md`. Follow fuzz parser coverage, network trust, SITL compatibility, macOS artifact publishing.

### FreeCAD

- **Repository:** https://github.com/FreeCAD/FreeCAD
- **Author / Org:** FreeCAD
- **Category:** parametric CAD / mechanical design / 3D modeling / Python automation
- **Evidence:** VERIFIED (upstream build and tests; no independent CAD execution)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Cross-platform, history-based parametric 3D modeler using OpenCASCADE, Qt and Python scripting.
- **Why it is valuable:** Open-source mechanical-design workflows with reusable sketch constraints, geometric modeling, technical drawings, and automation APIs.
- **Useful code/components:** `src/Mod/Sketcher/App/Constraint.cpp`, `SketchObject.cpp` (constraint model); `src/Mod/Part/App` (OpenCASCADE B-rep wrappers); `src/Mod/PartDesign` (feature modeling); `src/Mod/OpenSCAD/importCSG.py`, `exportCSG.py` (CSG exchange); `src/Mod/TechDraw` (drawings); `tests/src` and `SketcherTests` (regression).
- **Install / runtime:** Official desktop releases or CMake >=3.22 with OpenCASCADE, Qt, Python, Coin3D and platform build dependencies; documented Python API and workbenches.
- **Platforms:** Linux, Windows, macOS; C++/Python.
- **License:** Root LGPL-2.1 text; inspected `src/App/CMakeLists.txt` declares LGPL-2.1-or-later. Review each reused file, third-party dependency and asset license separately; no code copied.
- **Maintenance signals:** Stable 1.1.4 released 2026-09-28; upstream main FreeCAD CI primary [40346216527](https://github.com/FreeCAD/FreeCAD/actions/runs/40346216527) passed 2026-10-26 with build, CLI/GUI, C++ and install tests; CodeQL [40346215716](https://github.com/FreeCAD/FreeCAD/actions/runs/40346215716) passed.
- **Verification performed:** Inspected README, LICENSE, module SPDX, CMake, workbench and test trees, SECURITY.md, stable release and upstream CI steps. No independent installation, model generation, geometry precision or manufacturing test.
- **Source discovery:** GitHub-first 2026-10-26; YouTube seed pages throttled, no transcript evidence claimed.
- **Related projects:** `openscad/openscad` (in-tree FreeCAD OpenSCAD workbench), OpenCASCADE/OCCT, `FreeCAD/FreeCAD-Bundle`.
- **Caveats / risks:** Geometry and manufactured part tolerances require domain validation; macros/addons and imported CAD files require trust review. Root license does not imply uniform dependency licensing.
- **Research notes:** `research/2026-10-26-freecad-opencpn.md`. Follow OpenSCAD roundtrip fidelity, sketch solver regressions and Python macro sandboxing.

### OpenCPN

- **Repository:** https://github.com/OpenCPN/OpenCPN
- **Author / Org:** OpenCPN
- **Category:** marine navigation / offline charts / AIS / NMEA / geospatial sensors
- **Evidence:** VERIFIED (upstream multi-platform builds and tests; no independent navigation)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Open-source chartplotter and vessel navigation application with raster/vector charts, AIS, NMEA 0183/2000 and Signal K inputs.
- **Why it is valuable:** Mature offline-capable navigation interface and reusable marine telemetry, chart, protocol and plugin components.
- **Useful code/components:** `model/src/ais_decoder.cpp`, `ais_target_data.cpp` (AIS); `comm_drv_n0183_serial.cpp`, `comm_drv_n0183_net.cpp` (NMEA 0183); `comm_drv_n2k_socketcan.cpp` (NMEA 2000); `comm_drv_signalk_net.cpp` (Signal K); `libs/s57-charts` (ENC charts); `plugins/dashboard_pi`, `plugins/grib_pi` (dashboard and weather); `test/n2k_tests.cpp`, `test/rest-tests.cpp` (tests).
- **Install / runtime:** Desktop release packages or CMake/wxWidgets source build; chart datasets and sensor interfaces vary by platform. Android supported upstream but not tested this run.
- **Platforms:** Linux, Windows, macOS, Android.
- **License:** OpenCPN-authored files GPL-2.0-or-later per `LICENSING`; bundled dependencies and assets use multiple licenses, with file-level inventory in `data/copyright`. No code copied.
- **Maintenance signals:** Stable 5.14.2 released 2026-09-28; 2026-10-15 upstream Linux [38800150299](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150299) passed 3 jobs (including ASan and test steps), macOS [38800150392](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150392) 2/2, Windows [38800150288](https://github.com/OpenCPN/OpenCPN/actions/runs/38800150288) 1/1.
- **Verification performed:** Inspected README, LICENSING, SECURITY.md, source modules, plugins, test README and CI jobs. No independent AIS/GPS device, chart, sea-trial or Android testing.
- **Source discovery:** GitHub-first 2026-10-26; YouTube seed pages throttled, no transcript evidence claimed.
- **Related projects:** `SignalK/signalk-server-node`; OpenCPN in-tree plugins and chart parsers.
- **Caveats / risks:** Upstream SECURITY.md states third-party plugins inherit full user privileges; charts and sensor data can be untrusted. AIS/GPS data and chart currency must not be treated as infallible navigation safety evidence.
- **Research notes:** `research/2026-10-26-freecad-opencpn.md`. Follow AIS malformed-input tests, chart parser fuzzing, plugin trust and Signal K transport security.

## Rejected / Deferred Leads

- **PeterJBurke/esp32-c3-remote-id:** deferred because its own README explicitly states it is broken after an ESP development-stack upgrade and may be deleted. Keep as historical lead only; do not promote as working Gold.
- **colonelpanichacks/Remote-ID-Spoofer:** not promoted. Its primary purpose is Remote ID spoofing, outside this catalog's preferred defensive/interoperability scope.


### llama.cpp

- **Repository:** https://github.com/ggml-org/llama.cpp
- **Author / Org:** ggml-org
- **Category:** Local AI / LLM inference / GGUF / quantization / C++ / Android
- **Evidence:** VERIFIED (upstream builds and CI; not independently executed).
- **Tier / Score:** S / 29 (Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 4).
- **What it does:** Local LLM/VLM inference engine, GGUF model loader, quantization utilities and HTTP API server.
- **Why it is valuable:** Portable, low-resource CPU inference, optional GPU acceleration, embeddable C API, model inspection and reusable constrained-decoding components.
- **Useful code/components:** `include/llama.h` C API; `src/llama-model-loader.cpp`; `src/llama-sampler.cpp`; `src/llama-grammar.cpp`; `tools/server/`; `tools/quantize/`, `tools/imatrix/`; `gguf-py/gguf/scripts/gguf_dump.py`; `docs/android.md`; `examples/llama.android`; `tests/test-gguf.cpp`.
- **Install / runtime:** CMake source build or rolling binaries; separate GGUF model weights. Android/Termux and NDK instructions available. RAM/VRAM varies with model/context/quantization.
- **Platforms:** Linux, Windows, macOS, Android/Termux, iOS, WASM and accelerator-specific targets.
- **License:** MIT root; check `gguf-py/LICENSE`, `vendor/`, dependencies and model-weight terms before reuse.
- **Maintenance signals:** Rolling [b11907](https://github.com/ggml-org/llama.cpp/releases/tag/b11907) prerelease 2026-10-26 with 36 assets; [Server CI 40389494969](https://github.com/ggml-org/llama.cpp/actions/runs/40389494969) Windows/Ubuntu passed 2/2; [self-hosted Server 40379656923](https://github.com/ggml-org/llama.cpp/actions/runs/40379656923) CUDA/Metal/KleidiAI passed 3/3; [WASM 40389495039](https://github.com/ggml-org/llama.cpp/actions/runs/40389495039) passed.
- **Verification performed:** Inspected upstream README, LICENSE, SECURITY.md, source, tests, server/Android/GGUF docs and CI 2026-10-26. No independent build, inference, Android run, benchmark or security audit.
- **Source discovery:** GitHub-first; `research/2026-10-26-llamacpp-jq.md`. Two YouTube playlists throttled; no transcript attribution.
- **Related projects:** ggml-org/ggml; ggml-org/whisper.cpp; ggml-org/llama.vscode.
- **Caveats / risks:** Upstream security policy advises isolating untrusted models and not exposing server/RPC to untrusted networks. Model licenses vary; b-tags are rolling prereleases.
- **Research notes:** Follow GGUF parser fuzzing, model-license provenance, API isolation and Android memory profiling. No third-party code copied.

### jq

- **Repository:** https://github.com/jqlang/jq
- **Author / Org:** jqlang
- **Category:** JSON / structured-data CLI / C library / data transformation
- **Evidence:** VERIFIED (upstream release and CI; not independently executed).
- **Tier / Score:** S / 28 (Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4).
- **What it does:** JSON query and transformation CLI with an embeddable C filter language runtime.
- **Why it is valuable:** Reusable parser, typed-value model, filter compiler/VM, shell integration and regression/fuzzing components.
- **Useful code/components:** `src/jv_parse.c` parser; `src/jv.c` values; `src/compile.c` compiler; `src/execute.c` VM; `src/lexer.l`, `src/parser.y`; `src/builtin.c`, `src/builtin.jq`; `tests/jq.test`, `tests/jq_fuzz_parse.c`; `src/jq.h` C API.
- **Install / runtime:** Standalone release binaries, Docker or autotools build; optional Oniguruma; `make check` documented.
- **Platforms:** Linux, Windows, macOS, FreeBSD, NetBSD, ARM, RISC-V and other cross-built targets.
- **License:** MIT jq core; `COPYING` lists CC BY 3.0 documentation, ICU decNumber, Lucent dtoa, Heimdal/NetBSD notices; check Oniguruma separately.
- **Maintenance signals:** Stable [jq-1.8.2](https://github.com/jqlang/jq/releases/tag/jq-1.8.2) published 2026-06-20 with security fixes; [CI 40382053397](https://github.com/jqlang/jq/actions/runs/40382053397) 24 jobs passed, release job skipped; [Valgrind 40382053249](https://github.com/jqlang/jq/actions/runs/40382053249) and [BSD 40382053191](https://github.com/jqlang/jq/actions/runs/40382053191) passed. Source commits 2026-10-25.
- **Verification performed:** README, COPYING, SECURITY.md, source, tests, parser fuzz harness, release and CI inspected 2026-10-26. No independent execution or fuzz campaign.
- **Source discovery:** GitHub-first; `research/2026-10-26-llamacpp-jq.md`. Two YouTube playlists throttled; no transcript attribution.
- **Related projects:** nushell/nushell (complementary structured-data shell, not direct integration).
- **Caveats / risks:** jq-1.8.2 addresses multiple parser/memory-safety, path-depth and DoS CVEs. Patch deployments processing untrusted JSON. Bundled components have additional licenses.
- **Research notes:** Follow parser fuzzing, deep-input limits, regex engine configuration and embedded libjq use. No code copied.


### Joplin

- **Repository:** https://github.com/laurent22/joplin
- **Author / Org:** Laurent Cozic / Joplin SAS
- **Category:** Offline-first Markdown notes / encrypted sync / productivity / CLI
- **Evidence:** VERIFIED (upstream CI; no independent runtime execution)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Offline-first Markdown notes and tasks with cross-platform sync, E2EE, search, import/export and plugins.
- **Why it is valuable:** Reusable sync/conflict handling, encrypted content, indexing, import/export, mobile and CLI components.
- **Useful code/components:** `packages/lib/services/synchronizer/` (including E2EE/conflict tests), `packages/lib/services/e2ee/EncryptionService.ts`, `packages/lib/services/interop/`, `packages/lib/services/search/SearchEngine.ts`, `packages/app-cli/`, `packages/app-mobile/`.
- **Install / runtime:** Official desktop/mobile packages; development uses Node/Yarn monorepo and native mobile toolchains.
- **Platforms:** Linux, Windows, macOS, Android, iOS, CLI.
- **License:** Root AGPL-3.0-or-later **except overrides**; `packages/server/LICENSE.md` is separate Joplin Server Personal Use License; branding assets reserved.
- **Maintenance signals:** Stable [v3.7.21](https://github.com/laurent22/joplin/releases/tag/v3.7.21) 2026-09-25. [CI 40406257789](https://github.com/laurent22/joplin/actions/runs/40406257789) passed 7/7 jobs 2026-10-26; [UI tests 40423856061](https://github.com/laurent22/joplin/actions/runs/40423856061) passed 3/3 and [Android build 40423856058](https://github.com/laurent22/joplin/actions/runs/40423856058) passed 2026-10-27 UTC. Later [CI 40423856055](https://github.com/laurent22/joplin/actions/runs/40423856055) failed macOS Intel `packages/utils/ipc.test.ts:67` (expected pong, received no response), with 4 other jobs passed and 2 cancelled.
- **Verification performed:** README, root/server licenses, source and tests, release and upstream job logs inspected. No independent sync, E2EE, Android runtime or security audit.
- **Source discovery:** GitHub-first 2026-10-26; no YouTube transcript attribution.
- **Related projects:** Syncthing and restic (conceptual/complementary, not proven integrations).
- **Caveats / risks:** Server license differs from root; branding restricted; plugin trust and MCP/API exposure require review; intermittent macOS IPC test failure.
- **Research notes:** `research/2026-10-26-joplin-kicad-maintenance.md`. No third-party code copied.

### KiCad Source Mirror

- **Repository:** https://github.com/KiCad/kicad-source-mirror
- **Author / Org:** KiCad Development Team; canonical upstream https://gitlab.com/kicad/code/kicad
- **Category:** Electronics EDA / schematic capture / PCB layout / Gerber / hardware design
- **Evidence:** PROMISING (official release, source and test infrastructure; passing application CI not inspected)
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 3)
- **What it does:** Cross-platform schematic and PCB design with connectivity/ERC, DRC, Gerber viewing and automation APIs.
- **Why it is valuable:** Reusable EDA connectivity, layout, geometry, file-format and test infrastructure.
- **Useful code/components:** `eeschema/connection_graph.cpp`, `eeschema/erc/`, `pcbnew/board.cpp`, `pcbnew/board_loader.cpp`, `pcbnew/autorouter/` (placement, not complete general autorouter), `api/proto/board/`, `api/proto/schematic/`, `qa/tests/pcbnew/`, `gerbview/`.
- **Install / runtime:** Official packages; source build uses CMake/C++/wxWidgets and native dependencies.
- **Platforms:** Linux, Windows, macOS.
- **License:** Majority GPL-3.0-or-later per `LICENSE.README`; third-party portions MIT/BSD/Apache/Boost/ISC; file-by-file review required.
- **Maintenance signals:** Official [10.0.7 release announcement](https://www.kicad.org/blog/2026/10/KiCad-10.0.7-Release/) 2026-10-07; GitHub artifacts 2026-10-16; 10.0.8 RC1 announced 2026-10-22. `.gitlab-ci.yml` defines build/test pipelines but passing GitLab run not checked; mirror GitHub Actions are not application CI.
- **Verification performed:** README, licensing, source/API/QA trees, build configuration and official release inspected. No independent build, DRC, Gerber export or fabrication.
- **Source discovery:** GitHub-first and official KiCad release notes; no YouTube attribution.
- **Related projects:** LibrePCB (alternative), FreeCAD (complementary; no tested interoperability).
- **Caveats / risks:** GitHub is a mirror, upstream contributions on GitLab. Untrusted design/archive files, plugin behavior and engineering output require review.
- **Research notes:** `research/2026-10-26-joplin-kicad-maintenance.md`. No code copied.


### Paperless-ngx

- **Repository:** https://github.com/paperless-ngx/paperless-ngx
- **Author / Org:** paperless-ngx
- **Category:** Self-hosted document management / OCR / search / archiving / Django
- **Evidence:** VERIFIED (upstream release, source and CI; no independent deployment)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 5)
- **What it does:** Imports, OCR-processes, classifies and indexes documents into a searchable self-hosted archive.
- **Why it is valuable:** Practical ingestion, OCR, classification, document permissions, workflows and export architecture with real multi-platform container builds.
- **Useful code/components:** `src/documents/consumer.py` (ingestion); `src/paperless/parsers/tesseract.py` (OCRmyPDF/Tesseract); `src/documents/classifier.py`; `src/documents/search/`; `src/documents/permissions.py`; `src/documents/tests/test_permission_filtering_security.py`; `src/documents/export/`; `docker/compose/`.
- **Install / runtime:** Docker Compose recommended; Python >=3.11 for source builds, Django/Celery, database/Redis and OCR/PDF dependencies. Browser client.
- **Platforms:** Linux self-hosting; amd64/arm64 container builds; modern web browsers.
- **License:** GPL-3.0 root; separate OCRmyPDF/Tesseract/Ghostscript and other dependency notices. No source copied.
- **Maintenance signals:** Stable [v3.3.4](https://github.com/paperless-ngx/paperless-ngx/releases/tag/v3.3.4) (2026-10-22) addresses certifi/Pillow/aiohttp-related dependency security issues. 2026-10-27 UTC upstream [Backend Tests 40424424887](https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424424887) passed Python 3.11–3.14; [CodeQL 40424425034](https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424425034) passed JS/Python; [Docker Build 40424424910](https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424424910) passed amd64/arm64/manifest. These passing runs were on `fix/14557`, not a confirmed current `dev` head.
- **Verification performed:** Inspected README, root license, Python manifest, ingestion/OCR/permission source, regression test source, release and upstream job conclusions. Frontend workflow succeeded but its frontend test/build jobs were skipped due to no frontend changes. No independent OCR, install, backup/restore or security tests.
- **Source discovery:** GitHub-first 2026-10-26 CDT; no YouTube transcript attribution.
- **Related projects:** Tesseract OCR and OCRmyPDF (OCR dependencies); paperless-ngx/builder.
- **Caveats / risks:** Upstream warns document contents are stored in clear text at rest; do not host on untrusted infrastructure. Secure access, backups, untrusted document parsing and third-party licenses need review.
- **Research notes:** `research/2026-10-26-paperless-briar.md`. No third-party code copied.

### Briar Android

- **Repository:** https://github.com/briar/briar
- **Author / Org:** Briar Project; canonical https://code.briarproject.org/briar/briar (GitHub mirror)
- **Category:** Offline messaging / Android / Bluetooth / Wi-Fi / Tor / emergency communications
- **Evidence:** PROMISING (official release and source/test structure; passing CI and runtime not independently confirmed)
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 5 + Documentation 4 + Maintenance 3)
- **What it does:** Peer-to-peer encrypted messaging and synchronization over nearby Bluetooth/Wi-Fi, or Tor when internet is available.
- **Why it is valuable:** Modular offline-first message synchronization, cryptographic transport, Android radio adapters, mailbox and headless integration.
- **Useful code/components:** `bramble-core/src/main/java/org/briarproject/bramble/crypto/`, `bramble-core/src/main/java/org/briarproject/bramble/sync/`, `bramble-android/src/main/java/org/briarproject/bramble/plugin/bluetooth/`, `bramble-android/src/main/java/org/briarproject/bramble/plugin/tcp/`, `bramble-core/src/main/java/org/briarproject/bramble/plugin/file/`, `bramble-core/src/test/java/org/briarproject/bramble/sync/SyncIntegrationTest.java`, `bramble-core/src/test/java/org/briarproject/bramble/mailbox/`, `briar-headless/`.
- **Install / runtime:** Official Android app/APK; source uses Gradle, Java 17, Android SDK 35; minSdk 21 (Android 5.0). Bluetooth/Wi-Fi or Tor networking as available.
- **Platforms:** Android 5.0+; Java/Gradle headless components.
- **License:** GPL-3.0-or-later in inspected `LICENSE.txt`; submodules and third-party Tor/crypto dependencies require separate license review. No source copied.
- **Maintenance signals:** Official [Briar 1.5.22](https://www.briarproject.org/) dated 2026-10-13; October 9 GitHub mirror commit updated version and Tor 0.4.9.14. `.gitlab-ci.yml` specifies Gradle, emulator and reproducibility jobs, but no passing canonical GitLab pipeline was inspected. GitHub mirror has no release objects.
- **Verification performed:** Inspected README, license, Gradle Android build configuration, cryptographic/transport/sync source paths and test suite; official release page. No independent APK build, Bluetooth/Wi-Fi/Tor message delivery, reproducible build or security audit.
- **Source discovery:** GitHub-first 2026-10-26 CDT, checked against official Briar site; no YouTube transcript attribution.
- **Related projects:** briar/briar-mailbox, briar/briar-desktop, briar/onionwrapper; Reticulum is a conceptual off-grid alternative, not a proven integration.
- **Caveats / risks:** GitHub is a mirror; verify canonical GitLab CI and release signatures. Bluetooth/Wi-Fi needs nearby peers; Tor needs internet. Do not infer independently audited encryption from source names.
- **Research notes:** `research/2026-10-26-paperless-briar.md`. No third-party code copied.


### OCRmyPDF

- **Repository:** https://github.com/ocrmypdf/OCRmyPDF
- **Author / Org:** James R. Barlow and OCRmyPDF contributors
- **Category:** Offline OCR / PDF/A / document processing / Python CLI and API
- **Evidence:** VERIFIED (upstream source, tests and CI; no independent execution)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 5)
- **What it does:** Adds searchable text layers to scanned PDFs/images with rotation, deskew, PDF/A output and plugin-based processing.
- **Why it is valuable:** Reusable OCR pipeline, PDF/A validation, hOCR parsing, Python API, extension hooks, resource controls and watcher security components.
- **Useful code/components:** `src/ocrmypdf/api.py`, `src/ocrmypdf/_pipelines/ocr.py`, `src/ocrmypdf/pdfa.py`, `src/ocrmypdf/hocrtransform/hocr_parser.py`, `src/ocrmypdf/_exec/tesseract.py`, `src/ocrmypdf/pluginspec.py`, `src/ocrmypdf/_watcher_security.py`, `tests/test_pdfa_final_validation.py`, `tests/test_decompression_bomb.py`.
- **Install / runtime:** Python >=3.11 plus Tesseract and PDF/image native dependencies; CLI or Python API; optional watcher/HEIC extras.
- **Platforms:** Linux, Windows, macOS.
- **License:** MPL-2.0 application; README CC-BY-SA-4.0; separate dependency/font and optional HEIC/x265 licenses. Review each file before reuse.
- **Maintenance signals:** Stable [v17.13.0](https://github.com/ocrmypdf/OCRmyPDF/releases/tag/v17.13.0) 2026-09-28; main manifest 17.13.1 is not a confirmed release. 2026-10-26 [CI 40295734365](https://github.com/ocrmypdf/OCRmyPDF/actions/runs/40295734365) succeeded overall: 21 jobs passed, four experimental Python 3.15 dependency installs failed, one skipped. Python 3.11–3.14, lint and build jobs passed.
- **Verification performed:** Inspected README, license, manifest, OCR/PDF/A/API/watcher/plugin code, tests and workflow job steps. Python 3.15 install failure traced to onnxruntime 1.31.0 lacking cp315 wheel/sdist; 3.15 marked continue-on-error. No independent OCR or PDF/A validation.
- **Source discovery:** GitHub-first 2026-10-27; no YouTube transcript evidence.
- **Related projects:** Tesseract OCR, Paperless-ngx, pikepdf.
- **Caveats / risks:** Plugin and Pillow image limits are interpreter-global; different concurrent configs need separate processes. Watcher acknowledges TOCTOU/hardlink residual risks. Untrusted PDFs require isolation.
- **Research notes:** `research/2026-10-27-ocrmypdf-gokrazy.md`. No third-party code copied.

### gokrazy

- **Repository:** https://github.com/gokrazy/gokrazy
- **Author / Org:** gokrazy contributors
- **Category:** Minimal Go appliance OS / embedded Linux / Raspberry Pi / edge services
- **Evidence:** VERIFIED (upstream QEMU boot tests, Go tests and image generation; no physical hardware)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 5 + Documentation 4 + Maintenance 3)
- **What it does:** Runs Go programs as minimal Linux appliances with process supervision, a status interface and update support.
- **Why it is valuable:** Distinctive edge runtime with CI-tested MBR/UEFI boot, modular Go services, authenticated control-plane code and companion image builder.
- **Useful code/components:** `supervise.go`, `update.go`, `authenticated.go`, `cmd/dhcp/dhcp.go`, `cmd/ntp/ntp.go`, `netlink.go`, `integration/mbrboot/mbrboot_test.go`, `integration/uefiboot/uefiboot_test.go`.
- **Install / runtime:** Go 1.26 for inspected main source; `gokrazy/tools` supplies `gok` image builder; supported Raspberry Pi or x86_64 PC.
- **Platforms:** Raspberry Pi supported boards, x86_64 PC (MBR/UEFI); companion CLI builds Linux/macOS/Windows.
- **License:** BSD-3-Clause core and companion tools; kernel, firmware, EEPROM and dependencies separately licensed.
- **Maintenance signals:** Core [CI 35105853192](https://github.com/gokrazy/gokrazy/actions/runs/35105853192) passed 2026-09-16 including `go test ./...`, QEMU MBR/UEFI boot and image creation; [feature CI 37527198802](https://github.com/gokrazy/gokrazy/actions/runs/37527198802) passed 2026-10-06. Companion [tools CI 40385840520](https://github.com/gokrazy/tools/actions/runs/40385840520) passed Windows/macOS/Ubuntu 2026-10-26. No GitHub Releases in core.
- **Verification performed:** Inspected README, license, Go manifest, supervision/auth/update source, tests, CI YAML and job log; QEMU `TestMBRBoot` and `TestUEFIBoot` explicitly passed. No physical device boot, remote update or security audit.
- **Source discovery:** GitHub-first 2026-10-27; no transcript attribution.
- **Related projects:** `gokrazy/tools`, `gokrazy/internal`, `gokrazy/kernel`, `gokrazy/firmware`.
- **Caveats / risks:** No stable core release tag; firmware/kernel provenance and licenses separate. Review HTTPS/Basic auth, management exposure and update/rollback before deployment.
- **Research notes:** `research/2026-10-27-ocrmypdf-gokrazy.md`. No third-party code copied.

### yt-dlp

- **Repository:** https://github.com/yt-dlp/yt-dlp
- **Author / Org:** yt-dlp maintainers
- **Category:** media-archiving / python-cli / metadata-extraction / subtitles / offline-preservation
- **Evidence:** VERIFIED (upstream evidence; no independent execution)
- **Tier / Score:** S / 29 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5)
- **What it does:** Extensible Python media/metadata/subtitle downloader with format selection, HTTP resume and postprocessing.
- **Why it is valuable:** Reusable extractor, network, plugin and postprocessor architecture; useful for permitted archival workflows.
- **Useful code/components:** `yt_dlp/extractor/common.py`; `yt_dlp/downloader/http.py`; `yt_dlp/networking/`; `yt_dlp/plugins.py`; `yt_dlp/YoutubeDL.py`; `yt_dlp/postprocessor/`; `test/`.
- **Install / runtime:** Python >=3.11, optional FFmpeg and JS runtime depending on site/format.
- **Platforms:** Linux, Windows, macOS, Python >=3.11, Android/Termux with compatible tools.
- **License:** Unlicense root; optional dependencies and media have independent rights. No source copied.
- **Maintenance signals:** Stable [2026.10.26](https://github.com/yt-dlp/yt-dlp/releases/tag/2026.10.26) published 2026-10-26. [Core Tests](https://github.com/yt-dlp/yt-dlp/actions/runs/40404432725) 13/13 passed across Linux/Windows/Python 3.11–3.15/PyPy; [Quick Test](https://github.com/yt-dlp/yt-dlp/actions/runs/40404432887) 2/2 passed; [CodeQL](https://github.com/yt-dlp/yt-dlp/actions/runs/40404432831) passed. Later Core Tests run 40409938717 was skipped.
- **Verification performed:** README, license, manifest, source, release and upstream CI inspected; no local download, subtitle extraction or security test.
- **Source discovery:** GitHub-first 2026-10-27; playlist pages throttled, no transcript attribution.
- **Related projects:** ArchiveBox (optional external downloader), abx-dl, FFmpeg.
- **Caveats / risks:** Unlicense root does not cover FFmpeg, optional packages or downloaded content. Handle cookies and plugins as sensitive/untrusted. Respect rights and site terms.
- **Research notes:** `research/2026-10-27-ytdlp-immich.md`.

### Immich

- **Repository:** https://github.com/immich-app/immich
- **Author / Org:** immich-app
- **Category:** self-hosting / photo-video-archiving / mobile-backup / local-machine-learning / media-management
- **Evidence:** PROMISING (upstream evidence; no independent execution)
- **Tier / Score:** A / 25 (Utility 5 + Working Evidence 3 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 4)
- **What it does:** Self-hosted photo/video library with mobile backup, search, deduplication, ML and sharing.
- **Why it is valuable:** Reusable media lifecycle, authorization, duplicate resolution, database backups and typed local inference pipeline.
- **Useful code/components:** `server/src/services/asset.service.ts`; `duplicate.service.ts`; `database-backup.service.ts`; `search.service.ts`; `machine-learning/immich_ml/pipeline.py`; server `*.spec.ts` tests.
- **Install / runtime:** Docker server with PostgreSQL and Redis; optional ML service, Android/iOS apps and browser.
- **Platforms:** Linux/Docker server, web browsers, Android, iOS, PostgreSQL/Redis, Python ML service.
- **License:** AGPL-3.0 root; ML models, assets and dependencies separately licensed. No source copied.
- **Maintenance signals:** Stable [v3.3.5](https://github.com/immich-app/immich/releases/tag/v3.3.5) published 2026-10-21. 2026-10-27 [CodeQL](https://github.com/immich-app/immich/actions/runs/40492780574) and [static analysis](https://github.com/immich-app/immich/actions/runs/40492780708) passed; [Test](https://github.com/immich-app/immich/actions/runs/40492780438) failed overall. Server test/lint passed; SQL/e2e GHCR image pulls throttled (`toomanyrequests`), medium tests lacked PostgreSQL image. Mobile build-and-sign jobs were skipped.
- **Verification performed:** README, license, package manifest, source and upstream CI logs inspected; no local deployment, mobile upload, backup restore, ML inference or e2e test.
- **Source discovery:** GitHub-first 2026-10-27; playlist pages throttled, no transcript attribution.
- **Related projects:** immich-app/devtools, PostgreSQL, FFmpeg; no claimed direct integration.
- **Caveats / risks:** AGPL-3.0 network copyleft; third-party/model rights. Official 3-2-1 backup warning; database-only backup does not preserve media. Face/location privacy and public sharing need scrutiny.
- **Research notes:** `research/2026-10-27-ytdlp-immich.md`.

### libarchive

- **Repository:** https://github.com/libarchive/libarchive
- **Author / Org:** libarchive
- **Category:** archival / c-library / compression / format-parsing / cli-tools
- **Evidence:** VERIFIED (upstream CI and source inspection; no independent execution)
- **Tier / Score:** S / 28 (Utility 5 + Working Evidence 5 + Reusability 5 + Novelty 3 + Documentation 5 + Maintenance 5)
- **What it does:** Portable C archive reader/writer and implementations of bsdtar, bsdcpio, bsdcat and bsdunzip.
- **Why it is valuable:** Embeddable archive parsing, streaming compression, metadata handling and multi-format interoperability.
- **Useful code/components:** `libarchive/archive_read_support_format_zip.c — ZIP reader`; `libarchive/archive_read_support_format_7zip.c — 7z reader`; `libarchive/archive_read_support_format_tar.c — tar reader`; `libarchive/archive_read_support_filter_zstd.c — Zstandard filter`; `libarchive/archive_entry.c — entry metadata`; `examples/minitar/minitar.c — embedding example`; `tar/ — bsdtar`; `unzip/ — bsdunzip`; `libarchive/test/ — regression fixtures`.
- **Install / runtime:** CMake or Autotools C build; compression and crypto dependencies vary by configuration.
- **Platforms:** Linux, Windows, macOS, FreeBSD, Alpine Linux.
- **License:** Permissive two-clause BSD-style notice for most source; UC Regents, public-domain, BLAKE2 and build-script exceptions. No third-party source copied.
- **Maintenance signals:** [v3.8.10](https://github.com/libarchive/libarchive/releases/tag/v3.8.10) released 2026-10-14; [CI](https://github.com/libarchive/libarchive/actions/runs/40530777935) 20/20 passed 2026-10-27; [CodeQL](https://github.com/libarchive/libarchive/actions/runs/40530777979) passed.
- **Verification performed:** 2026-10-27 inspected README, COPYING, SECURITY.md, source, examples, test tree and CI workflow; Stable v3.8.10 released 2026-10-14; 2026-10-27 master CI 40530777935 passed 20/20 jobs with build/test stages on Ubuntu, Alpine, Windows, FreeBSD and macOS; 2026-10-27 master CodeQL 40530777979 passed; PR CIFuzz workflow exists; No independent compilation, extraction, fuzzing or security audit.
- **Source discovery:** GitHub-first 2026-10-27; no YouTube transcript attribution.
- **Related projects:** bsdtar, bsdcpio, bsdcat, bsdunzip (same repository).
- **Caveats / risks:** Individual source-file license headers govern reuse. Malformed archives, traversal, symlinks and decompression bombs require deployment safeguards; no code copied.
- **Research notes:** `research/2026-10-27-libarchive-kiwix-tools.md`.

### Kiwix Tools

- **Repository:** https://github.com/kiwix/kiwix-tools
- **Author / Org:** kiwix
- **Category:** offline-knowledge / zim-format / http-server / search / cli-tools
- **Evidence:** VERIFIED (upstream CI and source inspection; no independent execution)
- **Tier / Score:** S / 27 (Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 4)
- **What it does:** Provides offline ZIM HTTP serving (kiwix-serve), full-text search (kiwix-search) and library management (kiwix-manage).
- **Why it is valuable:** Completes the existing offline ZIM ecosystem with practical search and local multi-device HTTP access.
- **Useful code/components:** `src/server/kiwix-serve.cpp — offline ZIM HTTP serving, bind controls`; `src/searcher/kiwix-search.cpp — full-text search and suggestions`; `src/manager/kiwix-manage.cpp — ZIM library XML/OPDS catalog`; `meson.build — dependency constraints and C++17 build`; `docker/ — container packaging`.
- **Install / runtime:** Meson/Ninja C++17; libzim >=9,<10, libkiwix >=14.2,<15, docopt; official Docker image.
- **Platforms:** Linux x86_64 dynamic/static, Windows x64, POSIX, Docker.
- **License:** GPL-3.0-or-later per source headers; root COPYING GPLv3; dependencies separate. No third-party source copied.
- **Maintenance signals:** [3.8.2](https://github.com/kiwix/kiwix-tools/releases/tag/3.8.2) released 2026-03-02; [CI](https://github.com/kiwix/kiwix-tools/actions/runs/36844685289) 3/3 passed 2026-10-01 (Linux builds, Windows build/tests).
- **Verification performed:** 2026-10-27 inspected README, COPYING, C++ server/searcher/manager source, Meson manifest and CI workflow; Stable 3.8.2 released 2026-03-02; 2026-10-01 main CI 36844685289 passed 3/3 jobs: Linux dynamic/static compile and Windows compile plus Meson tests; 2026-10-26 scheduled 40272845437 passed only Actions analysis, not a runtime test; No independent HTTP serving, ZIM search, LAN security or Docker deployment.
- **Source discovery:** GitHub-first 2026-10-27; no YouTube transcript attribution.
- **Related projects:** kiwix/libkiwix (direct dependency); openzim/libzim (direct dependency); openzim/zim-tools (complementary); kiwix/kiwix-android (separate client); kiwix/kiwix-build (build support).
- **Caveats / risks:** Meson/Ninja C++17, libzim >=9,<10, libkiwix >=14.2,<15, docopt. kiwix-serve defaults to all network interfaces on HTTP port 80; restrict exposure. No source copied.
- **Research notes:** `research/2026-10-27-libarchive-kiwix-tools.md`.

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