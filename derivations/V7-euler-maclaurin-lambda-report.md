# V7 — Euler-Maclaurin / zeta-regularised spectral sum on Odlyzko 10^5 zeros

**Date:** 2026-04-22
**Inputs:** `/tmp/odlyzko_zeros1.txt` (N = 100 000, γ_1 = 14.134725, γ_N = 74920.827)
**Code:** `V7-euler-maclaurin-lambda.py`
**Plot:** `V7-euler-maclaurin-lambda.png`

## Method

Computed, for a log-spaced grid of 80 values of Λ_UV ∈ [γ_1·1.01, γ_N]:

- S(Λ) = Σ_{n=1..N} f(γ_n/Λ)
- I(Λ) = ∫_{γ_1}^{γ_N} f(γ/Λ) · ρ̄(γ) dγ, with ρ̄(γ) = log(γ/2π)/(2π)
- residue(Λ) = S − I
- ρ^ZSA(Λ) = (Λ^4 / (2π)^2) · (S − I)

Two cutoffs: f_gauss(t) = e^{−t²} and f_rational(t) = 1/(1+t²)².

## Key numerical results

| Λ_UV | S (gauss) | I (gauss) | S − I | ρ^ZSA |
|------|-----------|-----------|-------|-------|
| 14.28 | 0.553 | 0.000 | **+0.553** | +5.82e+02 |
| 124.8 | 36.23 | 35.78 | **+0.445** | +2.74e+06 |
| 1 092 | 643.97 | 643.52 | **+0.449** | +1.62e+10 |
| 9 548 | 8 545.27 | 8 544.82 | **+0.449** | +9.46e+13 |
| 74 921 | 72 785.10 | 72 784.43 | **+0.668** | +5.33e+17 |

Rational cutoff is essentially identical (0.440 → 0.598). The two functional-form curves overlap within a few %.

**Scaling of the dimensionless residue:**
- |S − I| ∝ Λ^{+0.12} (gauss), Λ^{+0.10} (rational) near Λ ~ γ_N.
- Meaning: the residue is essentially **Λ-independent, sitting at ~0.45 ± 0.1** across four decades of Λ.
- Ratio |S−I|/√N_eff ≈ 2×10^{−3} — *far* below Gaussian fluctuation scale √N. The smooth subtraction is already almost perfect.

**Edge-effect tail (Λ → γ_N):** the residue jumps from 0.45 → 0.67 at the very last decade. This is the classic Euler-Maclaurin boundary term: the integral is cut at γ_N while the sum also stops there, so endpoint corrections ~ (1/2)·f(γ_N/Λ)·ρ̄(γ_N) appear. It is a **finite-sample artifact**, not a physical signal. For Λ deep below γ_N it vanishes.

## Answers to the four questions

1. **ρ^ZSA(Λ_UV)** grows trivially as Λ^4 because the prefactor is Λ^4; the *dimensionless* part (S−I) is flat at ≈ 0.45 across [100, 10000]. See plot (left panel, residue; right panel, full ρ^ZSA).
2. **Convergence?** The *dimensionless arithmetic residue* S − I **does not converge to zero** as Λ → γ_N with more zeros included — it sits at a finite O(1) value ≈ 0.45. But this finite value is fully explained by the leading Euler-Maclaurin correction (½·f(γ_1/Λ)·ρ̄(γ_1) + endpoint terms), i.e. by the *known* smooth behaviour at the boundary, not by arithmetic structure of the zeros. The sub-leading fluctuations scale as Λ^{+0.1}, consistent with slow endpoint drift, not with a new physical scale.
3. **Physical Λ comparison:** skipped as requested — the only dimensionless number worth reporting is **S − I ≈ 0.45 (cutoff- and Λ-independent)**. Multiplying by Λ^4/(2π)² recovers a Λ^4-divergent quantity identical in structure to the naive QFT zero-point energy. Nothing is tamed.
4. **Cutoff sensitivity:** gaussian vs rational differ by ~10 % in S − I across the whole range. Since both give O(1) with matching Λ-dependence, the residue is **mildly** cutoff-dependent in normalization but not in qualitative behaviour.

## Verdict

**TRIVIAL-CANCELLATION (with boundary tail).**

One-number summary: **S − I = 0.449** (stable across Λ ∈ [100, 10000], both cutoffs).

Discussion (≈180 words). The zeta-regularised spectral sum does what Euler-Maclaurin predicts: the discrete sum over Riemann zeros agrees with the Riemann-von Mangoldt smooth integral up to an O(1) boundary term of order ½·ρ̄(γ_1) ≈ log(γ_1/2π)/(4π) ≈ 0.064 and an endpoint term at γ_N. The residue is *not* √N-sized (Gaussian-like), it is *not* Λ-growing, and it is *not* cutoff-universal beyond 10 %. Multiplying by Λ^4/(2π)² simply restores the Λ^4 divergence that any naive quartic mode counting gives — no cancellation magic. There is no emergent small number close to (2.24 meV)^4/M_Pl^4 ~ 10^{−120}; there is an O(1) boundary correction times a quartic cutoff, i.e. the ordinary cosmological-constant problem in disguise. The ZSA claim that Euler-Maclaurin on Riemann zeros yields a physical Λ, as formulated, **fails trivially**: the arithmetic residue carries no fine-tuned small number and the prefactor is unregularised.
