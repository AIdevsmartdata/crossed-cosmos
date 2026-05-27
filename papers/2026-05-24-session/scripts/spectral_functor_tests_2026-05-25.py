"""
Tests pour le foncteur spectral H²(M, ad P) → observables SM
==============================================================
Hypothèses DS Bot + C :
1. /23 cluster = K3 cohomology (b_2 = 22 + 1 trivial = 23)
2. /13 cluster = Weinberg secteur (sin²θ_W = 3/13)
3. /15 cluster = Higgs secteur (m_H/v⁴ = 1/15)
4. /27 cluster = EW scale (m_Z/v = 10/27)
5. ζ_M(s) factorise sur premiers {13, 23, 27...}

Tests calculables maintenant.
Auteur : Kevin Remondiere
"""
import numpy as np
from math import gcd
from collections import Counter

# Toutes les cibles SM
SM = {
    'm_H/v':       0.50808,
    'm_Z/v':       0.37035,
    'm_W/v':       0.32644,
    '(m_H/m_Z)²':  1.88210,
    '(m_W/m_Z)²':  0.77695,
    '(m_t/m_Z)²':  3.58145,
    'm_H/m_Z':     1.37190,
    'sin²θ_W':     0.23121,
    'sin θ_W':     0.48084,
    'cos²θ_W':     0.76879,
    'cos θ_W':     0.87681,
    'α_s':         0.118,
    'α_em(MZ)':    1/127.952,
    'y_top':       0.99119,
    'y_top²':      0.98246,
    'y_b':         0.02401,
    'y_τ':         0.01021,
    'A_CKM':       0.826,
    'A_CKM²':      0.6823,
    'λ_CKM':       0.225,
    'λ²':          0.05063,
    'ρ̄':           0.159,
    'η̄':           0.348,
    'sin δ_CKM':   0.91212,
    'cos δ_CKM':   0.40992,
    'δ_CKM/π':     0.36556,
    'sin²θ₁₂':     0.30319,
    'sin²θ₂₃':     0.57131,
    'sin²θ₁₃':     0.022,
    'θ₂₃/π':       0.27278,
    'θ₁₂/π':       0.18560,
    'θ₁₃/π':       0.04744,
    'n_s':         0.9649,
    'Ω_b/Ω_DM':    0.18657,
    'Ω_DM/Ω_b':    5.36,
}

print("="*78)
print("TEST 1 : /23 CLUSTER — observables fittent p/23 à <0.5% ?")
print("="*78)
print(f"  Hypothesis : K3 cohomology b_2 = 22 + 1 trivial = 23 levels")
print()
slash23_matches = []
for name, val in SM.items():
    for p in range(1, 24):
        if abs(p/23 - val)/val < 0.005:
            slash23_matches.append((name, val, p, abs(p/23-val)/val*100))
            break
print(f"Matches p/23 :")
for name, val, p, err in slash23_matches:
    print(f"  {name:15s} : {val:.5f} ≈ {p}/23 = {p/23:.5f}  ({err:.2f}%)")
print(f"\n→ {len(slash23_matches)} observables fit /23 — cluster taille {len(slash23_matches)}")

print("\n" + "="*78)
print("TEST 2 : /13 CLUSTER — observables fittent p/13 ?")
print("="*78)
print(f"  Hypothesis : Weinberg sector sin²θ_W = 3/13")
slash13 = []
for name, val in SM.items():
    for p in range(1, 14):
        if abs(p/13 - val)/val < 0.005:
            slash13.append((name, val, p, abs(p/13-val)/val*100))
            break
print(f"Matches p/13 :")
for name, val, p, err in slash13:
    print(f"  {name:15s} : {val:.5f} ≈ {p}/13 = {p/13:.5f}  ({err:.2f}%)")
print(f"\n→ {len(slash13)} observables fit /13")

print("\n" + "="*78)
print("TEST 3 : /15 CLUSTER — observables fittent p/15 ?")
print("="*78)
print(f"  Hypothesis : Higgs sector (m_H/v)⁴ = 1/15")
slash15 = []
for name, val in SM.items():
    for p in range(1, 16):
        if abs(p/15 - val)/val < 0.005:
            slash15.append((name, val, p, abs(p/15-val)/val*100))
            break
print(f"Matches p/15 :")
for name, val, p, err in slash15:
    print(f"  {name:15s} : {val:.5f} ≈ {p}/15 = {p/15:.5f}  ({err:.2f}%)")
print(f"\n→ {len(slash15)} observables fit /15")

print("\n" + "="*78)
print("TEST 4 : /27 CLUSTER — observables fittent p/27 ?")
print("="*78)
print(f"  Hypothesis : EW scale m_Z/v = 10/27 (27 = 3³)")
slash27 = []
for name, val in SM.items():
    for p in range(1, 28):
        if abs(p/27 - val)/val < 0.005:
            slash27.append((name, val, p, abs(p/27-val)/val*100))
            break
print(f"Matches p/27 :")
for name, val, p, err in slash27:
    print(f"  {name:15s} : {val:.5f} ≈ {p}/27 = {p/27:.5f}  ({err:.2f}%)")
print(f"\n→ {len(slash27)} observables fit /27")

print("\n" + "="*78)
print("TEST 5 : MAGIC DENOMINATORS — distribution best-fit denominators")
print("="*78)
print(f"  Pour chaque obs, on cherche LE meilleur p/q rationnel (q≤30) <0.3%")
print()
best_denoms = []
for name, val in SM.items():
    best = None
    best_err = 1
    for q in range(2, 31):
        for p in range(1, 5*q+1):
            if gcd(p, q) == 1:
                err = abs(p/q - val)/val
                if err < best_err:
                    best_err = err
                    best = (p, q)
    if best and best_err < 0.003:
        best_denoms.append((name, val, best, best_err*100))

print("Best p/q < 0.3% pour chaque observable :")
for name, val, (p, q), err in sorted(best_denoms, key=lambda x: x[2][1]):
    print(f"  {name:15s} : {val:.5f} = {p}/{q} = {p/q:.5f}  ({err:.2f}%)")

# Distribution des dénominateurs
denoms = [q for _, _, (_, q), _ in best_denoms]
print(f"\nDistribution dénominateurs (occurrence) :")
counter = Counter(denoms)
for q, count in counter.most_common():
    print(f"  q={q:2d} : {count} occurrence(s)")

print("\n" + "="*78)
print("TEST 6 : K3 b_2 = 22 + 1 = 23 — comptage classes Bianchi ?")
print("="*78)
print("""
  K3 surface :
    χ(K3) = 24
    b_0 = b_4 = 1
    b_1 = b_3 = 0
    b_2 = 22

  Décomposition Hodge :
    h^{2,0} = h^{0,2} = 1 (forme symplectique holomorphe)
    h^{1,1} = 20
    Total h² = 22

  Lattice cohomologique :
    H²(K3, Z) = E8(-1)² ⊕ U⊕U⊕U
    rank = 16 + 6 = 22

  Picard lattice :
    Pic(K3) ⊂ H²(K3, Z) ⊂ H²(K3, C)
    rk Pic ∈ {1, 2, ..., 20}

  Si on ajoute la classe triviale [0] : 22 + 1 = 23 classes

  Cohérent avec /23 cluster CKM si SM = K3 (ou variété analogue)
""")

print("\n" + "="*78)
print("TEST 7 : ζ_H²(s) factorization sur primes apparents")
print("="*78)
primes_found = {23: 0, 13: 0, 15: 0, 27: 0, 11: 0, 17: 0, 19: 0}
for name, val in SM.items():
    for q in [13, 15, 23, 27, 11, 17, 19, 7]:
        for p in range(1, 5*q+1):
            if gcd(p, q) == 1:
                if abs(p/q - val)/val < 0.005:
                    if q in primes_found:
                        primes_found[q] += 1
                    break

print(f"Comptage des observables par dénominateur (<0.5%) :")
for q, count in sorted(primes_found.items(), key=lambda x: -x[1]):
    print(f"  q={q:2d} : {count} observables")

# Identifier conjecture : ζ_H²(s) = ζ_{K3}(s) ?
# Sur K3 : ζ_K3(s) = ζ(s)·ζ(s-1)²² · ζ(s-2)
print("""
  Hypothèse perfectoid : ζ_H²(s) = ζ_K3(s)
    K3 → ζ_K3(s) = ζ(s)·L_K3(s)·ζ(s-2)
    où L_K3(s) = L de la variété K3 à représentation 22-dim

  Valeurs spéciales attendues :
    s=1 : pôle de ζ → divergence dim_H²
    s=2 : valeur ζ(2)=π²/6 → masses bosoniques
    s=3 : valeur ζ(3) → κ_∞ (CONFIRMÉ via κ_∞ = ζ(3)/√π)
    s=3/2 : valeur ζ(3/2) → masses fermions hypothèse
""")

print("\n" + "="*78)
print("TEST 8 : √π = √(b_4) = √(self-intersection of K3) ?")
print("="*78)
print(f"  Self-intersection point class on K3 = 1")
print(f"  Top intersection [K3] · [K3] = 24 (Euler)")
print(f"  But √π is transcendental, no K3 link direct")
print(f"  Possible link via Riemann-Roch on K3 :")
print(f"    χ(L) = 1 + L²/2 + 1 = 2 + L²/2")
print(f"    → for L² = 0: χ = 2, but √π in normalization Gaussienne")
print()
# Could ζ(3) factor in K3 Atiyah-Singer ?
print("  ζ(3) connexion : Apéry constant, apparaît dans :")
print("    - Beilinson's K-theory of K3 surfaces")
print("    - L(K3, 3) = ζ(3)·F(K3) ?")
print("    - K-theoretic invariants of K3 modular forms")
print()
print("  ⟹ Hypothèse : K3 + ζ(3) + Beilinson regulator donne κ_∞")
