# GitHub Gold — scrcpy, Syncthing and ntfy maintenance evidence (2026-10-21)

Scope: refresh three **existing** catalog entries, add missing six-factor Gold scoring, and document release, implementation, test, and licensing evidence. All findings are from primary GitHub sources; no transcript-derived discoveries or third-party code copying.

## scrcpy — VERIFIED (upstream), S / 29

- Repository: https://github.com/Genymobile/scrcpy (Genymobile / Romain Vimont).
- Score: Utility 5; Working Evidence 5; Reusability 5; Novelty 5; Documentation 5; Maintenance 4.
- Release: v5.0.1, **2026-10-08** — https://github.com/Genymobile/scrcpy/releases/tag/v5.0.1 . The old v4.1 snapshot was stale. This patch fixes Linux VA-API GPU selection, NVIDIA NV12 chroma-plane handling, Windows H.265 hardware decoding and EGL handling after v5 introduced hardware decoding.
- Evidence: README documents Android USB/TCP mirroring/control without root or a permanent installed app. Root `server/` and `app/` separate Android server from host client. Useful components: ADB tunnel, temporary server, media/control sockets, codec and render pipelines, UHID/OTG.
- Upstream CI: https://github.com/Genymobile/scrcpy/actions/runs/37737030700 — **17/17 successful jobs**, including server/client tests and cross-platform builds/packages. No independent hardware/GPU/USB execution.
- Runtime: Android target, Linux/Windows/macOS host; Java Android server, C desktop client; Gradle/Meson build infrastructure.
- License: root Apache-2.0 verified; review third-party dependencies and assets before copying. No source copied.
- Follow-up: map hardware-decoder compatibility and version-coupled server/client protocol.

## Syncthing — VERIFIED (upstream), S / 29

- Repository: https://github.com/syncthing/syncthing (Syncthing organization).
- Score: Utility 5; Working Evidence 5; Reusability 5; Novelty 5; Documentation 5; Maintenance 4.
- Release: v2.1.7, **2026-10-21** — https://github.com/syncthing/syncthing/releases/tag/v2.1.7 . Notes document Go 1.27.3, SQLite cleanup/prepared-statement fixes, receive-only reconciliation, protocol error handling and validation of incoming messages.
- Evidence: README documents continuous peer-to-peer folder synchronization. `lib/` contains `protocol/`, `model/`, `discover/`, `relay/`, `scanner/`, `versioner/`, `api/` and `fs/` — reusable components for replication and filesystem safety.
- Upstream main CI: https://github.com/syncthing/syncthing/actions/runs/39487469482 — Linux/macOS/Windows build-and-test jobs and govulncheck **succeeded**; some signing, lint and release jobs were **skipped**, not successes. No independent sync test.
- Runtime: Go source/build; native desktop/server and container packages. License: MPL-2.0 verified; file-level copyleft applies to covered source. No code copied.
- Follow-up: test receive-only and deletion semantics, fuzz protocol boundaries, assess discovery/relay privacy.

## ntfy — VERIFIED (upstream), S / 27

- Repository: https://github.com/binwiederhier/ntfy (Philipp C. Heckel).
- Score: Utility 5; Working Evidence 4; Reusability 5; Novelty 4; Documentation 5; Maintenance 4.
- Release: v2.32.0, **2026-10-18** — https://github.com/binwiederhier/ntfy/releases/tag/v2.32.0 . Adds RFC 10036 `Incremental: ?1` for streaming subscription proxies and early passive-node clustering/database compatibility controls.
- Evidence: README documents HTTP PUT/POST notifications. `server/` contains authorization, topic handling, cluster, Web Push and extensive tests; `client/`, `db/` and `web/` are separately reusable. Experimental clustering is not proven high availability.
- Upstream main test: https://github.com/binwiederhier/ntfy/actions/runs/39182637748 — test job **passed** 2026-10-19. No independent deployment, stream delivery or failover test.
- Runtime: Go server and web client; self-hosted HTTP(S), packages/containers. Root Apache-2.0 LICENSE and additional LICENSE.GPLv2 both present: check scope for specific files before reuse. No code copied.
- Follow-up: inspect `server/server_cluster.go` failover behavior, reverse-proxy buffering, secondary license applicability and topic privacy.

## Evidence boundary and catalog hygiene

All results above derive from inspected upstream README/license/source trees, dated releases and GitHub Actions conclusions. GitHub Gold did not independently compile, install, benchmark, run a synchronization session, control a phone, deploy a server or perform a security audit. Three pre-existing canonical records were refreshed; the catalog remains at **50** unique projects with **28** six-factor scoring breakdowns.
