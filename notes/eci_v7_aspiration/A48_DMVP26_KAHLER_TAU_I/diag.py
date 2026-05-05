"""Diagnostic: inspect M_u structure at best-fit and tau=i."""
import numpy as np
from numpy.linalg import svd, det
from kahler_tau_i import (build_Y_combinations, mass_matrix_up,
                           mass_matrix_down, C_BEST)

for tag, tau in [('best', 0.00455 + 1.00705j), ('tau=i', 1j)]:
    Mu = mass_matrix_up(tau, C_BEST)
    Md = mass_matrix_down(tau, C_BEST)
    print(f"\n=== {tag}    tau = {tau} ===")
    print("|M_u| =")
    print(np.abs(Mu))
    s = svd(Mu, compute_uv=False)
    s = np.sort(np.abs(s))[::-1]
    print(f"M_u SVs (desc): {s}")
    print(f"det(M_u) = {det(Mu):.4e}")
    print(f"|det| = {np.abs(det(Mu)):.4e}")
    print(f"product of SVs = {np.prod(s):.4e}")
    Y_uD, Y_u3, Y_dD, Y_d3 = build_Y_combinations(tau, C_BEST)
    print(f"|Y_uD| = {np.abs(Y_uD)}   arg = {np.angle(Y_uD, deg=True)}")
    print(f"|Y_u3| = {np.abs(Y_u3)}")
    sd = np.sort(np.abs(svd(Md, compute_uv=False)))[::-1]
    print(f"M_d SVs (desc): {sd}")
    print(f"|Y_dD| = {np.abs(Y_dD)}")
    print(f"|Y_d3| = {np.abs(Y_d3)}")
