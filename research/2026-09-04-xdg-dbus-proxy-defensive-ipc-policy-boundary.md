# xdg-dbus-proxy — defensive D-Bus IPC policy boundary

- **Repository:** https://github.com/flatpak/xdg-dbus-proxy
- **Organization:** Flatpak
- **Category:** Linux sandboxing / IPC mediation / desktop security / D-Bus policy
- **Evidence level:** VERIFIED
- **Provisional Gold score:** 27 / 30
- **Provisional tier:** S
- **License:** LGPL-2.1-or-later
- **Primary language:** C
- **Build system:** Meson
- **Runtime dependencies:** GLib, GIO, gio-unix
- **Latest inspected stable release:** 0.1.8 — 2026-08-11
- **Discovery source:** recursive follow-up from the Bubblewrap/Flatpak sandbox-policy ecosystem; GitHub-first source inspection. No playlist-derived claims are used in this dossier.

## Executive finding

`flatpak/xdg-dbus-proxy` is a compact, standalone filtering proxy for D-Bus connections. It originated inside Flatpak and was split into its own module specifically so it could be reused outside Flatpak.

Its value is not that it provides another D-Bus client API. It provides a **policy-enforcement boundary between a less-trusted process and an existing D-Bus bus**. The proxy accepts a client on a Unix-domain socket, opens a connection to the configured upstream bus, forwards the authentication phase, and then can filter post-authentication D-Bus traffic according to name-level and message-level policy.

This makes it a strong companion to namespace sandboxes such as Bubblewrap. Bubblewrap can decide whether an application sees a socket; xdg-dbus-proxy can narrow what the application is allowed to do through that socket.

## Why it qualifies as GitHub Gold

The project is small enough to study as a complete security-relevant component, but it contains several unusually reusable design ideas:

1. a standalone IPC mediation boundary rather than a full application sandbox;
2. name visibility and interaction policy separated into SEE / TALK / OWN levels;
3. finer-grained call and broadcast rules by bus name, interface/member and object path;
4. explicit request/reply tracking so replies are accepted only for outstanding calls;
5. mediation of D-Bus name discovery and ownership operations instead of merely filtering raw method destinations;
6. a Unix-socket front end that can be placed inside a sandbox while the real bus remains outside;
7. a test harness that launches a real D-Bus daemon and exercises policy behavior through actual D-Bus connections;
8. Meson subproject support for embedding the component in a larger build;
9. recent security maintenance with regression tests for a real filtering bypass.

## Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Provides a practical least-privilege boundary for exposing D-Bus to sandboxed applications. |
| Working evidence | 5/5 | Dedicated integration-style tests, Meson CI, Clang sanitizers, CodeQL, Valgrind, install/dist/subproject checks, and a current stable release. |
| Reusability | 5/5 | Standalone executable, documented policy CLI, explicit Meson subproject support, small dependency surface. |
| Novelty | 4/5 | D-Bus mediation is established technology, but this is a particularly compact and reusable implementation of desktop IPC policy. |
| Documentation | 4/5 | README is minimal, but the installed manual documents policy semantics, CLI options, rule grammar and examples in detail. |
| Maintenance | 4/5 | Security-focused release 0.1.8 landed 2026-08-11 with tests; activity is healthy but lower-volume than larger upstreams. |

**Total: 27 / 30 — provisional S tier.**

## Architecture

The current repository is deliberately small. The main implementation surface is centered on:

- `dbus-proxy.c` — command-line/process orchestration and proxy configuration;
- `flatpak-proxy.c` / `flatpak-proxy.h` — D-Bus connection forwarding, policy and message filtering;
- `xdg-dbus-proxy.xml` — user-facing manual and policy grammar;
- `tests/test-proxy.c` — live D-Bus policy test harness;
- `meson.build` — build, dependency and subproject integration;
- `.github/workflows/check.yml` — build/test/analyzer/Valgrind CI.

The build declares GLib, GIO and gio-unix >= 2.40. When used as a Meson subproject, the caller must provide a program prefix and the proxy installs into the caller's libexec directory rather than colliding with the system command.

## D-Bus mediation model

The proxy listens on a Unix-domain socket. For each client connection, it opens an upstream D-Bus connection. Authentication bytes are forwarded, and after authentication the proxy can either operate unfiltered or apply policy.

The upstream source documents an important scope boundary: filtering applies to **outgoing signals and method calls and incoming broadcast signals**. Replies to an outstanding method call are allowed once; unsolicited method returns or errors are not treated as freely acceptable traffic.

This reply-tracking behavior is an important reusable security pattern: authorization is not only destination-based. The proxy also maintains enough protocol state to distinguish a legitimate response from an unsolicited message that merely has a response-shaped message type.

## SEE / TALK / OWN policy model

The base policy is a mapping from well-known D-Bus names to three cumulative levels:

### SEE

Allows visibility-oriented operations such as listing the name, asking whether it has an owner, resolving its owner, and observing relevant `NameOwnerChanged` events.

### TALK

Includes SEE and permits interaction with the peer: method calls/signals, matching broadcast reception and `StartServiceByName()`.

### OWN

Includes TALK and allows ownership operations such as `RequestName`, `ReleaseName`, and `ListQueuedOwners` for the allowed name.

The initial filtered policy is intentionally restrictive: the proxied client can talk to the bus itself and its own unique ID while other clients remain invisible unless policy grants additional access.

Name policies may also use `.*` suffix matching, allowing namespace-style policy such as `org.example.*` without treating unrelated prefixes such as `org.examplemalicious` as matches.

## Fine-grained call and broadcast rules

Beyond SEE/TALK/OWN, the proxy supports `--call` and `--broadcast` rules. These can narrow access by:

- well-known bus name;
- D-Bus interface;
- specific interface member / method / signal;
- exact object path;
- object-path subtree.

The documented rule form is roughly:

`[METHOD][@PATH]`

where the method component can be wildcarded or narrowed to an interface/member and the path can be exact or subtree-style.

This is the major reason xdg-dbus-proxy is more useful than simply exposing or withholding the user's whole session bus. A sandbox can receive a mediated bus socket that exposes only the services and operations the application requires.

## Important security semantics and limitations

### Sticky unique-name policy

Policy is configured against well-known names but also affects the unique ID of the peer that owns those names. Upstream explicitly documents a race-related compromise: once a unique ID has gained policy because it owned an allowed name, the highest policy can remain "sticky" after the well-known name is released.

This should be treated as part of the threat model, not an implementation detail to ignore.

### Host peers are not all re-filtered symmetrically

The source documents that peers on the real bus are treated as privileged with respect to messages sent toward the proxied client, apart from broadcast filtering. If an untrusted peer can independently connect directly to the same host bus without a corresponding mediation boundary, xdg-dbus-proxy does not magically make the entire bus mutually isolated.

The intended deployment model therefore relies on untrusted clients being consistently placed behind appropriate proxies/policy boundaries.

### D-Bus filtering is not a complete sandbox

The component does not provide filesystem isolation, process isolation, network isolation, device mediation, resource limits or generic syscall filtering. It is one IPC boundary. A real application sandbox normally composes it with namespace/cgroup/seccomp/filesystem policy and portal-style capability mediation.

## 2026 broadcast-filter bypass fix

Release **0.1.8**, published **2026-08-11**, fixes an important filtering problem: broadcast messages could bypass object-path/interface/member checks.

The upstream commit history explains the failure mode. A prior behavior allowed the presence of a TALK-level rule to skip the detailed broadcast filter path. As a result, adding a supposedly narrow `--broadcast` rule could allow receiving broadcasts outside the requested path/interface/member restrictions.

Upstream explicitly described this as weakening the sandbox because a malicious or compromised sandboxed application could receive host-side broadcasts that were not intended to be visible, including traffic on the session bus or AT-SPI bus.

The fix reverted that bypass behavior and the project added regression coverage. A follow-up test commit states that its outside-sandbox message tests assert the fix for **GHSA-r7hp-698j-2h6c**.

This is strong maintenance evidence because the release did not merely patch code: it also expanded tests for name ownership, outgoing calls and incoming message reception.

## Testing evidence

`tests/test-proxy.c` is an integration-oriented harness rather than only a unit-test collection. It models multiple peers with policy identities such as:

- cannot access;
- can see;
- can talk;
- can own;
- can call anything;
- can call only selected operations;
- can receive any allowed broadcasts;
- can receive only selected broadcasts.

The fixture launches and connects to a D-Bus daemon and tracks received method calls, unicast signals and broadcasts on real `GDBusConnection` objects.

The current 0.1.8 release specifically records new or improved tests for:

- owning names;
- issuing method calls;
- receiving messages;
- broadcast filtering behavior related to the 2026 bypass fix.

## CI / working evidence

The current GitHub Actions workflow has three meaningful validation paths.

### GCC / Meson path

- installs D-Bus, GLib development packages and Meson;
- configures with Meson;
- builds with Ninja;
- runs the Meson test suite;
- performs an install check;
- performs `meson dist` / dist testing;
- unpacks the generated distribution and verifies xdg-dbus-proxy can be consumed as a Meson subproject;
- verifies the prefixed embedded executable is installed.

### Clang / analysis path

- builds with Clang;
- enables AddressSanitizer and UndefinedBehaviorSanitizer;
- runs CodeQL analysis;
- runs the Meson test suite.

### Valgrind path

- waits for the normal Meson job to succeed;
- builds with fortification flags;
- executes the tests under the project's Valgrind-enabled test configuration.

This is strong evidence that the project is treated as a security-sensitive native component rather than a lightly tested utility.

## CI supply-chain caveat

The inspected workflow uses several GitHub Actions by mutable major/version tags, including an old `actions/checkout@v1`, CodeQL `@v3` and `actions/upload-artifact@v4` rather than immutable commit SHAs.

This does not make the project unsafe, but it is weaker workflow supply-chain pinning than several other GitHub Gold candidates inspected in this repository. It should be recorded rather than silently granting perfect build-provenance marks.

## Release evidence

Latest inspected stable GitHub release:

- **0.1.8**
- published **2026-08-11**
- source archive: `xdg-dbus-proxy-0.1.8.tar.xz`
- upstream release metadata publishes SHA-256 digest `b6630bd24f8161b0e2546d2acbb014a3b3249f5c0d75f2a863ade898b9034d3d`

GitHub also exposes the same SHA-256 value in the release asset metadata.

GitHub Gold did **not** independently download and hash the archive in this pass, so the digest is recorded as upstream/GitHub release evidence rather than an independent verification result.

## License and reuse boundary

Current implementation headers state **GNU Lesser General Public License version 2.1 or, at the user's option, any later version**.

No source from xdg-dbus-proxy was copied into GitHub Gold.

If source is later incorporated into another project rather than merely executed as a separate system component, the LGPL obligations and any linked/modified-work implications must be evaluated for that exact reuse model. Attribution and license notices must be preserved.

## Useful components / patterns to study

### 1. Policy lookup and unique-name ownership tracking

The mapping between well-known names, unique D-Bus IDs and cumulative policy is a compact example of translating user-friendly service policy into runtime peer authorization.

### 2. Outstanding-call / reply correlation

The proxy's rule that replies are accepted for outstanding calls and not as arbitrary unsolicited traffic is a useful message-oriented authorization design pattern.

### 3. D-Bus visibility rewriting

Filtering `ListNames`, `ListActivatableNames`, `GetNameOwner`, `NameHasOwner`, `NameOwnerChanged` and related metadata surfaces shows that **metadata visibility itself is part of an IPC security boundary**.

### 4. Path/interface/member filters

The call/broadcast rule machinery is the highest-value component for future source-level study because the 2026 security issue demonstrates how subtle interactions between coarse TALK policy and fine filters can create bypasses.

### 5. Real-bus test fixture

`tests/test-proxy.c` is a useful pattern for security regression testing: stand up a real protocol service, create peers inside/outside the intended boundary, and assert both allowed traffic and forbidden traffic.

### 6. Meson subproject integration

The project intentionally supports being embedded as a Meson subproject and requires executable prefixing when embedded, reducing naming collisions.

## Platforms and runtime assumptions

The project is primarily a Unix/Linux desktop component:

- Unix-domain sockets are central to its deployment model;
- GLib/GIO are required;
- D-Bus is the mediated protocol;
- the dominant ecosystem is Flatpak/Linux desktop sandboxing.

It should not be cataloged as a cross-platform generic IPC firewall.

## Verification performed by GitHub Gold

This research pass inspected current upstream:

- repository metadata and structure;
- README;
- current manual / CLI and policy documentation;
- main proxy implementation documentation and license header;
- Meson build/dependency definition;
- test-tree structure and portions of the live D-Bus test fixture;
- CI workflow;
- NEWS / changelog;
- stable release metadata;
- recent commits explaining the 2026 broadcast-filter fix and regression tests.

## Not independently verified

GitHub Gold did **not**:

- build xdg-dbus-proxy;
- run Meson tests;
- run CodeQL, ASan, UBSan or Valgrind;
- start a D-Bus daemon or proxy instance;
- reproduce GHSA-r7hp-698j-2h6c;
- validate every SEE/TALK/OWN combination;
- fuzz D-Bus authentication/message parsing;
- test malformed GVariant/D-Bus frames;
- verify race behavior around name release/reacquisition;
- test Flatpak integration;
- perform a security audit;
- independently download/hash the 0.1.8 release archive.

All such claims remain outside the verification boundary.

## Caveats / risks

- IPC mediation is only one layer of a complete sandbox.
- Incorrectly broad `--talk`, `--own`, `--call` or `--broadcast` rules can defeat least privilege.
- The sticky unique-name policy behavior is an explicit approximation needed for race-free proxying and must be considered in high-assurance policy design.
- D-Bus is stateful; policy correctness depends on names, ownership changes, outstanding calls, broadcasts and bus metadata rather than simple packet filtering.
- The 2026 bypass demonstrates that interaction between coarse and fine-grained rules deserves adversarial regression coverage.
- Mutable GitHub Action tags are a supply-chain hardening opportunity.

## Related projects / recursive ecosystem

- `flatpak/flatpak` — primary production policy caller and sandbox orchestration layer.
- `containers/bubblewrap` — namespace/filesystem/process sandbox mechanism commonly paired with higher-level Flatpak policy.
- `flatpak/xdg-desktop-portal` ecosystem — capability-mediated desktop interfaces that reduce the need to expose unrestricted host services.
- D-Bus daemon/broker implementations — upstream protocol and bus behavior that the proxy must correctly mediate.

## Strongest next research leads

1. trace the exact `any_filter_matches()` and message-classification paths for calls vs broadcasts;
2. map the 0.1.8 security fix line-by-line and identify the invariant the regression test now protects;
3. inspect name-owner policy promotion and the sticky unique-ID behavior during release/reacquisition races;
4. inspect serial rewriting and reply correlation, especially the 0.1.6 non-monotonic serial handling changes;
5. inspect D-Bus authentication forwarding and Unix FD passing boundaries;
6. compare Flatpak's generated xdg-dbus-proxy arguments with app permission manifests to show how high-level permission declarations become low-level IPC policy;
7. inspect `xdg-desktop-portal` as the complementary capability broker rather than another raw bus-access mechanism;
8. assess whether CI should pin third-party Actions to immutable commit SHAs.

## Verdict

**VERIFIED — provisional S / 27.**

xdg-dbus-proxy is genuine GitHub Gold because it is a focused, reusable, security-relevant component with a clear threat boundary, a compact codebase, real integration tests, sanitizer/Valgrind/CodeQL coverage, Meson embedding support and current security maintenance. Its strongest value is architectural: it demonstrates how a sandbox can expose a stateful desktop IPC bus without granting the sandboxed process the full authority and metadata visibility of the host session bus.
