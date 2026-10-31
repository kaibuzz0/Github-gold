# dora-rs/dora `.drec` — resilient robotics record/replay subsystem

- **Upstream:** https://github.com/dora-rs/dora/tree/main/libraries/recording
- **Parent project:** https://github.com/dora-rs/dora
- **Author / Org:** dora-rs
- **Category:** robotics / deterministic debugging / record-replay / binary formats / Rust
- **Evidence:** VERIFIED
- **Provisional Gold score:** **A / 26**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 3/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** Apache-2.0 via parent workspace
- **Discovery source:** recursive component inspection from the existing `dora-rs/dora` S/29 dossier.

## What it is

Dora's `dora-recording` crate implements the binary `.drec` container used by the runtime's `dora record` / `dora replay` workflow. A recording stores a versioned header containing start time, dataflow UUID and the original YAML descriptor, followed by timestamped node/output records and an optional footer with message/byte totals.

The current source stamps **format version 2**. The framing is length-prefixed and event payloads are opaque to the container; the v2 transition changed event encoding from bincode to postcard. The reader deliberately rejects v1 instead of allowing downstream decode failures to masquerade as generic corruption.

## Why it matters

The value is not merely the file format. The implementation contains practical resilience patterns for recording high-rate robotics/sensor streams where capture can be interrupted or individual payloads can be pathological:

1. **Crash-tolerant tails** — a missing footer or partially written final record is treated as an interrupted capture; fully written records before the torn tail remain readable.
2. **Defensive parsing** — record/YAML sizes are capped at 64 MiB and decoded length fields are bounds/overflow checked before slicing or allocating.
3. **Oversized-message isolation** — a recorder can skip one oversized image/point-cloud record and continue capturing later messages instead of aborting the entire session.
4. **Selective replay scanning** — `next_entry_for_node` validates the stream while avoiding payload copies for records belonging to other nodes, useful because replay processes scan a common recording and retain only their own node's events.
5. **Descriptor provenance** — the original dataflow YAML is embedded in the recording header, which makes a capture more self-describing than a bare stream of timestamped payloads.
6. **Explicit format compatibility** — reader floors/ceilings provide a clear failure when an incompatible event encoding is encountered.

## Concrete implementation evidence

The recording crate is a real workspace package (`dora-recording`) rather than README-only functionality. Its `Cargo.toml` describes it as the recording format for Dora message capture/replay and inherits the workspace version/license.

`libraries/recording/src/lib.rs` contains `RecordingWriter`, `RecordingReader`, `RecordingHeader`, `RecordEntry`, `RecordEntryHeader`, and `RecordingFooter`, with generic `Read`/`Write` boundaries that allow files or in-memory buffers.

The implementation explicitly documents that this crate is **internal to Dora and not a stable public API**. It is published because other published Dora crates depend on it, but upstream warns that it may change even in a patch release. This materially reduces drop-in-library reusability despite the clean I/O abstraction.

## Test evidence inspected

The source contains focused unit tests for:

- header round-trip;
- single-record and multi-record round-trip;
- raw binary payload preservation;
- v1/pre-postcard format rejection;
- invalid magic rejection;
- empty descriptor handling;
- missing-footer behavior;
- graceful handling of a torn final record body;
- corrupt `node_id_len` rejection without panic;
- corrupt `event_bytes_len` rejection without panic;
- oversized-record rejection;
- skip-and-continue behavior after an oversized entry;
- exact encoded-length accounting.

These tests are unusually aligned with realistic recorder failure modes rather than only happy-path serialization.

## Useful components / patterns to mine

- `RecordingWriter<W: Write>` / `RecordingReader<R: Read>` generic stream boundary
- versioned binary framing with embedded provenance descriptor
- torn-tail recovery semantics
- checked length-prefixed parsing
- hard allocation/record-size ceilings
- skip-and-continue handling for pathological sensor frames
- metadata-only iteration with `next_entry_header`
- node-filtered scanning that avoids unnecessary payload copies
- explicit compatibility rejection when payload encoding changes

## Runtime / integration notes

The crate itself has a small direct dependency surface (`uuid`, `eyre`; `tempfile` for development tests), but real Dora replay also depends on the parent runtime's event encoding and replay-node behavior. The event bytes are intentionally opaque at the container layer, so using `.drec` outside Dora requires understanding the matching `Timestamped<InterDaemonEvent>` postcard schema/version.

The 64 MiB record ceiling is a deliberate safety boundary. Dora's live zero-copy path can carry messages larger than this, so recordings can be incomplete when oversized frames are skipped; callers are expected to count/report such skips.

## Licensing

The crate inherits Dora's **Apache-2.0** workspace license. No upstream source was copied into GitHub Gold. Any adaptation must preserve the applicable Apache license/NOTICE obligations and separately account for dependencies or surrounding integrations.

## Verification performed by GitHub Gold

Performed:

- inspected the crate manifest;
- inspected the current writer/reader implementation;
- inspected versioning, framing, size limits and corrupt-input handling;
- inspected source-level unit tests covering round-trip, truncation, malformed lengths and oversized records;
- confirmed the component is explicitly marked internal/unstable by upstream.

Not performed:

- did not compile the crate;
- did not execute its tests;
- did not create or replay a `.drec` file;
- did not benchmark large recordings or high-rate sensor streams;
- did not fuzz the parser;
- did not validate cross-version recordings against released Dora binaries;
- did not independently verify deterministic behavior of a full dataflow replay.

Therefore VERIFIED means the concrete implementation and targeted upstream test evidence were inspected, not that GitHub Gold independently reproduced runtime behavior.

## Caveats / risks

- **Internal API:** upstream explicitly excludes `dora-recording` from the Dora 1.0 stability guarantee; direct consumers can break on patch releases.
- **Not fully self-describing:** event payload interpretation depends on Dora's matching postcard event schema even though the container embeds the dataflow YAML.
- **Version discontinuity:** current code rejects v1 recordings because their event payloads use bincode; archival users need the matching older Dora release or a migration tool.
- **Torn-tail semantics favor salvage:** unexpected EOF at the final record body is treated as graceful end-of-recording. This is appropriate for crash recovery but means consumers needing forensic integrity should add independent checksums/signatures or stricter completeness validation.
- **No per-record checksum/authentication:** the inspected framing provides bounds checks and format validation, not cryptographic integrity/authenticity.
- **64 MiB ceiling:** large camera/point-cloud messages can be skipped, making a recording intentionally incomplete unless the caller surfaces the skip count.

## Follow-up leads

1. Inspect `binaries/record-node` and `binaries/replay-node` to determine how capture selection, skip accounting, timing/speed control and node substitution are wired around this library.
2. Evaluate whether the format has an index or seek strategy for very large recordings; the current reader is sequential.
3. Inspect the postcard `InterDaemonEvent` compatibility surface and whether a schema fingerprint should accompany future recordings.
4. Consider checksum/chunk-index extensions as a project idea for long-lived archival and random-access sensor datasets.
5. Compare Dora's replay semantics with downstream dataset replayers such as `enactic/dora-openarm-dataset-replayer` to distinguish runtime regression replay from ML-dataset episode replay.

## Verdict

**VERIFIED — A / 26.** The `.drec` subsystem is a compact, well-tested example of resilient robotics stream capture: it salvages clean records after interrupted writes, bounds untrusted lengths, isolates oversized messages, and avoids needless payload copies during node-filtered replay. It falls short of S primarily because the crate is intentionally unstable/internal, the format is coupled to Dora's event schema, and GitHub Gold has not independently executed or fuzzed it.