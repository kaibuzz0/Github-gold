# Research Dossier — Caddy and CertMagic

Date: 2026-08-20

This pass examined the Caddy ecosystem as a self-hosting, networking, and reusable TLS-automation branch. Findings are promotion-ready but remain in the candidate queue until the canonical human and machine-readable catalogs can be updated together.

## Caddy

- **Repository:** https://github.com/caddyserver/caddy
- **Owner:** caddyserver
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 29
- **Category:** web server / reverse proxy / automatic HTTPS / self-hosting / extensible server platform
- **License:** Apache-2.0
- **Verification performed:** official README inspected; root Apache-2.0 LICENSE inspected; recent commit history inspected; upstream build/test instructions and CI signals inspected. GitHub Gold did not deploy or benchmark Caddy.

### Why it is valuable

Caddy is more than a web server. Upstream describes it as an extensible Go server platform with native JSON configuration, a dynamic configuration API, config adapters, automatic HTTPS, a managed local CA, HTTP/1.1/2/3 support, clustering-aware certificate coordination, and a module/plugin architecture.

### Useful components and patterns

- automatic HTTPS and certificate lifecycle integration
- native JSON config model
- live/dynamic config API
- Caddyfile and other config adapters
- reverse proxy and active health checking
- HTTP/1.1, HTTP/2, and HTTP/3 server stack
- modular Go application/plugin architecture
- graceful online configuration changes
- internal/local CA support
- TLS issuer fallback and cluster coordination
- `xcaddy` custom-build workflow

### Maintenance signals

Recent upstream work includes an HTTPoxy mitigation in the FastCGI integration on 2026-08-19, an encoded-slash authorization-bypass fix on 2026-08-15, resource cleanup fixes on 2026-08-16, and reverse-proxy active health-check correctness work on 2026-08-12. These are strong maintenance signals but also reminders that exposed web infrastructure requires prompt security updates.

### Caveats

- Use current patched releases for internet-facing deployments.
- The Caddy name is trademarked; Apache-2.0 code permissions do not grant trademark rights.
- Plugins and optional modules can carry their own licenses and must be reviewed independently.
- Upstream scale/performance claims were not independently benchmarked by GitHub Gold.

## CertMagic

- **Repository:** https://github.com/caddyserver/certmagic
- **Owner:** caddyserver
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 29
- **Category:** Go library / TLS automation / ACME / certificate lifecycle / reusable infrastructure
- **License:** Apache-2.0
- **Verification performed:** official README inspected; Apache-2.0 LICENSE.txt inspected; feature/API documentation inspected; recent maintenance commits inspected. GitHub Gold did not perform live ACME issuance.

### Why it is valuable

CertMagic packages Caddy's automatic TLS machinery as a reusable Go library. It can obtain and renew certificates, solve ACME challenges, maintain certificate caches and storage, coordinate across clustered instances, support multiple issuers, and expose higher- and lower-level APIs for embedding managed TLS into other Go programs.

### Useful components and patterns

- automatic certificate issuance and renewal
- ACME HTTP, TLS-ALPN, and DNS challenge handling
- multiple issuer support and fallback
- pluggable storage backends
- distributed challenge coordination and locking
- certificate cache and OCSP stapling
- wildcard certificate workflows
- on-demand certificate issuance controls
- retry/backoff and rate-limit behavior
- event hooks
- high-level HTTPS/listener helpers
- lower-level `Config`, cache, issuer, and `tls.Config` integration
- libdns provider interoperability

### Maintenance signals

On 2026-08-05 upstream fixed retry exhaustion returning nil instead of the final error, which could cause failed renewals to appear successful and allow expired certificates to remain served. Tests were added for the retry exit paths. Earlier 2026 work addressed challenge-log behavior and a high-load certificate-waiter recursion/memory-growth problem. These are concrete signs of active maintenance and security-sensitive engineering.

### Caveats

- Production ACME use depends on DNS, reachability, CA behavior, rate limits, and persistent storage.
- DNS challenge integrations depend on external provider libraries with separate licenses and operational security concerns.
- Certificate automation reduces operational toil but does not eliminate TLS/server configuration responsibility.

## Promotion decision

Both repositories meet the quality bar for promotion. Caddy should be cataloged as the larger extensible server platform, while CertMagic deserves its own entry because its certificate-management and ACME machinery is independently reusable and technically valuable.

No third-party code was copied in this research pass.