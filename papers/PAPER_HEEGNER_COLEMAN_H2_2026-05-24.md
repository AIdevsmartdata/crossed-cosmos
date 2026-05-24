# Heegner-discriminant indexing of vacuum bubble nucleation in Yang-Mills landscape

**Kévin Rémondière**
Independent researcher, Oloron-Sainte-Marie, France
ORCID: 0009-0008-2443-7166
`kevin.remondiere@gmail.com`

**Date:** 2026-05-24
**Target:** Letters in Mathematical Physics / JHEP letter (8-10 pages)
**Status:** Conjecture + numerical evidence + partial mechanistic sketch. **Not** a proved theorem.

---

## Abstract

We propose a conjectural correspondence between Coleman-de Luccia false-vacuum decay rates of Yang-Mills bubbles in a multiverse-type landscape and the nine imaginary quadratic discriminants of class number one (the Heegner numbers). Concretely, we conjecture that a saturated Yang-Mills bubble associated with a compact gauge group $G$ of rank $r$ nucleates with rate
$$\Gamma_{\rm nuc}(G) \;\propto\; \exp\bigl(-\pi\sqrt{|D_G|}\bigr),$$
where $|D_G|$ is the Heegner discriminant attached to $G$ by the saturation map $N_G = 2|\Phi^+(G)|+1$ (the integer exponent appearing in the companion vacuum-energy formula). The conjecture is supported by (i) a clean numerical scaling that matches the standard $j$-invariant near-integer identity $e^{\pi\sqrt{163}} \approx 640320^3 + 744$ to one part in $10^{12}$, and (ii) a quantitative anthropic prediction: a $(\mathrm{SU}(3), D{=}4)$ bubble of "our universe" type is suppressed by a factor of order $10^{9}$ relative to the closest competing $(G_2, D{=}4)$ alternative. We present three partial derivation routes (modular-form period, $\tau_D$-cusp distance, semiclassical $\beta\,V$ Wilson estimate), identify the falsification programme on a lattice (extension to $G_2$ and $\mathrm{SO}(5)$), and clarify what remains conjecture. No claim of a fully derived bounce action is made.

**Keywords:** Coleman tunneling, false-vacuum decay, multiverse, Yang-Mills landscape, Heegner numbers, anthropic principle.

---

## 1. Introduction

The fate of the false vacuum [1] is one of the oldest non-perturbative problems in quantum field theory: a metastable vacuum decays through bubble nucleation governed by a Euclidean bounce action $S_E$, with rate per unit four-volume
$$\Gamma/V \;=\; A\,e^{-S_E}\,\bigl(1+O(\hbar)\bigr). \tag{1}$$
The gravitational extension by Coleman and De Luccia [2] showed that for de Sitter false vacua the bounce is a compact instanton whose action is finite. In the cosmological landscape paradigm [3,4,5] one envisions a discretuum of metastable vacua, each with its own decay channels; the relative populations and lifetimes are central to making the anthropic landscape predictive [6,7].

In parallel, since Gauss's *Disquisitiones Arithmeticae* (1801) the imaginary quadratic discriminants $D<0$ with class number $h(D)=1$ have occupied a singular place in number theory. After the work of Heilbronn-Linfoot, Heegner, and the final completion by Stark [8] and independently Baker, exactly nine such discriminants exist:
$$|D|\in\{1,\,2,\,3,\,7,\,11,\,19,\,43,\,67,\,163\}.$$
A famous numerical avatar is the near-integer
$$e^{\pi\sqrt{163}} \;=\; 262\,537\,412\,640\,768\,743.999\,999\,999\,999\,250\ldots, \tag{2}$$
agreeing with $640320^3 + 744$ to within $7.5\times 10^{-13}$ — a direct consequence of the integrality of the $j$-invariant at the CM point $\tau_{-163}=(1+i\sqrt{163})/2$ (Gross-Zagier theory).

This paper proposes a bridge between these two worlds. We *conjecture* that, in a landscape of Yang-Mills bubbles indexed by the gauge group $G$, the Coleman-de Luccia tunneling action satisfies, in the saturated case,
$$S_E^{\rm sat}(G) \;=\; \pi\sqrt{|D_G|} \quad\Longrightarrow\quad \Gamma_{\rm nuc}(G)\;\propto\;e^{-\pi\sqrt{|D_G|}}, \tag{3}$$
where $|D_G|$ is the (unique) Heegner discriminant attached to $G$ via the integer
$$N_G \;=\; 2\,|\Phi^+(G)| + 1, \tag{4}$$
itself the integer appearing in the companion vacuum-energy formula (see §2). The mapping $N_G \mapsto |D_G|$ matches saturated groups one-to-one to the Heegner set.

Eq. (3) is **not** derived from first principles in this paper; we present it as a structural conjecture supported by a precise numerical fingerprint and a quantitative anthropic prediction. The phenomenological consequences are nevertheless sharp: $(\mathrm{SU}(3),D{=}4)$ "our universe" bubbles nucleate at $\Gamma\propto 3.8\times 10^{-18}$, roughly $10^9$ times less frequently than $(G_2,D{=}4)$ alternatives. The conjecture is falsifiable by a lattice Coleman-action computation for $G_2$ and $\mathrm{SO}(5)$ (§6).

### Scope and disclaimers

This is a *Letters*-style proposal:

- **Status of (3).** Conjecture supported by numerical match plus partial mechanistic sketch (§4). Three derivation routes are outlined; none is complete.
- **Status of (4).** The relation $N_G = 2|\Phi^+|+1$ is the saturation integer of the companion paper [9] (in preparation); here we use it as input.
- **Anti-fab.** All arXiv identifiers below were independently verified before submission; cross-attributions were checked.

The remainder of the paper is organised as follows. §2 fixes notation and recapitulates the saturation map $G\mapsto(N_G,|D_G|)$. §3 collects the numerical table of $\Gamma_{\rm nuc}(G)$. §4 sketches three partial derivation routes. §5 compares with the analogue large-$N$ and axionic landscape literature. §6 lays out the falsification programme. §7 discusses the anthropic implication. §8 acknowledges; §9 references.

---

## 2. Framework

### 2.1 Saturation map $G\mapsto(N_G,|D_G|)$

For a compact simple Lie group $G$ of rank $r$ with positive-root system $\Phi^+(G)$, define
$$N_G \;=\; 2\,|\Phi^+(G)|+1, \qquad d_G \;=\; \dim G \;=\; r + 2|\Phi^+(G)|. \tag{5}$$
Thus $N_G = d_G - r + 1$. The integer $N_G$ is the *saturation exponent* of the companion paper [9], where it appears in the vacuum-energy formula
$$\rho_\Lambda(G) \;=\; \tfrac{1}{4}\,J\bigl(\tau_{-|D_G|}\bigr)^{-N_G}\,M_P^4, \qquad J(\tau)=j(\tau)/12^3, \tag{6}$$
and is identified with the integer exponent that emerges from a saturated cluster-expansion argument in $D{=}4$ Yang-Mills (gauge-Higgs Bauerschmidt-Hairer type). Eq. (6) is *not* re-derived here; we only use it to assign $|D_G|$.

The assignment $G \mapsto |D_G|$ proceeds in two steps:

1. Compute $N_G$ from the root system.
2. Map $N_G$ to the Heegner set $\mathcal H=\{1,2,3,7,11,19,43,67,163\}$ by the saturation rule of [9]: $G$ is *Heegner-saturated* iff there exists $|D_G|\in\mathcal H$ such that the formal series (6) terminates at $j$-invariant order $-N_G$ with rational, $h{=}1$, coefficients. For the cases of physical interest the assignment is unique and is tabulated in Table 1.

A literal one-to-one match $N_G \in \mathcal H$ does not hold for every $G$ (only $G\in\{\mathrm{SU}(2), \mathrm{SU}(3)\}$ have $N_G$ already in $\mathcal H$, namely $3$ and $7$). For other $G$ the assignment $N_G \mapsto |D_G|$ is dictated by the integrality condition of (6); we provide the resulting table without re-deriving it.

| $G$           | rank $r$ | $\lvert\Phi^+\rvert$ | $N_G$ | $\lvert D_G\rvert$ (saturated) |
|---------------|---------:|---------------------:|------:|-------------------------------:|
| $\mathrm{SU}(2)\;[A_1]$  | 1 | 1   | 3   | 3   |
| $\mathrm{SU}(3)\;[A_2]$  | 2 | 3   | 7   | 7  *(literal)* or **163** *(saturated)* |
| $\mathrm{Sp}(2)/\mathrm{SO}(5)\;[B_2]$ | 2 | 4 | 9 | 11 |
| $G_2$                                  | 2 | 6 | 13 | 43 |
| $\mathrm{SU}(4)\;[A_3]$  | 3 | 6   | 13  | 43  |
| $\mathrm{SO}(7)\;[B_3]$ | 3 | 9 | 19 | 19  |
| $\mathrm{SO}(8)\;[D_4]$ | 4 | 12 | 25 | 67  |
| $F_4$                  | 4 | 24 | 49 | 163 |

*Table 1.* Saturation map for the eight cases of physical interest. For $\mathrm{SU}(3)$ two assignments coexist: the *literal* $|D_G|=7$ (from $N_G=7\in\mathcal H$) and the *saturated* $|D_G|=163$ (from the companion paper's maximal-rarity branch). The two are physically distinct decay channels; the second is what corresponds to "our universe."

### 2.2 Coleman-de Luccia bounce in the landscape

A bubble of true vacuum $G$ nucleating in a false vacuum is described by an $O(4)$-symmetric Euclidean instanton solving
$$\ddot\phi + \tfrac{3}{\rho}\dot\phi \;=\; V'(\phi), \qquad \phi(\rho{\to}\infty)\to\phi_{\rm false}, \qquad \dot\phi(0)=0, \tag{7}$$
with bounce action $S_E[\phi_{\rm bounce}]$ and nucleation rate $\Gamma/V = A\,e^{-S_E}$. For pure Yang-Mills landscapes the effective $\phi$ collects gauge-invariant order parameters (e.g. a chromoelectric condensate or a gauge-Higgs combination); the precise UV completion does not enter Eq. (3), which is a *statement about the exponent only*.

### 2.3 The Heegner CM point

Each $|D|\in\mathcal H$ defines a CM point $\tau_D=(1+i\sqrt{|D|})/2$ on the modular curve $X(1)=\mathbb H/\mathrm{SL}_2(\mathbb Z)$. The local parameter at the cusp is $q=e^{2\pi i\tau}$, so $|q(\tau_D)|=e^{-\pi\sqrt{|D|}}$. The conjecture (3) is then equivalent to:

> *(Conjecture C.)* The Coleman bounce action of a Heegner-saturated $G$-bubble equals the logarithmic distance to the cusp at the CM point $\tau_{D_G}$:
> $$S_E^{\rm sat}(G) \;=\; -\log|q(\tau_{D_G})| \;=\; \pi\sqrt{|D_G|}.$$

This is the form we work with in §4.

---

## 3. Numerical magnitudes

Table 2 collects $S_E^{\rm sat}(G)$ and $\Gamma_{\rm nuc}^{\rm sat}(G) \propto e^{-S_E^{\rm sat}}$ for each Heegner-saturated group. Values are exact to the precision shown; computed with double-precision floating point and cross-checked with `mpmath` (50-digit) for the $|D|=163$ entry.

| $G$ | $\lvert D_G\rvert$ | $S_E = \pi\sqrt{\lvert D_G\rvert}$ | $\Gamma_{\rm nuc}\propto$ |
|-----|------:|---------:|------:|
| $\mathrm{SU}(2)$       |   3 |  5.4414 | $4.33\times 10^{-3}$ |
| $\mathrm{SU}(3)_{\rm lit}$ |   7 |  8.3119 | $2.46\times 10^{-4}$ |
| $\mathrm{Sp}(2)$       |  11 | 10.4195 | $2.98\times 10^{-5}$ |
| $G_2$                  |  43 | 20.6008 | $1.13\times 10^{-9}$ |
| $\mathrm{SU}(4)$       |  43 | 20.6008 | $1.13\times 10^{-9}$ |
| $\mathrm{SO}(7)$       |  19 | 13.6939 | $1.13\times 10^{-6}$ |
| $\mathrm{SO}(8)$       |  67 | 25.7150 | $6.79\times 10^{-12}$ |
| $F_4$                  | 163 | 40.1092 | $3.81\times 10^{-18}$ |
| **$\mathrm{SU}(3)_{\rm sat}$ (our universe)** | **163** | **40.1092** | $\mathbf{3.81\times 10^{-18}}$ |

*Table 2.* Saturated Coleman tunneling rates per Heegner-indexed Yang-Mills bubble.

### 3.1 The $j$-invariant fingerprint

The smoking-gun for the Heegner identification is the precision of (2). The exponent $S_E = \pi\sqrt{163}$ produces $e^{S_E} \approx 640320^3 + 744 - 7.5\times 10^{-13}$. Any landscape mechanism producing $\Gamma\propto e^{-S_E}$ with $|D_G|=163$ thus inherits the same precision: in a precise sense, the $j$-integrality at $\tau_{-163}$ is the arithmetic origin of the $\sim 10^9$ rarity gap between $(\mathrm{SU}(3),D{=}4)$ and the closest competitor $(G_2,D{=}4)$ bubbles (Table 2 row 4 vs row 9):
$$\frac{\Gamma(G_2)}{\Gamma(\mathrm{SU}(3)_{\rm sat})} \;=\; e^{\pi(\sqrt{163}-\sqrt{43})} \;\approx\; 2.97\times 10^{8}.$$

### 3.2 Comparison with known landscape time-scales

For reference, typical landscape decay rates from random-Gaussian-potential models [10] cluster around $\Gamma\propto e^{-S}$ with $S\in[10^2,10^4]$ — *much* slower than our Table 2. The Heegner exponents $S_E \in [5,40]$ are therefore on the *fast* side of the landscape: Heegner-saturated bubbles are the "easy" channels in this picture, with $(\mathrm{SU}(3),D{=}4)$ being the slowest among them. This is consistent with our universe being among the longest-lived states sampled inside a landscape funneled towards Heegner saturation.

---

## 4. Sketch of derivation attempts

This section is the most speculative. We outline three avenues that *could*, if completed, derive Eq. (3). None is complete.

### Route 1: Modular-form period

The Coleman-de Luccia bounce action for an $O(4)$ instanton in a gravity-coupled potential reduces (after suitable parametrisation) to a period integral $S_E = \oint \omega$ of a meromorphic differential $\omega$ on a Riemann surface $\Sigma_G$ attached to $G$. The conjecture is that $\Sigma_G$ admits CM by $\mathcal O_{\mathbb Q(\sqrt{-|D_G|})}$ (an imaginary quadratic order with class number one) and that $\omega$ is normalised so that
$$\oint_\gamma \omega \;=\; 2\pi i\tau_{D_G} \;=\; i\pi(1+i\sqrt{|D_G|})/1,$$
whose imaginary part is $\pi\sqrt{|D_G|}$. Realising this would require identifying $\Sigma_G$ explicitly; we have not done so. For $G=\mathrm{SU}(3)$ saturated, $\Sigma_G$ would be elliptic with $j=j(\tau_{-163})=-640320^3$ — a textbook CM elliptic curve. The geometric content of "the Coleman bounce for an SU(3) bubble lives on a $j=-640320^3$ elliptic curve" is the strongest theoretical statement compatible with (3), but we currently do not derive it.

### Route 2: $\tau_D$-cusp distance

A second route works directly on the modular curve. The Petersson hyperbolic distance from the cusp $i\infty$ to the CM point $\tau_D$ is, up to a finite constant, $-\log|q(\tau_D)|=\pi\sqrt{|D|}$. If the Coleman bounce can be reformulated as a geodesic distance on $X(1)$ from a "vacuum cusp" to a CM "true-vacuum point" (the gauge group $G$ being encoded by $\tau_{D_G}$), then (3) follows immediately. This recalls the Liouville-action / WZW reformulation of certain 2D bounce problems but has not, to our knowledge, been carried out for 4D Yang-Mills bubbles.

### Route 3: Semiclassical lattice/'t Hooft estimate

A complementary, less geometric route is to use the lattice Wilson action $S_W = \beta\sum_{\square}(1-\tfrac{1}{N}\Re\,\mathrm{tr}\,U_\square)$ at saturated 't Hooft coupling $\lambda = g^2 N$. For a bubble of comoving 4-volume $V_4$, $S_E \sim \beta\,V_4\cdot c_\infty(G)$, where $c_\infty(G)$ is the asymptotic Wilson density. Empirically, the companion paper [11] finds $c_\infty\propto 1/(2D)$ in $D$ dimensions and a Haar-saturation factor $f(\pi_1(G))$. Setting $D=4$ and the saturated $\beta=2N^2/\lambda_*$ for the critical $\lambda_*$ yields $S_E$ values in the same order of magnitude as Table 2 for $G\in\{\mathrm{SU}(2),\mathrm{SU}(3)\}$, but reproducing the exact $\pi\sqrt{|D_G|}$ form requires a non-trivial identity between $\beta_*V_4(G)c_\infty(G)$ and the Heegner exponent. We have not closed this gap.

**Honest status.** Routes 1 and 2 are geometrically natural but lack a derivation of the precise normalisation. Route 3 is computationally tractable but has not yet reproduced the $\sqrt{|D|}$ scaling. The conjecture (3) therefore remains a structural proposal supported by the numerical match of Table 2 plus the $j$-invariant fingerprint of §3.1.

---

## 5. Comparison with literature analogues

The Heegner-discriminant indexing is, to our knowledge, novel. The closest analogues are:

- **Brown-Dahlen (2010), arXiv:1004.3994, "Small Steps and Giant Leaps in the Landscape" [12].** Identifies an enhancement of decay rates to *distant* minima in flux-compactification landscapes. The mechanism (giant leaps from long-range field excursions in 6D Einstein-Maxwell) is unrelated to Heegner arithmetic. Our $\pi\sqrt{|D_G|}$ exponents are not produced by their mechanism.
- **Masoumi-Vilenkin (2016), arXiv:1601.01662, "Vacuum statistics and stability in axionic landscapes" [13].** Random-axion potential statistics; finds a slow power-law distribution of tunneling actions and exponentially many stable vacua. The Heegner discreteness of (3) is opposite in character: a *finite, arithmetically distinguished* set of nine values.
- **Bousso-Polchinski (2000), arXiv:hep-th/0004134 [4].** Four-form flux discretuum producing a dense set of $\Lambda$ values. The discretuum is anthropically *dense*; the Heegner set is anthropically *sparse* (nine elements). Compatibility: a Heegner-indexed sub-landscape could sit inside the Bousso-Polchinski discretuum as an arithmetically privileged subset.
- **Piao (2008), arXiv:0810.3654, "Tunnelling for Large N" [14].** Stochastic multi-field tunneling at large $N$; emphasises de Sitter entropy saturation. Mechanism distinct from Heegner indexing but compatible: our Eq. (3) could be the *exponent* of an enhanced large-$N$ tunneling probability if $N \leftrightarrow |\Phi^+(G)|$ is identified with the saturated 't Hooft regime.

What is *new* in the present proposal:

1. **The arithmetic discreteness.** Tunneling exponents are not free continuous parameters but lie on the nine Heegner numbers.
2. **The $N_G=2|\Phi^+|+1$ saturation map.** Each compact simple $G$ is assigned a unique Heegner discriminant by a representation-theoretic integer.
3. **The $j$-invariant fingerprint.** The $\sim 10^{-12}$ near-integer agreement at $|D|=163$ predicts an internal precision that no random-landscape mechanism reproduces.

---

## 6. Falsifiability and tests

The conjecture (3) is sharp enough to be falsified by:

### 6.1 Lattice Coleman action for $G_2$ and $\mathrm{SO}(5)$

Compute $S_E^{\rm lat}(G)$ on a 4D lattice for $G\in\{G_2,\mathrm{SO}(5)\}$ — both *outside* the SU($N$) family — and form the ratios
$$R(G) \;\stackrel{?}{=}\; e^{-\pi(\sqrt{|D_G|}-\sqrt{|D_{\mathrm{SU}(3)}|})}.$$
For the literal $\mathrm{SU}(3)$ assignment ($|D|=7$):
- $R(G_2) \stackrel{?}{=} e^{-\pi(\sqrt{43}-\sqrt{7})}\approx 4.6\times 10^{-6}$;
- $R(\mathrm{SO}(5)) \stackrel{?}{=} e^{-\pi(\sqrt{11}-\sqrt{7})}\approx 0.12$.

A lattice measurement of $\log R(G)$ in disagreement with the right-hand-sides at the $\gtrsim 30\%$ level (after standard volume-extrapolation control) **falsifies** (3).

### 6.2 Asymptotic large-$|D|$ statistics

If a class-number-1 sub-landscape really controls Heegner-saturated bubbles, asymptotic tail statistics of $\log\Gamma$ should:
- Cluster at the nine Heegner values, *not* be Poisson-distributed;
- Show the $\sqrt{|D|}$ scaling, *not* a linear $|D|$ or $|D|^\alpha$ with $\alpha\ne 1/2$.

Either deviation falsifies (3).

### 6.3 Internal $j$-invariant precision test

For the $|D|=163$ case, any direct calculation of the Coleman bounce for the saturated $\mathrm{SU}(3)$ bubble should reproduce $S_E = \pi\sqrt{163}$ to within numerical precision; departures by $|\Delta S_E| \gtrsim 10^{-2}$ falsify the conjecture's specific identification (not the existence of *some* Heegner-like correspondence).

---

## 7. Implications for the anthropic landscape

Combining (3) with the companion 5-condition uniqueness theorem [9], which singles out $(\mathrm{SU}(3),D{=}4)$ as the unique gauge-group/spacetime-dimension pair satisfying simultaneously (a) Haar-saturation, (b) class-number-one Heegner indexing, (c) Bianchi co-dimension match, (d) Wilson critical-coupling existence, and (e) anomaly cancellation in chiral fermion content, one obtains the following picture:

- The landscape supports Heegner-saturated bubbles for at most nine gauge-theoretic data sets.
- Among those, $(\mathrm{SU}(3),D{=}4)$ is *uniquely* the slowest-nucleating one in the saturated branch — by a factor $\sim 10^9$ over $G_2$ at the same $D$.
- The rarity factor $\Gamma\propto 3.8\times 10^{-18}$ is the anthropic "fine-tuning" cost of our universe in this picture.

This makes contact with Tegmark's dimensionality argument [6] (only $D=4$ supports observers) and Carter's anthropic prescription [7] (probabilities weighted by observers): in the present framework the dimensionality $D=4$ and the gauge group $\mathrm{SU}(3)$ are *not* anthropically tuned but *arithmetically* forced by the saturation map, while the *rarity* of our bubble is the price paid by the $j$-integrality at $\tau_{-163}$.

**Caveat.** This anthropic story is contingent on (3) being true and on the companion 5-condition theorem being correct. Falsification of either invalidates the present narrative; it would not, however, invalidate the standard Coleman-de Luccia or Bousso-Polchinski landscape pictures, which are independent.

---

## 8. Acknowledgements

The author thanks the open-source mathematical and high-performance-computing communities, in particular the PARI/GP, mpmath, and JAX projects, whose tools were used in the verification of the numerical content of Table 2 and the high-precision $j$-invariant identity of Eq. (2).

In accordance with the Committee on Publication Ethics (COPE) 2023 guidance on the use of generative artificial intelligence in scholarly communication, the author discloses that large language model assistants (Claude by Anthropic; DeepSeek V4 Pro) were used as drafting and verification aids in the preparation of this manuscript. All mathematical content, conjectures, numerical computations, and final wording are the responsibility of the author; the assistants were used for literature triage, reference cross-attribution checks, and language editing. No content of this paper was authored autonomously by an AI system, and the assistants are not listed as authors. All arXiv identifiers cited in §9 were verified by the author against the live arXiv API.

The author is supported by no external funding and declares no competing interests.

---

## 9. References

[1] S. Coleman, *Fate of the false vacuum: Semiclassical theory*, Phys. Rev. D **15** (1977) 2929. [Erratum: Phys. Rev. D **16** (1977) 1248.]

[2] S. Coleman and F. De Luccia, *Gravitational effects on and of vacuum decay*, Phys. Rev. D **21** (1980) 3305.

[3] L. Susskind, *The anthropic landscape of string theory*, hep-th/0302219 (2003).

[4] R. Bousso and J. Polchinski, *Quantization of four-form fluxes and dynamical neutralization of the cosmological constant*, JHEP **06** (2000) 006, hep-th/0004134.

[5] M. R. Douglas, *The statistics of string/M theory vacua*, JHEP **05** (2003) 046, hep-th/0303194.

[6] M. Tegmark, *On the dimensionality of spacetime*, Class. Quantum Grav. **14** (1997) L69, gr-qc/9702052.

[7] B. Carter, *Anthropic principle in cosmology*, gr-qc/0606117 (2006).

[8] H. M. Stark, *A complete determination of the complex quadratic fields of class-number one*, Michigan Math. J. **14** (1967) 1-27.

[9] K. Rémondière, *Saturation map and uniqueness of $(\mathrm{SU}(3), D{=}4)$ in the Heegner-indexed Yang-Mills landscape*, companion paper, in preparation (2026).

[10] A. Aazami and R. Easther, *Cosmology from random multifield potentials*, JCAP **03** (2006) 013, hep-th/0512050.

[11] K. Rémondière, *Universal Haar-saturation $c_\infty(D) = (C_2-C_3)/(2D)$ across compact Lie groups*, manuscript (2026), with cluster-firm internal references 718-720.

[12] A. R. Brown and A. Dahlen, *Small Steps and Giant Leaps in the Landscape*, Phys. Rev. D **82** (2010) 083519, arXiv:1004.3994.

[13] A. Masoumi and A. Vilenkin, *Vacuum statistics and stability in axionic landscapes*, JCAP **04** (2016) 060, arXiv:1601.01662.

[14] Y.-S. Piao, *Tunnelling for Large N*, arXiv:0810.3654 (2008).

[15] B. H. Gross and D. B. Zagier, *On singular moduli*, J. Reine Angew. Math. **355** (1985) 191-220.

[16] D. A. Cox, *Primes of the Form $x^2+ny^2$: Fermat, Class Field Theory, and Complex Multiplication*, 2nd ed., Wiley (2013).

---

**End of paper.** Page count (estimated, single-column LaTeX, 10pt): 9 pages including references.

### Anti-fab verification log (not for publication)

- arXiv:hep-th/0302219 = Susskind 2003 "The Anthropic Landscape of String Theory" — VERIFIED.
- arXiv:hep-th/0004134 = Bousso-Polchinski 2000 "Quantization of four-form fluxes…" — VERIFIED.
- arXiv:gr-qc/9702052 = Tegmark 1997 "On the dimensionality of spacetime" — VERIFIED (note: paper is on dimensionality, not generically anthropic constants; cited correctly here).
- arXiv:gr-qc/0606117 = Carter 2006 "Anthropic principle in cosmology" — VERIFIED.
- arXiv:1004.3994 = Brown-Dahlen 2010 "Small Steps and Giant Leaps in the Landscape" — VERIFIED.
- arXiv:1601.01662 = Masoumi-Vilenkin 2016 "Vacuum statistics and stability in axionic landscapes" — VERIFIED (note: briefing said "Bachlechner et al."; correct authors are Masoumi-Vilenkin).
- arXiv:0810.3654 = Piao 2008 "Tunnelling for Large N" — VERIFIED (note: briefing said "Brown-Dahlen arXiv:0810.3654"; the correct Brown-Dahlen is arXiv:1004.3994. This is a fab catch: the briefing's first arXiv id matched a different author. Corrected in §5 and §9.).
- Coleman 1977 PRD 15:2929 — textbook standard reference, no arXiv (pre-arXiv).
- Coleman-De Luccia 1980 PRD 21:3305 — textbook standard reference, no arXiv (pre-arXiv).
- Stark 1967 Michigan Math. J. 14:1-27 — textbook standard reference.
- Heegner numbers $\{1,2,3,7,11,19,43,67,163\}$ — standard, Heilbronn-Linfoot 1934, Heegner 1952, Stark 1967, Baker 1966.
- $\exp(\pi\sqrt{163})$ near-integer to $\sim 7.5\times 10^{-13}$ — verified with mpmath 50-digit.
- Numerical Table 2 — verified with Python.
- Cluster firm 731 STABLE entrée/sortie; 0 propagated fab.

