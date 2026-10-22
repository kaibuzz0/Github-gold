# 2026-10-22 — SOPS and MCUboot verification update

Research status: candidate promotion recommended; no independent execution.

## SOPS (getsops/sops)
Upstream: https://github.com/getsops/sops
Proposed VERIFIED / S 28 (Utility 5, Working 5, Reusability 5, Novelty 4, Docs 5, Maintenance 4).
Structured encrypted configuration for YAML/JSON/ENV/INI/binary. Reusable modules: `stores/` format adapters, `age/` and cloud-KMS providers, `keyservice/` gRPC, `shamir/` key groups, `audit/`.
Release v3.13.3 (2026-07-23): https://github.com/getsops/sops/releases/tag/v3.13.3
Upstream CLI main CI on 2026-10-20 passed 17/17 jobs: https://github.com/getsops/sops/actions/runs/39370255127
License: MPL-2.0 (root and shamir/LICENSE). File-level source and notice obligations. No code copied.
Limits: CI is not a cryptographic audit; editor plaintext, endpoint compromise and KMS/keyservice trust require independent assessment.

## MCUboot (mcu-tools/mcuboot)
Upstream: https://github.com/mcu-tools/mcuboot
Proposed VERIFIED / S 29 (Utility 5, Working 5, Reusability 5, Novelty 5, Docs 5, Maintenance 4).
Secure firmware boot/update framework. Components: `boot/bootutil/` image validation and swap, `boot/boot_serial/` recovery, `scripts/imgtool.py` signing, `sim/` regression harness.
Stable release v2.4.0 (2026-04-23): https://github.com/mcu-tools/mcuboot/releases/tag/v2.4.0
Source bumped to 2.5.0 on 2026-10-22; a stable 2.5.0 GitHub release was not verified.
Upstream main simulator CI passed 42/42 jobs on 2026-10-22: https://github.com/mcu-tools/mcuboot/actions/runs/39761866485
Main Zephyr, Espressif, imgtool and FIH workflows also passed 2026-10-22. Separate feature-branch failures are not main failures.
License: Apache-2.0 plus NOTICE; bundled crypto licenses require separate review. No code copied.
Limits: no independent compilation, flashing, physical fault injection or hardware trust-chain test.

Prior research: `research/2026-08-27-sops-secrets-management.md` and `research/2026-09-07-mcuboot-secure-boot-firmware-update-verification.md`.
Current catalog: 50 canonical records; these two are not yet cataloged. Promote only with synchronized master/JSON edits. No transcript-derived YouTube findings.
