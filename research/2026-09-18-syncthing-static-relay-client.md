# Syncthing static relay client: connection, trust, and liveness

- **Upstream:** https://github.com/syncthing/syncthing/tree/main/lib/relay/client
- **Primary files:** `static.go`, `methods.go`, `client.go`
- **Category:** networking / relay client / TLS identity / resilient connectivity
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — S
- **License:** MPL-2.0 at the Syncthing repository level
- **Discovery:** recursive follow-up from the Syncthing relay/dialer research chain

## What it does

The static relay client maintains Syncthing's control connection to a specific `relay://` endpoint. It connects through Syncthing's proxy-aware `dialer.DialContext`, wraps the socket in TLS, validates relay protocol/identity, joins the relay, and then services Ping, SessionInvitation, and RelayFull messages.

## Why it matters

This is a compact example of a long-lived control-plane client whose trust model is not ordinary public-Web PKI. The code combines ALPN protocol binding, optional certificate-derived relay identity, bounded connection/message timeouts, application-level ping/pong liveness, context cancellation, and invitation delivery.

## Source evidence

### Connection and join path

`staticClient.connect` accepts only the `relay` URI scheme, creates a context bounded by `connectTimeout`, and calls `dialer.DialContext` for the TCP connection. It clones the TLS config and sets `ServerName` from the relay host so SNI can be sent when a hostname is used. It then applies a connection deadline and calls `performHandshakeAndValidation` before retaining the connection.

After connection, `join` writes a `JoinRelayRequest` containing the optional URI `token`. A successful `Response` must have code zero; `RelayFull` and unexpected messages terminate the join.

### Trust and protocol validation

`configForCerts` supplies client certificates, advertises the relay ALPN protocol, disables session tickets, requires TLS 1.2 or newer, and sets `InsecureSkipVerify: true`. That flag must not be interpreted in isolation: `performHandshakeAndValidation` separately requires the negotiated ALPN protocol to equal the relay protocol name.

If the relay URI includes `id=...`, the value is parsed as a Syncthing DeviceID. The TLS peer must present exactly one certificate; Syncthing derives a DeviceID from that certificate's raw bytes and requires it to equal the URI identity. Thus an identity-bearing relay URI uses certificate-derived DeviceID pinning rather than ordinary Web-PKI hostname verification.

Important caveat: the `id` parameter is optional in this function. When absent, this certificate-ID comparison is skipped. The ALPN requirement remains. Any reuse of this design should make the intended trust policy explicit rather than copying only the TLS configuration.

### Liveness and message handling

After joining, the connection deadline is cleared. A reader goroutine decodes relay protocol messages while the service loop maintains a two-minute message timer. Receiving any message resets that timer. Ping receives Pong; SessionInvitation is forwarded to the invitations channel; RelayFull, protocol errors, read errors, context cancellation, or timer expiry terminate the service.

If an invitation carries an empty or unspecified address, the client substitutes the relay connection's remote IP before publishing the invitation.

### Session connection helper

`GetInvitationFromRelay` uses the same TLS handshake/validation routine before sending a `ConnectRequest` for a target DeviceID. `JoinSession` then dials the invitation's address/port, sends the invitation key in a `JoinSessionRequest`, requires a successful response, clears its temporary deadline, and returns the resulting `net.Conn`.

## Reusable components / patterns

- ALPN-bound application protocol over TLS.
- Certificate-derived application identity pinning.
- Explicit separation between transport TLS configuration and application trust validation.
- Context-bounded dial plus temporary handshake deadline.
- Long-lived control channel with application ping/pong and inactivity timeout.
- Typed control-message dispatch and strict rejection of unexpected messages.
- Invitation handoff through a channel.
- Relay-address fallback when an invitation omits a concrete address.

## Provisional scoring

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Useful relay/control-plane client architecture. |
| Working evidence | 5 | Integrated production source in active Syncthing; source path is complete and connected to relay protocol/dialer layers. |
| Reusability | 4 | Patterns are reusable, but tied to Syncthing protocol/DeviceID types. |
| Novelty | 4 | Certificate-derived DeviceID validation plus ALPN is technically interesting. |
| Documentation | 4 | Source is readable, but behavior is primarily code-defined. |
| Maintenance | 5 | Part of actively maintained Syncthing. |
| **Total** | **27/30** | **S** |

## Licensing

The enclosing Syncthing repository is MPL-2.0. No upstream source is copied into GitHub Gold; this dossier records architecture and evidence only. Component/dependency licensing must be reviewed before extraction or adaptation.

## Verification boundary

GitHub Gold inspected current upstream `static.go`, `methods.go`, `client.go`, and the repository license. GitHub Gold did **not** compile these packages, connect to a live relay, exercise token authentication, verify a real relay certificate/DeviceID, force RelayFull, test inactivity timeout behavior, join a real session, or independently audit the TLS/security model.

## Strong follow-ups

1. Trace platform-specific `ReusePortControl` and actual `SetTCPOptions` call sites.
2. Inspect relay-client tests and determine which handshake/identity/error cases have automated coverage.
3. Trace how relay URIs are produced and whether production/public-pool paths consistently carry `id=` pins.
4. Map reconnection/supervision behavior above `staticClient` through `svcutil`/`suture`.
