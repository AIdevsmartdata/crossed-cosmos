#!/usr/bin/env python3
"""Pourquoi les exposants des 17 patterns sont dans {0, ±1/2, ±1, ±2} ?

Tests :
1. Décomposition complète avec ALTERNATIVES (chaque pattern peut avoir
   plusieurs formes équivalentes — capter la diversité algébrique)
2. Bound test : |a|+|b|+|c|+|d| ≤ N pour quel N?
3. Lien modular weight theory (Eisenstein E_k, half-integer Shimura)
4. Sum-rule sur Casimir SU(3) representations
5. Test : si on retire un pattern, les autres respectent encore la sparsity?
"""
import math
import numpy as np
from itertools import product
from fractions import Fraction

kappa = 1/6
pi_const = math.pi

# 17 patterns avec valeurs
patterns = [
    ("κ_LSI", 1/6, "STRONG", "adj", 1),
    ("α_LSI", 5/6, "STRONG", "adj", 1),
    ("λ_H", 1/8, "EW", "doublet", 2),
    ("σ_8", math.sqrt(2/3), "COSMO", "scalar", 0),
    ("m_2++/m_0++", math.sqrt(2), "GLUEBALL", "tensor", 2),
    ("m_0-+/m_0++", 3/2, "GLUEBALL", "scalar", 0),
    ("Koide", 2/3, "LEPTON", "singlet", 1),
    ("m_p/Λ_pg", 6*pi_const/5, "STRONG", "triplet", 3),
    ("|μ_Σ+/μ_Ξ-|", 6*pi_const/5, "EM", "magnetic", 3),
    ("V_ud", 35/36, "WEAK", "diag", 1),
    ("V_cb", 1/24, "WEAK", "off", 2),
    ("V_us", pi_const/14, "WEAK", "off", 2),
    ("V_ub", 5/1296, "WEAK", "off", 3),
    ("V_tb", 1 - (1/6)**4, "WEAK", "diag", 1),
    ("K_ν_NH", 7/12, "NEUTRINO", "singlet", 1),
    ("sin²θ13", 1/45, "NEUTRINO_mix", "mix", 2),
    ("V_cs", 35/36, "WEAK", "diag", 1),  # duplicate V_ud formula
]

# ==============================================================
# Test 1 : Multiple decompositions per pattern
# ==============================================================
print("="*78)
print("Test 1 — All algebraic decompositions per pattern")
print("="*78)

# Decompose as κ^a · (1-κ)^b · (1+κ)^c · π^d · n/m
# Allow half-integers for exponents
a_set = [-2, -1, -0.5, 0, 0.5, 1, 2]
b_set = [-2, -1, -0.5, 0, 0.5, 1, 2]
c_set = [-2, -1, -0.5, 0, 0.5, 1, 2]
d_set = [-2, -1, -0.5, 0, 0.5, 1, 2]
n_set = list(range(1, 13))
m_set = list(range(1, 13))

def value(a, b, c, d, n, m):
    return (kappa**a) * ((1-kappa)**b) * ((1+kappa)**c) * (pi_const**d) * (n/m)

def total_weight(a, b, c, d):
    return abs(a) + abs(b) + abs(c) + abs(d)

# For each pattern, find ALL decompositions within 0.5% rel diff and with total weight ≤ 3
patterns_decomps = {}
for name, val, sector, rep, complexity in patterns:
    if val <= 0:
        continue
    decomps = []
    for a in a_set:
        for b in b_set:
            for c in c_set:
                for d in d_set:
                    tw = total_weight(a, b, c, d)
                    if tw > 3.5:
                        continue
                    for n in n_set:
                        for m in m_set:
                            v = value(a, b, c, d, n, m)
                            if v > 0 and abs(v - val)/val < 0.005:
                                decomps.append((a, b, c, d, n, m, tw, abs(v-val)/val*100))
    # Sort by total_weight + log(n*m) (prefer simple)
    decomps.sort(key=lambda x: (x[6], x[4]*x[5], x[7]))
    patterns_decomps[name] = decomps[:5]  # top 5

# Print
print(f"\n{'Pattern':>20} {'Value':>10} | Top 3 decompositions (within 0.5%)")
print("-"*100)
for name, val, sector, rep, _ in patterns:
    if name not in patterns_decomps or not patterns_decomps[name]:
        continue
    decs = patterns_decomps[name]
    print(f"{name:>20} {val:>10.5f} |")
    for i, (a, b, c, d, n, m, tw, rel) in enumerate(decs[:3]):
        f = f"κ^{a}·(1-κ)^{b}·(1+κ)^{c}·π^{d}·({n}/{m})"
        print(f"  {'':>30}   {f:<60} (TW={tw}, {rel:.2f}%)")

# ==============================================================
# Test 2 : Maximum total weight bound
# ==============================================================
print("\n" + "="*78)
print("Test 2 — Maximum total weight needed")
print("="*78)

# For each pattern, take MINIMUM total weight decomposition
min_tw_per_pattern = {}
for name, decs in patterns_decomps.items():
    if decs:
        min_tw_per_pattern[name] = min(d[6] for d in decs)

print(f"\nMinimum total weight |a|+|b|+|c|+|d| for each pattern :")
tws = []
for name, val, _, _, _ in patterns:
    if name in min_tw_per_pattern:
        tw = min_tw_per_pattern[name]
        tws.append(tw)
        print(f"  {name:>20} : min TW = {tw}")
print(f"\nMax TW across 17 patterns : {max(tws) if tws else 'N/A'}")
print(f"All TW ≤ 3 ? : {all(tw <= 3 for tw in tws)}")
print(f"All TW ≤ 2 ? : {all(tw <= 2 for tw in tws)}")

# Plot distribution
from collections import Counter
tw_counter = Counter(tws)
print(f"\nDistribution of TW :")
for tw in sorted(tw_counter.keys()):
    print(f"  TW={tw}: {tw_counter[tw]} patterns")

# ==============================================================
# Test 3 : Modular weight theory check
# ==============================================================
print("\n" + "="*78)
print("Test 3 — Modular form weight analogy")
print("="*78)

# Eisenstein series E_k has weight k (even integers k ≥ 2 : 2, 4, 6, 8, ...)
# Theta series Shimura have half-integer weights k/2
# Hauptmodul j(τ) has weight 0
# Total weight of a product = sum of weights

# Map exponents to modular weights :
# κ-related → q-related (q = exp(2πi·τ))
# (1-κ), (1+κ) → algebraic shifts of κ
# π → comes from period of modular forms / Eisenstein integration

# Total "weight" in modular sense = 2(a + b + c) for κ-related terms
# (d for π is separate)

# Hypothesis : "modular weight" = 2(a+b+c) ∈ {0, 1, 2, 3, 4, 5, 6} only
print(f"\nModular weight estimate W_mod = 2(a+b+c) for each pattern :")
for name, val, _, _, _ in patterns:
    if name not in patterns_decomps or not patterns_decomps[name]:
        continue
    a, b, c, d, n, m, tw, rel = patterns_decomps[name][0]
    w_mod = 2*(a + b + c)
    print(f"  {name:>20} : W_mod = {w_mod}, π-weight = 2d = {2*d}")

# ==============================================================
# Test 4 : Casimir spectrum SU(3) link
# ==============================================================
print("\n" + "="*78)
print("Test 4 — Lien Casimir SU(3) eigenvalues")
print("="*78)

# Casimir C_2 of SU(3) for various irreps :
# trivial : C_2 = 0
# fundamental (3) : C_2 = 4/3
# anti-fund (3̄) : C_2 = 4/3
# adjoint (8) : C_2 = 3
# decuplet (10) : C_2 = 6
# 6 of SU(3) : C_2 = 10/3

casimirs = {
    "trivial(1)": 0,
    "fund(3)": 4/3,
    "antifund(3̄)": 4/3,
    "6": 10/3,
    "adj(8)": 3,
    "10": 6,
}
print(f"\nCasimir C_2(R) of SU(3) irreps :")
for r, c in casimirs.items():
    print(f"  {r:>15} : C_2 = {c}")

# Test if any pattern formula relates to Casimir differences
# e.g., m_2++/m_0++ = √(C_2(2++)/C_2(0++)) ? Standard Casimir scaling
# For glueballs : 2++ has J=2, 0++ has J=0 — Casimir of J(J+1)/3 = 2/3 vs 0
# Hmm not directly Casimir

# Casimir ratios :
print(f"\nCasimir ratios :")
for r1, c1 in casimirs.items():
    for r2, c2 in casimirs.items():
        if c2 > 0 and c1 > c2:
            print(f"  C_2({r1})/C_2({r2}) = {c1/c2:.3f}")

# Look for matches with pattern values
print(f"\nMatches Casimir ratios with pattern values (within 5%) :")
for name, val, _, _, _ in patterns:
    for r1, c1 in casimirs.items():
        for r2, c2 in casimirs.items():
            if c2 > 0 and c1 > 0 and c1 != c2:
                ratio = c1/c2
                if abs(val - ratio)/val < 0.05:
                    print(f"  {name} = {val:.4f} ≈ C_2({r1})/C_2({r2}) = {ratio:.4f}")

# ==============================================================
# Test 5 : Random patterns — would they have similar sparsity?
# ==============================================================
print("\n" + "="*78)
print("Test 5 — Bonferroni : do RANDOM numbers decompose similarly?")
print("="*78)

# Generate 17 random values in similar range as patterns
import random
random.seed(2026)
random_vals = []
for _ in range(17):
    v = math.exp(random.uniform(-6, 4))  # log-uniform in [e^-6, e^4]
    random_vals.append(v)

random_tws = []
for v in random_vals:
    best_tw = float('inf')
    for a in a_set:
        for b in b_set:
            for c in c_set:
                for d in d_set:
                    tw = total_weight(a, b, c, d)
                    if tw > 3.5:
                        continue
                    for n in n_set:
                        for m in m_set:
                            val_test = value(a, b, c, d, n, m)
                            if val_test > 0 and abs(val_test - v)/v < 0.005:
                                if tw < best_tw:
                                    best_tw = tw
    if best_tw < float('inf'):
        random_tws.append(best_tw)
    else:
        random_tws.append(None)

print(f"\nMin TW for 17 RANDOM values within 0.5% match :")
none_count = sum(1 for x in random_tws if x is None)
matched = [x for x in random_tws if x is not None]
print(f"  Matched : {len(matched)}/17")
print(f"  Not matched (no decomp <0.5% within TW≤3.5) : {none_count}")
if matched:
    print(f"  Mean TW (matched) : {np.mean(matched):.2f}")
    print(f"  Max TW (matched) : {max(matched)}")

# ==============================================================
# Verdict
# ==============================================================
print("\n" + "="*78)
print("VERDICT")
print("="*78)

real_max_tw = max(tws) if tws else 0
print(f"""
Real patterns max TW : {real_max_tw}
Random patterns matched : {len(matched)}/17 (vs real 17/17 if all decomposed)

If Random = Real → la sparsity n'est pas spéciale (juste densité)
If Random < Real → la sparsity DES PATTERNS est statistiquement significative
""")

# Mod theory significance
print("Modular form analogy :")
print("  Si chaque exposant a∈{0, ±1/2, ±1, ±2} correspond à un poids modulaire,")
print("  alors la sparsity des exposants = sparsity des formes modulaires de bas poids")
print("  utilisées pour exprimer les observables.")
print("  ")
print("  Hypothèse : 17 patterns = projections de produits Eisenstein/theta de bas poids")
print("  sur la fibre de modules SU(3) D=4.")
print("  ")
print("  Test décisif : si exposant a > 2 jamais nécessaire pour AUCUN observable,")
print("  c'est une CONSÉQUENCE de la structure modulaire de A/G.")

print("\nDONE.")
