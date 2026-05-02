# v7-note v0.1 — erratum on Δ_BK prefactor (2026-05-02)

**Affects:** `paper/v7_note/v7_note.{tex,pdf}` v0.1 (Zenodo DOI 10.5281/zenodo.19983241).

**Severity:** Editorial — the **headline result M2 χ²/dof = 4.17 is unchanged**.
The fit's free `L_eff` parameter absorbed the prefactor error. Only the
canonical (A=1) M1 row and the best-fit amplitude `A_fit` move.

## What changes

Berry-Keating arithmetic correction Δ_BK formula prefactor:

| Quantity | v7-note v0.1 (incorrect) | Erratum (correct) |
|---|---|---|
| Prefactor | `−2/(2π)²` | **`−2/L²`** |
| M1 χ²/dof (A=1, L=L̄) | 11.911 | **4.523** |
| Best-fit A | 0.408 | **0.573** |
| Best-fit L_eff | 7.44 | **7.44** (unchanged) |
| **M2 χ²/dof (free A, L)** | **4.173** | **4.173** (unchanged) |
| M3 χ²/dof (BK+cos) | 1.275 | 1.275 (unchanged) |

## Origin of the error

The v7-note used the prefactor `1/(2π)²` from Conrey-Snaith 2007 Theorem 4.1
(arXiv:math/0509480 eq. 4.25), which is the prefactor for the **raw-γ** pair
correlation `Σ f(γ−γ')`. The V7-test5 pipeline computes the **unfolded-x**
pair correlation R₂(x) where `x = (γ_j − γ_i)/d̄` and `d̄ = L/(2π)` is the mean
density. Going from raw-γ to unfolded-x requires the unfolding Jacobian
`R₂_unfolded(x) = (1/d̄²) R₂(x/d̄)` (Bogomolny LH-2003 arXiv:nlin/0312061
page 62, verbatim quote in `notes/V7_BK_bisect_2026_05_02.md`), which
introduces a factor `(2π/L)² = 4π²/L²`. After this rescaling the prefactor
becomes `(1/(2π)²)·(4π²/L²) = 1/L²`, and with the c.c.~factor of 2 the
canonical Δ_BK prefactor in unfolded-x is `−2/L²`.

This matches Berry-Keating SIAM Review **41** (1999) 236-266 eq. (4.20)
verbatim, which directly writes `1/(2(π⟨d⟩)²) = 2/L²` for `⟨d⟩ = L/(2π)`.

(Aside: the v7-BK-fit.py docstring also miscited Berry-Keating 1999 as
"Rev. Mod. Phys. 71, 1183"; the correct journal is SIAM Review 41 (1999)
236-266. The miscitation is fixed in the same patch.)

## Triangulation

References checked verbatim against PDFs fetched directly from arXiv /
publisher mirrors:

1. Berry-Keating, *SIAM Review* **41** (1999) 236-266, eq. (4.20)/(4.23) →
   prefactor `1/(2(π⟨d⟩)²) = 2/L²` in unfolded x.
2. Bogomolny, *Quantum and Arithmetical Chaos*, Les Houches 2003,
   arXiv:nlin/0312061, eq. (57) for raw R₂ + page 62 unfolding rule →
   prefactor `1/L²` after rescaling, total `2/L²` with c.c.
3. Conrey-Snaith, *Proc. London Math. Soc.* **94** (2007) 594-646,
   arXiv:math/0509480, Theorem 4.1 eq. (4.25) → prefactor `1/(2π)²` in raw γ
   (the source of the v7-note error when applied without unfolding rescaling).

Crossref + arXiv API confirmation:
- Berry-Keating SIAM 41 (1999) 236-266: confirmed via Crossref query
  (DOI returned).
- Bogomolny nlin/0312061: confirmed via arXiv API id_list query
  (title "Quantum and Arithmetical Chaos", 2003-12-23).

## Numerical re-validation

After patching `derivations/V7-BK-fit.py` to use `−2/L²`:

```
====    chi^2    table ====
M0  GUE only                        434.19    58     7.486
M1  GUE+BK (A=1, L fixed)           262.31    58     4.523    <- was 11.911
M2  GUE+BK (A, L_eff free)          233.68    56     4.173    <- unchanged
M3  GUE+BK + Cos(nu x + phi)         67.57    53     1.275    <- unchanged

[M2 best-fit]  A = 0.5729, L_eff = 7.4413  (L_mean from data = 8.5055)
                                  ^^^^ was 0.408
```

The qualitative behaviour is now correct: at canonical A=1, the BK
correction **improves** the fit (4.52 < 7.49 = M0 baseline) instead of
**worsening** it (11.9 > 7.49) as in v0.1.

## What the v7-note v0.2 needs to update

1. The Δ_BK formula prefactor: `−2/(2π)²` → `−2/L²`.
2. The M1 row in the chi^2 table: 11.911 → 4.523.
3. The best-fit A value in the M2 paragraph: 0.408 → 0.573.
4. The Berry-Keating citation: SIAM Review 41 (1999) 236-266 (not Rev Mod Phys).
5. The Conrey-Snaith citation: Theorem 4.1 (not Theorem 4.3 — that's the
   Snaith 2010 review label).

The headline finding (BK is detected at high significance via the M2 ablation
and the cosine extension is a real feature at p=0.086) is unchanged.

## Disclosure

This erratum was caught by an internal triangulation pass on 2026-05-02
(notes/V7_BK_bisect_2026_05_02.md "Resolution" section). It has not yet
been published to Zenodo as a v0.2; the present file documents the issue
for the next release cycle.
