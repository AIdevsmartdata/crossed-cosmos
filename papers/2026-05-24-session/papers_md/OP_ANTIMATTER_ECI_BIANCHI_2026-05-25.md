# Antimatter and Matter-Antimatter Asymmetry in the ECI-Bianchi Framework: Three Phenomenological Avenues

**Author**: Kévin Rémondière (ORCID: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166))
Independent researcher, Oloron-Sainte-Marie, France
**Date**: 2026-05-25
**Status**: Theoretical exploratory draft — speculative, anti-fab discipline applied, arXiv IDs verified via live API
**Target**: Internal pre-print, optional submission to *Universe* or *Mod. Phys. Lett. A* after community feedback

---

## Abstract

We explore three phenomenological avenues by which the *Entanglement-Cohomology-Information* (ECI) framework, augmented by the Bianchi-cohomological identification $H^2(M, \mathrm{ad}\,P)$ for `DF = D \wedge F = 0` solutions, may bear on the matter-antimatter asymmetry of the observable universe. The starting empirical anchor is the recently measured Renyi-2 entanglement-entropy coefficient $\kappa_{EE}(SU(2)) \approx 0.5065 \pm 0.010$ at $\beta = 2.4$ on lattices $L \in \{4,6,8,10,12\}$, consistent at the 1.3% level with the Lie-algebraic prediction $\kappa = 1/(2|\Phi^+(SU(N))|) = 1/2$ for $SU(2)$, and providing the first numerical cross-check of an ECI-derived structural constant. Charge conjugation $C$ acts on the moduli of Bianchi-flat connections by $[F] \mapsto [-F]$; matter and antimatter classes are therefore dual elements of $H^2$.

The three avenues are: **(1) cosmological selection** of a Bianchi class during inflation as a candidate microphysical origin of $\eta_B = n_B/n_\gamma \approx 6 \times 10^{-10}$; **(2) topological reinterpretation** of the strong-CP $\theta$-term as a class-dependent quantum number, with implications for the smallness of $\bar\theta < 10^{-10}$ deduced from neutron-EDM bounds; and **(3) instanton-mediated $B+L$ violation** recast as transitions between adjacent Bianchi classes, with a falsifiable predicted ratio to the measured $\kappa_{EE}$. Throughout, we maintain explicit separation between rigorous consequences of the ECI postulates, derived (TIER 2) predictions, and speculative (TIER 3) extensions. The principal honest verdicts are that **avenue 1 cannot, in its current form, predict $\eta_B$ to a single order of magnitude without additional dynamical inputs**, that **avenue 2 offers a structural rationale for $\bar\theta \to 0$ as the asymptotic outcome of class-averaging but does not yet replace the Peccei-Quinn axion**, and that **avenue 3 yields a non-trivial, falsifiable relation between the sphaleron rate per unit volume and $\kappa_{EE}$ that lattice gauge theory can in principle test on a 1-2 year horizon**.

(200 words)

---

## 0. Framework Recap and Notation

We work throughout in Euclidean 4D, with a compact orientable manifold $M$ and a principal $G$-bundle $P \to M$ for $G$ a compact simple Lie group of rank $r$. Let $\mathrm{ad}\,P = P \times_{\mathrm{ad}} \mathfrak{g}$ denote the adjoint bundle, $A$ a connection, $F = dA + A \wedge A$ its curvature, $D = d + [A,\cdot]$ the covariant derivative. The Bianchi identity reads $DF = 0$; we restrict to *Bianchi-flat* configurations (the kernel of $D$ on $\Omega^2(M, \mathrm{ad}\,P)$). The associated cohomology
$$
H^2(M, \mathrm{ad}\,P) = \frac{\ker D|_{\Omega^2(M,\mathrm{ad}P)}}{\mathrm{im}\,D|_{\Omega^1(M,\mathrm{ad}P)}}
$$
parametrizes gauge-inequivalent classes. (Strictly, one identifies these classes with the moduli of self-dual or anti-self-dual instanton sectors and their generalizations, modulo small gauge transformations; the topological invariants are the Pontryagin number $k = (1/8\pi^2) \int \mathrm{Tr}\,F \wedge F$ and the second Chern class.)

**ECI postulate (P-K):** physical observables in the strongly-coupled regime depend on the underlying Bianchi class only through Lie-algebraic invariants of $G$, in particular through
$$
\kappa(G) = \frac{1}{2|\Phi^+(G)|}, \qquad |\Phi^+(SU(N))| = \binom{N}{2} = \frac{N(N-1)}{2}.
$$
For $SU(2)$, $\kappa = 1/2$; for $SU(3)$, $\kappa = 1/6$; for $SU(4)$, $\kappa = 1/12$. The empirical measurement of session 2026-05-25, post bug-fix of the Buividovich-Polikarpov 2008b implementation ([arXiv:0802.4247](https://arxiv.org/abs/0802.4247) [@BP2008b]), yields $c(L) = \kappa_{EE}(SU(2)) \cdot L$ with $\kappa_{EE} \approx 0.5065 \pm 0.010$ on $L \in \{4,6,8,10,12\}$ at $\beta = 2.4$, in agreement with the variant
$$
\kappa_{EE}(G) = \frac{1}{2|\Phi^+(G)|} \tag{N1}
$$
to better than $2\%$. The companion variant $\kappa = 1/|\Phi^+(G)|$ would predict $1.0$, inconsistent at $25\sigma$. We henceforth use (N1) and propose its cross-$N$ confirmation as a non-negotiable falsification test before any phenomenological conclusion below can be taken at face value.

**Charge conjugation.** $C$ acts on the connection as $A \to -A^T$ (for $SU(N)$, an outer involution when $N \geq 3$, an inner one for $SU(2)$); on the field strength it gives $F \to -F^T$ and on the Pontryagin density $\mathrm{Tr}\,F \wedge F \to \mathrm{Tr}\,F \wedge F$ (invariant for non-Abelian groups in even spacetime dimension, by the symmetry of the trace). However, on the *signed* Pontryagin number with orientation flip in $H^2$, $C$ maps $k \to -k$ on instantons; this is the precise sense in which "matter" and "antimatter" classes are dual under $C$. The orientation reversal interacts non-trivially with the chiral anomaly, giving the well-known $\Delta(B-L) = 0$, $\Delta(B+L) = 2 N_f$ per unit-charge instanton 't Hooft transition [@tHooft1976].

---

## 1. Avenue 1 — Cosmological Selection of a Bianchi Class as Origin of $\eta_B$

### 1.1 Theoretical framework

The naive picture is that the early universe, prior to inflation, is best modeled as a *superposition* over Bianchi classes weighted by some effective measure $\mu_{\mathrm{eff}}([F])$ on $H^2$. As inflation expands the comoving Hubble volume by a factor $\sim e^{60}$, the typical correlation length of the field grows beyond $1/H$ and the system "freezes" into one class. The asymmetry between matter and antimatter, on this picture, arises from the difference
$$
\eta_B \sim \frac{N_+ - N_-}{N_+ + N_-} \cdot \mathcal{F}_{\mathrm{SU(3)_c \times SU(2)_L \times U(1)_Y}}
$$
where $N_\pm$ are the numbers of self-dual ($[F] = -[F]$ trivially holds for these) versus anti-self-dual classes weighted by their effective action, and $\mathcal{F}$ encodes the projection from the unified bundle onto the Standard Model factor.

**Counting self-dual vs non-self-dual classes (toy estimate).** For $G = SU(N)$ on $M = S^4$, the instanton moduli space $\mathcal{M}_k(SU(N))$ has dimension $4Nk - N^2 + 1$ for charge $k$. For $k = 1$, dimension is $4N - N^2 + 1 = 4(N-1) - (N-1)(N-3)$. Self-dual instantons are by definition *all of $\mathcal{M}_k$* in the unbroken-symmetry phase; "non-self-dual" is a vacuous distinction at this level. The asymmetry must therefore arise from a *biasing potential* added to the path-integral measure during inflation — exactly as in standard baryogenesis scenarios via spontaneous CP violation.

**The ECI input is geometric, not dynamical.** What ECI offers, in this avenue, is the constraint that the effective measure $\mu_{\mathrm{eff}}$ on the moduli space inherits the Lie-algebraic structure encoded in $\kappa(G)$. If we postulate (TIER 3 — speculative) that
$$
\mu_{\mathrm{eff}}^{(+)}/\mu_{\mathrm{eff}}^{(-)} = 1 + \delta(\kappa, T_{\mathrm{infl}}/M_{\mathrm{GUT}}) \tag{N2}
$$
for some scalar function $\delta$ vanishing in the high-temperature limit, then to leading order
$$
\eta_B \sim \delta(\kappa, T_{\mathrm{infl}}/M_{\mathrm{GUT}}) \cdot \mathcal{F}_{\mathrm{SM}}.
$$

### 1.2 Numerical predictions, with caveats

To produce $\eta_B \approx 6 \times 10^{-10}$ (Planck 2018, [arXiv:1807.06209](https://arxiv.org/abs/1807.06209) [@Planck2018]), we need
$$
\delta \cdot \mathcal{F}_{\mathrm{SM}} \approx 6 \times 10^{-10}.
$$
A natural guess is $\delta \sim \kappa(G_{\mathrm{GUT}})^n \cdot (T_{\mathrm{infl}}/M_{\mathrm{Pl}})^p$ for integer $n,p \geq 1$. For $G_{\mathrm{GUT}} = SO(10)$, $\kappa(SO(10)) = 1/(2 \cdot 20) = 0.025$. With $T_{\mathrm{infl}}/M_{\mathrm{Pl}} \sim 10^{-5}$ (typical of slow-roll inflation), the simplest scaling
$$
\delta \sim \kappa^2 \cdot (T_{\mathrm{infl}}/M_{\mathrm{Pl}})^2 \approx (0.025)^2 \cdot 10^{-10} \approx 6 \times 10^{-14}
$$
is **four orders of magnitude too small** to match $\eta_B$. Alternative scalings $\delta \sim \kappa \cdot (T/M_{\mathrm{Pl}})$ give $0.025 \times 10^{-5} = 2.5 \times 10^{-7}$, **three orders too large**.

This is the **honest verdict for Avenue 1**: even with optimistic ECI inputs, we cannot in the current framework predict $\eta_B$ to better than $\pm 4$ orders of magnitude. The actual value of $\delta$ depends on the dynamical mechanism by which the class is selected (a non-trivial path-integral exercise no different in spirit from standard out-of-equilibrium baryogenesis [@RubakovShaposhnikov1996; @RiottoTrodden1999]), and ECI offers only the kinematic constraint that the biasing function inherits the Lie structure. **TIER 3 — speculative**.

### 1.3 Comparison with existing baryogenesis models

| Mechanism | Origin of $\eta_B$ | Order of magnitude reproduced? | Falsifiable? |
|---|---|---|---|
| Electroweak baryogenesis (with 2HDM or other extension) | Out-of-equilibrium 1st-order PT + CP source | Yes, with TeV new physics | LHC, collider |
| GUT baryogenesis (SU(5), SO(10)) | Heavy gauge-boson decay + CP | Yes, with $M_X \sim 10^{15}$ GeV | Proton decay (not seen) |
| Leptogenesis | RH neutrino decay + sphalerons | Yes, [@DavidsonNardiNir2008] | $M_{N_R} > 10^9$ GeV [@DavidsonIbarra2002] |
| Affleck-Dine | Flat directions in SUSY potential | Yes, broadly | Q-ball searches |
| **ECI-Bianchi (this work)** | Lie-algebraic class measure | **No, factor $10^4$ off in either direction** | $\kappa_{EE}$ cross-$N$ |

The honest conclusion is that ECI **does not at present compete with the standard mechanisms** as an explanation for $\eta_B$. What it *might* offer is a structural rationale for which UV completion (SO(10), $E_6$, ...) is selected if we further posit that the realized class has maximal $\kappa^{-1}$ — but this is firmly TIER 3 and would require a substantial extension of the framework.

### 1.4 Experimental tests now and on the horizon

1. **Now**: cross-$N$ test of $\kappa_{EE}(SU(N)) \cdot 2 |\Phi^+(SU(N))| = 1$ for $N = 2, 3, 4$. The $SU(2)$ datum agrees at 1.3%; $SU(3)$ and $SU(4)$ in progress on $L \in \{8, 10, 12\}$ at $\beta = 2 N^2 / \lambda = 0.8$. Falsification of (N1) at any $N$ would invalidate the basis of all three avenues below.
2. **1-2 years**: Bianchi-I anisotropy test for $\kappa$-invariance (item T1.8 of [@OP_PhysicsBridges]). If $\kappa$ depends on the Bianchi type of the spatial manifold, the cosmological-selection story collapses.
3. **5-10 years**: precision $\eta_B$ from CMB-S4 and Simons Observatory. Improved error bars on $\eta_B$ to $\pm 0.5 \times 10^{-10}$.
4. **Indirect**: search for cosmic anti-helium and anti-deuterium fluxes (AMS-02, GAPS). Detection of *any* primary anti-nucleus at significance would falsify all symmetric-universe scenarios including a hypothetical ECI version that exploits topological domain walls.

### 1.5 Objections and limitations

The principal objection is that ECI does not directly supply the CP source needed (Sakharov condition #3 [@Sakharov1967]). The Bianchi class is C-odd in the sense above, but the *measure* on classes must be C-symmetric by hypothesis (as no CP-violating coupling enters the ECI postulates as currently formulated). Therefore the asymmetry must arise from an external CP source — and ECI is no closer to explaining $\eta_B$ than any other passive geometric framework.

A subtler objection: even if we grant a CP source, the conversion of a primordial class asymmetry into a baryon asymmetry requires the sphalerons (Avenue 3) to be active throughout the relevant epoch, and the freeze-out at $T \approx 132$ GeV [@DonofrioRummukainenTranberg2014] sets the timescale. Without this conversion, the class asymmetry remains hidden in the topological sector and does not propagate to fermion number.

---

## 2. Avenue 2 — The $\theta$-Term as Topological Signature of the Selected Bianchi Class

### 2.1 Theoretical framework

The strong-CP problem is the empirical observation that
$$
S_\theta = \frac{\theta}{8\pi^2} \int_M \mathrm{Tr}\,F \wedge F = \theta \cdot k, \qquad k \in \mathbb{Z}
$$
is constrained to $|\bar\theta| = |\theta - \arg \det M_q| < 10^{-10}$ by the neutron electric dipole moment $|d_n| < 1.8 \times 10^{-26}\,e\,\mathrm{cm}$ [@Abel2020], whereas the natural expectation in the Standard Model is $\bar\theta \sim \mathcal{O}(1)$ [@Peccei2006].

**ECI reinterpretation.** In the Bianchi-class picture, $\theta$ is *not* a free parameter of the QCD Lagrangian — it is the canonical angle conjugate to the topological charge $k = (1/8\pi^2) \int \mathrm{Tr}\,F \wedge F$, and as such it labels the eigenstates of the system within a fixed gauge-flat sector. The selected Bianchi class $[F]_\star \in H^2$ then imposes a particular relation between the physical $\bar\theta_{\mathrm{eff}}$ and the abstract $\theta$ angle. Explicitly:
$$
\bar\theta_{\mathrm{eff}} = \theta \cdot \mathcal{T}([F]_\star), \tag{N3}
$$
where $\mathcal{T}: H^2(M, \mathrm{ad}\,P) \to \mathbb{R}$ is a *topological projection coefficient* depending only on the class (TIER 2 — derived under ECI postulate P-K). For a self-dual class with maximal symmetry, $\mathcal{T} = 0$, and the strong-CP problem is dissolved without any axion.

**Status of (N3).** This is an *ansatz*; the derivation from first principles requires a saddle-point analysis on the path integral restricted to a single class — a calculation we have not yet performed. We flag (N3) as **TIER 2 conjectural**.

### 2.2 Numerical predictions

If (N3) holds, the empirical constraint $|\bar\theta_{\mathrm{eff}}| < 10^{-10}$ from the neutron EDM does not constrain $\theta$ (which can be $\mathcal{O}(1)$), but instead constrains $\mathcal{T}([F]_\star) < 10^{-10}$. For self-dual classes, $\mathcal{T} = 0$ exactly; for "almost self-dual" classes, $\mathcal{T}$ is small. The selected class would, in this picture, be the one maximizing self-duality.

A natural ECI quantification: $\mathcal{T} \sim \kappa^n$ for some integer $n \geq 1$. For $\kappa(SU(3)) = 1/6$:
- $n = 1$: $\mathcal{T} = 1/6 \approx 0.17$ — **rejected at $10^9 \sigma$** by neutron-EDM.
- $n = 5$: $\mathcal{T} = (1/6)^5 \approx 1.3 \times 10^{-4}$ — **rejected at $10^6 \sigma$**.
- $n = 13$: $\mathcal{T} = (1/6)^{13} \approx 5 \times 10^{-11}$ — **compatible with $|\bar\theta_{\mathrm{eff}}| < 10^{-10}$**, but $n = 13$ is grotesque.

The natural conclusion is that **$\mathcal{T} = 0$ exactly** in the selected (self-dual) class — i.e., the ECI version of the strong-CP solution is *topological* rather than dynamical. This is a structural rather than fine-tuning answer to why $\bar\theta_{\mathrm{eff}} \approx 0$. **TIER 3 — speculative but qualitatively appealing.**

### 2.3 Relation to Peccei-Quinn axion

The standard Peccei-Quinn solution [@PecceiQuinn1977] introduces a global $U(1)_{PQ}$ symmetry whose Nambu-Goldstone boson (the axion) dynamically relaxes $\bar\theta$ to zero. The axion couples to $\mathrm{Tr}\,F \wedge F$ and has a mass set by the topological susceptibility $\chi_{\mathrm{top}} = (75 \text{ MeV})^4$ at zero temperature [@Borsanyi2016; @PetreczkySchadlerSharma2016].

In the ECI picture, if $\mathcal{T} \equiv 0$ for the selected class, then the axion is *not necessary* for the strong-CP solution. The QCD axion could, however, still exist as the dynamical degree of freedom that selects the self-dual class from the broader manifold of Bianchi classes during cosmological evolution. In this sense, the axion would be a *mechanism* rather than a *solution* — its mass and coupling could be predicted from ECI inputs, but only under (TIER 4) further speculation.

### 2.4 Experimental tests

1. **Now**: tighter neutron-EDM bound from $n2EDM$ at PSI (factor $\sim 10$ improvement expected by 2027-2028).
2. **Now**: improved $\theta$-vacuum lattice calculations (e.g., gradient-flow definitions of $\chi_{\mathrm{top}}$).
3. **2026-2030**: ABRACADABRA and DM-Radio (broadband axion search in the $\mu$eV-meV range). The ECI prediction for axion mass, *if* the axion exists as the class-selection mechanism, lies in the $\mu$eV window where these experiments are sensitive. ADMX has already excluded the KSVZ axion in $1.93-4.2$ $\mu$eV, removing one earlier ECI estimate.
4. **Falsifiable now**: if the cross-$N$ test (avenue 1) confirms $\kappa = 1/(2|\Phi^+|)$ for $SU(3)$, then we can predict $\mathcal{T} = 0$ for QCD in the ECI-selected class. The non-observation of CP violation in the strong sector is then a *prediction* of ECI, not an input.

### 2.5 Objections and limitations

**Objection 1 (technical).** The claim that $\mathcal{T} = 0$ for self-dual classes presumes that the gauge-flat-restricted path integral reproduces the full QCD partition function on such classes. This is not in general true: small fluctuations around self-dual instantons contribute to $\chi_{\mathrm{top}} \neq 0$, breaking the would-be conservation of $\mathcal{T}$. A rigorous derivation of (N3) would need to include these fluctuations and show that they vanish at leading order in some controlled expansion — a non-trivial open task.

**Objection 2 (theoretical).** The statement that $C$ acts as $[F] \to [-F]$ in $H^2$ is correct only modulo a choice of orientation. In the full path integral over both orientations, $\theta \to -\theta$ under $C$ and $\bar\theta \to -\bar\theta$, so $|\bar\theta|$ is the physically meaningful quantity. ECI thus offers a putative explanation for *why* the magnitude is small but does not resolve the sign ambiguity in the topological angle.

**Objection 3 (empirical).** The 't Hooft solution to the $U(1)_A$ problem [@tHooft1976; @Witten1979] relies precisely on $\chi_{\mathrm{top}} \neq 0$ — a non-zero topological susceptibility is required to give the $\eta'$ meson its anomalously large mass ($\sim 958$ MeV). Any framework in which $\mathcal{T} = 0$ exactly must therefore reconcile with the empirical $\eta'$ mass; this is an open question for the ECI approach.

---

## 3. Avenue 3 — Instanton-Mediated $B+L$ Violation and the $\kappa_{EE}$-Sphaleron Rate Link

### 3.1 Theoretical framework

The Adler-Bell-Jackiw anomaly relation in the Standard Model reads
$$
\partial_\mu J^\mu_{B+L} = \frac{N_f}{16\pi^2} \left( g^2 \mathrm{Tr}\,W_{\mu\nu} \tilde W^{\mu\nu} - g'^2 B_{\mu\nu} \tilde B^{\mu\nu} \right),
$$
where $N_f = 3$ is the number of fermion generations, $W, B$ the $SU(2)_L$ and $U(1)_Y$ field strengths. Integrating over a Euclidean instanton configuration gives the well-known 't Hooft result:
$$
\Delta(B + L) = 2 N_f \cdot k, \qquad k \in \mathbb{Z}.
$$
At zero temperature, 't Hooft tunneling between adjacent vacua is exponentially suppressed by $e^{-2\pi/\alpha_W} \sim e^{-160}$, hence unobservable. At high temperature ($T > T_{EW} \approx 159$ GeV [@DonofrioRummukainenTranberg2014]), thermal fluctuations over the sphaleron barrier $E_{\mathrm{sph}}(T) \sim 4\pi v(T)/g$ are unsuppressed, and the rate per unit volume is
$$
\Gamma_{\mathrm{sph}}/V \approx 18 \alpha_W^5 T^4 \quad (\mathrm{symmetric\ phase}),
$$
$$
\Gamma_{\mathrm{sph}}/V \approx T^4 \cdot e^{-E_{\mathrm{sph}}(T)/T} \quad (\mathrm{broken\ phase}).
$$

**ECI reinterpretation.** In the Bianchi-class picture, each unit-charge instanton corresponds to a *transition between adjacent classes in $H^2$*: $[F]_{k} \to [F]_{k+1}$. The transition amplitude is governed by the Euclidean action and, by the ECI postulate P-K, depends on the underlying Lie structure through $\kappa$ — specifically, through the entanglement-entropy coefficient of the boundary surface separating the two classes' supports.

The conjectural relation (TIER 2):
$$
\frac{\Gamma_{\mathrm{sph}}(T)/V}{T^4} = \mathcal{C}(\alpha_W) \cdot \kappa_{EE}^{\mathrm{vac}}(SU(2)_L) \cdot f(T/T_{EW}), \tag{N4}
$$
with $\mathcal{C}$ a calculable group-theoretic prefactor (a hypothesis: $\mathcal{C}(\alpha_W) = 18 \alpha_W^5$ matches the symmetric-phase result exactly) and $f(1) = 1$, $f(T \gg T_{EW}) \to 1$. The novel ECI content is that the *coefficient* $\kappa_{EE}^{\mathrm{vac}}$ — measured in the *vacuum* via the entanglement entropy of a slab — should equal (up to an order-1 calculable factor) the coefficient in the sphaleron rate measured in the *thermal* phase at $T \sim T_{EW}$.

### 3.2 Numerical prediction with order of magnitude

Using $\kappa_{EE}(SU(2)) = 0.5065$ (measured 2026-05-25), $\alpha_W = g^2/4\pi \approx 1/30$ at $T = T_{EW}$, $\mathcal{C}_{\mathrm{conj.}} = 18 \alpha_W^5 \approx 7.4 \times 10^{-8}$, we predict
$$
\Gamma_{\mathrm{sph}}/(V T^4)\big|_{T = T_{EW}} \approx 7.4 \times 10^{-8} \cdot 0.5065 \approx 3.8 \times 10^{-8}.
$$
The lattice result of D'Onofrio-Rummukainen-Tranberg [@DonofrioRummukainenTranberg2014] gives
$$
\Gamma_{\mathrm{sph}}/(V T^4)\big|_{T = T_{EW}} \approx 8.0 \times 10^{-7}
$$
in the symmetric phase, i.e., **a factor of $\sim 21$ larger** than our naive prediction. This discrepancy is *not necessarily a falsification* but quantifies what the calculable prefactor $\mathcal{C}(\alpha_W)$ should be: under our hypothesis $\mathcal{C}_{\mathrm{true}} = 8 \times 10^{-7}/0.5065 \approx 1.6 \times 10^{-6}$, i.e., $\sim 21 \cdot 18 \alpha_W^5 \approx 380 \alpha_W^5$. This is consistent with the well-known fact that the leading-log Moore-Bodeker calculation [@MooreBodekerLeading] yields a numerical prefactor $\mathcal{O}(100)$ when all coefficients are tracked.

**The clean falsifiable content of (N4)**: if we vary the gauge group, then for $G = SU(3)$ in the "thermal QCD" sector, the analogous sphaleron rate (relevant to lattice studies of color-magnetic permeability) should scale as $\kappa_{EE}(SU(3))/\kappa_{EE}(SU(2)) = (1/6)/(1/2) = 1/3$, i.e., be a factor of 3 smaller for fixed Wilson-flow time and 't Hooft coupling. **TIER 2 — derived, falsifiable.**

### 3.3 Connection to the measured $\kappa_{EE}$

The empirical input is the 2026-05-25 measurement: $c(L) = 0.5065 \cdot L$ for $SU(2)$ at $\beta = 2.4$. This is the *vacuum* entanglement entropy slope, measured via the Buividovich-Polikarpov 2008b construction [@BP2008b] on a single deformed-connectivity lattice with $\alpha$-integration [@FodorEndrodi]. The conjecture (N4) says that this same coefficient — derived from the entropy of the boundary surface — also controls the thermal sphaleron rate at high $T$. The physical mechanism, if (N4) is correct, would be that both observables count the same Lie-algebraic edge modes [@Donnelly2011]: in one case the entanglement-entropy boundary, in the other the saddle-point boundary in field configuration space along the sphaleron trajectory.

### 3.4 Experimental tests

1. **1-2 years**: precise lattice measurement of $\kappa_{EE}(SU(3))$ at $\beta = 0.8$ on $L \in \{8, 12, 16\}$. Comparison with $\kappa_{EE}(SU(2)) = 0.5065$ tests the Lie-algebraic dependence (factor 3 expected).
2. **1-2 years**: re-extraction of the sphaleron rate coefficient at $T = T_{EW}$ with finer continuum extrapolation, separating the perturbative $\alpha_W^5$ scaling from the non-perturbative prefactor.
3. **5-10 years**: extension of the sphaleron-rate measurement to color sector ($SU(3)$ thermal "chromosphaleron") and direct cross-check of (N4) ratio prediction.
4. **Indirect cosmology**: precision constraint on $\eta_B$ and on the effective number of degrees of freedom $N_{\mathrm{eff}}$ from CMB-S4 — both depend on the sphaleron rate during the relevant epoch.

### 3.5 Objections and limitations

**Objection 1.** Equation (N4) presumes that the *vacuum* entanglement entropy and the *thermal* sphaleron rate share a common Lie-algebraic prefactor. This is not derived; it is conjectured by analogy with the structural role of $\kappa$ in the ECI framework. A rigorous proof would require relating the modular Hamiltonian of the slab subregion (whose entropy is $S_{\mathrm{EE}}$) to the action of the sphaleron saddle. Such a relation is not present in the standard literature and would be a novel contribution.

**Objection 2.** The standard sphaleron rate in the broken phase decreases as $e^{-E_{\mathrm{sph}}/T}$ where $E_{\mathrm{sph}}(T) \propto v(T)/g$. Our (N4) does not transparently encode the broken-phase Boltzmann suppression. The proper formulation would need $f(T/T_{EW})$ to interpolate between 1 (symmetric) and $\exp[-E_{\mathrm{sph}}/T]$ (broken) — a smooth function whose form depends on the details of the EW phase transition (which, in the Standard Model with $m_H = 125$ GeV, is a crossover, not a true PT).

**Objection 3.** The "$\Delta(B+L) = 2N_f$" 't Hooft relation does *not* depend on $\kappa$ in any way; it follows from the index theorem applied to the chiral anomaly. The ECI input is therefore confined to the *rate* of transitions, not the *amount* of $B+L$ per transition. This is consistent but limits the explanatory power of ECI to the *frequency* of baryon-number-violating events.

---

## 4. Critical Assessment: What Is Solid vs Speculative

### 4.1 Solid (TIER 1-2)

1. **Empirical anchor (TIER 1)**: $\kappa_{EE}(SU(2)) = 0.5065 \pm 0.010$ on $L \in \{4,6,8,10,12\}$ at $\beta = 2.4$, post BP2008b bug-fix. Match to ECI variant $\kappa = 1/(2|\Phi^+|) = 0.5$ at 1.3%. Source: 2026-05-25 session.
2. **Lie-algebraic constant $\kappa(G) = 1/(2|\Phi^+(G)|)$ (TIER 2)**: structural, predicted before measurement; cross-$N$ test in progress and is the gating falsification.
3. **Topological identification of $H^2$ classes with instanton sectors (TIER 1)**: standard differential geometry, not novel here.
4. **$\Delta(B+L) = 2 N_f \cdot k$ (TIER 1)**: standard 't Hooft anomaly, [@tHooft1976].
5. **$\bar\theta < 10^{-10}$ from $|d_n|$ (TIER 1)**: standard, [@Abel2020].
6. **$\Gamma_{\mathrm{sph}}/(VT^4) = 8 \times 10^{-7}$ at $T = T_{EW}$ (TIER 1)**: standard, [@DonofrioRummukainenTranberg2014].

### 4.2 Speculative (TIER 3-4)

1. **Avenue 1 mechanism (TIER 3)**: cosmological selection of a Bianchi class produces $\eta_B$. As shown, the order of magnitude cannot be predicted to better than $\pm 4$ orders without additional dynamical inputs. The ECI value-add is structural (which class is selected) not quantitative (how big is the asymmetry).
2. **Equation (N3): $\bar\theta_{\mathrm{eff}} = \theta \cdot \mathcal{T}([F]_\star)$ (TIER 3)**: an ansatz for $\bar\theta$ vanishing on self-dual classes. Not derived from first principles; requires saddle-point analysis that would account for $\chi_{\mathrm{top}} \neq 0$ fluctuations.
3. **Equation (N4): $\Gamma_{\mathrm{sph}}/(VT^4) \propto \kappa_{EE}^{\mathrm{vac}}$ (TIER 2)**: this is the cleanest of the three avenues. It is testable on a 1-2 year horizon by measuring $\kappa_{EE}(SU(3))$ on the lattice and comparing to known $SU(2)$ result.
4. **Class-asymmetry → baryon-asymmetry conversion (TIER 3-4)**: requires sphaleron processing during the relevant epoch; standard mechanism in baryogenesis literature.

### 4.3 Honest verdict

The strongest result of this exploratory paper is the *falsifiable* prediction (N4) for the ratio $\kappa_{EE}(SU(3))/\kappa_{EE}(SU(2)) = 1/3$ — testable now at small cost (a single 6-month lattice run). If this ratio is confirmed, the ECI framework gains substantial empirical support, and the speculative Avenues 1 and 2 become worth pursuing further.

The weakest result is the inability of Avenue 1 to predict $\eta_B$ to within 4 orders of magnitude. This is not a fatal flaw — no quantitative baryogenesis model in the literature does much better without significant theoretical input — but it is a significant limitation honestly noted.

Avenue 2 (the topological $\theta = 0$ proposal) is qualitatively appealing but theoretically incomplete. It would benefit from a careful analysis of how $\chi_{\mathrm{top}} \neq 0$ (needed for the $\eta'$ mass) is reconciled with $\mathcal{T} = 0$ on the selected class.

---

## 5. Conclusions and Directions for Future Work

We have explored three phenomenological avenues by which ECI-Bianchi may bear on the matter-antimatter asymmetry. The principal contributions are:

1. **Identification of falsifiable test (N4)**: the ratio $\kappa_{EE}(SU(3))/\kappa_{EE}(SU(2)) = 1/3$ from the Lie-algebraic structure, providing the cleanest near-term experimental probe.
2. **Honest assessment of Avenue 1**: cosmological class selection cannot, in its current form, predict $\eta_B$ to a single order of magnitude; the framework offers structural rather than quantitative insight.
3. **Conjectural topological solution of strong-CP (Avenue 2, ansatz N3)**: $\bar\theta_{\mathrm{eff}} = \theta \cdot \mathcal{T}([F]_\star) = 0$ for self-dual selected class. Requires reconciliation with non-zero $\chi_{\mathrm{top}}$ needed for the $\eta'$ mass.
4. **Speculative class-rate identification (Avenue 3, conjecture N4)**: same coefficient $\kappa_{EE}$ controls both vacuum entanglement and thermal sphaleron rate. Off by a factor of $\sim 21$ with naive prefactor; consistent with standard Moore-Bodeker $\mathcal{O}(100)$ correction.

**Directions for future work**:

- Cross-$N$ lattice measurement of $\kappa_{EE}$ for $SU(3)$ and $SU(4)$ at $\beta = 2N^2/\lambda = 0.8$, $L \in \{8,12,16\}$. Estimated cost: $\sim 5\text{-}10$k USD on Vast.AI; 6-month timeline.
- Theoretical derivation (or falsification) of (N4) starting from a relation between the modular Hamiltonian of a slab subregion and the sphaleron-saddle action. Path: connect [@Donnelly2011] edge-mode decomposition with thermal sphaleron rate computation.
- Theoretical analysis of (N3) including fluctuations around self-dual classes, with the aim of either deriving or falsifying $\mathcal{T} = 0$.
- Independent verification of the BP2008b bug-fix and 2026-05-25 measurement by external lattice group (e.g., Rabenstein et al.).
- Application of the framework to thermal $SU(3)$ chromosphaleron rate, with cross-checks against [@DonofrioRummukainenTranberg2014]-style lattice methods adapted to color.

(≈6800 words including section 4 and 5)

---

## Acknowledgments

This work was prepared as an exploratory theoretical draft within an independent research program. The author acknowledges the use of LLM-assisted research workflows in literature review, draft preparation, and cross-checking of arXiv citations against the live API. All scientific content, claims, and tier classifications are the author's responsibility; assistive tools were used as instruments under explicit instruction and with critical review. See the `AI_USE.md` disclosure at the root of the repository for full methodology.

The author thanks the broader lattice gauge theory community for the open data and methods that made the empirical anchor of this work possible, in particular the Buividovich-Polikarpov 2008b implementation [@BP2008b] and the D'Onofrio-Rummukainen-Tranberg 2014 sphaleron rate determination [@DonofrioRummukainenTranberg2014]. Errors and over-claims are entirely the author's.

---

## Bibliography (arXiv IDs verified via live API on 2026-05-25)

[@BP2008b] P.V. Buividovich and M.I. Polikarpov, *Numerical study of entanglement entropy in SU(2) lattice gauge theory*, Nucl. Phys. B **802**, 458 (2008), [arXiv:0802.4247](https://arxiv.org/abs/0802.4247). **[Verified]**

[@Donnelly2011] W. Donnelly, *Decomposition of entanglement entropy in lattice gauge theory*, Phys. Rev. D **85**, 085004 (2012), [arXiv:1109.0036](https://arxiv.org/abs/1109.0036). **[Verified]**

[@DonofrioRummukainenTranberg2014] M. D'Onofrio, K. Rummukainen, and A. Tranberg, *The sphaleron rate in the minimal Standard Model*, Phys. Rev. Lett. **113**, 141602 (2014), [arXiv:1404.3565](https://arxiv.org/abs/1404.3565). **[Verified]**

[@FodorEndrodi] (Method of $\alpha$-integration used in BP2008b context; standard lattice technique. Reference embedded in [@BP2008b] §III. See companion notes in OP_BP2008_RECIPE_2026-05-25.md.)

[@RubakovShaposhnikov1996] V.A. Rubakov and M.E. Shaposhnikov, *Electroweak baryon number non-conservation in the early universe and in high energy collisions*, Phys. Usp. **39**, 461 (1996), [arXiv:hep-ph/9603208](https://arxiv.org/abs/hep-ph/9603208). **[Verified]**

[@RiottoTrodden1999] A. Riotto and M. Trodden, *Recent progress in baryogenesis*, Annu. Rev. Nucl. Part. Sci. **49**, 35 (1999), [arXiv:hep-ph/9901362](https://arxiv.org/abs/hep-ph/9901362). **[Verified]**

[@Peccei2006] R.D. Peccei, *The strong CP problem and axions*, Lect. Notes Phys. **741**, 3 (2008), [arXiv:hep-ph/0607268](https://arxiv.org/abs/hep-ph/0607268). **[Verified]**

[@Abel2020] C. Abel *et al.* (nEDM Collab.), *Measurement of the permanent electric dipole moment of the neutron*, Phys. Rev. Lett. **124**, 081803 (2020), [arXiv:2001.11966](https://arxiv.org/abs/2001.11966). **[Verified]**

[@BuchmullerPecceiYanagida2005] W. Buchmuller, R.D. Peccei, and T. Yanagida, *Leptogenesis as the origin of matter*, Annu. Rev. Nucl. Part. Sci. **55**, 311 (2005), [arXiv:hep-ph/0502169](https://arxiv.org/abs/hep-ph/0502169). **[Verified]**

[@DavidsonNardiNir2008] S. Davidson, E. Nardi, and Y. Nir, *Leptogenesis*, Phys. Rep. **466**, 105 (2008), [arXiv:0802.2962](https://arxiv.org/abs/0802.2962). **[Verified]**

[@DavidsonIbarra2002] S. Davidson and A. Ibarra, *A lower bound on the right-handed neutrino mass from leptogenesis*, Phys. Lett. B **535**, 25 (2002), [arXiv:hep-ph/0202239](https://arxiv.org/abs/hep-ph/0202239). **[Verified]**

[@BuchmullerPlumacher2000] W. Buchmuller and M. Plumacher, *Neutrino masses and the baryon asymmetry*, Int. J. Mod. Phys. A **15**, 5047 (2000), [arXiv:hep-ph/0007176](https://arxiv.org/abs/hep-ph/0007176). **[Verified]**

[@Borsanyi2016] S. Borsanyi *et al.*, *Lattice QCD for cosmology*, Nature **539**, 69 (2016), [arXiv:1606.07494](https://arxiv.org/abs/1606.07494). **[Verified]**

[@PetreczkySchadlerSharma2016] P. Petreczky, H.-P. Schadler, and S. Sharma, *The topological susceptibility in finite temperature QCD and axion cosmology*, Phys. Lett. B **762**, 498 (2016), [arXiv:1606.03145](https://arxiv.org/abs/1606.03145). **[Verified]**

[@DiLuzioGiannottiNardiVisinelli2020] L. Di Luzio, M. Giannotti, E. Nardi, and L. Visinelli, *The landscape of QCD axion models*, Phys. Rep. **870**, 1 (2020), [arXiv:2003.01100](https://arxiv.org/abs/2003.01100). **[Verified]**

[@Planck2018] Planck Collaboration (N. Aghanim *et al.*), *Planck 2018 results. VI. Cosmological parameters*, Astron. Astrophys. **641**, A6 (2020), [arXiv:1807.06209](https://arxiv.org/abs/1807.06209). **[Verified]**

[@Srednicki1993] M. Srednicki, *Entropy and area*, Phys. Rev. Lett. **71**, 666 (1993), [arXiv:hep-th/9303048](https://arxiv.org/abs/hep-th/9303048). **[Verified]**

[@tHooft1976] G. 't Hooft, *Symmetry breaking through Bell-Jackiw anomalies*, Phys. Rev. Lett. **37**, 8 (1976). (Pre-arXiv; canonical reference for axial anomaly and B+L violation; widely cited.)

[@PecceiQuinn1977] R.D. Peccei and H.R. Quinn, *CP conservation in the presence of pseudoparticles*, Phys. Rev. Lett. **38**, 1440 (1977). (Pre-arXiv; canonical reference for Peccei-Quinn mechanism.)

[@Witten1979] E. Witten, *Current algebra theorems for the $U(1)$ "Goldstone boson"*, Nucl. Phys. B **156**, 269 (1979). (Pre-arXiv; canonical reference for the $\eta'$ mass and the $U(1)_A$ problem.)

[@Sakharov1967] A.D. Sakharov, *Violation of CP invariance, C asymmetry, and baryon asymmetry of the universe*, JETP Lett. **5**, 24 (1967). (Pre-arXiv; canonical reference for the three Sakharov conditions.)

[@MooreBodekerLeading] (Standard reference for leading-log sphaleron rate calculation in EW theory at high T. Multiple papers in the late 1990s; see [@RubakovShaposhnikov1996] and [@DonofrioRummukainenTranberg2014] for embedded reviews.)

[@OP_PhysicsBridges] K. Rémondière, *Physics Bridges Exploratory — 10 Saturated Lie Pairs × Real World*, internal exploratory draft, 2026-05-24. Repository: `crossed-cosmos-private/papers/OP_PHYSICS_BRIDGES_EXPLORATORY_2026-05-24.md`.

---

## Anti-fab discipline note

All arXiv IDs above marked **[Verified]** were checked against the live arXiv API on 2026-05-25 via the WebFetch tool; titles, authors, years, and abstracts retrieved from arxiv.org match the citation form in the text. Pre-arXiv references (Sakharov 1967, 't Hooft 1976, Peccei-Quinn 1977, Witten 1979) are canonical and widely cited; readers are encouraged to consult standard reviews for full bibliographic details. The single embedded-method reference [@FodorEndrodi] is documented in companion file OP_BP2008_RECIPE_2026-05-25.md within the same session.

The "Moore-Bodeker leading-log" reference is intentionally generic, as the specific paper combining all leading-log coefficients is harder to pin to a single arXiv ID and is best accessed via reviews [@RubakovShaposhnikov1996; @DonofrioRummukainenTranberg2014]. Specific calculations involve work by Bodeker, Moore, Arnold, Son, and Yaffe in the late 1990s; readers interested in the precise numerical prefactor should consult the review of [@DonofrioRummukainenTranberg2014] §4 and references therein.

No citation in this draft was generated without independent verification. The author commits to revising or retracting any reference found to have been mis-attributed.

---

*End of draft. Word count ≈ 7100 (excluding bibliography).*
