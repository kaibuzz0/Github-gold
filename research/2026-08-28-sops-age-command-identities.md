# SOPS age command-backed identity boundary

Date: 2026-08-28

Project: https://github.com/getsops/sops

Status: source-level follow-up for existing **SOPS VERIFIED / provisional S / 28** candidate.

License context: SOPS is MPL-2.0.

This dossier contains research notes only. No upstream source code is copied.

## Why this follow-up matters

SOPS can obtain age and SSH-age private identity material by executing operator-configured helper commands. This is useful for integrating external secret stores, hardware wrappers, password managers, or custom credential brokers without writing plaintext private keys to the normal SOPS key files.

But a command-backed identity source has a materially different trust boundary from a static key file. This pass traces what SOPS actually executes, what environment the helper receives, what data comes back, and what failure/availability controls exist in the inspected implementation.

Primary upstream source inspected:

- `age/keysource.go`
- `age/keysource_test.go`

## Command-backed identity surfaces

Current SOPS defines two command-backed age identity mechanisms:

- `SOPS_AGE_KEY_CMD` — command whose stdout is interpreted as one or more age identities.
- `SOPS_AGE_SSH_PRIVATE_KEY_CMD` — command whose stdout is interpreted as an SSH private key for age-SSH decryption.

For both paths SOPS also supplies:

- `SOPS_AGE_RECIPIENT=<current recipient>`

This lets a helper choose the appropriate secret for the recipient SOPS is currently trying to decrypt.

## Execution model

The shared helper parses the configured command string with `google/shlex`, then invokes it with Go `exec.Command`.

That distinction matters:

- SOPS does **not** automatically execute the configured text through a shell.
- shell metacharacters therefore do not gain shell meaning merely because they appear in the configured string;
- an operator can still intentionally opt into shell evaluation by configuring a shell explicitly, for example `bash -c ...`.

The upstream tests demonstrate exactly that pattern when testing recipient-aware command behavior.

This is a useful defensive design property because the recipient is passed as an environment variable rather than being interpolated by SOPS into a shell command line.

## Environment boundary

The helper process inherits the entire SOPS process environment through `os.Environ()`, with `SOPS_AGE_RECIPIENT` appended for the command-backed identity paths.

Therefore a configured identity helper can observe not only the recipient but also any other environment variables visible to SOPS, potentially including cloud credentials, CI tokens, proxy settings, or other secrets supplied to the process.

This is not surprising for an operator-configured executable, but it is an important trust-boundary fact:

**granting control over `SOPS_AGE_KEY_CMD` or `SOPS_AGE_SSH_PRIVATE_KEY_CMD` is effectively granting code execution with SOPS's environment.**

GitHub Gold should not describe these variables as passive key-location settings.

## Output handling

For `SOPS_AGE_KEY_CMD`, SOPS captures the helper's stdout and feeds it into the age identity parser.

The parser accepts the supported age identity forms documented in the adjacent age-boundary dossier, including native X25519, hybrid post-quantum, and age-plugin identities.

For `SOPS_AGE_SSH_PRIVATE_KEY_CMD`, stdout is parsed as an SSH private key through the age SSH integration.

Current source explicitly rejects password-protected SSH keys returned by the command-backed SSH path; the parser returns an error indicating that encrypted private keys are unsupported there.

## Availability boundary: no explicit command timeout

The inspected helper uses `exec.Command`, not `exec.CommandContext`, and does not create its own timer around the child process.

Therefore the command-backed identity path has **no SOPS-level execution timeout in this helper**. A helper that blocks indefinitely can block the SOPS operation until the process exits or SOPS itself is externally interrupted.

This should be recorded as an operational availability boundary, not as a security vulnerability claim.

Operators integrating network-backed or interactive helpers should implement their own bounded timeout/retry behavior inside the helper or wrapper process if they require one.

## Availability boundary: stdout is buffered without an explicit local size cap

The helper uses Go's `cmd.Output()`, which captures the complete stdout result before SOPS parses it.

The inspected SOPS helper does not impose an explicit maximum output size before that buffering step.

A malfunctioning or hostile configured helper could therefore produce excessive output and consume memory. Again, this is best treated as a robustness/property-of-the-extension-boundary note rather than a vulnerability claim because the helper is already operator-configured executable code.

## Failure behavior

If command parsing fails, command execution fails, or the returned material cannot be parsed as an expected identity, SOPS records the corresponding identity-loading error.

The age key loader can aggregate identity-loading failures while also checking other configured identity locations. This means one failing identity source does not necessarily prevent decryption if another configured source provides a usable identity.

That is useful resilience, but it also means operators should distinguish:

- helper failure;
- helper returning no usable identity;
- another identity source successfully satisfying the decrypt operation.

A successful overall SOPS decrypt does not prove every configured identity helper succeeded.

## Recipient-routing behavior

The upstream tests specifically verify the `SOPS_AGE_RECIPIENT` contract.

A test configures `SOPS_AGE_KEY_CMD` to emit the private identity only when `SOPS_AGE_RECIPIENT` matches the expected public recipient. The matching recipient produces one usable identity; a non-matching recipient produces none.

That confirms this environment variable is not merely documentation—it is part of the tested integration contract for recipient-aware secret brokers.

## Existing upstream test coverage

The inspected `age/keysource_test.go` includes coverage for:

- loading native identities from environment and files;
- command-backed SSH identity success;
- command-backed age identity success;
- command execution failure;
- recipient-aware routing through `SOPS_AGE_RECIPIENT`;
- multiple identity sources;
- identity parsing failures;
- encrypted/passphrase-protected age identity behavior;
- user-config-directory behavior.

This is meaningful evidence for the identity-loading layer.

## Test/verification gaps from this pass

The inspected tests do not establish all operational properties of an external secret broker. This pass did not locate or execute tests specifically proving:

- a SOPS-enforced timeout for a hung identity command;
- a SOPS-enforced stdout byte limit for command output;
- environment minimization/sandboxing of the helper process;
- process privilege dropping;
- network isolation;
- command-backed age-plugin hardware interoperability end to end;
- concurrent helper behavior under many key attempts;
- cleanup behavior for child processes after external cancellation.

Absence from the inspected test path should not be overstated as absence from every possible upstream integration environment.

## Security model interpretation

The safe mental model is:

**The command-backed identity feature is an operator-controlled extension boundary, not a sandbox.**

SOPS supplies a recipient hint and expects valid identity material back. It does not attempt to confine the helper or treat it as untrusted code.

That has several practical consequences:

1. Do not allow untrusted input to control the command environment variables.
2. Treat the configured executable/script and its dependencies as part of the secrets trust boundary.
3. Remember that the helper inherits SOPS's broader environment.
4. Implement timeouts and output discipline in external/network-backed helpers where availability matters.
5. Prefer direct file/env identities when an external process boundary adds no value.
6. Prefer a narrowly scoped helper when external custody or hardware integration does add value.

## Relationship to the SOPS key service

This command-backed identity mechanism is separate from SOPS's optional gRPC key service.

The earlier key-service dossier established a provider-operation/process-separation abstraction with its own transport/authentication caveats.

The age command mechanism is lighter weight:

- no long-running RPC service is required;
- a child process is spawned to obtain identity material;
- the helper communicates through environment variables and stdout;
- the helper executes with the local SOPS process's OS-level permissions/environment unless the operator wraps it with additional confinement.

These two mechanisms should not be collapsed into one concept in the catalog.

## License/reuse boundary

The execution and identity-loading implementation is SOPS MPL-2.0 source.

No source was copied into GitHub Gold. Any future adaptation of covered SOPS source must preserve applicable MPL-2.0 file-level obligations and notices.

The underlying age library remains separately licensed as recorded in the age dossier.

## Verification boundary

GitHub Gold inspected current upstream source and tests only.

This pass did not:

- build or run SOPS;
- execute a real `SOPS_AGE_KEY_CMD` helper;
- connect a password manager, cloud secret store, HSM, or hardware token;
- simulate a hung helper;
- generate unbounded stdout;
- measure memory use;
- inspect OS child-process behavior after forced cancellation;
- test Windows command parsing;
- audit `google/shlex` or Go `os/exec` independently;
- validate third-party age plugins.

Claims are limited to the inspected source structure and upstream tests.

## Candidate impact

SOPS remains:

- Evidence: **VERIFIED**
- Provisional Gold score: **28 / 30**
- Tier: **S**
- License: **MPL-2.0**

No score change is justified. This pass improves the catalog's trust-boundary and operational-robustness notes without implying that command-backed identities are unsafe by design.

## Reusable design lessons

1. Pass resource/recipient selectors to credential helpers through a structured side channel such as environment variables rather than shell interpolation.
2. Avoid implicit shell execution for extension hooks; require an explicit shell when shell semantics are desired.
3. Document inherited environment access as part of the helper's trust boundary.
4. Bound external helper execution time when a blocking dependency can stall the primary operation.
5. Bound helper output when stdout is captured into memory.
6. Keep external identity discovery separate from the core encrypted-document model.
7. Test recipient routing and failure behavior, not only the happy path.

## Strong next leads

1. Inspect age-plugin and hybrid-PQ coverage in SOPS tests to determine which recipient families are verified beyond parsing.
2. Inspect child-process cancellation semantics and whether higher SOPS layers ever wrap identity loading with cancellable context.
3. Trace `updatekeys` behavior across plugin, SSH, and hybrid-PQ age recipient records.
4. Inspect age's current release/signing/Sigsum supply-chain verification workflow.
5. After one more bounded SOPS follow-up, broaden discovery into a different category to avoid over-concentrating the catalog.