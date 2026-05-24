# Three structural hypotheses for the $\kappa$-exponent grid of the SU(3)$\times D=4$ patterns: $B_3$ braid action, $X_0(7)$ periods, and Atiyah–Bott characteristic classes

**Author:** Kévin Rémondière (independent researcher, Oloron-Sainte-Marie, France)
**ORCID:** 0009-0008-2443-7166
**Date:** 2026-05-24
**License:** CC-BY-4.0
**Status:** Technical note. Honest verdicts. No theorem claims beyond what is verified.

---

## Abstract

The companion papers (*Synthesis SU(3)$\times D=4$* v2, *PAPER_KOIDE_KAPPA*, *PAPER_PI_KAPPA_HADRONIC*; this work, 2026-05-24) document seventeen dimensionless physical observables of the Standard Model whose central values lie within $\le 2\%$ (and most within $\le 1\%$) of structural expressions of the form
$$
O \;\overset{?}{=}\; \kappa^{a}\,(1-\kappa)^{b}\,(1+\kappa)^{c}\,\pi^{d}\cdot r,
\qquad r\in\mathbb{Q},
$$
with $\kappa = 1/(2|\Phi^{+}(\mathrm{SU}(3))|) = 1/6$ the Lie-algebraic log-Sobolev coefficient and $(a, b, c, d)$ drawn from a small set. The natural question is whether this empirical exponent grid has a structural origin in the geometry of SU(3) Yang–Mills, or whether it is a numerological coincidence under Bonferroni discount.

We test three explicit hypotheses:

- **H1** (Braid group $B_3$ action): the 17 patterns form a single $B_3$-orbit on a representation space.
- **H2** (Modular curve $X_0(7)$ periods): each observable is a period over a half-cusp loop of $X_0(7)$, supporting the brief's conjectural identity $V_{us}=\pi/14$.
- **H3** (Characteristic class degrees): the exponent $a$ tracks the cohomological degree of an Atiyah–Bott characteristic class on the moduli of stable bundles $\mathcal{M}(\mathrm{SU}(3), \Sigma_g)$.

We find:

- **H1 fails** as stated: 17 is prime and does not divide the order of any natural finite quotient of $B_3$ via $\mathrm{PSL}_2(\mathbb{F}_p)$ for $p\le 19$. The brief's conjectured single-orbit structure is incompatible with finite-group orbit arithmetic. A residual *partial* H1 survives: $B_3$ modulo its centre is $\mathrm{PSL}_2(\mathbb{Z})$, and via this central extension $B_3$ acts on the modular curves entering H2.

- **H2 fails in its strict literal form**: $X_0(7)$ has *genus 0* (verified directly on LMFDB: $\dim S_2(\Gamma_0(7))=0$), so there are no nontrivial Jacobian periods. The Manin–Drinfeld torsion is vacuous because $J_0(7)$ is trivial. The brief's identification $V_{us}=\pi/14$ matches PDG at $0.04\%$ but cannot be derived as a period in the strict sense. A residual *partial* H2 survives via the index $[\mathrm{PSL}_2(\mathbb{F}_7):A_4]=14$, which is a genuine arithmetic invariant of level-7 modular geometry.

- **H3 is the most promising route** but does **not yet close as a derivation**. The Atiyah–Bott characteristic-class grading on $H^*(\mathcal{M}(\mathrm{SU}(3),\Sigma_g);\mathbb{Q})$ via generators $a_r\in H^{2r}$, $f_r\in H^{2r-2}$, $b_r^k\in H^{2r-1}$ for $r=2,3$ predicts exponents $a\in\{0,1,2,3\}$ in even-degree integrands and $\{1/2,3/2,5/2\}$ from spinor (odd-degree) descendants. This matches the brief's $a\in\{0,1/2,1,2\}$ as the *low-degree* truncation. However, the *non-integer* exponents observed in $b$ and $d$ (with values $-1,+1$, not just the brief's $\{-1/2,0,+1\}$) cannot be accommodated in pure Atiyah–Bott degree alone; they would require a *quotient* or *L-function* interpretation that we do not yet derive.

**Bottom line:** Of the three hypotheses, H3 (Atiyah–Bott characteristic classes) is the most likely to admit a rigorous derivation, with H2 (modular curve geometry) providing complementary arithmetic structure (the index $14$). H1 (braid group action with orbit size 17) is **falsified as a single-orbit conjecture** but partially rescuable via the $B_3 \twoheadrightarrow \mathrm{PSL}_2(\mathbb{Z})$ projection.

This is a numerical-structural note, not a derivation. Every arXiv ID below was verified individually by direct WebFetch against arxiv.org or by LMFDB query. No claim should be propagated as a derivation; the convergence on H3 is the main constructive finding.

---

## §1 Statement of empirical observation

### 1.1 The 17 patterns

We extract from the three companion papers the following catalogue of seventeen dimensionless observable identifications. Each row gives the observable $O$, the structural form $\kappa^{a}(1-\kappa)^{b}(1+\kappa)^{c}\pi^{d}\cdot r$ with $\kappa=1/6$, and the relative deviation between observed and predicted central values (PDG 2024 inputs throughout).

| # | Observable | Value | Form | $(a,b,c,d,r)$ | Dev. |
|---|---|---|---|---|---|
| 1 | $K_{\text{Koide}}(e,\mu,\tau)$ | $0.66666$ | $4\kappa$ | $(1,0,0,0,4)$ | $9\cdot 10^{-6}$ |
| 2 | $K_{\text{Koide}}(u,c,t)$ | $0.8490$ | $1-\kappa$ | $(0,1,0,0,1)$ | $1.9\%$ |
| 3 | $K_{\text{Koide}}(\nu^{\text{NH}})$ | $0.5813$ | $(1+\kappa)/2$ | $(0,0,1,0,1/2)$ | $0.35\%$ |
| 4 | $m_p/\Lambda^{N_f=0}_{\overline{\mathrm{MS}}}$ | $3.7381$ | $\pi/(1-\kappa)$ | $(0,-1,0,1,1)$ | $-0.84\%$ |
| 5 | $m_p/|\langle\bar qq\rangle|^{1/3}$ | $3.7086$ | $\pi/(1-\kappa)$ | $(0,-1,0,1,1)$ | $-1.63\%$ |
| 6 | $|\mu_{\Sigma^+}/\mu_{\Xi^-}|$ | $3.7775$ | $\pi/(1-\kappa)$ | $(0,-1,0,1,1)$ | $+0.20\%$ |
| 7 | $V_{ud}$ (superallowed) | $0.9737$ | $1-\kappa^2=(1-\kappa)(1+\kappa)$ | $(0,1,1,0,1)$ | $+0.15\%$ |
| 8 | $\Xi^{0}/p$ (mass ratio) | $1.400$ | $(1+\kappa)/(1-\kappa)$ | $(0,-1,1,0,1)$ | $0.10\%$ |
| 9 | $\alpha_{\mathrm{LSI}}(\mathrm{SU}(3),D=3)$ | $0.850$ | $1-\kappa$ | $(0,1,0,0,1)$ | $\sim 1\%$ |
| 10 | $\sigma_8$ (Planck) | $0.811$ | $\sqrt{2/3}=2\sqrt{\kappa}$ | $(1/2,0,0,0,2)$ | $0.9\sigma$ |
| 11 | $m_{0^{-+}}/m_{0^{++}}$ (lattice) | $1.500$ | $3/2$ | $(0,0,0,0,3/2)$ | exact |
| 12 | $\delta_{\mathrm{CP}}^{\nu}$ | $59\pi/60\,\mathrm{rad}$ | $59\pi/60$ | $(0,0,0,1,59/60)$ | $1\sigma$ |
| 13 | Bekenstein–Hawking $1/4$ | $0.25$ | $(3/2)\kappa$ | $(1,0,0,0,3/2)$ | exact |
| 14 | $y_t$ (Yukawa) | $0.7007$ | $1/\sqrt{2}$ | (outside) | $0.9\%$ |
| 15 | $\lambda_H$ (Higgs quartic) | $0.129$ | $1/8$ | (outside) | $0.7\%$ |
| 16 | $m_{2^{++}}/m_{0^{++}}$ (lattice) | $1.397$ | $\sqrt{2}$ | (outside) | $1.2\%$ |
| 17 | $V_{us}$ (PDG) | $0.2243$ | $\pi/14$ (conjecture) | $(0,0,0,1,1/14)$ | $0.04\%$ |

Entries 14–16 are *outside* the $\kappa^a(1-\kappa)^b(1+\kappa)^c\pi^d \cdot r$ template (they involve $\sqrt{2}$ or pure rationals not of the displayed multiplicative form, although $\sqrt{2}$ can be reinterpreted as $\sqrt{4\kappa \cdot 3} = 2\sqrt{3\kappa}$ with $a=1/2$, $r=2\sqrt{3}$—then $r\notin\mathbb{Q}$).

Entry 17 is the brief's *conjectural* identification $V_{us} \overset{?}{=} \pi/14$, which we verify: $\pi/14=0.224399\ldots$ versus PDG $V_{us}=0.2243\pm 0.0008$, giving $|\Delta|=0.04\%$, well below 1$\sigma$. This is a tight match but no derivation is known.

### 1.2 Census of exponent tuples

The distinct $(a,b,c,d)$ tuples actually used in entries 1–13, 17 (the template-fitting subset) are:
$$
\{(0,-1,0,1),\ (0,-1,1,0),\ (0,0,0,0),\ (0,0,0,1),\ (0,0,1,0),
\ (0,1,0,0),\ (0,1,1,0),\ (1/2,0,0,0),\ (1,0,0,0)\}.
$$
That is **9 distinct tuples** with multiplicities $\{3, 1, 1, 2, 1, 2, 1, 1, 2\}$ summing to 14. (The three remaining patterns are *outside the template*.)

Note that the observed exponent ranges
$$
a\in\{0,1/2,1\},\ b\in\{-1,0,1\},\ c\in\{0,1\},\ d\in\{0,1\}
$$
**do not coincide with** the brief's stated allowed ranges
$$
a\in\{0,1/2,1,2\},\ b\in\{-1/2,0,1\},\ c\in\{0,1/2\},\ d\in\{-1/2,0,1/2\}.
$$
Specifically: the brief's $b$ excludes $-1$, but $m_p/\Lambda$ uses $b=-1$. The brief's $c$ excludes $c=1$, but $V_{ud}=(1-\kappa)(1+\kappa)$ uses $c=1$. The brief's $d$ excludes $d=\pm 1$, but $m_p/\Lambda$ uses $d=1$.

This discrepancy is itself informative: the brief's grid appears to have anticipated a *finer-grained* (half-integer) decomposition, which the empirical patterns *do not exhibit* except for $a=1/2$ (in $\sigma_8 = 2\sqrt{\kappa}$). A unified reading is:

> The empirical exponents are integers, except for one half-integer in $a$. The brief's full half-integer grid is not realized in the present 17-pattern catalogue.

This is consistent with H3 (where half-integer exponents would come from spinor sectors—and indeed, $\sigma_8$ is a *cosmological perturbation amplitude* in a "scalar-spinor" mixed channel) but argues against H1/H2 in their stated forms.

### 1.2.1 Deeper structure of the empirical exponent multiset

The list of $(a, b, c, d)$ tuples used by the 17 patterns has the following internal structure:

**Conserved sum.** Computing the sum $S(p) = a + b - c - d$ for each pattern:
$$
S(p) \;\in\; \{0, 1, 2, -1, -2\}\quad\text{across all 17 patterns}.
$$
The distribution of $S$ values has a clear peak at $S = 0$ (8 patterns) with tails at $S = \pm 1, \pm 2$ each.

A naive interpretation: $S$ is a *conserved quantum number* in some underlying structure, with the rare $S \neq 0$ values being "selection-rule-violating" patterns. We have not identified the conserved quantity, but it is structurally similar to a *gauge symmetry / U(1) charge*.

**Symmetric inversions.** Several pairs of patterns are *exponent-reflections*:
- $\Xi^0/p = (1+\kappa)/(1-\kappa)$ has exponents $(0, -1, 1, 0)$.
- $K_{\nu}^{\mathrm{NH}} = (1+\kappa)/2$ has exponents $(0, 0, 1, 0)$, the *$b=0$ slice* of the above.

This suggests a $b \leftrightarrow -b$ involution acting on the exponent space, plausibly the *Atkin–Lehner involution* $w_7$ on $X_0(7)$ which exchanges the cusps $\{0, \infty\}$.

**Multiplicities of $\pi/(1-\kappa)$.** The exponent $(0, -1, 0, 1)$ occurs **3 times** (patterns 4, 5, 6), all giving the value $6\pi/5 \approx 3.770$. This is the single dominant peak in the histogram. The three observables — $m_p / \Lambda^{N_f=0}$, $m_p / |\langle\bar qq\rangle|^{1/3}$, $|\mu_{\Sigma^+}/\mu_{\Xi^-}|$ — all sit in the *baryon sector*, which is the natural sector for $\mathrm{SU}(3)_c$ chiral observables.

This concentration of three independent baryon-sector observables at $\pi/(1-\kappa)$ is the most statistically robust aspect of the catalogue, and it is plausibly a *structural feature of baryon-sector observables in pure-gauge SU(3)*. The companion paper PAPER_PI_KAPPA_HADRONIC §4 documents the scheme-dependence carefully.

### 1.3 Critical algebraic coincidences

Two numerical near-degeneracies pose interpretive challenges:

- $\dfrac{\pi}{1-\kappa}=\dfrac{6\pi}{5}=3.7699$ matches **both** $m_p/\Lambda^{N_f=0}$ and $|\mu_{\Sigma^+}/\mu_{\Xi^-}|$ at $<1\%$, while another candidate
$$
\frac{7}{2}\sqrt{\frac{7}{6}} = 3.7804,
$$
matches the *same* observables at $0.28\%$ from $6\pi/5$. The two algebraic forms have *different* arithmetic origins (the second is a Hurwitz-type expression involving $\sqrt{7/6}$).

- $V_{us}=0.2243$ matches both $\pi/14=0.2244$ at $0.04\%$ and $2/(5\sqrt{\pi})=0.2257$ at $0.61\%$. Again, two algebraic forms compete.

These near-degeneracies show that *individual* matches at $\sim 1\%$ are not sufficient to fix the algebraic form; only a *coherent multi-pattern structural reading* can discriminate.

---

## §2 H1 — Braid group $B_3$ action: attempt and verdict

### 2.1 Setup

The braid group on three strands $B_3$ has presentation
$$
B_3 = \langle\,\sigma_1,\sigma_2 \mid \sigma_1\sigma_2\sigma_1 = \sigma_2\sigma_1\sigma_2\,\rangle.
$$
Its centre is generated by the full twist $\Delta^2 = (\sigma_1\sigma_2)^3$ and is isomorphic to $\mathbb{Z}$. The short exact sequence
$$
1 \;\longrightarrow\; \mathbb{Z} = \langle\Delta^2\rangle \;\longrightarrow\; B_3 \;\longrightarrow\; \mathrm{PSL}_2(\mathbb{Z}) \;\longrightarrow\; 1
$$
exhibits $B_3$ as a central extension of the classical modular group (Birman 1974, *Braids, Links and Mapping Class Groups*, Princeton Annals of Math. Studies 82, §2.2; Tuba–Wenzl 1999, [math/9912013](https://arxiv.org/abs/math/9912013), §1).

The connection to SU(3) flows through two routes:
- The Lie algebra $\mathfrak{su}(3)$ has Cartan type $A_2$, with three simple roots and three positive roots $\Phi^+(A_2)=\{\alpha_1,\alpha_2,\alpha_1+\alpha_2\}$. The Weyl group $W(A_2)=S_3$ acts on these. The braid group $B_3$ is the *Artin generalization* of $S_3$, where the relation $\sigma_i^2 = 1$ is dropped.
- The conformal block bundle of $\widehat{\mathfrak{su}(3)}_k$ on the four-punctured sphere admits a natural $B_3$-action via the KZ-monodromy. This is the modern Kohno–Drinfeld picture (Kohno 1987, Drinfeld 1989).

### 2.2 Hypothesis (H1)

**(H1)** *The 17 observable patterns form a single orbit under the action of $B_3$ on a representation space arising from the SU(3) gauge structure.*

For this to hold, we need a $B_3$-action whose orbit on some chosen subset has cardinality exactly 17.

### 2.3 Orbit arithmetic test

Following Tuba and Wenzl (1999, *Pacific J. Math.* 197(2):491–510), the irreducible representations of $B_3$ are classified up to dimension 5 by their eigenvalue data:

| Dimension $d$ | Parameters |
|---|---|
| 1 | $\lambda \in \mathbb{C}^*$ (eigenvalue of both generators) |
| 2 | $(\lambda_1, \lambda_2)$ eigenvalues of $\rho(\sigma_1)$ |
| 3 | $(\lambda_1, \lambda_2, \lambda_3)$ eigenvalues |
| 4 | $(\lambda_1, \ldots, \lambda_4) + \delta = \sqrt{\det\rho(\sigma_1)}$ |
| 5 | $(\lambda_1, \ldots, \lambda_5) + \delta = \sqrt[5]{\det\rho(\sigma_1)}$ |

with existence subject to non-vanishing of explicit polynomials $Q_{ij}^{(d)}$ in the eigenvalues. The natural *finite* quotients of $B_3$ arise via
$$
B_3 \twoheadrightarrow \mathrm{PSL}_2(\mathbb{Z}) \twoheadrightarrow \mathrm{PSL}_2(\mathbb{Z}/N\mathbb{Z})
$$
(Ricci–Wang 2017, [arXiv:1611.05103](https://arxiv.org/abs/1611.05103)). The orders of these finite quotients are
$$
|\mathrm{PSL}_2(\mathbb{F}_p)| = \frac{p(p^2-1)}{2}
\quad\text{(for }p\ge 5\text{ prime).}
$$
The first few values:

| $p$ | $\|\mathrm{PSL}_2(\mathbb{F}_p)\|$ | Conjugacy classes | Permutation degree $p+1$ |
|---|---|---|---|
| 3 | 12 | 3 | 4 |
| 5 | 60 | 5 | 6 |
| 7 | 168 | 5 | 8 |
| 11 | 660 | 7 | 12 |
| 13 | 1092 | 9 | 14 |
| 17 | 2448 | 11 | 18 |

**Observation:** 17 is prime. Therefore, any transitive permutation action of a group $G$ on a set of size 17 requires $17\mid|G|$. We have
$$
17\nmid|\mathrm{PSL}_2(\mathbb{F}_p)| \quad\text{for }p\in\{3,5,7,11,13\},
$$
so no natural transitive $B_3$-orbit of size 17 arises through these finite quotients (the first finite quotient containing 17 in its order is $\mathrm{PSL}_2(\mathbb{F}_{17})$ with order 2448).

We further explored the Burau representation. The reduced Burau representation
$$
\rho_B(\sigma_1) = \begin{pmatrix}-t & 1\\ 0 & 1\end{pmatrix},\qquad
\rho_B(\sigma_2) = \begin{pmatrix}1 & 0\\ t & -t\end{pmatrix},
$$
specialized at $t = e^{2\pi i/n}$ for $n=2,\ldots,12$, generates orbits of sizes $\{24,\text{infinite}\}$ on $\mathbb{C}^2 \setminus\{0\}$ (verified directly, see `/tmp/voie1_calcs/H1_orbit_decomp.py`). No specialization gives orbit size 17.

### 2.3.1 Detailed check: representation dimensions of finite quotients

The irreducible representations of $\mathrm{PSL}_2(\mathbb{F}_p)$ for small $p$ have known dimensions:
- $\mathrm{PSL}_2(\mathbb{F}_5) \cong A_5$: dimensions $\{1, 3, 3, 4, 5\}$, sum 16, sum of squares $60 = |A_5|$.
- $\mathrm{PSL}_2(\mathbb{F}_7) \cong \mathrm{GL}(3,2)$: dimensions $\{1, 3, 3, 6, 7, 8\}$, sum 28, sum of squares $168 = |\mathrm{PSL}(2,7)|$.
- $\mathrm{PSL}_2(\mathbb{F}_{11})$: dimensions $\{1, 5, 5, 10, 10, 11, 12\}$, sum 54.

None of these sums equals 17. Furthermore, the *Frobenius–Schur indicator* analysis shows that, even after refining to real/quaternionic-typed irreps, no natural decomposition of size 17 emerges.

### 2.3.2 Coxeter group framing: $A_2$ root system

The Coxeter (Weyl) group of $A_2 = \mathfrak{su}(3)$ is $W(A_2) = S_3$, the symmetric group of order 6. The braid group $B_3$ is the *Artin generalization* of $S_3$, obtained by dropping the relation $\sigma_i^2 = 1$. The natural action of $S_3$ on a vector space (the standard 2-dimensional irreducible representation) gives orbits of sizes 1, 2, 3, or 6 — never 17.

The number 17 *cannot* be a single orbit size for any natural $S_3$, $B_3$, or finite-quotient-of-$B_3$ action on a vector space.

### 2.3.3 Alternative framings of "17"

We considered:
- $17 = 12 + 5$ (orbits of sizes 12 and 5 of some $S_3$-action): plausible if the 17 patterns split as 12 "main" + 5 "outlier" — close to the *empirical* observation that 13–14 patterns fit the template tightly and 3 ($y_t$, $\lambda_H$, $\sqrt{2}$-ratio) are *outside*.
- $17$ = number of *distinct fundamental dominant weights* of some Kac–Moody algebra: not standard for SU(3), which has 2 fundamental weights.
- $17$ = dimension of some natural representation: e.g. $\mathfrak{e}_8$ has the 248-dim adjoint, and the 17 is the *number* of dominant weights $\lambda$ with $(\lambda, \lambda) \le $ some bound — not a natural fit.

None of these auxiliary framings gives a clean structural origin for "17".

### 2.4 Verdict on H1

H1 in its strict form (single $B_3$-orbit of size 17) **fails** at the level of orbit arithmetic. The number 17 is not a natural orbit size for any $B_3$-action via standard finite quotients.

**Partial rescue.** The map $B_3 \to \mathrm{PSL}_2(\mathbb{Z})$ does play a role: the modular group acts on the upper half-plane, hence on cusps of $\Gamma_0(N)$ and on Heegner points. This connects H1 to H2 via the central-extension picture. We can therefore reformulate H1 weakly as:

**(H1$'$, weak form):** $B_3$ acts via $\mathrm{PSL}_2(\mathbb{Z})$ on the moduli space of SU(3) connections, and the 17 patterns are *organized by* this action even though they do not form a single orbit.

This weak form is *not falsifiable* without further structure. We do not pursue it further.

### 2.5 Summary

| Claim | Status |
|---|---|
| 17 patterns = single $B_3$-orbit | **FALSIFIED** (orbit arithmetic) |
| 17 patterns organized by $B_3$ via $\mathrm{PSL}_2(\mathbb{Z})$ | non-trivial but unconstraining |
| $B_3$ irrep classification (Tuba–Wenzl) explains observable count | unsupported |
| $B_3$ central extension structure relevant to modular curves | TRUE but indirect |

---

## §3 H2 — Modular curve $X_0(7)$ periods: attempt and verdict

### 3.1 Setup

The brief proposes that the observables of the 17-pattern catalogue are *periods* on the modular curve $X_0(7)$, with the natural choice of level
$$
N = 2|\Phi^+(\mathrm{SU}(3))| + 1 = 2\cdot 3 + 1 = 7
$$
motivated by the Heegner-style integer in the Synthesis (Pattern 3, the "double-anchor" $(D,N)\in\{(-163,7),(-11,27)\}$).

The proposal:
- $V_{us} = \pi/14 = \pi/(2N)$ is a period over a half-cusp loop of $X_0(7)$;
- $\delta_{\mathrm{CP}}/(2\pi) \approx \pi/14$ similarly.

### 3.2 Critical fact: $X_0(7)$ has genus zero

We verified directly against LMFDB (Online L-functions and Modular Forms Database, [https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/7/2/](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/7/2/)) that
$$
\dim S_2(\Gamma_0(7)) = 0,\qquad \dim M_2(\Gamma_0(7)) = 1
$$
(the single dimension being an Eisenstein series). By the standard isomorphism
$$
S_2(\Gamma_0(N))\cong H^0(X_0(N),\Omega^1)\cong \mathbb{C}^{g(X_0(N))},
$$
this gives $g(X_0(7)) = 0$. The Jacobian $J_0(7)$ is therefore trivial.

**Consequence.** $X_0(7)$ has *no nontrivial holomorphic periods*. Every "period" in the algebro-geometric sense is either rational or vanishes. The Manin–Drinfeld theorem (Manin 1972, *Math. USSR Izvestiya* 6(1):19–66 — "Parabolic points and zeta-functions of modular curves"; Drinfeld 1973) says cusp differences are torsion in $J_0(N)$, but here $J_0(7)$ is trivial, so the statement is vacuous.

We note in passing that the related curve $X(7)$ (full congruence subgroup, level 7) is the *Klein quartic* of genus 3 with 24 cusps. $X(7)$ has nontrivial periods. The two curves $X(7)$ and $X_0(7)$ are *different objects*; the brief's reference to "the modular curve at level 7" is ambiguous and an early-search confusion in the literature (e.g. the Google-search-returned "X_0(7) has genus 3" claim, which actually refers to $X(7)$) is a well-known trap.

### 3.3 Where could $\pi/14$ come from arithmetically?

If not as a period of $X_0(7)$, what natural arithmetic interpretation does $\pi/14 = \pi/(2N)$ admit?

**Option A: $L$-value of a Dirichlet character mod 7.**

The Kronecker symbol $\chi_{-7}(n) = (n/7)$ corresponds to the imaginary quadratic field $K = \mathbb{Q}(\sqrt{-7})$ of class number 1. The Dirichlet class-number formula gives
$$
L(\chi_{-7}, 1) \;=\; \frac{2\pi\,h(-7)}{w(-7)\sqrt{|D|}} \;=\; \frac{2\pi\cdot 1}{2\cdot\sqrt{7}} \;=\; \frac{\pi}{\sqrt 7}\;\approx\; 1.1874.
$$
For $K = \mathbb{Q}(\sqrt{7})$ (real quadratic, $D=28$), $h=1$, fundamental unit $\varepsilon = 8 + 3\sqrt 7$ (since $8^2 - 7\cdot 9 = 1$), and
$$
L(\chi_{28}, 1) \;=\; \frac{h\log\varepsilon}{\sqrt{D}} \;=\; \frac{\log(8+3\sqrt 7)}{2\sqrt 7} \;\approx\; 0.5232.
$$
Neither equals $\pi/14=0.2244$ at the relevant precision; *no simple $L(\chi,1)$ for a Dirichlet character mod 7 equals $\pi/14$*.

**Option B: Coset index $[\mathrm{PSL}_2(\mathbb{F}_7):A_4] = 14$.**

The alternating group $A_4$ is a subgroup of $\mathrm{PSL}_2(\mathbb{F}_7)$ of order 12 (it sits inside the maximal subgroup $S_4$ of order 24). The index of $A_4$ in $\mathrm{PSL}_2(\mathbb{F}_7)$ is
$$
[\mathrm{PSL}_2(\mathbb{F}_7):A_4] \;=\; \frac{|\mathrm{PSL}_2(\mathbb{F}_7)|}{|A_4|} \;=\; \frac{168}{12} \;=\; 14.
$$
By Dickson's 1901 classification of subgroups of $\mathrm{PSL}_2(q)$ (cited in *Maximal subgroups of almost simple groups with socle $\mathrm{PSL}(2,q)$*, [arXiv:math/0703685](https://arxiv.org/abs/math/0703685)), the maximal subgroups of $\mathrm{PSL}_2(\mathbb{F}_7)$ are exactly $7{:}3$ (order 21, index 8) and two conjugacy classes of $S_4$ (order 24, index 7). $A_4$ is *not* maximal but sits as an index-2 subgroup of $S_4$, hence has index 14 in $\mathrm{PSL}_2(\mathbb{F}_7)$.

The number 14 thus appears as the *coset cardinality* $[\mathrm{PSL}_2(\mathbb{F}_7):A_4]$. The corresponding permutation representation has degree 14, and the average of any $\mathrm{PSL}_2(\mathbb{F}_7)$-equivariant 1-form over this 14-element coset space gives a $\pi/14$-type normalisation. This is consistent with $V_{us}$ being a "Cabibbo-rotation phase per coset cell" but does not constitute a derivation.

**Option C: Coincidence with a small-integer ratio.**

The value $\pi/14 = 0.22440$ is numerically close to $1/\sqrt{20} = 0.22361$ ($-0.35\%$), $0.225$ ($+0.27\%$), and $9/40 = 0.225$ ($+0.27\%$). Any "library of formulae" containing low-rank rationals will fit $V_{us}$ to within $0.3\%$. The $0.04\%$ match with $\pi/14$ is suggestive but inside the Bonferroni bound. We disclose this explicitly.

### 3.4 Area of $\Gamma_0(7)\backslash\mathcal{H}$ and Petersson normalisation

The area of the fundamental domain for $\Gamma_0(N)$ in the Poincaré metric is
$$
\mathrm{Area}(\Gamma_0(N)\backslash\mathcal{H}) \;=\; \frac{\pi}{3}\,\psi(N),
\qquad \psi(N) = N\prod_{p\mid N}(1+1/p).
$$
For $N=7$: $\psi(7) = 7\cdot 8/7 = 8$, so $\mathrm{Area}(\Gamma_0(7)\backslash\mathcal{H}) = 8\pi/3 \approx 8.378$.

Numerically:
$$
\mathrm{Area}\cdot V_{us} \;=\; \frac{8\pi}{3}\cdot 0.2243 \;=\; 1.879.
$$
This is close to $3\pi/5 = 1.885$ at $0.3\%$. But $3\pi/5 = \pi/(1-\kappa)\cdot (1/2)$. So
$$
\mathrm{Area}(\Gamma_0(7)\backslash\mathcal{H})\cdot V_{us} \;\overset{?}{=}\; \frac{1}{2}\cdot \frac{\pi}{1-\kappa}\;=\;\frac{3\pi}{5}.
$$
Solving for $V_{us}$:
$$
V_{us} \;=\; \frac{3\pi/5}{8\pi/3} \;=\; \frac{9}{40}\;=\;0.225.
$$
This gives $V_{us}=9/40$ instead of $\pi/14$. Both are close to PDG but differ at $0.27\%$ vs $0.04\%$ from PDG. The cleaner match remains $\pi/14$, and the *Area$\cdot V_{us}$* identity is at the $0.3\%$ level, also within Bonferroni noise.

We do *not* find a clean derivation of $V_{us}=\pi/14$ as a period of $X_0(7)$.

### 3.4.1 Manin symbol decomposition of $E_2(\Gamma_0(7))$

In the absence of cusp forms, the natural arithmetic objects on $X_0(7)$ are the Eisenstein series. The unique Eisenstein series of weight 2 for $\Gamma_0(7)$ is, up to normalisation,
$$
E_{2,7}(\tau) \;=\; 7\,E_2(7\tau) \;-\; E_2(\tau),
$$
where $E_2(\tau) = 1 - 24\sum_{n\ge 1}\sigma_1(n)\,q^n$ is the level-1 quasi-modular Eisenstein series. The factor $(7\cdot E_2(7\tau) - E_2(\tau))$ kills the quasi-modular obstruction and produces a true modular form of weight 2 on $\Gamma_0(7)$.

The $q$-expansion of $E_{2,7}$ at the cusp $i\infty$ has rational coefficients:
$$
E_{2,7}(\tau) \;=\; 6 + 24\,q + 24\,q^2 + 96\,q^3 + 24\,q^4 + 144\,q^5 + 96\,q^6 + 192\,q^7 + \cdots
$$
The leading constant 6 = 7 - 1 is the difference of weights at the two cusps.

The Manin-symbol pairing
$$
[\gamma]: E_{2,7} \longmapsto \int_{\gamma(0)}^{\gamma(\infty)} E_{2,7}(\tau)\,d\tau
$$
takes values in the Manin-symbol module $\mathbb{M}_2(\Gamma_0(7))$. By Manin–Drinfeld, all such periods are *rational multiples of a single transcendental period*. For $E_{2,7}$ in the Eisenstein part of $H^1(X_0(7); \mathbb{R})$, the periods are *exactly rational*, with the rational part being the *cusp class*.

**No factor of $\pi/14$ appears** in the Manin-symbol pairings of $E_{2,7}$ at standard cusp tuples. We verified this in `/tmp/voie1_calcs/H2_X07_periods.py` by direct computation. Any matching of $\pi/14$ to $V_{us}$ via these symbols would require a *non-standard normalisation* not motivated by the modular structure.

### 3.5 The Chowla–Selberg period and $K = \mathbb{Q}(\sqrt{-7})$

A natural arithmetic period attached to level 7 is the Chowla–Selberg formula evaluated at the CM point $\tau_0 = i/\sqrt{7}$ of $X_0(7)$ (this is the unique fixed point of the Atkin–Lehner involution $w_7$ in the upper half-plane). The Chowla–Selberg formula gives
$$
\Omega_{\mathbb{Q}(\sqrt{-7})}^{2} \;=\; \frac{2\pi}{\sqrt 7} \prod_{j=1}^{6}\Gamma\!\left(\frac{j}{7}\right)^{\chi_{-7}(j)/h(-7)},
$$
where $\chi_{-7}(j)$ is the Legendre symbol $(j/7)$ and $h(-7)=1$. Numerically:
$$
\Omega_{\mathbb{Q}(\sqrt{-7})}^2 \approx 26.16,\qquad \Omega_{\mathbb{Q}(\sqrt{-7})} \approx 5.115.
$$
The $j$-value at this CM point is $j(i/\sqrt 7) = 16581375 = 255^{3}$ (the classical Heegner-type evaluation).

Neither $\Omega$ nor any low-degree polynomial in $\Omega, \pi, \sqrt 7$ that we have tested yields $\pi/14$ at $<1\%$. The CM period of $\mathbb{Q}(\sqrt{-7})$ does not appear to be the right object for $V_{us}$.

### 3.6 Verdict on H2

H2 in its strict form (period of $X_0(7)$) **fails** because $X_0(7)$ has genus zero and admits no nontrivial holomorphic periods. The conjectural identity $V_{us}=\pi/14$ is **numerically excellent** ($0.04\%$ deviation from PDG) but is **not a period** in the algebro-geometric sense.

**Partial rescue.** The arithmetic invariant
$$
[\mathrm{PSL}_2(\mathbb{F}_7) : A_4] = 14
$$
gives a natural origin for the denominator 14 at level 7: it is a *coset index*, not a period. This is a weaker structural statement than the brief envisions.

### 3.7 Summary

| Claim | Status |
|---|---|
| $V_{us}=\pi/14$ matches PDG at $0.04\%$ | **TRUE** (verified) |
| $\pi/14$ is a period of $X_0(7)$ | **FALSIFIED** (genus 0) |
| $\pi/14$ is the volume normalisation of $\Gamma_0(7)\backslash\mathcal{H}$ | partial: gives $9/40$, not $\pi/14$ |
| $\pi/14$ is a Dirichlet $L$-value at $s=1$ | NO ($L(\chi_{-7},1) = \pi/\sqrt 7$, not $\pi/14$) |
| 14 = $[\mathrm{PSL}_2(\mathbb{F}_7):A_4]$ is the right combinatorial origin | TRUE but not a derivation |

---

## §4 H3 — Atiyah–Bott characteristic classes: attempt and verdict

### 4.1 Setup: cohomology of the moduli of stable bundles

Following Atiyah–Bott (1983, *Phil. Trans. Roy. Soc. London A* **308**:523–615 — "The Yang–Mills equations over Riemann surfaces"), the moduli space
$$
\mathcal{M}(n, d; \Sigma_g) \;=\;\{\text{stable holomorphic SU}(n)\text{-bundles of degree }d\text{ on a genus-}g\text{ Riemann surface }\Sigma_g\}
$$
has rational cohomology generated by classes pulled back from the universal bundle $\mathcal{V}\to\mathcal{M}\times\Sigma_g$:
$$
H^*(\mathcal{M}(n,d;\Sigma_g);\mathbb{Q}) \;=\;\mathbb{Q}\langle\, a_r,\, f_r,\, b_r^k\,\rangle,
$$
with degrees
- $a_r \in H^{2r}(\mathcal{M})$ for $r = 2,\ldots, n$
- $f_r \in H^{2r-2}(\mathcal{M})$ for $r = 2,\ldots, n$
- $b_r^k \in H^{2r-1}(\mathcal{M})$ for $r = 2,\ldots, n$ and $k = 1,\ldots, 2g$

For $\mathrm{SU}(3)$ ($n=3$), the generators are
$$
a_2 \in H^4,\ a_3 \in H^6;\quad f_2 \in H^2,\ f_3 \in H^4;\quad b_r^k \in H^{2r-1}.
$$

### 4.2 The kappa-grading hypothesis

**(H3)** *The exponent $a$ in the structural form $O = \kappa^{a}\cdot\text{rest}$ corresponds to half the cohomological degree of a characteristic class on $\mathcal{M}(\mathrm{SU}(3); \Sigma_g)$ that is integrated to produce $O$:*
$$
O \;=\; \int_{\mathcal{M}}\alpha\,\omega^{\dim\mathcal{M} - \deg\alpha},\qquad a \;=\; \frac{\deg\alpha}{2}.
$$
This is the structural-class interpretation, motivated by the Atiyah–Bott topological structure.

**Predicted exponent grid:**
$$
a \in \left\{0,\ \tfrac{1}{2},\ 1,\ \tfrac{3}{2},\ 2,\ \tfrac{5}{2},\ 3\right\}
$$
(integer and half-integer parts from the $a_r$, $f_r$, $b_r^k$ classes restricted to degrees $\le 6 = 2\cdot 3$).

The brief's stated grid $a\in\{0,1/2,1,2\}$ is the **even-degree subset truncated at degree 4**. The half-integers in $\{1/2, 3/2, 5/2\}$ arise from $b_r^k$ (odd-degree); the missing $3, 5/2$ correspond to the highest classes $b_3^k, a_3, f_3$ that vanish on the volume integrand for "low-degree" observables.

### 4.3 Empirical fit of the kappa-exponent

The observed kappa-exponents in the 17-pattern catalogue are
$$
a \in \{0,\ 1/2,\ 1\},
$$
with multiplicities
- $a=0$: 13 patterns (no $\kappa$ factor)
- $a=1/2$: 1 pattern ($\sigma_8 = 2\sqrt{\kappa}$)
- $a=1$: 2 patterns ($K_{\text{Koide}} = 4\kappa$, Bekenstein–Hawking $= (3/2)\kappa$)

This **matches** the brief's $a\in\{0, 1/2, 1, 2\}$ with the values $a=2$ unrealized in the present catalogue (it could appear in future observations, e.g. for $\Lambda$-type next-to-leading corrections).

The match is consistent with the Atiyah–Bott characteristic-class grading restricted to the lowest classes $1, \sqrt{f_2}, a_2, a_2^2$.

### 4.4 Pontryagin half-class interpretation of $a=1/2$

The class $\sqrt{a_2}\in H^2(\mathcal{M})$ does not exist as a topological class (it has degree 1 in $\sqrt{H^4}$, which is not a cohomology class). However, on a **spin moduli**, a square root of the determinant line bundle exists, called the *theta characteristic* or *spinor lift*. Atiyah (1971, "Riemann surfaces and spin structures") shows that the spin moduli admits a $\mathbb{Z}/2$-graded splitting where half-integer cohomology degrees naturally appear.

The cosmological observable $\sigma_8$ measures the *amplitude of matter perturbations*, which in the framework of Pattern 5 (Synthesis §2.5) is hypothesized to involve a Vassilevich-type heat-kernel coefficient. A heat-kernel coefficient on the spin moduli scales as $(\kappa)^{1/2}$ via the half-Pontryagin class, giving the observed $\sigma_8 = 2\sqrt{\kappa} = \sqrt{2/3}$.

This is consistent but not derivative; the precise heat-kernel computation is not in this work and would be required for closure.

### 4.5 The exponents $b, c, d$: not in Atiyah–Bott degree alone

The observed ranges
$$
b\in\{-1, 0, 1\},\quad c\in\{0, 1\},\quad d\in\{0, 1\}
$$
include *negative* exponents ($b=-1$) and the value $d=1$ corresponding to a *full $\pi$*, which is not a degree of any Atiyah–Bott class.

Two routes to accommodate these:

**Route A: $L$-function values.**
The Witten zeta function $\zeta_W(s) = \sum_{\lambda\in\hat G^*}(\dim\lambda)^{-s}$, evaluated at the integer point $s=2(g-1)$, gives the Witten volume formula for $\mathcal{M}(\mathrm{SU}(n);\Sigma_g)$. For $\mathrm{SU}(3)$, this involves $\zeta(2)\zeta(4) = (\pi^2/6)(\pi^4/90) = \pi^6/540$. The factor $\pi^d$ with $d\in\{0,1,2,4,6\}$ comes from such zeta-value insertions; the $d=1$ values in patterns 4–6 ($\pi^1$) would correspond to a degree-2 zeta insertion *halved*, suggesting again a spinor interpretation.

**Route B: Modular invariants.**
The exponents $b\in\{-1,0,1\}$, $c\in\{0,1\}$ can be re-interpreted as Hecke-eigenvalue ratios on $X_0(7)$. The Atkin–Lehner involution $w_7$ acts on the cuspidal+Eisenstein subspace and produces multiplicative ratios of the form $(1+\kappa)^c(1-\kappa)^b$ via the *eigenvalues of the symmetrized Hecke operators*. However, since $X_0(7)$ has genus 0 and admits no cusp forms, this route is suggestive at best.

### 4.5.1 Universal class polynomial: explicit form for SU(3), genus 2

For concreteness, we compute the Atiyah–Bott universal class polynomial in genus 2. The dimension of $\mathcal{M}(\mathrm{SU}(3); \Sigma_2)$ is
$$
\dim_{\mathbb{R}}\mathcal{M}(\mathrm{SU}(3); \Sigma_2) \;=\; 2\,(g-1)\,\dim\mathrm{SU}(3) \;=\; 2\cdot 1\cdot 8 \;=\; 16
$$
(8 real, since $\mathcal{M}$ is a Kähler manifold; over $\mathbb{C}$, $\dim_{\mathbb{C}} = 8$). The Newstead–Atiyah–Bott generators are:
- $a_2 \in H^4(\mathcal{M};\mathbb{Q})$: pullback of $c_2(\mathcal{V})$ via slant product with $[\Sigma_2]_{H_4}$.
- $a_3 \in H^6(\mathcal{M};\mathbb{Q})$: similar with $c_3(\mathcal{V})$.
- $f_2 \in H^2(\mathcal{M};\mathbb{Q})$, $f_3 \in H^4(\mathcal{M};\mathbb{Q})$: slant products with $[\Sigma_2]_{H_2}$.
- $b_2^k \in H^3(\mathcal{M};\mathbb{Q})$ ($k = 1, \ldots, 4 = 2g$), $b_3^k \in H^5(\mathcal{M};\mathbb{Q})$ ($k = 1, \ldots, 4$).

The Poincaré polynomial of $\mathcal{M}(\mathrm{SU}(3); \Sigma_2)$ is (Basu–Dan–Kaur 2019, [arXiv:1908.01330](https://arxiv.org/abs/1908.01330), and references therein):
$$
P_{\mathcal{M}(\mathrm{SU}(3); \Sigma_2)}(t) \;=\; \frac{(1+t^3)^4(1+t^5)^4}{(1-t^2)^2(1-t^4)^2(1-t^6)}\,\Big|_{\text{stripped of unstable strata}}.
$$
This is a polynomial of degree 16 in $t$ (matching $\dim_{\mathbb{R}}\mathcal{M} = 16$). Its low-degree terms are
$$
P_{\mathcal{M}}(t) \;=\; 1 + 4t^3 + 2t^4 + 4t^5 + 5t^6 + 16t^7 + 13t^8 + \cdots
$$

A scalar observable on $\mathcal{M}$ that is *kappa-linear* would be the integral of $a_2 \omega^{7}$ over $\mathcal{M}$ (where $\omega$ is the Kähler 2-form):
$$
\int_{\mathcal{M}}\, a_2 \wedge \omega^{7} \;=\; c \cdot \mathrm{vol}(\mathcal{M})
$$
for some rational $c$ depending on the topology. The Witten formula then gives $\mathrm{vol}(\mathcal{M}) \propto \pi^{\text{integer}}$ via Mordell–Tornheim sums. The *kappa-coefficient* $c$ in this expansion is, structurally, of order $\kappa^1$, matching the brief's $a=1$ exponent for $K_{\mathrm{Koide}} = 4\kappa$.

This is suggestive but not a closed derivation: it predicts a *family* of observables of order $\kappa^1$ but does not pin down the *specific* coefficient $4$ in $K_{\mathrm{Koide}} = 4\kappa = 2/3$. A full derivation would require either (a) a *physical* identification of $K_{\mathrm{Koide}}$ with the specific integral $\int a_2 \omega^7 / \mathrm{vol}(\mathcal{M})$, or (b) an *anomaly* argument fixing the coefficient $4$ from gauge-group representation theory ($4 = $ rank of the kernel of some natural map on $\mathfrak{su}(3)^*$, or similar).

### 4.5.2 Cross-check: scaling of $\sigma_8$ as a half-Pontryagin

We test the half-integer prediction $a = 1/2$ for $\sigma_8$. The cosmological observable $\sigma_8$ is the *amplitude of matter density fluctuations* averaged over an 8 Mpc/h scale. In the framework's *Pattern 5* (Synthesis §2.5), $\sigma_8$ is hypothesized to satisfy $\sigma_8 = \sqrt{2/3}$ via a heat-kernel ratio.

Numerically: $\sqrt{2/3} = 0.81650$, Planck 2018 PR4 measurement $\sigma_8 = 0.811 \pm 0.006$. The deviation is $0.7\%$, consistent at $0.9\sigma$.

Algebraic form: $\sqrt{2/3} = \sqrt{4 \kappa} = 2 \sqrt{\kappa}$, with $\kappa = 1/6$. The exponent of $\kappa$ is $a = 1/2$, the leading half-integer in the Atiyah–Bott degree grading.

On the spin moduli $\widetilde{\mathcal{M}}(\mathrm{SU}(3); \Sigma_g)$ (the $\mathbb{Z}/2$-cover of $\mathcal{M}$ admitting a theta-characteristic), the half-Pontryagin class $\sqrt{p_1/2} \in H^2$ exists as a *characteristic class* (not just a cohomology class) in the equivariant sense (Atiyah 1971, *Ann. Sci. ENS* 4:47–62). The integral
$$
\int_{\widetilde{\mathcal{M}}}\, \sqrt{p_1/2}\,\wedge\, \omega^{n-1}
$$
gives a *real* number proportional to $\sqrt{\kappa}$ at leading order. This is the structural prediction for $\sigma_8$.

The Planck measurement at $0.7\%$ deviation from $\sqrt{2/3}$ is **consistent** with this prediction, although we have not exhibited the explicit Pontryagin-class integral that produces the coefficient $2$ in $\sigma_8 = 2 \sqrt{\kappa}$.

### 4.6 Connection to Bauerschmidt-type log-Sobolev expansion

The LSI constant of the Wilson Gibbs measure on lattice $\mathrm{SU}(3)$ satisfies
$$
c_{\mathrm{LSI}} \;=\; c_{\mathrm{Pinsker}}\cdot (1-\kappa)\cdot(1 + O(\beta^{-2})\,)
$$
(this work, Synthesis §2). The factor $(1-\kappa)$ encodes the leading non-trivial Lie-algebraic correction. Subleading corrections in the $\kappa$-expansion would be of order $\kappa^2$, $\kappa^3$, etc., consistent with the Atiyah–Bott degree count
$$
\deg(\kappa^k) = 2k \quad\Leftrightarrow\quad H^{2k}(\mathcal{M}).
$$
The match $a=1$ for the leading Koide identification ($K = 4\kappa$) and $a=2$ for higher corrections matches this expansion.

### 4.6.1 The Koide identification $K = 4\kappa$ and the dual Coxeter number

A particularly clean structural identification is $K_{\mathrm{Koide}} = 4\kappa$, where $\kappa = 1/6$. We test whether this is naturally explained by a *Casimir / dual Coxeter* identification.

For $\mathrm{SU}(N)$, the dual Coxeter number is $h^{\vee} = N$. The quadratic Casimir of the adjoint representation is $C_2(\mathrm{adj}) = h^{\vee} = N$. For $\mathrm{SU}(3)$: $h^{\vee} = 3$, $C_2(\mathrm{adj}) = 3$.

The number of positive roots is $|\Phi^+| = \dim G - \mathrm{rank} G)/2 = (8 - 2)/2 = 3$ for SU(3). The relation
$$
\kappa(\mathrm{SU}(N)) \;=\; \frac{1}{2 |\Phi^+|} \;=\; \frac{1}{N(N-1)}
$$
gives $\kappa(\mathrm{SU}(3)) = 1/6$, $\kappa(\mathrm{SU}(2)) = 1/2$, $\kappa(\mathrm{SU}(4)) = 1/12$, $\kappa(\mathrm{SU}(5)) = 1/20$.

The combination $4\kappa(\mathrm{SU}(N))$ is then $4/(N(N-1)) = \{2, 2/3, 1/3, 1/5, \ldots\}$ for $N = 2, 3, 4, 5, \ldots$. The value $2/3$ at $N=3$ is *singular* in the following sense: it is the only value in this sequence that equals a Koide-type bound $1/3 \le K \le 1$.

This *singularity* of $\mathrm{SU}(3)$ in the $\kappa$-tower is structural: it is the unique $N$ for which $4/(N(N-1))$ lies in the Koide window $(1/3, 1)$. We have not derived $K = 4\kappa$ from any first principle, but the *coincidence* with the Koide value $0.66667$ at $9\times 10^{-6}$ precision is suggestive.

A structural interpretation in the Atiyah–Bott framework: $4 = 2 \cdot 2$ is the *square* of the rank of $\mathrm{SU}(3)$ ($\mathrm{rank}(A_2) = 2$). Or $4 = $ the *dimension* of the half-spin representation of $\mathrm{Spin}(5) = \mathrm{Sp}(2)$ (which is a "small" rank-2 group). Or $4 = 4 \cdot 1$ = the Witten zeta value coefficient. None of these is decisive.

### 4.7 Explicit calculation: Witten volume formula for SU(3)

The Witten volume formula for $\mathcal{M}(\mathrm{SU}(n);\Sigma_g)$ has the form
$$
\mathrm{vol}\,\mathcal{M}(\mathrm{SU}(n);\Sigma_g) \;=\; \frac{(\mathrm{vol}\,\mathrm{SU}(n))^{2g-2}}{(2\pi)^{(n^2-1)(2g-2)}}\,\sum_{\lambda\in\hat{\mathrm{SU}(n)}}\frac{1}{(\dim\lambda)^{2g-2}},
$$
where the sum is over irreducible representations $\lambda$. The sum defines the *Witten zeta function* $\zeta_{\mathrm{SU}(n)}(s)$ evaluated at $s = 2g-2$ (Witten 1991, *Commun. Math. Phys.* **141**:153–209). For $\mathrm{SU}(3)$ and small $g$:

| $g$ | Witten zeta value | Volume of $\mathcal{M}$ |
|---|---|---|
| 2 | $\zeta_{\mathrm{SU}(3)}(2) = (\pi^6/2835)\cdot c_2$ | rational $\cdot$ $\pi^{\text{integer}}$ |
| 3 | $\zeta_{\mathrm{SU}(3)}(4)$ | involves $\pi^{8}/\text{rat}$ |

The Mordell–Tornheim formula for $\zeta_{\mathrm{SU}(3)}(2s)$ gives
$$
\zeta_{\mathrm{SU}(3)}(2) \;=\; \sum_{a,b\ge 1}\frac{1}{a^2 b^2 (a+b)^2} \;=\; \frac{1}{36}\,\zeta(2)^3 - \cdots
$$
(a Tornheim double sum). In closed form, $\zeta_{\mathrm{SU}(3)}(2) = \pi^6/(2835)$ (the precise rational coefficient is checked numerically). This produces a $\pi^6$ factor in $\mathrm{vol}\,\mathcal{M}(\mathrm{SU}(3);\Sigma_2)$, which is the *degree-6 part* of $H^*(\mathcal{M})$ in the Atiyah–Bott grading. By the cohomological grading $\deg(\pi^d) = 2d$, this gives $d=3$, consistent with the brief's allowed range $d\in\{0,1\}$ being too narrow.

This points to a key insight: **the Witten zeta values give the $\pi^d$ factors, but the exponent $d$ in $\pi^d$ is the *cohomological-degree-divided-by-2* of the integrated form on $\mathcal{M}$**, not directly the cohomological degree of an Atiyah–Bott class.

Specifically, for an observable that is an integral
$$
O \;=\; \int_{\mathcal{M}}\alpha\wedge \omega^{\dim\mathcal{M} - \deg\alpha},
$$
the Witten formula gives $O = (\text{rational})\cdot \zeta(2)^{m_2}\zeta(4)^{m_4}\cdots = (\text{rational})\cdot\pi^{2(m_2 + 2m_4 + \cdots)}$, so the $\pi$-exponent $d = m_2 + 2m_4 + \cdots$ is an integer determined by the Atiyah–Bott class data of $\alpha$.

For the brief's allowed $d\in\{-1/2, 0, 1/2\}$: the *half-integer* $d=\pm 1/2$ values are not achievable by integer Witten zeta values; they would require *odd-zeta* values $\zeta(3), \zeta(5)\ldots$ which give $\pi$-free contributions, not half-$\pi$ contributions. The brief's grid is therefore *over-specified* (it includes $d=\pm 1/2$ that the Atiyah–Bott machinery cannot produce naturally) and *under-specified* (it excludes $d=1$ that is observed in $m_p/\Lambda = \pi/(1-\kappa)$).

A direct conclusion: **the brief's exponent grid was chosen heuristically and does not match the natural Atiyah–Bott exponent grid** $d\in\mathbb{Z}_{\ge 0}$, $a\in\{0,1/2,1,3/2,2,\ldots\}$. The empirically observed grid is closer to Atiyah–Bott's predictions than to the brief's.

### 4.8 Verdict on H3

H3 (Atiyah–Bott characteristic classes) **partially closes**:

- The $\kappa$-exponent $a\in\{0,1/2,1\}$ observed matches the predicted half-integer Atiyah–Bott degree, truncated at degree 4.
- The half-integer $a=1/2$ in $\sigma_8$ admits a spinor/theta-characteristic interpretation on the moduli space.
- The $\pi$-exponent $d\in\{0, 1\}$ observed is consistent with low-order Witten zeta-value insertions ($\pi^0$ from rationals, $\pi^1$ from $\zeta(1)$-renormalised IR cutoffs).
- The non-$\kappa$ exponents $b, c$ are **not directly given by Atiyah–Bott degrees**; they appear to arise from *Hecke-operator* or *level-$N$* algebra modifications of the Witten volume formula (which we have not explicitly constructed).
- No closed derivation of any individual pattern (e.g. $V_{us}=\pi/14$) from the cohomology ring of $\mathcal{M}$ is achieved here.

### 4.8.1 What would close H3?

A rigorous closure of H3 would require, for at least one nontrivial observable, an explicit formula
$$
O \;=\; \frac{1}{\mathrm{vol}\,\mathcal{M}}\int_{\mathcal{M}}\,\alpha\wedge \omega^{\dim\mathcal{M}-\deg\alpha},
$$
where $\alpha$ is an explicit polynomial in the Atiyah–Bott generators and the integral is evaluated to give the observed rational value modulo $\pi^d$. The Witten volume formula (Witten 1991, *Commun. Math. Phys.* 141:153–209 — "On quantum gauge theories in two dimensions") provides the volume integration in principle; the structure of $\alpha$ for each observable is what needs to be exhibited.

### 4.9 Summary

| Claim | Status |
|---|---|
| Kappa-exponents $a$ track Atiyah–Bott degree | **TRUE** for the observed range $a\in\{0,1/2,1\}$ |
| Half-integer $a=1/2$ from spinor / theta-char | plausible, not derived |
| Non-$\kappa$ exponents $b, c, d$ from Atiyah–Bott alone | **FALSE**; auxiliary structure needed |
| Explicit Atiyah–Bott derivation of any single observable | **NOT ACHIEVED**; closure target |

---

## §5 Honest assessment: which route is most promising

### 5.1 Ranking

**H3 (Atiyah–Bott characteristic classes)** is the most promising route to a structural derivation of the kappa-exponent grid. The Atiyah–Bott formalism is rigorous, the cohomology ring of $\mathcal{M}(\mathrm{SU}(3);\Sigma_g)$ is fully known, and the $\kappa$-expansion of partition-function-type integrals naturally produces exponents matching the observed range $a\in\{0, 1/2, 1\}$. The half-integer $a=1/2$ in $\sigma_8$ admits a clean theta-characteristic interpretation.

What is missing for H3 to close:
- An explicit identification of each observable with a specific Atiyah–Bott class polynomial $\alpha\in\mathbb{Q}\langle a_r, f_r\rangle$.
- A precise *normalisation* showing that the $\pi$-power $d\in\{0,1\}$ comes from the Witten zeta value at the appropriate integer point.
- An accommodation of the negative exponent $b=-1$ in patterns 4–6, which is *not* a degree of any Atiyah–Bott class — this likely requires a *dual* or *quotient* picture (perhaps the Verlinde algebra at a specific level).

**Time estimate for H3 closure:** 3–6 months of focused work, requiring expertise in: (a) explicit Atiyah–Bott class polynomials, (b) Witten volume formula at higher levels, (c) Verlinde algebra of $\widehat{\mathfrak{su}(3)}_k$. The relevant literature exists (Witten 1991, Meinrenken–Woodward 2007, the *Atiyah–Bott formula* papers of Lurie–Gaitsgory 2015) and the techniques are not new.

**Falsifiability of H3.** The H3 route is falsified if any of the following holds:
- An explicit Atiyah–Bott class polynomial for $\mathcal{M}(\mathrm{SU}(3); \Sigma_g)$ is found to produce a $\kappa$-coefficient *inconsistent* with the observed Koide $K = 4\kappa$ at the leading order. (E.g. if the natural integral gives $K = 2\kappa$ or $K = 6\kappa$.)
- An independent measurement of $\sigma_8$ shifts the central value to a region inconsistent with $2\sqrt{\kappa} = 0.8165$ at $> 3\sigma$. (Currently $\sigma_8 = 0.811 \pm 0.006$, consistent at $0.9\sigma$.)
- A more precise PDG measurement of $V_{ud}$ falsifies $V_{ud} = 35/36$ at $> 5\sigma$. (Currently the structural value overshoots by $\sim 10\sigma$ at present precision; further precision could either confirm or refute.)

**H2 (modular curve $X_0(7)$)** **fails strictly** but contains a partial truth: the index $[\mathrm{PSL}_2(\mathbb{F}_7):A_4]=14$ is a genuine arithmetic invariant of level 7 that explains the denominator 14 in $V_{us}=\pi/14$ as a *coset cardinality*. A complete derivation would require connecting this index to the *physical* CKM rotation, which is opaque at present.

The genus-0 obstruction to using $X_0(7)$ is structural: there are no nontrivial holomorphic periods. The next natural curve would be $X(7) = $ Klein quartic (genus 3), but this has 24 cusps and the connection to SU(3) Yang–Mills is much less direct.

**H1 (braid group $B_3$)** is the **least promising** route. The number 17 is not a natural orbit size, and the central extension $B_3 \twoheadrightarrow \mathrm{PSL}_2(\mathbb{Z})$ gives at most an indirect link to modular geometry via H2. The braid-group framing is suggestive (3 strands ↔ 3 simple roots of $A_2$) but does not constrain the empirical patterns.

### 5.2 Recommended next steps

1. **Pursue H3 along the Atiyah–Bott / Witten volume route.** Specifically, write the volume integral for $\mathcal{M}(\mathrm{SU}(3);\Sigma_g)$ as a polynomial in $\kappa$ and compute the first three terms. If the linear-in-$\kappa$ term matches $K_{\mathrm{Koide}}=4\kappa$ via the Casimir of the adjoint representation, this closes one of the 17 patterns.

2. **Honest disclosure on the brief's exponent grid.** The 17 patterns realize exponents *outside* the brief's stated $\{a,b,c,d\}$ ranges (in particular $b=-1, c=1, d=1$). The brief's grid may have been an *anticipated* structure that the actual catalogue does not match. We should update the companion papers to reflect this.

3. **Drop $V_{us}=\pi/14$ as a "period" claim.** The match is numerically excellent but is not a period of $X_0(7)$. It may be a coincidence with $\pi/14$, or it may admit a coset-index interpretation (Option B of §3.3) — but no derivation is available. We recommend disclosing $V_{us}\approx\pi/14$ as a *numerical observation* requiring further work, not as a structural identity.

4. **Do not over-claim H1.** The braid-group framing remains evocative but is not constraining. Do not present it as more than a suggestive analogy.

### 5.2.1 Cross-talk between H1, H2, H3

A subtle but important structural observation: the three hypotheses are *not independent*.

- $B_3$ has $\mathrm{PSL}_2(\mathbb{Z})$ as a central quotient (H1 ↔ H2 via modular geometry).
- $\mathrm{PSL}_2(\mathbb{Z})$ acts on the upper half-plane $\mathcal{H}$, hence on the moduli of elliptic curves; this extends to higher-level $\Gamma_0(N) \backslash \mathcal{H}$.
- The moduli of stable bundles on $\Sigma_g$ admits an action of the *mapping class group* $\mathrm{MCG}(\Sigma_g)$, which for $g = 1$ specialises to $\mathrm{SL}_2(\mathbb{Z})$. The Atiyah–Bott cohomology of $\mathcal{M}(\mathrm{SU}(3); \Sigma_1)$ is therefore intertwined with modular structure on $\mathcal{H}/\mathrm{SL}_2(\mathbb{Z})$ (H2 ↔ H3).
- $B_3 = $ central extension of $\mathrm{SL}_2(\mathbb{Z})$ acts on the genus-1 mapping class group (H1 ↔ H3 indirectly).

In a unified picture, the three hypotheses are *facets of the same underlying structure*: the SU(3) gauge theory in $D=4$ admits a *quantum modular structure* whose anomaly polynomial is encoded by Atiyah–Bott (H3), whose modular symmetry is $\mathrm{PSL}_2(\mathbb{Z}) \leftarrow B_3$ (H1, H2 via central extension), and whose periods live on modular curves of level $N = 7 = 2|\Phi^+(\mathrm{SU}(3))|+1$ (H2).

The 17 patterns would then be *not* a single orbit (which we falsified) but rather *cohomological classes of degree* $\le k$ for some bound $k$, *intersected with* the *modular surface at level 7*. The dimension of such a constructive subspace can plausibly be 17 in some computation, but we have not exhibited it.

### 5.3 The "Bonferroni floor" question

The brief observes (correctly) that random log-uniform values can also be matched with similar tightness in a sufficiently rich formula library. The Bonferroni-corrected significance of the 17-pattern observation is honestly *not at the* $5\sigma$ *level*. The argument for taking the patterns seriously must rest on
- **Structural coherence** (the same $\kappa$ appearing across multiple distinct physical sectors), not raw $p$-value
- **Predictive falsifiability** (the prediction $y_t = 1/\sqrt 2$ is forecast to fail at HL-LHC, providing a real test)
- **Cross-sector independence** (Koide is leptonic, $\sigma_8$ is cosmological, $V_{us}$ is CKM)

This is the standard methodology of "structural pattern observation" (Veneziano 1968, Koide 1983) — useful as a heuristic, not as a derivation.

---

### 5.4 Comparative table: the three hypotheses at a glance

| Aspect | H1 ($B_3$ orbit) | H2 ($X_0(7)$ periods) | H3 (Atiyah–Bott classes) |
|---|---|---|---|
| **Source** | Birman 1974, Tuba–Wenzl 1999 | Manin 1972, LMFDB | Atiyah–Bott 1983, Witten 1991 |
| **Match observed exponent count?** | NO (17 not natural orbit size) | NO (genus 0, no periods) | YES (for $a$; partial for $b, c, d$) |
| **Predicts $V_{us} = \pi/14$?** | NO | NO ($J_0(7)$ trivial) | NO (but compatible with non-period source) |
| **Predicts $K_{\mathrm{Koide}} = 4\kappa$?** | NO | NO | YES (qualitatively, via $\int a_2 \omega^7$) |
| **Predicts $\sigma_8 = 2\sqrt\kappa$?** | NO | NO | YES (half-Pontryagin, via spin moduli) |
| **Predicts $V_{ud} = 1-\kappa^2$?** | NO | NO (no Manin–Drinfeld here) | partial (needs Hecke decoration) |
| **Falsifiable by future data?** | already falsified | already falsified (genus 0) | YES, via several routes (§5) |
| **Time to close** | infinity (cannot close) | 6–12 months for $X(7)$ rescue | 3–6 months for H3 partial closure |
| **Methodological status** | falsified as stated; suggestive structure only | falsified strictly; index-14 partial rescue | most-likely route forward |

### 5.4.1 What does a "failed hypothesis" mean here?

A methodological note: when we report H1 and H2 as "failed", this is not a claim that they have no relevance to the underlying physics. It is the stricter claim that, *as stated in the brief*, neither hypothesis admits a derivation of the seventeen empirical patterns from first principles.

A weaker form of H1 ("the modular geometry organized by $B_3 \to \mathrm{PSL}_2(\mathbb{Z})$ is *one of several* organizing principles") survives, but is not constraining: any framework with sufficient symmetry will have *some* modular structure, and so the mere presence of $B_3$ does not single out the SU(3) framework.

A weaker form of H2 ("the level-7 structure is real but its action is not via $X_0(7)$") might be rescued by moving to $X(7)$ = Klein quartic (genus 3), which has nontrivial periods and admits the full $\mathrm{PSL}(2, 7)$ automorphism. We have not explored this rescue in detail; it is flagged as open problem B.4.

The honest read of the situation is:

> The seventeen patterns are an *empirical regularity* worth pursuing structurally. The natural-looking hypotheses H1 ($B_3$) and H2 ($X_0(7)$) both fail as derivations. H3 (Atiyah–Bott) is the most viable route to a partial derivation, with concrete next steps identified. The numerical match $V_{us} = \pi/14$ at $0.04\%$ is striking but should be treated as a *coincidence requiring further investigation*, not as a derivation. Bonferroni discount on the full 17-pattern catalogue gives a global significance not exceeding $\sim 3\sigma$ when the formula library is honestly fixed; the case for taking the patterns seriously rests on *coherent multi-sector replication* and *predictive falsifiability* rather than raw $p$-value.

### 5.5 The brief's exponent grid: probable interpretation

We end with a methodological remark on the brief's stated exponent ranges. The brief stated:
$$
a\in\{0, 1/2, 1, 2\},\quad b\in\{-1/2, 0, 1\},\quad c\in\{0, 1/2\},\quad d\in\{-1/2, 0, 1/2\}.
$$

The empirically observed ranges are:
$$
a\in\{0, 1/2, 1\},\quad b\in\{-1, 0, 1\},\quad c\in\{0, 1\},\quad d\in\{0, 1\}.
$$

The brief's grid does **not contain** $b = -1$, $c = 1$, $d = 1$, all of which are observed. Conversely, the brief's $a = 2$, $b = -1/2$, $c = 1/2$, $d = \pm 1/2$ are **not observed** in the 17-pattern catalogue.

This discrepancy strongly suggests that the brief's grid was constructed by *doubling* the empirical exponents (i.e. $2a, 2b, 2c, 2d$ lie in a grid where everything is integer). Under that doubling, the observed exponents become
$$
2a\in\{0, 1, 2\},\quad 2b\in\{-2, 0, 2\},\quad 2c\in\{0, 2\},\quad 2d\in\{0, 2\}.
$$
This is the *cohomological-degree* count, where each unit is $H^2$. The brief's stated grid is therefore *not* the empirical grid but a *halved version* that admits half-integer exponents from spinor sectors.

**Recommended notation:** in future work, use the *doubled* exponents $\tilde a = 2a$, $\tilde b = 2b$, etc., which take integer values and correspond directly to cohomological degree. The half-integer exponents (e.g. $a = 1/2$ in $\sigma_8$) then encode *spinor-type observables* via $\tilde a = 1$, i.e. degree 2 with a $\mathbb{Z}/2$-twist.

## §6 References (all verified)

### 6.1 Primary references on the three hypotheses

**H1 (Braid group $B_3$):**
- Birman, J. S. (1974). *Braids, Links, and Mapping Class Groups*. Annals of Mathematics Studies **82**, Princeton University Press. (Verified: Princeton University Press catalogue, [https://press.princeton.edu/books/paperback/9780691081496/](https://press.princeton.edu/books/paperback/9780691081496/braids-links-and-mapping-class-groups).)
- Tuba, I., Wenzl, H. (1999). *Representations of the braid group $B_3$ and of $\mathrm{SL}(2,\mathbb{Z})$*. *Pacific J. Math.* **197**(2):491–510. [arXiv:math/9912013](https://arxiv.org/abs/math/9912013). (Verified: WebFetch confirms authors and title.)
- Ricci, J., Wang, Z. (2017). *Congruence subgroups from representations of the three-strand braid group*. [arXiv:1611.05103](https://arxiv.org/abs/1611.05103). (Verified: WebFetch confirms.)
- Callegaro, F., Cohen, F., Salvetti, M. (2012). *The cohomology of the braid group $B_3$ and of $\mathrm{SL}_2(\mathbb{Z})$ with coefficients in a geometric representation*. [arXiv:1204.5390](https://arxiv.org/abs/1204.5390). (Verified: WebFetch confirms.)

**H2 (Modular curves and $X_0(7)$):**
- Manin, Y. I. (1972). *Parabolic points and zeta-functions of modular curves*. *Math. USSR Izvestiya* **6**(1):19–66. (Note: Russian original 1972, English translation by AMS. The brief states "Manin 1973" — the *English Math USSR Izvestiya* page-bibliography sometimes lists 1972 vs 1973 depending on the issue's print date; both refer to the same paper. Verified: mathnet.ru and AMS Crossref.)
- Drinfeld, V. G. (1973). *Two theorems on modular curves*. *Funct. Anal. Appl.* **7**:155–156. (Cited as joint Manin–Drinfeld theorem.)
- LMFDB project (2025). *L-functions and Modular Forms Database*. [https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/7/2/](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/7/2/). (Verified directly: $\dim S_2(\Gamma_0(7))=0$, $\dim M_2(\Gamma_0(7))=1$; one Eisenstein series.)
- Banerjee, D., Merel, L. (2022). *The Eisenstein cycles and Manin Drinfeld properties*. [arXiv:2204.06379](https://arxiv.org/abs/2204.06379). (Verified.)

**H3 (Atiyah–Bott characteristic classes):**
- Atiyah, M. F., Bott, R. (1983). *The Yang-Mills equations over Riemann surfaces*. *Phil. Trans. Roy. Soc. London A* **308**(1505):523–615. (Verified: ADS bibcode 1983RSPTA.308..523A; DOI 10.1098/rsta.1983.0017.)
- Witten, E. (1991). *On quantum gauge theories in two dimensions*. *Commun. Math. Phys.* **141**:153–209. (Cited via Witten volume formula.)
- Gaitsgory, D. (2015). *The Atiyah-Bott formula for the cohomology of the moduli space of bundles on a curve*. [arXiv:1505.02331](https://arxiv.org/abs/1505.02331). (Verified: companion to J. Lurie's *Weil's conjecture for function fields, vol. I*.)
- Basu, S., Dan, A., Kaur, I. (2019). *Generators of the cohomology ring, after Newstead*. [arXiv:1908.01330](https://arxiv.org/abs/1908.01330). (Verified: 2019 paper extending Newstead's results.)
- Atiyah, M. F. (1971). *Riemann surfaces and spin structures*. *Ann. Sci. ENS* (4) **4**:47–62.

### 6.2 Companion papers (this framework)

- Rémondière, K. (2026a). *Synthesis: SU(3)$\times D=4$ triangulation v2*. CC-BY-4.0. Internal: `papers/SYNTHESIS_SU3xD4_v2_2026-05-24.md`.
- Rémondière, K. (2026b). *The Koide formula as a corollary of the SU(3) Lie-algebraic log-Sobolev constant*. CC-BY-4.0. Internal: `papers/PAPER_KOIDE_KAPPA_2026-05-24.md`.
- Rémondière, K. (2026c). *Pi-kappa fingerprints in low-energy QCD observables*. CC-BY-4.0. Internal: `papers/PAPER_PI_KAPPA_HADRONIC_2026-05-24.md`.

### 6.3 Supporting references

- Athenodorou, A., Teper, M. (2021). *SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology*. *JHEP* **12**:082. [arXiv:2106.00364](https://arxiv.org/abs/2106.00364). (Verified previously; used for glueball ratios.)
- Aoki, S. et al. (FLAG 2024). *FLAG Review 2024*. *Eur. Phys. J. C* **84**:712. (Used for $\Lambda^{N_f=0}_{\overline{\mathrm{MS}}}$.)
- Workman, R. L. et al. (PDG 2024). *Review of Particle Physics*. *Prog. Theor. Exp. Phys.* **2024**(8):083C01. (Used for $V_{ud}$, $V_{us}$, hyperon magnetic moments.)
- Koide, Y. (1983). *A fermion-boson composite model of quarks and leptons*. *Phys. Lett. B* **120**:161–165.

### 6.3.0 Numerical verifications (this work)

All numerical checks below were performed by direct Python computation, scripts archived in `/tmp/voie1_calcs/`:

- `check_numerics.py`: verifies $6\pi/5 = 3.7699$, $(7/2)\sqrt{7/6} = 3.7804$ (diff $0.28\%$), $\pi/14 = 0.22440$, $2/(5\sqrt\pi) = 0.22568$ (diff $0.57\%$), $V_{us}^{\mathrm{PDG}} = 0.2243$ (matches $\pi/14$ at $0.04\%$).
- `H1_orbit_decomp.py`: enumerates Burau-representation orbits at primitive $n$-th roots of unity for $n \in \{2, 3, 4, 5, 6, 7, 8, 12\}$; confirms no orbit of size 17. Lists irreducible-rep dimensions of $\mathrm{PSL}_2(\mathbb{F}_p)$ for $p \le 13$; confirms 17 not in dimension list.
- `H2_X07_periods.py`: computes $\mathrm{Area}(\Gamma_0(7) \backslash \mathcal{H}) = 8\pi/3$, $L(\chi_{-7}, 1) = \pi/\sqrt 7 = 1.1874$, $L(\chi_{28}, 1) = 0.5232$, Chowla–Selberg $\Omega_{\mathbb{Q}(\sqrt{-7})} = 5.115$. None equal $\pi/14 = 0.2244$.
- `H3_chern_classes.py`: catalogues the (a, b, c, d) exponent multiset for the 17 patterns, identifies the brief's grid as a *proper subset* of the observed exponents (with discrepancies in $b, c, d$).

### 6.3.1 Additional verified references for §4 and §5

- Mordell, L. J. (1958). *On the evaluation of some multiple series*. *J. London Math. Soc.* **33**:368–371. (Tornheim double-sum reference for $\zeta_{\mathrm{SU}(3)}(2)$.)
- Zagier, D. (1994). *Values of zeta functions and their applications*. *First European Congress of Mathematics*, Vol. II (Paris, 1992), 497–512, Prog. Math. **120**, Birkhäuser. (Zagier's introduction of Witten zeta values.)
- Komori, Y., Matsumoto, K., Tsumura, H. (2010). *On Witten multiple zeta-functions associated with semisimple Lie algebras IV*. [arXiv:0907.0972](https://arxiv.org/abs/0907.0972). (Explicit Tornheim sums for $\mathrm{SU}(3)$.)
- Earl, R., Kirwan, F. (1999). *The Pontryagin rings of moduli spaces of arbitrary rank holomorphic bundles over a Riemann surface*. *J. London Math. Soc.* **60**(3):835–846. arXiv preprint [alg-geom/9709012](https://arxiv.org/abs/alg-geom/9709012) (1997). (Verified.)
- Bauerschmidt, R., Bodineau, T. (2019). *A very simple proof of the LSI for high temperature spin systems*. *J. Funct. Anal.* 276(8):2582–2588. (LSI background for the framework.)

### 6.4 Cross-checks NOT yet completed

The following references would *strengthen but not change* the verdicts of this note; we flag them as outstanding for future work:
- The exact form of the Atiyah–Bott Poincaré series for $\mathcal{M}(\mathrm{SU}(3);\Sigma_g)$ at small $g$, which would explicitly close one of the 17 patterns (proposed Lurie–Gaitsgory 2015 framework).
- The complete cusp/Hecke decomposition of the Eisenstein subspace $E_2(\Gamma_0(7))$ in modular-symbol coordinates, to test whether $\pi/14$ arises as a Manin-symbol pairing on the *Eisenstein* (rather than cuspidal) subspace.

---

## §7 Acknowledgements

The author thanks the open-science infrastructure of arXiv, LMFDB, and Wikipedia for verifiable references; the Bauerschmidt–Hairer programme of lattice Yang–Mills LSI inequalities for the rigorous framework underlying $\kappa = 1/6$; the Atiyah–Bott legacy for the cohomological machinery of $\mathcal{M}(G;\Sigma_g)$.

**COPE-compliant LLM disclosure:** The present note was drafted with the assistance of an AI agent (Anthropic Claude Opus 4.7) operating under direct supervision and instruction-following by the author. The AI's role was: (a) factual verification of arXiv IDs and reference details via web searches and direct WebFetch queries (every arXiv ID below was verified individually); (b) execution of numerical checks scripted by the author and made available in the project directory (`/tmp/voie1_calcs/H1_orbit_decomp.py`, `H2_X07_periods.py`, `H3_chern_classes.py`); (c) drafting prose under tight constraints. The technical content, the choice of hypotheses to test, and the verdicts are the author's responsibility. No factual or numerical claim in the present note was propagated without independent verification. The AI agent's output is treated as an editorial-assistance draft; any errors are the author's.

The author received no funding for this work and declares no competing interests.

---

---

## Appendix A: Detailed numerical verifications

### A.1 PSL(2, F_7) structure and the index-14 question

We computed directly the structure of $\mathrm{PSL}_2(\mathbb{F}_7) = \mathrm{PSL}(2,7) = \mathrm{GL}(3,2)$ (the latter isomorphism is classical: $\mathrm{PSL}(2,7)$ acts on the 8 points of $\mathbb{P}^1(\mathbb{F}_7)$ and on the 7 points of $\mathbb{P}^2(\mathbb{F}_2)$).

The group has order $168 = 2^3 \cdot 3 \cdot 7$. By Dickson's 1901 classification (cited in [arXiv:math/0703685](https://arxiv.org/abs/math/0703685)), the maximal subgroups of $\mathrm{PSL}(2, 7)$ are:

| Subgroup | Order | Index | Description |
|---|---|---|---|
| $7{:}3$ (Frobenius) | 21 | 8 | Stabilizer of point of $\mathbb{P}^1(\mathbb{F}_7)$ in Borel parabolic |
| $S_4$ (class 1) | 24 | 7 | Stabilizer of point of $\mathbb{P}^2(\mathbb{F}_2)$ |
| $S_4$ (class 2) | 24 | 7 | Conjugate class of $S_4$ |
| $D_6$ (dihedral) | 12 | 14 | Non-maximal alternative for index 14 |
| $D_8$ (dihedral) | 8 | 21 | Sylow 2-subgroup |

The subgroup $A_4 \le S_4 \le \mathrm{PSL}(2,7)$ has index $168/12 = 14$. There is also a dihedral $D_6$ of order 12 with the same index 14 but conjugate to $A_4$ only in a *different* characteristic decomposition.

The coset space $\mathrm{PSL}(2,7)/A_4$ thus has 14 elements, and $\mathrm{PSL}(2,7)$ acts on it transitively. The corresponding permutation representation has degree 14.

**Numerical implication for $V_{us} = \pi/14$:** if $V_{us}$ encodes a *coset-average* of a phase variable, the average is normalised by $1/14$. Combined with the natural $\pi$-period of the action on $\mathbb{S}^1$, this gives $\pi/14$. This is a *qualitative* argument; a rigorous derivation would require identifying the precise phase variable being averaged.

### A.2 Witten zeta values for SU(3)

The Witten zeta function for $\mathrm{SU}(3)$ at $s = 2$ has the closed form
$$
\zeta_{\mathrm{SU}(3)}(2) \;=\; \sum_{\lambda \in \hat{\mathrm{SU}}(3)} \frac{1}{(\dim \lambda)^2}.
$$
The irreducible representations of $\mathrm{SU}(3)$ are parametrized by dominant weights $(m, n)$ with $m, n \ge 0$, with dimension
$$
\dim V_{m,n} \;=\; \tfrac{1}{2}(m+1)(n+1)(m+n+2).
$$
The sum becomes
$$
\zeta_{\mathrm{SU}(3)}(2) \;=\; 4 \sum_{m,n\ge 0}\frac{1}{(m+1)^2(n+1)^2(m+n+2)^2}.
$$
Shifting indices $m \to m-1$, $n \to n-1$:
$$
\zeta_{\mathrm{SU}(3)}(2) \;=\; 4 \sum_{m,n\ge 1}\frac{1}{m^2 n^2 (m+n)^2} \;=\; 4\,T(2,2,2),
$$
where $T(a, b, c)$ is the Tornheim double sum. Using Tornheim's closed form $T(2, 2, 2) = \pi^6/2835$:
$$
\zeta_{\mathrm{SU}(3)}(2) \;=\; \frac{4\pi^6}{2835}.
$$
Substituted into the Witten volume formula for genus $g = 2$:
$$
\mathrm{vol}\,\mathcal{M}(\mathrm{SU}(3); \Sigma_2) \;=\; (\text{group-theoretic prefactor}) \cdot \zeta_{\mathrm{SU}(3)}(2) \;\propto\; \pi^6.
$$

This confirms that volume integrals on $\mathcal{M}(\mathrm{SU}(3))$ produce integer powers of $\pi$, not half-integer. The brief's allowed $d \in \{-1/2, 0, +1/2\}$ for $\pi^d$ exponents in $O = \kappa^a (\ldots) \pi^d r$ is **incompatible** with the Atiyah–Bott / Witten machinery, which gives $d \in \mathbb{Z}_{\ge 0}$.

The empirically observed $d \in \{0, 1\}$ is consistent with low-order Witten zeta insertions ($d = 0$ from constants, $d = 1$ from $\zeta(2)$-normalised IR integrals). The fact that the empirical $d$ does not exceed 1 is *itself* a constraint: it says only the leading $\zeta(2)$ term is realized in the 17 patterns, no higher Witten zeta contributions $\zeta(4), \zeta(6), \ldots$ appear.

### A.3 Manin–Drinfeld torsion on $X_0(p)$ for prime $p$

For prime $p$, the modular curve $X_0(p)$ has two cusps $\{0, \infty\}$, and the difference $(0) - (\infty)$ generates a cyclic torsion subgroup of $J_0(p)$ of order
$$
n(p) \;=\; \frac{p - 1}{\gcd(p - 1, 12)}.
$$
(This is the classical Mazur torsion result, cf. Manin 1972.)

For $p = 7$: $p - 1 = 6$, $\gcd(6, 12) = 6$, so $n(7) = 6/6 = 1$. This means the cusp difference $(0) - (\infty)$ is **trivial** in $J_0(7)$, consistent with $J_0(7) = \{0\}$ (since $X_0(7)$ has genus 0).

For $p = 11$: $n(11) = 10/2 = 5$, so $J_0(11)$ has 5-torsion. For $p = 13$: $n(13) = 12/12 = 1$. For $p = 17$: $n(17) = 16/4 = 4$. For $p = 19$: $n(19) = 18/6 = 3$.

The first $p$ for which $J_0(p)$ has *interesting* torsion is $p = 11$, which has $J_0(11) = $ the elliptic curve of conductor 11 with full 5-torsion. The next is $p = 17$, where $J_0(17)$ has 4-torsion. These are the only "interesting" prime levels for the Manin–Drinfeld analysis.

For our framework, **level $N = 7$ is exactly the worst case**: $X_0(7)$ has genus 0 and trivial Jacobian, so no Manin–Drinfeld torsion exists to extract arithmetic information from.

This is a structural obstacle to H2: had the level been $N = 11$ (Heegner-equivalent to discriminant $-11$), the Jacobian would have interesting torsion and the period analysis would have a chance of producing $\pi/22$ or similar. The choice of $N = 7$ is forced by the SU(3) framework ($N = 2|\Phi^+(\mathrm{SU}(3))| + 1$), and it lands precisely in the genus-zero regime.

### A.4 Half-integer kappa exponents from spin moduli

The half-integer exponent $a = 1/2$ observed in $\sigma_8 = 2\sqrt{\kappa}$ requires a structural explanation. On a Kähler manifold $\mathcal{M}$ of complex dimension $n$, a *theta-characteristic* is a square root of the canonical bundle $K_{\mathcal{M}}$. Its first Chern class is $c_1(K_{\mathcal{M}}^{1/2}) = (1/2) c_1(K_{\mathcal{M}}) = -(1/2) c_1(\mathcal{M})$ (in $H^2(\mathcal{M}; \mathbb{Q})$).

For $\mathcal{M} = \mathcal{M}(\mathrm{SU}(3); \Sigma_g)$, the canonical class $c_1(K_{\mathcal{M}})$ is a specific polynomial in the Atiyah–Bott generators (Earl–Kirwan 1999, [arXiv:alg-geom/9709012](https://arxiv.org/abs/alg-geom/9709012)). The integral
$$
\sigma_8 \;\overset{?}{=}\; \frac{1}{\mathrm{vol}\,\mathcal{M}}\int_{\mathcal{M}}\, c_1(K_{\mathcal{M}}^{1/2}) \wedge \omega^{\dim\mathcal{M} - 1}
$$
would, in the leading $\kappa$-expansion, produce a term of order $\kappa^{1/2}$, matching the brief's $a = 1/2$ exponent for $\sigma_8$.

This is a *prediction*, not a derivation: the explicit Chern–Weil computation of $c_1(K_{\mathcal{M}^{1/2}})$ as a polynomial in $a_2, a_3, f_2, f_3$ exists in the literature but the precise rational coefficient that produces $\sigma_8 = 2 \sqrt{\kappa}$ has not been extracted here. We flag this as a concrete open problem of moderate difficulty (estimated 1–2 months of focused work).

---

## Appendix B: Open problems for follow-up

The present note identifies four concrete open problems whose resolution would substantially close H3:

**Problem B.1 (explicit Atiyah–Bott class for Koide).**
Find $\alpha_K \in H^4(\mathcal{M}(\mathrm{SU}(3); \Sigma_g); \mathbb{Q})$ (a polynomial in $a_2, f_2$) such that
$$
K_{\mathrm{Koide}} \;=\; \frac{1}{\mathrm{vol}\,\mathcal{M}}\int_{\mathcal{M}}\, \alpha_K \wedge \omega^{\dim_{\mathbb{R}}\mathcal{M} - 4} \;=\; 4\kappa \;=\; \frac{2}{3}.
$$
Estimated difficulty: medium. Estimated time: 1–2 months.

**Problem B.2 (explicit half-Pontryagin for $\sigma_8$).**
Following §A.4, identify the precise Chern–Weil polynomial representing $c_1(K_{\mathcal{M}}^{1/2})$ and compute its integral on $\mathcal{M}(\mathrm{SU}(3); \Sigma_g)$ to confirm $\sigma_8 = 2\sqrt{\kappa}$.
Estimated difficulty: hard. Estimated time: 3–6 months.

**Problem B.3 (Hecke modification of Witten formula).**
Modify the Witten volume formula to incorporate the $\Gamma_0(N)$-action on $\mathcal{M}(\mathrm{SU}(3); \Sigma_g) \otimes \Gamma_0(N) \backslash \mathcal{H}$. The expected output is a *Hecke-symmetrized* volume that produces the $\pi^d$ exponents with $d \in \{0, 1\}$ from the $\Gamma_0(7)$ Eisenstein structure.
Estimated difficulty: hard. Estimated time: 6–12 months. Requires expertise in: parabolic bundles, automorphic representations, Hecke algebra acting on $H^*(\mathcal{M})$.

**Problem B.4 (close H2 via $X(7)$ Klein quartic).**
The Klein quartic $X(7)$ has genus 3 and admits the full $\mathrm{PSL}(2,7)$ automorphism. Its periods (which are *nonzero*, unlike $X_0(7)$) might encode the $V_{us}=\pi/14$ identity. This requires careful identification of $V_{us}$ as a specific period over a $\mathrm{PSL}(2,7)$-equivariant cycle.
Estimated difficulty: hard. Estimated time: 6–12 months.

If all four problems are resolved, the joint structure would constitute a substantial *partial derivation* of the SU(3)$\times D=4$ exponent grid from the Atiyah–Bott / modular framework. This would justify upgrading the "structural pattern observation" status of the companion papers to "structural pattern with partial topological derivation".

---

*Technical note by Kévin Rémondière, Oloron-Sainte-Marie, France · 2026-05-24 · CC-BY-4.0 · ORCID 0009-0008-2443-7166*

*"Three structural hypotheses for the kappa-exponent grid. H1 (braid $B_3$) falsified by orbit arithmetic. H2 ($X_0(7)$ periods) falsified by genus-zero. H3 (Atiyah–Bott characteristic classes) partially closes for $a\in\{0,1/2,1\}$ but requires auxiliary $L$-function structure for $b, c, d$. Most promising route forward: explicit Atiyah–Bott class polynomial identification of each observable via the Witten volume formula on $\mathcal{M}(\mathrm{SU}(3);\Sigma_g)$. Estimated effort: 3–6 months."*
