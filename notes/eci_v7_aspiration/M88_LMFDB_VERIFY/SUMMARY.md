---
name: M88 LMFDB live verify M85 critical predictions — 4 PASS, table STANDS
description: Test 1 d=3/k=4 → 9.4.a.a CM Q(√-3) PASS (first e_k=1 d=3 confirmed). Test 2 d=1/k=3 → 16.3.c.a CM Q(i) PASS (validates 3-case d=1 correction). Test 3 d=11 PASS+footnote (33.2.d.a and 121.2.a.b independently twist-minimal). Test 4 d=19 PASS+footnote (95.2.g.a dim4 vs 361.2.a.a dim1 different chars). M85 unified table unchanged. Hallu 92 → 92 held
type: project
---

# M88 — LMFDB live verify M85 critical predictions (D4-#1 follow-up)

**Date:** 2026-05-06 | **Hallu count: 92 → 92** (held — no M85 errors detected)

## VERDICT: M85 unified table STANDS — 4/4 LMFDB live PASS

| Test | d | k | M85 pred | LMFDB | Verdict |
|---|---|---|---|---|---|
| 1 | 3 | 4 | level 9 | **9.4.a.a** CM disc −3 | **PASS** |
| 2 | 1 | 3 | level 16 | **16.3.c.a** CM disc −4 | **PASS** |
| 3 | 11 | 2 | level 121 | **121.2.a.b** twist-min CM −11 | **PASS + footnote** |
| 4 | 19 | 2 | level 361 | **361.2.a.a** twist-min CM −19 dim 1 | **PASS + footnote** |

## Test 1 — d=3, k=4 → level 9 (KEY NEW PREDICTION)

**LMFDB label: `9.4.a.a`**
- has_cm: true, CM by Q(√-3)
- Character: trivial (orbit 9.a)
- η-quotient: **η(3z)⁸**
- Twist minimal: yes
- Sato-Tate: N(U(1))
- Dimension 1, coefficient field ℚ

**Implication:** First confirmed instance of e_k=1 for d=3 (k=4 ≡ 4 mod 6). Strongest single corroboration of M85's d=3 row + 3-case correction.

## Test 2 — d=1, k=3 → level 16

**LMFDB label: `16.3.c.a`**
- has_cm: true, CM by Q(i)
- Character: 16.c (order 2, minimal)
- η-quotient: **η(4z)⁶**
- Twist minimal: yes
- Sato-Tate: U(1)[D₂]

**Implication:** Validates d=1 three-case correction. M74 had only 2 cases for d=1; M85's k=3 case → level 16 = 2⁴ = (1+i)^{e_k} N_K = 4·4 confirmed.

## Test 3 — d=11 (level 33 ↔ 121 BOTH exist independently)

Both `33.2.d.a` and `121.2.a.b` are CM by Q(√-11), both twist-minimal:

**33.2.d.a:** char order 2 (orbit 33.d), conductor 33 = 3·11, inner twists × 4
**121.2.a.b:** char trivial, conductor 121, inner twists × 2 (trivial + CM)

Twists tables show NO overlap. They are different Hecke Grössencharakters: `33.2.d.a` involves auxiliary prime 3 in the character; `121.2.a.b` uses minimal-conductor character only at p=11.

## Test 4 — d=19 (level 95 ↔ 361 BOTH exist, dimension argument decisive)

**95.2.g.a:** char order **4**, dim **4** (rel. dim 2 over Q(i)), Sato-Tate U(1)[D₄], coef field Q(i, √19)
**361.2.a.a:** char trivial, dim **1**, coef ℚ, analytic rank 1

A quadratic twist preserves dim. Dim 4 ≠ Dim 1 → cannot be twists. Different Grössencharakters: `361.2.a.a` minimal at p=19; `95.2.g.a` uses order-4 character with auxiliary prime 5.

Level 361 also contains `361.2.c.b` (CM Q(√-19), order 3, dim 2) — third independent CM form.

## Required footnote for M85 Type IV

> *"The formula e_k(K) gives the exponent for the canonical Hecke Grössencharakter of K with conductor supported only on primes above disc(K). When auxiliary primes enter the character (e.g. K=Q(√-11) with order-2 char at level 33; K=Q(√-19) with order-4 char at level 95), LMFDB additionally lists CM newforms at levels N = p_K^{e_k} · m^2 (m = auxiliary prime conductor). These coexist with and do not replace the canonical level-p_K^{e_k} form."*

## Discipline log

- 0 fabrications
- All 4 LMFDB lookups successful at live API + web
- η-quotients verbatim (η(3z)⁸ for 9.4.a.a, η(4z)⁶ for 16.3.c.a)
- Mistral STRICT-BAN observed
- Hallu 92 → 92 (held)
