# Syncthing relay admission test (`client.TestRelay`)

- **Upstream:** https://github.com/syncthing/syncthing/blob/main/lib/relay/client/methods.go
- **Related registry:** https://github.com/syncthing/syncthing/tree/main/cmd/infra/strelaypoolsrv
- **Category:** networking / relay infrastructure / service admission / health verification
- **Evidence:** VERIFIED (source-inspected; not executed by GitHub Gold)
- **Provisional Gold score:** 26/30 — S tier
  - Utility 5/5
  - Working evidence 4/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5
- **Language:** Go
- **License:** MPL-2.0 at Syncthing repository/package level; review imported dependencies before extraction

## Why this matters

The relay-pool dossier established that a candidate relay is actively tested before admission. This dossier resolves what that test actually proves.

`client.TestRelay` is not merely a TCP port check. It creates a real relay client using the tester's certificate, starts the client's control-channel service, derives the tester's DeviceID from that certificate, and then asks the same relay for a `SessionInvitation` targeting that DeviceID. Success therefore demonstrates a meaningful slice of the relay protocol's control/rendezvous path.

At the same time, it is narrower than an end-to-end data-plane test: `TestRelay` does not call `JoinSession`, does not establish the invited session socket, and does not proxy application bytes through the relay.

## Evidence chain

### 1. Tester identity comes from its certificate

`TestRelay` derives a Syncthing DeviceID from `certs[0].Certificate[0]`. It then constructs a relay client with `NewClient(uri, certs, timeout)` and starts `c.Serve(ctx)`.

A goroutine drains the client's invitation channel while the control client runs.

### 2. The test asks the relay to rendezvous with the tester itself

After a short initial delay (`sleep / 10`), the function repeatedly calls `GetInvitationFromRelay(ctx, uri, id, certs, timeout)`, where `id` is the tester's own certificate-derived DeviceID.

`GetInvitationFromRelay` requires a `relay://` URI, opens the relay through Syncthing's proxy-aware dialer, wraps it in TLS, performs the relay handshake/validation, sends a protocol `ConnectRequest` containing the target DeviceID, and expects either a `SessionInvitation` or a protocol `Response`.

If the invitation has no usable address, the client substitutes the relay connection's remote IP while retaining the invitation's port/key data.

### 3. Retry semantics distinguish ordinary propagation delay from other protocol failures

`TestRelay` retries when invitation lookup fails or when the relay returns the protocol's `ResponseNotFound`. A non-NotFound protocol response aborts immediately. The loop succeeds as soon as an invitation is returned; otherwise the last error is returned after the configured number of attempts.

This retry structure is consistent with the control client needing time to register before a self-targeted ConnectRequest can resolve it.

## What successful admission supports

A successful `TestRelay` provides source-level evidence that, under the tested configuration, the candidate can support:

- TCP reachability through the client's dial path;
- relay TLS setup and relay handshake/validation used by the client;
- creation and serving of a relay control client;
- registration of the tester's certificate-derived DeviceID with the relay;
- handling of a `ConnectRequest` for that registered DeviceID;
- production and return of a syntactically valid `SessionInvitation`;
- the retry/lookup path needed for registration propagation.

This is substantially stronger than admitting a relay based on an HTTP health endpoint or open TCP port alone.

## What it does **not** prove

`TestRelay` does not itself:

- call `JoinSession`;
- dial the invitation's session endpoint;
- send the invitation key as `JoinSessionRequest`;
- verify that two session participants are paired;
- transfer arbitrary application bytes through the relay;
- benchmark throughput, latency, fairness, bandwidth limiting, or sustained availability;
- fuzz protocol parsing or independently audit TLS/security behavior.

Therefore pool admission should be described as **control-plane/rendezvous functional verification**, not full end-to-end relay data-plane verification or a security audit.

## Reusable patterns

- self-rendezvous service test using a certificate-derived identity;
- exercising the real client/protocol path rather than a separate health-check API;
- bounded retry for eventual registration visibility;
- distinguishing expected `not found yet` state from hard protocol errors;
- admission gating based on protocol-level behavior before registry publication.

This pattern is reusable in discovery registries, rendezvous networks, federated service pools, TURN-like infrastructure, and other systems where an open port is insufficient evidence that a node implements the expected protocol correctly.

## Licensing

The inspected `lib/relay/client/methods.go` is part of Syncthing's MPL-2.0 codebase. GitHub Gold copied no upstream source. Any future extraction or adaptation must preserve applicable MPL notices and separately review imported dependencies.

## Verification performed by GitHub Gold

Performed:

- inspected current upstream `lib/relay/client/methods.go`;
- traced `TestRelay` into `GetInvitationFromRelay`;
- distinguished the tested invitation/control path from the separate `JoinSession` data-plane join path;
- compared the finding with the prior relay-pool admission dossier.

Not performed:

- did not compile or run Syncthing;
- did not execute `TestRelay`;
- did not register a relay with a live pool;
- did not establish or join a real relay session;
- did not transfer data through a relay;
- did not benchmark or security-audit the implementation.

## Caveats

- The exact TLS identity guarantee depends on the relay URI/handshake validation rules documented in the static-client and relay-pool identity dossiers; arbitrary unpinned relay URLs remain a separate trust case.
- A successful invitation proves the rendezvous/control path reached invitation generation, not that the resulting session socket can actually carry traffic end-to-end.
- Operational pool parameters (`sleep`, `timeout`, `times`) should be read at the pool call site before making claims about production retry duration.

## Strong next leads

1. Trace the pool's concrete `TestRelay` arguments to document production retry/timeout policy.
2. Inspect whether any upstream integration test continues from invitation into `JoinSession` and actual byte transfer.
3. Inspect permanent/default relay inputs for identity-pin coverage.
4. Trace registry endpoint parsing -> dynamic selection -> static pinned connection to complete the client-side provenance chain.
