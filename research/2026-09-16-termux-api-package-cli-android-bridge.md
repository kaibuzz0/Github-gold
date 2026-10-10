# Termux API Package — shell-facing Android API client

- **Repository:** https://github.com/termux/termux-api-package
- **Author / organization:** Termux
- **Category:** Android / Termux / CLI / automation / device integration
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 25/30
- **Provisional tier:** A
- **License:** MIT
- **Discovery:** Recursive follow-up from the `termux/termux-api` dossier.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5/5 | Turns a broad set of Android device capabilities into composable shell commands. |
| Working Evidence | 4/5 | Mature released package with concrete C transport implementation and a large installed wrapper surface; no GitHub Gold runtime test was performed. |
| Reusability | 5/5 | Provides both CLI wrappers and shared/static `libtermux-api`, allowing shell use and native linkage. |
| Novelty | 4/5 | Bridges Unix shell processes to Android APIs using abstract Unix sockets, broadcasts, and optional file-descriptor passing. |
| Documentation | 3/5 | Root README is minimal; individual wrappers provide command help and the source is relatively direct. |
| Maintenance | 4/5 | Latest code-level fixes inspected are from 2025; repository is not archived and includes memory/error-handling fixes after v0.59.0. |

**Total: 25/30 — provisional A tier.**

## What it does

`termux-api-package` is the shell/client half of Termux:API. The repository's README describes it as the Termux package containing scripts that call API methods exposed by the separate `termux/termux-api` Android application.

The useful design is layered rather than just a directory of convenience scripts:

1. user-facing `termux-*` shell wrappers validate/translate CLI options;
2. the native `termux-api` implementation transports method names, arguments, stdin and results between the Termux process and the Android plugin;
3. CMake builds shared and static `libtermux-api` variants, so native programs can reuse the transport without shelling out to every wrapper;
4. the Android-side `termux/termux-api` repository implements the actual platform operations.

## Capability surface inspected

The CMake install list exposes a large command surface including:

- battery, brightness and audio information;
- camera information/photo capture;
- clipboard and contacts;
- dialogs and fingerprint interaction;
- infrared frequencies/transmit;
- job scheduling and keystore operations;
- location and sensors;
- media player, media scan and microphone recording;
- NFC;
- notifications and notification channels;
- Android Storage Access Framework create/list/read/write/stat/remove operations;
- sharing and storage selection;
- SMS inbox/list/send;
- speech-to-text and text-to-speech;
- telephony calls/cell/device information;
- torch, vibration, volume and wallpaper;
- USB;
- Wi-Fi connection/enable/scan information.

This command inventory is valuable as a ready-made Android automation vocabulary and as a map into the corresponding Android-side API implementations.

## Native transport / reusable components

`termux-api.c` is the most technically interesting component. Current source identifies package version `0.59.1` and implements communication with the plugin using Unix-domain sockets, with `am broadcast` as a fallback path.

A notable Android-version compatibility decision is explicit in the source: on Android API level 34+ the client avoids its normal plugin listen-socket fast path because Android may freeze the plugin process while leaving the socket connectable, which can make a read hang. It instead uses the broadcast path, which can cause Android to unfreeze the receiving process.

The listen-socket path also checks `SO_PEERCRED` and requires the peer UID to equal the caller UID before treating the socket as the plugin endpoint.

Other reusable transport details include:

- generated abstract Unix socket addresses for per-call input/output;
- a background thread forwarding stdin into the output socket;
- `recvmsg()` for API output;
- `SCM_RIGHTS` file-descriptor receipt, used by USB-related workflows;
- a callback execution path that can export a received USB descriptor through `TERMUX_USB_FD`;
- explicit SIGPIPE and child-process handling;
- a fallback `execv()` of Termux's `am broadcast` wrapper.

These are useful implementation references for local IPC and Android/Unix interoperability, independent of any one API wrapper.

## Build / packaging evidence

CMake builds:

- shared `libtermux-api.so`;
- static `libtermux-api.a`;
- `termux-api-broadcast`;
- the installed command wrappers;
- the callback helper.

The repository has tagged releases. The latest GitHub release inspected is `v0.59.0`, published 2025-03-16. Current source reports `0.59.1`, matching a later version-bump commit.

Recent maintenance inspected includes March 2025 corrections for failed `malloc()`, freeing the allocated child argv array on `execv()` failure, avoiding excess/uninitialized allocation, making a header include more portable outside Termux, and synchronizing USB error handling with changes in the Android-side API repository. A `SECURITY.md` file was added in June 2025.

## License / copying policy

The root LICENSE is MIT, copyright Termux 2017–2021. GitHub Gold copied no upstream C source, scripts, binaries, or package artifacts. If any implementation is later adapted, retain the MIT copyright and permission notice and re-check file-level notices first.

## Verification boundary

GitHub Gold inspected the upstream README, root tree, command/script inventory, CMake configuration, native transport source, license, release metadata and recent commits. GitHub Gold did **not**:

- compile or install the package;
- link against `libtermux-api`;
- execute any `termux-*` command;
- test Android 14+ broadcast fallback behavior;
- validate peer-credential behavior;
- test USB file-descriptor passing;
- test wrapper/API compatibility across Android versions;
- independently reproduce the 2025 memory/error-handling fixes.

Accordingly, VERIFIED means there is strong repository-native evidence of a substantive released implementation, not independent runtime validation by GitHub Gold.

## Caveats / risks

- The package depends on the separate Termux:API Android application for actual Android API execution.
- Effective capabilities vary with Android permissions, Android version, device hardware and OEM behavior.
- The shell-facing package and Android-side app evolve separately, so version/interface compatibility matters.
- Many commands expose private or sensitive device data/capabilities; automation should use least privilege and be intentionally configured by the device owner.
- Root documentation is sparse compared with the size of the command surface.
- Latest inspected repository activity is 2025 rather than 2026, so Maintenance is scored below the Android-side Termux:API repository.

## Related ecosystem

- `termux/termux-api` — Android-side API implementation and permission boundary.
- `termux/termux-app` — main terminal environment and application-signing counterpart.
- `termux/termux-packages` — distribution/package recipes for the Termux environment.

## Strong follow-up leads

1. Build an exact wrapper → `api_method` → Android implementation-class map.
2. Build a capability/permission matrix for Android 13–16, including hardware dependencies and privacy sensitivity.
3. Inspect `libtermux-api` as a reusable native embedding surface rather than only the command wrappers.
4. Audit socket lifecycle/timeouts and Android process-freezing behavior for failure modes beyond the documented API-34 workaround.
5. Map `SCM_RIGHTS`/USB descriptor handling end-to-end into the Android-side USB implementation.
6. Compare package version compatibility against Termux:API stable and current master.
7. Identify high-value offline/emergency/accessibility/field-automation compositions using only local device APIs.