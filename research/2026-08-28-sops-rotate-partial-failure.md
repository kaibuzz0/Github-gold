# SOPS rotation versus rewrapping and partial-failure semantics

Date: 2026-08-28

Project: https://github.com/getsops/sops

Status: source-level follow-up for existing **VERIFIED / provisional S / 28** candidate

License context: MPL-2.0. This dossier contains research notes only; no upstream source code is copied.

## Why this follow-up matters

Earlier GitHub Gold passes established that `updatekeys` changes recipient/key-group policy around an existing document data key. This pass answers two remaining questions:

1. how `sops rotate` differs from `updatekeys`; and
2. what happens when only some master-key wrapping operations succeed.

Primary upstream source inspected:

- `cmd/sops/rotate.go`
- `cmd/sops/subcommand/updatekeys/updatekeys.go`
- `cmd/sops/subcommand/groups/add.go`
- `cmd/sops/subcommand/groups/delete.go`
- `sops.go` (`GenerateDataKeyWithKeyServices` and `UpdateMasterKeysWithKeyServices`)

Primary links:

- https://github.com/getsops/sops/blob/main/cmd/sops/rotate.go
- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/updatekeys/updatekeys.go
- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/groups/add.go
- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/groups/delete.go
- https://github.com/getsops/sops/blob/main/sops.go

## Core distinction: `rotate` creates a new random data key

Current `rotate` control flow is materially different from `updatekeys`.

The rotate path:

1. loads the encrypted file;
2. decrypts the tree;
3. applies requested master-key additions/removals;
4. calls `GenerateDataKeyWithKeyServices`;
5. generates a fresh 32-byte random data key;
6. wraps/shares that new key across the configured master keys/groups;
7. re-encrypts the decrypted tree with the new data key;
8. emits a newly encrypted file.

This is full document data-key rotation.

By contrast, `updatekeys`:

1. loads the encrypted file;
2. recovers the existing data key;
3. selects the current creation-rule key groups;
4. re-wraps/re-shares that existing data key for the new policy;
5. emits the file without conceptually replacing the document data key.

So the operations should be described separately in GitHub Gold:

- **rotate:** new random document data key + content re-encryption;
- **updatekeys:** existing data key + recipient/master-key policy reconciliation.

## `rotate` failure boundary

`GenerateDataKeyWithKeyServices` first generates 32 random bytes and then calls `UpdateMasterKeysWithKeyServices` for the new key.

The rotate command checks the returned error slice. If any wrapping errors are reported, it returns before calling `EncryptTree` and before emitting the new encrypted document.

This means the inspected rotate command does not intentionally proceed to content re-encryption after a reported partial master-key wrapping failure.

GitHub Gold did not run failure injection, so this is a source-control-flow conclusion rather than a dynamic durability guarantee.

## `updatekeys` failure boundary

`updatekeys` also checks the error slice returned from `UpdateMasterKeysWithKeyServices`.

Its sequence is:

1. recover the existing data key;
2. replace key-group metadata in memory;
3. call `UpdateMasterKeysWithKeyServices`;
4. if any errors are returned, abort before marshaling/writing the file.

So although the in-memory tree can be partially mutated during failed wrapping attempts, the inspected `updatekeys` function does not emit that partially updated state when the helper reports errors.

This is a useful safety distinction from the dedicated group mutation functions below.

## Exact partial-failure behavior inside `UpdateMasterKeysWithKeyServices`

The helper iterates every key group and every master key.

For each master key it tries the configured key services until one succeeds.

On success:

- the returned ciphertext is immediately stored into that master-key object;
- processing continues with the remaining keys.

If all services fail for one master key:

- the collected errors for that key are appended to the returned error slice;
- processing continues with other keys rather than immediately rolling back prior successful mutations.

After the loops, the metadata cache is assigned the supplied data key and the accumulated errors are returned.

So the helper itself is **not transactional**. It can leave an in-memory metadata structure containing a mix of successful updates and failed/unupdated keys.

Whether that partial state reaches disk depends on the caller.

## One-key-group versus multi-group behavior

For one key group, every master key in the group receives the full data key.

For multiple groups, SOPS first Shamir-splits the data key into one part per group according to the configured threshold, then tries to wrap each group's part with every master key in that group.

A wrapping failure therefore has slightly different meaning depending on configuration:

- single group: one recipient may fail to receive a new wrapper for the full data key;
- multiple groups: one recipient may fail to receive the wrapper for that group's Shamir share.

The returned error slice lets callers decide whether any such failure should abort persistence.

## Group add/delete currently use a weaker caller boundary

The current dedicated group-add and group-delete functions call `UpdateMasterKeysWithKeyServices` but do not inspect its returned error slice in those functions.

They then continue to emit the encrypted-file representation.

This means these functions should **not** be described as having the same failure boundary as `updatekeys` or `rotate`.

A failed wrapping operation can be reported by the helper but ignored by the immediate caller while other successful key-wrapper mutations remain in the in-memory metadata used for emission.

GitHub Gold is recording this as a **source-level correctness/robustness caveat**, not as a demonstrated exploitable vulnerability. This pass did not inject failing key services or prove the exact emitted/decryptability outcome for every provider/group configuration.

## Additional group-command write-error caveat

The inspected group add/delete functions also invoke `outputFile.Write(output)` without checking the returned byte count/error in those functions.

That is separate from the master-key wrapping issue and should be treated as another write-path robustness lead.

This pass did not simulate disk-full, short-write, filesystem, stdout-pipe, or interrupted-write behavior.

## Why the helper is still reusable

The underlying design has useful properties despite the caller-boundary differences:

- one master key can try multiple key-service backends;
- success is accepted as soon as one service wraps the key;
- failures are accumulated per master key instead of losing diagnostic detail;
- Shamir splitting is centralized before provider-specific wrapping;
- callers can choose strict all-wrapper success by checking the returned errors.

The important reusable lesson is that **partial-success helpers need explicit transactional policy at the caller**. A caller that persists output should make a conscious decision about whether any wrapper failure is acceptable.

## Operational comparison

### `rotate`

Use when the goal is to replace the document data key itself.

Observed behavior:

- decrypt existing tree;
- generate fresh random data key;
- wrap/share fresh key;
- abort on returned wrapping errors;
- re-encrypt content with new key;
- emit output.

### `updatekeys`

Use when the goal is to reconcile recipient/key-group policy without necessarily replacing the document data key.

Observed behavior:

- recover existing data key;
- replace group policy in memory;
- re-wrap/re-share same key;
- abort on returned wrapping errors;
- emit updated metadata.

### group add/delete

Use for direct group mutations.

Observed source caveat:

- recover existing data key;
- mutate group configuration;
- call wrapper update;
- immediate function does not check returned wrapper-error slice;
- continue to emit output.

## Candidate impact

SOPS remains:

- Evidence: **VERIFIED**
- Provisional Gold score: **28 / 30**
- Tier: **S**
- License: **MPL-2.0**

No score change is justified from source inspection alone. The new dossier improves the catalog by separating three maintenance operations that should not be treated as equivalent.

## Verification boundary

GitHub Gold inspected current upstream source only.

This pass did not:

- execute `sops rotate`;
- execute `sops updatekeys`;
- execute group add/delete;
- inject a failing KMS, age, PGP, Vault, or key-service backend;
- prove decryptability after a partial group-command wrapping failure;
- simulate short writes or interrupted writes;
- audit cryptographic primitives;
- run the upstream test suite.

Claims are limited to the visible control flow and error handling in the inspected source.

## Strong next leads

1. Inspect upstream tests for rotate, updatekeys, and group operations under key-service failure.
2. Determine whether group add/delete ignored wrapper errors are already tracked in upstream issues or recent commits.
3. Trace audit-event coverage: rotate emits a dedicated audit event, while key-policy rewrapping should be checked separately.
4. Inspect the exact SOPS `age` integration boundary and compare SOPS key groups with age's native multi-recipient semantics.
5. Revisit in-place write durability and whether other command layers provide atomic-write protection outside the inspected functions.
