# Syncthing request/response buffer ownership and wire-copy lifetime

- **Upstream:** https://github.com/syncthing/syncthing
- **Components:** `lib/model/model.go`, `lib/protocol/protocol.go`, `lib/protocol/bep_request_response.go`
- **Category:** synchronization / protocol / memory ownership / backpressure
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — S
- **License:** MPL-2.0 (upstream Syncthing source; no source copied here)
- **Discovery:** recursive follow-up from the puller memory/concurrency investigation

## Why this matters

The previous dossier established per-folder concurrency and byte budgets around outbound block pulls, but left open exactly how block buffers are owned while a peer serves a request and while the requester receives the response. This trace shows an explicit ownership contract on the serving side and identifies a real, bounded overlap between the disk-read buffer and the serialized wire buffer.

## Source-backed findings

### 1. Incoming block requests allocate their payload through BufferPool

The model's `requestResponse` owns a `[]byte` obtained from `protocol.BufferPool.Get(size)`. Its `Close` method is guarded by `sync.Once`, returns that byte slice to `BufferPool`, and closes a completion channel. `Wait` blocks on that channel.

The public protocol `RequestResponse` interface documents the ownership rule directly: `Close()` must always be called once the byte slice is no longer in use, while `Wait()` blocks until that happens.

### 2. Serving-side request memory is byte-limited until the response is released

`model.Request` creates the result through `newLimitedRequestResponse(req.Size, limiter, m.globalRequestLimiter)`. That helper takes `size` bytes from the applicable semaphores before allocating the response buffer. A goroutine waits for `requestResponse.Close()` and only then gives those bytes back.

There are two layers visible in the model: a per-device/connection request limiter and a global incoming-request limiter. Device `MaxRequestKiB` values create per-device byte capacities; the default path uses the puller pending-byte default. The model-wide limiter is initialized from `MaxConcurrentIncomingRequestKiB()` and can be resized on configuration changes.

This is stronger than a goroutine-count limit: accounting follows requested payload bytes and remains charged for the lifetime of the response object.

### 3. The disk-read buffer remains owned until the protocol writer finishes

`rawConnection.handleRequest` receives the model's `RequestResponse`, builds a BEP `Response` whose `Data` points at `res.Data()`, and sends it with a `done` channel. It then blocks on `<-done` and calls `res.Close()` only after the writer has completed processing that outgoing message.

That handshake prevents the model buffer from being returned to BufferPool while the asynchronous writer still needs its contents.

### 4. Serialization creates a temporary overlapping wire buffer

`writeMessage` computes the protobuf message size, obtains a second BufferPool buffer large enough for framing plus the serialized message, marshals the response into that buffer, writes it to the connection, and returns the wire buffer afterward.

For an uncompressed block response, the serving process therefore has a source block buffer and a serialized/framed output buffer live at the same time during the write. This is an important correction to any memory estimate that counts only the request-response payload buffer.

Compression can add another temporary buffer: `writeCompressedMessage` obtains a separate candidate compressed-output buffer while the ordinary marshaled payload remains available. The compression path only proceeds when it achieves the configured minimum savings.

### 5. The receiving reader's framing buffer has a short lifetime

`readMessageAfterHeader` validates the wire message length against `MaxMessageLen`, obtains a BufferPool buffer for the encoded payload, reads the frame, optionally decompresses it, unmarshals it into a typed protobuf message, and returns. The function defers return of its framing buffer to BufferPool.

`responseFromWire` then exposes the decoded BEP response's `Data` slice through the protocol `Response`, and `handleResponse` transfers that slice to the channel associated with the matching request ID. `rawConnection.Request` returns the received slice to its caller.

The source establishes that the temporary frame buffer is returned when message decoding finishes and that the decoded response data continues through the awaiting-request path. This dossier does **not** claim a zero-copy receive path or a specific protobuf allocation strategy without runtime/allocation evidence.

### 6. Request correlation itself is explicit and bounded by caller concurrency

Outbound `rawConnection.Request` allocates a buffered one-result channel, assigns a monotonically increasing request ID, stores the channel in the `awaiting` map, sends the request, and waits for either the matching result or context cancellation. `handleResponse` deletes the matching map entry before delivering the result.

The puller dossier's weighted byte semaphore therefore remains the important caller-side control for normal block-fetch concurrency. The protocol layer can support multiple outstanding IDs, but the ordinary pull path accounts payload bytes before launching those requests.

## Reusable design ideas

- Make buffer ownership explicit with a response object whose `Close` releases both memory and byte-budget tokens.
- Keep limiter accounting active until the asynchronous writer has definitively finished consuming the source buffer.
- Use a completion channel between request handling and a serialized writer to avoid premature buffer reuse.
- Budget for serialization overlap: application payload buffers and wire/framing buffers can coexist even when both use the same pool abstraction.
- Separate per-peer byte limits from a global incoming-request byte limit to constrain both individual and aggregate request pressure.

## Verification boundary

GitHub Gold inspected current upstream source at commit `bb19c017ae672b766338e21ab8c4d8ef6024fae3` and traced the ownership/control path. It did **not** run Syncthing, measure allocations or RSS, inspect Go protobuf runtime allocation behavior dynamically, benchmark compressed/uncompressed writes, or prove a process-wide peak-memory formula. `VERIFIED` means the described ownership, limiter, completion, and BufferPool call paths are directly present in upstream source.

## Licensing caveat

The inspected Syncthing files are MPL-2.0. This dossier describes behavior and copies no implementation source. Any future extraction or adaptation must preserve applicable MPL notices and obligations.

## Strongest follow-ups

1. Quantify serialization overlap with Go allocation benchmarks for maximum-size block responses.
2. Inspect protobuf generated/runtime behavior to determine whether response `bytes` fields necessarily copy out of the reader frame buffer in the current dependency version.
3. Trace context-cancellation cleanup for entries in the protocol `awaiting` map and confirm late-response behavior.
4. Combine per-device incoming request limits, the global request limiter, puller byte budgets, and folder concurrency into a conservative process-level memory-pressure model.
