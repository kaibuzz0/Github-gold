# Quinn ↔ noq QUIC Architecture Comparison — 2026-08-24

## Purpose

This dossier compares the already researched `quinn-rs/quinn` and `n0-computer/noq` projects at the architectural level. It is not a new candidate promotion. The goal is to make the catalog more useful by documenting where the two codebases overlap, where `noq` intentionally diverges, and which components are most valuable to study or reuse.

## Executive finding

`noq` is not an unrelated QUIC implementation competing with Quinn from scratch. Upstream explicitly states that it **started as a fork of Quinn** and retained the same broad layering pattern: an async-friendly top-level crate, a sans-I/O protocol core, and a UDP transport layer.

The important distinction is direction of development:

- **Quinn** is the mature baseline/reference implementation of IETF QUIC, with a long release history and a deliberately conservative core focused on standardized QUIC behavior, deterministic protocol testing, loss recovery, congestion control, stream handling, ECN and platform UDP behavior.
- **noq** keeps that architectural ancestry but is being developed toward newer QUIC extension work, especially **Multipath QUIC**, **QUIC Address Discovery (QAD)** and **QUIC NAT Traversal (QNT)**.

For GitHub Gold, the best use is therefore not to choose one and discard the other. Quinn is the control/reference implementation; noq is the extension-oriented branch that exposes how a mature QUIC core changes when path identity, path migration and NAT traversal become first-class protocol concerns.

## Shared architectural ancestry

### Async API over a sans-I/O protocol engine

Both projects separate normal application-facing async networking from protocol-state processing.

**Quinn** documents:

- `quinn` — Tokio/futures-oriented async API
- `quinn-proto` — deterministic state machine with no internal I/O
- `quinn-udp` — UDP sockets, ECN metadata and protocol-tuned socket behavior

**noq** documents:

- `noq` — async-friendly public API
- `noq-proto` — sans-I/O protocol implementation
- corresponding UDP/runtime support in the workspace

This is a strong reusable pattern: protocol correctness can be exercised deterministically without coupling it to live sockets or wall-clock sleeps, while the outer runtime layer handles wakeups, sockets and platform integration.

## Where Quinn is the stronger reference

### Maturity and stable baseline

Quinn dates to 2018 and upstream reports more than 30 releases. Its documented scope covers standardized QUIC, application datagrams, ordered/unordered stream reads, pluggable cryptography, endpoint multiplexing and broad desktop testing.

This makes Quinn the better baseline for understanding:

- normal single-path QUIC connection lifecycle
- stream scheduling and reassembly
- loss detection and retransmission
- RTT accounting
- congestion-control interfaces
- path-MTU discovery and black-hole recovery
- connection-ID lifecycle
- ECN and UDP batching
- deterministic protocol tests
- fuzz/performance harness design

Recent Quinn maintenance inspected for the existing dossier also includes memory bounds on datagram queues and stream reassembly, MTU black-hole correctness and connection-ID limit handling. Those are useful examples of hardening mature transport code against resource exhaustion and subtle network-path behavior.

## Where noq intentionally extends the model

### Multipath QUIC

noq explicitly lists the IETF Multipath QUIC draft as a development focus. This changes a fundamental assumption present in conventional QUIC implementations: a connection may need to maintain multiple simultaneously meaningful paths rather than treating path migration primarily as movement from one active path to another.

Recent noq maintenance shows the resulting complexity directly:

- per-path idle timers are armed only after multipath negotiation
- timer computation was centralized to avoid inconsistent path timeout handling
- coalesced datagrams referring to paths that were never opened are discarded instead of reaching an internal `known path` assertion
- regression tests cover both never-opened and abandoned-path cases

These are exactly the kinds of path-lifecycle edge cases worth studying when evaluating multipath protocol designs.

### QUIC Address Discovery (QAD)

noq also targets the QUIC Address Discovery draft. At a high level, QAD gives endpoints a protocol-level mechanism for learning address information that can be useful to path establishment and traversal logic.

For GitHub Gold, the valuable architectural question is not merely the draft itself, but how address discovery is represented inside the transport state machine:

- how discovered addresses enter path state
- how they are validated before use
- how they interact with connection IDs
- how stale/disallowed paths are retired
- how events are surfaced to the outer async layer

These are strong follow-up targets for source-level inspection.

### QUIC NAT Traversal (QNT)

noq explicitly lists the QUIC NAT Traversal draft as another development focus. This is particularly relevant because noq is used beneath the Iroh networking ecosystem, where direct peer connectivity and NAT traversal are core product requirements.

The main architectural value is that NAT traversal behavior can move closer to the QUIC transport/path model rather than being implemented entirely as an unrelated side channel around QUIC.

Follow-up study targets:

- endpoint/address candidate exchange
- simultaneous path establishment
- validation and anti-spoofing boundaries
- interaction with multipath
- fallback behavior when traversal fails
- how Iroh consumes resulting path events

## Congestion control: divergence with continued upstream flow

A useful maintenance signal is that noq is not simply drifting away from Quinn. On **2026-08-12**, noq synchronized **BBRv3** work from Quinn.

The noq commit notes that Quinn's latest controller-related traits would require a breaking API change, so noq imported the BBRv3 implementation while adapting it to the current noq trait surface. This shows a practical fork-maintenance pattern:

1. retain upstream algorithm improvements,
2. isolate API incompatibility at the adapter boundary,
3. postpone unnecessary public breakage,
4. keep future re-synchronization feasible.

This is valuable beyond QUIC: it is a concrete example of maintaining a feature-focused fork without unnecessarily severing upstream lineage.

## Path state and timer correctness

The most concrete noq-specific correctness work inspected in this pass centers on path lifecycle.

### Per-path idle timers

A July 29 fix corrected multiple issues in per-path idle-timer handling:

- timers were being set before multipath negotiation
- timeout calculation differed between code paths
- the previous logic attempted to reconstruct elapsed path-idle time from a deadline that did not actually preserve the original last-use instant

The fix moved logic into a shared helper and constrained the timer to negotiated multipath operation.

### Unknown-path coalesced datagrams

An August 10 fix addressed a panic where the remainder of a coalesced QUIC datagram could reference a path ID that existed in neither active nor abandoned path state. The first packet was handled gracefully, but the coalesced tail reached an assertion expecting a known path.

The fix discards that remainder and adds a regression test reproducing the never-opened-path case. This is strong evidence that noq's multipath work is being exercised against malformed/stale path-state transitions rather than only happy-path demos.

## UDP / portability observations

Both projects retain a distinct UDP/platform layer, but noq's recent history also shows portability tradeoffs. A July 29 change disabled `SO_TIMESTAMPNS` because the implementation was broken on musl and the project did not rely on it.

This is a useful engineering signal: optional kernel/socket metadata should not be allowed to destabilize a cross-platform transport when the higher-level protocol does not require it. The follow-up note that musl should be exercised in CI is also a clear testing lead.

## Supply-chain and maintenance discipline

On August 20, noq hardened repository dependency handling by:

- enforcing locked Cargo dependency resolution
- pinning GitHub Actions versions
- adding Dependabot cooldown behavior
- adding `zizmor` / action-pinning checks

On August 24, upstream also removed an unmaintained internal book rather than leaving stale documentation discoverable. This is a positive repository-hygiene signal: documentation that is no longer maintained can be worse than no documentation when it teaches obsolete protocol behavior.

## Direct comparison table

| Area | Quinn | noq | GitHub Gold interpretation |
|---|---|---|---|
| Origin | Independent QUIC project founded 2018 | Forked from Quinn | Shared ancestry should be documented, not hidden |
| High-level API | `quinn` | `noq` | Similar async application layer |
| Protocol core | `quinn-proto` sans-I/O | `noq-proto` sans-I/O | Best direct comparison surface |
| UDP layer | `quinn-udp` | corresponding noq UDP layer | Compare ECN, batching and portability changes |
| Baseline QUIC | Mature/reference focus | Retained | Quinn is the control implementation |
| Multipath | Not a headline README feature | Explicit draft focus | Major noq differentiation |
| Address Discovery | Not a headline README feature | Explicit QAD focus | noq path-establishment extension |
| QUIC NAT Traversal | Not a headline README feature | Explicit QNT focus | Strong relevance to Iroh direct-connect architecture |
| Congestion control | Active BBR work | Syncs BBRv3 from Quinn | Evidence that upstream flow remains alive |
| Testing value | Mature deterministic protocol/fuzz/perf surfaces | Regression work around multipath/path state | Study both together |
| License | MIT OR Apache-2.0 | MIT OR Apache-2.0 | Clean permissive reuse paths in both |

## Reuse / research guidance

### Prefer Quinn when

- a stable general-purpose Rust QUIC implementation is needed
- standardized QUIC behavior is the primary goal
- mature baseline behavior matters more than experimental extensions
- studying deterministic sans-I/O protocol testing, MTU/loss handling or established transport hardening

### Study noq when

- multipath is a core requirement
- QUIC-native address discovery is relevant
- direct peer/NAT traversal is central to the application
- investigating how Quinn's architecture evolves under multi-path state
- studying a maintained fork that continues to import selected upstream improvements

### Study both together when

- evaluating congestion-control changes
- designing a custom sans-I/O transport core
- understanding path lifecycle and migration
- building peer-to-peer systems such as Iroh
- deciding whether a feature belongs in the transport layer or an application-level traversal layer

## Verification performed

This comparison is grounded in:

- upstream Quinn README and the existing Quinn dossier
- upstream noq README
- recent noq commit history
- documented noq multipath/QAD/QNT scope
- noq's explicit statement that it began as a Quinn fork
- recent BBRv3 synchronization from Quinn
- path-timer and unknown-path regression-fix commit evidence

Not performed:

- no local diff of every Quinn/noq source file
- no build or benchmark
- no network interoperability test
- no multipath deployment
- no NAT traversal experiment
- no cryptographic audit

Therefore this dossier compares repository-native architecture and maintenance evidence; it does not claim behavioral equivalence or protocol-conformance results.

## Catalog conclusion

Keep **both Quinn and noq** as separate Gold entries.

- **Quinn:** mature baseline/reference QUIC runtime — **VERIFIED / S / 29** from its existing dossier.
- **noq:** extension-focused QUIC runtime — retain its existing **VERIFIED / S / 28** assessment.

The strongest next source-level pass should inspect `quinn-proto` and `noq-proto` side by side for:

1. path representation and path-ID lifecycle,
2. congestion-controller trait differences,
3. MTU/black-hole handling,
4. multipath scheduling,
5. QAD/QNT frame and event flow,
6. UDP metadata/ECN boundaries,
7. what Iroh consumes from noq that cannot be expressed by baseline Quinn.
