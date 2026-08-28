# SOPS and age architectural boundary

Date: 2026-08-28

Projects:

- https://github.com/getsops/sops
- https://github.com/FiloSottile/age

Status: source-level follow-up for existing **SOPS VERIFIED / provisional S / 28** candidate and previously researched **age VERIFIED / provisional S / 27** candidate.

License context:

- SOPS: MPL-2.0
- age: permissive BSD-style 3-clause license

This dossier contains research notes only. No upstream source code is copied.

## Why this follow-up matters

SOPS and age are often described together, but they occupy different architectural layers. Treating SOPS as if it simply stores an ordinary age-encrypted document obscures SOPS's own tree, metadata, MAC, key-group, Shamir-threshold, updatekeys, and rotation semantics.

This pass asks a narrower question: exactly what does SOPS delegate to age, and what policy remains owned by SOPS itself?

Primary upstream source inspected:

- SOPS `age/keysource.go`
- SOPS `go.mod`
- age `README.md`
- age root `LICENSE`

## Dependency boundary

Current SOPS main directly depends on:

- `filippo.io/age v1.3.1`

The SOPS age key source imports the core age package plus:

- `filippo.io/age/agessh`
- `filippo.io/age/armor`
- `filippo.io/age/plugin`

This is a real library integration rather than a shell-out to the standalone `age` CLI for normal wrapping/unwrapping.

## What age does inside SOPS

SOPS's `age.MasterKey` represents one configured age recipient plus the encrypted SOPS data key associated with that recipient.

Its source-level contract is explicit: the master key exists to encrypt and decrypt **SOPS's data key**.

On encryption, SOPS:

1. parses the configured age recipient;
2. creates an age encryption writer for that recipient;
3. writes the SOPS data key into that age stream;
4. ASCII-armors the resulting age ciphertext;
5. stores that armored ciphertext in the SOPS master-key metadata as the encrypted data key.

On decryption, SOPS:

1. loads or uses already parsed age identities;
2. opens the armored age ciphertext stored in the master-key metadata;
3. calls the age library's decrypt path with those identities;
4. recovers the SOPS data key;
5. returns that data key to the higher-level SOPS document-decryption machinery.

Therefore, age is functioning as a **data-key wrapping/unwrapping provider inside SOPS**, not as the complete structured-document encryption layer.

## What remains SOPS-owned

The prior GitHub Gold SOPS dossiers establish that SOPS separately owns or coordinates:

- structured document traversal and selective encryption;
- the document MAC/integrity policy;
- storage of encryption metadata;
- key groups;
- Shamir splitting and threshold reconstruction across groups;
- creation-rule selection from `.sops.yaml`;
- `updatekeys` recipient-policy reconciliation;
- full data-key rotation;
- direct group add/delete workflows;
- built-in audit-event handling.

None of those higher-level policies should be attributed to age merely because an age recipient is one available SOPS master-key type.

## Recipient types SOPS accepts through age

Current `parseRecipient` logic supports several age-compatible recipient families:

- native X25519 age recipients beginning with the normal `age1...` form;
- hybrid post-quantum recipients using the current `age1pq1...` prefix;
- age-plugin recipients;
- SSH recipients beginning with `ssh-`, parsed through `agessh`.

The corresponding identity side supports:

- native `AGE-SECRET-KEY-1...` identities;
- hybrid `AGE-SECRET-KEY-PQ-1...` identities;
- `AGE-PLUGIN-...` identities;
- SSH private-key identities through the dedicated SSH-loading paths.

This means SOPS inherits a meaningful portion of age's recipient/identity ecosystem while still controlling the document policy around those recipients.

## SOPS-specific identity discovery

SOPS adds its own runtime identity-discovery conventions around the age library.

Current source can obtain age material from mechanisms including:

- `SOPS_AGE_KEY`;
- `SOPS_AGE_KEY_FILE`;
- `SOPS_AGE_KEY_CMD`;
- the default user config path `sops/age/keys.txt`;
- `SOPS_AGE_SSH_PRIVATE_KEY_FILE`;
- `SOPS_AGE_SSH_PRIVATE_KEY_CMD`;
- default SSH private-key locations such as `~/.ssh/id_ed25519` and `~/.ssh/id_rsa`.

The command-backed mechanisms are SOPS integration behavior, not properties of the standalone age file format itself.

## Standalone age multi-recipient semantics

The age README documents ordinary standalone encryption to multiple recipients by repeating `-r/--recipient`.

In that model, **every listed recipient can independently decrypt the age-encrypted file**.

That is useful to compare with SOPS key-group behavior, but the two policy layers are not identical.

## SOPS key groups versus age recipient lists

Earlier SOPS source inspection established:

- master keys within one SOPS key group are alternatives;
- Shamir threshold applies across SOPS groups.

An age recipient configured as one SOPS master key therefore participates in SOPS's group policy exactly like another master-key provider at that layer.

A useful mental model is:

- **age recipient semantics:** determine who can unwrap one age-wrapped share/data-key value;
- **SOPS group semantics:** determine which master keys can satisfy a group;
- **SOPS Shamir threshold:** determines how many distinct groups must contribute shares to reconstruct the document data key.

Putting two age recipients into the same SOPS group does not create a 2-of-2 age quorum. Either master key may satisfy that group's contribution.

True multi-party/quorum policy in SOPS is created by distinct groups plus a threshold, not by the standalone age multiple-recipient feature alone.

## One-recipient wrapper objects versus standalone age multi-recipient files

The inspected SOPS `age.MasterKey` stores one recipient string and one corresponding encrypted data-key blob.

SOPS's `MasterKeysFromRecipients` parses a comma-separated recipient list into multiple SOPS `MasterKey` objects rather than creating one age ciphertext addressed to all recipients at once.

This is an important implementation distinction:

- standalone age can construct one age file with multiple recipient stanzas;
- SOPS models age recipients as individual master-key records in SOPS metadata and lets SOPS's own key-group machinery combine them.

That design allows age recipients to coexist with KMS, PGP, Vault, or other SOPS master-key providers inside the same higher-level policy model.

## Plugin and hardware boundary

The standalone age project documents a plugin ecosystem, including hardware-backed integrations such as YubiKey/PIV through age plugins.

SOPS current source recognizes plugin recipient and identity forms using `filippo.io/age/plugin`, so plugin-backed age identities can participate in the SOPS age key-source layer.

However, GitHub Gold should distinguish:

- support exposed by the age plugin protocol/library;
- a particular third-party plugin's hardware/security properties;
- SOPS's use of that plugin identity as one master key in its own policy.

A plugin being compatible with age does not make SOPS the security implementation of that hardware plugin.

## Cryptographic-claim boundary

GitHub Gold should not describe SOPS as implementing age's cryptographic format itself. Current source delegates recipient parsing and age encrypt/decrypt operations to `filippo.io/age` and related age packages.

Likewise, GitHub Gold should not describe age as implementing SOPS's document MAC, Shamir group threshold, configuration rules, or recipient-reconciliation workflows.

The projects are composable but architecturally distinct.

## License boundary

The inspected age repository root license is permissive BSD-style with source/binary notice preservation and non-endorsement conditions.

SOPS itself remains MPL-2.0.

Because SOPS links to/imports age as a Go dependency, any future code-reuse work must track the license of the specific source being copied or modified rather than assigning SOPS's MPL-2.0 license to upstream age code or vice versa.

No code is copied into GitHub Gold in this pass.

## Verification boundary

GitHub Gold inspected current upstream source and documentation only.

This pass did not:

- build SOPS or age;
- run SOPS with age recipients;
- generate or decrypt an age-wrapped SOPS data key;
- exercise plugin or hardware-backed identities;
- test SSH identities;
- test hybrid post-quantum recipients;
- compare emitted SOPS metadata byte-for-byte with standalone age CLI output;
- independently audit age cryptography;
- independently validate interoperability with rage, Typage, or third-party plugins.

The claims are limited to the inspected source/API structure and upstream documentation.

## Candidate impact

SOPS remains:

- Evidence: **VERIFIED**
- Provisional Gold score: **28 / 30**
- Tier: **S**
- License: **MPL-2.0**

age remains a separately valuable project rather than being collapsed into the SOPS entry. The two candidates expose different reusable surfaces:

- **age:** file-encryption format, Go cryptographic API, recipient/identity abstraction, plugins, standalone CLI and interoperable ecosystem;
- **SOPS:** structured-secret management, document policy/integrity, multi-provider master-key orchestration, threshold groups, policy reconciliation, editing and operational workflows.

## Reusable design lessons

1. Separate content encryption from key wrapping so key providers remain replaceable.
2. Model external recipient systems behind a common master-key interface when heterogeneous providers must coexist.
3. Do not confuse recipient redundancy with quorum policy; quorum belongs at an explicit policy layer.
4. Keep provider-specific identity discovery outside the core document model.
5. Record dependency and license boundaries at the component level, not only at repository level.
6. Catalog integrations as composition of distinct responsibilities rather than merging two projects into one conceptual system.

## Strong next leads

1. Inspect SOPS age-specific unit/integration tests for plugin, SSH, hybrid-PQ, and multiple-recipient coverage.
2. Inspect whether SOPS preserves enough recipient/plugin metadata for deterministic `updatekeys` reconciliation across all age recipient types.
3. Compare SOPS command-backed identity loading with age's native identity-file and plugin mechanisms from a secrets-exposure/process-boundary perspective.
4. Inspect age's current release/signing/Sigsum verification workflow as a supply-chain follow-up.
5. Return to broader GitHub-first discovery after the SOPS batch reaches a natural stopping point rather than over-concentrating the catalog on one subsystem.
