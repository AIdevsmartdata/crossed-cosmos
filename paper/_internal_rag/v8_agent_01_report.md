# v8_agent_01_report.md — Logistic envelope ↔ Fermi-Dirac MaxEnt

**Agent:** agent-01 | **Date:** 2026-04-22 | **Script:**
`derivations/V8-agent-01-fermi-logistic.py`

**Rules checked:** PRINCIPLES rule 1, rule 12, V6-1, V6-4.
**FAILED.md match:** none — task not blocked.

---

## VERDICT: CONDITIONAL-YES

The logistic envelope `C_k(1 − C_k/C_k^max)` emerges from a MaxEnt
argument in **two exact steps** plus **one physical postulate** (M1).

---

## Derivation summary

**Setup.** Complexity-budget ensemble: states `|n⟩`, `n = 0,…,C_max`,
Gibbs weights `p_n = exp(−βn)/Z`, constraint `⟨C⟩ = fixed`.

**Step 1 — Legendre identity (EXACT).**
`S_Gibbs = log Z + β⟨C⟩` implies `dS_Gibbs/d⟨C⟩ = β` exactly, by the
standard convexity argument:

```
dS_G/d⟨C⟩ = (d log Z/dβ)(dβ/d⟨C⟩) + β + ⟨C⟩(dβ/d⟨C⟩) = β  QED
```

Numerical cross-check (N=50, β ∈ [0.05, 2.0]): max relative error
`1.0×10⁻³` (finite-difference artefact only).

**Step 2 — Rate operator (EXACT given definition).**
Define `R̂` with eigenvalues `R_n = (C_max − n)/C_max`.
By linearity of expectation:

```
⟨R̂⟩ = 1 − ⟨C⟩/C_max   [exactly; max abs error 2×10⁻¹⁶]
```

This is the capacity-fraction remaining: physically, the fraction of
the complexity budget not yet consumed.

**Step 3 — Logistic bound (CONDITIONAL on M1 postulate).**
Postulate (M1): `d⟨C⟩/dτ_R ≤ κ · ⟨C⟩ · ⟨R̂⟩` (capacity-limited rate).
Then:

```
dS_G/dτ_R  =  β · d⟨C⟩/dτ_R
           ≤  β·κ · ⟨C⟩ · (1 − ⟨C⟩/C_max)
           =  κ_R · C_k · (1 − C_k/C_k^max)
```

with `κ_R := β·κ`. This is **eq:logistic of Prop. 1 (v6.1)** (without
the `Θ` factor, which enters from the PH_k activator via the main
bound — unchanged).

---

## Fermi-Dirac analogy: ANALOGY, not isomorphism

| Object | FD (binary occupation MaxEnt) | Gibbs complexity ensemble |
|---|---|---|
| Distribution | `f_n = 1/(exp(β(E_n−μ))+1)` | `p_n = exp(−βn)/Z` |
| Blocking factor | `(1−f_n)` — single-level | `⟨R̂⟩ = 1−⟨C⟩/C_max` — global |
| At half-filling/half-complexity | `(1−f_μ) = 1/2` | `1−C_max/(2C_max) = 1/2` |
| Origin | Pauli exclusion per level | Capacity budget, mean-field |

The two blocking factors coincide numerically at `⟨C⟩ = C_max/2`
(`β → 0⁺`) and both vanish at saturation. The analogy is **structurally
sound as motivation**; it is not an algebraic identity. The FD factor
`(1−f_n)` is a single-level quantity; `(1−C/C_max)` is a global
mean-field quantity.

---

## Implications for v6.1

1. **Prop. 1 is strengthened**: the logistic envelope is now supported
   by a MaxEnt Legendre argument, not only by Brown–Susskind analogy.
   M1 in v6.1 can be rephrased as "capacity-limited rate law in the
   Gibbs complexity ensemble."

2. **M1 remains POSTULATE**: Step 3 above is still a physical
   assumption. MaxEnt delivers Steps 1–2 exactly; Step 3 is the
   M1 content. Nothing in the derivation promotes M1 to DERIVED.

3. **FD analogy can be cited as MOTIVATION** in §3 of v6.1 (under M1
   label), provided it is not described as an exact identification.

4. **Inequality preserved throughout** — V6-1 compliant.
   No cosmological claim — V6-4 compliant.
   All claims bounded by the derivation — rule 12 compliant.

---

## Artefact

`derivations/V8-agent-01-fermi-logistic.py` — sympy symbolic proof
(Parts 1–2) + numerical cross-check (Part 3), self-contained, reproducible.
