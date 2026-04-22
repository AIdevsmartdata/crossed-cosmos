# Audit scientifique — document Claude app v2 « Le test ECI : aucune révolution, mais une reconstruction honnête »

**Date.** 2026-04-22.
**Auditeur.** Claude CLI (Opus 4.7) + Mistral Magistral-medium cross-check
+ calcul numérique local + WebSearch Crossref.

**Verdict global.** **MIXED — quelques bons apports, une régression majeure sur Eq.(1), et violation V6-4.**

Ce document est **honnêtement plus défendable** que le précédent (renonce au framing Einstein-level, admet "Horndeski augmenté TDA", résultat négatif robuste sur la numérologie). Mais il contient deux problèmes qui exigent rejet partiel :

1. **Form B proposée pour v6.1 est une régression** vs Form A (v6.2 HEAD). Perd la cohérence Fan 2022.
2. **Pred 1–4 sont cosmologiques** (H_0 tension, dispersion GW, CMB birefringence, S_8) — violation V6-4 répétée.

À intégrer néanmoins : **Piège 1 (dépendance de base de C_k)** et **Piège 2 (seuil Θ arbitraire)** sont des observations honnêtes, partiellement traitées dans notre v6.2 mais méritant clarification §2.

---

## 1. Numerical audit du Tableau 1 (12 relations)

Vérification Python avec CODATA 2022. H_0 = 67.4 km/s/Mpc, Σm_ν = 0.06 eV.

| # | Doc claim | Mon calcul | Verdict |
|---|---|---|---|
| 1 | Λ·ℓ_P² ≈ 10^-121.55 | log10(Λ·ℓ_P²) = -121.56 | ✓ identité Friedmann |
| 2 | (H_0/ω_P)² log = -121.86 | -121.858 | ✓ |
| 3 | Λ^(1/4) ≈ 2.24 meV | 2.240 meV | ✓ |
| 3b | ⟨m_ν⟩/Λ^(1/4) ∈ [2,10] | 20/2.24 = 8.93 | ✓ compatible upper bound |
| 4 | (F_π/M_P)^6 log = -120.7 | -120.726 | ✓ mais coïncidence |
| 5 | (m_e/M_P)^5 α^4 log = -120.4 | -120.439 | ✓ |
| 7 | ⟨H⟩ prédit 106 MeV (Gonzalo) | 39.4 MeV (non-red) | partiel — ordre OK, facteur 3 off |
| 7 | v_EW observé / prédit = 2300× | 6240× | **Doc sous-estime** le facteur |
| 8 | k_opt = 2.72 (m_e/M_P) | 2.723 | ✓ non-rationnel |
| 9 | Koide Q = 0.666664 | 0.666664 | ✓ |
| 11 | ℓ_DD(α=1) = 88 μm | 88.1 μm | ✓ |

**Conclusion #1 :** la plupart du Tableau 1 est numériquement correct. Les relations 1, 2, 3, 9, 11 sont de bonne qualité ; 4, 5 sont des coïncidences numérologiques sans contenu physique ; 7 confirme l'échec prédictif du dark-dimension pour ⟨H⟩ (6240×, encore pire que les 2300× annoncés par le doc — le doc sous-estime).

**Conclusion #2 :** le "résultat négatif robuste" (aucune relation inédite < 1% sur 64+ combinaisons) est vraisemblable. C'est un apport méthodologique honnête.

---

## 2. Form A vs Form B — régression sur Eq.(1)

Le document propose comme « correction minimale ECI v6.1 » :

**Form B (proposée)** :
$$\frac{dS_{\mathrm{gen}}}{d\tau_R} \le \frac{k_B}{\tau_R^*}\,\log\!\left(1 + \frac{C_k}{C_k^*}\right)\,\Theta(\mathrm{PH}_k[\delta n(\tau_R-\Delta, \tau_R)])$$

**Form A (v6.2 HEAD, déjà approuvée)** :
$$\frac{dS_{\mathrm{gen}}}{d\tau_R} \le \kappa_R\, C_k\, \Theta(\mathrm{PH}_k[\delta n])$$
avec la Proposition logistique tightening $\kappa_R C_k(1-C_k/C_k^{\max})\Theta$.

### Mistral Magistral cross-check (indépendant)

> « In the Fan 2022 scrambling limit where C_k → C_k^max ~ exp(S_R):
> - Form A predicts dS/dτ → 0, consistent with Fan's result.
> - Form B, with C_k ~ 2^n and C_k* = 2^n, results in log(1 + C_k/C_k*) ≈ log 2,
>   a **finite O(1) value, not saturating to 0**.
> **Verdict : Form B is a regression.** »

### Calcul explicite

Au plateau de scrambling avec C_k^max ~ exp(S_R) ~ 2^n (pour S_R ~ n·ln 2 nats) :
- Form A logistic : $C_k(1 - C_k/C_k^{\max}) \cdot \kappa_R \to 0$ ✓ cohérent avec $\dot C_K \to 0$ de Fan 2022
- Form B : $\log(1 + 2^n/2^n) = \log 2 \approx 0.69$, fini. **Incohérent avec Fan.**

### Verdict Form B

**RÉGRESSION.** Perte de la cohérence avec Fan 2022 que nous avons soigneusement établie en L2 de §5. Notre Proposition 1 logistic envelope capture cette saturation naturellement, Form B non.

---

## 3. Piège 5 (non-localité causale PH_k) — mauvaise compréhension

Doc écrit :
> « dS_gen/dτ est instantané ; PH_k[δn(τ)] est une fonctionnelle d'histoire (filtration globale). Mélanger dérivée instantanée et fonctionnelle d'histoire est structurellement incohérent sans fenêtre causale explicite [τ−Δ, τ]. »

### Examen

Dans v6.2 HEAD, la dequantisation map :
$$\delta n(x,\tau_R) \equiv \mathrm{Tr}_R[\rho_R(\tau_R)\hat n(x)] - \langle n\rangle$$

est un **champ scalaire spatial** défini à un τ_R fixé. PH_k[δn(·, τ_R)] calcule l'homologie persistante par **filtration sur les valeurs seuil** du champ (Yip 2024 pipeline), pas par filtration temporelle. Il n'y a **pas d'intégration d'histoire**.

Mistral confirme :
> « The persistent homology filtration PH_k is computed from **spatial data at fixed τ_R**, not from temporal history. Thus, the causal window does not genuinely apply. »

### Verdict Piège 5

**MAL-COMPRIS.** Le doc confond la filtration interne de PH (seuil sur δn) avec une filtration temporelle. Notre Eq.(1) n'a pas de problème de causalité temporelle. La fenêtre [τ-Δ, τ] ajoutée par Form B est non-nécessaire et introduit un paramètre libre Δ supplémentaire.

---

## 4. Prédictions 1-4 : toutes cosmologiques → V6-4 violation

Le doc propose **4 prédictions falsifiables à 3σ d'ici 2035** :

| # | Prédiction | Instrument | V6-4 status |
|---|---|---|---|
| 1 | Atténuation tension H_0 (ΔH_0/H_0 ~ 5-8%) | Planck + SH0ES + DESI + Euclid stacking | **COSMO** ❌ |
| 2 | Dispersion GW résiduelle | LISA 2035, Einstein Tel. | GW cosmo-adjacent ⚠ |
| 3 | CMB birefringence α_bir ≈ 0.3° | LiteBIRD 2032 | **COSMO** ❌ |
| 4 | S_8 growth modifiée 2-4% | Euclid 3×2pt + DES Y6 | **COSMO** ❌ |

PRINCIPLES.md V6-4 explicite :
> « D18/D18b killed the fσ_8 × Θ(PH_2) falsifier [...] v6 is a FORMAL paper, not a cosmology paper. Do NOT re-propose a cosmological prediction in the v6 draft. »

Aucune des 4 prédictions ne porte un pipeline D19+ (Fisher + marginalisation nuisances + cross-model). **Même faute méthodologique que le document Claude-app précédent.**

Notablement, le doc lui-même admet pour Pred 4 :
> « KiDS-Legacy 2025 semble cependant réduire la tension à moins de 1σ, affaiblissant cette prédiction. »

C'est un aveu : l'observation récente rend la prédiction moins testable. Classique signal d'un falsifieur mal-cadré.

**Verdict :** 4/4 rejetées pour v6, conformément à V6-4.

---

## 5. V7 « cohesive–SymTFT » — spéculation, pas pour v6

Le doc propose une extension v7 reposant sur :
- Gaitsgory-Raskin 2024 Langlands géométrique ✓ (vérification WebSearch : preuves multi-papiers arXiv:2405.03599 etc. existent)
- Freed-Moore-Teleman SymTFT arXiv:2209.07471 ✓ (bien connu)
- Chandrasekaran-Penington-Witten 2023 arXiv:2209.10454 ✓

Formulation conjecturale :
$$d_\tau S_{II}[\psi] \le \frac{k_B}{\tau_{\mathrm{mod}}} \cdot \ell_{\mathrm{Nielsen}}[\rho\to\sigma] \cdot \chi(\mathrm{PH}_\bullet[\mathrm{histoire}])$$

**Évaluation.** Le doc lui-même admet :
> « Structurellement attractif mais reste spéculatif : aucun théorème n'établit la dualité Kapustin-Witten en gravité au-delà de N=4 SYM sur Σ×C. »

**Verdict.** V7 est un programme de recherche à long terme, pas un paper JHEP-ready. **Pas à intégrer dans v6.** Peut être mentionné comme « future direction » dans l'Open questions §7.

---

## 6. Ce qui EST récupérable du document

### 6.1 Résultat négatif numérologique (apport solide)

Le scan systématique (a,b,c) ∈ [-4,4] sur 64+ combinaisons de {H_0, Λ, m_e, m_p, m_ν, v_EW, Λ_QCD, F_π, α} normalisées par M_P, sans match < 1% inédit, est **une contribution méthodologique honnête**. Peut alimenter un paragraphe §6.3 de notre v6 outlook (en deuxième révision, pas bloquant) ou un appendix computationnel.

### 6.2 Observations sur les pièges 1 et 2

**Piège 1** (C_k dépend de la base de portes, équivalence polynomiale seulement — Brown 2024 Quantum 8, 1391) : est une critique légitime. Notre v6.2 M1' identifie déjà C_k à la spread complexity de Caputa 2024 sous flot modulaire, ce qui fixe une base canonique. **À préciser** dans §2 par une phrase du type : « The k-design/spread complexity identification canonically fixes the gate base up to a polynomial equivalence (Brown 2024) ; the inequality is preserved under this rescaling. »

**Piège 2** (seuil Θ implicite) : déjà adressé par M3 CONJECTURAL + α ∈ (0, 0.1]. OK.

### 6.3 κ_C = 2π k_B/ℏ comme « principe-borne », pas CODATA

Le doc reconnaît honnêtement :
> « κ_C n'est pas une constante fondamentale indépendante. [...] C'est un principe-borne, pas une constante CODATA au sens strict. »

C'est exactement ce que notre §6.2 dit déjà. Aucune action requise.

---

## 7. Recommandation finale

### Ce qui est REJETÉ

- **Form B v6.1** (log envelope) → régression Fan 2022, rejetée
- **Fenêtre causale [τ-Δ, τ]** → mal-comprise, non-nécessaire
- **Prédictions 1-4 cosmologiques** → V6-4 violation
- **Extension v7 cohesive-SymTFT** → spéculative, non-JHEP-ready

### Ce qui est INTÉGRABLE (optionnel, non-bloquant)

- **Note §2** clarifiant que l'identification spread-complexity fixe canoniquement la base de portes (Brown 2024 équivalence polynomiale)
- **Appendix ou §6.3 extension** mentionnant le résultat négatif numérologique comme motivation supplémentaire pour le focus formal-algébrique
- **§7 Open questions additions** mentionnant SymTFT et Langlands géométrique comme « far-future structural extensions »

### Ce qui ne change pas

v6.2 HEAD (`3aecf2f`) reste draft de référence. Zenodo `10.5281/zenodo.19699006` reste valide. Pas de retag nécessaire.

### Décision auto

Je n'applique AUCUN changement au tex v6 ce tour. Si l'owner veut intégrer les 3 éléments optionnels ci-dessus, je peux écrire le patch — mais la v6.2 actuelle passe déjà adv-v3 SHIP et 18/18 pipeline. Toucher pour ajouter des « fioritures honnêtes » peut rouvrir des risques minor.

**Verdict clarifié :** Ce document Claude-app n'oblige aucune modification du v6 déployé. Il renforce notre confiance que les décisions V6-1 et V6-4 sont correctes (Form A logistic > Form B log, et pas de falsifieur cosmo sans D19 pipeline).

---

## Annexe — Verification des citations load-bearing du doc

| Citation | arXiv | Vérification |
|---|---|---|
| Montero-Vafa-Valenzuela 2022 | 2205.12293 | ✓ |
| Gonzalo-Montero-Obied-Vafa 2022 | 2209.09249 | ✓ JHEP 11 (2023) 109 ; ⟨H⟩ ~ Λ^(1/6) M_Pl^(1/3) confirmé |
| CMS W mass 2024 | 2412.13872 | ✓ 80360.2 ± 9.9 MeV |
| CODATA 2022 (Mohr) | 2409.03787 | non-vérifié direct, cohérent |
| Haferkamp 2022 Nat Phys | 2106.05305 | ✓ (déjà bib) |
| Maldacena-Shenker-Stanford | 1503.01409 | non-vérifié, ultra-standard |
| Jacobson 2016 | 1505.04753 | ✓ (wishlist v6) |
| Bianconi 2024 | 2408.14391 | ✓ (bib v6.2) |
| Minami-Komatsu 2020 | 2011.11254 | non-vérifié direct |
| SH0ES 2022 | 2112.04510 | non-vérifié direct, standard |
| Planck 2018 | 1807.06209 | standard |

Aucune citation fabriquée détectée (contrairement au Lange-2021 du doc précédent).
