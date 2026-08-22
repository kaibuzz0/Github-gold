# Nebula Overlay Networking Research

Date: 2026-08-22

## Candidate

### Nebula

- **Repository:** https://github.com/slackhq/nebula
- **Author / Org:** Slack Technologies / slackhq contributors
- **Category:** overlay networking / peer-to-peer SDN / NAT traversal / private networking
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 28
- **License:** MIT
- **Primary language:** Go
- **Platforms documented upstream:** Linux, Windows, macOS, FreeBSD, iOS, Android

## What it does

Nebula is a mutually authenticated peer-to-peer software-defined overlay network. Upstream describes it as a scalable overlay networking tool focused on performance, simplicity, and security, with deployments ranging from a small number of hosts to tens of thousands.

Its network model combines certificate-backed node identity, user-defined groups, encrypted tunnels, provider-agnostic filtering, discovery through lighthouses, and UDP hole punching so peers behind NAT or firewalls can attempt direct connectivity.

Nebula is based on the Noise Protocol Framework. The default documented configuration uses elliptic-curve Diffie-Hellman and AES-256-GCM. Nodes receive Nebula certificates that bind overlay IP addresses, names, and group memberships to identities signed by a Nebula certificate authority.

## Why it is valuable to GitHub Gold

Nebula is useful as both a finished private-networking system and a compact reference implementation for building authenticated peer-to-peer overlays without requiring a centralized traffic relay for normal data paths.

Compared with merely cataloging another VPN application, the most valuable material is architectural:

- certificate-backed overlay identities
- distributed peer discovery through lightweight lighthouse nodes
- UDP hole punching and endpoint roaming
- Noise-based mutually authenticated handshakes
- encrypted packet processing
- group-aware host firewall policy
- virtual network interface integration
- certificate-authority and host-certificate CLI tooling
- cross-platform networking abstraction
- FIPS-oriented build paths

## High-value components to inspect further

- **Handshake / Noise integration:** authenticated session setup and key establishment.
- **Lighthouse subsystem:** host discovery, endpoint learning, and peer location coordination.
- **Host map / remote state:** tracking peer overlay identities and reachable underlay endpoints.
- **UDP hole punching:** direct-path establishment through NAT/firewall boundaries.
- **Firewall engine:** certificate group/name/IP-aware filtering rules independent of cloud-provider network policy.
- **Certificate system and `nebula-cert`:** CA creation, host signing, certificate identity fields, expiration and rotation behavior.
- **TUN/TAP and packet path:** virtual-interface ingestion, encryption/decryption, routing, and host delivery.
- **Connection management:** roaming, endpoint preference, reconnect behavior, and path state.
- **Configuration loader:** practical configuration surfaces for private overlay deployments.
- **FIPS build support:** native Go `fips140` build support plus P256/AES-GCM enforcement path.

## Working / maintenance evidence inspected

Repository metadata showed the project was active and not archived, with the default branch updated on 2026-08-21.

The official README documents:

- Linux, Windows, macOS, FreeBSD, iOS, and Android support
- packaged releases and common distribution packages
- source build targets
- `nebula` and `nebula-cert` tooling
- lighthouse-based discovery
- UDP hole punching
- certificate-backed node identity and groups
- Noise Protocol Framework use
- default ECDH and AES-256-GCM cryptography
- native Go FIPS 140-3 build support

Recent commits inspected include:

- **2026-08-21:** native Go `fips140` support with enforcement-mode build path
- **2026-08-21:** TUN offload work
- **2026-08-20:** IPv6 extension-header parsing changed to fail closed on unknown protocols
- **2026-08-20:** certificate-authority command memory-safety fix for 32-bit systems

These are meaningful protocol, packet-processing, portability, and compliance maintenance signals rather than cosmetic activity.

## Licensing

GitHub repository metadata identifies the root project as **MIT licensed**. That is a permissive reuse path, subject to retaining required copyright/license notice.

Mobile clients and other companion repositories are separate projects and must be checked independently before source reuse.

## Verification boundary

GitHub Gold inspected upstream repository metadata, the official README, documented architecture/build surfaces, root license metadata, and recent maintenance commits.

GitHub Gold did **not** independently:

- deploy a Nebula network
- build or execute the source
- run its full tests
- benchmark throughput or scale
- validate NAT traversal across network types
- perform a cryptographic/security audit
- fuzz packet parsing or handshakes
- test mobile clients
- verify FIPS certification/compliance of a deployed build

`VERIFIED` therefore means the repository, documented implementation surfaces, licensing, and active maintenance were inspected; it does not mean an independent security certification.

## Caveats / risks

- Private-network infrastructure is security-sensitive; catalog inclusion is not an audit.
- Certificate-authority key handling is operationally critical; compromise of the CA undermines network identity trust.
- Direct connectivity depends on NAT/firewall behavior; a lighthouse aids discovery but does not guarantee a direct path in every network topology.
- Companion mobile code lives in a separate repository and needs independent license/maintenance review.
- FIPS build support should not be described as blanket compliance for an arbitrary deployment; compliance depends on exact build/runtime/configuration conditions.

## Relationship to current networking batch

Nebula complements the current Tailscale, Headscale, and WireGuard research rather than duplicating it:

- **WireGuard / wireguard-go:** compact VPN protocol and userspace data-plane implementation.
- **Tailscale:** WireGuard-based overlay with NAT traversal, DERP relays, control-plane integration, and `tsnet` embedding.
- **Headscale:** self-hosted implementation of the Tailscale coordination/control server.
- **Nebula:** independent Noise-based overlay design with its own certificates, lighthouse discovery, group-based filtering, and hole punching.

That makes Nebula especially useful for comparative architecture study without requiring source-code copying between projects.

## Promotion status

**Promotion-ready: VERIFIED / provisional S / 28.**

The machine-readable queue already contains a substantial networking batch and `wireguard-go` is also awaiting a safe queue synchronization. Preserve queue integrity over forcing a whole-file mutation. Nebula can be appended together with `wireguard-go` in a controlled queue-maintenance pass.

## Strong recursive leads

1. `DefinedNet/mobile_nebula` — inspect mobile architecture and licensing separately.
2. Nebula lighthouse internals — discovery and endpoint-update mechanisms.
3. Nebula firewall implementation — identity/group-aware packet-policy evaluation.
4. Certificate encoding and rotation tooling — useful PKI design patterns.
5. Compare direct-path selection and roaming behavior with Tailscale's endpoint/path selection.
6. Compare Nebula Noise handshakes and certificate identity model with WireGuard/Tailscale identity/control-plane separation.
