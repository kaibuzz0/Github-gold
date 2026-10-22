# Maintenance evidence — OpenObserve, Loro, go-libp2p (2026-10-22)

**Scope:** Three existing catalog records. Evidence is upstream source, license and release inspection, not independent execution. No third-party implementation code copied.

## OpenObserve — VERIFIED (upstream), S/27
- Repository: https://github.com/openobserve/openobserve
- Release: https://github.com/openobserve/openobserve/releases/tag/v1.1.2 (2026-10-20)
- License: https://github.com/openobserve/openobserve/blob/main/LICENSE (AGPL-3.0)
- Score: Utility 5 + Working Evidence 4 + Reusability 4 + Novelty 4 + Documentation 5 + Maintenance 5 = **27**. Reduced from provisional 29 because cost/performance claims lack independent benchmarks and whole-platform AGPL/enterprise boundaries constrain reuse.
- Inspected: https://github.com/openobserve/openobserve/blob/main/src/api/grpc/src/handler/grpc/request/otlp.rs (OTLP HTTP-to-gRPC response mapping); https://github.com/openobserve/openobserve/blob/main/src/config/src/meta/otlp.rs (request-type tests); https://github.com/openobserve/openobserve/blob/main/src/core/src/profiles/dictionary_compat.rs (profile dictionary handling).
- Upstream release notes report PromQL alert and single-series query fixes, a disk-cache race fix, Kubernetes object-query fixes, stale cluster-peer routing fix and RED-insight gap fix. These are release claims; no independent deployment or regression run.
- Follow-up: locate release-specific regression tests, check OSS/enterprise boundaries, and measure performance under representative ingest/query workloads.

## Loro — VERIFIED (upstream), S/28
- Repository: https://github.com/loro-dev/loro
- Releases: https://github.com/loro-dev/loro/releases — `loro-crdt@1.16.4` and experimental `loro.js@0.3.0` (2026-09-30).
- License: https://github.com/loro-dev/loro/blob/main/LICENSE (MIT); preserve notice and review separate binding licenses.
- Score: Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 4 = **28**.
- Inspected: https://github.com/loro-dev/loro/blob/main/crates/loro-internal/src/container/richtext/fugue_span.rs (Fugue span representation); https://github.com/loro-dev/loro/blob/main/crates/loro/README.md (Rust delta sync APIs); https://github.com/loro-dev/loro/blob/main/loro-js/README.md (experimental pure-TypeScript runtime).
- The experimental runtime documents causally pending remote updates excluded from normal snapshots; `exportPendingUpdates()` supports a sidecar checkpoint. Upstream release notes describe convergence fixes. Neither Rust/JS interoperability nor out-of-order recovery was independently executed.
- Follow-up: compare concurrent move/delete and delayed causal update behavior across Rust/WASM and pure TypeScript.

## go-libp2p — VERIFIED (upstream), S/29
- Repository: https://github.com/libp2p/go-libp2p
- Release: https://github.com/libp2p/go-libp2p/releases/tag/v0.50.0 (2026-09-21).
- License: https://github.com/libp2p/go-libp2p/blob/master/LICENSE (MIT); dependencies and transport integrations require separate license review.
- Score: Utility 5 + Working Evidence 4 + Reusability 5 + Novelty 5 + Documentation 5 + Maintenance 5 = **29**.
- Inspected: https://github.com/libp2p/go-libp2p/blob/master/p2p/protocol/holepunch/svc.go (DCUtR); https://github.com/libp2p/go-libp2p/blob/master/p2p/host/autonat/autonat.go (reachability confidence); https://github.com/libp2p/go-libp2p/blob/master/p2p/protocol/autonatv2/autonat.go (dialback and anti-amplification).
- Upstream release notes mention reachability stress testing, hole-punch timeout correction, HTTP authentication input hardening, and QUIC/WebTransport dependency upgrades. **Go 1.26** required. No independent build, network traversal or security test.
- Recursive leads: libp2p/specs, go-libp2p-pubsub, go-libp2p-kad-dht, rust-libp2p. Not promoted in this batch.

## Discovery limitations and next steps
These projects were already in the canonical catalog; no new repositories were added. Two registered YouTube playlist pages were retried but access was throttled; no transcript claims made. Four legacy entries still lack structured scoring: OUI-SPY Unified Blue, termux-adb, ESP32-S3 Remote ID Add-on, App Manager. Avoid copying any source until component-specific licenses are checked.
