# GitHub Gold — OCRmyPDF, gokrazy, and Open MCT maintenance (2026-10-27 UTC)

## Research provenance
GitHub-first inspection of README, licenses, source files, manifests, test trees, releases, workflows and job logs. Exact-ID searches for YouTube seeds `PLMI6SBmd587c` and `PLfidXW0BixTc` yielded no indexed playlist/transcript data. Six seeds remain in `sources/youtube_playlists.md`; neither project is attributed to video evidence. No third-party code/assets copied. No independent install, build, OCR processing, device boot, firmware flash or security audit.

## OCRmyPDF — VERIFIED (upstream), S/28
- Repository: https://github.com/ocrmypdf/OCRmyPDF ; stable `v17.13.0` published 2026-09-28: https://github.com/ocrmypdf/OCRmyPDF/releases/tag/v17.13.0 . Main `pyproject.toml` declares `17.13.1`, not verified as a released tag.
- License: MPL-2.0 for core; README CC-BY-SA-4.0; `LICENSES/` includes multiple notices; optional HEIC extra notes GPLv2 x265; external Tesseract, pikepdf, Ghostscript and fonts require separate review.
- Runtime: Python >=3.11, native OCR/PDF/image dependencies, Linux/macOS/Windows, CLI and Python API.
- Reusable source: `src/ocrmypdf/api.py` (OCR API and plugin concurrency locks), `src/ocrmypdf/_pipelines/ocr.py`, `src/ocrmypdf/pdfa.py` (PDF/A validation), `src/ocrmypdf/hocrtransform/hocr_parser.py`, `src/ocrmypdf/_exec/tesseract.py`, `src/ocrmypdf/pluginspec.py`, `src/ocrmypdf/_watcher_security.py`. Tests cover PDF/A final validation, decompression bombs, API, concurrency, input validation and plugins.
- Upstream main CI https://github.com/ocrmypdf/OCRmyPDF/actions/runs/40295734365 (2026-10-26) concluded success: 21 passed jobs, four experimental Python 3.15 install failures, one skipped. Python 3.11–3.14 tests on Linux/macOS/Windows, lint, wheels and Docker builds passed. The 3.15 matrix is `continue-on-error`; failed Ubuntu job https://github.com/ocrmypdf/OCRmyPDF/actions/runs/40295734365/job/121481326829 reports `onnxruntime==1.31.0` lacks cp315 wheel/sdist. Do not misrepresent those as OCR test failures.
- Caveats: watcher acknowledges TOCTOU and hardlink risks; plugin paths may execute Python code. API documents interpreter-global plugin and Pillow decompression-bomb state; different configurations require separate processes. No independent OCR accuracy or PDF/A conformance check.
- Follow-up: malformed PDF sandboxing, watcher race defenses, PDF/A independent validation, plugin trust, memory/CPU budgets, Python 3.15 dependencies and licensing of optional components.

## gokrazy — VERIFIED (upstream QEMU), S/27
- Repository: https://github.com/gokrazy/gokrazy ; companion image builder https://github.com/gokrazy/tools .
- License: BSD-3-Clause for core and tools; separate kernel/firmware/EEPROM/Go dependency licenses. `go.mod` requires Go 1.26. Supports Go appliance deployment to supported Raspberry Pi/PC hardware; `gok` builds images.
- Reusable source: `supervise.go` (supervision/logging), `update.go` (boot partition updates), `authenticated.go` (Unix socket if no password, HTTP Basic auth otherwise), `cmd/dhcp/dhcp.go`, `cmd/ntp/ntp.go`, `netlink.go`, `integration/mbrboot/mbrboot_test.go`, `integration/uefiboot/uefiboot_test.go`.
- Core main CI https://github.com/gokrazy/gokrazy/actions/runs/35105853192 (2026-09-16) passed gofmt, `go test -v ./...`, QEMU/KVM boot tests and disk image generation. Log explicitly reports **TestMBRBoot PASS (37.06s)** and **TestUEFIBoot PASS (20.48s)**; this is upstream simulated boot, not physical hardware validation. Feature CI https://github.com/gokrazy/gokrazy/actions/runs/37527198802 passed 2026-10-06. Companion tools https://github.com/gokrazy/tools/actions/runs/40385840520 passed Windows/macOS/Ubuntu jobs 2026-10-26.
- No core GitHub Releases found; do not invent a stable version. Investigate management HTTPS/auth exposure, update rollback, QEMU negative tests, hardware support, and binary supply chain.

## Existing catalog maintenance
- Open MCT remains PROMISING/A25. 2026-10-27 UTC https://github.com/nasa/openmct/actions/runs/40427389616 Ubuntu job https://github.com/nasa/openmct/actions/runs/40427389616/job/121936441613 log confirms `npm ci` EBADENGINE: required Node >=24.14.1, actual v18.20.8/npm 10.8.2. Windows cancelled; Playwright tests never executed. The separate `e2e-perf` run failed, but its latest root cause was not analyzed. Do not promote without passing e2e evidence.
- Added OCRmyPDF cross-reference to existing Tesseract OCR entry. Paperless-ngx already cites OCRmyPDF.
- Updated `MASTER_LIST.md` and `catalog/tools.json` in sync; 108 canonical entries, 108 headings, valid six-factor scoring and no duplicate repository URLs verified before publish. No upstream source copied.
