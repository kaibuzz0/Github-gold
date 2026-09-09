# termux/termux-api-package — shell-side Android capability bridge runtime

- **Repository:** https://github.com/termux/termux-api-package
- **Author / organization:** Termux
- **Category:** Android / Termux / CLI interoperability / local IPC / automation bridge
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **22/30 — A tier**
- **License:** **MIT**
- **Discovery source:** recursive follow-up from `termux/termux-api`; GitHub-first, with no YouTube-derived technical claim used in this pass

## Executive finding

`termux/termux-api-package` is the shell-side half of Termux:API. It is not just a directory of wrapper scripts: it contains a small C runtime that creates Linux abstract-namespace Unix sockets, moves stdin/stdout between shell commands and the Android Termux:API process, invokes the Android receiver, supports file-descriptor passing with `SCM_RIGHTS`, and falls back to `am broadcast` when the direct plugin socket path is unavailable or undesirable.

Its strongest GitHub Gold value is the compact **Unix CLI ↔ Android app IPC bridge**. It shows how a normal shell process can preserve stdin/stdout semantics while delegating privileged Android API work to an app component.

## Provisional 30-point Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Supplies the command-line transport and wrappers that make Termux:API usable from ordinary shell scripts. |
| Working Evidence | 3/5 | Formal releases exist and the current Termux package repository still pins and checksums v0.59.1 source. No repository-local CI/test workflow was observed in this inspection. |
| Reusability | 5/5 | The socket bridge, stdin/stdout transport, fallback invocation and FD-passing patterns are compact and broadly instructive. |
| Novelty | 4/5 | Unix-domain IPC is standard, but adapting it into a shell-friendly Android capability bridge is unusually practical. |
| Documentation | 2/5 | Root README is minimal; most architecture knowledge must be recovered from C source, scripts, release notes and companion repositories. |
| Maintenance | 3/5 | Upstream's newest inspected commit is 2025-06-25, but the package remains an active dependency in `termux/termux-packages` in 2026 and is currently pinned at 0.59.1 with a source checksum. |
| **Total** | **22/30** | **Provisional A** |

## What the repository provides

### Native bridge library and executable

CMake builds the same `termux-api.c` implementation as both shared and static libraries and links a `termux-api-broadcast` executable against the static form. It also installs the public header, compatibility symlink and the shell command wrappers.

This makes the bridge usable both as an executable transport and as a small native library that other programs can link against.

### Broad command wrapper surface

The build installs wrappers for battery, camera, clipboard, contacts, dialogs, fingerprint, infrared, job scheduling, keystore, location, media, microphone, NFC, notifications, Android Storage Access Framework operations, sensors, SMS, speech, telephony, USB, vibration, volume, wallpaper and Wi-Fi operations.

The Android implementation for these capabilities lives in `termux/termux-api`; this repository supplies the shell-facing argument layer and transport.

### Abstract Unix socket transport

`run_api_command()` creates two Linux abstract-namespace `AF_UNIX` sockets with randomized names. One path transports shell stdin toward the Android implementation while the other returns the Android result to shell stdout.

A child process contacts the plugin while the parent accepts the socket connection, starts a thread that copies stdin into the outgoing socket, and reads results from the incoming socket.

### Direct plugin connection with peer-UID check

`contact_plugin()` first attempts to connect to the Termux:API app's known abstract listen socket on Android versions below API 34. It checks `SO_PEERCRED` and requires the peer UID to match the caller UID before sending the command payload.

This is an important trust boundary: a successfully connectable socket alone is not accepted as proof that the expected plugin owns it.

### Android 14 fallback behavior

The source explicitly avoids the direct plugin-socket route on Android API 34+ because Android may freeze a previously started app process while leaving its socket connectable, which could cause the shell-side read to hang. In that case the helper uses `am broadcast`, which can cause Android to deliver the intent and unfreeze the target process.

This is a useful example of IPC design adapting to Android background-process policy rather than assuming desktop-Linux process semantics.

### `am broadcast` fallback

If the direct socket route fails or is not used, the helper execs Termux's `am` command and targets `com.termux.api/.TermuxApiReceiver`, passing the input socket, output socket and API method as extras.

The input/output socket names are intentionally reversed from the Java process perspective: the shell helper's output is the Android process's input and vice versa.

### File-descriptor transport

The result reader uses `recvmsg()` ancillary data and recognizes `SCM_RIGHTS` to receive a file descriptor from the Android side. The USB path can either expose the descriptor through `TERMUX_USB_FD` or pass it into `termux-callback`.

That makes the project more than a JSON/text IPC shim: it can bridge Android-opened resources into native/shell workflows.

## Working and maintenance evidence

The repository does not expose a `.github/workflows` directory in the inspected default branch, so GitHub Gold does **not** claim repository-local automated build/test evidence.

Evidence that the component remains operationally integrated comes from the current `termux/termux-packages` tree: its `packages/termux-api/build.sh` pins **version 0.59.1**, downloads the tagged source archive from this repository, verifies it using an explicit SHA-256 value, and declares runtime dependencies including Bash, util-linux and `termux-am`.

The latest formal GitHub release observed is **v0.59.0, published 2025-03-16**. The repository was bumped to **0.59.1 on 2025-03-29** after memory-handling fixes. The newest inspected upstream commit is **2025-06-25**, adding `SECURITY.md`.

The lack of recent direct commits keeps Maintenance below the stronger Termux entries even though the package is still consumed by the current package repository.

## Notable implementation hardening

Recent 0.59.1-era fixes included:

- checking `malloc()` failure when constructing the `am` child argument array;
- allocating only the number of bytes actually needed for that array;
- freeing the array on `execv()` failure;
- replacing a Termux-specific endian include with `arpa/inet.h` for easier compilation on other systems.

These are upstream maintenance changes, not independently reproduced fixes.

## High-value reusable components and patterns

### `termux-api.c`

The core transport implementation. High-value areas include:

- abstract Unix socket creation;
- plugin listen-socket discovery;
- `SO_PEERCRED` identity verification;
- compact command serialization;
- stdin→socket worker thread;
- socket→stdout result forwarding;
- `SCM_RIGHTS` descriptor reception;
- Android-version-specific fallback policy;
- `am broadcast` execution.

### `libtermux-api.so` / static library

The build exposes the bridge as both shared and static libraries, making the IPC mechanism reusable from native programs rather than only through shell wrappers.

### Shell wrapper corpus

The `scripts/` directory provides a large collection of narrowly focused CLI interfaces. These are useful for argument-interface design and for understanding how Android API semantics are mapped into Unix command conventions.

The newer `termux-sms-list` work is particularly interesting because upstream moved toward Bash arrays and consistent argument-processing/logging helpers to avoid unsafe/non-deterministic unquoted parameter expansion.

### `termux-callback`

The callback mechanism is a focused follow-up target for descriptor/resource workflows, especially USB.

## Licensing boundary

The repository root contains an **MIT License** covering the project source. Any reuse must retain its copyright and permission notice.

The Android-side companion `termux/termux-api` is separately licensed, so this MIT label must not be generalized to the full end-to-end Termux:API stack.

No upstream source, binaries or scripts were copied into GitHub Gold.

## Security and operational caveats

- The bridge transports shell-controlled arguments across native serialization, Android intent/broadcast and Java/Kotlin handling boundaries.
- The direct listen-socket protocol creates its command payload manually; malformed or unexpectedly large arguments deserve dedicated fuzzing and bounds review.
- Peer UID checking reduces socket impersonation risk but is only one part of the complete Termux/Termux:API signing and shared-identity trust model.
- Android 14 process-freezing behavior already forced an IPC-policy change; future Android background-execution changes can alter reliability again.
- `SCM_RIGHTS` descriptor passing is powerful and should be treated as a privileged resource boundary.
- Wrapper scripts may differ in age and argument-safety conventions; the project itself notes a newer consistent Bash wrapper format being introduced incrementally.
- Repository-local CI/tests were not observed, so package integration and releases are weaker evidence than a current automated correctness matrix.
- The latest direct upstream commit observed is from 2025, despite continued downstream packaging in 2026.

## Verification performed in this pass

Performed:

- checked the live GitHub Gold PR/branch and searched for an existing entry;
- inspected upstream root structure, CMake build definition and MIT license;
- inspected the main C transport implementation, including socket creation, direct-plugin path, UID verification, Android 14 fallback, stdin/stdout transport and descriptor handling;
- inspected recent upstream commits and release history;
- checked for repository-local GitHub Actions workflows and found none under the inspected `.github` tree;
- verified current downstream integration in `termux/termux-packages`, including version 0.59.1 and an explicit SHA-256 source checksum.

Not performed:

- cloning or compiling the repository locally;
- linking against `libtermux-api`;
- installing/running the package in Termux;
- exercising a real Termux:API Android app;
- testing Android 14+ freeze/unfreeze behavior;
- testing USB descriptor passing;
- fuzzing command serialization, socket lifecycle or wrappers;
- reproducing the 0.59.1 memory fixes;
- independently hashing the source archive;
- auditing every shell wrapper.

## Strong recursive research leads

1. **End-to-end protocol trace** — wrapper → `termux-api.c` → Android receiver → `ResultReturner` → stdout.
2. **`ResultReturner`** — exact framing, encoding, error and socket lifecycle on the Android side.
3. **Serialization fuzzing** — quotes, very large values, malformed extras and partial socket I/O.
4. **FD passing** — USB `SCM_RIGHTS` lifecycle, ownership and cleanup semantics.
5. **Android 14+ behavior** — process freeze/background restrictions and broadcast fallback reliability.
6. **Wrapper modernization** — identify scripts still using legacy argument handling versus the safer Bash-array pattern.
7. **Native library API** — assess how cleanly third-party native Termux programs can embed `libtermux-api`.
8. **Termux:Boot / Termux:Widget** — rotate into adjacent user-controlled automation components after completing the IPC trace.

## Verdict

**VERIFIED / provisional A / 22.**

`termux/termux-api-package` qualifies as GitHub Gold because its small C runtime contains a genuinely reusable Android/Unix interoperability pattern: preserve familiar CLI stdin/stdout behavior while delegating capability access to an Android app over local authenticated IPC, with native descriptor passing and Android-policy-aware fallback behavior. Its score is intentionally below the strongest Termux candidates because documentation is sparse, repository-local CI/testing was not observed, and direct upstream maintenance has slowed even though the component remains integrated into the current Termux package ecosystem.