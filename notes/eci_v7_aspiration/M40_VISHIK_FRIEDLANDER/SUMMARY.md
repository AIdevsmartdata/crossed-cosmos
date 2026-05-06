---
name: M40 Vishik-Friedlander deeper exploration
description: FOOTNOTE-ONLY verdict (matches M30). Critical correction: M30 misattributed Shvydkoy-Friedlander 2008 as "Vishik-Friedlander AIHPC 713-758" (true: 713-724). True V-F bridge is Vishik 1996 J. Math. Pures Appl. 75 alone. Hallu 85 → 86
type: project
---

# M40 — Vishik-Friedlander deep exploration (Phase 3.F deepening)

**Date:** 2026-05-06
**Owner:** Sub-agent M40 (Opus 4.7, max-effort, ~5min)
**Hallu count:** 85 → **86** (M30 misattribution detected & corrected)
**Live-verified refs:** 4 (V96, VF03, VF93, FV91 + Shvydkoy-Friedlander 2008)

## Verdict: FOOTNOTE-ONLY (1 sentence)

3-5pp methodology paper NOT viable. No functor between cosmic-time scalar
ODE Lyapunov μ_+(N) and infinite-dim PDE fluid Lyapunov μ_fluid. Shared formula
λ = lim (1/t) log‖U(t,t₀)‖ is just the *definition* of any Lyapunov exponent.
No tool transfer either direction. *Phys. D Nonlinear Phenomena* would polite-reject.

## Critical correction to M30 (live-verified via numdam.org PDF)

M30 SUMMARY cited "Vishik-Friedlander *AIHPC* 25 (2008) 713-758" — **WRONG**:
- True authors: **Shvydkoy-Friedlander** (NOT Vishik-Friedlander)
- True page range: **713-724** (12pp, NOT 758)
- DOI: 10.1016/j.anihpc.2007.05.004

The "fluid Lyapunov exponent" / essential spectral radius formula is **Vishik 1996 alone** (V96, *J. Math. Pures Appl. (9)* **75** (6) 531-557, MR97k:35203). The 2008 paper extends V96 to viscous NS limit, by Shvydkoy-Friedlander. Genuine V-F joint papers are VF03 (CMP 243, 289-354) and VF93 (J. Math. Pures Appl. 72, 145-180) and FV91 (PRL 66, 2204).

**Counts as hallu 85 → 86** (M30 sub-agent fabrication, A52-class precedent).

## T1-T3 results

- **T1 functorial relationship:** NONE. ECI = autonomous 2×2 ODE; V96 = infinite-dim semigroup with bicharacteristic flow on T*M. Categorically disjoint.
- **T2 mathematical depth:** Disjoint machinery. ECI eigenvalue = undergrad linear algebra; V96 = WKB/Eikonal/Oseledets cocycle on T*M-bundle.
- **T3 cross-tool transfer:** None either direction. ECI's 0 spatial dim makes WKB empty; "integrate largest eigenvalue" predates both (Floquet 1883, Lyapunov 1892).

## 1-sentence footnote (for eci.tex M4 / §ξ_crit)

> The integrated growth criterion $\int \mu_+(N)\,dN > \log(1/(\sqrt{\xi}\,\phi_0))$
> used here is the cosmic-time scalar-field analogue of the well-known fluid
> Lyapunov-exponent criterion of Vishik (*J. Math. Pures Appl.* **75** (1996)
> 531-557), which gives the essential spectral radius of the linearized Euler
> evolution semigroup as $\rho_{\rm ess}(e^{tL_E}) = \exp(t\,\mu_{\rm fluid})$
> via the bicharacteristic flow on $T^*M$; the parallel is purely formal —
> no functor relates the finite-dimensional ODE setting to the infinite-dimensional
> PDE one.

## Recommendations
1. NO 3-5pp methodology paper
2. ADD 1-sentence footnote (above) to eci.tex M4 §ξ_crit, with bibitem `Vishik1996JMPA`
3. UPDATE M30 SUMMARY.md (DONE 2026-05-06)
4. UPDATE eci.bib if Vishik1996JMPA not present
5. UPDATE auto-memory: hallu 85 → 86 (M30 V-F misattribution)

## Discipline
- 0 new fabrications by M40
- 1 pre-existing M30 fabrication corrected (counts as hallu+1 per A52 precedent)
- AIHPC PDF live-downloaded (197 KB) and pp. 1-2 + 11-12 directly inspected
- Mistral NOT used; NO drift to settings.json
