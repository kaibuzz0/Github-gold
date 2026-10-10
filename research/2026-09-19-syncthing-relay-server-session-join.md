# Syncthing relay server: session join, pairing, and failure semantics

- Upstream: https://github.com/syncthing/syncthing/blob/main/cmd/strelaysrv/listener.go
- Component: `cmd/strelaysrv/listener.go` (`sessionConnectionHandler` plus control-path session creation)
- Category: networking / relay infrastructure / session rendezvous
- Evidence: **VERIFIED** (source-inspected)
- Provisional Gold score: **26/30 (S tier)**
  - Utility 4/5
  - Working evidence 4/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5

## What it is

`strelaysrv` multiplexes two roles on its relay listener. Connections detected as TLS are sent to the long-lived relay control protocol handler; non-TLS connections are sent to `sessionConnectionHandler`, which accepts the short-lived `JoinSessionRequest` used to attach a participant socket to a previously created relay session.

## End-to-end server-side path

The control path authenticates peer identity from the presented TLS certificate and tracks joined peers by DeviceID. When a joined client sends `ConnectRequest` for another currently joined DeviceID, the server creates a new session with `newSession(requestedPeer, id, sessionLimitBps, globalLimiter)`, starts `ses.Serve()`, generates separate client/server invitation messages, sends the client invitation back on the requesting control connection, and sends the server invitation through the target peer's outbox. The requesting control connection is then closed.

Each invitation contains a session key consumed later by the data connection. `sessionConnectionHandler` applies the normal message deadline, reads one relay-protocol message, and accepts only `JoinSessionRequest`. It looks up the session by the supplied key via `findSession(string(msg.Key))`. A missing/expired/unknown key returns `ResponseNotFound` and closes the socket.

If a session is found, the handler calls `ses.AddConnection(conn)`. Failure to attach returns `ResponseAlreadyConnected` and closes the socket. A successful attach receives `ResponseSuccess`, after which the handler clears the socket deadline and deliberately returns without closing the connection; ownership has effectively passed into the session machinery that was started by `ses.Serve()`.

## Failure and cleanup semantics

The control side rejects malformed target DeviceIDs with `ResponseNotFound`; rejects a requested peer that is not currently registered; and bounds delivery of the target peer's invitation with a one-second timeout. Joined control connections are kept alive with Ping/Pong and a network timeout.

When a joined control connection fails, its DeviceID outbox is removed and `dropSessions(id)` is called. The source comments explicitly state that this is intended to make the opposite endpoint notice the disconnect faster and to reduce stale `already connected` behavior during restarts.

The session data path has explicit responses for unknown keys (`NotFound`), duplicate/invalid attachment (`AlreadyConnected`), successful attachment (`Success`), and unexpected message types (`UnexpectedMessage`).

## Why it matters

This is a compact, reusable rendezvous architecture: identity-bearing control channels create a session and distribute independent invitation capabilities; separate data sockets redeem those capabilities; successful redemption hands the raw connection into a full-duplex session object. Control-plane liveness also tears down related data-plane sessions when a peer disappears.

The design is useful as a reference for NAT-friendly rendezvous services, relay gateways, capability-token session admission, and systems that intentionally separate durable control connections from short-lived application data sockets.

## Important verification boundary

Source inspection establishes the code path and response semantics. GitHub Gold did **not** run `strelaysrv`, create two live clients, test invitation expiration/races, fuzz keys, induce simultaneous duplicate joins, transfer bytes, or audit the concurrency/security properties of the session maps.

The presence of these branches does not by itself establish automated test coverage. The previous dossier identified an upstream manual `testutil` capable of joining both sides and moving bytes, but that remains distinct from CI-backed integration evidence.

## License

`cmd/strelaysrv` carries a dedicated MIT license. Imported Syncthing library packages retain their own applicable licenses and must be reviewed separately before extraction or redistribution. No upstream source is copied into GitHub Gold.

## Discovery provenance

Recursive follow-up from `research/2026-09-18-syncthing-relay-testutil-data-plane.md`, specifically its open lead to trace `JoinSessionRequest -> findSession -> AddConnection` on the relay server.

## Strong next leads

1. Inspect `lib/connections/relay_dial.go` and `relay_listen.go` to map how successful `JoinSession` sockets become normal Syncthing `internalConn` objects in production.
2. Search tests/CI for automated two-peer coverage of the server session join and byte-transfer path.
3. Inspect `session.go` together with the global session registry to document exact key deletion/expiry and duplicate-join race behavior.
4. Inspect the relay manpage for protocol timing and operational guarantees that complement the implementation.