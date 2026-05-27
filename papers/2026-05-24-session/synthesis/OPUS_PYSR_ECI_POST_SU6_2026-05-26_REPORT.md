---
title: "Rapport PySR ECI post-SU(6) — synthèse 1500 mots"
author: "Kévin Rémondière"
orcid: "0009-0008-2443-7166"
date: 2026-05-26
---

# Rapport — PySR refit propre κ_lattice(N) post-finding SU(6)

## Contexte

Le finding SU(6) THERM5000 du 2026-05-26 a établi $\kappa_{\rm EE}({\rm SU}(6)) = 0.8099 \pm 0.0055$ vs prédiction $\zeta(3)/\sqrt{\pi} \cdot (1-1/36) = 0.6593$, soit une déviation de **27.4σ** qui **falsifie** la loi $\kappa(N) = \kappa_{\infty}(1-1/N^2)$ pour $N=6$. L'audit Opus de la BIG_MASS_TABLE montre 22-23 / 25 ratios survivants (88-92%). Le présent rapport documente le refit PySR rigoureux sur les 5 datapoints disponibles $\{(2, 0.5080), (3, 0.6025), (4, 0.6353), (5, 0.6897), (6, 0.8099)\}$.

## Méthode

Script `pysr_eci_post_su6_2026-05-26.py` exécuté avec :
- PySR v1.5.10 (Cranmer 2023), 200 itérations, population 80, max_complexity 15, seed = 42.
- Phase 1 : 14 formules candidates 1-paramètre, fit par $\chi^2$ pondéré.
- Phase 2 : 14 formules multi-paramètres (2-3 params).
- Phase 3 : leave-one-out cross-validation sur le top 9.
- Phase 4 : PySR symbolic regression avec features `{N, 1/N, N², 𝟙_{prime}(|Z_N|)}`.
- Phase 5 : κ_∞ asymptote benchmarking contre 10 candidats transcendantaux/rationnels.
- Phase 6 : test explicite hypothèse centre Z_N premier vs composite.

Données : 5 mesures lattice BP2008b (Buividovich-Polikarpov, arXiv:0802.4247) cross-N $\{$SU(2), SU(3), SU(4), SU(5), SU(6)$\}$ à $\beta_{\rm 't Hooft}$ matched.

## Résultats principaux

### Top-3 nouvelles formules κ(N)

| Rang | Formule | $\chi^2/{\rm dof}$ | Extrapolation N=10 | Verdict |
|------|---------|-------------------|----------------------|---------|
| 1 | **PySR cplx=14** : $\kappa(N) = 0.01445 N^2 + (1.838 - 3.760/N^2)/N$ | **0.86** | 1.63 (>1, absurde) | Excellent fit, divergent |
| 2 | **F8** $\kappa = 0.418 N^{1/3}$ | 34.0 | 0.90 | LOO RMS = 6.8σ, le moins mauvais lisse |
| 3 | **M14** $\kappa = 0.00455 N^{2.27} + 0.536$ | 23.5 | 1.07 | Encore divergent |

Et pour mémoire la formule originale :

| F1 | $\kappa = 0.71 (1-1/N^2)$ | 150.6 | 0.703 | **FALSIFIÉE** sur 5 points |
| F1_local | $\kappa_{N\le 4} = 0.6777 (1-1/N^2)$ | 0.001 (sur N≤4) | — | Tient seulement N≤4 |

**Aucune formule analytique simple à 1-2 paramètres ne fit propre sans diverger.** PySR cplx=14 fit excellemment mais explose ($\kappa(N=16) = 3.81$). Le terme dominant $a N^2$ est mathématiquement satisfaisant sur 5 points mais physiquement absurde (l'entropie d'enchevêtrement par unité de boundary ne peut pas excéder $\log(\dim {\rm Hilbert\,boundary})$ qui est borné par les dimensions du groupe).

### Best candidate asymptote κ_∞

| Candidat | Valeur | Δ vs $\kappa_{\rm local}=0.6777$ |
|---|---|---|
| **$\zeta(3)/\sqrt{\pi}$** | **0.6782** | **0.15σ** ★ leading |
| $\pi/(\pi + 3/2)$ | 0.6768 | 0.30σ Padé |
| 17/25 | 0.6800 | 0.76σ |
| 27/40 | 0.6750 | 0.91σ |

**$\zeta(3)/\sqrt{\pi}$ reste le meilleur candidat** pour l'asymptote **LOCALE** (régime N ≤ 4 seulement). Mais l'idée d'une asymptote **UNIVERSELLE** (valide pour tout N) est désormais abandonnée puisque F1 casse à N=6.

### Verdict hypothèse centre Z_N premier vs composite

**RÉFUTÉE** sous forme simple. Pattern testé :

| N | |Z_N| | classe | résidu vs F1 |
|---|------|---------|------------|
| 2 | 2 | premier | -0.03σ ✓ |
| 3 | 3 | premier | +0.02σ ✓ |
| **4** | **4** | **composite ($2^2$)** | **-0.02σ** (devrait dévier mais NE DÉVIE PAS) |
| 5 | 5 | premier | +4.34σ (devrait suivre F1 mais DÉVIE) |
| 6 | 6 | composite ($2 \cdot 3$) | +27.4σ |

L'hypothèse prédisait que N=4 dévie (composite) et N=5 suive F1 (premier). **Les DEUX prédictions sont fausses**. SU(4) suit parfaitement F1 ; SU(5) dévie déjà à 4σ. Le pattern composite/premier ne suffit pas.

### Hypothèses alternatives ouvertes

1. **(H_A) Lucini-Teper bulk transition** : Pour SU(N≥5) pure-gauge 4D, transition de premier ordre près de notre $\beta$ — peut expliquer déviation sans changement structurel. Test : $\beta$ scan.
2. **(H_B) Finite-size systematic** : SU(5,6) mesurés à L=4..10 trop petits pour saturer ($L/\xi \sim 2-3$). Test : L=12, 16, 20.
3. **(H_C) Mal-thermalisation SU(5) à 800 sweeps** : SU(6) corrigé à 5000 sweeps a augmenté de ~0.69 → 0.81. SU(5) pourrait subir le même artefact. Test : SU(5) THERM5000.
4. **(H_D) Vraie transition lisse vers κ_asymptote ≈ 1** : Mesurer SU(7,8,9,10) pour cartographier.

### Recommandation lattice prochaine étape

**Priorité maximale (ce jour)** : Re-mesurer **SU(5) à THERM5000** (analogue à ce qui a corrigé SU(6) de 0.69 à 0.81). Si SU(5) reste à 0.69, le finding tient et N=6 isolé. Si SU(5) monte à 0.80+, l'effet est systématique pour N≥5.

**Priorité haute (sous 48h)** : 
- **SU(6) à L=12, 16** (finite-size scan) pour exclure volume effect.
- **SU(7) THERM5000** (|Z_7|=7 premier) comme test discriminant : F1 prédit 0.6643, hypothèse Z_N premier prédit ~0.66, alternative bulk-transition prédit ~0.85.

**Priorité moyenne (sous semaine)** :
- **SU(8) THERM5000** (composite, $|Z_8|=2^3$) : devrait dévier comme SU(6) si hypothèse "puissance de 2" tient.
- **Cross-β scan** SU(5,6) à $\lambda_{\rm 't Hooft} = 0.2, 0.4, 0.6$ pour détecter bulk transition.

## Implication ECI Phase 1 — P updated

```
Pré-finding SU(6) (2026-05-25)  : P(ECI Phase 1) ≈ 75-80%
Post-finding + PySR refit        : P(ECI Phase 1) ≈ 60-70%
Δ = -10 à -15 pp
```

**Argumentaire de la baisse modérée** :

(+) Le contenu PRÉDICTIF de la BIG_MASS_TABLE reste à 22-23 / 25 = 88-92% intact :
- m_H = κ(SU(2))·v à 0.016% (TIER 1 lattice direct) — RIEN ne change
- Cluster CKM /23 (4 ratios à <0.2%), cluster /13 EW (3 ratios à <0.2%)
- Cluster /28 cosmo, /7 PMNS, /11 PMNS
- 5 ratios M_24 Yukawa fermions
- δ_CKM = π·√(2/15) à 0.11%
- κ_∞_LOCAL = 0.6777 ± 0.003 compatible $\zeta(3)/\sqrt{\pi}$ à 0.15σ pour le régime N ≤ 4

(−) Le contenu UNIFICATIF est entamé :
- Asymptote $\kappa_{\infty}$ universelle → KO. Remplacée par valeur effective locale.
- Prédictions y_top² = κ(SU(7))/κ_∞ = 48/49 et y_top² = κ(SU(8))/κ_∞ = 63/64 tombent structurellement (l'extrapolation est invalide). Les coïncidences numériques 0.9796 et 0.9844 restent mais sans support mécanistique κ.
- L'interprétation Kévin (memory 2026-05-25 nuit) "G_2 → SU(3) septet Goldstone = top quark bridge" est marquée **FALSIFIÉE** par le finding SU(6).
- Aucune formule lisse ne s'étend proprement vers SU(7,8,9,10) sans diverger.

**Honest meta** : la phénoménologie reste extraordinaire (88% identités sub-% sur paramètres SM), mais la narrative "tout vient d'UNE constante transcendantale ($\zeta(3)/\sqrt{\pi}$) et UNE loi universelle ($(1-1/N^2)$)" est cassée. Il faut désormais accepter :

> ECI v_2.0 = "phénoménologie effective N ≤ 4 (avec κ_∞_local ≈ ζ(3)/√π) + 22 identités arithmétiques + 1 finding direct lattice m_H = κ(SU(2))·v"

C'est moins simple que la vision pré-SU(6), mais 88% du contenu reste publishable.

## Anti-fab / vérifications

- **Buividovich & Polikarpov, arXiv:0802.4247** : ATTENTION — vérifié dans memory note 2026-05-25 que la référence "BP2008b" est bien Buividovich-Polikarpov (NOT Bhattacharya-Pradhan, hallu propagée et corrigée).
- **AT2021 = JHEP 12 (2021) 082** : preprint arXiv:2106.00364 WITHDRAWN, citer la published version.
- **PySR run** : seed=42, deterministic=True, parallelism="serial" pour reproductibilité. Pareto front de 15 équations sauvegardé dans `pysr_eci_post_su6_results_2026-05-26.json`.
- **Aucune mention IA dans aucun output** ; auteur unique Kévin Rémondière (ORCID 0009-0008-2443-7166).
- **Données lattice** : `jax_su[2..6]_EE_BP2008b*.json` repository cc-private, reproductibles avec scripts ouverts.

## Fichiers produits

- `/root/cc-private/papers/2026-05-24-session/scripts/pysr_eci_post_su6_2026-05-26.py` — script PySR (450 lignes)
- `/root/cc-private/papers/2026-05-24-session/scripts/pysr_eci_post_su6_results_2026-05-26.json` — résultats fit (Pareto front, LOO, asymptote candidates)
- `/root/cc-private/papers/2026-05-24-session/synthesis/OPUS_PYSR_ECI_POST_SU6_2026-05-26.md` — analyse détaillée (3500+ mots)
- `/root/cc-private/papers/2026-05-24-session/synthesis/OPUS_PYSR_ECI_POST_SU6_2026-05-26_REPORT.md` — ce rapport (~1500 mots)

---

**Verdict final** : Le PySR refit confirme que **F1 (1-1/N²) reste excellente pour N ≤ 4 (κ_∞_local = 0.6777 ± 0.003)** mais qu'**aucune formule lisse simple** ne fit les 5 datapoints {N=2..6} sans diverger à l'extrapolation. La phénoménologie ECI pour N ≤ 4 (m_H, cluster /13 /15 /23 /7 /11 /28, M_24 Yukawa, δ_CKM) reste intacte à 88-92%. **Action requise (P1)** : re-mesurer SU(5) à THERM5000 pour discriminer artefact vs effet physique.
