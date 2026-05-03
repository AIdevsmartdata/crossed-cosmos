# C2 — Holographic complexity (CV/CA/CV2.0) vs ECI Krylov K(t) on FRW

**Goal.** On a dynamic FRW background with past-light-cone diamond geometry, compute the three holographic-complexity prescriptions (Complexity = Volume, Complexity = Action, CV2.0 a.k.a. CA-2.0) via HRT extremization, and compare time-dependence with ECI's modular Krylov complexity K(t) (CMPT 2023, arXiv:2306.14732).

**Why it matters.** ECI postulates that K(t) emerges as the modular-flow analogue of holographic complexity. A direct numerical agreement at leading order on dynamic FRW would constitute strong evidence; a structural mismatch sharpens the claim that they are independent objects converging on the same physical quantity.

**Stack.** JAX (CPU + GPU). Geodesic / minimal-surface extremization via JAXopt or custom Hessian descent.

**Scale.** Workstation. ~10³ CPU-h on i5; 1-3 days on 1×A100; trivial on H100. Memory: 1-4 GB.

**Reproduction.**
```bash
cd $REPO/compute/C2_holographic_complexity
python run_complexity_scan.py --N 256 --t_max 10 --output results/cv_ca_cv2.h5
python compare_with_K_t.py results/cv_ca_cv2.h5 ../C3_dmrg_krylov/results/K_t.h5
python make_figures.py
```

**Theory anchors.**
- HRT 2007 ([arXiv:0705.0016](https://arxiv.org/abs/0705.0016))
- Stanford-Susskind CV ([arXiv:1406.2678](https://arxiv.org/abs/1406.2678))
- Susskind CA ([arXiv:1411.0690](https://arxiv.org/abs/1411.0690))
- CV2.0 Couch-Fischler-Nguyen ([arXiv:1610.02038](https://arxiv.org/abs/1610.02038))
- ECI Krylov K(t) closed form: `paper/k_frw_generalised_entropy/lemma33.tex`
- CMPT 2023 modular Krylov: [arXiv:2306.14732](https://arxiv.org/abs/2306.14732)

**Output paper target.** `paper/holographic_vs_krylov/` — Tier-1 numerical comparison, 6-8 pp.

## Layout

- `run_complexity_scan.py` — main driver (TODO)
- `cv_kernel.py`, `ca_kernel.py`, `cv2_kernel.py` — JAX kernels per prescription (TODO)
- `frw_geometry.py` — past-light-cone diamond geometry helpers
- `compare_with_K_t.py` — alignment + residuals vs ECI's K(t)
- `results/` — h5 output (gitignored)
- `figures/` — pdf output (gitignored)
