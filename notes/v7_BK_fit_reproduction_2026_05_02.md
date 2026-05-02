# V7 BK-fit reproduction on Vast.ai — 10⁵ zeros baseline

**Date:** 2026-05-02
**Run:** during Levier #1B MCMC, on Vast.ai EPYC 7V13 contract 36023758
**Scripts:** `derivations/V7-test5-odlyzko.py`, `derivations/V7-BK-fit.py`
**Data:** Odlyzko zeros1 (100,000 zeros, T_max ≈ 74,921)

## v7-note baseline reproduced

| Model | χ² | dof | χ²/dof | p-value |
|---|---|---|---|---|
| **M0**  GUE only | 434.19 | 58 | **7.486** | 0 |
| M1  GUE+BK fixed (A=1, L fixed) | 690.85 | 58 | 11.911 | 0 |
| **M2**  GUE+BK free (A, L_eff free) | 233.68 | 56 | **4.173** | 0 |
| **M3**  GUE+BK + Cos(νx + φ) | 67.57 | 53 | **1.275** | 0.086 |

The **M2 fit χ²/dof = 4.173** matches the v7-note paper value **4.17** to four significant figures. Pipeline confirmed.

## New observation: M3 cosine extension is much better than BK alone

The M3 model (BK arithmetic correction + a single cosine modulation `C·cos(νx + φ)`) reduces χ²/dof from 4.17 to **1.27** with p-value 0.086. This is *statistically compatible with the empirical residual* at p > 5%, whereas M2 (BK alone) is rejected at very high significance.

F-test ladder:
- M2 → M3: F = 43.43, p = 2.6×10⁻¹⁴ (cosine highly favoured)
- M0 → M2: F = 24.02, p = 2.9×10⁻⁸ (BK highly favoured over GUE-only)
- M1 → M2: F = 54.78, p = 6.6×10⁻¹⁴ (free L favoured over fixed L)

M3 best-fit parameters:
- BK amplitude A = 0.353
- BK effective L = 6.42 (below L_mean = 8.505 from data)
- Cosine amplitude C = 0.031
- **Cosine frequency ν = 1.109**
- Cosine phase φ = 0.395

## Interpretation note

The cosine frequency ν = 1.109 is suggestive — close to 1 but not equal. In the unfolded mean-spacing variable, ν = 1 would correspond to a one-zero-per-cycle modulation. The slight deviation could be:
- A subleading correction to the Bogomolny-Keating formula not captured by the leading prime-pair sum
- A boundary artefact from the finite N=10⁵ window
- A genuine new modulation that v7-note's published M2 fit did not capture

## Action items for v7-note follow-up

1. **Publish M3 results explicitly** in a v7-note v0.2 or update. v0.1 (zenodo DOI 10.5281/zenodo.19983241) only reports the M2 χ²/dof = 4.17. The fact that adding ONE more mode (cosine) collapses the residual to χ²/dof = 1.27 is a significant scientific update.

2. **Test ν stability**: run the same fit on different sub-windows of the 10⁵ zeros (e.g., first 25,000, middle 50,000, last 25,000). If ν is genuinely ~1.109 across windows, it's a real signal. If it drifts, it's a finite-N artefact.

3. **Extension to higher T was attempted but blocked**: Odlyzko's `zeros2`-`zeros10` files do NOT contain consecutive low-T zeros (zeros1 is the only 10⁵-zero consecutive low-T file; subsequent files are at T ~ 10²¹ or higher with sparse coverage). To get 10⁶ consecutive low-T zeros for sharper BK fitting would require either:
   - Direct mpmath computation (slow, ~hours-days)
   - LMFDB API (faster, but rate-limited and may have its own format)
   - Trudgian or van de Lune lists (separate publications)
   
   Deferred as a future enhancement; the 10⁵ baseline is sufficient for the present claim.

## Files generated

- `/tmp/V7-test5-residuals.csv` — empirical R₂(x) - R₂_GUE(x) per bin (60 bins, x ∈ [0,3])
- `/tmp/V7_BK_fit_1M_results.json` — (only created if 10⁶ extension succeeds; not present this run)
- `derivations/V7-test5-odlyzko.png` — pair-correlation plot (symlinked to /home/remondiere/...)
- `derivations/V7-BK-fit.png` — fit visualisation
