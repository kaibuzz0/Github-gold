# Syncthing — BEP, local discovery, and relay architecture

- **Repository:** https://github.com/syncthing/syncthing
- **Author / Org:** Syncthing
- **Category:** local-first / synchronization protocol / peer discovery / relay infrastructure
- **Evidence:** VERIFIED
- **Gold score:** 29 / 30
- **Tier:** S
- **Discovery source:** Recursive follow-up from the verified Syncthing dossier.

## Why this component matters

Syncthing's value is not only the application. Its networking stack is a useful reference architecture for synchronization that can operate directly on a LAN while optionally using global discovery and relays to solve addressability/NAT problems across wider networks.

## Architecture verified from upstream

### Block Exchange Protocol

The source package `lib/protocol` explicitly implements the Block Exchange Protocol (BEP). The generated `syncthing-bep(7)` manual describes BEP as the protocol used between two or more devices forming a cluster. The protocol layer is therefore a first-class implementation component, not merely documentation terminology.

### Address resolution has independent paths

Current upstream device-ID documentation describes three ways to determine where a peer is reachable:

1. **Static configured address** — an IP/port or hostname can be configured directly.
2. **Local discovery** — LAN Syncthing instances periodically announce device ID, address and port; a received announcement supplies an address to try.
3. **Global discovery** — when enabled, a device announces to a global discovery service; it can be queried when no static address or local announcement is available.

This separation is important: public/global discovery is not conceptually required for two peers that can resolve each other by static configuration or local discovery.

### Local discovery is a concrete protocol

The repository contains `lib/discover/local.go`, and the current generated manual identifies **Local Discovery Protocol v4**. The implementation periodically sends announcement packets and maintains discovery state/cache. This provides repository-native evidence for LAN peer discovery rather than relying on marketing claims.

### Peer authentication remains tied to device identity

After address resolution and connection establishment, upstream documentation describes a TLS handshake where peers present certificates. Syncthing derives the remote device ID from the certificate and checks it against configured expected device IDs before accepting the connection. Current documentation says new installations use a 256-bit Ed25519 key and that the device ID is derived from certificate data.

A useful security distinction follows: upstream explicitly notes that local discovery announcements themselves are not cryptographically protected and can be spoofed, but the subsequent certificate/device-ID verification is a separate gate. Discovery information should therefore be treated as an address hint, not peer authentication.

### Relays are optional connectivity infrastructure

The repository contains dedicated relay dial/listen code, a relay client/protocol implementation, and `cmd/strelaysrv` for operating a relay server. The relay protocol identifies itself as `bep-relay`. Upstream networking documentation describes relaying as a fallback when direct connectivity/port forwarding is unavailable and notes that relay performance is poorer than a direct connection.

The bundled relay server can participate in the public relay pool by default, but the existence of the server implementation and static/dynamic relay client machinery makes the relay layer independently deployable infrastructure rather than an opaque hosted dependency.

## Practical local-first conclusion

For a controlled LAN, Syncthing can avoid public discovery and public relays when peers can reach each other through static addresses and/or local discovery. The core synchronization relationship is peer-to-peer; global discovery helps locate peers across networks and relays help when a direct connection cannot be established.

This does **not** mean every topology works automatically while fully offline. Routed/VLAN-separated networks may block broadcast/multicast local discovery, and NAT/firewall boundaries can prevent direct reachability. Static addresses, network configuration, or self-hosted infrastructure may be needed.

## Useful reusable components / research targets

- `lib/protocol` — BEP implementation
- `lib/discover` — local/global discovery management
- `lib/connections` — direct and relay connection orchestration
- `lib/relay/client` — relay client machinery
- `lib/relay/protocol` — relay protocol implementation
- `cmd/strelaysrv` — self-hostable relay server
- `cmd/stdiscosrv` — discovery server implementation
- generated protocol manuals (`syncthing-bep`, `syncthing-localdisco`, `syncthing-relay`, `syncthing-device-ids`, `syncthing-networking`)

## Verification performed

Inspected current repository code-search results and generated manuals for BEP, local discovery, device identity/address resolution, connection orchestration and relay implementation. Confirmed concrete implementation files for protocol, discovery, relay dial/listen, relay client/protocol and relay server.

## Not verified by GitHub Gold

GitHub Gold did **not**:

- execute two Syncthing nodes on an isolated LAN;
- packet-capture local discovery or BEP;
- disable internet access and demonstrate synchronization;
- operate `stdiscosrv` or `strelaysrv`;
- test NAT traversal or relay failover;
- benchmark direct versus relay throughput;
- independently audit TLS/device-ID authentication or discovery spoofing behavior.

## Caveats / risks

- Local discovery depends on network support for its broadcast/multicast traffic; segmentation can prevent discovery even when IP routing exists.
- Upstream documentation explicitly states that local discovery is not cryptographically protected, so announcements can theoretically be spoofed. Peer certificate/device-ID verification is the authentication boundary.
- Relays solve reachability, not performance; upstream warns relay connections can perform poorly compared with direct connectivity.
- A relay server joining the default public pool can consume operator bandwidth serving other users; private/self-hosted deployments should configure this intentionally.
- Synchronization remains distinct from backup; deletion or unwanted changes can propagate.

## Licensing

Syncthing is MPL-2.0. GitHub Gold copied no implementation source. Any reuse/adaptation of covered source must preserve applicable MPL obligations.

## Score rationale

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5 | Practical synchronization and connectivity architecture with LAN-only and wider-network deployment paths. |
| Working Evidence | 5 | Concrete protocol/discovery/relay implementations plus generated protocol manuals and the mature parent application's evidence base. |
| Reusability | 5 | BEP, discovery, connection orchestration and relay design are useful architectural references/components. |
| Novelty | 4 | The techniques are established, but their integrated, mature local-first design is technically valuable. |
| Documentation | 5 | Dedicated manuals document BEP, local discovery, relays, networking and device identity. |
| Maintenance | 5 | Parent repository is actively maintained in September 2026. |

**Total: 29 / 30 — S tier.**

## Strongest next leads

1. Inspect `cmd/stdiscosrv` and its API/storage/replication model as a self-hostable discovery service.
2. Inspect `cmd/strelaysrv` configuration for a minimal private relay deployment and public-pool opt-out behavior.
3. Investigate current Android/Termux viability separately; do not infer mobile support from desktop/server architecture.
4. After one infrastructure follow-up, rotate to a different technical category to preserve catalog breadth.
