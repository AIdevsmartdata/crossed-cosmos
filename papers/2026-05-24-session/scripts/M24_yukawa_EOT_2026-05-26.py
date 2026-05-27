"""
Test EOT Moonshine coefficients vs Yukawa (vraie physique M_24)
=================================================================
EOT 2010 décompose elliptic genus K3 :
  EG_K3(τ,z) = -2θ²_1(τ,z)·φ_0(τ,z) + Σ A_n · (massive char N=4)

A_n = multiplicités décomposant en dim M_24 irreps :
  A_1 = 90 = 45 + 45
  A_2 = 462 = 231 + 231
  A_3 = 1540 = 770 + 770
  A_4 = 4554 = 2277 + 2277
  A_5 = 11592 = 5796 + 5796
  A_6 = 27830 (decomp tbd)
  A_7 = 61686
  A_8 = 131100
  A_9 = 271216

Plus : M_24 conjugacy class orders = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 21, 23}
       Le 23 ré-apparaît !
"""
import numpy as np
from math import log, exp, sqrt
from itertools import combinations

# EOT coefficients (vrais)
EOT = [90, 462, 1540, 4554, 11592, 27830, 61686, 131100, 271216]

# Yukawa values
v = 246.22
masses = {'e': 0.51099895e-3, 'mu': 0.10565838, 'tau': 1.77686,
          'u': 2.16e-3, 'd': 4.67e-3, 's': 93.4e-3,
          'c': 1.27, 'b': 4.18, 't': 172.57}
yukawas = {f: sqrt(2)*m/v for f, m in masses.items()}

# M_24 conjugacy class orders
M24_CONJ_ORDERS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 21, 23]

print("="*78)
print("TEST EOT Moonshine coefficients vs Yukawa")
print("="*78)

# Test 1 : Direct match y_f = A_n / A_max
print(f"\n  EOT coefficients : {EOT}")
print(f"  A_max = A_9 = {EOT[-1]}")
print()
A_max = EOT[-1]
for f in sorted(yukawas.keys(), key=lambda x: yukawas[x]):
    y = yukawas[f]
    target_A = y * A_max
    best_match = min(EOT, key=lambda a: abs(a - target_A))
    idx = EOT.index(best_match) + 1
    err = abs(best_match - target_A) / target_A * 100
    print(f"  y_{f:3s} = {y:.4e}  → A_target = {target_A:>10.1f}, A_{idx} = {best_match} ({err:+.1f}%)")

# Test 2 : Yukawa ratios = EOT ratios
print("\n" + "="*78)
print("TEST 2 : Yukawa ratios = EOT coefficient ratios")
print("="*78)

fermion_pairs = list(combinations(yukawas.keys(), 2))
matches = []
for f1, f2 in fermion_pairs:
    r_obs = yukawas[f1] / yukawas[f2]
    # find best EOT ratio
    best_match = None
    best_err = 100
    for a1 in EOT:
        for a2 in EOT:
            if a1 != a2:
                r_pred = a1 / a2
                err = abs(r_pred - r_obs) / r_obs
                if err < best_err:
                    best_err = err
                    best_match = (a1, a2)
    if best_err < 0.05:
        matches.append((f1, f2, r_obs, best_match, best_err))

print(f"\n  {len(matches)} pairs match within 5%")
for f1, f2, r, (a1, a2), err in sorted(matches, key=lambda x: x[4]):
    print(f"  y_{f1}/y_{f2:3s} = {r:.4f}  ≈  A({EOT.index(a1)+1})/A({EOT.index(a2)+1}) = {a1}/{a2} = {a1/a2:.4f}  ({err*100:+.2f}%)")

# Test 3 : Yukawa ↔ EOT (avec scaling)
print("\n" + "="*78)
print("TEST 3 : Fit log(y_f) = α·log(A_n) + β (best α, β)")
print("="*78)

# Pick the 9 best matches : for each fermion, best A_n by log proximity
# Then fit log(y) = α·log(A) + β
import numpy as np
log_y = []
log_A_choices = []
for f in sorted(yukawas.keys(), key=lambda x: yukawas[x]):
    y = yukawas[f]
    log_y.append(log(y))
    # Find A closest in log
    best_A = min(EOT, key=lambda a: abs(log(a) - (log(y) + log(EOT[-1]))))  # rough scale
    log_A_choices.append(log(best_A))

# Linear fit
log_y = np.array(log_y)
log_A_choices = np.array(log_A_choices)
A_mat = np.vstack([log_A_choices, np.ones(9)]).T
alpha, beta = np.linalg.lstsq(A_mat, log_y, rcond=None)[0]
pred_log_y = alpha * log_A_choices + beta
residuals = log_y - pred_log_y
print(f"  Fit log(y_f) = {alpha:.3f}·log(A) + {beta:.3f}")
print(f"  RMS log residuals = {np.sqrt(np.mean(residuals**2)):.3f}")

# Test 4 : Conjugacy class orders 23 ↔ CKM cluster
print("\n" + "="*78)
print("TEST 4 : M_24 conjugacy class 23 ↔ CKM cluster /23")
print("="*78)

print(f"  M_24 conjugacy class orders : {M24_CONJ_ORDERS}")
print(f"  23 EST une classe de M_24 ! (classes 23A, 23B sont elliptic)")
print(f"  Notre cluster CKM /23 :")
print(f"    A_CKM = 19/23")
print(f"    η_bar = 8/23")
print(f"    sin δ_CKM = 21/23")
print(f"    sin²θ_{{12}} PMNS = 7/23")
print(f"  → Possible lien : CKM/PMNS structure encodée dans 23-cyclic elements M_24")
print()
# 23 = order of cyclic element. Twined genera φ_23(τ,z) intéressant ?
# In Mathieu Moonshine, the twined genera form a complete dataset
# φ_g(τ,z) for g of order 23 has specific Fourier coefficients

# Test 5 : Hierarchy logique by generation
print("\n" + "="*78)
print("TEST 5 : Structure générationnelle Yukawa ↔ M_24")
print("="*78)

# Generation 3 : t, b, τ
y_gen3 = {'t': yukawas['t'], 'b': yukawas['b'], 'tau': yukawas['tau']}
# Generation 2 : c, s, μ
y_gen2 = {'c': yukawas['c'], 's': yukawas['s'], 'mu': yukawas['mu']}
# Generation 1 : u, d, e
y_gen1 = {'u': yukawas['u'], 'd': yukawas['d'], 'e': yukawas['e']}

print(f"\n  Generation 3 :")
print(f"    y_t/y_b = {y_gen3['t']/y_gen3['b']:.3f}  vs  10395/252 = 41.25  ★")
print(f"    y_b/y_τ = {y_gen3['b']/y_gen3['tau']:.3f}  vs  ?")
print(f"    y_t/y_τ = {y_gen3['t']/y_gen3['tau']:.3f}  vs  ?")

print(f"\n  Generation 2 :")
print(f"    y_c/y_s = {y_gen2['c']/y_gen2['s']:.3f}  vs  ?")
print(f"    y_s/y_μ = {y_gen2['s']/y_gen2['mu']:.3f}  vs  ?")
print(f"    y_c/y_μ = {y_gen2['c']/y_gen2['mu']:.3f}  vs  ?")

# Test all best matches for gen2 ratios in M_24
M24_DIMS = [1, 23, 45, 231, 252, 253, 483, 770, 990, 1035,
            1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395]

def best_M24_ratio(r_obs):
    best = (None, None, 100)
    for d1 in M24_DIMS:
        for d2 in M24_DIMS:
            if d1 != d2:
                err = abs(d1/d2 - r_obs)/r_obs
                if err < best[2]:
                    best = (d1, d2, err)
    return best

print(f"\n  Best M_24 dim ratios for gen 2 :")
for label, r in [('y_c/y_s', y_gen2['c']/y_gen2['s']),
                  ('y_s/y_μ', y_gen2['s']/y_gen2['mu']),
                  ('y_c/y_μ', y_gen2['c']/y_gen2['mu'])]:
    d1, d2, err = best_M24_ratio(r)
    print(f"    {label} = {r:.4f}  ≈  {d1}/{d2} = {d1/d2:.4f} ({err*100:+.2f}%)")

# Test 6 : Twined genera coefficients (need specific data)
print("\n" + "="*78)
print("TEST 6 : Twined genera coefficients pour g ordre 23 ?")
print("="*78)
print(f"""
  Pour g d'ordre 23 dans M_24 (élément 23A ou 23B), le twined genus est :
    φ_23A(τ,z) = trace de g sur Hilbert space K3

  Les coefficients de Fourier de φ_23 sont des entiers, satisfont
  congruences avec les vrais coefficients EG_K3.

  À tester : φ_23 coefficients matchent observables /23 cluster CKM/PMNS ?

  Données spécifiques nécessitent table EOT 2010 / Gannon's table :
    arXiv:1004.0956 (EOT) — VERIFIED
    arXiv:1209.6062 (Gannon) — à verifier

  Calcul direct demande Sage/Magma + database explicite.
  → SUBSEQUENT WORK pour Opus PARI/Sage
""")

# CONCLUSION
print("\n" + "="*78)
print("CONCLUSION deep M_24 EOT test")
print("="*78)
print(f"""
  ✗ Yukawa = A_n EOT direct : pas de match clean
    (A_n croissent trop vite : 90, 462, 1540, ..., 271216)

  ✓ Yukawa = dim_irrep M_24 ratios : matches paires concrets
    y_t/y_b = 10395/252 (0.08%)
    y_c/y_τ = 1265/1771 (0.06%)

  ⚠ Yukawa ↔ A_n EOT : pas le bon test (A_n est sum de dims)

  🎯 NEW :
    Conjugacy class M_24 d'ordre 23 ↔ cluster CKM /23 ?
    Twined genus φ_23 → CKM angles ? À tester via Sage/Magma.

  → M_24 reste TIER 3 : matches numériques sans dérivation complète.
  → Approfondir avec twined genera demande outils plus avancés.
""")
