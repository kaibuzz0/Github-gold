# GitHub Gold research — Paperless-ngx and Briar (2026-10-26 CDT / 2026-10-27 UTC)

## Scope and provenance
GitHub-first inspection of upstream READMEs, source paths, manifests, licensing, releases and CI. The first two seed YouTube playlists (PLMI6SBmd587c and PLfidXW0BixTc) were requested but throttled; no transcript attribution. No upstream implementation code or assets copied. Neither project was installed, built, executed, audited, or hardware-tested locally.

## Paperless-ngx — VERIFIED (upstream), S/28
- Repository: https://github.com/paperless-ngx/paperless-ngx
- Stable v3.3.4 (2026-10-22): https://github.com/paperless-ngx/paperless-ngx/releases/tag/v3.3.4 ; upstream notes dependency security updates for certifi, Pillow and aiohttp, not a confirmed application-code flaw.
- Backend Tests https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424424887 passed on 2026-10-27 UTC: Python 3.11/3.12/3.13/3.14, typing and CI gate. Docker https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424424910 passed amd64, arm64 and manifest. CodeQL https://github.com/paperless-ngx/paperless-ngx/actions/runs/40424425034 passed Python and JavaScript. These runs were on PR branch fix/14557, not proof that every dev revision passed. Frontend run 40424424907 passed its gate, but unit/e2e/build jobs were skipped because no frontend changes were detected.
- Inspected reusable source: `src/documents/consumer.py` ingestion, `src/paperless/parsers/tesseract.py` Tesseract/OCRmyPDF integration, `src/documents/classifier.py`, `src/documents/search/`, `src/documents/permissions.py`, `src/documents/tests/test_permission_filtering_security.py`, `src/documents/export/`, `docker/compose/`. `pyproject.toml` requires Python >=3.11 and includes Django/Celery and document-processing dependencies.
- Root license GPL-3.0; inspect exact dependencies and files before any reuse. Upstream README warns documents are stored unencrypted at rest: trusted host, access control and backups are mandatory operational considerations.
- Follow up: permission-regression coverage for sharing, OCRmyPDF subprocess limits and malformed-file handling, backup/restore verification, deployment isolation and license audit.

## Briar Android — PROMISING, A/25
- GitHub mirror: https://github.com/briar/briar ; canonical development: https://code.briarproject.org/briar/briar
- Official Briar website https://www.briarproject.org/ states release 1.5.22 on 2026-10-13. GitHub mirror commit d03d6fc on 2026-10-09 bumps version to 1.5.22; adjacent commits upgrade Tor to 0.4.9.14. GitHub releases endpoint returns no release objects, which does not negate the official release.
- Inspected `bramble-core/src/main/java/org/briarproject/bramble/crypto/` (cryptography), `bramble-core/src/main/java/org/briarproject/bramble/sync/` (sync), `bramble-android/src/main/java/org/briarproject/bramble/plugin/bluetooth/` (Bluetooth), `bramble-android/src/main/java/org/briarproject/bramble/plugin/tcp/` (LAN), `bramble-core/src/main/java/org/briarproject/bramble/plugin/file/` (mailbox/removable media), `bramble-core/src/test/java/org/briarproject/bramble/sync/SyncIntegrationTest.java` and mailbox tests.
- `briar-android/build.gradle` declares Android minSdk 21, targetSdk 35 and versionName 1.5.22. Root build.gradle specifies Java/Kotlin/Tor dependencies; GitLab CI declares Gradle builds/checks, emulator and reproducibility jobs. Passing canonical GitLab pipeline outcome could not be inspected, so not marked VERIFIED.
- License `LICENSE.txt` GPL-3.0-or-later; review included submodules, Tor/crypto dependencies and notices before copying.
- Follow up: inspect GitLab pipeline results, release signature and APK reproducibility, test actual Bluetooth/LAN/Tor transfer and mailbox synchronization, threat-model/privacy boundaries, and compare Briar Mailbox/Desktop components. Reticulum is only a conceptual alternative, not a verified integration.

## Maintenance
- Updated existing Tesseract OCR cross-reference to Paperless-ngx. Paperless `src/paperless/parsers/tesseract.py` explicitly names Tesseract and uses OCRmyPDF, establishing an actual downstream integration rather than speculative compatibility.
- Deferred PocketBase: https://github.com/pocketbase/pocketbase README now explicitly states repository moved to https://ganigeorgiev.com/pocketbase/pocketbase; evaluate new canonical upstream and GitHub mirror freshness before cataloging. No claim of abandonment.
- Open MCT remains PROMISING/A25; no new verified passing Playwright e2e evidence obtained in this batch. Existing Node >=24.14.1 vs CI Node 18 EBADENGINE failure remains documented.

## Verification boundary
All evidence is repository-native or official release/CI inspection. No local builds, deployment, document ingestion, OCR accuracy checks, radio tests, security audits or code copying.
