# libiio `iiod` remote trust-boundary research — 2026-08-28

## Scope

This dossier deepens the existing `analogdevicesinc/libiio` candidate by inspecting the current `iiod` network daemon as a remote hardware-control boundary.

- **Parent candidate:** `analogdevicesinc/libiio`
- **Evidence:** VERIFIED source-level architecture finding
- **Parent provisional Gold score:** **S / 27** — unchanged
- **Category:** remote instrumentation / SDR and sensor control / embedded systems / network protocol / defensive deployment review
- **Primary upstream files inspected:** `iiod/network.c`, `iiod/iiod.c`, `iiod/parser.y`, `man/iiod.1.in`, `iiod/init/iiod.service.cmakein`
- **License of inspected daemon source files:** SPDX `LGPL-2.1-or-later`; the manual uses GPLv2+-style documentation licensing. Continue file-level license review before reuse.

## Executive finding

`iiod` should be treated as a **remote device-control service**, not merely a sensor-data endpoint.

The current network daemon opens a TCP listener, binds to the wildcard address, accepts clients, and hands each accepted socket directly to the IIO command interpreter. The protocol exposed by that interpreter includes both read and mutation operations: device/channel/debug/buffer attribute writes, raw output-buffer writes, trigger changes, buffer-count changes, stream open/close, and timeout controls.

That means the network trust boundary can include the ability to change connected IIO hardware state, depending on the devices and kernel attributes exposed by the local context.

The inspected stock TCP path does **not show an authentication or TLS wrapper** between `accept4()` and the command interpreter. Repository search in the `iiod` area for TLS/SSL/authentication/authorization terms also returned no matching implementation in this pass. This is a source-level observation about the inspected current paths, not a claim that operators cannot protect `iiod` externally with network isolation, VPNs, tunnels, firewalls, service wrappers, or downstream integration.

## Network listener behavior

Current `iiod/network.c`:

1. creates an IPv6 TCP socket when available, falling back to IPv4;
2. uses wildcard bind addresses (`IN6ADDR_ANY` or `INADDR_ANY`);
3. listens with backlog 16;
4. accepts a client socket;
5. configures TCP keepalive and `TCP_NODELAY`;
6. passes the same accepted file descriptor as both input and output to `interpreter(...)`;
7. creates a worker thread for the client.

The daemon therefore does not default to loopback-only exposure at this layer.

The current man page documents the default network port as **30431** and documents `--port 0` for an ephemeral port. When Zeroconf/Avahi support is built, the network daemon can also advertise the selected service port.

### Operational implication

A deployment that only intends local-host access should not assume the daemon binds only to localhost. Exposure should be constrained by the host/network deployment if remote access is not intended.

## Remote protocol capability is read/write

The current parser explicitly exposes commands including:

- `PRINT` / `ZPRINT` — obtain context XML;
- `OPEN` / `CLOSE` — manage device streaming state;
- `READ` — read device, debug, buffer, and channel attributes;
- `WRITE` — modify device, debug, buffer, and channel attributes;
- `READBUF` — receive raw device data;
- `WRITEBUF` — send raw data to a device;
- `GETTRIG` / `SETTRIG` — inspect or change the device trigger;
- `SET <device> BUFFERS_COUNT <count>` — change kernel buffer count;
- `TIMEOUT` — change I/O timeout behavior;
- `BINARY` — switch protocol mode.

This is the most important trust-boundary fact: a reachable `iiod` client may have **control-plane and data-plane mutation capability**, not simply read access.

The exact physical consequence depends on the exposed IIO devices. For an ADC-only sensor, writes may be comparatively limited. For DAC, RF transceiver, DDS, gain, trigger, or other writable IIO devices, remote writes can affect active hardware configuration or output behavior.

GitHub Gold did not connect hardware or execute these commands, so this dossier does not claim a universal effect for every IIO target.

## Transport protection boundary

In the inspected current network implementation, the accepted TCP socket is handed directly to the interpreter. The path inspected here did not show:

- a TLS handshake;
- client certificates;
- shared-secret authentication;
- per-client authorization policy;
- protocol-native user identities or roles.

The main `iiod` option table likewise exposes debug, demux, USB, pipe-count, serial, port, and source-URI controls, but no obvious authentication or TLS options in the inspected source.

A repository search scoped to the `iiod` area for TLS/SSL/authentication/authorization terms returned no implementation hits in this pass.

### Verification boundary

This is **not** an independent penetration test and should not be converted into a vulnerability claim. It is a deployment-boundary observation from current upstream source:

> the stock network path inspected is plain TCP device-control transport, so confidentiality, peer authentication, and network admission should be treated as external deployment responsibilities unless another uninspected layer supplies them.

For untrusted or routed networks, a safer architecture would place the service behind an authenticated secure transport or a private overlay and restrict the listener with host/network policy. This is a general defensive deployment conclusion, not a claim about one required product or topology.

## Connection and availability controls

The current network code provides several transport-level robustness measures:

- TCP keepalive is enabled;
- idle probes begin after 10 seconds;
- probes repeat every 10 seconds;
- six failed probes are configured before declaring a dead peer;
- `TCP_NODELAY` is enabled;
- the listen backlog is 16;
- client allocation failures close the new connection rather than proceeding.

However, the inspected path starts a worker thread per accepted client and this file does not expose an obvious authentication gate or explicit per-source connection quota before worker creation.

This should be treated as a **follow-up availability/resource-control question**, not a demonstrated denial-of-service defect. The thread-pool implementation and OS/service limits need separate inspection before making stronger claims about maximum concurrent client behavior.

## Service-manager boundary

The current upstream systemd template launches `iiod` through `ExecStart` and supports additional options through `/etc/default/iiod`.

The inspected template does not itself specify directives such as:

- `User=` / `Group=`;
- `DynamicUser=`;
- `NoNewPrivileges=`;
- `ProtectSystem=`;
- `ProtectHome=`;
- `PrivateDevices=`;
- `IPAddressAllow=` / `IPAddressDeny=`.

This does **not** prove every packaged deployment runs with broad privileges: distributions, generated configuration, drop-ins, device permissions, containers, or integrators can add stronger restrictions. It does mean the upstream template itself should not be cited as evidence of privilege dropping or systemd sandboxing.

For a hardware-control daemon, the meaningful privilege question is ultimately which `/dev/iio:*`, sysfs/debug attributes, USB endpoints, and related resources the service account can reach.

## Discovery and network visibility

When built with Avahi support, the network daemon calls the DNS-SD advertisement path after it has begun listening. This is useful for zero-configuration lab and embedded discovery, but it also means discoverability and reachability should be considered together during threat modeling.

The man page's blank `ip:` form similarly describes network discovery when Zeroconf support is present.

The design is useful for controlled LANs and lab networks; it should not be interpreted as an authentication mechanism.

## Reusable architecture lessons

### 1. Separate hardware API from transport

The underlying libiio object model remains one of the project's strongest reusable ideas: applications work with contexts/devices/channels while the transport decides whether the hardware is local or remote.

### 2. Remote hardware APIs need an explicit trust layer

Because the same remote protocol exposes reads and writes, a reusable remote-I/O architecture should document separately:

- transport confidentiality;
- client identity;
- authorization scope;
- resource limits;
- device/attribute allowlists;
- auditability;
- service privilege.

These concerns are orthogonal to whether the hardware abstraction itself is well designed.

### 3. Discovery is not authorization

mDNS/Zeroconf can make instrumentation easy to find, but discovery should never be conflated with admission control.

### 4. Protocol capability should drive network policy

A service capable of DAC/RF/trigger/debug writes deserves a different deployment assumption from a telemetry-only sensor endpoint.

## Licensing boundary

The inspected `iiod/network.c`, `iiod/iiod.c`, and parser source carry SPDX `LGPL-2.1-or-later` headers. The manual page has GPLv2+-style documentation licensing.

This reinforces the parent dossier's rule: libiio reuse must be evaluated at component/file level. No third-party source was copied into GitHub Gold.

## Verification performed

GitHub Gold inspected current upstream source and documentation for:

- network socket creation/bind/listen/accept behavior;
- default port documentation;
- client handoff to the interpreter;
- parser-level command capabilities;
- daemon command-line options;
- upstream systemd service template;
- targeted repository search for TLS/auth-related implementation terms.

Not performed:

- no build;
- no `iiod` deployment;
- no network capture;
- no protocol fuzzing;
- no authentication-bypass testing;
- no hardware connection;
- no concurrent-client stress test;
- no distribution-package comparison;
- no independent security audit.

## Candidate impact

**libiio remains VERIFIED / provisional S / 27.**

The new findings do not reduce the project's architectural value. Instead they make the catalog entry more useful by separating two claims:

- libiio/`iiod` is strong remote hardware-interoperability infrastructure;
- the inspected stock TCP daemon should be treated as a trusted-network/device-control boundary rather than assumed to provide protocol-native zero-trust security.

## Strong next leads

1. **`iiod/thread-pool.c` and resource limits** — determine actual concurrent-client/thread behavior and shutdown semantics before making availability claims.
2. **SoapySDR ↔ libiio modules** — map whether higher-level SDR abstractions inherit or change this remote trust boundary.
3. **pyadi-iio / libad9361** — inspect how RF-specific applications constrain or expose writable device attributes.
4. **GNU Radio IIO integration** — map source/sink and control-plane behavior around libiio.
5. **Zephyr `iiod`** — establish whether the embedded network implementation exposes the same command set and what resource/security controls differ.
6. **Distribution hardening** — compare upstream systemd template with major packaged units/drop-ins before making claims about real-world service privilege.
