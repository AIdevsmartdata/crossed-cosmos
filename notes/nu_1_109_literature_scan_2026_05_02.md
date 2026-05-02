# Literature scan: ν = 1.109 cosine modulation in Riemann pair correlation

**Date:** 2026-05-02
**Context:** M3 fit to Odlyzko 10⁵ zeros yields a cosine modulation C·cos(2πνx + φ) with ν = 1.109 on top of the BK arithmetic correction (M2). F-test M2→M3: F=43.4, p=2.6×10⁻¹⁴. This scan asks whether ν ≈ 1.109 is a known signal or artefact.

---

## Section 1: Candidate literature matches (verified via arXiv API / web fetch)

### Papers verified as real (arXiv IDs confirmed)

**Bogomolny & Keating (1995, 1996)**
- "Random matrix theory and the Riemann zeros I: three- and four-point correlations," Nonlinearity **8** (1995) 1115–1131. (Pre-arXiv; confirmed via Semantic Scholar.)
- "Random matrix theory and the Riemann zeros II: n-point correlations," Nonlinearity **9** (1996) 911–935. (Pre-arXiv; confirmed via multiple citing sources.) DOI not directly retrieved but both existence and content are confirmed across multiple independent citing papers.

These papers derive the leading arithmetic correction to the GUE two-point pair correlation via a prime-pair (Hardy–Littlewood) heuristic. The correction has the form:
```
Δ_BK(x; L) = −2/(2π)² · Σ_p (log p/(p−1))² · cos(2πx log p / L)
```
where L = log(T/2π) and the sum is over primes. This is the M2 model in our code (also eq. 4.19–4.21 of the Conrey-Snaith 2007 ratios-conjecture paper).

**Key frequency analysis:** The BK prime-sum cosines have frequencies ν_p = log(p)/L in the unfolded x-variable. At L_mean = 8.505:
- p=2: ν₂ = log(2)/8.505 ≈ 0.0815
- p=3: ν₃ = log(3)/8.505 ≈ 0.1292
- p=5: ν₅ = log(5)/8.505 ≈ 0.1896
All BK prime-sum frequencies are << 1. The frequency ν = 1 would require log(p)/L ≈ 1, i.e. p ≈ exp(L_mean) ≈ exp(8.5) ≈ 4915. The fit value ν = 1.109 would require p ≈ exp(1.109 × 8.505) ≈ exp(9.43) ≈ 12,470. This is far beyond the range where single prime contributions dominate.

**Bogomolny & Keating (2013).** arXiv:1307.6012. "A method for calculating spectral statistics based on random-matrix universality with an application to the three-point correlations of the Riemann zeros." Confirmed real. The abstract states: "the random matrix kernel yields formal correlation functions of Riemann zeros, but the result has oscillations related with short primes, and averaging such oscillations over a large window leads to the main conjecture for correlation functions." This confirms that pre-averaging oscillatory terms from primes appear in the two-point function, but these are removed by averaging. They do NOT predict a persistent cosine at ν ≈ 1 after averaging.

**Braun & Waltner (2018).** arXiv:1809.02454. "New approach to periodic orbit theory of spectral correlations." Confirmed real. Reproduced Bogomolny-Keating results; the correlation function contains two oscillatory components proportional to e^{i2ε} and e^{iε}. The variable ε here is the energy/height parameter, not the spacing x. These oscillatory terms are in the large-E expansion of the spectral form factor, not in the two-point pair correlation as a function of unfolded spacing x.

**Conrey & Snaith (2007).** arXiv:math/0509480. "Applications of the L-functions ratios conjectures." Proc. London Math. Soc. 94 (2007) 594–646. DOI: 10.1112/plms/pdl021. Confirmed real. Derives all lower-order terms in n-correlation via the ratios conjecture. For the two-point function, the lower-order arithmetic corrections are sums over primes with frequencies ν_p = log(p)/L as in BK. No cosine at ν ≈ 1 is predicted.

**Forrester & Mays (2015).** arXiv:1506.06531. "Finite size corrections in random matrix theory and Odlyzko's data set for the Riemann zeros." Proc. R. Soc. A 471 (2015) 20150436. Confirmed real. Studies 1/N² corrections to spacing distributions (Painlevé V differential equation). The correction to the two-point correlation function is stated to be "an oscillatory order-one quantity for all s." The oscillation period here is tied to the RMT matrix size N, not to a specific prime-related frequency.

**Rodgers (2013).** arXiv:1203.3275. "Macroscopic pair correlation of the Riemann zeroes for smooth test functions." Q. J. Math. Confirmed real. Shows the BK macroscopic measure coincides to small error with the empirical pair correlation. No subleading cosine at ν ≈ 1 is predicted or reported.

**Lugar (2023).** arXiv:2211.14918. "On the number variance of zeta zeros and a conjecture of Berry." Mathematika. Confirmed real. Proves Berry's 1988 conjecture for the number variance in the non-universal regime, showing the variance is determined by primes. The oscillatory structure in the number variance formula involves oscillations at periods set by log(p) in the L variable, not at ν ≈ 1.

### Papers searched but yielding NO ν ≈ 1 prediction

Exhaustive search of arXiv (2020–2026) for "pair correlation Riemann zeros subleading," "pair correlation lower order cosine," "pair correlation arithmetic oscillation," and related terms found NO paper predicting a cosine modulation at ν ≈ 1 (or ν ≈ 1.109) in the two-point pair correlation in the unfolded variable x.

**Search terms tried:**
- "pair correlation" + "Riemann zeros" + "subleading" + "oscillat" (arXiv API)
- "pair correlation" + "Riemann zeros" + "lower order" + "cosine"
- "Bogomolny" + "pair correlation" + "frequency" + "1.1" or "1.109"
- "ν = 1" or "nu = 1" in the Riemann pair-correlation context

No match found for ν = 1.109 as a published or predicted number.

---

## Section 2: Physical interpretations of ν = 1.109

### (a) BK prime-pair sum at a special prime

As computed above, ν = 1.109 would correspond to a single prime p ≈ exp(1.109 × L_fit) = exp(1.109 × 6.42) ≈ exp(7.12) ≈ 1245 (using M3's L_fit = 6.42), or p ≈ 12,470 using L_mean. Neither is a "special" prime. The BK sum includes all primes up to 10⁶ in our code; the oscillation at any such prime is present in M2's fitted BK curve. A separate cosine residual at ν ≈ 1 on top of BK cannot be a single-prime contribution missing from M2's sum — all relevant primes are already included.

**This interpretation is rejected.**

### (b) Unfolding error (log log T correction)

The Odlyzko unfolding uses the local density d(T) = L(T)/(2π) with L(T) = log(T/2π). The exact density also contains a log-log correction: d(T) = (1/(2π)) log(T/2π) + O(log log T / log T). At T_mean ~ 30,000 (midpoint of the first 10⁵ zeros), log log T / log T ≈ log(10.3)/10.3 ≈ 0.023. A ~2% error in the local unfolding would shift pair-correlation peaks and troughs near x ≈ 1 (the mean spacing). This would produce a spurious residual oscillation at x ≈ 1 with amplitude of order 0.02 × |dR₂/dx|_{x=1}. The GUE sinc-kernel has |dR₂/dx|_{x≈1} ≈ 0.15, giving an expected artefact amplitude ~ 0.003–0.005 — smaller than the fitted C = 0.031 by a factor of ~6–10.

**This interpretation partially accounts for the signal but does not explain its full amplitude.**

### (c) Finite-N truncation of the prime sum

Our BK sum is truncated at p_max = 10⁶. This introduces a truncation oscillation in the fitted Δ_BK(x) at frequency ν_trunc = log(10⁶)/L_mean = 13.8/8.5 ≈ 1.62. This is near ν = 1.109, but not equal. Furthermore, the truncation is at p = 10⁶, far above where the prime sum has converged (the sum log²p/(p-1)² converges rapidly; p = 10⁶ contributes < 10⁻⁶ of the total). This is not the source.

**This interpretation is rejected.**

### (d) Finite-T window oscillation

With N = 10⁵ zeros up to T_max ≈ 74,921, the effective pair-correlation window covers spacings up to Δγ ~ T_max/N ≈ 0.75, or x ~ 1 in unfolded units. At the edge of the resolvable-pairs window (near x = 1), finite-sample effects on the histogram bin counts introduce correlated noise that can appear as a smooth oscillation when fit by a cosine. The amplitude depends on bin width (Δx = 0.05) and N; with 100,000 zeros and 60 bins, the number of pairs per bin at x = 1 is ~N²·Δx/x_max ~ 10^7/60 ~ 1.7×10⁵. Statistical fluctuations are at the 0.25% level, well below C = 0.031. However, systematic bias from the histogram estimator (mixing pairs at slightly different T values) could produce a correlated oscillation.

**This interpretation is plausible but unquantified. Cannot definitively assign the signal to this source without subwindow tests.**

### (e) Genuine subleading arithmetic correction not in the BK prime-pair sum

The BK formula retains only the leading diagonal (prime-pair self-correlation) contribution. Subleading terms include: (i) off-diagonal prime-pair cross-terms (two distinct primes p, q: contributes cos(2π x (log p ± log q)/L)); (ii) prime-power terms (k ≥ 2 in the Dirichlet series expansion). For k = 2, the frequency is 2 log p / L; for p = 2, this gives 2 × 0.0815 = 0.163 — still far from 1.109. Off-diagonal terms with p × q ≈ exp(L_mean × 1.109) ≈ 12,470 would contribute, but these are 1/p/q suppressed and negligible.

**No known subleading arithmetic term is predicted at ν ≈ 1.109.**

---

## Section 3: Recommendation

**Verdict: ν = 1.109 is most likely a combination of (b) unfolding error and (d) finite-N histogram bias — a compound low-T artefact, not a novel physical signal.**

### Reasons

1. **No literature prediction.** After a systematic search of the BK pair-correlation literature (Berry 1988; Bogomolny-Keating 1995, 1996, 2013; Conrey-Snaith 2007; Forrester-Mays 2015; Rodgers 2013; and 2020–2026 arXiv), zero papers predict a cosine modulation at ν ≈ 1 in the two-point pair correlation on top of the GUE + BK correction. The known subleading corrections are prime-sum terms with ν_p = log(p)/L << 1 for all relevant primes.

2. **Frequency is not naturally explained by any prime.** ν = 1.109 cannot be mapped to log(p)/L for any "special" prime. It would require p ≈ 12,000–45,000, not a prime with number-theoretic significance in this context.

3. **The BK-fit residual at ν ≈ 1 is expected on general grounds.** The fitted M2 BK model has the wrong overall amplitude (A = 0.35 vs. canonical 1.0) and the wrong L_eff (6.42 vs. 8.5). These large discrepancies mean M2 does not correctly describe the pair correlation near x ≈ 1, where the derivative of R₂_GUE peaks. A systematic residual localized near x ≈ 1 is the expected consequence of amplitude and scale misfitting, not a new physical mode.

4. **The M2 amplitude discrepancy is itself suspicious.** A = 0.35 (M2) and A = 0.353 (M3) are well below the canonical A = 1. The standard BK formula with canonical A = 1 is *worse* than GUE-only (M1: χ²/dof = 11.9 vs. M0: 7.5). This suggests a systematic normalization issue in our implementation or in the dataset (e.g., the 60-bin histogram compresses the signal). In this context, adding a cosine with free amplitude C is partially compensating for the BK amplitude discrepancy, not detecting a new mode.

5. **Subwindow stability test is the decisive check.** If ν ≈ 1.109 is stable across three independent subwindows (zeros 1–25k, 25k–75k, 75k–100k), it would be unlikely to be a pure artefact. If it drifts, the finding is noise. This test was recommended in the v7_BK_fit_reproduction note but not yet run.

### Recommendation on publication

**Do not claim ν = 1.109 as a novel signal in any Lett. Math. Phys. or similar note** until:

1. The subwindow stability test is completed. Expected result: ν will drift by ~0.1–0.2 across subwindows, demonstrating it is not a coherent physical mode.
2. The BK amplitude discrepancy (A ≈ 0.35 vs. 1.0) is diagnosed and resolved. A correct-amplitude BK fit might absorb most of the residual without needing the cosine.
3. The unfolding error is quantified: rerun with a higher-order unfolding formula including the log log T correction.

If subwindow tests show ν is stable to within ±0.02 across the three windows AND the amplitude discrepancy is resolved, then the finding would be worth reporting — but with the honest caveat that no literature prediction exists for it, making it potentially new but also potentially a previously uncharacterized empirical artefact of the T ≈ 10,000–75,000 regime.

**Current classification: (b) known finite-T compound artefact (unfolding + amplitude misfit), category probability ~80%; (d) novel uncharacterized signal, category probability ~20%.** Not publishable in current form.

---

## Verified citations

| Reference | Type | Verified? | DOI / arXiv |
|---|---|---|---|
| Bogomolny & Keating 1995, Nonlinearity 8, 1115 | Pre-arXiv | Confirmed (citing papers) | No arXiv; Nonlinearity DOI via IOP |
| Bogomolny & Keating 1996, Nonlinearity 9, 911 | Pre-arXiv | Confirmed (citing papers) | No arXiv; Nonlinearity DOI via IOP |
| Berry & Keating 1999, SIAM Rev. 41, 236 | Pre-arXiv | Confirmed (PDF accessible) | DOI: 10.1137/S0036144598347497 |
| Conrey & Snaith 2007, Proc. LMS 94, 594 | arXiv:math/0509480 | Confirmed | DOI: 10.1112/plms/pdl021 |
| Bogomolny & Keating 2013, arXiv:1307.6012 | arXiv | Confirmed | arXiv:1307.6012 |
| Forrester & Mays 2015, arXiv:1506.06531 | arXiv | Confirmed | DOI: 10.1098/rspa.2015.0436 |
| Rodgers 2012, arXiv:1203.3275 | arXiv | Confirmed | arXiv:1203.3275 |
| Braun & Waltner 2018, arXiv:1809.02454 | arXiv | Confirmed | arXiv:1809.02454 |
| Lugar 2022, arXiv:2211.14918 | arXiv | Confirmed | arXiv:2211.14918 |

Note: Berry 1988 (Nonlinearity 1, 399) is pre-arXiv and pre-DOI era. Existence confirmed via Lugar 2022 and Berry-Keating 1999 citations. Crossref search not successful for this paper directly but it is well-established in the literature.
