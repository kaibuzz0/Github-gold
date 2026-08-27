# Tailscale DERP Admission Test Coverage and Concurrency Boundaries — 2026-08-26

## Purpose

This dossier follows the external DERP admission-controller trace and closes two remaining operational questions:

1. what upstream tests visibly cover the `--verify-client-url` path; and
2. what concurrency/backpressure controls bound simultaneous admission-controller requests.

This is not a new Gold candidate and not a vulnerability report. It is a source-level reliability and operator-capacity note for the already researched Tailscale/DERP stack.

## Executive finding

Current upstream source shows a simple synchronous verification model:

- each DERP connection that reaches `verifyClient` can perform one outbound admission-controller HTTP request;
- that request has a hard 5-second context timeout;
- there is no explicit retry loop;
- no admission-specific semaphore, worker pool, or concurrent-request cap was found in the inspected verification path;
- `cmd/derper` does provide an outer TCP accept-rate limiter, but its defaults are effectively unlimited;
- therefore, unless the operator configures the outer connection limiter or controls load elsewhere, a burst of accepted client handshakes can translate into a burst of concurrent HTTP verification work.

The upstream `cmd/derper/derper_test.go` file inspected in this pass does not contain tests for the external admission-controller flags or HTTP decision matrix. Repository code search for `DERPAdmitClientResponse` under `derp/` found only the production implementation, not a matching DERP test path.

That is a **test-coverage observation**, not proof that the behavior is untested everywhere in Tailscale's private/internal infrastructure. GitHub Gold only claims what is visible in the inspected public repository.

## Verification placement in the handshake

Current `derpserver.Server` connection handling receives the client key and then calls:

`verifyClient(ctx, clientKey, clientInfo, remoteIP)`

If that function returns an error, the connection is rejected before DERP clears the connection deadline and begins treating the client as trusted.

This means the admission controller sits directly on the connection-establishment path rather than running asynchronously after admission.

Operational consequence: controller latency contributes directly to client connection latency.

## One verification request per connection path

When an external URL is configured, `verifyClient`:

1. creates a 5-second child context;
2. marshals `DERPAdmitClientRequest`;
3. creates one HTTP POST;
4. calls `http.DefaultClient.Do(req)` once;
5. applies fail-open/fail-closed policy to request errors;
6. validates HTTP status and decodes a bounded response.

No explicit retry loop is present around that request.

No admission-specific goroutine pool, semaphore, token bucket, or queue was found around the HTTP call in the inspected function.

## Concurrency model

The important distinction is **rate** versus **in-flight concurrency**.

### Admission-specific in-flight cap

No dedicated cap was found in the inspected admission verification code.

Because each accepted connection proceeds through its own verification call, multiple connection handshakes can have admission requests in flight at the same time.

The 5-second request context limits the lifetime of each individual request, but it does not itself limit how many requests can be simultaneously active.

### Outer accept-rate limiter

`cmd/derper` wraps its TLS listener with a rate-limited listener when serving TLS.

The public flags are:

- `--accept-connection-limit`
- `--accept-connection-burst`

The listener accepts a socket and immediately closes/rejects it when the configured token bucket does not allow the connection. The source comment explicitly explains that this avoids leaving excess connections queued in the kernel.

This is useful protection against connection floods before expensive higher-level work.

However, the current flag defaults are:

- limit: positive infinity
- burst: maximum integer

So the mechanism exists, but operators must configure it if they want it to provide a meaningful bound.

### What the accept limiter does not guarantee

A token-bucket accept-rate limit is not the same thing as a hard maximum number of simultaneous admission-controller requests.

For example, if the configured accept rate allows a sufficiently large burst and the controller is slow, many admitted TCP connections may still overlap in the 5-second HTTP-verification window.

GitHub Gold did not load-test this path, so this dossier does not claim a measured maximum concurrency value.

## HTTP-client behavior boundary

The verification path uses `http.DefaultClient` with a per-request context rather than a dedicated client object with an admission-specific transport or explicit pool configuration.

That means connection reuse, idle connection pooling, DNS behavior, and transport-level limits come from Go's default HTTP client/transport behavior plus the request context.

GitHub Gold did not attempt to infer exact production concurrency from Go transport defaults because those details are separate from DERP's own explicit policy surface and can change by Go version/runtime configuration.

The safe repository statement is simply:

> DERP adds a per-request 5-second timeout but does not visibly add an admission-specific concurrent-request cap around `http.DefaultClient.Do`.

## Visible upstream test coverage

### `cmd/derper/derper_test.go`

The inspected public test file contains tests for:

- production autocert hostname policy;
- `/generate_204` challenge behavior;
- dependency constraints;
- homepage/template content.

It does not contain tests for:

- `--verify-client-url`;
- `--verify-client-url-fail-open`;
- admission request payload construction;
- HTTP 200 allow/deny behavior;
- non-200 rejection;
- malformed JSON rejection;
- 5-second timeout behavior;
- fail-open request-error behavior;
- response-size limiting;
- concurrent verification behavior.

### Repository search

A repository code search for `DERPAdmitClientResponse` scoped under `derp/` returned the production `derpserver.go` implementation and no separate DERP test implementation.

A search for the phrase `admission controller` found the public schema/config/production implementation surfaces rather than a dedicated admission test suite.

This supports the narrow conclusion that **dedicated public tests for this path were not located in this pass**.

It does not prove that no indirect, integration, private, generated, or downstream tests exist.

## Observability status

The prior dossier identified no dedicated admission-controller metric family in the visible request path.

This pass's repository search likewise did not surface dedicated counters/histograms named around admission-controller latency, transport errors, non-200 responses, explicit denies, malformed replies, or fail-open admissions.

The fail-open transport-error case is visibly logged.

DERP does expose broader server metrics, including connection acceptance/rejection and packet/client operational signals, but those do not by themselves identify the external controller as the failure source.

## Operator interpretation

The current architecture gives operators three important knobs/bounds:

1. **connection admission rate/burst** at the listener;
2. **5-second maximum request context** per external verification;
3. **fail-open/fail-closed policy** when the HTTP request itself errors.

What it does not visibly provide is a dedicated admission-controller concurrency budget.

For operators relying heavily on an external verifier, the useful capacity-planning question is therefore:

> How many simultaneous verification requests can the controller tolerate during DERP reconnect bursts, and what listener accept-rate/burst values keep that demand inside a safe envelope?

GitHub Gold does not prescribe values because no deployment/load test was performed.

## Reliability interpretation

This architecture is simple and easy to reason about, but it couples external-controller health directly to connection establishment.

The 5-second bound prevents indefinite stalls. The outer accept limiter can reduce burst pressure. The absence of retries avoids retry amplification. At the same time, without a dedicated in-flight cap, an operator should not assume the timeout alone protects the controller from high concurrent demand.

## Test cases worth tracking upstream

The most valuable public regression coverage for this path would exercise:

- request body contains the expected node key and source IP;
- HTTP 200 + `Allow:true` admits;
- HTTP 200 + `Allow:false` rejects;
- non-200 rejects regardless of fail-open;
- malformed JSON rejects regardless of fail-open;
- request/network error obeys fail-open true/false;
- context timeout obeys the same request-error policy;
- response decoding remains bounded;
- multiple simultaneous verifications do not leak goroutines/resources;
- listener rate limiting constrains connection bursts as intended.

This list is a research/testing recommendation, not a claim that upstream is obligated to implement it exactly this way.

## Verification performed

Inspected current upstream Tailscale public repository source for:

- DERP admission-controller flags and defaults;
- connection accept-rate limiter implementation;
- `Server.verifyClient` placement in the connection handshake;
- HTTP verification call structure;
- visible DERP server metrics fields;
- `cmd/derper/derper_test.go`;
- repository code-search results for the admission request/response symbols and `admission controller` phrase.

Not performed:

- no DERP build;
- no test suite execution;
- no custom admission server;
- no concurrent load test;
- no DNS/TCP/TLS fault injection;
- no goroutine profiling;
- no production traffic measurement;
- no claim about private Tailscale test infrastructure.

## Repository conclusion

The strongest new statement for GitHub Gold is:

> DERP's external admission controller is synchronously invoked per connecting client, bounded by a 5-second request context but not by a visible admission-specific concurrency limiter. An outer connection accept-rate limiter exists but defaults to effectively unlimited. Dedicated public regression tests for the external admission decision matrix were not located in the inspected upstream test surfaces.

This is an operational capacity and test-coverage observation, not evidence of an exploitable vulnerability.

## Strongest next leads

1. Trace the exact client-visible DERP handshake failure when `verifyClient` rejects a client.
2. Inspect recent upstream issues/PRs for external admission-controller failures or capacity incidents.
3. Compare this synchronous HTTP policy hook with Iroh's in-process `AccessControl` callback and its external authorization mode.
4. Determine whether DERP's generic connection metrics can be correlated with admission failures strongly enough for practical alerting.
5. If a safe test environment becomes available, reproduce the decision matrix and measure in-flight verifier concurrency under controlled reconnect bursts.
