# Peer Connectivity Architecture Comparison: Iroh vs Tailscale vs go-libp2p

Date: 2026-08-25

## Purpose

This dossier compares three high-value peer-connectivity architectures already represented in GitHub Gold research:

- **Iroh + noq** — application-embedded public-key peer connectivity built above a multipath-capable QUIC transport
- **Tailscale** — WireGuard overlay connectivity with direct-path discovery plus DERP/UDP-relay fallback
- **go-libp2p** — modular peer-to-peer networking with AutoNAT reachability detection, Circuit Relay v2, Identify/address exchange and DCUtR hole punching

The goal is not to rank them as interchangeable products. The useful result is to isolate **where each architecture places responsibility** for address discovery, reachability classification, relay use, hole punching, path validation and peer-level route policy.

## Evidence boundary

GitHub Gold directly inspected selected current upstream source and recent commit history. It did **not** build, deploy, benchmark, packet-capture, fuzz, perform NAT-lab testing, run protocol conformance or security-audit these systems in this pass.

### Tailscale source inspected

- `tailscale/tailscale` at commit `af4b7b03633a5fe06e6fc274e27fc369007a0e66`
- `wgengine/magicsock/magicsock.go`
- `wgengine/magicsock/endpoint.go`
- recent upstream commits affecting magicsock/DERP

### go-libp2p source inspected

- `libp2p/go-libp2p` at commit `e20bb60ffc4b4ee33640e5fe8f45fccce893cecd`
- `p2p/host/autonat/autonat.go`
- `p2p/host/autorelay/relay_finder.go`
- `p2p/protocol/holepunch/holepuncher.go`
- Circuit Relay v2 client/relay surfaces identified from repository structure

### Iroh/noq evidence

This dossier builds on the source-level findings already recorded in:

- `research/2026-08-25-quinn-noq-source-diff.md`
- `research/2026-08-25-iroh-noq-integration.md`

## Executive architecture map

| Responsibility | Iroh + noq | Tailscale | go-libp2p |
|---|---|---|---|
| Peer identity | Iroh public-key endpoint identity | WireGuard node key + control-plane node metadata + disco key | libp2p Peer ID / crypto identity |
| Transport core | noq QUIC with multipath/NAT traversal extensions | UDP/WireGuard carried through `magicsock`; DERP and peer UDP relay are alternate paths | Pluggable transports such as QUIC/TCP/WebTransport; circuit relay is a separate protocol transport path |
| Address discovery | Iroh peer actor merges lookup, local/reflexive, relay and transport candidates | netmap/control endpoints + STUN/netcheck + port mapping + disco/CallMeMaybe + observed peer paths | Identify/peerstore addresses + AutoNAT/AutoNATv2 + relay addresses + application peer-discovery sources |
| Reachability classification | Candidate/path validity emerges from noq/Iroh connectivity state | `netcheck` characterizes local network; per-peer `endpoint` tracks trusted best direct path | AutoNAT explicitly publishes local `Public`, `Private`, or `Unknown` reachability with confidence |
| Relay infrastructure | Relay is a first-class working path and bootstrap path while direct upgrade continues | DERP is fallback/bootstrap; newer peer UDP relay paths can also become selected best non-DERP paths | Circuit Relay v2 reservations expose `/p2p-circuit` addresses; AutoRelay finds/maintains suitable relays |
| Hole punching | Iroh peer controller schedules attempts; noq handles transport path validation/NAT events | `magicsock` discovery/pings/CallMeMaybe/STUN and WireGuard traffic establish direct UDP reachability | DCUtR coordinates hole punching over an existing relay connection after a direct dial attempt |
| Direct-path validation | noq owns QUIC path state/validation; Iroh only prefers routes that are functional | Disco ping/pong and path trust windows drive `bestAddr`; direct path must be confirmed | Success is a real direct libp2p connection; DCUtR exchanges observed addresses and synchronizes dialing |
| Path preference | Injected Iroh `PathSelector` and peer `RemoteStateActor` above transport | Per-peer `endpoint.bestAddr` plus quality/trust logic inside magicsock | More distributed: dialer/connection manager chooses connections; holepunch upgrades from limited relay connection to direct, rather than one central best-path state machine |
| Control-plane dependence | Can use DNS/Pkarr/relay discovery without a Tailscale-style central network map | Strong control-plane role: netmap distributes peers/endpoints/DERP map/capabilities, while data path remains peer-to-peer/relay | Protocols are decentralized/modular; applications choose DHT/rendezvous/static sources/relay discovery strategy |

## 1. Iroh + noq: transport mechanics below peer-level policy

The previous source trace showed a deliberately layered design.

### noq transport layer

noq owns the QUIC mechanics that should remain below application policy:

- path validation
- logical `PathId` state
- multiple path generations
- per-path timers, draining and retransmission state
- candidate-address exchange
- QUIC NAT-traversal events
- multipath transport behavior

A key architectural point is that a **candidate address is not automatically a trusted route**. Candidate discovery and validated path state remain distinct.

### Iroh compatibility/configuration layer

Iroh wraps noq rather than leaking all transport internals upward. Its QUIC wrapper sets peer-connectivity-oriented defaults for:

- multipath path counts
- per-path keepalive and idle behavior
- remote NAT-traversal candidate limits
- migration behavior

### Iroh `RemoteStateActor`

The peer actor then owns the policy that cannot be cleanly expressed as pure QUIC transport logic:

- merging endpoint/address lookup results
- local and reflexive address candidates
- relay mappings
- custom transports
- noq path lifecycle events
- NAT candidate events
- hole-punch scheduling
- pending path-open retries
- path-selection policy

This produces a reusable separation:

> **Transport validates paths. Peer policy decides which validated path should be preferred and when to continue upgrading connectivity.**

Relay connectivity is intentionally useful immediately. Iroh can keep traffic working over relay while continuing to discover and validate a direct route.

## 2. Tailscale: `magicsock` centralizes adaptive peer routing beneath WireGuard

Tailscale's `magicsock` is architecturally different. It presents WireGuard with an endpoint abstraction while internally managing **multiple possible physical paths for each peer**.

The current `endpoint.go` source explicitly explains that ordinary WireGuard has one endpoint per peer, whereas Tailscale stores likely peer addresses and chooses the currently best endpoint when WireGuard sends.

### Path types visible in current source

`magicsock` currently distinguishes metrics/labels for:

- direct IPv4
- direct IPv6
- DERP
- peer relay IPv4
- peer relay IPv6

The `Conn` owns:

- IPv4/IPv6 UDP sockets
- `netcheck` for local network/NAT conditions and nearest DERP
- NAT-PMP/PCP/UPnP port mapping
- DERP receive channels and active DERP state
- peer/netmap metadata
- discovery keys
- endpoint tracking
- UDP relay management

This is a **single adaptive transport facade beneath WireGuard**, not a set of separately composed application protocols.

### Per-peer endpoint state

Each `endpoint` keeps a set of possible addresses but also maintains:

- `derpAddr` as fallback/bootstrap
- `bestAddr` for the best non-DERP path
- `bestAddrAt`
- `trustBestAddrUntil`
- ping state
- per-address endpoint state
- CallMeMaybe endpoint markers
- UDP-lifetime probing state

`udpRelayEndpointReady()` only installs a relay path after functionality has been proven by disco pong reception, and the best-address update is constrained by trust and address quality.

This is important: Tailscale does not simply prefer 'direct' because it is direct. It maintains a **time-bounded trust relationship with a proven peer path** and re-runs path discovery when that trust becomes invalid.

A very recent example is the August 24, 2026 commit `65d222674245e22bac64bb31a5c39cc3de2f9251`, which resets endpoint trust on rekey so magicsock does not coast on a dead path until the old trust window expires.

### Discovery and bootstrap

Tailscale combines several inputs:

- control-plane distributed endpoint information/netmap
- local STUN/netcheck results
- port mappings where available
- disco protocol ping/pong
- CallMeMaybe address exchange
- observed peer paths
- DERP bootstrap/fallback

The architecture therefore places more responsibility in **one peer path manager** than go-libp2p does.

### Fresh maintenance evidence

Current upstream work reinforces that this subsystem is active:

- **2026-08-25** `da1fc4fc...` — magicsock facilities for multiple disco-key sources, enabling future dynamic key switching
- **2026-08-24** `65d22267...` — reset endpoint path trust on rekey
- **2026-08-24** `75519889...` — DERP client app-name propagation and server-side filtering support
- **2026-08-24** `6872f1c4...` — compatibility tests for DERP `peerPresent` frames across server versions

## 3. go-libp2p: reachability, relay and hole punching are intentionally separate services/protocols

go-libp2p has a more compositional architecture. Instead of one monolithic path manager, it separates several concerns.

### AutoNAT: classify local reachability

`p2p/host/autonat/autonat.go` maintains explicit reachability state:

- `Public`
- `Private`
- `Unknown`

It combines:

- external dial-back observations from AutoNAT peers
- recent inbound public connections
- local-address changes
- peer protocol capability discovery
- a confidence counter to avoid flipping state on one ambiguous failure

AutoNAT publishes `EvtLocalReachabilityChanged`, so other host subsystems can react to reachability without being tightly coupled to the detection implementation.

That is a strong reusable pattern:

> **Make NAT/reachability classification an event-producing subsystem rather than embedding it directly in every connection decision.**

### AutoRelay + Circuit Relay v2: obtain durable relay reachability

`p2p/host/autorelay/relay_finder.go` maintains two distinct concepts:

- **candidate** — a peer that appears capable of Circuit Relay v2
- **relay** — a candidate with which the node has an active reservation

The relay finder:

- consumes an application-supplied peer source
- tests relay capability
- obtains reservations
- refreshes reservations
- backs off failed candidates
- expires old candidates
- publishes updated `/p2p/.../p2p-circuit` addresses

The current source comments explicitly note that candidate selection is currently simple/random and could later incorporate better strategies such as RTT.

This differs sharply from Tailscale's centrally operated DERP map. libp2p defines the relay protocol and host machinery, but **applications decide where relay candidates come from**.

### DCUtR hole punching: coordinate direct upgrade over an existing relay connection

`p2p/protocol/holepunch/holepuncher.go` makes the relay/direct upgrade sequence unusually explicit.

For a peer behind NAT/firewall, the hole puncher:

1. observes an inbound relayed connection
2. waits for Identify so peer public/observed addresses are available
3. checks whether a direct connection already exists
4. tries a normal direct dial if a public peer address exists
5. only if that fails, opens the DCUtR coordination stream over the relay connection
6. exchanges non-relay observed addresses
7. measures RTT
8. sends a SYNC message
9. waits approximately half the measured RTT
10. performs synchronized direct connection attempts
11. retries a bounded number of times

The current implementation uses up to three hole-punch attempts and records tracing/metrics throughout.

This yields another reusable pattern:

> **Use the relay connection as a rendezvous/control channel for direct-path establishment, not only as a fallback data pipe.**

### Fresh maintenance evidence

The current go-libp2p head is from **August 3, 2026**. The latest commit `e20bb60f...` fixes a hole-punch initialization ordering bug by initializing the timeout before registering the network notifiee. July 29 also added a reachability stress test, and release `v0.49.0` landed July 28.

## 4. The three architectures solve the same broad problem at different layers

### Iroh: peer-centric application connectivity

Iroh's core abstraction is an application peer identified by a key. QUIC/noq paths are transport implementation details. A per-peer actor decides how relay and direct routes evolve over time.

Best fit as a reusable model when an application wants:

- secure peer identity
- QUIC streams/datagrams
- transparent relay fallback
- ongoing direct-path upgrades
- protocol embedding inside the application process

### Tailscale: packet-overlay connectivity beneath WireGuard

Tailscale's core abstraction is an overlay-network peer. `magicsock` hides path churn underneath WireGuard, so upper layers see stable encrypted network connectivity while endpoint addresses, DERP routes and direct UDP paths change.

Best fit as an architecture reference when the goal is:

- transparent IP/network overlay behavior
- control-plane-distributed peer membership
- one adaptive endpoint/path manager beneath a packet tunnel
- sophisticated direct-vs-relay path probing without exposing that complexity to applications

### go-libp2p: protocol-composable decentralized connectivity

go-libp2p's core abstraction is a peer host composed from transports and protocols. AutoNAT, AutoRelay, Identify and DCUtR cooperate through host/event interfaces but stay separately replaceable.

Best fit as an architecture reference when the goal is:

- application-selectable discovery mechanisms
- multiple transports
- decentralized relay selection
- explicit reachability signals
- protocol-by-protocol composability

## 5. Responsibility matrix

### Transport layer

- **Iroh/noq:** transport understands multipath path identity and NAT-related QUIC events.
- **Tailscale:** magicsock is effectively a path-adaptive UDP transport facade underneath WireGuard.
- **go-libp2p:** transports are modular; NAT/relay/hole-punch behavior largely lives in host/protocol layers above them.

### Discovery layer

- **Iroh:** peer actor merges several candidate sources and feeds transport path openings.
- **Tailscale:** control-plane endpoints, STUN/netcheck, disco and port mapping are integrated into magicsock's worldview.
- **go-libp2p:** peerstore/Identify, AutoNAT, application discovery and relay peer sources stay more separate.

### Relay layer

- **Iroh:** relay is a usable path while direct connectivity continues to improve.
- **Tailscale:** DERP is bootstrap/fallback; peer UDP relay has become another measured path type.
- **go-libp2p:** Circuit Relay v2 is an addressable protocol path with explicit reservations and limited connections.

### Peer policy layer

- **Iroh:** explicit peer actor + injected path selector.
- **Tailscale:** explicit per-peer endpoint object and best-address trust state.
- **go-libp2p:** policy is more distributed across host connection management, relay services, peerstore and DCUtR upgrade logic.

## 6. High-value reusable design patterns

### Pattern A — keep candidate discovery separate from path validation

Seen most clearly in Iroh/noq, but Tailscale also follows it through disco pong confirmation and trusted `bestAddr` state.

Do not treat 'we learned an address' as 'this route works.'

### Pattern B — let relay connectivity establish service immediately

Iroh and libp2p both make this explicit. A relay path can carry traffic while direct-path work continues.

This avoids making successful NAT traversal a prerequisite for basic connectivity.

### Pattern C — use relay connectivity to improve direct connectivity

- Iroh continues direct upgrade attempts while relayed.
- libp2p DCUtR explicitly uses the relay stream to exchange addresses and synchronize hole punching.
- Tailscale DERP/disco provides bootstrap reachability and address coordination while magicsock searches for direct paths.

### Pattern D — expire path confidence

Tailscale's `trustBestAddrUntil` is a particularly concrete implementation. A previously good UDP route is not assumed good forever.

Iroh/noq similarly distinguishes live validated paths from stale candidates and path lifecycle state.

### Pattern E — expose reachability as state/events when multiple subsystems need it

libp2p AutoNAT's reachability event model is a strong pattern when relay advertisement, discovery and application behavior all depend on whether a host appears publicly reachable.

### Pattern F — centralize peer policy only when the upper abstraction benefits

- Tailscale benefits from centralizing path choice because WireGuard should see one stable endpoint abstraction.
- Iroh benefits from a peer actor because all QUIC connections to one endpoint share address/path policy.
- libp2p benefits from decomposition because applications may replace discovery, transports and relay policy independently.

There is no universally correct layer boundary; the right split follows the abstraction being presented to application code.

## 7. Potential GitHub Gold component targets

### From Tailscale

- `wgengine/magicsock/endpoint.go` — per-peer candidate/path quality and trust-window state machine
- `wgengine/magicsock/magicsock.go` — transport facade and DERP/direct/peer-relay integration
- `net/netcheck` — local NAT/network characterization
- `net/portmapper` — PCP/NAT-PMP/UPnP mapping abstraction
- `disco` — encrypted discovery ping/pong and address-coordination mechanisms
- DERP protocol/server compatibility testing patterns

**License:** Tailscale repository code inspected here uses BSD-3-Clause SPDX headers. Re-check file/component licensing before reuse.

### From go-libp2p

- `p2p/host/autonat` — confidence-based reachability classification
- `p2p/host/autorelay` — relay candidate/reservation lifecycle
- `p2p/protocol/circuitv2` — reusable relay protocol
- `p2p/protocol/holepunch` — DCUtR coordination and synchronized punching
- Identify/peerstore integration for observed-address distribution
- tracing/metrics surfaces for NAT/hole-punch observability

**License:** go-libp2p is MIT-licensed at repository level as recorded in the existing GitHub Gold dossier; preserve attribution and verify nested dependencies separately.

### From Iroh/noq

See the prior dossiers for detailed targets. The most relevant to this comparison are:

- Iroh `RemoteStateActor`
- `PathSelector`
- Iroh noq wrapper/default tuning
- noq PathId/path lifecycle
- noq NAT traversal candidate/event state machine
- relay-to-direct pending path-open retry behavior

## 8. Caveats

- Tailscale's architecture includes a coordinated control plane; extracting magicsock ideas without that context can miss important assumptions about peer metadata, DERP maps and keys.
- go-libp2p's modularity means behavior depends heavily on host configuration and which discovery/relay services an application enables.
- Iroh/noq is actively evolving around experimental/newer QUIC extensions; source architecture may move faster than mature libp2p/Tailscale interfaces.
- Relay, NAT traversal and path migration are security-sensitive. Reusing individual mechanisms without preserving authentication, replay protection, rate limiting and resource controls can create unsafe designs.
- No performance ranking is asserted by this dossier.

## 9. Strong next research leads

1. **Tailscale `netcheck` + magicsock source trace** — map STUN observations, port mapping, endpoint advertisements and disco probes into `bestAddr` changes.
2. **libp2p AutoNATv2 vs legacy AutoNAT** — identify the newer dial-request model, address validation and how applications should transition.
3. **Circuit Relay v2 resource limits** — inspect reservation lifetime, byte/duration limits and abuse controls.
4. **Iroh vs DCUtR retry policy** — compare Iroh's continuing path-open/hole-punch scheduling with libp2p's bounded synchronized attempts.
5. **Observability comparison** — Tailscale path metrics vs libp2p AutoNAT/holepunch dashboards vs Iroh/noq tracing.

## Promotion status

This is a comparative architecture dossier. It does not add a new standalone project to the promotion queue. Tailscale, go-libp2p, Iroh and noq retain the evidence levels/scores recorded in their existing GitHub Gold dossiers and catalog queue state.
