# GitHub Gold research: libusb and Tippecanoe

Date: 2026-10-31 UTC (2026-10-30 America/Chicago). Method: GitHub-first primary-source review. No upstream code copied; no independent builds, device transfers or tile conversions.

## 1. libusb — VERIFIED / S28

Repository: https://github.com/libusb/libusb. Stable v1.0.30 published 2026-05-17; current master commit 987c117 dated 2026-10-30.

Source evidence: README.md; COPYING (LGPL-2.1-or-later); libusb/libusb.h (SPDX); libusb/core.c, descriptor.c, io.c, hotplug.c, sync.c; libusb/os/{linux_usbfs.c,windows_winusb.c,darwin_usb.c,emscripten_webusb.cpp}; android/README; tests/umockdev.c and tests/fuzz/.

Observed upstream CI: 2026-10-30 master Linux https://github.com/libusb/libusb/actions/runs/40983130249 succeeded (GCC 16/C23 compile, Linux release/configuration builds, Emscripten compile and umockdev test). Optional sanitizer rebuild and BOS descriptor fuzzer steps were **skipped**. Android https://github.com/libusb/libusb/actions/runs/40983130732 succeeded with NDK build artifacts for armeabi-v7a, arm64-v8a and x86_64; no physical USB execution. Other same-commit workflows succeeded for macOS, Windows, MSYS2, Cygwin, BSD, Haiku and illumos.

Why useful: portable C USB transport, asynchronous events, hotplug and OS abstraction; Android's UsbManager permission -> UsbDeviceConnection FD -> libusb_wrap_sys_device pattern is especially valuable for authorized device interoperability. It is a *related pattern*, not a proven dependency of nohajc/termux-adb. Runtime permissions, driver access, untrusted descriptors and transfer timeouts remain untested here.

License: LGPL-2.1-or-later, not a blanket permissive license. Respect library modifications, attribution and applicable relinking obligations; review examples and dependencies separately. No source copied.

Score: utility 5, working evidence 5, reusability 5, novelty 4, documentation 4, maintenance 5 = 28. Next: test permitted USB device access on Linux and Android, compare FD handoff with termux-adb, validate hotplug races and error handling, inspect fuzz/sanitizer results on a successful executed run.

## 2. Tippecanoe — VERIFIED / S27

Repository: https://github.com/felt/tippecanoe. README identifies Erica Fischer/Felt as maintainers, traces lineage to mapbox/tippecanoe; main uses C++17. Published stable GitHub release 2.79.0 (2025-07-24), while main CHANGELOG starts at 2.82.0. Do **not** describe 2.82.0 as a published stable release.

Source evidence: README.md, LICENSE.md, Makefile, CHANGELOG.md, main.cpp, tile.cpp, geometry.cpp, geojson.cpp, flatgeobuf.cpp, mbtiles.cpp, pmtiles_file.cpp, pmtiles/pmtiles.hpp, mvt.cpp, tile-join.cpp, jsontool.cpp, jsonpull/ and tests/. README explicitly accepts GeoJSON, FlatGeobuf and CSV and documents .mbtiles/.pmtiles output and --temporary-directory.

Observed upstream CI: https://github.com/felt/tippecanoe/actions/runs/31769908097 on 2026-08-14 main passed **7/7 jobs**: Ubuntu x86_64 and ARM64 plus macOS, each Release and Debug `make` + `make test`, and documentation regeneration. This is upstream evidence, not independently executed tests. Last inspected main commit 4f262118 (2026-08-14) includes JSON parser ownership changes. CHANGELOG 2.82.0 documents a JSON array deletion double-free/corruption fix, malformed Unicode fixes, numeric field crashes and null-properties uninitialized read. Release 2.79.0 predates those main changes; no stable backport established.

Why useful: direct **FlatGeobuf input -> PMTiles output** bridge; also MBTiles, MVT encoding, filtering, simplification, tile-join, JSON utilities. Relates to existing FlatGeobuf, PMTiles and MapLibre Native catalog records. Requires SQLite3/zlib/pthreads and enough temporary storage for large datasets.

License: two-condition BSD-style text in LICENSE.md, Mapbox and Protomaps copyrights; bundled clipper2, FlatBuffers, protozero and PMTiles code need component-level notice/license review. Geographic data may have separate licensing. No source or data copied.

Score: utility 5, working evidence 5, reusability 5, novelty 4, documentation 5, maintenance 3 = 27. Next: run small reproducible FlatGeobuf -> PMTiles -> MapLibre rendering test, compare stable vs main JSON handling on benign malformed fixtures, bound disk/RAM usage, inspect vendored license notices and confirm whether fixed stable release is published.

## Maintenance cross-links

PMTiles and FlatGeobuf existing records now reference Tippecanoe's verified input/output source paths. This is source-level integration evidence, **not** a claim that an end-to-end map conversion or rendering was independently executed.

## YouTube seeds

Exact-ID searches on 2026-10-31 UTC for `PLMI6SBmd587c` and `PLfidXW0BixTc` yielded no indexed playlist/transcript material. No playlist video was viewed and neither discovery is attributed to YouTube. Four other seeds were not retried this pass.

## Next research

Follow libusb's Android permission/FD ecosystem and Tippecanoe's PMTiles/FlatGeobuf/MapLibre integration. Inspect new stable releases, security fixes and full test outcomes before changing scores.
