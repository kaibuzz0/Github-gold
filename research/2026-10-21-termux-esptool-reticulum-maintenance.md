# Maintenance review — 2026-10-21

**Scope:** Three existing canonical projects; no new entries or third-party code copied. Research based on repository-native README, source paths, releases, workflows, commits and license files. No independent installation, software execution, firmware flashing, RF tests or cryptographic audit.

## Termux Tools — VERIFIED (upstream), A/25
Factors: Utility 5, Working Evidence 4, Reusability 5, Novelty 3, Documentation 4, Maintenance 4.

- Repo: https://github.com/termux/termux-tools ; GPL-3.0 confirmed in COPYING.
- Components: scripts/pkg.in (package manager wrapper and mirror checks), scripts/termux-change-repo.in (interactive mirror selector), scripts/termux-backup.in, scripts/termux-restore.in, scripts/termux-fix-shebang.in, src/cmd.c and mirrors/.
- Stable v1.48.0, 2025-11-29: https://github.com/termux/termux-tools/releases/tag/v1.48.0 .
- Master commit 05c857ee (2026-10-16) added South American mirror: https://github.com/termux/termux-tools/commit/05c857ee9af84fb762efba3042cc9383ad1bacab .
- CI: https://github.com/termux/termux-tools/actions/runs/38838597990 — push-triggered Autotools Linux build/install, 1/1 job passed. Scheduled mirror-update workflows are not code tests.
- Limits: no independent Android execution or mirror reachability check. GPL obligations for code reuse.

## Espressif esptool — VERIFIED (upstream), S/28
Factors: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.

- Repo: https://github.com/espressif/esptool ; pyproject.toml and source SPDX headers specify GPL-2.0-or-later. Python >=3.10, pyserial, cryptography and other dependencies; Linux/macOS/Windows hosts.
- Components: esptool/loader.py (serial bootloader protocol), esptool/bin_image.py (image/Intel HEX parsing), esptool/cmds.py, esptool/targets/, espefuse/, espsecure/. Companion flasher stub source: https://github.com/espressif/esp-flasher-stub .
- Stable v5.6.0 released 2026-10-15: https://github.com/espressif/esptool/releases/tag/v5.6.0 .
- Master commit 93477ace (2026-10-20) added --encrypt-files alignment validation: https://github.com/espressif/esptool/commit/93477aceb5bc28971db26223a60339bb53e9390a . Do not assume it is in v5.6.0.
- CI: https://github.com/espressif/esptool/actions/runs/39435542641 — 7/7 host-test and stub-check jobs passed (Python 3.10–3.15). https://github.com/espressif/esptool/actions/runs/39435542027 — six cross-platform build jobs passed; release step skipped.
- Limits: host CI does not prove physical flashing, eFuse safety or security. Inspect bundled firmware/dependency licenses separately.

## Reticulum Network Stack — VERIFIED (upstream), A/24 (down from A/25)
Factors: Utility 5, Working Evidence 4, Reusability 3, Novelty 5, Documentation 5, Maintenance 2.

- Repo: https://github.com/markqvist/Reticulum . Custom license: https://github.com/markqvist/Reticulum/blob/master/LICENSE prohibits harmful systems and AI/ML training datasets. Not a standard OSI-approved license; do not copy/adapt source without legal review or permission. Protocol public-domain statement is not a blanket source license.
- Critical maintenance notice: https://github.com/markqvist/Reticulum/blob/master/MIRROR.md — public GitHub mirror, development elsewhere, no issue responses, public support, community management or predictable update schedule. This lowers maintenance confidence; it does not prove code is broken.
- Components: RNS/Interfaces/ (RNode, KISS, TCP, UDP, serial, backbone), RNS/Transport.py, RNS/Link.py, RNS/Identity.py, RNS/Channel.py, RNS/Resource.py, tests/, Examples/. Standard Python setup lists cryptography >=3.4.7 and pyserial >=3.5.
- Stable 1.5.5, 2026-09-29: https://github.com/markqvist/Reticulum/releases/tag/1.5.5 . Master mirror commit e40191b (2026-09-30).
- CI: https://github.com/markqvist/Reticulum/actions/runs/36723645574 — make test succeeded (1 test job), tag-only package/release skipped.
- Limits: no live transport, radio, interoperability or independent cryptographic tests.

## Next research
Check Reticulum license compatibility before any code reuse; confirm esptool alignment fix in a future release; validate Termux mirror failover on Android; continue remaining 13 legacy score breakdowns; revisit abx-plugins CI. Six YouTube playlist seeds remain registered; no usable transcript evidence was established for this batch.
