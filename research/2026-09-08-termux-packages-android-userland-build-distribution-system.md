# termux/termux-packages — Android userland build and distribution system

- **Repository:** https://github.com/termux/termux-packages
- **Author / organization:** Termux
- **Category:** Android / Termux / package build system / cross-compilation / software distribution / developer tooling
- **Evidence level:** VERIFIED
- **Provisional Gold score:** **28/30 — S tier**
- **License:** **Apache-2.0 for build infrastructure outside package trees; package recipes/patches inherit each upstream package's license**
- **Discovery source:** recursive follow-up from `termux/termux-app`; GitHub-first, with no YouTube-derived technical claim used in this pass

## Executive finding

`termux/termux-packages` is the build-and-distribution substrate that turns conventional Unix/Linux software into installable Android packages for Termux. It contains the package recipes, Android-specific patches, cross-build helpers, repository metadata, bootstrap generation, CI orchestration, release automation and publishing logic behind the Termux userland.

The project is more valuable than a package list. It is a large, living compatibility layer showing how software that normally assumes glibc/Linux filesystem conventions, desktop-oriented build systems or conventional distributions can be adapted to Android's Bionic libc, filesystem layout, linker behavior and app sandbox.

## Provisional 30-point Gold score

| Dimension | Score | Rationale |
|---|---:|---|
| Utility | 5/5 | Provides the package ecosystem that makes Termux a practical Android Linux-style environment and is directly useful for porting software to Android. |
| Working Evidence | 5/5 | CI lints and cross-builds changed packages for aarch64, arm, i686 and x86_64, generates checksums, validates package-index collisions, publishes repositories and creates recurring bootstrap releases. |
| Reusability | 5/5 | Build helpers, Dockerized builder, package recipes, patch patterns, bootstrap generator and CI/publishing scripts are highly reusable as references for Android ports. |
| Novelty | 4/5 | Package building is established technology, but the breadth of Android-specific adaptation and reproducible multi-architecture orchestration is unusually valuable. |
| Documentation | 4/5 | README, contributing guidance, wiki and script conventions are substantial; knowledge is distributed across recipes/scripts/wiki rather than one complete architectural document. |
| Maintenance | 5/5 | Active on 2026-09-08 with package updates and build-system maintenance; automated update workflows and weekly bootstrap releases provide strong current-maintenance evidence. |
| **Total** | **28/30** | **Provisional S** |

## What the repository provides

### Package recipes and Android compatibility patches

The repository explicitly contains scripts and patches used to build packages for the Termux Android application. Package trees include the main repository plus root and X11 package sets. Individual recipes encode upstream source locations, versions, checksums, dependencies, configure/build flags and Android-specific patches.

This makes the repository a high-value porting corpus: when a conventional Linux project fails on Android, existing Termux recipes often show the exact compatibility changes needed for Bionic, Android's linker, filesystem paths, unavailable syscalls, cross-compilation, GUI/X11 integration or mobile constraints.

### Cross-architecture package CI

The current `Packages` workflow uses a four-architecture matrix:

- `aarch64`
- `arm`
- `i686`
- `x86_64`

For changed package recipes it determines the affected packages, rejects merge commits in PR history, lints recipes and builds packages through the repository's Dockerized build environment using `build-package.sh`.

The workflow does not merely compile one representative target. It executes the package-build path separately for all four supported architectures and preserves per-architecture build artifacts.

### Package artifact checksums

After builds, CI computes SHA-256 sums for generated `.deb` packages and uploads the checksum manifests as build artifacts. This is strong integrity metadata for CI outputs, though it is not equivalent to independently verified reproducible-build attestations.

### Repository collision check before publication

For non-master branches, CI downloads the published `Packages.bz2` indexes for each architecture and checks whether newly built package filenames collide with files already present on the server. If duplicates are found, the workflow fails and requires a revision bump, rebase or explicit no-build handling.

This is a useful package-distribution correctness pattern because it prevents silent filename reuse against the current repository state.

### Publishing pipeline

On master, the workflow downloads built package artifacts and uses the repository's Aptly API helpers to upload package files, add them to the repository and publish repository changes. It also publishes a staging distribution.

The publishing job is guarded by repository/ref checks and receives the Aptly authentication and GPG passphrase through GitHub secrets.

### Bootstrap generation

A dedicated workflow generates Termux bootstrap archives weekly and on manual dispatch for all four architectures. It executes `scripts/generate-bootstraps.sh`, uploads the generated ZIPs, then creates a dated GitHub release and publishes the four architecture-specific archives.

The newest inspected bootstrap release is **`bootstrap-2026.09.06-r1+apt.android-7`**, published **2026-09-06**. GitHub exposes SHA-256 digest metadata for the inspected aarch64, arm, i686 and x86_64 ZIP assets.

This is operationally important because those archives seed a new Termux installation's initial userland.

### Automated package maintenance

Recent history on **2026-09-08** includes multiple automated package-version bumps plus manual build-infrastructure cleanup. The repository also has dedicated workflows for package updates, repository-health checks, CodeQL, Go/Zig validation, Docker image generation and bootstrap generation.

The update volume is not itself proof that every package works perfectly, but it is strong evidence of an actively maintained package ecosystem rather than a static port archive.

## High-value reusable components and patterns

### `build-package.sh`

The central build entry point is a high-value reference for orchestrating Termux package builds and cross-compilation. It should be inspected further as its own architecture component rather than copied blindly.

### `scripts/run-docker.sh` and builder image

The hosted CI uses a containerized build environment, reducing host drift and providing a reproducible development/build substrate. The Docker image and setup scripts are strong candidates for deeper supply-chain inspection.

### Package recipe corpus

The per-package `build.sh` and patch sets are arguably the repository's largest practical treasure trove. They encode years of Android porting knowledge across compilers, shells, networking tools, databases, languages, media stacks, editors and developer utilities.

Because recipe licensing follows each upstream package, these files cannot be treated as uniformly Apache-2.0.

### Bootstrap generator

`scripts/generate-bootstraps.sh` is a reusable packaging pattern for turning a package repository into architecture-specific first-run root/userland archives.

### Aptly publishing helpers

`scripts/aptly_api.sh` and associated workflow logic implement repository upload, add and publish operations and are useful references for automated APT repository delivery.

## Licensing boundary

The repository's root licensing document deliberately uses a split model:

- build infrastructure **outside** `packages/`, `x11-packages/`, `root-packages/` and `disabled-packages/` is **Apache-2.0**;
- scripts and patches inside package directories use the **same license as the corresponding upstream package**.

This is a critical GitHub Gold caveat. There is no single license that authorizes copying arbitrary package recipes or patches. Exact package and upstream licensing must be checked before reuse.

No package recipe, patch, source archive, `.deb`, bootstrap ZIP or other third-party code/artifact was copied into GitHub Gold in this pass.

## Security and supply-chain caveats

- The inspected workflows use mutable major-version Action references such as `actions/checkout@v7`, `actions/upload-artifact@v6` and `actions/download-artifact@v7` rather than immutable commit-SHA pins.
- Package builds consume many third-party upstream sources; recipe source URLs and hashes form a broad software-supply-chain boundary that deserves dedicated automated audit.
- A successful cross-build does not prove runtime correctness on physical Android devices.
- Package-specific patches may alter security assumptions made by upstream software and need exact-project review.
- Repository publication relies on privileged Aptly/GPG credentials in GitHub Actions; workflow permission and secret-handling changes deserve close monitoring.
- Bootstrap archives are especially sensitive because they become the initial executable userland for new installations.

## Verification performed in this pass

Performed:

- inspected current repository metadata and default branch;
- inspected the upstream README and project role;
- inspected root licensing rules;
- inspected workflow inventory;
- inspected the package build workflow, architecture matrix, lint/build/checksum, collision-check and publication logic;
- inspected bootstrap-generation workflow;
- inspected current releases and GitHub-provided digest metadata for the newest bootstrap archives;
- inspected recent commit activity through 2026-09-08;
- checked the active GitHub Gold PR/candidate inventory to avoid a duplicate entry.

Not performed:

- cloning `termux-packages`;
- executing a package build;
- building the package-builder Docker image;
- running package lint or build-order tests;
- installing generated `.deb` files on Android;
- comparing outputs for bit-for-bit reproducibility;
- independently hashing bootstrap ZIPs or `.deb` artifacts;
- validating repository GPG signatures;
- auditing every package recipe's source URL/checksum/license;
- testing the Aptly publication path;
- reproducing package runtime behavior on aarch64/arm/i686/x86_64 devices;
- fuzzing package metadata, bootstrap extraction or installer paths.

## Strong recursive research leads

1. **`build-package.sh` architecture** — environment setup, dependency graph, source verification, patch application and cross-compile phases.
2. **Source-integrity enforcement** — how `TERMUX_PKG_SHA256`, alternate mirrors, git sources and generated artifacts are validated.
3. **Package-builder container** — base image provenance, toolchain pinning and reproducibility.
4. **Bootstrap trust chain** — package selection → archive generation → GitHub release → `termux-app` first-run installation.
5. **APT repository signing** — GPG key management, metadata signing and client verification.
6. **`scripts/buildorder.py`** — dependency ordering and graph semantics; CI already runs randomized build-order testing.
7. **Automated package updater** — how upstream versions are discovered and whether source-integrity metadata is refreshed safely.
8. **Representative difficult ports** — inspect projects with substantial Bionic/syscall/linker patches to extract reusable Android-porting patterns.
9. **X11 packages** — graphical Linux software adaptation to Android/Termux:X11.
10. **Reproducible-build measurement** — independently rebuild selected packages across clean environments and compare artifacts.

## Verdict

**VERIFIED / provisional S / 28.**

`termux/termux-packages` is one of the strongest Android-specific technical corpora for GitHub Gold because it combines a live multi-architecture package ecosystem, a large reusable body of Android porting knowledge, CI-backed cross-build evidence, repository publication and first-run bootstrap generation. Its principal caveat is licensing and provenance granularity: package scripts/patches inherit upstream licenses, and the huge third-party source surface requires per-package verification rather than blanket trust.