# Asterics AAC — offline-capable accessible communication and control platform

- **Upstream:** https://github.com/asterics/Asterics-AAC
- **Author/org:** asterics / AsTeRICS Foundation ecosystem
- **Category:** accessibility / AAC / offline-first web app / assistive input / smart-home control
- **Evidence:** VERIFIED (primary-source inspection; not independently executed)
- **Gold score:** **29/30 — S tier**
  - Utility 5/5
  - Working Evidence 5/5
  - Reusability 5/5
  - Novelty 4/5
  - Documentation 5/5
  - Maintenance 5/5
- **License:** AGPL-3.0 for source; repository README states documentation/non-source material is CC BY-SA 4.0; bundled/external assets and services can carry separate terms
- **Discovery:** independent GitHub-first accessibility research after rotating out of Atlas/geospatial infrastructure

## Why it matters

Asterics AAC is a mature browser-based augmentative and alternative communication platform rather than a narrow symbol board. It combines offline-capable customizable communication grids with text-to-speech, multilingual boards, word forms, predictive/self-learning dictionaries, multiple access methods, media access, messaging and smart-home actions.

Its unusually broad input model is the strongest differentiator for GitHub Gold: the application documents operation through click/touch, keyboard, scanning and switches, with eye tracking, head tracking and EMG muscle-sensor access available through the wider AsTeRICS framework. This makes the project useful both as a complete assistive application and as a source of design patterns for software that cannot assume conventional touch/mouse input.

## Concrete capabilities inspected

The upstream README documents:

- communication boards ranging from simple to complex AAC layouts;
- cross-platform browser/PWA-style use on PC, smartphones and tablets across Windows, Linux, Android and iOS;
- offline operation;
- optional cross-device cloud synchronization with end-to-end encryption;
- text-to-speech and multilingual communicators;
- ARASAAC and Open Symbols search integration;
- word forms, customizable keyboards, word prediction and self-learning dictionaries;
- a global grid for persistent/core vocabulary;
- progressive-language layouts;
- sentence sharing to other applications;
- Matrix-backed in-app messaging;
- HTTP actions and integrations with openHAB/Home Assistant;
- live elements, web radio, podcasts and YouTube access.

Some network-backed media/search/messaging/sync features naturally require connectivity even though the core application is documented as offline-capable.

## Architecture and reusable pieces

The inspected package manifest shows a conventional JavaScript/Vue web application with useful composable dependencies and subsystems rather than a proprietary native runtime. Notable building blocks include:

- PouchDB for local/browser data;
- Matrix JS SDK plus encrypted-attachment support for messaging;
- `predictionary` for predictive text;
- `interactjs` for interaction behavior;
- JSZip/FileSaver and PDF/image tooling for import/export and generated material;
- Vue 2 plus vue-i18n;
- Jest/jsdom tests;
- Webpack production builds.

The production build command runs Jest before producing the bundle and generating service-worker cache paths. That is useful evidence that tests are part of the normal build path rather than merely present in the repository.

## Working and maintenance evidence

Primary-source inspection on 2026-09-25 found:

- documented local install/build/test commands (`yarn install`, `npm run start`, `npm run build`, `npm run test`);
- Jest configured with a jsdom environment;
- a production build script that executes the test suite before Webpack;
- a current stable hosted deployment and a separate latest/testing deployment documented upstream;
- active commits through 2026-09-18;
- a stable release published 2026-09-18 whose notes record an Android Chromium voice-selection workaround, pronunciation support for collect elements and speech sequencing/stability improvements;
- earlier September/August 2026 releases addressing performance, search, global-grid behavior, speech interruption, grid ordering, fullscreen behavior and hover-triggered actions;
- ongoing funded development under the InDiKo accessibility research project (2024-2028), as documented by upstream.

These signals support VERIFIED as repository evidence. GitHub Gold did not execute the software.

## Accessibility value

Asterics AAC is especially strong as a reference for alternate-input UX. It does not treat accessibility as a single screen-reader toggle; its documented access surface includes scanning, switches and advanced sensor-driven methods. The same grid/action abstraction also extends beyond speech into media and environmental control, which is valuable for users who may need one interface for both communication and device interaction.

The project's global-grid/core-vocabulary and progressive-language concepts are also useful design patterns for adaptive interfaces: persistent high-value actions can remain available across pages while vocabulary/layout complexity changes with the user's needs.

## Offline/local-first characteristics

Upstream explicitly states that Asterics AAC works without an Internet connection. The package also uses browser-local PouchDB and the build pipeline generates service-worker cache paths. Optional synchronization and Internet integrations are layered on top rather than making cloud connectivity the only operating mode.

This distinction matters for assistive technology: loss of Internet connectivity should not inherently remove the core communication surface. GitHub Gold has not independently tested cold-start/offline cache behavior, however, so the exact boundaries of first-load and asset availability remain an empirical follow-up item.

## License / reuse caveats

The repository README and package manifest identify the source as **AGPL-3.0**. The repository README separately states that documentation and non-source code are CC BY-SA 4.0. Integrations/assets can have their own terms; upstream specifically acknowledges external symbol, font, voice and service providers.

Do not assume every symbol, font, voice or remotely obtained media asset inherits the application's AGPL license. Inspect the applicable provider/content license before redistributing a bundled derivative. No upstream implementation code or assets were copied into GitHub Gold.

## Limitations / risks

- Developer documentation is explicitly described upstream as unfinished and potentially outdated.
- The codebase includes Vue 2-era architecture and a substantial dependency surface, so long-term dependency modernization deserves inspection even though current maintenance is active.
- Optional cloud sync, Matrix messaging, symbol search, media and smart-home integrations enlarge the security/privacy surface compared with a purely offline board.
- Browser speech synthesis quality and voice availability vary by platform; the September 2026 release itself contains a Chromium/Android voice-switching workaround, demonstrating real platform-specific behavior.
- HTTP smart-home actions and the documented non-HTTPS deployment option can create mixed-content/security tradeoffs and should be treated as trusted-local-network functionality rather than exposed blindly.
- AAC suitability is user-specific. Repository evidence can establish software capability, not clinical appropriateness for an individual communicator.

## What GitHub Gold did not verify

GitHub Gold did **not**:

- install dependencies or build the application;
- execute Jest or browser/UI tests;
- run the PWA offline or verify cold-start cache completeness;
- test switch scanning, eye gaze, head tracking or EMG hardware;
- evaluate communication-board usability with AAC users;
- test cloud synchronization or independently audit its end-to-end encryption;
- connect Matrix messaging;
- operate Home Assistant/openHAB or arbitrary HTTP actions;
- validate TTS behavior across browsers/devices; or
- perform a security/privacy audit of local or network integrations.

## Strong recursive leads

1. **`asterics/predictionary`** — inspect the self-learning/predictive dictionary as a reusable accessibility/text-entry component.
2. **AsTeRICS Framework sensor/input bridge** — inspect how eye gaze, head tracking, switches and EMG inputs are normalized and delivered to applications.
3. **Offline/sync layer** — inspect PouchDB/service-worker behavior and encryption boundaries to establish exactly what remains usable from a fresh offline start versus after prior caching.
4. Compare current Asterics AAC with newer small offline AAC projects only where they offer materially different on-device TTS, vocabulary or deployment designs; do not create redundant AAC link dumps.

## Verdict

**VERIFIED — S / 29.** Asterics AAC clears the Gold bar because it combines a mature maintained AAC application, broad alternate-input support, offline capability, customizable/predictive language tooling, environmental control and a test-bearing open web architecture. Its strongest reusable value is not merely its communication-board UI but the way it unifies communication, alternate access and actionable grid elements across heterogeneous devices and user input capabilities.