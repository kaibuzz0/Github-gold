# SoapyRemote — network-transparent SDR device and stream transport

- Upstream: https://github.com/pothosware/SoapyRemote
- Project: SoapyRemote
- Research date: 2026-09-05
- Category: SDR / remote hardware access / RPC / sample streaming / discovery / interoperability
- Evidence level: VERIFIED
- Provisional Gold score: A / 24
- License: Boost Software License 1.0 (BSL-1.0)
- Primary language: C++
- Platforms evidenced in CI: Linux, macOS, Windows, FreeBSD
- Discovery source: recursive follow-up from the SoapySDR dossier; GitHub-first verification

## Executive finding

`pothosware/SoapyRemote` extends the SoapySDR abstraction across a network boundary. A server exports locally available SoapySDR devices, while the client side registers a `remote` SoapySDR module so applications can enumerate and operate those remote devices through the same API shape used for local radios.

Its strongest value is architectural rather than release freshness: it separates a control-plane RPC channel from high-volume sample-stream transport, supports automatic service discovery, negotiates remote stream formats, and can use UDP or TCP for sample transport while preserving the SoapySDR device interface above it.

This is useful Gold for remote radio stations, LAN-attached SDR appliances, headless receivers, distributed RF monitoring, and as a reference design for transporting a hardware abstraction API over a network.

## Why it matters

The preceding SoapySDR dossier established a stable application-to-hardware abstraction. SoapyRemote adds another boundary:

**SDR application -> local SoapySDR API -> SoapyRemote client -> control RPC + sample transport -> SoapySDRServer -> local SoapySDR driver -> radio hardware**

That design lets software written for local SoapySDR devices interact with radios physically attached to another machine without requiring every application to implement its own network protocol.

The repository is therefore valuable both as a whole project and as a source of reusable design patterns for:

- remote hardware virtualization;
- split control/data planes;
- stream-format negotiation and conversion;
- UDP/TCP sample transport;
- automatic LAN service discovery;
- cross-platform socket and interface handling;
- network forwarding of device metadata and control operations.

## Repository structure

The inspected source tree is divided into clear functional layers:

- `client/` — remote SoapySDR device implementation, discovery, control settings, logging, stream setup and client stream state;
- `server/` — listener, per-client request handling, server stream state, log forwarding and `SoapySDRServer` entry point;
- `common/` — RPC/socket/URL/discovery/network helpers shared by client and server;
- `system/` — service/install integration;
- `debian/` — packaging material.

This separation is a positive reusability signal because transport, discovery, client abstraction and server execution are not collapsed into one monolithic file.

## Network-transparent device model

The server man page describes `SoapySDRServer` as exporting locally available SoapySDR devices over the network. The client-side module then presents those server-side modules locally.

The default documented server port is **55132**, and the server can bind an explicit IPv4 or IPv6 address or all local interfaces.

That is a strong interoperability property: existing SoapySDR applications can remain above the device API rather than learning a second application-specific RF protocol.

## Control-plane RPC

Client code uses `SoapyRPCPacker` and `SoapyRPCUnpacker` around the control socket for remote operations. The inspected streaming implementation sends operation identifiers and structured parameters for calls such as:

- stream-format enumeration;
- native-format/full-scale queries;
- stream-argument metadata;
- stream setup;
- stream lifecycle operations.

The server side contains a large `ClientHandler.cpp` request dispatcher and corresponding stream/server state objects.

The reusable pattern is a relatively thin RPC mirror of a mature device API rather than a separate domain model.

## Stream transport and negotiation

`client/Streaming.cpp` is the strongest component inspected in this run.

It exposes remote-specific stream parameters including:

- `remote:format` — sample representation used across the network;
- `remote:scale` — sample scaling factor;
- `remote:mtu` — datagram transfer size;
- `remote:window` — kernel socket-buffer sizing;
- `remote:priority` — server forwarding-thread priority;
- `remote:prot` — `udp`, `tcp`, or `none`.

For normal network streams, setup distinguishes UDP datagram mode from reliable TCP mode. The client creates stream/status sockets, coordinates binding information through the control RPC channel, connects the transport endpoints, and instantiates a `SoapyStreamEndpoint` with channel count, element size, MTU and window parameters.

A `none` mode also exists for bypass/direct handling when network transport is not required.

## Format-conversion strategy

The client negotiates a remote stream representation separately from the application's local representation.

The inspected code prefers the remote device's native sample format when a supported conversion exists. Explicit conversion paths include combinations among:

- `CF32`
- `CS16`
- `CS12`
- `CS8`
- `CU8`

This can reduce network bandwidth compared with forcing every stream to floating-point complex samples.

The changelog records historical fixes to CS12/CF32 and CS16/CS8 scaling, which is important evidence that numeric conversion is a real correctness boundary rather than incidental glue.

## Discovery

The repository includes `DiscoverServers.cpp` and common discovery implementations for mDNS/DNS-SD and SSDP-style network discovery.

The common layer includes platform-specific mDNS implementations, including Apple and Avahi paths, plus network-interface enumeration helpers for Unix and Windows.

The changelog records:

- SSDP automatic server discovery;
- DNS-SD publishing/discovery through Avahi;
- macOS discovery timeout handling;
- IPv4/IPv6 discovery preferences;
- fixes for larger client counts and Avahi edge cases.

This makes discovery a meaningful subsystem rather than a hard-coded server-address example.

## Working evidence

The current GitHub Actions workflow builds both Debug and Release configurations across a broad historical matrix:

### Linux

Multiple GCC and Clang versions on Ubuntu 20.04/22.04 are configured. The workflow builds an early compatible SoapySDR, builds/installs SoapyRemote, then checks module registration using:

`SoapySDRUtil --check=remote`

### macOS

The workflow builds against a pinned SoapySDR revision and again installs SoapyRemote and checks remote-module registration.

### Windows

Visual Studio 2015, 2019 and 2022 configurations are represented for Win32/x64 combinations, followed by installation and `SoapySDRUtil --check=remote`.

### FreeBSD

FreeBSD 12.3/13.0/13.1 VM jobs build, install and check the remote module.

This is useful cross-platform build evidence, but it is narrower than the strongest projects in GitHub Gold: the inspected CI verifies compilation/installation/module registration, not an end-to-end client/server sample stream with a real or simulated radio.

## CI and reproducibility caveats

The workflow uses mutable action references such as:

- `actions/checkout@v2`
- `ilammy/msvc-dev-cmd@v1`
- `vmactions/freebsd-vm@v0`

Some SoapySDR dependencies are pinned to explicit commits, but the Linux path clones the `soapy-sdr-0.8.1` branch/tag reference and the overall workflow reflects older runner/toolchain generations.

This weakens reproducibility and supply-chain provenance compared with projects that pin Actions and dependencies to immutable SHAs.

## Maintenance and release status

Maintenance is significantly weaker than SoapySDR itself.

The latest commit observed on `master` during this run is:

- **2025-10-09 — `Update for compat with newer CMake`**

The previous visible commit is from January 2024, so activity is sparse rather than continuous.

`Changelog.txt` lists:

- **0.6.0 — pending**
- **0.5.3 — pending**
- **0.5.2 — 2020-07-20**

Therefore the latest completed release documented in the repository remains **0.5.2 from July 20, 2020**. This is the principal reason the candidate remains A-tier rather than S-tier despite its useful architecture.

## Security / trust boundary

This project should be treated as a remote-device transport for controlled networks, not assumed to be an internet-facing secure access gateway.

During this inspection, no TLS, certificate-authentication or user-authentication mechanism was identified in the root documentation, server man page, or targeted source search. The documented server can bind to all local interfaces, and its purpose is to export locally available SDR devices.

That means operators should not infer confidentiality, peer authentication, authorization or hostile-network resistance merely from the fact that the API is remote-capable. Safer deployment patterns include trusted LANs, host firewalls, VPN/overlay-network protection, or another authenticated tunnel.

This is an inspection finding, not a formal security audit; a deeper protocol review could uncover additional controls not identified here.

## Licensing

The README and root `LICENSE_1_0.txt` identify the project as Boost Software License 1.0.

The license permits use, reproduction, distribution, execution, transmission and derivative works subject to retaining required copyright/license notices for covered source distributions and derivatives, with the license's machine-executable object-code exception.

Inspected source files also carry `SPDX-License-Identifier: BSL-1.0`.

No upstream SoapyRemote source was copied into GitHub Gold.

## Gold score

Provisional score: **24 / 30 — A tier**

- Utility: **5/5** — solves a practical remote-hardware problem and composes directly with the SoapySDR ecosystem.
- Working Evidence: **3/5** — broad cross-platform build/registration CI exists, but no inspected end-to-end stream test or recent release artifact validates the complete network path.
- Reusability: **5/5** — clean client/server/common separation and a transparent SoapySDR module boundary.
- Novelty: **4/5** — remote RPC/streaming is established engineering, but transparent SDR-device virtualization plus adaptive sample transport is unusually useful.
- Documentation: **4/5** — wiki/manpage/changelog/source naming provide useful orientation, though the root README is minimal.
- Maintenance: **3/5** — a 2025 compatibility commit shows the repository is not abandoned, but release cadence and commit frequency are weak.

## Verification performed in this run

Inspected directly:

- repository metadata/default branch;
- root README;
- root BSL-1.0 license;
- repository directory structure;
- `client/Streaming.cpp`;
- client/common/server file inventories;
- `server/SoapySDRServer.1`;
- `.github/workflows/ci.yml`;
- `Changelog.txt`;
- recent commit history;
- targeted repository search for authentication/TLS-related mechanisms.

## Verification boundary

I did **not**:

- build or install SoapyRemote;
- run its CI locally;
- start `SoapySDRServer`;
- connect a SoapyRemote client;
- stream I/Q samples over UDP or TCP;
- test packet loss, jitter, latency or reconnect behavior;
- attach physical SDR hardware;
- validate every RPC opcode;
- test mDNS/Avahi/SSDP discovery;
- measure bandwidth savings from native sample formats;
- test malformed or hostile network inputs;
- prove the absence of undocumented authentication or encryption paths;
- perform a security audit.

All claims are limited to direct source/documentation/workflow/history inspection or clearly identified upstream evidence.

## Risks and limitations

- Sparse maintenance and an old completed release boundary increase downstream integration risk.
- CI validates module registration, not complete remote streaming behavior.
- Network transport introduces packet-loss, latency, MTU, buffering and NAT/firewall constraints absent from local SDR use.
- UDP favors low-latency streaming but is inherently loss-prone; TCP can trade loss behavior for head-of-line blocking/latency.
- Numeric sample-format conversion must remain scale-correct across both endpoints.
- Remote exposure of radio control should not be treated as authenticated/secure unless protected externally and verified for the actual deployment.
- SoapySDR ABI/version compatibility still applies on both ends.

## Strongest follow-up leads

1. Trace `SoapyStreamEndpoint` framing, sequence/status handling and packet-loss behavior in `common/`.
2. Inspect RPC serialization bounds and malformed-input handling in `SoapyRPCPacker` / `SoapyRPCUnpacker`.
3. Map SSDP + mDNS discovery trust assumptions and spoofing implications.
4. Build a future local loopback harness using SoapySDR's null/example driver to validate end-to-end control and sample transport without RF hardware.
5. Compare SoapyRemote with authenticated tunnel/overlay options such as Tailscale for a safer remote-radio deployment pattern.
6. Research `pothosware/SoapyMultiSDR` as the next recursive ecosystem candidate.

## Steward verdict

**Keep as VERIFIED A-tier Gold, with explicit deployment/security and maintenance caveats.**

SoapyRemote is valuable because it turns SoapySDR's local hardware abstraction into a network-transparent device model while keeping control RPC, stream transport, discovery and sample-format negotiation reasonably modular. It does not receive S-tier status because current evidence is mostly compile/module-registration CI, the latest completed documented release is from 2020, maintenance is sparse, and the inspected interfaces should not be assumed safe for direct exposure to untrusted networks.