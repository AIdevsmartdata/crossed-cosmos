"""
I2 DIAGNOSTIC — Deep analysis of what the model can achieve at τ=i.

Key question: Can LYD20 Model VI achieve sin θ_C ≈ 0.225 at τ=i
while SIMULTANEOUSLY fitting all mass ratios to LYD20 values?

The previous run showed:
- At τ=i, joint fit gives sin θ_C = 0.220 BUT m_u/m_c = 0.49 (wrong by 250x)
- At τ=i, forcing correct m_u/m_c gives sin θ_C ≈ 0.001 (wrong by 225x)
- At τ_LYD20, fitting gives sin θ_C = 0.226 with correct m_c/m_t and sin θ_C

This suggests: at τ=i, the model has a structural constraint that
makes it impossible to simultaneously achieve correct m_u/m_c AND correct sin θ_C.

Let me investigate this by:
1. Fixing m_c/m_t correct, scanning sin θ_C vs m_u/m_c at τ=i
2. Understanding the structural reason (fixed-point symmetry of τ=i)
3. Checking if the CKM matrix STRUCTURE at τ=i is compatible with Cabibbo mixing
"""

import numpy as np
from numpy import pi, sqrt, exp
from scipy.linalg import svd
from scipy.optimize import minimize, differential_evolution
import sys, warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/H3')
from mass_matrix import M_u, M_d, modular_forms_weight1, modular_forms_all

TAU_LYD20 = -0.4999 + 0.8958j
TAU_CM = 1j
PDG_SIN_THETA_C = 0.2253
LYD20_THETA12   = 0.22731
LYD20_THETA23   = 0.04873
LYD20_MC_MT     = 0.00268
LYD20_MU_MC     = 0.00204
LYD20_MD_MS     = 0.05182
LYD20_MS_MB     = 0.01309

def svd_sort(M):
    U, s, Vh = svd(M)
    idx = np.argsort(s)
    return U[:, idx], s[idx], Vh[idx, :]

def get_ckm(tau, bu, gu, bd, gd1, gd2):
    Mu = M_u(tau, 1.0, bu, gu)
    Md = M_d(tau, 1.0, bd, gd1, gd2)
    Uu, su, _ = svd_sort(Mu)
    Ud, sd, _ = svd_sort(Md)
    V = Uu.conj().T @ Ud
    return V, su, sd

def s12_from_V(V):
    aV = np.abs(V)
    s13 = aV[0,2]
    denom = sqrt(max(1-s13**2, 1e-30))
    return aV[0,1]/denom, s13, aV[1,2]/denom

# ─────────────────────────────────────────────────────────────────
# ANALYSIS 1: Structure at τ=i — modular form symmetry
# ─────────────────────────────────────────────────────────────────

print("=" * 70)
print("ANALYSIS 1: Modular form symmetry at τ=i")
print("=" * 70)

Y1, Y2, Y3 = modular_forms_weight1(TAU_CM)
f = modular_forms_all(Y1, Y2, Y3)

print(f"\nWeight-1 forms at τ=i:")
print(f"  Y1 = {Y1:.6f}")
print(f"  Y2 = {Y2:.6f}")
print(f"  Y3 = {Y3:.6f}")

print(f"\nM_u structure at τ=i with unit couplings (α=β=γ=1):")
Mu_unit = M_u(TAU_CM, 1.0, 1.0, 1.0)
print("  Row 0 (u^c, Y^1): ", [f'{x:.4f}' for x in Mu_unit[0,:]])
print("  Row 1 (c^c, Y^2): ", [f'{x:.4f}' for x in Mu_unit[1,:]])
print("  Row 2 (t^c, Y^5): ", [f'{x:.4f}' for x in Mu_unit[2,:]])

# At τ=i (fixed point), S transformation maps τ → -1/τ = i
# Under S: Y1 → ... (S'_4 transformation)
# The key point: at the fixed point, S acts on Y_i as a matrix.
# For weight-k forms under S: f(−1/τ) = τ^k ρ(S) f(τ)
# At τ=i: τ^k = i^k, so Y_i acquire phase factors.

# Let's check the ratio Y3/Y2 and Y1/Y2 at τ=i
print(f"\n  Y3/Y2 = {Y3/Y2:.6f}")
print(f"  Y1/Y2 = {Y1/Y2:.6f}")
print(f"  |Y1|/|Y2| = {abs(Y1)/abs(Y2):.4f}")
print(f"  |Y3|/|Y2| = {abs(Y3)/abs(Y2):.4f}")

# At τ=i, check if there's a special structure in M_u
Mu_test = M_u(TAU_CM, 1.0, 99.86627437, 585.57655766)
print(f"\nM_u at τ=i with fitted params (β/α=99.87, γ/α=585.6):")
print("  |M_u| =")
print(np.abs(Mu_test))

Uu_t, su_t, Uvht = svd_sort(Mu_test)
print(f"  Singular values: {su_t}")
print(f"  m_c/m_t = {su_t[1]/su_t[2]:.5e}  [target: {LYD20_MC_MT:.5e}]")
print(f"  m_u/m_c = {su_t[0]/su_t[1]:.5e}  [target: {LYD20_MU_MC:.5e}]")
print(f"  U_L (left sing vectors, columns = mixing matrices):")
print(np.abs(Uu_t))

# ─────────────────────────────────────────────────────────────────
# ANALYSIS 2: At τ=i, scan sin θ_C as function of ONLY down-sector
# with CORRECT up-sector (m_c/m_t and m_u/m_c correct)
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("ANALYSIS 2: Sin θ_C scan with correct up mass ratios at τ=i")
print("=" * 70)

# Find up-sector params at τ=i that give correct mass ratios
def chi2_up(log_params):
    bu, gu = exp(log_params[0]), exp(log_params[1])
    Mu = M_u(TAU_CM, 1.0, bu, gu)
    _, s, _ = svd(Mu)
    s = np.sort(s)
    if s[2] == 0 or s[1] == 0:
        return 1e20
    mc_mt = s[1]/s[2]
    mu_mc = s[0]/s[1]
    return ((np.log(mc_mt) - np.log(LYD20_MC_MT))/0.01)**2 + \
           ((np.log(mu_mc) - np.log(LYD20_MU_MC))/0.01)**2

r_up = minimize(chi2_up, [np.log(100), np.log(600)], method='Nelder-Mead',
                options={'xatol':1e-14, 'fatol':1e-14, 'maxiter':50000})
bu_cm_fit, gu_cm_fit = exp(r_up.x[0]), exp(r_up.x[1])

Mu_cm = M_u(TAU_CM, 1.0, bu_cm_fit, gu_cm_fit)
_, su_cm, _ = svd(Mu_cm)
su_cm = np.sort(su_cm)
print(f"\nUp-sector at τ=i (fitting mass ratios only):")
print(f"  β_u/α_u = {bu_cm_fit:.6f}")
print(f"  γ_u/α_u = {gu_cm_fit:.6f}")
print(f"  m_c/m_t = {su_cm[1]/su_cm[2]:.6e}  [target: {LYD20_MC_MT:.6e}]")
print(f"  m_u/m_c = {su_cm[0]/su_cm[1]:.6e}  [target: {LYD20_MU_MC:.6e}]")

# Now scan down-sector at τ=i, looking for sin θ_C ≈ 0.225
# while also matching m_d/m_s and m_s/m_b

# Try many random starting points to map the solution landscape
print(f"\nScanning down-sector landscape at τ=i...")

Uu_cm, su_cm_sv, _ = svd_sort(Mu_cm)  # Left singular vectors of M_u

best_s12 = None
best_chi2 = np.inf
best_x = None

# Record all solutions found
found_solutions = []

np.random.seed(42)

def chi2_down_strict(x):
    """Fit down-sector with correct mass ratios AND sin θ_C."""
    bd, gd1, gd2_re, gd2_im = exp(x[0]), exp(x[1]), x[2], x[3]
    try:
        Md = M_d(TAU_CM, 1.0, bd, gd1, gd2_re + 1j*gd2_im)
        Ud, sd, _ = svd_sort(Md)
        if sd[2] == 0 or sd[1] == 0:
            return 1e20
        md_ms = sd[0]/sd[1]
        ms_mb = sd[1]/sd[2]
        V = Uu_cm.conj().T @ Ud
        s12, s13, s23 = s12_from_V(V)
        chi2 = (
            ((np.log(md_ms) - np.log(LYD20_MD_MS))/0.05)**2 +
            ((np.log(ms_mb) - np.log(LYD20_MS_MB))/0.05)**2 +
            ((s12 - PDG_SIN_THETA_C)/0.001)**2 +
            ((s13 - 0.00369)/0.001)**2 +
            ((s23 - LYD20_THETA23)/0.002)**2
        )
        return chi2
    except:
        return 1e20

# Run multiple global searches
for seed in [0, 1, 2, 3, 42, 100]:
    bounds = [(-5, 5), (-5, 5), (-15, 15), (-15, 15)]
    r_de = differential_evolution(chi2_down_strict, bounds, maxiter=2000,
                                   tol=1e-10, seed=seed, workers=1, popsize=20, disp=False)
    r_nm = minimize(chi2_down_strict, r_de.x, method='Nelder-Mead',
                    options={'xatol':1e-12, 'fatol':1e-12, 'maxiter':100000})
    if r_nm.fun < 100:
        bd, gd1 = exp(r_nm.x[0]), exp(r_nm.x[1])
        gd2 = r_nm.x[2] + 1j*r_nm.x[3]
        Md = M_d(TAU_CM, 1.0, bd, gd1, gd2)
        Ud, sd, _ = svd_sort(Md)
        V = Uu_cm.conj().T @ Ud
        s12, s13, s23 = s12_from_V(V)
        found_solutions.append({
            'chi2': r_nm.fun, 's12': s12, 's13': s13, 's23': s23,
            'md_ms': sd[0]/sd[1], 'ms_mb': sd[1]/sd[2],
            'x': r_nm.x
        })
    if r_nm.fun < best_chi2:
        best_chi2 = r_nm.fun
        best_x = r_nm.x

print(f"  Best chi2 = {best_chi2:.4e}")
print(f"  Solutions with chi2 < 100: {len(found_solutions)}")

if found_solutions:
    found_solutions.sort(key=lambda x: x['chi2'])
    for sol in found_solutions[:5]:
        print(f"\n  chi2={sol['chi2']:.2f}: sin θ_12={sol['s12']:.5f}, m_d/m_s={sol['md_ms']:.4e}, m_s/m_b={sol['ms_mb']:.4e}")
else:
    print(f"\n  NO SOLUTIONS FOUND with chi2 < 100!")
    print(f"  Best solution: chi2={best_chi2:.4e}")
    bd, gd1 = exp(best_x[0]), exp(best_x[1])
    gd2 = best_x[2] + 1j*best_x[3]
    Md = M_d(TAU_CM, 1.0, bd, gd1, gd2)
    Ud, sd, _ = svd_sort(Md)
    V = Uu_cm.conj().T @ Ud
    s12, s13, s23 = s12_from_V(V)
    print(f"  Best: sin θ_12={s12:.5f}, m_d/m_s={sd[0]/sd[1]:.4e}, m_s/m_b={sd[1]/sd[2]:.4e}")

# ─────────────────────────────────────────────────────────────────
# ANALYSIS 3: Why does V_CKM at τ=i fail? Check U_u structure.
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("ANALYSIS 3: Structural analysis of M_u at τ=i")
print("=" * 70)

Uu_struct, su_struct, Uvh_struct = svd_sort(Mu_cm)
print(f"\nLeft unitary U_uL at τ=i (columns = mixing basis of left-handed Q):")
print(np.abs(Uu_struct))
print("\nPhases of U_uL:")
print(np.angle(Uu_struct, deg=True))

print(f"\nKey observation: U_uL column structure determines which V_CKM patterns are accessible.")
print(f"The Cabibbo mixing requires a non-trivial angle between u and d mass eigenstates.")
print(f"If U_uL is nearly diagonal or has special symmetry at τ=i, V_CKM is constrained.")

# Check the actual M_u entries at τ=i with correct mass ratios
print(f"\nM_u at τ=i (|M_u|):")
print(np.abs(Mu_cm))

# Compare U_uL at LYD20 τ vs at τ=i
Mu_lyd20 = M_u(TAU_LYD20, 1.0, 99.5, 590.7)
Uu_lyd20, su_lyd20_sv, _ = svd_sort(Mu_lyd20)
print(f"\nLeft unitary U_uL at LYD20 τ:")
print(np.abs(Uu_lyd20))

print("\n\nDIAGNOSIS:")
print("The U_uL matrix at τ=i vs τ_LYD20 differs significantly.")
print("At τ=i, the CKM structure is constrained by the S'_4 fixed-point symmetry.")

# ─────────────────────────────────────────────────────────────────
# ANALYSIS 4: What sin θ_C values ARE accessible at τ=i?
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("ANALYSIS 4: Range of sin θ_C accessible at τ=i with correct mass ratios")
print("=" * 70)

# Scan over down-sector couplings, compute sin θ_C
# Don't impose sin θ_C target — just see what range is achievable

best_s12_vals = []

# Use random search
np.random.seed(0)
n_samples = 3000
for _ in range(n_samples):
    log_bd  = np.random.uniform(-4, 4)
    log_gd1 = np.random.uniform(-4, 4)
    gd2_re  = np.random.uniform(-10, 10)
    gd2_im  = np.random.uniform(-10, 10)

    try:
        Md = M_d(TAU_CM, 1.0, exp(log_bd), exp(log_gd1), gd2_re + 1j*gd2_im)
        Ud, sd, _ = svd_sort(Md)
        if sd[2] == 0 or sd[1] == 0:
            continue
        md_ms = sd[0]/sd[1]
        ms_mb = sd[1]/sd[2]
        # Only keep if mass ratios are in right ballpark (within factor 3)
        if (0.01 < md_ms < 0.3) and (0.003 < ms_mb < 0.05):
            V = Uu_cm.conj().T @ Ud
            s12, s13, s23 = s12_from_V(V)
            best_s12_vals.append(s12)
    except:
        pass

if best_s12_vals:
    best_s12_vals = sorted(best_s12_vals)
    n = len(best_s12_vals)
    print(f"\nFound {n} parameter sets with approximate mass ratios at τ=i")
    print(f"  sin θ_C range: [{min(best_s12_vals):.5f}, {max(best_s12_vals):.5f}]")
    print(f"  10th percentile: {best_s12_vals[n//10]:.5f}")
    print(f"  50th percentile: {best_s12_vals[n//2]:.5f}")
    print(f"  90th percentile: {best_s12_vals[9*n//10]:.5f}")
    print(f"  PDG target: {PDG_SIN_THETA_C:.5f}")
    print(f"  Can reach PDG target? {any(abs(s - PDG_SIN_THETA_C) < 0.015 for s in best_s12_vals)}")
else:
    print("No valid parameter sets found in random scan")

# ─────────────────────────────────────────────────────────────────
# ANALYSIS 5: Scan with STRICT mass ratios using refined optimizer
# ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("ANALYSIS 5: Refined search — fix mass ratios, maximize sin θ_C")
print("=" * 70)

def neg_s12_given_masses(x):
    """Maximize sin θ_C subject to correct mass ratios."""
    bd, gd1, gd2_re, gd2_im = exp(x[0]), exp(x[1]), x[2], x[3]
    try:
        Md = M_d(TAU_CM, 1.0, bd, gd1, gd2_re + 1j*gd2_im)
        Ud, sd, _ = svd_sort(Md)
        if sd[2] == 0 or sd[1] == 0:
            return 1e20
        md_ms = sd[0]/sd[1]
        ms_mb = sd[1]/sd[2]
        V = Uu_cm.conj().T @ Ud
        s12, s13, s23 = s12_from_V(V)
        # Penalise if mass ratios too far off
        penalty = (
            100 * ((np.log(md_ms) - np.log(LYD20_MD_MS))/0.2)**2 +
            100 * ((np.log(ms_mb) - np.log(LYD20_MS_MB))/0.2)**2
        )
        return -s12 + penalty
    except:
        return 1e20

for seed in [0, 1, 2, 42]:
    r = differential_evolution(neg_s12_given_masses,
                                [(-5, 5), (-5, 5), (-15, 15), (-15, 15)],
                                maxiter=3000, tol=1e-10, seed=seed, workers=1, popsize=20, disp=False)
    r2 = minimize(neg_s12_given_masses, r.x, method='Nelder-Mead',
                  options={'xatol':1e-12, 'fatol':1e-12, 'maxiter':100000})
    bd, gd1 = exp(r2.x[0]), exp(r2.x[1])
    gd2 = r2.x[2] + 1j*r2.x[3]
    Md = M_d(TAU_CM, 1.0, bd, gd1, gd2)
    Ud, sd, _ = svd_sort(Md)
    V = Uu_cm.conj().T @ Ud
    s12, s13, s23 = s12_from_V(V)
    print(f"  seed={seed}: max sin θ_12 = {s12:.5f} (χ²_mass={r2.fun+s12:.2f})")
    print(f"    m_d/m_s={sd[0]/sd[1]:.4e}, m_s/m_b={sd[1]/sd[2]:.4e}")
    print(f"    sin θ_12={s12:.5f}, sin θ_23={s23:.5f}")
