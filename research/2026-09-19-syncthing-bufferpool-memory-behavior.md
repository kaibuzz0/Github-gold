# Syncthing BufferPool memory behavior

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `lib/protocol/bufferpool.go`, `lib/protocol/bufferpool_test.go`, block-size constants in `lib/protocol/protocol.go`
- **Category:** P2P synchronization / memory reuse / buffer pooling / protocol implementation
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 — S
- **License:** MPL-2.0 for the inspected source and tests
- **Discovery:** Recursive follow-up from the BEP LZ4 memory-bounds dossier

## Why this is Gold

Syncthing's global protocol `BufferPool` is a compact, reusable example of size-classed byte-buffer reuse. It avoids pooling oversized protocol buffers, rounds ordinary allocations into known block-size buckets, can satisfy a request from its fitting bucket or any larger bucket, and exposes atomic hit/miss/put/skip counters useful for observing behavior. The implementation is small enough to audit directly and has upstream concurrency/stress coverage.

## Implementation evidence

`BufferPool` contains one `sync.Pool` per protocol block size. `BlockSizes` is initialized by doubling from `MinBlockSize` through `MaxBlockSize`; current constants are 128 KiB minimum and 16 MiB maximum, yielding size classes of 128 KiB, 256 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, 8 MiB, and 16 MiB.

`Get(size)` behaves differently by size:

- requests above 16 MiB bypass pooling and allocate exactly the requested size;
- requests within the pool range first try the fitting bucket and then progressively larger buckets;
- on a miss, very small requests below `MinBlockSize/64` allocate exactly their requested size rather than paying for a 128 KiB bucket;
- other misses allocate the fitting bucket capacity and return a slice shortened to the requested length.

`Put` only retains buffers whose capacity exactly belongs to the supported block-size range. Buffers above 16 MiB or below 128 KiB are skipped. A noncanonical capacity inside the nominal range would fail the exact bucket lookup rather than silently entering a mismatched pool; callers are explicitly required to return only slices obtained from `Get`.

The pool tracks puts, skips, misses, and per-bucket hits with atomics.

## Memory-retention boundary

This component does **not** impose an explicit byte budget, item-count ceiling, per-peer quota, or global retained-buffer cap. Each size class is backed by Go's `sync.Pool`, so retention/reclamation is delegated to the runtime rather than managed by a deterministic cache limit in this code.

That matters for interpreting the previous LZ4 finding. Decompressed messages above `MaxBlockSize` (16 MiB) are not retained by this BufferPool when returned; they are allocated directly and skipped on `Put`. Thus a permitted decompressed message approaching the 500 MB BEP message ceiling can create substantial transient allocation pressure, but this specific pool does not intentionally cache that giant allocation afterward.

Conversely, ordinary concurrent protocol/file operations can hold or recycle many buffers up to 16 MiB each. The source provides no simple fixed aggregate-memory bound based only on the number of buckets because concurrent borrowers and runtime-managed `sync.Pool` contents determine actual memory use.

## Upstream test evidence

`bufferpool_test.go` verifies bucket selection and panic behavior for invalid bucket capacities. Its non-short stress test launches 10 goroutines for two seconds; each repeatedly obtains ten buffers of random sizes spanning below-minimum through above-maximum, checks returned lengths, returns them, and finally requires that put, skip, miss, and hit paths were all exercised.

This is useful concurrency evidence for the allocator/recycler mechanics, but it is not a memory-pressure benchmark and does not establish a maximum resident-memory footprint.

## Reusable pieces

- size-classed `sync.Pool` array;
- fitting-or-larger bucket reuse;
- exact allocation for very small requests;
- deliberate non-pooling of oversized buffers;
- exact-capacity validation on return;
- low-cost atomic pool telemetry;
- concurrent randomized stress-test pattern.

## Verification boundary

GitHub Gold inspected the current upstream implementation, constants, and tests. GitHub Gold did **not** run the stress test, profile heap/RSS behavior, force garbage collections, benchmark allocation rates, simulate many peers, or experimentally measure `sync.Pool` retention.

`VERIFIED` therefore refers to direct source and upstream-test evidence for the documented allocation/pooling rules, not to an independent runtime memory benchmark.

## Caveats

- `sync.Pool` is runtime-managed; this source does not provide deterministic retention or eviction guarantees.
- The absence of an explicit retained-byte cap means this component alone cannot establish a global memory ceiling.
- A 500 MB BEP/LZ4 message can still create large transient allocations even though buffers above 16 MiB bypass this pool.
- Pooling reduces allocation churn but can trade some memory retention for reuse.
- Source reuse must comply with MPL-2.0; no upstream code was copied into GitHub Gold.

## Follow-up leads

1. Trace all major `BufferPool.Get` call sites and their concurrency controls to estimate realistic simultaneous borrowers.
2. Inspect request-limiting / puller concurrency settings that bound block-level allocations per peer/folder.
3. Search upstream benchmarks, issues, and memory profiling work for observed BufferPool pressure under large deployments.
4. Inspect Go runtime `sync.Pool` behavior only as a separate implementation/runtime dependency; do not conflate runtime semantics with guarantees made by Syncthing itself.
