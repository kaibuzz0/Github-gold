# Ghidra and Open MCT discovery — 2026-10-25

## Scope
Inspected current README, active draft PR #7, 84-entry catalog, master list, existing Rizin record and research workflow. GitHub-first discovery; two YouTube playlist pages could not be fetched (throttled/disabled), so no transcript-derived claims. No third-party code copied.

## Ghidra — VERIFIED (upstream), S/28
Repository: https://github.com/NationalSecurityAgency/ghidra
Score factors: 5 utility + 4 working evidence + 5 reusability + 5 novelty + 5 documentation + 4 maintenance = 28.

Inspected README, LICENSE, NOTICE, Ghidra/application.properties, .github/workflows/build-ghidra.yml, Ghidra/Features/Decompiler/src/main/java/ghidra/app/decompiler/DecompInterface.java, Ghidra/Features/Decompiler/src/decompile/cpp/sleigh.hh, and headless launcher source. Stable 12.2 released 2026-10-22: https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build . Upstream build run 39747670372 (2026-10-22) passed one Ubuntu Gradle buildGhidra job: https://github.com/NationalSecurityAgency/ghidra/actions/runs/39747670372 . Not a full regression suite; no independent execution.

Useful components: DecompInterface (persistent decompiler process), SLEIGH (instruction-to-p-code), AnalyzeHeadless (batch analysis), analyzeHeadless and sleigh launchers. JDK 25, Gradle 9.1+, Python 3.9–3.15 and native tools for source builds; Linux/macOS/Windows. NOTICE distinguishes Apache-2.0 core, GPL-3 stand-alone helpers and module-specific licenses. 2026 advisories GHSA-8jqp-qv73-395r (decompiler use-after-free) and GHSA-wm33-9f68-3vjg (Mach-O parser resource exhaustion) were patched in 12.1. No security audit or parser fuzzing performed.

## Open MCT — PROMISING, A/25
Repository: https://github.com/nasa/openmct
Score factors: 5 utility + 3 working evidence + 5 reusability + 4 novelty + 5 documentation + 3 maintenance = 25.

Inspected README, LICENSE.md, package.json, API.md, src/api/telemetry/TelemetryAPI.js, AGENTS.md, .github/workflows/e2e-full.yml and CI job steps. Stable v4.3.1 released 2026-08-31: https://github.com/nasa/openmct/releases/tag/v4.3.1 . Current package engine Node >=24.14.1; workflow selects Node lts/hydrogen (18). On 2026-10-25 upstream run 40147454572 FAILED at Ubuntu npm ci; Playwright tests skipped, Windows job cancelled: https://github.com/nasa/openmct/actions/runs/40147454572 . Node mismatch is a hypothesis, not established cause; do not claim e2e verified.

Useful components: TelemetryAPI.js, BatchingWebSocket.js, TelemetryCollection.js, src/plugins/persistence/couch/, src/api/plan/PlanAPI.js, API.md, e2e/tests/. Core Apache-2.0 LICENSE.md; source headers reference LICENSES.md not found at root, requiring package/asset license inspection. No independent install, browser test, telemetry ingestion or security audit.

## Maintenance and next leads
Added Ghidra to Rizin's related projects as an independent alternative, without changing Rizin A/25 score or its Capstone CI caveat. Next: Ghidra SLEIGH/PyGhidra and parser fuzzing; Open MCT Node mismatch, passing e2e, telemetry reconnect/batching, CouchDB security and third-party licensing.
