# v8 Math Survey: Condensed Mathematics & Cohesive ∞-Topoi as Foundations for ECI

**Date:** 2026-04-22
**Author:** K. Remondière (research map, internal)
**Scope:** Honest assessment of whether Scholze–Clausen condensed mathematics and/or Sati–Schreiber cohesive ∞-topoi provide a **native** foundation for the four ingredients of the v6 ECI inequality:
(i) type-II crossed-product algebra $\mathcal{A}_R$ (CLPW 2023);
(ii) modular flow $\sigma^R_\tau$ (Connes–Tomita–Takesaki);
(iii) $k$-design complexity $C_k$ (Ma–Huang 2024, Brown–Susskind 2018);
(iv) persistent-homology activator $\Theta(PH_k[\delta n])$ (Yip et al. 2024).

**Verdict taxonomy:** HOOK-RIGOROUS (published theorem directly applies) · HOOK-PROGRAMMATIC (research-programme goal, not theorem) · ANALOGY (surface parallel, no theorem) · NONE.

All citations below were verified via WebSearch against arXiv / journal landing pages on 2026-04-22.

---

## 1. Condensed mathematics (Scholze–Clausen)

### 1.1 Key verified references

- **Scholze, *Lectures on Condensed Mathematics*** (Bonn notes, 2019/2022). URL: https://www.math.uni-bonn.de/people/scholze/Condensed.pdf — foundational condensed/solid abelian groups.
- **Clausen–Scholze, *Lectures on Analytic Geometry*** (Bonn 2020; notes at https://www.math.uni-bonn.de/people/scholze/Analytic.pdf) — liquid vector spaces, functional analysis.
- **Clausen–Scholze, *Condensed Mathematics and Complex Geometry*** (Bonn–Copenhagen summer 2022): https://people.mpim-bonn.mpg.de/scholze/Complex.pdf — liquid quasi-coherent sheaves, Serre duality via condensed.
- **Liquid Tensor Experiment** (Commelin et al., completed 2022-07-14): https://leanprover-community.github.io/blog/posts/lte-final/ — Lean4 formalisation of Theorem 9.4 of the Analytic Geometry notes.
- **Clausen–Scholze, *Analytic Stacks*** (2023–2024 lecture series; notes compiled at https://people.mpim-bonn.mpg.de/scholze/AnalyticStacks.html).
- **Rodríguez Camargo, *Notes on Solid Geometry*** (arXiv 2603.03012, 2024) — solid-geometric reformulation.

### 1.2 Ingredient-by-ingredient verdict

| Ingredient | Native in condensed? | Verdict |
|---|---|---|
| (i) type-II crossed product $\mathcal{A}_R$ | Condensed handles **p-adic / complex analytic** functional analysis via liquid modules. Liquid $\ell^1$-type vector spaces give a good abelian category of "topological vector spaces". There is **no published extension to von Neumann algebras of type II$_1$ / II$_\infty$** nor to C*-algebras. Web-search yielded no Chirvasitu–Clausen or Clausen–operator-algebra crossover. | **ANALOGY** — liquid modules "look like" a better category for completions, but modular theory, faithful normal semifinite traces, and the crossed-product construction (Takesaki duality) have no condensed formulation as of 2026-04. |
| (ii) modular flow $\sigma^R_\tau$ | Tomita–Takesaki requires a faithful normal state on a vN algebra. Condensed has no built-in notion of state / KMS condition. | **NONE** (not even analogy: condensed is $\infty$-abelian; modular flow is $*$-algebraic and state-dependent). |
| (iii) $k$-design $C_k$ | Pseudorandom unitaries (Ma–Huang, arXiv:2410.10116) live on finite-dim Hilbert spaces. Condensed is not required. | **NONE**. |
| (iv) $\Theta(PH_k)$ persistent homology | Persistent homology has well-developed sheaf / microlocal foundations (Kashiwara–Schapira, arXiv:1705.00955; Curry; Brown–Bobrowski). These are *1-categorical* sheaf theory on ordered real lines, not condensed. Solid/liquid structure adds nothing. | **ANALOGY** at best. |

### 1.3 Overall condensed verdict

**NONE of our four ingredients is NATIVELY hosted by condensed mathematics as of 2026-04.** The framework solves problems in *homological algebra of topological abelian groups* and *analytic geometry*. Our problem is *$*$-algebraic / state-dependent / combinatorial-topological*. There is no HOOK-RIGOROUS and no HOOK-PROGRAMMATIC: I found no preprint or lecture where Scholze, Clausen, or a follower claims vN-algebraic modular theory as a target for condensed methods.

---

## 2. Cohesive ∞-topoi & Hypothesis H (Schreiber; Sati–Schreiber)

### 2.1 Key verified references

- **Schreiber, *Differential cohomology in a cohesive ∞-topos*** (arXiv:1310.7930, v2 2013) — foundations of cohesive ∞-topoi for differential / gauge geometry.
- **Schreiber, *Quantum gauge field theory in cohesive homotopy type theory*** (arXiv:1408.0054, EPTCS 2014).
- **Fiorenza–Sati–Schreiber, *Twisted Cohomotopy implies twisted String structure on M5-branes*** (arXiv:2002.11093, J. Math. Phys. 62, 042301 (2021)) — **Hypothesis H** statement (C-field charge-quantised in twisted Cohomotopy).
- **Sati–Schreiber, *Flux Quantization*** (lecture notes 2024-02 / 2024-03, https://ncatlab.org/schreiber/files/FluxQuantization-240302.pdf).
- **Sati–Schreiber, *Topological QBits in Flux-Quantized Super-Gravity*** (arXiv:2411.00628, Nov 2024) — anyonic qubits on M5-probes.
- **Sati–Schreiber, *Quantum Observables of Quantized Fluxes*** (Ann. Henri Poincaré 2024, https://link.springer.com/article/10.1007/s00023-024-01517-z).
- **Sati–Schreiber, *Engineering of Anyons on M5-Probes via Flux Quantization*** (arXiv:2501.17927, 2025).

### 2.2 Ingredient-by-ingredient verdict

| Ingredient | Native in cohesive ∞-topos / Hypothesis H? | Verdict |
|---|---|---|
| (i) type-II crossed product $\mathcal{A}_R$ | Cohesive ∞-topoi encode *smooth / differential / étale* structure on higher stacks. Sati–Schreiber's "quantum observables of quantized fluxes" constructs observable algebras from flux moduli, but these are **topological / higher-gauge** algebras, not type-II vN factors. No theorem connects flux-quantised observables to the crossed product of an AQFT local net by modular flow. | **ANALOGY** — both frameworks produce "observer / subregion" algebras, but the Haag–Kastler→CLPW→type-II construction is not derived from cohesion. |
| (ii) modular flow $\sigma^R_\tau$ | Cohesion has $\int \dashv \flat \dashv \sharp$ adjoint triple and differential-cohomology hexagon, but no state / KMS / modular automorphism construction. Schreiber's programme addresses *kinematics* of gauge fields, not *thermal* dynamics of vN algebras. Web-search returned no Schreiber-authored piece on Tomita–Takesaki. | **NONE**. |
| (iii) $k$-design $C_k$ | Sati–Schreiber topological-qubit programme (arXiv:2411.00628, 2501.17927) constructs **anyonic quantum gates** on M5-brane probes. This gives a *higher-geometric* gate set, not a Haar-random or $k$-design unitary ensemble. $k$-design complexity is a *statistical* quantity over ensembles; cohesive framework produces *deterministic* topological gates. | **ANALOGY** (both yield "quantum complexity on stringy backgrounds") — no theorem linking Ma–Huang PRU complexity to flux-quantised gate complexity. |
| (iv) $\Theta(PH_k)$ persistent homology | Cohesive ∞-topoi contain *shape* functor $\int$ (fundamental ∞-groupoid). Persistent homology is a shape-like invariant filtered by a poset. This is a genuine structural parallel (shape ↔ persistence), but no Sati–Schreiber paper formalises PH of a cosmological density field as a cohesive shape. | **ANALOGY** (suggestive; Schreiber has written informally on shape/persistence parallels on nLab, but no theorem). |

### 2.3 Overall cohesive verdict

**HOOK-PROGRAMMATIC at best, for ingredients (i) and (iii).** Sati–Schreiber programmatically claim that *all* physics observables should arise from flux-quantised higher-stacky constructions; type-II observer algebras would, in principle, be a target. But as of 2026-04 no published theorem derives CLPW-type II$_1$ from a cohesive construction, and no paper connects Ma–Huang PRU complexity to topological-qbit gate depth. The strongest concrete bridge is the *shape* / persistence parallel (iv), but it remains ANALOGY.

---

## 3. Cross-cutting: other rigorous foundations relevant to our ingredients

Found during the survey (not the requested frameworks but worth noting for v7/v8):

- **Algebraic QFT / Haag–Kastler nets** (verified active: Brunetti–Fredenhagen–Rejzner review arXiv:2305.12923, 2023; arXiv:2511.09360, 2025) — **this is the native home** of (i) and (ii). CLPW lives inside AQFT, not inside condensed or cohesive.
- **Microlocal sheaf theory for persistent homology** (Kashiwara–Schapira, arXiv:1705.00955) — HOOK-RIGOROUS for ingredient (iv) if one ever needs a derived-category foundation for $\Theta(PH_k)$. Not condensed/cohesive.
- **Random-matrix / unitary-design theory** (Ma–Huang arXiv:2410.10116) — HOOK-RIGOROUS for (iii), ambient Hilbert-space setting. No higher-geometric scaffold needed.

---

## 4. Negative result (as required by the honesty gate)

**There is no HOOK-RIGOROUS connection between any of the four v6 ingredients and either condensed mathematics or Sati–Schreiber cohesive ∞-topoi as of 2026-04-22.** The closest hits are:

- Cohesive/Hypothesis-H as HOOK-PROGRAMMATIC umbrella for (i) and (iii) — but the programme has not produced the required theorems.
- Microlocal sheaves as HOOK-RIGOROUS for (iv), but this is a *separate* framework (Kashiwara–Schapira), not condensed or cohesive.
- Everything else is ANALOGY.

A v7/v8 paper that *claimed* unification of ECI with condensed math or Hypothesis H would be overreach and would fail PRINCIPLES honesty-gate.

---

## 5. What we can actually use for v7/v8 (≈ 100 words)

Do **not** rewrite v6 ingredients in condensed / cohesive language; there is no theorem to anchor such a rewrite and no programme currently pursuing CLPW-type-II from cohesion. The productive moves for v7/v8 are: **(a)** stay inside AQFT / Haag–Kastler for ingredients (i)–(ii), which is the native foundation and already rigorous (CLPW, Chandrasekaran–Longo–Penington–Witten arXiv:2206.10780); **(b)** adopt Kashiwara–Schapira microlocal-sheaf formalism (arXiv:1705.00955) as the rigorous derived-category home for the persistent-homology activator, replacing the ad-hoc $\Theta$-map with a sheaf-theoretic convolution distance; **(c)** reference Sati–Schreiber Hypothesis H only as a far-future umbrella in a "speculative outlook" paragraph, clearly marked programmatic.

---

## Sources (verified 2026-04-22)

- Scholze, *Lectures on Condensed Mathematics*: https://www.math.uni-bonn.de/people/scholze/Condensed.pdf
- Clausen–Scholze, *Analytic Geometry*: https://www.math.uni-bonn.de/people/scholze/Analytic.pdf
- Clausen–Scholze, *Complex Geometry via Condensed*: https://people.mpim-bonn.mpg.de/scholze/Complex.pdf
- Clausen–Scholze, *Analytic Stacks*: https://people.mpim-bonn.mpg.de/scholze/AnalyticStacks.html
- Liquid Tensor Experiment final report: https://leanprover-community.github.io/blog/posts/lte-final/
- Rodríguez Camargo, *Notes on Solid Geometry*: https://arxiv.org/pdf/2603.03012
- Schreiber, *Differential cohomology in a cohesive ∞-topos*: https://arxiv.org/abs/1310.7930
- Schreiber, *Quantum gauge field theory in cohesive HoTT*: https://arxiv.org/abs/1408.0054
- Fiorenza–Sati–Schreiber, Hypothesis H paper: https://arxiv.org/abs/2002.11093
- Sati–Schreiber, *Topological QBits in Flux-Quantized Super-Gravity*: https://arxiv.org/abs/2411.00628
- Sati–Schreiber, *Engineering of Anyons on M5-Probes*: https://arxiv.org/abs/2501.17927
- Sati–Schreiber, *Quantum Observables of Quantized Fluxes*: https://link.springer.com/article/10.1007/s00023-024-01517-z
- CLPW / Witten et al., *Algebra of Observables for de Sitter Space*: https://arxiv.org/abs/2206.10780
- Chen–Penington–Witten-style, *Crossed product algebras and generalized entropy for subregions*: https://arxiv.org/abs/2306.07323
- Ma–Huang, *How to Construct Random Unitaries*: https://arxiv.org/abs/2410.10116
- Yip–Biagetti–Cole–Viswanathan–Shiu, *Cosmology with Persistent Homology: A Fisher Forecast*: https://arxiv.org/abs/2403.13985
- Kashiwara–Schapira, *Persistent homology and microlocal sheaf theory*: https://arxiv.org/abs/1705.00955
- Brunetti–Fredenhagen–Rejzner, *AQFT: objectives, methods, results*: https://arxiv.org/abs/2305.12923
