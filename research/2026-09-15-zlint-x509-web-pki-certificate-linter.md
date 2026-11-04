# ZLint — X.509 / Web PKI Certificate Linter

- **Repository:** https://github.com/zmap/zlint
- **Author / Org:** ZMap / University of Michigan
- **Category:** PKI / X.509 / certificate linting / Web PKI / developer tooling
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28 / 30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **License:** Apache-2.0
- **Primary language:** Go
- **Discovery source:** Recursive GitHub-first follow-up from `zmap/zcrypto`.

## What it does

ZLint is an X.509 certificate linter implemented in Go. It checks certificates and certificate-related structures against standards and policy requirements, including RFC 5280, CA/Browser Forum Baseline Requirements and EV guidance, ETSI ESI requirements, Mozilla PKI policy, Apple Certificate Transparency policy, and additional RFCs.

It is usable both as a standalone `zlint` command-line utility and as an embeddable Go library. Consumers can run all applicable lints, select or exclude named lints and sources, use predefined profiles, and provide TOML configuration for configurable lints. The repository also documents Certificate Revocation List linting, and recent releases have expanded certificate ecosystem coverage.

## Why it matters

Certificate correctness is not merely syntactic. Publicly trusted PKI has overlapping requirements from X.509 standards, browser/root-store policy, CA/B Forum documents, CT rules, and specialized profiles. ZLint turns many of those requirements into executable checks that can be used before certificate issuance or during large-scale certificate research.

This is especially valuable to GitHub Gold because it forms a coherent toolchain with `zmap/zcrypto`: ZLint parses certificate structures through ZCrypto rather than Go's stock `crypto/x509`, then applies a registry of policy-aware lints. It is therefore both a practical PKI tool and a useful architecture reference for standards-to-code validation systems.

## Valuable components

- `v3/cmd/zlint/` — command-line frontend.
- `v3/lint/` — lint registry, filtering, configuration, result/status machinery, applicability/effective-date handling.
- `v3/lints/` — standards- and policy-specific lint implementations.
- configurable lint profiles and source/name filtering.
- CRL lint support.
- ZCrypto-backed X.509 parsing.
- TOML lint configuration.
- integration corpus machinery under `v3/integration/`.
- custom code-lint checks for lint implementation consistency.
- release automation producing platform binaries/checksums.

## Working evidence inspected

Upstream README exposes dedicated CI, integration-test, and golangci-lint workflows and documents both CLI and library APIs.

The integration workflow runs on pushes, pull requests, and a 12-hour schedule. It caches an integration corpus and executes `make integration PARALLELISM=3`, followed by the project's custom code-lint checks.

The repository also contains workflows for normal Go tests, golangci-lint, release generation, testdata linting, and TLD-data updating.

The current release surface inspected on 2026-09-15 includes **v3.7.2-rc1**, published **2026-09-06**, with packaged artifacts/checksums for Linux, macOS, FreeBSD, and Windows. Its release notes include new PSD2/ETSI, CA/B Forum, code-signing, S/MIME, key-usage, and certificate-field lints.

Recent repository commits on **2026-09-06** include:

- upgrading ZCrypto and restoring Windows/FreeBSD release targets after upstream root-store portability fixes;
- adding a KeyUsage-presence lint for TLS subscriber certificates;
- multiple PSD2 QCStatement structure/role/organizationIdentifier validation additions with fixtures and explicit test assertions.

This is concrete upstream evidence of active standards maintenance, tests, release engineering, and dependency coordination. GitHub Gold did not independently execute these workflows.

## Reuse model

ZLint is attractive both as a complete tool and as an architecture study:

1. **CLI certificate QA** — lint PEM certificates or CRLs during development/review.
2. **Embedded CA validation** — invoke the Go library before issuance.
3. **Research pipelines** — lint large certificate datasets parsed through ZCrypto.
4. **Policy-as-code reference** — study how normative requirements, effective dates, applicability, severity, citations, and configuration are represented as executable rules.
5. **Regression design** — inspect how individual lints pair implementation logic with test fixtures and integration corpus checks.

## Dependencies / requirements

- Go toolchain.
- ZCrypto for X.509 parsing.
- Additional development/test dependencies are managed by the Go module and integration tooling.

The README still states a historical minimum of Go 1.16.x, but current dependency/release behavior should be checked against `go.mod` before relying on that minimum for a new deployment.

## Platforms

Current release automation evidence includes:

- Linux x86_64
- macOS x86_64
- FreeBSD x86_64
- Windows x86_64

The underlying Go library may support additional environments, but this dossier does not claim them without explicit verification.

## Maintenance signals

- active September 2026 commits;
- current release-candidate pipeline;
- scheduled integration tests every 12 hours;
- multiple CI/static-analysis workflows;
- active additions tracking changing PKI requirements;
- coordinated ZCrypto dependency updates;
- documented downstream integrations across certificate authorities and PKI software.

## License / provenance

Root license is Apache License 2.0. No upstream source, test certificates, binaries, or release artifacts were copied into GitHub Gold during this research pass.

Any future extraction should still inspect file-level notices and dependency licenses, especially where ZCrypto or generated/test corpus material is involved.

## Caveats and limitations

- ZLint checks encoded standards/policy rules; passing ZLint is not proof that a certificate, CA, issuance system, or PKI is secure or policy-compliant in every respect.
- Coverage is not represented upstream as universally complete for every standards source.
- Lint semantics can change as CA/B Forum, browser/root programs, ETSI documents, RFC interpretations, and effective dates evolve.
- ZLint intentionally depends on ZCrypto's certificate model, so parser behavior and portability can inherit upstream dependency issues.
- Release candidate `v3.7.2-rc1` is a prerelease, not evidence that all of its new behavior has reached a final stable release.
- Existing open issues can identify correctness gaps in individual lints; consumers making issuance decisions should pin versions, review changes, and maintain their own validation policy.

## Verification performed by GitHub Gold

Inspected:

- upstream README and documented CLI/library interfaces;
- root Apache-2.0 license;
- workflow inventory;
- integration-test workflow;
- current release metadata;
- recent commit history;
- relationship with ZCrypto;
- existing GitHub Gold catalog for duplicate detection.

Not performed:

- no local build;
- no `go test` execution;
- no integration-corpus execution;
- no certificate or CRL lint run;
- no independent audit of every lint against its cited normative source;
- no binary/checksum verification;
- no exhaustive audit of all test-certificate provenance.

Therefore **VERIFIED** means there is strong repository-native evidence that the project is functioning and actively tested; it does **not** mean GitHub Gold independently validated every lint or built the software.

## Related projects

- https://github.com/zmap/zcrypto — certificate/TLS parsing foundation used by ZLint.
- https://github.com/zmap/zlint-test-corpus — external certificate corpus used for ZLint CI/integration research.
- https://github.com/zmap/zcertificate — certificate parser/CLI integrating ZLint.
- https://github.com/zmap/zgrab2 — ZMap ecosystem application-layer measurement framework.
- https://github.com/letsencrypt/boulder — documented downstream ZLint integration.

## Follow-up research

1. Inspect `zmap/zlint-test-corpus`, including provenance and licensing of its certificate dataset.
2. Map the lint registry architecture: source → applicability → effective date → execution → severity/result.
3. Quantify current lint coverage by policy family instead of assuming README completeness.
4. Inspect how ZLint handles panics, malformed ASN.1, and parser failures after recent hardening.
5. Map ZLint's dependency boundary with ZCrypto and identify which certificate semantics come from parser vs lint logic.
6. Review final v3.7.2 when released and compare it with the current RC.
7. Compare ZLint with alternative certificate-linting pipelines and CA pre-issuance validation approaches.

## Steward verdict

**Keep — VERIFIED, S / 28.** ZLint is a high-value, actively maintained PKI validation tool with a reusable library interface, strong standards-to-code architecture, scheduled integration testing, active release engineering, and direct synergy with the already-cataloged ZCrypto research stack.