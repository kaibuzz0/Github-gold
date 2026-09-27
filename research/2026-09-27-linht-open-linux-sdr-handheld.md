# LinHT — open Linux SDR handheld hardware

- **Upstream:** https://github.com/M17-Project/LinHT-hw
- **Author / org:** M17-Project
- **Category:** open hardware / SDR / amateur radio / embedded Linux / GNU Radio
- **Evidence:** VERIFIED
- **Provisional Gold score:** **28 / 30 (S)**
  - Utility: 5
  - Working evidence: 5
  - Reusability: 4
  - Novelty: 5
  - Documentation: 5
  - Maintenance: 4
- **Discovery:** GitHub-first category rotation after local-first synchronization research.

## What it is

LinHT is an open-source, Linux-based UHF software-defined-radio handheld transceiver built around a CompuLab MCM-iMX93 Linux SoM and Semtech SX1255 direct-IQ RF front end. It is the successor to OpenHT and deliberately removes an FPGA from the signal path to make the platform easier to develop against with ordinary Linux, GNU Radio, SoapySDR, C/C++ and Python tooling.

This repository is the hardware-design side of a larger ecosystem. It contains KiCad 9 project files, schematics, PCB layout and automated manufacturing outputs; companion M17-Project repositories provide Yocto hardware/software/SDR layers.

## Why it is Gold

The important feature is not merely that the schematic is published. LinHT exposes a genuinely hackable handheld radio architecture with a general Linux compute platform, direct complex-IQ baseband access, programmable RF attenuation, audio codec, GNSS, battery/power management and an always-on ATtiny power controller.

The project also preserves hardware revisions and documents failures rather than presenting an unvalidated board as finished. Rev A established the architecture; Rev B was physically manufactured and extensively tested; current Rev C incorporates concrete corrections learned from Rev B.

That combination makes LinHT useful both as a complete experimental radio and as a reference architecture for open handheld SDR, embedded-Linux radio integration, power sequencing, direct-IQ RF paths and reproducible KiCad fabrication automation.

## Concrete working evidence

Upstream states that four Rev A proof-of-concept prototypes validated Linux boot, USB development access, display integration and the initial SDR/DSP architecture.

Rev B is preserved as a tagged GitHub release and upstream reports several manufactured prototypes were tested successfully. The documented Rev B hardware added the GRF5604 transmit PA, SKY13330 RF switch, dual PE4312 step attenuators, USB-C charging, GNSS, TLV320 audio, and ATtiny826 power management.

Upstream reports demonstrated Rev A/B software operation for:

- FM TX/RX with pre-/de-emphasis and CTCSS;
- SSB TX/RX;
- M17 TX/RX;
- TETRA receive;
- experimental 64-QAM at 2 Mbps.

The README reports approximately 4.5 W CW measured on Rev B and about 3.5 W during an M17 test. These are **upstream measurements**, not measurements performed by GitHub Gold.

## Particularly useful components / patterns

- **Direct-IQ Linux radio architecture:** SX1255 complex baseband feeding a Linux SoM without an FPGA in the signal path.
- **Embedded Linux SDR environment:** Yocto + GNU Radio + SoapySDR + normal Linux development/debug tooling on the handheld itself.
- **RF chain:** GRF5604 PA, SKY13330 TX/RX switch and two PE4312 digital step attenuators.
- **Power architecture:** BQ25792 2S USB-C buck/boost charger, TPS565242 main 5 V converter and ATtiny826 always-on sequencing/controller logic.
- **Audio:** TLV320AIC3100 codec and speaker path.
- **GNSS:** Quectel LG77L family receiver; Rev C replaces the underperforming board antenna with an external-antenna connector.
- **Reproducible fabrication pipeline:** GitHub Actions runs the KiCad build and publishes fabrication/web artifacts and Pages documentation.
- **Revision-as-evidence workflow:** revA/revB tags preserve manufactured states while `main` is explicitly identified as unvalidated Rev C.

## Current Rev C status

As of September 2026, Rev C is active development on `main`. It incorporates fixes discovered during Rev B testing, including side-button voltage-domain isolation, software-reset control for the audio codec, changes to the audio clock arrangement, replacement of obsolete inductors, external GNSS antenna support and PCB thermal/DRC corrections.

Recent upstream commits through **2026-09-17** include completing Mouser part numbers for Rev C, fixing the routed panel outline for fabrication, adding the side-buttons PCB fabrication/docs, fixing a keyboard-bus connection and adding SD2 test points.

A Rev C test batch is being manufactured, but upstream explicitly says Rev C has **not yet been manufactured/validated**. Do not transfer Rev B validation claims to Rev C.

## CI / manufacturing evidence

`.github/workflows/main.yml` runs on pushes in a KiCad builder container, checks the board input, executes `make`, requires fabrication/web output files, uploads those artifacts and deploys the generated web output to GitHub Pages on `main`.

This is useful reproducibility evidence for the design/fabrication pipeline. It is not equivalent to electrical/RF validation of the resulting board.

## Hardware / runtime requirements

The current design is a replacement mainboard for a **Retevis C62** donor handheld and reuses its enclosure, display, keypad, battery, side-button PCB, SMA/audio connectors, encoder and mechanical parts. A custom PCB must be manufactured and populated.

The radio is UHF-only in current revisions. Upstream describes up to 500 kHz IQ bandwidth. It is experimental hardware, not a consumer radio.

Flashing uses NXP Universal Update Utility (`uuu`) once the board is placed into USB boot mode. Rev B has a known limitation in the intended side-button USB-boot mechanism; the Rev C correction remains unvalidated until physical boards are tested.

## License

The hardware repository is licensed **CC BY-NC-SA 4.0**.

This is a major reuse caveat: the **NonCommercial** restriction makes it unsuitable for treating as ordinary permissive open hardware for commercial reuse. Attribution and ShareAlike requirements also apply. Companion software/Yocto repositories and third-party components must be checked under their own licenses.

No upstream design/source files were copied into GitHub Gold.

## Caveats / risks

- Rev C on `main` is currently unvalidated hardware.
- Rev B is functional/tested but upstream explicitly recommends **not** manufacturing it because its known defects are corrected in Rev C.
- Current hardware is UHF-only.
- Building requires PCB manufacture, assembly and a donor Retevis C62.
- The device is not certified; transmit operation is subject to applicable spectrum/amateur-radio rules.
- RF output/filter performance and compliance must not be inferred beyond upstream measurements.
- CC BY-NC-SA 4.0 materially restricts reuse compared with permissive hardware licenses.

## Verification performed by GitHub Gold

Inspected:

- upstream README and explicit September 2026 status;
- hardware revision changelog;
- tagged Rev B release notes and known-issue record;
- current GitHub Actions fabrication workflow;
- recent commit history through 2026-09-17;
- root licensing statement.

GitHub Gold **did not** manufacture a PCB, boot Linux on LinHT, flash an image, execute the DSP software, measure RF output/spectral purity, test receiver sensitivity, exercise GNSS/audio/power subsystems, reproduce M17/SSB/FM/64-QAM demonstrations, or validate Rev C.

## Related ecosystem / recursive leads

- https://github.com/M17-Project/meta-linht-hardware
- https://github.com/M17-Project/meta-linht-software
- https://github.com/M17-Project/meta-linht-sdr
- https://github.com/M17-Project/LinHT-utils
- M17 protocol/tooling ecosystem
- OpenHT predecessor history

The strongest next component-level research target is the **LinHT Yocto/SDR software stack**: determine how the SX1255 IQ path is exposed into Linux/GNU Radio/SoapySDR, which drivers and DSP blocks are reusable independently, and whether those companion repositories have reproducible CI and compatible licenses.
