# Smoke test: NMC(xi=0) == quintessence_monomial

## Setup
- Fork: `mcmc/nmc_patch/hi_class_nmc/` (hi_class 3.0 / CLASS 3.2.3, upstream 50f447c).
- Inputs:
  - `tests/nmc_zero.ini`: `gravity_model = nonminimal_coupling`, `parameters_smg = 0.0, 2., 1, 0, 10`, `V_chi_form = monomial`.
  - `tests/vanilla_quint.ini`: `gravity_model = quintessence_monomial`, `parameters_smg = 2., 1, 0, 10`.
- Same cosmology (default CLASS), `Omega_smg = -1` shooting.

## Result
Shooting parameter converges to identical value in both runs:
`shooting_parameter_smg = 9.60106382676749817162e-03`.

Fractional H(z) agreement on z in [0, 1000] (8573 sampled points
from CLASS's internal background table, interpolated to a common grid):

```
max  |dH|/H = 0.000e+00
mean |dH|/H = 0.000e+00
at z=0:   H_nmc=2.26189747e-04  H_van=2.26189747e-04
PASS (threshold 1e-4)
```

The two runs are **bit-for-bit identical** on H(z). This is the
correct and expected behavior: at xi=0 the NMC branch of
`gravity_models_smg.c` sets G4 = 1/2 exactly and G2 = X - V0 (H0/h)^2 phi^N,
which is **literally the same expression** evaluated by the
`quintessence_monomial` branch. The IC branch also copies the same
H0-normalized phi'_ini. No numerical drift is introduced.

## Verdict
Pass by >4 orders of magnitude (0 vs 1e-4 target).
Ready for downstream MCMC use with xi in a small neighborhood of 0.
Larger-xi stability and perturbation-level physics still require
validation (see learning_log notes).

## How to reproduce
```
cd mcmc/nmc_patch/hi_class_nmc
./class ../tests/nmc_zero.ini
./class ../tests/vanilla_quint.ini
python3 ../tests/compare_Hz.py
```
