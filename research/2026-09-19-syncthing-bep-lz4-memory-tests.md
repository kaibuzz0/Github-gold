# Syncthing BEP LZ4 memory bounds and protocol tests

- Upstream: https://github.com/syncthing/syncthing/blob/main/lib/protocol/protocol.go
- Tests: https://github.com/syncthing/syncthing/blob/main/lib/protocol/protocol_test.go
- Category: networking / synchronization protocol / defensive parsing / reusable protocol design
- Evidence: VERIFIED (source and upstream-test inspection; not runtime-tested by GitHub Gold)
- Provisional Gold score: 27/30 (S)
- License: MPL-2.0 at inspected source/test files

## Why this is gold

This follow-up closes the main memory-safety question left by the BEP framing dossier: Syncthing does not trust the LZ4 block's advertised decompressed size without a ceiling. The compressed BEP payload itself is already limited by `MaxMessageLen`; `lz4Decompress` then reads the four-byte uncompressed-size prefix and independently rejects values above the same 500,000,000-byte `MaxMessageLen` before requesting the destination buffer.

That gives the receive path two explicit size gates: one on the wire payload and another on the decompressed allocation request. This does not make 500 MB cheap, but it prevents an LZ4 prefix from requesting an unbounded allocation.

## Exact decompression path

`readMessage` first rejects a framed payload above `MaxMessageLen`, obtains a pooled buffer for the compressed payload, reads it fully, and dispatches LZ4 payloads to `lz4Decompress`.

`lz4Decompress`:

1. rejects compressed payloads shorter than four bytes;
2. interprets the first four bytes as a big-endian uncompressed length;
3. rejects that length when it exceeds `MaxMessageLen`;
4. obtains a destination buffer from `BufferPool` sized to the advertised length;
5. calls `lz4.UncompressBlock` on the remaining compressed bytes;
6. returns the destination buffer to the pool on decompression error;
7. returns the successfully decompressed slice on success.

The parser then protobuf-unmarshals the decompressed bytes into the message type selected by the BEP header.

## Upstream test evidence

`protocol_test.go` contains direct round-trip compression coverage in `TestWriteCompressed`: it writes and rereads a 10 KiB Response in both highly compressible and randomized/incompressible forms and verifies the payload is unchanged. The test additionally checks that compression does not enlarge the resulting message.

`TestLZ4Compression` repeatedly compresses and decompresses partially randomized buffers and checks exact length and byte equality. `TestLZ4CompressionUpdate` contains a historical compressed fixture from Syncthing 1.18.6 and earlier, verifies current code can decompress it, and verifies the current compressor emits equivalent bytes. This is useful explicit backward-compatibility evidence for the compression format.

The same protocol test file also exercises connection lifecycle/state behavior such as ping, close paths, blocking-send close behavior, close races and the requirement that ClusterConfig precede ordinary traffic.

## Fuzzing boundary

A repository code search for `Fuzz` did not surface a Go fuzz target in `lib/protocol`; the matches were unrelated uses of the word or fuzz-like tests elsewhere. Therefore this dossier does **not** claim dedicated native fuzz coverage for BEP framing or LZ4 parsing. Absence from this search is not proof that no external fuzzing infrastructure exists; it is a current-repository evidence limitation.

## Verification performed

GitHub Gold inspected current upstream `lib/protocol/protocol.go` around `readMessage`, `lz4Compress`, and `lz4Decompress`, plus current `lib/protocol/protocol_test.go` evidence for connection behavior and LZ4 round trips/compatibility.

GitHub Gold did not compile or execute these tests, fuzz malformed compressed blocks, profile memory, attempt resource exhaustion, or independently security-audit the LZ4 dependency. `VERIFIED` means the documented guards and upstream tests are directly present in source.

## Reusable lessons

- Bound compressed wire input and advertised decompressed output independently.
- Validate an embedded decompressed-size prefix before allocating its destination.
- Return pooled buffers on decompression failure.
- Keep historical compressed fixtures to detect format regressions across implementation upgrades.
- Test both compressible and intentionally incompressible data so fallback behavior is covered.
- Do not equate unit/compatibility tests with fuzzing or adversarial resource-exhaustion validation.

## Caveats

The 500 MB ceiling remains large enough to create meaningful transient memory pressure, especially with multiple concurrent peers/messages; this run did not quantify aggregate limits or `BufferPool` retention behavior. The destination buffer is sized from an attacker-controlled length only after the 500 MB ceiling check, so bounded does not mean inexpensive. Dependency-level LZ4 safety is outside this dossier.

## Follow-up leads

1. Inspect `BufferPool` implementation, bucket sizes, retention and concurrent memory behavior.
2. Search CI/workflows and external Syncthing infrastructure for protocol fuzzing not visible as Go `Fuzz*` functions.
3. Inspect encrypted-folder wrappers and key-generation semantics around `NewConnection`.
4. Inspect BEP protobuf definitions and compatibility/versioning strategy.
