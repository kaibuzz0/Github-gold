# SoapyRemote — remote SDR control and network trust boundary

- **Upstream:** https://github.com/pothosware/SoapyRemote
- **Author / Org:** Pothosware / Josh Blum and contributors
- **Category:** SDR / networking / SoapySDR / remote hardware control / interoperability
- **Evidence:** VERIFIED
- **Provisional Gold score:** 24 / 30 — **A tier**
  - Utility: 5
  - Working evidence: 4
  - Reusability: 5
  - Novelty: 4
  - Documentation: 3
  - Maintenance: 3
- **License:** Boost Software License 1.0
- **Research date:** 2026-08-29
- **Discovery:** recursive follow-up from SoapySDR / SoapyPlutoSDR / GNU Radio `gr-soapy` research

## Executive assessment

SoapyRemote is the network bridge for the SoapySDR device abstraction. It lets a client-side SoapySDR application discover and instantiate SDR devices exported by a remote `SoapySDRServer`, then forwards the generic SoapySDR control and streaming interfaces across the network.

This makes it more than an IQ sample relay. The RPC surface includes hardware-changing operations such as gain/frequency/sample-rate/bandwidth controls, clock/time configuration, register writes, settings, GPIO, I2C, SPI, UART, stream activation, and other capabilities exposed by the underlying Soapy driver. Therefore the server should be treated operationally as a **remote hardware-control endpoint**.

The project is technically valuable and highly reusable, but the inspected stock server path should not be assumed to provide an authenticated/encrypted network security layer. Deployments should establish their own trust boundary through interface binding, network segmentation, firewalling, VPN/overlay transport, SSH tunneling, or another authenticated wrapper when remote access crosses an untrusted network.

This is a deployment-boundary observation, not a vulnerability claim.

## Architecture

Typical path:

```text
SDR application
  -> SoapySDR
  -> SoapyRemote client module
  -> TCP RPC control plane + stream transport
  -> SoapySDRServer
  -> local SoapySDR driver
  -> physical SDR
```

For the Pluto stack researched in this branch:

```text
GNU Radio
  -> gr-soapy
  -> SoapySDR
  -> SoapyRemote
  -> network
  -> SoapySDRServer
  -> SoapyPlutoSDR
  -> libiio / libad9361
  -> Pluto-class SDR
```

## Source-level findings

### 1. Server binds broadly by default

`server/SoapyServer.cpp` constructs the default server URL using `::` when IPv6 is supported or `0.0.0.0` otherwise. If no service is specified, it uses the default SoapyRemote service. The server binds the resulting socket, calls `listen()`, and starts both SSDP and DNS-SD publication/discovery helpers.

The bundled man page states that `--bind` without an explicit IP binds the default port on **all local network addresses**. It documents the default port as **55132**.

Relevant upstream files:

- https://github.com/pothosware/SoapyRemote/blob/master/server/SoapyServer.cpp
- https://github.com/pothosware/SoapyRemote/blob/master/server/SoapySDRServer.1
- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRemoteDefs.hpp

### 2. One handler thread is created per accepted control client

`server/ServerListener.cpp` accepts a client socket, allocates handler state, and creates a new `std::thread` running `SoapyServerThreadData::handlerLoop()` for that client. Completed handlers are removed on later listener iterations.

The inspected source does not show a fixed worker-pool size or explicit application-level concurrent-client ceiling in this listener. `SOAPY_REMOTE_LISTEN_BACKLOG` is 100, but that is a socket listen backlog rather than an active-session quota.

This is a resource-model observation only; no exhaustion/load testing was performed.

Relevant upstream files:

- https://github.com/pothosware/SoapyRemote/blob/master/server/ServerListener.cpp
- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRemoteDefs.hpp

### 3. The RPC control surface is broad

`common/SoapyRemoteDefs.hpp` defines RPC calls covering, among other areas:

- device discovery / make / unmake;
- channel and duplex information;
- setup / activate / deactivate / close stream;
- antenna selection;
- DC/IQ correction controls;
- gain and gain-mode controls;
- center/component frequency controls;
- sample-rate and bandwidth controls;
- clock source/rate and hardware-time controls;
- sensors;
- register reads **and writes**;
- device/channel settings;
- GPIO reads/writes/direction;
- I2C read/write;
- SPI transactions;
- UART read/write.

Therefore network access to a SoapyRemote server can imply access to whatever subset of those capabilities the underlying hardware plugin implements. It should not be described as read-only telemetry.

Relevant upstream file:

- https://github.com/pothosware/SoapyRemote/blob/master/common/SoapyRemoteDefs.hpp

### 4. Streaming is configurable independently of the RPC surface

The common definitions expose stream arguments including:

- `remote:format`
- `remote:scale`
- `remote:mtu`
- `remote:prot`
- `remote:window`
- `remote:priority`

The stream protocol selector explicitly supports TCP or UDP. The default endpoint MTU is 1500 bytes, and the non-Apple default socket/window size is 42 MiB. This separation is useful for applications that need generic hardware control but must tune data-plane behavior for latency or throughput.

### 5. Discovery is part of the design

The server publishes itself through SSDP and DNS-SD/mDNS support. The 2024 maintenance history added an `ENABLE_AVAHI` build option, so Avahi integration can be controlled at build time.

This makes SoapyRemote useful for automatically locating SDR servers on trusted local networks, but discovery itself should not be confused with authorization.

### 6. Security boundary observed in inspected stock path

The inspected `SoapySDRServer` command-line interface exposes `--bind` and `--help`. The server accepts the resulting RPC socket and hands it to the client handler. Repository searches and the inspected server/common sources did not identify a stock TLS certificate, password, token, or client-authentication layer in this path.

Do **not** generalize that observation into a claim that SoapyRemote cannot be deployed securely. It can be placed behind external authenticated/encrypted transport or restricted to trusted interfaces/networks. The finding is specifically that the inspected stock RPC server should not itself be presumed to establish that boundary.

### 7. Timeout and buffering primitives exist

The shared definitions use a 100 ms socket poll-loop timeout and cap individual packer/unpacker socket calls at 4096 bytes. These are useful robustness primitives, but they are not equivalent to a maximum client-session lifetime or an admission-control policy.

## Working evidence

Evidence inspected:

- repository is public, unarchived, and identifies BSL-1.0 licensing;
- source contains the client, server, common RPC, discovery, streaming, system-service and build surfaces;
- CI builds SoapyRemote in Release and Debug configurations across Linux, macOS, Windows, and FreeBSD matrices;
- CI installs the resulting module and executes `SoapySDRUtil --check=remote` to verify module registration;
- a 2025-10-09 commit updated compatibility with newer CMake;
- 2024 commits include Avahi configuration support and sample-conversion fixes.

Verification boundary:

- GitHub Gold **did not** build SoapyRemote locally;
- did not launch `SoapySDRServer`;
- did not connect a remote client;
- did not transmit IQ data;
- did not test an SDR;
- did not benchmark throughput or latency;
- did not perform penetration, fuzz, DoS, or resource-exhaustion testing.

The VERIFIED label is based on concrete upstream source/build/CI evidence for the project and module-registration path, not on a GitHub Gold physical/network execution test.

## Release / maintenance caveat

The repository metadata shows the latest inspected commit on `master` at **2025-10-09** (`Update for compat with newer CMake`). The GitHub Releases API returned no release objects during this pass.

`Changelog.txt` still labels **0.6.0** and **0.5.3** as pending, while the last dated changelog release is **0.5.2 (2020-07-20)**. Therefore current source activity and formal release/versioning should be treated as separate signals.

This is the main reason Maintenance and Documentation are not scored at 5.

## License / reuse

Root licensing is Boost Software License 1.0, a permissive license suitable for study and reuse subject to its notice requirements.

No third-party source code was copied into GitHub Gold in this pass.

## High-value reusable concepts

- generic RPC projection of a hardware-abstraction API;
- discovery + remote device factory integration;
- independent control-plane and sample-stream transport;
- selectable TCP/UDP stream transport;
- format/MTU/window negotiation;
- client-handler lifecycle accounting;
- transparent propagation of driver capabilities instead of vendor-specific client APIs;
- network publication via SSDP + DNS-SD.

## Caveats

- broad hardware-write capability increases the importance of deployment network trust;
- default all-address binding can expose the service beyond the intended interface if the host/network firewall is permissive;
- thread-per-client listener design makes OS/service resource controls relevant under high connection counts;
- plugin-specific behavior still depends on the server's local SoapySDR drivers;
- CI verifies build/registration but does not by itself prove every end-to-end hardware/network path;
- formal release metadata is weak compared with source-tree maintenance.

## Related GitHub Gold research

- `research/2026-08-29-soapysdr-core-abstraction.md`
- `research/2026-08-29-soapyplutosdr-libiio-bridge.md`
- `research/2026-08-29-gnuradio-gr-soapy-integration.md`
- `research/2026-08-28-libiio-hardware-interoperability.md`
- `research/2026-08-28-libiio-iiod-remote-boundary.md`

## Strong next leads

1. Inspect SoapyRemote client stream framing, loss/reordering handling, and TCP-vs-UDP behavior.
2. Inspect the systemd service file for privilege/sandbox/resource controls.
3. Trace one concrete SoapyRemote request from client packer through server dispatch into `SoapySDR::Device`.
4. Compare SoapyRemote's remote abstraction with UHD's network-device model and libiio `iiod`.
5. Check current issues for protocol-version, performance, IPv6, discovery, and security-related operational caveats.
