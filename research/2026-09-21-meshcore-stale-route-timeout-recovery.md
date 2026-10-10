# MeshCore stale-route timeout and recovery behavior

- Upstream: https://github.com/meshcore-dev/MeshCore
- Category: off-grid communications / embedded mesh routing
- Evidence: VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- Provisional Gold score: 28/30 — S tier
- License: MIT (project-level license established in prior MeshCore dossier)
- Discovery path: recursive follow-up from MeshCore packet/routing dossier

## Question

What happens when a cached direct path stops working? Does an ACK timeout automatically invalidate the route and fall back to flooding/re-discovery?

## Findings

### 1. Send mode is selected entirely from cached path state

`BaseChatMesh::sendMessage()` composes the encrypted datagram and checks `recipient.out_path_len`. If it is `OUT_PATH_UNKNOWN`, the message is flooded and a flood timeout is calculated. Otherwise it is sent with `sendDirect()` over the cached `out_path`, with a direct timeout calculated from packet airtime and path length.

This makes `out_path_len` the immediate routing-state switch between discovery/flood behavior and direct-path behavior.

### 2. ACK reception cancels the send timer

When a matching ACK is received, `processAck()` identifies the pending send and `txt_send_timeout` is cleared. Path-return packets can carry an encoded ACK as well; a matching embedded ACK likewise clears the timer.

A path-return also replaces the contact's current `out_path` with the newly supplied route. Upstream explicitly notes that the default implementation simply replaces the existing path rather than keeping multiple alternatives.

### 3. Timeout itself does not implement automatic stale-path invalidation

`BaseChatMesh::loop()` checks `txt_send_timeout`; if it expires without an ACK, it calls the virtual `onSendTimeout()` callback and clears the timer.

Critically, this base timeout path does not itself clear `recipient.out_path`, set `out_path_len` to `OUT_PATH_UNKNOWN`, retransmit the failed message, or automatically flood for a replacement route.

The behavior after timeout is therefore firmware/application policy, not an automatic routing-core failover in this path.

### 4. Concrete examples confirm the callback can be passive

The `simple_secure_chat` example implements `onSendTimeout()` by printing an error (`timed out, no ACK`). The companion-radio `MyMesh` implementation has an empty `onSendTimeout()`.

Those implementations are strong evidence against describing current `BaseChatMesh` behavior as automatic direct-path failure -> flood retry -> route re-discovery.

### 5. MeshCore does have reciprocal-path repair behavior, but it is triggered by received traffic

When a valid ACK or response arrives by flood while a contact already has a direct `out_path`, `BaseChatMesh` interprets this as evidence that the other side may not have received the reciprocal path. `handleReturnPathRetry()` creates another path-return and sends it directly after a delay.

This is a useful self-repair mechanism, but it is distinct from recovery when a cached outbound direct path becomes completely unusable and no ACK arrives.

## Gold interpretation

MeshCore's routing is lightweight and application-extensible, but GitHub Gold should not claim transparent stale-route failover at the `BaseChatMesh` layer. The inspected implementation provides:

- flood transmission when no cached path exists;
- direct transmission when a cached path exists;
- ACK/path-return handling that can refresh cached routes;
- timeout notification through a virtual callback;
- reciprocal-path repair when flooded return traffic reveals asymmetry.

It does **not**, in the inspected base path, automatically invalidate a cached direct route solely because an ACK timer expires.

This design can be reasonable for constrained embedded systems because policy remains with the firmware/application, but integrators need to implement retry/path-invalidation behavior appropriate to their reliability requirements.

## Verification performed

Source-inspected on the current upstream default branch:

- `src/helpers/BaseChatMesh.cpp`
- `src/helpers/BaseChatMesh.h`
- `examples/simple_secure_chat/main.cpp`
- `examples/companion_radio/MyMesh.cpp`

No code was copied from upstream into GitHub Gold; only behavioral findings and references are recorded.

## Caveats

GitHub Gold did not compile or execute MeshCore, flash hardware, simulate a broken repeater/path, measure ACK timing, or verify behavior over real LoRa links. Other applications built on MeshCore may implement stronger timeout recovery in their own `onSendTimeout()` or host-side logic. The conclusion here is specifically about the inspected `BaseChatMesh` behavior and cited example implementations.

## Strong next leads

1. Inspect companion host protocol behavior to determine whether retry/path invalidation is implemented above firmware `BaseChatMesh`.
2. Audit the duplicate-packet table retention and collision model, especially under dense flood traffic.
3. Inspect KISS modem framing and host interoperability as a reusable component.
4. Evaluate `meshcore.js` / Python host libraries and determine which recovery semantics live client-side.
5. Build a Meshtastic / MeshCore / Reticulum routing-and-recovery comparison using only verified implementation evidence.
