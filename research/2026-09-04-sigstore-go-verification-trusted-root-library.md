# sigstore-go — reusable Sigstore verification, trusted-root, and bundle library

- **Repository:** https://github.com/sigstore/sigstore-go
- **Organization:** Sigstore
- **Category:** software supply chain / signature verification / trusted roots / transparency / Go library
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 29 / 30
- **Provisional tier:** S
- **License:** Apache-2.0
- **Primary language:** Go
- **Latest inspected stable release:** v1.3.0 — 2026-07-30
- **Discovery source:** Recursive follow-up from the Cosign dossier. No playlist-derived claims are used in this dossier.

## Executive finding

`sigstore/sigstore-go` is the reusable Go library layer behind modern Sigstore signing and verification workflows. Upstream describes it as a smaller, integration-friendly API than Cosign, focused on Sigstore's specified bundle/trusted-root data structures, with support for bundle signing/verification, raw signatures, Rekor transparency evidence, RFC3161 timestamp authorities, TUF-fetched trusted roots, structured verification results, and custom trust material.

Upstream explicitly states the library is stable and ready for production use and that it passes the `sigstore-conformance` signing and verification suite. GitHub Gold did not independently reproduce that conformance result, but the repository contains concrete cross-platform CI and extensive verification/root package tests.

The most reusable design lesson is that verification is configurable over multiple independent evidence classes. `pkg/verify/signed_entity.go` models separate thresholds and requirements for signed RFC3161 timestamps, integrated transparency-log timestamps, observer timestamps, log inclusion proofs, and Fulcio SCTs. This keeps "a signature verified" from collapsing distinct trust assumptions into one Boolean.

## Why it qualifies as GitHub Gold

1. Provides a library-first Sigstore integration surface rather than only a CLI.
2. Implements bundle signing and verification against Sigstore's specified protobuf structures.
3. Separates trusted material, verifier policy, transparency evidence, timestamp evidence, certificate identity, and artifact policy.
4. Supports custom trusted roots and TUF-backed public-good trust roots.
5. Exposes dedicated packages for bundles, Fulcio, roots, signing, transparency logs, TUF, utilities, and verification.
6. Includes fuzz tests and large verification test surfaces in addition to ordinary unit tests.
7. Cross-platform CI builds and tests on macOS, Linux, and Windows.
8. CI actions inspected here are pinned to immutable commit SHAs.
9. Stable release history includes security/correctness fixes in verification paths.
10. Active maintenance continued through 2026-09-03.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Directly useful for integrating software-signing verification into Go services, CLIs, policy engines, and package ecosystems. |
| Working evidence | 5/5 | Stable releases, cross-platform CI, conformance claim, extensive unit/fuzz tests, and repeated verification-hardening changes. |
| Reusability | 5/5 | Library-first package structure with explicit interfaces and configurable trust material/policy. |
| Novelty | 4/5 | Signature verification is established, but the composable identity/transparency/timestamp/trusted-root model is unusually useful. |
| Documentation | 5/5 | README, docs, examples, pkg.go.dev references, and verification-focused examples are maintained upstream. |
| Maintenance | 5/5 | Stable v1.3.0 in July 2026 and substantive trusted-root/TUF work on September 3, 2026. |

**Total: 29 / 30 — provisional S tier.**

## Package architecture

The current `pkg/` tree exposes these major reusable surfaces:

- `pkg/bundle` — Sigstore bundle structures and helpers;
- `pkg/fulcio` — Fulcio certificate/signing integration;
- `pkg/root` — trusted material, trusted roots, signing configuration, CA/log/TSA authority representations;
- `pkg/sign` — signing interfaces and implementations;
- `pkg/testing` — reusable test support;
- `pkg/tlog` — transparency-log logic;
- `pkg/tuf` — trusted-root distribution/update support;
- `pkg/util` — shared helpers;
- `pkg/verify` — signature, certificate, SCT, DSSE, identity, artifact-policy, and signed-entity verification.

This package split is strong evidence that the project is designed for embedding into other systems rather than functioning only as an executable.

## Verification configuration as explicit trust policy

`pkg/verify/signed_entity.go` defines `VerifierConfig` with separate controls for:

- RFC3161 signed timestamps;
- integrated transparency-log timestamps;
- combined observer timestamps;
- transparency-log inclusion evidence;
- Signed Certificate Timestamps for Fulcio certificates;
- current-time verification for selected private/long-lived certificate deployments;
- no-observer-timestamp mode for key-based rather than certificate-based verification.

Each threshold-setting helper rejects thresholds below 1. Configuration validation also rejects an unspecified time-verification model and rejects combinations that conflict with `WithNoObserverTimestamps()`.

This is a reusable security pattern: **make the verifier's evidence assumptions explicit at construction time and fail configuration early rather than silently accepting an underspecified trust model.**

## Trusted material and root model

`pkg/root` separates trusted material from the verification engine. The current tree contains explicit models for:

- certificate authorities;
- timestamping authorities;
- trusted material interfaces;
- trusted roots;
- trusted-root creation;
- signing configuration;
- related tests.

This separation allows a verifier to consume public-good Sigstore roots, custom/private deployment roots, or other trusted-material implementations without hard-coding one global trust environment into the verifier.

The README documents TUF support for fetching trusted root certificates and transparency-log keys. A September 3, 2026 commit hardened this path operationally by making the default TUF downloader retry transient failures while preserving non-retry behavior for permanent 404 responses and leaving custom fetchers unchanged.

## Transparency and timestamp evidence

The verifier does not treat time as a single wall-clock check.

Supported verification modes include:

- RFC3161 timestamp evidence verified against configured Timestamp Authorities;
- transparency-log integrated timestamps / Signed Entry Timestamps verified against Rekor log material;
- combined observer timestamp thresholds;
- transparency-log inclusion evidence;
- Fulcio SCT verification against CT-log authorities.

These mechanisms matter because short-lived signing certificates require trustworthy evidence about *when* a signature existed. A certificate that is expired at verification time can still be valid for an earlier signing event if the verifier can prove the signature existed during the certificate's validity window.

## Security-relevant release history

The inspected release history contains several useful correctness/security signals:

- **v1.2.1 — 2026-06-09:** resolves `GHSA-wqqc-jjcq-vfxm` by checking signature time against public-key validity windows.
- **v1.2.2 — 2026-07-06:** rejects certificate identity configuration that supplies neither SAN criteria nor issuer criteria, preventing an effectively unconstrained identity matcher.
- **v1.3.0 — 2026-07-30:** includes a fix preventing a nil-pointer panic in transparency-log entry handling, graceful recovery from Rekor v1 HTTP 409 conflicts, and a lower-allocation DSSE/in-toto verification path for large predicates.

These are not treated as proof of perfect security. They are evidence that edge cases in trust, identity, transparency, and malformed-input paths receive active maintenance.

## Large-attestation verification optimization

A July 30, 2026 change introduced a particularly reusable performance lesson. Upstream found that parsing large in-toto predicates into generic protobuf structures caused heavy allocation overhead for SBOMs, vulnerability reports, and provenance documents.

The new verification path can summarize only the statement fields actually needed for policy checks—statement type, subjects, and predicate type—while leaving the large predicate unmaterialized. An optional `WithoutStatementPredicate()` mode also lets callers omit predicate materialization from the structured verification result when they already consume the verified DSSE payload directly.

Upstream's commit message reports a benchmark on a roughly 1.4 MiB predicate dropping from about 14 MB and 410k allocations per parse to about 1.4 MB and 38 allocations for the summary path. GitHub Gold did not reproduce that benchmark, so those numbers remain upstream evidence only.

## PyPI / PEP 740 integration signal

A 2026-08-25 commit added a walkthrough for verifying PyPI PEP 740 attestations. The documented flow reconstructs a Sigstore bundle from PyPI's attestation representation and verifies it against the public-good trusted root while binding artifact policy to the SHA-256 digest reported for the distribution file.

This is a strong recursive connection to the existing GitHub Gold PyPI provenance research: `sigstore-go` is directly useful for consumers that want to validate package attestations rather than only publish them.

## CI and working evidence

The current `Build and test` workflow:

- runs on macOS, Ubuntu, and Windows;
- checks out full history/tags;
- installs the Go version declared by the module;
- builds with `make all`;
- runs tests with `make test`.

The inspected workflow pins both `actions/checkout` and `actions/setup-go` to immutable commit SHAs rather than mutable version tags.

The verification package also includes dedicated tests for certificates, certificate identity, DSSE, signatures, SCTs, signed entities, and fuzzing.

GitHub Gold did not execute these tests in this pass.

## Release and maintenance evidence

Latest stable release inspected:

- **v1.3.0**
- published **2026-07-30**
- not marked prerelease.

The most recent inspected commit is **2026-09-03**, `retry transient TUF downloads by default (#671)`, which modifies the default trusted-root retrieval behavior to tolerate temporary server failures.

This is substantive maintenance of a security-critical dependency path rather than only documentation churn.

## License and reuse boundary

The repository root contains **Apache License 2.0**.

No upstream source code was copied into GitHub Gold.

Future extraction or adaptation should preserve Apache-2.0 copyright, license, NOTICE/patent obligations where applicable, while separately reviewing licenses of imported dependencies and any copied generated/protobuf material.

## Important caveats / risks

### 1. Library correctness does not define authorization policy for the application

A library can successfully validate certificate chains, timestamps and signatures while the embedding application still authorizes the wrong identity or artifact. Callers must define appropriate certificate identity and artifact policies.

### 2. Trusted-root freshness is operational security

TUF-backed root retrieval reduces manual key distribution problems, but operators must still protect bootstrap trust, caches, mirrors, custom roots, and update policy.

### 3. Thresholds encode security assumptions

Choosing one log/timestamp versus multiple observers is a deployment policy decision. Lower thresholds increase availability but may reduce resilience against a compromised or unavailable authority.

### 4. Current-time verification is not a substitute for observer evidence for short-lived certificates

The source explicitly warns that `WithCurrentTime()` should not be used for ordinary short-lived-certificate verification because observer timestamps are required to prove the relevant signing time.

### 5. Key-based verification has different assumptions from certificate-based verification

`WithNoObserverTimestamps()` is intentionally limited to key-based workflows. Applications should not blur the different lifetime and identity models of bare keys and Fulcio-style short-lived certificates.

### 6. Transparency evidence does not establish signer authorization by itself

A Rekor entry can prove that a signed object existed in the log; it does not independently prove the embedded identity was authorized for the artifact.

### 7. Dependency and network security remain external concerns

TUF, Rekor, Fulcio, TSA, HTTP clients, protobuf parsers, cryptographic libraries, and application-provided custom implementations all contribute to the effective attack surface.

## Verification performed by GitHub Gold

This pass inspected upstream:

- repository metadata;
- README/status/features;
- root Apache-2.0 license;
- current package tree;
- current verification package tree;
- `pkg/verify/signed_entity.go` verifier configuration and thresholds;
- current `pkg/root` structure;
- main build/test workflow;
- stable release metadata through v1.3.0;
- recent commits through 2026-09-03.

## Not independently verified

GitHub Gold did **not**:

- build `sigstore-go`;
- run unit, fuzz, or conformance tests;
- sign or verify a bundle;
- fetch or validate a TUF trusted root;
- query Rekor;
- validate an RFC3161 timestamp;
- validate a Fulcio certificate or SCT;
- reproduce GHSA-wqqc-jjcq-vfxm;
- reproduce the large-predicate benchmark;
- verify a PEP 740 PyPI attestation end to end;
- fuzz bundle/protobuf inputs;
- conduct a cryptographic or security audit.

All claims above distinguish upstream evidence from GitHub Gold's own source inspection.

## Related projects / recursive ecosystem

- `sigstore/cosign` — user-facing CLI/toolchain increasingly able to consume this library layer.
- `sigstore/sigstore-conformance` — signing/verification interoperability suite.
- `sigstore/protobuf-specs` — bundle and trusted-root data structures.
- `sigstore/rekor` — transparency log.
- `sigstore/fulcio` — signing certificate authority.
- `sigstore/root-signing` — public-good trust-root/TUF material.
- PyPI PEP 740 / Integrity API — package-attestation consumer use case.

## Strongest next research leads

1. inspect `sigstore/sigstore-conformance` as a standalone verification/interoperability Gold candidate;
2. trace `pkg/root/trusted_root.go` and TUF bootstrap/update invariants;
3. inspect Rekor v1/v2 inclusion and integrated-time verification paths;
4. inspect RFC3161 timestamp validation and threshold semantics;
5. inspect certificate identity matching, SAN/issuer/regex behavior, and fail-closed defaults;
6. inspect `pkg/bundle` validation against protobuf-spec versions;
7. inspect raw-signature-to-bundle conversion and malformed-material behavior;
8. reproduce or independently benchmark large in-toto predicate verification;
9. implement an offline PEP 740 verification harness against downloaded package provenance;
10. compare Cosign's remaining verification logic with what has migrated into `sigstore-go`.

## Verdict

**VERIFIED — provisional S / 29.**

`sigstore/sigstore-go` is GitHub Gold because it is a focused, reusable, production-oriented security library with explicit trusted-material abstractions, configurable verification evidence, transparency/timestamp support, current conformance claims, cross-platform tests, active security hardening, and direct applicability to OCI, PyPI provenance, policy engines, CI/CD, and custom software-supply-chain tooling.