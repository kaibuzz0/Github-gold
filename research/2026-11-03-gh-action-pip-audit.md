# gh-action-pip-audit — 2026-11-03

Discovery: GitHub-first recursive follow-up from existing pypa/pip-audit entry; no usable YouTube transcript evidence. Upstream: https://github.com/pypa/gh-action-pip-audit.

## Evidence and scope
Inspected upstream README.md, action.yml, action.py (first 110 lines), setup/setup.bash, requirements.txt, LICENSE, .github/workflows/ci.yml and .github/workflows/selftest.yml. Latest observed upstream commit fb241f5 is dated 2026-06-08 and concerns action dependency updates. README documents v1.1.0 invocation. Self-test workflow defines checks for intentionally vulnerable requirements and installed environments, virtualenv, pyproject, and expected failure handling. **No passing upstream workflow run was independently confirmed; no local action run, installation, or vulnerability scan.**

## Valuable components
- `action.yml`: composite GitHub Action wiring for requirements, local environments, virtualenv, PyPI/OSV selection, package indexes, lockfiles, summary and ignore lists.
- `action.py`: pip-audit argument builder, Markdown summary generation and output encoding.
- `setup/setup.bash`, `setup/venv.bash`: environment preparation.
- `.github/workflows/selftest.yml`: reusable CI test patterns for vulnerable fixtures and failure behavior (link rather than copy).

## Score and caveats
VERIFIED (source/test definitions; execution unconfirmed), A25 = Utility 5, Working Evidence 4, Reusability 5, Novelty 3, Documentation 4, Maintenance 4. Root LICENSE Apache-2.0; no third-party code copied. Setup checks Python >=3.7, while modern pip-audit requires Python >=3.10: users must select a compatible runtime. `internal-be-careful-allow-failure` deliberately permits vulnerable audits to pass; intended for self-tests only. Private package index credentials and dependency confusion need careful handling. Audit results are limited by available vulnerability records.

## Next
Confirm current self-test CI status; verify lockfile and Windows coverage; check GitHub Action tag versus immutable commit pin; investigate index credential redaction and failure propagation.
