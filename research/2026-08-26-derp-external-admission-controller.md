# Tailscale DERP External Admission Controller Trace — 2026-08-26

## Purpose

This dossier closes the verification gap left in the prior DERP operational research by tracing the external `--verify-client-url` admission path in current upstream Tailscale source.

This is not a new Gold candidate. It is a source-level operational/security note for the already researched Tailscale/DERP stack.

## Executive finding

DERP's external admission controller is deliberately simple and has an important fail-open boundary:

- DERP creates a JSON request containing the connecting node public key and source IP.
- It POSTs that JSON to the configured admission-controller URL.
- The request uses a context with a hard **5-second timeout**.
- There is no explicit retry loop in the inspected admission path.
- If the HTTP request itself returns an error and `--verify-client-url-fail-open` is true, DERP logs that the controller is unreachable and admits the client.
- If fail-open is false, that request error rejects the connection.
- HTTP non-200 responses reject the connection even when fail-open is enabled.
- A malformed response body rejects the connection.
- A decoded response with `Allow:false` rejects the connection.
- The response JSON reader is capped at **4 KiB** before decoding.

The operational consequence is that **fail-open is not a universal "controller problem means allow" switch**. It is limited to the transport/request-error branch around the outbound HTTP call. A controller that is reachable but returns an error status, invalid JSON, or `Allow:false` fails closed.

## Configuration surface

`cmd/derper` exposes:

- `--verify-client-url` — admission-controller URL
- `--verify-client-url-fail-open` — whether to admit when the URL is unreachable

The current flag default for fail-open is **true**.

The configured values are passed into `derpserver.Server` through `SetVerifyClientURL` and `SetVerifyClientURLFailOpen`.

This is separate from `--verify-clients`, which verifies against a local `tailscaled` instance.

## Request schema

Current `tailcfg` source defines `DERPAdmitClientRequest` with two fields:

- `NodePublic` — connecting node public key
- `Source` — DERP client's source IP address

The response schema contains:

- `Allow bool`

A source comment leaves possible future bandwidth-limit fields as a TODO, but no such limits are part of the inspected response type.

## End-to-end request path

### 1. Admission verification is conditional

The external HTTP verification path runs only when `verifyClientsURL` is non-empty.

### 2. A 5-second child context is created

The server wraps the current connection context with:

`context.WithTimeout(ctx, 5*time.Second)`

That context is attached to the outbound HTTP request, so DNS/connect/TLS/request/response activity performed through that request is bounded by the request context rather than being allowed to hang indefinitely.

Important boundary: GitHub Gold did not live-test each possible network failure phase, so this dossier records the source-level timeout boundary rather than claiming measured wall-clock behavior under every resolver/proxy/TLS configuration.

### 3. Request JSON is marshaled

DERP marshals the node public key and source IP into `tailcfg.DERPAdmitClientRequest`.

Marshal failure returns an error and does **not** enter the fail-open branch.

In practice these fields are normal structured types, so marshal failure is not expected during ordinary operation, but the code path remains fail-closed.

### 4. HTTP request creation

The server creates an HTTP `POST` with `http.NewRequestWithContext` and sends the JSON bytes as the request body.

The inspected code does not set a custom `Content-Type` header in this path.

Request-construction failure returns an error and does not enter the fail-open network-error branch.

### 5. Single outbound HTTP call

The request is issued with `http.DefaultClient.Do(req)`.

No explicit retry loop was found around this admission call.

This matters operationally: admission latency and controller availability are directly on the DERP connection-accept path. Operators should not assume DERP itself will retry a transient controller failure before applying fail-open/fail-closed policy.

### 6. Exact fail-open branch

If `http.DefaultClient.Do(req)` returns an error:

- with fail-open enabled, DERP logs `admission controller unreachable; allowing client ...` and returns success;
- with fail-open disabled, the error is returned and the client is rejected.

Therefore failures represented by the HTTP client as request errors—including the request context expiring—enter this branch.

This is the narrow source-level meaning of "unreachable" in the implementation.

## What does NOT fail open

### Non-200 HTTP status

If an HTTP response is received but its status code is not 200, DERP returns an admission-controller error.

This rejects the client regardless of the fail-open flag because the code has already passed the `Do` error branch.

Examples at the semantic level include a reachable controller returning 401, 403, 429, 500, or 503.

GitHub Gold did not live-test each status code; the conclusion follows from the shared `res.StatusCode != 200` branch.

### Malformed or invalid JSON response

For HTTP 200 responses, DERP decodes `tailcfg.DERPAdmitClientResponse` from the response body.

Decode errors are returned directly and reject the client. They do not trigger the fail-open path.

### Oversized response body

The JSON decoder reads through `io.LimitReader(res.Body, 4<<10)`, limiting the readable response to 4 KiB.

This protects the admission path from unbounded response-body consumption.

If the JSON needed to form a valid response cannot be decoded within that bounded input, decoding fails and the connection is rejected.

### Explicit deny

A valid JSON response with `Allow:false` returns an error identifying the node/source as not allowed.

This is the normal policy-denial path and is fail-closed regardless of the fail-open setting.

## Failure matrix

| Condition | Fail-open=true | Fail-open=false | Source-level reason |
|---|---|---|---|
| Controller URL not configured | external controller not used | external controller not used | verification block skipped |
| HTTP request succeeds + 200 + `Allow:true` | allow | allow | positive admission |
| HTTP request succeeds + 200 + `Allow:false` | reject | reject | explicit deny |
| HTTP response is non-200 | reject | reject | status error occurs after request succeeded |
| HTTP 200 body is malformed JSON | reject | reject | decode error |
| Request/network error from `Do` | allow | reject | exact fail-open branch |
| 5-second request context expires and surfaces as request error | allow | reject | timeout is on request context |

## Availability vs admission-integrity tradeoff

The current CLI default makes external admission **availability-biased** for transport-level controller outages because `--verify-client-url-fail-open` defaults to true.

That does not mean DERP silently accepts a controller's negative decision. A responsive controller retains authority to reject through:

- non-200 status,
- invalid response handling,
- explicit `Allow:false`.

The key operator decision is therefore not simply "use an admission controller." It is whether **controller unreachability should interrupt DERP availability or temporarily weaken admission enforcement**.

For environments where external admission is a hard security boundary, operators should understand the default before deployment and explicitly choose the failure policy appropriate to that environment.

## Resource-control observations

The admission path contains two useful bounds:

1. **5-second request context** — limits how long one verification can remain blocked.
2. **4 KiB response decode window** — limits response-body data consumed by the JSON decoder.

The inspected code does not show a dedicated admission-controller retry loop or separate admission-specific HTTP client with custom transport pooling/timeouts. It uses `http.DefaultClient` with the per-request context timeout.

This means global connection acceptance pressure can still translate into concurrent admission-controller requests; the previous DERP operator-control dossier's accept-connection limiting remains relevant as an outer defensive control.

## Observability gap

The inspected path logs the fail-open case when the controller is unreachable, but this pass did not identify a dedicated metric family for:

- controller request latency,
- controller request errors,
- HTTP status-code distribution,
- explicit denies,
- malformed response failures,
- fail-open admission count.

That is now a concrete follow-up lead. If those signals exist elsewhere, they should be mapped; if not, this is an operational visibility gap worth recording rather than assuming generic DERP metrics cover admission-controller health.

## Security interpretation

The safest architectural lesson is to separate three outcomes:

1. **negative policy decision** — explicit reject, always fail closed;
2. **controller protocol failure** — reachable but invalid/non-200 response, currently fail closed;
3. **controller transport failure** — no successful HTTP response, configurable fail open/closed.

That distinction prevents a common configuration misunderstanding where "fail open" is assumed to override all controller failures.

## Verification performed

Inspected current upstream Tailscale source for:

- `cmd/derper` admission-related CLI flags and defaults;
- propagation into `derpserver.Server`;
- the `verifyClientsURL` request path;
- timeout construction;
- HTTP call and error branch;
- HTTP status handling;
- bounded JSON response decoding;
- explicit allow/deny handling;
- `tailcfg.DERPAdmitClientRequest` and `DERPAdmitClientResponse` schemas.

Not performed:

- no live DERP deployment;
- no external controller server was run;
- no DNS/TCP/TLS failure injection;
- no timeout timing measurement;
- no proxy behavior testing;
- no load test;
- no security audit of `http.DefaultClient` behavior outside the visible request path.

## Repository conclusion

This dossier resolves the previous open question about exact external DERP admission behavior.

The most important corrected/confirmed statement for GitHub Gold is:

> `--verify-client-url-fail-open` only changes the outcome when the outbound admission HTTP request itself errors. A reachable controller returning non-200, invalid JSON, or `Allow:false` still rejects the client.

## Strongest next leads

1. Find or confirm metrics for admission-controller latency/errors/deny/fail-open counts.
2. Inspect tests covering the external admission path and add exact tested edge cases to the dossier.
3. Trace how a verification error propagates into the DERP handshake and what the client observes.
4. Compare the external admission failure model with Iroh relay `AccessControl` and libp2p relay reservation admission.
5. Determine whether admission-controller requests share any concurrency/backpressure limit beyond the outer connection acceptance controls.
