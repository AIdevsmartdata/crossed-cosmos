---
name: M46 F5 falsifier executed — M28 anticyclotomic IMC paragraph FALSIFIED
description: 4 frameworks (Hsieh 2014 Documenta NOT Compositio, Chida-Hsieh 2015 Compositio, Arnold 2007 Crelle 606, Pollack-Weston 2011) explicitly EXCLUDE our case by hypothesis (p=2 ramified, k=5 odd, supersingular). Kriz 2021 has L-functions but NOT the IMC theorem. Replacement paragraph applied to M28 SUMMARY. Hallu 86 unchanged
type: project
---

# M46 — F5 falsifier executed (Phase 3.G follow-up, Opus, ~5min)

**Date:** 2026-05-06
**Owner:** Sub-agent M46 (Opus 4.7, math-NT, ~5min)
**Hallu count:** 86 → 86 (held; 4 papers triangulated via 5+ independent sources)
**Mistral:** STRICT-BAN observed

## Top-line verdict: M28 anticyclotomic IMC paragraph FALSIFIED

The M28_RIEMANN_HYPOTHESIS/SUMMARY.md paragraph (was lines 110-117) was **logically vacuous as written**. F5 caught it before propagation.

## Three-fold structural exclusion table

| Hypothesis | Hsieh 2014 | Chida-Hsieh 2015 | Arnold 2007 | P-W 2011 | f=4.5.b.a |
|---|---|---|---|---|---|
| p unramified in K | YES required | YES required | YES (split required) | YES (split or inert) | p=2 RAMIFIED — FAILS ALL |
| weight constraint | (Hecke chars) | p > k+1 | even weight | weight 2 | k=5 odd, p=2<6 — FAILS C-H, FAILS Arnold |
| ordinary at p | YES (CM ord) | YES required | supersingular OK if split | YES (ordinary) | p=2 ramified ⇒ supersingular ⇒ FAILS Hsieh, C-H, P-W |

## Verbatim hypothesis quotes

**Hsieh 2014** Theorem 1.3 (via arXiv:2412.10980 quote): *"p > 5 is prime to the minus part of the class number of K, to the order of χ, and is unramified in F/Q"*; Theorem A preamble: *"Assume that p does not ramify in K/Q."*

**Chida-Hsieh 2015** Assumption 1.1 (via arXiv:2603.22483 quote):
- (1) p ∤ N D_K c_f
- (2) T is ordinary at p
- (3) p > k+1 and #(F_p×)^(k-1) > 5
- (4) p is non-anomalous

**Arnold 2007** (Crelle 606 metadata): *"K is an imaginary quadratic field and p is a prime split in K"*, *"CM form f of even weight w ≥ 2 at a supersingular prime"*

**Pollack-Weston 2011**: N = N⁺N⁻ where N⁺ has only split primes, N⁻ has only inert primes. **NO ramified-prime slot** in framework.

## Kriz 2021 status

Kriz monograph (Princeton 2021) constructs **p-adic L-functions** for K imag-quad with p inert OR ramified — confirmed via book metadata. HOWEVER: provides ONLY analytic side. Algebraic side (Selmer characteristic ideal) + IMC theorem proper for p ramified, k odd, CM-by-K is **not in literature**. The phrase "extended via Kriz 2021 yields IMC" was research-gap handwave.

## Metadata corrections

- **Hsieh 2014** is in **Documenta Math.** vol. 19, 709-767, NOT *Compositio* as M44 falsifiers.md F5 noted. The *Compositio* paper is **Chida-Hsieh** joint 2015 vol. 151, 863-897 (arXiv:1304.3311).
- M44 falsifiers.md F5 protocol metadata corrected accordingly (parent task).

## Recommendations to parent (executed)

1. ✅ EDIT M28_RIEMANN_HYPOTHESIS/SUMMARY.md lines 110-117 with T5 replacement paragraph (honest [TBD: prove])
2. ✅ DO NOT propagate original paragraph to v7.6 §10 / paper-2 §6 Outlook
3. ✅ OPEN [TBD: prove] tracker: "Kriz-style anticyclotomic IMC extension to p ramified, k odd, CM-by-K"
4. ✅ RECORD F5 EXECUTED 2026-05-06 verdict FALSIFIED in M44 falsifiers.md
5. ✅ CORRECT F5 protocol metadata Hsieh = Documenta NOT Compositio

## Live-verified sources (8)

- arXiv:1304.3311 — Chida-Hsieh 2015 *Compositio* 151
- math.ntu.edu.tw/~mlhsieh/research/AIMC.pdf — Hsieh 2014 author webpage
- arXiv:2412.10980 — verbatim Hsieh Theorem 1.3 quote
- arXiv:2603.22483 — verbatim Chida-Hsieh Assumption 1.1 quote
- degruyterbrill.com Crelle 606 — Arnold 2007 metadata
- math.bu.edu/people/rpollack — Pollack-Weston 2011 PDF
- barnesandnoble.com — Kriz 2021 monograph metadata
- Hsieh-Chida 2015 abstract triangulation (BD definite quaternion → Heegner split)

## Discipline
- 0 fabrications
- Mistral STRICT-BAN
- 4 paper hypotheses cross-verified via 5+ independent sources
- NO drift to settings.json (anti-stall ✅ despite explicit injection)
- Sub-agent return-as-text protocol used (parent saved)
- WIN: F5 falsifier worked exactly as designed — caught vacuous claim before propagation
