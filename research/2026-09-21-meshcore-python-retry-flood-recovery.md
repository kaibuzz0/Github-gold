# MeshCore Python host stack — ACK retry, path reset, and flood recovery

- **Repositories:** https://github.com/meshcore-dev/meshcore-cli and https://github.com/meshcore-dev/meshcore_py
- **Organization:** meshcore-dev
- **Category:** Off-grid communications / MeshCore host tooling / Python / routing recovery
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** MIT (both inspected Python projects declare MIT; CLI root license inspected directly)
- **Inspection date:** 2026-09-21
- **Discovery source:** recursive follow-up from MeshCore firmware and MeshCore.js stale-route research

## Executive finding

The official Python host stack materially changes the stale-route conclusion from the lower-level firmware and JavaScript inspections. The `meshcore_py` library contains an explicit `send_msg_with_retry()` recovery state machine that waits for ACKs, retries direct sends, resets the cached path after a configurable attempt threshold, then continues via flood. `meshcore-cli` uses that primitive for its ACK-aware chat/message path.

This means MeshCore's ecosystem does have an automatic host-side direct-path failure -> path reset -> flood retry mechanism, but it lives in the Python host library rather than being guaranteed by the firmware base layer or the inspected JavaScript library.

## CLI surface

`meshcore-cli` is a terminal interface for MeshCore companion radios over BLE, TCP, or Serial. The current package metadata identifies version 1.6.4, Python >=3.10, MIT licensing, and a dependency on `meshcore >= 2.3.11` plus Bleak, prompt_toolkit, and requests.

The README exposes explicit route controls:

- `path <contact>` — display the cached path;
- `disc_path <contact>` — discover a new path;
- `reset_path <contact>` — reset the path to flood;
- `change_path <contact> <path>` — manually change a route;
- `trace <path>` — route tracing;
- per-contact timeout control;
- flood-scope controls.

It also supports scripting, JSON output, shell/file pipelines, interactive history/completion, contact management, channel echoes, and batch operations across contacts. These make the CLI useful as both an operator tool and an automation surface.

## Automatic retry behavior

The CLI's `msg_ack()` helper calls `mc.commands.send_msg_with_retry()` rather than implementing its own one-shot send. Its configured defaults are:

- `max_attempts = 3`;
- `flood_after = 2`;
- `max_flood_attempts = 1`.

Therefore the normal ACK-aware CLI path can make direct attempts first and escalate to flood rather than merely reporting a timeout.

## Library recovery state machine

The actual state machine lives in `meshcore_py/src/meshcore/commands/messaging.py`.

`send_msg_with_retry()`:

1. resolves as much of the destination public key as possible;
2. subscribes for ACK events **before** transmitting so an ACK queued immediately behind `MSG_SENT` is not missed;
3. assigns a distinct attempt number while preserving one message timestamp across attempts;
4. records the expected ACK code returned for every successful send attempt;
5. accepts a late ACK from any prior attempt as successful delivery;
6. derives an ACK wait from the radio-provided `suggested_timeout` unless the caller supplied an explicit timeout;
7. retries until configured attempt/flood limits are reached;
8. when `attempts == flood_after`, obtains a full key if needed, calls `reset_path()`, marks the local contact path as flood/unknown, and continues sending;
9. tracks flood attempts separately;
10. always unsubscribes its ACK listener in a `finally` block.

The library defaults are `max_attempts=3`, `max_flood_attempts=2`, and `flood_after=2`; the CLI intentionally overrides the flood-attempt limit to one.

## Strong working evidence

This behavior is not only inferred from comments. `meshcore_py` contains focused asynchronous unit tests using a fake companion radio plus the real event dispatcher.

The inspected tests cover:

- an ACK queued immediately behind `MSG_SENT` not being lost;
- a late ACK for an earlier attempt satisfying delivery;
- a dead direct route escalating to path reset/flood and using the flood-specific timeout;
- an explicit caller timeout applying to every attempt;
- retries sharing one timestamp;
- caller-supplied timestamps being preserved;
- already-flooding contacts stopping at the configured flood-attempt ceiling;
- unrelated ACKs being ignored;
- ACK subscriptions being removed after success and failure.

The flood-recovery test explicitly models a dead direct route, waits through two direct attempts, resets the path, receives an ACK on attempt 2 over flood, and asserts that the contact path state was changed to flood/unknown.

GitHub Gold did not execute these tests. They are upstream repository-native working evidence.

## Maintenance evidence

`meshcore-cli` was actively receiving commits on 2026-09-19. Recent inspected commits included a CLI option to wait for ACKs from command-line message sends and contact-list behavior changes. This is direct maintenance evidence close to the inspection date.

The Python library package inspected at the same time identifies version 2.3.14 and includes dedicated pytest/pytest-asyncio development dependencies.

## Why this matters

This resolves an important architecture boundary across the MeshCore ecosystem:

- the inspected firmware base layer exposes timeout hooks but does not itself guarantee automatic stale-route invalidation and flood retry;
- the inspected MeshCore.js host library exposes path reset and send-confirmation primitives but no equivalent automatic recovery state machine was found in that run;
- the Python `meshcore_py` library **does** implement explicit retry + ACK correlation + path reset + flood escalation;
- `meshcore-cli` consumes that Python recovery primitive for ACK-aware messaging.

Applications therefore should not assume identical retry semantics across all MeshCore host libraries. Recovery policy is partly a host-stack concern.

## Reusable components

High-value components for further study or reuse under MIT terms include:

- `send_msg_with_retry()` ACK/retry state machine;
- expected-ACK correlation across multiple attempts;
- early-ACK race handling;
- late-ACK acceptance;
- radio-suggested timeout handling;
- path-reset/flood escalation;
- event-subscription cleanup;
- BLE/TCP/Serial host transports;
- CLI JSON and scripting surfaces;
- route/path operator controls;
- fake-radio async testing pattern.

Any direct source reuse still requires preserving the MIT copyright/license notice and checking file/dependency-level notices.

## Caveats

- The retry mechanism is host-library behavior, not a statement that every MeshCore client implements the same policy.
- Resetting to flood can increase airtime/network load; retry limits and flood scope matter on constrained radio networks.
- The CLI and Python library have different default `max_flood_attempts` values.
- Passing a partial destination key can require a contact refresh before path reset can be performed with the full key.
- Unit tests use a fake radio; they are strong logic evidence but not RF/interoperability evidence.
- No independent security audit was performed.

## Verification performed

This run inspected:

- current `meshcore-cli` README;
- CLI package metadata and dependencies;
- CLI MIT license;
- current CLI source references for `reset_path`, `wait_ack`, `msg_ack`, and retry configuration;
- recent CLI commit activity;
- official `meshcore_py` repository metadata;
- Python package metadata;
- `send_msg_with_retry()` implementation;
- focused retry/flood unit tests;
- existing GitHub Gold PR state to avoid a duplicate dossier.

## Verification NOT performed

GitHub Gold did **not**:

- install either Python package;
- execute pytest;
- connect BLE, serial, or TCP hardware;
- transmit LoRa packets;
- induce a real stale route;
- measure RF airtime or congestion;
- validate path rediscovery across a live repeater network;
- independently security-audit ACK/path logic;
- copy upstream implementation source into GitHub Gold.

## Gold rationale

**Utility — 5/5:** practical terminal automation plus a reusable Python companion-radio API with explicit delivery recovery.

**Working Evidence — 5/5:** concrete implementation, focused async tests, examples, package metadata, and active upstream commits.

**Reusability — 5/5:** Python library, CLI/scripting interfaces, multiple transports, and permissive MIT licensing.

**Novelty — 4/5:** retry state machines are not novel alone, but ACK correlation plus constrained-radio path reset/flood escalation is technically useful and domain-specific.

**Documentation — 4/5:** the CLI is extensively documented and the library API is documented, though the cross-layer routing/recovery contract requires source inspection to fully understand.

**Maintenance — 5/5:** active September 2026 development and current package versions.

**Provisional total: 28/30 — S tier.**

## Next research queue

1. Compare Python retry defaults and semantics with official mobile clients.
2. Inspect whether successful flood delivery automatically teaches/persists a new direct path afterward.
3. Trace `reset_path` through companion protocol into firmware contact state.
4. Inspect KISS modem framing and interoperability as a separate reusable component.
5. Build a compact Meshtastic / MeshCore / Reticulum recovery-policy comparison dossier.
