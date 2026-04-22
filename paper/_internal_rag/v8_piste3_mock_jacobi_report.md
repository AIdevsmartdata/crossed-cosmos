# v8_piste3_mock_jacobi_report.md

**Pre-registered falsifier:** V8-Piste3-MockJacobi (REGISTRY_FALSIFIERS.md)
**Date:** 2026-04-22
**Artefact:** `derivations/V8-piste3-mock-jacobi.py`
**PRINCIPLES rules enforced:** rule 1, rule 12, V6-1, V6-4

---

## Section 1 — Z(τ): Explicit Form

The horizon partition function for the NMC quintessence static patch with
coupling ξ_χ R χ²/2 (χ₀ = M_P/10) is constructed following CLPW 2023
(arXiv:2206.10780) for the gravitational crossed-product sector and
Jensen-Sorce-Speranza 2023 (arXiv:2306.01837) for the matter contribution.

**Gravitational sector** (Gibbons-Hawking Euclidean path integral on dS₄/S⁴):

    Z_grav(β) = exp(π / (G_N H²_eff))

where H_eff is determined self-consistently at slow-roll order by:

    3 M_P² H²_eff = V(χ₀) + ξ_χ R χ₀²/2 = V₀ exp(−αχ₀/M_P) + 6 ξ_χ H²_eff χ₀²

i.e. H²_eff = V₀ exp(−αχ₀/M_P) / (3M_P² − 6 ξ_χ χ₀²).

**Matter sector** (NMC scalar χ on S³ spatial sections of static patch):

    Z_matter(β) = ∏_{n,l,m} [ q^{E_{nlm}/(2H_eff)} / (1 − q^{E_{nlm}/H_eff}) ]

where q = exp(−β H_eff) and the eigenfrequencies are:

    E_{nlm}/H_eff = √[(n + l + 3/2)² + ν²]

    ν² = m²_eff / H²_eff − 9/4,   m²_eff = α²V₀/M_P² + 12 ξ_χ H²_eff

with degeneracy (2l+1) per mode. The full partition function at leading
slow-roll order is:

    Z(β) = exp(π/(G_N H²_eff)) × Z_matter(β)

**Modular parameter extension.** For BPS systems one sets τ = iβH_eff/(2π)
and extends τ to ℂ (Im τ > 0). This step is tested in Section 2.

---

## Section 2 — Holomorphy Test

**Is Z(τ) holomorphic in τ ∈ ℂ (Im τ > 0)?**

ANSWER: NO. Two independent obstructions, both fatal.

**Obstruction 1 — Irrational spectrum.**
The eigenfrequencies E_{nlm}/H_eff = √[(n+l+3/2)² + ν²] are irrational
in general: ν² = m²_eff/H²_eff − 9/4 is a sum of the slow-roll parameter
ratio α²V₀/(M_P² H²_eff) and the NMC term 12ξ_χ − 9/4. At fiducial
χ₀ = M_P/10, ξ_χ ~ 10⁻², α ~ 1, none of these combine to an integer square.

Consequence: the q-series Z_matter(q) = Σ_E d(E) q^E has exponents E
that are dense in ℝ₊, NOT the integer lattice required for a Jacobi/modular
q-series. The formal expression Z_matter(τ) = Σ_{n,l,m} ... exp(2πiτ·E/H_eff)
is NOT a Fourier series in τ with integer coefficients. It is not a
holomorphic function of τ in any standard sense.

**Obstruction 2 — Quasi-normal mode non-analyticity.**
The Lorentzian static patch has quasi-normal modes (QNMs) with complex
frequencies ω_QNM = ω_R − iΓ (Γ > 0 = decay rate). Under the Euclidean
continuation t → −iτ_E the damping becomes oscillatory; the analytic
continuation to complex τ introduces a non-holomorphic sector (anti-holomorphic
dependence on τ̄ from the imaginary part of ω). This anti-holomorphic sector
is NOT of Zwegers form (∂_τ̄ ĥ = shadow): it is simply real-time dissipation,
with no modular interpretation.

**Conclusion:** Z(τ) is not holomorphic. Mock Jacobi classification requires
holomorphy as a prerequisite. The test is FAILED at this stage.

---

## Section 3 — Modular Transformation Test

Holomorphy having failed, the modular test is formally moot. It is carried
out explicitly to confirm the conclusion and to prevent re-opening.

**τ → τ + 1 (T-transformation):**
Requires Z(τ+1) = χ Z(τ) for some phase χ (quasi-modularity). In β-language,
τ → τ+1 corresponds to β → β − 2πi/H_eff (complex temperature shift).
Z_grav is β-independent at leading order → trivially T-invariant.
Z_matter(q e^{2πi}) = Π_{n,l,m} [q e^{2πi}]^{E/H_eff} / (1 − [q e^{2πi}]^{E/H_eff}).
For this to equal χ Z_matter(q), we need exp(2πi E/H_eff) to be a root
of unity for all modes — i.e. E/H_eff ∈ ℤ/2 for all (n,l,m).
This requires ν ∈ ℤ/2, i.e. m²_eff = (k + 1/2)² H²_eff for some integer k.
This is a measure-zero condition not satisfied at χ₀ = M_P/10 generically.

**RESULT: T-invariance FAILS.**

**τ → −1/τ (S-transformation):**
Modular inversion β → 4π²/(β H²_eff). There is no known S-duality for the
dS₄ static patch. The Cardy formula (relevant for AdS₃/CFT₂) requires a
central charge and a 2D CFT; neither applies here. The Gibbons-Hawking
entropy S_dS = π/(G_N H²_eff) does not transform to itself under
β → 4π²/(β H²_eff) (it is β-independent, hence trivially S-invariant, but
this is not modular invariance — it simply means the leading semiclassical
gravity does not see the inverse temperature).

**RESULT: S-invariance FAILS (no modular group action).**

**Conclusion:** Z(τ) possesses no SL(2,ℤ) or Γ_0(N) transformation law.
Mock modular forms are defined by their transformation laws; without one,
the classification does not apply.

---

## Section 4 — Zwegers Shadow vs v6 GSL Term

Assume counterfactually that Z(τ) had a mock Jacobi decomposition:
Z(τ,z) = h(τ,z) + μ(τ,z) (mock part + Appell-Lerch). The Zwegers
completion reads:

    ĥ(τ,z) = h(τ,z) + ∫_{−τ̄}^{i∞} (z+τ)^{−k} S(z,z₀) dz

with shadow S of weight 2−k and ∂_τ̄ ĥ = (−2i)^{1−k} (Im τ)^{−k} S(−τ̄)*.

**The v6 GSL type-II violation term** (GROUND_TRUTH.md Part G):

    κ_R C_k [1 − Θ(PH_k[δn])]

has dimension [H_eff] (a rate), is linear in the Brown-Susskind complexity
C_k (dimensionless), and involves the PH_k activator Θ (dimensionless,
0/1-valued in the step-function limit).

**Dimensional mismatch:**
The Zwegers shadow S(τ) for k=1/2 mock theta functions is a holomorphic
modular form of weight 3/2 with dimensions of a counting generating function.
The shadow integral has schematic dimension [τ]^{1/2} in natural units.
No identification κ_R C_k (1−Θ) ~ shadow integral is dimensionally
consistent without introducing an ad-hoc dimensional constant not derivable
from the NMC quintessence action.

**Structural mismatch:**
The Zwegers shadow emerges from the POLAR (meromorphic in τ) part of Z,
physically arising from 2-centered BPS black holes and hypermultiplet
halos (D-M-Z §3). The v6 term κ_R C_k (1−Θ) arises from the modular
Hamiltonian commutator and PH_k filtration of the matter density field δn.
These are categorically different objects:
- Shadow: algebraic-geometric completion of a meromorphic Jacobi form
- κ_R C_k (1−Θ): thermodynamic rate × complexity × topology indicator

**Verdict:** NO MATCH. The structural mismatch is categorical, not a matter
of adjustable constants. Even if Z(τ) were a mock Jacobi form (which it is
not), its shadow would not reproduce the v6 GSL term.

---

## Section 5 — Universality Class Assessment

**D-M-Z 2012 prerequisite checklist:**

| Prerequisite | D-M-Z system | NMC quintessence dS₄ | Status |
|---|---|---|---|
| (a) UV framework | N=4 string on K3×T² | None assumed (or QG) | UNMATCHED |
| (b) BPS condition | Quarter-BPS dyons | Thermal dS₄ (T_H>0) | UNMATCHED |
| (c) Holomorphic Z | Yes (meromorphic Jacobi) | No (irrational spectrum) | UNMATCHED |
| (d) AdS₃ throat | 2-centered attractor | S⁴ Euclidean dS₄ | UNMATCHED |

Score: 0/4 prerequisites satisfied.

The NMC quintessence horizon is thermal (T_H = H_eff/2π), non-BPS, non-SUSY,
and governed by the de Sitter group SO(4,1) rather than the SL(2,ℤ) modular
group relevant to the torus T². The universality class mismatch is complete.

**Related literature (not mock Jacobi):**
- Anninos-Harlow-Maloney 2013 (arXiv:1207.3204): dS partition functions
  studied as matrix integrals (no mock Jacobi structure found).
- Dong-Silverstein-Torroba 2018 (arXiv:1811.07965): inflation as dS string
  theory (no mock Jacobi claim).
No extension of D-M-Z to thermal dS₄ exists in the accessible literature.

**Literature verification note (PRINCIPLES rule 1):** arXiv:1208.4074 is
the Dabholkar-Murthy-Zagier "Quantum Black Holes, Wall Crossing, and Mock
Modular Forms" paper. Its theorem is stated for N=4 string theory on K3×T².
This is consistent with the pre-registration description and with the
obstruction identified here. Zwegers 2002 PhD thesis introduces mock theta
completions for indefinite theta series; the physical application is to
BPS state counting, not thermal dS₄.

---

## Verdict

**FAILURE / NOT-APPLICABLE**

Four independent fatal obstructions identified:

1. Z(τ) for NMC quintessence dS₄ is NOT holomorphic in τ (irrational
   spectrum + QNM non-analyticity). Mock Jacobi classification requires
   holomorphy as prerequisite. ← PRIMARY BLOCKER.

2. No modular group action: τ→τ+1 fails (irrational spectrum);
   τ→−1/τ fails (no self-dual dS geometry). Without SL(2,ℤ) action,
   there is no mock modular form.

3. Wrong universality class: D-M-Z 2012 applies to N=4 SUSY BPS counting;
   NMC quintessence dS₄ satisfies 0/4 prerequisites.

4. No structural or dimensional match between Zwegers shadow and
   v6 GSL violation term κ_R C_k (1−Θ).

Decision per registry threshold: **FAILURE**.

---

## Proposed F-19 Entry for FAILED.md

### F-19 — Mock Jacobi form for NMC quintessence horizon Z(τ)

**Date.** 2026-04-22.

**Proposed.** The horizon partition function Z(τ) = Tr_{A_R} e^{−β H_R}
for the NMC quintessence static patch (ξ_χ R χ²/2, χ₀ = M_P/10) admits a
mock Jacobi decomposition à la Dabholkar-Murthy-Zagier 2012 (arXiv:1208.4074),
and the Zwegers harmonic completion reproduces (up to known constants) the
v6 GSL type-II violation term κ_R C_k (1−Θ).

**Why it failed.** Four fatal obstructions:
(1) Non-holomorphy: eigenspectrum of H_χ on S³ has irrational frequencies
    ν² = m²_eff/H²_eff − 9/4 ∉ ℤ; QNM damping also breaks holomorphy.
    Z(τ) is not a meromorphic Jacobi form.
(2) No modular group action: τ→τ+1 and τ→−1/τ both fail. No SL(2,ℤ)
    orbit, hence no mock modular classification.
(3) Wrong universality class: D-M-Z requires N=4 SUSY BPS dyons on K3×T²;
    dS₄ NMC quintessence satisfies 0/4 prerequisites.
(4) Categorical mismatch: Zwegers shadow (meromorphic polar completion)
    is structurally and dimensionally incompatible with κ_R C_k (1−Θ)
    (modular-Hamiltonian rate × complexity × PH_k indicator).

**Artefacts.** `derivations/V8-piste3-mock-jacobi.py`,
`paper/_internal_rag/v8_piste3_mock_jacobi_report.md`.

**Re-open conditions.** Extension to BPS sectors of a string-theoretic
NMC embedding where χ arises as a compactification modulus with a BPS
attractor (e.g. type-IIB or N=2 matter sector, Dark Dimension scenario).
Requires: (a) proof that χ is a BPS object in the UV completion;
(b) explicit construction of a holomorphic Jacobi form from the string
partition function; (c) identification of the mock part's shadow with
a physical entropy-rate observable. This is a multi-paper research program,
not achievable in a single derivation session.
