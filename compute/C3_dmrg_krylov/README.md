# C3 — DMRG / MERA Krylov complexity at large N

**Goal.** Direct numerical computation of K(t) for ECI's modular Hamiltonian on a finite-N tensor network, scaling N from 2^10 to 2^20. Verifies analytical K_FRW result (`paper/k_frw_generalised_entropy/lemma33.tex`) and exposes finite-N corrections.

**Stack.** TenPy + cuQuantum (CUDA 12 backend). Quimb fallback for portability.

**Scale.**
- N=2^16: fits 16 GB VRAM (RTX 5060 Ti) — 1 day GPU
- N=2^18: borderline 16 GB — 1 week GPU OR 80 GB H100 in 1 day
- N=2^20: needs H100 80 GB or A100 80 GB; 1-3 days

**Reproduction.**
```bash
cd $REPO/compute/C3_dmrg_krylov
python build_modular_H.py --N 65536 --output results/H_mod_N65k.npz
python run_lanczos.py results/H_mod_N65k.npz --steps 256 --output results/K_t_N65k.h5
python plot_K_t.py results/K_t_N*.h5
```

**Theory anchors.**
- Caputa-Magán-Patramanis-Tonni 2023 modular Krylov ([arXiv:2306.14732](https://arxiv.org/abs/2306.14732)) — main analytical reference
- Parker-Cao-Avdoshkin-Scaffidi-Altman 2019 universal operator growth ([arXiv:1812.08657](https://arxiv.org/abs/1812.08657))
- ECI's K_FRW lemma 3.3-3.4: `paper/k_frw_generalised_entropy/lemma{33,34}.tex`

**Output paper target.** `paper/dmrg_krylov_finite_N/` — Tier-1 6-8 pp numerical paper.

## Layout

- `build_modular_H.py` — constructs Type II_∞ modular Hamiltonian on a finite tensor network (TODO)
- `run_lanczos.py` — Lanczos tridiagonalisation + Krylov complexity reconstruction (TODO)
- `plot_K_t.py` — finite-N scaling plots
- `tests/` — small-N regression vs CMPT closed form
- `results/` — h5 output (gitignored, can be large)
