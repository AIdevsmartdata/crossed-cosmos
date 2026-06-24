# DECODER_GRAPH v10 — notes narratives

**Date** : 2026-06-24
**Fichier** : `/root/cc-private/papers/DECODER_GRAPH_v10.json`
**Base** : v9.2 canonique (`/tmp/v92_canonical.json` = 83 nœuds / 117 arêtes, identique GitHub privé+public) + portage du retag hygiène local du 3 juin.
**Mode** : MÉCANISME-PAS-NUMÉROLOGIE. Tout lien-pont porte une équation/un mécanisme dans son `label` ; les collisions d'entiers sont MORTES.
**Compute** : VPS local, 0 GPU. GPU gamer = PROD F4 Ns24 (intouché). Aucun kevinotron lancé. Aucun git pull/commit/push/stash.

---

## Compteurs

| | v9.2 | **v10** | Δ |
|---|---|---|---|
| Nœuds | 83 | **104** | **+21** |
| Arêtes | 117 | **151** | **+34** |

Décomposition des +21 nœuds : **1** correction (hygiène) + **6** découvertes-lattice + **7** expériences + **7** ponts-mécanisme.
Décomposition des +34 arêtes : 4 RETRACTS (hygiène portée) + 30 arêtes-pont/mesure/contrainte.

---

## 1. Hygiène portée (la confusion de dates résolue)

**La confusion private/public/local.** Il existait trois objets :
- **v9.2 canonique** (28 mai, `n_nodes=83`) : la version la plus RICHE, identique sur GitHub privé et public. C'est la BASE de v10.
- **v9 local hygiène** (3 juin, `DECODER_GRAPH_v9_LOCAL_hygiene_2026-06-03.json`, `n_nodes=73`) : un retag local **régressif en nombre de nœuds** (il avait 73 nœuds, manquant tout l'apport « world-first F4/E6 + HMC » du 28 mai), mais qui portait une hygiène correcte : il marquait 4 nœuds collision-d'entiers comme `FALSIFIED`.

v10 prend la **richesse de v9.2** (83 nœuds) ET la **propreté de v9 local** (retag des 4 collisions). On ne part PAS du v9 local (régression).

**Ce que v9.2 avait DÉJÀ rétracté** (via le nœud-correction `adjoint_bug_fix`, bug einsum) :
- `Gribov_1327_neg` (n_neg=0 partout après bugfix) ;
- `Z1_Gribov_classification` ;
- `d_s(G2_FP)=2.24` (tier `RETRACTED_bug_einsum`).
Ce sont les rétractations **Gribov/mesure**. v10 les conserve telles quelles (pas de double-comptage).

**Ce que v10 PORTE depuis le 3 juin** (les 4 collisions d'ENTIERS, qui étaient encore tier=EXACT dans v9.2) :
| Nœud | tier v9.2 | tier v10 | Pourquoi MORT |
|---|---|---|---|
| `b2=22=Σ(dim-1)` | EXACT_p=0.002 | **RETRACTED** | partition coïncidence 1/286 ; SM donne 9 pas 22 ; ne matche pas {8,8,2,2,2} |
| `b2_22_dual_counting` | EXACT_adversarial_p=0.002 | **RETRACTED** | 2e fit au même 22 (12q+6l+4H) ; même erreur |
| `K_Koide=1-8/24` | EXACT_DS_Bot_H2 | **RETRACTED** | 2/3 = midpoint de la bande Koide ; Leech rootless ; pas de mécanisme |
| `d_s=7/3_via_G2` | EXACT_DS_Bot_H1 | **RETRACTED** | forme SU(3)-Gribov tautologique (1 équation, pas 2) |

**Implémentation** : un nœud-correction unique `integer_collision_hygiene` (kind `correction`) émet **4 arêtes RETRACTS** vers les 4 nœuds, et chaque nœud reçoit `tier="RETRACTED"` + `status="FALSIFIED"` + `falsified_reason` + `falsified_by`. Le `b_2(K3)=22` reste **VIVANT comme STRUCTURE** (forme d'intersection 2E8+3H), pas comme l'entier 22.

**Principe écrit (dans le nœud-correction)** : « La STRUCTURE des réseaux/groupes est féconde ; les collisions d'ENTIERS (22, 24, 8) sont MORTES. »

---

## 2. Le sous-graphe NEUF : découverte ↔ pont-mécanisme ↔ expérience

C'est l'apport central de v10 : connecter les **découvertes lattice de juin** à la **théorie rigoureuse** et aux **expériences réelles**, chaque arête justifiée par une équation.

### 2.1 Nœuds-découverte lattice (kind measurement/discovery, tiers HONNÊTES)

| Nœud | valeur | tier honnête |
|---|---|---|
| `σ_cd_Tc3_G2` | 0.124–0.126 | MEASURED_per-volume_pre-FSS_pre-continuum |
| `Anderson_F4_26_chGOE` | ⟨r⟩=0.534 (1.1σ chGOE) | MEASURED_valid_citable |
| `w0_G2_coeffE42` | w0/a=1.365 ; coeff E G2=42 | MEASURED_per-volume_pre-FSS |
| `F4_thermo_betac_Nt4` | β_c(Nt4)≈32 | **MEASURED_order-INDETERMINATE** (Ns24 en PROD) |
| `BanksCasher_Sigma_F4` | Σ≈30 | **MEASURED_QUENCHED_raw-number** (diagnostic modeste) |
| `m0pp_G2_escrow` | a·m_0++=0.484 | **ESCROW_isotropic-precision-wall** |

### 2.2 Nœuds-pont-mécanisme (kind theory/bridge — chacun PORTE son équation)

| Nœud | équation | tier |
|---|---|---|
| `Svetitsky_Yaffe` | déconfinement ↔ modèle de spin à symétrie de centre Z(G) | THEOREM 1982 |
| `BanksCasher_relation` | Σ = π·ρ(0) | THEOREM 1980 (EXACT) |
| `Luscher_string` | V(r) = σr − π(d−2)/24r | THEOREM 1980 (coeff EXACT) |
| `dim_transmutation` | Λ = μ·(…)·e^{−8π²/(b₀g²)} | THEOREM RG pert. (EXACT) |
| `Altland_Zirnbauer` | classe chRMT = symétrie anti-unitaire de Dirac | THEOREM tenfold (EXACT) |
| `GW_sound_shell` | Ω_GW(α, β/H, v_w) | MODEL Caprini-Hindmarsh (thin-wall = BORNE-SUP) |
| `trace_anomaly_Clausius` | Δ = β(g)/2g·⟨F²⟩ ; L_h via Clausius-Clapeyron | THEOREM + thermo (EXACT/FEEDS) |

### 2.3 Nœuds-expérience (kind `experiment`, bornes vérifiées rapport §5)

`EXP_LISA`, `EXP_BBO`, `EXP_DECIGO`, `EXP_PTA_NANOGrav`, `EXP_SIDM_Bullet`, `EXP_CMB_S4`, `EXP_BESIII`.
Toutes les bornes citées sont issues d'IDs arXiv marqués ✓ dans le rapport (2007.04241, gr-qc/0512039, 2006.13545, 1503.07675, 1701.05877, 1907.04473, 2503.13286, 2508.21821). Aucun ID fabriqué ajouté ; aucun ID [NON-VÉRIFIÉ] promu.

### 2.4 La chaîne mécaniste (lattice → pont → expérience)

```
trace_anomaly_Clausius  ──FEEDS──►  GW_sound_shell  ──CONSTRAINS──►  EXP_LISA   (sub-LISA ~4 ordres, négatif-honnête)
   ▲ (Δ=β/2g⟨F²⟩, L_h)                 (Ω_GW(α,β/H,v_w))           ──CONSTRAINS──►  EXP_BBO    (marginal au mieux)
   │                                                              ──CONSTRAINS──►  EXP_DECIGO (NON détectable, hors-bande)
σ_cd_Tc3_G2  ──FEEDS──┘                                           ──CONSTRAINS──►  EXP_CMB_S4 (clos, ~6 ordres)
F4_thermo_betac_Nt4 ──FEEDS──►  GW_sound_shell   (F4→Ω_GW = 1er groupe exceptionnel SI 1er ordre ; Ns24)

Svetitsky_Yaffe ──STRUCTURAL──► {F4_thermo, σ_cd_G2, G_2=Aut(𝕆)}   (centre trivial → l'ABSENCE d'ordre exact est PHYSIQUE)
BanksCasher_relation ──EXACT──► BanksCasher_Sigma_F4   (Σ=πρ(0), QUENCHED brut)
Altland_Zirnbauer ──EXACT──► Anderson_F4_26_chGOE   (rep réelle {26} → chGOE)
Luscher_string ──TESTS──► σ_cd_Tc3_G2   (−π/12r sépare corde/universel, ≥2 volumes)
dim_transmutation ──EXACT──► {w0_G2_coeffE42, b_0}   (Λ=μe^{−8π²/b₀g²})
m0pp_G2_escrow ──TESTS──► EXP_BESIII   (ratio universel m/√σ ; G2 = escrow, PAS prédiction)
              ──CONSTRAINS──► EXP_SIDM_Bullet   (ESCROW : signe attractif seul, magnitude non résolue)
```

Le **hub h^∨** existant (`h_dual_coxeter`) est relié à `dim_transmutation` (SHARED : b₀ ∝ h^∨) et à `w0_G2_coeffE42` (STRUCTURAL : κ_FP=1/(2h^∨), cf. erratum 2026-06-01 — voir §4).

---

## 3. Centralités (recalculées via networkx)

Le profil de centralité bascule : avec l'apport lattice↔pont↔expérience, `KEVINOTRON_FORMULA` passe en tête de la betweenness (0.039), devant `G_2=Aut(𝕆)` (0.034) puis `𝕆_octonions` et `F4_group`. Le sous-graphe physique (F4_group, GW_sound_shell, trace_anomaly) devient un second pôle, distinct du pôle arithmétique historique (octonions↔Leech↔M24).

---

## 4. Notes locales intégrées

- **Erratum κ_FP (2026-06-01)** : κ_FP = 1/(2 h^∨) (Coxeter DUAL), PAS 1/(2|Φ⁺|) ; coïncident seulement pour SU(3). Intégré comme arête STRUCTURAL `h_dual_coxeter → w0_G2_coeffE42` (les deux clés sont h^∨) et SHARED `h_dual_coxeter → dim_transmutation`. Les résultats SU(3) sont inchangés (κ=1/6).
- **OBSERVABLES_RECENT_2026-06** : la table d'observables récentes (g−2, DESI, Cabibbo, glueballs A-T 3.405(21)) a été consultée ; la valeur A-T 3.405(21) est référencée dans le label de l'arête `m0pp_G2_escrow → EXP_BESIII` (mécanisme = ratio universel m/√σ). Les tensions hors-secteur (H₀, neutron-lifetime, DESI) n'ont PAS été ajoutées comme nœuds : aucun mécanisme du moteur ne s'y branche (anti-numérologie).

---

## 5. Check adversarial DeepSeek (verdict)

`deepseek.py --temperature 0.0`, système « relecteur, verdict défaut REJETER, distinguer PONT de NUMÉROLOGIE ». 17 arêtes-pont soumises (labels uniquement).

- **1er passage** : 12 PONT, 5 NUMÉROLOGIE. Les 5 flaggées (GW→LISA/DECIGO/CMB-S4, Anderson→F4, m0++→SIDM) étaient des arêtes **observable→expérience** dont le label énonçait une comparaison numérique sans re-citer le mécanisme (porté par le nœud-source). DeepSeek était littéral.
- **Correctif** : labels durcis pour nommer explicitement l'équation/le mécanisme à l'arête (Ω_GW(α,β/H,v_w) ; f_peak∝T_c ; ΔNeff∝g* ; classe AZ par réalité de rep ; ESCROW = signe seul). m0++→BESIII repassé en `TESTS` avec mécanisme = ratio universel m/√σ.
- **2e/3e passage** : **17/17 PONT**. Aucune numérologie résiduelle dans les arêtes-pont.

Garde-fou anti-fab : DeepSeek n'a proposé AUCUN ID arXiv (interdit dans le prompt) ; aucun ID inventé n'a été retenu.

---

## 6. Régénération enriched/diagram (skippé proprement)

`enrich_decoder_graph.py` est **hardcodé sur l'ancien schéma** `DECODER_GRAPH.json` (DAG 45 nœuds, nœuds `Branson-Gilkey`/`K3_topology`, squelette TikZ figé). Il n'a aucune référence à v10 et ne consomme PAS le schéma v9.2/v10 (kinds `experiment`, dict `nodes` v9.2). Lancé, il régénère `DECODER_GRAPH_ENRICHED.json` + `DECODER_diagram.{mmd,dot,tex,html}` **à partir du vieux graphe** — il ne touche PAS `DECODER_GRAPH_v10.json`. Régénérer l'enriched/diagram pour v10 exigerait de réécrire le script (SRC + listes de nœuds + TikZ). **SKIP propre** : v10 est livré comme JSON autonome valide ; l'enriched v10 est laissé à une itération dédiée du script.

---

## Fichiers écrits

- `/root/cc-private/papers/DECODER_GRAPH_v10.json` (104 nœuds / 151 arêtes)
- `/root/cc-private/papers/DECODER_GRAPH_v10_NOTES_2026-06-24.md` (ce fichier)

Aucun commit/push. Repo non perturbé.
