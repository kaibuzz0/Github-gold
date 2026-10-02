# Syncthing proxy dialer implementation (`lib/dialer/internal.go`)

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/lib/dialer/internal.go
- **Repository:** https://github.com/syncthing/syncthing
- **Category:** networking / proxy tunneling / SOCKS5 / HTTP CONNECT / HTTPS proxy
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 26/30 — S tier
- **License:** MPL-2.0, explicitly declared in the source header. No upstream source copied here.
- **Discovery:** Follow-up from the Syncthing proxy-aware dialer dossier.

## What it implements

Syncthing extends `golang.org/x/net/proxy` by registering three URL schemes: `socks`, `http`, and `https`. SOCKS uses `proxy.SOCKS5` and accepts URL user-info credentials. HTTP and HTTPS use a custom CONNECT dialer.

At package initialization, `proxy.FromEnvironment()` determines whether proxy settings exist. When a proxy is detected, Syncthing replaces `http.DefaultTransport` with a transport whose `DialContext` is the package's proxy-aware dialer while retaining `http.ProxyFromEnvironment`; the transport also sets a ten-second TLS handshake timeout.

The environment variable `ALL_PROXY_NO_FALLBACK` disables the direct fallback behavior documented in the companion `public.go` dossier whenever it is non-empty.

## HTTP/HTTPS CONNECT path

The custom HTTP proxy dialer accepts only `tcp`, `tcp4`, or `tcp6` requests. It first connects to the proxy through its forward dialer. If the context has a deadline, that deadline is temporarily applied to the proxy connection.

For an `https` proxy URL, the connection to the proxy is wrapped in TLS and explicitly performs `HandshakeContext`; `ServerName` is set from the proxy hostname, so ordinary TLS hostname/certificate verification remains enabled for this proxy hop.

The dialer then writes an HTTP CONNECT request targeting the requested destination. A non-200 response is rejected and the connection is closed.

Because `http.ReadResponse` may buffer bytes beyond the CONNECT response, successful connections are returned through `bufferedConn`, whose `Read` method consumes the existing buffered reader before falling through to the embedded connection. This is a small but important reusable tunneling detail.

## Authentication behavior

When user-info is present on an HTTP/HTTPS proxy URL, Syncthing emits a `Proxy-Authorization: Basic ...` header. For cleartext `http` proxies it logs a warning once that Basic authentication is being used over cleartext transport. HTTPS proxies protect the proxy hop with TLS before the CONNECT request and authorization header are sent.

SOCKS credentials are supplied to `proxy.SOCKS5` as username/password authentication.

This is authentication to the configured proxy, not authentication to the ultimate Syncthing peer or relay.

## Logical remote-address wrapper

Proxy-created connections naturally report the proxy itself through `RemoteAddr()`. Syncthing's `dialerConn` wrapper overrides this with the intended logical destination address. The source comment identifies LAN classification and relay-invitation address derivation as reasons this distinction matters.

`newDialerAddr` attempts to resolve the logical address to an IP address and falls back to a lightweight network/address representation if resolution fails.

## Why it matters

This file completes the implementation picture behind the previous `DialContext` dossier: Syncthing has a compact proxy subsystem supporting SOCKS5 and HTTP CONNECT, optional TLS to HTTPS proxies, proxy authentication, context deadlines, buffered CONNECT handoff, logical destination addressing, and an explicit environment switch controlling direct fallback.

The design is reusable conceptually for local-first/offline-capable applications that need proxy support without allowing proxy plumbing to leak incorrect endpoint identity into higher networking layers.

## Verification performed

GitHub Gold directly inspected current upstream `lib/dialer/internal.go` and connected it to the previously inspected `lib/dialer/public.go` behavior. No proxy server, authentication exchange, TLS handshake, CONNECT tunnel, environment configuration, or fallback path was executed by GitHub Gold.

## Caveats

- Source inspection establishes implementation structure, not runtime interoperability with particular proxy products.
- The `socks` scheme is implemented using SOCKS5; this dossier does not claim SOCKS4 support.
- Cleartext HTTP proxy Basic credentials are only base64-encoded and Syncthing explicitly warns about that case.
- Environment-variable parsing semantics ultimately include behavior from `golang.org/x/net/proxy` and Go's HTTP proxy handling; this dossier does not enumerate every accepted variable/NO_PROXY edge case.
- Replacing `http.DefaultTransport` can affect package-level HTTP clients that use the default transport; call-site consequences were not exhaustively traced.
- MPL-2.0 obligations apply to upstream source.

## Strong next leads

1. Inspect platform-specific `ReusePortControl` implementations and document OS support/failure semantics.
2. Trace `SetTCPOptions` and `SetTrafficClass` call sites to establish where socket policies are actually applied.
3. Inspect tests covering HTTP CONNECT/proxy behavior, if present, to raise or lower Working Evidence.
4. Continue into `lib/relay/client/static.go` for reconnect and relay certificate/DeviceID validation.