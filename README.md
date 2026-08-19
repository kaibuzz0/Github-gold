# GitHub Gold

A curated research repository for discovering high-value open-source projects, working tools, reusable code, techniques, and technical leads from YouTube research, GitHub exploration, and related sources.

## Mission

Find useful projects and code, verify what is actually usable, and organize the results so the repository becomes a practical master index rather than a link dump.

## What counts as Gold

A strong candidate should have one or more of these qualities:

- working or plausibly working code
- practical utility
- unusual capability or clever implementation
- reusable components or algorithms
- clear documentation or runnable examples
- active maintenance, releases, tests, or meaningful community use
- useful hardware/software integration
- strong research value even if not production-ready

## Evidence levels

- **VERIFIED** — inspected and there is concrete evidence the relevant functionality works
- **PROMISING** — strong indicators, but not yet independently verified
- **LEAD** — worth deeper investigation
- **ARCHIVED** — interesting history or ideas, but obsolete, broken, superseded, or unsuitable for reuse

## Repository structure

- `MASTER_LIST.md` — human-readable master catalog
- `catalog/tools.json` — structured machine-readable catalog
- `sources/youtube_playlists.md` — seed playlists and research status
- `research/` — deeper notes and investigations
- `extracted/` — notes on specific reusable files/components; third-party code is only copied when licensing permits and attribution is preserved

## Research rules

1. Preserve the original project URL and author.
2. Record the license before copying or adapting code.
3. Prefer linking to upstream source over duplicating entire projects.
4. Identify the exact files/functions/components that are useful.
5. Separate observed facts from assumptions.
6. Record install/runtime requirements and platform constraints.
7. Avoid duplicate entries; connect forks and related projects.
8. Raise the evidence level only when supporting evidence is recorded.
9. Keep potentially dual-use tools described in legitimate research, defensive, interoperability, or authorized-testing context.

## Current seed source

The initial discovery corpus is six YouTube playlists supplied for transcript-driven research. See `sources/youtube_playlists.md`.
