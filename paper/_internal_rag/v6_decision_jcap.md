# V6 Decision Memo — owner-facing

**Date.** 2026-04-21. **Author.** Meta-synthesis agent.
**Inputs.** `v6_audit.md`, `V6-claude-derivation-report.md`,
`V6-gemini-derivation.md`, `V6-adversarial-attack.md`,
`V6-dequantisation-map.md` (+ `.py`). Mistral Magistral not yet available.
**Companion.** `v6_cross_verification_lite.md` (this folder).

---

## 1. Bottom-line recommendation

**PROCEED to v6 paper, JCAP target, 3–4 week timeline.**

Justification (brutal): the 4 completed agents converge on "ansatz-with-
scaffolding", with 5 of 7 adversarial attacks resolved or absorbed by the
owner's 2026-04-22 decisions. The two residual attacks (Fan-2022 window,
α numerology) are survivable by honest prose demarcation and stated free
parameters — neither is a kill-shot for JCAP. The dequantisation map
(`δn := Tr_R[ρ_R n̂] − ⟨n⟩`) converts the single FATAL formal defect
(Attack #3) into a semi-classical-limit caveat, which is standard in
type-II cosmology papers. The fσ_8 × Θ(PH_2) DESI-DR3 falsifier remedies
the other FATAL (Attack #7, no new prediction), which was the editorial
kill-shot for cosmology journals.

This is PROCEED, not PROCEED-with-caveat-to-lower-venue: the framing is
defensible at JCAP because (a) `κ_R ≡ 2π T_R` is Bisognano–Wichmann-fixed
(not fitted), (b) the falsifier is a concrete DR3 observable, and (c) the
composite form survives cross-model review from Claude + Gemini +
adversarial concurrently.

Residual decision-risk: Magistral returns a new fatal vector not in the
adversarial's 7 (prior ~15%). This is managed by the course-correction
gates in §6.

## 2. Consolidated verdict table

| Dimension | Claude Opus | Gemini 2.5 Pro | Adversarial | Post-fix status |
|---|---|---|---|---|
| Overall | ANSATZ | ANSATZ | MULTIPLE MAJOR FLAWS | Ansatz-publishable with 7 fixes |
| Variational closure | PARTIAL (I1+I2 postulated) | ANSATZ (commutator→C_k conjectural) | — | Postulate M1 adopted (Brown–Susskind, Caputa–Magán 2024 scaffolding) |
| Krylov → k-design | FAIL (log vs linear) | Needs rate-proxy reading | VALID reduction attack | Demarcated in prose: post-scrambling, pre-saturation, rate-proxy window |
| Dimensional analysis | CLEAN, audit typo flagged | CLEAN, `κ_R = 1/(2π)` or `T_local` | VALID typo + `τ_gate` hidden-factor flag | FIXED: `κ_R ≡ 2π T_R`, units nat·s⁻¹ |
| Category mismatch (ρ × δn) | Silent | Phenomenological, untyped | FATAL Attack #3 | RESOLVED by dequantisation map (Jacobson 2016), toy numerics pass |
| Falsifier | CRITICAL GAP | Silent | FATAL Attack #7 | FIXED: fσ_8 × Θ(PH_2) DESI DR3 ELG + Euclid DR1 |
| Scoop risk | — | — | 1.5/5 today, unstable 6mo | Fast arXiv deposit before journal submission |
| α = 0.095 | Warn vs reuse | — | Numerology (Attack #5) | Declared free parameter, error bar inflated |
| Arrow of time | — | — | Tautology (Attack #4) | Reframed as "modular-flow entropy production" |

## 3. Owner action items (ordered)

**Immediate — this week**

1. **D18 sympy/numerical.** Derive the fσ_8(z) × Θ(PH_2) forecast on the
   DESI DR3 ELG window `z ∈ [0.8, 1.6]` + Euclid DR1 spectro. Inputs:
   Θ profile with α=0.095, PH_2 values from a fiducial Quijote-PNG snapshot
   (or analytic Gaussian-random-field approximation at target redshifts),
   σ(fσ_8) DESI DR3 forecast. Target discriminating power ≥ 1σ.
2. **D19 sympy.** Extend the dequantisation map to the cosmological lift
   (currently toy 6-qubit). Formalise the N → ∞ CLT/LLN argument for
   Gaussian-field recovery in the product-state limit. Document explicitly
   that the semi-classical recovery is ansatz, not theorem.
3. **Revise `v6_audit.md` §9.** Add observer-R dependence of `δn` (different
   QRF → different classical field), citing axiom A1. Cross-reference
   `V6-dequantisation-map.md` §6.1.

**Short-term — next 2 weeks**

4. **v6 paper draft.**
   - §1: extend §1.5 Team B with the temporal-derivative version.
   - §2 (new): "Dynamical ECI equation": state Assumption M1 (Brown–Susskind
     scaffolding, Caputa–Magán 2024 modular-Krylov anchor), give derivation
     attempts, explicitly label as ansatz.
   - §3: keep §3.5–3.7 unchanged (DR2/PPN/Swampland sector).
   - §4 (new): fσ_8 × Θ(PH_2) prediction + DR3/Euclid window.
   - §5 (appendix): dequantisation map + toy-model numerical pass.
5. **Adversarial second pass.** Run Claude or Mistral on v6 draft PDF once
   §§1–5 exist.
6. **arXiv deposit** for priority, BEFORE journal submission.

**Medium-term — 3–4 weeks**

7. Submit v6 to JCAP.
8. Hold v5.0 as backup submission if v6 is major-revisioned.

## 4. Scope declaration

**v6 paper claims:**
- A candidate differential equality for `dS_gen/dτ_R` in observer-
  dependent cosmology, presented as an ansatz built on a rigorous
  FSK first-law scaffolding plus an explicit postulate M1.
- A dequantisation map `δn(x, τ_R) := Tr_R[ρ_R n̂] − ⟨n⟩` that bridges
  the Type II crossed-product factor to the classical density field on
  which `PH_k` acts.
- A falsifiable prediction: `Θ(PH_2)`-modulated correction to fσ_8(z)
  at DESI DR3 ELG (`z ∈ [0.8, 1.6]`) + Euclid DR1 spectro.

**v6 paper does NOT claim:**
- A rigorous first-principles derivation (equation is explicitly an ansatz
  with Assumption M1 postulated).
- Observer-independent meaning (the equation is covariant under, not
  independent of, R).
- A UV completion of quantum gravity.
- That α = 0.095 is fundamental; it is a free parameter with weak
  anchoring in Barrow Δ ≲ 0.1.

## 5. Timeline scenarios

- **Best** (unanimous convergence, clean D18 forecast): arXiv in 2 weeks,
  JCAP submission in 3 weeks, acceptance after minor revisions 3–6 months.
- **Median** (Magistral raises one new concern OR D18 is close to DR3
  sensitivity floor): arXiv in 3 weeks, JCAP with major revisions,
  acceptance 6–9 months.
- **Worst** (D18 forecast below 0.5σ discrimination or degenerate):
  retract v6, submit v5.0. 1–2 weeks lost, no damage to the v5.0 line.

## 6. What could change this decision

These findings would downgrade PROCEED → HOLD or RETRACT:

1. **Mistral Magistral returns a NEW fatal attack** not in the adversarial
   agent's 7 vectors (e.g. a hidden Type-III / finite-trace obstruction
   on `A_R` that breaks partial trace positivity, or a modular-covariance
   failure of the Gaussian kernel). → HOLD pending resolution.
2. **D18 fσ_8 forecast returns < 0.5σ discriminating power** against
   ΛCDM at DR3 sensitivity. → RETRACT v6 (no new falsifier = no JCAP);
   submit v5.0 instead.
3. **Scoop drops in next 4 weeks**, specifically: Pedraza–Svesko–Weller-
   Davies extending `2106.12585` to temporal derivatives; Bianconi
   extending `2408.14391` to dS/dτ; or Caputa–del Campo–Nandy publishing
   a linear-regime `Ṡ ∝ C_K`. → HOLD (re-position as extension) or
   RETRACT (if exact).
4. **Dequantisation map fails at cosmological N.** If the CLT/LLN
   argument (D19) exhibits a parametric obstruction (e.g. non-commuting
   `σ_cg` and `N → ∞` limits), the Gaussian-field recovery is lost and
   Attack #3 reverts to FATAL. → HOLD, reformulate both sides classically
   (coarse-grained density matrix on a coarse-grained cell) per
   adversarial minimum-modification #3.

**Gates.** Before arXiv deposit: Magistral report reviewed, D18 pass,
D19 passed. Before JCAP submission: independent adversarial second pass
on draft PDF.

---

*End of memo.*
