# DERP reconnect, backoff, and health-state trace

Date: 2026-08-26

## Scope

This dossier traces how current Tailscale `magicsock` reacts when an established or attempted DERP connection fails, with particular attention to reconnect/backoff behavior and health reporting. It follows the prior external-admission and client-visible-denial research, but does **not** claim that every DERP reconnect error is caused by admission policy.

Upstream inspected at commit `d7253cb40e38cd71cdf4366246ff3078414b1662`.

Primary source paths:

- `wgengine/magicsock/derp.go`
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

## What the 5-second value means

The constructor is given a 5-second duration, but this research pass does **not** treat that as a guaranteed constant retry interval. The imported `util/backoff` implementation was not fully re-derived here, so the safe claim is:

- magicsock uses Tailscale's shared backoff helper;
- the DERP reader configures it with a 5-second parameter;
- failure retries are intentionally delayed rather than tight-looped;
- success resets the backoff state.

Do not rewrite this as "DERP retries exactly every five seconds" without separately inspecting and validating `util/backoff` semantics.

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

Combined with the reconnect code above, a persistent policy rejection can plausibly enter the generic DERP failure/reconnect machinery rather than a specialized "admission denied" state.

Safe source-derived conclusion:

- reconnect/backoff and region connected-state handling are generic;
- current inspected magicsock code does not branch on a dedicated external-admission-denied protocol event;
- server-side policy context can therefore be richer than client-side reconnect telemetry.

Not established in this pass:

- exact user-visible error text under repeated admission rejection;
- exact retry timing under a continuously rejecting controller;
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

### 3. Reset retry state only after observed success

The DERP reader clears its backoff after successful receive activity rather than merely after scheduling a new connection.

### 4. Distinguish connection state from server health

A boolean connected signal and a protocol-provided health problem string answer different operational questions and should remain separate.

### 5. Bound reconnect-adjacent queues

The 32-entry write queue is deliberately kept shallow. Upstream comments reject queue growth as the primary fix for slow/broken paths.

### 6. Do not over-interpret generic reconnect telemetry

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

1. Inspect `util/backoff` to derive the exact delay/jitter/reset semantics behind the 5-second DERP configuration.
2. Trace higher-level health consumers to see how repeated `SetDERPRegionConnectedState(false)` affects user-visible network-health reporting.
3. Search recent Tailscale issues/PRs for persistent DERP reconnect storms, admission diagnostics, or requests for admission-specific metrics.
4. Compare this generic reconnect model with Iroh relay `AccessControl` rejection and reconnection behavior.
5. Design an upstream-style in-memory regression test that proves the client-visible behavior of repeated external admission rejection without requiring public relay infrastructure.
