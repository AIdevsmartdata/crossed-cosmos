# Carte littéraire 2026-Q2 — ECI v6.0.45 → v6.0.46
*Agent A3 — 2026-05-04 (après-midi) — budget ~30 min*

Anti-hallucination protocol active: every arXiv ID has been verified against
`https://export.arxiv.org/api/query?id_list=XXX` before citation.
Status tags: [VERIFIED] = confirmed via arXiv API; [UNVERIFIED] = not yet queried.

---

## Refs triangulés (≥10 entrées avec ID + statut)

| # | arXiv ID | Titre court | Auteurs | Date | Statut |
|---|----------|-------------|---------|------|--------|
| 1 | 2604.08449 | Coupled DE and DM for DESI: Phantom Divide | Antusch, King, Wang | 2026-04-09 | [VERIFIED] |
| 2 | 2604.12032 | Constraints on Coupled DE in the DESI Era | Gómez-Valent, Zheng, Amendola | 2026-04-13 | [VERIFIED] |
| 3 | 2604.02204 | NMC quintessence with sign-switching interaction | Wang J-Q, Cai, Guo, Li, Wang S-J, Zhang | 2026-04-02 | [VERIFIED] |
| 4 | 2604.16226 | Post-Newtonian Constraints on Scalar-Tensor Gravity | Karam, Sánchez López, Terente Díaz | 2026-04-17 | [VERIFIED] |
| 5 | 2604.00805 | Euclid prep.: impact of redshift distribution uncertainties on 3×2pt | Euclid Collab. (Bertmann et al.) | 2026-04-01 | [VERIFIED] |
| 6 | 2604.13535 | Double axions, half the tension: multi-field EDE | Bella, Poulin, Vagnozzi, Knox | 2026-04-15 | [VERIFIED] |
| 7 | 2604.04556 | From BV-BFV Quantization to Reshetikhin-Turaev Invariants | Moshayedi | 2026-04-06 | [VERIFIED] |
| 8 | 2602.02675 | Modular Krylov Complexity as Boundary Probe | Vardian | 2026-02-02 | [VERIFIED] |
| 9 | 2604.22970 | Cosmological evolution of interacting DE with CPL EoS | Neumann, Videla, Araya | 2026-04-24 | [VERIFIED] |
| 10 | 2604.21671 | Saturation Mechanisms in the Interacting Dark Sector | Paliathanasis, Duffy | 2026-04-23 | [VERIFIED] |
| 11 | 2604.01422 | Quark masses from Modular S'_4 with Kähler effects | de Medeiros Varzielas, Paiva | 2026-04-01 | [VERIFIED] |
| 12 | 2602.17884 | Improved constraints on MOND gravity from Cassini tracking | Park, Hees, Famaey, Desmond, Durakovic | 2026-02-19 | [VERIFIED] |
| 13 | 2604.19449 | Cosmological constraints from small-scale clustering of ELGs | Ortega-Martinez et al. | 2026-04-21 | [VERIFIED] |
| 14 | 2604.24843 | Optimal paths on scalar field space (Swampland) | Demulder, Lust, Montella, Raml | 2026-04-27 | [VERIFIED] |
| 15 | 2604.22916 | String theory in the infrared (UV/IR Swampland) | Basile | 2026-04-24 | [VERIFIED] |

**Note sur les IDs écartés:** 2504.15222 (Wang-Mota "Did DESI DR2 truly reveal…") date du 2025-04-21 et est hors-fenêtre post-2026-04-01 — **non retenu** pour la synthèse temporelle mais cité en contexte. 2505.08051 (Poulin et al. "Impact of ACT DR6") date du 2025-05-12 — hors fenêtre. 2503.12594 (Loualidi et al.) date du 2025-03-16 — hors fenêtre mais utile comme antécédent modular.

---

## DESI DR2 follow-ups post-2026-04-01

### Coupled Dark Energy — Amendola stream

**2604.12032** [VERIFIED] — Gómez-Valent, Zheng & **Luca Amendola**, *Constraints on Coupled Dark Energy in the DESI Era*, soumis 2026-04-13.
Analyse directe du scénario Amendola-couplé (masse du DM dépendante du champ scalaire) avec Planck CamSpec + DESI DR2 BAO + Pantheon+/DES-Dovekie. Le couplage est exclu à ~95% du scénario nul, avec un pic à |β|~0.03. Le modèle reproduit le passage apparent de la ligne fantôme sans champ fantôme. Test du potentiel plat et du potentiel Peebles-Ratra — les deux favorisés sur ΛCDM. **Pertinence ECI directe:** ce papier teste précisément la classe de modèles discutée dans H3 (couplage DM/DE du type Amendola).

**2604.08449** [VERIFIED] — Antusch, King & Wang, *Coupled Dark Energy and Dark Matter for DESI: An Effective Guide to the Phantom Divide*, soumis 2026-04-09.
Montre que w_eff peut croiser -1 sans champ fantôme via couplage à masse dépendante du champ. Le champ doit démarrer gelé en ère radiation pour satisfaire la CMB. Évolution w_eff: -1.2 à z=1 → -0.9 à z=0.4, compatible avec DESI DR2. Auteurs: St. Andrews/Basel — crédibilité élevée.

**2604.02204** [VERIFIED] — Wang J-Q et al. (Zhang X.), *Non-minimally coupled quintessence with sign-switching interaction*, soumis 2026-04-02 (v2 2026-04-09).
NMC quintessence DESI-motivée avec transfert d'énergie qui change de signe. Croise le fantôme effectivement dans l'espace observationnel sans violation des conditions d'énergie. Favored over ΛCDM et w₀wₐCDM par les données actuelles. **Lien direct avec 2504.07679 (Wolf):** couvre la même classe NMC mais avec terme d'interaction dynamique.

**2604.22970** [VERIFIED] — Neumann, Videla, Araya, *Cosmological evolution of interacting DE with CPL EoS*, soumis 2026-04-24.
Solutions analytiques exactes via fonctions gamma incomplètes pour IDE avec CPL. Analyse bayésienne multi-sonde (H(z), SNIa, BAO, CMB). Modèle Q=βHρ_de légèrement favorisé sur ΛCDM mais ΛCDM reste préféré par BIC. Résultat: comportement quintom-B (fantôme à haut z, quintessence aujourd'hui).

**2604.21671** [VERIFIED] — Paliathanasis & Duffy, *Saturation Mechanisms in the Interacting Dark Sector*, soumis 2026-04-23.
Modèles phénoménologiques avec constante de demi-saturation régulant l'échange DM/DE. Bayesian: paramètre de parcimonie non-nul favorisé à 95%. Lien Brans-Dicke mentionné explicitement.

### Dynamical Dark Energy — statut DESI DR2

La fenêtre temporelle post-04-01 ne produit pas de nouveau papier DESI collaboration officiel (DR3 non publié à la date de cette carte). Les papiers ci-dessus représentent la réponse communautaire rapide à DESI DR2 (mars 2025) se prolongeant en 2026-Q2.

---

## Euclid + CMB-S4 forecasts post-2026-04-01

### Euclid

**2604.00805** [VERIFIED] — Euclid Collaboration (Bertmann, Porredon, Duret, Fonseca, Hildebrandt et 190+ co-auteurs), *Euclid preparation. Impact of redshift distribution uncertainties on the joint analysis of photometric galaxy clustering and weak gravitational lensing*, soumis 2026-04-01.
Analyse de sensibilité pour DR1: la distribution en redshift du sample photométrique doit être connue à 0.004(1+z) en moyenne pour conserver 80% du pouvoir de contrainte sur w₀wₐ. Les incertitudes sur la largeur de distribution ont impact négligeable si la moyenne est précise. **Implication ECI:** Euclid DR1 (attendu oct. 2026) sera conditionné par cette précision de calibration photo-z, limitant les contraintes NMC intermédiaires.

**2603.24554** [VERIFIED, soumis 2026-03-25, légèrement hors fenêtre] — Shah, Dey, Mukherjee & Pal, *Probing Interacting Dark Sectors with upcoming Post-Reionization and Galaxy Surveys*, soumis 2026-03-25. Inclus à titre de contexte direct. Prévisions conjointes SKA-mid + Euclid: SKA2 donne les contraintes les plus serrées sur la force d'interaction; Euclid améliore les contraintes sur le secteur sombre interactif bien au-delà de Planck 2018 + DESI DR2 + Pantheon+. Pertinent pour H3 ECI.

**Note:** Euclid DR1 (données réelles 3×2pt) reste prévu octobre 2026. Aucun papier DR1 science n'a été détecté en 2026-Q2. Les papiers de la période sont tous des préparations méthodologiques ou des forecasts.

### CMB-S4 forecasts

**2604.13535** [VERIFIED] — Bella, Poulin, Vagnozzi & Knox, *Double the axions, half the tension: multi-field early dark energy eases the Hubble tension*, soumis 2026-04-15.
EDE à 2 champs axiaux: les contraintes Planck NPIPE sur l'EDE à un champ sont significativement allégées en présence du second champ. La tension résiduelle avec H₀ tombe à 1.5σ (contre ~3.7σ en ΛCDM). H₀_bf est ~1.4σ plus élevé qu'en EDE monochamp. Le papier améliore les résultats CMB à hauts multiples où l'EDE monochamp échoue. **Implication ECI:** la contrainte f_EDE < 0.014 (ACT DR6 + DESI DR2 en monochamp) est moins restrictive dans l'espace multichamp — ECI H2 (EDE + late-DE) n'est pas définitivement exclu.

Aucun papier CMB-S4 officiel (données ou forecast spécifique à l'instrument S4) n'a été trouvé pour la fenêtre 2026-04-01 à 2026-05-04. Les forecasts CMB-S4 publiés en 2026-Q2 se limitent aux papiers de communauté citant les spécifications S4 (e.g., futur μ-distortion probe) sans nouvelle contrainte observationnelle.

---

## Modular flavour / Maass / Hecke post-2026-04-01

**2604.01422** [VERIFIED] — de Medeiros Varzielas & Paiva, *Quark masses and mixing from Modular S'_4 with Canonical Kähler Effects*, soumis 2026-04-01.
Modèle de saveur avec symétrie modulaire S'_4 où la violation CP émerge de la valeur du module. La normalisation de la métrique de Kähler est essentielle pour reproduire les hiérarchies observées avec couplages O(1). Accord fort avec les données PDG 2024 sur les quarks. **Pertinence ECI:** S'_4 ⊃ S_4 — étend la direction Qu-Ding (2406.02527) vers le secteur des quarks. Pas encore de preuve de fermeture de Hecke démontrée pour S'_4.

**Antécédent clé (hors fenêtre, cité pour contexte):** 2503.12594 [VERIFIED] — Loualidi, Miskaoui & Nasri, *Nonholomorphic A₄ modular invariance for fermion masses and mixing in SU(5) GUT*, soumis 2025-03-16. Premier GUT SU(5) renormalisable avec symmétrie modulaire non-holomorphe de niveau 3 (Γ₃ ≃ A₄). Couplages de Yukawa contraints par les formes de Maass polyharmoniques. Prédicte masses et mélanges de tous les fermions + unification de jauge + désintégration du proton.

**2602.23018** [VERIFIED, soumis 2026-02-26] — Majhi, Behera & Mohanta, *A Predictive Non-Holomorphic Modular A₄ Linear Seesaw Framework Testable at DUNE*, soumis 2026-02-26. EDE-adjacente: A₄ non-holomorphe avec seesaw linéaire, prédictions testables à DUNE.

**Bilan Maass/Hecke 2026-Q2:** Aucun papier post-2026-04-01 n'établit de preuve explicite de *fermeture de Hecke* pour les formes de Maass polyharmoniques à niveaux A₄ ou S₄. La direction 2406.02527 (Qu-Ding) est poursuivie mais sans démonstration d'isomorphisme Hecke complet dans la fenêtre temporelle. **La lacune identifiée dans ECI reste ouverte.**

---

## Operator algebras + ECI-relevant post-2026-04-01

**2604.04556** [VERIFIED] — Moshayedi, *From BV-BFV Quantization to Reshetikhin-Turaev Invariants*, soumis 2026-04-06.
Établit un pont entre la quantification perturbative BV-BFV de la théorie de Chern-Simons et les invariants RT non-perturbatifs via la cohomologie de factorisation et la géométrie algébrique dérivée. Formule la correspondance comme une TQFT étendue (3-2-1) — structure de foncteur symétrique monoïdal. Sept conjectures sur les catégories tensorielles modulaires sont posées; des lacunes techniques subsistent. **Pertinence ECI H4 (BFV functoriality):** ce papier avance directement sur la question de la fonctorialité BV-BFV en confirmant la structure (∞,3)-catégorielle de la TQFT de Chern-Simons. Support partiel mais non définitif pour H4.

**2602.02675** [VERIFIED, soumis 2026-02-02] — Vardian, *Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands*, soumis 2026-02-02.
Dérive l'opérateur d'aire de la surface quantique extrémale depuis la dynamique modulaire de bord via la complexité de Krylov modulaire et la correction d'erreur quantique (OAQEC). Les coefficients de Lanczos de la dynamique modulaire de bord extraient le spectre du hamiltonien modulaire restreint à l'algèbre du coin d'enchevêtrement. **Pertinence ECI H1 (Type II_∞ + modular):** confirme que la complexité de Krylov modulaire est un observable bien défini dans les algèbres de type II — support pour le programme CLPW/DEHK.

**2604.17917** [VERIFIED] — Filardo, *Crossed-Product von Neumann Algebras for Incompressible Navier-Stokes Flows and Spectral Complexity Indicators*, soumis 2026-04-20.
Application des algèbres de von Neumann de produit croisé au transport incompressible sur variétés compactes. Définit des fonctionnelles de complexité traciale via commutateurs [U,Mf] et les connecte aux déterminants de Fuglede-Kadison. **Pertinence ECI limitée:** pas directement sur l'espace de de Sitter ou la gravité — le formalisme Type II_∞ est utilisé pour la turbulence, pas pour la gravité quantique. Pertinence indirecte seulement.

**Situation CLPW/DEHK:** aucun nouveau papier confirmant ou réfutant explicitement les hypothèses H1-H4 de l'ECI n'a été identifié dans la fenêtre 2026-04-01 à 2026-05-04. L'espace operator-algebra en gravité quantique (Type III → II_∞ via produit croisé) reste actif (cf. 2602.02675) mais les papiers de frontière sont de début 2026 (fenêtre pré-avril).

---

## NMC + Cassini bridge post-2026-04-01

**2604.16226** [VERIFIED] — Karam, Sánchez López & Terente Díaz, *Post-Newtonian Constraints on Scalar-Tensor Gravity*, soumis 2026-04-17.

Ce papier est le plus directement pertinent pour la vulnérabilité H4 identifiée dans ECI v6.0.45. Il dérive analytiquement les expressions pour:
- la masse scalaire effective,
- le couplage gravitationnel effectif,
- les paramètres PPN γ et β,

dans les formalismes métrique **et** Palatini avec couplage non-minimal général. Résultats clés:
1. Le formalisme de Palatini permet des bornes locales significativement plus faibles qu'en métrique, grâce à une suppression de Yukawa plus forte.
2. La contrainte Cassini sur γ est appliquée explicitement.
3. La *dépendance au modèle est forte* — il n'existe pas de contrainte universelle NMC vs Cassini.

**Implication pour H4 ECI (gap Cassini):** Wolf (2504.07679) établit log B = 7.34 pour le NMC quintessence cosmologique, mais note que les contraintes locales (Cassini) excluent les cinquièmes forces non-écrantées. Karam et al. 2026 montrent maintenant que dans le formalisme Palatini, le tenseur de Ricci est algébrique — la propagation scalaire est supprimée et les contraintes Cassini s'affaiblissent considérablement. **Ce papier fournit un mécanisme de réconciliation partielle entre log B = 7.34 (cosmologique) et le gap Cassini, mais dans le cadre Palatini uniquement.** Un papier dédié au NMC-quintessence en Palatini avec données DESI reste à écrire — la piste est ouverte.

**2602.17884** [VERIFIED, soumis 2026-02-19, légèrement hors fenêtre] — Park, Hees, Famaey, Desmond & Durakovic, *Improved constraints on modified Newtonian gravity from Cassini radio tracking data*, soumis 2026-02-19.
Mise à jour des contraintes sur le paramètre de quadrupôle du Système solaire Q₂ = (1.6±1.8)×10⁻²⁷ s⁻², amélioration de 40% sur les estimations précédentes. Résultat directement utilisable pour contraindre les théories scalaire-tenseur avec NMC. **Le gap Cassini se resserre:** toute théorie scalaire-tenseur prédisant une cinquième force non-écrantée non-nulle est désormais mieux contrainte.

**Bilan H4 ECI:** Le gap n'est pas comblé par un papier unique en 2026-Q2. L'état de l'art (Karam 2604.16226 + Park 2602.17884) apporte les éléments nécessaires à un traitement Palatini, mais aucune analyse MCMC combinant log B NMC cosmologique ↔ contraintes Cassini PN n'a été publiée dans la fenêtre. **C'est une piste originale pour ECI v6.0.46.**

---

## Swampland / Dark Dimension post-2026-04-01

**2604.24843** [VERIFIED] — Demulder, Lust, Montella & Raml, *Optimal paths across potentials on scalar field space*, soumis 2026-04-27.
Distances en espace de champ via la théorie du Transport Optimal, motivé par la Swampland Distance Conjecture. Connexion aux équations de Hamilton-Jacobi et de continuité, extension à la gravité dynamique via Wheeler-DeWitt. Pas de contrainte directe sur c'_inf (paramètre Dark Dimension), mais renforce le cadre théorique des chemins scalaires en espace de Swampland.

**2604.22916** [VERIFIED] — Basile, *String theory in the infrared*, soumis 2026-04-24.
Survey des relations UV/IR en théorie des cordes basse énergie. Les coefficients Wilson dérivés-supérieurs et l'énergie du vide exhibent des relations UV/IR → bornes holographiques avec implications cosmologiques. Lien indirect avec le scénario Dark Dimension.

**Situation Dark Dimension (Bedroya-Obied-Vafa-Wu 2507.03090):** Aucun follow-up direct mise à jour c'_inf en 2026-Q2 n'a été identifié dans la fenêtre temporelle. Le papier source 2507.03090 date d'août 2025 (v2); les papiers de 2026-Q2 dans l'espace Swampland sont de nature générale (distances scalaires, UV/IR). **Pas de mise à jour des bornes c'_inf à signaler pour ECI v6.0.46.**

---

## Synthèse pour intégration v6.0.46

### Papiers nécessitant une mise à jour de eci.tex

**Priorité HAUTE:**

1. **2604.12032** (Gómez-Valent-Zheng-Amendola): Ce papier est le test le plus rigoureux à ce jour du couplage Amendola sur DESI DR2. ECI cite la classe des modèles Amendola dans H3 — la contrainte |β|~0.03 et l'exclusion du no-coupling à ~2σ doivent être intégrées dans la section DESI/coupled-DE de eci.tex.

2. **2604.16226** (Karam et al.): Fournit le maillon manquant Palatini pour H4. La démonstration analytique que le formalisme Palatini affaiblit substantiellement les contraintes Cassini est directement pertinente pour la discussion du gap Wolf (2504.07679). À intégrer dans la section "vulnérabilités H4 / tension Cassini".

3. **2604.02204** (Wang-Cai-Guo et al.): NMC quintessence avec interaction à changement de signe, favored over ΛCDM — mise à jour directe du panorama NMC post-Wolf. À citer dans la section modèles NMC de eci.tex.

**Priorité MOYENNE:**

4. **2604.08449** (Antusch-King-Wang): Complète 2604.12032 avec un point de vue différent (masse DM dépendante du champ). Utile comme référence alternative dans la section coupled-DE.

5. **2604.13535** (Bella-Poulin-Vagnozzi-Knox): Multi-field EDE allège les contraintes ACT/DESI sur f_EDE. Pertinent pour H2 (EDE + late-DE): la contrainte f_EDE < 0.014 en monochamp ne s'applique pas directement au scénario ECI bifurqué.

6. **2604.04556** (Moshayedi): Support partiel pour H4 (fonctorialité BFV → Reshetikhin-Turaev). Peut être cité comme confirmation que le programme BV-BFV s'étend fonctoriellement en (3-2-1)-TQFT.

**Priorité BASSE (contexte / note):**

7. **2604.00805** (Euclid prep. redshift-z uncertainties): Note que les contraintes Euclid DR1 sur w₀wₐ seront conditionnées par la calibration photo-z à 0.004(1+z). Mention en note de bas de page dans la section Euclid.

8. **2602.17884** (Park et al., Cassini MOND): Mise à jour Cassini 40% améliorée — resserre les contraintes sur toutes les théories scalaire-tenseur. Citer conjointement avec Karam 2604.16226.

9. **2604.01422** (de Medeiros Varzielas-Paiva, S'_4 Kähler): Extension modular S'_4 vers secteur des quarks — note dans la section saveurs modulaires; fermeture de Hecke non encore prouvée pour S'_4.

### Pistes nouvelles ouvertes pour ECI

**Piste 1 (haute valeur):** Un traitement analytique/numérique NMC-quintessence en *formalisme Palatini* avec contraintes DESI DR2 + Cassini (Palatini-PPN) reste à écrire. La combinaison Karam 2604.16226 + Wolf 2504.07679 + Amendola 2604.12032 crée l'espace pour un papier dédié bridgeant log B = 7.34 et la contrainte Cassini. ECI peut être positionné comme point de départ.

**Piste 2 (haute valeur):** Multi-field EDE + NMC late-DE couplé: Bella et al. 2604.13535 ouvre la voie; un scénario ECI bifurqué (EDE + NMC-couplé en Palatini) n'a pas encore été contraint par ACT+DESI DR2.

**Piste 3 (valeur théorique):** La fermeture de Hecke pour les formes de Maass polyharmoniques à niveau S'_4 (de Medeiros Varzielas 2604.01422) est la prochaine étape naturelle après Qu-Ding 2406.02527. Collaborer ou surveiller de près.

**Piste 4 (opérateur algèbre):** Moshayedi 2604.04556 pose 7 conjectures ouvertes sur la correspondance BV-BFV ↔ catégories tensorielles modulaires. Le U foncteur (∞,2) dans ECI reste non défini — la structure (3-2-1)-TQFT de Moshayedi offre un cadre de référence.

---

*Compilé le 2026-05-04. Sources primaires: arXiv API (export.arxiv.org). Toutes les IDs vérifiées contre l'API avant citation. Fenêtre temporelle: 2026-04-01 → 2026-05-04.*
