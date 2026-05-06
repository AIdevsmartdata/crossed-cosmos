---
name: M1 Bug Inventory — A71 likelihood bugs
date: 2026-05-06
agent: Sub-agent M1 (Sonnet 4.6)
hallu_count: 85 → 85
---

# Bug Inventory: A71 likelihood bugs causing unphysical posteriors

## Status

Two critical bugs FIXED. Two moderate issues remain and are documented as [TBD].

---

## BUG A (CRITICAL — FIXED): PLANCK2018_COV_APPROX not positive definite

**Location:** `mcmc/a71_prod/likelihoods.py`, line ~617 (original), now line ~637

**Root cause:** The off-diagonal elements of the 5×5 Planck compressed covariance
were guessed approximations. These guesses produced a non-positive-definite matrix:
- Minimum eigenvalue: -3.998e-6 (negative)
- det(COV): -2.157e-29 (negative)

**Effect:** `chi2 = delta^T C^{-1} delta` is unbounded below when the covariance is
non-PD. The C^{-1} matrix has a negative eigenvalue (-2.501e5), meaning NUTS can
find configurations where chi2 = -∞. Combined with Bug B, NUTS drove parameters to
prior boundaries (n_s → 0.90, log10As_e10 → 3.50, omega_b → 0.019).

**Fix (BEFORE):**
```python
PLANCK2018_COV_APPROX = np.array([
    [ 2.25e-8,    -7.2e-9,      -2.0e-8,       5.0e-7,       5.0e-8],
    [-7.2e-9,     1.44e-6,       1.0e-7,      -3.0e-5,      -5.0e-7],
    [-2.0e-8,     1.0e-7,        9.61e-8,      1.0e-7,       1.0e-8],
    [ 5.0e-7,    -3.0e-5,        1.0e-7,       1.96e-4,      3.0e-5],
    [ 5.0e-8,    -5.0e-7,        1.0e-8,       3.0e-5,       1.764e-5],
], dtype=np.float64)
```

**Fix (AFTER):**
```python
PLANCK2018_COV_APPROX = np.diag(np.array([
    2.25e-8,   # omega_b:      sigma=0.00015 (Table 2, arXiv:1807.06209)
    1.44e-6,   # omega_c:      sigma=0.00120 (Table 2, arXiv:1807.06209)
    9.61e-8,   # theta_MC_100: sigma=0.00031 (Table 2, arXiv:1807.06209)
    1.96e-4,   # ln_As_e10:    sigma=0.014   (Table 2, arXiv:1807.06209)
    1.764e-5,  # n_s:          sigma=0.0042  (Table 2, arXiv:1807.06209)
]))
```

**Numerical verification:**
- Before: min eigenvalue = -3.998e-6, C^{-1}[omega_c, omega_c] = -1.924e5 (NEGATIVE)
- After: min eigenvalue = +2.250e-8, all diagonal C^{-1} elements POSITIVE

**Reference:** Aghanim et al. 2018, arXiv:1807.06209 (confirmed), Table 2 (sigma values)

**Additional fix:** Added PD validation in `_load_planck2018_compressed_from_file()`:
if the JSON file on disk contains a non-PD covariance, it falls back to the diagonal
(prevents the on-disk JSON from reinstating the bug).

---

## BUG B (CRITICAL — FIXED): ln_As conversion factor ln(10) applied incorrectly

**Location:** `mcmc/a71_prod/likelihoods.py`, `loglike_planck2018_compressed()`,
line ~731 (original)

**Root cause:** The sampled parameter `log10As_e10` has prior `Uniform[2.7, 3.5]`.
This range is physically meaningful ONLY for `ln(10^10 A_s)` (Planck fiducial = 3.044),
not `log10(10^10 A_s)` (which would be 1.322, far outside the prior).

The code converted `ln_As = log10As_e10 * ln(10)`, treating the parameter as
log10. This doubled the effective ln_As value at the Planck fiducial:
- Sampled value: 3.044 (the true ln(10^10 A_s))
- Code computed: 3.044 × 2.302585 = 7.008
- Planck mean: 3.044
- chi2 contribution: (7.008 - 3.044)^2 / 0.014^2 = 80213

With chi2~80000 from A_s alone, NUTS cannot find the true minimum. Combined with
Bug A (non-PD cov), it converged to a pathological posterior at prior boundaries.

**Fix (BEFORE):**
```python
ln_As = log10As_e10 * jnp.log(10.0)  # convert log10 → ln  [WRONG]
```

**Fix (AFTER):**
```python
# M1 bug-fix: parameter IS ln(10^10 A_s) — no conversion needed
ln_As = log10As_e10  # identity: parameter is already ln(10^10 A_s)
```

**Numerical verification:**
- Before: chi2(A_s) at Planck fiducial = 80213
- After: chi2(A_s) at Planck fiducial = 0
- Total chi2 after both fixes: 9.70 (from theta_MC approx bias only)

**Note:** The parameter name `log10As_e10` is a misnomer. It should be `ln_As_e10`.
The renaming is deferred to avoid breaking API (see [TBD]).

---

## BUG C (MODERATE — NOT FIXED, documented): theta_MC power-law approximation 3.1 sigma off

**Location:** `mcmc/a71_prod/likelihoods.py`, `theta_MC_approx()`, line ~693

**Description:** The power-law approximation for 100×theta_MC:
```python
theta_approx = 100.0 * 0.010411 * (omega_b/0.02238)**0.013 * (omega_m/0.1428)**(-0.252)
```
gives 1.041885 at Planck fiducial (omega_b=0.02237, omega_c=0.1200) vs
Planck 2018 Table 2 value of 1.04092 (sigma = 0.00031).
Error = (1.041885 - 1.04092) / 0.00031 = 3.11 sigma.

**Impact:** With the diagonal Planck covariance, this 3.11 sigma offset in theta_MC
causes a systematic bias in omega_c of ~0.44 sigma (-0.00053). This is ACCEPTABLE
for the smoke test but should be fixed before production.

**Fix options (TBD):**
- (a) Implement CLASS/CAMB call for theta_MC [most accurate, requires CLASS on PC]
- (b) Use EH 1998 Eqs 4-6 for z_drag, r_s(z_drag), and comoving distance background
      integral for D_M(z_*) [moderate accuracy, full implementation pending]
- (c) Recalibrate the power-law formula against CLASS output at grid of (omega_b, omega_m)

**Status:** [TBD: fix before production run. Not urgent for smoke test.]

---

## BUG D (MEDIUM — NOT FIXED): r_d (EH) 0.27% off CLASS

**Location:** `mcmc/a71_prod/background.py`, `sound_horizon_EH()`, line ~149

**Description:** The Aubourg 2015 fitting formula:
```python
r_d = 147.78 * (omega_m/0.1432)**(-0.255) * (omega_b/0.02083)**(-0.128)
```
gives r_d = 146.65 Mpc at Planck fiducial vs CLASS value of 147.05 Mpc (-0.27%).

DESI DR2 constrains r_d to ~0.3%, so this 0.27% offset introduces a ~1-sigma
systematic bias in the BAO chi2. The stated accuracy of the EH formula is ~2%,
so the formula is working within specification.

**Status:** [TBD: consider Friedmann integral (n_steps=2000 between z=10^5 and z_drag)
or CLASS-calibrated formula for production runs.]

---

## BUG E (NOT A BUG): Pantheon+ M_B marginalization sign

**Description:** The analytic M_B marginalization:
```python
chi2_marg = chi2_raw - A**2 / B
```
is CORRECT (chi2_marg <= chi2_raw, marginalizing improves likelihood).
Unit test confirms: ll_marg >= ll_fixed (as expected). Not a bug.

---

## Files modified

1. `/root/crossed-cosmos/mcmc/a71_prod/likelihoods.py`
   - `PLANCK2018_COV_APPROX`: replaced 5×5 non-PD matrix with diagonal
   - `loglike_planck2018_compressed()`: removed `* jnp.log(10.0)` factor
   - `_load_planck2018_compressed_from_file()`: added PD validation
   - Module docstring: updated with M1 bug-fix notes
   - `__main__` block: corrected test value (log10As_e10 = 3.044 directly)

2. `/root/crossed-cosmos/mcmc/a71_prod/likelihoods_unit_tests.py` (NEW)
   - 8 pure-numpy unit tests
   - Runnable on VPS without JAX
