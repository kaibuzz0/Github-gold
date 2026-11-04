# 2026-10-27/28 UTC — Cosign, Task and Open MCT maintenance

GitHub-first discovery, not YouTube-derived. Six seed playlist IDs were searched in earlier passes without accessible transcript evidence. No third-party source copied; no independent builds, signing, task execution, browser tests or security audits.

## Cosign — VERIFIED upstream, S29
https://github.com/sigstore/cosign — Apache-2.0 root. Stable v3.1.4 published 2026-10-20. Main Go module requires 1.27. Inspected README, LICENSE, go.mod, `cmd/cosign/cli/verify/verify.go`, `verify_attestation.go`, `verify_bundle.go`, `pkg/oci/remote/remote.go`, bundle types and attestation policy. Main [CI-Tests 40262470330](https://github.com/sigstore/cosign/actions/runs/40262470330) passed 6/6 jobs, main [E2E 40262470331](https://github.com/sigstore/cosign/actions/runs/40262470331) passed 5/5 (registry/KMS/PKCS#11/cross-platform), and [CodeQL 40262470324](https://github.com/sigstore/cosign/actions/runs/40262470324) passed 2026-10-26. Conformance nightly 40428072278 and 40609410330 succeeded 2026-10-27/28 UTC. Related ecosystem: sigstore/fulcio, sigstore/rekor, sigstore/sigstore-go, google/go-containerregistry, in-toto. Caveat: verify signer identity, issuer, trust roots and digest binding; check offline bundles, registry permissions, network service availability and dependency licenses. No local verification.

## Task — VERIFIED upstream, S28
https://github.com/go-task/task — MIT root. Stable v3.54.0 published 2026-10-01; current main go.mod requires Go 1.26.4. Inspected README, LICENSE, go.mod, `executor.go`, `compiler.go`, `taskfile/node_git.go`, `taskfile/node_http.go`, `internal/fingerprint/sources_checksum.go`, `watch.go`, AST and test fixtures. [CI 40605488694](https://github.com/go-task/task/actions/runs/40605488694) passed 16/16 jobs on 2026-10-27 (Go 1.26/1.27, Linux/macOS/Windows tests, lint, schema, docs and vulnerability checks). **This was a Renovate branch run, not main.** Nightly release 40607644805 succeeded 2026-10-28 UTC but is not stable release evidence. Dependencies/recursive leads: go-task/template, go-task/slim-sprig, mvdan.cc/sh/v3, chainguard-dev/git-urls. Remote Taskfiles execute arbitrary commands; pin immutable refs and review. Git loader rejects HTTP unless insecure enabled and uses private cache; not sandboxing.

## Open MCT — PROMISING/A25 unchanged
[2026-10-28 UTC e2e-full 40608853694](https://github.com/nasa/openmct/actions/runs/40608853694) Ubuntu job 122555106241 failed npm ci with EBADENGINE (required Node >=24.14.1, actual Node v18.20.8/npm 10.8.2). Windows cancelled; Playwright did not run. [e2e-perf 40607018153](https://github.com/nasa/openmct/actions/runs/40607018153) also failed npm ci; exact cause not separately diagnosed. Fix CI Node and obtain passing browser tests before promotion.

## Next
Cosign offline trust policy; Task remote include pinning and cache permissions; Open MCT CI Node version. Root licenses do not cover every dependency; no code copied.
