# Research dossier — python-can-isotp and pip-audit (2026-11-02)

## Provenance and method
GitHub-first recursive CAN protocol investigation and independent defensive Python supply-chain discovery. Examined primary upstream README, licenses, manifests, releases, source/test trees, recent commits, CI definitions and job results. Exact-ID searches for YouTube seeds `PLMy8ocrgmZ9yfqy1-bgSX4q3HPezvTMAr` and `PLMI6SBmd587c` returned no indexed transcripts. No claims attributed to YouTube; no third-party code copied.

## python-can-isotp — VERIFIED upstream, A24 (5/3/5/4/4/3)
- https://github.com/pylessard/python-can-isotp; MIT license (2017 Pier-Yves Lessard). [v2.0.7](https://github.com/pylessard/python-can-isotp/releases/tag/v2.0.7) published **2025-05-14**. Tagged setup.py declares Python >=3.7; python-can appears as optional test/dev dependency.
- Reusable pieces: `isotp/protocol.py` ISO-TP PDU, flow-control and transport state machine, `CanStack`/`NotifierBasedCanStack`; `isotp/address.py` addressing; `isotp/tpsock/` Linux kernel CAN_ISOTP wrapper; `test/test_transport_layer_logic.py`, `test/test_can_stack.py` and `test/test_socket.py` fixtures.
- Jenkinsfile defines Docker NET_ADMIN, vcan0–vcan4 and Python 3.7–3.11 test matrix. **Configuration is not evidence of a successful Jenkins run.** GitHub Actions returned no runs; no independent test performed.
- [2026-08-22 commit](https://github.com/pylessard/python-can-isotp/commit/5593c219f) fixes reserved STmin handling on v2.x. This postdates stable v2.0.7; do not attribute fix to tagged release.
- Linux kernel path requires SocketCAN support; user-space path can integrate with optional python-can. CAN transmissions can actuate equipment; use virtual or authorized isolated systems.
- Follow-up: offline frame/flow-control round trips, vcan integration, compare stable/main, obtain Jenkins results, inspect UDS ecosystem.

## pip-audit — VERIFIED upstream, S28 (5/5/5/4/5/4)
- https://github.com/pypa/pip-audit; Apache-2.0 license. [v2.10.1](https://github.com/pypa/pip-audit/releases/tag/v2.10.1) published **2026-06-10** with OSV malformed-range handling fix. Main updated **2026-10-30**. Python >=3.10.
- Reusable pieces: `pip_audit/_dependency_source/` requirements, pyproject and PEP 751 lockfile parsing; `_service/pypi.py`, `osv.py`, `esms.py`; `_format/` JSON/Markdown/CycloneDX; `_fix.py` opt-in remediation. Dedicated test/service, test/format and test/dependency_source fixtures.
- [2026-11-02 scheduled CI](https://github.com/pypa/pip-audit/actions/runs/41443587420) **8 successful jobs**: Linux Python 3.10–3.14, Windows, coverage and aggregate. Workflow enforces >=100% reported coverage; this is upstream evidence, not a security guarantee.
- [pypa/gh-action-pip-audit](https://github.com/pypa/gh-action-pip-audit) is official Apache-2.0 companion; [pypa/advisory-database](https://github.com/pypa/advisory-database) uses CC-BY-4.0 data license. OSV and CycloneDX are related integrations.
- Limits: feeds may lack advisories, resolution may be incomplete, network/index access can fail, and `--fix` can alter dependency graphs. No independent install, scan, SBOM check or fix performed.
- Follow-up: PEP 751 fixture tests, JSON/CycloneDX export, private-index behavior, action pinning, coverage of transitive dependency resolution.

## Catalog maintenance
Existing python-can entry cross-linked to optional python-can-isotp; not represented as a core dependency. Added two canonical entries and corresponding master headings. License obligations documented; no third-party source copied.
