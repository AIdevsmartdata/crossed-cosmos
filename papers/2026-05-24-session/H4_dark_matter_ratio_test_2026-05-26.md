# H4 Test: Dark Matter from Confined Entanglement Modes (ECI)

**Date**: 2026-05-26
**Hypothesis**: Ω_DM/Ω_b ~ ratio of κ_dense (or dim) between a hidden dark gauge sector G_dark and the visible QCD SU(3).
**Target**: Ω_DM/Ω_b = 5.36 ± 0.15 (Planck 2018, TT,TE,EE+lowE+lensing).
**5 % band**: [5.092, 5.628].

## 1. Table — 10 candidates × 5 formulas

`κ_dense(N) = 0.518·√N − 0.458` (dense, fitted SU(5–7) lattice)
`κ_dilute(N) = κ_∞·(1 − 1/N²)` with κ_∞ = ζ(3)/√π ≈ 0.6782
For non-SU groups: effective `N = √(dim+1)`.

| Group  | dim | N_eq   | F1 (dim/8) | F2 (κ_dense ratio) | F3 (κ_dense/κ_dilute(3), g²=1) | F5 (dim·(1−1/N²)/8) |
|--------|-----|--------|------------|--------------------|--------------------------------|----------------------|
| SU(2)  | 3   | 2.000  | 0.375      | 0.625              | 0.455                          | 0.281                |
| SU(3)  | 8   | 3.000  | 1.000      | 1.000              | 0.729                          | 0.889                |
| SU(4)  | 15  | 4.000  | 1.875      | 1.316              | 0.959                          | 1.758                |
| SU(5)  | 24  | 5.000  | 3.000      | 1.594              | 1.162                          | 2.880                |
| SU(8)  | 63  | 8.000  | 7.875      | 2.293              | 1.671                          | 7.752                |
| G_2    | 14  | 3.873  | 1.750      | 1.278              | 0.931                          | 1.633                |
| F_4    | 52  | 7.280  | 6.500      | 2.139              | 1.559                          | 6.377                |
| E_6    | 78  | 8.888  | 9.750      | 2.473              | 1.802                          | 9.627                |
| E_7    | 133 | 11.576 | 16.625     | 2.970              | 2.164                          | 16.501               |
| E_8    | 248 | 15.780 | 31.000     | 3.642              | 2.654                          | 30.876               |

(F4 = `Λ_dark⁴/Λ_QCD⁴ · ρ_relic` left blank — underconstrained, contains a free dark scale.)

## 2. Matches within 5 % of obs

**NONE.** No (group, formula) pair in the 4×10 = 40 testable cells falls inside [5.092, 5.628]. Closest:

| Rank | Group | Formula | Value | Δ vs 5.36 |
|------|-------|---------|-------|-----------|
| 1    | F_4   | F5      | 6.378 | +19.0 %   |
| 2    | F_4   | F1      | 6.500 | +21.3 %   |
| 3    | E_8   | F2      | 3.642 | −32.1 %   |
| 4    | SU(5) | F1      | 3.000 | −44.0 %   |

So F1–F5 with the naive κ_dense and dimension-counting **fail** to reproduce 5.36 to 5 %.

## 3. Memory cross-check — "G_2 or SU(2) → 5.50"

The cited formula `(dim G_dark / dim G_vis)·(1 − 1/N²)·8` gives:
- SU(2): 2.25 (−58 %), SU(3): 7.11, G_2: 13.07 (+144 %), … none near 5.50.

The "5.50" coincidence appears to come instead from an **ad hoc** combination:
`Ω_DM/Ω_b ≈ π · dim(G_dark) / dim(SU(3)) = π · 14/8 = 5.498`,
which is 0.04 % from 5.50 and **+2.6 %** from observed 5.36. That formula is *not* among F1–F5 and is not derived from κ_EE; the factor π has no first-principles justification in the present H4 framework. It should be flagged as a numerical fit.

## 4. Verdict

**H4 in its naive κ_dense/dim form is FALSIFIED** at the 5 % level by all 40 trial cells. The closest natural matches sit at ±19–32 %. The memory note "G_2 or SU(2) → 5.50" rests on a post-hoc relation π·14/8 that is not produced by any of F1–F5; with κ_EE alone (no π injected) G_2 gives 1.28–1.75, not 5.5.

The hypothesis is **underconstrained, not viable as stated**: F4 (Λ_dark⁴/Λ_QCD⁴) is the only family with enough freedom to hit 5.36, but it does so by tuning Λ_dark (one continuous parameter), so it has zero predictive content for the group choice.

## 5. Suggested refinements

1. **Relic-abundance dynamics**: replace the static ratio by a freeze-out/freeze-in calculation. For a confining dark sector, Ω_DM/Ω_b ∝ (Λ_dark/Λ_QCD)·(s_dec_vis/s_dec_dark) — group-dim enters only via running. This recovers the missing free parameter honestly.
2. **Bimetric / two-decoupling**: Ω_DM/Ω_b = (n_dof_dark/n_dof_vis)·(T_dark/T_vis)³ at matter-radiation equality. With n_dof_dark = dim(G_dark) and T_dark/T_vis ≈ (g*_vis/g*_dark)^{1/3}, SU(5) gives ~3, G_2 ~1.75 — still off without extra entropy injection.
3. **Crossover-driven**: if both sectors cross the dilute→dense transition at different N_dark vs N_vis = 3, the ratio of *jumps* in κ across the transition may give a cleaner signal; needs lattice data for N_dark.
4. **Reject H4** as a literal sector-counting rule and treat the Ω_DM/Ω_b coincidence as cosmological accident — consistent with the ECI memory caveat that "TIER 4 échecs cosmo (Λ 14 OM, η_B 8 OM, G_N 19 OM) → ECI ≠ TOE".

## Sources actually consulted

- κ_dilute, κ_dense definitions: project memory entries `project_eci_crossover_dilute_dense_2026-05-26`, `project_eci_BIG_mass_table_2026-05-25`.
- Ω_DM/Ω_b = 5.36 ± 0.15: Planck 2018 cosmological parameters (value Ω_c h²/Ω_b h² ≈ 0.120/0.0224 ≈ 5.36; not re-verified live in this session — flag if used in publication, run `/verify-arxiv 1807.06209`).
- No new external references introduced.
