# FRW Non-Stationary Crossed-Product Classification: Attack Plan
**Date:** 2026-05-02
**Author:** ECI sub-agent (Sonnet 4.6), arXiv-verified
**Status:** Open question confirmed. No prior resolution found.
**Commissioned context:** ECI v6.0.13 footnote; open math.OA question flagged in §sec:limits.

---

## Section 1: Literature Verification

### 1.1 Confirmed baseline papers (all verified via arXiv API or arxiv.org HTML)

| arXiv ID | Authors | Title (shortened) | Verified? | Covers non-stationary FRW? |
|---|---|---|---|---|
| 2206.10780 | Chandrasekaran–Longo–Penington–Witten | An Algebra of Observables for de Sitter Space | YES | No. de Sitter static patch only; Killing-stationary. |
| 2406.01669 | Kudler-Flam–Leutheusser–Satishchandran | Algebraic Observational Cosmology | YES | No. FLRW with inflationary (asymptotically de Sitter) past only; asymptotically Killing. |
| 2406.02116 | Chen–Penington | A clock is just a way to tell the time | YES | No. Slow-roll inflation + evaporating Schwarzschild-de Sitter; specific cases with physical clock. |
| 2405.00847 | Faulkner–Speranza | Gravitational algebras and the generalized second law | YES | No. Killing horizons explicitly required. |
| 2601.07910 | Klinger–Kudler-Flam–Satishchandran | Generalized Entropy is von Neumann Entropy II | YES (arxiv.org) | No. Stationary black holes and de Sitter static patch. |
| 2601.07915 | Chandrasekaran–Flanagan | Subregion algebras in classical and quantum gravity | YES | No. Null surfaces and Killing horizons; non-stationary linearized perturbations of Killing horizons only (not cosmological). |

### 1.2 Search evidence that the question is unresolved

The following arXiv API and full-text searches were conducted on 2026-05-02 using User-Agent `ECI-frw-attack/1.0`. All returned zero relevant results:

- `abs:"crossed product" AND abs:"FRW"` — 0 results
- `abs:"crossed product" AND abs:"Friedmann"` — 0 results
- `abs:"modular automorphism" AND abs:"FRW"` — 0 results
- `abs:"von Neumann algebra" AND abs:"radiation dominated"` — 0 results
- `abs:"von Neumann algebra" AND abs:"matter dominated"` — 0 results
- `abs:"gravitational algebra" AND abs:"FLRW"` — 0 results
- `abs:"observable algebra" AND abs:"cosmological" AND abs:"type II"` — 0 results
- `cat:math.OA AND abs:"Friedmann"` — 0 results
- `ti:FRW AND ti:"crossed product"` — 0 results
- arxiv.org full-text searches for "FRW crossed product modular von Neumann", "Friedmann Robertson Walker crossed product type II algebra", "FLRW von Neumann algebra type", "FLRW modular flow algebra" — 0 results each

One adjacent paper was found: Gomez (arXiv:2407.20671, July 2024, verified) treats inflationary cosmology via type III_1 factors and flow of integrable weights, but addresses de Sitter and slow-roll inflation, not radiation- or matter-dominated FRW.

Additional post-2024-08 papers by key authors (Kudler-Flam, Satishchandran) verified via arxiv.org HTML: arXiv:2510.06376 (baby universes/AdS-CFT), arXiv:2510.01556 (stringy algebras/AdS), arXiv:2505.14771 (no-boundary state/JT gravity) — none address non-stationary FRW.

**Verdict:** As of 2026-05-02, no paper has classified `A(O) ⋊_σ ℝ` for a comoving observer in radiation- or matter-dominated FRW. The question is open.

---

## Section 2: Technical Attack Plan

### 2.1 Choose a concrete background

We fix **radiation-dominated FRW** in conformal time η:

```
ds² = a(η)² (−dη² + dχ² + χ² dΩ²),    a(η) = a₀ η,    η > 0.
```

This is the simplest case with no Killing vector along a generic comoving worldline (the background admits spatial translations and rotations but no timelike Killing field). Matter-dominated (a(η) ∝ η²) is the secondary target; it shares the structural features but with a softer conformal factor.

### 2.2 Define the local algebra A(O)

Let O be a comoving observer with worldline χ = 0 in the above coordinates. The causal diamond D(O, τ₁, τ₂) centered on O between proper times τ₁, τ₂ defines a region of Minkowski-like size set by the conformal time interval. The local algebra is:

```
A(O) := π_Ω(A_loc(D(O)))''  ⊆ B(H),
```

where A_loc is the net of local algebras for a free QFT (scalar field φ, mass m ≥ 0) in the FRW background, π_Ω is the GNS representation of the preferred vacuum state Ω (conformal vacuum in radiation domination), and the double commutant '' is the von Neumann closure. Standard Haag-Kastler axioms apply in the conformal frame since radiation-dominated FRW is conformally flat and the conformally coupled scalar is unitarily equivalent to flat Minkowski QFT restricted to the conformal diamond.

For the analysis, we additionally include a single gravitational degree of freedom (a quantum clock variable p_t conjugate to the Hamiltonian H, following CLPW 2022 / arXiv:2206.10780) to dress the algebra. The extended algebra is:

```
A_ext(O) = A(O) ⊗ L^∞(ℝ),    [p_t, H] = iℏ,
```

and the physical algebra after imposing the constraint H_tot |phys⟩ = 0 is the crossed product

```
A(O) ⋊_σ ℝ,
```

where σ_τ is the Tomita–Takesaki modular automorphism of A(O) with respect to the state Ω.

### 2.3 The core difficulty: σ_τ is not a geometric flow

In the de Sitter static patch (CLPW 2022), the modular automorphism σ_τ of the Bunch–Davies vacuum restricted to the static patch coincides (by a theorem of Bisognano-Wichmann type) with the boost (Killing) flow, which is a bona fide geometric symmetry. This identification is the key step that makes the Connes–Takesaki analysis tractable.

In radiation-dominated FRW with comoving observer O, there is no Killing vector field that generates the flow on D(O). The Tomita–Takesaki modular automorphism σ_τ of A(O) with respect to the conformal vacuum Ω exists abstractly (by Tomita–Takesaki theory), but is NOT geometrically implementable as a diffeomorphism of the spacetime.

This makes the problem harder but also technically cleaner: one must work directly with the abstract Connes spectral theory of crossed products, without relying on the geometric crutch.

### 2.4 Reduction to spectral classification

By Connes–Takesaki duality (the fundamental theorem of the Connes invariant theory), the type of M = A(O) ⋊_σ ℝ is determined by the **Connes spectrum** Γ(σ) ⊆ ℝ:

- If Γ(σ) = {0}: M is type I (ruled out for local QFT algebras by standard results).
- If Γ(σ) = ℝ: M is type II_∞ (the CLPW result for de Sitter; the hoped-for outcome here).
- If Γ(σ) = λ^ℤ for some λ ∈ (0,1): M is type III_λ.
- If Γ(σ) = {0} ∪ {λ^n} (hybrid): type III_0 or more exotic.

The Connes spectrum Γ(σ) is the intersection over all σ-invariant projections e ≠ 0 of the Arveson spectrum Sp(σ_e), where σ_e = σ|_{eMe}. For local algebras in conformal QFTs, standard results (Buchholz–Wichmann, Guido–Longo) suggest that local algebras on diamonds in conformally flat spacetimes are type III_1 (full Connes spectrum = ℝ). However, the *crossed product* M = A(O) ⋊_σ ℝ is generically type II_∞ precisely when Γ(σ) = ℝ — but the question is whether the gravitational dressing by the clock degree of freedom stabilizes this or introduces a gap.

### 2.5 The radiation-dominated conformal trick

The conformally coupled massless scalar in radiation-dominated FRW with a(η) = a₀ η satisfies the same equation as in flat Minkowski space (the conformal anomaly vanishes for the conformally coupled scalar in 3+1 dimensions). This means:

- The vacuum state Ω on A(O) is unitarily equivalent (via the conformal map) to the Minkowski vacuum on a conformally transformed diamond.
- The modular automorphism σ_τ of the Rindler-type algebra in the conformal Minkowski frame IS the Lorentz boost (Bisognano-Wichmann theorem).
- Pulling back: σ_τ for A(O) in FRW equals the Bisognano-Wichmann boost in the conformal frame, but conjugated by the conformal factor a(η). This conjugation introduces a time-dependent rescaling that **does not** correspond to any geometric symmetry of the original FRW spacetime.

The precise form of the pullback modular automorphism is the first concrete computation the attack must perform. Working hypothesis: σ_τ has continuous spectrum on ℝ (arising from the conformal rescaling), which would imply Γ(σ) = ℝ and hence M is type II_∞. But the coupling to the conformal factor a(η) = a₀ η introduces a non-trivial weight that might instead produce a discrete component.

---

## Section 3: Three Sub-Results for a Publishable Paper

### Sub-result (a): Explicit modular automorphism for the radiation-dominated FRW patch

**Target:** Derive σ_τ for A(O) explicitly in conformal time coordinates, using the conformal equivalence of radiation-dominated FRW to flat Minkowski space (for conformally coupled scalar, m = 0).

**Method:** Apply the Bisognano-Wichmann theorem in the conformal frame, then pull back via the conformal factor a(η) = a₀ η. The key computation is the Jacobian of the conformal map on the causal diamond and its action on the modular Hamiltonian K_O = −log Δ_Ω, where Δ_Ω is the Tomita–Takesaki modular operator.

**Expected output:** An explicit operator formula K_O = K_BW + δK_{conf}, where K_BW is the Bisognano-Wichmann boost generator and δK_{conf} is a correction term depending on a(η).

**Comparison with de Sitter:** For de Sitter, σ_τ = geometric boost = Killing flow. For radiation FRW, σ_τ = conformal pullback of boost = Killing flow + conformal correction. The correction term is the key novelty.

### Sub-result (b): Spectrum classification of M = A(O) ⋊_σ ℝ

**Target:** Determine whether M is type II_∞ or type III_λ.

**Method:** Compute Γ(σ) by analyzing the Arveson spectrum of σ on A(O). Use the Bisognano-Wichmann decomposition from (a). The conformal correction δK_{conf} introduces a time-dependent weight; analyze whether this weight is integrable (favors type II_∞) or produces discrete spectral gaps (favors type III_λ).

**Key lemma to prove or refute:** The conformal correction δK_{conf} = (d/dτ) log a(η(τ)) · G, where G is a local operator (the stress-energy trace), is a bounded perturbation of K_BW in an appropriate operator topology. If true, the spectral theory of K_BW (continuous spectrum ℝ) is preserved and M is type II_∞.

**Comparison with de Sitter:** CLPW 2022 (arXiv:2206.10780, verified) proves M_{dS} = type II_∞ via Killing stationarity. This paper would prove (or refute) that M_{FRW-rad} is also type II_∞ via the conformal trick — a structural result that does not require stationarity.

**Fallback:** If the conformal correction is not bounded (possible if a(η) → 0 as η → 0, i.e., at the Big Bang singularity), the result may be type III. This would be a genuinely new finding: a cosmological background where gravitational algebra is type III rather than type II, with implications for whether entropy is well-defined for early-universe observers.

### Sub-result (c): Structural comparison with stationary cases

**Target:** Identify precisely what algebraic properties are preserved and what is lost when passing from stationary (Killing) backgrounds to the radiation-dominated FRW case.

**Content:**
1. Table of algebra types: de Sitter (type II_1 [CLPW 2022 verified]), de Sitter static patch ⋊ ℝ (type II_∞ [CLPW 2022 verified]), Schwarzschild exterior (type II_∞ [CLPW 2022 context]), radiation-dominated FRW (this paper: type II_∞ or type III, to be determined).
2. Theorem: For conformally flat FRW backgrounds with a conformal boundary, the crossed-product type is determined by the integrability of the conformal weight function ω(τ) = (d/dτ) log a(η(τ)) along the observer's worldline.
3. Corollary: A necessary condition for type II_∞ is that ∫ |ω(τ)|² dτ < ∞ along the worldline (or a weaker L^p condition to be determined). This is satisfied in radiation-dominated FRW (where ω ∝ 1/η → ∞ as η → 0, but is integrable near η → ∞) and may fail near the Big Bang singularity.

---

## Section 4: Proposed Timeline (3–6 months toward a 20-page paper)

### Month 1 (May 2026): Setup and conformal reduction

- Write out the conformal map D(O) → D_Mink(O) in detail for radiation-dominated FRW with a(η) = a₀ η.
- Verify that the conformally coupled scalar algebra A(O) in FRW is unitarily equivalent to the corresponding flat-space algebra. Check whether this extends to massive fields (it does not; the conformal trick is exact only for m = 0, conformally coupled).
- Compute the pullback of the Bisognano-Wichmann modular Hamiltonian: derive K_O = K_BW + δK_{conf} explicitly.
- Deliverable: internal technical note (5 pages) with all conventions fixed and the modular Hamiltonian written down.

### Month 2 (June 2026): Arveson spectrum analysis

- Analyze the Arveson spectrum Sp(σ) for the pulled-back modular automorphism. Focus on whether δK_{conf} is a Hilbert-Schmidt or trace-class perturbation.
- If the perturbation is bounded: apply stability theorems for the Connes spectrum under bounded perturbations (check Connes 1973, Takesaki Vol. II [unverified — classic references, not arXiv]). Conclude type II_∞.
- If unbounded near η → 0: analyze the behavior of A(O) near the Big Bang (possibly with a UV cutoff / adiabatic regularization). This may require restricting to the causal diamond avoiding η = 0.
- Deliverable: proof sketch or explicit counterexample for the type II_∞ claim.

### Month 3 (July 2026): Write up sub-result (a) and (b) + extension to massive fields

- Write Sections 1–3 of the paper (introduction, modular automorphism, spectrum classification).
- Test whether sub-result (b) extends to m > 0 (massive scalar) or non-conformally-coupled scalar. The conformal trick fails here; this will require a separate analysis using KMS states and Radzikowski propagators [unverified terminology — standard AQFT on curved spacetime].
- Deliverable: draft Sections 1–3 (~12 pages).

### Month 4 (August 2026): Sub-result (c) and matter-dominated FRW

- Extend to matter-dominated FRW (a(η) = a₀ η²). The conformal trick still applies for the conformally coupled scalar, but the conformal weight ω(τ) = (d/dτ) log a(η(τ)) behaves differently.
- Write the comparison table (sub-result c) and prove the integrability criterion.
- Deliverable: draft Section 4 + comparison section (~5 pages).

### Month 5 (September 2026): Internal review and extension

- Internal review of full 20-page draft.
- Consider whether the result extends to any FRW background (general a(η)): the criterion should be expressible purely in terms of the Hubble parameter H(t) = ȧ/a.
- Check whether the result is consistent with Gomez (arXiv:2407.20671, verified) on inflationary cosmology type III_1 factors: the Gomez result applies to de Sitter before the crossed-product step; our result is post-crossed-product, so no contradiction is expected, but the relationship should be stated.
- Deliverable: complete first draft (20 pages).

### Month 6 (October 2026): Submission preparation

- Prepare arXiv preprint.
- Submission to primary target journal (see Section 4 below).
- Post to math.OA and hep-th on arXiv.
- Circulate to Kudler-Flam–Satishchandran group for feedback (their 2406.01669 is the closest predecessor).

---

## Section 5: Target Journal

Three options, in order of preference:

1. **Communications in Mathematical Physics (Comm. Math. Phys., Springer):** The natural home for a result at the interface of operator algebras and mathematical physics. Previous papers in the CLPW tradition (Longo, Faulkner-Speranza) have appeared here or in similar journals. Expected review time: 6–9 months. Impact: high within math-phys community. Appropriate length: 20–35 pages.

2. **Letters in Mathematical Physics (Lett. Math. Phys., Springer):** If sub-results (a) and (b) are obtained but (c) requires more work, a 12–15 page letter is viable. Faster review. Appropriate if the main result is a clean type II_∞ theorem for radiation-dominated FRW without extensions.

3. **Journal of Functional Analysis (JFA, Elsevier):** If the primary contribution is the operator-algebraic spectral analysis (the Connes spectrum computation and integrability criterion) with the physics interpretation as secondary, JFA is appropriate. Stronger audience in the math.OA community; less visibility to physicists.

Avoid hep-th journals (JHEP, Phys. Rev. D) as primary targets: the result is a math.OA theorem and will receive stronger review in math-phys venues. arXiv cross-listing to hep-th is appropriate.

---

## Appendix: Search Log (2026-05-02)

All searches conducted via `https://export.arxiv.org/api/query` with `User-Agent: ECI-frw-attack/1.0` and via `https://arxiv.org/search/` (HTML), on 2026-05-02.

| Query | Results |
|---|---|
| `abs:"crossed product" AND abs:"FRW"` | 0 |
| `abs:"crossed product" AND abs:"Friedmann"` | 0 |
| `abs:"modular automorphism" AND abs:"FRW"` | 0 |
| `abs:"von Neumann algebra" AND abs:"radiation dominated"` | 0 |
| `abs:"von Neumann algebra" AND abs:"matter dominated"` | 0 |
| `abs:"gravitational algebra" AND abs:"FLRW"` | 0 |
| `abs:"observable algebra" AND abs:"cosmological" AND abs:"type II"` | 0 |
| `cat:math.OA AND abs:"Friedmann"` | 0 |
| `ti:FRW AND ti:"crossed product"` | 0 |
| `abs:"non-stationary" AND abs:"crossed product" AND abs:"type II"` | 1 result: arXiv:2601.07915 (Chandrasekaran-Flanagan, non-stationary Killing horizon perturbations — not cosmological FRW) |
| `abs:"crossed product" AND abs:"cosmological" AND abs:"modular"` | 1 result: arXiv:2407.20671 (Gomez, inflationary/de Sitter — not radiation/matter FRW) |
| arxiv.org full text: "FLRW von Neumann algebra type" | 0 |
| arxiv.org full text: "FRW crossed product modular von Neumann" | 0 |
| arxiv.org full text: "Friedmann Robertson Walker crossed product type II algebra" | 0 |
| arxiv.org full text: "FLRW modular flow algebra" | 0 |
| arxiv.org: "cosmological observer algebra type II non-stationary" | 1 result: arXiv:2601.07910 (Klinger-Kudler-Flam-Satishchandran, de Sitter static patch — not FRW) |

**Total candidate papers requiring abstract-level checking:** 3 (arXiv:2601.07915, 2407.20671, 2601.07910). All three confirmed via direct arxiv.org abstract pages to address stationary or asymptotically stationary backgrounds only.

**Conclusion:** The question is open as of 2026-05-02.
