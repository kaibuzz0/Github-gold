# SOPS key service — trust boundary and transport analysis

- Upstream repository: https://github.com/getsops/sops
- Parent candidate: SOPS
- Evidence level: VERIFIED source-level architecture notes
- Research date: 2026-08-27
- Scope: `keyservice/`, CLI transport wiring, and authorization assumptions

## Why this follow-up exists

The initial SOPS dossier identified `keyservice/` as a potentially reusable privilege-separation surface. This pass inspected the implementation closely enough to narrow that claim.

The key service is a useful provider-abstraction and process-separation mechanism, but the stock implementation should **not** be treated as a complete authenticated remote key-custody security boundary by itself. Its transport and prompt behavior place important security responsibilities on the deployment environment.

## Protocol surface

`keyservice/keyservice.proto` defines a small gRPC service with two methods:

- `Encrypt(EncryptRequest) -> EncryptResponse`
- `Decrypt(DecryptRequest) -> DecryptResponse`

Requests carry a typed key descriptor plus plaintext or ciphertext bytes. Supported key descriptors include AWS KMS, PGP, GCP KMS, Azure Key Vault, HashiCorp Vault Transit, age, and HuaweiCloud KMS.

This is architecturally attractive because callers can request key operations without embedding every provider implementation directly into the calling workflow.

## Server behavior

`keyservice/server.go` translates protobuf key descriptions into SOPS provider-specific `MasterKey` implementations and invokes their normal `Encrypt` or `Decrypt` methods.

Important boundary: the server therefore inherits the credential, IAM, local-key, agent, environment, and network trust assumptions of whichever provider implementation is selected. The gRPC layer does not remove those provider-specific trust boundaries.

## Critical prompt ordering detail

The optional `Server.Prompt` mode is **not a pre-operation authorization gate** in the inspected implementation.

For both `Encrypt` and `Decrypt`, the server:

1. selects the requested key type;
2. performs the provider encryption/decryption operation;
3. constructs the response;
4. only then calls `ks.prompt(...)` when prompting is enabled;
5. returns the response only if the operator answers yes.

This means an operator answering `n` can prevent the result from being returned to the caller, but the underlying key-provider operation has already occurred.

Practical implication: do not describe prompt mode as preventing use of a KMS/private-key operation. It is better understood as a post-operation release confirmation in the current source ordering.

This distinction can matter for:

- KMS/Vault audit logs;
- provider-side request costs or quotas;
- side effects associated with access attempts;
- threat models where merely invoking a key operation is security-sensitive.

GitHub Gold is recording this as an implementation fact, **not** as a vulnerability claim.

## Transport boundary

The key-service command creates a plain `grpc.NewServer()` over a listener selected by `Network` and `Address`.

The general SOPS CLI allows additional key services using syntax such as:

`tcp://myserver.com:5000`

The inspected CLI imports gRPC's `credentials/insecure` package for this remote-keyservice path. No TLS, mutual-TLS, token authentication, or application-level caller identity appears in the inspected key-service protobuf or server registration layer.

Therefore the stock remote service should not be assumed to provide confidentiality, server authentication, or caller authentication at this layer.

Deployment rule for GitHub Gold:

- local/in-process use is a different trust model from exposing the service over a network;
- remote deployments should rely on a protected transport/environment or add a separate authenticated transport/proxy/control layer;
- do not present the stock service as a hardened internet-facing KMS proxy.

## Local client path

`keyservice/client.go` also exposes `LocalClient`, which directly calls a `KeyServiceServer` implementation in-process rather than crossing gRPC.

That makes the abstraction useful even when no remote service is desired. A project can reuse the conceptual separation between key descriptions and key operations without introducing a network trust boundary.

The `NewCustomLocalClient` entry point is also useful architecturally because a caller can provide an alternate `KeyServiceServer` implementation.

## What the protobuf does not contain

The inspected protobuf includes key descriptors and Encrypt/Decrypt payloads, but does not itself define:

- caller identity;
- authorization policy;
- authentication tokens;
- certificate identity;
- request purpose/context beyond provider-specific fields;
- explicit audit metadata;
- rate-limit/quota policy;
- approval identity;
- tenant separation.

Those are deployment/application concerns around the stock protocol.

## Reusable architecture lessons

### 1. Keep provider operations behind a narrow interface

The typed request model cleanly hides AWS/GCP/Azure/Vault/PGP/age/HuaweiCloud implementation details from callers.

### 2. Separate local abstraction from remote transport

The same service interface can be called locally or over gRPC. This is a useful design pattern because process separation can be introduced without rewriting the higher-level secret-file workflow.

### 3. Authorization must be positioned before the sensitive operation if invocation itself matters

The current prompt ordering is an important general lesson. A confirmation step after a cryptographic/KMS operation can control disclosure of the result, but cannot prevent the underlying operation from occurring.

### 4. A narrow RPC schema is not automatically a hardened security service

Remote key custody needs explicit transport authentication, authorization, observability, rate limiting, and deployment controls. The SOPS schema is a useful primitive, not a complete zero-trust control plane.

## Verification boundaries

This pass inspected source only.

GitHub Gold did **not**:

- run a key service;
- capture gRPC traffic;
- perform a MITM test;
- test provider credentials or IAM behavior;
- execute prompt-mode operations against a real KMS;
- fuzz protobuf requests;
- perform an independent security audit;
- prove that no external proxy/deployment documentation can add stronger protections.

The transport/authentication conclusions are limited to the inspected stock code paths.

## Parent-candidate impact

SOPS remains **VERIFIED — provisional S / 28**.

This follow-up does not lower the overall candidate below promotion-ready status because the key service is an optional subsystem and the source is explicit enough to document its boundary accurately. It does, however, strengthen the canonical caveat that the remote key-service feature must not be advertised as an authenticated secure KMS gateway without additional controls.

## Strong next targets

- trace the exact remote `grpc.Dial`/connection-construction path and defaults end to end;
- inspect whether key-service tests exercise prompt ordering and network transport assumptions;
- inspect the tree MAC/integrity design and what metadata is authenticated;
- inspect Shamir key-group behavior and thresholds;
- inspect `.sops.yaml` creation-rule matching and policy precedence;
- compare SOPS's `age` backend boundary with direct age CLI/library use.
