---
name: M145 Opus BSD-CM × ECI v8.1 — VERDICT (D) PARTIAL — 5-fold ϖ kinematic coincidence, NO new BSD information
description: ECI v8.1 does NOT give new BSD info for E:y²=x³-x (LMFDB 32.a3). DOES discover 5-fold ϖ structural coincidence: Ω_real=2ϖ + Ω_∞=ϖ Yager-Katz + α_2=1/12 weight-5 + m_τ²∝ϖ⁴ N=1 SUGRA + L(E,1)=ϖ/4 BSD-strong. Important myths dispelled: CW1977 only proves rank>0⟹L=0 (NOT Sha finite, that's Rubin 1991); Yager Table k+j≥4 not BSD; 4.5.b.a is weight-5 not elliptic curve. Hallu 100 held
type: project
---

# M145 — Opus BSD-CM × ECI v8.1

**Date:** 2026-05-06 | **Hallu count: 100 → 100** held (M145: 0 fabs) | **Mistral STRICT-BAN** | Time ~110min

## VERDICT (D) PARTIAL — structural connection, NO new BSD information

ECI v8.1 (M134 lemniscate ϖ at τ=i + M142 Yager Table) does **NOT** give new BSD information for E: y²=x³-x (LMFDB 32.a3, Cremona 32a2). It gives a **kinematic alignment** between two literatures — the lemniscate constant ϖ appears as both the SUGRA modulus mass scale (M134) and the BSD real period (LMFDB 32.a3 verified Ω_real = 2ϖ exactly).

Probability calibration retroactive: (A) <0.5%, (B) 5-15%, (C) 60-75%, (D) 15-25%. **Achieved (D) at lower-mid** — partial structural link.

## What is rigorously CONFIRMED

### LMFDB 32.a3 verified live 2026-05-06

E: y² = x³ - x ≅ y² = 4x³ - 4x (Coates-Wiles model) via (x, y) ↔ (x, y/2)
- Conductor N = **32 = 2⁵** (NOT 64)
- j(E) = 1728, CM discriminant D = -4 (CM by ℤ[i])
- Rank E(ℚ) = 0
- E(ℚ)_tors = ℤ/2ℤ ⊕ ℤ/2ℤ (generators (0,0), (1,0))
- **Ω_real = 5.244115108... = 2ϖ exactly** (ϖ lemniscate)
- **L(E,1) = 0.65551438857... = ϖ/4** numerically (= 2ϖ × 1/8)
- Tamagawa c_2 = 2 (only bad prime)
- BSD strong: L(E,1)·#(E_tor)²/(Ω·Reg·∏c_p) = 0.65551×16/(5.244×1×2) = **1** ⟹ **#Sha_an = 1 exact**

### Coates-Wiles 1977 page 12 Theorem 3 (verbatim)

> "**Theorem 3.** Assume that E is defined over Q, and has complex multiplication by the ring of integers of an imaginary quadratic field with class number 1. **If E has a rational point of infinite order, then the Hasse-Weil zeta function of E over Q vanishes at s=1.**"

This is the **rank > 0 ⟹ L(E,1) = 0** half (BSD weak, descending direction only). Does NOT prove Sha finiteness.

### Rubin Cetraro lectures Corollary 12.13 (verbatim p.64)

> "**Corollary 12.13.** Suppose 𝔭∤𝔣, p > 7, and K_𝔭 = Q_p.
> (i) If L(ψ̄, 1) = 0 then S_{𝔭^∞} is infinite.
> (ii) If L(ψ̄, 1) ≠ 0 then **#(III(E)_{𝔭^∞}) ~ L(ψ̄, 1) / Ω**."

So **BSD-strong p-part is rigorous for all p > 7 split in K = Q(i)**. Open primes p ∈ {2, 3, 5, 7} ; for our curve **p = 2 is bad reduction** (conductor 2⁵).

## What Yager 1982 + ECI v8.1 do NOT give

The BSD-relevant value is **L(ψ̄, 1) / Ω** at WEIGHT-1 character. Yager's table covers k+j ≥ 4 only ; **BSD-relevant k+j=1, k=1 case is OUTSIDE Yager's framework**. M142's α_2 = 1/12 is for the WEIGHT-5 newform L-value at s=2 (Damerell-normalized), NOT BSD-relevant elliptic-curve L-value at s=1.

## Direction-by-direction

**A. Sha(E/ℚ)[2] — NEGATIVE.** 2-descent (classical Cassels-Tate, Cremona ECDATA) gives Sha(E/ℚ)[2^∞] = 0. Yager 1982 does NOT improve this.

**B. Heegner points at τ=i — STRUCTURAL HINT.** Heegner hypothesis FAILS for K = Q(i) at level 32: gcd(disc K, N) = gcd(-4, 32) = 4 ≠ 1. Standard Gross-Zagier 1986 doesn't apply. M134's V_F lives on X(1) (j-line), not X_0(32). V_F (SUGRA scalar potential) and Néron-Tate height (bilinear pairing on E(ℚ̄)) are different mathematical objects — no height formula connects them. **No new BSD information.**

**C. IMC bypass via R-2 — UNRELATED.** ECI's R-2 BKNO p=2 obstruction is for **weight-5 motive M_f**, not weight-2 elliptic curve motive M_E. For E at p=2: 2 ramifies in ℤ[i] ((2)=(1+i)²), Rubin's "p split + p > 7" hypothesis fails on both counts. IMC at p=2 for E is Kobayashi 2003 supersingular framework (separate). **NEGATIVE.**

**D. Dispel myths — CLARIFIED.**

| Myth | Status |
|---|---|
| "Coates-Wiles 1977 proved BSD strong for y²=x³-x" | **FALSE.** CW 1977 Thm 3 only gives rank>0 ⟹ L(E,1)=0. Sha finiteness = Rubin 1991 [Ru2] using Kolyvagin Euler systems on elliptic units. |
| "Yager 1982 Table gives Sha order" | **FALSE.** Yager k+j ≥ 4. BSD-relevant value at k+j=1, k=1 is outside table. |
| "ECI v8.1 + ϖ at τ=i gives BSD-strong refinement" | **(D) PARTIAL.** L(E,1)/Ω = 1/8 is structurally lemniscate-clean but classical (Hurwitz 1899, Damerell 1971). |
| "f = 4.5.b.a is an elliptic curve" | **FALSE.** Weight-5 newform; L(f,s) = L(ψ̄⁴, s), NOT L(ψ̄, s). M142 α_2=1/12 is for weight-5 motive, not BSD-strong of E. |

## Observation M145.1 (kinematic) — what ECI v8.1 DOES contribute

The lemniscate constant ϖ appears simultaneously as:
1. Real period **Ω_real = 2ϖ** of E:y²=x³-x (LMFDB 32.a3)
2. Yager-Katz period **Ω_∞ = ϖ** of (E, dx/y) (Katz 1977 §3.9 verbatim)
3. Weight-5 CM L-value normalization **α_k for f = 4.5.b.a** (M142 α_2 = 1/12 RIGOROUS)
4. N=1 SUGRA modulus mass **m_τ² ∝ ϖ⁴** at τ=i (M134 RIGOROUS)
5. BSD-strong leading term **L(E,1) = ϖ/4 = Ω_real/8** (LMFDB numerical)

This **5-fold ϖ-coincidence** is structurally suggestive — same period across number theory, modular geometry, N=1 SUGRA. Supports ECI v8.1 thesis that τ=i is dynamically-selected modulus VEV across multiple sectors. **NOT a new BSD theorem** — publishable structural-connection observation.

## Recommendations

1. **DO NOT claim** ECI attacks BSD Millennium. Negative outcome (D) is the honest conclusion.
2. **DO add Observation M145.1** to ECI v8.1 manifesto (5-fold ϖ kinematic coincidence) as Lakatos-style heuristic.
3. **R-6 paper (α_2 = 1/12 RIGOROUS via M142) is the publishable result.** Do NOT add BSD-strong claims beyond explicit Damerell/Yager normalization.
4. **Future M150+ idea**: Congruent number family E_d: y²=x³-d²x. BSD over family = congruent number problem (Millennium-adjacent). Tunnell 1983 conditional. ECI might give framing.

## Discipline log

- Mistral STRICT-BAN observed
- All claims verbatim PDFs Read multimodally (CW 23pp, Yager 12pp, Rubin 1-65 selective)
- LMFDB live (3 WebFetch passes), 6 WebSearch queries
- 0 fabrications, 0 catches needed
- Hallu count: 100 → 100 held
- Time ~110min within budget

## References verified live

- LMFDB 32.a3 https://www.lmfdb.org/EllipticCurve/Q/32/a/3
- Yager 1982 Compositio Math 47 NUMDAM (M142 + M145 cross-verified)
- Coates-Wiles 1977 Inventiones BSD link.springer.com/article/10.1007/BF01402975
