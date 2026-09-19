# Syncthing relay testutil: manual end-to-end data-plane harness

- Upstream: https://github.com/syncthing/syncthing/tree/main/cmd/strelaysrv/testutil
- Component: `cmd/strelaysrv/testutil/main.go`
- Category: networking / relay infrastructure / verification harness
- Evidence: **VERIFIED** (source-inspected; upstream manual harness exists)
- Provisional Gold score: **25/30 (S tier)**
  - Utility 4/5
  - Working evidence 4/5
  - Reusability 4/5
  - Novelty 4/5
  - Documentation 4/5
  - Maintenance 5/5

## What it is

Syncthing ships a small command-line utility beside `strelaysrv` that can exercise more of the relay data plane than `client.TestRelay` alone. It loads a TLS certificate/key pair, derives the local Syncthing DeviceID, and exposes three operating paths: join a relay and wait for invitations, connect to a specified DeviceID through a relay, or invoke the narrower generic `client.TestRelay` check.

## Why it matters

The join/connect paths continue past rendezvous. The connector obtains a `SessionInvitation` using `GetInvitationFromRelay`, calls `client.JoinSession`, then passes the resulting `net.Conn` to `connectToStdio`. The joiner likewise receives invitations from a running relay client, calls `JoinSession`, and hands the connection to the same stdio bridge. `connectToStdio` reads bytes from the relay session to stdout and writes stdin bytes back to the session connection. This is therefore an upstream manual harness capable of exercising invitation -> session join -> bidirectional application-byte transfer when two suitable clients are operated against a relay.

This materially extends the evidence boundary established for `client.TestRelay`: the generic test stops at successful invitation acquisition, while this utility contains an explicit path for joining the invited data socket and moving real bytes through it.

## Important verification boundary

Source inspection proves that the harness exists and is wired for real session I/O. It does **not** prove that GitHub Gold executed it, that current CI automatically exercises this path, that every relay deployment passes it, or that the relay has been benchmarked/security-audited. The utility is interactive/manual in this inspection; no claim is made here of automated integration-test coverage.

The `-test` mode is also intentionally narrower: it invokes `client.TestRelay(ctx, uri, certs, 1s, 2s, 4)` and prints OK/FAIL. Full data-plane exercise requires the `-join` / `-connect` paths and participating endpoints.

## Useful implementation pieces

- certificate-backed DeviceID derivation for test peers;
- real relay client startup and invitation channel handling;
- `GetInvitationFromRelay` for connector-side rendezvous;
- `JoinSession` on both sides of the relay session;
- a compact stdio-to-`net.Conn` bridge for interactive byte-transfer testing;
- bounded client construction using a 10-second timeout.

## Requirements / platform

Go source within the Syncthing tree. Runtime use expects `cert.pem` and `key.pem` in the configured key directory and a reachable relay URL. The connect path also needs the target peer's DeviceID.

## License

`cmd/strelaysrv` carries a dedicated MIT license. The test utility imports Syncthing library packages; any extraction or redistribution of those imported components must review their own applicable licensing rather than assuming the command-level MIT notice automatically relicenses them.

No upstream source is copied into GitHub Gold.

## Verification performed by GitHub Gold

Source inspection only. GitHub Gold did not compile or run the utility, create certificates, launch two peers, operate a relay, transfer bytes, benchmark throughput, induce disconnects, or capture traffic.

## Discovery provenance

Recursive follow-up from the relay admission dossier while searching upstream for `JoinSession` call sites and evidence that continues beyond invitation acquisition.

## Strong next leads

1. Inspect whether automated upstream tests or CI invoke equivalent two-peer data-plane behavior rather than relying on this manual utility.
2. Trace `cmd/strelaysrv/listener.go` from `JoinSessionRequest` through `findSession` and `AddConnection` to confirm server-side pairing/error semantics against the client path.
3. Inspect `lib/connections/relay_dial.go` and `relay_listen.go` to map how production Syncthing hands joined relay sockets into its normal connection stack.
4. Determine whether the manual harness has documented operational procedures elsewhere in Syncthing's docs/manpages.