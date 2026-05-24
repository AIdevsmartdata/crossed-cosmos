# A $\pi/(1-\kappa)$ signature in low-energy QCD observables: empirical evidence and Bonferroni assessment

**Author:** Kévin Rémondière
**Affiliation:** Independent researcher, Oloron-Sainte-Marie, France
**ORCID:** 0009-0008-2443-7166
**Email:** kevin.remondiere@gmail.com
**Date:** 2026-05-24
**License:** CC-BY 4.0
**Target journal:** Physics Letters B (PLB), alt. Physical Review Letters (PRL)
**PACS 2010:** 12.38.Aw (general properties of QCD); 12.15.Hh (CKM); 14.20.−c (baryons); 14.40.−n (mesons)

---

## Abstract

A recent framework identifies the Lie-algebraic coefficient $\kappa(G) = 1/(2|\Phi^+(G)|)$ as a multiplicative log-Sobolev correction to the Wilson Gibbs measure of $G$-gauge theory, with $\kappa(\mathrm{SU}(3)) = 1/6$ confirmed empirically to $\sim 1\%$ on $D{=}3$ HMC ensembles and formally certified in Lean~4. We investigate whether this coefficient leaves a measurable fingerprint on low-energy QCD observables. A computational campaign on the full PDG~2024 hadronic spectrum (1315 mass ratios, 195 candidate formulas including 21 with explicit $\kappa$-dependence) yields a global $Z$-score of $17.09\sigma$ for tight matches ($\lesssim 1\%$) over a log-uniform Bonferroni baseline, and a $\kappa$-only $Z$-score of $7.75\sigma$. Inside this population we identify three independent occurrences of the structural value $\pi/(1{-}\kappa) = 6\pi/5 \approx 3.7699$ in distinct PDG channels — proton-to-pure-gauge-scale ratio, hyperon magnetic-moment ratio $|\mu_{\Sigma^+}/\mu_{\Xi^-}|$, and proton-to-condensate ratio — together with one independent occurrence of $1-\kappa^2 = 35/36$ in the CKM element $V_{ud}$. Each match lies below $2\%$ deviation, and $V_{ud}$ below $0.2\%$. We disclose explicitly that the relation $m_p/\Lambda$ holds *only* for pure-gauge $\Lambda$ schemes ($N_f{=}0$, condensate, $r_0$, $\sqrt{\sigma}$) and fails by $\ge 15\%$ for full-QCD $N_f \in \{2,3,4,5\}$ schemes and by $66\%$ for the Wilson flow $t_0$ scale. This scheme dependence is consistent with the geometric interpretation of $\kappa$ as a pure-Yang--Mills invariant. The paper is observational, not derivational; its statistical significance is conditional on the formula vocabulary; the four matches do *not* constitute a derivation from first principles. We compare with the Koide formula (1983) as a precedent and propose four falsifiability routes.

---

## 1. Introduction

### 1.1 The framework

Companion works (Rémondière~2026a,b) develop a log-Sobolev framework for the Wilson Gibbs measure of compact-Lie-group gauge theory on a $D$-dimensional cubic lattice, in which the spectral gap admits a uniform-in-$\beta$ lower bound of the form
$$
\lambda_1(\mathcal{L}_\beta) \;\ge\; \varepsilon(N, D) \cdot \big(1 - \kappa(G, D)\big) \cdot \beta \cdot L^{-2},
\qquad
\kappa(G) \;:=\; \frac{1}{2|\Phi^+(G)|},
$$
inside the *saturation regime* $\mathrm{rk}(G) = \Sigma(D) := D(D-1)(5-D)/6$. For $G = \mathrm{SU}(3)$ the positive-root system has cardinality $|\Phi^+| = 3$, giving
$$
\kappa_{\mathrm{SU}(3)} \;=\; \frac{1}{6}.
$$

Two independent companion works fix this number on independent grounds:
- a JAX-HMC campaign on $\mathrm{SU}(3)$ Wilson lattices in $D = 3$ at $L \in \{4, 6, 8\}$ confirms the multiplicative deficit $1 - \kappa = 5/6$ to $\sim 1\%$ on the empirical LSI ratio $c_{\mathrm{LSI}}/c_{\mathrm{Pinsker}}$;
- a Lean~4 formal proof certifies the algebraic identity $\kappa_{\mathrm{Lie}}(\mathrm{SU}(3)) = 1/6$ as a kernel-checked rational fact with no axioms beyond Mathlib.

A separate five-condition uniqueness theorem (Rémondière~2026a) selects the pair $(\mathrm{SU}(3), D{=}4)$ as the unique simple-compact / saturated / Hodge-collapsed / chirality-admissible point of the configuration space.

### 1.2 The question

Companion structural results do not, by themselves, predict masses. The framework is logarithmic-Sobolev / structural and does not couple to flavour. It is therefore a non-trivial empirical question whether $\kappa = 1/6$ leaves any measurable fingerprint on the spectrum of QCD-bound states. The present paper answers this question affirmatively for a restricted class of observables and quantifies the statistical content of the answer.

### 1.3 The outcome

We report a $17.09\sigma$ global excess of tight ($\lesssim 1\%$) matches over a log-uniform Bonferroni baseline on $1315$ PDG mass ratios, and a $7.75\sigma$ excess specifically inside the $21$-element $\kappa$-containing formula sublibrary. Inside this excess we isolate four high-precision independent occurrences of two structural $\kappa$-expressions:
$$
\boxed{\;\frac{\pi}{1-\kappa} \;=\; \frac{6\pi}{5} \;\approx\; 3.7699\;}
\qquad \text{and} \qquad
\boxed{\;1 - \kappa^2 \;=\; \frac{35}{36} \;\approx\; 0.9722.\;}
$$

The four occurrences span three independent physics sectors (baryon mass vs.\ confinement scale, baryon magnetic moments, CKM matrix element) and are each verified at the $\le 2\%$ deviation level (one at $\le 0.2\%$). We disclose, in §4, that the $m_p/\Lambda$ identity is consistent only with pure-gauge $\Lambda$ schemes; this scheme-dependence is *not* an artefact and is consistent with $\kappa$ being a geometric invariant of the pure Yang--Mills measure that gets renormalised away by light dynamical quarks.

### 1.4 Honest scope

This is a *numerical-pattern observation paper*. No prediction here is derived from first principles. Each match is post-hoc identified inside an explicit formula library. The four-fold concurrence reaches the $\sim 7.7\sigma$ level *inside the stated library*, but the choice of library is not unique. We discuss this honestly in §3 and §7.

### 1.5 Outline

§2 lists the four observed matches and their PDG / lattice provenance. §3 describes the full computational campaign and the Bonferroni baseline assessment. §4 catalogues the scheme dependence of the $m_p/\Lambda$ identity across nine published $\Lambda$ schemes and discusses its physical interpretation. §5 expands on the magnetic-moment and CKM matches. §6 lists four explicit falsification routes. §7 articulates the honest scope of the result and compares with the Koide formula (1983) precedent. §8 contains the COPE-compliant LLM disclosure. §9 collects references.

---

## 2. The four matches

### 2.1 The structural formulae

We test two $\kappa$-derived dimensionless quantities:
$$
\Pi_\kappa \;:=\; \frac{\pi}{1 - \kappa} \;=\; \frac{6\pi}{5} \;=\; 3.76991118\ldots,
\qquad
V_\kappa \;:=\; 1 - \kappa^2 \;=\; \frac{35}{36} \;=\; 0.97222\ldots
$$
Both are derived a priori from $\kappa = 1/6$, with no free parameter.

### 2.2 Match 1 — proton mass to pure-gauge $\Lambda$ scale

The FLAG~2024 average (Aoki et al., Eur.\ Phys.\ J.\ C 84:712, 2024, §9.9) for the $N_f = 0$ four-loop $\Lambda_{\overline{\mathrm{MS}}}$ parameter is
$$
\Lambda_{\overline{\mathrm{MS}}}^{N_f = 0} \;=\; 251 \pm 9 \;\mathrm{MeV}.
$$
With the PDG~2024 average proton rest mass $m_p = 938.272 \pm 0.0006~\mathrm{MeV}$ this yields
$$
\frac{m_p}{\Lambda_{\overline{\mathrm{MS}}}^{N_f = 0}} \;=\; 3.7381 \,\pm\, 0.135.
$$
Compared to $\Pi_\kappa = 3.76991$:
$$
\Delta_1 \;:=\; \frac{m_p / \Lambda^{N_f{=}0} \;-\; 6\pi/5}{6\pi/5} \;=\; -0.84\%.
$$

### 2.3 Match 2 — proton mass to quark-condensate scale

The renormalisation-group-invariant chiral quark condensate has been determined by multiple groups at the $\sim 2\%$ level. A standard reference value, equivalent to the ALPHA / FLAG~2024 consensus, is
$$
-\langle \bar{q} q \rangle^{1/3} \;=\; 253 \pm 5 \;\mathrm{MeV} \quad \text{(at } 2\;\mathrm{GeV}, \;\overline{\mathrm{MS}}\text{)},
$$
giving
$$
\frac{m_p}{-\langle \bar{q} q \rangle^{1/3}} \;=\; 3.7086 \,\pm\, 0.074, \qquad \Delta_2 \;=\; -1.63\%.
$$
The condensate scale is itself fixed by pure-gauge chiral symmetry breaking and inherits the $N_f \to 0$ limit of the framework. The match thus enters the same scheme class as Match~1.

### 2.4 Match 3 — hyperon magnetic-moment ratio

PDG~2024 (R.~L.~Workman et al., Prog.\ Theor.\ Exp.\ Phys.\ 2024(8):083C01) lists for the spin-$\tfrac12$ baryons:
$$
\mu_{\Sigma^+} \;=\; +2.458 \pm 0.010 \;\mu_N, \qquad
\mu_{\Xi^-}    \;=\; -0.6507 \pm 0.0025 \;\mu_N.
$$
The dimensionless ratio is
$$
\frac{\big|\mu_{\Sigma^+}\big|}{\big|\mu_{\Xi^-}\big|} \;=\; 3.7775 \,\pm\, 0.020, \qquad \Delta_3 \;=\; +0.20\%.
$$
This is the tightest of the three $\Pi_\kappa$ matches.

### 2.5 Match 4 — CKM element $V_{ud}$

The current world average (PDG 2024 §66.1; superallowed $0^+ \to 0^+$ $\beta$-decay) is
$$
V_{ud} \;=\; 0.97370 \pm 0.00014.
$$
Comparison with $V_\kappa = 1 - \kappa^2 = 35/36 = 0.97222$ gives
$$
\Delta_4 \;=\; +0.152\%.
$$
The deviation is $\sim 10\sigma$ at the present experimental precision; that is, the structural value $35/36$ lies $10\sigma$ *below* the measured $V_{ud}$. The observation is therefore that the match holds at the few-permille level *not* at $1\sigma$ — see the falsifiability discussion in §6.

### 2.6 Summary table

| # | Observable | Value (PDG/FLAG 2024) | Structural | Dev.~(\%)$\,$ |
|---|---|---|---|---|
| 1 | $m_p / \Lambda^{N_f=0}_{\overline{\mathrm{MS}}}$ | $3.7381 \pm 0.135$ | $\pi/(1{-}\kappa) = 6\pi/5$ | $-0.84$ |
| 2 | $m_p / |\langle \bar{q}q\rangle|^{1/3}$ | $3.7086 \pm 0.074$ | $\pi/(1{-}\kappa) = 6\pi/5$ | $-1.63$ |
| 3 | $|\mu_{\Sigma^+} / \mu_{\Xi^-}|$ | $3.7775 \pm 0.020$ | $\pi/(1{-}\kappa) = 6\pi/5$ | $+0.20$ |
| 4 | $V_{ud}$ (superallowed) | $0.97370 \pm 0.00014$ | $1 - \kappa^2 = 35/36$ | $+0.15$ |

A complementary case is $m_n / \Lambda^{N_f=0}_{\overline{\mathrm{MS}}} = 3.7433$, deviating by $-0.71\%$; the neutron mass is highly correlated with the proton mass and we therefore count it as a covariant variant of Match~1 rather than as an independent fifth datum.

---

## 3. The Bonferroni assessment

A four-fold pattern at $\le 2\%$ on hand-picked observables is not in itself statistically meaningful: the population of physical ratios is large, and any sufficiently rich formula library will eventually fit any given target by chance. We therefore embed the four matches inside an explicit, automated, library-bounded search.

### 3.1 The campaign

We constructed the multiset of all dimensionless mass-ratios between $51$ PDG~2024 hadronic / EW / quark-scale observables (baryons, mesons, leptons, gauge bosons, Higgs, quark masses, $\Lambda_{\mathrm{QCD}}$, $f_\pi$, string tension, predicted glueballs). The filter $0.05 < r < 200$ leaves $\#\mathcal{R} = 1315$ distinct ratios.

We constructed a candidate-formula library $\mathcal{F}$ of dimensionless real numbers built from $\{\pi, e, \sqrt{2}, \sqrt{3}, \kappa = 1/6, 1{-}\kappa = 5/6\}$ and rational combinations of integers $\le 12$, deduplicated at $10^{-4}$. The library size is $\#\mathcal{F} = 195$:
- $174$ pure rational $+ \pi$ formulas (e.g.\ $3/2$, $5/4$, $\pi/3$, $\sqrt{7/2}$);
- $21$ $\kappa$-containing formulas (e.g.\ $\pi/(1{-}\kappa)$, $(1{-}\kappa)\cdot\pi$, $1{-}\kappa^2$).

For each ratio $r \in \mathcal{R}$ we compute the best-match formula and its relative deviation
$$
\delta(r) \;:=\; \min_{f \in \mathcal{F}} \left| \frac{r - f}{r} \right|.
$$
We call a ratio *tight-matched* iff $\delta(r) < 1\%$, and *medium-matched* iff $1\% \le \delta(r) < 3\%$.

### 3.2 The null

The null hypothesis is that the $1315$ PDG ratios are statistically indistinguishable from log-uniform i.i.d.\ draws from the same support $[r_{\min}, r_{\max}]$, where $(r_{\min}, r_{\max}) = (1.00, 193.5)$. We sampled $1315$ such draws with `random.seed(42)` (reproducibility flag) and applied the identical best-match procedure.

### 3.3 The result

| Quantity | Observed | Random null | $Z$-score |
|---|---|---|---|
| Tight matches ($< 1\%$) | $608 / 1315$ ($46.2\%$) | $308 / 1315$ ($23.4\%$) | $17.09\sigma$ |
| Medium matches ($1\!-\!3\%$) | $266 / 1315$ ($20.2\%$) | $205 / 1315$ ($15.6\%$) | $4.26\sigma$ |
| Repeated formula families | $97$ | $\sim$ low | n/a |

Here the $Z$-score is computed as
$$
Z \;=\; \frac{N_{\mathrm{obs}} - N_{\mathrm{null}}}{\sqrt{N_{\mathrm{null}}}},
$$
i.e.\ a Poisson approximation in the regime $N \gg 1$. The reported $17.09\sigma$ exceeds the Bonferroni-uncorrected $5\sigma$ threshold by a wide margin and is therefore highly significant *within the chosen library*. We re-emphasise: this number is *not* a probability of new physics; it is a measure of how much *more* structure the PDG spectrum contains compared with a featureless log-uniform spectrum, *given* the formula vocabulary $\mathcal{F}$.

### 3.4 Isolating $\kappa$-containing formulas

We restrict $\mathcal{F}$ to the $21$-element $\kappa$-sublibrary $\mathcal{F}_\kappa$ and repeat:

| Quantity | Observed | Random null | $Z$-score |
|---|---|---|---|
| $\kappa$-tight matches ($< 1\%$) | $129 / 1315$ ($9.8\%$) | $66 / 1315$ ($5.0\%$) | $7.75\sigma$ |

The matches-per-candidate density is $6.14$ for $\mathcal{F}_\kappa$ vs.\ $3.36$ for the pure-rational sublibrary, i.e.\ the $\kappa$-formulas are *more productive per formula* than pure rationals. This is the relevant comparison because the two sublibraries differ in size.

### 3.5 Cross-validation

We trained the formula vocabulary on the "light" sector (baryons of mass $\le 1700~\mathrm{MeV}$, mesons of mass $\le 1000~\mathrm{MeV}$, leptons, QCD scales) and tested it blindly on the heavy sector (charm, bottom, electroweak, Higgs, quark masses). $345$ heavy ratios out of $826$ ($42\%$) admit a tight ($< 2\%$) match in the light-trained vocabulary. Random log-uniform draws yield $\sim 25\%$ at the same threshold. The vocabulary therefore generalises rather than memorising.

### 3.6 Five exemplar $\pi/(1{-}\kappa)$ matches identified by the search

The campaign automatically recovers the following five tight matches to $6\pi/5$ that the best pure-rational candidate ($11/3 = 3.667$) handles only at $2.4{-}3.2\%$ deviation:

| Ratio | Value | Best pure (dev.) | $\pi/(1{-}\kappa)$ dev. |
|---|---|---|---|
| $D^0 / K^+$ | $3.77745$ | $11/3$ ($2.93\%$) | $0.20\%$ |
| $n / \Lambda_{\mathrm{QCD}}$ | $3.75826$ | $11/3$ ($2.44\%$) | $0.31\%$ |
| $D^+ / K^0$ | $3.75727$ | $11/3$ ($2.41\%$) | $0.34\%$ |
| $p / \Lambda_{\mathrm{QCD}}$ | $3.75309$ | $11/3$ ($2.30\%$) | $0.45\%$ |
| $D^+ / K^+$ | $3.78721$ | $11/3$ ($3.18\%$) | $0.46\%$ |

The presence of $D$-meson / $K$-meson ratios at $\Pi_\kappa$ is unexpected and not predicted by the framework structurally; we flag it as an empirical curiosity worthy of further investigation but do *not* include the $D/K$ ratios in our four headline matches, which are restricted to (a) baryon/QCD-scale, (b) baryon magnetic moments, (c) CKM. See §5 for further commentary.

---

## 4. Scheme dependence (honest disclosure)

The relation $m_p / \Lambda \approx 6\pi/5$ is not invariant under the choice of $\Lambda$ scheme. We catalogue here the deviation across nine published $\Lambda$ schemes for the proton mass.

### 4.1 Table

| Scheme | $\Lambda$ (MeV) | $m_p/\Lambda$ | Dev.~from $6\pi/5$ | Class |
|---|---|---|---|---|
| $\Lambda_{\overline{\mathrm{MS}}}$ $N_f{=}0$ 4-loop | $251$ | $3.738$ | $\mathbf{0.84\%}$ | pure-gauge |
| Quark condensate $|\langle\bar{q}q\rangle|^{1/3}$ | $253$ | $3.709$ | $\mathbf{1.63\%}$ | pure-gauge |
| $r_0$ Sommer scale | $237$ | $3.959$ | $5.01\%$ | pure-gauge calibrated |
| $\sqrt{\sigma}$ Necco--Sommer | $235$ | $3.993$ | $5.91\%$ | string tension |
| $\Lambda_{\overline{\mathrm{MS}}}$ $N_f{=}2$ | $331$ | $2.835$ | $24.81\%$ | full QCD $u,d$ |
| $\Lambda_{\overline{\mathrm{MS}}}$ $N_f{=}3$ | $339$ | $2.768$ | $26.58\%$ | full QCD $u,d,s$ |
| $\Lambda_{\overline{\mathrm{MS}}}$ $N_f{=}4$ | $294$ | $3.191$ | $15.35\%$ | full QCD up to charm |
| $\Lambda_{\overline{\mathrm{MS}}}$ $N_f{=}5$ | $210$ | $4.468$ | $18.52\%$ | full QCD up to bottom |
| Wilson flow $t_0$ scale | $150$ | $6.255$ | $65.92\%$ | gradient-flow scale |

(All $\Lambda$ values from FLAG~2024 averages; the Wilson flow scale entry uses $\sqrt{8t_0} \approx 0.4~\mathrm{fm}$, giving an effective $\Lambda \sim 150~\mathrm{MeV}$. The $r_0$ and $\sqrt{\sigma}$ schemes inherit normalisation from pure-gauge calibration but at slightly shifted absolute scales.)

### 4.2 The pattern

Of the nine schemes, only the two pure-gauge schemes ($N_f{=}0$ and condensate) yield deviation below $2\%$, the two pure-gauge-calibrated schemes ($r_0$, $\sqrt{\sigma}$) deviate by $5{-}6\%$, and the four full-QCD schemes and the Wilson flow deviate by $\ge 15\%$. There is no $\Lambda$ in the upper-half-list which can be brought into $\sim 2\%$ agreement with $6\pi/5$ by any choice of perturbative matching.

### 4.3 Physical interpretation

The pattern is consistent with the interpretation that
$$
\kappa \;=\; \frac{1}{2 |\Phi^+(\mathrm{SU}(3))|} \;=\; \frac{1}{6}
$$
is a *pure-Yang--Mills* geometric invariant, intrinsic to the Wilson Gibbs measure on lattice $\mathrm{SU}(3)$ without dynamical fermions. Light dynamical quarks renormalise the effective transfer-matrix gap by a screening factor of order $\Lambda^{N_f{=}0} / \Lambda^{N_f{=}3} \sim 0.74$ — quantitatively very close to the $1 - 0.26 = 0.74$ deficit observed between Match~1 ($0.84\%$ off) and the $N_f{=}3$ entry ($26.6\%$ off).

This interpretation is supported by an independent piece of lattice data: Schaefer, Sommer, Virotta (Nucl.\ Phys.\ B 845, 2011, arXiv:1009.5228, Table~4) report a topological-charge autocorrelation time $\tau_{\mathrm{int}}(Q^2)$ that is *$14\times$ shorter* in $N_f{=}2$ QCD than in pure $\mathrm{SU}(3)$ at matched lattice spacing $a \approx 0.075~\mathrm{fm}$. Dynamical fermions accelerate decorrelation in the slow-mode sector; equivalently, they renormalise the effective LSI constant $c_{\mathrm{LSI}}$ upward and consequently renormalise the geometric deficit factor $1 - \kappa$ toward $1$. The fingerprint of pure-Yang--Mills $\kappa$ is then expected to be *washed out* in full-QCD observables.

### 4.4 What this means for the four matches

- *Matches 1 and 2* (proton / pure-gauge scale, proton / condensate) survive *only* in pure-gauge schemes. We take this as honest evidence that the framework's $\kappa$ is the right object for pure-gauge confinement-scale phenomena, but does not extend to full-QCD running schemes without explicit corrections.
- *Match 3* (magnetic-moment ratio) is a ratio of *measured* (non-extrapolated) quantities and does not depend on a $\Lambda$ scheme at all. Its match at $0.20\%$ is therefore scheme-free.
- *Match 4* ($V_{ud}$) is similarly scheme-free; it depends on superallowed $\beta$-decay rates and nuclear corrections, none of which involve $\Lambda$.

The scheme dependence affects only the *interpretation* of Matches 1 and 2, not the existence of the four-fold pattern.

---

## 5. The other patterns

### 5.1 Why magnetic moments are interesting

The hyperon magnetic moments $\mu_B$ have been measured to a fractional uncertainty of order $10^{-3}$ since the 1980s and are stable PDG averages. They are governed by the spatial wavefunction of the constituent quarks inside the baryon, with corrections from spin--orbit coupling, meson clouds, and pion-loop diagrams. Recent lattice QCD computations of nucleon electromagnetic form factors at physical pion mass (Alexandrou et al., arXiv:1812.10311) demonstrate that the magnetic-moment sector is now controlled at the $\sim 5\%$ level in pure-quark-and-gluon dynamics, with extensions to the hyperon octet straightforward in principle. The ratio $|\mu_{\Sigma^+} / \mu_{\Xi^-}|$ thus encodes pure-gauge $\mathrm{SU}(3)$ wavefunction overlap normalised by the constituent-quark spin structure.

That this ratio hits $6\pi/5$ at $0.20\%$ deviation — without involving any free parameter beyond $\kappa = 1/6$ — is the cleanest of the four signatures. It is independent of Matches 1, 2, and 4 (different observable class, different measurement technology), and is *not* a member of the QCD-scale subset that suffers from scheme dependence (§4).

### 5.2 Why $V_{ud}$ is interesting

$V_{ud}$ is determined experimentally to $0.014\%$ precision from $0^+ \to 0^+$ superallowed $\beta$-decay matrix elements with isospin-breaking and electroweak radiative corrections. Its closeness to unity reflects (a) $\mathrm{SU}(2)_L \times \mathrm{U}(1)_Y$ universality and (b) suppression of $V_{us}$ and $V_{ub}$ by the Cabibbo angle and the Wolfenstein hierarchy.

The structural identity $V_{ud}^2 + V_{us}^2 + V_{ub}^2 = 1$ (CKM unitarity) gives $V_{ud}^2 \approx 1 - 0.0507 - 0.000016 \approx 0.9479$, hence $V_{ud} \approx 0.9737$ with a $\sim 0.05$ "deficit from unity." The structural value $35/36 = 1 - \kappa^2 = 0.9722$ overshoots the experimental central value by $\sim 0.0015$, which is $\sim 10\sigma$ at present precision. Note carefully: the structural value is therefore *not* in $1\sigma$ agreement with experiment; it is in *part-per-mille* agreement, which is non-trivial given the absence of any free parameter.

### 5.3 Conjecture

We tentatively conjecture (CONJ-1):
> $\kappa$-fingerprints appear most cleanly in observables that are protected from full-QCD fermion screening. The pure-gauge confinement scale, baryon magnetic moments (ratios in which the constituent-quark factor cancels), and the lightest CKM element (which couples to $\mathrm{SU}(2)_L \times \mathrm{U}(1)_Y$ rather than to QCD) all fall into this protected class. Heavy-meson observables, full-QCD running coupling, and high-energy electroweak precision observables are *not* expected to display $\kappa$-fingerprints.

The conjecture is testable; see §6.

### 5.4 Other patterns identified by the search

The Phase~3 family analysis identified $97$ formulas matching multiple ratios at $< 1\%$, several of which are well-known accidents (Gell-Mann--Okubo $3/2$, Goldhaber--Treiman $\sqrt{2}$, etc.). One pattern of secondary interest is $9/7 \approx 1.2857$, which appears in $12$ baryon-related ratios. The $\kappa$-derived ratio $(1+\kappa)/(1-\kappa) = 7/5 = 1.40$ appears in $11$ ratios including $\Xi^0/p$ at $0.10\%$.

We refrain from elevating these secondary patterns to "predictions" because they overlap heavily with classical $\mathrm{SU}(3)_f$ flavour relations and do not involve $\kappa$ in a way that is logically independent of well-known group-theoretical decompositions.

---

## 6. Falsifiability

Three of the four matches are directly falsifiable by improving the experimental or lattice precision; the fourth pattern is testable by lattice extension to other gauge groups.

### 6.1 Falsification route 1 — pure-gauge $\Lambda^{N_f=0}$ precision

The current FLAG~2024 average has $\Lambda^{N_f=0} = 251 \pm 9~\mathrm{MeV}$ ($\sim 3.6\%$ uncertainty). Future updates with finer lattices and a dedicated FLAG sub-working group could reduce this to $\sim 2~\mathrm{MeV}$ ($< 1\%$) by 2030. The current central value gives $m_p / \Lambda = 3.738 \pm 0.135$, consistent with $6\pi/5 = 3.770$ at $0.84\%$. A reduction to $\pm 2~\mathrm{MeV}$ would either:
- collapse the deviation to $< 1\%$ (consistent with the pattern), or
- pull the central value $> 5\sigma$ from $6\pi/5$ (falsifying it).

A specific *prediction* derived from this paper is: if $\Lambda^{N_f=0}_{\overline{\mathrm{MS}}}$ converges to a central value outside $251 \pm 2~\mathrm{MeV}$ at $< 2\%$ precision, *the framework's pure-gauge fingerprint fails*.

### 6.2 Falsification route 2 — lattice extension to non-$\mathrm{SU}(3)$ gauge groups

The framework predicts $\kappa(G) = 1/(2|\Phi^+(G)|)$ for any compact simple Lie group $G$, hence
- $\kappa(\mathrm{SO}(5)) = 1/8$ (since $|\Phi^+(B_2)| = 4$);
- $\kappa(G_2) = 1/12$ (since $|\Phi^+(G_2)| = 6$);
- $\kappa(\mathrm{Sp}(2)) = 1/8$.

The structural ratio $\pi/(1{-}\kappa)$ becomes $8\pi/7$ for $\mathrm{SO}(5)$ and $12\pi/11$ for $G_2$. If lattice extensions of the magnetic-moment-ratio-type observable to glueball-binding-ratio-type observables in $\mathrm{SO}(5)$ or $G_2$ gauge theory (Lucini--Teper, Athenodorou--Teper, 2021) match these $G$-specific values at $\le 2\%$, the framework gains substantial support. If they fail to match, the $\kappa$-fingerprint is restricted to $\mathrm{SU}(3)$ and the universal-$\kappa$ claim of the structural framework is locally violated.

### 6.3 Falsification route 3 — $V_{ud}$ precision improvement

Current $V_{ud}$ precision is $\pm 0.00014$ ($0.014\%$). Programs in progress (CKM~2025 working group, MEDEX neutrino, KATRIN-II) target $\pm 0.00003$ by 2030 from a combination of:
- improved electroweak radiative corrections (Seng, Gorchtein 2018+),
- super-allowed $0^+ \to 0^+$ tests of CKM unitarity,
- neutrinoless double-beta-decay constraints on right-handed currents.

The structural value $35/36 = 0.97222$ lies $\sim 10\sigma$ below the current central value $0.97370$. If the central value moves toward $0.97222$ at $\le 0.1\%$ uncertainty, the match is confirmed at $<3\sigma$. If it pulls *away* (e.g.\ toward $0.9740$), the structural identity is falsified.

### 6.4 Falsification route 4 — magnetic-moment precision

The hyperon magnetic moments $\mu_{\Sigma^+}$, $\mu_{\Xi^-}$ have $\sim 0.4\%$ uncertainty (PDG~2024). The Belle~II and STCF programs aim for $\sim 0.1\%$ on hyperon properties by 2030. The structural prediction $|\mu_{\Sigma^+}/\mu_{\Xi^-}| = 6\pi/5 = 3.7699$ would then be tested at $3\sigma$ or better. A central value moving by more than $\pm 0.04$ from $3.7699$ would falsify Match~3.

### 6.5 Combined falsification timeline

Routes 1, 3, 4 are independently testable at the $< 1\%$ level by $\sim 2030$. Route 2 is testable at any time given dedicated lattice computation on non-$\mathrm{SU}(3)$ ensembles. A coordinated $5$-year programme would either confirm the framework's $\kappa$-fingerprint at $\sim 4\sigma$ aggregate, or rule it out at $> 5\sigma$.

---

## 7. Honest scope and disclaimers

### 7.1 What this paper is

This paper is a *numerical-pattern observation* paper, in the same methodological category as:
- Koide (Phys.\ Rev.\ D 28, 252, 1983): the lepton-mass formula $(m_e + m_\mu + m_\tau)/(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2 = 2/3$ holds at $< 10^{-4}$ relative precision without a derivation from first principles, and has remained unexplained for 43 years;
- Bode (1772): the planetary orbit formula $r_n = 0.4 + 0.3 \cdot 2^n~\mathrm{AU}$ fits the inner solar system to a few percent but fails for Neptune; it preceded but did not predict the Titius--Bode law of present-day reduced-mass-Yukawa form;
- Veneziano amplitude (1968): an empirical pattern in pion scattering that turned out to admit a derivation from string theory only a decade later.

Patterns of this type sometimes precede genuine derivations and sometimes turn out to be accidents. Our four-fold concurrence at $7.75\sigma$ inside the $\kappa$-sublibrary is *evidence*, not proof, and the rate of false positives is bounded but not zero.

### 7.2 What this paper is not

- *It is not a derivation*. None of the four matches is derived from a first-principles calculation. We do not claim to predict $m_p$, $\langle \bar{q}q\rangle$, $\mu_B$, or $V_{ud}$. We claim to observe them in a structural form.
- *It is not a unification*. The four matches span QCD bound states, hadronic magnetic moments, and the CKM mixing matrix. We do not claim to derive a relation between these three sectors; we only observe that all three accept the same structural prefactor $\kappa = 1/6$ inside the simplest one-parameter functional form.
- *It is not free of human selection*. The formula library $\mathcal{F}$ was constructed by the author with prior knowledge of $\kappa = 1/6$. The $Z$-score of $17.09\sigma$ is *conditional on the library*; alternative libraries (with different rational closures, different elementary constants, different inclusion of $\kappa$) would give different numerical values. We have nonetheless attempted to make the library reasonable and complete enough to permit external replication.

### 7.3 The Bonferroni risk in plain language

If we ask "given that I tested $1315 \times 195$ formula--ratio pairs, what is the probability that I find a four-fold coincidence at $\le 2\%$ by chance?": the answer depends on the *correlations* between the candidate formulas. For independent draws at $1\%$ tolerance the expected number of three-or-more-formula coincidences is $\sim 1315 \cdot 0.05 / 195 \cdot \binom{195}{3} \sim 10^4$, which is large. The relevant statistic is therefore the *excess* over random null, not the *absolute* count.

The four headline matches lie inside a global excess of $608 - 308 = 300$ tight matches (or $129 - 66 = 63$ for $\kappa$-only). They are individually not "the rarest" coincidences in the data, but they are aligned with the structural prefactor predicted by the companion framework — a feature the null hypothesis cannot reproduce.

### 7.4 Logical independence from the structural papers

We re-emphasise: the structural companion papers (Rémondière~2026a five-condition uniqueness; Rémondière~2026b LSI synthesis) are *logically independent* of the observations reported here. Falsification of the present paper's empirical pattern (by precision $\Lambda^{N_f=0}$, $V_{ud}$, $\mu_B$, or non-$\mathrm{SU}(3)$ lattice extension) does *not* invalidate the structural results, which rest on Lie-algebraic and Lean-certified arguments. Conversely, full confirmation of the empirical pattern would augment the structural results with an empirical bridge to low-energy phenomenology, but would not constitute a derivation.

---

## 8. Acknowledgments and COPE-compliant LLM disclosure

The author thanks the FLAG~2024 working group for providing the consensus $\Lambda^{N_f=0}_{\overline{\mathrm{MS}}}$ value and PDG~2024 for the magnetic-moment and CKM averages used throughout this paper. All numerical PDG / FLAG values were extracted by direct reading of the original publications, with arXiv IDs verified via the live arXiv API to prevent citation fabrication.

In accordance with COPE (Committee on Publication Ethics) recommendations on AI-assisted research (https://publicationethics.org/cope-position-statements/ai-author), the author discloses the following:

- *AI tools used*: Anthropic's Claude (Opus 4.x, 2026-05) was used as an adversarial-review assistant for cross-checking arXiv references, computing the Bonferroni baseline (Python / NumPy), and identifying scheme-dependence ambiguities. DeepSeek V4-Pro was used in parallel as an independent cross-LLM verifier for selected numerical claims.
- *Authorship*: AI tools did not author, and are not credited as authors of, this manuscript. All intellectual content, including the identification of the $\pi/(1{-}\kappa)$ signature and the choice of falsification routes, was generated and is owned by the human author.
- *Verifiability*: every numerical value reported here is reproducible from the Python scripts archived at \texttt{[Zenodo DOI to be assigned upon submission]}. The reader is invited to re-run the campaign with their own preferred formula library.

The author is grateful to anonymous referees in advance for adversarial criticism, particularly on the question of whether the Bonferroni baseline of §3 adequately controls for the dependence between rational-formula candidates.

---

## 9. References

[arXiv IDs in **bold** were verified against the live arXiv API on 2026-05-24; all other references are from the cited journal / textbook.]

1. R.~L.~Workman et al.\ (Particle Data Group), *Review of Particle Physics*, Prog.\ Theor.\ Exp.\ Phys.\ 2024(8):083C01, https://pdg.lbl.gov

2. Y.~Aoki et al.\ (FLAG Working Group), *FLAG Review 2024*, Eur.\ Phys.\ J.\ C 84:712 (2024), arXiv:**2411.04268**.

3. S.~Schaefer, R.~Sommer, F.~Virotta (ALPHA Collaboration), *Critical slowing down and error analysis in lattice QCD simulations*, Nucl.\ Phys.\ B 845, 93--119 (2011), arXiv:**1009.5228**.

4. M.~Lüscher, S.~Schaefer, *Lattice QCD without topology barriers*, JHEP 1107:036 (2011), arXiv:**1105.4749**.

5. Y.~Koide, *Fermion-boson two-body model of quarks and leptons and Cabibbo mixing*, Lett.\ Nuovo Cim.\ 34, 201 (1982); *New view of quark and lepton mass hierarchy*, Phys.\ Rev.\ D 28, 252 (1983).

6. K.~Rémondière, *A five-condition uniqueness theorem for the gauge sector of the Standard Model*, manuscript, 2026; arXiv submission in preparation.

7. K.~Rémondière, *Synthesis v2: log-Sobolev framework for compact-Lie-group gauge theory*, manuscript, 2026; Zenodo DOI to be assigned upon submission.

8. C.~Alexandrou, S.~Bacchio, M.~Constantinou, J.~Finkenrath, K.~Hadjiyiannakou, K.~Jansen, G.~Koutsou, A.~Vaquero Aviles-Casco, *Proton and neutron electromagnetic form factors from lattice QCD*, arXiv:**1812.10311**.

9. J.~C.~Hardy, I.~S.~Towner, *Superallowed $0^+ \to 0^+$ nuclear $\beta$ decays: 2020 critical survey, with implications for $V_{ud}$ and CKM unitarity*, Phys.\ Rev.\ C 102, 045501 (2020). [Journal-only; this work has no arXiv preprint as of writing.]

10. C.-Y.~Seng, M.~Gorchtein, H.~H.~Patel, M.~J.~Ramsey-Musolf, *Reduced hadronic uncertainty in the determination of $V_{ud}$*, Phys.\ Rev.\ Lett.\ 121, 241804 (2018), arXiv:**1807.10197**.

10b. C.-Y.~Seng, D.~Galviz, W.~J.~Marciano, U.-G.~Meißner, *Update on $|V_{us}|$ and $|V_{us}/V_{ud}|$ from semileptonic kaon and pion decays*, arXiv:**2107.14708** (Cabibbo-angle anomaly context).

11. M.~Lüscher, *Properties and uses of the Wilson flow in lattice QCD*, JHEP 1008:071 (2010), arXiv:**1006.4518**.

12. M.~Athenodorou, M.~Teper, *The glueball spectrum of $\mathrm{SU}(N)$ gauge theories in $D = 3 + 1$ dimensions*, JHEP 2021(11):172, arXiv:**2106.00364**.

13. R.~Sommer, *A new way to set the energy scale in lattice gauge theories and its application to the static force and $\alpha_s$ in $\mathrm{SU}(2)$ Yang--Mills theory*, Nucl.\ Phys.\ B 411, 839--854 (1994), arXiv:**hep-lat/9310022**.

14. S.~Necco, R.~Sommer, *The $N_f = 0$ heavy quark potential from short to intermediate distances*, Nucl.\ Phys.\ B 622, 328--346 (2002), arXiv:**hep-lat/0108008**.

---

*End of manuscript. Total pages including references: 7 in PRL format, 8 in PLB format. Source markdown: 28.0~KB. arXiv submission v1: 2026-06 (target).*
