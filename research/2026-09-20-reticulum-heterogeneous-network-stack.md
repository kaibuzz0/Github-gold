# Reticulum — heterogeneous cryptographic network stack

- Repository: https://github.com/markqvist/Reticulum
- Author: Mark Qvist
- Category: mesh/radio communications; networking; offline systems; privacy; emergency/off-grid communications
- Evidence: **VERIFIED**
- Provisional Gold score: **27/30 (S tier)**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 5/5
  - Documentation 5/5
  - Maintenance 2/5 (GitHub is explicitly a public mirror; active upstream development occurs elsewhere, so GitHub commit freshness alone is not the full maintenance signal)
- Primary language: Python
- License: custom **Reticulum License** (source-available with use restrictions; not standard OSI-permissive licensing)

## What it is

Reticulum is a user-space networking stack designed to build local and wide-area networks across heterogeneous carriers such as LoRa/RNode, packet-radio TNCs, serial/KISS links, TCP, UDP, Ethernet/Wi-Fi and external programs. It does not require IP as its network layer, although IP transports can carry Reticulum.

The reference implementation is also the project's authoritative protocol definition. Upstream describes coordination-less addressing, self-configuring multi-hop transport, encrypted links and packets, delivery acknowledgements, arbitrary-data transfer, request/response primitives, channels/buffers and extensible interfaces.

## Why it is Gold

Reticulum is unusually valuable because it is not merely a LoRa messenger. It is a reusable networking layer that can bridge very slow radio links and ordinary IP networks under one application API. That makes it a strong architectural reference for resilient/offline systems, heterogeneous transport abstraction, low-bandwidth networking and user-controlled infrastructure.

Particularly useful surfaces for deeper study include:

- `RNS/Interfaces/` — heterogeneous physical/link interface adapters;
- identity, destination and link primitives;
- transport/path discovery and announcement handling;
- channel/buffer and resource-transfer machinery;
- included network utilities such as `rnsd` and related diagnostic/management tools;
- RNode integration for LoRa;
- custom-interface extension points;
- companion/community implementations, especially microReticulum and Reticulum-Go, which upstream currently identifies as known-good implementations.

## Working evidence

Evidence inspected on 2026-09-20:

1. The official repository documents a complete reference implementation and states that core protocol features are implemented and the API/wire format can be considered stable.
2. The project documents built-in interfaces spanning Ethernet/IP, RNode/LoRa, packet-radio TNC/KISS, serial, TCP/UDP and process/stdin-stdout style transports.
3. The repository provides installation through the `rns` Python package and documents an `rnspure` option for unusual systems where normal external dependencies are unavailable.
4. GitHub release **RNS 1.5.2** was published 2026-08-29 with wheel/source artifacts plus manual PDF/EPUB artifacts; GitHub exposes SHA-256 digests for those assets.
5. The public mirror received documentation commits as recently as 2026-09-19.
6. Upstream explicitly warns that GitHub is a public mirror and development happens elsewhere; maintenance conclusions therefore must not rely solely on GitHub PR/commit activity.

`VERIFIED` here means repository-native evidence establishes a released, documented, actively maintained reference implementation with concrete install artifacts and multiple supported transport interfaces. GitHub Gold did **not** independently install Reticulum, establish a radio/IP network, verify wire interoperability, benchmark throughput, or security-audit the protocol.

## Runtime / requirements

The reference implementation runs in Python 3 userland and does not require kernel modules. The normal `rns` package lists PyCA/cryptography and pyserial as its principal external dependencies. Hardware is transport-dependent: pure IP operation needs no radio hardware, while LoRa commonly uses RNode-compatible hardware and packet-radio operation requires the corresponding modem/TNC/interface.

## Security boundary

Upstream documents X25519/Ed25519 identity/key-agreement primitives, HKDF, SHA-256/SHA-512, HMAC-SHA256 and AES-256-CBC-based encrypted tokens. These are implementation claims and design evidence, **not** an independent GitHub Gold security certification. Upstream itself states that Reticulum has not been externally security audited and warns about reduced assurance/performance when falling back to its pure-Python cryptographic primitives instead of PyCA/OpenSSL.

## Licensing caveat — important

The current `LICENSE` is a custom Reticulum License. It grants broad rights but adds at least two material restrictions: the software may not be used in systems whose functions include purposefully harming human beings, and may not be used directly or indirectly to create AI/ML/language-model training datasets. Because these are additional field/use restrictions, do **not** treat this repository as ordinary MIT/BSD/Apache-style permissive open source.

GitHub Gold therefore catalogs and links Reticulum rather than copying implementation source. Any reuse, redistribution or incorporation should be reviewed against the current upstream license first.

## Risks / limitations

- The GitHub repository is explicitly a mirror, not the primary development location.
- No external security audit was established in this run; upstream explicitly notes that one has not occurred.
- The custom license restricts some uses and requires more care than conventional permissive OSS.
- RF legality, frequency allocation, transmit power and duty-cycle rules remain jurisdiction-dependent when radio transports are used.
- Performance varies radically by physical carrier; upstream performance figures were not independently reproduced here.
- Community implementations should not be assumed wire-compatible merely because they use the Reticulum name; upstream explicitly warns about incorrect/fake implementations and names only selected known-good implementations.

## Meshtastic comparison

Reticulum and Meshtastic overlap in off-grid radio use but occupy different architectural layers. Meshtastic is a device firmware/ecosystem centered on LoRa mesh messaging and telemetry across supported embedded boards. Reticulum is a general networking stack intended to span LoRa, packet radio, serial and IP transports and expose reusable networking primitives to applications. They are therefore better cataloged as complementary architectural references than as direct substitutes.

## Discovery provenance

Independent GitHub-first follow-up from the Meshtastic dossier's planned comparison work. A duplicate search of the GitHub Gold repository returned no existing Reticulum entry before this dossier was created.

## Strong follow-up leads

1. Inspect the `RNS/Interfaces` architecture and identify the cleanest reusable transport-abstraction patterns.
2. Trace announce/path discovery and transport routing with source evidence.
3. Inspect `Resource`, `Channel` and `Buffer` for low-bandwidth reliable-transfer techniques.
4. Verify the current RNode firmware ecosystem and licensing separately.
5. Evaluate upstream-recognized microReticulum and Reticulum-Go as independent implementation candidates rather than assuming parity.
6. Complete the off-grid landscape with MeshCore using the same evidence/scoring rubric.
