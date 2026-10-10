# CertMagic — automatic TLS certificate lifecycle for Go

- **Repository:** https://github.com/caddyserver/certmagic
- **Author / Org:** Caddy / caddyserver
- **Category:** networking / TLS / PKI / ACME / certificate automation / Go library / self-hosting infrastructure
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30**
- **Provisional tier:** **S**
- **Discovery:** Recursive follow-up from the Caddy dossier; GitHub-first. No YouTube-derived technical claim used.
- **License:** Apache-2.0 at repository root.

## Executive assessment

CertMagic is the reusable automatic-certificate-management library underneath Caddy. It embeds ACME-driven certificate issuance, renewal, TLS configuration, certificate caching, OCSP handling, issuer fallback, distributed coordination, pluggable storage, DNS-provider integration, and on-demand certificate acquisition into Go applications.

This is GitHub Gold because the project is useful independently of Caddy and exposes several unusually reusable infrastructure patterns: automated certificate lifecycle management, clustered certificate state, distributed locking, multiple certificate issuers, challenge orchestration, storage abstraction, local/remote cache layering, and TLS configuration integration.

The repository is actively maintained, has a formal stable release, and runs its Go test suite under the race detector across Linux, macOS, and Windows. GitHub Gold did not execute the library or tests itself; VERIFIED here reflects inspected implementation, test, CI, release, and maintenance evidence.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Automatic certificate issuance/renewal and TLS integration are broadly useful infrastructure capabilities. |
| Working Evidence | 5/5 | Current CI runs short race-enabled tests across three operating systems and two Go versions; formal releases and extensive test files exist. |
| Reusability | 5/5 | It is a standalone Go library with pluggable storage, issuers, DNS providers, key sources, event hooks, and configurable TLS behavior. |
| Novelty | 4/5 | ACME clients are not unique, but CertMagic's integrated lifecycle, clustered coordination, on-demand issuance, issuer fallback, and storage model are distinctive. |
| Documentation | 5/5 | README documentation covers features, requirements, APIs, examples, challenges, clustering, storage, cache, events, and operational caveats. |
| Maintenance | 5/5 | Commits were landing on 2026-09-10, including storage/cache correctness and performance-related changes. |

**Total: 29 / 30 — provisional S tier.**

## What it does

The upstream README describes CertMagic as the automatic HTTPS/certificate-management library used by Caddy. It can integrate directly with Go HTTP servers and TLS listeners and supports:

- automatic certificate issuance and renewal;
- ACME-compatible certificate authorities;
- HTTP-01, TLS-ALPN-01, and DNS-01 challenge workflows;
- multiple issuers for redundancy/fallback;
- pluggable storage backends;
- pluggable private-key sources;
- wildcard certificates;
- OCSP stapling;
- certificate revocation workflows;
- clustered/distributed certificate management;
- on-demand issuance during TLS handshakes with policy controls;
- event hooks;
- RFC 9773 ACME Renewal Information support;
- integration with `libdns` DNS providers.

The high-level API can wrap an HTTP handler in managed HTTPS, while lower-level APIs expose certificate caches, `tls.Config` integration, custom issuers, and explicit synchronous/asynchronous certificate management.

## Reusable components and architecture

### Certificate lifecycle manager

CertMagic automates the full operational cycle around certificates rather than only making ACME requests. The documented behavior includes acquisition, renewal, retry/backoff, issuer selection, certificate loading, OCSP staple management, and replacement of certificates when appropriate.

This is reusable as both a library and a design reference for unattended PKI lifecycle systems.

### Storage abstraction

`storage.go` defines a `Storage` interface with file-system-like key semantics. Implementations provide:

- `Store`;
- `Load`;
- `Delete`;
- `Exists`;
- `List`;
- `Stat`;
- distributed locking through the embedded `Locker` interface.

The interface explicitly requires concurrent safety and context cancellation. Processes in a cluster are expected to share the same storage configuration so certificates and related TLS state are coordinated across nodes.

The API is intentionally not streaming and upstream warns it is not appropriate for very large files. That is a useful, explicit design boundary rather than an implied unlimited object store.

### Distributed locking

The storage layer defines a named distributed-lock abstraction for expensive coordinated operations such as certificate acquisition.

Upstream explicitly discusses two synchronization models:

- fencing-token-based distributed locks where feasible;
- timeout/staleness-based locking where fencing is not available.

The comments also warn that consumers must tolerate rare synchronization errors and should re-check whether idempotent work is still required after acquiring a lock. This is a strong example of documenting distributed-systems failure assumptions in the interface contract itself.

An optional `LockLeaseRenewer` interface supports renewal of leases for long-running clustered work.

### Certificate/key storage keys

`KeyBuilder` centralizes storage namespaces for certificate artifacts including:

- certificate files;
- private-key files;
- metadata;
- OCSP staples;
- issuer/account-related state.

Centralizing these paths makes storage backends interchangeable without scattering persistence layout logic across the codebase.

### Local cache + authoritative storage split

A current 2026-09-10 upstream change added an optional `LocalCache` storage tier for certificate assets when the authoritative shared `Storage` is remote.

The commit message documents a deliberate trust/consistency split:

- handshake-serving reads may use the local cache;
- issuance, renewal, peer-refresh, and other cluster-coordination operations use authoritative storage;
- writes/deletes go to authoritative storage first and then update the cache;
- distributed locking never becomes local-only;
- unusable/torn local cache writes can fall back to authoritative storage.

This is a particularly valuable reusable design pattern for latency-sensitive distributed state that still needs a single coordination source of truth.

### ACME integration

The current module depends on `github.com/mholt/acmez/v3` and uses CertMagic-specific orchestration around ACME accounts, issuers, challenges, retries, storage, and certificate deployment.

The project supports any compatible ACME CA rather than hard-coding a single provider. Let's Encrypt is the documented default, and the README recommends staging endpoints for development to avoid production rate limits.

### DNS challenge ecosystem

The module depends on `github.com/libdns/libdns`. Upstream documents compatibility with the broader libdns provider ecosystem for DNS challenge automation.

This is operationally useful but creates an important dependency boundary: each DNS provider plugin has its own credentials, permissions, maintenance status, and license and should be assessed independently.

## Runtime and development requirements

The current `go.mod` declares:

- module `github.com/caddyserver/certmagic`;
- Go **1.25.0**;
- direct dependencies including `acmez/v3`, `libdns`, `miekg/dns`, `x/crypto`, `x/net`, Zap, Blake3, and ZeroSSL integration.

The upstream README gives a simpler minimum of Go 1.21 or newer in its prose; the module file is the more precise current source-build dependency and should be treated as authoritative for the current master branch.

Operational requirements depend on the challenge type. For normal public ACME HTTP/TLS challenges the documented assumptions include controlled DNS names, public reachability, relevant ports, and persistent storage; DNS challenge use can remove the public port/reachability requirement but requires DNS-provider credentials.

## CI / working evidence

The current `.github/workflows/ci.yml` runs on pushes and pull requests targeting `master`.

Its matrix is:

- Ubuntu latest;
- macOS latest;
- Windows latest;
- Go 1.25;
- Go 1.26.

For each combination it:

1. checks out the repository;
2. installs Go;
3. prints environment/toolchain details;
4. downloads module dependencies;
5. runs `go test -v -short -race ./...`.

The race detector is meaningful evidence for a library that manages shared in-memory certificate caches and asynchronous/clustered state.

This is upstream CI evidence only. GitHub Gold did not run the workflow independently.

## Releases

The latest stable GitHub release inspected during this run was **v0.25.3**, published **2026-05-11**.

Its changelog includes fixes or improvements for:

- asynchronous certificate management;
- IPv6 handling for HTTP-01 challenges;
- IPv6 normalization for ACME challenge handling;
- additional validation of delegated OCSP responders following a reported potential security risk.

The release has no standalone binary assets because CertMagic is primarily a Go library; source release/tag provenance is therefore more relevant than executable bundles.

## Maintenance signals

The repository was actively changing on the same date as this dossier.

An inspected **2026-09-10** commit added the optional local certificate-asset cache described above and explicitly added recovery from torn local-cache writes by reloading unusable data from authoritative storage.

Another **2026-09-10** change optimized TLS-handshake event processing by skipping construction of event data when no observer would consume it.

Repository metadata also showed a current push timestamp on 2026-09-10 and the repository is not archived.

## Licensing

GitHub repository metadata identifies the project license as **Apache-2.0**, and root source files carry Apache-2.0 headers.

No CertMagic source code, private keys, certificates, account data, DNS credentials, binaries, or release archives were copied into GitHub Gold.

Third-party dependencies and DNS/storage integrations must be reviewed under their own licenses before redistribution or source reuse.

## Security and trust boundaries

### Private keys and ACME account credentials

CertMagic manages sensitive PKI material. Storage backend confidentiality, permissions, backups, credential scope, and host/process security are therefore central to safe deployment.

Pluggable storage is an architectural strength but should not be mistaken for automatic storage security.

### Distributed storage consistency

Clustered operation depends on the semantics of the selected `Storage` and `Locker` implementation. The interface explicitly documents that not all locks use fencing tokens and that rare mis-synchronization must be tolerated.

A storage backend that violates concurrency, cancellation, durability, or locking expectations could undermine certificate lifecycle correctness.

### On-demand TLS

On-demand certificate issuance can trigger CA requests during TLS handshakes. Upstream provides decision/policy hooks and throttling concepts because unconstrained issuance can create abuse, resource, and CA-rate-limit risk.

### DNS provider credentials

DNS-01 integrations typically require credentials capable of modifying DNS records. Provider modules should be granted narrowly scoped permissions where possible and reviewed separately.

### Issuer/network dependency

Automatic issuance and renewal depend on external certificate authorities, DNS APIs, network reachability, time, and correct local storage. Multi-issuer support improves resilience but does not eliminate those external trust/availability dependencies.

### OCSP and revocation behavior

The v0.25.3 release contains an OCSP validation hardening change associated with a reported potential security risk. That is positive maintenance evidence and also a reminder that certificate-status processing is security-sensitive code deserving independent review.

## Verification boundary

GitHub Gold inspected repository-native evidence but **did not**:

- compile a Go program using CertMagic;
- run its unit/race tests;
- obtain or renew a real certificate;
- exercise Let's Encrypt, ZeroSSL, or another ACME CA;
- execute HTTP-01, TLS-ALPN-01, or DNS-01 challenges;
- test wildcard certificates;
- test issuer fallback;
- test on-demand issuance or its policy hooks;
- test OCSP stapling or revocation;
- test a distributed deployment;
- test storage locks, fencing, lease renewal, or stale-lock recovery;
- reproduce torn local-cache writes;
- validate DNS-provider credentials or permissions;
- fuzz ACME, certificate, TLS, storage, or network inputs;
- independently verify release tags or dependency provenance.

Therefore **VERIFIED** means that concrete implementation, CI, release, source-structure, and current-maintenance evidence was inspected. It does not mean GitHub Gold independently validated production PKI behavior.

## Why it matters to GitHub Gold

CertMagic is valuable at several layers:

1. **Reusable library:** adds managed certificate lifecycle to Go services without requiring Caddy itself.
2. **Distributed-systems pattern:** storage + locking + cache separation provides a concrete design for coordinated shared state.
3. **PKI automation:** ACME issuance, renewal, challenge handling, OCSP, revocation, and issuer fallback are integrated in one lifecycle system.
4. **Extensibility:** storage, key sources, issuers, DNS providers, and event hooks are replaceable interfaces.
5. **Operational resilience:** retry/backoff, multi-issuer support, clustered state, and local-cache recovery are explicitly engineered concerns.
6. **Research value:** current code exposes meaningful trust boundaries around private keys, DNS credentials, distributed locks, and certificate-status processing.

## Related projects / recursive leads

- `caddyserver/caddy` — primary downstream server platform using CertMagic;
- `caddyserver/xcaddy` — custom Caddy build/composition tooling;
- `mholt/acmez` — lower-level ACME client layer used by CertMagic;
- `libdns/libdns` and provider repositories — DNS challenge abstraction/ecosystem;
- CertMagic storage implementations — alternate clustered persistence backends.

## Strongest next research questions

1. Inspect `mholt/acmez` independently and map which ACME protocol responsibilities live there versus CertMagic.
2. Trace certificate renewal decision logic, ARI integration, retry/backoff, and issuer fallback in source.
3. Inspect default file-storage locking, stale-lock detection, lease renewal, and failure handling.
4. Review the new `LocalCache` path and tests for torn writes, stale data, and authoritative-store refresh.
5. Trace private-key generation/storage and pluggable key-source boundaries.
6. Inspect OCSP responder validation and staple persistence/recovery.
7. Map DNS-01 provider credential flow through `libdns` and identify high-quality provider implementations.
8. Inspect on-demand TLS decision hooks and safeguards against unintended certificate issuance.