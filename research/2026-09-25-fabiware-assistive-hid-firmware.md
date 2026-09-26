# FabiWare — unified assistive HID firmware

- **Upstream:** https://github.com/asterics/FabiWare
- **Author / organization:** AsTeRICS
- **Category:** accessibility / embedded firmware / alternative input / USB HID / Bluetooth
- **Evidence level:** VERIFIED (repository evidence; not independently hardware-tested by GitHub Gold)
- **Provisional Gold score:** 27/30 — **S tier**
  - Utility: 5/5
  - Working Evidence: 4/5
  - Reusability: 5/5
  - Novelty: 4/5
  - Documentation: 4/5
  - Maintenance: 5/5
- **License:** GPL-3.0 (repository LICENSE). Dependencies retain their own licenses.
- **Discovery:** recursive lead from the AsTeRICS accessibility ecosystem.

## What it is

FabiWare is the current shared firmware for the AsTeRICS FABI, FLipMouse and FLipPad alternative-input devices from hardware version 3 onward. It consolidates several assistive controllers around Raspberry Pi Pico-family microcontrollers and exposes build targets for RP2040/RP2350-based FABI hardware and Arduino Nano RP2040 Connect FLipMouse hardware.

The project is interesting as a reusable embedded assistive-input stack rather than only as device firmware. Its source tree separates button handling, commands, persistent configuration, GPIO, display, Bluetooth, infrared and a HID hardware-abstraction layer. That makes the architecture worth studying for custom switch interfaces, low-force controllers and accessible USB/Bluetooth HID devices.

## Why it matters

FabiWare sits at a useful boundary between inexpensive commodity microcontrollers and specialized accessibility hardware. A single firmware family supports multiple physical interfaces while preserving configurable HID behavior. The upstream README also documents a browser-based configuration manager that can store multiple settings and switch configurations on the fly.

Potentially reusable pieces include:

- `src/hid_hal.cpp` / `hid_hal.h` — HID abstraction boundary.
- `src/buttons.cpp` / `buttons.h` — physical switch/button input handling.
- `src/bluetooth.cpp` / `bluetooth.h` — Bluetooth transport support.
- `src/commands.cpp` / `commands.h` — configurable action/command layer.
- `src/eeprom.cpp` / `eeprom.h` — persistent configuration handling.
- `src/gpio.cpp` / `gpio.h` — hardware GPIO integration.
- `src/infrared.cpp` / `infrared.h` — environmental-control / IR functionality.
- load-cell and dual-channel NAU7802 dependencies for force-sensitive input designs.

## Build and platform evidence

Upstream documents PlatformIO builds and `.uf2` output. The current `platformio.ini` contains explicit environments for:

- `FABI_RP2350` — Raspberry Pi Pico 2W / RP2350, including low-power/battery-related features.
- `FABI_RP2040` — Raspberry Pi Pico W / RP2040.
- `FLIPMOUSE` — Arduino Nano RP2040 Connect.

The Pico targets pin the Earle Philhower Arduino-Pico framework at 4.7.1 and declare Adafruit BusIO, NeoPixel, SSD1306Ascii, LoadCellSensor and NAU7802-DualChannel dependencies. Bluetooth is enabled for FABI targets; the FLipMouse target deliberately ignores several BLE HID libraries.

## Maintenance evidence

The repository is active in 2026. The latest inspected commit is `2c58e699fe995c4abe9d2ed377ca27640d007a8a` from **2026-07-09**, fixing the firmware version number. Nearby July 8 commits include NAU7802 damping/readout changes and debug-output work, indicating recent maintenance against real sensor behavior rather than only documentation churn.

## Verification boundary

**Upstream/repository evidence observed:**

- explicit PlatformIO target configurations for three current hardware families;
- a substantial modular C/C++ source tree including HID, Bluetooth, buttons, commands, persistence, GPIO and infrared;
- current 2026 sensor/firmware maintenance;
- build/install instructions and links to device manuals/configuration tooling;
- GPL-3.0 license file.

**Not performed by GitHub Gold:**

- no firmware build or PlatformIO dependency resolution;
- no UF2 flashing;
- no FABI, FLipMouse or FLipPad hardware was connected;
- no USB/Bluetooth HID behavior was exercised;
- no load-cell, NAU7802, switch, infrared or battery behavior was independently tested;
- no accessibility/user evaluation was performed;
- no security audit of Bluetooth, configuration storage or command handling was performed.

The repository contains a `test/` directory, but the inspected directory currently only exposes a README; this pass did not find a substantive automated test suite there. That limits the Working Evidence score despite the concrete build targets and active hardware-oriented maintenance.

## Licensing caveat

The repository license is GPL-3.0. Do not copy implementation files into GitHub Gold without preserving GPL obligations and attribution. PlatformIO dependencies are separate upstream projects and must be license-checked independently before extraction or redistribution.

## Related projects / recursive leads

- https://github.com/asterics/FABI — hardware, manuals and legacy firmware history for the Flexible Assistive Button Interface.
- https://github.com/asterics/FLipMouse — low-force alternative pointing/controller hardware and legacy firmware.
- FLipPad — related flexible touchpad hardware in the same ecosystem.
- `ChrisVeigl/LoadcellSensor` — reusable load-cell input library referenced directly by FabiWare.
- `benjaminaigner/NAU7802-DualChannel` — dual-channel load-cell ADC support referenced directly by FabiWare.

## Follow-up

The strongest next component-level target is the HID/input pipeline (`buttons` → command mapping → `hid_hal`) and its use across FABI versus FLipMouse. A separate hardware dossier is justified only if the FABI/FLipMouse repositories provide substantial schematics, fabrication artifacts, calibration procedures or measured performance beyond what this firmware dossier already captures.
