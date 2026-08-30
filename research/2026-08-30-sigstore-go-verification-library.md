# sigstore-go — reusable Sigstore verification library

- Upstream repository: https://github.com/sigstore/sigstore-go
- Research date: 2026-08-30
- Category: software supply chain / signing / verification libraries
- Evidence level: VERIFIED
- Provisional Gold score: S / 29
- License: Apache-2.0
- Primary language: Go

## Executive finding

`sigstore/sigstore-go` is a high-value library candidate for GitHub Gold because it isolates modern Sigstore signing and verification primitives behind a substantially smaller integration surface than the Cosign CLI. Upstream explicitly describes it as a minimal Go client focused on Sigstore bundle structures and states that it is stable, production-ready, and passing the Sigstore conformance suite.

The project is especially valuable as reusable infrastructure rather than merely another command-line application: its public packages separate bundle parsing, trusted-root material, TUF bootstrap/update, certificate and identity verification, Rekor transparency-log verification, TSA timestamps, signing, and verification policy.

GitHub Gold did not independently compile or execute this repository during this pass. VERIFIED means source-level inspection plus explicit upstream CI/conformance/release evidence, not local runtime validation.

## Why it matters

Cosign is a feature-rich user-facing tool with OCI, registry, KMS, PKCS#11 and policy integrations. `sigstore-go` exposes the lower-level library pieces that an application can embed directly without inheriting the full Cosign command surface.

This makes it useful for:

- custom software-update verifiers;
- CI/CD artifact admission systems;
- package-manager verification;
- attestation consumers;
- offline or private-root verification workflows;
- provenance inspection tools;
- security gateways that need structured verification results rather than shelling out to `cosign`;
- projects that need Sigstore primitives but not container-specific behavior.

Upstream README states that `sigstore-go` intentionally omits built-in KMS and container-image verification to keep the dependency/API surface smaller, while allowing custom key implementations through the `Keypair` interface.

## Core reusable components

### `pkg/bundle`

Parses and represents Sigstore bundles, including message signatures or DSSE attestations plus verification material such as certificates, transparency-log entries and timestamps.

The tree includes extensive bundle tests and a fuzz target, which is valuable because bundle parsing sits directly on an attacker-controlled artifact boundary in many verifier deployments.

### `pkg/verify`

The main verification engine. Its public abstraction separates:

- `SignedEntity`: the object carrying signatures, timestamps, transparency-log evidence and verification material;
- `VerificationContent`: certificate/public-key material;
- `SignatureContent`: raw signature or DSSE/message-signature representation;
- policy checks for artifact binding and signer identity;
- certificate, SCT, transparency-log and timestamp verification;
- structured verification results.

A particularly strong design choice is that the documented normal verification flow requires both an expected artifact and an expected signer identity. Upstream names the bypasses `WithoutArtifactUnsafe` and `WithoutIdentitiesUnsafe`, making it explicit that cryptographic validity alone is insufficient.

### `pkg/root`

Defines `TrustedMaterial`, which supplies the verifier with:

- timestamping authorities;
- Fulcio certificate authorities;
- Rekor transparency-log keys;
- CT log keys;
- explicit public-key verifiers.

`TrustedMaterialCollection` allows multiple independent trust sources to be composed. Public keys can be represented as time-constrained verifiers, so key validity windows can be enforced against the evidence time rather than treating a key as eternally valid.

This is one of the strongest reusable architectural pieces in the repository: trust material is an interface boundary rather than hard-coded global state.

### `pkg/tuf`

Provides TUF-backed trusted-root retrieval/update support. This is the mechanism used by documented examples to bootstrap the Sigstore public-good trust root while preserving TUF's signed metadata/update model.

This separation matters operationally because bundle verification and trust-root maintenance are different problems. A verifier can validate a bundle correctly yet still be unsafe if its trust material is stale, incorrectly bootstrapped or replaced.

### `pkg/tlog`

Handles Rekor transparency-log entry structures and verification. The project includes tests and fuzzing around this parsing/verification boundary.

### `pkg/sign`

Contains signing primitives, certificate acquisition, timestamping and transparency-log submission. The README explicitly notes that KMS is not built in, but custom key support can be added by implementing the `Keypair` abstraction.

### certificate metadata helpers

`pkg/fulcio/certificate` parses and summarizes Fulcio certificate extensions. Verification results can expose certificate identity and CI/workflow metadata, making the library useful for policy systems that need to reason about build provenance rather than only a binary pass/fail.

## Verification model

The documented verification sequence is:

1. establish trusted material, normally from the Sigstore TUF repository or a custom trusted root;
2. construct a reusable `Verifier` with global verification requirements such as SCT, transparency-log and timestamp thresholds;
3. construct a per-artifact `Policy` containing the expected digest/key and signer identity;
4. verify a `SignedEntity`/bundle;
5. consume a structured `VerificationResult`.

This split is useful for high-volume services: one verifier can hold the common trust configuration while each artifact receives a separate identity and digest policy.

## Identity binding

The documentation explicitly warns that simply verifying a bundle is not enough. Normal certificate verification should constrain the expected issuer and subject identity/SAN, while key-based verification should use an explicitly trusted key.

This is a critical catalog caveat: a consumer that uses an overly broad regular expression or the unsafe identity bypass can turn a cryptographically valid Sigstore bundle into an authorization failure at the application layer.

The v1.2.2 release specifically tightened this area by rejecting certificate-identity configurations that contain neither SAN nor issuer criteria.

## Artifact binding

The library similarly expects a caller to bind verification to the artifact being authorized. `WithArtifactDigest` verifies that the signed statement/message corresponds to the expected digest. The alternative bypass is intentionally named `WithoutArtifactUnsafe`.

This is an important reusable lesson for any signing system: verifying a signature object without binding it to the intended local artifact is incomplete verification.

## Time and trust material

The library models multiple independent time-evidence systems:

- Rekor integrated timestamps;
- RFC3161/TSA timestamps;
- certificate validity;
- explicit public-key validity periods.

Release v1.2.1 fixed a security issue by checking signature time against public-key validity windows. This is strong evidence that upstream treats historical key validity as part of the verification model rather than only checking whether the signature mathematics succeeds.

## Transparency-log behavior

Rekor support is first-class. Current source/release history includes:

- verification of transparency-log material;
- inclusion-proof/promise interfaces;
- current Rekor v1/v2 handling;
- fail-closed work around Rekor v2 parsing;
- recovery from Rekor v1 HTTP 409 conflicts by fetching the existing log entry.

The transparency log remains a trust/privacy boundary. Public logging can expose certificate identity metadata, and verification depends on trusted Rekor log keys from the selected trusted material.

## Performance/reliability evidence

A July 30, 2026 change optimized verification of large DSSE/in-toto predicates. Upstream profiling showed full predicate materialization causing heavy allocation pressure; the new summarized-statement path reads only fields needed during verification and offers a `WithoutStatementPredicate` result option for callers that do not need a fully materialized predicate.

The commit reports an example benchmark for a ~1.4 MiB predicate dropping from roughly 14 MB and hundreds of thousands of allocations per parse to approximately the payload size and a few dozen allocations in the summary path. GitHub Gold treats those numbers as upstream benchmark evidence, not independently reproduced performance results.

This is particularly relevant for SBOM and vulnerability-report attestations, which can contain multi-megabyte predicates.

## Testing and CI evidence

The repository has multiple independent quality surfaces:

- standard Go tests;
- dedicated `test/e2e` coverage;
- Sigstore conformance testing;
- fuzz targets for bundle, verification and transparency-log parsing;
- CodeQL workflow;
- dependency review;
- OpenSSF Scorecard workflow;
- license verification;
- scheduled conformance runs against both public-good and staging environments.

The conformance workflow builds the repository's conformance adapter and runs `sigstore/sigstore-conformance` on pushes, pull requests, manual runs and a twice-weekly schedule.

Upstream README states the project is stable, ready for production use and passes the Sigstore conformance signing and verification suite. GitHub Gold records this as upstream evidence, not a local certification.

## Maintenance and releases

Current inspected `main` head: `ef103a7d4f8f82296e2f2899ca6a23b56952c08a`, dated August 25, 2026.

That commit added a PyPI PEP 740 attestation verification walkthrough, showing the library is being extended into package-ecosystem provenance rather than remaining OCI-only.

Recent maintenance also includes:

- July 30, 2026: v1.3.0 release;
- July 30: large in-toto predicate verification memory optimization;
- July 30: dependency/security maintenance;
- July 28: Rekor v1 conflict handling;
- July 24: nil-pointer hardening in transparency-log handling;
- July 6: v1.2.2 identity-policy hardening;
- June 9: v1.2.1 public-key validity-window security fix.

The latest formal release inspected is **v1.3.0, published July 30, 2026**.

## License

Root source files and inspected public APIs use Apache License 2.0 notices. Repository root includes an Apache-2.0 `LICENSE` file.

No third-party source code was copied into GitHub Gold during this pass.

## Provisional Gold scoring

- Utility: 5/5 — directly reusable supply-chain verification/signing library.
- Working Evidence: 5/5 — formal releases, conformance, unit/e2e testing, fuzzing and active CI.
- Reusability: 5/5 — clean Go package boundaries and trust-policy abstractions.
- Novelty: 4/5 — built on established Sigstore/TUF/Rekor concepts, but packages them into a notably clean reusable integration layer.
- Documentation: 5/5 — README, signing/verification docs, examples, OCI and PyPI walkthroughs.
- Maintenance: 5/5 — active 2026 commits/releases/security fixes.

**Total: 29/30 — provisional S tier.**

## Caveats and trust boundaries

### Trust-root bootstrap

A correct verifier still depends on correct trust material. Public-good TUF bootstrap or custom-root provisioning must itself be protected.

### Identity policy

Issuer/SAN/extension matching is authorization logic. Broad regexes or unsafe identity bypasses can accept an unintended signer.

### Artifact policy

Verification should bind to the expected local artifact/digest. The unsafe bypass should not be treated as equivalent to artifact verification.

### Transparency logs

Rekor introduces both a trust dependency and public metadata/privacy considerations.

### Timestamp policy

A deployment must choose meaningful timestamp and evidence thresholds. Merely having time evidence is not identical to selecting the correct authorization policy.

### BYO key integrations

KMS/HSM support is intentionally outside the built-in library surface. Implementations of `Keypair` or `TrustedMaterial` become independent security-critical components.

### Structured-result consumers

Applications should authorize on verified fields, not on unverified metadata merely present in a bundle. Downstream policy logic remains a separate security boundary.

## Verification boundary

GitHub Gold performed source/document/release/CI inspection only.

Not performed:

- local `go test` or `go build`;
- live signing or verification;
- Fulcio/OIDC authentication;
- Rekor submission/query;
- TUF refresh against production;
- TSA verification;
- fuzz execution;
- benchmark reproduction;
- private Sigstore deployment;
- cryptographic audit.

## Relationship to Cosign

Cosign remains the stronger end-user/OCI operational tool. `sigstore-go` is the stronger reusable library candidate when another Go application needs Sigstore primitives directly.

Upstream explicitly states that parts of Cosign are intended to depend on `sigstore-go`, so the relationship should be represented as layered infrastructure rather than duplicate entries:

`application / Cosign feature → sigstore-go verification/signing primitives → TUF/Fulcio/Rekor/TSA trust services`

## Strong next leads

1. Trace `verify.NewVerifier` and `Verifier.Verify` end-to-end through certificate, timestamp and transparency-log validation to document exact fail-closed ordering.
2. Inspect `pkg/tuf` bootstrap/update behavior, cache paths and rollback/freeze protections inherited from go-tuf.
3. Inspect `pkg/sign/keys.go` to document the exact contract a KMS/HSM adapter must satisfy.
4. Compare `sigstore-go` policy semantics with Cosign v3's higher-level CLI policy defaults.
5. Follow the new PyPI PEP 740 verification path into Python package provenance and package-index integrity tooling.
6. Broaden the next research batch into another category after this supply-chain cluster is sufficiently mapped.