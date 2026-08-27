# DERP health propagation from magicsock to frontends

Date: 2026-08-26

## Scope

This dossier closes the next open boundary in the DERP reconnect research: how per-region DERP connectivity state becomes a user-facing Tailscale health warning.

Upstream inspected at commit `a7769cbc33a3eba62bb16fc803b97077c2969d16`.

Primary source paths:

- `wgengine/magicsock/derp.go`
- `health/health.go`
- `health/warnings.go`
- `ipn/ipnlocal/local.go`

## Evidence level

**VERIFIED source architecture**, not runtime/UI reproduction.

GitHub Gold inspected current upstream source. It did not run `tailscaled`, inject DERP failures, capture frontend notifications, or verify the rendering behavior of every platform GUI.

## Main finding

`SetDERPRegionConnectedState(region, connected)` is not itself a UI event. It writes per-region connection state into the central health tracker and immediately invokes the tracker's self-check logic.

That self-check converts low-level DERP state into higher-level `Warnable` health objects. `LocalBackend` subscribes to health changes, logs each changed warnable, calls `health.CurrentState()`, and sends the resulting full health state to frontends in `ipn.Notify{Health: state}`.

The propagation chain is therefore:

1. magicsock DERP reader observes transport state;
2. `health.Tracker` stores DERP region connection/freshness state;
3. `selfCheckLocked` evaluates DERP-specific warning conditions;
4. warnable state changes are published through the health event bus;
5. `LocalBackend.onHealthChange` receives the change;
6. `LocalBackend` sends the current health snapshot to frontend consumers.

This is a useful architecture boundary: transport code reports facts, the health layer derives policy-visible warnings, and frontends receive normalized health state instead of DERP implementation details.

## DERP warning state machine

Current health self-check logic treats the home DERP specially.

### No home DERP

If Tailscale wants to be running, is actively map-polling, is not intentionally "homeless", and still has no home DERP, the tracker marks `noDERPHomeWarnable` unhealthy.

The warning is defined as:

- title: `No home relay server`;
- severity: medium;
- impacts connectivity: true;
- visibility delay: 10 seconds;
- dependency: network status must otherwise be healthy/relevant.

This means startup and short-lived home-selection gaps are intentionally filtered rather than surfaced immediately.

### Home DERP selected but disconnected

If a home DERP exists but `derpRegionConnected[homeDERP]` is false, the tracker marks `noDERPConnectionWarnable` unhealthy and includes the DERP region ID/name as arguments.

The warning is defined as:

- title: `Relay server unavailable`;
- severity: medium;
- impacts connectivity: true;
- visibility delay: 10 seconds;
- dependencies: network status and the no-home-DERP warning.

This is the direct higher-level consumer of repeated `SetDERPRegionConnectedState(false)` for the selected home region.

A key nuance is that the warning is specifically home-DERP oriented in current source. The warning definition notes that, although it could theoretically represent failure to connect to another region, the current use is for the home DERP.

### Connected but no recent DERP frames

When the home DERP is marked connected, `noDERPConnectionWarnable` is cleared. The tracker then checks the last received DERP frame.

Current source defines an idle threshold of:

`2 minutes + 5 seconds`

If the last frame is older than that threshold, `derpTimeoutWarnable` becomes unhealthy and includes the region name plus the rounded idle duration.

The warning is:

- title: `Relay server timed out`;
- severity: medium;
- dependent on network status, a valid home DERP, and an active DERP connection.

This creates a useful distinction between:

- **socket/region disconnected** -> `Relay server unavailable`;
- **region marked connected but silent** -> `Relay server timed out`.

Those are separate operational failure classes.

## Startup and state-change suppression

The health self-check deliberately suppresses several DERP warnings when the node has only just been turned on or when it is not yet in map polling.

Current source considers the user to have `recentlyOn` status for the first **5 seconds** after the desired-running state transitions true. During that window, the no-home, no-connection, and DERP-timeout warnings are forced healthy.

Combined with the warnables' own 10-second visibility delays, this prevents common startup transients from immediately becoming user-visible errors.

This is stronger than simply adding retry backoff in magicsock: reconnect damping controls transport behavior, while health visibility delays independently control user-facing noise.

## Dependency-based warning suppression

DERP warnables use explicit dependency relationships.

Examples:

- `noDERPHomeWarnable` depends on the network-status warning;
- `noDERPConnectionWarnable` depends on network status and no-home-DERP state;
- `derpTimeoutWarnable` depends on network status, an active DERP connection, and a known home DERP.

The health model documents that if a dependency is unhealthy, a dependent warning can be treated as irrelevant by UI consumers.

This avoids stacking redundant errors. For example, if the entire network is down, the UI does not need to emphasize a separate DERP timeout as though it were an independent root cause.

## Frontend propagation

The health tracker emits change events whenever a warnable becomes unhealthy, changes unhealthy state, or becomes healthy.

`LocalBackend.onHealthChange` handles those events. For warnable changes it logs either:

- `health(warnable=<code>): ok`, or
- `health(warnable=<code>): error: <text>`.

Then, regardless of which single warning changed, it retrieves the current aggregate health state and sends it to frontends through:

`ipn.Notify{Health: state}`

This means frontends receive a normalized current health snapshot rather than having to reconstruct DERP connection state from transport callbacks.

The `Warnable` type itself carries UI-oriented metadata such as:

- globally unique code;
- title;
- severity;
- user-displayable text;
- dependency relationships;
- `ImpactsConnectivity`;
- `TimeToVisible`.

Upstream comments explicitly state that GUI implementations can use severity and connectivity impact to decide presentation behavior; for supported tray-icon platforms, an unhealthy warning with `ImpactsConnectivity` can cause an exclamation indicator.

## What repeated DERP rejection looks like at the health layer

The prior admission/reconnect dossiers established that external admission rejection can collapse into generic DERP connection failure from the normal client's perspective.

The health trace now narrows the consequence:

- if a home DERP remains selected but repeatedly fails to become/stay connected, the health layer can surface `Relay server unavailable` after the relevant suppression/visibility windows;
- if a connection is considered established but stops delivering frames for more than roughly 2m5s, the separate `Relay server timed out` path can fire;
- the warning text is transport/relay-oriented, not external-admission-specific.

Therefore persistent external policy rejection can plausibly become a generic relay-unavailable user-visible health state, while the DERP server logs retain the richer admission reason.

This remains a source-derived architectural conclusion, not a claim about one exact platform notification under a live rejecting controller.

## Reusable architecture lessons

### 1. Keep transport facts separate from user-facing diagnosis

Magicsock reports connection/freshness state. The health layer decides whether that state is warning-worthy.

### 2. Add a visibility debounce independent of retry backoff

Fast reconnect attempts and quiet user-facing health are different concerns. Tailscale implements both separately.

### 3. Distinguish disconnected from connected-but-stalled

A boolean connection state and a frame-freshness timer capture different failure modes and produce different warnings.

### 4. Use dependency graphs to suppress secondary symptoms

If the underlying network is down, downstream relay warnings can be deprioritized rather than overwhelming the user with cascading symptoms.

### 5. Push normalized health snapshots to frontends

Frontends consume a stable health model with severity/text/dependency metadata instead of depending on internal DERP state-machine details.

### 6. Preserve diagnostic specificity at the layer that owns it

The health layer intentionally speaks in user-relevant relay terms. Admission-policy detail remains server-side unless the protocol grows an explicit structured denial signal.

## Relationship to prior GitHub Gold dossiers

This dossier extends:

- `2026-08-25-derp-operational-failure-modes.md`
- `2026-08-26-derp-external-admission-controller.md`
- `2026-08-26-derp-admission-test-concurrency.md`
- `2026-08-26-derp-client-visible-admission-failure.md`
- `2026-08-26-derp-reconnect-health.md`

Together they now trace the path from external admission decision -> client transport failure -> generic reconnect/backoff -> per-region health facts -> normalized frontend health notification.

## Verification boundary

GitHub Gold did not:

- run Tailscale;
- execute upstream health tests;
- force a home-DERP outage;
- configure a rejecting external admission controller;
- inspect every platform GUI renderer;
- verify tray-icon behavior on a live client;
- independently security-audit the health subsystem.

No third-party source code was copied into GitHub Gold.

## Strong next leads

1. Inspect `health/health_test.go` for DERP warning-transition coverage and visibility-timer edge cases.
2. Trace one concrete frontend/client consumer of `ipn.Notify.Health` to document how severity, dependencies, and `ImpactsConnectivity` are rendered.
3. Search recent Tailscale issues/PRs for user reports of relay-unavailable warnings under reconnect storms or policy rejection.
4. Compare Tailscale's normalized health-snapshot model with Iroh relay rejection/error propagation.
5. Design a focused upstream-style test that drives home-DERP connected/disconnected state and verifies warning debounce plus dependency suppression.