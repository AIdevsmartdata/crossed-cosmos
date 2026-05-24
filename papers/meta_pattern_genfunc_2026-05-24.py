#!/usr/bin/env python3
"""META-PATTERN search : trouve la fonction génératrice F(κ, |Φ⁺|, D, sector)
qui produit les 17 patterns observés comme cas particuliers.

(A) S_EE interpolation : C ∝ dim·(1-κ)^α — chercher α qui matche.
(B) Décomposition des 17 patterns comme κ^a · (1-κ)^b · (1+κ)^c · π^d · rational.
(C) Recherche de règles sectorielles.
"""
import numpy as np
import math
from scipy.optimize import minimize_scalar, minimize
import itertools

kappa = 1/6
pi_const = math.pi
phi_plus = 3
D = 4
N_c = 3
dim_G = N_c**2 - 1  # = 8

# ==============================================================
# PART A : S_EE interpolation
# ==============================================================
print("="*78)
print("PART A — S_EE interpolation : C ∝ dim · (1-κ)^α et autres familles")
print("="*78)

# Rabenstein 2018 data
C_data = {
    "SU(2)": (0.054, 0.001),
    "SU(3)": (0.173, 0.005),
    "SU(4)": (0.411, 0.006),
}
groups_data = [
    ("SU(2)", 2, 1, 1/2),     # N, |Φ⁺|, κ
    ("SU(3)", 3, 3, 1/6),
    ("SU(4)", 4, 6, 1/12),
]

# Family 1 : C ∝ dim·(1-κ)^α
def predict_F1(N, kappa, alpha, A):
    dim = N**2 - 1
    return A * dim * (1-kappa)**alpha

# Family 2 : C ∝ |Φ⁺|^β · dim^γ
def predict_F2(N, phi, beta, gamma, A):
    dim = N**2 - 1
    return A * phi**beta * dim**gamma

# Family 3 : C ∝ (N²-1)^p (empirical found earlier p=1.26)
def predict_F3(N, p, A):
    dim = N**2 - 1
    return A * dim**p

# Family 4 : C ∝ dim · log(N) ? (sub-leading log corrections)
def predict_F4(N, A, B):
    dim = N**2 - 1
    return A * dim + B * math.log(N)

# Family 5 : C ∝ (dim) · (1-κ + γ·κ²)
def predict_F5(N, kappa, gamma, A):
    dim = N**2 - 1
    return A * dim * (1 - kappa + gamma*kappa**2)

# Family 6 : C ∝ (N²-1)·(N²)^δ
def predict_F6(N, delta, A):
    dim = N**2 - 1
    return A * dim * N**(2*delta)

# Fit each family
print(f"\n{'Family':>50} {'A':>10} {'param':>10} {'χ² SU(2,3,4)':>15}")
print("-"*100)

# Family 1 : Fix A from SU(3), find α
def chi2_F1(alpha):
    # Normalize so SU(3) matches
    A = C_data["SU(3)"][0] / (8 * (5/6)**alpha)
    chi2 = 0
    for name, N, phi, k in groups_data:
        obs, err = C_data[name]
        pred = predict_F1(N, k, alpha, A)
        chi2 += ((pred - obs)/err)**2
    return chi2

res1 = minimize_scalar(chi2_F1, bounds=(-3, 3), method='bounded')
alpha_best = res1.x
A1 = C_data["SU(3)"][0] / (8 * (5/6)**alpha_best)
print(f"  Family 1 : C ∝ dim·(1-κ)^α  →  α = {alpha_best:.3f}, A = {A1:.5f}, χ² = {res1.fun:.2f}")
for name, N, phi, k in groups_data:
    obs, err = C_data[name]
    pred = predict_F1(N, k, alpha_best, A1)
    print(f"    {name:>10} : obs={obs:.4f}±{err:.4f}, pred={pred:.4f}, σ={abs(obs-pred)/err:.2f}")

# Family 2 : 2 params
def chi2_F2(params):
    beta, gamma = params
    A = C_data["SU(3)"][0] / (3**beta * 8**gamma)
    chi2 = 0
    for name, N, phi, k in groups_data:
        obs, err = C_data[name]
        pred = predict_F2(N, phi, beta, gamma, A)
        chi2 += ((pred - obs)/err)**2
    return chi2

res2 = minimize(chi2_F2, [0.5, 1.0], method='Nelder-Mead')
beta_best, gamma_best = res2.x
A2 = C_data["SU(3)"][0] / (3**beta_best * 8**gamma_best)
print(f"\n  Family 2 : C ∝ |Φ⁺|^β · dim^γ  →  β={beta_best:.3f}, γ={gamma_best:.3f}, χ²={res2.fun:.2f}")
for name, N, phi, k in groups_data:
    obs, err = C_data[name]
    pred = predict_F2(N, phi, beta_best, gamma_best, A2)
    print(f"    {name:>10} : obs={obs:.4f}, pred={pred:.4f}, σ={abs(obs-pred)/err:.2f}")

# Family 3 : 1 param
res3 = minimize_scalar(lambda p: sum(((C_data[n][0] / (C_data['SU(3)'][0]/8**p) - (N**2-1)**p) /
                                      C_data[n][1] * (C_data['SU(3)'][0]/8**p))**2
                                     for n, N, _, _ in groups_data),
                       bounds=(0.5, 2.5), method='bounded')
p3 = res3.x
A3 = C_data["SU(3)"][0] / 8**p3
print(f"\n  Family 3 : C ∝ (N²-1)^p  →  p={p3:.3f}, A={A3:.5f}")
for name, N, phi, k in groups_data:
    obs, err = C_data[name]
    pred = A3 * (N**2-1)**p3
    print(f"    {name:>10} : obs={obs:.4f}, pred={pred:.4f}, σ={abs(obs-pred)/err:.2f}")

# Family 5 : C ∝ dim·(1-κ+γκ²)
def chi2_F5(gamma):
    A = C_data["SU(3)"][0] / (8 * (1 - 1/6 + gamma*(1/6)**2))
    chi2 = 0
    for name, N, phi, k in groups_data:
        obs, err = C_data[name]
        pred = A * (N**2-1) * (1 - k + gamma*k**2)
        chi2 += ((pred - obs)/err)**2
    return chi2

res5 = minimize_scalar(chi2_F5, bounds=(-20, 20), method='bounded')
g5 = res5.x
A5 = C_data["SU(3)"][0] / (8 * (1 - 1/6 + g5*(1/6)**2))
print(f"\n  Family 5 : C ∝ dim·(1-κ+γκ²)  →  γ={g5:.3f}, χ²={res5.fun:.2f}")
for name, N, phi, k in groups_data:
    obs, err = C_data[name]
    pred = A5 * (N**2-1) * (1 - k + g5*k**2)
    print(f"    {name:>10} : obs={obs:.4f}, pred={pred:.4f}, σ={abs(obs-pred)/err:.2f}")

print(f"""

INTERPRÉTATION S_EE :

Family 1 (1-κ)^α : α best fit ≈ {alpha_best:.3f}
  α=0 : pure (N²-1)  → rejected
  α=1 : pure (1-κ)(N²-1)  → rejected
  α=0.5 : (1-κ)^(1/2) interpolation? → check χ²

Family 3 (N²-1)^p : p={p3:.3f} ≈ 1.26
  Not clean closed-form

Family 5 : dim·(1-κ+γκ²) avec γ={g5:.2f}
  Si γ ≈ entier simple : suggestif. Sinon : encore fit ad hoc.
""")

# Check if α=1/2 works
A_half = C_data["SU(3)"][0] / (8 * math.sqrt(5/6))
print(f"\nSpecial : C ∝ dim·√(1-κ) hypothesis (DS Bot suggested!) :")
for name, N, phi, k in groups_data:
    obs, err = C_data[name]
    pred = A_half * (N**2-1) * math.sqrt(1-k)
    print(f"  {name:>10} : obs={obs:.4f}±{err:.4f}, pred={pred:.4f}, σ={abs(obs-pred)/err:.2f}")

# ==============================================================
# PART B : Meta-pattern decomposition
# ==============================================================
print("\n" + "="*78)
print("PART B — Meta-pattern decomposition: O = κ^a·(1-κ)^b·(1+κ)^c·π^d·rational")
print("="*78)

# 17 patterns avec valeurs et formules
patterns_17 = [
    # (name, value, sector, repr, formula_kappa_text)
    ("κ_LSI", 1/6, "STRONG", "adj", "κ"),
    ("α_LSI", 5/6, "STRONG", "adj", "1-κ"),
    ("λ_H", 1/8, "WEAK_higgs", "doublet", "κ·(D-1)/D"),
    ("σ_8", math.sqrt(2/3), "COSMO", "scalar", "√(1-2κ)"),
    ("m_2++/m_0++", math.sqrt(2), "GLUEBALL", "tensor", "√2"),
    ("m_0-+/m_0++", 1.5, "GLUEBALL", "scalar", "3/2"),
    ("Koide K_lep", 2/3, "LEPTON", "singlet", "4κ"),
    ("m_p/Λ_pg", 6*pi_const/5, "STRONG", "triplet", "π/(1-κ)"),
    ("|μ_Σ+/μ_Ξ-|", 6*pi_const/5, "EM", "magnetic", "π/(1-κ)"),
    ("V_ud", 35/36, "WEAK_diag", "fund", "1-κ²"),
    ("V_cb", 1/24, "WEAK_off", "fund", "3κ²/2"),
    ("V_us", pi_const/14, "WEAK_off", "fund", "π/(2N_H)"),
    ("V_ub", 5/1296, "WEAK_off", "fund", "κ³(1-κ)"),
    ("V_tb", 1-(1/6)**4, "WEAK_diag", "fund", "1-κ⁴"),
    ("K_ν_NH", 7/12, "NEUTRINO", "singlet", "(1+κ)/2"),
    ("sin²θ13", 1/45, "NEUTRINO_mix", "mix", "4κ²/5"),
    ("|μ_Σ+/μ_Ξ-|_alt", 6*pi_const/5, "EM", "magnetic", "π/(1-κ)"),  # duplicate for verify
]

# Decompose each as κ^a · (1-κ)^b · (1+κ)^c · π^d · rational
# log(O) = a·log(κ) + b·log(1-κ) + c·log(1+κ) + d·log(π) + log(rational)
log_kappa = math.log(kappa)         # -1.79
log_1mk = math.log(1-kappa)         # -0.182
log_1pk = math.log(1+kappa)         # +0.154
log_pi = math.log(pi_const)         # +1.144

print(f"\nBase factors :")
print(f"  log(κ)       = {log_kappa:.4f}")
print(f"  log(1-κ)     = {log_1mk:.4f}")
print(f"  log(1+κ)     = {log_1pk:.4f}")
print(f"  log(π)       = {log_pi:.4f}")

# For each pattern, find (a, b, c, d, q) where q is log of rational
# q = log(O) - a·log_kappa - b·log_1mk - c·log_1pk - d·log_pi
# Try grid of small (a, b, c, d) integers + half-integers
print(f"\n{'Pattern':>20} {'Value':>10} {'Best (a, b, c, d, rat)':>40} {'Match %':>8}")
print("-"*95)

best_decomps = []
for name, val, sector, rep, _ in patterns_17:
    if val <= 0:
        continue
    log_O = math.log(val)

    best_diff = float('inf')
    best_combo = None
    # Try a, b, c in [-3, 3] half-integers, d in [-2, 2] half-integers
    for a in [-2, -1, -0.5, 0, 0.5, 1, 2, 3]:
        for b in [-2, -1, -0.5, 0, 0.5, 1, 2]:
            for c in [-1, 0, 0.5, 1]:
                for d in [-1, -0.5, 0, 0.5, 1, 2]:
                    # Compute residual = log(rational)
                    res_log = log_O - a*log_kappa - b*log_1mk - c*log_1pk - d*log_pi
                    res_rational = math.exp(res_log)
                    # Check if res_rational is close to a simple rational
                    for num in range(1, 16):
                        for den in range(1, 16):
                            r = num/den
                            if abs(res_rational - r) < 0.01 * res_rational and abs(r) > 0.001:
                                diff = abs(res_rational - r)/res_rational
                                # Score : prefer smaller exponents + smaller integers
                                score = abs(a) + abs(b) + abs(c) + abs(d) + (num + den)/20 + diff*100
                                if score < best_diff:
                                    best_diff = score
                                    best_combo = (a, b, c, d, num, den, diff)

    if best_combo:
        a, b, c, d, num, den, diff = best_combo
        pred = (kappa**a) * ((1-kappa)**b) * ((1+kappa)**c) * (pi_const**d) * (num/den)
        formula_str = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({num}/{den})"
        rel = abs(pred - val)/val * 100
        print(f"{name:>20} {val:>10.5f} {formula_str:>40} {rel:>7.2f}%")
        best_decomps.append((name, sector, a, b, c, d, num, den, rel))

# Analyze : do exponents cluster by sector?
print(f"\n=== ANALYSIS : exponent clusters by sector ===")
from collections import defaultdict
sector_decomps = defaultdict(list)
for name, sector, a, b, c, d, num, den, rel in best_decomps:
    sector_decomps[sector].append((name, a, b, c, d, num, den))

for sec, lst in sector_decomps.items():
    print(f"\nSector {sec} :")
    for n, a, b, c, d, num, den in lst:
        print(f"  {n:>20} : (a={a}, b={b}, c={c}, d={d}, rat={num}/{den})")

# Check : are exponents constrained?
print(f"\n=== Exponent statistics across 17 patterns ===")
all_a = [r[2] for r in best_decomps]
all_b = [r[3] for r in best_decomps]
all_c = [r[4] for r in best_decomps]
all_d = [r[5] for r in best_decomps]
print(f"a (κ-exponent) : {all_a}")
print(f"b ((1-κ)-exponent) : {all_b}")
print(f"c ((1+κ)-exponent) : {all_c}")
print(f"d (π-exponent) : {all_d}")
print(f"\na range : [{min(all_a)}, {max(all_a)}]")
print(f"b range : [{min(all_b)}, {max(all_b)}]")
print(f"c range : [{min(all_c)}, {max(all_c)}]")
print(f"d range : [{min(all_d)}, {max(all_d)}]")

print("\nIf exponents cluster in small set, the META-pattern is :")
print("  O_i = κ^(a_i) · (1-κ)^(b_i) · (1+κ)^(c_i) · π^(d_i) · rational_i")
print("with (a, b, c, d) taking values in a small discrete set.")
print("This would be a META-formula of the SM.")

print("\nDONE.")
