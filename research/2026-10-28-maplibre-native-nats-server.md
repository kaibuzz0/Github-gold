# MapLibre Native and NATS Server — GitHub Gold research (2026-10-28 UTC)

GitHub-first follow-up to `research/2026-09-05-maplibre-native-offline-cross-platform-map-renderer.md` and `research/2026-09-03-nats-server-messaging-jetstream-edge-runtime.md`. No YouTube transcript findings attributed. No independent builds, device tests, server deployments or security audits. No third-party source copied.

## MapLibre Native — VERIFIED / S29

Upstream: https://github.com/maplibre/maplibre-native . BSD-2-Clause root; additional notices in LICENSES.core.md and vendor; map data separately licensed. Core C++ renderer in `src/mln/renderer/`, style expression engine in `src/mln/style/expression/`, tile parsing in `src/mln/tile/`, SQLite-backed offline cache in `platform/default/src/mln/storage/offline_database.cpp`, PMTiles v3 header/directory/range reader in `platform/default/src/mln/storage/pmtiles_file_source.cpp`, offline CLI in `bin/offline.cpp`, and experimental plugin API in `include/mln/plugin/plugin_api.h`.

**Concrete recursive PMTiles integration:** `pmtiles_file_source.cpp` includes `pmtiles.hpp`, parses PMTiles headers and bounds its directory cache. Android [v13.7.1](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1) (2026-10-15) explicitly supports `pmtiles://asset://...` for APK-bundled PMTiles with range reads. iOS [v7.0.0](https://github.com/maplibre/maplibre-native/releases/tag/ios-v7.0.0) (2026-10-28 01:30 UTC) requires iOS >=15.5 and replaces Mapbox.h with MapLibre.h.

**Upstream main CI 2026-10-27:** [Android 10/10](https://github.com/maplibre/maplibre-native/actions/runs/40603579515) including OpenGL/Vulkan/multiBackend and C++/render tests; [iOS 6/6](https://github.com/maplibre/maplibre-native/actions/runs/40603579220); [Linux 6/6](https://github.com/maplibre/maplibre-native/actions/runs/40603579610). Separate [pr-linux-tests](https://github.com/maplibre/maplibre-native/actions/runs/40632794426) failed two benchmark/bloat jobs 2026-10-28; no passing benchmark claimed.

**Limitations:** Offline use requires licensed map tiles, styles, fonts and sprites; no independent archive or hardware tests. Untrusted vector tiles, PMTiles directory metadata, HTTP range bounds, GPU backends and experimental plugin ABI warrant testing. Related: protomaps/PMTiles, protomaps/go-pmtiles, maplibre/maplibre-compose, maplibre/maplibre-native-qt.

## NATS Server — VERIFIED / S29

Upstream: https://github.com/nats-io/nats-server . Apache-2.0 root, dependencies separate. Go server implements JetStream in `server/jetstream.go`, `jetstream_cluster.go`, `stream.go`, `consumer.go`; storage in `filestore.go`, `memstore.go`, `store.go`; consensus in `raft.go` and `raft_transport.go`; edge networking in `leafnode.go`, `route.go`, `gateway.go`; auth in `auth.go`, `auth_callout.go`; MQTT in `mqtt.go`; monitoring in `monitor.go`. Dedicated *_test.go fixtures exist.

Stable [v2.15.2](https://github.com/nats-io/nats-server/releases/tag/v2.15.2) and v2.14.9 published 2026-10-26. Release notes document fixes for OCSP response certificate-serial binding, auth-callout connection-type enforcement, oversized restored JetStream snapshots, leafnode MQTT ACL and MQTT OCSP option handling. Release Go 1.27.3 includes mitigation for CVE-2026-111943; current main go.mod separately specifies Go 1.26.0/toolchain 1.26.10.

**Upstream main CI:** [NATS Server Tests 21/21](https://github.com/nats-io/nats-server/actions/runs/40365928969) passed 2026-10-26 including Raft, JetStream, storage, MQTT, JWT, Windows and lint; [Long JetStream Tests](https://github.com/nats-io/nats-server/actions/runs/40507265134) and [govulncheck](https://github.com/nats-io/nats-server/actions/runs/40459212504) passed 2026-10-27.

**Limitations:** No independent execution, partition/failover, recovery, security or benchmark tests. Enforce TLS, least-privilege accounts and monitoring isolation; review 2.15 upgrade guide and backup/restore. Related: nats-io/nats.go, nats-io/natscli, nats-io/nkeys, nats-io/jwt, nats-io/nats-general.

## Maintenance and next research

PMTiles VERIFIED/S28 entry receives an upstream-proven MapLibre Native cross-reference, score unchanged. Open MCT remains PROMISING/A25: [2026-10-28 e2e-full](https://github.com/nasa/openmct/actions/runs/40608853694) failed npm ci (Node 18 vs required >=24); no Playwright tests executed. Next: offline APK PMTiles testing, tile parsing fuzzing, NATS JetStream snapshot restore and auth callout fail-closed tests. Playlist seeds inaccessible in prior runs; no fabricated transcript findings.
