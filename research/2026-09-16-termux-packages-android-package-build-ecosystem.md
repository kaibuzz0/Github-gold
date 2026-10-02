# termux/termux-packages — Android package build ecosystem

- Repository: https://github.com/termux/termux-packages
- Author/organization: Termux
- Category: Android / Termux / package build infrastructure / portability
- Evidence level: VERIFIED
- Provisional Gold score: 28/30 (S)
  - Utility: 5/5
  - Working Evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- Discovery: recursive follow-up from the Termux:API / termux-api-package ecosystem

## What it is

`termux/termux-packages` is the build-definition and infrastructure repository used to adapt a large Unix/Linux software ecosystem for the Termux Android environment. The upstream README describes it as scripts and patches for building packages for the Termux Android application.

This is more valuable than a package-name list. It is a large portability knowledge base: package recipes, Android-specific patches, build-system workarounds, architecture handling, repository metadata, build tooling, linting, CI, Docker-based reproducible build infrastructure, and package-update automation.

## Why it matters

For GitHub Gold, the strongest reusable asset is the accumulated Android/Linux portability knowledge encoded across package recipes and patches. When conventional Linux software assumes glibc, desktop filesystem layouts, unavailable syscalls, systemd, GNU userland behavior, or host build conventions, Termux package work often documents the concrete changes needed to make the project function in Android's userspace.

The repository is therefore useful both operationally and as a research index for answering questions such as:

- Which upstream tools have already been made to work under Termux?
- What Android/Bionic incompatibilities were encountered?
- Which patches are generic enough to upstream or reuse elsewhere?
- Which projects can operate on a phone without a traditional Linux distribution?
- Which package recipes expose useful low-resource, offline, field, development, networking, scientific, or automation tools?

## Working evidence inspected

The package CI is substantial rather than cosmetic. The current `Packages` workflow reacts to package-tree changes, determines affected packages, lints changed package recipes, and builds them in a matrix covering `aarch64`, `arm`, `i686`, and `x86_64` on Ubuntu runners. It uses the repository's Docker/build tooling, generates package artifacts, and computes SHA-256 checksums for resulting `.deb` files.

The workflow also contains engineering for large-package disk pressure, zram, reusable prior PR artifacts, changed-package detection, subpackages, deleted packages, manual rebuild selection, and Docker-image regeneration when build-environment files change.

This provides strong upstream evidence that package definitions are continuously exercised rather than merely archived as recipes.

## Maintenance signals

Maintenance is extremely active. On 2026-09-16 alone, recent commits inspected included an upstream-feedback change for `mandoc` and automated version bumps for Nextcloud Client, Sonarr, Ruff, and Prowlarr. The cadence indicates a continuously maintained package ecosystem with automated update support.

## Licensing

Licensing is intentionally heterogeneous:

- build infrastructure outside the package trees is Apache-2.0;
- scripts and patches associated with individual packages are licensed under the same license as the corresponding upstream package.

Therefore GitHub Gold must not treat the entire repository as Apache-2.0 when extracting package-specific patches. License review must happen at the package/upstream level before copying or adapting anything.

No upstream code, patches, recipes, binaries, or package artifacts were copied into GitHub Gold in this research pass.

## Valuable components / research surfaces

- `packages/` — main package recipes and Android portability patches
- `x11-packages/` — graphical/X11-oriented packages
- `root-packages/` — packages requiring/root-oriented functionality
- `disabled-packages/` — useful record of software that is currently blocked or unsuitable, often a source of portability leads
- `scripts/` — package builder, linting, Docker/build-environment, automation and repository tooling
- `.github/workflows/packages.yml` — changed-package CI/build matrix and artifact pipeline
- package `build.sh` files — compact machine-readable-ish build knowledge
- package patch sets — Android/Bionic portability knowledge requiring per-package license review

## Verification boundary

GitHub Gold inspected upstream README, licensing policy, current package CI, and recent commit activity. GitHub Gold did **not** clone the repository locally, execute package builds, install generated packages on Android, verify every package recipe, reproduce architecture builds, validate package signatures/repositories, or independently audit individual upstream patches.

`VERIFIED` therefore means the repository's purpose, structure, active maintenance, and substantial upstream build-validation infrastructure were verified from primary repository evidence. It does not mean every package was independently tested by GitHub Gold.

## Caveats

- Package behavior depends on Android version, Termux environment, architecture, device/OEM constraints, and upstream changes.
- A successful package build is not equivalent to exhaustive runtime validation on real Android hardware.
- Package-specific licensing varies with upstream software.
- Some patches may be historical compatibility work rather than generally reusable solutions.
- `root-packages` and some networking/system packages can require privileges or capabilities unavailable on ordinary devices.

## Recursive research leads

1. Mine package patches for recurring Bionic-vs-glibc and Android filesystem/process compatibility patterns.
2. Identify unusually useful low-resource/offline packages that deserve standalone Gold entries.
3. Audit `disabled-packages` for high-value projects blocked by one or two solvable portability issues.
4. Inspect `scripts/build-package.sh`, Docker infrastructure, dependency resolution and package-lint architecture as reusable build-system components.
5. Map packages suitable for emergency communications, offline mapping, SDR, scientific work, local AI, development, archival work and field automation.
6. Compare official Termux recipes with Termux User Repository (TUR) for complementary high-value software while keeping trust/provenance levels distinct.
7. Track Android 15/16 compatibility changes and patches that may reveal reusable mobile-Linux portability techniques.
