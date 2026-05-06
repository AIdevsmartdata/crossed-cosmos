---
name: M85 (1+i)^{e_k} 9 Heegner-Stark fields — SCAFFOLD-EXISTS confirmed + M74 CORRECTED (3 cases, not 2 for d=1)
description: Unified 9-field × 8-weight conductor exponent table derived via local unit filtration. M74 had 2 errors at d=1 (stated e=2 for k≡1 mod 4 should be e=0, missed k≡3 mod 4 → e=2 case). 4 LMFDB entries verified. New prediction d=3 k=4 → level 9. ~50% publishable as M55 paper appendix sub-lemma. Hallu BUMP 91 → 92
type: project
---

# M85 — (1+i)^{e_k} extension to all 9 Heegner-Stark imag-quad fields (D4-#1)

**Date:** 2026-05-06 | **Hallu count: 91 → 92** (M74 d=1 formula error caught) | **Mistral STRICT-BAN observed**

## VERDICT: SCAFFOLD-EXISTS (M75 F-3 confirmed) + M74 CORRECTED

The unified 9-field × 8-weight table for e_k(K) and minimal level N_k(K) is derivable from elementary local CFT (Watkins PMB 2011 + Schertz Cambridge 2010 + Neukirch Ch. VI), but **explicit unified table appears absent from literature**. Publishability ~50% as M55 paper appendix sub-lemma.

## CRITICAL: M74 d=1 formula was WRONG (3 cases, not 2)

**M74 stated:** "e_k = 2 if 4|(k-1), else e_k = 3" (2 cases)

**M85 derives (correct):**
- k ≡ 1 mod 4: e_k = 0 → level 4
- k ≡ 3 mod 4: e_k = 2 → level 16 ← **MISSED by M74**
- k ≡ 0 or 2 mod 4: e_k = 3 → level 32

**Verification:**
- k=2 (≡2 mod 4 → e=3, level 32) → 32.2.a.a ✓
- k=5 (≡1 mod 4 → e=0, level 4) → 4.5.b.a ✓ (M74 said e=2 here, would predict level 16 — WRONG)

**Hallu bump 91 → 92.**

## Unified Lemma M85.1 (4 type formulas)

**Type I — d=1 (K=Q(i), w_K=4, p_K=2):**
- e_k = 0 if k ≡ 1 mod 4 → level 4
- e_k = 2 if k ≡ 3 mod 4 → level 16
- e_k = 3 if k ≡ 0 or 2 mod 4 → level 32

**Type II — d=2 (w_K=2, p_K=2):**
- e_k = 0 if k odd → level 8
- e_k = 3 if k even → level 64

**Type III — d=3 (w_K=6, p_K=3):**
- e_k = 0 if k ≡ 1 mod 6 → level 3
- e_k = 1 if k ≡ 4 mod 6 → level 9
- e_k = 2 if k ≡ 0,2,3,5 mod 6 → level 27

**Type IV — d ∈ {7,11,19,43,67,163} (w_K=2, p_K=d odd):**
- e_k = 0 if k odd → level d
- e_k = 1 if k even → level d²

## 9×8 Table (e_k values)

```
        k=2  k=3  k=4  k=5  k=6  k=7  k=8  k=9
d=1      3    2    3    0    3    2    3    0
d=2      3    0    3    0    3    0    3    0
d=3      2    2    1    2    2    0    2    2
d=7      1    0    1    0    1    0    1    0
d=11     1    0    1    0    1    0    1    0
d=19     1    0    1    0    1    0    1    0
d=43     1    0    1    0    1    0    1    0
d=67     1    0    1    0    1    0    1    0
d=163    1    0    1    0    1    0    1    0
```

## LMFDB-verified entries (M85 live)

- **32.2.a.a** (d=1, k=2): level 32 ✓
- **4.5.b.a** (d=1, k=5): level 4 ✓ (M74's STATED e=2 was WRONG)
- **27.2.a.a** (d=3, k=2): level 27 ✓
- **49.2.a.a** (d=7, k=2): level 49 ✓
- **64.2.b.a** (d=2, k=2): level 64 ✓ (consistent with Type II e=3)

## Key NEW predictions (untested)

- **d=1, k=3 → level 16** (key test of Type I three-case correction)
- **d=3, k=4 → level 9** (first instance e_k=1 for d=3)
- **d=11, k=2 → level 121** (LMFDB has 33.2.d.a level 33 — twist-minimality check needed)
- **d=19, k=2 → level 361** (LMFDB has 95.2.g.a level 95 — same check)

## Honest verdict

- Publishability as M55 appendix: **~50%**
- As M74 sequel short note: **~25%**
- As standalone paper: **<10%**
- M75 F-3 verdict SCAFFOLD-EXISTS: **CONFIRMED**

## M88 LMFDB live verification (added 2026-05-06 ~16h30)

**4/4 PASS — table unchanged.** See `M88_LMFDB_VERIFY/SUMMARY.md`.

| Test | LMFDB confirmed |
|---|---|
| d=3 k=4 → 9 | 9.4.a.a, η(3z)⁸, CM Q(√-3) |
| d=1 k=3 → 16 | 16.3.c.a, η(4z)⁶, CM Q(i) |
| d=11 k=2 → 121 | 121.2.a.b twist-minimal CM Q(√-11) (coexists with 33.2.d.a) |
| d=19 k=2 → 361 | 361.2.a.a twist-minimal dim 1 CM Q(√-19) (coexists with 95.2.g.a dim 4) |

### Footnote required for Type IV

> *The formula e_k(K) gives the exponent for the canonical Hecke Grössencharakter of K with conductor supported only on primes above disc(K). When auxiliary primes enter the character (e.g. K=Q(√-11) with order-2 char at level 33; K=Q(√-19) with order-4 char at level 95), LMFDB additionally lists CM newforms at levels N = p_K^{e_k} · m² with m the auxiliary prime conductor. These coexist with and do not replace the canonical level-p_K^{e_k} form.*

## Discipline log

- Hallu count: **91 → 92** (M74 d=1 formula error caught by M85)
- M88 LMFDB verify: **92 → 92 (held)** — no further M85 errors
- Bash + Write blocked → return-as-text protocol
- Mistral STRICT-BAN observed
- 8 [TBD] markers; 4 RESOLVED via M88 (Tests 1-4 above)
- d=11, d=19 discrepancy resolved — both levels coexist independently
