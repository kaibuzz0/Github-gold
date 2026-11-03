# CycloneDX Python Library — 2026-11-03

## Decision
VERIFIED (upstream source and documented release evidence); S / 27. Six-factor provisional scoring: Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4. This is not an independent runtime certification.

## Evidence inspected
- README: explicitly says this is a reusable library, not a standalone SBOM generator. https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/README.md
- pyproject.toml: package version 11.12.0, Python >=3.9,<4, packageurl-python, py-serializable, sortedcontainers, license-expression; optional JSON/XML validation dependencies. https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/pyproject.toml
- CHANGELOG: v11.12.0 dated 2026-08-13, CycloneDX v1.7 isExternal support. https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md
- Source: cyclonedx/model/bom.py, cyclonedx/output/json.py, cyclonedx/validation/json.py; explicit Apache-2.0 headers. These establish implementation structure, not execution success.
- CI: .github/workflows/python.yml configures push, PR, scheduled testing; no successful run independently checked.
- LICENSE: Apache-2.0; no code copied. https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE

## Reuse targets
BOM dependency model and graph handling; JSON serialization; schema-aware JSON validation; optional XML validation. Source modules should be linked rather than copied.

## Limitations and follow-up
A schema-valid BOM may omit dependencies or contain inaccurate metadata. Validation extras are optional; check runtime availability. Independently run JSON/XML round trips, malformed-document tests, dependency graph edge cases, and version compatibility. Review notices and transitive dependency licensing before extraction. Follow related CycloneDX/cyclonedx-python for standalone generation and pypa/pip-audit for export integration.

## Provenance
GitHub-first recursive discovery from Python supply-chain tooling. No usable YouTube transcript evidence. No local installation or runtime test performed.
