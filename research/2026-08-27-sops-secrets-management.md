# SOPS — structured secrets-management architecture

- Repository: https://github.com/getsops/sops
- Evidence level: VERIFIED
- Provisional Gold score: 28/30
- Provisional tier: S
- Category: secrets management / encrypted configuration / developer infrastructure
- License: Mozilla Public License 2.0
- Discovery mode: independent GitHub-first research
- Research date: 2026-08-27

## Executive assessment

SOPS is a mature encrypted-file editor and Go codebase for keeping structured configuration encrypted while preserving enough document structure for practical review and version-control workflows. It supports YAML, JSON, ENV, INI, and binary files and can protect data keys with AWS KMS, GCP KMS, Azure Key Vault, HuaweiCloud KMS, age, and PGP.

The project is high-value for GitHub Gold because it is not merely a CLI wrapper around one cryptographic provider. The repository contains a reusable document/tree encryption model, provider-specific key-source packages, data-key rotation/update workflows, a protobuf/gRPC-style key-service boundary, format stores, auditing hooks, and a substantial command surface for edit/encrypt/decrypt/set/unset/rotate/updatekeys/publish operations.

SOPS is CNCF Sandbox software and was originally launched at Mozilla. The current upstream remains actively maintained.

## Gold score

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Utility | 5/5 | Solves a common secrets-in-Git/configuration problem across multiple structured formats and key backends. |
| Working evidence | 5/5 | Mature release history, packaged releases, active upstream maintenance, documented security-reporting process, CI/release infrastructure. |
| Reusability | 4/5 | Strong Go package/component boundaries, but MPL-2.0 file-level copyleft requires care when source is copied or modified. |
| Novelty | 4/5 | The structured-file + envelope-key approach is established but remains technically valuable and unusually composable. |
| Documentation | 5/5 | Dedicated documentation site plus README, changelog, examples, package-level code surfaces, release metadata. |
| Maintenance | 5/5 | Main branch was still receiving feature and CI maintenance on 2026-08-26. |

Total: **28/30 — provisional S tier**.

## Upstream evidence inspected

### README / project status

The upstream README states that SOPS edits encrypted YAML, JSON, ENV, INI, and binary files and supports AWS KMS, GCP KMS, Azure Key Vault, HuaweiCloud KMS, age, and PGP. It also identifies the repository as MPL-2.0 and a CNCF Sandbox project.

### Current release

The latest release located during this pass is **v3.13.3**, published **2026-07-23**. Release assets include native packages/binaries, checksums, SPDX SBOM artifacts, and Sigstore-related release material.

### Fresh maintenance

The current main branch includes a **2026-08-26** merged feature adding encrypted/unencrypted comment-regex controls to `sops encrypt`. Additional recent work includes CI dependency maintenance. This is fresh code/maintenance evidence rather than popularity alone.

## Component-level targets

### 1. Core structured document/tree encryption

- `sops.go`
- format/tree handling used by encrypt/decrypt/edit/set/unset flows

Why it matters: SOPS keeps document structure visible while encrypting selected values, which is more useful for configuration review than treating every file as one opaque ciphertext blob.

Research value:
- tree traversal and selective encryption
- metadata handling
- data-key lifecycle
- integrity/MAC handling
- format-independent encrypted-document model

### 2. Key-source backends

Repository-level provider directories include integrations such as:

- `age/`
- cloud KMS provider packages
- PGP-related key handling

Why it matters: these packages demonstrate a pluggable envelope-encryption model where a randomly generated file/data key is protected by one or more external key sources rather than hard-wiring the file format to one provider.

The `age/keysource.go` surface is particularly relevant because GitHub Gold already tracks `age` as a separate cryptographic-format/tool candidate.

### 3. Key service boundary

Inspected code-search results show:

- `keyservice/keyservice.proto`
- `keyservice/keyservice.go`
- `keyservice/client.go`
- `keyservice/server.go`
- `cmd/sops/subcommand/keyservice/keyservice.go`

Why it matters: SOPS can separate encryption/decryption key operations behind a service boundary. This is a useful reference for privilege separation, remote key custody, hardware/KMS bridging, or environments where the process editing a file should not directly own every private key implementation.

Follow-up target: inspect authentication assumptions and transport/security expectations before treating the key-service pattern as production-safe outside its intended deployment model.

### 4. Key lifecycle / rotation tooling

Relevant command surfaces include:

- `cmd/sops/rotate.go`
- `cmd/sops/subcommand/updatekeys/updatekeys.go`
- group-management commands under `cmd/sops/subcommand/groups/`

Why it matters: secret-management systems are only useful if recipient/key changes and rotations are operationally manageable. These commands are strong reusable references for separating content encryption from recipient metadata/key wrapping.

### 5. Structured editing commands

Relevant files located during source search include:

- `cmd/sops/encrypt.go`
- `cmd/sops/decrypt.go`
- `cmd/sops/edit.go`
- `cmd/sops/set.go`
- `cmd/sops/unset.go`
- `cmd/sops/subcommand/publish/publish.go`

Why it matters: this is the practical workflow layer that allows encrypted configuration to remain editable, scriptable, and CI-friendly rather than being a one-shot encryption utility.

### 6. Audit / policy surfaces

The root repository contains an `audit/` package and dedicated security-reporting guidance.

Follow-up target: inspect exactly what audit events are emitted and how they interact with key-service and editing workflows before assigning independent security-control claims.

## Reuse / licensing boundary

The root license is **Mozilla Public License 2.0**.

Practical GitHub Gold rule:

- linking, documenting, and studying the architecture is straightforward;
- copying or modifying covered source files requires preserving MPL notices and making modified covered source files available under MPL-2.0 when distributed;
- a larger work may combine MPL-covered files with differently licensed files, but the MPL-covered source files retain their obligations;
- do not strip copyright/license notices.

Because this is not an MIT/BSD/Apache-only project, component extraction should be deliberate and license-aware.

## Security boundaries and caveats

- SOPS is security-sensitive software. Repository maturity is not equivalent to an independent cryptographic audit by GitHub Gold.
- GitHub Gold did **not** independently cryptographically audit the algorithms, key-service design, provider integrations, MAC behavior, editor temp-file behavior, or cloud-KMS trust boundaries in this pass.
- GitHub Gold did **not** build or run SOPS, execute its test suite, perform cross-provider interoperability tests, or test failure/recovery behavior.
- SOPS protects secrets at rest in files; it does not by itself solve endpoint compromise, malicious editors/processes, cloud-provider compromise, runtime secret exposure, or poor key-access policy.
- PGP, KMS, age, and remote key-service trust models differ and should not be treated as interchangeable operationally.

## Why it belongs in GitHub Gold

SOPS is valuable both as a finished tool and as a source architecture reference. Particularly reusable ideas are:

1. structured selective encryption instead of opaque whole-file blobs;
2. envelope encryption with multiple independent key-source providers;
3. recipient/key rotation without rewriting the application configuration model;
4. remote key-operation service boundaries;
5. editing/CI workflows designed around encrypted configuration in version control;
6. release provenance/SBOM practices for security-sensitive tooling.

## Related GitHub Gold candidates

- `FiloSottile/age` — cryptographic file format/tool/library used as one SOPS key source
- `getsops/sops` should remain a separate entry because SOPS is the higher-level structured-secret workflow and multi-provider envelope layer, while age is the lower-level file-encryption format/library/CLI.

## Strong recursive leads

- inspect `keyservice/` protocol and threat model in depth;
- inspect SOPS tree/MAC design and how integrity metadata is computed and verified;
- map the file-format stores and comment-preservation behavior across YAML/JSON/ENV/INI;
- inspect creation-rule matching in `.sops.yaml` and recipient-group policy mechanics;
- inspect audit integration and whether it can provide useful local/remote key-use observability;
- compare SOPS with Mozilla/Google-style secret-management alternatives without collapsing projects that solve different layers;
- inspect release-signing/SBOM pipeline as a reusable supply-chain reference.

## Promotion recommendation

**VERIFIED — provisional S / 28 — promotion-ready as a catalog candidate.**

Do not claim independent cryptographic verification. Preserve the MPL-2.0 boundary prominently in any canonical entry.