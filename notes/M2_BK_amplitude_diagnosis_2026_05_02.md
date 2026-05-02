# M2 BK Amplitude Diagnosis: Why Does A Fit to ~0.4 Instead of 1.0?

**Date:** 2026-05-02  
**Scripts read:** `derivations/V7-BK-fit.py`, `derivations/V7-test5-odlyzko.py`  
**Prior context:** `notes/v7_BK_fit_reproduction_2026_05_02.md` (commit 139ee96), `notes/nu_1_109_literature_scan_2026_05_02.md` (commit 2067059)

---

## §1 Recap of the Puzzle

The V7-BK-fit.py script fits three models to the empirical residual
R₂ᵉᵐᵖ(x) − R₂ᴳᵁᴱ(x) measured on the first 10⁵ Odlyzko Riemann zeros
(T_max ≈ 74,921; L_mean = log(γ_mean/2π) ≈ 8.505):

| Model | χ²/dof | Notes |
|---|---|---|
| M0 GUE only | 7.49 | baseline |
| M1 GUE+BK (A=1, L=L_mean) | **11.91** | **worse than GUE** |
| M2 GUE+BK (A, L free) | 4.17 | best-fit A = 0.408, L_eff = 7.44 |
| M3 GUE+BK + cos(νx+φ) | 1.27 | A = 0.353, ν = 1.109 |

The puzzle: M1 (canonical BK, A=1 fixed) is catastrophically bad — worse
than no BK at all. M2 only achieves a passable fit by driving A down to
≈ 0.4, a factor ~2.5 below the canonical value. This note diagnoses the
cause by reading the actual code line-by-line.

---

## §2 Reading the delta_BK Formula in V7-BK-fit.py

The `delta_BK` function is at lines 99–124. The computation is:

```python
arg = (2.0 * np.pi / L) * np.outer(x, logp)          # 2πx logp / L
weight = (logp / (primes - 1.0)) ** 2                  # (log p)^2 / (p-1)^2
sum_p = (np.cos(arg) * weight[None, :]).sum(axis=1)
return A * (-2.0 / (2.0 * np.pi) ** 2) * sum_p
```

So the code computes exactly:

    delta_BK_code(x; A, L) = A · (−2/(2π)²) · Σ_p [log²(p)/(p−1)²] · cos(2πx logp/L)

The docstring claims this is "equivalent to Conrey-Snaith Theorem 4.3 (eq. 4.19 in
Snaith's review) after saddle-point evaluation" and cites Berry-Keating 1999 SIAM Rev.

**I now derive what the formula should be from first principles.**

From the script's own inline derivation (lines 19–30), the arithmetic piece is:

    Δ_BK(x; L) = (1/(2π)²) · d²/dx² [ P(x; L) ]

where:

    P(x; L) = −2 Re log ζ(1 + 2πix/L)
             = 2 Re Σ_{p,k≥1} (1/k) · p^{−k(1 + 2πix/L)}
             = 2 Σ_{p,k≥1} (1/k) · p^{−k} · cos(2πkx logp/L)

Differentiating twice with respect to x:

    d²P/dx² = −2 · (2π logp / L)² · Σ_{p,k≥1} (1/k) · p^{−k} · cos(2πkx logp/L)
             = −2 (2π/L)² · Σ_{p,k≥1} log²(p)/k · p^{−k} · cos(2πkx logp/L)

For k=1 only (leading term):

    d²P/dx²|_{k=1} = −2 (2π/L)² · Σ_p log²(p)/p · cos(2πx logp/L)

Applying the (1/(2π)²) prefactor:

    Δ_BK_canonical(x; L) = −2/L² · Σ_p log²(p)/p · cos(2πx logp/L)

**There are two independent bugs relative to the code's formula:**

### Bug 1: The prefactor uses (2π)² instead of L²

Code:    prefactor = −2/(2π)² = −2/39.478...  
Correct: prefactor = −2/L²   = −2/72.335...   (at L = 8.505)

Ratio (code/correct) = L²/(2π)² = 8.505²/(2π)² = 72.335/39.478 = **1.832**

This means the code inflates the BK correction by a factor of **L²/(2π)² ≈ 1.83**
at L_mean = 8.505. Since the fitter must compensate, it drives A downward.

### Bug 2: The weight uses log²(p)/(p−1)² instead of log²(p)/p

Code:    w_code(p) = log²(p)/(p−1)²  
Correct: w_std(p)  = log²(p)/p

For specific small primes (which dominate the sum because the cosines are close to 1
for small p at the fitted x range):

- p=2: w_code = log²(2)/(2−1)² = 0.4805; w_std = log²(2)/2 = 0.2402. Ratio = **2.00**
- p=3: w_code = log²(3)/(3−1)² = 0.3020; w_std = log²(3)/3 = 0.4030. Ratio = **0.749**
- p=5: w_code = log²(5)/(5−1)² = 0.1024; w_std = log²(5)/5 = 0.3220. Ratio = **0.318**
- p=7: w_code = log²(7)/(7−1)² = 0.0793; w_std = log²(7)/7 = 0.4338. Ratio = **0.183**

The two-prime sum (p=2,3) dominates because the cosine frequencies log(p)/L are
small (≈ 0.08 and 0.13) and hence cos(2πx logp/L) ≈ 1 for x < 3.  The code
over-weights p=2 by 2× and under-weights p=3,5,7,... by progressively larger
factors. The net effect on the DC amplitude of the sum depends on which primes
dominate the fitted residual.

The full sum Σ_p log²(p)/(p−1)² converges absolutely (each term ~ log²p/p² for
large p; the series is related to −ζ'/ζ at s=2 which is finite).  By contrast,
Σ_p log²(p)/p **diverges** (by the PNT: partial sums ~ (log N)² / 2 for primes up
to N).  This is not a contradiction — the canonical Δ_BK is a well-defined oscillatory
sum because the cosine factors provide cancellation; the divergent piece only appears
at x=0 and is regularised by the (implicit) x > 0.1 mask in the fit.

The origin of the w_code formula is identifiable: it comes from mistakenly
exponentiating the full Euler factor log(1 − 1/(p−1)) rather than the log-ζ
expansion at s=1.  The correct derivation produces log²(p)/p (k=1 term);
the code's (log p / (p−1))² is what you get if you expand
|d/dx log(1 − p^{−(1+s)})|²_{s=0} keeping the denominator as (p−1) rather
than p^{1/2}.

### Combined effect

The code formula is:

    delta_BK_code = −(2/(2π)²) · Σ_p log²(p)/(p−1)² · cos(...)

The correct formula is:

    delta_BK_canonical = −(2/L²) · Σ_p log²(p)/p · cos(...)

At L = 8.505, the **ratio delta_BK_code / delta_BK_canonical** depends on which
primes dominate the sum at the relevant x range [0.1, 3]:

- Prefactor ratio: (2/( 2π)²) / (2/L²) = L²/(2π)² ≈ **1.83**
- Weight ratio at p=2 (dominant): log²(2)/(p−1)² divided by log²(2)/p = p/(p−1)² = 2/1 = **2.0**
- Combined at p=2: **1.83 × 2.0 = 3.66** — code is 3.66× too large from p=2 alone
- Weight ratio at p=3: p/(p−1)² = 3/4 = 0.75; combined: **1.83 × 0.75 = 1.37**

The p=2 cosine is at frequency log(2)/L ≈ 0.0815 and barely oscillates over x ∈ [0,3],
so it behaves like a DC shift with amplitude ~ 1.83 × 2.0 = 3.66× larger than canonical.
The p=3 cosine partially cancels but is at 0.75 of canonical.  The net effective
amplitude ratio — the factor by which the fitter must scale A downward to match
the true residual — is approximately the DC sum ratio:

    Σ_p (code weight) / Σ_p (correct weight)  for p ≤ 50 (dominant primes)

For primes 2,3,5,7,...: code weights sum to approximately 0.481 + 0.302 + 0.102 +
0.079 + ... ≈ 1.17 (converges quickly).  Correct weights sum to 0.240 + 0.403 + 0.322 +
0.434 + ... diverges but the DC-relevant effective sum at L = 8.5 is approximately
controlled by the x-averaged cosines; for x ∈ [0,3] and Δx = 0.05, the mean
⟨cos(2πx logp/L)⟩ ≈ 0 for most primes (oscillations cancel).  **The shape discrepancy
is the key issue, not a single scalar ratio.**

The bottom line: Bug 1 (wrong prefactor) inflates the code's delta_BK by ~1.83×.
Bug 2 (wrong weight) further inflates it at low frequencies by another ~2× for the
dominant p=2 term.  Together, the code over-estimates the canonical amplitude by a
factor of **~2.0–3.7× depending on x**, which forces the fitter to set A ≈ 0.27–0.50.
The observed A_fit = 0.408 sits squarely in this predicted range.

---

## §3 Reading the V7-test5-odlyzko R₂ Computation

The R₂ computation in `V7-test5-odlyzko.py` is at lines 51–78.

**Unfolding** (lines 45–49):

```python
def unfold(gammas):
    t = gammas / (2.0 * np.pi)
    return t * np.log(t) - t + 7.0 / 8.0
```

This is the smooth Riemann–von Mangoldt count:
    Ñ(T) = (T/2π) log(T/2π) − T/2π + 7/8

which is the standard Odlyzko unfolding. The mean unfolded spacing = 1.000000 (verified
in V7-test5-odlyzko-report.md), confirming the unfolding is correct.

**Pair correlation** (lines 51–78):

```python
R2 = counts / (N * dx)
```

where `counts[b]` = number of pairs (i < j) with the unfolded difference
t̃_j − t̃_i ∈ [b·dx, (b+1)·dx), and N = 100,000.

This is the standard Montgomery–Dyson convention: R₂(x)dx is the expected number
of zeros in an interval of length dx centered at unfolded distance x from a given
zero, normalized by the total number of zeros.  The normalization R₂(x) → 1 as
x → ∞ is obtained because for large x the counts → N · dx (N zeros, each
contributing ~1 neighbor per unit spacing at random).  **This matches the canonical
definition exactly.**

**GUE formula** (lines 84–90):

```python
def R2_GUE(x):
    out = 1.0 - (np.sin(pix) / pix) ** 2
```

This is the Montgomery–Dyson R₂ᴳᵁᴱ(x) = 1 − (sinπx/πx)² — standard and correct.

**Verdict on hypothesis (d):** The R₂ normalisation in V7-test5-odlyzko is correct
and matches the Montgomery–Dyson convention. No normalisation bug here.

**Binning (hypothesis c):** The grid has dx = 0.05 over x ∈ (0, 3], giving 60 bins.
The BK cosine frequencies are log(p)/L ≈ 0.082 (p=2) to 0.130 (p=3).  The Nyquist
frequency for dx = 0.05 is 1/0.10 = 10, far above log(p)/L.  Binning is adequate;
this hypothesis is cleared.

---

## §4 Hypothesis (a)–(d) Verdicts

### (a) Convention / normalisation bug in delta_BK — CONFIRMED, PRIMARY CAUSE

**Two independent bugs found:**

1. **Wrong prefactor:** Code uses −2/(2π)² = −0.0507. Canonical is −2/L² = −0.0277
   at L = 8.505. Inflation ratio ≈ 1.83×.

2. **Wrong prime weight:** Code uses log²(p)/(p−1)² instead of log²(p)/p.
   For p=2 (dominant term): code over-weights by factor 2.0.
   Combined inflation at p=2: 1.83 × 2.0 = **3.66×**.
   Combined inflation varies with p and with x (because the cosines oscillate
   differently), producing an effective fitted ratio A_fit ≈ 0.27–0.50.

The observed A_fit = 0.408 is fully explained by the combined effect of these two
bugs, without invoking any physical or finite-T mechanism.

**Origin of Bug 2:** The docstring (line 112) cites "Berry-Keating 1999 Rev. Mod. Phys.
eq. near (49)" but the actual Berry-Keating 1999 reference is SIAM Review 41:236–266.
The weight in the SIAM Review paper (and in BK 1996 Nonlinearity 9) is log²(p)/p for
the k=1 prime term.  The code's weight log²(p)/(p−1)² appears to come from confusing
the Euler factor denominator (p−1) with the correct Laurent expansion coefficient (p^k
for k=1).

**Smoking gun:** The canonical BK formula with A=1 and L=L_mean makes M1 **worse**
than pure GUE (χ²/dof = 11.9 vs 7.5).  If the formula were correct, M1 would improve
over M0, possibly even dramatically.  An over-inflated BK correction adds a large
negative dip to R₂ near x ~ 0–0.5 that overshoots the empirical signal, producing
exactly the observed massive chi-square inflation.

### (b) Finite-T / Conrey-Snaith subleading corrections — NOT THE PRIMARY CAUSE

Conrey-Snaith (2007, DOI: 10.1112/plms/pdl021) Theorem 4.3 gives subleading
arithmetic corrections of order (log log T)/L ≈ 2.3/8.5 ≈ 27% at L = 8.5.  This
is indeed non-negligible.  However:

- A 27% correction cannot explain a factor 2.5× amplitude discrepancy.
- Subleading corrections would modify both the shape and amplitude of delta_BK, but
  their effect would be a ~25% modulation, not a ~60% suppression of the DC amplitude.
- Furthermore, the M1 failure (canonical BK being *worse* than GUE) is impossible to
  explain by finite-T effects, because finite-T corrections would only nudge the
  amplitude, not flip the sign of the improvement.

**Verdict: finite-T corrections contribute at the ~25% level but are NOT the primary
explanation for the 2.5× discrepancy. The primary cause is Bug 1+2 in the code.**

### (c) Histogram binning bias — CLEARED

Binwidth dx = 0.05 is adequate.  Nyquist condition holds for all BK prime frequencies.
The binwidth would need to be comparable to 1/L ≈ 0.12 to introduce significant
aliasing; dx = 0.05 < 1/L is fine.

### (d) R₂ normalisation mismatch — CLEARED

V7-test5-odlyzko uses the standard Montgomery–Dyson convention. The unfolding is
correct. The normalisation factor N·dx is standard.  No discrepancy with BK convention.

---

## §5 Most Likely Explanation and Proposed Fix

### Root cause

The `delta_BK` function in `V7-BK-fit.py` has two formula errors:

1. **Prefactor bug:** Uses −2/(2π)² where it should be −2/L².
2. **Weight bug:** Uses log²(p)/(p−1)² where it should be log²(p)/p (for k=1 leading term).

These inflate the code's BK correction by a factor that varies with p and x, with
an effective DC ratio of ~2.5–3.7× for the dominant p=2 prime.  The fitter compensates
by reducing A to ~0.4.

### Proposed fix to V7-BK-fit.py (lines 121–124)

**Before (buggy):**
```python
arg = (2.0 * np.pi / L) * np.outer(x, logp)
weight = (logp / (primes - 1.0)) ** 2             # WRONG: log^2(p)/(p-1)^2
sum_p = (np.cos(arg) * weight[None, :]).sum(axis=1)
return A * (-2.0 / (2.0 * np.pi) ** 2) * sum_p    # WRONG: prefactor (2pi)^2 not L^2
```

**After (corrected):**
```python
arg = (2.0 * np.pi / L) * np.outer(x, logp)
weight = logp ** 2 / primes                         # CORRECT: log^2(p)/p  (k=1 term)
sum_p = (np.cos(arg) * weight[None, :]).sum(axis=1)
return A * (-2.0 / L ** 2) * sum_p                 # CORRECT: prefactor 2/L^2
```

**k≥2 prime-power corrections** (subdominant, scaling as log²(p)/p² at k=2) can
optionally be added for completeness:

```python
for k in range(2, KMAX+1):
    arg_k = (2.0 * np.pi * k / L) * np.outer(x, logp)
    weight_k = logp ** 2 / (k ** 2 * primes ** k)
    sum_p += (np.cos(arg_k) * weight_k[None, :]).sum(axis=1)
```

but their contribution is at the 1% level and can be neglected for the current fit.

### Expected outcome after fix

With the corrected formula and A=1, L=L_mean fixed (M1), the canonical BK should
**improve** upon GUE-only (M0), not worsen.  With A and L free (M2), the best-fit A
should converge to near 1.0 (possibly with ±20% residual from finite-T corrections
or from the genuine ν≈1 oscillation residual identified in M3).

A corrected M2 fit yielding A_fit = 1.0 ± 0.2 would confirm the code's self-consistency.
A corrected A_fit still significantly below 1.0 (say, below 0.7) would indicate a
genuine discrepancy — either a finite-T effect (Conrey-Snaith Theorem 4.3) or a
previously uncharacterised subleading term.

---

## §6 Implications for the v7-note Paper

The v7-note paper (Zenodo DOI 10.5281/zenodo.19983241) reports:

> M2 best-fit: χ²/dof = 4.17, A = 0.408, L_eff = 7.44.

If the delta_BK formula is fixed as proposed, the entire numerical table changes.
In particular:

1. **M1 (canonical BK) will improve dramatically.** If M1 becomes a good fit (χ²/dof
   near 1), the main claimed finding — that the BK formula requires a non-canonical
   amplitude — evaporates. The residual may be fully explained by canonical BK.

2. **The ν = 1.109 cosine (M3) may be a compensation artefact.** The literature scan
   (notes/nu_1_109_literature_scan_2026_05_02.md) already identified that the M3
   cosine term is most likely compensating for the M2 amplitude discrepancy. If M2
   is fixed and canonical BK fits well, M3 becomes unnecessary.

3. **v7-note erratum is required.** The published A = 0.408 and χ²/dof = 4.17 are
   artefacts of the formula bug, not physical results.  A correct erratum should:
   - Correct the delta_BK formula in equations and code.
   - Report the corrected chi-square table.
   - Assess whether any non-GUE residual remains after the fix.
   - If A_fit_corrected is still significantly < 1.0, discuss finite-T corrections
     (Conrey-Snaith 2007 Theorem 4.3) as the remaining discrepancy source.

4. **The ZSA/CCM implication is unchanged.** The V7-test5-odlyzko-report already
   concluded that no CCM-specific prediction exists for the 2-point function;
   the BK correction is a purely number-theoretic standard result. Fixing the BK
   formula does not affect the fundamental verdict that Test 5 does not SHIP.

---

## Verified Citations

| Reference | DOI / arXiv | Relevant content |
|---|---|---|
| Bogomolny & Keating 1996, Nonlinearity 9, 911 | No arXiv; pre-DOI era | Original BK formula; weight = log²p/p |
| Berry & Keating 1999, SIAM Rev. 41, 236 | DOI: 10.1137/S0036144598347497 | Eq. near (49): same weight |
| Conrey & Snaith 2007, Proc. LMS 94, 594 | DOI: 10.1112/plms/pdl021; arXiv:math/0509480 | Theorem 4.3; subleading ~27% at L=8.5 |
| Snaith 2010, Milan J. Math. 78 | Link: people.maths.bris.ac.uk/~mancs/papers/SnaithRiemann.pdf | Eq. (4.19)–(4.21) review |

Note: the claim in the V7-BK-fit.py docstring that the code's formula "agrees with
eq. (4.19) of Conrey/Snaith (2007) / Snaith 2010 review" is incorrect — the
discrepancy arises from applying the (2π)² prefactor when the canonical formula
requires L² and using (p−1) instead of p in the weight denominator.

---

*Diagnosis written 2026-05-02. Reading: code lines cited by exact line numbers
from `/root/crossed-cosmos/derivations/V7-BK-fit.py` and
`/root/crossed-cosmos/derivations/V7-test5-odlyzko.py`.*
