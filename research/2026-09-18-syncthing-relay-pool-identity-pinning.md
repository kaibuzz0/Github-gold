# Syncthing relay pool identity pinning and advertisement

- **Upstream:** https://github.com/syncthing/syncthing/tree/main/cmd/infra/strelaypoolsrv
- **Related producer:** https://github.com/syncthing/syncthing/tree/main/cmd/strelaysrv
- **Category:** networking / relay infrastructure / service discovery / identity pinning
- **Evidence:** VERIFIED (source-inspected; upstream runtime testing exists, but not executed by GitHub Gold)
- **Provisional Gold score:** 27/30 — S tier
  - Utility 5/5
  - Working evidence 5/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- **Language:** Go
- **License:** MIT for `cmd/infra/strelaypoolsrv`; dependencies/imported packages require their own license review

## Why this matters

This closes an important trust-model question from the static relay-client dossier: whether relay URLs delivered by Syncthing's public relay-pool path retain the `id=` certificate identity pin.

The answer from current upstream source is **yes for the normal `strelaysrv` -> relay-pool -> short endpoint path**. The relay server constructs its advertised URI itself, derives a Syncthing DeviceID from its TLS certificate, and places that ID in the URI query. The pool preserves that `id` when producing its short endpoint response. The pool additionally tests a joining relay before accepting it.

This is stronger evidence than merely observing example URLs because it traces the producer, registration path, validation path, and consumer-facing serialization.

## Evidence chain

### 1. `strelaysrv` generates an identity-bearing URI

`cmd/strelaysrv/main.go` derives `id := protocol.NewDeviceID(cert.Certificate[0])`, constructs `relay://<mapped address>/`, and sets `id=<derived device ID>` in the URL query. The same URI also carries operational metadata such as ping/network timeouts, limits, status address, and provider attribution when configured.

When pool registration is enabled, that URI is handed to `poolHandler`.

### 2. Pool registration sends the URI as structured JSON

`cmd/strelaysrv/pool.go` copies the URI, refreshes its host from the current NAT mapping, and POSTs JSON containing `{ "url": <relay URI> }` to each configured pool. On success it uses the pool's `evictionIn` response to re-register before eviction (80% of the returned lifetime). Transient errors retry after a minute; an unauthorized response stops that pool-registration loop.

This means NAT-address refresh does not discard the identity query parameters.

### 3. The pool canonicalizes and validates joining relays

`cmd/infra/strelaypoolsrv/main.go` parses and canonicalizes the submitted URL. If the registration request itself supplied a TLS client certificate, the pool derives a DeviceID from that certificate and rejects a submitted URL whose advertised `id` differs.

The pool also applies address-origin checks: an unspecified advertised IP is replaced with the observed client IP, while a conflicting explicit IP is rejected when no registration TLS certificate is available.

Most importantly, a candidate is not inserted immediately. It is queued for `client.TestRelay(...)`; only a successful relay test proceeds into `knownRelays`. Repeated failed joins feed an IP error tracker/blocking mechanism.

### 4. The public short endpoint deliberately preserves `id`

`GET /endpoint` emits a compact relay list. Before serialization each URL passes through `slimURL`.

`slimURL` intentionally removes the relay's auxiliary query metadata but copies `id` into a fresh query when present. Upstream has a dedicated `TestSlimURL` asserting that a URL containing limits, timeouts, provider/status metadata and `id` is reduced to a relay URL retaining only `id`.

Therefore the dynamic relay client consuming the default relay endpoint receives identity-bearing URLs from the normal public-pool registration path, enabling the static client's certificate/DeviceID comparison described in the previous dossier.

## Important trust boundary

Do **not** generalize this finding to every syntactically valid `relay://` URI.

The static client permits a URI without `id`, in which case certificate/DeviceID comparison is skipped. Private manually configured relay URLs, permanent pool entries loaded from operator-controlled files, alternate pool implementations, or other externally supplied relay URLs need separate provenance analysis.

For the standard current `strelaysrv` registration flow, however, the server generates `id` from its certificate and the public pool's compact endpoint preserves it.

## Reusable components / patterns

- certificate-derived service identity embedded in endpoint metadata;
- registry-side consistency checking between registration certificate and advertised identity;
- active health/protocol test before admitting a service into discovery;
- NAT-aware advertised-address correction;
- bounded admission queue with HTTP 429 overload behavior;
- failure tracking / temporary blocking for repeatedly bad registrants;
- lease/eviction registration with proactive renewal;
- metadata minimization at the public lookup boundary while preserving the security-critical identity field;
- separate full-metadata and compact discovery endpoints;
- Prometheus instrumentation around API and relay-test activity.

These patterns are broadly reusable for self-hosted service registries, rendezvous systems, peer-discovery infrastructure, and small federated service pools.

## Licensing

`cmd/infra/strelaypoolsrv/LICENSE` is MIT. That makes the pool-server component comparatively reuse-friendly, but imported Syncthing packages and third-party dependencies must still be reviewed individually before source extraction. This dossier links upstream only; no third-party source was copied.

## Verification performed by GitHub Gold

Performed:

- inspected current `cmd/strelaysrv/main.go` URI construction;
- inspected current `cmd/strelaysrv/pool.go` registration/renewal behavior;
- inspected current `cmd/infra/strelaypoolsrv/main.go` registration, relay testing, endpoint serialization and `slimURL` behavior;
- inspected upstream `TestSlimURL`;
- inspected the component-level MIT license and README.

Not performed:

- did not build or run `strelaypoolsrv` or `strelaysrv`;
- did not query the live `relays.syncthing.net` endpoint;
- did not register a relay with the production pool;
- did not execute `client.TestRelay`;
- did not test mismatched certificates/IDs, NAT rewriting, blocklisting or eviction timing;
- did not independently audit TLS or relay protocol security.

## Caveats

- `id` preservation is established for URLs that contain `id`; `slimURL` does not invent one when absent.
- Registration-certificate-to-advertised-ID comparison is conditional on a TLS peer certificate being present on the pool registration request.
- Active `TestRelay` admission provides functional evidence but should not be described as a comprehensive security audit.
- Permanent relay entries and nonstandard/private pools need separate provenance and pinning review.

## Strong next leads

1. Inspect the live/default pool deployment configuration and permanent-relay source to determine whether every default endpoint entry is identity pinned in practice.
2. Inspect `client.TestRelay` end-to-end to document exactly what pool admission proves (TLS/ALPN, JoinRelay, session behavior, retries).
3. Trace dynamic endpoint fetching and parsing into `staticClient` to complete the full registry -> selection -> pinned connection chain.
4. Inspect pool persistence (`saveKnownRelays` / load paths), GeoIP/stat collection, and eviction semantics as reusable registry patterns.
