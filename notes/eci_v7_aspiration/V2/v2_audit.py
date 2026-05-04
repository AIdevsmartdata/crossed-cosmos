"""
V2 — Independent Audit of I2's sin θ_C "structural obstruction" at τ=i

FRESH CODE — does NOT import mass_matrix.py or any I2 module.

All formulas re-derived independently from:
  - LYD20 arXiv:2006.10722 (Liu, Yao, Ding 2020)
  - LYD20 Model VI: Q~3, u^c~1^, c^c~1, t^c~1^', d^c~1^, s^c~1^', b^c~1^
  - Modular forms: weight-1 seed Y1,Y2,Y3 via Dedekind eta functions
  - Higher-weight forms as polynomials in Y1,Y2,Y3

Tasks:
  V2.A — Collinearity of modular forms at τ=i (do all components have real ratios?)
  V2.B — Independent CKM computation at τ=i (fresh SVD, not using I2 code)
  V2.C — Alternative bases/convention tests
  V2.D — Verdict
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.linalg import svd
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("V2 — Independent Audit of I2's sin θ_C claim at τ=i")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────
# PDG 2022 values (PDG Review of Particle Physics 2022, Workman et al.)
# CKM matrix values from PDG Table 1 in CKM review (Tanabashi et al.)
# ─────────────────────────────────────────────────────────────────
PDG_SIN_T12 = 0.2253   # |V_us|, PDG 2022, CKM review
PDG_SIN_T13 = 0.00369  # |V_ub|, PDG 2022
PDG_SIN_T23 = 0.04182  # |V_cb|, PDG 2022
PDG_MC_MT   = 0.00268  # LYD20 Table I best fit
PDG_MU_MC   = 0.00204  # LYD20 Table I best fit
PDG_MD_MS   = 0.05182  # LYD20 Table I best fit
PDG_MS_MB   = 0.01309  # LYD20 Table I best fit

# LYD20 best-fit τ
TAU_LYD20 = -0.4999 + 0.8958j
TAU_CM    = 1j  # CM point τ=i (S fixed point)

# ─────────────────────────────────────────────────────────────────
# SECTION 1 — FRESH IMPLEMENTATION OF MODULAR FORMS
# Source: LYD20 §II, lines 296-395 (weight-1 seed via Dedekind eta)
# ─────────────────────────────────────────────────────────────────

def eta_func(tau, n_terms=80):
    """
    Dedekind eta function: η(τ) = q^{1/24} Π_{n=1}^∞ (1 - q^n), q = e^{2πiτ}
    """
    q = exp(2j * pi * tau)
    result = q ** (1.0/24.0)
    prod = 1.0 + 0j
    for n in range(1, n_terms + 1):
        prod *= (1.0 - q**n)
    return result * prod


def weight1_forms(tau, n_terms=80):
    """
    Weight-1 modular forms Y1, Y2, Y3 transforming as 3̂' of S'_4.
    Source: LYD20 arXiv:2006.10722, lines 296-330.

    Basis functions:
      e1(τ) = η(4τ)^4 / η(2τ)^2
      e2(τ) = η(2τ)^{10} / [η(4τ)^4 · η(τ)^4]
      e3(τ) = η(2τ)^4 / η(τ)^2

    Weight-1 triplet (LYD20 lines 317-330):
      Y1 = 4√2 e1 + i√2 e2 + 2√2(1-i) e3
      Y2 = -2√2(1+√3) ω² e1 - i(1-√3)/√2 ω² e2 + 2√2(1-i) ω² e3
      Y3 = 2√2(√3-1) ω e1 - i(1+√3)/√2 ω e2 + 2√2(1-i) ω e3
    where ω = e^{2πi/3}
    """
    e1 = eta_func(4*tau, n_terms)**4 / eta_func(2*tau, n_terms)**2
    e2 = (eta_func(2*tau, n_terms)**10 /
          (eta_func(4*tau, n_terms)**4 * eta_func(tau, n_terms)**4))
    e3 = eta_func(2*tau, n_terms)**4 / eta_func(tau, n_terms)**2

    omega = exp(2j*pi/3)
    s2 = sqrt(2.0)
    s3 = sqrt(3.0)

    Y1 = 4*s2*e1 + 1j*s2*e2 + 2*s2*(1 - 1j)*e3
    Y2 = (-2*s2*(1 + s3)*omega**2*e1
          - 1j*(1 - s3)/s2*omega**2*e2
          + 2*s2*(1 - 1j)*omega**2*e3)
    Y3 = (2*s2*(s3 - 1)*omega*e1
          - 1j*(1 + s3)/s2*omega*e2
          + 2*s2*(1 - 1j)*omega*e3)

    return Y1, Y2, Y3


def all_forms(Y1, Y2, Y3):
    """
    Compute all modular form components needed for LYD20 Model VI.
    Polynomials in (Y1, Y2, Y3) from LYD20 lines 346-395, 1850-1876.
    INDEPENDENT from mass_matrix.py — re-transcribed from LYD20.

    Used forms:
      Weight 1:  (Y1_1, Y1_2, Y1_3) = (Y1, Y2, Y3)
      Weight 2:  Y2_3 = 2Y1^2-2Y2Y3, Y2_4 = 2Y3^2-2Y1Y2, Y2_5 = 2Y2^2-2Y1Y3
      Weight 5:  Y5_3, Y5_4, Y5_5 (3̂ multiplet)
                 Y5_6, Y5_7, Y5_8 (3̂',I multiplet)
                 Y5_9, Y5_10, Y5_11 (3̂',II multiplet)
    """
    f = {}
    # Weight 1
    f['Y1_1'] = Y1
    f['Y1_2'] = Y2
    f['Y1_3'] = Y3

    # Weight 2 triplet (3): LYD20 lines 347-351
    f['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    f['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    f['Y2_5'] = 2*Y2**2 - 2*Y1*Y3

    # Weight 5 triplet (3̂): LYD20 lines 1866-1870
    f['Y5_3'] = 18*Y1**2*(-Y2**3 + Y3**3)
    f['Y5_4'] = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
                 + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
                 + 6*Y1**2*Y2**2*Y3)
    f['Y5_5'] = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
                 - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
                 - 6*Y1**2*Y2*Y3**2)

    # Weight 5 triplet (3̂',I): LYD20 lines 1871-1873
    f['Y5_6'] = (8*Y1**3*Y2*Y3 - 6*Y1**2*(Y2**3 + Y3**3)
                 + 2*Y2*Y3*(Y2**3 + Y3**3))
    f['Y5_7'] = (4*Y1**4*Y2 - 2*Y1*Y2**4 - 6*Y1**2*Y2**2*Y3
                 - 2*Y1**3*Y3**2 + 4*Y2**3*Y3**2 + 4*Y1*Y2*Y3**3
                 - 2*Y3**5)
    f['Y5_8'] = -2*(Y1**3*Y2**2 + Y2**5 - 2*Y1**4*Y3
                    + 3*Y1**2*Y2*Y3**2 - 2*Y2**2*Y3**3
                    + Y1*(-2*Y2**3*Y3 + Y3**4))

    # Weight 5 triplet (3̂',II): LYD20 lines 1874-1876
    D = Y1**4 + 3*Y2**2*Y3**2 - 2*Y1*(Y2**3 + Y3**3)
    f['Y5_9']  = 4*Y1*D
    f['Y5_10'] = 4*Y2*D
    f['Y5_11'] = 4*Y3*D

    return f


def build_Mu(tau, alpha_u, beta_u, gamma_u):
    """
    Build M_u for LYD20 Model VI.
    Row convention: rows = right-handed singlets (u^c, c^c, t^c).
    Columns = left-handed doublets Q = (Q1, Q2, Q3).

    M_u[0,:] = alpha_u * (Y1, Y3, Y2)   [u^c coupling to weight-1 3̂']
    M_u[1,:] = beta_u  * (Y2_3, Y2_5, Y2_4)  [c^c coupling to weight-2 3]
    M_u[2,:] = gamma_u * (Y5_3, Y5_5, Y5_4)  [t^c coupling to weight-5 3̂]

    Source: LYD20 Eq. (Mq_6), lines 1379-1384.
    """
    Y1, Y2, Y3 = weight1_forms(tau)
    f = all_forms(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = alpha_u * f['Y1_1']
    M[0, 1] = alpha_u * f['Y1_3']
    M[0, 2] = alpha_u * f['Y1_2']

    M[1, 0] = beta_u * f['Y2_3']
    M[1, 1] = beta_u * f['Y2_5']
    M[1, 2] = beta_u * f['Y2_4']

    M[2, 0] = gamma_u * f['Y5_3']
    M[2, 1] = gamma_u * f['Y5_5']
    M[2, 2] = gamma_u * f['Y5_4']

    return M


def build_Md(tau, alpha_d, beta_d, gamma_d1, gamma_d2):
    """
    Build M_d for LYD20 Model VI.

    M_d[0,:] = alpha_d * (Y1, Y3, Y2)    [d^c, weight-1 3̂']
    M_d[1,:] = beta_d  * (Y5_3, Y5_5, Y5_4)  [s^c, weight-5 3̂]
    M_d[2,:] = gamma_d1*(Y5_6, Y5_8, Y5_7) + gamma_d2*(Y5_9, Y5_11, Y5_10)
                                              [b^c, weight-5 3̂',I + 3̂',II]

    Source: LYD20 Eq. (Mq_6), lines 1385-1389.
    """
    Y1, Y2, Y3 = weight1_forms(tau)
    f = all_forms(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = alpha_d * f['Y1_1']
    M[0, 1] = alpha_d * f['Y1_3']
    M[0, 2] = alpha_d * f['Y1_2']

    M[1, 0] = beta_d * f['Y5_3']
    M[1, 1] = beta_d * f['Y5_5']
    M[1, 2] = beta_d * f['Y5_4']

    M[2, 0] = gamma_d1 * f['Y5_6'] + gamma_d2 * f['Y5_9']
    M[2, 1] = gamma_d1 * f['Y5_8'] + gamma_d2 * f['Y5_11']
    M[2, 2] = gamma_d1 * f['Y5_7'] + gamma_d2 * f['Y5_10']

    return M


def compute_ckm(Mu, Md):
    """
    V_CKM = U_uL† U_dL where U_L is the LEFT singular vector matrix
    of M (rows = left-handed doublets Q).

    SVD convention: M = U diag(s) V†
      U[:, i] = left singular vectors  (these are U_L in W = q^c M Q basis)

    Sort by ascending singular values (lightest first: u < c < t).
    """
    Uu, su, _ = svd(Mu)
    Ud, sd, _ = svd(Md)

    # Sort ascending
    iu = np.argsort(su)
    id_ = np.argsort(sd)
    Uu = Uu[:, iu]
    Ud = Ud[:, id_]
    su = su[iu]
    sd = sd[id_]

    V = Uu.conj().T @ Ud
    return V, su, sd


def extract_angles(V):
    """Extract CKM angles (PDG 2022 convention). Rows = (u,c,t), cols = (d,s,b)."""
    aV = np.abs(V)
    s13 = aV[0, 2]
    denom = sqrt(max(1.0 - s13**2, 1e-20))
    s12 = aV[0, 1] / denom
    s23 = aV[1, 2] / denom
    return s12, s13, s23, aV


# ─────────────────────────────────────────────────────────────────
# V2.A — COLLINEARITY AUDIT at τ=i
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("V2.A — Collinearity of modular form multiplets at τ=i")
print("─" * 60)

tau = TAU_CM
Y1, Y2, Y3 = weight1_forms(tau)

print(f"\nWeight-1 seed forms at τ=i:")
print(f"  Y1 = {Y1:.6f}  arg = {np.angle(Y1)*180/pi:.2f}°")
print(f"  Y2 = {Y2:.6f}  arg = {np.angle(Y2)*180/pi:.2f}°")
print(f"  Y3 = {Y3:.6f}  arg = {np.angle(Y3)*180/pi:.2f}°")

# Verify constraint Y1^2 + 2*Y2*Y3 = 0
constr = Y1**2 + 2*Y2*Y3
print(f"\nModular form constraint Y1^2 + 2*Y2*Y3 = {abs(constr):.2e} (should be ~0)")

# Collinearity = are ratios real?
print(f"\nWeight-1 intra-multiplet ratios (real = collinear):")
r21 = Y2/Y1
r31 = Y3/Y1
print(f"  Y2/Y1 = {r21:.8f}  |Im/Re| = {abs(r21.imag/r21.real):.2e}")
print(f"  Y3/Y1 = {r31:.8f}  |Im/Re| = {abs(r31.imag/r31.real):.2e}")
print(f"  -> All weight-1 forms collinear (real ratios): {abs(r21.imag) < 1e-10 and abs(r31.imag) < 1e-10}")

f = all_forms(Y1, Y2, Y3)

print(f"\nWeight-2 triplet (Y2_3, Y2_4, Y2_5) at τ=i:")
for k in ['Y2_3', 'Y2_4', 'Y2_5']:
    print(f"  {k} = {f[k]:.6f}  arg = {np.angle(f[k])*180/pi:.2f}°")
r_23_24 = f['Y2_4'] / f['Y2_3'] if abs(f['Y2_3']) > 1e-30 else float('nan')
r_23_25 = f['Y2_5'] / f['Y2_3'] if abs(f['Y2_3']) > 1e-30 else float('nan')
print(f"  Y2_4/Y2_3 = {r_23_24:.8f}  |Im/Re| = {abs(r_23_24.imag/r_23_24.real):.2e}")
print(f"  Y2_5/Y2_3 = {r_23_25:.8f}  |Im/Re| = {abs(r_23_25.imag/r_23_25.real):.2e}")
print(f"  -> Weight-2 triplet collinear: {abs(r_23_24.imag) < 1e-8 and abs(r_23_25.imag) < 1e-8}")

print(f"\nWeight-5 triplet 3̂ (Y5_3, Y5_4, Y5_5) at τ=i:")
for k in ['Y5_3', 'Y5_4', 'Y5_5']:
    print(f"  {k} = {f[k]:.6f}  arg = {np.angle(f[k])*180/pi:.2f}°")
if abs(f['Y5_3']) > 1e-30:
    r_35_34 = f['Y5_4'] / f['Y5_3']
    r_35_35 = f['Y5_5'] / f['Y5_3']
    print(f"  Y5_4/Y5_3 = {r_35_34:.8f}  |Im/Re| = {abs(r_35_34.imag/max(abs(r_35_34.real),1e-30)):.2e}")
    print(f"  Y5_5/Y5_3 = {r_35_35:.8f}  |Im/Re| = {abs(r_35_35.imag/max(abs(r_35_35.real),1e-30)):.2e}")
    print(f"  -> Weight-5 3̂ triplet collinear: {abs(r_35_34.imag) < 1e-6 and abs(r_35_35.imag) < 1e-6}")
else:
    print("  Y5_3 ≈ 0 — need different reference element")

print(f"\nWeight-5 triplet 3̂',I (Y5_6, Y5_7, Y5_8) at τ=i:")
for k in ['Y5_6', 'Y5_7', 'Y5_8']:
    print(f"  {k} = {f[k]:.6f}  arg = {np.angle(f[k])*180/pi:.2f}°")

print(f"\nWeight-5 triplet 3̂',II (Y5_9, Y5_10, Y5_11) at τ=i:")
for k in ['Y5_9', 'Y5_10', 'Y5_11']:
    print(f"  {k} = {f[k]:.6f}  arg = {np.angle(f[k])*180/pi:.2f}°")

# ─────────────────────────────────────────────────────────────────
# Summary of phases to understand phase pattern
# ─────────────────────────────────────────────────────────────────

print("\nPhase summary (degrees) for all used forms at τ=i:")
for k in ['Y1_1', 'Y1_2', 'Y1_3',
          'Y2_3', 'Y2_4', 'Y2_5',
          'Y5_3', 'Y5_4', 'Y5_5',
          'Y5_6', 'Y5_7', 'Y5_8',
          'Y5_9', 'Y5_10', 'Y5_11']:
    v = f[k]
    if abs(v) > 1e-20:
        print(f"  {k:8s}: |val|={abs(v):.4e}  arg={np.angle(v)*180/pi:+7.2f}°")
    else:
        print(f"  {k:8s}: ≈ 0")

# ─────────────────────────────────────────────────────────────────
# V2.B — INDEPENDENT V_CKM COMPUTATION AT τ=i
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("V2.B — Independent CKM computation at τ=i")
print("─" * 60)

# Step B1: Verify that up-sector can fit mass ratios at τ=i
# I2's "re-fitted" values: β/α ≈ 100, γ/α ≈ 590 (approximately)
# We independently re-fit using a fresh optimizer

def chi2_up(log_params, tau):
    """
    Fit up-sector mass ratios at fixed τ.
    log_params = [log(β_u/α_u), log(γ_u/α_u)]
    Target: m_c/m_t = 0.00268, m_u/m_c = 0.00204
    """
    bu = exp(log_params[0])
    gu = exp(log_params[1])
    Mu = build_Mu(tau, 1.0, bu, gu)
    _, su, _ = svd(Mu)
    su = np.sort(su)
    if su[2] == 0 or su[1] == 0:
        return 1e20
    mc_mt = su[1]/su[2]
    mu_mc = su[0]/su[1]
    if mc_mt <= 0 or mu_mc <= 0:
        return 1e20
    return ((np.log(mc_mt) - np.log(PDG_MC_MT))/0.05)**2 + \
           ((np.log(mu_mc) - np.log(PDG_MU_MC))/0.05)**2

print(f"\nFitting up-sector mass ratios at τ=i (independent optimizer)...")
res_up = differential_evolution(
    chi2_up, [(-4, 8), (-4, 8)], args=(TAU_CM,),
    maxiter=3000, tol=1e-12, seed=123, popsize=20, mutation=(0.5,1.5),
    recombination=0.9, workers=1, disp=False
)
res_up2 = minimize(chi2_up, res_up.x, args=(TAU_CM,), method='Nelder-Mead',
                   options={'xatol':1e-13,'fatol':1e-13,'maxiter':100000})
log_bu_cm, log_gu_cm = res_up2.x
bu_cm = exp(log_bu_cm)
gu_cm = exp(log_gu_cm)

Mu_cm = build_Mu(TAU_CM, 1.0, bu_cm, gu_cm)
_, su_cm, _ = svd(Mu_cm)
su_cm = np.sort(su_cm)

print(f"  β_u/α_u at τ=i = {bu_cm:.6f}  (I2 used: ~100)")
print(f"  γ_u/α_u at τ=i = {gu_cm:.6f}  (I2 used: ~590)")
print(f"  m_c/m_t = {su_cm[1]/su_cm[2]:.5e}  [target: {PDG_MC_MT:.5e}]")
print(f"  m_u/m_c = {su_cm[0]/su_cm[1]:.5e}  [target: {PDG_MU_MC:.5e}]")
print(f"  chi2 = {res_up2.fun:.4e}")

# Step B2: Examine U_uL structure at τ=i
Uu_cm, su_raw, _ = svd(Mu_cm)
iu = np.argsort(su_raw)
Uu_cm_sorted = Uu_cm[:, iu]
print(f"\nU_uL at τ=i (left singular vectors, sorted by ascending mass):")
print(np.round(np.abs(Uu_cm_sorted), 6))
print("Phases (degrees):")
print(np.round(np.angle(Uu_cm_sorted)*180/pi, 2))

# Step B3: Joint fit at τ=i (all 6 real coupling params free)

def chi2_joint(x, tau):
    """
    Full joint fit at fixed τ.
    x = [log_bu, log_gu, log_bd, log_gd1, gd2_re, gd2_im]
    """
    bu = exp(x[0])
    gu = exp(x[1])
    bd = exp(x[2])
    gd1 = exp(x[3])
    gd2 = x[4] + 1j*x[5]
    try:
        Mu = build_Mu(tau, 1.0, bu, gu)
        Md = build_Md(tau, 1.0, bd, gd1, gd2)
        V, su, sd = compute_ckm(Mu, Md)
    except Exception:
        return 1e20
    if np.any(~np.isfinite(su)) or np.any(~np.isfinite(sd)):
        return 1e20
    if su[2] == 0 or su[1] == 0 or sd[2] == 0 or sd[1] == 0:
        return 1e20

    mc_mt = su[1]/su[2]
    mu_mc = su[0]/su[1]
    md_ms = sd[0]/sd[1]
    ms_mb = sd[1]/sd[2]
    s12, s13, s23, _ = extract_angles(V)

    if mc_mt <= 0 or mu_mc <= 0 or md_ms <= 0 or ms_mb <= 0:
        return 1e20

    chi2 = (
        ((np.log(mc_mt) - np.log(PDG_MC_MT))/0.05)**2 +
        ((np.log(mu_mc) - np.log(PDG_MU_MC))/0.05)**2 +
        ((np.log(md_ms) - np.log(PDG_MD_MS))/0.10)**2 +
        ((np.log(ms_mb) - np.log(PDG_MS_MB))/0.10)**2 +
        ((s12 - PDG_SIN_T12)/0.001)**2 +
        ((s13 - PDG_SIN_T13)/0.0005)**2 +
        ((s23 - PDG_SIN_T23)/0.002)**2
    )
    return chi2

bounds_joint = [
    (-4, 9),   # log(β_u)
    (-4, 9),   # log(γ_u)
    (-4, 9),   # log(β_d)
    (-4, 9),   # log(γ_d1)
    (-8, 8),   # Re(γ_d2)
    (-8, 8),   # Im(γ_d2)
]

print(f"\nFull joint fit at τ=i (all 6 params free, independent optimization)...")
print("Running DE (4000 iters, popsize 30)...")
res_joint_de = differential_evolution(
    chi2_joint, bounds_joint, args=(TAU_CM,),
    maxiter=4000, tol=1e-10, seed=456, popsize=30,
    mutation=(0.5,1.5), recombination=0.9, workers=1, disp=False
)
print(f"  DE chi2 = {res_joint_de.fun:.4e}")

res_joint = minimize(
    chi2_joint, res_joint_de.x, args=(TAU_CM,), method='Nelder-Mead',
    options={'xatol':1e-13,'fatol':1e-13,'maxiter':500000}
)
print(f"  NM chi2 = {res_joint.fun:.4e}")

xj = res_joint.x
Mu_j = build_Mu(TAU_CM, 1.0, exp(xj[0]), exp(xj[1]))
Md_j = build_Md(TAU_CM, 1.0, exp(xj[2]), exp(xj[3]), xj[4]+1j*xj[5])
V_j, su_j, sd_j = compute_ckm(Mu_j, Md_j)
s12_j, s13_j, s23_j, aV_j = extract_angles(V_j)

print(f"\nJoint fit result at τ=i:")
print(f"  β_u/α_u  = {exp(xj[0]):.6f}")
print(f"  γ_u/α_u  = {exp(xj[1]):.6f}")
print(f"  β_d/α_d  = {exp(xj[2]):.6f}")
print(f"  γ_d1/α_d = {exp(xj[3]):.6f}")
print(f"  γ_d2/α_d = {xj[4]:.6f} + {xj[5]:.6f}i")
print(f"\n  Mass ratios:")
print(f"    m_c/m_t = {su_j[1]/su_j[2]:.5e}  [target: {PDG_MC_MT:.5e}]")
print(f"    m_u/m_c = {su_j[0]/su_j[1]:.5e}  [target: {PDG_MU_MC:.5e}]")
print(f"    m_d/m_s = {sd_j[0]/sd_j[1]:.5e}  [target: {PDG_MD_MS:.5e}]")
print(f"    m_s/m_b = {sd_j[1]/sd_j[2]:.5e}  [target: {PDG_MS_MB:.5e}]")
print(f"\n  |V_CKM|:")
print(f"    |V_ud|={aV_j[0,0]:.5f}  |V_us|={aV_j[0,1]:.5f}  |V_ub|={aV_j[0,2]:.6f}")
print(f"    |V_cd|={aV_j[1,0]:.5f}  |V_cs|={aV_j[1,1]:.5f}  |V_cb|={aV_j[1,2]:.6f}")
print(f"    |V_td|={aV_j[2,0]:.5f}  |V_ts|={aV_j[2,1]:.5f}  |V_tb|={aV_j[2,2]:.6f}")
print(f"\n  CKM angles:")
print(f"    sin θ_12 = {s12_j:.5f}  [PDG: {PDG_SIN_T12:.5f}]  dev = {100*(s12_j-PDG_SIN_T12)/PDG_SIN_T12:+.1f}%")
print(f"    sin θ_13 = {s13_j:.6f}  [PDG: {PDG_SIN_T13:.6f}]  dev = {100*(s13_j-PDG_SIN_T13)/PDG_SIN_T13:+.1f}%")
print(f"    sin θ_23 = {s23_j:.5f}  [PDG: {PDG_SIN_T23:.5f}]  dev = {100*(s23_j-PDG_SIN_T23)/PDG_SIN_T23:+.1f}%")

# ─────────────────────────────────────────────────────────────────
# CROSS CHECK: What does I2's claim predict?
# I2 claimed sin θ_C ≈ 0.00068 (with its parameters)
# We verify with I2's β/α=83, γ/α=901 (from its corrected script)
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("Cross-check: I2's claimed parameters at τ=i")
print("─" * 60)

# I2 corrected script used β=83.060068, γ=901.148082
Mu_i2 = build_Mu(TAU_CM, 1.0, 83.060068, 901.148082)
_, su_i2, _ = svd(Mu_i2)
su_i2 = np.sort(su_i2)
print(f"With I2's params (β/α=83.06, γ/α=901.15):")
print(f"  m_c/m_t = {su_i2[1]/su_i2[2]:.5e}  [target: {PDG_MC_MT:.5e}]")
print(f"  m_u/m_c = {su_i2[0]/su_i2[1]:.5e}  [target: {PDG_MU_MC:.5e}]")

# Check U_uL structure with I2's params
Uu_i2, su_i2_raw, _ = svd(Mu_i2)
iu_i2 = np.argsort(su_i2_raw)
Uu_i2_sorted = Uu_i2[:, iu_i2]
print(f"\n|U_uL| at τ=i (I2 params):")
print(np.round(np.abs(Uu_i2_sorted), 6))

# ─────────────────────────────────────────────────────────────────
# V2.C — BASIS/CONVENTION TESTS
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("V2.C — Basis/convention tests")
print("─" * 60)

# Test 1: Reverse field ordering (Q3, Q2, Q1 instead of Q1, Q2, Q3)
def build_Mu_reversed(tau, alpha_u, beta_u, gamma_u):
    """Same as build_Mu but with reversed Q ordering (Q3, Q2, Q1)."""
    M = build_Mu(tau, alpha_u, beta_u, gamma_u)
    return M[:, ::-1]  # reverse column order

def build_Md_reversed(tau, alpha_d, beta_d, gamma_d1, gamma_d2):
    M = build_Md(tau, alpha_d, beta_d, gamma_d1, gamma_d2)
    return M[:, ::-1]

def chi2_joint_rev(x, tau):
    """Joint chi2 with reversed Q ordering."""
    bu = exp(x[0]); gu = exp(x[1])
    bd = exp(x[2]); gd1 = exp(x[3])
    gd2 = x[4] + 1j*x[5]
    try:
        Mu = build_Mu_reversed(tau, 1.0, bu, gu)
        Md = build_Md_reversed(tau, 1.0, bd, gd1, gd2)
        V, su, sd = compute_ckm(Mu, Md)
    except Exception:
        return 1e20
    if np.any(~np.isfinite(su)) or np.any(~np.isfinite(sd)):
        return 1e20
    if su[2]==0 or su[1]==0 or sd[2]==0 or sd[1]==0:
        return 1e20
    mc_mt = su[1]/su[2]; mu_mc = su[0]/su[1]
    md_ms = sd[0]/sd[1]; ms_mb = sd[1]/sd[2]
    s12, s13, s23, _ = extract_angles(V)
    if mc_mt<=0 or mu_mc<=0 or md_ms<=0 or ms_mb<=0: return 1e20
    chi2 = (
        ((np.log(mc_mt)-np.log(PDG_MC_MT))/0.05)**2 +
        ((np.log(mu_mc)-np.log(PDG_MU_MC))/0.05)**2 +
        ((np.log(md_ms)-np.log(PDG_MD_MS))/0.10)**2 +
        ((np.log(ms_mb)-np.log(PDG_MS_MB))/0.10)**2 +
        ((s12-PDG_SIN_T12)/0.001)**2 +
        ((s13-PDG_SIN_T13)/0.0005)**2 +
        ((s23-PDG_SIN_T23)/0.002)**2
    )
    return chi2

print("Testing reversed Q ordering (Q3,Q2,Q1)...")
res_rev_de = differential_evolution(
    chi2_joint_rev, bounds_joint, args=(TAU_CM,),
    maxiter=3000, tol=1e-10, seed=789, popsize=25,
    mutation=(0.5,1.5), recombination=0.9, workers=1, disp=False
)
res_rev = minimize(chi2_joint_rev, res_rev_de.x, args=(TAU_CM,), method='Nelder-Mead',
                   options={'xatol':1e-12,'fatol':1e-12,'maxiter':300000})
xr = res_rev.x
Mu_r = build_Mu_reversed(TAU_CM, 1.0, exp(xr[0]), exp(xr[1]))
Md_r = build_Md_reversed(TAU_CM, 1.0, exp(xr[2]), exp(xr[3]), xr[4]+1j*xr[5])
V_r, su_r, sd_r = compute_ckm(Mu_r, Md_r)
s12_r, s13_r, s23_r, aV_r = extract_angles(V_r)
print(f"  chi2 = {res_rev.fun:.4e}")
print(f"  sin θ_12 = {s12_r:.5f}  [PDG: {PDG_SIN_T12:.5f}]  dev = {100*(s12_r-PDG_SIN_T12)/PDG_SIN_T12:+.1f}%")

# Test 2: Complex conjugate the modular forms (different gCP convention)
def weight1_forms_cc(tau, n_terms=80):
    """Complex conjugate of weight1_forms (alternative gCP convention)."""
    Y1, Y2, Y3 = weight1_forms(tau, n_terms)
    return Y1.conjugate(), Y2.conjugate(), Y3.conjugate()

def build_Mu_cc(tau, alpha_u, beta_u, gamma_u):
    """M_u with complex conjugated modular forms."""
    Y1, Y2, Y3 = weight1_forms_cc(tau)
    f = all_forms(Y1, Y2, Y3)
    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = alpha_u * f['Y1_1']
    M[0, 1] = alpha_u * f['Y1_3']
    M[0, 2] = alpha_u * f['Y1_2']
    M[1, 0] = beta_u * f['Y2_3']
    M[1, 1] = beta_u * f['Y2_5']
    M[1, 2] = beta_u * f['Y2_4']
    M[2, 0] = gamma_u * f['Y5_3']
    M[2, 1] = gamma_u * f['Y5_5']
    M[2, 2] = gamma_u * f['Y5_4']
    return M

def build_Md_cc(tau, alpha_d, beta_d, gamma_d1, gamma_d2):
    Y1, Y2, Y3 = weight1_forms_cc(tau)
    f = all_forms(Y1, Y2, Y3)
    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = alpha_d * f['Y1_1']
    M[0, 1] = alpha_d * f['Y1_3']
    M[0, 2] = alpha_d * f['Y1_2']
    M[1, 0] = beta_d * f['Y5_3']
    M[1, 1] = beta_d * f['Y5_5']
    M[1, 2] = beta_d * f['Y5_4']
    M[2, 0] = gamma_d1 * f['Y5_6'] + gamma_d2 * f['Y5_9']
    M[2, 1] = gamma_d1 * f['Y5_8'] + gamma_d2 * f['Y5_11']
    M[2, 2] = gamma_d1 * f['Y5_7'] + gamma_d2 * f['Y5_10']
    return M

def chi2_joint_cc(x, tau):
    bu=exp(x[0]); gu=exp(x[1])
    bd=exp(x[2]); gd1=exp(x[3])
    gd2=x[4]+1j*x[5]
    try:
        Mu = build_Mu_cc(tau, 1.0, bu, gu)
        Md = build_Md_cc(tau, 1.0, bd, gd1, gd2)
        V, su, sd = compute_ckm(Mu, Md)
    except Exception:
        return 1e20
    if np.any(~np.isfinite(su)) or np.any(~np.isfinite(sd)): return 1e20
    if su[2]==0 or su[1]==0 or sd[2]==0 or sd[1]==0: return 1e20
    mc_mt=su[1]/su[2]; mu_mc=su[0]/su[1]
    md_ms=sd[0]/sd[1]; ms_mb=sd[1]/sd[2]
    s12,s13,s23,_ = extract_angles(V)
    if mc_mt<=0 or mu_mc<=0 or md_ms<=0 or ms_mb<=0: return 1e20
    return (
        ((np.log(mc_mt)-np.log(PDG_MC_MT))/0.05)**2 +
        ((np.log(mu_mc)-np.log(PDG_MU_MC))/0.05)**2 +
        ((np.log(md_ms)-np.log(PDG_MD_MS))/0.10)**2 +
        ((np.log(ms_mb)-np.log(PDG_MS_MB))/0.10)**2 +
        ((s12-PDG_SIN_T12)/0.001)**2 +
        ((s13-PDG_SIN_T13)/0.0005)**2 +
        ((s23-PDG_SIN_T23)/0.002)**2
    )

print("\nTesting complex-conjugated modular forms (alternative gCP)...")
res_cc_de = differential_evolution(
    chi2_joint_cc, bounds_joint, args=(TAU_CM,),
    maxiter=3000, tol=1e-10, seed=321, popsize=25,
    mutation=(0.5,1.5), recombination=0.9, workers=1, disp=False
)
res_cc = minimize(chi2_joint_cc, res_cc_de.x, args=(TAU_CM,), method='Nelder-Mead',
                  options={'xatol':1e-12,'fatol':1e-12,'maxiter':300000})
xcc = res_cc.x
Mu_cc = build_Mu_cc(TAU_CM, 1.0, exp(xcc[0]), exp(xcc[1]))
Md_cc = build_Md_cc(TAU_CM, 1.0, exp(xcc[2]), exp(xcc[3]), xcc[4]+1j*xcc[5])
V_cc, su_cc, sd_cc = compute_ckm(Mu_cc, Md_cc)
s12_cc, s13_cc, s23_cc, aV_cc = extract_angles(V_cc)
print(f"  chi2 = {res_cc.fun:.4e}")
print(f"  sin θ_12 = {s12_cc:.5f}  [PDG: {PDG_SIN_T12:.5f}]  dev = {100*(s12_cc-PDG_SIN_T12)/PDG_SIN_T12:+.1f}%")

# Test 3: Transpose convention (W = Q M q^c instead of W = q^c M Q)
# V_CKM_transposed convention uses RIGHT singular vectors
def compute_ckm_transposed(Mu, Md):
    """
    Transpose convention: V_CKM = U_uR† U_dR
    where U_R = right singular vectors of M.
    SVD: M = U diag(s) V†  →  V = U_R
    """
    _, su, Vhu = svd(Mu)
    _, sd, Vhd = svd(Md)
    UuR = Vhu.conj().T
    UdR = Vhd.conj().T
    iu = np.argsort(su)
    id_ = np.argsort(sd)
    UuR = UuR[:, iu]
    UdR = UdR[:, id_]
    V = UuR.conj().T @ UdR
    return V, np.sort(su), np.sort(sd)

def chi2_joint_transposed(x, tau):
    bu=exp(x[0]); gu=exp(x[1])
    bd=exp(x[2]); gd1=exp(x[3])
    gd2=x[4]+1j*x[5]
    try:
        Mu = build_Mu(tau, 1.0, bu, gu)
        Md = build_Md(tau, 1.0, bd, gd1, gd2)
        V, su, sd = compute_ckm_transposed(Mu, Md)
    except Exception:
        return 1e20
    if np.any(~np.isfinite(su)) or np.any(~np.isfinite(sd)): return 1e20
    if su[2]==0 or su[1]==0 or sd[2]==0 or sd[1]==0: return 1e20
    mc_mt=su[1]/su[2]; mu_mc=su[0]/su[1]
    md_ms=sd[0]/sd[1]; ms_mb=sd[1]/sd[2]
    s12,s13,s23,_ = extract_angles(V)
    if mc_mt<=0 or mu_mc<=0 or md_ms<=0 or ms_mb<=0: return 1e20
    return (
        ((np.log(mc_mt)-np.log(PDG_MC_MT))/0.05)**2 +
        ((np.log(mu_mc)-np.log(PDG_MU_MC))/0.05)**2 +
        ((np.log(md_ms)-np.log(PDG_MD_MS))/0.10)**2 +
        ((np.log(ms_mb)-np.log(PDG_MS_MB))/0.10)**2 +
        ((s12-PDG_SIN_T12)/0.001)**2 +
        ((s13-PDG_SIN_T13)/0.0005)**2 +
        ((s23-PDG_SIN_T23)/0.002)**2
    )

print("\nTesting transposed convention (right singular vectors)...")
res_tr_de = differential_evolution(
    chi2_joint_transposed, bounds_joint, args=(TAU_CM,),
    maxiter=3000, tol=1e-10, seed=654, popsize=25,
    mutation=(0.5,1.5), recombination=0.9, workers=1, disp=False
)
res_tr = minimize(chi2_joint_transposed, res_tr_de.x, args=(TAU_CM,), method='Nelder-Mead',
                  options={'xatol':1e-12,'fatol':1e-12,'maxiter':300000})
xtr = res_tr.x
Mu_tr = build_Mu(TAU_CM, 1.0, exp(xtr[0]), exp(xtr[1]))
Md_tr = build_Md(TAU_CM, 1.0, exp(xtr[2]), exp(xtr[3]), xtr[4]+1j*xtr[5])
V_tr, su_tr, sd_tr = compute_ckm_transposed(Mu_tr, Md_tr)
s12_tr, s13_tr, s23_tr, aV_tr = extract_angles(V_tr)
print(f"  chi2 = {res_tr.fun:.4e}")
print(f"  sin θ_12 = {s12_tr:.5f}  [PDG: {PDG_SIN_T12:.5f}]  dev = {100*(s12_tr-PDG_SIN_T12)/PDG_SIN_T12:+.1f}%")

# ─────────────────────────────────────────────────────────────────
# ANALYTIC UNDERSTANDING — why collinearity implies sin θ_C suppression
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("ANALYTIC ARGUMENT: Why collinearity → sin θ_C suppression")
print("─" * 60)

# At τ=i, all weight-k forms have the same phase φ = k * 45° = k * π/4
# So Y^(k)_i = |Y^(k)_i| * e^{ik*π/4} * (sign)

# Each row of M_u is proportional to e^{ik*π/4} * (real vector)
# Row 0 (weight 1): M_u[0,:] ∝ e^{i*π/4} * (a1, a3, a2) for real a1, a2, a3
# Row 1 (weight 2): M_u[1,:] ∝ e^{i*2*π/4} = i * (b3, b5, b4) for real b's
# Row 2 (weight 5): M_u[2,:] ∝ e^{i*5*π/4} * (c3, c5, c4) for real c's

# Factor out row phases:
# M_u = diag(e^{iπ/4}, i, e^{i5π/4}) @ M_real
# where M_real has REAL entries (up to overall sign ambiguities in Y5)

# Key: M_u = D_u @ M_real_u where D_u is diagonal complex phase
# SVD of M_u = (D_u @ U_u^real) @ diag(su) @ Vh_u^real
# So U_uL = D_u @ U_u^real where U_u^real is real orthogonal
# Similarly U_dL = D_d @ U_d^real

# V_CKM = U_uL† U_dL = (U_u^real)† @ D_u† D_d @ (U_d^real)
# This is a product of real orthogonal matrices sandwiching a diagonal unitary

# For V_CKM to have large sin θ_12, need (U_u^real)† @ Δ_phase @ U_d^real
# to have large off-diagonal (0,1) element.
# Δ_phase = D_u† D_d has diagonal entries e^{i(φ_d_k - φ_u_k)}

# CRITICAL: If both M_u and M_d have the SAME row weights (same multiplets per row),
# then D_u = D_d → Δ_phase = I → V = (U_u^real)† U_d^real (REAL orthogonal matrix)
# A real 3x3 orthogonal matrix can have any CKM angle including sin θ_C = 0.2253!

# BUT: M_u and M_d do NOT have the same row weights:
#   M_u rows: w=1 (u^c), w=2 (c^c), w=5 (t^c)
#   M_d rows: w=1 (d^c), w=5 (s^c), w=5 (b^c, two triplets)

# Phase analysis at τ=i:
# Row 0 both M_u and M_d: Y^(1) → phase = 45°  (same for both)
# Row 1 M_u (c^c): Y^(2) → phase = 90°
# Row 1 M_d (s^c): Y^(5) 3̂ → phase = 225° = -135°
# Row 2 M_u (t^c): Y^(5) 3̂ → phase = 225°
# Row 2 M_d (b^c): Y^(5) 3̂' I and II → check phases

Y1i, Y2i, Y3i = weight1_forms(TAU_CM)
fi = all_forms(Y1i, Y2i, Y3i)
print(f"\nPhases at τ=i for rows used in M_u and M_d:")
print(f"  Row 0, both (weight-1): Y1 arg = {np.angle(Y1i)*180/pi:.1f}°")
print(f"  Row 1, M_u (weight-2): Y2_3 arg = {np.angle(fi['Y2_3'])*180/pi:.1f}°")
print(f"  Row 1, M_d (weight-5 3̂): Y5_3 arg = {np.angle(fi['Y5_3'])*180/pi:.1f}°  (≈ {np.angle(fi['Y5_3'])*180/pi:.1f}°)")
print(f"  Row 2, M_u (weight-5 3̂): Y5_3 arg = {np.angle(fi['Y5_3'])*180/pi:.1f}°")
print(f"  Row 2, M_d (weight-5 3̂'I): Y5_6 arg = {np.angle(fi['Y5_6'])*180/pi:.1f}°")
print(f"  Row 2, M_d (weight-5 3̂'II): Y5_9 arg = {np.angle(fi['Y5_9'])*180/pi:.1f}°")

print(f"\nPhase differences D_u†D_d on diagonal:")
phi_u = [np.angle(Y1i), np.angle(fi['Y2_3']), np.angle(fi['Y5_3'])]
phi_d = [np.angle(Y1i), np.angle(fi['Y5_3']), np.angle(fi['Y5_6'])]  # use Y5_6 for b^c
delta_phase = [(phi_d[k] - phi_u[k])*180/pi for k in range(3)]
print(f"  Δφ_0 (d vs u, row 0): {delta_phase[0]:.1f}° (SAME multiplet → 0°)")
print(f"  Δφ_1 (s vs c, row 1): {delta_phase[1]:.1f}°")
print(f"  Δφ_2 (b vs t, row 2): {delta_phase[2]:.1f}°")

print("\nKey insight:")
print("  d^c row uses Y^(1) (weight 1) — SAME as u^c row → φ_d0 = φ_u0")
print("  s^c row uses Y^(5) (weight 5) — DIFFERENT from c^c (weight 2)")
print("  This means M_u and M_d factor out DIFFERENT phase matrices D_u, D_d")
print("  V_CKM = (U^real_u)† (D_u†D_d) U^real_d is NOT simply a real O(3) matrix")

# ─────────────────────────────────────────────────────────────────
# MATHEMATICAL PROOF: At τ=i, rows 0 and 1 of M_d are proportional
# M_d[0,:] ∝ (Y1, Y3, Y2) weight-1 → direction v1 in C^3
# M_d[1,:] ∝ (Y5_3, Y5_5, Y5_4) weight-5 3̂ → direction v5 in C^3
# Are v1 and v5 proportional? (i.e., is M_d rank-1 in rows 0 and 1?)
# ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("Rank analysis: rows of M_d at τ=i")
print("─" * 60)

# Normalized direction vectors
v1_d = np.array([fi['Y1_1'], fi['Y1_3'], fi['Y1_2']])  # d^c row (weight-1)
v5_3hat = np.array([fi['Y5_3'], fi['Y5_5'], fi['Y5_4']])  # s^c row (weight-5 3̂)

v1_n = v1_d / np.linalg.norm(v1_d)
v5_n = v5_3hat / np.linalg.norm(v5_3hat)

print(f"\nNormalized row directions in C^3 (as ratios to first component):")
print(f"  d^c row (wt-1): [1, {v1_d[1]/v1_d[0]:.6f}, {v1_d[2]/v1_d[0]:.6f}]")
print(f"  s^c row (wt-5 3̂): [1, {v5_3hat[1]/v5_3hat[0]:.6f}, {v5_3hat[2]/v5_3hat[0]:.6f}]")

# Overlap |<v1 | v5>|² (if 1 → parallel; if 0 → orthogonal)
overlap = abs(np.vdot(v1_n, v5_n))**2
print(f"\n  |<v_d^c | v_s^c>|² = {overlap:.8f}")
print(f"  (= 1.0 → parallel directions, < 1 → some angle)")

# Cross product to check if they span different subspaces
cross = np.cross(v1_n, v5_n)
print(f"  |v_d^c × v_s^c| = {np.linalg.norm(cross):.8f}")
print(f"  (= 0 → collinear in C^3, > 0 → different directions)")

# Also check u^c vs c^c directions in M_u
v1_u = np.array([fi['Y1_1'], fi['Y1_3'], fi['Y1_2']])  # u^c row
v2_u = np.array([fi['Y2_3'], fi['Y2_5'], fi['Y2_4']])  # c^c row
v1_u_n = v1_u / np.linalg.norm(v1_u)
v2_u_n = v2_u / np.linalg.norm(v2_u)
overlap_u = abs(np.vdot(v1_u_n, v2_u_n))**2
print(f"\n  M_u: |<v_u^c | v_c^c>|² = {overlap_u:.8f}")
print(f"  M_u rows 0,1 share direction: {'YES (rank deficient!)' if overlap_u > 0.999 else 'NO'}")

cross_u = np.cross(v1_u_n, v2_u_n)
print(f"  |v_u^c × v_c^c| = {np.linalg.norm(cross_u):.8f}")

# Check weight-1 vs weight-5 3̂ ratios
print(f"\n  Ratio Y5_5/Y5_3 = {fi['Y5_5']/fi['Y5_3']:.8f} (imaginary part = {abs((fi['Y5_5']/fi['Y5_3']).imag):.2e})")
print(f"  Ratio Y2_5/Y2_3 = {fi['Y2_5']/fi['Y2_3']:.8f} (imaginary part = {abs((fi['Y2_5']/fi['Y2_3']).imag):.2e})")
print(f"  Ratio Y1_3/Y1_1 = {fi['Y1_3']/fi['Y1_1']:.8f} (imaginary part = {abs((fi['Y1_3']/fi['Y1_1']).imag):.2e})")

# Key: the REAL parts of these ratios (Y5_5/Y5_3 vs Y1_3/Y1_1) differ
# This means the direction vectors for d^c and s^c rows differ
# → M_d is NOT rank-1 in rows 0,1 (they point in DIFFERENT directions in C^3)
# → U_dL is NOT near-identity, and CKM angle is potentially free

print("\n" + "─" * 60)
print("SUMMARY OF FINDINGS")
print("─" * 60)
print(f"\nAt τ=i:")
print(f"  sin θ_C (V2 joint fit, all 6 params free)  = {s12_j:.5f}")
print(f"  sin θ_C (reversed Q ordering)              = {s12_r:.5f}")
print(f"  sin θ_C (complex conj. modular forms)      = {s12_cc:.5f}")
print(f"  sin θ_C (transposed convention)            = {s12_tr:.5f}")
print(f"  PDG target                                 = {PDG_SIN_T12:.5f}")

best_chi2 = min(res_joint.fun, res_rev.fun, res_cc.fun, res_tr.fun)
best_s12 = [s12_j, s12_r, s12_cc, s12_tr][[res_joint.fun, res_rev.fun, res_cc.fun, res_tr.fun].index(min([res_joint.fun, res_rev.fun, res_cc.fun, res_tr.fun]))]
print(f"\n  Best chi2 across all conventions: {best_chi2:.4e}")
print(f"  sin θ_C at best chi2: {best_s12:.5f}")

dev_best = 100*(best_s12 - PDG_SIN_T12)/PDG_SIN_T12
if abs(dev_best) <= 5:
    verdict = "I2 OBSTRUCTION REFUTED — sin θ_C achievable at τ=i"
elif abs(dev_best) <= 50:
    verdict = "I2 PARTIALLY CORRECT — collinearity is real but θ_C partially recoverable"
else:
    verdict = "I2 OBSTRUCTION CONFIRMED — sin θ_C structurally pinned at τ=i"

print(f"\n  VERDICT: [{verdict}]")
print(f"  PDG deviation at best fit: {dev_best:+.1f}%")
