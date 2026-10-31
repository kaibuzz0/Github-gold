# Meshtastic vs MeshCore vs Reticulum — routing and recovery comparison

- **Research date:** 2026-09-22
- **Evidence:** VERIFIED (source-level comparison; no RF/hardware test performed by GitHub Gold)
- **Provisional Gold value:** S / 28
- **Category:** mesh networking / LoRa / resilient communications / routing architecture

## Executive result

These projects overlap in off-grid/resilient communications, but they solve routing at different layers and should not be treated as interchangeable implementations.

- **Meshtastic firmware** is a LoRa-device communications stack whose baseline delivery model remains managed flooding, with newer next-hop hints able to direct traffic when a unique currently reachable neighbor can be resolved; source explicitly falls back to managed flooding when a stored hint is ambiguous or no longer maps to a direct neighbor.
- **MeshCore** uses a compact flood-then-directed-path model. The first contact path can be learned from flooded traffic; later messages can use the cached explicit path. The official Python host stack adds a practical recovery policy: ACK-aware retries, path reset, flood fallback, and subsequent reciprocal path learning that can restore a direct route.
- **Reticulum** is a broader transport/network stack rather than LoRa firmware. It maintains destination paths, transports announces and path requests across heterogeneous interfaces, and expires/gates path-discovery state. Its architecture is therefore closer to a general resilient network layer than to either radio firmware project.

## Comparison

| Dimension | Meshtastic | MeshCore | Reticulum |
|---|---|---|---|
| Primary abstraction | LoRa mesh firmware/ecosystem | Lightweight packet-radio mesh firmware | General-purpose resilient network stack |
| Baseline discovery/delivery | Managed flooding | Flood discovery, then explicit directed path | Destination announces + path discovery/request machinery |
| Learned/direct optimization | `NextHopRouter` can emit a stored next-hop hint when it resolves to a unique reachable direct neighbor | Cached `out_path` is used for directed traffic | Transport maintains path state toward destination hashes |
| Failure fallback | Source shows ambiguous/stale next-hop hints falling back to managed flooding | Official Python stack can retry, reset path, then flood; flooded response can relearn a direct route | Path state and in-flight path requests are timed/managed by transport; discovery can be requested again when needed |
| Route metric characterization | Do not describe baseline managed flooding as shortest-path routing | Do not describe upstream path selection as shortest-path/ETX; prior source inspection found first-arriving flood behavior rather than metric-optimal selection | Do not reduce Reticulum to a single LoRa hop metric; it spans heterogeneous interfaces and transport-node paths |
| Scope | Embedded radio + clients/services | Embedded radio + host libraries/clients | Network/transport layer across radio, serial, TCP/UDP and other interfaces |
| Root license | GPL-3.0 | MIT | Custom Reticulum License with use restrictions |
| Best GitHub Gold reuse mode | Study routing/embedded architecture; GPL obligations before covered code reuse | Strong permissive component-study/reuse candidate with attribution | Catalog/link and architecture study; do not copy/adapt without careful custom-license review |

## Meshtastic evidence

Official firmware source inspected on 2026-09-22 includes `src/mesh/NextHopRouter.cpp`. The current code validates a stored `next_hop` against a **unique, currently reachable direct neighbor**. Its own comment explains that an ambiguous last-byte mapping could point at the wrong physical node, while a departed neighbor would direct traffic into a void; in either case the code chooses flooding and explicitly notes that managed flooding still delivers.

This is useful because it prevents an overly simplistic description of current Meshtastic as “only flooding.” The safer description is: managed flooding remains the robust fallback/delivery substrate, while next-hop routing can reduce unnecessary flood behavior when the firmware has a usable neighbor hint.

Upstream: https://github.com/meshtastic/firmware/blob/master/src/mesh/NextHopRouter.cpp

## MeshCore evidence

The preceding GitHub Gold dossiers traced the recovery chain through upstream firmware plus the official Python host stack:

1. unknown contact path causes flood delivery;
2. returned path information can populate `out_path`;
3. later messages use the directed path;
4. an ACK timeout in the base firmware does not by itself perform automatic flood recovery;
5. official Python `meshcore_py.send_msg_with_retry()` supplies higher-layer retry policy and can reset a failed path and fall back to flood;
6. flood-delivered text can return reciprocal path information plus ACK;
7. the sender can therefore relearn a direct path after recovery;
8. route reset/relearning is scheduled for contact persistence by companion firmware.

The important systems lesson is **layering**: MeshCore's firmware supplies the path primitives, while official host software can supply stronger retry/recovery policy.

Upstream: https://github.com/meshcore-dev/MeshCore

## Reticulum evidence

Official `RNS/Transport.py` contains explicit path tables, path requests, announce handling, request gating, expiry and timeout behavior. Current source inspection found `inflight_path_requests` entries being removed after `PATH_REQUEST_GATE_TIMEOUT`, confirming that path-discovery state is actively bounded rather than assumed permanent.

Reticulum should therefore not be compared to MeshCore solely as another LoRa routing algorithm. Its useful architectural role is as a network layer that can route across heterogeneous interfaces and transport nodes, with LoRa/RNode being one possible bearer.

Upstream: https://github.com/markqvist/Reticulum/blob/master/RNS/Transport.py

## Licensing

### Meshtastic

The official firmware root `LICENSE` is **GNU GPL v3**. Covered code reuse/distribution must preserve the applicable GPL obligations.

### MeshCore

The official `license.txt` is the standard **MIT License** and requires preservation of the copyright and permission notice in copies or substantial portions.

### Reticulum

The current root license is a **custom Reticulum License**, not standard MIT. Although much of its wording resembles MIT, it adds restrictions including prohibitions on use in systems that purposefully harm humans and on use in creating AI/ML/language-model training datasets. Treat this as a material reuse caveat; GitHub Gold should catalog and link to upstream rather than copying implementation code by default.

## Practical selection guidance

- Choose **Meshtastic** when the priority is the mature Meshtastic hardware/client ecosystem and a flooding-based LoRa mesh with incremental routing optimizations.
- Choose **MeshCore** when the priority is a lightweight embedded flood-to-directed-path design, permissive MIT licensing, and explicit host-controlled retry/path-reset behavior.
- Choose **Reticulum** when the requirement is a bearer-agnostic resilient network layer that can bridge multiple interface types rather than only a single LoRa firmware ecosystem.

This is architectural guidance, not a claim that one project is universally superior. Network density, RF environment, airtime constraints, hardware, regulatory settings, client requirements, and topology can dominate real-world results.

## Verification boundaries

GitHub Gold inspected current repository-native source and license material and consolidated prior source-level MeshCore research. It did **not** compile any of the three projects, run their tests, flash radios, build a mixed test network, inject failures, measure delivery ratio, benchmark airtime, validate route convergence, or independently audit cryptography/security. No third-party implementation source was copied.

## Follow-up leads

1. Rotate out of mesh networking for the next discovery batch to preserve catalog breadth.
2. Revisit this comparison only when a material upstream routing change lands or hardware measurements become available.
3. Potential future interoperability lead: inspect projects that bridge Reticulum over MeshCore or Meshtastic, but score them separately and require clear licensing plus working evidence.
