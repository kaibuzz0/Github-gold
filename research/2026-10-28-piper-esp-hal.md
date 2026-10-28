# Piper and esp-hal — 2026-10-28 UTC

GitHub-first discovery in offline accessibility and embedded Rust. The six seed YouTube playlists previously lacked usable transcripts; no transcript attribution. No third-party code, model or firmware copied. No independent builds, speech generation, flashing, benchmarks or security audits.

## Piper — VERIFIED upstream / S27

**Upstream:** https://github.com/OHF-Voice/piper1-gpl . Inspected README, GPL-3.0 `COPYING`, `src/piper/voice.py` (ONNX synthesis and audio chunks), `src/piper/http_server.py` (Flask HTTP server), `libpiper/include/piper.h` (C ABI), `docs/STREAMING.md` (split encoder/decoder), `docs/API_PYTHON.md`, `docs/VOICES.md`, and `.github/workflows/test.yml`.

**Evidence:** [v1.8.0](https://github.com/OHF-Voice/piper1-gpl/releases/tag/v1.8.0) released 2026-09-04 with platform wheels. [v1.5.0 upstream publish workflow](https://github.com/OHF-Voice/piper1-gpl/actions/runs/29609618090) 2026-07-17 had 14 successful jobs (five wheel builds, five wheel tests, publication). **Predates** v1.8.0 and [2026-10-23 streaming merge](https://github.com/OHF-Voice/piper1-gpl/commit/74ac24e7e8e2e57a5e1fada5505c74e3d9c1843a). No current-head passing test confirmed.

**Licensing and risks:** GPL-3.0 source; each voice's MODEL_CARD is independent, potentially restrictive. [Model provenance question #340](https://github.com/OHF-Voice/piper1-gpl/issues/340) opened 2026-10-22. HTTP server defaults to `0.0.0.0:5000`; no authenticated exposure verified. README seeks maintainers. Related espeak-ng, ONNX Runtime, rhasspy/piper-voices, Home Assistant, NVDA (upstream mentions use, direct integration not verified).

**Next:** v1.8/current-head test evidence, voice licensing, stream latency and fidelity, HTTP network isolation.

## esp-hal — PROMISING / A25

**Upstream:** https://github.com/esp-rs/esp-hal . Inspected README, `esp-hal/Cargo.toml` (v1.2.0, Rust 1.95), MIT/Apache-2.0 license files, `esp-hal/src/lib.rs`, `esp-hal/src/gpio/mod.rs`, `esp-hal/src/i2c/master/mod.rs`, `esp-rtos/src/lib.rs`, `hil-test/README.md`, `examples/README.md`, `.github/workflows/ci.yml`.

**Evidence:** [esp-hal-v1.2.0](https://github.com/esp-rs/esp-hal/releases/tag/esp-hal-v1.2.0) released 2026-09-03; [2026-10-27 main commit](https://github.com/esp-rs/esp-hal/commit/5c0820cf9e2be0a49719bd71c30e7a45cae48134). [2026-09-10 merge-group CI](https://github.com/esp-rs/esp-hal/actions/runs/34454713435) 22 successful, 4 failed HIL and 3 skipped jobs; aggregator succeeded but hardware matrix **not fully green**. Several HIL targets did pass. No independent hardware testing.

**Reuse and risks:** Typed GPIO and I2C drivers, RTOS integration and chip-specific examples. Per-chip feature coverage varies; unstable APIs can break between minor versions. MIT OR Apache-2.0 source, third-party/radio firmware licenses separate. Companion esp-rs/esp-generate, esp-rs/espflash, esp-rs/esp-pacs, esp-rs/esp-idf (distinct stack), espressif/esptool (complementary host flasher), probe-rs.

**Next:** recent HIL failure logs and status, C6/S3 physical tests, toolchain reproducibility, firmware license review.

## Hygiene

Pre-edit PR #7 contained 122 entries. No candidate duplicates. Added esptool cross-reference without score change. Corrected one pre-existing master heading alias to match its canonical JSON name (`ESP32-S3 Remote ID Add-on`).
