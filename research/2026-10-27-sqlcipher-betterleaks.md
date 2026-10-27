# 2026-10-27 — SQLCipher and Betterleaks: encryption and defensive secret scanning

**Provenance:** GitHub-first discovery, including a Gitleaks/Betterleaks ecosystem lead. Two remaining YouTube playlist IDs were searched with no indexed transcript results; no video viewed. No third-party code copied. No independent builds, credential scans, encryption tests or security audits.

## SQLCipher — PROMISING / A25 (5/3/5/3/5/4)

- [Repository](https://github.com/sqlcipher/sqlcipher); [v4.20.0](https://github.com/sqlcipher/sqlcipher/releases/tag/v4.20.0) published 2026-10-27 14:15 UTC; SQLite baseline 3.54.1. [CHANGELOG](https://github.com/sqlcipher/sqlcipher/blob/master/CHANGELOG.md) documents migration-error and WebAssembly fixes, plus previous escaping and error-handling improvements.
- Inspected [README](https://github.com/sqlcipher/sqlcipher/blob/master/README.md), [Zetetic license](https://github.com/sqlcipher/sqlcipher/blob/master/LICENSE.md), [SQLite license distinctions](https://github.com/sqlcipher/sqlcipher/blob/master/SQLITE_LICENSE.md), [src/sqlcipher.c](https://github.com/sqlcipher/sqlcipher/blob/master/src/sqlcipher.c), [OpenSSL provider](https://github.com/sqlcipher/sqlcipher/blob/master/src/crypto_openssl.c), and [test/sqlcipher.test](https://github.com/sqlcipher/sqlcipher/blob/master/test/sqlcipher.test).
- Reusable: encrypted SQLite pager, KDF, key/rekey/migration, provider abstraction (OpenSSL, CommonCrypto, LibTomCrypt), SQLCipher-specific Tcl regression suite including core, compatibility, integrity, rekey, backup and memory tests.
- Build needs SQLite codec macros, temp-store configuration and crypto provider; README documents `make testfixture` and `./testfixture test/sqlcipher.test` after `SQLCIPHER_TEST` configuration. No current passing GitHub Actions runs were returned, so presence of tests is not evidence of their successful execution. Upstream says its own suite is not exhaustive.
- License: Zetetic BSD-style notice with attribution and non-endorsement; SQLite core public domain; build and crypto components vary. No code copied.
- Risks: SQLCipher 4 format migration from older majors, key storage, plaintext export, backup restoration, platform builds, provider interoperability. Next: observe an actual SQLCipher-specific test run and validate migration/rekey.

## Betterleaks — VERIFIED upstream / S28 (5/5/5/4/5/4)

- [Repository](https://github.com/betterleaks/betterleaks); [stable v1.9.0](https://github.com/betterleaks/betterleaks/releases/tag/v1.9.0) 2026-09-29, [v2.0.0-rc.4](https://github.com/betterleaks/betterleaks/releases/tag/v2.0.0-rc.4) 2026-10-20. Main tracks v2 development; `go.mod` specifies Go 1.26.
- Inspected [README](https://github.com/betterleaks/betterleaks/blob/main/README.md), [MIT license](https://github.com/betterleaks/betterleaks/blob/main/LICENSE), [security policy](https://github.com/betterleaks/betterleaks/blob/main/.github/SECURITY.md), [scan/scanner.go](https://github.com/betterleaks/betterleaks/blob/main/scan/scanner.go), [analyze/analyzer.go](https://github.com/betterleaks/betterleaks/blob/main/analyze/analyzer.go), [go.mod](https://github.com/betterleaks/betterleaks/blob/main/go.mod), and [test workflow](https://github.com/betterleaks/betterleaks/blob/main/.github/workflows/test.yml).
- Reusable: concurrent scanner, Aho-Corasick keyword prefilter, Expr rules, provider validation and analysis, Git/filesystem/hosted-code/container source adapters, fingerprints, SDK examples.
- **Upstream executed CI:** [main Test run 40351219706](https://github.com/betterleaks/betterleaks/actions/runs/40351219706) passed **2/2** Ubuntu and Windows jobs on 2026-10-26. Both executed `go build ./...`, RE2/stdlib config checks and `go test -race ./...`. [Feature branch run 40571307863](https://github.com/betterleaks/betterleaks/actions/runs/40571307863) also passed 2026-10-27 but does not establish main-branch status.
- License: MIT at root; dependencies separately licensed. No code copied.
- Security: optional credential validation/analysis sends provider requests when enabled; untrusted rules may create network risks. Revocation is a separate explicit command. Scanning is not proof of secret absence. Protect reports and use only on authorized sources.
- Related: Gitleaks historical maintainer ecosystem, Expr and go-git dependencies; SOPS complements scanning with encryption, not a tested integration.
- Next: v2 stable release CI, synthetic false-positive fixtures, credential-validation boundaries, container limits, HMAC fingerprint privacy and SDK behavior.

## Catalog hygiene

Added two unique entries, updated the existing SOPS cross-reference, preserved scores/evidence, and synchronized JSON and master-list records. No source copied. 
