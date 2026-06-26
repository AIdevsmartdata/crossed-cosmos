# DECODER_GRAPH v13 — notes de version (2026-06-26)

**Base :** v12 (125 nœuds / 192 arêtes, `DECODER_GRAPH_v12.json`).
**v13 :** **142 nœuds (+17) / 232 arêtes (+40)**, 0 arête pendante, 0 self-loop, 0 label vide, JSON valide.
**Source de vérité :** `~/crossed_cosmos_notes/PREREG_HYPOTHESES_FALSIFIABLES_2026-06-24.md` (H7, H15, H16, H25, H26/D2) + `finding_anderson_az_complete_2026-06-25` (D1, D2, D3, D6, AUDIT) + `finding_sigcd_llr_pivot_2026-06-25` (PIVOT).
**Mode :** MÉCANISME-PAS-NUMÉROLOGIE. Tiers HONNÊTES (DERIVED / SCALING-pas-théorème / PARTIAL / INCONCLUSIVE / CONJECTURAL).
**Mantra de portée :** tout reste dans le secteur de jauge confiné ; les portes GW restent CONSTRAINS/sub-LISA (héritées) ; H7 AJOUTE le résultat NÉGATIF (impossibilité multi-messager).
**0 GPU / 0 gamer / 0 prod touché. 0 commit / 0 push (proposé, à faire après le gate par Kévin).**

---

## NŒUDS AJOUTÉS (17 = 6 équations + 11 résultats/audits/pivot)

### 6 nœuds ÉQUATION (`kind="equation"`)
| id | formule | gouverne |
|---|---|---|
| `EQ_FS_indicator` | ν(R)=(1/|G|)∫χ_R(g²)dg ∈ {+1,0,−1} ; T²=ν | la classe AZ (D1, Altland_Zirnbauer) |
| `EQ_Sigma2_2_beta_pi2` | Σ²(L)≈(2/β π²)·ln L = 0.2026/0.1013/0.0507 | D2 (test rigidité longue-portée H26) |
| `EQ_master_field_m2inf` | m₂^∞(τ)=−e^{−τ}+27e^{−5τ/3}−(25+10τ)e^{−2τ} | CLT_Deligne, Deligne_series, H15, H16 |
| `EQ_kappa_FP_1_2hdual` | κ_FP=1/(2h∨) | κ_FP=1/6 (SU3), mass_gap_geometric |
| `EQ_coeff_E_6dfund_TF` | a⁴E coeff = 6·d_fund/T_F | coeff_E_Dynkin, w0_G2_coeffE42 |
| `EQ_RRS_sigcd_N2` | σ_cd/Tc³=0.0182N²−0.194 (RRS) | large_N_dof_dimadj, D6, σ_cd_Tc3_G2 |

Chaque équation est reliée **aux mesures/résultats qu'elle gouverne** (pas une coïncidence). Les constantes 27 & 10/3 de `EQ_master_field_m2inf` sont explicitement étiquetées **coïncidences arbitrées, PAS octonioniques/decoder** (héritage du caveat `Deligne_series`).

### 5 dérivations D1–D6 (`discovery`/`correction`/`theory`)
1. **`FS_indicator_AZ_flip`** (D1, discovery, DERIVED referee-SOUND) — l'indicateur de Frobenius-Schur ν → classe AZ ; **dérive le flip T²=ν** (D→bloc even-odd W→T anti-unitaire, intertwineurs 1e-15, pivot σ_Dirac=−1). Élève Anderson de « théorème CITÉ » à « mécanisme DÉRIVÉ+VÉRIFIÉ ». Caveat : reproduction de Verbaarschot, PAS un théorème neuf.
2. **`Sigma2_log_coeff_AZ`** (D2, discovery, DERIVED SOUND) — coeff log Σ²(L)=2/(βπ²) (GUE exact 1/π², GOE/GSE <0.05 %). Test H26 : **4 PASS / 3 INCONCLUSIVE / 0 FAIL** (les 4 reps réelles → chGOE à longue portée ; G2 sur-claime → vraie provenance G2 = ⟨r⟩=0.534).
3. **`CLT_Deligne_conjectural`** (D3, correction) — le referee a **ÉCHOUÉ le CLT fort ce tour** : CLT FAIBLE seulement (κ_{k≥3}→0 numérique au bruit ~3-4e-3, pas exact), **champ-maître CONJECTURAL**. NE PAS lire comme prouvé. → `UPDATES` CLT_Deligne (tempère).
4. **`sigcd_scaling_dimadj_077`** (D6, theory, SCALING TIER-4 PAS théorème) — argument réduction-dimensionnelle : la théorie **penche dim(adj) → σ_cd/Tc³(F4)≈0.77** (vs h∨²→1.28). Kill-test pré-enregistré (<0.95 confirme dim(adj), >1.1 le tue). Réserves : RRS=FIT, R²=1 sur SU(N) **tautologique**, seul le F4 non-mesuré discrimine.

### 4 hypothèses falsifiables (H7, H15, H16, H25)
5. **`H15_master_field_deterministic`** (discovery, **PARTIAL**) — corrélateurs multi-aires adjoints 2D-YM EXACTS (validés MC SU(2)). Le KILL non-gaussien N'est PAS atteint, MAIS la prédiction « le 2-point connecté SURVIT » est **RÉFUTÉE** : conn2~h^{−1.43}→0, var(W)~1/h→0 → la limite stricte est un **champ-maître DÉTERMINISTE**, PAS un champ libre. Referee : FLAWED (label sur-vendu, rétrogradé).
6. **`H15_free_field_2D`** (prediction, **RETRACTED/FALSIFIED**) — le sur-claim « champ libre 2D, propagateur 2-pt survivant ». Cible du `RETRACTS` de H15 (miroir du patron Edgeworth de v12).
7. **`H16_gaussianity_universal`** (discovery, **PASS** referee-SOUND) — la gaussianité s'étend au **fondamental** (G2{7}…E8{248}) : sup|m₃|↓ exposant +1.17 = même classe d'échelle que l'adjoint, MÊME m₂^∞(τ). Gaussianité **UNIVERSELLE** (fond+adj), PAS adjoint-spécifique. Caveat : SCALING numérique, pas théorème.
8. **`H7_grav_impossibility`** (discovery, **PASS** compute-zéro) — les **3 portes gravitationnelles Λ_D collapsent sur UN seul ξ** : f_peak~ξ⁻³, Ωh²~ξ⁰ (impuissante, sub-LISA), σ/m~ξ⁺⁹, ΔNeff~ξ⁺⁴ (exposants sympy EXACTS, DeepSeek 0 loophole). = 1ère carte d'exclusion multi-messager d'un ξ sombre G2 = **résultat NÉGATIF publiable**. FMS 1605.08048 (vérifié).
9. **`H25_betac_circular`** (measurement, **INCONCLUSIVE**) — β_c(G2,Nt4)≈9.3, β_c(F4,Nt4)≈32, ratio brut 3.44 ≈ dim(adj) 3.71 MAIS **test circulaire** : β_c brut porte β_norm=dim_fund, et **dim(adj)=2·dim_fund EXACT** pour G2/F4 → dégénéré avec la normalisation. Discriminant requis = Tc/√σ au β_c (non calculable sur l'existant).

### 2 nœuds transverses (AUDIT + PIVOT)
10. **`Reliability_audit_2026-06-25`** (correction, CRITICAL paper-level) — (a) **⟨r⟩ mesure l'indice de Dyson β, PAS la chiralité** ; label Cartan = THÉORIE-assigné ; hard-edge = sonde chirale → re-scope manuscrit. (b) **E6 0.2σ INNOCENTÉ 🟢** : dérive reproject MESURÉE ~3.14e-14(E6)/1.37e-14(F4) ≪ menace 0.006 (fix#2). (c) barres block-jackknife+τ_int → verdicts survivent 13/13. **3 maillons faibles** : Anderson=provenance G2 (#1 levier de rejet, physique survit), Deligne=CLT conjectural extrapolé, thermo=stats Ns24 (BIC ~6 cfg → major-revision pas PRL).
11. **`Pivot_sigcd_LLR`** (discovery, METHOD-PIVOT) — σ_cd(F4) **NON mesurable direct** (1er-ordre FORT : ΔP≈0.23, gap d'action 3.8σ Ns24, barrière ∝σ·Ns²) → **pivot LLR** (ρ(E), a(E)=d ln ρ/dE). Phase A PARTIAL : méthode marche sur F4 (a(E_eq)→−β/26=−1.192 à ~3 %), mais perf-bound. **G5 (par_iter_mut windows) ×9.2 @16t, déterministe==sériel bit-pour-bit. G2/G3 SOUND** (centrage réparé le wall-pinning, a→−β/7 à −0.2…−0.7 %). Phase B (σ_cd CONNU sur G2/SU3) = INCONCLUSIVE (infra, pas bug ; gamer offline ~06:00 26 juin). Clone ISOLÉ, NON mergé.

---

## ARÊTES AJOUTÉES (40) — chaque label porte une équation/mécanisme

**Équations → ce qu'elles gouvernent (13) :**
- `EQ_FS_indicator --DERIVES--> FS_indicator_AZ_flip` ; `--STRUCTURAL--> Altland_Zirnbauer`
- `EQ_Sigma2_2_beta_pi2 --DERIVES--> Sigma2_log_coeff_AZ`
- `EQ_master_field_m2inf --STRUCTURAL--> {CLT_Deligne, Deligne_series}`
- `EQ_kappa_FP_1_2hdual --DERIVES--> κ_FP=1/6` ; `--STRUCTURAL--> {h_dual_coxeter, mass_gap_geometric}`
- `EQ_coeff_E_6dfund_TF --STRUCTURAL--> coeff_E_Dynkin` ; `--VALIDATES--> w0_G2_coeffE42`
- `EQ_RRS_sigcd_N2 --STRUCTURAL--> {large_N_dof_dimadj, σ_cd_Tc3_G2}` ; `--PREDICTS--> sigcd_scaling_dimadj_077`

**Dérivations D1/D2 (DERIVES/CONFIRMS) :**
- `FS_indicator_AZ_flip --DERIVES--> AZ_reality_class` (D1 ancre le mécanisme) ; `--STRUCTURAL--> SU3adj_chGOE` (le flip = signe de ν)
- `Sigma2_log_coeff_AZ --CONFIRMS--> AZ_reality_class` (longue portée) ; `--STRUCTURAL--> Anderson_F4_26_chGOE` (F4 triple-PASS)

**Tempérage / supersede (UPDATES) :**
- `CLT_Deligne_conjectural --UPDATES--> CLT_Deligne` (conjectural) ; `--STRUCTURAL--> EQ_master_field_m2inf`
- `sigcd_scaling_dimadj_077 --STRUCTURAL--> large_N_dof_dimadj`

**Falsification H15 (RETRACTS) :**
- `H15_master_field_deterministic --RETRACTS--> H15_free_field_2D` (conn2→0, pas de propagateur)
- `H15_master_field_deterministic --STRUCTURAL--> {CLT_Deligne, EQ_master_field_m2inf}` (déterministe ; gaussien seulement après rescaling)

**Universalité H16 (CONFIRMS) :**
- `H16_gaussianity_universal --STRUCTURAL--> CLT_Deligne` ; `--CONFIRMS--> EQ_master_field_m2inf` (même m₂^∞)
- `Deligne_gaussian_CLT --STRUCTURAL--> H16_gaussianity_universal` (fille de H10)

**Impossibilité gravitationnelle H7 (3 portes) :**
- `H7_grav_impossibility --STRUCTURAL--> {GW_sound_shell (porte A ξ⁰), EXP_SIDM_Bullet (porte B ξ⁺⁹), EXP_CMB_S4 (porte C ξ⁺⁴), SECTOR_DARK}`

**Circularité H25 :**
- `H25_betac_circular --STRUCTURAL--> {dim_adj_C2_2hvee (dim(adj)=2·dim_fund dégénéré), F4_thermo_betac_Nt4 (β_c≈32)}`
- `Tc_sqrtsigma_LTW --TESTS--> H25_betac_circular` (le discriminant Tc/√σ, non calculable)

**Audit fiabilité :**
- `Reliability_audit_2026-06-25 --UPDATES--> AZ_reality_class` (β mesuré, Cartan théorie-assigné) ; `--VALIDATES--> Anderson_F4_26_chGOE` (E6/F4 innocentés 🟢) ; `--STRUCTURAL--> {CLT_Deligne_conjectural (maillon Deligne), F4_1st_order (maillon Ns24)}`

**Pivot σ_cd→LLR :**
- `F4_1st_order --STRUCTURAL--> Pivot_sigcd_LLR` (le 1er-ordre FORT = l'obstacle = l'argument)
- `Pivot_sigcd_LLR --TESTS--> {sigcd_scaling_dimadj_077 (kill-test D6 via LLR), σ_cd_Tc3_G2 (validation Phase B sur σ_cd connu)}`

Distribution des 40 types : STRUCTURAL 25, DERIVES 4, TESTS 3, VALIDATES 2, CONFIRMS 2, UPDATES 2, PREDICTS 1, RETRACTS 1 — **tous dans le set canonique**.

---

## CHEMINS-CLÉS (le récit v13)

1. **Le mécanisme AZ est maintenant DÉRIVÉ, pas cité** : `EQ_FS_indicator → FS_indicator_AZ_flip (D1) → AZ_reality_class`, renforcé à longue portée par `EQ_Sigma2 → Sigma2_log_coeff_AZ (D2) → AZ_reality_class` (4 PASS). Le flip T²=ν isole la réalité-de-rep.
2. **Hub champ-maître** : `EQ_master_field_m2inf` relie CLT_Deligne, Deligne_series, H15 (déterministe), H16 (universel) ; `CLT_Deligne_conjectural (D3) → UPDATES CLT_Deligne` le tempère (conjectural).
3. **Impossibilité gravitationnelle** : `H7 → {GW_sound_shell, EXP_SIDM_Bullet, EXP_CMB_S4, SECTOR_DARK}` — les 3 portes collapsent sur ξ. Cohabite avec `F4_1st_order → GW_sound_shell` (prémisse débloquée) MAIS H7 dit « non-détectable » = résultat négatif honnête.
4. **Pivot méthodologique** : `F4_1st_order → Pivot_sigcd_LLR → {D6 kill-test, σ_cd_Tc3_G2 validation}` — le 1er-ordre fort interdit la mesure naïve, LLR est la sortie.
5. **Hygiène** : `Reliability_audit_2026-06-25` = nœud transverse (comme `integer_collision_hygiene`) : innocente E6, re-scope ⟨r⟩=β, nomme les 3 maillons faibles.

---

## CHECK ADVERSARIAL DeepSeek (mécanisme vs numérologie) — sur les 6 arêtes-équations

DeepSeek-V4 (referee, reasoning_effort=high, instruit de NE PAS inventer d'ID arXiv) :

| Arête-équation | Verdict |
|---|---|
| 1. `EQ_FS_indicator → AZ class` | **MÉCANISME** (FS classe la réalité → indice de Dyson, rigoureux) |
| 2. `EQ_Sigma2 → AZ class` | **MÉCANISME** (rigidité spectrale standard) |
| 3. `EQ_master_field_m2inf → CLT` | constantes 27 & 10/3 = coïncidences **(déjà étiquetées comme telles)** ; l'arête (m₂^∞=cumulant survivant) est structurelle |
| 4. `EQ_kappa_FP → 1/6` | **MÉCANISME** (invariant de Kostant) |
| 5. `EQ_coeff_E → 42` | **MÉCANISME** (invariants de groupe, validé G2) |
| 6. `EQ_RRS → 0.77` | fit empirique → **PREDICTS** (tautologique sur SU(N), déjà étiqueté) — arête re-typée DERIVES→**PREDICTS** suite à ce flag |

> **Verdict global DeepSeek** : « *None of these are the same class as the retracted integer-collision examples (b2=22, log|det|/S2=6/5).* » Les 2 flags (#3, #6) portent sur des constantes/fits **déjà honnêtement étiquetés** dans les nœuds (27/10/3 = coïncidences arbitrées ; RRS = FIT tautologique, kill-test en attente). **Action prise** : arête #6 re-typée `DERIVES → PREDICTS` (un fit empirique PRÉDIT, ne dérive pas). D3 garde `UPDATES` (tempérage, pas dérivation). → conforme « 0 numérologie, chaque arête = relation réelle ».

---

## CAVEATS HONNÊTES (à ne jamais effacer en aval)

- **D1** : reproduction de Verbaarschot (continuum inféré algébriquement, pas diagonalisé), PAS un théorème neuf.
- **D2/H26** : coeff Σ² absolu NON comparable cross-groupes ; G2 sur-claime (vraie provenance = ⟨r⟩) ; 3 INCONCLUSIVE.
- **D3** : CLT FAIBLE seulement, champ-maître **CONJECTURAL** (série Deligne finie → pas de théorème de concentration). NE PAS lire comme prouvé.
- **D6** : **SCALING, PAS théorème, PAS DERIVED** ; RRS=FIT ; tautologique sur SU(N) ; seul le F4 (non-mesuré) discrimine. Mesure via LLR encore DUE.
- **H15** : PARTIAL ; n=2,3,4, 1 géométrie, 5 membres, exposants empiriques ; label « champ libre » rétracté.
- **H16** : SCALING numérique pas théorème ; PASS sur moments BRUTS ; série Deligne finie (E8 redondant).
- **H7** : compute-zéro ; seule échappatoire = production non-thermique (inflaton) découplant ξ ; framing « collapse + porte impuissante », PAS « anti-corrélation pure ».
- **H25** : INCONCLUSIVE, per-volume, Nt=4 seul ; le « ≈dim(adj) » est un artefact de β_norm.
- **AUDIT** : ⟨r⟩ mesure β PAS chiralité ; provenance G2 = maillon #1 (geste Kévin requis, physique chGOE survit).
- **PIVOT** : AUCUN chiffre σ_cd fiable tant que Phase B non validée ; clone isolé NON mergé ; Phase C compute-bound → Vast/GPU.

---

## RÉFÉRENCES arXiv VÉRIFIÉES (live, arXiv API, 2026-06-26)
- **2506.15509** — « Confined-deconfined interface tension and latent heat in SU(N) gauge theory » (RRS ; EQ_RRS, D6, H25). ✓
- **1605.08048** — « Non-Abelian Dark Forces and the Relic Densities of Dark Glueballs » (FMS ; H7 ligne de relique Λ_D∝ξ⁻³). ✓
- **cond-mat/9508026** — Altland & Zirnbauer (EQ_FS_indicator, D1). ✓
- **hep-lat/9501025** — Halász & Verbaarschot (flip staggered→GSE). ✓
- **cond-mat/9811142** — Forrester-Nagao-Honner (bord-dur symplectique). ✓

(Tous re-vérifiés contre l'API arXiv live ce tour ; titres confirmés correspondant à l'usage.)

---

## INVARIANTS DE BUILD
- v12 : 125 / 192. v13 : **142 / 232** (+17 nœuds / +40 arêtes).
- **0 arête pendante, 0 self-loop, 0 label vide, 0 doublon (src,dst,type), 0 nœud isolé** (degré min des nouveaux = 1). JSON valide (indent=2, ensure_ascii=False).
- 6 nœuds `kind="equation"` ajoutés (premier emploi du kind equation : 0→6).
- Nouveaux types d'arêtes (40) ⊂ set canonique {EXACT, STRUCTURAL, VALIDATES, TESTS, DERIVES, FEEDS, RETRACTS, PREDICTS, CONFIRMS, UPDATES}. Les arêtes v12 héritées gardent leurs types d'origine (non modifiées).
- `date` mise à jour ; `centrality_note` rafraîchie (recalcul networkx si besoin).
- **0 commit / 0 push** (conforme). VPS local, 0 GPU/gamer/prod touché. **Push PROPOSÉ à Kévin après le gate.**
