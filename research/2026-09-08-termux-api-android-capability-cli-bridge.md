# termux/termux-api — Android capability-to-CLI bridge

- **Repository:** https://github.com/termux/termux-api
- **Author / organization:** Termux
- **Category:** Android / Termux / automation / mobile hardware API bridge / scripting
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **27/30 — S tier**
- **License:** **GPLv3 stated by upstream README; no standalone root LICENSE file observed in this inspection**
- **Discovery source:** recursive follow-up from `termux/termux-app` and `termux/termux-packages`; GitHub-first, with no YouTube-derived technical claim used in this pass

## Executive finding

`termux/termux-api` is the Android-side bridge that exposes mobile operating-system and hardware capabilities to Termux shell scripts and command-line programs. It converts Android APIs that normally require Java/Kotlin application code into callable primitives for battery state, location, sensors, camera, microphone, telephony, SMS, contacts, notifications, NFC, USB, Wi-Fi, biometric prompts, storage access, text-to-speech, speech-to-text and other device services.

Its strongest GitHub Gold value is not any one API wrapper. The reusable architecture is the **shell process → local socket pair → Android broadcast receiver → permission-gated API implementation → socket result** path, combined with Android's same-signing/shared-identity boundary between Termux and its plugin.

## Provisional 30-point Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Makes a broad set of Android device capabilities directly scriptable from Termux. |
| Working Evidence | 4/5 | Current CI builds APKs, validates output, emits SHA-256 checksums and publishes artifacts; formal releases exist. The inspected workflow did not expose a broad unit/instrumentation-test matrix. |
| Reusability | 5/5 | The API dispatcher, permission checks, result-return/socket pattern and many focused API wrappers are useful design references for Android automation bridges. |
| Novelty | 4/5 | Android API wrapping is established, but exposing a large mobile capability surface coherently to Unix-style scripts is unusually practical. |
| Documentation | 4/5 | README clearly documents the invocation architecture and installation/signing constraints; implementation knowledge is distributed across API classes and companion package scripts. |
| Maintenance | 5/5 | Active fixes landed on 2026-09-06 and the latest stable release inspected is v0.53.0 from 2025-09-01. |
| **Total** | **27/30** | **Provisional S** |

## What the repository provides

### Command-line access to Android capabilities

The upstream README defines the project as an app exposing Android APIs to command-line use and scripts/programs. The Android-side source contains focused classes for audio, battery, brightness, call logs, camera information/photos, clipboard, contacts, dialogs, downloads, fingerprint prompts, infrared, job scheduling, keystore operations, location, media, microphone recording, NFC, notifications, SAF/storage, sensors, SMS, speech, telephony, text-to-speech, torch, USB, vibration, volume, wallpaper and Wi-Fi.

This breadth makes it useful for user-controlled mobile automation, field tooling, accessibility workflows, sensor logging, offline data collection and hardware-assisted scripts without requiring each script author to write a standalone Android application.

### Socket-based command/result bridge

The README documents the companion `termux-api` helper binary creating two Linux anonymous namespace sockets and passing their addresses to `TermuxApiReceiver` through an Android broadcast. Those sockets carry stdin into the selected Android API implementation and return output to the shell process.

This is a compact interoperability pattern: retain Android privilege/API access inside an Android component while exposing a Unix-friendly stdin/stdout interface to shell tooling.

### Central API dispatcher and permission gating

`TermuxApiReceiver` dispatches on an `api_method` extra and routes requests to the corresponding focused API class. Permission-sensitive operations explicitly check/request Android permissions before invoking the implementation—for example camera, contacts, location, microphone, SMS, telephony and Wi-Fi scan operations.

The receiver also wraps execution in broad exception handling so failures do not escape the `BroadcastReceiver` and cause Android to mark the process bad; errors are logged/notified and result completion is signaled.

### Same-signing / shared-identity boundary

The upstream README states that the API app must be signed with the same key as the main Termux app for permissions to work, and that only the main Termux app is allowed to call its API methods. The manifest uses the Termux package identity as `sharedUserId`; the principal `TermuxApiReceiver` is `android:exported="false"`.

This is a critical architectural boundary rather than an installation footnote. The usefulness of Termux:API depends on privileged cooperation between two apps, so changing distribution/signing sources can break the relationship and can alter the trust boundary.

### Broad Android permission surface

The manifest requests access spanning location, camera, microphone, calls, contacts, SMS, NFC, USB, notification listeners, storage, settings, wallpaper, infrared and other capabilities. Many hardware features are marked optional so installation is not restricted to devices possessing every capability.

This breadth is the source of the project's utility and its principal security risk: compromise or incorrect authorization can expose highly sensitive device data and actions.

## Working and maintenance evidence

The current GitHub Actions build workflow runs on pushes, pull requests, periodic schedule and manual dispatch. It:

- checks out the repository;
- derives a semantic per-commit build version;
- executes `./gradlew assembleDebug`;
- verifies that the expected APK exists;
- generates `checksums-sha256.txt` with `sha256sum`;
- uploads the APK, checksum file and output metadata as workflow artifacts.

The latest stable release inspected is **v0.53.0, published 2025-09-01**. GitHub exposes SHA-256 digest metadata for both the release checksum file and APK asset. That release fixed a `BatteryStatusAPI` null-handling crash.

Development is still active. On **2026-09-06**, upstream landed fixes for microphone-recorder exception handling/null output and a dialog lifecycle bug caused by activity recreation after orientation changes.

## High-value reusable components and patterns

### `TermuxApiReceiver`

A concise central dispatcher for mapping shell-request method names to Android implementations while applying permission gates and failure containment.

### `ResultReturner`

This helper is a strong follow-up target because it sits at the Android-to-shell output boundary and handles return-data transport over the socket mechanism.

### Focused API classes

The `apis/` directory is a useful corpus of narrow Android integration examples. Particularly valuable candidates for deeper inspection include:

- `SensorAPI`
- `LocationAPI`
- `UsbAPI`
- `NotificationAPI` / `NotificationListAPI`
- `JobSchedulerAPI`
- `KeystoreAPI`
- `SAFAPI`
- `MicRecorderAPI`
- `SpeechToTextAPI`

### Companion `termux-api-package`

The Android APK is only half of the architecture. The shell-side helper binary and wrapper scripts live in `termux/termux-api-package` and should be evaluated independently to trace exact serialization, socket lifecycle, argument processing and failure behavior end-to-end.

## Licensing boundary

The upstream README states the project is released under **GPLv3**. During this inspection, the root directory listing did not expose a standalone root `LICENSE` file, so GitHub Gold records the README statement rather than asserting a stronger SPDX conclusion from a file that was not observed.

The application also depends on shared Termux components and the companion `termux-api-package`; exact reuse of files should therefore preserve per-file notices and verify dependency licensing rather than relying only on this dossier-level label.

No upstream source code, APKs, scripts or binaries were copied into GitHub Gold.

## Security and operational caveats

- The app requests a very broad set of sensitive Android permissions; misuse can expose location, contacts, messages, microphone/camera data and device actions.
- Correct signing relationship with the main Termux app is security-critical and operationally fragile when switching installation sources.
- GitHub debug builds and F-Droid/main Termux builds may use different signature keys; upstream explicitly warns that installation sources cannot be mixed without uninstalling Termux and plugins.
- The inspected CI uses mutable Action references such as `actions/checkout@v4` and `actions/upload-artifact@v4`, not immutable commit-SHA pins.
- Build success is not equivalent to runtime correctness across Android versions, vendors and permission-policy changes.
- Shell arguments, broadcasts, socket data, file paths and responses cross multiple trust/serialization boundaries and deserve fuzzing.
- Notification-listener, storage, USB, telephony, SMS and microphone functionality materially widen the attack/privacy surface.

## Verification performed in this pass

Performed:

- checked the active GitHub Gold branch/PR and searched for an existing Termux:API entry;
- inspected upstream README and documented socket/signing architecture;
- inspected workflow inventory and current APK build/checksum workflow;
- inspected stable releases and GitHub-provided digest metadata for v0.53.0 assets;
- inspected recent commits through 2026-09-06;
- inspected the Android API implementation directory;
- inspected the manifest permission/component surface;
- inspected `TermuxApiReceiver` dispatch, permission checks and exception handling;
- inspected root contents for licensing/documentation context.

Not performed:

- cloning or building Termux:API locally;
- installing the APK or pairing it with Termux on Android hardware;
- running Gradle/unit/instrumentation tests;
- exercising any device API;
- validating signature compatibility across distribution sources;
- independently hashing APK assets;
- fuzzing socket/broadcast/argument/result handling;
- testing behavior across Android versions or OEM permission implementations;
- auditing every API class for security/correctness;
- testing the companion `termux-api-package` helper binary.

## Strong recursive research leads

1. **`termux/termux-api-package`** — trace the C helper and shell wrappers into the Android receiver.
2. **`ResultReturner`** — socket protocol, lifecycle, encoding, errors and backpressure.
3. **Permission model** — same-signing/shared-user assumptions and Android version migration risk.
4. **USB API** — useful field-hardware bridge and parser/device trust boundary.
5. **Sensors/location** — low-power field telemetry patterns and permission semantics.
6. **JobScheduler** — Android background-execution limits and durable automation behavior.
7. **Notification listener/reply** — high-value automation with a sensitive trust surface.
8. **Keystore API** — safe use of Android-backed key material from shell workflows.
9. **Fuzzing** — malformed shell arguments, socket payloads, result JSON and API-specific inputs.
10. **Distribution provenance** — F-Droid vs GitHub debug builds and signature-chain implications.

## Verdict

**VERIFIED / provisional S / 27.**

`termux/termux-api` is genuine GitHub Gold for Android automation: it exposes a large mobile hardware/OS capability surface to ordinary shell scripts through a compact, composable bridge. Its score is held below the strongest infrastructure entries because the inspected CI evidence is primarily build/artifact validation rather than a broad automated correctness matrix, and because its privileged permission/signing architecture creates a large security and compatibility surface that requires careful handling.