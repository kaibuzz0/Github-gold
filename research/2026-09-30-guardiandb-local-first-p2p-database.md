# GuardianDB — local-first P2P database and edge compute

- **Repository:** https://github.com/wmaslonek/guardian-db
- **Author:** William Maslonek / wmaslonek
- **Category:** local-first database / P2P / Rust / Iroh / CRDT / SQL / edge compute
- **Evidence:** VERIFIED (repository-native evidence; not independently executed by GitHub Gold)
- **Provisional Gold score:** 28/30 — S
  - Utility 5/5
  - Working evidence 5/5
  - Reusability 5/5
  - Novelty 5/5
  - Documentation 5/5
  - Maintenance 3/5
- **License:** MIT OR Apache-2.0
- **Discovery:** GitHub-first breadth rotation. YouTube transcripts were not required for this candidate.

## Why it matters

GuardianDB is an unusually broad local-first data substrate. Each node keeps a local replica, reads and writes locally, and synchronizes changes over Iroh. The project combines key/value and document stores, an append-only causal event log, PostgreSQL-compatible SQL/wire protocol, a Supabase-shaped gateway, vector search/RAG, and optional peer-delegated WebAssembly/AI compute.

The useful idea is not merely the feature count: several components expose reusable patterns for applications that need to keep operating through intermittent connectivity while retaining conventional database interfaces.

## Architecture / useful components

Upstream documents these principal surfaces:

- Iroh-based encrypted P2P connectivity, discovery, QUIC transport, blobs/docs/gossip, connection pooling and metrics.
- KeyValueStore and DocumentStore backed by Iroh Docs with LWW conflict semantics and Willow range-based reconciliation.
- EventLogStore with causal DAG ordering and BLAKE3 links.
- PostgreSQL-compatible SQL and `pgwire` support so existing clients such as psql, node-postgres, TypeORM and DBeaver can connect.
- Optional ODM/model layer over replicated document storage.
- HNSW vector index, embedding pipeline and RAG helper.
- Guardian Compute: sandboxed Wasmtime tasks, peer capability telemetry, scheduling/failover/redundancy and optional NN/LLM backends.
- Sentinel administration/monitoring surface.
- Payload-codec extension point plus optional XChaCha20-Poly1305 record encryption and encrypted keystore.

Specific reusable research targets:

1. `src/p2p/network/` — Iroh client/backend, discovery, blobs/docs/gossip and connection management.
2. `src/stores/document_store/` — live-index synchronization for changes arriving from P2P replication.
3. `src/stores/kv_store/` — replicated key/value store behavior and payload codec integration.
4. `src/log/` — causal event-log structures, Lamport clock and access control.
5. SQL/pgwire layer — conventional database compatibility over local-first replicated storage.
6. Compute feature family — Wasmtime sandbox, capability-aware scheduling, failover and peer delegation.
7. Vector/embedding/RAG feature family — per-node derived ANN state over replicated source records.
8. Payload codecs / keystore — application-controlled confidentiality boundary when replicas possess replication tickets.

## Evidence inspected

### Source/package evidence

`Cargo.toml` declares version 0.20.26, Rust edition 2024 / Rust 1.97+, and `MIT OR Apache-2.0`. Its feature graph exposes optional ODM, SQL, PostgreSQL wire protocol, Supabase-compatible gateway, Wasmtime compute, NN/CUDA, LLM, HNSW vector indexing, embedding, ONNX embedding, RAG and encryption surfaces rather than presenting them only as README concepts.

### Release evidence

GitHub's latest stable release is **v0.20.26**, published **2026-07-31**. The release notes describe the vector-search/embedding/RAG stack, SQL decoded-table cache, payload-codec/encryption work, messaging/pub-sub refactors and transport fixes. No binary assets were attached to the inspected release; the primary distribution is source/crate-oriented.

### CI evidence

GitHub Actions has current successful scheduled evidence. The inspected `GuardianDB ODM CI` run #43 completed successfully on **2026-09-28** against the repository's current main commit. This supports continuing build/test activity, but it must not be generalized into proof that every optional feature combination or distributed deployment scenario passed.

### Important evidence boundary

The repository's own RFC material still identifies replication/conformance work that should not be overstated. In particular, an RFC calls for un-ignoring SQL replication tests, replacing fixed propagation sleeps with event waits, and extending convergence coverage to deletes, >2 peers and DDL. Therefore the dossier treats the implementation and current CI as concrete working evidence while **not** claiming comprehensive distributed-SQL convergence verification.

## Security / privacy notes

The README correctly distinguishes transport encryption from payload confidentiality. A peer holding an Iroh Docs ticket can replicate the namespace, so applications that require confidentiality from replica holders need payload encryption/key management. The optional payload codec addresses record values, but metadata such as keys, sizes, write timing and authorship is not thereby hidden. Direct blob use also has separate content-addressing implications.

This is a useful design lesson for any local-first system: replication authorization and content confidentiality are different trust boundaries.

## Requirements / platforms

Core library is Rust/Tokio and requires Rust 1.97+ according to the package metadata. Feature requirements vary significantly: SQL/pgwire are lighter than compute/NN/CUDA or local ONNX/LLM stacks. Iroh supplies the P2P transport layer. Applications integrating the heavier feature sets should audit build-time downloads, native runtime requirements and model licensing separately.

## Licensing

Root/package licensing is dual **MIT OR Apache-2.0**. No upstream implementation was copied into GitHub Gold. Dependencies, model weights, ONNX Runtime/CUDA artifacts and externally supervised LLM backends retain their own licenses and distribution terms and require component-level review before redistribution.

## Verification performed by GitHub Gold

Inspected repository metadata, README architecture, Cargo feature/package metadata, latest GitHub release, current GitHub Actions history and code/RFC search results around replication.

GitHub Gold did **not** build GuardianDB, execute its tests, create a multi-peer cluster, measure Willow reconciliation, connect psql/TypeORM, run Supabase compatibility tests, exercise Wasmtime/AI compute, benchmark HNSW, test encryption, or independently reproduce performance claims. Any numerical performance claims in upstream documentation remain upstream measurements.

## Caveats

- Pre-1.0 API; feature surface is large and can change materially.
- A successful ODM CI run does not prove every optional Cargo feature or distributed failure mode.
- RFC text exposes still-desired SQL replication/convergence test hardening; do not market the distributed SQL layer as exhaustively verified.
- Full-replica architecture may be unsuitable for very large or selectively replicated datasets without application-level partitioning/topology decisions.
- Payload encryption does not provide metadata privacy, forward secrecy or automatic key management.
- Heavy AI/GPU features expand dependency and supply-chain surface considerably.

## Gold assessment

**VERIFIED / S / 28** is justified by concrete source architecture, a deep feature graph, stable tagged release, active successful CI and unusually strong documentation. Maintenance is scored conservatively because the inspected stable release is from July and the current successful scheduled CI points at an August main commit; the repository is active operationally, but this pass did not establish rapid post-August source evolution.

## Strong next leads

1. Inspect Iroh/Willow reconciliation and live-index update semantics under partitions and reconnects.
2. Audit SQL replication tests and the fenced-shard-primary RFC against implemented guarantees.
3. Study payload-codec associated-data/key lifecycle and ticket threat boundaries.
4. Inspect Guardian Compute scheduling, sandbox capabilities, cancellation and k-of-n redundancy.
5. Compare GuardianDB's local-first architecture with Loro, Automerge, ElectricSQL and other CRDT/sync engines without conflating their consistency models.
6. Verify crate publication/reproducible builds and feature-matrix CI coverage.