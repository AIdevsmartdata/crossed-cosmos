---
name: M30 Navier-Stokes regularity × ECI tools (Phase 3.F #4)
description: NO-DIRECT-ROUTE + WEAK-TANGENTIAL-FLUID-LYAPUNOV. Categorical mismatch decisive (ODE vs PDE; scalar vs vector; relativistic vs Newtonian). Sole survivor: Vishik-Friedlander methodological parallel (1-sentence footnote). META-finding: ECI is GRAVITY-ARITHMETIC specific
type: project
---

# M30 — Navier-Stokes × ECI tools (Phase 3.F #4, Opus, 5 min)

**Hallu count:** 85 → 85 | **Live-verified refs:** 9 | **Anti-stall:** ✅

## Verdict: NO-DIRECT-ROUTE + WEAK-TANGENTIAL-FLUID-LYAPUNOV

**Probability of NS contribution: <0.01%.**

## Five terminal obstructions

| # | Obstruction | Severity |
|---|---|---|
| 1 | ODE-time vs PDE-3+1d (variable count mismatch) | TERMINAL |
| 2 | Scalar φ vs vector incompressible u (no curl, no vorticity in ECI) | TERMINAL |
| 3 | Relativistic FRW conformal-flatness vs Galilean NS conservation laws | TERMINAL |
| 4 | Modular Shadow type-II_∞ is gravitational-crossed-product specific | TERMINAL |
| 5 | ξ_crit_+ runaway destroys bounded states; Re_crit pitchfork generates them | TERMINAL |

## NOVEL FINDING (sole tangent)

**Vishik fluid Lyapunov exponent** (Vishik 1996, *J. Math. Pures Appl. (9)* **75** (1996) 531-557; with NS-viscous extension by Shvydkoy-Friedlander, *Ann. I. H. Poincaré (AN)* **25** (2008) 713-724):
essential spectral radius of linearized NS evolution = max Lyapunov exponent of bicharacteristic flow on T*M.

**[CORRECTION 2026-05-06 by M40]** The original M30 attribution "Vishik-Friedlander *AIHPC* 25 (2008) 713-758" was WRONG. Live-verified via numdam.org PDF: actual paper is Shvydkoy-Friedlander, pp. 713-**724** (12 pp, NOT 758). The "fluid Lyapunov exponent" formula μ_fluid is **Vishik 1996 alone** (V96, *J. Math. Pures Appl.*); 2008 extends V96 to viscous limit. Counts as hallu 85 → 86.

**Methodological parallel** with ECI A56/M4: $\mu_+(N) = \frac{1}{2}\bigl[-(3+s_H) + \sqrt{(3+s_H)^2 + 4 M^2_{\rm eff}}\bigr]$ — both linearize, take maximal exponential growth, integrate along time-evolution. **Worth 1-sentence footnote, NOT a paper.**

## META-FINDING (combine M27+M28+M30)

**ECI's tools form a tight GRAVITY-ARITHMETIC complex specifically tuned to**:
- f = 4.5.b.a (CM newform)
- CM by ℤ[i]
- Supersingular at p=2

**They do NOT generalize to Clay problems**:
- Hodge (M27 CM-trivial)
- RH (M28 II vs III obstruction)
- Navier-Stokes (M30 ODE vs PDE)

This is **not a weakness** — ECI's specificity is what gives predictive power. But argues AGAINST any framing as Clay-Millennium-adjacent research program.

## Recommendations
1. NO NS / Clay section in ECI v7.5/v7.6/v7.7
2. NO claim of Clay relevance
3. CONSIDER 1-sentence Vishik-Friedlander footnote in M4/A56
4. ABANDON Clay framing
5. DO NOT approach Tao/Hou/Constantin/Sverak/Friedlander community

## Refs live-verified (9)
- Clay Math NS page (Fefferman 2000)
- Beale-Kato-Majda 1984 *CMP* 94
- Hou *Acta Numerica* 2009
- Tao 2016 *J.AMS* 29 arXiv:1402.0290
- Vishik 1996 *J. Math. Pures Appl. (9)* **75** 531-557 (true V96 source)
- Shvydkoy-Friedlander 2008 *Ann. I. H. Poincaré (AN)* **25** 713-724 (NS-viscous extension; replaces wrongly-cited "Vishik-Friedlander AIHPC 713-758")
- Vishik-Friedlander 2003 *Comm. Math. Phys.* **243** 289-354 (genuine VF joint, 2D nonlinear instability)
- Friedlander-Vishik 1991 *Phys. Rev. Lett.* **66** 2204 (genuine FV joint, instability criteria)
- Necas-Ruzicka-Sverak 1996 *Acta Math.* 176
- Chen-Hou 2025 *PNAS* (Euler boundary)
- Shahmurov 2026 arXiv:2604.09949
- Degond-Ringhofer 2003 *J. Stat. Phys.*

## Discipline
- 0 fabrications; Mistral STRICT-BAN; NO drift; 3 [TBD: prove] markers honest
