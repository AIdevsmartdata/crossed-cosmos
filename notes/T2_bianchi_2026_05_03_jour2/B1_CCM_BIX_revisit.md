# B1 + CCM-BIX revisit — max-effort Opus 4.7 (1M ctx)

**Date**: 2026-05-03. **Companion**: `/tmp/B1_CCM_BIX_revisit.{py,tex}`.
**Inputs**: `/tmp/B1_frw_entropy.md`, `/tmp/ccm_hartnoll_frw_bridge.md`,
`/tmp/T2_bianchi_extension.{md,tex,py}`. **arXiv API verified**:
2502.02661v2 (Hartnoll–Yang), 2511.22755v1 (Connes–Consani–Moscovici),
2305.11388 (Banerjee–Niedermaier).

---

## 1. B1-revisit verdict — **PARTIAL (no new theorem)**

Sympy-verified for vacuum Bianchi I, Kasner `(-1/3, 2/3, 2/3)`:

| Quantity | Value at `t→0⁺` |
|---|---|
| `√g_3` | `t` |
| `A_AH = 36π t²` | `→ 0` |
| `S_BH = 9π t²/G_N` | `→ 0` |
| `<K>_max = S_BH/(2π r_AH) = 3t/(2 G_N)` | `→ 0` |
| Algebraic obstruction (T2-BI) | smeared `<φ(f)²> ~ log³(δ) → ∞` |

The vanishings COINCIDE at `t→0⁺`, but the algebraic obstruction (no
cyclic-separating Ω) and the geometric one (`A_AH→0`) are *independent*
manifestations of the singular geometry. No derivation of `S = A/4G`.

Bekenstein-Bousso `<K>_ω ≤ S_BH` is **semi-classical** and breaks down
exactly at `t→0` (same caveat as S5 of the T2 paper). The FRW pullback
flattens the Hubble scale (yesterday B1 §5(a)); T2-BI uses direct
mode-decomposition, not pullback, so doesn't kill T2-BI itself but kills
B1's pullback-route. **B1 NO-GO of yesterday stands.**

## 2. CCM-BIX bridge verdict — **PARTIAL OPENING**

Sympy-verified algebraic relation (script Section 2):

```
   D_CCM = -i u ∂_u           on L²([λ⁻¹, λ], du/u)        (CCM eq 5.14)
   D_HY  =  i(x ∂_x + Δ)       on L²(R, dx),  Δ=½+iε         (HY eq 37)

   substituting u ↔ x:
   D_HY  =  -D_CCM + iΔ · id                              (sympy: 0 ≡ 0 ✓)
```

Change of variable `u = e^x`, `du/u = dx`, gives
`L²([λ⁻¹,λ], du/u) ≅ L²([-log λ, log λ], dx)` with `-i u ∂_u = -i ∂_x`.

> **Mapping (sympy-verified).** CCM's compact-interval dilation is the
> **periodic compactification** of HY's noncompact-picture dilation
> restricted to `[-log λ, log λ]`, up to sign flip + `iΔ` conformal-weight
> shift.

This **invalidates yesterday's NO-GO** (`ccm_hartnoll_frw_bridge.md`),
which compared CCM with the FRW modular `K_FRW ~ (R²-η²)∂_η`,
**quadratic** in η. HY's BKL/BIX dilation is **linear** in its Iwasawa
coordinate, exactly matching CCM. **The geometry is different** (BIX ≠ FRW).

**Residual gaps (honest)**:
- (a) HY's L-function is a wavefunction *overlap*, not an eigenvalue.
  Riemann zeros are zeros of `φ(t)~L(½+it)`, not of `D_HY` (HY §6:
  "absorption spectrum").
- (b) CCM spectrum approaches `{γ_n}` only after rank-one perturbation
  tied to Euler product over `p ≤ λ²` (CCM Thm 1.1).
- (c) **No dictionary** known mapping CCM's perturbation to HY's
  modular-invariance constraint.
- (d) Framework gap: HY = Wheeler-DeWitt minisuperspace (1-particle QM);
  T2-BI = local-AQFT BFV folium. Mathematically distinct.

## 3. Recommendation

**Pursue CCM-BIX further** — two specific directions:

1. **Iwasawa dilation on BIX minisuperspace.** Sympy-check that the
   BKL Iwasawa-`y` dilation on `SL(2,Z)\H` is literally CCM's `-i u ∂_u`
   via `u = e^y`. ~1 week.
2. **CCM perturbation ↔ HY modular constraint dictionary.** Show CCM's
   rank-one perturbation is an instance of HY's modular invariance.
   High-risk, high-reward. ~2-3 months.

**Do NOT pursue B1-revisit further.** "Both vanish together" is
structurally interesting but yields no new theorem beyond T2-BI.

---

**Sources verified live (arXiv API + HTML fetch)**: HY §2.1, §4.2 eq 37
verbatim: `Hψ=-i dψ/dx, Dψ=i(x dψ/dx + Δψ)`, SL(2,R) algebra. CCM Thm
1.1: rank-one spectrum convergence to ζ zeros, numerical only (NOT
proven RH).
