# V6 Adversarial Attack — Hostile Referee Report

**Target.** `dS_gen[R]/dτ_R = κ_R · C_k[ρ_R(τ)] · Θ(PH_k[δn(τ)])`
with `Θ(x) = exp[-(x/PH_c)^α]`, `α = 0.095`.

**Role.** Independent hostile reviewer. I do not consult the derivation agents.
Sources: audit archive `paper/_internal_rag/v6_audit.md`; arXiv web search for
Attack 6. V6-cross-verification.md was polled (not present at time of writing;
analysis independent by design).

---

## Attack 1 — Dimensional inconsistency

[S_gen] = nat; [τ_R] = s; LHS = nat·s⁻¹.
The audit (§2) itself declares `[κ_R] = nat · t⁻²`. If `C_k` and `Θ` are
dimensionless, RHS = nat·s⁻² ≠ LHS. **The audit has a typo or the paper
has a dimensional error.** Either `[κ_R] = nat·s⁻¹` and the audit is wrong, or
the equation is wrong.

Second issue: `C_k` in the Ma–Huang PRU sense is the minimum circuit size
realising a k-design, counted in 2-qubit gates. It is an integer, "dimensionless"
only by convention — it implicitly carries a gate-time scale `τ_gate`. When one
writes `κ_R · C_k`, a hidden `τ_gate⁻¹` is absorbed into `κ_R`, which makes the
three candidate identifications of `κ_R` (scrambling rate, `2πT_R`, Haferkamp
linear rate `b_1`) **non-equivalent** — they differ by `τ_gate` factors of
order `ln(dim ℋ_R)`. The equation as written does not discriminate.

Third issue: `PH_c` is a normalisation Betti number with **no first-principles
definition** in the audit. Claiming `PH_k/PH_c` is "scale-free" (§8.3) is
circular — the scale-freeness is imposed, not derived. The chameleon exponent
`α = 0.095` is therefore a number without a unit-bearing anchor.

**Verdict: VALID.** Referee will insist on a dimensional-analysis appendix
reconciling `[κ_R]`, fixing `τ_gate`, and defining `PH_c` operationally
(e.g. Betti count at the nonlinear scale `k_NL`).

---

## Attack 2 — Reduction to known trivial cases

- **ξ_χ → 0** (chameleon decoupling, D15 limit): `Θ → 1` only if the
  argument `PH_k/PH_c → 0` as well. Chameleon decoupling affects **coupling**,
  not the argument. So ξ_χ → 0 does **not** give Θ → 1. The advertised
  reduction to Faulkner–Speranza GSL is **not automatic** and has to be shown.
- **PH_k → 0** (Gaussian homogeneous): `Θ → 1`. Then
  `dS_gen/dτ = κ_R · C_k`. This is structurally **Brown–Susskind 2nd law
  of complexity dressed as entropy rate**; in the Fan 2022 logarithmic regime
  it contradicts `Ṡ_K ≈ Ċ_K / C_K`. The equation has no log, so in the Krylov
  regime it **over-predicts** entropy growth by a factor `C_K`. This is not a
  minor quibble — it is a direct conflict with a published result in a limit
  the equation claims to subsume.
- **C_k saturation** (Brown–Susskind 2^K plateau): the equation predicts a
  *finite plateau* `dS_gen/dτ = κ_R · 2^K · Θ`, which is incompatible with the
  GSL area-bound saturation `dS_gen/dτ → 0`. A compensating saturation of
  `κ_R → 0` or `Θ → 0` must be postulated; neither is in the equation.

**Verdict: VALID** on the Krylov-regime conflict; **REBUTTABLE** on the
saturation point (audit §4 already flags a "post-scrambling pre-saturation"
regime — just needs explicit bounds).

---

## Attack 3 — Category mismatch (quantum ρ × classical δn)

`C_k` acts on `ρ_R(τ)` — a quantum reduced density matrix. `PH_k` is computed
on `δn(τ)` — a classical coarse-grained density contrast.
The equation multiplies them without specifying the **dequantisation map**
`ρ_R ↦ δn`. In Yip et al. 2024 `δn` is a late-Universe observable; in Ma–Huang
`ρ_R` lives on a Hilbert space of dimension 2^K. Coarse-graining one into the
other requires a semiclassical limit (Ehrenfest / decoherence) plus a
symplectic projector — **neither is specified**.

Worse: if `δn` is classical stochastic, `PH_k` is a **random variable**, so
`Θ(PH_k)` must be an expectation `⟨Θ⟩_{δn}` with a prior. The audit is silent
on this. A referee will demand an explicit stochastic averaging recipe.

**Verdict: VALID.** This is the cleanest attack — the cross-category
multiplication is the single most visible formal defect.

---

## Attack 4 — Arrow-of-time tautology

`τ_R` is modular time (Connes–Tomita–Takesaki). Modular flow has a
**built-in positive direction** relative to any cyclic and separating state;
Brown–Susskind-style monotone `C_k` growth along modular flow is
**automatic** in the post-scrambling regime by the 2nd law of complexity.
Hence `dS_gen/dτ_R > 0` along `τ_R` is **true by construction**, not a
derived arrow of time.

Claiming this as an "emergent arrow of time" conflates modular covariance
with thermodynamic irreversibility. Connes–Rovelli 1994 already warned
against exactly this — modular flow is a *definition* of thermal time, not
a derivation of a cosmological arrow.

**Verdict: VALID** as written, **REBUTTABLE** if the paper reframes the
claim as "the rate of modular-time entropy production is sourced by
complexity" (descriptive, not explanatory).

---

## Attack 5 — α = 0.095 is ad hoc

D15 derived `α = 0.095` for a chameleon damping between `ρ_solar` and
`ρ_cosmic` — i.e. a ratio of matter densities on a coupling potential.
`PH_k/PH_c` is a ratio of **integer topological invariants** on a density
field. The two "α" live in categorically different functionals: one is a
power on `(ρ/Λ)` in a scalar potential, the other is a power on a Betti
ratio in an activator envelope.

The audit §4.5 offers a secondary anchor: Barrow 2020 entropy index
`Δ ≲ 0.1`. But Barrow Δ is yet a **third** object (fractal dimension excess
of the horizon), unrelated to both chameleon and PH. Having three
unrelated small-number anchors ≈ 0.1 is numerology, not physics.

**Verdict: VALID.** Referee will call this fine-tuning. The fix: either
allow `α` to vary and fit it (and accept a new parameter), or give a
first-principles derivation from a single RG or CFT argument.

---

## Attack 6 — Scoop risk in disguise

arXiv searches (Apr 2026) for `"linear complexity growth" + "entropy rate"
2024–2025`, `Fan Krylov linear generalisation`, and the modular-Krylov
literature (Caputa et al. `2306.14732`; "Generalized Krylov Complexity"
`2507.23739`; "Modular Krylov Complexity as Boundary Probe" `2602.02675`;
Krylov-early-universe `2411.18405`) return **no direct linear-form
competitor**. The audit's risk rating 1.5/5 holds as of today.

However `2602.02675` (modular Krylov + area operator) and the `2507.23739`
generalised Krylov framework are **exactly the surveillance targets §6.3
predicts**. The window is short: both are ≤ 10 months old. `2604.07432`
(Holographic Krylov, charged probes) is younger still.

**Verdict: REBUTTABLE today, UNSTABLE on a 6-month horizon.** A fast arXiv
deposit is mandatory (already in audit §7).

---

## Attack 7 — Does it predict anything new?

Testable consequences:
- **CMB low-ℓ anomalies via PH_k on CMB maps.** Pranav 2024 (3.9σ loops) is
  a measurement, not a prediction of v6. v6 would have to compute a specific
  `Θ(PH_k)` shift of a CMB observable. Not done in the audit.
- **"Algorithmic Big Bang."** Philosophy, not physics — no falsifier.
- **Arrow of time.** Tautology (Attack 4).
- **DR2 posterior / PPN / D14 / D15.** These are **v5.0 predictions**;
  v6 inherits them, does not add.

The one operational testable: a **shift in the growth rate of cosmic
structure complexity** measurable as a `Θ(PH_k)`-dependent modification
of `fσ_8(z)` — this is **not stated in the audit** and would need to be
worked out. As written, v6 adds **zero new testable prediction**.

**Verdict: VALID and FATAL for publication as physics.** A pure-formalism
paper (JHEP) survives; a cosmology paper (JCAP) does not.

---

## Overall verdict

**MULTIPLE MAJOR FLAWS** — one FATAL-for-cosmology (Attack 7), three VALID
formal defects (Attacks 1, 2-Krylov, 3), one tautology (Attack 4), one
numerology (Attack 5). Scoop risk low **today** only.

## Top 3 attacks a real referee will use

1. **Attack 3 (category mismatch).** Formal, immediate, unanswerable
   without a new dequantisation recipe.
2. **Attack 2 (Fan 2022 conflict in PH_k → 0 limit).** Quantitative,
   published precursor, direct contradiction.
3. **Attack 7 (no new testable prediction).** Editorial kill-shot for any
   cosmology journal; deflects to JHEP/PRD-formal only.

## Minimum modifications to be publishable

1. Fix `[κ_R]` dimensionally; publish a dimensional-analysis appendix.
2. Define `PH_c` operationally (`k_NL`, or a specified reference shell).
3. Specify the `ρ_R → δn` dequantisation map, or reformulate both sides
   classically (coarse-grained density matrix on a coarse-grained cell).
4. Replace the equality with an **inequality** `dS_gen/dτ_R ≤ κ_R C_k Θ`
   (Wall-style GSL), removing the Fan-2022 conflict and the saturation
   mismatch simultaneously.
5. Derive `α` from one principle, or fit it and inflate the error bar.
6. Add one **genuinely new** falsifier (e.g. a `Θ(PH_k)`-modulated
   `fσ_8(z)` shift matchable against DESI DR3).
7. Drop "arrow of time" rhetoric; reframe as modular-flow entropy
   production.
8. Fast arXiv deposit for priority against `2507.23739` / `2602.02675`
   line.

With (1)–(4) and (6), the equation becomes a defensible JCAP submission.
Without (4) and (6), PRD-formal at best; JCAP unlikely; JHEP only if the
paper pivots to pure von Neumann algebra formalism and drops all
cosmological claims.
