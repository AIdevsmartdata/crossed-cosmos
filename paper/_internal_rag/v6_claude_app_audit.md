# Audit scientifique — document "Loi de saturation modulaire-computationnelle"

**Source.** Document Claude app reçu 2026-04-22, proposant promotion de v6 en « loi ECI finale » avec principe d'équivalence, 5ème constante fondamentale, et 3 prédictions falsifiables (PBH burst ×3, LISA plateau, α̇/α).

**Auditeur.** Claude CLI (Opus 4.7) + Mistral Magistral-medium cross-check + calculs locaux (sympy/numpy) + WebSearch Crossref/arXiv.

**Verdict global.** **MAJOR FIX / REJET PARTIEL.** Le document contient une synthèse conceptuelle intéressante mais **trois erreurs arithmétiques critiques sur les claims load-bearing** et **quatre violations directes de PRINCIPLES.md** (règles V6-1, V6-4, 1, 16). La prédiction phare (PBH burst ×3) est **numériquement fausse de ~15 ordres de grandeur**. L'adoption telle quelle violerait le gate d'honnêteté et produirait un papier rétractable.

---

## 1. Erreurs arithmétiques critiques

### 1.1 **FAUX : ω_P = 2π k_B T_P/ℏ**

Le document écrit : « Elle est par ailleurs égale à $2\pi k_B T_P/\hbar$ où $T_P$ est la température de Planck, manifestant son origine thermique modulaire. »

**Calcul indépendant (Python + Magistral cross-check) :**
- $T_P = \sqrt{\hbar c^5 / (G k_B^2)} = 1.4168 \times 10^{32}$ K
- $2\pi k_B T_P / \hbar = 1.1654 \times 10^{44}$ rad/s
- $\omega_P = \sqrt{c^5/(G\hbar)} = 1.8549 \times 10^{43}$ rad/s
- **Ratio $2\pi k_B T_P/\hbar : \omega_P = 2\pi$, pas 1.**

L'identité prétendue est **fausse par un facteur 2π**. Magistral (cross-check indépendant) confirme : « κ_R = 2π k_B T_R / ℏ is **not** equal to ω_Planck, but rather 2π times ω_Planck when T_R is the Planck temperature. »

**Conséquence.** Toute la structure « UV-IR » du tableau des deux valeurs-limites est bâtie sur une identité incorrecte. La « cinquième constante fondamentale » κ n'est pas ω_P à la limite UV ; elle est $2\pi \omega_P$. Ce n'est pas un détail cosmétique : la suite du document utilise cette identité pour identifier κ à la fréquence de Planck, puis pour géométriser Λ via $(H_0/\omega_P)^2$.

### 1.2 **FAUX : $S_{BH}(M_* = 5.1\times 10^{14}\,\text{g}) \approx 10^{25}$**

Le document écrit : « au voisinage de M* avec $S_{BH} \approx 10^{25}$, $S^{-0{,}05} \approx 0{,}055$, $\ln S \approx 58$, on obtient $\Delta t/\tau \approx 3$ — **le sursaut final est allongé d'un facteur trois**. »

**Calcul indépendant.**
$$S_{BH} = 4\pi G M^2 / (\hbar c) = 4\pi k_B (M/M_P)^2$$

Pour $M = 5.1\times 10^{14}$ g $= 5.1\times 10^{11}$ kg :
$$S_{BH} \approx 6.9 \times 10^{39} \;(\text{en unités de } k_B)$$

Soit $\log_{10} S_{BH} \approx 40$. **Le document est faux de ~15 ordres de grandeur sur l'entropie du PBH critique.**

Avec la valeur correcte $S = 10^{40}$ :
- $S^{-0.05} = 10^{-2} = 0.010$ (document : 0.055)
- $\ln S = 92$ (document : 58)
- produit $\approx 0.92$ (document : 3)

**Le facteur 3 d'allongement du sursaut disparaît sous la valeur correcte.** La formule $\Delta t / \tau \sim S^{-\alpha} \ln S$ donne ~1, c'est-à-dire **pas d'allongement significatif**, pour un PBH évaporant actuellement. La prédiction phare du document est **numériquement fausse**.

*Pour obtenir S ≈ 10^25 il faudrait un BH de masse M ≈ 2×10^4 kg (≈ 20 tonnes), pas 5×10¹¹ kg. Le document confond deux régimes de masse.*

### 1.3 **IMPRÉCIS : $\Lambda/M_P^4 = (H_0/\omega_P)^2 = 10^{-122}$**

Le document écrit : « le rapport notoire $\Lambda/M_P^4 \approx 10^{-122}$ est exactement $(\kappa_{dS}/\kappa_P)^2 = (H_0/\omega_P)^2$. »

**Calcul :**
- $(H_0/\omega_P)^2 = 1.39\times 10^{-122}$, soit $\log_{10} = -121.86$
- $\rho_\Lambda/\rho_P \approx 1.13\times 10^{-123}$, soit $\log_{10} = -122.95$

Les deux ratios **diffèrent d'~1 ordre de grandeur** ; ils ne sont pas « exactement » égaux. Le document présente l'identité comme structurelle (« ce n'est pas fortuit mais structurel »), alors que la vérification numérique montre qu'elle tient seulement en ordre-de-grandeur, et avec un préfacteur ~10 non identifié. **Requiert softening** : « l'identité est approximative à un ordre de grandeur près », ou une dérivation explicite du préfacteur manquant.

### 1.4 **FAUX : Lange 2021 PRL 126 011102 — valeur de $\dot\alpha/\alpha$**

Le document cite : « Lange et al., PRL 126 (2021) 011102 : $(-8{,}0\pm 3{,}6)\times 10^{-18}$/an via Yb⁺ E2/E3 ».

**Vérification web.** Le résumé publié (APS) rapporte $\dot\alpha/\alpha = 1.0(1.1)\times 10^{-18}$/an, pas $-8.0 \pm 3.6 \times 10^{-18}$/an. Le signe, la valeur centrale, et la barre d'erreur sont tous incorrects. **Citation fabriquée ou erronée.** Violation de PRINCIPLES rule 1 (honesty gate).

### 1.5 Corrects

- $\omega_P = 1.855\times 10^{43}$ rad/s ✓
- $H_0$ à 67.4 km/s/Mpc = $2.184\times 10^{-18}$ s⁻¹ ✓
- $T_{dS} = \hbar H_0 / (2\pi k_B) = 2.66\times 10^{-30}$ K ✓
- Haferkamp et al., *Nat. Phys.* 18, 528 (2022), « Linear growth of quantum circuit complexity » ✓

---

## 2. Violations PRINCIPLES.md

### 2.1 **V6-1 : « No equality without proof »**

Le document promeut Eq.(1) d'**inégalité → égalité stricte** :

> « Sa force se mesure à son pouvoir générateur : […] l'hypothèse de saturation […] promeut l'inégalité en **égalité stricte** »
> « la loi ECI finale s'énonce […] sous la forme de l'**égalité** $\dot S_{\text{gen}}[R] = \kappa_R C_k \Theta(PH_k)$ »

PRINCIPLES.md V6-1 (commit 31525e1, 2026-04-22) :
> « The v6 equation form is $dS_{gen}/d\tau_R \le \kappa_R \cdot C_k \cdot \Theta(PH_k)$, **NOT equality**. Equality was attempted, three independent derivation agents (Claude/Gemini/Magistral) all verdicted ANSATZ, adversarial landed fatal Attack #2 (Krylov log regime becomes contradiction under equality). »

Le document ignore explicitement ce verdict et reproduit l'erreur que V6-1 prohibe. **Régression directe sur une décision à triple-lock.**

### 2.2 **V6-4 : « No cosmological falsifier in v6 »**

Le document propose **trois** falsifieurs cosmologiques (PBH burst ×3, LISA plateau, α̇/α dérive) comme « signatures observationnelles discriminantes ».

PRINCIPLES.md V6-4 :
> « D18 and D18b killed the fσ_8 × Θ(PH_2) falsifier at DR3+Euclid precision (S/N ≈ 0.36σ at fiducial, σ(ε_0) degradation 27× under marginalisation, degeneracy with galaxy bias b(z) |ρ| = 0.998). v6 is a FORMAL paper, not a cosmology paper. Do NOT re-propose a cosmological prediction in the v6 draft. »

Les trois falsifieurs proposés n'ont **aucun passage d'audit adversarial** (D18-équivalent pour PBH, LISA, α̇/α) ni de forecast Fisher avec marginalisation de nuisances. Le document présente des S/N nominaux (« 3–5σ si événement », « 2–5σ », « 3σ vers 2028 ») **sans propagation d'erreurs ni covariance avec le bias astrophysique**. C'est la même faute méthodologique qui a tué fσ_8 × Θ(PH_2).

Réintroduction de falsifieurs cosmologiques dans le papier formel = **violation directe de V6-4**.

### 2.3 **Rule 1 : « Honesty gate »**

- Citation fabriquée Lange 2021 (cf. §1.4).
- Multiples claims citant Brown-Susskind 2018, Verlinde 2017 *SciPost Phys* 2, 016, Rovelli *PRD* 48 1708 sans vérification RAG. Ces citations doivent être validées contre `paper/_rag/` avant inclusion.

### 2.4 **Rule 16 : « Negative literature claims : soften or substantiate »**

Le document contient :
> « Aucune publication entre 2015 et 2026 ne formule explicitement leur unification sous un principe d'indistinguabilité opérationnelle — c'est notre contribution axiomatique propre. »

Claim négatif de littérature non-substantiée sur 11 ans × 4 programmes actifs (Connes-Rovelli, CLPW-DEHK, Brown-Susskind, Jacobson). PRINCIPLES rule 16 exige soit une literature-survey scope précise, soit reformulation « n'a pas été tabulée en forme fermée dans [références spécifiques] ».

Plus important : il y a des publications qui y ressemblent : par ex. la ligne Susskind 2020 (« gravity is the tendency of complexity to grow ») et la série Pedraza-Russo-Svesko-Weller-Davies 2022-2023 sont proches. À reformuler comme « distinct from Susskind 2020 in [X], distinct from Pedraza 2022 in [Y] ».

---

## 3. Claims théoriques à (in)valider

### 3.1 **Principe d'équivalence opérationnel** (énoncé B5)

Magistral (cross-check) :
> « The claim lacks a clear definition of what is meant by "complexity" in this context and how it is measured. Without a precise definition and a clear operational meaning, it's hard to evaluate the equivalence. […] For it to be well-posed, the paper should define the metrics for δS and δC_k, show that they are invariant under the specified transformations, and demonstrate that any physical measurement cannot distinguish between changes in entropy and changes in complexity. »

L'analogie Einstein 1907 est séduisante mais la structure mathématique n'est pas donnée. En particulier :
- Qu'est-ce qu'une « expérience intrinsèquement interne à l'algèbre modulaire » (notion non-définie) ?
- Comment mesure-t-on opérationnellement $C_k$ dans un type $\mathrm{II}_1$ ? M1′ dans v6 actuel tend vers Caputa 2024 spread complexity ; le document ignore ce raffinement.
- La « covariance sous Tomita-Takesaki » est déjà partiellement assurée par Prop. 1 (logistic envelope), pas une nouveauté conceptuelle.

**Verdict.** B5 tel qu'énoncé est **un slogan, pas un théorème**. L'analogie Einstein ne se tient que si (a) l'opérationnalité est construite, (b) le protocole-d'indistinguabilité est écrit en opérateurs de l'algèbre. Ni l'un ni l'autre n'est fait.

### 3.2 **Chaîne déductive A1–A6 « théorèmes de B5 »**

Chaque axiome A1-A6 est présenté comme « théorème » dérivé de B5. L'examen détaillé :

- **A1 (type II_1)** : le document argue que la trace finie est *nécessaire* à la co-définition du doublet. MAIS CLPW, DEHK utilisent aussi type $\mathrm{II}_\infty$ dans des contextes plus larges ; la prétendue unicité est fausse.
- **A3 (temps modulaire)** : cité comme « théorème de Connes-Takesaki ». Le théorème modulaire de Connes donne l'unicité à automorphisme interne près, pas au sens fort invoqué ici. Softening requis.
- **A4 (complexité k-design)** : « seule la version k-design est invariante sous $\sigma_t^\omega$ ». Claim non-trivial, non sourcé, à vérifier contre Ma-Huang 2025 et Caputa 2024. **À ne pas affirmer sans preuve.**

**Verdict global sur la section « dérivation ».** Le document avoue : « Cette déduction n'est pas encore un théorème rigoureux au sens mathématique ». Cela est correct et honnête, mais contredit le framing « chaque axiome est un théorème de B5 ». Il faut choisir : soit garder la structure comme programme (plausible), soit affirmer les théorèmes (insoutenable).

### 3.3 **Facteur 1/4 de Bekenstein-Hawking « expliqué » par 2π/8π**

Claim : « la normalisation du flot modulaire absorbe exactement le 1/4 comme rapport 2π/8π ».

Arithmétiquement, 2π/8π = 1/4 ✓. Physiquement, le lien n'est pas dérivé : la calibration du flot modulaire $\Delta^{it} = e^{-2\pi t K}$ fait apparaître un 2π au compteur, et le périmètre thermique euclidien donne 2π (pas 8π). Le 1/4 de BH vient de calculs euclidiens sur l'action de Gibbons-Hawking, où le 8π vient de $16\pi G$ dans l'action d'Einstein-Hilbert. **Le rapprochement 2π/8π = 1/4 est une coïncidence numérique, pas une dérivation.** À retirer ou transformer en « heuristique ».

---

## 4. Prédictions : évaluation une-par-une

| # | Prédiction | Verdict | Détail |
|---|---|---|---|
| 1 | Burst PBH ×3 | **FAUX numériquement** | S_BH utilisé = 10^25 incorrect ; correct = 10^40 → extension ~1, pas 3 |
| 2 | LISA plateau Ω_gw h² ~ 5×10⁻¹¹ à 10⁻³ Hz | **NON-PROPAGÉ** | Pas de dérivation de A_eff ~ ε_PH ~ 10⁻¹⁰ ; Fisher forecast absent |
| 3 | α̇/α ~ H_0 = 2×10⁻¹⁸/an | **PLAUSIBLE mais non-falsifiable distinctement** | Prédiction naturelle de toute théorie scalaire ; indistinguable de quintessence standard |
| 4 | ΔΤ/τ +8% sur PBH 10¹² kg | même problème que #1 | |
| 5 | ΔC_2^TT ≈ +128 μK² | **0.5σ max** (admis dans le doc) | sous variance cosmique |
| 6 | Plateau NANOGrav sous-dominant | **<1σ** (admis dans le doc) | dégénéré |
| 7 | δφ_CP ~ 10⁻²² rad neutrinos | **NON-TESTABLE** (admis dans le doc) | 21 ordres sous DUNE |

**Conclusion.** Sur 7 prédictions, 4 sont **trivialement ou admis non-testables** ; 2 sont **numériquement fausses ou non-dérivées** ; 1 est **plausible mais dégénérée** avec quintessence standard. **Aucune ne survit à une revue rigoureuse en l'état.**

---

## 5. Recommandation concrète

### Ce qui peut être récupéré du document

1. **La structure « principe d'équivalence opérationnel »** comme *motivation conceptuelle* (pas comme théorème). Peut être un paragraphe §6 programmatique dans le v6.1 actuel.
2. **La discussion UV-IR avec κ observer-dépendante** comme *réflexion* dans §5 « Relation to existing programs », pas comme « cinquième constante fondamentale ».
3. **La comparaison systématique avec RG / QFT / cordes / LQG / Verlinde** est utile — bon matériel pour la §5 comparative table (déjà ajoutée en a09bbce).

### Ce qui doit être **rejeté**

1. **Égalité stricte au lieu d'inégalité** (V6-1). Non-négociable.
2. **Trois falsifieurs cosmologiques** (V6-4). Non-négociable sans pipeline D18-équivalent.
3. **Affirmation $S_{BH}(M_*) = 10^{25}$** et conséquences (V6-1 : honesty gate).
4. **Identité $\omega_P = 2\pi k_B T_P/\hbar$** (V6-1 : honesty gate).
5. **Citation Lange 2021 avec $-8.0 \times 10^{-18}$/an** (V6-1 : honesty gate).
6. **Proposition CODATA adoption de κ** : prématuré par plusieurs décennies.

### Ce qui doit être **softening**

1. Claim « A1-A6 sont théorèmes de B5 » → « B5 motive A1-A6 ; dérivations rigoureuses restent à écrire ».
2. « Λ/M_P⁴ = (H_0/ω_P)² exactement » → « coïncidence numérique à ~1 ordre de grandeur près ».
3. « 1/4 de BH expliqué par 2π/8π » → retirer, ou transformer en remarque heuristique.
4. Toutes les phrases « aucune publication entre 2015 et 2026 » → soit préciser le scope de littérature, soit reformuler.

---

## 6. Verdict final

Le document Claude app est **une ambition saine mais mal exécutée**. Le framing « Einstein 1915 » est dangereux : toute critique devient plus dure quand on se compare à Einstein. Les erreurs arithmétiques (S_BH off par 15 ordres, ω_P vs 2π·ω_P, Lange mal cité) sont du niveau qu'un referee PRL cueille en 10 minutes. Les violations PRINCIPLES (V6-1, V6-4) régressent sur des décisions que nous avons prises il y a 6 heures avec audit triple-agent.

**Si on adopte le document tel quel → rétraction certaine dans les 6 mois suivant publication.**

**Recommandation.** Garder v6.1 actuel (HEAD `a09bbce`, 6 pages, SHIP-ready) comme paper JHEP formel. Le matériel Claude app peut alimenter :
- Un §6 « programmatic outlook » court (2 paragraphes max) sur l'analogie équivalence principle.
- Une réflexion future dans un **companion paper** v7 phénoménologique SI et seulement SI les 3 falsifieurs passent un pipeline D18-equivalent (Fisher + marginalisation + cross-model adversarial).

**Pas de modification de Eq.(1) ou Prop. 1.** Pas d'introduction des 3 falsifieurs cosmologiques dans v6. Pas de promotion de κ au rang de constante CODATA dans v6.

**Commit SHA vérifications.** Cet audit : à commit. Calculs : `/tmp/eci_numerical_audit.py`. Magistral cross-check : `/tmp/mistral_crosscheck.py` (output tronqué à 2000 tokens mais cruciaux confirmés).
