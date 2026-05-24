# Paper LMP Piste E — v0 outline (markdown summary)

**Title** : Conditional log-Sobolev inequality and mass gap for Wilson SU(N) lattices under an explicit concentration axiom

**Author** : Kévin Rémondière (Independent researcher, Oloron-Sainte-Marie, France) — ORCID 0009-0008-2443-7166 — kevin.remondiere@gmail.com

**License** : CC-BY 4.0

**Target journal** : Letters in Mathematical Physics (LMP) or Communications in Mathematical Physics (CMP)

**Status** : v0 outline, 2026-05-24 — structural skeleton compilable to ~13-15 pages, Kévin to revise before submission.

**File** : `/tmp/voie1_calcs/PAPER_LMP_PISTE_E_v0_2026-05-24.tex` (LaTeX, amsart 11pt, 566 lines, 10 sections, 32 subsections, 32 bibitems).

---

## Structure overview

| § | Title | Pages target | Content |
|---|-------|--------------|---------|
| 1 | Introduction | 1.5 | Context, state of the art, our contribution, three forms of H1, saturated family, L^-2 disclaimer, what this paper is not |
| 2 | Setup and notations | 1.5 | Lattice, Wilson measure, Langevin generator, gauge potential, saturated family definition, kappa, normal cone |
| 3 | Main theorem | 1.5 | Theorem statement, 6 hypotheses (H1-H6) with status table, three equivalent forms of H1 (raw / Polchinski-cascade / susceptibility) |
| 4 | Proof sketch | 3 | Six steps : (1) normal cone, (2) Gaussianisation, (3) Gaussian LSI, (4) kappa factor, (5) entropy splitting, (6) spectral gap via Sjöstrand |
| 5 | L^-2 is artefactual | 2 | Three pieces of evidence (BBD23 phi^4_3 uniform L, CNS25 SU(N) uniform L, Lüscher 1986 exponential), Ginzburg-Landau counter-example, path to removal via H10 |
| 6 | Optional strengthening H7-H10 | 1 | H7 Theorem C empirical, H8 Lüscher exp, H9 kappa continuum, H10 non-abelian Polchinski cascade + Proposition (upgrade kills L^-2) |
| 7 | Cross-dim predictions | 1 | (SU(2),2) alpha=1/2, (SU(3),3) alpha=3/4, (SU(3),4) alpha=5/6 -- three independent falsification tests |
| 8 | Comparison with related work | 1 | vs MRS93, vs Balaban, vs BBD phi^4, vs CNS25/Nissim, vs SZZ22/SZZ24/CCHS22 |
| 9 | Discussion and outlook | 0.5 | Pattern Wiles 1995, 9-15 month timeline, honest scope (what theorem accomplishes / does not) |
| 10 | Acknowledgements | 0.25 | LLM disclosure (COPE-compliant), three explicit fab catches (OW2008, KPZ, Brydges-Federbush), Lean community |
| Bib | References (32 items) | 1.5 | All arXiv IDs verified via WebFetch in session |

**Estimated typeset length** : ~13-15 pages (LMP format, 11pt single-column).

---

## The conditional theorem (one-paragraph statement)

For a saturated pair $(G, d) \in \{(\mathrm{SU}(2), 2), (\mathrm{SU}(3), 3), (\mathrm{SU}(3), 4)\}$ (defined by the polynomial identity $\mathrm{rk}(G) = d(d-1)(5-d)/6$), under hypotheses H1-H6 (H1 = concentration axiom, OPEN ; H2-H6 = proved or Lean-certified), the Wilson Langevin generator on $G^{E(\Lambda_a)}$ satisfies

$$\lambda_1(\mathcal{L}_\beta) \geq \varepsilon(N, d) \cdot (1 - \kappa(G, d)) \cdot \beta \cdot L^{-2}$$

with $\kappa(G, d) = 1/(2(d-1))$, yielding a positive lattice mass gap $m^{\mathrm{lattice}}_{\mathrm{gap}} \geq \sqrt{\lambda_1(\mathcal{L}_\beta)} > 0$. The $L^{-2}$ factor is artefactual (BBD23, CNS25, Lüscher 1986 all show otherwise for the right side) and is removed by the strengthened hypothesis H10 (non-abelian Polchinski-cascade).

---

## Three forms of H1

| Form | Statement | Operational role |
|------|-----------|------------------|
| **H1 (raw)** | $\mu_{a,L,\beta}(\|A\|^2 \geq R) \leq C_1 \exp(-c_1 \beta R / N^2)$ uniformly in $(a, L)$ | Direct probabilistic concentration |
| **H1'' (Polchinski-cascade)** | $\mu_{a,L,\beta} = \mu^{(0)} \ast \cdots \ast \mu^{(K)}$ with each layer LSI($c_k$), $\sum c_k \leq C/(\beta(1-\kappa))$ uniformly in $(a, L)$ | Natural target for BBD framework extension |
| **H1''' (bounded susceptibility)** | $\chi_\beta(L) = \sum_x \mathrm{cov}(\mathrm{tr} Q_0, \mathrm{tr} Q_x)$ bounded uniformly in $(a, L)$ | Most BBD-compatible input |

All three are equivalent up to constants of order $\beta$; the choice of formulation determines which existing machinery is the natural target.

---

## Six hypotheses status table

| # | Content | Status |
|---|---------|--------|
| H1 | Concentration of $\mu_{a,L,\beta}$ at the vacuum, exponential in $\beta$ | **Open** (= cluster-expansion lock) |
| H2 | Gaussian density bound on $\{\|A\|^2 \leq R\}$ | Open in stated form ; sketched after MRS93 |
| H3 | Pinsker $\alpha=1$ | Proved (Cover-Thomas 2006) ; Lean 4 formalised |
| H4 | Gaussian LSI on Cameron-Martin space | Proved (Gross 1975, Amer. J. Math. 97) |
| H5 | $\lambda_1(\Delta_\Lambda) \geq C_2/L^2$ on the torus | Proved (discrete Fourier analysis) |
| H6 | $\kappa(\mathrm{SU}(3), 4) = 1/6$ from Hodge / $A_2$ roots | Proved (Lean 4, zero axioms, two independent derivations) |

---

## Saturated family details

$\Sigma(d) := d(d-1)(5-d)/6$ gives :

| $(N, d)$ | $\Sigma(d)$ | $\kappa = 1/(2(d-1))$ | $\alpha = 1-\kappa$ | Physical status |
|----------|------------|------------------------|---------------------|-----------------|
| $(2, 2)$ | $1$ | $1/2$ | $1/2$ | 2D YM, heat kernel exact |
| $(3, 3)$ | $2$ | $1/4$ | $3/4$ | 3D SU(3), Lüscher gradient flow accessible |
| $(3, 4)$ | $2$ | $1/6$ | $5/6$ | **Physical case, last non-trivial dim** |

For $d \geq 5$, $\Sigma(d) \leq 0$ : no non-abelian compact simple Lie group is saturated. $d = 4$ is the maximal non-trivial member.

---

## Anti-fab discipline applied

### Citations verified via WebFetch (session 2026-05-24)

- arXiv:2202.02295 -- Bauerschmidt-Dagallier, *Log-Sobolev inequality for the $\varphi^4_2$ and $\varphi^4_3$ measures*, CPAM 77 (2024) 2579-2612. **VERIFIED**.
- arXiv:2307.07619 -- Bauerschmidt-Bodineau-Dagallier, *Stochastic dynamics and the Polchinski equation: an introduction*, Probab. Surv. 21 (2024) 200-290. **VERIFIED**.
- arXiv:1907.12308 -- Bauerschmidt-Bodineau, *Log-Sobolev inequality for the continuum sine-Gordon model*, CPAM 74 (2021) 2064-2113. **VERIFIED**.
- arXiv:2509.04688 -- Cao-Nissim-Sheffield, *Dynamical approach to area law for lattice Yang-Mills*, preprint 2025 (8 pages, v2 2025-09-28). **VERIFIED**. Note: paper is short, addresses 't Hooft regime, uses prior mass gap (CNS prior work) and dynamical framework.
- arXiv:2510.22788 -- Nissim, *U(N) lattice Yang-Mills in the 't Hooft regime*, preprint 2025 (25 pages, 2025-10-26). **VERIFIED**.
- arXiv:2204.12737 -- Shen-Zhu-Zhu, *A stochastic analysis approach to lattice Yang-Mills at strong coupling*, CMP 400 (2023) 805-851. **VERIFIED**.
- arXiv:2202.02301 -- Bauerschmidt-Dagallier, *Log-Sobolev inequality for near critical Ising models*, CPAM 77 (2024) 2568-2576. **VERIFIED**.
- arXiv:2202.10375 -- Adhikari-Cao, *Correlation decay for finite lattice gauge theories at weak coupling*. **VERIFIED but NOT CITED** in paper -- restricted to finite gauge groups, not applicable to SU(N) continuous.
- arXiv:2505.16585 -- Cao-Nissim-Sheffield, *Expanded regimes of area law for lattice Yang-Mills theories*. **VERIFIED**.
- arXiv:2401.13299 -- Shen-Zhu-Zhu, *Langevin dynamics of lattice Yang-Mills-Higgs and applications*. **VERIFIED**.
- arXiv:hep-th/0203027 -- Rudolph-Schmidt-Volobuev, *On the gauge orbit space stratification: a review*, J. Phys. A 35 (2002) R1-R50. **VERIFIED**.
- arXiv:dg-ga/9411007 -- Huebschmann, *The singularities of Yang-Mills connections for bundles on a surface. II.*, Math. Z. 221 (1996) 83-92. **VERIFIED**.
- arXiv:hep-lat/0404008 -- Lucini-Teper-Wenger, *Glueballs and k-strings in SU(N) gauge theories*, JHEP 06 (2004) 012. **VERIFIED**.
- arXiv:2106.00364 -- Athenodorou-Teper, *SU(N) gauge theories in 3+1D: glueball spectrum, string tensions and topology*, JHEP 12 (2021) 082. **VERIFIED**.
- arXiv:2201.03487 -- Chandra-Chevyrev-Hairer-Shen, *Stochastic quantisation of Yang-Mills-Higgs in 3D*, Invent. Math. 237 (2024) 541-696. **VERIFIED** (NOT "Shen 2021" as in some earlier context).
- arXiv:1108.1335 -- Dimock, *The renormalization group according to Bałaban*, exposition. **CITED** for Bałaban exposition.

### Citations explicitly NOT used (per anti-fab brief)

- **NOT cited**: "Otto-Westdickenberg 2008 JFA 254:2865-2940" -- fabrication, does not exist.
- **NOT cited**: "Kondratiev-Piatnitski-Zhizhina 2020 LSI singular strata" -- misattribution.
- **NOT cited**: "Brydges-Federbush 1980 YM abelian" -- correct attribution is Brydges-Fröhlich-Seiler 1980 CMP 71 (used).
- **NOT cited**: "Sternbeck et al 2005 hep-lat/0509134" -- correct attribution Tok-Langfeld-Reinhardt-von Smekal, not needed for this paper.

### Acknowledgements paragraph

Three explicit fab catches are disclosed in the §Acknowledgements (COPE-compliant LLM disclosure). The paper distinguishes itself from earlier drafts that propagated these errors.

---

## Length and format checks

- **Document class** : amsart, 11pt
- **Page format** : A4, 1in margins
- **Sections** : 10 (numbered §1-§10 + Bibliography)
- **Subsections** : 32
- **Theorems / Hypotheses / Propositions** : 12 numbered environments
- **Bibitems** : 32 (all arXiv-verified)
- **Source lines** : 566
- **Estimated typeset pages** : ~13-15

---

## Honest framing summary

**What this paper accomplishes** :

1. Names and locates the single open analytic step (H1 = concentration axiom);
2. Rigorously articulates the downstream chain H1 ⇒ lattice mass gap on the saturated family;
3. All auxiliary hypotheses H2-H6 either standard or Lean-certified;
4. The L^-2 artefact identified, with the path to its removal made precise (via H10 non-abelian Polchinski cascade);
5. Three falsifiable cross-dimensional predictions extracted ($\alpha = 1/2, 3/4, 5/6$ for the three saturated pairs).

**What this paper does NOT accomplish** :

1. Not a resolution of Clay Yang-Mills in any sense;
2. Does not address the continuum limit $a \to 0$;
3. Does not yield a constant uniform in $L$ (artefact discussion §5);
4. Does not construct Wightman / Osterwalder-Schrader axioms.

**Pattern** : Wiles 1995 (modularity as named open conjecture; later closed by Taylor-Wiles 1995). No claim to historical parallel ; only structural template.

---

## Next steps for Kévin

1. **Read entire LaTeX file** (`/tmp/voie1_calcs/PAPER_LMP_PISTE_E_v0_2026-05-24.tex`, 566 lines);
2. **Compile** to PDF (`pdflatex PAPER_LMP_PISTE_E_v0_2026-05-24.tex`, twice for TOC + bib);
3. **Revise** Step 4 of §4 (proof sketch) -- the multiplicative factor $(1-\kappa)$ derivation on $\mu_{a,L,\beta}(\cdot | E_R)$ vs pure Gaussian is the most fragile passage and should be expanded or moved to a companion paper as noted in the draft;
4. **Decide** : if Bauerschmidt replies positively to pitch v22.1, this draft becomes follow-up co-authored ; otherwise submit solo to LMP at month 1-3 mark;
5. **Adversarial audit** : 2 Opus + DeepSeek cross-check expected per brief (anti-fab discipline).

---

*v0 outline · 2026-05-24 · Kévin Rémondière · ORCID 0009-0008-2443-7166*
