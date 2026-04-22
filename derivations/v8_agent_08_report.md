# v8-agent-08 — Species-scale c' ↔ modular anomalous dimension

**Date.** 2026-04-22
**Verdict.** FRAMEWORK-MISMATCH

---

## 1. Setup

Species scale (MVV22 Eq. 2.2; AAL23):
$$\Lambda_{\rm sp}(H) = M_P\bigl(H/M_P\bigr)^{c'}$$
ECI anchor (GROUND_TRUTH A5): $c' = 1/6$ (fifth-force bound $c'<0.2$).
Literature range (full DD scenario): $c' \in [1/3, 1/2]$.

Modular anomalous dimension of the mass operator $m^2\chi^2$ under
$\sigma^R_\tau$ (Tomita–Takesaki flow, Bisognano–Wichmann Rindler limit)
on the v6 quintessence background with $\mathcal{L} \supset -\tfrac{1}{2}\xi_\chi R\chi^2$:

$$\gamma_m := \frac{d\log m_{\rm eff}}{d\log(H/M_P)}$$

## 2. Computation

On quasi-dS ($R = 12H^2$, $H$ = const):

| Regime | $m_{\rm eff}^2$ | $\gamma_m$ |
|---|---|---|
| NMC-dominated ($\xi_\chi R \gg V''$) | $12\,\xi_\chi H^2$ | $1$ |
| Potential-dominated ($V'' \gg \xi_\chi R$) | $\alpha^2 V_0/M_P^2$ (const) | $0$ |

Ratios: $\gamma_m^{\rm NMC}/c'_{\rm ECI} = 6.0$;
$\gamma_m^{\rm NMC}/c'_{\rm lit\,mid} = 2.4$;
$\gamma_m^{\rm NMC}/c'_{0.29} = 3.45$.

## 3. Verdict

**FRAMEWORK-MISMATCH.** $\gamma_m$ is a kinematic exponent fixed by the
conformal weight of the mass operator in the Rindler/dS modular picture
($\gamma_m \in \{0,1\}$ from background geometry). $c'$ is a Swampland
parameter encoding the asymptotic KK-tower species density
$N_{\rm sp} \sim (M_P/\Lambda_{\rm sp})^{1/c'}$. Bridging the two
requires the identification "KK-tower density of states = modular spectral
density of $\mathcal{A}_R$", which has no support in the literature or in
the derivation cache. The analogy is ANALOGY-only (FAILED F-8 pattern:
exponent without theoretical principle). No OFF-BY-FACTOR rescue is
possible: $\gamma_m/c' \approx 6$ (ECI) is not a small rational, and the
two objects are dimensionally and conceptually distinct.

*Rules checked: V6-1 (no inequality promoted), V6-4 (no new cosmological
claim), PRINCIPLES rule 1 (honesty gate — all numbers symbolic/GT-anchored),
PRINCIPLES rule 12 (no bib edit), FAILED F-3 (no Planck-freq substitution),
FAILED F-8 (no exponent scan).*
