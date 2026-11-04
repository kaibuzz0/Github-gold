# Reticulum — cryptographic overlay network stack for heterogeneous low-bandwidth links

- **Repository:** https://github.com/markqvist/Reticulum
- **Author / Maintainer:** Mark Qvist
- **Category:** resilient networking / emergency communications / overlay networks / low-bandwidth networking / LoRa / packet radio / privacy
- **Evidence:** VERIFIED
- **Provisional Gold score:** 25 / 30
- **Provisional tier:** A
- **Primary language:** Python
- **Discovery source:** Recursive emergency/off-grid networking research following Meshtastic review
- **Research date:** 2026-09-14

## Score

| Dimension | Score | Notes |
| --- | ---: | --- |
| Utility | 5 | Builds encrypted local or wide-area networks across heterogeneous transports, including very low-bandwidth links. |
| Working evidence | 4 | Packaged releases, CI tests, deployed companion applications, included utilities, and a mature reference implementation; GitHub Gold did not execute it. |
| Reusability | 3 | Excellent API/interface architecture, but the custom Reticulum License imposes use restrictions and forbids AI/ML training-dataset use. |
| Novelty | 5 | Cryptography-native, non-IP multi-hop networking across heterogeneous carriers is technically distinctive. |
| Documentation | 4 | Extensive manual, examples and utilities; the GitHub repository is explicitly a public mirror and the implementation itself is the authoritative protocol specification. |
| Maintenance | 4 | Active September 2026 commits and recent release activity, though canonical development occurs outside this GitHub mirror. |

**Total: 25 / 30 — provisional A tier.**

## Executive finding

Reticulum is a user-space networking stack designed to build encrypted, self-configuring networks across extremely heterogeneous and potentially very low-bandwidth carriers. Upstream describes operation over LoRa, packet-radio TNCs, serial links, Wi-Fi/Ethernet, TCP/UDP, external programs over pipes, and custom interfaces.

The project is particularly unusual because it is not an application-layer mesh protocol sitting on top of IP. Reticulum defines its own cryptography-backed addressing, link establishment, routing, data transfer, request/response, and interface model, while still allowing IP to be used as one underlying carrier when useful.

For GitHub Gold, Reticulum is valuable as both a practical networking toolkit and a reference architecture for resilient, low-bandwidth, user-controlled communications.

## Critical provenance note

The upstream README explicitly states that **the GitHub repository is a public mirror and all development happens elsewhere**.

Accordingly:

- GitHub commit/release activity is useful evidence of maintenance, but GitHub should not be treated as the canonical development forge;
- issue/PR activity on this mirror may not represent the project's actual development workflow;
- future research should identify and inspect the canonical development source before making claims about review process, contribution velocity, or branch governance.

This caveat materially limits how much repository-hosting metadata should influence scoring.

## What it provides

Upstream documents the following major capabilities:

- coordination-less destination addressing and identification;
- self-configuring multi-hop routing;
- operation across heterogeneous links/topologies;
- end-to-end encryption;
- initiator anonymity design goals;
- X25519- and Ed25519-based identity/cryptographic primitives;
- optional forward secrecy;
- reliable transfer of arbitrary-size data with sequencing, compression, coordination and checksumming;
- request/response primitives;
- reliable sequential channels and buffers;
- extensible physical/interface adapters;
- interface authentication and virtual segmentation;
- user-space operation without kernel modules or custom drivers.

The README states that the Python implementation in this repository is the **reference implementation** and that the implementation plus manual form the authoritative Reticulum protocol definition.

That design choice is important for GitHub Gold: there is no separate formal RFC that can be treated as independent ground truth. Interoperability research must compare against this implementation and manual.

## Supported carriers and interfaces

Current upstream documentation describes built-in support for:

- Ethernet;
- LoRa through RNode;
- packet-radio TNCs, with or without AX.25;
- KISS-compatible hardware/software modems;
- serial devices;
- TCP;
- UDP;
- external programs via stdio/pipes;
- custom hardware via stdio/pipes.

The project states that a physical medium only needs to provide approximately half-duplex communication, an MTU of about 500 bytes, and extremely low minimum throughput to be usable in principle.

That makes Reticulum a useful architecture for mixed networks where high-speed IP links, serial devices, LoRa nodes, packet radio and custom transports must interoperate without exposing application logic to every carrier type.

## Included operational tools

The repository ships a useful set of operator/developer utilities rather than only a Python library:

- `rnsd` — long-running Reticulum daemon/service;
- `rnstatus` — interface/status inspection;
- `rnpath` — path-table lookup/management;
- `rnprobe` — destination connectivity diagnostics;
- `rncp` — file transfer;
- `rnid` — identity management plus file encryption/decryption;
- `rnsh` — interactive remote shell functionality;
- `rnx` — remote command execution/output retrieval;
- `rngit` — Git repository serving over Reticulum;
- `git-remote-rns` — Git remote helper for Reticulum transport.

These utilities are high-value research leads in their own right because they demonstrate the stack being used for diagnostics, file movement, interactive sessions, command execution and source-control transport over nontraditional links.

They should be cataloged and assessed as operational tools, not assumed safe for arbitrary exposure. Authentication, authorization and remote-command threat boundaries deserve separate review.

## Reference applications / ecosystem

Upstream directly identifies several applications built on the stack:

- `markqvist/lxmf` — delay/disruption-tolerant message transfer;
- `markqvist/lxst` — real-time audio/signals transport;
- Nomad Network — resilient/off-grid mesh communications;
- Sideband — graphical Android/Linux/macOS/Windows client with messaging, file/image/voice transfer, calls, telemetry and mapping;
- additional third-party clients such as MeshChatX.

This ecosystem is useful evidence that Reticulum is not purely theoretical. However, each companion project's own maintenance, licensing and security posture must be evaluated separately.

## Working evidence inspected

### CI tests

The GitHub mirror contains a `Build Reticulum` workflow that runs on branch pushes and pull requests.

The test job:

- checks out the repository;
- configures Python 3.11;
- installs `cryptography`;
- runs `make test`.

Tagged releases additionally build both dependency-declaring and pure Python wheels through project Make targets before the release stage.

This is credible upstream working evidence, though the workflow is much smaller than the CI of very large projects and GitHub Gold did not independently execute it.

### Release packaging

The latest GitHub release returned during inspection is **RNS 1.5.2**, published **2026-08-29**.

Observed release assets include:

- Python wheel;
- source tarball;
- PDF manual;
- EPUB manual;
- companion `.rsg` signature files.

GitHub metadata exposes SHA-256 digests for these assets.

This supports a functioning packaging/release pipeline. GitHub Gold did not independently validate the signatures, hashes, wheel contents, or source reproducibility.

### Current maintenance

The mirror contains fresh September 2026 activity. Inspected commits through **2026-09-12** include release preparation, changelog/version updates and fixes improving RNode Bluetooth Low Energy reconnection reliability, including a desktop reconnection deadlock fix.

Because this GitHub repository is explicitly a mirror, those commits should be treated as mirrored maintenance evidence rather than proof that GitHub is where the changes were originally authored/reviewed.

## Cryptographic architecture — upstream claims, not independent audit

The README documents a cryptography-native design using X25519 and Ed25519 as foundational primitives and describes encrypted-token construction involving ECDH-derived ephemeral/link keys, AES-256-CBC, PKCS7 padding, HMAC-SHA256, and random IVs.

It also documents forward-secrecy capabilities and delivery acknowledgements intended to be unforgeable.

These are **upstream architectural claims**. GitHub Gold did not perform a cryptographic review, validate nonce/key lifecycle behavior, inspect side-channel resistance, reproduce protocol proofs, or evaluate whether implementation details fully achieve the stated anonymity/security properties.

Any security-sensitive deployment should be evaluated against the exact version, threat model, and current upstream security documentation.

## Install / runtime model

The standard Python package is installable as:

`pip install rns`

Upstream also documents `pipx install rns` and a dependency-free metadata variant named `rnspure` whose source contents are described as identical but whose package metadata does not require external dependencies.

The standard package lists two primary external dependencies:

- PyCA `cryptography`;
- `pyserial`.

The stack runs in user space and is intended to work on systems capable of running Python 3.

Hardware requirements depend entirely on the chosen carrier. IP-only use requires no specialist radio hardware; LoRa use through RNode requires compatible radio hardware; packet-radio use requires appropriate TNC/modem equipment.

## License — major caveat

The repository does **not** use a standard OSI-style permissive license such as MIT, BSD or Apache.

The custom **Reticulum License** grants broad rights to use, copy, modify, merge, publish, distribute, sublicense and sell the software, but adds two material restrictions:

1. the software may not be used in systems whose functions include the ability to purposefully harm human beings;
2. the software may not be used directly or indirectly in creating AI, machine-learning or language-model training datasets.

These restrictions mean downstream reuse must be evaluated carefully. In particular, the repository should **not** be treated as conventional permissively licensed open source merely because much of the license resembles MIT-style language.

Upstream separately states that the **Reticulum Protocol** was dedicated to the public domain in 2016. That does not automatically make this reference implementation's source code public-domain or remove the custom software-license restrictions.

No Reticulum source code was copied into GitHub Gold during this run.

## Reusability assessment

Reticulum is architecturally very reusable but legally more constrained than many GitHub Gold candidates.

High-value reusable concepts/components include:

- pluggable transport/interface abstraction;
- path discovery and multi-hop transport;
- destination/identity model;
- link/session abstraction;
- request/response primitives;
- resource transfer and sequencing;
- channel/buffer abstractions;
- route/path diagnostics;
- host daemon architecture;
- custom interface loading;
- very-low-bandwidth operation patterns.

For implementation reuse, prefer linking to upstream and studying interfaces unless the exact downstream use has been reviewed against the Reticulum License.

## Important caveats and risks

- The GitHub repository is a mirror, not the canonical development location.
- The custom license contains nonstandard use restrictions.
- The protocol specification is intentionally embodied in the reference implementation/manual rather than a separate formal spec, increasing the importance of version-specific interoperability tests.
- Security/anonymity claims require independent threat-model review before high-risk use.
- Remote-shell and remote-command utilities increase the operational attack surface when enabled.
- Radio performance depends on hardware, antenna, propagation, bandwidth, interference and regulatory constraints.
- Bridging carriers can create unexpected reachability/trust relationships if interface segmentation is configured incorrectly.
- Public routing/transport deployment can expose nodes to malformed or resource-exhaustion traffic even when payload confidentiality is protected.

## Verification performed by GitHub Gold

Inspected:

- upstream GitHub mirror metadata;
- README and project scope;
- supported interfaces/carriers and included utilities documented upstream;
- custom Reticulum License;
- GitHub Actions workflow and `make test` execution path;
- tag/release packaging workflow;
- latest GitHub release metadata and representative asset digests;
- recent mirrored commit history through 2026-09-12;
- duplicate status against the active GitHub Gold research branch.

GitHub Gold did **not**:

- install Reticulum;
- execute `make test`;
- start `rnsd`;
- build a multi-node Reticulum network;
- use LoRa, packet radio, TCP, UDP or serial interfaces;
- transfer files with `rncp`;
- use `rnsh`, `rnx`, `rngit` or `git-remote-rns`;
- test LXMF/LXST/Nomad Network/Sideband interoperability;
- audit route/path behavior;
- benchmark throughput;
- validate the upstream performance figures;
- validate release signatures or artifact reproducibility;
- perform a cryptographic or anonymity audit;
- inspect the non-GitHub canonical development forge.

## Evidence boundary

**VERIFIED** means repository-native evidence supports that Reticulum is a mature, packaged, tested reference implementation with active maintenance and a substantial deployed application ecosystem.

It does **not** mean GitHub Gold independently verified its cryptographic guarantees, anonymity properties, routing correctness, performance claims, physical-radio behavior, or suitability for life-safety/emergency-critical deployment.

## Strong recursive leads

1. **Canonical Reticulum development forge** — identify and inspect the source-of-truth repository/review history instead of relying on the GitHub mirror.
2. **RNode firmware/hardware** — open LoRa interface designed for Reticulum; investigate firmware, board designs, supported radios, update path and license.
3. **LXMF** — delay/disruption-tolerant messaging over Reticulum.
4. **LXST** — real-time audio/signals transport over the same network stack.
5. **Sideband** — broad GUI communications client across mobile/desktop platforms.
6. **Nomad Network** — resilient/off-grid application and page-browsing layer.
7. **`rncp` / Resource transfer** — fragmentation, resumption, checksumming, backpressure and large-file behavior on tiny links.
8. **`rnsh` / `rnx`** — authentication, authorization, sandboxing and remote-execution boundaries.
9. **`rngit` / `git-remote-rns`** — Git transport over resilient low-bandwidth links.
10. **Alternative Reticulum implementations** — `microReticulum`, Rust implementations and interoperability test quality.
11. **Reticulum vs Meshtastic** — compare routing model, application architecture, bandwidth assumptions, identity/security model, hardware coupling and use cases without treating them as interchangeable systems.

## Curator verdict

**KEEP — VERIFIED — A / 25.**

Reticulum is unusually valuable technical research material: a complete cryptography-oriented networking stack designed to bridge LoRa, packet radio, serial and IP-class transports while remaining usable on very low-bandwidth links. Its custom protocol architecture and included operational utilities make it genuine GitHub Gold.

The two main reasons it is not scored higher are important rather than cosmetic: the GitHub repository is only a mirror of development happening elsewhere, and the custom Reticulum License contains significant use restrictions that reduce straightforward code reuse.