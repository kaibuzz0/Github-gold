# termux/termux-app — Android Linux terminal/runtime integration platform

- **Repository:** https://github.com/termux/termux-app
- **Author / organization:** Termux
- **Category:** Android / Termux / local-first computing / developer tooling / automation platform
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **26/30 — S tier**
- **License:** **GPL-3.0-only** for the repository, with documented Apache-2.0 terminal-emulator/view exceptions and additional `termux-shared` licensing exceptions that require exact-file review
- **Discovery source:** GitHub-first category rotation; no YouTube-derived technical claim used in this pass

## Why this is GitHub Gold

Termux is more than a terminal emulator. The app is the Android-side execution and integration shell around a Linux-style userland: terminal UI/emulation, session/process management, bootstrap installation, Android intent/service bridges, plugin integration, storage/environment conventions, and a reusable shared library used across the Termux application family.

The repository's own README explicitly distinguishes the app from `termux/termux-packages`, which supplies the packages installed inside the environment. That separation is architecturally useful: `termux-app` provides the Android host/runtime boundary, while the package ecosystem provides userland software.

The project is especially valuable for low-cost, portable and offline-capable computing because it turns ordinary Android devices into programmable Unix-like workstations without requiring a conventional desktop Linux installation.

## Provisional 30-point Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | General-purpose terminal/Linux environment on Android; useful for shells, scripting, development, local servers, automation and device-side workflows. |
| Working Evidence | 4/5 | Dedicated Gradle unit-test CI plus multi-variant APK build CI and artifact validation. Strong build evidence, but the inspected hosted CI is not a broad physical-device/instrumentation matrix. |
| Reusability | 5/5 | Reusable terminal emulator/view libraries, `termux-shared`, Android command/service bridges, plugin architecture, and a large companion ecosystem. |
| Novelty | 4/5 | The individual primitives are established, but the Android-native Linux runtime + terminal + plugin/intent integration is unusually coherent and broadly useful. |
| Documentation | 5/5 | Extensive installation, security, compatibility, plugin, debugging, file-layout and integration documentation. |
| Maintenance | 3/5 | Security maintenance is current through 2026-08-24, but formal app releases are comparatively slow; the newest GitHub release inspected is a 2025 beta and the README still describes v0.118.3 as the latest stable version. |
| **Total** | **26/30** | **Provisional S** |

## What the project actually provides

### Android terminal + Linux environment host

The upstream README describes Termux as an Android terminal application and Linux environment. The app repository owns the user interface and terminal emulation, while installable Unix packages are maintained separately in `termux/termux-packages`.

The installation model includes bootstrap archives that seed the initial shell environment. Supported production use is documented primarily for Android 7+, with older Android 5/6 app compatibility retained without current package-update support.

### Reusable terminal libraries

The repository contains dedicated `terminal-emulator` and `terminal-view` libraries. These derive in part from Terminal Emulator for Android and are explicitly called out as Apache-2.0 licensing exceptions to the GPL-3.0-only repository default.

This separation is useful for projects needing terminal-state parsing/rendering or an embeddable Android terminal view without adopting the entire Termux application.

### `termux-shared`

`termux-shared` is a reusable internal/common library for shared Termux application functionality. Exact-file licensing must be checked against `termux-shared/LICENSE.md` before extraction or reuse.

### Android integration / command execution

Termux exposes integration surfaces allowing other Android applications and companion plugins to initiate controlled commands and exchange results. The README links dedicated documentation for the `RUN_COMMAND` intent.

This is one of the project's highest-value reusable architecture patterns because it bridges Android's application/service/intent model with a Unix command environment.

It is also a security-sensitive trust boundary. A 2026-08-24 upstream security commit changed `RunCommandService` so file-based result output is not honored before the `allow-external-apps` property is verified. The commit states that the existing `RUN_COMMAND` permission check remains enforced, but closes an additional result-path/configuration exposure.

### Companion plugin ecosystem

The core README identifies optional companion applications:

- Termux:API
- Termux:Boot
- Termux:Float
- Termux:Styling
- Termux:Tasker
- Termux:Widget

These should be treated as related repositories rather than folded automatically into this candidate's score. They create strong recursive research opportunities around Android API access, boot-time jobs, automation, UI surfaces and home-screen command launchers.

## Build and verification evidence

### Unit-test CI

The current `Unit tests` workflow runs on pushes and pull requests for the main development branches, checks out the repository, installs Temurin Java 17 and executes:

```text
./gradlew test
```

This is explicit automated test execution rather than a build-only signal.

### APK build matrix

The current build workflow runs two package variants:

- `apt-android-7`
- `apt-android-5`

It builds debug APKs and explicitly checks that APK outputs exist for:

- universal
- arm64-v8a
- armeabi-v7a
- x86_64
- x86

It then generates a SHA-256 sums file and uploads the architecture-specific/universal APKs and checksum artifact.

This is meaningful reproducible build evidence across Android CPU architectures, although it should not be confused with runtime testing on all those architectures.

### Additional CI hygiene

The workflow inventory also includes dedicated Gradle-wrapper validation and dependency-submission workflows.

A supply-chain caveat remains: inspected workflows use mutable major-version GitHub Action references such as `actions/checkout@v6`, `actions/setup-java@v5`, and `actions/upload-artifact@v6`, not immutable commit-SHA pins.

## Releases and maintenance

The newest GitHub Release returned by the inspected releases endpoint is **v0.119.0-beta.3**, published **2025-05-22**, and marked prerelease. Its APK assets do not expose GitHub `digest` metadata in the inspected API response, although the project workflow itself generates and publishes SHA-256 checksum files for the APK set.

The README states **v0.118.3** as the latest stable version. This relatively slow formal release cadence is the main reason Maintenance is scored 3/5 instead of 4-5/5.

Repository maintenance itself is newer. The newest inspected commit is **2026-08-24** and is explicitly security-related: it hardens `RunCommandService` handling of file-based result configuration relative to the `allow-external-apps` setting. That commit is GitHub-verified with a valid signature.

## Security and operational caveats

### GitHub APK signing model

Upstream explicitly warns that GitHub-hosted Termux APKs are signed with a community-known **test key**, not a private official developer key. This means third parties can create APKs signed with the same test key. Users should obtain those builds only from trusted upstream channels and should not treat possession of that signing key as authenticity proof.

This is a significant distribution-security caveat and must remain visible in any catalog entry.

### Installation-source mixing

Termux and its plugins use a shared Android UID model and therefore must be signed compatibly. Upstream warns against mixing F-Droid, GitHub and other APK sources. Switching source generally requires uninstalling all Termux-family APKs first, with backup/restore implications.

### Android process restrictions

The README documents Android 12+ phantom-process and excessive-CPU restrictions that can terminate Termux subprocesses. This is an OS/platform constraint, not necessarily a Termux defect, but it materially affects long-running agents, servers and automation.

### External command trust boundary

`RUN_COMMAND`, plugin IPC, file/result exchange and API bridges should be treated as high-value integration points and security boundaries. The August 2026 hardening commit demonstrates that these paths receive active security attention but also deserve dedicated review and adversarial testing.

## Licensing

The root licensing document states **GPLv3 only**.

Documented exceptions include:

- Terminal Emulator for Android-derived material in `terminal-view` and `terminal-emulator`: Apache-2.0.
- `termux-shared`: additional exceptions documented in its own license file.

Do not copy individual components based only on the repository-level GPL label. Inspect exact files and notices first.

No upstream source code, APKs, bootstrap archives or package artifacts were copied into GitHub Gold in this pass.

## Verification performed in this pass

Performed:

- inspected upstream repository metadata and current default branch;
- inspected README architecture/install/plugin/security documentation;
- inspected root licensing documentation;
- inspected workflow inventory;
- inspected unit-test workflow;
- inspected APK build/output/checksum workflow;
- inspected recent GitHub release metadata;
- inspected recent commit history including the 2026-08-24 `RunCommandService` security hardening commit;
- checked GitHub Gold's active draft PR for duplicates before adding this dossier.

Not performed:

- cloning or locally building Termux;
- executing Gradle tests;
- installing APKs;
- running Termux on Android hardware/emulators;
- validating bootstraps or package repositories;
- testing F-Droid/Google Play/GitHub migration paths;
- exercising `RUN_COMMAND` or plugin IPC;
- reproducing the August 2026 security issue;
- independently hashing APKs;
- validating signing certificates beyond upstream documentation;
- fuzzing terminal escape sequences, intents, files, IPC or command-result handling;
- security auditing Android services/providers/receivers.

## Strong recursive research leads

1. **termux/termux-packages** — package build system, cross-compilation recipes, patches, mirrors, bootstrap creation and reproducibility.
2. **termux/termux-api** — Android API-to-shell bridge and permission boundaries.
3. **Termux:Boot** — boot-time automation and Android background-execution constraints.
4. **Termux:Widget** — reusable homescreen/launcher command execution model.
5. **`RUN_COMMAND` path** — permission, allowlist/configuration, output destination and intent-validation semantics.
6. **`termux-shared`** — reusable environment/filesystem/process/Android integration utilities.
7. **terminal-emulator / terminal-view** — escape-sequence parser, terminal state machine, rendering and malformed-sequence fuzzing.
8. **bootstrap integrity** — provenance from `termux-packages` release generation through first-run installation.
9. **Android 12+ process survival** — behavior under phantom-process and CPU trimming for legitimate long-running services/agents.
10. **Termux plugin signing/shared UID model** — security and migration implications as Android platform rules evolve.

## Verdict

**VERIFIED / provisional S / 26.**

Termux earns a high catalog rank because it is a practical Android computing substrate with reusable terminal, Android-integration and plugin architecture rather than merely a command prompt. It loses points relative to the strongest 29/30 candidates because formal release cadence is slow, GitHub-distributed APK authenticity relies on an intentionally shared test key, and the inspected CI provides strong build/unit-test evidence but not broad device-level behavioral validation.
