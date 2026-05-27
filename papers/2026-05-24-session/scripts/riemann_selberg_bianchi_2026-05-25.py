"""
TEST Kevin vision : Riemann zeros ↔ Selberg trace ↔ Class numbers ↔ Bianchi ↔ dim(G)
=====================================================================================
"""
import numpy as np
from math import log, exp, log10, pi, sqrt

# ==================================================================
# Riemann zeros (premiers 30, valeurs précises connues)
# ==================================================================
# Source : OEIS A002410 / LMFDB
RIEMANN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]

# Σ k premiers
def first_n_primes(n):
    primes = []; num = 2
    while len(primes) < n:
        if all(num % p != 0 for p in primes if p*p <= num):
            primes.append(num)
        num += 1
    return primes

print("="*78)
print("TEST 1 : Riemann zeros t_n vs Σ_k premiers — corrélation ?")
print("="*78)
print(f"\n  {'n':>3s}  {'t_n':>10s}  {'Σ_n':>5s}  {'ratio':>8s}  {'diff':>8s}")
for n in range(1, 16):
    t = RIEMANN_ZEROS[n-1]
    s = sum(first_n_primes(n))
    print(f"  {n:3d}  {t:10.3f}  {s:5d}  {t/s:8.4f}  {t-s:+8.2f}")
print(f"""
  Observation :
    t_n croît plus LENTEMENT que Σ_k premiers
    t_n ~ 2πn/log(n)        (Riemann-Mangoldt)
    Σ_k premiers ~ k²·log(k)/2  (Mertens approx)
    Pas correspondance directe numérique.
""")

# Cumulative check : avg ratio
ratios = [RIEMANN_ZEROS[i]/sum(first_n_primes(i+1)) for i in range(15)]
print(f"  Ratio moyen t_n/Σ_n (n=1..15) : {np.mean(ratios):.4f} ± {np.std(ratios):.4f}")

# ==================================================================
# TEST 2 : Class numbers h(d) pour Q(√-d)
# ==================================================================
print("\n" + "="*78)
print("TEST 2 : Class numbers h(d) pour discriminants imaginaires")
print("="*78)
# Table connue (Cohen, Davenport)
class_numbers = {
    3:1, 4:1, 7:1, 8:1, 11:1,
    15:2, 19:1, 20:2, 23:3, 24:2,
    31:3, 35:2, 39:4, 40:2, 43:1,
    47:5, 51:2, 52:2, 55:4, 56:4,
    59:3, 67:1, 68:4, 71:7, 79:5,
    83:3, 84:4, 87:6, 88:2, 91:2,
    95:8, 103:5, 104:6, 107:3, 111:8,
    115:2, 119:10, 120:4, 123:2, 127:5,
    131:5, 132:4, 136:4, 139:3, 143:10,
    151:7, 152:6, 155:4, 159:10, 160:4,
    163:1, 164:8, 167:11, 168:4, 179:5,
    180:4, 183:8, 184:4, 187:2, 191:13,
    195:4, 199:9, 203:4, 211:3, 212:6,
    219:4, 223:7, 227:5, 228:4, 231:12,
}

dim_targets = {3, 8, 14, 15, 21, 22, 24}  # physics dimensions
print(f"\n  Class numbers h(d) match dim(G_physics) ?")
matches_with_dim = []
for d, h in sorted(class_numbers.items()):
    if h in dim_targets:
        matches_with_dim.append((d, h))
        print(f"    d=-{d:3d} : h(d)={h} → dim physics candidate")

# Mostly h=1,2,3,4 — not matching gauge dim 8,14,21
print(f"""
  Observation :
    h(d) majoritairement petits (1-10) pour d ≤ 200
    Dim(G_physics) = 3, 8, 14, 15, 21, 22, 24 rarement atteints
    Heegner d ∈ {{1,2,3,7,11,19,43,67,163}} : h=1 (PCID)
    h(d) ne donne PAS directement dim(G).
""")

# Mais : k = dim(G) peut être paramètre, et class numbers = comptage multiplicité
# Selon Selberg : geodesic length l_γ = 2 arccosh(|tr(γ)|/2), multiplicity = h(disc)
# Pas correspondance directe Cl ↔ dim(G).

# ==================================================================
# TEST 3 : Euler product partial vs ECI scales
# ==================================================================
print("\n" + "="*78)
print("TEST 3 : Produit d'Euler partial vs scales ECI")
print("="*78)
# ζ(s) = ∏_p (1 - p^-s)^-1
# Pour les k premiers premiers, ζ_k(s) = ∏_{i=1..k} (1 - p_i^-s)^-1
# log ζ_k(s) = Σ_p log(1/(1-p^-s)) = Σ_p [p^-s + p^-2s/2 + ...]

# Pour s=1 (critical limit), ζ diverge mais ζ_k partial finit
# ζ_k(1) = ∏ p_i/(p_i - 1)

s_vals = [0.5, 1.0, 1.5, 2.0, 3.0]
print(f"\n  Compute ζ_k(s) partial Euler product for k=1..14")
print(f"  {'s':>4s}  {'ζ_8(s)':>10s}  {'ζ_14(s)':>10s}  {'log ζ_8(s)':>12s}  {'log ζ_14(s)':>12s}")
for s in s_vals:
    z_8 = 1.0; z_14 = 1.0
    for i, p in enumerate(first_n_primes(14)):
        if i < 8:
            z_8 *= 1 / (1 - p**(-s))
        z_14 *= 1 / (1 - p**(-s))
    print(f"  {s:4.1f}  {z_8:10.5f}  {z_14:10.5f}  {log(z_8):12.5f}  {log(z_14):12.5f}")

print(f"""
  Lien direct Σ premiers ↔ log ζ_k(s) :
    Σ premiers = Σ p_i             linéaire
    log ζ_k(s) = Σ -log(1-p_i^-s)  série exponentielle inverse

  Pour s grand, log ζ_k(s) → 0 rapidement
  Pour s→1, log ζ_k(s) → divergence

  → log ζ_k(s) ≠ Σ premiers directement
  → Lien manque : peut-être via residus, mais pas Σ première intuitive
""")

# ==================================================================
# TEST 4 : Sensibilité du choix k pour M_Pl, Λ
# ==================================================================
print("\n" + "="*78)
print("TEST 4 : choix k = dim(G) — quelle sensibilité ?")
print("="*78)
log_MPl2_v2 = 76.90
log_Lambda_M4 = -281.0

print(f"\n  Pour Hiérarchie ln(M_Pl²/v²) = {log_MPl2_v2:.2f} :")
for k in range(5, 12):
    s = sum(first_n_primes(k))
    err = abs(s - log_MPl2_v2)
    flag = "★" if err < 1 else ""
    print(f"    k={k}: Σ_k = {s:3d}, err = {err:.2f} {flag}")
print(f"  → k=8 (Σ=77) UNIQUE choix dans 1 unit")
print(f"  → k=8 = dim SU(3) QCD ★ correspond")

print(f"\n  Pour Λ ln(Λ/M_Pl⁴) = {log_Lambda_M4:.2f} :")
for k in range(10, 17):
    s = sum(first_n_primes(k))
    err = abs(s + log_Lambda_M4)
    flag = "★" if err < 1 else ""
    print(f"    k={k}: Σ_k = {s:3d}, err = {err:.2f} {flag}")
print(f"  → k=14 (Σ=281) UNIQUE choix dans 1 unit")
print(f"  → k=14 = dim G_2 dark ★ correspond")

# ==================================================================
# TEST 5 : Multivers générés par autres choix k
# ==================================================================
print("\n" + "="*78)
print("TEST 5 : 'Univers' alternatifs avec autres choix k")
print("="*78)

# Si on changeait QCD pour SU(N) different, on aurait dim(G_QCD)=N²-1
# Et M_Pl/v changerait
print(f"\n  Si QCD était SU(N) pour différent N :")
for N in range(2, 10):
    dim_N = N**2 - 1
    s_dim_N = sum(first_n_primes(dim_N)) if dim_N <= 25 else "huge"
    if dim_N <= 25:
        log_ratio = s_dim_N / 2  # Σ_k pred ln(M_Pl/v)
        M_Pl_pred_GeV = 246.22 * exp(log_ratio)
        log10_ratio = log_ratio / log(10)
        print(f"    N={N}: dim={dim_N:2d}, Σ_dim premiers={s_dim_N:4d}, M_Pl/v ≈ 10^{log10_ratio:.1f}, → M_Pl pred = {M_Pl_pred_GeV:.2e} GeV")

print(f"""
  ⟹ Notre univers (N=3, dim=8) → M_Pl/v ≈ 10^16.7 ← cohérent obs
     N=2 : dim=3, Σ_3=10  → M_Pl/v ≈ 10^2.2  (univers "léger")
     N=4 : dim=15, Σ_15=328 → M_Pl/v ≈ 10^71  (univers "ultra-lourd")
     N=5 : dim=24, Σ_24=963 → M_Pl/v ≈ 10^209 (univers "extrême")

  → Le choix N=3 (SU(3) QCD) est UNIQUE pour M_Pl/v ~ 10^17.
  → Si Nature avait choisi N=4, l'univers serait inconnaissable.
""")

# Pareil pour Λ avec G_dark
print(f"  Si G_dark était autre groupe (dim alternative) :")
for dim_d in [3, 7, 8, 14, 15, 24]:
    s = sum(first_n_primes(dim_d))
    pred_log10 = -s / log(10)
    print(f"    G_dark dim={dim_d:2d}: Σ_dim={s:3d}, Λ/M_Pl⁴ ≈ 10^{pred_log10:+.1f}")

print(f"""
  → Notre univers : dim=14 (G_2) → Λ ≈ 10^-122 ← cohérent obs
  → dim=3 (SU(2)) : Λ ≈ 10^-4 (énorme, univers inhabitable)
  → dim=24 (SU(5)) : Λ ≈ 10^-418 (univers presque sans énergie vide)
""")

# ==================================================================
# SUMMARY
# ==================================================================
print("\n" + "="*78)
print("BILAN HONNÊTE — vision Kevin Riemann/Selberg/Bianchi")
print("="*78)
print("""
  ✓ EMPIRIQUE confirmé :
    Pattern ln(X) = ±Σ_k premiers avec k=dim(G) marche pour
    Λ (k=14) et M_Pl²/v² (k=8). Choix k unique dans 1 unit.

  ✓ Univers paramétré par k :
    Si on change k = dim(G_QCD ou G_dark), on change l'échelle.
    Notre univers correspond à un choix précis : k_QCD=8, k_dark=14.

  ⚠ THÉORIQUE incomplet :
    Selberg trace formula relie zéros ζ à géodésiques modulaires,
    multiplicité h(d) class numbers.
    MAIS h(d) ≠ dim(G_physics) en numerique direct.
    Lien ζ-fonction K3 → Σ premiers reste conjecture.

  ✗ FALSIFIÉ direct :
    Riemann zeros t_n ≠ Σ_k premiers numériquement.
    Riemann zeros ne sont PAS l'instance directe des dim(G).

  ⟹ Vision Kevin = ÉLÉGANTE METAPHOR mais pas dérivation formelle.
     L'algorithme empirique reste valide.
     La PROOF rigoureuse nécessite foncteur spectral K3 (Opus voie).
""")
