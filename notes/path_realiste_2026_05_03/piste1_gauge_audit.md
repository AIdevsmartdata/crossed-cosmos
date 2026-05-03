# Piste 1 Gauge-Invariance Audit (Mistral counter-review)

**Date:** 2026-05-02. **Author:** Opus 4.7 sub-agent, max-effort.
**Source:** /tmp/piste1_hubble_kc.{md,py,tex} (commit 1b2d055).
**Adversarial input:** /tmp/mistral_v620_review.txt (Mistral large-latest).
**This audit:** sympy-verified, /tmp/piste1_gauge_audit.py.

## Mistral's claim under scrutiny

> "The 1/(2t) scaling is not robust to gauge transformations. If you change
> the slicing (e.g., to proper time), the match breaks."
> — Mistral large-latest, /tmp/mistral_v620_review.txt §B

Translation: Piste 1 derives `(1/C_k) dC_k/dt = 1/(2t) = H_rad(t)` via a
Casini-Huerta-Myers (2008) Jacobian `ds/dt = 1/(2π R_proper)`, where the
final `t` is interpreted ambiguously. Mistral suspects the match works in
conformal time `η` but breaks in cosmic (proper) time `t`.

## Setup — what does Piste 1 actually use?

CMPT24 universal late-modular-time slope: `(1/C_k) dC_k/ds = λ^mod_L = 2π`,
where **`s` is the parameter of the modular automorphism `Δ^{is}` (Tomita–
Takesaki)**, intrinsic to the algebra (web search of arXiv:2306.14732
confirms; cf. also Vardian 2026 arXiv:2602.02675 eq.(74); Aguilar-Gutierrez
2025 arXiv:2511.03779; Parker et al. 2019 arXiv:1812.08657).

CHM08 (eq. 3.16) Unruh-temperature relation at the *center* of a diamond:
`ds/dτ_proper = 1/(2π R_proper)`, where `R_proper = a(η_c) · R_conf` is the
**gauge-invariant proper radius** of the diamond at its bifurcation slice.

Combining: `(1/C_k) dC_k/dτ_proper = λ^mod_L · ds/dτ_proper = 1/R_proper`.

For the comoving observer in FRW, `τ_proper ≡ t` (cosmic time). So:

> **Piste 1's true content:**  `(1/C_k) dC_k/dt = 1 / R_proper(η_c)`.

This is a *scalar equation* on the observer's worldline. Both sides
transform identically under any reparametrisation `t → t'(t)`: by the
chain rule, `dC_k/dt' = (dC_k/dt)·(dt/dt')`, and `1/R_proper` is a
spacetime scalar (no time-coordinate dependence). **It is manifestly
gauge-invariant in Mistral's specific sense (slicing).**

## Sympy results (era-by-era; deliverable §1–4)

For all three eras, sympy computes both `H(t)` (textbook) and the Piste 1
rate `1/R_proper(η_c)` directly, in BOTH `η` and `t`, then the ratio.

| Era | a(η) | t(η) | H(t) | Diamond conv. | Piste 1 rate / H(t) |
|---|---|---|---|---|---|
| Radiation | `a₀ η`   | `a₀ η²/2` | `1/(2t)` | PLC, R_conf=η_obs | **1** (exact) |
| Matter    | `a₀ η²`  | `a₀ η³/3` | `2/(3t)` | PLC, R_conf=η_obs | **1/2** |
| Matter    | `a₀ η²`  | `a₀ η³/3` | `2/(3t)` | Hubble-horizon    | **1** (tautological) |
| de Sitter | `−1/(H_dS η)` | `−log(−H_dS η)/H_dS` | `H_dS` | H-horizon (R_proper=1/H_dS) | **1** (tautological) |

Sympy verifies (ratios computed in *cosmic time t*, using
`η(t)=√(2t/a₀)` for radiation, `η(t)=(3t/a₀)^{1/3}` for matter):

- Radiation PLC: `(1/C_k)dC_k/dt = 1/(2t) = H(t)`. **MATCH in both η and t.**
- Matter PLC: `(1/C_k)dC_k/dt = 1/(3t)`, vs `H(t) = 2/(3t)`. **OFF BY 1/2** (i.e. ratio = `(d log a / d log η)^{−1} = 1/p` for `a∝η^p`).
- dS Hubble-horizon: `(1/C_k)dC_k/dt = H_dS`. **MATCH** (by construction of the diamond).

## Why does Mistral's "slicing" objection fail in the strict sense?

The chain-rule sanity check (sympy direct): going through `η` first, the rate is
`1/(a(η_c)·R_conf)`; going through `t` first, the rate is `1/R_proper(t)`;
these are LITERALLY THE SAME function evaluated at the SAME spacetime point.
There is no separate "rate in η" and "rate in t" that could disagree — both
are values of the spacetime scalar `1/R_proper` at the observer.

## Geometric reformulation — what Piste 1 actually says

**Theorem (sympy-checked, conjectural at the operator-algebra level):** In
any FRW background, for the comoving observer at the centre of a
spacelike-symmetric diamond `D_O ⊂ FRW`, the Krylov modular complexity
on the type II_∞ crossed product `A(D_O)⋊_σℝ` satisfies, in the late-
modular-time asymptotic regime,

```
    (1/C_k(t)) dC_k(t)/dt   =   1 / R_proper(t)   +  O(C_k^{-1}) .
```

Special cases:
- Radiation + past-light-cone (`R_conf = η_obs`): RHS = `1/(2t) = H(t)`.
- de Sitter + Hubble-horizon: RHS = `H_dS = H(t)`.
- Matter + past-light-cone: RHS = `1/(3t) = (2/3) H(t)`.
- Matter + Hubble-horizon: RHS = `H(t)` (tautology).

**The match `rate = H(t)` is era-dependent and diamond-convention-dependent
— but the underlying identity `rate = 1/R_proper` is era-independent.**

## Verdict

**GAUGE-INVARIANT-AFTER-CAREFUL-INTERPRETATION.**

- *Strict sense* (Mistral's literal claim, "breaks under proper-time
  slicing"): **REFUTED.** Both sides are scalars on the worldline; the
  match in `η` and the match in `t` are the same equation. Sympy verifies.

- *Spirit* (Piste 1 over-claimed as a universal cosmological identity):
  **PARTIALLY CORRECT.** The substantive content is `rate = 1/R_proper`;
  the H-match is a feature of the diamond convention, exact only for
  radiation+PLC and dS+Hubble-horizon. For matter+PLC the ratio is 1/2.

## Recommended downgrade & reframe

**Old framing (v6.0.20):** "Piste 1 = partial positive: H(t)=Krylov rate
in radiation FRW."

**New framing (post-audit):** "Piste 1 = **geometric Krylov–proper-radius
correspondence** for type II_∞ FRW crossed-product algebra:
`(1/C_k)dC_k/dt = 1/R_proper(t)`. The Hubble identity `H = 1/R_proper`
holds for radiation+PLC and dS+horizon by Friedmann arithmetic, not by
deeper structure."

**Status of Piste 1 as a 'paper-worthy' result:** still YES, but title
must be *"Krylov–Modular–Diameter correspondence on type II_∞ FRW
crossed product"*, not *"Hubble = Krylov rate"*. The cosmological-Hubble
headline is era/diamond-conditional.

## Sources verified (web search, 2026-05-02)

- **arXiv:2306.14732** Caputa-Magán-Patramanis-Tonni (PRD 109 086004,
  2024): `λ^mod_L = 2π` in modular-time `s` (parameter of `Δ^{is}`,
  Tomita-Takesaki). Web search confirms `s` is intrinsic, not cosmic.
- **arXiv:1812.08657** Parker et al. (PRX 9 041017, 2019): finite-dim
  universal operator growth, `b_n = O(n) ⇒ C(t) = O(e^{2αt})`, time
  parameter is the system Hamiltonian's `t`.
- **arXiv:2511.03779** Aguilar-Gutierrez (2025): DSSYK Krylov on type
  II_1, modular time intrinsic to algebra (closest published precedent
  for Piste 1's II_∞ extension).
- **CHM08** Casini-Huerta-Myers, JHEP 0805:012 (2008), eq. (3.16):
  `T_local = 1/(2π R_proper)` at diamond center (used in Jacobian).
- This audit script: /tmp/piste1_gauge_audit.py.

## Files

- /tmp/piste1_gauge_audit.py (sympy script, runs end-to-end)
- /tmp/piste1_gauge_audit.md (this document)
- /tmp/piste1_gauge_audit.tex (LaTeX writeup, mirror of this content)
