# Syncthing dialer proxy/fallback abstraction (`lib/dialer/public.go`)

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/lib/dialer/public.go
- **Repository:** https://github.com/syncthing/syncthing
- **Category:** networking / proxy-aware dialing / connection racing / socket policy
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — S tier
- **License:** MPL-2.0, explicitly declared in the source header. No upstream source copied here.
- **Discovery:** Follow-up from the Syncthing TCP latency-probe dossier.

## What the abstraction actually does

`DialContext` is not simply an alias for Go's `net.Dialer`. It calls `dialContextWithFallback` with `proxy.Direct` as the fallback and checks `golang.org/x/net/proxy.FromEnvironment()` first.

If no proxy is configured, it dials directly. If a proxy is configured and fallback is disabled, it uses only the proxy. If a proxy is configured and fallback is allowed, Syncthing races a proxy connection against the direct fallback using `dialTwicePreferFirst`.

The first path is preferred rather than merely the fastest path. The fallback attempt is delayed: normally by one second, or by one third of the remaining context deadline when a deadline exists. If the preferred path succeeds before that delay, the second path is not attempted. If the preferred path is still unresolved when the delay expires, the fallback begins in parallel. If the first path later succeeds, it wins and any successful second connection is closed asynchronously. Only if the first path fails does the function wait for and return the fallback result.

For proxy connections, Syncthing wraps the returned connection in `dialerConn` so the logical network/address can be retained instead of exposing only the proxy endpoint's addressing.

## Why this changes the prior latency finding

The preceding `TCPPing` dossier correctly established that relay ranking measures a TCP dial rather than ICMP/TLS/application latency. This inspection adds an important qualification: the TCP dial is performed through Syncthing's proxy-aware dialer.

Therefore, when a proxy is configured, the measured duration can represent proxy-mediated connectivity and may involve a delayed direct fallback. It should not universally be described as a bare direct TCP SYN/handshake measurement from the host to the relay.

## Reuse-port dialing

`DialContextReusePortFunc` adds another useful strategy for discovery/connection code. When no proxy is configured and a compatible unspecified TCP listen address exists in Syncthing's connection registry, it constructs a `net.Dialer` using that local address plus `ReusePortControl`.

It then races that preferred reuse-port dial against an ordinary non-reuse dial. This protects against routing behavior where binding/reusing the listening address might make the destination unreachable. When a proxy is configured, the reuse-port strategy is bypassed and ordinary `DialContext` is used.

## TCP policy helpers

`SetTCPOptions` recursively unwraps `dialerConn` and, for TCP connections, configures:

- linger = 0;
- Nagle enabled (`SetNoDelay(false)`);
- TCP keepalive period = 60 seconds;
- TCP keepalive enabled.

`SetTrafficClass` likewise unwraps proxy wrappers and attempts to apply IPv4 TOS / IPv6 traffic class settings.

These helpers are separate from `DialContext`; inspecting them does not prove every dialed socket receives these options. Call sites must be checked before making that claim.

## Verification performed

GitHub Gold directly inspected current upstream `lib/dialer/public.go` and connected it to the previously inspected `lib/osutil/ping.go` call path. No runtime dial, proxy, reuse-port, socket-option, or address-family test was performed.

## Caveats

- No proxy environment was configured or tested by GitHub Gold.
- The exact proxy schemes and environment parsing behavior live in `proxy.FromEnvironment` and related internal implementation and are not fully characterized here.
- DNS resolution and Happy-Eyeballs/address-family behavior ultimately depend on the selected underlying dialer and Go networking stack; this dossier does not claim a complete resolver trace.
- `dialTwicePreferFirst` intentionally prefers the first strategy, not whichever connection finishes first.
- The one-second fallback delay can shrink to one third of a shorter context deadline.
- Reuse-port behavior is platform-dependent through `ReusePortControl` and requires separate inspection.
- MPL-2.0 obligations apply to upstream source.

## Strong next leads

1. Inspect `lib/dialer/internal.go` and proxy initialization to map supported proxy types, authentication behavior, environment variables, and `noFallback` configuration.
2. Inspect platform-specific `ReusePortControl` implementations and their OS support/failure semantics.
3. Trace call sites of `SetTCPOptions` to distinguish default policy helpers from options actually applied to relay/device connections.
4. Revisit the relay-latency dossier with this proxy/fallback qualification when canonical promotion occurs.