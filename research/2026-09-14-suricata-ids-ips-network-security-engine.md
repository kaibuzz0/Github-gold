# Suricata — IDS/IPS and Network Security Monitoring Engine

- **Repository:** https://github.com/OISF/suricata
- **Author / organization:** Open Information Security Foundation (OISF)
- **Category:** Defensive security / network monitoring / IDS / IPS / protocol analysis
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 28/30 — **S tier**
- **Score:** Utility 5 / Working Evidence 5 / Reusability 4 / Novelty 4 / Documentation 5 / Maintenance 5
- **Primary languages:** C and Rust, with supporting Python/shell/build tooling
- **License:** GPL-2.0 (root LICENSE); inspect individual bundled/dependency notices before extracting components
- **Discovery source:** GitHub-first recursive research following the Zeek, nDPI, and NFStream network-observability cluster

## What it is

Suricata is a mature network Intrusion Detection System (IDS), Intrusion Prevention System (IPS), and Network Security Monitoring (NSM) engine developed by OISF and the Suricata community. It occupies a different layer from the existing Zeek, nDPI, and NFStream dossiers: it combines high-performance packet acquisition and protocol parsing with signature/detection logic, inline prevention capabilities, structured event output, and extensive security-oriented QA.

## Why it matters

Suricata is valuable as both a complete defensive network engine and as an architectural reference for safely processing hostile packet input. Its upstream README explicitly treats parser correctness and resource safety as high-stakes because a crash in IPS mode can disrupt a network, while a compromise of a passive sensor can expose sensitive monitoring data.

Particularly valuable study surfaces include:

- packet acquisition and multi-threaded processing paths;
- application-layer protocol parsers, including substantial Rust parser code;
- signature/detection engine and rule keyword architecture;
- EVE/structured event logging;
- flow and transaction lifecycle management;
- AF_PACKET and other capture/inline paths;
- fuzzing and hostile-input parser hardening;
- protocol fingerprinting and metadata extraction;
- integration with `suricata-update` and external rulesets;
- the companion `OISF/suricata-verify` regression corpus/harness;
- `OISF/libhtp`, the security-aware HTTP parsing lineage;
- performance, memory-management, and resource-exhaustion controls.

## Working evidence

Upstream documents a deliberately extensive acceptance/QA process. Current stated coverage includes:

- GitHub CI on pull requests;
- builds across different operating systems, compilers, optimization levels, and configure features;
- cppcheck and scan-build static analysis;
- Valgrind, AddressSanitizer, and LeakSanitizer runtime analysis;
- regression tests for historical bugs;
- logging-output validation;
- Unix-socket testing;
- PCAP-based fuzz testing under ASAN/LSAN;
- traffic-replay IDS and IPS tests.

OISF also documents deeper manual/private QA including multi-gigabit traffic replay, multi-terabyte PCAP collections, long-running fuzzing, PCAP performance tests, and live performance tests. These are **upstream claims/evidence**, not tests performed by GitHub Gold.

The README exposes an OSS-Fuzz status badge and Codecov integration, providing additional evidence of continuous parser/fuzzing attention.

## Release and maintenance signals

The latest GitHub stable release inspected was **Suricata 8.0.6**, published **July 7, 2026**. Upstream release metadata links a source tarball, detached signature, release-specific documentation, and release notes.

Maintenance remained active in September 2026. Recent inspected commits included:

- an SSLv2 `CLIENT_HELLO` record-length/underflow fix;
- a TLS JA3 allocation-failure/dangling-pointer fix;
- removal of an EOL Debian 11 CI build;
- a Public Suffix List update;
- correction and expanded unit coverage for a fallback `memrchr()` implementation.

This is meaningful maintenance evidence because several recent changes directly address parser memory safety and correctness rather than cosmetic churn.

## Security-maintenance evidence

A July 21, 2026 GitHub advisory documents a high-severity application-layer transaction resource-exhaustion issue affecting Suricata 8.0.0 through 8.0.5, patched in 8.0.6. Another 2026 advisory documents a Lua sandbox allocation-limit issue patched in 8.0.5. These are important caveats, but the public advisories and patched releases are also evidence of an active vulnerability-response process.

The related `suricata-update` ecosystem also had a 2026 rule-archive path-traversal advisory, reinforcing that ruleset ingestion and supply-chain boundaries deserve separate scrutiny.

## Installation / runtime requirements

Suricata is a native network-security engine rather than a lightweight script. Exact dependencies and capture backends vary by operating system and feature set. Deployment commonly requires packet-capture privileges/capabilities, appropriate capture or inline networking configuration, rulesets, and sufficient CPU/memory for traffic volume and enabled protocol/detection features. Refer to upstream installation documentation for supported configurations rather than assuming a generic build recipe.

## Platforms

Upstream QA explicitly describes builds across multiple operating systems and compilers. Linux is a major deployment target; the project also maintains cross-platform build/testing coverage. Capture and inline capabilities vary by OS/backend.

## Reusable components / research value

Suricata is especially valuable for studying defensive implementations of:

1. hostile-input protocol parsing;
2. flow/transaction state machines;
3. multi-threaded packet-processing architecture;
4. IDS rule matching and sticky-buffer design;
5. structured telemetry/event pipelines;
6. fuzzing harnesses and regression-driven parser hardening;
7. memory/resource limits under adversarial traffic;
8. packet capture and inline IPS abstractions;
9. C/Rust interoperability in a mature security engine;
10. reproducible network-security verification through companion test repositories.

## Related projects / recursive leads

- `OISF/suricata-verify` — verification tests and output validation; strong next dossier candidate.
- `OISF/suricata-update` — ruleset acquisition/update tooling; inspect current 1.3.8+ security state.
- `OISF/libhtp` — security-aware HTTP parser; repository is archived but remains historically/architecturally relevant.
- `OISF/suricata-intel-index` — rules/intel index consumed by update tooling.
- Zeek — complementary event-driven/stateful NSM architecture.
- nDPI — embeddable traffic classification.
- NFStream — Python-oriented flow analytics and feature extraction.

## License / reuse caveat

The repository root `LICENSE` contains GNU GPL version 2. Do not blindly copy Suricata source into GitHub Gold or into incompatible projects. Before adapting any particular source file, parser, Rust crate/module, bundled library, test fixture, or generated artifact, inspect that item's copyright/license notices and dependency provenance. This dossier catalogs and links; it copies no upstream source code.

## Verification performed by GitHub Gold

Inspected during this research run:

- upstream repository metadata;
- README and documented QA model;
- root license;
- latest GitHub release metadata;
- recent commit history;
- public 2026 security-maintenance evidence;
- current GitHub Gold branch/catalog search to avoid a duplicate Suricata dossier.

## Not independently verified

GitHub Gold did **not**:

- compile or install Suricata;
- execute its unit/regression suites;
- run `suricata-verify`;
- replay PCAPs or capture live traffic;
- enable inline IPS mode;
- fuzz protocol parsers;
- benchmark throughput or packet loss;
- validate rule accuracy or false-positive rates;
- reproduce the private OISF QA environment;
- independently verify the release tarball signature;
- audit the complete parser/detection codebase.

## Caveats / risks

- IDS/IPS engines consume attacker-controlled input and therefore have a large security-sensitive parser surface.
- Detection quality depends heavily on ruleset quality, configuration, traffic visibility, protocol coverage, and tuning.
- Inline IPS deployment has materially greater operational risk than passive monitoring.
- High traffic rates and expensive parsing/detection features can create CPU/memory pressure.
- Ruleset/update supply chains are a separate trust boundary and should be hardened independently.
- Public vulnerability history should be treated as a reason to track supported patched releases, not to freeze on older builds.

## Follow-up research

1. Deep-inspect `OISF/suricata-verify` and map regression cases to engine behavior.
2. Inspect OSS-Fuzz harnesses and Rust/C parser boundaries.
3. Map AF_PACKET/IPS packet paths and thread/runmode architecture.
4. Review flow/transaction cleanup and resource-exhaustion controls after the 8.0.6 fixes.
5. Study EVE output schemas and interoperability with downstream observability pipelines.
6. Audit `suricata-update` 1.3.8+ archive/ruleset trust boundaries.
7. Compare Suricata, Zeek, nDPI, and NFStream by layer, failure mode, resource model, and reusable component surface.
8. Evaluate `suricata-verify`, `libhtp`, and Rust protocol-parser crates as separate Gold candidates.