# SOPS audit-event coverage and observability boundaries

Date: 2026-08-28

Project: https://github.com/getsops/sops

Status: source-level follow-up for existing **VERIFIED / provisional S / 28** candidate

License context: MPL-2.0. This dossier contains research notes only; no upstream source code is copied.

## Why this follow-up matters

Earlier GitHub Gold passes separated SOPS full data-key rotation from recipient-policy rewrapping and identified weaker error handling in direct key-group mutation commands. This pass asks a separate operational question: which of those security-sensitive actions are actually represented in SOPS's built-in audit subsystem?

Primary upstream source inspected:

- `audit/audit.go`
- repository-wide uses of `audit.SubmitEvent`
- `cmd/sops/rotate.go`
- `cmd/sops/subcommand/updatekeys/updatekeys.go`
- `cmd/sops/subcommand/groups/add.go`
- `cmd/sops/subcommand/groups/delete.go`

## Built-in audit event model

Current `audit/audit.go` defines three concrete event types:

- `DecryptEvent`
- `EncryptEvent`
- `RotateEvent`

The stock PostgreSQL auditor persists these as the actions `decrypt`, `encrypt`, and `rotate` together with the current OS username and file path.

The auditor interface itself is extensible: callers can register additional `Auditor` implementations, and `SubmitEvent` forwards events to every registered auditor. However, the built-in event vocabulary inspected here is intentionally small.

## Repository-wide event submission coverage

A repository-wide search for `SubmitEvent(` located production submission paths in the normal SOPS encryption/decryption flow and the rotate command, plus the audit implementation itself.

The inspected search did **not** locate dedicated built-in audit submissions in:

- `updatekeys`;
- `groups add`;
- `groups delete`.

This means GitHub Gold should not describe SOPS's stock audit database as a complete record of all recipient/key-policy mutations.

A full data-key rotation has a dedicated `RotateEvent`; recipient reconciliation and direct group changes do not currently appear to have equivalent first-class built-in event types in the inspected source.

## Why the distinction matters

`rotate` and `updatekeys` are different security operations:

- `rotate` replaces the document data key and re-encrypts content;
- `updatekeys` keeps the existing data key while changing who can unwrap/reconstruct it;
- group add/delete directly mutate the key-group policy around that data key.

From an access-governance perspective, changing recipients or threshold structure can be just as important to review as rotating ciphertext keys. An audit stream containing only encrypt/decrypt/rotate therefore does not necessarily answer questions such as:

- who added a new recipient group;
- who removed a recipient group;
- who reconciled an existing file to a changed `.sops.yaml` policy;
- whether a Shamir threshold changed during a recipient-policy maintenance operation.

## Audit backend behavior

The stock audit implementation reads `/etc/sops/audit.yaml` and currently configures PostgreSQL auditor backends.

Startup behavior is fail-closed for configured audit-database connection failures: if one or more configured PostgreSQL audit backends cannot be initialized successfully, the audit package logs the failures and exits.

For a running PostgreSQL auditor, event persistence errors are also fatal in the inspected implementation: a failed insert calls the logger's fatal path rather than silently dropping the event.

This is a strong durability preference for the events that are actually emitted.

## Extensibility boundary

The `Auditor` interface accepts a generic event value, so downstream code could theoretically define custom event types and auditors. But stock `PostgresAuditor.Handle` only recognizes the three built-in event types above; unknown event types are logged as unknown rather than persisted as a generic row.

Therefore, adding policy-mutation auditing cleanly would require more than simply calling `SubmitEvent` with an arbitrary struct if the stock PostgreSQL backend is expected to store it. The event type and backend handling would need to be extended together.

## Verification boundary

GitHub Gold inspected current upstream source and repository-wide code-search results only.

This pass did not:

- run SOPS with `/etc/sops/audit.yaml` configured;
- initialize PostgreSQL;
- generate live encrypt/decrypt/rotate audit rows;
- dynamically test audit-database failure behavior;
- prove that no out-of-tree, downstream, or private integration adds updatekeys/group audit events;
- inspect every historical SOPS release.

The claim is limited to the inspected current upstream repository state.

## Candidate impact

SOPS remains:

- Evidence: **VERIFIED**
- Provisional Gold score: **28 / 30**
- Tier: **S**
- License: **MPL-2.0**

No score change is justified. The important catalog improvement is a more accurate observability claim: SOPS has a real audit subsystem with strong failure behavior for its emitted events, but the stock event model should not be presented as comprehensive recipient-policy audit coverage.

## Reusable design lessons

1. Security-event durability and security-event coverage are separate qualities.
2. Failing closed on audit persistence is valuable, but it only protects event classes that are emitted.
3. Recipient-policy mutations deserve first-class events when access-governance history matters.
4. Extensible auditor interfaces should pair extension points with a storage schema capable of representing new event classes.
5. Catalog entries should distinguish encryption/decryption auditability from recipient-management auditability.

## Strong next leads

1. Inspect upstream issues/PRs for requested `updatekeys` or key-group audit coverage.
2. Trace whether the CLI command layer provides any ordinary logs that can partially reconstruct recipient-policy changes even without audit events.
3. Compare SOPS's age integration with standalone age recipient semantics and determine what recipient detail is preserved in SOPS metadata.
4. Inspect release-signing/SBOM provenance and dependency-update policy as a separate supply-chain dossier.
