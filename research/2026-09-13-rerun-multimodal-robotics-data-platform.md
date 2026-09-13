# Rerun — Multimodal Robotics Data Platform

- **Repository:** https://github.com/rerun-io/rerun
- **Author / Org:** Rerun Technologies AB / rerun-io
- **Category:** robotics / physical AI / multimodal telemetry / visualization / columnar storage / query engine / data tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
- **Discovery:** GitHub-first breadth rotation into robotics and scientific/physical-AI data infrastructure; no YouTube-derived technical claim used.

## Why it matters

Rerun is an open-source data layer and visualization platform for multi-rate, multimodal data such as images, point clouds, transforms, time series, tensors, joint states and video. It is designed around robotics, computer vision, simulation and physical-AI workflows, but its underlying architecture is broader: a columnar Arrow-based data model, logging SDKs, a query layer, importers, an in-memory chunk store, a native/WebAssembly viewer, a renderer, protocol clients/servers and data transformation APIs.

For GitHub Gold, the strongest value is the combination of whole-product utility and reusable subcomponents. Rerun does not merely draw robot telemetry. The repository contains independently interesting storage, transport, query, rendering, importer, transform and SDK-generation pieces, with Python, Rust, C and C++ surfaces and explicit architecture documentation.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Directly useful for robotics, CV, simulation, multimodal debugging, dataset inspection and physical-AI data workflows. |
| Working evidence | 5 | Extensive Rust/Python testing infrastructure, protocol compliance tests, local server/client integration tests, Python end-to-end tests, snapshot/UI testing and active release artifacts. |
| Reusability | 5 | Dual MIT/Apache-2.0 licensing, modular Rust crates, Python/Rust/C/C++ SDK surfaces, Arrow-based storage and protocol/query components. |
| Novelty | 4 | Robotics visualization is not unique, but the unified log/query/store/viewer architecture and time-aware multimodal columnar model are technically distinctive. |
| Documentation | 5 | README, architecture, build, testing, release and SDK documentation are substantial and repository-native. |
| Maintenance | 5 | Stable v0.37.2 published 2026-09-11 and active development observed through 2026-09-12. |

## Repository-native evidence

The upstream README describes Rerun as a data layer for physical AI that can log, query, visualize and stream multimodal data. Documented data types and sources include images, point clouds, transforms, time series, joint states, tensors and video, including ingestion from robot logs, simulation, MCAP, RRD and LeRobot-style datasets.

The primary SDK surfaces are:

- Python SDK;
- Rust SDK;
- C SDK;
- C++ SDK;
- `rerun`/`rerun-cli` native viewer and command-line application;
- native and WebAssembly viewer deployments.

The architecture documentation states that logging SDKs encode data with Apache Arrow. Data can be written to `.rrd` files or transmitted over gRPC to a viewer or server. The viewer can run natively or in WebAssembly. The repository also contains a web-viewer server and a large set of modular Rust crates.

## Particularly valuable subcomponents

The generated architecture inventory exposes several unusually reusable areas.

### Store and data-flow layer

- `re_chunk` — Arrow-encoded Rerun data chunk used across logging, transport, storage and compute;
- `re_chunk_optimizer` — analysis and memory-bounded chunk-layout optimization;
- `re_chunk_store` — storage engine for Rerun chunks;
- `re_dataframe` / `re_datafusion` / `re_query` — query APIs and DataFusion-related query infrastructure;
- `re_entity_db` — in-memory storage for Rerun entities;
- `re_importer` — importer plugin surface;
- `re_hdf5` — HDF5-to-chunk loading;
- `re_lerobot` — LeRobot dataset ingestion;
- `re_mcap` — MCAP conversion into Rerun-compatible data;
- `re_mp4_reader` — MP4-to-chunk loading;
- `re_parquet` — Parquet-to-chunk loading;
- `re_log_encoding` — RRD stream encode/decode and serialization;
- `re_protos` — remote gRPC/protobuf API types;
- `re_redap_client` — client for the Rerun Data Protocol;
- `re_server` — open-source server implementation backed by an in-memory store;
- `re_sorbet` — Arrow metadata definitions;
- `re_tf` — spatial transform processing;
- `re_uri` — Rerun URI parsing/construction;
- `re_lenses` / `re_lenses_core` — data extraction, transformation and restructuring primitives.

### Viewer and renderer layer

- `re_renderer` — wgpu-based rendering layer used by the viewer;
- `re_view_spatial` — 2D/3D spatial visualization;
- `re_view_time_series` — timeline-based plotting;
- `re_view_tensor` — arbitrary-dimensional tensor visualization;
- `re_view_dataframe` — tabular/dataframe view;
- `re_view_map` — map view;
- `re_view_graph` — node-link graph view;
- `re_time_panel` / `re_time_ruler` — temporal navigation UI;
- `re_memory_view` — flamegraph-style memory visualization;
- `re_dataframe_ui` — rich DataFusion-backed table widget;
- `re_viewer_mcp` — MCP server allowing LLM agents to interact with the viewer;
- `re_agent_ui` — agent-driving chat UI using the Agent Client Protocol.

### SDK/build infrastructure

- `re_sdk` — logging SDK layer;
- `rerun_py` — Python SDK;
- `rerun_c` — C SDK;
- `rerun` — Rust SDK;
- `re_type_definitions` and `re_types_builder` — schema/type-definition and code-generation infrastructure for SDKs;
- `re_protos_builder` — protobuf/gRPC code generation;
- `re_web_viewer_server` — small HTTP host for the WebAssembly viewer.

These are stronger GitHub Gold targets than treating the repository as one monolithic application.

## Storage and transport architecture

Rerun uses Apache Arrow as the shared columnar representation for logging, network transmission and the in-memory data store. Upstream describes `.rrd` files as append-oriented sequences of log messages. Current architecture documentation explicitly warns that `.rrd` is not guaranteed to have full long-term forward/backward compatibility; the current release guarantees compatibility with files from the immediately previous release, not arbitrary historical versions.

Data can move through several paths:

- SDK -> `.rrd` file;
- SDK -> viewer over gRPC;
- SDK/client -> Rerun server;
- imported MCAP/HDF5/Parquet/MP4/LeRobot-style data -> Rerun chunks;
- chunk store/query APIs -> dataframe/SQL-style analysis and visualization;
- native or browser viewer -> synchronized multimodal inspection.

This architecture makes the repository relevant not only to visualization but also telemetry ingestion, compact structured logging, robotics data interoperability and local analytical tooling.

## Working evidence

The repository's testing documentation describes multiple independent layers:

- Rust unit tests using the standard test framework and `cargo nextest`;
- feature-matrix testing in CI;
- `insta` snapshot testing;
- UI snapshot tests using `egui_kittest`;
- Python unit tests using `pytest` and `syrupy` snapshots;
- `re_redap_tests`, a Rust compliance suite for the Rerun Data Protocol service handlers;
- `re_integration_test`, which launches an open-source local server and connects the Rust client to it;
- Python `e2e_redap_tests`, which use the Python SDK against a running server.

Additional repository-native test evidence observed in source search includes:

- backward-compatibility tests that open previous-release `.rrd` recordings in the current viewer;
- importer tests for LeRobot datasets;
- end-to-end PLY importer tests using a real 3D Gaussian Splatting reconstruction fixture;
- HDF5 importer fixtures with corresponding Rust integration coverage;
- web/browser integration testing;
- memory-overhead tests for the chunk store;
- rendering smoke/comparison utilities.

This is strong upstream working evidence. GitHub Gold did not independently execute those tests during this run.

## Release and maintenance evidence

The latest stable GitHub release inspected was **0.37.2**, published **2026-09-11**. The release includes platform-specific artifacts such as the native Rerun CLI/viewer and static C libraries, and GitHub exposes SHA-256 digest metadata for inspected release assets.

Development remained active after that release. Commits inspected through **2026-09-12** included architecture/dependency-layer enforcement, deterministic generation of the crate-dependency diagram and timeline navigation behavior changes. The architecture document states that the crate dependency graph and crate tables are generated from Cargo metadata and checked in CI, with a script enforcing downward dependency layering between crate groups.

The README explicitly states that the project is under active development and warns users to expect API changes. This is an important maintenance strength and compatibility caveat at the same time.

## Platforms / requirements

Rerun is built primarily in Rust with SDK and integration surfaces in Python, C and C++.

Upstream documents:

- Python installation via `pip install rerun-sdk`;
- Rust installation through crates.io/Cargo;
- C++ SDK usage with a separately installed viewer;
- native viewer operation;
- WebAssembly/browser viewer builds;
- gRPC streaming to viewers/servers;
- optional NASM support for improved video decoding performance when building the CLI with the relevant feature.

Exact platform support varies by SDK, viewer build and optional feature set. Release assets and build infrastructure should be inspected before claiming support for a specific deployment target.

## Licensing

The repository exposes both:

- **MIT License**;
- **Apache License 2.0**.

This dual permissive model is favorable for study and component reuse, subject to the selected license's attribution/notice requirements and any third-party dependency obligations.

The README also describes an **open-core business model**: the code in this repository is intended to remain open source, while Rerun Hub is a separate commercial product. Cataloging this repository should not imply that every Rerun-branded service or hosted/server capability outside this repository is covered by the same open-source scope.

No upstream source code, binaries, datasets, release artifacts or third-party assets were copied into GitHub Gold during this run.

## Verification performed

GitHub Gold inspected:

- current upstream README;
- MIT license;
- Apache-2.0 license;
- architecture documentation;
- testing documentation;
- workflow inventory;
- repository source/test search results;
- latest stable GitHub release metadata;
- recent commit history through 2026-09-12;
- current GitHub Gold branch and open research PR;
- existing GitHub Gold repository search for duplicate `rerun-io/rerun` entries.

**Not performed:** GitHub Gold did not compile or run Rerun, execute Rust/Python tests, launch the viewer, ingest real robotics data, benchmark the chunk store/query engine, validate renderer performance, run the WebAssembly viewer, verify `.rrd` compatibility independently, connect a live gRPC client/server pair, reproduce release binaries or independently validate release hashes.

Claims above are therefore based on repository-native upstream evidence, not independent execution by GitHub Gold.

## Caveats / risks

- The project explicitly warns that APIs are evolving and breaking changes should be expected.
- `.rrd` compatibility is intentionally limited; current upstream documentation only guarantees the current release can open data generated by the previous release.
- Large entity counts and multi-million-point clouds are documented performance limitations.
- Rerun spans a large Rust workspace and multiple SDK/toolchains; source builds are significantly heavier than single-purpose visualization libraries.
- Browser/Wasm builds have different filesystem, threading and networking constraints than native builds.
- The open-source repository and commercial Rerun Hub should be treated as separate licensing/deployment surfaces.
- Dependency licenses, imported data licenses and model/dataset licenses remain independent of Rerun's own dual license.
- High-level working evidence does not prove correctness of every importer, backend, renderer path or query combination.

## Related ecosystem

- Apache Arrow — shared columnar data representation;
- DataFusion — query/dataframe-related ecosystem dependency;
- `wgpu` — cross-platform GPU abstraction used by the renderer;
- `egui` / `eframe` — immediate-mode native/Web UI framework;
- MCAP — robotics telemetry container format already cataloged separately by GitHub Gold;
- LeRobot — robotics dataset ecosystem supported by import tooling;
- gRPC / protobuf — remote Rerun Data Protocol transport;
- HDF5 / Parquet / MP4 import paths.

## Follow-up research

1. Deep-map `re_chunk`, `re_chunk_store` and `re_chunk_optimizer`, including memory layout, indexing, eviction and compaction behavior.
2. Inspect the Rerun Data Protocol (`redap`) and its protocol compliance tests, including version negotiation and compatibility guarantees.
3. Trace `.rrd` encoding, corruption handling, stream framing and backward-compatibility boundaries.
4. Evaluate `re_mcap`, `re_hdf5`, `re_parquet`, `re_lerobot` and importer plugins as independent interoperability components.
5. Inspect `re_dataframe`, DataFusion integration and SQL/query execution for reusable analytical patterns.
6. Map `re_renderer` architecture and determine which primitives are reusable independently of the full viewer.
7. Study spatial-transform handling in `re_tf`, especially multi-frame robotics coordinate systems.
8. Review WebAssembly viewer constraints and local/offline deployment patterns.
9. Inspect `re_viewer_mcp` and `re_agent_ui` as emerging agent-to-visualization interfaces.
10. Compare Rerun's data model and workflow with Foxglove/MCAP, RViz/ROS tooling and generic Arrow/Parquet telemetry pipelines.
