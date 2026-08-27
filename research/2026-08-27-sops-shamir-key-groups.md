# SOPS — Shamir key groups and quorum semantics

- Upstream repository: https://github.com/getsops/sops
- Parent candidate: SOPS
- Evidence level: VERIFIED source-level architecture notes
- Research date: 2026-08-27
- Scope: key-group semantics, Shamir split/reconstruction behavior, quorum defaults, decryption ordering, and operational caveats

## Why this follow-up exists

The parent SOPS dossier records key groups and Shamir Secret Sharing as an important high-value feature, but a simple statement such as "SOPS can require multiple keys" is too imprecise.

Current upstream behavior has two distinct policy layers:

1. **inside a key group:** master keys are alternatives; any usable master key in that group can recover the group's share;
2. **across key groups:** a configurable Shamir threshold determines how many distinct group shares are required to reconstruct the document data key.

That distinction is central to using the feature correctly.

## Source snapshot used

This pass inspected current upstream `main`, including:

- `sops.go` data-key split/recovery paths;
- `config/config.go` creation-rule/key-group parsing;
- current upstream README key-group documentation.

Observed source commit/search snapshot: `73416337fd881c74b516772b75e5db0ffd29616e`.

GitHub Gold did not independently execute the cryptographic routines.

## Core data-key model

SOPS encrypts document values with a per-document data key.

Without multiple key groups, master keys act as alternative wrappers around that same data key: possession of any usable configured master key can recover it.

With multiple key groups, SOPS changes the data-key wrapping model:

- the data key is split into one Shamir share per key group;
- every master key inside a given group encrypts the same share for that group;
- reconstruction requires enough successfully recovered **group shares** to meet `ShamirThreshold`.

The unit of quorum is therefore the **key group**, not the individual master key.

## OR inside a group

`decryptKeyGroup` iterates the group's master keys and returns as soon as one key successfully decrypts the group's share.

Operationally, a group such as:

- one AWS KMS key;
- one age recipient;
- one PGP key;

is not a 3-of-3 requirement.

It is an OR-set protecting one Shamir fragment: any one of those usable identities can satisfy that group.

This is useful for redundancy and provider diversity inside a policy domain, but it should not be described as increasing the Shamir threshold by adding more keys to the same group.

## AND / threshold across groups

`UpdateMasterKeysWithKeyServices` allocates one Shamir part for each group whenever more than one key group exists.

If the stored/configured threshold is zero, current source sets:

`ShamirThreshold = len(KeyGroups)`

before calling the Shamir split routine.

That means the default multi-group policy is effectively **all groups required**.

For example:

- 3 key groups;
- threshold omitted / zero;

becomes a 3-of-3 group requirement.

Current upstream documentation describes the same default.

## Explicit threshold

Operators can lower the required quorum with `shamir_threshold` in `.sops.yaml` or the CLI threshold option when creating/editing a file.

Example conceptual policy:

- Group A: organization KMS + backup age identity;
- Group B: security-team KMS + hardware-backed identity;
- Group C: disaster-recovery identity;
- threshold: 2.

This creates a 2-of-3 **group** requirement, while each group can still contain several alternative master keys for its own share.

That gives SOPS a useful two-level resilience model:

- redundancy **within** a group;
- quorum **between** groups.

## Single-group special case

Current source explicitly bypasses Shamir splitting when there is only one key group.

In that case:

- the whole data key is used as the group's `part`;
- every master key in that one group encrypts the whole data key;
- decryption succeeds when one key from the group succeeds.

So a configured threshold concept is meaningful only when multiple key groups are actually present in the active metadata path.

This matters when reviewing `.sops.yaml`: putting several identities into one group is not equivalent to creating several groups.

## Encryption path

For multiple groups, the encryption/update path does the following:

1. if threshold is zero, replace it with the number of groups;
2. call the Shamir split routine with:
   - number of parts = number of key groups;
   - quorum = `ShamirThreshold`;
3. associate one returned share with each group;
4. encrypt that same share independently with every master key inside the group;
5. store each key's encrypted data-key/share material in SOPS metadata.

The source also rejects an empty key group during master-key update.

This is important: group boundaries become part of the durable encrypted-file recovery policy, not merely a UI grouping convention.

## Decryption and reconstruction path

`GetDataKeyWithKeyServices` walks all key groups and asks `decryptKeyGroup` to recover one share from each group.

For each group:

- configured decryption ordering can prioritize key types;
- each master key is attempted until one succeeds;
- successfully recovered group shares are collected;
- group-level failures are preserved for error reporting.

If there are multiple groups and fewer recovered shares than `ShamirThreshold`, SOPS returns a structured data-key-recovery error rather than attempting reconstruction with insufficient shares.

Once enough shares are available, SOPS calls the Shamir combine routine to recover the original data key.

## Important implementation nuance: it currently scans all groups

The current `GetDataKeyWithKeyServices` implementation loops over all configured groups before it tests whether enough parts were recovered.

So although the cryptographic policy may only require (for example) 2 of 3 groups, current source does not simply stop after the first two successful groups during this loop.

That means a lower quorum does not necessarily imply that SOPS avoids touching/attempting identities in later groups during data-key recovery.

GitHub Gold records this as an operational/source observation, not a security flaw. It can matter when key backends have audit logs, latency, prompts, network dependencies, or per-operation costs.

## Decryption ordering is not quorum priority

SOPS supports a decryption-order list that affects the order of master-key types **within each group**.

The code sorts indices for the group's keys by key-type priority, then tries them in that order.

This does not change:

- which groups exist;
- the Shamir threshold;
- how many group shares are required.

It only influences which identity/backend is tried first while attempting to satisfy a group.

This is a useful separation between recovery policy and backend preference.

## Error-reporting model

The data-key recovery path builds a group-oriented error structure that records:

- the required number of successful groups;
- one result/error per configured key group.

That aligns error reporting with the actual quorum boundary rather than flattening every master-key failure into one undifferentiated list.

For operators, this can help identify whether a failure is caused by:

- one unavailable alternative identity inside an otherwise recoverable group;
- a completely unrecoverable group;
- insufficient successful groups to meet quorum.

## Threshold validation boundary

Current public documentation states that `shamir_threshold` is either zero/default or an integer at least 2.

The inspected `configFromRule` path copies the configured integer into the runtime `Config`; the actual data-key split path then passes that threshold into the Shamir implementation.

This pass did not fully trace every CLI/config validation path for all impossible combinations, such as a threshold greater than the number of groups.

GitHub Gold therefore should not claim that every malformed threshold configuration is rejected at config-parse time. The verified claim is narrower: the active split path delegates the requested quorum to the Shamir split implementation, and normal documented configuration requires a valid quorum.

## Security-policy interpretation

### Group = trust domain / recovery domain

A key group should be treated as a set of identities that are interchangeable for one share.

If two parties must both participate, placing both parties' keys in the same group does **not** enforce that requirement.

They need distinct groups and a threshold that requires both groups.

### Threshold = cross-domain quorum

The threshold is the actual multi-party recovery control.

Examples:

- 2 groups, default threshold -> 2-of-2;
- 3 groups, default threshold -> 3-of-3;
- 3 groups, threshold 2 -> 2-of-3;
- many keys inside Group A -> still only one recovered share from Group A.

### Redundancy and quorum are orthogonal

Adding backup identities to one group improves availability of that group without weakening or strengthening the number of group shares required.

That is one of the most reusable design patterns in SOPS's architecture.

## Failure-domain design lessons

A strong group layout can separate independent failure domains, for example:

- cloud KMS under production IAM;
- security-team offline age identity;
- disaster-recovery/HSM identity.

Then a 2-of-3 threshold can survive one unavailable domain while still requiring more than one domain to recover the data key.

But if several supposedly independent identities ultimately depend on the same account, IAM root, CI environment, or network control plane, the Shamir grouping alone does not create real organizational independence.

The cryptographic grouping should therefore reflect real operational trust boundaries.

## Interaction with key service

The previous key-service dossier matters here.

A remote SOPS key service can be one path through which group keys are attempted, but the stock key-service protocol does not itself provide a full remote authentication/authorization policy framework.

Using key groups does not automatically fix a weakly protected key-service deployment. Quorum policy and service-authentication policy are separate controls.

Likewise, because provider operations can occur while attempting group recovery, backend audit logs may record attempts even when another set of shares ultimately satisfies the threshold.

## Interaction with document MAC

Shamir groups protect access to the document data key.

After SOPS reconstructs the data key, the normal decrypt helper still:

1. decrypts the tree;
2. recomputes its document MAC;
3. decrypts the stored MAC;
4. verifies equality before returning plaintext unless MAC checking was explicitly bypassed.

So quorum recovery and document integrity are separate gates:

- key groups decide whether the data key can be recovered;
- the tree/MAC path decides whether the decrypted document passes integrity verification.

## Reusable architecture lessons

### 1. Separate quorum from redundancy

Make multiple credentials inside one trust domain alternatives, then apply quorum across independent domains.

### 2. Store policy with the encrypted artifact

The encrypted file carries group/share metadata and threshold information needed for later recovery rather than relying solely on ephemeral runtime state.

### 3. Keep backend preference separate from cryptographic quorum

Decryption ordering can optimize latency/user experience without changing which shares are required.

### 4. Model errors at the quorum boundary

Group-oriented error reporting better reflects the actual recovery policy than a flat list of credential failures.

### 5. Do not confuse cryptographic independence with administrative independence

A 2-of-3 cryptographic threshold is only as organizationally independent as the systems/accounts controlling those three groups.

## Verification boundaries

This pass inspected upstream source and public documentation only.

GitHub Gold did **not**:

- independently verify the Shamir implementation mathematically;
- execute split/recombine tests;
- test corrupted/duplicate shares;
- benchmark large group layouts;
- validate every impossible threshold value;
- test every master-key backend inside mixed groups;
- verify backend audit behavior dynamically;
- perform a cryptographic security audit;
- prove that every CLI/config path enforces identical threshold validation.

The conclusions are source-level architecture observations, not independent cryptographic certification.

## Parent-candidate impact

SOPS remains **VERIFIED — provisional S / 28**.

This follow-up strengthens its architectural value. The key-group system provides a clean two-level policy model: redundancy within a group and Shamir quorum across groups. The main caveat is configuration semantics: reviewers must inspect actual group boundaries and threshold rather than assuming that a long list of configured master keys implies multi-party authorization.

## Strong next targets

- trace `.sops.yaml` creation-rule first-match behavior and precedence in detail;
- inspect threshold-specific upstream tests, including malformed threshold/group combinations;
- inspect `sops groups add/delete` behavior and whether group mutations force safe data-key rewrapping;
- inspect audit-event coverage during group recovery and key rotation;
- compare SOPS key-group semantics with envelope-encryption/quorum designs in other secret-management systems;
- trace the exact SOPS ↔ age boundary so age recipients inside a group are not confused with SOPS's cross-group Shamir policy.