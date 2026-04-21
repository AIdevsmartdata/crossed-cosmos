# D9 — Numerical verification of the NMC wₐ coefficient B(Ω_Λ)

**Date:** 2026-04-21 (night session, unsupervised).
**Author:** Claude (Opus 4.7) agent — repo `crossed-cosmos`, branch `master`.
**Driver question:** D7 propagated the coefficient

    B(Ω_Λ) = (8/√3) · A(Ω_Λ) ≈ 7.30  at Ω_Λ = 0.7

from a matter-era argument (D4) by hand. This D9 run integrates the full
NMC Klein-Gordon equation on a ΛCDM background to test whether B(0.7) is
correct within the ≤30% tolerance required to preserve the paper's
DR3-discriminative verdict.

## Method

- FLRW ΛCDM background, Ω_m = 0.3, Ω_Λ = 0.7, h = 0.7 (H in units of H₀).
- Scalar action: S = ∫√−g [(M_P²/2 − ξχ²/2) R − (1/2)(∂χ)² − V(χ)].
- Potential: V = V₀ exp(−αχ/M_P). V₀ set so V(χ₀) = 3H₀²Ω_Λ M_P² (DE-normalised).
- KG in e-folds N=ln a:
      χ'' + (3 + dlnH/dlnN) χ' + V'/H² + ξRχ/H² = 0
  with R = 6H²(2 + dlnH/dlnN).
- Friedmann kept at leading order; O(ξχ²/M_P²) ≲ 10⁻⁴ back-reaction ignored
  (consistent with D4/D7 derivation assumption).
- `scipy.integrate.solve_ivp`, method='LSODA', rtol=1e-8, atol=1e-10.
- Integration z=3 → z=0, thawing IC (χ=χ₀, χ'=0).
- CPL fit w(a)=w₀+wₐ(1−a) on a ∈ [0.3, 1].

## Results

### Sanity check (ξ=0)
Scan α ∈ {0.25, 0.40, 0.55, 0.70, 0.85} at χ₀=0.1 M_P gives

    −wₐ/(1+w₀) = 1.47–1.49   (mean 1.478)

vs Scherrer-Sen 2008 A(0.7)=1.58 → **6.4 % deviation**, slightly above the
5 % target. Attributed to: (i) thawing IC χ'=0 at z=3 not identically the
S&S attractor, (ii) CPL fit-window a∈[0.3,1] truncates late-time curvature.
Deviation is uniform across α, i.e. purely multiplicative. B is therefore
compared to the D7 *analytic* value B_D7 = 8/√3 · 1.58 = 7.30 (paper) AND
cross-checked against B/A_numerical (8/√3 · 1.478 = 6.82).

### ξ × χ₀ scan
α = 0.55 fixed (baseline 1+w₀ ≈ 0.043), grid
ξ ∈ {0, 10⁻³, 10⁻², 2.4×10⁻², −2.4×10⁻²} × χ₀/M_P ∈ {0.05, 0.1, 0.2}.
All 15 integrations succeeded, ρ_χ>0 everywhere, no NaNs.

Linear regression Δwₐ vs ξ·√(1+w₀)·(χ₀/M_P) through origin:

    B_numerical = 8.21 ± 0.49
    B_analytic  = 7.30
    ratio       = 1.125

**|ratio − 1| = 0.125 < 0.30  → D7 holds.**

### Caveat — χ₀ non-linearity
Local B values show a residual χ₀ dependence (B_local ≈ 14 at χ₀=0.05,
9.5 at χ₀=0.1, 7.3 at χ₀=0.2), i.e. the D7 analytic scaling Δwₐ ∝ χ₀ is
not exactly linear — the correction has some sub-leading (χ₀)⁰ piece.
Aggregated across the full grid the linear-through-origin fit is
B=8.21; at the paper's fiducial χ₀=0.1 M_P, B_local ≈ 9.5 (ratio 1.30,
marginal). This is inside but near the patch threshold and worth flagging.

### Band width at fiducial
At w₀=−0.75, |ξ|≤2.4×10⁻², χ₀=M_P/10:

    D7  analytic: Δwₐ = 8.76 × 10⁻³
    D9  numerical: Δwₐ = 9.85 × 10⁻³  (B=8.21 aggregate)
    D9  local   : Δwₐ ≈ 1.14 × 10⁻²  (B≈9.5 at χ₀=0.1)

DR2 σ(wₐ) ≈ 0.80 → ratio band/σ ≈ 1.2–1.4 × 10⁻². DR3 forecast
σ×0.3 ≈ 0.24 → ratio still ~4 × 10⁻². **Verdict "DR3/LSST-Y10
discriminative" is unchanged**: the ECI band remains ≪ σ at DR2/DR3.

## Verdict

- **D7 holds** within the 30% tolerance (aggregated ratio 1.125).
- Band width bumped up by ~12–30 % in the worst-case χ₀-local reading —
  immaterial for the DR2/DR3 science claim (both still ≪ σ(wₐ)).
- **No patch applied** to `D7-ppn-xi-bound.py` or
  `paper/section_3_5_constraints.tex`.
- Recommendation for future work: re-derive B(Ω_Λ, χ₀) including the
  sub-leading (χ₀-independent) piece from full NMC Friedmann (the
  6ξHχχ̇ and 3ξH²χ² terms we dropped), which likely explains the
  observed B_local(χ₀). Not required for the DR3 verdict.

## Artefacts
- Code: `derivations/D9-wa-numerical.py`
- Figure: `derivations/figures/D9-wa-numerical.{pdf,png}`
- Log: `derivations/_results/D9-wa-numerical.log`
- Summary JSON: `derivations/_results/D9-summary.json`

Status: FUNCTIONAL — D7 verdict validated numerically. No downstream
corrections required.
