# Syncthing dynamic relay selection (`lib/relay/client/dynamic.go`)

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/lib/relay/client/dynamic.go
- **Repository:** https://github.com/syncthing/syncthing
- **Category:** P2P networking / relay discovery / failover / latency-aware selection
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — S tier
- **License:** MPL-2.0 at Syncthing repository root. No upstream source copied here.
- **Discovery:** Recursive follow-up from the Syncthing relay-server/session research branch.

## What it does

`dynamicClient` converts a `dynamic+...` relay-pool URI into the underlying HTTP(S) pool endpoint, requests a relay announcement, parses the returned relay URLs, orders candidate relays by measured latency, and hands each candidate to the existing static relay client until a connection can be maintained or the candidate set is exhausted.

The announcement shape is intentionally small: a JSON object containing a `relays` array whose entries expose a relay `url`.

## Selection algorithm

`relayAddressesOrder` measures each candidate with `osutil.GetLatencyForURL`. It quantizes latency into 50 ms buckets using integer division, shuffles candidates within each bucket, sorts bucket IDs from lowest to highest latency, then flattens the buckets in that order.

This is a useful compromise between strict lowest-latency selection and load concentration: relays with roughly equivalent latency are randomized rather than deterministically preferring a single endpoint. A latency probe failure is assigned `time.Hour`, effectively placing that candidate into a very poor bucket rather than immediately deleting it from the candidate set.

Context cancellation is checked during latency measurement and while iterating candidates.

## Failover / lifecycle behavior

For each ordered address, the client parses the URL, creates a `staticClient`, publishes it behind an RWMutex, and calls its `Serve(ctx)`. When that static client disconnects/returns, the dynamic client clears the current-client pointer and advances to the next ordered candidate. If no candidate remains connectable, it returns `could not find a connectable relay`.

`Error()` and `URI()` delegate to the currently selected static client while one exists; access is guarded by the RWMutex.

This is sequential failover, not parallel racing. The current implementation does not appear in this file to periodically re-query the pool while a selected static relay remains connected; a fresh dynamic-client serve cycle is therefore an important lifecycle boundary to inspect elsewhere before making stronger claims about pool refresh behavior.

## Evidence / useful components

- small HTTP/JSON relay-pool discovery client;
- User-Agent set from Syncthing build metadata;
- latency-aware 50 ms bucket ranking;
- randomized tie handling within latency buckets;
- sequential static-client failover;
- context-aware cancellation;
- mutex-protected handoff/delegation to the active relay client.

## Why it matters

This is a compact, reusable architecture pattern for selecting service endpoints without overfitting to tiny latency differences. Bucketing plus randomization can reduce deterministic herd behavior while still preferring materially closer endpoints. The separation between dynamic discovery/selection and a static endpoint client also keeps transport/session logic out of the selection layer.

## Caveats

- GitHub Gold did not compile or execute this package.
- No live relay-pool request, latency measurement, failover test, or packet capture was performed.
- No dedicated `dynamic_test.go` exists in the current `lib/relay/client` directory listing; only `empty_test.go` is present there, so this specific selection path does not have obvious colocated unit-test evidence from that directory inspection.
- This dossier does not independently establish how `GetLatencyForURL` measures every supported relay URI; inspect `osutil` before relying on transport-specific assumptions.
- HTTP response status handling, response-size limits, retry/backoff behavior, pool refresh cadence, and static-client TLS/device-ID validation should be evaluated in their respective layers before treating this as a standalone hardened discovery client.
- MPL-2.0 obligations apply to covered Syncthing source. Link rather than copy unless reuse requirements are deliberately handled.

## Verification performed

Directly inspected current upstream `lib/relay/client/dynamic.go`, the current `lib/relay/client` directory listing, and the Syncthing root MPL-2.0 license. GitHub Gold performed source review only.

## Strong next leads

1. Inspect `osutil.GetLatencyForURL` to determine exact latency-probe semantics by URI scheme.
2. Inspect `static.go` for reconnect behavior, certificate/device-ID validation, keepalive and invitation handling.
3. Trace who constructs/restarts `dynamicClient` to establish pool re-query and backoff cadence.
4. Search broader tests for dynamic relay selection/failover coverage outside `lib/relay/client`.
5. Compare bucketed randomized selection with relay-pool load/uptime metadata, if the pool exposes it, before proposing smarter ranking.