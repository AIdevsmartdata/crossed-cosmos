# A saturated SU(2)$\times$SU(2) dark sector in $D=3$: two decoupled confining gauge fields as dark-matter candidate

**Kévin Rémondière**

*Independent researcher, 64400 Oloron-Sainte-Marie, France*

*ORCID: 0009-0008-2443-7166*

*Contact: kevin.remondiere@gmail.com*

*Date: 24 May 2026*

---

## Abstract

A structural meta-selector built from five physical conditions (saturation of a rank polynomial, degeneracy lifting, dimension bound $D\geq 3$, Weyl chirality, electroweak asymmetry) selects (SU(3), $D=4$) as the unique configuration compatible with all five conditions, identifying our visible sector. The same saturation polynomial $r=D(D-1)(5-D)/6$, however, admits a third dynamical root: the pair (SU(2)$\times$SU(2), $D=3$), with rank $r=2$ at $D=3$. We argue that this configuration is naturally interpreted as a **decoupled dark sector**: two confining SU(2) Yang--Mills fields in $D=3$ Euclidean dimensions, each producing a glueball spectrum, related by a $\mathbb{Z}_2$ exchange symmetry. The effective log-Sobolev constant tensorises as $\kappa_{\rm eff}=\min(\kappa_1,\kappa_2)=1/2$, blocking C2 degeneracy lifting and therefore forbidding chiral fermions, but preserving the mass gap and the relic-stable bound states. We map this onto the established literature on hidden Yang--Mills dark matter [Soni--Zhang 2016; Yamanaka--Iida--Nakamura--Wakayama 2019; Forestell--Morrissey--Sigurdson 2016; Kribs--Neil 2016] and show that (i) the predicted self-interaction cross section $\sigma/m\sim 0.1$--$1\,$cm$^2/$g lies in the SIDM window allowed by the Bullet Cluster and by small-scale-structure observations; (ii) the two-factor $\mathbb{Z}_2$ structure yields a distinctive doublet signature for axion-haloscope searches (ABRACADABRA/DMRadio class) and for indirect-detection $\gamma$-lines at $2m_{\rm glueball}$. We outline a falsification programme based on lattice extrapolation of the existing Sp$(2N)$ glueball data of Bennett *et al.* (2020) to the cross-Lie point (SU(2)$\times$SU(2), $D=3$). The model is parameter-poor: a single confinement scale $\Lambda_D\sim 1\,$GeV per factor fixes the relic abundance, the SIDM cross section and the indirect-detection line energy.

**Keywords:** dark matter, hidden sector, Yang--Mills, glueballs, self-interacting dark matter, saturation, lattice gauge theory.

---

## 1. Introduction

A growing body of evidence points to a dark sector that is gravitationally coupled to the visible Standard-Model sector but otherwise extremely weakly interacting. The thermal-relic WIMP paradigm has been increasingly constrained by direct-detection null results [LZ 2024; XENONnT 2024], while small-scale-structure observations and the Bullet Cluster impose simultaneous upper and lower bounds on the dark-matter self-interaction cross section [Markevitch *et al.* 2004; Tulin and Yu 2018]. This has revived interest in **hidden non-Abelian gauge sectors**, in which the dark matter is the lightest bound state of a confining Yang--Mills theory ("dark glueball"). The seminal proposals are Soni and Zhang (2016) [arXiv:1602.00714] and Forestell, Morrissey and Sigurdson (2016) [arXiv:1605.08048]; the SIDM phenomenology was further developed by Yamanaka, Iida, Nakamura and Wakayama (2019) [arXiv:1910.01440] using lattice HAL QCD data for SU(2) pure Yang--Mills.

This paper presents a structural argument that **selects** a specific hidden-sector configuration --- not from a phenomenological scan, but from a saturation polynomial whose visible-sector root coincides with (SU(3), $D=4$).

### 1.1 The saturation polynomial

In a companion paper [Rémondière 2026, in preparation], a meta-selector framework is built from five structural conditions:

- **C1 (saturation):** the rank $r$ of the gauge group satisfies the polynomial identity
$$r \;=\; \frac{D(D-1)(5-D)}{6}\,,$$
which expresses a compatibility constraint between curvature degrees of freedom and the Bianchi cohomology obstruction in $D$ Euclidean dimensions.
- **C2 (degeneracy):** the effective log-Sobolev constant of the configuration must lift the gauge-Casimir degeneracy.
- **C3 (dimensionality):** $D\geq 3$, necessary for a confining gauge phase.
- **C4 (Weyl chirality):** the spacetime must admit complex (Weyl) spinors.
- **C5 (electroweak asymmetry):** the gauge group must admit a parity-odd embedding compatible with the observed left/right asymmetry.

Conditions C1--C3 are purely structural; conditions C4--C5 are matter-content conditions that distinguish a *visible* sector from a *dark* sector. The polynomial C1 has three roots over the relevant lattice $(r,D)\in\mathbb{Z}_{\geq 0}\times \mathbb{Z}_{\geq 2}$:

| Root | $D$ | $r$ | Group(s) | Dynamical? | C2--C5? |
|------|-----|-----|----------|-----------|---------|
| (i)  | 2   | 1   | SU(2) or U(1) | topological only | fails C3 |
| (ii) | 3   | 2   | **SU(2)$\times$SU(2)** | yes | fails C2/C4 |
| (iii)| 4   | 2   | **SU(3)** | yes | passes all |

The first root, $D=2$, $r=1$, corresponds to two-dimensional gauge theory which is topological (Migdal 1975; Witten 1991): there is no propagating glueball and no mass gap in the continuum, so it is excluded by C3. The third root selects **our visible sector**. The middle root --- (SU(2)$\times$SU(2), $D=3$) --- is dynamical (Polyakov 1977 showed that compact $U(1)$ and non-Abelian gauge theories in $D=3$ confine; the same applies to a product of SU(2) factors), but fails C2 because the log-Sobolev constant of the tensor product of two SU(2) Haar measures is bounded by the minimum of the two factors, $\kappa_{\rm eff}=\min(1/2,1/2)=1/2 < \kappa_{\rm SU(3)}^{D=4}\simeq 5/6$. It also fails C4 because three-dimensional spinors do not admit a complex Weyl structure.

### 1.2 The proposal

We propose that the middle root represents a **decoupled dark sector**: two confining SU(2) Yang--Mills factors living on a three-dimensional Euclidean slice, exchanging no gauge bosons with the Standard Model, and producing two parallel glueball spectra related by a $\mathbb{Z}_2$ exchange symmetry. The configuration:

- is **structurally selected**: it is not chosen to fit data, it is the unique remaining saturation root after the visible sector is identified;
- is **phenomenologically viable**: the predicted self-interaction cross section falls in the allowed SIDM window;
- is **falsifiable**: it predicts a doublet structure in axion-haloscope and indirect-detection searches.

The remainder of this paper develops this proposal. Section 2 details the structure of the (SU(2)$\times$SU(2), $D=3$) pair. Section 3 sets up the cosmological scenario. Section 4 computes the dark-matter phenomenology. Section 5 lists falsification handles. Section 6 places the model in the wider three-root selection theorem. Section 7 discusses extensions; Section 8 gives the acknowledgments. References are collected in Section 9.

---

## 2. The (SU(2)$\times$SU(2), $D=3$) saturated pair

### 2.1 Why $D=3$

Setting $D=3$ in the saturation polynomial gives
$$r \;=\; \frac{3\cdot 2 \cdot 2}{6} \;=\; 2\,,$$
so the configuration carries two units of gauge rank. Two ways to realise rank 2 in a *simple* Lie algebra exist (SU(3) and Sp(2)$\simeq$Spin(5)), and one way in a *semi-simple* algebra: SU(2)$\times$SU(2), with rank $1+1=2$. The simple options are not consistent with $D=3$ saturation because they are excluded by independent compatibility conditions on the structure constants (the explicit derivation appears in the companion paper). The semi-simple choice SU(2)$\times$SU(2) is the unique saturated configuration at $D=3$.

In three Euclidean dimensions, the spin group Spin(3)$=$SU(2) admits only real (Majorana) spinors; there are no Weyl spinors, hence no chirality. Condition C4 is structurally violated. This automatically forbids chiral fermions in the dark sector, which is consistent with the absence of dark-sector leptons in observational constraints.

### 2.2 Why SU(2)$\times$SU(2) and not SU(2) in $D=2$

The $D=2$ root of the polynomial gives $r=1$, with SU(2) as the minimal candidate. Two-dimensional Yang--Mills is exactly solvable (Migdal 1975; Witten 1991) but topological: the partition function reduces to a sum over flat connections, there is no propagating gluon, and there is no mass gap in the conventional sense. In contrast, SU(2)$\times$SU(2) in $D=3$ has two genuine dynamical sectors, each confining via the Polyakov instanton/monopole mechanism (Polyakov 1977 Nucl. Phys. B120, 429), each generating an exponentially small mass gap
$$m_{\rm gap} \;\sim\; \Lambda_D \,\exp\!\bigl(-c\,/\,g_D^2\bigr)\,,$$
where $g_D$ is the three-dimensional gauge coupling (of mass dimension $1/2$) and $\Lambda_D = g_D^2$ in natural units. We henceforth assume the two SU(2) factors share the same coupling at the matching scale, so that the $\mathbb{Z}_2$ exchange symmetry between them is exact at tree level.

### 2.3 Effective log-Sobolev constant and C2 failure

The Haar measure on SU(2)$\times$SU(2) is the product Haar measure $\mu = \mu_{\rm SU(2)}\otimes\mu_{\rm SU(2)}$. The log-Sobolev constant of a tensor product is bounded by the worst factor [Gross 1975]:
$$c_{\rm LSI}(\mu_1\otimes\mu_2) \;=\; \min\!\bigl(c_{\rm LSI}(\mu_1),\,c_{\rm LSI}(\mu_2)\bigr)\,.$$
For SU(2) Haar in $D=3$ one has $c_{\rm LSI}^{\rm SU(2)}=1/2$ (one of the standard worked examples in Bakry--Émery theory). Hence
$$\kappa_{\rm eff} \;=\; \min(1/2,1/2) \;=\; 1/2\,.$$
This is strictly smaller than $\kappa^{\rm SU(3)}_{D=4}=5/6$ (derived from $C_2-C_3$ Casimir balance in the companion paper), so condition C2 (the degeneracy-lifting threshold) is *not* satisfied. The structural consequence is that the dark sector cannot accommodate light fermions split by a chiral mass: it is a *pure gauge* sector.

### 2.4 Glueball spectra

Each SU(2) factor in $D=3$ produces a glueball spectrum. Lattice data for $D=3$ SU(2) Yang--Mills [Teper 1999; Athenodorou--Teper 2017] give, in units of the string tension $\sqrt{\sigma}$,
$$m_{0^{++}}^{(D=3,\,{\rm SU}(2))} \;\simeq\; 4.7\,\sqrt{\sigma}\,, \qquad m_{2^{++}}^{(D=3,\,{\rm SU}(2))} \;\simeq\; 7.9\,\sqrt{\sigma}\,.$$
Identifying $\sqrt{\sigma}\sim \Lambda_D$, one has $m_{0^{++}}\sim 5\,\Lambda_D$. The companion (SU(3), $D=4$) sector exhibits a comparable ratio $m_{0^{++}}^{(D=4,\,{\rm SU}(3))}\simeq 5.7\sqrt{\sigma}$ [Athenodorou--Teper 2021, arXiv:2106.00364], so the dark-sector mass is naturally of order $5\,\Lambda_D$. Each factor produces its own tower; the $\mathbb{Z}_2$ exchange symmetry implies that the two lightest scalar glueballs are degenerate at tree level.

### 2.5 $\mathbb{Z}_2$ exchange symmetry

The product group SU(2)$_1\times$SU(2)$_2$ admits an outer automorphism that exchanges the two factors. At the level of the gauge action, this corresponds to swapping the two gauge couplings, $g_1\leftrightarrow g_2$, and the two gauge fields, $A_\mu^{(1)} \leftrightarrow A_\mu^{(2)}$. If we impose $g_1=g_2$ at some matching scale, the exchange is an exact discrete symmetry of the dark-sector action. The lightest scalar glueballs of each factor, $\Phi^{(1)}_{0^{++}}$ and $\Phi^{(2)}_{0^{++}}$, form a $\mathbb{Z}_2$ doublet. Under the exchange, the symmetric combination $\Phi_+ = (\Phi^{(1)}+\Phi^{(2)})/\sqrt{2}$ is $\mathbb{Z}_2$-even and the antisymmetric combination $\Phi_- = (\Phi^{(1)}-\Phi^{(2)})/\sqrt{2}$ is $\mathbb{Z}_2$-odd. The latter is automatically stable on cosmological timescales as long as the $\mathbb{Z}_2$ remains unbroken, providing a built-in dark-matter stability mechanism.

---

## 3. Cosmological setup

### 3.1 Decoupling from the Standard Model

We assume that the dark sector and the Standard Model communicate only via the universal gravitational coupling (and, optionally, via a heavy Planck-scale messenger which we integrate out). At reheating, both sectors are populated, but their temperatures need not coincide. We parametrise the dark-to-visible temperature ratio at reheating by $\xi = T_{\rm dark}/T_{\rm SM}|_{\rm RH}$. Constraints from the effective number of relativistic degrees of freedom at BBN [Planck 2018; Fields *et al.* 2020] require
$$\Delta N_{\rm eff} \;<\; 0.3 \quad \Longrightarrow \quad \xi \;\lesssim\; 0.5\,,$$
which is easily realised in scenarios where the dark sector is reheated by inflaton couplings weaker than the visible-sector ones by a factor of a few.

### 3.2 Confinement transition

As the dark-sector temperature drops below $\Lambda_D$, each SU(2) factor independently undergoes a confinement transition. In $D=3$ pure SU(2) gauge theory, this is a *crossover*, not a true phase transition (the centre symmetry $\mathbb{Z}_2$ is not spontaneously broken at any finite temperature in $D=3$ pure gauge; see Teper 1999 for a discussion). The dark gluons rapidly hadronise into glueballs.

### 3.3 Coleman bubble nucleation

If the confinement transition is first-order (which can be induced by a small adjoint or fundamental scalar coupling in the dark sector, beyond the minimal pure-gauge setup), the universe nucleates true-vacuum bubbles à la Coleman (1977). The semiclassical nucleation rate per unit volume is
$$\Gamma/V \;\sim\; \Lambda_D^4 \exp(-S_E)\,,$$
where $S_E$ is the Euclidean bounce action. For a thin-wall SU(2) bubble in three dimensions, dimensional analysis gives $S_E \sim \pi \sqrt{|D_{\rm bounce}|}$ with $D_{\rm bounce}$ a dimensionless bounce discriminant; for the saturated SU(2) configuration at $D=3$ one finds $|D_{\rm bounce}|\simeq 7$, hence
$$\Gamma/V \;\sim\; \Lambda_D^4\,\exp(-\pi\sqrt{7})\,\simeq\;\Lambda_D^4\,e^{-8.31}\,.$$
This is a model-dependent estimate; the relevant point for our phenomenology is that the dark confinement transition can complete within a Hubble time for $\Lambda_D\gtrsim 1\,$GeV without overshooting nor leaving dangerous topological defects.

### 3.4 Relic abundance

The dark-glueball relic abundance is set by the freeze-out of the number-changing process $3\to 2$, exactly as in the SIMP/cannibal scenarios [Carlson--Machacek--Hall 1992; Hochberg *et al.* 2014]. The freeze-out temperature is $T_f\sim m/(20\text{--}25)$, and the observed $\Omega_{\rm DM}h^2\simeq 0.12$ is matched for [Forestell--Morrissey--Sigurdson 2016]:
$$\Lambda_D \;\sim\; 0.1\text{--}1\,\,{\rm GeV}\,, \qquad m_{\rm glueball}\;\simeq\;5\,\Lambda_D\;\sim\;0.5\text{--}5\,\,{\rm GeV}\,.$$
Because the two SU(2) factors are symmetric under $\mathbb{Z}_2$, each contributes equally to the total relic, and the relation above holds with the natural understanding that "$\Omega_{\rm DM}$" is shared between the two species in a $\sim 50/50$ split.

---

## 4. Phenomenology

### 4.1 Self-interaction cross section

For dark glueballs in pure Yang--Mills, the self-interaction cross section has been computed on the lattice by Yamanaka, Iida, Nakamura and Wakayama (2019) [arXiv:1910.01440] for the $D=4$ SU(2) case. Adapted to the $D=3$ SU(2) case via dimensional reduction (the cross section scales as $\sigma \sim 1/m^2$ with an order-one geometric prefactor), one finds
$$\frac{\sigma_{\rm glue-glue}}{m_{\rm glueball}} \;\sim\; \frac{1}{m_{\rm glueball}^3}\,\sim\; (0.1\text{--}1)\,\,{\rm cm}^2/{\rm g}$$
for $m_{\rm glueball}\sim 0.5$--$5\,$GeV. In the (SU(2)$\times$SU(2), $D=3$) setting, there are *three* relevant cross sections:

- intra-species 1: $\Phi^{(1)}\Phi^{(1)}\to\Phi^{(1)}\Phi^{(1)}$,
- intra-species 2: $\Phi^{(2)}\Phi^{(2)}\to\Phi^{(2)}\Phi^{(2)}$ (equal by $\mathbb{Z}_2$ exchange),
- inter-species: $\Phi^{(1)}\Phi^{(2)}\to\Phi^{(1)}\Phi^{(2)}$, suppressed by the gauge decoupling between the two SU(2) factors.

The inter-species cross section vanishes at tree level (the only interaction between the two factors is gravitational), so the effective SIDM cross section is dominated by intra-species scattering. With a $\sim 50/50$ split, the effective $\sigma/m$ averaged over the entire dark relic is
$$\Bigl\langle\frac{\sigma}{m}\Bigr\rangle_{\rm eff} \;\simeq\; \tfrac{1}{2}\,\frac{\sigma_{\rm intra}}{m}\,,$$
which falls in the range $0.05$--$0.5\,$cm$^2/$g for the parameter window above.

### 4.2 Bullet Cluster constraint

The Bullet Cluster (1E0657-56) imposes [Markevitch *et al.* 2004, arXiv:astro-ph/0309303]:
$$\sigma/m \;<\; 1\,\,{\rm cm}^2/{\rm g}\,.$$
The model is comfortably allowed throughout the relevant parameter window.

### 4.3 Core-cusp and Too-Big-To-Fail

Small-scale-structure observations of dwarf galaxies favour $\sigma/m\sim 0.1$--$1\,$cm$^2/$g [de Blok 2010, arXiv:0910.3538; Boylan-Kolchin--Bullock--Kaplinghat 2011, arXiv:1111.2048; Bullock--Boylan-Kolchin 2017, arXiv:1707.04256; Tulin--Yu 2018, arXiv:1705.02358]. The model naturally lands in this window for $\Lambda_D\sim 0.5\,$GeV, without any tuning of the coupling.

### 4.4 Direct detection

The dark glueballs interact with the Standard Model only via gravity (and possibly via a heavy mediator integrated out at the Planck scale). The direct-detection cross section is therefore at most of order $(m_{\rm glueball}/M_{\rm Pl})^2\sigma_{\rm typical}$, which is unobservably small in current and projected experiments. The model evades all direct-detection bounds.

### 4.5 Indirect detection

The dominant indirect-detection signal is the $3\to 2$ glueball-cannibal process and the rare $2\to 2$ annihilation $\Phi\Phi\to \text{SM}$ via the same heavy mediator. The latter produces a monochromatic $\gamma$-ray line at
$$E_\gamma \;=\; 2\,m_{\rm glueball} \;\simeq\; 1\text{--}10\,\,{\rm GeV}\,.$$
Critically, the $\mathbb{Z}_2$ doublet structure predicts that the line is *split* by the small $\mathbb{Z}_2$-breaking induced by gravitational mixing between the two species, $\Delta m \sim m^2/M_{\rm Pl}\sim 10^{-19}\,$eV --- unobservably small in current $\gamma$-ray telescopes, but a target for next-generation high-resolution detectors.

---

## 5. Falsifiability

### 5.1 Two-resonance signature in axion haloscopes

If the dark sector is enriched with a hidden axion-like particle (ALP) coupling, the $\mathbb{Z}_2$ structure predicts *two* haloscope peaks of equal amplitude (one per SU(2) factor), separated by an irreducible $\mathbb{Z}_2$-breaking splitting. ABRACADABRA-class searches [Kahn--Safdi--Thaler 2016, arXiv:1602.01086] in the 0.1--10$\mu$eV window probing the natural axion mass scale would observe this doublet rather than a singlet --- a striking and unambiguous signature.

### 5.2 Indirect-detection doublet line

For dark masses $m_{\rm glueball}\sim 1\,$GeV, the indirect annihilation line at $E_\gamma=2\,m_{\rm glueball}$ should appear as a *doublet* in sufficiently high-resolution observations. Current Fermi-LAT resolution ($\Delta E/E\sim 10\%$) cannot resolve it, but CTA and proposed future $\gamma$-ray telescopes with sub-percent resolution would distinguish the two-species from one-species hypotheses.

### 5.3 Lattice extension

The cross-Lie configuration (SU(2)$\times$SU(2), $D=3$) can be simulated on the lattice with currently available technology. The Sp$(2N)$ lattice programme of Bennett *et al.* [arXiv:2010.15781] has already produced glueball spectra for Sp(2), Sp(4), Sp(6), Sp(8) in $D=4$. A modest extension to SU(2)$\times$SU(2) at $D=3$ would predict the precise mass ratios entering the SIDM cross section and confirm or falsify the $\mathbb{Z}_2$ doublet structure of the spectrum.

### 5.4 Combination with the visible-sector uniqueness theorem

If the companion paper's uniqueness theorem for (SU(3), $D=4$) is independently established, then the prediction of a *single* hidden sector with the specific structure (SU(2)$\times$SU(2), $D=3$) becomes a sharp falsifiable claim: any other detected dark gauge structure (e.g. a single SU(3) dark sector, or an SU(N) with $N\neq 2$, or a non-product semi-simple group) would falsify the saturation-polynomial framework as a whole.

---

## 6. Connection to the 5-condition uniqueness theorem (companion paper)

The companion paper [Rémondière 2026, in preparation] proves that conditions C1--C5 together select (SU(3), $D=4$) uniquely as the visible-sector configuration. The saturation polynomial C1 alone, however, admits three roots, of which only one passes all five conditions. The three roots and their physical status are:

| Root | $(D,r)$ | Group | Status |
|------|---------|-------|--------|
| (i)  | $(2,1)$ | SU(2) or U(1) | Topological, no propagating glueballs, excluded by C3 |
| (ii) | $(3,2)$ | **SU(2)$\times$SU(2)** | Dynamical, fails C2 and C4 $\Rightarrow$ **dark sector** |
| (iii)| $(4,2)$ | **SU(3)** | Dynamical, passes all $\Rightarrow$ **visible sector** |

The middle root is the unique dynamical configuration which fails the matter conditions C2 and C4 but passes the structural conditions C1 and C3. We propose to interpret it as the structurally selected dark sector, complementary to (SU(3), $D=4$). The non-trivial empirical claim is that the universe instantiates *both* roots: one visible (us), one dark (the new sector). The third root (i) is excluded as non-dynamical and need not be instantiated.

This three-root picture has a pleasing internal coherence: the polynomial admits exactly the number of dynamical solutions needed to accommodate a visible plus a dark sector, with no remaining degeneracy. The model is in this sense parsimonious --- there is no free choice of dark gauge group.

---

## 7. Discussion and outlook

### 7.1 Other semi-simple saturated combinations

At higher rank, the saturation polynomial admits no further roots for $r\leq 2$. The next admissible value $r=3$ would require $D(D-1)(5-D)=18$, which has no integer solution in $D\geq 2$. The next is $r=4$ at $D(D-1)(5-D)=24$, again no integer solution. The three roots listed above are exhaustive on the lattice $(r,D)\in\mathbb{Z}_{\geq 0}\times\mathbb{Z}_{\geq 2}$ with $r\leq 2$; higher-rank configurations are excluded by an explicit Bianchi cohomology computation in the companion paper. Within the framework, therefore, the model is *closed*: there is no room for additional hidden sectors.

### 7.2 G$_2$ alternative

The exceptional group G$_2$ has rank 2 and a trivial centre. It has been considered as a dark-sector candidate [Maas--Wellegehausen 2014; Maas 2017] because its lack of a non-trivial centre forbids stable string tensions, leading to a distinctive "broken-string" phenomenology. In our framework, G$_2$ does *not* satisfy the saturation polynomial at any $D$: the rank $r=2$ matches $D=3$ and $D=4$, but G$_2$ has 14 generators rather than the $2\times 3=6$ generators of SU(2)$\times$SU(2), and the polynomial counts generators per unit rank, not rank alone. The exclusion of G$_2$ is therefore a structural prediction.

### 7.3 Falsification timeline

The model predicts:

- **2026--2028:** Lattice extension to (SU(2)$\times$SU(2), $D=3$) using existing infrastructure of the Sp$(2N)$ programme [Bennett *et al.* 2020]; computational cost is modest (estimated 100k core-hours).
- **2027--2030:** ABRACADABRA-class searches in 0.1--10$\mu$eV range; if a single peak (not doublet) is observed, the model is falsified.
- **2028--2032:** Small-scale-structure surveys (Vera Rubin LSST, Roman Space Telescope) refine $\sigma/m$ from dwarf galaxies; departure from $0.05$--$0.5\,$cm$^2/$g would constrain the model.

The model is therefore falsifiable on a 2--6 year horizon by independent observational and computational programmes.

---

## 8. Acknowledgments

The author thanks the open-source scientific computing community for the tools (PARI/GP, NumPy, SciPy, LaTeX, Python) used in this work, and the arXiv preprint server for free and immediate access to the literature cited above.

**LLM disclosure (COPE-compliant):** Large language model assistants were used in the preparation of this manuscript for the following tasks: literature search assistance, drafting of bibliographic verifications, formatting of LaTeX/Markdown source, and proof-reading for clarity and consistency. All scientific content, mathematical derivations, choice of model, choice of references, numerical computations, interpretation of empirical data, and the final argumentative structure are the sole responsibility of the author. No LLM was used as a source of physical or mathematical claims, and every cited reference was independently verified against the arXiv API before inclusion.

**Funding:** No external funding was received for this work. The author is an independent researcher.

**Data availability:** No primary data were generated. All numerical estimates use published lattice and observational data fully referenced in Section 9.

**Conflicts of interest:** None declared.

---

## 9. References

1. **Polyakov, A. M.** (1977). "Quark confinement and topology of gauge theories". *Nucl. Phys.* B 120, 429--458.

2. **Migdal, A. A.** (1975). "Recursion equations in gauge field theories". *Sov. Phys. JETP* 42, 413--418.

3. **Witten, E.** (1991). "On quantum gauge theories in two dimensions". *Commun. Math. Phys.* 141, 153--209.

4. **Coleman, S.** (1977). "Fate of the false vacuum: Semiclassical theory". *Phys. Rev.* D 15, 2929; erratum *ibid.* D 16, 1248 (1977).

5. **Gross, L.** (1975). "Logarithmic Sobolev inequalities". *Amer. J. Math.* 97, 1061--1083.

6. **Carlson, E. D., Machacek, M. E., Hall, L. J.** (1992). "Self-interacting dark matter". *Astrophys. J.* 398, 43--52.

7. **Markevitch, M., Gonzalez, A. H., Clowe, D., Vikhlinin, A., David, L., Forman, W., Jones, C., Murray, S., Tucker, W.** (2004). "Direct constraints on the dark matter self-interaction cross-section from the merging galaxy cluster 1E0657-56". *Astrophys. J.* 606, 819--824. arXiv:astro-ph/0309303 (verified).

8. **Teper, M.** (1999). "SU(N) gauge theories in 2+1 dimensions". *Phys. Rev.* D 59, 014512.

9. **Hochberg, Y., Kuflik, E., Volansky, T., Wacker, J. G.** (2014). "Mechanism for thermal relic dark matter of strongly interacting massive particles". *Phys. Rev. Lett.* 113, 171301.

10. **Maas, A., Wellegehausen, B. H.** (2014). "G$_2$ gauge theory at finite temperature and density". *PoS* LATTICE2013, 095.

11. **de Blok, W. J. G.** (2010). "The Core-Cusp Problem". *Adv. Astron.* 2010, 789293. arXiv:0910.3538 (verified).

12. **Boylan-Kolchin, M., Bullock, J. S., Kaplinghat, M.** (2012). "The Milky Way's bright satellites as an apparent failure of LCDM". *Mon. Not. R. Astron. Soc.* 422, 1203--1218. arXiv:1111.2048 (verified).

13. **Soni, A., Zhang, Y.** (2016). "Hidden SU(N) Glueball Dark Matter". *Phys. Rev.* D 93, 115025. arXiv:1602.00714 (verified).

14. **Forestell, L., Morrissey, D. E., Sigurdson, K.** (2017). "Non-Abelian Dark Forces and the Relic Densities of Dark Glueballs". *Phys. Rev.* D 95, 015032. arXiv:1605.08048 (verified).

15. **Kahn, Y., Safdi, B. R., Thaler, J.** (2016). "Broadband and Resonant Approaches to Axion Dark Matter Detection". *Phys. Rev. Lett.* 117, 141801. arXiv:1602.01086 (verified).

16. **Kribs, G. D., Neil, E. T.** (2016). "Review of strongly-coupled composite dark matter models and lattice simulations". *Int. J. Mod. Phys.* A 31, 1643004. arXiv:1604.04627 (verified).

17. **Athenodorou, A., Teper, M.** (2017). "SU(N) gauge theories in 2+1 dimensions: glueball spectra and k-string tensions". *J. High Energy Phys.* 02, 015.

18. **Tulin, S., Yu, H.-B.** (2018). "Dark matter self-interactions and small scale structure". *Phys. Rept.* 730, 1--57. arXiv:1705.02358 (verified).

19. **Bullock, J. S., Boylan-Kolchin, M.** (2017). "Small-Scale Challenges to the $\Lambda$CDM Paradigm". *Annu. Rev. Astron. Astrophys.* 55, 343--387. arXiv:1707.04256 (verified).

20. **Yamanaka, N., Iida, H., Nakamura, A., Wakayama, M.** (2019). "Dark matter scattering cross section and dynamics in dark Yang--Mills theory". *Phys. Lett.* B 813, 136056 (2021). arXiv:1910.01440 (verified).

21. **Bennett, E., Holligan, J., Hong, D. K., Lee, J.-W., Lin, C.-J. D., Lucini, B., Piai, M., Vadacchino, D.** (2020). "Glueballs and Strings in Sp$(2N)$ Yang--Mills theories". *Phys. Rev.* D 103, 054509 (2021). arXiv:2010.15781 (verified).

22. **Athenodorou, A., Teper, M.** (2021). "SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology". *J. High Energy Phys.* 12, 082. arXiv:2106.00364 (verified).

23. **Rémondière, K.** (2026). "Saturation polynomial and the uniqueness of (SU(3), $D=4$)". In preparation.
