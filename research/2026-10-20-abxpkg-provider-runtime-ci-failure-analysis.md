# abxpkg provider runtime — evidence and CI review (2026-10-20)

Upstream: https://github.com/ArchiveBox/abxpkg  
Evidence: VERIFIED from upstream release, source, tests, and CI (not independently executed).  
Provisional score: **S / 27** (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 5, Maintenance 4).  
License: MIT, Copyright 2024 Nick Sweeting.

## Reusable components

- `abxpkg/binary.py`: typed binary descriptions and version constraints.
- `abxpkg/binprovider.py`: provider lifecycle and locking.
- `abxpkg/binprovider_npm.py`: npm adapter and cache paths.
- `abxpkg/config.py`: cache identity and environment projection.
- `abxpkg/semver.py`: version parsing.
- `abxpkg/cli.py`: command-line interface.
- `tests/test_security_controls.py` and `tests/test_provider_install_locks.py`: regression tests.

Python >=3.12,<3.15. Upstream documents pip/uv installation and provider support across Linux/macOS. Provider-specific external runtimes are required.

## Verification and maintenance

Version v1.13.58 was released 2026-10-20. Linux CI run 39413598967 passed 30/30 jobs. An earlier macOS test run 39444656035 failed one Deno-provider test because the runtime was unavailable; a later macOS run 39501442167 succeeded, including the Deno test. Its precheck and packaging jobs were skipped as scheduled.

Policy caveat: provider-level options such as release-age thresholds and post-install behavior are not universally enforceable. The upstream tests document warnings when unsupported options are supplied. Installed packages and external providers retain separate licenses. No source copied or independent installation performed.

## Related research deferred

ArchiveBox/abx-plugins remains PROMISING. Main Parallel Tests run 39502689323 had 56 successful, 2 failed, and 3 skipped jobs. The PDF test exceeded a 120-second timeout; an iWork/Keynote PDF download did not finish before its timeout. Root causes remain unresolved. The suite contains reusable hook/config patterns, but broad promotion is deferred.

Six registered YouTube playlists were inaccessible or throttled during this run; no video-derived claims are made.

## Sources

- https://github.com/ArchiveBox/abxpkg/releases/tag/v1.13.58
- https://github.com/ArchiveBox/abxpkg/actions/runs/39413598967
- https://github.com/ArchiveBox/abxpkg/actions/runs/39444656035
- https://github.com/ArchiveBox/abxpkg/actions/runs/39501442167
- https://github.com/ArchiveBox/abx-plugins/actions/runs/39502689323
- https://github.com/ArchiveBox/abxpkg/blob/main/LICENSE
- https://github.com/ArchiveBox/abxpkg/blob/main/pyproject.toml
