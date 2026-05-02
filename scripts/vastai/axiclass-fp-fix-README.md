# AxiCLASS FP endpoint fix — apply, build, and test

## What this fixes

On AMD EPYC Zen 3 (Vast.ai instance type `epyc7v13`, and potentially
other architectures with different FP rounding), bare-default LCDM
fails immediately with:

```
Error in Class: thermodynamics_init(L:382) :error in thermodynamics_lists(...)
=>thermodynamics_lists(L:1146) :error in background_tau_of_z(...)
=>background_tau_of_z(L:285) :condition (z < pba->z_table[pba->bt_size-1]) is true;
   out of range: z=0.000000e+00 < z_min=6.661338e-16
```

The value `6.661338e-16 = 3 × DBL_EPSILON` identifies a floating-point
endpoint drift in the background module's `loga_table` array.

### Root cause

AxiCLASS wraps the entire background integration in a
`while (is_axion_converged == _FALSE_)` loop (absent in upstream
CLASS).  Inside that loop, `loga_table` is allocated and filled as:

```c
loga_table[i] = loga_ini + i * (loga_final - loga_ini) / (bt_size - 1);
```

In exact arithmetic, `i = bt_size - 1` gives `loga_final = 0.0`.  In
IEEE 754 double precision on Zen 3, the cancellation
`loga_ini + (large_integer × (-loga_ini)) / large_integer` produces
approximately `−3 × DBL_EPSILON` instead of `0`.  The
`background_sources` callback then stores:

```c
z_table[bt_size-1] = exp(-loga_table[bt_size-1]) - 1
                   ≈ exp(3e-16) - 1
                   ≈ 3×DBL_EPSILON = 6.66e-16
```

When `thermodynamics_lists` calls `background_tau_of_z(pba, 0.0)` for
the last row of the thermodynamics z-table, the guard

```c
class_test(z < pba->z_table[pba->bt_size-1], ...)
```

evaluates `0.0 < 6.66e-16 = TRUE` and aborts.

The bug is independent of compiler optimisation flags (`-O0`, `-O2`,
`-O3`, `-march=native`, `-ffast-math`).

Vanilla upstream CLASS 3.3.4 is not affected because it has no
`while`-loop wrapper and uses a single, fixed `loga_ini` whose
arithmetic happens to round differently.

### Fix

A one-liner that pins the last `loga_table` element to exactly
`loga_final` (= `0.0`) after the filling loop, before the evolver is
called.  This guarantees the today endpoint is architecturally exact
on all platforms and touches no EDE/axion code paths.

### Upstream commit status

The upstream `lesgourg/class_public` commit range v3.3.0→v3.3.4
(https://github.com/lesgourg/class_public/compare/v3.3.0...v3.3.4)
was inspected.  Background.c was only changed in commit `2e41ebd`
(adding `Omega_m(z)` / `Omega_r(z)` output columns) — not relevant.

The thermodynamics `break;` fix (upstream commit `c41f6d8`, "fixed
bug affecting tau_reio to z_reio conversion", verified at
https://github.com/lesgourg/class_public/commit/c41f6d8.patch) is
**already present** in AxiCLASS master and is not needed here.

**Conclusion: fix not located in upstream CLASS; Plan B one-liner
applied as described in the patch header.**

---

## Prerequisites

- AxiCLASS source tree checked out at `/root/src/AxiCLASS`
- GCC (any version ≥ 9), OpenMP, CFITSIO, FFTW3

---

## Apply the patch

```bash
# Dry-run first (safe — does not modify files):
patch -p1 --dry-run -l -d /root/src/AxiCLASS \
    < /root/crossed-cosmos/scripts/vastai/axiclass-fp-fix.patch

# If the dry-run reports "1 hunk succeeded", apply for real:
patch -p1 -l -d /root/src/AxiCLASS \
    < /root/crossed-cosmos/scripts/vastai/axiclass-fp-fix.patch
```

The `-l` flag enables whitespace-tolerant matching, which guards
against tab/space differences in the context lines.

Expected output:
```
patching file source/background.c
Hunk #1 succeeded at NNNN (offset N lines).
```

If the hunk fails (offset too large, or context mismatch), see
**Fallback: manual edit** below.

---

## Build

```bash
cd /root/src/AxiCLASS
make clean && make -j16 CC=gcc OPTFLAG="-O3 -fopenmp"
```

Typical build time on EPYC 7V13: ~25 s.

---

## Install the Python wrapper

```bash
cd /root/src/AxiCLASS/python
pip install --no-build-isolation -e . --force-reinstall
```

---

## Verify the fix

```bash
python -c "
import classy
cl = classy.Class()
cl.set({'output': 'mPk'})
cl.compute()
print('sigma8 =', cl.sigma8())
cl.struct_cleanup()
cl.empty()
"
```

Expected output (bare LCDM defaults):
```
sigma8 = 0.82...   # should be ≈ 0.825, matching upstream CLASS 3.3.4
```

A `sigma8` value in the range `0.82–0.84` confirms the fix is working.
Any `Error in Class` output means the patch did not apply correctly.

---

## Quick EDE smoke test

After confirming LCDM works, run a minimal EDE parameter set:

```bash
python -c "
import classy
cl = classy.Class()
cl.set({
    'output': 'tCl,mPk',
    'f_ede': 0.1,
    'log10z_c': 3.56,
    'thetai_scf': 2.83,
    'scf_potential': 'axion',
    'scf_parameters': '2,0,0,1',
    'n_axion': 3,
    'Omega_Lambda': 0,
    'Omega_fld': 0,
    'h': 0.72,
    'omega_b': 0.02242,
    'omega_cdm': 0.1193,
})
cl.compute()
print('EDE sigma8 =', cl.sigma8())
cl.struct_cleanup()
cl.empty()
"
```

---

## Fallback: manual edit

If `patch` fails due to line-number drift from subsequent commits,
apply the fix by hand.  Open `source/background.c` and search for the
unique string:

```
// is_axion_converged = _TRUE_;
```

The line immediately above that comment is the closing `}` of the
`loga_table` filling loop.  Insert this line **between** that `}`
and the `// is_axion_converged` comment:

```c
   pba->loga_table[pba->bt_size-1] = loga_final;
```

The patched block should look like:

```c
   for (index_loga=0; index_loga<pba->bt_size; index_loga++) {
     pba->loga_table[index_loga] = loga_ini + index_loga*(loga_final-loga_ini)/(pba->bt_size-1);
     used_in_output[index_loga] = 1;
   }
   /* Pin the today endpoint to exactly loga_final (=0.0) to prevent FP
    * cancellation from producing a slightly negative value.  Without this,
    * background_sources stores z_table[bt_size-1] = exp(-eps)-1 ~ 3*DBL_EPSILON
    * rather than 0, causing background_tau_of_z to reject z=0 from
    * thermodynamics_lists (observed on EPYC Zen3, independent of -O level). */
   pba->loga_table[pba->bt_size-1] = loga_final;

  // is_axion_converged = _TRUE_;
  /** - perform the integration */
  class_call(generic_evolver(background_derivs,
```

---

## Notes

- The fix does not change any numerical results — it only ensures the
  pre-computed table endpoint is exactly representable as 0.0.
- The fix is safe to re-apply after `git pull` of AxiCLASS; no
  conflicts with EDE-specific code are expected.
- Tested scenario: bare LCDM (`output: mPk`) and EDE axion potential.
  MCMC use (MontePython + AxiCLASS + NMC quintessence) should behave
  identically to the unfixed code on architectures where the FP
  arithmetic happens to round correctly.
