# C5 — Numerical Hadamard parametrix on Bianchi VII_0

**Goal.** Reinforce the SLE Hadamard result in `paper/bvii0_sle_bieberbach/note.tex` (currently parametrix-only) with a direct numerical verification of the wavefront-set decay condition on Bianchi VII_0.

**Stack.** Fortran kernel (existing GR community code) + JAX wrapper for autodiff comparison.

**Scale.** 10³-10⁴ CPU-h. Local-feasible at modest grid; production on Vast.ai mid (32 vCPU) for 1-2 days.

**Reproduction.**
```bash
cd $REPO/compute/C5_hadamard_bvii0
make -j  # builds Fortran kernel
python run_wf_check.py --grid 256 --output results/wf_bvii0.h5
python verify_radzikowski.py results/wf_bvii0.h5
```

**Theory anchor.**
- Radzikowski 1996 (CMP 179:529) — wavefront-set characterisation of Hadamard
- Banerjee-Niedermaier 2023 ([arXiv:2305.11388](https://arxiv.org/abs/2305.11388)) — SLE Hadamard on Bianchi I
- ECI extension: `paper/bvii0_sle_bieberbach/note.tex` (parametrix-only currently)

**Output.** Section in `paper/bvii0_sle_bieberbach/` v2 closing the parametrix-vs-WF gap. Or short companion note.

## Layout

- `Makefile` + `kernel.f90` — Fortran wavefront-set checker (TODO)
- `run_wf_check.py` — Python driver (TODO)
- `verify_radzikowski.py` — apply Radzikowski criterion to numerical WF
- `results/`, `figures/` — gitignored
