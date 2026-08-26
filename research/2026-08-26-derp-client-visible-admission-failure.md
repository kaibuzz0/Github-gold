# Tailscale DERP Client-Visible Admission Failure Path — 2026-08-26

## Purpose

This dossier closes the next open question in the DERP external-admission research:

> What does an ordinary DERP client actually observe when `Server.verifyClient` rejects it?

This is a source-level protocol/operations note for the already researched Tailscale/DERP stack. It is not a new Gold candidate and not a vulnerability report.

## Executive finding

Current upstream source shows an important asymmetry between the server and client sides of the DERP handshake:

- the server receives and decrypts `ClientInfo`, then runs `verifyClient` before registering the client and before sending `ServerInfo`;
- if verification fails, the server returns an error such as `client <key> rejected: <reason>` and closes the connection;
- the ordinary DERP client constructor sends `ClientInfo` but deliberately does **not** wait for the post-admission `ServerInfo` frame before returning;
- therefore, a DERP-over-HTTP `Connect` can complete its client-side constructor path before the server has positively admitted the client;
- an admission denial is consequently expected to become visible through a subsequent read/write/connection failure (for example EOF/closed connection), not through a structured DERP "admission denied" frame carrying the server's policy reason.

The server-side rejection reason is useful to the DERP operator through logs/errors, but the inspected protocol path does not send that reason to the ordinary client as a dedicated policy message.

This conclusion is based on source inspection only. GitHub Gold did not run a DERP server with an admission controller and did not capture packets or client logs for a live rejection.

## Upstream snapshot inspected

Primary source snapshot:

- Tailscale repository commit `d7253cb40e38cd71cdf4366246ff3078414b1662`
- server: `derp/derpserver/derpserver.go`
- DERP client: `derp/derp_client.go`
- DERP-over-HTTP client: `derp/derphttp/derphttp_client.go`

Source URLs:

- https://github.com/tailscale/tailscale/blob/d7253cb40e38cd71cdf4366246ff3078414b1662/derp/derpserver/derpserver.go
- https://github.com/tailscale/tailscale/blob/d7253cb40e38cd71cdf4366246ff3078414b1662/derp/derp_client.go
- https://github.com/tailscale/tailscale/blob/d7253cb40e38cd71cdf4366246ff3078414b1662/derp/derphttp/derphttp_client.go

## Server-side ordering

The server's connection path first receives the client's key and `ClientInfo`, determines the remote IP, and calls:

`verifyClient(ctx, clientKey, clientInfo, remoteIP)`

If verification fails, the server returns an error wrapped as:

`client <key> rejected: <reason>`

Only after verification succeeds does the server clear the connection deadline and treat the peer as trusted.

The later successful path creates/registers the client and sends `ServerInfo` before entering the long-running client loop.

So the ordering is effectively:

1. initial DERP/server greeting;
2. receive encrypted client identity/info;
3. run local/external/app-name admission checks;
4. **reject and close on failure**;
5. register client on success;
6. send `ServerInfo`;
7. run the steady-state client loop.

This makes `ServerInfo` a useful protocol boundary: a rejected client does not reach that post-admission server-info path.

## Why the client can still think `Connect` succeeded briefly

The client implementation is intentionally optimized not to wait an extra RTT before giving the connection to higher layers.

`derp.NewClient` performs the following setup:

1. establish/learn the DERP server public key if needed;
2. send the client's encrypted `ClientInfo` frame;
3. return the `*derp.Client`.

It does not synchronously wait for `ServerInfo` before returning.

The receive path later parses `ServerInfo`. The source comment explicitly explains the design choice: the protocol is extensible enough that the client prefers to hand the connection to magicsock quickly instead of waiting an RTT just to discover the server version.

That is normally a latency optimization. In the admission-controller case it also means the local client constructor's success is not identical to server-side policy acceptance.

## DERP-over-HTTP wrapper behavior

`derphttp.Client.connect` calls `derp.NewClient` and stores the returned client when the constructor succeeds.

The wrapper's documented behavior is that a failed `Send` or `Recv` reports the error, while subsequent calls can re-establish the connection unless the client has been closed.

Because `derp.NewClient` does not wait for post-admission `ServerInfo`, an external admission rejection can race with the wrapper's successful completion of the local construction path.

The safe operational conclusion is:

> A successful local `derphttp.Client.Connect` call should not be interpreted as proof that an external DERP admission controller accepted the client unless higher-level traffic/receive state confirms the connection survived the post-ClientInfo server checks.

GitHub Gold is not claiming every rejection always returns `Connect == nil` or always returns a particular later error string; the exact user-visible error can depend on timing, transport closure behavior, and which operation observes the closed socket first.

## What the rejected client does *not* receive

In the inspected path, the server's admission error is returned internally from the connection handler.

No dedicated DERP frame was found that serializes:

- `Allow:false`;
- non-200 controller response;
- malformed controller reply;
- local tailscaled authorization failure;
- disallowed app-name reason;
- external verifier network/timeout failure;
- the human-readable `client <key> rejected: ...` server error.

The ordinary client therefore does not appear to receive a structured admission-policy reason over the DERP protocol before the connection is terminated.

This matters for operations: the server/operator can know *why* admission failed while the client may only know that the DERP connection stopped working.

## Expected failure surfaces

Without executing the path, the source supports several possible client-side failure surfaces rather than one guaranteed error string:

### Read path

A client waiting for the first post-handshake server frame can observe the underlying connection closing before a valid `ServerInfo` arrives. Depending on transport/timing this can surface as EOF or another socket/read error.

### Write path

Because the constructor returns after sending `ClientInfo`, a caller may attempt a DERP write shortly before or after the server closes the rejected connection. The write can therefore race with rejection and eventually surface a closed/broken transport error.

### Reconnect path

`derphttp.Client` is designed to reconnect after failed send/receive operations. A persistently denied identity can therefore create repeated connection attempts unless a higher layer applies its own backoff/health logic.

This reinforces the previous capacity dossier: external admission is not only an authorization decision; persistent denial during reconnect behavior can also become an operational load pattern worth monitoring.

## Server-side observability versus client-side observability

The current source exposes a useful distinction.

### Server/operator side

The server wraps the admission failure with the client key and reason. The external verifier's unreachable/fail-open case is explicitly logged. The DERP process therefore has significantly more policy context than the remote client.

### Client side

The ordinary DERP protocol path does not visibly carry the policy rejection reason to the client.

A client-side health system may be able to say that DERP connectivity failed, but it cannot infer from the transport failure alone whether the cause was:

- explicit admission deny;
- malformed/non-200 controller response;
- fail-closed controller timeout/network error;
- generic server-side close;
- an unrelated transport failure.

That means client-only telemetry is insufficient for precise external-admission diagnosis.

## Metric correlation

The previous DERP dossiers found no dedicated admission-controller metric family in the inspected server fields/request path.

This source trace sharpens that observation:

- `accepts` is incremented at the beginning of `Server.Accept`, before client verification;
- `curClients` is incremented only when a client is actually registered after the handshake/admission path;
- therefore, admission failures contribute to connection accepts but do not become registered current clients.

That difference can be operationally suggestive, but it is **not admission-specific**. Other handshake failures can also occur between accept and successful registration.

So an operator should not interpret `accepts - successful/current clients` as an admission-deny counter.

A dedicated reason-labeled admission metric would make this failure mode much easier to distinguish, but GitHub Gold is not prescribing an upstream implementation.

## Useful invariant for future testing

A controlled test can now assert a stronger protocol invariant:

> When an admission policy rejects a normal client, the server must not register it or send the normal post-admission `ServerInfo` path, and the connection must terminate without exposing server policy details as an ordinary DERP data/control frame.

A test matrix should separately observe:

- server handler/log error;
- whether `derphttp.Client.Connect` itself returns before the rejection is observed;
- first `Recv` result;
- first `Send` result;
- reconnect behavior/backoff;
- `accepts` and `curClients` metric changes;
- whether any server-info frame was received.

## Security/privacy interpretation

Not sending detailed rejection text to unauthenticated/unadmitted clients has a potential information-minimization benefit: policy internals and local authorization details are not automatically exposed across the wire.

The tradeoff is diagnosability. Clients may see only a generic connectivity failure, requiring server-side logs/telemetry to identify the policy cause.

GitHub Gold records this as an architecture tradeoff, not a claim that the current behavior is intentionally designed for information-hiding or that it is optimal.

## Verification performed

Inspected current upstream public source for:

- server ordering around `verifyClient`, registration, and `sendServerInfo`;
- server rejection error wrapping;
- client constructor ordering;
- `sendClientKey` behavior;
- delayed `ServerInfo` parsing in the receive path;
- DERP-over-HTTP connection wrapper semantics;
- `accepts` and `curClients` update locations;
- visible protocol surfaces for a dedicated admission-rejection frame.

Not performed:

- no Tailscale/DERP build;
- no upstream test execution;
- no custom external admission controller;
- no packet capture;
- no live denial reproduction;
- no measurement of exact error strings at the caller;
- no reconnect/load measurement;
- no claim about private Tailscale test or telemetry systems.

## Repository conclusion

The strongest new statement for GitHub Gold is:

> DERP verifies a client before registration and before sending the normal post-admission `ServerInfo`, but the ordinary client constructor intentionally returns after sending `ClientInfo` instead of waiting for that server frame. As a result, external-admission rejection is not exposed as a structured policy-denial message to the normal DERP client and may instead surface on a subsequent receive/write/connection path. Server-side logs retain much more rejection context than client-side transport errors.

## Strongest next leads

1. Inspect the higher-level magicsock DERP reconnect/backoff path to determine how persistent admission rejection is surfaced in health state and how aggressively it reconnects.
2. Search recent Tailscale issues/PRs for external DERP admission incidents, diagnostics, or requested metrics.
3. Compare DERP's close-without-policy-frame model against Iroh relay `AccessControl` rejection behavior.
4. Design a small upstream-style regression test using an in-memory DERP server/client pair to pin the client-visible denial behavior without requiring production deployment.
5. Trace whether DERP handler error logs include enough source/controller context for operators to correlate repeated failures without exposing sensitive node identifiers excessively.
