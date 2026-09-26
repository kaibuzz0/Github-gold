# MeshCore flood text delivery and reciprocal-path restoration

- **Upstream:** https://github.com/meshcore-dev/MeshCore
- **Category:** off-grid communications / packet-radio mesh / routing recovery
- **Evidence:** VERIFIED
- **Provisional Gold score:** 28/30 — S tier
- **License:** MIT (GitHub repository metadata)
- **Research date:** 2026-09-21

## Why this matters

This closes the remaining lifecycle question from the stale-route recovery investigation: after a sender abandons a dead cached direct route and retransmits a normal text message by flood, does successful delivery itself cause the receiver to return routing information that can restore a direct path?

For ordinary peer text, the answer in the inspected firmware is **yes**. Flood-delivered text does not merely produce a standalone ACK. The receiver constructs a cryptographically protected path-return packet containing both the reverse path information and the ACK, then sends that path-return by scoped flood. When the sender receives the path-return, the normal path handler stores the returned path as the contact's new `out_path` and processes the embedded ACK.

This gives the official Python retry policy a complete source-level recovery chain: **direct-path failure -> host resets path to flood/unknown -> text retry by flood -> receiver generates path-return+ACK -> sender learns replacement direct path -> subsequent traffic can again use direct routing**.

## Source trace

### 1. Flood-delivered plain text generates a path-return plus ACK

In `src/helpers/BaseChatMesh.cpp`, `onPeerDataRecv()` handles `PAYLOAD_TYPE_TXT_MSG`. For `TXT_TYPE_PLAIN`, it calculates an ACK hash. If `packet->isRouteFlood()` is true, it does not call the ordinary direct `sendAckTo()` path. Instead it calls `createPathReturn(from.id, secret, packet->path, packet->path_len, PAYLOAD_TYPE_ACK, ack_hash, 6)` and sends the resulting packet with `sendFloodScoped()` after `TXT_ACK_DELAY`.

The source comment states the purpose directly: tell the sender the path **to this receiver** so the sender can use `sendDirect()`, while encoding the ACK in the same return packet.

The signed-text branch (`TXT_TYPE_SIGNED_PLAIN`) follows the same pattern, using a four-byte ACK hash. Flood-delivered CLI data also generates a path-return, but with no ACK because CLI data replies do not expect one.

### 2. The sender stores the returned route and consumes the embedded ACK

`onPeerPathRecv()` passes authenticated path-return material into `onContactPathRecv()`. The default implementation replaces the contact's current `out_path` using `Packet::copyPath()`, updates `lastmod`, and invokes `onContactPathUpdated()`.

If the path-return carries `PAYLOAD_TYPE_ACK`, `onContactPathRecv()` calls `processAck(extra)` and clears `txt_send_timeout` when the ACK matches an outstanding transmission.

Thus route relearning and delivery acknowledgement occur in one received path-return packet, but they remain logically distinct operations: storing the route happens before ACK correlation.

### 3. This is specifically triggered by flood reception

For the same ordinary text message received via a non-flood route, the code uses `sendAckTo()` rather than constructing a path-return. The route-teaching behavior is therefore intentionally tied to flood delivery, where the inbound packet contains the path information needed to construct a reciprocal route.

### 4. Additional recovery reinforcement exists

Elsewhere in the same base layer, if an ACK or response still arrives by flood while a direct path is already known, `handleReturnPathRetry()` can send another reciprocal path directly. This is a separate repair mechanism for asymmetric path knowledge and is not required for the basic stale-route -> flood -> relearn lifecycle above.

## Verification boundary

This dossier is based on source inspection of upstream MeshCore at commit `e94125987ed87497e706a0b54d1e80c709343980` and repository metadata. GitHub Gold did **not** compile firmware, run unit tests, flash hardware, transmit LoRa packets, induce a stale route on physical nodes, measure recovery latency, validate RF behavior, or independently audit the cryptography. Statements above distinguish source behavior from runtime verification.

No upstream implementation source was copied into GitHub Gold.

## Maintenance and licensing

GitHub repository metadata reports MeshCore as MIT-licensed and not archived. The repository reported a push on 2026-09-21, providing current maintenance evidence for this research date.

## Gold scoring

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Concrete self-healing behavior for low-infrastructure mesh messaging. |
| Working Evidence | 5/5 | Recovery chain is represented directly in the official firmware source; prior host-side dossier also identified upstream retry tests. |
| Reusability | 5/5 | MIT licensing and clean separation between host retry policy and firmware route learning. |
| Novelty | 5/5 | Combines flood fallback, reciprocal path learning and ACK transport in a compact embedded protocol. |
| Documentation | 4/5 | Source comments are unusually explicit, though the full recovery lifecycle is easier to see by tracing code than from one architectural document. |
| Maintenance | 4/5 | Active upstream with a push on the research date; runtime behavior was not independently exercised here. |
| **Total** | **28/30** | **S tier** |

## Architectural takeaway

The earlier caveat that base firmware does not autonomously turn an ACK timeout into flood fallback remains correct: that escalation policy lives above the base layer (and the official Python stack supplies it). Once a retry actually arrives by flood, however, the firmware receiver automatically supplies the reciprocal path-return needed to relearn direct routing. The two layers therefore compose into an end-to-end recovery mechanism without requiring a separate explicit path-discovery transaction after a successful flooded text retry.

## Strong follow-up leads

1. Verify whether reset-to-flood state is persisted immediately or only after later contact writes.
2. Compare official Android/iOS client behavior with Python `send_msg_with_retry()`.
3. Trace scoped-flood limits and whether they can prevent path-return delivery after a successful inbound flood.
4. Inspect KISS framing/interoperability and gateway behavior.
5. Build a concise Meshtastic vs MeshCore vs Reticulum route-recovery comparison after the MeshCore thread is closed.