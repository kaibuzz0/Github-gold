# MeshCore.js host routing controls and recovery boundary

- Upstream: https://github.com/meshcore-dev/meshcore.js
- Category: off-grid communications / JavaScript host library / MeshCore interoperability
- Evidence: VERIFIED (source-inspected; not runtime-tested by GitHub Gold)
- Provisional Gold score: 27/30 — S tier
- License: MIT
- Discovery path: recursive follow-up from MeshCore stale-route timeout/recovery dossier

## Question

Does the official JavaScript host library implement automatic retry or route invalidation above MeshCore firmware when a direct message times out, or does it expose primitives and leave recovery policy to the application/firmware?

## Findings

### 1. MeshCore.js is a reusable multi-transport companion protocol library

The official library targets MeshCore Companion Radio firmware. Its documented transports are browser Web Bluetooth and Web Serial plus Node.js TCP/Wi-Fi and USB Serial. This makes it a useful interoperability layer independent of any one UI.

### 2. The host protocol exposes explicit route-reset control

`Connection` implements the companion `ResetPath` command and exposes a public `resetPath(pubKey)` operation. The bundled browser UI exposes a user-facing `Reset Path` action for a contact.

This is important because stale-path invalidation is available to host applications as an explicit control even though the previously inspected firmware `BaseChatMesh::onSendTimeout()` path does not automatically clear the route.

### 3. Message sending delegates routing to the companion radio

The library's text-message command sends message type, attempt number, sender timestamp, the destination public-key prefix, and text to the radio. The bundled browser example calls `connection.sendTextMessage(contact.publicKey, message)` and logs the immediate response.

The host does not construct or select the contact's LoRa path for ordinary text sends in this API. That routing decision remains in the companion firmware/contact state.

### 4. The protocol exposes asynchronous delivery/path signals

The frame dispatcher recognizes `PathUpdated` and `SendConfirmed` push codes. `SendConfirmed` carries an ACK code and round-trip value, while `PathUpdated` identifies the contact whose path changed. These are useful building blocks for a richer client-side reliability policy.

### 5. No automatic send-timeout -> resetPath -> resend policy was found in the inspected official JS library

Repository search and inspection found the route-reset primitive, send-confirmation/path-update events, and ordinary send APIs, but no library-level state machine that automatically reacts to a failed direct send by resetting the route and retrying through flood discovery.

The bundled browser UI likewise provides `Reset Path` as an explicit user action rather than coupling it automatically to `sendMessage()`.

This means the current evidence supports a layered interpretation:

- firmware owns normal direct-vs-flood route selection from cached contact state;
- the host protocol can explicitly reset a contact path;
- the host receives delivery/path events that an application can use;
- MeshCore.js itself does not appear to impose an automatic stale-route recovery policy in the inspected path.

## Maintenance and reuse evidence

The repository is under the `meshcore-dev` organization and remained active in September 2026. The latest inspected commit was `9e76c51409c13c3ed0183ee1e9c1b380e671a038` on 2026-09-07, merging a stats-parsing fix. The README documents installation through the `@liamcottle/meshcore.js` npm package and includes browser/Node transport examples.

The project uses the standard MIT license, making the protocol/transport implementation comparatively straightforward to study and reuse with attribution.

## Gold interpretation

MeshCore.js is valuable as a compact, permissively licensed host interoperability layer. Particularly useful reusable pieces include:

- Web BLE transport;
- Web Serial transport;
- Node.js TCP/Wi-Fi transport;
- Node.js serial transport;
- companion command/frame encoding and decoding;
- contact synchronization and management;
- explicit path-reset control;
- path-update and send-confirmation event decoding;
- examples for scripted/bot operation.

The stale-route investigation also clarifies an architectural boundary: applications that require automatic retry after a dead cached path should implement that policy deliberately rather than assuming MeshCore.js supplies it.

## Verification performed

Source/documentation inspected on the upstream default branch:

- `README.md`
- `LICENSE`
- `src/connection/connection.js`
- `src/constants.js` through code-search evidence
- bundled `index.html` example UI
- recent upstream commit history

No upstream source was copied into GitHub Gold; only behavioral findings and references are recorded.

## Caveats

GitHub Gold did not install the npm package, run examples, connect to BLE/serial/TCP hardware, transmit LoRa messages, simulate an ACK timeout, or verify application behavior against a physical MeshCore companion. Repository search cannot prove that no external application built on this library implements stronger retry logic; this conclusion is limited to the inspected official `meshcore.js` repository.

## Strong next leads

1. Inspect `meshcore-cli` (Python) for retry/reset-path behavior and compare its host policy with MeshCore.js.
2. Inspect the official/primary mobile-client code if source is available; distinguish closed/mobile behavior from open host libraries.
3. Audit MeshCore KISS modem framing/interoperability as a standalone reusable component.
4. Audit duplicate-packet table retention/collision behavior under dense flooding.
5. Build a verified host-stack matrix: MeshCore.js vs Python CLI vs mobile clients, including transport support, path controls, ACK exposure, retries, and licensing.
