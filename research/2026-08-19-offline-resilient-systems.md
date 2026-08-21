# Research Pass — Offline & Resilient Systems — 2026-08-19

This dossier records promotion-ready candidates discovered during a breadth pass covering heterogeneous off-grid networking, offline navigation, and resilient encrypted storage. These entries are intentionally staged outside `MASTER_LIST.md` and `catalog/tools.json` until a clean synchronized promotion edit can be made.

## Organic Maps

- **Repository:** https://github.com/organicmaps/organicmaps
- **Author / Org:** Organic Maps
- **Category:** offline maps / navigation / OpenStreetMap / privacy / mobile
- **Evidence:** VERIFIED
- **Provisional Tier / Score:** S / 29
- **What it does:** Privacy-first offline mapping and GPS navigation for walking, hiking, cycling, driving, and public transport using OpenStreetMap data.
- **Why it is valuable:** Mature production-grade offline navigation with downloadable map regions, offline search, routing, elevation/contour data, bookmarks/tracks, and Android/iOS applications. It is a strong architecture reference for disconnected/mobile geospatial systems.
- **Useful code/components:** offline map storage and rendering; routing engine; geocoding/search; OpenStreetMap ingestion; map update pipeline; Android/iOS platform layers; KML/KMZ/GPX/GeoJSON import/export; elevation/contour support; offline Wikipedia integration.
- **Install / runtime:** Distributed through major mobile app stores, F-Droid/Accrescent/Obtainium paths, and source builds documented upstream.
- **Platforms:** Android, iOS, desktop development/build tooling.
- **License:** Code is Apache-2.0. Binary map/data files have a separate data license. Upstream also documents attribution expectations for derivative apps and forks.
- **Maintenance signals:** Multiple commits observed on 2026-08-19, including Android/iOS upload-state correctness fixes, background task handling, and repository maintenance.
- **Verification performed:** README and same-day commit history inspected. Upstream licensing declaration and separate data-license boundary inspected. GitHub Gold did not build the application or perform a navigation test.
- **Source discovery:** Independent offline/navigation breadth pass.
- **Related projects:** OpenStreetMap; Organic Maps map-generation tooling; Kothic-related components; community builds and integrations.
- **Caveats / risks:** Do not treat map data as Apache-2.0 merely because the application code is Apache-2.0. Review `DATA_LICENSE.txt`, `NOTICE`, and REUSE metadata before redistributing data or derivative applications.
- **Research notes:** High-value candidate for deeper component mapping around compact offline-map formats, routing, region updates, and disconnected search.

## Kopia

- **Repository:** https://github.com/kopia/kopia
- **Author / Org:** Kopia
- **Category:** backup / encrypted snapshots / deduplication / storage abstraction / self-hosting
- **Evidence:** VERIFIED
- **Provisional Tier / Score:** S / 28
- **What it does:** Creates encrypted, compressed, deduplicated filesystem snapshots and stores them locally, on network storage, through cloud/object backends, or through a dedicated Kopia repository server.
- **Why it is valuable:** Combines CLI and GUI workflows with user-controlled end-to-end encryption, deduplication, compression, error correction, multiple storage transports, multi-machine repositories, and server mode.
- **Useful code/components:** encrypted snapshot repository; content deduplication; compression; error-correction support; repository server; S3/Azure/B2/GCS/WebDAV/SFTP/local backends; rclone integration; CLI; Electron/GUI client; build/CI machinery.
- **Install / runtime:** Native packages/binaries and documented source builds; server and container deployment paths are available upstream.
- **Platforms:** Linux, Windows, macOS and other supported Go/Electron environments.
- **License:** Apache-2.0.
- **Maintenance signals:** Active dependency/security-toolchain maintenance observed on 2026-08-18, including CodeQL, crypto/network dependencies, Electron, and Playwright updates. README exposes build, coverage, release, and Go quality signals.
- **Verification performed:** README, Apache-2.0 root license, repository metadata, and recent commits inspected. GitHub Gold did not execute backup/restore or repository-integrity tests.
- **Source discovery:** Independent resilient-storage breadth pass.
- **Related projects:** rclone; S3-compatible object stores; Kopia repository server ecosystem.
- **Caveats / risks:** Backup systems should be judged by tested restore procedures, not only successful snapshot creation. Backend credentials and repository passwords require operational protection.
- **Research notes:** Complements restic rather than replacing it in the catalog: stronger integrated GUI/server story and explicit error-correction support make its architecture separately useful.

## Reticulum Network Stack

- **Repository:** https://github.com/markqvist/Reticulum
- **Author / Org:** Mark Qvist
- **Category:** off-grid networking / delay-tolerant networking / cryptographic routing / heterogeneous transports
- **Evidence:** VERIFIED
- **Provisional Tier / Score:** A / 25
- **What it does:** Userland cryptography-based network stack designed to build local and wide-area networks across heterogeneous carriers including LoRa/RNode, packet-radio TNCs, serial links, TCP, UDP, Ethernet/Wi-Fi, pipes, and custom interfaces.
- **Why it is valuable:** Unusually broad transport abstraction aimed at very-low-bandwidth and high-latency links, with self-configuring multi-hop routing, cryptographic identities, links, request/response, channels, file transfer, and included operational utilities.
- **Useful code/components:** interface abstraction; path discovery/routing; cryptographic identities; link establishment; low-bandwidth transport; request/response API; channels/buffers; `rnsd`; `rnstatus`; `rnpath`; `rnprobe`; `rncp`; `rnid`; `rnsh`; `rnx`; `rngit`; `git-remote-rns`.
- **Install / runtime:** Python 3; upstream documents `pip install rns` and `pipx install rns`. A dependency-minimal `rnspure` package is also documented.
- **Platforms:** Systems capable of running Python 3, with optional serial/radio/IP hardware interfaces.
- **License:** Custom **Reticulum License** for the reference implementation. It allows use/modification/distribution but adds restrictions including no use in systems designed to purposefully harm human beings and no use in AI/ML/language-model training datasets. The README separately states that the Reticulum Protocol was dedicated to the public domain in 2016.
- **Maintenance signals:** Release-preparation and cleanup commits observed 2026-07-25/26. Upstream README exposes build workflow and extensive manuals.
- **Verification performed:** README, custom LICENSE, installation guidance, supported-interface list, included utility list, and recent commit history inspected. GitHub Gold did not establish a Reticulum link or test radio hardware.
- **Source discovery:** Independent off-grid-networking breadth pass.
- **Related projects:** markqvist/lxmf; markqvist/NomadNet; markqvist/Sideband; markqvist/lxst; RNode; community Reticulum implementations.
- **Caveats / risks:** The custom license is not equivalent to MIT/Apache/BSD and contains field-of-use/training restrictions. Do not copy reference-implementation code into other projects without explicit compatibility review. Also note the GitHub repository states it is a public mirror and development occurs elsewhere.
- **Research notes:** The protocol/architecture is extremely valuable to study, but code reuse must be handled more cautiously than the catalog's permissively licensed networking projects.

## Promotion recommendation

All three are strong enough to preserve. Organic Maps and Kopia are ready for promotion into the canonical catalog after a synchronized human/machine edit. Reticulum is technically strong but should retain an explicit custom-license warning and a lower reusability score than its engineering quality alone would imply.
