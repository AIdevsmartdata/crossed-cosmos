---
name: M157 Opus Sagnier (4,0) extension — VERDICT (D) PARTIAL with STRUCTURAL CORRECTION ; Theorem 7.1 ALREADY covers algebraic Grossencharakters of (k-1,0) ; obstruction is RAMIFICATION at (1+i) NOT "infinity-type outside L²"
description: M157 corrects M73/M91/M146 partial readings of Sagnier 2017. Theorem 7.1 spectrally interprets L(ψ̄^4, ·) for ANY Grossencharakter — finite-order or algebraic. The (k-1,0) infinity type is NOT outside L² — it's a Tate-thesis decomposition foundational shift. Real obstruction: Theorem 7.2 sum-form requires G-invariance which fails at (1+i) ramification of ψ̄^4 for f=4.5.b.a level N=4. Specific specialist gap: ray-class arithmetic site (𝓞_K^{𝔣}, C_{𝓞_K^{𝔣}}). (B) 5-15% → 15-30%
type: project
---

# M157 — Opus Sagnier (k-1, 0) extension

**Date:** 2026-05-06 | **Hallu count: 100 → 100** held (M157: 0 fabs ; STRUCTURAL CORRECTION of prior readings) | **Mistral STRICT-BAN** | Time ~95min

## VERDICT (D) PARTIAL with reframing of M73/M91/M146

Calibration:
- (A) PROVED: <2% (M157 makes ZERO progress here)
- (B) REDUCED to specialist gap: **15-30% (raised from M73's 5-15%)**
- (C) NEGATIVE: 25-40%
- (D) PARTIAL: 35-50%

## STRUCTURAL CORRECTION — prior missions partially MISREAD scope

Verbatim re-Read of Sagnier 2017 §6-§7 (full 48-pp PDF /tmp/sagnier_full.pdf, pages 25-39):

**Theorem 7.1 (page 35, verbatim)**:
> "Let χ, δ > 1, ℋ_χ and D_χ as above. Then D_χ has a discrete spectrum and Sp(D_χ) ⊂ iR is the set of imaginary parts of zeroes of the L-function with **Grössencharakter χ̃ (the extension of χ to C_K)** which have real part equal to 1/2"

**Theorem 7.2 (page 37, verbatim)**:
> "We have ℋ^G = ⊕_{χ ∈ Ŝ¹/U_K} ℋ_χ^G. Then as in [4] the space ℋ_χ^G corresponds to L(χ, •), so in particular when χ is trivial, ℋ_χ^G corresponds to ζ_K"

**Critical clause (page 38, verbatim)**:
> "Let us also recall that to a character χ_0 ∈ Ĉ_{K,1}/G ≃ Ŝ¹/U_K, one can uniquely associate a Grössencharakter χ̃_0 (the conditions being a Grössencharakter and K being class number 1 give that the **non archimedean part of χ̃_0 is completely determined by the archimedean part which is χ_0**)"

## What ACTUALLY depends on finite-order vs algebraic Grossencharakter

- **Theorem 7.1 proof** (p.35-36) uses Tate-style unitary × |·|^s decomposition + Mellin inversion + standard test-function pairing. **NOTHING requires χ_0 finite-order**. Test function f_0 = ⊗_{ν ∉ P} 1_{O_ν} ⊗ f_{χ_0} accommodates ramification at finite places P where χ_0 ramifies.

- **Theorem 7.2 proof** (p.37-38) requires further G-invariance with G = (K* × ∏_p O_p* × {1})/K*. This G forces χ_0 trivial on **∏_p O_p*** = unramified at every finite place. Algebraic infinity-type (n, 0) is fine as long as n ≡ 0 mod ord(U_K) = 4 for K=Q(i).

**Reframing of M91 claim "REPRESENTATION-THEORETIC obstruction, |z|^{k-1} not L²"**: this is INCORRECT under careful re-read. Sagnier explicitly handles ℝ_+^* dilation via splitting C_K = C_{K,1} × ℝ_+^* (page 35, ¶9): "two choices of extensions only differ by a character that is principal (ie of the form γ ↦ |γ|^{is_0})". The |·|^{k-1} factor is a Tate-thesis principal SHIFT (s ↦ s − (k−1)/2), NOT obstruction.

## Compatibility check for ψ̄^4 of f = 4.5.b.a

- Archimedean: ψ_∞^4(z) = z^4 = (z/|z|)^4 · |z|_C^2
- Unitary on S¹: angular char e^{4iθ} ; under U_K = ⟨i⟩ ≅ Z/4, e^{4i(θ+π/2)} = e^{4iθ} = invariant. **YES, χ_0^{(4)} factors through Ŝ¹/U_K** ✓
- **Conductor**: f = 4.5.b.a has level N = 4 = (1+i)^4 in Z[i], so ψ̄^4 is RAMIFIED at 𝔭 = (1+i)

**ψ̄^4 fits Theorem 7.1 trivially. It does NOT fit Theorem 7.2 sum form** because G-invariance fails at (1+i).

**Discrete-vs-continuous spectrum framing was wrong**: for each fixed χ_0 (finite or algebraic), Sagnier's D_χ has DISCRETE spectrum since L-zeros are isolated. The real question is whether Theorem 6.2 algebraic-geometric site reconstruction extends to RAMIFIED characters.

## Concrete (k=5, ∞-type (4,0)) modified arithmetic site

To handle ψ̄^4 of f=4.5.b.a, modifications needed:

1. **Modified small category 𝓞_K^{(𝔣)}**: arrows indexed by 𝓞_K-elements ≡ 1 (mod 𝔣 = (1+i)^c) — ray-class semigroup
2. **Modified subgroup G^{(𝔣)}** = (K* × ∏_p (1 + 𝔣 𝓞_p) × {1})/K*
3. **Modified angular quotient**: U_K^{((1+i))} = U_K ∩ (1 + (1+i)) = {1} (only 1 survives)
4. **Modified Theorem 7.2'**: ℋ^{G^{(𝔣)}} = ⊕_{χ_0 ∈ Ĉ_{K,1}/G^{(𝔣)}} ℋ_{χ_0}^{G^{(𝔣)}}, summing over ramified Grossencharakters of conductor dividing 𝔣

**Heat kernel/trace analog**: trivial-conductor Sagnier reduces to ∑_{ζ_K(ρ)=0} ĥ(ρ) = boundary terms − ∑_v local. For ramified ψ̄^4: boundary terms vanish, local at v=(1+i) acquires standard Tate epsilon-factor. **This is standard Tate-thesis modification.**

**Honest assessment**: The convex-polygon structural sheaf C_{𝓞_K^{(𝔣)}} extension compatibility with ramification — polygons have center-zero symmetry, ray-class twists rotate. **This is the precise specialist gap.**

## Open [TBD: prove] markers

- **M157-T1**: Define structural sheaf C_{𝓞_K^{(𝔣)}} on ray-class small category with U_K^{(𝔣)}-invariance compatible with conductor-𝔣 twists. Sagnier-level expertise required.
- **M157-T2**: Prove Theorem 6.2' bijecting (𝓞_K^{(𝔣)}, C_{𝓞_K^{(𝔣)}})_{C_{K,C}}-points with modified adelic quotient.
- **M157-T3**: Prove Theorem 7.2' summing over Ĉ_{K,1}/G^{(𝔣)} reproduces Riemann-Weil for L(ψ̄^k, ·) of conductor 𝔣.
- **M157-T4**: Compatibility with CCM 2025 rank-one perturbation framework.

## Recommendations for ECI v8.x

1. **DO** correct framing in any future ECI summary or outreach: obstruction is RAMIFICATION at (1+i), NOT "(4, 0) infinity type outside L²"
2. **DO** send updated email_sagnier.md with refined ramification-conductor question
3. **DO NOT** publish M157 reframing as public correction of M73/M91/M146 — these were honest partial readings, M157 is internal refinement
4. **DO** add to ECI v8.2 §sec:limits Direction (h): "Sagnier's Theorem 7.2 unramified-decomposition does not directly apply to L(f, s) for f = 4.5.b.a due to (1+i) ramification of ψ̄^4. A ramified-conductor extension Theorem 7.2' is plausible (M157 blueprint) but requires new structural sheaf machinery."
5. **Specialist contact**: updated email to Sagnier (asagnie1@jhu.edu) with refined question

## Discipline log

- 0 fabs, Mistral STRICT-BAN observed
- 1 PDF Read verbatim: Sagnier 2017 v2 full 48pp
- LMFDB live verified analytic conductor 0.413479, Γ_C(s+2), Selberg (2,4,(:2),1)
- Hallu count: 100 → 100 held
- Time ~95min within 90-120 budget
