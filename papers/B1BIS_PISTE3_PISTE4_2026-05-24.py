#!/usr/bin/env python3
"""B1bis Piste 3 (κ ↔ Betti) + Piste 4 (Morse-Bott Casimir T^D).

Calculs concrets demandés par DS Bot pour ancrer κ=1/6 dans :
  - Piste 3 : κ = 1/b_{D/2}(T^D) pour D pair saturé
  - Piste 4 : κ = ratio Casimir / dim modes transverses YM sur T^D
"""
from fractions import Fraction
from math import comb

print("="*72)
print("B1bis PISTE 3 — κ ↔ b_{D/2}(T^D) pour D pair saturé")
print("="*72)
print("""
Hypothèse DS Bot : κ_sat = 1/b_{D/2}(T^D) pour D pair.
Betti de T^D : b_k(T^D) = C(D, k).
Donc b_{D/2}(T^D) = C(D, D/2).
""")

print(f"{'D':>3} | {'b_{D/2}(T^D)':>12} | {'2(D-1)':>8} | {'κ=1/(2(D-1))':>14} | {'κ=1/b_{D/2}':>12} | {'Match?':>7}")
print("-"*72)
for D in [2, 4, 6, 8]:
    if D % 2 == 1: continue
    b_D2 = comb(D, D//2)
    twoDm1 = 2*(D-1)
    kappa_formula = Fraction(1, twoDm1)
    kappa_betti = Fraction(1, b_D2)
    match = "✅" if kappa_formula == kappa_betti else "❌"
    print(f"{D:>3} | {b_D2:>12} | {twoDm1:>8} | {str(kappa_formula):>14} | {str(kappa_betti):>12} | {match:>7}")

print(f"""
CONCLUSION Piste 3 :
- D=2 : 2(D-1) = 2 = C(2,1) ✅ (b_1(T²) = 2)
- D=4 : 2(D-1) = 6 = C(4,2) ✅ (b_2(T⁴) = 6) ← interprétation Hodge
- D=6 : 2(D-1) = 10 ≠ C(6,3) = 20 ❌
- D=8 : 2(D-1) = 14 ≠ C(8,4) = 70 ❌

Donc κ = 1/b_{{D/2}}(T^D) COÏNCIDE avec 1/(2(D-1)) UNIQUEMENT pour D=2,4.
Puisque D≥5 n'a pas de saturation (polynôme 5-D ≤ 0), la coïncidence n'a pas de
contre-exemple dans le domaine de validité.

INTERPRÉTATION pour pitch :
  Pour D=4 (cas physique Clay) : κ = 1/b_2(T⁴) — DIRECTEMENT lié à la
  topologie spacetime (Hodge decomposition).
  Pour D=2 : κ = 1/b_1(T²) — analogue 1-forme.
  Cette identification est PROPRE à D ∈ {{2,4}} (paires saturées avec D pair).
""")

print("="*72)
print("B1bis PISTE 4 — Morse-Bott Casimir T^D modes transverses YM")
print("="*72)
print("""
Setup : pure YM SU(N) sur T^D = R^D/ℤ^D. Modes de Fourier :
  A_μ(x) = Σ_{k ∈ 2π·ℤ^D / L} A_μ(k) e^{ik·x}, k = (k_1, ..., k_D), k_μ ∈ 2π·ℤ/L

Action quadratique :
  S_quad = Σ_k A_μ(k) (k² δ_μν - k_μ k_ν) A_ν(-k) / (2g²)

Décomposition modes par k :
  - k ≠ 0 : (D-1) modes transverses physiques (k²) + 1 mode longitudinal (jauge)
  - k = 0 : tous les D modes sont zero → modes plats / espace des modules
""")

print(f"{'D':>3} | {'N':>3} | {'dim(SU(N))':>11} | {'(D-1)':>6} | {'modes/k':>8} | {'modes/k/(D-1)':>14} | {'κ predicted':>12}")
print("-"*72)
for D, N in [(2,2), (3,3), (4,3), (4,2), (4,4)]:
    dim_G = N**2 - 1
    modes_per_k = (D-1) * dim_G
    modes_per_dir = modes_per_k  # total transverse modes per momentum
    kappa_candidate1 = Fraction(1, modes_per_k) if modes_per_k > 0 else Fraction(0)
    sat = "SAT" if (N-1 == (D*(D-1)*(5-D)) // 6) else "non"
    print(f"{D:>3} | {N:>3} | {dim_G:>11} | {D-1:>6} | {modes_per_k:>8} | {modes_per_k/(D-1):>14.2f} | {str(kappa_candidate1):>12} ({sat})")

print(f"""
ANALYSE Piste 4 :
- SU(3) D=4 saturé : modes/k = 3·8 = 24 → κ candidate = 1/24 ❌ (vrai κ = 1/6)
- SU(3) D=3 saturé : modes/k = 2·8 = 16 → κ candidate = 1/16 ❌ (vrai κ = 1/4)
- SU(2) D=2 saturé : modes/k = 1·3 = 3 → κ candidate = 1/3 ❌ (vrai κ = 1/2)

κ ≠ 1/(modes total). Trop simple.

ALTERNATIVE : κ = ratio (Hodge auto-dual modes) / (modes totaux) ?
Pour D=4 : b_2^+ = 3 / b_2 = 6 = 1/2 → κ = 1/2 ❌

ALTERNATIVE 2 : κ = (rank de G) / (modes transverses par direction) ?
Pour SU(3) D=4 saturé : 2 / 24 = 1/12 ❌

ALTERNATIVE 3 (la BONNE) : κ_sat = (1/2) · (rank/|Φ|)
- SU(3) D=4 : (1/2) · (2/6) = 1/6 ✅
- SU(2) D=2 : (1/2) · (1/2) = 1/4 ❌ (vrai = 1/2)
- SU(3) D=3 : (1/2) · (2/6) = 1/6 ❌ (vrai = 1/4)

Donc même cette formule (présente dans KappaOneSixth.lean pour SU(3) D=4)
NE GÉNÉRALISE PAS à toutes les paires saturées. Le κ_sat varie avec (N,D)
pour chaque paire saturée.

ALTERNATIVE 4 : κ_sat = (1/2) · (1/(D-1)) ?
- D=2 : (1/2)·1 = 1/2 ✅
- D=3 : (1/2)·(1/2) = 1/4 ✅
- D=4 : (1/2)·(1/3) = 1/6 ✅

OUI !! κ_sat(D) = 1/(2(D-1)) qui se REFORMULE comme :
  κ_sat = (1/2) × (1/(D-1))

où le facteur (1/2) vient de la dualité de Hodge (auto-dual vs anti-auto-dual)
et (D-1) vient des modes transverses par direction.

INTERPRÉTATION FINALE :
  κ_sat = (1/2) · (1/modes_transverses_par_direction)

  où modes_transverses_par_direction = D-1 pour pure YM sur T^D.

C'est cohérent avec la dimension d'un photon polarisation transverse en D=4 = 2,
mais ici on a (D-1) modes par direction pour un gluon (sans masse).

Le facteur 1/2 = b_+^2 / b_2 = 1/2 vient de la SELF-DUALITY en D=4 spécifiquement,
mais pour D≠4 il faut une autre interprétation (parité auto-dual/anti-auto-dual
disponible seulement en D=4·k).

Pour D=2,3 le facteur 1/2 doit venir d'une AUTRE source :
- D=2 : 1/2 = 1/dim(Harm^0(T²)) où Harm^0 = ℝ (constantes)? Pas clair.
- D=3 : 1/2 = ?

Donc la formule κ = 1/(2(D-1)) tient empiriquement sur les 3 paires saturées
mais l'interprétation MORSE-BOTT CASIMIR ne donne pas le facteur 1/2 directement.
""")

print("="*72)
print("VERDICT GLOBAL B1bis Piste 3+4")
print("="*72)
print("""
✅ Piste 3 (Hodge Betti) :
   - κ = 1/b_2(T⁴) ✅ ancrage topologique D=4 PROPRE et solide
   - Mais : généralisation à D général ne tient pas (b_{D/2} ≠ 2(D-1) sauf D=2,4)
   - DEJA DANS KappaOneSixth.lean comme route Hodge

🟡 Piste 4 (Morse-Bott Casimir) :
   - Modes transverses (D-1)·dim(G) par moment k
   - κ_sat = 1/(2(D-1)) reformulé : (1/2) · (1/(D-1))
   - Le facteur 1/2 = Hodge self-duality SPÉCIFIQUE D=4
   - Pour D=2,3 le facteur 1/2 vient d'autre chose (à clarifier)
   - PAS de bridge propre vers κ_sat universel

🔴 Conclusion honnête :
   Les pistes 3 et 4 ne donnent PAS de bridge unifié vers κ_sat universel
   couvrant les 3 paires saturées. La formule κ = 1/(2(D-1)) reste
   un FAIT empirique structurellement vérifié par Manifestation 9, mais
   sa DÉRIVATION universelle (cross-D=2,3,4) nécessite probablement les
   pistes 1 (Dirac index) ou 5 (Ricci A/G) — plus longues (semaines-mois).

ACTION RECOMMANDÉE :
  Garder pour le pitch Bauerschmidt la formulation :
  "κ_sat(D) = 1/(2(D-1)) is empirically verified for the 3 saturated pairs
   and topologically interpreted as 1/b_{D/2}(T^D) for D=4 specifically.
   A unified derivation across saturated pairs remains open."

  Pour pousser plus loin : nécessite Opus dedicated sur Piste 1 ou Piste 5
  (Dirac index ou Ricci A/G) — dispatch séparé.
""")
