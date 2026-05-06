---
name: M22 formula comparison table — 8 renormalization formulas × 4 m-values
description: Sympy-by-hand verification of 2-adic valuation patterns for each formula
date: 2026-05-06
owner: Sub-agent M22 (Sonnet 4.6, Phase 3.D VALIDATION)
hallu_count: 85/85
---

# M22 — Formula Comparison Table: β-Renormalization Monotonicity

## Setup

**Newform:** 4.5.b.a, k=5, N=4, p=2, CM by K=Q(i)

**Hurwitz-normalized α_m values (exact, verified by A5 to 60 digits):**
| m | α_m | factored | v_2(α_m) |
|---|-----|----------|----------|
| 1 | 1/10 | 1/(2·5) | -1 |
| 2 | 1/12 | 1/(4·3) | -2 |
| 3 | 1/24 | 1/(8·3) | -3 |
| 4 | 1/60 | 1/(4·15) | -2 |

**Raw v_2 pattern: {-1, -2, -3, -2} — NOT monotone.**

Parameters: p=2, k=5, p^(m-1) for m=1..4: {1, 2, 4, 8}. α_p = -4.

---

## 2-adic valuation function v_2(a/b) = v_2(a) - v_2(b)

All computations are exact rational arithmetic verified by hand.

---

## F1: M13 Baseline
**Formula:** α_m · (-2^(m-1)) · (1 + 2^(m-3))

| m | 2^(m-1) | 2^(m-3) | (1+2^(m-3)) | F1(α_m) | Factored | v_2 |
|---|---------|---------|-------------|---------|---------|-----|
| 1 | 1 | 1/4 | 5/4 | (1/10)·(-1)·(5/4) = -1/8 | -1/2³ | **-3** |
| 2 | 2 | 1/2 | 3/2 | (1/12)·(-2)·(3/2) = -1/4 | -1/2² | **-2** |
| 3 | 4 | 1 | 2 | (1/24)·(-4)·2 = -1/3 | -1/3 | **0** |
| 4 | 8 | 2 | 3 | (1/60)·(-8)·3 = -2/5 | -2/5 | **+1** |

**v_2 pattern: {-3, -2, 0, +1} — STRICTLY MONOTONE INCREASING ✓**

---

## F2: Pollack-style (positive)
**Formula:** α_m · 2^(m-1)

| m | 2^(m-1) | F2(α_m) | Factored | v_2 |
|---|---------|---------|---------|-----|
| 1 | 1 | 1/10 | 1/(2·5) | **-1** |
| 2 | 2 | 2/12 = 1/6 | 1/(2·3) | **-1** |
| 3 | 4 | 4/24 = 1/6 | 1/(2·3) | **-1** |
| 4 | 8 | 8/60 = 2/15 | 2/(3·5) | **+1** |

**v_2 pattern: {-1, -1, -1, +1} — WEAKLY increasing (3-way tie then jump). NOT STRICTLY MONOTONE.**

Note: Adding a negative sign (F2b: α_m·(-2^(m-1))) gives identical v_2 pattern since v_2 is sign-blind.

---

## F3: Functional-equation antisymmetrization
**Formula:** α_m - α_{k-m}, k=5

| m | k-m | α_m | α_{k-m} | F3(α_m) | Factored | v_2 |
|---|-----|-----|---------|---------|---------|-----|
| 1 | 4 | 1/10 | 1/60 | 6/60-1/60 = 5/60 = 1/12 | 1/(4·3) | **-2** |
| 2 | 3 | 1/12 | 1/24 | 2/24-1/24 = 1/24 | 1/(8·3) | **-3** |
| 3 | 2 | 1/24 | 1/12 | 1/24-2/24 = -1/24 | -1/(8·3) | **-3** |
| 4 | 1 | 1/60 | 1/10 | 1/60-6/60 = -5/60 = -1/12 | -1/(4·3) | **-2** |

**v_2 pattern: {-2, -3, -3, -2} — SYMMETRIC, descends then ascends. NOT MONOTONE.**

---

## F4: Functional-equation symmetrization
**Formula:** (α_m + α_{k-m})/2, k=5

| m | k-m | F4(α_m) | Factored | v_2 |
|---|-----|---------|---------|-----|
| 1 | 4 | (1/10+1/60)/2 = (7/60)/2 = 7/120 | 7/(8·15) | **-3** |
| 2 | 3 | (1/12+1/24)/2 = (3/24)/2 = 1/16 | 1/2⁴ | **-4** |
| 3 | 2 | same as m=2: 1/16 | 1/2⁴ | **-4** |
| 4 | 1 | same as m=1: 7/120 | 7/(8·15) | **-3** |

**v_2 pattern: {-3, -4, -4, -3} — SYMMETRIC (M13 Finding 2). NOT MONOTONE.**

---

## F5: Euler-factor compensation
**Formula:** α_m · (1 - α_p^{m-1}), α_p = -4

| m | (-4)^(m-1) | (1-(-4)^(m-1)) | F5(α_m) | v_2 |
|---|-----------|---------------|---------|-----|
| 1 | 1 | 0 | 0 | **+∞** |
| 2 | -4 | 5 | 5/12 = 5/(4·3) | **-2** |
| 3 | 16 | -15 | -15/24 = -5/8 | **-3** |
| 4 | -64 | 65 | 65/60 = 13/12 = 13/(4·3) | **-2** |

**v_2 pattern: {+∞, -2, -3, -2} — NOT MONOTONE (degenerate at m=1).**

*Note: The zero at m=1 reflects the Euler factor vanishing at the Steinberg edge — this is the degeneracy M13 identified.*

---

## F6: Iwasawa-log convention (renormalizer with 2-adic unit factor)
**Formula:** α_m · log_2(γ)/(γ-1), γ=5 (generator of 1+4Z_2)

**2-adic analysis of log_2(5):**
- log_2(5) = Σ_{k≥1} (-1)^{k+1} (5-1)^k/k = 4 - 8 + 64/3 - 64 + 1024/5 - ...
- v_2(term_1) = v_2(4) = 2
- v_2(term_2) = v_2(-8) = 3
- All subsequent terms have v_2 ≥ 6
- Therefore v_2(log_2(5)) = **2** (determined by leading term)

**Renormalizer:** log_2(5)/(γ-1) = log_2(5)/4; v_2 = 2-2 = **0**.

A factor with v_2 = 0 (2-adic unit) does NOT change the v_2 of any product.

| m | F6(α_m) ~ α_m | v_2 |
|---|--------------|-----|
| 1 | same v_2 as 1/10 | **-1** |
| 2 | same v_2 as 1/12 | **-2** |
| 3 | same v_2 as 1/24 | **-3** |
| 4 | same v_2 as 1/60 | **-2** |

**v_2 pattern: {-1, -2, -3, -2} — SAME AS RAW. NOT MONOTONE.**

*This shows that the Iwasawa-log renormalizer (used in Pollack's construction) alone does not restore monotonicity for this form.*

---

## F7: Gauss-sum/triangular factor
**Formula:** α_m · 2^{m(m-1)/2}

| m | m(m-1)/2 | 2^{m(m-1)/2} | F7(α_m) | Factored | v_2 |
|---|----------|-------------|---------|---------|-----|
| 1 | 0 | 1 | 1/10 | 1/(2·5) | **-1** |
| 2 | 1 | 2 | 2/12=1/6 | 1/(2·3) | **-1** |
| 3 | 3 | 8 | 8/24=1/3 | 1/3 | **0** |
| 4 | 6 | 64 | 64/60=16/15 | 16/(3·5) | **+4** |

**v_2 pattern: {-1, -1, 0, +4} — WEAKLY increasing (tie at m=1,2 then strict jump). NOT STRICTLY MONOTONE.**

*The triangular exponent gives a larger jump at m=4 than M13, but shares the non-strict tie at m=1,2.*

---

## F8: Galois-twist (cyclotomic character weight)
**Formula:** α_m · 2^(m-1) · m

| m | 2^(m-1)·m | F8(α_m) | Factored | v_2 |
|---|----------|---------|---------|-----|
| 1 | 1 | 1/10 | 1/(2·5) | **-1** |
| 2 | 4 | 4/12=1/3 | 1/3 | **0** |
| 3 | 12 | 12/24=1/2 | 1/2 | **-1** |
| 4 | 32 | 32/60=8/15 | 8/(3·5) | **+3** |

**v_2 pattern: {-1, 0, -1, +3} — NOT MONOTONE (up, then down, then jump).**

---

## Summary Table

| Formula | Description | v_2 pattern | Strictly Monotone | Weakly Inc |
|---------|-------------|------------|-------------------|------------|
| Raw | α_m (no renorm) | {-1,-2,-3,-2} | NO | NO |
| **F1 (M13)** | α_m·(-2^{m-1})·(1+2^{m-3}) | **{-3,-2,0,+1}** | **YES ✓** | YES |
| F2 (Pollack+) | α_m·2^{m-1} | {-1,-1,-1,+1} | NO | YES (weak) |
| F3 (FE-antisymm) | α_m-α_{k-m} | {-2,-3,-3,-2} | NO | NO |
| F4 (FE-symm) | (α_m+α_{k-m})/2 | {-3,-4,-4,-3} | NO | NO |
| F5 (Euler-factor) | α_m·(1-α_p^{m-1}) | {+∞,-2,-3,-2} | NO | NO |
| F6 (Iwasawa-log) | α_m·log_p(γ)/(γ-1) | {-1,-2,-3,-2} | NO | NO |
| F7 (Gauss-triang) | α_m·2^{m(m-1)/2} | {-1,-1,0,+4} | NO | YES (weak) |
| F8 (Galois-twist) | α_m·2^{m-1}·m | {-1,0,-1,+3} | NO | NO |

**Strictly monotone: 1/8 formulas (F1 only)**
**Weakly increasing (non-decreasing): 3/8 formulas (F1, F2, F7)**

---

## Key Observations

1. **Strict monotonicity is unique to F1.** No other natural formula produces a strictly increasing v_2 sequence.

2. **F2 and F7 are weakly increasing**, but fail strict monotonicity due to ties at m=1 and m=2. The absence of the (1+2^{m-3}) correction factor (present in F1) causes the tie.

3. **The (1+2^{m-3}) factor in F1 is load-bearing.** It contributes:
   - At m=1: multiplies by 5/4, subtracting 2 from v_2 to shift from -1 to -3
   - At m=2: multiplies by 3/2, adding 0 net (shifts from -1 to -2 via the overall factor combination)
   - At m=3: multiplies by 2 = 2^1, adding 1 to v_2 (shifts from -1 to 0)
   - At m=4: multiplies by 3, adding 0 to v_2 (maintains shift)

   Without it (F2), the sequence stalls at -1 for m=1,2,3.

4. **Functional-equation formulas (F3, F4) are anti-monotone by construction:** they symmetrize, producing palindromic patterns.

5. **F5 degenerates at m=1** because (1-α_p^0) = 0, reflecting the Steinberg-edge zero-root issue M13 identified as the core obstruction.
