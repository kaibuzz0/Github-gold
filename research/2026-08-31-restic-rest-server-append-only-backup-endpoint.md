# restic/rest-server — append-only remote backup endpoint

- **Repository:** https://github.com/restic/rest-server
- **Organization:** restic
- **Category:** backup infrastructure / remote storage / HTTP services / append-only storage boundary
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 27 / 30
- **Provisional tier:** S
- **License:** BSD-2-Clause
- **Primary language:** Go
- **Discovery source:** recursive follow-up from the Restic architecture dossier
- **Research date:** 2026-08-31

## Executive summary

`restic/rest-server` is a compact HTTP server that implements Restic's REST backend API. Its value is not only that it provides a network endpoint for Restic repositories; it also exposes a relatively small, auditable storage boundary with append-only enforcement, optional per-user repository isolation, upload-integrity verification, quota controls, Prometheus instrumentation, Basic/.htpasswd authentication, proxy-delegated authentication, and TLS support.

The strongest GitHub Gold property is the append-only trust split. A client can retain credentials that are sufficient to create future backups while the server rejects deletion operations. That reduces the damage possible when a backed-up machine is compromised and the attacker obtains that machine's backup credentials. It does not protect against compromise of the backup server/storage account itself, so it should be understood as a credential/authorization boundary rather than immutable-storage magic.

The project has direct source evidence, targeted tests, cross-platform build checks, race-enabled tests, linting, a formal release, recent 2026 maintenance, and a permissive BSD license. The latest formal release inspected is older than the current source head, so maintenance receives a small deduction.

## Why it matters

Backup confidentiality and backup survivability are separate problems. Restic encrypts repository content client-side, but a normal fully privileged repository credential can still permit deletion. `rest-server` adds a server-side policy layer that can deny destructive operations even when the client credential is compromised.

Useful deployment roles include:

- hardened remote Restic targets;
- ransomware-resistant backup layouts;
- small self-hosted backup appliances;
- low-resource HTTP backup endpoints;
- private per-user backup services;
- backup targets behind restrictive firewalls where HTTP/S is easier to permit than SFTP;
- storage services that need simple repository quotas and observability.

It should be cataloged separately from `restic/restic`: Restic is the encrypted backup engine and repository client; `rest-server` is the remote repository service and policy boundary.

## Append-only enforcement

The server exposes `--append-only`, documented as permitting creation of new backups while preventing deletion and modification of existing backups.

Source inspection confirms that append-only state is passed from the top-level server into `repo.Options`. The repository handler checks this flag before destructive operations. For example, configuration deletion returns HTTP 403 when append-only mode is enabled, and the same option is used by blob-deletion handling.

Primary sources:

- https://github.com/restic/rest-server/blob/master/handlers.go
- https://github.com/restic/rest-server/blob/master/repo/repo.go
- https://github.com/restic/rest-server/blob/master/handlers_test.go

This is a useful security boundary because the enforcement point lives on the backup target rather than solely in the potentially compromised client.

### Threat-model boundary

Append-only mode does **not** make the underlying storage physically immutable. An attacker who gains filesystem/root/cloud-admin access to the server can still bypass application-level policy. The protection is specifically against destructive actions performed through the REST interface with ordinary client credentials.

For stronger ransomware resistance, retention/pruning administration should therefore be separated from routine backup credentials and ideally from the backed-up host itself.

## Authentication paths

`rest-server` exposes three authentication modes:

1. built-in `.htpasswd` authentication;
2. trusted reverse-proxy username headers;
3. explicit unauthenticated mode via `--no-auth`.

### `.htpasswd`

When authentication is enabled and proxy authentication is not configured, startup loads the configured `.htpasswd` file. If the file cannot be loaded, the server fails to initialize rather than silently disabling authentication. The README notes that this fail-closed behavior differs from older releases up to 0.9.7.

The README recommends bcrypt and supports bcrypt/SHA htpasswd entries, explicitly calling SHA insecure by modern standards.

### Proxy authentication

`--proxy-auth-username` delegates identity to a configured HTTP header such as `X-Forwarded-User`. The implementation accepts the header value as the authenticated username when present.

This is intentionally a trust transfer: upstream explicitly warns that the reverse proxy must guarantee the header cannot be forged by a client. Deployments therefore need the backend isolated so untrusted clients cannot bypass the authenticating proxy and inject the header directly.

### No-auth mode

`--no-auth` bypasses authentication entirely. This can be appropriate behind a separately enforced private transport/control plane, but it should not be treated as safe on an exposed listener merely because Restic encrypts backup data.

Primary sources:

- https://github.com/restic/rest-server/blob/master/mux.go
- https://github.com/restic/rest-server/blob/master/README.md

## Private repository isolation

The `--private-repos` mode binds the first repository path component to the authenticated username.

Source inspection shows that after authentication and path parsing, the server denies access unless the first folder component equals the authenticated username. The README documents that a user such as `foo` may access `/foo/` and subrepositories below it but not `/foobar/` or the root repository.

This is a simple but useful multi-user isolation primitive for small deployments.

Primary source:

- https://github.com/restic/rest-server/blob/master/handlers.go

## Path safety

The top-level handler separates repository-folder path components from Restic object paths and validates folder names before joining them to the configured storage root.

The `join` helper normalizes components and the handler rejects empty, `.` and `..` folder names. Repository object paths are separately constrained by a strict regular expression covering known Restic object classes and 64-character lowercase hex identifiers.

Primary sources:

- https://github.com/restic/rest-server/blob/master/handlers.go
- https://github.com/restic/rest-server/blob/master/repo/repo.go

This does not substitute for a dedicated security audit, but it is useful source-level evidence that path handling is intentionally constrained rather than directly concatenating arbitrary request paths.

## Upload-integrity verification

By default the server verifies that uploaded `data` content hashes to the object identifier supplied in the URL. Upstream added this behavior specifically to detect transmission errors and force Restic to retry corrupted uploads.

A `--no-verify-upload` escape hatch exists for very low-power devices, and the CLI help explicitly warns against enabling it unless necessary.

Primary sources:

- https://github.com/restic/rest-server/blob/master/repo/repo.go
- https://github.com/restic/rest-server/blob/master/CHANGELOG.md

This verification is valuable but should not be confused with repository authentication: Restic's encrypted repository format remains the primary end-to-end integrity/confidentiality mechanism, while this server-side check protects the transport/storage ingestion path against mismatched uploaded data objects.

## Quota and resource controls

The server supports `--max-size`, which initializes a quota manager over the configured repository storage path. The quota layer tracks repository space usage and wraps writes so the maximum repository size can be enforced.

The top-level server also exposes blob-operation metrics, Prometheus support, request logging, and CPU profiling hooks.

Primary sources:

- https://github.com/restic/rest-server/blob/master/mux.go
- https://github.com/restic/rest-server/blob/master/quota/quota.go
- https://github.com/restic/rest-server/blob/master/repo/repo.go

The quota mechanism is useful for preventing unbounded repository growth, but it is not a comprehensive denial-of-service sandbox. Operators still need network/process/container/filesystem resource controls appropriate to their deployment.

## TLS boundary

The server can terminate TLS itself and allows a minimum TLS version of 1.2 or 1.3.

Upstream warns that plain HTTP combined with Basic Authentication exposes usernames and passwords on the transport. Although Restic encrypts repository payloads client-side, that does not protect HTTP authentication credentials.

The README therefore distinguishes two concerns:

- repository payload confidentiality is already provided by Restic;
- HTTPS remains important for authentication credential protection and endpoint authenticity.

Primary source:

- https://github.com/restic/rest-server/blob/master/README.md

## Storage layout and interoperability

Upstream states that the server uses the same on-disk directory structure as Restic's local backend. That allows the same repository to be accessed locally and through the REST server.

This is an attractive interoperability property because `rest-server` is not introducing a proprietary server-only repository format. The server is primarily an HTTP/API and authorization layer over the familiar Restic repository layout.

## Working evidence

The repository includes targeted tests around server routing, authentication, append-only behavior, repository operations, quotas, metrics, and related helpers.

The current GitHub Actions workflow performs:

- Linux builds for Linux, Windows, and macOS targets;
- `go test -cover ./...`;
- a race-enabled Linux test job;
- testing on Go 1.24 and Go 1.25;
- `golangci-lint` on pull requests;
- `go mod tidy` consistency checks;
- changelog validation;
- an aggregate all-green status job.

Primary source:

- https://github.com/restic/rest-server/blob/master/.github/workflows/tests.yml

This is strong working evidence for a relatively small infrastructure service.

## Release and maintenance evidence

The latest formal release inspected is **v0.14.0**, published **2025-05-31**.

Current `master` is newer. The inspected head commit is from **2026-07-22**, adding timezone-data support, which demonstrates that the repository remained maintained after the most recent formal release.

Release:

- https://github.com/restic/rest-server/releases/tag/v0.14.0

Current source head inspected:

- https://github.com/restic/rest-server/commit/3aec7b45b9928811ef5f66d22ba06195097cd29a

The release/source gap is a modest maintenance caveat: operators consuming only tagged releases may not receive newer source changes until another release is cut.

## Runtime and build requirements

The current README states:

- Go **1.24 or newer** is required to build;
- the official Go compiler is the tested compiler;
- Restic client **v0.7.1 or newer** is required;
- a static binary can be built with `CGO_ENABLED=0 go build -o rest-server ./cmd/rest-server`.

The project also publishes container images and includes a Dockerfile, systemd service example, and a Docker Compose/Grafana example stack.

## License

The repository is licensed under the **BSD 2-Clause License**.

Source:

- https://github.com/restic/rest-server/blob/master/LICENSE

No source code was copied into GitHub Gold during this research pass.

## Verification performed in this run

GitHub Gold inspected:

- repository metadata;
- README;
- server routing/authentication source;
- repository handler source;
- append-only code paths;
- upload-integrity documentation/source references;
- quota source references;
- CI workflow;
- formal releases;
- recent commits;
- license.

GitHub Gold did **not**:

- build `rest-server`;
- run `go test`;
- execute the race detector;
- deploy a Restic repository;
- perform backup/restore operations;
- attempt destructive requests against append-only mode;
- test htpasswd authentication;
- test reverse-proxy authentication;
- test TLS configuration;
- exhaust repository quotas;
- perform fuzzing/path-traversal testing;
- benchmark REST versus SFTP performance;
- validate container images or signatures;
- perform a security audit.

Claims above distinguish repository-native source/CI evidence from direct runtime verification.

## Caveats and boundaries

### Append-only is an application-layer policy

A privileged attacker on the storage server can bypass it. The intended benefit is limiting damage from compromised backup-client credentials.

### Pruning needs a different trust path

Append-only clients cannot perform normal destructive retention maintenance. A secure architecture should use separately controlled credentials or a server-side/offline maintenance path for prune/forget operations.

### Proxy auth requires network isolation

If an attacker can connect directly to the backend while supplying the trusted username header, proxy authentication is defeated. The reverse proxy and network path are part of the authentication boundary.

### Basic auth requires protected transport

Repository encryption does not hide HTTP Basic credentials. Use TLS or an equivalent protected/authenticated transport when Basic Authentication crosses an untrusted network.

### `--no-verify-upload` weakens ingestion checks

Disabling server-side hash verification saves CPU but removes an early corrupted-upload detection layer.

### Quotas are not complete DoS protection

`--max-size` constrains repository storage growth but does not replace CPU, memory, connection, network, and process-level resource controls.

## Gold scoring

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Solves a concrete remote-backup and ransomware-resistance boundary for Restic. |
| Working Evidence | 5/5 | Production-oriented project with targeted tests, coverage, race testing and cross-target builds. |
| Reusability | 4/5 | Small, understandable Go service and REST backend implementation; primarily Restic-specific rather than generic object storage. |
| Novelty | 4/5 | HTTP backup servers are established, but append-only enforcement plus Restic-native layout is particularly useful. |
| Documentation | 5/5 | README documents auth, TLS, append-only, private repos, containers, systemd and deployment caveats in useful detail. |
| Maintenance | 4/5 | Current 2026 source activity and modern CI; latest formal release remains from May 2025. |
| **Total** | **27/30** | **Provisional S tier** |

## Evidence classification

**VERIFIED** means the repository's purpose and the key behaviors cataloged here are supported by repository-native source, tests, CI, release history, and documentation.

It does **not** mean GitHub Gold independently deployed or security-audited the service.

## Relationship to existing GitHub Gold candidates

### `restic/restic`

Parent backup engine and client. `rest-server` adds the remote REST endpoint and server-enforced append-only authorization layer.

### `restic/chunker`

Reusable CDC primitive used within Restic's data-processing stack. It solves chunk-boundary selection, not remote repository authorization or storage serving.

### Syncthing

Syncthing is peer-to-peer continuous synchronization. `rest-server` is a client/server backup endpoint optimized for immutable historical backup workflows; the two solve distinct persistence problems.

## Strong follow-up leads

1. Trace Restic's repository key/KDF/master-key wrapping path from source.
2. Inspect the exact tests for append-only delete rejection and overwrite behavior to document all protected object classes.
3. Examine `quota.Manager.WrapWriter` for concurrency/race/partial-upload semantics.
4. Compare `rest-server` with another mature append-only backup target such as Borg's server-side restrictions, focusing on authorization architecture rather than popularity.
5. Broaden the next major discovery into a non-storage category after this focused Restic component pass.

## Bottom line

`restic/rest-server` qualifies as GitHub Gold because it turns Restic's encrypted repository format into a small remote service with a meaningful server-side survivability boundary. Its most valuable features are append-only enforcement, fail-closed htpasswd loading, optional private-user repository namespaces, upload hash verification, quota support, TLS, observability, and a straightforward Go implementation with strong test/CI evidence.

**Verdict: VERIFIED — provisional S / 27.**
