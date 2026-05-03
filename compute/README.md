# compute/ — ECI numerical campaign

Scaffolding for Vast.ai rental + local execution. Each `Cn_*/` is a standalone numerical project that produces a publishable Tier-1 paper or a section of a larger paper.

## Hardware targets

| Target | Spec | Cost / hour | Items feasible |
|---|---|---|---|
| **Local desktop** | i5-14600KF (14C/20T) + 32 GB DDR5 + RTX 5060 Ti 16 GB (sm_120) | 0 | C1, C2, C3 (small N), C5 (small grid) |
| **Vast.ai mid** | 32 vCPU + 1×A6000 48 GB or 1×L40S 48 GB | $0.50–0.90 | C1 (production), C2 (production), C3 (medium N), C5 (production) |
| **Vast.ai big** | 64 vCPU + 4×H100 80 GB or 4×A100 80 GB | $4–8 | C4 (joint MCMC 10 models), C3 (large N MERA), CDT/EPRL spin-foam |

## Items

- **C1_fv_qei_bounce/** — Numerical refutation of LQC / pre-big-bang / matter bounce as Hadamard resolutions, via Fewster-Verch quantum energy inequality (QEI). Confirms analytic refutation that Mistral cross-check produced for the Z4 LQG sub-agent. Stack: JAX. Scale: 10³ CPU-h or 1 GPU-day.
- **C2_holographic_complexity/** — HRT extremization on dynamic FRW background, comparing CV/CA/CV2.0 with ECI's K(t) modular Krylov complexity. Stack: JAX. Scale: workstation, 10³ CPU-h.
- **C3_dmrg_krylov/** — Direct DMRG/MERA computation of Krylov complexity K(t) for ECI's modular Hamiltonian. N up to 2^18 fits on 16 GB VRAM. Stack: TenPy + cuQuantum. Scale: 1-3 GPU-weeks at largest N.
- **C4_joint_mcmc/** — Joint MCMC across 10 cosmological models on Planck PR4 + DESI DR2 + DES Y6 + Euclid Q4. AxiCLASS + Cobaya. Builds on existing `mcmc/` infra. Scale: 10⁴-10⁵ CPU-h.
- **C5_hadamard_bvii0/** — Numerical Hadamard parametrix verification on Bianchi VII_0 (currently parametrix-only in `paper/bvii0_sle_bieberbach`). Reinforces the SLE result. Stack: Fortran kernel + JAX wrapper. Scale: 10⁴ CPU-h.

Per-item README in each subdir gives exact reproduction command + expected output + estimated wall-time at given allocation.

## Pre-existing infrastructure to reuse

- `/root/crossed-cosmos/mcmc/` — Cobaya MCMC chains + deploy scripts (proven to work on Vast.ai per `notes/vastai-debug-2026-05-02.md`)
- `/root/crossed-cosmos/scripts/vastai/launch-mcmc.sh` — known-good MPI flags for Docker/Vast.ai
- Local `~/AxiCLASS` and `~/hi_class_public` — Boltzmann solvers
- Local `~/.venv-mcmc-bench` — Cobaya 3.6.2, cosmopower_jax 0.5.5, JAX cuda12

## Workflow

1. Develop on local desktop using small grids (single-A100-equivalent equiv via 5060Ti)
2. Validate on Vast.ai mid for 1-2 hours
3. Production run on Vast.ai big or local long-night
4. Push results to `compute/CN_*/results/` and write paper section

See `setup-vastai.sh` for one-shot Vast.ai instance bootstrap.
