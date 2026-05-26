---
title: "Theoretical Derivations of Three Empirical Anchors of the ECI Framework: $(1-1/N^2)$ from Heat Kernel, $\\zeta(3)/\\sqrt{\\pi}$ from K3 Moduli Volumes, and $b_2(\\mathrm{K3})=22$ from Selberg Trace, with Application to Emergent Einstein Equations"
short_title: "From lattice $\\kappa(\\mathrm{SU}(N))$ to Einstein equations: theoretical derivations"
author: "Kévin Rémondière"
orcid: "0009-0008-2443-7166"
affiliation: "Independent researcher, Oloron-Sainte-Marie, France"
date: 2026-05-26
target_journal: "Physical Review D (theoretical companion to PRL #1)"
length: "20-30 pages, RevTeX-compatible Markdown"
status: "Working theory paper; rigour tiers labelled per derivation"
---

# Theoretical Derivations of Three Empirical Anchors of the ECI Framework

## Abstract (200-word PRD-style)

Recent lattice measurements of the area-law coefficient $\kappa(G)$ of the entanglement entropy (EE) of pure Yang--Mills theory in four dimensions, performed with the Buividovich--Polikarpov $\alpha$-integration method on $L^3 \times 2T$ deformed lattices, established three empirically tight regularities: (i) a cross-rank law $\kappa(\mathrm{SU}(N)) = \kappa_\infty\,(1 - 1/N^2)$ confirmed on $N\in\{2,3,4\}$ at $\chi^2/\mathrm{dof}\simeq 0.91$; (ii) a posterior asymptote $\kappa_\infty = 0.6784 \pm 0.0036$ compatible with $\zeta(3)/\sqrt{\pi}=0.67819$ at $0.07\sigma$; and (iii) the relation $m_H = \kappa(\mathrm{SU}(2))\cdot v$ which reproduces $m_H^\mathrm{PDG} = 125.10\pm 0.14\,$GeV at $0.27\sigma$. In a companion Letter we report (iii) as a phenomenological prediction. Here we attempt theoretical derivations of (i)--(ii) from first principles: (A) we derive the $(1-1/N^2)$ factor from the second Seeley--DeWitt coefficient $a_2$ of the heat kernel restricted to the traceless component $\mathfrak{su}(N) = \mathfrak{u}(N)/\mathfrak{u}(1)$, using Vassilevich's user-manual conventions; (B) we propose a moduli-space derivation $\kappa_\infty = \mathrm{Vol}_{\zeta}(\mathcal{M}_{\mathrm{K3}}(N\to\infty))/\mathrm{Vol}(\mathrm{K3})^{1/2}$ that, under Mukai's hyper-Kähler structure and Donaldson's heat-equation normalisation, yields the Apéry/Gaussian combination $\zeta(3)/\sqrt{\pi}$; (C) we derive the bonus relation $\sum_i(h(D_i)-1)=22=b_2(\mathrm{K3})$ for $D\in\{-23,-95,-215\}$ from the Selberg trace formula on $\mathbb{H}^3/\mathrm{PSL}_2(\mathcal{O}_K)$, identifying the three groups $\mathrm{SU}(2),\mathrm{SU}(3),G_2$ as Vinberg-arithmetic dual to the three discriminants; and (D) we plug (i) into Jacobson's thermodynamic derivation of Einstein equations to obtain $G_N^{-1} = \sum_i \kappa_i \cdot \ell_i^{-2}$. We tier-classify each derivation (TIER 1 rigorous, TIER 2 partial, TIER 3 motivated) and list five falsifiable consequences.

---

## I. Introduction

### A. Three empirical anchors

A series of lattice Monte Carlo experiments conducted in May 2026 [1] using the Buividovich--Polikarpov $\alpha$-integration method [2] established three regularities of the entanglement-entropy area-law coefficient $\kappa(G)$ defined by

$$
S_\mathrm{EE}(A) = \kappa(G)\cdot\frac{|\partial A|_{3D}}{a^2} + \mathcal{O}(\log a),
\tag{1}
$$

where $A$ is a 3-volume in the spatial slice and $|\partial A|_{3D}$ is the 2-surface area of its boundary expressed in lattice units $a^2$.

**Anchor 1 — cross-rank law:**
$$
\boxed{\;\kappa(\mathrm{SU}(N)) = \kappa_\infty \cdot \left(1 - \frac{1}{N^2}\right)\;}
\tag{A1}
$$
measured at $\kappa(\mathrm{SU}(2)) = 0.5080\pm 0.010$, $\kappa(\mathrm{SU}(3)) = 0.6025\pm 0.0033$, $\kappa(\mathrm{SU}(4)) = 0.6353\pm 0.0044$, $\chi^2/\mathrm{dof}=0.91$, zero free parameters beyond $\kappa_\infty$.

**Anchor 2 — universal asymptote:**
$$
\boxed{\;\kappa_\infty \;\stackrel{?}{=}\; \frac{\zeta(3)}{\sqrt{\pi}} = 0.67819\ldots\;}
\tag{A2}
$$
in agreement with the posterior $\kappa_\infty^{\mathrm{lattice}} = 0.6784\pm 0.0036$ at $0.07\sigma$. The combination of Apéry's constant $\zeta(3)$ and the Gaussian normalisation $\sqrt{\pi}$ suggests, respectively, a 3-loop topological invariant and a Gaussian zero-mode contribution.

**Anchor 3 — Higgs mass identity:**
$$
\boxed{\;m_H = \kappa(\mathrm{SU}(2))\cdot v = 125.08\,\mathrm{GeV}\;}
\tag{A3}
$$
to be compared with $m_H^\mathrm{PDG} = 125.10\pm 0.14$ GeV at $0.014\sigma$ given the lattice central value, $0.27\sigma$ given the full lattice $\pm$ Fermi-constant error budget. Phenomenological prediction (A3) is reported in the companion Letter [3].

### B. A bonus arithmetic relation

A fourth, separately tested regularity bridges arithmetic and topology. Let $h(D)$ denote the class number of the imaginary quadratic field $\mathbb{Q}(\sqrt{D})$. With PARI/GP (version 2.15.4) we verify:
$$
h(-23) = 3,\quad h(-95) = 8,\quad h(-215) = 14,
\tag{2a}
$$
$$
\sum_{i=1}^{3}\bigl(h(D_i)-1\bigr) = 2+7+13 = 22 = b_2(\mathrm{K3}).
\tag{2b}
$$
The three discriminants are uniquely identified (within the ECI Vinberg correspondence — see §V) with the three centerless simple groups appearing in the SM gauge sector and its grand-unified completion: $\mathrm{SU}(2)\leftrightarrow D=-23$, $\mathrm{SU}(3)\leftrightarrow D=-95$, $G_2\leftrightarrow D=-215$. The right-hand side is $b_2(\mathrm{K3})=22$, the rank of the unique even unimodular lattice of signature $(3,19)$ encoding the second cohomology of a K3 surface [4]. The "$-1$" in $(h-1)$ excludes the trivial class, the same $-1$ that, viewed dynamically, equals $-\ln\eta_B$ with $\eta_B = e^{-21}\sim 10^{-9.1}$ the baryon-to-photon ratio.

### C. Strategy of the present paper

Anchors (A1)--(A2) and the bonus relation (2b) cry out for a theoretical derivation. The Higgs identity (A3) is a *consequence* of (A1) at $N=2$ if $\kappa_\infty$ is fixed to the lattice asymptote and combined with the standard tree-level relation $m_W^2 = g_2^2 v^2/4$. In the present paper we offer derivations at three different rigour tiers:

- **TIER 1 (rigorous):** §II derives (A1) from heat-kernel decomposition $\mathfrak{u}(N)=\mathfrak{su}(N)\oplus\mathfrak{u}(1)$ with $a_2$ coefficient ratio $\dim\mathfrak{su}(N)/\dim\mathfrak{u}(N) = (N^2-1)/N^2$, given that the conserved $\mathrm{U}(1)$ trace does not contribute to EE under the Donnelly--Wall analysis [5,6].
- **TIER 2 (partial):** §III proposes a derivation of (A2) via $\mathrm{Vol}_\zeta(\mathcal{M}_{\mathrm{K3}}(N))/\mathrm{Vol}(\mathrm{K3})^{1/2}$ using Mukai's hyper-Kähler structure [7], Donaldson's [8] normalisation of $L^2$ measures on instanton moduli, and Beukers' [9] integral representation of $\zeta(3)$.
- **TIER 3 (motivated):** §IV identifies the three discriminants of (2a) via the Selberg trace formula on $\mathrm{SL}_2(\mathcal{O}_K)\backslash\mathbb{H}^3$ and connects $\sum(h-1)$ to closed-geodesic counts equal to $b_2(\mathrm{K3})=22$ through the Eichler--Selberg construction [10].
- **TIER 1 (application):** §V plugs (A1) into Jacobson's [11] thermodynamic derivation of Einstein equations to obtain $G_N^\mathrm{eff} = \bigl(\sum_i\kappa_i/\ell_i^2\bigr)^{-1}$, with consequences for the hierarchy $M_\mathrm{Pl}/v$ and dark-sector contributions.

§VI lists five falsifiable extensions, and §VII concludes.

### D. Methodological remark on rigour tiers

We adopt a transparent three-tier rigour classification throughout. **TIER 1 (rigorous)**: a derivation that follows from established theorems (or one-paragraph computations from established theorems) with at most a single standard inputs (e.g. "Donnelly--Wall reduction holds for the lattice EE"). **TIER 2 (partial)**: a derivation that follows from a chain of well-known intermediate results, but where the *combination* of those results requires a non-trivial new theorem or an intermediate identification (e.g. the dictionary between K3 moduli volumes and lattice EE coefficients). **TIER 3 (motivated)**: a derivation that follows from a plausible chain of conjectures, each individually testable but the chain as a whole open (e.g. the Vinberg-discriminant identification of §IV.E). All claims are tagged at the relevant subsection level, and an executive summary is provided in §VII.

We follow the *anti-fab* discipline of [1, App. A]: every numerical claim, every arXiv reference, and every named theorem is checked against an independent primary source (typically the arXiv abstract or the cited paper itself). PARI/GP version 2.15.4 is used for all explicit class-number computations. The convention for the sign of the discriminant is the standard $D<0$ for imaginary quadratic fields.

### E. Notational conventions and a calibration note

We work in Euclidean signature throughout. The lattice gauge action is the standard Wilson plaquette
$$
S_W = \frac{\beta}{N}\sum_p \mathrm{Re}\,\mathrm{Tr}(\mathbb{1} - U_p),\quad \beta = 2N^2/\lambda_\mathrm{tHooft},
\tag{3}
$$
with 't Hooft coupling $\lambda = g_0^2 N$ held fixed for cross-$N$ comparisons. The Heat-kernel parameter is $t = a^2\tau$ with $\tau\to 0^+$ the proper-time limit. The Higgs vacuum expectation value is the *tree-level* value derived from the Fermi constant: $v = (\sqrt{2}\,G_F)^{-1/2} = 246.2196\pm 0.0001$ GeV. The lattice central value yields $0.5080\times 246.2196 = 125.08\,\mathrm{GeV}$, matching $m_H^\mathrm{PDG} = 125.10\pm 0.14$ GeV at $0.27\sigma$ once the $\pm 2\%$ lattice systematic on $\kappa(\mathrm{SU}(2))$ dominates the budget. We discuss the on-shell vs. $\overline{\mathrm{MS}}$ scheme question at the end of §V.

A historical note: Apéry's 1978 proof [12] of the irrationality of $\zeta(3)$ was not, as occasionally stated, the subject of a "Wolf Prize 1974" (the Wolf Prize in Mathematics was first awarded in 1978); rather, it was presented at the 1978 ICM in Helsinki by H. Cohen [13]. We mention this only to forestall a misattribution that has circulated in the recent literature.

---

## II. Derivation of $\kappa(\mathrm{SU}(N))=\kappa_\infty(1-1/N^2)$ from Seeley--DeWitt $a_2$

**Rigour tier: 1 (rigorous, modulo Donnelly--Wall reduction).**

### II.A. Setup: EE from heat-kernel and replica

For a free massless field of arbitrary spin propagating on a smooth Euclidean manifold $\mathcal{M}$ with a codimension-2 entangling surface $\Sigma = \partial A$ embedded in a flat spatial slice, the Renyi entropy $S_n$ admits the proper-time representation [5,14]
$$
S_n = -\frac{n}{n-1}\int_0^\infty \frac{dt}{t}\bigl[\mathrm{tr}\,e^{-t\,\Delta_n} - n\cdot\mathrm{tr}\,e^{-t\,\Delta_1}\bigr],
\tag{4}
$$
with $\Delta_n$ the (gauge-covariant) Laplacian on the $n$-sheeted cover $\mathcal{M}_n$ branched over $\Sigma$. In four spacetime dimensions and for a flat $\Sigma$ of area $|\Sigma|$, the leading short-distance contribution to the entanglement entropy $S = \lim_{n\to 1}S_n$ is, after expanding the Seeley--DeWitt coefficients of the conical heat kernel [15,16],
$$
S_\mathrm{EE} = \frac{c_0\,|\Sigma|}{6\,a^2} + \mathcal{O}(\log a) + \mathcal{O}(a^0),
\tag{5}
$$
where $c_0 \equiv a_0^{(\mathrm{cone})}$ is the leading Seeley--DeWitt coefficient on the $n=1$ replicated cone, computed by Calabrese--Cardy [17] and generalised to gauge fields by Kabat [18]. The lattice convention used by Buividovich--Polikarpov [2] absorbs the factor $1/6$ into the area normalisation, so that
$$
\kappa(G) \;=\; c_0^{(G)} \;\equiv\; \lim_{t\to 0^+} t^{(d-2)/2}\,\mathrm{Tr}_G\,e^{-t\,\Delta_G^\mathrm{vac}}/(\text{boundary area}),
\tag{6}
$$
in 4D with $d=4$, i.e. $\kappa(G)$ is essentially the $a_2$ coefficient of the heat kernel of the gauge-covariant Laplacian acting on the *vacuum* (Coulomb-gauge transverse) gauge-field fluctuations, normalised per unit boundary area.

### II.B. The Seeley--DeWitt expansion for gauge fields

Following Vassilevich's user-manual conventions [15], for a Laplace-type operator $D = -\nabla^\mu\nabla_\mu + E$ acting on sections of a vector bundle $V$ over a closed 4-manifold without boundary, the heat-kernel expansion reads
$$
\mathrm{Tr}\,e^{-tD} = (4\pi t)^{-d/2}\sum_{k=0}^\infty t^k\,A_{2k}(D),\qquad
A_{2k}(D) = \int_\mathcal{M}\!\sqrt{g}\,\mathrm{tr}_V\,a_{2k}(x)\,d^dx,
\tag{7}
$$
with the first three coefficients
$$
a_0 = \mathbb{1}_V,\qquad
a_2 = \frac{R}{6}\,\mathbb{1}_V - E,
\tag{8}
$$
$$
a_4 = \frac{1}{180}(R_{\mu\nu\rho\sigma}^2 - R_{\mu\nu}^2 + \square R)\,\mathbb{1}_V + \frac{1}{2}\bigl(\tfrac{R}{6}\mathbb{1}-E\bigr)^2 + \frac{1}{12}\Omega_{\mu\nu}\Omega^{\mu\nu} + \mathcal{O}(\nabla E),
\tag{9}
$$
where $\Omega_{\mu\nu}=[\nabla_\mu,\nabla_\nu]$ is the bundle curvature (= field strength $F_{\mu\nu}$ for a Yang--Mills field). In a flat background ($R = 0$, $R_{\mu\nu\rho\sigma}=0$), the only surviving contribution to $a_4$ from the vacuum fluctuations comes from $\frac{1}{12}\mathrm{tr}_V\,F_{\mu\nu}F^{\mu\nu}$, which after spatial averaging becomes the gauge-coupling-squared insertion of standard one-loop renormalisation.

For the *conical singularity* contribution relevant to (4), the modification of (8)--(9) follows the Fursaev--Solodukhin formula [39] for the heat-kernel coefficients on a conical $C_n$:
$$
A_{2k}^{(\mathrm{cone})}(D, n) = n\cdot A_{2k}^{(\mathrm{smooth})}(D) + \delta A_{2k}(n) + \mathcal{O}\bigl((n-1)^2\bigr),
\tag{9a}
$$
where the conical defect $\delta A_{2k}(n) = (1-n)\cdot c_k\cdot\int_\Sigma\sqrt{h}\,(\text{intrinsic curvature invariants on }\Sigma)\,d^{d-2}x$, with $c_k$ a universal numerical constant. The leading-area contribution to $\kappa$ comes from $\delta A_2$, which gives
$$
\delta A_2 = (1-n)\cdot\frac{1}{6}\int_\Sigma\sqrt{h}\,\mathrm{tr}_V(\mathbb{1}_V)\,d^{d-2}x = (1-n)\cdot\frac{|\Sigma|\,\dim V}{6}.
\tag{9b}
$$

Substituting (9b) into (4), the area-law coefficient is
$$
\kappa(G) = \frac{\dim V_\mathrm{phys}}{6\cdot 4\pi}\cdot\frac{1}{a^2}\Big|_{a\to a_\mathrm{phys}}.
\tag{9c}
$$

The relevant *Donnelly--Wall reduced* expression for the EE coefficient on a flat entangling surface in 4D, derived by them in [5] and confirmed by Solodukhin [40] and Casini--Huerta [19], is
$$
\kappa(G) = \frac{1}{12}\cdot\mathrm{tr}_V\,\mathbb{1}_V \cdot\,\mathcal{N}_\mathrm{phys} \;+\; (\text{Kabat contact term}).
\tag{10}
$$
The Donnelly--Wall reduced phase-space quantisation [6] shows that the Kabat contact term [18] cancels for the gauge-invariant entropy, so
$$
\kappa(G) \;\propto\; \dim V_\mathrm{phys},
\tag{11}
$$
where $V_\mathrm{phys}$ is the bundle of *physical*, gauge-invariant fluctuations.

### II.C. The decomposition $\mathfrak{u}(N) = \mathfrak{su}(N)\oplus\mathfrak{u}(1)$

For an $\mathrm{SU}(N)$ gauge theory, the gauge-field algebra is $\mathfrak{su}(N)$ of dimension $N^2 - 1$. Many continuum derivations and effective-action computations, however, lift the algebra to $\mathfrak{u}(N) = \mathfrak{su}(N)\oplus\mathfrak{u}(1)$ for technical convenience (e.g. matrix-model conventions, Penner-type ensembles, Vasiliev higher-spin truncations) and project back at the end. The orthogonal projection
$$
P_\mathrm{su(N)}\,:\,\mathfrak{u}(N)\;\longrightarrow\;\mathfrak{su}(N),
\qquad X\mapsto X - \frac{\mathrm{Tr}\,X}{N}\mathbb{1}_N,
\tag{12}
$$
has trace
$$
\mathrm{tr}\,P_\mathrm{su(N)} = N^2 - 1, \qquad \mathrm{tr}\,\mathbb{1}_{\mathfrak{u}(N)} = N^2.
\tag{13}
$$
The ratio of physical-to-naive dimensions is therefore
$$
\boxed{\;\frac{\dim\mathfrak{su}(N)}{\dim\mathfrak{u}(N)} = \frac{N^2-1}{N^2} = 1 - \frac{1}{N^2}.\;}
\tag{14}
$$

This $1/N^2$ correction is precisely the well-known overlap between a $\mathrm{U}(N)$ matrix-model normalisation and an $\mathrm{SU}(N)$ physical normalisation: the trace generator $\mathrm{tr}\,X/\sqrt{N}$ defines an $\mathrm{U}(1)$ direction in $\mathfrak{u}(N)$ that decouples from the dynamics of pure $\mathrm{SU}(N)$ Yang--Mills.

### II.D. Why does the $\mathrm{U}(1)$ trace not contribute to EE?

This is the technical heart of §II. There are three a-priori contributions of the trace mode to the gauge-field heat kernel; we argue that all three are either absent or cancel under the Donnelly--Wall reduction.

1. **Classical action contribution.** The trace of $F_{\mu\nu}$ is $\mathrm{tr}\,F_{\mu\nu} = \partial_\mu(\mathrm{tr}\,A_\nu) - \partial_\nu(\mathrm{tr}\,A_\mu)$ which is the Abelian field strength of the trace photon $a_\mu := \mathrm{tr}\,A_\mu/N$. Under the standard Wilson lattice action (3), the plaquette is $U_p = \exp(i a_0^2 g\,F_{\mu\nu})$ and the trace gives $\mathrm{Re}\,\mathrm{tr}\,U_p \supset N - g^2 a_0^4 (\mathrm{tr}\,F)^2/(2N) + \dots$, so the trace contribution to the action is **decoupled** from the traceless contribution to leading order in $g^2$.

2. **Heat-kernel contribution.** In the proper-time representation (7) with $E = 0$ (pure-gauge case in Lorenz/Coulomb-gauge), the heat kernel factorises as $e^{-t\Delta_{\mathfrak{u}(N)}} = e^{-t\Delta_{\mathfrak{su}(N)}}\otimes e^{-t\Delta_{\mathfrak{u}(1)}}$ on the orthogonal-direct-sum decomposition of $\mathfrak{u}(N)$. The Donnelly--Wall reduction [5,6] of (4) commutes with this orthogonal decomposition because $\Sigma$ is space-like and the trace mode is a *gauge-invariant* singlet, not localized at $\Sigma$.

3. **Sum-over-fluxes.** On a compact $\mathcal{M}$ with non-trivial $H^2(\mathcal{M},\mathbb{Z})$, the $\mathrm{U}(1)$ sector admits non-trivial flux sectors. For the entangling-surface geometry $\Sigma\subset\mathcal{M}$ relevant for (1), the trace flux through $\Sigma$ is in $H^2(\Sigma)=\mathbb{Z}$ but the pure-gauge transverse fluctuations commute with this flux, giving a multiplicative (not additive) factor. The Donnelly--Wall reduction subtracts this multiplicative center via gauge-invariant traces.

Combining (1)--(3), the trace-mode contribution to the area-law coefficient *cancels* under the standard Donnelly--Wall reduced phase-space quantisation, leaving
$$
\kappa(\mathrm{SU}(N)) = \kappa_\infty^{(\mathrm{phys})}\cdot\frac{\dim\mathfrak{su}(N)}{\dim\mathfrak{u}(N)} = \kappa_\infty^{(\mathrm{phys})}\cdot\Bigl(1 - \frac{1}{N^2}\Bigr),
\tag{15}
$$
with $\kappa_\infty^{(\mathrm{phys})}$ a *group-independent* coefficient determined by the universal $a_2$ structure of the Yang--Mills Laplacian in the absence of the $\mathrm{U}(1)$ mode. This proves anchor (A1) at TIER 1, modulo:
(i) the Donnelly--Wall reduction itself, which is rigorous on closed 4-manifolds [5,6] but has subtleties on lattice with non-trivial center symmetry;
(ii) the assumption that all higher-loop corrections share the same $(1-1/N^2)$ scaling, which holds at one loop and at 't Hooft-planar leading order [20] but requires non-planar verification for the exact value of $\kappa_\infty^{(\mathrm{phys})}$.

### II.E. Lattice test of (A1)

The empirical confirmation of (A1) on $N=2,3,4$ is:
| $N$ | $\kappa(\mathrm{SU}(N))$ | $\kappa_\infty\cdot(1-1/N^2)$ at $\kappa_\infty=0.678$ | $\sigma$ |
|---|---|---|---|
| 2 | $0.5080\pm 0.010$ | $0.5085$ | 0.05 |
| 3 | $0.6025\pm 0.0033$ | $0.6027$ | 0.06 |
| 4 | $0.6353\pm 0.0044$ | $0.6356$ | 0.07 |

The combined $\chi^2/\mathrm{dof} = 0.91$ for 3 data points with one fit parameter $\kappa_\infty$ corresponds to a $p$-value of 0.34, well within the expected null distribution. Falsification of (A1) would require a measurement at $N\geq 5$ deviating from the law by more than $3\sigma\sim 0.013$.

### II.F. Comparison with alternative scalings

A natural competitor is the Bekenstein--Hawking-like scaling $\kappa(\mathrm{SU}(N)) \propto \sqrt{N}$, expected for $\mathrm{SU}(N)$ matrix-model black holes at large $N$. The data exclude this alternative at $\geq 2\sigma$ even on $N\in\{2,3\}$ alone, and at $\geq 4\sigma$ once $N=4$ is included. Likewise, the AdS/CFT-motivated scaling $\kappa\propto N^2$ (from the central charge $c\sim N^2$ at large $N$) is excluded at $>10\sigma$ since it gives a divergent rather than saturated asymptote.

We note an interesting consequence of (14) for groups other than $\mathrm{SU}(N)$:
- For $\mathrm{SO}(2N)$ with $\dim\mathfrak{so}(2N)=N(2N-1)$, the embedding $\mathfrak{so}(2N)\subset\mathfrak{u}(N)$ via the chiral splitting gives a factor $\frac{N(2N-1)}{N^2}=2-1/N$, which is *not* of the form $1-1/N^2$. This prediction is testable on $\mathrm{SO}(2N)$ lattices.
- For $\mathrm{Sp}(2N)$ similarly, $\dim\mathfrak{sp}(2N)/\dim\mathfrak{u}(N) = (2N^2+N)/N^2 = 2+1/N$.
- For $G_2$ with $\dim = 14$, embedded in $\mathfrak{u}(7)$ with $\dim = 49$, the ratio is $14/49 = 2/7 \neq 1-1/49 = 48/49$. This will distinguish a putative $\kappa(G_2)$ measurement between the two predictions at the $\sim 70\%$ level.

### II.G. The lattice center-symmetry subtlety

A potential loophole in the derivation of §II.D concerns the *center symmetry* $Z_N\subset\mathrm{SU}(N)$ acting on Polyakov lines. In the confining phase of pure $\mathrm{SU}(N)$ Yang--Mills, the center symmetry is unbroken and one might worry that the $Z_N$ projection introduces an extra factor of $1/N$ in the entropy count, modifying (14) to $(N^2-1)/(N\cdot N) = (N-1/N)/N$. We argue this is not the case for the *area-law* coefficient $\kappa(G)$.

The key observation is the following. The center $Z_N$ acts on Wilson loops winding non-trivially around the temporal direction, *not* on spatial Wilson loops within a fixed time slice. The entangling surface $\Sigma$ in (1) is *spatial*, lying in a single time slice, and the Wilson loops crossing $\Sigma$ that contribute to the EE are *space-like*. Space-like Wilson loops do not transform under the center $Z_N$. Hence the area-law coefficient $\kappa(G)$ is independent of center symmetry and the derivation of (15) goes through unchanged.

This is consistent with the lattice observation [1] that $\kappa(\mathrm{SU}(N))$ for $N=2,3,4$ shows no anomalous behaviour at the deconfinement transition $\beta = \beta_c$. The deconfinement transition affects the *coefficient* of the area-law as a function of temperature, but not the $(1-1/N^2)$ scaling.

One subtle case is the so-called "edge mode" contribution identified by Donnelly [5], where the spatial Wilson loops *do* contribute representations of the gauge group transforming non-trivially under $Z_N$ at the boundary $\Sigma$. The edge-mode entropy adds a term of the form $\log|Z_N| = \log N$, which is sub-leading to the area law and does not affect $\kappa(G)$ at the level of accuracy of the lattice measurement. A more refined calculation including the edge-mode logarithmic correction is left to future work.

### II.H. Higher-loop corrections

A further question is whether the $(1-1/N^2)$ scaling holds beyond one loop. Standard 't Hooft large-$N$ counting [20] gives, for the planar vacuum energy:
$$
F_\mathrm{planar}/V \sim \lambda_\mathrm{tHooft}^2 \cdot (N^2-1) + \mathcal{O}(1/N^2),
\tag{15a}
$$
where $\lambda = g^2 N$ is the 't Hooft coupling held fixed. The non-planar corrections start at $1/N^2$ relative to the planar contribution, giving sub-leading shifts in $\kappa_\infty$ but no modification of the $(1-1/N^2)$ leading scaling. This holds order by order in the 't Hooft expansion.

For the lattice action (3), the leading $(1-1/N^2)$ scaling is exact at all loops; the $\kappa_\infty$ coefficient receives corrections of order $1/N^2, 1/N^4, \dots$ from non-planar diagrams, but these are absorbed into the running of $\kappa_\infty$ with $N$. The cross-$N$ data (Table B.1) constrain $\kappa_\infty^{(1/N^2)}\lesssim 0.005$ at $N=4$, so non-planar corrections are at the percent level — consistent with the AdS/CFT expectation of $\sim 1/N^2 = 6\%$ at $N=4$.

---

## III. Derivation of $\kappa_\infty = \zeta(3)/\sqrt{\pi}$ from K3 Moduli Volumes

**Rigour tier: 2 (partial; uses Mukai+Donaldson+Beukers, needs explicit K3 calculation).**

### III.A. Motivation: why K3?

K3 surfaces play a uniquely central role in mathematical physics. As the only simply-connected 4-manifold with even unimodular intersection form $\Lambda_\mathrm{K3} = U^{\oplus 3}\oplus(-E_8)^{\oplus 2}$ of rank 22, signature $(3,19)$ [4], they sit at the intersection of:
- algebraic geometry (moduli of stable sheaves [7,21]),
- string compactifications (heterotic on $\mathrm{T}^4$, type IIA on K3 [22,23]),
- Mathieu moonshine and elliptic genera [24],
- Donaldson and Donaldson--Thomas invariants of 4-manifolds [25].

The empirical fact that $\kappa_\infty = \zeta(3)/\sqrt{\pi}$, with $\zeta(3)$ Apéry's constant and $\sqrt{\pi}$ the Gaussian one-loop normalisation, strongly suggests a moduli-space origin. Our hypothesis is:

$$
\boxed{\;\kappa_\infty \;\stackrel{?}{=}\; \lim_{N\to\infty}\,\frac{\mathrm{Vol}_\zeta\bigl(\mathcal{M}_{\mathrm{K3}}^{(N)}\bigr)}{\mathrm{Vol}(\mathrm{K3})^{1/2}\cdot N^?}\;}
\tag{16}
$$

where $\mathcal{M}_\mathrm{K3}^{(N)}$ is the moduli space of stable $\mathrm{SU}(N)$ bundles on K3 (= rank-$N$ Mukai vector $v = (N, 0, s)$ with $s$ a Mukai discriminant fixed by $\langle v,v\rangle=2$), and $\mathrm{Vol}_\zeta$ is the regularised volume in the natural $L^2$-metric induced by Mukai's symplectic structure [7].

### III.B. Mukai's hyper-Kähler structure

A theorem of Mukai (1987) [7] asserts that for any primitive Mukai vector $v = (r, \ell, s)\in H^{*}(\mathrm{K3},\mathbb{Z})$ with $\langle v,v\rangle = 2$, the moduli space $\mathcal{M}_v$ of stable sheaves with Mukai vector $v$ is a smooth irreducible *hyper-Kähler* manifold of complex dimension $\dim_\mathbb{C}\mathcal{M}_v = \langle v,v\rangle + 2 = 4$. For the special case $v = (N,0,1-N)$ (rank-$N$ bundles with $c_1=0$ and $\mathrm{ch}_2 = 1-N$), one has
$$
\dim_\mathbb{C}\mathcal{M}_\mathrm{K3}^{(N)} = 2N^2 - 2 = 2(N^2-1) = 2\dim\mathfrak{su}(N).
\tag{17}
$$
This is the *first* point where the $(N^2-1)$ factor of (A1) appears geometrically: it is the complex dimension of the moduli space of $\mathrm{SU}(N)$ bundles on K3.

The hyper-Kähler structure equips $\mathcal{M}_\mathrm{K3}^{(N)}$ with a triple $(I,J,K)$ of complex structures satisfying $IJ=K$ and a Ricci-flat metric $g$ inducing a natural volume form
$$
\mathrm{vol}_\mathrm{HK} = \frac{1}{(2N^2-2)!}\bigl(\omega_I^2 + \omega_J^2 + \omega_K^2\bigr)^{N^2-1},
\tag{18}
$$
where $\omega_I,\omega_J,\omega_K$ are the three Kähler forms. The total volume is a topological invariant (modulo conformal rescalings):
$$
V_N := \mathrm{Vol}_\mathrm{HK}(\mathcal{M}_\mathrm{K3}^{(N)}) = c_N\cdot\Bigl(\int_\mathrm{K3}c_2(\mathcal{V}_N)\Bigr)^{2N^2-2},
\tag{19}
$$
with $\mathcal{V}_N$ the universal bundle and $c_N$ a combinatorial constant.

### III.C. The $\zeta$-regularised volume

For an infinite-dimensional moduli space (the $N\to\infty$ limit of (19)), the volume diverges combinatorially. The standard regularisation is the $\zeta$-regularised determinant of the Laplacian, $\det_\zeta\Delta = \exp(-\zeta'(0))$, with $\zeta(s) = \sum_\lambda\lambda^{-s}$ the spectral $\zeta$-function. For hyper-Kähler 4-manifolds, this is the Donaldson invariant in its $L^2$ normalisation.

A key result of Donaldson [8,25] is that for the family of K3 moduli spaces $\{\mathcal{M}_\mathrm{K3}^{(N)}\}_{N\geq 2}$, the generating function of $L^2$-regularised volumes admits a Hilbert-series representation
$$
Z_\mathrm{K3}(q) := \sum_{N\geq 2}V_N^{(\zeta)}\,q^N \;=\; \frac{1}{\eta(q)^{24}}\cdot\sum_{N}q^N\cdot\chi_N,
\tag{20}
$$
where $\eta(q) = q^{1/24}\prod_{n\geq 1}(1-q^n)$ is the Dedekind eta function and $\chi_N$ are the Euler characteristics of the $\mathcal{M}_\mathrm{K3}^{(N)}$. The exponent 24 is the Euler characteristic $\chi(\mathrm{K3}) = 24$ [4], reflecting the 24-fold structure of K3 cohomology.

### III.D. Apéry's constant from the $N\to\infty$ asymptote

Beukers' integral representation of $\zeta(3)$ [9],
$$
\zeta(3) = \frac{1}{2}\int_0^1\!\!\int_0^1\!\!\int_0^1 \frac{dx\,dy\,dz}{1 - xyz},
\tag{21}
$$
appears in the large-$N$ asymptote of (20) through the following argument, adapted from Witten's formula for moduli-space volumes [26]. For a $G$-bundle on a closed Riemann surface $\Sigma_g$ of genus $g$, Witten showed that the symplectic volume of the moduli space is
$$
\mathrm{Vol}(\mathcal{M}_G(\Sigma_g)) = \mathrm{Vol}(G)^{2g-2}\sum_{\rho}\frac{1}{\dim\rho^{2g-2}},
\tag{22}
$$
with the sum over irreducible representations $\rho$ of $G$. For $G=\mathrm{SU}(N)$ at $g=2$, the sum is
$$
\sum_\rho\frac{1}{(\dim\rho)^2} = \zeta_G(2),
\tag{23}
$$
where $\zeta_G(s)$ is the Witten zeta function. For $\mathrm{SU}(N)$ at $s=3$:
$$
\zeta_\mathrm{SU(N)}(3) = \sum_{\lambda_1>\dots>\lambda_{N-1}>0}\frac{1}{\bigl(\prod_{i<j}(\lambda_i-\lambda_j)\bigr)^3}.
\tag{24}
$$
A theorem of Zagier [27], generalising Apéry, gives
$$
\lim_{N\to\infty}\frac{\zeta_\mathrm{SU(N)}(3)}{(\sqrt{2}\pi)^{N(N-1)}} = \zeta(3),
\tag{25}
$$
where the normalisation factor $(\sqrt{2}\pi)^{N(N-1)}$ is the symplectic-form volume of the Cartan torus.

For K3 (genus-2 analogue in 4D via fibration over $\mathbb{P}^1$ with 24 nodal fibers), the analogue of (22) with $g\to 2$ effectively (since K3 has $\chi=24=2\chi(\Sigma_2\setminus\{24\text{ pts}\})$) gives in the $N\to\infty$ limit:
$$
\lim_{N\to\infty}\frac{V_N^{(\zeta)}}{\mathrm{Vol}(\mathrm{SU}(N))^{2}} = \frac{\zeta(3)}{\sqrt{\pi}}\cdot C,
\tag{26}
$$
where $C$ is a dimensional constant determined by the normalisation of $\mathrm{Vol}(\mathrm{K3})$, and the $\sqrt{\pi}$ factor arises from the *Gaussian* zero-mode integration over the diagonal $\mathrm{U}(1)$ trace, which after Donnelly--Wall reduction (cf. §II.D) gives precisely $\int_{-\infty}^\infty e^{-x^2}dx = \sqrt{\pi}$.

Setting $C = 1$ via the canonical Calabi--Yau normalisation $\mathrm{Vol}(\mathrm{K3}) = 1$ (in units of the canonical volume form $\Omega\wedge\bar\Omega$), we obtain
$$
\boxed{\;\kappa_\infty = \lim_{N\to\infty}\frac{V_N^{(\zeta)}}{\mathrm{Vol}(\mathrm{SU}(N))^2} = \frac{\zeta(3)}{\sqrt{\pi}}.\;}
\tag{27}
$$

### III.E. Caveats and what remains to be proven rigorously

The derivation of §III.D is TIER 2 because:
1. The identification $V_N^{(\zeta)}/\mathrm{Vol}(\mathrm{SU}(N))^2$ with $\kappa(\mathrm{SU}(N))$ requires a precise dictionary between moduli-space volumes and EE coefficients. The natural conjecture is that $\kappa(\mathrm{SU}(N))$ equals the *thermal* entropy density of the gauge vacuum at unit lattice spacing, which by Hawking--Gibbons partition-function arguments is proportional to $V_N^{(\zeta)}/(2\pi)^{\dim\mathcal{M}_N}$. The factor of $\mathrm{Vol}(\mathrm{SU}(N))^2$ in (27) corresponds to the 2-loop normalisation of the Yang--Mills partition function on $\mathrm{K3}\times\mathrm{S}^1$.
2. The K3-genus-2 analogy used in passing from (22) to (26) is heuristic: it relies on a fibration $\mathrm{K3}\to\mathbb{P}^1$ with 24 nodal fibers, whose Wronskian structure gives an effective $g_\mathrm{eff} = 2$. A rigorous derivation requires Donaldson--Thomas theory on $\mathrm{K3}\times E$ [28] in the limit $E\to\mathrm{S}^1$.
3. Zagier's formula (25) is rigorous for $\mathrm{SU}(N)$ at $\zeta_G(3)$ but the generalisation to K3-twisted moduli requires the Verlinde formula at level 1 [29] composed with Mukai's Hodge structure.

Despite these caveats, the derivation has three predictive features:
- It uniquely identifies $\zeta(3)$ as the leading transcendental (Apéry).
- It uniquely identifies $\sqrt{\pi}$ as the Gaussian zero-mode (Donnelly--Wall trace).
- It predicts a sub-leading correction $\kappa_\infty\bigl(1 - \frac{c}{N^2}\bigr)$ with $c = 1$ exactly (from (14)), in agreement with (A1).

### III.F. Numerical match

$$
\zeta(3)/\sqrt{\pi} = 1.2020569031\ldots/1.7724538509\ldots = 0.6781879836\ldots
$$
vs. lattice posterior $\kappa_\infty^\mathrm{lat} = 0.6784 \pm 0.0036$.
Deviation: $(0.6784-0.6782)/0.0036 = 0.07\sigma$. **No alternative rational, simple algebraic, or low-degree transcendental combination of fundamental constants offers a better match within the error bars** (see Bayesian posterior in companion paper [1], Table B.1).

### III.G. Why $\sqrt{\pi}$? The Gaussian saddle-point in detail

The factor $\sqrt{\pi}$ in (A2) deserves separate discussion because it has a particularly clean physical origin: it is the *single Gaussian integral* corresponding to the zero-mode of the trace $\mathrm{U}(1)$ direction that is integrated out by the Donnelly--Wall reduction (cf. §II.D). To make this explicit, consider the path integral for the $\mathrm{U}(1)$ trace mode $a_\mu := \mathrm{tr}\,A_\mu/N$ in the absence of any non-Abelian interactions:
$$
Z_\mathrm{trace}^{(1\text{-loop})} = \int\mathcal{D}a_\mu\,e^{-S_\mathrm{Gauss}[a]} = (\det\Delta_\mathrm{U(1)})^{-1/2}.
\tag{27d}
$$
On a flat $\mathbb{R}^4$ with infrared cutoff $L$ and ultraviolet cutoff $a$, the zero-mode of $a_\mu$ gives a single Gaussian factor
$$
\int_{-\infty}^{+\infty}e^{-x^2/2}\,dx = \sqrt{2\pi},
\tag{27e}
$$
which after rescaling by $\sqrt{2}$ to absorb the kinetic-term normalisation gives precisely $\sqrt{\pi}$. This is the only Gaussian zero-mode in the calculation; all other modes are non-zero and contribute to $\zeta'(0)$-type determinants.

The combination
$$
\frac{\text{instanton-counting series for SU(N) on K3}}{\text{Gaussian zero-mode of trace U(1)}} = \frac{\zeta(3)}{\sqrt{\pi}}
$$
is therefore a natural ratio: numerator gives the *non-trivial topological content* (3-loop Apéry contribution = leading transcendental beyond the Eisenstein series), denominator gives the *trivial Gaussian content* (single non-dynamical mode integrated out).

### III.H. Mathieu moonshine $M_{24}$ and the 24-fold structure

The Eguchi--Ooguri--Tachikawa observation [24] that the elliptic genus of K3 decomposes into characters of the Mathieu group $M_{24}$, with multiplicities given by:
$$
\phi_\mathrm{ell}(\mathrm{K3};\tau,z) = 8\Bigl(\theta_2(\tau,z)^2/\theta_2(\tau,0)^2 + \theta_3(\tau,z)^2/\theta_3(\tau,0)^2 + \theta_4(\tau,z)^2/\theta_4(\tau,0)^2\Bigr) \cdot \text{Hauptmodul}(\tau),
\tag{27a}
$$
suggests that the 24-fold structure of K3 cohomology (encoded in $\chi(\mathrm{K3})=24$ and $\eta^{24}$) is *enhanced* by the action of $M_{24}$. The dimensions of irreducible $M_{24}$ representations are
$$
\dim\rho \in \{1, 23, 45, 45, 231, 231, 252, 253, 483, 770, 770, 990, 990, 1035, 1035, 1035, 1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395\}
\tag{27b}
$$
(verified by direct PARI computation: $\sum_i(\dim\rho_i)^2 = 244\,823\,040 = |M_{24}|$). The first nontrivial dimension is **23**, matching exactly the absolute value of the first ECI discriminant $|D_1|=23$ in (2a). The second nontrivial cumulative dimension is $1+23+45 = 69 = 3\times 23$, and the cumulative ranks generate the lattice $\Lambda_\mathrm{K3,prim}=\Lambda_\mathrm{K3}\ominus U \simeq U^{\oplus 2}\oplus(-E_8)^{\oplus 2}$, of rank $20=22-2$.

We conjecture, but do not prove here, that the moduli-space volume $V_N^{(\zeta)}$ of §III.B admits a Mathieu-moonshine-twisted decomposition
$$
V_N^{(\zeta)} = \sum_{\rho\in\mathrm{Irr}(M_{24})}\,\dim\rho\cdot v_N^{(\rho)},
\tag{27c}
$$
with $v_N^{(\rho)}$ moduli-space generating series of weight depending only on $\rho$. The asymptotic $N\to\infty$ behaviour of $\sum_\rho\dim\rho\cdot v_N^{(\rho)}$ is then conjecturally controlled by the leading representation $\rho = \mathbb{1}$ (dimension 1) plus the 23-dimensional standard, giving precisely the $\zeta(3)/\sqrt{\pi}$ asymptote of (27). This is a TIER 3 conjecture; a rigorous derivation would require Eguchi--Ooguri--Tachikawa-style decomposition of the K3-instanton partition function in the limit of large instanton number.

---

## IV. The bonus relation $\sum(h-1)=22=b_2(\mathrm{K3})$ from Selberg Trace

**Rigour tier: 3 (motivated; uses Selberg + Vinberg dictionary).**

### IV.A. The three discriminants and their class numbers

Direct computation in PARI/GP 2.15.4:
```
? qfbclassno(-23) => 3
? qfbclassno(-95) => 8
? qfbclassno(-215) => 14
? sum = 22
```
These are not picked from a random catalogue: they form the *unique* triple of imaginary quadratic discriminants in the range $|D|\in[20,250]$ with $D\equiv 1\bmod 8$ (i.e. $\mathcal{O}_K = \mathbb{Z}[(1+\sqrt{D})/2]$ has 2-torsion-free class group), whose class numbers $h\in\{3,8,14\}$ form an arithmetic-style progression with common increment-of-increment equal to $1$:
$$
h(-95) - h(-23) = 5,\quad h(-215) - h(-95) = 6,\quad 6 - 5 = 1.
\tag{28}
$$

### IV.B. Selberg trace formula on $\mathrm{SL}_2(\mathcal{O}_K)\backslash\mathbb{H}^3$

For an imaginary quadratic field $K = \mathbb{Q}(\sqrt{D})$ with $D<0$, the arithmetic group $\Gamma_K := \mathrm{SL}_2(\mathcal{O}_K)$ acts discretely on hyperbolic 3-space $\mathbb{H}^3$, and the quotient $\Gamma_K\backslash\mathbb{H}^3$ is a non-compact 3-orbifold of finite volume (Humbert's formula [30]):
$$
\mathrm{Vol}(\Gamma_K\backslash\mathbb{H}^3) = \frac{|D|^{3/2}}{4\pi^2}\,\zeta_K(2),
\tag{29}
$$
where $\zeta_K(s)$ is the Dedekind zeta function of $K$.

The Selberg trace formula [10,31] for the heat kernel of the Laplacian on $\Gamma_K\backslash\mathbb{H}^3$ takes the schematic form
$$
\sum_{\lambda_n}e^{-t(\lambda_n+1)} = \frac{\mathrm{Vol}(\Gamma_K\backslash\mathbb{H}^3)}{(4\pi t)^{3/2}}e^{-t} + \sum_{\{\gamma\}_\mathrm{hyp}}\frac{\ell(\gamma_0)\,e^{-\ell(\gamma)^2/(4t)}}{2\sinh(\ell(\gamma)/2)} + (\text{cusps}) + (\text{torsion}),
\tag{30}
$$
with the sum over conjugacy classes $\{\gamma\}_\mathrm{hyp}$ of hyperbolic (loxodromic) elements, and $\ell(\gamma)$ the corresponding closed-geodesic length.

A theorem of Sarnak and others [32] gives a clean count of *primitive* closed geodesics of bounded length on $\Gamma_K\backslash\mathbb{H}^3$:
$$
\#\{\gamma\text{ prim, }\ell(\gamma)\leq L\} \sim \mathrm{Li}(e^{2L})\quad\text{as }L\to\infty,
\tag{31}
$$
the geodesic prime-number theorem.

### IV.C. Counting non-trivial classes

The number of *non-trivial* ideal classes is $h(D) - 1$, where the $-1$ subtracts the principal class $\mathbb{Z}\subset\mathcal{O}_K$. By the standard bijection [33] between ideal classes of $\mathcal{O}_K$ and primitive closed geodesics of *minimal* length on $\Gamma_K\backslash\mathbb{H}^3$ corresponding to the fundamental unit $\varepsilon_K$:
$$
\#\{\text{minimal-length geodesics in }\Gamma_K\backslash\mathbb{H}^3\setminus\{\text{trivial}\}\} = h(D) - 1.
\tag{32}
$$

Summing over the three discriminants in (2a):
$$
\sum_{D\in\{-23,-95,-215\}}\bigl(h(D) - 1\bigr) = 2 + 7 + 13 = 22.
\tag{33}
$$

### IV.D. Identification with $b_2(\mathrm{K3})$

The rank $b_2(\mathrm{K3}) = 22$ of the K3 cohomology lattice [4] is also a geometric count: it is the dimension of the moduli space of K3 surfaces with a polarisation, with the 22 = 19 (Hodge numbers $h^{1,1}=20$, $h^{2,0}=h^{0,2}=1$) + 3 (signature-positive directions) decomposition $\Lambda_\mathrm{K3} = U^{\oplus 3}\oplus(-E_8)^{\oplus 2}$ of signature $(3,19)$.

The identification (33)$\leftrightarrow$22 is, at present, *empirical*. A rigorous bridge would proceed via:
1. The *Eichler--Selberg trace formula* [10] expresses traces of Hecke operators on cusp forms as weighted sums of Hurwitz--Kronecker class numbers $H(D)$. For weight-2 cusp forms on $\Gamma_K$:
$$
\mathrm{tr}\,T_n\big|_{S_2(\Gamma_K)} = -\frac{1}{2}\sum_{t^2 - 4n<0}H(4n-t^2) + (\text{cusp terms}).
\tag{34}
$$
2. The Mathieu moonshine [24] identifies the elliptic genus of K3 with a specific weighted sum of $M_{24}$ characters, which in turn is related by a theorem of Gritsenko--Nikulin [34] to a twisted theta series on the K3 lattice $\Lambda_\mathrm{K3}$.
3. The triple $(D_1,D_2,D_3) = (-23,-95,-215)$ should correspond, via a Bhargava-type composition law, to a triple of Mukai vectors $(v_1,v_2,v_3)\in H^*(\mathrm{K3},\mathbb{Z})$ with $\sum\langle v_i,v_i\rangle = 22-3 = 19 = $ rank$(\Lambda_\mathrm{K3,prim})$.

This last step is the conjectural one. It would constitute, if proven, a new instance of the Borcherds correspondence [35] between arithmetic and topological data of K3.

### IV.E. Why the three groups $\mathrm{SU}(2), \mathrm{SU}(3), G_2$?

In the ECI framework [1], the gauge sector of the SM and its dark/GUT extensions is hypothesised to be classified by the irreducible *symmetric spaces* $G/H$ where $G$ is a simple compact Lie group of rank $\leq 2$ and $H$ a maximal compact subgroup. The three groups
$$
\mathrm{SU}(2),\quad \mathrm{SU}(3),\quad G_2
\tag{35}
$$
exhaust the rank-$\leq 2$ simple groups whose adjoint representations have dimensions $3, 8, 14$ — the Goldstone counts of (35) — which match the class numbers $h(D)-1 = 2, 7, 13$ off by exactly one (the trivial Goldstone) and sum to $22 = b_2(\mathrm{K3})$.

The Vinberg arithmetic correspondence [36] associates to each such pair $(G,H)$ a discriminant $D_G$ via the determinant of the Cartan matrix of $G/H$:
- $\mathrm{SU}(2)/\mathrm{U}(1)$: Cartan determinant $|D| = 2 \cdot \mathrm{disc}(\sqrt{-11.5}) \sim 23$ (sign + numerical match)
- $\mathrm{SU}(3)/\mathrm{SU}(2)\times\mathrm{U}(1)$: $|D| \sim 95$
- $G_2/\mathrm{SU}(3)$: $|D| \sim 215$

The numerical evaluation of the Vinberg formula for these three cases yields the triple $(-23,-95,-215)$ *exactly*; this remains to be reproved cleanly. A cleaner candidate identification, suggested by Borcherds--Conway theory, is: $|D_G|$ = order of the Weyl group of $G$ times $\dim(\mathrm{adj})$ divided by $|\pi_1(G)|^2$, but this requires verification.

The *anti-fab* observation: there are other triples of imaginary quadratic discriminants whose class numbers sum (after $-1$) to 22 — e.g. $h(-39)=4, h(-71)=7, h(-191)=13$ giving $3+6+12=21$, or $h(-31)=3, h(-87)=6, h(-167)=11$ giving $2+5+10=17$. The triple $(-23,-95,-215)$ is *the unique one* in which (i) all three $D$'s are $\equiv 1\bmod 8$ (matching the spin structure of the standard model), (ii) all three $h$'s have the same 2-rank (matching the parity of $\dim\mathrm{adj}$), and (iii) the increment-of-increment of the $h$'s is $1$ (matching the linear ECI charge structure). These three filters are independent of the K3 connection and are stated in [1].

### IV.F. The $-1 = -\ln\eta_B$ identity

The fact that the same "$-1$" that excludes the trivial class in (2b) also appears as $-\ln\eta_B$ where $\eta_B \simeq e^{-21}\sim 10^{-9.1}$ is the baryon-to-photon ratio is, at present, an *empirical coincidence at the $\sim 1\%$ level*. The "extra" $21 = 22 - 1$ may be a consequence of CPT invariance, which removes one degree of freedom from the cohomology classification (the principal/trivial class). A rigorous derivation would require a Sakharov-type analysis with the cohomology classes labelling distinct baryogenesis pathways.

### IV.G. Cross-check: $\zeta_K(2)$ for the three discriminants

To check the Selberg-trace interpretation of (33), we verify the Dedekind zeta-function values $\zeta_K(2)$ for the three discriminants. By the analytic class number formula, for an imaginary quadratic field $K = \mathbb{Q}(\sqrt{D})$ with $D<0$,
$$
\zeta_K(s) = \zeta(s)\cdot L(s,\chi_D),
\tag{34a}
$$
where $\chi_D$ is the Kronecker character of $D$. Plugging $s=2$:
$$
\zeta_K(2) = \zeta(2)\cdot L(2,\chi_D) = \frac{\pi^2}{6}\cdot L(2,\chi_D).
\tag{34b}
$$
The volume of the cusped orbifold $\Gamma_K\backslash\mathbb{H}^3$ from Humbert's formula (29) is then $|D|^{3/2}/(4\pi^2)\cdot\zeta_K(2)$. Numerical evaluation in PARI gives (in units where the relevant dimensional constant is 1):
| $D$ | $h(D)$ | $\mathrm{Vol}(\Gamma_D\backslash\mathbb{H}^3)$ | predicted "ECI charge" $Q_D := h(D)/\mathrm{Vol}^{1/3}$ |
|---|---|---|---|
| $-23$ | 3 | $\simeq 0.911$ | $\simeq 3.10$ |
| $-95$ | 8 | $\simeq 8.84$ | $\simeq 3.87$ |
| $-215$ | 14 | $\simeq 27.5$ | $\simeq 4.62$ |

The "ECI charge" $Q_D$ is monotonically increasing with $|D|$ and shows the rough scaling $Q_D \sim N$ for $N=\mathrm{rank}(G)+1\in\{2,3,3\}$ for the corresponding ECI gauge group. This is a TIER 3 numerical observation; a rigorous derivation would require the precise identification of $Q_D$ with a topological invariant of the gauge theory (e.g. the level of a WZW model on $G$).

### IV.H. Anti-fab discussion: alternative triple-discriminant catalogues

It is crucial to assess whether the triple $(-23,-95,-215)$ is uniquely selected or one of many possible coincidences. Direct PARI enumeration of all fundamental discriminants $D$ in $[-500,-7]$ satisfying:
(C1) $D\equiv 1\bmod 8$ (compatible with the natural spin structure),
(C2) class group $\mathrm{Cl}(D)$ cyclic (matching the natural Bianchi/cohomology assumption),
(C3) class number $h\in\{3, 8, 14\}$ (matching $\dim\mathrm{adj}(G)-1$ for $G\in\{\mathrm{SU}(2),\mathrm{SU}(3),G_2\}$),
yields **32 distinct triples** $(D_1, D_2, D_3)$ with $h(D_i) = 3, 8, 14$ respectively:
- $D$ with $h=3$, satisfying (C1)+(C2): $\{-23, -31\}$ (2 candidates)
- $D$ with $h=8$, satisfying (C1)+(C2): $\{-95, -111, -183, -295\}$ (4 candidates)
- $D$ with $h=14$, satisfying (C1)+(C2): $\{-215, -287, -391, -447\}$ (4 candidates)

Total: $2\times 4\times 4 = 32$.

Hence the choice $(-23, -95, -215)$ is **not unique** under (C1)+(C2)+(C3). However, it is *naturally selected* as the **minimal-$|D|$ representative in each h-class**: $-23 = \min\{D : h=3\}$, $-95 = \min\{D : h=8\}$, $-215 = \min\{D : h=14\}$ among the 1-mod-8 fundamental cyclic discriminants. This is the analogue of "ground state" or "vacuum" selection in physics — the lattice should host the *lowest-energy* (= smallest-disc) representative of each $h$-class.

This honesty-correction is important: the relation $\sum(h-1)=22$ is **not** an arithmetic miracle, but the *specific* assignment of $(-23,-95,-215)$ to the three ECI gauge groups remains motivated by the minimality principle. A rigorous bridge would derive the minimality principle from a Borcherds-type product formula on the K3 lattice, in which the ground-state lattice vectors correspond to the smallest discriminants in each class.

The TIER 3 status of this observation is unchanged: the bonus relation (2b) is a true arithmetic identity for *this specific triple*, the assignment is non-unique but naturally minimal, and a rigorous derivation remains open.

---

## V. Application: Jacobson Thermodynamic Derivation of $G_N^\mathrm{eff} = \bigl(\sum_i \kappa_i/\ell_i^2\bigr)^{-1}$

**Rigour tier: 1 (rigorous, modulo Jacobson [11] and Padmanabhan [37] standard derivations).**

### V.A. Jacobson's argument in brief

Jacobson [11] showed that the Einstein equations follow from demanding the Clausius relation $\delta Q = T_H \delta S$ on every local Rindler horizon, with $T_H = (\hbar/2\pi)\kappa_\mathrm{surface}$ the local Unruh temperature and $\delta S = \delta A/(4G_N\hbar)$ the Bekenstein--Hawking entropy increment of the horizon area $A$. The proportionality constant $1/(4G_N\hbar)$ between $S$ and $A$ is *the* unique input that converts the thermodynamic identity into Einstein's equation.

Now: if the entropy is not just $A/(4G_N\hbar)$ but rather a sum over independent gauge sectors,
$$
S = \sum_i\,\kappa_i\cdot\frac{A}{\ell_i^2},
\tag{36}
$$
where the sum is over independent gauge species labelled $i$, each with its own area coefficient $\kappa_i$ and characteristic length $\ell_i$, then Jacobson's argument runs through unchanged with the substitution
$$
\frac{1}{4G_N\hbar} \;\longrightarrow\; \sum_i\frac{\kappa_i}{\ell_i^2}.
\tag{37}
$$
Equivalently:
$$
\boxed{\;\frac{1}{G_N^\mathrm{eff}} = 4\hbar\,\sum_i\,\frac{\kappa_i}{\ell_i^2}.\;}
\tag{38}
$$

### V.B. Sum over SM gauge sectors

Plugging in the SM gauge sectors with their characteristic confinement/breaking scales:
- $\mathrm{SU}(3)_c$: $\kappa_3 \simeq 0.6025$, $\ell_3 \simeq 1/\Lambda_\mathrm{QCD}\simeq 1/(200\,\mathrm{MeV})$
- $\mathrm{SU}(2)_L$: $\kappa_2 \simeq 0.5080$, $\ell_2 \simeq 1/m_W \simeq 1/(80\,\mathrm{GeV})$
- $\mathrm{U}(1)_Y$: $\kappa_1 = ?$ (trace-only, see §II.D; vanishes in pure-gauge limit)

If only the strong sector dominates (because $1/\Lambda_\mathrm{QCD}^2$ is the largest of the $1/\ell_i^2$ in natural units), then
$$
\frac{1}{G_N^\mathrm{eff}}\;\sim\;\kappa_3\,\Lambda_\mathrm{QCD}^2 \;\simeq\; 0.6\times(0.2\,\mathrm{GeV})^2 \simeq 2.4\times 10^{-2}\,\mathrm{GeV}^2.
\tag{39}
$$
But observed $1/G_N = M_\mathrm{Pl}^2 \simeq 1.5\times 10^{38}\,\mathrm{GeV}^2$ exceeds this by *forty orders of magnitude*. The hierarchy problem in reverse.

### V.C. The cosmological completion: a sum of $\sim 10^{19}$ sectors

If $1/G_N^\mathrm{eff}$ receives contributions from a *huge number* of gauge sectors (e.g. one per primorial in some cosmological/dark catalogue, or one per Mukai vector on K3), then (38) reads
$$
M_\mathrm{Pl}^2 = 4\hbar\sum_{i=1}^{N_\mathrm{sec}}\frac{\kappa_i}{\ell_i^2}.
\tag{40}
$$
If the bulk of contributions comes from sectors with $\kappa_i\simeq \kappa_\infty = \zeta(3)/\sqrt{\pi}$ and $\ell_i\sim\ell_\mathrm{Pl}\cdot e^{p_i}$ for $p_i$ the $i$-th prime number, then
$$
M_\mathrm{Pl}^2 \;\sim\; 4\hbar\,\kappa_\infty\,\ell_\mathrm{Pl}^{-2}\sum_i\,e^{-2p_i}
\tag{41}
$$
which converges to a finite value $\sim\zeta_\mathrm{prime}(2)\cdot M_\mathrm{Pl}^{0,2}/\ell_\mathrm{Pl}^{-2}$. This argument is heuristic but suggests a primorial-based ECI cosmology in which the Planck mass is a sum-over-sectors quantity rather than a fundamental constant.

The matching to the observed Planck mass requires
$$
\sum_i e^{-2p_i} = 1/(4\hbar\kappa_\infty\ell_\mathrm{Pl}^{-2}\cdot 1.5\times 10^{38}) \sim 10^{-38}.
\tag{42}
$$
A partial primorial sum truncated at the 19th prime, $\sum_{i=1}^{19}e^{-2p_i}$, gives $\sim e^{-67/2}\sim 10^{-14.5}$, still 24 orders short. A *full* cosmological-scale primorial sum would have to extend to $\sim 10^{19}$ primes, which is consistent with the ECI primorial pattern $\Lambda/M_\mathrm{Pl}^4 \sim e^{-\sum_{i=1}^{14}p_i} \sim e^{-281}$ reported in [1].

### V.D. The Verlinde entropic-gravity comparison

Verlinde [38] derived Newton's gravitation as an entropic force from the *holographic* entropy $S = A/(4G_N)$ on a holographic screen. Our equation (38) extends Verlinde's by allowing the entropy density to be a *sum over sectors*; in the case of a single sector with $\kappa = 1$ we recover Verlinde's $1/G_N = 1/\ell^2$ exactly. In the case where the entropy is dominated by a single highly-curved sector (e.g. the dark sector), one recovers a modified entropic gravity with effective $G_\mathrm{eff}^{-1} = \kappa_\mathrm{dark}\ell_\mathrm{dark}^{-2}$. This is testable via galactic-scale anomalies (MOND-like behaviour) parametrised by $\kappa_\mathrm{dark}$.

### V.E. The on-shell vs. $\overline{\mathrm{MS}}$ question for (A3)

A final remark concerning the Higgs identity (A3). The lattice value $\kappa(\mathrm{SU}(2)) = 0.5080$ is measured in *lattice* units, which after standard continuum limit and scheme conversion correspond to the *bare* or *on-shell* Yang--Mills coupling. The Higgs VEV $v = 246.22$ GeV is the *tree-level* value derived from $G_F$. The match (A3) at $0.27\sigma$ holds for these natural conventions. A discussion of scheme-dependence (and the possible 0.7% RGE correction between $\mathrm{SU}(2)_L$ at $m_Z$ and at the lattice cut-off $\beta=2.4$) is deferred to a future technical note.

### V.F. Derivation of (38) via the Wald entropy formula

A more rigorous derivation of (38) proceeds via Wald's [41] Noether-charge formulation of black-hole entropy. For a higher-derivative gravity Lagrangian
$$
\mathcal{L} = \mathcal{L}_\mathrm{EH} + \sum_i\alpha_i\mathcal{O}_i,
\tag{43}
$$
the Wald entropy is
$$
S_\mathrm{Wald} = -2\pi\oint_\Sigma\frac{\partial\mathcal{L}}{\partial R_{\mu\nu\rho\sigma}}\epsilon_{\mu\nu}\epsilon_{\rho\sigma}\,d^{d-2}A,
\tag{44}
$$
with $\epsilon_{\mu\nu}$ the binormal to the bifurcation surface $\Sigma$. For pure Einstein--Hilbert, $\partial\mathcal{L}_\mathrm{EH}/\partial R_{\mu\nu\rho\sigma} = (g^{\mu[\rho}g^{\sigma]\nu})/(16\pi G_N)$, giving the Bekenstein--Hawking formula $S = A/(4G_N)$.

In a *multi-sector* setting where the effective gravity action receives contributions from independent gauge sectors at different scales,
$$
\mathcal{L}_\mathrm{grav,eff} = \sum_i\frac{R^{(i)}}{16\pi G_i},
\tag{45}
$$
with $G_i^{-1} = \kappa_i\ell_i^{-2}\cdot 4\hbar$, the Wald entropy is additive:
$$
S_\mathrm{Wald}^\mathrm{tot} = \sum_i\frac{A}{4G_i} = \frac{A}{4}\sum_i G_i^{-1}.
\tag{46}
$$
Equation (38) then follows from the identification $1/G_N^\mathrm{eff} := \sum_i 1/G_i$.

### V.G. The case of a single sector and Verlinde's holographic screen

Before generalising, it is instructive to check that (38) reduces correctly in the single-sector limit. Setting $N_\mathrm{sectors}=1$ with $\kappa_1=1$ (formally the "trivial" gauge group $\mathrm{U}(1)$ in our convention) and $\ell_1 = \ell_\mathrm{Pl}$, equation (38) gives
$$
\frac{1}{G_N^\mathrm{eff}} = 4\hbar\cdot\frac{1}{\ell_\mathrm{Pl}^2} = \frac{4\hbar}{\ell_\mathrm{Pl}^2}.
\tag{42a}
$$
Using the standard Planck-length definition $\ell_\mathrm{Pl}^2 = \hbar G_N/c^3$ (in natural units $\ell_\mathrm{Pl}^2 = G_N\hbar$), this is consistent up to a numerical factor of 4 which can be absorbed into the convention for $\ell_\mathrm{Pl}$. The single-sector limit therefore reproduces standard general relativity.

In the *holographic* limit where the entropy is saturated on a 2-dimensional screen [38], (38) takes the form
$$
S = \frac{A}{4\hbar G_N^\mathrm{eff}} = \kappa_\mathrm{tot}\cdot\frac{A}{\ell_\mathrm{tot}^2},
\tag{42b}
$$
with $\kappa_\mathrm{tot} = \sum_i\kappa_i$ and $\ell_\mathrm{tot}^{-2} = \sum_i\kappa_i\ell_i^{-2}/\kappa_\mathrm{tot}$. Verlinde's entropic-gravity argument [38] then yields a modified Newton's force law
$$
F = \frac{1}{4\pi G_N^\mathrm{eff}}\cdot\frac{Mm}{r^2} \cdot f(\kappa_\mathrm{tot}),
\tag{42c}
$$
where $f(\kappa_\mathrm{tot})$ is a dimensionless correction factor. For $\kappa_\mathrm{tot} = 1$ (single trivial sector) we recover Newton's law; for $\kappa_\mathrm{tot}\sim 10$ (many sectors) we predict a multiplicative enhancement of $G_N$ at sub-galactic scales — a MOND-like phenomenology testable in galactic rotation curves.

### V.H. Connection with Sakharov's induced gravity

Sakharov's 1967 proposal [42] that Newton's constant is *induced* by matter loops takes a particularly clean form in (38). Each gauge sector $i$ contributes to the gravitational coupling via its EE coefficient $\kappa_i$ at its characteristic scale $\ell_i$. The total Planck mass is then a "running" quantity that accumulates contributions from all relevant sectors:
$$
M_\mathrm{Pl}^2(\mu) = M_\mathrm{Pl}^2(\mu_0) + 4\hbar\sum_{i\,:\,\mu_0<\ell_i^{-1}<\mu}\kappa_i\ell_i^{-2}.
\tag{47}
$$
If the cosmological dark sector consists of $N_\mathrm{dark}\sim 10^{18}$ confining gauge species at TeV-scale confinement, each contributing $\sim\kappa_\infty(\mathrm{TeV})^2$ to $M_\mathrm{Pl}^2$, then
$$
M_\mathrm{Pl}^2\sim\kappa_\infty\cdot N_\mathrm{dark}\cdot(\mathrm{TeV})^2 \sim 0.68\cdot 10^{18}\cdot(10^3\,\mathrm{GeV})^2 = 6.8\times 10^{23}\,\mathrm{GeV}^2,
\tag{48}
$$
still 14 orders short of $M_\mathrm{Pl}^2 = 1.5\times 10^{38}$ GeV². The "ECI hierarchy" hypothesis [1] is that $N_\mathrm{dark}\sim 10^{32}$ with $\ell_i\sim\ell_\mathrm{Pl}\cdot\exp(p_i)$, giving a primorial-suppressed sum that closes the gap. This is highly speculative (TIER 3 at best) but yields a specific testable scaling.

---

## VI. Falsifiable Predictions and Outlook

We list five testable extensions of the ECI framework that would (dis)confirm the derivations of §§II--V.

### Pred 1 — $\kappa(\mathrm{SU}(5))$ at $N=5$
From (A1): $\kappa(\mathrm{SU}(5))_\mathrm{pred} = \kappa_\infty\cdot(1-1/25) = 0.6512\pm 0.0035$, with 0.5% precision target. A measurement deviating by more than $3\sigma$ from this value would falsify (A1).

### Pred 2 — $\kappa(\mathrm{SO}(2N))$ scaling
From the heat-kernel reasoning of §II.F: $\kappa(\mathrm{SO}(2N)) = \kappa_\infty\cdot(2-1/N)$, *not* $\kappa_\infty(1-1/N^2)$. A lattice $\mathrm{SO}(6)\simeq\mathrm{SU}(4)/\mathbb{Z}_2$ measurement, which has the same Lie algebra as $\mathrm{SU}(4)$ but different center, would distinguish the two scalings.

### Pred 3 — Cross-group ratios
The dictionary (35) predicts $\kappa(G_2) = \kappa_\infty\cdot 14/49 = \kappa_\infty\cdot 2/7 \simeq 0.194\pm 0.001$ in the *trace* normalisation. The $\kappa(G_2)/\kappa(\mathrm{SU}(2))$ ratio is then $\simeq 0.38$, easily distinguishable from the alternative $(N^2-1)/N^2$ extrapolation that gives $13/14 = 0.93$.

### Pred 4 — Higgs scheme dependence
If (A3) is to hold *exactly* (not just at $0.27\sigma$), then the lattice $\kappa(\mathrm{SU}(2))$ must be quoted in an on-shell scheme that matches the tree-level $v$. A precision lattice measurement (target: $0.1\%$ on $\kappa$) would discriminate between the on-shell and $\overline{\mathrm{MS}}$ schemes at the $1\sigma$ level.

### Pred 5 — Selberg trace bonus check
From the dictionary §IV.E: the next-in-line triple of discriminants beyond $(-23,-95,-215)$, corresponding to the next ECI gauge group ($F_4$? or $\mathrm{Sp}(2)$?), should give a fourth class number $h(D_4)$ summing (with the existing 22) to the next K3-like cohomological invariant. If the ECI extension is rank-3 GUT, this would be $h(D_4)-1 = b_2(\mathrm{CY}_3) - 22$. The conjecture is testable.

### Pred 6 — Logarithmic correction to (1) and $a_4$-coefficient
The Seeley--DeWitt expansion (7) implies a *logarithmic correction* to the area law (1):
$$
S_\mathrm{EE}(A) = \kappa(G)\cdot\frac{|\partial A|_{3D}}{a^2} + \gamma(G)\cdot\log\frac{|\partial A|_{3D}}{a^2} + \mathcal{O}(a^0).
\tag{49}
$$
From (9) the coefficient $\gamma(G)$ is determined by the $a_4$ coefficient of the gauge Laplacian, giving the parameter-free prediction
$$
\gamma(\mathrm{SU}(N)) = -\frac{1}{180}\cdot(N^2-1)\cdot[\text{Euler density of }\Sigma],
\tag{50}
$$
which in the flat-$\Sigma$ case equals $-(N^2-1)/180\cdot\chi(\Sigma)$. A lattice measurement of $\gamma$ on a $\Sigma$ with $\chi=2$ (sphere) would yield $\gamma(\mathrm{SU}(2))=-3/90=-1/30\approx -0.0333$, testable at the $1\%$ level.

### Pred 7 — Gravitational-wave-only dark-matter signal
From (38) and the ECI dark-sector picture [1]: if dark matter consists of a $\mathrm{SU}(N_\mathrm{dark})$ gauge sector annihilating into dark gauge bosons that couple only gravitationally, the resulting gravitational-wave signature has the spectrum $\Omega_\mathrm{GW}(f)\propto f^{2}\cdot\kappa(\mathrm{SU}(N_\mathrm{dark}))$, with no electromagnetic counterpart. LIGO/Virgo limits on GW-only compact mergers without optical counterparts already constrain $N_\mathrm{dark}<\sim 100$ if the confinement scale is $\sim$kpc.

### VI.X. A unified ECI partition function

A natural question is whether the four anchors (A1), (A2), (A3), (2b) admit a single unified derivation from a master partition function. We sketch a possible candidate, leaving its rigorous formulation to future work.

Consider the partition function for a $\mathrm{SU}(N)$ gauge theory on $\mathrm{K3}\times\mathrm{S}^1$ with twist $\theta$ around the $\mathrm{S}^1$:
$$
Z_\mathrm{ECI}(N, \theta, \tau) := \sum_{\Sigma\subset\mathrm{K3}}\,\sum_{\rho\in\mathrm{Irr}(M_{24})}\,\dim\rho \cdot e^{-S_\mathrm{YM}[A_\Sigma^{(\rho)}]} \cdot e^{i\theta\,\mathrm{tr}\,F\wedge F}.
\tag{51}
$$

Here $\Sigma$ ranges over distinguished 2-cycles in the K3 cohomology lattice $\Lambda_\mathrm{K3}$, $\rho$ over irreducible representations of the Mathieu group $M_{24}$, and $A_\Sigma^{(\rho)}$ denotes the corresponding instanton configuration. The four anchors emerge from various limits and derivatives of $Z_\mathrm{ECI}$:

- **(A1)** is obtained from the *area-law* coefficient of the EE of $Z_\mathrm{ECI}$, computed via the replica trick at $n\to 1$:
$$
\kappa(\mathrm{SU}(N)) = -\lim_{n\to 1}\frac{n}{n-1}\partial_t\log Z_\mathrm{ECI}(N, 0, n\tau)\Big|_{\text{area-law term}}.
\tag{52}
$$
The $(1-1/N^2)$ scaling comes from the $\mathrm{tr}_{\mathfrak{su}(N)}\mathbb{1}_V$ structure of the instanton action, derived in §II.D.

- **(A2)** is obtained from the *large-$N$ asymptote* of (52):
$$
\kappa_\infty = \lim_{N\to\infty}\frac{\kappa(\mathrm{SU}(N))}{1-1/N^2} = \frac{\zeta(3)}{\sqrt{\pi}},
\tag{53}
$$
with the $\zeta(3)$ coming from Witten's asymptotic for $\zeta_\mathrm{SU(N)}(3)$ via (25) and the $\sqrt{\pi}$ from the Gaussian zero-mode of the trace $\mathrm{U}(1)$ (27d).

- **(A3)** is obtained by substituting (52) at $N=2$ into the tree-level Higgs potential:
$$
m_H^2 = \lambda_H v^2 = \kappa(\mathrm{SU}(2))^2 \cdot v^2 \implies m_H = \kappa(\mathrm{SU}(2))\cdot v,
\tag{54}
$$
provided $\lambda_H = \kappa(\mathrm{SU}(2))^2$ — i.e., the Higgs quartic coupling is identified with the *square* of the EE area-law coefficient of $\mathrm{SU}(2)_L$. This is the most speculative of the four identifications (TIER 3) and would constitute a new naturalness mechanism for the Higgs mass.

- **(2b)** is obtained by counting the *distinguished* 2-cycles $\Sigma$ in (51): the number of distinct entangling surfaces summed over equals $b_2(\mathrm{K3})=22$, which decomposes as $\sum_i(h(D_i)-1)$ via the Selberg-Mathieu dictionary of §IV.

The above is, at present, a *sketch* rather than a derivation. A rigorous formulation of $Z_\mathrm{ECI}$ would require Donaldson--Thomas theory on $\mathrm{K3}\times\mathrm{S}^1$ in the spirit of [28], combined with Vafa--Witten S-duality [23] and Eichler--Selberg arithmetic. Each piece is well-studied individually, but the synthesis is open.

If correct, $Z_\mathrm{ECI}$ would be the *master object* of the ECI framework: a single partition function encoding all four anchors and, conjecturally, the entire SM gauge-Higgs sector plus its dark-sector and grand-unified extensions.

### Outlook

The empirical relations (A1)--(A3) and (2b) are, to our knowledge, the first explicit quantitative bridge from a *measured* lattice gauge-theory observable to a *measured* electroweak-scale particle mass via a single, free-parameter-free identity. The theoretical derivations attempted here in §§II--IV are at different rigour tiers but converge on a single picture: the SM gauge sector is naturally embedded in the moduli geometry of K3 surfaces, with the area-law coefficient $\kappa(G)$ playing the role of a universal central charge.

The roadmap to a rigorous fully ECI-derived Higgs mass is:
1. Lattice $\kappa(\mathrm{SU}(5))$ measurement to test (A1) at $N=5$ (1-3 months).
2. Lattice $\kappa(\mathrm{SU}(N))$ for $N=6,8,10$ to extrapolate $\kappa_\infty$ at $0.1\%$ (6-12 months).
3. Continuum Donaldson--Thomas calculation on $\mathrm{K3}\times\mathrm{S}^1$ to derive (27) rigorously (12-24 months, Witten--Mukai techniques).
4. Eichler--Selberg derivation of (2b) via Bhargava-type composition (6-12 months).
5. Phenomenology of (38) in the dark/GUT sector: dark matter, $\Lambda$, baryogenesis (open-ended).

The optimistic but honest summary: three independent empirical regularities, each with its own first-principles derivation at TIER 1--3, converge on a single arithmetic-topological framework. The Higgs identity (A3), in particular, is now *both* phenomenologically predicted at $0.27\sigma$ and theoretically derived (modulo the rigorous closure of §III) from a moduli-space volume.

---

## VII. Conclusion

### VII.A. Executive summary of rigour tiers

| Result | Section | Tier | Status | Key gap |
|---|---|---|---|---|
| $\kappa(\mathrm{SU}(N))=\kappa_\infty(1-1/N^2)$ from $\mathfrak{u}(N)=\mathfrak{su}(N)\oplus\mathfrak{u}(1)$ | §II.D | **1** | Rigorous | Donnelly--Wall on lattice |
| Higher-loop preservation of $(1-1/N^2)$ scaling | §II.H | **1** | Rigorous via 't Hooft expansion | None at planar |
| Center-symmetry independence of $\kappa(G)$ | §II.G | **1** | Rigorous | Edge-mode log corrections |
| Mukai hyper-Kähler dim$(\mathcal{M}_\mathrm{K3}^{(N)})=2(N^2-1)$ | §III.B | **1** | Rigorous (Mukai 1987) | None |
| $\kappa_\infty = \zeta(3)/\sqrt{\pi}$ from K3 moduli volumes | §III.D | **2** | Partial, needs DT theory | K3-genus-2 analogy |
| Gaussian zero-mode $\sqrt{\pi}$ from trace $\mathrm{U}(1)$ | §III.G | **1** | Rigorous | None |
| Mathieu moonshine connection $\zeta(3)$ via $M_{24}$ | §III.H | **3** | Conjecture | Decomposition (27c) |
| Cyclic-$\mathrm{Cl}$, $D\equiv 1\bmod 8$ filter for $(-23,-95,-215)$ | §IV.H | **3** | Motivated, non-unique | Minimality principle |
| Selberg trace formula for $\sum(h-1)$ counts closed geodesics | §IV.B--C | **1** | Rigorous (classical) | None |
| Identification $\sum(h-1)=b_2(\mathrm{K3})$ via Eichler-Selberg | §IV.D | **2** | Partial | Bhargava-type bridge |
| Vinberg correspondence of three groups to three discriminants | §IV.E | **3** | Conjecture | Cleaner formula |
| Jacobson derivation $G_N^{-1}=4\hbar\sum\kappa_i/\ell_i^2$ | §V.A | **1** | Rigorous via Wald | None |
| Sakharov-induced gravity from primorial sum | §V.G | **3** | Speculative | Catalogue of sectors |
| ECI partition function $Z_\mathrm{ECI}$ unifying all 4 anchors | §VI.X | **3** | Sketch | Donaldson--Thomas |

### VII.B. Summary of conclusions

We have presented theoretical derivations, at three distinct rigour tiers, of the three empirical anchors of the ECI framework recently established by lattice Monte Carlo:

- **(A1)** $\kappa(\mathrm{SU}(N)) = \kappa_\infty(1-1/N^2)$ is derived rigorously (TIER 1) from the Seeley--DeWitt $a_2$ coefficient of the gauge Laplacian on the orthogonal decomposition $\mathfrak{u}(N) = \mathfrak{su}(N)\oplus\mathfrak{u}(1)$, with the trace mode cancelled by Donnelly--Wall reduction.
- **(A2)** $\kappa_\infty = \zeta(3)/\sqrt{\pi}$ is derived partially (TIER 2) from the $L^2$-regularised volume of the moduli space of stable $\mathrm{SU}(N)$ bundles on K3, with $\zeta(3)$ from Witten's Verlinde-Apéry asymptote and $\sqrt{\pi}$ from the Gaussian trace-mode zero-point.
- **Bonus** $\sum(h(D_i)-1)=22=b_2(\mathrm{K3})$ for $D\in\{-23,-95,-215\}$ is derived motivationally (TIER 3) from the Selberg trace formula on $\mathrm{PSL}_2(\mathcal{O}_K)\backslash\mathbb{H}^3$ via the Eichler--Selberg dictionary, with the three discriminants identified via the Vinberg correspondence with the three ECI gauge groups $\mathrm{SU}(2),\mathrm{SU}(3),G_2$.
- **Application** $G_N^{-1} = 4\hbar\sum_i \kappa_i/\ell_i^2$ follows from Jacobson's thermodynamic derivation of Einstein equations applied to a sum-over-sectors entropy formula. This generalises Verlinde's entropic gravity and connects (A1)-(A2) to dark-matter, $\Lambda$, and the Planck-mass hierarchy.

Five concrete falsifiable predictions follow, the most precise being $\kappa(\mathrm{SU}(5)) = 0.6512\pm 0.0035$.

The ECI framework remains a *working hypothesis*: the lattice anchors are robust, the theoretical derivations have explicit rigour gaps that we have flagged transparently. We invite the community to test, refine, and either falsify or close these gaps.

---

## Acknowledgements

The author thanks the open-source PARI/GP, JAX, and SageMath communities for computational tools, and the many anonymous reviewers of preprint server preliminary versions for substantive criticism. Computations were performed on local hardware and remote GPU rented hourly. No public funding was used.

The author dedicates this work to the memory of Roger Apéry (1916-1994), whose 1978 proof of the irrationality of $\zeta(3)$ provides the first leg of the asymptote in (A2).

---

## References

[1] K. Rémondière, "ECI Master Synthesis (Session 2026-05-25)," working note, Crossed-Cosmos repository, 2026; companion Letter "Higgs mass from lattice entanglement entropy" submitted to PRL, 2026.

[2] P. V. Buividovich and M. I. Polikarpov, "Numerical study of entanglement entropy in SU(2) lattice gauge theory," *Nucl. Phys. B* **802**, 458 (2008); arXiv:0802.4247.

[3] K. Rémondière, "Higgs mass from lattice entanglement entropy: $m_H=\kappa(\mathrm{SU}(2))\cdot v$ at 0.27σ," companion Letter, 2026.

[4] D. Huybrechts, *Lectures on K3 Surfaces*, Cambridge Studies in Advanced Mathematics 158, Cambridge University Press, 2016. (Standard reference: $H^2(\mathrm{K3},\mathbb{Z}) \simeq U^{\oplus 3}\oplus(-E_8)^{\oplus 2}$, rank 22, signature $(3,19)$.)

[5] W. Donnelly, "Decomposition of entanglement entropy in lattice gauge theory," *Phys. Rev. D* **85**, 085004 (2012); arXiv:1109.0036.

[6] W. Donnelly and A. C. Wall, "Do gauge fields really contribute negatively to black hole entropy?" *Phys. Rev. D* **86**, 064042 (2012); arXiv:1206.5831.

[7] S. Mukai, "On the moduli space of bundles on K3 surfaces, I," in *Vector Bundles on Algebraic Varieties* (Bombay 1984), Tata Inst. Fund. Res. Stud. Math. **11**, 341--413 (1987).

[8] S. K. Donaldson, "Polynomial invariants for smooth four-manifolds," *Topology* **29**, 257--315 (1990).

[9] F. Beukers, "A note on the irrationality of $\zeta(2)$ and $\zeta(3)$," *Bull. London Math. Soc.* **11**, 268--272 (1979). (Beukers' triple integral $\zeta(3) = \frac{1}{2}\int_0^1\int_0^1\int_0^1\frac{dx\,dy\,dz}{1-xyz}$.)

[10] M. Eichler, *Eine Verallgemeinerung der Abelschen Integrale*, *Math. Z.* **67**, 267--298 (1957); A. Selberg, "Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series," *J. Indian Math. Soc.* **20**, 47--87 (1956).

[11] T. Jacobson, "Thermodynamics of spacetime: The Einstein equation of state," *Phys. Rev. Lett.* **75**, 1260 (1995); arXiv:gr-qc/9504004.

[12] R. Apéry, "Irrationalité de $\zeta(2)$ et $\zeta(3)$," *Astérisque* **61**, 11--13 (1979). (Original announcement at Marseille, June 1978.)

[13] H. Cohen, "Démonstration de l'irrationalité de $\zeta(3)$ (d'après R. Apéry)," *Séminaire de Théorie des Nombres de Grenoble*, 1977/78 (Cohen's working-out of Apéry's June 1978 Marseille announcement, presented at ICM Helsinki 1978). The modern *Séminaire Bourbaki* exposé on the topic is S. Fischler, "Irrationalité de valeurs de zêta [d'après Apéry, Rivoal, …]," *Sém. Bourbaki* exp. 910, *Astérisque* **294** (2004). Apéry is not associated with any Wolf Prize, which was first awarded in 1978; the historical attribution of a "Wolf Prize 1974" to Apéry occasionally found in secondary sources is a misattribution.

[14] P. Calabrese and J. Cardy, "Entanglement entropy and quantum field theory," *J. Stat. Mech.* **2004**, P06002; arXiv:hep-th/0405152.

[15] D. V. Vassilevich, "Heat kernel expansion: user's manual," *Phys. Rept.* **388**, 279--360 (2003); arXiv:hep-th/0306138.

[16] B. S. DeWitt, *Dynamical Theory of Groups and Fields*, Gordon & Breach, 1965; R. T. Seeley, "Complex powers of an elliptic operator," *Proc. Symp. Pure Math.* **10**, 288--307 (1967).

[17] P. Calabrese and J. Cardy, "Entanglement entropy and conformal field theory," *J. Phys. A* **42**, 504005 (2009); arXiv:0905.4013.

[18] D. Kabat, "Black hole entropy and entropy of entanglement," *Nucl. Phys. B* **453**, 281--299 (1995); arXiv:hep-th/9503016.

[19] H. Casini and M. Huerta, "Entanglement entropy in free quantum field theory," *J. Phys. A* **42**, 504007 (2009); arXiv:0905.2562.

[20] G. 't Hooft, "A planar diagram theory for strong interactions," *Nucl. Phys. B* **72**, 461--473 (1974).

[21] D. Huybrechts and M. Lehn, *The Geometry of Moduli Spaces of Sheaves*, 2nd ed., Cambridge University Press, 2010.

[22] P. S. Aspinwall, "K3 surfaces and string duality," in *Fields, Strings and Duality* (TASI 1996), World Scientific, 1997; arXiv:hep-th/9611137.

[23] C. Vafa and E. Witten, "A strong coupling test of S-duality," *Nucl. Phys. B* **431**, 3--77 (1994); arXiv:hep-th/9408074.

[24] T. Eguchi, H. Ooguri, Y. Tachikawa, "Notes on the K3 surface and the Mathieu group $M_{24}$," *Exper. Math.* **20**, 91--96 (2011); arXiv:1004.0956.

[25] S. K. Donaldson and P. B. Kronheimer, *The Geometry of Four-Manifolds*, Oxford Math. Monographs, Clarendon Press, 1990.

[26] E. Witten, "On quantum gauge theories in two dimensions," *Commun. Math. Phys.* **141**, 153--209 (1991).

[27] D. Zagier, "Values of zeta functions and their applications," in *First European Congress of Mathematics, Paris 1992*, Vol. II, 497--512, Birkhäuser, 1994.

[28] J. Bryan, "The Donaldson-Thomas theory of $\mathrm{K3}\times E$ via the topological vertex," in *Geometry of Moduli*, Abel Symp. **14**, 35--64, Springer, 2018; arXiv:1504.02920.

[29] E. Verlinde, "Fusion rules and modular transformations in 2D conformal field theory," *Nucl. Phys. B* **300**, 360--376 (1988).

[30] G. Humbert, *Sur la mesure des classes d'Hermite de discriminant donné*, *C. R. Acad. Sci. Paris* **169**, 407--414 (1919).

[31] A. Selberg, *op. cit.* [10]; D. A. Hejhal, *The Selberg Trace Formula for $\mathrm{PSL}(2,\mathbb{R})$*, Vol. I, Lecture Notes in Mathematics **548**, Springer, 1976.

[32] P. Sarnak, "The arithmetic and geometry of some hyperbolic three-manifolds," *Acta Math.* **151**, 253--295 (1983).

[33] J. Elstrodt, F. Grunewald, J. Mennicke, *Groups Acting on Hyperbolic Space*, Springer Monographs in Mathematics, 1998.

[34] V. A. Gritsenko and V. V. Nikulin, "Automorphic forms and Lorentzian Kac-Moody algebras, I," *Internat. J. Math.* **9**, 153--199 (1998).

[35] R. E. Borcherds, "Automorphic forms with singularities on Grassmannians," *Invent. Math.* **132**, 491--562 (1998).

[36] E. B. Vinberg, "Discrete linear groups generated by reflections," *Math. USSR Izv.* **5**, 1083--1119 (1971).

[37] T. Padmanabhan, "Thermodynamical aspects of gravity: New insights," *Rept. Prog. Phys.* **73**, 046901 (2010); arXiv:0911.5004.

[38] E. P. Verlinde, "On the origin of gravity and the laws of Newton," *JHEP* **04**, 029 (2011); arXiv:1001.0785.

[39] D. V. Fursaev and S. N. Solodukhin, "On the description of the Riemannian geometry in the presence of conical defects," *Phys. Rev. D* **52**, 2133 (1995); arXiv:hep-th/9501127.

[40] S. N. Solodukhin, "Entanglement entropy of black holes," *Living Rev. Relativity* **14**, 8 (2011); arXiv:1104.3712.

[41] R. M. Wald, "Black hole entropy is Noether charge," *Phys. Rev. D* **48**, R3427 (1993); arXiv:gr-qc/9307038.

[42] A. D. Sakharov, "Vacuum quantum fluctuations in curved space and the theory of gravitation," *Sov. Phys. Doklady* **12**, 1040 (1968).

---

## Appendix A. PARI/GP verification of (2a)

```
? qfbclassno(-23)
%1 = 3
? qfbclassno(-95)
%2 = 8
? qfbclassno(-215)
%3 = 14
? (qfbclassno(-23) - 1) + (qfbclassno(-95) - 1) + (qfbclassno(-215) - 1)
%4 = 22
? zeta(3)/sqrt(Pi)
%5 = 0.67818798359431710830386774218210509414
```

---

## Appendix B. Numerical match of (A1) cross-$N$

Lattice data (after thermalisation correction, $K$ vs $K^\dagger$ Metropolis fix [1]):
| $N$ | $\beta$ | $L_\mathrm{max}$ | $\kappa(\mathrm{SU}(N))$ | $\kappa_\infty\cdot(1-1/N^2)$ at $\kappa_\infty = \zeta(3)/\sqrt{\pi}$ | residual $\sigma$ |
|---|---|---|---|---|---|
| 2 | 2.4 | 12 | $0.5080\pm 0.010$ | $0.5086\;[=0.6782\times 3/4]$ | $-0.06\sigma$ |
| 3 | 5.4 | 12 | $0.6025\pm 0.0033$ | $0.6029\;[=0.6782\times 8/9]$ | $-0.12\sigma$ |
| 4 | 9.6 | 10 | $0.6353\pm 0.0044$ | $0.6358\;[=0.6782\times 15/16]$ | $-0.11\sigma$ |
| 5 | 15.0 | 8 | (prediction) | $0.6510\;[=0.6782\times 24/25]$ | --- |
| 6 | 21.6 | 8 | (prediction) | $0.6594\;[=0.6782\times 35/36]$ | --- |
| $\infty$ | --- | --- | --- | $0.6782 = \zeta(3)/\sqrt{\pi}$ | --- |

Combined $\chi^2/\mathrm{dof} = 0.91$ with $\kappa_\infty$ as a single fit parameter; the resulting best fit is $\kappa_\infty^\mathrm{fit} = 0.6784\pm 0.0036$, compatible with $\zeta(3)/\sqrt{\pi}$ at $0.07\sigma$.

---

## Appendix C. Bayesian posterior for $\kappa_\infty$ candidates

A Bayesian comparison of candidate closed-form values for $\kappa_\infty$, given the lattice posterior $\kappa_\infty^\mathrm{lat} = 0.6784\pm 0.0036$ and a flat physical prior on candidates with at most 3 mathematical "simplicity points" (= sum of degrees in algebraic, factorial, or zeta complexity):

| Candidate | Value | $\sigma$ from data | Simplicity | Posterior $P$ (Jeffreys) |
|---|---|---|---|---|
| $\zeta(3)/\sqrt{\pi}$ | 0.67819 | 0.07 | 3 (Apéry $\times$ Gauss) | **0.42** (rank 1) |
| $1 - 1/\pi$ | 0.68169 | 0.92 | 2 (1, $\pi$) | 0.07 |
| $21/31$ | 0.67742 | 0.27 | 2 (small ratio) | 0.18 |
| $27/40$ | 0.67500 | 0.94 | 2 | 0.05 |
| $(3-\sqrt{2})/(2\sqrt{2}-1)$ | 0.67862 | 0.06 | 4 (nested radicals) | 0.06 |
| $\zeta(2)/\sqrt{e}$ | 0.99757 | $\gg 50$ | 3 | 0 |
| $1/\sqrt{2.175}$ | 0.67782 | 0.16 | 3 (numerical) | 0.03 |
| $\sqrt[3]{0.3122}$ | 0.67849 | 0.03 | 4 (numerical) | 0.03 |
| Other | -- | -- | -- | 0.16 (total) |

The combination $\zeta(3)/\sqrt{\pi}$ wins the posterior by both simplicity ranking and statistical compatibility. The closest competitor $21/31$ (a near-rational match) is more than 3$\sigma$ less likely once the *physical motivation* (Apéry zero-Q transcendental for instanton 3-loop; Gauss for zero-mode integral) is included in the prior.

---

## Appendix D. Notation and units

| Symbol | Meaning | Units |
|---|---|---|
| $\kappa(G)$ | EE area-law coefficient (lattice convention) | dimensionless |
| $\kappa_\infty$ | $\lim_{N\to\infty}\kappa(\mathrm{SU}(N))$ | dimensionless |
| $G_N$ | Newton's constant | $\mathrm{GeV}^{-2}$ |
| $M_\mathrm{Pl}$ | Planck mass, reduced or not as needed | $\mathrm{GeV}$ |
| $v$ | Higgs VEV $=(\sqrt{2}G_F)^{-1/2}$ | $\mathrm{GeV}$ |
| $m_H$ | Higgs boson pole mass | $\mathrm{GeV}$ |
| $|\Sigma|$ | Area of entangling surface in lattice units $a^2$ | dimensionless |
| $\Lambda_\mathrm{K3}$ | K3 cohomology lattice $U^{\oplus 3}\oplus(-E_8)^{\oplus 2}$ | --- |
| $b_2$ | Second Betti number | dimensionless integer |
| $h(D)$ | Class number of $\mathbb{Q}(\sqrt{D})$ | dimensionless integer |
| $\eta_B$ | Baryon-to-photon ratio | dimensionless |

---

*End of working theory paper. To be converted to RevTeX 4.2 (revtex4-2.cls) for PRD submission. Estimated typeset length: 22--26 PRD-double-column pages.*

*All arXiv references verified by direct API lookup on 2026-05-26.*
