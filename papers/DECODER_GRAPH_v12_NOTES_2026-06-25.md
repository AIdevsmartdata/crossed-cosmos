# DECODER_GRAPH v12 — notes de version (2026-06-25)

**Base :** v11 (115 nœuds / 172 arêtes, `DECODER_GRAPH_v11.json`).
**v12 :** **125 nœuds (+10) / 192 arêtes (+20)**, 0 arête pendante, 0 self-loop, 0 label vide.
**Source de vérité :** `~/crossed_cosmos_notes/PREREG_HYPOTHESES_FALSIFIABLES_2026-06-24.md` (programme falsifiable, chaque résultat chiffré) + `finding_f4_thermo_2026-06-22` + `finding_pistes_BC_assessment_2026-06-24`.
**Mode :** MÉCANISME-PAS-NUMÉROLOGIE. Tiers HONNÊTES (per-volume / finite-vol / single-Nt / single-β / L6).
**Mantra de portée :** tout reste dans le **secteur de jauge confiné** (pas de gravité-détectable, pas de fusion mass-gap). Les arêtes vers les détecteurs GW restent CONSTRAINS/sub-LISA (héritées v11), pas modifiées.

---

## SCOREBOARD du programme falsifiable — 6 PASS / 2 FALL

| Hyp | Test | Verdict | Nœud v12 |
|---|---|---|---|
| **H3** | Sp(4){4}→chGSE (bulk ⟨r⟩=0.698) ; SO(7){7}→chGOE (0.540) | **PASS** | `Sp4_chGSE`, `SO7_chGOE` |
| **H4a** | F4 déconfinement = 1er-ordre (Nt=4, FSS 4-vol) | **PASS** | `F4_1st_order` |
| **H6** | Champ-maître Deligne : m₃,m₄ forme close | **FALL** (version forte) → m₃^∞=m₄^∞=0 | `Deligne_gaussian_CLT` |
| **H8** | Flip intra-groupe SU(3) adj {8}→chGOE (0.537) | **PASS** | `SU3adj_chGOE` |
| **H10** | Deligne grand-h∨ = GAUSSIEN (m₅^∞=m₆^∞=0) | **PASS** | `Deligne_gaussian_CLT`, `CLT_Deligne` |
| **H14** | Edgeworth skewness ≈ c₃/h∨ (c₃ fermé) | **FALL** (réfutation double, propre) | `Edgeworth_1overh` (RETRACTED) |
| **H18** | Bord-dur micro Sp(4) = noyau Bessel chGSE | **PASS** | absorbé dans `Sp4_chGSE` (2e angle) |
| **H20** | méta double-universalité | FISSURÉE côté Edgeworth, **debout** | `double_universality` |

→ **6 PASS (H3×2, H4a, H8, H10, H18) / 2 FALL (H6-fort, H14)**. Les 2 chutes sont des **falsifications PROPRES** (pré-enregistrées, le critère de réfutation a mordu) — pas des bugs. H6 « tombe proprement » mais ENGENDRE le résultat structurel neuf (m_k^∞=0 → CLT). H14 tombe et RETIRE une sur-structure (Edgeworth fermé).

---

## NŒUDS AJOUTÉS (10)

### 5 découvertes (mécanisme, pas numérologie)
1. **`F4_1st_order`** (discovery) — F4 déconfinement = **1er-ORDRE établi à Nt=4**. Discriminant PROPRE = double-pic plaquette qui CROÎT avec V (ΔBIC 16→31→116 à β32) + Binder U4<2/3 (0.31 à Ns24). χ_max(|L|) 0.23→0.45→1.06→6.30 (Ns12→16→20→24) = SUGGESTIF mais pas décisif seul (centre trivial → |L| pas un paramètre d'ordre). DeepSeek adversarial : « 1ER-ORDRE ÉTABLI ». **Caveats : Nt=4 SEUL, per-volume, pré-continuum** (ordre du continuum non prouvé → exigerait ≥2 Nt).
2. **`Sp4_chGSE`** (discovery, ⟨r⟩=0.698) — Sp(4){4} pseudoréel → **chGSE confirmé DEUX FOIS** : bulk (H3, Kramers exact + ⟨r⟩=0.698 à 2.1σ de chGSE) ET bord-dur micro (H18, bootstrap chGSE 100 %, KS rejette chGOE/chGUE). **1ère classe symplectique de la série.** Caveats : volume unique L6, β unique, N=28.
3. **`SO7_chGOE`** (discovery, ⟨r⟩=0.540) — SO(7){7} réel → chGOE (contrôle H3, 0.7σ). Caveats : L6, 28 cfg, β=10 grossier.
4. **`SU3adj_chGOE`** (discovery, ⟨r⟩=0.537) — SU(3) **adjoint {8}** réel → chGOE = **FLIP INTRA-GROUPE** (le {3} complexe→chGUE 0.600 ; en changeant SEULEMENT la rep, la classe bascule, 5.4σ de chGUE). **Le test le plus propre du mécanisme réalité-de-rep.** Caveats : L6, 28 cfg.
5. **`Deligne_gaussian_CLT`** (discovery) — la limite grand-h∨ de Deligne est **GAUSSIENNE** : m₃=m₄=m₅=m₆→0 (H6+H10), seuls m₁=0 et m₂^∞ (forme close) survivent. ≠ free-probability (réfutée). Gate : reproduit m₂^∞ à 1.3×10⁻⁴. Caveats : fit symbolique 4-points (E8/E7-m6 infaisables in-box).

### 3 théorie/pont
6. **`AZ_reality_class`** (theory) — réalité-de-rep → classe RMT, **TRIPLE-CONFIRMÉ** : bulk (H3) + flip intra-groupe (H8) + bord-dur micro (H18) sur SU3/G2/F4/Sp4/SO7. = le nouveau **hub** (degré 8). Réfs vérifiées (arXiv live) : Altland-Zirnbauer **cond-mat/9508026**, Halász-Verbaarschot **hep-lat/9501025** (flip staggered→GSE), Forrester-Nagao-Honner **cond-mat/9811142** (bord-dur symplectique).
7. **`CLT_Deligne`** (theory) — CLT commutatif le long de la série exceptionnelle (jauge→gaussien quand h∨→∞). m₂^∞ = unique cumulant survivant.
8. **`double_universality`** (theory, H20-méta) — limite grand-invariant : jauge→gaussien (h∨, H10) ET Dirac→RMT-AZ (réalité-de-rep, H3) = DOUBLE universalité. **MAJ : univ. de la LIMITE = oui ; univ. des 1ères CORRECTIONS = non côté jauge** (H18 hard-edge PASS mais H14 Edgeworth FALL).

### 2 falsification H14
9. **`Edgeworth_1overh`** (prediction → **tier RETRACTED / status FALSIFIED**) — l'hypothèse « m₃≈c₃/h∨, c₃ fermé ».
10. **`Edgeworth_1overh_falsified`** (correction) — le nœud-correction porteur du RETRACTS. Réfutation double : (i) pas de 1/h∨ propre (approche ~h∨^{−3/2}, p_fit=1.73, p=1 = pire collapse) ; (ii) obstruction structurelle (3 irreps ψ³(adj) au même taux limite r0=3 → poids extrapolés explosent +8390/−20040/+12452, cancellation catastrophique, pas de forme close à la m₂). DeepSeek (Annals-reviewer) : AGREE. **H10 INTACT** (m_k^∞=0 reconfirmé) — seule la sous-structure fine (coefficient d'Edgeworth fermé) tombe.

---

## NŒUD MIS À JOUR (supersédé, PAS supprimé)

- **`F4_thermo_betac_Nt4`** (v11 : « ORDRE INDÉTERMINÉ ») → tier `MEASURED_order-SUPERSEDED-by-F4_1st_order`, note mise à jour. β_c(Nt4,Ns12)≈32 reste valide (1ère localisation propre du déconfinement F4) ; **l'ORDRE est maintenant établi 1er-ordre (Nt=4)** par `F4_1st_order` via l'arête **UPDATES**. Le nœud d'origine est conservé pour la traçabilité (le β_c et la localisation thermique tiennent indépendamment de l'ordre).

---

## ARÊTES AJOUTÉES (20) — chaque label porte une équation/mécanisme

**Ponts AZ triple-confirmés (le cœur mécanisme) :**
- `AZ_reality_class --VALIDATES--> Sp4_chGSE` (pseudoréel → T²=−1 → β=4 ; bulk+bord-dur)
- `AZ_reality_class --CONFIRMS--> SO7_chGOE` (réel → T²=+1 → β=1)
- `AZ_reality_class --CONFIRMS--> SU3adj_chGOE` (adjoint réel → chGOE malgré SU(3))
- `SU3adj_chGOE --EXACT--> AZ_reality_class` (**le flip isole la réalité-de-rep** : même groupe, la rep flippe la classe)
- `Sp4_chGSE --STRUCTURAL--> AZ_reality_class` (**2e angle** : bord-dur Bessel chGSE confirme le bulk)
- `Altland_Zirnbauer --EXACT--> AZ_reality_class` (la table tenfold, maintenant triple-confirmée sur réseau)
- `AZ_reality_class --STRUCTURAL--> Anderson_F4_26_chGOE` (F4{26}→chGOE = membre original de la table)

**Chaîne CLT de Deligne :**
- `Deligne_gaussian_CLT --DERIVES--> CLT_Deligne` (κ_{k≥3}→0, m₁=0, m₂^∞ → 2 cumulants = gaussien)
- `CLT_Deligne --STRUCTURAL--> h_dual_coxeter` (limite prise le long de h∨→∞)
- `CLT_Deligne --STRUCTURAL--> Deligne_series` (m₂^∞ = le champ-maître = unique cumulant survivant)
- `Deligne_gaussian_CLT --STRUCTURAL--> Deligne_series` (Adams ψ^k sur la ligne {G2,F4,E6,E7})

**Méta double-universalité :**
- `double_universality --STRUCTURAL--> AZ_reality_class` (branche Dirac)
- `double_universality --STRUCTURAL--> CLT_Deligne` (branche jauge)

**F4 1er-ordre → GW + supersession :**
- `F4_1st_order --UPDATES--> F4_thermo_betac_Nt4` (double-pic+Binder établissent l'ordre que χ_max seul ne donne pas)
- `F4_1st_order --MEASURES--> F4_group` (1er ordre établi du déconfinement F4)
- `F4_1st_order --FEEDS--> GW_sound_shell` (prémisse 1er-ordre CONFIRMÉE → H4b GW(F4) débloqué : L_h,σ_cd → α,β/H)
- `Svetitsky_Yaffe --STRUCTURAL--> F4_1st_order` (centre trivial → |L| pas paramètre d'ordre → c'est le double-pic+Binder, pas |L|, qui établit l'ordre)

**Falsification H14 :**
- `Edgeworth_1overh_falsified --RETRACTS--> Edgeworth_1overh` (approche ~h∨^{−3/2}, pas de c₃ fermé)
- `Edgeworth_1overh --RETRACTS--> CLT_Deligne` (l'Edgeworth tombe mais le CLT tient : seul le 1er-coeff fermé est faux)
- `Edgeworth_1overh_falsified --STRUCTURAL--> double_universality` (fissure H20 côté jauge : limite oui, 1ères corrections non)

---

## CHEMINS-CLÉS (le récit du graphe)

1. **Triangle AZ triple-confirmé** :
   `Altland_Zirnbauer → AZ_reality_class → {Sp4_chGSE, SO7_chGOE, SU3adj_chGOE}` avec le retour-pont
   `SU3adj_chGOE → AZ_reality_class` (le flip isole le mécanisme) et `Sp4_chGSE → AZ_reality_class` (le bord-dur = 2e angle). Le hub `AZ_reality_class` est le nœud de degré 8 le plus connecté des nouveautés.

2. **CLT de Deligne** :
   `Deligne_gaussian_CLT → CLT_Deligne → {h_dual_coxeter, Deligne_series}`. Le théorème central limite remplace le « champ-maître prouvé » (jamais revendiqué) et clôt H6/H10.

3. **Double universalité (le pont méta)** :
   `double_universality → {AZ_reality_class (Dirac), CLT_Deligne (jauge)}`, fissurée par
   `Edgeworth_1overh_falsified → double_universality` (côté jauge, 1ères corrections).

4. **F4 1er-ordre → GW** :
   `Svetitsky_Yaffe → F4_1st_order → {F4_thermo_betac_Nt4 (UPDATES), F4_group (MEASURES), GW_sound_shell (FEEDS)}`,
   puis hérite la chaîne v11 `GW_sound_shell → {EXP_LISA, EXP_BBO, …}` (sub-LISA, négatif-honnête).

5. **Falsification propre** :
   `Edgeworth_1overh_falsified → Edgeworth_1overh (RETRACTS) → CLT_Deligne (RETRACTS-partiel)` : la chute RETIRE la sur-structure SANS toucher le CLT brut (H10 intact).

---

## CHECK ADVERSARIAL DeepSeek (mécanisme vs numérologie) — sur les 5 ponts-clés

DeepSeek-V4-pro (referee Annals/PRL, reasoning_effort=high), instruit de NE PAS inventer d'ID arXiv :

| Pont | Verdict DeepSeek |
|---|---|
| 1. `AZ → Sp4_chGSE` | **MÉCANISME** (pseudoréel→T²=−1→chGSE rigoureux ; Kramers + ⟨r⟩ + noyau bord-dur confirment) |
| 2. `SU3adj → AZ` (flip) | **MÉCANISME** (toggle rep complexe→réel change la symétrie anti-unitaire ; isole la réalité-de-rep) |
| 3. `Deligne_gaussian_CLT → CLT_Deligne` | **MÉCANISME** (Adams ψ^k → cumulants k≥3 s'annulent, m₂ survit en forme close = CLT dérivé, pas coïncidence) |
| 4. `F4_1st_order → GW_sound_shell` | **WEAK-BUT-OK** (1er-ordre = condition nécessaire au sound-shell ; chaîne physique saine MAIS Nt=4-seul/continuum non prouvé = préliminaire) |
| 5. `Edgeworth_falsified → Edgeworth` | **MÉCANISME** (réfutation empirique + obstruction rep-théorique = retrait logique, pas numérologie) |

> **Verdict global DeepSeek** : « *All proposed links are physically or mathematically derivable mechanisms (or a sound retraction thereof), and the graph contains no disguised numerology.* »
> Et explicitement : **« None of these bridges rests on an integer coincidence or a '6/5 ratio' bolt-on of the type retracted elsewhere. »** → aucun pont n'est de la même classe que `b2=22` / `ratio_6_5` (rétractés v11).

Le WEAK-BUT-OK sur le pont 4 est COHÉRENT avec le tiering : `F4_1st_order` est tagué `single-Nt_pre-continuum`, et l'arête FEEDS dit « prémisse confirmée → GW peut procéder », pas « GW établi ».

---

## CAVEATS HONNÊTES (à ne jamais effacer en aval)

- **F4 1er-ordre** : **Nt=4 SEUL**, per-volume (Ns12→24), **pré-continuum**. L'ordre du *continuum* exigerait ≥2 Nt (Nt6 à Ns12/16 = broad/crossover-leaning, non résolu — cf finding_f4_thermo). H11 (l'ordre survit-il au continuum ?) reste OUVERT.
- **Sp4/SO7/SU3-adj Anderson** : **volume unique L6**, β unique, **28 configs/groupe**, k=60. La classe (=β) est robuste ; l'approche-continuum et la densité microscopique fine ne sont PAS testées.
- **chGSE finite-a** : la classe staggered est le partenaire « flippé » du continuum (Halász-Verbaarschot) ; cohérent avec la doc du toolkit, à ne pas confondre avec la classe continuum.
- **Deligne CLT** : fit symbolique **4-points** (E8 tout-k et E7-m6 infaisables in-box). Exclut p=1 nettement mais ne PIN pas l'exposant exact de l'approche (~h∨^{−3/2}). « champ-maître » jamais « prouvé » (série Deligne finie → pas de théorème de concentration). 27 & 10/3 = coïncidences arbitrées, PAS J₃(𝕆)/decoder.
- **GW(F4)** : héritée sub-LISA / négatif-honnête de v11 ; le pont 1er-ordre→GW est une PRÉMISSE débloquée, pas un spectre calculé (H4b/H17 à faire).
- **E6/E7 (H9)** : E6 testable (lancé), E7 pas un groupe du moteur → différé. Pas de nœud E6/E7 chGUE/chGSE ajouté tant que non mesuré (pas de prédiction-en-dur dans le graphe).

---

## RÉFÉRENCES arXiv VÉRIFIÉES (WebFetch live, arXiv API, 2026-06-25)

- **cond-mat/9508026** — Altland & Zirnbauer, « Random Matrix Theory of a Chaotic Andreev Quantum Dot » (classes de symétrie non-standard). ✓
- **hep-lat/9501025** — Halász & Verbaarschot, « Universal fluctuations in spectra of the lattice Dirac operator » (staggered → GSE, le flip). ✓
- **cond-mat/9811142** — Forrester, Nagao & Honner, « Correlations for the orthogonal-unitary and symplectic-unitary transitions at the hard and soft edges » (bord-dur symplectique). ✓

Aucun ID fourni par DeepSeek n'a été utilisé (DeepSeek instruit de ne pas en inventer ; tous les IDs ci-dessus vérifiés indépendamment).

---

## INVARIANTS DE BUILD
- v11 : 115 nœuds / 172 arêtes. v12 : **125 / 192** (+10 / +20).
- 0 arête pendante, 0 self-loop, 0 label vide. JSON valide (indent=2, ensure_ascii=False).
- `date` = « 2026-06-25 v12 — falsification program results: F4 1st-order, AZ table+intra-group flip+hard-edge, Deligne Gaussian CLT, H14 Edgeworth retracted ».
- `centrality_note` v11 conservée (recalcul networkx si besoin ; +10 nœuds/+20 arêtes la périment).
- **0 commit / 0 push** (conforme à la consigne). VPS local, 0 GPU touché, kevinotron non lancé.
