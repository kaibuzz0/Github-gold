# Syncthing BEP framing and connection loops

- Upstream: https://github.com/syncthing/syncthing/blob/main/lib/protocol/protocol.go
- Category: networking / synchronization protocol / reusable protocol design
- Evidence: VERIFIED (source inspection; not runtime-tested by GitHub Gold)
- Provisional Gold score: 27/30 (S)
- License: MPL-2.0 at inspected source file

## Why this is gold

Syncthing's `lib/protocol/protocol.go` is a compact example of a production binary protocol engine layered above an already-authenticated transport. `NewConnection` composes model wrapping, native/wire path conversion, optional encryption support, and a `rawConnection`. Starting the raw connection launches separate reader, dispatcher, writer, ping-sender, and ping-receiver goroutines.

## Wire framing

Each normal BEP message is encoded as:

1. 2-byte big-endian protobuf-header length;
2. protobuf `bep.Header` containing message type and compression mode;
3. 4-byte big-endian payload length;
4. protobuf message payload.

The reader rejects negative payload lengths and payloads above `MaxMessageLen` (500,000,000 bytes), allocates through a shared buffer pool, optionally LZ4-decompresses, then unmarshals according to the header's message type. Unknown message types are skipped by the reader loop for forward extensibility; unknown compression modes are errors.

## Protocol state and validation

The dispatcher requires `ClusterConfig` before ordinary traffic. After entering the ready state it handles Index, IndexUpdate, Request, Response and DownloadProgress messages. Incoming requests are bounded by `MaxRequestSize` (twice the 16 MiB maximum block size), must include a block hash, and filenames are checked for canonical folder-relative form. Index metadata receives additional consistency checks.

This is useful defensive protocol design: framing limits, state-machine validation, filename/path validation, semantic object validation and request-size limits occur before higher-level model handling.

## Request/response correlation and concurrency

Outgoing block requests receive monotonically incremented integer IDs stored in an `awaiting` map protected by a mutex. Responses resolve the matching channel and remove the entry. Incoming requests are dispatched asynchronously, allowing request processing without blocking the main dispatcher.

Index and IndexUpdate sending is separately serialized with `idxMut`. The writer itself owns serialization of actual wire writes through its channel-driven loop.

## Compression policy

BEP supports no compression or LZ4. Syncthing does not blindly compress everything. The configurable modes are Never, Always and Metadata. Even when compression is enabled, payloads below 128 bytes are not compressed. `writeCompressedMessage` also abandons compression unless it can save at least approximately 3.125% of bandwidth. Metadata mode excludes Response messages, avoiding compression of block-data responses.

## Liveness and shutdown

`Start` launches five loops: reader, dispatcher, writer, ping sender and ping receiver. Production constants define a 90-second ping-send interval and 300-second receive timeout. Normal `Close` attempts to send a BEP Close message with the reason before asynchronously tearing down the underlying connection; `CloseTimeout` bounds this graceful-close attempt.

## Verification performed

GitHub Gold inspected current upstream `lib/protocol/protocol.go`, including `NewConnection`, `Start`, `Request`, dispatcher validation, read framing, write framing, compression selection, request/response correlation and close handling.

GitHub Gold did not compile Syncthing, execute a BEP session, fuzz the parser, benchmark compression, transfer blocks, or independently audit concurrency/security properties. `VERIFIED` here means the described mechanisms are directly present in current upstream source, not that this run independently validated them at runtime.

## Reusable lessons

- Separate transport authentication/session establishment from application framing.
- Put hard framing and request-size bounds before allocation/dispatch where practical.
- Make protocol readiness explicit instead of accepting arbitrary message ordering.
- Correlate asynchronous requests without blocking the dispatcher.
- Treat compression as an economic decision: threshold it and require measurable savings.
- Keep I/O serialization in a dedicated writer path while allowing higher-level request concurrency.
- Design unknown-message behavior deliberately for forward compatibility.

## Caveats

The 500 MB protocol message ceiling is a protocol guard, not a claim that such messages are cheap or desirable. The architecture relies on surrounding Syncthing layers for authenticated peer identity, configuration policy, rate limiting and model semantics. Extracting this code requires MPL-2.0 compliance and review of imported dependencies.

## Follow-up leads

1. Inspect protocol tests/fuzz coverage for malformed lengths, compression and state ordering.
2. Inspect `lz4Compress`/`lz4Decompress` and buffer-pool limits for decompression/memory behavior.
3. Trace encrypted-folder wrappers around `NewConnection` and key-generation semantics.
4. Inspect BEP protobuf definitions and compatibility/versioning strategy.
