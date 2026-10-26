# OpenWrt and MAVSDK — GitHub-first research (2026-10-26)

## Evidence and provenance
Reviewed upstream repositories, README files, licensing, source trees, releases, CI jobs and maintenance. Evidence level VERIFIED means *upstream working evidence*, not an independent build or test. No third-party implementation code copied. Two direct YouTube playlist requests (PLMI6SBmd587c, PLfidXW0BixTc) were throttled; no transcripts read or attributed. Remaining four playlists were not checked this batch.

## OpenWrt — VERIFIED / S 28
**Repository:** https://github.com/openwrt/openwrt

**Gold factors:** Utility 5, Working 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.

**Specific source:** [scripts/feeds](https://github.com/openwrt/openwrt/blob/main/scripts/feeds), [netifd package](https://github.com/openwrt/openwrt/tree/main/package/network/config/netifd), [firewall4 package](https://github.com/openwrt/openwrt/tree/main/package/network/config/firewall4), [base-files](https://github.com/openwrt/openwrt/tree/main/package/base-files/files/etc), [image builder](https://github.com/openwrt/openwrt/blob/main/target/imagebuilder/Makefile), [image assembly](https://github.com/openwrt/openwrt/blob/main/scripts/gen_image_generic.sh), [APK package](https://github.com/openwrt/openwrt/blob/main/package/system/apk/Makefile).

**Build/install:** Build on case-sensitive GNU/Linux/BSD/macOS with appropriate compiler dependencies. Official README documents `./scripts/feeds update -a`, `./scripts/feeds install -a`, `make menuconfig`, `make`. Match device and board revision before flashing.

**Maintenance:** [v25.12.6](https://github.com/openwrt/openwrt/releases/tag/v25.12.6) published 2026-10-18; active commits 2026-10-26. 2026-10-25 upstream [kernel 40231519176](https://github.com/openwrt/openwrt/actions/runs/40231519176) passed 29/29 jobs, [core packages 40231388127](https://github.com/openwrt/openwrt/actions/runs/40231388127) passed 10/10; [toolchains 40231388106](https://github.com/openwrt/openwrt/actions/runs/40231388106) succeeded (130-job matrix, first page inspected).

**Licensing:** Root COPYING GPL-2.0-only; inspect all package, driver, kernel and feed licensing individually.

**Notable caveat:** README describes opkg, while current source includes APK and conditional APK/OPKG image-builder logic. Do not assume one package manager applies to every release or board.

**Ecosystem:** [LuCI](https://github.com/openwrt/luci), [packages](https://github.com/openwrt/packages), [routing](https://github.com/openwrt/routing), [shared workflows](https://github.com/openwrt/actions-shared-workflows). Not separately promoted.

**Next:** Reproducible images, sysupgrade recovery, firewall4/nftables testing, firmware signing and device support. No independent build, flash, network test or audit.

## MAVSDK — VERIFIED / S 27
**Repository:** https://github.com/mavlink/MAVSDK

**Gold factors:** Utility 5, Working 5, Reusability 5, Novelty 4, Documentation 4, Maintenance 4.

**Specific source:** [core](https://github.com/mavlink/MAVSDK/tree/main/cpp/src/mavsdk/core), [plugins](https://github.com/mavlink/MAVSDK/tree/main/cpp/src/mavsdk/plugins), [examples](https://github.com/mavlink/MAVSDK/tree/main/cpp/examples), [Python direct wrapper](https://github.com/mavlink/MAVSDK/tree/main/py/mavsdk), [optional gRPC server](https://github.com/mavlink/MAVSDK/tree/main/cpp/src/mavsdk_server).

**Build/install:** CMake/C++ library; C, Python and Kotlin direct bindings (Android/JNI included). Optional separate gRPC server for legacy clients; real vehicle or SITL necessary for functional integration.

**Maintenance:** [v4.0.6](https://github.com/mavlink/MAVSDK/releases/tag/v4.0.6) published 2026-10-08; active 2026-10-26 fuzz parser fixes. Upstream 2026-10-26 [Linux 40313071240](https://github.com/mavlink/MAVSDK/actions/runs/40313071240) 30 passing jobs; [Windows 40313071239](https://github.com/mavlink/MAVSDK/actions/runs/40313071239) 14/14; [Kotlin 40313071246](https://github.com/mavlink/MAVSDK/actions/runs/40313071246) 9 passing and one skipped; [Fuzzing 40313071314](https://github.com/mavlink/MAVSDK/actions/runs/40313071314) passed. [macOS 40313071347](https://github.com/mavlink/MAVSDK/actions/runs/40313071347) failed overall: x64 artifact upload step failed; six jobs passed and one skipped. Packaging failure does not prove compilation or runtime failure.

**Critical security caveat:** [SECURITY.md](https://github.com/mavlink/MAVSDK/blob/main/SECURITY.md) states MAVLink signing is not implemented. The optional gRPC `mavsdk_server` is unauthenticated, unencrypted and binds `0.0.0.0` by default. Anyone reaching it can control attached vehicles. Prefer direct v4 bindings, restrict network access and use secure transport. The upstream Python README says the new asyncio wrapper is less tested than the older gRPC client.

**Licensing:** BSD-3-Clause core; `proto/` submodule points to [MAVSDK-Proto](https://github.com/mavlink/MAVSDK-Proto); check dependencies separately.

**Ecosystem:** [MAVSDK-Proto](https://github.com/mavlink/MAVSDK-Proto), [MAVSDK-Python](https://github.com/mavlink/MAVSDK-Python), [ArduPilot](https://github.com/ArduPilot/ardupilot), [PX4](https://github.com/PX4/PX4-Autopilot). ArduPilot cross-reference added without claiming interoperability testing.

**Next:** malformed-MAVLink fuzz corpus, authentication boundaries, macOS artifact publishing, direct Python bindings and SITL interoperability. No independent SDK execution, simulator, hardware flight or security audit.

## Existing-entry maintenance
ArduPilot related-projects updated to reference MAVSDK without changing evidence/score. [Open MCT scheduled e2e](https://github.com/nasa/openmct/actions/runs/40250211098) remains failed as of 2026-10-26; previously confirmed Node 18 versus >=24.14.1 `EBADENGINE` mismatch remains unresolved. No promotion.
