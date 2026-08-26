# DERP reconnect, backoff, and health-state trace

Date: 2026-08-26

## Scope

This dossier traces how current Tailscale `magicsock` reacts when an established or attempted DERP connection fails, with particular attention to reconnect/backoff behavior and health reporting. It follows the prior external-admission and client-visible-denial research, but does **not** claim that every DERP reconnect error is caused by admission policy.

Upstream inspected at commit `d7253cb40e38cd71cdf4366246ff3078414b1662`.

Primary source paths:

- `wgengine/magicsock/derp.go`
- `util/backoff/backoff.go`
- `health/health.go`
- DERP HTTP/client behavior already mapped in the preceding admission dossiers

## Evidence level

**VERIFIED source architecture**, not runtime reproduction.

GitHub Gold inspected current upstream source. It did not deploy Tailscale, configure a rejecting external admission controller, inject network faults, capture reconnect traffic, or benchmark retry timing.

## Main finding

DERP reconnect behavior is owned primarily by the long-lived `magicsock` DERP reader loop, while DERP-home selection and user-visible health are separate layers.

The current `runDerpReader` loop creates a per-region backoff object:

```text
backoff.NewBackoff("derp-<region>", ..., 5*time.Second)
```

When `dc.RecvDetail()` returns an error, the loop:

1. marks that DERP region disconnected in the health tracker;
2. removes peer routes learned through the failed DERP connection;
3. exits immediately for an explicitly closed DERP client;
4. exits if the network is down or the connection context is cancelled;
5. otherwise logs the receive error;
6. triggers `ReSTUN("derp-recv-error")` because the failure may reflect changed network conditions;
7. invokes the backoff object before continuing the receive/reconnect loop.

A successful receive resets the backoff with `bo.BackOff(ctx, nil)`.

## Exact backoff semantics

The 5-second value passed by magicsock is **the maximum backoff parameter**, not a fixed reconnect interval.

The shared `util/backoff.Backoff` implementation tracks consecutive failures as `n` and computes the pre-jitter delay as:

```text
min(n² × 10 ms, maxBackoff)
```

It then multiplies that delay by a random factor in the range **0.5x to 1.5x** to reduce thundering-herd synchronization.

For DERP, `maxBackoff` is configured as 5 seconds. Because jitter is applied after the cap, the final sleep can be below or above 5 seconds; once the pre-jitter value has reached the cap, the randomized sleep is approximately **2.5 to 7.5 seconds**.

Illustrative pre-jitter progression:

- failure 1: 10 ms
- failure 2: 40 ms
- failure 3: 90 ms
- failure 4: 160 ms
- failure 5: 250 ms
- failure 10: 1 s
- failure 20: 4 s
- failure 23 and later: capped at 5 s before jitter

The implementation intentionally uses `n²` rather than exponential `2^n` growth because upstream describes quadratic growth as smoother.

If `BackOff` receives a nil error, it resets `n` to zero immediately. Cancellation also interrupts an in-progress timer through the supplied context.

Operationally, this means DERP reconnect is:

- very fast for the first few failures;
- progressively damped during repeated failure;
- jittered to avoid synchronized client reconnect storms;
- bounded rather than growing without limit;
- reset as soon as the reader observes a successful receive.

## Health-state transition

`runDerpReader` defers cleanup that marks the region disconnected and clears the region-specific health string when the reader exits.

On each receive failure it explicitly sets:

- `SetDERPRegionConnectedState(regionID, false)`

When the DERP server later supplies a `ServerInfoMessage`, magicsock sets:

- `SetDERPRegionConnectedState(regionID, true)`
- `SetDERPRegionHealth(regionID, "")`

and logs the successful connection generation.

Separately, a DERP `HealthMessage` can set a region-specific problem string through `SetDERPRegionHealth(regionID, m.Problem)`.

This yields three distinct health concepts that should not be collapsed:

1. **connection state** — whether a DERP region is currently considered connected;
2. **server-reported DERP health** — a problem string carried by DERP protocol health messages;
3. **fresh receive activity** — recorded separately through `NoteDERPRegionReceivedFrame` at a bounded cadence.

## ReSTUN is part of reconnect recovery

A receive error triggers `ReSTUN("derp-recv-error")` before the reconnect delay. This is significant because magicsock does not assume that a broken DERP connection is purely a server problem. It treats failure as a signal that local network conditions, paths, or NAT state may have changed and schedules fresh network probing.

This connects the DERP failure path to the broader direct-path system: a broken relay session can cause magicsock to reconsider network conditions rather than only reconnecting blindly to the same socket path.

## Home DERP selection is a separate policy layer

`maybeSetNearestDERP` and `setNearestDERP` own preferred/home DERP selection. That policy is not the same thing as the per-region reconnect loop.

Important behavior in current source:

- netcheck supplies a preferred DERP region;
- if UDP/netcheck cannot produce one, magicsock can choose a deterministic fallback;
- magicsock intentionally avoids changing an existing home DERP while disconnected from control, because peers could not reliably learn the new home;
- if no home DERP exists, selecting some DERP can still be better than none;
- a home-DERP change starts a connection to the newly selected region and notifies already connected DERP sessions of preferred status.

Therefore persistent failure of one DERP connection does not imply that the reader loop itself autonomously chooses a different home region. Reconnect, network re-evaluation, and preferred-region policy are related but separate mechanisms.

## Why persistent external-admission rejection is operationally awkward

The preceding source trace established that a DERP client may locally finish construction before positive server-side admission is observed, and that rejection does not carry a dedicated structured denial frame to the normal client.

Combined with the reconnect code above, a persistent policy rejection can plausibly enter the generic DERP failure/reconnect machinery rather than a specialized `admission denied` state.

Safe source-derived conclusion:

- reconnect/backoff and region connected-state handling are generic;
- current inspected magicsock code does not branch on a dedicated external-admission-denied protocol event;
- server-side policy context can therefore be richer than client-side reconnect telemetry.

Not established in this pass:

- exact user-visible error text under repeated admission rejection;
- exact sequence of reconnect attempts under a continuously rejecting controller;
- whether a particular caller suppresses or escalates repeated failures;
- whether health UI surfaces distinguish admission rejection from ordinary DERP transport failure.

Those require live reproduction or a higher-level health/UI trace.

## Write-path behavior

The DERP writer is intentionally simple: it reads queued `derpWriteRequest` objects and calls `dc.Send`.

On send errors it:

- logs the error;
- increments `metricSendDERPError`;
- increments outbound dropped-packet error metrics for non-disco packets.

The in-process write queue depth is currently 32. Upstream comments explicitly describe deeper queues as undesirable buffer bloat and note that connect/reconnect currently sits in the write path, which is why the queue exists at all.

This is another useful design principle: **bound the queue and fix connectivity/backpressure rather than hiding slow or broken relays behind ever-larger buffers.**

## Reusable architecture lessons

### 1. Keep reconnect separate from route policy

A transport reader can own retry/backoff while a higher policy layer owns preferred-region selection. This prevents every transient socket error from immediately rewriting network topology.

### 2. Couple relay failure to network re-evaluation

Triggering fresh network checks after relay receive errors acknowledges that the cause may be local path/NAT change, not only relay-server failure.

### 3. Use bounded jittered retry growth

Quadratic growth gives fast early recovery without allowing persistent failures to become a tight reconnect storm. Randomization reduces synchronized reconnect bursts across many clients.

### 4. Reset retry state only after observed success

The DERP reader clears its backoff after successful receive activity rather than merely after scheduling a new connection.

### 5. Distinguish connection state from server health

A boolean connected signal and a protocol-provided health problem string answer different operational questions and should remain separate.

### 6. Bound reconnect-adjacent queues

The 32-entry write queue is deliberately kept shallow. Upstream comments reject queue growth as the primary fix for slow/broken paths.

### 7. Do not over-interpret generic reconnect telemetry

A generic connection failure may represent server failure, network movement, control-plane issues, policy rejection, or transport errors. Admission-specific diagnosis requires admission-specific telemetry.

## Relationship to prior GitHub Gold dossiers

This dossier extends:

- `2026-08-25-derp-operational-failure-modes.md`
- `2026-08-26-derp-external-admission-controller.md`
- `2026-08-26-derp-admission-test-concurrency.md`
- `2026-08-26-derp-client-visible-admission-failure.md`

Together they now cover:

- server-side admission decision semantics;
- fail-open boundaries;
- admission-controller timeout and concurrency behavior;
- client-visible denial limitations;
- reconnect/backoff after generic DERP failures;
- exact retry-growth, jitter, cap, cancellation, and reset semantics;
- per-region health-state transitions;
- the separation between reconnect and home-DERP selection.

## Verification boundary

GitHub Gold did not:

- execute upstream tests;
- run `tailscaled` or `derper`;
- configure an external verifier;
- cause a live DERP rejection;
- packet-capture reconnect attempts;
- benchmark retry intervals;
- inspect every downstream health/UI consumer;
- independently security-audit Tailscale.

No third-party source code was copied into GitHub Gold.

## Strong next leads

1. Trace higher-level health consumers to see how repeated `SetDERPRegionConnectedState(false)` affects user-visible network-health reporting.
2. Search recent Tailscale issues/PRs for persistent DERP reconnect storms, admission diagnostics, or requests for admission-specific metrics.
3. Compare this generic reconnect model with Iroh relay `AccessControl` rejection and reconnection behavior.
4. Design an upstream-style in-memory regression test that proves the client-visible behavior of repeated external admission rejection without requiring public relay infrastructure.
5. Inspect whether any DERP-specific caller adds an additional retry/backoff layer around the `derphttp.Client` connection path.
