# DERP operational failure modes and observability

Date: 2026-08-25
Status: source-level architecture research
Scope: Tailscale DERP operator behavior and observability

## Why this dossier exists

Earlier GitHub Gold research mapped DERP admission controls, per-client rate limiting, bounded send queues, write timeouts, duplicate-key handling, and operator metrics. This pass narrows the question further: when those mechanisms fail or become stressed in production, what signals does the server expose and what should an operator watch?

This is not an independent security audit or load test. Findings below come from selected current upstream source inspection and are intentionally limited to what the code exposes.

## Current upstream source inspected

Repository: https://github.com/tailscale/tailscale

Primary files:

- `cmd/derper/derper.go`
- `derp/derpserver/derpserver.go`

Inspected upstream commit: `af4b7b03633a5fe06e6fc274e27fc369007a0e66`

Root project license: BSD-3-Clause.

## Operator-visible failure surfaces

### 1. Slow or stuck client writes

DERP has a server-side TCP write timeout. Current source defines a default ordinary-client timeout of 2 seconds and a longer privileged timeout for mesh-key clients.

A dedicated server counter records client write timeouts. This makes slow-reader or blocked-client behavior directly observable instead of only surfacing as vague connection churn.

Operational interpretation:

- rising write-timeout counts can indicate slow clients, network degradation, overloaded hosts, or clients that are no longer draining queued packets;
- correlate write timeouts with queue-duration and drop metrics before assuming malicious behavior;
- sustained write timeouts plus growing queue pressure are a stronger signal than either metric alone.

### 2. Per-client outbound queue pressure

Current source defines a default per-client send queue depth of 32 packets. It also tracks average queue duration and packet/byte drops by reason and packet kind.

This gives an operator multiple views of the same scarcity problem:

- queue occupancy pressure indirectly through average queue duration;
- final shedding through packet/byte drop counters;
- client write timeouts when the receiving side stops making progress.

A useful alert should therefore avoid a single-threshold design. Queue duration rising without drops may only mean temporary congestion; drops plus timeouts indicate a more serious backpressure condition.

### 3. Per-client receive-rate pressure

DERP supports per-client frame-rate limiting loaded from rate configuration. Current server state includes a counter for the number of times a per-client rate limit caused a wait.

The source also contains a TODO for richer rate-limit wait-time metrics, so current observability is stronger for event count than for total throttling duration.

Operational interpretation:

- a rapidly increasing wait counter identifies clients repeatedly reaching receive limits;
- pair it with bytes/packets received and drop reasons to separate a legitimately busy client from abusive traffic;
- because wait duration is not yet fully represented, do not infer exact throttling impact from event count alone.

### 4. Duplicate node identities

DERP explicitly tracks duplicate public-key connections. Current server metrics include:

- number of public keys with two or more connections;
- number of connections sharing duplicate keys;
- total accepted connections where a duplicate key already existed.

The server also has logic for duplicate-client sets. Temporary duplicates can occur during ordinary network transitions, but cloned keys can cause multiple peers to fight for the same identity. The source describes a policy that can disable conflicting connections when they interleave traffic.

Operational interpretation:

- short-lived duplicate counts are not automatically abuse;
- persistent or repeatedly increasing duplicate-key metrics deserve investigation;
- duplicate-key signals should be correlated with reconnect churn, packet drops, and client health rather than treated as a standalone compromise detector.

### 5. Packet and byte drops by reason

DERP exposes labeled packet and byte drop metrics. The labels include drop reason and packet kind, allowing operators to distinguish broad failure classes rather than monitoring only a global drop total.

This is particularly useful when combined with queue and write-timeout signals because it helps answer whether the server is dropping due to congestion/backpressure or another path-specific condition.

### 6. Client population and placement signals

Current server state tracks:

- accepted connections;
- current clients;
- clients that are not on their ideal server;
- clients considering this DERP region home;
- home moves in/out;
- mesh forwarding activity.

These signals matter because traffic anomalies can be caused by topology changes rather than abuse. A sudden increase in clients that are not on their ideal DERP server can precede queue pressure or relay load imbalance.

### 7. Mesh behavior

DERP tracks mesh update batch size, mesh update loop counts, forwarded packet counts, multi-forwarder creation/deletion, and peer-gone signaling.

For multi-DERP deployments, this gives operators a separate view of regional or mesh-level instability rather than conflating all traffic problems with individual clients.

### 8. Debug and consistency surfaces

The `derper` entry point publishes server metrics through expvar and exposes a consistency-check debug handler. A traffic debug handler is also registered, along with runtime/debug controls.

These surfaces are useful for diagnosing invariants and traffic state, but they should be treated as operator/debug interfaces rather than ordinary public product endpoints. Deployment-layer access control remains important.

## External verification failure model

The DERP entry point can enable local tailscaled client verification and can configure an external verification URL. The server also exposes an explicit fail-open configuration option for external verification.

This is an important operational distinction:

- fail-closed prioritizes admission integrity when the verifier is unavailable;
- fail-open prioritizes DERP availability when the verifier is unavailable.

GitHub Gold did not fully trace the external verifier's request timeout/retry code in this pass, so no claim is made here about exact timeout duration or retry count. That remains a targeted follow-up item.

## Suggested operator alert groups

These are architecture-derived groupings, not upstream-prescribed thresholds.

### Backpressure group

Watch together:

- client write-timeout count;
- average queue duration;
- packet/byte drops by reason;
- per-client rate-limit wait count.

Reason: each metric alone is ambiguous; together they describe whether traffic is merely busy, actively throttled, or no longer draining.

### Identity-conflict group

Watch together:

- duplicate public-key count;
- duplicate connection count;
- duplicate-connection total;
- reconnect/accept churn;
- packet drops or disabled-client behavior.

Reason: transient duplicate connections can be normal during roaming, while persistent duplicate activity can indicate cloned identity state or broken clients.

### Topology/placement group

Watch together:

- current clients;
- not-ideal clients;
- home moves in/out;
- mesh forwarding and update-loop metrics;
- queue/backpressure signals.

Reason: a regional or mesh routing shift can look like a traffic attack if topology metrics are ignored.

## Reusable design lessons

1. **Expose scarcity at multiple stages.** Track queue delay, final drops, and write timeouts instead of only one symptom.
2. **Treat identity conflicts as stateful behavior.** A duplicate connection is not inherently malicious; persistence and traffic interleaving matter.
3. **Separate traffic abuse from topology changes.** Placement and mesh metrics are necessary context for rate/drop alarms.
4. **Make availability-vs-integrity policy explicit.** External admission systems should expose fail-open/fail-closed behavior as configuration rather than hiding it.
5. **Keep debug invariants inspectable.** A consistency-check endpoint is useful when complex client/mesh maps must remain synchronized.
6. **Do not overclaim from counters.** Event counts such as rate-limit waits do not substitute for latency/duration histograms.

## Verification boundary

GitHub Gold inspected selected upstream source at the commit recorded above. It did not:

- deploy a DERP server;
- induce verifier failures;
- perform load or denial-of-service testing;
- validate metric cardinality or scraping behavior in production;
- independently security-audit duplicate-key logic;
- confirm deployment-specific debug endpoint exposure;
- measure false-positive rates for any proposed alert grouping.

No third-party source code is copied into GitHub Gold.

## Strongest next targets

1. Trace the external verification HTTP request path end-to-end, including timeout, cancellation, response-code handling, malformed responses, and fail-open behavior.
2. Inspect exact packet-drop reason labels and map them to operator remediation categories.
3. Compare DERP's observability model against Iroh relay metrics and libp2p relay reservation/resource metrics.
4. Inspect whether duplicate-key disable events are surfaced directly to clients or only via server-side state/metrics.
5. Separate debug endpoints that are expected to be private from endpoints intended for normal public DERP operation.
