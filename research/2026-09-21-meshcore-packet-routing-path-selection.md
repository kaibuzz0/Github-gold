# MeshCore — packet format, hybrid routing, and path-selection internals

- Repository: https://github.com/meshcore-dev/MeshCore
- Category: mesh/radio communications; embedded networking; LoRa; protocol internals
- Evidence: **VERIFIED**
- Provisional Gold score: **28/30 (S tier)**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- Primary language: C++
- License: **MIT**

## Scope

This dossier deepens the existing MeshCore project entry by tracing its packet representation and the transition between flood discovery and explicit direct paths. It is a component-level architecture record, not a second catalog entry.

## Packet wire format

Current upstream documentation describes a compact Version 1 frame:

`[header][transport_codes(optional)][path_length][path][payload]`

The one-byte header packs route type, payload type, and payload-version bits. Route types distinguish flood, direct, and transport-code variants. `path_length` is itself encoded: six bits hold the path-hash count and the upper two bits encode hash size minus one. Current code accepts 1-, 2-, and 3-byte path hashes; the fourth encoding is reserved/invalid. The path storage ceiling is 64 bytes and the payload ceiling is 184 bytes.

`Packet::readFrom()` validates the encoded path before copying it, rejects malformed path encodings, requires remaining payload bytes, and rejects payloads larger than its fixed payload buffer. `Packet::writeTo()` serializes the same header / optional transport codes / path metadata / path / payload layout.

This is useful embedded protocol design: framing is compact, bounded, and represented without dynamic packet allocation inside the parser itself.

## Hybrid routing behavior

MeshCore is not simply a conventional all-message flood mesh. The core source establishes two distinct forwarding modes.

### Flood discovery

For a flood-routed packet, `Mesh::routeRecvPacket()` appends the forwarding node's identity hash to the packet path, provided the resulting path still fits `MAX_PATH_SIZE` and the firmware role allows forwarding. It then schedules delayed retransmission. The retransmit priority becomes lower as path depth grows.

The default retransmit delay is randomized from an airtime-derived interval. This reduces deterministic simultaneous forwarding, although this run did not simulate collision behavior.

### Direct forwarding

For a direct packet carrying path hashes, a forwarding node checks whether the first path hash matches its identity. If so, and forwarding is permitted, it marks the packet seen, removes its own hash from the front of the path, and schedules direct retransmission. Nodes that are not the next hop release/discard that packet rather than flooding it.

Thus the path is an active forwarding instruction, not merely a historical traceroute record.

## How a direct path is learned

The important transition occurs when useful traffic initially arrives through flood mode.

For chat/request traffic, the receiver can construct a `PAYLOAD_TYPE_PATH` response containing the discovered path. `createPathReturn()` encodes that path inside an encrypted/MAC-protected payload and can include an ACK or application response as extra data. `BaseChatMesh` uses this mechanism after receiving flooded messages or requests so the remote peer can subsequently use `sendDirect()`.

When a path return is received, `BaseChatMesh::onContactPathRecv()` copies the returned path into the contact's `out_path` and updates its timestamp. Later sends choose `sendDirect()` when `out_path_len` is known; otherwise they fall back to flood mode.

This is the central reusable pattern: **flood to discover reachability/path information, cache an explicit route, then send subsequent traffic directly along the cached path.**

## Path-selection caveat: first arrival wins

The core source explicitly labels current flood handling as a **"first packet wins"** implementation. When duplicate copies arrive through multiple flood paths, the first accepted packet determines the path exposed to the application. Upstream comments explicitly note that this may not be the best path by hop count.

The default `BaseChatMesh::onContactPathRecv()` also replaces the contact's existing `out_path` whenever a new path is supplied; an upstream comment identifies storing multiple candidate paths and selecting a best path as future work.

Accordingly, this dossier does **not** describe MeshCore's current path selection as shortest-path, lowest-airtime, highest-SNR, ETX, or other metric routing. The inspected upstream implementation supports opportunistic flood discovery plus cached explicit paths, with first-arrival behavior in the relevant discovery path.

## Duplicate and path controls

The forwarding path uses the repository's seen-packet table to avoid retransmitting already-seen traffic. Flood path growth is bounded by `MAX_PATH_SIZE`; direct forwarding consumes path hashes hop by hop. `Packet::isValidPathLen()` rejects the reserved hash-size encoding and any encoded path whose byte size exceeds the fixed path buffer.

These are useful defensive properties for constrained firmware, but this run did not fuzz malformed packets or prove every caller validates packet lengths before field access.

## Why this component is Gold

The routing core is unusually reusable because it combines:

- a compact bounded packet format;
- flood-based route discovery;
- explicit source-style direct paths after discovery;
- hop-by-hop path consumption;
- duplicate suppression hooks;
- path-return packets that can piggyback ACK/application data;
- fixed-size embedded data structures;
- an MIT license.

The design is especially relevant to low-bandwidth half-duplex packet radio where repeated network-wide flooding is expensive but maintaining a heavy proactive routing protocol may also be undesirable.

## Verification performed

Repository-native inspection covered:

- `docs/packet_format.md`;
- `src/Packet.cpp`;
- `src/Mesh.cpp`;
- `src/helpers/BaseChatMesh.cpp`;
- repository code search for path-return and direct/flood call sites.

The source directly supports the framing, path-validation, flood-path append, direct next-hop consumption, path-return, cached `out_path`, and first-arrival findings above.

GitHub Gold did **not** compile or execute MeshCore, run native tests, flash hardware, transmit radio packets, benchmark route convergence, measure airtime, simulate packet loss/collisions, or independently security-audit the protocol.

## Licensing

MeshCore is MIT-licensed. No upstream implementation source was copied into GitHub Gold; this dossier records architecture and exact upstream locations for further study.

## Risks / limitations

- First-arrival flood discovery is not proof of best-path selection.
- Cached paths can become stale as topology changes; higher-level retry/recovery behavior deserves separate tracing.
- Path hashes are deliberately compact and therefore should not be described as globally collision-free identities.
- Maximum practical hop count depends on encoded hash size and the 64-byte path ceiling, not merely the six-bit count field.
- RF collision, hidden-node, congestion, duty-cycle, antenna, terrain and regional-regulation behavior are outside this source-only verification.
- Current protocol documentation labels later payload versions as future versions; do not treat them as shipped protocol revisions.

## Relationship to the existing MeshCore dossier

The project-level dossier establishes MeshCore as VERIFIED S-tier firmware/library. This file explains *why the routing core itself is technically interesting*: it turns flood-discovered path information into bounded explicit routes that later traffic can consume hop by hop.

## Strong follow-up leads

1. Trace stale-path failure, ACK timeout and flood fallback/re-discovery behavior.
2. Inspect `docs/kiss_modem_protocol.md` and the KISS modem example as a standalone interoperability component.
3. Inspect packet-table duplicate detection, retention and collision behavior.
4. Compare MeshCore route discovery with Meshtastic managed/flood routing and Reticulum path discovery without flattening their different network models.
5. Evaluate host libraries (`meshcore.js`, `meshcore_py`, CLI) as separate reusable components.