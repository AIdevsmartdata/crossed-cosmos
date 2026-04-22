# V8-agent-15 — Heat-kernel spectral action Λ audit

**Date:** 2026-04-22  
**Verdict:** FINITE-WRONG-ORDER  
**Script:** `derivations/V8-agent-15-heat-kernel-lambda.py`

---

## Analogy tested

Chamseddine–Connes 1996 [CC96, Commun. Math. Phys. 186, 731] + CCM 2007
[Adv. Theor. Math. Phys. 11, 991] spectral action `S = Tr f(D/Λ)` with
heat-kernel expansion `Tr(e^{−tD²}) = Σ_k a_k t^{(k−4)/2}`.
Applied to `D_ZSA = D_M ⊗ 1 + γ ⊗ H_ζ` with 10^5 Odlyzko zeros as
`H_ζ` spectrum; rigorous Mellin–UV/IR cutoff at `t_UV=1` (Planck) and
`t_IR = 1/H_0^2 ~ 7×10^{121}`.

---

## Key numerical results

| Quantity | Value |
|---|---|
| `ρ_Λ^spec / M_P^4` at `Λ = M_P` | `1.27 × 10^{−2}` |
| `Λ_obs / M_P^4` | `1.07 × 10^{−122}` |
| Discrepancy | **`1.2 × 10^{120}`** |
| `a_4^ζ = ζ_{H_ζ}(4)/(4π²)` | `1.08 × 10^{−3}` (dimensionless) |
| Arithmetic residue `Δ/K` at `t=10^{−8}` | `0.002` (UV) |
| Arithmetic residue `Δ/K` at `t=10^{−3}` | `0.22` (F-7 scale) |

---

## Why it fails

**The cosmological constant lives in `a_0`, not `a_4`.** The spectral
action CC term is `ρ_Λ^spec ∝ f_2 Λ^4/(4π²)` — quartic in the UV
cutoff. At `Λ ~ M_P` it exceeds `Λ_obs` by 120 orders.

The ζ-zero sector contributes to the **curvature-squared** coefficient
`a_4` (a dimensionless `O(1)` rescaling of `R²`, `R_{μν}²` terms), not
to the vacuum energy. `ζ_{H_ζ}(4) = 4.26 × 10^{−2}` → `a_4^ζ ~ 10^{−3}`:
finite, wrong tensor structure to help with `Λ_obs`.

The arithmetic residue `Δ(t) = K_ζ − I_smooth` is `O(10^{−3})` to
`O(10^{−2})` of `K_ζ` at small `t`, confirming the F-7
Trivial-Cancellation structure with a log dressing. CC96 §4 and CCM07 §4.5
explicitly acknowledge that the spectral action CC requires fine-tuning or
SUSY cancellation; adding Riemann zeros gives an `O(1)` rescaling of `a_4`,
not a natural suppression of `a_0`.

---

## Verdict: FINITE-WRONG-ORDER

Consolidates **F-7**. No new hook. The heat-kernel spectral action route is
closed: it produces the standard quartic CC problem irrespective of the
Odlyzko spectrum in `H_ζ`.
