# GitHub Gold — Organic Maps, Kopia and age maintenance

2026-10-21. GitHub-first maintenance; no YouTube-derived evidence. VERIFIED means upstream code/release/CI evidence, not independent execution. No third-party source code copied.

## Organic Maps — VERIFIED / S / 29 (5+5+5+5+5+4)

- Repository: https://github.com/organicmaps/organicmaps
- Evidence: Android release 2026.09.29-32-android (2026-09-29); master Android/iOS navigation updates 2026-10-21; main Android Check, Android Beta, iOS Check, CMake and translation workflows succeeded 2026-10-21. One feature-branch Android Check failed; this is not a main-branch failure.
- Reusable source paths: `libs/routing/`, `libs/search/`, `libs/storage/`, `libs/mwm_diff/`, `libs/kml/`, `generator/`, `android/`, `iphone/`
- License, testing and risk boundary: Source is Apache-2.0; binary map/data use separate DATA_LICENSE.txt including ODbL/CC BY-SA upstream terms. No on-device navigation, route accuracy, or map-generation test.
- Sources:
  - https://github.com/organicmaps/organicmaps/releases/tag/2026.09.29-32-android
  - https://github.com/organicmaps/organicmaps/actions/runs/39606979087
  - https://github.com/organicmaps/organicmaps/blob/master/DATA_LICENSE.txt

## Kopia — VERIFIED / S / 28 (5+5+5+4+5+4)

- Repository: https://github.com/kopia/kopia
- Evidence: v0.23.1 (2026-06-16) fixes a rare epoch-compaction index race that may cause data loss (#5371); upstream recommends upgrade. 2026-10-21 master stress/endurance workflows succeeded. Providers - Core workflow failed: Azure PIT tests got nil version IDs; S3 MinIO integration tests could not pull minio/minio Docker image.
- Reusable source paths: `repo/content/`, `repo/blob/`, `repo/encryption/`, `repo/compression/`, `repo/ecc/`, `repo/splitter/`, `snapshot/`, `cli/`, `repo/api_server_repository.go`
- License, testing and risk boundary: Root license Apache-2.0. No independently performed backup/restore or regression test. Provider CI is not all green; check Azure versioning and MinIO test infrastructure.
- Sources:
  - https://github.com/kopia/kopia/releases/tag/v0.23.1
  - https://github.com/kopia/kopia/issues/5371
  - https://github.com/kopia/kopia/actions/runs/39634509364
  - https://github.com/kopia/kopia/actions/runs/39563290238

## age — VERIFIED / S / 27 (5+4+5+4+5+4)

- Repository: https://github.com/FiloSottile/age
- Evidence: v1.3.2 (2026-08-29) adds parser/input hardening and new binary/platform coverage. Main Go tests passed 2026-10-21; earlier main tests failed October 10–12, with later successful runs. Feature-branch checks are not counted as main evidence.
- Reusable source paths: `age.go`, `x25519.go`, `scrypt.go`, `pq.go`, `plugin/`, `cmd/age/`, `cmd/age-keygen/`, `cmd/age-inspect/`, `age_test.go`
- License, testing and risk boundary: Root BSD 3-Clause-style license requires notices; plugin/dependency terms vary. No independent cryptographic audit, interoperability, fuzzing, CLI encryption or decryption test.
- Sources:
  - https://github.com/FiloSottile/age/releases/tag/v1.3.2
  - https://github.com/FiloSottile/age/actions/runs/39579906755
  - https://github.com/FiloSottile/age/blob/main/LICENSE

## Next leads

- Organic Maps: incremental map diffs and offline search/routing resource costs.
- Kopia: compaction regression coverage, Azure PIT versioning, MinIO test image and isolated restore tests.
- age: plugin interoperability fixtures and malformed-header regression tests.
