# sigstore-conformance — implementation-neutral Sigstore client interoperability and adversarial verification suite

- **Repository:** https://github.com/sigstore/sigstore-conformance
- **Organization:** Sigstore
- **Category:** software supply chain / conformance testing / interoperability / adversarial verification / CI
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **License:** Apache-2.0 stated in README; no root `LICENSE` file was present during this inspection
- **Primary language:** Python
- **Latest inspected stable release:** v0.0.29 — 2026-06-02
- **Latest inspected repository activity:** 2026-08-25
- **Discovery source:** Recursive follow-up from `sigstore/sigstore-go` and Cosign research. No playlist-derived claims are used in this dossier.

## Executive finding

`sigstore/sigstore-conformance` is a reusable end-to-end conformance harness for Sigstore clients. Its value is not merely that it runs tests: it defines an implementation-neutral command protocol that allows substantially different clients to be exercised against the same signing and verification semantics, then supplies adversarial bundles and live infrastructure workflows to test whether those clients fail closed when Sigstore trust evidence is malformed, inconsistent, untrusted, or cryptographically invalid.

The strongest reusable component is the combination of:

1. `docs/cli_protocol.md` — a small compatibility protocol for driving arbitrary Sigstore clients;
2. `test/client.py` — the process-level client adapter used by the suite;
3. `test/assets/bundle-verify/` — parameterized positive and negative verification fixtures;
4. `test/test_bundle.py` — end-to-end bundle, DSSE, Rekor v2, managed-key, and CPython release verification paths;
5. `action.yml` — a composite GitHub Action that turns the suite into a portable CI gate.

This makes the project useful both as a Sigstore interoperability test suite and as a reference architecture for cross-implementation conformance testing in other security-sensitive ecosystems.

## Why it qualifies as GitHub Gold

1. Tests whole client workflows instead of only isolated library functions.
2. Exercises live Sigstore production and staging infrastructure in addition to prepared fixtures.
3. Defines a client-under-test CLI protocol that decouples the suite from any one implementation.
4. Provides large sets of fail-closed fixtures for malformed bundles, invalid signatures, bad transparency proofs, wrong roots, identity mismatches, and protocol-version edge cases.
5. Includes DSSE/in-toto and Rekor v2 coverage.
6. Includes verification against real CPython release Sigstore bundles when tracker data is available.
7. Publishes client conformance results on a recurring basis.
8. Ships as a reusable composite GitHub Action.
9. Inspected Action dependencies are pinned to immutable commit SHAs, including a fixed commit for CPython release metadata.
10. Active dependency and workflow maintenance continued into late August 2026.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Directly useful for validating Sigstore clients, release tooling, provenance consumers, and interoperability layers. |
| Working evidence | 5/5 | Daily/self-test workflows, production/staging execution, release history, live-client adapters, and extensive positive/negative fixtures. |
| Reusability | 5/5 | Generic CLI protocol plus GitHub Action allows unrelated implementations to use the same test suite. |
| Novelty | 4/5 | Conformance testing is established, but this suite's implementation-neutral trust-workflow testing is unusually reusable. |
| Documentation | 5/5 | README, CLI protocol, action inputs, fixture documentation, release notes, and examples are present. |
| Maintenance | 4/5 | Latest inspected stable release is June 2026 and repository maintenance continued through 2026-08-25. |

**Total: 28 / 30 — provisional S tier.**

## Core architecture

### `docs/cli_protocol.md`

The suite does not require each client to expose the same native command line. Instead, it defines a thin compatibility protocol with two principal operations:

- `sign-bundle`
- `verify-bundle`

The protocol normalizes:

- staging versus production selection;
- OIDC identity tokens;
- Sigstore bundle paths;
- in-toto / DSSE signing;
- custom trusted roots;
- custom signing configuration;
- certificate identity and OIDC issuer policy;
- public-key / managed-key verification;
- artifact path versus `sha256:` digest verification.

A client can therefore provide a small wrapper that translates this protocol to its own native CLI. This is a strong reuse pattern for testing heterogeneous implementations without coupling the test suite to one product's command syntax.

## Workflow-focused test philosophy

Upstream explicitly states that the suite is intended to be workflow-focused rather than a fuzzing or code-coverage project. Tests are designed to exercise the client end to end, including network interactions with Fulcio, Rekor, and other Sigstore infrastructure where applicable.

This distinction matters. A client can have excellent unit coverage while still mishandling the composition of trust roots, identity, transparency evidence, timestamps, DSSE material, or live service responses. The conformance suite targets those integration boundaries.

## Adversarial verification fixture library

`test/assets/bundle-verify/` contains parameterized fixtures that are automatically interpreted as expected success or expected failure based on the fixture naming convention.

Inspected fixture names include failures for:

- empty certificate chains;
- bundles from the wrong Sigstore instance;
- invalid base64 signatures;
- malformed bundle JSON;
- negative transparency-log indexes;
- unknown bundle versions;
- bundles containing a root certificate where a leaf chain is expected;
- bad transparency checkpoint key hints;
- incorrect checkpoint root hashes;
- invalid DSSE signatures;
- mismatched DSSE envelopes.

The current fixture tree also includes a positive SCT-with-extensions case intended to cover forward-looking CT behavior.

This fixture-driven architecture is especially valuable because many new verification cases can be added primarily as data rather than requiring custom test logic.

## Bundle and DSSE verification paths

`test/test_bundle.py` contains concrete workflow tests that:

- automatically execute every bundle fixture;
- require failure for `_fail` fixtures and success for valid fixtures;
- check that signing output does not improperly embed root CA certificates;
- require expected message-signature versus DSSE-envelope forms;
- exercise Rekor v2 hashedrekord bundles;
- sign and verify DSSE/in-toto statements;
- cross-check produced material with the included self-test client.

This gives the suite value beyond static corpus testing: it validates output generated by a client and feeds it back through independent verification logic.

## Rekor v2 coverage

Release **v0.0.29**, published **2026-06-02**, added tests for DSSE envelopes represented through Rekor v2 `hashedrekord` entries.

The preceding **v0.0.28** release removed the older Rekor v2 DSSE/0.0.2 path because that entry type was being discontinued, then the next release introduced the replacement representation.

This sequence is useful maintenance evidence: the suite is tracking protocol evolution rather than freezing tests around obsolete behavior.

## Real-world CPython release verification

One unusually strong test path consumes Sigstore bundle metadata from `woodruffw/cpython-release-tracker` when running in GitHub Actions.

For each tracked CPython release with Sigstore material, the suite derives the expected release-manager identity and OIDC issuer, reconstructs a temporary bundle file, and invokes the client-under-test against the published SHA-256 digest.

The GitHub Action pins the tracker repository to a specific immutable commit rather than following a mutable branch.

This is a practical design lesson: conformance suites become more useful when they mix synthetic adversarial fixtures with verification of real ecosystem artifacts.

## GitHub Action integration

`action.yml` packages the project as a composite Action with inputs for:

- client entrypoint;
- production or staging environment;
- skipping signing tests;
- skipping result upload;
- skipping CPython release tests;
- expected-failure patterns;
- internal debug logging.

The Action:

1. checks out a pinned CPython release metadata snapshot;
2. creates/installs the suite environment;
3. invokes the configured client through the conformance adapter;
4. records metadata about the tested client/repository/commit;
5. uploads a conformance-report artifact for production runs unless disabled.

The inspected `actions/checkout` and `actions/upload-artifact` uses are pinned to immutable commit SHAs.

## Self-test and infrastructure coverage

The repository's self-test workflow runs on pushes, pull requests, manual dispatch, and a daily schedule.

Its current matrix includes:

- production Sigstore infrastructure with CPython release tests enabled;
- production infrastructure with those external release tests skipped;
- staging infrastructure.

The workflow uses the included self-test client backed by `sigstore-python`, making the repository verify its own action/adapter/test machinery against a real Sigstore implementation.

Expected-failure configuration is explicit for optional or not-yet-supported behavior rather than silently ignoring those tests.

## Client conformance reporting

Upstream states that results for known clients are published daily in the Sigstore Client Conformance Report.

This turns the suite from a one-off library test into an ecosystem-level compatibility signal. It can reveal when client behavior diverges as bundle formats, Rekor versions, identity requirements, or trusted-root semantics evolve.

GitHub Gold did not independently inspect or validate every published report result in this pass.

## Release and maintenance evidence

Latest inspected stable release:

- **v0.0.29**
- published **2026-06-02**
- not marked prerelease
- release notes identify Rekor v2 DSSE-as-hashedrekord coverage.

Recent inspected repository activity continued through **2026-08-25**, including dependency updates and GitHub Action dependency maintenance.

This is active enough for a high maintenance score, but not same-day/current-week development at the time of this inspection, so maintenance remains **4/5** rather than 5/5.

## Supply-chain posture

The inspected self-test workflow pins:

- `actions/checkout`
- `actions/setup-python`

by immutable commit SHA.

The composite Action also pins:

- `actions/checkout`
- `actions/upload-artifact`
- the CPython release tracker repository revision

by immutable commit identifiers.

This reduces mutable-tag risk in a project whose purpose is itself software-supply-chain verification.

A deeper pass should still inspect every workflow, setup script, Python dependency lock/update policy, downloaded identity-token path, and report-publishing workflow before describing the whole repository as fully immutable or hermetic.

## License and reuse boundary

The README states that `sigstore-conformance` is licensed under **Apache License 2.0**.

During this inspection, GitHub Gold did **not** find a root `LICENSE` file through the repository contents API. That is a licensing-hygiene caveat worth retaining even though the project explicitly declares Apache-2.0 in its README.

No upstream source code was copied into GitHub Gold.

If code is later adapted, preserve upstream attribution and Apache-2.0 obligations, and verify whether the repository has since added a canonical license file or per-file headers.

## Important caveats / risks

### 1. Conformance is not formal verification

Passing this suite demonstrates behavior against the included workflows and fixtures. It does not prove implementation correctness for all malformed inputs, cryptographic edge cases, or attack strategies.

### 2. Expected failures can hide real gaps if poorly governed

`xfail` is useful for optional features and staged migrations, but clients can obtain superficially cleaner CI by broadly marking tests expected to fail. Consumers should inspect the exact expected-failure set, not only whether the workflow is green.

### 3. Live infrastructure introduces nondeterminism

Production/staging tests depend on external Sigstore services, OIDC test-token availability, networking, and service-side behavior. Failures can reflect infrastructure problems rather than client regressions.

### 4. Fixture coverage must evolve with specifications

Sigstore bundle formats, Rekor versions, transparency mechanisms, trusted-root structures, and certificate/timestamp rules continue to evolve. A conformance suite is only useful while its vectors track those changes.

### 5. Wrapper correctness matters

A thin client adapter can accidentally normalize or alter behavior in a way that hides differences in the underlying client. The adapter itself becomes part of the test trust boundary.

### 6. No root LICENSE file was observed

README licensing is explicit, but the missing canonical root license file is a repository-hygiene issue for downstream reuse until independently resolved.

## Verification performed by GitHub Gold

This dossier is based on source/repository inspection only. GitHub Gold inspected:

- repository metadata and root structure;
- README and documented test philosophy;
- client-under-test CLI protocol;
- composite GitHub Action;
- self-test workflow;
- test tree and bundle test code;
- adversarial bundle fixture names;
- recent release metadata;
- recent commit metadata;
- declared licensing text in the README;
- presence/absence check for a root `LICENSE` path.

GitHub Gold did **not**:

- install the Python dependencies;
- run `pytest`;
- invoke the GitHub Action;
- run against Sigstore production or staging;
- fetch or use the testing OIDC token;
- execute Cosign, sigstore-go, sigstore-python, sigstore-js, or other client adapters;
- reproduce Rekor v1/v2 failures;
- verify CPython release bundles;
- independently validate every fixture's cryptographic construction;
- audit the suite for bypasses;
- perform fuzzing;
- independently verify all published conformance-report results.

Claims about successful conformance remain upstream evidence unless explicitly stated otherwise.

## Reusable components worth tracking

### `docs/cli_protocol.md`

A compact model for normalizing heterogeneous security clients behind one conformance interface.

### `test/client.py`

Process wrapper / adapter layer for invoking arbitrary clients and classifying expected success or failure.

### `test/assets/bundle-verify/`

A valuable corpus of positive and adversarial Sigstore bundles, trust roots, signatures, transparency proofs, identities, and malformed structures.

### `test/test_bundle.py`

End-to-end bundle and DSSE workflow tests, including Rekor v2 and real CPython release material.

### `action.yml`

Reusable CI packaging for dropping the suite into downstream client repositories.

### Published conformance reporting

A model for turning per-client CI into an ecosystem compatibility dashboard.

## Related projects

- `sigstore/cosign` — production CLI and signing/verification client already cataloged in GitHub Gold.
- `sigstore/sigstore-go` — reusable Go verification/trusted-root library already cataloged.
- `sigstore/sigstore-python` — Python client used by the suite's self-test path.
- `sigstore/sigstore-js` — JavaScript implementation that can be evaluated against the same client protocol.
- `sigstore/architecture-docs` — evolving Sigstore architecture/specification source.
- `woodruffw/cpython-release-tracker` — real-world release bundle metadata consumed by the conformance action.

## Strongest follow-up leads

1. Inspect `test/assets/bundle-verify/README.md` and enumerate the complete negative-test taxonomy.
2. Trace transparency-checkpoint, inclusion-proof, integrated-time, SCT, and TSA fixtures back to the exact verification invariant each targets.
3. Audit `test/client.py` for process isolation, argument quoting, timeout behavior, and result classification.
4. Inspect `setup/setup.bash` and the full dependency bootstrap path for supply-chain pinning and hash verification.
5. Inspect `publish-report.yml` and the report aggregation format as a reusable interoperability dashboard design.
6. Compare conformance coverage across Cosign, sigstore-go-backed clients, sigstore-python, and sigstore-js.
7. Examine how Rekor v2 migrations are represented in fixtures and expected failures.
8. Build a small local adapter for an already cataloged Sigstore client and actually run the verification-only subset in a future safe validation pass.
9. Consider the adversarial bundle corpus itself as a reusable test-data component, subject to license clarification.
10. Rotate the next major discovery pass away from Sigstore into another category after this recursive chain.

## Verdict

**VERIFIED — provisional S / 28.**

`sigstore-conformance` is GitHub Gold because it captures a difficult and reusable problem: testing whether independent security clients agree on what must be accepted and, more importantly, what must be rejected. Its generic CLI protocol, adversarial fixture corpus, production/staging execution, CPython release verification, composite Action, and ecosystem reporting make it substantially more valuable than a conventional repository-specific test suite.
