# Syncthing relay production handoff into normal BEP connections

- **Upstream:** https://github.com/syncthing/syncthing
- **Primary files:** `lib/connections/relay_dial.go`, `lib/connections/relay_listen.go`, `lib/connections/structs.go`, `lib/connections/service.go`
- **Category:** peer-to-peer networking / relay transport / TLS / connection orchestration
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 (S)
- **License:** MPL-2.0 for the inspected `lib/connections` source files
- **Discovery:** recursive follow-up from the relay session-join dossier

## Finding

The production relay path does not stop at `JoinSession`. Both outgoing relay dials and incoming relay invitations turn the joined relay data socket into the same `internalConn` abstraction consumed by Syncthing's common connection service.

### Outgoing relay dial

`relayDialer.Dial`:

1. calls `client.GetInvitationFromRelay` for the target DeviceID;
2. calls `client.JoinSession` with the invitation;
3. applies `dialer.SetTCPOptions` and attempts `SetTrafficClass`;
4. chooses `tls.Server` or `tls.Client` from the invitation's `ServerSocket` role;
5. performs `tlsTimedHandshake`;
6. returns `newInternalConn(..., connTypeRelayClient, false, wanPriority)`.

Thus the relay is a transport for an end-to-end peer TLS connection; the post-join socket is not handed directly to BEP in plaintext.

### Incoming relay invitation

`relayListener.handleInvitations` consumes invitations from the relay client, calls `JoinSession`, applies TCP options / traffic class, assigns the TLS client/server role from `ServerSocket`, performs the timed TLS handshake, then sends `newInternalConn(..., connTypeRelayServer, false, ConnectionPriorityRelay)` into the connection service's shared `conns` channel.

The listener also checks the active relay URI every ten seconds and notifies the connection service if a dynamic relay client has moved to another relay.

### Common connection pipeline

`internalConn` wraps the TLS connection with transport type, locality, priority, establishment time, and later a connection ID. Relay client/server types both report transport `relay`.

The service creates one common `conns chan internalConn` and runs `handleConns` and `handleHellos` alongside the dial loop. Once a relay connection reaches `handleConns`, it follows the same post-transport path as TCP/QUIC connections:

- inspect TLS connection state / negotiated BEP protocol;
- require exactly one peer certificate and derive the remote DeviceID from its raw certificate;
- reject self-connections and perform early policy/priority checks;
- exchange Syncthing Hello messages with a bounded deadline;
- call the model's `OnHello` policy hook;
- verify the configured certificate name;
- install read/write rate limiters;
- create `protocol.NewConnection(...)`;
- account for the connection and call `model.AddConnection`.

This establishes the production handoff chain:

`relay invitation -> JoinSession -> socket options -> peer TLS -> internalConn -> certificate/DeviceID checks -> Hello -> protocol.NewConnection -> model.AddConnection`

## Why it matters

This is a reusable architecture pattern for transport abstraction. Relay, direct TCP, and QUIC converge on a small authenticated connection object before application-protocol setup. Transport-specific rendezvous is separated from peer identity, policy checks, Hello negotiation, rate limiting, and protocol construction.

The TLS role is explicitly coordinated by the relay invitation's `ServerSocket` bit, allowing two peers that both made outbound relay connections to deterministically choose complementary TLS roles after the relay pairs them.

## Verification boundary

Verified by static inspection of current upstream source. GitHub Gold did **not** build Syncthing, establish a live relay connection, run the TLS/BEP exchange, transfer files, benchmark the relay path, or independently security-audit the implementation.

The source shows the intended production path and upstream implementation evidence; it is not an independent runtime test by GitHub Gold.

## Licensing / reuse

The inspected `lib/connections` files carry MPL-2.0 notices. No upstream code was copied into GitHub Gold. Any extraction or adaptation requires file-level MPL compliance and separate review of imported components.

## Follow-up

1. Inspect automated tests around `relayDialer`, `relayListener`, `handleConns`, and Hello exchange to determine the actual automated coverage of this end-to-end handoff.
2. Trace `tlsCfg` construction to document peer certificate verification semantics and ALPN configuration precisely.
3. Inspect `protocol.NewConnection` and BEP framing/flow-control internals as the next layer after transport convergence.
4. Check relay reconnect and dynamic-relay address-change behavior under failure.