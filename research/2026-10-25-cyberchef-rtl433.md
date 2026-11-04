# CyberChef and rtl_433 discovery and maintenance — 2026-10-25

## Provenance and repository state
- Reviewed current draft PR #7 head `01d8e97e` on `agent/research-ladybird-browser-engine`, README, 88-entry catalog, master list, existing radio entries and playlist seeds before editing.
- Exact-ID web searches for `PLMI6SBmd587c` and `PLfidXW0BixTc` returned no indexed transcript/metadata. No findings attributed to YouTube. The remaining four seed playlists were not directly checked this run.
- No upstream implementation code or assets copied. Evidence below is upstream CI, not independent installation or hardware testing.

## CyberChef — VERIFIED (upstream), S/28
- Repo: https://github.com/gchq/CyberChef ; root LICENSE Apache-2.0; package.json 11.5.0.
- Score: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- Source inspected: README, SECURITY.md, LICENSE, package.json, `src/core/Chef.mjs`, `Operation.mjs`, `src/core/operations/` (506 listed files), `tests/`, `.github/workflows/master.yml`.
- Stable v11.5.0 published 2026-09-18: https://github.com/gchq/CyberChef/releases/tag/v11.5.0
- Upstream 2026-10-23 https://github.com/gchq/CyberChef/actions/runs/39942157083 : 2/2 jobs passed. Both Node 24 and 26 jobs passed lint, unit tests, production build, browser UI tests. No independent execution.
- Components: `Chef.mjs` baking, `Recipe.mjs` pipeline, `Dish.mjs` typed payload, `Operation.mjs` extension contract, `src/node/` consumer API, per-operation modules and test suites.
- Caveats: SECURITY.md explicitly disclaims crypto correctness/security; inspect operation-specific dependencies and any sensitive-data handling. Third-party package and vendored licenses need separate review. Browser local-first claim is deployment-dependent.
- Next: examine crypto-operation test vectors and security boundaries, large-file memory use, supply-chain and vendored-license audit.

## rtl_433 — VERIFIED (upstream), S/27
- Repo: https://github.com/merbanan/rtl_433 ; COPYING GPL-2.0 text, `src/rtl_433.c` and `src/bitbuffer.c` GPL-2.0-or-later headers.
- Score: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 4, Maintenance 4.
- Source inspected: README, COPYING, CMakeLists.txt, `src/`, `src/devices/` (331 listed files), `tests/`, `.github/workflows/check.yml`.
- Stable 25.12 published 2025-12-12: https://github.com/merbanan/rtl_433/releases/tag/25.12 ; nightly prerelease object 2026-09-20.
- Upstream 2026-10-23 https://github.com/merbanan/rtl_433/actions/runs/39967799370 : 12/12 jobs passed; Linux debug/release builds/tests, macOS builds/tests, coverage suite, Clang analyzer, style and docs. Linux matrix disables hardware backends. Later 2026-10-24 run https://github.com/merbanan/rtl_433/actions/runs/40144928023 ended action_required; not equivalent to a tested build failure.
- Components: pulse detection/FSK, slicer, bitbuffer, device decoders, MQTT/Influx/HTTP outputs and sample-file processing. C99 and CMake.
- Caveats: no SDR hardware test, RF decoding accuracy validation or security audit. MQTT/HTTP exposure and sensor identifier privacy; per-file licenses for bundled sources. Use within applicable spectrum law.
- Next: examine device decoder test fixtures, protocol coverage, malformed packet fuzzing and SoapySDR input behavior.

## Maintenance
- Cross-linked `merbanan/rtl_433` from the existing SoapySDR entry in JSON and master list. SoapySDR evidence/score unchanged; integration is upstream-documented, not independently RF-tested.
- No changes to other existing scores or classifications.
