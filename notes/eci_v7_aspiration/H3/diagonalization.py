"""
H3.D — Diagonalization of M_u and fit to PDG quark masses.

Uses LYD20 Model VI mass matrix from mass_matrix.py.

PDG values used [PDG-2024-CITED-NOT-VERIFIED]:
  m_u(2 GeV, MS-bar) = 2.16 ± 0.49 MeV
  m_c(2 GeV, MS-bar) = 1.273 GeV
  m_t(pole)          = 172.69 GeV

LYD20 uses GUT-scale values (with SUSY threshold):
  m_u/m_c = (1.9286 ± 0.6017) × 10^{-3}
  m_c/m_t = (2.7247 ± 0.1200) × 10^{-3}
  [from LYD20 Eq. exp-data-quark, lines 1126-1131]

We fit both: (a) PDG MS-bar scale ratios, (b) LYD20 GUT-scale ratios.

FLAG: All PDG values marked [PDG-2024-CITED-NOT-VERIFIED] as instructed.
The LYD20 GUT-scale values come from arXiv:1310.5755 (Antusch-Maurer).
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.optimize import minimize
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from mass_matrix import M_u, M_d, modular_forms_weight1

# ─────────────────────────────────────────────────────────────────
# PDG target values [PDG-2024-CITED-NOT-VERIFIED]
# ─────────────────────────────────────────────────────────────────
# MS-bar at 2 GeV:
PDG_mu_2GeV = 2.16e-3   # GeV  [PDG-2024-CITED-NOT-VERIFIED]
PDG_mc_2GeV = 1.273      # GeV  [PDG-2024-CITED-NOT-VERIFIED]
PDG_mt_pole = 172.69     # GeV  [PDG-2024-CITED-NOT-VERIFIED]

# Ratios at 2 GeV scale:
PDG_mu_over_mc = PDG_mu_2GeV / PDG_mc_2GeV  # = 1.697e-3
PDG_mc_over_mt = PDG_mc_2GeV / PDG_mt_pole  # = 7.372e-3 (2GeV/pole — not GUT)

# LYD20 GUT-scale ratios (from Antusch-Maurer 2013 with tan β=7.5, SUSY at 1 TeV):
LYD20_mu_over_mc = 1.9286e-3   # [from LYD20 Eq. exp-data-quark]
LYD20_mu_over_mc_err = 0.6017e-3
LYD20_mc_over_mt = 2.7247e-3   # [from LYD20 Eq. exp-data-quark]
LYD20_mc_over_mt_err = 0.1200e-3

# ─────────────────────────────────────────────────────────────────
# Diagonalization utility
# ─────────────────────────────────────────────────────────────────

def singular_values_sorted(M):
    """Return singular values of M in ASCENDING order."""
    _, s, _ = np.linalg.svd(M)
    return np.sort(s)  # ascending: [m_u, m_c, m_t]

def mass_ratios(M):
    """Return (m_u/m_c, m_c/m_t) from singular values."""
    sv = singular_values_sorted(M)
    # sv[0]=m_u (lightest), sv[1]=m_c, sv[2]=m_t (heaviest)
    if sv[1] < 1e-30 or sv[2] < 1e-30:
        return 1e10, 1e10
    return sv[0] / sv[1], sv[1] / sv[2]

# ─────────────────────────────────────────────────────────────────
# χ² function for up-sector fit
# ─────────────────────────────────────────────────────────────────

def chi2_up(params, target='LYD20'):
    """
    χ² for fitting (m_u/m_c, m_c/m_t) in the up-sector.

    params = [Re(τ), Im(τ), log(β_u/α_u), log(γ_u/α_u)]
    We fix α_u = 1 (only ratios matter for mass ratios).
    """
    re_tau, im_tau, log_beta_ratio, log_gamma_ratio = params

    if im_tau < 0.1:  # enforce Im(τ) > 0
        return 1e10

    tau = re_tau + 1j * im_tau
    beta_u = exp(log_beta_ratio)   # β_u/α_u
    gamma_u = exp(log_gamma_ratio) # γ_u/α_u

    try:
        M = M_u(tau, 1.0, beta_u, gamma_u, n_terms=30)
        r1, r2 = mass_ratios(M)
    except Exception:
        return 1e10

    if target == 'LYD20':
        # Use LYD20 GUT-scale ratios with uncertainties
        chi2 = ((r1 - LYD20_mu_over_mc) / LYD20_mu_over_mc_err)**2 \
             + ((r2 - LYD20_mc_over_mt) / LYD20_mc_over_mt_err)**2
    elif target == 'PDG':
        # Use PDG 2 GeV ratios (rough, same uncertainty ~30%)
        sig_r1 = 0.3 * PDG_mu_over_mc
        sig_r2 = 0.05 * PDG_mc_over_mt  # less uncertainty on m_c/m_t
        chi2 = ((r1 - PDG_mu_over_mc) / sig_r1)**2 \
             + ((r2 - PDG_mc_over_mt) / sig_r2)**2
    else:
        raise ValueError(f"Unknown target: {target}")

    return chi2

# ─────────────────────────────────────────────────────────────────
# Fixed-τ evaluation
# ─────────────────────────────────────────────────────────────────

def evaluate_at_tau(tau, alpha_u=1.0, beta_ratio=62.2142, gamma_ratio=0.00104,
                    label="custom"):
    """Evaluate mass matrix and print singular values at a given τ."""
    M = M_u(tau, alpha_u, beta_ratio, gamma_ratio, n_terms=50)
    sv = singular_values_sorted(M)
    r1, r2 = mass_ratios(M)
    print(f"  τ = {tau} [{label}]")
    print(f"  Singular values (∝ m_u, m_c, m_t): {sv[0]:.4e}, {sv[1]:.4e}, {sv[2]:.4e}")
    print(f"  m_u/m_c = {r1:.4e}  (LYD20 target: {LYD20_mu_over_mc:.4e})")
    print(f"  m_c/m_t = {r2:.4e}  (LYD20 target: {LYD20_mc_over_mt:.4e})")
    print()
    return sv, r1, r2

# ─────────────────────────────────────────────────────────────────
# Main fitting routine
# ─────────────────────────────────────────────────────────────────

def fit_up_sector(target='LYD20', n_trials=20):
    """
    Minimize χ² over (τ, β_u/α_u, γ_u/α_u).
    Uses multiple random starts to avoid local minima.
    """
    print(f"\nFitting up-sector to {target} targets...")
    print(f"  Targets: m_u/m_c = {LYD20_mu_over_mc:.4e}, m_c/m_t = {LYD20_mc_over_mt:.4e}")

    best_chi2 = 1e20
    best_result = None

    # Random starts
    rng = np.random.RandomState(42)

    # Also try LYD20 best-fit as starting point
    starts = [
        [-0.4999, 0.8958, np.log(62.2142), np.log(0.00104)],  # LYD20 best fit Model VI
        [0.0, 1.0, np.log(50.0), np.log(0.001)],
        [0.0, 1.5, np.log(100.0), np.log(0.002)],
        [0.4, 0.9, np.log(80.0), np.log(0.005)],
        [-0.3, 1.5, np.log(200.0), np.log(0.0005)],
    ]

    # Add random starts
    for _ in range(n_trials):
        re_tau = rng.uniform(-0.5, 0.5)
        im_tau = rng.uniform(0.5, 3.0)
        log_beta = rng.uniform(2.0, 8.0)
        log_gamma = rng.uniform(-8.0, -2.0)
        starts.append([re_tau, im_tau, log_beta, log_gamma])

    for x0 in starts:
        try:
            result = minimize(
                chi2_up, x0,
                args=(target,),
                method='Nelder-Mead',
                options={'maxiter': 10000, 'xatol': 1e-8, 'fatol': 1e-8}
            )
            if result.fun < best_chi2:
                best_chi2 = result.fun
                best_result = result
        except Exception:
            continue

    if best_result is None:
        print("  FAILED: No successful optimization")
        return None

    p = best_result.x
    re_tau, im_tau, log_beta, log_gamma = p
    tau_fit = re_tau + 1j * im_tau
    beta_fit = exp(log_beta)
    gamma_fit = exp(log_gamma)

    print(f"\n  Best fit:")
    print(f"    τ = {re_tau:.6f} + {im_tau:.6f}i")
    print(f"    β_u/α_u = {beta_fit:.4f}")
    print(f"    γ_u/α_u = {gamma_fit:.6f}")

    M = M_u(tau_fit, 1.0, beta_fit, gamma_fit, n_terms=50)
    sv = singular_values_sorted(M)
    r1, r2 = mass_ratios(M)

    print(f"\n  Predictions:")
    print(f"    m_u/m_c = {r1:.4e}  (target: {LYD20_mu_over_mc:.4e})")
    print(f"    m_c/m_t = {r2:.4e}  (target: {LYD20_mc_over_mt:.4e})")
    print(f"    χ² = {best_chi2:.3f}")
    print(f"    χ²/dof = {best_chi2/2:.3f}  (2 observables, 4 params = 2 DOF)")

    # m_u/m_c as falsifiability test
    if target == 'PDG':
        print(f"\n  Falsifiability (m_u/m_c) [PDG-2024-CITED-NOT-VERIFIED]:")
        print(f"    Prediction: m_u/m_c = {r1:.4e}")
        print(f"    PDG target: m_u/m_c = {PDG_mu_over_mc:.4e}")
        pull = (r1 - PDG_mu_over_mc) / (0.3 * PDG_mu_over_mc)
        print(f"    Pull: {pull:.2f}σ")

    return {
        'tau': tau_fit,
        'beta_ratio': beta_fit,
        'gamma_ratio': gamma_fit,
        'chi2': best_chi2,
        'r1': r1,
        'r2': r2,
        'sv': sv,
    }

# ─────────────────────────────────────────────────────────────────
# CKM angle estimation (Cabibbo angle θ_C from m_d/m_s structure)
# ─────────────────────────────────────────────────────────────────

def estimate_cabibbo(tau, alpha_u=1.0, beta_u_ratio=62.2142, gamma_u_ratio=0.00104,
                     alpha_d=1.0, beta_d_ratio=0.7378,
                     gamma_d1_ratio=1.4946, gamma_d2=-0.1958-0.2762j):
    """
    Estimate Cabibbo angle θ_12 from up and down mass matrices.
    Uses LYD20 Model VI best-fit parameters.

    The CKM matrix V = U_u† U_d where M_u = U_u S_u V_u† and M_d = U_d S_d V_d†
    are SVDs. θ_C ≈ |V_{us}| ≈ |V[0,1]|.
    """
    Mu = M_u(tau, alpha_u, beta_u_ratio, gamma_u_ratio)
    Md = M_d(tau, alpha_d, beta_d_ratio, gamma_d1_ratio, gamma_d2)

    # SVD: M = U S Vh, so left singular vectors in U
    U_u, _, _ = np.linalg.svd(Mu)
    U_d, _, _ = np.linalg.svd(Md)

    # CKM = U_u† U_d (in standard convention)
    CKM = U_u.conj().T @ U_d

    theta_12 = abs(CKM[0, 1])
    theta_13 = abs(CKM[0, 2])
    theta_23 = abs(CKM[1, 2])

    print(f"  CKM angles at τ={tau}:")
    print(f"    |V_us| (θ_12 ≈ Cabibbo): {theta_12:.5f}")
    print(f"    |V_ub| (θ_13):            {theta_13:.5f}")
    print(f"    |V_cb| (θ_23):            {theta_23:.5f}")
    print(f"  LYD20 best-fit predictions:")
    print(f"    θ_12 = 0.22731, θ_13 = 0.00298, θ_23 = 0.04873")
    print(f"  PDG [PDG-2024-CITED-NOT-VERIFIED]:")
    print(f"    θ_12 ≈ 0.2265, θ_13 ≈ 0.0036, θ_23 ≈ 0.0421")

    return CKM

# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("H3.D — Diagonalization and Quark Mass Fit")
    print("=" * 60)

    # ── Section 1: Fixed-τ evaluations ──────────────────────────
    print("\n--- Fixed-τ evaluations (LYD20 best-fit coupling ratios) ---")
    print("Using β_u/α_u = 62.2142, γ_u/α_u = 0.00104 (LYD20 Model VI best fit)\n")

    # τ = i (square fixed point)
    sv_i, r1_i, r2_i = evaluate_at_tau(1j, label="square fixed point S: τ=i")

    # τ = ω = exp(2πi/3) = -1/2 + i√3/2 (cube root of unity, fixed point of ST)
    tau_omega = exp(2j * pi / 3)
    sv_w, r1_w, r2_w = evaluate_at_tau(tau_omega, label="cube root of unity ST: τ=ω")

    # τ → i∞ approximated by large Im(τ)
    tau_inf = 0 + 5j   # Im(τ)=5 is effectively i∞ for leading terms
    sv_inf, r1_inf, r2_inf = evaluate_at_tau(tau_inf, label="τ→i∞ approx (Im τ=5)")

    # LYD20 best-fit τ
    tau_bf = -0.4999 + 0.8958j
    sv_bf, r1_bf, r2_bf = evaluate_at_tau(tau_bf, label="LYD20 best-fit τ")

    # ── Section 2: Numerical fit to LYD20 GUT-scale targets ─────
    print("\n--- Fitting to LYD20 GUT-scale ratios ---")
    result_lyd = fit_up_sector(target='LYD20', n_trials=30)

    # ── Section 3: Numerical fit to PDG 2 GeV targets ───────────
    print("\n--- Fitting to PDG 2 GeV ratios [PDG-2024-CITED-NOT-VERIFIED] ---")
    print(f"PDG targets:")
    print(f"  m_u(2GeV) = {PDG_mu_2GeV*1000:.2f} MeV [PDG-2024-CITED-NOT-VERIFIED]")
    print(f"  m_c(2GeV) = {PDG_mc_2GeV:.3f} GeV [PDG-2024-CITED-NOT-VERIFIED]")
    print(f"  m_t(pole) = {PDG_mt_pole:.2f} GeV [PDG-2024-CITED-NOT-VERIFIED]")
    print(f"  m_u/m_c   = {PDG_mu_over_mc:.4e}")
    print(f"  m_c/m_t   = {PDG_mc_over_mt:.4e}")

    result_pdg = fit_up_sector(target='PDG', n_trials=30)

    # ── Section 4: CKM Cabibbo angle ────────────────────────────
    print("\n--- CKM Cabibbo angle estimation at LYD20 best-fit τ ---")
    CKM = estimate_cabibbo(
        tau=tau_bf,
        alpha_u=1.0, beta_u_ratio=62.2142, gamma_u_ratio=0.00104,
        alpha_d=1.0, beta_d_ratio=0.7378,
        gamma_d1_ratio=1.4946, gamma_d2=-0.1958-0.2762j
    )

    # ── Section 5: Summary table ─────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'τ value':<30} {'m_u/m_c':>12} {'m_c/m_t':>12}")
    print("-" * 60)
    print(f"{'LYD20 target (GUT scale)':<30} {LYD20_mu_over_mc:>12.4e} {LYD20_mc_over_mt:>12.4e}")
    print(f"{'PDG 2 GeV [NOT-VERIFIED]':<30} {PDG_mu_over_mc:>12.4e} {PDG_mc_over_mt:>12.4e}")
    print(f"{'τ = i (sq. fixed pt)':<30} {r1_i:>12.4e} {r2_i:>12.4e}")
    print(f"{'τ = ω (ST fixed pt)':<30} {r1_w:>12.4e} {r2_w:>12.4e}")
    print(f"{'τ → i∞ (Im τ = 5)':<30} {r1_inf:>12.4e} {r2_inf:>12.4e}")
    print(f"{'LYD20 best-fit τ':<30} {r1_bf:>12.4e} {r2_bf:>12.4e}")
    if result_lyd:
        r1l, r2l, c2l = result_lyd['r1'], result_lyd['r2'], result_lyd['chi2']
        print(f"{'Our fit (LYD20 targets)':<30} {r1l:>12.4e} {r2l:>12.4e}  chi2={c2l:.2f}")
    if result_pdg:
        r1p, r2p, c2p = result_pdg['r1'], result_pdg['r2'], result_pdg['chi2']
        print(f"{'Our fit (PDG targets)':<30} {r1p:>12.4e} {r2p:>12.4e}  chi2={c2p:.2f}")

    print("\n[PDG-2024-CITED-NOT-VERIFIED]: All PDG values above need verification")
    print("against a fresh PDG publication before use in submitted papers.")
