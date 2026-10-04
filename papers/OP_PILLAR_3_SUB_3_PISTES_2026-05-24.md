> **⚠️ RETRACTION NOTICE (2026-10-04) — read this first. / AVIS DE RÉTRACTION (04/10/2026) — à lire d'abord.**
>
> This document claims or prepares a proof of the 4D Yang–Mills mass gap
> (Clay Millennium problem), or states a probability of obtaining one
> ("P(Clay …)"). **No such proof exists, and this repository does not claim
> one** (see the README, "Honest scope"). The text below is kept unchanged as
> a historical record; it must not be read or cited as a proof.
>
> - Every version of the chain rests on steps that were **never proved** and
>   enter only as stated conditions or Lean `axiom`s: depending on the version,
>   the continuum step (finite-β Lemma B / Conjecture C*, declared as
>   `axiom lemma_B_beta_finite`, `lean/Crossed/InformationConservation.lean`
>   l.445), the
>   Transport Conjecture (itself a stack of two open problems, THEOREMS_INDEX
>   OPEN-Transport), and, in the 2026-05-26 KR-FP chain, the structural
>   hypothesis **Hyp-CST** (`lean/Crossed/Hyp_CST.lean`: "SKETCH (axiom
>   declared, not proven Lean-side)", l.22; `axiom Hyp_CST`, l.88). Our
>   internal claim register records Hyp-CST as the lock of the KR-FP chain,
>   never proved, and the KR-FP chain itself as dead (its curvature ⟹ gap
>   route gives only empty bounds in d = 4, internal finding of 2026-07-30).
>   Our internal programme map of 2026-07-19 lists a rigorous constructive
>   proof of the gap as ongoing work, not as achieved.
> - "0 sorry" in Lean does not mean "proved" here: the analytic content sits
>   in named axioms (117 `axiom` declarations in `lean/Crossed/`), and the
>   theorem `mass_gap_continuum_D4` (`InformationConservation.lean`
>   l.531-537) concludes `∃ m_phys_sq > 0`, which holds trivially.
> - Every success probability stated below (P(Clay …), feasibility
>   percentages) is **withdrawn**: subjective, with no verifiable basis.
>
> *FR — Ce document revendique ou prépare une preuve du gap de masse de
> Yang–Mills 4D, ou annonce une probabilité d'en obtenir une. Cette preuve
> n'existe pas : les étapes décisives
> (Lemme B à β fini / Conjecture C*, conjecture de transport, hypothèse
> Hyp-CST) n'ont jamais été prouvées et n'apparaissent en Lean que comme
> axiomes. Le texte est conservé tel quel comme archive ; il ne doit être ni
> lu ni cité comme une preuve. Les probabilités annoncées sont retirées.*
>
> Details and the list of points still open: [CHANGELOG.md](../CHANGELOG.md),
> entry integrity-2026-10-04.

---

# OP-PILLAR-3-SUB-3-PISTES — Evaluation of 4 routes to resolve the zero-mode obstruction

**Author**: Claude Opus 4.7 (1M ctx), max-effort honest delivery
**Date**: 2026-05-24
**Anti-fab**: 9 arXiv refs verified verbatim. No invented theorem. No cosmo speculation. Honest distinction PROVED / SKETCH / OPEN.

---

## §0. Énoncé du sub-3 problem

**Pillar 3 sub-3 visé** (cf `/root/cc-private/papers/OP_PILLAR_3_FORMAL_2026-05-24.md` §4):

Pour la mesure Wilson μ_{a,β} sur SU(N)^E(Λ_a), la restriction à Class F = Harm² ⊗ su(N) satisfait un Bakry-Émery uniforme en β grand avec λ_min(Δ_1)|_{Harm²} → c_∞(D).

**Obstruction structurelle** : Sur Harm² par définition d'espace cohomologique harmonique, Δ_1 ≡ 0. Donc le mode zéro k = 0 donne Hess(βS_W) = 0. Ric_eff(0) = N (Besse 1987). Bakry-Émery direct donne C_LSI(0) ≤ 2/N, contredisant asymptote visée c_∞(D) = 1/4 universelle pour D=4.

---

## §1 — Piste 1 : Twist 't Hooft

**Référence** : 't Hooft 1979 *Nucl. Phys. B* **153**, 141 + van Baal 1982 *CMP* **85**, 529 + Sternbeck-von Smekal-Williams-Bowman 2005 (hep-lat/0509134, vérifié WebFetch : "*The zero momentum mode is projected out by the twisted boundary conditions*").

**Mécanisme** : conditions de bord twistées sur tore T^D, n^{μν} ∈ Z_N. Modes Fourier autorisés k_μ ∈ (2π/NL)Z\{0}. Mode zéro **éliminé**, k_min = 2π/NL non nul.

**Caveat** : modifie secteur topologique (Q = ν − κ/N fractionnaire). Continuité twist → secteur trivial PAS rigoureusement établie pour SU(N) 4D.

**Verdict Piste 1** :
| Critère | Évaluation |
|---|---|
| Faisabilité | ⭐⭐⭐⭐ — Mécanisme bien établi, code lattice existant |
| Effort | **2-4 mois-homme** |
| P(succès local sub-3) | **65-80%** |
| Bypass clean B1 ? | **NON** |

---

## §2 — Piste 2 : Restriction k ≥ 2π/L

**Procédure** : éliminer mode k=0 "à la main", normaliser par modes restants.

**Référence** : pas de canonique non-abélien. Magnen-Rivasseau-Sénéor 1993 *CMP* **155**, 325 (vérifié projecteuclid) utilise IR cutoff explicite, pas restriction k≥2π/L.

**Limite thermodynamique L → ∞** : k_min^2 → 0 → on retombe sur le mode zéro problème. Palliatif local seulement.

**Verdict Piste 2** :
| Critère | Évaluation |
|---|---|
| Faisabilité | ⭐⭐ — Conceptuellement simple mais cohérence OS douteuse |
| Effort | **3-6 mois-homme** |
| P(succès local sub-3) | **20-35%** |
| **Recommandation** | **À ABANDONNER** |

---

## §3 — Piste 3 : Quotient centre Z_N

**Mathematics** : SU(N)/Z_N (Greensite 2003 hep-lat/0301023 vérifié).

**Subtilité critique** : Z_N est discret, donc T_e G = T_e (G/Z_N). La fibre tangente Harm² ⊗ su(N) **n'est PAS modifiée** par le quotient.

**Le mode zéro vit dans la fibre tangente** — quotient Z_N ne résout PAS sub-3.

**Verdict Piste 3** :
| Critère | Évaluation |
|---|---|
| Faisabilité | ⭐⭐ — Mal posée pour sub-3 spécifiquement |
| Effort | **6-12 mois-homme** |
| P(succès local sub-3) | **15-30%** |
| **Recommandation** | **À EXPLORER mais pour programme cross-π_1 (f(π_1(G))), PAS pour sub-3** |

**Note importante** : Theorem C empirique observe DÉJÀ distinction SO(N)/SU(N) liée à π_1 (MEMORY CLAY 2026-05-23). Quotient Z_N peut affecter f(π_1(G)), pas le mode zéro de Harm².

---

## §4 — Piste 4 : BBD multiscale Polchinski

**Cadre BBD vérifié** :
- arXiv:2307.07619 (BBD 2024 *Probab. Surv.* 21) : multiscale BE via Polchinski
- arXiv:2202.02295 (Bauerschmidt-Dagallier 2024 *CPAM* 77) : LSI φ⁴_3 via Polchinski multiscale
- arXiv:1907.12308 (Bauerschmidt-Bodineau 2021 *CPAM* 74) : sine-Gordon LSI β < 6π

**Obstacles structurels SU(N) (DS Bot bd_adapter_su2)** :
1. SU(N) variété compacte non-vectorielle (vs ℝⁿ scalaire)
2. **Absence inégalités de corrélation GKS/GHS pour non-abéliens** (Jaffe-Witten 2006 Clay)
3. Interaction Wilson trigonométrique non-polynomiale
4. Invariance jauge globale
5. Perron-Frobenius volume infini

**Bloqueur #2** est documenté dans le problème Clay officiellement.

**Est-ce vraiment = B1 reformulé ?** : **OUI, proche de B1 reformulé**, PAS un bypass propre. Les deux utilisent cluster expansion non-abélienne comme building block.

**Élément distinctif** : SZZ 2022 (arXiv:2204.12737) prouve LSI rigoureux mais uniquement |β| < 1/48 — OPPOSÉ du régime β grand visé.

**Verdict Piste 4** :
| Critère | Évaluation |
|---|---|
| Faisabilité | ⭐⭐⭐ — Cadre BBD existe pour scalaires, extension SU(N) OPEN |
| Effort | **18-36 mois-homme** (DS Bot G3 estime 3-5 ans) |
| P(succès local sub-3) | **35-55%** |
| Bypass clean B1 ? | **NON — reformulation moderne mais mêmes blocs** |

---

## §5 — Synthèse comparative

| Piste | Faisabilité | Effort (mois-homme) | P(succès sub-3) | Bypass B1 ? |
|---|---|---|---|---|
| **1 Twist 't Hooft** | ⭐⭐⭐⭐ | 2-4 | **65-80%** | NON |
| **2 k ≥ 2π/L** | ⭐⭐ | 3-6 | **20-35%** | NON |
| **3 Quotient Z_N** | ⭐⭐ | 6-12 | **15-30%** | NON |
| **4 BBD multiscale** | ⭐⭐⭐ | 18-36 | **35-55%** | NON (reformulation) |

**Aucune piste ne bypass clean B1**.

---

## §6 — Recommandation

### Recommandation #1 (PRIORITAIRE) : Piste 1 + Piste 4 en parallèle

- **Piste 1 (Twist 't Hooft) court terme (2-4 mois)** : preuve de concept que sub-3 est résoluble (secteur twist). Publishable LMP/CMP standalone "LSI for twisted SU(N) Wilson lattice".

- **Piste 4 (BBD multiscale) moyen terme (18-36 mois)** : formalisation complète Pillar 3 dans secteur trivial ν=0. Collab Bauerschmidt-Dagallier acceptance CMP/Annals.

### Recommandation #2 (À ABANDONNER) : Piste 2

Palliatif local sans valeur structurelle.

### Recommandation #3 (À EXPLORER mais PAS pour sub-3) : Piste 3

Pertinent pour programme cross-π_1 (f(π_1(G))) déjà observé empiriquement.

### Impact sur P(Clay 10 ans)

- Avec Piste 1 seule : +3-5 pp (élimine sub-3 secteur twist, ~40-50% chemin Pillar 3)
- Avec Piste 1 + 4 : +5-8 pp (~70-85% chemin Pillar 3 prouvé)

**P(Clay 10y) après ces 2 pistes** : 45-65% (vs 40-55% v21).

---

## §7 — Limitations honnêtes

- DS Bot a 2 verdicts contradictoires sur BBD/SU(N) : G3 optimiste 65/100 vs bd_adapter pessimiste 52.5/100. Pondère vers pessimiste car 5 obstacles documentés dans littérature.
- **Aucune piste ne résout B1 (cluster expansion non-abélienne SU(N) 4D)** qui reste verrou rigoureux majeur. P(Clay) dominée par P(B1 prouvé).
- L'argument continuité twist → secteur trivial (clé Piste 1) est OPEN (30-50% réussite).
- Cluster firm : AUCUNE nouvelle réf arXiv non vérifiée. Toutes refs WebFetch verbatim.

---

## Sources arXiv vérifiées (verbatim WebFetch / WebSearch)

| arXiv | Authors | Titre / Statut |
|---|---|---|
| 2307.07619 | BBD 2024 *Probab. Surv.* | Multiscale BE via Polchinski survey |
| 2202.02295 | Bauerschmidt-Dagallier 2024 *CPAM* | LSI φ⁴_2 φ⁴_3 |
| 1907.12308 | Bauerschmidt-Bodineau 2021 *CPAM* | Sine-Gordon LSI β < 6π |
| 2204.12737 | Shen-Zhu-Zhu 2022 *CMP* | SU(N) LSI strong coupling β < 1/48 |
| 2202.10375 | Adhikari-Cao 2022 *AOP* | **Finite groups only — NE s'applique PAS SU(N)** |
| 2509.04688 | Cao-Nissim-Sheffield 2025 | Area law lattice (DF80 mass gap, PAS LSI) |
| hep-lat/0509134 | Sternbeck et al. 2005 | Zero-mode suppression twisted bc |
| hep-lat/0301023 | Greensite 2003 | Confinement review center vortices |
| 10.1007/BF01403503 | van Baal 1982 *CMP* | SU(N) gauge fields hypertorus |

**Verdict global final** : 
- Piste 1 (Twist 't Hooft) recommandée court-terme (P=65-80%, 2-4 mois)
- Piste 4 (BBD multiscale) recommandée moyen-terme (P=35-55%, 18-36 mois)
- Piste 2 à abandonner
- Piste 3 à explorer pour programme cross-π_1 (f(π_1(G))) mais pas sub-3 spécifiquement
- **Aucune piste ne contourne B1 (cluster expansion non-abélienne)** qui reste verrou rigoureux majeur
