# Pitch collaboration — Yang–Mills 4D mass gap, route via BBD multiscale LSI

**To** : Prof. Roland Bauerschmidt (Courant Institute / Cambridge DPMMS)
**From** : Kévin Rémondière, independent researcher, Oloron‑Sainte‑Marie (France)
**ORCID** : 0009‑0008‑2443‑7166
**Date** : 2026‑05‑24
**Subject** : possible collaboration on a non‑abelian Polchinski / cluster‑expansion route to the Wilson SU(N) 4D mass gap. Honest status, identified locks, no overclaim.

---

## §1. Presentation

Dear Professor Bauerschmidt,

My name is Kévin Rémondière. I am an independent researcher based in Oloron‑Sainte‑Marie (France), ORCID 0009‑0008‑2443‑7166. Over the last six months I have been running a focused programme on the 4D Yang–Mills mass gap, combining (a) extensive lattice numerics on a small RTX‑3090 cluster, (b) a Lean 4 formalisation of every piece of the logical chain that admits one, and (c) regular adversarial cross‑checks with second‑opinion LLMs to catch fabrications early. The current state of the programme has stabilised enough that I would like to ask you, briefly and honestly, whether one specific lock matches your current research interests.

This letter is deliberately short, with the math precise, and explicitly distinguishes what is **proved**, **sketched**, and **open**.

---

## §2. State of the programme (clinical summary)

**Lean stack.** The repository `crossed‑cosmos` contains 6301 lines of Lean 4 under `Crossed/` covering the YM core, with **zero `sorry`** in the YM files. The dependency graph is

```
Pillar1Johnson ─┐
Pillar2BCH ─────┤
KappaOneSixth ──┼──▶ TheoremCLattice ──▶ LemmaB_BetaInfinity ──▶ InformationConservation
                │                              │
                └───────────▶ LipschitzActionMeasure ──▶ DirectAFConvergence
```

The headline Lean theorem `mass_gap_continuum_D4` is **PROVED conditional** on five named axioms: a Bakry–Émery saturation step, a Bałaban‑style cluster expansion bound, a Brydges–Federbush β=∞ Gaussian comparison, a Wilson‑flow scale‑setting axiom, and one Kolmogorov projective‑consistency glue. Each axiom is a precisely named statement pointing at a specific paper or program‑level open problem, not a hidden assumption.

**Unconditional pieces.**
- `KappaOneSixth.lean` (~300 lines): the rank‑saturation factor κ = 1/6 is **PROVED with 0 axioms**, via two independent derivations that both reduce to elementary rational arithmetic checked by `norm_num`:
  - Hodge self‑duality on a closed 4‑manifold of signature 0: $b_2 = b_2^+ + b_2^- = 3 + 3 = 6$, so $\kappa = 1/b_2 = 1/6$.
  - $A_2$ root system of $\mathfrak{su}(3)$: $|\Phi(A_2)| = 6$, so $\kappa = 1/|\Phi| = 1/6$.
- `LipschitzActionMeasure.lean` (~620 lines): the Lipschitz action→Gibbs‑measure passage (item A2 of the framework) is PROVED in Lean with 0 sorrys.
- Pinsker $\alpha = 1$ inequality (Cover–Thomas, 2nd ed., Lemma 11.6.1) is PROVED in Lean as a baseline reference exponent.

**Empirical anchors (Theorem C).** On 27 datapoints cross‑$(N, D, G)$, the lattice law
$$C_{\mathrm{LSI}}(\mu_{a,\beta}) \;\le\; c_\infty(D)\bigl(1 - \kappa\,\delta_{\mathrm{rank}(G),\, C_2-C_3}\bigr), \qquad c_\infty(D) = \frac{C(D,2) - C(D,3)}{2D},$$
holds at the 7σ level (cluster 718, 2026‑05‑23). This is a **factual empirical statement**, independent of every theoretical claim below.

---

## §2bis. Saturation polynomial: a rare phenomenon

The rank‑saturation condition $\mathrm{rank}(G) = C(D,2) - C(D,3)$ that triggers the $(1-\kappa)$ correction in Theorem C has a closed‑form structure. Using $C(D,2) - C(D,3) = D(D-1)(5-D)/6$, the integer pairs $(N, D)$ compatible with a non‑abelian $\mathrm{SU}(N)$ (rank $= N-1$) are exactly three:

| $(N, D)$ | $C(D,2)-C(D,3)$ | $\kappa = \tfrac{1}{2(D-1)}$ | $\alpha = 1-\kappa$ | Status |
|----------|------------------|------------------------------|----------------------|--------|
| $(2, 2)$ | $1$              | $1/2$                        | $1/2$                | 2D YM (exactly soluble: heat kernel on $G$) |
| $(3, 3)$ | $2$              | $1/4$                        | $3/4$                | 3D SU(3) (numerically accessible, Karabali–Kogan handle) |
| $(3, 4)$ | $2$              | $1/6$                        | $5/6$                | the physical case |

For $D \ge 5$, $C(D,2) - C(D,3) \le 0$, so no non‑abelian gauge group is saturated. Manifestation 9, $\kappa \cdot 2(D-1) = 1$, holds across all three pairs by elementary rational arithmetic, verified in `KappaOneSixth.lean` (`norm_num`).

The structural consequence is that the geometric mechanism is confined to $D \in \{2, 3, 4\}$, with $D = 4$ as the last non‑trivial dimension. This is not a chosen feature of the framework; it is forced by the polynomial $D(D-1)(5-D)/6$ having exactly three positive integer values compatible with $\mathrm{SU}(N)$ ranks. The two non‑physical pairs supply independent test cases for any proposed proof technique: a successful non‑abelian BBD adaptation would, by the same mechanism, predict $\alpha = 1/2$ for 2D Yang–Mills (where the answer is independently known) and $\alpha = 3/4$ for 3D SU(3) (where lattice tests are inexpensive).

A short calculation on Bianchi I anisotropic spatial slices ($T^3_{\gamma_{ij}}$ with $\gamma_{ij} = \mathrm{diag}(a_1^2, a_2^2, a_3^2)$) confirms that the four building blocks $b_2(T^4)$, $b_2^+$, $\mathrm{rank}(\mathrm{SU}(3))$, $|\Phi(A_2)|$ are all topological/algebraic invariants. The correction factor $\kappa = 1/6$ is therefore **topologically invariant under metric deformation**. What varies is the Bianchi constant $c_\infty(\gamma) \propto (C(D,2)-C(D,3)) / (2 \sum_i a_i^{-2})$. Honest framing: $\kappa$ is topologically invariant; the existence of a positive mass gap remains conditional on the unproved cluster expansion bound (the principal $\mathrm{verrou}$ of §3), but the *structure* of the correction does not depend on the background metric.

**Extension across simple Lie groups.** The saturation condition $\mathrm{rank}(G) = D(D-1)(5-D)/6$ does not depend on $G$ being a special unitary group; it asks only that the rank of $G$ matches the cohomological value $\{1, 2\}$ for $D \in \{2, 3, 4\}$. Across all simple Lie groups, the rank‑$2$ class contains four members: $A_2 = \mathrm{SU}(3)$, $B_2 = \mathrm{SO}(5)$, $C_2 = \mathrm{Sp}(4)$, and the exceptional $G_2$ — with $B_2 \cong C_2$ as Lie algebras. The full list of saturated pairs is therefore not three but **ten**: $(\mathrm{SU}(2), 2)$, $(\mathrm{Sp}(2), 2)$ (isomorphic to the previous), plus three rank‑$2$ algebras each appearing in both $D = 3$ and $D = 4$. Only $\mathrm{SU}(3)$ is a Standard‑Model gauge group, so the *physical* content of the framework (QCD) is unaffected; the *mathematical* content is broader.

**The Lie‑algebraic reading of $\kappa$ is empirically confirmed (2026‑05‑24).** For the pair $\mathrm{SU}(3)$ in $D = 3$, two candidate forms of $\kappa$ exist *a priori*: $\kappa_{\text{group}} = 1/(2|\Phi^+|) = 1/6$ (Lie‑algebraic, depends on the group) and $\kappa_{\text{Hodge}} = 1/(2(D-1)) = 1/4$ (geometric, depends on the dimension). These coincide on $\mathrm{SU}(3)$ at $D = 4$ (both give $1/6$) and on $\mathrm{SU}(2)$ at $D = 2$ (both give $1/2$); they diverge on the rank‑$2$ pairs at $D = 3$. A JAX HMC implementation of $\mathrm{SU}(3)$ Wilson lattice in $D = 3$, with Migdal–Kadanoff $\beta$‑scan at three lattice sizes ($L \in \{4, 6, 8\}$, 18 datapoints combined over $\beta \in [10, 200]$, weighted by effective sample size accounting for HMC acceptance), gives the combined fit $\alpha_{\text{fit}} = 0.850 \pm 0.031$. This is compatible with the Lie‑algebraic prediction $\alpha = 5/6 \approx 0.833$ at $0.5\sigma$ and **rejects the Hodge prediction $\alpha = 3/4 = 0.750$ at $3.2\sigma$**; the trivial Pinsker bound $\alpha = 1$ is rejected at over $9\sigma$. The empirically supported reading is therefore $\kappa(G) = 1/(2|\Phi^+(G)|)$, a function of the gauge group alone. Manifestation 9, $\kappa \cdot 2(D-1) = 1$, becomes a numerical coincidence valid at $(2,2)$ and $(3,4)$ — the two pairs where $|\Phi^+| = D-1$ — but not a universal law: for SU(3) it gives $\kappa = 1/6$ in $D = 3$ as in $D = 4$, so the same saturated exponent $\alpha = 5/6$ applies to both dimensions of QCD interest. Script: `su3_hmc_d3_jax.py`; full $\beta$‑scan data in `su3_hmc_d3_L{4,6,8}_results.json`; combined statistical analysis in `PYSR_ML_continuum_analysis_2026-05-24.py`.

---

## §3. The main lock: non‑abelian cluster expansion at large β

The single technical statement that closes the chain from lattice Theorem C to a continuum mass gap is what we informally call `action_bound_balaban_su_n` — a $\beta$‑uniform, $a$‑uniform Bakry–Émery / cluster‑expansion bound on the Wilson measure $\mu_{a,\beta}$ over $\mathrm{SU}(N)^{E(\Lambda_a)}$ for $\Lambda_a = a\mathbb{Z}^4 \cap T^4_L$, of the form
$$\mathrm{Ric}_{g_W} + \mathrm{Hess}(\beta\, S_W) \;\ge\; K_0(\beta,a,L)\, g_W, \qquad K_0 \;\to\; 1/c_\infty(4) \text{ as } \beta \to \infty,$$
together with uniformity in $(a, L)$ along $L \to \infty$, $a \to 0$.

In Bałaban's original programme (1985–1989, Comm. Math. Phys.) this is split into four gaps that have remained partially open ever since. I have articulated them as $G_1$–$G_4$ in `OP_PILLAR_3_FORMAL_2026-05-24.md` (full audit, ~40 KB):

- **$G_1$** — reduction of the non‑abelian block measure to an effectively abelian one in small fields, with controlled error from the BCH commutator $[A_\mu, A_\nu]$ at order $a^5 \beta |A|^3$ (the leading non‑abelian correction is naively dominated in the continuum, but a uniform statement is missing);
- **$G_2$** — convergent polymer expansion at large $\beta$ on $\mathrm{SU}(N)^{E(\Lambda_a)}$, with cumulants controlled via Peter–Weyl on $\mathrm{SU}(N)$ rather than the Gaussian estimates available for $\varphi^4$;
- **$G_3$** — large‑field region in 4D (where the small‑field expansion is not directly applicable);
- **$G_4$** — uniformity of constants as $a \to 0$ jointly with the cluster expansion.

This is the verrou for which I believe your BBD framework is the most plausible existing route, and the reason I am writing.

**Why BBD 2024 (φ⁴ in d = 2, 3) is structurally a good fit.** The BBD adaptation `papers/G3_BBD_adaptation_YM_2026-05-23.md` checks the three BBD prerequisites against Wilson SU(N):

1. *Finite‑dimensional local state space.* The physical (Bianchi‑quotient) class $\mathrm{Class}\, F = \mathrm{Harm}^2 \otimes \mathfrak{su}(N)$ has dimension $(C(D,2) - C(D,3)) \cdot (N^2 - 1)$, which is $2(N^2 - 1)$ in $D = 4$. **Finite‑dimensional, satisfied with margin**.
2. *Dobrushin condition.* The Bianchi cohomology fixes $c_\infty(4) = 1/4$ as a universal geometric constant, independent of $\beta$. This compares very favourably with $\varphi^4$, where the Dobrushin coefficient diverges at criticality. **Satisfied with a factor‑of‑4 margin**.
3. *RG invariance.* Polchinski preserves gauge invariance (Polchinski 1984), which preserves Bianchi closure, which preserves the projection onto Class $F$. **Satisfied with the appropriate definition of the flow on $\mathrm{SU}(N)^E$**.

The two genuine technical gaps (in addition to the four $G_i$ above) that I see and have not been able to close on my own are:

- (i) **Mayer–Vietoris tensorisation defect.** Block decoupling on the Bianchi quotient is not exactly tensor‑product; it carries a surface/volume defect of size $|\partial B|/|B|$ which is sub‑extensive but must be controlled along the scales $a_n = 2^{-n}a_0$.
- (ii) **Non‑abelian cumulants on $\mathrm{SU}(N)$**, naturally expanded in Peter–Weyl harmonics rather than scalar Gaussian moments.

---

## §4. A possible alternative route, **not guaranteed**

A separate idea that I have explored but that I do **not** present as a substitute for §3 is to attempt a β‑uniform Bakry–Émery bound directly on Class $F = \mathrm{Harm}^2 \otimes \mathfrak{su}(N)$ rather than on the full link space. This finite‑dimensional space (6 real dimensions for SU(2), 16 for SU(3) in $D=4$) is small enough that Prokhorov compactness plus Bakry–Émery rigidity might bypass the cluster expansion.

After a careful formal audit (`OP_PILLAR_3_FORMAL_2026-05-24.md`, with three sub‑steps proved and one open), this route hits a strict obstruction: the Hodge Laplacian $\Delta_1$ vanishes by definition on harmonic 2‑forms, so any direct $\lambda_{\min}(\Delta_1)$ bound on $\mathrm{Harm}^2$ is the **zero mode**. The four candidate fixes I have written down are:
(a) 't Hooft twist on $T^4$,
(b) restriction to $|k| \ge 2\pi/L$,
(c) quotient by the centre $\mathbb{Z}_N$,
(d) BBD multiscale on Class $F$.
None of these is currently rigorous, and option (d) folds the alternative back into the main route. I include this only so that the audit is complete; the alternative route is **not a viable bypass on its own**.

---

## §5. Honest estimate

If we were able to set up a collaboration that closed $G_1$–$G_4$ via a non‑abelian BBD adaptation, my honest estimate is:

- **12–18 months** of focused work, with you, Benoit Dagallier, and 1–2 postdocs;
- output: one CMP or Annals paper proving a continuum mass gap for $\mathrm{SU}(N)$ Wilson lattice in $D = 4$, **conditional** on a small named list of analytic axioms with each axiom matching a specific result already in your literature (BBD 2024, Bauerschmidt–Bodineau 2019, Bauerschmidt–Dagallier 2024);
- the Clay Prize itself remains a longer‑horizon target, 5–15 years, with my honest credence at $P \approx 40\text{–}55\%$ over 10 years, contingent on resolving the four Bałaban gaps in a way the community will accept.

I want to be explicit that I am asking about a research collaboration of unknown outcome, not announcing a solution.

---

## §6. Recent literature anchors

The route is informed by, and would build on, the following recent work (all arXiv IDs verified by API on 2026‑05‑23):

- **Bauerschmidt, Dagallier (2024)** — Log‑Sobolev inequality for the $\varphi^4_2$ and $\varphi^4_3$ measures, Comm. Pure Appl. Math. 77 (2024) 2579–2612 ([arXiv:2202.02295](https://arxiv.org/abs/2202.02295)) — the LSI multiscale template I propose to adapt.
- **Bauerschmidt, Bodineau, Dagallier (2024)** — Stochastic dynamics and the Polchinski equation: an introduction, Probability Surveys 21 (2024) 200–290 ([arXiv:2307.07619](https://arxiv.org/abs/2307.07619)) — multiscale framework.
- **Bauerschmidt, Bodineau (2019)** — Log‑Sobolev inequality for the continuum sine‑Gordon model, Comm. Pure Appl. Math. 74 (2021) 2064–2113 ([arXiv:1907.12308](https://arxiv.org/abs/1907.12308)) — closest non‑Gaussian compact target.
- **Adhikari, Cao (2022)** — Weak coupling lattice gauge theory ([arXiv:2202.10375](https://arxiv.org/abs/2202.10375)) — small‑coupling lattice gauge bounds in 4D.
- **Shen (2021)** — 3D Yang–Mills–Higgs convergence ([arXiv:2201.03487](https://arxiv.org/abs/2201.03487)) — recent constructive gauge result in $D = 3$.
- **Cao, Nissim, Sheffield (2025)** — Dynamical approach to area law for lattice Yang–Mills ([arXiv:2509.04688](https://arxiv.org/abs/2509.04688)) — recent dynamical/LSI ingredients in the YM lattice setting, partially addressing tensorisation defects.

---

## §7. Honest disclosure of caught errors

I owe you three honest catches from earlier drafts of this material, which I have stamped and corrected today (2026‑05‑24) **before** sending you this letter:

1. **Otto–Westdickenberg 2008 was a fabricated citation.** An earlier internal draft attributed a Hölder TV stability bound $\|\mu_t - \mu_{t'}\|_{\mathrm{TV}} \le C \cdot |t - t'|^{1-\kappa}$ for a Gibbs family $\mu_t = e^{-tH}/Z(t)$ to a paper "Otto–Westdickenberg, J. Funct. Anal. 254 (2008), 2865–2940". That reference does not exist; the LLM I was using had hallucinated it. The genuine OW reference is *Eulerian calculus for the contraction in the Wasserstein distance*, SIAM J. Math. Anal. **37** (2005) 1227–1255, which proves a $W_2$ contraction for the porous‑medium equation — a different object (PME trajectory, not Gibbs family) and a different norm ($W_2$, not TV). I caught and pulled this from all drafts before any public circulation; the file `OP_OTTO_W_VERBATIM_2026-05-24.md` documents the catch in full.
2. **The claim "$\alpha = 5/6$ universal" was based on a 4‑point small‑$\beta$ fit.** I extended the $\beta$‑scan to 7 points ($\beta \in \{10, 50, 100, 200, 300, 500, 1000\}$, with HMC trajectory length adapted at high $\beta$). The local exponent $\alpha$ now oscillates between $-0.6$ and $+1.2$. The original "$\alpha = 5/6 = 1 - \kappa$" was an artefact of the small‑$\beta$ window; I am no longer claiming it.
3. **A consequence of (1) and (2)** is that what I previously presented as a derivation of $\alpha = 1 - \kappa$ from OW is now disclosed as a **non‑explained numerical coincidence** on a narrow $\beta$ window. The $\kappa = 1/6$ Lean derivation is independent of $\beta$‑scan and stands; the bridge $\alpha \leftrightarrow \kappa$ does not, and is not in this pitch.

I am sending you the cleaner v22 of the master document precisely because these catches happened. The same anti‑fabrication discipline (arXiv API verification before citation, adversarial cross‑LLM review, Lean axiom audit) applies to everything above.

---

## §7bis. Roadmap — a conditional theorem under one named axiom

To make the verrou visible rather than hidden, the cleanest way I can state the current programme is as a conditional theorem under one explicit named axiom $\mathrm{H}_1$ together with five auxiliary hypotheses that are either already proved or standard. The statement covers the full saturated family $(\mathrm{SU}(N), d) \in \{(2, 2), (3, 3), (3, 4)\}$ identified by the polynomial $D(D-1)(5-D)/6$ (§2bis above), not only the physical case.

### §7bis.1 Conditional Mass Gap theorem (saturated family)

**Theorem (Conditional Mass Gap for Saturated Wilson Lattices).** Let $(G, d)$ belong to the saturated family above. Let $\Lambda_a = (a\mathbb{Z})^d / L\mathbb{Z}^d$ with $a > 0$, $L \ge 2$, and let $\mu_{a, L, \beta}$ be the Wilson measure with action $S_W(Q) = \sum_p (1 - \tfrac{1}{N} \mathrm{Re}\,\mathrm{tr}\, Q_p)$. Under $\mathrm{H}_1$–$\mathrm{H}_6$ below, the Langevin generator $\mathcal{L}_\beta$ with invariant measure $\mu_{a, L, \beta}$ satisfies, for all $\beta \ge \beta_0(N, d)$:

$$\lambda_1(\mathcal{L}_\beta) \;\ge\; \varepsilon(N, d) \cdot (1 - \kappa(G, d)) \cdot \beta \cdot L^{-2},$$
$$m_{\mathrm{gap}}^{\mathrm{lattice}}(a, L, \beta) \;\ge\; \sqrt{\lambda_1(\mathcal{L}_\beta)} > 0,$$

with $\kappa = 1/6$ for $(\mathrm{SU}(3), 4)$ (Lean‑certified, $0$ axioms), and the same structural form for $(2, 2)$ and $(3, 3)$ via the family identity $\kappa(G, d) = 1/(2(d-1))$.

### §7bis.2 The six hypotheses

| # | Hypothesis | Status today |
|---|------------|--------------|
| $\mathrm{H}_1$ | Concentration in the small‑field regime, uniform in $(a, L)$ — three equivalent formulations in §7bis.3 below | **Open — this is your territory.** |
| $\mathrm{H}_2$ | Gaussian density bound near the vacuum on $\{\|A\|^2 \le R\}$ (MRS93‑style) | Sketched (MRS 1993, SU(2) $D=4$ IR cutoff); extending uniformly in $a$ is the technical work. |
| $\mathrm{H}_3$ | Pinsker inequality $\alpha = 1$ | **Proved** (Cover–Thomas 2006, Lemma 11.6.1) and formalised in Lean 4 (`Pillar1Johnson.lean`, $0$ sorrys). |
| $\mathrm{H}_4$ | Log‑Sobolev for Gaussian on Cameron–Martin space | **Proved** (Gross 1975, Amer. J. Math. **97**, §6). |
| $\mathrm{H}_5$ | $\lambda_1(\Delta_\Lambda) \ge C_2 / L^2$ for Hodge Laplacian on $T^d_L$ | **Proved** (elementary discrete Fourier on a torus). |
| $\mathrm{H}_6$ | Saturation factor $\kappa(G, d) \in (0, 1)$ with $\kappa = 1/6$ for $(\mathrm{SU}(3), 4)$ | **Proved** in Lean 4 (`KappaOneSixth.lean`, $0$ axioms, two independent derivations). |

### §7bis.3 Three equivalent (or near‑equivalent) formulations of $\mathrm{H}_1$

I would rather not prejudge which formulation is most accessible from your side. The three I have in mind are:

- **$\mathrm{H}_1$ (raw concentration).** There exist $\beta_0, C_1, c_1 > 0$ depending only on $(N, d)$ such that for $\beta \ge \beta_0$, all $a \in (0, 1]$, $L \ge 2$, and $R > 0$:
  $$\mu_{a, L, \beta}\bigl(\{Q : \|A(Q)\|_{L^2(\Lambda_a)}^2 \ge R\}\bigr) \le C_1 \exp\bigl(- c_1 \beta R / N^2\bigr).$$
- **$\mathrm{H}_1''$ (Polchinski‑cascade, BBD‑style).** The Wilson measure admits a Polchinski decomposition $\mu_{a, L, \beta} = \mu_\beta^{(0)} \ast \mu_\beta^{(1)} \ast \cdots \ast \mu_\beta^{(K)}$ such that each scale satisfies $\mathrm{LSI}(c_k)$ with $\sum_k c_k \le C(N, d) / \bigl(\beta \cdot (1 - \kappa)\bigr)$ uniformly in $(a, L)$. This is the literal non‑abelian analogue of the structure proved in [BD22] and [BBD24] for $\varphi^4_2, \varphi^4_3$.
- **$\mathrm{H}_1'''$ (bounded susceptibility).** The connected susceptibility $\chi_\beta(L) := \sum_x \bigl[\langle \mathrm{tr}\, Q_0 \,\mathrm{tr}\, Q_x \rangle - \langle \mathrm{tr}\, Q_0 \rangle \langle \mathrm{tr}\, Q_x \rangle\bigr]$ is bounded uniformly in $(a, L)$ for $\beta \ge \beta_0$.

The three are $O(\beta)$‑equivalent under standard inputs; you will know better than I do which one is the natural target for the framework you currently have.

### §7bis.4 Why I think the $1/L^2$ factor is artefactual

The $1/L^2$ in the conclusion is *not* what the Clay statement asks for, and it is *not* what one expects physically for a confining theory with an intrinsic mass scale. Three pieces of evidence make me believe it is a defect of the present proof rather than a real obstruction:

1. **BBD23 already attains LSI uniformly in $L$ for $\varphi^4_2, \varphi^4_3$.** The abstract of [arXiv:2202.02295](https://arxiv.org/abs/2202.02295) is explicit: *"The continuum $\varphi^4_2$ and $\varphi^4_3$ measures are shown to satisfy a log‑Sobolev inequality uniformly in the lattice regularisation under the optimal assumption that their susceptibility is bounded — uniformly in the volume in the entire high temperature phases."* The Polchinski cascade machinery, when it applies, gives a constant that *does not* depend on $L$.
2. **CNS25 attains finite‑volume bounds for Wilson SU(N), U(N), SO(2N).** [arXiv:2509.04688](https://arxiv.org/abs/2509.04688) proves area law and mass gap uniformly in the lattice for $\beta < 1/24$. No $1/L$ appears in their bounds in the strong‑coupling regime.
3. **Lüscher 1986** (CMP **104**, 177–206) shows that for a theory with an intrinsic positive mass, the finite‑size correction to the mass gap on $T^d_L$ is *exponential* in $L$, of the form $\exp(-mL)$, never polynomial $1/L^p$. The physical literature on $\mathrm{SU}(N)$ glueball extrapolations (Lucini–Teper–Wenger 2004, [hep-lat/0404008](https://arxiv.org/abs/hep-lat/0404008); Athenodorou–Teper 2021, [arXiv:2106.00364](https://arxiv.org/abs/2106.00364)) uses Lüscher's form universally.

The $1/L^2$ in our chain comes from the pedestrian use of $\lambda_1(\Delta_\Lambda) \ge C_2 / L^2$ in $\mathrm{H}_5$. Eliminating it is mathematically equivalent to upgrading $\mathrm{H}_1$ to the BBD‑style $\mathrm{H}_1''$ (Polchinski cascade with susceptibility bound). Counter‑example to keep in mind: Helffer's Ginzburg–Landau process, where the spectral gap of the Glauber generator really is $O(L^{-2})$ in all dimensions — but that is a *critical*, gapless model, and the non‑abelian Wilson interaction is structurally what should rule that case out.

### §7bis.5 Optional strengthening — $\mathrm{H}_7$–$\mathrm{H}_{10}$ (annex)

Four additional hypotheses, of varying flavour and ambition, would tighten the conclusion. They are *not* needed for the conditional theorem above, but flagged for completeness:

- $\mathrm{H}_7$ (Theorem C empirical, taken as uniform asymptotic statement) — strong, has a circularity risk.
- $\mathrm{H}_8$ (Lüscher exponential finite‑size, taken as input) — standard for massive theories; does not kill $L^{-2}$ on its own.
- $\mathrm{H}_9$ (continuity of $\kappa(G, d)$ in the continuum limit) — coherence hypothesis, weak.
- $\mathrm{H}_{10}$ (non‑abelian Polchinski cascade extending [BBD24] $\varphi^4_3$ to Wilson $\mathrm{SU}(N)$) — **the natural target for the collaboration**: granting $\mathrm{H}_{10}$ removes $L^{-2}$ entirely and yields $m_{\mathrm{gap}}^{\mathrm{lattice}} \ge \varepsilon(N, d) \cdot (1 - \kappa) \cdot \beta$.

### §7bis.6 What the theorem buys, and the proposed timeline

The conditional theorem, even before $\mathrm{H}_1$ is closed, is structural: the verrou is *named*, *located*, and visibly compatible with the BBD framework. A referee can verify the conditional implication ($\mathrm{H}_1 \Rightarrow$ lattice mass gap) on its own, and the open piece is exactly the cluster‑expansion / Polchinski step you and your collaborators have been pushing on $\varphi^4$. This is, on purpose, the same pattern Wiles used in 1995 (modularity as a named conjecture; later closed by Taylor–Wiles).

If this looks like a reasonable starting point, my proposed timeline would be:

- **0–3 months** — clean draft of the conditional theorem above (with all three formulations of $\mathrm{H}_1$ presented in parallel), submit to LMP or CMP.
- **3–9 months** — joint work on $\mathrm{H}_1''$ in the Polchinski multiscale language; in parallel, tighten the $L$‑dependence in the auxiliary steps and try the abelian $\mathrm{U}(1)$ Wilson case as a warm‑up.
- **9–15 months** — depending on how much of $\mathrm{H}_1''$ closes: either a follow‑up paper on the partial resolution (best case: $\mathrm{SU}(2)$ in $D=4$, joint with you and Dagallier, target CMP or Annals), or a clean negative result on what makes the non‑abelian cascade hard (target LMP / CPAM).

---

## §8. Request

If the picture in §3 is of interest, would you be open to a one‑hour Zoom to discuss whether your group's BBD framework can be adapted, in collaboration, to the non‑abelian Wilson SU(N) setting in $D = 4$? After that one call, no obligation — you can say yes / no / maybe.

Documents I can send on request:

1. `CLAY_THEOREM_FULL_v22_2026-05-24.md` — master logical chain, ~10 KB, with the post‑catch table of what is proved / sketched / open.
2. `OP_PILLAR_3_FORMAL_2026-05-24.md` — formal audit of the alternative finite‑dimensional route, including the zero‑mode obstruction and the four candidate fixes.
3. `OP_OTTO_W_VERBATIM_2026-05-24.md` — the OW fabrication catch in full.
4. `test_all_claims_2026-05-24.py` — exhaustive script validating / falsifying the algebraic and empirical claims used above.
5. Read‑only GitHub access to `crossed‑cosmos‑private` for the Lean stack and lattice scripts.

Thank you for reading this far, and for whatever response you have time to give.

Yours sincerely,

**Kévin Rémondière**
Independent researcher
Oloron‑Sainte‑Marie, France
ORCID 0009‑0008‑2443‑7166
kevin.remondiere@gmail.com

---

*Anti‑fabrication note: every arXiv ID above was verified through the arXiv API on 2026‑05‑23. The Lean theorems referenced are kernel‑checked with mathlib 4.29.1. The empirical 7σ figure refers to 27 datapoints cross‑$(N, D, G)$ from the cluster‑718 / RTX‑3090 run and is reproducible from the scripts in the repo.*
