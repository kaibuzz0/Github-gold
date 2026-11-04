# AsTeRICS — assistive integration runtime and sensor/actuator construction set

- **Repository:** https://github.com/asterics/AsTeRICS
- **Author / Org:** AsTeRICS
- **Category:** accessibility / assistive technology / alternate input / sensor-actuator integration / environmental control
- **Evidence:** VERIFIED
- **Provisional Gold score:** 25 / 30 — **A tier**
  - Utility: 5/5
  - Working evidence: 5/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 2/5
- **Discovery source:** Recursive follow-up from the Asterics AAC dossier; GitHub-first verification against the upstream repository.

## What it is

AsTeRICS (Assistive Technology Rapid Integration & Construction Set) is a graphical construction framework for composing assistive-technology solutions from sensor, processor and actuator components. Upstream explicitly targets computer input, environmental control, games/toys, brain/neural interfaces and Android-phone interaction.

The important catalog value is not simply the end-user application. The repository is a large integration corpus containing the AsTeRICS Runtime Environment (ARE), graphical/configuration tooling, many device/protocol plugins, REST client libraries, deployment/model tooling, native bridges and examples. This makes it useful as a reference architecture for connecting unconventional human-input sensors to operating-system or environmental-control actions.

## Why it matters

Asterics AAC identifies the AsTeRICS framework as the bridge for advanced access methods such as eye tracking, head tracking and EMG muscle sensors. The framework itself confirms the broader design: heterogeneous sensors and actuators are assembled into deployable models rather than hard-wired into one monolithic application.

That architecture is reusable well beyond AAC. A project can use the repository as a source of patterns for alternate input, signal processing, model-driven device integration, assistive HID generation and environmental-control interoperability.

## Useful components / code surfaces

### ARE middleware and component model

`ARE/` contains the runtime middleware and component/plugin tree. Repository-native tests exist for middleware parsers, resource management, thread-pool behavior, timer/event components and APE model inspection. This is concrete code/test evidence, not only a README claim.

### REST integration surface

`ARE_RestAPIlibraries/` contains client code and examples for remotely controlling the runtime. The Java client exposes operations such as starting a deployed model through `/runtime/model/state/start`, and the documentation contains browser-side REST examples. This is a particularly reusable boundary for connecting modern UIs or automation to the older Java runtime without embedding directly into it.

### Eye-tracking implementation

`ARE/components/sensor.eyetracker/` contains a dedicated sensor component with Java/JNI glue and native C++ implementation. The bundle descriptor classifies it as a computer-vision sensor, while the manifest declares native libraries. Related native code includes pupil-detection logic. Treat this as implementation evidence, not a claim that current commodity eye trackers were independently verified by GitHub Gold.

### APE model/deployment tooling

`ARE/tools/APE/` includes model-inspection/deployment tooling and JUnit targets. This is useful for understanding how AsTeRICS packages solution-specific models around the runtime.

### Release automation

The repository contains GitHub Actions release workflows for Linux, macOS and Windows. Stable release 4.3.0, published 2024-01-31, includes packaged Linux, macOS and Windows artifacts. This is strong historical working evidence even though release cadence is now slow.

## Install / runtime requirements

Current upstream quick-build instructions require JDK 8 and Apache Ant >= 1.9.1 and start the runtime with `ant run`. The README prefers a 32-bit JDK. These requirements are a material modernization constraint in 2026 and reduce the maintenance score.

## Platforms

Historically packaged for Windows, Linux and macOS. Individual plugins can have narrower native/device/platform constraints.

## Languages / technologies

Predominantly Java plus native C/C++, Ant build infrastructure, OSGi-style bundles, REST clients and device-specific/native libraries.

## License

**Mixed / component-specific. Do not treat the repository as carrying one simple license.**

Upstream states:

- ACS and NativeASAPI libraries: LGPL.
- ARE middleware, ARE plugins, services and BNCI Suite: dual MIT or GPL with CLASSPATH exception, subject to the selected component set.
- Some plugins, including examples named upstream such as MathEvaluator and VLC, are GPL without the CLASSPATH exception.
- Upstream explicitly instructs users to inspect the `LICENSE` directory of each plugin/service.

Therefore no implementation source was copied into GitHub Gold. Any future extraction must resolve licensing at the exact component/file boundary first.

## Maintenance signals

The repository is not archived. The newest inspected commit is 2025-11-24 and corrects the documented JDK requirement to JDK 8. The previous visible maintenance wave in September 2024 updated GitHub Actions artifact actions and constrained release runner versions. The latest inspected stable release is 4.3.0 from 2024-01-31.

This is weaker current maintenance than Asterics AAC and Predictionary's ecosystem relevance, so the project is scored A rather than S despite its unusually broad technical corpus.

## Verification performed

GitHub Gold inspected:

- upstream README and build requirements;
- repository structure and recent commit history;
- published release metadata/artifacts;
- GitHub Actions release-workflow inventory;
- repository-native JUnit/test source locations;
- REST client/API implementation and documentation;
- eye-tracker Java/JNI/native component structure;
- upstream licensing explanation.

GitHub Gold did **not** compile or run AsTeRICS, execute its tests, install release artifacts, connect assistive hardware, validate eye/head/EMG tracking, exercise environmental-control protocols, test Android integration, or independently audit native libraries.

## Caveats / risks

1. **Legacy runtime requirements:** JDK 8, Ant and 32-bit preference make deployment less modern than newer accessibility stacks.
2. **Mixed licensing:** licensing must be resolved per selected plugin/service before reuse or redistribution.
3. **Hardware age:** the repository spans many generations of sensors, native SDKs and environmental-control technologies; presence of a plugin is not evidence that its hardware/driver stack remains obtainable or compatible in 2026.
4. **Native dependencies:** JNI/native DLLs and platform-specific device SDKs reduce portability for some components.
5. **Maintenance cadence:** current upstream activity is sparse relative to the breadth of the codebase.
6. **Safety/accessibility:** assistive control systems should be evaluated with actual users and appropriate fail-safe behavior; source-level inspection is not clinical or usability validation.

## Related projects

- https://github.com/asterics/Asterics-AAC — actively maintained AAC application that can use AsTeRICS for advanced access methods.
- https://github.com/asterics/predictionary — local self-learning prediction library used in the AAC ecosystem.
- https://github.com/asterics/FLipMouse — alternate mouse/keyboard/joystick hardware project.
- https://github.com/asterics/FABI — flexible assistive button interface.
- https://github.com/asterics/FabiWare — newer shared firmware line for FABI/FLipMouse/FLipPad devices.
- https://github.com/asterics/esp32_mouse_keyboard — ESP32 BLE HID keyboard/mouse implementation.

## Follow-up research

The strongest recursive lead is now **FabiWare / FLipMouse / FABI** rather than another pass over the legacy framework itself. Those projects may expose current embedded HID, switch, sip/puff and low-force input components with substantially newer hardware relevance. A second useful component lead is the ARE REST boundary, but it should only receive a separate dossier if inspection reveals a sufficiently standalone, reusable interface rather than duplicating this entry.
