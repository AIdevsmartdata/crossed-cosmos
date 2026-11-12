# PARTIE I (versions 1.0 et 1.1, inchangée)

# Concordance texte / Lean (12/11/2026)

Fichier Lean de référence : `TUBE_PONT_v1_0/Paper_TubeBridge_SU2/lean/TubePont_pont_6.lean` (copie de `chantiers/flux_tube_2026-11-11/lean8/tours/pont_6.lean`, sha256 `e0a70f803c73a1b095755ee30ec3175fa98aeb15f445c74a6a86654ef37b8bb6`, 3 091 lignes). Texte de référence : `note/tube_bridge_su2_v1_0.tex`, section 3 (« The twenty-three statements »). Numérotation L01-L23 = ordre de la section 3 ; L19 est l'identité `signedWilsonEnergy_one` (ce n'est pas une inégalité) ; le décompte « 23 théorèmes » du certificat compte 22 théorèmes d'inégalité ou d'existence plus cette identité. Les définitions auxiliaires (`signedWilsonEnergy`, `planeTwist`) ne sont pas comptées.

Règle : toute différence se corrige dans le TEXTE ; aucun fichier de `chantiers/flux_tube_2026-11-11/` n'a été modifié. Verdicts : identique / plus faible / plus fort / différent. Le texte est de la prose mathématique : « identique » signifie mêmes hypothèses et même conclusion, aux conventions de notation près (instances de classes de types omises, notations `plaq`, `sgn` écrites en mots). Contrôle fait par moi (Claude Sonnet 5.5), ligne à ligne, le 12/11/2026 ; une relecture indépendante par GPT-6.1 Sol est décrite dans `RELECTURES.md`.


## L01 `TubeArea.column_flip_bound` (lignes 164-179)

**Énoncé du texte (LaTeX, section 3) :**

> Let $\Omega$ be a measurable space and $E,P$ finite types. Let $\mu$ be a probability measure on $\Omega$. For each $\sigma:E\to\mathbb Z^\times$, let $\tau_\sigma:\Omega\to\Omega$ be measure-preserving. Let $bd:P\to\operatorname{Finset}E$, and write $\operatorname{plaq} bd \sigma p=\prod_{e\in bd p}\sigma(e)$. Assume the map $\sigma\mapsto p\mapsto \operatorname{plaq} bd \sigma p$ is surjective. Let $K:P\to\Omega\to\mathbb R$ be measurable with $|K_p\omega|\le \kappa$, $K_p(\tau_\sigma\omega)=\operatorname{sgn}(\operatorname{plaq} bd \sigma p)K_p\omega$, let $R\ge 0$ be measurable, invariant under every $\tau_\sigma$, with $R\exp(\sum_p K_p)$ integrable, and let $W$ be measurable, $|W|\le 1$, such that $W(\tau_\sigma\omega)=\operatorname{sgn}(\prod_{p\in A}\operatorname{plaq} bd \sigma p)W\omega$. Then
> \[
> \Bigl|\int W\,R\,e^{\sum_p K_p}\,d\mu\Bigr|
> \le (\tanh\kappa)^{|A|}\int R\,e^{\sum_p K_p}\,d\mu .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
164: theorem column_flip_bound
165:     {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
166:     (μ : Measure Ω) [IsProbabilityMeasure μ]
167:     (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
168:     (bd : P → Finset E)
169:     (hsurj : Function.Surjective (fun σ : E → ℤˣ => plaq bd σ))
170:     (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
171:     (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
172:     (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
173:     (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
174:     (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
175:     (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
176:     (A : Finset P)
177:     (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
178:     |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
179:       ≤ Real.tanh κ ^ A.card * ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
```

**Verdict : identical.** Same hypotheses (hsurj, hKτ, hRτ, hWτ, integrability of R·exp(ΣK)), same conclusion; the note writes plaq and sgn in words. The note adds in Section 4 the remark that kappa >= 0 is forced when P is non-empty (not a hypothesis).


## L02 `TubeArea.sharp_one_edge` (lignes 316-320)

**Énoncé du texte (LaTeX, section 3) :**

> For every real $J$ there exists a probability measure $\mu$ on $\mathbb Z^\times$ such that, for every $u\in\mathbb Z^\times$, multiplication by $u$ preserves $\mu$, and
> \[
> \int \operatorname{sgn}\omega\, e^{J\operatorname{sgn}\omega}\,d\mu
> =\tanh J \int e^{J\operatorname{sgn}\omega}\,d\mu,\qquad
> \int e^{J\operatorname{sgn}\omega}\,d\mu>0.
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
316: theorem sharp_one_edge (J : ℝ) :
317:     ∃ μ : Measure ℤˣ, IsProbabilityMeasure μ ∧
318:       (∀ u : ℤˣ, MeasurePreserving (fun ω : ℤˣ => u * ω) μ μ) ∧
319:       (∫ ω, sgn ω * Real.exp (J * sgn ω) ∂μ = Real.tanh J * ∫ ω, Real.exp (J * sgn ω) ∂μ) ∧
320:       0 < ∫ ω, Real.exp (J * sgn ω) ∂μ := by
```

**Verdict : identical.** Existential statement for every real J, uniform measure on {±1}; the equality for J = kappa >= 0 in Section 4 is a reading, not an extra claim.


## L03 `TubeArea.wilson_column_flip_bound` (lignes 621-647)

**Énoncé du texte (LaTeX, section 3) :**

> Let $G$ be a group with measurable multiplication and inverse, and let $\operatorname{haar}_G$ be a left-invariant probability measure on $G$. Let $z\in G$ satisfy $z^2=1$ and be central. Let $\chi:G\to\mathbb R$ be measurable, $|\chi|\le 1$, and $\chi(z g)=-\chi(g)$. Let $E,F,X,P$ be finite. A \emph{WilsonConfig} $G E F X$ is a configuration of group elements on the long links $E\times F$ and the auxiliary links $X$; $\operatorname{wilsonMeasure}\operatorname{haar}_G$ is the product of $\operatorname{haar}_G$ over all link variables. The map $\operatorname{columnFlip} z \sigma$ changes a configuration by left-multiplying the long-link variables of columns with $\sigma(e)=-1$ by $z$. For $w:P\to\operatorname{List}(E\times\operatorname{Bool})$ with each first-coordinate list duplication-free, $c:P\to F\to\mathbb R$ with $|c p y|\le 1$, $\beta\ge 0$, the coupling $\operatorname{wilsonCoupling} \beta c \chi w p \omega$ is $\beta\sum_y c p y\,\chi(\text{holonomy of }w p\text{ at }y)$. Let $R$ be measurable, nonnegative, invariant under $\operatorname{columnFlip} z\sigma$ for all $\sigma$, with $R\exp(\sum_p\operatorname{wilsonCoupling}\beta c \chi w p)$ integrable. Let $w_C$ be a duplication-free word, $y_0\in F$, and $A\subseteq P$ finite. Assume the Stokes boundary condition: for all $\sigma$,
> \[
> \prod_{e\in\operatorname{wordBoundary}w_C}\sigma(e)
> =\prod_{p\in A}\operatorname{plaq}\bigl(p\mapsto \operatorname{wordBoundary}(w p)\bigr)\sigma p,
> \]
> and assume surjectivity of the corresponding plaquette-sign map. Write $K_p=\operatorname{wilsonCoupling}\beta\,c\,\chi\,w\,p$, $\Phi=R\,e^{\sum_pK_p}$ and $\mu_W=\operatorname{wilsonMeasure}$. Then
> \[
> \Bigl|\int \operatorname{wilsonLoop}\chi\,w_C\,y_0\;\Phi\,d\mu_W\Bigr|
> \le \tanh(\beta|F|)^{|A|}\int \Phi\,d\mu_W .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
621: theorem wilson_column_flip_bound
622:     {G E F X P : Type*} [Group G] [MeasurableSpace G]
623:     [MeasurableMul₂ G] [MeasurableInv G]
624:     [Fintype E] [DecidableEq E] [Fintype F] [Fintype X]
625:     [Fintype P] [DecidableEq P]
626:     (haarG : Measure G) [IsProbabilityMeasure haarG]
627:     (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
628:     (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
629:     (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
630:     (hodd : ∀ g, chi (z * g) = -chi g)
631:     (w : P → List (E × Bool)) (hw : ∀ p, ((w p).map Prod.fst).Nodup)
632:     (c : P → F → ℝ) (hc : ∀ p y, |c p y| ≤ 1)
633:     (β : ℝ) (hβ : 0 ≤ β)
634:     (R : WilsonConfig G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
635:     (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
636:     (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω))
637:       (wilsonMeasure haarG))
638:     (wC : List (E × Bool)) (hwC : (wC.map Prod.fst).Nodup) (y0 : F)
639:     (A : Finset P)
640:     (hStokes : ∀ σ : E → ℤˣ,
641:       (∏ e ∈ wordBoundary wC, σ e) = ∏ p ∈ A, plaq (fun p => wordBoundary (w p)) σ p)
642:     (hsurj : Function.Surjective
643:       (fun σ : E → ℤˣ => plaq (fun p => wordBoundary (w p)) σ)) :
644:     |∫ ω, wilsonLoop chi wC y0 ω *
645:         (R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω)) ∂wilsonMeasure haarG|
646:       ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ A.card *
647:         ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG := by
```

**Verdict : identical.** Typeclass assumptions (Fintype, DecidableEq, MeasurableMul₂, MeasurableInv) omitted in the prose; all hypotheses of the Lean text listed: left-invariance, z²=1, z central, chi measurable/bounded/odd, nodup words, |c|<=1, beta>=0, R measurable/nonneg/flip-invariant/integrable, nodup loop word, Stokes, surjectivity.


## L04 `TubeArea.grid_plaq_surjective` (lignes 738-739)

**Énoncé du texte (LaTeX, section 3) :**

> For natural numbers $m,n$, $\operatorname{GridEdge} m n$ is the finite set of edges of the rectangular $m\times n$ grid and $\operatorname{gridBd}p$ is the four-edge boundary of the plaquette $p$. The map
> \[
> \sigma:\operatorname{GridEdge} m n\to \mathbb Z^\times
> \;\longmapsto\;
> p\mapsto \operatorname{plaq}\operatorname{gridBd}\sigma p
> \]
> is surjective.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
738: theorem grid_plaq_surjective (m n : ℕ) :
739:     Function.Surjective (fun σ : GridEdge m n → ℤˣ => plaq gridBd σ) := by
```

**Verdict : identical.** No hypothesis on m, n (m = 0 or n = 0 allowed).


## L05 `TubeArea.grid_stokes_rectangle` (lignes 1108-1111)

**Énoncé du texte (LaTeX, section 3) :**

> Let $a,b:\operatorname{Fin}(m+1)$, $c,d:\operatorname{Fin}(n+1)$ with $a<b$ and $c<d$. The set $\operatorname{rectPlaquettes}a b c d$ is the set of plaquettes in the rectangle $[a,b)\times[c,d)$, and $\operatorname{rectBoundary}a b c d$ is its boundary-edge set. For every $\sigma:\operatorname{GridEdge} m n\to \mathbb Z^\times$,
> \[
> \prod_{e\in\operatorname{rectBoundary}a b c d}\sigma(e)
> =\prod_{p\in\operatorname{rectPlaquettes}a b c d}\operatorname{plaq}\operatorname{gridBd}\sigma p .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1108: theorem grid_stokes_rectangle {m n : ℕ} (a b : Fin (m + 1)) (c d : Fin (n + 1))
1109:     (hab : a.val < b.val) (hcd : c.val < d.val) (σ : GridEdge m n → ℤˣ) :
1110:     (∏ e ∈ rectBoundary a b c d, σ e) =
1111:       ∏ p ∈ rectPlaquettes a b c d, plaq gridBd σ p := by
```

**Verdict : identical.** Strict a < b and c < d as in Lean.


## L06 `TubeArea.tube_area_law_rectangle` (lignes 1121-1145)

**Énoncé du texte (LaTeX, section 3) :**

> With $G,\operatorname{haar}_G,z,\chi$ as in L03, let $m,n\in\mathbb N$, $a,b:\operatorname{Fin}(m+1)$, $c,d:\operatorname{Fin}(n+1)$ with $a<b$, $c<d$, and $y_0\in F$. Let $\operatorname{weights}:(\operatorname{Fin}m\times\operatorname{Fin}n)\to F\to\mathbb R$ satisfy $|\operatorname{weights}\,p\,y|\le 1$, let $\beta\ge0$, and let $R$ be measurable, nonnegative, invariant under every column flip $\operatorname{columnFlip}\,z\,\sigma$ for $\sigma:\operatorname{GridEdge}\,m\,n\to\mathbb Z^\times$, such that $\Phi=R\,e^{\sum_p\operatorname{wilsonCoupling}\beta\operatorname{weights}\chi\operatorname{gridWord}p}$ is integrable. Then
> \[
> \Bigl|\int \operatorname{wilsonLoop}\chi\,(\operatorname{rectWord}a\,b\,c\,d)\,y_0\;\Phi\,d\mu_W\Bigr|
> \le \tanh(\beta|F|)^{(b-a)(d-c)}\int \Phi\,d\mu_W .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1121: theorem tube_area_law_rectangle
1122:     {G F X : Type*} [Group G] [MeasurableSpace G]
1123:     [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X]
1124:     (m n : ℕ) (a b : Fin (m + 1)) (c d : Fin (n + 1))
1125:     (hab : a.val < b.val) (hcd : c.val < d.val)
1126:     (haarG : Measure G) [IsProbabilityMeasure haarG]
1127:     (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
1128:     (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
1129:     (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
1130:     (hodd : ∀ g, chi (z * g) = -chi g)
1131:     (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
1132:     (β : ℝ) (hβ : 0 ≤ β)
1133:     (R : WilsonConfig G (GridEdge m n) F X → ℝ)
1134:     (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
1135:     (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
1136:     (hRint : Integrable
1137:       (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
1138:       (wilsonMeasure haarG))
1139:     (y0 : F) :
1140:     |∫ ω, wilsonLoop chi (rectWord a b c d) y0 ω *
1141:         (R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
1142:         ∂wilsonMeasure haarG| ≤
1143:       Real.tanh (β * (Fintype.card F : ℝ)) ^ ((b.val - a.val) * (d.val - c.val)) *
1144:         ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω)
1145:           ∂wilsonMeasure haarG := by
```

**Verdict : identical.** y0 in F and the integrability of Φ stated; R arbitrary flip-invariant (hypothesis).


## L07 `TubeArea.neutral_word_flip_invariant` (lignes 1257-1261)

**Énoncé du texte (LaTeX, section 3) :**

> A \emph{GeneralWord} $E F X$ is a finite oriented word whose letters are long links $(e,y)$ with $e\in E$, $y\in F$, or auxiliary links $x\in X$; its holonomy is the ordered product with inverses for negative orientations. A word $q$ is \emph{NeutralWord} if the product of the column signs at its long-link occurrences is identically $1$ for every sign assignment. If $G$ is a group, $z$ is a central involution, and $q$ is neutral, then for every $\sigma:E\to\mathbb Z^\times$ and every configuration $\omega$,
> \[
> \operatorname{generalHolonomy}q(\operatorname{columnFlip}z\sigma\,\omega)
> =\operatorname{generalHolonomy}q\,\omega.
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1257: theorem neutral_word_flip_invariant {G E F X : Type*} [Group G] {z : G}
1258:     (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
1259:     (q : GeneralWord E F X) (hq : NeutralWord q)
1260:     (σ : E → ℤˣ) (ω : WilsonConfig G E F X) :
1261:     generalHolonomy q (columnFlip z σ ω) = generalHolonomy q ω := by
```

**Verdict : identical.** No hypothesis on chi; the note says so in Section 2 (neutral = even number of occurrences of each long link; the Lean definition is the sign-product condition, which the note states as the formal definition).


## L08 `TubeArea.mixedWord_neutral` (lignes 1282-1283)

**Énoncé du texte (LaTeX, section 3) :**

> For $e:E$, $y,y':F$, $x,x':X$, the \emph{mixedWord} $e y y' x x'$ is the word consisting of the long link $e$ at $y$, the auxiliary link $x$, the same long link at $y'$ in reverse, and the auxiliary link $x'$ in reverse. This mixed word is neutral.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1282: theorem mixedWord_neutral {E F X : Type*} (e : E) (y y' : F) (x x' : X) :
1283:     NeutralWord (mixedWord e y y' x x') := by
```

**Verdict : identical.** Holds for all e, y, y', x, x' (repeated sites allowed).


## L09 `TubeArea.wilson_action_area_law_rectangle` (lignes 1441-1462)

**Énoncé du texte (LaTeX, section 3) :**

> The weight $\operatorname{neutralActionWeight}\chi\,wq\,coef\,\omega$ is $\exp\bigl(\sum_q coef_q\,\chi(\operatorname{generalHolonomy}(wq_q)\,\omega)\bigr)$. Under the group data of L06 (no weight $R$ is assumed), let $Q$ be finite, $wq:Q\to\operatorname{GeneralWord}(\operatorname{GridEdge}\,m\,n)\,F\,X$ with every $wq_q$ neutral, and $coef:Q\to\mathbb R$. Put $\Psi=\operatorname{neutralActionWeight}\chi\,wq\,coef\cdot e^{\sum_p\operatorname{wilsonCoupling}\beta\operatorname{weights}\chi\operatorname{gridWord}p}$. Then
> \[
> \Bigl|\int \operatorname{wilsonLoop}\chi\,(\operatorname{rectWord}a\,b\,c\,d)\,y_0\;\Psi\,d\mu_W\Bigr|
> \le \tanh(\beta|F|)^{(b-a)(d-c)}\int \Psi\,d\mu_W .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1441: theorem wilson_action_area_law_rectangle
1442:     {G F X Q : Type*} [Group G] [MeasurableSpace G]
1443:     [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X] [Fintype Q]
1444:     (m n : ℕ) (a b : Fin (m + 1)) (c d : Fin (n + 1))
1445:     (hab : a.val < b.val) (hcd : c.val < d.val)
1446:     (haarG : Measure G) [IsProbabilityMeasure haarG]
1447:     (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
1448:     (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
1449:     (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
1450:     (hodd : ∀ g, chi (z * g) = -chi g)
1451:     (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
1452:     (β : ℝ) (hβ : 0 ≤ β)
1453:     (wq : Q → GeneralWord (GridEdge m n) F X)
1454:     (hq : ∀ q, NeutralWord (wq q)) (coef : Q → ℝ) (y0 : F) :
1455:     |∫ ω, wilsonLoop chi (rectWord a b c d) y0 ω *
1456:         (neutralActionWeight chi wq coef ω *
1457:           Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω))
1458:         ∂wilsonMeasure haarG| ≤
1459:       Real.tanh (β * (Fintype.card F : ℝ)) ^ ((b.val - a.val) * (d.val - c.val)) *
1460:         ∫ ω, neutralActionWeight chi wq coef ω *
1461:           Real.exp (∑ p, wilsonCoupling β weights chi gridWord p ω)
1462:           ∂wilsonMeasure haarG := by
```

**Verdict : identical.** No R and no integrability hypothesis in the Lean statement; the weight is the neutral exponential times the base-plaquette exponential.


## L10 `TubeArea.torus_plaq_explicit` (lignes 2178-2182)

**Énoncé du texte (LaTeX, section 3) :**

> Let $m,n\ge2$. $\operatorname{TorusEdge} m n$ is the set of horizontal and vertical edges of the discrete torus $(\mathbb Z/m)\times(\mathbb Z/n)$, written as a sum type, and $\operatorname{torusBd}p$ is the four-edge boundary of the plaquette at $p$. For every $\sigma:\operatorname{TorusEdge} m n\to\mathbb Z^\times$ and every $p:\operatorname{Fin}m\times\operatorname{Fin}n$,
> \[
> \operatorname{plaq}\operatorname{torusBd}\sigma p
> =
> \sigma(\operatorname{inl}(p_1,p_2))\,
> \sigma(\operatorname{inl}(p_1,\operatorname{finRotate} n\,p_2))\,
> \sigma(\operatorname{inr}(p_1,p_2))\,
> \sigma(\operatorname{inr}(\operatorname{finRotate} m\,p_1,p_2)).
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2178: theorem torus_plaq_explicit {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n)
2179:     (σ : TorusEdge m n → ℤˣ) (p : Fin m × Fin n) :
2180:     plaq torusBd σ p =
2181:       σ (Sum.inl (p.1, p.2)) * σ (Sum.inl (p.1, finRotate n p.2)) *
2182:         σ (Sum.inr (p.1, p.2)) * σ (Sum.inr (finRotate m p.1, p.2)) := by
```

**Verdict : identical.** Periods >= 2; finRotate is the cyclic successor.


## L11 `TubeArea.torus_plaq_parity` (lignes 2211-2212)

**Énoncé du texte (LaTeX, section 3) :**

> For $m,n\ge2$ and every $\sigma:\operatorname{TorusEdge} m n\to\mathbb Z^\times$,
> \[
> \prod_{p:\operatorname{Fin}m\times\operatorname{Fin}n}
> \operatorname{plaq}\operatorname{torusBd}\sigma p=1.
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2211: theorem torus_plaq_parity {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (σ : TorusEdge m n → ℤˣ) :
2212:     ∏ p : Fin m × Fin n, plaq torusBd σ p = 1 := by
```

**Verdict : identical.** Periods >= 2.


## L12 `TubeArea.torus_plaq_image` (lignes 2227-2228)

**Énoncé du texte (LaTeX, section 3) :**

> For $m,n\ge2$, if $t:\operatorname{Fin}m\times\operatorname{Fin}n\to\mathbb Z^\times$ satisfies $\prod_p t p=1$, then there exists $\sigma:\operatorname{TorusEdge} m n\to\mathbb Z^\times$ such that, for every $p$, $\operatorname{plaq}\operatorname{torusBd}\sigma p=t p$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2227: theorem torus_plaq_image {m n : ℕ} (hm : 2 ≤ m) (hn : 2 ≤ n) (t : Fin m × Fin n → ℤˣ)
2228:     (ht : ∏ p, t p = 1) : ∃ σ : TorusEdge m n → ℤˣ, ∀ p, plaq torusBd σ p = t p := by
```

**Verdict : identical.** Periods >= 2; t with product 1.


## L13 `TubeArea.torus_flip_bound` (lignes 1786-1803)

**Énoncé du texte (LaTeX, section 3) :**

> With the same abstract data as L01, but with surjectivity replaced by the parity and image conditions
> \[
> \prod_p\operatorname{plaq}bd\sigma p=1
> \qquad\text{for all }\sigma,
> \]
> and every $t:P\to\mathbb Z^\times$ with $\prod_p t p=1$ is realized by some $\sigma$, the following bound holds:
> \[
> \bigl(1-(\tanh\kappa)^{|P|}\bigr)
> \Bigl|\int W\,R\,e^{\sum_p K_p}\,d\mu\Bigr|
> \le
> \bigl((\tanh\kappa)^{|A|}+(\tanh\kappa)^{|P|-|A|}\bigr)
> \int R\,e^{\sum_p K_p}\,d\mu .
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1786: theorem torus_flip_bound
1787:     {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
1788:     (μ : Measure Ω) [IsProbabilityMeasure μ]
1789:     (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
1790:     (bd : P → Finset E)
1791:     (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq bd σ p = 1)
1792:     (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
1793:     (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
1794:     (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
1795:     (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
1796:     (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
1797:     (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
1798:     (W : Ω → ℝ) (hWm : Measurable W) (hW1 : ∀ ω, |W ω| ≤ 1)
1799:     (A : Finset P)
1800:     (hWτ : ∀ σ ω, W (τ σ ω) = sgn (∏ p ∈ A, plaq bd σ p) * W ω) :
1801:     (1 - Real.tanh κ ^ Fintype.card P) * |∫ ω, W ω * (R ω * Real.exp (∑ p, K p ω)) ∂μ|
1802:       ≤ (Real.tanh κ ^ A.card + Real.tanh κ ^ (Fintype.card P - A.card)) *
1803:           ∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ := by
```

**Verdict : identical.** Closed-surface version of L01 (hpar, himg in place of hsurj); constant (1 - q^N)·|I| <= (q^|A| + q^(N-|A|))·Z with N = card P (natural-number subtraction N - |A| in Lean, harmless since A ⊆ P).


## L14 `TubeArea.twist_ratio_bound` (lignes 1934-1951)

**Énoncé du texte (LaTeX, section 3) :**

> With the same closed-surface data and hypotheses as L13 except that there is no $W$, no $A$ and no $\operatorname{hWm},\operatorname{hW1},\operatorname{hW\tau}$, and with a distinguished plaquette $p_0:P$, let $Z_0=\int R\,e^{\sum_p K_p}\,d\mu$ and let $Z_1$ be the same integral with $K_{p_0}$ replaced by $-K_{p_0}$. Then
> \[
> |Z_0-Z_1|
> \le
> (\tanh\kappa)^{|P|}(Z_0+Z_1).
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
1934: theorem twist_ratio_bound
1935:     {Ω E P : Type*} [MeasurableSpace Ω] [Fintype E] [DecidableEq E] [Fintype P] [DecidableEq P]
1936:     (μ : Measure Ω) [IsProbabilityMeasure μ]
1937:     (τ : (E → ℤˣ) → Ω → Ω) (hτ : ∀ σ, MeasurePreserving (τ σ) μ μ)
1938:     (bd : P → Finset E)
1939:     (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq bd σ p = 1)
1940:     (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 → ∃ σ : E → ℤˣ, ∀ p, plaq bd σ p = t p)
1941:     (K : P → Ω → ℝ) (hKm : ∀ p, Measurable (K p))
1942:     (κ : ℝ) (hK : ∀ p ω, |K p ω| ≤ κ)
1943:     (hKτ : ∀ σ p ω, K p (τ σ ω) = sgn (plaq bd σ p) * K p ω)
1944:     (R : Ω → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω) (hRτ : ∀ σ ω, R (τ σ ω) = R ω)
1945:     (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, K p ω)) μ)
1946:     (p₀ : P) :
1947:     |(∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
1948:         - ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ|
1949:       ≤ Real.tanh κ ^ Fintype.card P *
1950:         ((∫ ω, R ω * Real.exp (∑ p, K p ω) ∂μ)
1951:           + ∫ ω, R ω * Real.exp (∑ p, (if p = p₀ then -(K p ω) else K p ω)) ∂μ) := by
```

**Verdict : identical.** After correction of the text on 12/11: the text first said "same hypotheses as L13", which included an observable W and a set A absent from the Lean statement; the text now says there is no W and no A.


## L15 `TubeArea.le_of_forall_pow_le_const_mul_pow` (lignes 2047-2048)

**Énoncé du texte (LaTeX, section 3) :**

> If $a,b,M$ are real numbers with $0\le a$, $0\le b$, $0<M$, and $a^n\le M b^n$ for every positive natural number $n$, then $a\le b$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2047: theorem le_of_forall_pow_le_const_mul_pow (a b M : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hM : 0 < M)
2048:     (h : ∀ n : ℕ, 0 < n → a ^ n ≤ M * b ^ n) : a ≤ b := by
```

**Verdict : identical.** 


## L16 `TubeArea.flux_gap_of_traces` (lignes 2068-2074)

**Énoncé du texte (LaTeX, section 3) :**

> Let $\ell\in\mathbb N$, $q,\lambda_0,\lambda_1,D\in\mathbb R$ with $q,\lambda_0,\lambda_1\ge0$ and $D>0$. Let $Ev,Od:\mathbb N\to\mathbb R$ satisfy, for every positive $n$,
> \[
> \lambda_1^n\le Od(n),\qquad Ev(n)\le D\lambda_0^n,\qquad
> Od(n)\le q^{n\ell}Ev(n).
> \]
> Then $\lambda_1\le q^{\ell}\lambda_0$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2068: theorem flux_gap_of_traces (ℓ : ℕ) (q lam0 lam1 D : ℝ)
2069:     (hq : 0 ≤ q) (h0 : 0 ≤ lam0) (h1 : 0 ≤ lam1) (hD : 0 < D)
2070:     (Ev Od : ℕ → ℝ)
2071:     (hOd : ∀ n : ℕ, 0 < n → lam1 ^ n ≤ Od n)
2072:     (hEv : ∀ n : ℕ, 0 < n → Ev n ≤ D * lam0 ^ n)
2073:     (hratio : ∀ n : ℕ, 0 < n → Od n ≤ q ^ (n * ℓ) * Ev n) :
2074:     lam1 ≤ q ^ ℓ * lam0 := by
```

**Verdict : identical.** Holds for all n >= 1 (not n >= 2); the note says in Section 5 that it is not applied literally.


## L17 `TubeArea.wilson_twist_ratio_bound` (lignes 2295-2322)

**Énoncé du texte (LaTeX, section 3) :**

> Retain the group, coupling and remaining-weight data and hypotheses of L03 (including $\beta\ge0$, $|c|\le1$ and the flip-invariant integrable $R$), omit the loop word $w_C$, the site $y_0$, the set $A$ and the Stokes condition, and replace surjectivity by the parity and image conditions
> \[
> \prod_p\operatorname{plaq}\bigl(p\mapsto\operatorname{wordBoundary}(w p)\bigr)\sigma p=1
> \qquad\text{for all }\sigma,
> \]
> and every $t:P\to\mathbb Z^\times$ with $\prod_p t p=1$ is realized, let $p_0:P$. Then
> \[
> |Z_0-Z_1|
> \le
> (\tanh(\beta|F|))^{|P|}(Z_0+Z_1),
> \]
> where $Z_0=\int R\,e^{\sum_p\operatorname{wilsonCoupling}\beta c\chi w p}\,d\operatorname{wilsonMeasure}$ and $Z_1$ is the same integral with $c p_0$ replaced by $-c p_0$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2295: theorem wilson_twist_ratio_bound
2296:     {G E F X P : Type*} [Group G] [MeasurableSpace G]
2297:     [MeasurableMul₂ G] [MeasurableInv G]
2298:     [Fintype E] [DecidableEq E] [Fintype F] [Fintype X]
2299:     [Fintype P] [DecidableEq P]
2300:     (haarG : Measure G) [IsProbabilityMeasure haarG]
2301:     (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
2302:     (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
2303:     (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
2304:     (hodd : ∀ g, chi (z * g) = -chi g)
2305:     (w : P → List (E × Bool)) (hw : ∀ p, ((w p).map Prod.fst).Nodup)
2306:     (c : P → F → ℝ) (hc : ∀ p y, |c p y| ≤ 1)
2307:     (β : ℝ) (hβ : 0 ≤ β)
2308:     (R : WilsonConfig G E F X → ℝ) (hRm : Measurable R) (hR0 : ∀ ω, 0 ≤ R ω)
2309:     (hRflip : ∀ σ ω, R (columnFlip z σ ω) = R ω)
2310:     (hRint : Integrable (fun ω => R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω))
2311:       (wilsonMeasure haarG))
2312:     (hpar : ∀ σ : E → ℤˣ, ∏ p, plaq (fun p => wordBoundary (w p)) σ p = 1)
2313:     (himg : ∀ t : P → ℤˣ, ∏ p, t p = 1 →
2314:       ∃ σ : E → ℤˣ, ∀ p, plaq (fun p => wordBoundary (w p)) σ p = t p)
2315:     (p₀ : P) :
2316:     |(∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG)
2317:         - ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β
2318:               (fun p y => if p = p₀ then -(c p y) else c p y) chi w p ω) ∂wilsonMeasure haarG|
2319:       ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ Fintype.card P *
2320:         ((∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β c chi w p ω) ∂wilsonMeasure haarG)
2321:           + ∫ ω, R ω * Real.exp (∑ p, wilsonCoupling β
2322:               (fun p y => if p = p₀ then -(c p y) else c p y) chi w p ω) ∂wilsonMeasure haarG) := by
```

**Verdict : identical.** Z1 obtained by negating the weights c p0 y for all y; abstract parity and image hypotheses; no Stokes hypothesis. After Sol's remark (12/11): the text first inherited all of L03 (loop word, y0, A), which is more than the Lean statement has; the text now says which data of L03 are retained and which are omitted.


## L18 `TubeArea.wilson_electric_flux_torus` (lignes 2371-2397)

**Énoncé du texte (LaTeX, section 3) :**

> Let $m,n\ge2$, and let $\operatorname{torusWord}\,p$ be the word around the plaquette with corner $p$ on the torus $(\mathbb Z/m)\times(\mathbb Z/n)$ (bottom, right, top reversed, left reversed, with cyclic successors \lean{finRotate}). With the group data $(G,\operatorname{haar}_G,z,\chi)$ of L06 and with $\operatorname{weights}:(\operatorname{Fin}m\times\operatorname{Fin}n)\to F\to\mathbb R$ bounded by $1$, a finite family $wq:Q\to\operatorname{GeneralWord}(\operatorname{TorusEdge}\,m\,n)\,F\,X$ of neutral words, coefficients $coef:Q\to\mathbb R$, $\beta\ge0$ and a plaquette $p_0$,
> \[
> |Z_0-Z_1|\le\tanh(\beta|F|)^{mn}(Z_0+Z_1),
> \]
> where $Z_0=\int\operatorname{neutralActionWeight}\chi\,wq\,coef\cdot e^{\sum_p\operatorname{wilsonCoupling}\beta\operatorname{weights}\chi\operatorname{torusWord}p}\,d\mu_W$ and $Z_1$ is the same integral with the weights $\operatorname{weights}\,p_0\,y$ negated for all $y$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2371: theorem wilson_electric_flux_torus
2372:     {G F X Q : Type*} [Group G] [MeasurableSpace G]
2373:     [MeasurableMul₂ G] [MeasurableInv G] [Fintype F] [Fintype X] [Fintype Q]
2374:     (m n : ℕ) (hm : 2 ≤ m) (hn : 2 ≤ n)
2375:     (haarG : Measure G) [IsProbabilityMeasure haarG]
2376:     (hleft : ∀ g : G, MeasurePreserving (fun h : G => g * h) haarG haarG)
2377:     (z : G) (hz : z * z = 1) (hcentral : ∀ g : G, z * g = g * z)
2378:     (chi : G → ℝ) (hchim : Measurable chi) (hchi1 : ∀ g, |chi g| ≤ 1)
2379:     (hodd : ∀ g, chi (z * g) = -chi g)
2380:     (weights : (Fin m × Fin n) → F → ℝ) (hweights : ∀ p y, |weights p y| ≤ 1)
2381:     (β : ℝ) (hβ : 0 ≤ β)
2382:     (wq : Q → GeneralWord (TorusEdge m n) F X)
2383:     (hq : ∀ q, NeutralWord (wq q)) (coef : Q → ℝ)
2384:     (p₀ : Fin m × Fin n) :
2385:     |(∫ ω, neutralActionWeight chi wq coef ω *
2386:           Real.exp (∑ p, wilsonCoupling β weights chi torusWord p ω) ∂wilsonMeasure haarG)
2387:         - ∫ ω, neutralActionWeight chi wq coef ω *
2388:           Real.exp (∑ p, wilsonCoupling β
2389:             (fun p y => if p = p₀ then -(weights p y) else weights p y) chi torusWord p ω)
2390:             ∂wilsonMeasure haarG|
2391:       ≤ Real.tanh (β * (Fintype.card F : ℝ)) ^ (m * n) *
2392:         ((∫ ω, neutralActionWeight chi wq coef ω *
2393:           Real.exp (∑ p, wilsonCoupling β weights chi torusWord p ω) ∂wilsonMeasure haarG)
2394:           + ∫ ω, neutralActionWeight chi wq coef ω *
2395:           Real.exp (∑ p, wilsonCoupling β
2396:             (fun p y => if p = p₀ then -(weights p y) else weights p y) chi torusWord p ω)
2397:             ∂wilsonMeasure haarG) := by
```

**Verdict : identical.** m, n >= 2; neutral family; weights bounded by 1; no hypothesis on R (the weight is the neutral exponential).


## L19 `TubeBridge.signedWilsonEnergy_one` (lignes 2430-2431)

**Énoncé du texte (LaTeX, section 3) :**

> In the OpenAI objects, a \emph{GaugeGroup} is a closed subgroup of a unitary group, and a \emph{Configuration} $g l$ assigns link variables on the four-dimensional periodic lattice of side $l$. The \emph{Wilson energy} is the usual Wilson action, and \emph{signedWilsonEnergy} $s U$ is the sum $\sum_p\bigl(1-s_p\,\tfrac{1}{n+1}\operatorname{Re}\Tr U_p\bigr)$ in which the sign $s_p$ multiplies only the normalised trace term (the constant $1$ is unchanged). For every gauge group $g$, positive natural $l$, and configuration $U$,
> \[
> \operatorname{signedWilsonEnergy}(\operatorname{fun}\_\Rightarrow 1)U
> =\operatorname{wilsonEnergy}U.
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2430: theorem signedWilsonEnergy_one {g : GaugeGroup} {l : ℕ+} (U : Configuration g l) :
2431:     signedWilsonEnergy (fun _ => (1 : ℝ)) U = wilsonEnergy U := by
```

**Verdict : identical.** Identity of two real functions. After Sol's remark (12/11): the text first described the signed energy as the Wilson energy with each plaquette TERM multiplied by the sign, which is wrong (it differs by 2 per negative plaquette); the Lean definition (lines 2424-2428 of the cumulative file) is the sum of 1 - s_p * (trace term), the sign multiplies only the normalised trace term, and the text now says so.


## L20 `TubeBridge.openai_wilson_twist_ratio` (lignes 2863-2875)

**Énoncé du texte (LaTeX, section 3) :**

> The sign function \emph{planeTwist}$(a,b)$ on $\operatorname{Site}\,l\times\operatorname{Directions}$ takes the value $-1$ exactly on the plaquettes in the plane spanned by axes $0$ and $1$ with base coordinates $(a,b)$, and value $1$ elsewhere. Let $g$ be a gauge group whose image contains $-1$, let $l$ be a positive natural with $l\ge2$, let $\beta\ge0$, and let $\operatorname{haar}$ be a left-invariant probability measure on $g.\operatorname{image}$. Then
> \[
> |Z_0-Z_1|\le\tanh(\beta l^2)^{l^2}\,(Z_0+Z_1),
> \]
> where $\mu$ is the product of $\operatorname{haar}$ over all links $\operatorname{Site}\,l\times\operatorname{Axis}$, $Z_0=\int e^{-\beta\operatorname{wilsonEnergy}U}d\mu(U)$ and $Z_1=\int e^{-\beta\operatorname{signedWilsonEnergy}(\operatorname{planeTwist}a\,b)\,U}d\mu(U)$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2863: theorem openai_wilson_twist_ratio (g : GaugeGroup)
2864:     (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image)
2865:     (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β)
2866:     (haar : Measure g.image) [IsProbabilityMeasure haar]
2867:     (hleft : ∀ u : g.image, MeasurePreserving (fun v : g.image => u * v) haar haar)
2868:     (a b : ZMod l.val) :
2869:     |(∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => haar))
2870:         - ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2871:             ∂(Measure.pi fun _ : Site l × Axis => haar)|
2872:       ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
2873:         ((∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => haar))
2874:           + ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2875:               ∂(Measure.pi fun _ : Site l × Axis => haar)) := by
```

**Verdict : identical.** All gauge groups g with -1 in the image; haar a probability measure on g.image, left-invariant; l >= 2; Z0, Z1 integrals w.r.t. Measure.pi; planeTwist(a,b) as defined (sign -1 on directions (0,1) with base coordinates (a,b)).


## L21 `TubeBridge.openai_wilson_twist_ratio_family` (lignes 2914-2923)

**Énoncé du texte (LaTeX, section 3) :**

> A \emph{WilsonFamily} $g$ packages a chosen probability Haar measure $C.\operatorname{haar}$ on $g.\operatorname{image}$. Under the same hypotheses as L20, with $C$ a WilsonFamily for $g$ and $\mu$ the product measure built from $C.\operatorname{haar}$, the same twist-ratio inequality holds for all $a,b:\mathbb Z/l$.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2914: theorem openai_wilson_twist_ratio_family (g : GaugeGroup)
2915:     (hneg : (-1 : UnitaryRepresentation g.n) ∈ g.image) (C : WilsonFamily g)
2916:     (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β) (a b : ZMod l.val) :
2917:     |(∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
2918:         - ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2919:             ∂(Measure.pi fun _ : Site l × Axis => C.haar)|
2920:       ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
2921:         ((∫ U : Configuration g l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
2922:           + ∫ U : Configuration g l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2923:               ∂(Measure.pi fun _ : Site l × Axis => C.haar)) := by
```

**Verdict : identical.** Haar measure of a WilsonFamily; the Lean statement spells out the inequality again.


## L22 `TubeBridge.su2_neg_one_mem` (lignes 2931-2931)

**Énoncé du texte (LaTeX, section 3) :**

> The public OpenAI object $\operatorname{su2}$ contains the negative identity:
> \[
> (-1:\operatorname{UnitaryRepresentation}\operatorname{su2}.n)\in\operatorname{su2}.\operatorname{image}.
> \]

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2931: theorem su2_neg_one_mem : (-1 : UnitaryRepresentation su2.n) ∈ su2.image := by
```

**Verdict : identical.** 


## L23 `TubeBridge.openai_su2_twist_ratio` (lignes 2936-2944)

**Énoncé du texte (LaTeX, section 3) :**

> For every WilsonFamily $C$ for $\operatorname{su2}$, every positive natural $l$ with $l\ge2$, every $\beta\ge0$, and all $a,b:\mathbb Z/l$, with $Z_0,Z_1$ as in L20 and $\mu$ the product of $C.\operatorname{haar}$,
> \[
> |Z_0-Z_1|\le\tanh(\beta l^2)^{l^2}\,(Z_0+Z_1),
> \]
> where $\mu$ is the product of $C.\operatorname{haar}$ over all links and $Z_0,Z_1$ are as in L20.

**Énoncé Lean (copié du fichier, avec numéros de ligne) :**

```lean
2936: theorem openai_su2_twist_ratio (C : WilsonFamily su2)
2937:     (l : ℕ+) (hl : 2 ≤ l.val) (β : ℝ) (hβ : 0 ≤ β) (a b : ZMod l.val) :
2938:     |(∫ U : Configuration su2 l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
2939:         - ∫ U : Configuration su2 l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2940:             ∂(Measure.pi fun _ : Site l × Axis => C.haar)|
2941:       ≤ Real.tanh (β * (l.val : ℝ) ^ 2) ^ (l.val ^ 2) *
2942:         ((∫ U : Configuration su2 l, Real.exp (-β * wilsonEnergy U) ∂(Measure.pi fun _ : Site l × Axis => C.haar))
2943:           + ∫ U : Configuration su2 l, Real.exp (-β * signedWilsonEnergy (planeTwist a b) U)
2944:               ∂(Measure.pi fun _ : Site l × Axis => C.haar)) := by
```

**Verdict : identical.** Statement for su2 and any WilsonFamily su2; no assumption beyond l >= 2 and beta >= 0.

---

# PARTIE II (version 1.2) — Concordance texte / Lean pour la section 6 « The cyclic centre Z_N » (12/11/2026)

Établie par Claude Sonnet 5.5 (NON auteur des énoncés, des preuves Lean ni du théorème), à partir de : `lean/CentreZN/ENONCES_GELES.lean` (sha256 `17f5a9116a37…b863`), des preuves de Sol, de la section « Cyclic centre Z_N » de la note et de la note (section 6). Règle : toute différence se corrige dans le TEXTE.

## 0. Contrôles mécaniques (rejeu, voir `CERTIFICAT_ZN_REJEU.md`)
* Pour les 16 théorèmes, le texte d'énoncé (de `theorem NOM` à `:= by`) du fichier prouvé est identique, au caractère près, à celui du fichier figé ; les définitions de la partie B (`Config`, `configMeasure`, `columnTwist`, `orientedLink`, `Word`, `holonomy`, `charge`, `Neutral`, `baseWord`, `baseCharge`, `coupling`, `termsWeight`, `TorusEdge`, `torusWord`) sont identiques à celles du fichier figé.
* Contrôle plus fort, au niveau des termes du noyau : le fichier figé (avec `sorry`, espace de noms `CentreZNFrozen`) et le fichier prouvé sont élaborés dans le MÊME fichier Lean ; pour chacun des 16 noms, le type de `CentreZNFrozen.NOM`, après remplacement du préfixe, est égal (`Expr` égal) au type de `CentreZN.NOM` : « TYPE-IDENTIQUE » 16 sur 16 (Lean 4.32.0).
* `recover_column_flip_bound` et `recover_twist_ratio_bound` ont, aux espaces près, le texte des réénoncés `enonce_canonique_A` et `enonce_canonique_F2` des pieds de vérification publiés de la v1.1 (`lean/pieds/PIED_D.lean`, `PIED_F.lean`).

## 1. Tableau à seize lignes
Notation : (H_ρ) = « pour tout t ∈ ℂ avec ‖t‖ ≤ κ, ‖Σ_j ζ^{(qj).val} e^{Re(ζ^{j.val} t)}‖ ≤ ρ Σ_j e^{Re(ζ^{j.val} t)} ». « Écart » = différence entre le Lean et l'énoncé de la note.

| # | déclaration `CentreZN.` | ce que dit le Lean, en clair | ce que dit la note | écart |
|---|---|---|---|---|
| 1 | `centre_flip_bound` (A1) | Espace probabilisé mesurable ; famille de transformations τ_s qui préservent μ ; charges chg : S → (ZMod N)^P SURJECTIVE ; couplages complexes T_p mesurables, ‖T_p ω‖ ≤ κ pour tout ω, T_p(τ_s ω) = ζ^{(chg s p).val} T_p ω ; poids R ≥ 0 mesurable invariant, R·exp(Σ Re T_p) intégrable ; W mesurable, ‖W‖ ≤ 1 partout, W(τ_s ω) = ζ^{(q Σ_{p∈A} chg s p).val} W ω ; ρ vérifiant (H_ρ) ; alors ‖∫ W·R·e^{Σ Re T}‖ ≤ ρ^{card A} ∫ R e^{Σ Re T}. ζ^N = 1 seulement (non primitive). | Théorème 6.3 (open surface) : mêmes données, même conclusion. | Aucun. Cas dégénérés couverts par le Lean : P vide (alors A vide, borne 1·∫R, vraie), q = 0 (alors A_0 = S et ρ ≥ 1 est forcé par (H_ρ)), N = 1. Le Lean ne suppose pas κ ≥ 0 ; si P est non vide il est forcé par `hT`. |
| 2 | `twist_ratio_bound` (A2) | Mêmes données sans W ni A ; l'hypothèse de surjectivité est REMPLACÉE par `himg` : toute affectation t : P → ZMod N de somme nulle est un chg s. p₀ ∈ P donné. Z_k = ∫ R·exp(Σ_p Re((si p = p₀ alors ζ^k sinon 1)·T_p)). Conclusion : ‖Σ_k ζ^{(qk).val} Z_k‖ ≤ ρ^{card P} Σ_k Z_k. | Théorème 6.4 (closed surface) : idem. | Aucun. Plus faible en hypothèse que A1 (seulement la somme nulle) ; pas d'hypothèse de parité (la parité n'est pas utilisée). |
| 3 | `rho_crude` (A3) | ζ racine primitive N-ième (`IsPrimitiveRoot ζ N`), q ≠ 0 dans ZMod N, t ∈ ℂ quelconque : ‖A_q(t)‖ ≤ (1 − e^{−2‖t‖}) S(t). | Lemme 6.1(a) (la note ajoute, sur papier, le lemme 6.2 : ρ ≤ tanh κ, qui n'est PAS dans le Lean). | Aucun. Cas N = 1 : q ≠ 0 est impossible dans ZMod 1, énoncé vide, comme dans la note (q ≢ 0). |
| 4 | `rho_two` (A4) | N = 2, ζ = −1, charge « 1 », t ∈ ℂ : ‖A_1(t)‖ ≤ tanh‖t‖·S(t). | Lemme 6.1(b). | Aucun (la note donne même r = \|tanh Re t\| ≤ tanh\|t\| ; le Lean ne contient que l'inégalité). |
| 5 | `sharp_one_plaquette` (A5) | Pour N, ζ (ζ^N = 1), q, t quelconques : il existe une probabilité μ sur ZMod N telle que : les translations préservent μ ; ‖ζ^j t‖ = ‖t‖ ; ‖ζ^{qj}‖ = 1 ; les deux covariances ζ^{s+j} t = ζ^s (ζ^j t) et ζ^{q(s+j)} = ζ^{qs} ζ^{qj} ; ∫ ζ^{qj} e^{Re(ζ^j t)} = N⁻¹ A_q(t) ; ∫ e^{Re(ζ^j t)} = N⁻¹ S(t). | Proposition 6.5 (sharpness) : « les hypothèses du théorème A sont satisfaites avec κ = \|t\| et les deux intégrales valent a_q(t), a_0(t) ; donc la constante optimale est ρ_{N,q}(κ) = sup r ». | RÉDUCTION À NOTER : le Lean énonce les covariances et les deux intégrales, pas la structure complète « données de A1 » (S = ZMod N, chg = identité est implicite dans les covariances) ni la conclusion « constante optimale = sup » ; cette dernière est une déduction de deux lignes (A1 + A5) faite sur papier. Le texte le dit (« Hence… »). |
| 6 | `centre_flip_bound_crude` (A6a) | A1 avec ζ primitive, q ≠ 0, et la constante (1 − e^{−2κ}) à la place de ρ (plus d'hypothèse (H_ρ)). | Fin du théorème 6.3 : « one may take ρ = 1 − e^{−2κ} ». | Aucun. |
| 7 | `twist_ratio_bound_crude` (A6b) | A2 avec ζ primitive, q ≠ 0, constante (1 − e^{−2κ})^{card P}. | Idem. | Aucun. |
| 8 | `recover_column_flip_bound` (A7a) | Texte des énoncés publiés (L01) sans les définitions `plaq`, `sgn` (produit de signes dans ℤˣ converti en réel), DÉDUIT de A1 (N = 2, ζ = −1, q = 1) et A4. | « Return to N = 2 ». | Aucun : texte égal au réénoncé du pied de la v1.1. Le lien entre ce réénoncé et `TubeArea.column_flip_bound` (qui utilise `plaq`, `sgn`) est celui de la v1.1 (même terme après dépliage). |
| 9 | `recover_twist_ratio_bound` (A7b) | Idem pour L14 : avec l'hypothèse de parité `hpar` (inutilisée dans la preuve, d'où l'avertissement de style) ; DÉDUIT de A2 (N = 2) et A4. | Idem. | Aucun. |
| 10 | `mixed_word_neutral` (B0) | Pour TOUT N : ℕ (y compris 0) et tous e, y, y', x, x', le mot [(inl (e,y), +), (inr x, +), (inl (e,y'), −), (inr x', −)] est neutre. | Puce « mixed_word_neutral ». | Le Lean est plus général : N quelconque, y' = y permis. Pas de contradiction. |
| 11 | `wilson_centre_flip_bound` (B1) | Groupe G à multiplication et inverse mesurables, mesure de probabilité haarG invariante à gauche ; z central avec z^N = 1 ; χ mesurable, ‖χ‖ ≤ 1, χ(zg) = ζ χ(g) ; mots de base w_p, poids c_{p,y} (‖c‖ ≤ 1), β ≥ 0 ; R ≥ 0 mesurable invariant par TOUTES les torsions de colonnes, intégrable ; ψ mesurable, ‖ψ‖ ≤ 1, ψ(zg) = ζ^{q.val} ψ(g) ; Stokes (baseCharge wC σ = Σ_{p∈A} baseCharge (w p) σ pour tout σ) ET surjectivité des charges de plaquettes en HYPOTHÈSES ; (H_ρ) à κ = β·card F. Conclusion de A1 pour l'observable ψ(holonomie du mot wC au site y0). | Puce « wilson_centre_flip_bound ». | Aucun. Les deux hypothèses (Stokes, surjectivité) sont des hypothèses, non démontrées pour le réseau : le texte les nomme ainsi. Le Lean ne suppose pas card F > 0. |
| 12 | `torus_charge_explicit` (B2a) | Pour tous m, n, N (N = 0 permis : ZMod 0 = ℤ), σ sur les arêtes du tore : baseCharge(torusWord p) σ = σH(i,j) + σV(i+1,j) − σH(i,j+1) − σV(i,j). | « discrete curl ». | Plus fort (N quelconque). |
| 13 | `torus_charge_sum` (B2b) | Σ_p baseCharge (torusWord p) σ = 0 pour tous m, n, N. | « the charges sum to 0 ». | Plus fort (aucune condition m, n ≥ 2). |
| 14 | `torus_charge_image` (B2c) | m, n ≥ 2, N quelconque, t : Fin m × Fin n → ZMod N de somme nulle : il existe σ avec baseCharge(torusWord p) σ = t p pour tout p. | « if m, n ≥ 2 every assignment of total charge 0 is realised ». | Aucun (N quelconque pour le Lean, N ≥ 1 pour la note). |
| 15 | `wilson_twist_ratio_torus` (B3) | Tore m × n (m, n ≥ 2) × fibre finie F, autres liens X, famille finie Q de mots NEUTRES (`Neutral N (wq k)`) à coefficients complexes, poids ‖weights p y‖ ≤ 1, β ≥ 0 ; Z_k = ∫ termsWeight·exp(Σ_p Re coupling) où les poids du plaquette de base p₀ sont multipliés par ζ^k en TOUT site de fibre ; (H_ρ) à κ = β·card F. Conclusion : ‖Σ_k ζ^{(qk).val} Z_k‖ ≤ ρ^{m·n} Σ_k Z_k. | Dernière puce de la liste « Wilson-type ». | Aucun. ATTENTION : le Lean ne contient pas le réseau 4D ; que les plaquettes (x,(i,j)), i ∈ {0,1}, j ∈ {2,3} soient des mots neutres de la forme de B0 est un argument de la note, sur papier (voir 16 et la Proposition SU(N)). |
| 16 | `wilson_twist_ratio_torus_crude` (B3c) | B3 avec ζ primitive, q ≠ 0, constante (1 − e^{−2βΣ})^{mn}, Σ = card F. | Idem, « ≤ (1 − e^{−2β\|F\|})^{mn} Σ_k Z_k ». | Aucun. |

## 2. Ce que le Lean ne contient pas (et que la note classe « sur papier » ou « conjecture »)
1. Le réseau périodique 4D et SU(N) (aucun SU(N) concret ni mesure de Haar de SU(N) dans la chaîne utilisée) : identification des liens longs, des plaquettes mixtes, de la surjectivité pour l = 2, de la covariance de χ = Tr/N. Sur papier, hypothèses vérifiées une à une dans la note (Proposition SU(N)) ; relues par DeepSeek et GPT-6 Astra (voir `RELECTURES_ZN.md`).
2. Les énoncés sur la constante optimale ρ_{N,q}(κ) = sup_{|t|≤κ} r (déduction de A1 + A5 sur papier), les formes closes (N = 2, N = 4 sur papier ; N ≤ 8 calculé ; conjecture générale).
3. La composition avec le Théorème 2 de Kanazawa (sa partie « boucle de Wilson ≤ projecteurs de flux » est de lui ; non formalisée).
4. Les définitions de la note (r_{N,q}, ρ_{N,q}) n'existent pas dans le Lean ; seule (H_ρ) y figure.
