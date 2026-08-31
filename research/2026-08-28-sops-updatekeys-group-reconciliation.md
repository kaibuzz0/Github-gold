# SOPS `updatekeys` and key-group reconciliation

Date: 2026-08-28

Project: https://github.com/getsops/sops

Status: source-level follow-up for existing **VERIFIED / provisional S / 28** candidate

License context: MPL-2.0. This dossier contains research notes only; no upstream source code is copied.

## Why this follow-up matters

Earlier GitHub Gold passes established that SOPS creation rules are ordered first-match policy and that Shamir thresholds apply across key groups. This pass traces what happens after policy changes: how an already encrypted file is reconciled with a changed `.sops.yaml`, and how the dedicated group add/delete commands alter metadata.

The main source inspected was:

- `cmd/sops/subcommand/updatekeys/updatekeys.go`
- `cmd/sops/subcommand/groups/add.go`
- `cmd/sops/subcommand/groups/delete.go`

Primary upstream links:

- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/updatekeys/updatekeys.go
- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/groups/add.go
- https://github.com/getsops/sops/blob/main/cmd/sops/subcommand/groups/delete.go

## Core finding: `updatekeys` is key-wrapper reconciliation, not content re-encryption

The update path first loads the existing encrypted file and retrieves its current data key using the file's existing metadata/key groups.

Only after recovering that data key does it replace `tree.Metadata.KeyGroups` with the key groups selected from the current creation rule and call `UpdateMasterKeysWithKeyServices` using the same recovered data key.

This means the conceptual operation is:

1. recover the existing SOPS data key under the old key policy;
2. select the current creation rule for the file;
3. replace the key-group metadata;
4. re-wrap/re-share the same data key under the new master-key policy;
5. emit the encrypted file again.

The encrypted document values are therefore not being conceptually rotated to a new random data key merely because `updatekeys` is run. The important change is the master-key/key-group wrapping metadata around the existing data key.

This distinction matters operationally: changing who can unwrap the file is different from rotating the underlying data key used for the encrypted tree.

## Key-group reconciliation uses the current first-match creation rule

`updatekeys` calls `config.LoadCreationRuleForFile` for the target path and obtains the rule-selected `KeyGroups`.

It computes a diff between:

- `tree.Metadata.KeyGroups` from the encrypted file; and
- `conf.KeyGroups` from the currently selected creation rule.

If keys were added or removed, the command can display the group diff before applying it. In interactive mode, the user can reject the proposed change before the existing data key is fetched and the metadata is rewritten.

This connects directly to the previous creation-rule finding: rule ordering can change which key policy `updatekeys` attempts to reconcile a file toward.

## Important threshold caveat: plain `updatekeys` does not simply adopt `conf.ShamirThreshold`

The current source contains an explicit TODO around threshold selection.

The observed behavior is:

- start from `tree.Metadata.ShamirThreshold`, i.e. the threshold already stored in the encrypted file;
- if the command options provide a non-zero `ShamirThreshold`, use that override;
- clamp the result so it cannot exceed the number of key groups selected by the current rule.

The current function does **not** automatically replace the stored threshold with `conf.ShamirThreshold` from the selected creation rule.

The source itself contains the comment:

> TODO: use conf.ShamirThreshold instead of tree.Metadata.ShamirThreshold ... Or make this configurable?

GitHub Gold records the implementation consequence, not the quoted wording: **changing only the threshold in `.sops.yaml` should not be assumed to make a plain `updatekeys` invocation adopt that new threshold automatically.**

This is a material policy-management caveat because key-group membership and quorum threshold are separate authorization dimensions.

## Threshold clamping

After selecting the current or explicitly overridden threshold, `updatekeys` applies:

`min(threshold, len(conf.KeyGroups))`

So if policy changes remove groups and leave the old threshold above the new group count, the update path reduces the threshold to the new group count rather than leaving an impossible quorum.

This is different from the explicit group-delete command behavior described below.

## No-op detection

The command detects two classes of policy difference:

- added/removed keys in any group; and
- a threshold difference after the updatekeys threshold-selection logic above.

If neither is present, it logs that the file is already up to date and returns without re-emitting the file.

Because threshold selection starts from file metadata unless explicitly overridden, a `.sops.yaml` threshold-only change may not become a detected threshold change through this path.

## Group-add behavior

The dedicated group-add command:

1. loads the encrypted file;
2. recovers the existing data key;
3. appends the requested key group;
4. optionally replaces the Shamir threshold if `GroupThreshold` is non-zero;
5. re-runs master-key wrapping/sharing with the same recovered data key;
6. emits the updated encrypted file.

If no new threshold is supplied, the existing stored threshold is retained.

This means adding a new group does not by itself make that new group required. For example, adding a third group to an existing 2-of-2 file while keeping threshold 2 changes the policy to 2-of-3 unless the caller explicitly changes the threshold.

That behavior is mechanically consistent with the separate concepts of group membership and quorum.

## Group-delete behavior

The group-delete command follows the same broad pattern:

1. recover the existing data key under the current metadata;
2. remove one group by index;
3. optionally set a new threshold;
4. reject the operation if the remaining group count is lower than the resulting threshold;
5. re-wrap/re-share the same data key for the remaining groups;
6. emit the updated file.

Unlike `updatekeys`, the explicit delete command does not silently clamp an impossible threshold after removing a group. It returns an error stating that the resulting Shamir threshold cannot be satisfied.

That difference is worth preserving in the catalog because the two maintenance paths have different failure semantics.

## Policy examples

### Example A: change recipients only

Existing file:

- group 1: Alice age key
- group 2: production KMS
- threshold: 2

New creation rule:

- group 1: Bob age key
- group 2: production KMS
- threshold: 2

`updatekeys` can recover the old data key, replace Alice's wrapping group with Bob's, and re-wrap the same document data key for the new groups.

### Example B: threshold-only policy change

Existing file:

- three groups
- threshold 2

New `.sops.yaml` rule:

- same three groups
- threshold 3

The inspected `updatekeys` source should **not** be described as automatically adopting 3 merely because `conf.ShamirThreshold` changed. Its default threshold source is the encrypted file metadata unless an explicit threshold option is provided.

### Example C: removing a group

Existing file:

- three groups
- threshold 3

Explicit group delete without changing threshold:

- remaining group count becomes 2
- threshold remains 3
- delete command rejects the operation as impossible

The `updatekeys` path, by contrast, clamps its selected threshold to the number of groups in the current creation rule.

## Write-path caveat

For in-place output, the inspected `updatekeys`, group-add, and group-delete implementations use `os.Create` on the destination path and then write the emitted encrypted bytes.

In the inspected source this is not implemented as an obvious temporary-file-plus-atomic-rename sequence inside these functions.

GitHub Gold is recording this only as an **operational write-path caveat**. This pass did not simulate interruption, disk-full conditions, partial writes, filesystem semantics, or recovery behavior, and does not label the pattern a vulnerability.

## Error-handling boundary worth deeper inspection

`updatekeys` captures the error slice returned from `UpdateMasterKeysWithKeyServices` and aborts if any errors are returned.

The inspected group add/delete functions call `UpdateMasterKeysWithKeyServices` without checking the returned error slice in these functions before emitting output.

That difference deserves a dedicated upstream-code/test inspection before drawing a stronger conclusion, because behavior may depend on lower-level metadata state, output encoding, and caller/test assumptions.

For now it is a **research lead**, not a defect claim.

## Reusable architecture lessons

SOPS exposes several generally useful patterns for secrets tooling:

- separate encrypted content from the policy that wraps its data key;
- allow recipient/key policy rotation without necessarily rotating all encrypted values;
- make group membership and quorum threshold independently configurable;
- diff policy metadata before rewriting encrypted files;
- preserve the ability to recover the old data key before replacing old recipients;
- explicitly reject impossible quorum states in direct mutation operations;
- distinguish rule selection from existing-file reconciliation.

The main caution is equally reusable: configuration-as-policy is only safe when operators understand which fields are actually synchronized automatically and which require explicit command options.

## Verification boundary

GitHub Gold inspected current upstream source and repository structure only.

This pass did not:

- run `sops updatekeys`;
- dynamically add/delete groups;
- test interruption or partial-write recovery;
- test multiple KMS providers;
- verify the exact CLI flag wiring for every threshold-related option;
- cryptographically verify data-key reuse;
- run upstream tests;
- prove whether the unhandled error slices in group add/delete can produce an unsafe output state.

Claims above are therefore limited to the control flow visible in the inspected upstream source.

## Candidate impact

SOPS remains:

- Evidence: **VERIFIED**
- Provisional Gold score: **28 / 30**
- Tier: **S**
- License: **MPL-2.0**

This pass does not justify a score change. It instead makes the policy-maintenance caveats more precise.

## Strong next leads

1. Inspect `UpdateMasterKeysWithKeyServices` to determine exact partial-failure behavior and what the group add/delete ignored return value can mean in practice.
2. Trace CLI wiring for `updatekeys` threshold flags and compare it with `.sops.yaml` threshold expectations/documentation.
3. Inspect upstream tests for updatekeys group-diff, threshold-clamp, add/delete, and failed-key-service behavior.
4. Inspect audit-event coverage during rewrap/updatekeys operations.
5. Compare `rotate` versus `updatekeys` to clearly separate data-key rotation from recipient-policy rewrapping.
6. Trace standalone `age` recipients through SOPS group metadata and identify what SOPS adds beyond age's native multi-recipient file format.
