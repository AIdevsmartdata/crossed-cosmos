# D7 Plan — PPN bound on ξ_χ and NMC Scherrer–Sen

**Goal.** Close the two gaps flagged in `docs/REVIEW_NOTES.md` and paper §3.1:
(i) Cassini PPN γ−1 bound on the NMC coupling ξ_χ; (ii) derivation of the
NMC generalisation of Scherrer–Sen wₐ(w₀; ξ_χ), so that ECI Prediction #1
becomes (or fails to become) discriminative vs wCDM on DESI DR2.

## Steps

1. **Plan (this file).** Committed first.
2. **PPN derivation (`D7-ppn-xi-bound.py`, sympy).** Start from
   S = ∫ d⁴x √−g [ (M_P²/2) R − (1/2)(∂χ)² − V(χ) − (ξ_χ/2) R χ² ].
   In the Jordan frame the effective Newton "constant" is
   G_eff(r) = G [1 + 2 (ξ_χ χ)² /(M_P²/φ')² ]-type factor. Use the standard
   Damour–Esposito-Farèse 1993 result: for a scalar coupled to curvature with
   F(χ) = M_P² + ξ_χ χ², the PPN parameter is
     γ − 1 = −2 F_χ² / (F + 2 F_χ²) evaluated at χ=χ₀,
   where F_χ ≡ dF/dχ = 2 ξ_χ χ. This gives
     γ − 1 = − 8 ξ_χ² χ₀² / (M_P² + ξ_χ χ₀² (1 + 8 ξ_χ)).
   For |ξ_χ| ≪ 1 and χ₀ ≲ M_P this simplifies to
     γ − 1 ≃ − 8 ξ_χ² χ₀² / M_P²    (leading order).
   Cassini: |γ − 1| < 2.3×10⁻⁵ ⇒ |ξ_χ| (χ₀/M_P) ≲ 1.7×10⁻³.
   For χ₀ = M_P/10 ⇒ |ξ_χ| ≲ 1.7×10⁻². Verify ξ→0 limit: γ=1. OK.
3. **NMC Scherrer–Sen (reuse D4 machinery).** D4 already computed
   wₐ = −(24/7)(1+w₀)[1 + 8ξ_χ χ/(α M_P)] in the matter-era approximation
   with exponential V. The −24/7 assumes Ω_m=1; the true coefficient at
   Ω_Λ=0.7 is A(Ω_Λ) ≈ 1.58 (Scherrer–Sen 2008 Eq. (15)). Factorise as
     wₐ = −A(Ω_Λ)(1+w₀) + B(Ω_Λ) ξ_χ (1+w₀)^{1/2} (χ₀/M_P)
   with A(0.7)=1.58, B(0.7)=8/√3 · A · 1 ≈ 7.30. Limit ξ→0 → −1.58(1+w₀) ✓.
4. **Plot.** (w₀, wₐ) plane. DESI DR2 mean (−0.75, −0.86); approximate
   covariance σ_w0=0.2, σ_wa=0.8, ρ=−0.8. Scherrer–Sen line. ECI band
   from |ξ_χ| ≤ ξ_max(χ₀=M_P/10) ≈ 1.7×10⁻². The correction
   B·ξ·(1+w₀)^{1/2}·0.1 with w₀=−0.75 is 7.3·0.017·0.5·0.1 ≈ 6×10⁻³,
   i.e. *tiny* compared to σ_wa=0.8. The band will be narrower than the
   linewidth of Scherrer–Sen. **Prediction:** ECI indistinguishable from
   wCDM at DR2. Needs DR3/LSST Y10.
5. **LaTeX `section_3_5_constraints.tex`.** Write up with caveats.
   Compile standalone to verify.
6. **Table append.** Add row #1b in eci.tex prediction table with
   `% TODO REMONDIERE: validate` — flag DR3/LSST Y10 as the true horizon.

## Honesty budget
- ξ² suppression means the PPN bound is *weak* (only requires |ξ| ≲ 10⁻²);
- the NMC correction to wₐ scales like ξ·χ/M_P, thus ≲ 10⁻³: well inside
  DR2 error ellipse. Must state clearly: ECI is NOT DR2-falsifiable.
