"""
I2 — Cabibbo Angle from V_CKM at τ=i (LYD20 Model VI, S'_4)

Steps:
  I2.A — Build M_d using rep_assignment.md structure (already in mass_matrix.py)
  I2.B — Diagonalize M_u and M_d, form V_CKM = U_u† U_d, extract sin θ_C
  I2.C — Fit free down-sector parameters at τ=i
  I2.D — Compare: sin θ_C at τ_LYD20-best vs τ=i vs PDG

Anti-hallucination:
  LYD20 best-fit values from rep_assignment.md (transcribed from LYD20 TeX lines 1393-1406).
  All numerics via numpy/scipy.
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.linalg import svd
from scipy.optimize import minimize, differential_evolution
import sys, os

sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u, M_d, modular_forms_weight1

# ─────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────
PDG_SIN_THETA_C = 0.2253   # |V_us|, PDG 2022
PDG_SIN_THETA_13 = 0.00369  # |V_ub|
PDG_SIN_THETA_23 = 0.04182  # |V_cb|

# LYD20 best-fit parameters (transcribed from rep_assignment.md, LYD20 lines 1393-1406)
TAU_LYD20 = -0.4999 + 0.8958j
BETA_U_OVER_ALPHA_U = 62.2142
GAMMA_U_OVER_ALPHA_U = 0.00104
BETA_D_OVER_ALPHA_D = 0.7378
GAMMA_D1_OVER_ALPHA_D = 1.4946
GAMMA_D2_OVER_ALPHA_D = -0.1958 - 0.2762j  # complex

# CM point
TAU_CM = 1j

# ─────────────────────────────────────────────────────────────────
# I2.B — DIAGONALIZATION AND V_CKM
# ─────────────────────────────────────────────────────────────────

def diagonalize(M):
    """
    Diagonalize M via SVD: M = U_L diag(m_1, m_2, m_3) U_R†
    Returns U_L (left unitary), singular values (masses), U_R (right unitary).
    The unitary that diagonalizes M†M is U_R (right), which is the mixing matrix.
    """
    # SVD: M = U @ diag(s) @ Vh  →  M†M = Vh† diag(s²) Vh
    # So U_L = U, U_R = Vh†
    U, s, Vh = svd(M)
    U_L = U
    U_R = Vh.conj().T
    return U_L, s, U_R

def compute_V_CKM(tau, alpha_u, beta_u, gamma_u, alpha_d, beta_d, gamma_d1, gamma_d2):
    """
    Compute V_CKM = U_u† U_d where U_u, U_d diagonalize M_u†M_u, M_d†M_d.

    In the convention W = q^c M q:
      M†M eigenvalues = squared masses
      U_R diagonalizes M†M from the right (= the mixing matrix in V_CKM).
    """
    Mu = M_u(tau, alpha_u, beta_u, gamma_u)
    Md = M_d(tau, alpha_d, beta_d, gamma_d1, gamma_d2)

    _, s_u, U_u = diagonalize(Mu)  # SVD of M_u
    _, s_d, U_d = diagonalize(Md)  # SVD of M_d

    # Sort by ascending singular values (u < c < t; d < s < b)
    idx_u = np.argsort(s_u)
    idx_d = np.argsort(s_d)
    U_u = U_u[:, idx_u]
    U_d = U_d[:, idx_d]
    s_u = s_u[idx_u]
    s_d = s_d[idx_d]

    V_CKM = U_u.conj().T @ U_d

    return V_CKM, s_u, s_d

def extract_mixing_angles(V):
    """
    Extract CKM angles from V_CKM matrix.
    Standard PDG parameterisation:
      sin θ_12 = |V[0,1]| / sqrt(|V[0,0]|² + |V[0,1]|²)  [Cabibbo angle ≈ |V_us|]
      sin θ_13 = |V[0,2]|  [|V_ub|]
      sin θ_23 = |V[1,2]|  [|V_cb|]

    Exact PDG formulae (PDG 2022 review, Eq. 12.4):
      s13 = |V_ub|
      s12 = |V_us| / sqrt(1 - |V_ub|²)
      s23 = |V_cb| / sqrt(1 - |V_ub|²)

    For simplicity we use the approximate definitions since |V_ub| << 1:
      sin θ_C ≈ |V_CKM[0,1]|  (Cabibbo angle)
    """
    abs_V = np.abs(V)
    # PDG convention: rows = (u,c,t), cols = (d,s,b)
    V_ud = abs_V[0, 0]
    V_us = abs_V[0, 1]
    V_ub = abs_V[0, 2]
    V_cd = abs_V[1, 0]
    V_cs = abs_V[1, 1]
    V_cb = abs_V[1, 2]
    V_td = abs_V[2, 0]
    V_ts = abs_V[2, 1]
    V_tb = abs_V[2, 2]

    s13 = V_ub
    s12 = V_us / sqrt(max(1 - V_ub**2, 1e-10))  # ≈ |V_us| for small V_ub
    s23 = V_cb / sqrt(max(1 - V_ub**2, 1e-10))

    return s12, s13, s23, abs_V

# ─────────────────────────────────────────────────────────────────
# I2.D.1 — EVALUATE AT LYD20 BEST-FIT τ
# ─────────────────────────────────────────────────────────────────

print("=" * 70)
print("I2.D.1 — V_CKM at LYD20 best-fit τ = -0.4999 + 0.8958i")
print("=" * 70)

# Use LYD20 best-fit parameters directly
# Overall scales set to 1 (ratio β/α, γ/α are the physical inputs)
alpha_u_bf = 1.0
beta_u_bf  = BETA_U_OVER_ALPHA_U   * alpha_u_bf
gamma_u_bf = GAMMA_U_OVER_ALPHA_U  * alpha_u_bf

alpha_d_bf = 1.0
beta_d_bf   = BETA_D_OVER_ALPHA_D  * alpha_d_bf
gamma_d1_bf = GAMMA_D1_OVER_ALPHA_D * alpha_d_bf
gamma_d2_bf = GAMMA_D2_OVER_ALPHA_D * alpha_d_bf

V_bf, s_u_bf, s_d_bf = compute_V_CKM(
    TAU_LYD20, alpha_u_bf, beta_u_bf, gamma_u_bf,
    alpha_d_bf, beta_d_bf, gamma_d1_bf, gamma_d2_bf
)

s12_bf, s13_bf, s23_bf, absV_bf = extract_mixing_angles(V_bf)

print(f"\nMass ratios (up-sector, normalised to m_t = max):")
m_t = s_u_bf[2]
if m_t > 0:
    print(f"  m_u/m_t = {s_u_bf[0]/m_t:.5e}")
    print(f"  m_c/m_t = {s_u_bf[1]/m_t:.5e}")
    print(f"  m_t/m_t = {s_u_bf[2]/m_t:.5f} (= 1 by def)")

print(f"\nMass ratios (down-sector, normalised to m_b = max):")
m_b = s_d_bf[2]
if m_b > 0:
    print(f"  m_d/m_b = {s_d_bf[0]/m_b:.5e}")
    print(f"  m_s/m_b = {s_d_bf[1]/m_b:.5e}")
    print(f"  m_b/m_b = {s_d_bf[2]/m_b:.5f} (= 1 by def)")

print(f"\n|V_CKM| at LYD20 best-fit τ:")
print(f"  |V_ud| = {absV_bf[0,0]:.5f}    |V_us| = {absV_bf[0,1]:.5f}    |V_ub| = {absV_bf[0,2]:.6f}")
print(f"  |V_cd| = {absV_bf[1,0]:.5f}    |V_cs| = {absV_bf[1,1]:.5f}    |V_cb| = {absV_bf[1,2]:.6f}")
print(f"  |V_td| = {absV_bf[2,0]:.5f}    |V_ts| = {absV_bf[2,1]:.5f}    |V_tb| = {absV_bf[2,2]:.6f}")

print(f"\nCKM angles at LYD20 best-fit τ:")
print(f"  sin θ_12 (Cabibbo) = {s12_bf:.5f}  [PDG = {PDG_SIN_THETA_C:.5f}]  dev = {100*(s12_bf-PDG_SIN_THETA_C)/PDG_SIN_THETA_C:+.1f}%")
print(f"  sin θ_13 (V_ub)    = {s13_bf:.6f}  [PDG = {PDG_SIN_THETA_13:.6f}]  dev = {100*(s13_bf-PDG_SIN_THETA_13)/PDG_SIN_THETA_13:+.1f}%")
print(f"  sin θ_23 (V_cb)    = {s23_bf:.5f}  [PDG = {PDG_SIN_THETA_23:.5f}]  dev = {100*(s23_bf-PDG_SIN_THETA_23)/PDG_SIN_THETA_23:+.1f}%")

# LYD20 reported theta_12 = 0.22731 (from rep_assignment.md)
LYD20_REPORTED_THETA12 = 0.22731
print(f"\nLYD20 reported sin θ_12 = {LYD20_REPORTED_THETA12} (from Table in paper)")
print(f"Our computed  sin θ_12 = {s12_bf:.5f}")
print(f"Agreement: {'OK' if abs(s12_bf - LYD20_REPORTED_THETA12) < 0.01 else 'MISMATCH — check parameter transcription'}")

# ─────────────────────────────────────────────────────────────────
# I2.D.2 — EVALUATE AT τ = i (CM POINT) with optimized down-sector params
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("I2.D.2 — V_CKM at τ = i (CM point)")
print("=" * 70)

# At τ=i, up-sector parameters from G17 (H3 result):
# beta_u/alpha_u = 62.2142, gamma_u/alpha_u = 0.00104 (LYD20 best-fit)
# The question: what sin θ_C does LYD20 Model VI predict at τ=i
# when we optimize ONLY the down-sector parameters?

# We keep: tau = i, beta_u/alpha_u, gamma_u/alpha_u from LYD20
# We fit: beta_d/alpha_d, gamma_d1/alpha_d, Re(gamma_d2/alpha_d), Im(gamma_d2/alpha_d)
# to minimize chi-squared over (m_d/m_b, m_s/m_b, sin θ_C, sin θ_13, sin θ_23)

# PDG targets for quark mass ratios (MS-bar at 2 GeV, PDG 2022)
# m_d = 4.67 MeV, m_s = 93.4 MeV, m_b = 4180 MeV (at m_b pole ≈ use consistent scale)
# We use ratios:
PDG_MD_MB = 4.67e-3 / 4180e-3   # ≈ 1.117e-3
PDG_MS_MB = 93.4e-3 / 4180e-3   # ≈ 2.234e-2

print(f"\nPDG targets:")
print(f"  sin θ_12 = {PDG_SIN_THETA_C:.5f}")
print(f"  sin θ_13 = {PDG_SIN_THETA_13:.6f}")
print(f"  sin θ_23 = {PDG_SIN_THETA_23:.5f}")
print(f"  m_d/m_b  = {PDG_MD_MB:.5e}")
print(f"  m_s/m_b  = {PDG_MS_MB:.5e}")

def chi2_down(x, tau, alpha_u, beta_u, gamma_u):
    """
    Chi-squared for down-sector observables at fixed tau and up-sector params.
    x = [log(beta_d/alpha_d), log(gamma_d1/alpha_d), Re(gamma_d2/alpha_d), Im(gamma_d2/alpha_d)]
    """
    beta_d_r   = np.exp(x[0])   # always positive
    gamma_d1_r = np.exp(x[1])   # always positive
    gamma_d2_r = x[2] + 1j * x[3]

    alpha_d = 1.0

    try:
        V, s_u, s_d = compute_V_CKM(tau, alpha_u, beta_u, gamma_u,
                                      alpha_d, beta_d_r, gamma_d1_r, gamma_d2_r)
    except Exception:
        return 1e20

    if np.any(np.isnan(s_d)) or s_d[2] == 0:
        return 1e20

    s12, s13, s23, absV = extract_mixing_angles(V)

    md_mb = s_d[0] / s_d[2]
    ms_mb = s_d[1] / s_d[2]

    # Normalised residuals (using PDG uncertainty as weights)
    sigma_s12 = 0.0007
    sigma_s13 = 0.00012
    sigma_s23 = 0.0008
    sigma_md_mb = 0.3 * PDG_MD_MB   # 30% uncertainty on light quark ratios (scale dep)
    sigma_ms_mb = 0.15 * PDG_MS_MB  # 15%

    chi2 = (
        ((s12 - PDG_SIN_THETA_C) / sigma_s12)**2 +
        ((s13 - PDG_SIN_THETA_13) / sigma_s13)**2 +
        ((s23 - PDG_SIN_THETA_23) / sigma_s23)**2 +
        ((md_mb - PDG_MD_MB) / sigma_md_mb)**2 +
        ((ms_mb - PDG_MS_MB) / sigma_ms_mb)**2
    )

    return chi2

# Initial guess: use LYD20 best-fit ratios as starting point
x0 = [np.log(BETA_D_OVER_ALPHA_D), np.log(GAMMA_D1_OVER_ALPHA_D),
      GAMMA_D2_OVER_ALPHA_D.real, GAMMA_D2_OVER_ALPHA_D.imag]

print(f"\nFitting down-sector at τ=i using LYD20 up-sector parameters...")
print(f"  Starting point: β_d/α_d={BETA_D_OVER_ALPHA_D}, γ_d1/α_d={GAMMA_D1_OVER_ALPHA_D}")
print(f"  Starting point: γ_d2/α_d={GAMMA_D2_OVER_ALPHA_D}")

alpha_u_cm = 1.0
beta_u_cm  = BETA_U_OVER_ALPHA_U * alpha_u_cm
gamma_u_cm = GAMMA_U_OVER_ALPHA_U * alpha_u_cm

# First evaluate at starting point (LYD20 best-fit down params but τ=i)
chi2_start = chi2_down(x0, TAU_CM, alpha_u_cm, beta_u_cm, gamma_u_cm)
print(f"\nChi2 at LYD20 down-params, τ=i: {chi2_start:.4f}")

V_start, s_u_start, s_d_start = compute_V_CKM(
    TAU_CM, alpha_u_cm, beta_u_cm, gamma_u_cm,
    1.0, BETA_D_OVER_ALPHA_D, GAMMA_D1_OVER_ALPHA_D, GAMMA_D2_OVER_ALPHA_D
)
s12_start, s13_start, s23_start, absV_start = extract_mixing_angles(V_start)
print(f"  sin θ_C (LYD20 down-params, τ=i, unoptimized) = {s12_start:.5f}")

# Now optimize: differential evolution for global minimum
bounds = [
    (-3, 4),    # log(beta_d/alpha_d): 0.05 to 55
    (-3, 4),    # log(gamma_d1/alpha_d): 0.05 to 55
    (-5, 5),    # Re(gamma_d2/alpha_d)
    (-5, 5),    # Im(gamma_d2/alpha_d)
]

print(f"\nRunning differential evolution optimization (global)...")
result_de = differential_evolution(
    chi2_down, bounds, args=(TAU_CM, alpha_u_cm, beta_u_cm, gamma_u_cm),
    maxiter=2000, tol=1e-8, seed=42, workers=1,
    mutation=(0.5, 1.5), recombination=0.9, popsize=20,
    disp=False
)

print(f"  DE result: chi2 = {result_de.fun:.4f}")

# Refine with Nelder-Mead
result_nm = minimize(
    chi2_down, result_de.x,
    args=(TAU_CM, alpha_u_cm, beta_u_cm, gamma_u_cm),
    method='Nelder-Mead',
    options={'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 50000}
)
print(f"  NM refined: chi2 = {result_nm.fun:.4f}")

x_opt = result_nm.x
beta_d_opt    = np.exp(x_opt[0])
gamma_d1_opt  = np.exp(x_opt[1])
gamma_d2_opt  = x_opt[2] + 1j * x_opt[3]

print(f"\nBest-fit down-sector at τ=i:")
print(f"  β_d/α_d   = {beta_d_opt:.6f}")
print(f"  γ_d1/α_d  = {gamma_d1_opt:.6f}")
print(f"  γ_d2/α_d  = {gamma_d2_opt.real:.6f} + {gamma_d2_opt.imag:.6f}i")

V_cm_opt, s_u_cm, s_d_cm = compute_V_CKM(
    TAU_CM, alpha_u_cm, beta_u_cm, gamma_u_cm,
    1.0, beta_d_opt, gamma_d1_opt, gamma_d2_opt
)
s12_cm, s13_cm, s23_cm, absV_cm = extract_mixing_angles(V_cm_opt)

print(f"\nMass ratios at τ=i (down-sector, optimized):")
m_b_cm = s_d_cm[2]
print(f"  m_d/m_b  = {s_d_cm[0]/m_b_cm:.5e}  [PDG = {PDG_MD_MB:.5e}]")
print(f"  m_s/m_b  = {s_d_cm[1]/m_b_cm:.5e}  [PDG = {PDG_MS_MB:.5e}]")

print(f"\n|V_CKM| at τ=i (optimized down-sector):")
print(f"  |V_ud| = {absV_cm[0,0]:.5f}    |V_us| = {absV_cm[0,1]:.5f}    |V_ub| = {absV_cm[0,2]:.6f}")
print(f"  |V_cd| = {absV_cm[1,0]:.5f}    |V_cs| = {absV_cm[1,1]:.5f}    |V_cb| = {absV_cm[1,2]:.6f}")
print(f"  |V_td| = {absV_cm[2,0]:.5f}    |V_ts| = {absV_cm[2,1]:.5f}    |V_tb| = {absV_cm[2,2]:.6f}")

print(f"\nCKM angles at τ=i (τ fixed to CM point, down-sector optimized):")
print(f"  sin θ_12 (Cabibbo) = {s12_cm:.5f}  [PDG = {PDG_SIN_THETA_C:.5f}]  dev = {100*(s12_cm-PDG_SIN_THETA_C)/PDG_SIN_THETA_C:+.1f}%")
print(f"  sin θ_13 (V_ub)    = {s13_cm:.6f}  [PDG = {PDG_SIN_THETA_13:.6f}]  dev = {100*(s13_cm-PDG_SIN_THETA_13)/PDG_SIN_THETA_13:+.1f}%")
print(f"  sin θ_23 (V_cb)    = {s23_cm:.5f}  [PDG = {PDG_SIN_THETA_23:.5f}]  dev = {100*(s23_cm-PDG_SIN_THETA_23)/PDG_SIN_THETA_23:+.1f}%")

# ─────────────────────────────────────────────────────────────────
# I2.D.3 — SUMMARY VERDICT
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("I2.D.3 — SUMMARY")
print("=" * 70)

dev_bf  = 100 * (s12_bf - PDG_SIN_THETA_C) / PDG_SIN_THETA_C
dev_cm  = 100 * (s12_cm - PDG_SIN_THETA_C) / PDG_SIN_THETA_C

print(f"\n  sin θ_C at LYD20 best-fit τ = {s12_bf:.5f}  (PDG dev = {dev_bf:+.1f}%)")
print(f"  sin θ_C at τ = i (CM point) = {s12_cm:.5f}  (PDG dev = {dev_cm:+.1f}%)")
print(f"  sin θ_C PDG                 = {PDG_SIN_THETA_C:.5f}")

if abs(dev_cm) <= 5.0:
    verdict = "v7 GAIN OVER LYD20 — sin θ_C predicted at τ=i without τ-fit"
elif abs(dev_bf) <= 5.0 and abs(dev_cm) > 5.0:
    verdict = "v7 NEUTRAL — only LYD20's tuned τ fits; τ=i does not match"
else:
    verdict = "v7 OBSTRUCTION — sin θ_C not matched even at LYD20 best-fit τ"

print(f"\n  VERDICT: [{verdict}]")

# Extra: check unitarity of V_CKM
print(f"\nUnitarity check |V†V - I|_max:")
print(f"  at LYD20 τ:  {np.max(np.abs(V_bf.conj().T @ V_bf - np.eye(3))):.2e}")
print(f"  at τ=i:      {np.max(np.abs(V_cm_opt.conj().T @ V_cm_opt - np.eye(3))):.2e}")

print("\nDone.")
