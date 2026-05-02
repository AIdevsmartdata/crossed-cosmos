# AxiCLASS Shooting Failure: Search Results and Workaround Analysis
**Date:** 2026-05-02  
**Context:** EPYC 7V13 (Zen 3) on Vast.ai; AxiCLASS master (ba4ede7, 2026-04-27); EDE config `scf_potential=axion, fraction_axion_ac=0.05, log10_axion_ac=-3.531, scf_parameters="2.0,0.0"`.

---

## Section 1: GitHub Repository Search Results

### AxiCLASS Issue Tracker (PoulinV/AxiCLASS)

The repository has exactly **4 open/closed issues and PRs** total (verified via `api.github.com/repos/PoulinV/AxiCLASS/issues?state=all`):

| # | Type | Title | State |
|---|------|-------|-------|
| 4 | PR | add perturbations type1 coupling | open |
| 3 | Issue | Incompatibility of classy.pyx with python 3.12 | closed |
| 2 | PR | Implemented shooting for Omega_scf by varying f_ax | closed/merged |
| 1 | Issue | Math library linking commented out | closed |

**None of these address the shooting failure, ludcmp singular matrix, fzero_Newton convergence, or Zen 3 FP behaviour.** Zero results for searches on "ludcmp", "singular matrix", "fzero_Newton", "EPYC", "AMD", "Zen", or "AVX" in issues.

### Upstream CLASS (lesgourg/class_public) — Critical Finding

Upstream CLASS released **v3.3.4 on 2025-11-24** with commit `e85808324f51fc694d12e3ed7439552a3c3f9540`, message:

> "Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table."

The fix in `source/input.c` at line 934 changed:
```c
if(dx < x1*_EPSILON_){      // BEFORE: negative dx silently passes the convergence check
```
to:
```c
if(fabs(dx) < x1*_EPSILON_){ // AFTER: correct absolute-value test
```

**AxiCLASS "updating to CLASS v3.3" commit is dated 2025-04-15** (SHA `8a049832`), which is **7 months before the v3.3.4 fix**. CLASS v3.3.0 was released on 2025-02-17. AxiCLASS merged v3.3.0's architecture changes but none of the subsequent v3.3.1–v3.3.4 patch series.

Checking AxiCLASS master `source/input.c` for `fabs(dx)`: **not found**. The raw file search for `_EPSILON_` in the 1D Ridders path shows `fabs(xnew-ans)` (correct), but no evidence of the fabs fix in the multidimensional Newton path used for dual-target shooting (`fraction_axion_ac` + `log10_axion_ac`).

### Related Commits in AxiCLASS Since v3.3 Merge

Post-April-2025 commits (the entire set):
- `ba4ede7` (2026-04-27): "Follow CLASS logic for SCF fluid switch" — perturbation mode flag logic
- `2a46148` (2026-04-23): "Add no-fluid axion notebook with explicit background and perturbation step sizes"
- `37897c9` (2025-04-15): "debug, almost done"
- `8a04983` (2025-04-15): "updating to CLASS v3.3"

None address the shooting numerical stability or the ludcmp failure.

---

## Section 2: arXiv Literature Search Results

No arXiv paper was found that specifically reports or resolves the AxiCLASS `evolver_ndf15` / `ludcmp` / `singular matrix` shooting failure for the axion EDE parametrisation. Searches on "AxiCLASS shooting numerical instability", "background_init singular", "fzero_Newton EDE" all returned zero relevant hits.

The foundational AxiCLASS paper (Poulin, Smith, Karwal, Kamionkowski 2018, arXiv:1811.04083) does not discuss shooting convergence issues. The review paper arXiv:2302.09032 ("Ups and Downs of EDE") also does not mention this failure mode.

One recent paper (arXiv:2604.13535, submitted April 2026, "Double the axions, half the tension") uses multi-field EDE but does not document shooting fixes.

**No published fix or workaround for this specific failure exists in the arXiv literature.**

---

## Section 3: Workaround Proposals

### Root Cause Analysis

The failure chain is:
1. `fzero_Newton` (Newton's method for 2-target shooting: `fraction_axion_ac` + `log10_axion_ac`) calls
2. `input_try_unknown_parameters` which calls `background_init` which calls
3. `background_solve` → `evolver_ndf15` → `new_linearisation` → `ludcmp`
4. `ludcmp` detects a near-singular Jacobian matrix and fails.

The Jacobian becomes degenerate because during the axion's transition from frozen (slow-roll) to oscillating phase (at `a_c = 10^{-3.531} ≈ 2.94 × 10^{-4}`), the second derivative of the potential `ddV_scf = d²V/dφ²` swings through zero as the field crosses the inflection point of the cosine potential `V ∝ (1 - cos φ)^n`. For `n=2, φ_ini=2.0`, this creates a near-singular right-hand side in the implicit ODE system, yielding a degenerate Jacobian for `ndf15`.

A secondary issue: the `fabs(dx)` bug in `fzero_Newton` (fixed upstream in CLASS v3.3.4 but absent in AxiCLASS) means the Newton shooter can oscillate with a negative `dx` step that incorrectly satisfies the convergence test, driving the system into degenerate regions of parameter space.

### Workaround A: Backport the CLASS v3.3.4 fabs(dx) Fix (Effort: 30 minutes)

In `source/input.c`, find the convergence guard in the 1D bracket-walking code near the Ridders method. The multidimensional Newton path (`fzero_Newton` call at line ~1358) is in `source/input.c`; the actual `fzero_Newton` implementation is inside `source/input.c` itself around line 1118. Apply:

```c
// Find: (somewhere around the dx convergence test inside fzero_Newton)
if(dx < x1*_EPSILON_){
// Replace with:
if(fabs(dx) < x1*_EPSILON_){
```

To apply without full source access, use `grep -n "_EPSILON_" source/input.c` on the Vast.ai instance to locate the exact line, then apply `sed -i 's/if(dx < x1\*_EPSILON_)/if(fabs(dx) < x1*_EPSILON_)/g' source/input.c`.

**Caveat:** This fixes the shooting oscillation but does NOT fix the underlying singular Jacobian in `ndf15`.

### Workaround B: Force Runge-Kutta Evolver for Background (Effort: 5 minutes, parameter-level)

In the `.ini` file or a `.pre` precision file, set:
```ini
background_evolver = 0   # 0 = RK45 (evolver_rkck), 1 = ndf15 (default)
```
`evolver_rkck` does not use LU decomposition and is immune to the singular Jacobian. It is less stable for stiff problems but the axion background (while oscillatory) is tractable in RK if the step size is tight.

Combine with tighter step control:
```ini
background_integration_stepsize = 0.1   # default 0.5; reduce for oscillating axion
back_integration_stepsize = 7.e-3       # from REFCLASS.pre reference
```

This can be tested immediately without code changes.

### Workaround C: Looser Shooting Tolerances (Effort: 2 minutes, parameter-level)

The precision file defaults are `tol_shooting_deltax = 1e-4`, `tol_shooting_deltaF = 1e-6`. Setting looser values can help the Newton solver accept a less-precise converge before the background integration drifts into the degenerate zone:
```ini
tol_shooting_deltax = 1e-3
tol_shooting_deltaF = 1e-3
```
The `scf_3p_base.yaml` cobaya file already uses `precision_newton_method_F: 1e-3` and `precision_newton_method_x: 1e-3` — the `.ini` equivalents should be set to match. The `adptative_stepsize = 1000` field (note: typo in code as "adptative") in the cobaya yaml is an AxiCLASS-specific parameter that should also be passed via `extra_args`.

### Workaround D: Use Effective/Fluid Parametrisation (Effort: 30 minutes to test)

The `class_ede` fork (mwt5345/class_ede) implements EDE with parameters `{f_EDE, log10z_c, thetai}` using a different shooting strategy that avoids the degenerate regime by parametrising in effective observables rather than particle physics parameters. However, class_ede is based on CLASS (unknown version, last commit unclear) and uses a different SCF implementation. Migration from AxiCLASS to class_ede would require re-validating the parameter mapping.

### Workaround E: Pheno Fluid Mode (Effort: Already tried, limited)

`scf_evolve_as_fluid: yes` or `scf_evolve_like_axionCAMB: yes` bypasses the Klein-Gordon ODE and replaces it with a fluid EOS. This avoids the oscillation transition singularity but the `README` documents a known bug: "code seems to get stuck, probably an issue with tables handling." This mode does not support perturbations reliably.

---

## Section 4: Effort Estimate and Recommendation

| Fix | Effort | Confidence |
|-----|--------|------------|
| A: Backport fabs(dx) from CLASS v3.3.4 | 30 min | Medium — addresses part of the failure |
| B: Switch background_evolver=0 (RK) | 5 min | Medium-high — avoids ludcmp entirely |
| C: Loosen shooting tolerances | 2 min | Low-medium — may allow convergence at cost of precision |
| A+B+C combined | 1 hour | High — best immediate attempt |
| Full upstream merge to CLASS v3.3.4 | 3-5 days | Very high — requires careful diff/merge of 7 months of CLASS patches into AxiCLASS's axion extensions |
| Migrate to class_ede or EDE-CLASS | 1-2 weeks | High — different code base, parameter mapping not trivial |

**Brutally honest assessment:** There is no existing published fix for this specific failure. The bug has two components: (1) a known upstream CLASS v3.3.4 bug (fabs(dx)) that AxiCLASS has not incorporated, and (2) a deeper singular-Jacobian issue in ndf15 triggered by the rapid oscillation of the axion field at the EDE transition scale factor. Workarounds B+C should be tested in 10 minutes on the Vast.ai instance without any code changes. If they fail, Workaround A requires modifying one line of source code and recompiling.

The Zen 3 / EPYC 7V13 architecture is very likely irrelevant to this failure: the `ludcmp` singular matrix error is deterministic in parameter space (not a floating-point precision difference between ISAs). The FP fix in `scripts/vastai/axiclass-fp-fix.patch` that resolved the `background_tau_of_z` boundary check was a real FP-precision issue; the shooting failure is a different, parameter-level numerical instability that would reproduce on any architecture.

**If Workarounds A+B+C all fail after 1 day of debugging, recommend pivoting Levier #1 to permanently drop AxiCLASS EDE** and continue with Levier #1B (pure LCDM 7-param) which already works (sigma8=0.8249 confirmed). A future Levier #1-EDE could use class_ede with the effective parametrisation, but that is a multi-day rewrite of the MCMC pipeline.
