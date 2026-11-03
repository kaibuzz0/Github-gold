# CycloneDX Python SBOM generator — research lead (2026-11-03)

## Decision
**PROMISING / candidate for A-tier (provisional 24/30, not yet a canonical catalog entry).** Utility 5, Working Evidence 3, Reusability 4, Novelty 3, Documentation 5, Maintenance 4. Source structure and test *definitions* inspected, but no successful workflow run or independent execution confirmed. Do not conflate this CLI with the already cataloged CycloneDX Python Library.

## Primary evidence inspected
- [README](https://github.com/CycloneDX/cyclonedx-python/blob/main/README.md): command `cyclonedx-py` (or `python3 -m cyclonedx_py`), installation as `cyclonedx-bom`, environment/requirements/Pipenv/Poetry input modes. The README explicitly says uv and PDM manifest/lockfile parsing is **not** supported directly, though their environments can be scanned; Conda package-manager support was removed in v4.
- [pyproject.toml](https://github.com/CycloneDX/cyclonedx-python/blob/main/pyproject.toml): version **7.6.0** in inspected main tree (not independently verified as the latest published release); Python >=3.9,<4; `cyclonedx-python-lib[validation]>=8,<12`; `pip-requirements-parser>=32,<33`; `packageurl-python>=0.11,<2`; CLI entry point `cyclonedx_py._internal.cli:run`.
- [LICENSE](https://github.com/CycloneDX/cyclonedx-python/blob/main/LICENSE): Apache-2.0. No source copied.
- [Python CI workflow](https://github.com/CycloneDX/cyclonedx-python/blob/main/.github/workflows/python.yml): push/PR/tag/daily triggers; lint and dependency checks; pinned action SHAs. **Configured jobs are not evidence that a particular run passed.**

## Reusable components and relationships
The CLI bridges Python environment and manifest parsing to the existing `CycloneDX/cyclonedx-python-lib` BOM model, serializer and validator. Specific useful integration points: `cyclonedx_py._internal.cli:run` command dispatch, input adapters for requirements/Poetry/Pipenv/environment, PURL normalization, and SBOM serialization via the library. Exact adapter module paths and test fixtures remain to be inspected before promoting to VERIFIED.

## Caveats
- An SBOM generated from an environment may differ from the full intended dependency graph; incomplete or stale environments produce incomplete inventories.
- Manifest/lockfile support is selective; do not advertise direct uv/PDM lockfile parsing.
- Project README's comparative accuracy and SCVS-level claims are **upstream assertions**, not independent verification.
- No independent installation, SBOM generation, JSON schema validation, vulnerability scanning, or CI run verification.
- Apache-2.0 permits reuse subject to license and notices; prefer upstream links rather than copying code.

## Next investigation
Inspect source adapter modules and tests; confirm a successful upstream CI run and published release; run reproducible fixture comparisons for requirements, Poetry, Pipenv, and venv; compare output to pip-audit CycloneDX export; check direct dependency graph completeness and malformed inputs. If supported, add one canonical entry to both `MASTER_LIST.md` and `catalog/tools.json` in the same reviewed batch.

## Provenance
GitHub-first recursive follow-up from the cataloged CycloneDX Python Library. No YouTube transcript evidence used.

## Follow-up source inspection — 2026-11-03

Inspected the actual upstream Python modules (not merely the README or configured CI):
- [`cyclonedx_py/_internal/cli.py`](https://github.com/CycloneDX/cyclonedx-python/blob/main/cyclonedx_py/_internal/cli.py) imports `EnvironmentBB`, `RequirementsBB`, `PoetryBB`, and `PipenvBB`, plus CycloneDX outputters and schema validators. It explicitly supports `SOURCE_DATE_EPOCH` for reproducible-build timestamp control. This verifies command-dispatch and serialization integration exist in source, not that all modes execute successfully.
- [`requirements.py`](https://github.com/CycloneDX/cyclonedx-python/blob/main/cyclonedx_py/_internal/requirements.py) implements `RequirementsBB` using `pip_requirements_parser.RequirementsFile`; documents stdin and merged requirements use. Its import of `redact_auth_from_url` identifies an intended credential-sanitization path.
- [`poetry.py`](https://github.com/CycloneDX/cyclonedx-python/blob/main/cyclonedx_py/_internal/poetry.py) defines `_LockEntry` with normalized dependency/extras relationships and uses CycloneDX `Dependency` models. This is more concrete than generic Poetry support claims; graph correctness remains untested.
- [`pipenv.py`](https://github.com/CycloneDX/cyclonedx-python/blob/main/cyclonedx_py/_internal/pipenv.py) defines `PipenvBB`, parses JSON and handles package metadata, supporting the existence of a dedicated Pipenv adapter.
- [`utils/secret.py`](https://github.com/CycloneDX/cyclonedx-python/blob/main/cyclonedx_py/_internal/utils/secret.py) defines `redact_auth_from_url` using a regular expression matching `scheme://username:password@` forms. This is **limited syntactic redaction**, not proof that all credential-bearing URLs, percent-encoded cases, tokens, or logging paths are safe. Test with synthetic credentials only.

**Evidence decision:** Keep PROMISING / provisional A 24. Source inspection strengthens evidence for implemented adapters, but no successful CI execution, independent SBOM generation, graph round-trip, or credential-leak regression test has been confirmed. No source code copied. Priority for next pass: inspect test fixtures and CI run outcomes, then promote only if working evidence justifies it.
