# GitHub Gold — dbus-fast and STAC API Validator research (2026-11-01)

## Scope and provenance
GitHub-first recursive follow-up from Bleak (Linux D-Bus backend) and PySTAC Client (STAC API conformance). The six YouTube seeds remain recorded in `sources/youtube_playlists.md`; no playlist transcript was retrieved or attributed in this batch. Source trees, manifests, releases, tests and GitHub Actions job conclusions were inspected. **CI evidence is upstream, not local execution.** No third-party source was copied.

## dbus-fast — VERIFIED (upstream) / S28
- Repository: https://github.com/Bluetooth-Devices/dbus-fast ; root MIT LICENSE: https://github.com/Bluetooth-Devices/dbus-fast/blob/main/LICENSE . Preserve copyright/permission notice; review build-time dependencies separately.
- Stable [v5.2.0](https://github.com/Bluetooth-Devices/dbus-fast/releases/tag/v5.2.0) published **2026-10-02**. `pyproject.toml` declares Python **>=3.11**. v5.1.0 changelog explicitly dropped Python 3.10. `pip install dbus-fast` provides D-Bus support; optional Cython wheels accelerate (un)marshalling; `SKIP_CYTHON=1` allows pure-Python source builds.
- Source evidence: `src/dbus_fast/aio/message_bus.py` implements async socket write queues and D-Bus authentication; `aio/proxy_object.py` exposes proxies; `glib/` supplies GLib integration; `_private/marshaller.py` validates typed messages, rejects embedded NUL strings and caps arrays at 64 MiB; `service.py`, `signature.py`, `introspection.py`, `auth.py` are reusable. Examples include `aio-list-names.py`, `example-service.py`, `mpris.py`. Tests include auth, fd passing, marshalling and message-bus suites.
- **Upstream main push CI:** [2026-10-02 run 37015505832](https://github.com/Bluetooth-Devices/dbus-fast/actions/runs/37015505832) — **18 successful jobs, 3 skipped**. Python 3.11–3.15, Cython and pure-Python variants, s390x, lint and benchmarks. The separate [2026-11-01 scheduled workflow](https://github.com/Bluetooth-Devices/dbus-fast/actions/runs/41335649926) failed; it was not diagnosed and should not be conflated with successful push CI.
- Relationship: Bleak v3.0.2 Linux backend declares `dbus-fast>=1.83.0`; this does **not** mean dbus-fast 5.2 works on Python 3.10, which Bleak itself still supports. Resolve a compatible older dbus-fast on Python 3.10. dbus-fast derives from `altdesktop/python-dbus-next`; BlueZ is an OS service, not a Python package dependency.
- Limitations: no independent install, D-Bus session/system bus test, BlueZ/GATT test, performance reproduction, or security audit. System bus permissions and spoofable service identity require trust boundaries.
- Next: test pure-Python serialization and invalid-input handling; isolate a private D-Bus daemon and run an example service; verify Bleak BlueZ compatibility on Python 3.11+ and resolve Python 3.10 dependency pin.

## STAC API Validator — VERIFIED (upstream) / A24
- Repository: https://github.com/stac-utils/stac-api-validator ; root [Apache-2.0 LICENSE](https://github.com/stac-utils/stac-api-validator/blob/main/LICENSE), with Radiant Earth Foundation copyright. Preserve license and notices; inspect third-party dependencies separately.
- Stable [v0.6.8](https://github.com/stac-utils/stac-api-validator/releases/tag/v0.6.8) published **2026-02-20**. Manifest declares Python **>=3.11**, `pystac-client>=0.8.6`, `pystac[orjson]>=1.13.0`, `stac-check>=1.11.1`, `stac-validator>=3.10.1`, plus requests, Shapely, jsonschema, and others.
- Source evidence: `src/stac_api_validator/validations.py` imports PySTAC, PySTAC Client, requests and validators and checks API responses/conformance; `filters.py` constructs CQL2 text/JSON comparison, temporal and spatial filters; `geometries.py` contains spatial fixtures; `__main__.py` is the CLI. `tests/test_validations.py` uses mock HTTP and local STAC fixtures; additional `test_main.py` and `test_landing_page.py` exist.
- **Upstream main push Tests CI:** [2026-03-23 run 23437566679](https://github.com/stac-utils/stac-api-validator/actions/runs/23437566679) — **8/8 jobs passed** (Ubuntu Python 3.11–3.14, Windows/macOS 3.14, docs, coverage). June 2026 dependency PR workflows passed; latest inspected main commit dated 2026-03-23.
- Important quality boundary: README explicitly calls API behavior validation **work in progress** and a **subset**. `pyproject.toml` has `fail_under=10` for coverage (TODO to restore 85). This is useful conformance evidence, **not certification** or complete STAC API coverage; score A24 rather than S.
- Risks: validation issues HTTP requests and may send bearer/query credentials to the configured root. Do not point at untrusted/internal endpoints or use broad production credentials; expensive spatial searches may burden remote services. No independent installation, endpoint request, authenticated test, or security audit.
- Related: `stac-utils/pystac-client` and `stac-utils/pystac` are **upstream direct dependencies** of the validator, not vice versa; `stac-utils/stac-check` and `StacLabs/stac-validator` handle related object validation. Specification: `radiantearth/stac-api-spec`.
- Next: run deterministic local mock STAC API tests (core, item-search, filter/CQL2); assess false positives against known fixtures; document auth isolation and resource limits.

## Existing catalog maintenance
- **Bleak S28:** added exact Linux D-Bus dependency and Python-version compatibility warning; no score change.
- **PySTAC Client S27:** recorded downstream STAC API Validator as a consumer; not a dependency of the client.
- **PySTAC S28:** recorded validator as a downstream consumer; not a dependency of PySTAC.

## Verification boundary
Upstream documentation, release records, manifests, source trees, tests and CI job conclusions were inspected. **No code was installed, executed, benchmarked, or hardware-tested by GitHub Gold in this batch.** No third-party code was copied.