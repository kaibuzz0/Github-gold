# cmwen/syncthing-android-fork — maintained Syncthing 2 Android personal fork

- Repository: https://github.com/cmwen/syncthing-android-fork
- Author: cmwen
- Category: Android / local-first / peer-to-peer synchronization
- Evidence: PROMISING
- Provisional Gold score: 23/30 (A)
  - Utility: 4/5
  - Working Evidence: 4/5
  - Reusability: 4/5
  - Novelty: 3/5
  - Documentation: 5/5
  - Maintenance: 3/5
- License: MPL-2.0
- Discovery: recursive follow-up from the Syncthing dossier; GitHub-first verification.

## What it is

A personal continuation of the discontinued official `syncthing/syncthing-android` wrapper. The fork documents a migration to Syncthing 2.0.11, Docker/devcontainer build paths, self-signed APK automation, GitHub release automation, checksums, and migration guidance from Syncthing 1.x.

The project is explicitly described by its maintainer as a personal-use/learning fork rather than a broadly supported distribution. That limitation is important: it is technically useful and well documented, but should not be represented as the official Android successor.

## Why it matters

The official Syncthing Android wrapper was discontinued in December 2024, leaving Android users and developers with a fragmented successor landscape. This fork is useful as:

- a concrete Android wrapper updated for Syncthing 2.x;
- a build/reference implementation for embedding Syncthing on Android;
- a migration case study covering the 1.x -> 2.x compatibility boundary;
- an example of reproducible-ish Android build infrastructure using Docker/devcontainers;
- a source of Android-specific wrapper and lifecycle engineering leads.

## Evidence inspected

Repository metadata confirms the repository is public, unarchived, and uses `main` as its default branch.

Recent commit history inspected through GitHub shows a November 16, 2025 batch migrating the wrapper to Syncthing 2.0.11 and fixing build compatibility, including Go 1.25.3 selection and linker/build adjustments. This is newer than the last commit found in another unarchived Syncthing-Fork candidate (`geekwolverine/syncthing-android-fork`, January 2025).

The README documents:

- Syncthing 2.0.11 integration;
- the breaking 1.x/2.x compatibility boundary;
- LevelDB -> SQLite migration expectations;
- prebuilt APK releases and SHA-256 checksums;
- Docker and devcontainer build procedures;
- Android SDK/NDK, Java and Go build requirements;
- automated CI/release workflows;
- self-signed APK behavior and optional persistent signing configuration.

The root LICENSE is Mozilla Public License 2.0.

## Useful components / research leads

- Android wrapper architecture around the Syncthing native/core component.
- `docker/Dockerfile` and devcontainer environment as Android build reproducibility references.
- Gradle `buildNative` integration.
- GitHub Actions APK build/release/checksum pipeline.
- Syncthing 2.x migration documentation and wrapper compatibility work.
- Android background/lifecycle behavior inherited from the discontinued wrapper lineage.

## Caveats

- Maintainer explicitly says the fork is for personal use and learning and is not intended for distribution.
- Latest commit found during this run was November 16, 2025, so maintenance is not strong enough for a VERIFIED/S-tier designation in September 2026.
- Self-signed APK automation is not equivalent to an independently trusted distribution channel; persistent signatures matter for seamless upgrades.
- Syncthing 2.x is incompatible with 1.x peers according to this fork's migration documentation; mixed-version networks require careful migration.
- Fork lineage is fragmented. Several similarly named repositories exist; one candidate inspected (`nel0x/syncthing-android`) is currently archived, while another (`geekwolverine/syncthing-android-fork`) had its newest commit in January 2025.
- No upstream code or binaries were copied into GitHub Gold.

## Verification performed by GitHub Gold

Performed:

- repository metadata inspection;
- recent commit-history inspection;
- README/build/migration documentation inspection;
- root-license inspection;
- comparison against selected alternative Android forks;
- duplicate search in the current GitHub Gold default-branch index.

Not performed:

- APK build or installation;
- GitHub Actions execution/reproduction;
- checksum or signature verification;
- Android runtime/background-sync testing;
- Syncthing 1.x -> 2.x migration testing;
- synchronization interoperability testing;
- source-level security audit.

## Follow-up

1. Inspect the APK CI workflow and determine exactly what it proves versus merely automates.
2. Compare this fork against the strongest current Android successors, including F-Droid-visible lineages, using commit/release freshness and Syncthing-core version.
3. Investigate a direct Termux deployment of upstream Syncthing as a potentially simpler and more maintainable Android path.
4. Map Android background-execution, storage-access, notification, battery-optimization, and lifecycle constraints relevant to Syncthing 2.x.
5. Re-evaluate this entry if maintenance resumes or a clearly maintained successor emerges.
