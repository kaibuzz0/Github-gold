# Wasmtime and Zstandard — 2026-10-29 UTC

**Method:** Inspected the current draft PR #7, README, master list, 126-entry JSON catalog, candidate queue, audit script and branch head. Discoveries were GitHub-first; the six earlier YouTube playlist checks did not produce accessible transcripts. No third-party code, binaries or models copied. No independent build, Wasm execution, compression, fuzzing, hardware test or security audit.

## Wasmtime — VERIFIED (upstream) / S29

**Primary sources:** [README](https://github.com/bytecodealliance/wasmtime/blob/main/README.md), [Cargo.toml](https://github.com/bytecodealliance/wasmtime/blob/main/Cargo.toml), [LICENSE](https://github.com/bytecodealliance/wasmtime/blob/main/LICENSE), [SECURITY.md](https://github.com/bytecodealliance/wasmtime/blob/main/SECURITY.md).

**Exact reusable components:** [config.rs](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasmtime/src/config.rs) engine configuration; [store.rs](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasmtime/src/runtime/store.rs) Store and fuel; [limits.rs](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasmtime/src/runtime/limits.rs) ResourceLimiter; [component API](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasmtime/src/runtime/component/mod.rs); [WASI host](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasi/src/lib.rs); [wasi:http](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasi-http/src/lib.rs); [C API](https://github.com/bytecodealliance/wasmtime/tree/main/crates/c-api); [Cranelift](https://github.com/bytecodealliance/wasmtime/tree/main/cranelift); [Pulley](https://github.com/bytecodealliance/wasmtime/tree/main/pulley).

**Release and CI:** [v50.0.0](https://github.com/bytecodealliance/wasmtime/releases/tag/v50.0.0) released 2026-10-20. [2026-10-28 main merge-queue CI](https://github.com/bytecodealliance/wasmtime/actions/runs/40740727895) SHA `829c86c68659`: 190 passed, 3 skipped, 0 failed among 193 jobs (both job pages inspected). [2026-10-29 cargo audit](https://github.com/bytecodealliance/wasmtime/actions/runs/40792277264) passed. Separate release-48 CI success is not v50 release validation. These are upstream tests, not independent security assessment.

**Licensing:** Root LICENSE Apache-2.0, but root Cargo.toml specifies **Apache-2.0 WITH LLVM-exception**. Preserve exception and attribution and review dependencies.

**Risks and recursion:** Limit host-granted WASI preopens, network/HTTP access, host callbacks, resource limits and interruption. Follow [wasm-tools](https://github.com/bytecodealliance/wasm-tools), Cranelift, WIT and component-model examples. Review version-specific advisories before embedding untrusted modules.

## Zstandard — VERIFIED (upstream) / S28

**Canonical upstream:** [meta/zstd](https://github.com/meta/zstd). Former `facebook/zstd` path redirects to `meta/zstd`. [README](https://github.com/meta/zstd/blob/dev/README.md), [LICENSE](https://github.com/meta/zstd/blob/dev/LICENSE), [COPYING](https://github.com/meta/zstd/blob/dev/COPYING), [TESTING](https://github.com/meta/zstd/blob/dev/TESTING.md).

**Exact reusable components:** [lib/zstd.h](https://github.com/meta/zstd/blob/dev/lib/zstd.h) streaming C API; [lib/zdict.h](https://github.com/meta/zstd/blob/dev/lib/zdict.h) dictionary API; [zstdmt_compress.c](https://github.com/meta/zstd/blob/dev/lib/compress/zstdmt_compress.c) multithreaded compressor; [zstd_compress.c](https://github.com/meta/zstd/blob/dev/lib/compress/zstd_compress.c); [zstd_decompress.c](https://github.com/meta/zstd/blob/dev/lib/decompress/zstd_decompress.c); [fastcover.c](https://github.com/meta/zstd/blob/dev/lib/dictBuilder/fastcover.c). Frame format [RFC 8878](https://www.rfc-editor.org/rfc/rfc8878).

**Release and CI:** [v1.5.7](https://github.com/meta/zstd/releases/tag/v1.5.7) published 2025-02-19; dev SHA `49cf51799ea0` committed 2026-10-06. [2026-10-19 PR dev-long-tests](https://github.com/meta/zstd/actions/runs/39212353135) passed 30/30 jobs on different `macos14` branch; [2026-10-29 dev nightly regression](https://github.com/meta/zstd/actions/runs/40794889524) passed its one regression-test job on dev SHA. Recent dev push workflows with `action_required` status are not passing CI evidence. Green Pages deployment/Scorecards does not verify the codec. No independent codec run or performance test.

**Licensing:** BSD-style OR GPLv2 at user option, verified in root LICENSE/COPYING and [lib/zstd.h](https://github.com/meta/zstd/blob/dev/lib/zstd.h) source header. No source copied.

**Risks and recursion:** [libarchive's Zstandard filter](https://github.com/libarchive/libarchive/blob/master/libarchive/archive_read_support_filter_zstd.c) is a downstream integration; [FiniteStateEntropy](https://github.com/Cyan4973/FiniteStateEntropy) is a related entropy-coding lead with separate licensing. Limit decompressed output, RAM/CPU and dictionary trust for untrusted streams. Dev [lib/README](https://github.com/meta/zstd/blob/dev/lib/README.md) mentions future v1.6.0 legacy-decoder changes; not a stable v1.6.0 release.

## Maintenance

Existing libarchive cross-reference updated to canonical meta/zstd, with its VERIFIED/S28 rating unchanged. Two new catalog entries and matching master headings; no unrelated changes.
