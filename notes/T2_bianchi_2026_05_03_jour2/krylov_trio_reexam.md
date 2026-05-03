# Krylov-Diameter Trio — Independent Re-examination

**Date:** 2026-05-03 | **Method:** arXiv API + HTML re-read of HPS/LL/Vardian; sympy (`/tmp/krylov_trio_reexam.py`); seven cross-searches on arXiv 2024-2026.

## arXiv re-verification

All three target papers exist and metadata matches the prior agent: 2412.17785v2 (HPS, PRL 135 151602), 2508.00056v1 (LL, 45 pp., Kosaki-disclaimer verbatim recovered), 2602.02675v1 (Vardian, OAQEC + modular Krylov).

## Independent verdict on T1–T6

| ID | Prior verdict | My verdict | Notes |
|---:|---|---|---|
| T1 | Fails: HPS contains no log-index | **AGREE** | HPS HTML re-read: zero hits for "Jones/subfactor/Kosaki/log index/type II/type III/Murray-von Neumann/FRW". HPS uses chord Hilbert space + transfer matrix, no operator-algebra machinery (no trace, no modular operator, no KMS state). |
| T2 | Fails: incompatible algebra types | **AGREE — sharper** | Vardian's central decomposition eq.(12) requires non-trivial centre Z(A); but A(D_O)_FRW (III_1) AND its crossed product N (II_∞) are both **factors**, so Vardian's "area = central element" identification trivialises to a c-number even before tensor-decomposition issues. |
| T3 | Fails: LL (4) is circular on FRW | **AGREE** | sympy check (`C3` in `.py`): substituting (4) gives `(1/log(M:N)) d log(M:N)/dt - (1/Vol) dVol/dt = 0` identically. Without an independent subfactor computation of `(A(D_O') : A(D_O))_FRW`, plugging (4) into the chain is purely a definition. LL §V applies to dS pole observers (II_1, CLPW), not to FRW comoving diamonds; FRW is never mentioned. |
| T4 | UOGH on II_∞ open | **AGREE** | arXiv search "UOGH"+"type II" → 0 hits 2024-2026. Search "operator growth"+"crossed product" → 0 hits. The gap is structural, not bibliographic. |
| T5 | Volume mismatch HPS↔LL | **AGREE** | HPS volume = AdS₂ Kruskal length L̂ (2D); LL volume = maximal-volume slice of AdS_d subregion. No paper bridges these to FRW R_proper(η_c). |
| T6 | Vardian OAQEC fails in II_∞ | **AGREE — sharpened** | Same as T2 sharpening: failure happens at the level of "is the algebra a factor?" not just "is it type I?". |

## arXiv 2024-2026 cross-search

Seven targeted queries, **all zero matches**: `"modular Krylov" AND "type II"`; `"spread complexity" AND "holographic index"`; `"Krylov complexity" AND "crossed product"`; `"Krylov" AND "Jones index"`; `"holographic complexity" AND "subfactor"`; `"UOGH" AND "type II"`; `"operator growth" AND "crossed product"`. Only Vardian itself matches `"modular Krylov"`.

**Closest non-bridging** (none closes T1–T6):
- arXiv:2511.03779 (Aguilar-Gutierrez et al., Nov 2025) — DSSYK type II_1 + Krylov of HH state; no crossed product, no FRW, no log-index.
- arXiv:2511.17711 (Krylov in canonical quantum cosmology, Nov 2025) — WdW/LQC, scalar-clock quadratic; no type II, no modular machinery.
- arXiv:2510.13986 (dS holographic complexity from DSSYK, Oct 2025) — extremal-timelike volume; explicitly NOT horizon/observer-algebra.
- arXiv:2506.03273 (Krylov in holographic CFTs, Jun 2025) — bulk reconstruction via radial momentum; no II_∞ FRW.

## Final verdict

**All 6 paths CONFIRMED failed.** The prior agent's reading of each paper is accurate (re-verified by direct HTML extraction), and two obstructions (T2 and T6) are actually **sharper** than stated — Vardian fails on factor algebras in general, not just type-II. T3 is verified algebraically by sympy (tautology of eq. (4)). No new 2024–2026 paper supplies a missing bridge. Restricted-class Block A1 (Theorem 4 conditional on UOGH transfer) remains the best available statement.

**No further closure attempt is warranted with these three papers.** The recommendation in `/tmp/krylov_trio_close.md` §6 (defensive-citation appendix; do not push) stands.
