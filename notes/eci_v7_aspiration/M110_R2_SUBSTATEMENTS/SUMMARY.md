---
name: M110 R-2.1 + R-2.3 LaTeX subsections — ready-to-paste, FE+Bernoulli aware, M22 ladder explicit
description: 2 LaTeX subsections written (~85L R-2.1 + ~100L R-2.3 + 3 bibitems) ready for r2_blochkato_paper.tex. R-2.1 = full BK Tamagawa formula α_m = c_2·c_∞/#H^1_f, blocked by 5 GAPS. R-2.3 = SEMI-INDEPENDENT, FALSIFIABLE, predicts v_2(c_2(m))-v_2(#H^1_{f,2}(m)) = v_2(α_m^F1) ∈ {-3,-2,0,+1}. Most accessible test: m=3 exact 2-adic balance. LVW25 title 1 unverified watch
type: project
---

# M110 — R-2.1 + R-2.3 sub-statements LaTeX subsections

**Date:** 2026-05-06 | **Hallu count: 94 → 94 held** | **Mistral STRICT-BAN observed**

## TL;DR

Wrote 2 LaTeX subsections ready to paste into `r2_blochkato_paper.tex` (M70 paper):
- **R-2.1** (~85 lines): full Bloch-Kato Tamagawa formula with explicit product structure for m∈{1,2,3,4}; documents 3 simultaneous obstructions (5 GAPS per M86/M90)
- **R-2.3** (~100 lines): 2-adic valuation lattice (M22 fingerprint) — **SEMI-INDEPENDENT and FALSIFIABLE**

## Critical insight (R-2.3 vs R-2.1)

**R-2.3 is semi-independent from R-2.1 and falsifiable BEFORE the full IMC.**

R-2.1 requires anticyclotomic IMC at p=2 ramified (timeline 5-10y, 3 simultaneous obstructions).
R-2.3 only requires:
- TBD-R2-1: bound v_2(c_2(m)) from local Tate cohomology
- TBD-R2-2: bound v_2(#H^1_{f,2}(m)) from Rubin-style CM descent

If both bounds tight + constraint v_2(c_2)−v_2(Sha_2) = v_2(α_m^F1) fails for ANY single m → R-2.3 REFUTED. **Most accessible entry: m=3**, predicts v_2(c_2(3)) = v_2(#H^1_{f,2}(3)) exact 2-adic balance.

This makes R-2.3 a **concrete falsifier** for BK Tamagawa in Steinberg-ramified regime — much more testable than R-2.1.

## R-2.1 product structure (predicted)

For α_m ∈ {1/10, 1/12, 1/24, 1/60} :

| m | c_2 · c_∞ / #H^1_f predicted = | Prime factors |
|---|---|---|
| 1 | 1/(2·5) | 2, 5 |
| 2 | 1/(4·3) | 4, 3 |
| 3 | 1/(8·3) | 8, 3 |
| 4 | 1/(4·3·5) | 4, 3, 5 |

Prime 5 at m=1, 4 ; prime 3 at m=2, 3, 4 ; 2-adic structure → R-2.3.

## R-2.3 M22 ladder (RIGOROUS computation)

Steinberg renormalization: E_2^±(f, m) = (-2^{m-1})(1 + 2^{m-3})

| m | α_m | E_2^±(f,m) | α_m^F1 | v_2(α_m^F1) |
|---|---|---|---|---|
| 1 | 1/10 | -5/4 | -1/8 | **-3** |
| 2 | 1/12 | -3 | -1/4 | **-2** |
| 3 | 1/24 | -8 | -1/3 | **0** |
| 4 | 1/60 | -24 | -2/5 | **+1** |

Sequence {-3, -2, 0, +1} = **strictly monotone**, M22 fingerprint, unique to F1 among 8 renormalizations tested (M22).

## Pollack 2003 (Duke 118, 523-558) interaction

3 modifications needed for k=5 + p=2 ramified Steinberg:
1. **a_2 = -4 ≠ 0** (Steinberg edge, not supersingular) → factor (1+2^{m-3}) corrects
2. **Weight k=5 vs Pollack's k=2** → Wach module Berger 2004
3. **Anticyclotomic vs cyclotomic** → Damerell-Shimura Rankin-Selberg identity

Primary reference for closure: Fan-Wan arXiv:2304.09806 §3-4 (handles p=2 ramified ±-Dieudonné module, but only weight-2 self-dual CM chars).

## 5 GAPS (M86/M90 confirmed) summarized

3 simultaneous obstructions to R-2.1:
- (I) Odd weight k=5 (LVW25 needs ℓ ∈ ℤ; ℓ=3/2 ∉ ℤ FAIL)
- (II) p=2 ramified in K=Q(i) (Fan-Wan only weight-2 CM)
- (III) ord_2(N) = 2 (BN26 needs ord_p(N) ≤ 1 FAIL)

19 papers verified live arXiv (M86+M90), no framework resolves all 3. Probability formal R-2.1 contribution: 5-10%.

## LaTeX integration plan

**Target file** : `/root/crossed-cosmos/notes/eci_v7_aspiration/M70_R2_PAPER/r2_blochkato_paper.tex`

**Replace** :
- existing `\subsection{Conjecture R-2.1}` (lines ~328-363) with R-2.1 block (~85L)
- existing `\subsection{Conjecture R-2.3}` (lines ~401-426) with R-2.3 block (~100L)

**Add** 3 bibitems:
- Pollack 2003 Duke 118, 523-558 (verified per memory)
- LPV 2603.22483 (verified M90)
- LVW25 arXiv:2501.03673 (title FLAGGED — needs WebFetch verify before final submit)

**Macros** : `\tbdtag{N}{...}` already defined preamble line 44

## Hallu watch

- **LVW25 arXiv:2501.03673 title** : flagged unverified by M110. M86 SUMMARY says "Generalized Rubin formula for Hecke characters". Need WebFetch live verify before paste.

## Discipline log

- 0 new arXiv citations introduced beyond M70/M86/M90 verified
- Pollack 2003 memory-verified (DOI 10.1215/S0012-7094-03-11835-9)
- LVW25 title flagged WARNING in bibitem
- Mistral STRICT-BAN observed
- Hallu 94 → 94 held
