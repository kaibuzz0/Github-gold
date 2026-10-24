# Tesseract OCR + OpenSCAD — GitHub Gold research, 2026-10-24

## Provenance and scope
GitHub-first discovery in offline document processing and parametric CAD. The active research branch already held 76 unique canonical entries and an empty candidate queue. The six saved YouTube playlist IDs were searched exactly in indexed results; no usable transcript or video metadata was obtained. No findings were attributed to playlists. No third-party source code was copied.

## Tesseract OCR — VERIFIED (upstream), S / 28
Repository: https://github.com/tesseract-ocr/tesseract

**Score:** Utility 5; Working Evidence 5; Reusability 5; Novelty 3; Documentation 5; Maintenance 5.

Inspected README, Apache-2.0 LICENSE, VERSION, `doc/tesseract.1.asc`, C/C++ API headers and implementations, output renderers, `src/textord/`, `src/lstm/`, `src/training/`, `unittest/` and CI workflows. The CLI and embeddable APIs process raster images and emit text, hOCR, ALTO, PAGE, TSV or searchable PDF. Native PDF *input* is not provided by the engine. Leptonica handles image decoding; language `traineddata` must be provided separately.

GitHub stable release **5.5.3**, published **2026-07-24**. Upstream Linux autotools [40128395434](https://github.com/tesseract-ocr/tesseract/actions/runs/40128395434) passed 4/4 jobs, CMake [40025480669](https://github.com/tesseract-ocr/tesseract/actions/runs/40025480669) passed 8/8 and sanitizer unit tests [40042891468](https://github.com/tesseract-ocr/tesseract/actions/runs/40042891468) passed 2/2. macOS autotools [40127924448](https://github.com/tesseract-ocr/tesseract/actions/runs/40127924448), Windows msys2 [40114227579](https://github.com/tesseract-ocr/tesseract/actions/runs/40114227579) and CodeQL [40091625811](https://github.com/tesseract-ocr/tesseract/actions/runs/40091625811) also succeeded. Workflow steps show `make check` and sample OCR executions, not just compilation.

**Licensing:** Engine Apache-2.0, dependency/model licensing separate. **Verification limit:** no independent installation, OCR accuracy benchmark, malformed-image fuzzing, traineddata license audit or security testing. Follow `tesseract-ocr/tessdata_fast`, `tessdata_best`, and `DanBloomberg/leptonica` to investigate speed/accuracy/preprocessing tradeoffs and model licensing.

## OpenSCAD — VERIFIED (upstream), S / 26
Repository: https://github.com/openscad/openscad

**Score:** Utility 5; Working Evidence 5; Reusability 5; Novelty 4; Documentation 4; Maintenance 3. Reduced maintenance score recognizes the old tagged stable release despite active commits.

Inspected README, COPYING and `src/openscad.cc` license header, `.gitmodules`, CMake, `src/core/` parametric AST and CSG, `src/geometry/` Boolean and extrusion functions, `src/io/` STL/3MF import-export and `tests/` regressions. C++17/CMake build uses Qt, CGAL, OpenCSG, Eigen, Boost and others. Headless build configurations exist.

Last non-prerelease GitHub release found **openscad-2021.01**, published **2021-02-07**; inspected master commit `bf28796b` dated **2026-10-24**. Upstream Linux build [40109445217](https://github.com/openscad/openscad/actions/runs/40109445217), release tests [40109445203](https://github.com/openscad/openscad/actions/runs/40109445203), experimental tests [40109445087](https://github.com/openscad/openscad/actions/runs/40109445087), macOS tests [40109445085](https://github.com/openscad/openscad/actions/runs/40109445085) and Windows tests [40109445266](https://github.com/openscad/openscad/actions/runs/40109445266) succeeded on 2026-10-24. Linux experimental workflow runs CTest, examples and coverage.

**Licensing:** GPL-2.0-or-later with CGAL linking exception; `libraries/MCAD` uses LGPL-2.1; Manifold, OpenCSG, Clipper2, mimalloc and other submodules have separate terms. **Verification limit:** no independent render, STL manifold check, print or engineering validation. Investigate `openscad/MCAD`, `elalish/manifold` and `AngusJohnson/Clipper2` before considering code extraction.

## Maintenance findings and next research
Previous GitHub Gold commit `f943c235` has **two** successful catalog audits: [40112975585](https://github.com/kaibuzz0/Github-gold/actions/runs/40112975585) and [40112972554](https://github.com/kaibuzz0/Github-gold/actions/runs/40112972554); one was still pending in the previous report. Rizin development CI remains failed at [40000224650](https://github.com/rizinorg/rizin/actions/runs/40000224650); no promotion warranted. Next: traineddata licenses and OCR accuracy; OpenSCAD nightly/stable geometry correctness; rotate to EDA or accessibility hardware.

**Execution boundary:** All builds/tests cited above are upstream GitHub Actions, not independent GitHub Gold runs.
