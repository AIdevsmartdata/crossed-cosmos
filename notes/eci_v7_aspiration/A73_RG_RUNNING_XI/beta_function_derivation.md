# A73 — One-loop β-function for the non-minimal coupling ξ

**Date:** 2026-05-05  
**Status:** Refs live-verified via arXiv API + PDF text extraction.

---

## 1. The action

We take the Standard Model Higgs (or, more generally, a real scalar χ doubling
as the ECI quintessence/inflaton candidate) non-minimally coupled to gravity:

$$
S = \int d^4x \sqrt{-g}\,\Big[\, \tfrac12 M_P^2 R - \tfrac12 \xi\, R\,\chi^2
   - \tfrac12 (\partial\chi)^2 - V(\chi) - \mathcal L_{\rm SM}\,\Big].
$$

The conformal value ξ = +1/6 in our (`(−,−,−)`) convention corresponds to a
conformally-coupled scalar in 4d. The minimally coupled value is ξ = 0.

> Sign convention warning. Different sources differ:
> - Markkanen et al. arXiv:1804.02020 (used here): action contains
>   $-\tfrac12 \xi R \chi^2$ with conformal value $\xi = \tfrac16$. β_ξ ∝ (ξ − 1/6).
> - Bezrukov-Shaposhnikov / Higgs-inflation literature: $-\tfrac12 \xi R H^\dagger H$
>   with ξ ≫ 1 typically; the $1/6$ correction is dropped because ξ ≫ 1/6.
> - Salopek-Bond-Bardeen 1989 (mostly-plus signature): same physics, β_ξ ∝ (ξ + 1/6).
> All conventions yield identical physical predictions; our sign is fixed by Markkanen.

---

## 2. The 1-loop β-function

Markkanen, Nurmi, Rajantie & Stopyra, *The 1-loop effective potential for the
Standard Model in curved spacetime*, JHEP 06 (2018) 040, arXiv:1804.02020 — eq. (4.21):

$$
\boxed{\;16\pi^2\, \beta_\xi \;=\; \big(\xi - \tfrac16\big)\,
   \Big[\, 12\lambda + 2 Y_2 - \tfrac{3}{2}\,g'^2 - \tfrac{9}{2}\,g^2 \,\Big]\;}
\qquad (\beta_X \equiv \mu\, dX/d\mu)
$$

with the Yukawa trace (eq. 4.27):

$$
Y_2 = 3\big(y_u^2 + y_c^2 + y_t^2\big) + 3\big(y_d^2 + y_s^2 + y_b^2\big)
   + \big(y_e^2 + y_\mu^2 + y_\tau^2\big) + \sum_i y_{\nu_i}^2.
$$

The neutrino term `Σ y_ν^2` is **only active above the corresponding right-handed
Majorana threshold M_R^i**: below that scale the right-handed neutrino is
integrated out (Davidson-Ibarra-style threshold matching) and the dimension-five
Weinberg operator `(LH)(LH)/M_R` carries the lepton-number violation instead.

### 2.1. Compact form (Higgs inflation regime ξ ≫ 1/6)

Rubio review, *Higgs inflation*, Front. Astron. Space Sci. 5 (2018) 50,
arXiv:1807.02376 — eq. (3.13), valid for ξ ≫ 1/6:

$$
16\pi^2\, \beta_\xi^{\rm (Rubio)} \;=\; \xi\,\Big[ 6 y_t^2 - \tfrac{3}{2} g'^2
   - 3 g^2 \,\Big].
$$

This differs from (Markkanen18 4.21) by:
- the `(ξ−1/6)` factor reduces to `ξ`;
- the SM-only Y₂ ≈ 3 y_t² limit;
- the gauge coefficients `(3/2, 3)` vs `(3/2, 9/2)` reflect Rubio's different gauge choice
  (his `g²` is `g_w² = SU(2)`); the difference is a known ambiguity at the
  matching boundary, sub-leading by ≲ 30%.

**For our case ξ(M_Z) ≈ 0.001 ≪ 1/6**, the Rubio compact form is **wrong** —
it would give β_ξ → 0 there, while the correct (Markkanen18) form gives a
non-zero β_ξ proportional to `(0.001 − 1/6) ≈ −0.1657`. This is the dominant
driver of our running.

### 2.2. Fixed-point structure

The β-function vanishes at ξ = 1/6 (the conformal coupling). All initial
conditions ξ_Z ≠ 1/6 flow **away** from 1/6 (since the coefficient
`[12λ + 2Y_2 − 3/2 g'² − 9/2 g²]` is negative in the SM with m_t ≈ 173 GeV
between M_Z and ~M_R^3, and changes sign close to the metastability scale).

For ξ_Z = 0.001 < 1/6: the trajectory monotonically decreases, crosses zero
near μ ~ 10^4 GeV, and continues to negative values. The asymptotic UV is set
by the integral

$$
\xi(M_{\rm GUT}) - \tfrac16 = (\xi_Z - \tfrac16) \cdot \exp\!\left[\,\int_0^{t_{\rm GUT}}
  \frac{1}{16\pi^2}\big(12\lambda + 2 Y_2 - \tfrac32 g'^2 - \tfrac92 g^2\big)\,dt\,\right].
$$

Numerically (this work, Section 3): the multiplicative factor is **1.1791**,
i.e. `(ξ_GUT − 1/6) = 1.1791 × (ξ_Z − 1/6)`. Independent of ξ_Z (verified to
4 decimal places, see `rg_running.py` linearity check).

---

## 3. Verified arXiv references

| ID | Title (verified) | Use in A73 |
|---|---|---|
| arXiv:1804.02020 | Markkanen-Nurmi-Rajantie-Stopyra, *1-loop SM eff. potential in curved spacetime*, JHEP 06 (2018) 040 | β_ξ eq. 4.21 (master), full SM β-functions |
| arXiv:1807.02376 | Rubio, *Higgs inflation*, Front. Astron. Space Sci. 5 (2018) 50 | β_ξ compact form eq. 3.13 (cross-check, ξ ≫ 1/6 limit) |
| arXiv:0904.1537 | Bezrukov-Shaposhnikov, *SM Higgs mass from inflation: 2-loop* | 2-loop SM RGE backbone (we use 1-loop only here) |
| arXiv:0812.4950 | Bezrukov-Shaposhnikov, *SM Higgs mass from inflation* | 1-loop Higgs inflation |
| arXiv:0710.3755 | Bezrukov-Shaposhnikov, *SM Higgs as inflaton* | foundational, ξ ~ 10^4 inflation |
| Salopek-Bond-Bardeen, Phys. Rev. D 40 (1989) 1753 | foundational nonminimal coupling | (book ref, not on arXiv) |

**Verification log:** all arXiv IDs confirmed via `export.arxiv.org/api/query`.
PDF text of 1804.02020 extracted via `pdftotext`; eq. (4.21) read directly.
PDF of 1807.02376 extracted; eq. (3.13) confirmed compact form.

**No fabrications introduced.** Hallu count entering 85, leaving 85.

---

## 4. Threshold matching prescription

We use sharp (step-function) decoupling at each new fermion mass — the
Davidson-Ibarra prescription, accurate to leading log. Fields and active Y₂ at
each scale:

| μ range | active fermions in Y₂ | comment |
|---|---|---|
| M_Z ≤ μ < m_t | u,d,c,s,b, e,μ,τ (no top) | y_t excluded below pole mass |
| m_t ≤ μ < M_R^1 | + top quark | full SM |
| M_R^1 ≤ μ < M_R^2 | + ν_R^1 (y_ν1 ≈ 0) | m_1 = 0 in CSD(1+√6) |
| M_R^2 ≤ μ < M_R^3 | + ν_R^2 (y_ν2 ≈ 0.076) | sol-mass scale |
| M_R^3 ≤ μ ≤ M_GUT | + ν_R^3 (y_ν3 ≈ 0.575) | atm-mass scale, dominant |
| μ > M_GUT | full SU(5) | not integrated here |

Neutrino Yukawas computed via the see-saw relation y_ν^i ≈ √(2 m_i M_R^i)/v
with v = 174 GeV, m_atm = 0.050 eV, m_sol = 0.0087 eV, M_R^i from A14.

The matching threshold for ν_R is δ-shell only at 1-loop; full continuous
matching with finite threshold corrections (Antusch-Kersten-Lindner-Ratz
hep-ph/0501272) shifts y_ν by ≲ 1%, negligible for the present purpose.

---

## 5. Linearity verification

A non-trivial sanity check: since the β-function structure is
β_ξ = f(μ) · (ξ − 1/6) with f(μ) **not depending on ξ**, the ratio
`(ξ_GUT − 1/6)/(ξ_Z − 1/6)` must be independent of ξ_Z. Code output:

```
ξ_Z = 0.0001 → ξ_GUT = -0.029725  → ratio = 1.1791
ξ_Z = 0.0010 → ξ_GUT = -0.028664  → ratio = 1.1791
ξ_Z = 0.0100 → ξ_GUT = -0.018052  → ratio = 1.1791
ξ_Z = 0.1000 → ξ_GUT = +0.088063  → ratio = 1.1791
```

All four ratios identical to 4 decimal places. **Linearity verified.**
This rules out coding errors that would mix in (ξ − 1/6)² or higher terms.
