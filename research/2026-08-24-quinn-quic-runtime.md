# Quinn QUIC Runtime Research — 2026-08-24

## Candidate

- **Project:** Quinn
- **Repository:** https://github.com/quinn-rs/quinn
- **Author / Org:** quinn-rs
- **Category:** networking / QUIC / async transport / protocol runtime
- **Evidence:** VERIFIED
- **Provisional tier / score:** **S / 29**
- **License:** **MIT OR Apache-2.0**
- **Promotion state:** promotion-ready dossier; do not force into the large queue JSON unless it can be updated losslessly and re-audited.

## Executive finding

Quinn is a mature pure-Rust implementation of IETF QUIC with a deliberately layered architecture: a high-level async API (`quinn`), a deterministic sans-I/O protocol state machine (`quinn-proto`), and a platform UDP/ECN layer (`quinn-udp`). It is especially valuable to GitHub Gold as the stable architectural reference point for evaluating newer transport stacks such as `n0-computer/noq`.

The project states that it began in 2018 and has had more than 30 releases. Upstream currently documents simultaneous client/server operation, ordered and unordered stream reads, application datagrams, pluggable cryptography, stable-Rust support, and testing on Linux, macOS, and Windows.

## Why this is Gold

Quinn exposes several unusually reusable layers rather than one monolithic networking binary:

1. **`quinn`** — futures-based async API built around Tokio for normal application use.
2. **`quinn-proto`** — deterministic QUIC state machine with no internal I/O, suitable for custom runtimes/event loops and potentially non-Rust interfaces.
3. **`quinn-udp`** — UDP socket handling, ECN support, batching and platform-specific transport optimizations.
4. **`bench` / `perf`** — dedicated performance harnesses.
5. **`fuzz`** — protocol fuzz-testing surface.
6. **Examples and documentation** — runnable client/server examples and a networking guide.

This separation makes Quinn useful not only as a dependency, but as a reference implementation for transport-state machines, loss recovery, congestion control, path MTU discovery, stream reassembly, connection-ID management, datagram limits, ECN, cryptographic integration, and reproducible protocol testing.

## Architecture targets worth studying

### High-level async transport API

The `quinn` crate provides endpoint, connection, stream, and datagram abstractions over the lower-level protocol engine. A single endpoint maps to one UDP socket while multiplexing many QUIC connections.

Reusable study targets:

- endpoint/session lifecycle
- bidirectional and unidirectional stream APIs
- application datagrams
- async wakeup/backpressure design
- certificate and crypto configuration
- endpoint-wide UDP buffering behavior

### Sans-I/O protocol engine

`quinn-proto` is the highest-value component architecturally. Upstream describes it as a deterministic QUIC state machine performing no I/O internally.

Study targets:

- packet and frame state machines
- handshake and connection lifecycle
- stream scheduling/reassembly
- loss detection and retransmission
- congestion-control abstraction
- RTT/path statistics
- path MTU discovery and black-hole detection
- connection-ID lifecycle and limits
- deterministic simulated-I/O tests

This layer is the most useful direct comparison point against `noq-proto`.

### UDP / ECN transport layer

`quinn-udp` encapsulates platform UDP behavior and QUIC-specific socket requirements.

Study targets:

- ECN metadata
- send/receive batching
- socket portability
- buffer sizing
- platform-specific acceleration paths
- integration boundary between transport I/O and protocol state

### Testing, fuzzing and performance

The workspace explicitly includes `bench`, `perf`, and `fuzz` members. The README also documents simulated-I/O protocol testing and optional packet/key-log emission for Wireshark inspection.

This makes Quinn a useful reference for how to test timing-sensitive networking logic reproducibly rather than only through live network integration tests.

## Maintenance evidence inspected

Recent upstream changes show active correctness, security, and resource-boundary work rather than superficial churn:

- **2026-08-23:** exposed BBR bandwidth estimates in path statistics.
- **2026-08-20:** fixed path-MTU black-hole detection so ordinary loss after equal-sized successful deliveries does not incorrectly collapse MTU to the minimum; commit includes a regression test and notes existing black-hole tests remain green.
- **2026-08-20:** updated a transitive development/performance dependency after RustSec advisory `RUSTSEC-2026-0258`; upstream notes the published Quinn crates were not affected by that dependency path.
- **2026-08-17:** added total-memory limits for outgoing and incoming application datagram queues.
- **2026-08-17:** tightened connection-ID retirement limit handling.
- **2026-08-17:** bounded stream-assembler chunk counts to close a memory-exhaustion class where many gapped STREAM frames could otherwise grow buffered chunk state excessively.

These are strong maintenance signals because they target protocol correctness, memory exhaustion, loss/MTU behavior, and supply-chain auditing.

## License and reuse boundary

The workspace declares **MIT OR Apache-2.0**. The MIT root license was inspected directly. Reuse should preserve the selected license's notices and attribution requirements.

No third-party source code is copied into GitHub Gold by this dossier.

## Verification performed by GitHub Gold

Inspected:

- official repository metadata
- upstream README
- workspace manifest
- root MIT license
- recent commit history and commit messages
- documented workspace/test/fuzz structure

Not performed:

- no local build
- no benchmark run
- no packet-level interoperability test
- no live QUIC deployment
- no fuzz campaign
- no cryptographic audit
- no review of every platform-specific socket path

Therefore **VERIFIED** means repository-native evidence strongly supports the described architecture and maintenance activity; it does not mean GitHub Gold independently validated QUIC conformance or security.

## Quinn vs noq

Both projects use a layered async + sans-I/O + UDP architecture, but they should remain separate catalog candidates.

### Quinn

- mature baseline IETF QUIC implementation
- more than 30 releases since 2018
- broad production/reference value
- high-level Tokio API + `quinn-proto` + `quinn-udp`
- established loss recovery, MTU, congestion, stream, ECN and fuzzing infrastructure

### noq

- newer N0 transport foundation used by Iroh
- similar separation between async API, sans-I/O protocol core and UDP layer
- adds or actively develops N0-specific/experimental QUIC work such as multipath, address discovery and QUIC NAT-traversal extensions

For GitHub Gold, **Quinn is the mature comparison/control implementation; noq is the experimental extension-focused transport line.** Comparing their protocol cores is more useful than treating one as a duplicate of the other.

## Strong recursive leads

- compare `quinn-proto` path state against `noq-proto`
- compare congestion-control APIs, especially BBR support and path statistics
- inspect QUIC path-MTU discovery and black-hole detection tests
- inspect stream assembler memory bounds and fuzz coverage
- inspect `quinn-udp` batching/ECN portability versus `noq-udp`
- map which Quinn concepts or code ancestry remain inside current N0/noq architecture
- inspect downstream high-scale users for operational integration patterns

## Provisional Gold score

| Axis | Score | Rationale |
|---|---:|---|
| Utility | 5 | General-purpose QUIC transport usable directly or as an architectural reference. |
| Working evidence | 5 | Long release history, CI, regression tests, fuzz/perf surfaces, active fixes. |
| Reusability | 5 | Clean split between async API, sans-I/O core, and UDP layer; permissive dual license. |
| Novelty | 4 | QUIC itself is standardized, but the deterministic sans-I/O architecture is highly valuable. |
| Documentation | 5 | README, guide, examples, API docs and testing notes are strong. |
| Maintenance | 5 | Active August 2026 correctness, resource-boundary and audit work. |
| **Total** | **29 / 30** | **S tier** |

## Promotion recommendation

**VERIFIED / S / 29 — promotion-ready.**

Promote when the canonical catalog or candidate queue can be updated atomically and losslessly. Preserve Quinn and noq as distinct entries and cross-link them as baseline versus extension-focused QUIC implementations.
