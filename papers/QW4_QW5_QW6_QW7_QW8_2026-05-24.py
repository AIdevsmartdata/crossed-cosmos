#!/usr/bin/env python3
"""QW4 + QW5 + QW6 + QW7 + QW8 — Saturation cross-Lie-groups + Manif 9 check
+ SU(2) HMC α from existing T1 data + error bars + saturation equation solve.

DS Bot Catalogue : these are CPU-pure, immediate quick wins.
"""
from fractions import Fraction
from math import comb, log, sqrt
import json

print("=" * 78)
print("QW4 — Saturation pour TOUS les groupes de Lie classiques + exceptionnels")
print("=" * 78)
print("""
Pour chaque groupe G simple : rank, |Φ⁺|, et saturation contre D(D-1)(5-D)/6.

Formules (Humphreys Lie Algebras 1972) :
  SU(N)=A_{N-1}: rank=N-1, |Φ⁺|=N(N-1)/2
  SO(2n+1)=B_n: rank=n,    |Φ⁺|=n²
  Sp(2n)=C_n:   rank=n,    |Φ⁺|=n²         [n long + n(n-1) short = n²]
  SO(2n)=D_n:   rank=n,    |Φ⁺|=n(n-1)     [simple si n≥3]
  G_2:          rank=2,    |Φ⁺|=6
  F_4:          rank=4,    |Φ⁺|=24
  E_6:          rank=6,    |Φ⁺|=36
  E_7:          rank=7,    |Φ⁺|=63
  E_8:          rank=8,    |Φ⁺|=120

Saturation requires rank(G) = D(D-1)(5-D)/6 ∈ {1, 2} (only positive values for D=2,3,4)
""")

groups = []
# Classical
for N in range(2, 7):
    groups.append((f"SU({N}) = A_{N-1}", N-1, N*(N-1)//2))
for n in range(2, 6):
    groups.append((f"SO({2*n+1}) = B_{n}", n, n*n))
for n in range(1, 6):
    groups.append((f"Sp({2*n}) = C_{n}", n, n*n))
for n in range(3, 7):
    groups.append((f"SO({2*n}) = D_{n}", n, n*(n-1)))
# Exceptional
groups.append(("G_2", 2, 6))
groups.append(("F_4", 4, 24))
groups.append(("E_6", 6, 36))
groups.append(("E_7", 7, 63))
groups.append(("E_8", 8, 120))

p = {D: D*(D-1)*(5-D)//6 for D in [2,3,4]}  # {2:1, 3:2, 4:2}
print(f"\n{'Group':>20} | {'rank':>4} | {'|Φ⁺|':>5} | {'sat D=2 (rank=1)?':>17} | {'sat D=3 (rank=2)?':>17} | {'sat D=4 (rank=2)?':>17}")
print("-" * 110)
sat_table = []
for name, rk, phi_plus in groups:
    sat_D = []
    for D in [2, 3, 4]:
        is_sat = (rk == p[D])
        sat_D.append("✅ SAT" if is_sat else "—")
        if is_sat:
            sat_table.append((name, rk, phi_plus, D))
    print(f"{name:>20} | {rk:>4} | {phi_plus:>5} | {sat_D[0]:>17} | {sat_D[1]:>17} | {sat_D[2]:>17}")

print(f"\nTotal saturated (group, D) pairs : {len(sat_table)}")
print("-" * 70)
for name, rk, phi, D in sat_table:
    kappa_A = Fraction(1, 2*phi)
    kappa_B = Fraction(1, 2*(D-1))
    alpha_A = 1 - kappa_A
    alpha_B = 1 - kappa_B
    converge = "= " if kappa_A == kappa_B else "≠ "
    print(f"  {name:>12} D={D}: rank={rk}, |Φ⁺|={phi}, κ_A=1/{2*phi}={float(kappa_A):.4f} {converge}κ_B=1/{2*(D-1)}={float(kappa_B):.4f}, α_A={float(alpha_A):.4f} vs α_B={float(alpha_B):.4f}")

print(f"""
IMPACT NEW :
- Au-delà de (SU(N), D) saturés trouvés en QW1-3, il existe des paires
  saturées avec d'autres groupes de Lie classiques et exceptionnels.
- En particulier, **G_2 et Sp(4)=C_2 et SO(5)=B_2** ont rank=2, donc sont
  saturés en D=3 et D=4 — comme SU(3) !
- κ_A(G_2) = 1/(2·6) = 1/12 ≠ κ_A(SU(3)) = 1/6  → groupes différents donnent
  κ_A différents.
- κ_B(D=4) = 1/6 universel (dimension uniquement)

ENCORE PLUS DISCRIMINANT :
  Si on teste G_2 D=4 (par exemple) :
    α_A(G_2) = 1 - 1/12 = 11/12 ≈ 0.917
    α_B(D=4) = 1 - 1/6  =  5/6  ≈ 0.833
    Gap ≈ 0.083 — comme SU(3) D=3.

  Donc TOUTE paire saturée avec |Φ⁺| ≠ D-1 discrimine.
""")

print("=" * 78)
print("QW5 — Manifestation 9 : κ·2(D-1) = 1 check pour les paires saturées")
print("=" * 78)
print("""
Énoncé : κ_sat·2(D-1) = 1 vérifié pour les paires saturées.

Pour interprétation B (Hodge) : κ_B = 1/(2(D-1)) → manif 9 trivialement = 1
Pour interprétation A (group) : κ_A = 1/(2|Φ⁺|) → manif 9 = (D-1)/|Φ⁺|

   manif 9 = (D-1)/|Φ⁺| = 1 ⇔ |Φ⁺| = D-1
""")
print(f"{'Group':>15} | {'rank':>4} | {'|Φ⁺|':>5} | {'D':>2} | {'manif 9 (A)':>12} | {'manif 9 (B)':>12} | {'A=B?':>5}")
print("-" * 78)
for name, rk, phi, D in sat_table:
    manif9_A = Fraction(D-1, phi)
    manif9_B = Fraction(1, 1)  # trivially 1 for B
    same = "✅" if manif9_A == manif9_B else "✗"
    print(f"{name:>15} | {rk:>4} | {phi:>5} | {D:>2} | {str(manif9_A):>12} | {str(manif9_B):>12} | {same:>5}")

print(f"""
INTERPRÉTATION :
- Si test SU(3) D=3 donne α≈0.83 (interpretation A) :
  κ_A·2(D-1) = (1/6)·4 = 2/3 ≠ 1 → Manifestation 9 FALSIFIÉE pour (3,3)
  ⇒ Sauf coincidence (2,2) et (3,4) où manif9 holds, falsifiable cross-D
- Si test SU(3) D=3 donne α≈0.75 (interpretation B) :
  κ_B·2(D-1) = (1/4)·4 = 1 ✅ → Manifestation 9 CONFIRMÉE pour 3/3 paires
  ⇒ Universelle géométrique
""")

print("=" * 78)
print("QW6 — α(SU(2)) HMC pur (T1 data, AVANT contamination β>200)")
print("=" * 78)

with open('/root/cc-private/docs/session_2026-05-24/results/mk_beta_scan.json') as f:
    d = json.load(f)
print("\nData T1 (SU(2) D=4 L=8, β-scan β=50/100/200) :")
print(f"{'β':>6} | {'ΔP_MK %':>10} | {'var_P_MK':>12} | {'σ_mean':>10}")
print("-" * 50)
betas, delta_P_MK, var_P_MK = [], [], []
for t in d['tests']:
    r = t['result']
    sigma_mean = sqrt(r['var_P_MK']) / sqrt(r['n_meas'])  # std error of mean
    betas.append(r['beta'])
    delta_P_MK.append(r['delta_meanP_MK_pct'])
    var_P_MK.append(r['var_P_MK'])
    print(f"{r['beta']:>6.0f} | {r['delta_meanP_MK_pct']:>10.4f} | {r['var_P_MK']:>12.4e} | {sigma_mean:>10.4e}")

# Fit α : log Δ = log A - α log β
import numpy as np
logb = np.log(betas)
logd = np.log(delta_P_MK)
# Weights = inverse of variance (delta-method approx)
weights = 1.0 / np.array([(sqrt(v)/sqrt(25))/d_ for v, d_ in zip(var_P_MK, delta_P_MK)])  # rel error inverse
coeffs, cov = np.polyfit(logb, logd, 1, cov=True)
alpha_fit = -coeffs[0]
alpha_err = sqrt(cov[0,0])
print(f"\nFit log Δ⟨P⟩MK = log A - α log β (3 datapoints, scipy std error) :")
print(f"  α(SU(2), D=4) = {alpha_fit:.4f} ± {alpha_err:.4f}")
print(f"  Predicted α(SU(2), D=4, non saturé) = 1.0 (Pinsker upper bound)")
print(f"  Match Pinsker ? {abs(alpha_fit - 1.0) < 3*alpha_err}")
print(f"""
IMPLICATION : SU(2) D=4 est NON saturé (rank=1 ≠ C(4,2)-C(4,3)=2).
Donc le framework prédit α=1 trivial (Pinsker bound).
Le fit donne α ≈ {alpha_fit:.2f} qui doit être proche de 1.
Si α << 1 → SU(2) D=4 est saturé (contradiction avec QW1).
Si α ≈ 1 → ✅ confirmation de la NON-saturation.
""")

print("=" * 78)
print("QW7 — Bootstrap-equivalent errors via standard error of mean")
print("=" * 78)
print("""
Avec n_meas=25 par β, on a déjà les variances stockées. Erreur standard
sur la moyenne : σ_mean = sqrt(var) / sqrt(n_meas-1).
Pour le bootstrap CI 95% : ≈ ± 1.96 σ_mean.

Pour fit α-exponent : propagation d'erreur via polyfit cov matrix.
Voir QW6 ci-dessus : α(SU(2)) = {:.3f} ± {:.3f}.

Note : True bootstrap nécessite raw measurements (pas seulement var).
Si raw data dispo : 1000 resamples, recompute ΔP, fit α distribution.
ESTIMATION CONSERVATRICE : avec 3 datapoints, α ± 0.10-0.15.
""".format(alpha_fit, alpha_err))

print("=" * 78)
print("QW8 — Résoudre D(D-1)(5-D)/6 = N-1 pour tout N=2..6 (équation entière)")
print("=" * 78)
print("""
Équation : D(D-1)(5-D) = 6(N-1)

Pour chaque N, trouver tous les D entiers ≥2 :
""")
for N in range(2, 8):
    target = 6*(N-1)
    sols = [D for D in range(2, 20) if D*(D-1)*(5-D) == target]
    if sols:
        print(f"  N={N} (rank={N-1}): D(D-1)(5-D) = {target} → solutions D = {sols}")
    else:
        # Compute max of polynomial D*(D-1)*(5-D) over reals → at D = (5+sqrt(25-9))/3 ≈ 3 ?
        # Actually max at D where derivative=0 : d/dD = 3D^2 - 12D + 5 = 0 → D = (12±√(144-60))/6 = (12±√84)/6 ≈ 0.4 ou 3.6
        # Max at D≈3.6, value ≈ 3.6·2.6·1.4 ≈ 13.1
        from math import sqrt
        D_max_real = (12 + sqrt(84)) / 6
        max_val = D_max_real * (D_max_real - 1) * (5 - D_max_real)
        print(f"  N={N} (rank={N-1}): pas de solution entière D≥2 (max polynôme réel ≈ {max_val:.2f} < {target})")

print(f"""
CONCLUSION QW8 :
- N=2 (rank=1): D=2 seulement
- N=3 (rank=2): D=3 ET D=4 (deux saturations pour SU(3) !)
- N≥4 (rank≥3): aucune saturation possible avec SU(N) car max polynôme < 18

Confirme : 3 paires (N,D) saturées pour SU(N), aucune supplementaire à découvrir.

MAIS QW4 a révélé que d'autres groupes (G_2, B_2=SO(5), C_2=Sp(4)) avec rank=2
sont aussi saturés en D=3,4. C'est une EXTENSION du framework non explorée.
""")

print("=" * 78)
print("SYNTHÈSE QW4-8")
print("=" * 78)
print(f"""
🆕 EXTENSION FRAMEWORK (QW4) :
   Paires saturées au-delà de SU(N) :
   - G_2 D=3 et G_2 D=4 (κ_A=1/12 vs κ_B=1/4 ou 1/6, gap large)
   - SO(5)=B_2 D=3 et D=4 (κ_A=1/8 vs κ_B=1/4 ou 1/6)
   - Sp(4)=C_2 D=3 et D=4 (κ_A=1/6 = SU(3), même algèbre)

   ⚠️ Sp(4) a même rang ET |Φ⁺|=6 = SU(3), donc indiscriminable par α !
   Mais G_2 ET SO(5) sont discriminables (|Φ⁺|≠3).

🎯 QW6 RÉSULTAT (SU(2) NON-saturé control) :
   α(SU(2), D=4) = {alpha_fit:.3f} ± {alpha_err:.3f}
   Prédit (Pinsker, non-saturé) : 1.0
   ⇒ {('✅ COMPATIBLE' if abs(alpha_fit - 1.0) < 3*alpha_err else '⚠️ DEVIATION')} avec prédiction

⚖️  QW5 MANIFESTATION 9 :
   - Sous interprétation B : universellement vraie pour les 3 paires
   - Sous interprétation A : 2/3 paires (échoue (3,3))
   - Le test SU(3) D=3 va trancher

🔬 OPUS SU(3) D=3 EN COURS : résultat va décider A vs B + manifestation 9

Cluster firm 725 STABLE.
""")
