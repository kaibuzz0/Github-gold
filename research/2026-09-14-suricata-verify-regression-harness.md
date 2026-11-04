# OISF/suricata-verify — Suricata regression and output-verification harness

- **Repository:** https://github.com/OISF/suricata-verify
- **Author / organization:** Open Information Security Foundation (OISF)
- **Category:** Defensive security / network IDS testing / regression corpus / QA tooling
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 27/30
- **Provisional tier:** A
- **Discovery source:** Recursive research from the existing `OISF/suricata` dossier
- **License:** MIT-style permissive license in `LICENSE.txt`

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Provides a practical regression/output-verification system for a production-grade IDS/IPS engine. |
| Working Evidence | 5/5 | CI builds Suricata itself and executes the harness on Linux, macOS, and Windows; harness also has self-tests. |
| Reusability | 4/5 | Test descriptor/check architecture and corpus methodology are reusable, although tightly integrated with Suricata semantics. |
| Novelty | 4/5 | Combines packet fixtures, engine configuration, rules, expected telemetry, negative tests, and feature/version gating in one corpus. |
| Documentation | 4/5 | README documents test creation and a broad `test.yaml` schema with examples. |
| Maintenance | 5/5 | Active September 2026 commits track current Suricata branches and newly discovered parser/security regressions. |

**Total: 27/30 — provisional A tier.**

## What it is

`suricata-verify` is OISF's regression and output-verification repository for Suricata. A test can provide packet input, Suricata configuration, detection rules, version/platform/feature requirements, command overrides, expected exit behavior, and checks against generated output. This makes it more than a packet corpus: it is executable behavioral specification around the Suricata engine.

The README documents both full-suite and single-test execution. A basic test may consist of a PCAP, while richer `test.yaml` descriptors can gate on Suricata version, OS, architecture, compile-time features and source files; execute prerequisite scripts; override engine arguments or commands; retry timing-sensitive cases; specify expected exit codes; and validate EVE JSON, statistics, shell output, and file equality.

## Why it matters

The repository is valuable independently of Suricata's main source tree because it demonstrates a mature pattern for testing packet-processing/security software against stable traffic fixtures and observable outputs. It provides concrete examples of how protocol parser fixes, detection keywords, anomalies, telemetry schemas, IPS behavior and past bug/security regressions can be converted into repeatable tests.

For GitHub Gold, the reusable idea is the architecture: **fixture + configuration + rules + feature gating + expected structured output + regression provenance**. That pattern is applicable to other packet analyzers, protocol parsers, forensic pipelines and telemetry systems.

## Particularly useful components

- **`run.py`** — main test runner and descriptor/check execution machinery.
- **`tests/`** — large behavioral/regression test tree containing PCAP-driven cases and expected output semantics.
- **`createst.py`** — helper that generates a test directory and `test.yaml` from a PCAP, with options for event filtering, rules, checksums, midstream behavior, minimum versions and required features.
- **`check-eve.py`** — EVE JSON checking utility.
- **`eve-validator/`** — structured EVE validation material.
- **`pcap-check.sh` / `pcapng-check.sh`** — packet-fixture integrity/sanity checks used by CI.
- **`.github/workflows/builds.yml`** — useful reference architecture showing the corpus exercised against real Suricata builds on multiple operating systems and maintained branches.

## Test model observed

The documented `test.yaml` format supports, among other controls:

- minimum, maximum and exact Suricata version requirements;
- OS and architecture restrictions;
- required build features;
- required source files;
- optional/no-PCAP tests;
- prerequisite scripts;
- custom engine arguments and complete command overrides;
- retries and repeated execution;
- pre-check scripts;
- explicit PCAP and rule paths;
- expected nonzero exit codes for negative tests;
- EVE JSON filters with field existence, array membership, substring/prefix/suffix and numeric comparisons;
- statistics assertions;
- shell assertions;
- exact file comparisons.

This gives the harness enough expressiveness to encode both positive protocol behavior and expected failure/error behavior.

## Working evidence inspected

Current GitHub Actions CI performs more than linting the corpus:

1. packet fixture checks run through `pcapng-check.sh` and `pcap-check.sh`;
2. the harness runs its own `run.py --self-test`;
3. CI clones the actual `OISF/suricata` repository;
4. Suricata is compiled from source;
5. `suricata-verify` is executed against the resulting engine.

The inspected workflow covers Ubuntu 24.04, AlmaLinux 8, macOS and Windows/MSYS2. Its matrix exercises both Suricata `main` and `main-8.0.x`. The Ubuntu path builds with AddressSanitizer and debug/QA simulation configuration enabled. Pull requests that modify only particular test directories can be narrowed to the relevant tests.

This is strong upstream evidence that the project is an actively used verification system rather than a passive collection of captures.

## Maintenance signals

Recent commits inspected on September 14, 2026 include September 7 backports for Suricata 8.0.x/8.0.7 keyword and issue tests. A September 4 regression fixture documents an RFB/VNC long-name case that could trigger an out-of-bounds Rust slice and engine abort; the commit records both the failing behavior and expected behavior after bounding the in-buffer tail. This is unusually concrete evidence that the corpus is used to preserve parser/security fixes.

No GitHub Releases were present when inspected. That is not a significant negative for this project because it is a continuously maintained test corpus designed to track Suricata development/release branches rather than an independently packaged end-user application.

## Runtime / requirements

The harness is Python-based and expects a Suricata source/build environment for normal verification. Individual tests can additionally depend on Suricata compile-time features, platform capabilities, rules, PCAP fixtures and configuration. CI demonstrates Linux, macOS and Windows execution paths.

## Licensing

The root `LICENSE.txt` grants MIT-style permissive rights to use, copy, modify, merge, publish, distribute, sublicense and sell copies, subject to retaining the copyright and permission notice.

GitHub Gold copied **no** upstream source code, packet captures, rules or fixtures. If a particular PCAP or fixture is ever extracted or redistributed, its test README/provenance should still be inspected individually because packet-capture provenance can carry constraints independent of the harness source license.

## Verification performed by GitHub Gold

Inspected:

- repository metadata and default branch;
- root README and documented test schema;
- root license;
- repository root structure;
- GitHub Actions workflow;
- recent commits;
- GitHub release collection;
- existing GitHub Gold branch/catalog search to avoid a duplicate dossier.

GitHub Gold did **not** clone or install the project, compile Suricata, execute `run.py`, run the self-tests, replay any PCAP, inspect every fixture's provenance, validate expected EVE output, reproduce the RFB crash, or independently confirm every regression test.

## Caveats / risks

- The harness is intentionally coupled to Suricata and its build/features/output schemas; reuse outside that ecosystem requires adaptation.
- A passing upstream regression test demonstrates expected behavior for the tested configuration, not complete correctness or security of the protocol analyzer.
- PCAP fixtures may contain synthetic or captured traffic; provenance and redistribution terms should be checked per fixture before copying data.
- There are no independent GitHub releases; branch compatibility is more important than package-version semantics here.
- Some tests explicitly encode timing/retry behavior, so deterministic interpretation requires attention to each descriptor.

## Relationship to existing Gold entries

This dossier is deliberately separate from `OISF/suricata`. Suricata is the IDS/IPS/NSM engine; `suricata-verify` is the external executable regression corpus and validation harness that tests the engine's observable behavior. It therefore represents a reusable QA/testing component rather than a duplicate catalog entry.

It also complements Zeek-style packet regression approaches and could serve as a reference when evaluating test quality in nDPI/NFStream or other protocol-processing projects.

## Follow-up research

1. Map representative parser/security CVEs or bug fixes to exact `suricata-verify` fixtures and expected assertions.
2. Inspect `run.py` internals for reusable descriptor parsing, filtering and result-reporting architecture.
3. Audit `eve-validator/` and schema-validation behavior as a standalone telemetry-validation component.
4. Sample PCAP provenance/readmes to determine how consistently capture origin and redistribution status are documented.
5. Compare Suricata Verify's fixture architecture with Zeek's `zeek-testing` corpus and OSS-Fuzz parser harnesses.
6. Identify tests that exercise C/Rust parser boundaries, resource limits, malformed stream reassembly and IPS simulation.
7. Determine whether the test descriptor schema is stable/documented enough to support external generators or machine-readable cataloging.
