# ZMap — stateless high-speed network measurement scanner

- **Repository:** https://github.com/zmap/zmap
- **Organization:** ZMap Project
- **Category:** Network measurement / defensive security / Internet research / packet tooling
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **27/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 4/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 4/5
- **Primary language:** C
- **License:** Apache-2.0
- **Discovery source:** GitHub-first recursive research from the network-observability/testing cluster
- **Inspection date:** 2026-09-15

## Executive finding

ZMap is a mature stateless single-packet network scanner designed for large-scale Internet measurement. It is valuable to GitHub Gold primarily as a research and defensive measurement engine, as a reusable implementation of high-rate packet generation/response validation, and as the discovery half of the ZMap/ZGrab2 measurement pipeline.

Upstream documents Linux, macOS, and BSD support and probe modules for TCP SYN, ICMP, DNS, UPnP, BACnet, and configurable UDP probes. For stateful application-layer handshakes, the project explicitly points to its companion ZGrab2 repository.

Because high-rate scanning is dual-use and can create operational impact, this dossier treats ZMap strictly in authorized measurement, inventory, defensive research, interoperability, and Internet-measurement contexts. Upstream itself prominently warns users about ethical scanning, conservative rates, and operator opt-out mechanisms.

## Why it matters

ZMap is not merely another sequential port scanner. Its architecture is built around stateless single-packet measurement at very large target scales. That makes it technically interesting for:

- authorized Internet measurement;
- defensive asset and exposure research;
- protocol deployment studies;
- measurement pipelines where discovery feeds a stateful application scanner;
- packet-generation and response-validation research;
- reproducible scanning methodology;
- studying high-throughput networking paths such as netmap/PF_RING integration;
- controlled laboratory testing of rate limiting, target permutation, probe modules, and output pipelines.

The README claims Internet-wide IPv4 single-port scans can complete in under 45 minutes on a typical gigabit desktop and substantially faster with 10GbE plus accelerated packet I/O. GitHub Gold did not reproduce those performance figures, so they remain upstream claims rather than independent benchmark results.

## High-value components and patterns

### Stateless probe architecture

The most distinctive reusable idea is the separation of target generation, packet construction, transmission, response validation, and output. The repository exposes multiple protocol probe modules rather than coupling the engine to only TCP SYN.

Useful research targets include:

- probe-module interfaces;
- TCP SYN response processing;
- ICMP and DNS probes;
- UDP probe payload definitions;
- target permutation/sharding;
- rate-control logic;
- response validation and deduplication;
- output modules and field selection;
- network-interface/gateway discovery;
- accelerated packet-I/O paths.

These are component-level research leads, not claims that GitHub Gold independently audited each implementation.

### ZMap → ZGrab2 pipeline

Upstream explicitly distinguishes ZMap's stateless discovery role from ZGrab2's stateful application-layer handshake role. This separation is a strong composability pattern: use a cheap single-packet measurement to identify likely responders, then apply more expensive protocol handshakes only to the reduced set.

Release 4.4.0 added a blank output-field option specifically intended to make multi-port output easier to pipe into ZGrab2, reinforcing that this is an intentional ecosystem architecture rather than an incidental integration.

### RTT and JA4TS observations

Release 4.4.0 added RTT measurement to the TCP SYN probe and optional JA4TS fingerprinting of SYN-ACK responses. These features make the probe layer useful for more than binary open/closed discovery and create follow-up research around passive characteristics observable from a minimal active probe.

## Working evidence

### Cross-platform compilation CI

The current CMake workflow builds the project on a broad platform matrix. Inspected jobs include:

- current Ubuntu/container build;
- Ubuntu 16.04, 18.04, 20.04, 22.04, and 24.04 compatibility containers;
- Debian;
- Arch Linux;
- Fedora;
- macOS 15;
- FreeBSD through a VM action.

The main jobs configure with development and trace logging enabled, compile the project, and run the project's manpage checker. This is concrete repository-native evidence of broad compilation coverage.

### Integration validation

A separate `integration.yml` workflow builds the repository's pytest container and executes its integration validation on pushes and pull requests to `main`.

The workflow directory also contains separate scan-coverage infrastructure, which is a strong next target for understanding how ZMap verifies large-scale target/probe behavior without relying only on successful compilation.

### Release evidence

The newest stable release inspected is **v4.4.0**, published **2026-05-29**.

Notable changes documented by upstream include:

- correction of a macOS interface-index out-of-bounds condition;
- TCP SYN RTT measurement;
- easier multi-port piping into ZGrab2;
- fixes to rate limiting when multiple probes are used;
- correction of Linux interface binding behavior;
- optional JA4TS SYN-ACK fingerprinting;
- a DNS TXT heap-corruption fix;
- a `sprintf` buffer-overflow hardening change;
- FreeBSD CI fixes.

These release notes are useful maintenance/security evidence. GitHub Gold did not independently reproduce the bugs or fixes.

### Current maintenance

Repository metadata inspected on 2026-09-15 shows the project is not archived, uses `main` as its default branch, and was pushed on 2026-08-28. The repository remains actively used and maintained, although its release cadence is not as rapid as some continuously shipped developer tools.

## Runtime and platform profile

Upstream documents operation on:

- GNU/Linux;
- macOS;
- BSD.

Normal raw-packet scanning requires elevated network privileges. High-performance deployments can involve specialized packet-I/O facilities such as netmap or PF_RING.

This is therefore not a natural Android/Termux-first candidate and should not be represented as one without separate platform validation.

## Licensing

The repository is licensed under **Apache License 2.0**. That is favorable for reuse, modification, and integration subject to the license's notice and other requirements.

No ZMap source, probe payloads, binaries, or datasets were copied into GitHub Gold during this run.

Specific third-party dependencies, example payloads, or external datasets should still receive file-level provenance review before redistribution.

## Safety / operational caveats

ZMap can generate traffic at rates capable of affecting networks and triggering abuse responses. Upstream prominently documents ethical-scanning responsibilities and recommends conservative scanning rates and opt-out handling.

GitHub Gold catalogs the project for legitimate defensive, research, interoperability, inventory, and controlled measurement use. This dossier intentionally does not provide an operational recipe for indiscriminate third-party scanning.

Additional limitations:

- raw-packet operation commonly requires elevated privileges;
- very high scan rates require careful local/network capacity engineering;
- packet loss and middleboxes can bias measurement results;
- stateless discovery does not replace stateful protocol validation;
- Internet-wide measurements require legal, ethical, and abuse-handling planning;
- performance claims are environment-dependent.

## Verification performed by GitHub Gold

This run inspected:

- repository metadata;
- current README and documented architecture/use boundaries;
- Apache-2.0 licensing declaration;
- current workflow inventory;
- cross-platform CMake workflow;
- integration-validation workflow;
- latest stable GitHub release metadata and release notes;
- current GitHub Gold default-branch catalog search to avoid an obvious duplicate;
- active GitHub Gold draft PR state before writing.

## Verification NOT performed

GitHub Gold did **not**:

- compile ZMap;
- execute its pytest/integration suite;
- send network probes;
- scan public or private networks;
- benchmark packet rates;
- validate target permutation statistically;
- exercise netmap or PF_RING;
- reproduce the release's memory-safety bugs;
- independently audit packet parsing or response validation;
- verify Internet-wide performance claims.

## Related ecosystem directions

Strong recursive leads include:

- `zmap/zgrab2` for stateful application-layer handshakes;
- ZMap scan-coverage tests;
- probe-module API and custom probe construction;
- UDP probe corpus provenance and reuse;
- JA4TS implementation and semantics;
- target permutation/sharding mathematics;
- rate-control behavior and reproducibility;
- netmap/PF_RING accelerated paths;
- ethical scanning / opt-out tooling;
- comparisons with Masscan and ProjectDiscovery Naabu for authorized measurement use.

## Gold rationale

**Utility — 5/5:** highly useful for authorized large-scale network measurement and discovery pipelines.

**Working Evidence — 5/5:** stable releases, broad cross-platform compilation CI, integration validation, and active maintenance/security fixes.

**Reusability — 4/5:** Apache-2.0 and modular probe/output architecture are strong, but raw networking privileges and specialized high-rate operation constrain embedding compared with ordinary libraries.

**Novelty — 4/5:** stateless high-speed scanning is now an established category, but ZMap remains a foundational and technically distinctive implementation.

**Documentation — 5/5:** README, wiki, best-practice guidance, architecture papers, installation documentation, and explicit companion-tool guidance are strong.

**Maintenance — 4/5:** current and actively maintained with a 2026 stable release and recent pushes; cadence is healthy but not continuous-release level.

**Provisional total: 27/30 — S tier.**

## Next research queue

1. Deep-inspect `zmap/zgrab2` as the companion stateful handshake engine.
2. Inspect ZMap's scan-coverage workflow and pytest corpus.
3. Trace target permutation/sharding and response-validation internals.
4. Inspect JA4TS SYN-ACK fingerprint implementation and limitations.
5. Compare ZMap, Masscan, and Naabu architectures strictly for authorized measurement/inventory.
6. Review UDP probe definitions and provenance before considering any reusable extraction.
7. Map rate-control and packet-I/O backends, including netmap/PF_RING.
