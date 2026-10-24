# Syncthing protocol request cancellation and late-response ownership

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `lib/protocol` request/response correlation (`rawConnection.Request`, `handleResponse`, `internalClose`)
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 — S tier
- **License:** MPL-2.0 for the inspected Syncthing source. No upstream implementation source copied here.
- **Research date:** 2026-09-20

## Why this matters

The previous dossier traced response-buffer ownership but left a narrower lifecycle question: what happens to an `awaiting` request entry if the caller's context is canceled before the peer responds?

The current implementation has a subtle but bounded-by-connection behavior worth recording. Cancellation returns promptly to the caller, but it does not itself remove the request ID from `rawConnection.awaiting`. The entry is removed later by a matching response or by connection teardown.

## Source-traced lifecycle

`rawConnection.Request` first rejects an already-closed connection or already-canceled context. It then creates a **buffered channel of capacity one**, assigns the next request ID, and inserts that channel into the `awaiting` map under `awaitingMut`.

The request is sent with the caller's context. If `send` fails because the connection closes or the context becomes canceled while the send is pending, `Request` returns `ErrClosed`; the code path shown does not delete the map entry at that point.

After a successful send, `Request` waits on either the response channel or `ctx.Done()`. If the context wins, it returns `ctx.Err()` immediately. Again, that cancellation branch does not delete the corresponding `awaiting` entry.

When a response eventually arrives, `handleResponse` locks `awaitingMut`, looks up the response ID, deletes the matching map entry, sends the `asyncResult` into the buffered channel, and closes the channel. Because the channel has capacity one, this late-response send does not require the original caller to still be receiving from it. The map/bookkeeping entry is therefore reclaimed when the late response is dispatched.

If the peer never responds, `internalClose` provides the second cleanup path: connection teardown closes every non-nil awaiting channel and deletes every entry from the map.

## Practical interpretation

The implementation favors prompt caller cancellation without a separate protocol-level request-cancel message. A canceled request can consequently remain represented in `awaiting` until either:

1. its peer response arrives, or
2. the connection closes.

That means cancellation is **not immediate bookkeeping reclamation**. On a long-lived connection to a peer that accepts requests but never sends responses, repeated caller cancellations can leave request-channel/map entries live for longer than the caller itself. The retained object per request is small relative to block payloads (map entry + buffered channel/bookkeeping), and this source review does not establish an exploitable memory-exhaustion condition or quantify heap cost.

A late response does not appear to deadlock `handleResponse`: it deletes the map entry first and can place one result into the abandoned channel's single buffer. The response payload then remains reachable through that channel until the channel/map/result become unreachable and garbage collection can reclaim them. This dossier does not claim exact GC timing or protobuf backing-memory behavior.

Connection shutdown is explicit and comprehensive for outstanding request bookkeeping: `internalClose` closes and deletes all remaining awaiting channels while holding `awaitingMut`.

## Verification boundary

Verified directly from current upstream source structure:

- request IDs/channels are inserted into `awaiting` before send;
- caller context cancellation returns without an explicit `awaiting` deletion in `Request`;
- matching responses delete the map entry and deliver through a capacity-one channel;
- connection teardown closes and deletes all outstanding entries.

Not performed:

- no Syncthing build or runtime execution;
- no cancellation stress test;
- no heap/RSS profiling;
- no adversarial peer simulation;
- no measurement of retained bytes per canceled request;
- no claim that this constitutes a vulnerability.

## Reusable engineering lesson

This is a useful correlation-map design case study: a buffered one-shot result channel makes late delivery non-blocking after caller abandonment, while connection teardown guarantees eventual cleanup. The tradeoff is that context cancellation alone does not retire the correlation entry. Systems adapting this pattern should decide explicitly whether they need immediate cancellation cleanup, a request-cancel wire message, expiry/timeout sweeping, or a bound on outstanding correlation entries.

## Strong next leads

1. Inspect tests around `rawConnection.Request` for cancellation/late-response coverage.
2. Determine whether higher layers impose request deadlines that bound how often cancellation occurs while a connection stays alive.
3. Quantify the approximate heap footprint of an abandoned `awaiting` entry and a late response buffered after caller cancellation.
4. Check whether request-ID growth/wrap behavior has dedicated tests or guards under extremely long-lived connections.
