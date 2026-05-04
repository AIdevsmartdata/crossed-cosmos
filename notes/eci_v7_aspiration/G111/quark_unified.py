"""
G1.11 — LYD20 UNIFIED MODEL quark sector at τ=i and τ=LYD20-best

Source: LYD20 arXiv:2006.10722, TeX lines 1507-1526 (Eq. WqII, MqII)
        Appendix lines 1850-1894 for higher-weight modular forms.
        Best-fit parameters at lines 1534-1538.

ANTI-HALLUCINATION NOTE:
All modular form polynomials transcribed from LYD20 TeX source
(lines 1854-1863 for weight-4, 1865-1876 for weight-5, 1879-1893 for weight-6).
All index mappings from LYD20 lines 379-395.

Unified model M_u structure (Eq. MqII, lines 1516-1519):
  Row 0 (u^c ~ 1, k_Q + k_{u^c} = 4, Y^(4)_3):
    [α_u Y4^(4), α_u Y6^(4), α_u Y5^(4)] = [α_u * Y4_4, α_u * Y4_6, α_u * Y4_5]
  Row 1 (c^c ~ 1, k_Q + k_{c^c} = 6, β_u Y^(6)_{3,I} + γ_u Y^(6)_{3,II}):
    [β_u Y5^(6)+γ_u Y8^(6), β_u Y7^(6)+γ_u Y10^(6), β_u Y6^(6)+γ_u Y9^(6)]
     = [β_u*Y6_5+γ_u*Y6_8, β_u*Y6_7+γ_u*Y6_10, β_u*Y6_6+γ_u*Y6_9]
  Row 2 (t^c ~ 1̂', k_Q + k_{t^c} = 3, Y^(3)_hat3):
    [δ_u Y2^(3), δ_u Y4^(3), δ_u Y3^(3)] = [δ_u*Y3_2, δ_u*Y3_4, δ_u*Y3_3]

Compare Model VI M_u (standalone, Eq. Mq_6):
  Row 0: α_u * Y^(1)_{hat3'} = [Y1_1, Y1_3, Y1_2]  (weight-1, DIFFERENT)
  Row 1: β_u * Y^(2)_3 = [Y2_3, Y2_5, Y2_4]        (weight-2, DIFFERENT)
  Row 2: γ_u * Y^(5)_hat3 = [Y5_3, Y5_5, Y5_4]      (weight-5, DIFFERENT)
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize

# ─────────────────────────────────────────────────────────────────
# 1. ETA FUNCTION AND WEIGHT-1 MODULAR FORMS
# ─────────────────────────────────────────────────────────────────

def eta(tau, n_terms=80):
    """Dedekind eta function. q = exp(2πiτ)."""
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

def modular_forms_weight1(tau, n_terms=80):
    """
    Y_1, Y_2, Y_3 (weight-1, 3̂' of S'_4).
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
# 2. ALL MODULAR FORMS  (LYD20 Appendix lines 346-394, 1854-1894)
# ─────────────────────────────────────────────────────────────────

def modular_forms_all(Y1, Y2, Y3):
    """Compute all modular form components from (Y1, Y2, Y3)."""
    f = {}

    # Weight-1 (Y^(1)_{3̂'})
    f['Y1_1'] = Y1
    f['Y1_2'] = Y2
    f['Y1_3'] = Y3

    # Weight-2  (lines 347-351)
    f['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    f['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    f['Y2_5'] = 2*Y2**2 - 2*Y1*Y3

    # Weight-3  (lines 355-360)
    # Y^(3)_hat3 = (Y3_2, Y3_3, Y3_4)
    f['Y3_2'] = 2*(2*Y1**3 - Y2**3 - Y3**3)
    f['Y3_3'] = 6*Y3*(Y2**2 - Y1*Y3)
    f['Y3_4'] = 6*Y2*(Y3**2 - Y1*Y2)

    # Weight-4  (Appendix lines 1854-1863)
    # Y^(4)_3 = (Y4_4, Y4_5, Y4_6)  (LYD20 index notation, line 386-387)
    f['Y4_4'] = 6*Y1*(-Y2**3 + Y3**3)
    f['Y4_5'] = (6*Y1*Y3*(Y2**2 - Y1*Y3)
                 + 2*Y2*(-2*Y1**3 + Y2**3 + Y3**3))
    f['Y4_6'] = (6*Y1*Y2*(Y1*Y2 - Y3**2)
                 - 2*Y3*(-2*Y1**3 + Y2**3 + Y3**3))

    # Weight-6  (Appendix lines 1886-1890)
    # Y^(6)_{3,I} = (Y6_5, Y6_6, Y6_7)  (LYD20 index notation, line 392-393)
    f['Y6_5'] = 2*(Y2**6 + Y3**6 + 4*Y1**4*Y2*Y3 + 6*Y1**2*Y2**2*Y3**2
                   - 4*Y2**3*Y3**3 - 5*Y1**3*(Y2**3 + Y3**3)
                   + Y1*Y2*Y3*(Y2**3 + Y3**3))
    f['Y6_6'] = -2*(2*Y1**5*Y2 - 5*Y1**4*Y3**2 + 3*Y1**3*Y2**2*Y3
                    + 3*Y2**2*Y3*(Y2**3 - Y3**3) + Y1**2*(5*Y2*Y3**3 - 4*Y2**4)
                    + Y1*(Y3**5 - 2*Y2**3*Y3**2))
    f['Y6_7'] = -2*(2*Y1**5*Y3 - 5*Y1**4*Y2**2 + 3*Y1**3*Y2*Y3**2
                    + 3*Y2*Y3**2*(Y3**3 - Y2**3) + Y1*(Y2**5 - 2*Y2**2*Y3**3)
                    + Y1**2*(5*Y2**3*Y3 - 4*Y3**4))

    # Y^(6)_{3,II} = (Y6_8, Y6_9, Y6_10)  (LYD20 index notation, line 392-393)
    D = Y1**4 - 2*Y1*(Y2**3 + Y3**3) + 3*Y2**2*Y3**2
    f['Y6_8']  = 8*(Y1**2 - Y2*Y3)*D
    f['Y6_9']  = 8*(Y3**2 - Y1*Y2)*D
    f['Y6_10'] = 8*(Y2**2 - Y1*Y3)*D

    return f

# ─────────────────────────────────────────────────────────────────
# 3. UNIFIED MODEL M_u  (Eq. MqII, lines 1516-1519)
# ─────────────────────────────────────────────────────────────────

def M_u_unified(tau, alpha_u, beta_u, gamma_u, delta_u, n_terms=80):
    """
    Up-quark mass matrix for LYD20 UNIFIED MODEL.
    Source: LYD20 Eq. MqII, TeX lines 1516-1519.

    Row 0 (u^c ~ 1, k_Q + k_{u^c} = 4):
        α_u * [Y4^(4), Y6^(4), Y5^(4)] = α_u * [Y4_4, Y4_6, Y4_5]
    Row 1 (c^c ~ 1, k_Q + k_{c^c} = 6):
        β_u*[Y5^(6), Y7^(6), Y6^(6)] + γ_u*[Y8^(6), Y10^(6), Y9^(6)]
        = [β_u*Y6_5+γ_u*Y6_8, β_u*Y6_7+γ_u*Y6_10, β_u*Y6_6+γ_u*Y6_9]
    Row 2 (t^c ~ 1̂', k_Q + k_{t^c} = 3):
        δ_u * [Y2^(3), Y4^(3), Y3^(3)] = δ_u * [Y3_2, Y3_4, Y3_3]
    """
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    f = modular_forms_all(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)

    # Row 0: u^c — weight-4 Y^(4)_3: components Y4_4, Y4_6, Y4_5
    M[0, 0] = alpha_u * f['Y4_4']
    M[0, 1] = alpha_u * f['Y4_6']
    M[0, 2] = alpha_u * f['Y4_5']

    # Row 1: c^c — weight-6 Y^(6)_{3,I} + Y^(6)_{3,II}
    # LYD20 matrix line 1518: β_u Y5^(6)+γ_u Y8^(6), β_u Y7^(6)+γ_u Y10^(6), β_u Y6^(6)+γ_u Y9^(6)
    # Y5^(6) = Y6_5, Y7^(6) = Y6_7, Y6^(6) = Y6_6; Y8^(6) = Y6_8, Y10^(6) = Y6_10, Y9^(6) = Y6_9
    M[1, 0] = beta_u * f['Y6_5'] + gamma_u * f['Y6_8']
    M[1, 1] = beta_u * f['Y6_7'] + gamma_u * f['Y6_10']
    M[1, 2] = beta_u * f['Y6_6'] + gamma_u * f['Y6_9']

    # Row 2: t^c — weight-3 Y^(3)_hat3: components Y3_2, Y3_4, Y3_3
    # LYD20 matrix line 1519: δ_u Y2^(3), δ_u Y4^(3), δ_u Y3^(3)
    M[2, 0] = delta_u * f['Y3_2']
    M[2, 1] = delta_u * f['Y3_4']
    M[2, 2] = delta_u * f['Y3_3']

    return M

# ─────────────────────────────────────────────────────────────────
# 4. SINGULAR VALUE DECOMPOSITION → mass ratios
# ─────────────────────────────────────────────────────────────────

def mass_ratios(M):
    """Return (m_u/m_c, m_c/m_t) from singular values of M."""
    sv = np.linalg.svd(M, compute_uv=False)
    sv_sorted = np.sort(np.abs(sv))  # ascending
    m_u, m_c, m_t = sv_sorted[0], sv_sorted[1], sv_sorted[2]
    return m_u / m_c, m_c / m_t, m_u, m_c, m_t

# ─────────────────────────────────────────────────────────────────
# 5. MAIN CALCULATION
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("G1.11 — LYD20 UNIFIED MODEL Quark Sector")
    print("Source: LYD20 arXiv:2006.10722, Eq. MqII, TeX lines 1516-1526")
    print("=" * 70)

    # ── A. VERIFICATION at LYD20 best-fit τ with their quoted parameters ──
    tau_lyd = -0.2123 + 1.5201j

    # Best-fit parameters from LYD20 lines 1534-1536:
    # β_u/α_u = 325.6502,  γ_u/α_u = 2427.3101,  δ_u/α_u = 219.3019
    # α_u * v_u = 2.7758e-5 GeV
    alpha_u_lyd   = 1.0
    beta_u_lyd    = 325.6502
    gamma_u_lyd   = 2427.3101
    delta_u_lyd   = 219.3019

    print(f"\n--- LYD20 best-fit τ = {tau_lyd} ---")
    print(f"Parameters: β/α={beta_u_lyd}, γ/α={gamma_u_lyd}, δ/α={delta_u_lyd}")

    M_lyd = M_u_unified(tau_lyd, alpha_u_lyd, beta_u_lyd, gamma_u_lyd, delta_u_lyd)
    r_uc_lyd, r_ct_lyd, mu_lyd, mc_lyd, mt_lyd = mass_ratios(M_lyd)

    print(f"Singular values (relative): {mu_lyd:.4e}, {mc_lyd:.4e}, {mt_lyd:.4e}")
    print(f"m_u/m_c = {r_uc_lyd:.6f}  (LYD20 quoted: 0.001929)")
    print(f"m_c/m_t = {r_ct_lyd:.6f}  (LYD20 quoted: 0.002725)")
    print(f"Sanity check — m_u/m_c match: {'PASS' if abs(r_uc_lyd - 0.001929)/0.001929 < 0.05 else 'FAIL'}")
    print(f"Sanity check — m_c/m_t match: {'PASS' if abs(r_ct_lyd - 0.002725)/0.002725 < 0.05 else 'FAIL'}")

    # ── B. KEY CALCULATION at τ = i with LYD20 parameters ──
    tau_i = 1j

    print(f"\n--- τ = i (CM-point) with LYD20 best-fit parameters ---")
    M_i = M_u_unified(tau_i, alpha_u_lyd, beta_u_lyd, gamma_u_lyd, delta_u_lyd)

    # Check modular forms at τ=i
    Y1i, Y2i, Y3i = modular_forms_weight1(tau_i)
    fi = modular_forms_all(Y1i, Y2i, Y3i)
    print(f"Y1, Y2, Y3 at τ=i: {Y1i:.4f}, {Y2i:.4f}, {Y3i:.4f}")
    print(f"Y4_4 (first comp Y^(4)_3) at τ=i: {fi['Y4_4']:.4f}")
    print(f"Y4_5 (second comp Y^(4)_3) at τ=i: {fi['Y4_5']:.4f}")
    print(f"Y4_6 (third comp Y^(4)_3) at τ=i: {fi['Y4_6']:.4f}")
    print(f"Y6_5 (first comp Y^(6)_{{3,I}}) at τ=i: {fi['Y6_5']:.4f}")
    print(f"Y6_8 (first comp Y^(6)_{{3,II}}) at τ=i: {fi['Y6_8']:.4f}")
    print(f"Y3_2 (first comp Y^(3)_hat3) at τ=i: {fi['Y3_2']:.4f}")
    print(f"\nM_u at τ=i (magnitudes):")
    print(np.abs(M_i))

    r_uc_i, r_ct_i, mu_i, mc_i, mt_i = mass_ratios(M_i)
    print(f"\nm_u/m_c at τ=i = {r_uc_i:.6e}")
    print(f"m_c/m_t at τ=i = {r_ct_i:.6e}")

    # ── C. FIT at τ=i to find optimal parameters ──
    print(f"\n--- Optimal fit at τ=i (free β/α, γ/α, δ/α) ---")
    # PDG targets at GUT scale (from context: m_u/m_t = 1.25e-5, m_c/m_t = 7.36e-3 at 2 GeV)
    # At GUT scale: m_u/m_t ~ 1.25e-5 * (RGE factor), m_c/m_t ~ 3.26e-3 (SM-derived GUT target)
    # Use PDG values at 2 GeV for fitting (then note GUT-scale equivalents)
    pdg_mc_mt_2gev = 7.36e-3   # m_c/m_t at 2 GeV (PDG)
    pdg_mu_mt_2gev = 1.25e-5   # m_u/m_t at 2 GeV (PDG)
    # GUT-scale target for m_c/m_t from H3 context: 3.26e-3
    gut_mc_mt = 3.26e-3
    gut_mu_mt = 1.25e-5 / 2.0  # approximate: m_u runs faster than m_c

    def chi2_fit(log_params):
        b_over_a = np.exp(log_params[0])
        g_over_a = np.exp(log_params[1])
        d_over_a = np.exp(log_params[2])
        # sign for gamma_u can be +/-; allow sign via tanh reparametrization
        try:
            M = M_u_unified(tau_i, 1.0, b_over_a, g_over_a, d_over_a)
            r_uc, r_ct, _, _, _ = mass_ratios(M)
            # Fit m_c/m_t and m_u/m_c with GUT-scale targets
            # m_c/m_t target: 3.26e-3 (GUT) or also check 2.72e-3 (LYD20 best)
            chi2 = ((np.log(r_ct) - np.log(gut_mc_mt)) / 0.3)**2 + \
                   ((np.log(r_uc * r_ct) - np.log(gut_mu_mt * gut_mc_mt / gut_mc_mt)) / 0.3)**2
            return chi2
        except:
            return 1e10

    # Grid search for starting point
    best_chi2 = 1e10
    best_params = None
    for lb in np.linspace(3, 8, 6):
        for lg in np.linspace(4, 10, 6):
            for ld in np.linspace(3, 8, 6):
                c = chi2_fit([lb, lg, ld])
                if c < best_chi2:
                    best_chi2 = c
                    best_params = [lb, lg, ld]

    result = minimize(chi2_fit, best_params, method='Nelder-Mead',
                      options={'xatol': 1e-8, 'fatol': 1e-12, 'maxiter': 100000})

    b_opt = np.exp(result.x[0])
    g_opt = np.exp(result.x[1])
    d_opt = np.exp(result.x[2])

    M_opt = M_u_unified(tau_i, 1.0, b_opt, g_opt, d_opt)
    r_uc_opt, r_ct_opt, _, _, _ = mass_ratios(M_opt)
    print(f"β/α = {b_opt:.2e}, γ/α = {g_opt:.2e}, δ/α = {d_opt:.2e}")
    print(f"m_u/m_c = {r_uc_opt:.4e},  m_c/m_t = {r_ct_opt:.4e}")
    print(f"GUT target: m_c/m_t = {gut_mc_mt:.3e}")
    print(f"χ² = {result.fun:.4f}")

    # ── D. ALSO: try with LYD20 sign conventions: γ_u can be negative ──
    print(f"\n--- Testing γ_u negative at τ=i with LYD20 parameters ---")
    M_i_neg = M_u_unified(tau_i, alpha_u_lyd, beta_u_lyd, -gamma_u_lyd, delta_u_lyd)
    r_uc_neg, r_ct_neg, _, _, _ = mass_ratios(M_i_neg)
    print(f"γ/α = -{gamma_u_lyd}: m_u/m_c = {r_uc_neg:.6e}, m_c/m_t = {r_ct_neg:.6e}")

    # ── E. SUMMARY ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"LYD20 best-fit τ={tau_lyd}:")
    print(f"  m_u/m_c = {r_uc_lyd:.4e}  (LYD20 quoted: 1.929e-3)  {'PASS' if abs(r_uc_lyd-0.001929)/0.001929 < 0.05 else 'FAIL'}")
    print(f"  m_c/m_t = {r_ct_lyd:.4e}  (LYD20 quoted: 2.725e-3)  {'PASS' if abs(r_ct_lyd-0.002725)/0.002725 < 0.05 else 'FAIL'}")
    print(f"\nτ = i with LYD20 best-fit parameters:")
    print(f"  m_u/m_c = {r_uc_i:.4e}")
    print(f"  m_c/m_t = {r_ct_i:.4e}")
    print(f"\nComparison:")
    print(f"  H3 Model VI at τ=i:       m_c/m_t ≈ 2.72e-3 (reproduced)")
    print(f"  SM-derived GUT target:    m_c/m_t ≈ 3.26e-3")
    print(f"  LYD20 unified model τ=i:  m_c/m_t = {r_ct_i:.4e}")

    gap_H3 = (3.26e-3 - 2.72e-3) / 3.26e-3 * 100
    gap_unified = (3.26e-3 - r_ct_i) / 3.26e-3 * 100
    print(f"  Gap in H3 Model VI: {gap_H3:.1f}%")
    print(f"  Gap in unified model at τ=i: {gap_unified:.1f}%")
