"""
V1.B — Independent audit of LYD20 Model VI mass matrix
Source: modular_symmetry_S4prime.tex lines 1366-1407
"""
import numpy as np
from numpy import pi, sqrt, exp

# ─────────────────────────────────────────────────────
# Eta function (Dedekind)
# ─────────────────────────────────────────────────────
def eta(tau, n_terms=80):
    """Dedekind eta via q-product. q = exp(2*pi*i*tau)."""
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

# ─────────────────────────────────────────────────────
# Weight-1 modular forms (LYD20 lines 296-330)
# Y^(1)_{3hat'} = (Y1, Y2, Y3)
# ─────────────────────────────────────────────────────
def weight1_forms(tau, n_terms=80):
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

# ─────────────────────────────────────────────────────
# Higher-weight forms (LYD20 Appendix lines 347-395, 1865-1876)
# ─────────────────────────────────────────────────────
def all_forms(Y1, Y2, Y3):
    f = {}
    # Weight 1
    f['Y1_1'] = Y1; f['Y1_2'] = Y2; f['Y1_3'] = Y3
    # Weight 2 (3): Y^(2)_3, Y^(2)_4, Y^(2)_5
    f['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    f['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    f['Y2_5'] = 2*Y2**2 - 2*Y1*Y3
    # Weight 5 (3hat): Y^(5)_3, Y^(5)_4, Y^(5)_5
    f['Y5_3'] = 18*Y1**2*(-Y2**3 + Y3**3)
    f['Y5_4'] = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
                 + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
                 + 6*Y1**2*Y2**2*Y3)
    f['Y5_5'] = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
                 - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
                 - 6*Y1**2*Y2*Y3**2)
    return f

def M_u_matrix(tau, alpha_u, beta_u, gamma_u, n_terms=80):
    """LYD20 Eq. Mq_6 (lines 1379-1384)"""
    Y1, Y2, Y3 = weight1_forms(tau, n_terms)
    f = all_forms(Y1, Y2, Y3)
    M = np.zeros((3,3), dtype=complex)
    # Row 0: u^c — weight-1 forms [Y1_1, Y1_3, Y1_2]
    M[0, :] = alpha_u * np.array([f['Y1_1'], f['Y1_3'], f['Y1_2']])
    # Row 1: c^c — weight-2 forms [Y2_3, Y2_5, Y2_4]
    M[1, :] = beta_u  * np.array([f['Y2_3'], f['Y2_5'], f['Y2_4']])
    # Row 2: t^c — weight-5 forms [Y5_3, Y5_5, Y5_4]
    M[2, :] = gamma_u * np.array([f['Y5_3'], f['Y5_5'], f['Y5_4']])
    return M

def mass_ratios(M):
    """Compute singular values -> quark masses and ratios."""
    sv = np.linalg.svd(M, compute_uv=False)
    sv_sorted = np.sort(sv)  # ascending: [m_u, m_c, m_t]
    m_u, m_c, m_t = sv_sorted
    ratio_ct = m_c / m_t
    ratio_uc = m_u / m_c
    return m_u, m_c, m_t, ratio_ct, ratio_uc

# ─────────────────────────────────────────────────────
# SCENARIO 1: LYD20 best-fit parameters at best-fit tau
# tau = -0.4999 + 0.8958i  (LYD20 line 1395)
# beta_u/alpha_u = 62.2142, gamma_u/alpha_u = 0.00104
# ─────────────────────────────────────────────────────
print("=" * 60)
print("SCENARIO 1: LYD20 best-fit params at best-fit tau")
print("tau = -0.4999 + 0.8958i  [TeX line 1395]")
print("beta/alpha = 62.2142, gamma/alpha = 0.00104  [TeX line 1395]")
print("=" * 60)

tau_bf = -0.4999 + 0.8958j
alpha_u = 1.0
beta_u  = 62.2142
gamma_u = 0.00104

Y1, Y2, Y3 = weight1_forms(tau_bf)
print(f"\nModular form magnitudes at tau_bf:")
print(f"  |Y1| = {abs(Y1):.6f}")
print(f"  |Y2| = {abs(Y2):.6f}")
print(f"  |Y3| = {abs(Y3):.6f}")

f = all_forms(Y1, Y2, Y3)
row0 = np.array([f['Y1_1'], f['Y1_3'], f['Y1_2']])
row1 = np.array([f['Y2_3'], f['Y2_5'], f['Y2_4']])
row2 = np.array([f['Y5_3'], f['Y5_5'], f['Y5_4']])
print(f"\nRow norms at tau_bf:")
print(f"  ||u^c row|| = 1 * {np.linalg.norm(row0):.4f}")
print(f"  ||c^c row|| = 62.2142 * {np.linalg.norm(row1):.4f} = {beta_u * np.linalg.norm(row1):.4f}")
print(f"  ||t^c row|| = 0.00104 * {np.linalg.norm(row2):.4f} = {gamma_u * np.linalg.norm(row2):.6f}")
print(f"  |Y5_3| = {abs(f['Y5_3']):.4f}")
print(f"  |Y5_4| = {abs(f['Y5_4']):.4f}")
print(f"  |Y5_5| = {abs(f['Y5_5']):.4f}")

M_bf = M_u_matrix(tau_bf, alpha_u, beta_u, gamma_u)
m_u, m_c, m_t, ratio_ct, ratio_uc = mass_ratios(M_bf)
print(f"\nSingular values (ascending): {m_u:.6e}, {m_c:.6e}, {m_t:.6e}")
print(f"  m_c/m_t = {ratio_ct:.6f}  (LYD20 claims 0.00268)")
print(f"  m_u/m_c = {ratio_uc:.6f}  (LYD20 claims 0.00204)")
print(f"  Reproduced LYD20 best-fit? m_c/m_t: {'YES' if abs(ratio_ct - 0.00268)/0.00268 < 0.02 else 'NO'}")

# ─────────────────────────────────────────────────────
# SCENARIO 2: LYD20 best-fit parameters at tau = i
# ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SCENARIO 2: LYD20 best-fit params at tau = i (CM point)")
print("beta/alpha = 62.2142, gamma/alpha = 0.00104")
print("=" * 60)

tau_i = 1j

Y1i, Y2i, Y3i = weight1_forms(tau_i)
print(f"\nModular form magnitudes at tau=i:")
print(f"  |Y1| = {abs(Y1i):.6f}")
print(f"  |Y2| = {abs(Y2i):.6f}")
print(f"  |Y3| = {abs(Y3i):.6f}")

fi = all_forms(Y1i, Y2i, Y3i)
row0i = np.array([fi['Y1_1'], fi['Y1_3'], fi['Y1_2']])
row1i = np.array([fi['Y2_3'], fi['Y2_5'], fi['Y2_4']])
row2i = np.array([fi['Y5_3'], fi['Y5_5'], fi['Y5_4']])
print(f"\nRow norms at tau=i (alpha=1, beta=62.2142, gamma=0.00104):")
print(f"  u^c row norm = {np.linalg.norm(row0i):.6f}")
print(f"  c^c row norm (x beta) = {beta_u * np.linalg.norm(row1i):.6f}")
print(f"  t^c row norm (x gamma) = {gamma_u * np.linalg.norm(row2i):.6f}")
print(f"  |Y5_3| = {abs(fi['Y5_3']):.4f}")
print(f"  |Y5_4| = {abs(fi['Y5_4']):.4f}")
print(f"  |Y5_5| = {abs(fi['Y5_5']):.4f}")

M_i = M_u_matrix(tau_i, alpha_u, beta_u, gamma_u)
m_u_i, m_c_i, m_t_i, ratio_ct_i, ratio_uc_i = mass_ratios(M_i)
print(f"\nSingular values (ascending): {m_u_i:.6e}, {m_c_i:.6e}, {m_t_i:.6e}")
print(f"  m_c/m_t = {ratio_ct_i:.6e}  ({ratio_ct_i*1e3:.4f} x 10^-3)")
print(f"  m_u/m_c = {ratio_uc_i:.6e}")
print(f"  H3's claim: m_c/m_t = 2.7247e-3 at tau=i")
print(f"  Match? {'YES' if abs(ratio_ct_i - 2.7247e-3)/2.7247e-3 < 0.02 else 'NO (differs by ' + f'{abs(ratio_ct_i - 2.7247e-3)/2.7247e-3*100:.1f}%)'}")

# ─────────────────────────────────────────────────────
# HIERARCHY CHECK
# ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("HIERARCHY CHECK at tau=i")
print("Expected: t^c row >> c^c row >> u^c row")
print("=" * 60)
r0_norm = np.linalg.norm(row0i)
r1_norm = beta_u * np.linalg.norm(row1i)
r2_norm = gamma_u * np.linalg.norm(row2i)
print(f"  u^c row norm = {r0_norm:.6e}")
print(f"  c^c row norm = {r1_norm:.6e}")
print(f"  t^c row norm = {r2_norm:.6e}")
if r2_norm > r1_norm > r0_norm:
    print("  -> CORRECT hierarchy (t^c > c^c > u^c)")
elif r1_norm > r2_norm:
    print(f"  -> INVERTED: c^c ({r1_norm:.4f}) > t^c ({r2_norm:.4f})")
    print(f"  -> Row ordering mismatch: largest SV comes from c^c row, NOT t^c row")
    print(f"  -> gamma_u/alpha_u = 0.00104 is TOO SMALL to dominate at tau=i")

# ─────────────────────────────────────────────────────
# SCENARIO 3: Scan gamma/alpha to find correct value for hierarchy at tau=i
# ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SCENARIO 3: Find gamma/alpha so that t^c row dominates at tau=i")
print("and m_c/m_t = 0.00268 (LYD20 target)")
print("=" * 60)

Y5_norm_i = np.linalg.norm(row2i)  # norm of [Y5_3, Y5_5, Y5_4] at tau=i
Y2_norm_i = np.linalg.norm(row1i)  # norm of [Y2_3, Y2_5, Y2_4] at tau=i
Y1_norm_i = np.linalg.norm(row0i)

print(f"  |[Y5_3,Y5_5,Y5_4]| at tau=i = {Y5_norm_i:.4f}")
print(f"  |[Y2_3,Y2_5,Y2_4]| at tau=i = {Y2_norm_i:.4f}")
print(f"  |[Y1_1,Y1_3,Y1_2]| at tau=i = {Y1_norm_i:.4f}")
print(f"  For t^c to dominate: need gamma/alpha * {Y5_norm_i:.4f} >> beta/alpha * {Y2_norm_i:.4f} = {beta_u * Y2_norm_i:.4f}")
print(f"  Minimum gamma/alpha for dominance: ~ {beta_u * Y2_norm_i / Y5_norm_i:.2f}")

# Scan gamma values
print("\n  Scanning gamma/alpha values for m_c/m_t and hierarchy:")
for g in [0.00104, 1.0, 10.0, 50.0, 100.0, 200.0, 300.0, 400.0, 590.0, 1000.0]:
    M_scan = M_u_matrix(tau_i, 1.0, 62.2142, g)
    sv = np.sort(np.linalg.svd(M_scan, compute_uv=False))
    t_norm = g * Y5_norm_i
    c_norm = 62.2142 * Y2_norm_i
    dominant = "t^c" if t_norm > c_norm else "c^c"
    print(f"  gamma/alpha = {g:8.3f}: m_c/m_t = {sv[1]/sv[2]:.6e}, "
          f"m_u/m_c = {sv[0]/sv[1]:.6e}, dominant = {dominant}")

print("\nDone.")
