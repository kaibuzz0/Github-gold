# Syncthing request IDs, cancellation lifetime, and higher-layer deadlines

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `lib/protocol/rawConnection.Request`, model `RequestGlobal`, send/receive pull path
- **Category:** protocol lifecycle / correlation IDs / cancellation / resource ownership
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **27/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** MPL-2.0 for inspected Syncthing source
- **Inspection date:** 2026-09-20

## Executive finding

This follow-up closes two questions left by the request-cancellation dossier: how request IDs advance, and whether the normal pull path adds its own request deadline.

`rawConnection.Request` protects `awaiting` and `nextID` with the same mutex. It assigns `id := c.nextID`, increments `nextID`, panics if the chosen ID is already present in `awaiting`, and then inserts a capacity-one result channel. There is no explicit request-ID wrap/reset policy in this path.

On ordinary Go targets `int` is machine-sized. Consequently, wrap is an extreme-lifetime concern rather than a practical short-run rollover mechanism, but the source does not contain a special wrap guard. If an eventually wrapped ID were still present in `awaiting`, the existing collision check would panic instead of silently overwriting the old correlation entry.

The higher-level normal pull path does **not** introduce a fixed per-block timeout in the inspected chain. `pullBlock` receives the folder operation context and passes that context through `model.RequestGlobal`; `RequestGlobal` forwards it directly to `conn.Request`. The folder pull code creates a cancellation context for pull-duration metrics, but the actual `pullerIteration` calls shown in the inspected source use the parent `ctx`, not a `context.WithTimeout` deadline.

This means request cancellation in the normal sync path is principally tied to the lifetime/cancellation of the enclosing folder operation rather than to a hard per-request wall-clock deadline visible in these call sites.

## Evidence

### Correlation ID allocation

`rawConnection.Request`:

1. creates `rc := make(chan asyncResult, 1)`;
2. locks `awaitingMut`;
3. copies `nextID` into the request ID;
4. increments `nextID`;
5. checks whether that ID is already in `awaiting` and panics on collision;
6. stores the channel in `awaiting`;
7. writes the ID into the wire request;
8. waits for either the response channel or `ctx.Done()`.

This makes allocation and collision detection atomic with respect to other request goroutines on the same connection.

### No explicit rollover policy observed

The inspected protocol source declares:

- `awaiting map[int]chan asyncResult`
- `nextID int`

and the request path increments `nextID` directly. Repository search for this protocol `nextID` surfaced this declaration/use but no dedicated rollover/reset routine for the protocol request counter.

The appropriate conclusion is narrow: **no explicit rollover handling was observed in the inspected source**. This dossier does not claim that integer rollover is reachable in realistic deployments.

### Pull path forwards caller context

`model.RequestGlobal` selects a usable device connection and then directly calls `conn.Request(ctx, &protocol.Request{...})` with the context it received. It does not add a timeout or replace that context.

`folder_sendrecv.go` passes its `ctx` into `RequestGlobal` while pulling a remote block. The puller iteration and worker routines are also created with that same operation context.

### Pull lifecycle cancellation, not fixed block timeout

The folder `pull` method creates `pullCtx, cancel := context.WithCancel(ctx)` for `addTimeUntilCancelled`, but the inspected loop invokes `f.pullerIteration(ctx, scanChan)`. Thus the derived `pullCtx` shown there is metric-lifetime plumbing, not evidence of a request deadline.

A repository search performed in this run did not surface a `context.WithTimeout` around `RequestGlobal` in the normal pull path.

## Why it matters

The combination of this dossier and the preceding cancellation dossier establishes a useful reusable design lesson for asynchronous request/response protocols:

- caller cancellation and correlation-table reclamation are separate lifecycle events;
- buffered response channels permit late delivery without blocking the dispatcher;
- monotonically increasing correlation IDs avoid routine reuse complexity;
- collision checks prevent silent map replacement;
- without a per-request deadline, abandoned correlation state can remain response-or-connection-bound after an enclosing caller cancels.

That pattern is useful to study when designing multiplexed RPC, P2P, relay, and framed-protocol implementations.

## Caveats

- No integer-overflow experiment was performed.
- No calculation here asserts a real-world time-to-wrap because request rate, architecture word size, connection lifetime, and workload vary.
- Repository search is evidence of what was found, not a formal proof that no timeout exists anywhere in every alternate Syncthing request caller.
- The conclusion about the normal pull path is based on the directly traced `pullBlock -> RequestGlobal -> conn.Request` chain.
- The previous finding still applies: cancellation returns promptly to the caller, while an `awaiting` entry is removed by a matching response or connection teardown rather than by the cancellation branch itself.

## Verification performed

GitHub Gold inspected upstream:

- `lib/protocol/protocol.go` request allocation/cancellation path;
- protocol `nextID` search results;
- `lib/model/model.go` `RequestGlobal` implementation;
- `lib/model/folder_sendrecv.go` pull lifecycle and puller iteration;
- repository searches for timeout/cancellation-related call sites.

## Verification NOT performed

GitHub Gold did **not**:

- build or run Syncthing;
- force request-ID overflow;
- measure request rates or realistic rollover time;
- simulate a permanently nonresponding peer;
- profile retained correlation entries;
- prove absence of timeouts in unrelated API/internal callers;
- fuzz request IDs or cancellation races.

## Licensing

The inspected Syncthing source is MPL-2.0. No upstream implementation source was copied into GitHub Gold; this dossier records architecture and evidence only.

## Next research queue

1. Inspect protocol tests specifically for `Request` cancellation, late response, and connection-close cleanup.
2. Determine whether any test deliberately exercises duplicate/colliding response IDs or unknown response IDs.
3. Inspect dispatcher behavior for unsolicited/late responses after teardown boundaries.
4. Quantify the bookkeeping retained per canceled outstanding request using a controlled upstream benchmark or test rather than source-only estimation.
5. Rotate discovery away from Syncthing after this protocol thread is sufficiently closed, returning to broader GitHub Gold category coverage.
