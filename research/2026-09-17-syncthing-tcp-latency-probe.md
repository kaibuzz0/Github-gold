# Syncthing TCP latency probe (`lib/osutil/ping.go`)

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/lib/osutil/ping.go
- **Repository:** https://github.com/syncthing/syncthing
- **Category:** networking / endpoint measurement / relay selection primitive
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 24/30 — A tier
- **License:** MPL-2.0, explicitly declared in the source header. No upstream source copied here.
- **Discovery:** Follow-up from the Syncthing dynamic relay-selection dossier.

## What it actually measures

`GetLatencyForURL` parses the supplied URL and passes only `uri.Host` to `TCPPing`. `TCPPing` records the start time, creates a one-second context timeout, calls Syncthing's `dialer.DialContext(ctx, "tcp", address)`, closes the connection on success, and returns elapsed wall-clock time plus any dial error.

Despite the helper name, this is therefore not ICMP ping and it does not measure a relay-protocol, TLS, HTTP, authentication, or application-level round trip. It measures TCP connection-establishment latency to the URL's host/port through Syncthing's dialer abstraction.

This resolves the principal caveat in the preceding `dynamic.go` dossier: dynamic relay ranking is transport-scheme agnostic at this layer. The URL is parsed for its authority, but the URI scheme is not used to choose a scheme-specific probe.

## Operational semantics

- hard per-probe timeout: one second;
- successful probe: TCP connection is immediately closed;
- returned duration includes the TCP dial attempt from immediately before the call through success/failure;
- parse failures return before a network attempt;
- dial failures return elapsed time and the dial error;
- callers such as dynamic relay selection can apply their own failure ranking policy (currently `time.Hour` there).

## Why it matters

This is a small but useful primitive for unprivileged endpoint ranking. The source explicitly explains why TCP is used instead of ICMP: ICMP packets require privileges that cannot be assumed. For portable user-space software, measuring TCP establishment to the actual service port can also be more operationally relevant than raw ICMP reachability.

The design is deliberately narrow. It should not be described as measuring end-to-end relay quality: it says nothing about TLS handshake cost, relay load, session setup, packet loss after connection, sustained throughput, congestion, geographic stability, or application responsiveness.

## Reusable component notes

The useful pattern is conceptual rather than code to copy: parse a service URL, extract the network endpoint, enforce a tight context deadline, measure a real TCP dial, close immediately, and let the higher-level selector decide how failures affect ranking.

Because the function delegates to Syncthing's `dialer.DialContext`, anyone reusing the design should inspect that abstraction before assuming identical behavior to the Go standard library's bare `net.Dialer` in every environment.

## Verification performed

GitHub Gold directly inspected current upstream `lib/osutil/ping.go` and the call site in `lib/relay/client/dynamic.go`. No runtime network probe was performed.

## Caveats

- GitHub Gold did not compile or execute the helper.
- No live relay endpoint was measured.
- No timing accuracy, DNS behavior, IPv4/IPv6 behavior, proxy behavior, cancellation edge cases, or one-second timeout behavior was independently tested.
- This dossier does not yet inspect Syncthing's `lib/dialer` implementation, which is the next layer needed to characterize actual socket dialing behavior.
- A TCP connect metric should not be conflated with application latency or relay throughput.
- MPL-2.0 obligations apply to the upstream source.

## Strong next leads

1. Inspect `lib/dialer` to establish DNS, address-family, socket-option, proxy and platform-specific behavior behind `DialContext`.
2. Inspect `lib/relay/client/static.go` for TLS/device-ID verification and reconnect behavior.
3. Trace dynamic-client reconstruction to establish relay-pool refresh/backoff cadence.
4. Search tests for `GetLatencyForURL`, `TCPPing`, and dynamic relay ranking outside their immediate directories.