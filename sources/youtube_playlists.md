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
