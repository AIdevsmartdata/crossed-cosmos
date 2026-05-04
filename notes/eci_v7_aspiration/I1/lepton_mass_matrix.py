"""
I1 — Charged Lepton Mass Matrix from LYD20 arXiv:2006.10722

SOURCE CITATIONS (all page/equation numbers from the PDF as read):
  - Lepton model table: LYD20 Table 2 (page 14), section 5.1 "Charged lepton sector"
  - Case C1 mass matrix: Table 2 row C1, Eq. (44), page 12-13
  - Superpotential: Eq. (44), page 12
  - Weight constraints: Eq. (45), page 12-13
  - Modular forms: same polynomials in Y1,Y2,Y3 as H3/mass_matrix.py (from LYD20 App)

LYD20 LEPTON CASE C1 (Table 2, page 14):
  The four representation sub-cases giving SAME mass matrix (quoted verbatim):
    rho_L = 3,  rho_{E1c} = 1̂,  rho_{E2c} = 1,   rho_{E3c} = 1̂'
    rho_L = 3', rho_{E1c} = 1̂', rho_{E2c} = 1',  rho_{E3c} = 1̂
    rho_L = 3̂,  rho_{E1c} = 1,   rho_{E2c} = 1̂',  rho_{E3c} = 1'
    rho_L = 3̂', rho_{E1c} = 1',  rho_{E2c} = 1̂,   rho_{E3c} = 1

  f_{E1}(Y) = Y^(1)_{3̂'}, f_{E2}(Y) = Y^(2)_{3}, f_{E3}(Y) = Y^(3)_{3̂}
  Weights: k_L + k_{E1} = 1,  k_L + k_{E2} = 2,  k_L + k_{E3} = 3
  [i.e., k_E1 = 1-k_L, k_E2 = 2-k_L, k_E3 = 3-k_L]

CHARGED LEPTON MASS MATRIX M_e (LYD20 Table 2, page 14, case C1):
  Convention: M_e is in E^c M_e L basis (E^c on left, L on right)
  M_e = | alpha Y1     alpha Y3     alpha Y2    | * v_d
        | beta  Y3^(2)  beta  Y5^(2)  beta  Y4^(2)| * v_d
        | gamma Y2^(3)  gamma Y4^(3)  gamma Y3^(3)| * v_d

  where Y1,Y2,Y3 are weight-1 modular forms (3̂' of S'_4),
        Y3^(2),Y4^(2),Y5^(2) are weight-2 (3 of S'_4), labeled Y^(2)_3,Y^(2)_4,Y^(2)_5
        Y2^(3),Y3^(3),Y4^(3) are weight-3 (3̂ of S'_4), labeled Y^(3)_2,Y^(3)_3,Y^(3)_4

WHY C1 IS THE NATURAL COMPANION TO QUARK MODEL VI:
  - Quark Model VI uses Q~3 with RH quarks as singlets {1̂, 1, 1̂'} at weights {1,2,5}-k_Q
  - Lepton C1 uses L~3 with RH leptons as singlets {1̂, 1, 1̂'} at weights {1,2,3}-k_L
  - Both have the same leading-row structure: row 1 uses Y^(1)_{3̂'} with contraction to 1̂'
  - C1 is the MINIMAL weight lepton case (weight-3 max vs weight-5 for Model VI)
  - This is the natural pairing discussed in LYD20 section 5.1

PDG VALUES (PDG 2022, particle data booklet):
  m_e = 0.51099895000 MeV  [PDG 2022]
  m_mu = 105.6583755 MeV   [PDG 2022]
  m_tau = 1776.86 MeV      [PDG 2022]
  m_e/m_mu = 4.836e-3
  m_mu/m_tau = 5.946e-2

  LYD20 Eq. (82) gives:
    m_e/m_mu = 0.0048 +/- 0.0002
    m_mu/m_tau = 0.0565 +/- 0.0045
  [citing Ref [68] in LYD20 — their experimental inputs]

ANTI-HALLUCINATION NOTICE:
  All mass matrix entries below are TRANSCRIBED DIRECTLY from LYD20 Table 2 (page 14).
  The modular form polynomials (Y^(k)_i in terms of Y1,Y2,Y3) use the same
  expressions as H3/mass_matrix.py which were transcribed from LYD20 Appendix lines 346-395.
"""

import numpy as np
from numpy import pi, sqrt, exp
import sys
import os

# ─────────────────────────────────────────────────────────────────
# 1. WEIGHT-1 MODULAR FORMS  (same as H3/mass_matrix.py)
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=80):
    """Dedekind eta function via q-product. q = exp(2πiτ)."""
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

def modular_forms_weight1(tau, n_terms=80):
    """
    Y_1, Y_2, Y_3 (weight-1, 3̂' of S'_4) via eta functions.
    LYD20 lines 296-330.
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


# ─────────────────────────────────────────────────────────────────
# 2. HIGHER-WEIGHT MODULAR FORMS (same polynomials as H3/mass_matrix.py)
# ─────────────────────────────────────────────────────────────────

def modular_forms_all(Y1, Y2, Y3):
    """All needed modular form components. Same as H3/mass_matrix.py."""
    forms = {}

    # Weight-1
    forms['Y1_1'] = Y1
    forms['Y1_2'] = Y2
    forms['Y1_3'] = Y3

    # Weight-2 (LYD20 lines 347-351)
    forms['Y2_1'] = -Y2**2 - 2*Y1*Y3
    forms['Y2_2'] =  Y3**2 + 2*Y1*Y2
    forms['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    forms['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    forms['Y2_5'] = 2*Y2**2 - 2*Y1*Y3

    # Weight-3 (LYD20 lines 355-360)
    forms['Y3_1'] = 2*(Y1**3 + Y2**3 + Y3**3 - 3*Y1*Y2*Y3)
    forms['Y3_2'] = 2*(2*Y1**3 - Y2**3 - Y3**3)
    forms['Y3_3'] = 6*Y3*(Y2**2 - Y1*Y3)
    forms['Y3_4'] = 6*Y2*(Y3**2 - Y1*Y2)
    forms['Y3_5'] = 2*(Y2**3 - Y3**3)
    forms['Y3_6'] = 2*(-2*Y1**2*Y2 + Y2**2*Y3 + Y1*Y3**2)
    forms['Y3_7'] = 2*(2*Y1**2*Y3 - Y1*Y2**2 - Y2*Y3**2)

    return forms


# ─────────────────────────────────────────────────────────────────
# 3. CHARGED LEPTON MASS MATRIX M_e (LYD20 Table 2, Case C1, page 14)
#
# EXPLICIT MATRIX (LYD20 Table 2 C1, Eq.(44), page 12-14):
#   M_e = | alpha*Y1      alpha*Y3      alpha*Y2    |
#          | beta*Y3^(2)  beta*Y5^(2)   beta*Y4^(2)  |
#          | gamma*Y2^(3)  gamma*Y4^(3)  gamma*Y3^(3)|  * v_d
#
# Row 0 (E1^c coupling): uses weight-1 modular forms Y^(1)_{3̂'}
#   components: Y1, Y3, Y2  [indices from LYD20 Table 2 C1 column order]
# Row 1 (E2^c coupling): uses weight-2 modular forms Y^(2)_{3}
#   components: Y^(2)_3, Y^(2)_5, Y^(2)_4
# Row 2 (E3^c coupling): uses weight-3 modular forms Y^(3)_{3̂}
#   components: Y^(3)_2, Y^(3)_4, Y^(3)_3
#
# NOTE ON COLUMN ORDER: LYD20's M_e columns run over L=(L1,L2,L3).
# The product E_1^c (L Y^(1)_{3̂'})_{1̂'} via CG [3 x 3̂' -> 1̂'] gives:
#   (L1 Y1 + L3 Y3 + L2 Y2) [same CG as quark up-sector]
# So the row is [alpha*Y1, alpha*Y3, alpha*Y2] — consistent with Table 2.
# ─────────────────────────────────────────────────────────────────

def M_e(tau, alpha_e, beta_e, gamma_e, n_terms=80):
    """
    Charged lepton Yukawa mass matrix for LYD20 Case C1.
    Source: LYD20 arXiv:2006.10722, Table 2 (page 14), Eq. (44) (page 12-13).

    Convention: M_e appears in W_e = E^c M_e L * H_d
    (E^c on left, L on right, v_d absorbed into couplings)

    Structure:
      Row 0 (E1^c, weight-1 forms Y^(1)_{3̂'}):
        [alpha_e * Y1,  alpha_e * Y3,  alpha_e * Y2]

      Row 1 (E2^c, weight-2 forms Y^(2)_{3}):
        [beta_e * Y3^(2),  beta_e * Y5^(2),  beta_e * Y4^(2)]
        = [beta_e * (2Y1^2-2Y2Y3),  beta_e * (2Y2^2-2Y1Y3),  beta_e * (2Y3^2-2Y1Y2)]

      Row 2 (E3^c, weight-3 forms Y^(3)_{3̂}):
        [gamma_e * Y2^(3),  gamma_e * Y4^(3),  gamma_e * Y3^(3)]
        = [gamma_e * 2(2Y1^3-Y2^3-Y3^3),
           gamma_e * 6Y2(Y3^2-Y1Y2),
           gamma_e * 6Y3(Y2^2-Y1Y3)]

    Parameters
    ----------
    tau : complex    modulus value
    alpha_e : float  coupling for e (lightest charged lepton row)
    beta_e : float   coupling for mu (middle row)
    gamma_e : float  coupling for tau (heaviest row)
    """
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    f = modular_forms_all(Y1, Y2, Y3)

    Me = np.zeros((3, 3), dtype=complex)

    # Row 0: E1^c — weight-1 forms Y^(1)_{3̂'} contracted with L~3
    # (3 x 3̂' -> 1̂') CG: L1*Y1 + L3*Y3 + L2*Y2
    Me[0, 0] = alpha_e * f['Y1_1']   # Y1
    Me[0, 1] = alpha_e * f['Y1_3']   # Y3
    Me[0, 2] = alpha_e * f['Y1_2']   # Y2

    # Row 1: E2^c — weight-2 forms Y^(2)_{3} contracted with L~3
    # (3 x 3 -> 1) CG: L1*Y3^(2) + L2*Y5^(2) + L3*Y4^(2)  [from LYD20 Table 2]
    Me[1, 0] = beta_e * f['Y2_3']    # Y^(2)_3 = 2Y1^2 - 2Y2Y3
    Me[1, 1] = beta_e * f['Y2_5']    # Y^(2)_5 = 2Y2^2 - 2Y1Y3
    Me[1, 2] = beta_e * f['Y2_4']    # Y^(2)_4 = 2Y3^2 - 2Y1Y2

    # Row 2: E3^c — weight-3 forms Y^(3)_{3̂} contracted with L~3
    # (3 x 3̂ -> 1̂) CG: L1*Y2^(3) + L2*Y4^(3) + L3*Y3^(3)  [from LYD20 Table 2]
    Me[2, 0] = gamma_e * f['Y3_2']   # Y^(3)_2 = 2(2Y1^3 - Y2^3 - Y3^3)
    Me[2, 1] = gamma_e * f['Y3_4']   # Y^(3)_4 = 6Y2(Y3^2 - Y1Y2)
    Me[2, 2] = gamma_e * f['Y3_3']   # Y^(3)_3 = 6Y3(Y2^2 - Y1Y3)

    return Me


# ─────────────────────────────────────────────────────────────────
# 4. DIAGONALIZATION
# ─────────────────────────────────────────────────────────────────

def singular_values_sorted(M):
    """Return singular values of M in ASCENDING order (m_e, m_mu, m_tau)."""
    _, s, _ = np.linalg.svd(M)
    return np.sort(s)

def mass_ratios_lepton(M):
    """Return (m_e/m_mu, m_mu/m_tau) from singular values."""
    sv = singular_values_sorted(M)
    if sv[1] < 1e-30 or sv[2] < 1e-30:
        return 1e10, 1e10
    return sv[0] / sv[1], sv[1] / sv[2]


# ─────────────────────────────────────────────────────────────────
# 5. FIT LEPTON RATIOS
# ─────────────────────────────────────────────────────────────────

# PDG target values:
# LYD20 Eq.(82) cites: m_e/m_mu = 0.0048+/-0.0002, m_mu/m_tau = 0.0565+/-0.0045
# These are confirmed by PDG 2022:
#   m_e = 0.51099895 MeV, m_mu = 105.6583755 MeV, m_tau = 1776.86 MeV
PDG_me = 0.51099895e-3     # GeV
PDG_mmu = 105.6583755e-3   # GeV
PDG_mtau = 1776.86e-3      # GeV

PDG_me_over_mmu = PDG_me / PDG_mmu      # 4.836e-3
PDG_mmu_over_mtau = PDG_mmu / PDG_mtau  # 5.946e-2

# LYD20's quoted experimental inputs (Eq. 82, page 19-20):
LYD20_me_over_mmu = 0.0048     # +/- 0.0002
LYD20_me_over_mmu_err = 0.0002
LYD20_mmu_over_mtau = 0.0565   # +/- 0.0045
LYD20_mmu_over_mtau_err = 0.0045


def chi2_lepton(params, tau_fixed=None):
    """
    Chi^2 for lepton mass ratios.
    If tau_fixed is set, only fit (log_beta_ratio, log_gamma_ratio).
    Otherwise fit (re_tau, im_tau, log_beta_ratio, log_gamma_ratio).
    """
    from scipy.optimize import minimize

    if tau_fixed is not None:
        log_beta_ratio, log_gamma_ratio = params
        tau = tau_fixed
    else:
        re_tau, im_tau, log_beta_ratio, log_gamma_ratio = params
        if im_tau < 0.1:
            return 1e10
        tau = re_tau + 1j * im_tau

    beta_ratio = exp(log_beta_ratio)
    gamma_ratio = exp(log_gamma_ratio)

    try:
        M = M_e(tau, 1.0, beta_ratio, gamma_ratio, n_terms=60)
        r1, r2 = mass_ratios_lepton(M)
    except Exception:
        return 1e10

    if r1 <= 0 or r2 <= 0 or r1 >= 1 or r2 >= 1:
        return 1e10

    # Use LYD20 quoted uncertainties
    c2 = ((r1 - LYD20_me_over_mmu) / LYD20_me_over_mmu_err)**2 \
       + ((r2 - LYD20_mmu_over_mtau) / LYD20_mmu_over_mtau_err)**2

    return c2


def fit_lepton_sector_fixed_tau(tau, n_trials=30, verbose=True):
    """Fit beta/alpha and gamma/alpha at fixed tau=i."""
    from scipy.optimize import minimize
    import numpy as np

    if verbose:
        print(f"\n--- Fitting lepton sector at fixed tau={tau} ---")
        print(f"    PDG targets: m_e/m_mu = {PDG_me_over_mmu:.4e}, m_mu/m_tau = {PDG_mmu_over_mtau:.4e}")
        print(f"    LYD20 Eq(82): m_e/m_mu = {LYD20_me_over_mmu:.4f}+/-{LYD20_me_over_mmu_err:.4f}")
        print(f"                  m_mu/m_tau = {LYD20_mmu_over_mtau:.4f}+/-{LYD20_mmu_over_mtau_err:.4f}")

    best_chi2 = 1e20
    best_result = None

    rng = np.random.RandomState(123)

    # Starting points for (log_beta, log_gamma) with tau fixed at i
    starts = [
        [np.log(10.0), np.log(0.1)],
        [np.log(50.0), np.log(0.05)],
        [np.log(100.0), np.log(0.01)],
        [np.log(5.0), np.log(0.3)],
        [np.log(20.0), np.log(0.2)],
        [np.log(200.0), np.log(0.001)],
        [np.log(500.0), np.log(0.005)],
        [np.log(1000.0), np.log(0.001)],
    ]

    for _ in range(n_trials):
        log_beta = rng.uniform(-2, 8)
        log_gamma = rng.uniform(-5, 3)
        starts.append([log_beta, log_gamma])

    for x0 in starts:
        try:
            result = minimize(
                chi2_lepton, x0,
                args=(tau,),
                method='Nelder-Mead',
                options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-10}
            )
            if result.fun < best_chi2:
                best_chi2 = result.fun
                best_result = result
        except Exception:
            continue

    if best_result is None:
        print("    FAILED: No successful optimization")
        return None

    log_beta, log_gamma = best_result.x
    beta_fit = exp(log_beta)
    gamma_fit = exp(log_gamma)

    M = M_e(tau, 1.0, beta_fit, gamma_fit, n_terms=80)
    sv = singular_values_sorted(M)
    r1, r2 = mass_ratios_lepton(M)

    if verbose:
        print(f"\n    Best fit (tau fixed at {tau}):")
        print(f"      beta_e/alpha_e  = {beta_fit:.6f}")
        print(f"      gamma_e/alpha_e = {gamma_fit:.6f}")
        print(f"\n    Predictions:")
        print(f"      m_e/m_mu   = {r1:.4e}  (PDG: {PDG_me_over_mmu:.4e}, LYD20: {LYD20_me_over_mmu:.4e})")
        print(f"      m_mu/m_tau = {r2:.4e}  (PDG: {PDG_mmu_over_mtau:.4e}, LYD20: {LYD20_mmu_over_mtau:.4e})")
        print(f"      chi2 = {best_chi2:.4f}")

        if r1 > 0 and r2 > 0:
            err_r1 = abs(r1 - PDG_me_over_mmu) / PDG_me_over_mmu * 100
            err_r2 = abs(r2 - PDG_mmu_over_mtau) / PDG_mmu_over_mtau * 100
            print(f"\n    Discrepancies from PDG:")
            print(f"      m_e/m_mu:   {err_r1:.1f}% off PDG")
            print(f"      m_mu/m_tau: {err_r2:.1f}% off PDG")

    return {
        'tau': tau,
        'beta_ratio': beta_fit,
        'gamma_ratio': gamma_fit,
        'chi2': best_chi2,
        'r1': r1,
        'r2': r2,
        'sv': sv,
    }


def fit_lepton_sector_free_tau(n_trials=40, verbose=True):
    """Fit all parameters including tau."""
    from scipy.optimize import minimize

    if verbose:
        print(f"\n--- Fitting lepton sector with FREE tau ---")

    best_chi2 = 1e20
    best_result = None
    rng = np.random.RandomState(456)

    starts = [
        [0.0, 1.0, np.log(10.0), np.log(0.1)],
        [0.0, 1.0, np.log(50.0), np.log(0.05)],
        [-0.5, 0.866, np.log(20.0), np.log(0.1)],  # tau=omega
        [-0.5, 0.9, np.log(30.0), np.log(0.08)],
        [0.0, 1.5, np.log(100.0), np.log(0.01)],
        [-0.4999, 0.8958, np.log(50.0), np.log(0.05)],  # LYD20 quark best-fit tau
    ]

    for _ in range(n_trials):
        re_tau = rng.uniform(-0.5, 0.5)
        im_tau = rng.uniform(0.5, 3.0)
        log_beta = rng.uniform(-2, 8)
        log_gamma = rng.uniform(-5, 3)
        starts.append([re_tau, im_tau, log_beta, log_gamma])

    for x0 in starts:
        try:
            result = minimize(
                chi2_lepton, x0,
                method='Nelder-Mead',
                options={'maxiter': 100000, 'xatol': 1e-10, 'fatol': 1e-10}
            )
            if result.fun < best_chi2:
                best_chi2 = result.fun
                best_result = result
        except Exception:
            continue

    if best_result is None:
        print("    FAILED")
        return None

    re_tau, im_tau, log_beta, log_gamma = best_result.x
    tau_fit = re_tau + 1j * im_tau
    beta_fit = exp(log_beta)
    gamma_fit = exp(log_gamma)

    M = M_e(tau_fit, 1.0, beta_fit, gamma_fit, n_terms=80)
    sv = singular_values_sorted(M)
    r1, r2 = mass_ratios_lepton(M)

    if verbose:
        print(f"\n    Best fit (free tau):")
        print(f"      tau = {re_tau:.6f} + {im_tau:.6f}i")
        print(f"      beta_e/alpha_e  = {beta_fit:.6f}")
        print(f"      gamma_e/alpha_e = {gamma_fit:.6f}")
        print(f"\n    Predictions:")
        print(f"      m_e/m_mu   = {r1:.4e}  (PDG: {PDG_me_over_mmu:.4e})")
        print(f"      m_mu/m_tau = {r2:.4e}  (PDG: {PDG_mmu_over_mtau:.4e})")
        print(f"      chi2 = {best_chi2:.4f}")

    return {
        'tau': tau_fit,
        'beta_ratio': beta_fit,
        'gamma_ratio': gamma_fit,
        'chi2': best_chi2,
        'r1': r1,
        'r2': r2,
        'sv': sv,
    }


if __name__ == "__main__":
    print("=" * 65)
    print("I1 — LYD20 Charged Lepton Sector (Case C1) at tau = i")
    print("=" * 65)
    print()
    print("Source: LYD20 arXiv:2006.10722, Table 2 (page 14), Eq.(44)")
    print(f"PDG targets: m_e/m_mu = {PDG_me_over_mmu:.4e},  m_mu/m_tau = {PDG_mmu_over_mtau:.4e}")
    print()

    # Step 1: Evaluate at tau=i with scan over coupling ratios
    tau_i = 1j

    print("=" * 65)
    print("STEP 1: Grid scan at tau=i to find approximate parameter range")
    print("=" * 65)
    print("Scanning beta/alpha in [0.01, 1000], gamma/alpha in [0.001, 10]")
    print()

    best_chi2_scan = 1e20
    best_beta_scan = None
    best_gamma_scan = None

    for log_beta in np.linspace(-2, 7, 40):
        for log_gamma in np.linspace(-5, 3, 40):
            beta = exp(log_beta)
            gamma = exp(log_gamma)
            try:
                M = M_e(tau_i, 1.0, beta, gamma, n_terms=60)
                r1, r2 = mass_ratios_lepton(M)
                if r1 > 0 and r2 > 0 and r1 < 1 and r2 < 1:
                    c2 = ((r1 - LYD20_me_over_mmu) / LYD20_me_over_mmu_err)**2 \
                       + ((r2 - LYD20_mmu_over_mtau) / LYD20_mmu_over_mtau_err)**2
                    if c2 < best_chi2_scan:
                        best_chi2_scan = c2
                        best_beta_scan = beta
                        best_gamma_scan = gamma
            except Exception:
                pass

    print(f"Grid scan best: beta/alpha = {best_beta_scan:.4f}, gamma/alpha = {best_gamma_scan:.4f}")
    print(f"  chi2 = {best_chi2_scan:.4f}")
    M_scan = M_e(tau_i, 1.0, best_beta_scan, best_gamma_scan, n_terms=80)
    r1s, r2s = mass_ratios_lepton(M_scan)
    print(f"  m_e/m_mu   = {r1s:.4e}  (PDG: {PDG_me_over_mmu:.4e})")
    print(f"  m_mu/m_tau = {r2s:.4e}  (PDG: {PDG_mmu_over_mtau:.4e})")
    print()

    # Step 2: Full optimization at tau=i
    print("=" * 65)
    print("STEP 2: Full optimization at tau=i")
    print("=" * 65)
    result_i = fit_lepton_sector_fixed_tau(tau_i, n_trials=50, verbose=True)

    # Step 3: Free tau fit
    print()
    print("=" * 65)
    print("STEP 3: Free tau fit (to find true minimum)")
    print("=" * 65)
    result_free = fit_lepton_sector_free_tau(n_trials=60, verbose=True)

    # Step 4: Summary
    print()
    print("=" * 65)
    print("SUMMARY TABLE")
    print("=" * 65)
    print(f"{'Configuration':<35} {'m_e/m_mu':>12} {'m_mu/m_tau':>12}")
    print("-" * 65)
    print(f"{'PDG 2022 [verified from LYD20 Eq.82]':<35} {PDG_me_over_mmu:>12.4e} {PDG_mmu_over_mtau:>12.4e}")
    if result_i:
        print(f"{'tau=i, C1 best fit':<35} {result_i['r1']:>12.4e} {result_i['r2']:>12.4e}")
    if result_free:
        re_tau_f = result_free['tau'].real
        im_tau_f = result_free['tau'].imag
        print(f"{'tau free ({:.3f}+{:.3f}i), C1'.format(re_tau_f, im_tau_f):<35} {result_free['r1']:>12.4e} {result_free['r2']:>12.4e}")
    print()

    if result_i:
        r1 = result_i['r1']
        r2 = result_i['r2']
        pct1 = abs(r1 - PDG_me_over_mmu) / PDG_me_over_mmu * 100
        pct2 = abs(r2 - PDG_mmu_over_mtau) / PDG_mmu_over_mtau * 100
        print(f"Discrepancy from PDG at tau=i:")
        print(f"  m_e/m_mu:   {pct1:.1f}%")
        print(f"  m_mu/m_tau: {pct2:.1f}%")
        print()

        # Parameter naturalness
        print("Parameter naturalness (O(1) test):")
        print(f"  beta_e/alpha_e  = {result_i['beta_ratio']:.4f}  -> log10 = {np.log10(abs(result_i['beta_ratio'])):.2f}")
        print(f"  gamma_e/alpha_e = {result_i['gamma_ratio']:.4f}  -> log10 = {np.log10(abs(result_i['gamma_ratio'])):.2f}")
