# pypi/pypi-attestations — PEP 740 verification and conversion layer

- Repository: https://github.com/pypi/pypi-attestations
- Category: software supply chain / Python package provenance / artifact verification
- Evidence: VERIFIED
- Provisional Gold score: 28/30
- Provisional tier: S
- License: Apache-2.0
- Discovery source: recursive follow-up from the existing PyPI Trusted Publishing / Warehouse / Sigstore research chain
- Verification boundary: source, release, workflow, and documentation inspection only; no local execution was performed

## Executive assessment

`pypi-attestations` is the reference-adjacent Python library that converts between Sigstore Bundles and PEP 740 Attestation objects and verifies those attestations against concrete Python package distributions.

It is materially more useful than a pure schema/serialization package. The current implementation binds verification to:

1. Sigstore cryptographic verification and identity policy;
2. a valid DSSE/in-toto statement shape;
3. exactly one artifact subject;
4. a parseable Python distribution filename;
5. semantic equality between the attested distribution and the candidate artifact;
6. exact SHA-256 digest equality; and
7. a known PEP 740 attestation predicate type.

This makes it a compact reusable trust layer between package-index provenance metadata and the actual wheel/sdist a consumer is evaluating.

## Why it matters

PyPI Trusted Publishing answers the question "who is allowed to publish?" while PEP 740 provenance answers a different question: "does this specific distribution have a verifiable attestation from the expected publishing identity?"

`pypi-attestations` implements the consumer-facing artifact verification layer needed to make that second question operational.

The current researched chain is therefore:

GitHub / CI workload identity
-> Trusted Publisher authorization in Warehouse
-> short-lived scoped upload capability
-> package + PEP 740 attestation publication
-> PyPI provenance storage/serving
-> `pypi-attestations`
-> Sigstore verification + publisher policy
-> exact wheel/sdist filename and digest binding

## Public-purpose surface

The README documents two primary supported library operations:

- create a PEP 740 `Attestation` by signing a Python `Distribution`;
- verify an `Attestation` against a `Distribution` and an expected identity policy.

It also exposes conversions between Sigstore Bundle objects and PEP 740 Attestation objects.

The CLI supports signing, verifying, inspecting, and converting, but upstream explicitly warns that the CLI is primarily experimental and not considered a stable interface. The Python API is therefore the stronger reuse target.

## Core data model

### Distribution

A `Distribution` contains:

- `name`: the wheel or source-distribution filename;
- `digest`: its SHA-256 digest.

`Distribution.from_file()` hashes the actual file contents and validates the filename through Python packaging parsers.

Supported distribution forms in the inspected code are:

- `.whl`;
- `.tar.gz`;
- `.zip` source distributions.

Malformed or unknown distribution formats are rejected before verification proceeds.

### Attestation

A PEP 740 attestation contains:

- format version `1`;
- verification material;
- signing certificate;
- one or more transparency-log entries at the model level;
- a DSSE-style envelope;
- attested statement bytes;
- signature bytes.

The implementation exposes certificate claims from a defined range of Sigstore/Fulcio OIDs, including source repository, owner, workflow/build configuration, repository ref/digest, trigger, invocation URI, runner environment, and repository visibility information where those extensions are present.

## Verification pipeline

The current `Attestation.verify()` path performs the following sequence.

### 1. Resolve identity policy

The caller can provide either:

- an arbitrary Sigstore `VerificationPolicy`; or
- a structured Trusted Publisher object.

Publisher objects are converted into Sigstore verification policies before signature verification.

### 2. Construct production or staging Sigstore verifier

The implementation chooses Sigstore production by default, with optional staging mode. It also exposes an `offline` flag passed into the Sigstore verifier.

### 3. Convert the PEP 740 object back into a Sigstore Bundle

The attestation's certificate, DSSE envelope, signature, and transparency-log data are reconstructed into the form expected by Sigstore's verifier.

### 4. Perform Sigstore DSSE verification

`verify_dsse()` verifies the cryptographic and identity-policy layer. Sigstore verification failure is converted into this package's `VerificationError`.

### 5. Require JSON DSSE content

The returned content type must match the expected DSSE JSON-envelope type.

### 6. Validate the in-toto statement

The payload is parsed as an in-toto statement.

The implementation requires exactly one subject.

### 7. Validate artifact name semantics

The subject must contain a non-empty distribution filename.

Both the attested subject and local candidate distribution names are parsed using `packaging` wheel/sdist filename parsers. Verification compares parsed distribution identities rather than naïvely trusting arbitrary strings.

This allows semantically equivalent wheel metadata representation while still rejecting a subject that refers to a different package/version/build/tag combination.

### 8. Bind to the artifact digest

The subject must contain SHA-256 and that digest must exactly equal the `Distribution.digest` computed for the candidate artifact.

This is the most important artifact-binding property: an identity-valid signature for some other wheel or sdist does not satisfy verification of the local candidate.

### 9. Restrict known predicate types

The current code recognizes:

- `https://slsa.dev/provenance/v1`;
- `https://docs.pypi.org/attestations/publish/v1`.

Unknown predicate types are rejected.

### 10. Return verified predicate information

On success the caller receives the predicate type and predicate body.

## GitHub Trusted Publisher policy

The library contains a dedicated GitHub Trusted Publisher verification policy.

Its baseline requirements include:

- GitHub Actions OIDC issuer `https://token.actions.githubusercontent.com`;
- the expected GitHub source repository URI.

It then verifies the build-config URI against the Trusted Publisher's configured repository and workflow filename.

Because the publisher record does not itself encode the exact runtime ref/SHA, the implementation derives acceptable suffixes from signed certificate claims such as source repository digest and source repository ref and constructs expected workflow URIs from those signed values.

This is a useful design pattern: policy-controlled stable identity fields are combined with runtime-specific values only when those runtime values themselves come from authenticated certificate claims.

## GitLab support

The source also includes a GitLab Trusted Publisher policy with equivalent intent:

- verify GitLab's issuer;
- verify the expected repository;
- require repository digest/ref claims;
- match the build-config URI to the expected workflow filepath plus signed ref/SHA information.

This broadens the package from a GitHub-specific helper into a more general package-index publisher-verification layer.

## Bundle conversion boundary

`Attestation.to_bundle()` reconstructs a Sigstore DSSE bundle from PEP 740 fields.

The inspected implementation currently uses the first transparency-log entry when rebuilding the Sigstore bundle.

It validates the embedded X.509 certificate and transparency-log entry before creating the bundle.

`Attestation.from_bundle()` performs the reverse conversion and requires:

- a DSSE envelope;
- exactly one DSSE signature.

The conversion result stores the signing certificate in DER form and serializes the bundle's transparency-log entry into PEP 740 verification material.

## Working evidence

Upstream CI is substantive.

The unit-test workflow currently runs across Python:

- 3.10;
- 3.11;
- 3.12;
- 3.13;
- 3.14.

A separate offline test job installs Firejail and executes the test suite with networking disabled via `firejail --net=none`, with `TEST_OFFLINE=1` set.

That is particularly relevant because the public verification API exposes offline Sigstore verification behavior; upstream therefore has explicit CI coverage intended to catch accidental network dependencies in offline paths.

The repository also ships dedicated workflows for:

- linting;
- documentation;
- release automation;
- unit/offline testing;
- `zizmor` GitHub Actions security analysis.

## Maintenance and release evidence

The latest inspected formal release is `v0.0.30`, published July 28, 2026.

That release included:

- raw-content handling for JSON parsing;
- CircleCI publisher support;
- CLI help improvements;
- minimum Sigstore version update to 4.5.0.

Repository maintenance continued after that release, including August 2026 dependency/security workflow maintenance. The latest inspected commit is from August 25, 2026.

The repository moved from Trail of Bits into the `pypi` GitHub organization in the v0.0.28 era, which is a useful governance/ownership signal because the package now sits directly alongside Warehouse and other PyPI infrastructure.

## Reusable components

Strong reuse targets include:

- `Distribution` artifact identity + hashing model;
- `Attestation` PEP 740 model;
- Sigstore Bundle <-> PEP 740 conversion;
- exact artifact digest binding;
- parsed wheel/sdist identity comparison;
- GitHub Trusted Publisher certificate policy;
- GitLab Trusted Publisher certificate policy;
- certificate-claim extraction for provenance/UI inspection;
- offline verification support;
- CLI logic for fetching/verifying PyPI provenance as a reference implementation.

## Requirements and platform

Primary language: Python.

Important dependencies visible from source behavior include:

- `sigstore` / sigstore-python;
- `packaging`;
- `cryptography`;
- `pydantic`;
- Sigstore model packages;
- ASN.1 helpers for selected certificate-extension decoding.

The package is naturally portable across platforms supported by its Python and cryptographic dependencies. The inspected CI matrix is Linux-based rather than a cross-OS runtime matrix.

## License

The project is Apache-2.0 licensed.

No upstream source is copied into GitHub Gold by this dossier.

Any future code adaptation should preserve Apache-2.0 attribution and notices as required.

## Caveats and limits

### Verification depends on Sigstore trust

This project delegates cryptographic certificate/transparency-log verification to sigstore-python. Its security properties therefore inherit important trust and implementation boundaries from Sigstore, Fulcio, Rekor, TUF/trusted-root handling, and the configured verification policy.

### Identity policy is mandatory security context

A valid cryptographic signature is insufficient by itself. Consumers must verify against the publisher/repository/workflow identity they actually expect.

### Offline does not mean timeless trust

The API can disable TUF refresh activity, but offline verification still depends on valid local trust material supplied through Sigstore's verification stack.

### CLI stability warning

Upstream explicitly describes the CLI as experimental. Reuse should prefer the public Python API unless a user specifically needs command-line experimentation.

### Transparency-entry conversion

The inspected PEP 740 -> Sigstore conversion reconstructs the bundle using the first transparency entry, even though the PEP 740 verification material model allows a non-empty list. This should be understood before treating the format as a general multi-log abstraction.

### No independent cryptographic audit here

GitHub Gold inspected architecture and upstream evidence only. This dossier does not establish independent correctness of Sigstore cryptography, certificate handling, transparency-log verification, or TUF behavior.

## Gold score

| Dimension | Score | Rationale |
| --- | ---: | --- |
| Utility | 5/5 | Directly verifies PyPI artifact provenance and supports practical package-consumer workflows. |
| Working Evidence | 5/5 | Current releases, tests across Python versions, offline CI, and production integration in the PyPI provenance ecosystem. |
| Reusability | 5/5 | Small Python API with artifact, attestation, publisher-policy, and conversion primitives. |
| Novelty | 4/5 | PEP 740-specific verification and publisher mapping is distinctive, although underlying cryptography comes from Sigstore. |
| Documentation | 5/5 | README/API docs explain supported library and CLI flows plus stability boundaries. |
| Maintenance | 4/5 | Active 2026 maintenance and current release, but still pre-1.0 and explicitly evolving. |
| **Total** | **28/30** | **Provisional S tier** |

## Verification performed by GitHub Gold

Performed:

- inspected repository README;
- inspected current source for `Distribution`, `Attestation`, bundle conversion, verification, and publisher policy logic;
- inspected CI workflow inventory;
- inspected the Python version/offline test workflow;
- inspected recent commit history;
- inspected current release metadata;
- inspected licensing statements;
- checked that this project was not already represented as its own dossier in the current research batch.

Not performed:

- no `pip install`;
- no local signing;
- no local attestation verification;
- no live PyPI provenance retrieval;
- no Sigstore/OIDC interaction;
- no TUF refresh or offline-cache experiment;
- no test-suite execution;
- no malformed-bundle fuzzing;
- no cryptographic audit;
- no cross-platform runtime testing.

## Relationship to existing GitHub Gold research

This project completes a major missing consumer-side layer from the current PyPI provenance chain.

Previously researched components include:

- `pypa/gh-action-pypi-publish`: publisher-side OIDC and attestation generation;
- `pypi/warehouse`: server-side Trusted Publisher authorization and PEP 740 enforcement;
- `sigstore/cosign`: general artifact signing CLI/tooling;
- `sigstore/sigstore-go`: reusable Sigstore verification library;
- Sigstore TUF trust bootstrap/cache behavior.

`pypi-attestations` sits on the consumption/verification side, mapping package-index provenance into a concrete artifact + expected publisher policy decision.

## Strongest next leads

1. Trace Warehouse's `/integrity/.../provenance` response shape into the CLI's PyPI verification path.
2. Inspect `pypi-attestations` test cases specifically for subject confusion, digest mismatch, publisher mismatch, and malformed transparency material.
3. Compare PEP 740 verification semantics with GitHub artifact attestations and SLSA provenance verification.
4. Inspect CircleCI/GCP publisher policy implementations added to the evolving publisher model.
5. After completing the PyPI provenance chain, broaden discovery into another technical category rather than over-clustering further around package publishing.
