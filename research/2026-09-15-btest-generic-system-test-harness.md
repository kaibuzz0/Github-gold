# zeek/btest — Generic system-test and baseline harness

- **Repository:** https://github.com/zeek/btest
- **Author/organization:** Zeek Project
- **Category:** developer tooling / system testing / regression harness
- **Evidence:** VERIFIED
- **Provisional Gold score:** 27/30 — S
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 3/5
  - Documentation 4/5
  - Maintenance 5/5
- **Discovery:** recursive follow-up from the `zeek/zeek-testing` dossier.

## What it is

`btest` is a generic shell-oriented system-test driver maintained by the Zeek Project. Although it is deeply used in Zeek's own regression infrastructure, the project is not Zeek-specific: test directives can be embedded in arbitrary text or source files, and the harness executes commands, evaluates exit status, isolates tests in per-test sandboxes, and compares generated output against maintained baselines.

Upstream currently documents Python and Bash as core requirements. The package can be installed with `pip install btest`, and the repository also supports local/source installation.

## Why it is GitHub Gold

The strongest value is composability. BTest provides a relatively small reusable harness for projects that need executable system/integration tests without adopting a large language-specific testing stack. A test file can simultaneously be source/input and carry `@TEST-*` directives in comments, making the harness adaptable to shell programs, interpreters, network analyzers, compilers, generated output, command-line tools, and mixed-language projects.

Its baseline model is particularly useful for complex tools whose correctness is best expressed as stable output rather than individual assertions.

## Useful components and capabilities

- `btest` — main test-suite driver.
- `btest-diff` — compares produced output against stored baselines.
- baseline update mode (`-U`) and interactive baseline updating.
- canonifiers — normalization hooks for unstable output such as paths/timestamps.
- per-test sandbox directories.
- parallel execution via worker jobs.
- serialization sets for tests that cannot safely run concurrently.
- rerun-only-failures mode.
- test groups and alternatives/configuration variants.
- JUnit XML output for CI integration.
- diagnostics and retained temporary-state modes.
- timing baselines and Chrome trace-format execution timing.
- documentation generation from test metadata.
- background-run/wait helper scripts.
- Sphinx helpers for incorporating test results/examples into documentation.

These are reusable testing primitives rather than Zeek-specific protocol logic.

## Working evidence

The repository's GitHub Actions workflow runs `make test` across macOS, Ubuntu, and Windows for Python 3.10, 3.11, 3.12, 3.13, and 3.14. A second installation/package job installs the project and executes its test suite using the installed `btest`, then builds source and wheel distributions.

Tagged builds are gated on those test jobs before the source distribution is uploaded to PyPI. This provides stronger evidence than README claims alone that the project is exercised cross-platform and as an installed package.

The project metadata classifies BTest as Production/Stable and currently requires Python >=3.10. Windows additionally needs a Bash implementation such as Git Bash, MSYS2, Cygwin, or WSL with `bash.exe` available.

## Maintenance evidence

Maintenance is current through September 15, 2026. Recent work refactored the test-dispatch machinery from the old sentinel protocol toward a generator-based worker loop, reduced repeated timing-file I/O, cleaned naming after the concurrency implementation moved to asyncio workers, and simplified failure/queue handling. This is substantive internal maintenance rather than cosmetic repository activity.

The repository does not currently publish GitHub Releases through the GitHub Releases API; distribution is instead tied to tagged CI/PyPI packaging. Absence of GitHub Release objects should therefore not be interpreted as absence of maintained packaging.

## License

The repository carries a permissive BSD-style three-clause license. Redistribution requires preserving the copyright/license terms, and upstream notes that individual files can carry their own notices.

No BTest source was copied into GitHub Gold.

## Verification performed

Inspected repository metadata, README/user documentation, package metadata, license, current CI workflow, recent commit history, and its relationship to the existing `zeek/zeek-testing` dossier. Checked the current GitHub Gold catalog/default-branch search and active research branch context to avoid adding an obvious duplicate.

## Not independently verified

GitHub Gold did **not** install BTest, execute `make test`, run example tests, publish/install a wheel, reproduce baseline behavior, test parallel/serialization semantics, benchmark large suites, or independently validate the PyPI artifacts.

`VERIFIED` therefore means concrete upstream implementation/testing evidence was inspected; it does not mean this research run independently executed the project.

## Caveats

- Bash remains a runtime dependency, including on Windows.
- Baseline-heavy testing can encode intended behavior very effectively, but poorly reviewed baseline updates can also bless regressions; projects adopting this pattern need disciplined review around `-U` changes.
- The framework is intentionally shell/system-test oriented and is not a replacement for fine-grained language-native unit testing.
- Per-file licensing notices should be checked before copying individual helper scripts.

## Related projects

- `zeek/zeek-testing` — major real-world BTest regression corpus already cataloged in GitHub Gold.
- `zeek/zeek` — prominent upstream consumer.
- `OISF/suricata-verify` — useful comparison point for descriptor/assertion-driven network regression testing.

## Follow-up leads

1. Inspect the BTest directive parser and execution/sandbox architecture for reusable design patterns.
2. Study canonifier design as a general solution for deterministic golden-file testing.
3. Evaluate concurrency/serialization correctness after the asyncio worker refactor.
4. Map how Zeek composes BTest with external packet corpora and leak checks.
5. Compare BTest against pytest golden-file plugins, LLVM lit/FileCheck, CTest, and Suricata Verify.
6. Inspect release/tag/PyPI provenance and whether packaging could adopt stronger artifact attestations.
7. Identify other substantial open-source projects using BTest outside Zeek's core repositories.
