"""
I1.5.D — Charged Lepton Mass Ratios from LYD20 Joint Unified Model

SOURCE: LYD20 arXiv:2006.10722, Section "Quark-Lepton Unification" (lines 1480-1556
of modular_symmetry_S4prime.tex), specifically Eq.(eq:unification) and Eq.(eq:Ml).

UNIFIED MODEL LEPTON ASSIGNMENTS (LYD20 lines 1482-1489, TeX source):
  L      ~ 3   of S'_4, k_L = 2
  E1^c   ~ 1   of S'_4, k_{E1^c} = 2  → k_L + k_{E1^c} = 4 → Y^(4)_3 row
  E2^c   ~ 1   of S'_4, k_{E2^c} = 0  → k_L + k_{E2^c} = 2 → Y^(2)_3 row
  E3^c   ~ 1̂'  of S'_4, k_{E3^c} = 1  → k_L + k_{E3^c} = 3 → Y^(3)_hat3 row

CHARGED LEPTON MASS MATRIX (LYD20 Eq. eq:Ml, lines 1491-1495):
  M_e = | alpha_e Y4^(4)  alpha_e Y6^(4)  alpha_e Y5^(4) |
        | beta_e  Y3^(2)  beta_e  Y5^(2)  beta_e  Y4^(2) |  * v_d
        | gamma_e Y2^(3)  gamma_e Y4^(3)  gamma_e Y3^(3) |

NOTE: Row 1 uses Y^(4)_3 = (Y4^(4), Y5^(4), Y6^(4))^T but the matrix shows
  (Y4, Y6, Y5) ordering — same permutation as C1's (Y1,Y3,Y2) pattern.
  Verify: In LYD20's contraction rule for (E1^c · L · Y^(4)_3)_1 with
  E1^c~1 and L~3: the singlet contraction of 3 ⊗ 3 → 1 picks up
  L1*Y4 + L2*Y5 + L3*Y6, giving row = (Y4^(4), Y5^(4), Y6^(4)).
  But LYD20 Eq.(Ml) writes (Y4^(4), Y6^(4), Y5^(4)) — consistent with
  the CG convention used throughout LYD20 (same as C1 row pattern).

KEY DIFFERENCE FROM I1 (Case C1):
  C1 (I1): Row 1 = alpha * (Y1, Y3, Y2)  [weight-1 Y^(1)_3hat']
  Unified:  Row 1 = alpha * (Y4^(4), Y6^(4), Y5^(4))  [weight-4 Y^(4)_3]

BEST-FIT τ (LYD20 Eq. line 1531):
  tau = -0.2123 + 1.5201i

BEST-FIT PARAMETERS (LYD20 lines 1535-1538):
  beta_e/alpha_e  = 0.0187
  gamma_e/alpha_e = 0.1466
  alpha_e * v_d   = 16.8880 MeV
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize

# ─────────────────────────────────────────────────────────────────
# Modular forms
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=60):
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result


def modular_forms_weight1(tau, n_terms=60):
    """
    Y_1, Y_2, Y_3 (weight-1, 3̂' of S'_4) via eta functions.
    LYD20 lines 314-376 of TeX source.
    """
    e1 = eta(4*tau, n_terms)**4 / eta(2*tau, n_terms)**2
    e2 = eta(2*tau, n_terms)**10 / (eta(4*tau, n_terms)**4 * eta(tau, n_terms)**4)
    e3 = eta(2*tau, n_terms)**4 / eta(tau, n_terms)**2

    omega = exp(2j * pi / 3)
    s2 = sqrt(2)
    s3 = sqrt(3)

    Y1 = 4*s2*e1 + s2*1j*e2 + 2*s2*(1-1j)*e3
    Y2 = (-2*s2*(1+s3)*omega**2*e1
          - (1-s3)/s2*1j*omega**2*e2
          + 2*s2*(1-1j)*omega**2*e3)
    Y3 = (2*s2*(s3-1)*omega*e1
          - (1+s3)/s2*1j*omega*e2
          + 2*s2*(1-1j)*omega*e3)
    return Y1, Y2, Y3


def get_all_forms(tau, n_terms=60):
    """
    Compute all modular forms needed for unified M_e.
    Weight-2: Y^(2)_3 = (Y3,Y4,Y5) from LYD20 Eq.(345-376)
    Weight-3: Y^(3)_hat3 = (Y2,Y3,Y4) from LYD20 Eq.(same)
    Weight-4: Y^(4)_3 = (Y4,Y5,Y6) from LYD20 Appendix Eq.(1858-1860)
    """
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)

    # Weight-2 forms (LYD20 lines 345-377)
    # Y^(2)_3 = (Y3^(2), Y4^(2), Y5^(2))
    Y2_3 = 2*Y1**2 - 2*Y2*Y3       # Y3^(2) = component 1 of Y^(2)_3
    Y2_4 = 2*Y3**2 - 2*Y1*Y2       # Y4^(2) = component 2
    Y2_5 = 2*Y2**2 - 2*Y1*Y3       # Y5^(2) = component 3
    # Y^(2)_2 = (Y1^(2), Y2^(2))
    Y2_1 = Y2**2 + 2*Y1*Y3         # Y1^(2)
    Y2_2 = Y3**2 + 2*Y1*Y2         # Y2^(2)

    # Weight-3 forms (LYD20 lines 383)
    # Y^(3)_hat3 = (Y2^(3), Y3^(3), Y4^(3))
    Y3_2 = 2*(2*Y1**3 - Y2**3 - Y3**3)   # Y2^(3)
    Y3_3 = 6*Y3*(Y2**2 - Y1*Y3)           # Y3^(3)
    Y3_4 = 6*Y2*(Y3**2 - Y1*Y2)           # Y4^(3)
    # Y^(3)_hat3' = (Y5^(3), Y6^(3), Y7^(3))
    Y3_5 = 6*Y1*(Y3**2 - Y1*Y2)           # Y5^(3) [from CG, check: anti-symm structure]
    Y3_6 = 2*(2*Y2**3 - Y1**3 - Y3**3)   # Y6^(3) [permuted]
    Y3_7 = 6*Y2*(Y1**2 - Y2*Y3)           # Y7^(3) [permuted]

    # Weight-4 forms (LYD20 Appendix lines 1858-1860)
    # Y^(4)_3 = (Y4^(4), Y5^(4), Y6^(4))
    # From LYD20: Y^(4)_3 = (Y^(3)_hat3 ⊗ Y^(1)_hat3')_3
    # Components from TeX line 1858-1860:
    # Y^(4)_3[0] = 6*Y1*(-Y2^3 + Y3^3)
    # Y^(4)_3[1] = 6*Y1*Y3*(Y2^2 - Y1*Y3) + 2*Y2*(-2*Y1^3 + Y2^3 + Y3^3)
    # Y^(4)_3[2] = 6*Y1*Y2*(Y1*Y2 - Y3^2) - 2*Y3*(-2*Y1^3 + Y2^3 + Y3^3)
    Y4_4 = 6*Y1*(-Y2**3 + Y3**3)
    Y4_5 = 6*Y1*Y3*(Y2**2 - Y1*Y3) + 2*Y2*(-2*Y1**3 + Y2**3 + Y3**3)
    Y4_6 = 6*Y1*Y2*(Y1*Y2 - Y3**2) - 2*Y3*(-2*Y1**3 + Y2**3 + Y3**3)

    return (Y1, Y2, Y3,
            Y2_3, Y2_4, Y2_5,
            Y3_2, Y3_3, Y3_4,
            Y4_4, Y4_5, Y4_6)


def M_e_unified(forms, alpha_e, beta_e, gamma_e):
    """
    Charged lepton mass matrix for LYD20 unified model.
    Convention: M_e in E^c M_e L basis (E^c on left, L on right).
    LYD20 Eq.(Ml), lines 1491-1495:
      Row 0 (E1^c ~ 1,  k=2): alpha_e * (Y4^(4), Y6^(4), Y5^(4))
      Row 1 (E2^c ~ 1,  k=0): beta_e  * (Y3^(2), Y5^(2), Y4^(2))
      Row 2 (E3^c ~ 1̂', k=1): gamma_e * (Y2^(3), Y4^(3), Y3^(3))
    Note: LYD20's column ordering (col1, col3, col2) follows the same
    CG pattern as C1 and is reproduced here by using (Y4,Y6,Y5) for row 0.
    """
    (Y1, Y2, Y3,
     Y2_3, Y2_4, Y2_5,
     Y3_2, Y3_3, Y3_4,
     Y4_4, Y4_5, Y4_6) = forms

    Me = np.zeros((3, 3), dtype=complex)
    # Row 0: E1^c, weight-4 Y^(4)_3 → (Y4^(4), Y6^(4), Y5^(4))
    Me[0] = [alpha_e * Y4_4, alpha_e * Y4_6, alpha_e * Y4_5]
    # Row 1: E2^c, weight-2 Y^(2)_3 → (Y3^(2), Y5^(2), Y4^(2))
    Me[1] = [beta_e * Y2_3, beta_e * Y2_5, beta_e * Y2_4]
    # Row 2: E3^c, weight-3 Y^(3)_hat3 → (Y2^(3), Y4^(3), Y3^(3))
    Me[2] = [gamma_e * Y3_2, gamma_e * Y3_4, gamma_e * Y3_3]
    return Me


def sv_sorted(M):
    _, s, _ = np.linalg.svd(M)
    return np.sort(s)


def ratios(M):
    sv = sv_sorted(M)
    if sv[1] < 1e-30 or sv[2] < 1e-30:
        return 1e10, 1e10
    return sv[0]/sv[1], sv[1]/sv[2]


# PDG values
PDG_me   = 0.51099895e-3   # GeV
PDG_mmu  = 105.6583755e-3  # GeV
PDG_mtau = 1776.86e-3      # GeV
r1_PDG = PDG_me / PDG_mmu         # 4.836e-3
r2_PDG = PDG_mmu / PDG_mtau       # 5.946e-2

# LYD20 Eq.(82) targets
r1_LYD = 0.0048;  s1 = 0.0002
r2_LYD = 0.0565;  s2_lyd = 0.0045


def chi2_fixed_tau(params, forms):
    log_beta, log_gamma = params
    beta = exp(log_beta)
    gamma = exp(log_gamma)
    Me = M_e_unified(forms, 1.0, beta, gamma)
    r1, r2 = ratios(Me)
    if r1 <= 0 or r2 <= 0 or r1 >= 1 or r2 >= 1:
        return 1e10
    return ((r1 - r1_LYD)/s1)**2 + ((r2 - r2_LYD)/s2_lyd)**2


def chi2_free_tau(params, n_terms=30):
    re_tau, im_tau, log_beta, log_gamma = params
    if im_tau < 0.05:
        return 1e10
    tau = re_tau + 1j * im_tau
    try:
        forms = get_all_forms(tau, n_terms)
        beta = exp(log_beta)
        gamma = exp(log_gamma)
        Me = M_e_unified(forms, 1.0, beta, gamma)
        r1, r2 = ratios(Me)
        if r1 <= 0 or r2 <= 0 or r1 >= 1 or r2 >= 1:
            return 1e10
        return ((r1 - r1_LYD)/s1)**2 + ((r2 - r2_LYD)/s2_lyd)**2
    except Exception:
        return 1e10


if __name__ == "__main__":
    print("=" * 70)
    print("I1.5.D — LYD20 UNIFIED MODEL Charged Leptons")
    print("=" * 70)
    print(f"PDG: m_e/m_mu = {r1_PDG:.4e},  m_mu/m_tau = {r2_PDG:.4e}")
    print(f"LYD20 best-fit tau (unified) = -0.2123 + 1.5201i  [line 1531]")
    print(f"LYD20 best-fit beta_e/alpha_e = 0.0187, gamma_e/alpha_e = 0.1466")
    print()

    rng = np.random.RandomState(42)

    # ─────────────────────────────────────────────────────────
    # STEP 0: Verify LYD20 best-fit parameters reproduce data
    # ─────────────────────────────────────────────────────────
    print("STEP 0: Verify LYD20 stated best-fit parameters")
    tau_lyd = -0.2123 + 1.5201j
    print(f"  Computing forms at tau = {tau_lyd} ...")
    try:
        forms_lyd = get_all_forms(tau_lyd, n_terms=60)
        beta_lyd  = 0.0187
        gamma_lyd = 0.1466
        Me_lyd = M_e_unified(forms_lyd, 1.0, beta_lyd, gamma_lyd)
        r1_lyd_pred, r2_lyd_pred = ratios(Me_lyd)
        print(f"  m_e/m_mu   at tau_LYD = {r1_lyd_pred:.6e}  (PDG: {r1_PDG:.4e})")
        print(f"  m_mu/m_tau at tau_LYD = {r2_lyd_pred:.6e}  (PDG: {r2_PDG:.4e})")
        print(f"  off PDG: m_e/m_mu = {abs(r1_lyd_pred - r1_PDG)/r1_PDG*100:.1f}%,"
              f"  m_mu/m_tau = {abs(r2_lyd_pred - r2_PDG)/r2_PDG*100:.1f}%")
        print()
    except Exception as ex:
        print(f"  ERROR: {ex}")
        print()

    # ─────────────────────────────────────────────────────────
    # STEP 1: Evaluate at tau=i with optimized beta/gamma
    # ─────────────────────────────────────────────────────────
    print("STEP 1: Optimize beta/gamma at tau=i (unified model)")
    tau_i = 1j
    forms_i = get_all_forms(tau_i, n_terms=60)

    # Check that weight-4 forms are non-trivially zero at tau=i
    Y4_4_i, Y4_5_i, Y4_6_i = forms_i[9], forms_i[10], forms_i[11]
    print(f"  Y4^(4)(i) = {Y4_4_i:.6f}")
    print(f"  Y5^(4)(i) = {Y4_5_i:.6f}")
    print(f"  Y6^(4)(i) = {Y4_6_i:.6f}")
    print()

    best_chi2 = 1e20
    best_params = None

    starts = []
    for lb in np.linspace(-3, 5, 20):
        for lg in np.linspace(-3, 5, 20):
            starts.append([lb, lg])
    for _ in range(50):
        starts.append([rng.uniform(-4, 6), rng.uniform(-4, 6)])

    for x0 in starts:
        try:
            res = minimize(chi2_fixed_tau, x0, args=(forms_i,),
                           method='Nelder-Mead',
                           options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_params = res.x
        except Exception:
            pass

    if best_params is not None:
        log_beta_i, log_gamma_i = best_params
        beta_i = exp(log_beta_i)
        gamma_i = exp(log_gamma_i)
        Me_i = M_e_unified(forms_i, 1.0, beta_i, gamma_i)
        r1_i, r2_i = ratios(Me_i)

        print(f"  Best fit at tau=i (unified model):")
        print(f"    beta_e/alpha_e  = {beta_i:.6e}  (log10 = {np.log10(abs(beta_i)):.3f})")
        print(f"    gamma_e/alpha_e = {gamma_i:.6e}  (log10 = {np.log10(abs(gamma_i)):.3f})")
        print(f"    chi2 = {best_chi2:.6f}")
        print(f"  Predictions:")
        print(f"    m_e/m_mu   = {r1_i:.6e}  (PDG: {r1_PDG:.4e})")
        print(f"    m_mu/m_tau = {r2_i:.6e}  (PDG: {r2_PDG:.4e})")
        pct1 = abs(r1_i - r1_PDG)/r1_PDG * 100
        pct2 = abs(r2_i - r2_PDG)/r2_PDG * 100
        print(f"  Discrepancy from PDG:")
        print(f"    m_e/m_mu:   {pct1:.1f}% off PDG")
        print(f"    m_mu/m_tau: {pct2:.1f}% off PDG")
    print()

    # ─────────────────────────────────────────────────────────
    # STEP 2: Free-tau fit (find global optimum)
    # ─────────────────────────────────────────────────────────
    print("STEP 2: Free tau fit (unified model)")
    best_chi2_free = 1e20
    best_params_free = None

    lb0 = log_beta_i if best_params is not None else -2.0
    lg0 = log_gamma_i if best_params is not None else -2.0

    starts_free = [
        [0.0, 1.0, lb0, lg0],
        [-0.2123, 1.5201, np.log(0.0187), np.log(0.1466)],  # LYD20 best fit
        [-0.5, 0.866, lb0, lg0],
        [-0.5, 0.866, np.log(0.0187), np.log(0.1466)],
        [0.0, 1.5, lb0, lg0],
        [0.0, 2.0, lb0, lg0],
        [-0.3, 1.2, lb0, lg0],
        [0.3, 1.0, lb0, lg0],
    ]
    for _ in range(60):
        re_tau = rng.uniform(-0.5, 0.5)
        im_tau = rng.uniform(0.3, 5.0)
        starts_free.append([re_tau, im_tau,
                             rng.uniform(-5, 4), rng.uniform(-5, 4)])

    for x0 in starts_free:
        try:
            res = minimize(chi2_free_tau, x0,
                           method='Nelder-Mead',
                           options={'maxiter': 40000, 'xatol': 1e-10, 'fatol': 1e-10})
            if res.fun < best_chi2_free:
                best_chi2_free = res.fun
                best_params_free = res.x
        except Exception:
            pass

    if best_params_free is not None:
        re_free, im_free, lb_free, lg_free = best_params_free
        tau_free = re_free + 1j * im_free
        beta_free = exp(lb_free)
        gamma_free = exp(lg_free)
        forms_free = get_all_forms(tau_free, n_terms=60)
        Me_free = M_e_unified(forms_free, 1.0, beta_free, gamma_free)
        r1_free, r2_free = ratios(Me_free)

        print(f"  Best fit (free tau, unified model):")
        print(f"    tau = {re_free:.6f} + {im_free:.6f}i")
        print(f"    beta_e/alpha_e  = {beta_free:.6e}")
        print(f"    gamma_e/alpha_e = {gamma_free:.6e}")
        print(f"    chi2 = {best_chi2_free:.6f}")
        print(f"  Predictions:")
        print(f"    m_e/m_mu   = {r1_free:.6e}  (PDG: {r1_PDG:.4e})")
        print(f"    m_mu/m_tau = {r2_free:.6e}  (PDG: {r2_PDG:.4e})")
        pct1_f = abs(r1_free - r1_PDG)/r1_PDG * 100
        pct2_f = abs(r2_free - r2_PDG)/r2_PDG * 100
        print(f"  Discrepancy from PDG:")
        print(f"    m_e/m_mu:   {pct1_f:.1f}% off PDG")
        print(f"    m_mu/m_tau: {pct2_f:.1f}% off PDG")
    print()

    # ─────────────────────────────────────────────────────────
    # FINAL VERDICT
    # ─────────────────────────────────────────────────────────
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    if best_params is not None:
        pct1 = abs(r1_i - r1_PDG)/r1_PDG * 100
        pct2 = abs(r2_i - r2_PDG)/r2_PDG * 100
        max_pct = max(pct1, pct2)

        print(f"\n  Unified model at tau=i:")
        print(f"    m_e/m_mu   = {r1_i:.4e}  PDG = {r1_PDG:.4e}  off = {pct1:.1f}%")
        print(f"    m_mu/m_tau = {r2_i:.4e}  PDG = {r2_PDG:.4e}  off = {pct2:.1f}%")
        print()

        if max_pct < 15:
            verdict_i = "[v7 LEPTON CLOSURE OK at tau=i with unified model]"
        elif max_pct < 100:
            verdict_i = f"[v7 LEPTON FAILS at tau=i — off by {max_pct:.0f}% with unified model]"
        else:
            verdict_i = f"[v7 LEPTON REFUTED at tau=i — off by >{max_pct:.0f}% with unified model]"

        print(f"  VERDICT (tau=i, unified): {verdict_i}")

    if best_params_free is not None:
        pct1_f = abs(r1_free - r1_PDG)/r1_PDG * 100
        pct2_f = abs(r2_free - r2_PDG)/r2_PDG * 100
        max_pct_f = max(pct1_f, pct2_f)

        print(f"\n  Unified model at free tau ({re_free:.4f}+{im_free:.4f}i):")
        print(f"    m_e/m_mu   = {r1_free:.4e}  PDG = {r1_PDG:.4e}  off = {pct1_f:.1f}%")
        print(f"    m_mu/m_tau = {r2_free:.4e}  PDG = {r2_PDG:.4e}  off = {pct2_f:.1f}%")

        if max_pct_f < 15:
            verdict_f = "[v7 LEPTON CLOSURE OK at free tau]"
        elif max_pct_f < 100:
            verdict_f = f"[LEPTON FIT TIGHT at free tau — off by {max_pct_f:.0f}%]"
        else:
            verdict_f = f"[LEPTON REFUTED even at free tau — off by {max_pct_f:.0f}%]"

        print(f"  VERDICT (free tau, unified): {verdict_f}")

    print()
    print("  LYD20 joint-unified best fit tau: -0.2123 + 1.5201i")
    print(f"  Distance from i: |tau_LYD - i| = {abs(-0.2123 + 1.5201j - 1j):.4f}")
    print(f"  => tau_LYD is {abs(-0.2123 + 1.5201j - 1j)/abs(1j):.2f}x |i| away from tau=i")
    print()
    print("  Note: Model VI (H3) is a standalone quark-only model (NOT the unified model).")
    print("  LYD20's unified model uses a DIFFERENT quark sector (higher-weight forms,")
    print("  Eq.(WqII)), different from Model VI's Eq.(Wq6).")
    print("  The unified model's lepton sector uses weight-4 Y^(4)_3 for row-1 (NOT C1's weight-1).")
