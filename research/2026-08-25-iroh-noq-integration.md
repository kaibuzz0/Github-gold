# Iroh ↔ noq Integration Boundary — 2026-08-25

## Purpose

This dossier moves one layer upward from the existing Quinn/noq transport comparison and inspects how current `n0-computer/iroh` actually consumes `n0-computer/noq`.

The goal is to identify the reusable architectural boundary between:

- **noq** — QUIC transport, multipath state, path events, NAT-traversal events, connection/path handles and transport configuration
- **Iroh** — endpoint identity, address discovery, relay fallback, direct-path discovery, hole punching, path selection and application-facing connection APIs

This is source inspection only. GitHub Gold did not build, deploy, packet-capture, benchmark or interoperability-test Iroh/noq in this pass.

## Executive finding

Iroh does **not** simply call noq as a generic QUIC socket.

Instead, Iroh deliberately wraps and constrains the noq surface, configures noq with Iroh-specific multipath/NAT-traversal defaults, and then runs its own per-remote state machine above noq.

That upper state machine merges:

- endpoint identity
- address lookup results
- local/reflexive direct addresses
- relay mappings
- custom transport addresses
- noq path events
- noq NAT-traversal candidate-address events
- connection lifecycle events
- scheduled hole-punch attempts
- pending path-open attempts
- preferred-path selection

The resulting split is clean and reusable:

> **noq answers “what QUIC paths exist and what happened to them?”; Iroh answers “which peer addresses should we try, when should we punch/open them, and which working path should the application prefer?”**

This makes Iroh/noq a particularly useful reference for separating transport-level traversal mechanics from application-level peer-connectivity policy.

## Source snapshot inspected

Current Iroh source inspection used upstream commit:

`2b9f4418014b574365ae025efe42d5ddfbb2527f` — August 24, 2026

Primary inspected files:

- `iroh/src/endpoint/quic.rs`
- `iroh/src/socket/remote_map/remote_state.rs`

Supporting repository search hits confirmed related integration surfaces in:

- `iroh/src/socket/remote_map/remote_state/path_watcher.rs`
- `iroh/src/socket/transports.rs`
- `iroh/src/socket/transports/relay.rs`
- `iroh/src/endpoint/connection.rs`
- `iroh/src/socket.rs`
- `iroh-relay/src/quic.rs`

## 1. Iroh creates an explicit noq encapsulation layer

`iroh/src/endpoint/quic.rs` begins by stating that the module exists to co-locate Iroh's noq exports and to **limit or expand how selected noq types are used inside Iroh**.

That is a strong architectural signal: Iroh does not let the transport dependency leak indiscriminately through its public API.

The wrapper selectively re-exports noq/noq-proto types such as:

- streams and datagrams
- connection errors/stats
- path stats and PathId
- congestion-controller traits/metrics
- MTU and ACK-frequency configuration
- transport parameters and crypto-facing types

This creates a compatibility boundary where Iroh can expose transport capability without making every internal noq detail part of Iroh's long-term API contract.

### Reuse lesson

For an application built over an evolving transport fork, a narrow compatibility module is valuable because it:

- prevents accidental dependency leakage
- localizes breaking upstream changes
- gives the application room to enforce safe defaults
- makes future transport replacement or fork synchronization less invasive

## 2. Iroh overrides noq defaults specifically for peer connectivity

`QuicTransportConfigBuilder::new()` starts with `noq::TransportConfig::default()` and then overrides settings for Iroh.

Inspected defaults include:

- connection keepalive interval
- **default path keepalive interval**
- **default path maximum idle timeout**
- **maximum concurrent multipath paths**
- **maximum remote NAT-traversal addresses**
- server handshake migration enabled

The module documentation explicitly warns that these defaults are chosen so **Iroh hole punching works well with QUIC multipath**, and that changing them can produce suboptimal behavior.

This is important: peer-connectivity behavior is not only an application policy sitting above a neutral transport. Iroh deliberately tunes transport liveness/path capacity so the higher-level traversal logic has enough viable path state to work with.

### Architectural boundary

The split is therefore:

- **noq** provides the knobs and transport machinery.
- **Iroh** chooses operational values appropriate for its peer-to-peer network model.

That distinction is useful when reusing the transport elsewhere: copying Iroh's values blindly would be inappropriate for a conventional client/server QUIC service.

## 3. One actor owns connectivity state for each remote endpoint

`RemoteStateActor` is the central upper-layer integration point.

The source describes it as managing **all connections to one remote endpoint**, triggering hole punching and selecting the best path.

Its state contains two broad groups.

### Hooks into the broader Iroh socket

- remote `EndpointId`
- socket metrics
- local/direct/reflexive address watcher
- relay mapped-address table
- custom mapped-address table
- address lookup services

### noq-driven connection/path state

- open connections indexed by stable connection ID
- connection-close futures
- merged noq path-event streams across connections
- merged noq NAT-traversal address-event streams across connections

### Iroh's own path-policy state

- all known potential remote paths
- most recent hole-punch attempt
- current selected/preferred path
- scheduled next hole punch
- scheduled pending path-open retry
- paths waiting for enough remote connection IDs / PathIds to become openable
- current address-lookup stream
- injected path-selection policy

This actor is where transport observations become peer-connectivity decisions.

## 4. Iroh combines multiple address sources before transport selection

The remote state is not built only from addresses learned by QUIC.

Potential paths can come from:

- Iroh address lookup
- local/direct address discovery
- reflexive direct addresses
- relay address mappings
- custom transport mappings
- noq's announced NAT-traversal candidates

The source explicitly notes that address-lookup paths may be entirely unusable; they are treated as **potential** paths rather than immediately trusted/selected routes.

That separation between **candidate knowledge** and **validated working path** is an important design property.

A directory/DNS/discovery layer may tell the system where a peer might be. noq path state tells the system whether a concrete QUIC path actually works.

## 5. noq path events are merged across every active connection

The actor keeps a merged stream of noq `PathEvent`s from all connections to the same endpoint.

This is a subtle but useful design choice: preferred connectivity is managed at the **peer/endpoint level**, not independently inside each individual application connection.

Iroh can therefore retain knowledge about a peer's working or failing paths and use that state while multiple QUIC connections are active.

The actor also intentionally survives for a short period after becoming idle so path knowledge can be reused by subsequent connections instead of being discarded immediately.

### Reuse lesson

For peer-to-peer applications, network-path intelligence often belongs to the **peer session** rather than a single transport connection.

That permits:

- faster later connections
- shared path quality knowledge
- less repeated discovery work
- coordinated relay/direct upgrade decisions

## 6. noq NAT-address events trigger Iroh hole-punch policy

The actor separately merges noq NAT-traversal address events.

When those events arrive, Iroh does not treat them as a complete connection decision. Instead, the actor records that remote-address information has changed and **triggers its own hole-punching workflow**.

Local direct-address changes do the same thing.

This cleanly shows the layer boundary:

- noq produces traversal/address events.
- Iroh decides when those changes justify a new peer-connectivity attempt.

That prevents the lower transport from owning all retry policy and endpoint-level discovery behavior.

## 7. Hole punching is deliberately rate-limited and scheduled

The actor defines a minimum interval between hole-punch attempts when candidate addresses have not changed.

Current inspected constant:

- `HOLEPUNCH_ATTEMPTS_INTERVAL = 5s`

Iroh also carries explicit scheduling state for future attempts rather than immediately spinning on failures.

This matters operationally because traversal can involve probing externally supplied candidate addresses. Bounding retry frequency protects both local resource usage and remote/unrelated networks from uncontrolled probe loops.

The existing noq source-level dossier already documents capped off-path NAT probe attempts inside the transport. Iroh adds another policy layer above that transport cap.

This is a good defense-in-depth pattern:

- **transport:** cap individual traversal/probe mechanics
- **application peer manager:** cap when traversal campaigns are initiated

## 8. Relay is a working path, not the final preferred state

The actor's comments make a key policy explicit: having a selected working path does **not** mean Iroh stops searching for something better.

A selected relay path is considered functional, but the actor continues to schedule hole punching/upgrades so it can discover a direct route.

Iroh defines:

- a periodic upgrade/check interval
- a low-latency threshold under which a path is considered “good enough”

Current inspected values include:

- upgrade check interval: `60s`
- good-enough latency: `10ms`

The key architecture is more important than the exact constants:

1. relay gives immediate reachability
2. direct candidates continue to be explored
3. only paths that become functional in noq are eligible for selection
4. a peer-level selector chooses the preferred working route

This is the relay-to-direct transition boundary that the earlier QUIC dossiers were missing.

## 9. Path opening can be deferred by QUIC path-identity resources

The actor maintains `pending_open_paths` for paths that could not yet be opened because the remote side had not provided enough connection IDs / PathIds.

It then schedules retries and calls path-open logic across active connections when resources become available.

This directly connects the previous noq source findings to Iroh policy:

- noq exposes logical PathIds and multipath path-opening constraints
- Iroh may know a network route is worth trying before the QUIC connection has enough path identity resources to open it
- Iroh therefore queues that route at the peer-management layer rather than losing it

This is a concrete example of why transport multipath and application path discovery cannot be treated as completely independent systems.

## 10. Preferred-path policy is injected rather than hard-coded

`RemoteStateActor` carries an `Arc<dyn PathSelector>`.

That means path choice is represented as a replaceable policy abstraction rather than being fused into the actor's discovery/event loop.

The actor owns:

- candidate acquisition
- validation/event observation
- scheduling
- connection/path lifecycle

while the selector owns the choice among viable paths.

### Reuse value

This separation makes it possible to experiment with path-selection criteria such as:

- latency
- direct-vs-relay preference
- metered-network cost
- interface preference
- reliability/history
- policy/security requirements

without rewriting the machinery that discovers and maintains paths.

GitHub Gold did not inspect every current selector implementation in this pass, so no claim is made about the full present scoring algorithm.

## 11. Iroh keeps selected-path state separate from “all known paths”

The actor stores both:

- a broad set of potential/observed paths
- a single currently preferred path expected to work

The source comments emphasize that the selected path is only assigned after it is **functional in noq**.

If Iroh learns that path is broken, selection returns to `None` and discovery/upgrade logic can continue.

This avoids a common networking mistake: treating a recently discovered address as equivalent to a validated route.

## 12. Multiple connections share one remote connectivity controller

When a new noq connection is added, Iroh:

- allocates a path-state watcher for it
- indexes it by stable connection ID
- hooks its path events into the actor's merged path stream
- hooks its NAT-address events into the merged address stream
- tracks its closed future

The remote actor therefore becomes a coordinator above multiple transport connections.

That design is particularly valuable for protocol-rich P2P applications where several logical/application sessions may target the same cryptographic endpoint.

## 13. Current maintenance reinforces the chosen boundaries

Recent Iroh maintenance inspected in this run includes:

### August 24, 2026 — datagram-batch processing regression fix

Upstream fixed handling where an empty datagram batch could prematurely stop processing later batches, and added a smaller regression test.

### August 24, 2026 — relay shutdown cancellation fix

Upstream replaced a `JoinSet::join_all` shutdown path that could panic when a relay task had been cancelled with explicit draining using `join_next`, together with a regression test targeting the cancelled-task state.

This is directly relevant to Iroh's relay layer: relay fallback is production lifecycle infrastructure, not only a connection bootstrap trick.

### August 21, 2026 — randomized mapped addresses

Iroh replaced predictable counter-derived internal mapped addresses with random values so external observers cannot guess those internal mappings.

### August 21, 2026 — dependency/Actions hardening

Upstream introduced locked dependency usage, pinned Actions and additional CI/supply-chain hardening.

These changes reinforce that the project is actively maintaining both transport correctness and the operational layers surrounding noq.

## 14. Relationship to Quinn and noq

The current Gold architecture picture is now:

### Quinn

Best reference for:

- mature standardized QUIC
- compact conventional path migration
- long-lived protocol hardening
- deterministic sans-I/O testing baseline

### noq

Best reference for:

- logical multipath PathIds
- simultaneous path lifecycle
- QUIC-integrated address discovery
- transport-level NAT traversal
- richer path/congestion-controller signaling

### Iroh

Best reference for:

- cryptographic peer identity above QUIC
- merging multiple candidate-address sources
- peer-level path intelligence across connections
- relay-first reachability with continuing direct upgrade attempts
- application-controlled hole-punch scheduling
- pending path-open orchestration
- pluggable preferred-path policy
- converting noq path/address events into application connectivity

This three-layer view is more useful than treating the projects as interchangeable networking libraries.

## 15. Practical design pattern extracted for GitHub Gold

A reusable peer-connectivity stack can be decomposed into four layers:

### Layer A — transport protocol

Owns:

- packets
- validation
- connection IDs / PathIds
- RTT/loss/MTU
- streams/datagrams
- transport NAT-traversal primitives

Reference: `noq-proto` / noq.

### Layer B — transport wrapper

Owns:

- curated public exports
- application-safe defaults
- dependency compatibility boundary

Reference: `iroh/src/endpoint/quic.rs`.

### Layer C — peer path controller

Owns:

- address-source merging
- relay/direct candidates
- hole-punch scheduling
- retry/backoff campaigns
- connection aggregation
- pending path opens
- selected working path

Reference: `RemoteStateActor`.

### Layer D — application protocol

Owns:

- which endpoint to dial
- application ALPN/protocol
- stream/datagram semantics
- higher-level blob/gossip/document behavior

Reference: broader Iroh ecosystem.

Keeping these responsibilities separate is one of the strongest reusable architecture findings from the Quinn → noq → Iroh research line.

## Security and operational caveats

- Candidate addresses from discovery mechanisms are only potential paths and should not be treated as trusted/working until validated.
- Relay availability is a resilience mechanism but creates operational dependency on relay infrastructure unless self-hosted.
- Traversal probes need bounded retry behavior; both noq and Iroh contribute limits/policy at different layers.
- Multipath/QAD/QNT work remains evolving and should not be assumed interoperable with arbitrary QUIC implementations.
- Randomized internal mapped addresses reduce predictability but are not a substitute for access control or transport authentication.
- Per-peer retained path intelligence can improve reconnect performance, but stale state must be expired or invalidated on network changes.

## Verification boundary

Performed:

- direct inspection of Iroh's noq wrapper/configuration layer
- direct inspection of `RemoteStateActor` state and event loop
- inspection of how noq path events and NAT-address events feed Iroh scheduling
- inspection of relay/direct path-state comments and pending path-open state
- inspection of current upstream Iroh commit history through August 24, 2026
- cross-reference against the existing Quinn/noq source-level dossier

Not performed:

- no local build
- no unit/integration test execution
- no deployment behind real NATs
- no relay deployment
- no packet capture
- no path-selection benchmark
- no Iroh↔generic Quinn interoperability test
- no QAD/QNT conformance testing
- no security audit

## Catalog conclusion

This pass does not create a new candidate; it **strengthens the existing Iroh/noq/Quinn entries with a concrete integration architecture**.

The source evidence supports retaining:

- **Quinn — VERIFIED / provisional S / 29**
- **noq — VERIFIED / provisional S / 28**
- **Iroh — VERIFIED / provisional S / 29**

The strongest next comparison is lateral rather than deeper in the same codebase: compare Iroh's relay-first/direct-upgrade controller with **Tailscale DERP/direct path selection** and **go-libp2p AutoNAT + hole punching**, focusing on which responsibilities each system puts in transport, discovery, relay, and peer-policy layers.
