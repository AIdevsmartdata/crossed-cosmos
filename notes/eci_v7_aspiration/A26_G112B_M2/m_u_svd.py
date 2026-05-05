"""
A26 -- G1.12.B Milestone M2: Off-diagonal Y_u from LYD20 Model VI at tau=W1*
==============================================================================

OWNER     : Sonnet sub-agent A26 (parent persisted)
DATE      : 2026-05-05 evening
HALLU     : 78 entering
GOAL      : Build M_u = alpha_u*M^(1) + beta_u*M^(2) + gamma_u*M^(3) at the
            W1 best-fit modular point tau* = -0.1897 + 1.0034i, refit the
            LYD20 Model VI coupling ratios (beta_u/alpha_u, gamma_u/alpha_u),
            then SVD to extract (m_u, m_c, m_t) and unitary U_L, U_R.

PHYSICS
=======
LYD20 Model VI up-quark mass matrix (arXiv:2006.10722, Eq. Mq_6):

    M_u = ( alpha_u Y^(1)_3hat'(tau)               row 0  : u^c
            beta_u  Y^(2)_3(tau)                  row 1  : c^c
            gamma_u Y^(5)_3hat(tau)               row 2  : t^c
          ) <H_u>

where (in column order Q1, Q2, Q3):
    row 0 = (Y1   , Y3   , Y2   )            weight 1, irrep 3hat'
    row 1 = (Y2_3 , Y2_5 , Y2_4 )            weight 2, irrep 3
    row 2 = (Y5_3 , Y5_5 , Y5_4 )            weight 5, irrep 3hat

with Y2_3 = 2 Y1^2 - 2 Y2 Y3 etc.

Fit targets (M2 binary gate, Antusch-Hinze-Saad arXiv:2510.01312 GUT scale):
    y_c/y_t (M_GUT) = 2.725e-3  (1% tolerance per A18 / A22 spec)
    y_u/y_c (M_GUT) = 1.94e-3   (PDG ratio survives to GUT to within ~5%)

The SVD outputs:
    sv_u  -> (m_u, m_c, m_t) up to alpha_u v_u overall scale
    U_L   -> 3x3 unitary, left singular vectors (rotations of L-handed quarks)
    U_R   -> 3x3 unitary, right singular vectors (rotations of R-handed quarks)

These feed M3 as input to Patel-Shukla 1-loop matching of Eq. (8).

M2 BINARY GATE
==============
PASS iff:
    (i)   beta_u, gamma_u fit converges with chi2_up < 1
    (ii)  m_c/m_t within 1% of 2.725e-3 (Antusch-Hinze-Saad GUT-scale target)
    (iii) U_L, U_R verified unitary to <1e-10
    (iv)  Output handoff JSON written for M3 (Patel-Shukla)
"""

import numpy as np
from numpy import pi, exp, sqrt, log
from scipy.optimize import minimize
from scipy.linalg import svd as scipy_svd
import json
import os
import sys

# ---------------------------------------------------------------------------
# 1. Targets (Antusch-Hinze-Saad 2025, arXiv:2510.01312, GUT-scale Yukawas)
# ---------------------------------------------------------------------------
# These are the GUT-scale up-quark Yukawa ratios from SM 2-loop running
# (Antusch-Hinze-Saad 2025 Table 2 / equivalent reference values).
# A22 SUMMARY references: y_c/y_t target = 2.725e-3 (1% tolerance).

AHS_yt_GUT       = 0.4454       # y_t at M_GUT
AHS_yc_yt_GUT    = 2.725e-3     # y_c/y_t at M_GUT  (M2 binary gate target)
AHS_yu_yc_GUT    = 2.05e-3      # y_u/y_c at M_GUT  (~PDG ratio, weak running)

# 1-sigma fit weights (log-space)
SIG_LOG_RAT      = 0.05         # 5% log-tolerance for the up-row fit

# Modular best-fit (W1 verdict)
TAU_W1 = -0.1897 + 1.0034j

# ---------------------------------------------------------------------------
# 2. Modular forms (transcribed from W1 / LYD20 / A22)
# ---------------------------------------------------------------------------

def eta(tau, n_terms=120):
    """Dedekind eta function via q-product."""
    q = exp(2j * pi * tau)
    out = q ** (1.0 / 24.0)
    for n in range(1, n_terms):
        out *= (1.0 - q ** n)
    return out

def weight1_forms(tau, n_terms=120):
    """LYD20 weight-1 seeds (Y1, Y2, Y3) via eta(tau), eta(2tau), eta(4tau)."""
    e1 = eta(4 * tau, n_terms) ** 4 / eta(2 * tau, n_terms) ** 2
    e2 = (eta(2 * tau, n_terms) ** 10
          / (eta(4 * tau, n_terms) ** 4 * eta(tau, n_terms) ** 4))
    e3 = eta(2 * tau, n_terms) ** 4 / eta(tau, n_terms) ** 2
    omega = exp(2j * pi / 3.0)
    s2 = sqrt(2.0); s3 = sqrt(3.0)
    Y1 = 4 * s2 * e1 + s2 * 1j * e2 + 2 * s2 * (1 - 1j) * e3
    Y2 = (-2 * s2 * (1 + s3) * omega ** 2 * e1
          - (1 - s3) / s2 * 1j * omega ** 2 * e2
          + 2 * s2 * (1 - 1j) * omega ** 2 * e3)
    Y3 = (2 * s2 * (s3 - 1) * omega * e1
          - (1 + s3) / s2 * 1j * omega * e2
          + 2 * s2 * (1 - 1j) * omega * e3)
    return Y1, Y2, Y3

def all_forms(tau, n_terms=120):
    """All LYD20 modular forms used in M_up (weight-1, weight-2 triplet, weight-5 3hat)."""
    Y1, Y2, Y3 = weight1_forms(tau, n_terms)
    f = {'Y1': Y1, 'Y2': Y2, 'Y3': Y3}
    # weight-2 triplet 3 components Y^(2)_3, Y^(2)_4, Y^(2)_5
    f['Y2_3'] = 2 * Y1 ** 2 - 2 * Y2 * Y3
    f['Y2_4'] = 2 * Y3 ** 2 - 2 * Y1 * Y2
    f['Y2_5'] = 2 * Y2 ** 2 - 2 * Y1 * Y3
    # weight-5 3hat: Y^(5)_3, Y^(5)_4, Y^(5)_5
    f['Y5_3'] = 18 * Y1 ** 2 * (-Y2 ** 3 + Y3 ** 3)
    f['Y5_4'] = (4 * Y1 ** 4 * Y2 + 4 * Y1 * (Y2 ** 4 - 5 * Y2 * Y3 ** 3)
                 + 14 * Y1 ** 3 * Y3 ** 2 - 4 * Y3 ** 2 * (Y2 ** 3 + Y3 ** 3)
                 + 6 * Y1 ** 2 * Y2 ** 2 * Y3)
    f['Y5_5'] = (-4 * Y1 ** 4 * Y3 - 4 * Y1 * (Y3 ** 4 - 5 * Y2 ** 3 * Y3)
                 - 14 * Y1 ** 3 * Y2 ** 2 + 4 * Y2 ** 2 * (Y2 ** 3 + Y3 ** 3)
                 - 6 * Y1 ** 2 * Y2 * Y3 ** 2)
    return f

# ---------------------------------------------------------------------------
# 3. M_u construction (LYD20 Model VI Eq. Mq_6) -- alpha_u absorbed in scale
# ---------------------------------------------------------------------------

def M_up(f, beta_u, gamma_u, alpha_u=1.0):
    """LYD20 Model VI up-quark mass matrix.
    Returns 3x3 complex matrix (alpha_u v_u factored out -> overall scale).
    """
    M = np.zeros((3, 3), dtype=complex)
    M[0] = [alpha_u * f['Y1'], alpha_u * f['Y3'], alpha_u * f['Y2']]
    M[1] = [beta_u * f['Y2_3'], beta_u * f['Y2_5'], beta_u * f['Y2_4']]
    M[2] = [gamma_u * f['Y5_3'], gamma_u * f['Y5_5'], gamma_u * f['Y5_4']]
    return M

def M_up_from_components(M1, M2, M3, alpha_u, beta_u, gamma_u):
    """Decomposed form M_u = alpha_u M^(1) + beta_u M^(2) + gamma_u M^(3)."""
    return alpha_u * M1 + beta_u * M2 + gamma_u * M3

def decompose_M_up(f):
    """Build the three component matrices M^(1), M^(2), M^(3) of LYD20 Model VI.

    M^(1) is the alpha_u row template (only row 0 nonzero), M^(2) the beta_u
    row template (only row 1), M^(3) the gamma_u row template (only row 2).
    """
    M1 = np.zeros((3, 3), dtype=complex)
    M2 = np.zeros((3, 3), dtype=complex)
    M3 = np.zeros((3, 3), dtype=complex)
    M1[0] = [f['Y1'], f['Y3'], f['Y2']]
    M2[1] = [f['Y2_3'], f['Y2_5'], f['Y2_4']]
    M3[2] = [f['Y5_3'], f['Y5_5'], f['Y5_4']]
    return M1, M2, M3

# ---------------------------------------------------------------------------
# 4. SVD utilities
# ---------------------------------------------------------------------------

def svd_full(M):
    """Return (U_L, sv_sorted_ascending, U_R) such that
       M = U_L diag(sv_descending) U_R^dagger  (scipy convention).
    For the M2 deliverable we re-order to mass-ascending [m_u, m_c, m_t]:
       M = U_L_mass diag(sv_ascending) U_R_mass^dagger
    """
    U, sv, Vh = scipy_svd(M)
    # scipy returns sv descending. Re-order to ascending.
    idx = np.argsort(sv)         # ascending
    sv_asc = sv[idx]
    U_L = U[:, idx]
    U_R = Vh.conj().T[:, idx]
    return U_L, sv_asc, U_R

def mass_ratios_from_M(M):
    """(m_u/m_c, m_c/m_t) from singular values of M."""
    _, sv, _ = svd_full(M)
    return sv[0] / sv[1], sv[1] / sv[2], sv

# ---------------------------------------------------------------------------
# 5. Fit beta_u, gamma_u to AHS GUT-scale targets at tau*
# ---------------------------------------------------------------------------

def fit_up_sector_AHS(f, n_starts=10):
    """Fit (beta_u, gamma_u) so SVD of M_up reproduces:
         m_c/m_t = AHS_yc_yt_GUT
         m_u/m_c = AHS_yu_yc_GUT
    Uses log-space residuals; alpha_u = 1 fixed.
    """
    def obj(x):
        bu, gu = exp(x[0]), exp(x[1])
        try:
            M = M_up(f, bu, gu, alpha_u=1.0)
            r01, r12, _ = mass_ratios_from_M(M)
        except Exception:
            return 1e12
        if r01 <= 0 or r12 <= 0 or not (np.isfinite(r01) and np.isfinite(r12)):
            return 1e12
        c = ((log(r01) - log(AHS_yu_yc_GUT)) / SIG_LOG_RAT) ** 2
        c += ((log(r12) - log(AHS_yc_yt_GUT)) / SIG_LOG_RAT) ** 2
        return c

    best = 1e12
    best_x = None
    for lb in np.linspace(-4, 8, 8):
        for lg in np.linspace(-4, 8, 8):
            try:
                res = minimize(obj, [lb, lg], method='Nelder-Mead',
                               options={'maxiter': 10000, 'xatol': 1e-10,
                                        'fatol': 1e-10})
                if res.fun < best:
                    best = res.fun
                    best_x = res.x
            except Exception:
                pass
    if best_x is None:
        return None, None, 1e12
    return exp(best_x[0]), exp(best_x[1]), best

# ---------------------------------------------------------------------------
# 6. Unitarity verification
# ---------------------------------------------------------------------------

def unitarity_residual(U):
    """Return ||U U^dagger - I||_max."""
    return float(np.max(np.abs(U @ U.conj().T - np.eye(U.shape[0]))))

# ---------------------------------------------------------------------------
# 7. Determine alpha_u from y_t = AHS_yt_GUT (overall scale fix)
# ---------------------------------------------------------------------------

def fix_overall_scale(M_unit, target_yt=AHS_yt_GUT):
    """Multiply M by alpha_u so that the largest singular value equals target_yt.
    Returns (alpha_u, M_scaled, sv_scaled).
    """
    _, sv, _ = svd_full(M_unit)
    sv_top = sv[2]
    if sv_top <= 0:
        raise ValueError("largest singular value <= 0")
    alpha = target_yt / sv_top
    return alpha, alpha * M_unit, alpha * sv

# ---------------------------------------------------------------------------
# 8. Main M2 driver
# ---------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("A26 -- G1.12.B Milestone M2: SVD of LYD20 Model VI M_u at tau* = W1*")
    print("=" * 78)
    print(f"  tau*        = {TAU_W1.real:+.4f}{TAU_W1.imag:+.4f}i  (W1 verdict 2026-05-05)")
    print(f"  Targets (AHS arXiv:2510.01312, GUT-scale):")
    print(f"     y_c/y_t = {AHS_yc_yt_GUT:.5e}    (M2 binary-gate, 1% tol)")
    print(f"     y_u/y_c = {AHS_yu_yc_GUT:.5e}    (informational)")
    print(f"     y_t     = {AHS_yt_GUT:.5e}    (overall scale fix)")
    print()

    # 8.1 modular forms at tau*
    print("[1] Modular forms at tau*")
    print("-" * 78)
    f = all_forms(TAU_W1, n_terms=160)
    Y1, Y2, Y3 = f['Y1'], f['Y2'], f['Y3']
    constraint = Y1 ** 2 + 2 * Y2 * Y3
    print(f"  Y1(tau*)            = {Y1:.4e}")
    print(f"  Y2(tau*)            = {Y2:.4e}")
    print(f"  Y3(tau*)            = {Y3:.4e}")
    print(f"  Y1^2 + 2 Y2 Y3      = {constraint:.4e}  (LYD20 MF-constraint, target 0)")
    print()

    # 8.2 component matrices
    print("[2] Decompose M_u = alpha M^(1) + beta M^(2) + gamma M^(3) (LYD20 Model VI)")
    print("-" * 78)
    M1, M2c, M3 = decompose_M_up(f)
    print("  |M^(1)| (u-row template, weight-1, 3hat'):")
    print(np.abs(M1))
    print("  |M^(2)| (c-row template, weight-2, 3):")
    print(np.abs(M2c))
    print("  |M^(3)| (t-row template, weight-5, 3hat):")
    print(np.abs(M3))
    print()

    # 8.3 fit beta_u, gamma_u
    print("[3] Fit beta_u/alpha_u, gamma_u/alpha_u to AHS GUT-scale targets")
    print("-" * 78)
    bu, gu, chi2 = fit_up_sector_AHS(f, n_starts=8)
    print(f"  beta_u  / alpha_u   = {bu:.6e}")
    print(f"  gamma_u / alpha_u   = {gu:.6e}")
    print(f"  chi2_up (2 obs)     = {chi2:.4e}")
    print()

    # 8.4 build M_u, SVD
    print("[4] Construct M_u and SVD")
    print("-" * 78)
    Mu_unit = M_up(f, bu, gu, alpha_u=1.0)
    print("  |M_u| (alpha_u=1, before overall-scale fix):")
    print(np.abs(Mu_unit))
    U_L, sv_unit, U_R = svd_full(Mu_unit)
    r01_unit = sv_unit[0] / sv_unit[1]
    r12_unit = sv_unit[1] / sv_unit[2]
    print(f"  Singular values (asc, alpha_u=1)            = {sv_unit}")
    print(f"  m_u/m_c (predicted)  = {r01_unit:.6e}    target = {AHS_yu_yc_GUT:.6e}")
    print(f"  m_c/m_t (predicted)  = {r12_unit:.6e}    target = {AHS_yc_yt_GUT:.6e}")
    pct_yc_yt = 100 * (r12_unit - AHS_yc_yt_GUT) / AHS_yc_yt_GUT
    pct_yu_yc = 100 * (r01_unit - AHS_yu_yc_GUT) / AHS_yu_yc_GUT
    print(f"  Delta y_c/y_t        = {pct_yc_yt:+.3f}%   (M2 binary gate: |.| < 1%)")
    print(f"  Delta y_u/y_c        = {pct_yu_yc:+.3f}%   (informational)")
    print()

    # 8.5 fix alpha_u from y_t
    print("[5] Fix alpha_u so y_t = AHS top Yukawa at GUT")
    print("-" * 78)
    alpha_u, Mu_scaled, sv_scaled = fix_overall_scale(Mu_unit, target_yt=AHS_yt_GUT)
    print(f"  alpha_u (overall)    = {alpha_u:.6e}")
    print(f"  Singular values (asc, scaled)               = {sv_scaled}")
    print(f"  -> y_u (predicted GUT) = {sv_scaled[0]:.6e}")
    print(f"  -> y_c (predicted GUT) = {sv_scaled[1]:.6e}")
    print(f"  -> y_t (predicted GUT) = {sv_scaled[2]:.6e}    target = {AHS_yt_GUT:.5e}")
    print()

    # 8.6 unitarity check
    print("[6] Unitarity check on U_L, U_R")
    print("-" * 78)
    eL = unitarity_residual(U_L)
    eR = unitarity_residual(U_R)
    print(f"  ||U_L U_L^dag - I||_max = {eL:.3e}  (target < 1e-10)")
    print(f"  ||U_R U_R^dag - I||_max = {eR:.3e}  (target < 1e-10)")
    print()

    # 8.7 reconstruction sanity
    print("[7] Reconstruction sanity: U_L diag(sv) U_R^dag should reproduce M_u")
    print("-" * 78)
    Mu_recon = U_L @ np.diag(sv_unit) @ U_R.conj().T
    recon_err = float(np.max(np.abs(Mu_recon - Mu_unit)))
    print(f"  ||M_u_recon - M_u||_max = {recon_err:.3e}")
    print()

    # 8.8 print U_L, U_R
    print("[8] Mixing matrices U_L, U_R (mass-ascending columns)")
    print("-" * 78)
    np.set_printoptions(precision=5, suppress=False)
    print("  U_L:")
    print(U_L)
    print("  U_R:")
    print(U_R)
    print()

    # 8.9 binary gate
    print("[9] M2 BINARY GATE")
    print("-" * 78)
    g_fit  = chi2 < 1.0
    g_yc_yt = abs(pct_yc_yt) < 1.0
    g_unitL = eL < 1e-10
    g_unitR = eR < 1e-10
    g_recon = recon_err < 1e-10
    print(f"  GATE A (chi2_up < 1)               : {'PASS' if g_fit else 'FAIL'} ({chi2:.3e})")
    print(f"  GATE B (|Delta y_c/y_t| < 1%)      : {'PASS' if g_yc_yt else 'FAIL'} ({pct_yc_yt:+.3f}%)")
    print(f"  GATE C (U_L unitary < 1e-10)       : {'PASS' if g_unitL else 'FAIL'} ({eL:.2e})")
    print(f"  GATE D (U_R unitary < 1e-10)       : {'PASS' if g_unitR else 'FAIL'} ({eR:.2e})")
    print(f"  GATE E (M_u reconstruction clean)  : {'PASS' if g_recon else 'FAIL'} ({recon_err:.2e})")
    n_pass = sum([g_fit, g_yc_yt, g_unitL, g_unitR, g_recon])
    print(f"  ----------------------------------------")
    print(f"  PASSED: {n_pass}/5")
    if n_pass == 5:
        verdict = "M2 BINARY GATE PASS"
    elif n_pass >= 4:
        verdict = f"M2 PARTIAL ({n_pass}/5)"
    else:
        verdict = "M2 FAIL"
    print(f"  VERDICT: {verdict}")
    print()

    # 8.10 dump JSON for M3 handoff
    def to_floats(arr):
        return [[float(x) for x in row] for row in arr]
    out_json = {
        'tau_star': {'re': float(TAU_W1.real), 'im': float(TAU_W1.imag)},
        'targets_AHS': {'yt_GUT': float(AHS_yt_GUT),
                        'yc_yt_GUT': float(AHS_yc_yt_GUT),
                        'yu_yc_GUT': float(AHS_yu_yc_GUT)},
        'fit': {'beta_over_alpha': float(bu),
                'gamma_over_alpha': float(gu),
                'alpha_u_overall': float(alpha_u),
                'chi2_up': float(chi2)},
        'singular_values_GUT': {
            'y_u': float(sv_scaled[0]),
            'y_c': float(sv_scaled[1]),
            'y_t': float(sv_scaled[2]),
            'mc_mt': float(r12_unit),
            'mu_mc': float(r01_unit),
            'mc_mt_pct_vs_target': float(pct_yc_yt),
            'mu_mc_pct_vs_target': float(pct_yu_yc),
        },
        'M_u_alpha1': {
            're': to_floats(Mu_unit.real),
            'im': to_floats(Mu_unit.imag),
        },
        'U_L': {'re': to_floats(U_L.real), 'im': to_floats(U_L.imag)},
        'U_R': {'re': to_floats(U_R.real), 'im': to_floats(U_R.imag)},
        'unitarity': {'UL_resid': float(eL), 'UR_resid': float(eR),
                      'reconstruction_resid': float(recon_err)},
        'verdict': str(verdict),
        'n_pass': int(n_pass),
        'gates': {
            'A_chi2_lt_1': bool(g_fit),
            'B_dyc_yt_lt_1pct': bool(g_yc_yt),
            'C_UL_unitary': bool(g_unitL),
            'D_UR_unitary': bool(g_unitR),
            'E_reconstruction': bool(g_recon),
        },
    }
    out_path = os.path.join(os.path.dirname(__file__), 'svd_results.json')
    with open(out_path, 'w') as fh:
        json.dump(out_json, fh, indent=2)
    print(f"  svd_results.json written -> {out_path}")
    print()

    return out_json


if __name__ == "__main__":
    res = main()
