# V2 — Verification of D10 (DESI DR2 covariance + ECI Mahalanobis)

**Date:** 2026-04-21
**Target:** `derivations/D10-report.md`, `derivations/D10-desi-covariance.py`
**Source paper:** arXiv:2503.14738 (DESI DR2 Results II), cached at
`derivations/_cache/desi-dr2.pdf` + `.txt`.

## 1. Published values (independent re-extraction from cached PDF text)

From the paper text, Section VII, Eqs. (27)–(28) and pivot-redshift discussion
(lines 1820–1862 of the OCR text):

- Eq. (28) DESI+CMB+DESY5:
  **w₀ = −0.752 ± 0.057,  wₐ = −0.86 (+0.23 / −0.20)**
- Pivot: **z_p = 0.31,  w_p = −0.954 ± 0.024**
- Eq. (27) DESI+CMB+Union3: w₀=−0.667±0.088, wₐ=−1.09(+0.31/−0.27)
- DESI+CMB: z_p=0.53, w_p=−1.024±0.043

No 2×2 covariance matrix is published in the paper text or tables; the
covariance must be reconstructed. D10's source citation is correct.

## 2. Pivot-formula reconstruction (independent)

With a_p = 1/(1+z_p) = 1/1.31 = 0.7634 ⇒ **(1 − a_p) = 0.2366**.

Using the pivot-minimisation identity (d σ²(w_p)/d(1−a_p) = 0):

    cov(w₀, wₐ) = −(1 − a_p) · σ²(wₐ) = −0.2366 · 0.215² = **−0.01094**
    ρ(w₀, wₐ)   = cov / (σ_w0 σ_wa) = **−0.8926**
    σ(w_p)_pred = √(σ_w0² − (1−a_p)² σ_wa²)
                = √(0.003249 − 0.002590) = √0.000659 = **0.0257**

Compare to D10:

| Quantity       | D10 value | This verification | Match |
|----------------|-----------|-------------------|-------|
| σ(w₀)          | 0.057     | 0.057 (published) | ✓     |
| σ(wₐ) sym      | 0.215     | 0.215 (sym. of +0.23/−0.20) | ✓ |
| ρ(w₀,wₐ)       | −0.893    | **−0.8926**       | ✓     |
| cov(w₀,wₐ)     | −0.01094  | **−0.01094**      | ✓     |
| σ(w_p) predicted | 0.0257  | **0.0257**        | ✓     |
| σ(w_p) quoted  | 0.024     | 0.024 (published) | —     |

The 0.0257 vs 0.024 residual (≈ 7 %) is consistent with the mildly
asymmetric posterior; using σ_wa = 0.20 gives σ_p_pred = 0.032 (worse),
using σ_wa = 0.23 gives 0.017 (worse on the other side) — the symmetrised
0.215 minimises the discrepancy. D10's treatment is defensible.

## 3. Independent Mahalanobis distances

With mean (w₀, wₐ) = (−0.752, −0.86) and reconstructed C, I computed:

| Target                                                        | d (σ, 2-dof) | D10   |
|---------------------------------------------------------------|-------------:|------:|
| ΛCDM point (−1, 0)                                            | **4.359**    | 4.36  |
| Scherrer–Sen line wₐ = −1.58(1+w₀), minimum over w₀           | **3.330** at (−0.890, −0.174) | 3.33 |
| ECI NMC band (|ξ_χ| ≤ 2.4·10⁻², χ₀ = M_P/10), min over band    | **3.288**    | 3.29  |

All three match D10 to the precision reported (≤ 0.01σ).

2-dof thresholds: 1σ = √2.30 = 1.52, 2σ = √6.17 = 2.48. **The ECI band
(3.29σ) lies outside the DR2 + DESY5 2σ contour**, and is barely
distinguishable from the minimal-coupling Scherrer–Sen locus (3.33σ).

## 4. Verdict

**D10 is SOLID.**

- Published inputs (w₀, σ_w0, wₐ±, z_p, w_p±σ_wp) correctly transcribed
  from arXiv:2503.14738, Eq. (28) and the pivot paragraph.
- Pivot-minimisation identity correctly applied; ρ = −0.893 reproduced
  to 4 decimals; internal cross-check σ(w_p)_pred = 0.0257 vs quoted
  0.024 is a 7 % residual that D10 flags honestly.
- Mahalanobis distances (ΛCDM: 4.36σ, Scherrer–Sen: 3.33σ, ECI:
  3.29σ) reproduced independently to ≤ 0.01σ.
- The qualitative conclusion — ECI and minimal-coupling wCDM are
  *equally* disfavoured at ≈ 3.3σ by DR2+DESY5, with the ECI-specific
  band width adding < 0.05σ — follows directly and is correct.

No numbers in D10-report.md or D10-desi-covariance.py require correction.
The pending patch to `paper/section_3_5_constraints.tex` (Caveat 4) can
proceed on the basis of D10 as written.

**Caveat acknowledged but not blocking:** no official DESI DR2 2×2
covariance file is yet public, so the reconstruction relies on the
pivot identity. The 7 % σ(w_p) residual bounds the systematic at the
same level — well below the 3σ signal.
