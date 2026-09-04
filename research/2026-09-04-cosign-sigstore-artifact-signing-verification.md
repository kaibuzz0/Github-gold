# Cosign — Sigstore artifact signing, verification, and transparency tooling

- **Repository:** https://github.com/sigstore/cosign
- **Organization:** Sigstore
- **Category:** software supply chain / artifact signing / OCI security / provenance verification
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 29 / 30
- **Provisional tier:** S
- **License:** Apache-2.0
- **Primary language:** Go
- **Latest inspected stable release:** v3.1.3 — 2026-08-06
- **Discovery source:** GitHub-first category rotation into software-supply-chain infrastructure. No playlist-derived claims are used in this dossier.

## Executive finding

`sigstore/cosign` is a mature signing and verification tool for OCI images, blobs, binaries, and other artifacts. Its strongest value is not merely CLI convenience: it composes identity-based signing, Fulcio-issued short-lived certificates, Rekor transparency evidence, OCI registry storage, local/public-key workflows, KMS and hardware-backed keys, offline verification bundles, trusted-root material, and policy-aware verification in one production-oriented toolchain.

For GitHub Gold, Cosign is especially valuable because it exposes reusable Go packages under `pkg/` for blob handling, signature logic, OCI structures, providers, verification/policy, and shared types, while its end-to-end and conformance workflows exercise real integration paths rather than only isolated unit tests.

## Why it qualifies as GitHub Gold

1. Practical software-supply-chain utility with broad deployment relevance.
2. Supports identity-based keyless signing as well as traditional keys, KMS, hardware, and private PKI.
3. Signs OCI artifacts by digest and stores signatures alongside artifacts in registries.
4. Supports detached blob signing and verification with Sigstore bundles.
5. Supports offline verification when the required bundle and trusted-root material are available locally.
6. Exposes reusable Go packages rather than only a monolithic command.
7. Maintains cross-platform, PKCS#11, KMS, registry, OCI 1.1, conformance, CodeQL, dependency-review, and other CI surfaces.
8. Publishes multi-platform release assets together with digest metadata and `.sigstore.json` material.
9. Current maintenance continued through 2026-09-03.
10. Apache-2.0 licensing is reuse-friendly, subject to preservation of required notices and attribution.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Directly useful for signing and verifying software artifacts and container supply chains. |
| Working evidence | 5/5 | Stable releases, broad E2E coverage, conformance testing, registry/KMS/PKCS#11 tests, CodeQL and dependency review. |
| Reusability | 5/5 | CLI plus reusable Go packages for signing, verification, OCI, blob, providers and policy-related logic. |
| Novelty | 4/5 | Digital signing is established, but Sigstore's identity/transparency workflow and OCI integration are unusually composable. |
| Documentation | 5/5 | README and Sigstore documentation cover keyless, key-based, OCI, blob, offline and installation workflows. |
| Maintenance | 5/5 | Latest inspected stable release is August 2026 and upstream commits continued through September 3, 2026. |

**Total: 29 / 30 — provisional S tier.**

## Core capability model

The README documents these primary signing modes:

- keyless signing with Sigstore's public Fulcio certificate authority and Rekor transparency log;
- hardware- and KMS-backed signing;
- Cosign-generated encrypted keypairs;
- bring-your-own PKI;
- signing, verifying, and storing OCI signatures in registries.

For keyless signing, Cosign obtains identity information through OIDC, requests a short-lived signing certificate from Fulcio, signs the target artifact, records transparency evidence, and stores signature material in or alongside the OCI artifact workflow.

Verification is policy-sensitive. A valid cryptographic signature is not enough by itself: identity-based verification expects the verifier to specify the intended certificate identity and OIDC issuer. This is a high-value security boundary because it forces callers to define *who* is authorized to sign, not merely whether some valid Sigstore certificate exists.

## Digest-first artifact identity

Upstream explicitly recommends signing container images by digest (`@sha256:...`) rather than mutable tags such as `:latest`.

That design principle is worth cataloging independently of the CLI: **bind authorization and signature evidence to immutable content identity, not a mutable human-friendly reference.**

The same pattern appears in generic OCI artifact workflows, where digest-qualified artifact references provide the stable object identity that the signature covers.

## Offline verification

Cosign supports offline verification when required material is available locally. The README distinguishes two important inputs:

1. the artifact/signature bundle, which can carry the evidence needed for offline validation;
2. trusted-root material, which must remain current if the verifier relies on the Sigstore public-good trust root.

This is valuable for air-gapped systems, but it also establishes an operational caveat: offline verification is only as trustworthy as the freshness and provenance of the trusted root and bundle material supplied to the verifier.

The README itself marks part of its older air-gapped example as out of date, which is useful evidence that operators should prefer current version-specific Sigstore documentation over blindly copying historical command examples.

## Reusable package surfaces

The current `pkg/` tree exposes several independently interesting components:

- `pkg/blob` — blob-oriented operations;
- `pkg/cosign` — central Cosign verification/signing support;
- `pkg/oci` — OCI signature and artifact representations;
- `pkg/policy` — policy-related functionality;
- `pkg/providers` — key/signing provider integrations;
- `pkg/signature` — signature abstractions and implementation support;
- `pkg/types` — shared data structures.

These should be studied as reusable library surfaces rather than treating the repository as only a command-line program.

## Verification and policy boundary

Cosign's identity verification model deserves explicit treatment as a reusable security pattern.

A verifier should normally constrain expected signer identity and issuer, for example through certificate identity and OIDC issuer policy. Regex forms exist for controlled cases, but widening these checks increases the authorization surface.

Important distinction:

- **cryptographic validity** answers whether signature material verifies correctly;
- **identity authorization** answers whether the signer was an allowed principal for the artifact;
- **transparency evidence** provides append-only public evidence of signing events;
- **artifact digest binding** answers whether the signature covers the intended immutable content;
- **trust-root freshness** determines which CA/log/timestamp authorities the verifier trusts.

These are separate invariants and should not be collapsed into a single "signature valid" checkbox.

## CI and working evidence

The current workflow inventory includes dedicated surfaces for:

- builds;
- CodeQL;
- dependency review;
- normal conformance tests;
- nightly conformance tests;
- cross-platform E2E testing;
- PKCS#11 E2E testing;
- KMS/Vault E2E testing;
- registry E2E testing;
- OCI 1.1 registry behavior;
- GitHub OIDC paths;
- attestation verification;
- linting and supply-chain scorecard checks.

The inspected E2E workflow runs cross-platform Go tests on macOS and Ubuntu, executes dedicated PKCS#11 tests, exercises Vault-backed KMS signing, installs a local Sigstore test environment, and tests multiple registry configurations including an insecure registry and an OCI 1.1 registry.

The inspected conformance workflow runs against both **production and staging** environments and invokes the Sigstore conformance test suite.

This is strong evidence that interoperability against the wider Sigstore ecosystem is an explicit project concern.

## CI supply-chain posture

A strong signal is that many GitHub Actions in the inspected E2E and conformance workflows are pinned to immutable commit SHAs, including checkout, setup-go, Vault installer, setup-crane, Chainguard actions, and the Sigstore conformance action.

A caveat remains: the E2E workflow also invokes `sigstore/scaffolding/actions/setup@main`, which is a mutable branch reference. This creates a weaker trust boundary than the otherwise SHA-pinned workflow dependencies.

The workflow also uses service/container image tags such as `hashicorp/vault:latest` in testing. That is acceptable for some compatibility testing but means the E2E environment is not perfectly reproducible from Git references alone.

## Release evidence

The latest stable GitHub release inspected is:

- **v3.1.3**
- published **2026-08-06**
- not marked prerelease
- multi-platform packages/binaries are published
- GitHub asset metadata includes SHA-256 digests
- release assets include `.sigstore.json` sidecar material for packaged artifacts.

GitHub Gold did **not** independently download or hash the release assets in this pass, so digest values are treated as upstream/GitHub release metadata rather than independent verification.

## Maintenance evidence

Repository metadata shows the project was pushed on **2026-09-03**. The latest inspected commit on that date refactored signing flag validation and fixed bundle-path propagation for signing/attestation validation.

This is useful maintenance evidence because it touches correctness around command validation rather than being only documentation churn.

Upstream's README also states that future major development is increasingly centered on `sigstore-go`, while Cosign remains the supported user-facing implementation and current release line. That makes `sigstore/sigstore-go` one of the strongest recursive research targets from this dossier.

## License and reuse boundary

The repository license is **Apache License 2.0**.

No upstream source code was copied into GitHub Gold.

Any future source reuse should preserve required license, attribution, copyright, patent, and NOTICE obligations. Dependency licenses must still be checked independently; the repository's Apache-2.0 license does not automatically relicense all third-party components used by Cosign.

## Important caveats / risks

### 1. Signing is not authorization by itself

A signature can be cryptographically valid while being produced by an identity that should not have authority over the artifact. Verification policy must constrain expected signer identity and issuer.

### 2. Transparency logs can preserve identity information

Upstream warns that keyless signing can associate personally identifying account information with public transparency-log entries. Public log persistence is part of the operational privacy model.

### 3. Tags are mutable

Signing or verifying mutable image tags without resolving the intended digest can create target-confusion risk. Digest-qualified references are the safer artifact identity.

### 4. Offline trust data can go stale

Air-gapped verification still requires trustworthy and sufficiently current root material. A stale trusted root can break verification or preserve outdated trust assumptions.

### 5. Public-good service dependencies matter

Default keyless signing depends on OIDC plus Sigstore services such as Fulcio and Rekor. Service availability, trust roots, and protocol compatibility affect the online workflow.

### 6. KMS/HSM security is external to Cosign

Cosign can integrate with hardware and cloud KMS providers, but key custody, provider IAM, hardware security, audit policy, and compromise recovery remain deployment responsibilities.

### 7. Signature presence is not artifact safety

A correctly signed artifact can still contain vulnerable or malicious software if an authorized signer signs it. Cosign provides provenance/authenticity evidence, not semantic safety analysis.

## Verification performed by GitHub Gold

This pass inspected upstream:

- repository metadata and current maintenance timestamp;
- README and documented signing/verification modes;
- current `pkg/` package structure;
- latest stable release metadata;
- Apache-2.0 license;
- workflow inventory;
- E2E workflow;
- conformance workflow;
- recent commits.

## Not independently verified

GitHub Gold did **not**:

- build Cosign;
- run its unit, E2E, conformance, CodeQL, dependency-review or PKCS#11/KMS tests;
- sign an OCI image or blob;
- verify a signature or attestation;
- obtain an OIDC identity token;
- request a Fulcio certificate;
- publish or query a Rekor entry;
- exercise an OCI registry;
- test KMS, HSM or PKCS#11 providers;
- validate offline trust-root freshness;
- independently hash v3.1.3 release assets;
- reproduce Sigstore conformance results;
- conduct a cryptographic or security audit.

All stronger claims remain outside the verification boundary.

## Related projects / recursive ecosystem

- `sigstore/sigstore-go` — emerging core Go implementation and major future development target.
- `sigstore/rekor` — transparency-log infrastructure.
- `sigstore/fulcio` — signing-certificate authority.
- `sigstore/root-signing` — trusted-root/TUF material.
- `sigstore/sigstore-conformance` — interoperability/conformance suite.
- `google/go-containerregistry` — OCI/container registry primitives used across this ecosystem.
- policy engines and admission controllers that consume Cosign verification evidence.

## Strongest next research leads

1. inspect `sigstore/sigstore-go` as the underlying modern verification/signing library;
2. trace Cosign bundle verification and trusted-root selection line-by-line;
3. inspect Rekor inclusion/integrated-time verification and RFC3161 timestamp handling;
4. inspect Fulcio identity binding and certificate-profile validation;
5. inspect OCI signature/attestation storage and referrer compatibility across registries;
6. inspect `pkg/policy` and identity matching, including regex authorization edge cases;
7. inspect KMS/PKCS#11 provider boundaries and key-reference parsing;
8. inspect release provenance and how Cosign signs/verifies its own release artifacts;
9. evaluate `sigstore/sigstore-conformance` as a standalone Gold candidate;
10. assess replacing remaining mutable workflow refs such as `sigstore/scaffolding/actions/setup@main` with immutable SHAs where practical.

## Verdict

**VERIFIED — provisional S / 29.**

Cosign is GitHub Gold because it combines a production-grade artifact-signing CLI, reusable Go packages, identity-aware verification policy, transparency-log integration, offline bundle support, broad key-provider support, OCI-native workflows, current releases, active maintenance, extensive E2E testing, and formal ecosystem conformance testing. Its most reusable lesson is that software-signing trust is a composition of immutable content identity, authorized signer identity, cryptographic validity, transparency/timestamp evidence, and current trusted-root material—not merely the existence of a signature.