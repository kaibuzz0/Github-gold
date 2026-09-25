# Predictionary — local self-learning word-prediction component

- **Upstream:** https://github.com/asterics/predictionary
- **Author/org:** asterics / AsTeRICS ecosystem; package author Benjamin Klaus
- **Category:** accessibility / text entry / local word prediction / JavaScript library
- **Evidence:** VERIFIED (primary-source code/test inspection; not independently executed)
- **Gold score:** **24/30 — A tier**
  - Utility 5/5
  - Working Evidence 4/5
  - Reusability 5/5
  - Novelty 3/5
  - Documentation 4/5
  - Maintenance 3/5
- **License:** AGPL-3.0
- **Discovery:** recursive lead from the Asterics AAC dossier

## Why it matters

Predictionary is a small, reusable JavaScript word-prediction engine that does not require a remote inference service. It supports prefix completion, previous-word next-word prediction, multiple dictionaries, dictionary import/export, ranked vocabulary, and local learning from user selections/typing. This makes it relevant to AAC, alternate-input keyboards, low-bandwidth/offline interfaces and privacy-sensitive text entry.

The component is materially smaller and easier to reuse than the full Asterics AAC application. Its value is architectural simplicity rather than state-of-the-art language modeling: a host application can ship a base vocabulary, maintain user-specific dictionaries, learn word and transition frequencies locally, and serialize that state as JSON.

## Concrete implementation inspected

`src/index.mjs` exposes the higher-level predictor. Primary-source inspection found:

- multiple named internal dictionaries;
- enable/disable selection of dictionaries for a prediction session;
- adding/deleting words and importing ranked word lists;
- single-dictionary and all-dictionary JSON export/import;
- word-completion and next-word prediction paths;
- learning/refinement from chosen words and previous-word context.

`src/dictionary.mjs` contains the compact underlying model. Each learned word carries frequency/rank information and transition counts to following words. `learn()` increments the selected word frequency and, when a previous word exists, increments or creates the previous→chosen transition count. `predictNextWord()` reads those learned transition frequencies. Prefix completion is case-insensitive and includes a fallback that backs up to a shorter prefix when no direct match exists, marking the returned results as fuzzy matches.

This is intentionally a lightweight frequency/transition model, not a neural language model. That is useful for predictable offline behavior and constrained environments, but it also limits linguistic sophistication.

## Working evidence

Primary-source inspection on 2026-09-25 found:

- package version **1.6.0**;
- npm and browser/CDN installation documented upstream;
- a browser demo and generated API documentation linked from the README;
- Jest tests in the source tree, including tests that exercise learning behavior;
- the package build script runs `jest` before documentation generation and Webpack production bundling;
- a Node demo is included;
- source-level implementation for learning, prediction and serialization rather than README-only claims.

GitHub's Releases endpoint currently returns no formal GitHub Releases. The latest inspected repository commit is from **2022-09-28**, so this is a mature/stable component rather than an actively evolving standalone project. Current use as a dependency of the actively maintained Asterics AAC application is a useful ecosystem signal, but it should not be confused with current maintenance of this repository itself.

## Reusable pieces

- `src/index.mjs` — public predictor/dictionary-management API.
- `src/dictionary.mjs` — word storage, prefix completion, transition-based next-word prediction and learning.
- JSON import/export — useful for local persistence, migration and user-specific learned state.
- Ranked word-list import — allows corpus-derived frequency lists to seed predictions.
- Multi-dictionary selection — useful for language, domain, user or context-specific vocabularies.
- Jest tests — executable examples of expected prediction/learning semantics.

## Runtime / platforms

The library is ES6 JavaScript and is documented for browser use via npm/unpkg and for Node through the included demo. Its package metadata reflects an older toolchain (`webpack` 4, Jest 24 and the historical Node `--experimental-modules` invocation), so integration into a modern build should be validated rather than assuming the original setup is current.

No special hardware is required.

## Licensing / data caveats

The package manifest identifies the library as **AGPL-3.0**. GitHub Gold did not copy implementation source. Any redistribution or derivative integration must evaluate AGPL obligations for the intended deployment model.

The README separately acknowledges external n-gram sample data from Mark Davies/ngrams.info and word-frequency lists from the University of Leeds corpus for training/demo purposes. Do not assume those data sets inherit the source-code license; inspect their applicable permissions before redistributing corpus-derived assets.

## Limitations / risks

- Standalone repository maintenance is stale: latest inspected commit is September 2022.
- No formal GitHub Releases were present during inspection.
- Dependency/build tooling is old and should be modernized or isolated before new production adoption.
- Prediction is frequency/transition based; it does not provide modern semantic/contextual language-model behavior.
- Prefix prediction iterates dictionary keys, which may become costly for very large vocabularies; benchmark realistic dictionary sizes before latency-sensitive use.
- Learned dictionaries can encode sensitive personal vocabulary and phrase-transition information. Host applications should treat exported/local learned state as user data and protect it accordingly.
- Corpus/demo-data licensing must be checked independently from the AGPL source license.

## What GitHub Gold did not verify

GitHub Gold did **not**:

- install the npm package;
- execute Jest or Webpack;
- run the browser or Node demos;
- benchmark dictionary size, latency or memory use;
- test multilingual morphology or AAC-specific prediction quality;
- validate compatibility with current Node/browser bundlers;
- independently inspect npm publication integrity; or
- evaluate prediction quality with end users.

## Follow-up leads

1. Inspect how current Asterics AAC persists and scopes Predictionary learned state, particularly privacy and reset/export behavior.
2. Compare with one actively maintained lightweight local predictor only if it offers materially stronger multilingual, trie/indexing or on-device-model behavior.
3. Rotate accessibility research toward the AsTeRICS alternate-input/sensor bridge; it is likely more novel than further mining this mature predictor.

## Verdict

**VERIFIED — A / 24.** Predictionary is useful GitHub Gold because it is a compact, code-backed, tested local prediction component with self-learning transition frequencies, serializable dictionaries and straightforward browser integration. Its standalone maintenance age and old build stack keep it below S tier, while active use inside Asterics AAC preserves practical relevance.