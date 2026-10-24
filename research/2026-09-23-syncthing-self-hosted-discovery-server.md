# Syncthing `stdiscosrv`: self-hosted discovery infrastructure

- **Upstream:** https://github.com/syncthing/syncthing
- **Component:** `cmd/stdiscosrv`
- **Category:** local-first / synchronization / self-hosted infrastructure
- **Evidence:** VERIFIED (source-level; not independently deployed)
- **Provisional Gold score:** 29/30 — S tier
- **License:** MPL-2.0 (same repository; file headers inspected)
- **Discovery path:** recursive follow-up from the Syncthing BEP/discovery/relay dossier

## Why it matters

Syncthing ships its global discovery server in the same upstream repository as the synchronization engine. This means operators who need discovery across routed/private networks are not inherently dependent on the public Syncthing discovery service: the discovery-server component is available for private deployment.

This is especially valuable for local-first installations spanning VLANs, VPNs, sites, or other networks where local broadcast/multicast discovery is insufficient but a centrally reachable private rendezvous service is acceptable.

## Source-level verification

The upstream `cmd/stdiscosrv/README.md` explicitly identifies `stdiscosrv` as the global discovery server for Syncthing.

The current `cmd/stdiscosrv` source tree contains the server implementation plus dedicated API and database tests. Inspected files include:

- `main.go` — process configuration, TLS/HTTP listener, database service, optional replication, metrics and shutdown handling.
- `apisrv.go` / `apisrv_test.go` — discovery API and tests.
- `database.go` / `database_test.go` — discovery record storage and tests.
- `amqp.go` — optional AMQP-backed replication path.
- `stats.go` — server statistics/metrics support.

The current CLI/source exposes operational controls for:

- certificate and key files;
- HTTPS operation or plain HTTP behind an HTTPS reverse proxy;
- configurable listen address (default `:8443`);
- optional gzip response compression;
- configurable metrics listener with Prometheus `/metrics` handler;
- database directory and flush interval;
- hidden S3-compatible database-backup settings;
- optional AMQP replication;
- configurable not-found response-rate controls;
- graceful shutdown delay.

When not placed behind an HTTPS proxy, the server loads an X.509 keypair and can generate one when the configured certificate does not yet exist. The certificate is also converted into a Syncthing device ID in the startup path.

The implementation stores discovery data through an in-memory store backed by the configured database directory. Source constants show discovered addresses expire after two hours, while clients are given randomized reannounce/retry intervals.

## Reusable components / patterns

1. **Private discovery service** — useful for self-contained Syncthing infrastructure when public global discovery is undesirable.
2. **TLS-or-reverse-proxy deployment model** — native TLS or HTTP behind an external HTTPS terminator.
3. **Prometheus observability** — optional metrics endpoint can integrate with standard monitoring stacks.
4. **Replication hooks** — optional AMQP replication supports multi-instance architecture.
5. **Database backup plumbing** — source includes optional S3-compatible backup configuration.
6. **Rate controls** — separate desired rates for not-found responses to previously seen and unseen device IDs.

## Architecture context

`stdiscosrv` solves address discovery, not file synchronization itself. Syncthing peers still establish their own authenticated peer connection and exchange data through the Block Exchange Protocol. A private discovery server therefore acts as rendezvous/address infrastructure rather than a file relay or storage server.

For a simple same-LAN installation, static addresses and/or local discovery may make `stdiscosrv` unnecessary. Its value rises when peers cross network segments where local discovery packets do not propagate.

## Caveats

- GitHub Gold did **not** build or execute `stdiscosrv`.
- No private discovery instance was deployed.
- API/database tests were inspected as upstream evidence but were not executed by GitHub Gold.
- TLS enrollment, reverse-proxy configuration, S3 backup, AMQP replication, rate limiting and Prometheus metrics were not exercised.
- This dossier does not claim that a private discovery service by itself traverses NAT/firewalls; peers must still have a viable direct or relay connection path.
- MPL-2.0 obligations apply to covered source files and modifications; preserve notices and review the license before redistributing modified implementation files.

## Verification performed

Repository-native source inspection only. The upstream README, `cmd/stdiscosrv` tree and current `main.go` were inspected to distinguish implemented capabilities from documentation claims. No runtime verification was performed.

## Next leads

- Inspect `cmd/strelaysrv` private relay deployment and pool-registration controls.
- Determine how a Syncthing client is configured to use only private discovery/relay infrastructure and disable public infrastructure.
- Investigate failure behavior when private discovery is unavailable but peers have cached/static addresses.
- After the private-relay pass, rotate research into another technical category to preserve catalog breadth.
