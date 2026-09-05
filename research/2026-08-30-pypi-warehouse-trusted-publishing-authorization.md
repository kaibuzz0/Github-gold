# PyPI Warehouse — Trusted Publishing authorization and attestation boundary

- Upstream: https://github.com/pypi/warehouse
- Project: Warehouse / Python Package Index
- Research date: 2026-08-30
- Category: package registry / software supply chain / OIDC / provenance
- Evidence level: VERIFIED
- Provisional Gold score: S / 28
- License: Apache-2.0

## Executive finding

Warehouse is the server-side authorization boundary behind PyPI Trusted Publishing. The current implementation does substantially more than exchange a GitHub Actions OIDC token for an upload credential.

The inspected flow is:

1. expose the configured PyPI OIDC audience;
2. accept a workload JWT;
3. inspect only the unverified `iss` claim to choose the appropriate OIDC verifier;
4. verify the JWT cryptographically against the issuer's JWKS;
5. enforce issuer, issued-at, expiration, audience, optional not-before, and a single expected audience;
6. locate a registered Trusted Publisher whose stored repository/workflow/owner/environment policy matches the signed claims;
7. prevent JWT replay using the token's `jti` where present;
8. mint a short-lived PyPI macaroon restricted to the OIDC publisher, authorized project IDs, and an expiration window;
9. when attestations accompany an upload, verify them against both the authenticated Trusted Publisher identity and the exact distribution being uploaded before storing provenance.

This makes Warehouse valuable GitHub Gold material not just as a package-index web application, but as a concrete implementation of workload-identity-to-artifact-publication authorization.

## Why it matters

The architecture demonstrates a strong reusable pattern for CI/CD publication systems:

**external workload identity -> cryptographic token verification -> stored publisher policy -> scoped short-lived capability -> artifact + provenance verification**

The important lesson is that OIDC authentication alone is insufficient. Warehouse separately verifies that the authenticated workload corresponds to a publisher policy registered for the project.

## Audience discovery

`warehouse/oidc/views.py` exposes an `oidc.audience` endpoint that returns the configured `warehouse.oidc.audience` value when Trusted Publishing is enabled.

This allows publishing clients to request an OIDC token whose audience is specifically PyPI rather than relying on a generic workload token.

## Issuer selection versus authorization

`mint_token_from_oidc` initially decodes the JWT without verifying its signature, but only to inspect the `iss` claim and determine which configured `OIDCPublisherService` should verify it.

That unverified decode is not treated as authentication or authorization.

Unknown issuers are rejected. Known issuers are routed to their corresponding verifier, after which `mint_token` calls `verify_jwt_signature` before publisher lookup or credential issuance.

This is a useful defensive design boundary: untrusted token metadata may be used for verifier selection, but it does not establish identity.

## JWT verification

`OIDCPublisherService.verify_jwt_signature` resolves the token's `kid` against the selected issuer's JWKS and verifies the token with PyJWT.

The inspected configuration explicitly requires and validates:

- `iss`
- `iat`
- `exp`
- `aud`
- signature validity
- optional `nbf` when present

Warehouse currently restricts accepted JWT signatures in this code path to `RS256` and uses `strict_aud=True`, meaning the configured PyPI audience must be the only audience rather than one member of a multi-audience token.

A 30-second clock-skew allowance is configured for time validation.

### JWKS caching

Issuer JWKS are cached in Redis. When a requested `kid` is absent, Warehouse can refresh from the issuer's OpenID configuration and JWKS endpoint. A refresh cooldown prevents repeated key refreshes within a short window.

Network or malformed-keyset failures fall back to the existing cached key set rather than silently accepting an unverifiable key.

## Canonical issuer boundary

After JWT verification, `find_publisher` checks whether the token issuer matches the service's canonical issuer unless that publisher type explicitly supports custom issuers.

The source comments identify the reason: providers such as GitHub do not themselves filter the database lookup by issuer URL, so without the explicit canonical-issuer check a compromised custom issuer could potentially forge claims resembling a canonical publisher.

This is a particularly useful reusable security pattern: provider-specific claim matching should not accidentally erase the upstream identity-provider boundary.

## GitHub publisher matching

`warehouse/oidc/models/github.py` shows that a GitHub Trusted Publisher is matched using signed claims including:

- repository owner and repository name;
- immutable repository-owner ID;
- workflow filename extracted from `job_workflow_ref`;
- optional GitHub environment constraint.

Repository matching is case-insensitive, consistent with GitHub repository naming behavior.

### Workflow binding

Warehouse checks `job_workflow_ref` against the configured repository/workflow path plus either the signed token's `ref` or `sha`.

This means a stored publisher does not merely authorize an entire GitHub account or repository. The configured workflow file participates directly in authorization.

### Environment binding

A Trusted Publisher can optionally constrain publication to a GitHub environment.

If no environment was configured, Warehouse currently allows publication regardless of the environment claim and may send a warning encouraging project owners to add that restriction when it observes an environment in the workload token.

If an environment is configured, the signed environment claim must be present and match it case-insensitively.

### `pull_request_target` boundary

The GitHub publisher code explicitly rejects publication from workflows invoked by `pull_request_target`.

That is a security-relevant policy because `pull_request_target` workflows operate in a privileged context and require particularly careful handling of untrusted pull-request content.

## Reusable-workflow caveat

Current source still contains a warning boundary around GitHub reusable workflows. Warehouse records metrics when `job_workflow_ref` and `workflow_ref` differ and comments that reusable-workflow support is accidental/not correctly implemented.

This aligns with the client-side `pypa/gh-action-pypi-publish` caveat previously recorded by GitHub Gold: reusable workflows should not be assumed to have the same clean publisher semantics as a directly configured publication workflow.

## Replay protection

Warehouse uses the JWT `jti` when available as an anti-replay key.

`store_jwt_identifier` performs an atomic Redis `SET ... NX` so only one request can successfully claim a previously unseen identifier. The replay key outlives the JWT acceptance window by including the configured JWT leeway plus an additional margin.

If the `jti` has already been claimed, token minting fails.

The unit-test surface includes explicit duplicate-token behavior as well as invalid payload, malformed JWT, unknown issuer, failed signature verification, missing publisher, and pending-publisher paths.

## Short-lived PyPI capability

Only after JWT validation and publisher-policy matching does Warehouse mint an upload credential.

The resulting macaroon contains caveats for:

- the OIDC publisher ID;
- the project IDs attached to that publisher;
- expiration / not-before time.

The source currently sets the minted credential lifetime to **900 seconds (15 minutes)**.

This is a useful capability-security pattern: the external OIDC credential is not turned into a general long-lived PyPI API token. It is exchanged for a narrowly scoped, expiring registry credential.

## Pending Trusted Publishers

Warehouse also supports pending Trusted Publishers for project creation.

If a valid workload identity matches a pending publisher and the project does not already exist, the server can create the project, convert the pending publisher into a normal publisher, record an audit event, and notify the registrant.

The unit tests exercise this path, including organization-owned projects and invalid existing-project cases.

This is powerful but should be understood as a distinct bootstrap workflow: a pre-registered workload identity can participate in first-project creation, not only publication to an existing project.

## PEP 740 attestation enforcement

`warehouse/attestations/services.py` shows that attestations are accepted only when the upload is authenticated through a Trusted Publisher that exposes an attestation identity.

The production `IntegrityService` then verifies every supplied attestation against:

1. `request.oidc_publisher.attestation_identity`; and
2. the exact `Distribution` representing the artifact being uploaded.

The accepted predicate types currently include:

- PyPI Publish Attestation v1;
- SLSA Provenance v1.

Warehouse rejects malformed attestation sets, unsupported predicate types, duplicate predicate types, excessive attestation counts, publisher identities without attestation support, and cryptographic/semantic verification failures.

This is the critical server-side complement to `gh-action-pypi-publish`: an uploaded attestation is not accepted merely because it is syntactically valid or Sigstore-signed. It must bind correctly to both the expected publisher identity and distribution.

## Stored provenance

After successful verification, Warehouse creates a provenance bundle containing the authenticated publisher identity and verified attestations and associates that provenance with the uploaded file.

The repository's attestation internals documentation states that PyPI Publish Attestations are expected to match the Trusted Publisher identity exactly, while SLSA Provenance permits a broader source identity under the configured repository because build and release workflows may be separated.

Downstream consumers therefore still need policy appropriate to the attestation type; presence of provenance is not a universal authorization decision.

## Useful files and components

- `warehouse/oidc/views.py` — audience discovery, token exchange, replay claim, scoped macaroon minting, pending publisher bootstrap.
- `warehouse/oidc/services.py` — JWKS retrieval/cache, JWT verification, canonical issuer enforcement, JTI storage.
- `warehouse/oidc/models/github.py` — GitHub repository/workflow/environment claim policy.
- `warehouse/attestations/services.py` — PEP 740 upload parsing, identity/artifact verification, provenance construction.
- `docs/dev/security/attestation-internals.md` — server-side identity model and attestation-type semantics.
- `tests/unit/oidc/test_views.py` — failure-path and issuance-path unit coverage for OIDC token exchange.

## Runtime / integration requirements

Warehouse is a large production Python web application rather than a drop-in authentication library. Relevant parts depend on infrastructure including:

- PostgreSQL-backed Warehouse state;
- Redis for JWKS/replay state;
- external OIDC providers;
- PyPI macaroon authorization infrastructure;
- `pypi-attestations` for provenance verification;
- Sigstore-backed attestation material through that ecosystem.

The highest reuse value is therefore architectural and component-level unless an adopter is operating Warehouse itself.

## License

The upstream repository declares Apache-2.0 licensing and the inspected files carry SPDX `Apache-2.0` identifiers.

No third-party source was copied into GitHub Gold.

## Maintenance signals

At inspection time on 2026-08-30, the public GitHub repository was active and not archived, with source pushed on 2026-08-29. Warehouse is the implementation serving the Python Package Index and has extensive tests, migrations, documentation, operational code, and continuous maintenance.

Stars are intentionally not used as evidence for the Gold score.

## Gold score

Provisional: **28 / 30 — S tier**

- Utility: 5/5
- Working evidence: 5/5
- Reusability: 4/5
- Novelty: 4/5
- Documentation: 5/5
- Maintenance: 5/5

The reusability deduction reflects that Warehouse is a large service rather than a small standalone library. The novelty score reflects strong implementation design while recognizing that OIDC, capability tokens, JWKS, and Sigstore provenance are established standards/components rather than Warehouse-only inventions.

## Verification performed by GitHub Gold

This pass performed source/document/test inspection only.

Confirmed from current upstream source:

- audience discovery;
- verifier selection using unverified issuer metadata;
- cryptographic JWT verification configuration;
- canonical issuer check;
- GitHub repository/workflow/owner/environment matching;
- `pull_request_target` rejection;
- atomic `jti` replay claim;
- 15-minute project/publisher-scoped macaroon issuance;
- Trusted-Publisher-only attestation ingestion;
- attestation verification against publisher identity and exact distribution;
- provenance bundle construction;
- unit-test coverage for multiple token-exchange failure and success paths.

GitHub Gold did **not** run Warehouse locally, execute pytest, perform a live GitHub OIDC exchange, publish to PyPI/TestPyPI, mint or exercise a real macaroon, manipulate Redis replay state, test key rotation, generate a Sigstore certificate, or independently audit PyJWT, `pypi-attestations`, Sigstore, Rekor, or the production PyPI deployment.

## Caveats / trust boundaries

1. Security still depends on the external OIDC issuer and its key-distribution infrastructure.
2. Redis availability/state participates in JWKS caching and replay protection.
3. The stored Trusted Publisher configuration must itself be correct; an overly broad publisher policy remains broad even when the JWT is valid.
4. Omitting an environment constraint intentionally permits a wider set of GitHub runs from the configured workflow.
5. Reusable-workflow semantics remain a documented caveat in current source.
6. A verified SLSA provenance statement may intentionally have broader identity semantics than a PyPI Publish Attestation; consumers must apply policy appropriate to the predicate.
7. The production service contains additional authorization, upload, database, and operational layers not exhaustively audited in this dossier.

## Relationship to previously researched projects

This completes a useful trust chain already present in GitHub Gold:

**GitHub Actions workload -> `pypa/gh-action-pypi-publish` -> PyPI audience + OIDC JWT -> Warehouse Trusted Publisher authorization -> 15-minute scoped upload credential -> package upload + PEP 740 verification -> stored provenance -> downstream `pypi-attestations` / Sigstore verification**

Related dossiers:

- `research/2026-08-30-pypa-gh-action-pypi-publish-trusted-publishing-attestations.md`
- `research/2026-08-30-sigstore-go-verification-library.md`
- `research/2026-08-30-sigstore-go-tuf-trust-bootstrap-cache-boundary.md`
- `research/2026-08-30-cosign-software-supply-chain-signing.md`

## Strong next leads

1. Inspect `pypi-attestations` directly as the Python data-model and verification layer used by Warehouse.
2. Trace the Warehouse upload-authentication path that consumes the OIDC macaroon and sets `request.oidc_publisher`.
3. Inspect the `/integrity/.../provenance` serving path and caching semantics.
4. Map publisher administration/audit controls: registration, deletion, environment tightening, organization ownership, event records, and notifications.
5. Compare PyPI's workload-identity model with npm trusted publishing or another registry to find reusable cross-ecosystem patterns.
