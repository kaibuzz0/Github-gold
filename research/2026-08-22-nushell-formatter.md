# Nushell Formatter and Parser-Tooling Research — 2026-08-22

## Executive verdict

### nufmt

- **Repository:** https://github.com/nushell/nufmt
- **Author / Org:** Nushell Project
- **Category:** developer tooling / formatter / Rust library / Nushell ecosystem
- **Evidence:** VERIFIED
- **Provisional tier / score:** **S / 27**
- **License:** MIT
- **Promotion status:** READY in research dossier; machine-readable queue append intentionally deferred until the large JSON can be updated losslessly.

### tree-sitter-nu

- **Repository:** https://github.com/nushell/tree-sitter-nu
- **Evidence:** LEAD
- **Promotion status:** DEFER
- **Reason:** upstream README still explicitly labels the grammar **WIP**. It remains a useful editor/parser lead but does not currently meet the same confidence bar as nufmt.

## Why nufmt qualifies

nufmt is not merely a cosmetic command-line wrapper. It is built on Nushell's own `nu-parser` and `nu-protocol` parsing infrastructure and exposes both a command-line binary and a reusable Rust library (`nu_formatter`). That makes it a useful reference for syntax-aware source transformation, AST traversal, formatter idempotency, comment preservation, structured configuration, and editor/CI integration.

Upstream documentation describes:

- AST-based formatting using Nushell's actual parser
- idempotent output expectations
- preservation of comments
- NUON-based formatter configuration
- parallel file processing with Rayon
- stdin/stdout operation for editor and pipeline integration
- dry-run exit semantics suitable for CI
- directory and multi-file formatting
- broad construct coverage across control flow, pipelines, data structures, modules, strings, ranges, closures, aliases, externs, and error handling

The current manifest identifies `nufmt` version **0.1.4**, Rust edition 2021, MIT licensing, a `nu_formatter` library target, a separate CLI binary, Nushell 0.114.1 parser/protocol dependencies, and a Criterion benchmark target.

## Verification evidence inspected

GitHub Gold inspected upstream repository metadata, README, LICENSE, Cargo manifest, and recent commit history.

Important maintenance evidence includes:

- **2026-08-12:** batch issue-fix commit closing multiple formatter issues.
- **2026-07-23:** fix preserving comments at the end of multiline pipelines.
- **2026-07-20:** exclusive stepped-range formatting correctness fix.
- **2026-07-08:** fixes for comment loss/misplacement in match arms, nested records, and raw strings; upstream commit states the full suite was green with **273 tests** and seven new fixtures.
- **2026-07-05:** quote/comment scanning correctness fix.
- **2026-05-24:** inline-comment preservation improvements and configurable tabs/spaces.

These are substantive formatter-correctness changes, not merely dependency churn.

## Testing architecture worth studying

Upstream documents a ground-truth system with intentionally poorly formatted valid input fixtures paired with expected formatted output. It also documents explicit idempotency testing and category-based test execution.

Useful ideas/components:

- source-to-AST formatting pipeline
- comment extraction and comment-position preservation
- AST pretty-printing decisions
- idempotency assertions
- ground-truth input/expected fixture design
- syntax-category test organization
- parse-error handling before mutation
- CI-friendly dry-run behavior
- stdin formatter integration
- directory traversal and exclusion rules
- Rayon parallel file processing
- NUON configuration parsing
- reusable library / CLI separation

## Reuse targets

1. **`nu_formatter` library boundary** — embedding formatter behavior without invoking the CLI.
2. **AST traversal / emission logic** — reference architecture for syntax-aware source rewriting.
3. **Comment-preservation machinery** — especially interesting because recent upstream bugs demonstrate the hard edge cases.
4. **Ground-truth + idempotency tests** — broadly reusable testing pattern for any source formatter or serializer.
5. **Dry-run exit contract** — useful pattern for CI and pre-commit tooling.
6. **Config handling** — NUON-based typed configuration and exclusion rules.
7. **Parallel formatting orchestration** — Rayon-backed multi-file execution.

## License and copying boundary

The root repository is MIT licensed. Any copied or adapted source must retain the required copyright and permission notice. Nushell dependencies and other third-party crates remain separately licensed and should be checked independently when extracting components.

No third-party source code was copied into GitHub Gold during this pass.

## Verification boundary

GitHub Gold **did not independently build, install, benchmark, fuzz, run the test suite, or editor-integration test nufmt** during this research pass. Claims about 273 passing tests, performance, and formatter behavior are upstream evidence unless explicitly stated otherwise.

## tree-sitter-nu disposition

`nushell/tree-sitter-nu` is MIT licensed and has plausible long-term value for editor parsing, syntax highlighting, and Tree-sitter integrations. However, its upstream README still starts with `[WIP]` and presents major goals as brainstorming items. It should remain a **LEAD**, not be promoted simply because it belongs to a strong ecosystem.

Promotion trigger for tree-sitter-nu:

- WIP designation removed or significantly narrowed
- documented parser coverage/maturity
- evidence of maintained editor integrations and regression tests
- clearer compatibility expectations against current Nushell syntax

## Recursive leads

- inspect `nufmt`'s formatter/comment modules at file/function level
- inspect its benchmark harness and ground-truth fixtures
- inspect Nushell's `nu-parser` public boundaries used by nufmt
- revisit `tree-sitter-nu` when grammar maturity improves
- inspect editor/LSP integrations that consume either nufmt or tree-sitter-nu

## Score rationale — 27 / 30

- Utility: 4/5
- Working evidence: 5/5
- Reusability: 5/5
- Novelty: 4/5
- Documentation: 5/5
- Maintenance: 4/5

The score reflects strong testing/documentation and reusable architecture while avoiding a perfect maintenance/utility score for a young, language-specific formatter.