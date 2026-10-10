# NFStream — network flow analytics and feature-extraction framework

- **Repository:** https://github.com/nfstream/nfstream
- **Organization:** NFStream
- **Category:** Networking / observability / defensive security / flow analytics / machine-learning feature extraction
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **26/30 — S tier**
  - Utility: 4/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 4/5
- **Primary languages:** Python with native C/CFFI components
- **License:** LGPL-3.0-or-later
- **Discovery source:** Recursive follow-up from the nDPI dossier; GitHub-first verification
- **Inspection date:** 2026-09-14

## Executive finding

NFStream is a high-level network-flow analytics framework that turns live interfaces or offline packet captures into structured bidirectional flow records. Its strongest value is the combination of packet capture, nDPI-backed application classification, statistical feature extraction, system/process visibility, multiprocessing, export interfaces, and a Python plugin model in one reusable framework.

This is a meaningful complement to the existing nDPI dossier rather than a duplicate. nDPI is the low-level protocol-classification engine; NFStream wraps that class of capability into a researcher- and analyst-friendly flow pipeline with Python APIs, feature computation, plugins, live/offline ingestion, and machine-learning-oriented workflows.

The project has concrete upstream working evidence: dedicated Linux, macOS, and Windows build/test workflows, a current Linux matrix spanning CPython 3.9 through 3.14 plus PyPy 3.11, wheel-publishing automation, CodeQL, and an OSS-Fuzz-backed CI fuzz workflow that builds and runs fuzzers on pull requests.

GitHub Gold did not run NFStream, capture traffic, execute the tests, or independently validate classification accuracy in this run.

## Why it matters

A large amount of practical network analysis begins by converting packets into flows and then deriving features that can be searched, aggregated, modeled, or exported.

NFStream provides that layer directly. Upstream documents use for:

- live network-interface capture;
- offline PCAP processing;
- encrypted application identification and metadata extraction through nDPI;
- bidirectional flow aggregation;
- packet-size and inter-arrival-time statistics;
- early packet-sequence features;
- process/PID attribution through host system visibility;
- pandas and CSV export;
- custom per-flow feature extraction through `NFPlugin`;
- machine-learning training and live model deployment.

This makes it useful for authorized observability, telemetry pipelines, network research, troubleshooting, reproducible experiments, anomaly research, and defensive-security analytics.

## High-value reusable components

### `NFStreamer`

The principal API accepts either a PCAP source or a live interface and yields structured `NFlow` records.

Important configurable behaviors documented upstream include:

- tunnel decoding;
- BPF filters;
- promiscuous mode;
- packet snapshot length;
- active and idle timeouts;
- accounting mode;
- plugin list (`udps`);
- nDPI dissection depth;
- statistical analysis;
- SPLT/early-flow analysis;
- worker count;
- maximum-flow limits;
- performance reporting;
- system visibility polling.

This is the central reusable abstraction for building analyzers without manually reimplementing packet-to-flow state management.

### `NFlow` records

Flow objects expose network and application metadata including addresses, ports, protocol, VLAN/tunnel identifiers, timestamps, direction-specific packet/byte counters, application names/categories, confidence information, requested server names, fingerprints, user-agent/content metadata where available, and optional statistical features.

For research and ML pipelines, the consistent bidirectional record model is one of the most valuable parts of the project.

### nDPI integration

NFStream embeds nDPI-backed application identification rather than relying solely on port numbers.

Upstream documents encrypted-traffic metadata extraction including TLS, SSH, DHCP, and HTTP-related signals. This can materially enrich flow telemetry, though the resulting classifications and fingerprints should be treated as evidence/signals rather than infallible identity.

NFStream release **v6.6.0**, published **2026-02-15**, specifically added support for nDPI 5.x.

### Statistical feature extraction

NFStream documents 48 post-mortem statistical flow features, including directional packet-size and inter-arrival-time minimum, mean, standard deviation, and maximum values plus TCP flag analysis.

It also supports early-flow/SPLT-style features based on the first `n` packets' sizes, directions, and inter-arrival times.

This is particularly reusable for anomaly detection, traffic classification, research datasets, and reproducible ML feature pipelines.

### `NFPlugin` extension model

NFStream supports user-defined plugins for adding or modifying flow features in Python.

This is a major reusability advantage because domain-specific enrichment can be layered onto the flow engine without forking the core packet-processing implementation.

Follow-up research should inspect plugin lifecycle hooks, exception/failure isolation, multiprocessing serialization requirements, and performance effects.

### Process/system visibility

Upstream documents a system-visibility mode that probes host kernel socket state to associate observed flows with process names and PIDs.

This is valuable for endpoint observability and ground-truth collection in controlled experiments, although support and semantics can differ by operating system and privilege level.

### CFFI/native engine

NFStream describes a native CFFI-based computation engine and Linux AF_PACKET_V3/FANOUT support alongside multiprocessing.

This architecture is worth further component-level study because it attempts to preserve Python ergonomics without moving all packet processing into pure Python.

### Export and analytics interfaces

NFStream supports direct pandas and CSV-oriented workflows, making it suitable as a bridge between packet capture and existing Python data-science tooling.

The package currently declares runtime dependencies including CFFI, psutil, dpkt, NumPy, and pandas (with a PyPy-specific version constraint).

## Working evidence

### Linux CI

The current `build_test_linux.yml` matrix includes:

- Ubuntu latest;
- CPython 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14;
- PyPy 3.11;
- recursive submodule checkout;
- installation of native build prerequisites;
- package build/install through `pip install .`;
- execution of `python tests.py` on normal matrix jobs;
- coverage execution on Python 3.10.

This is strong evidence that the project is exercised as an installed package rather than only linted.

### Cross-platform workflow inventory

The inspected workflow directory contains dedicated jobs for:

- Linux build/test;
- macOS build/test;
- Windows build/test;
- wheel build/publishing;
- CI fuzzing;
- CodeQL.

The README also exposes Linux, macOS, Windows, OSS-Fuzz, and coverage status indicators.

GitHub Gold did not independently execute these workflows.

### OSS-Fuzz / CIFuzz integration

The current `cifuzz.yml` workflow uses Google's OSS-Fuzz CIFuzz actions to:

1. build NFStream fuzzers for pull requests;
2. run the fuzzers for 300 seconds;
3. upload crash artifacts if a fuzzing run fails after a successful build.

This is particularly relevant because packet and metadata parsers operate on attacker-influenced or malformed input in many real deployments.

### Packaging evidence

`pyproject.toml` currently identifies the package as version **6.6.1**, requires **Python >=3.9**, and declares **LGPL-3.0-or-later** licensing.

It also contains cibuildwheel configuration and native dependency setup for Linux/musllinux wheel creation.

The most recent GitHub release inspected is **v6.6.0**, published **2026-02-15**. The release notes state nDPI 5.x support plus minor fixes.

The package metadata being at 6.6.1 while the newest GitHub release is 6.6.0 is recorded as a provenance distinction rather than treated as an error; PyPI/package publication may have advanced independently of GitHub Releases.

## Current maintenance

Recent repository activity inspected includes substantial CI and portability maintenance on **2026-08-01**:

- Windows Npcap download retries, validation, and clearer failure handling;
- correction of a Windows multiprocessing/plugin pickling test issue;
- pip-cache handling fixes for macOS/PyPy CI;
- automatic cancellation of superseded workflow runs;
- release-tool compatibility maintenance.

These commits are useful maintenance signals because they respond to real cross-platform build/test failures rather than cosmetic repository churn.

The project is not as continuously active as nDPI itself, so the maintenance score is 4/5 rather than 5/5.

## Platforms and requirements

Upstream presents NFStream as multiplatform and maintains Linux, macOS, and Windows build/test workflows.

Important requirements and constraints include:

- Python >=3.9 according to current package metadata;
- native build dependencies when compiling from source;
- Npcap on Windows for packet capture;
- CFFI and native compiler/toolchain requirements for source builds;
- standard scientific/data dependencies such as NumPy and pandas;
- privileges appropriate to live packet capture on the target platform.

Offline PCAP analysis avoids some of the live-capture privilege and driver constraints.

## Licensing

The root license is **GNU LGPL version 3**, and current package metadata declares `LGPL-3.0-or-later`.

That is reuse-friendly relative to a full GPL application but still imposes LGPL obligations when distributing covered code or linked/combined works. Consumers must preserve notices and satisfy the applicable relinking/source requirements.

NFStream also vendors or incorporates dependencies and submodules with their own licensing. In particular, nDPI's current component-level licensing model should be reviewed separately when a downstream product depends on functionality delivered through that dependency.

No upstream NFStream code was copied into GitHub Gold during this run.

## Security, privacy, and ethical constraints

Network capture and traffic analytics are dual-use. GitHub Gold catalogs NFStream for authorized observability, troubleshooting, interoperability, education, research, and defensive-security work.

Live capture, DPI-derived metadata, host process attribution, and exported flow datasets can contain sensitive information. Deployments should respect authorization, privacy, retention, and applicable legal requirements.

Application classifications, fingerprints, and ML outputs should not be treated as infallible ground truth.

## Caveats and limitations

- Deep/encrypted application classification is inherently imperfect and evolves with protocols and services.
- Live capture behavior depends on platform drivers, privileges, interface configuration, and packet visibility.
- Windows requires Npcap because NFStream does not bundle capture drivers.
- Python convenience does not eliminate native build/runtime dependencies.
- Multiprocessing and plugin behavior can differ across fork- and spawn-based operating systems; recent Windows test fixes provide direct evidence of this portability boundary.
- Statistical features can be useful for ML but do not by themselves establish model validity or generalization.
- nDPI-derived metadata inherits limitations and licensing considerations from the underlying dependency.
- GitHub Gold did not independently benchmark throughput, memory consumption, packet loss, or feature correctness.

## Verification performed by GitHub Gold

This run inspected:

- GitHub repository metadata;
- current README and documented capabilities;
- root LGPLv3 license;
- package metadata and current declared version/runtime requirements;
- GitHub Releases metadata;
- workflow inventory;
- Linux build/test workflow;
- CIFuzz/OSS-Fuzz workflow;
- recent commit history;
- the active GitHub Gold PR's changed-file list for duplicate avoidance;
- the existing nDPI dossier to distinguish the dependency layer from this higher-level framework.

## Verification NOT performed

GitHub Gold did **not**:

- install NFStream;
- compile the native engine;
- execute `tests.py`;
- run fuzzers;
- capture live packets;
- process a PCAP;
- compare NFStream output against another flow meter;
- validate nDPI classifications;
- test process/PID attribution;
- test pandas/CSV exports;
- train or deploy an ML model;
- benchmark performance or packet loss;
- test Windows/macOS/Linux behavior directly;
- audit the codebase for vulnerabilities;
- independently verify every feature field or plugin lifecycle contract.

Claims above therefore distinguish upstream evidence from work directly performed by GitHub Gold.

## Related ecosystem and recursive leads

Strong follow-up targets include:

- `ntop/nDPI` — already cataloged; underlying protocol-classification engine;
- NFStream's `NFPlugin` lifecycle and multiprocessing model;
- native CFFI engine internals;
- system-visibility implementation and OS-specific process attribution;
- OSS-Fuzz harnesses and historical crash classes;
- AF_PACKET_V3/FANOUT capture path on Linux;
- SPLT/early-flow feature implementation;
- reproducibility of research datasets generated across NFStream releases;
- comparison with Zeek flow/log abstractions;
- comparison with Arkime, Suricata EVE output, and IPFIX/NetFlow collectors;
- real-time ML deployment examples and failure modes;
- J4A plugin added in the 6.5.4 release;
- release/package provenance between GitHub Releases and PyPI.

## Gold rationale

**Utility — 4/5:** highly useful for researchers, analysts, network observability, and defensive telemetry pipelines, though narrower than a general-purpose networking library.

**Working Evidence — 5/5:** real cross-platform build/test workflows, broad Python-version testing, package installation tests, OSS-Fuzz/CIFuzz, CodeQL, coverage, wheel automation, and release history.

**Reusability — 5/5:** clean high-level Python API, structured flow objects, plugin model, live/offline sources, exports, and a native engine provide multiple reusable integration surfaces.

**Novelty — 4/5:** packet-to-flow analytics is established, but combining nDPI classification, system visibility, flow statistics, early-flow features, multiprocessing, and ML-oriented plugins behind one Python interface is technically distinctive.

**Documentation — 4/5:** README examples cover major workflows and the project maintains external API/tutorial documentation; some deeper implementation/runtime behavior still requires source inspection.

**Maintenance — 4/5:** current 2026 package/release state and August 2026 cross-platform CI fixes show active maintenance, but commit cadence is lower than the most actively evolving projects in the catalog.

**Total: 26/30 — provisional S tier.**
