"""
A63 — Fix the x90 normalisation/structural gap in A48 dMVP26 reconstruction.

Reference: dMVP26 = arXiv:2604.01422 (de Medeiros Varzielas - Paiva, Apr 2026)
Verified live 2026-05-05 from the live PDF: pages 5-7 (Eqs 16-21, 24, 28-33).

A48 baseline produces y_u/y_c = 1.79e-1 vs PDG 1.99e-3 (ratio x90).

After comparing the running code in A48/kahler_tau_i.py to the verbatim
Eqs 18, 20, 21, 24 in the PDF, the discrepancy is a STRUCTURAL TRANSCRIPTION
BUG in the explicit Yukawa block, NOT a Kahler normalisation issue.

Eq 24 (verbatim, p. 11):

    (alpha1)         (beta1)        (    -alpha2 * beta1                              )
    (      )_2  ⊗   (beta2)_3  ⊃  ( sqrt(3)/2 * alpha1*beta3 + 1/2 * alpha2*beta2  )
    (alpha2)         (beta3)        ( sqrt(3)/2 * alpha1*beta2 + 1/2 * alpha2*beta3  )

Note the SWAP of beta3 and beta2 between the second and third components.

Eq 20 (verbatim, p. 6):

    M_u = (vu/sqrt(6)) * diag((2 Im tau)^-3, (2 Im tau)^-3, (2 Im tau)^-1/2) *
          [[ 0,        sqrt(3)/2 * Y_uD,2,   sqrt(3)/2 * Y_uD,3 ],
           [ -Y_uD,1,  1/2 * Y_uD,3,         1/2 * Y_uD,2       ],
           [ Y_u3,1,   Y_u3,3,               Y_u3,2             ]]

The current A48 code uses for row 2:

    [-YuD1,  1/2 * YuD2,  1/2 * YuD3]

i.e. it does NOT swap YuD2 <-> YuD3 in cols 2 and 3 of row 2.
That is Eq 24's signature swap (alpha2*beta2 in col 2, alpha2*beta3 in col 3
*coupled with* alpha1*beta3 in col 2, alpha1*beta2 in col 3).

In M_u as an explicit (Q_a, q^c_b) matrix the beta_i are still the modular
form components (which keep their own labelling), so the index-swap of
the C-G must show up explicitly in the matrix. The Y_u3 row already has
this swap (cols (1,3,2)); paper has it in BOTH the YuD-rows row1 (no
swap, fine) AND row2 (swap), AND the Y_u3 row (swap).

The bug: A48 swapped only Y_u3 row, forgot to swap YuD-row2.

Same bug in M_d (row 2 has (1/2*YdD2, 1/2*YdD3) instead of (1/2*YdD3, 1/2*YdD2)).

This script:
  1. Reproduces the A48 buggy result (sanity).
  2. Patches Eq 20/21 row 2 cols 2<->3.
  3. Tries other conventions (sign flip on -Y_uD,1, alternative C-G sign)
     as defensive checks.
  4. Reports y_u/y_c, y_c/y_t, y_d/y_s, y_s/y_b for each variant at:
       (a) author best-fit  tau = 0.00455 + 1.00705 i
       (b) tau = i (CM-anchor)
"""

import numpy as np
from numpy.linalg import svd

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..',
                                 'A48_DMVP26_KAHLER_TAU_I'))
from kahler_tau_i import (build_Y_combinations, C_BEST, TARGET, theta_eps,
                          Y3_hat_w1, Y3p_w6_1, Y3p_w6_2,
                          Y3p_w10_1, Y3p_w10_2, Y3p_w10_3)


# -------------------- Variant builders --------------------
def Mu_buggy(tau, C, vu=1.0):
    """A48 reconstruction (the buggy one)."""
    Y_uD, Y_u3, _, _ = build_Y_combinations(tau, C)
    YuD1, YuD2, YuD3 = Y_uD
    s32 = np.sqrt(3.0) / 2.0
    Y_block = np.array([
        [0.0,        s32 * YuD2,  s32 * YuD3],
        [-YuD1,      0.5 * YuD2,  0.5 * YuD3],   # BUG: should be YuD3, YuD2
        [Y_u3[0],    Y_u3[2],     Y_u3[1]   ],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K = np.diag([Im2 ** -3.0, Im2 ** -3.0, Im2 ** -0.5])
    return (vu / np.sqrt(6.0)) * (K @ Y_block)


def Mu_fixed(tau, C, vu=1.0):
    """Eq 20 verbatim (row 2 cols 2<->3 swapped to match Eq 24)."""
    Y_uD, Y_u3, _, _ = build_Y_combinations(tau, C)
    YuD1, YuD2, YuD3 = Y_uD
    s32 = np.sqrt(3.0) / 2.0
    Y_block = np.array([
        [0.0,        s32 * YuD2,  s32 * YuD3],
        [-YuD1,      0.5 * YuD3,  0.5 * YuD2],   # FIX: Eq 20 verbatim
        [Y_u3[0],    Y_u3[2],     Y_u3[1]   ],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K = np.diag([Im2 ** -3.0, Im2 ** -3.0, Im2 ** -0.5])
    return (vu / np.sqrt(6.0)) * (K @ Y_block)


def Md_buggy(tau, C, vd=1.0):
    _, _, Y_dD, Y_d3 = build_Y_combinations(tau, C)
    YdD1, YdD2, YdD3 = Y_dD
    s32 = np.sqrt(3.0) / 2.0
    Y_block = np.array([
        [0.0,        s32 * YdD2,  s32 * YdD3],
        [-YdD1,      0.5 * YdD2,  0.5 * YdD3],   # BUG
        [Y_d3[0],    Y_d3[2],     Y_d3[1]   ],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K = np.diag([Im2 ** -5.0, Im2 ** -5.0, Im2 ** -3.0])
    return (vd / np.sqrt(6.0)) * (K @ Y_block)


def Md_fixed(tau, C, vd=1.0):
    """Eq 21 verbatim."""
    _, _, Y_dD, Y_d3 = build_Y_combinations(tau, C)
    YdD1, YdD2, YdD3 = Y_dD
    s32 = np.sqrt(3.0) / 2.0
    Y_block = np.array([
        [0.0,        s32 * YdD2,  s32 * YdD3],
        [-YdD1,      0.5 * YdD3,  0.5 * YdD2],   # FIX
        [Y_d3[0],    Y_d3[2],     Y_d3[1]   ],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K = np.diag([Im2 ** -5.0, Im2 ** -5.0, Im2 ** -3.0])
    return (vd / np.sqrt(6.0)) * (K @ Y_block)


# Defensive alternative sign conventions
def Mu_fixed_signflip(tau, C, vu=1.0):
    """Same as fixed but with +Y_uD,1 (test C-G overall sign)."""
    Y_uD, Y_u3, _, _ = build_Y_combinations(tau, C)
    YuD1, YuD2, YuD3 = Y_uD
    s32 = np.sqrt(3.0) / 2.0
    Y_block = np.array([
        [0.0,        s32 * YuD2,  s32 * YuD3],
        [+YuD1,      0.5 * YuD3,  0.5 * YuD2],
        [Y_u3[0],    Y_u3[2],     Y_u3[1]   ],
    ], dtype=complex)
    Im2 = 2.0 * tau.imag
    K = np.diag([Im2 ** -3.0, Im2 ** -3.0, Im2 ** -0.5])
    return (vu / np.sqrt(6.0)) * (K @ Y_block)


def yukawa_ratios(M):
    s = np.sort(np.abs(svd(M, compute_uv=False)))[::-1]
    return s[2] / s[1], s[1] / s[0]


CASES = {
    'best':  0.00455 + 1.00705j,
    'tau=i': 0.0 + 1.0j,
}

VARIANTS = [
    ('A48 buggy (M_u baseline, M_d baseline)', Mu_buggy, Md_buggy),
    ('FIX Eq 20/21 row2 swap',                  Mu_fixed, Md_fixed),
    ('FIX + signflip on -Y_uD,1',               Mu_fixed_signflip, Md_fixed),
]


def report():
    print("=" * 84)
    print("A63 - dMVP26 Kahler-norm fix attempts (vs PDG-2024 GUT targets)")
    print("=" * 84)
    print(f"{'variant':<48s} {'tag':<6s}  yu/yc      yc/yt      yd/ys      ys/yb")
    print("-" * 84)
    for name, fU, fD in VARIANTS:
        for tag, tau in CASES.items():
            Mu = fU(tau, C_BEST)
            Md = fD(tau, C_BEST)
            yu_yc, yc_yt = yukawa_ratios(Mu)
            yd_ys, ys_yb = yukawa_ratios(Md)
            print(f"{name:<48s} {tag:<6s}  "
                  f"{yu_yc:.3e}  {yc_yt:.3e}  {yd_ys:.3e}  {ys_yb:.3e}")
        # ratios vs targets
        Mu = fU(CASES['best'], C_BEST); Md = fD(CASES['best'], C_BEST)
        a, b = yukawa_ratios(Mu); c, d = yukawa_ratios(Md)
        print(f"{'  -> ratio vs PDG (best)':<48s} {'':<6s}  "
              f"{a/TARGET['yu/yc']:.2f}x      {b/TARGET['yc/yt']:.2f}x      "
              f"{c/TARGET['yd/ys']:.2f}x      {d/TARGET['ys/yb']:.2f}x")
        print()
    print("Targets:                                                "
          f"{TARGET['yu/yc']:.3e}  {TARGET['yc/yt']:.3e}  "
          f"{TARGET['yd/ys']:.3e}  {TARGET['ys/yb']:.3e}")


if __name__ == "__main__":
    report()
