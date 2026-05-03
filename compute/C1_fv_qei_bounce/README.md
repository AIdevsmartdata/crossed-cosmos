# C1 — Fewster-Verch QEI numerical refutation of bouncing cosmologies

**Goal.** Confirm numerically what Mistral cross-check showed analytically (Phase-3 Z4 audit): LQC-style bounces, pre-big-bang, and matter-bounce scenarios are NOT Hadamard resolutions of the FRW initial-data singularity, because they violate the Fewster-Verch quantum energy inequality (FV-QEI) on the relevant past-light-cone diamond.

**Stack.** JAX (CPU + GPU), sympy for closed forms, mpmath for high-precision regression tests.

**Scale.** ~10³ CPU-h on i5 = 1-2 weeks wall-time (parallelisable across 14 cores). On Vast.ai 32-core: 1-2 days. On 1×A100: 6-12 hours.

**Reproduction.**
```bash
cd $REPO/compute/C1_fv_qei_bounce
python run_qei_scan.py --bounce loop_quantum  --grid 128 --output results/lqc.h5
python run_qei_scan.py --bounce pre_big_bang  --grid 128 --output results/pbb.h5
python run_qei_scan.py --bounce matter_bounce --grid 128 --output results/mb.h5
python analyse_violations.py results/*.h5 --output figures/
```

**Expected output.** For each bounce model: a 2-panel figure showing (a) the energy-density expectation value as a function of the smearing-time τ on the past-light-cone diamond, (b) the FV-QEI bound $-C/\tau^4$, and the violation curve (a) + (b). All three bounce models should violate at small τ.

**Theory anchor.** Fewster-Verch 2003 (CMP 240:329, [arXiv:math-ph/0203010](https://arxiv.org/abs/math-ph/0203010)) for the QEI; Hollands-Wald 2001 (CMP 223:289, [arXiv:gr-qc/0103074](https://arxiv.org/abs/gr-qc/0103074)) for Hadamard parametrix subtraction; LQC bounce: Ashtekar-Singh 2011 ([arXiv:1108.0893](https://arxiv.org/abs/1108.0893)).

**Output paper target.** `paper/fv_qei_bounce_refutation/` — Tier-1 short note, 4-6 pp, JCAP or PRD short.

## Layout

- `run_qei_scan.py` — main driver (TODO)
- `qei_kernel.py` — JAX-vmap'd QEI bound + bounce energy density (TODO)
- `bounce_models.py` — LQC, PBB, matter-bounce a(τ) profiles (TODO)
- `tests/` — sympy regression for closed-form QEI on de Sitter (Hollands-Wald) and Minkowski (Fewster-Verch original)
- `results/` — h5 output (gitignored)
- `figures/` — pdf output (gitignored)
