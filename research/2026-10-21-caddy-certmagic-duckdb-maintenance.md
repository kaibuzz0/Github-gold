# 2026-10-21 — Caddy, CertMagic, DuckDB scoring and maintenance audit

GitHub-first inspection of three **existing** catalog entries. Primary evidence: upstream README, root license, source files, release metadata, recent commits and CI jobs. First YouTube seed playlist retried; throttled, so no transcript findings claimed. No source copied; no independent installation, execution, TLS issuance, benchmarking or security audit.

## Caddy — VERIFIED (upstream), S / 29
- https://github.com/caddyserver/caddy ; root Apache-2.0; score Utility 5 / Working Evidence 5 / Reusability 5 / Novelty 4 / Documentation 5 / Maintenance 5.
- Reusable: [reverseproxy.go](https://github.com/caddyserver/caddy/blob/master/modules/caddyhttp/reverseproxy/reverseproxy.go), HTTP modules, config adapters, TLS/PKI.
- [v2.11.7](https://github.com/caddyserver/caddy/releases/tag/v2.11.7) published 2026-10-03, fixing v2.11.6 HTTP/2 proxy panic and streaming cutoffs.
- [2026-10-21 commit f355b868](https://github.com/caddyserver/caddy/commit/f355b8687d5582ea9fcc99f71598109d1e5b6ced) improves forward-proxy-wrapped dial retries; **not assumed shipped in stable**.
- [Upstream Tests 39594833694](https://github.com/caddyserver/caddy/actions/runs/39594833694): 3 platform jobs passed, 2 optional jobs skipped. Caveat: proxy/admin exposure, plugin licenses.

## CertMagic — VERIFIED (upstream), S / 29
- https://github.com/caddyserver/certmagic ; root Apache-2.0; score 5 / 5 / 5 / 4 / 5 / 5.
- Reusable: [certmagic.go](https://github.com/caddyserver/certmagic/blob/master/certmagic.go) HTTPS/Listen/TLS, Cache/Config, ACME challenges, renewals and storage.
- [v0.25.6](https://github.com/caddyserver/certmagic/releases/tag/v0.25.6) published 2026-09-30, upgrading ZeroSSL dependency for Authorization: ApiKey.
- [2026-10-01 commit cfd20205](https://github.com/caddyserver/certmagic/commit/cfd20205029dd9bd1166cdbd3e9708cba4d4db26) fixes README link.
- [Upstream Tests 36915271739](https://github.com/caddyserver/certmagic/actions/runs/36915271739): 6/6 jobs passed on Ubuntu/macOS/Windows and Go 1.25/1.26. Caveat: CA/challenge/storage conditions, external provider licenses.

## DuckDB — VERIFIED (upstream), S / 28 (reassessed from provisional S / 29)
- https://github.com/duckdb/duckdb ; root MIT; score Utility 5 / Working Evidence 4 / Reusability 5 / Novelty 5 / Documentation 5 / Maintenance 4.
- Reusable: [generated public C API](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb.h), SQL/vectorized execution, CSV/Parquet/JSON and extension architecture. Use versioned public API.
- [v2.0.0](https://github.com/duckdb/duckdb/releases/tag/v2.0.0) published 2026-10-21 with 28 release assets; major-version compatibility requires review.
- [2026-10-21 main commit c15a232a](https://github.com/duckdb/duckdb/commit/c15a232a57040c59d5004ea4a7e54520260b2db2) fixes a window-aggregate memory-limit livelock; **not assumed included in tag**.
- [On Tag 39602672912](https://github.com/duckdb/duckdb/actions/runs/39602672912) failed staging download; [SwiftRelease 39602672833](https://github.com/duckdb/duckdb/actions/runs/39602672833) failed push. [Oct 19 Main 39259831957](https://github.com/duckdb/duckdb/actions/runs/39259831957) passed many core/platform jobs but failed parser benchmark and cloud-extension builds. These failures do not prove core engine malfunction.
- Caveat: v2 client/extension compatibility, licensing and release pipeline follow-up.

## Next research
Caddy proxy streaming regression tests and release of retry fix; CertMagic distributed storage locks/issuer switch tests; DuckDB v2 release pipeline and public C API/extension compatibility. No duplicate catalog entries created.
