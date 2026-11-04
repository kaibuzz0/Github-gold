# syncthing/syncthing — peer-to-peer file synchronization

- Repository: https://github.com/syncthing/syncthing
- Author/organization: Syncthing Project
- Category: local-first / peer-to-peer / file synchronization / offline-capable infrastructure
- Evidence level: VERIFIED
- Provisional Gold score: 29/30 (S)
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 5/5
  - Maintenance: 5/5
- Discovery: independent breadth expansion following the Termux/mobile-local-first research thread

## What it is

Syncthing is an open-source continuous file synchronization system. It synchronizes files directly between user-controlled devices rather than requiring a central cloud-storage service. Devices are identified cryptographically and device-to-device traffic is protected with TLS.

The project is valuable to GitHub Gold both as a complete tool and as a collection of reusable architectural components for local-first and resilient systems.

## Why it matters

Syncthing combines several properties that are unusually useful together: peer-to-peer synchronization, encrypted transport, automatic discovery/connection machinery, conflict/version handling, a REST control API, relay/discovery infrastructure, cross-platform builds, and operation without dependence on a single storage provider.

This makes it relevant to offline-first workflows, field systems, user-controlled backups/synchronization, multi-device development environments, local data pipelines, and resilient personal infrastructure.

## Working evidence inspected

The current GitHub Actions build workflow performs a build-and-test matrix on Windows, Ubuntu, and macOS using both supported Go generations (currently Go 1.26 and 1.27). The same workflow packages Syncthing and its discovery/relay servers for a broad set of targets. Linux packaging includes amd64, 386, arm, arm64, mips/mipsle, mips64/mips64le, riscv64, s390x, loong64 and ppc64le; separate packaging exists for Windows and illumos, with release signing paths for supported platforms.

The workflow also gates its aggregate basic-check job on tests, platform packaging, vulnerability checking, golangci and metadata checks. This is substantial upstream validation rather than a documentation-only claim.

Current repository activity remains strong. September 2026 commits include file-model error handling and documentation/release maintenance, and the project continues to carry active feature and protocol work.

## Security / architecture evidence

Upstream security documentation states that device-to-device traffic is protected by TLS and that peers are admitted by comparing certificate fingerprints represented as device IDs against configured devices. This is an important architectural distinction from account/password-centric cloud synchronization.

The project exposes a JSON-oriented REST API on the GUI port for control and integration. API-key or bearer-token authentication is supported. This makes Syncthing useful as an automation component rather than only an interactive end-user application.

## Valuable components / research surfaces

- core synchronization/model engine
- block transfer and pull scheduling
- file versioning/conflict handling
- filesystem abstraction and case-sensitivity handling
- device identity/certificate model
- encrypted peer transport
- local/global discovery mechanisms
- relay support and companion relay server
- REST API and event/control surfaces
- ignore-pattern engine
- database/index architecture
- static cross-platform packaging/build infrastructure
- automatic upgrade/signature machinery
- `stdiscosrv` and `strelaysrv` companion services

## Platforms / requirements

Core implementation is Go. Upstream CI directly tests Windows, Linux and macOS and packages a much broader architecture set. Runtime behavior and filesystem semantics vary by platform.

For Android specifically, the former official `syncthing-android` wrapper was discontinued and archived in December 2024. That does not make the core Syncthing project abandoned; the core remains actively maintained. Android deployment should therefore be treated separately from core project health and verified against currently maintained wrappers/packages before recommendation.

## Licensing

Repository root license: Mozilla Public License 2.0 (MPL-2.0).

MPL-2.0 is file-level copyleft. GitHub Gold copied no Syncthing source, binaries, protocol fixtures, or generated artifacts in this pass. Any future source extraction/adaptation must preserve MPL obligations and notices.

## Verification boundary

GitHub Gold inspected current repository metadata, upstream documentation/security material, licensing, recent commit activity, and the current build/test/package workflow. GitHub Gold did **not** clone or compile Syncthing, execute its test suite, synchronize files between devices, run discovery/relay infrastructure, inspect network traffic, validate release signatures, benchmark synchronization performance, or independently audit its cryptographic implementation.

`VERIFIED` means the project's architecture, maintenance, licensing and substantial upstream build/test evidence were verified from primary sources. It does not mean GitHub Gold independently reproduced every runtime or security claim.

## Caveats

- A peer-to-peer design does not remove the need for careful device authorization and GUI/API security.
- Synchronization is not identical to backup; deletions and unwanted changes can propagate unless versioning/backup policy is configured appropriately.
- NAT traversal and connectivity can depend on discovery and relay infrastructure when direct connectivity is unavailable.
- Filesystem behavior differs across platforms, especially case sensitivity, permissions, ownership and unsupported filename semantics.
- The former official Android wrapper is archived, so Android packaging is a separate maintenance/provenance question.

## Recursive research leads

1. Inspect the Block Exchange Protocol and message-validation boundaries as reusable synchronization protocol architecture.
2. Map local discovery, global discovery and relay fallback as a resilient connectivity stack.
3. Inspect `stdiscosrv` and `strelaysrv` as standalone self-hostable components.
4. Study block hashing, pull scheduling, rename detection and sparse synchronization optimizations.
5. Audit versioning/conflict behavior and clarify where synchronization ends and backup begins.
6. Map REST API and event interfaces for automation/agent integration.
7. Identify the best currently maintained Android/Termux deployment path without relying on the archived official Android wrapper.
8. Compare Syncthing with LocalSend, Resilio-like architectures, rsync-over-transport workflows and content-addressed synchronization systems while preserving trust/evidence distinctions.
