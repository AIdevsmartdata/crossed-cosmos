"""
V3 Independent Re-Verification of I1.5 Lepton Sector Claims
============================================================
Source: LYD20 arXiv:2006.10722, TeX lines 1480-1556.

This script is FRESHLY WRITTEN — it does NOT reuse I1.5/lepton_unified.py.
It uses the same eta-based modular form infrastructure as H3/mass_matrix.py
but applies it to the LEPTON sector of LYD20's unified model.

LYD20 unified-model lepton assignment (TeX line 1483, eq:unification):
  L    ~ 3 (triplet S'_4),  k_L = 2
  E1^c ~ 1 (trivial),       k_{E1c} = 2   → k_L + k_{E1c} = 4 → Y^(4)_3
  E2^c ~ 1 (trivial),       k_{E2c} = 0   → k_L + k_{E2c} = 2 → Y^(2)_3
  E3^c ~ 1hat' (hat-1'),    k_{E3c} = 1   → k_L + k_{E3c} = 3 → Y^(3)_hat3

Charged-lepton mass matrix (TeX lines 1491-1495, eq:Ml):
  M_e = | alpha_e Y4^(4)   alpha_e Y6^(4)   alpha_e Y5^(4) |
        | beta_e  Y3^(2)   beta_e  Y5^(2)   beta_e  Y4^(2) |  * v_d
        | gamma_e Y2^(3)   gamma_e Y4^(3)   gamma_e Y3^(3) |

Note on LYD20 component indexing:
  Y^(4)_3 triplet = (Y4_4, Y4_5, Y4_6) in H3 notation
  Y^(2)_3 triplet = (Y2_3, Y2_4, Y2_5) in H3 notation
  Y^(3)_hat3 triplet = (Y3_2, Y3_3, Y3_4) in H3 notation

LYD20 unified model's eq:Ml uses subscripts 4,6,5 for row1 and 3,5,4 for row2
and 2,4,3 for row3 — these are the component indices within each triplet,
matching the same CG coefficient pattern used throughout LYD20.

PDG values (2022):
  m_e = 0.510998950 MeV
  m_mu = 105.6583755 MeV
  m_tau = 1776.86 MeV
  m_e/m_mu = 4.8363e-3
  m_mu/m_tau = 5.9457e-2

LYD20 target values (TeX line 928-930):
  m_e/m_mu = 0.0048 ± 0.0002
  m_mu/m_tau = 0.0565 ± 0.0045

LYD20 unified model best-fit params (TeX lines 1537-1538):
  tau = -0.2123 + 1.5201i
  beta_e/alpha_e = 0.0187
  gamma_e/alpha_e = 0.1466
  alpha_e * v_d = 16.8880 MeV
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────
# 1. MODULAR FORMS (same eta-based infrastructure as H3/mass_matrix.py)
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=80):
    """Dedekind eta: q = exp(2πiτ), η(τ) = q^(1/24) prod_{n>=1}(1-q^n)."""
    q = exp(2j * pi * tau)
    result = q**(1.0/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

def weight1_forms(tau, n_terms=80):
    """
    Y_1, Y_2, Y_3: weight-1 triplet 3hat' of S'_4.
    LYD20 lines 296-330. Basis: e1=eta^4(4τ)/eta^2(2τ), etc.
    """
    e1 = eta(4*tau, n_terms)**4 / eta(2*tau, n_terms)**2
    e2 = eta(2*tau, n_terms)**10 / (eta(4*tau, n_terms)**4 * eta(tau, n_terms)**4)
    e3 = eta(2*tau, n_terms)**4 / eta(tau, n_terms)**2

    omega = exp(2j * pi / 3)
    s2 = sqrt(2.0)
    s3 = sqrt(3.0)

    Y1 = 4*s2*e1 + s2*1j*e2 + 2*s2*(1-1j)*e3
    Y2 = (-2*s2*(1+s3)*omega**2*e1
          - (1-s3)/s2*1j*omega**2*e2
          + 2*s2*(1-1j)*omega**2*e3)
    Y3 = (2*s2*(s3-1)*omega*e1
          - (1+s3)/s2*1j*omega*e2
          + 2*s2*(1-1j)*omega*e3)
    return Y1, Y2, Y3

def all_forms(Y1, Y2, Y3):
    """
    Compute all needed modular form components from weight-1 (Y1,Y2,Y3).
    Polynomials transcribed from LYD20 TeX lines 346-395, 1854-1863.
    """
    f = {}
    # Weight-1
    f['Y1_1'], f['Y1_2'], f['Y1_3'] = Y1, Y2, Y3

    # Weight-2, triplet 3 (LYD20 lines 347-351)
    f['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    f['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    f['Y2_5'] = 2*Y2**2 - 2*Y1*Y3

    # Weight-3, triplet 3hat (LYD20 lines 355-360)
    # Y^(3)_hat3 = (Y3_2, Y3_3, Y3_4) in H3 notation
    f['Y3_2'] = 2*(2*Y1**3 - Y2**3 - Y3**3)
    f['Y3_3'] = 6*Y3*(Y2**2 - Y1*Y3)
    f['Y3_4'] = 6*Y2*(Y3**2 - Y1*Y2)

    # Weight-4, triplet 3 (LYD20 Appendix lines 1854-1863)
    # Y^(4)_3 triplet = (Y4_4, Y4_5, Y4_6) in H3 notation
    f['Y4_4'] = 6*Y1*(-Y2**3 + Y3**3)
    f['Y4_5'] = (6*Y1*Y3*(Y2**2 - Y1*Y3)
                 + 2*Y2*(-2*Y1**3 + Y2**3 + Y3**3))
    f['Y4_6'] = (6*Y1*Y2*(Y1*Y2 - Y3**2)
                 - 2*Y3*(-2*Y1**3 + Y2**3 + Y3**3))

    return f

def M_e_unified(tau, alpha_e, beta_e, gamma_e):
    """
    Charged-lepton mass matrix for LYD20 unified model.
    LYD20 TeX lines 1491-1495, eq:Ml.

    Convention: M_e row-i couples E_i^c to L via Y-forms.
    Row 0 (E1^c, trivial, weight 2): Y^(4)_3 triplet → (Y4_4, Y4_6, Y4_5)
    Row 1 (E2^c, trivial, weight 0): Y^(2)_3 triplet → (Y2_3, Y2_5, Y2_4)
    Row 2 (E3^c, hat-1', weight 1): Y^(3)_hat3     → (Y3_2, Y3_4, Y3_3)

    LYD20 eq:Ml column ordering matches (Y_4, Y_6, Y_5) for row 1,
    (Y_3, Y_5, Y_4) for row 2, (Y_2, Y_4, Y_3) for row 3.
    """
    Y1, Y2, Y3 = weight1_forms(tau)
    f = all_forms(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)

    # Row 0: alpha_e * (Y4^(4), Y6^(4), Y5^(4))
    # In H3 notation: Y4_4 = Y4^(4)_component4, Y4_6 = ..._6, Y4_5 = ..._5
    M[0, 0] = alpha_e * f['Y4_4']
    M[0, 1] = alpha_e * f['Y4_6']
    M[0, 2] = alpha_e * f['Y4_5']

    # Row 1: beta_e * (Y3^(2), Y5^(2), Y4^(2))
    M[1, 0] = beta_e * f['Y2_3']
    M[1, 1] = beta_e * f['Y2_5']
    M[1, 2] = beta_e * f['Y2_4']

    # Row 2: gamma_e * (Y2^(3), Y4^(3), Y3^(3))
    M[2, 0] = gamma_e * f['Y3_2']
    M[2, 1] = gamma_e * f['Y3_4']
    M[2, 2] = gamma_e * f['Y3_3']

    return M

def lepton_mass_ratios(M):
    """SVD-diagonalize M†M, return sorted singular values and ratios."""
    evals = np.linalg.svd(M, compute_uv=False)
    evals_sorted = np.sort(evals)  # ascending: m_e < m_mu < m_tau
    if evals_sorted[0] < 1e-30:
        return None, None
    r1 = evals_sorted[0] / evals_sorted[1]  # m_e/m_mu
    r2 = evals_sorted[1] / evals_sorted[2]  # m_mu/m_tau
    return r1, r2

# PDG values (2022 review)
PDG_me  = 0.510998950   # MeV
PDG_mmu = 105.6583755   # MeV
PDG_mtau = 1776.86      # MeV
PDG_r1 = PDG_me / PDG_mmu    # 4.8363e-3
PDG_r2 = PDG_mmu / PDG_mtau  # 5.9457e-2

# LYD20 quoted targets (TeX line 928-930)
LYD20_r1_target = 0.0048
LYD20_r1_sigma  = 0.0002
LYD20_r2_target = 0.0565
LYD20_r2_sigma  = 0.0045


def run_all():
    print("=" * 65)
    print("V3 — Independent Lepton Sector Verification")
    print("=" * 65)

    # ─────────────────────────────────────────────────────────
    # V3.A — Verify LYD20's own best-fit at tau=-0.2123+1.5201i
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.A: LYD20 best-fit tau = -0.2123+1.5201i ---")
    tau_lyd = -0.2123 + 1.5201j
    be_a = 0.0187   # beta_e/alpha_e (LYD20 TeX line 1537)
    ge_a = 0.1466   # gamma_e/alpha_e (LYD20 TeX line 1538)
    # Set alpha_e=1; ratios are what matter for mass ratios
    M_lyd = M_e_unified(tau_lyd, alpha_e=1.0, beta_e=be_a, gamma_e=ge_a)
    r1_lyd, r2_lyd = lepton_mass_ratios(M_lyd)
    print(f"  tau (LYD20 quoted) = {tau_lyd}")
    print(f"  beta_e/alpha_e = 0.0187 (LYD20 TeX line 1537)")
    print(f"  gamma_e/alpha_e = 0.1466 (LYD20 TeX line 1538)")
    print(f"  m_e/m_mu  = {r1_lyd:.4e}  (PDG: {PDG_r1:.4e},  LYD20 target: 0.0048±0.0002)")
    print(f"  m_mu/m_tau = {r2_lyd:.4e}  (PDG: {PDG_r2:.4e},  LYD20 target: 0.0565±0.0045)")
    if r1_lyd and r2_lyd:
        print(f"  % off PDG: r1={100*(r1_lyd-PDG_r1)/PDG_r1:+.1f}%,  r2={100*(r2_lyd-PDG_r2)/PDG_r2:+.1f}%")

    # ─────────────────────────────────────────────────────────
    # V3.B.1 — Weight-4 forms at tau=i (critical check: are they zero?)
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.B.1: Weight-4 forms at tau=i ---")
    tau_i = 1j
    Y1i, Y2i, Y3i = weight1_forms(tau_i)
    fi = all_forms(Y1i, Y2i, Y3i)
    print(f"  Y4_4 = {fi['Y4_4'].real:.4f} + {fi['Y4_4'].imag:.4f}i")
    print(f"  Y4_5 = {fi['Y4_5'].real:.4f} + {fi['Y4_5'].imag:.4f}i")
    print(f"  Y4_6 = {fi['Y4_6'].real:.4f} + {fi['Y4_6'].imag:.4f}i")
    print(f"  Y2_3 = {fi['Y2_3'].real:.4f} + {fi['Y2_3'].imag:.4f}i")
    print(f"  Y2_4 = {fi['Y2_4'].real:.4f} + {fi['Y2_4'].imag:.4f}i")
    print(f"  Y2_5 = {fi['Y2_5'].real:.4f} + {fi['Y2_5'].imag:.4f}i")
    print(f"  Y3_2 = {fi['Y3_2'].real:.4f} + {fi['Y3_2'].imag:.4f}i")
    print(f"  Y3_3 = {fi['Y3_3'].real:.4f} + {fi['Y3_3'].imag:.4f}i")
    print(f"  Y3_4 = {fi['Y3_4'].real:.4f} + {fi['Y3_4'].imag:.4f}i")
    print(f"  Constraint check Y1^2+2*Y2*Y3 = {abs(Y1i**2 + 2*Y2i*Y3i):.2e} (should be ~0)")

    # ─────────────────────────────────────────────────────────
    # V3.B.2 — Evaluate at tau=i with LYD20's quoted params
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.B.2: tau=i with LYD20's QUOTED params (beta/alpha=0.0187, gamma/alpha=0.1466) ---")
    M_i_lyd_params = M_e_unified(tau_i, alpha_e=1.0, beta_e=0.0187, gamma_e=0.1466)
    r1_i_lyd, r2_i_lyd = lepton_mass_ratios(M_i_lyd_params)
    print(f"  m_e/m_mu   = {r1_i_lyd:.4e}  (PDG: {PDG_r1:.4e})")
    print(f"  m_mu/m_tau = {r2_i_lyd:.4e}  (PDG: {PDG_r2:.4e})")
    if r1_i_lyd:
        print(f"  % off PDG: r1={100*(r1_i_lyd-PDG_r1)/PDG_r1:+.1f}%,  r2={100*(r2_i_lyd-PDG_r2)/PDG_r2:+.1f}%")
        print(f"  --> These are LYD20's quark-sector-fitted params AT tau=i (NOT at LYD20's best-fit tau)")

    # ─────────────────────────────────────────────────────────
    # V3.B.3 — Optimize (beta/alpha, gamma/alpha) at tau=i to match PDG
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.B.3: Optimize params at tau=i to match PDG ratios ---")

    def chi2_tau_i(params):
        log_be, log_ge = params
        be = 10**log_be
        ge = 10**log_ge
        M = M_e_unified(tau_i, alpha_e=1.0, beta_e=be, gamma_e=ge)
        r1, r2 = lepton_mass_ratios(M)
        if r1 is None or r1 <= 0 or r2 <= 0:
            return 1e10
        chi2 = ((r1 - PDG_r1)/LYD20_r1_sigma)**2 + ((r2 - PDG_r2)/LYD20_r2_sigma)**2
        return chi2

    # Grid search first
    best_chi2 = 1e12
    best_be, best_ge = 0.5, 1e-3

    for log_be in np.linspace(-3, 2, 30):
        for log_ge in np.linspace(-5, 1, 30):
            c = chi2_tau_i([log_be, log_ge])
            if c < best_chi2:
                best_chi2 = c
                best_be = 10**log_be
                best_ge = 10**log_ge

    print(f"  Grid search best: chi2={best_chi2:.4f}, beta/alpha={best_be:.4f}, gamma/alpha={best_ge:.6f}")

    # Refine with scipy minimize
    res = minimize(chi2_tau_i, [np.log10(best_be), np.log10(best_ge)],
                   method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-10, 'maxiter': 10000})

    opt_be = 10**res.x[0]
    opt_ge = 10**res.x[1]
    M_opt = M_e_unified(tau_i, alpha_e=1.0, beta_e=opt_be, gamma_e=opt_ge)
    r1_opt, r2_opt = lepton_mass_ratios(M_opt)

    print(f"\n  OPTIMIZED at tau=i:")
    print(f"  beta_e/alpha_e  = {opt_be:.6f}")
    print(f"  gamma_e/alpha_e = {opt_ge:.6f}")
    print(f"  chi2 = {res.fun:.6f}")
    print(f"  m_e/m_mu   = {r1_opt:.4e}  (PDG: {PDG_r1:.4e})  % off = {100*(r1_opt-PDG_r1)/PDG_r1:+.2f}%")
    print(f"  m_mu/m_tau = {r2_opt:.4e}  (PDG: {PDG_r2:.4e})  % off = {100*(r2_opt-PDG_r2)/PDG_r2:+.2f}%")
    print(f"  --> LYD20 1-sigma: r1=0.0048±0.0002, r2=0.0565±0.0045")
    if r1_opt and r2_opt:
        in_r1 = abs(r1_opt - LYD20_r1_target) < LYD20_r1_sigma
        in_r2 = abs(r2_opt - LYD20_r2_target) < LYD20_r2_sigma
        print(f"  r1 within LYD20 1-sigma: {in_r1}")
        print(f"  r2 within LYD20 1-sigma: {in_r2}")

    # ─────────────────────────────────────────────────────────
    # V3.C — DOF analysis
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.C: Degrees-of-freedom analysis ---")
    print("  Free parameters at tau=i (fixed):")
    print("    beta_e/alpha_e : 1 real param")
    print("    gamma_e/alpha_e: 1 real param")
    print("    alpha_e * v_d  : 1 overall scale (sets absolute mass, not ratios)")
    print("  Observables for mass ratios: m_e/m_mu, m_mu/m_tau = 2")
    print("  DOF = 2 obs - 2 params = 0")
    print("  --> This is a 0-DOF fit (exactly determined, not over-determined)")
    print("  --> I1.5 re-fit (beta/alpha, gamma/alpha) at tau=i to match PDG")
    print("  --> LYD20's quoted (beta/alpha=0.0187, gamma/alpha=0.1466) fitted at tau=-0.2123+1.5201i")
    print("  --> These are DIFFERENT parameter sets; tau=i requires different (beta, gamma)")

    # ─────────────────────────────────────────────────────────
    # V3.D — Cross-check: tau=-0.2123+1.5201i vs tau=i chi2 comparison
    # ─────────────────────────────────────────────────────────
    print("\n--- V3.D: Structural question — is tau=i special or generic? ---")
    # Try a few other tau values to see if chi2 is equally low elsewhere
    test_taus = [
        (0.0 + 1.2j, "tau=1.2i"),
        (0.0 + 1.5j, "tau=1.5i"),
        (-0.2 + 1.5j, "tau=-0.2+1.5i (near LYD20 bf)"),
        (0.0 + 2.0j, "tau=2.0i"),
        (0.3 + 1.0j, "tau=0.3+i"),
    ]

    def best_chi2_at_tau(tau_val):
        def obj(params):
            log_be, log_ge = params
            be = 10**log_be
            ge = 10**log_ge
            M = M_e_unified(tau_val, alpha_e=1.0, beta_e=be, gamma_e=ge)
            r1, r2 = lepton_mass_ratios(M)
            if r1 is None or r1 <= 0 or r2 <= 0:
                return 1e10
            return ((r1 - PDG_r1)/LYD20_r1_sigma)**2 + ((r2 - PDG_r2)/LYD20_r2_sigma)**2

        best_c = 1e12
        best_p = [0.0, -2.0]
        for lb in np.linspace(-3, 2, 15):
            for lg in np.linspace(-5, 1, 15):
                c = obj([lb, lg])
                if c < best_c:
                    best_c = c
                    best_p = [lb, lg]
        r = minimize(obj, best_p, method='Nelder-Mead',
                     options={'xatol': 1e-7, 'fatol': 1e-8, 'maxiter': 5000})
        return r.fun

    print("\n  Minimum chi2 achievable by re-fitting (beta, gamma) at various tau values:")
    for tv, label in test_taus:
        try:
            c = best_chi2_at_tau(tv)
            print(f"    {label}: min chi2 = {c:.4f}")
        except Exception as e:
            print(f"    {label}: ERROR {e}")

    print(f"    tau=i:       min chi2 = {res.fun:.4f}  [from V3.B.3]")

    print("\n--- SUMMARY ---")
    print(f"PDG values used (2022):")
    print(f"  m_e = {PDG_me} MeV, m_mu = {PDG_mmu} MeV, m_tau = {PDG_mtau} MeV")
    print(f"  m_e/m_mu  = {PDG_r1:.5e}")
    print(f"  m_mu/m_tau = {PDG_r2:.5e}")
    print(f"\nLYD20 unified model lepton matrix (TeX lines 1491-1495) at tau=i:")
    print(f"  Row 0 uses Y^(4)_3 (weight-4) — NON-ZERO at tau=i")
    print(f"  Row 1 uses Y^(2)_3 (weight-2)")
    print(f"  Row 2 uses Y^(3)_hat3 (weight-3)")
    print(f"\nWith free (beta/alpha, gamma/alpha) at tau=i:")
    print(f"  m_e/m_mu  = {r1_opt:.4e} ({100*(r1_opt-PDG_r1)/PDG_r1:+.2f}% from PDG)")
    print(f"  m_mu/m_tau = {r2_opt:.4e} ({100*(r2_opt-PDG_r2)/PDG_r2:+.2f}% from PDG)")
    print(f"\nWith LYD20's quoted params (0.0187, 0.1466) at tau=i (NOT at their best-fit tau):")
    print(f"  m_e/m_mu  = {r1_i_lyd:.4e} ({100*(r1_i_lyd-PDG_r1)/PDG_r1:+.1f}% from PDG)")
    print(f"  m_mu/m_tau = {r2_i_lyd:.4e} ({100*(r2_i_lyd-PDG_r2)/PDG_r2:+.1f}% from PDG)")


if __name__ == "__main__":
    run_all()
