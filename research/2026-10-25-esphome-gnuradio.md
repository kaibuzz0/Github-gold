# ESPHome and GNU Radio research batch — 2026-10-25

## Provenance and hygiene
- Continued existing draft PR #7 branch `agent/research-ladybird-browser-engine` from head `cbe38daae71e`, after reading README, full catalog, MASTER_LIST, playlist seeds and recent research notes. Confirmed 90 unique canonical entries before adding two; checked aliases and canonical URLs. No unrelated work merged or deleted.
- GitHub-first discovery. Exact-ID web searches for playlist seeds `PLIzKw1zY_ruBUkaijwskxrfApmK_sKPvO` and `PLPKYjlUn3Lxl-XOQ0P0FpIgDZit2rYlE3` produced no usable indexed transcripts or video metadata. No video-derived claims.
- Evidence is upstream source, releases, commits and CI. No independent installs, builds, RF/hardware tests, security audits or third-party code copies.

## ESPHome — VERIFIED upstream, S/28
- Source: https://github.com/esphome/esphome ; latest inspected stable [2026.10.0](https://github.com/esphome/esphome/releases/tag/2026.10.0), published 2026-10-21.
- Six factors: utility 5, working evidence 5, reusability 5, novelty 4, documentation 5, maintenance 4.
- Inspected README, LICENSE, pyproject.toml, `esphome/config.py`, `esphome/codegen.py`, `esphome/components/api/__init__.py`, `ota/__init__.py`, `safe_mode/__init__.py`, `mqtt/__init__.py` and `.github/workflows/ci.yml`. Verified integration-test files exist (e.g. `tests/integration/test_api_reboot_timeout.py`).
- PR #21626 upstream [CI run 40218426253](https://github.com/esphome/esphome/actions/runs/40218426253) on 2026-10-25: 30 jobs, 28 success and 2 skipped; included integration-test shards, C++ unit tests, ESP8266 and ESP32 build/component checks, static checks. No physical device verification.
- **Critical license split:** root LICENSE explicitly assigns GPLv3 to C/C++ runtime and MIT to Python and other parts; `pyproject.toml` metadata saying MIT must not override per-file/root split. Third-party dependencies and external components need separate checks.
- Python runtime requires >=3.12,<3.16. Device toolchains/flash hardware differ by target. Security: API Noise keys, OTA auth, safe-mode recovery, user-provided YAML/external components. Follow-up: simulate OTA interruption, inspect encrypted API lifecycle, compile representative boards and audit external component provenance.

## GNU Radio — VERIFIED upstream, S/27
- Source: https://github.com/gnuradio/gnuradio ; latest inspected stable [v3.10.12.0](https://github.com/gnuradio/gnuradio/releases/tag/v3.10.12.0) published 2025-02-20, active main October 2026.
- Six factors: utility 5, working evidence 5, reusability 5, novelty 4, documentation 4, maintenance 4.
- Inspected README, COPYING, CMakeLists.txt, `gnuradio-runtime/lib/top_block_impl.cc`, `gr-digital/lib/CMakeLists.txt`, `gr-filter/lib/CMakeLists.txt`, `gr-soapy/CMakeLists.txt`, `gr-soapy/docs/README.soapy`, `grc/core/FlowGraph.py`, `gr-utils/modtool/CMakeLists.txt`, OFDM QA tests and `.github/workflows/make-test.yml`.
- Upstream PR #8240 [Make Test 39263827649](https://github.com/gnuradio/gnuradio/actions/runs/39263827649) passed 10/10 jobs (2026-10-20) on Fedora/Ubuntu/Debian, 32-bit and clang; [Conda packaging 39263827623](https://github.com/gnuradio/gnuradio/actions/runs/39263827623) failed 2/2 jobs. Separate 2026-10-08 PR #8124 [Make Test 37622209718](https://github.com/gnuradio/gnuradio/actions/runs/37622209718) passed 11/11 after DVB-T heap-buffer-overflow fix. Upstream test evidence does not establish hardware RF correctness.
- GPL-3.0-or-later core; inspect driver and DSP dependencies separately. `gr-soapy` is a concrete bridge to SoapySDR; recorded reciprocal link without claiming hardware interoperability. `gnuradio/gnuradio4` is a separate C++23 next-generation project, not assumed a compatible replacement.
- Follow-up: investigate Conda packaging failures, sample-format/flowgraph regression vectors, fuzz packet/stream handling, compare GNU Radio 4 design and gr-soapy behavior.

## Maintenance and deferred research
- Improved existing SoapySDR cross-reference in both catalogs: explicitly identified GNU Radio's `gr-soapy` module, without changing SoapySDR evidence/score.
- Revisited existing Open MCT PROMISING/25 record and recent commits (last inspected 2026-10-07); no new passing e2e run was verified, so classification and prior failure caveat were preserved.
- No unverified release, CI, YouTube or hardware claim was promoted. No third-party code was copied.
