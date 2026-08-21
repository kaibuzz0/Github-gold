# Research Dossier — Embedded Analytics

Date: 2026-08-20

## DuckDB

- **Repository:** https://github.com/duckdb/duckdb
- **Author / Org:** DuckDB
- **Category:** embedded analytics / SQL / data tooling / columnar processing
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 29
- **License:** MIT
- **Code copied into GitHub Gold:** No

### What it does

DuckDB is an embeddable analytical SQL database designed for local and in-process analytics. Upstream documents a standalone CLI plus client integrations for Python, R, Java, Wasm, and other environments. CSV and Parquet files can be queried directly through SQL without a separate import step.

### Why it is valuable

DuckDB is useful as a reusable analytical engine rather than only as an end-user application. It can be embedded into larger tools that need local SQL, columnar analytics, data transformation, file inspection, or lightweight analytical workflows without deploying a separate database server.

### Useful code / components

- Embeddable analytical SQL engine
- Public C API in `src/include/duckdb.h`
- Version-targeted C API surface and extension ABI macros
- CLI application
- CSV and Parquet readers
- Query planner and optimizer
- Vectorized execution engine
- Storage and transaction layers
- Extension architecture
- Python, R, Java, Wasm, and other client bindings/ecosystem integration points
- Unit-test and benchmark infrastructure

### Install / runtime / build evidence

The upstream README documents a CMake/Python/C++17 development toolchain. It provides `make`, `make debug`, `make unit`, and `make allunit` development paths and standard benchmark tooling. GitHub Gold did not independently compile or benchmark DuckDB during this pass.

### Maintenance evidence

Recent upstream commits on 2026-08-20 included:

- restoration of static-link behavior for C API extensions after a regression
- qualified-name fixes for nested schemas
- ARM64 portability hardening with new unit tests and upstream benchmark measurements
- identifier-case compatibility and behavior fixes

This is strong evidence of active maintenance across API compatibility, portability, correctness, and extension use cases.

### License / reuse

The repository root `LICENSE` is MIT and permits use, modification, redistribution, sublicensing, and sale while requiring preservation of the copyright and permission notice. Third-party dependencies and separately distributed extensions should still be checked individually before extraction or redistribution.

### Verification boundary

GitHub Gold inspected repository metadata, the upstream README, the root MIT license, the generated public C API header, and recent upstream commits. GitHub Gold did **not** independently build, benchmark, execute, or fuzz DuckDB in this pass.

### Caveats

- The repository is large and rapidly changing; extension ABI/API consumers need to target documented compatibility surfaces rather than private internals.
- Optional extensions and external dependencies may have licenses different from the MIT root project.
- High Gold score reflects inspected upstream engineering evidence, not an independent performance benchmark by GitHub Gold.

### Discovery provenance

GitHub-first discovery during the 2026-08-20 broad data-tooling research pass.

### Follow-up leads

- DuckDB extension SDK and extension templates
- Parquet subsystem and vectorized scan architecture
- Arrow interoperability
- Wasm client architecture
- MotherDuck ecosystem boundaries versus core OSS
- reusable C API patterns for embedding into Android/Termux/local-first tools
