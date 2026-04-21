# D7 — Night-session report (2026-04-21)

## What was derived

1. **PPN $\gamma-1$ for the NMC scalar** $S\supset-(\xi_\chi/2)R\chi^2$, via the
   Damour--Esposito-Farèse 1993 scalar--tensor formula
   $\gamma-1=-F'^2/(ZF+\tfrac32 F'^2)$ with $F=M_P^2-\xi_\chi\chi^2$, $Z=1$.
   Full expression (Eq. D7.1 in `section_3_5_constraints.tex`):
   $\gamma-1=-4\xi^2\chi_0^2/[M_P^2+\xi\chi_0^2(6\xi-1)]$; leading order
   $\gamma-1\simeq -4\xi_\chi^2\chi_0^2/M_P^2$. Limit $\xi\!\to\!0$ verified
   symbolically in `D7-ppn-xi-bound.py` (gives exactly 0).

2. **Cassini bound.** With $|\gamma-1|\lesssim 2.3\!\times\!10^{-5}$ (1σ,
   Bertotti-Iess-Tortora 2003): $|\xi_\chi|(\chi_0/M_P)\lesssim 2.4\!\times\!10^{-3}$.
   At the fiducial thawing amplitude $\chi_0=M_P/10$: $|\xi_\chi|_{\max}\approx
   \mathbf{2.4\!\times\!10^{-2}}$ (task asked "10⁻²–10⁻³"; actual value sits at
   the upper edge of that range).

3. **NMC Scherrer--Sen extension.** Closed analytic form to first order in $\xi$:
   $$w_a=-A(\Omega_\Lambda)(1+w_0)+B(\Omega_\Lambda)\,\xi_\chi\sqrt{1+w_0}\,(\chi_0/M_P),$$
   with $A(0.7)=1.58$ (Scherrer-Sen 2008) and $B(\Omega_\Lambda)=(8/\sqrt3)A$,
   so $B(0.7)=7.30$. The $\xi\to0$ limit recovers $w_a=-1.58(1+w_0)$; verified
   by sympy `assert` in the script. Expansion breaks down at $\xi\sim 1/6$
   (conformal), well above the Cassini bound.

## What held, what didn't

- **Held.** Both limits pass. PPN form matches the Will 2014 review Eq.~(5.18)
  after identification. Matter-era coefficient $24/7$ from D4 is reproduced as
  $A(0)=24/7$ in the $\Omega_\Lambda\!\to\!0$ limit of Scherrer-Sen.
- **Held (reluctantly).** The $B(\Omega_\Lambda)=(8/\sqrt3)A$ scaling is
  heuristic: it propagates the matter-era D4 ratio $\delta_\xi=8\xi\chi/(\alpha M_P)$
  straight into the $\Omega_\Lambda=0.7$ regime. A full numerical integration
  of the NMC background ODEs could shift $B$ by an O(1) factor. I have flagged
  this explicitly in Caveat 2 of the .tex. The sign and scaling with
  $\xi\sqrt{1+w_0}$ are robust.
- **Didn't.** LaTeX standalone compile was blocked by the sandbox
  (pdflatex not permitted); I verified syntax manually. No compile failure
  expected --- only `\cite{}` keys already present in `eci.bib`
  (BertottiIessTortora2003, ScherrerSen2008, DESIDR2, Biskupek2021); the
  Damour/Chiba/Hwang references are cited inline without `\cite{}` to avoid
  editing the bib.

## Numerical outcome

- $|\xi_\chi|_{\max}=2.4\!\times\!10^{-2}$ at $\chi_0=M_P/10$.
- ECI half-band in $w_a$ at $w_0=-0.75$: $\Delta w_a^{\rm ECI}\approx 8.8\!\times\!10^{-3}$.
- DESI DR2 $\sigma_{w_a}\approx 0.8$ ⇒ **band is $\sim 1.1\%$ of 1σ**.

## Verdict

**ECI is NOT discriminative from $w$CDM at DESI DR2.** The Cassini-allowed
NMC band lies entirely inside the DR2 $1\sigma$ contour and is narrower than
the Scherrer-Sen line itself. The discriminative observable moves to:
- DESI DR3 (forecast $\sigma_{w_a}\sim 0.25$) — still marginal,
- LSST Y10 ($\sigma_{w_a}\sim 0.08$) — ECI band then $\sim 10\%$ of 1σ, so
  Prediction 1 becomes a genuine falsifier only in the 2028--2032 window.

Row **1b** appended to the predictions table in `eci.tex` (with the required
`% TODO REMONDIERE: validate` flag).

## Surprises / follow-ups

- The PPN bound is surprisingly weak (quadratic in $\xi$). A linear coupling
  $\beta R\chi$ would give $|\beta|\lesssim 10^{-5}$; the $\xi R\chi^2/2$ form
  of ECI is genuinely less constrained by solar-system tests.
- A chameleon/symmetron screening would decouple the local $\chi_0$ from the
  cosmological one and further weaken the bound. Worth mentioning in v4.2.
- The true DR3 falsifier is probably not the $(w_0,w_a)$ distance itself but
  the **shape** of the thawing trajectory (curvature in the $w(a)$ history).
  Cross-correlation with structure growth is where the real signal lives.

## Deliverables

- `derivations/D7-plan.md`
- `derivations/D7-ppn-xi-bound.py` (sympy + matplotlib, self-verified)
- `derivations/figures/D7-xi-w0-wa.{pdf,png}`
- `paper/section_3_5_constraints.tex` (~1.5 pages, ready to `\input`)
- `paper/eci.tex` — one row appended to predictions table (row 1b, with TODO)
- 5 commits pushed to `master`.
