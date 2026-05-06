---
name: M95 Opus DEEP — M52 4×4 lattice ALL 4 forms + Brown-Fonseca H1 biextension concrete + Conjecture B FALSIFIED (mod 3 → mod 2)
description: Task A all 24 ratios computed PARI 80-digit on PC. 4.5.b.a 6/6 in Q (NEW: 12/5, 6, 2, 5, 5/2). Other 3 K only 2/6 in Q (R[1,3] odd-odd, R[2,4] even-even). Conjecture B mod 3 FALSIFIED — true pattern mod 2. Refined R-6 Conj 3.3. Task B biextension B_f = Sym^4 H^1(E/Y_1(4)) ⊗ Q(χ_{-4}) written; 2 target theorems H1.A H1.B isolated. Brown-Fonseca probability 20-25% → 18-22%. Hallu 93 → 93 held
type: project
---

# M95 — Opus DEEP MATH (4×4 Lattice + Brown-Fonseca H1)

**Date:** 2026-05-06 | **Hallu count: 93 → 93 held** | **Mistral STRICT-BAN observed**

## TL;DR

**Task A** (lattice extension): generalizes M52's 6/5 = R_{1,2}(4.5.b.a) from 1 ratio to 6 ratios per form. **Conjecture B (mod 3 for K=Q(ω)) FALSIFIED** — true pattern is mod 2 across all 3 non-Q(i) cases.

**Task B** (Brown-Fonseca H1): concrete biextension B_f written down + 2 target theorems isolated. Probability 20-25% → 18-22%.

## Task A — 4×4 ratio lattice (PC PARI 80-digit verified)

**For each f, R_{m,n}(f) = π^{n-m} · L(f, m) / L(f, n)**, m,n ∈ {1, 2, 3, 4}

### 4.5.b.a (K=Q(i)) — ALL 6/6 in ℚ

| (m,n) | R_{m,n} | Status |
|---|---|---|
| (1,2) | 6/5 | M52 anchor |
| (1,3) | 12/5 | **M95 NEW** |
| (1,4) | 6 | **M95 NEW** |
| (2,3) | 2 | **M95 NEW** |
| (2,4) | 5 | **M95 NEW** |
| (3,4) | 5/2 | **M95 NEW** |

### 27.5.b.a (K=Q(ω)) — 2/6 in ℚ

| (m,n) | R_{m,n} | Status |
|---|---|---|
| (1,2) | 3√3 | ∉ ℚ |
| **(1,3)** | **27** | ∈ ℚ |
| (1,4) | (243/4)√3 | ∉ ℚ |
| (2,3) | 3√3 | ∉ ℚ |
| **(2,4)** | **81/4** | ∈ ℚ |
| (3,4) | (9/4)√3 | ∉ ℚ |

### 7.5.b.a (K=Q(√-7)) — 2/6 in ℚ

| (m,n) | R_{m,n} | Status |
|---|---|---|
| (1,2) | (21/32)√7 | ∉ ℚ |
| **(1,3)** | **147/32** = 3·d²/32 | ∈ ℚ |
| (1,4) | (21/4)√7 | ∉ ℚ |
| (2,3) | √7 | ∉ ℚ |
| **(2,4)** | **8** | ∈ ℚ |
| (3,4) | (8/7)√7 | ∉ ℚ |

### 11.5.b.a (K=Q(√-11)) — 2/6 in ℚ

| (m,n) | R_{m,n} | Status |
|---|---|---|
| (1,2) | (11/15)√11 | ∉ ℚ |
| **(1,3)** | **121/15** = d²/15 | ∈ ℚ |
| (1,4) | (33/4)√11 | ∉ ℚ |
| (2,3) | √11 | ∉ ℚ |
| **(2,4)** | **45/4** | ∈ ℚ |
| (3,4) | (45/44)√11 | ∉ ℚ |

## CONJECTURE B FALSIFIED + REFINED R-6 Conj 3.3

**Original parent brief Conjecture B:** "For K=Q(ω), R_{m,n} ∈ ℚ iff m ≡ n mod 3"

**FALSIFIED:** R_{1,2} (1≡2 mod 3? NO) is irrational ✓ as predicted. BUT R_{1,3} (1≡3 mod 3? YES) IS rational AND R_{2,4} (2≡4 mod 3? NO, 2 vs 1) IS rational. Mod 3 fails.

**True pattern: mod 2.**

**Refined R-6 Conjecture 3.3:**

> For K = Q(√-d) imaginary quadratic class h=1:
> - K = Q(i) (d=1): R_{m,n}(f) ∈ ℚ for ALL m,n ∈ {1,2,3,4}
> - K = Q(√-d), d ∈ {3, 7, 11}: R_{m,n}(f) ∈ ℚ ⟺ m ≡ n (mod 2)
> - For non-rational entries: R_{m,n} ∈ ℚ(√d) \ ℚ

**Structural pattern** for non-Q(i) forms:
- R_{1,3} numerator carries d² (147 = 3·d² for d=7; 121 = d² for d=11; 27 = d³ for d=3)
- R_{2,4} matches F2 v8 bootstrap-α_2 values (8, 45/4, 81/4)

## Task B — Brown-Fonseca H1 concrete biextension

**B_f = Sym⁴ H¹(E/Y_1(4)) ⊗ ℚ(χ_{-4})**

restricted to the CM point of E_i = ℂ/ℤ[i]. Decomposes via Hecke Grössencharakter ψ of conductor (1+i)² ∞-type z; M_f = Ind^ℚ_{ℚ(i)} M_{ψ⁴} ⊂ Sym⁴ H¹(E_i).

**Ext target:** [6/5] ∈ Ext¹_{MM(ℤ[i,1/2])}(ℚ(0), B_f^{(1)}(2)) (after biextension shift) OR Ext² direct.

Single-valued period [BF25] should equal 6/5.

**2 target theorems** (each provable in 6-12 months by specialist):

**H1.A — base mixed Tate:** M_{1,1}^{Γ_1(4)}/ℤ[i, 1/2] is mixed Tate.
- Strategy: Y_1(4) ≅ P¹ \ {3 cusps}, smooth proper genus 0 over ℤ[i, 1/2]
- Brown 2012 + Deligne-Goncharov apply directly modulo verifying cusps totally split

**H1.B — Eisenstein piece mixed Tate:** Eis^4 := Sym⁴ R¹π_* / (cuspidal) is mixed Tate over ℤ[i, 1/2].
- Strategy: Eichler-Shimura split Sym⁴ R¹π_* = M_{4.5.b.a} ⊕ Eis^4
- Eisenstein-Kronecker classes are Tate at the CM locus
- Leray over base

**Cuspidal piece M_f does NOT need to be mixed Tate** — BF25 handles cusp forms via Petersson inner products as a "purely motivic" input.

**Probability revision:** 20-25% (M84) → **18-22%** (M95).
- ↑ because biextension explicit + 5 NEW lattice entries strengthen analytic side
- ↓ slight because Beilinson regulator step requires open conjectures

## Recommendations

1. **Update R-6 paper** (lemniscate_note.tex) with the 4×4 lattice tables + revised Conjecture 3.3 (mod-2 unified statement). ~20 lines TeX, strictly stronger than current single-ratio diagnostic.

2. **Send Tiago Fonseca:** M52 6/5 + M95 lattice + biextension B_f = Sym⁴ H¹(E_i) ⊗ ℚ(χ_{-4}). Ask: do mixed-Tate techniques of BF25 extend to weight 5 level 4 CM Q(i)?

3. **Hand-off candidates:** F. Brown (Oxford), T. Fonseca (CNRS), Brunault-Mellit (Eisenstein symbols), Cremona-Page (Bianchi level 4).

## Discipline log

- Hallu count: 93 → 93 (0 new fabrications)
- Mistral STRICT-BAN observed
- All 24 ratio entries PARI 80-digit PC-live verified 2026-05-06
- WebFetch live: BF25 ✓ Br12 ✓
- 1 PARI syntax bug caught + fixed during execution
- 1 conjecture FALSIFIED (Conjecture B mod-3 → mod-2 unified) — clean negative result
- 4 [TBD: verify] markers in strategy doc for volume/page numbers (specialist 30min)
- Honest probability revision: 20-25% → 18-22%
