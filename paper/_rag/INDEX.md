# RAG Source Cache — Crossed Cosmos (eci.tex)

Primary-source cache for editing agents working on Dark Dimension, Swampland, NMC-PPN,
DESI DR2 covariance, crossed-product dS, persistent homology, and thawing-quintessence
claims in `paper/eci.tex`.

**Rule for editors**: before writing or revising any factual/numerical claim in these
domains, open the relevant `_rag/<SHORTKEY>.txt` and quote from the verbatim text
rather than from memory. If a number/bound you want to cite does not appear in the
cached text, either grep a larger context window in the `.txt` file or flag the claim.

**Fetched 2026-04-21 from arXiv** (User-Agent: `crossed-cosmos-rag/1.0`). PDFs are
git-ignored; extracted `.txt` (via `pdftotext -layout`) is committed.

## Shortkey → arXiv ID map

```
Montero2022              2205.12293
AAL2023                  2306.16491
AAL2025                  2501.11690      (user-provided 2501.00960 was WRONG ID; refetched)
Bedroya2025DS            2507.03090
Bedroya2025              2503.19898      (NOTE: this arXiv is actually Pan–Ye; V1 attribution confusion confirmed)
OoguriVafa2007           hep-th/0605264
OOSV2018                 1806.08362
BedroyaVafa2019          1909.11063
Chiba1999                gr-qc/9903094
BEFPS2000                gr-qc/0001066
Faraoni2000              gr-qc/0008028   (NOTE: this arXiv is Bento–Lemos "helicity-1 instabilities", NOT the Faraoni NMC paper — user ID likely wrong)
PettorinoBaccigalupi2008 0802.1086
Faraoni2004              gr-qc/0404078
DESIDR2                  2503.14738
DEF1993PRL               —               (PRL 70, 2220; no arXiv; UNAVAILABLE)
DEF1996PRD               gr-qc/9602056
Poulin2019               1811.04083
PoulinSmith2026          2505.08051
CLPW2023                 2206.10780
DEHK2025a                2412.15502
DEHK2025b                2503.14454
CryptoCensorship         2402.03425
Yip2024                  2403.13985
Matsubara2003            astro-ph/0305472  UNAVAILABLE (user-provided ID is a different paper on ionised gas halos, Rossa & Dettmar 2003; correct Matsubara Minkowski-functionals arXiv ID not located)
ScherrerSen2008          0712.3450
Wolf2025                 2504.07679
Ye2025                   2407.15832
PanYe2026                2503.19898      (same PDF as Bedroya2025; symlinked copy)
```

---

## Entries

### Montero2022 — arXiv:2205.12293
**File**: `_rag/Montero2022.txt`
**Why**: Foundational Dark Dimension paper. Used in eci.tex wherever we cite the micron-scale extra dimension l ~ Λ^{-1/4}, the species scale M̂ ~ Λ^{1/12} M_Pl^{2/3} ~ 10^9–10^10 GeV, and the Higgs/neutrino predictions of the scenario.
**Key passage** (verbatim):
```
using the Distance/Duality conjecture and the smallness of dark energy, we predict
the existence of a light tower of states and a unique extra mesoscopic dimension of length
l ∼ Λ^{-1/4} ∼ 10^{-6} m, with extra massless fermions propagating on it. ...
Another prediction of the scenario is a species scale
M̂ ∼ Λ^{1/12} M_pl^{2/3} ∼ 10^9 − 10^10 GeV , corresponding to the higher-dimensional Planck scale.
```
**Equation/bound referenced in our paper**: §3.6 Dark-Dimension/Swampland cross-check; species-scale and l~Λ^{-1/4} estimates.

---

### AAL2023 — arXiv:2306.16491
**File**: `_rag/AAL2023.txt`
**Why**: Provides the neutrino-mass upper bound inside the dark-dimension scenario used as a cosmological consistency check.
**Key passage**:
```
neutrino Kaluza-Klein (KK) towers compensate for the graviton tower to maintain stable
de Sitter (dS) vacua ... the first KK neutrino mode is too heavy to alter the shape of the
radion potential or the required maximum mass for the lightest neutrino to carry dS rather
than AdS vacua found in the absence of the dark dimension, m_{1,max} ≲ 7.63 meV. We also
show that a very light gravitino (with mass in the meV range) could help relax the neutrino
mass constraint m_{1,max} ≲ 50 meV.
```
**Equation/bound referenced in our paper**: §3.6 neutrino-mass comparison to Σm_ν bounds.

---

### AAL2025 — arXiv:2501.11690 ("Two Micron-Size Dark Dimensions")
**File**: `_rag/AAL2025.txt`
**Why**: Two-extra-dimension refinement addressing both gauge and cosmological hierarchy. Use when discussing alternative dark-dimension geometries.
**Key passage** (title+authorship confirmed; see full txt for opening sections):
```
Two Micron-Size Dark Dimensions
Luis A. Anchordoqui, Ignatios Antoniadis, and Dieter Lüst
MPP-2025-5, LMU-ASC 02/25
```
**Equation/bound referenced in our paper**: §3.6 alternative geometry caveat (cite with care — user's original ID 2501.00960 was wrong; refetched with correct ID).

---

### Bedroya2025DS — arXiv:2507.03090
**File**: `_rag/Bedroya2025DS.txt`
**Why**: Evolving dark sector in dark-dimension scenario. Gives the exponential potential / dark-matter-mass parametrisation V = V_0 exp(-cφ), m_DM = m_0 exp(-c'φ) used when coupling Dark Dimension to w_0-w_a evolution.
**Key passage**:
```
We consider the natural possibility that the radius of the dark dimension varies as the
dark energy decreases, leading to the variation of the dark matter mass. ... A simple
realization of this idea for small range of ϕ is adequately captured by choosing a
potential which is locally of the form V = V_0 exp(−cϕ) and dark matter mass
m_DM = m_0 exp(−c'ϕ) where the sign of ϕ is chosen such that c' ≥ 0 while we have two
choices for the sign of c ... by either c ≥ 0, c' ≥ 0 or c ≤ 0, c' ≥ 0.
```
**Equation/bound referenced in our paper**: §3.6 evolving dark-sector cross-check with w_0-w_a DESI fit.

---

### Bedroya2025 — arXiv:2503.19898 (ATTRIBUTION WARNING: actually Pan & Ye)
**File**: `_rag/Bedroya2025.txt`
**Why**: eci.bib key `Bedroya2025` points at 2503.19898 which is Pan & Ye "Non-minimally coupled gravity constraints from DESI DR2 data" — NOT a Bedroya paper. The V1 attribution flag in the task spec is correct; either rename the bibkey or move the citation to `PanYe2026`.
**Key passage**:
```
We analyzed DESI DR2 BAO together with CMB and Type Ia supernova data to constrain
non-minimal coupling of gravity in the effective field theory (EFT) approach. Using a
non-parametric method to infer the EFT functions, we found that with DESI BAO, DESY5 SN,
and Planck CMB data the signal for non-minimal coupling reaches ∼3σ. ... current data
can constrain up to the quadratic order (n = 2) ...
```
**Equation/bound referenced in our paper**: §3.6 / §3.5 — 3σ NMC-hint quoted for DESI DR2 should cite PanYe2026 (same PDF).

---

### OoguriVafa2007 — arXiv:hep-th/0605264
**File**: `_rag/OoguriVafa2007.txt`
**Why**: Original Swampland Distance Conjecture — tower of states at infinite distance in moduli space, exp(-α·Δφ) mass decay. Cited wherever we invoke the distance conjecture / tower scale.
**Key passage**:
```
moduli spaces with finite non-zero diameter belong to the swampland. We also conjecture
that points at infinity in a moduli space correspond to points where an infinite tower
of massless states appear, and that near these regions the moduli space is negatively
curved. ... These conjectures put strong constraints on inflaton potentials that can
appear in a consistent quantum theory of gravity.
```
**Equation/bound referenced in our paper**: Distance-conjecture discussion (§3.6); underlies the dark-dimension deduction.

---

### OOSV2018 — arXiv:1806.08362
**File**: `_rag/OOSV2018.txt`
**Why**: de Sitter swampland conjecture |∇V| ≥ c·V; forbids stable dS.
**Key passage**:
```
we propose a swampland criterion in the form of |∇V| ≥ c · V for a scalar potential V
of any consistent theory of quantum gravity, with a positive constant c. In particular,
this bound forbids dS vacua.
```
**Equation/bound referenced in our paper**: §3.6 Swampland cross — dS conjecture bound c=O(1).

---

### BedroyaVafa2019 — arXiv:1909.11063
**File**: `_rag/BedroyaVafa2019.txt`
**Why**: Trans-Planckian Censorship Conjecture; gives sharper bound |V'|/V ≥ 2/√(d-2) asymptotically.
**Key passage**:
```
we propose a new Swampland condition, the Trans-Planckian Censorship Conjecture (TCC),
based on the idea that in a consistent quantum theory of gravity sub-Planckian quantum
fluctuations should remain quantum and never become larger than the Hubble horizon ...
applied to the case of cosmologies driven only by a scalar field, the TCC imposes an
upper bound of 2/√(d − 2) on the asymptotic value of |V'|/V ... the TCC forbids long-lived
meta-stable dS spaces, but allows sufficiently short-lived ones.
```
**Equation/bound referenced in our paper**: §3.6 TCC cross-check.

---

### Chiba1999 — arXiv:gr-qc/9903094
**File**: `_rag/Chiba1999.txt`
**Why**: First derivation of the NMC solar-system bound |ξ| ≲ 10^{-2}. Canonical reference for the PPN constraint on non-minimal quintessence.
**Key passage**:
```
the solar system experiments put a constraint on the non-minimal coupling: |ξ| ≲ 10^{-2}.
S = ∫ d^4x √−g [ −ξφ^2 R − (1/2) g^{ab} ∂_a φ ∂_b φ − V(φ) ] + S_m
The effective gravitational "constant" is defined by κ^2_eff ≡ κ^2 (1 − ξ κ^2 φ^2)^{-1}.
ξ is the non-minimal coupling between the scalar field and the curvature. In our
conventions, ξ = 1/6 corresponds to conformal coupling.
```
**Equation/bound referenced in our paper**: NMC-PPN bound |ξ| ≲ 10^{-2}, Cassini comparison (§3.5, A5 appendix).

---

### BEFPS2000 — arXiv:gr-qc/0001066
**File**: `_rag/BEFPS2000.txt`
**Why**: Boisseau-Esposito-Farèse-Polarski-Starobinsky reconstruction program for scalar-tensor quintessence from H(z) and δ_m(z). Needed wherever we mention F(φ)R reconstruction.
**Key passage**:
```
Reconstruction of a scalar-tensor theory of gravity modeled in the scope of a
scalar-tensor theory of gravity. We show that it is possible to determine ... Our
results generalize those obtained in GR ... and constrain any attempt to explain a
varying Λ-term using scalar-tensor theories of gravity. Good data on δ_m(z) expected to
appear soon from observations of clustering and abundance of different objects at
redshifts ∼ 1 and more, as well as from weak gravitational lensing, together with better
data on D_L(z) from more supernova events, will allow implementation of the
reconstruction program ...
```
**Equation/bound referenced in our paper**: §3.5 DEF/BEFPS reconstruction machinery.

---

### Faraoni2000 — arXiv:gr-qc/0008028 (WARNING: content does not match cite)
**File**: `_rag/Faraoni2000.txt`
**Why**: The arXiv ID gr-qc/0008028 is **Bento & Lemos, "Instability of helicity-1 gravitational-matter modes"** — not a Faraoni NMC paper. If eci.tex cites `Faraoni2000` for a non-minimal coupling / PPN claim, the bibkey or arXiv ID is wrong. Flag for correction.
**Key passage** (of what we actually fetched):
```
Abstract: It is shown that the interaction of helicity-1 waves of gravity and matter in
a thin slab configuration produces new types of instabilities. ... this mode is unstable
above a critical wavelength, λ_c = √(πc^2/2Gρ). This should be compared with Jeans
wavelength ...
```
**Equation/bound referenced in our paper**: UNCLEAR — editor MUST locate the intended Faraoni reference (likely Faraoni 2000 "Inflation and quintessence with nonminimal coupling", arXiv:gr-qc/0006091) before citing.

---

### PettorinoBaccigalupi2008 — arXiv:0802.1086
**File**: `_rag/PettorinoBaccigalupi2008.txt`
**Why**: Coupled vs Extended Quintessence; Jordan-frame scalar-tensor action; reference for EQ linear perturbation growth.
**Key passage**:
```
Coupled and Extended Quintessence: theoretical differences and structure formation
...In the Jordan frame, a scalar tensor theory in which EQ holds is in general described
by the following action ... CQ models [enhance clustering] with respect to the
corresponding Quintessence ones where the coupling is absent and to ΛCDM, structures in
EQ models may grow slower.
```
**Equation/bound referenced in our paper**: §3.5 Extended-Quintessence Jordan-frame action and growth.

---

### Faraoni2004 — arXiv:gr-qc/0404078
**File**: `_rag/Faraoni2004.txt`
**Why**: Phantom / nonminimally-coupled scalar dynamical systems. Reference for ξ=1/6 conformal coupling as IR fixed point.
**Key passage**:
```
ξ = 1/6. In fact, this value of the coupling constant is an infrared fixed point of the
renormalization group equations ... for a nonminimally coupled scalar field: oscillating
solutions for ξ > 0 ... and non-oscillating ones for ξ < 0 ...
φ̈ + 3Hφ̇ − m^2 φ − ξRφ = 0 .
```
**Equation/bound referenced in our paper**: Appendix A5 — conformal-coupling ξ=1/6 and KG with ξR coupling.

---

### DESIDR2 — arXiv:2503.14738
**File**: `_rag/DESIDR2.txt`
**Why**: DR2 BAO measurements, 2.3σ tension with flat ΛCDM in BAO-only, w_0-w_a preferred over ΛCDM at 3.1σ (BAO+CMB) up to 4.2σ with SNe, Σm_ν bounds.
**Key passage**:
```
[BAO] parameters preferred by BAO are in mild, 2.3σ tension ... and w_a < 0. This
solution is preferred over ΛCDM at 3.1σ for the combination of DESI BAO [+CMB]; over
ΛCDM ranges from 2.8 − 4.2σ depending on which SNe sample is used.
Σm_ν < 0.064 eV assuming ΛCDM and Σm_ν < 0.16 eV in the w_0 w_a model.
```
**Equation/bound referenced in our paper**: §3.5 / §3.6 DESI w_0-w_a significance, Σm_ν limits. The full PDF (12 MB) contains the covariance matrices — large file, grep inside `.txt` for specific tables.

---

### DEF1993PRL — Phys. Rev. Lett. 70, 2220 (1993) — UNAVAILABLE
**File**: —
**Why**: Damour–Esposito-Farèse "Nonperturbative strong-field effects in tensor-scalar theories of gravitation". No arXiv (pre-arXiv PRL). Access via DOI 10.1103/PhysRevLett.70.2220 (paywalled). Editors needing the spontaneous-scalarization claim should cite DEF1996PRD (arXiv:gr-qc/9602056) which contains the full framework.

---

### DEF1996PRD — arXiv:gr-qc/9602056
**File**: `_rag/DEF1996PRD.txt`
**Why**: Damour–Esposito-Farèse tensor-scalar PRD paper. "Spontaneous scalarization" form factors, binary-pulsar constraints vs solar-system; standard reference for scalar-tensor framework and strong-field deviations.
**Key passage**:
```
Some recently discovered nonperturbative strong-field effects in tensor–scalar theories
of gravitation are interpreted as a scalar analog of ferromagnetism: "spontaneous
scalarization". ... nonperturbative scalar field effects are already very tightly
constrained by published data on three binary-pulsar systems. We contrast the probing
power of pulsar experiments with that of solar-system ones by plotting the regions they
exclude in a generic two-dimensional plane of tensor–scalar theories.
```
**Equation/bound referenced in our paper**: A5 / §3.5 scalar-tensor framework; γ_PPN-1 expressed via α_0^2.

---

### Poulin2019 — arXiv:1811.04083
**File**: `_rag/Poulin2019.txt`
**Why**: Seminal EDE-resolves-H0 paper. Two concrete EDE models (oscillating scalar, slow-roll scalar). Needed for §3.6 H0-tension discussion.
**Key passage**:
```
Early dark energy (EDE) that behaves like a cosmological constant at early times
(redshifts z ≳ 3000) and then dilutes away like radiation or faster at later times can
solve the Hubble tension. In these models, the sound horizon at decoupling is reduced
resulting in a larger value of the Hubble parameter H_0 inferred from the cosmic
microwave background (CMB). We consider two physical models for this EDE, one involving
an oscillating scalar field and another a slowly-rolling field.
```
**Equation/bound referenced in our paper**: §3.6 EDE reference.

---

### PoulinSmith2026 — arXiv:2505.08051
**File**: `_rag/PoulinSmith2026.txt`
**Why**: Up-to-date EDE status after ACT DR6 + DESI DR2. Residual SH0ES tension ~2σ.
**Key passage**:
```
While ACT DR6 does not favor EDE over the core cosmological model ΛCDM, it allows for a
significantly larger maximum contribution of EDE, f_EDE, in the pre-recombination era
than the latest analysis of Planck NPIPE ... EDE rises the value of H_0 r_s, improving
consistency between CMB and DESI DR2 data. We find a residual tension with SH0ES of
∼2σ for the combination of Planck at ℓ < 1000 + ACT DR6 ...
```
**Equation/bound referenced in our paper**: §3.6 EDE-after-DR6-DR2 status.

---

### CLPW2023 — arXiv:2206.10780
**File**: `_rag/CLPW2023.txt`
**Why**: Chandrasekaran-Longo Penna-Witten crossed-product construction for the dS static patch. Type II_1 algebra, generalised entropy S_gen = A/(4G_N) + S_out.
**Key passage**:
```
We describe an algebra of observables for a static patch in de Sitter space, with
operators gravitationally dressed to the worldline of an observer. The algebra is a
von Neumann algebra of Type II_1. There is a natural notion of entropy for a state of
such an algebra. There is a maximum entropy state, which corresponds to empty de Sitter
space, and the entropy of any semiclassical state of the Type II_1 algebras agrees, up
to an additive constant independent of the state, with the expected generalized entropy
S_gen = (A/4G_N) + S_out.
```
**Equation/bound referenced in our paper**: Crossed-product / dS entropy formula.

---

### DEHK2025a — arXiv:2412.15502
**File**: `_rag/DEHK2025a.txt`
**Why**: Observer-dependent gravitational entropy via perspective-neutral QRFs; multiple-observer crossed product. Background for A4/A5 appendix on observer algebras.
**Key passage**:
```
Using the perspective-neutral QRF formalism, we extend previous constructions to allow
for arbitrarily many observers, each carrying a clock with possibly degenerate energy
spectra. We consider a semiclassical regime ... At leading order the von Neumann
entropy still reduces to the generalised entropy, but linear corrections are typically
non-vanishing and quantify the degree of entanglement between the clocks and fields.
```
**Equation/bound referenced in our paper**: Crossed-product/QRF appendix.

---

### DEHK2025b — arXiv:2503.14454
**File**: `_rag/DEHK2025b.txt`
**Why**: ACT DR6 extended-cosmology constraints. Needed whenever we quote ACT-DR6 bounds on EDE/MG/PMF.
**Key passage**:
```
The Atacama Cosmology Telescope: DR6 Constraints on Extended Cosmological Models
... use measurements from the Atacama Cosmology Telescope (ACT) Data Release 6 (DR6) to
test foundational assumptions of the standard cosmological model, ΛCDM, and set
constraints on extensions to it ... In fits to models invoking early dark energy,
primordial magnetic fields, or [modified recombination], primary CMB are not favored
over ΛCDM by our data.
```
**Equation/bound referenced in our paper**: §3.6 ACT DR6 cross-check.

---

### CryptoCensorship — arXiv:2402.03425
**File**: `_rag/CryptoCensorship.txt`
**Why**: Engelhardt-Folkestad-Levine-Verheijden-Yang "Cryptographic Censorship". Pseudorandomness ⇒ event horizon; quantum cosmic-censorship stride.
**Key passage**:
```
We first prove "Cryptographic Censorship": a theorem showing that when the time
evolution operator of a holographic CFT is approximately pseudorandom (or Haar random)
on some code subspace, then there must be an event horizon in the corresponding bulk
dual. ... we separate singularities into classical, semi-Planckian, and Planckian types
... classical and semi-Planckian singularities are compatible with approximately
pseudorandom CFT time evolution; thus, if such singularities are indeed approximately
pseudorandom, by Cryptographic Censorship, they cannot exist in the absence of event
horizons.
```
**Equation/bound referenced in our paper**: Censorship / holography references.

---

### Yip2024 — arXiv:2403.13985
**File**: `_rag/Yip2024.txt`
**Why**: Persistent-homology Fisher forecast; 13–50% tighter constraints on 8/10 parameters vs P+B. Key citation for topological-data-analysis motivation.
**Key passage**:
```
Persistent homology naturally addresses the multi-scale topological characteristics of
the large-scale structure as a distribution of clusters, loops, and voids. We apply
this tool to the dark matter halo catalogs from the Quijote simulations, and build a
summary statistic for comparison with the joint power spectrum and bispectrum statistic
... Through a Fisher analysis, we find that constraints from persistent homology are
tighter for 8 out of the 10 parameters by margins of 13 − 50%.
```
**Equation/bound referenced in our paper**: §3 persistent-homology motivation.

---

### Matsubara2003 — UNAVAILABLE
**File**: —
**Why**: The user-provided arXiv ID `astro-ph/0305472` resolves to Rossa & Dettmar (extraplanar diffuse ionised gas survey), NOT to Matsubara's Minkowski-functionals paper. The correct arXiv ID for Matsubara's 2003 Minkowski/genus paper was not located; editors should manually verify the intended reference (candidates: Matsubara 1996 astro-ph/9501055 or Matsubara 2003 in ApJ 584, 1-33 — check eci.bib `Matsubara2003` year/journal and re-search).

---

### ScherrerSen2008 — arXiv:0712.3450
**File**: `_rag/ScherrerSen2008.txt`
**Why**: Thawing-quintessence slow-roll formula for w(a). Foundation for our thawing-quintessence cross-check.
**Key passage**:
```
The thawing quintessence model with a nearly flat potential provides a natural mechanism
to produce an equation of state parameter, w, close to −1 today. ... the potential
satisfies the slow roll conditions: [(1/V)(dV/dφ)]^2 ≪ 1 and (1/V)(d^2V/dφ^2) ≪ 1 ... in
this limit, all such models converge to a unique relation between 1 + w, Ω_φ, and the
initial value of (1/V)(dV/dφ). We derive this relation, and use it to determine the
corresponding expression for w(a) ... For redshift z ≲ 1, w(a) is well-fit by the
Chevallier-Polarski-Linder parametrization, in which w(a) is a linear function of a.
```
**Equation/bound referenced in our paper**: Scherrer-Sen w(a) formula; thawing fit.

---

### Wolf2025 — arXiv:2504.07679
**File**: `_rag/Wolf2025.txt`
**Why**: Bayesian evidence for non-minimal coupling from DESI-era data; Bayes factor log(B) = 7.34 ± 0.6.
**Key passage**:
```
We find that, if the accelerated expansion is driven by quintessence, the data favour a
potential energy V(φ) that is concave, i.e., m^2 = d^2V/dφ^2 < 0. Furthermore, and more
significantly, the data strongly favour a scalar field that is non-minimally coupled to
gravity (Bayes factor log(B) = 7.34 ± 0.6), leading to time variations in the
gravitational constant on cosmological scales, and the existence of fifth forces on
smaller scales. The fact that we do not observe such fifth forces implies that either
new physics must come into play on non-cosmological scales or that quintessence is an
unlikely explanation for the observed cosmic acceleration.
```
**Equation/bound referenced in our paper**: §3.5 NMC Bayes-factor quote.

---

### Ye2025 — arXiv:2407.15832
**File**: `_rag/Ye2025.txt`
**Why**: "Hints of Nonminimally Coupled Gravity in DESI 2024 BAO" — original DESI-DR1 NMC hint, phantom crossing.
**Key passage**:
```
We find that the DESI data can rule out quintessence dark energy by indicating a
crossing of the phantom divide at z ≲ 1. ... the DESI result as the first hint of
modified gravity. Based on these insights, we propose the thawing gravity model to
explain the nonminimal coupling and phantom crossing indicated by observation, which
also fits better to DESI BAO, CMB and type Ia Supernovae data than ΛCDM.
```
**Equation/bound referenced in our paper**: §3.5 phantom-crossing hint.

---

### PanYe2026 — arXiv:2503.19898
**File**: `_rag/PanYe2026.txt` (copy of `Bedroya2025.txt` — same PDF)
**Why**: Pan & Ye NMC DESI DR2 follow-up to Ye2025. The 3σ NMC signal at quadratic EFT order is the claim our §3.5 cites.
**Key passage**: (see Bedroya2025 entry above — identical content)
```
with DESI BAO, DESY5 SN, and Planck CMB data the signal for non-minimal coupling
reaches ∼3σ. It is found that current data can constrain up to the quadratic order
(n = 2) ... Ω_EFT(a) = Σ_{i=0}^n c_i^EFT Ω_DE(a)^i.
```
**Equation/bound referenced in our paper**: §3.5 NMC 3σ DESI DR2 hint; this is the correct bibkey to use — NOT Bedroya2025.
