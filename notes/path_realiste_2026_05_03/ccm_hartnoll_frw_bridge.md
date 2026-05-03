# CCM 2511.22755 + Hartnoll-Yang 2502.02661 vs FRW Type II_∞

**arXiv (curl, 2026-05-03):** 2511.22755v1 *Zeta Spectral Triples* (CCM, 2025-11-27); 2502.02661v2 *Conformal Primon Gas at the End of Time* (Hartnoll-Yang, 2025-02-04). Both verified.

## 1. Hartnoll-Yang result (verbatim, eq. 53)
ϕ(t_n)=0 on the xi zeros, with ϕ(t) ∝ ξ(1/2+it)/Γ-prefactors, dilation generator (eq. 37) **D ψ = i(x ∂_x + Δ ψ)**, Δ=1/2+iε, on L²(R_+, dx). Continuous Lebesgue spectrum on R; zeros = *absorption* spectrum, not eigenvalues.

## 2. CCM dilation generator (verbatim, eq. 5.14)
"**D^(λ)_log = −i u ∂/∂u** on L²([λ⁻¹,λ], du/u) with periodic boundary conditions." Spectrum {2πn/L : n∈Z}, L=2 log λ. Theorem 1.1: rank-one perturbation D^(λ,N)_log = D^(λ)_log − |D^(λ)_log ξ⟩⟨δ_N| → spectra → {γ_n}.

## 3. FRW dS dilation operator (Cor 3.7, derived)
a(η)=−1/(Hη). Sympy: a(λη)=a(η)/λ ⇒ background dilation **K_dil=−i η ∂_η**, formal twin of D^(λ)_log under η↔u. But *modular* generator K_FRW=U⁻¹ K_HL U with K_HL Möbius on Mink diamond; r=0: **K_HL ~ (π/2R)(R²−η²) ∂_η** — *quadratic* in η.

## 4. Comparison
| Operator | η-coefficient | degree |
|---|---|---|
| CCM D^(λ)_log | η | linear |
| dS background dilation | η | linear (matches CCM) |
| K_FRW = U⁻¹ K_HL U | (π/2R)(R²−η²) | quadratic (mismatch) |

Sympy: (R²−η²)/η = R²/η−η, η-dependent ⇒ no constant rescaling. Background dilation matches CCM trivially; **modular flow does not**.

## 5. Verdict — **IMPOSSIBLE (clean closure)**

(a) Modular generator quadratic, dilation linear ⇒ no unitary/scalar identification.
(b) CCM lives on a 1D number-theoretic scaling space; K_FRW on a 4D geometric vN algebra. Spec(K_FRW)=R continuous; {γ_n} discrete; Connes 1973 cocycle invariance blocks deformation.
(c) HY's BKL "end of time" is η→0, exactly the regime excluded by Cor 3.7 (η_f<0) and Question 4(b)–(c) of frw_note (Big Bang kills cyclic-separating Ω_FRW).

**Closure.** The Sonnet "substantive frontier" (B,F) refers to CCM/HY's *internal* RH program; the FRW bridge is blocked by the same obstruction as Piste 4. The Piste 4 NO-GO paragraph (line 375) already cites CCM 2511.22755 and is sharp. HY adds no attack vector (same continuous Lebesgue spectrum on R). **Do not open Piste 4-bis.**
