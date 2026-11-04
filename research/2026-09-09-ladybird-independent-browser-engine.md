# Ladybird — independent browser engine and multi-process web platform

- **Repository:** https://github.com/LadybirdBrowser/ladybird
- **Organization:** LadybirdBrowser
- **Category:** Browser engines / web platform / systems software / sandboxed multi-process applications
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **26/30 — S tier**
  - Utility: 4/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 4/5
- **Primary language:** C++
- **License:** BSD-2-Clause
- **Discovery source:** GitHub-first category rotation after the Android/Termux research batch
- **Inspection date:** 2026-09-09

## Executive finding

Ladybird is an unusually ambitious independent browser implementation rather than another Chromium/WebKit shell. The project is still explicitly **pre-alpha** and upstream says it is suitable only for developers, so this dossier does not treat it as a production-ready daily browser. It nevertheless qualifies as GitHub Gold because the repository contains a broad, actively developed web-platform implementation with concrete architecture, deep standards-oriented subsystems, large test/CI surfaces, sanitizers/fuzzing, and multiple reusable engine/library components.

The main technical value is not merely the finished browser executable. The repository contains an ecosystem of reusable or research-worthy components including a web rendering engine, JavaScript engine, WebAssembly implementation, Unicode and locale support, graphics/image decoding, media, IPC, HTTP, crypto/TLS, OS abstraction/event-loop infrastructure, parsers, layout/style machinery, test harnesses, and fuzzing targets.

## What upstream says it is

The project describes Ladybird as a truly independent browser using a novel engine based on web standards. The README explicitly marks the browser **pre-alpha** and says it is currently suitable only for developers.

The documented architecture is multi-process:

- a main UI process;
- multiple `WebContent` renderer processes;
- a separate `ImageDecoder` process;
- a separate `RequestServer` process;
- one renderer process per tab;
- renderer sandboxing from the rest of the system;
- image decoding and network connections moved out of process for robustness against malicious content.

This architecture is one reason the project is more valuable than a monolithic browser experiment: process boundaries, IPC, sandboxing, parser behavior, rendering, networking, and decoding can be studied as separate systems.

## High-value internal components

The README identifies the current core support libraries, many inherited historically from SerenityOS and now developed in the Ladybird repository:

### `LibWeb`

Web rendering and web-platform implementation. This is the highest-value research surface in the repository. Recent upstream commits show active work in selection styling, caret geometry, editing behavior, layout invalidation, CSS observability, and visual/regression coverage.

### `LibJS`

JavaScript engine. The repository contains dedicated conformance and benchmark infrastructure, including a Test262 workflow and JavaScript benchmark workflows.

### `LibWasm`

WebAssembly implementation. This is independently useful as a runtime/parser/execution research target and shares artifact/benchmark infrastructure with the JS engine.

### `LibCrypto` / `LibTLS`

Cryptographic primitives and TLS support. These should be treated cautiously for reuse because cryptographic code needs focused security review even when the project-level license is permissive.

### `LibHTTP`

HTTP/1.1 client implementation and related protocol code.

### `LibGfx`

2D graphics, image decoding, and rendering infrastructure.

### `LibUnicode`

Unicode and locale handling. This is a potentially valuable reusable subsystem because modern browser engines require extensive Unicode normalization, segmentation, locale, text-direction, and character-property behavior.

### `LibMedia`

Audio/video playback support.

### `LibCore`

Event-loop and operating-system abstraction infrastructure.

### `LibIPC`

Inter-process communication infrastructure supporting the browser's multi-process design.

## Working evidence

Ladybird has unusually strong repository-native working evidence for a pre-alpha project.

### CI matrix

The inspected `.github/workflows/ci.yml` runs on pushes to `master` and pull requests. The matrix includes:

- Linux x86_64 Release with GNU;
- Linux x86_64 Sanitizer with Clang and Clang plugins;
- macOS arm64 Sanitizer with Clang;
- Linux arm64 Sanitizer with Clang;
- Linux x86_64 Fuzzers with Clang;
- Linux x86_64 All_Debug with Clang;
- Windows x86_64 Sanitizer with ClangCL.

The Linux jobs use an explicitly versioned Ladybird CI container image (`ghcr.io/ladybirdbrowser/ladybird-ci:2026.08.28` at inspection time).

### Dedicated workflows

The workflow tree contains separate automation for at least:

- core CI;
- CI image construction;
- development containers;
- Flatpak builds;
- JavaScript and WebAssembly artifacts;
- JavaScript/WebAssembly benchmarks;
- Test262 JavaScript conformance work;
- code linting;
- commit linting;
- nightly Android work;
- nightly Lagom/library work;
- merge-conflict labeling and additional maintenance tasks.

### Current successful automation

A repository Actions query on 2026-09-09 showed recent workflow runs on the then-current master head. The inspected JavaScript benchmark run for commit `d0895b4dab6266f021f77463a1f3a4adaf2af341` completed successfully. This is upstream CI evidence, not a locally reproduced benchmark.

### Regression-oriented commits

The newest inspected commits on 2026-09-09 included concrete bugfixes with explicit regression or visual-test coverage. Examples included:

- limiting `::selection` style updates to the selected region while preserving required repaint and CSSOM behavior;
- sizing empty editable-element carets from font metrics rather than full line-height boxes;
- resolving parent/text-node boundary carets from text fragment geometry;
- preventing temporary editing selections from unnecessarily activating selection styles across the document.

These commit descriptions explicitly mention geometry tests, visual tests, regression cases, local invalidation coverage, RTL/vertical text, focus changes, insertion behavior, and layout/repaint distinctions. This is materially stronger evidence than README claims alone.

## Build and runtime requirements

The inspected build documentation is substantial and current.

Baseline requirements include:

- Qt 6.9+ development packages for the Qt frontend;
- NASM and platform build tools;
- a C++23-capable compiler;
- Rust toolchain;
- CMake 3.30+;
- Ninja and other platform dependencies.

The documentation states current CI uses gcc-14 and clang-21 and points developers to `Meta/Utils/find_compiler.py` for minimum compatible compiler versions.

Documented build environments include Debian/Ubuntu, Arch/Manjaro, Fedora, openSUSE, Void Linux, Nix, macOS, Windows through WSL2, experimental native Windows/Clang-CL, Android, and FreeBSD.

The primary developer entry point is `Meta/ladybird.py`, with examples for:

- building/running the browser;
- running under gdb;
- selecting Debug builds;
- running JS or WebAssembly REPL executables;
- choosing UI frameworks;
- controlling custom CMake build directories;
- limiting parallel linker jobs for low-memory systems.

## UI/platform architecture

The build documentation identifies multiple frontends:

- AppKit on macOS;
- Qt on other desktop platforms;
- native Android UI on Android.

Windows is supported primarily through WSL2; native Windows remains experimental with limited functionality. MinGW/MSYS2 is explicitly unsupported in the inspected documentation.

## Reusability assessment

The project is highly reusable for research, but individual components are not necessarily packaged as drop-in standalone libraries. Reuse potential is strongest in:

- parser and standards implementation patterns;
- JavaScript/WebAssembly runtime internals;
- Unicode/locale machinery;
- image/graphics code;
- IPC architecture;
- process isolation design;
- testing/fuzzing infrastructure;
- browser regression tests;
- build orchestration through `Meta/ladybird.py`;
- cross-platform CMake/toolchain patterns.

Any extraction should preserve attribution and verify file-level third-party notices before copying because browser engines routinely vendor or integrate third-party sources even when the repository's root license is permissive.

## License

The root repository uses the **BSD 2-Clause License**. The inspected LICENSE permits redistribution and modification in source or binary form provided the copyright notice, conditions, and disclaimer are preserved as required.

No Ladybird source code was copied into GitHub Gold during this research pass.

## Maintenance signals

Maintenance is extremely active at inspection time:

- repository push activity occurred on 2026-09-09;
- multiple substantive `LibWeb` commits landed on 2026-09-09;
- recent CI/benchmark workflows completed on those commits;
- the repository maintains a large collection of specialized workflows;
- build documentation tracks current compiler/toolchain requirements rather than stale historical versions.

The 4/5 Maintenance score instead of 5/5 reflects the project's explicit pre-alpha status and the fact that rapid architecture churn can make APIs and internal components unstable for downstream consumers.

## Gold score rationale

### Utility — 4/5

Extremely valuable for browser-engine, standards, parser, layout, JS/Wasm, IPC, sandboxing, graphics, networking, and systems research. Lower than 5 because upstream explicitly says it is not yet appropriate as a general-user browser.

### Working Evidence — 5/5

Strong multi-platform CI, sanitizer builds, fuzzing configuration, conformance/benchmark workflows, active regression testing, visual tests, and successful current automation.

### Reusability — 4/5

Many valuable libraries and implementation patterns, permissive root license, and modular architecture. Reduced because internal APIs are evolving rapidly and many pieces are tightly integrated into a browser engine.

### Novelty — 5/5

A genuinely independent modern browser engine is rare. The project is not simply a UI around Chromium, WebKit, or Gecko.

### Documentation — 4/5

README, extensive build documentation, contributor documentation, issue policy, and code-oriented documentation are present. A point is withheld because the project remains developer-focused/pre-alpha and not every subsystem is necessarily documented as a standalone reusable component.

### Maintenance — 4/5

Very active current development and automation. One point withheld for pre-alpha churn and API instability rather than inactivity.

## Important caveats

1. **Pre-alpha:** upstream explicitly warns that Ladybird is currently suitable only for developers.
2. **Not independently built in this run:** GitHub Gold did not compile or launch Ladybird.
3. **No independent conformance measurement:** Test262/web-platform correctness percentages were not independently calculated.
4. **No sandbox penetration test:** process isolation and sandboxing were identified from architecture and source/workflow evidence but were not security-tested here.
5. **No cryptographic validation:** `LibCrypto`/`LibTLS` were not audited for security or standards compliance.
6. **Rapidly changing internals:** reusable APIs may change substantially before stable releases.
7. **Large dependency/toolchain footprint:** C++23, Qt 6.9+, Rust, modern CMake, vcpkg/build dependencies, and large builds make it unsuitable for lightweight environments.
8. **Cross-platform support is uneven:** WSL2 is the primary Windows route; native Windows remains experimental.

## Verification performed by GitHub Gold

This dossier inspected upstream repository-native evidence including:

- repository metadata and current maintenance timestamps;
- README architecture/features/license statements;
- root LICENSE;
- core CI matrix;
- workflow inventory;
- build instructions and documented platform/toolchain requirements;
- recent commits;
- recent GitHub Actions status.

GitHub Gold did **not**:

- clone the repository;
- compile Ladybird;
- run the browser;
- execute Test262 or WPT locally;
- run benchmarks locally;
- run fuzzers locally;
- validate renderer sandbox escape resistance;
- inspect every dependency or third-party license;
- independently validate TLS/crypto behavior;
- test Android, Windows, macOS, Linux, or FreeBSD builds on hardware.

All working claims in this dossier are therefore either direct source/architecture observations or explicit upstream CI/test evidence, not claims of local execution.

## Related ecosystem leads

Strong recursive research targets:

1. **LibWeb architecture** — style calculation, DOM bindings, layout, painting, editing, accessibility tree, networking hooks, and WPT integration.
2. **LibJS + Test262** — conformance runner, bytecode/interpreter/JIT direction if present, parser architecture, GC, and temporal/internationalization support.
3. **LibWasm** — parser, validator, interpreter/compiler pipeline, WASI relationship, and benchmark infrastructure.
4. **LibIPC** — message generation, serialization, descriptor passing, process lifetime, backpressure, and trust boundaries.
5. **Renderer sandbox** — OS-specific implementation, syscall/filesystem/network restrictions, and brokered capabilities.
6. **RequestServer** — HTTP/TLS/network process boundaries, proxy/cookie/cache behavior, and attack surface.
7. **ImageDecoder process** — codec isolation, malformed-image fuzzing, and decoder crash containment.
8. **Web-platform test infrastructure** — how WPT imports, expectations, rebaselines, and visual regression testing are managed.
9. **Android frontend/nightly pipeline** — maturity, architecture, packaging, and feature parity.
10. **SerenityOS lineage** — identify which libraries have diverged enough to treat the Ladybird versions as independent implementations and where upstream/downstream code relationships still matter.

## Next-action recommendation

Keep Ladybird at **VERIFIED / provisional S 26** rather than promoting it as a production browser. The next highest-value pass is a focused `LibWeb`/sandbox dossier that distinguishes concrete implementation depth from project-level ambition and identifies exact reusable engine components without copying source.