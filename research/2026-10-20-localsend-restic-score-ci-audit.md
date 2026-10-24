# LocalSend and restic: scoring backfill and CI evidence (2026-10-20)

## Scope
Existing canonical entries were improved rather than duplicated. No new project was promoted. Scores and S tiers were preserved; six-factor breakdowns were added. Evidence is from upstream repositories, releases and workflow results. No upstream source was copied or executed.

## LocalSend — VERIFIED (upstream), S / 28
- Breakdown: Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 5; Maintenance 4.
- Apache-2.0 root license. Flutter application and network providers: `app/lib/provider/network/`, `app/lib/provider/network/server/`; Rust CLI and server: `cli/src/`, `server/src/`; shared Rust package: `packages/core/`.
- Upstream stable release `v1.18.2` was published **2026-08-21**, not 2026-08-17 as the old catalog prose suggested. Release notes document backward-compatibility fixes and avoidance of peer HTTP redirects; previous v1.17.0 notes a path-traversal fix.
- Main-branch CI run `38703786899` created **2026-10-15**: all four jobs (test, packaging, rust, format) succeeded.
- Limits: no independent cross-platform transfer test, TLS/protocol audit, or release-artifact verification. LAN multicast discovery can be affected by isolation and firewall rules.

## restic — VERIFIED (upstream), S / 29
- Breakdown: Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 5; Maintenance 5.
- BSD-2-Clause root license. Reusable components: `internal/repository/` (indexes, packs, locks, integrity), `internal/archiver/` (scanning, tree saving), `internal/restorer/`, and `internal/backend/` (REST/S3/SFTP/Azure/B2/GCS and more).
- Latest stable GitHub release inspected: `v0.19.1`, published **2026-07-05**.
- **CI caveat:** master push run `39135808574` on **2026-10-18** failed. Job `117699961719` failed in `TestBackendSwift` during cloud backend testing: the upstream authentication endpoint returned `x509: certificate has expired or is not yet valid`, with expiration **2026-10-01T23:59:59Z**. This is direct upstream log evidence for a remote TLS failure, not evidence that restic encryption or backup/restore is broken. Root cause/repair of remote service was not independently confirmed.
- Other jobs in that run succeeded: Linux Go 1.26, macOS Go 1.27, cross-compile subsets, lint, Docker. Linux race and Windows jobs were cancelled, and aggregate Analyze results failed. Do not describe this workflow as passing.
- Limits: no independent backup/restore, disaster recovery, cryptographic, or storage backend integration test. Maintain the high score on broader maturity and source evidence, while flagging the red CI run.

## Follow-up
1. Check for resolution of restic Swift backend TLS certificate and restored master CI.
2. Independently test LocalSend device discovery and mixed-version transfer.
3. Continue scoring backfill for remaining 25 canonical entries lacking six-factor breakdowns.

## Primary sources
- https://github.com/localsend/localsend/releases/tag/v1.18.2
- https://github.com/localsend/localsend/actions/runs/38703786899
- https://github.com/localsend/localsend/tree/main/app/lib/provider/network
- https://github.com/localsend/localsend/blob/main/LICENSE
- https://github.com/restic/restic/releases/tag/v0.19.1
- https://github.com/restic/restic/actions/runs/39135808574
- https://github.com/restic/restic/actions/runs/39135808574/job/117699961719
- https://github.com/restic/restic/tree/master/internal/repository
- https://github.com/restic/restic/blob/master/LICENSE
