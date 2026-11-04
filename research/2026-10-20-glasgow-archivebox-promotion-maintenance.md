# Glasgow Interface Explorer and ArchiveBox — promotion evidence (2026-10-20)

**Method:** GitHub-first upstream inspection. YouTube seed search yielded no usable transcript lead. No third-party source copied.

## Glasgow Interface Explorer — PROMISING / S 27
- Upstream: https://github.com/GlasgowEmbedded/glasgow
- Score factors: Utility 5, Working Evidence 4, Reusability 5, Novelty 5, Documentation 4, Maintenance 4.
- Inspected software manifest (`0BSD OR Apache-2.0`, Python >=3.13,<3.16, Amaranth), source/test trees, license texts, workflow, recent commits and CI status.
- **Upstream main CI succeeded 2026-10-20** on `640848a91c93f697b67f1802639963ffc645d235`: https://github.com/GlasgowEmbedded/glasgow/actions/runs/39421095221 . This improves Working Evidence from the earlier 3/5 to 4/5, but does not establish real-hardware behavior.
- Specific components: `software/glasgow/gateware/` (SPI, I2C, UART, JTAG, SWD, QSPI), `software/glasgow/protocol/sfdp.py`, `software/glasgow/applet/interface/`, `software/tests/gateware/`, `firmware/`, `hardware/boards/glasgow/`.
- Current commit switches to PEP 751 lockfile format; no GitHub Releases observed; package labels itself Alpha.
- Caveats: SFDP parser covers base JESD216/JESD216A, not every revision; hardware electrical limits; external submodule/vendor/hardware licensing. No local tests, synthesis, flashing or measurements.

## ArchiveBox — VERIFIED / S 28
- Upstream: https://github.com/ArchiveBox/ArchiveBox
- Score factors: Utility 5, Working Evidence 5, Reusability 5, Novelty 4, Documentation 5, Maintenance 4.
- **Corrected maintenance snapshot:** v0.9.73 published **2026-10-06** as non-prerelease, superseding the September dossier's v0.7.4 stable claim. Release: https://github.com/ArchiveBox/ArchiveBox/releases/tag/v0.9.73 . Features include cloud document capture plugins, mobile replay improvements and large-archive performance fixes.
- On 2026-10-20 dev manifest reports `0.9.74rc327`; this is development, not a newer stable release.
- **Upstream CI succeeded 2026-10-20** on `11e6dd3150eb1e88794d7d29787ba82e5fa914ba`; later dev-head CI was still queued at inspection.
- Reusable modules: `archivebox/cli/`, `archivebox/api/`, `archivebox/crawls/`, `archivebox/personas/`, `archivebox/mcp/`, `archivebox/plugins/`; companion https://github.com/ArchiveBox/abx-dl .
- Root MIT license (Nick Sweeting 2026); external browsers, downloaders, plugins and captured content retain independent rights.
- Caveats: untrusted replay, authenticated browser cookies, external tool dependency surface. No independent installation, live crawl, replay or security audit.

## Integration and next checks
- Existing branch: 45 canonical entries, 45 matching master headings, empty candidate queue; neither new repository was present.
- Proposed synchronized promotion: 47 unique canonical entries, 47 matching headings; two six-factor scores checked.
- Follow up: Glasgow pinned CI reproduction and malformed SFDP fixtures; ArchiveBox isolated stable v0.9.73 capture/replay testing and abx-dl plugin license review.
