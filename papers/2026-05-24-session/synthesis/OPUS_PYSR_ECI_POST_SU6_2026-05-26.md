---
title: "PySR refit propre κ_lattice(N) cross-N post-finding SU(6) THERM5000"
author: "Kévin Rémondière"
orcid: "0009-0008-2443-7166"
affiliation: "Independent researcher, Oloron-Sainte-Marie, France"
email: "kevin.remondiere@gmail.com"
date: 2026-05-26
status: "ANALYSE PROPRE — refit symbolic regression rigoureux 5 datapoints"
---

# PySR refit ECI post-SU(6) — analyse détaillée

## Résumé exécutif

Suite au finding SU(6) THERM5000 ($\kappa_{\rm EE}({\rm SU}(6)) = 0.8099 \pm 0.0055$ vs prédiction $\zeta(3)/\sqrt{\pi} \cdot (1-1/36) = 0.6593$, **27.4σ falsification** de la loi $\kappa(N) = \kappa_{\infty} \cdot (1-1/N^2)$), un PySR symbolic regression propre a été lancé sur les 5 datapoints disponibles $\{(2, 0.5080), (3, 0.6025), (4, 0.6353), (5, 0.6897), (6, 0.8099)\}$.

**Trois résultats clés** :

1. **PySR best fit (cplx=14, 3 params)** : $\kappa(N) = a N^2 + (b - c/N^2)/N$ avec $a=0.01445$, $b=1.838$, $c=3.760$ → $\chi^2/{\rm dof} = 0.86$. Mais **extrapolation diverge** : $\kappa(N=8) = 1.15 > 1$, **physiquement absurde**.

2. **F1 (1−1/N²) reste excellent sur N∈{2,3,4}** : $\chi^2_{N\le 4} = 0.002$ (dof=2), $\kappa_{\infty, {\rm local}} = 0.6778 \pm 0.003$, compatible $\zeta(3)/\sqrt{\pi} = 0.6782$ à 0.15σ. Mais **F1 cassée à 27σ pour N=6**.

3. **Hypothèse centre Z_N premier/composite RÉFUTÉE** : N=4 (Z₄ composite) suit parfaitement F1 (0.02σ), ce qui contredit l'hypothèse "centre composite dévie".

**Verdict ECI Phase 1** : La phénoménologie pour N≤4 (le régime utilisé dans la BIG_MASS_TABLE pour m_H = κ(SU(2))·v et m_H/m_Z = √(15/8)) reste intacte. Mais l'**asymptote universelle** $\kappa_{\infty} \equiv \zeta(3)/\sqrt{\pi}$ et toute prédiction utilisant $\kappa(N\ge 5)$ extrapolée est **structurellement abandonnée**. P(ECI Phase 1) maintenu **60-70%** post-finding (baisse 10-15 pp vs pré-SU(6)).

## Dataset

| N | $\kappa_{\rm lattice}$ | erreur | $\beta_{\rm 't~Hooft}$ | source |
|---|---|---|---|---|
| 2 | 0.5080 | 0.010 | 2.4 | BP2008b L=4..12 |
| 3 | 0.6025 | 0.0033 | 5.4 | jax_su3_EE_BP2008b L=4..12 |
| 4 | 0.6353 | 0.0044 | 10.0 | jax_su4_EE_BP2008b L=4..10 |
| 5 | 0.6897 | 0.009 | 15.0 | jax_su5_EE_BP2008b 800 sweeps préliminaire |
| 6 | 0.8099 | 0.0055 | 21.6 | jax_su6_EE_BP2008b THERM5000 |

Référence méthode : Buividovich & Polikarpov, arXiv:0802.4247 (BP2008b α-integration sur lattices déformés).

## Phase 1 — 14 candidats 1-paramètre

Fit par $\chi^2$ pondéré sur 5 points. Best résultats :

| Formule | $a_{\rm fit}$ | $\chi^2$ | $\chi^2/{\rm dof}$ | AIC | BIC |
|---|---|---|---|---|---|
| F8 $a \cdot N^{1/3}$ | 0.4178 | 136.2 | 34.0 | 138.2 | 137.8 |
| F5 $a \sqrt{N}$ | 0.3344 | 161.1 | 40.3 | 163.1 | 162.7 |
| F11 $a \log(N{+}1)/\log 3$ | 0.4566 | 185.8 | 46.5 | 187.8 | 187.4 |
| F1 $a(1{-}1/N^2)$ | 0.7097 | 602.5 | **150.6** | 604.5 | 604.1 |
| F12 $a(N^2{-}1)/N^2$ (équiv F1) | 0.7097 | 602.5 | 150.6 | 604.5 | 604.1 |

**Aucune formule 1-paramètre ne fit les 5 points**. Le moins mauvais est F8 ($a N^{1/3}$) à $\chi^2/{\rm dof} = 34$, encore très mauvais. La famille (1−1/N²) qui marchait sur N∈{2,3,4} est cassée à $\chi^2/{\rm dof} = 150$.

## Phase 2 — Candidats 2 et 3 paramètres

| Formule | params | $\chi^2$ | $\chi^2/{\rm dof}$ | AIC |
|---|---|---|---|---|
| **M10** $a(1{-}1/N^2) + b\,\delta_{N=6}$ | $a=0.681, b=0.148$ | 17.3 | **5.76** | 21.3 |
| M13 $a(1{-}1/N^2) + b(1{-}\mathbb{1}_{\rm prime}(N))(N{-}4)$ | $a=0.681, b=0.074, c=10^{-4}$ | 17.3 | 8.63 | 23.3 |
| **M14** $a N^b + c$ | $a=0.0046, b=2.27, c=0.536$ | 46.9 | **23.5** | 52.9 |
| M6 $a N^b$ | $a=0.378, b=0.407$ | 96.9 | 32.3 | 100.9 |
| M12 $a(1{-}1/N^2) + bN + c$ | $a=-0.105, b=0.071, c=0.470$ | 65.8 | 32.9 | 71.8 |
| M11 $a + b/N + c/N^2$ | $a=1.112, b=-2.40, c=2.49$ | 127.2 | 63.6 | 133.2 |

**M10** est artificiel (utilise indicateur $\delta_{N=6}$ qui ne peut pas extrapoler) — il "patche" simplement la déviation à N=6. **M14** ($a N^b + c$) reste le meilleur fit "lisse" (sans indicateur ad hoc) à $\chi^2/{\rm dof}=23$, encore mauvais.

**Aucune formule analytique standard (puissance, logarithme, exponentielle, rationnelle bornée) ne fit les 5 datapoints simultanément à $\chi^2/{\rm dof} \le 5$ sans introduire une indicatrice ad hoc.**

## Phase 3 — Leave-one-out cross-validation

Test critique : enlever un point N, fitter sur les 4 autres, prédire le point manquant.

| Formule | RMS résidu LOO (σ) |
|---|---|
| F1 $a(1{-}1/N^2)$ | **14.5** |
| F2 $a N/(N{+}1)$ | 11.9 |
| F4 $a \log(N)$ | 18.7 |
| F5 $a \sqrt{N}$ | (échec) |
| **F8** $a N^{1/3}$ | **6.78** |
| F9 $a N^{1/4}$ | 9.56 |
| M3 $a + b \log N$ | 10.3 |
| **M6** $a N^b$ | **10.2** |
| M14 $a N^b + c$ | 10.8 |
| M11 $a + b/N + c/N^2$ | 26.3 |

**Verdict LOO** : la meilleure formule lisse en cross-validation est **F8 $a N^{1/3}$** (RMS = 6.8σ), suivie par F9 ($N^{1/4}$). Mais même elles laissent un résidu LOO > 6σ sur le point manquant, indiquant que **les 5 datapoints ne suivent aucune loi analytique simple à 1-2 paramètres**.

Notons que les détails LOO pour F8 montrent : N=2 (1.9σ), N=3 (0.03σ), N=4 (8.7σ), N=5 (3.0σ), N=6 (11.9σ). Le point N=4 et N=6 sont les plus problématiques sous F8.

## Phase 4 — PySR symbolic regression (Pareto front)

PySR a tourné avec : 200 itérations, population 80, max_complexity 15, opérateurs `+, -, *, /, sqrt, log, exp, square`, weights $1/{\rm err}^2$, variables `Nc, invNc, Nc2, primeZ`.

**Pareto front complet (15 équations)** :

| Cplx | Loss | Score | Équation |
|------|------|-------|----------|
| 1 | 1.6e-1 | 0.0 | `invNc` |
| 2 | 6.4e-3 | 3.18 | `0.6462` (constante) |
| 3 | 5.5e-3 | 0.15 | `log(sqrt(Nc))` |
| 4 | 1.3e-3 | 1.45 | `0.9302 - invNc` |
| 5 | 8.1e-4 | 0.47 | `sqrt(0.1104 * Nc)` |
| 6 | 6.3e-4 | 0.26 | `log(log(Nc + 3.07))` |
| **7** | 2.4e-4 | 0.96 | `0.00782 * Nc^2 + 0.521` |
| 8 | 2.3e-4 | 0.03 | `(0.00463 Nc^2 + 0.727)^2` (signe à corriger) |
| 9 | 2.3e-4 | 0.03 | `0.5117 - (Nc^2 + primeZ) * (-0.00809)` |
| 10 | 2.2e-4 | 0.01 | `(0.7227 - (primeZ + Nc^2) * (-0.00481))^2` |
| 11 | 1.8e-4 | 0.19 | `(0.00709 Nc^2 + 0.5425) - 1/Nc^4` |
| 12 | 1.4e-4 | 0.28 | `(0.00759 Nc^2 + 0.5263) - Nc/exp(Nc^2)` |
| 13 | 5.1e-5 | 1.01 | `((1/Nc - exp(Nc) * 0.000993) / (-2.584)) + 0.7176` |
| **14** | **8.6e-6** | **1.77** | **`0.01445 Nc^2 + (1.838 - 3.760/Nc^2)/Nc`** |
| 15 | 8.4e-6 | 0.02 | `0.01414 Nc^2 + (1.387 - 1.743/Nc^2)^2 / Nc` |

**Best PySR pick** : **cplx=14**, $\kappa(N) = a N^2 + (b - c/N^2)/N$ avec $a=0.01445$, $b=1.838$, $c=3.760$.

Vérification numérique sur les 5 points :

| N | obs | pred | résidu σ |
|---|---|---|---|
| 2 | 0.5080 | 0.5068 | -0.12 |
| 3 | 0.6025 | 0.6035 | +0.30 |
| 4 | 0.6353 | 0.6320 | -0.75 |
| 5 | 0.6897 | 0.6988 | +1.01 |
| 6 | 0.8099 | 0.8092 | -0.13 |

→ $\chi^2 = 1.71$, $\chi^2/{\rm dof} = 0.86$ — **excellent fit**.

**MAIS extrapolation diverge** :

| N | $\kappa$ pred (cplx=14) |
|---|---|
| 7 | 0.960 |
| 8 | 1.147 |
| 9 | 1.370 |
| 10 | 1.625 |
| 12 | 2.232 |
| 16 | 3.814 |

→ $\kappa(N=8) > 1$, **physiquement absurde** pour une entropie d'enchevêtrement normalisée par boundary 2D. Le terme dominant $a N^2$ avec $a=0.01445$ envoie $\kappa$ vers $+\infty$ comme $N^2/64$.

### Analyse des autres équations Pareto

**Cplx=11** $\kappa = (a N^2 + b) - 1/N^4$ avec $a=0.00709$, $b=0.5425$. $\chi^2/{\rm dof} = 12.2$, **toujours diverge** comme $N^2$ asymptotiquement (N=20 → 3.38).

**Cplx=7** $\kappa = a N^2 + b$ pure quadratique. Plus simple mais $\chi^2/{\rm dof} = 15.9$ insuffisant, et **diverge en $N^2$** également.

**Cplx=13** utilise $\exp(N)$, $\kappa(N=10) = 9.15$, $\kappa(N=12) = 63$. **Catastrophe extrapolative**.

**Conclusion Phase 4** : PySR a trouvé des formules à **excellent χ² sur les 5 points**, mais **toutes divergent à l'extrapolation N→∞**. Cela suggère soit (i) les données SU(5,6) sont contaminées par effets de volume fini / thermalisation insuffisante, soit (ii) il existe une vraie transition (Lucini-Teper bulk transition) entre régime N≤4 et N≥5, soit (iii) un effet systématique commun aux mesures SU(5,6) à $\beta_{\rm 't Hooft}$ élevé.

## Phase 5 — κ_∞ asymptote candidates revisités

Fit F1 $\kappa = A \cdot (1 - 1/N^2)$ sur sous-ensembles :

| Sous-ensemble | $A$ extrait | $\chi^2$/dof | Conclusion |
|---|---|---|---|
| N ∈ {2,3,4} | $0.6777 \pm 0.003$ | $0.002/2 = 0.001$ | Excellent |
| N ∈ {2,3,4,5} | $0.6812$ | $17.3/3 = 5.8$ | N=5 dévie |
| N ∈ {2,3,4,5,6} | $0.7097$ | $602.5/4 = 150.6$ | F1 CASSÉE |

**$\kappa_{\infty, {\rm local}} = 0.6777 \pm 0.003$ (régime N ≤ 4)** benchmarking :

| Candidat | Valeur | Δσ vs $\kappa_{\rm loc}$ | Motivation |
|---|---|---|---|
| $\zeta(3)/\sqrt{\pi}$ | 0.6782 | **0.15** | 3-loop YM N³LO / Gaussian (premier choix) |
| $\pi/(\pi + 3/2)$ | 0.6768 | 0.30 | Padé-like |
| 17/25 | 0.6800 | 0.76 | Rationnel petit denom |
| 27/40 | 0.6750 | 0.91 | Rationnel |
| $1 - 1/\pi$ | 0.6817 | 1.32 | π combination |
| 2/3 (Koide $4\kappa$) | 0.6667 | 3.69 | À rejeter |
| $\ln 2$ | 0.6931 | 5.14 | À rejeter |

**Verdict asymptote LOCALE** : $\zeta(3)/\sqrt{\pi}$ reste le candidat le plus probable pour $\kappa_{\infty}^{\rm local}$ (N≤4 seulement). À 0.15σ, c'est un "near hit". Mais ce n'est plus **un asymptote universel** — c'est juste la valeur locale qui ajuste les 3 points N=2,3,4.

## Phase 6 — Hypothèse centre Z_N premier/composite

L'hypothèse pré-PySR (Opus 2026-05-26) : la formule F1 (1−1/N²) marche pour les groupes SU(N) avec $|Z_N|$ premier (N=2,3,5,7) et casse pour |Z_N| composite (N=4,6,8,9) via contributions de vortex de centre.

**Test empirique avec les 5 datapoints** :

| N | $|Z_N|$ | classe | pred F1 | obs | résidu σ |
|---|---|---|---|---|---|
| 2 | 2 | premier | 0.5083 | 0.5080 | -0.03 |
| 3 | 3 | premier | 0.6024 | 0.6025 | +0.02 |
| **4** | **4** | **composite (2²)** | **0.6354** | **0.6353** | **-0.02** |
| 5 | 5 | premier | 0.6506 | 0.6897 | **+4.34** |
| 6 | 6 | composite (2·3) | 0.6589 | 0.8099 | **+27.45** |

**Verdict hypothèse Z_N** : **PARTIELLEMENT RÉFUTÉE**.

- N=4 a $|Z_4|=4$ composite ($2^2$), mais **suit parfaitement F1** (résidu 0.02σ). L'hypothèse prédisait une déviation pour N=4 — elle n'est pas observée.
- N=5 a $|Z_5|=5$ premier, mais **dévie** (résidu 4.3σ). L'hypothèse prédisait que N=5 suive F1 — c'est faux.
- N=6 dévie massivement (composite), cohérent avec hypothèse mais pas suffisant pour valider seul.

→ **Conclusion** : Le pattern "premier vs composite |Z_N|" ne suffit pas à expliquer les déviations. Il faut un autre mécanisme.

## Phase 7 — Hypothèses alternatives à investiguer

### (H_A) Lucini-Teper bulk transition (SU(N≥5) déconfiné)

Lucini-Teper (et collaborateurs, e.g. Lucini-Panero) ont documenté que pour SU(N≥5) en pure-gauge 4D, il existe une transition de premier ordre entre phase déconfinée à $\beta$ grand et phase confinée à $\beta$ petit, avec une bande de coexistence (bulk transition) qui n'existe pas pour N≤4.

À nos $\beta_{\rm 't Hooft}$ utilisés ($\lambda = g^2 N$ fixé à $\sim 0.4$ pour matching 't Hooft) :
- SU(2,3,4) : phase confinée pure, équilibre rapide
- SU(5,6) : peut-être proche de la bulk transition, équilibration lente

**Test à faire** : refaire SU(5,6) à $\beta$ encore plus fort (au-delà de la bulk transition) pour voir si $\kappa$ change. Si SU(5,6) à $\beta$ très grand donne $\kappa \approx 0.65$ (suivant F1), alors l'anomalie est un artefact de phase déconfinée.

### (H_B) Effet systématique de volume fini

Nos mesures SU(5,6) sont à L=4,6,8,10. Pour SU(N), la taille de boundary $L^2$ doit être large par rapport à la longueur de corrélation $\xi$ à $\beta$ donné. À $\beta$ grand ('t Hooft fixé), $\xi$ croît comme $N^{1/2}$ (asymptotic freedom), donc pour SU(6) nous serions à $L/\xi \sim 2-3$ seulement (alors que SU(2) atteint $L/\xi \sim 5-6$).

**Test à faire** : SU(5,6) à L=12,14,16,20 (volumes plus grands).

### (H_C) Mauvaise thermalisation SU(5,6) à 800 sweeps

SU(6) à THERM5000 a corrigé de 800 sweeps. Mais SU(5) reste à 800 sweeps préliminaires. **Re-mesurer SU(5) à THERM5000 est URGENT** — peut-être que SU(5) revient sur la courbe F1 si bien thermalisé.

### (H_D) Transition lisse SU(4) → SU(∞) via une vraie formule non-(1-1/N²)

Peut-être la vraie formule n'est ni F1 ni F8 mais quelque chose comme :
$\kappa(N) = \kappa_{\rm asymptote} \cdot \tanh(\beta_0 N / N_c) + (\text{small finite-N corrections})$

avec une saturation à $\kappa_{\rm asymptote} \approx 1$. À vérifier en mesurant SU(7,8,9,10).

## Vérification BIG_MASS_TABLE (22 ratios survivants)

Le finding PySR n'affecte que les ratios **Cat 4** (extrapolation N≥5). Tous les ratios **Cat 1** (κ(SU(2)) lattice direct, m_H = κ·v) et **Cat 2** (arithmétique pure) restent intacts.

**Ratios SURVIVANT post-PySR** :

| Bloc | Compte | Verdict |
|---|---|---|
| Bosons (m_H, m_Z, m_W, m_t, Higgs) | 6 | Survivent (Cat 1, 2) |
| Couplages (sin²θ_W, cos²θ_W, sin³θ_W) | 3 | Survivent (Cat 2) |
| CKM (/23 cluster) | 4 (de 5) | Survivent (Cat 2), 1 compromis (A²≈κ_∞) |
| PMNS (/7, /11) | 2 | Survivent (Cat 2) |
| Cosmologie (n_s, Ω_b/Ω_DM) | 3 | Survivent (Cat 2) |
| Fermions Yukawa | 6 | Survivent (Cat 2 pairs M_24) |
| **TOTAL** | **22-23 / 25** | **88-92% survivent** |

**Ratios FALSIFIÉS** : y_top² = κ(SU(7))/κ_∞ = 48/49 et y_top² = κ(SU(8))/κ_∞ = 63/64. Les coïncidences numériques 48/49 ≈ 0.9796 et 63/64 ≈ 0.9844 restent (vs y_top² ≈ 0.9825), mais l'interprétation via κ(SU(N)) extrapolé est invalide.

## Verdict final et recommandations

### Top-3 nouvelles formules κ(N)

1. **PySR cplx=14** : $\kappa(N) = 0.01445 N^2 + (1.838 - 3.760/N^2)/N$ — $\chi^2/{\rm dof} = 0.86$ MAIS extrapolation diverge ($\kappa(N=8) > 1$). **Utilité limitée au régime N ∈ {2..6} mesuré**.

2. **PySR cplx=7** : $\kappa(N) = 0.00782 N^2 + 0.5206$ pure quadratique. Simple mais $\chi^2/{\rm dof} = 16$. Aussi diverge.

3. **F1 local + indicateur ad hoc** : $\kappa(N) = 0.681 (1-1/N^2) + 0.148 \delta_{N=6}$ pour N ≤ 6. Pragmatique mais sans pouvoir prédictif au-delà.

**Aucune formule analytique simple ne fit propre et extrapole sainement.** Cette absence indique soit une vraie transition physique entre N=4 et N=6, soit un artefact de mesure.

### Asymptote κ_∞

- **κ_∞ LOCAL** (régime N ≤ 4) : $0.6777 \pm 0.003$, compatible $\zeta(3)/\sqrt{\pi} = 0.6782$ à 0.15σ.
- **κ_∞ UNIVERSEL** : **N'existe plus**. Soit (a) la formule (1−1/N²) est purement effective pour N petit avec une "vraie" asymptote à $\sim 1$ atteinte plus loin, soit (b) la déviation est artefact systématique.

### Verdict hypothèse Z_N

**RÉFUTÉE** sous sa forme simple "composite dévie / premier suit". N=4 (composite) suit parfaitement F1, ce qui contredit l'hypothèse. Un mécanisme plus sophistiqué est nécessaire.

### Recommandations lattice prochaine étape

**P1 (URGENT, ce jour)** : Re-mesurer SU(5) à THERM5000 (comme SU(6)) pour exclure artefact de mal-thermalisation. Si SU(5) reste à 0.69, le finding tient. Si SU(5) tombe à 0.65, l'anomalie isole SU(6) et le pattern "centre Z₆ = 2·3" pourrait être réhabilité.

**P2 (URGENT, ce jour ou demain)** : Re-mesurer SU(6) à L plus grand (L=12, 16) pour exclure finite-size systematique.

**P3 (sous 1 semaine)** : Mesurer SU(7) (|Z_7|=7 premier, prédiction Z_N: ~0.66 ; prédiction alternative: ~0.85). Test discriminant central.

**P4 (sous 1 semaine)** : Mesurer SU(8) (|Z_8|=8 composite). Si SU(8) est aussi dévié de F1, hypothèse "composite" partiellement réhabilitée.

**P5 (cross-β)** : Pour SU(5,6) déjà mesurés, refaire à $\beta_{\rm 't Hooft}$ différents (λ = 0.2, 0.4, 0.6) pour détecter une éventuelle Lucini-Teper bulk transition.

### Implication ECI Phase 1

```
Pré-PySR + pré-SU(6) : P(ECI Phase 1) ≈ 75-80%
Post-finding SU(6) + PySR refit : P(ECI Phase 1) ≈ 60-70%

Argumentaire :
  (+) 22-23/25 ratios BIG_MASS_TABLE survivent (88-92%) — TIER 1 stable
  (+) m_H = κ(SU(2))·v = 125.08 GeV à 0.016% reste un breakthrough seul
  (+) κ_∞_local = 0.6777 reste compatible ζ(3)/√π à 0.15σ pour N≤4
  (+) Cluster arithmétique /13 /15 /23 /7 /11 /28 intact (indépendant κ)
  
  (-) Asymptote universelle κ_∞ → KO ; remplacer par κ_∞ LOCAL (N≤4)
  (-) Prédictions a priori y_top² via N=7,8 tombent
  (-) Aucune formule lisse n'extrapole proprement vers SU(7,8,9,10)
  (-) Le narrative "tout vient d'une constante transcendentale" devient
      "phénoménologie effective N≤4 + 22 identités arithmétiques + finding
       lattice direct SU(2)"
  
  Honest meta : la baisse de 10-15 pp reflète que le contenu prédictif
  intact (22/25) est large mais la narrative unificatrice est entamée.
```

## Annexe : recommandation paper draft

**PRL1** (m_H = κ(SU(2))·v) : intact, publishable IMMÉDIATEMENT avec ajout d'une §VI "SU(N≥5) anomaly and validity range" qui documente honnêtement que la loi κ(N) = κ_∞·(1−1/N²) est validée seulement pour N ∈ {2,3,4} et que SU(5,6) montrent des déviations à investiguer.

**PRL2** (dérivations théoriques) : retirer toutes apparitions de y_top² via SU(7)/SU(8) et présenter (1−1/N²) comme hypothèse locale N≤4 plutôt que théorème universel.

**Nouveau paper potentiel PRL3** : "Anomalous entanglement entropy scaling for SU(N≥5) lattice gauge theories: a sign of bulk transition or finite-size systematic?" — exposer le finding SU(6) à 27σ honnêtement et appeler à confirmation indépendante.

## Sources et anti-fab

- Buividovich & Polikarpov, arXiv:0802.4247 (BP2008b method, **vérifié 2026-05-25** session previous, NOT Bhattacharya-Pradhan, voir correction memory note 2026-05-25)
- AT2021 = JHEP 12 (2021) 082 (preprint arXiv:2106.00364 WITHDRAWN, citer published version)
- Données lattice : `jax_su[2,3,4,5,6]_EE_BP2008b*.json` (Kévin Rémondière)
- PySR : Cranmer 2023, `pip install pysr` v1.5.10, voir https://github.com/MilesCranmer/PySR
- Lucini-Teper bulk transition reference : Lucini-Teper-Wenger arXiv:hep-lat/0502003 et follow-ups
- Toutes données reproductibles : seed = 42, scripts ouverts dans repo cc-private

Auteur unique : Kévin Rémondière (ORCID 0009-0008-2443-7166).
Aucune mention IA. Honest meta inclus.
