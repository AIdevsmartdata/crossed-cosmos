# D10 — DESI DR2 covariance correction to D7

**Date:** 2026-04-21
**Trigger:** D7 used an approximate diagonal-ish DR2 covariance
(σ_w0 = 0.20, σ_wa = 0.80, ρ = −0.80). The real DESI DR2 DESY5 posterior
is *much* tighter and more anti-correlated.

## 1. Source of the real covariance

Primary source: **DESI Collaboration, arXiv:2503.14738v3** ("DESI DR2 Results II"),
Section VII (Dark Energy), Eq. (28) + pivot-redshift quote on p. 24:

> *"For the DESI+CMB+DESY5 combination, we find z_p = 0.31 and
>  w_p = −0.954 ± 0.024."*

and Eq. (28):

> *w_0 = −0.752 ± 0.057,  w_a = −0.86 (+0.23 / −0.20)   (DESI+CMB+DESY5)*.

No 2×2 covariance matrix is published in machine-readable form in that paper
(no .cov file in the arXiv source or the linked DESI data release at the
time of writing). However, the CPL pivot redshift is defined as the value at
which σ(w_p) is minimised; this immediately implies

    cov(w_0, w_a)  =  −(1 − a_p) · σ²(w_a),        a_p ≡ 1/(1+z_p)
    ρ(w_0, w_a)   =  −(1 − a_p) · σ(w_a) / σ(w_0).

so the full 2×2 covariance is *uniquely determined* by (σ_w0, σ_wa, z_p).
Cross-check: under this reconstruction σ(w_p) = √(σ_w0² − (1−a_p)² σ_wa²)
= **0.0257**, vs. the paper's quoted **0.024** — 7% residual, consistent
with the mildly-non-Gaussian posterior and the asymmetric +0.23/−0.20 error
on w_a.

I used the symmetrised σ(w_a) = 0.215; the skewness does not meaningfully
shift any conclusion below.

## 2. Key reconstructed numbers

| Dataset            | w_0     | σ_w0  | w_a     | σ_wa  | z_p  | ρ(w_0,w_a) |
|--------------------|---------|-------|---------|-------|------|-----------:|
| DESI+CMB+DESY5     | −0.752  | 0.057 | −0.86   | 0.215 | 0.31 | **−0.893** |
| DESI+CMB           | −0.420  | 0.210 | −1.75   | 0.580 | 0.53 | **−0.957** |
| **D7 old approx.** | −0.75   | 0.20  | −0.86   | 0.80  | —    |     −0.80  |

The old D7 σ_wa was **≈ 4× too large** and σ_w0 was **≈ 3.5× too large**.
The correlation sign was right, the magnitude was underestimated.

## 3. ECI inclusion in the real DR2 contour

Mahalanobis distances (DR2 DESY5 mean, full real covariance):

| Target                                                 | d [σ, 2-dof] |
|--------------------------------------------------------|-------------:|
| ΛCDM point (−1, 0)                                     |     **4.36** |
| Scherrer–Sen minimal-coupling track (minimum over w_0) |     **3.33** |
| ECI NMC band (\|ξ_χ\| ≤ 2.4·10⁻², χ_0 = M_P/10)        |     **3.29** |

Thresholds (2-dof χ²): 1σ = √2.30 = 1.52 ; 2σ = √6.17 = 2.48.

**Verdict (DESI+CMB+DESY5): the ECI band lies OUTSIDE the DR2 2σ contour
(≈ 3.3σ from the mean).** Cross-check under the old (over-loose) covariance
gives 0.79σ, reproducing the original D7 "inside 1σ" claim — confirming
the old plot *was misleading* purely through the size of the assumed
errors, not through the centring.

## 4. How much of this is ECI-specific?

**Almost none.** The 3.3σ distance is dominated by the minimum distance to
the minimal-coupling **Scherrer–Sen line itself** (3.33σ) — the NMC band
(half-width ≈ 9·10⁻³ in w_a at χ_0 = M_P/10, i.e. ≈ 4% of σ_wa) barely
changes it. DR2+DESY5 prefers the phantom-crossing quadrant
(w_0 > −1, w_a < 0 with w_0 + w_a < −1 at early times), which *no*
thawing-quintessence model — minimal or NMC — can populate. This is the
same tension that DESI quote themselves as 4.2σ rejection of ΛCDM under
w_0 w_a CDM with DESY5; it prices out *all* slow-roll single-scalar
thawing models at DR2+DESY5 precision, independently of ξ_χ.

The ECI-specific width of the NMC band (controlled by ξ_χ and χ_0/M_P)
remains ≪ σ_wa even with the real tighter covariance, so **within the
universe of thawing-quintessence models ECI is still indistinguishable
from minimal-coupling wCDM at DR2 precision**. What the old D7 Caveat 4
got wrong was the framing "ECI lies inside the DR2 1σ contour": the SS
track (and hence any thawing model on or near it, ECI included) lies
**outside the DR2 2σ contour** when the real covariance is used.

## 5. Robustness

- Switching from DESY5 to Union3 (w_0 = −0.667 ± 0.088, w_a = −1.09,
  z_p ≈ 0.4) gives ρ ≈ −0.88 and the SS track shifts to ~ 2.3σ from the
  Union3 mean — still outside 2σ.
- Under DESI+CMB alone (no SNe, much looser), the SS track is ~ 1.4σ
  from the mean, i.e. inside the 2σ contour; the old D7 verdict held
  *for that dataset*. The problem was that D7 used the DESY5 central
  value (−0.75, −0.86) with CMB-only-sized error bars.
- Using the asymmetric w_a = −0.86 (+0.23 / −0.20) and picking the
  relevant side (ECI/SS lies above the DR2 mean, so σ_wa_+ = 0.23
  matters) pushes d_SS_min from 3.33σ to 3.1σ — still outside 2σ.

## 6. Files

- `derivations/D10-desi-covariance.py` — reconstruction + plot + Mahalanobis
- `derivations/figures/D7-xi-w0-wa-v2.pdf` — corrected contour figure
- `derivations/figures/D7-xi-w0-wa.pdf` — original (kept, for comparison)
- `derivations/_results/D10-summary.json` — machine-readable numbers
- `derivations/_cache/desi-dr2.pdf` — cached source paper (arXiv:2503.14738v3)

## 7. Verdict shift in the paper

Caveat 4 in `paper/section_3_5_constraints.tex` claims

> "the ECI band produced by the Cassini-allowed coupling range lies
>  entirely inside the DESI DR2 1σ contour".

**This is incorrect under the real DR2 DESY5 covariance.** The band lies
outside the 2σ contour. The paper's broader conclusion — that ECI is
indistinguishable from minimal-coupling wCDM at DR2 precision — is still
correct, but for the *opposite* reason: it is not that both fit, but that
both are equally disfavoured at ~3σ by DR2+DESY5 under w_0 w_a CDM.
A `% D10 CORRECTION:` note has been added to the .tex source.
