# llama.cpp and jq — research batch (2026-10-26)

## Method and verification boundary
Inspected repository-native README, licenses, security notes, source/test trees, releases and CI jobs. VERIFIED means explicit **upstream** evidence; no independent build, installation, model execution, JSON parse, fuzz campaign, benchmark, hardware test or security audit. No third-party code, weights or assets copied. Two YouTube seed playlists (`PLMI6SBmd587c`, `PLfidXW0BixTc`) were directly requested 2026-10-26 and throttled. Other four not retried; no transcript claims.

## llama.cpp — VERIFIED / S 29
- **Repo:** https://github.com/ggml-org/llama.cpp
- **Score:** Utility 5, Working Evidence 5, Reusability 5, Novelty 5, Documentation 5, Maintenance 4.
- **Components:** [C API](https://github.com/ggml-org/llama.cpp/blob/master/include/llama.h), [GGUF loader](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-model-loader.cpp), [sampler](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-sampler.cpp), [grammar](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-grammar.cpp), [server](https://github.com/ggml-org/llama.cpp/tree/master/tools/server), [quantization](https://github.com/ggml-org/llama.cpp/tree/master/tools/quantize), [GGUF Python tools](https://github.com/ggml-org/llama.cpp/blob/master/gguf-py/README.md), [Android/Termux](https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md), [tests](https://github.com/ggml-org/llama.cpp/tree/master/tests).
- **Build:** CMake or release binaries; separately licensed GGUF models; RAM/VRAM dependent on quantization/context; optional CPU/GPU backends.
- **Release:** [b11907](https://github.com/ggml-org/llama.cpp/releases/tag/b11907), 2026-10-26, 36 artifacts; rolling prerelease, **not confirmed stable**.
- **Upstream CI:** [Server 40389494969](https://github.com/ggml-org/llama.cpp/actions/runs/40389494969) Windows/Ubuntu 2/2 success; [self-hosted Server 40379656923](https://github.com/ggml-org/llama.cpp/actions/runs/40379656923) CUDA/Metal/KleidiAI 3/3 success; [WASM 40389495039](https://github.com/ggml-org/llama.cpp/actions/runs/40389495039) success. Other PR runs marked action_required do not negate these passing runs.
- **License:** [MIT root](https://github.com/ggml-org/llama.cpp/blob/master/LICENSE), per-file and model license review required.
- **Risk:** [SECURITY.md](https://github.com/ggml-org/llama.cpp/blob/master/SECURITY.md) warns about untrusted models and untrusted-network exposure of server/RPC. No independent audit.
- **Ecosystem:** ggml-org/ggml, ggml-org/whisper.cpp (talk-llama example), model converters.
- **Next:** GGUF parser fuzzing, model-license provenance, local server network boundaries, Android memory profiling.

## jq — VERIFIED / S 28
- **Repo:** https://github.com/jqlang/jq
- **Score:** Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **Components:** [JSON parser](https://github.com/jqlang/jq/blob/master/src/jv_parse.c), [values](https://github.com/jqlang/jq/blob/master/src/jv.c), [compiler](https://github.com/jqlang/jq/blob/master/src/compile.c), [VM](https://github.com/jqlang/jq/blob/master/src/execute.c), [lexer](https://github.com/jqlang/jq/blob/master/src/lexer.l), [grammar](https://github.com/jqlang/jq/blob/master/src/parser.y), [builtins](https://github.com/jqlang/jq/blob/master/src/builtin.c), [fuzz harness](https://github.com/jqlang/jq/blob/master/tests/jq_fuzz_parse.c).
- **Build:** Standalone binaries, Docker or autotools; optional Oniguruma; `make check`.
- **Release:** [jq-1.8.2](https://github.com/jqlang/jq/releases/tag/jq-1.8.2), 2026-06-20, multiple CVE fixes including NUL parsing, memory safety, deep path handling and hash collision DoS.
- **Upstream CI:** [CI 40382053397](https://github.com/jqlang/jq/actions/runs/40382053397) 24 jobs passed (one release skipped), [Valgrind 40382053249](https://github.com/jqlang/jq/actions/runs/40382053249) passed, [BSD 40382053191](https://github.com/jqlang/jq/actions/runs/40382053191) FreeBSD/NetBSD passed. 2026-10-25 source commits show maintenance.
- **License:** [COPYING](https://github.com/jqlang/jq/blob/master/COPYING) includes MIT core, CC BY 3.0 docs, ICU decNumber, Lucent dtoa, Heimdal/NetBSD notices; review Oniguruma.
- **Risk:** Upstream fuzz harness exists, but no independent fuzzing; deploy security-patched versions when handling untrusted JSON.
- **Ecosystem:** Nushell is complementary, not an asserted dependency.
- **Next:** Parser/VM fuzzing, nested-input resource limits, regex dependency configuration and distro patch levels.

## Existing-entry maintenance
Updated whisper.cpp and Nushell cross-references in both catalogs, preserving scores. Open MCT remains PROMISING/A25: 2026-10-26 upstream e2e workflow still failed at npm ci (Node 18 vs required >=24.14.1); no passing Playwright execution established.
