# Syncthing `lib/relay/protocol` + `lib/relay/client` — Relay Protocol and Client Library

- **Upstream:** https://github.com/syncthing/syncthing/tree/main/lib/relay
- **Author / Org:** Syncthing Project
- **Category:** peer-to-peer infrastructure / relay protocol / networking library / NAT traversal
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27 / 30 — S
- **Scoring:** Utility 5; Working Evidence 5; Reusability 4; Novelty 4; Documentation 4; Maintenance 5
- **Discovery:** recursive follow-up from the Syncthing `strelaysrv` dossier.

## What it is

Syncthing's `lib/relay/protocol` defines the wire messages used to register with a relay, request a peer connection, broker a session and maintain relay liveness. `lib/relay/client` implements the client-side negotiation and turns a successful relay invitation into a normal `net.Conn` that higher layers can use as the session transport.

This is more reusable than treating `strelaysrv` as a black box: it exposes a compact example of a rendezvous-assisted relay protocol with explicit framing, identity-aware TLS negotiation, bounded control messages, invitation brokering and a clean handoff from control plane to data-plane connection.

## Protocol framing

`protocol.go` uses a fixed header containing:

- magic value `0x9E79BC40`;
- signed 32-bit message type;
- signed 32-bit payload length.

Payloads are XDR encoded. `ReadMessage` rejects a wrong magic value and rejects negative or greater-than-1024-byte control payload lengths before allocating/reading the payload. The protocol currently recognizes Ping, Pong, JoinRelayRequest, JoinSessionRequest, Response, ConnectRequest, SessionInvitation and RelayFull.

The protocol name advertised through TLS ALPN is `bep-relay`.

An explicit backward-compatibility path accepts a zero-length legacy JoinRelayRequest, representing the older protocol form before the token field existed.

## Message model

The current packet definitions expose a small state vocabulary:

- `JoinRelayRequest { Token }` registers a client with a relay;
- `ConnectRequest { ID }` asks a relay for a path to a target device ID;
- `SessionInvitation { From, Key, Address, Port, ServerSocket }` brokers the connection parameters;
- `JoinSessionRequest { Key }` presents the invitation/session key to the session endpoint;
- `Response { Code, Message }` communicates success/failure;
- Ping/Pong maintains liveness;
- RelayFull tells a client the relay cannot accept it.

Known response codes include success, not-found, already-connected, wrong-token and unexpected-message.

## Client negotiation

`lib/relay/client` exposes a `RelayClient` abstraction and supports static `relay://` endpoints plus dynamic HTTP/HTTPS relay discovery clients.

For a static relay, the client:

1. opens TCP to the relay;
2. performs TLS with ALPN `bep-relay` and TLS 1.2 minimum;
3. optionally verifies the relay certificate-derived device ID against the `id=` value in the relay URI;
4. sends JoinRelayRequest, including an optional token;
5. expects a successful Response;
6. remains connected, answers Ping with Pong and publishes SessionInvitation messages to an invitation channel;
7. treats RelayFull, protocol errors, reader failures and a two-minute message timeout as disconnect conditions.

For an outbound connection request, `GetInvitationFromRelay` opens a relay control connection, validates the handshake, sends ConnectRequest for a target DeviceID and expects either a SessionInvitation or an error Response.

`JoinSession` then dials the invitation's advertised address/port, sends JoinSessionRequest containing the invitation key, requires a successful Response and returns the resulting socket as `net.Conn`. At that point the relay control protocol has done its job and the established connection can carry the higher-level peer session.

If an invitation contains an unspecified address, the client substitutes the relay connection's remote IP. This lets the relay communicate a port/session key while allowing the client to infer the reachable relay-side address.

## Identity and TLS boundary

The client TLS configuration deliberately uses `InsecureSkipVerify`, so normal Web-PKI hostname verification is not the trust mechanism. When a relay URI contains `id=`, `performHandshakeAndValidation` derives a Syncthing DeviceID from the relay's single presented certificate and compares it to the URI identity. It also requires ALPN negotiation to resolve to `bep-relay`.

That distinction matters for reuse: callers should preserve certificate-ID pinning when using identity-bearing relay URIs rather than assuming conventional CA validation occurs.

## Working evidence

Evidence inspected directly in current upstream source:

- `lib/relay/protocol/protocol.go` implements bounded message framing and parsing;
- `lib/relay/protocol/packets.go` defines the complete current control-message model and drives generated XDR code;
- `lib/relay/client/client.go` defines the RelayClient interface and static/dynamic client selection;
- `lib/relay/client/static.go` implements long-lived relay registration, liveness, invitation delivery, ALPN and certificate-ID validation;
- `lib/relay/client/methods.go` implements invitation lookup, session joining and a relay connectivity test helper;
- the library is consumed by the actively maintained Syncthing relay/server ecosystem cataloged in the adjacent dossiers.

This supports VERIFIED at the source-evidence level. GitHub Gold did not independently execute the protocol or client.

## License

No dedicated `lib/relay/protocol/LICENSE` was found. The Syncthing repository root is **Mozilla Public License 2.0**, so these library files should be treated as MPL-2.0-covered unless a more specific applicable notice is identified. This differs from `cmd/strelaysrv`, which has its own MIT license.

Do not assume the MIT license on the relay executable automatically extends to these imported library packages. Any extraction or adaptation should preserve applicable MPL notices and satisfy MPL source-form obligations.

No upstream source was copied into GitHub Gold.

## Caveats / risks

- This is a Syncthing-specific relay protocol, not a generic standardized relay protocol.
- The control-message maximum is 1024 bytes; applications adapting the design need their own bounds and compatibility policy.
- `InsecureSkipVerify` is intentional only because Syncthing can perform its own certificate-derived identity check; copying that TLS configuration without the corresponding validation would remove an important trust boundary.
- A relay URI without an identity parameter does not receive the same certificate-ID pinning check.
- Session invitations contain key/address/port material and should be treated as security-sensitive ephemeral control data.
- Static and dynamic relay selection have different operational paths and deserve separate failure-mode analysis.

## Verification boundary

GitHub Gold inspected current framing, packet definitions, static-client lifecycle, invitation/session methods and root licensing. It did **not** compile the packages, execute relay tests, capture packets, fuzz XDR parsing, connect two real Syncthing devices through a relay, test malformed messages, validate dynamic relay selection, or independently audit the cryptography/protocol security.

## Why it is Gold

The value is architectural and directly reusable as a reference design: a very small control protocol brokers connectivity while leaving the actual data session on a normal socket. It combines bounded binary framing, backward compatibility, explicit error messages, ALPN, certificate-derived service identity, liveness, invitation channels and a simple session-key handoff. Together with `strelaysrv`, it provides enough source evidence to study both sides of a production relay architecture instead of cataloging only an executable.

## Strong next leads

1. Inspect `cmd/strelaysrv/session.go` to map invitation-key lifecycle, session pairing and byte-copy/backpressure behavior end to end.
2. Inspect `lib/relay/client/dynamic.go` and relay-pool selection logic.
3. Locate relay protocol/unit/fuzz tests and determine malformed-frame coverage.
4. Trace how Syncthing proper decides direct versus relay-assisted dialing.
5. Build a concise control-plane sequence diagram: register -> connect request -> invitation -> join session -> data relay.
6. Compare the design with TURN and other standardized relay/rendezvous approaches without conflating their trust models.