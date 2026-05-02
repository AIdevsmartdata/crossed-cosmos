# AxiCLASS Zen 3 FP fix — apply, build, test

## What this fixes

On AMD EPYC Zen 3 (verified Vast.ai EPYC 7V13 contract 36023758, 2026-05-02), bare-default LCDM compute on AxiCLASS aborts immediately with:

```
Error in Class: thermodynamics_init(L:382) :error in thermodynamics_lists(...)
=>thermodynamics_lists(L:1146) :error in background_tau_of_z(...)
=>background_tau_of_z(L:285) :condition (z < pba->z_table[pba->bt_size-1]) is true;
   out of range: z=0.000000e+00 < z_min=6.661338e-16
```

The value `6.661338e-16 = 3 × DBL_EPSILON` is a floating-point endpoint drift in `pba->loga_table[pba->bt_size-1]`. Detailed root-cause analysis is in `axiclass-fp-fix.patch` header comments.

This patch is a **boundary-check tolerance** approach: relax the `class_test` in `background_tau_of_z` line 285 from `z < pba->z_table[pba->bt_size-1]` to `z < pba->z_table[pba->bt_size-1] - 1e-12`. The tolerance `1e-12` is well above `DBL_EPSILON ≈ 2.22e-16` but well below any physically meaningful `z_min`. One line.

A surgical alternative (pin `loga_table[bt_size-1] = loga_final` after the fill loop) was attempted first but did not propagate because AxiCLASS wraps the integration in an outer `while (is_axion_converged == _FALSE_)` loop that re-fills `loga_table` per iteration. The tolerance-in-check approach is robust against this.

## Verification, 2026-05-02 on Vast.ai EPYC 7V13:

```
classy: v3.3.0 (AxiCLASS) /root/src/AxiCLASS/python/classy.cpython-310-x86_64-linux-gnu.so
bare LCDM: sigma8 = 0.8249    (matches vanilla CLASS 3.3.4 exactly)
```

## Apply

```bash
cd /root/src/AxiCLASS
patch -p1 < /root/crossed-cosmos/scripts/vastai/axiclass-fp-fix.patch
```

If the patch tooling has issues with whitespace, edit `source/background.c` line 285 manually:

```c
class_test(z < pba->z_table[pba->bt_size-1] - 1e-12,
```

## Build

```bash
cd /root/src/AxiCLASS
make clean
make -j16 CC=gcc OPTFLAG="-O3 -fopenmp"
```

## Install in the venv

**Critical:** Python's import resolution prefers a `classy.cpython-310-*.so` in `$VENV/lib/python3.10/site-packages/` over the editable install in `/root/src/AxiCLASS/python/`. Earlier `pip install classy_szfast` (a cosmopower dependency) drops a `classy 3.2.3` .so directly into site-packages. **You must remove that residual `.so` before the editable install takes effect.**

```bash
source /root/.venv/physics/bin/activate
rm -f /root/.venv/physics/lib/python3.10/site-packages/classy.cpython-*.so
cd /root/src/AxiCLASS/python
python setup.py build_ext --inplace --force
pip install --no-build-isolation -e . --force-reinstall
```

## Test

```bash
python -W ignore -c "
import classy
print('classy:', classy.__version__, classy.__file__)
cl = classy.Class(); cl.set({'output':'mPk'}); cl.compute()
print('LCDM compute OK; sigma8 =', round(cl.sigma8(), 4))
"
```

Expected:
```
classy: v3.3.0 /root/src/AxiCLASS/python/classy.cpython-310-x86_64-linux-gnu.so
LCDM compute OK; sigma8 = 0.8249
```

## What this does NOT fix

**AxiCLASS axion shooting failure for EDE configurations.** Setting `scf_potential = axion` with realistic EDE parameters (e.g., `fraction_axion_ac = 0.132`, `log10_axion_ac = -3.531`) currently fails with:

```
background_init(L:952) :condition (pba->shooting_failed == _TRUE_) is true;
Shooting failed, try optimising input_get_guess().
=>new_linearisation(L:998) :condition (funcreturn == _FAILURE_) is true;
Failure in ludcmp. Possibly singular matrix!
```

This is a separate convergence issue in `input_get_guess` that requires param-space-specific initial guesses. **TODO for Levier #1 12-param launch:** tune the `input_get_guess` defaults via the Cobaya YAML's `extra_args`, or use the alternative `m_axion`, `f_axion` parameterisation in `example_axiCLASS.ini` which bypasses shooting entirely. See `notes/levier1_README.md`.

## Path forward

1. Land this patch on the running Vast.ai instance (done, 2026-05-02).
2. For Levier #1 12-param production: tune EDE shooting initial guesses in the YAML. Likely add `m_axion: 1e4`, `f_axion: 0.1` as the "alternative" parameterisation in `example_axiCLASS.ini`, which avoids the shooting altogether.
3. Optionally: file an upstream issue at `PoulinV/AxiCLASS` proposing this tolerance fix as a portable change. The fix is harmless on architectures where the FP cancellation does not occur.
