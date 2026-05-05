"""
A48 — Test dMVP26 (arXiv:2604.01422) Kahler-canonical hierarchy mechanism
when tau is pinned at the CP fix-point tau = i (instead of best-fit
tau = 0.00455 + 1.00705 i).

Strategy:
  1. Reconstruct the published superpotential / Kahler structure (Eqs 14-21).
  2. Build modular forms at tau = i from Jacoby theta-constants
     (Eqs 26-33: theta(tau), epsilon(tau), q4 = exp(i pi tau / 2)).
  3. Plug the published O(1) coefficients C1..C7 from Table 4.
  4. Compare three configurations:
       (a) Authors' best fit  tau = 0.00455 + 1.00705 i  (sanity check)
       (b) Pinned             tau = i exactly             (ECI v7.4 desideratum)
       (c) Authors' nearby    tau = 0       + 1.00705 i  (J_CP -> 0 limit)
  5. Diagonalise M_u, M_d via singular values; report y_u/y_c, y_c/y_t,
     y_d/y_s, y_s/y_b vs PDG-2024 GUT-scale targets.

References:
  * dMVP26      = arXiv:2604.01422 (de Medeiros Varzielas - Paiva, Apr 2026)
  * AHS         = arXiv:2510.01312 (Antusch - Hinze - Saad, GUT-scale running)
  * Theta basis = Novichkov-Penedo-Petcov NPB 963 (2021), arXiv:2006.03058 [10]
"""

import numpy as np
import sympy as sp
from numpy.linalg import svd

# --------------------------------------------------------------------------
# Modular forms of S'_4 (level 4) — from dMVP26 App A.2 and NPP21
# Variable q4 = exp(i pi tau / 2)
# theta(tau) = 1 + 2 q4^4 + 2 q4^16 + ...   (theta_3(0|2 tau))
# epsilon(tau) = 2 q4 + 2 q4^9 + 2 q4^25 + ... (theta_2(0|2 tau))
# --------------------------------------------------------------------------

def theta_eps(tau, n_terms=80):
    """Compute theta(tau), epsilon(tau) as truncated series in q4."""
    q4 = np.exp(1j * np.pi * tau / 2.0)
    th = 1.0 + 0.0j
    ep = 0.0 + 0.0j
    for n in range(1, n_terms):
        # theta has powers 4 n^2: 4, 16, 36, 64, ...
        th += 2.0 * q4 ** (4 * n * n)
        # epsilon has powers (2n-1)^2: 1, 9, 25, 49, ...
        ep += 2.0 * q4 ** ((2 * n - 1) ** 2)
    return th, ep

# --------------------------------------------------------------------------
# Modular multiplets used in dMVP26 (App A.2, Eqs 28-33)
# --------------------------------------------------------------------------

def Y3_hat_w1(tau):
    """Y^(1)_{3-hat} : weight 1 triplet of double cover."""
    th, ep = theta_eps(tau)
    return np.array([np.sqrt(2.0) * ep * th,
                     ep ** 2,
                     -th ** 2], dtype=complex)

def Y3p_w6_1(tau):
    th, ep = theta_eps(tau)
    a = -3.0 / (8.0 * np.sqrt(13.0)) * (th ** 12 - 3.0 * ep ** 4 * th ** 8
                                        + 3.0 * ep ** 8 * th ** 4 - ep ** 12)
    b = 3.0 * np.sqrt(2.0) / np.sqrt(13.0) * (3.0 * ep ** 5 * th ** 7 + ep ** 9 * th ** 3)
    c = 3.0 * np.sqrt(2.0) / np.sqrt(13.0) * (ep ** 3 * th ** 9 + 3.0 * ep ** 7 * th ** 5)
    return np.array([a, b, c], dtype=complex)

def Y3p_w6_2(tau):
    th, ep = theta_eps(tau)
    a = 3.0 * (ep ** 4 * th ** 8 - ep ** 8 * th ** 4)
    b = -3.0 / (4.0 * np.sqrt(2.0)) * (ep * th ** 11 + 2.0 * ep ** 5 * th ** 7
                                       - 3.0 * ep ** 9 * th ** 3)
    c = 3.0 / (4.0 * np.sqrt(2.0)) * (3.0 * ep ** 3 * th ** 9 - 2.0 * ep ** 7 * th ** 5
                                      - ep ** 11 * th)
    return np.array([a, b, c], dtype=complex)

def Y3p_w10_1(tau):
    th, ep = theta_eps(tau)
    a = -3.0 / (32.0 * np.sqrt(29.0)) * (th ** 20 + 59.0 * ep ** 4 * th ** 16
                                         - 182.0 * ep ** 8 * th ** 12
                                         + 182.0 * ep ** 12 * th ** 8
                                         - 59.0 * ep ** 16 * th ** 4 - ep ** 20)
    b = 3.0 * np.sqrt(2.0 / 29.0) * (13.0 * ep ** 9 * th ** 11 + 2.0 * ep ** 13 * th ** 7
                                     + ep ** 17 * th ** 3)
    c = 3.0 * np.sqrt(2.0 / 29.0) * (ep ** 3 * th ** 17 + 2.0 * ep ** 7 * th ** 13
                                     + 13.0 * ep ** 11 * th ** 9)
    return np.array([a, b, c], dtype=complex)

def Y3p_w10_2(tau):
    th, ep = theta_eps(tau)
    a = 36.0 / np.sqrt(13.0) * (ep ** 8 * th ** 12 - ep ** 12 * th ** 8)
    b = -9.0 / (16.0 * np.sqrt(26.0)) * (ep * th ** 19 + 20.0 * ep ** 5 * th ** 15
                                         + 14.0 * ep ** 9 * th ** 11
                                         - 28.0 * ep ** 13 * th ** 7
                                         - 7.0 * ep ** 17 * th ** 3)
    c = 9.0 / (16.0 * np.sqrt(26.0)) * (7.0 * ep ** 3 * th ** 17 + 28.0 * ep ** 7 * th ** 13
                                        - 14.0 * ep ** 11 * th ** 9
                                        - 20.0 * ep ** 15 * th ** 5
                                        - ep ** 19 * th)
    return np.array([a, b, c], dtype=complex)

def Y3p_w10_3(tau):
    th, ep = theta_eps(tau)
    a = 9.0 / 8.0 * (ep ** 4 * th ** 16 - 3.0 * ep ** 8 * th ** 12
                     + 3.0 * ep ** 12 * th ** 8 - ep ** 16 * th ** 4)
    b = 9.0 / (8.0 * np.sqrt(2.0)) * (ep ** 5 * th ** 15 - 3.0 * ep ** 9 * th ** 11
                                      + 3.0 * ep ** 13 * th ** 7 - ep ** 17 * th ** 3)
    c = -9.0 / (8.0 * np.sqrt(2.0)) * (ep ** 3 * th ** 17 - 3.0 * ep ** 7 * th ** 13
                                       + 3.0 * ep ** 11 * th ** 9 - ep ** 15 * th ** 5)
    return np.array([a, b, c], dtype=complex)

# --------------------------------------------------------------------------
# Mass matrices (dMVP26 Eqs 20, 21).
# Ordering of triplets:
#   row index of Q (alpha_2)  -> components labelled 1,2,3
#   contraction (qD QY)_1 with C-G (Eqs 18, 24-25)
# We build Y_{uD}, Y_{u3}, Y_{dD}, Y_{d3} as 3-vectors (Y_1, Y_2, Y_3),
# then assemble the explicit mass matrices from Eqs 20, 21.
# --------------------------------------------------------------------------

def build_Y_combinations(tau, C):
    """Return Y_uD (vec3), Y_u3 (vec3), Y_dD (vec3), Y_d3 (vec3)."""
    C1, C2, C3, C4, C5, C6, C7 = C
    Y61 = Y3p_w6_1(tau)
    Y62 = Y3p_w6_2(tau)
    Y_uD = C1 * Y61 + C2 * Y62          # weight-6 triplet  (u^c sector)
    Y_hat = Y3_hat_w1(tau)              # weight-1 triplet-hat (t^c sector)
    Y_u3 = C3 * Y_hat                   # C_{u3,1} = C3
    Y101 = Y3p_w10_1(tau)
    Y102 = Y3p_w10_2(tau)
    Y103 = Y3p_w10_3(tau)
    Y_dD = C3 * Y101 + C4 * Y102 + C5 * Y103   # C_{dD,1} = C3 (constraint)
    Y_d3 = C6 * Y61 + C7 * Y62                 # weight-6 triplet (b^c sector)
    return Y_uD, Y_u3, Y_dD, Y_d3

def diag_kahler_factors(tau, k_list):
    """diag( (2 Im tau)^{k_i / 2} )^{-1}  i.e.  (2 Im tau)^{-k_i/2}.
       In dMVP26 Eqs 20-21 the prefactors come in as (2 Im tau)^{-k/2}
       absorbed in front of each row. We return the diag of these factors."""
    return np.diag([(2.0 * tau.imag) ** (k / 2.0) for k in k_list])

def mass_matrix_up(tau, C, vu=1.0):
    """Construct M_u as in dMVP26 Eq 20 (overall vu/sqrt(6) prefactor)."""
    Y_uD, Y_u3, _, _ = build_Y_combinations(tau, C)
    YuD1, YuD2, YuD3 = Y_uD
    # Yukawa block (the right matrix in Eq 20)
    sqrt3o2 = np.sqrt(3.0) / 2.0
    half = 0.5
    Y_block = np.array([
        [0.0,                sqrt3o2 * YuD2,            sqrt3o2 * YuD3],
        [-YuD1,             half * YuD2,                half * YuD3],
        [Y_u3[0],           Y_u3[2],                    Y_u3[1]],
    ], dtype=complex)
    # Kahler diagonal from row weights k_uD = -6, t^c weight = -1
    # The (2 Im tau) prefactors in Eq 20:  diag( (2Im)^-3, (2Im)^-3, (2Im)^-1/2 )
    Im2 = 2.0 * tau.imag
    K_left = np.diag([Im2 ** (-3.0), Im2 ** (-3.0), Im2 ** (-0.5)])
    return (vu / np.sqrt(6.0)) * (K_left @ Y_block)

def mass_matrix_down(tau, C, vd=1.0):
    """Construct M_d as in dMVP26 Eq 21."""
    _, _, Y_dD, Y_d3 = build_Y_combinations(tau, C)
    YdD1, YdD2, YdD3 = Y_dD
    sqrt3o2 = np.sqrt(3.0) / 2.0
    half = 0.5
    Y_block = np.array([
        [0.0,                sqrt3o2 * YdD2,            sqrt3o2 * YdD3],
        [-YdD1,             half * YdD2,                half * YdD3],
        [Y_d3[0],           Y_d3[2],                    Y_d3[1]],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K_left = np.diag([Im2 ** (-5.0), Im2 ** (-5.0), Im2 ** (-3.0)])
    return (vd / np.sqrt(6.0)) * (K_left @ Y_block)

def yukawa_ratios(M):
    """Return (m1/m2, m2/m3) from a 3x3 mass matrix via singular values."""
    s = svd(M, compute_uv=False)
    s = np.sort(s)[::-1]   # m_top, m_charm, m_up
    return s[2] / s[1], s[1] / s[0]

# --------------------------------------------------------------------------
# Authors' published best-fit constants (Table 4)
# --------------------------------------------------------------------------
C_BEST = (-0.3951, +0.2181, +3.7065, +1.0452, +5.5783, +1.3828, +0.3861)

# PDG-2024 GUT-scale targets (dMVP26 Table 4 / AHS arXiv:2510.01312)
TARGET = {
    'yu/yc':  1.986e-3,
    'yc/yt':  2.810e-3,
    'yd/ys':  5.000e-2,
    'ys/yb':  1.782e-2,
}

CASES = {
    'best':       0.00455 + 1.00705j,
    'tau=i':      0.0     + 1.0j,
    'Re=0,Im=fit':0.0     + 1.00705j,
}

def report():
    print("=" * 78)
    print("A48  dMVP26 Kahler hierarchy at tau = i  (ECI v7.4 graft test)")
    print("=" * 78)
    for tag, tau in CASES.items():
        Mu = mass_matrix_up(tau, C_BEST, vu=1.0)
        Md = mass_matrix_down(tau, C_BEST, vd=1.0)
        yu_yc, yc_yt = yukawa_ratios(Mu)
        yd_ys, ys_yb = yukawa_ratios(Md)
        print(f"\n--- {tag}    tau = {tau} ---")
        print(f"  y_u/y_c = {yu_yc:.3e}   target {TARGET['yu/yc']:.3e}"
              f"   ratio = {yu_yc / TARGET['yu/yc']:.2f}")
        print(f"  y_c/y_t = {yc_yt:.3e}   target {TARGET['yc/yt']:.3e}"
              f"   ratio = {yc_yt / TARGET['yc/yt']:.2f}")
        print(f"  y_d/y_s = {yd_ys:.3e}   target {TARGET['yd/ys']:.3e}"
              f"   ratio = {yd_ys / TARGET['yd/ys']:.2f}")
        print(f"  y_s/y_b = {ys_yb:.3e}   target {TARGET['ys/yb']:.3e}"
              f"   ratio = {ys_yb / TARGET['ys/yb']:.2f}")
        # Jarlskog proxy:  Im(det(Mu Mu^dag, Md Md^dag) commutator) sign
        # Cheap proxy: Im( tr( (Mu @ Mu.conj().T) @ (Md @ Md.conj().T) )^3 ) -- skip
        # Just print Re(tau) deviation
        print(f"  Re(tau) - 0 = {tau.real:+.5f}   (J_CP proxy ~ Re(tau))")
    print()
    print("Note: with strictly real C_i and tau on imaginary axis, ALL Yukawas")
    print("become real (gCP unbroken) and J_CP = 0. CKM mixing magnitudes still")
    print("nontrivial — angles set by triplet ratios at tau=i.")


if __name__ == "__main__":
    report()
