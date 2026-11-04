# MeshSat Android — DTN fragmentation, reassembly, and custody transfer

- **Upstream:** https://github.com/meshsat/meshsat-android
- **Author/org:** MeshSat
- **Category:** DTN / resilient messaging / Android / intermittent networks
- **Evidence:** PROMISING (source inspected; upstream test evidence is partial and one documented test surface could not be located)
- **Provisional Gold score:** **24/30 — A tier**
  - Utility 5/5
  - Working Evidence 3/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 3/5
- **License:** GPL-3.0 at repository root; no source copied into GitHub Gold
- **Discovery:** component-level follow-up from the MeshSat Android dossier

## Why it matters

This is a compact delay/disruption-tolerant transport layer intended for bearers with small MTUs and intermittent connectivity. The useful boundary is not the Android UI: it is the combination of MTU-aware fragmentation, out-of-order reassembly, bounded incomplete-bundle lifetime, and explicit point-to-point custody handoff.

The component is potentially reusable as a reference for satellite, LoRa, packet-radio, store-and-forward, and other constrained transports, but the present implementation should not be treated as a hardened general-purpose DTN stack.

## Fragmentation

`BundleFragmenter` subtracts the protocol fragment-header size from the caller-supplied MTU, rejects MTUs that cannot contain the header, generates a shared bundle ID, and splits the payload into indexed fragments. Even a payload that fits in one fragment receives a fragment header for wire-format consistency.

Each fragment records bundle ID, fragment index, total fragment count, and original total size. This makes reassembly independent of arrival ordering.

## Reassembly

`BundleReassembler` keys incomplete state by bundle ID and uses a `ConcurrentHashMap`, allowing fragments to arrive from different interface threads. It stores fragments by index and reconstructs only after the expected count is present. The default incomplete-bundle lifetime is five minutes; `pruneStale()` removes older state.

Upstream tests directly exercise a 1,000-byte fragmentation/reassembly round trip with MTU 340, a single-fragment payload, reverse-order delivery, and fragment-header field preservation. The same test file checks little-endian fragment-header round trips and custody offer/ACK wire-format compatibility.

## Custody transfer

`CustodyManager` implements an explicit point-to-point handoff rather than broadcast custody:

1. sender creates a custody offer and records local OFFERED state;
2. receiver accepts only while below a configurable capacity (default 100 records);
3. receiver signs `custodyId || localDestHash` through a caller-provided signing callback and returns a custody ACK on the same interface;
4. sender matches the ACK by custody ID, marks the record transferred, and removes it from pending custody state.

The wire-format tests establish type `0x16` for custody offers and `0x17` for custody ACKs; the ACK test expects a 97-byte encoded structure with a 64-byte signature.

## Important verification caveat

Upstream `steering/test-strategy.md` lists `BundleFragmenterTest.kt`, `BundleReassemblerTest.kt`, and `CustodyManagerTest.kt` as DTN tests. During this inspection, GitHub Gold located `BundleFragmenterTest.kt` and its concrete fragmentation/reassembly and custody wire-format tests, but an exact repository search/fetch did **not** locate `CustodyManagerTest.kt` on the current default branch. Therefore the documented test inventory appears at least partly stale or incomplete, and the custody state-machine implementation is not credited here with a dedicated located test suite.

This is why the component is classified PROMISING rather than VERIFIED despite the parent MeshSat Android project having stronger whole-project evidence.

## Security / robustness observations

The custody receiver creates a signature through a callback, but `processAck()` itself only looks up the custody ID and transitions/removes the record; this class does not verify the ACK signature. Verification may occur elsewhere in the delivery pipeline, but that was not established in this pass. A future audit should trace the full receive path before treating signed custody ACKs as authenticated end-to-end behavior.

The reassembler accepts metadata from the first fragment that creates a bundle record and does not, in the inspected class, visibly enforce global limits on total size, fragment count, number of pending bundles, or per-bundle memory. Its five-minute pruning is useful, but hostile-input/resource-exhaustion behavior deserves explicit fuzz/bounds testing before reuse on an exposed transport.

## Licensing

The parent repository is GPL-3.0. No implementation source was copied into GitHub Gold. Any extraction or adaptation must preserve applicable GPL obligations and review upstream third-party notices.

## Verification boundary

GitHub Gold inspected the current implementation of `BundleFragmenter.kt`, `BundleReassembler.kt`, `CustodyManager.kt`, repository search results, and the located `BundleFragmenterTest.kt`. GitHub Gold did **not**:

- compile or run the Android/JVM tests;
- inject loss, duplication, corruption, or malicious fragment metadata;
- test large payloads or memory exhaustion;
- exercise real LoRa, Iridium, APRS, BLE, TCP, or Reticulum links;
- verify custody ACK signatures through the complete receive pipeline;
- establish persistence of custody/reassembly state across process death;
- benchmark throughput, latency, memory, or battery cost.

## Strong follow-up leads

1. Trace custody ACK signature verification through the complete delivery pipeline.
2. Determine whether custody state survives Android process death/restart or is intentionally ephemeral.
3. Add/locate adversarial tests for fragment-count/total-size bounds, conflicting metadata, duplicates, corruption, and incomplete-bundle flooding.
4. Inspect the adjacent Reed-Solomon/RLNC implementation separately, including algorithm provenance and tests.
5. Rotate the main research stream away from MeshSat after this component pass to preserve catalog breadth.
