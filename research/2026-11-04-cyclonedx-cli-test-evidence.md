# CycloneDX Python CLI: source-level verification notes (2026-11-04)

Upstream: https://github.com/CycloneDX/cyclonedx-python

## Scope and provenance

This is a source-inspection research note, **not** an installation, build, or independently executed test. The previously discussed research branch and draft PR #7 could not be located among currently discoverable open pull requests/branches, so this narrowly scoped branch was created from current `main`. Do not infer that historical PR claims are current repository state.

## Verified directly from upstream source

- `tests/integration/test_cli.py`: https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli.py
- The module imports `subprocess.run`, `sys.executable`, `unittest.TestCase`, `cyclonedx_py.__version__`, and the integration helper `run_cli`.
- `test_version_as_module` invokes `python -m cyclonedx_py --version` using the current interpreter with `shell=False`; asserts exit status zero and that stdout contains the package version.
- `test_version` invokes the CLI helper with `--version`; asserts zero exit status and matching version.
- `test_help` invokes the CLI helper with `--help`; asserts exit status zero.

These are concrete CLI entry-point and packaging smoke-test assertions, **not** evidence that generated SBOM contents or dependency graphs are correct.

## Evidence assessment

**PROMISING**, provisional **24/30 (A)**, pending repository catalog reconciliation. Upstream source confirms meaningful executable test assertions, but this review did not execute them. No independent successful CI run was inspected in this pass. The project identifies Apache-2.0 in the inspected source header; verify root license before copying any code. No third-party code was copied.

## Research gaps and follow-up

1. Locate exact integration-test modules for requirements, Poetry, Pipenv, and environment adapters through repository tree browsing rather than guessed paths. Guessed `tests/integration/test_requirements.py`, `test_poetry.py`, and `test_pipenv.py` returned 404; this does not establish that those adapters lack tests.
2. Inspect fixture assertions for SBOM component identity, dependency edges, reproducibility, and malformed inputs.
3. Run synthetic-secret tests for URL credential masking and CLI error/log output.
4. Inspect successful CI execution tied to a specific commit and perform isolated CLI smoke tests before promoting to VERIFIED.
5. Check existing `catalog/tools.json` and `MASTER_LIST.md` for duplicates before canonical promotion.

No canonical catalog record or score was changed by this research-only batch.


## Adapter integration assertions confirmed (2026-11-04 follow-up)

The earlier guessed filenames were wrong: the actual modules use the `test_cli_*` naming convention. Directly inspected upstream source on the default branch:

- [Requirements integration tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_requirements.py): parameterized file and stdin input cases assert exit code zero and compare normalized SBOM output to stored snapshots across supported schema/output combinations. Missing-file failures are asserted. Synthetic `--index-url` and `--extra-index-url` URLs containing `user:password@` are included in snapshot comparisons.
- [Poetry integration tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_poetry.py): snapshot assertions cover baseline lockfile input, dependency group inclusion/exclusion, dev dependency exclusion, and selected/all extras. Invalid group and extras selections are asserted to fail.
- [Pipenv integration tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_pipenv.py): snapshot assertions cover baseline Pipfile.lock parsing, category selection, dev dependencies, and a synthetic credential-bearing PyPI mirror URL. Missing-file handling is checked.
- [Environment integration tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_environment.py): includes a particularly useful regression for inherited `PYTHONPATH` contamination. A synthetic `leakypkg` appears in output without `-E` and is asserted absent with `-E`. Another test checks `-S` suppression of site evaluation with a deliberately malicious `.pth` fixture.

**Evidence implication:** These are substantially stronger than simple CLI help/version smoke tests: the source defines fixture-backed expected-output comparisons and negative cases. This supports upgrading the candidate's *working-evidence assessment*, but no independent test execution or snapshot-content review occurred in this pass. Retain **PROMISING / provisional A 24/30** until canonical catalog reconciliation and explicit promotion criteria are checked.

**Security boundary:** Synthetic user/password URLs in tests do not by themselves establish that every secret is redacted from stdout, stderr, logs, generated SBOMs, or unusual encoded URL forms. The `-S` and `-E` tests demonstrate specific mitigations in test assertions, not a general guarantee that scanning an untrusted Python environment is safe.

**Next steps:** Inspect the stored JSON/XML snapshots for dependency edges, purls and credential masking; confirm a successful CI run at the same upstream commit as these files; execute isolated tests with synthetic fixtures if possible. No source was copied, no tests were run locally, and no canonical catalog entry was modified.

## Snapshot harness and reproducibility audit (2026-11-04)

Inspected upstream [tests/__init__.py](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/__init__.py), [tests/integration/__init__.py](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/__init__.py), [requirements tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_requirements.py), [Pipenv tests](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_pipenv.py), and [snapshot README](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/_data/snapshots/README.md).

- Snapshot assertions compare normalized output against checked-in fixture files under `tests/_data/snapshots/`; paths are constructed with a `.bin` suffix even for JSON/XML text. Requirements cases cover file versus stdin and a matrix of schema versions and output formats. Pipenv cases cover categories and synthetic authenticated mirrors.
- `make_comparable` normalizes repository-local file URIs, the CLI's own version, and selected cyclonedx-python-lib metadata. XML also normalizes an older Python XML writer's quotation behavior. **Therefore snapshot equality deliberately does not validate the exact original metadata values that are stripped or replaced.** Dependency edges and purls may still be present in snapshots, but their correctness has not been audited.
- `SUPPORTED_OF_SV` excludes JSON output for schema v1.0 and v1.1; tests should not be described as covering every schema/format combination.
- The test helper invokes the internal CLI function `_run_cli(argv=args)` with captured stdout/stderr and synthetic stdin; it clears `SOURCE_DATE_EPOCH` from its patched environment. These adapter tests **do not** establish behavior of the installed shell executable or independence from host environment in all circumstances. Separate entry-point smoke tests cover module invocation.
- **Verification trap:** setting `CDX_TEST_RECREATE_SNAPSHOTS=1` rewrites expected fixtures *before* comparison, so a green test run in regeneration mode would not be an independent regression check against pre-existing expected outputs. For verification, leave this variable unset and review snapshot diffs explicitly. Upstream documentation describes the regeneration option.
- Source-level licensing is confirmed by upstream root `LICENSE` (Apache-2.0); no source was copied. This pass performed source inspection only, not test execution or independent SBOM validation.

**Assessment:** retain PROMISING / provisional A 24/30. The next highest-value check is to read specific `.bin` snapshots for purls, dependency references, and any literal `user:password` occurrences, then compare against the associated fixture inputs. Verify CI at the exact inspected revision before promotion.

**Workflow correction:** On this pass both draft PR #7 and draft PR #8 were discoverable as open; the earlier note that PR #7 could not be found was an observation from that earlier search, not its current status. Continue the existing PR #8 research branch for this dossier.

## Inspected concrete requirements SBOM snapshot (2026-11-04)

Primary upstream artifacts inspected directly (source inspection, **not** a locally generated SBOM):

- [Credential-bearing test invocation](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/integration/test_cli_requirements.py) — `test_with_index_auth` supplies synthetic `https://user:password@` URLs for three indexes, enables `--output-reproducible`, and compares normalized output against a checked-in snapshot.
- [Exact JSON snapshot](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/_data/snapshots/requirements/index_auth_frozen_1.6.json.bin) — CycloneDX JSON schema 1.6, with two library components: `colorama@0.4.6` and `FooProject@1.2`. Each has a `pkg:pypi/...` purl and a line-derived `bom-ref` (`requirements-L4` and `requirements-L7`). `FooProject` carries two SHA-256 distribution hashes matching the input fixture. Three distribution-reference hosts appear without the synthetic `user:password@` userinfo.
- [Input requirements fixture](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/_data/infiles/requirements/frozen.txt) — two pinned packages, including the two hashes on `FooProject`; compared against the snapshot fields above.
- [Snapshot comparison implementation](https://github.com/CycloneDX/cyclonedx-python/blob/main/tests/__init__.py) — normalizes file URIs and selected tool/library metadata; does not show blanket removal of package purls or index URL userinfo in the inspected JSON normalization function.

**What the evidence supports:** This specific committed expected-output fixture preserves package names, versions, purls, hashes and index hostnames while omitting the synthetic username/password from its distribution URLs. That is narrower than proving all credentials are masked: other URL encodings, stderr/logs, XML output, and runtime behavior have not been independently checked. The fixture's `dependencies` array has three `ref` entries (the two requirements and `root-component`) but **no `dependsOn` edges**. Therefore this fixture does not prove accurate transitive dependency-graph construction. The root component is populated from the optional `--pyproject` fixture, and its license expression is `Apache-2.0 OR MIT`.

**Verification boundary:** The snapshot is a stored expected output, not independently executed output. It was inspected as text via the upstream repository; no package installation, code execution, schema validation, or broad secret-scanning was performed. Retain **PROMISING / provisional A 24/30** until representative generation and stronger graph/security checks. No upstream code was copied.

**Next targeted work:** Inspect Poetry/Pipenv snapshots with explicit `dependsOn` edges, compare credential-bearing XML snapshots, run tests without `CDX_TEST_RECREATE_SNAPSHOTS`, and confirm successful CI at the same upstream revision.


## Poetry dependency-edge snapshot inspection (2026-11-04)

Inspected the **actual checked-in upstream** [Poetry JSON fixture](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/snapshots/poetry/plain_with-urls_lock21_1.2.json.bin), located by searching upstream source for `dependsOn` rather than guessing filenames. The corresponding [Poetry integration tests](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/integration/test_cli_poetry.py) compare generated normalized output against snapshots through `test_plain_as_expected` and other fixture-backed cases.

**Concrete stored graph evidence:** The `with-urls` root application has explicit `dependsOn` edges to `Pillow@10.1.0`, `numpy@1.24.4`, `six@1.16.0`, and `wxPython@4.2.2`. The `wxPython@4.2.2` component has edges to `numpy@1.24.4` and `six@1.16.0`. The snapshot contains four corresponding component records and `bom-ref` identifiers. It also records VCS and distribution source URLs, including a pinned Pillow Git revision and a wxPython wheel URL. This demonstrates that at least one committed Poetry expected-output fixture encodes nontrivial dependency relationships; it closes the earlier *fixture-inspection* gap left by the requirements snapshot with no edges.

**Important version boundary:** This exact fixture declares **CycloneDX schema 1.2**, not 1.6. Do not describe it as proving graph handling in every schema version or current runtime release. A checked-in expected fixture plus test assertions is upstream test-design evidence, **not** an independently executed graph-correctness test. The input Poetry lockfile was not compared line-by-line here, and CI at the exact linked upstream revision was not checked. No package installation or tests were performed, and no third-party code was copied.

**Assessment:** retain **PROMISING / provisional A 24/30** pending independently executed fixtures and validation of expected edges against lockfile source. Next: compare the specific Poetry `with-urls` input lockfile to these graph edges, inspect a 1.6 JSON snapshot and Pipenv authenticated-index XML snapshot, then verify tests run without snapshot regeneration.


## CycloneDX 1.6 snapshot and direct-dependency cross-check (2026-11-05)

Pinned upstream revision: `9d0acc7be9e2bdc507104a6d6815761c5522e26e`. Inspected [CycloneDX 1.6 JSON expected snapshot](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/snapshots/poetry/plain_with-urls_lock21_1.6.json.bin), [CycloneDX 1.2 JSON expected snapshot](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/snapshots/poetry/plain_with-urls_lock21_1.2.json.bin), [Poetry direct-dependency template](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/infiles/poetry/with-urls/pyproject-proto.toml), and [integration-test source](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/integration/test_cli_poetry.py).

- The template declares **four direct dependencies**: `wxpython` via a wheel URL, `numpy` via a tarball URL, `pillow` via Git tag 10.1.0, and `six` via Git/SSH tag 1.16.0. The 1.6 expected snapshot records precisely those four root `dependsOn` references, with corresponding component records. This is an input-to-expected-output **direct-dependency** consistency check, not a generated-output execution test.
- Both 1.2 and 1.6 expected snapshots record `wxPython@4.2.2` depending on `numpy@1.24.4` and `six@1.16.0`. **These transitive edges are not asserted by the direct-dependency template**; the original resolved Poetry lockfile must be inspected to confirm them independently.
- The 1.6 snapshot retains the source provenance: Pillow and six VCS URLs/revisions; NumPy and wxPython distribution URLs, SHA-256 hashes on the latter two distribution references, and `cdx:poetry:group=main` component properties. It also marks `cdx:reproducible=true` in metadata. This is a metadata declaration in a stored fixture, **not** proof of byte-for-byte reproducible output across environments.
- The 1.2 fixture lacks some richer 1.6 metadata, but both store the same root and wxPython graph relationships. Schema version changes should be audited for information loss rather than assumed equivalent.
- The integration test enumerates nested `poetry.lock` fixtures with a glob and compares normalized CLI output against snapshots; this pass did not retrieve the matching lockfile, execute the tests, or validate the JSON against the CycloneDX schema.

**Assessment:** PROMISING, provisional **A / 24** unchanged. Direct dependencies are now cross-checked against an upstream input template, while transitive graph correctness remains unresolved. Apache-2.0 upstream license applies; no code copied. Next: locate the nested lockfile and verify wxPython's transitive requirements, inspect an authenticated-index XML snapshot, and run tests without snapshot regeneration.


## Resolved Poetry 2.1 lockfile cross-check (2026-11-05)

Located and inspected the **actual nested lockfile** [`tests/_data/infiles/poetry/with-urls/lock21/poetry.lock`](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/infiles/poetry/with-urls/lock21/poetry.lock), pinned to upstream commit `9d0acc7be9e2bdc507104a6d6815761c5522e26e`. The test discovers this path via `poetry/*/*/poetry.lock`, explaining earlier failed guesses.

- The lockfile contains exactly four resolved packages: `numpy 1.24.4`, `Pillow 10.1.0`, `six 1.16.0`, and `wxPython 4.2.2`. These names and versions match the [CycloneDX 1.6 expected snapshot](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/snapshots/poetry/plain_with-urls_lock21_1.6.json.bin).
- Crucially, `[package.dependencies]` under wxPython explicitly declares `six = "*"` and `numpy = {version = "*", markers = "python_version >= \\\"3.0\\\" and python_version < \\\"3.12\\\""}`. Thus **both wxPython edges in the expected snapshot have corresponding lockfile declarations**. The NumPy edge is **environment-marker conditional**; its presence in the snapshot must not be presented as a universal dependency across every Python version.
- The lockfile independently records NumPy and wxPython distribution URLs/hashes and Pillow/six Git sources with resolved revisions. These are useful fields to cross-check against snapshot provenance; no claim of complete byte-for-byte equality is made here.
- **Scope:** This is a direct inspection and static comparison of upstream checked-in inputs and expected outputs, not local execution, proof of runtime graph correctness, or a successful CI run at this exact commit. Keep **PROMISING / provisional A 24/30** pending actual CLI generation and schema validation. Apache-2.0; no upstream code copied.

**Next highest-value verification:** test the conditional NumPy edge with different Python target environments; run the pinned fixture tests with snapshot regeneration disabled; inspect authenticated-index XML output for leaked credentials. The direct and transitive lockfile-to-snapshot graph cross-check for this specific fixture is now complete.


## Authenticated-index CycloneDX 1.6 XML snapshot audit (2026-11-05)

Inspected the upstream checked-in [requirements/index_auth_frozen_1.6.xml.bin](https://github.com/CycloneDX/cyclonedx-python/blob/9d0acc7be9e2bdc507104a6d6815761c5522e26e/tests/_data/snapshots/requirements/index_auth_frozen_1.6.xml.bin), pinned to revision `9d0acc7be9e2bdc507104a6d6815761c5522e26e`, and compared its fields with the JSON snapshot and previously inspected synthetic-auth integration invocation.

- XML document declares the CycloneDX 1.6 namespace and contains the two expected libraries: `FooProject@1.2` and `colorama@0.4.6`, with matching `pkg:pypi/...` identifiers and line-based component references.
- All three synthetic package-index hostnames are preserved as distribution URLs for both libraries, **without** the supplied `user:password@` URL userinfo. The two SHA-256 values attached to FooProject appear in each corresponding distribution reference.
- Its `dependencies` section contains three empty dependency elements for `requirements-L4`, `requirements-L7`, and `root-component`; no transitive edges are demonstrated by this fixture.
- The XML contains explicit snapshot-normalization placeholders such as `thisVersion-testing`, `libVersion-testing`, and `<!-- stripped -->`. These prevent interpreting the checked-in XML as untouched runtime output. The `cdx:reproducible=true` property is a declared field, not proof of cross-environment byte reproducibility.

**Security scope:** This is a **static review of one expected-output XML fixture**, not an executed secret-leak test. It supports the narrow observation that synthetic basic-auth userinfo is absent from this stored XML artifact. It does not validate unusual encodings, other SBOM inputs, stderr/logging, or runtime redaction. The JSON counterpart exhibits the same narrow property. No third-party code was copied.

**Assessment unchanged:** PROMISING / provisional A 24/30, Apache-2.0. Next: run pinned tests with snapshot regeneration disabled, exercise synthetic credentials in both XML and JSON at runtime, validate output against schema, and test Python-version-dependent Poetry dependency edges.
