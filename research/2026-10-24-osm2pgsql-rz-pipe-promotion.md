# osm2pgsql and rz-pipe — upstream evidence and catalog promotion (2026-10-24)

## Repository hygiene and provenance
- Continued existing draft PR #7 on `agent/research-ladybird-browser-engine` from parent `258cd30a2f4566b648888f33bf6b08c4401962f4`; no unrelated branch or merge.
- Starting canonical catalog: 74 entries; both repository URLs and names absent, and candidate queue empty. This batch promotes 2 entries, updates matching MASTER_LIST headings, and records a dated YouTube access limitation.
- All six supplied YouTube playlist IDs searched by exact ID; no indexed playlist or transcript material obtained. These are GitHub-first discoveries, not video-derived claims.
- No third-party implementation source, assets, binary artifacts or firmware copied into GitHub Gold.

## osm2pgsql — VERIFIED (upstream), S / 28
- Source: https://github.com/osm2pgsql-dev/osm2pgsql ; official documentation https://osm2pgsql.org/doc/
- Purpose: OSM/PBF/O5M ingestion into PostgreSQL/PostGIS with configurable Lua flex outputs, geometry assembly, replication-diff updates and dirty-tile expiration.
- Inspected: `README.md`, `COPYING`, `CMakeLists.txt`, `src/`, `tests/`, `flex-config/README.md`, `.github/workflows/ci.yml`, `.github/actions/build-and-test/action.yml`, release metadata and master commits.
- Reusable components: `src/input.cpp`, `src/osmdata.cpp` (input); `src/output-flex.cpp`, `src/flex-lua-*.cpp` (flex output); `src/geom-from-osm.cpp`, `src/geom-functions.cpp` (geometry); `src/expire-tiles.cpp`, `src/expire-output.cpp` (incremental dirty-tile tracking); `src/node-persistent-cache.cpp` (storage); `flex-config/*.lua` (documented examples).
- Evidence: 2.3.1 release on 2026-07-05 https://github.com/osm2pgsql-dev/osm2pgsql/releases/tag/2.3.1 fixed a segfault in diff-expire on multiple output tables and a manpage install issue. Master commit 5d821cce (2026-10-15) added grouped-linemerge example.
- CI: https://github.com/osm2pgsql-dev/osm2pgsql/actions/runs/38734399518 (2026-10-15) passed 20/20 jobs including Linux/PostgreSQL matrix and Windows builds; composite build-and-test action explicitly runs `make` and `ctest`, using `pg_virtualenv` where configured. https://github.com/osm2pgsql-dev/osm2pgsql/actions/runs/38734399525 passed 2/2 installation jobs. Lint and clang-tidy workflows also succeeded on 2026-10-15.
- Requirements: C++17 and CMake, PostgreSQL >=12 (14+ recommended), PostGIS >=3.0, Lua and required C++/GIS libraries; Linux/Windows/macOS documented. Global imports need considerable resources.
- License: README states GPL v2 or later; inspected `src/expire-tiles.hpp` carries GPL-2.0-or-later SPDX. `flex-config/README.md` explicitly dedicates example configurations to public domain. Included third-party libraries and OSM dataset licensing require separate review.
- Score: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4 = **28 / S**. Strong upstream CI is not an independent import.
- Ecosystem: `osm2pgsql-dev/osm2pgsql-themepark` is a companion; `osmcode/libosmium` and `mapbox/protozero` are input dependencies. `onthegomap/planetiler` and `protomaps/PMTiles` are adjacent map-stack tools, not assumed dependencies.
- Follow-up: run a small OSM PBF import and repeat diff application in isolated PostgreSQL/PostGIS; test multi-expire-output regression, dirty tile correctness, and Lua data conversion; review OpenStreetMap ODbL attribution for downstream datasets.

## rz-pipe — VERIFIED (upstream), A / 24
- Source: https://github.com/rizinorg/rz-pipe ; discovered recursively from existing Rizin entry.
- Purpose: Rizin command/JSON automation through Python, Go, Rust, Haskell, OCaml, Ruby and Racket; transports include subprocess/pipe, TCP, HTTP, and other Rizin IPC methods.
- Inspected: root README, `python/README.md`, `python/LICENSE`, `python/setup.py`, `python/rzpipe/open_sync.py`, `python/tests/`, `rust/Cargo.toml`, `rust/README.md`, `rust/src/`, `go/Makefile`, Go source/tests, Haskell LICENSE, CI workflow and commit history.
- Upstream CI https://github.com/rizinorg/rz-pipe/actions/runs/36352169977 succeeded on 2026-09-27: 2/2 jobs. Ubuntu job builds Rizin, runs Python pytest, Go `go test`, OCaml installation, Rust `cargo build`, Ruby make, and Racket `raco test`; Rust format/Clippy job passes. **Rust unit tests were not executed by this workflow.**
- Latest inspected master commit b2fa2dfd (2026-09-27) adds Racket support; preceding change fixed Python command response handling of embedded NUL bytes. No GitHub Releases objects returned; `rust/Cargo.toml` version 0.1.0 is a manifest value, not a verified published release.
- License: Python and Haskell have MIT LICENSE; Rust has MIT OR Apache-2.0. No root LICENSE; Go, Ruby, OCaml, Racket need file/package-level confirmation before copying. No code copied.
- Score: Utility 4, Working Evidence 4, Reusability 5, Novelty 3, Documentation 4, Maintenance 4 = **24 / A**. Working evidence is upstream tests/builds only; maintenance lacks a release cadence.
- Security: `python/rzpipe/open_sync.py` supports HTTP and TCP endpoints and starts local Rizin with `Popen(..., shell=False)`; remote transport encryption/authentication is not established by source inspected. Avoid untrusted endpoints and publicly exposed remote Rizin services. Command transport can invoke arbitrary Rizin analysis commands.
- Follow-up: confirm licenses of all bindings; test Python NUL framing and stderr behavior, timeout/termination and Windows portability; test Rust APIs with real Rizin; verify remote transport security controls and whether versioned releases exist outside GitHub.

## Verification boundary
- GitHub Gold performed upstream source and CI inspection only. No independent code builds, installs, PostGIS imports, Rizin commands, remote connections, benchmarks or security audits were performed.
