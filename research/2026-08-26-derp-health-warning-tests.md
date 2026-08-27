# DERP health warning test semantics

Date: 2026-08-26

Status: VERIFIED SOURCE-LEVEL RESEARCH

Scope: Tailscale health warning visibility/debounce behavior, with emphasis on what upstream tests actually prove for delayed DERP-facing health states.

## Executive finding

Tailscale's health framework has explicit regression coverage for delayed warning visibility. The test is generic rather than DERP-specific, but it exercises the exact `Warnable.TimeToVisible` mechanism used by the current DERP warnings `No home relay server` and `Relay server unavailable`.

The upstream test establishes two important semantics:

1. a warning with `TimeToVisible` must not publish an unhealthy event before the delay expires;
2. if the condition becomes healthy again before the visibility delay expires, neither the transient unhealthy state nor a compensating healthy event is published to watchers.

This means the 10-second delays on the current DERP home/unavailable warnings are not simply presentation metadata. They participate in a tested debounce mechanism intended to suppress short-lived connectivity failures before they become visible health events.

## Current DERP warnables

Current Tailscale source defines:

- `noDERPHomeWarnable`: title `No home relay server`, medium severity, connectivity-impacting, `TimeToVisible: 10 * time.Second`, dependent on network health;
- `noDERPConnectionWarnable`: title `Relay server unavailable`, medium severity, connectivity-impacting, `TimeToVisible: 10 * time.Second`, dependent on network health and the no-home-DERP condition;
- `derpTimeoutWarnable`: title `Relay server timed out`, medium severity, dependent on network health plus the home/connection warnables, with no separate `TimeToVisible` field in the warnable definition.

The dependency graph matters because a more fundamental network or home-DERP failure can suppress a downstream relay symptom rather than exposing multiple competing warnings.

## Upstream test coverage for `TimeToVisible`

The current `health/health_test.go` contains `TestSetUnhealthyWithTimeToVisible`. It creates a synthetic warnable with a two-second visibility delay, installs a watcher through the health event bus, and advances a controlled test clock.

Observed test behavior:

- after only half the delay, no unhealthy or healthy watcher event is expected;
- after the full delay elapses, the unhealthy event must be delivered;
- after resetting the warnable to healthy, a healthy event is delivered for the already-visible warning;
- when the warnable is set unhealthy and then immediately healthy before the visibility delay elapses, advancing beyond the delay must produce neither unhealthy nor healthy watcher events.

This directly validates the health framework's transient-failure suppression behavior.

## What this proves for DERP

Because the DERP home and connection warnables use the same `Warnable.TimeToVisible` mechanism, current source plus the generic regression test support the following architecture conclusion:

- a brief home-DERP selection/connection problem that clears inside the 10-second visibility window should not become a visible health event through this mechanism;
- a sustained condition that remains unhealthy beyond the visibility delay can become visible and propagate through the health event bus;
- once a warning has become visible, returning it to healthy can generate the corresponding health-state transition;
- transient unhealthy states that never become visible are intentionally collapsed rather than generating noisy unhealthy/healthy pairs.

This is useful for interpreting repeated DERP reconnects: transport failures may occur internally without every short failure surfacing to ordinary frontend health.

## Important test-coverage boundary

The inspected test is framework-level, not a dedicated end-to-end DERP transition test. This pass did not find evidence in the inspected snippets of a test that drives a real `magicsock` DERP region from connected to disconnected, advances exactly 10 seconds, and asserts the final `Relay server unavailable` frontend notification.

Therefore GitHub Gold records two separate confidence levels:

- VERIFIED: generic `TimeToVisible` debounce semantics are covered by upstream tests;
- NOT VERIFIED IN THIS PASS: a DERP-specific integration test covering the complete `magicsock -> health.Tracker -> LocalBackend -> frontend Notify.Health` chain at the 10-second boundary.

Absence from this source search is not proof that no such integration/private test exists elsewhere.

## Reusable architecture lesson

A robust health system should separate raw fault detection from user-visible warning publication. Tailscale's design provides a reusable pattern:

1. producers report raw unhealthy/healthy state;
2. each warning declares its own visibility delay and dependencies;
3. the health tracker suppresses transient states until their delay expires;
4. warnings that recover before visibility do not generate noisy event pairs;
5. consumers receive normalized health events rather than raw transport churn.

This is especially appropriate for mobile and roaming peer-to-peer networks where path changes and relay reconnects are expected during normal operation.

## Suggested next regression target

A focused DERP integration regression test would be valuable if upstream coverage does not already exist. The test should use a controlled clock and assert at least:

- selected home DERP starts connected;
- home DERP becomes disconnected;
- no `Relay server unavailable` visible state before 10 seconds;
- disconnect clears before 10 seconds -> no visible warning;
- sustained disconnect beyond 10 seconds -> warning visible;
- reconnect after visibility -> warning cleared;
- network-down dependency suppresses the DERP-specific warning;
- a stale-but-still-connected DERP eventually exercises the separate timeout warning path.

This would validate the full state-propagation chain rather than only the generic health timer primitive.

## Verification boundary

GitHub Gold inspected current public Tailscale source and tests. It did not run the Go test suite, modify upstream source, deploy `tailscaled`, inject DERP failures, or inspect private test infrastructure. No third-party source code is copied into this repository.

## Sources inspected

- `tailscale/tailscale/health/warnings.go`
- `tailscale/tailscale/health/health_test.go`
- prior branch research tracing DERP connection state into health and frontend notification

## Follow-up leads

1. Search for DERP-specific integration tests outside `health/health_test.go` that exercise home-region transitions.
2. Trace one concrete frontend consumer that renders `ipn.Notify.Health` and determine whether it preserves severity, connectivity impact, code, and dependency context.
3. Compare Tailscale's delayed health publication with Iroh's relay connection/error propagation model.
4. Inspect recent upstream issues/PRs mentioning relay health false positives, home-DERP flapping, or warning debounce.