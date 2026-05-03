# Diamond Master Equation as a partial functor — formal report

**Status (2026-05-02):** speculative categorical synthesis; sympy-internal
consistency only; **NO new theorem**; NO arXiv claim; NO push.
Companion files: `DME_functor.tex`, `DME_functor.py`.

---

## 1. Source category $\mathbf{Diam}_{\mathrm{FRW}}$

**Objects.** Admissible diamonds $D=(\eta_i,\eta_f,R_{\mathrm{conf}})$ with
$0<\eta_i<\eta_f<\infty$, $R_{\mathrm{conf}}>0$,
$R_{\mathrm{conf}}\le(\eta_f-\eta_i)/2$ (radiation-dominated FRW
$a=a_0\eta$; matter and Poincaré-patch dS analogous).

**Morphisms.** Inclusions $D'\hookrightarrow D$, i.e.\
$\eta_i\le\eta_i'$, $\eta_f'\le\eta_f$, $R_{\mathrm{conf}}'\le R_{\mathrm{conf}}$.

**Structure.** Thin category (poset). Reflexivity, antisymmetry,
transitivity verified by sympy on $\ge 2000$ random admissible chains
(`DME_functor.py` Block 1, all True).

---

## 2. Target category candidates

| Candidate | Morphisms | Verdict |
|---|---|---|
| $\mathbf{Cat}_1$ = W*-algebras + W*-iso | algebra isos | **rejected**: inclusions are not iso |
| $\mathbf{Cat}_2$ = W*-dyn syst + covariant W*-iso | covariant isos | **rejected**: $\sigma^D$ is not preserved by iso under inclusion |
| $\mathbf{Cat}_3 = \mathbf{W^*Cat}_{\mathrm{inj}}$ (BFV CMP 237 (2003)) | normal injective unital $*$-hom | **selected**: encodes Haag-Kastler isotony exactly |

The BFV 2003 framework is the natural target: locally covariant QFT *is*
a covariant functor from a category of spacetimes (with isometric
embeddings) to $\mathbf{W^*Cat}_{\mathrm{inj}}$, and quantum fields are
natural transformations between such functors.

---

## 3. Functoriality check

**Theorem (conditional, see `DME_functor.tex` Thm 1).** Under the
modular-compatibility hypothesis $(\star)$ — for each $D'\subset D$ a
faithful normal state-preserving conditional expectation
$E_{D',D}:\mathcal{N}(D)\to\mathcal{N}(D')$ exists (Takesaki 1972
sub-pair condition) —

$$\mathcal{N}\;:\;\mathbf{Diam}_{\mathrm{FRW}}\longrightarrow\mathbf{W^*Cat}_{\mathrm{inj}},\qquad D\mapsto\mathcal{A}(D)_{\mathrm{FRW}}\rtimes_{\sigma^D}\mathbb{R}$$

is a covariant functor.

**Status of $(\star)$.** Provable in the conformal-pullback regime of
`frw_note.tex` (Hislop-Longo Minkowski net + conformal unitary $U$ from
Prop 3.4 transports Buchholz 1974 / Longo 1979 conditional expectations
back to FRW). Open beyond that.

**$K(D)$ is NOT a functor** at the operator level: modular operators of
inclusions are not restrictions of the larger one (Takesaki 1972
counterexample). Only the outer-modular *class* $[\sigma^D]$ is
functorial up to inner perturbations, by Connes 1973 cocycle theorem
(Théorème 1.2.4). Sympy verification of the $u_{D',D}$ cocycle identity
on 3 profiles in `DME_functor.py` Block 3 (all True).

**$C(D;s)$** is well-defined per object (Block A def of
`krylov_diameter.tex` Def 2). Saturating Parker-Cao asymptotic
$C_k(s)=\sinh(\pi s)^2/\pi^2$ gives $(1/C_k)\,dC_k/ds\to 2\pi$
(`DME_functor.py` Block 4, True).

---

## 4. KDC as natural transformation: explicit obstruction

Define functors $\mathbf{Diam}_{\mathrm{FRW}}\to\mathbb{R}^*_+$
(positive reals, discrete category):
$F_C(D):=\lim_{t\to\infty}(1/C_k(D;t))\,dC_k(D;t)/dt$ and
$F_R^{-1}(D):=1/R_{\mathrm{proper}}(\eta_c(D))$.

**Pointwise:** $F_C(D)=F_R^{-1}(D)$ on each $D$ (KDC,
`krylov_diameter.tex` Thm 4 + Casini-Huerta-Myers chain rule;
sympy-checked, Block 4).

**Naturality square (FAILS in general):** for $D'\subset D$,

$$\begin{array}{ccc}
F_C(D') & \xrightarrow{\phi_{D'}} & F_R^{-1}(D')\\
\downarrow & & \downarrow\\
F_C(D) & \xrightarrow{\phi_D} & F_R^{-1}(D)
\end{array}$$

right vertical = multiplication by $R_{\mathrm{proper}}(D')/R_{\mathrm{proper}}(D)\le 1$, well-defined (Block 5, True).

left vertical = projection of Lanczos coefficients $\{b_n^{D'}\}$ via
the Connes-Takesaki conditional expectation
$E_{D',D}:\mathcal{N}(D)\to\mathcal{N}(D')$. **Open question**: this
requires $K_{\mathcal{N}(D)}$ to commute with $E_{D',D}$, which is the
modular-invariance hypothesis of Connes-Takesaki 1977 — NOT
established for the FRW crossed product beyond conformal pullback.

**Verdict.** KDC is a *pointwise* identity but **not** a categorical
natural transformation. The naturality square fails on a generic
inclusion.

---

## 5. Limits / colimits

- **Colimit** (growing $D$): $\mathcal{N}_{\mathrm{global}}=
\varinjlim_{D}\mathcal{N}(D)$ — well-defined under $(\star)$, type
II$_\infty$ if all $\mathcal{N}(D)$ are.
- **Limit** (shrinking $\eta_i\to 0^+$, BB): $\mathcal{N}_{\mathrm{BB}}=
\varprojlim_D\mathcal{N}(D)$ — categorical realisation of `frw_note.tex`
Open Question 4.4. The IR singularity of the conformal vacuum at
$\eta=0$ may obstruct existence of a cyclic separating vector for the
projective limit. **Open.**

---

## 6. Verdict

**Partial functor with non-natural transformation.**

| Layer | Status |
|---|---|
| Source poset $\mathbf{Diam}_{\mathrm{FRW}}$ | well-defined |
| $D\mapsto\mathcal{N}(D)$ functor to $\mathbf{W^*Cat}_{\mathrm{inj}}$ | **conditional** on $(\star)$ — provable in conformal-pullback regime |
| $D\mapsto K(D)$ as operator-valued field | **fails** (only $[\sigma^D]$ outer-class is functorial) |
| $D\mapsto C(D;s)$ pointwise saturation $2\pi$ | OK on Parker-Cao asymptotic |
| KDC as natural transformation $F_C\Rightarrow F_R^{-1}$ | **fails** on inclusions; Lanczos coefficients not preserved by $E_{D',D}$ |
| Colimit (growing $D$) | global FRW algebra, well-defined under $(\star)$ |
| Limit (shrinking to BB) | open (= `frw_note.tex` Q.4.4) |

**No new theorem.** The construction is honest categorical
re-packaging of `frw_note` Thm 3.5/3.6 + Cor 3.7, `krylov_diameter`
Thm 4, and `frw_note` Prop 4.2.

---

## 7. Recommendation for publication target — *if* gaps are filled

This as-is is a **research-direction marker, not publishable**. Two
specific theorems would be needed to upgrade:

1. **Hypothesis $(\star)$ as a theorem** beyond conformal pullback —
i.e., existence of a state-preserving conditional expectation
$E_{D',D}:\mathcal{N}(D)\to\mathcal{N}(D')$ for arbitrary admissible
inclusions in non-conformal cosmologies. Required tools: a Takesaki
sub-pair theorem for the FRW crossed product. Likely venue once
proved: **Comm. Math. Phys.** (continuing the BFV 2003 / FaulknerSperanza
2024 line) or **Ann. Henri Poincaré**.

2. **Lanczos-projection compatibility** under $E_{D',D}$ — i.e.,
$b_n^{D'}=b_n^D|_{\text{Krylov}(D')}$ in some controlled sense. Required
tool: a modular-invariance theorem for the conditional expectation.
Likely venue once proved: **JFA** (Krylov side) or **JPAA** /
**Theory and Applications of Categories** (categorical re-packaging
side) — as a *natural transformation* theorem.

3. **The Big Bang limit** (Open Question 4.4) as a categorical limit
in $\mathbf{W^*Cat}_{\mathrm{inj}}$ — the most genuinely novel
direction. Likely venue once proved: **Adv. Math.** or **JFA**, as a
genuinely new operator-algebraic construction.

In its current state, NO publication is warranted. The DME is a
roadmap marker, exactly as flagged in
`/tmp/unifying_equation_attempt.md`.

---

## 8. Honest caveat

This document does NOT prove $(\star)$ in general; it does NOT prove
KDC naturality; it does NOT classify the BB limit; it does NOT add new
theorems beyond `frw_note` and `krylov_diameter`. It only formalises
*what would have to be proved* to make the speculative DME of
`/tmp/unifying_equation_attempt.md` Candidate C into a categorical
theorem. All sympy checks are internal-consistency verifications on
admissible-parameter samples and saturating asymptotic profiles, not
new derivations.

**Sources** (web-validated 2026-05-02):

- Connes, *Une classification des facteurs de type III*, ASENS (4) **6**
(1973), 133–252 — `https://www.numdam.org/item/ASENS_1973_4_6_2_133_0/`
- Brunetti, Fredenhagen, Verch, *The generally covariant locality
principle*, CMP **237** (2003), 31–68 —
`https://link.springer.com/article/10.1007/s00220-003-0815-7`
- Doplicher, Haag, Roberts, *Local observables and particle statistics
I/II*, CMP **23** (1971) / **35** (1974) —
`https://link.springer.com/article/10.1007/BF01877742`
- Longo, *Index of subfactors and statistics of quantum fields*, CMP
**126** (1989), 217–247 / **130** (1990), 285–309 —
`https://link.springer.com/article/10.1007/BF02125124`
- Buchholz, Wichmann, *Causal independence and the energy-level density
of states in local QFT*, CMP **106** (1986), 321–344.
- `frw_note.tex` Thm 3.5, 3.6, Cor 3.7, Prop 4.2, Open Q 4.4
(`/root/crossed-cosmos/paper/frw_typeII_note/`).
- `krylov_diameter.tex` Def 2, Thm 4 (`/root/crossed-cosmos/paper/krylov_diameter/`).
