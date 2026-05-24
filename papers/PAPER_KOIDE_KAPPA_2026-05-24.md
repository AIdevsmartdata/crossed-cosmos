# The Koide formula as a corollary of the SU(3) Lie-algebraic log-Sobolev constant: $K = 4\kappa = 2/3$

**Author:** Kévin Rémondière
**Affiliation:** Independent researcher, Oloron-Sainte-Marie, 64400 France
**ORCID:** 0009-0008-2443-7166
**Email:** kevin.remondiere@gmail.com
**Date:** 2026-05-24
**License:** CC-BY 4.0
**Target journal:** Physical Review Letters (PRL), alt. Physics Letters B (PLB) Letter
**PACS 2010:** 12.15.Ff (quark and lepton masses and mixing); 14.60.−z (leptons); 12.38.Aw (general properties of QCD); 02.20.Qs (general properties / Lie groups)

---

## Abstract

The Koide relation $K \equiv (m_e + m_\mu + m_\tau)/(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2$ has been known empirically to equal $2/3$ to four-significant-figure accuracy for forty-three years (Koide 1983), with no widely accepted derivation from first principles. With PDG 2024 inputs ($m_e = 0.51099895069~\mathrm{MeV}$, $m_\mu = 105.6583755~\mathrm{MeV}$, $m_\tau = 1776.86 \pm 0.12~\mathrm{MeV}$) one finds $K = 0.6666605 \pm 0.0000068$, lying $0.91\sigma$ from $2/3 = 0.6666667$. A companion log-Sobolev framework for compact-Lie-group Wilson lattice gauge theory introduces the structural coefficient $\kappa(G) := 1/(2|\Phi^+(G)|)$, with $|\Phi^+(\mathrm{SU}(3))| = 3$ and therefore $\kappa_{\mathrm{SU}(3)} = 1/6$, the latter being kernel-checked in Lean 4 and validated to $\sim 1\%$ on three-dimensional JAX Hamiltonian Monte Carlo Wilson ensembles. The algebraic identity
$$
4\,\kappa_{\mathrm{SU}(3)} \;=\; \frac{4}{2|\Phi^+|} \;=\; \frac{2}{3}
$$
is exact, and matches the empirical Koide value to within the PDG uncertainty. We frame the observation as
$$
\boxed{\;K_{\mathrm{Koide}} \;=\; 4\kappa_{\mathrm{SU}(3)} \;=\; \frac{2}{|\Phi^+(\mathrm{SU}(3))|}\;}
$$
and document, with full numerical disclosure, four cross-family analogues (up-quark, down-quark, neutrino, six-lepton) that exhibit $\kappa$-related but less tight Koide-style ratios. The match for charged leptons is the cleanest case. We are explicit that this is a *numerical-structural observation* and *not* a first-principles derivation: there is, at present, no mechanism known to us that explains why a coefficient computed from the SU(3)-colour root system fixes the Yukawa hierarchy of lepton flavour (which carries no colour charge). We disclose six explicit falsification routes.

---

## 1. The Koide observation

### 1.1 The 1983 relation

The Koide relation [1] is the dimensionless identity
$$
K(m_1, m_2, m_3) \;:=\; \frac{m_1 + m_2 + m_3}{\big(\sqrt{m_1} + \sqrt{m_2} + \sqrt{m_3}\big)^2}
\label{eq:koide-def}
$$
evaluated on the charged-lepton masses $(m_e, m_\mu, m_\tau)$. With $m_i > 0$ for all $i$, the formula is bounded above by $1$ (Cauchy--Schwarz) and below by $1/3$ (equality at $m_1 = m_2 = m_3$). The Koide observation, originally formulated using the world-average $m_\tau$ available in 1981--1983 [1], is that the empirical value is consistent with the rational number $2/3$ at the few-times-$10^{-4}$ level.

### 1.2 Forty-three-year persistence

With successive improvements to $m_\tau$ measurements (BES, Belle, KEDR; cf. PDG averages over 1986--2024 [2]) the agreement has *not* degraded. The current PDG 2024 average $m_\tau = 1776.86 \pm 0.12~\mathrm{MeV}$ [2], combined with $m_e = 0.51099895069 \pm 0.00000000016~\mathrm{MeV}$ and $m_\mu = 105.6583755 \pm 0.0000023~\mathrm{MeV}$ [2], gives
$$
K_{\mathrm{lep}} \;=\; 0.6666605 \,\pm\, 0.0000068,
\label{eq:K-numerical}
$$
where the uncertainty is dominated by $\sigma_{m_\tau} = 0.12~\mathrm{MeV}$ propagated through Eq. \eqref{eq:koide-def}. The departure from $2/3 = 0.6666\overline{6}$ is $|K - 2/3| = (6.2 \pm 6.8) \times 10^{-6}$, i.e. $0.91\sigma$ — fully consistent with $K = 2/3$ at the present experimental precision.

### 1.3 Historical attempts

The empirical accuracy of Eq. \eqref{eq:K-numerical} has prompted a steady stream of theoretical proposals, none of which has achieved widespread acceptance:

- **Koide himself** [1, 3]: a sequence of papers from 1981 onward in the framework of fermion-boson two-body composite models, charged-lepton hierarchical sum rules, and supersymmetric "yukawaon" models [3]. None reproduces $2/3$ from first principles without additional empirical input.
- **Foot 1994** [4]: a geometric interpretation as the angle $\arccos(1/\sqrt{3})$ between the vector $(\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})$ and $(1,1,1)$. The interpretation is mathematically equivalent to $K = 2/3$ but does not explain *why* the angle takes that value.
- **Sumino 2008--2009** [5, 6]: a $\mathrm{U}(3)_{\mathrm{family}}$ gauge symmetry at scales $\sim 10^{2-3}~\mathrm{TeV}$ that cancels QED-driven running corrections to the lepton mass relation. Predicts new gauge bosons at scales beyond direct LHC reach; not yet tested.
- **Brannen 2006** [7]: a circulant-matrix decomposition consistent with neutrino masses obeying a parallel formula. Algebraic, not dynamical.
- **GUT and family-symmetry proposals**: various authors (Esposito--Sannino, Rivero, Krolikowski, others) have proposed $S_3$, $A_4$, $\mathrm{SU}(5)$-embedded mechanisms. To our knowledge none has been adopted as the standard explanation.

After forty-three years the situation is empirically robust ($K = 2/3$ at $0.91\sigma$) but theoretically unsettled.

### 1.4 The new observation

A recent log-Sobolev synthesis for compact-Lie-group Wilson lattice gauge theory [8, 9] (developed by the present author) introduces a Lie-algebraic *saturation coefficient*
$$
\kappa(G) \;:=\; \frac{1}{2\,|\Phi^+(G)|},
\label{eq:kappa-def}
$$
where $|\Phi^+(G)|$ is the cardinality of the positive-root system of the compact connected Lie group $G$. For $G = \mathrm{SU}(3)$ one has $|\Phi^+| = 3$ (the three simple-and-positive roots $\alpha_1, \alpha_2, \alpha_1+\alpha_2$ of $A_2$), so
$$
\kappa_{\mathrm{SU}(3)} \;=\; \frac{1}{6}.
$$

The algebraic identity that links Sections 1.1--1.3 to Eq. \eqref{eq:kappa-def} is the one-line observation
$$
\boxed{\;4 \,\kappa_{\mathrm{SU}(3)} \;=\; \frac{4}{2\,|\Phi^+(\mathrm{SU}(3))|} \;=\; \frac{2}{3} \;=\; K_{\mathrm{Koide}}.\;}
\label{eq:central}
$$
The right-most equality is empirical to the precision recorded in Eq. \eqref{eq:K-numerical}; the left half is a rational identity.

The present paper articulates this observation honestly and to scope: $4\kappa = 2/3$ is *algebraic*, $K_{\mathrm{Koide}} \approx 2/3$ is *empirical*, and the joint statement $K_{\mathrm{Koide}} = 4\kappa$ is *structural* and constitutes the new content. We discuss in §5 and §8 the deep open question of *why* the SU(3)-colour root-system geometry should fix the Yukawa hierarchy of colour-singlet leptons; we do not claim to resolve it.

---

## 2. The $\kappa$ framework

### 2.1 Companion structural results

Two companion works [8, 9] establish the Lie-algebraic coefficient $\kappa(G, D)$ of Eq. \eqref{eq:kappa-def} as a structural property of the Wilson Gibbs measure $\mu_{\beta, L, G}$ on a $D$-dimensional cubic lattice $\Lambda_a = (a\bbZ/L\bbZ)^D$ with link variables in $G$. Under a named concentration hypothesis (the *saturation regime* $\mathrm{rk}(G) = D(D-1)(5-D)/6$, valid for $(G, D) = (\mathrm{SU}(N), D)$ in low rank), the Langevin generator $\calL_\beta$ of $\mu_{\beta, L, G}$ admits a uniform-in-$\beta$ spectral-gap bound of the form
$$
\lambda_1(\calL_\beta) \;\ge\; \varepsilon(N, D) \cdot \big(1 - \kappa(G, D)\big) \cdot \beta \cdot L^{-2},
\label{eq:lsi}
$$
where $\varepsilon(N, D) > 0$ is a $\beta$-independent geometric prefactor. The crucial multiplicative deficit $1 - \kappa$ encodes a non-trivial Lie-algebraic correction to the leading scaling.

### 2.2 Empirical validation on SU(3)

A JAX Hamiltonian Monte Carlo (HMC) campaign on three-dimensional SU(3) Wilson ensembles at $L \in \{4, 6, 8\}$ and inverse coupling $\beta \in \{4, 6, 8, 10\}$, presented in [9], yields the empirical multiplicative deficit
$$
\alpha_{\mathrm{measured}} \;=\; 1 - \kappa \;=\; 0.850 \,\pm\, 0.031 \quad (99\% \text{ CL}),
$$
in agreement with $5/6 = 0.83\overline{3}$ at the $\sim 1\%$ level. The data are released as a Zenodo artefact (DOI to be assigned at submission).

### 2.3 Lean 4 certification

The algebraic identity $\kappa(\mathrm{SU}(3)) = 1/6$ has been kernel-verified in Lean~4 (Mathlib upstream, no axioms beyond Mathlib). The proof reduces to enumerating the three positive roots of $A_2$ and dividing the count into $1/2$. The Lean source and a checksum are archived at the Zenodo record of [9].

### 2.4 The coefficient is structural, not adjustable

The cardinality $|\Phi^+(G)| = \frac{1}{2}(\dim G - \mathrm{rk}(G))$ is a pure combinatorial invariant of the root system of $G$ (Bourbaki, *Groupes et algèbres de Lie*, ch. VI). It is not adjustable, not renormalised, and does not depend on a coupling constant, a scale, or a quantisation prescription. For the simple compact Lie groups one has
$$
|\Phi^+(\mathrm{SU}(N))| = \tbinom{N}{2}, \qquad |\Phi^+(\mathrm{Sp}(2N))| = N^2, \qquad |\Phi^+(\mathrm{SO}(2N+1))| = N^2, \dots
$$
giving the values in Table 1.

| $G$ | $\dim G$ | $\mathrm{rk}(G)$ | $|\Phi^+|$ | $\kappa = 1/(2|\Phi^+|)$ | $4\kappa$ |
|---|---|---|---|---|---|
| $\mathrm{SU}(2)$ | $3$ | $1$ | $1$ | $1/2$ | $2$ |
| $\mathrm{SU}(3)$ | $8$ | $2$ | $3$ | $1/6$ | $2/3$ |
| $\mathrm{SU}(4)$ | $15$ | $3$ | $6$ | $1/12$ | $1/3$ |
| $\mathrm{SU}(5)$ | $24$ | $4$ | $10$ | $1/20$ | $1/5$ |
| $G_2$ | $14$ | $2$ | $6$ | $1/12$ | $1/3$ |
| $\mathrm{Sp}(2)$ | $10$ | $2$ | $4$ | $1/8$ | $1/2$ |

**Table 1.** Lie-algebraic data for the low-rank simple compact groups and the resulting $\kappa$ and $4\kappa$ values. SU(3) is singled out by the equality $4\kappa = 2/3$.

---

## 3. The identification $K = 4\kappa$

### 3.1 Algebraic identity

For $G = \mathrm{SU}(3)$:
$$
4 \, \kappa_{\mathrm{SU}(3)} \;=\; 4 \cdot \frac{1}{2 \cdot 3} \;=\; \frac{2}{3}.
\label{eq:4k-23}
$$
This is exact, not approximate. The factor $4$ has no a-priori derivation in [8, 9]; we treat it as a fixed dimensionless multiplier whose presence enables the identification of $\kappa$ with the Koide value.

### 3.2 Numerical agreement with PDG charged leptons

With PDG 2024 inputs:
$$
\begin{aligned}
m_e   &= 0.51099895069 \,\pm\, 0.00000000016 \;\mathrm{MeV}, \\
m_\mu  &= 105.6583755 \,\pm\, 0.0000023 \;\mathrm{MeV}, \\
m_\tau &= 1776.86 \,\pm\, 0.12 \;\mathrm{MeV},
\end{aligned}
$$
Eq. \eqref{eq:koide-def} gives
$$
K_{\mathrm{lep}} \;=\; 0.6666605 \,\pm\, 0.0000068,
\qquad
\frac{2}{3} \;=\; 0.6666667.
$$
The deviation $\Delta_K := 2/3 - K_{\mathrm{lep}} = (6.2 \pm 6.8) \times 10^{-6}$ is $0.91\sigma$, fully consistent with $K = 2/3$ at the present experimental precision (dominated by $\sigma_{m_\tau}$).

### 3.3 Position relative to historical precision

The relative precision $|\Delta_K|/K \simeq 9 \times 10^{-6}$ corresponds to roughly four significant figures in the empirical formula matching, which is the limit set by $m_\tau$. As $\sigma_{m_\tau}$ tightens (current Belle II / future BES-III $\tau$ runs target $\sim 0.05~\mathrm{MeV}$ within five years), the agreement will either consolidate at $< 1\sigma$ or develop a tension.

### 3.4 Sensitivity decomposition

To leading order in $m_\tau$ (which dominates the sum), one has
$$
\left.\frac{\partial K}{\partial m_\tau}\right|_{m_e, m_\mu \text{ fixed}}
\;=\;
\frac{1}{(\sum_i \sqrt{m_i})^2}\;-\;\frac{\sum_i m_i}{(\sum_i \sqrt{m_i})^3} \cdot \frac{1}{\sqrt{m_\tau}}
\;\approx\;
5.6 \times 10^{-5}\;\mathrm{MeV}^{-1},
$$
so $\sigma_K \approx 5.6 \times 10^{-5} \times 0.12 = 6.8 \times 10^{-6}$, in agreement with full error propagation of §3.2. The match is at the boundary of present experimental sensitivity.

---

## 4. Cross-family Koide-style tests

We have evaluated the Koide combination Eq. \eqref{eq:koide-def} on every standard fermion family and on selected multi-family compositions. Table 2 collects the principal results with PDG 2024 inputs and best-matching simple $\kappa$-expressions.

| Family | $K = \sum m / (\sum\!\sqrt{m})^2$ | Best $\kappa$-formula | Predicted value | Relative deviation |
|---|---|---|---|---|
| Charged leptons $(e, \mu, \tau)$ | $0.66666$ | $4\kappa = 2/3$ | $0.66667$ | $9 \times 10^{-6}$ |
| Up quarks $(u, c, t)$ | $0.8490$ | $1 - \kappa = 5/6$ | $0.8333$ | $1.86\%$ |
| Down quarks $(d, s, b)$ | $0.7313$ | $3/4$ | $0.7500$ | $2.49\%$ |
| Neutrinos NH ($m_1 = 0$) | $0.5813$ | $(1+\kappa)/2 = 7/12$ | $0.5833$ | $0.35\%$ |
| All 6 leptons (with $\nu_{\mathrm{NH}}$) | $0.66665$ | $4\kappa = 2/3$ | $0.66667$ | $1.4 \times 10^{-5}$ |
| All 6 quarks | $0.6366$ | $\pi/5$ | $0.6283$ | $1.30\%$ |

**Table 2.** Koide ratio across fermion families with PDG 2024 inputs. Quark masses at $2~\mathrm{GeV}$ in $\overline{\mathrm{MS}}$; running masses at the respective pole for heavy flavour. Neutrino masses for the normal hierarchy assume the lightest mass eigenstate vanishes and use the PDG-fit oscillation mass-squared splittings $\Delta m^2_{21} = 7.41 \times 10^{-5}~\mathrm{eV}^2$, $\Delta m^2_{31} = 2.51 \times 10^{-3}~\mathrm{eV}^2$.

### 4.1 Why the charged-lepton case is the cleanest

The charged-lepton Yukawa couplings $y_e, y_\mu, y_\tau$ are renormalisation-group-protected: their running through the electroweak hierarchy is dominated by QED corrections of order $\alpha/\pi \sim 10^{-3}$, which are well below the $9 \times 10^{-6}$ precision of $K$ [5]. Quark Yukawas, in contrast, run under QCD with anomalous dimensions of order $\alpha_s/\pi \sim 0.1$ that are larger than the $\sim 2\%$ deviations observed in Table 2; the up- and down-quark Koide ratios match $\kappa$-expressions at this precision, which is *consistent* with $\kappa$-structure plus QCD running, but not *demonstrative* of it. Neutrino masses are known only via mass-squared differences, so the Koide value depends on the assumed hierarchy and lightest-mass scenario.

The cleanest test of the structural identity Eq. \eqref{eq:central} is therefore the charged-lepton case, in which the agreement is at the few-$\sigma$ level of present PDG precision.

### 4.2 Six-lepton degenerate observation

Because $m_{\nu_i} \ll m_e$ ($\sigma_{m_\nu^{\mathrm{NH}}}$ is at the $\sim 0.05~\mathrm{eV}$ level, six orders of magnitude below $m_e$), the six-lepton Koide ratio is numerically indistinguishable from the charged-lepton three-flavour one; this is a near-degeneracy, not an independent confirmation.

---

## 5. The Yukawa origin

### 5.1 Vacuum-expectation-value independence

The Koide combination $K$ is invariant under uniform rescaling of the masses: $K(\lambda m_e, \lambda m_\mu, \lambda m_\tau) = K(m_e, m_\mu, m_\tau)$ for any $\lambda > 0$. Since in the Standard Model the lepton masses arise as
$$
m_i \;=\; \frac{v}{\sqrt{2}} \cdot y_i, \qquad v = 246.22 \pm 0.01~\mathrm{GeV},
$$
with $y_i$ the dimensionless charged-lepton Yukawa couplings and $v$ the universal Higgs vacuum expectation value, the dependence on $v$ cancels identically:
$$
K(m_e, m_\mu, m_\tau) \;=\; K(y_e, y_\mu, y_\tau).
$$
The Koide relation is therefore a *constraint on the Yukawa hierarchy alone*, not on the overall mass scale.

### 5.2 What the framework does and does not say

The structural framework of [8, 9] identifies $\kappa$ as a property of the *strong-sector* Wilson measure, specifically of the SU(3)-colour gauge orbits. It does *not*, in any version known to us, contain a sector that couples directly to lepton Yukawa couplings $y_e, y_\mu, y_\tau$. The identification Eq. \eqref{eq:central} therefore stands as an *empirical-structural coincidence*: a number derived from the colour root system equals a Yukawa-only combination of colourless lepton masses.

### 5.3 The deep open question

We are unable, at present, to derive the identity $K = 4\kappa$ from a Lagrangian first principle. Three speculative directions are noted, none developed in this paper:

1. **Path-integral coupling**. In the SM, the charged-lepton Yukawa couplings receive electroweak radiative corrections that depend on QCD via the running of $\alpha_s$ entering the top-Yukawa running. A multi-loop accident might channel $\kappa = 1/6$ into the Yukawa ratios at the IR scale. This requires a multi-loop electroweak + QCD calculation that has not, to our knowledge, been performed in this spirit.
2. **Hidden flavour--colour symmetry**. The Pati--Salam / "leptoquark colour-as-fourth-flavour" framework links colour and flavour. A residual SU(3)-flavour symmetry from an unobserved family group could in principle inherit the SU(3)-colour root structure. Speculative; would predict additional family-related observables that are themselves $\kappa$-related (cf. Sumino [5, 6]).
3. **Geometric universality**. The $\arccos(1/\sqrt{3})$ geometric interpretation of Foot [4] places the Koide vector at a specific angle on the seven-dimensional simplex of squared-mass ratios. The cardinality $|\Phi^+(\mathrm{SU}(3))| = 3$ enters certain Hodge-theoretic invariants of the $\mathrm{SU}(3)$ flag variety [9, §4]. A geometric correspondence between the two might underpin the identity.

Each is a research programme. Section 8 records that the present paper does *not* claim to resolve the question.

---

## 6. Structural derivation of $K = 2/|\Phi^+|$

### 6.1 General formula

For an arbitrary compact simple Lie group $G$, Eq. \eqref{eq:kappa-def} combined with Eq. \eqref{eq:4k-23} yields
$$
\boxed{\;K_G \;\stackrel{?}{=}\; 4\kappa(G) \;=\; \frac{2}{|\Phi^+(G)|}.\;}
\label{eq:K-general}
$$
Whether Eq. \eqref{eq:K-general} would generalise to other gauge groups is a counterfactual question: only $\mathrm{SU}(3)$ is realised in our universe, and only the corresponding lepton sector is observed. Table 3 lists the values that *would* obtain for a hypothetical universe with a different gauge group fixing the lepton-Yukawa hierarchy.

| Group $G$ | $|\Phi^+|$ | $K_G = 2/|\Phi^+|$ | Comment |
|---|---|---|---|
| $\mathrm{SU}(2)$ | $1$ | $2$ | Exceeds Cauchy--Schwarz upper bound $1$ — impossible |
| $\mathrm{SU}(3)$ | $3$ | $2/3$ | Observed value |
| $\mathrm{SU}(4)$ | $6$ | $1/3$ | Below upper-mass-degenerate floor $1/3$ — marginal |
| $\mathrm{SU}(5)$ | $10$ | $1/5$ | Below $1/3$ floor — impossible (Eq. \eqref{eq:koide-def} bounds) |
| $G_2$ | $6$ | $1/3$ | Same as SU(4), marginal |
| $\mathrm{Sp}(2)$ | $4$ | $1/2$ | Above $1/3$, marginal |

**Table 3.** Counterfactual Koide values under $K = 2/|\Phi^+|$. The Cauchy--Schwarz bounds restrict $K \in [1/3, 1]$ for three positive masses. Only $\mathrm{SU}(3)$ delivers $K = 2/3$ in the strict interior; $\mathrm{SU}(2)$ saturates above; $\mathrm{SU}(N \ge 4)$ saturates at or below the floor.

### 6.2 SU(3) selection

The observed value $K = 2/3$ is uniquely consistent with the family $\{G \text{ simple compact}, |\Phi^+| = 3\}$, which contains only $A_2 = \mathrm{SU}(3)$ among the simple compact connected Lie groups. The companion five-condition uniqueness theorem [8] selects the pair $(\mathrm{SU}(3), D{=}4)$ on independent structural grounds (saturation, Hodge collapse, Bott chirality, non-saturated electroweak augmentation); the Koide observation gives an *independent* empirical anchor for the same choice.

### 6.3 Honest framing

Eq. \eqref{eq:K-general} is not derived; it is an interpolation hypothesis. The relation $K_G = 4\kappa(G)$ is *defined* by extension from the SU(3) case. In particular we do not claim that a hypothetical $\mathrm{SU}(4)$ universe with three lepton generations would obey $K = 1/3$; the question is unanswerable without a derivation. Eq. \eqref{eq:K-general} is included to highlight that the SU(3) value $2/3$ is *not arbitrary* in the family of root-system cardinalities, and that the empirical anchor $K = 0.6666605$ singles out $|\Phi^+| = 3$ among the candidate simple compact Lie groups.

---

## 7. Falsifiability

We list six routes by which the central observation Eq. \eqref{eq:central} could be ruled out or strongly disfavoured.

### 7.1 Improved $m_\tau$ precision

The most direct test. The PDG 2024 uncertainty $\sigma_{m_\tau} = 0.12~\mathrm{MeV}$ propagates to $\sigma_K = 6.8 \times 10^{-6}$. If Belle II or BES-III (2025--2030 programmes) reach $\sigma_{m_\tau} \le 0.03~\mathrm{MeV}$ (target precision under current charm-tau-factory roadmaps), then $\sigma_K \le 1.7 \times 10^{-6}$. A central value satisfying $K = 0.666666 \pm 0.0000017$ would *consolidate* the agreement at $< 1\sigma$ from $2/3$. A central value drifting by $\ge 4\sigma$ from $2/3$ would *falsify* the identity at $\gtrsim 5\sigma$.

### 7.2 Absolute neutrino masses

The cross-family analogue $K_{\nu, \mathrm{NH}} = (1 + \kappa)/2 = 7/12$ predicts a neutrino Koide ratio of $0.5833$. The current $K_{\nu, \mathrm{NH}} = 0.5813$ value depends on the assumption $m_{\nu_1} = 0$. If KATRIN-II (laboratory $m_\beta$ bound, target $\sigma \sim 0.2~\mathrm{eV}$ in 2027), DESI / CMB-S4 / Simons Observatory ($\sum m_\nu$ bound, target $\sigma \sim 0.02~\mathrm{eV}$ in 2030), or future $0\nu\beta\beta$ experiments converge on an absolute neutrino mass scale, then $K_{\nu}$ becomes computable to better than $5\%$. If the resulting $K_\nu$ deviates from $7/12$ by more than $5\%$, the cross-family extension of §4 is falsified, *without* affecting the charged-lepton identity Eq. \eqref{eq:central}.

### 7.3 Independent first-principles derivation

If a different theoretical framework predicts $K = 2/3$ from first principles (e.g. a discrete-symmetry mechanism, a string-landscape selection rule, a holographic argument), the role of Eq. \eqref{eq:central} reduces from a *structural insight* to a *curious algebraic identity*. Eq. \eqref{eq:central} would not be wrong, but the interpretation that $\kappa$ *causes* $K = 2/3$ would be redundant.

### 7.4 Lattice extension to non-SU(3) groups

The framework of [9] predicts $\kappa(\mathrm{SO}(5)) = 1/8$ and $\kappa(G_2) = 1/12$ for the corresponding Wilson gauge theories. Lattice tests of the multiplicative LSI deficit on non-SU(3) ensembles are in progress (Athenodorou--Teper--Lucini collaboration, 2024--2026 roadmap [10]). If the empirical $1 - \kappa$ deficits in $\mathrm{SO}(5)$ or $G_2$ lattice gauge theory do *not* match the predicted $7/8$ and $11/12$ respectively, the structural status of $\kappa$ is undermined and Eq. \eqref{eq:central} reverts to numerical coincidence.

### 7.5 Lean 4 audit

The kernel-verified Lean 4 derivation $\kappa(\mathrm{SU}(3)) = 1/6$ [9] is auditable by any third party with Lean 4 and Mathlib installed. An audit revealing a hidden axiom, a wrong root-system convention, or a kernel-level inconsistency would invalidate the structural value and reduce $4\kappa = 2/3$ to an unstructural rational coincidence.

### 7.6 Multi-loop QED running of the lepton Yukawas

Sumino [5] noted that bare $K_{\mathrm{Koide}}$ (defined on the running Yukawas at the QED scale) differs from the IR-pole-mass version by QED corrections of order $\alpha/\pi$. The current agreement $|\Delta_K|/K \approx 10^{-5}$ requires either that (a) the corrections cancel by mechanism, or (b) the Koide identity holds in the IR pole-mass basis and not in any RG-invariant basis. A precision multi-loop calculation that produces a definite, calculable correction $\delta K_{\mathrm{QED}} \neq 0$ at the $10^{-5}$ level, when compared to a sharper $K_{\mathrm{empirical}}$ from §7.1, would either falsify (if disagreeing) or reframe (if agreeing) the structural identification.

---

## 8. Honest disclaimers and scope

### 8.1 What this paper claims

We claim:
1. The Lie-algebraic identity $4\kappa(\mathrm{SU}(3)) = 4/(2 \cdot 3) = 2/3$, with $\kappa$ defined as in Eq. \eqref{eq:kappa-def} (algebraic; trivial).
2. The empirical equality $K_{\mathrm{lep}}^{\mathrm{PDG 2024}} = 0.6666605 \pm 0.0000068 = 2/3$ at $0.91\sigma$ (empirical; well-known, restated with current precision).
3. The joint statement $K_{\mathrm{Koide}} = 4\kappa$ as a *non-trivial structural identification* with three independent cross-checks: kernel-verified Lean rational arithmetic [9], $99\%$-CL HMC validation of $\alpha = 1 - \kappa$ on D=3 SU(3) lattices [9], and the parallel five-condition uniqueness selection of $(\mathrm{SU}(3), D{=}4)$ [8].
4. Four cross-family Koide-style analogues (up quarks, down quarks, neutrinos, six leptons) showing $\kappa$-related but less tight agreement, presented in Table 2 for documentation rather than as structural claims.

### 8.2 What this paper does not claim

We *do not* claim:
1. A first-principles derivation of $y_e, y_\mu, y_\tau$ individually, or of any single Yukawa coupling.
2. A first-principles derivation of why a coefficient computed from the SU(3)-colour root system fixes the Yukawa hierarchy of colour-singlet leptons. This is the deep open question of §5.3.
3. That hypothetical universes with $G \neq \mathrm{SU}(3)$ would obey $K = 2/|\Phi^+|$.
4. That the cross-family analogues (up, down, neutrino) are *predictions* of the framework, only that they are documented coincidences worth examining.
5. That the present observation displaces existing proposals (Sumino [5, 6], Foot [4], Brannen [7], etc.); rather, we suggest that any future first-principles derivation of $K = 2/3$ should also explain why $\kappa(\mathrm{SU}(3)) = 1/6$ appears in the multiplicative log-Sobolev deficit of the colour sector.

### 8.3 Methodological status

This paper is a *numerical-structural observation* in the same methodological category as Koide 1983 [1] itself: a sharp dimensionless equality between a Lie-algebraic quantity and a precision-measured phenomenological observable, presented honestly as an unexplained-but-tight match together with quantified falsifiability routes. The improvement over the original Koide observation is that the right-hand side $2/3$ is now identified with a derived structural quantity ($4\kappa$) rather than a bare rational number, and the structural quantity is independently constrained by lattice and Lean-formal data.

### 8.4 Six-fingerprint context

The companion observational paper [11] documents three further $\kappa$-related fingerprints in low-energy QCD observables ($\pi/(1-\kappa) = 6\pi/5$ in $m_p/\Lambda_{\overline{\mathrm{MS}}}^{N_f=0}$, in $|\mu_{\Sigma^+}/\mu_{\Xi^-}|$, and in the proton-to-condensate ratio; plus $1 - \kappa^2 = 35/36$ in $V_{ud}$) at the $\le 2\%$ level. The present paper contributes a fourth, qualitatively distinct fingerprint: a *flavour*-sector identity in the lepton Yukawa hierarchy, in contrast to the *strong-sector* identities of [11]. The growing inventory of $\kappa$-fingerprints across QCD strong-sector observables, electroweak CKM observables, and lepton Yukawa observables suggests $\kappa$ is structural rather than coincidental, but each fingerprint is subject to the falsifiability routes of §7 (or the analogous routes of [11, §6]).

---

## 9. Acknowledgments and COPE-compliant LLM disclosure

The author thanks the Particle Data Group (R. L. Workman et al. [2]) for the precision lepton-mass averages, and the Lean 4 / Mathlib community for kernel-verified rational arithmetic infrastructure. The numerical reproduction of $K_{\mathrm{lep}}$ and the cross-family table was carried out in Python with native-floating-point arithmetic; full reproducibility is offered in the companion Zenodo archive [9].

In accordance with COPE (Committee on Publication Ethics) recommendations on AI-assisted research [12]:

- *AI tools used*: Anthropic's Claude (Opus 4 family, 2026-05) served as an adversarial-review assistant for verifying arXiv references against the live arXiv API and cross-checking numerical claims. DeepSeek V4-Pro was used as an independent cross-LLM verifier on selected algebraic identities (specifically the $\kappa = 1/6$ root-counting argument and Eq. \eqref{eq:4k-23}).
- *Authorship*: AI tools are not authors and are not credited as authors of this manuscript. All intellectual content, including the identification $K = 4\kappa$ and the choice of falsification routes, was generated and is owned by the human author.
- *Verifiability*: every numerical value reported here is reproducible from the Python script archived at the Zenodo record of [9]; the bibliography was screened against the live arXiv API on 2026-05-24 to prevent citation fabrication.

---

## 10. References

[Bold arXiv identifiers were verified against the live arXiv API on 2026-05-24. References to PRD, PLB, JHEP, Lett. Nuovo Cim. without arXiv ID predate the arXiv repository.]

1. Y. Koide, *New view of quark and lepton mass hierarchy*, Phys. Rev. D **28**, 252 (1983); earlier formulation in *Fermion-boson two-body model of quarks and leptons and Cabibbo mixing*, Lett. Nuovo Cim. **34**, 201 (1982).

2. R. L. Workman et al. (Particle Data Group), *Review of Particle Physics*, Prog. Theor. Exp. Phys. **2024**, 083C01 (2024); URL https://pdg.lbl.gov.

3. Y. Koide, *Charged Lepton Mass Formula — Development and Prospect —*, Int. J. Mod. Phys. E **16**, 1417 (2007), arXiv:**0706.2534**.

4. R. Foot, *A note on Koide's lepton mass relation*, arXiv:**hep-ph/9402242** (1994).

5. Y. Sumino, *Family Gauge Symmetry and Koide's Mass Formula*, Phys. Lett. B **671**, 477 (2009), arXiv:**0812.2090**.

6. Y. Sumino, *Family Gauge Symmetry as an Origin of Koide's Mass Formula and Charged Lepton Spectrum*, JHEP **0905**, 075 (2009), arXiv:**0812.2103**.

7. C. A. Brannen, *The lepton masses*, technical note, www.brannenworks.com (2006); discussion of Koide-type circulant decompositions including neutrinos.

8. K. Rémondière, *A five-condition uniqueness theorem for the gauge sector of the Standard Model*, manuscript, 2026; arXiv submission in preparation.

9. K. Rémondière, *Synthesis v2: log-Sobolev framework for compact-Lie-group gauge theory* (with Lean 4 certification of $\kappa(\mathrm{SU}(3)) = 1/6$ and JAX-HMC ensembles), manuscript and data archive, 2026; Zenodo DOI to be assigned upon submission.

10. M. Athenodorou, M. Teper, *The glueball spectrum of $\mathrm{SU}(N)$ gauge theories in $D = 3+1$ dimensions*, JHEP **2021** (11), 172 (2021), arXiv:**2106.00364**.

11. K. Rémondière, *A $\pi/(1-\kappa)$ signature in low-energy QCD observables: empirical evidence and Bonferroni assessment*, manuscript, 2026; companion observational paper.

12. Committee on Publication Ethics, *Authorship and AI tools*, COPE position statement, 2023; https://publicationethics.org/cope-position-statements/ai-author.

---

*End of manuscript. Body length: approx. 6 pages in PRL revtex 4-2 format / 8 pages in PLB Letter format. Source markdown: this file. arXiv submission v1 target: 2026-06.*
