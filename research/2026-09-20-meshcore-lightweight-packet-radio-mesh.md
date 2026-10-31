# MeshCore — lightweight packet-radio mesh firmware/library

- Repository: https://github.com/meshcore-dev/MeshCore
- Organization: meshcore-dev (original copyright notice identifies Scott Powell / rippleradios.com)
- Category: mesh/radio communications; embedded systems; LoRa; emergency/off-grid communications; IoT
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

## What it is

MeshCore is a lightweight portable C++ library and firmware ecosystem for multi-hop packet routing over LoRa and other packet radios. Its design targets embedded devices and infrastructure-independent communication rather than requiring IP or a central server.

The repository supplies both reusable core code and concrete firmware/application roles: Companion Radio, KISS Modem, Simple Repeater, Simple Room Server, Simple Secure Chat and Simple Sensor. Companion firmware can expose a radio to host applications over BLE, USB/serial or Wi-Fi; the KISS example provides a serial KISS bridge; repeaters extend radio coverage; room servers provide a small shared-post/BBS role; and sensor examples demonstrate telemetry/alerting.

## Why it is Gold

MeshCore fills a useful middle position in the off-grid stack landscape. It is substantially lighter and more embedded-focused than Reticulum while exposing more developer-oriented packet-routing primitives and application examples than a simple radio messenger. The MIT license materially improves reuse potential.

Particularly useful surfaces for deeper study include:

- core packet/routing implementation under `src/` and `include/`;
- `examples/companion_radio` host-device bridge patterns;
- `examples/kiss_modem` and `docs/kiss_modem_protocol.md` for interoperability with KISS-aware host software;
- `examples/simple_repeater` for lightweight forwarding/routing behavior;
- `examples/simple_room_server` for low-bandwidth store/share patterns;
- `examples/simple_secure_chat` for embedded encrypted messaging design;
- `examples/simple_sensor` for low-bandwidth telemetry;
- board/variant definitions and PlatformIO build matrix;
- companion ecosystem libraries such as `meshcore-dev/meshcore.js`.

## Working evidence

Evidence inspected on 2026-09-20:

1. The official README documents supported developer examples, PlatformIO build workflow, prebuilt firmware flashing and multiple client/transport options.
2. Upstream documents a native PlatformIO unit-test command (`pio test --environment native --verbose`), establishing an explicit test surface. GitHub Gold did not execute it in this run.
3. GitHub releases show **v1.17.1** Companion, Repeater and Room Server firmware published in August 2026 with large target-specific artifact sets. GitHub exposes SHA-256 digests on release assets.
4. Release artifacts include board-specific `.bin`, `.uf2` and/or `.zip` outputs, providing stronger evidence than README-only build claims.
5. The repository received merged documentation work as recently as **2026-09-19**, after the August 2026 firmware release, indicating current maintenance.
6. The repository's release documentation states that GitHub Actions automatically builds track-specific firmware releases when companion/repeater/room-server version tags are pushed.

`VERIFIED` means repository-native evidence establishes maintained source, concrete application examples, automated release machinery and published firmware artifacts. GitHub Gold did **not** compile the project, run unit tests, flash hardware, transmit LoRa packets, reproduce range/power claims, or independently security-audit the protocol.

## Runtime / hardware

Development uses C++ with PlatformIO. Runtime hardware depends on the selected target and firmware role; upstream points users to its flasher-supported device matrix and explicitly names Heltec, RAK Wireless and other LoRa-based hardware families. Host interaction can use BLE, USB/serial or Wi-Fi depending on the companion firmware/board. RF frequency, power and duty-cycle legality remain jurisdiction-dependent.

## Architecture and engineering signals

The contribution guidance is unusually relevant for embedded reuse: upstream explicitly asks contributors to keep the architecture concise and avoid dynamic memory allocation except during setup/begin functions. That is a design-policy claim rather than proof that every code path is allocation-free, but it signals deliberate constrained-device engineering.

The current roadmap also makes unfinished work visible instead of presenting it as complete. Items still listed include standardized repeater/bridge transport codes, round-trip manual paths, multiple sub-mesh support, LZW message compression, dynamic coding rate and a V2 protocol design discussion. These should remain roadmap items, not cataloged as current capabilities.

## Licensing

`license.txt` is the standard MIT License, copyright 2025 Scott Powell / rippleradios.com. This is significantly easier to reuse than Reticulum's current custom restricted license. Attribution/license preservation is still required when copying substantial portions.

No third-party implementation code was copied into GitHub Gold during this run.

## Risks / limitations

- No independent range, battery-life, throughput, congestion or large-mesh benchmark was performed.
- No independent cryptographic/security audit was established in this run.
- Hardware behavior varies by radio, antenna, board and regional RF configuration.
- Several ambitious capabilities remain roadmap items rather than shipped functionality.
- The README still contains at least one legacy support link pointing at the older `ripplebiz/MeshCore` issue location; ecosystem naming/organization migration should be watched for stale references.
- Tactical/security use is mentioned upstream, but GitHub Gold catalogs the project for legitimate off-grid, emergency, interoperability, research and user-controlled networking uses.

## Meshtastic / Reticulum comparison

**MeshCore** is the lightweight embedded-routing option of the three: C++/PlatformIO, role-oriented firmware, KISS/companion bridges, repeaters and room servers, with a permissive MIT license.

**Meshtastic** is the larger LoRa messaging/telemetry firmware ecosystem with broad device/client support and GPL-3.0 licensing.

**Reticulum** is the higher-layer heterogeneous networking stack: it can span LoRa/RNode, packet-radio TNC/KISS, serial and IP transports while exposing identity, link, routing and reliable-transfer primitives to applications; its current custom license imposes additional use restrictions.

They overlap in off-grid communication but are not interchangeable. MeshCore is particularly attractive where constrained embedded implementation, simple role deployment and permissive reuse matter.

## Discovery provenance

Independent GitHub-first follow-up from the Meshtastic and Reticulum comparison work. A duplicate search of GitHub Gold returned no existing MeshCore entry before this dossier was created.

## Strong follow-up leads

1. Trace MeshCore's packet format and routing/path-selection implementation with source evidence.
2. Inspect the KISS modem protocol as an interoperability component.
3. Inspect `meshcore-dev/meshcore.js` and the Python CLI as host-side reusable libraries.
4. Compare cryptographic packet/session design with Meshtastic and Reticulum without assuming equivalent threat models.
5. Map supported board families and firmware roles from release/build configuration rather than relying only on marketing documentation.
6. Build a concise Meshtastic vs MeshCore vs Reticulum comparison dossier after the routing internals are understood.