# YouTube Seed Playlists

These playlists are the initial transcript-driven discovery corpus. Research should extract project names, repositories, developer names, tools, libraries, protocols, hardware, techniques, keywords, and references that can lead to useful open-source code.

## Seeds

1. `PLMI6SBmd587c`
   - https://youtube.com/playlist?list=PLMI6SBmd587c
   - Status: queued

2. `PLfidXW0BixTc`
   - https://youtube.com/playlist?list=PLfidXW0BixTc
   - Status: queued

3. `PLI99ObbYUvDn_0tkbXsOYB4ApTyHFQxSi`
   - https://youtube.com/playlist?list=PLI99ObbYUvDn_0tkbXsOYB4ApTyHFQxSi
   - Status: queued

4. `PLIzKw1zY_ruBUkaijwskxrfApmK_sKPvO`
   - https://youtube.com/playlist?list=PLIzKw1zY_ruBUkaijwskxrfApmK_sKPvO
   - Status: queued

5. `PLPKYjlUn3Lxl-XOQ0P0FpIgDZit2rYlE3`
   - https://youtube.com/playlist?list=PLPKYjlUn3Lxl-XOQ0P0FpIgDZit2rYlE3
   - Status: queued

6. `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr`
   - https://youtube.com/playlist?list=PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr
   - Status: queued

## Transcript mining workflow

For each video with usable subtitles or transcript data:

1. Record video title, URL, channel, and date when available.
2. Extract named projects, GitHub URLs, developers, libraries, hardware, protocols, product names, technical phrases, and distinctive keywords.
3. Search GitHub for exact names plus semantic/related alternatives.
4. Follow promising repositories into forks, dependencies, contributors, related projects, releases, and linked papers/sites.
5. Identify specific useful files, functions, modules, scripts, firmware, or designs.
6. Check license before copying code.
7. Add candidates to `catalog/tools.json` and promote sufficiently researched entries into `MASTER_LIST.md`.
8. Record dead ends so later research does not repeat them.

## Research principle

A transcript mention is a lead, not proof. GitHub popularity is also not proof. The goal is to discover and verify genuinely useful code and tools.

## Access check — 2026-10-24

Exact-ID web searches for all six seed playlist identifiers returned no indexed playlist or transcript material during this research batch. No video metadata, transcript content or GitHub discoveries were attributed to those searches. The seeds remain queued for direct metadata/subtitle access in a later run; do not infer that videos were viewed or that a playlist was empty.

## Access check — 2026-10-27

Direct requests to seed playlists `PLMI6SBmd587c` and `PLfidXW0BixTc` were throttled; exact-ID searches returned no indexed transcripts. Neither discovery was attributed to video evidence. The other four playlists were not revisited in this batch.

## Access check — 2026-10-27 (additional seed IDs)

Exact-ID searches for `PLIzKw1zY_ruBUkaijwskxrfApmK_sKPvO` and `PLPKYjlUn3Lxl-XOQ0P0FpIgDZit2rYlE3` returned no indexed playlist or transcript material. No direct viewing or subtitle extraction occurred, and no discoveries were attributed to these playlists.

## Access check — 2026-10-27 (remaining seed IDs)

Exact-ID searches for `PLI99ObbYUvDn_0tkbXsOYB4ApTyHFQxSi` and `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr` returned no indexed playlist or transcript material. No video or subtitles were accessed and neither discovery was attributed to video evidence. All six IDs have now been searched at least once; direct metadata/subtitle access remains queued.
