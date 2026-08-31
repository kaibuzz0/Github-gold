# SOPS — tree MAC and integrity boundary

- Upstream repository: https://github.com/getsops/sops
- Parent candidate: SOPS
- Evidence level: VERIFIED source-level architecture notes
- Research date: 2026-08-27
- Scope: document tree integrity, MAC verification, authenticated metadata coupling, and selective-MAC caveats

## Why this follow-up exists

The parent SOPS dossier identified the structured document model as one of the project's strongest reusable ideas. This pass narrows exactly what SOPS means by document integrity and where the MAC boundary sits.

The important distinction is that SOPS does not merely encrypt values independently and trust the surrounding YAML/JSON structure. Its core tree model computes a document-level integrity value and verifies it during decryption.

## Upstream integrity model

The package-level source documentation states that a SOPS document is represented as a tree containing a data branch plus metadata carrying encryption and integrity information.

For structured JSON/YAML documents, keys remain visible while values are encrypted. This makes diffs and merges practical, but also means structural integrity cannot rely on ciphertext confidentiality alone.

SOPS therefore computes a Message Authentication Code over the document tree. Upstream explicitly states that the MAC covers:

- keys;
- values;
- ordering.

That ordering guarantee matters. Reordering entries is not treated as an integrity-neutral operation by the normal MAC model.

## Data-key coupling

SOPS generates a per-document data key and uses that data key to encrypt document values. The same data-key trust boundary also protects the document MAC.

This gives the format two related but distinct integrity layers:

1. individual encrypted values are protected by the configured cipher's authenticated-encryption behavior and associated data;
2. the document-level MAC protects the reconstructed tree as a whole.

The master-key backends protect access to the data key; they do not individually MAC every document node.

## Decrypt/verify path

The public stable Go decryption helper shows the verification sequence clearly:

1. load the encrypted file into a SOPS tree;
2. recover the data key from metadata;
3. decrypt the tree while calculating the cleartext-tree MAC;
4. decrypt the stored `MessageAuthenticationCode` using the data key;
5. compare the stored MAC with the recomputed MAC;
6. refuse to emit the plaintext file if they differ.

This is important operationally: successful key recovery and successful value decryption are not, by themselves, enough for the normal helper to return plaintext. The integrity comparison is a separate gate.

## LastModified coupling

The stored MAC ciphertext is decrypted using `Metadata.LastModified.Format(time.RFC3339)` as additional authenticated data in the public helper.

That means the stored encrypted MAC is not independent of the `lastmodified` metadata field. Changing that field without producing a corresponding valid MAC ciphertext causes the MAC-decryption/verification path to fail.

GitHub Gold records this as a useful design pattern: metadata that controls integrity verification can itself be cryptographically coupled to the integrity artifact rather than left entirely unauthenticated.

This pass did not attempt to enumerate every metadata field and should not be read as a claim that all SOPS metadata is authenticated by the document MAC.

## MAC mismatch behavior

The core package defines a `MacMismatch` error and the stable decryption helper returns an integrity-verification failure when the decrypted stored MAC and recomputed tree MAC differ.

Practical consequence:

- a structurally parseable SOPS file can still be rejected as tampered;
- successful KMS/age/PGP access does not bypass the document-integrity check;
- accidental edits to encrypted documents can surface as integrity failures rather than silently producing modified plaintext.

## Selective MAC mode

Current source contains a dedicated `MACOnlyEncryptedInitialization` marker and configuration support for `mac_only_encrypted`.

The source comment is explicit: this mode computes the MAC only over values that end up encrypted, and uses a distinct initialization value so a MAC generated with that setting is always distinguishable from the normal full-tree MAC mode.

This is a significant security/configuration boundary.

Normal mode gives the strongest interpretation of SOPS's package-level statement that the MAC covers keys, values, and ordering. When `mac_only_encrypted` is enabled, operators are deliberately choosing a narrower integrity scope.

GitHub Gold therefore should not summarize all SOPS files as having identical whole-document integrity without checking this setting.

## Cleartext-field caveat

SOPS supports intentionally unencrypted values through suffix/regex/comment-driven rules. Those features improve practical mixed public/secret configuration workflows, but they interact with integrity policy.

In the normal MAC mode, the package-level design says the tree MAC covers the document structure rather than only encrypted ciphertext values.

With `mac_only_encrypted`, intentionally cleartext values can fall outside the MAC scope by design.

That is not automatically a flaw; it is a policy choice. But it changes what downstream systems may safely assume about tamper detection for mixed encrypted/unencrypted configuration.

## Reusable architecture lessons

### 1. Preserve structure, then authenticate structure

Keeping YAML/JSON keys visible makes Git workflows much more usable, but visible structure should still participate in an integrity mechanism when the threat model requires it.

### 2. Separate field authentication from document authentication

Authenticated encryption of individual leaf values does not prove that an attacker has not deleted, duplicated, reordered, or substituted fields. A document-level MAC addresses a different problem.

### 3. Bind integrity metadata to context

Using `LastModified` as additional authenticated data for the stored MAC creates a cryptographic relationship between the integrity artifact and metadata used during verification.

### 4. Make weaker integrity modes explicit and domain-separated

SOPS's separate initialization marker for `mac_only_encrypted` is a good pattern: a narrower integrity policy should not accidentally produce artifacts indistinguishable from the stronger default mode.

### 5. Treat configuration as part of the security model

A statement like "SOPS verifies the MAC" is incomplete unless the active integrity configuration is known. `mac_only_encrypted` materially changes the scope of what is authenticated.

## Verification boundaries

This pass inspected upstream source/documentation paths only.

GitHub Gold did **not**:

- cryptographically audit the MAC construction;
- independently recompute a SOPS MAC;
- mutate real files and execute the CLI against them;
- test every structured format;
- test `mac_only_encrypted` behavior dynamically;
- prove which metadata fields beyond the observed `LastModified` coupling are authenticated;
- fuzz parser/order edge cases;
- verify resistance to cryptographic attacks.

The conclusions are architecture/source observations, not an independent cryptographic certification.

## Parent-candidate impact

SOPS remains **VERIFIED — provisional S / 28**.

This follow-up strengthens the candidate rather than lowering it: the project has a deliberate document-level integrity model and a clear verification path. The main caveat is now more precise: integrity guarantees depend on configuration, especially `mac_only_encrypted`, and GitHub Gold should preserve that distinction in any future canonical entry.

## Strong next targets

- inspect the exact tree-walk/MAC serialization rules for each scalar type and comments;
- inspect tests for key/value ordering and tamper detection;
- trace `mac_only_encrypted` configuration from `.sops.yaml` into metadata and verification;
- inspect Shamir key groups and threshold reconstruction;
- inspect `.sops.yaml` creation-rule matching and precedence;
- inspect audit-event behavior around decrypt/edit/key-service operations.
