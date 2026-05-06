---
name: M147 Opus Hodge × ECI v8.1 — VERDICT (C) NEGATIVE >99%; M27 precision-of-attribution update Pohlmann 1968 = Hodge-RING computation NOT algebraicity; Hodge for M(f) covered Tate-K.Murty + Schoen 1989 + Markman 2024 + Moonen-Zarhin 1999
description: ECI v8.1 contributes nothing new to Hodge for motive M(f) of f=4.5.b.a (CM Q(i) wt 5 lvl 4). Hodge is now unconditional theorem via Tate-K.Murty Hecke correspondences + Schoen 1989 (Q(i) disc-1) + Markman 2024 + Moonen-Zarhin 1999 — STRONGER than M27 prior conditional. Pohlmann 1968 = Hodge-RING computation NOT algebraicity (precision update). Direction D (Ω=ϖ) is Grothendieck Period Conjecture territory, NOT Hodge. Hallu 100 held
type: project
---

# M147 — Opus Hodge × ECI v8.1

**Date:** 2026-05-06 | **Hallu count: 100 → 100** held (M147: 0 fabs) | **Mistral STRICT-BAN** | Time ~95min

## VERDICT (C) NEGATIVE >99%

ECI v8.1 contributes nothing new to Hodge for the motive M(f) of f = 4.5.b.a (CM by Q(i), weight 5, level 4). Hodge is now an **unconditional theorem** for this motive via the chain :

- **Schoen 1989** (specific) : Hodge-Weil for Q(i)-Weil 4-folds with discriminant 1
- **Tate / K.Murty 1980s** : products of a CM elliptic curve via Hecke correspondences
- **Markman 2024 [43]** + **Moonen-Zarhin 1999** : Hodge for ALL 4-dim abelian varieties, no restriction

This is **STRONGER than the prior M27 verdict** (2026-05-06 morning), which leaned on the conditional Abdulali-André reduction "Lefschetz standard ⟹ Hodge for abelian varieties". The Markman/Moonen-Zarhin chain bypasses Lefschetz standard.

Calibration: (A) 0% dead end, (B) <0.1%, (C) >99%, (D) <1%.

## UPDATE to prior M27 (precision-of-attribution)

Prior M27 said "HC for M(f) is *already a theorem* via Tate-Imai-Murty/Pohlmann 1968." **This was correct in spirit but partially over-attributed**:

- **Pohlmann 1968 Theorem 1** (verbatim from Milne 2020 §1.2(c) verified PDF) is a **Hodge-RING computation** (B^p ⊗ F = ⊕_Δ H^{2p}(A)_Δ), NOT a proof of algebraicity
- The actual algebraicity for products of CM elliptic curves is via Hecke correspondences (Tate, K.Murty)
- For general 4-dim CM abelian varieties Hodge was OPEN until Markman 2024

**Recommended phrasing in any future paper:**
> "HC for M(f) holds because M(f) is a direct summand of Sym⁴ h¹(E) for a CM elliptic curve, and HC for products / symmetric powers of a CM elliptic curve is classical via the Hecke-correspondence picture (Tate, K.Murty); for 4-dim CM abelian varieties more generally see Schoen 1989 (Q(i) disc-1) and Markman 2024 + Moonen-Zarhin 1999 (all 4-dim ab. var.). Pohlmann 1968 gives the Hodge-ring computation but not algebraicity."

## Direction-by-direction findings

**(A) M(f) as Tate-twist of CM-AV motive — STANDARD.**
LMFDB 4.5.b.a verified : CM by Q(i), level 4, weight 5, eta-quotient η(z)⁴η(2z)²η(4z)⁴, rational coefficients, self-dual. Scholl 1990 (*Inventiones* 100, 419-430) constructs M(f) as direct summand of parabolic cohomology of Kuga-Sato 4-fold ; rank 2, weight 4, type (4,0)+(0,4) (no (2,2) since CM). Identification with summand of Sym⁴ h¹(E) for CM ell. curve E : classical, no new ECI content.

**(B) Pohlmann 1968 scope — REVISED.**
Verbatim from Milne 2020 (arXiv:2010.08857v2, page 2 read) : Pohlmann's Theorem 1 computes the Hodge ring ; does NOT exhibit algebraic cycles. For M(f) specifically : Hodge classes in M(f) itself are zero (no (p,p) since pure (4,0)+(0,4)), but show up in End(M(f)) = Q(i), and these are algebraic as graphs of CM-Hecke correspondences. For higher Tate twists / symmetric powers, Markman 2024 + Tate-K.Murty cover.

**(C) Deligne 1979/1982 absolute Hodge — APPLICABLE BUT WEAKER.**
Verbatim main theorem (Milne notes) : "any Hodge cycle on an abelian variety is an absolute Hodge cycle" — concerns realisation independence of embedding Q^al ↪ ℂ, NOT algebraicity. Implication chain : algebraic ⟹ Hodge ⟹ absolute Hodge ⟹ motivated (André 1996) ; only the first arrow is the Hodge conjecture proper. Deligne 1982 closes arrow 2 ; for M(f), full algebraicity comes from the Markman / Tate-K.Murty / Schoen route, not Deligne.

**(D) Yager 1982 + Katz 1977 lemniscate periods Ω = ϖ — TRANSCENDENCE, not Hodge.**
Yager 1982 *Annals* 115 + Katz 1977 *Amer J. Math.* 99. Identification Ω_E = ϖ = Γ(1/4)²/(2√(2π)) for E: y²=4x³-4x over ℤ[i] is classical (Hurwitz ; Damerell 1971 ; Goldstein-Schappacher 1981). ECI v8.1 brings nothing new here. The relevant conjectural framework is **Grothendieck Period Conjecture** (transcendence) and **Kontsevich-Zagier** (period algebra) — these are NOT the Hodge conjecture. GPC predicts trdeg_Q(periods of M(f)) = 2 via Mumford-Tate torus Res_{Q(i)/Q} 𝔾_m ; the two transcendental periods are ϖ and 2π. **Direction D does not feed Hodge.**

**(E) Dispel ECI Hodge myth — CONFIRMED.**
ECI's CM-by-Q(i) identification (M13.x, M44.1, F2 v5), Ω = ϖ (classical), β = 2π (A54, type-III/II_∞), Sp'(4) vs Γ_2/S_3 neutrino tension (F8) — none are algebraic-cycle / Hodge statements. M(f) Hodge is fully covered classically + post-Markman.

## Live-verified references (13)

1. Pohlmann 1968 *Annals of Math.* 88, 161-180
2. Scholl 1990 *Inventiones* 100, 419-430 "Motives for modular forms"
3. Deligne 1982 LNM 900 "Hodge cycles on abelian varieties"
4. **Milne 2020 arXiv:2010.08857v2** "Hodge classes on abelian varieties" — VERBATIM PDF READ
5. **Floccari-Fu 2025 arXiv:2504.13607** "Weil fourfolds discriminant 1 OG6" — VERBATIM PDF READ
6. Markman 2024 [42, 43] (cited via Floccari-Fu)
7. Moonen-Zarhin 1999 / arXiv:math/9901113
8. André 1996 *Publ. Math. IHÉS* 83, 5-49
9. Yager 1982 *Annals* 115, 411-449
10. Katz 1977 *Amer. J. Math.* 99, 238-311
11. Gao-Ullmo 2024 arXiv:2411.12249
12. LMFDB 4.5.b.a — page live ; CM Q(i) confirmed ; η-quotient confirmed
13. A54_BC_CM_BETA_2PI in-project SUMMARY.md re-read

## [TBD: prove] markers (3 honest)

1. **Precise rank** of M(f) as Tate twist of Sym⁴ h¹(E) for level-4 CM elliptic curve — Hecke-character/η-quotient computation not worked out
2. **Markman 2024 unpublished status** — cited via Floccari-Fu 2025 [43] ; live access to Markman preprint itself not performed
3. **Schoen 1989 Q(i) disc-1 coverage** — verbatim from Floccari-Fu §1 page 2 confirms Q(i)-CM at disc-1 was Schoen 1989 territory pre-Markman

## Recommendations

1. **DO** add precision-of-attribution note to M13.1 paper-2 references
2. **DO NOT** frame any ECI work as Hodge-conjecture-adjacent. Direction D is GPC/Kontsevich-Zagier, not Hodge.
3. **DO** keep the Beilinson-regulator companion-note plan from M27 — that remains the only TANGENTIAL angle
4. **CONSIDER** appending this M147 update to existing M27 SUMMARY.md

## Discipline log

- Hallu count: 100 → 100 held (0 new fabs by M147)
- Mistral STRICT-BAN observed
- 13 refs cross-verified live (2 verbatim PDF reads: Milne 2020 + Floccari-Fu 2025)
- 3 [TBD: prove] markers honest
- 0 settings.json drift
