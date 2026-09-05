# DuckDB-Wasm — In-browser analytical SQL engine and reusable WebAssembly data stack

- **Repository:** https://github.com/duckdb/duckdb-wasm
- **Author / Org:** DuckDB / Stichting DuckDB Foundation
- **Category:** browser analytics / WebAssembly / embedded database / local-first data processing / Arrow / Parquet / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **License:** MIT
- **Discovery:** Independent GitHub-first follow-up from the DuckDB core-engine dossier
- **Research date:** 2026-09-02

## Executive assessment

DuckDB-Wasm brings DuckDB's analytical SQL engine into browsers and JavaScript environments through WebAssembly. It is unusually valuable for GitHub Gold because it combines local analytical execution, direct Parquet/CSV/JSON access, Apache Arrow interoperability, a TypeScript API, worker-based browser integration, a Rust shell, React bindings, extension loading, and a documented browser compatibility surface in one repository.

The project is best understood as a reusable browser data-engine stack rather than merely a demo build of DuckDB. Its architecture makes it possible to move substantial analytical work from a remote server into the user's browser, which is relevant to local-first applications, offline-capable dashboards, privacy-sensitive analytical tools, static-site data explorers, scientific interfaces, data portals, education, and low-infrastructure deployments.

The main caveat is release cadence. The source tree remains active and was updated through 2026-07-28 during this pass, while the latest formal GitHub release returned by the API is v1.33.0 from 2025-12-16. The README, however, states that the current source is based on DuckDB v1.5.4, demonstrating that the repository has advanced materially beyond that GitHub release. This mismatch is recorded rather than ignored.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Enables substantial SQL analytics directly in browsers/Node with local and remote files. |
| Working Evidence | 5/5 | Large CI workflow, browser-targeted Wasm builds, TypeScript tests/tooling, examples, public shell and documented production package. |
| Reusability | 5/5 | TypeScript API, Wasm library, Arrow integration, worker model, React hooks, shell and extension interfaces. |
| Novelty | 4/5 | Browser databases exist, but the combination of DuckDB OLAP, Arrow, direct analytical formats and extension support is unusually capable. |
| Documentation | 5/5 | Clear README, API docs, examples, architecture/repository structure and differences from native DuckDB. |
| Maintenance | 4/5 | Source updated through 2026-07-28, but latest GitHub release observed is 2025-12-16 and release/version signaling is less current than the source tree. |
| **Total** | **28/30** | **S** |

## What it does

Upstream describes DuckDB-Wasm as DuckDB running in browsers through WebAssembly. The current README says it:

- works in browsers and Node.js;
- interoperates with Apache Arrow;
- reads Parquet, CSV and JSON;
- can source files through browser filesystem APIs or HTTP;
- has been tested with Chrome, Firefox and Safari;
- can load a growing subset of DuckDB core, community and external extensions;
- can open DuckDB database files;
- supports a browser SQL shell and visualizer ecosystem.

The current source README states that DuckDB-Wasm is based on DuckDB v1.5.4.

## Why it matters for GitHub Gold

### 1. Local-first analytical applications

A browser application can execute analytical SQL locally instead of shipping every query and dataset to an application server. This can reduce backend requirements and can keep some data-processing workflows on the user's machine.

This does **not** automatically make an application private or offline. Queries may fetch remote files or extensions, and the surrounding application may still transmit data. The useful architectural property is that the analytical engine itself can execute in the browser.

### 2. Static-site and low-infrastructure analytics

Because the engine executes client-side, developers can build data explorers and analytical interfaces that are hosted primarily as static web assets while querying local or remotely accessible analytical files.

This is especially interesting for:

- public data portals;
- offline/field research tools;
- interactive documentation;
- local data notebooks;
- scientific visualization frontends;
- personal analytics;
- educational SQL environments;
- privacy-sensitive data inspection where server upload is undesirable.

### 3. Direct analytical-file access

DuckDB-Wasm reads Parquet, CSV and JSON rather than requiring every dataset to be transformed into an application-specific browser database first.

Parquet is particularly valuable because analytical applications can transfer only the data needed by a query when the surrounding HTTP server and file layout allow efficient access patterns.

### 4. Apache Arrow interoperability

The project "speaks Arrow fluently" according to upstream. Arrow is a strong interoperability layer for moving columnar data between analytical engines, JavaScript visualization/data libraries and other tools without forcing everything through row-oriented JSON representations.

A future component-level pass should trace:

- Arrow result materialization;
- Arrow table/batch conversion;
- memory ownership/copying boundaries;
- streaming result paths;
- integration with browser visualization libraries.

## Repository architecture

The README identifies several distinct subprojects:

- `lib/` — C++ WebAssembly library layer;
- `packages/duckdb-wasm/` — TypeScript API package;
- `packages/duckdb-wasm-shell/` — Rust SQL shell;
- `packages/duckdb-wasm-app/` — web application / GitHub Pages surface;
- `packages/react-duckdb/` — React hooks/integration.

The TypeScript package also contains its own source tree, test tree, bundling scripts, coverage tooling, ESLint/Prettier/TypeScript configuration and browser-test infrastructure.

This modularity is a major reason to catalog the repository: useful implementation patterns can be studied independently rather than treating the project as one opaque Wasm binary.

## Browser execution model

DuckDB-Wasm's browser build is intentionally different from native DuckDB.

Upstream documents several key differences:

- the default HTTP stack is browser/JavaScript specific;
- network requests are constrained by browser security policy and CORS;
- HTTP is upgraded to HTTPS in the documented network path;
- Wasm builds are optimized for download size;
- extensions such as Parquet, JSON, ICU and autocomplete may be fetched/autoloaded at runtime instead of being permanently bundled;
- the default mode is single-threaded;
- multithreading exists but remains experimental;
- browser sandbox/filesystem constraints limit parity with native out-of-core and filesystem behavior.

These differences are operationally important and should not be collapsed into "DuckDB in a browser is identical to native DuckDB."

## Extension architecture

DuckDB-Wasm supports a growing subset of DuckDB extensions.

The README documents loading from:

- DuckDB core extension repositories;
- community extension repositories;
- explicit extension repository endpoints.

It also notes lazy extension installation behavior: fetching can be deferred until first `LOAD` rather than necessarily occurring at `INSTALL` time.

This is useful for reducing initial payload size, but it creates a network and supply-chain boundary. Applications that require deterministic offline behavior should not assume every extension is already embedded in the initial Wasm bundle.

Future research should verify:

- signature verification behavior in the Wasm loader;
- extension origin/repository trust decisions;
- cache persistence;
- offline pre-bundling options;
- failure behavior when extension endpoints are unavailable;
- whether community/external extension trust semantics differ from native DuckDB.

## HTTP and remote-file layer

The browser network stack is a particularly valuable research target.

Upstream explicitly notes that browser requests require the remote resource to permit cross-origin access. This makes CORS configuration a first-class operational constraint for static analytical applications.

A recent 2026-07-20 source commit corrected Authorization-header detection to use case-insensitive comparison, indicating that authentication/header handling remains an actively maintained part of the HTTP bridge.

Potential reusable components include:

- HTTP file registration;
- range-request handling;
- browser credential/header plumbing;
- remote database attachment;
- fetch scheduling;
- caching;
- error propagation across worker/Wasm boundaries.

## Worker and isolation pattern

The TypeScript/WebAssembly design is especially relevant for browser applications because heavy analytical work should not block the UI thread.

A future deep pass should map:

- worker startup and lifecycle;
- message protocol between main thread and database worker;
- query cancellation;
- result transfer;
- error serialization;
- file registration and Blob/File transfer;
- Wasm module selection;
- termination/recovery behavior.

The browser sandbox provides an important process-like containment layer compared with native DuckDB, but it should not be described as a complete security solution for every threat. The Wasm engine still consumes CPU/memory, can access resources exposed by the host page, and can make permitted network requests through its integration layer.

## Build system

Upstream documents the source workflow:

```text
git clone https://github.com/duckdb/duckdb-wasm.git
cd duckdb-wasm
git submodule init
git submodule update
make apply_patches
make serve
```

The repository tracks DuckDB through a submodule/patch integration model rather than duplicating the entire native engine as unrelated source.

The CI environment currently specifies Emscripten versions and builds multiple Wasm targets.

Observed jobs include:

- Clang-format checks for the C++ Wasm library;
- ESLint for TypeScript/Rust-adjacent package surfaces;
- TPC-H test-data generation;
- data-preparation tooling;
- `wasm_mvp` builds;
- `wasm_eh` builds;
- `wasm_coi` builds;
- artifact upload/download between jobs;
- browser/package build and testing stages elsewhere in the large workflow.

The workflow is more than 50 KB and should receive its own CI audit before GitHub Gold claims complete job coverage.

## Supply-chain observations

The CI is mixed in its action pinning.

Positive signal:

- the project-specific `duckdb/duckdb-wasm-ci-env` action is referenced by an immutable commit SHA in the inspected workflow.

Caveat:

- common third-party actions such as `actions/checkout@v6`, `actions/cache@v5`, `actions/upload-artifact@v7`, `mymindstorm/setup-emsdk@v14` and `hendrikmuhs/ccache-action@main` are referenced by version tags or a branch rather than all being pinned to immutable SHAs.

This does not imply compromise. It is simply a supply-chain-hardening observation worth preserving in the catalog.

## Working evidence

### Current source activity

The latest commits returned during this pass reach **2026-07-28**.

Recent examples include:

- fixing the DuckDB patch integration;
- updating toward DuckDB v1.5.5;
- avoiding duplicate publishing behavior;
- case-insensitive Authorization-header detection.

The README currently states the project is based on DuckDB v1.5.4, which is materially newer than the latest formal GitHub release metadata.

### GitHub release state

The latest non-prerelease GitHub release returned during this pass is:

- **v1.33.0**
- published **2025-12-16**
- release note says the release primarily corrected NPM publishing setup.

No GitHub release assets were attached to that release in the returned metadata.

Because the project is primarily distributed through NPM/web artifacts, GitHub Releases alone are not a complete distribution-health signal. This run did not query NPM package publication metadata through a package-registry API, so it does not claim what the latest NPM version is.

### CI / tests

The main GitHub Actions workflow is substantial and includes separate lint, build, data-generation and WebAssembly target jobs.

The TypeScript package contains:

- `test/`;
- Jasmine configuration;
- Karma browser-test infrastructure;
- coverage tooling;
- TypeScript configuration;
- lint/format configuration.

This is strong upstream working evidence, but GitHub Gold did not execute those tests.

## Supported environments

Documented/tested surfaces include:

- Chrome;
- Firefox;
- Safari;
- Node.js;
- browser WebAssembly;
- TypeScript/JavaScript applications;
- React integration;
- Rust-based shell tooling.

Exact browser-version compatibility should be verified against the deployed package version.

## Runtime and deployment requirements

Typical consumers need:

- a modern browser with WebAssembly support, or Node.js;
- JavaScript/TypeScript application integration;
- network/CORS configuration when reading remote files;
- sufficient browser memory for the target workload;
- cross-origin isolation and browser support where experimental multithreading is used.

Building from source additionally requires the repository's native/Wasm toolchain, submodules and Emscripten setup.

## Security and trust boundaries

### Browser sandbox

Compared with native DuckDB, WebAssembly executes within browser sandbox constraints and does not inherently receive arbitrary host filesystem access.

That is useful, but GitHub Gold should not overstate it. The surrounding JavaScript application determines which files, URLs, credentials and APIs are exposed to the engine.

### Network access

Remote data and extension loading can cause network traffic. CORS and HTTPS behavior are part of the security model, but an application must still control which origins and credentials are made available.

### Extension loading

Extensions add executable database functionality. Even in Wasm form, extension origin and integrity remain meaningful trust concerns. This run did not audit the extension verification implementation.

### Resource exhaustion

Analytical SQL can consume significant CPU and memory. Running in a browser moves that resource cost to the user's device; it does not eliminate denial-of-service or runaway-query concerns.

### Untrusted SQL

DuckDB core's general guidance treats SQL as executable behavior rather than a simple inert document format. The browser sandbox changes the host privilege boundary, but applications accepting arbitrary SQL should still enforce workload/resource policy and carefully control exposed files/network capabilities.

## Licensing

The root repository license is **MIT**, copyright Stichting DuckDB Foundation.

The license permits use, modification, redistribution, sublicensing and sale while requiring preservation of the copyright and permission notice in copies or substantial portions.

No DuckDB-Wasm source code was copied into GitHub Gold during this run.

Dependencies, DuckDB extensions and external/community extensions may carry separate licenses and should be reviewed individually before redistribution or extraction.

## Caveats and limitations

- Default execution is single-threaded; multithreading is documented as experimental.
- Browser memory and filesystem constraints differ materially from native DuckDB.
- CORS can prevent reading otherwise-public remote datasets.
- Network-backed extensions can undermine fully offline operation unless intentionally packaged/cached.
- Browser-side analytics still consumes local CPU/memory and can freeze or pressure constrained devices if workload control is poor.
- Current source is ahead of the latest GitHub release observed; deployment should use explicit package/version pinning rather than assuming GitHub Releases reflect current package state.
- Native DuckDB and DuckDB-Wasm are not feature-identical.
- Extension availability differs between native and Wasm targets.
- No independent performance claims are made here.

## Verification performed by GitHub Gold

Performed:

- inspected current upstream README;
- inspected repository architecture documented by upstream;
- inspected root MIT license;
- inspected current source commit history;
- inspected latest GitHub release metadata;
- inspected `.github/workflows/` inventory;
- inspected the large main CI workflow;
- inspected the TypeScript package structure and test/tooling surfaces;
- checked the existing GitHub Gold catalog/research branch for a prior `duckdb-wasm` entry before adding this dossier.

Not performed:

- no local clone/build;
- no `make apply_patches` execution;
- no Emscripten compilation;
- no browser test execution;
- no Jasmine/Karma test execution;
- no Node.js test execution;
- no SQL correctness testing;
- no Parquet/CSV/JSON workload test;
- no Arrow interoperability test;
- no offline-mode validation;
- no extension loading test;
- no multithreading test;
- no CORS/range-request test;
- no browser-memory benchmark;
- no NPM package-provenance verification;
- no security audit.

## Particularly valuable files / areas for follow-up

- `lib/` — C++ WebAssembly integration layer
- `packages/duckdb-wasm/src/` — TypeScript API and browser integration
- `packages/duckdb-wasm/test/` — package tests
- `packages/duckdb-wasm/karma/` — browser test setup
- `packages/react-duckdb/` — reusable React integration
- `packages/duckdb-wasm-shell/` — Rust shell implementation
- `.github/workflows/main.yml` — multi-target build/test/release architecture
- HTTP/file registration and range-request code
- worker/message protocol
- Wasm bundle selection logic
- extension-loader path
- Arrow conversion/result APIs

## Strong follow-up research

1. Trace the complete `AsyncDuckDB` worker lifecycle from bundle selection through instantiation, query execution and shutdown.
2. Map remote Parquet reads to HTTP range requests and identify how request coalescing/caching is handled.
3. Inspect extension integrity/signature verification and repository trust semantics in Wasm.
4. Compare MVP, exception-handling and cross-origin-isolated Wasm builds and their browser requirements.
5. Audit Arrow result transfer and copying behavior between Wasm memory, workers and JavaScript.
6. Inspect `react-duckdb` as a separately reusable frontend integration layer.
7. Verify current NPM release cadence/provenance in a later package-registry-focused pass.
8. Test whether a deterministic fully offline bundle can preload required extensions and datasets without runtime network dependencies.

## Verdict

**VERIFIED — provisional S / 28.**

DuckDB-Wasm is genuine GitHub Gold because it turns a serious analytical engine into a reusable browser-side infrastructure layer instead of merely compiling a CLI to WebAssembly. The strongest value lies in local-first analytics, direct analytical-file access, Arrow interoperability, worker-based browser execution and its modular TypeScript/Wasm integration surfaces. Its current source quality and CI justify VERIFIED status, while the mismatch between active source and older GitHub release metadata keeps Maintenance at 4/5 pending a dedicated NPM/distribution provenance pass.
