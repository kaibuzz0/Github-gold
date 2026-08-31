# PyPA gh-action-pypi-publish — Trusted Publishing and PEP 740 provenance boundary

- Repository: https://github.com/pypa/gh-action-pypi-publish
- Organization: PyPA
- Category: software supply chain / Python packaging / CI release automation
- Evidence level: VERIFIED
- Provisional Gold score: 27/30
- Provisional tier: S
- License: BSD 3-Clause-style license (`LICENSE.md`)
- Primary language/runtime: Python + GitHub Actions composite action + containerized publishing path
- Research date: 2026-08-30

## Executive summary

`pypa/gh-action-pypi-publish` is the PyPA-maintained GitHub Action for publishing already-built Python distributions to PyPI-compatible indexes. Its strongest value is not merely wrapping Twine: the current action integrates PyPI Trusted Publishing through GitHub OIDC and, for PyPI/TestPyPI trusted-publishing flows, generates and uploads PEP 740 digital attestations by default.

The repository is strong GitHub Gold material because it is a compact, production-facing example of how to separate an untrusted or dependency-heavy build stage from a narrowly privileged release stage, exchange a short-lived GitHub OIDC identity for a package-index credential, bind release provenance to that same workload identity, and fail closed when attestation generation or token exchange fails.

This dossier is based on upstream source, action metadata, releases, workflow definitions, and recent commit history. GitHub Gold did not perform a live PyPI publication or OIDC exchange.

## Gold score

| Dimension | Score | Evidence |
|---|---:|---|
| Utility | 5/5 | Directly automates secure Python package publication and provenance generation. |
| Working evidence | 5/5 | Current releases, smoke-test workflow, action metadata, production PyPI use, and maintained release line. |
| Reusability | 4/5 | Highly reusable for GitHub-hosted Python release pipelines, but intentionally constrained to supported release patterns. |
| Novelty | 3/5 | The mechanisms are standards/ecosystem based rather than unique, but the integration is technically valuable. |
| Documentation | 5/5 | Detailed README with secure deployment guidance, non-goals, and trust-boundary warnings. |
| Maintenance | 5/5 | Active 2026 releases and dependency/security maintenance. |
| **Total** | **27/30** | **Provisional S** |

## What it actually does

The current action metadata exposes publishing inputs for repository URL, package directory, metadata verification, existing-file handling, logging/hash output, and PEP 740 attestations. `attestations` defaults to `true`.

The action is implemented as a composite action that creates and invokes a generated Docker-container action. It explicitly fails on non-Linux runners. The README states that building distributions is a non-goal: callers are expected to produce wheels/sdists in a separate job and hand the completed artifacts to the publishing job.

That separation is security-relevant. Upstream specifically recommends granting `id-token: write` only to the dedicated publishing job rather than globally, and warns against mixing dependency-heavy build machinery into the same privileged job that can obtain an OIDC identity.

## Trusted Publishing flow

With no explicit username/password and with `id-token: write`, the action can use PyPI Trusted Publishing.

The source-level flow in `oidc-exchange.py` is:

1. Normalize the configured package-index URL.
2. Query `https://<index>/_/oidc/audience` to discover the audience expected by that index.
3. Request a GitHub OIDC credential for that audience using the `id` package.
4. Inspect selected token claims for diagnostics and reusable-workflow detection.
5. POST the OIDC token to `https://<index>/_/oidc/mint-token`.
6. Reject non-success responses and render server-provided failure reasons.
7. Extract the short-lived package-index token.
8. Mask the newly minted token in GitHub Actions logs before passing it to the upload path.

The action also detects the common fork-PR condition where GitHub will not provide the needed OIDC permission and emits a distinct failure explanation.

### Important trust boundary

The code decodes selected JWT claims for diagnostics, but it does not locally treat that parsing as authorization. The package index is the party that validates the GitHub OIDC token and decides whether the configured Trusted Publisher identity is authorized to mint a PyPI upload credential.

That distinction matters: merely seeing expected claims in an unverified decoded JWT payload is not proof of authorization. The authorization decision occurs at the package index's OIDC exchange endpoint.

## PEP 740 attestation generation

For supported Trusted Publishing flows to PyPI/TestPyPI, attestations are enabled by default.

`attestations.py`:

- enumerates wheel, `.tar.gz`, and `.zip` distribution files;
- verifies that candidate paths are regular files before signing;
- refuses to proceed if a corresponding `.publish.attestation` file already exists;
- obtains a Sigstore-compatible OIDC identity from the GitHub Actions environment;
- creates a production Sigstore signing context;
- converts each distribution into a `pypi_attestations.Distribution`;
- signs it with `pypi_attestations.Attestation.sign(...)`;
- writes a separate JSON publish-attestation file per distribution.

The explicit preflight checks are useful reusable design ideas. In particular, the action checks for invalid distribution paths and pre-existing publication attestations before iterating through signing, reducing obvious partial-signing/confusion states.

## Identity coupling

The README documents an important property: Trusted Publishing authentication and the generated Sigstore attestations are tied to the same GitHub workflow identity.

This gives a verifier two related but distinct evidence paths:

- PyPI can authorize the workload identity to publish the package;
- a PEP 740 attestation can preserve signed provenance associated with that workload identity for the uploaded artifact.

The action itself is not the entire trust system. The security result depends on GitHub OIDC, PyPI's Trusted Publisher configuration and token-minting service, Sigstore trust infrastructure, the `pypi-attestations` library, and downstream verification policy.

## Reusable components / design patterns

### `oidc-exchange.py`

Useful as a compact reference for a package-index OIDC exchange client:

- audience discovery;
- short timeout usage on network requests;
- differentiated error handling;
- third-party-fork diagnostics;
- token masking;
- separation between diagnostic claim decoding and server-side authorization.

### `attestations.py`

Useful as a reference for:

- artifact enumeration before signing;
- fail-fast preflight validation;
- one-attestation-per-distribution mapping;
- Sigstore OIDC credential discovery;
- production trust configuration;
- PEP 740 attestation serialization.

### workflow architecture

The strongest reusable pattern is architectural rather than a specific function:

`build/test jobs (restricted) -> immutable workflow artifact -> dedicated publish job (id-token: write) -> PyPI Trusted Publishing -> PEP 740 provenance`

This limits the amount of code executing in the OIDC-capable release context.

## Working evidence

The project has an active release line. The latest release inspected was **v1.14.2**, published **2026-07-29**.

That release updated Twine to v7 and bumped `pypi-attestations`/Sigstore dependencies after an ecosystem incident involving short GitHub OIDC lifetimes and slower downstream Sigstore/Rekor operations. This is useful maintenance evidence because the project responded to a real release-path failure mode through coordinated dependency updates rather than leaving the integration stale.

Recent repository commits in July 2026 include those Twine and Sigstore/attestation dependency updates.

The repository also contains dedicated GitHub Actions workflows for Docker-image build/push, reusable smoke testing, and `zizmor` GitHub Actions security analysis.

## Security and operational caveats

### Publishing permissions are powerful

A workflow with `id-token: write` plus a matching PyPI Trusted Publisher registration can obtain a release credential. Upstream therefore recommends scoping that permission to the publishing job and keeping build logic elsewhere.

### Reusable workflows are currently unsupported for Trusted Publishing

The README and exchange implementation explicitly warn about reusable workflows. The code compares `workflow_ref` and `job_workflow_ref` and emits a warning when they differ.

This should not be papered over in a catalog entry: a pattern that works for ordinary GitHub Actions composition may not currently be a supported PyPI Trusted Publishing configuration.

### GitHub OIDC credentials are short-lived

The July 2026 release notes document a real operational incident where package releases with many large wheels began hitting a roughly five-minute identity-lifetime boundary while Sigstore/Rekor work consumed time. Upstream dependency updates addressed a related cache issue, but the broader lesson remains: identity lifetime and external transparency/signing service latency are part of the release-path reliability boundary.

### Attestation generation is not independent verification

The action creates attestations; it does not prove that downstream consumers will verify them correctly. Consumers still need a verification policy that binds the expected artifact and expected publisher/workflow identity.

### Linux runner constraint

The action intentionally supports GNU/Linux GitHub Actions jobs for the publishing step. Platform-specific wheels may be built elsewhere, but publication should be centralized into the supported Linux release job.

### Self-hosted runners are best-effort

Upstream documents self-hosted runners as best effort and cannot exercise them comprehensively in its own CI. A self-hosted release runner also changes the host-trust boundary substantially.

## License

`LICENSE.md` contains a permissive three-clause BSD-style license with source/binary redistribution conditions and a no-endorsement clause. No upstream source was copied into GitHub Gold.

## Verification performed for this dossier

GitHub Gold inspected:

- `README.md`;
- `action.yml`;
- `oidc-exchange.py`;
- `attestations.py`;
- `LICENSE.md`;
- current workflow inventory;
- recent commit history;
- current formal release metadata.

GitHub Gold did **not**:

- publish a package to PyPI or TestPyPI;
- request a live GitHub OIDC token;
- mint a live PyPI token;
- generate or verify a live PEP 740 attestation;
- run the repository smoke tests;
- build the Docker image;
- reproduce the July 2026 timeout incident;
- audit Sigstore, PyPI, GitHub OIDC, Twine, or `pypi-attestations` cryptography/protocol implementations.

## Discovery provenance

Recursive follow-up from the `sigstore-go` / Cosign supply-chain research. The registered YouTube playlists remain seed sources, but no reliable playlist transcript evidence was used for this candidate.

## Related projects

- `sigstore/sigstore-go`
- `sigstore/cosign`
- `sigstore/sigstore-python`
- `pypa/warehouse` (PyPI server)
- `pypa/twine`
- `pypa/packaging-problems`
- `trailofbits/pypi-attestations`
- PEP 740 — Index support for digital attestations

## Strong next leads

1. Inspect `pypa/warehouse` implementation of `/_/oidc/audience` and `/_/oidc/mint-token` to map server-side Trusted Publisher authorization.
2. Inspect PyPI's PEP 740 attestation storage/serving path and verification semantics.
3. Inspect `trailofbits/pypi-attestations` as the artifact/attestation data-model layer.
4. Compare `pypa/gh-action-pypi-publish` with `sigstore/gh-action-sigstore-python` to separate publication provenance from generic artifact signing.
5. Trace how downstream tools retrieve and verify PyPI-hosted attestations.
