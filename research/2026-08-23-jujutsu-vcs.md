# Jujutsu (jj) — version-control architecture research

## Candidate verdict

- **Repository:** https://github.com/jj-vcs/jj
- **Author / org:** jj-vcs
- **Category:** developer tooling / version control / Git interoperability
- **Evidence:** VERIFIED
- **Provisional Gold tier / score:** S / 28
- **License:** Apache-2.0
- **Promotion status:** promotion-ready research dossier; do not force into the large candidate JSON unless the file can be updated losslessly

## What it is

Jujutsu is a version-control system whose current production storage backend is Git. Upstream deliberately separates its user-facing/version-control algorithms from the physical storage backend, allowing the system to use Git repositories for commit/file storage while maintaining higher-level metadata separately.

The project is notable because it redesigns several familiar VCS concepts instead of merely wrapping Git commands.

## Why it is GitHub Gold

Jujutsu exposes several unusually reusable ideas and implementations:

1. **Working-copy-as-a-commit** — the working copy is represented as a real commit and commands automatically snapshot/update it. This removes a separate staging-index model and substantially changes how dirty working trees, stashes, and amendment flows are handled.
2. **Operation log and undo** — repository operations themselves are versioned, which enables inspection and recovery of prior repository states.
3. **First-class conflicts** — conflict state can live in commits rather than existing only as a transient failed-operation condition.
4. **Automatic descendant rebasing** — rewriting a commit automatically rebases descendants, including propagation of conflict resolution.
5. **Git-compatible storage** — the production backend uses Git repositories and supports normal Git remotes; colocated workspaces can use both `jj` and `git`.
6. **Revset and template languages** — commit selection and output formatting are programmable rather than hard-coded command behavior.
7. **Backend abstraction** — the repository model intentionally separates VCS logic from storage implementation, making the architecture interesting beyond the CLI itself.
8. **Concurrent-repository design** — upstream documents experimental work aimed at keeping repositories recoverable under concurrent replication/copy scenarios where ordinary filesystem-lock assumptions do not hold.

## Useful components / study targets

- Git storage backend and gitoxide integration
- repository/view model and operation log
- working-copy snapshot/update machinery
- revset parser/evaluator
- template language
- conflict representation and merge machinery
- automatic rebase / rewrite propagation
- transaction and operation-description layers
- Git import/export and colocated-workspace behavior
- path completion and CLI parsing
- concurrency-safe repository-state design
- test infrastructure around Git interoperability and workspace state

## Upstream evidence inspected

### README / architecture claims

The upstream README documents:

- Git as the current production-ready storage backend
- compatibility with normal Git remotes
- colocated `jj` + `git` workspaces
- working-copy-as-a-commit semantics
- operation-log/undo behavior
- first-class conflicts
- automatic rebase and conflict-resolution propagation
- revsets and templates
- storage-backend abstraction
- experimental concurrent-replication safety goals

Upstream also states plainly that Jujutsu remains an **experimental version-control system**. Git compatibility is described as stable and core developers use jj for daily development, but upstream warns that experimental features may have bugs, storage changes, UX changes, or workflow gaps.

### License

The root `LICENSE` is Apache License 2.0. Covered code reuse is therefore permissive but must retain required notices and comply with Apache-2.0 attribution/patent terms.

### Maintenance evidence

Fresh commits inspected include:

- **2026-08-23:** path completion updated to honor repeated/canonical diff revision selectors, with additional coverage for revision/range cases.
- **2026-08-21:** Git-push operation-description formatting cleanup prompted by Clippy diagnostics.
- **2026-08-19:** tests tightened so Git `HEAD` synchronization behavior is exercised in colocated workspaces where that behavior is actually relevant.

This indicates active maintenance across CLI correctness, Git interoperability, and test behavior rather than documentation-only churn.

## Verification boundary

GitHub Gold did **not** independently install Jujutsu, migrate a production Git repository, benchmark large-history performance, validate every Git-forge workflow, test concurrent replication, fuzz repository parsing, or verify recovery guarantees.

`VERIFIED` here means the repository, source/license structure, documented architecture, current maintenance signals, and explicit upstream caveats were inspected. It does not mean every experimental feature is production-safe.

## Caveats / risks

- Upstream itself labels Jujutsu experimental.
- Only the Git backend is described as production-ready today; the broader backend abstraction is architectural potential rather than proof that multiple mature backends exist.
- Higher-level metadata is not stored solely as ordinary Git refs/objects, so interoperability details matter when switching tools.
- Experimental concurrent-replication behavior should not be treated as a backup guarantee without independent testing.
- VCS correctness is high-impact: code reuse from merge/rewrite/storage paths should receive substantially more testing than ordinary utility code.

## Related ecosystem / recursive leads

- `gitoxide` / `gix` — Rust Git implementation used by Jujutsu's Git backend
- Jujutsu revset implementation
- Jujutsu template-language implementation
- merge/conflict representation
- operation-log storage model
- `jj-dojo` learning ecosystem
- editor/IDE integrations

## Promotion rationale

Provisional **S / 28** because the project combines high utility, strong documentation, active maintenance, clean licensing, real Git interoperability, and genuinely distinctive VCS architecture. One point is intentionally withheld from the top score because upstream still designates the project experimental and several advanced features retain explicit stability caveats.
