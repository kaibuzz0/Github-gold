# Syncthing `strelaysrv/session.go` — relay session lifecycle and backpressure

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/cmd/strelaysrv/session.go
- **Parent project:** https://github.com/syncthing/syncthing
- **Category:** networking / peer-to-peer / relay infrastructure / reusable server patterns
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 — S tier
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Language:** Go
- **Component license:** MIT (`cmd/strelaysrv/LICENSE`); imported Syncthing packages must still be reviewed independently before extraction.

## What it is

`session.go` is the data-plane session manager behind Syncthing's relay server. It turns a relay rendezvous into a paired bidirectional byte proxy and contains compact, reusable patterns for capability-style session admission, bounded waiting, connection cleanup, traffic accounting and combined per-session/global bandwidth limiting.

## Direct source evidence

### Unpredictable one-use invitation keys

`newSession` generates two independent 32-byte keys with `crypto/rand`: one for the server-side participant and one for the client-side participant. Both keys initially map to the same session in `pendingSessions`.

`findSession` performs lookup while holding the session mutex and immediately deletes the presented key before returning the session. This gives each side a single-use admission token at this layer: a successfully consumed key cannot be looked up a second time.

The client and server invitation messages carry their respective key, the configured relay session address/port and a `ServerSocket` role flag. Each invitation identifies the opposite DeviceID in `From`.

### Pairing and timeout lifecycle

A session owns an unbuffered `connsChan`. `AddConnection` uses a non-blocking send, so it accepts a connection only while `Serve` is actively ready to receive it.

`Serve` waits for two connections or `messageTimeout`. After the second connection arrives it closes the connection channel and launches two proxy goroutines, one for each direction. The session is then recorded in `activeSessions` until both proxy directions return.

Cleanup removes both still-pending invitation keys, removes the session from `activeSessions`, and closes all collected connections. The source explicitly anticipates repeated connection closes during overlapping termination paths.

`dropSessions(DeviceID)` can terminate active sessions involving a disconnected participant, while `hasSessions` checks whether a participant currently belongs to an active session.

### Bidirectional proxy and failure behavior

Each proxy direction has its own loop and fixed `networkBufferSize` buffer. Before each read and write, the relay installs a `networkTimeout` deadline. A read or write error returns from that direction. `Serve` waits for both directions before final cleanup; closing the session connections provides the mechanism for unwinding the peer direction when cleanup is triggered externally.

Traffic is counted globally with atomics: `numProxies` tracks live directional proxy loops and `bytesProxied` counts bytes read for forwarding.

### Bandwidth limiting and backpressure

The session may have a per-session `rate.Limiter` and a shared global limiter. `makeRateLimitFunc` specializes the hot-path callback for four cases: no limiter, global only, session only, or both.

When both apply, `take` determines the smallest supported burst across the limiters, divides traffic into chunks no larger than that burst, reserves each chunk against every limiter, and sleeps for the longest required delay. This means a chunk must satisfy both the session and global traffic budgets.

The limiter is applied after a source read and before the destination write. Consequently, throttling naturally delays forwarding and eventually pushes back into socket reads as buffers fill; it is not an unbounded application-level queue.

## Why it matters

The component is small enough to study as a reference architecture yet contains several useful server-side primitives:

- cryptographically random per-participant rendezvous capabilities;
- consume-on-lookup admission tokens;
- two-party connection pairing;
- explicit pending-to-active session state;
- bounded join lifetime;
- participant-driven session teardown;
- symmetric full-duplex forwarding;
- read/write deadlines;
- global atomic telemetry;
- composable session + service-wide token-bucket limits;
- deterministic cleanup of pending and active state.

These patterns are potentially reusable in legitimate private relay services, peer-to-peer rendezvous systems, temporary tunnels and constrained forwarding services.

## Caveats / risks

- This file is only one part of the relay trust boundary. Authentication, TLS/ALPN, DeviceID checks and protocol framing live elsewhere and must not be inferred from `session.go` alone.
- The invitation keys are capability tokens; confidentiality of their delivery matters.
- `AddConnection` is intentionally non-blocking and can reject a connection when the serving goroutine is not ready.
- The limiter sleeps in the forwarding path. This is straightforward backpressure, not a sophisticated fairness scheduler.
- The code uses shared process-global session maps/slices guarded by one RWMutex; scalability should be benchmarked rather than assumed.
- MIT applies to `cmd/strelaysrv`, but imports from other Syncthing directories can have different licensing. Review dependencies before copying/extracting code.

## Verification performed

Performed direct source inspection of current upstream `cmd/strelaysrv/session.go` and its component license. Verified from source structure the random key generation, pending-key insertion/consumption, two-connection pairing, timeout cleanup, active-session tracking, bidirectional proxy loops, deadlines, atomic counters and combined limiter behavior.

## Not verified

GitHub Gold did **not** compile or run `strelaysrv`, execute tests, establish a real relay session, benchmark throughput/fairness, inject malformed or duplicate invitation keys, simulate half-closed sockets, measure mutex contention, or independently security-audit the implementation.

## Discovery provenance

Recursive follow-up from the existing Syncthing `strelaysrv` and `lib/relay` dossiers. This was the strongest explicit next lead from the preceding relay-protocol research run.

## Strong next leads

1. Trace the protocol handler that calls `findSession`/`AddConnection` to establish the exact key-validation and socket-handoff sequence.
2. Inspect tests around duplicate keys, join timeout, half-close and failed writes.
3. Inspect `lib/relay/client/dynamic.go` for relay discovery/selection and failover policy.
4. Map Syncthing's direct-vs-relay dial decision path end-to-end.
5. Compare this capability-token rendezvous design with TURN allocations/permissions and other standardized relay architectures without assuming semantic equivalence.
