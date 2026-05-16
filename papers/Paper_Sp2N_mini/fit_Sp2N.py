#!/usr/bin/env python3
"""Fit the conjectured one-parameter glueball mass ansatz to lattice data.

Sp(2N): F_Sp(N) = (1+c/N)/(1+c/3) for m_0++(N) / m_0++(3).
SU(N) : F_SU(N) = (1+c'/N^2)/(1+c'/9) for m_0++(N) / m_0++(3).

Sources
-------
Sp(2N) data : Bennett et al. PRD 103, 054509 (2021)  arXiv:2010.15781  Table IV.
SU(N)  data : Athenodorou & Teper JHEP 12 (2021) 082 arXiv:2106.00364  Tables 34, 35, 38.

Author: K. Remondiere (ECI/YM project), 2026-05-16.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Sp(2N) continuum-extrapolated 0++ ground-state masses, m / sqrt(sigma).
# Table IV of Bennett et al. 2021 (arXiv:2010.15781). N = 1..4 + large-N.
# ---------------------------------------------------------------------------
N_Sp        = np.array([1.0, 2.0, 3.0, 4.0])
m_Sp        = np.array([3.841, 3.577, 3.430, 3.308])   # m/sqrt(sigma)
dm_Sp       = np.array([0.084, 0.049, 0.075, 0.098])
m_Sp_inf    = 3.241
dm_Sp_inf   = 0.088

# ---------------------------------------------------------------------------
# SU(N) continuum-extrapolated 0++ ground-state masses, m / sqrt(sigma).
# Tables 34 & 35 of Athenodorou & Teper 2021 (arXiv:2106.00364).
# ---------------------------------------------------------------------------
N_SU        = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0])
m_SU        = np.array([3.781, 3.405, 3.271, 3.156, 3.102, 3.099, 3.102, 3.151])
dm_SU       = np.array([0.023, 0.021, 0.027, 0.031, 0.032, 0.026, 0.037, 0.033])
m_SU_inf    = 3.072
dm_SU_inf   = 0.014


def F_Sp(N: np.ndarray, c: float) -> np.ndarray:
    """Linear-in-1/N ansatz, normalised so F_Sp(3) = 1."""
    return (1.0 + c / N) / (1.0 + c / 3.0)


def F_SU(N: np.ndarray, c: float) -> np.ndarray:
    """Quadratic-in-1/N ansatz, normalised so F_SU(3) = 1."""
    return (1.0 + c / N**2) / (1.0 + c / 9.0)


def fit_F(Nvals: np.ndarray, mvals: np.ndarray, dmvals: np.ndarray,
          F: callable, m3_ref: float, dm3_ref: float) -> tuple:
    """Fit F(N; c) to lattice ratios, propagating m_0++(3) error in quadrature."""
    y  = mvals / m3_ref
    # Independent-error propagation for the ratio
    dy = np.sqrt((dmvals / m3_ref)**2 + (mvals * dm3_ref / m3_ref**2)**2)
    popt, pcov = curve_fit(F, Nvals, y, sigma=dy, absolute_sigma=True, p0=[0.5])
    c     = popt[0]
    dc    = float(np.sqrt(pcov[0, 0]))
    resid = (y - F(Nvals, c)) / dy
    chi2  = float(np.sum(resid**2))
    dof   = len(Nvals) - 1
    return c, dc, chi2, dof


def main() -> None:
    # Sp(2N): anchor on the SU(2) ~ Sp(2) point (N=1) since we have it,
    # then fit the (N >= 2) data with normalisation m_0++(N=3).
    m3_Sp, dm3_Sp = m_Sp[2], dm_Sp[2]
    c_Sp, dc_Sp, chi2_Sp, dof_Sp = fit_F(N_Sp, m_Sp, dm_Sp,
                                         F_Sp, m3_Sp, dm3_Sp)

    # Predicted large-N limit from the fit, in m/sqrt(sigma) units.
    m_Sp_inf_pred  = m3_Sp / (1.0 + c_Sp / 3.0)
    dm_Sp_inf_pred = np.hypot(dm3_Sp / (1.0 + c_Sp / 3.0),
                              m3_Sp * dc_Sp / (3.0 * (1.0 + c_Sp / 3.0)**2))

    # SU(N): same normalisation (N=3) since SU(3) is the QCD anchor.
    m3_SU, dm3_SU = m_SU[1], dm_SU[1]
    c_SU, dc_SU, chi2_SU, dof_SU = fit_F(N_SU, m_SU, dm_SU,
                                         F_SU, m3_SU, dm3_SU)
    m_SU_inf_pred  = m3_SU / (1.0 + c_SU / 9.0)
    dm_SU_inf_pred = np.hypot(dm3_SU / (1.0 + c_SU / 9.0),
                              m3_SU * dc_SU / (9.0 * (1.0 + c_SU / 9.0)**2))

    print("=" * 72)
    print(" Sp(2N) one-parameter fit:  F_Sp(N) = (1 + c/N) / (1 + c/3)")
    print("=" * 72)
    print(f"  c              = {c_Sp:.3f} +/- {dc_Sp:.3f}")
    print(f"  chi^2/dof      = {chi2_Sp:.2f}/{dof_Sp}")
    print(f"  m_0++(N=inf) predicted = {m_Sp_inf_pred:.3f} +/- {dm_Sp_inf_pred:.3f}")
    print(f"  m_0++(N=inf) lattice   = {m_Sp_inf:.3f} +/- {dm_Sp_inf}")
    print()
    print("=" * 72)
    print(" SU(N) one-parameter fit:   F_SU(N) = (1 + c/N^2) / (1 + c/9)")
    print("=" * 72)
    print(f"  c              = {c_SU:.3f} +/- {dc_SU:.3f}")
    print(f"  chi^2/dof      = {chi2_SU:.2f}/{dof_SU}")
    print(f"  m_0++(N=inf) predicted = {m_SU_inf_pred:.3f} +/- {dm_SU_inf_pred:.3f}")
    print(f"  m_0++(N=inf) lattice   = {m_SU_inf:.3f} +/- {dm_SU_inf}")
    print()
    print("Residuals (Sp):", (m_Sp / m3_Sp - F_Sp(N_Sp, c_Sp)))
    print("Residuals (SU):", (m_SU / m3_SU - F_SU(N_SU, c_SU)))


if __name__ == "__main__":
    main()
