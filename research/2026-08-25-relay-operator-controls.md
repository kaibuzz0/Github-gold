# Tailscale DERP and Iroh relay — operator-side admission and resource controls

Date: 2026-08-25

## Research status

- **Projects:** `tailscale/tailscale` DERP server and `n0-computer/iroh` relay server
- **Area:** public relay admission, rate limiting, backpressure, identity-aware policy and operator controls
- **Evidence:** VERIFIED source-level architecture research
- **Catalog effect:** strengthens the existing Tailscale and Iroh entries; this is not a separate project candidate
- **Verification boundary:** selected current upstream source and recent commit history inspected; GitHub Gold did not deploy either relay, load-test them, perform denial-of-service testing, fuzz them independently, verify every configuration path, or conduct a security audit

## Why this pass matters

The previous relay-defense pass documented go-libp2p's explicit reservation, circuit, byte, time, IP and ASN quotas. That model is useful, but it should not become the assumed template for all public relay systems.

Tailscale DERP and Iroh expose a different operator model. Both can enforce client admission and traffic limits, but neither presents the same reservation-oriented quota surface as Circuit Relay v2. Their defenses are instead concentrated around connection admission, authenticated identity, per-client receive limits, bounded queues/write timeouts, duplicate-key handling, policy callbacks and observability.

The important catalog lesson is therefore not "relay systems all need the same limits." It is: **identify where each architecture places its trust boundary and which scarce resources are explicitly bounded at that boundary.**

---

## 1. Tailscale DERP: authenticated relay with configurable admission and per-client rate control

The current DERP server keeps a relatively compact data-plane model: connected clients are keyed by their Tailscale node public key and packets are forwarded to local or meshed destinations. Operator controls are layered around that core.

### Admission control can be tied to the operator's tailnet

The DERP server exposes a `SetVerifyClient` path that checks connecting clients against a local `tailscaled` instance. It also supports `SetVerifyClientURL`, which delegates admission to an external HTTP controller.

The external admission path has an explicit `verifyClientsURLFailOpen` policy. This matters operationally because an unreachable policy backend forces the operator to choose whether relay availability or admission strictness wins during control-plane failure.

**Reusable pattern:** external admission systems should make fail-open versus fail-closed behavior explicit rather than silently choosing one.

### Application-level deny policy

DERP can reject selected client `AppName` values while exempting trusted mesh peers. Recent upstream work on **2026-08-24** also constrained advertised app names to at most 32 bytes of printable ASCII and propagated them to trusted DERP watchers so operators can attribute connections by application.

This is a useful pattern because it adds a policy/observability dimension without treating an application label as a cryptographic identity. The actual client identity remains the node public key.

### Per-client receive-rate token bucket

DERP exposes a JSON-serializable `RateConfig` with:

- `PerClientRateLimitBytesPerSec`
- `PerClientRateBurstBytes`

The burst value is clamped upward to at least the maximum DERP send-packet frame size plus key material so a valid packet cannot become impossible to receive purely because the configured burst bucket is too small.

Rate-limit changes are applied to existing connected clients, not just new connections. Trusted mesh peers are exempt.

A zero per-client rate disables this limiter, so this is an **operator-configured control, not proof that every DERP deployment is rate-limited by default**.

**Reusable pattern:** when a byte-rate limiter wraps framed protocols, make the minimum burst capacity large enough for the largest legitimate frame.

### Bounded outbound queue and client write timeout

The server's default per-client send queue depth is **32 packets**. Ordinary client TCP writes default to a **2-second timeout**. Trusted mesh writes use a longer privileged timeout.

These controls bound how much queued relay traffic a slow or stalled client can accumulate and how long a write can occupy the send path.

The server also exports explicit drop reasons, including queue-head, queue-tail, write-error, duplicate-client and unavailable-destination cases, along with packet/byte drop metrics.

**Reusable pattern:** backpressure is not complete unless drops and timeout causes are observable enough for operators to distinguish congestion, dead clients, bad destinations and policy behavior.

### Duplicate node-key behavior

DERP tracks multiple simultaneous connections presenting the same node public key. Temporary overlap is expected during network transitions, so duplicates are not automatically fatal.

However, the server tracks which duplicate connections are actively sending. Under its duplicate-connection policy it can disable a set of connections when multiple peers appear to be "fighting" with the same cloned node key.

This is a useful defensive distinction: **tolerate benign transient duplication, but detect concurrent conflicting use of one authenticated identity.**

### Mesh separation

DERP mesh peers use a separate pre-shared mesh key and are exempt from some ordinary-client controls such as the per-client receive limiter and application-name deny policy.

That creates a clear trust tier:

- ordinary authenticated relay clients
- trusted regional mesh peers

This is operationally powerful, but it means compromise or misconfiguration of the privileged mesh tier has a different blast radius than an ordinary client.

---

## 2. Iroh relay: authenticated endpoint identity plus pluggable lifecycle-aware policy

Iroh's relay server exposes a more application-embeddable policy surface. Its relay configuration includes a generic access-control trait rather than only a fixed allow/deny mechanism.

### The access hook sees a proven endpoint identity

`ClientRequest` carries an Iroh `EndpointId`, and current source documents that the relay handshake proves possession of the corresponding secret key before the access hook runs.

Each physical relay connection also receives a process-unique `ConnectionId`. That is important because one endpoint may have several concurrent connections, and policy code may need to count or track those connections separately.

### Lifecycle-aware access control

The `AccessControl` interface has:

- asynchronous `on_connect`, called before registration
- `on_disconnect`, called for every admitted connection

Iroh threads an `OnDisconnectGuard` through the connection lifetime so an admitted connection reports its disconnect even when setup or execution exits through an error path.

This is a strong reusable pattern for quota/accounting systems: **admission and release should be paired structurally, not rely on every call site remembering to decrement counters manually.**

A custom access policy could therefore implement limits that are not hard-coded into the stock binary, such as:

- maximum connections per endpoint
- account/subscription quotas
- organization-based policy
- externally maintained deny/allow state
- time-window or abuse-scoring logic

GitHub Gold did not implement or test such policies; this is an architectural capability exposed by the inspected interface.

### Stock relay access modes

The current relay binary supports:

- allow everyone
- endpoint allowlist
- endpoint denylist
- external HTTP authorization
- shared bearer-token authorization

The HTTP authorization mode is fail-closed in the inspected implementation: only HTTP `200` with response body `true` grants access. Network errors, other status codes or malformed response text deny the client.

Shared-token mode rejects empty token configurations and can source a token from an environment variable.

### Configurable connection and per-client receive limits

The relay binary exposes optional `Limits` containing:

- connection-accept rate
- connection-accept burst
- per-client receive rate in bytes/second
- per-client maximum receive burst

The comments describe token-bucket semantics for the client data limiter.

The important boundary is that the binary's `limits` field is optional and documented as **disabled when absent**. Like DERP, the existence of rate-limit machinery should not be confused with a guarantee that every public deployment enables it.

### Relay can be disabled while address discovery remains

Iroh can run with relaying disabled while keeping QUIC address discovery enabled. In that mode the server helps peers learn observed addresses for hole punching but does not proxy application traffic.

That separation is architecturally valuable because operators can choose to expose only the lower-cost connectivity-discovery service when they do not want to provide an open relay data plane.

### Key-cache and metrics hooks

The relay configuration exposes a key-cache capacity and a dedicated metrics server option. Those are smaller details than access/rate limits, but they matter for operating a public service because expensive identity-related state and abuse signals should be measurable and bounded where practical.

---

## 3. DERP versus Iroh versus Circuit Relay v2

These systems should not be judged by whether they all expose identical knobs.

### Tailscale DERP

Primary operator controls observed in this pass:

- authenticated node public keys
- optional verification against local `tailscaled`
- external admission-controller URL with explicit fail-open policy
- application-name deny policy
- configurable per-client receive byte rate/burst
- default 32-packet per-client send queue
- default 2-second ordinary-client write timeout
- duplicate-key conflict handling
- detailed drop/rate/queue/client metrics
- separately trusted mesh peers

DERP's model is connection/identity/backpressure oriented rather than reservation-ticket oriented.

### Iroh relay

Primary operator controls observed in this pass:

- handshake-proven endpoint public-key identity
- connection-unique lifecycle IDs
- pluggable `on_connect` / `on_disconnect` policy interface
- allowlist, denylist, external HTTP and shared-token stock policies
- fail-closed external HTTP authorization
- optional accept-rate/burst limits
- optional per-client RX byte-rate/burst limits
- configurable key-cache capacity
- relay-off/address-discovery-only mode
- metrics endpoint

Iroh's most reusable idea is the lifecycle-aware policy hook around an already authenticated endpoint identity.

### go-libp2p Circuit Relay v2

The previously inspected libp2p architecture exposes more explicit built-in reservation/data-plane quotas:

- reservation TTL
- total reservations
- per-IP and per-ASN reservations
- open circuits per peer
- per-circuit duration
- bytes in each direction

This is a different service model rather than evidence that one of the other systems is missing the same exact abstraction.

---

## 4. Reusable design principles extracted from this comparison

1. **Authenticate identity before policy.** Admission hooks are much more useful when the peer identity has already been cryptographically proven.
2. **Make external-policy failure semantics explicit.** Operators should consciously choose fail-open or fail-closed behavior.
3. **Pair admission and disconnect structurally.** Lifecycle guards reduce leaked quota/accounting state.
4. **Separate identity from labels.** Application names are useful for policy and observability but should not replace cryptographic identity.
5. **Bound slow consumers with queue depth and write deadlines, not only incoming byte rate.**
6. **Expose drop reasons.** Backpressure without observability makes production abuse/congestion diagnosis unnecessarily difficult.
7. **Allow safe transient duplicate identity connections while detecting conflicting concurrent use.**
8. **Treat privileged relay-mesh links as a separate trust tier and document their exemptions.**
9. **Do not confuse configurable limits with default enforcement.** Record whether controls are opt-in, default-on or operator-supplied.
10. **Separate discovery from relaying when possible.** A service may help peers establish direct connectivity without taking on the cost/risk of proxying arbitrary data.
11. **Design policy hooks around connection lifecycle, not just one-time authentication.** That enables concurrent-connection quotas and accurate release of state.
12. **Choose quotas that match the relay abstraction.** Reservation limits make sense for reservation-based relays; queue/write/rate/admission limits may be more natural for persistent connection relays.

---

## 5. Maintenance evidence

Tailscale DERP remains actively maintained. A **2026-08-24** commit added bounded printable application names, propagated them to trusted watchers, and added an operator flag for rejecting selected application names. July 2026 history also includes DERP server maintenance around connection metadata and certificate-chain memory handling.

Iroh's current relay source exposes structured-concurrency server lifecycle, authenticated endpoint IDs, pluggable access control, optional traffic/connection limits and relay-versus-address-discovery separation. This pass focused on current source architecture rather than making a claim about production scale or security certification.

---

## Verification boundary

GitHub Gold inspected selected current source in:

- `tailscale/tailscale/derp/derpserver`
- `n0-computer/iroh/iroh-relay`

and relevant recent Tailscale DERP commit metadata.

It did **not**:

- run either public relay
- measure actual memory/CPU/bandwidth ceilings
- test fail-open/fail-closed behavior against a live policy service
- verify per-client rate limits experimentally
- generate duplicate-key conflicts
- inspect every DERP mesh path
- implement a custom Iroh `AccessControl`
- perform protocol fuzzing, penetration testing or formal security review
- prove that public hosted deployments use the available limiter settings

These findings describe inspected architecture and configuration surfaces, not independent security certification.

## Next research leads

1. inspect DERP's exact client-verification HTTP request/response path and timeout behavior
2. inspect Tailscale DERP metrics for alertable queue pressure, rate-limit waits and duplicate identities
3. trace Iroh's connection/byte limit implementation from CLI config into server/client actors
4. inspect whether Iroh's relay stream queues and write paths have independent backpressure limits beyond RX rate control
5. compare authentication/voucher semantics: DERP node proof, Iroh EndpointId proof and libp2p relay reservation vouchers
6. inspect operator guidance/default configurations used by the standalone `derper` and `iroh-relay` binaries so the catalog distinguishes library capability from typical deployment defaults
