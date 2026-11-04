# GitHub Gold — rclone, OpenDroneID Core C, ZIM Tools (2026-10-21)

Three **existing** canonical projects received six-factor scoring and refreshed primary-source evidence. Upstream CI is not independent testing. No source code copied.

## rclone — VERIFIED (upstream), S / 27
- Repository: https://github.com/rclone/rclone
- Gold factors (Utility, Working Evidence, Reusability, Novelty, Documentation, Maintenance): 5 / 5 / 5 / 4 / 4 / 4.
- Latest tagged release: v1.75.2 (2026-10-09).
- CI: master build 39406871189 succeeded 9/9 jobs (2026-10-20).
- Implementation: 2026-10-20 master fixes corrected S3 Last-Modified caching and rejected overflowing duration arguments.
- Valuable components: large storage-backend abstraction layer; copy sync bisync check operations; Crypt backend; Chunker backend; Union and Combine virtual filesystems; FUSE mount; HTTP WebDAV FTP SFTP DLNA serving; hash verification; remote-control API and GUI.
- Platforms: Linux, Windows, macOS, BSD, other Go-supported systems.
- License: MIT. Review security advisories and patched versions before exposing serving protocols; no transfer or mount test performed.

## OpenDroneID Core C — VERIFIED (upstream), S / 28
- Repository: https://github.com/opendroneid/opendroneid-core-c
- Gold factors (Utility, Working Evidence, Reusability, Novelty, Documentation, Maintenance): 5 / 5 / 5 / 5 / 4 / 4.
- Latest tagged release: v2.0 (2022-04-06).
- CI: master CMake 37671876169 succeeded 1/1 job (2026-10-07).
- Implementation: 2026-10-07 master merged a MAVLink Basic ID cycling index fix with regression test; newer than the latest tagged release.
- Valuable components: OpenDroneID message encoders and decoders; libopendroneid API; MAVLink conversion layer; Wi-Fi beacon and NaN reference code; unit tests; low-memory compile options.
- Platforms: portable-C, Linux, embedded-downstream-integrations.
- License: Apache-2.0. Do not assume master fixes are in v2.0; no independent packet, hardware or regulatory-conformance test.

## ZIM Tools — VERIFIED (upstream), S / 28
- Repository: https://github.com/openzim/zim-tools
- Gold factors (Utility, Working Evidence, Reusability, Novelty, Documentation, Maintenance): 5 / 5 / 5 / 4 / 5 / 4.
- Latest tagged release: 3.8.0 (2026-08-13).
- CI: main CI 39216346633 succeeded 5/5 cross-platform jobs (2026-10-19).
- Implementation: Version 3.8.0 improved zimcheck link/metadata validation, zimsplit sizing and zimwriterfs URL parsing.
- Valuable components: zimcheck archive validation; zimdump inspection and extraction; zimsplit archive chunking; zimwriterfs HTML-directory to ZIM packaging; Meson build; automated tests; official container image.
- Platforms: Linux, containerized deployments, other Meson-supported Unix-like systems.
- License: GPL-3.0-or-later. GPL-3.0-or-later and third-party dependencies need license review; no independent archive build/validation.

## Primary-source references
- rclone: https://github.com/rclone/rclone/releases/tag/v1.75.2 ; https://github.com/rclone/rclone/actions/runs/39406871189 ; https://github.com/rclone/rclone/commit/81e7372f6fbedfa80592e9a564593d63a8dc32f3 ; https://github.com/rclone/rclone/commit/40139a749e9822effa686fa196eab1cf531829b3 ; https://github.com/rclone/rclone/blob/master/COPYING
- OpenDroneID: https://github.com/opendroneid/opendroneid-core-c/releases/tag/v2.0 ; https://github.com/opendroneid/opendroneid-core-c/actions/runs/37671876169 ; https://github.com/opendroneid/opendroneid-core-c/commit/5ddddcca488d207e9706808a180005ff2856a4e9 ; https://github.com/opendroneid/opendroneid-core-c/blob/master/CMakeLists.txt
- ZIM Tools: https://github.com/openzim/zim-tools/releases/tag/3.8.0 ; https://github.com/openzim/zim-tools/actions/runs/39216346633 ; https://github.com/openzim/zim-tools/actions/runs/39216346666 ; https://github.com/openzim/zim-tools/blob/main/meson.build

## Follow-up
Validate rclone serving security advisory patch boundaries; compare OpenDroneID tagged release to master fixes and test decoder boundaries; exercise a zimwriterfs → zimcheck → reader round trip. Continue legacy score backfill. No YouTube transcript evidence used.
