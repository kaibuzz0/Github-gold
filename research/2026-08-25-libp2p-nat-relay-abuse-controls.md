# go-libp2p AutoNATv2 and Circuit Relay v2 — defensive resource architecture

Date: 2026-08-25

## Research status

- **Project:** `libp2p/go-libp2p`
- **Area:** AutoNATv2, Circuit Relay v2, Resource Manager integration
- **Evidence:** VERIFIED source-level architecture research
- **Catalog effect:** strengthens the existing go-libp2p entry; this is not a separate project candidate
- **Verification boundary:** source and recent commit history inspected; GitHub Gold did not deploy a public relay, perform load/DoS testing, packet-capture the protocols, fuzz them independently, or conduct a security audit

## Why this pass matters

Previous GitHub Gold research mapped how go-libp2p discovers reachability, reserves relays, and upgrades relayed connections to direct paths. That covered the success path but not the equally important question: **how do public NAT-check and relay services avoid becoming unbounded amplification or resource-exhaustion infrastructure?**

The current implementation answers that at multiple layers rather than relying on one global limiter.

---

## 1. AutoNATv2: reachability verification with bounded server cost

AutoNATv2 lets one peer ask another peer to dial back a candidate address in order to verify external reachability. A naive implementation would be dangerous because an attacker could use a public server to generate traffic toward third-party victims or consume server sockets/memory/CPU.

The current server code includes several independent defenses.

### Resource-manager memory reservation

Before parsing a dial request, the stream is attached to the AutoNATv2 service scope and reserves `maxMsgSize` bytes through the libp2p Resource Manager. If memory cannot be reserved, the stream is reset and the request fails with a resource-limit error.

**Reusable pattern:** protocol handlers should enter a service-specific resource scope and reserve expected memory *before* expensive parsing or allocation.

### Rate limiting at several dimensions

Default AutoNATv2 server settings include:

- global request rate: **60 requests/minute**
- per-peer request rate: **12 requests/minute**
- dial-data request rate: **12 requests/minute**
- maximum concurrent requests per peer: **2**

The server performs the rate-limit check before parsing the dial request.

**Reusable pattern:** apply cheap admission control before parsing attacker-controlled payloads; combine global, identity-scoped, special-expensive-operation, and concurrency limits.

### Public-address filtering by default

`allowPrivateAddrs` defaults to false. Candidate dial addresses are skipped unless they are public, parse correctly, and are dialable by the dedicated dialer host.

This prevents the public AutoNAT service from being casually turned into an internal-network dial primitive. A dedicated `AllowPrivateAddrs` option exists for controlled environments where private-address verification is intentional.

### Candidate-count bounding

The handler stops scanning request-provided addresses after `maxPeerAddresses`, limiting attacker-controlled address-list work.

### Amplification-attack prevention by dial-data challenge

The server's default data-request policy is explicitly described in source as amplification-attack prevention. For requests where this policy triggers, the server requires the client to send a randomized amount of dial data before the server performs the dial-back.

The dial-data path also has its own RPM budget. The reader rejects excessively tiny chunks while more data remains, preventing a peer from forcing disproportionate parsing/loop overhead by satisfying the byte requirement with a huge number of tiny messages.

**Reusable pattern:** when a service may emit significant network work on behalf of a requester, require the requester to demonstrate comparable upstream effort/data first.

### Randomized delay before dial-back

After the amplification-resistant dial-data exchange, the server waits for a random duration up to the configured anti-amplification wait (default **3 seconds**) before dialing. The source comment explicitly describes this as protection against "thundering herd style attacks on a victim."

This is important because many independently operated AutoNAT servers could otherwise be synchronized against one target.

### Dedicated dialer host and cleanup

Dial-back uses a dedicated host, force-direct dialing, temporary peerstore state, a bounded dial timeout, and cleanup that closes the peer and removes temporary addresses/state after the test.

This limits state leakage from a reachability probe into ordinary host operation.

### Defensive panic containment

The stream handler catches panics, prints the stack, and resets the stream rather than allowing one malformed/request-edge path to tear down the whole process.

This is not a substitute for correctness, but it is a useful boundary for public protocol services.

---

## 2. AutoNATv2 is newer than the legacy single-status AutoNAT model

GitHub Gold's earlier architecture comparison described AutoNAT conceptually as Public/Private/Unknown reachability state. Current go-libp2p goes further with AutoNATv2 address-level verification integrated into the basic host's address manager/reachability tracker.

Recent history confirms that this path is actively maintained:

- **2026-07-27:** fixed a shutdown race where `GetReachability` could panic after `Close`
- **2026-07-27:** refactored server selection locking so panic unwinding cannot leave the mutex permanently locked
- **2026-06-02:** exposed private-address testing through an explicit option rather than changing the secure default
- earlier work introduced per-address reachable/unreachable/unknown tracking and primary/secondary address logic

**Catalog implication:** future go-libp2p notes should distinguish legacy AutoNAT concepts from the newer AutoNATv2 per-address verification path.

---

## 3. Circuit Relay v2: bounded relay service by default

A public relay can become expensive even when it behaves correctly, so Circuit Relay v2 has a separate resource model.

The current default relay resources include:

- reservation TTL: **1 hour**
- maximum active reservations: **128**
- maximum open relay circuits per peer: **16**
- relay buffer size: **2048 bytes**
- maximum reservations per IP: **8**
- maximum reservations per ASN: **32** (for tracked IPv6 ASNs)
- default per-relayed-connection duration: **2 minutes**
- default data limit: **128 KiB in each direction**

The old `MaxReservationsPerPeer` field is deprecated with the note that only one reservation per peer is needed.

### Why IP and ASN quotas matter

Peer identities alone are cheap to create, so a peer-ID limit is not sufficient against Sybil-style reservation exhaustion. The relay constraint layer therefore tracks reservation pressure by:

1. total reservations
2. source IP
3. ASN for IPv6 addresses when ASN information is available

Expired reservations are cleaned before admitting new ones, and refreshing a peer's reservation first removes its old reservation so refreshes do not accidentally consume multiple slots.

**Reusable pattern:** public rendezvous/relay infrastructure needs quotas anchored to multiple identities — cryptographic identity plus network-origin identity — because each dimension alone is cheap to evade in some environments.

### Connection-level byte and time budgets

Relay reservations and actual relayed circuits are separate resources. Even a legitimately reserved peer cannot create unbounded data forwarding: `RelayLimit` can bound both circuit lifetime and bytes relayed in each direction.

**Reusable pattern:** bound scarce *control-plane slots* and *data-plane consumption* independently.

---

## 4. Resource Manager is a cross-cutting defensive layer

AutoNATv2 explicitly uses libp2p stream service scopes and memory reservations. This complements protocol-specific limits rather than replacing them.

The broader design lesson is a layered budget model:

- **host/resource-manager scope:** memory/stream/service resource admission
- **protocol scope:** message-size, concurrency and RPM budgets
- **identity/network scope:** per-peer, per-IP and per-ASN quotas
- **operation scope:** special budget for amplification-sensitive dial-data operations
- **data-plane scope:** relay duration and byte caps
- **time scope:** deadlines, TTLs, expiry cleanup and randomized anti-herd delay

No single limiter needs to perfectly classify abuse if multiple layers cap different failure modes.

---

## 5. Comparison to the previous Iroh/Tailscale/libp2p findings

### go-libp2p

libp2p exposes the most visibly modular defensive architecture of the three stacks researched so far:

- AutoNATv2 verifies external addresses
- AutoRelay obtains relay reservations
- Circuit Relay v2 bounds relay resources
- DCUtR coordinates relay-to-direct upgrades
- Resource Manager enforces service/stream/memory budgets

This modularity makes individual mechanisms reusable, but operators must configure and compose several subsystems correctly.

### Iroh/noq

Iroh/noq centralizes more path-upgrade behavior around the endpoint/transport relationship. A useful next comparison is whether Iroh's relay service has equivalent reservation/byte/time/network-origin quotas and how those limits interact with continuing relay-to-direct upgrade attempts.

### Tailscale

Tailscale centralizes peer path policy in `magicsock` and relies on DERP for relay fallback. A useful next comparison is DERP's operator-side admission and resource controls versus Circuit Relay v2's explicit reservation model.

---

## 6. High-value reusable design principles

1. **Reject before parse when possible.** Admission/rate checks should precede expensive request decoding.
2. **Reserve memory before handling attacker-controlled protocol messages.**
3. **Use a separate dialer identity/state boundary for server-driven reachability probes.**
4. **Prevent reflection/amplification by requiring requester-side data work before server-side outbound traffic.**
5. **Add randomized jitter when many independent servers could otherwise synchronize traffic toward one target.**
6. **Do not trust cryptographic identity as the only quota key.** Add IP/ASN/network-origin constraints for public infrastructure.
7. **Separate reservation quotas from active-circuit quotas and data-plane byte/time budgets.**
8. **Expire state aggressively and make refresh idempotent with respect to quota usage.**
9. **Expose private-network behavior only as an explicit opt-in when the public-safe default should reject it.**
10. **Layer generic resource management under protocol-specific abuse controls.**

---

## Verification boundary

GitHub Gold inspected current upstream source for AutoNATv2 server/options and Circuit Relay v2 resource/constraint code, plus recent relevant commit metadata. It did not:

- run a public relay or AutoNAT server
- generate malicious or high-volume traffic
- verify limits experimentally
- inspect every Resource Manager path
- conduct a cryptographic or security audit
- perform fuzzing or race testing
- validate behavior across NAT types or IPv4/IPv6 provider networks

The findings describe inspected architecture and upstream-maintained code, not an independent security certification.

## Next research leads

1. inspect Circuit Relay v2 reservation vouchers/authentication and connection admission paths
2. compare relay-v2 limits to Tailscale DERP server limits/admission controls
3. inspect Iroh relay server quotas and anti-abuse controls
4. trace AutoNATv2 reachable/unreachable/unknown results into BasicHost address advertisement
5. inspect AutoNATv2 dashboard metrics and identify operational alerts for abuse/resource exhaustion
6. inspect libp2p Resource Manager default service/protocol limit generation and how relay/AutoNAT scopes inherit those limits
