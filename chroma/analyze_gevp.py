#!/usr/bin/env python3
"""
CHROMA SU(2) Glueball GEVP Analysis
Reads Chroma HDF5 correlator output, extracts m_0++/sqrt(sigma).
Reference: Athenodorou-TePer 2021 (arXiv:2106.00364), LT JHEP 08(2010)119
"""
import numpy as np
import sys, os, json
from pathlib import Path

def effective_mass(corr, t):
    """m_eff(t) = ln(C(t)/C(t+1))"""
    if corr[t+1] <= 0 or corr[t] <= 0:
        return np.nan
    return np.log(corr[t] / corr[t+1])

def plateau_fit(m_eff, t_start, t_end):
    """Constant fit to effective mass plateau."""
    vals = m_eff[t_start:t_end+1]
    vals = vals[~np.isnan(vals)]
    if len(vals) < 2:
        return np.nan, np.nan
    m = np.mean(vals)
    e = np.std(vals) / np.sqrt(len(vals))
    return m, e

def solve_gevp(corr_matrix, t0=0):
    """
    Solve generalized eigenvalue problem C(t) v = λ C(t0) v.
    Returns principal correlator λ_0(t).
    """
    nt = corr_matrix.shape[0]
    C0 = corr_matrix[t0]
    # Regularize
    C0 += 1e-10 * np.eye(len(C0))
    
    lam_0 = np.zeros(nt)
    for t in range(nt):
        try:
            Ct = corr_matrix[t]
            # Symmetrize
            Ct = 0.5 * (Ct + Ct.T)
            eigvals = eigh(Ct, C0, eigvals_only=True)
            lam_0[t] = eigvals[0]  # ground state
        except:
            lam_0[t] = np.nan
    return lam_0

def main():
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 2.40
    
    print(f"=== GEVP Analysis β={beta} ===")
    print(f"Framework: Theorem C.6 ECI v15")
    print(f"Target: m_0++/sqrt(σ) ≈ 3.78 (Lucini-TePer 2010)")
    print(f"Alt ref: m_0++/sqrt(σ) ≈ 3.56(11) (Athenodorou-TePer 2021, SU(2))")
    print()
    
    # Placeholder — real analysis reads HDF5 from Chroma output
    # When flow data exists, this will:
    # 1. Load HDF5 correlator data for each irrep (A1g, Eg, T2g)
    # 2. Build correlation matrix C_ij(t) over operator basis
    # 3. Solve GEVP → principal correlator λ_0(t)
    # 4. Extract effective mass plateau → a*m_0++
    # 5. Fit static potential from Wilson loops → a*sqrt(σ)
    # 6. Form dimensionless ratio m_0++/sqrt(σ)
    
    result = {
        "protocol": "M47_D1 consolidated",
        "beta": beta,
        "lattice": "16^4",
        "action": "SU(2) Wilson",
        "reference_lt2010": 3.78,
        "reference_at2021": 3.56,
        "status": "PENDING_DATA",
        "note": "Real analysis runs when Chroma HDF5 output exists"
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
