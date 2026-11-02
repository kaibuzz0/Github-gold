# Research dossier — USB Devices and PgSTAC (2026-11-02)

## Research method and provenance
GitHub-first recursive follow-up of the previously cataloged Bluetooth Adapters and STAC-GeoParquet. Reviewed GitHub-native source, release tags, manifests, licenses, CI workflows and completed job results. Two playlist identifier searches (`PLMI6SBmd587c`, `PLfidXW0BixTc`) returned no indexed transcript evidence; **no findings are attributed to YouTube**. No third-party implementation code was copied.

## USB Devices — VERIFIED upstream, A24 (4/5/4/3/4/4)
- Repository: https://github.com/Bluetooth-Devices/usb-devices — Bluetooth-Devices / J. Nick Koston.
- License: [MIT](https://github.com/Bluetooth-Devices/usb-devices/blob/main/LICENSE), copyright 2022 J. Nick Koston. Preserve notice for reuse; no code copied.
- Stable [v0.5.1](https://github.com/Bluetooth-Devices/usb-devices/releases/tag/v0.5.1) published **2026-05-27**; main maintenance commits **2026-06-22**.
- Inspected `src/usb_devices/__init__.py`: `BluetoothDevice` maps `/sys/class/bluetooth/hciN/device` symlinks to `USBDevice`, which reads `/sys/bus/usb/devices` metadata and forms `/dev/bus/usb` paths. `reset()` uses Linux `USBDEVFS_RESET` ioctl; `async_reset()` wraps it in an executor. `examples/info.py` enumerates hci devices.
- Manifest: Python `^3.10`; no required third-party runtime Python dependency in inspected Poetry manifest; Linux hardware interfaces required for meaningful operation.
- [2026-10-26 PR CI](https://github.com/Bluetooth-Devices/usb-devices/actions/runs/40377578152): 15/15 Python 3.10–3.14 tests across Ubuntu/macOS/Windows passed; lint, PR title and release dry run passed; real release job skipped. **These are upstream test results**, not physical USB tests. Cross-platform mock tests do not establish non-Linux sysfs/ioctl functionality.
- Caveat: reset may disconnect devices and interrupt running services; avoid without explicit ownership/authorization and appropriate OS permissions. No independent install, device read, reset or security test.
- Ecosystem: Bluetooth-Devices/bluetooth-adapters uses the helper for Linux adapter metadata. Sibling `uart-devices` merits separate source/CI inspection; PyUSB is a distinct general USB transfer library.
- Next: create fake sysfs fixtures for `USBDevice.setup`, test malformed symlinks and absent descriptors, evaluate privilege requirements without executing destructive reset.

## PgSTAC — VERIFIED upstream, S27 (5/5/5/4/4/4)
- Repository: https://github.com/stac-utils/pgstac — stac-utils contributors.
- License: [MIT](https://github.com/stac-utils/pgstac/blob/main/LICENSE) (Microsoft Corporation and other contributors). Review component/dependency licenses separately; no code copied.
- [v0.10.0 release](https://github.com/stac-utils/pgstac/releases/tag/v0.10.0) published **2026-10-01**. **Important version split:** `v0.10.0` tag tree has `src/pgstac/` SQL and `src/pypgstac/` Python tooling. The inspected **main branch** instead exposes `src/pgstac-rs/` Rust CLI/ingest/export and `src/pgstac-migrate/` (manifest version `0.9.11-dev`). Do not advertise main-development Rust components as stable v0.10.0 functionality.
- Tag changelog: v0.10.0 is a breaking release. Database and pypgstac 0.10.x must be upgraded together; queryables migration can halt on invalid wrappers/indexes; old pagination tokens are invalid after upgrade. Read upstream migration instructions and back up production catalogs.
- Inspected `src/pgstac/sql/001_core.sql` (settings, migration/version and SQL helpers), `src/pgstac-rs/src/bin/pgstac.rs` (main-development CLI for load/search/dump/restore), `src/pgstac-rs/src/load/pool_ingest.rs` (main-development dehydrate and binary COPY path), `src/pgstac-rs/Cargo.toml` (Rust >=1.88; optional features; explicit development-only rustac git patch), `src/pgstac-migrate/pyproject.toml` (Python >=3.11), README and CI.
- [2026-11-01 scheduled main CI](https://github.com/stac-utils/pgstac/actions/runs/41301500534): 12/12 jobs successful; six PostgreSQL 16/17/18 matrix tests (including lowest-direct dependency resolution), Rust compile/docs, and container builds. This tests the **main branch**, not necessarily the v0.10.0 tag. No independent SQL, migration, performance, security or data-integrity test.
- Ecosystem: optional pgstac reader in STAC-GeoParquet; STAC FastAPI provides an HTTP-facing backend (PgSTAC alone is not an HTTP server); PySTAC models and PostGIS spatial operations.
- Next: compare tag/main migration graph and supported database versions; stage a disposable Postgres/PostGIS migration test with rollback/backup; test CQL2 filters, keyset pagination and heterogeneous STAC extension metadata; audit security-definer SQL functions and roles before production use.

## Verification boundary
Evidence classification `VERIFIED` means upstream code and test/CI evidence was inspected; it does **not** mean GitHub Gold independently installed, tested, benchmarked, deployed, reset devices, or performed security analysis. Scores use utility, working evidence, reusability, novelty, documentation, maintenance (each 0–5). 
