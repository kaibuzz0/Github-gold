# Maintenance notes — 2026-10-21

Upstream evidence only; no independent execution or source copying.

- Meshtastic firmware: latest GitHub non-prerelease v2.7.26.54e0d8d (2026-06-24); develop CI succeeded 2026-10-21 (https://github.com/meshtastic/firmware/actions/runs/39633190319). Routing and packet-state modules in src/mesh are promising. GPL-3.0.
- whisper.cpp: v1.9.5 (2026-10-06); upstream CPU CI passed 5/5 jobs on 2026-10-19 (https://github.com/ggml-org/whisper.cpp/actions/runs/39266836864). C API, streaming and VAD examples. MIT root source; model weights separately licensed.
- uv: v0.13.5 (2026-10-22 UTC) updates managed Python builds after certificate-trust changes; existing pinned virtual environments do not update automatically. CI passed (https://github.com/astral-sh/uv/actions/runs/39720666204). Apache-2.0 OR MIT.

Follow up on Meshtastic signing policy, whisper model validation and uv interpreter updates.
