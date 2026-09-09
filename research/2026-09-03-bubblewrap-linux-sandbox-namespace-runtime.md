# containers/bubblewrap — Linux namespace sandbox construction runtime

- **Repository:** https://github.com/containers/bubblewrap
- **Author / organization:** containers
- **Category:** Linux sandboxing / namespace isolation / defensive runtime / desktop application isolation
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28 / 30 — S tier**
- **License:** LGPL-2.1-or-later
- **Primary language:** C
- **Inspection date:** 2026-09-03
- **Discovery mode:** GitHub-first category rotation; no playlist-derived claims used in this pass

## Why this is GitHub Gold

Bubblewrap is a compact Linux sandbox-construction tool built directly on kernel isolation primitives rather than a large orchestration stack. It always constructs a new mount namespace and can additionally isolate user IDs, IPC, PIDs, networking, UTS/hostname state, and apply caller-supplied seccomp filters. It is used as a lower-level isolation primitive by larger systems such as Flatpak.

The strongest Gold value is not a prepackaged security policy: Bubblewrap is intentionally a **policy mechanism**. Its caller decides what filesystem paths, namespaces, devices, sockets, capabilities, and syscalls should be visible. That makes the repository valuable both as a production defensive tool and as a compact reference implementation for Linux sandbox construction.

Upstream repository: https://github.com/containers/bubblewrap

## Gold scoring

| Dimension | Score | Evidence summary |
|---|---:|---|
| Utility | 5/5 | Practical process isolation for desktop apps, build systems, test runners, developer tools, local agents, and other unprivileged Linux workloads. |
| Working Evidence | 5/5 | Current security releases, Meson build/test CI, ASan/UBSan, CodeQL, smoke tests, distribution-build tests, and explicit subproject integration tests. |
| Reusability | 4/5 | Small focused C codebase and command-line primitive with reusable implementation ideas, but it is primarily a Linux executable rather than a stable embeddable library API. |
| Novelty | 4/5 | Linux namespaces/seccomp are established mechanisms, but Bubblewrap's minimal policy-neutral construction model and careful path/mount handling are unusually valuable. |
| Documentation | 5/5 | Detailed README, manual XML, security policy, limitations, demos, NEWS/release notes, tests, and implementation comments. |
| Maintenance | 5/5 | v0.12.0 shipped 2026-08-26 with a security fix and architectural cleanup; substantive main commits continued through 2026-09-01. |

**Total: 28/30 — provisional S tier.**

## What the project actually does

Bubblewrap creates a new, initially empty mount namespace whose root is a tmpfs, then constructs the filesystem and process environment requested by the caller. The README documents optional isolation using:

- user namespaces (`CLONE_NEWUSER`)
- IPC namespaces (`CLONE_NEWIPC`)
- PID namespaces (`CLONE_NEWPID`)
- network namespaces (`CLONE_NEWNET`)
- UTS namespaces (`CLONE_NEWUTS`)
- seccomp filters
- read-only and device-restricted bind mounts
- `PR_SET_NO_NEW_PRIVS`

Reference:
https://github.com/containers/bubblewrap/blob/main/README.md

Bubblewrap also supplies a minimal PID 1 inside a PID namespace to reap children correctly.

## Strong reusable components / ideas

### 1. Root-confined path resolution with `openat2()`

`safe_openat.c` is one of the highest-value implementation surfaces. Current code attempts Linux `openat2()` with:

- `RESOLVE_IN_ROOT`
- `RESOLVE_NO_MAGICLINKS`

This resolves paths relative to an already-open root directory rather than trusting normal pathname traversal. When `openat2()` is unavailable or rejected in supported compatibility cases, Bubblewrap falls back to its own chroot-style path-resolution logic.

Source:
https://github.com/containers/bubblewrap/blob/main/safe_openat.c

This deserves separate study for any project that must safely construct files or mounts beneath an attacker-influenced directory tree.

### 2. Symlink-escape hardening during sandbox setup

Release **v0.12.0** fixed GHSA-pxhw-h44j-8pfx, where files/directories created during sandbox setup could follow parent symlinks outside the intended sandbox root. Upstream addressed this through root-confined path resolution using `openat2(RESOLVE_IN_ROOT)` or its compatibility fallback.

Release:
https://github.com/containers/bubblewrap/releases/tag/v0.12.0

This is particularly useful evidence because it shows the maintainers actively treating filesystem construction as a security-sensitive race/path-resolution problem rather than ordinary path manipulation.

### 3. Recursive mount-attribute hardening with `mount_setattr()`

A substantive **2026-08-27** commit moved recursive mount-flag application to the newer `mount_setattr()` API where available. Upstream states that this applies flags to an entire mount tree in one operation, avoiding time-of-check/time-of-use races caused by a changing mount table and improving performance with many mounts.

Commit:
https://github.com/containers/bubblewrap/commit/b7cdf7a0e6d70106de56f34d82d9e35856c0cf27

The repository also retains a fallback path for older kernels.

### 4. Namespace assembly and privilege reduction

`bubblewrap.c` is the core process/namespace orchestration surface. The project uses unprivileged user namespaces rather than relying on a privileged long-running daemon.

The README explicitly notes `PR_SET_NO_NEW_PRIVS`, preventing setuid binaries inside the sandbox from gaining new privilege in the traditional chroot-escape style.

Relevant source:
https://github.com/containers/bubblewrap/blob/main/bubblewrap.c

### 5. Seccomp plumbing without hardcoding application policy

Bubblewrap accepts seccomp programs supplied by its caller rather than trying to encode one universal syscall policy. The test tree contains a dedicated `tests/test-seccomp.py` suite.

This is a useful separation-of-concerns model: Bubblewrap supplies the enforcement mechanism while frameworks such as Flatpak decide which syscall policy belongs to a particular application class.

### 6. Bind-mount construction and mount-tree handling

`bind-mount.c` / `bind-mount.h` implement a large part of the filesystem-view construction logic. This is worth deeper component inspection around:

- read-only bind behavior
- recursive mount properties
- mount propagation
- device restrictions
- nested mount trees
- race-resistant remount handling

Sources:
https://github.com/containers/bubblewrap/blob/main/bind-mount.c
https://github.com/containers/bubblewrap/blob/main/bind-mount.h

### 7. Policy boundary as an architectural lesson

The repository is unusually explicit that Bubblewrap itself is **not a complete sandbox policy**. The security boundary depends on the arguments supplied by the caller.

Examples from upstream limitations:

- exposing a D-Bus socket can allow the sandbox to invoke privileged host services unless communication is filtered;
- `--new-session` or appropriate seccomp filtering is needed to address terminal `TIOCSTI` attacks;
- removing syscalls or filesystem resources required by an application's own internal sandbox can accidentally weaken defense-in-depth.

That distinction is important enough to treat as a Gold design principle: isolation primitives and isolation policy are separate security layers.

## Current security model changes

### Setuid mode removed

Historical Bubblewrap supported a setuid installation mode for systems without usable unprivileged user namespaces. Upstream deprecated that path following security problems and **v0.12.0 removes setuid support entirely**. Current security documentation states that newer Bubblewrap refuses to operate if the binary is made setuid.

This materially reduces one of the project's historical host-privilege attack surfaces.

Earlier **v0.11.2** was a security update for **CVE-2026-41163**, affecting setuid Bubblewrap configurations. The release prevented low-privilege setup code from running dumpable, which had allowed ptrace interference. The current removal of setuid support narrows future exposure to this class.

Security policy:
https://github.com/containers/bubblewrap/blob/main/SECURITY.md

Release notes:
https://github.com/containers/bubblewrap/releases/tag/v0.11.2
https://github.com/containers/bubblewrap/releases/tag/v0.12.0

## Working evidence

### Current release

Latest stable release inspected:

- **v0.12.0**
- published **2026-08-26**
- source tarball plus SHA-256 checksum asset
- GitHub release metadata also exposes the tarball digest

The release includes the `openat2(RESOLVE_IN_ROOT)` symlink-escape fix, removes setuid support, introduces an `assume_kernel` build option, and adds `--not-a-security-boundary` for explicitly non-security uses where some setup failures can be tolerated.

GitHub Gold did **not** independently download and hash the release artifact.

### Current maintenance

Main remained active through **2026-09-01**. Recent substantive work includes:

- rejecting empty path arguments that could otherwise map to the sandbox root in dangerous ways;
- recursive mount-flag application through `mount_setattr()` to reduce TOCTOU exposure;
- compatibility fixes for musl and older compiler language modes;
- test cleanup and portability improvements.

Recent commits:
https://github.com/containers/bubblewrap/commits/main/

### Tests / CI

Current CI builds Bubblewrap with Meson/GCC and enables:

- `_FORTIFY_SOURCE=2`
- AddressSanitizer
- UndefinedBehaviorSanitizer
- a real Bubblewrap smoke test
- the Meson test suite with `BWRAP_MUST_WORK=1`
- install validation
- `meson dist` validation
- an explicit **use-as-subproject** build/install/test path

A separate Clang job builds with SELinux enabled and runs GitHub CodeQL analysis.

Workflow:
https://github.com/containers/bubblewrap/blob/main/.github/workflows/check.yml

The test directory includes:

- `test-run.sh`
- `test-sandbox.py`
- `test-seccomp.py`
- explicit PID namespace tests
- explicit user namespace tests
- C utility tests
- syscall helper tests
- subproject integration tests

Tests:
https://github.com/containers/bubblewrap/tree/main/tests

### CI supply-chain caveat

The inspected workflow references `actions/checkout@v4`, `actions/upload-artifact@v4`, and `github/codeql-action/*@v2` through version tags rather than immutable commit SHAs. This does not invalidate the CI evidence, but GitHub Gold should not describe the workflow as fully immutable-pinned.

## Build / runtime requirements

Bubblewrap is Linux-specific and relies on Linux namespaces and mount APIs. Upstream uses Meson/Ninja for source builds:

```text
meson _builddir
meson compile -C _builddir
meson test -C _builddir
meson install -C _builddir
```

Modern deployments require usable unprivileged user namespaces because setuid mode has been removed.

Kernel capability and policy vary by distribution; some distributions restrict unprivileged user namespaces through sysctls, LSM policy, or downstream configuration.

## Licensing / reuse

Current source has been updated to **LGPL-2.1-or-later**. The repository's `COPYING` contains GNU LGPL 2.1 and current source notices use LGPL 2.1-or-later language.

License:
https://github.com/containers/bubblewrap/blob/main/COPYING

The current release notes explicitly record the project-wide update from LGPL 2.0-or-later to LGPL 2.1-or-later.

No Bubblewrap source was copied into GitHub Gold during this pass.

Because this is copyleft-licensed source, any future extraction or adaptation should review the precise LGPL obligations and file-level provenance before copying code. `safe_openat.c`, for example, explicitly records that it was adapted/copied from `crun` and preserves that provenance.

## Security / operational caveats

Bubblewrap must not be cataloged as "run any untrusted program safely" without qualification.

Important boundaries:

- the caller defines the sandbox policy;
- host files, sockets, devices, or services explicitly exposed to the sandbox can become escape/privilege channels;
- a network namespace does not itself define application-layer authorization;
- seccomp policies can remove attack surface but can also conflict with an application's own sandboxing;
- kernel namespace and mount vulnerabilities remain below Bubblewrap's trust boundary;
- denial-of-service/resource exhaustion needs separate cgroup/rlimit/operator controls;
- Linux distribution user-namespace policy can determine whether Bubblewrap can run at all;
- filesystem sandboxing does not automatically protect secrets deliberately mounted into the sandbox.

## Why 28 instead of 30

Reusability is 4/5 because Bubblewrap is designed primarily as a focused executable/tool rather than a stable reusable library API. Novelty is 4/5 because namespaces, seccomp, no-new-privileges, and bind mounts are established Linux mechanisms. Its value lies in careful implementation and composition rather than inventing new isolation primitives.

## Verification performed by GitHub Gold

Performed in this pass:

- repository metadata inspection
- README/security-model inspection
- current license inspection
- v0.12.0 and v0.11.2 release inspection
- recent commit inspection
- CI workflow inspection
- test-tree inspection
- source inspection of `safe_openat.c`
- source/component discovery for namespace, bind-mount, seccomp, and mount handling
- duplicate search against the current GitHub Gold repository

Not performed:

- local build
- Meson test execution
- ASan/UBSan execution
- CodeQL reproduction
- namespace isolation test
- seccomp execution test
- mount-race reproduction
- symlink-escape exploit reproduction
- CVE-2026-41163 reproduction
- GHSA-pxhw-h44j-8pfx reproduction
- Flatpak integration test
- independent security audit
- release artifact checksum verification

Therefore **VERIFIED** means repository-native evidence strongly supports the cataloged behavior; it does not mean GitHub Gold independently proved the sandbox boundary in this pass.

## Strong recursive leads

1. **`safe_openat.c`** — compare `openat2(RESOLVE_IN_ROOT)` with the compatibility fallback and enumerate path-resolution invariants.
2. **`bind-mount.c`** — inspect recursive mount handling and `mount_setattr()` fallback behavior.
3. **Flatpak sandbox policy** — study how a major caller converts an application permission model into Bubblewrap arguments.
4. **`xdg-dbus-proxy`** — separate Gold candidate for filtering D-Bus IPC exposed to sandboxes.
5. **seccomp handoff** — inspect FD passing/filter installation and interaction with application self-sandboxing.
6. **PID 1 helper behavior** — child reaping, signals, process lifecycle, and exit propagation.
7. **user namespace policy differences** — catalog practical constraints across major Linux distributions.
8. **crun provenance** — compare Bubblewrap's `safe_openat` implementation with upstream crun hardening.
9. **sandbox test harness** — inspect the Python/shell test suite for reusable namespace/security regression patterns.
10. **resource controls** — identify complementary cgroup/rlimit tooling because Bubblewrap is intentionally not a resource-governance system.

## Steward conclusion

`containers/bubblewrap` clears the GitHub Gold quality bar as a compact, actively maintained, security-sensitive Linux isolation primitive. Its strongest technical value is in race-resistant filesystem construction, namespace composition, privilege reduction, and its explicit separation between sandbox mechanism and sandbox policy. Future work should go component-level on `safe_openat.c`, `bind-mount.c`, and a major caller such as Flatpak rather than treating Bubblewrap as a universal sandbox by itself.
