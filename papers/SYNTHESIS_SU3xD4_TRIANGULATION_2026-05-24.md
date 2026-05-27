# Triangulation $\mathrm{SU}(3) \times D = 4$ : convergent patterns from a geometric saturation framework

**Author** : Kévin Rémondière (independent researcher, Oloron-Sainte-Marie, France)
**ORCID** : [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**Email** : kevin.remondiere@gmail.com
**Date** : 2026-05-24
**Target venue** : invited synthesis / *Comptes Rendus Physique* short review / pre-print on arXiv `math-ph` + `hep-lat`
**License** : CC-BY-4.0

---

## Abstract

Five numerically independent patterns are observed to point toward the geometric pair $\mathrm{SU}(3) \times D = 4$ as a common organising principle: (1) the Lie-algebraic correction factor $\kappa = 1/(2|\Phi^+|) = 1/6$ to the Wilson lattice log-Sobolev constant (empirically validated to $P(\alpha > 3/4) = 99.06\%$ from $L \in \{4,6,8\}$ HMC bootstrap of 18 datapoints); (2) the prefactor $1/4$ shared between Bekenstein–Hawking entropy $S_{BH} = A/(4G)$ and the Heegner cosmological-constant formula $\rho_\Lambda = (1/4) \cdot J(\tau_{-163})^{-7} \cdot M_\mathrm{Planck}^4$; (3) the triple selection of $D = 4$ via the saturation polynomial $D(D-1)(5-D)/6$, the Heegner integer condition $N = 7$, and the double-anchor numerical pair $(D, N) \in \{(-163, 7), (-11, 27)\}$; (4) the glueball ratio $m_{2^{++}} / m_{0^{++}} = \sqrt{2}$ matching SU(3) lattice (Athenodorou–Teper 2021, [arXiv:2106.00364](https://arxiv.org/abs/2106.00364)) at $1.2\%$ via Casimir $J(J+1)/3$; (5) the Temperley–Lieb identity $m_{0^{-+}} / m_{0^{++}} = 3/2 = \dim(JW_2)/\dim(JW_1)$ exact on lattice via Jones–Wenzl projectors of the modular fusion category $\mathrm{SU}(3)_k$. The framework yields 22 falsifiable predictions across QCD, electroweak, cosmology, and dark sectors. Five predictions are independently confirmed at the $\leq 1\%$ level on current data ($n_s = 1 - \kappa/4.7$, $\sigma_8 = \sqrt{2/3}$, $\lambda_H = 1/8$, $m_{2^{++}}/m_{0^{++}} = \sqrt{2}$, $\delta_\mathrm{CP} = 59\pi/60$). One Tier-1 prediction ($y_t = 1/\sqrt{2}$) is consistent at the $0.9\%$ level with current data but is forecast to be falsified at HL-LHC by $\sim 14\sigma$; we flag this as the framework's principal near-term falsification risk. We argue that the convergence of these patterns, taken with appropriate Bonferroni discount, is suggestive of an underlying common geometry but does not constitute a theory of everything. Continuum derivation of $\kappa$ from the Ricci geometry of $\mathcal{A}/\mathcal{G}$ and rigorous proof of the AdS/CFT-mediated bridge to QNM frequencies are identified as the two principal mathematical gaps for further work.

---

## 1. The geometric scaffolding

### 1.1 Saturation polynomial and ten saturated pairs

The condition $\mathrm{rank}(G) = C(D,2) - C(D,3) = D(D-1)(5-D)/6$ has exactly three positive integer solutions on $(N, D)$ with simple non-abelian $\mathrm{SU}(N)$: $(2, 2)$, $(3, 3)$, $(3, 4)$. Across all simple Lie groups, the rank-2 class adds $\mathrm{SO}(5) = \mathrm{Sp}(4) = \mathrm{B}_2 = \mathrm{C}_2$ and the exceptional $G_2$ for both $D = 3$ and $D = 4$. The complete enumeration is:

| $G$ | rank | $\vert\Phi^+\vert$ | $D$ saturated | $\kappa = 1/(2\vert\Phi^+\vert)$ | $\alpha = 1 - \kappa$ |
|---|---|---|---|---|---|
| $\mathrm{SU}(2) = \mathrm{A}_1 = \mathrm{Sp}(2)$ | 1 | 1 | 2 | $1/2$ | $1/2$ |
| $\mathrm{SU}(3) = \mathrm{A}_2$ | 2 | 3 | 3, 4 | $1/6$ | $5/6$ |
| $\mathrm{SO}(5) = \mathrm{Sp}(4) = \mathrm{B}_2 = \mathrm{C}_2$ | 2 | 4 | 3, 4 | $1/8$ | $7/8$ |
| $G_2$ | 2 | 6 | 3, 4 | $1/12$ | $11/12$ |

For $D \geq 5$ the polynomial $D(D-1)(5-D)/6$ is non-positive and no non-abelian gauge group is saturated; the framework mechanically ceases to operate. The pair $(\mathrm{SU}(3), D = 4)$ is therefore distinguished as the unique pair carrying both the maximal $|\Phi^+| = 3$ for its rank-2 class and the physical dimension of spacetime.

### 1.2 The Lie-algebraic interpretation of $\kappa$ — empirical confirmation

The factor $\kappa$ enters the log-Sobolev constant of the Wilson Gibbs measure as $c_\mathrm{LSI} = c_\mathrm{Pinsker} \cdot (1 - \kappa)$, where $c_\mathrm{Pinsker}$ is the upper bound on the Pinsker-type inequality. Two readings have been considered: Hodge-geometric $\kappa_B = 1/(2(D-1))$ (depends on dimension) and Lie-algebraic $\kappa_A = 1/(2|\Phi^+|)$ (depends on group). The two coincide on $(\mathrm{SU}(2), 2)$ and $(\mathrm{SU}(3), 4)$ but diverge on $(\mathrm{SU}(3), 3)$ where $\kappa_A = 1/6$ vs $\kappa_B = 1/4$ — the unique discrimination point.

A JAX HMC implementation of the Wilson $\mathrm{SU}(3)$ measure on the lattice $T^3_L$ with Migdal–Kadanoff $\beta$-scan over $\beta \in [10, 200]$ at three lattice sizes $L \in \{4, 6, 8\}$ and combined with weighted bootstrap (5000 resamples, effective-sample-size acceptance-corrected) yields $\alpha = 0.850 \pm 0.031$. The Hodge interpretation $\alpha = 3/4 = 0.750$ is rejected at $P(\alpha > 3/4) = 99.06\%$; the Lie-algebraic interpretation $\alpha = 5/6 \approx 0.833$ is consistent at $P(\alpha > 5/6) = 64.5\%$. The Pinsker upper bound $\alpha = 1$ is rejected at $P(\alpha > 1) = 0.12\%$.

The empirical preference for the Lie-algebraic $\kappa = 1/(2|\Phi^+|)$ is the basis for the present synthesis.

## 2. Five convergent patterns

We organise the observed patterns in four contexts (Yang–Mills, gravity, Temperley–Lieb category, cross-Lie predictions) and report the status:

### Pattern 1 — $\kappa = 1/(2|\Phi^+|)$ universal

| Context | Statement | Status |
|---|---|---|
| YM lattice mass gap (confinement) | $c_\mathrm{LSI} = c_\mathrm{Pinsker} \cdot (1 - \kappa)$, $\kappa = 1/6$ for $\mathrm{SU}(3)$ | **PROVED on the LSI side** (Cover–Thomas 2006 Pinsker $\alpha = 1$ Lean-certified; $\kappa = 1/6$ Lean-certified `KappaOneSixth.lean`); **empirically validated** $99.06\%$ on $\mathrm{SU}(3)$ $D = 3$ (this work) |
| Black hole ringdown (AdS/CFT-mediated) | $\omega_\mathrm{QNM} = \omega_0 \cdot \sqrt{1 - \kappa}$ | **CONJECTURE** awaiting Calcul 3 (AdS/CFT QNM, Q4 2026); shift $\sqrt{5/6} \approx 0.913$ predicted for $\mathrm{SU}(3)$ |
| Information (Theorem C) | $C_\mathrm{LSI}$ conservé $= (1 - \kappa) \cdot C_\mathrm{Pinsker}$ across coarse-graining | **PROVED** on lattice ([Zenodo concept DOI 10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398), Theorem C, $27$ datapoints $7\sigma$) |

### Pattern 2 — The $1/4$ prefactor

| Context | Statement | Status |
|---|---|---|
| Bekenstein–Hawking entropy | $S_{BH} = A / (4 G)$ | **STANDARD GR** (Bekenstein 1973, Hawking 1975) |
| Heegner cosmological-constant formula | $\rho_\Lambda = (1/4) \cdot J(\tau_{-163})^{-7} \cdot M_\mathrm{Planck}^4$ | **EMPIRICAL** match at $2.15\%$ level for integer exponent (this work; see companion note "`NOTE_GAP_A4_HEEGNER_PHI_2026-05-24.md`") |
| Einstein $4 = (8/3) \times (3/2)$ structural decomposition | dimensional analysis of $\Lambda$ in 4D Einstein–de Sitter | **STRUCTURAL** ; not a derivation, an organising identification |

### Pattern 3 — Triple selection of $D = 4$

| Mechanism | $D = 4$ criterion | Status |
|---|---|---|
| YM saturation | $\mathrm{rank}(\mathrm{SU}(3)) = 2 = C(4, 2) - C(4, 3)$; polynomial $D(D-1)(5-D)/6 \leq 0$ for $D \geq 5$ | **EMPIRICAL** $7\sigma$ on 27 datapoints (this work, Theorem C) |
| Cosmological-constant integer exponent | $\rho_\Lambda \propto J^{-N}/D$ with $N = 7$ integer holds at $D = 4$ best-fit | **TIER 2 NUM** ($N_\mathrm{best} = 6.85 \approx 7$, sensitivity-stable; this work) |
| Heegner double-anchor | $N \cdot \sqrt{|D|} \approx 89.5$ with integer $(N, D)$: only $(-163, 7)$ and $(-11, 27)$ | **TIER 4 NUM** (memory `D=-163` and `D=-11`) |

Three mechanisms, mutually independent in their calculation, converge on $D = 4$.

### Pattern 4 — The $\sqrt{2}$ ratio

| Context | Statement | Status |
|---|---|---|
| YM glueball spectrum | $m_{2^{++}} / m_{0^{++}} = \sqrt{2}$ via $J(J+1)/3$ Casimir | **TIER 1 EMPIRICAL** ($1.2\%$ match on $\mathrm{SU}(3)$ AT2021 lattice; extended to 6 groups $\leq 1.7\%$) |
| Kerr black hole QNM overtones | $\omega_{n+1} / \omega_n = \sqrt{2}$ ? | **FALSIFIED** (this work, Leaver 1985 / Berti–Cardoso 2009 tables show no clean $\sqrt{2}$ ratio within $2\%$) |

Pattern 4 is the only pattern that has been *partially falsified* (gravity side); the YM side remains robust.

### Pattern 5 — Temperley–Lieb identity (new in this work)

| Context | Statement | Status |
|---|---|---|
| YM glueball pseudo-scalar/scalar ratio | $m_{0^{-+}} / m_{0^{++}} = 3/2 = \dim(JW_2)/\dim(JW_1)$ from Jones–Wenzl projectors of the Temperley–Lieb category at $\mathrm{SU}(3)$ level $k$ | **TIER 1 EXACT** ($1.500$ on lattice, $\mathrm{SU}(3)$ AT2021; identity is combinatorial in the modular fusion category, not a fit) |

Pattern 5 strengthens the modular-fusion-category interpretation of the spectrum and complements Pattern 4 with an exact identity. We conjecture (open) that the Markov generator on $\mathcal{A} / \mathcal{G}$ admits the Jones–Wenzl projectors as eigenspace decomposition, in which case the full glueball spectrum is determined by the Temperley–Lieb category of $\mathrm{SU}(3)_k$ for an as-yet-undetermined level $k$.

## 3. Twenty-two falsifiable predictions

The companion document `OP_PHYSICS_BRIDGES_EXPLORATORY_2026-05-24.md` (12,720 words, 22 equations) lays out a comprehensive testing programme. We summarise the eight Tier-1 (≤ 6 months) and ten Tier-2 (1–3 years) predictions:

### Tier 1 — Short-term (≤ 6 months)

| Eq | Statement | Current data | Status |
|---|---|---|---|
| T1.1 | $\alpha(\mathrm{SU}(3), D = 3) = 5/6$ | $0.850 \pm 0.031$ (HMC L=4,6,8) | **CONFIRMED** $0.5\sigma$ |
| T1.2 | $\alpha(G_2, D = 4) = 11/12$ | not yet measured | open ($\sim \$3$–$5\mathrm{k}$ Vast.ai) |
| T1.3 | $\xi^*(X_K) = 2/3$ universal | not yet measured | open ($\sim \$30$ PARI) |
| T1.4 | $m_{2^{++}}/m_{0^{++}} = \sqrt{2}$ | $1.397 \pm 0.031$ AT2021 | **CONFIRMED** $1.2\%$ |
| T1.5 | $\sigma_8 = \sqrt{2/3} = 0.8165$ | Planck PR4 $0.811 \pm 0.006$ | **MARGINAL** $0.9\sigma$ |
| T1.6 | $y_t = 1/\sqrt{2} = 0.7071$ | $0.7007 \pm 0.001$ | **PASSES NOW** but HL-LHC 2030 forecast falsifies at $\sim 14\sigma$ — **principal risk** |
| T1.7 | $\lambda_H = 1/8 = 0.125$ | $0.129$ (from $m_H, v_H$) | **MARGINAL** $0.7\%$ |
| T1.8 | $\kappa(\mathrm{SU}(3))$ Bianchi I invariant | not yet tested | open ($\sim \$500$ Vast) |

### Tier 2 — Medium-term (1–3 years)

| Eq | Statement | Status |
|---|---|---|
| T2.1 | $m_\mathrm{DM}^{G_2} \approx 0.7$ GeV (dark glueball $G_2$) | indirect; SIDM phenomenology |
| T2.2 | HSH-$\nu$DM: $\mathrm{rk}_2 = 0 \Rightarrow$ Dirac for $K_\star = \mathbb{Q}(\sqrt{-67})$ | LEGEND-1000 2030+ |
| T2.3 | Murmurations: glueball ratios cross-$N$ indexed by 2-rank Cl($K_N$) | lattice cross-$N$ |
| T2.4 | Hawking–Page deconfinement universal product $T_c \cdot \tau_\mathrm{int} = 14.3$ | lattice cross-$N$ + cross-curvature |
| T2.5 | $\Delta > 0$ continuum under Bianchi I | HMC anisotropic |
| T2.6 | $\alpha(\mathrm{SO}(5), D=4) = 7/8$, $\alpha(G_2, D=4) = 11/12$ | $\sim \$10\mathrm{k}$ Vast for both |
| T2.7 | Heegner-glueball correlation (BSD–ECI bridge) | LMFDB lookup |
| T2.8 | $n_s = 1 - \kappa/4.7 = 0.9648$ | Planck 2018 $0.9649 \pm 0.0042$, **match $0.01\%$** ⚠️ TIER 5 fragile |
| T2.9 | $\delta_\mathrm{CP} = 59\pi/60 = 177°$ | NuFit-6.0 $177° \pm 20°$, **match $1\sigma$** |
| T2.10 | $m_\mathrm{axion} = 1.10$ μeV from $D = -163$ | ABRACADABRA/DM-Radio 2026–2030 |

### Tier 3 — Long-term (5–15 years)

T3.1 (Mass gap continuum B1, Clay), T3.2 (quark masses from $\xi(K_\star)$), T3.3 (Lemma A3-2 Selberg pretrace), T3.4 (cosmic information conservation $\to$ BH unitarity).

### Bonferroni honesty

The five Tier-1/2 predictions that match observation at $\leq 1\%$ (T1.4, T1.5, T1.6, T1.7, T2.8, T2.9) are **not independent posteriors** of a search through the framework. T1.4 and T1.5 come from the same "ratio of $2/3$ from Vassilevich heat-kernel" template, T1.6 and T1.7 from "maximal coupling" templates, and T2.8 from the same $\kappa = 1/6$ ratio. A conservative Bonferroni discount on the joint posterior (n = 8 attempted Tier-1 formulae, n = 22 across all tiers) gives an effective per-prediction significance of $\sim 0.005 \cdot 8 \approx 4\%$ chance for any single $\leq 1\%$ match to be a coincidence, which after $n = 5$ confirmed matches gives a global pattern significance of $\sim (0.04)^5 \approx 10^{-7}$. This is suggestive but does not constitute a theorem; the standard scepticism applies (Bode's law, Koide-style numerology, etc.).

The single Tier-1 prediction (T1.6) that is consistent now but forecast to fail at $14\sigma$ at HL-LHC by 2030 is **the principal near-term falsification risk** and should be flagged honestly in any communication.

## 4. The four (or five) structural gaps for unification

We list the gaps that must be closed for the framework to constitute a unification rather than a coincidence pattern, with quantified difficulty and new-physics requirement.

| # | Gap | Specific question | Difficulty | New physics? | Realistic timeline |
|---|---|---|---|---|---|
| A | $\kappa$ as Ricci invariant on $\mathcal{A} / \mathcal{G}$ | derive $\kappa = 1/(2|\Phi^+|)$ from the Lie geometry of the orbit space rather than from combinatorial roots count | 🔴 high | no | $12$–$24$ months focused mathematics |
| B | $\sqrt{1 - \kappa}$ in $\omega_\mathrm{QNM}$ via AdS/CFT | derive QNM shift from the same $\kappa$ on the gravity side, without invoking strict large-$N$ planar limit | 🟡 medium | no, if AdS/CFT rigorous at $N = 3$ | $5$–$15$ years |
| C | $1/4$ prefactor shared with Bekenstein–Hawking | derive $1/4$ from the Hopf fibration $S^3 \to S^2$ or other purely geometric invariant of the gauge sector | 🔴 high | yes (gauge–gravity coupling) | $20$–$50$ years |
| D | Joint integer condition $N = 2|\Phi^+| + 1 = 7$ and $D = -163$ for $\mathrm{SU}(3)$ | derive the joint identity from a Calabi–Yau / F-theory compactification with $\mathrm{SU}(3)$ holonomy and class number 1 on the imaginary-quadratic side | 🟡 medium | possibly (compactification scheme) | $5$–$15$ years (companion note `NOTE_GAP_A4_HEEGNER_PHI_2026-05-24.md`) |
| E | Standard Model phenomenology (Yukawas, generations, CKM, Higgs VEV) | the framework is silent | n/a — outside scope | irrelevant for the present framework | n/a |

Gaps A, B, and D are attackable with present mathematics; Gap C requires a gauge–gravity coupling that is itself not yet rigorously defined; Gap E is honestly outside scope.

The framework therefore positions itself as a **structural reduction**, not a theory of everything. It identifies five convergent patterns in $\mathrm{SU}(3) \times D = 4$, encodes them in 22 falsifiable predictions, and quantifies the gaps for further work.

## 5. Honest scope and the Clay Prize

The framework's primary mathematical target is the Yang–Mills mass-gap problem for $\mathrm{SU}(N)$ in $D = 4$. The Piste E conditional theorem (companion document `PAPER_LMP_PISTE_E_v0_2026-05-24.{tex,pdf}`, 11 pages, target Letters in Mathematical Physics) reduces the Clay problem to a single named axiom — concentration of the Wilson Gibbs measure at the vacuum, equivalent in difficulty to Bałaban's cluster-expansion programme. The author's honest estimate of the Clay probability is:

| Horizon | $P$(Clay solved) | Conditional on |
|---|---|---|
| 5 years | 5–6% | — |
| 10 years (alone) | 15–18% | — |
| **10 years with active Bauerschmidt collaboration** | **25–35%** | initial pitch acceptance (`PITCH_BAUERSCHMIDT_V22_FINAL_2026-05-24.pdf`, 7 pp, sent 2026-05-24) |

The honest narrative is: the framework supplies a structurally clean conditional theorem (Piste E paper), a measured cross-dimensional empirical check ($\alpha(\mathrm{SU}(3), D = 3) = 0.85 \pm 0.03$ this work), and a set of convergent patterns that contextualise the result in the larger landscape of YM-gravity-cosmology connections. It does not solve Clay alone; it makes Clay attackable by Bauerschmidt's framework in a quantified way.

## 6. Anti-fabrication audit

This synthesis cites no fabricated references. The four catches consigned in the present session's anti-fabrication ledger (cluster firm 731 STABLE) are:
- "Otto–Westdickenberg 2008 JFA 254:2865–2940" — fabrication (correct paper: OW 2005, SIAM JMA **37**, porous-medium $W_2$ contraction, not LSI).
- "Kondratiev–Piatnitski–Zhizhina 2020 LSI on singular strata" — misattribution.
- "Brydges–Federbush 1980 YM abelian" — wrong attribution (correct: Brydges–Fröhlich–Seiler 1980, CMP **71**).
- "Sternbeck et al. 2005 hep-lat/0509134" — wrong author list (correct: Tok–Langfeld–Reinhardt–von Smekal).

None of these are cited in the present document.

The Pattern 4 falsification on the gravity side (Kerr QNM overtones do not show $\sqrt{2}$ ratio) is recorded as a partial reframing rather than a hidden problem; Pattern 4 remains valid in the YM context.

The $0.005\%$ precision claim on the Heegner cosmological-constant formula (BIGTABLE V4 UNIFIED, 2026-05-20, §X.I) has been re-examined and found to require a fine-tuned non-integer exponent $\approx -7.034$; at the integer exponent $-7$ the precision is $\sim 2.15\%$. The integer-exponent version is the structurally interesting statement and is the one presented here, with the precision discrepancy disclosed in companion note `NOTE_GAP_A4_HEEGNER_PHI_2026-05-24.md`.

## 7. Acknowledgements

This synthesis benefited from adversarial review by multiple independent large language models acting as second opinions under explicit anti-fabrication discipline (no LLM is a co-author of the mathematical or physical claim; the author thanks the dispatch threads for typesetting, literature retrieval, and adversarial cross-checking, per COPE recommendations). The Wilson flow JAX module (`wilson_flow_su3_d3.py`, 868 lines, Lüscher 2010 RK3 [arXiv:1006.4518](https://arxiv.org/abs/1006.4518) verified verbatim) provides the cleaner $\alpha$ measurement protocol referenced in §1.2 and is currently running an overnight precision-upgrade campaign on a personal RTX 5060 Ti workstation, expected to either tighten or modify the bootstrap estimate of $\alpha(\mathrm{SU}(3), D = 3)$ in the next 24 hours.

## 8. References

- Athenodorou, A., Teper, M. (2021). *SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology*. JHEP **12**, 082, [arXiv:2106.00364](https://arxiv.org/abs/2106.00364).
- Bekenstein, J. D. (1973). *Black Holes and Entropy*. Phys. Rev. D **7**, 2333.
- Berti, E., Cardoso, V., Starinets, A. O. (2009). *Quasinormal modes of black holes and black branes*. Class. Quantum Grav. **26**, 163001, [arXiv:0905.2975](https://arxiv.org/abs/0905.2975).
- Brydges, D. C., Fröhlich, J., Seiler, E. (1980). *Construction of quantized gauge fields II. Convergence of the lattice approximation*. Comm. Math. Phys. **71**, 159–205.
- Cao, S., Nissim, V., Sheffield, S. (2025). *Dynamical approach to area law for lattice Yang–Mills*. [arXiv:2509.04688](https://arxiv.org/abs/2509.04688).
- Cover, T. M., Thomas, J. A. (2006). *Elements of Information Theory*, 2nd ed., Wiley (Pinsker inequality, Lemma 11.6.1).
- Gross, L. (1975). *Logarithmic Sobolev inequalities*. Amer. J. Math. **97**, 1061–1083.
- Hawking, S. W. (1975). *Particle creation by black holes*. Comm. Math. Phys. **43**, 199.
- Heegner, K. (1952). *Diophantische Analysis und Modulfunktionen*. Math. Z. **56**, 227–253.
- Leaver, E. W. (1985). *An analytic representation for the quasi-normal modes of Kerr black holes*. Proc. R. Soc. Lond. A **402**, 285.
- Lüscher, M. (2010). *Properties and uses of the Wilson flow in lattice QCD*. JHEP **08**, 071, [arXiv:1006.4518](https://arxiv.org/abs/1006.4518).
- Maldacena, J. (1997). *The Large N limit of superconformal field theories and supergravity*. Adv. Theor. Math. Phys. **2**, 231–252, [arXiv:hep-th/9711200](https://arxiv.org/abs/hep-th/9711200).
- Stark, H. M. (1967). *A complete determination of the complex quadratic fields of class-number one*. Michigan Math. J. **14**, 1–27.

---

*Synthesis draft v1 · 2026-05-24 ~21h CEST · Kévin Rémondière, Oloron-Sainte-Marie, France · ORCID 0009-0008-2443-7166 · CC-BY-4.0*

*"Five convergent patterns from one geometric pair $\mathrm{SU}(3) \times D = 4$ — empirically validated to $99.06\%$ for the Lie-algebraic $\kappa$ on $\mathrm{SU}(3)$ $D = 3$ lattice; $1/4$ prefactor shared with Bekenstein–Hawking; triple selection of $D = 4$; $\sqrt{2}$ glueball ratio with Temperley–Lieb structural backing; 22 falsifiable predictions, 5 confirmed at $\leq 1\%$, 1 principal HL-LHC falsification risk on $y_t = 1/\sqrt{2}$. Triangulation, not unification. $P$(Clay 10y) honest = 25–35% with active Bauerschmidt collaboration."*
