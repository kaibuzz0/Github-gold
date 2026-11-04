# 2026-10-27: yt-dlp and Immich — source and CI research

**Provenance:** GitHub-first. Two playlist pages throttled; exact-ID search found no usable transcripts. No independent builds, downloads, installations, hardware tests, ML inference or security audits. No third-party implementation code copied.

## yt-dlp — VERIFIED upstream, S29

- Repository: https://github.com/yt-dlp/yt-dlp ; stable 2026.10.26 released 2026-10-26 22:25 UTC.
- Root Unlicense; optional tools and media rights separate. Python >=3.11 per `pyproject.toml`.
- Source inspected: `yt_dlp/extractor/common.py` (extractor base), `yt_dlp/downloader/http.py` (range/resume/retry), `yt_dlp/plugins.py` (plugin loader), `yt_dlp/YoutubeDL.py` (orchestrator), `yt_dlp/networking/` and `yt_dlp/postprocessor/`.
- CI: https://github.com/yt-dlp/yt-dlp/actions/runs/40404432725 passed 13 core test jobs (Python 3.11–3.15/PyPy, Windows/Linux); https://github.com/yt-dlp/yt-dlp/actions/runs/40404432887 passed two quick tests; https://github.com/yt-dlp/yt-dlp/actions/runs/40404432831 CodeQL passed. Later core workflow 40409938717 was skipped.
- ArchiveBox README already documents yt-dlp as an external optional downloader; added catalog cross-reference. No integration test.
- Caveats: Site extractors break as websites change; untrusted plugins execute code; cookies sensitive; legal permission for archived material required.
- Follow-up: authorized subtitle-only extraction, cookie isolation, plugin security, upstream release provenance.

## Immich — PROMISING, A25

- Repository: https://github.com/immich-app/immich ; stable v3.3.5 released 2026-10-21.
- Root AGPL-3.0. Separate model weights, assets, FFmpeg and dependency licenses. Docker/PostgreSQL/Redis server and mobile/web clients.
- Source inspected: `server/src/services/asset.service.ts` (permission checks); `duplicate.service.ts` (duplicate resolution); `database-backup.service.ts` (scheduled DB backup); `machine-learning/immich_ml/pipeline.py` (CLIP/face/OCR inference requests); server unit test tree.
- 2026-10-27 upstream CodeQL https://github.com/immich-app/immich/actions/runs/40492780574 and static analysis https://github.com/immich-app/immich/actions/runs/40492780708 passed. Test workflow https://github.com/immich-app/immich/actions/runs/40492780438 failed overall: server test/lint passed; SQL schema image pull and e2e Docker Compose hit GHCR `toomanyrequests`; medium test lacked PostgreSQL image. This is infrastructure evidence, not proof of an application regression. Mobile workflow 40492780707 succeeded only at gate; actual Android/iOS build jobs skipped.
- Caveats: Official 3-2-1 backup warning. DB backups alone do not protect image/video files. Face/location data and shared links are sensitive.
- Follow-up: clean end-to-end CI after registry recovery; complete media+database restore; authorization regression and model licensing.

## Hygiene and scoring

- yt-dlp 5/5/5/4/5/5 = 29, VERIFIED upstream (not independently executed).
- Immich 5/3/5/3/5/4 = 25, PROMISING (integrated CI incomplete).
- ArchiveBox cross-reference improved. Catalog and master now 110 unique entries; 110 valid six-factor breakdowns; no duplicate canonical URLs. No copied source.
