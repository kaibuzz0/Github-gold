# GitHub Gold — PySTAC Client and Bleak research (2026-11-01)

## Provenance and scope
GitHub-first recursive follow-up from PySTAC and independent Bluetooth LE discovery. Exact-ID web searches for two YouTube seed playlists produced no indexed transcript material. No video-derived claims. All build/test evidence is **upstream**, not independent execution. No third-party implementation code copied.

## PySTAC Client — VERIFIED (upstream) / S27
- Upstream: https://github.com/stac-utils/pystac-client ; Apache-2.0 root license https://github.com/stac-utils/pystac-client/blob/main/LICENSE (preserve attribution; review dependencies).
- Stable v0.9.1 released **2026-10-20**: https://github.com/stac-utils/pystac-client/releases/tag/v0.9.1 . Tagged `pyproject.toml` requires Python >=3.10 and directly declares `pystac>=1.10.0`, `requests>=2.28.2`, `python-dateutil>=2.8.2`. This is a **direct** dependency on PySTAC, not vice versa.
- Reusable components: `pystac_client/client.py` (STAC catalog/API client, conformance), `item_search.py` (bbox/time/filter, CQL2, pagination), `collection_search.py`, `collection_client.py` (transaction extension), `stac_api_io.py` (HTTP session, retries, timeout, request modifiers), `conformance.py`, `cli.py`. Regression tests `tests/test_item_search.py`, `test_stac_api_io.py`, `test_collection_client.py`.
- **Upstream CI:** https://github.com/stac-utils/pystac-client/actions/runs/41075734547 — **2026-10-30 main push, 13/13 jobs passed**: Python 3.10–3.12 across Linux/macOS/Windows, docs, min versions, prerelease and upstream compatibility. Source tests use `--block-network` and HTTP cassettes/mocks; this does not prove arbitrary remote STAC services work.
- v0.9.1 changelog explicitly adds STAC Item and Collection transaction methods; server must advertise supported conformance and authorize writes. The main changelog's SQLite free-text connection cleanup is **unreleased**; do not attribute it to v0.9.1.
- Risks: remote STAC URLs and asset redirects are untrusted network inputs; API transactions can mutate remote catalogs. Apply allowlists/timeouts/auth and limit remote write privileges. No local install, HTTP call, remote transaction, schema validation or security audit performed.
- Next: deterministic mocked STAC search with pagination and CQL2; local STAC fixture interoperability with PySTAC; test read-only auth boundary and transaction error paths.

## Bleak — VERIFIED (upstream) / S28
- Upstream: https://github.com/hbldh/bleak ; root MIT license https://github.com/hbldh/bleak/blob/develop/LICENSE ; preserve copyright and license, review platform binding dependencies.
- Stable v3.0.2 released **2026-05-02**: https://github.com/hbldh/bleak/releases/tag/v3.0.2 . Tagged manifest requires Python >=3.10; Linux `dbus-fast>=1.83.0` and BlueZ >=5.55, Windows 11 >=22000 with WinRT bindings, macOS >=10.15 with PyObjC, and Android through python-for-android packaging.
- Reusable components: `bleak/backends/scanner.py`, `client.py`, `service.py`, `characteristic.py`, `descriptor.py`; backend trees `bluezdbus/`, `winrt/`, `corebluetooth/`, `p4android/`; `examples/` and `tests/integration/`.
- **Upstream CI:** https://github.com/hbldh/bleak/actions/runs/36764733562 — **2026-09-30 develop push, 27/27 jobs passed**: 15 desktop build/test jobs, five BlueZ integration jobs, five Windows integration jobs, two Android integration jobs. Inspected `.github/workflows/build_and_test.yml`: BlueZ integration uses QEMU Alpine VM/virtual HCI. These are not independently executed hardware tests and this run is newer develop, not the stable release tag.
- Develop `CHANGELOG.rst` lists **unreleased** BeeWare/Briefcase Android backend (Python >=3.13) and `dbus-fast>=4.0` floor, plus BLE callback/connection fixes. Do not assume these changes exist in stable 3.0.2. Some October PR workflows failed or required action; this does not negate the cited successful September develop push.
- Risks: Bluetooth scan/connect permissions, OS adapter constraints, pairing/security, device-specific GATT behavior, untrusted advertisements and mobile background restrictions. No independent scan, GATT operation, physical peripheral, Android package build or security audit performed.
- Next: simulated BlueZ GATT regression with virtual controller, Windows mock integration, Android packaging feasibility, BLE discovery and GATT error-path handling.

## Existing catalog maintenance
- **PySTAC:** replaced a generic uninspected follow-up reference with source-backed direct dependency and upstream CI context; score remains S28.
- **python-zeroconf:** identified as complementary local-network discovery, **not** a Bleak dependency. No score or dependency change.

## Verification boundary
GitHub READMEs, tagged manifests, root licenses, changelogs, source and test trees, CI workflow definitions and individual GitHub Actions job conclusions were inspected. No code copied. No local Python build, test, installation, network transaction, Bluetooth connection, firmware flashing or security assessment was performed.
