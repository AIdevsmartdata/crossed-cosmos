# DECODER_GRAPH v11 — notes narratives (ponts formule↔mesure)

**Date** : 2026-06-24
**Fichier** : `/root/cc-private/papers/DECODER_GRAPH_v11.json`
**Base** : v10 (`/root/cc-private/papers/DECODER_GRAPH_v10.json` = 104 nœuds / 151 arêtes).
**Objet** : matérialiser les **ponts formule↔mesure** entre les deux programmes (ECI/h∨/Deligne/κ_FP côté formule, Kevinotron côté mesure), avec des **tiers honnêtes**.
**Mode** : MÉCANISME-PAS-NUMÉROLOGIE. Tout pont = une ÉQUATION dans le `label` reliant une mesure à une formule via un mécanisme dérivable (CONFRONTE ou ALIMENTE). Avec ≤3-5 groupes mesurés, tout « trend cross-groupe » est `insufficient-N` (jamais EXACT sur un fit).
**Compute** : VPS local, 0 GPU. GPU gamer = PROD F4 Ns24 (intouché). Aucun kevinotron lancé. Aucun git pull/commit/push/stash.

---

## Compteurs

| | v10 | **v11** | Δ |
|---|---|---|---|
| Nœuds | 104 | **115** | **+11** |
| Arêtes | 151 | **172** | **+21** |
| Arêtes pendantes | 0 | **0** | — |

`top_betweenness` / `top_degree` de v10 ont été **retirés** de v11 (ils seraient périmés avec +11 nœuds/+21 arêtes ; champ `centrality_note` ajouté pour le signaler — recalcul networkx si besoin).

Décomposition des **+11 nœuds** : 5 théorie-formule (`coeff_E_Dynkin`, `Deligne_series`, `large_N_dof_dimadj`, `glueball_ratio_universal`, `Tc_sqrtsigma_LTW`) + 1 ancre-formule (`dim_adj_C2_2hvee`) + 5 mesures (`L_h_Tc4_G2`, `sqrt_sigma_G2_SU3`, `w0_F4_pending`, `w0_SO7_pending`, `w0_E6_pending`).

Décomposition des **+21 arêtes** : 1 RETRACTS (ratio_6_5 via hygiène) + 20 ponts/prédictions (EXACT/STRUCTURAL/PARTIAL/PREDICTS/FEEDS/TESTS/MEASURES). **6 arêtes v10 re-taguées** (5 → RETRACTS pour numérologie, 1 → label corrigé pour l'erratum κ_FP).

---

## 1. Le SEUL pont EXACT formule↔mesure du projet : coeff E (Dynkin)

Nouveau nœud-théorie **`coeff_E_Dynkin`** : `a⁴E = (6·d_fund/T_F)·(1−⟨P⟩)`, coeff = `6·d_fund/T_F` (T_F = indice de Dynkin du fondamental ; T_F(SU(N))=½ ⇒ 12·d_fund). Identité de groupe `Tr_R(F F)=T_R·(G^a G^a)`, **PAS un fit**. Réfs vérifiées : Lüscher **1006.4518** (t²⟨E⟩=0.3, échelle t0), BMW **1203.4469** (échelle w0). Refs LTW/RRS : **hep-lat/0307017**, **2506.15509**. Deligne : Landsberg-Manivel **math/0107032**.

Arêtes :
- `coeff_E_Dynkin --VALIDATES--> w0_G2_coeffE42` (**EXACT**) : G2{7} T_F=1 ⇒ 42, validé bout-en-bout (84→ratio w0/√t0=2.73 FAIL ; 42→ratio∈[1.10,1.17] sur β9.76/9.85/10.0/10.2). **Caveat honnête** : le ratio w0/√t0 est INVARIANT sous un rescaling pur ; il discrimine seulement parce qu'un mauvais coeff pousse le croisement-0.3 fixe en région-artefact. La PREUVE est l'identité de Dynkin ; le lattice fournit une confirmation de cohérence (croisement dans le plateau).
- `coeff_E_Dynkin --PREDICTS--> w0_F4_pending (52)`, `w0_SO7_pending (42)`, `w0_E6_pending (54)` : dérivés (T(26,F4)=3, T(7,B3)=1, T(27,E6)=3) mais **lattice-UNTESTED** → type `PREDICTS`, label `[insufficient-N]`, JAMAIS EXACT.
- `h_dual_coxeter --STRUCTURAL--> coeff_E_Dynkin` : T_F clé sur la même normalisation Casimir/Dynkin où T_adj=h∨. **Hub-keyed mais DISTINCT de la série Deligne dim_g** (anti-mis-attribution).

⚠️ **Caveat câblage (porté du lane wilsonflow)** : l'override n'est PAS dans le miroir de base (`wilson_flow.rs:269` = `12·d·(1−P)`=84 pour tous). G2=42 fut un override EXPLICITE du run de prod ; F4=52 n'est qu'un nombre dérivé. « G2=42 câblé » n'est vrai que pour le build de prod, pas la source de base.

---

## 2. Les ponts STRUCTURAL (mécanisme réel, mais 1 point exceptionnel)

### 2.1 σ_cd / L_h ∝ dim(adj) (comptage de dof de gluon, RRS)

Nouveau nœud `large_N_dof_dimadj` : `σ_cd/Tc³=0.0182N²−0.194`, `L_h/Tc⁴=0.360N²−1.88` (RRS 2506.15509, jusqu'à N=10). Le N² = comptage de dof de gluon = **dim(adj)+1, PAS h∨**.
- `large_N_dof_dimadj --STRUCTURAL--> σ_cd_Tc3_G2` : G2 mesure 0.125 vs loi-SU(N)@N=h∨=4 = 0.097 → **~25-30 % AU-DESSUS** = off-curve exceptionnel. **insufficient-N** (1 point Kevinotron), jamais EXACT.
- `large_N_dof_dimadj --STRUCTURAL--> L_h_Tc4_G2` : G2 3.7-4.9 ~ SU(4) RRS(N=4)=3.88 COMPATIBLE mais 1 point + R_β-dépendant.
- `dim_adj_C2_2hvee --STRUCTURAL--> large_N_dof_dimadj` : le N² est dim(adj), pas h∨ — pour SU(N) ils diffèrent de O(1) → **indistinguables sur la courbe SU(N)**.

**Numérologie RETIRÉE (correction de discipline)** : « σ_cd(G2)≈σ_cd(SU4) PILE / 14 vs 15 générateurs » reposait sur le **σ_cd(G2,Nt6)=0.144 PÉRIMÉ**. Le durci 0.124-0.126 met G2 ~25-30 % au-dessus de la loi SU(N) → la coïncidence TOMBE. **Aucune arête h∨→σ_cd créée** (le scaling est dim(adj), pas h∨).

### 2.2 dim(adj) / C₂(adj)=2h∨ autonome

Nouveau nœud-ancre `dim_adj_C2_2hvee` (était seulement à l'intérieur de `h_dual_coxeter`). Arêtes : `--STRUCTURAL--> h_dual_coxeter` (les deux faces du Casimir adjoint), `--STRUCTURAL--> Anderson_F4_26_chGOE` (dim(adj) fixe la taille de matrice Dirac {26}/{52}/{7} ; input structurel, pas un fit).

### 2.3 Deligne/Vogel = STRUCTURAL-ONLY, ZÉRO arête de mesure

Nouveau nœud-théorie `Deligne_series` : `dim g=2(5h∨−6)(h∨+1)/(h∨+6)` + master field m₂^∞(τ). Une seule arête : `--STRUCTURAL--> h_dual_coxeter`. **Aucune arête mesure↔Deligne** (en créer serait la numérologie interdite). dim_g est un INPUT, pas une mesure ; m₂(τ) est de l'analytique 2D-YM exacte que le 4D dilue ; le 27 et le 10/3 sont des coïncidences adjugées. Parmi les groupes lattice, ON-line = SU3,G2,F4,E6 ; OFF-line = SU4,SU5,Sp4(C2),SO7(B3). Le coeff E=42 appartient à la famille **Dynkin/h∨**, PAS Deligne (flaggé pour éviter la mis-attribution).

---

## 3. Le pont PARTIAL : b₀∝h∨ → running → w0/R_β (κ_FP/b₀ lane)

- `b_0=11N/(48π²) --PARTIAL--> w0_G2_coeffE42` : `b₀=(11/3)C₂(adj)/(16π²)=(11/3)·2h∨/(16π²)∝h∨` (textbook-exact). R_β(G2)=−0.95±0.11 confronte la pente 1-loop. **MAIS N=1 groupe propre** (w0 propre = G2 seul ; le « w0(SU3)=1.092 » du disque est un sous-produit de validation-flow, pas une mesure-échelle de physique) → `insufficient-N`, JAMAIS EXACT.
- `h_dual_coxeter --STRUCTURAL--> b_0=11N/(48π²)` : le hub dual-Coxeter fixe le coeff 1-loop.
- `h_dual_coxeter --STRUCTURAL--> κ_FP=1/6` : κ_FP=1/(2h∨) (erratum) — même invariant que b₀∝2h∨, mais **canal FP/gap sans observable lattice** → STRUCTURAL, confronté seulement par l'auto-cohérence d'un futur trend R_β(h∨).

**Fermeture (CPU-now)** : un scan w0(SU3) propre à ≥2 β → N=2 ; puis w0(F4) après Ns24 (GPU) → N=3 = 1er vrai trend (reste PARTIAL sur 3 points).

---

## 4. Les ponts TESTS (universalité confrontée, mais donnée escrow/incohérente)

- `glueball_ratio_universal --TESTS--> m0pp_G2_escrow` : m_0++/√σ≈3.4 universel ; G2 mesure 1.2 = **ESCROW** (mur de précision isotrope, ~2.9× sous l'universel, PAS continuum) → ne confronte PAS la formule, garder ESCROW.
- `Luscher_string --TESTS--> sqrt_sigma_G2_SU3` et `Tc_sqrtsigma_LTW --TESTS--> sqrt_sigma_G2_SU3` : √σ·a SU3=0.225, G2=0.335 (β9.7, **PAS 0.30 — c'était un β différent** ; **F4=0.51 NON-reproductible EXCLU/retracté**). 2 groupes → insufficient-N. **Tc/√σ NON formable en l'état** : Tc(G2) et √σ(G2) à `a` différents (incohérent dimensionnellement) → closable seulement en unités w0 communes.

---

## 5. RETRACTS : numérologie identifiée par L3

| Pont v10 | type v10 | type v11 | Raison |
|---|---|---|---|
| `ratio_6_5_fermion_gauge → fermion_det_scan` | DERIVES | **RETRACTS** | 1.20=6/5 = coïncidence d'entier mono-groupe SU(3), no mechanism |
| `ratio_6_5_fermion_gauge → KEVINOTRON_FORMULA` | BRIDGES | **RETRACTS** | « 6/5 fermion/gauge » = numérologie, aucun map log|det(D)|/S₂→gen×chiral/d_fund |
| `ratio_6_5_fermion_gauge → SECTOR_Yukawa` | STRUCTURAL | **RETRACTS** | « 6/5=(3gen×2chiral)/d_fund encode flavor » = collision d'inputs SM |
| `fermion_det_scan → KEVINOTRON_FORMULA` | EXTENDS | **RETRACTS** | log|det|/N≈1.2·S₂/A = même coïncidence 1.2, no mechanism |
| `neg_evals_formula → Gribov_1327_neg` | DERIVES | **RETRACTS** | |Φ⁺|²×N/d≈1327 fit combinatoire ; n_neg=0 partout post-bugfix = artefact |

Le nœud `ratio_6_5_fermion_gauge` reçoit `tier=RETRACTED_numerology`, `status=FALSIFIED`. Nouvelle arête `integer_collision_hygiene --RETRACTS--> ratio_6_5_fermion_gauge`. Le `value` du nœud-hygiène est mis à jour pour lister ratio_6_5 et neg_evals=1327.

**Coefficient `(π+e)` de KEVINOTRON_FORMULA** : NON rétracté (le `−h∨` validé 9 groupes et `β−|Φ⁺|` PySR/Weyl sont des ponts légitimes), mais le préfacteur (π+e)≈5.859 reste un **coefficient empirique non dérivé décoratif** — ne jamais le présenter comme EXACT (note de discipline, pas une modification d'arête en v11).
**`screening_law_PySR`** : reste, mais c'est un **fit sur-paramétré 8 groupes** (4.04/1.28/0.31/2.36), pas une loi mécaniste (note de discipline ; `slope_monotone_screening` est la version qualitative-correcte).

---

## 6. Fix de staleness : erratum κ_FP

L'arête `mass_gap_geometric → κ_FP=1/6` portait encore le label PÉRIMÉ « κ_FP = 1/(2|Φ⁺|) » (FAUX pour G≠SU(3)). Corrigée en `USES` avec label « κ_FP = 1/(2h∨) (ERRATUM 2026-06-01 ; =1/6 pour SU3 où |Φ⁺|=h∨=3 ; NOT 1/(2|Φ⁺|) pour G≠SU3) ». La valeur 1/6 du nœud reste juste pour SU(3) ; le `note` du nœud porte la table cross-groupe (SU2=1/4, SU4=1/8, G2=1/8, Sp4=1/6, SO7=1/10, F4=1/18, E6=1/24).

---

## 7. Verdicts par lane (synthèse)

| Lane | Observable | Verdict | Pont v11 |
|---|---|---|---|
| **wilsonflow** | coeff E → w0 (G2) | **EXACT** | `coeff_E_Dynkin --VALIDATES--> w0_G2_coeffE42` |
| **wilsonflow** | coeff E (F4/SO7/E6) | **PREDICTS** (untested) | `coeff_E_Dynkin --PREDICTS--> w0_{F4,SO7,E6}_pending` |
| **kappaFP_b0** | b₀∝h∨ → running/R_β | **PARTIAL** (N=1) | `b_0 --PARTIAL--> w0_G2_coeffE42` |
| **kappaFP_b0** | κ_FP=1/(2h∨) | **STRUCTURAL** (no obs.) | `h_dual_coxeter --STRUCTURAL--> κ_FP=1/6` |
| **hscaling** | σ_cd/Tc³ ∝ dim(adj) | **STRUCTURAL** (1 pt off-curve) | `large_N_dof_dimadj --STRUCTURAL--> σ_cd_Tc3_G2` |
| **hscaling** | L_h/Tc⁴ ∝ dim(adj) | **STRUCTURAL** (1 pt) | `large_N_dof_dimadj --STRUCTURAL--> L_h_Tc4_G2` |
| **hscaling** | Tc/√σ (LTW) | **REJET** (a-mismatch) | TESTS via `sqrt_sigma_G2_SU3` (non formable, caveat) |
| **hscaling** | m_0++/√σ ≈ 3.4 | **TESTS** (G2=escrow) | `glueball_ratio_universal --TESTS--> m0pp_G2_escrow` |
| **hscaling** | Anderson ⟨r⟩ | **STRUCTURAL classe** (déjà EXACT v10 via AZ) | inchangé ; `dim_adj_C2_2hvee --STRUCTURAL--> Anderson` (taille matrice) |
| **deligne** | dim_g / master field | **STRUCTURAL-only** (0 mesure) | `Deligne_series --STRUCTURAL--> h_dual_coxeter` |
| **deligne** | σ_cd(G2)≈σ_cd(SU4) | **REJET** (0.126≠0.097, ~30 %) | aucune arête créée |
| **L3 audit** | ratio 6/5, neg_evals 1327 | **RETRACTS** | 5 arêtes re-taguées RETRACTS |

**Règle FER appliquée** : zéro EXACT déclaré sur un fit cross-groupe (le seul EXACT, coeff E, est une identité de Dynkin mono-mesure validée, pas un fit). Toute arête PARTIAL porte `insufficient-N`. Aucune arête sans équation dans le label. 0 arête pendante.

---

## Fichiers écrits

- `/root/cc-private/papers/DECODER_GRAPH_v11.json` (115 nœuds / 172 arêtes, 0 pendante)
- `/root/cc-private/papers/DECODER_GRAPH_v11_NOTES_2026-06-24.md` (ce fichier)

**Refs arXiv vérifiées (lanes)** : 1006.4518 (Lüscher t0), 1203.4469 (BMW w0), hep-lat/0307017 (LTW Tc/√σ), 2506.15509 (RRS σ_cd/L_h), math/0107032 (Landsberg-Manivel Deligne). Erratum κ_FP=1/(2h∨) : interne `ERRATUM_kappaFP_dualCoxeter_2026-06-01.md`.

Aucun commit/push. Repo non perturbé.
