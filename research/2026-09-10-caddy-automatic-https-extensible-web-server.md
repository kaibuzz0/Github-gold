# Caddy — automatic HTTPS and extensible web-server platform

- **Repository:** https://github.com/caddyserver/caddy
- **Author / Org:** Caddy / caddyserver
- **Category:** networking / self-hosting / web server / reverse proxy / TLS automation / extensible server platform
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30**
- **Provisional tier:** **S**
- **Discovery:** GitHub-first category rotation; no YouTube-derived technical claim used.
- **License:** Apache-2.0 at repository root.

## Executive assessment

Caddy is a high-value general-purpose server platform written in Go. Its default distribution is an HTTP server and reverse proxy with automatic HTTPS, HTTP/1.1, HTTP/2 and HTTP/3 support, but the more reusable architectural idea is its module system: applications, handlers, TLS components, storage backends, config adapters and other functionality are composed as Go modules and driven by a native JSON configuration model.

This is strong GitHub Gold because the repository combines unusually high practical utility with clear architecture, extensive documentation, a large test surface, current maintenance, reproducible source builds, automated release infrastructure, cross-platform binaries, and a separate `xcaddy` ecosystem for building custom distributions.

The project is catalog-worthy both as a whole product and as a source of reusable architectural patterns: automatic certificate lifecycle management, graceful dynamic configuration, modular server composition, reverse-proxy health checking, event dispatch, listener lifecycle handling, and cross-platform release automation.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Production-grade HTTPS serving, reverse proxying, TLS automation, dynamic configuration and extensible server composition are broadly useful. |
| Working Evidence | 5/5 | Repository CI builds and smoke-tests Caddy on Linux/macOS/Windows, then runs short race-enabled tests; release and cross-build automation are present. |
| Reusability | 5/5 | Go module architecture, JSON config, adapters, handlers, apps and the companion `xcaddy` builder make the system highly composable. |
| Novelty | 4/5 | Web serving/reverse proxying is mature territory, but automatic HTTPS-by-default plus the uniform module/config architecture remains distinctive. |
| Documentation | 5/5 | README, architecture/config/API documentation, build instructions, quick starts and module documentation are extensive. |
| Maintenance | 5/5 | Active commits were observed through 2026-09-09 and the repository has a current formal release and maintained CI/release machinery. |

**Total: 29 / 30 — provisional S tier.**

## What it does

Upstream describes Caddy as an extensible server platform that uses TLS by default. The standard distribution includes the `http` and `tls` apps and supports:

- automatic HTTPS;
- public certificate issuance through supported ACME issuers;
- a managed local CA for internal names/IPs;
- multi-issuer fallback;
- HTTP/1.1, HTTP/2 and HTTP/3;
- reverse proxying and active health checks;
- Caddyfile configuration;
- native JSON configuration;
- config adapters;
- a dynamic configuration API;
- a modular Go application/plugin model.

The README explicitly positions Caddy as more than an HTTP binary: Caddy applications are Go programs implemented as modules and gain shared configuration/documentation/runtime facilities.

## Architecture and reusable components

### Native JSON configuration and dynamic API

Caddy's native configuration is JSON. The configuration API allows live configuration changes without treating a static config file as the sole control plane. Config adapters can translate formats such as Caddyfile and other formats into the native JSON representation.

Reusable ideas:

- declarative configuration mapped closely to initialized runtime types;
- dynamic config updates;
- adapter boundary between human-oriented syntax and canonical machine configuration;
- centralized configuration instead of large collections of unrelated flags/environment variables.

### Modular server platform

Caddy functionality is organized around modules. This makes the repository useful as a reference for plugin-oriented long-running Go services, not only for web serving.

High-value component areas include:

- HTTP server and middleware modules;
- reverse proxy logic;
- TLS application integration;
- certificate and storage integrations;
- event handling;
- listener/network lifecycle code;
- config adapters;
- command-line tooling;
- module registration/provisioning.

### Automatic HTTPS / certificate lifecycle

The README identifies `caddyserver/certmagic` as the underlying certificate automation component. Caddy layers server-level policy and configuration around automated certificate acquisition, renewal and deployment.

This is valuable for studying:

- ACME-driven certificate lifecycle automation;
- certificate issuer fallback;
- local/internal PKI workflows;
- TLS configuration orchestration;
- clustering/storage coordination around certificate state.

`certmagic` should be treated as a related upstream project and researched independently before any component-level promotion.

### Reverse proxy and health checking

Recent upstream work shows continued maintenance of active health-check behavior and placeholder expansion. A 2026-09-09 commit changed health-check body replacement so user-supplied JSON containing braces is not accidentally destroyed while still allowing known placeholders to expand.

This is useful evidence that reverse-proxy edge cases receive targeted correctness work rather than the feature merely existing in documentation.

### Event subsystem

A separate 2026-09-09 commit optimized event emission by returning early when nothing is subscribed, avoiding unnecessary logger/replacer setup on frequently emitted paths such as TLS certificate lookups. The commit notes benchmarks were included in the associated pull request.

### Listener lifecycle

A 2026-09-07 change fixed a Windows reload/listener edge case involving shared sockets. This is a useful maintenance signal for cross-platform long-running-service behavior.

## Build and runtime requirements

The inspected README currently requires **Go 1.25.0 or newer** for source builds.

Basic development flow:

- clone the repository;
- build `cmd/caddy` with Go;
- run the Go test suite;
- optionally use `xcaddy` to produce version-aware/custom-plugin builds.

The project states that the normal Go-built executable has no external runtime dependency such as libc when built in the documented static configuration.

## Platforms

Repository-native CI directly tests the primary build on:

- Linux;
- macOS;
- Windows.

The inspected CI also contains a separate s390x test path and the repository contains dedicated cross-build/release workflows. Release artifacts cover a much broader OS/architecture matrix; those release targets should be treated as release evidence rather than equivalent to full CI test coverage on every target.

## CI / working evidence

The current `.github/workflows/ci.yml` provides unusually concrete evidence:

1. installs the configured Go toolchain;
2. downloads test dependencies;
3. builds `cmd/caddy` with `CGO_ENABLED=0`;
4. performs a **smoke test** using `caddy start` then `caddy stop`;
5. uploads the built binary as a CI artifact;
6. runs `go test -coverprofile=cover-profile.out -short -race ./...`;
7. checks GoReleaser configuration and performs a snapshot build for eligible same-repository PRs.

The OS matrix is Linux, macOS and Windows. The workflow pins external GitHub Actions by full commit hashes and runs StepSecurity hardening in audit mode.

This is upstream automation evidence. GitHub Gold did **not** execute this workflow independently.

## Releases and provenance signals

The newest stable release inspected during this run is **v2.11.4**, published **2026-06-03**.

The release exposes, among other assets:

- platform binaries/archives;
- `caddy_2.11.4_checksums.txt`;
- signature material for the checksum/buildable-artifact flow;
- GitHub-provided SHA-256 digest metadata on inspected assets.

An inspected buildable source artifact and the checksum file both have GitHub-side SHA-256 digest metadata, and signature/certificate companion assets are present.

GitHub Gold did not independently download, hash, or cryptographically verify these release assets.

## Maintenance signals

The repository was actively changing immediately before this dossier was written.

Recent inspected commits include:

- **2026-09-09:** reverse-proxy health-check placeholder/body correctness fix;
- **2026-09-09:** event-dispatch hot-path optimization;
- **2026-09-08:** HTTP Alt-Svc logging behavior adjustment;
- **2026-09-07:** Windows shared-listener reload fix;
- **2026-09-06:** Caddyfile directive-order isolation fix.

This is strong evidence of current maintenance across correctness, performance, HTTP behavior, Windows lifecycle handling and configuration adaptation.

## Licensing

The repository root contains the standard **Apache License 2.0** text.

No Caddy source code, binaries, certificate material, release archives, or plugin code were copied into GitHub Gold during this run.

The Caddy name is a registered trademark according to the upstream README. The software license does not grant unrestricted trademark rights, so downstream redistribution or modified distributions should keep trademark considerations separate from source-license permissions.

Third-party Caddy modules/plugins can carry their own licenses and must be reviewed individually before source reuse or redistribution.

## Security and trust boundaries

Caddy is often deployed directly on network boundaries, so several areas deserve explicit treatment.

### Dynamic configuration API

The admin/config API can change live server behavior. Exposure, authentication/authorization decisions, bind address and surrounding network controls therefore matter. A powerful runtime configuration surface should not be assumed safe merely because it is convenient.

### Custom plugins

`xcaddy` builds plugins into the Caddy executable by importing Go modules at build time. A custom plugin therefore executes with the process privileges and trust of the resulting server binary; this is not a constrained sandbox plugin model.

Before adopting a plugin, inspect:

- repository ownership/provenance;
- exact version/commit;
- transitive Go dependencies;
- license;
- maintenance status;
- build scripts/generation;
- network/file/process capabilities exercised by the module.

### TLS and PKI state

Automatic certificate management involves private keys, account credentials, certificate storage, issuer APIs and potentially shared storage. Storage backends and deployment permissions need separate review.

### Privileged ports

The README documents binding to low ports and gives Linux `setcap cap_net_bind_service=+ep` as one option. Capability assignment changes the privilege model and should be applied narrowly to the intended binary.

## Verification boundary

GitHub Gold inspected repository-native evidence but **did not**:

- compile Caddy;
- execute the Caddy binary;
- run unit/integration/race tests;
- start a real HTTP/HTTPS server;
- obtain or renew a certificate;
- exercise ACME issuer fallback;
- test HTTP/3;
- test reverse-proxy health checks;
- test dynamic configuration reloads;
- test Windows listener reload behavior;
- load third-party plugins;
- audit `certmagic` independently;
- fuzz configuration, HTTP, TLS or proxy inputs;
- independently download/hash/verify release artifacts or signatures.

Therefore **VERIFIED** here means that concrete upstream implementation, CI, release, test and maintenance evidence was inspected. It does not mean GitHub Gold independently validated production behavior.

## Why it matters to GitHub Gold

Caddy is valuable at several layers:

1. **Whole tool:** immediately useful self-hosted HTTPS/reverse-proxy platform.
2. **Architecture:** strong example of a modular long-running Go service.
3. **Automation:** automatic certificate lifecycle and live configuration patterns.
4. **Networking:** HTTP/1.1, HTTP/2, HTTP/3, proxy and listener infrastructure.
5. **Build tooling:** `xcaddy` demonstrates reproducible custom composition through Go modules.
6. **Supply chain:** current release workflows expose checksum/signature/provenance material worth deeper inspection.

## Related projects / recursive leads

Highest-value ecosystem follow-ups:

- `caddyserver/certmagic` — automatic TLS/certificate lifecycle core;
- `caddyserver/xcaddy` — custom Caddy builder/plugin composition;
- Caddy module ecosystem — storage, DNS, auth and application modules;
- Caddy website/docs repository — machine-generated module/config documentation pipeline.

## Strongest next research questions

1. Trace the admin API authorization/bind defaults and config transaction/rollback model.
2. Inspect `certmagic` certificate/key storage, locking, renewal and issuer-fallback behavior.
3. Inspect `xcaddy` version pinning and dependency provenance for custom builds.
4. Map reverse-proxy retry, health-check, load-balancing and streaming internals.
5. Inspect graceful reload/listener sharing across Linux/macOS/Windows.
6. Inspect HTTP/3/QUIC dependency boundaries and test coverage.
7. Inspect release signing and buildable-artifact provenance end-to-end.
8. Determine whether selected Caddy modules deserve independent component dossiers.
