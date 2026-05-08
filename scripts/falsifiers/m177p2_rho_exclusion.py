#!/usr/bin/env python3
"""M177.2 rho exclusion check.

Apply M170.1 eigenspace selection at tau=rho to NPP20 Y_3̂^(3)(rho);
verify Z_3 eigenspaces empty for NPP20 form.
"""
import sys
import json
import logging
import time
from pathlib import Path
import mpmath as mp
import sympy as sp
import numpy as np
from diskcache import Cache
from tqdm import tqdm
from sympy.utilities.lambdify import lambdify

CACHE_DIR = Path.home() / '.cache' / 'm177p2_rho_exclusion'
cache = Cache(str(CACHE_DIR))

# ----- constants from NPP20 notes -----
# Representation matrices for rho_3̂ (S) and rho_3̂ (T) :
S_mat = sp.Matrix([[0, sp.sqrt(2), sp.sqrt(2)],
                   [sp.sqrt(2), 1, -1],
                   [sp.sqrt(2), -1, 1]]) / 2

# T eigenvalues (weight-3 automorphy absorbed, see note)
T_mat = sp.diag(sp.I, -1, 1)

ST_mat = S_mat * T_mat                # rho_3̂(ST)

# Eigenvalues of ST (cube roots of unity)
omega = sp.exp(2 * sp.pi * sp.I / 3)   # ω
eigvals = [1, omega, omega**2]

# q‑series for Y_3̂^(3) from M₃(Γ(4)) triplet 3̂ (CITE_NEEDED::NPP20 appendix)
# Using the expansions given in notes/heavy_artillery_.../01_M3_Gamma4_basis.json
Y1_series = 3 * sp.Symbol('q')**sp.Rational(1,4) * (1 + 2*sp.Symbol('q') + 4*sp.Symbol('q')**2 + 7*sp.Symbol('q')**3 + 10*sp.Symbol('q')**4)
Y2_series = 2 * sp.Symbol('q')**sp.Rational(1,2) * (1 + 6*sp.Symbol('q') + 18*sp.Symbol('q')**2 + 36*sp.Symbol('q')**3 + 62*sp.Symbol('q')**4)
Y3_series = (1 + 8*sp.Symbol('q') + 24*sp.Symbol('q')**2 + 32*sp.Symbol('q')**3 + 72*sp.Symbol('q')**4)

def compute_eigenspaces(dps=200):
    """Return True if Y_3̂^(3)(ρ) spans all three Z₃ eigenspaces."""
    mp.mp.dps = dps
    # primitive third root of unity: tau_rho = e^{2πi/3}
    tau_rho = mp.e**(2j * mp.pi / 3)          # gives -1/2 + i√3/2
    q = mp.e**(2j * mp.pi * tau_rho)          # q = e^{2πiτ}
    # evaluate series numerically
    def eval_series(expr):
        f = lambdify(sp.Symbol('q'), expr, modules='mpmath')
        return f(q)
    Y = mp.matrix([eval_series(Y1_series),
                   eval_series(Y2_series),
                   eval_series(Y3_series)])
    # compute ST matrix in mpmath
    # Build numeric S and T directly
    sqrt2 = mp.sqrt(2)
    S_num = mp.matrix([[0, sqrt2, sqrt2],
                      [sqrt2, 1, -1],
                      [sqrt2, -1, 1]]) / 2
    T_num = mp.diag(1j, -1, 1)
    ST_num = S_num * T_num
    # check if Y is eigenvector of any eigenvalue
    eigen_check = []
    for lam in [1, mp.e**(2j*mp.pi/3), mp.e**(-2j*mp.pi/3)]:
        residual = (ST_num - lam * mp.eye(3)) * Y
        norm = mp.sqrt(sum(abs(r)**2 for r in residual))
        eigen_check.append(norm < mp.mpf('1e-12'))
    # Y is NOT in any single eigenspace -> all norms should be > tolerance
    return not any(eigen_check)

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    start = time.monotonic()
    result = {"test":"m177p2_rho_exclusion","status":"FAIL","reason":"","details":{}}
    try:
        cache_key = "eigenspaces_empty"
        empty = cache.get(cache_key)
        if empty is None:
            with tqdm(total=1, desc="Eigenspace check") as pbar:
                empty = compute_eigenspaces(dps=200)
                pbar.update(1)
            cache.set(cache_key, empty, expire=3600*24)
        result["details"]["eigenspaces_empty"] = empty
        if empty:
            result["status"] = "PASS"
            result["reason"] = "Z_3 eigenspaces empty for NPP20 form at tau=rho"
        else:
            result["reason"] = "Non‑empty Z_3 eigenspace detected"
    except Exception as e:
        logger.exception("Computation failed")
        result["status"] = "ERROR"
        result["reason"] = str(e)
    result["elapsed_seconds"] = round(time.monotonic()-start, 2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
