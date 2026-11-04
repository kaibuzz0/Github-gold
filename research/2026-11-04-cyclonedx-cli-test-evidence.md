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
