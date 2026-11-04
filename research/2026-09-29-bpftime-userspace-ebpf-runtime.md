# bpftime — userspace eBPF runtime and extension framework

- **Upstream:** https://github.com/eunomia-bpf/bpftime
- **Author/org:** eunomia-bpf
- **Category:** observability / systems / eBPF / runtime / developer tooling
- **Evidence:** VERIFIED
- **Gold score:** 28/30 — S tier (provisional)
- **License:** MIT (root LICENSE inspected)
- **Discovery:** independent GitHub-first breadth rotation; duplicate search in Github-gold returned no bpftime entry

## Why it matters

bpftime moves a substantial eBPF execution environment into userspace rather than being merely another eBPF VM. Upstream exposes a loader, verifier integration, helpers, maps, shared-memory/interprocess maps, JIT/AOT backends and attach/event mechanisms. This makes it interesting both as an observability component and as a reusable general extension runtime where kernel eBPF is unavailable, restricted, or too expensive for a particular hook path.

Particularly valuable capabilities include userspace uprobes, syscall hooks, GPU-kernel instrumentation, experimental XDP/DPDK integration, CO-RE/BTF compatibility, interoperability with existing clang/libbpf/bpftrace workflows, and the ability to cooperate with kernel eBPF rather than requiring an all-or-nothing replacement.

## Gold score

| Dimension | Score | Notes |
|---|---:|---|
| Utility | 5 | Broad observability, instrumentation, network and extension-runtime uses. |
| Working Evidence | 5 | Extensive CI, examples, release history and peer-reviewed OSDI 2025 publication. |
| Reusability | 5 | Runtime, VM/JIT, verifier, maps, loader and attach mechanisms are separable components. |
| Novelty | 5 | Kernel-compatible eBPF semantics moved into a general userspace extension framework, including GPU work. |
| Documentation | 4 | Strong README/docs/examples/paper, but the breadth and experimental surfaces require careful feature-by-feature reading. |
| Maintenance | 4 | Very active development and CI; still pre-1.0 and some surfaces are explicitly experimental. |

**Total: 28/30.**

## Repository-native evidence

The README describes bpftime as a userspace runtime containing the loader, verifier, helpers, maps, ufunc support and multiple event sources rather than only a VM. It documents LLVM-based llvmbpf plus uBPF/interpreter options, shared userspace maps, CO-RE/BTF support, libbpf/clang compatibility, LD_PRELOAD and daemon loader modes, dynamic binary rewriting, and example programs.

The architecture identifies reusable areas under `vm`, `runtime`, `attach`, `bpftime-verifier`, `runtime/syscall-server`, `daemon`, and `example`. The current hooking design cites Frida Gum for userspace function hooks, zpoline/syscall_intercept techniques for syscall interception, a GPU path that converts eBPF to PTX, and experimental XDP with DPDK.

Upstream links an OSDI 2025 paper, *Extending Applications Safely and Efficiently*, which is stronger external technical evidence than repository claims alone. Performance claims such as "up to 10x" lower uprobe overhead are retained here only as upstream/paper claims; Github-gold did not reproduce them.

## Release and maintenance signals

Stable `v0.9.0` was published 2026-08-14. Its release notes show substantial runtime, verifier, GPU, CUDA/PTX, shared-map, dynamic-attach, compatibility and CI work. The default branch was still being updated on 2026-09-23, including an llvmbpf submodule update to trim linked LLVM backends.

GitHub Actions remains active. An inspected 2026-09-28 PR workflow run for GCC 13 completed successfully, as did the corresponding Docker workflow. This demonstrates current CI activity, but it does **not** mean Github-gold independently ran bpftime or that every platform/feature is proven by that one workflow.

## Useful components / extraction leads

- `vm` / llvmbpf: LLVM JIT/AOT eBPF execution backend.
- `runtime`: helpers, maps, ufuncs and runtime safety machinery.
- shared-memory maps: interprocess aggregation/control-plane primitive.
- `attach`: userspace uprobes, syscall tracepoints, GPU and experimental network event sources.
- `bpftime-verifier`: PREVAIL userspace verifier integration, with kernel verifier option where available.
- `runtime/syscall-server`: compatibility layer for existing eBPF toolchains.
- daemon/kernel cooperation path: bridge userspace execution with kernel eBPF maps/programs.
- GPU/PTX instrumentation: unusual path for tracing/extending CUDA kernels.
- examples and benchmark repository: useful verification targets before extracting individual components.

## Requirements / platforms

The project is primarily a systems-level C/C++ stack using LLVM and eBPF tooling. Linux is the clearest documented host environment for the current loader/attach ecosystem. Individual capabilities have additional dependencies: libbpf/BTF for kernel interoperability, Frida-based machinery for some binary rewriting, CUDA for GPU instrumentation, and DPDK/AF_XDP for experimental network paths. Cross-platform ambition should not be interpreted as equal maturity on every operating system.

## License and reuse

The root `LICENSE` is MIT, copyright 2024 Yusheng Zheng and Tong Yu. No bpftime source was copied into Github-gold. Before extracting code, inspect submodule and third-party licenses independently—especially llvmbpf, libbpf, verifier, Frida-related and other vendored dependencies—and preserve all notices.

## Evidence boundary / caveats

- Github-gold did **not** build bpftime, execute its tests, run its examples, inject it into a process, attach probes, execute GPU instrumentation, run DPDK/XDP, or reproduce benchmarks.
- Upstream performance numbers are not independent measurements from this research pass.
- The project is pre-1.0 (`v0.9.0` inspected), so API/ABI and feature stability deserve scrutiny.
- Some helpers/kfuncs and direct kernel-structure access available to kernel eBPF are unavailable in userspace; upstream explicitly documents this boundary.
- XDP/DPDK is described as experimental.
- Dynamic binary rewriting and process injection materially expand the trust/safety surface; production adoption should include verifier, loader, privilege, crash-containment and target-compatibility review.
- GPU instrumentation is moving quickly and should be scored independently before treating it as equivalent in maturity to the core runtime.

## Verification performed this run

1. Searched Github-gold for `bpftime`; no existing indexed entry was returned.
2. Inspected upstream README and architecture/component descriptions.
3. Inspected the authoritative root MIT license.
4. Inspected current GitHub Actions activity and observed successful 2026-09-28 build/Docker PR workflows.
5. Inspected release metadata for v0.9.0 (published 2026-08-14).
6. Inspected the current default-branch commit, dated 2026-09-23.
7. Distinguished upstream/paper performance claims from actions actually performed by Github-gold.

## Strong next leads

1. **llvmbpf** — score separately as a standalone LLVM eBPF JIT/AOT VM/library.
2. **Userspace verifier path** — inspect PREVAIL configuration, verification modes and fallback boundaries.
3. **GPU/PTX path** — trace eBPF→PTX transformation, map semantics, CUDA attach lifecycle and GPU-specific CI.
4. **Syscall interception** — inspect zpoline/syscall_intercept-derived mechanics and containment assumptions.
5. **bpf-benchmark** — determine whether benchmark methodology and raw data support the headline performance claims.
6. **Compatibility matrix** — test representative unmodified libbpf/bpftrace programs against userspace and kernel modes.
