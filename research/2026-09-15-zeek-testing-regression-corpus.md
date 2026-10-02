# zeek/zeek-testing — Zeek regression corpus

- **Repository:** https://github.com/zeek/zeek-testing
- **Category:** network observability / protocol regression / packet corpus
- **Evidence:** VERIFIED
- **Provisional Gold score:** 24/30 — A
  - Utility 4/5
  - Working Evidence 5/5
  - Reusability 3/5
  - Novelty 3/5
  - Documentation 4/5
  - Maintenance 5/5
- **Discovery:** recursive follow-up from the Zeek and Suricata Verify dossiers.

## What it is

`zeek-testing` is Zeek's external regression-data repository. It carries packet/trace inputs, expected baseline outputs, Zeek test scripts, trace-update helpers, and btest configuration used by the broader Zeek testing workflow. The repository is valuable less as a standalone application than as a maintained behavioral corpus for validating changes to Zeek protocol analysis and logging.

The root layout contains `Baseline/`, `Traces/`, `tests/`, `scripts/`, `Makefile`, `btest.cfg`, and `traces.cfg`. The Makefile invokes Zeek's `btest` harness, supports normal and leak-check runs, refreshes trace material, and calculates script coverage.

## Useful components

- `Traces/` — packet/trace fixtures consumed by regression tests.
- `Baseline/` — expected output used to detect behavioral changes.
- `tests/*.zeek` — focused test scripts, including IPv6, M57, and CTU scenarios.
- `scripts/update-traces` — trace synchronization helper used by the Makefile.
- `Makefile` — concise example of integrating a large external corpus with btest, leak checking, and script coverage.

This separation of large fixtures/baselines from the main engine repository is a useful architecture pattern for projects whose regression assets would otherwise bloat the core source tree.

## Working and maintenance evidence

The repository is active rather than frozen historical data. Recent 2026 commits update expected output after corresponding Zeek engine changes, including Kerberos logging, mDNS query/reply behavior, LDAP extensions, FTP session logging, and CTU trace maintenance.

A June 2026 CTU cleanup is especially instructive: upstream reduced two very large flows while deliberately retaining the first 20 packets needed to preserve interesting STUN/DTLS and TLS log behavior, reducing debug-build processing cost. This shows active curation of the corpus for signal-to-cost rather than blindly accumulating captures.

The repository is also referenced by Zeek's main CI/testing architecture as external regression data, giving it direct upstream integration evidence.

## Trace provenance

The root README explicitly identifies two M57 traces as originating from DigitalCorpora's 2009 M57 Patents scenario and states that the source corpus is intended for computer-forensics education/research. Upstream notes that checksums in those traces were modified. Provenance should still be evaluated per trace before redistribution because the repository contains multiple fixture families and one README statement should not be generalized to every capture.

## License caveat

No root `LICENSE` or `COPYING` file was found in the inspected repository root. Treat the repository as **link-and-study only** unless licensing/provenance is established for the specific script, baseline, or trace being reused. Do not copy corpus material into GitHub Gold merely because it is public.

## Verification performed

Inspected repository metadata, root tree, README provenance statement, Makefile/btest integration, test-script tree, and recent commit history. Compared the candidate against the current GitHub Gold default-branch catalog/search and active research PR context to avoid an obvious duplicate.

## Not independently verified

GitHub Gold did **not** clone the corpus, execute btest, run Zeek against its traces, reproduce expected baselines, perform leak checks, validate every packet capture, or independently audit the provenance/license of every fixture.

## Why it matters

This is a strong example of an executable network-analysis regression corpus: packet evidence plus expected behavioral output, continuously synchronized with changes in the upstream analyzer. It complements `OISF/suricata-verify`, but its design emphasizes Zeek's btest/baseline model rather than Suricata Verify's descriptor-driven assertions.

## Follow-up leads

1. Map representative `zeek/zeek` fixes to exact `zeek-testing` baseline/trace changes.
2. Inspect `btest` as a reusable regression-harness project in its own right.
3. Audit trace-family provenance and licensing systematically.
4. Compare corpus minimization strategies with Suricata Verify and OSS-Fuzz.
5. Identify protocol areas with high-value real-world traces but weak regression coverage.
6. Examine whether malformed/adversarial parser fixtures live here, in the main Zeek tree, or in separate fuzzing corpora.
