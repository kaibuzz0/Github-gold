# ACMEz — RFC 8555 ACME client protocol library for Go

- **Repository:** https://github.com/mholt/acmez
- **Author / Org:** Matthew Holt / mholt
- **Category:** networking / TLS / PKI / ACME / certificate issuance / Go library / protocol implementation
- **Evidence:** VERIFIED
- **Provisional Gold score:** **27 / 30**
- **Provisional tier:** **S**
- **Discovery:** Recursive follow-up from the CertMagic/Caddy ecosystem; GitHub-first. No YouTube-derived technical claim used.
- **License:** Apache-2.0 at repository root, with a separate `THIRD-PARTY` notice for modified Go crypto ACME/JWS-derived material.

## Executive assessment

ACMEz is a focused Go implementation of the Automated Certificate Management Environment protocol. It deliberately separates certificate **issuance** from certificate **lifecycle management**: ACMEz performs ACME account/order/challenge/finalization/certificate operations, while CertMagic layers long-running renewal, storage, clustering, and deployment policy above it.

This separation makes ACMEz valuable to GitHub Gold both as a reusable library and as a compact reference implementation of RFC 8555-era certificate issuance flows. The project exposes a high-level `acmez` package for the complete order flow and a lower-level `acme` package for direct protocol operations.

The repository has concrete working evidence in source, unit tests, and an integration-style test that embeds Let's Encrypt's Pebble ACME test CA and exercises a real HTTP-01 issuance/replacement path inside Go tests. It also has current 2026 releases and maintenance. However, the repository currently does **not** contain a GitHub Actions workflow, so its Working Evidence score is intentionally lower than projects in this catalog with continuously visible CI matrices.

GitHub Gold did not execute the tests or contact a live ACME CA. VERIFIED here means repository-native implementation, tests, releases, and maintenance evidence were inspected.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | ACME certificate issuance is broadly useful infrastructure for automated TLS and PKI systems. |
| Working Evidence | 4/5 | Extensive tests include an embedded Pebble ACME integration path and current release history, but no repository-local GitHub Actions workflow was present during inspection and GitHub Gold did not run the suite. |
| Reusability | 5/5 | Standalone Go module with both high- and low-level APIs, pluggable challenge solvers, context cancellation, structured errors, and focused protocol scope. |
| Novelty | 4/5 | ACME clients exist elsewhere, but the compact porcelain/plumbing split, challenge plasticity, ARI support, and CertMagic integration make this implementation technically distinctive. |
| Documentation | 5/5 | README clearly documents scope, APIs, protocol responsibilities, challenge model, extensions, examples, and the CertMagic boundary. |
| Maintenance | 4/5 | Current 2026 releases and an August 2026 correctness fix show active maintenance, though activity is less frequent than the most actively changing S-tier projects in this batch. |

**Total: 27 / 30 — provisional S tier.**

## What it does

The upstream README describes ACMEz as a pure-Go implementation of RFC 8555 with a high-level certificate-obtainment API and a lower-level ACME protocol package.

The two principal packages are:

- **`acmez`** — high-level orchestration of the ACME order flow, challenge selection/solving, CSR validation, finalization, and certificate retrieval;
- **`acme`** — lower-level protocol operations for advanced or specialized users.

The project explicitly states that it **gets** certificates but does not manage their lifetime. Long-running applications that need renewal and certificate management are directed to CertMagic.

Documented capabilities include:

- RFC 8555 ACME order flow;
- multiple ACME certificate authorities rather than a single hard-coded CA;
- External Account Binding;
- structured RFC 7807-style ACME problem errors;
- retries for transient network/server failures;
- randomized challenge selection and fallback to alternate challenges;
- context cancellation;
- account key rollover;
- alternate certificate chains;
- large SAN-list handling;
- TLS-ALPN-01 helpers;
- email-reply-00 helpers;
- device-attestation challenge helpers;
- DNS account-label challenge helpers;
- ACME Renewal Information (ARI / RFC 9773) support;
- ACME profile support;
- current draft support including `dns-persist-01`.

## Reusable components and architecture

### High-level ACME order orchestration

`client.go` implements the high-level issuance path. `Client.ObtainCertificate()` validates input state, creates an ACME order, solves authorizations, obtains a CSR, verifies the CSR identifiers against the order, finalizes the order, and downloads the available certificate chain or chains.

This is a useful reference because the high-level flow remains visibly mapped to ACME protocol stages instead of hiding all issuance behavior behind a large server framework.

### Porcelain versus plumbing split

The README describes the architecture using Git terminology:

- `acmez` is the **porcelain** convenience layer;
- `acme` is the **plumbing** layer.

That split is useful for projects that want the normal issuance flow but still need the option to drop down into direct protocol operations for specialized account, order, authorization, challenge, or certificate behavior.

### Pluggable challenge solvers

The high-level client contains a `ChallengeSolvers` map keyed by challenge type. The library provides protocol/helper support but deliberately does not hard-code environmental challenge deployment.

That means an application can supply implementations appropriate to its environment, such as:

- HTTP-01 token serving;
- DNS-01 through a DNS API integration;
- TLS-ALPN-01 certificate presentation;
- custom or emerging challenge types.

CertMagic is one downstream example and provides a general-purpose DNS-01 solver through the libdns ecosystem.

### Challenge fallback and retry behavior

The issuance code tracks failed challenge types per identifier and can retry with alternative challenges. It also has a hard cap on issuance transaction attempts and respects context cancellation while backing off between retries.

A 2026 code path also handles ACME `alreadyReplaced` behavior by retrying an order without the `replaces` field where appropriate. That fix was linked upstream to a CertMagic issue, illustrating direct feedback between the protocol library and its production lifecycle-management consumer.

### CSR/order identifier validation

Before finalization, ACMEz checks that the identifiers in the ACME order match the identifiers represented by the CSR.

An inspected **2026-08-06** correctness commit strengthened this logic in two ways:

- URI SANs are now included in identifier creation/validation;
- order and CSR identifiers are compared as multisets instead of using a match-count approach that could mishandle duplicates or mismatched names.

This is strong maintenance evidence because the change closes a concrete client-side validation gap rather than merely refreshing dependencies.

### Emerging challenge support

An inspected **2026-03-09** commit added `dns-persist-01` support from the corresponding IETF draft, including:

- a challenge-type constant;
- issuer-domain-name handling;
- TXT-record name helper;
- TXT-record value helper;
- tests for the helper behavior.

The README separately warns that exported APIs associated with draft specifications may change or disappear without a major version bump. This is an appropriate caveat for experimental protocol surface.

### TLS-ALPN-01 helper path

The repository includes `tlsalpn01.go` and documents helpers for generating the special validation certificate required by TLS-ALPN-01.

A late-2025 fix updated generated validation certificates for IP identifiers so the Subject Alternative Name contains the required IP address form. This is another example of protocol correctness maintenance tied to a specific RFC requirement.

### ACME Renewal Information

The README documents support for ACME Renewal Information under RFC 9773. In the broader Caddy stack, ACMEz provides the protocol-level capability while CertMagic consumes renewal information as part of certificate lifecycle policy.

This boundary is architecturally useful: protocol parsing/transport remains here while long-running scheduling and certificate deployment remain in CertMagic.

## Tests and working evidence

The repository contains conventional unit tests as well as an important integration-style test path in `pebble_test.go`.

That test imports Let's Encrypt's **Pebble** ACME test server components and constructs an in-memory CA / validation authority / web front end. It then:

1. creates a local HTTP challenge solver;
2. constructs an ACME client against the embedded Pebble server;
3. creates an ACME account;
4. generates a certificate key;
5. obtains an initial certificate for `127.0.0.1`;
6. parses the returned certificate;
7. performs a replacement issuance;
8. attempts another replacement of the same prior certificate;
9. asserts that the client recovers successfully.

This is materially stronger than tests that only validate string formatting or static parsing because it exercises multiple interacting ACME layers in-process.

The module file pins `github.com/letsencrypt/pebble/v2` and `github.com/letsencrypt/challtestsrv` as test dependencies, together with cryptographic/network dependencies from `golang.org/x/*`.

### Important CI limitation

During this run, the repository's `.github` directory contained only `FUNDING.yml`; no `.github/workflows` directory was present.

Therefore GitHub Gold did **not** claim active GitHub Actions CI for ACMEz. The project has meaningful tests, but their existence does not prove they are run automatically on every change.

This distinction is the main reason Working Evidence is scored **4/5**, not 5/5.

## Runtime and development requirements

Current `go.mod` declares:

- module `github.com/mholt/acmez/v3`;
- Go **1.24.0**;
- direct requirements including `code.pfad.fr/check`, Let's Encrypt Pebble, `golang.org/x/crypto`, and `golang.org/x/net`;
- additional indirect testing/network dependencies including `go-jose`, `challtestsrv`, `miekg/dns`, `x/sync`, `x/sys`, `x/text`, and `x/tools`.

The README installation path is:

`go get github.com/mholt/acmez/v3`

Operational requirements depend on the selected challenge solver and ACME CA. The core module is not itself a DNS provider, web server, or long-running certificate manager.

## Releases

The newest stable GitHub release inspected during this run was **v3.1.6**, published **2026-02-20**.

Its release notes describe dependency updates and lint cleanup.

The immediately preceding **v3.1.5** release includes more operationally significant fixes:

- TLS-ALPN-01 certificate generation for IP identifiers;
- omission of an empty ACME account status field for strict CAs;
- retry behavior when a `replaces` field is rejected or no longer appropriate.

The project is a library, so releases contain source/tag artifacts rather than standalone executable binaries.

## Maintenance signals

The repository is unarchived and repository metadata showed a push on **2026-08-06**.

The newest inspected commit from that date fixed URI SAN handling and multiset identifier comparison in order-versus-CSR validation.

Other 2026 maintenance includes:

- `dns-persist-01` challenge support plus tests;
- dependency upgrades;
- lint/test fixes;
- `replaces` retry behavior tied to CertMagic operational feedback;
- ACME account serialization compatibility improvements.

This is active and relevant maintenance, but the cadence is lower than projects receiving a 5/5 Maintenance score in this batch.

## Licensing

Repository metadata and the root `LICENSE` identify ACMEz as **Apache-2.0**.

The repository also contains a `THIRD-PARTY` notice identifying modified material derived from Go's `crypto/acme` JWS implementation under its original permissive license terms.

This matters for source extraction: Apache-2.0 at the repository root is not a reason to discard the separate third-party notice. Required upstream notices should remain attached to any covered derived material.

No ACMEz source code, certificates, keys, challenge tokens, release archives, or test-CA artifacts were copied into GitHub Gold.

## Security and trust boundaries

### Account and certificate private keys

ACME issuance operates on cryptographic private keys. ACMEz accepts signing keys but is not a secret-management system. Applications embedding it remain responsible for key generation, storage, permissions, rotation, and process security.

### Challenge solver authority

`acmez.Solver` is intentionally pluggable. A solver may expose HTTP resources, alter DNS, or participate in a TLS handshake. The security of the overall issuance system therefore depends strongly on the solver implementation and the credentials/capabilities granted to it.

### ACME CA trust and protocol responses

The client depends on remote ACME directory/order/authorization endpoints and ultimately accepts certificates issued by external CAs. Robust retry logic improves reliability but does not remove CA, network, DNS, or time dependencies.

### Emerging draft protocol surface

The project supports several non-final or emerging ACME extensions. Upstream explicitly warns that APIs tied to drafts can change without a major-version increment. Consumers should pin versions and distinguish finalized RFC behavior from draft experiments.

### Validation versus authoritative CA checks

The August 2026 identifier-validation fix improves ACMEz's client-side safety check, but the commit itself notes that the CA remains authoritative. Local validation should be treated as defense-in-depth and error detection rather than a replacement for CA enforcement.

## Verification boundary

GitHub Gold inspected repository-native evidence but **did not**:

- build ACMEz;
- run `go test`;
- execute the Pebble integration tests;
- create an ACME account against a live CA;
- obtain or renew a public certificate;
- execute HTTP-01, DNS-01, TLS-ALPN-01, email-reply-00, device-attestation, dns-account-01, or dns-persist-01 challenges;
- test External Account Binding;
- test account key rollover;
- exercise alternate certificate chains;
- validate ARI against a production CA;
- test large SAN-list performance;
- fuzz JWS, CSR, authorization, challenge, certificate, or HTTP response parsing;
- independently verify release tags;
- independently audit cryptographic correctness;
- verify that upstream maintainers run the test suite outside GitHub Actions.

Therefore **VERIFIED** means concrete implementation, integration-test structure, release history, source organization, and current maintenance were inspected. It does not mean GitHub Gold independently certified ACME protocol correctness or production PKI safety.

## Why it matters to GitHub Gold

ACMEz is useful at several levels:

1. **Reusable protocol library:** Go projects can perform direct ACME issuance without embedding a complete web server.
2. **Architecture reference:** cleanly separates ACME protocol mechanics from long-running certificate lifecycle management.
3. **Protocol study:** exposes account/order/authorization/challenge/finalization/certificate flows in a relatively compact codebase.
4. **Testing pattern:** embeds Pebble to exercise real ACME interactions in-process.
5. **Extensibility:** challenge solvers are environment-specific plugins rather than hard-coded provider logic.
6. **Standards evolution:** implements finalized RFCs while also exposing carefully caveated emerging challenge/profile work.
7. **Ecosystem value:** forms the protocol layer beneath CertMagic and therefore indirectly beneath Caddy's automatic HTTPS stack.

## Related projects / recursive leads

- **caddyserver/certmagic** — certificate lifecycle, renewal, storage, clustering, issuer fallback, and DNS-provider orchestration layered above ACMEz.
- **caddyserver/caddy** — major downstream production consumer through CertMagic.
- **letsencrypt/pebble** — ACME test CA used directly by ACMEz tests; strong candidate for deeper protocol-testing research.
- **libdns ecosystem** — DNS-provider abstraction used by CertMagic's DNS-01 solver rather than ACMEz core.
- **go-acme/lego** — historically related Go ACME client ecosystem and useful comparison target.

## Strongest next research questions

1. Map the low-level `acme` package into account, nonce/JWS, order, authorization, challenge, finalize, certificate, ARI, and error-handling components.
2. Inspect the exact retry/backoff and `Retry-After` semantics in the lower-level HTTP client.
3. Trace how CertMagic configures ACMEz issuers, accounts, challenge solvers, ARI, and alternate chains.
4. Inspect Pebble as a reusable local ACME conformance/integration testing component.
5. Compare ACMEz's scope and dependency surface with lego and `golang.org/x/crypto/acme`.
6. Review draft-extension code separately from finalized RFC code so experimental APIs do not inherit production confidence automatically.
7. Determine whether external CI exists outside the repository; until then, retain the explicit no-visible-GitHub-Actions caveat.
