# Termux:API — Android command-line and scripting bridge

- **Repository:** https://github.com/termux/termux-api
- **Author / organization:** Termux
- **Category:** Android / Termux / automation / device integration
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 27/30
- **Provisional tier:** S
- **License:** GPLv3 (upstream README)
- **Discovery:** Independent GitHub-first discovery; selected to broaden the current research batch beyond network-security and PKI tooling.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Bridges Android platform capabilities into shell scripts and command-line programs. |
| Working Evidence | 4/5 | Upstream CI builds debug APKs on pushes/PRs and on a scheduled cadence, validates the APK exists, and generates SHA-256 checksums. No GitHub Gold runtime test was performed. |
| Reusability | 5/5 | Exposes device capabilities to ordinary Termux shell/program workflows; companion client package separates CLI argument processing from Android-side implementation. |
| Novelty | 4/5 | The Unix-socket + Android broadcast bridge is a useful architecture for exposing mobile platform APIs to command-line tooling. |
| Documentation | 4/5 | README documents installation, signing constraint, IPC design, client-package relationship, and licensing; implementation is organized into API-specific classes. |
| Maintenance | 5/5 | Repository is not archived and received multiple corrective commits on 2026-09-06, including MicRecorder and Dialog fixes. |

**Total: 27/30 — provisional S tier.**

## What it does

Termux:API is the Android application side of the Termux API bridge. Upstream describes it as an app that exposes Android APIs to command-line usage, scripts, and programs. It is paired with the separate `termux-api-package`, which provides the client binary and command wrappers.

The documented IPC design is particularly reusable as an architectural reference: the `termux-api` client creates two Linux anonymous-namespace sockets, passes their addresses to the Android `TermuxApiReceiver` using an Android broadcast, forwards stdin through one socket, and returns API output through the other.

## Valuable components / surfaces

The Android-side source tree contains dedicated API implementations for device capabilities. Examples observed directly in the upstream API directory include:

- audio;
- battery status;
- brightness;
- call log;
- camera information and camera photo capture;
- clipboard;
- contacts;
- dialogs;
- downloads;
- fingerprint interaction;
- infrared;
- Android job scheduling.

This is more useful than treating the repository as one monolithic app: the individual API classes are good research leads for understanding Android permission boundaries and for designing user-controlled phone automation.

## Installation / runtime requirements

Upstream lists the current release as `v0.53.0` and points users to F-Droid. It also provides per-commit debug builds through GitHub Actions.

A critical compatibility constraint is signing: upstream states that Termux:API must be signed with the same key as the main Termux app for its permissions to work. Switching installation sources can therefore require uninstalling the main Termux application and installed plugins first. This is operationally important and should not be hidden in a generic installation note.

## Working evidence inspected

The upstream build workflow currently triggers on pushes and pull requests to `master`, on a scheduled cadence, and manually. It:

1. checks out the repository;
2. derives a semantic build version;
3. runs `./gradlew assembleDebug`;
4. verifies that the expected APK exists;
5. generates a SHA-256 checksum file;
6. uploads the APK, checksum, and output metadata as workflow artifacts.

This supports the narrower claim that upstream continuously checks whether a debug APK can be assembled and packaged. It does **not** establish that every API works correctly across Android versions/devices.

## Maintenance evidence

Recent commits inspected include three fixes dated 2026-09-06:

- MicRecorderAPI no longer appends null/empty message or error text;
- MicRecorderAPI catches broader failures when starting MediaRecorder rather than only two exception classes;
- DialogAPI avoids attempting to return a result twice after orientation changes.

These are concrete maintenance signals around real Android lifecycle/media edge cases rather than cosmetic repository churn.

## License / copying policy

The upstream README states GPLv3. GitHub Gold copied no Termux:API source, APKs, binaries, or assets. If source is ever adapted rather than merely cataloged, GPL obligations and file-level notices must be reviewed first.

## Verification boundary

GitHub Gold inspected repository documentation, source-tree structure, build workflow, and recent commit metadata. GitHub Gold did **not**:

- build or install the APK;
- install the companion `termux-api-package`;
- execute API commands on Android;
- test Android-version compatibility;
- test permission behavior;
- validate F-Droid artifacts or signatures;
- independently reproduce the September 2026 fixes.

Accordingly, **VERIFIED** here means strong repository-native evidence that this is a maintained, build-checked, technically substantive project, not independent runtime validation by GitHub Gold.

## Caveats / risks

- API availability depends on Android version, device hardware, runtime permissions, and OEM behavior.
- Signing-key compatibility between Termux and plugins is a hard deployment constraint.
- Some APIs expose sensitive device capabilities/data; scripts should follow least privilege and avoid unattended access to contacts, call logs, microphone, camera, or other private data unless intentionally configured by the device owner.
- A successful APK build does not prove every API path works on current Android releases.

## Related ecosystem

- `termux/termux-api-package` — client binary and shell-facing command wrappers; strongest immediate follow-up.
- `termux/termux-app` — main Android terminal environment and signing/permission counterpart.
- `termux/termux-packages` — package ecosystem used inside Termux.

## Strong follow-up leads

1. Inspect `termux/termux-api-package` and map every CLI command to its Android-side API class.
2. Build a capability matrix: command, Android permission, minimum/affected Android version, hardware dependency, input/output format, and privacy sensitivity.
3. Inspect the broadcast-receiver/socket IPC boundary for failure handling, cancellation, timeouts, and structured output behavior.
4. Review Android 13–16 behavior changes affecting notifications, background services, storage, Wi-Fi, Bluetooth, microphone/camera, and job scheduling.
5. Compare F-Droid stable release cadence against current `master` and document meaningful unreleased fixes.
6. Evaluate which APIs are especially useful for offline/emergency, accessibility, field-research, sensor-logging, and user-owned automation workflows.
