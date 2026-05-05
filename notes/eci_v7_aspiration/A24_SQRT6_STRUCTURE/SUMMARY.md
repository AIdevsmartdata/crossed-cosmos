# A24 — √6 vs Q(i) Chowla–Selberg periods

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A24 (parent persisted)
**Hallu count entering / leaving:** 78 / 78 (held; pure numerical, no refs added)

## Verdict

**PSLQ EXHAUSTED.** √6 is **Galois-rational**, not period-anchored. A14's CSD(1+√6) Q(i)-anchoring at τ=i is **combinatorial** (S-fixed point), NOT period-theoretic.

**Implication for v7.4 + DUNE 2030 falsifier:** No upgrade to A14's "~20% weak deep" assessment. The δ_CP ≈ −87° prediction remains empirically anchored, not promoted to deep CM identity.

## A14's flagged candidate is FALSE

`2·θ_2(i)²·θ_3(i)²/θ_4(i)⁴` evaluates to **2^{3/2} = 2√2 ≈ 2.828427**, NOT √6 ≈ 2.449490. Closed-form residual 0.0 at dps=60. Reason: at τ=i, θ_2=θ_4 (verified to 5×10⁻⁶²) so the expression collapses to 2θ_3²/θ_2² = 2/√λ(i) = 2/√(1/2) = 2^{3/2} (Gauss lemniscatic λ(i)=1/2). The Δ to √6 is 0.378937 — gross mismatch, not subtle.

## High-precision values (60 digits)

- √6 = 2.449489742783178098197284074705891391965947480656670128
- Γ(1/4) = 3.625609908221908311930685155867672002995167682880065467
- Ω_K = Γ(1/4)²/(2√(2π)) = 2.622057554292119810464839589891119413682754951431623163
- θ_2(i) = θ_4(i) = 0.913579138156116821407242593401222089701963916393469033
- θ_3(i) = 1.086434811213308014575316121510223457070205707245218886 = π^{1/4}/Γ(3/4) ✓
- η(i) = Γ(1/4)/(2π^{3/4}) ✓; θ_2θ_3θ_4 = 2η³ ✓ (all cross-checks <10⁻⁶¹)

## PSLQ search results (tol 10⁻⁵⁰)

| Basis | Result | Reading |
|---|---|---|
| B1 linear (√6,Γ(1/4),π,log2,Ω_K), \|c\|≤500 | **none** | √6 not Q-linear in periods |
| B2 log basis +Ω_K | [0,4,−1,−3,−2] | recovers Chowla–Selberg Ω_K²=Γ(1/4)⁴/(8π); coeff on log√6 = 0 |
| B3 (+log 3) | [2,0,0,−1,−1] | trivial 2log√6 = log2+log3 |
| B4 drop log3 | **none** | √6 PSLQ-independent of {Γ(1/4),π,2} |
| B5 (log√6, log θ_2,3, log2,π) | [0,4,−4,1,0] | recovers λ(i)=1/2; coeff on log√6 = 0 |
| B6 (+log η) | [0,0,−2,2,0,1] | Jacobi 2η²=θ_3²; coeff on log√6 = 0 |
| B7 linear 8 elts, \|c\|≤1000 | **none** | — |

In **every** non-trivial relation found, the coefficient on log√6 is zero.

## Interpretation for ECI v7 / A14 / DUNE 2030 falsifier

**√6 is Galois-rational, not period-anchored.** It enters CSD(1+√6) as the discriminant √(b²−4c) of the 2×2 secular polynomial of Y₃^(2)(i) eigenvalues, not via Chowla–Selberg. The Q(i)-anchoring of τ=i is *combinatorial* (S-fixed point), not *period-theoretic*. **No upgrade to A14's "~20% weak deep" assessment.** A14's open question (√6 ↔ Γ(1/4) ratios) is **CLOSED in the negative** at dps=60, |c|≤500. DUNE 2030 δ_CP≈−87° falsifier remains empirically anchored, no extra structural support gained.

## Future probes

- Q(√−24)/Q(√−6) period rings (which contain √6 natively)
- τ=i+ε holomorphic deformation of Σm_ν

## Files

- `/root/crossed-cosmos/notes/eci_v7_aspiration/A24_SQRT6_STRUCTURE/sqrt6_pslq.py` — mpmath dps=60, ~3s runtime
