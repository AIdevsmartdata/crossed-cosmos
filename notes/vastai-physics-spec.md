# Vast.ai Physics Researcher Stack Spec — 2026-05-02
*Companion to `vastai-physics-setup.sh` and `vastai-physics-postinstall.sh`*

## What this is

A reproducible, hardware-optimised setup for running ECI-related computations on Vast.ai instances. Three workloads:

1. **Levier #1 MCMC** — joint `(ξ_χ, f_EDE, c'_DD)` on DESI DR2 + Pantheon+ + KiDS-1000. CPU-bound (Boltzmann solver) with mild GPU benefit if cosmopower_jax is used.
2. **GR-cosmo numerics** — D1–D6 derivations + N1–N5 numerics from `crossed-cosmos/derivations/` and `numerics/`. Pure-CPU, modest.
3. **Chimère-Ω runtime experiments** — LLM inference benchmarks, LeJEPA / SIGReg / Gated-DeltaNet sketches. GPU-bound.

## Hardware tiers — Vast.ai quick guide

| Tier | Use | GPU | CPU | RAM | $/hr (approx) | Notes |
|---|---|---|---|---|---|---|
| **A — Levier #1 baseline** | MCMC validation, 4 chains × 5 k steps | none required (CPU only) | EPYC 7763 (64-core) or Xeon Platinum | 64–128 GB | 0.3–0.6 | Maximize CPU cores; classy is the bottleneck. Pin chains to physical cores via `mpirun --bind-to core --map-by socket`. |
| **B — Levier #1 production** | 8 chains × 100 k steps, R−1 < 0.02 | none required | EPYC 9654 (96-core) or Threadripper 7995WX | 128–256 GB | 0.6–1.2 | 18–24 h walltime expected. Single-node, OMP per chain = floor(cores / chains). |
| **C — Cosmopower training + Chimère** | NN emulator on DR3 grid; LLM inference | A100 80 GB or H100 80 GB | 32-core | 128 GB | 1.5–3.0 | Use only when the emulator is the goal; not needed for plain MCMC. RTX 4090 24 GB also works for Chimère but tight for emulator training. |

**Recommendation for "tonight's run after re-setup":** Tier A — pick a single-node EPYC 64-core, no GPU. Cheapest path to validate the Cobaya YAML reproducibly.

## Files in this kit

```
~/vastai-physics-setup.sh         system-level (sudo) — apt + LaTeX + CUDA env
~/vastai-physics-postinstall.sh   user-level (no sudo) — venv + Python stack + AxiCLASS
~/vastai-physics-spec-2026-05-02.md   this doc
```

## Stack contents

### System (sudo) — `vastai-physics-setup.sh`

| Layer | Packages | Why |
|---|---|---|
| Build chain | gcc, g++, gfortran, cmake, ninja, ccache | Native compile of Boltzmann codes (CLASS family is pure C with Fortran-style numerics) |
| BLAS / LAPACK | OpenBLAS pthreads, LAPACK, LAPACKe | numpy / scipy / classy linear algebra. Auto-pin to AVX2 (Haswell) or AVX-512 (SkylakeX) coretype. |
| FFT | FFTW3 + MPI variant | CLASS uses FFTW for transfer functions; persistent homology uses it via gudhi |
| GSL | libgsl-dev | CLASS ODE integrators |
| HDF5 | libhdf5-dev + MPI | Cobaya chain output, large-array storage |
| MPI | OpenMPI 4.x + hwloc + numactl | 4–8 MCMC chains in parallel. `numactl --physcpubind` to dodge E-cores on hybrid CPUs |
| LaTeX | texlive-publishers, texlive-science, latexmk, biber, cm-super | Build eci.pdf, v6_jhep.pdf etc. — same toolchain that worked for v6.0.16 timestamp |
| Persistent homology | libgudhi-dev, libcgal-dev, libeigen3-dev | D5 derivation (β_k forecast on N-body snapshots) |
| Number theory | libgmp, libmpfr, libmpc, libprimesieve | v7-note Riemann-zero pipeline |
| Nested sampling | libnlopt | PolyChord backend, log-evidence Bayes factor |
| Monitoring | htop, nvtop, iotop, dstat, sysstat, strace, lsof | Live diagnostics during 18 h MCMC runs |

### User (no-sudo) — `vastai-physics-postinstall.sh`

| Group | Packages |
|---|---|
| Core scientific | `numpy<2`, scipy, sympy, mpmath, h5py, pandas, matplotlib, seaborn, plotly, ipython, jupyter, rich, tqdm |
| GPU compute | jax[cuda12], torch (cu124 wheel), accelerate, xformers |
| MCMC + nested | cobaya[mcmc], polychord-py3, dynesty, nautilus-sampler, ultranest, emcee, zeus-mcmc, pymc, pyro-ppl, numpyro |
| Posterior analysis | getdist, anesthetic, chainconsumer, corner, arviz |
| Cosmology side | camb, classy_sz, cosmopower, cosmopower_jax, halomod, hmf |
| Math | gudhi, ripser, persim, giotto-tda, primesieve |
| LLM / ML | transformers, datasets, peft, trl, bitsandbytes, safetensors, einops, vllm (GPU-conditional) |
| Optimisation | optuna, nevergrad |
| Boltzmann (built from source, native flags) | AxiCLASS (Poulin EDE), hi_class_public (Bellini–Sawicki αM/αB/αT/αK) |

`numpy<2` is **deliberate**: classy / hi_class C extensions are still ABI-locked to NumPy 1.x as of 2026-05; bumping to numpy 2.x silently breaks `import classy` (we hit this on Kevin's local box on 2026-05-02 night).

## Hardware-specific tuning

The setup script auto-detects:
- AVX2 vs AVX-512 (sets `OPENBLAS_CORETYPE`)
- GPU compute capability (A100 sm_80, H100 sm_90, RTX 40-series sm_89, RTX 50-series sm_120)
- CPU vendor (Intel / AMD)

…and writes everything to `/etc/profile.d/vastai-physics.sh`. CFLAGS use `-march=native` so AxiCLASS / hi_class are recompiled per-instance — no stale cross-tuning across rentals.

## Smoke tests (run automatically by postinstall)

```python
import numpy, scipy, sympy, mpmath, jax, torch, classy, cobaya, gudhi
# All must import cleanly
classy.Class().compute()    # smoke-test the actual Boltzmann loop
print(jax.devices())        # must show CudaDevice if GPU instance
```

## MCMC launch template (Tier A or B)

```bash
source /etc/profile.d/vastai-physics.sh
source ~/.venv/physics/bin/activate
cd ~/crossed-cosmos
export OMP_NUM_THREADS=$(( $(nproc) / 4 ))   # 4 chains × OMP threads
mpirun -np 4 --bind-to core --map-by socket cobaya-run mcmc/levier1/eci_levier1.yaml --resume
```

Monitor live:
```bash
nvtop                                                      # GPU
htop                                                        # CPU
watch -n 5 'wc -l ~/crossed-cosmos/mcmc/levier1/*.txt'      # chain progress
```

## Cost ceiling for Levier #1

Tier A validation: ~6 h × $0.5/h ≈ **$3**
Tier B production: 24 h × $1/h ≈ **$24**
Cosmopower training (Tier C, only if needed): 12 h × $2/h ≈ **$24**

**Total budget for full Levier #1 run with emulator: ~$50.** Compatible with current $11.79 Vast.ai credit + a $50 top-up.

## What this does NOT include

- A magical proof of M1 (the Sonnet audit on 2026-05-02 confirmed M1 stays Conjecture M1-C; no compute fixes that).
- A derivation of `ρ_Λ` (the cosmo-const audit on 2026-05-02 ruled all three Mistral approaches off by 14–89 orders).
- Anything that produces a "Nobel" by running at 2 a.m. — that's not how this works.

What it *does* enable: a clean, reproducible Levier #1 MCMC + Chimère-Ω benchmark + audit-pass infrastructure that any reviewer can re-run.
