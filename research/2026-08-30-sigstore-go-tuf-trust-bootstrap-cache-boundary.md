# sigstore-go TUF trust bootstrap and cache boundary

- Upstream repository: https://github.com/sigstore/sigstore-go
- Research date: 2026-08-30
- Scope: `pkg/tuf` trust bootstrap, metadata refresh, cache behavior, offline constraints
- Parent candidate: sigstore-go — VERIFIED — provisional S / 29 — Apache-2.0
- Verification type: source/test inspection only; no live TUF refresh performed

## Executive finding

The `sigstore-go/pkg/tuf` layer is a small but security-critical boundary between bundle verification and the trust material used to authorize that verification. Its design makes the initial TUF root an explicit trust anchor, then delegates signed metadata update and target verification to `go-tuf/v2`.

The most useful architectural lesson is that `sigstore-go` does **not** treat network retrieval as the root of trust. `DefaultOptions()` embeds a public-good `root.json` inside the library and supplies it to the TUF updater; custom deployments can replace that root explicitly with `WithRoot(...)`. The configured repository URL therefore supplies update data, while the initial root bytes establish the trust anchor.

This is a strong reusable pattern for update clients: bootstrap trust separately from the transport used to fetch future metadata.

## Bootstrap path

`DefaultOptions()` establishes:

- embedded public-good `root.json` as the default TUF root;
- `https://tuf-repo-cdn.sigstore.dev` as the default metadata/target repository;
- a cache under `$HOME/.sigstore/root` (falling back to a temp directory when the home directory cannot be resolved);
- the standard go-tuf HTTP fetcher with Sigstore's user agent.

`New()` passes the configured repository URL and root bytes into `go-tuf/v2`'s updater configuration. This makes the root bytes the initial authorization material for repository metadata.

The client supports dependency injection of a custom fetcher, repository URL, root, and cache path, which is useful for private Sigstore deployments, deterministic tests, custom transports, or controlled mirrors.

## Initial local-first check

Client creation intentionally begins with a temporary updater configured in `UnsafeLocalMode=true`. In this specific use, the source comments explain that the mode is used so the first initialization reads only metadata already present on disk. The code then decides whether a full refresh is required.

This naming deserves care in downstream documentation: `UnsafeLocalMode` is an upstream go-tuf mode name, but `sigstore-go` is using it narrowly as a local metadata inspection step before deciding whether to perform a normal verified update.

If local metadata cannot be loaded and verified, `loadMetadata()` falls back to `Refresh()`.

## Refresh behavior

`Refresh()` creates a normal updater from the configured TUF options and calls its `Refresh()` method. Errors from the TUF refresh fail client initialization/refresh rather than silently accepting unverifiable metadata.

After a successful refresh, the client records a local `LastTimestamp` used only to control how aggressively subsequent clients refresh. The recorded wall-clock timestamp is not itself the cryptographic TUF metadata timestamp and should not be confused with signed repository freshness evidence.

## Cache controls

The client exposes three materially different cache behaviors:

### Default / `CacheValidity == 0`

After loading locally available metadata, the client performs a normal refresh. This is the most freshness-oriented behavior.

### `CacheValidity > 0`

The client may skip a network refresh when its persisted local update timestamp remains within the configured number of days. However, the source comments and tests show that expired TUF metadata still forces a refresh/failure path; `CacheValidity` is not a mechanism for accepting expired signed metadata.

### `ForceCache`

`ForceCache` uses locally cached data without updating **while the TUF metadata is still valid**. Once metadata expires, the client attempts a refresh. The test suite explicitly exercises this behavior.

This is an important operational distinction: `ForceCache` is not equivalent to 'trust cached metadata forever.'

## Air-gapped boundary

Upstream comments explicitly state that `CacheValidity` and `ForceCache` are not ideal controls for truly air-gapped environments because initialization or metadata expiry can still require a refresh.

The recommended architecture for an air-gapped verifier is to provide trust-root material directly and bypass TUF-based online root retrieval/update when network refresh cannot be guaranteed.

For GitHub Gold, this means the reusable component should be cataloged as both:

1. a TUF update client for connected environments; and
2. a clear example of why offline verification and online trust-root maintenance are separate deployment modes.

## Target retrieval

`GetTarget()` first obtains target metadata from the verified updater state, then asks the updater whether a matching cached target exists. If not, it downloads the target through go-tuf's verified target flow.

The code does not simply fetch an arbitrary URL and return bytes; target retrieval is driven by TUF target metadata.

## Test evidence

The inspected `pkg/tuf/client_test.go` contains concrete coverage for the wrapper's own trust/cache behavior:

- an offline/forced-cache initialization with no metadata fails;
- refreshing changes a target from version 1 to version 2;
- a root belonging to a different test repository is rejected;
- an invalid repository URL is rejected;
- a still-valid cache returns the older target until the configured cache-validity period expires;
- deleting the local cache-timestamp configuration triggers fresh metadata retrieval;
- `ForceCache` returns cached data while metadata is valid;
- an expired TUF timestamp causes client creation to fail when the repository also serves expired metadata;
- once the repository timestamp becomes valid again, the client refreshes and retrieves the newer target even with `ForceCache` enabled.

The test file explicitly states that advanced TUF properties such as delegation, threshold behavior, and other core TUF security properties are expected to be covered by upstream `go-tuf` tests rather than reimplemented in this wrapper suite.

## Trust boundary interpretation

The security chain can be summarized as:

`embedded/provisioned root.json -> go-tuf metadata verification -> verified target metadata -> trusted-root target bytes -> sigstore-go TrustedMaterial -> bundle verification`

Important consequences:

- changing the repository URL does not by itself redefine trust if the original root remains authoritative;
- replacing the bootstrap root is a security-sensitive provisioning operation;
- a compromised mirror should still have to satisfy TUF metadata verification, assuming the trusted root and updater implementation remain sound;
- stale-but-unexpired metadata may be deliberately reused according to cache policy;
- expired metadata is not made valid merely because `ForceCache` is enabled;
- private or air-gapped deployments need an explicit trust-root distribution/update plan rather than only a mirror URL.

## Reusable components / patterns

### Embedded trust-anchor bootstrap

Embedding the initial root in the client binary reduces dependence on first-use network trust. This is a useful pattern for signed updater clients and provenance verifiers.

### Fetcher injection

The `Fetcher` interface lets users replace the network mechanism while retaining the TUF verification layer. This is useful for testing, proxies, controlled transports, offline staging, and private infrastructure.

### Local-first metadata decision

The client inspects locally available verified metadata before deciding whether a remote refresh is required, reducing unnecessary network work without confusing local cache policy with signature validation.

### Fail-closed expiry behavior

The tests demonstrate that expired timestamp metadata causes failure/refresh rather than unconditional cached acceptance.

### Separate cache timestamp vs signed metadata freshness

The wrapper's own `LastTimestamp` controls refresh cadence, while TUF metadata expiration remains enforced by the updater. Keeping those concepts separate is a valuable design pattern.

## Caveats

### TUF guarantees are largely inherited

`sigstore-go/pkg/tuf` is a wrapper around `github.com/theupdateframework/go-tuf/v2`. Core rollback, freeze, threshold-signature, consistent-snapshot, delegation, and metadata-chain guarantees should be attributed to the actual go-tuf behavior and tests, not claimed as independently implemented by this wrapper.

### `DisableConsistentSnapshot`

The options surface allows consistent-snapshot target prefixing to be disabled. That is a deliberate compatibility/configuration knob and should be treated as a security-relevant deployment option rather than a cosmetic setting.

### Custom fetchers

A custom fetcher becomes part of the availability/privacy boundary. It should not be assumed to replace TUF verification, but buggy custom transport behavior can still affect availability, routing, proxying, credentials, and metadata exposure.

### Bootstrap-root lifecycle

An embedded root solves initial trust only if release/update processes securely rotate that root over time. Long-lived or private deployments still need a root-rotation strategy.

### Cache persistence

The cache and wrapper timestamp are local mutable state. TUF validation limits what cached signed metadata can authorize, but filesystem access can still affect availability and refresh behavior.

## Verification boundary

GitHub Gold inspected current upstream source and wrapper tests only.

Not performed:

- live request to the Sigstore TUF CDN;
- local `go test`;
- root rotation test;
- rollback/freeze attack simulation;
- cache tampering test;
- private mirror test;
- custom fetcher implementation;
- air-gapped deployment;
- independent audit of `go-tuf/v2`.

No third-party source code was copied.

## Impact on parent score

`sigstore-go` remains **VERIFIED — provisional S / 29**. This deeper inspection strengthens confidence in its trust-material architecture but does not justify a score increase because 29/30 already reflects exceptional evidence and GitHub Gold still has not performed local execution or an independent cryptographic/security audit.

## Strong next leads

1. Inspect the exact `TrustedRootFromTUF`/root-target conversion path into `TrustedMaterial`.
2. Trace `Verifier.Verify` fail-closed ordering across certificate, SCT, Rekor, timestamp, identity, and artifact checks.
3. Inspect `pkg/sign` key interfaces to document KMS/HSM adapter requirements.
4. Compare Cosign v3's higher-level TUF/root behavior against direct `sigstore-go` usage.
5. Broaden the next discovery pass into package provenance / PEP 740 or another technical category.