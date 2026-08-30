# SoapyRemote — stream framing, RPC call path, and service resource boundary

- **Upstream:** https://github.com/pothosware/SoapyRemote
- **Author / Org:** Pothosware / Josh Blum and contributors
- **Category:** SDR / networking / remote hardware control / stream transport / SoapySDR interoperability
- **Evidence:** VERIFIED
- **Candidate score:** retain provisional **24 / 30 — A tier**
- **License:** Boost Software License 1.0
- **Research date:** 2026-08-29
- **Discovery:** bounded follow-up from `research/2026-08-29-soapyremote-network-trust-boundary.md`

## Executive result

This pass closes three of the strongest open questions from the first SoapyRemote dossier:

1. **What is actually carried in the stream data plane?**
2. **How does UDP loss/reordering differ from TCP behavior?**
3. **Does a client control call really terminate in a local `SoapySDR::Device` method on the server?**

The answer is yes: the stream path has its own framed transport with sequence numbers, element/error counts, flags, and timestamps, while the control path serializes typed RPC messages separately and dispatches them into the server-side Soapy device object.

The UDP path can detect sequence discontinuities but, in the inspected implementation, it currently logs that condition rather than converting it into a distinct Soapy stream error. TCP instead reads a fixed header and then continues receiving until the declared frame length has arrived, so the stream framing is reconstructed over the reliable byte stream.

The packaged Linux service also favors streaming performance through real-time-priority allowance and very large socket-buffer sysctls, but the inspected unit does not itself demonstrate privilege dropping, connection/resource quotas, or common systemd sandbox directives. These are deployment observations, not vulnerability claims.

No local server/client session, RF test, packet-loss injection, fuzzing, throughput benchmark, or privilege test was performed.

## 1. Stream protocol selection and negotiation

`client/Streaming.cpp` exposes SoapyRemote-specific stream arguments including:

- `remote:format`
- `remote:scale`
- `remote:mtu`
- `remote:window`
- `remote:priority`
- `remote:prot`

The protocol selector accepts `udp`, `tcp`, or `none` in the public argument description. The normal network setup path explicitly supports UDP and TCP, while `none` uses the separate bypass setup RPC.

The current defaults in `common/SoapyRemoteDefs.hpp` are:

- endpoint MTU: **1500 bytes**;
- endpoint window: **42 MiB** on non-Apple systems and 16 KiB on Apple;
- endpoint direct-access buffers: **8**;
- per-socket-call buffer cap: **4096 bytes**;
- poll-loop timeout: **100 ms**.

For UDP, the client binds ephemeral stream and status sockets locally and sends the resulting ports to the server during stream setup. For TCP, the server returns a binding port and the client connects stream/status sockets to it.

The control RPC connection is therefore not the IQ stream itself: stream sockets are negotiated separately.

Relevant upstream files:

- https://github.com/pothosware/SoapyRemote/blob/master/client/Streaming.cpp
- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRemoteDefs.hpp

## 2. Stream frame format

`common/SoapyStreamEndpoint.cpp` defines an internal `StreamDatagramHeader` containing:

- total frame byte count;
- 32-bit sequence number;
- element count or Soapy error code;
- Soapy stream flags;
- 64-bit timestamp.

The same logical frame header is used in datagram and TCP modes.

This makes the data plane more structured than a raw socket full of IQ bytes. The framing can carry stream status/error information and time metadata alongside sample payloads.

The endpoint calculates its sample capacity from the configured transfer size, channel count, and sample element size, then lays channel buffers out behind the header in one transfer buffer.

Reusable design concept: **separate hardware-stream semantics from the underlying network transport by preserving sequence, flags, error codes, timestamps, and channel layout in an explicit frame header.**

Relevant upstream file:

- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyStreamEndpoint.cpp

## 3. UDP loss and reordering behavior

The receive endpoint compares each received frame's sequence number with `_lastRecvSequence`.

When the values differ, upstream labels the case:

> dropped or out of order packets

The current code then emits the `S` SSI/log indication and contains a TODO to return an error code rather than only a notification.

After the comparison it advances the expected sequence to `received_sequence + 1`.

Therefore the inspected UDP path has **loss/reordering detection**, but GitHub Gold should not describe it as transparent recovery, retransmission, or guaranteed in-order delivery.

No packet is reconstructed from another packet, and no retransmission mechanism was identified in this endpoint path.

This is an important catalog caveat for applications considering UDP because the API may continue delivering subsequent sample frames even after a sequence discontinuity rather than necessarily surfacing a dedicated stream error to the caller.

This source reading does **not** establish the exact behavior under every loss pattern, wraparound, kernel-drop scenario, or hardware driver. No packet-loss experiment was performed.

## 4. Flow control is explicit and sequence-window based

SoapyRemote uses the same stream header structure for flow-control acknowledgements.

On a receiving endpoint:

- the socket receive-buffer size is used to estimate a maximum number of in-flight sequences;
- an ACK communicates the receiver's last received sequence and the allowed in-flight sequence count;
- further ACKs are triggered as receive progress crosses a calculated window threshold.

On a sending endpoint, `waitSend()` blocks when the number of outstanding sequences reaches the advertised in-flight limit and waits for additional ACKs before allowing more traffic.

This is not TCP congestion control. It is an application-level SoapyRemote flow-control window built on top of the stream socket behavior and used for both transport modes through the endpoint abstraction.

Reusable component idea: **receiver-advertised sequence windows tied to actual kernel socket-buffer capacity** can decouple application buffering from a fixed packet-count assumption.

## 5. TCP framing behavior

In non-datagram mode, `acquireRecv()` first reads exactly the fixed stream-header size using `MSG_WAITALL`. It then reads the byte count declared by that header and loops until the complete logical frame has arrived.

This means TCP's byte-stream semantics are converted back into SoapyRemote frame boundaries by the header length field.

On send, `releaseSend()` likewise loops until all bytes in a frame are sent; the implementation limits each socket send operation to `SOAPY_REMOTE_SOCKET_BUFFMAX` bytes.

Therefore a useful high-level distinction is:

```text
UDP: one datagram-oriented frame transfer, sequence discontinuities can be observed
TCP: reliable byte stream, logical SoapyRemote frames reconstructed using header length
```

GitHub Gold does not claim that TCP is always operationally superior: latency, head-of-line blocking, RF sample-rate demands, network behavior, and device-specific buffering can change the tradeoff.

## 6. Status path is separate from sample data

`SoapyStreamEndpoint` has a distinct status socket and status-frame helpers.

Status records reuse the frame header fields to carry:

- channel mask;
- status/error code;
- flags;
- timestamp.

This clean separation between sample data and asynchronous stream status is another reusable architectural pattern for remote hardware APIs.

## 7. Concrete RPC trace: `setFrequency()`

A current control call can be traced end to end without relying on README claims.

### Client

`client/Settings.cpp` implements:

```text
SoapyRemoteDevice::setFrequency(...)
  -> SoapyRPCPacker
  -> SOAPY_REMOTE_SET_FREQUENCY
  -> direction
  -> channel
  -> frequency
  -> kwargs
  -> send packed request
  -> wait for SoapyRPCUnpacker response
```

### Wire format

`common/SoapyRPCPacker.cpp` constructs a typed RPC message with:

- a protocol header word;
- RPC version;
- total message length;
- typed values;
- a protocol trailer word.

The current RPC version constant in `SoapyRemoteDefs.hpp` is `0x000400`.

The packer loops across socket sends until the complete message has been transmitted and caps each individual socket send operation to the project's defined socket-call maximum.

### Server

`server/ClientHandler.cpp` dispatches `SOAPY_REMOTE_SET_FREQUENCY`, unpacks direction, channel, frequency and kwargs, then calls:

```text
_dev->setFrequency(direction, channel, value, args)
```

It then returns the protocol's void response.

That `_dev` object is the locally instantiated SoapySDR device on the server side.

So the architecture is concretely:

```text
client Soapy API call
  -> typed SoapyRemote RPC
  -> network control connection
  -> server RPC dispatcher
  -> local SoapySDR::Device API
  -> underlying hardware driver
```

This confirms why network access to the control service must be treated as potential hardware-control access rather than simple remote observation.

Relevant upstream files:

- https://github.com/pothosware/SoapyRemote/blob/master/client/Settings.cpp
- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRPCPacker.cpp
- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRemoteDefs.hpp
- https://github.com/pothosware/SoapyRemote/blob/master/server/ClientHandler.cpp

## 8. Packaged systemd service boundary

The repository ships `system/SoapySDRServer.service.in` with:

- `ExecStart=.../SoapySDRServer --bind`;
- `KillMode=process`;
- `Restart=on-failure`;
- `LimitRTPRIO=99`.

The inspected unit does **not** itself contain directives such as:

- `User=` / `Group=`;
- `NoNewPrivileges=`;
- `ProtectSystem=`;
- `ProtectHome=`;
- `PrivateTmp=`;
- `RestrictAddressFamilies=`;
- `MemoryMax=`;
- `TasksMax=`;
- connection/session quotas.

This should not be converted into a claim about the effective privileges of every SoapyRemote package or deployment. Distribution packaging, drop-ins, containers, service managers, ACLs, udev rules, device permissions, firewalls, or administrator overrides can impose additional controls.

The narrower finding is that **the upstream service template itself is performance-oriented and minimal rather than a complete sandbox/resource-policy profile**.

Relevant upstream file:

- https://github.com/pothosware/SoapyRemote/blob/master/system/SoapySDRServer.service.in

## 9. Socket-buffer sysctl boundary

The repository also ships `system/SoapySDRServer.sysctl`, which raises:

- `net.core.rmem_max` to **104857600** bytes;
- `net.core.wmem_max` to **104857600** bytes.

The comments explicitly state that this is intended to accommodate the default client/server socket-buffer requests.

That is consistent with SoapyRemote's design goal of moving high-rate sample streams, but it reinforces that system-level networking configuration is part of the operational architecture.

This file changes maximum permitted kernel socket-buffer sizes, not the amount that every connection necessarily allocates immediately.

Relevant upstream file:

- https://github.com/pothosware/SoapyRemote/blob/master/system/SoapySDRServer.sysctl

## 10. Maintenance check

The current upstream `master` head inspected in this pass is commit:

`40c3ef9053b63885b7444ce7e9ef00d2c7964c9d`

from **2025-10-09**, `Update for compat with newer CMake`.

No newer upstream source commit was found during this pass. This supports retaining the previous Maintenance score rather than increasing it.

## Score decision

Retain the existing **24 / 30 — A tier** provisional score.

This deeper transport analysis increases confidence in the project's technical value but does not justify a score increase because:

- formal release metadata remains weak/stale compared with source activity;
- the stock network trust boundary still depends significantly on deployment controls;
- UDP discontinuity handling is detection-oriented rather than recovery-oriented in the inspected endpoint path;
- no new GitHub Gold runtime verification was performed.

## Reusable components / design patterns worth cataloging

- explicit SDR stream frame header with sequence/flags/time/error semantics;
- receiver-advertised application-level flow-control window;
- transport-independent sample endpoint abstraction for UDP/TCP;
- split sample and status sockets;
- typed RPC packer/unpacker with versioned header/trailer framing;
- generic server dispatch directly into an abstract hardware API;
- stream format conversion/scale negotiation;
- remote MTU/window configuration;
- service-level real-time scheduling allowance;
- system socket-buffer tuning for high-rate streams.

## Caveats and verification boundary

GitHub Gold did **not**:

- build SoapyRemote;
- launch `SoapySDRServer`;
- connect a Soapy client;
- inject UDP loss or reordering;
- validate TCP recovery/latency;
- measure IQ throughput;
- test multiple simultaneous streams or clients;
- verify Linux scheduling priority at runtime;
- inspect downstream distro service overrides;
- test an SDR;
- fuzz RPC or stream parsers;
- perform a security assessment.

All findings above are source-level observations from the current upstream repository and are deliberately scoped that way.

## Related GitHub Gold research

- `research/2026-08-29-soapyremote-network-trust-boundary.md`
- `research/2026-08-29-soapysdr-core-abstraction.md`
- `research/2026-08-29-gnuradio-gr-soapy-integration.md`
- `research/2026-08-29-soapyplutosdr-libiio-bridge.md`
- `research/2026-08-28-libiio-iiod-remote-boundary.md`

## Strong next leads

1. Inspect `analogdevicesinc/libad9361-iio` as the RF-specific helper layer between SoapyPlutoSDR and libiio.
2. Compare SoapyRemote stream/control architecture with UHD's network transport and libiio `iiod`.
3. Inspect current SoapyRemote issues for performance, IPv6, protocol-version and device-locking caveats.
4. Determine whether existing automated tests exercise stream framing/loss behavior or only build/module registration.
5. After the bounded SDR stack is complete, broaden to another technical category rather than continuing indefinite depth on one ecosystem.
