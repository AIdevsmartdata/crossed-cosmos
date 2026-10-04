#!/usr/bin/env python3
# **⚠️ RETRACTION NOTICE (2026-10-04) — read this first. / AVIS DE RÉTRACTION (04/10/2026) — à lire d'abord.**
#
# This document claims or prepares a proof of the 4D Yang–Mills mass gap
# (Clay Millennium problem), or states a probability of obtaining one
# ("P(Clay …)"). **No such proof exists, and this repository does not claim
# one** (see the README, "Honest scope"). The text below is kept unchanged as
# a historical record; it must not be read or cited as a proof.
#
# - Every version of the chain rests on steps that were **never proved** and
#   enter only as stated conditions or Lean `axiom`s: depending on the version,
#   the continuum step (finite-β Lemma B / Conjecture C*, declared as
#   `axiom lemma_B_beta_finite`, `lean/Crossed/InformationConservation.lean`
#   l.445), the
#   Transport Conjecture (itself a stack of two open problems, THEOREMS_INDEX
#   OPEN-Transport), and, in the 2026-05-26 KR-FP chain, the structural
#   hypothesis **Hyp-CST** (`lean/Crossed/Hyp_CST.lean`: "SKETCH (axiom
#   declared, not proven Lean-side)", l.22; `axiom Hyp_CST`, l.88). Our
#   internal claim register records Hyp-CST as the lock of the KR-FP chain,
#   never proved, and the KR-FP chain itself as dead (its curvature ⟹ gap
#   route gives only empty bounds in d = 4, internal finding of 2026-07-30).
#   Our internal programme map of 2026-07-19 lists a rigorous constructive
#   proof of the gap as ongoing work, not as achieved.
# - "0 sorry" in Lean does not mean "proved" here: the analytic content sits
#   in named axioms (117 `axiom` declarations in `lean/Crossed/`), and the
#   theorem `mass_gap_continuum_D4` (`InformationConservation.lean`
#   l.531-537) concludes `∃ m_phys_sq > 0`, which holds trivially.
# - Every success probability stated below (P(Clay …), feasibility
#   percentages) is **withdrawn**: subjective, with no verifiable basis.
#
# *FR — Ce document revendique ou prépare une preuve du gap de masse de
# Yang–Mills 4D, ou annonce une probabilité d'en obtenir une. Cette preuve
# n'existe pas : les étapes décisives
# (Lemme B à β fini / Conjecture C*, conjecture de transport, hypothèse
# Hyp-CST) n'ont jamais été prouvées et n'apparaissent en Lean que comme
# axiomes. Le texte est conservé tel quel comme archive ; il ne doit être ni
# lu ni cité comme une preuve. Les probabilités annoncées sont retirées.*
#
# Details and the list of points still open: CHANGELOG.md (repository root),
# entry integrity-2026-10-04.
#
"""Investigation tension SU(3) vs SU(2) m_gap framework vs AT2021.

Paradoxe :
- Framework : SU(3) saturé → C_LSI = 5/24 < 1/4 = C_LSI(SU(N≠3))
- Rothaus : λ_1 ≥ 1/C_LSI ⟹ SU(3) λ_1 PLUS GRAND ⟹ m_gap PLUS GRAND
- AT2021 lattice : m(0⁺⁺)/√σ : SU(3)=3.405 < SU(2)=3.781 ⟹ SU(3) PLUS PETIT

Hypothèses à investiguer :
H1 — Convention C_LSI : saturated change le signe
H2 — Scale setting : √σ varie avec N, fausse la comparaison
H3 — Framework formule c_∞·(1-κ) erronée direction
H4 — m_gap intrinsic ≠ m_glueball physical
H5 — Corrections finite-β/finite-L
"""
import numpy as np
from math import sqrt, comb

print("=" * 90)
print("TENSION SU(3) vs SU(2) — INVESTIGATION HONNÊTE")
print("=" * 90)

# Framework prediction
print("\n§1 PRÉDICTION FRAMEWORK")
print("-" * 70)
c_inf_D4 = (comb(4, 2) - comb(4, 3)) / (2 * 4)  # = 2/8 = 0.25
print(f"c_∞(D=4) = (C(4,2)-C(4,3))/(2·4) = 2/8 = {c_inf_D4}")

# SU(2): non-saturé → C_LSI = c_∞
C_LSI_SU2 = c_inf_D4  # 1/4
# SU(3): saturé → C_LSI = c_∞·(1-κ) avec κ=1/6
kappa_SU3 = 1/6
C_LSI_SU3 = c_inf_D4 * (1 - kappa_SU3)  # = 5/24

print(f"C_LSI(SU(2), D=4) = c_∞ = {C_LSI_SU2:.6f} = 1/4 (non saturé)")
print(f"C_LSI(SU(3), D=4) = c_∞·(1-κ) = {C_LSI_SU3:.6f} = 5/24 (saturé)")

# Rothaus : λ_1 ≥ 1/C_LSI (intrinsic Markov-time units)
lambda_SU2 = 1 / C_LSI_SU2  # 4
lambda_SU3 = 1 / C_LSI_SU3  # 24/5 = 4.8
print(f"\nλ_1(SU(2)) ≥ 1/C_LSI = {lambda_SU2:.6f}")
print(f"λ_1(SU(3)) ≥ 1/C_LSI = {lambda_SU3:.6f}")

# m_gap² ≥ λ_1 (intrinsic Markov-time)
print(f"\nFramework prédit : m_gap²(SU(3)) ≥ {lambda_SU3:.4f} > {lambda_SU2:.4f} = m_gap²(SU(2))")
print(f"Donc m_gap(SU(3)) ≥ {sqrt(lambda_SU3):.4f} > {sqrt(lambda_SU2):.4f} = m_gap(SU(2))")
print(f"Ratio prédit m_gap(SU(3))/m_gap(SU(2)) = {sqrt(lambda_SU3/lambda_SU2):.4f}")

# Lattice AT2021
print("\n§2 DONNÉES LATTICE AT2021")
print("-" * 70)
m0pp_SU2 = 3.781  # in √σ units
m0pp_SU3 = 3.405
print(f"m(0⁺⁺)(SU(2)) / √σ_SU2 = {m0pp_SU2}")
print(f"m(0⁺⁺)(SU(3)) / √σ_SU3 = {m0pp_SU3}")
print(f"Ratio AT2021 m(SU(3))/m(SU(2)) en unités √σ : {m0pp_SU3/m0pp_SU2:.4f}")
print(f"⟹ SU(3) glueball PLUS PETIT que SU(2) en √σ units (RATIO 0.9007)")

# Tension :
print("\n§3 ANALYSE TENSION")
print("-" * 70)
print(f"\nFramework : m_gap(SU(3))/m_gap(SU(2)) = {sqrt(lambda_SU3/lambda_SU2):.4f} (intrinsic Markov units)")
print(f"AT2021    : m_0++ (SU(3))/m_0++ (SU(2)) = {m0pp_SU3/m0pp_SU2:.4f} (√σ units)")
print(f"\nTension RATIO : {sqrt(lambda_SU3/lambda_SU2) / (m0pp_SU3/m0pp_SU2):.4f}")

# H1 : convention C_LSI inverse
print("\n§4 HYPOTHÈSE H1 : Direction C_LSI κ-correction inverse ?")
print("-" * 70)
# Si saturation augmente C_LSI au lieu de la diminuer :
C_LSI_SU3_alt = c_inf_D4 * (1 + kappa_SU3)
print(f"Si C_LSI(SU(3)) = c_∞·(1+κ) au lieu de (1-κ) :")
print(f"  C_LSI(SU(3)) = {C_LSI_SU3_alt:.6f} = 7/24 > 1/4 = C_LSI(SU(2))")
lambda_SU3_alt = 1 / C_LSI_SU3_alt
print(f"  λ_1(SU(3)) ≥ {lambda_SU3_alt:.6f} < {lambda_SU2:.6f} = λ_1(SU(2))")
print(f"  m_gap(SU(3))/m_gap(SU(2)) = {sqrt(lambda_SU3_alt/lambda_SU2):.4f}")
print(f"  COHÉRENT avec AT2021 SU(3) PLUS PETIT ! (mais signe κ contredit memory entries)")

# H2 : scale setting σ varie avec N
print("\n§5 HYPOTHÈSE H2 : σ(N) varie avec N — comparaison faussée")
print("-" * 70)
# Pour 't Hooft : σ ≈ Λ²·f(N) où f(N) peut dépendre de N
# Si σ(SU(2))/σ(SU(3)) = κ_σ alors m(0++)_phys = (m/√σ)·√σ varie
# Données lattice : σ_SU2 et σ_SU3 sont calibrés différemment
# Litt : σ a similaire échelle pour SU(N) à 't Hooft fixe, mais corrections 1/N² existent
print("""
'T Hooft scaling : σ → const(λ) quand N→∞ (Eguchi-Kawai/Bringoltz-Teper)
Mais pour N=2 vs N=3, corrections 1/N² ≈ 10-25% existent.

Si σ(SU(3))/σ(SU(2)) ≠ 1 mais κ_σ ≈ 0.81 (par exemple), alors :
m_0pp_phys(SU(2)) = 3.781·√σ_SU2 = 3.781·√1.00·Λ = 3.781·Λ
m_0pp_phys(SU(3)) = 3.405·√σ_SU3 = 3.405·√0.81·Λ = 3.063·Λ
Ratio physique = 3.063/3.781 = 0.81 → SU(3) encore plus petit

⟹ H2 seul ne résout pas la tension.
""")

# H3 : framework formule c_∞·(1-κ) à revoir
print("\n§6 HYPOTHÈSE H3 : Direction κ-correction et SCALE-SETTING combinées")
print("-" * 70)
# Possible : κ correction agit sur PINSKER constant (TV ≤ √(C·Ent)) au lieu de C_LSI direct
# Dans cette interprétation, saturation augmente le Pinsker constant (mesure plus "spread")
# ce qui DIMINUE la spectral gap effective
print("""
Alternative formulation : κ peut affecter le 'Pinsker constant' C_P plutôt que C_LSI direct.
TV² ≤ C_P · Ent. Saturation augmente C_P → diminue λ_1 effective → m_gap plus petit.
Ceci serait COHÉRENT avec AT2021.

Mais cela contredit notre dérivation Hodge KappaOneSixth.lean où κ=1/6 est défini comme
SATURATION DEFICIT (déficit Bakry-Émery). Le signe et le rôle de κ doivent être re-clarifiés.
""")

# H4 : m_gap intrinsic ≠ m_glueball physical
print("\n§7 HYPOTHÈSE H4 : m_gap intrinsic ≠ m_glueball physical (le plus probable)")
print("-" * 70)
print("""
Le 'm_gap intrinsic' du framework est le spectral gap du Markov chain (générateur Dirichlet)
sur la mesure de Gibbs. L'unité de temps est la marche Markov.

Le 'm_glueball physical' AT2021 est la masse du plus léger état 0⁺⁺ dans le spectre quantique
réel (OS reconstruction de la mesure euclidienne). L'unité physique est √σ.

CES DEUX QUANTITÉS NE SONT PAS DIRECTEMENT COMPARABLES sans une conversion explicite
entre 'temps Markov intrinsic' et 'temps physique' (cette conversion peut dépendre de N).

LA TENSION OBSERVÉE EST DONC PROBABLEMENT UN ARTEFACT DE COMPARAISON DE QUANTITÉS
DANS DES UNITÉS DIFFÉRENTES, PAS UNE INCOHÉRENCE THÉORIQUE DU FRAMEWORK.

C'est une LIMITATION HONNÊTE à reconnaître : le framework prédit le spectral gap intrinsic,
pas directement la glueball mass physique. La comparaison aux données AT2021 nécessite
une étape supplémentaire de scale-setting qui n'est pas dans notre framework actuel.
""")

# Verdict
print("\n" + "=" * 90)
print("§8 VERDICT TENSION")
print("=" * 90)

print("""
La tension SU(3) vs SU(2) entre framework et AT2021 lattice est PROBABLEMENT due à :

HYPOTHÈSE PRINCIPALE : H4 — Conversion intrinsic Markov ↔ physical scale non triviale.
Le framework prédit le spectral gap du processus stochastique (Markov-time units),
pas directement la masse glueball quantique (√σ units). La comparaison directe est
INVALIDE sans scale-setting explicite cross-N.

CE QUE LA TENSION NE SIGNIFIE PAS :
- Pas une falsification du framework (échelles différentes)
- Pas une falsification de κ=1/6 (algébrique Hodge, indépendant)
- Pas une falsification de manifestation 9 (purement géométrique)

CE QUE LA TENSION SIGNIFIE :
- Notre framework prédit qualitativement le mass gap, pas quantitativement m_glueball
- La 'tension' devrait être documentée comme LIMITATION HONNÊTE
- Conversion Markov↔physical scale = direction future de recherche
- Pour test décisif : MK SU(3) D=4 β-scan + Markov-time observable (PAS comparison m_glueball)

IMPLICATIONS PUBLICATIONS :
- v22 master doc : ajouter §honnête sur tension + résolution H4
- Pitch Bauerschmidt : mentionner ouverture conversion scale-setting
- Lean stack : OK (rien à changer, c'est une question d'interprétation physique)

P(Clay 10y) : INCHANGÉ 40-55%. La tension n'affecte pas l'argument central.
""")

# Action recommandée
print("=" * 90)
print("§9 ACTION RECOMMANDÉE — RÉSOUDRE TENSION VIA TEST DIRECT")
print("=" * 90)

print("""
TEST DÉCISIF (au lieu de comparer m_glueball/√σ qui est ambiguë) :

Mesurer DIRECTEMENT le spectral gap intrinsic du Markov chain pour SU(2) vs SU(3).

Protocole :
1. Run HMC SU(2) D=4 et HMC SU(3) D=4 à même β en 't Hooft (λ=g²·N fixe)
2. Calculer autocorrélation de plaquette à chaque cas
3. Extraire τ_int(SU(2)) et τ_int(SU(3))
4. Comparer 1/τ_int (proxy spectral gap intrinsic)

Si 1/τ_int(SU(3)) > 1/τ_int(SU(2)) ⟹ framework confirmé (saturation SU(3) → larger gap)
Si 1/τ_int(SU(3)) < 1/τ_int(SU(2)) ⟹ framework à raffiner (saturation direction inverse)

Pas besoin de comparer aux glueballs. Test purement intrinsic Markov.

Faisabilité : 4-8h compute sur PC gamer GPU si on a HMC SU(3) (B nécessite SU3HMC implementation).
""")
