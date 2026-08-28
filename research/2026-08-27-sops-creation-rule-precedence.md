# SOPS creation-rule precedence and config lookup

Date: 2026-08-27
Project: getsops/sops
Repository: https://github.com/getsops/sops
Evidence level: VERIFIED
Provisional Gold score: S / 28
Scope: `.sops.yaml` discovery, creation-rule matching, precedence, path semantics, and configuration edge cases

## Executive finding

SOPS configuration is intentionally simple but order-sensitive. Current source and official documentation show two separate first-match decisions:

1. SOPS searches the current working directory and then parent directories for a file named exactly `.sops.yaml`, using the first one it finds.
2. Inside that configuration, SOPS scans `creation_rules` in list order and uses the first rule whose `path_regex` matches. A rule with no `path_regex` matches every file and therefore acts as a catch-all at the point where it appears.

This means `.sops.yaml` should be treated as an ordered policy file, not as a collection of mergeable selectors. A broad rule placed before a narrow rule can shadow the narrow rule completely.

## Evidence inspected

Primary evidence:

- `config/config.go` on `getsops/sops` main
- official SOPS reference documentation, including the current config-file specification
- official advanced-usage documentation for `--filename-override`
- current upstream issue #2237 concerning Windows path separator behavior in creation-rule matching

GitHub Gold did not independently build or execute SOPS for this pass. Behavioral statements below are limited to inspected source, current official documentation, and clearly labeled upstream issue evidence.

## Config-file discovery

The official reference states that the config file must be named `.sops.yaml`, not `.sops.yml`. SOPS searches the current working directory and its parents and uses the first `.sops.yaml` it finds.

Current `LookupConfigFile` source implements an upward walk with a maximum depth of 100. It checks `.sops.yaml` first at each level. If it encounters `.sops.yml`, it records that alternate name only to emit a warning; it does not treat `.sops.yml` as the active config.

### Architectural consequence

Nested repositories or subdirectories can intentionally override a parent policy by placing a nearer `.sops.yaml`. Parent and child config files are not merged by this lookup path. The nearest valid config wins.

A caller can bypass discovery by explicitly selecting a config through SOPS's `--config` option or `SOPS_CONFIG` environment variable, as documented upstream.

## Creation-rule precedence

Current `parseCreationRuleForFile` source iterates `conf.CreationRules` in order.

For each rule:

- if `PathRegex` is empty, that rule is selected immediately;
- otherwise SOPS compiles the regular expression;
- if compilation fails, loading fails with a regex compilation error;
- if the regex matches the candidate file path, that rule is selected immediately;
- evaluation stops after the first selection.

If no rule is selected, SOPS returns `error loading config: no matching creation rules found`.

### Practical policy rule

Order rules from most specific to most general.

A catch-all rule with no `path_regex` should normally appear last. If it appears first, every later rule is unreachable through this matching path.

Example policy shape:

```yaml
creation_rules:
  - path_regex: ^production/
    # production identities and encryption policy

  - path_regex: ^staging/
    # staging identities and encryption policy

  - path_regex: .*
    # general fallback
```

The final `.*` could also be represented by omitting `path_regex`; the important property is that the fallback comes after the narrower rules.

## Path matched against the regex

Current source obtains the absolute directory containing the selected config and attempts to strip that directory prefix from the candidate file path before running `path_regex`.

The intended policy model is therefore a path relative to the config location rather than an arbitrary machine-wide absolute path. This is consistent with official examples such as repository-relative `secrets/...` paths.

### Filename override for stdin and transformed paths

Official advanced-usage documentation explicitly warns that encryption uses the filename to choose a creation rule. When content arrives from stdin or the real input path is not the policy path, `--filename-override` can provide the logical filename SOPS should use for rule lookup and store-type inference.

This is an important reusable design pattern: separate the physical input stream from the logical policy identity of the artifact.

## Windows path-separator caveat

As of the inspected current main source, the matching path is trimmed with the native `filepath.Separator`, then passed directly to Go's regular-expression matcher. The inspected code does not normalize the resulting path with `filepath.ToSlash` before matching.

Upstream issue #2237, opened July 1, 2026, reports that this causes creation rules written with forward-slash separators to fail on Windows when the runtime path contains backslashes. The issue points to the same current matching path and proposes normalizing to forward slashes before regex evaluation.

GitHub Gold classifies this as a CURRENT UPSTREAM CAVEAT, not as independently reproduced behavior. Until upstream changes or closes the issue with a verified fix, cross-platform `.sops.yaml` authors should account for native path-separator semantics rather than assuming `/` patterns are portable everywhere.

## Default-rule semantics

A rule with no `path_regex` is not a repository-global default that gets merged with later matching rules. It is a normal first-match rule that matches everything.

Therefore this configuration:

```yaml
creation_rules:
  - age: age1GENERAL...
  - path_regex: ^prod/
    age: age1PRODUCTION...
```

selects the first rule for `prod/...` too. The production rule is unreachable.

This distinction matters because users may otherwise interpret YAML order as cosmetic.

## No rule merging in the inspected path

The selected creation rule is converted directly into one `Config`. The inspected matcher does not accumulate multiple matching rules and merge their identities, regex settings, or MAC policy.

This gives SOPS deterministic policy selection but means reusable policy composition must happen through the fields inside one rule, such as `key_groups` and nested key-group `merge`, rather than by stacking multiple matching creation rules.

## Relationship to key groups

Creation-rule selection and key-group quorum are separate layers:

- creation-rule ordering determines which policy object applies to the file;
- once one rule has been selected, its key groups and `shamir_threshold` determine the data-key recovery policy.

A perfectly designed Shamir quorum does not help if a broader earlier creation rule shadows the intended rule.

This makes configuration review a two-stage exercise:

1. confirm that the correct creation rule wins for the intended path;
2. confirm that the selected rule's identity/quorum policy is correct.

## Relationship to `updatekeys`

Official SOPS documentation recommends `updatekeys` for reconciling the master-key metadata in an already encrypted file with the identities defined by `.sops.yaml`.

Because creation-rule selection is first-match-wins, `updatekeys` inherits the importance of deterministic rule ordering: the selected rule controls the target identity/key-group policy used for the reconciliation.

This is a useful maintenance boundary for GitHub Gold to preserve: editing `.sops.yaml` does not, by itself, prove old encrypted files have been reconciled to the new policy.

## Security and operations lessons

### 1. Treat configuration order as authorization logic

A broad early rule can silently apply weaker or simply unintended recipients to sensitive paths.

### 2. Put catch-all rules last

An empty `path_regex` is unconditional at that position.

### 3. Review nested `.sops.yaml` files

The nearest config wins. A nested config can intentionally or accidentally replace parent policy for work performed beneath it.

### 4. Test logical filenames, not only file contents

For stdin, generated files, CI pipes, or temporary paths, use the documented filename-override mechanism when the physical input path is not the path policy should evaluate.

### 5. Include cross-platform path tests

The current Windows separator issue is a concrete example of why policy regexes should be tested on every supported execution platform.

### 6. Reconcile existing ciphertext after policy changes

Creation rules affect selection for creation/update workflows; existing SOPS metadata remains part of each encrypted file. Use the appropriate key-management workflow rather than assuming a config edit retroactively changes ciphertext access policy.

## Verification boundary

VERIFIED here means:

- source-level confirmation of config lookup and creation-rule iteration semantics;
- confirmation of official documentation describing first config discovery, config naming, rule matching, and filename override;
- confirmation that current inspected main source does not normalize creation-rule paths to forward slashes before regex matching;
- confirmation of an active upstream issue describing the Windows consequence.

It does not mean GitHub Gold independently ran Linux/Windows test matrices, fuzzed config parsing, verified every CLI code path, or reproduced issue #2237.

## Promotion impact

SOPS remains VERIFIED, provisional S / 28.

This follow-up does not justify a score change. It improves the catalog entry by making a security-relevant configuration property explicit: `.sops.yaml` is an ordered first-match policy surface with nearest-config discovery semantics.

## Strong next leads

1. Inspect creation-rule and config lookup tests for explicit precedence and nested-config coverage.
2. Trace `updatekeys` from selected creation rule through metadata reconciliation, including group/threshold changes.
3. Inspect group add/delete behavior to determine exactly when shares and wrapped data keys are regenerated.
4. Map SOPS audit-event coverage: what operations emit events, which provider identities are recorded, and where failures are visible.
5. Compare SOPS's `age` integration boundary with the standalone `FiloSottile/age` project already researched by GitHub Gold.
