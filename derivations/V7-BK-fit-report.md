# V7 BK-fit — Explicit Bogomolny-Keating fit to Odlyzko 10⁵ residual

**Date.** 2026-04-22
**Script.** `derivations/V7-BK-fit.py`
**Plot.** `derivations/V7-BK-fit.png`
**Input.** `/tmp/V7-test5-residuals.csv` (60 bins, Δx = 0.05, x ∈ (0, 3]).

---

## Verdict

**BK-PLUS-EXTRA.**

The Bogomolny–Keating (1996) arithmetic correction captures about half
the empirical residual variance. A free-amplitude BK fit reduces
χ²/dof from 7.49 (pure GUE) to 4.17, a highly significant improvement
(F-test p ≈ 3 × 10⁻⁸). However, the BK-only model is still a bad
fit (χ²/dof = 4.2, p ≈ 0). A single extra cosine term at frequency
ν ≈ 1.11 captures the rest and brings χ²/dof to 1.27 (p ≈ 0.086 —
acceptable). So the residual is **dominantly BK but with a coherent
non-BK oscillation at ν ≈ 1**.

---

## Formula used

The BK scaled two-point arithmetic correction, in the form derived
from Conrey-Snaith / Snaith 2010 review eq. (4.19)-(4.21) (equivalent
to Bogomolny-Keating 1996 after r-integration over the saddle at
r = 0), and quoted in Berry-Keating 1999 "The Riemann Zeros and
Eigenvalue Asymptotics" (Rev. Mod. Phys.) near eq. (49):

    Δ_BK(x; L) = − (2 / (2π)²) · Σ_p (log p / (p − 1))² · cos(2π x log p / L),

with L = log(T / 2π) and T the mean height of the sample.
The prime sum converges absolutely (Σ_p log²p / (p−1)² ≈ 1.17).
We implement up to p ≤ 10⁶ (78 498 primes); truncation error well
below data precision.

**Ambiguity disclosure.** Several equivalent forms circulate in the
literature — some authors absorb extra factors of 2 or of (2π)² into
the prefactor, and some include prime-power terms (k ≥ 2 in the log ζ
Dirichlet-series expansion) which are negligible at the precision
here (they scale like log²p / p²ᵏ). We use the form above. The
canonical amplitude corresponds to A = 1 in the fit.

---

## Numbers

Data: N = 10⁵ zeros, γ ∈ [14.13, 74 920.83]. Sample-mean of
log(γ/2π) is **L_mean = 8.5055**. dof after x > 0.1 mask = 58.

| Model | free pars | χ² | dof | χ²/dof | p-value |
|---|---|---|---|---|---|
| M0 GUE only | 0 | 434.19 | 58 | 7.49 | ≈ 0 |
| M1 GUE+BK (A=1, L=L_mean) | 0 | 690.85 | 58 | 11.91 | ≈ 0 |
| M2 GUE+BK (A, L_eff free) | 2 | 233.68 | 56 | 4.17 | ≈ 0 |
| M3 GUE+BK + C cos(2π ν x + φ) | 5 | 67.57 | 53 | 1.27 | 0.086 |

**F-tests (nested):**

- M0 → M2:  F = 24.0, p ≈ 3 × 10⁻⁸  (BK provides real signal)
- M2 → M3:  F = 43.4, p ≈ 3 × 10⁻¹⁴ (residual beyond BK is real)

**Best-fit parameters.**
- M2:  A = 0.41, L_eff = 7.44 (vs L_mean = 8.51)
- M3:  A = 0.35, L = 6.42, C = 0.031, ν = 1.109, φ = 0.40

---

## Discussion

### (1) Canonical BK has the wrong amplitude

With A = 1 and L = L_mean = 8.51 fixed, the BK formula is *worse* than
pure GUE (M1 χ²/dof = 11.9 vs M0 = 7.49). Freeing A drops it to A ≈
0.41 — i.e. the measured arithmetic amplitude is roughly 40% of the
naive closed form. Possible interpretations:

(a) My form miscounts an O(1) prefactor (literature has at least three
    equivalent forms; I used the Berry-Keating 1999 / Bogomolny 2007
    convention). A factor-of-~2.5 discrepancy is plausibly a missing
    factor of 2 plus a (2π)-style convention in the normalisation.

(b) The *shape* χ²/dof still = 4.2 after freeing A and L, so the
    discrepancy is not purely an overall amplitude — the BK
    functional form does not fully match the measured residual,
    independent of normalisation.

(c) L_eff = 7.44 is significantly lower than L_mean = 8.51. This is
    consistent with lower-height zeros dominating the pair-correlation
    signal (the density of pairs per unit height grows like (log γ)²,
    but at fixed unfolded x the number of pairs per zero is roughly
    uniform, so pairs from lower-γ zeros — which have smaller L —
    contribute more weight to bumps at small x where the residual is
    largest).

### (2) There is a clear non-BK residual at ν ≈ 1

The M2 → M3 F-test is overwhelmingly significant. The extra cosine
has frequency ν = 1.109 (period ≈ 0.90 in x), amplitude C = 0.031.
Interpretations:

- **GUE sine-kernel harmonic.** R_2^GUE(x) = 1 − sinc²(πx) has its
  first "shoulder" at x = 1 (spacing = mean spacing). A small
  miscalibration of the Odlyzko unfolding (e.g. missing a log log T
  correction of order 1%) would produce exactly such a x ≈ 1 residual
  at first order. Most likely explanation.
- **Higher-order arithmetic term** beyond BK leading order
  (prime-power k = 2 corrections? off-diagonal prime-pair terms?).
  Plausible but sub-dominant in literature analysis.
- **Bin-edge aliasing** from Δx = 0.05 near x = 1.

Without further measurement I cannot distinguish these. The honest
statement: **the residual is dominantly BK but a ν ≈ 1 modulation of
amplitude ~0.03 remains unexplained**.

### (3) What this means for the ZSA / CCM hypothesis

Nothing new. As the prior Test 5 report concluded, the BK arithmetic
correction is a long-known, non-CCM-specific, purely number-theoretic
artefact; detecting it in 10⁵ Odlyzko zeros is consistent with decades
of literature (see Figure 3 of Snaith 2010, showing the same dips at
x ≈ 14, 21, 25 on the *unscaled* pair correlation — we see the
smoothed continuum analogue on the *scaled* pair correlation). No
ZSA-specific conclusion can be drawn.

---

## Files

- `/home/remondiere/crossed-cosmos/derivations/V7-BK-fit.py`
- `/home/remondiere/crossed-cosmos/derivations/V7-BK-fit.png`
- `/tmp/V7-test5-residuals.csv` (input)

## References consulted

- Bogomolny & Keating, *Random matrix theory and the Riemann zeros II:
  n-point correlations*, Nonlinearity 9 (1996) 911-935.
- Snaith, *Riemann zeros and random matrix theory*, Milan J. Math. 78
  (2010) — §4, esp. Theorem 4.3 and Fig. 3 (via
  https://people.maths.bris.ac.uk/~mancs/papers/SnaithRiemann.pdf).
- Berry & Keating, *The Riemann Zeros and Eigenvalue Asymptotics*,
  SIAM Review 41 (1999) — eq. (49) form.
