# ZCrypto — research TLS/X.509 measurement library

- **Repository:** https://github.com/zmap/zcrypto
- **Author / organization:** ZMap Project
- **Category:** network measurement / TLS / PKI / cryptography research
- **Evidence:** VERIFIED
- **Provisional Gold score:** 26/30 — S tier
- **Scoring:** Utility 5, Working Evidence 5, Reusability 4, Novelty 5, Documentation 3, Maintenance 4
- **Discovery:** recursive follow-up from the ZGrab2 dossier

## What it is

ZCrypto is a Go research library containing specialized forks/variants of TLS, X.509, and Certificate Transparency components. Upstream explicitly describes it as a data-collection, analysis, experimentation, and prototyping library rather than a production security library.

The TLS package exposes protocol behavior that normal production TLS libraries intentionally hide or reject: old TLS versions, export ciphers, handshake-message logging, and unusually configurable internals. ZGrab2 uses this capability for measurement. The X.509 fork adds certificate-to-JSON functionality and Certificate Transparency interoperability; the CT package is adapted from Google's CT Go library.

## Why it matters

Production crypto APIs optimize for safe defaults. Measurement and interoperability research sometimes needs the opposite: detailed transcripts, legacy behavior, malformed/obsolete ecosystem visibility, certificate serialization, and enough instrumentation to study what endpoints actually deploy. ZCrypto is valuable because it provides that research-oriented boundary while clearly warning that it must not secure production systems.

## Useful components

- `tls/` — research TLS implementation used by ZGrab2; legacy protocol/cipher support, handshake logging, configurable behavior.
- `x509/` — Go X.509 fork with JSON certificate serialization and CT-oriented behavior.
- `ct/` — adapted Certificate Transparency library.
- supporting certificate/root/platform code — useful for understanding cross-platform trust-store behavior and compatibility.

## Working / maintenance evidence

Current GitHub Actions runs on pushes, pull requests, manual dispatches, and every 12 hours. It uses Go >=1.24, builds every package with `go build -v ./...`, then executes `go test -v -failfast ./...`.

Maintenance is current in September 2026. A September 6 change repaired Windows and FreeBSD-family build regressions in the X.509/CT root-certificate code. The commit documents that Windows had lacked a required `loadSystemRoots()` implementation and that BSD-family targets lacked certificate-file/directory definitions; it also notes AIX/Solaris remain outside that fix. A same-day dependency update moved `actions/setup-go` to v7.

## Requirements / platforms

- Go; current CI requests Go >=1.24.
- Primarily a library consumed by other Go software such as ZGrab2.
- Recent upstream fixes explicitly address Windows and FreeBSD/DragonFly/NetBSD/OpenBSD compatibility. Linux is the CI execution platform inspected here.

## License

Mixed permissive licensing is explicitly documented at the repository root:

- University of Michigan original ZCrypto work: Apache-2.0.
- Google-origin Go standard-library / BoringSSL-derived fork code: ISC.
- `util/isURL.go` from Alex Saskevich: MIT.

File-level provenance therefore matters before extracting or adapting components. GitHub Gold copied no upstream source.

## Verification performed for this dossier

Inspected upstream README, root license, workflow inventory, current Go build/test workflow, and recent commit history. Confirmed repository is not archived and that current upstream maintenance includes concrete portability fixes.

## Important caveats

- Upstream explicitly labels ZCrypto **experimental** and says it should **not** provide security for production systems.
- Its intentionally permissive/legacy TLS behavior is useful for measurement but is precisely why it should not replace a hardened standard TLS stack.
- Mixed Apache/ISC/MIT provenance requires file-level notice preservation for extraction.
- Windows/BSD fixes are recent; the inspected commit explicitly says AIX and Solaris analogous failures remain unfixed.
- GitHub Gold did not compile the project, run tests, perform TLS handshakes, validate certificate parsing, reproduce portability failures, or audit the cryptographic implementation.

## Relationship to existing Gold entries

ZCrypto is a foundational dependency boundary behind ZGrab2. ZMap can discover endpoints, ZGrab2 can perform structured application handshakes, and ZCrypto supplies research-oriented TLS/X.509/CT behavior needed to observe legacy and unusual cryptographic deployments.

## Follow-up leads

1. Map exactly which ZGrab2 modules import ZCrypto and which data fields originate at this layer.
2. Inspect TLS handshake transcript structures and JSON serialization boundaries.
3. Inspect certificate/chain parsing differences from contemporary Go `crypto/x509`.
4. Audit CT package divergence from its Google upstream.
5. Review test coverage for malformed certificates, legacy TLS, and parser edge cases.
6. Track the documented AIX/Solaris portability gap.
7. Investigate sibling `zmap/zlint` as a certificate-linting component in the same ecosystem.
