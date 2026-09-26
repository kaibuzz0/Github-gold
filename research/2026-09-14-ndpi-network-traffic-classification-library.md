# nDPI — network traffic classification and protocol inspection library

- **Repository:** https://github.com/ntop/nDPI
- **Organization:** ntop
- **Category:** Networking / observability / defensive security / protocol classification / traffic analysis
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **27/30 — A tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Primary language:** C
- **License:** Core library LGPLv3; additional ntop-created components/dissectors may be dual-licensed and require a commercial license for for-profit use
- **Discovery source:** GitHub-first category rotation into network observability and defensive traffic analysis
- **Inspection date:** 2026-09-14

## Executive finding

nDPI is a mature open-source deep-packet-inspection and network traffic classification library intended to be embedded into monitoring, observability, troubleshooting, policy, and defensive-security applications.

Its value to GitHub Gold is not merely a large list of recognizable protocols. The repository contains a reusable C library, protocol dissectors, flow-state machinery, fingerprinting and metadata extraction, example readers, protocol and category data, anomaly-related helpers, DGA tests, Python bindings, build/package infrastructure, and extensive regression/fuzzing support.

The project is actively maintained because traffic classification is inherently a moving target: application protocols, hostnames, TLS behavior, fingerprints, CDNs, and service endpoints continuously change.

The main caveat is licensing. The core library is LGPLv3, but upstream explicitly documents a dual-license model for additional ntop components. For-profit projects must either restrict use to the LGPLv3 core or obtain the applicable commercial license for those components. GitHub Gold therefore catalogs and links to the project but does not copy upstream implementation code.

## Why it matters

Network observability often needs more than ports and IP addresses. Modern applications multiplex over HTTPS, QUIC, CDNs, cloud infrastructure, VPNs, relays, and rapidly changing endpoint sets.

nDPI attempts to classify traffic using protocol-specific parsing and multiple metadata/fingerprint signals. This makes it useful for legitimate applications such as:

- network inventory;
- observability and telemetry enrichment;
- troubleshooting;
- authorized packet analysis;
- IDS/monitoring enrichment;
- protocol research;
- application/service categorization;
- traffic statistics;
- anomaly and DGA research;
- passive fingerprinting;
- policy enforcement in authorized environments.

Upstream itself warns that protocol detection is not guaranteed to be error-free or 100% accurate and specifically reminds users to respect privacy and authorization requirements when capturing or inspecting traffic.

## High-value reusable components

### Core libnDPI

The core deliverable is a C library that applications can embed rather than a standalone appliance.

The documented build system supports producing only the library with:

`./autogen.sh && ./configure --with-only-libndpi`

followed by `make`.

This separation is useful for projects that need classification without the repository's example and test tooling.

### Protocol dissectors

Protocol implementations live primarily under:

`src/lib/protocols/`

Upstream documents the process for adding a new dissector, including protocol IDs, flow-state variables, search functions, selection bitmasks, default ports, documentation, build integration, and regression testing.

This makes the repository valuable as a reference corpus for writing stateful protocol recognizers.

### Flow-state structures and public API

Important research targets include:

- `src/include/ndpi_api.h`;
- `src/include/ndpi_protocol_ids.h`;
- `src/include/ndpi_typedefs.h`;
- `src/lib/ndpi_main.c`;
- TCP/UDP/general flow structures;
- initialization and classification APIs;
- protocol/category metadata;
- fingerprint and flow-finalization paths.

These paths were identified from upstream documentation and repository organization; GitHub Gold did not independently validate every API contract in this run.

### ndpiReader

The repository builds an example traffic reader that exercises the library against packet captures and live capture configurations.

Current CI explicitly builds the example directory and runs `ndpiReader -H`, making it a useful reference application for integrating libnDPI.

### Regression PCAP framework

The documented primary regression path is:

- `./tests/do.sh` for PCAP-driven regression output;
- `./tests/do-unit.sh` for unit tests;
- `./tests/do-dga.sh` for DGA-related tests;
- `make check` as the aggregate path.

This is important because packet classifiers are particularly susceptible to regressions when a new recognizer accidentally steals traffic from an older recognizer or when metadata handling changes.

### Python bindings

Main CI builds the C library, installs it, generates Python bindings, installs those bindings, and runs `python tests.py`.

That provides an additional integration surface for analysis tooling and experimentation without requiring every consumer to build an application directly in C.

### Fingerprinting and metadata extraction

The 6.0 release documents expanded nDPI fingerprint behavior and richer TLS/SSH metadata extraction.

Research targets include:

- client/server fingerprint generation;
- optional TCP contribution to fingerprints;
- TLS block processing;
- HASSH/SSH metadata;
- negotiated SSH parameters;
- server fingerprints;
- flow metadata selection/configuration.

These are potentially useful for passive inventory and observability, but they should not be treated as definitive identity proof.

### Anomaly/DGA-oriented helpers

The 6.0 release added new anomaly-related APIs and `ndpi_data_burstiness()`, while the repository maintains a dedicated DGA regression test path.

These components are relevant for defensive traffic analytics and feature generation. GitHub Gold did not independently evaluate the statistical quality or false-positive characteristics.

### Runtime-loadable dissectors

nDPI 6.0 added the ability to define protocol dissectors in shared libraries and load them at runtime.

This is a high-value architectural direction because it can separate protocol-extension lifecycles from the main library build. Follow-up research should inspect the plugin ABI, symbol/version compatibility, trust boundary, and failure isolation.

### USDT tracepoints

The 6.0 release documents static USDT tracing probes for runtime observability.

This could make nDPI useful as a reference for exposing low-overhead internal tracing from a native networking library.

## Working evidence

### Documented build/test path

Upstream documents normal source builds with Autoconf/Automake/Libtool and either GCC or Clang.

It documents compilation on Linux, FreeBSD, macOS, and Windows via MSYS2, MinGW-w64, or Visual Studio.

Out-of-tree builds are supported.

### Main CI

The current `build.yml` workflow contains multiple real compile-and-test jobs rather than only static checks.

Observed coverage includes:

- Python bindings on Ubuntu;
- utility-script consistency checks;
- Ubuntu 22.04, 24.04, and 26.04;
- macOS 15 and 26;
- GCC and Clang variants;
- old/new compiler coverage including GCC 4.9/GCC 15 and Clang 12/22 configurations;
- multiple optimization levels;
- extended sanity checks;
- sanitizer-enabled builds;
- PCRE2 and MaxMindDB configurations;
- library, example, and rrdtool builds;
- install-layout verification;
- PCAP regression tests;
- unit tests;
- DGA tests;
- Windows MSYS2 builds and tests;
- MinGW cross-compilation;
- tarball/package/symbol checks.

Current CI also checks that the private header is not accidentally installed while verifying public headers and static/shared library artifacts.

### Additional workflow evidence

The workflow directory inspected on 2026-09-14 contains dedicated configurations for:

- Visual Studio/MSBuild;
- RPM builds;
- BSD;
- cross-compilation;
- Docker;
- memory-sanitizer-related work;
- scheduled builds;
- CI fuzzing;
- CodeQL.

The project README also carries an OSS-Fuzz badge, giving additional evidence that parser/dissector inputs receive continuous fuzzing attention.

GitHub Gold did not independently execute any of these jobs in this run.

## Release evidence

The latest stable GitHub release inspected was **nDPI 6.0**, published **2026-08-28**.

Notable release changes include:

- revised component licensing terms;
- Slow DoS / Slowloris-related detection;
- expanded nDPI fingerprints;
- USDT tracepoints;
- runtime-loadable shared-library dissectors;
- Meshtastic recognition;
- JSON and MsgPack recognition;
- GitHub service sub-classification;
- libp2p detection;
- Yggdrasil and Nebula detection;
- additional Proton service classification;
- Discord audio/video call recognition;
- new content categories;
- burstiness/anomaly-oriented APIs;
- richer TLS/SSH metadata;
- build-system and fuzzing improvements.

The release is source-oriented on GitHub; the inspected release object had no binary assets attached.

## Current maintenance

Maintenance was active on the inspection date itself.

Recent commits observed include:

- 2026-09-14: dynamic `host_server_name` handling and JA5 implementation;
- 2026-09-12: TLS ephemeral-extension updates;
- 2026-09-11: fix for IPv6 prefix-tree matching plus a new unit test;
- 2026-09-10: CDN category corrections;
- 2026-09-10: DuckDuckGo and Peacock host-based protocols;
- 2026-09-10: CharacterAI protocol support;
- 2026-09-10: USDT compilation fix;
- 2026-09-08: additional flow-freeing APIs.

This is strong evidence of ongoing protocol, correctness, API, and observability maintenance rather than repository inactivity.

## Platforms and requirements

Documented build environments include:

- Linux;
- FreeBSD;
- macOS;
- Windows/MSYS2;
- Windows/MinGW-w64;
- Visual Studio.

Typical dependencies include Autoconf, Automake, Libtool, pkg-config, gettext, flex, bison, libpcap, json-c, and optional/supporting packages such as PCRE2, MaxMindDB, rrdtool, and NUMA libraries depending on the configuration.

Windows packet capture requires Npcap in WinPcap compatibility mode according to upstream documentation.

## Licensing

### Core

The root `COPYING` is LGPL version 3 and the README identifies nDPI as an LGPLv3 library.

### Dual-licensed ntop components

`README.license.md` documents an additional dual-license model for certain ntop-created components.

Upstream states:

- not-for-profit use may use those additional components without purchasing a commercial license;
- for-profit use may use only the LGPLv3 core, or obtain a commercial license for the additional dual-licensed components.

This distinction materially affects reuse.

Before embedding specific dissectors/components into another commercial project, inspect the exact source/file/component licensing and current upstream licensing documentation instead of assuming that the entire tree is uniformly LGPLv3.

No nDPI source code was copied into GitHub Gold during this run.

## Security, privacy, and ethical constraints

Deep-packet inspection is dual-use. GitHub Gold catalogs nDPI for authorized monitoring, interoperability, observability, research, troubleshooting, and defensive-security purposes.

Users should have authorization to capture and inspect the traffic involved and should consider privacy, data-retention, and regulatory requirements.

Classification and fingerprint output should be treated as evidence/signals, not infallible ground truth.

## Caveats and limitations

- Encrypted traffic limits directly observable application content.
- Protocol classification is heuristic/stateful in many cases and can produce false positives or false negatives.
- Hostname/category lists can become stale quickly.
- Fingerprints are useful features, not cryptographic identity.
- Traffic behavior varies across application versions, CDNs, VPNs, proxies, QUIC, relays, and regional deployments.
- Some additional components are not available under the same simple licensing terms as the core LGPLv3 library.
- Broad upstream CI is evidence of engineering quality, not proof that every commit is defect-free.
- GitHub Gold did not benchmark throughput or memory consumption.

## Verification performed by GitHub Gold

This run inspected:

- repository metadata and active `dev` branch;
- root README;
- root LGPLv3 license text;
- `README.license.md` component-licensing policy;
- main GitHub Actions build workflow;
- workflow inventory;
- latest stable GitHub release metadata and release notes;
- recent commit metadata;
- existing GitHub Gold default-branch search and active PR changed-file list to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- compile nDPI;
- run its PCAP regression suite;
- run unit or DGA tests;
- execute OSS-Fuzz cases;
- capture live network traffic;
- benchmark classification throughput;
- measure memory use;
- validate every protocol detector;
- test Windows/BSD/macOS builds;
- test Python bindings;
- load a runtime dissector plugin;
- audit the library for vulnerabilities;
- validate fingerprint uniqueness or stability;
- quantify false-positive/false-negative rates;
- independently verify protocol/category data feeds.

Claims above therefore distinguish upstream working evidence from work directly performed by GitHub Gold.

## Related ecosystem and recursive leads

Strong follow-up targets include:

- `aouinizied/nfstream` for flow-based analytics built around nDPI;
- `utoni/nDPId` for daemonized nDPI integration;
- `ntop/ntopng` as a major real-world consumer;
- `PF_RING` / nBPF integration;
- runtime dissector plugin ABI and security;
- protocol-regression PCAP corpus organization;
- OSS-Fuzz harnesses and historical parser bugs;
- DGA feature extraction and evaluation;
- TLS/SSH/nDPI fingerprint semantics;
- JA4/JA5-style fingerprint comparisons;
- Meshtastic, libp2p, Nebula, and Yggdrasil dissector implementations;
- QUIC/TLS classification under encrypted metadata constraints;
- performance tradeoffs between full metadata extraction and minimal classification.

## Gold rationale

**Utility — 5/5:** immediately useful as an embeddable traffic-classification engine for authorized observability and security systems.

**Working Evidence — 5/5:** extensive PCAP/unit/DGA testing, multi-platform builds, sanitizers, fuzzing, CodeQL, bindings tests, package checks, and active releases.

**Reusability — 4/5:** strong C library/API and plugin/dissector architecture, reduced from 5 because component-level licensing requires careful review.

**Novelty — 4/5:** deep protocol/fingerprint corpus and mature classification machinery, though DPI itself is an established technical category.

**Documentation — 4/5:** strong build/contribution/protocol documentation and release notes, but the breadth and evolving licensing/component model requires careful navigation.

**Maintenance — 5/5:** active commits on the inspection date, a stable release less than three weeks earlier, and continuous protocol/correctness maintenance.

**Total: 27/30 — provisional A tier.**
