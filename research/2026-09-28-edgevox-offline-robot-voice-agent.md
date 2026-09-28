# EdgeVox — offline voice-agent framework for robotics

- Upstream: https://github.com/nrl-ai/edgevox
- Author/org: Neural Research Lab (`nrl-ai`), Viet-Anh Nguyen
- Category: robotics / offline AI / voice / ROS 2 / simulation / agent frameworks
- Evidence: **VERIFIED** (repository-native source/tests plus upstream recorded local runs; GitHub Gold did not execute the software)
- Provisional Gold score: **28/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 5/5
  - Documentation 5/5
  - Maintenance 3/5
- License: **Apache-2.0** at repository root. Note: README text surfaced by search may contain stale license wording, so the root `LICENSE` is treated as authoritative.

## Why it matters

EdgeVox is an unusually broad but componentized local/offline robotics stack: a streaming STT→LLM→TTS voice substrate, cancellable agent skills, workflow primitives, simulation adapters, and ROS 2 integration. The most reusable design is its separation of a reactive safety/preemption path from the LLM path: stop words become a dedicated `StopFrame`, and cancellation does not require an LLM round trip.

The repository is also useful as an evidence-oriented reference for small-model agent reliability. Upstream commits record both successes and failures rather than only demos: deterministic scripted harnesses cover workflow/robot behavior, while recorded local Gemma runs expose tool-routing and multi-step-plan failure modes.

## Concrete reusable surfaces

- `edgevox/core/processors.py` — `SafetyMonitor` between transcription and LLM processing; recognizes stop words and emits the hard-stop path.
- `edgevox/core/frames.py` — dedicated `StopFrame`, distinct from conversational/TTS interruption.
- Agent `GoalHandle` lifecycle — poll/cancel/feedback model for preemptible long-running skills.
- `edgevox/agents/workflow_recipes.py` — plan/execute/evaluate and iterative recovery recipes with separate evaluator roles and optional world predicates.
- Workflow primitives: Sequence, Fallback, Loop, Parallel, Router, Supervisor, Orchestrator, Retry, Timeout.
- `SimEnvironment` abstraction and ToyWorld / IR-SIM / MuJoCo adapters.
- ROS 2 bridge for transcription/response/state/metrics plus robot state, TF/Nav2/sensors and skill execution.
- `benchmarks/perf/bench_safety_preempt.py` — benchmark harness intended to quantify cancellation observation latency.
- Deterministic harness tests using scripted LLM behavior and ToyWorld to test agent topology without model downloads.

## Evidence inspected

README/source search confirms the safety architecture and documents that the LLM is not consulted on the critical stop path. Repository documentation names `tests/test_safety_monitor.py`, agent-skill lifecycle tests, workflow tests, simulation tests, and integration tests.

Commit history contains particularly useful upstream verification records:

- deterministic workflow tests spanning single/parallel tools, plan-execute-evaluate, loop-to-world-predicate and skill cancellation;
- scenario tests across ToyWorld, IR-SIM and MuJoCo;
- upstream-recorded local Gemma 4 runs, including explicit failures where a small model skipped required actions or misrouted tools;
- a correction where upstream first attributed a failed MuJoCo demo to the model, then directly tested the simulator, found a gantry-physics failure, switched to Franka, and documented the remaining LLM-side failure separately.

This is strong evidence discipline because simulation defects and model limitations are distinguished rather than folded into a success claim.

## Runtime / platforms

Primary implementation is Python. Documented environments include Linux, macOS and Windows, with CPU/CUDA/Metal paths. Optional robotics dependencies include ROS 2, IR-SIM and MuJoCo. Local voice/model paths include faster-whisper, llama.cpp and local TTS backends. Model setup is non-trivial and the README indicates roughly multi-gigabyte model downloads for the standard setup.

## Caveats

- GitHub Gold did **not** install EdgeVox, download its models, run pytest, execute the benchmark harness, launch IR-SIM/MuJoCo, attach ROS 2, drive physical hardware, measure stop latency, or independently validate the claimed offline/privacy boundary.
- The README explicitly says the sub-second first-audio voice target has not yet been backed by published measured performance; a benchmark harness exists, but the target must not be represented as a measured result.
- Upstream recorded real local model/simulation runs, but those are upstream evidence, not independent GitHub Gold verification.
- Physical-robot safety must not be inferred from a software `SafetyMonitor`; deployment still requires hardware-level limits, E-stop design, motion-controller safety and platform-specific validation.
- Latest inspected commit was 2026-08-09. That is reasonably recent but not active in the final weeks of September, so Maintenance is scored 3/5 rather than 5/5.
- Root `LICENSE` is Apache-2.0 and is authoritative for this dossier. Any conflicting stale badge/text elsewhere should be treated as documentation drift and checked before reuse of separately vendored assets/models.

## Verification boundary

Classification **VERIFIED** means concrete repository-native implementation/test evidence and explicit upstream run records were inspected. It does **not** mean GitHub Gold independently executed, benchmarked, safety-certified, or hardware-tested EdgeVox.

## Discovery provenance

Independent GitHub-first category rotation after the SQLite/local-first synchronization pass. A duplicate search of `kaibuzz0/Github-gold` returned no existing EdgeVox entry before this dossier was added.

## Strong recursive leads

1. Inspect `SafetyMonitor` + `GoalHandle` cancellation end-to-end and determine whether the preemption benchmark has recorded results or only a harness.
2. Inspect the ROS 2 bridge/action-server contract for clean extraction into other local agent frameworks.
3. Audit model/voice asset licenses separately from the Apache-2.0 application code.
4. Compare the world-predicate `PlanThenLoop` pattern with other agent harnesses that use external state rather than model self-evaluation.
5. Inspect `nrl-ai/edgevox-models` provenance and packaging before treating bundled simulation/model assets as reusable.
