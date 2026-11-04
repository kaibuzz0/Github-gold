# Syncthing puller memory concurrency bounds

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `lib/model/folder_sendrecv.go`
- **Category:** synchronization / concurrency / memory-pressure controls
- **Evidence:** VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — S
- **License:** MPL-2.0 (upstream Syncthing source; no source copied here)
- **Discovery:** recursive follow-up from the BufferPool/LZ4 memory investigation

## Why this matters

The protocol BufferPool dossier established that buffers above 16 MiB are not retained by the pool, but that finding alone did not say how many ordinary block buffers may be live at once. The send/receive folder implementation adds explicit concurrency and byte-budget controls around the two important block paths: local copying and remote pulling.

## Source-backed findings

### 1. Folder copy concurrency has a CPU-derived ceiling

`newSendReceiveFolder` treats `Copiers` as a broader folder-runner concurrency setting, defaults it to 2 when configured as zero, and caps it at `2 * runtime.NumCPU()`. `pullerIteration` then creates exactly `f.Copiers` copier goroutines and `f.Copiers` finisher goroutines, with channels buffered to the same value.

This matters because `copyBlock` obtains one `protocol.BufferPool` buffer of `block.Size` and defers its return. Therefore the local-copy path has a straightforward source-level concurrency relationship: at most the active copier routines can simultaneously be inside this block-copy function for one folder iteration. This is a concurrency bound, not a complete process-memory bound.

### 2. Remote block requests are limited by pending bytes, not just goroutine count

`pullerRoutine` constructs a weighted semaphore with capacity `PullerMaxPendingKiB * 1024`. Before launching a goroutine for a non-empty block, it takes `state.block.Size` bytes from that semaphore; the goroutine returns the same weight only after `pullBlock` completes.

The default pending budget is `2 * protocol.MaxBlockSize`. If a user configures zero, that default is used. If a nonzero configured value is smaller than one protocol maximum block, Syncthing raises it to at least `protocol.MaxBlockSize`.

Consequently, the normal remote pull path has an explicit per-folder in-flight byte budget around block requests. With default settings, pending requested block bytes are budgeted at two maximum-size blocks. A user can intentionally configure a larger budget, so this is not a universal fixed ceiling.

### 3. The byte token spans network fetch, verification, and disk write

The semaphore token is acquired before the goroutine starts and released with a deferred `Give(bytes)` after `pullBlock` returns. Inside `pullBlock`, Syncthing chooses a candidate device, calls `RequestGlobal`, verifies the returned block hash for ordinary folders, and writes the buffer to the temporary file before completion.

That placement is important: the limiter is not merely throttling request issuance. Its accounting covers the period in which returned block data can be resident and processed by the pull path.

### 4. Local-copy and remote-pull budgets are separate

Each copier can allocate a BufferPool block while searching the current file and indexed folders for reusable data. Blocks that cannot be copied are queued to the single `pullerRoutine`, which then applies the weighted pending-byte semaphore to remote requests.

Therefore it would be incorrect to claim that `PullerMaxPendingKiB` bounds *all* block-sized memory in the folder runner. Copy buffers, remote response buffers, protocol framing, database work, filesystem buffers, encryption wrappers, and other process allocations can coexist.

### 5. The limits are per folder runner, not a demonstrated process-wide memory cap

The semaphore is created inside a folder's `pullerRoutine`, and `Copiers` belongs to that folder configuration. Multiple folders can therefore have independent work in flight. The inspected code does not establish a single global BufferPool-byte budget across all folders or peers.

This is the main remaining aggregate-memory caveat: per-folder controls substantially constrain ordinary pull concurrency, but process-wide peak memory depends on simultaneously active folders plus protocol/network and non-puller allocations.

## Reusable design ideas

- Use a **weighted byte semaphore** when task memory roughly scales with payload size; a goroutine-count semaphore alone treats tiny and maximum-size blocks as equivalent.
- Hold the token across the complete resource lifetime (fetch → verify → persist), not only request dispatch.
- Combine a CPU-derived worker cap for local work with a byte-derived cap for network payloads.
- Normalize unsafe/ineffective configuration values upward to one atomic maximum payload so a legal block cannot deadlock against a too-small semaphore capacity.

## Verification boundary

GitHub Gold inspected the current upstream source paths and traced the relevant call sites. It did **not** run Syncthing, measure heap/RSS, simulate many folders or peers, benchmark the semaphore, or prove a process-wide maximum resident set. `VERIFIED` here means the documented concurrency and accounting behavior is directly supported by upstream source.

## Licensing caveat

The inspected Syncthing source is MPL-2.0. This dossier describes behavior and does not copy implementation source. Any extraction or adaptation of code requires preserving applicable MPL notices and obligations.

## Strongest follow-ups

1. Trace `RequestGlobal` / `requestResponse` ownership to determine exactly when protocol BufferPool response buffers are returned.
2. Quantify whether protocol reader buffers coexist with model request-response buffers or are copied between them.
3. Inspect global I/O and connection-level limiters for additional cross-folder constraints.
4. Search upstream issues/benchmarks for measured memory behavior under many simultaneously active folders/peers.
