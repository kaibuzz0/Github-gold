# Quinn ↔ noq Source-Level QUIC Divergence — 2026-08-25

## Purpose

This dossier deepens the existing Quinn/noq architectural comparison with direct source inspection of the current upstream protocol cores. It is not a build, benchmark, protocol-conformance test, or cryptographic audit. The goal is to identify concrete code-level differences that explain why `n0-computer/noq` is useful as a separate Gold entry despite its Quinn ancestry.

## Executive finding

The divergence is now concrete enough to state precisely:

- **Quinn** keeps the conventional mature single-active-path / migration-oriented QUIC model in `quinn-proto`.
- **noq** has reworked that path model so **path identity, path-number spaces, path migration, path draining, per-path liveness, address discovery and NAT traversal are first-class protocol state**.

The result is not merely a Quinn fork with experimental frames bolted on. The extension work reaches into packet-number spaces, path state, timers, congestion control callbacks, transport configuration, frame handling and async API surfaces.

For GitHub Gold, Quinn remains the cleaner baseline for standardized mature QUIC behavior; noq is the stronger research reference for how such a core evolves when simultaneous paths and transport-integrated NAT traversal become design requirements.

## Source snapshots inspected

### Quinn

Current inspected source paths:

- `quinn-proto/src/connection/paths.rs`
- `quinn-proto/src/congestion.rs`

### noq

Current inspected source paths:

- `noq-proto/src/connection/paths.rs`
- `noq-proto/src/congestion.rs`
- `noq-proto/src/n0_nat_traversal.rs`
- supporting search hits in `connection/mod.rs`, `connection/spaces.rs`, `transport_parameters.rs`, `frame.rs`, `tests/multipath.rs` and `config/transport.rs`

The noq source snapshot inspected corresponds to upstream commit `a62dafd56ad9f90e759e0c3917176a5969871b2c` (August 24, 2026 release). Quinn source inspection used the current `main` representation returned by GitHub during this run.

## 1. Path identity is a structural noq addition

### Quinn baseline

Quinn's `PathData` models a particular network path around a remote socket address. It carries:

- remote address
- RTT estimator
- ECN state
- congestion controller
- pacer
- PATH_CHALLENGE state
- validation state
- sent/received byte counters
- MTU discovery
- in-flight accounting
- path generation identifier

Migration creates a new `PathData` from the previous one while retaining cloned congestion/RTT/MTU state where appropriate.

This is a strong and relatively compact model for normal RFC 9000 path migration.

### noq multipath model

noq introduces an explicit encoded `PathId(u32)` with `ZERO`, `MAX`, encode/decode logic and arithmetic helpers.

More importantly, the source comments separate two concepts:

1. **`PacketNumberSpace` / PathId state** — persists across migration and identifies a multipath QUIC path.
2. **`PathData` / network 4-tuple state** — represents one concrete network route used by that path ID.

A single PathId can therefore migrate to another 4-tuple while retaining its path-number-space identity, and several PathIds may use the same 4-tuple.

This is a major architectural distinction from baseline Quinn. Path identity is no longer synonymous with the current remote socket route.

## 2. noq retains previous path data explicitly

noq wraps current path data in `PathState` with:

- current `PathData`
- optional previous `(ConnectionId, PathData)`

The comments state this retained previous path exists to defend against migration attacks, support probing, and correctly account packets associated with older path generations.

The source also tracks a unique `generation` for each new 4-tuple incarnation even when the same PathId migrates.

This creates a two-dimensional identity system:

- protocol-level PathId
- concrete network-path generation

That separation is valuable for any multipath transport because stale packets, migration races and path-reuse cases cannot be handled safely using only a socket tuple or only a logical path identifier.

## 3. noq adds substantially richer per-path lifecycle state

Compared with Quinn's `PathData`, noq's inspected `PathData` adds or expands:

- application-limited tracking tied to congestion-control growth
- multiple outstanding path challenges rather than a single challenge slot
- challenge-loss counters with exponential retry behavior
- path-specific retransmit queues
- last observed-address report
- explicit multipath path status
- path-level PTO count
- **per-path idle timeout**
- **per-path keepalive interval**
- idle-reset permission state
- **draining state for abandoned paths**
- network path represented as a full `FourTuple`

The source comments distinguish on-path multipath/RFC9000 validation challenges from off-path n0 NAT-traversal probes. That distinction is important: traversal probes intentionally operate outside the normal validated current path while still feeding into later path opening.

## 4. NAT traversal is transport-integrated state, not an outer helper

The strongest source-level difference inspected is `noq-proto/src/n0_nat_traversal.rs`.

noq's protocol core maintains explicit NAT-traversal state with:

- client/server role-specific state machines
- negotiated enable/disable state
- canonicalized IPv4/IPv6 candidate addresses
- maximum local/remote address counts
- address-add/remove events
- candidate sets
- probing rounds
- per-round attempt counts
- sent PATH_CHALLENGE tokens
- pending off-path probes
- retry scheduling with capped exponential backoff
- successfully probed paths waiting for connection IDs / available PathIds
- conversion between canonical and local socket address families

The source caps NAT probe attempts and documents why: probes may be lost, two probes may be required to open NAT/firewall state, but repeated probes also risk hitting unrelated internet hosts.

A successful off-path response does **not** immediately mark the complete path validated. The comments explicitly note that the traversal probe is not padded to QUIC's normal 1200-byte path-validation size, so it validates reachability/addressing but still requires the path-opening/validation machinery afterward.

That is a strong security/correctness boundary.

## 5. Address exchange is wired into the QUIC frame/state machine

The NAT traversal module references transport frames including:

- `AddAddress`
- `RemoveAddress`
- `ReachOut`
- observed-address reporting

The state machine emits address-added/address-removed events and queues reach-out/probe behavior based on negotiated extension state.

This demonstrates that noq's traversal model is protocol-integrated rather than merely an application exchanging UDP endpoints on a side channel.

For future research, the exact wire-format/versioning status of these frames should be compared against the active IETF QAD/QNT drafts and N0-specific extension identifiers before treating them as interoperable standards work.

## 6. Congestion-controller API has diverged materially

The Quinn and noq `Controller` traits share common ancestry but are no longer identical.

### Quinn current trait surface

Quinn exposes callbacks including:

- `on_sent`
- `on_ack`
- `on_end_acks`
- `on_congestion_event`
- spurious congestion
- MTU updates
- window and metrics
- cloning/downcasting

Quinn's inspected metrics expose congestion window, slow-start threshold, pacing rate and a bandwidth estimate.

### noq additions / differences

noq adds or changes several signals:

- `Controller: ... + Debug`
- **`on_packet_sent`** per individual packet
- **`on_cwnd_limited`** when the sender fully utilizes the congestion window
- packet number passed into `on_ack`
- largest-lost packet number passed into congestion events
- **`on_packet_lost`** per individual loss
- **`on_ack_frequency_update`** with peer ACK-threshold/max-delay information
- controller metrics include **`send_quantum`** used to control burst size/pacing behavior

These additions are consistent with a more BBRv3/ACK-frequency-aware controller integration and explain the August 12 upstream note that syncing Quinn's BBRv3 required adapting around noq's current controller trait rather than simply copying the entire latest Quinn interface.

## 7. Fork synchronization remains active

The source divergence should not be mistaken for total architectural independence.

On August 12, 2026 noq explicitly synchronized BBRv3 from Quinn. The commit states that the newest Quinn controller-related traits would have required a breaking change, so the implementation was imported while adapting the trait implementation to noq's current API.

This is a useful maintenance pattern:

- maintain extension-specific API divergence where necessary
- continue importing upstream algorithms and fixes
- document compatibility boundaries
- avoid gratuitous public API breakage

For a long-lived technical fork, this is healthier than either freezing upstream or repeatedly wholesale-merging incompatible interfaces.

## 8. Path correctness bugs validate the complexity cost

Recent noq fixes reinforce why first-class multipath state needs dedicated invariants and tests.

### Per-path idle timer fix — July 29, 2026

Upstream fixed:

- path timers being set before multipath negotiation
- inconsistent timeout calculation
- incorrect assumptions about reconstructing last-use time from an existing deadline

Timer logic was centralized and constrained to negotiated multipath behavior.

### Unknown-path coalesced datagram fix — August 10, 2026

A coalesced datagram could contain a remainder associated with a PathId that was neither active nor abandoned. The first packet was rejected safely, but later processing reached an assertion that expected a known path and panicked.

Upstream changed the remainder handling to discard the unknown-path tail and added a regression test for a never-opened PathId while preserving coverage for stale abandoned paths.

These are valuable examples of the failure modes introduced when path identity becomes independent from one active socket path.

## 9. MTU architecture: inherited core, multiplied per path

Both projects place `MtuDiscovery` inside path data and couple MTU changes to congestion/pacing behavior.

Quinn's recent maintenance includes path-MTU black-hole recovery correctness. noq retains the same broad MTU-discovery model but its source instantiates MTU discovery inside each `PathData`, meaning simultaneous/migrated paths may maintain different network-route MTU histories.

A future source-level diff should specifically compare:

- black-hole detection reset semantics
- MTU probe packet-number accounting
- whether PathId migration carries or resets MTU knowledge
- interaction with multiple paths sharing one 4-tuple
- controller `on_mtu_update` behavior after path changes

No claim is made here that current Quinn and noq MTU algorithms are behaviorally equivalent.

## 10. Practical reuse interpretation

### Quinn is the stronger reference for

- standardized, mature QUIC transport behavior
- compact path-migration architecture
- deterministic sans-I/O protocol design
- established loss/RTT/MTU behavior
- mature fuzz/performance/testing baseline

### noq is the stronger reference for

- explicit logical path IDs
- simultaneous multipath state
- path-number-space separation from concrete routes
- per-path idle/keepalive/draining lifecycle
- transport-integrated address exchange
- off-path NAT probing feeding into validated path opening
- ACK-frequency/BBRv3-oriented congestion-controller signals
- experimental QUIC traversal architecture for Iroh-style peer connectivity

### Study both for

- long-lived fork maintenance
- congestion-control portability
- migration/path-generation safety
- deciding whether traversal belongs above or inside transport
- designing test invariants for malformed/stale path identifiers

## Security and interoperability caveats

- Multipath/QAD/QNT-related work is evolving; implementation presence does not imply final-standard interoperability.
- NAT traversal intentionally sends probes to candidate addresses, so retry limits and candidate validation are meaningful abuse/safety boundaries.
- Successful lightweight probes do not replace full QUIC path validation.
- A maintained fork can inherit upstream fixes unevenly; both upstream lineages require separate security/release monitoring.
- This dossier does not establish that Iroh or any third-party implementation interoperates with generic Quinn for noq-specific extensions.

## Verification boundary

Performed:

- direct inspection of the current Quinn `PathData` implementation
- direct inspection of noq `PathId`, `PathState`, `PathData`, NAT-traversal state and controller trait
- inspection of recent noq commit history related to BBRv3 sync, multipath timers and unknown-path handling
- comparison against the existing high-level Quinn/noq dossier

Not performed:

- no local source-tree diff
- no compilation
- no unit/integration test execution
- no packet capture
- no draft-protocol conformance suite
- no Quinn↔noq interoperability test
- no multipath/NAT traversal deployment
- no fuzzing or security audit

## Catalog conclusion

The source-level evidence strengthens the existing decision to keep both projects as distinct Gold entries.

- **Quinn:** retain **VERIFIED / S / 29** as the mature baseline/reference Rust QUIC stack.
- **noq:** retain **VERIFIED / S / 28** as the extension-focused fork with concrete multipath, address-discovery/NAT-traversal and richer path/controller machinery.

The next highest-value comparison should move one layer upward into **Iroh's consumption of noq**: identify the exact public noq APIs/events Iroh uses for candidate addresses, path opening, relay-to-direct transitions and connection/path selection, then compare that boundary with Tailscale DERP/direct-path logic and go-libp2p AutoNAT/hole punching.