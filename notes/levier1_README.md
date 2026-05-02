# ECI Levier #1 — Launch Guide

**Configuration file:** `mcmc/chains/eci_levier1_run1/eci_levier1.yaml`
**Plugin files:** `mcmc/cobaya_nmc/eci_kids_s8.py`, `mcmc/cobaya_nmc/eci_nmc_theory.py`
**Status:** ready to launch once AxiCLASS F6 FP-bug is patched (see §Prerequisites)

---

## What this run does

Joint 12-parameter MCMC on DESI DR2 BAO + Pantheon+ + KiDS-1000 S8 prior, sampling the full ECI parameter space: standard LCDM base (omega_b, omega_cdm, H0, n_s, logA, tau_reio), EDE axion sector (fraction_axion_ac, log10_axion_ac, theta_i), and ECI NMC/DD sector (xi_chi, log10lambda_chi, c_prime_DD). This is the first simultaneous attack on both the H0 and S8 tensions within the ECI framework.

---

## Prerequisites before launching

1. **Patch AxiCLASS F6 FP-bug** (blocking). AxiCLASS 3.3.0 fails on Zen 3 with a near-zero z boundary error. Fix: backport the upstream `lesgourg/class_public` 3.3.4 background.c patch into AxiCLASS, or merge AxiCLASS EDE patches onto class_public 3.3.4. Estimated: 1-2 days (see `notes/vastai-debug-2026-05-02.md §F6`).

2. **Resolve scf_parameters injection** (known issue). Cobaya's classy wrapper does not natively pass a sampled-parameter-dependent string into `extra_args`. The parameter `theta_i` needs to reach AxiCLASS as `scf_parameters = "<theta_i>,0.0"` at each likelihood call. Two resolution paths:
   - Extend `ECINMCTheory.calculate()` to call `provider.get_classy_cosmo().set({"scf_parameters": f"{theta_i},0.0"})` before the AxiCLASS computation step.
   - Write a thin Cobaya `classy` subclass that overrides `set_cl_reqs()` to inject `scf_parameters` dynamically.
   The YAML flags this as `# AXICLASS_ARG_TBD` at the theta_i parameter block.

3. **Install likelihoods and packages:**
   ```
   cobaya-install bao.desi_dr2.desi_bao_all sn.pantheonplus -p mcmc/packages/
   ```

4. **Build and install AxiCLASS** (patched version):
   ```
   cd ~/src/AxiCLASS
   pip install --no-build-isolation -e python/
   ```
   Activate venv before make to ensure `python` resolves (see `notes/vastai-debug-2026-05-02.md §F4`).

---

## Launch command

```bash
mpirun --bind-to none --mca btl_vader_single_copy_mechanism none \
  -np 4 python -m cobaya run \
  mcmc/chains/eci_levier1_run1/eci_levier1.yaml \
  --packages-path mcmc/packages/
```

Use `setsid ... disown` pattern for background survival on Vast.ai (see `notes/vastai-debug-2026-05-02.md §F13`).

---

## Walltime estimates

From `notes/calculation_triage_2026_05_02.md §A1`:

| Hardware | Chains | Estimate |
|---|---|---|
| Local i5 (single-threaded) | 4 × serial | 12-15 days |
| Vast.ai Tier B (96-core EPYC) | 4 MPI | ~18 h |
| Vast.ai Tier A (128-core EPYC 7V13, $0.40/h) | 4 MPI | 2-3 days |

These estimates assume the AxiCLASS call takes ~10x longer than vanilla CLASS due to the shooting algorithm. Actual timing should be benchmarked on the first 500-step checkpoint.

---

## Scenario classification (decision tree from triage §A1)

After chains converge (R-1 < 0.02), apply the following decision tree:

**Scenario (a) — target outcome:**
All four hold simultaneously:
- `fraction_axion_ac > 0.05` at > 2 sigma
- `|xi_chi| > 0.005` at > 1 sigma
- S8 tension retreats to < 2 sigma
- H0 tension retreats to < 2 sigma

Action: draft PRD/JCAP letter "ECI is the first single framework simultaneously addressing both H0 and S8 tensions."

**Scenario (b) — realistic fallback:**
H0 retreats (EDE + NMC work together), but S8 tension persists (> 2 sigma). The Dark Dimension sector alone is insufficient to suppress sigma8.

Action: extend to IDM Yukawa extension (13th parameter: interaction rate Gamma_IDM). Redirect to Levier #2.

**Scenario (c) — null result:**
Both tensions persist above 3 sigma after marginalisation. The joint EDE + NMC + DD parameter space does not have enough freedom within the given priors.

Action: retract Levier #1 as a standalone publication claim. Redirect compute to Levier #2 (lab-scale Dark Dimension) and Levier #3 (persistent homology). Document the null result in a short note.

---

## Disclaimer

This YAML and likelihood plugin have not been executed. All parameter names, prior ranges, and likelihood formulations are based on: (i) verified AxiCLASS ini files fetched from PoulinV/AxiCLASS HEAD, (ii) source-level verification of AxiCLASS input.c and background.c for parameter conventions, (iii) the existing working v5 MCMC pipeline, and (iv) the triage specification in `notes/calculation_triage_2026_05_02.md`. The outcome of this run is entirely unknown until chains converge. Past sessions in this codebase have caught 6+ LLM-fabricated references and parameter names; the AxiCLASS argument names used here have been verified against primary source code, with the one known TBD flagged explicitly (`scf_parameters` injection mechanism). There is no guarantee that all 12 parameters are well-constrained by this dataset combination, that the proposal scales are optimal, or that convergence will be achieved within the walltime estimates. Treat the first checkpoint (R-1 progress at 1000 steps) as the real confidence signal.
