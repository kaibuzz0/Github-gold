# xdg-desktop-portal — sandbox capability broker and document portal

- **Repository:** https://github.com/flatpak/xdg-desktop-portal
- **Organization:** Flatpak
- **Category:** Linux sandboxing / desktop security / capability mediation / D-Bus / document access
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 28 / 30
- **Provisional tier:** S
- **Primary implementation license:** LGPL-2.1-or-later; repository also carries additional SPDX license texts for ancillary material
- **Primary language:** C
- **Build system:** Meson
- **Latest inspected stable release:** 1.22.1 — 2026-06-17
- **Discovery source:** recursive follow-up from `flatpak/xdg-dbus-proxy` and the Flatpak/Bubblewrap sandbox-policy ecosystem. No playlist-derived claims are used in this dossier.

## Executive finding

`flatpak/xdg-desktop-portal` is the Linux desktop capability-broker layer that allows sandboxed or otherwise contained applications to request narrowly scoped access to host resources through well-defined D-Bus interfaces.

It is valuable because it solves a different problem than namespace or IPC filtering. Bubblewrap can remove direct filesystem/device/network visibility. xdg-dbus-proxy can restrict what a sandbox can do over D-Bus. xdg-desktop-portal then provides explicit, mediated paths for operations that would otherwise require broad host authority: choosing files, opening URIs, screen capture, camera access, printing, notifications, background execution, USB access and related desktop capabilities.

The repository also contains a substantial **Document Portal**. That subsystem maps selected host files into a FUSE-backed document namespace and persists per-application access state instead of simply exposing arbitrary host paths to the sandbox.

## Why it qualifies as GitHub Gold

The project combines several reusable security and systems-design patterns:

1. capability-oriented APIs for sandboxed applications;
2. separation between generic portal interfaces and desktop-environment-specific backends;
3. user-mediated grants for sensitive host resources;
4. a FUSE-backed document namespace rather than raw path disclosure;
5. persistent permission storage and application identity tracking;
6. Unix file-descriptor passing for file selection and transfer;
7. request/session abstractions for long-running portal operations;
8. explicit security maintenance with regression fixes for real sandbox-boundary failures;
9. integration-style tests, installed tests, GCC/Clang builds and AddressSanitizer;
10. independently useful subcomponents such as the Document Portal, Permission Store and FileTransfer machinery.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Core desktop capability broker used to give confined applications controlled access to host resources. |
| Working evidence | 5/5 | Stable releases, broad installed/integration test surface, GCC/Clang CI, ASan, Meson install/dist checks and active security maintenance. |
| Reusability | 4/5 | Portal interfaces and architectural patterns are highly reusable, but the implementation is tightly coupled to Linux desktop, D-Bus, GLib, FUSE and desktop backend ecosystems. |
| Novelty | 4/5 | Capability brokering is established security architecture, but the combination of portal APIs, document FUSE namespace, app identity and desktop backend delegation is unusually useful. |
| Documentation | 5/5 | Dedicated generated portal documentation, interface definitions, release notes, security policy and architecture-visible source organization. |
| Maintenance | 5/5 | Active through 2026-09-02 with current fixes, plus a security-focused stable release on 2026-06-17. |

**Total: 28 / 30 — provisional S tier.**

## Architecture

The current repository is split into several security-relevant surfaces:

- `desktop-portal/` — the main generic portal broker and portal implementations;
- `document-portal/` — FUSE document namespace, document database, permission database and file-transfer support;
- `data/` — D-Bus interface/service metadata and portal definitions;
- `tests/` — portal and integration tests;
- `doc/` — generated interface and developer documentation;
- `.github/workflows/` — build/test/check/release automation.

The main portal layer contains dedicated implementations for capabilities such as account information, background execution, camera, clipboard, dynamic launchers, email, file chooser and other desktop operations.

The Document Portal is a separate and particularly strong component. Its current source tree includes:

- `document-portal-fuse.c` — FUSE-backed exported document namespace;
- `document-portal.c` — D-Bus document service and access orchestration;
- `document-store.c` — persisted document metadata;
- `permission-db.c` — permission database;
- `file-transfer.c` — cross-application file transfer using generated transfer keys and Unix FDs;
- service definitions for `org.freedesktop.portal.Documents` and the Permission Store.

## Capability-broker model

Portal APIs are meant to be callable by applications that do not possess broad direct access to the host resource. Instead of granting a sandbox unrestricted filesystem, camera, screen, USB or desktop authority, the application calls a portal interface.

The generic portal service can then:

1. identify the caller/application;
2. validate request arguments and policy;
3. delegate presentation or desktop-specific behavior to an implementation backend;
4. obtain user consent when the portal requires it;
5. return a bounded resource, handle, file descriptor or session rather than full ambient host access.

This is a classic capability-security pattern: **authority is obtained through explicit operations and bounded objects instead of global namespace visibility**.

## Document Portal and FUSE namespace

The Document Portal is one of the highest-value pieces in the repository.

Rather than exposing arbitrary host paths directly into a sandbox, selected files can be represented in a dedicated FUSE mount and associated with document IDs and application-specific permissions. This allows a sandbox to see only documents that have been intentionally exported to it.

The document subsystem stores metadata and permission state separately from the ordinary desktop portal process. The repository includes dedicated document-store and permission-database code, plus a service for `org.freedesktop.impl.portal.PermissionStore`.

This is a reusable design pattern for sandboxed systems: **translate a large host namespace into a narrow virtual namespace backed by explicit grants**.

## FileTransfer component

`document-portal/file-transfer.c` is a particularly useful source-level component.

A transfer object tracks:

- the sending D-Bus peer;
- the sender's resolved application identity;
- whether the transfer is writable;
- whether it auto-stops after retrieval;
- the exported files;
- a generated transfer key.

Files are added through Unix file descriptors rather than untrusted string paths alone. The code validates FDs and records parent device/inode information. For sandboxed receivers it opens selected files with `O_PATH | O_CLOEXEC`, passes them through the document-export machinery and returns paths inside the Document Portal mount.

The current implementation also checks that only the D-Bus sender that created a transfer can add files to it.

## 2026 FileTransfer security fix

Release **1.22.1**, published **2026-06-17**, fixed a security issue in `FileTransfer.RetrieveFiles` identified as **GHSA-c5cf-79w8-pvfh**.

Upstream states that a malicious sandboxed application could redirect drag-and-drop or copy/paste data to itself by exploiting a predictable FileTransfer key.

The current source creates transfer keys through `xdp_generate_key()` rather than relying on an obvious sequential or predictable identifier.

This is an important capability-security lesson: a transfer handle that authorizes retrieval is itself a security token. If another application can predict or steal it, the higher-level portal authorization model can be bypassed even when the underlying file access machinery is correct.

## 2026 FileChooser SaveFiles security fix

The same **1.22.1** release fixed **GHSA-cm83-2936-gxjm**, where a malicious sandboxed application could gain arbitrary write access to nonexistent files outside the sandbox through the `files` option in `FileChooser.SaveFiles`.

This illustrates another reusable invariant: path-like data returned from, or accepted around, a file chooser cannot automatically be treated as equivalent to a capability granted by the user. Creation targets, nonexistent paths and parent-directory authority require separate validation.

## App-ID validation hardening

Release 1.22.1 also tightened Document Portal application-ID validation. Upstream reports that a maliciously crafted App ID could cause arbitrary host files to be parsed as `Glib.KeyFile` data.

Application identity is therefore not just labeling metadata. In this architecture it influences permission lookup, persistence and file access. Caller identity strings must be validated before they are used in filesystem-backed or configuration-backed state.

## Testing and working evidence

The current reusable build-and-test workflow runs inside a controlled container and builds with both **GCC and Clang**.

The inspected workflow:

- enables `_FORTIFY_SOURCE=2`;
- configures Meson with installed tests and regular tests enabled;
- enables AddressSanitizer;
- treats warnings as errors;
- executes the Meson test suite with long tests enabled;
- installs the project;
- runs GNOME installed tests;
- builds a distribution tarball;
- uploads logs on both success and failure.

The repository has additional workflows for checks, container maintenance, main CI, documentation Pages and releases.

This is stronger evidence than a README claim alone because the project continuously exercises both its source-tree tests and its post-install test surface.

## CI supply-chain caveat

The inspected build workflow uses `actions/checkout@v4` and `actions/upload-artifact@v4` by mutable major-version tags rather than immutable commit SHAs.

That does not negate the runtime/test evidence, but it means workflow supply-chain pinning is not perfect and should not receive an implicit provenance guarantee.

## Release and maintenance evidence

Latest inspected stable GitHub release:

- **1.22.1**
- published **2026-06-17**
- release source archive: `xdg-desktop-portal-1.22.1.tar.xz`
- GitHub release metadata publishes SHA-256 digest `d4879ddb3d65ff1a8f19187497e6f13dc5d267bcac404a5d501218be355753d3`
- a separate `.sha256sum` asset is published alongside the tarball.

GitHub Gold did **not** independently download and hash the archive in this pass.

Development remained active through **2026-09-02**. Recent upstream changes include a compatibility fix for older libdex builds, conditionalization of portal tests based on optional dependencies, concurrency protection around application-info registry state, ordering/error-propagation fixes and session-persistence ownership fixes.

## License and reuse boundary

The main implementation headers and README use **LGPL-2.1-or-later** SPDX identifiers. The top-level Meson project also declares an LGPL-or-later license.

The repository additionally carries license texts for GPL-2.0-or-later, MIT, CC0-1.0 and the SIL Open Font License, indicating that ancillary files or bundled material may have different licensing.

Therefore this dossier does **not** describe the entire repository as uniformly LGPL without qualification. Any future copying or embedding must inspect the SPDX header of the exact files being reused.

No xdg-desktop-portal source was copied into GitHub Gold.

## Useful components / patterns to study

### 1. Document Portal FUSE implementation

`document-portal/document-portal-fuse.c` is a substantial reference implementation of a virtual filesystem used as a security boundary between host paths and sandbox-visible document paths.

### 2. Permission database

`document-portal/permission-db.c` is useful for studying persistent application-scoped capability records and update semantics.

### 3. FileTransfer token lifecycle

`document-portal/file-transfer.c` combines capability tokens, Unix FD passing, sender identity, document export, write-permission propagation and auto-stop semantics.

### 4. Application identity registry

Recent concurrency fixes around the app-info registry show that caller identity resolution is a shared stateful subsystem, not a trivial string lookup.

### 5. Request/session abstractions

Screen-cast, remote-desktop and similar portal operations require long-lived request/session state, cancellation and persistence semantics. These are strong patterns for any broker that mediates asynchronous privileged operations.

### 6. Generic interface / backend separation

The generic broker exposes stable D-Bus interfaces while desktop-environment-specific implementation backends provide presentation and platform integration. That separation is useful for portability within a heterogeneous platform ecosystem.

## Platforms and requirements

This project should be cataloged as Linux/Unix desktop infrastructure rather than a generic cross-platform capability broker.

Key assumptions include:

- D-Bus;
- GLib/GIO;
- Linux/Unix file descriptors and process semantics;
- FUSE for the Document Portal;
- desktop-specific portal implementation backends;
- optional integrations such as PipeWire/WirePlumber, Flatpak interfaces, geolocation or USB support depending on the build.

## Security boundaries and caveats

- Portals reduce ambient authority; they do not make an untrusted application safe by themselves.
- Correct security depends on the surrounding sandbox preventing direct access that would bypass the portal.
- Desktop backend implementations are part of the trusted path and require their own review.
- User-consent dialogs are security UX and can still be undermined by confused-deputy or spoofing problems if application identity/presentation is wrong.
- Long-lived permissions and restore tokens require careful persistence and revocation semantics.
- FUSE/document mappings must preserve inode/path/rename/unlink invariants under races.
- File descriptors, transfer keys, session handles and restore tokens are capabilities and must be treated as sensitive authority-bearing objects.

## Verification performed by GitHub Gold

This pass inspected current upstream:

- repository metadata and README;
- repository source-tree organization;
- `desktop-portal/` portal implementation surface;
- `document-portal/` component inventory;
- `document-portal/file-transfer.c` transfer lifecycle and FD/document-export path;
- current GitHub release metadata and 1.22.1 security notes;
- current commit activity through 2026-09-02;
- the reusable build-and-test GitHub Actions workflow;
- top-level Meson project/build metadata;
- repository license inventory.

## Not independently verified

GitHub Gold did **not**:

- build or install xdg-desktop-portal;
- run its regular or installed tests;
- launch a portal backend;
- create a sandbox and request capabilities through the portal;
- mount or exercise the Document Portal FUSE filesystem;
- reproduce either 1.22.1 security advisory;
- test FileTransfer key unpredictability statistically;
- test file-chooser path race behavior;
- verify D-Bus application identity under hostile peers;
- reproduce screen-cast/remote-desktop/session persistence behavior;
- fuzz D-Bus, FUSE, file-descriptor or permission-database inputs;
- independently hash release assets;
- perform a security audit.

Claims above are therefore separated between upstream release/source/CI evidence and actions independently performed by GitHub Gold.

## Related projects

- https://github.com/flatpak/xdg-dbus-proxy — filters D-Bus authority exposed to confined applications.
- https://github.com/containers/bubblewrap — constructs namespace-based Linux sandboxes.
- https://github.com/flatpak/flatpak — primary desktop sandbox ecosystem integrating these primitives.
- desktop-specific portal backends such as GNOME/KDE implementations — trusted implementations behind generic portal interfaces.

## Strongest follow-up research

1. trace `document-portal-fuse.c` lookup/open/rename/unlink behavior and TOCTOU resistance;
2. inspect `permission-db.c` persistence, atomicity, corruption handling and revocation semantics;
3. trace `xdp_generate_key()` entropy/source and FileTransfer lifecycle after the 1.22.1 advisory;
4. inspect application-ID validation and app-info registry identity derivation;
5. trace `FileChooser.SaveFiles` handling around nonexistent files and parent-directory authority;
6. inspect request/session persistence and restore-token authorization for ScreenCast/RemoteDesktop;
7. map the trusted path across xdg-desktop-portal and desktop-specific backend implementations;
8. evaluate the Document Portal and Permission Store as individually catalogable reusable subcomponents.
