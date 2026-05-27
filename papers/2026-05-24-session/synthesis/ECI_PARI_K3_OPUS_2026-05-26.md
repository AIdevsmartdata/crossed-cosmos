# ECI as Arithmetic Code on K3 — Rigorous Tests of H1 (Frobenius) and H3 (Yukawa/M_24)

**Auteur** : Kévin Rémondière (ORCID: 0009-0008-2443-7166), Oloron-Sainte-Marie, France
**Date** : 2026-05-26 (session calculs PARI/GP K3 + Mathieu Moonshine)
**Status** : Working note, intended as basis for Phase 2 paper if tests support a positive direction
**Lineage** : Post-`m_H = κ(SU(2)) · v` breakthrough (0.016%) and `pattern Σ premiers` cosmologique TIER 3

---

## 0. Pré-flight et catches arXiv

Vérifications effectuées :

- **EOT 2010 = arXiv:1004.0956** : "Notes on the K3 Surface and the Mathieu group M_24" par Eguchi, Ooguri, Tachikawa. Confirmé via lecture abstract direct. C'est le paper fondateur de Mathieu Moonshine.
- **BP2008 = arXiv:0802.4247** : Buividovich-Polikarpov (PAS Bhattacharya-Pradhan 0805.0098). Confirmé lors de la session précédente.
- **PARI/GP 2.15.4** disponible localement et utilisé pour tous les calculs Frobenius/modular forms.
- **Liste M_24 irreps** : 26 reps de dimensions
  $\{1, 23, 45, 45, 231, 231, 252, 253, 483, 770, 770, 990, 990, 1035, 1035, 1035, 1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395\}$.
  Vérifié : somme des carrés = 244823040 = $|M_{24}|$. Pas de fabrication.

---

## 1. Cadre théorique des deux hypothèses

### 1.1 H1 — ECI primes comme spectre arithmétique de K3

**Énoncé** : Les "premiers" qui apparaissent dans le pattern empirique $\Lambda/M_{Pl}^4 = \exp(-\sum_{i=1}^{14} p_i) = \exp(-281)$ et $M_{Pl}^2/v^2 = \exp(+\sum_{i=1}^8 p_i) = \exp(+77)$ seraient une projection d'une structure spectrale plus profonde sur une variété K3.

Plus précisément : la séquence $\text{Tr}(\text{Frob}_p | H^2(K3, \mathbb{Q}_\ell))$ encoderait-elle la suite $\{p_1, p_2, p_3, \ldots\}$ ?

### 1.2 H3 — Yukawa fermions comme inverses de dim$(M_{24}\text{-irreps})$

**Énoncé** : Via le elliptic genus K3 décomposé en représentations irréductibles de $M_{24}$ (Mathieu Moonshine), les 9 masses fermioniques pourraient s'écrire $m_f \propto 1/\dim(\rho_f)$ pour $\rho_f \in \text{Irr}(M_{24})$.

---

## 2. Calculs H1 — Fermat quartic Frobenius traces

### 2.1 Choix de variété : Fermat quartic $X : x^4 + y^4 + z^4 + w^4 = 0 \subset \mathbb{P}^3$

K3 surface avec CM par $\mathbb{Q}(\zeta_8)$. Picard rank 20 sur $\bar{\mathbb{Q}}$. Bonne réduction sauf en $p=2$.

### 2.2 Méthode PARI/GP

Comptage direct des points projectifs via décomposition en chartes affines $\{w=1\}$, $\{w=0, z=1\}$, $\{w=0, z=0, y=1\}$ :

$$\#X(\mathbb{F}_p) = \#\{(x,y,z) : x^4+y^4+z^4+1 = 0\} + \#\{(x,y) : x^4+y^4+1=0\} + \#\{x : x^4+1=0\}$$

Application de la formule de Lefschetz pour K3 ($H^1 = 0$) :

$$\#X(\mathbb{F}_p) = 1 + p^2 + \text{Tr}(\text{Frob}_p | H^2)$$

### 2.3 Résultats numériques (PARI 50-digit)

| $p$ | $p \bmod 4$ | $\#X(\mathbb{F}_p)$ | $\text{Tr}(\text{Frob}\|H^2)$ | $\text{Tr}/p$ |
|-----|-----------:|--------------------:|-----------------------------:|-------------:|
| 3   | 3 | 16   | 6     | 2.0000 |
| 5   | 1 | 0    | -26   | -5.2000 |
| 7   | 3 | 64   | 14    | 2.0000 |
| 11  | 3 | 144  | 22    | 2.0000 |
| 13  | 1 | 128  | -42   | -3.2308 |
| 17  | 1 | 600  | 310   | 18.2353 |
| 19  | 3 | 400  | 38    | 2.0000 |
| 23  | 3 | 576  | 46    | 2.0000 |
| 29  | 1 | 768  | -74   | -2.5517 |
| 31  | 3 | 1024 | 62    | 2.0000 |
| 37  | 1 | 1152 | -218  | -7.8919 |
| 41  | 1 | 2520 | 838   | 20.4390 |
| 43  | 3 | 1936 | 86    | 2.0000 |
| 47  | 3 | 2304 | 94    | 2.0000 |

### 2.4 Structure découverte (élégante)

**Observation cruciale** : Pour $p \equiv 3 \pmod{4}$ (8 primes sur 14), $\text{Tr}(\text{Frob}_p | H^2) = 2p$ **exactement**.

Interprétation arithmétique :
- 22 valeurs propres de Frob sur $H^2(K3) \otimes \mathbb{Q}_\ell$ chacune de module $p$ (Weil).
- 20 d'entre elles proviennent du Picard ($H^{1,1}_{NS}$).
- 2 transcendentales proviennent du Hecke Grossencharacter sur $\mathbb{Q}(\zeta_8)$.
- Pour $p \equiv 3 \pmod{4}$ : $\mu_4 \not\subset \mathbb{F}_p$, donc le caractère d'ordre 4 ne s'active pas. Seul le quadratic character contribue.
- Le `+2p` reflète la **classe hyperplane** et **un autre cycle Galois-stable** (signe $+p$, multiplicité 2).
- Les 20 autres valeurs propres s'annulent en somme.

Pour $p \equiv 1 \pmod{4}$, surcroît de cycles algébriques (et contribution transcendantale).

### 2.5 Identification du newform CM transcendental

Via `mfinit([16, 3, -4])` dans PARI, on identifie le newform CM **16.3.b.a** (LMFDB notation) :

$$f_{16.3.b.a}(\tau) = \sum_{n \geq 1} a_n q^n$$

avec coefficients $a_1=1$, $a_5=-6$, $a_9=9$, $a_{13}=10$, $a_{17}=-30$, $a_{25}=11$, et $a_p = 0$ pour $p \equiv 3 \pmod{4}$.

Ces $a_p = 2 \cdot \text{Re}(\alpha^2)$ pour $p = N(\alpha) = a^2+b^2$ avec $\alpha = a+bi \in \mathbb{Z}[i]$.

**Cependant** : la transcendental L-function du Fermat quartic est PLUS riche : pour $p=5$, le candidat naïf `Tr - 2p = -36` ne correspond ni à `2*a_5(16.3.b.a) = -12` ni à `a_5(\text{Sym}^2 E_a) = -1`. Il faut un Hecke Grossencharacter sur $\mathbb{Q}(\zeta_8)$ de degré 4, qui décompose en plusieurs facteurs $\mathbb{Q}$-rationnels.

### 2.6 Test ECI : Σ a_p vs Σ premiers

| Cumul $\sum_{p \leq p_k} a_p$ | Σ first $j$ primes le plus proche | $j$ | écart relatif |
|------------------------------:|----------------------------------:|----:|--------------:|
| $k=4$ ($p \leq 11$): 16 | 17 | 4 | 6.25% |
| $k=6$ ($p \leq 17$): 284 | **281** | **14** | **1.06%** |
| $k=7$ ($p \leq 19$): 322 | 328 | 15 | 1.86% |
| $k=13$ ($p \leq 43$): 1062 | 1060 | 25 | **0.19%** |
| $k=14$ ($p \leq 47$): 1156 | 1161 | 26 | 0.43% |

**Le hit $k=6 \to$ Σ_14 premiers = 281** correspond à la cible ECI $\Lambda$ exponent !

### 2.7 Test de significativité (adversarial)

Null hypothesis: random $a_p$ avec mêmes magnitudes, signes random.

- 5000 trials : meilleur match relatif moyen = 6.01%, std = 18.2%
- Le résultat réel best $\approx$ 0.19% est battu par **23.1%** des trials random
- Null avec full Weil bound : 15.4% des trials battent

**Verdict H1 : INCONCLUSIVE → TIER 3 (probably coincidence)**

Le résultat n'est pas significatif au seuil 5%. La structure modulaire est bien réelle et le Frobenius factorise élégamment, mais le **codage des "premiers ECI" via Frobenius traces n'est PAS établi statistiquement**.

### 2.8 Bonus inattendu : la valeur ζ(3)

En calculant la $L$-fonction partielle linéarisée du Fermat quartic à $s=3$ :

$$L_{\text{partial}}^{\text{lin}}(K3, 3) = \prod_{p=3}^{47} (1 - a_p \cdot p^{-3})^{-1} \approx 1.2035$$

contre $\zeta(3) = 1.2021$ → **0.12% d'écart**.

**MAIS** avec correction quadratique correcte $L_p(T) = 1 - a_p T + p^2 T^2$ :

$$L_{\text{partial}}^{\text{quad}}(K3, 3) \approx 1.1825$$

ce qui s'écarte de $\zeta(3)$ à **1.6%**. Et l'adversarial dit 3-4% des trials random font aussi bien.

**Verdict** : la fameuse coïncidence ζ(3) est un artefact de la linéarisation. Le κ_∞ candidat ζ(3)/√π = 0.6782 reste à dériver par d'autres moyens.

---

## 3. Calculs H3 — Yukawa vs M_24 irrep dimensions

### 3.1 Données

| fermion | $m_f$ (GeV) | $y_f = \sqrt{2} m_f / v$ |
|---------|------------:|-------------------------:|
| $e$     | 0.000511    | 2.94e-6                  |
| $u$     | 0.00216     | 1.24e-5                  |
| $d$     | 0.00467     | 2.68e-5                  |
| $s$     | 0.0935      | 5.37e-4                  |
| $\mu$   | 0.10566     | 6.07e-4                  |
| $c$     | 1.273       | 7.31e-3                  |
| $\tau$  | 1.77686     | 1.02e-2                  |
| $b$     | 4.183       | 2.40e-2                  |
| $t$     | 172.57      | 0.991                    |

M_24 dimensions distinctes : 20 valeurs $\{1, 23, 45, 231, 252, 253, 483, 770, 990, 1035, 1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395\}$.

### 3.2 Best-fit cherché : $m_f = m_t \cdot (d_f / d_t)^{-\alpha}$

Brute force : test des $\binom{20}{9} = 167,960$ combinaisons d'assigner 9 dim de M_24 aux 9 fermions, avec ajustement linéaire optimal de $\alpha$ en log-log.

**Best assignment trouvée** :

| fermion (heaviest first) | $d$ assigné | $m_{\text{pred}}$ (GeV) | erreur rel. |
|--------------------------|------------:|------------------------:|------------:|
| $t$                      | 253         | 184.04                  | 6.7%        |
| $b$                      | 770         | 3.73                    | 10.8%       |
| $\tau$                   | 990         | 1.55                    | 12.9%       |
| $c$                      | 1035        | 1.32                    | 4.0%        |
| $\mu$                    | 2024        | 0.126                   | 19.6%       |
| $s$                      | 2277        | 0.0837                  | 10.5%       |
| $d$                      | 5313        | 4.30e-3                 | 7.9%        |
| $u$                      | 5796        | 3.17e-3                 | 46.8%       |
| $e$                      | 10395       | 4.10e-4                 | 19.8%       |

Avec **best $\alpha = 3.50$** (cas où $m_f = m_t \cdot (d_t/d_f)^{3.50}$).

Total sum sq log residuals : **0.285**.

### 3.3 Tests adversariaux

**Null A : 50 trials avec 20 random log-uniform dims en [1, 11000]**
- Mean score: 1.26, min: 0.31
- Real $\leq$ null : 0%

**Null B : 50 trials avec M_24 dims perturbées ±50%**
- Mean score: 1.04, min: 0.36
- Real $\leq$ null : 0%

**Null C (control) : dims idéales calculées pour $\alpha=2$ entier (instanton-like)**
- Best score: 0.022 (dims $\{1, 6, 10, 12, 40, 43, 192, 283, 581\}$) → **bien meilleur que M_24**

### 3.4 Verdict H3

**Le fit M_24 est statistiquement significatif vs random log-uniform** (Z > 2σ effectif sur le score), MAIS :

1. **$\alpha = 3.50$ n'a pas d'interprétation physique évidente.** Pas 1 (Yukawa direct), pas 2 (instanton action), pas 1/2 (BPS overlap).
2. **Les ratios Yukawa observés matchent des ratios de dim M_24 à <2%** pour de nombreuses paires (Test 3 in `m24_yukawa_test.py`) :
   - $y_d/y_e = 9.14 \approx 2277/252 = 9.04$ (1.13%)
   - $y_s/y_u = 43.29 \approx 990/23 = 43.04$ (0.56%)
   - $y_c/y_s = 13.62 \approx 10395/770 = 13.50$ (0.84%)
   - $y_b/y_c = 3.29 \approx 5796/1771 = 3.27$ (0.40%)
   - $y_t/y_b = 41.26 \approx 10395/252 = 41.25$ (**0.01%**) ★

3. **Le Null C montre qu'avec d "designed", on peut fitter à $\alpha = 2$ et précision <0.5%.** Donc M_24 n'est pas optimal physiquement, mais offre quand même un fit acceptable.

4. **Restricted to McKay-Mathieu coefficients** ($1, 45, 231, 770, 2277, 5796, 10395, 13915, 30843$), le fit est MAUVAIS (mean err > 50%, alpha = 1.24). Donc ce ne sont **pas** les coefficients McKay qui matchent, mais l'ENSEMBLE des dim M_24 distinctes.

**Verdict H3 : TIER 3 motivated** ($M_{24}$ irrep dims donnent un fit statistiquement significatif et un ratio frappant $y_t/y_b \approx 10395/252$ à 0.01%, mais sans alpha physique propre).

---

## 4. Mathématique théorique : pourquoi ces résultats ?

### 4.1 Structure modulaire du Frobenius (H1 partial answer)

Le Frobenius sur le Fermat quartic se décompose géométriquement :

$$H^2(X, \mathbb{Q}_\ell) = NS(X) \otimes \mathbb{Q}_\ell \oplus T(X) \otimes \mathbb{Q}_\ell$$

avec $\text{rank}(NS) = 20$ (pour $\bar{\mathbb{F}}_p$) et $\text{rank}(T) = 2$.

Le **NS** porte une action de Frob qui fixe la classe hyperplane $H$ (valeur propre $+p$, multiplicité 1) et un autre cycle Galois-stable (Hodge classe), donnant le `+2p` observé pour $p \equiv 3 \pmod 4$.

Le **T** porte un Hecke Grossencharacter $\psi$ sur $\mathbb{Q}(\zeta_8)$ de type $(\infty)$ avec exposant cohomologique. Pour $p \equiv 3 \pmod 4$, $\psi$ s'annule (caractère d'ordre 4 trivialisé), donc contribution 0.

**Pas de connexion directe avec "primes ECI"** dans cette structure. Les primes apparaissent comme NUMÉRATEURS (modules de valeurs propres) mais leur **séquence ordonnée** ne se relit pas dans la suite des $a_p$.

### 4.2 Décomposition Mathieu Moonshine du K3 elliptic genus (H3 partial answer)

L'elliptic genus de K3 est :

$$\chi_{K3}(\tau, z) = 2\phi_{0,1}(\tau, z)$$

où $\phi_{0,1}$ est la première forme de Jacobi de poids 0 indice 1.

EOT 2010 ont observé que la décomposition en caractères $\mathcal{N}=4$ donne :

$$\chi_{K3}(\tau, z) = 24 \mu(\tau, z) + 2 \cdot \sum_{n \geq 0} A_n \, q^{n-1/8} \cdot \chi_n(\tau, z)$$

avec $A_1 = 90 = 2 \cdot 45$, $A_2 = 462 = 2 \cdot 231$, $A_3 = 1540 = 2 \cdot 770$, $A_4 = 4554 = 2 \cdot 2277$, $A_5 = 11592 = 2 \cdot 5796$, et $A_n/2$ se décompose toujours en sommes de dim M_24 irreps.

Ceci définit une **structure additive** dim$(M_{24}$-rep$)$ → coefficient Fourier elliptic genus K3. Mais le passage à **Yukawa $y_f = $ overlap d'states $\langle \psi_i | F^{(f)} | \psi_j \rangle$** demande un mécanisme PHYSIQUE non trivial.

Une hypothèse possible : si chaque fermion correspond à une **représentation BPS spécifique** dans la $\mathcal{N}=4$ sigma-model K3, et si l'overlap entre l'état Higgs et cet état BPS est proportionnel à $1/\dim$ (par mesure de Haar normalisée sur l'orbite M_24), alors $y_f = c/\dim(\rho_f)$.

**Problème** : la $\mathcal{N}=4$ K3 model est 2D, pas 4D phénoménologique. Le pont via M-théorie sur K3 × $\mathbb{R}^{1,2}$ ou heterotic-Type IIA duality est conjectural. Aucun mécanisme rigoureux ne donne $\alpha = 3.50$.

### 4.3 Sur les "premiers" comme spectre arithmétique

**Théorème heuristique (pas démontré rigoureusement)** : si $X = K3$ avec structure CM par $K = \mathbb{Q}(\zeta_8)$, alors les primes $p$ "rationnels" se décomposent dans $\mathcal{O}_K$ selon $p \bmod 8$ :
- $p \equiv 1 \pmod 8$ : $p$ se décompose en 4 idéaux premiers (split complet)
- $p \equiv 7 \pmod 8$ : 2 idéaux premiers
- $p \equiv 3, 5 \pmod 8$ : 1 idéal premier
- $p = 2$ : ramifié

Et le **Frobenius "élémentaire"** sur la $T$-part agit via $\psi(\mathfrak{p})$ pour $\mathfrak{p}$ au-dessus de $p$.

La séquence canonique de primes 2, 3, 5, 7, 11, ... **ne reflète pas** directement cette décomposition. Pour l'encoder, on aurait besoin d'une fonction $f(p)$ choisie spécifiquement, pas la suite naïve.

**Donc** : "primes ECI" comme **labeling structural** des générateurs gauge n'a pas d'analogue arithmétique direct sur K3. La séquence des premiers est trop "amorphe" pour porter un sens géométrique précis.

---

## 5. Tests sur Kummer K3 (variante)

Pour vérifier que les résultats ne sont pas spécifiques à la Fermat quartic, on a calculé `Km(E_a × E_a)` avec $E_a : y^2 = x^3 - x$ (Cremona 32a2, CM par $\mathbb{Z}[i]$).

Les coefficients transcendantal (formule $a_p = a_p(E_a)^2 - 2p$) :

| $p$ | $a_p(E_a)$ | $a_p^{\text{trans}}$ Kummer |
|-----|-----------:|----------------------------:|
| 3   | 0          | -6                          |
| 5   | -2         | -6                          |
| 7   | 0          | -14                         |
| 11  | 0          | -22                         |
| 13  | 6          | 10                          |
| 17  | 2          | -30                         |
| 19  | 0          | -38                         |
| 23  | 0          | -46                         |
| 29  | -10        | 42                          |
| 31  | 0          | -62                         |
| 37  | -2         | -70                         |
| 41  | 10         | 18                          |
| 43  | 0          | -86                         |
| 47  | 0          | -94                         |

Note remarquable : $a_p^{\text{trans}} = -2p$ pour $p \equiv 3 \pmod 4$ (puisque $a_p(E_a) = 0$ pour ces $p$), exactement le **négatif** du Fermat quartic pour ces primes.

**Cela suggère** que les deux K3 sont reliés par un twist quadratique (caractère $\chi_{-4}$). Le pattern $\text{Tr} \propto p$ est universel pour les K3 CM.

Aucun nouveau lien avec ECI primes émergent.

---

## 6. Plan calculatoire et roadmap

### 6.1 Si les tests positifs : Phase 2 paper "ECI as arithmetic code on K3"

Vu nos résultats :
- H1 : **INCONCLUSIVE / TIER 3** (pas significant statistiquement)
- H3 : **TIER 3 motivated** (significant vs random log-uniform, mais α physique manque)

Le paper Phase 2 ne tient PAS sur ces résultats seuls. Il faudrait au minimum :
1. **Identifier explicitement** le Hecke Grossencharacter de la Fermat quartic K3 et tester si ses coefficients individuels (séparés du NS contribution) matchent un pattern ECI.
2. **Dériver $\alpha$ théoriquement** dans H3. Pour $\alpha = 3.5 \approx 7/2$, peut-être un argument BPS (1/2 BPS spectrum + 3 dimensions instanton). Sinon, H3 reste numérique.
3. **Calculer Spec(D̸) explicit** sur Kummer K3 avec twist $[F]$ et tester si les eigenvalues reproduisent la suite des dim$(M_{24}$-reps$)$.

### 6.2 Tests futurs prioritaires (si poursuite)

| Test | Calcul | ETA | Critère verdict |
|------|--------|-----|----------------|
| T1 | Compute $\#X(\mathbb{F}_{p^2})$ to get $\text{Tr}(\text{Frob}^2)$ | 1 jour PARI | Sépare NS vs T spectra |
| T2 | Identify Grossencharacter Fermat quartic | 3-5 jours | Donne **degré-4 L-fn** rationnelle |
| T3 | Compute K3 with rank-19 Picard (one trans more) | 1 semaine | Cross-check $\alpha$ et ratios |
| T4 | $D̸$ spectrum on Kummer K3 numerically | 2-4 semaines (lattice) | Test direct $\lambda_n$ vs dim M_24 |
| T5 | Test ECI primes labeling on **other CY surfaces** | 2-3 semaines | Universality / specific to K3 ? |

### 6.3 Si tests futurs négatifs : alternative variétés

Candidats si K3 ne marche pas :
- **CY3 quintic** $X_5 \subset \mathbb{P}^4$ (rank du module 100, plus rich)
- **Hyperkähler $\text{K3}^{[n]}$** (Hilbert scheme de $n$ points sur K3)
- **Moduli space des CY3** avec mirror symmetry

### 6.4 Honnête : que faire SI on ne dérive rien ?

L'observation cosmologique $\Lambda \sim \exp(-\Sigma_{14}$ premiers$)$ et $M_{Pl}^2/v^2 \sim \exp(+\Sigma_8$ premiers$)$ reste un **PATTERN EMPIRIQUE FRAPPANT** sans mécanisme dérivé. Si après 6 mois on ne trouve pas de mécanisme arithmétique propre, alors la valeur ECI reste dans les hits TIER 1 individuels ($m_H$, Koide) et les patterns cosmologiques sont à publier comme **observation** (pas TOE).

---

## 7. Bilan et TIER classification

### H1 (Frobenius K3 = ECI primes)

**Verdict : TIER 3 → LIKELY COINCIDENCE**

- Structure modulaire confirmée (Frobenius = 2p pour p ≡ 3 mod 4) — élégant mais pas ECI-specific
- Σ partial a_p match Σ first k primes pour k=6 (1.06%) et k=13 (0.19%) — mais 23% des trials random font aussi bien
- ζ(3) coincidence (1.2035 ≈ 1.2021 à 0.12%) — artefact de linéarisation, vrai écart 1.6%
- **Le labeling "primes ↔ générateurs Lie" n'est pas dérivable de l'arithmétique K3**

### H3 (Yukawa = 1/dim M_24)

**Verdict : TIER 3 MOTIVATED → INTRIGUING BUT INCOMPLETE**

- Best fit avec 9 dim M_24 → α=3.50, max error 47% (pour $y_u$), max log residual = 0.38
- Statistiquement significatif vs random log-uniform (0% des trials battent)
- Plusieurs ratios Yukawa matchent ratios M_24 à <1% (notamment $y_t/y_b = 0.01\%$)
- **MAIS** : Null C montre que dim "designed" pour α=2 donnent fit meilleur (score 0.022 vs 0.285) — M_24 n'est pas optimal
- **MAIS** : $\alpha = 3.50$ n'a pas d'interprétation physique évidente
- **MAIS** : Restricted to McKay coefficients (les vraies dim qui apparaissent dans EOT decomposition) → MAUVAIS fit, prouvant que H3 originale "dim M_24 directement" est faussée

**Interprétation honnête** : Le succès partiel vient de l'**espacement logarithmique** des dim M_24 sur le range $[1, 10395]$, qui couvre 5 ordres de magnitude — comparable au range des Yukawa. Ce n'est probablement pas une signature de **physique M_24** mais d'une **bonne couverture du log-range**.

### Synthèse

Aucune des deux hypothèses (H1 ou H3) ne tient comme TIER 1/2 rigoureux. Les deux sont des **patterns numériques intéressants** (TIER 3) qui méritent investigation supplémentaire mais ne fondent pas en l'état un "code arithmétique K3" pour le SM.

Le résultat fort de la session reste : **le Frobenius sur Fermat quartic se factorise élégamment** (Tr = 2p pour p ≡ 3 mod 4), démontrant que les K3 portent une **structure modulaire profonde** — cohérente avec le programme Beilinson/Schoen — mais **sans lien direct identifiable** avec la séquence des "primes ECI".

---

## 8. P(ECI cadre tient) — Update

| Avant cette session | Après |
|--------------------|-------|
| 70-80% (post-pattern universel) | **65-75%** (légère baisse) |

**Raisons de la baisse** :
- H1 testé rigoureusement et trouvé non-significatif statistiquement → réduit confiance dans "primes = code arithmétique"
- H3 partiel mais insufficient → pas de dérivation Yukawa

**Raisons de stabilité** :
- m_H = κ(SU(2)) · v reste TIER 1 inchangé
- Koide K = 2/3 reste TIER 1 inchangé
- Structure modulaire K3 est confirmée → ouvre d'autres pistes (CM newforms etc.)

**P(ECI = code K3 arithmétique)** : 10-20% (basé sur ces tests).
**P(ECI = code algébrique général, K3 ou autre)** : 30-50%.

---

## 9. Annexe — Fichiers calculatoires

Tous les scripts sont dans `/root/cc-private/papers/2026-05-24-session/synthesis/eci_pari_k3/` :

| Fichier | Description | Output principal |
|---------|-------------|------------------|
| `fermat_quartic_v2.gp` | PARI/GP comptage Fermat quartic | Table Tr(Frob|H²) p=3..47 |
| `fermat_quartic_v3.gp` | Extension primes | p=31..47, log-derivative L-fn |
| `kummer_test.gp` | Kummer Km(E_a × E_a) | a_p transcendental |
| `cm_newform_test.gp` | Identification CM newform | 16.3.b.a confirmé |
| `cm_newform_identify.gp` | Eigenbasis level 32 | 4 newforms identifiés |
| `zeta_K3_v2.gp` | Test Sym²(E_a) vs Fermat | Pas de match constant |
| `m24_eot_test.py` | M_24 reps vs Yukawa | Best assignment table |
| `eot_yukawa_full.py` | Brute force 167960 combos | α=3.50, score 0.285 |
| `h3_fast_null.py` | Adversarial null tests | Real bat 100% random |
| `selberg_lite.py` | Selberg trace T^4 | r_4(n) multiplicities |
| `zeta3_test.py` | L(K3, 3) vs ζ(3) | 1.6% off (quadratic) |
| `ratio_test.py` | Convergence L_partial | Ratio 0.78 ≈ 7/9 |
| `h1_significance.py` | Adversarial H1 | 23% random battent |

---

## 10. Pour le prochain Opus / DS

### Tâches dispatchables

1. **WebFetch arXiv complet de EOT 2010** (1004.0956) pour vérifier la table de décomposition exacte McKay-Mathieu A_n levels 1-20.
2. **Cross-check** : LMFDB pour newform 16.3.b.a — confirmer level/weight/character/eigenvalues.
3. **Calcul Tr(Frob² | H²)** sur Fermat quartic via comptage sur $\mathbb{F}_{p^2}$ pour p=3..13 (PARI 1-2h).
4. **Identification du Hecke Grossencharacter** du Fermat quartic transcendental (référence : Schoen 1988 ou Yui 2013 K3 modular).
5. **Test ECI sur ζ K3 résidu** : calcul de $L'(K3, 0)$ ou $L(K3, 2)$ et comparaison avec constantes ECI ($\zeta(3)/\sqrt{\pi}$, $\pi/(1-\kappa)$, etc.).
6. **Si possible** : compute Spec($\Delta$) sur Kummer K3 avec **metric flat** (KZ approximation) — pour voir si les eigenvalues du Laplacien forment une "séquence reconnaissable".

### Recommandations stratégiques

- **Suspendre la branche "primes ECI = arithmétique K3"** : statistiquement non-significatif, dérive plus consommatrice de temps que productive.
- **Préserver branch "m_H = κ(SU(2))v + Koide"** : TIER 1 publishable immédiatement.
- **Investiguer alternative** : peut-être les "premiers ECI" ne sont pas Frobenius K3 mais **multiplicités de zero modes Dirac** sur K3 (Atiyah-Singer index), qui sont aussi des entiers structurés.
- **Considérer abandon de la connexion stricte primes ↔ dim G** : peut-être seulement les valeurs Σ premiers sont matching par hasard cosmologique (anthropic / multivers), pas un mécanisme dynamique.

---

## Conclusion

Cette session de calculs PARI/GP rigoureux a permis de :

1. **Confirmer** la structure modulaire profonde du Fermat quartic K3 (Tr Frob = 2p systématique pour p≡3 mod 4)
2. **Identifier** le newform CM associé (16.3.b.a level 16, weight 3, character $\chi_{-4}$)
3. **Tester** rigoureusement H1 (Frobenius vs ECI primes) et trouver l'hypothèse statistiquement non significative
4. **Tester** rigoureusement H3 (Yukawa vs dim M_24) et trouver un fit significatif vs random mais sans interprétation physique propre

Les **résultats TIER 1 de la session précédente** ($m_H = \kappa(SU(2)) \cdot v$ à 0.016%, Koide à 0.9σ) restent **non affectés** par ces tests négatifs. Le programme ECI reste viable sur les "bricks" individuelles validées, même si l'unification arithmétique via K3 ne tient pas en l'état.

P(ECI cadre tient) : **65-75% honest**, sensible aux confirmations futures du programme lattice κ(SU(N)) cross-N et aux dérivations théoriques de κ_∞.

---

*Document généré dans le cadre du programme ECI de Kévin Rémondière. Données et codes reproductibles dans `/root/cc-private/papers/2026-05-24-session/synthesis/eci_pari_k3/`. Toutes les références arXiv vérifiées au moment de l'écriture.*
