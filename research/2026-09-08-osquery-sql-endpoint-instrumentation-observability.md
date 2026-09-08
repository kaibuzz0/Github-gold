# osquery: SQL endpoint instrumentation and observability

- **Repository:** https://github.com/osquery/osquery
- **Organization:** osquery
- **Category:** Defensive security / endpoint observability / operating-system instrumentation
- **Evidence:** VERIFIED
- **Provisional Gold score:** **29 / 30 — S tier**
- **License:** **Apache-2.0 OR GPL-2.0-only** (dual-licensed root project; exact-file/dependency review still applies)
- **Primary languages:** C++ with CMake, Python/build tooling, platform-specific support code
- **Platforms:** Linux, macOS, Windows; current CI includes x86_64 and ARM64 paths
- **Discovery source:** GitHub-first independent research; no video-derived technical claims used in this pass

## Executive finding

`osquery/osquery` turns operating-system state into relational tables that can be queried with SQL. Instead of forcing every monitoring or incident-response tool to implement separate APIs for processes, sockets, users, packages, browser state, hashes, kernel/system information and other host data, osquery presents those concepts through a common query model.

The repository clears the GitHub Gold quality bar because the useful artifact is not merely the `osqueryi` command-line shell. The codebase contains a reusable table/plugin/extension architecture, scheduled daemon execution, event collection, filesystem and hashing components, distributed-query support, multiple platform-specific table implementations, packaging/build tooling, and a substantial automated test/build matrix.

The project is particularly useful for defensive inventory, incident response, compliance-oriented host inspection, endpoint telemetry, fleet diagnostics, and custom tooling that wants a stable SQL-shaped abstraction over operating-system state.

## Why it matters

The central engineering idea is unusually reusable: **represent heterogeneous operating-system facts as typed virtual SQL tables**.

Examples documented upstream include querying:

- users;
- running processes;
- processes whose executable is no longer present on disk;
- listening ports joined to process identity;
- macOS LaunchDaemons;
- ARP-cache anomalies.

Queries can be run interactively through `osqueryi`, scheduled continuously through `osqueryd`, or invoked from custom software through the project's APIs/extensions.

This turns a large collection of platform-specific probes into one composable relational interface. SQL joins are especially valuable because they let a user correlate data that would otherwise require custom glue code—for example, network-listener state with process metadata.

## Reusable components and architecture

### 1. Virtual-table / table-spec system

The primary reusable concept is osquery's table abstraction. Tables map operating-system or application state into schemas that can be queried with SQLite-compatible SQL semantics.

Useful research surfaces include:

- `specs/` — table schema/specification definitions;
- `osquery/tables/` — platform and application table implementations;
- table code-generation tooling;
- constraint handling, so implementations can avoid expensive full scans when a query supplies useful predicates.

This architecture is valuable beyond endpoint security: it is a general pattern for turning irregular host APIs and files into a consistent queryable model.

### 2. Plugin and extension architecture

The upstream README states that SQL tables are implemented through a plugin and extensions API. The source tree includes dedicated `osquery/extensions/` infrastructure plus plugin-oriented subsystems for configuration, logging, distributed queries and related services.

That makes osquery useful not only as a finished endpoint agent but also as an embeddable/extensible instrumentation framework.

Potential component-level research targets:

- extension transport and registration;
- table-plugin lifecycle;
- configuration plugins;
- logger plugins;
- distributed-query interfaces;
- watchdog/worker isolation.

### 3. Interactive and scheduled execution

Two operational surfaces matter:

- **`osqueryi`** — ad-hoc interactive SQL inspection;
- **`osqueryd`** — daemonized scheduled collection/monitoring.

The daemon model is useful for fleet-style telemetry, while the interactive shell is useful for diagnostics and incident response without requiring a full external management platform.

### 4. Evented collection

The source tree contains `osquery/events/` and platform/event-specific functionality. Event tables complement snapshot-style queries by collecting changes over time.

A recent maintenance fix is especially instructive: upstream changed file-event hashing so FIFOs are not read while hashing, because reading a FIFO can consume data intended for another process. That demonstrates active attention to the side effects an observability agent can accidentally cause.

### 5. Filesystem and hashing utilities

Dedicated `osquery/filesystem/` and `osquery/hashing/` subsystems support file-oriented inventory and inspection. These pieces are useful for defensive file-integrity, inventory and incident-response workflows, but they also require careful handling of special files, mount boundaries, permissions and performance.

### 6. Distributed query support

The source tree contains `osquery/distributed/`, allowing remote/fleet-management systems to submit work to enrolled endpoints through osquery's distributed-query interfaces.

This is a useful abstraction boundary: GitHub Gold should distinguish the open-source endpoint engine from third-party fleet managers, which have their own licenses, architectures and trust models.

### 7. Cross-platform package and application inventory

The project contains many system/application inventory tables. Recent upstream work added a `pacman_packages` table for Arch-family systems and included parser tests plus comparison against package-manager output in the contributor's validation notes.

This is a good example of osquery's reuse pattern: one relational query interface can normalize software inventory across different operating-system/package ecosystems.

## Working evidence

### Automated tests

Upstream build documentation explicitly supports `OSQUERY_BUILD_TESTS=ON` and uses **CTest** as the test runner. The repository contains many GoogleTest/CTest targets, including platform-specific tests and subsystem tests.

The current source tree includes test registration and dedicated test implementations for low-level Linux `/proc` handling, system tables, IPC conversions and many other components.

This is materially stronger evidence than a project that only compiles artifacts.

### Current CI matrix

The inspected `.github/workflows/hosted_runners.yml` states that it covers Windows, macOS and Linux builds across x86_64 and ARM64.

Notable CI behavior includes:

- daily scheduled runs against the default branch;
- push and pull-request validation;
- copyright/header checks;
- formatting validation;
- third-party-library manifest validation;
- generated website/schema JSON checks;
- cppcheck source analysis;
- CMake configuration with tests enabled;
- Linux Release, RelWithDebInfo and Debug build variants;
- x86_64 and ARM64 Linux runner paths;
- packaging repository pinned to a specific commit;
- build artifact generation.

The workflow is large and should not be treated as proof that every table behaves correctly on every operating-system release, but it provides substantial recurring integration evidence.

### Supply-chain note on CI

The inspected workflow currently uses mutable major-version GitHub Action references such as:

- `actions/checkout@v7`;
- `actions/cache/restore@v6`;
- `actions/cache/save@v6`;
- `actions/upload-artifact@v7`.

Those are not immutable commit-SHA pins.

The workflow also downloads the osquery toolchain with `wget` and extracts it. A separate packaging repository is checked out to a fixed commit, which is a positive reproducibility signal, but download-integrity and workflow dependency pinning remain useful supply-chain review areas.

## Release evidence

The latest stable GitHub release inspected is:

- **5.23.1**
- **Published:** 2026-06-24
- **Stable / not prerelease**

The release contains platform packages/artifacts including Linux RPM/tarball builds, Windows MSI/ZIP builds and a macOS PKG.

The GitHub API exposes SHA-256 digest metadata for inspected release assets. Examples include Linux x86_64/aarch64 packages, Windows x86_64/ARM64 archives, MSI and macOS PKG assets.

The release itself is **not marked immutable**, so GitHub-provided digest metadata is useful evidence but should not be interpreted as equivalent to an immutable release policy or an independently verified signature chain.

## Maintenance evidence

Repository activity remained current into late August 2026.

Recent inspected commits include:

- **2026-08-25:** moved GitHub Actions to newer Node 24-compatible major versions;
- **2026-08-19:** fixed an off-by-one bounds check in the `platform_info` BIOS/SMBIOS parser; the contributor documented an ASan reproduction of the heap-buffer-overflow condition;
- **2026-08-13:** fixed sudoers parsing for escaped whitespace and added regression tests;
- **2026-08-13:** prevented file-event hashing from consuming FIFO contents;
- **2026-08-13:** added an Arch/pacman package-inventory table with parser/integration validation;
- **2026-08-13:** reduced unnecessary OpenSSL build work;
- **2026-08-13:** added a Chrome-family default-search-engine table;
- **2026-08-07:** increased the accepted configuration-size limit from 1 MiB to 4 MiB.

The BIOS parser fix is particularly relevant for Gold scoring because it shows maintenance against memory-safety defects in a parser that consumes firmware-controlled data.

## Security and operational boundaries

osquery is defensive instrumentation, but it operates close to sensitive host state. Important boundaries include:

- many tables inspect privileged or security-sensitive system information;
- scheduled queries can create CPU, disk or I/O load if poorly designed;
- filesystem/event collection can have side effects if special files are handled incorrectly, as demonstrated by the FIFO fix;
- parsers ingest data from firmware, operating-system files, application databases/configuration files and other potentially malformed sources;
- extensions/plugins and distributed-query/fleet integrations expand the trust boundary;
- fleet managers listed by upstream are separate projects and are explicitly not endorsed or tested by the osquery project;
- endpoint telemetry can contain private or sensitive information and needs deliberate retention/access policy;
- osquery is an observability/query engine, not by itself an EDR decision system or proof that a host is uncompromised.

## License

The repository root `LICENSE` states that contributions are licensed under both:

- `LICENSE-Apache-2.0`; and
- `LICENSE-GPL-2.0`.

Users may choose one of the provided licenses.

The root SPDX expression is:

`Apache-2.0 OR GPL-2.0-only`

Before extracting individual files/components, exact-file SPDX notices and bundled third-party library licenses must still be checked. GitHub Gold copied **no upstream source code** in this pass.

## Gold scoring

| Dimension | Score | Rationale |
| --- | ---: | --- |
| Utility | 5/5 | Broad endpoint inventory, diagnostics, monitoring and incident-response use across major desktop/server OSes. |
| Working Evidence | 5/5 | CTest/GoogleTest coverage, static analysis, large multi-platform/multi-architecture CI and published packages. |
| Reusability | 5/5 | SQL virtual-table model, plugins/extensions, eventing, distributed queries and many separable subsystems. |
| Novelty | 4/5 | Mature concept rather than a new research idea, but the OS-as-relational-database abstraction remains unusually composable. |
| Documentation | 5/5 | README, versioned docs, schema site, build/test docs, release process and extensive source organization. |
| Maintenance | 5/5 | Current parser hardening, new inventory tables, CI upgrades and stable 2026 release line. |
| **Total** | **29/30** | **Provisional S tier** |

## Verification performed in this pass

Inspected directly from upstream GitHub:

- repository metadata and activity dates;
- README and stated platform/query model;
- root dual-license declaration;
- source-tree subsystem organization;
- current workflow inventory;
- primary hosted-runner CI configuration;
- test/CTest evidence in repository documentation/source search;
- latest stable GitHub release metadata and selected artifact SHA-256 digest fields;
- recent commit history and maintenance rationale.

## Verification NOT performed

GitHub Gold did **not**:

- clone or build osquery;
- run CTest/GoogleTest targets;
- install `osqueryi` or `osqueryd`;
- execute SQL queries against a live host;
- enroll an endpoint into a fleet manager;
- test distributed queries or extensions;
- validate package signatures;
- independently hash release artifacts;
- reproduce the SMBIOS ASan issue/fix;
- reproduce sudoers/package/browser table behavior;
- benchmark CPU/I/O impact;
- fuzz firmware, config, database or application parsers;
- conduct an endpoint-security/privacy audit.

Statements about those areas are therefore limited to upstream evidence, not independent execution.

## Related ecosystem leads

### FleetDM Fleet

https://github.com/fleetdm/fleet

A major osquery fleet-management/control-plane ecosystem project. Upstream osquery lists Fleet but explicitly says listed fleet managers are not endorsed, recommended or tested by osquery. Fleet requires an independent license/architecture/security review before catalog promotion.

### osctrl

https://github.com/jmpsec/osctrl

Open-source fleet-management lead for distributed osquery management. Candidate for later independent inspection.

### Zentral

https://github.com/zentralopensource/zentral

Another fleet/inventory orchestration lead requiring separate verification.

## Strongest next research targets

1. Trace the table-generation path from `specs/` through generated code to a platform implementation and SQL query execution.
2. Inspect extension registration/transport and identify the exact trust boundary for third-party extension processes.
3. Inspect event publisher/subscriber buffering, persistence and backpressure semantics.
4. Review the watchdog/worker isolation architecture and failure/restart behavior.
5. Review distributed-query authentication, replay/idempotency and result-delivery assumptions.
6. Inspect firmware/system/application parsers for fuzzing coverage and malformed-input handling.
7. Map file-event collection across inotify/FSEvents/Windows event mechanisms and identify semantic differences.
8. Independently score Fleet or osctrl rather than treating fleet management as part of osquery itself.
9. Review release signing/package-repository verification in addition to GitHub asset digests.
10. Evaluate whether the table-spec/codegen layer deserves a component-level GitHub Gold entry of its own.
