#!/usr/bin/env python3
"""Audit GitHub Gold catalog consistency using only the Python standard library.

Checks:
- catalog/tools.json and catalog/candidate_queue.json parse successfully
- required top-level structures exist
- canonical repository URLs and names are unique
- evidence levels and scores are valid
- queued candidates do not already exist in the canonical catalog
- MASTER_LIST.md contains every canonical project heading
- every canonical project heading represented in tools.json exists exactly once

The script is intentionally read-only. It exits non-zero on invariant failures so it
can be used locally or in CI before catalog promotion changes are merged.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS_PATH = ROOT / "catalog" / "tools.json"
QUEUE_PATH = ROOT / "catalog" / "candidate_queue.json"
MASTER_PATH = ROOT / "MASTER_LIST.md"

VALID_EVIDENCE = {"VERIFIED", "PROMISING", "LEAD", "ARCHIVED"}
VALID_TIERS = {"S", "A", "B", "C", "D"}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_json(path: Path, audit: Audit) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        audit.error(f"missing required file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        audit.error(
            f"invalid JSON in {path.relative_to(ROOT)}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
        return {}

    if not isinstance(data, dict):
        audit.error(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return data


def normalize_repo(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.endswith(".git"):
        value = value[:-4]
    return value.casefold()


def normalize_heading(value: str) -> str:
    """Normalize optional descriptive heading aliases used only in MASTER_LIST.md.

    Human-readable headings may append a parenthetical repository alias, such as
    ``Project Name (`repo-slug`)``. The canonical machine-readable name remains
    ``Project Name``. Only a trailing parenthetical is stripped; the underlying
    project name must still match exactly after case folding.
    """
    value = value.strip()
    return re.sub(r"\s+\([^\n()]+\)\s*$", "", value).strip().casefold()


def validate_entry(
    entry: Any,
    *,
    where: str,
    score_key: str,
    tier_key: str,
    audit: Audit,
) -> tuple[str | None, str | None]:
    if not isinstance(entry, dict):
        audit.error(f"{where}: entry must be an object")
        return None, None

    name = entry.get("name")
    repo = entry.get("repository")
    evidence = entry.get("evidence")
    score = entry.get(score_key)
    tier = entry.get(tier_key)

    if not isinstance(name, str) or not name.strip():
        audit.error(f"{where}: missing non-empty name")
        name = None
    if not isinstance(repo, str) or not repo.startswith("https://github.com/"):
        audit.error(f"{where}: repository must be a https://github.com/ URL")
        repo = None
    if evidence not in VALID_EVIDENCE:
        audit.error(f"{where}: invalid evidence level {evidence!r}")
    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 30:
        audit.error(f"{where}: {score_key} must be an integer from 0 to 30")
    if tier not in VALID_TIERS:
        audit.error(f"{where}: invalid tier {tier!r}")

    license_value = entry.get("license")
    if not isinstance(license_value, str) or not license_value.strip():
        audit.warn(f"{where}: license is missing or empty")

    verification = entry.get("verification")
    if verification is not None and not isinstance(verification, list):
        audit.error(f"{where}: verification must be a list when present")

    return name.strip() if isinstance(name, str) else None, normalize_repo(repo) if isinstance(repo, str) else None


def check_unique(values: list[tuple[str, int]], label: str, audit: Audit) -> None:
    seen: dict[str, int] = {}
    for value, index in values:
        key = value.casefold()
        if key in seen:
            audit.error(f"duplicate {label}: entries {seen[key]} and {index}: {value}")
        else:
            seen[key] = index


def extract_master_headings(text: str) -> list[str]:
    # Project entries are H3 headings under Catalog. Ignore the Entry format example.
    catalog = text.split("## Catalog", 1)
    if len(catalog) != 2:
        return []
    body = catalog[1].split("## Entry format", 1)[0]
    return [match.group(1).strip() for match in re.finditer(r"^###\s+(.+?)\s*$", body, re.MULTILINE)]


def main() -> int:
    audit = Audit()
    tools = load_json(TOOLS_PATH, audit)
    queue = load_json(QUEUE_PATH, audit)

    entries = tools.get("entries", [])
    candidates = queue.get("candidates", [])
    if not isinstance(entries, list):
        audit.error("catalog/tools.json: entries must be a list")
        entries = []
    if not isinstance(candidates, list):
        audit.error("catalog/candidate_queue.json: candidates must be a list")
        candidates = []

    canonical_names: list[tuple[str, int]] = []
    canonical_repos: list[tuple[str, int]] = []
    canonical_name_set: set[str] = set()
    canonical_repo_set: set[str] = set()

    for index, entry in enumerate(entries):
        name, repo = validate_entry(
            entry,
            where=f"catalog/tools.json entries[{index}]",
            score_key="score",
            tier_key="tier",
            audit=audit,
        )
        if name:
            canonical_names.append((name, index))
            canonical_name_set.add(name.casefold())
        if repo:
            canonical_repos.append((repo, index))
            canonical_repo_set.add(repo)

    check_unique(canonical_names, "canonical project name", audit)
    check_unique(canonical_repos, "canonical repository", audit)

    queue_names: list[tuple[str, int]] = []
    queue_repos: list[tuple[str, int]] = []
    for index, candidate in enumerate(candidates):
        name, repo = validate_entry(
            candidate,
            where=f"catalog/candidate_queue.json candidates[{index}]",
            score_key="provisional_score",
            tier_key="provisional_tier",
            audit=audit,
        )
        if name:
            queue_names.append((name, index))
            if name.casefold() in canonical_name_set:
                audit.error(f"queued candidate already exists canonically by name: {name}")
        if repo:
            queue_repos.append((repo, index))
            if repo in canonical_repo_set:
                audit.error(f"queued candidate already exists canonically by repository: {repo}")

    check_unique(queue_names, "queued project name", audit)
    check_unique(queue_repos, "queued repository", audit)

    try:
        master_text = MASTER_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        audit.error("missing required file: MASTER_LIST.md")
        master_text = ""

    master_headings = extract_master_headings(master_text)
    if not master_headings:
        audit.error("MASTER_LIST.md: could not find catalog project headings")

    master_counts: dict[str, int] = {}
    for heading in master_headings:
        key = normalize_heading(heading)
        master_counts[key] = master_counts.get(key, 0) + 1

    for name, _ in canonical_names:
        count = master_counts.get(name.casefold(), 0)
        if count == 0:
            audit.error(f"MASTER_LIST.md is missing canonical project heading: {name}")
        elif count > 1:
            audit.error(f"MASTER_LIST.md contains duplicate canonical heading: {name}")

    canonical_keys = {name.casefold() for name, _ in canonical_names}
    for heading in master_headings:
        if normalize_heading(heading) not in canonical_keys:
            audit.warn(f"MASTER_LIST.md heading has no matching canonical JSON entry: {heading}")

    print(
        f"GitHub Gold catalog audit: {len(entries)} canonical entries, "
        f"{len(candidates)} queued candidates, {len(master_headings)} master headings"
    )
    for warning in audit.warnings:
        print(f"WARNING: {warning}")
    for error in audit.errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if audit.errors:
        print(f"FAIL: {len(audit.errors)} error(s), {len(audit.warnings)} warning(s)", file=sys.stderr)
        return 1

    print(f"PASS: 0 errors, {len(audit.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
