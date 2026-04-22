# v7 Test 5 — Odlyzko zero-statistics vs CCM-predicted GUE deviations

**Date.** 2026-04-22.
**Commissioned.** Owner decision after Claude-app v3 (ZSA) audit: execute
the one falsifier that is computable locally within days.
**Test.** Does the empirical pair-correlation statistic of Riemann-zero
spacings deviate from pure Montgomery–Dyson GUE at finite height T in a
way compatible with the O(1/log T) corrections predicted by
Connes–Consani–Moscovici arXiv:2511.22755 (Euler-product truncation) ?

**Outcome matrix.**
- **Deviations confirmed, structured along the CCM prediction** →
  opens a v7 research track. ZSA survives as a serious programme.
- **Deviations confirmed but NOT matching the CCM prediction** →
  arithmetic structure beyond GUE exists but ZSA's specific mechanism
  is wrong; back to watchlist.
- **No deviations, pure GUE consistent within statistical error** →
  ZSA Test 5 falsified. ZSA track closed pending a different falsifier.

## Data

Odlyzko's public zero tables:
- [First 100 000 zeros](http://www.dtc.umn.edu/~odlyzko/zeta_tables/)
- [Zeros 10^21 to 10^21 + 10^4](http://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros3.gz)
  (if high-height sample needed)

The first 10^5 zeros suffice for a first-pass pair-correlation test;
they are ~5 MB download, straightforward to process.

## Methodology (standard)

Let {γ_n} be the imaginary parts of the non-trivial zeros.
Define normalised spacings:
  δ_n = (γ_{n+1} − γ_n) · (log γ_n) / (2π)
(the log γ_n / (2π) factor compensates for the slow increase of the
zero density at height T ≈ γ_n).

**Empirical pair-correlation:**
  R_2^{emp}(x) = (1/N) · #{(n,m) : n ≠ m,  δ_n + δ_{n+1} + … up to
  δ_m = x within tolerance Δx}

**Theoretical predictions to compare:**
- Pure Montgomery–Dyson GUE:
  R_2^{GUE}(x) = 1 − (sin(πx)/(πx))^2 + δ(x)
- CCM-truncated Euler product prediction: exact form requires reading
  arXiv:2511.22755 §§3–4 for the truncation-induced correction (not
  pre-computed here; agent must extract).

## Agent task

Execute in `derivations/V7-test5-odlyzko.py`:
1. Download Odlyzko's first 10^5 zeros (HTTPS).
2. Compute normalised spacings and empirical R_2^{emp}(x) on a grid.
3. Overlay GUE prediction and compute residual.
4. Read arXiv:2511.22755 §§3–4 via WebFetch to extract the specific
   form of O(1/log T) correction predicted; apply it as a candidate
   fit of the residual.
5. Compute χ² / degrees-of-freedom for:
   a. Pure GUE model.
   b. GUE + CCM correction (one free parameter if amplitude is free).
6. Produce plot `derivations/V7-test5-odlyzko.png`.
7. Write report `derivations/V7-test5-odlyzko-report.md` with verdict
   SHIP / REFUTED / INCONCLUSIVE.

**Honesty constraints (PRINCIPLES rule 1).**
- If arXiv:2511.22755 does not give an explicit functional form for the
  O(1/log T) correction, say so and report what *kind* of structured
  residual (if any) we see. No fabrication of CCM formula.
- If empirical R_2 is fully consistent with pure GUE (χ²/dof ≈ 1), the
  test is negative — do not manufacture a "signal".
- If a signal exists, quote statistical significance honestly.

## Execution plan

1. **Day 0 (now)**: launch agent. Budget: 1-3 hours wall-clock for
   first-pass on 10^5 zeros.
2. **Day 0–1**: review agent output. If verdict is SHIP, schedule an
   extended run on higher-height zeros (10^9 sample) for statistical
   power.
3. **Day 1–5**: if SHIP, produce a short research note
   `paper/_internal_rag/v7_test5_result.md` summarising verdict,
   zeroing in on which specific CCM prediction the data supports or
   excludes. Possible companion commit on derivations/ with full
   code + plots.

## What this test DOES NOT establish

- It does not prove or disprove the full ZSA framework.
- It does not validate the PH_k → HP or C_k → Σ log p substitutions
  (those are separate category errors, unrelated to the zero
  statistics).
- A positive result only means CCM's prediction survives at the level
  of zero spacings. The overall physical framework still requires the
  four corrective steps listed in the v3 audit.

## Gate before any v7 paper draft

Even with a positive Test 5, we do NOT draft a v7 paper until:
- D_ZSA = D_M ⊗ 1 + γ ⊗ H_ζ is rigorously constructed
  (auto-adjoint, compact resolvent, heat-kernel expansion) by an
  expert or via an extended agent programme.
- C_k vs Euler truncation is disambiguated.
- PH_k / HP substitution is replaced by a valid mathematical
  construction.
- Λ Euler–Maclaurin is explicitly computed.

Test 5 SHIP is necessary but not sufficient for a v7 paper.
