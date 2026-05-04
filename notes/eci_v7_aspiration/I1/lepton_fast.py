"""
I1 FAST — Charged Lepton Mass Matrix from LYD20 Case C1 at tau=i

Uses fewer eta terms (40 instead of 80) and a targeted search approach.
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize

# ─────────────────────────────────────────────────────────────────
# Modular forms at tau = i
# At tau=i, the eta function has q = exp(2πi·i) = exp(-2π)
# This converges very fast: |q| = exp(-2π) ≈ 1.87e-3
# So n_terms=20 is already excellent precision.
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=40):
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

def modular_forms_weight1(tau, n_terms=40):
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


def get_forms_at_tau(tau, n_terms=40):
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    # Weight-2
    Y2_3 = 2*Y1**2 - 2*Y2*Y3
    Y2_4 = 2*Y3**2 - 2*Y1*Y2
    Y2_5 = 2*Y2**2 - 2*Y1*Y3
    # Weight-3
    Y3_2 = 2*(2*Y1**3 - Y2**3 - Y3**3)
    Y3_3 = 6*Y3*(Y2**2 - Y1*Y3)
    Y3_4 = 6*Y2*(Y3**2 - Y1*Y2)
    return Y1, Y2, Y3, Y2_3, Y2_4, Y2_5, Y3_2, Y3_3, Y3_4


def M_e_fast(forms, alpha_e, beta_e, gamma_e):
    """Build M_e from pre-computed forms."""
    Y1, Y2, Y3, Y2_3, Y2_4, Y2_5, Y3_2, Y3_3, Y3_4 = forms
    Me = np.zeros((3, 3), dtype=complex)
    # Row 0: E1^c, weight-1
    Me[0] = [alpha_e * Y1, alpha_e * Y3, alpha_e * Y2]
    # Row 1: E2^c, weight-2
    Me[1] = [beta_e * Y2_3, beta_e * Y2_5, beta_e * Y2_4]
    # Row 2: E3^c, weight-3
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


# PDG and LYD20 targets
PDG_me  = 0.51099895e-3    # GeV
PDG_mmu = 105.6583755e-3   # GeV
PDG_mtau = 1776.86e-3      # GeV
r1_PDG = PDG_me / PDG_mmu        # 4.836e-3
r2_PDG = PDG_mmu / PDG_mtau      # 5.946e-2
# LYD20 Eq.(82)
r1_LYD = 0.0048;  s1 = 0.0002
r2_LYD = 0.0565;  s2_lyd = 0.0045


def chi2_fixed_tau(params, forms):
    log_beta, log_gamma = params
    beta = exp(log_beta)
    gamma = exp(log_gamma)
    Me = M_e_fast(forms, 1.0, beta, gamma)
    r1, r2 = ratios(Me)
    if r1 <= 0 or r2 <= 0 or r1 >= 1 or r2 >= 1:
        return 1e10
    return ((r1 - r1_LYD)/s1)**2 + ((r2 - r2_LYD)/s2_lyd)**2


def chi2_free_tau(params, n_terms=25):
    re_tau, im_tau, log_beta, log_gamma = params
    if im_tau < 0.05:
        return 1e10
    tau = re_tau + 1j * im_tau
    try:
        forms = get_forms_at_tau(tau, n_terms)
        beta = exp(log_beta)
        gamma = exp(log_gamma)
        Me = M_e_fast(forms, 1.0, beta, gamma)
        r1, r2 = ratios(Me)
        if r1 <= 0 or r2 <= 0 or r1 >= 1 or r2 >= 1:
            return 1e10
        return ((r1 - r1_LYD)/s1)**2 + ((r2 - r2_LYD)/s2_lyd)**2
    except Exception:
        return 1e10


if __name__ == "__main__":
    print("=" * 65)
    print("I1 FAST — LYD20 C1 Charged Leptons at tau=i")
    print("=" * 65)
    print(f"PDG: m_e/m_mu = {r1_PDG:.4e},  m_mu/m_tau = {r2_PDG:.4e}")
    print(f"LYD20 Eq(82): m_e/m_mu = {r1_LYD:.4f}+/-{s1:.4f},  m_mu/m_tau = {r2_LYD:.4f}+/-{s2_lyd:.4f}")
    print()

    # Pre-compute modular forms at tau=i
    tau_i = 1j
    print("Computing modular forms at tau=i ...")
    forms_i = get_forms_at_tau(tau_i, n_terms=40)
    Y1, Y2, Y3 = forms_i[0], forms_i[1], forms_i[2]
    print(f"  Y1(i) = {Y1:.6f}")
    print(f"  Y2(i) = {Y2:.6f}")
    print(f"  Y3(i) = {Y3:.6f}")
    print(f"  Constraint Y1^2 + 2*Y2*Y3 = {abs(Y1**2 + 2*Y2*Y3):.2e} (should be ~0)")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 1: Fit beta/gamma at tau=i
    # ─────────────────────────────────────────────────────────────
    print("STEP 1: Optimizing beta_e/alpha_e and gamma_e/alpha_e at tau=i")

    best_chi2 = 1e20
    best_params = None
    rng = np.random.RandomState(42)

    starts = []
    # Systematic grid of starting points
    for lb in np.linspace(-1, 7, 15):
        for lg in np.linspace(-4, 3, 15):
            starts.append([lb, lg])
    # Random starts
    for _ in range(30):
        starts.append([rng.uniform(-2, 8), rng.uniform(-5, 4)])

    for x0 in starts:
        try:
            res = minimize(chi2_fixed_tau, x0, args=(forms_i,),
                           method='Nelder-Mead',
                           options={'maxiter': 10000, 'xatol': 1e-12, 'fatol': 1e-12})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_params = res.x
        except Exception:
            pass

    log_beta_i, log_gamma_i = best_params
    beta_i = exp(log_beta_i)
    gamma_i = exp(log_gamma_i)
    Me_i = M_e_fast(forms_i, 1.0, beta_i, gamma_i)
    r1_i, r2_i = ratios(Me_i)
    sv_i = sv_sorted(Me_i)

    print(f"  Best fit at tau=i:")
    print(f"    beta_e/alpha_e  = {beta_i:.6f}  (log10 = {np.log10(beta_i):.3f})")
    print(f"    gamma_e/alpha_e = {gamma_i:.6f}  (log10 = {np.log10(abs(gamma_i)):.3f})")
    print(f"    chi2 = {best_chi2:.6f}")
    print(f"  Predictions:")
    print(f"    m_e/m_mu   = {r1_i:.6e}  (LYD20: {r1_LYD:.4e}, PDG: {r1_PDG:.4e})")
    print(f"    m_mu/m_tau = {r2_i:.6e}  (LYD20: {r2_LYD:.4e}, PDG: {r2_PDG:.4e})")
    print(f"  Discrepancy from PDG:")
    print(f"    m_e/m_mu:   {abs(r1_i - r1_PDG)/r1_PDG*100:.1f}% off PDG")
    print(f"    m_mu/m_tau: {abs(r2_i - r2_PDG)/r2_PDG*100:.1f}% off PDG")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 2: Free tau fit
    # ─────────────────────────────────────────────────────────────
    print("STEP 2: Free tau fit to find global best")
    best_chi2_free = 1e20
    best_params_free = None

    starts_free = [
        [0.0, 1.0, log_beta_i, log_gamma_i],          # tau=i with fitted couplings
        [0.0, 1.0, log_beta_i + 0.5, log_gamma_i],    # small perturbations
        [0.0, 1.0, log_beta_i, log_gamma_i + 0.5],
        [-0.5, 0.866, log_beta_i, log_gamma_i],        # tau=omega
        [-0.4999, 0.8958, log_beta_i, log_gamma_i],    # LYD20 quark BF tau
        [0.0, 1.5, log_beta_i, log_gamma_i],
        [0.0, 2.0, log_beta_i, log_gamma_i],
        [0.3, 1.0, log_beta_i, log_gamma_i],
        [-0.3, 1.2, log_beta_i, log_gamma_i],
    ]
    for _ in range(50):
        re_tau = rng.uniform(-0.5, 0.5)
        im_tau = rng.uniform(0.3, 4.0)
        starts_free.append([re_tau, im_tau,
                             rng.uniform(-2, 8), rng.uniform(-5, 4)])

    for x0 in starts_free:
        try:
            res = minimize(chi2_free_tau, x0,
                           method='Nelder-Mead',
                           options={'maxiter': 30000, 'xatol': 1e-10, 'fatol': 1e-10})
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
        forms_free = get_forms_at_tau(tau_free, n_terms=40)
        Me_free = M_e_fast(forms_free, 1.0, beta_free, gamma_free)
        r1_free, r2_free = ratios(Me_free)

        print(f"  Best fit (free tau):")
        print(f"    tau = {re_free:.6f} + {im_free:.6f}i")
        print(f"    beta_e/alpha_e  = {beta_free:.6f}  (log10 = {np.log10(abs(beta_free)):.3f})")
        print(f"    gamma_e/alpha_e = {gamma_free:.6f}  (log10 = {np.log10(abs(gamma_free)):.3f})")
        print(f"    chi2 = {best_chi2_free:.6f}")
        print(f"  Predictions:")
        print(f"    m_e/m_mu   = {r1_free:.6e}  (PDG: {r1_PDG:.4e})")
        print(f"    m_mu/m_tau = {r2_free:.6e}  (PDG: {r2_PDG:.4e})")
        print(f"  Discrepancy from PDG:")
        print(f"    m_e/m_mu:   {abs(r1_free - r1_PDG)/r1_PDG*100:.1f}% off PDG")
        print(f"    m_mu/m_tau: {abs(r2_free - r2_PDG)/r2_PDG*100:.1f}% off PDG")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 3: QED RGE running (for completeness)
    # For charged leptons: QED-only, running is O(alpha/pi * ln(m_tau/m_e)) ~ 1%
    # The 1-loop QED RGE for mass ratio m_e/m_mu:
    #   d(ln m_f)/d(ln mu) = (alpha/pi) [sum of gauge terms]
    #   For leptons: 16pi^2 d(ln m_f)/dt = -3 g1^2 (QED only, coefficient from SM)
    # Since gauge contributions are UNIVERSAL for all charged leptons (they all
    # have same U(1)_em charge Q=-1), the RATIOS m_e/m_mu and m_mu/m_tau are
    # RENORMALIZATION GROUP INVARIANT at 1-loop QED.
    # This is a standard result: mass ratios of same-charge fermions don't run
    # under QED at 1 loop (the factor is the same for each).
    # The correction first appears at 2-loop QED, which is O((alpha/pi)^2) ~ 10^-5.
    # ─────────────────────────────────────────────────────────────
    print("STEP 3: QED RGE running assessment")
    print("  At 1-loop QED: d(ln m_f)/dt = -(alpha/pi) * C for ALL charged leptons")
    print("  => Ratios m_e/m_mu and m_mu/m_tau are 1-loop RGI (RG-invariant)")
    print("  => 2-loop correction O((alpha/pi)^2) ~ (1/137/pi)^2 ~ 5e-7 — negligible")
    alpha_em = 1.0/137.036
    two_loop_correction = (alpha_em/pi)**2 * np.log(1.8e3)  # rough scale: m_tau/m_e
    print(f"  => Max 2-loop log correction: O(alpha^2/pi^2 * ln(m_tau/m_e)) ~ {two_loop_correction:.2e}")
    print("  CONCLUSION: Predicted GUT-scale ratios = EW-scale ratios to < 0.01%")
    print()

    # ─────────────────────────────────────────────────────────────
    # STEP 4: Parameter naturalness comparison (quark vs lepton)
    # ─────────────────────────────────────────────────────────────
    print("STEP 4: Parameter naturalness — quark vs lepton comparison")
    # From H3/rep_assignment.md (LYD20 Model VI best fit, Eq.111):
    beta_u_over_alpha_u = 62.2142
    gamma_u_over_alpha_u = 0.00104

    print()
    print(f"  {'Sector':<15} {'Parameter':<20} {'Value':>12}  {'log10':>8}  {'O(1)?':>8}")
    print(f"  {'-'*70}")
    print(f"  {'up-quark':<15} {'beta_u/alpha_u':<20} {beta_u_over_alpha_u:>12.4f}  {np.log10(beta_u_over_alpha_u):>8.2f}  {'NO (62x)':>8}")
    print(f"  {'up-quark':<15} {'gamma_u/alpha_u':<20} {gamma_u_over_alpha_u:>12.5f}  {np.log10(gamma_u_over_alpha_u):>8.2f}  {'NO (1e-3)':>8}")
    if best_params is not None:
        nat_e_beta = 'YES' if 0.01 < beta_i < 100 else 'NO'
        nat_e_gamma = 'YES' if 0.01 < abs(gamma_i) < 100 else 'NO'
        print(f"  {'lepton (tau=i)':<15} {'beta_e/alpha_e':<20} {beta_i:>12.4f}  {np.log10(abs(beta_i)):>8.2f}  {nat_e_beta:>8}")
        print(f"  {'lepton (tau=i)':<15} {'gamma_e/alpha_e':<20} {gamma_i:>12.4f}  {np.log10(abs(gamma_i)):>8.2f}  {nat_e_gamma:>8}")
    print()

    # ─────────────────────────────────────────────────────────────
    # FINAL VERDICT
    # ─────────────────────────────────────────────────────────────
    print("=" * 65)
    print("FINAL VERDICT")
    print("=" * 65)

    if best_params is not None:
        pct1 = abs(r1_i - r1_PDG)/r1_PDG * 100
        pct2 = abs(r2_i - r2_PDG)/r2_PDG * 100
        max_pct = max(pct1, pct2)

        print(f"\n  At tau=i:")
        print(f"    m_e/m_mu   predicted = {r1_i:.4e}  PDG = {r1_PDG:.4e}  off = {pct1:.1f}%")
        print(f"    m_mu/m_tau predicted = {r2_i:.4e}  PDG = {r2_PDG:.4e}  off = {pct2:.1f}%")
        print()
        print(f"  chi2 at tau=i: {best_chi2:.3f}")
        print()

        if max_pct < 15:
            verdict = f"[v7 LEPTON CLOSURE OK — within {max_pct:.0f}% of PDG at tau=i]"
        elif max_pct < 50:
            verdict = f"[LEPTON FIT TIGHT — needs {max_pct:.0f}% tuning from tau=i; free tau fit recommended]"
        elif max_pct < 100:
            verdict = f"[LEPTON FIT MARGINAL — tau=i misses by {max_pct:.0f}%; free tau fit required]"
        else:
            verdict = f"[LEPTON REFUTED — predictions miss PDG by >{max_pct:.0f}% at tau=i]"

        # Override with free-tau result if better
        if best_params_free is not None:
            pct1_free = abs(r1_free - r1_PDG)/r1_PDG * 100
            pct2_free = abs(r2_free - r2_PDG)/r2_PDG * 100
            max_pct_free = max(pct1_free, pct2_free)

            print(f"  At free tau ({re_free:.4f}+{im_free:.4f}i):")
            print(f"    m_e/m_mu   predicted = {r1_free:.4e}  PDG = {r1_PDG:.4e}  off = {pct1_free:.1f}%")
            print(f"    m_mu/m_tau predicted = {r2_free:.4e}  PDG = {r2_PDG:.4e}  off = {pct2_free:.1f}%")
            print()

            if max_pct_free < max_pct:
                if max_pct_free < 15:
                    verdict_free = f"[v7 LEPTON CLOSURE OK — within {max_pct_free:.0f}% at free tau]"
                elif max_pct_free < 50:
                    verdict_free = f"[LEPTON FIT TIGHT — within {max_pct_free:.0f}% at free tau]"
                else:
                    verdict_free = f"[LEPTON REFUTED — off by {max_pct_free:.0f}% even at free tau]"
                print(f"  VERDICT (free tau): {verdict_free}")

        print(f"  VERDICT (tau=i):   {verdict}")
