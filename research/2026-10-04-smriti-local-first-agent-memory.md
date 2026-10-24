# Smriti — local-first bi-temporal memory for AI agents

- **Repository:** https://github.com/vn-envy/Smriti
- **Author / Org:** vn-envy / Neekhil Vatsa
- **Category:** AI agents / local-first memory / SQLite / retrieval / MCP
- **Evidence:** VERIFIED
- **Tier / Score:** S / 28
- **Score:** Utility 5; Working Evidence 4; Reusability 5; Novelty 5; Documentation 5; Maintenance 4.
- **Version inspected:** 0.4.2 (2026-09-26)
- **Language / runtime:** Python 3.9+; core dependency surface is Python stdlib + numpy.
- **License:** Apache-2.0.

## What it does

Smriti is a zero-infrastructure memory layer for AI agents centered on a single SQLite database. It stores append-only conversational episodes plus bi-temporal facts that can be superseded without deleting historical state. Its current default read path combines BM25 and vector evidence, temporal grounding, session roll-up, question-aware priors and budget-aware context packing. It also exposes an MCP server and a read-only doctor utility.

## Why it matters

The valuable part is not merely another vector-memory wrapper. Smriti combines several reusable ideas in a compact, inspectable system:

- bi-temporal fact supersession with validity windows;
- append-only episodic memory;
- SQLite FTS5 plus exact numpy vector search;
- deterministic temporal grounding for relative dates;
- evidence-first context packing that preserves whole supporting turns where possible;
- named retrieval profiles for facts, relations, timeline and deeper recall;
- embedder-identity checks, export/import, erasure and diagnostic tooling;
- a benchmark harness designed to measure evidence retrieval and context survival rather than only end-answer scores.

## Useful components

- `smriti/store.py` — SQLite-backed episodes, facts, FTS and vectors.
- `smriti/recall.py` — evidence-first retrieval/fusion and packing.
- `smriti/temporal.py` — deterministic relative-date and time-window handling.
- `smriti/profiles.py` — retrieval profiles and zero-token routing.
- `smriti/mcp_server.py` — MCP integration.
- `smriti/doctor.py` — read-only database/integrity diagnostics.
- `bench/lab/` — deterministic retrieval/context-survival benchmark framework.
- `audit/` — unusually detailed benchmark provenance, raw results and research notes.

## Evidence inspected

Repository metadata, README, package metadata, Apache-2.0 license, changelog, benchmark documentation and implementation/search surfaces were inspected. Package metadata declares v0.4.2, Python >=3.9 and numpy as the sole core dependency. The repository contains explicit benchmark methods and raw/audit material rather than only headline performance claims. An enterprise CI workflow covers Python 3.9 and 3.12.

Upstream reports 326 core + enterprise tests and held-out benchmark improvements for its evidence-first read path. Those figures are recorded as **upstream measurements**, not GitHub Gold independent results. The README explicitly warns that its LME-X construction is not the official LongMemEval-S haystack and therefore should not be compared directly with published LongMemEval leaderboard scores.

## Verification boundary

GitHub Gold did **not** install Smriti, run its tests, reproduce its benchmark results, run the MCP server, validate concurrent SQLite behavior, exercise export/import or erasure, run ONNX embeddings, or independently compare it with Mem0/GBrain/Hindsight/Graphify. VERIFIED here means repository-native evidence for implemented functionality is concrete and inspectable, not independent operational certification.

## Caveats

- Package metadata still classifies the project as **Alpha**.
- README states there is no PyPI release yet; installation is from source.
- Benchmark numbers are primarily upstream self-evaluation, albeit with unusually good methodology/provenance.
- Exact numpy vector scanning is intentionally simple and may become the limiting factor at larger scales.
- Full mode can call an LLM for extraction/arbitration; only lite mode and the default query path can be fully token-free/offline.
- External models, datasets and optional dependencies retain their own licenses/terms.

## Discovery / provenance

GitHub-first discovery on 2026-10-04. No existing Smriti entry was found in Github-gold before this dossier was prepared.

## Strong follow-ups

1. Independently run the offline test suite.
2. Reproduce the quickstart supersession/as-of behavior.
3. Run the deterministic benchmark harness on a fixed local dataset/model cache.
4. Audit SQLite transaction/concurrency and crash-recovery behavior.
5. Verify export/import and owner-erasure invariants.
6. Exercise MCP against a real agent client.
7. Profile exact-vector search at 100k–1m turns.
8. Compare the same corpus/budget against Mem0, Letta/MemGPT, Hindsight and lightweight SQLite-only baselines.
