# Research dossier — file encryption and portable cryptographic tooling

Date: 2026-08-21

## age

- **Repository:** https://github.com/FiloSottile/age
- **Author / Org:** FiloSottile / age contributors
- **Category:** file encryption / cryptographic format / Go library / CLI
- **Evidence:** VERIFIED
- **Provisional tier / score:** S / 27
- **License:** BSD 3-Clause-style license in root `LICENSE`
- **Platforms:** Go-supported systems; upstream documents packaged/prebuilt support across major Linux distributions, macOS, Windows, FreeBSD, and OpenBSD

### What it does

`age` is a focused file-encryption tool, interoperable format, and Go library. Upstream documents public-key recipient encryption, passphrase encryption, SSH-key recipients, multiple recipients, streaming UNIX-style composition, hybrid post-quantum recipients, and an inspection command for encrypted-file metadata.

### Why it is valuable

The project is unusually composable: the CLI, file format, Go API, plugin interface, and independent implementations form a reusable encryption ecosystem rather than a single opaque application. It is especially useful as a reference for simple recipient-based encryption, portable encrypted archives, backup pipelines, and local-first/self-hosted systems that need encryption without a heavy PKI layer.

### Useful components / study targets

- `age` CLI encryption/decryption flow
- `age-keygen`
- `age-inspect` metadata inspection and JSON output
- Go library API (`filippo.io/age`)
- recipient / identity abstractions
- streaming encrypted-file format
- passphrase recipient support
- SSH recipient and identity support
- hybrid post-quantum recipient support
- plugin architecture
- Sigsum-backed release verification workflow
- C2SP format specification and interoperability model

### Ecosystem leads

- `str4d/rage` — interoperable Rust implementation
- `FiloSottile/typage` — TypeScript implementation for browsers, Node.js, Deno, and Bun
- `str4d/age-plugin-yubikey` — YubiKey/PIV integration
- `FiloSottile/awesome-age` — integrations, plugins, tools, and implementations
- C2SP `age-encryption.org/v1` specification

### Verification performed

- repository metadata inspected
- README inspected
- root `LICENSE` inspected
- recent commit history inspected
- upstream documentation for the C2SP specification, package installation, Sigsum proofs, post-quantum keys, SSH recipients, plugin ecosystem, and `age-inspect` observed
- GitHub Gold did **not** independently build, fuzz, cryptographically audit, benchmark, or interoperability-test age in this pass

### Maintenance signals

Recent inspected commits include March 20, 2026 correctness/cleanup work in the internal format and post-quantum inspection code, plus release-verification workflow maintenance earlier in 2026. Maintenance is real but less frequent than the most actively changing S-tier repositories, so the provisional score is held below the 28–29 range.

### Licensing / reuse caveats

The root project uses a permissive BSD-style license requiring retention of copyright/license notices and restricting endorsement with contributor/project names. Plugins, independent implementations, downloaded binaries, package-manager recipes, cryptographic dependencies, and external key hardware integrations may have separate terms and should be reviewed independently.

### Security caveat

Catalog inclusion is not an independent cryptographic audit. For high-assurance deployments, consumers should follow upstream security guidance, keep versions current, verify release provenance, and assess key-management and operational risks separately from the format/library design.
