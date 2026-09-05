# Automerge: local-first CRDT engine and transport-agnostic sync protocol

- **Repository:** https://github.com/automerge/automerge
- **Author / Org:** Automerge / Ink & Switch contributors
- **Category:** local-first software / CRDTs / synchronization / offline-first data / collaborative applications
- **Evidence:** VERIFIED
- **Provisional Gold score:** 29/30 (S)
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 5/5
  - Novelty: 5/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** MIT
- **Discovery:** GitHub-first category rotation; no YouTube transcript claim used

## What it is

Automerge is a reusable local-first data engine built around conflict-free replicated data types (CRDTs). Upstream describes three core pieces in one stack: fast CRDT implementations, a compact encoded representation for CRDT state/history, and a synchronization protocol that efficiently transmits changes between peers.

Its design goal is unusually ambitious and useful: applications should be able to keep authoritative state locally, continue working while offline, accept concurrent edits on multiple replicas, and later merge those replicas without forcing application developers to manually implement conflict-resolution logic for every network interruption or concurrent edit.

The repository contains a core Rust implementation, JavaScript bindings built through WebAssembly, and a C FFI layer. The JavaScript package is the most polished developer-facing interface today; upstream explicitly says the lower-level Rust API is still comparatively under-documented and oriented toward the JavaScript backend.

## Why it qualifies as GitHub Gold

Automerge is valuable both as a complete library and as a source of reusable distributed-systems components:

- CRDT document and change-graph machinery;
- append-only/content-addressed change history;
- compact columnar serialization;
- peer synchronization state machines;
- Bloom-filter-assisted missing-change discovery;
- JavaScript/WASM bindings;
- C FFI support;
- incremental patch generation and application;
- offline-first persistence semantics;
- transport-agnostic replication primitives.

This is not simply a collaborative-text widget. It is infrastructure for building local-first editors, notes systems, shared structured documents, field-data tools, intermittent-connectivity applications, peer-to-peer data systems, and replicated state layers where replicas may diverge for substantial periods and later converge.

## Core repository structure

The repository is organized around several distinct implementation surfaces:

- `rust/automerge` — core Rust CRDT engine;
- `rust/automerge-wasm` — WebAssembly bridge used by the JavaScript package;
- `rust/automerge-c` — C FFI layer;
- `javascript` — idiomatic JavaScript interface over the WASM backend;
- `scripts` — CI/release/build tooling.

The Rust source tree exposes useful subsystem boundaries such as `change.rs`, `change_graph.rs`, `change_queue.rs`, `clock.rs`, `columnar`, `cursor.rs`, decoding/storage code, patch machinery, transactions, and `sync.rs`. These are strong recursive-research targets because they separate causality/history, storage, patching, synchronization, and public API concerns instead of collapsing all behavior into one opaque object.

## Synchronization protocol

`rust/automerge/src/sync.rs` is one of the strongest component-level findings.

The module documents a peer-to-peer synchronization loop built around per-peer `State` objects. Each side tracks what it believes the other peer has, generates a sync message, receives the peer's response, applies changes, and continues until neither side has anything further to send.

The implementation exposes a `SyncDoc` trait with methods for generating and receiving messages, which means the synchronization protocol is expressed as a reusable document capability rather than being inseparably bound to a particular HTTP/WebSocket/cloud service.

The protocol source currently includes:

- per-peer sync state;
- advertised document heads;
- explicit `need` and `have` sets;
- Bloom filters for efficiently representing likely-known changes;
- tracking of hashes already sent;
- in-flight-message state;
- read-only peer handling;
- protocol capability negotiation;
- V1/V2 message recognition;
- sync reset behavior;
- logic that chooses between incremental changes and sending a larger/full representation when doing so is more efficient.

One noteworthy current optimization: if the set of hashes that would need to be sent exceeds roughly one third of the document's change graph and the remote supports V2 messages, the implementation can choose a compact full-document transfer path instead of serializing a large set of individual changes.

That is exactly the kind of practical engineering signal GitHub Gold should capture: the protocol is not only theoretically convergent; the source contains explicit bandwidth/state-management tradeoffs.

## Transport boundary

Automerge's sync protocol assumes a reliable, in-order byte/message stream between two peers, but the library itself does not require a specific networking product or centralized server.

That makes the synchronization engine composable with higher-level transports such as WebSockets, authenticated application relays, peer-to-peer channels, local IPC, Bluetooth/mesh gateways, or other ordered transports, provided the surrounding application supplies the connectivity and security policy.

This also creates an important boundary: **Automerge synchronization is not, by itself, an authentication, authorization, identity, encryption, or hostile-peer sandbox.** An application still needs to decide who is allowed to exchange document changes, how peers are authenticated, whether the transport is confidential/integrity-protected, what documents a peer may access, and how resource-abuse limits are enforced.

That distinction should be preserved whenever Automerge is recommended for sensitive or multi-tenant systems.

## CRDT/change graph as reusable technical material

The core source exposes explicit change and change-graph modules rather than hiding causal history behind a storage server.

Recent September 2, 2026 commits continue refactoring `ChangeGraph` and clock handling for efficiency/readability, demonstrating that these internals are active engineering surfaces rather than abandoned legacy code.

Potential component research targets include:

- causal-head computation;
- vector/actor clocks;
- dependency traversal;
- missing-dependency calculation;
- change queues for temporarily orphaned changes;
- change hash addressing;
- history traversal and compaction behavior;
- incremental patch production;
- persistence and reload semantics.

These mechanisms are directly useful as references for other replicated-state systems even when Automerge is not adopted wholesale.

## Compact representation and Automerge 3

Upstream states that Automerge 3 achieved approximately a **10x reduction in memory usage** versus the preceding generation. GitHub Gold treats that figure as an upstream project claim rather than an independently reproduced benchmark.

The existence of a dedicated binary-format specification plus columnar storage modules is nevertheless strong evidence that storage/memory efficiency is a first-class part of the architecture rather than an afterthought.

A future pass should inspect the Automerge binary format and column encoders in depth, including how actor identifiers, operation IDs, causal dependencies, scalar values, strings, and change metadata are compressed and how format compatibility is maintained across releases.

## JavaScript, WebAssembly, and C reuse surfaces

The repository currently exposes the Rust engine through multiple environments:

- a stable `@automerge/automerge` JavaScript package;
- an internal/public `@automerge/automerge-wasm` layer;
- native Rust crates;
- a C library/FFI surface.

This materially raises reusability. A CRDT engine that only works inside one browser framework would score lower; Automerge instead has a systems-language core with WASM and native interoperability paths.

The README is candid that the Rust API is lower level and not yet documented to the same standard as the JavaScript interface. That is why Documentation is scored 4/5 rather than 5/5 despite the project's strong website/specification material.

## Working evidence and CI

The project has substantive current CI across multiple implementation and platform surfaces.

The main workflow currently runs:

- formatting checks;
- lint checks;
- Rust documentation builds;
- `cargo-deny` license/source/advisory checks;
- WASM tests;
- JavaScript tests;
- a dedicated Node 18 packaging compatibility test;
- native build/test jobs on Linux;
- native build/test jobs on macOS;
- native build/test jobs on Windows.

A recent September 2 commit moved most non-Windows CI execution behind reproducible Nix entry points so that the same jobs can be invoked locally rather than existing only as opaque GitHub Actions steps. The README documents `nix run .#ci` plus individual jobs such as formatting, lint, JS tests, and packaging checks.

That is a particularly strong verification/reproducibility signal.

The Windows path remains native because the maintainers explicitly note that Nix under WSL would validate Linux rather than true Windows behavior.

## Supply-chain caveat

The current CI workflow uses several GitHub Actions by mutable/version tags, including `actions/checkout@v7`, `cachix/install-nix-action@v31`, `dtolnay/rust-toolchain@1.90.0`, and `Swatinem/rust-cache@v2`, rather than pinning every external Action to an immutable commit SHA.

This is not a reason to reject the project, but it is worth recording as a supply-chain hardening opportunity.

`cargo-deny` is present and checks advisories, bans, licenses, and sources. In the inspected workflow the advisories matrix leg is configured `continue-on-error`, while the bans/licenses/sources checks are not. That nuance should not be flattened into a claim that every vulnerability advisory necessarily blocks CI.

## Release and maintenance state

The latest JavaScript GitHub release inspected is **v3.4.1**, published **August 12, 2026**. It follows v3.4.0 on July 31 and v3.3.x releases earlier in July.

Development is extremely current. Commits on **September 2, 2026** include:

- a WASM fix for very large list-insert patches that could exceed JavaScript engine argument/stack limits;
- migration of CI toward reproducible Nix commands;
- `ChangeGraph` clock-calculation refactoring;
- clock API readability improvements;
- public `Value`/`ScalarValue` API cleanup and documentation;
- dependency/configuration maintenance.

The large-list fix is particularly good maintenance evidence: the commit identifies the browser/JS-engine failure mechanism, explains why a very large consolidated insert could exceed V8's argument limits, and changes insertion to bounded chunks.

This is substantive correctness/robustness work, not only dependency churn.

## License and reuse boundary

The repository's root license is **MIT**. That is a highly permissive reuse posture, subject to retaining the copyright and permission notice in copies or substantial portions.

No Automerge source code was copied into GitHub Gold in this pass.

Future extraction/adaptation should still inspect package-specific manifests/notices for bundled dependencies, generated artifacts, examples, or companion repositories before assuming every external dependency shares the MIT license.

## Operational and security caveats

### CRDT convergence does not define application authorization

Automerge helps replicas converge, but the application must still decide whether a peer is authorized to read or contribute to a document. A technically valid Automerge change is not automatically an application-authorized change.

### Transport security is external

The sync engine assumes an ordered reliable transport. Encryption, authenticated peer identity, session establishment, relay policy, rate limiting, and network exposure belong to the surrounding system.

### Malicious/oversized input needs resource boundaries

Any parser and replicated-state engine receiving untrusted data should be given message/document size ceilings and memory/CPU controls. The September 2 large-list fix demonstrates that extremely large legitimate document operations can reach language/runtime limits even without malicious intent.

### CRDT history has storage/memory implications

Local-first replication intentionally preserves enough causal/change information to support merging and synchronization. Applications with very large histories should evaluate compaction, save/load behavior, document partitioning, snapshot size, and long-running peer-state overhead rather than assuming CRDT history is free.

### Rust API maturity differs from JavaScript

The JavaScript package is the project's primary polished interface. Upstream says the Rust API is comparatively low-level and less documented. Native Rust adopters should account for that maturity difference.

## Verification performed by GitHub Gold

This pass inspected:

- the current upstream README;
- root MIT license;
- latest GitHub release metadata;
- current commit history through September 2, 2026;
- repository CI workflow inventory;
- current main CI configuration;
- core Rust source-tree organization;
- `rust/automerge/src/sync.rs` synchronization protocol implementation and documentation;
- the existing GitHub Gold repository/search surface to confirm Automerge was not already cataloged;
- the current GitHub Gold draft PR/branch state so this work continues the existing research workflow rather than creating a parallel branch.

## Not verified locally

GitHub Gold did **not**:

- clone or build Automerge locally;
- run `nix run .#ci` or `./scripts/ci/run`;
- run Rust, WASM, JavaScript, C, Node, Windows, macOS, or Linux tests;
- execute a two-peer synchronization session;
- reproduce offline concurrent edits and convergence;
- benchmark memory use or independently reproduce the project's ~10x Automerge 3 memory claim;
- fuzz the binary format or synchronization parser;
- verify NPM/crates.io package provenance;
- test C FFI interoperability;
- test persistence/reload behavior;
- audit authorization or encrypted transport integrations;
- independently review the CRDT convergence proof or sync-protocol paper;
- perform a security or denial-of-service audit.

Claims here are source/document/release/workflow/upstream-evidence claims, not local operational certification.

## Strong recursive leads

1. **Automerge binary format** — columnar compression, compatibility guarantees, corruption handling, and format evolution.
2. **`sync.rs` + sync state** — V1/V2 negotiation, reset behavior, Bloom filters, read-only peers, message sizing, and interrupted-session recovery.
3. **`change_graph.rs`** — causal traversal, head computation, clocks, missing dependencies, and scalability.
4. **Patch system** — incremental UI updates, large-list behavior, text/list/map patches, and change observation.
5. **`automerge-wasm`** — JS/WASM boundary cost, memory ownership, large-patch chunking, and browser/runtime portability.
6. **`automerge-c`** — native interoperability and suitability for embedded/mobile/native application integration.
7. **`automerge-repo` ecosystem** — networking/storage adapters and repository-level document lifecycle beyond the core CRDT engine.
8. **`autosurgeon`** — higher-level Rust serialization/data-model ergonomics over the low-level Automerge API.
9. **Persistence/compaction** — save formats, incremental saves, long histories, garbage/retention behavior, and large-document recovery.
10. **Security envelope patterns** — authenticated document membership, encrypted transports, capability models, and abuse limits layered around CRDT synchronization.

## Promotion recommendation

**VERIFIED / S / provisional 29.**

Promote atomically into the synchronized catalog surfaces when the current draft research batch reaches its promotion phase. Automerge is unusually strong GitHub Gold because it provides a mature systems-language CRDT core, efficient synchronization protocol, compact persistent representation, multiple language bindings, reproducible cross-platform CI, and very active maintenance. The score remains below 30 because the native Rust developer surface is still explicitly less polished/documented than the JavaScript API and because the security/network envelope must be supplied by the embedding application.