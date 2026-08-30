# Cosign — software-supply-chain signing and verification

**Repository:** https://github.com/sigstore/cosign  
**Author / Org:** Sigstore  
**Category:** software supply chain / artifact signing / OCI / provenance / transparency logs / keyless identity / verification tooling  
**Evidence:** VERIFIED  
**Provisional tier / score:** **S / 29**  
**Score breakdown:** Utility 5 / Working Evidence 5 / Reusability 5 / Novelty 4 / Documentation 5 / Maintenance 5  
**License:** Apache-2.0

## Why it matters

Cosign is a mature signing and verification tool for OCI container images and other artifacts. It is useful both as an operator-facing CLI and as a source-level reference for modern software-supply-chain trust flows: identity-based/keyless signing, public-key signing, hardware/KMS-backed keys, OCI signature storage, transparency-log integration, trusted-root handling, offline bundles, attestations, registry interaction, and policy-aware verification.

The project is especially valuable because it connects multiple trust systems behind one practical workflow rather than implementing only a detached-signature primitive. Current upstream documentation identifies support for Sigstore Fulcio/Rekor keyless signing, hardware and KMS signing, encrypted keypairs, bring-your-own PKI, OCI signing/verification/storage, and blob signing/verification.

## Useful components and architecture

### CLI and command composition

The repository contains the `cmd/cosign` CLI plus reusable command packages under `cmd/cosign/cli`. Important operator surfaces include image signing and verification, blob signing and verification, attestations, trusted-root initialization, artifact saving for local/offline verification, and key generation.

### Keyless / identity signing

The default identity-based flow uses OIDC authentication, obtains an ephemeral signing certificate from Fulcio, records verification material in Sigstore transparency infrastructure, and stores the signature/certificate alongside the OCI artifact. Verification requires the expected certificate identity and issuer rather than simply accepting any valid Sigstore certificate.

This identity binding is an important reusable design lesson: cryptographic validity alone is not sufficient; callers must constrain the signer identity they expect.

### Traditional keys, hardware, and KMS

Cosign also supports generated encrypted keypairs, hardware-backed signing, PKCS#11-style integration, and cloud/HSM/KMS workflows. The current module graph includes Sigstore KMS integrations for AWS, Azure, GCP, and HashiCorp Vault together with PIV/PKCS#11 dependencies.

### OCI registry integration

Cosign can sign container images and store associated signature material in OCI registries. Upstream explicitly recommends signing immutable image digests rather than mutable tags, which prevents a signing workflow from accidentally authenticating a different object after a tag moves.

Generic blobs and non-container artifacts can also be uploaded and addressed through OCI registries.

### Transparency logs and trusted roots

Cosign integrates with Rekor transparency infrastructure and Sigstore trusted-root/TUF material. This creates a stronger provenance trail than a standalone detached signature, but it also means verification workflows must understand trusted-root freshness and the privacy implications of public transparency logging.

The README explicitly warns that identity information used during public keyless signing can become permanently recorded in public transparency logs.

### Offline / air-gapped verification

Cosign supports offline verification when the required artifact, signature/bundle, and trusted material are available locally. Upstream documents `cosign save` for preparing local images and verification with `--offline`, while also warning that trusted-root material still needs an update strategy when disconnected.

This makes Cosign relevant to reproducible release verification, constrained networks, recovery media, and other environments where verification may need to occur without live Sigstore services.

### Attestations and policy-adjacent verification

The dependency graph includes in-toto attestation libraries and Open Policy Agent. The repository also has Kubernetes-oriented verification/attestation CI surfaces. This makes Cosign useful as a building block for provenance and admission workflows rather than only manual signature checks.

## Working evidence

Evidence inspected in this pass:

- upstream README and documented sign/verify/keyless/offline workflows;
- Apache-2.0 root license;
- current `go.mod`, which declares module `github.com/sigstore/cosign/v3`, Go 1.26, Sigstore/Rekor/TUF/in-toto/OPA dependencies, cloud KMS integrations, PIV/PKCS#11 support, OCI registry libraries, Kubernetes clients, and related trust tooling;
- GitHub Actions workflow inventory containing build, CodeQL, dependency review, conformance, end-to-end, GitHub OIDC, attestation, lint, Scorecard, and release-related workflows;
- `e2e-tests.yml`, which runs cross-platform end-to-end tests on macOS and Ubuntu and has dedicated PKCS#11, KMS/Vault, and registry test jobs;
- latest formal release **v3.1.3**, published **2026-08-06**;
- active August 2026 maintenance commits.

A particularly strong recent correctness signal is commit `84effabfc90218daa4e4e73bb29bb45de9ef3304` from **2026-08-18**, which corrected non-default key hash handling in verification commands and added regression tests. The commit message records upstream execution of `go build ./...`, `go vet`, targeted/full Go tests, and golangci-lint for the change. GitHub Gold did not independently rerun those commands.

Other August 2026 work includes clearer GitHub Actions OIDC provider errors, privacy-warning corrections for custom/self-hosted Rekor endpoints, sigstore-go v1.3.0 adoption, dependency maintenance, and CI/release adjustments.

## Maintenance and release state

- Repository is active and unarchived.
- Latest release inspected: **v3.1.3 — 2026-08-06**.
- Recent source maintenance observed through **2026-08-19**.
- README states Cosign 2.x remains stable and receives periodic fixes while future major development is increasingly centered in `sigstore-go`.

That last point is important for recursive research: some reusable verification architecture is moving downward into `sigstore/sigstore-go`, so Cosign should not be treated as the only long-term library-level implementation surface.

## Platforms / runtime

Primary implementation language is Go. Upstream publishes Linux/macOS release assets and documents Homebrew, Arch, Nix, GitHub Action, and Kubernetes installation paths. CI includes macOS and Ubuntu end-to-end coverage; release assets include multiple Linux architectures.

Development documentation currently requires Go 1.22+ in the README, while current `go.mod` declares Go 1.26.0. Consumers building `main` should therefore follow the module/toolchain requirements rather than assuming the older README minimum is sufficient for the newest source tree.

## Licensing and reuse

Root license is **Apache-2.0**. No third-party source code was copied into GitHub Gold.

Cosign depends on a large ecosystem of cryptographic, registry, policy, cloud-provider, Kubernetes, and Sigstore components. Anyone extracting a subcomponent should review dependency-level licensing and security assumptions rather than assuming the root license describes every transitive component.

## Caveats / risks

- Catalog inclusion is **not** a cryptographic or supply-chain security audit.
- Identity-based verification is only meaningful when the expected identity/issuer constraints are configured correctly.
- Public transparency logging can create permanent metadata/privacy implications; upstream explicitly warns about this.
- Offline verification still requires a trustworthy and sufficiently current trusted-root strategy.
- Cloud KMS, hardware tokens, PKCS#11 modules, registry credentials, OIDC providers, and private PKI introduce separate trust and availability boundaries.
- Signing mutable OCI tags instead of immutable digests is a workflow hazard; upstream recommends digest-based signing.
- The repository is in an architectural transition: future major work is increasingly based on `sigstore-go`, so API/library consumers should inspect that project rather than relying solely on Cosign internals.

## Verification boundary

GitHub Gold inspected upstream repository documentation, license, module dependencies, workflow/test definitions, release metadata, and recent commit history. It did **not** independently build Cosign, execute its tests, sign an artifact, authenticate through OIDC, contact Fulcio/Rekor, exercise a registry, use a KMS/HSM/token, verify an attestation, test an air-gapped deployment, fuzz cryptographic inputs, benchmark it, or perform a security audit.

## Discovery source

Independent GitHub-first discovery during a deliberate category-broadening pass after the SDR/libiio research cluster.

The six registered YouTube playlists remain seed sources, but playlist search did not provide reliable technical transcript evidence for this candidate in this run. No Cosign claim in this dossier is attributed to a video.

## Related projects / recursive leads

- https://github.com/sigstore/sigstore-go — increasingly important reusable verification/signing library layer and stated basis for future major Cosign development.
- https://github.com/sigstore/rekor — transparency-log service and client ecosystem.
- https://github.com/sigstore/fulcio — certificate authority used by Sigstore keyless identity flows.
- https://github.com/sigstore/root-signing — trusted-root material and trust-distribution workflow.
- https://github.com/in-toto/attestation — provenance/attestation data model used by supply-chain systems.
- https://github.com/slsa-framework/slsa — provenance/security-level framework frequently paired with artifact signing and verification.
- https://github.com/chainguard-dev/rekor-monitor — transparency-log monitoring is a useful follow-up category distinct from signing itself.

## Next research targets

1. Inspect `sigstore/sigstore-go` as the likely reusable library-level successor/foundation for future Cosign major versions.
2. Map one complete keyless verification path from OCI artifact retrieval through trusted-root evaluation, certificate identity constraints, transparency-log verification, and bundle validation.
3. Inspect Cosign's KMS/PKCS#11 provider interfaces for reusable signer abstractions and trust-boundary handling.
4. Compare offline bundle verification with live Rekor/TUF-dependent verification and record exactly which trust material must be pre-provisioned.
5. Inspect release provenance/self-verification: how Cosign release artifacts are themselves signed and how a bootstrap verifier can validate them.
