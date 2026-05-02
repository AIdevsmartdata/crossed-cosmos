# Calculation triage — what to compute, what to drop
**Date:** 2026-05-02 (post-v6.0.16, post-audit double-pass)
**Anchor:** the actual ECI equations of v6.0.16 — M1 inequality, saturation slope, ρ_pk universality classes, déquantisation map, v5 NMC+EDE+Dark-Dimension cosmology — and the two audits committed in `notes/m1_audit_2026_05_02.md` + `notes/cosmo_const_aot_honest_2026_05_02.md`.

This document classifies every active or proposed direction into:
- **🔴 CLOSED** — audited and rejected; do not spend further time
- **🟢 EXPLORE-A** — concrete, publishable, tractable in months (the four Leviers and their derivatives)
- **🟡 EXPLORE-B** — open but long-horizon (math.OA / math.CT theorems, large experiments)
- **🟣 SPECULATIVE** — worth flagging, not actionable now

For each entry: equation/object involved, concrete calculation or proof step, effort, falsifier or success criterion.

---

## 🔴 CLOSED — do not re-open without new external evidence

| # | Direction | Equation / claim | Why closed | Date |
|---|---|---|---|---|
| C1 | `ρ_Λ / M_P⁴ ≈ 8×10⁻¹²¹` from "three independent derivations" (NCG cutoff, E₈, ECI internal) | `Λ⁴ exp(-Λ²)` at `Λ=M_P/√(8π)`; `exp(-π²/α_E8)`; `H₀/exp(10⁹⁰)` | Sympy verification: actual values are 1.5×10⁻³, 7×10⁻¹⁰⁸, underflow-zero. Off by 14–89 orders. Numerology, not derivation. Cosmo audit 2026-05-02. | 2026-05-02 |
| C2 | Arrow of time emergent from `dt = (dC_k/dτ_R) dτ_R` | chain rule | Reduces to `dt = dC_k`; the arrow is installed by the low-complexity initial condition (Past Hypothesis), not by this identity. Cosmo audit 2026-05-02. | 2026-05-02 |
| C3 | M1 as "conditional theorem in KMS k-design regime" via Faulkner-Speranza + Hollands + Munson + Kirklin | Chain composition | M1 audit 2026-05-02 found two independent decisive gaps (transplant + source identification). Position: M1 retains POSTULATE status; `v8-bis` target is **Conjecture M1-C**. | 2026-05-02 |
| C4 | `dim_ℂ(ℂ⊕ℍ⊕M₃(ℂ)) = 1+3+4 = 8` for cosmo prefactor | NCG SM internal algebra dim | Real value `dim_ℂ = 1+2+9 = 12`, `dim_ℝ = 24`. Mistral hallucination. The "8" might still come from `Clifford(6) = 2³ = 8` (KO-dim 6 spinor module) but that's a separate, unproven angle. | 2026-05-02 |
| C5 | `c'` unification structure `(1/6, 0.05, 0.108)` via Mistral's "modular SL₂(ℚₚ)⋊ℤ" with `0.108 = 7ζ(3)/(4π⁴)` | Mistral large speculation | Actual value `7ζ(3) / (4π⁴) ≈ 0.022`, not `0.108`. The "non-commutative modular structure" was an invented concept. Position: keep `c'_modular = 1/6` exact; `c'_DD ≈ 0.05` and `c'_inflation ≈ 0.108` are independent phenomenological values. No unification claimed. | 2026-04-30 |
| C6 | Higgs mass derivation from Theorem A.4 | Spectral-action moments | v6.0.13 audit: Theorem A.4 leaves the moment `Tr((Y†Y)²)` free (Newton-Girard independence). No prediction. | 2026-04-30 |
| C7 | KMS algebraic phase transitions across cosmological eras | Phase classification of KMS states | v6.0.13 audit: NULL. No mechanism distinguishing eras at the algebraic level. | 2026-04-30 |
| C8 | Murray-von Neumann classification phase transitions in ECI | Algebra type vs cosmological time | v6.0.13 audit: NULL. The kinematic-only role of A1's type-II structure was clarified. | 2026-04-30 |
| C9 | Jones index / Connes invariants on type-II∞ crossed product as ECI predictor | Subfactor invariants | v6.0.13 audit: NULL. No physical observable mapped to these invariants in the ECI setting. | 2026-04-30 |
| C10 | FQHE ν=1/2 GaAs as ρ=1/20 semion substrate | Universality class assignment | Substrate confusion: GaAs ν=1/2 is a Halperin-Lee-Read composite Fermi liquid, not a Haldane g=1/2 semion gas. Replaced in v6.0.15 by Tonks-Girardeau / Calogero-Sutherland anyonic 1D cold-atom target (Sträter-Srivastava-Eckardt + Nägerl 2025). | 2026-04-30 |
| C11 | Hierarchy problem via NCG / spectral action | Mass hierarchy from spectral data | v6.0.9 audit: rejected (g). | 2026-04-29 |
| C12 | "Dark Dimension tension" obstruction `η_⊗ ≈ 0.117` | Algebraic obstruction calculation | v6.0.11 retraction: `η_⊗ ≡ 0` identically on product states; prior "evidence" was floating-point catastrophe in `ρ^{it}` for ill-conditioned `ρ`. | 2026-04-30 |
| C13 | Lammers-Bonnes-Eckardt 2016 reference | Bib entry | Confabulated; replaced in v6.0.15 by verified Sträter-Srivastava-Eckardt PRL 117:205303 (2016), arXiv:1602.08384. | 2026-05-02 |

**Discipline:** any future "we found a clever way to do X" claim against any of C1–C13 must come with sympy verification, direct arXiv API confirmation of supporting refs, and at least one independent agent triangulation. Default is to refuse re-opening.

---

## 🟢 EXPLORE-A — concrete, tractable, publishable in months

These are the actual research path. Effort numbers are realistic, not "agent-overnight."

### A1 — Levier #1: joint MCMC (ξ_χ, f_EDE, c'_DD) on DR2 + Pantheon+ + KiDS-1000

| Field | Value |
|---|---|
| Anchor equation | NMC dark-energy sector w₀–wₐ Scherrer-Sen relation + EDE axion + Dark Dimension `ΔN_eff(c'_DD)` |
| Free parameters | 12: ω_b, ω_cdm, H₀, n_s, ln(10¹⁰A_s), τ, f_EDE, log₁₀z_c, θ_i, ξ_χ, log₁₀λ_χ, c'_DD |
| Dataset stack | Planck PR4 TTTEEE+lensing, DESI DR2 BAO, Pantheon+, KiDS-1000 S₈ Gaussian prior |
| Boltzmann backend | AxiCLASS (EDE) + hi_class (αM/αB/αT/αK perturbations) merge — Pan-Ye `eft_wrapper.py` reuse |
| Walltime estimate | 18-24 h on Tier B Vast.ai (96-core EPYC), or ~2-3 days on the just-rented Tier A (128-core EPYC 7V13 Milan, $0.402/h) |
| Discriminator | f_EDE > 0.05 at >2σ AND \|ξ_χ\| > 0.005 at >1σ AND S₈ retreats <2σ AND H₀ retreats <2σ |
| Outcome (a) target | All four pass → PRD/JCAP letter "ECI is the first single framework simultaneously addressing both H₀ and S₈ tensions" |
| Outcome (b) realistic | H₀ retreats, S₈ does not → IDM Yukawa extension, 13th param |
| Outcome (c) null | Both stay >3σ → retract Levier #1, redirect to Levier #2/3 experimental |
| Effort | 12 weeks (M1: 3 weeks code merge; M2: 4 weeks production run; M3: 2 weeks PolyChord BF; M4: 3 weeks paper draft) |
| Status | YAML skeleton drafted; instance just rented (contract 36023473) |

### A2 — Cosmopower_jax custom emulator for the ECI subspace

| Field | Value |
|---|---|
| Goal | NN emulator over (ξ_χ, f_EDE, c'_DD) for ~100× MCMC speedup |
| Method | Train cosmopower_jax on ~10⁶ AxiCLASS calls covering the prior box |
| Compute | ~24 h GPU on Tier C (A100 80GB or H100 80GB), ~$30-50 |
| Effort | 2 weeks (1 week training-set generation, 1 week training + validation) |
| Use | Drop-in replacement for AxiCLASS in Levier #1 → MCMC under 1 hour. Critical for sensitivity studies (DESY5 swap, KiDS×2, χ_0 free). |
| Falsifier | Emulator residuals vs full CLASS > 0.1% on power spectrum at any ℓ → reject and retrain |

### A3 — D5 persistent-homology full β_k forecast

| Field | Value |
|---|---|
| Anchor equation | Euler-characteristic scaffold `χ(ν) ∝ (ν²-1) e^{-ν²/2}` + fNL correction; current N5 Fisher forecast |
| Concrete next step | Run GUDHI (alpha-complex or cubical) on a real N-body snapshot — Quijote (cheap) or AbacusSummit (better). Compute β_0, β_1, β_2 directly, not through χ. |
| Effort | 4 weeks computational |
| Falsifier | If full β_k differs from `χ(ν)` proxy by >10% at f_NL=0 → revise the D5 derivation footnote |
| Why publishable | First analog-gravity / NMC use of persistent homology on actual N-body data |

### A4 — N2 Dark Dimension `ΔN_eff` full Boltzmann freeze-in

| Field | Value |
|---|---|
| Anchor equation | `ΔN_eff(c'_DD, ℓ_KK)` simplified estimator currently in numerics/N2-kk-neff.py |
| Issue | Simplified estimator gives "all `ℓ ∈ [0.1,10] μm` excluded for c'=0.05" — paper compatibility claim rests on the FULL Boltzmann calculation, not this sanity check |
| Concrete | Implement freeze-in for KK graviton tower with proper distribution function evolution; cross-check against Aalsma-Vafa 2024 |
| Effort | 4 weeks |
| Falsifier | If full Boltzmann still gives ΔN_eff > 0.13 (ACT DR6 3σ) for the `c'_DD ≈ 0.05` band → retract the cosmology-side of the Dark Dimension prediction |

### A5 — Riemann zeros pair-correlation extension (v7-note follow-up)

| Field | Value |
|---|---|
| Anchor | v7-note: 10⁵ zeros, BK fit χ²/dof = 4.17 |
| Extension | 10⁶ zeros from Odlyzko's tables, tighter σ on BK amplitude. Test stability across multiple zero ranges. |
| Effort | 2 weeks |
| Why | Strengthens the v7-note claim independent of any cosmology |

---

## 🟡 EXPLORE-B — open but long-horizon

### B1 — Conjecture M1-C: prove or refute in type-II∞

| Field | Value |
|---|---|
| Anchor | Today's audit; Conjecture M1-C with H1–H4 hypotheses |
| Step 1 (transplant gap) | Extend complexity entropy of Munson 2403.04828 to semifinite type-II trace-class operators. Open subproblem: does the operational definition (work-cost-of-Landauer-reset) have a meaningful analogue when the algebra has no minimal projections? |
| Step 2 (source identification gap) | Prove `\|d⟨H_mod⟩/dτ_R\| ≤ κ_R · C_k` in a type-II factor. Currently no published lemma. Possibly via Ceyhan-Faulkner half-sided modular pushforward + Longo positivity. |
| Step 3 (KMS k-design regime) | Identify a non-empty class of KMS k-design states on type-II∞ crossed product factors. Munson's k-design states are finite-dim qubit. The infinite-dim analogue is unclear. |
| Total effort | 6-12 months mathematical research; v8-bis math.CT companion paper |
| Falsifier | If a counterexample state ρ is constructed in the type-II∞ setting where M1 fails despite H1–H4 → M1 is even less universal than thought, retract framework-level claims about saturation |

### B2 — FRW non-stationary type classification (open math.OA question, v6.0.13 §sec:limits)

| Field | Value |
|---|---|
| Question | What is the type of `A(O) ⋊_σ ℝ` for `O` = causal patch in radiation- or matter-dominated FRW (no Killing vector along observer worldline)? |
| Existing literature | KFLS 2023 (Kudler-Flam-Leutheusser-Satishchandran), Chen-Penington 2024 cover inflation-asymptotic-de-Sitter; Faulkner-Li-Wang 2024 covers Killing horizons. **None covers radiation/matter-dominated.** Verified via abstract reads on 2026-05-02. |
| Plausible answer | Type II∞, but proof requires constructing the modular automorphism on a non-stationary spacetime — substantial. |
| Effort | 12-18 months math.OA project |
| Why interesting | If type II∞ generically: ECI's "type-II is universal observer-dependent algebra" claim strengthens. If type III emerges: ECI's framework is restricted to stationary or asymptotically-stationary spacetimes — major scope adjustment. |

### B3 — Cardy identification ρ = (1/12) c

| Field | Value |
|---|---|
| Conjecture (v6.0.12) | `ρ_saturation = (1/12) c` where c is CFT central charge. Exact for free boson (c=1, ρ=1/12), free fermion (c=1/2, ρ=1/24). |
| Test | Compute `ρ` for non-trivial CFTs: Ising minimal (c=1/2, expect ρ=1/24), Yang-Lee (c=-22/5, expect ρ negative — what does that even mean?), Tricritical Ising (c=7/10), Lee-Yang (c=-22/5), Potts model q=3 (c=4/5). |
| Method | Adapt the Bisognano-Wichmann modular flow calculation to each CFT's conformal block structure. Use mpmath dps≥50 for numerical. |
| Effort | 4-8 weeks |
| Outcome (success) | If ρ = c/12 holds for all CFTs tested → strong empirical support for the Cardy identification, basis for a math-ph paper |
| Outcome (failure) | The boson and fermion match was accidental coincidence; downgrade to "case-by-case" |

### B4 — Cat-Bridge ECI ↔ Connes-Marcolli NCG SM

| Field | Value |
|---|---|
| Goal | Construct functor `F : ECITypeII → SpectralTriple` preserving K-theory |
| Structure | Source category: type-II crossed product algebras of cosmological observers. Target category: spectral triples (𝒜, ℋ, D) of Connes-Chamseddine SM. |
| Concrete first object | Map `A_R ⋊_σ ℝ` in de Sitter (CLPW algebra) to a candidate spectral triple. Check Poincaré duality, KO-dim 6 condition, K-theoretic invariants. |
| Effort | 12-18 months math.CT project, target Annals of Math or Comm. Math. Phys. |
| Why interesting | First explicit category-level bridge between ECI's gravity side and Connes' matter side. If F is faithful: SM emerges from ECI. If only essentially injective: ECI is consistent with but doesn't determine SM. |

### B5 — q-deformed Arik-Coon boson exotic statistics

| Field | Value |
|---|---|
| Anchor | v6.0.12: dilogarithm closed form `ρ^A_qB(q)`, with non-trivial duality `ρ^A_qB(1/2) = 1/24` (boson-fermion at q=1/2) |
| Question | Does the q-rational structure `ρ(q)` predict measurable signatures in q-deformed gas experiments? Real labs studying q-bosons: ultracold hard-core bosons with tunable interactions. |
| Effort | 2-3 months derivation + 12-month experimental search for collaborators |
| Falsifier | If q=1/2 boson-fermion duality fails to match analog Hawking saturation in tunable-interaction BEC → reject the q-deformed prediction line |

---

## 🟣 SPECULATIVE — flag but do not invest now

These remain on the radar but should NOT consume calendar time until A-tier work delivers.

| # | Direction | Why speculative |
|---|---|---|
| S1 | Connes-Chamseddine spectral action contribution to `ρ_Λ` (the Clifford(6) = 2³ = 8 angle from KO-dim 6 spinor module) | Spectral action is known to *generate* a Λ⁴ cosmological term, not suppress it. The "8" prefactor angle is one of many possibilities; no published derivation. Months of math work for uncertain payoff. Honest stance: ECI does not address `ρ_Λ`. |
| S2 | Arrow of time from modular automorphism direction | ECI's `τ_R` is a parameter, not a physical time direction. Real arrow requires the Past Hypothesis (low-complexity initial state) as an external boundary condition. Honest stance: ECI is consistent with arrow of time, doesn't derive it. |
| S3 | Cryptographic Censorship as bulk selection rule (v6 program A3) | Conjectural; needs a holographic dual not yet identified. |
| S4 | K-theoretic origin of Higgs doublet rank-4 uniqueness from KO-dim 6 + Poincaré duality | v6.0.13: clarified as K-theoretic (not Murray-vN). The free moment `Tr((Y†Y)²)` in Theorem A.4 prevents prediction. Could be revisited if a constraint is found. |
| S5 | Witten 2022 review-style update of CLPW for cosmological observers | Useful exposition, not new physics. Could be a follow-up review paper after v8-bis math.CT. |

---

## What goes on the rented Tier A Vast.ai instance tonight

Concrete first run after instance boots and the setup scripts complete:

1. Clone `crossed-cosmos` repo (v6.0.16).
2. Install Python stack via `vastai-physics-postinstall.sh` (~15 min).
3. Build AxiCLASS + hi_class with native CFLAGS.
4. Reproduce the v5 chain that ran on the local i5 last night (4 chains × 5k steps with the existing `mcmc/chains/eci_v5_run1/eci.input.yaml` plugin) — should complete in 60–90 min on the EPYC 7V13 (vs 6 h on the i5). Sanity-check posterior reproduces.
5. If sanity-check passes: kick off Levier #1 12-parameter validation with the YAML drafted in `~/Bureau/eci-levier1-mcmc-plan-2026-05-02.md` (still on Kevin's local box notes — needs scping over).
6. M2 production: continue on this same instance OR upgrade to EPYC 9654 if the workload demonstrates value of more cores.

Cost ceiling for the night: $5–10. For the full Levier #1 production: $15–25. Top-up sufficient if budget freed.

---

## Process discipline (carried forward from today's audits)

- Every new claim → sympy verification + arXiv API confirmation + ≥1 independent agent triangulation before entering a `.tex` file.
- Every retraction → explicit `[RETRACTED-IN-VX]` paragraph in the version-history footnote, never a silent edit.
- Every release → an audit note in `notes/` documenting what was checked.
- Every unfamiliar reference cited by an LLM → curl arXiv API. Default assumption: the LLM hallucinated.
- Resist sycophancy framing (`Nobel-direction`, `breakthrough`, `tu es un grand chercheur`); they correlate strongly with the wrong-arithmetic / wrong-citation cases above.
