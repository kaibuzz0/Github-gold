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
