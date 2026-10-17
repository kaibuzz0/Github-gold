# Bagel — auditable robotics-data MCP + edge reduction pipelines

- **Repository:** https://github.com/Extelligence-ai/bagel
- **Author / Org:** Extelligence-ai
- **Category:** robotics data / ROS / drones / IoT / MCP / DuckDB / edge data reduction
- **Evidence:** VERIFIED
- **Provisional Gold score:** **S / 28**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 5/5
  - Maintenance: 3/5
- **License:** Apache-2.0 at repository root; review dependencies, container bases, models and external services separately before extraction or redistribution.
- **Discovery:** Independent GitHub-first breadth rotation after the bpftime observability pass.

## What it is

Bagel is an analysis and data-reduction layer for robotics, drone, automotive and IoT telemetry. It exposes data and workflows through MCP while keeping calculations auditable: repository documentation states that calculations over message data are expressed as DuckDB SQL and the generated query is shown rather than delegating numerical answers to an LLM.

The current format surface includes ROS1, ROS2, MCAP, PX4 ULog, ArduPilot, Betaflight, MQTT, PostgreSQL/TimescaleDB, InfluxDB 3, ASAM MDF4, CAN BLF/ASC+DBC and several ecosystem-specific inputs. It can run with cloud model clients or a local MCP-facing LLM.

## Why it matters

The highest-value design is the separation between natural-language intent and deterministic telemetry computation. The LLM is used as an interface/planner; the underlying numerical work is queryable/auditable SQL. That is a useful pattern for agentic scientific/robotics tooling where plausible-looking model arithmetic is unacceptable.

A second unusually useful surface is edge data reduction. Pipelines can identify events, retain windows around them, discard irrelevant intervals, and optionally upload selected output. The repository explicitly frames this as reducing robot/fleet telemetry before transport rather than putting an LLM in the robot control loop.

## Specific reusable components / patterns

- DuckDB-backed deterministic telemetry query layer.
- MCP server and capability-discovery surface for robotics-data analysis.
- ROS1/ROS2/MCAP/PX4/ArduPilot/Betaflight readers and normalization paths.
- Live MQTT/ROS sink architecture.
- Declarative edge pipelines with preview-before-write semantics.
- Event-window slicing and data-reduction workflow.
- Pipeline worker that moves expensive live pipeline work off the transport callback thread.
- Bounded pending queue, maximum-lag handling, drain semantics and failure isolation for live pipelines.
- Anomaly-screening and typed-decision gates, clearly marked upstream as beta.
- S3/GCS/Azure/MinIO/R2-oriented output/upload paths.
- Dockerized environment matrix for multiple ROS and drone ecosystems.
- Agent plugin/skills plus MCP integration for multiple clients.

## Evidence inspected

### README / operational surface

The default-branch README documents a runnable container demo using a bundled PX4 sample, Docker Compose services for ROS2 Kilted/Jazzy/Iron/Humble, ROS1 Noetic, PX4, ArduPilot, Betaflight and IoT, MCP setup, local-model operation, supported data formats, edge reduction, live sources and pipeline workflows.

The README is careful about at least one headline reduction example: its 1,200-second to 92-second / 2.1-GB to 161-MB example is explicitly described as illustrative demo output rather than a benchmark. That distinction improves evidence quality.

### Tests / CI

`.github/workflows/test.yaml` has a substantial validation matrix. It builds and runs pytest inside service images for ROS2 Kilted/Jazzy/Iron/Humble, ROS1 Noetic and Noetic-CV, PX4, ArduPilot, Betaflight, IoT and Apache Arrow. Separate host-side tests run on Python 3.10, 3.11 and 3.12 and include pipeline, sink, adversarial, automotive, database/source and agent/plugin paths. Coverage artifacts are combined and checked through a coverage gate; database tests and a final quality gate are also wired into the workflow.

This is upstream CI evidence, not a GitHub Gold execution of the suite.

### Recent maintenance and defect handling

The repository remained highly active through 2026-09-28. Recent history includes:

- live pipelines moved off transport callback threads into ordered workers, with queue/lag bounds, drain handling and tests for slow pipelines, failures and lifecycle edge cases;
- a real MQTT testing session exposed a singleton reinitialization bug in the documented list-then-subscribe flow, followed by regression tests and several concurrency/failed-init fixes;
- anomaly-screening work received repeated adversarial/Codex fixes for non-finite values, redirect credential forwarding, baseline behavior, dropout semantics, live-vs-recorded execution and model-score handling;
- arm64 support for the default ROS2 Kilted image was tested on a native arm64 runner before release.

This history is useful evidence because it records failures and corrections rather than only success claims.

### Release evidence

Stable **v2.4.1** was published **2026-09-28**. Upstream states that the default `ros2-kilted` image is now an amd64+arm64 manifest, while the other services remain amd64-only. The release notes say the native arm64 build had been exercised on the real GitHub arm runner before release. No standalone release assets are attached because the distribution path is container-oriented.

## Platforms / runtime

- Python 3.10+
- Docker / Docker Compose is the primary documented deployment path.
- Linux and Docker Desktop hosts; arm64 support varies by service.
- `ros2-kilted` is documented/published as native amd64 + arm64 in v2.4.1.
- Other service images are documented as amd64-only and need emulation on arm64 hosts; plain arm64 Linux needs QEMU/binfmt if using those images.
- GPU is optional for the beta local decision-model path.

## License / copying boundary

The root `LICENSE` is Apache License 2.0. No Bagel source is copied into Github-gold by this dossier. Before extracting implementation pieces, inspect component-specific notices, Python dependencies, Docker base images, ROS/PX4/ArduPilot ecosystem dependencies, model weights and external-service terms.

## Verification boundary

GitHub Gold inspected repository-native documentation, root licensing, test workflow, recent commit history and the v2.4.1 release metadata.

GitHub Gold **did not**:

- build or run Bagel;
- execute its pytest/coverage suite;
- start its Docker services;
- ingest a ROS/MCAP/PX4/ArduPilot/Betaflight log;
- connect an MCP client;
- run an MQTT/ROS live sink;
- reproduce edge-reduction outputs;
- upload data to cloud object storage;
- run the beta anomaly/decision model;
- verify the published container manifests independently;
- audit the complete security, dependency or model supply chain.

Accordingly, VERIFIED means there is concrete upstream implementation/test/release evidence for the cataloged functionality, not that Github-gold independently reproduced it.

## Caveats / risks

- The project is moving quickly; interfaces and pipeline semantics may change.
- The Jev/anomaly/decision surface is explicitly beta and upstream says detection quality is not yet established on known-incident reference logs.
- Some data-format support is marked beta.
- Local/offline operation depends on choosing a local model; MCP use with hosted models can send prompts/context outside the machine depending on configuration.
- Edge reduction is inherently lossy: a bad detector/pipeline can discard telemetry that later turns out to matter. Previewing, retaining raw data where feasible and validating event definitions are operationally important.
- Bagel belongs in the analysis/data plane, not a safety-critical robot control loop.

## Strong recursive leads

1. **PipelineWorker / live-sink lifecycle** — bounded queue, lag/drop policy, ordered execution, drain/replace behavior and callback-thread isolation.
2. **Deterministic query planner** — trace how natural-language requests become DuckDB SQL and what guardrails constrain generated queries.
3. **Cross-format normalization** — identify the common table/message abstraction spanning ROS, MCAP, PX4, ArduPilot, Betaflight and IoT sources.
4. **Edge windowing/reduction** — inspect preview semantics, merge behavior, checksums, upload idempotency and failure recovery.
5. **Anomaly screen** — useful engineering around rolling baselines, non-finite telemetry, dropouts and conservative fallback, but retain beta status until stronger reference-log evidence exists.
6. **CI reachability guard** — repository history documents a test-reachability mechanism intended to prevent test files from silently falling outside every CI execution path.
7. **Gantry Bench / Copper / WaffleForm integrations** — follow ecosystem links only if they survive independent quality and license review.

## Ranking rationale

Bagel reaches **28/30** because it combines a genuinely useful multi-format robotics analysis surface, an unusually auditable SQL-first agent architecture, edge reduction, broad composability and unusually strong current testing/maintenance evidence. Maintenance is held at 3/5 rather than 5 because the project is young and fast-moving, and some of its most novel anomaly/automotive surfaces remain beta. The score should be revisited after a longer operating history and independent execution of representative pipelines.
