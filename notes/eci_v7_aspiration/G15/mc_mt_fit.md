# Deliverable B — m_c/m_t structural ratio test

**Run:** `gate_g15.py` (Deliverable B section).
**PDG source:** PDG Particle Data Book 2024 RPP, https://pdg.lbl.gov/2024/.
Specifically: m_u(2 GeV, MS-bar) = 2.16 +0.49−0.26 MeV; m_c(2 GeV, MS-bar)
= 1.273 ± 0.0046 GeV; m_t(pole) = 172.69 ± 0.30 GeV. Tag:
**[PDG-2024-VALUES-CITED-NOT-VERIFIED]** — values stated from the standard
PDG running-mass table; cross-check against a fresh PDG copy before any
publication.

## B.1 — The G1 morning conjecture

The G1 morning sketch (`gate_g1_hatted.py`, line ≈ 580) postulated that the
up-quark Yukawa structure in an S'_4 model with Q ~ 3̂ and u^c ~ {1, 2̂}
gives, at the symmetric point τ → i∞:

> m_c/m_t = (β/α) · F(λ_3̂(p_*), λ_2̂(p_*))   where  F = λ_2̂(5)/λ_3̂(5) · (ρ/v)

This was tagged [CONJECTURED] in G1 with the explicit caveat
"numerical prefactors set in fit not done here."

## B.2 — Numerical evaluation at two reference primes

Using the G1.5-verified Hecke eigenvalues (5/5 primes p ≡ 1 mod 4):

| p* | λ_3̂(3)(p*) | λ_2̂(5)(p*) | naive ratio R(p*) = λ_2̂/λ_3̂ |
|---|---|---|---|
| 5  | 26   | 18   | **0.6923** |
| 13 | 170  | 178  | **1.0471** |
| 17 | 290  | −126 | −0.4345 |
| 29 | 842  | −1422 | −1.689 |
| 37 | 1370 | 530  | 0.3869 |

**Bombshell: R(p*) IS NOT PRIME-INDEPENDENT.** Five primes give five different
ratios (factor of ~5× variation, including sign changes).

## B.3 — Implication: the G1 morning conjecture is a FIT, not a derivation

If R(p*) varied by < 1%, we'd have a structural prediction independent of
which p* we chose. The 5× variation we measure says: the single-eigenvalue
ratio λ_2̂/λ_3̂ is NOT the right invariant.

The mathematical reason: 3̂(3) has Eisenstein eigenvalues λ(p) = 1 + p², which
grow polynomially with p. 2̂(5) has cuspidal eigenvalues that satisfy the
Deligne bound |a(p)| ≤ 2 p^{(k-1)/2} = 2 p² (same growth rate as the bound,
but with arbitrary sign). The ratio λ_2̂/λ_3̂ ≈ a_cuspidal(p)/(1 + p²) → 0 (or
oscillates) as p → ∞ generically, and is sharply prime-dependent at small p.

## B.4 — 1-parameter "fit" to PDG (for completeness)

If we IGNORE the prime-dependence and pick p* = 5 (the smallest prime in H₁),
we can fit one free parameter ξ ≡ ρ/v to match PDG:

  R(5) · ξ = m_c/m_t (PDG, μ = 2 GeV)
  0.6923 · ξ = 7.36×10⁻³
  ξ = **1.06×10⁻²**

This is in the NATURAL SUSY-breaking-scale-to-EW-VEV window (ξ in [10⁻², 10²]).
But it's a 0-DOF fit (1 parameter, 1 datum) and prime-arbitrary (ξ would be
0.70×10⁻² at p=13, which is also natural but inconsistent with ξ=1.06×10⁻²).

## B.5 — What a real prediction would look like

A genuine v7 prediction of m_c/m_t would require:
1. A specific S'_4 representation assignment for Q, u^c, d^c (e.g., from LYD20
   or dMVP26) that fixes the Clebsch-Gordan structure.
2. A specific value of τ (the "modulus VEV") chosen at a fixed point of the
   modular group — typically τ = i, τ = ω = e^{iπ/3}, or τ = i∞.
3. Computation of the full 3×3 mass matrix M_u(τ) including all CG-allowed
   terms in the Yukawa Lagrangian.
4. Diagonalization and extraction of mass ratios m_u/m_c, m_c/m_t.
5. **Bonus**: simultaneously fit lepton sector (m_e/m_μ, m_μ/m_τ) using the
   same modular structure → 2 params, 4 ratios = real over-determined test.

This is the work for G1.6 / Paper B (PRD 2027 Q1 in the v7 plan).

## B.6 — m_u/m_t cannot be predicted at this gate

PDG: m_u/m_t (2 GeV) ≈ 1.25×10⁻⁵.

Hatted multiplets at k = 3 are: 1̂'(3), 3̂(3), 3̂'(3). The singlet 1̂'(3) and
the second triplet 3̂'(3) have the SAME Hecke eigenvalues as 3̂(3) on
p ≡ 1 mod 4 (both are Eisenstein-class with λ(p) = 1 + p²; G1 sanity check
confirmed). So they cannot generate a third distinct mass scale.

The next genuinely independent modular form is at higher weight (k ≥ 7) or
in the doublet 2̂'(5) and quartet 4̂(5). These have not been built in G1 or
G1.5; they are the input to G1.6.

## Verdict (Deliverable B)

**At this gate, m_c/m_t is a 1-parameter FIT, not a structural derivation.**
The morning's structural ratio R = 18/26 = 0.692 is real but prime-dependent
(varies 0.39 ↔ 1.05 across {5, 13, 17, 29, 37}); using it as a prediction
requires arbitrary choice of reference prime. Any of the five would yield
a "natural" ξ ~ 10⁻², so the fit is unfalsifiable in this form.

The path to a real prediction is: build the full Clebsch-Gordan mass matrix
with a specified rep assignment (G1.6).
