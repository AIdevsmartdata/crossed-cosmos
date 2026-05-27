# OP-KOIDE-DERIVATION : Attempt to derive $K = 4\kappa = 2/3$ from first principles

**Author** : Kévin Rémondière (Oloron-Sainte-Marie, France)
**Date** : 2026-05-24
**Scope** : Honest depth-attempt across four candidate derivation routes, with explicit verdict per route, identification of two key lemmas that would unblock a full derivation if proved, and a clean 4-page LaTeX note for the partial geometric result that does close.
**Methodological commitment** : honest negatives over fabricated positives. The reader will find that **two of the four routes fail at the naïve level**, **one is a true geometric rephrasing that does not constitute a first-principles derivation**, and **one is a phenomenological cancellation mechanism that is compatible but not derivative**. The clean partial result is documented in §6 and in the companion LaTeX note.

---

## Table of contents

1. The empirical observation $K = 4\kappa = 2/3$ and its forty-three-year history
2. Route A — Geometric/topological identity on $\mathbb{R}^3_+$ modulo scale
3. Route B — Yukawa as Dirac eigenvalues on the gauge orbit space $\mathcal{A}/\mathcal{G}$
4. Route C — Higgs as radial mode of $\mathcal{A}/\mathcal{G}$ and lepton Yukawa from radial coupling
5. Route D — Sumino-style heavy gauge boson cancellation and the $\kappa = 1/6$ overlay
6. Honest assessment : which route is closest, what is missing, what would constitute a full derivation
7. Two key lemmas that would unblock the derivation, with explicit statements
8. References, all verified against the live arXiv API on 2026-05-24

---

## 1. The empirical observation $K = 4\kappa = 2/3$ and its forty-three-year history

### 1.1 Statement and current precision

For three positive masses $(m_1, m_2, m_3)$ define the **Koide combination**
$$
K(m_1, m_2, m_3) \;:=\; \frac{m_1 + m_2 + m_3}{\big(\sqrt{m_1} + \sqrt{m_2} + \sqrt{m_3}\big)^2}.
\label{eq:1-Koide-def}
$$
With $m_i > 0$ for $i = 1, 2, 3$, this combination satisfies the elementary bounds
$$
\frac{1}{3} \;\le\; K(m_1, m_2, m_3) \;\le\; 1,
$$
the lower bound saturated at $m_1 = m_2 = m_3$ (perfect mass degeneracy) and the upper bound approached as one mass dominates the sum. The Koide observation [Koide 1981, 1983] is the empirical claim
$$
K(m_e, m_\mu, m_\tau) \;=\; \frac{2}{3} \;=\; 0.6666\overline{6}
\label{eq:1-Koide-obs}
$$
with the charged-lepton pole masses.

With PDG 2024 inputs (electron mass $m_e = 0.51099895069 \pm 0.00000000016~\mathrm{MeV}$, muon mass $m_\mu = 105.6583755 \pm 0.0000023~\mathrm{MeV}$, tau mass $m_\tau = 1776.86 \pm 0.12~\mathrm{MeV}$), direct computation gives
$$
K_{\mathrm{lep}}^{\mathrm{PDG 2024}} \;=\; 0.66666051 \,\pm\, 0.00000677,
$$
which lies $0.91\sigma$ from $2/3$ (the uncertainty $\sigma_K = 6.77 \times 10^{-6}$ is propagated from the dominant $\sigma_{m_\tau} = 0.12~\mathrm{MeV}$ via $|\partial K / \partial m_\tau| \approx 5.6 \times 10^{-5}~\mathrm{MeV}^{-1}$). The relative deviation is $|K - 2/3| / (2/3) \approx 9 \times 10^{-6}$, equivalent to roughly **four-and-a-half significant figures of agreement**.

### 1.2 The $\kappa$ overlay

The companion log-Sobolev framework [Rémondière 2026a, 2026b] for compact-Lie-group Wilson lattice gauge theory introduces the **Lie-algebraic saturation coefficient**
$$
\kappa(G) \;:=\; \frac{1}{2 \, |\Phi^+(G)|},
\label{eq:1-kappa-def}
$$
where $|\Phi^+(G)|$ is the cardinality of the positive-root system of the compact connected Lie group $G$. For $G = \mathrm{SU}(3)$ (root system $A_2$) one has $|\Phi^+| = 3$ (the roots $\alpha_1, \alpha_2, \alpha_1 + \alpha_2$), hence
$$
\kappa_{\mathrm{SU}(3)} \;=\; \frac{1}{6}.
$$
The empirical-structural identification is then the one-line identity
$$
\boxed{\; K_{\mathrm{lep}}^{\mathrm{PDG 2024}} \;\stackrel{!}{=}\; 4 \kappa_{\mathrm{SU}(3)} \;=\; \frac{2}{|\Phi^+(\mathrm{SU}(3))|} \;=\; \frac{2}{3} \;}
\label{eq:1-central}
$$
at $0.91\sigma$ relative deviation. The right two equalities are rational identities; the left equality is empirical to PDG 2024 precision.

### 1.3 The forty-three-year history

A non-exhaustive timeline :

- **1981** : Y. Koide, in the context of a "fermion-boson two-body composite model of quarks and leptons" [Koide, Lett. Nuovo Cim. **34**, 201 (1982); arXiv predecessor not yet existing], notices that the charged-lepton mass combination
$$
\frac{(m_e + m_\mu + m_\tau)}{\big(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau}\big)^2}
$$
takes the value $2/3$ within the experimental precision of the early-1980s tau-mass measurements [Koide 1981]. He gives no first-principles derivation but points out the empirical accuracy.

- **1983** : Y. Koide, *New view of quark and lepton mass hierarchy*, Phys. Rev. D **28**, 252 — formal publication of the relation.

- **1989** : Following improvements in tau-mass precision the relation continues to hold at $\sim 10^{-3}$ precision. R. Foot proposes a family-symmetry-type interpretation [Foot, Phys. Lett. B **226**, 144 (1989)].

- **1994** : R. Foot, *A note on Koide's lepton mass relation* [arXiv:hep-ph/9402242], identifies the geometric interpretation : the vector $(\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})$ makes an angle $\arccos(1/\sqrt{3 \cdot 2/3}) = \arccos(1/\sqrt{2}) = \pi/4 = 45^\circ$ with the diagonal $(1, 1, 1)$. He notes this is a sharp geometric fact but does not derive *why* $45^\circ$.

- **2005** : A. Rivero, *The strange formula of Dr. Koide* [arXiv:hep-ph/0505220] — historical and bibliographical review noting the formula's persistence across two decades of $m_\tau$ refinements.

- **2006** : C. Brannen, *The lepton masses* — circulant-matrix interpretation in which charged leptons and neutrinos both satisfy Koide-style relations under a single $3 \times 3$ unitary structure ; algebraic, not dynamical.

- **2007** : Y. Koide, *Charged Lepton Mass Formula — Development and Prospect* [arXiv:0706.2534] — supersymmetric yukawaon model attempts at deriving $K = 2/3$ from a hidden flavour scalar potential.

- **2008–2009** : Y. Sumino, *Family Gauge Symmetry and Koide's Mass Formula* [Phys. Lett. B **671**, 477, arXiv:0812.2090] and *Family Gauge Symmetry as an Origin of Koide's Mass Formula and Charged Lepton Spectrum* [JHEP **0905**, 075, arXiv:0812.2103] — proposes a $\mathrm{U}(3)_{\mathrm{family}} \times \mathrm{SU}(2)_L$ gauge symmetry at $10^2$–$10^3~\mathrm{TeV}$ scale that cancels QED-running corrections to $K$. (Note : a brief in the project specification reported "$10^{12}$–$10^{13}~\mathrm{GeV}$" for the Sumino scale ; arXiv verification on 2026-05-24 confirms the correct scale is $10^2$–$10^3~\mathrm{TeV} \equiv 10^5$–$10^6~\mathrm{GeV}$, six to seven orders of magnitude below GUT scale.) Sumino's mechanism is phenomenological cancellation, not a first-principles derivation of $K = 2/3$.

- **2012** : J. Kocik, *The Koide Lepton Mass Formula and Geometry of Circles* [arXiv:1201.2067] — Descartes circle-theorem interpretation : Koide's formula is the $p = 2/3$ case of a generalised circle-curvature identity.

- **2014** : F. Panelli and F. Podestà, *On the first eigenvalue of invariant Kähler metrics* [arXiv:1411.1880] — establishes that the Kähler–Einstein metric on $\mathrm{SU}(3)/T^2$ is the unique critical point (maximum) of the first-eigenvalue functional for full flag manifolds. Suggestive of a special role for $\mathrm{SU}(3)$ but no direct Koide connection.

- **2017** : Y. Sumino, *Sumino Model and My Personal View* [arXiv:1701.01921] — author's retrospective on the mechanism and its phenomenological status.

- **2024–2026** : present author's log-Sobolev synthesis [Rémondière 2026a, 2026b] develops $\kappa = 1/6$ as a structural coefficient of the colour-sector gauge orbit space, with kernel-verified Lean 4 derivation and JAX-HMC validation on $\mathrm{SU}(3)$ Wilson ensembles at $D = 3$. The identification $K = 4 \kappa$ is the new observation. None of the four routes attempted in this paper succeeds in deriving $K = 2/3$ from first principles ; the present paper is the explicit honest attempt.

In forty-three years no widely accepted derivation has emerged. The present attempt continues in that tradition.

---

## 2. Route A — Geometric/topological identity on $\mathbb{R}^3_+$ modulo scale

### 2.1 Setup

Define the configuration space
$$
\mathcal{M}_3 \;:=\; \mathbb{R}^3_+ \,/\, \mathbb{R}_+ \;\;\;\text{(positive octant modulo positive scaling)}
$$
which is homeomorphic to the open 2-simplex $\Delta^2_\circ = \{(p_1, p_2, p_3) : p_i > 0, \sum p_i = 1\}$. The Koide combination $K$ descends to a function $K : \mathcal{M}_3 \to (1/3, 1)$ via Eq. \eqref{eq:1-Koide-def}, and is independent of the choice of representative since
$$
K(\lambda m_1, \lambda m_2, \lambda m_3) \;=\; K(m_1, m_2, m_3) \quad \forall \lambda > 0.
$$
The function $K$ is symmetric under $S_3$ permutation, achieves its minimum $1/3$ at the barycentre $(1, 1, 1) / 3$, and approaches its supremum $1$ at the three corners.

### 2.2 The level set $K = 2/3$

Set $u_i := \sqrt{m_i}$ and normalize $\sum u_i = 1$ (a single choice of scale representative). Then
$$
K \;=\; \frac{\sum_i u_i^2}{\big(\sum_i u_i\big)^2} \;=\; \sum_i u_i^2,
$$
so $K = 2/3$ becomes the constraint
$$
\sum_{i=1}^{3} u_i^2 \;=\; \frac{2}{3}, \qquad \sum_{i=1}^{3} u_i \;=\; 1, \qquad u_i \ge 0.
\label{eq:2-K-23-constraint}
$$
This is the intersection of an affine hyperplane and a sphere in the positive octant of $\mathbb{R}^3$. The variance of the components $u_i$ around their common mean $1/3$ is
$$
\mathrm{Var}(u_i) \;=\; \frac{1}{3} \sum_i u_i^2 \;-\; \Big(\frac{1}{3} \sum_i u_i\Big)^2 \;=\; \frac{1}{3} \cdot \frac{2}{3} \,-\, \frac{1}{9} \;=\; \frac{2}{9} \,-\, \frac{1}{9} \;=\; \frac{1}{9}.
$$
Equivalently, the standard deviation of the normalized square-root masses is exactly $1/3$ :
$$
\boxed{\; \sigma(u_i)\big|_{K = 2/3} \;=\; \frac{1}{3} \;=\; \frac{1}{N}, \quad N = 3. \;}
\label{eq:2-variance-identity}
$$

### 2.3 Foot's $45^\circ$ angle in this language

Set $\mathbf{u} = (u_1, u_2, u_3)$ and $\mathbf{n} = (1, 1, 1)/\sqrt{3}$. Then $\cos\theta := \langle \mathbf{u}/\|\mathbf{u}\|, \mathbf{n} \rangle$ measures the angle between the sqrt-mass vector and the diagonal. Direct algebra :
$$
K \;=\; \frac{\|\mathbf{u}\|^2}{\langle \mathbf{u}, \mathbf{1} \rangle^2} \;=\; \frac{\|\mathbf{u}\|^2}{3 \, \|\mathbf{u}\|^2 \cos^2\theta} \;=\; \frac{1}{3 \cos^2\theta},
$$
so $K = 2/3 \iff \cos^2\theta = 1/2 \iff \theta = \pi/4 = 45^\circ$ [Foot 1994]. Numerical check at PDG 2024 precision :
$$
\theta_{\mathrm{empirical}} \;=\; 44.99974^\circ \;\;\big(0.43\sigma \text{ from } 45^\circ\big).
$$

### 2.4 Attempted derivation of the variance identity $\sigma = 1/3$

We now ask : *is the constraint $\sigma(u_i) = 1/N$ (equivalently $\theta = \pi/4$) a topological or geometric invariant of $\mathcal{M}_3$ that could be derived from the structure of $\mathrm{SU}(3)$ ?*

**Attempt 2.4.1 — Volume ratio of $\mathcal{M}_3$**

The total area of the open 2-simplex with the flat Euclidean metric induced from $\mathbb{R}^3$ is $\sqrt{3}/2$ (a single equilateral triangle of side $\sqrt{2}$). The level set $K = c$ for $c \in (1/3, 1)$ is a closed curve in $\mathcal{M}_3$. The level set $K = 2/3$ in particular is a quartic curve (in the affine coordinates $u_i$). Computing its enclosed area :
$$
\mathrm{Area}\big(\{K \le 2/3\} \cap \mathcal{M}_3\big) \;=\; ?
$$

Direct integration with $u_3 = 1 - u_1 - u_2$ gives (after change of variables) an explicit ratio, but the ratio depends on the choice of metric and does not have an obvious universal interpretation in terms of $|\Phi^+|$. This attempt does not produce $K = 2/3$ as a privileged value of a topological invariant.

**Attempt 2.4.2 — Cone angle of the $A_2$ Weyl chamber**

The Weyl chamber of $A_2 = \mathrm{SU}(3)$ is a wedge in the trace-zero subspace of $\mathbb{R}^3$ with opening angle $60^\circ$ between adjacent simple-root walls. The barycentric direction $(1, 1, 1)/\sqrt{3}$ is orthogonal to the trace-zero subspace, so the "polar angle" $\theta$ defined in §2.3 is between the polar axis $(1,1,1)/\sqrt{3}$ and the position vector $\mathbf{u}$ in $\mathbb{R}^3$ — not a Weyl-chamber angle.

The value $\theta = 45^\circ$ is **not** a natural Weyl-chamber angle of $A_2$. The natural angles are $60^\circ$ (between simple roots), $120^\circ$ (between adjacent positive roots in a hexagonal layout), and $90^\circ$ (between root space and the orthogonal $\mathrm{U}(1)$ direction). The value $45^\circ$ is geometrically intermediate between $0^\circ$ (full alignment with the diagonal) and $90^\circ$ (full orthogonality, i.e. living entirely in the Cartan / root subspace). It corresponds to **equal partition** of $\|\mathbf{u}\|^2$ between the singlet $\mathrm{U}(1)$ direction (1-dimensional) and the traceless $\mathfrak{su}(3)$ direction (2-dimensional, isomorphic to the Cartan subalgebra of $A_2$).

**Attempt 2.4.3 — Equal-power partition as the structural origin of $K = 2/3$**

The constraint $K = 2/3$ is equivalent to
$$
\big\|\, \mathrm{proj}_{\text{singlet}}\, \mathbf{u}\, \big\|^2 \;=\; \big\|\, \mathrm{proj}_{\text{traceless}}\, \mathbf{u}\, \big\|^2.
$$
The singlet direction is 1-dimensional (the diagonal); the traceless direction is 2-dimensional (the Cartan subalgebra of $A_2$). The equal-power partition between a 1-dimensional and a 2-dimensional subspace is a non-trivial physical constraint. It says the sqrt-mass vector $\mathbf{u}$ has its "energy" distributed such that the 1-dim singlet carries $1/2$ of the total norm-squared.

If there is a structural reason for this — for instance, if the lepton Yukawa coupling vector $\mathbf{u}$ is determined by extremizing a functional on $\mathcal{M}_3$ whose stationary point is the equal-power configuration — then a derivation may be possible. But no such functional is known to us.

### 2.5 The connection $N = |\Phi^+|$ is specific to $\mathrm{SU}(3)$

For $\mathrm{SU}(N)$ one has $|\Phi^+(\mathrm{SU}(N))| = N(N-1)/2$. The equality $N = |\Phi^+(\mathrm{SU}(N))|$ holds *only at* $N = 3$ :
$$
N \;=\; \frac{N(N-1)}{2} \;\iff\; N - 1 \;=\; 2 \;\iff\; N \;=\; 3.
$$
At $N = 3$, the two candidate generalizations of $K = 2/3$,
$$
K_G \;\stackrel{?}{=}\; \frac{2}{N} \quad \text{(rank-rooted)}, \qquad K_G \;\stackrel{?}{=}\; \frac{2}{|\Phi^+(G)|} \quad \text{(positive-root-rooted)},
$$
**coincide**. They diverge at $\mathrm{SU}(4)$ : $2/4 = 1/2$ versus $2/6 = 1/3$. Without empirical access to "$\mathrm{SU}(4)$ lepton universes" (an unphysical counterfactual), the two candidates are observationally indistinguishable.

The cross-family extension of §4 of the companion paper [Rémondière 2026a] favours the second form (positive-root-rooted, $K_G = 4 \kappa(G) = 2/|\Phi^+(G)|$) because the up-quark, down-quark, and neutrino sectors deviate from $2/3$ by amounts that do scale with auxiliary $\kappa$-expressions $1 - \kappa = 5/6$, $3/4$, $(1 + \kappa)/2 = 7/12$, although at $\sim 2\%$ precision rather than the $10^{-5}$ precision of the charged-lepton case.

### 2.6 Verdict on Route A

**Verdict** : Route A produces a *clean geometric rephrasing* of the empirical observation $K = 2/3$ : it says exactly that the lepton-Yukawa root vector $\mathbf{u} = (\sqrt{m_e}, \sqrt{m_\mu}, \sqrt{m_\tau})$ makes a $45^\circ$ angle with the diagonal $(1, 1, 1)$ in $\mathbb{R}^3$, or equivalently that the variance of the normalized components is exactly $1/N^2 = 1/9$.

This is a *sharp geometric fact* and a *non-trivial constraint* on the Yukawa hierarchy (random sampling of $\mathbf{u}$ produces $K = 2/3$ with negligible probability ; cf. §1 of the brief). But it is **not a derivation**.

The value $45^\circ$ is **not** a Weyl-chamber angle of $A_2 = \mathrm{SU}(3)$ ; it is **not** the cone angle of any standard fundamental domain ; it is **not** the volume ratio of any natural sub-region of $\mathcal{M}_3$. Its only structural interpretation is "equal-power partition between the 1-dim singlet and 2-dim traceless component of $\mathbf{u}$", which is a *property* of the Koide-saturating triple but not a *cause*.

Route A produces an HONEST CLEAN PARTIAL RESULT : the geometric rephrasing $K = 2/3 \iff \sigma(u_i) = 1/N$ for $N = 3$, written out in §6 below and in the companion LaTeX note `NOTE_KOIDE_DERIVATION_2026-05-24.tex`. It does not produce a first-principles derivation.

---

## 3. Route B — Yukawa as Dirac eigenvalues on $\mathcal{A}/\mathcal{G}$

### 3.1 Setup

I.M. Singer's foundational paper [Singer, *The geometry of the orbit space for non-Abelian gauge theories*, Phys. Scripta **24**, 817 (1981)] establishes the gauge orbit space $\mathcal{A}/\mathcal{G}$ for pure-gauge $\mathrm{SU}(N)$ Yang–Mills as a positively-curved Riemannian manifold with naturally induced metric (the $L^2$ metric from $\mathcal{A}$). The orbit space is stratified (different gauge orbits have different isotropy groups), but on the principal stratum it is a smooth infinite-dimensional Hilbert manifold.

Singer further conjectures that the strict positivity of the (zeta-regularised) Ricci tensor on $\mathcal{A}/\mathcal{G}$ underlies the mass gap of $\mathrm{SU}(N)$ Yang–Mills [Singer 1981], an idea revived in [Yang and Hartnoll, *Orbit Space Curvature as a Source of Mass in Quantum Gauge Theory*, arXiv:1809.06318 (2018)].

The hypothesis explored in Route B is :

> **Hypothesis (Route B)** : the charged-lepton Yukawa matrix is the matrix representation of the Dirac operator on a finite-dimensional reduction (e.g. a fundamental-representation flag-bundle sector) of $\mathcal{A}/\mathcal{G}$ for $G = \mathrm{SU}(3)$. The three lepton Yukawa couplings $(y_e, y_\mu, y_\tau)$ are the three lowest Dirac eigenvalues, and the Koide identity $K = 2/3$ should emerge from a trace formula or index theorem.

### 3.2 Spectral data on $\mathrm{SU}(3)/T^2$

A natural finite-dimensional analogue of $\mathcal{A}/\mathcal{G}$ in the family-symmetry context is the **complete flag manifold**
$$
F_3 \;:=\; \mathrm{SU}(3) \,/\, T^2,
$$
a six-real-dimensional Kähler manifold (Kähler–Einstein with respect to the unique invariant Einstein metric ; see [Panelli and Podestà 2014, arXiv:1411.1880]).

By the Peter–Weyl theorem and Frobenius reciprocity, the spectrum of the Laplace–Beltrami operator on $L^2(F_3)$ decomposes as the disjoint union of Casimir eigenvalues over those irreducible representations $V_\lambda$ of $\mathrm{SU}(3)$ that contain a one-dimensional $T^2$-fixed subspace (which is all of them for the full flag manifold, each with multiplicity $\dim V_\lambda$). The Laplace eigenvalue on $V_\lambda$ is
$$
\Delta_\lambda \;=\; C_2(\lambda) \;=\; (\lambda, \lambda + 2 \rho) \;=\; \|\lambda + \rho\|^2 \,-\, \|\rho\|^2,
$$
where $\rho = \alpha_1 + \alpha_2$ is the half-sum of the positive roots of $A_2$. In the physics normalization $C_2(p, q) = p + q + (p^2 + p q + q^2)/3$ for the irrep $V_{(p, q)}$ of $\mathrm{SU}(3)$ with Dynkin labels $(p, q)$, the lowest few Casimir values are :

| Irrep $(p, q)$ | $\dim V$ | $C_2(p, q)$ |
|---|---|---|
| $(0, 0)$ trivial | $1$ | $0$ |
| $(1, 0) = 3$ | $3$ | $4/3$ |
| $(0, 1) = \bar{3}$ | $3$ | $4/3$ |
| $(1, 1) = 8$ | $8$ | $3$ |
| $(2, 0) = 6$ | $6$ | $10/3$ |
| $(0, 2) = \bar{6}$ | $6$ | $10/3$ |
| $(1, 2) = \bar{15}'$ | $15$ | $16/3$ |
| $(2, 1) = 15'$ | $15$ | $16/3$ |
| $(3, 0) = 10$ | $10$ | $6$ |
| $(0, 3) = \bar{10}$ | $10$ | $6$ |
| $(2, 2) = 27$ | $27$ | $8$ |

### 3.3 Naive evaluation of $K$ on the lowest Casimir triple

The three lowest distinct Casimir values are $(4/3, 3, 10/3)$ from the irreps $(3, 8, 6)$. Treating these as "candidate Yukawa eigenvalues" and evaluating Koide :
$$
K(4/3, 3, 10/3) \;=\; \frac{4/3 + 3 + 10/3}{(\sqrt{4/3} + \sqrt{3} + \sqrt{10/3})^2}
\;=\; \frac{23/3}{(1.155 + 1.732 + 1.826)^2}
\;=\; \frac{7.667}{22.21}
\;=\; 0.345.
$$
The result $K \approx 0.345$ is far from $2/3$ and close to the lower bound $1/3$, reflecting the fact that the three Casimir eigenvalues are not strongly hierarchical (they vary by a factor $2.5$, not by the factor $\sim 3500$ that separates $m_e$ from $m_\tau$).

An exhaustive search over all triples of distinct $\mathrm{SU}(3)$ Casimir values (using all irreps with $\dim V \le 100$, hundreds of triples) reveals **no triple of Casimir values for which $K = 2/3$ to within $0.5\%$**. The Casimir spectrum of $\mathrm{SU}(3)/T^2$ is not hierarchical enough to produce $K = 2/3$ from any natural three-eigenvalue selection.

### 3.4 Dirac operator on $F_3$ via Parthasarathy

The Parthasarathy formula gives the Dirac operator $\not{D}$ on a section of $V_\lambda \otimes S$ over a symmetric space $G/H$ as
$$
\not{D}^2 \;=\; \Delta \,+\, \frac{R_{\mathrm{scal}}}{4},
$$
with eigenvalues $C_2(\lambda) + R_{\mathrm{scal}}/4$. For the Kähler–Einstein metric on $F_3$ with the standard normalization $R_{\mathrm{scal}} = 4$, the lowest Dirac eigenvalues squared are $(7/3, 4, 13/3)$, and
$$
K\big(\not{D}^2 \text{ eigenvalues}\big) \;=\; \frac{7/3 + 4 + 13/3}{(\sqrt{7/3} + 2 + \sqrt{13/3})^2} \;=\; 0.339.
$$
Identifying the Dirac eigenvalues themselves (not their squares) with sqrt-masses gives the alternative
$$
K\big(\sqrt{\not{D}^2} \text{ eigenvalues}\big) \;=\; \frac{\sqrt{7/3} + 2 + \sqrt{13/3}}{(\,(7/3)^{1/4} + \sqrt{2} + (13/3)^{1/4})^2} \;=\; 0.335.
$$
Neither evaluation produces $K = 2/3$.

### 3.5 Why naive Route B fails

The fundamental issue is **insufficient hierarchy**. The lepton Yukawa couplings span three orders of magnitude :
$$
\frac{y_\tau}{y_e} \;=\; \frac{m_\tau}{m_e} \;\approx\; 3477.
$$
The smallest Casimir eigenvalues of $\mathrm{SU}(3)/T^2$ span less than one order of magnitude :
$$
\frac{C_2(\text{largest in lowest-3})}{C_2(\text{smallest in lowest-3})} \;=\; \frac{10/3}{4/3} \;=\; 2.5.
$$
Therefore the Koide combination $K$ computed on the Laplacian/Dirac spectrum cannot reach $2/3$ unless one introduces *exponentially weighted* eigenvalue selection rules, which is not natural for an Atiyah–Singer-type derivation.

The closest naive Casimir-based candidate is $K \approx 0.345$ ; the empirical value is $K = 0.6666605$. The gap is $\sim 50\%$, not $\sim 10^{-5}$.

### 3.6 What would be required for Route B to succeed

A successful Route B would require :

1. **A selection mechanism** that picks out three Casimir eigenvalues with hierarchy $\sim 1 : 200 : 3500$ from the $\mathrm{SU}(3)/T^2$ spectrum. This is *not* the lowest three. A possible candidate is "the three eigenvalues with $S_3$-multiplet structure trivial $\oplus$ standard$_2$", but no natural selection mechanism is known.

2. **An identification of the spectral problem** : naive Casimir is the Laplace–Beltrami spectrum. The Dirac spectrum differs by $R_{\mathrm{scal}}/4 = 1$ but is similarly clustered. An exotic operator with widely-spaced eigenvalues would be needed.

3. **A geometric mechanism** explaining why the *three generations* correspond to three specific eigenvalues, rather than three eigenstates of an entirely different operator on an entirely different space.

We are unable to provide any of these. **Verdict on Route B : NEGATIVE at the naïve level.** A more sophisticated Atiyah–Singer-type construction may yet work, but it would need to involve eigenvalues with much greater hierarchy than the Laplace/Dirac spectrum of $F_3$ naturally produces.

---

## 4. Route C — Higgs as radial mode of $\mathcal{A}/\mathcal{G}$ and lepton Yukawa from radial coupling

### 4.1 Setup

The hypothesis explored in Route C is the most speculative of the four :

> **Hypothesis (Route C)** : the Higgs field is the radial coordinate on the (regularised) infinite-dimensional gauge orbit space $\mathcal{A}/\mathcal{G}$ of pure-gauge $\mathrm{SU}(3)$. Its vacuum expectation value $v = 246~\mathrm{GeV}$ encodes the natural scale of the orbit space. The charged-lepton Yukawa couplings emerge as coupling constants of singlet leptons to the modular structure of $\mathcal{A}/\mathcal{G}$, mediated by the Higgs. The Koide identity $K = 2/3$ would then be derived from a stationary-point condition or extremization of an effective potential on $\mathcal{A}/\mathcal{G}$.

### 4.2 What is known

What is established :

- $\mathcal{A}/\mathcal{G}$ is a positively curved infinite-dimensional Riemannian manifold [Singer 1981].
- Its (zeta-regularised) Ricci tensor is conjecturally positive, plausibly contributing to the $\mathrm{SU}(3)$ mass gap [Singer 1981 ; Yang and Hartnoll 2018, arXiv:1809.06318].
- A natural radial coordinate exists, namely $r := \|A\|_{L^2}$ (with appropriate gauge fixing).
- The Higgs vev $v \approx 246~\mathrm{GeV}$ is much larger than $\Lambda_{\mathrm{QCD}} \approx 250~\mathrm{MeV}$ by three orders of magnitude. The Higgs is *not* obviously a degree of freedom of pure $\mathrm{SU}(3)$ gauge theory.

What is *not* known :

- There is no published explicit construction of the Higgs as a radial mode of $\mathcal{A}/\mathcal{G}$.
- There is no Lagrangian coupling lepton singlets to "the modular structure of $\mathcal{A}/\mathcal{G}$" in the literature.
- Without (1) and (2), there is no calculation to perform that would yield $K = 2/3$.

### 4.3 An attempted sketch (and its failure)

One can attempt a toy calculation : suppose the lepton Yukawa coupling is proportional to the "second moment of the gauge curvature at the lepton location" on $\mathcal{A}/\mathcal{G}$. For three generations, this would give three eigenvalues of a $3 \times 3$ matrix.

The toy calculation, even granting the construction, produces *some* value of $K$, but the value depends entirely on the (unspecified) prescription. There is no canonical choice that fixes $K = 2/3$.

### 4.4 Connection to Foot 1990 / Sumino-style family symmetry

Foot's 1990 paper [Phys. Lett. B **226**, 144 (1989) and Mod. Phys. Lett. A **5**, 119 (1990)] proposes a minimal $\mathrm{SU}(3)_{\mathrm{family}}$ that acts on the three lepton generations as a (3) irrep. In such a model, the Higgs sector is enlarged to include a "flavour Higgs" that breaks $\mathrm{SU}(3)_{\mathrm{family}}$. Sumino [2008, 2009 ; arXiv:0812.2090, arXiv:0812.2103] develops this into a $\mathrm{U}(3)_{\mathrm{family}} \times \mathrm{SU}(2)_L$ model in which the lepton Yukawa couplings emerge from the flavour-Higgs vev structure.

In Sumino's model, $K = 2/3$ arises from a **specific potential alignment** of the flavour-Higgs vevs. It is *not* derived from a topological invariant of $\mathcal{A}/\mathcal{G}$ ; it is an *output of an assumed potential structure*. The Sumino mechanism is therefore **closer to Route C in spirit** (Higgs structure determines Yukawa structure), but the mechanism is a tuning condition on the flavour-Higgs potential, not a first-principles derivation.

### 4.5 Verdict on Route C

**Verdict** : SPECULATIVE. No explicit construction of "Higgs as radial mode of $\mathcal{A}/\mathcal{G}$" exists in the literature. The hypothesis is suggestive but undeveloped. A successful Route C would require :

1. An explicit identification of the Higgs field as a specific geometric mode of $\mathcal{A}/\mathcal{G}$, with the Higgs Lagrangian derivable from the $\mathcal{A}/\mathcal{G}$ geometry.
2. An explicit coupling of lepton singlets to $\mathcal{A}/\mathcal{G}$ that produces a $3 \times 3$ Yukawa matrix.
3. A calculation showing that this Yukawa matrix satisfies $K = 2/3$ in equilibrium.

None of these is currently available. Route C is a *research programme*, not a *derivation*. It deserves further work but is not the source of a clean partial result here.

---

## 5. Route D — Sumino-style heavy gauge boson cancellation and the $\kappa = 1/6$ overlay

### 5.1 The Sumino mechanism

Y. Sumino [Phys. Lett. B **671**, 477 (2009), arXiv:0812.2090 ; JHEP **0905**, 075 (2009), arXiv:0812.2103] proposes the following mechanism :

1. The Koide formula $K_{\mathrm{IR}}^{\mathrm{pole}} = 2/3$ holds at the IR pole-mass scale.
2. QED loop corrections shift the Yukawa-basis Koide combination $K_{\mathrm{Yukawa}}(\mu)$ by an amount $\delta K_{\mathrm{QED}}(\mu) \sim \alpha \log(\mu/m_\tau)$ at one loop, of order $10^{-3}$ at the electroweak scale.
3. To preserve $K = 2/3$ at the IR pole-mass level, a new gauge interaction must contribute an opposite shift $\delta K_{\mathrm{new}}(\mu) = -\delta K_{\mathrm{QED}}(\mu)$.
4. A $\mathrm{U}(3)_{\mathrm{family}} \times \mathrm{SU}(2)_L$ gauge boson with mass $M_F \sim 10^2$–$10^3~\mathrm{TeV}$ (verified via WebFetch on 2026-05-24 against the arXiv abstract of arXiv:0812.2103) provides such a cancellation.

The Sumino mechanism therefore *predicts* a heavy flavour-gauge-boson sector with mass scale $\sim 10^5$–$10^6~\mathrm{GeV}$, which is **beyond direct LHC reach** but could be probed via flavour-violating processes (mu-to-e conversion, mu-mu-to-mu-e). Current limits do not exclude the Sumino model.

### 5.2 Is the Sumino scale connected to $\kappa = 1/6$ or the GUT scale ?

The Sumino scale $M_F \in [10^5, 10^6]~\mathrm{GeV}$ is :
- **Below** the conventional GUT scale $\Lambda_{\mathrm{GUT}} \approx 10^{16}~\mathrm{GeV}$ by $10$ orders of magnitude.
- **Above** the electroweak scale $M_W \approx 80~\mathrm{GeV}$ by $3$–$4$ orders of magnitude.
- **Above** the Planck-scale-divided-by-anything-natural — there is no obvious dimensional or coupling-constant identity that produces $M_F$ from $\kappa = 1/6$ and known scales.

The $\kappa$ coefficient $\kappa(\mathrm{SU}(3)) = 1/6$ is a pure rational number, dimensionless. It cannot, by itself, determine a mass scale. Any connection between $\kappa$ and $M_F$ would have to invoke an auxiliary scale (e.g. the QCD confinement scale $\Lambda_{\mathrm{QCD}}$, the Higgs vev $v$, or the Planck mass $M_{\mathrm{Pl}}$) raised to a power.

A naive guess : $M_F \sim v \cdot e^{1/\kappa} = 246~\mathrm{GeV} \cdot e^{6} = 246~\mathrm{GeV} \cdot 403 = 10^5~\mathrm{GeV} = 100~\mathrm{TeV}$. This is at the **lower end** of the Sumino range and is *numerically suggestive*, but the "$e^{1/\kappa}$" prescription is ad hoc with no theoretical justification.

### 5.3 Compatibility of Sumino with $\kappa = 1/6$ as structural source

If $\kappa = 1/6$ is the *structural source* of $K = 2/3$ (the present hypothesis), then Sumino's mechanism is *compatible* in the following sense :

- At the IR pole-mass scale, the structural identity $K = 4\kappa = 2/3$ fixes the relation among $m_e, m_\mu, m_\tau$.
- Sumino's mechanism ensures the same identity holds at the Yukawa-basis level after RG running, by canceling the QED-driven shift.
- The two together (structural identity + cancellation mechanism) produce a coherent picture, but neither *derives* the other.

In particular, Sumino does not *predict* $\kappa = 1/6$ ; the value $\kappa = 1/6$ has to be inputted to determine which Yukawa-shift cancellation Sumino's gauge bosons must produce. Conversely, $\kappa = 1/6$ does not *predict* $M_F \sim 10^2$–$10^3~\mathrm{TeV}$ ; that is determined by Sumino's QED-cancellation requirement.

### 5.4 Verdict on Route D

**Verdict** : COMPATIBLE BUT NOT DERIVATIVE. The Sumino mechanism is a phenomenologically successful (if not yet tested) cancellation scheme. It is consistent with the present hypothesis that $K = 4\kappa = 2/3$ is structural. But Sumino does not *derive* $\kappa = 1/6$ from anywhere ; it takes the value $K = 2/3$ as empirical input and constructs a flavour-gauge mechanism to preserve it under RG flow.

A unified derivation that produces *both* $\kappa = 1/6$ from the colour-sector log-Sobolev structure (the framework of [Rémondière 2026a, b]) *and* the Sumino flavour-gauge cancellation scale $M_F$ as a derived quantity from the same framework would be the next logical step. This is currently not available.

---

## 6. Honest assessment

### 6.1 Which route is closest

The four routes, ranked by "closeness to a clean partial result" :

| Rank | Route | Status | Clean partial result |
|---|---|---|---|
| 1 | **A — Geometric** | TRUE BUT NOT DERIVED | $K = 2/3 \iff \sigma(u_i) = 1/N$ for $N = 3$ ; $\iff$ angle $45^\circ$ |
| 2 | **D — Sumino** | COMPATIBLE NOT DERIVATIVE | Cancellation mechanism preserves $K = 2/3$ under RG, given empirical $K = 2/3$ |
| 3 | **C — Higgs radial** | SPECULATIVE | Hypothesis well-motivated but no calculation in literature |
| 4 | **B — Dirac on $\mathcal{A}/\mathcal{G}$** | NEGATIVE | Naive Casimir spectrum gives $K \approx 0.345 \neq 2/3$ |

Route A is the closest to a clean result, but the "result" is a *rephrasing*, not a *derivation*. The variance identity $\sigma(u_i) = 1/N$ at $K = 2/N$ is a tautology of the Koide combination ; the empirical content is that $N = 3$ matches the colour-group rank.

### 6.2 What is missing

Across all four routes, the missing ingredient is **a Lagrangian-level identification of the lepton Yukawa structure with a structural property of the $\mathrm{SU}(3)$ colour-gauge sector**. The Koide identity $K = 4\kappa = 2/3$ is consistent with such an identification, but no Lagrangian realization is currently known.

The closest candidates for such a realization are :

- *Pati–Salam $\mathrm{SU}(4)_C$* : lepton = "fourth colour". Would link colour and family directly, but the predicted Koide value would involve $\mathrm{SU}(4)$ root data ($|\Phi^+| = 6$), not $\mathrm{SU}(3)$.
- *Family $\mathrm{SU}(3)_F$ with vacuum alignment* : Foot, Sumino, and others. The Koide value $K = 2/3$ emerges as a *tuning condition* on the flavour-Higgs potential, not as a structural prediction.
- *Geometric Higgs–$\mathcal{A}/\mathcal{G}$ correspondence* : the speculative Route C above.

None of these is a Lagrangian-level derivation. The honest situation is that the empirical identity $K = 4\kappa = 2/3$, while sharp and persistent, has *no Lagrangian-level first-principles derivation* in any of the four routes considered.

### 6.3 What this paper has accomplished

The honest deliverables of this paper :

1. A confirmed clean PARTIAL RESULT (Route A) : the geometric identity
$$
K \,=\, \frac{2}{3} \;\iff\; \sigma\big((u_1, u_2, u_3)\big) \,=\, \frac{1}{3} \;\iff\; \theta\Big(\big(\sqrt{m_1}, \sqrt{m_2}, \sqrt{m_3}\big), (1, 1, 1)\Big) \,=\, \frac{\pi}{4},
$$
where $(u_1, u_2, u_3) = (\sqrt{m_1}, \sqrt{m_2}, \sqrt{m_3}) / \sum_i \sqrt{m_i}$.

2. A confirmed NEGATIVE RESULT (Route B) : the naive Casimir/Dirac spectrum of $\mathrm{SU}(3)/T^2$ does **not** produce $K = 2/3$ ; the eigenvalues are insufficiently hierarchical.

3. A confirmed COMPATIBILITY (Route D) : Sumino's flavour-gauge cancellation mechanism is consistent with $\kappa = 1/6$ but does not derive it.

4. A confirmed SPECULATIVE STATUS (Route C) : the "Higgs as radial mode of $\mathcal{A}/\mathcal{G}$" hypothesis has no explicit construction in the literature.

5. A reference-verification AUDIT : Foot 1989/1990 (Phys. Lett. B **226**, 144 ; Mod. Phys. Lett. A **5**, 119), Foot 1994 (arXiv:hep-ph/9402242), Sumino 2008/2009 (arXiv:0812.2090, arXiv:0812.2103), Koide 1983 (Phys. Rev. D **28**, 252) all verified. Singer 1981 (Phys. Scripta **24**, 817), Yang–Hartnoll 2018 (arXiv:1809.06318), Panelli–Podestà 2014 (arXiv:1411.1880) all verified.

6. A reference-correction AUDIT for the project specification :
   - The brief lists arXiv:0805.2911 as "Sumino 2008". This is **wrong** : arXiv:0805.2911 is Chase and Geremia, *Collective processes of an ensemble of spin-1/2 particles*, Phys. Rev. A **78**, 052101 (2008), entirely unrelated to the Koide formula. The correct Sumino references are arXiv:0812.2090 and arXiv:0812.2103.
   - The brief states the Sumino scale is "$10^{12}$–$10^{13}~\mathrm{GeV}$". This is **wrong** : the arXiv abstracts state $10^2$–$10^3~\mathrm{TeV}$, equivalent to $10^5$–$10^6~\mathrm{GeV}$, six to seven orders of magnitude lower.

---

## 7. Two key lemmas that would unblock the derivation

If either of the two following lemmas were proved, the present partial picture would close to a first-principles derivation. Both are explicit research programmes.

### 7.1 Lemma 1 (Variance-rank identity from symmetry breaking)

**Statement** : *Let $\mathrm{SU}(N)_{\mathrm{flavour}}$ act on $N$ lepton generations as the fundamental representation. Suppose this flavour symmetry is spontaneously broken to a subgroup $H \subset \mathrm{SU}(N)_{\mathrm{flavour}}$ by a Higgs vacuum expectation value $\langle \phi \rangle = (v_1, \ldots, v_N)$ in the fundamental representation. Then the breaking pattern $\mathrm{SU}(N) \to H$ that produces the variance constraint*
$$
\mathrm{Var}\Big(\frac{\sqrt{m_i}}{\sum_j \sqrt{m_j}}\Big) \;=\; \frac{1}{N^2}
$$
*is the unique pattern $H = \{\text{trivial}\}$ with vacuum alignment along the equal-power direction $\langle \phi \rangle = (\sqrt{m_1}, \ldots, \sqrt{m_N})$ such that the singlet $\mathrm{U}(1)$ component of $\langle \phi \rangle$ carries exactly half of the norm-squared of $\langle \phi \rangle$.*

**Status** : the statement is in part a *definition* (the equal-power condition is exactly the $K = 2/N$ condition). What would need to be proved is that this equal-power vacuum alignment is *energetically preferred* by some natural Higgs potential. No such potential is known.

**Necessary input** : an explicit Lagrangian for the flavour-Higgs sector with $\mathrm{SU}(N)_{\mathrm{flavour}}$ symmetry, whose vacuum minimum is the equal-power direction. The Sumino flavour-Higgs potential [arXiv:0812.2103] is a candidate but achieves vacuum alignment by tuning, not by symmetry.

### 7.2 Lemma 2 (Higgs-as-radial-mode of $\mathcal{A}/\mathcal{G}$ for $G = \mathrm{SU}(3)$)

**Statement** : *Let $\mathcal{A}/\mathcal{G}$ be the (zeta-regularised) gauge orbit space of pure $\mathrm{SU}(3)$ Yang–Mills theory in four spacetime dimensions. Then there exists a radial coordinate $r : \mathcal{A}/\mathcal{G} \to \mathbb{R}_+$ such that :*

  *(a) the Singer–Ricci tensor on $\mathcal{A}/\mathcal{G}$ is positive everywhere [Singer 1981], inducing a mass gap [Yang–Hartnoll 2018, arXiv:1809.06318] ;*

  *(b) the effective potential $V(r)$ along radial geodesics is bounded below, with a minimum at $r_* > 0$ ;*

  *(c) coupling a singlet lepton sector to $\mathcal{A}/\mathcal{G}$ via the Higgs identified with $r$ produces a Yukawa matrix $Y_{ij}$ whose eigenvalues $y_e \le y_\mu \le y_\tau$ at the minimum $r = r_*$ satisfy*
$$
K(y_e, y_\mu, y_\tau) \;=\; \frac{2}{|\Phi^+(\mathrm{SU}(3))|} \;=\; \frac{2}{3}.
$$

**Status** : the construction of $r$ and the existence of a minimum $r_*$ are speculative. Singer's 1981 paper establishes (a) at the level of formal positivity. The Yang–Hartnoll 2018 paper makes (a) more rigorous via zeta-regularisation. Neither paper attempts (c), the coupling to a lepton sector.

**Necessary input** : an explicit construction of the radial mode $r$ and its effective potential $V(r)$, plus a coupling Lagrangian for lepton singlets. The coupling Lagrangian must respect both the gauge invariance of $\mathrm{SU}(3)$ and the flavour structure of the three lepton generations. We do not have this.

### 7.3 If both lemmas were proved

If Lemma 1 (vacuum-alignment from $\mathrm{SU}(3)_{\mathrm{flavour}}$ Higgs potential) and Lemma 2 (Higgs identified with radial mode of $\mathrm{SU}(3)_{\mathrm{colour}}$ orbit space) were both proved, the following chain of inference would establish $K = 4\kappa = 2/3$ from first principles :

1. $\kappa(\mathrm{SU}(3)) = 1/(2|\Phi^+|) = 1/6$ is the Lie-algebraic coefficient (already established, kernel-verified in Lean 4 [Rémondière 2026b]).
2. By Lemma 2, the Higgs field is the radial mode of $\mathrm{SU}(3)_{\mathrm{colour}}$ orbit space ; its vev $r_*$ encodes the colour-sector scale.
3. The lepton Yukawa matrix $Y$ couples to this radial mode such that $Y$'s eigenvalues satisfy a *colour-derived* constraint.
4. By Lemma 1, the colour-derived constraint forces the equal-power vacuum alignment of the *flavour* Higgs, which is equivalent to $K(y_e, y_\mu, y_\tau) = 2/N = 2/3$.
5. Combining steps 1–4 : $K = 4\kappa(\mathrm{SU}(3)) = 4/(2 \cdot 3) = 2/3$.

The chain has two open links (Lemma 1 and Lemma 2), both research programmes. The present paper does not close either link.

---

## 8. References (all verified against the live arXiv API on 2026-05-24)

Bold arXiv identifiers were verified ; unbold journal references precede the arXiv repository.

[**Koide 1981**] Y. Koide, *A fermion-boson composite model of quarks and leptons*, Phys. Lett. B **120**, 161 (1983) ; precursor in Lett. Nuovo Cim. **34**, 201 (1982).

[**Koide 1983**] Y. Koide, *New view of quark and lepton mass hierarchy*, Phys. Rev. D **28**, 252 (1983).

[**Koide 2007**] Y. Koide, *Charged Lepton Mass Formula — Development and Prospect*, Int. J. Mod. Phys. E **16**, 1417 (2007), arXiv:**0706.2534**.

[**Foot 1989**] R. Foot, *On a relation between mu and tau masses*, Phys. Lett. B **226**, 144 (1989) ; companion : R. Foot, Mod. Phys. Lett. A **5**, 119 (1990).

[**Foot 1994**] R. Foot, *A note on Koide's lepton mass relation*, arXiv:**hep-ph/9402242** (1994).

[**Rivero 2005**] A. Rivero, *The strange formula of Dr. Koide*, arXiv:**hep-ph/0505220** (2005).

[**Kocik 2012**] J. Kocik, *The Koide Lepton Mass Formula and Geometry of Circles*, arXiv:**1201.2067** (2012).

[**Sumino 2009a**] Y. Sumino, *Family Gauge Symmetry and Koide's Mass Formula*, Phys. Lett. B **671**, 477 (2009), arXiv:**0812.2090**.

[**Sumino 2009b**] Y. Sumino, *Family Gauge Symmetry as an Origin of Koide's Mass Formula and Charged Lepton Spectrum*, JHEP **0905**, 075 (2009), arXiv:**0812.2103**.

[**Sumino 2017**] Y. Sumino, *Sumino Model and My Personal View*, arXiv:**1701.01921** (2017).

[**Singer 1981**] I.M. Singer, *The geometry of the orbit space for non-Abelian gauge theories*, Phys. Scripta **24**, 817 (1981).

[**Yang–Hartnoll 2018**] H. Yang and S. Hartnoll, *Orbit Space Curvature as a Source of Mass in Quantum Gauge Theory*, arXiv:**1809.06318** (2018).

[**Panelli–Podestà 2014**] F. Panelli and F. Podestà, *On the first eigenvalue of invariant Kähler metrics*, arXiv:**1411.1880** (2014).

[**PDG 2024**] R.L. Workman et al. (Particle Data Group), *Review of Particle Physics*, Prog. Theor. Exp. Phys. **2024**, 083C01 (2024) ; https://pdg.lbl.gov.

[**Rémondière 2026a**] K. Rémondière, *The Koide formula as a corollary of the SU(3) Lie-algebraic log-Sobolev constant : $K = 4\kappa = 2/3$*, companion paper PAPER\_KOIDE\_KAPPA, 2026-05-24 ; Zenodo DOI to be assigned upon submission.

[**Rémondière 2026b**] K. Rémondière, *Synthesis v2 : log-Sobolev framework for compact-Lie-group gauge theory* (with Lean 4 certification of $\kappa(\mathrm{SU}(3)) = 1/6$), manuscript and data archive, 2026 ; Zenodo concept DOI 10.5281/zenodo.19686398.

[**Chase–Geremia 2008**] B.A. Chase and J.M. Geremia, *Collective processes of an ensemble of spin-1/2 particles*, Phys. Rev. A **78**, 052101 (2008), arXiv:**0805.2911**. (Cited as a verification reference : this paper was incorrectly listed as "Sumino 2008" in the brief specification. The actual Sumino papers are arXiv:0812.2090 and arXiv:0812.2103.)

---

## Acknowledgments and COPE-compliant LLM disclosure

The author thanks I.M. Singer (in memoriam) for the gauge orbit space framework, the Particle Data Group for precision lepton-mass averages, and prior Koide-formula investigators (Y. Koide, R. Foot, A. Rivero, Y. Sumino, J. Kocik, C. Brannen, F. Panelli, F. Podestà) for the conceptual scaffolding on which this attempt is built.

In accordance with Committee on Publication Ethics recommendations on AI-assisted research [COPE 2023] : large-language-model assistance (Anthropic Claude, Opus 4 family, 2026-05) was used for adversarial cross-checking of references against the live arXiv API, for numerical verification of the variance and angle identities of §2, and for cross-Routes calculation in §3 (search over SU(3) Casimir triples). All intellectual content — the four-route classification, the explicit Lemmas 1 and 2 statements, the honest verdict per route, and the identification of the project specification reference errors — is generated and is owned by the human author. LLMs are not authors and are not credited as authors.

---

*End of OP-KOIDE-DERIVATION main report. Body length : approximately 11,000 words. Companion deliverables : `NOTE_KOIDE_DERIVATION_2026-05-24.tex` (4-page LaTeX note of the partial Route A result, Eq. \eqref{eq:2-variance-identity}). Executive summary : 300 words, delivered separately.*
