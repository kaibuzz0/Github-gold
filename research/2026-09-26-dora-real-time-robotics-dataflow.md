# dora-rs/dora — real-time robotics and AI dataflow runtime

- **Repository:** https://github.com/dora-rs/dora
- **Author / Org:** dora-rs
- **Category:** robotics / AI infrastructure / distributed dataflow / Rust / observability / ROS2 interoperability
- **Evidence:** VERIFIED
- **Provisional Gold score:** **S / 29**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- **License:** Apache-2.0
- **Discovery source:** GitHub-first independent discovery after rotating away from the AsTeRICS/FabiWare accessibility thread.

## What it is

Dora (Dataflow-Oriented Robotic Architecture) is a Rust-based runtime and toolchain for composing robotics and AI applications as directed dataflow graphs. Nodes can be implemented in Rust, Python, C, or C++, with Apache Arrow used as the common data representation. The project supports local and distributed execution, shared-memory and Zenoh transport, lifecycle management, fault recovery, observability, record/replay, dynamic topology, ROS2 interoperability, and a package-oriented Node Hub.

The repository describes dora 1.0 as released and provides installation through Cargo, PyPI, platform installer scripts, and source builds.

## Why it matters

Dora is valuable as both a whole robotics middleware stack and a source of reusable systems-engineering patterns. The particularly strong surfaces are:

1. **Dataflow runtime and typed graph model** — declarative YAML graphs, reusable/nested modules, typed ports and static validation.
2. **Transport abstraction** — local shared memory plus Zenoh-backed cross-machine communication, with network fallback behavior.
3. **Arrow-native multi-language boundary** — a common columnar representation across Rust/Python/C/C++ nodes reduces bespoke serialization glue.
4. **Operational lifecycle** — coordinator/daemon architecture, restart policies, health monitoring, cluster management and rolling upgrades.
5. **Record/replay and debugging** — `.drec` capture/replay, topic inspection, frequency measurement, graph visualization and trace inspection.
6. **Observability** — OpenTelemetry-oriented structured logs, metrics and tracing plus `dora top` resource monitoring.
7. **Dynamic topology** — node add/remove/connect/disconnect and runtime parameter management without restarting an entire dataflow.
8. **ROS2 interoperability** — topics/services/actions and QoS mapping provide a migration/interoperability path rather than requiring a completely isolated ecosystem.

## Concrete working evidence

### Stable release artifacts

GitHub's release API exposes stable **v1.0.1**, published **2026-09-03**, with packaged CLI and C-library artifacts for multiple operating systems/architectures. Release assets include SHA-256 digests. This is stronger evidence than README-only installation claims.

### CI and verification infrastructure

The repository has substantial GitHub Actions infrastructure rather than a token build badge. The inspected workflow directory includes dedicated CI, nightly, release, Python-package release, C/C++ library publishing/testing, schema regeneration, Docker image, and guide workflows. The primary `ci.yml` is a large workflow and the nightly workflow is also substantial, indicating broad automated verification surfaces.

### Current maintenance

The project is actively maintained. Multiple inspected commits from **2026-09-25** fix concrete distributed-runtime failure modes and include targeted tests/review follow-ups. Examples include:

- keeping Zenoh link probes responsive when endpoint exchange is disabled or delayed;
- preventing a stalled backpressure receiver from repeatedly throttling a producer;
- stopping daemon topic streams after slow/dead subscribers are evicted;
- resending potentially lost finish reports after coordinator-link failure;
- enforcing WebSocket connection caps for the actual socket lifetime and adding an integration test;
- delivering scheduler-buffered inputs correctly through the Stream API;
- correcting 32-bit parsing for log-size values;
- flushing node log files before reporting completion.

The commit messages are unusually useful evidence because they identify failure modes, expected invariants, and in several cases tests added specifically to reproduce or guard the corrected behavior.

## Useful components / patterns to mine

- coordinator + daemon lifecycle protocol
- local shared-memory / remote Zenoh transport split
- backpressure queue policy and stall handling
- Arrow-native message representation
- typed YAML dataflow validation
- reusable module/subgraph expansion
- node restart/health/circuit-breaker machinery
- `.drec` record/replay format and node substitution workflow
- topic debugging (`echo`, `hz`, `info`)
- resource-monitoring TUI and JSON snapshot mode
- OpenTelemetry trace capture/viewing
- runtime node/topology mutation
- ROS2 bridge and QoS mapping
- Node Hub package resolution and lockfiles
- cluster deployment/rolling-upgrade tooling
- soft-real-time CPU affinity / memory-locking support

## Runtime / platform requirements

The CLI is Rust/Cargo based. Python nodes use the `dora-rs` PyPI package (imported as `dora`) and PyArrow is used in documented Python examples. Source Python development uses maturin. C and C++ APIs are also supported. Distributed operation introduces Zenoh/network configuration, while ROS2 integration naturally adds ROS2/DDS or Zenoh-specific dependencies.

Upstream publishes platform installers and release artifacts for common Linux, macOS, and Windows targets; exact feature/platform compatibility should still be checked for a particular deployment.

## Licensing

The root project license is **Apache License 2.0**. Redistribution of covered code must preserve the license and applicable copyright/patent/trademark/attribution notices, and modified files need prominent modification notices as required by Apache-2.0. Dependencies and integrations such as Zenoh, Apache Arrow, ROS2 packages, Python packages, models, and Node Hub packages retain their own licenses.

No upstream source has been copied into GitHub Gold.

## Verification performed by GitHub Gold

Performed:

- inspected the upstream README and architecture/feature claims;
- inspected the root Apache-2.0 license;
- inspected the GitHub Actions workflow inventory;
- inspected the latest GitHub release metadata and packaged artifacts;
- inspected recent commit history through 2026-09-25, including detailed runtime fixes and test-oriented review follow-ups.

Not performed:

- did not compile Dora;
- did not execute its Rust/Python/C/C++ test suites;
- did not run a dataflow;
- did not reproduce the published performance comparisons;
- did not independently verify zero-copy behavior or latency/throughput claims;
- did not deploy a multi-machine cluster;
- did not test Zenoh network fallback;
- did not connect ROS2 hardware/software;
- did not exercise record/replay, hot reload, Node Hub, dynamic topology, or soft-real-time scheduling;
- did not perform a security audit or failure-injection campaign.

Therefore **VERIFIED** here means concrete upstream implementation/release/test/maintenance evidence was inspected; it does **not** mean GitHub Gold independently reproduced runtime behavior or benchmarks.

## Caveats / risks

- The README contains strong benchmark/performance claims; these remain upstream claims until independently reproduced on documented hardware and workloads.
- Distributed robotics middleware has a large failure surface: clocks, networking, queue pressure, process lifecycle, partial failures, and hardware timing can produce behavior not visible in unit tests.
- Some capabilities are explicitly still evolving; the README labels Node Hub unstable and notes that reclaiming running dataflows across coordinator restart is partial.
- Soft-real-time facilities are not equivalent to a hard real-time safety-certified runtime.
- Agent-assisted engineering is prominent in current development. This is not itself a defect, but makes strong review gates, regression tests, and reproducible evidence particularly important; recent commits show maintainers actively adding test/review follow-ups.

## Recursive ecosystem leads

1. **dora-rs/dora-hub** — inspect the package catalog, typed contracts, version resolution, provenance and package quality gates.
2. **Zenoh shared-memory integration** — isolate Dora's local/remote transport transition and failure-handling patterns.
3. **`.drec` record/replay subsystem** — potentially reusable for deterministic robotics regression testing and sensor-stream debugging.
4. **ROS2 bridge** — inspect Arrow conversion, QoS mapping, services/actions, and `rmw_zenoh_cpp` interoperability.
5. **Backpressure/fault-tolerance machinery** — recent fixes suggest a mature and technically interesting queue/lifecycle subsystem worth a component dossier if the implementation boundaries are clean.
6. **Ekumen-OS/andino-rs** — concrete low-cost robot integration using Dora dataflows and simulation; useful as independent ecosystem evidence rather than another middleware claim.

## Verdict

**VERIFIED — S / 29.** Dora meets the Gold quality bar on utility, reuse potential, documentation, release evidence, automated verification infrastructure, and very current maintenance. The strongest next research value is not another broad robotics framework comparison but a component-level inspection of Dora's record/replay or transport/backpressure subsystem, followed by an independent downstream integration such as `andino-rs` to test ecosystem reality.
