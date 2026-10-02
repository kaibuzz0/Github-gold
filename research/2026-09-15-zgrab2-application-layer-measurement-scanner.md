# ZGrab2 — modular application-layer measurement scanner

- **Repository:** https://github.com/zmap/zgrab2
- **Author / organization:** ZMap Project (`zmap`)
- **Category:** network measurement / application-layer protocol analysis / defensive inventory
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **Languages:** Go; Python is used for output schemas/integration validation
- **License:** Apache-2.0 for original ZGrab work plus ISC-covered Google-derived/forked code; inspect per-file notices when extracting components.
- **Discovery:** recursive follow-up from the existing `zmap/zmap` dossier.

## What it is

ZGrab2 is the stateful application-layer half of the ZMap measurement ecosystem. ZMap discovers responsive L4 endpoints; ZGrab2 performs protocol handshakes and records structured handshake transcripts for offline analysis. The project explicitly supersedes the original `zmap/zgrab`.

The framework accepts targets through stdin/files, supports IP/domain/tag/port metadata, and can run individual or multiple protocol modules. Domain-aware targets let a scanner connect to a selected IP while still using the hostname in protocol contexts such as HTTP Host and TLS SNI.

Upstream's stated ethical boundary is important: scanners are intended to collect information available to a normal unauthenticated client, application handshakes are aborted before authentication, and contributions aimed at exploitation or credential brute forcing are rejected.

## Why it matters

ZGrab2 is useful as both a complete measurement tool and a source of reusable protocol-engineering patterns:

- modular stateful handshake scanners;
- structured protocol transcripts suitable for later analysis;
- shared dialer/session/timeout infrastructure;
- schema-backed output validation;
- protocol-specific parsers and serializers;
- multi-module routing through target tags;
- integration testing against real services in containers;
- fuzzing coverage for parser-heavy modules and libraries;
- a natural second stage after stateless discovery with ZMap.

This makes it relevant to authorized asset inventory, protocol interoperability testing, Internet-measurement research, defensive exposure studies, service fingerprinting, and parser engineering.

## Protocol surface

The README documents modules including AMQP, BACnet, Banner, DNP3, Fox, FTP, HTTP, IMAP, IPP, JARM, ManageSieve, Memcached, Modbus, MongoDB, MQTT, MSSQL, MySQL, NTP, Oracle, POP3, PostgreSQL, PPTP, Redis, Siemens, SMB, SMTP, SOCKS5, SSH, Telnet, and TLS.

Development has continued beyond that table. A September 6, 2026 commit added four OT/ICS and Windows-oriented modules: **GE SRTP, MSMQ, MSRPC, and SNMP**. This is a useful reminder to inspect the module tree rather than relying only on the README list.

## Particularly valuable components

### Scanner/module framework

New protocol modules are expected to implement a scanner around common framework interfaces and base flags. The current contribution workflow includes a `make scaffold-new-module PROTO=...` target that creates scanner and registration boilerplate.

This is one of the strongest reusable ideas in the repository: protocol-specific logic is separated from shared target handling, dialers, timeouts, CLI plumbing, output records, and test/schema expectations.

### Dialer and connection abstractions

Modules describe their expected transport behavior through shared dialer configuration. This is worth deeper study because it centralizes connection policy instead of forcing every scanner to independently reimplement TCP/UDP/TLS setup and timeout handling.

A September 1, 2026 fix to `ReadAvailable` is concrete evidence that these shared primitives materially affect many modules: the prior first-read timeout behavior could make DNP3, Fox and RDP fail frequently on non-local connections and potentially affected Memcached, JARM and Telnet as well. Shared infrastructure therefore has high reuse value but also a broad failure radius.

### Structured schemas

New modules require corresponding schemas under `zgrab2_schemas`. Integration output is validated against schemas, giving the project a useful pattern for keeping scanner output machine-consumable and catching accidental shape changes.

### Integration-test architecture

The contribution requirements state that a new module must cleanly compile, pass lint/tests, and include an integration test against a real service whose output is validated against a schema. Upstream recommends containerized real-world services where possible.

Current GitHub Actions independently performs a normal Go build/unit-test job and an integration-test job. The latter installs Python tooling including `zschema`, then runs `make integration-test`.

### Fuzzing architecture

The current fuzz workflow runs weekly and on pull requests touching `modules/**` or `lib/**`. It:

1. checks expected fuzz coverage;
2. discovers packages containing `*_fuzz_test.go` dynamically;
3. builds a matrix from those packages;
4. discovers `Fuzz*` functions through `go test -list`;
5. runs each fuzz target for a bounded interval.

That dynamic discovery design is a useful reusable CI pattern for a growing parser collection.

## Working evidence inspected

Evidence inspected during this run includes:

- current upstream README and documented module/build architecture;
- source-build path requiring Go 1.23+;
- official Docker usage documented by upstream;
- GitHub Actions build/unit-test workflow;
- GitHub Actions real-service integration-test workflow;
- scheduled/PR Go fuzz workflow with dynamically discovered fuzz targets;
- recent upstream commits through September 6, 2026;
- the first stable **v1.0.0** release, published December 4, 2025;
- root licensing text describing Apache-2.0 plus ISC-covered Google-derived code.

The v1.0.0 release is meaningful evidence rather than a cosmetic tag: upstream said the module/framework API had stabilized enough for its first major release. That release included HTTP/2 and h2c support, per-IP/DNS rate limiting, TLS failure-detail retention, ManageSieve and Memcached work, scanner-interface documentation, and multiple parser/bounds-check fixes.

Recent 2026 maintenance remains active. Besides dependency maintenance, September changes include the new GE SRTP/MSMQ/MSRPC/SNMP modules and the shared read-timeout correction described above.

## Requirements / platforms

- Go **1.23 or later** per current README.
- Source build uses `make`.
- An official GHCR Docker image is documented for containerized execution.
- Integration testing relies on Python tooling plus service containers/test infrastructure.
- Individual protocol modules may have their own target/service assumptions.

## Licensing / reuse

The root license explains that original ZGrab work is Apache-2.0, while forked Go standard-library packages and BoringSSL test-runner-derived material carry Google copyright and ISC terms. Do not assume every file has identical provenance merely because the repository is broadly permissive.

**No upstream source was copied into GitHub Gold.** For future extraction, preserve per-file copyright/license notices and prefer linking to exact upstream components unless there is a clear reason to vendor/adapt code.

## Caveats and risk boundaries

- ZGrab2 is a network scanner. Cataloging it here is for authorized inventory, defensive security, interoperability and legitimate research.
- The tool can operate at measurement scale, so target authorization, rate control, network policy, and research ethics remain operator responsibilities.
- Upstream deliberately avoids authentication attempts and exploit/brute-force contributions; downstream modifications should preserve that boundary.
- Parser correctness varies by protocol and evolves over time; a successful integration test is not proof that a parser is complete or vulnerability-free.
- Shared transport helpers have broad impact across modules, as demonstrated by the September 2026 `ReadAvailable` fix.
- The README's protocol table can lag the source tree; use the current module registry/tree as the authoritative capability inventory.

## Verification boundary

GitHub Gold inspected upstream documentation, workflows, release metadata, license text, and recent commit evidence. **We did not compile ZGrab2, run `make test`, execute integration tests, run fuzzers, contact any network service, perform Internet scanning, validate protocol transcripts, benchmark throughput, or independently reproduce upstream bug fixes.**

Accordingly, VERIFIED here means there is strong repository-native evidence of a functioning and actively tested project; it does not mean GitHub Gold independently executed the scanner.

## Related projects

- `zmap/zmap` — stateless L4 discovery stage already researched by GitHub Gold.
- `zmap/zgrab` — deprecated predecessor; superseded by ZGrab2.
- `zmap/zcrypto` — cryptographic/TLS-related dependency worth separate inspection.
- ZMap Project measurement documentation and getting-started pipeline.

## Follow-up research

1. Inventory the live module registry and reconcile it against the README table.
2. Deep-inspect the shared dialer/connection/timeout layer and map which modules depend on each helper.
3. Inspect `zgrab2_schemas` as a reusable protocol-output contract system.
4. Audit integration-test services for deterministic and reproducible handshake fixtures.
5. Map fuzz targets to protocol parsers and identify parser-heavy modules lacking fuzz coverage.
6. Inspect `zmap/zcrypto` and determine how much of ZGrab2's TLS/SSH behavior depends on forked crypto/network stacks.
7. Study per-IP/DNS rate limiting and multi-module scheduling as defensive measurement-safety mechanisms.
8. Compare ZGrab2's application-layer transcript model with Nmap service probes, Zeek analyzers, and purpose-built protocol clients without reducing the comparison to raw scan speed.
