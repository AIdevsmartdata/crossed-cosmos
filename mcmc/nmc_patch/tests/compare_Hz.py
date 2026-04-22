#!/usr/bin/env python3
"""Smoke test: fractional H(z) agreement between NMC(xi=0) and quintessence_monomial."""
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "hi_class_nmc" / "output"
nmc = np.loadtxt(ROOT / "nmc_zero_00_background.dat")
van = np.loadtxt(ROOT / "vanilla_00_background.dat")
zN, HN = nmc[:, 0], nmc[:, 3]
zV, HV = van[:, 0], van[:, 3]
# Interpolate on a common z-grid in [0, 1000] (note columns are sorted descending in z).
zmax = 1000.0
mask = (zN >= 0.0) & (zN <= zmax)
HVi = np.interp(zN[mask][::-1], zV[::-1], HV[::-1])[::-1]
frac = np.abs(HN[mask] - HVi) / HVi
print(f"npts in z in [0,{zmax}]: {mask.sum()}")
print(f"max  |dH|/H = {frac.max():.3e}")
print(f"mean |dH|/H = {frac.mean():.3e}")
print(f"at z=0:   H_nmc={HN[mask][-1]:.8e}  H_van={HVi[-1]:.8e}")
ok = frac.max() < 1e-4
print("PASS" if ok else "FAIL", "(threshold 1e-4)")
raise SystemExit(0 if ok else 1)
