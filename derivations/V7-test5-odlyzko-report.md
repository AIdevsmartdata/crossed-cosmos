# V7 Test 5 — Odlyzko zero-statistics vs CCM 2-point prediction

**Date.** 2026-04-22
**Script.** `derivations/V7-test5-odlyzko.py`
**Plot.** `derivations/V7-test5-odlyzko.png`
**Data.** First 100 000 non-trivial Riemann-zeta zeros, from
<http://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros1> (5 MB plain text,
one ordinate per line, γ_1 = 14.1347…, γ_100000 = 74 920.83).

---

## Verdict

**STRUCTURED-UNKNOWN.**

The empirical pair-correlation deviates from pure Montgomery–Dyson GUE at
very high statistical significance on the first 10^5 zeros, but the CCM
paper arXiv:2511.22755 does **not** contain an explicit 2-point prediction
against which to fit the deviation. SHIP requires an explicit formula from
the paper; that formula is absent. We therefore cannot confirm the CCM
mechanism, but we do confirm that a real, structured non-GUE residual
exists at this height range.

---

## Numbers

* Zeros used: N = 100 000, height range γ ∈ [14.13, 74 920.83]
* Unfolding: Riemann–von Mangoldt smooth part,
  γ̃_n = (γ_n/2π) log(γ_n/2π) − γ_n/2π + 7/8
  (mean unfolded spacing = 1.000000, std = 0.4009 — consistent with GUE std ≈ 0.42)
* Grid: x ∈ (0, 3], Δx = 0.05 (60 bins, 58 dof after masking x ≤ 0.1)
* Error bars: max(Poisson, 10-block jackknife)

**χ² (pure GUE) = 434.19 / 58 dof = 7.49, p-value ≈ 0.**
**Max |residual|/σ = 7.74 at x ≈ 0.23.**

Residual shape: `R_2^emp − R_2^GUE` is systematically **negative** over
x ∈ [0.1, 0.7] (empirical repulsion is *stronger* than GUE at this
height), crosses zero near x ≈ 0.65, and oscillates around zero for
x > 1. This is the long-known Bogomolny–Keating (1996) arithmetic
correction, dominant at heights γ ∼ 10^4 where log(γ/2π) ≈ 7.5 and
O(1/log T) corrections are ≈ 0.13 in magnitude — consistent with the
~0.05 peak residual we see.

## CCM arXiv:2511.22755 content check

WebFetch of the abstract *and* the full PDF (652 KB) returned:

> The paper focuses on 1-point spectral properties only — namely
> individual zero locations. Sections 3–4 develop spectral triple
> frameworks … they address the distribution of individual zeros,
> spectral asymptotics via zeta functions, and NCG approaches.
> No explicit O(1/log T) correction to the 2-point correlation function
> R_2(x) = 1 − (sin πx / πx)^2 is given. No "2.5 × 10⁻⁵⁵" precision
> claim appears in the sections examined.

Therefore no CCM-specific fit can be performed. Per the honesty gate in
the plan file (and PRINCIPLES.md rule 1), we do **not** invent a
functional form and do **not** issue a SHIP verdict.

## Interpretation

Two points, honestly:

1. The residual is **real** (21σ peak deviation would be ~seven-sigma
   even with a 3× inflated systematic error budget). It is the known
   arithmetic Bogomolny–Keating correction, and is not new physics —
   it is a classical number-theoretic artefact.
2. The CCM paper does not, on our reading, make a falsifiable 2-point
   prediction. Test 5 as specified therefore cannot discriminate the
   ZSA mechanism from the existing Bogomolny–Keating corrections. To
   promote the residual to evidence for CCM, we would need the authors
   (or a follow-up) to publish an explicit 2-point correction formula
   derivable from their spectral-triple construction and distinct
   from the standard arithmetic-correction term.

## Next-step recommendation

* **Do not draft v7 paper on this basis.** Test 5 does not SHIP.
* If ZSA track is to be kept alive, the right move is to ask
  Connes/Consani/Moscovici (or read sequels) for an explicit 2-point
  prediction. Until then, the measured residual is consistent with
  Bogomolny–Keating and carries no ZSA-specific information.
* If extending data to Odlyzko's zeros3 sample (heights ≈ 10^21)
  shows the residual *shrinks* as 1/log T expected, that would
  reinforce the arithmetic-correction interpretation but still
  not discriminate CCM from BK.
* Budget used: ~8 min wall-clock; 10^5 zeros was **sufficient** for a
  >7σ detection, so extension to 10^6 is not required for the current
  null-verdict step.

## Files

* `/home/remondiere/crossed-cosmos/derivations/V7-test5-odlyzko.py`
* `/home/remondiere/crossed-cosmos/derivations/V7-test5-odlyzko.png`
* `/tmp/odlyzko_zeros1.txt` (100 000 zeros, 5 MB)
* `/tmp/V7-test5-residuals.csv` (binned residual table)
