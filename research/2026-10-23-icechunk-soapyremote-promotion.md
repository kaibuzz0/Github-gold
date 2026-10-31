# GitHub Gold — Icechunk and SoapyRemote promotion evidence
**Checked:** 2026-10-23 (America/Chicago)  
**Method:** GitHub-first recursive research using existing September dossiers plus current upstream README, source trees, manifests, licenses, changelogs, releases, commit history and GitHub Actions.  
**Independent execution:** None. No upstream implementation code, data or firmware copied.

## Icechunk — VERIFIED (upstream), S / 28
- **Upstream:** https://github.com/earth-mover/icechunk
- **Why it matters:** Adds committed snapshots, conflict-aware transactions, branches/tags, virtual chunk references and versioned scientific data management on top of the Zarr key/value model.
- **Source evidence:** Root Apache-2.0 license; README maps `icechunk-format/`, `icechunk-storage/`, `icechunk-arrow-object-store/`, `icechunk-s3/`, `icechunk/`, `icechunk-python/`; current tree also has `icechunk-js/`. Inspected `icechunk/src/` with `repository.rs`, `session.rs`, `conflicts/`, `virtual_chunks.rs` and `cli/`.
- **Requirements:** `icechunk-python/pyproject.toml` requires Python >=3.12 and `zarr>=3.1.0`. The v2.3.0 changelog raises Rust MSRV to 1.95 and changes the Rust repository-builder API.
- **Release:** v2.3.0 published **2026-10-06**: https://github.com/earth-mover/icechunk/releases/tag/v2.3.0. Changelog notes object-store request attribution, storage-class handling, memory improvements and Rust breaking changes. Do not conflate this release with subsequent unreleased fixes.
- **Positive CI:** 2026-10-23 upstream Python Check https://github.com/earth-mover/icechunk/actions/runs/39895350092 completed successfully. Its inspected jobs include build wheels, xarray backend compatibility, free-threaded tests, stateful compatibility, Hypothesis and minimum/latest dependency shards. This is upstream execution evidence, not GitHub Gold testing.
- **Negative CI:** 2026-10-23 Python CI and library release https://github.com/earth-mover/icechunk/actions/runs/39898974564 failed. Inspected first-page job failures include legacy `support/v1.x` Python 3.15t wheel builds on Windows/macOS. Many `main` wheel jobs succeeded. Treat this as a packaging-matrix warning; the failed workflow is not proof of broken v2.3.0 transaction semantics.
- **Score:** Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 5 + Maintenance 5 = **28/30**. Evidence held at 4 due to lack of independent object-store/concurrency testing and partially failed packaging workflow.
- **Risks:** Conditional-write semantics differ by backend; GC and branch reset require strong invariants; external-file virtual chunks have availability and integrity dependencies; datasets/backends have separate licenses. Apache-2.0 attribution and NOTICE requirements apply to covered source.
- **Prior dossier:** `research/2026-09-06-icechunk-transactional-zarr-object-storage-versioning.md`.
- **Next:** Inspect commit compare-and-swap implementation and Hypothesis/Shuttle test models; verify GC recovery and partial failures; test cloud metadata and snapshot-reference edge cases with reproducible fixtures.

## SoapyRemote — VERIFIED (upstream), A / 25
- **Upstream:** https://github.com/pothosware/SoapyRemote
- **Why it matters:** Transparent SoapySDR client/server network device abstraction; useful for remotely attached SDR hardware and as a reusable design for split control-plane RPC plus UDP/TCP sample streaming.
- **Source evidence:** Root `LICENSE_1_0.txt` is Boost Software License 1.0; inspected `client/`, `server/`, `common/`, `Changelog.txt`, `.github/workflows/ci.yml`, and `common/SoapyRemoteDefs.hpp`. Key files: `client/Streaming.cpp`, `client/DiscoverServers.cpp`, `server/ClientHandler.cpp`, `server/SoapyServer.cpp`, `server/ServerListener.cpp`.
- **Maintenance correction:** Older September dossier said latest completed release was 0.5.2 (2020). Current upstream changelog now declares **Release 0.5.3 (2026-10-10)**, including CMake updates, clock-rate API and IQ-balance API support. GitHub Releases API returned no Release object; this is a changelog version, not a confirmed published GitHub Release.
- **Commits:** 2026-09-29 fixed dereference on malformed remote calls; 2026-10-05 updated GitHub Actions; 2026-10-10 bumped version.
- **Positive CI:** Both 2026-10-10 upstream workflows succeeded: https://github.com/pothosware/SoapyRemote/actions/runs/38059816370 and https://github.com/pothosware/SoapyRemote/actions/runs/38059814840. Inspected Linux/macOS/Windows/FreeBSD jobs. Workflow builds SoapySDR + SoapyRemote and runs `SoapySDRUtil --check=remote`; this proves build/module registration in those jobs, **not** real end-to-end IQ streaming or physical RF operation.
- **Trust boundary:** `SoapyRemoteDefs.hpp` defines default service **55132**. The server man page documents broad interface binding; source and prior dossier show RPC operations include device-changing control, not read-only telemetry. No stock TLS/client-auth mechanism was identified in inspected code/docs, but absence was not formally proven. Use a trusted network, firewall or authenticated tunnel for remote hardware.
- **Score:** Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 4 + Documentation 3 + Maintenance 4 = **25/30**. Good current build evidence and recent maintenance, but limited end-to-end tests and no GitHub Release artifact.
- **License:** BSL-1.0 with copyright/license notice obligations for covered source; SoapySDR plugins/vendor SDKs and device firmware have independent licenses.
- **Prior dossiers:** `research/2026-09-05-soapyremote-network-transparent-sdr-transport.md` and `research/2026-08-29-soapyremote-network-trust-boundary.md`.
- **Next:** Build a localhost null-device client/server streaming test with known IQ samples; audit RPC deserialization bounds and discovery trust; verify network exposure and ACL behavior before use beyond trusted LAN.

## Provenance and boundaries
- Both projects were already deeply researched as September dossiers and were absent from the 62-entry canonical catalog and empty promotion queue before this run.
- YouTube seed playlists in `sources/youtube_playlists.md` remain registered. No transcript-derived evidence was available or attributed during this pass.
- No independent builds, installations, network streams, RF captures, cloud transactions, fuzzing, benchmarks or security audits were performed.
- No upstream source code was copied. Changes are limited to two canonical promotions and this research dossier.
