# abxbus — typed cross-runtime event bus (2026-10-20)

**Upstream:** https://github.com/ArchiveBox/abxbus  
**Discovery:** GitHub-first recursive investigation from ArchiveBox/abx-dl.  
**Evidence:** VERIFIED, based on upstream source, release and CI; not independently executed.  
**Gold:** S / 28 (Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 5; Maintenance 4).  
**License:** MIT root (ArchiveBox contributors 2026). No source copied.

## Components verified by source inspection

- [Python EventBus](https://github.com/ArchiveBox/abxbus/blob/main/abxbus/event_bus.py): async event dispatch, context propagation, handler registration, queueing and middleware.
- [BaseEvent and EventResult](https://github.com/ArchiveBox/abxbus/blob/main/abxbus/base_event.py): typed Pydantic schemas and lifecycle/result tracking.
- [Lock manager](https://github.com/ArchiveBox/abxbus/blob/main/abxbus/lock_manager.py): context-aware reentrant asyncio locks and serial/parallel concurrency.
- [History](https://github.com/ArchiveBox/abxbus/blob/main/abxbus/event_history.py): ancestry lookup, bounded history and retention.
- [JSONL bridge](https://github.com/ArchiveBox/abxbus/blob/main/abxbus/bridge_jsonl.py): append-and-poll file bridge. Startup starts at current file size; exceptions in polling (other than cancellation) are suppressed. Do not assume durable replay or acknowledged delivery.
- Optional `bridge_redis.py`, `bridge_nats.py`, `bridge_postgres.py`, `bridge_sqlite.py`, `bridge_tachyon.py`: adapter implementations; not independently tested.
- [TypeScript](https://github.com/ArchiveBox/abxbus/blob/main/abxbus-ts/src/EventBus.ts), [Rust](https://github.com/ArchiveBox/abxbus/blob/main/abxbus-rust/src/event_bus.rs), [Go](https://github.com/ArchiveBox/abxbus/blob/main/abxbus-go/event_bus.go): independent language implementations.
- [Cross-runtime tests](https://github.com/ArchiveBox/abxbus/blob/main/tests/test_cross_runtime_roundtrip.py), plus Go, Rust and TS test suites.

## Release and working evidence

- [v2.5.77](https://github.com/ArchiveBox/abxbus/releases/tag/2.5.77) published 2026-10-09 19:52 UTC; default branch last inspected commit `4f1afa820aee6f266bbcac1701a35304592813c7`.
- [Main CI run 37981912198](https://github.com/ArchiveBox/abxbus/actions/runs/37981912198) passed 2026-10-09. All 120 job conclusions inspected across two pages were success, including Python, TypeScript, Go, Rust, roundtrip tests and release artifact smoke tests.
- [Docs run 39406555390](https://github.com/ArchiveBox/abxbus/actions/runs/39406555390) succeeded 2026-10-20.
- [Experimental rust-core-ffi CI 38198182954](https://github.com/ArchiveBox/abxbus/actions/runs/38198182954) **failed** 2026-10-12. It is not the successful default-branch run.
- `pyproject.toml`: Python >=3.11, Pydantic and optional Postgres/NATS/Redis/Tachyon extras. `abxbus-ts/package.json`: Node/browser ESM and CJS. `abxbus-rust/Cargo.toml`: MIT. `abxbus-go/go.mod`: Go 1.25.

## Caveats and maintenance

No local compilation, installation, runtime tests, benchmarking or security audit was performed. The event bus is in-memory by default. JSONL polling does not provide transactional acknowledgments or exactly-once guarantees. Optional transports require authentication, TLS, shutdown and replay testing; Python/TS/Rust/Go feature parity should be tested for each intended integration. MIT requires preserving attribution; dependencies have their own licenses.

**Adjacent ecosystem triage (2026-10-20):** [abx-plugins](https://github.com/ArchiveBox/abx-plugins) has an MIT root, substantial hook/config/test tree and release v1.13.474, but its latest inspected Parallel Tests run [39450943390](https://github.com/ArchiveBox/abx-plugins/actions/runs/39450943390) failed after prior [39446264043](https://github.com/ArchiveBox/abx-plugins/actions/runs/39446264043) succeeded. [abxpkg](https://github.com/ArchiveBox/abxpkg) has MIT root, binary-provider implementations and tests, but latest Run Tests [39444656035](https://github.com/ArchiveBox/abxpkg/actions/runs/39444656035) failed after [39413598967](https://github.com/ArchiveBox/abxpkg/actions/runs/39413598967) succeeded. Both remain research leads until failures and binary/plugin trust boundaries are assessed.

**YouTube:** Six playlist pages in `sources/youtube_playlists.md` retried 2026-10-20; three throttled, three disabled. No transcripts were accessible, so no YouTube-derived discoveries were claimed.

**Next:** Independently test cross-runtime roundtrips and optional bridge delivery semantics; diagnose abx-plugins/abxpkg CI failures; backfill legacy six-factor scoring.
