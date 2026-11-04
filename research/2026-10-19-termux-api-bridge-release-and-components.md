# Termux:API stack — October 19, 2026 evidence and maintenance refresh

**Scope:** `termux/termux-api` (Android companion) and `termux/termux-api-package` (native CLI). GitHub-first research; no usable YouTube transcripts in this pass. **No source code copied.**

## Verdict

| Project | Evidence | Provisional score | License |
| --- | --- | --- | --- |
| [Termux:API Android app](https://github.com/termux/termux-api) | VERIFIED from upstream implementation, workflow and maintenance history; not independently executed | **S / 27** (Utility 5, Working Evidence 4, Reusability 5, Novelty 4, Documentation 4, Maintenance 5) | GPLv3 stated in README; inspect per-file notices |
| [Termux API CLI package](https://github.com/termux/termux-api-package) | VERIFIED from upstream C source, tagged release and downstream package recipe; not independently executed | **A / 23** (Utility 5, Working Evidence 3, Reusability 5, Novelty 4, Documentation 2, Maintenance 4) | MIT root LICENSE; Android companion is separate GPLv3 project |

## Important maintenance correction

The [native CLI v0.60.0 release](https://github.com/termux/termux-api-package/releases/tag/v0.60.0) was published **2026-09-16 22:16 UTC**, replacing the v0.59.1 snapshot in [the earlier dossier](2026-09-08-termux-api-package-shell-android-bridge-runtime.md). The [release commit](https://github.com/termux/termux-api-package/commit/9e7f1531e1aa4a9c1e261a2dbde4de93653c366e) and [downstream Termux package recipe](https://github.com/termux/termux-packages/blob/master/packages/termux-api/build.sh) agree on v0.60.0. The recipe pins source SHA-256 `b2329008248233a7c2d69aa6158ccc4134f9dd83f6c5b1b311c717e997113bcf`, with runtime dependencies `bash`, `util-linux`, and `termux-am >= 0.8.0`. The [preceding native commit](https://github.com/termux/termux-api-package/commit/73a586d3460af7f551ec7229304fb1b32aa05c6c) sends PID, UID and process start time to the app for caller/process-lifecycle validation. **Maintenance score corrected from 3 to 4; total from 22 to 23.** This is not an independent runtime verification.

The [Android companion README](https://github.com/termux/termux-api/blob/master/README.md) still identifies v0.53.0 as the latest stable app release. [September 16](https://github.com/termux/termux-api/commit/ee29d4314ca4e93dc6df1522469764dd651f06f1) updated Android 11+ background-location permission instructions; [September 17](https://github.com/termux/termux-api/commit/fc26ce17e3badf85d4df191af364fcf7798047f1) added explicit handling of duplicate ResultReturner completion calls.

## Exact reusable implementation targets

**Android side:**
- [`TermuxApiReceiver.java`](https://github.com/termux/termux-api/blob/master/app/src/main/java/com/termux/api/TermuxApiReceiver.java): method dispatch, permission gating, receiver exception containment and lifecycle.
- [`ResultReturner.java`](https://github.com/termux/termux-api/blob/master/app/src/main/java/com/termux/api/util/ResultReturner.java): result transport and completion.
- [`LocationAPI.java`](https://github.com/termux/termux-api/blob/master/app/src/main/java/com/termux/api/apis/LocationAPI.java), [`SensorAPI.java`](https://github.com/termux/termux-api/blob/master/app/src/main/java/com/termux/api/apis/SensorAPI.java), [`UsbAPI.java`](https://github.com/termux/termux-api/blob/master/app/src/main/java/com/termux/api/apis/UsbAPI.java): focused device API adapters.
- [APK build workflow](https://github.com/termux/termux-api/blob/master/.github/workflows/github_action_build.yml): upstream `assembleDebug`, APK artifact existence and SHA-256 checks. Build configuration is not proof of Android device functionality.

**Native CLI side:**
- [`termux-api.c`](https://github.com/termux/termux-api-package/blob/v0.60.0/termux-api.c): abstract Unix sockets, stdin/stdout forwarding, `SO_PEERCRED` peer-UID check, `SCM_RIGHTS` descriptor passing, PID/UID/starttime metadata, Android 14+ broadcast fallback.
- [`termux-api.h`](https://github.com/termux/termux-api-package/blob/v0.60.0/termux-api.h), [`CMakeLists.txt`](https://github.com/termux/termux-api-package/blob/v0.60.0/CMakeLists.txt), [`scripts/`](https://github.com/termux/termux-api-package/tree/v0.60.0/scripts), [`termux-callback.in`](https://github.com/termux/termux-api-package/blob/v0.60.0/termux-callback.in): reusable library, CLI and USB callback integration. No repository-local automated test matrix established.

## Architecture and trust boundary

The native helper creates two anonymous-namespace Unix sockets for stdin and stdout, and invokes the companion Android receiver. On supported Android versions it can contact the plugin directly, checking peer identity with `SO_PEERCRED`. On Android 14+ it prefers a broadcast route because a frozen app may retain a connectable socket without processing requests. Android-side permission checks protect sensitive capabilities; the upstream README requires compatible signing keys for Termux and the API app. The companion requests sensitive device permissions (location, SMS, contacts, camera, microphone and others); do not treat it as a general untrusted-command execution endpoint.

## License and verification boundaries

The [CLI root LICENSE](https://github.com/termux/termux-api-package/blob/master/LICENSE) is MIT. The [Android README](https://github.com/termux/termux-api/blob/master/README.md) states GPLv3; no standalone root license file was established in the earlier inspection. These licenses must not be conflated; review dependency and per-file notices before adapting any source. No third-party code was copied. No APK/native build, installation, device test, fuzz run, network test or security audit was performed by GitHub Gold. Upstream CI/release/package evidence is not independent execution evidence.

## Ecosystem leads

- [termux/termux-boot](https://github.com/termux/termux-boot): boot-time automation; **LEAD** pending implementation/test review.
- [termux/termux-widget](https://github.com/termux/termux-widget): launcher/widget script execution; **LEAD** pending implementation/test review.
- [termux/termux-app](https://github.com/termux/termux-app) and [termux/termux-packages](https://github.com/termux/termux-packages): distribution/signing and package integration.
- Future checks: v0.60.0 Android 14+ process freeze/recovery behavior, native IPC bounds/fuzz tests, caller-identity enforcement, source-vs-package reproducibility, signing-key migration.
