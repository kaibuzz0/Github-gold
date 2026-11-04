# Atuin and OpenBao — source-backed discovery (2026-10-29 UTC)

## Research scope and provenance
GitHub-first research. Inspected both canonical repositories, source layouts, manifests, licenses, releases and GitHub Actions. Six YouTube seeds were previously searched without accessible transcript evidence; **no YouTube attribution** is claimed. No third-party code was copied. No local builds, network deployments, encryption tests, or security audits were performed.

## Atuin — VERIFIED upstream / S27
- Repository: https://github.com/atuinsh/atuin ; MIT root LICENSE, 2026 copyright. Rust workspace `rust-version = "1.95.0"`; pinned `rust-toolchain.toml` 1.98.0. Review dependencies before reuse.
- Stable release v18.24.3 published 2026-10-29: https://github.com/atuinsh/atuin/releases/tag/v18.24.3 . Current inspected main commit `4532ceacd860885c2310ab8fab92a1bc00d6d7e8` (2026-10-29).
- Primary upstream evidence: https://github.com/atuinsh/atuin/actions/runs/40611984554 — Windows 2026-10-28 earlier-main run, two successful jobs. One executed `cargo test`; another executed several `cargo check` feature configurations. This **does not** establish current release cross-platform or encrypted sync E2E success.
- https://github.com/atuinsh/atuin/actions/runs/40801883907 — current-main Docker build succeeded 2026-10-29, but is not a functional test. Main CI uses Buildkite; its full results were not independently inspected.
- Reusable exact locations: `crates/atuin-client/src/history/{capture.rs,store.rs,builder.rs}`; `crates/atuin-client/src/record/{sqlite_store.rs,sync/}`; `crates/atuin-client/src/tui/`; `crates/atuin-server/src/{router.rs,handlers/,db/}`; `crates/atuin-history/src/{sort.rs,stats.rs}`; `crates/atuin-client/tests/{e2e_sync.rs,shells/}`.
- Shell integrations claimed in README: Bash, Zsh, Fish, Nushell, Xonsh and PowerShell; local SQLite and optional encrypted sync. Nushell catalog entry cross-linked, without implying that Atuin is part of Nushell core.
- Risks: command history may expose tokens, passwords, file paths and hostnames locally; encrypted synchronization is not a substitute for endpoint protection. Avoid piping unreviewed installers to a shell. Test offline history capture, shell hooks, sync conflicts, key recovery and encrypted server storage in a controlled environment before operational reliance.

## OpenBao — VERIFIED upstream / S28
- Repository: https://github.com/openbao/openbao ; MPL-2.0 root license with original HashiCorp copyright. `.go-version` pins Go 1.27.3.
- Stable v2.7.2 published 2026-10-26: https://github.com/openbao/openbao/releases/tag/v2.7.2 . Inspected main `159a64c9a08be548eef7939449e336e97cd878b7` (2026-10-29).
- Main CI: https://github.com/openbao/openbao/actions/runs/40850965740 — **39/39 jobs successful** on that exact SHA. Included 17 regular Go test shards, 16 Go race-test shards, setup/matrix/reporting jobs. `Run Go tests` and `Test Summary` steps succeeded. Lint workflow https://github.com/openbao/openbao/actions/runs/40850965627 also passed. This does not establish live HA/failover, external PKI, auth backend or cryptographic security.
- Reusable public interfaces: `api/client.go`, `api/kv_v2.go`, `api/lifetime_watcher.go`, and `sdk/`. README explicitly supports `github.com/openbao/openbao/api/v2` and `.../sdk/v2` as imports; importing root `github.com/openbao/openbao` is unsupported.
- Internal architectural references (not public APIs): `internal/vault/{barrier/,seal/,expiration.go,token_store.go,policy/,audit.go,raft.go}`; `internal/builtin/{credential/,logical/,database/}`.
- Relationship: SOPS encrypts configuration files at rest; OpenBao supplies a centralized service for secret lifecycle, leases, policies and dynamic credentials. Complementary design, **not a verified integration**.
- Risks: default development `server -dev` is inappropriate for production. Protect TLS endpoints, unseal/recovery keys, root tokens, audit sinks, backups and plugin execution. MPL-2.0 file-level copyleft; do not copy implementation without reviewing notices/dependency licenses.

## Deferred and follow-up
1. Atuin: inspect current Buildkite test matrix, Linux/macOS shell integration, encrypted sync conflict resolution, and Termux compatibility. Cross-reference Nushell plugin documentation if stronger runtime evidence emerges.
2. OpenBao: test API/SDK client in isolated dev environment; validate HA/raft recovery, audit failure modes, token policies, secret engine rotation and TLS. Examine `openbao/openbao-helm` separately before claiming deployability.
3. Compare OpenBao against SOPS only at architectural level. No evidence justifies changing SOPS's score.
