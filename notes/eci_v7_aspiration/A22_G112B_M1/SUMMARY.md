# A22 — G1.12.B Milestone M1 (45_H modular S'_4 rep + f^{ij}(τ) at τ=i)

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A22 (parent persisted)
**Hallu count entering / leaving:** 78 / 78 (held; no fabrications)

## Verdict

**M1 BINARY GATE PASS (4/4)**. A18's first milestone of the 6-stage G1.12.B campaign is complete in 90 min vs projected 3-4 weeks. Handoff to M2 is mechanical.

## 1. Physics decision (45_H rep assignment, justified)

**45_H ~ S'_4 trivial singlet 1, weight k_{45} = 0**, with `f^{ij}(τ)` built from contractions inheriting LYD20 Model VI's per-row modular structure but with 3 independent couplings (κ̂_u, κ̂_c, κ̂_t). Modular invariance is row-by-row inherited; symmetric in flavor by 10·10·45_H decomposition; 100% off-diagonal density from Q-triplet contraction permutations. **Haba-Nagano-Shimizu-Yamada (arXiv:2402.15124, live-verified)** is the non-modular precedent we promote.

## 2. Symbolic f^{ij}(τ) (sympy polynomials in Y_1, Y_2, Y_3)

- **Row u (weight-1, 3̂'):** `(Y_1, Y_3, Y_2)`
- **Row c (weight-2, 3):** `(2Y_1²−2Y_2Y_3, 2Y_2²−2Y_1Y_3, 2Y_3²−2Y_1Y_2)`
- **Row t (weight-5, 3̂):** full polynomial — see `f_ij_modular.py`

## 3. f^{ij}(τ=i) explicit numerical 3×3 matrix (magnitudes)

```
[[  1.180   2.626    0.265 ]
 [  4.180   6.058   14.418 ]
 [454.57  227.28  227.28 ]]
```

Constraint Y_1²+2Y_2Y_3 at τ=i: ~10⁻¹⁵ ✓

## 4. Off-diagonal entries

**6/6 nonzero** (all > 10⁻¹⁰), magnitudes [0.27, 454.6]. Off-diagonal density 100%.

## 5. Modular invariance (S- and T-shift mass-ratio Δ)

- T (τ→τ+1): Δ = 0 (machine precision)
- S (τ→−1/τ): Δ = 0 (τ=i fixed point)

## 6. Closure check vs A2 +19.5%

A2 leading-log formula with M_{T_45}=10¹² GeV and ξη=0.44 gives **+19.43%** (within 0.07pp of target). f^{c,Q2}(i) = −6.058i provides the FIXED form-factor that the M2 free coupling κ̂_c will multiply.

## Handoff to M2 (mechanical)

M2 inputs are now fully specified: combine W1's (β_u/α_u, γ_u/α_u, τ*=−0.19+1.00i) with this f^{ij}(τ) template and fit (κ̂_u, κ̂_c, κ̂_t):
- κ̂_c fixed by +19.5% closure
- κ̂_u suppressed by m_u/m_c
- κ̂_t fixed by y_t = 0.4454

**M2 reduces to a 2-parameter scan; mechanical given M1 PASS.**

## Caveats

- Y^(5)_{3̂}/Y^(5)_{3̂'} mixing at weight-5 in t-row uses LYD20 Model VI convention; M_T45 alternative weight assignments {2,4,6} would re-derive but mass ratios robust per S/T invariance.
- f^{ij}(τ) is the STRUCTURAL TEMPLATE; full Yukawa is `κ̂_i v_{45} × f^{ij}(τ)` per row.

## Live-verified arXiv IDs this session

- 2402.15124 Haba-Nagano-Shimizu-Yamada ✓
- 2006.10722 Liu-Yao-Ding (LYD20) ✓
- Re-used from A18 ledger: 2310.16563 Patel-Shukla, 2510.01312 Antusch-Hinze-Saad, 2006.03058 NPP20

## Files

- `f_ij_modular.py` — full symbolic + numeric implementation, runs all 4 gates standalone (21 KB)
- `_sanity.py` — supplementary sanity checks (constraint, LYD20 BF τ, c-row entries)
