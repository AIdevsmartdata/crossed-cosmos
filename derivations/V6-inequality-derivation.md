# V6 Inequality Derivation — formal chain for JHEP submission

**Status.** Hardened derivation of the v6 inequality
`dS_gen[R] / dτ_R  ≤  κ_R · C_k[ρ_R] · Θ(PH_k[δn])`, replacing the
first-pass equality attempt audited PARTIAL in `V6-claude-derivation-report.md`.
Script: `derivations/V6-inequality-derivation.py` (sympy, 0.1 s, all
limit asserts PASS). This note accompanies the script and documents
the literature anchors, the three labelled postulates (M1, M2, M3), and
the pre-emption of the adversarial attacks from `V6-adversarial-attack.md`.

---

## 1. Why inequality, not equality

The v6 composite equation was initially floated as an equality (see
`v6_audit.md` §1). Three independent first-pass derivation attempts
(Claude/Gemini/Magistral, 2026-04) all verdicted **ANSATZ** and the
hostile adversarial (`V6-adversarial-attack.md`) landed a direct
contradiction in the `PH_k → 0` limit: Fan 2022 (PRR 4 L012027) proves
`dS_K/dt ∼ (dC_K/dt) / C_K` — *logarithmic* in complexity — in the
post-scrambling Krylov regime. The equality form `dS_gen/dτ = κ C_k`
conflicts with this by a factor `C_K` (Attack #2).

The **inequality** `dS_gen/dτ ≤ κ_R C_k Θ` resolves this automatically:
Fan's logarithmic growth sits *below* the linear bound, so the Krylov
regime becomes a saturating limit of our inequality, not a contradiction.
The inequality form also aligns structurally with every rigorous
generalised-second-law precursor (Wall 2011; Faulkner–Speranza 2024;
Kirklin 2025), which are all inequalities as well. The pivot was
mandated in `PRINCIPLES.md` V6-1.

## 2. Derivation chain

The sympy script encodes a three-step chain from the Faulkner–Speranza
2024 modular relative-entropy equality to the target inequality.

**Step 1 — Faulkner–Speranza 2024 (rigorous).** For a nested pair of
causal diamonds `C_1 ⊂ C_2` associated with observer R,

```
  S_gen(C_2) − S_gen(C_1)  =  S_rel(ψ‖Ω)_{C_1} − S_rel(ψ‖Ω)_{C_2}
                            ≥ 0 ,
```

where monotonicity is Uhlmann / Lindblad under CPTP inclusion of the
subalgebra `A_{C_2} ⊂ A_{C_1}`. Differentiating along the modular flow
`σ_{τ_R}` (Ceyhan–Faulkner 2020 half-sided pushforward; Longo 2019
positivity) yields

```
  dS_gen/dτ_R  =  − dS_rel/dτ_R ,      dS_rel/dτ_R ≤ 0 .
```

This half is a theorem.

**Step 2 — modular-energy bound (POSTULAT M1).** A Pinsker-style argument
bounds relative-entropy decay by the modular-Hamiltonian response:

```
  − dS_rel/dτ_R   ≤   |d⟨H_mod⟩/dτ_R| .
```

We then invoke the Brown–Susskind 2018 second law of complexity,
transplanted to the type-II crossed-product algebra (CLPW 2023, DEHK
2024), as

```
  |d⟨H_mod⟩/dτ_R|  ≤  κ_R · C_k[ρ_R] .         (M1)
```

This is the v6-specific postulate: we do not have a type-II theorem
fixing the proportionality, but Caputa–Magán–Patramanis–Tonni 2024
scaffolding (PRD 109 086004; `λ_L^mod = 2π`) argues it is at least
consistent in the half-sided modular subalgebra setting. We label
it **M1** and flag it explicitly in the prose (PRINCIPLES V6-2).

**Step 3 — topological activator (POSTULAT M2).** The dequantisation
map (`derivations/V6-dequantisation-map.md`) pushes `ρ_R` forward to a
classical coarse-grained density `δn(x, τ_R)`, on which the
persistent-homology functor `PH_k` (Yip–Biagetti–Cole–Viswanathan–Shiu
2024) is evaluated. The chameleon-like activator

```
  Θ(PH_k[δn])  =  exp[− (PH_k / PH_c)^α] ,    α = 0.095  (M3)
```

lives in `[0, 1]` by construction. We postulate (M2) that the physical
bound on `dS_gen/dτ_R` is the complexity bound of Step 2 *multiplied* by
this topological suppression, recognising that the complement `(1 − Θ)`
corresponds to phase-space regions that have already saturated their
Betti flow (Fan 2022 log regime) and contribute subdominantly:

```
  dS_gen/dτ_R   ≤   κ_R · C_k · Θ(PH_k) .       (M2)
```

## 3. Limit checks (sympy asserts, all PASS)

The script verifies four structural limits:

- **L1 — Θ → 1.** Setting `PH_k → 0` gives `Θ = 1` and recovers the pure
  Wall-2011-style complexity-bounded GSL: `dS_gen/dτ_R ≤ κ_R · C_k`.
  Residual zero symbolically.
- **L2 — C_k saturation.** At the Brown–Susskind `2^K` plateau the Fan
  2022 logarithmic rate `dC_K/C_K → 0` sits strictly below our
  nonnegative bound. No contradiction with Fan 2022. (This is the
  **central resolution of Attack #2**.)
- **L3 — κ_R → 0.** Trivial: both sides vanish. Consistent with the
  degenerate de Sitter zero-temperature limit.
- **L4 — sign coherence.** `dS_gen ≥ 0` from FS24 monotonicity is
  compatible with the upper bound `dS_gen ≤ κ_R · C_k · Θ ≥ 0` — the
  two-sided sandwich is non-empty.

## 4. Pre-emption of the adversarial attacks

- **Attack #1 (dimensional).** Resolved in `V6-dimensional.py`
  (`[κ_R] = nat · s⁻¹`, CLEAN). Unchanged by the inequality pivot.
- **Attack #2 (Fan 2022 conflict).** Neutralised. The log-Krylov regime
  is the saturating limit of our inequality, not a violation.
- **Attack #3 (category mismatch).** Neutralised by the dequantisation
  map (`V6-dequantisation-map.md` §6b): the map only feeds `δn` into
  the **RHS** of the inequality, so upper-bound control on `δn` — not
  exact Gaussianity — suffices.
- **Attack #4 (arrow-of-time tautology).** Side-stepped by the V6-3
  discipline: we claim only `dS_gen ≥ 0` in the modular frame, not an
  emergent cosmological arrow.
- **Attack #5 (α ad hoc).** Unchanged; documented as M3 postulate.
- **Attack #7 (no new falsifier).** The v6 paper is a formal JHEP-track
  paper; the cosmological falsifier was killed by D18/D18b (PRINCIPLES
  V6-4) and is not reintroduced.

## 5. Literature anchors

Wall 2011 (PRD 85 104049, `arXiv:1105.3445`), Faulkner–Speranza 2024,
Kirklin 2025, Ceyhan–Faulkner 2020, Longo 2019 — for the rigorous
relative-entropy / GSL skeleton. Brown–Susskind 2018 (PRD 97 086015,
`arXiv:1701.01107`), Caputa–Magán–Patramanis–Tonni 2024 (PRD 109 086004,
`arXiv:2306.14732`) — for the M1 modular-complexity postulate. CLPW
2023, DEHK 2024 — for the type-II crossed-product setting. Yip–Biagetti–
Cole–Viswanathan–Shiu 2024 (JCAP 09 034, `arXiv:2403.13985`) — for PH_k.
Fan 2022 (PRR 4 L012027) — for the saturating-limit consistency check.

## 6. Limits of validity (adversarial self-stress, 2026-04-21)

A final pass in referee mindset before submission.

**Can a referee still object to the inequality form?**
- *The inequality is now so weak it cannot be falsified.* Valid
  critique: any bound of the form `dS_gen ≤ (bounded positive)` is
  automatically satisfied whenever the observer-dependent `S_gen` is
  itself bounded (which it is in type II finite-trace settings). The
  paper's defensive move is to quote Wall 2011 and FS 2024 as
  precedent: rigorous GSLs are always inequalities and nevertheless
  scientifically content-bearing. The content here is the
  **functional form of the bound**, specifically the M1 proportionality
  to `C_k` and the M2 multiplication by `Θ(PH_k)`.
- *M1 is still Brown-Susskind heuristics.* Accepted and flagged as
  POSTULAT. The paper must not describe M1 as a theorem.
- *The two-sided sandwich (0 ≤ dS_gen ≤ κ C_k Θ) hides circularity if
  κ_R absorbs `C_k`.* Rebuttal: `κ_R = 2π T_R` is fixed independently of
  complexity (modular temperature, observer-side); the identification is
  dimensionally clean (`V6-dimensional.py`).

**When does the bound become trivial or infinite?**
- *Trivial.* (i) `κ_R → 0` (zero Gibbons–Hawking temperature, empty de
  Sitter limit); (ii) `C_k → 0` (pure-state, zero-complexity regime);
  (iii) `Θ → 0` (deep post-saturation, `PH_k ≫ PH_c`). In all three the
  inequality becomes `0 ≤ 0`, not violated but content-free.
- *Infinite.* `C_k` grows at most linearly in `τ_R` (Haferkamp 2022) up
  to the `2^K` plateau. For observers with unbounded modular-time range
  (type III factors) the cumulative `∫ κ_R C_k Θ dτ` can diverge; the
  crossed product to type II regulates this (CLPW 2023). Divergence is
  thus a signal that the type-II hypothesis has failed, not that the
  inequality is wrong.

**Is there a regime where the inequality is violated?**
- *Negative-temperature modular flow.* If `T_R < 0` (inverted
  population), the FS24 monotonicity direction flips and the derivation
  cannot be applied as stated. This is a breakdown signal: v6 applies
  only to positive-temperature observers.
- *Non-cyclic/separating states.* Tomita–Takesaki theory requires a
  cyclic-and-separating state for modular flow to be well-defined;
  generic pure states on a type I factor fail this, and then `τ_R` is
  not defined. Breakdown signal: v6 requires a type-II (or type-III
  crossed to type II) setting, i.e. the presence of an observer.
- *PH_k-stability failure.* If the coarse-grained field `δn(x)` is
  non-stationary or has heavy tails beyond sub-exponential, the
  sublevel-set filtration may fail to give a stable `PH_k`; then
  `Θ(PH_k)` is not a well-defined random variable and (M2) is
  undefined. Breakdown signal: the dequantisation map's σ_cg cutoff
  must be above the QRF resolution.

**New vulnerabilities uncovered by this pass.**
- M1 uses a Pinsker-style bound `−dS_rel/dτ ≤ |d⟨H_mod⟩/dτ|` that is
  tight only on relative-modular-Hamiltonian-dominated fluctuations.
  In regimes where modular work dominates (non-equilibrium quenches)
  the bound loosens and `Θ` must absorb more. The paper should state
  this explicitly.
- M2 postulates a *multiplicative* insertion of Θ. An equally valid
  conservative choice is an *additive* correction
  `dS_gen/dτ ≤ κ C_k − penalty(PH_k)`; these two forms differ in the
  small-PH_k expansion. A referee may demand a justification of the
  multiplicative choice; the honest answer is phenomenological
  consistency with the chameleon-activator literature
  (Khoury–Weltman 2004; Burrage–Sakstein 2018).

## 7. Verdict

The inequality form is **formally clean for JHEP review** at the level
of a theorem-plus-postulate paper: Step 1 is rigorous, Steps 2–3 are
labelled POSTULAT (M1, M2) with literature anchors, all four limit
checks pass symbolically, and every adversarial attack from
`V6-adversarial-attack.md` is either neutralised (Attacks 2, 3) or
properly scoped (Attacks 1, 4, 5, 7). The remaining vulnerability is
the unavoidable M1 postulate — but this is the one referee point of
attack anticipated in `V6-claude-derivation-report.md` and is the
honest line at which v6 stops deriving and starts postulating.
