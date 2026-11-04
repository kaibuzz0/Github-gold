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
