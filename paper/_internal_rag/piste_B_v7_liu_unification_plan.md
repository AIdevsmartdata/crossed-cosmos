# Piste B — v7 Paper: v6 + Chandrasekaran-Flanagan 2026 Unification Investigation Plan

**File:** `paper/_internal_rag/piste_B_v7_liu_unification_plan.md`
**Date:** 2026-04-22
**Rules enforced:** V6-1, V6-4, PRINCIPLES rule 1, rule 12
**Based on:** WebFetch of arXiv:2601.07915 (2026-04-22), v6.0.4 HEAD, FAILED.md, GROUND_TRUTH.md Part G, v6_gap_analysis.md

---

## CRITICAL FIRST FINDING — Author Correction

The paper cited in the task as "Liu 2026 (arXiv:2601.07915)" is **NOT by Liu et al.**

WebFetch of arXiv:2601.07915 (2026-04-22, confirmed from abstract page) identifies the authors as:
> **Venkatesa Chandrasekaran and Éanna É. Flanagan**
> "Subregion algebras in classical and quantum gravity" (January 12, 2026)

This paper is hereafter cited as **CF26** (Chandrasekaran-Flanagan 2026). The bib key `Liu2026Subregion` already used in v6.0.4 §3 proof sketch is **incorrect** and must be corrected to `ChandrasekFlanagan2026` before any arXiv submission. This is a rule 1 (honesty gate) violation in the current draft.

All analysis below uses the correct attribution CF26 = Chandrasekaran-Flanagan 2026.

---

## Task 1 — Precise Statement of CF26 (arXiv:2601.07915)

**Source:** WebFetch of abstract page (full PDF text was binary-opaque; this section is based on confirmed abstract text only, per PRINCIPLES rule 1 — no training-data extrapolation).

**Authors:** Venkatesa Chandrasekaran, Éanna É. Flanagan.

**Paper length:** 111 pages + appendices A–G.

**What CF26 proves (from abstract, verbatim paraphrase):**

1. **Algebra construction.** For each cut of a null-surface horizon (black hole background), CF26 constructs a **type-II∞ von Neumann algebra** whose von Neumann entropy equals the **generalised entropy** of that cut. This is a gravitational analogue of the CLPW construction but for null-surface cuts rather than the full crossed-product observer algebra.

2. **GSL for non-stationary perturbations.** CF26 proves a **generalised second law** for non-stationary linearised perturbations of Killing horizons. The GSL is dS_gen ≥ 0 across the horizon cut family (increasing under the null-translation family, i.e. dS_gen/dλ ≥ 0 where λ is the null affine parameter).

3. **Quantum Focusing Conjecture.** CF26 uses "gravitational half-sided modular inclusion algebras" to **prove the QFC in the perturbative quantum gravity regime**. QFC statement: dΘ/dλ ≤ 0 where Θ = dA/dλ is the expansion of the null congruence, or equivalently in the generalised entropy form: d²S_gen/dλ² ≤ 0 (focusing). **The QFC is an upper bound on the second derivative of generalised entropy**, not an upper bound on the first derivative.

4. **Key mechanism:** gravitational half-sided modular inclusion of the horizon-cut algebras. The nesting of algebras A(λ₁) ⊆ A(λ₂) for λ₁ < λ₂ (cuts further along the null surface) forms a Borchers half-sided modular inclusion, and CF26 uses this structure together with relative-entropy monotonicity to prove both the GSL and the QFC.

**Hypothesis class:** perturbative quantum gravity around a Killing-horizon background (linearised). The half-sided modular inclusion requires the algebras to be type-II∞ (guaranteed by the gravitational edge-mode phase space construction). No explicit Pinsker step is visible from abstract; the proof likely uses monotonicity of relative entropy under the inclusion map directly (Connes–Narnhofer–Thirring type argument), but this cannot be confirmed without the rendered §§3-4 text.

**Theorem/section references:** Full theorem numbering in §§3-4 could not be extracted (PDF was binary-encoded). Reference to the QFC proof is in the abstract only; the v6_gap_analysis.md §B3 note (written 2026-04-22 after an earlier web survey) describes CF26 as proving "QFC via half-sided modular inclusion" in §§ consistent with the abstract. This is the extent of what can be confirmed at rule-1 standard.

**HONEST FLAG:** The precise theorem numbers, hypothesis labelling (H1/H2/H3 or similar), and whether CF26 uses a Pinsker step or a direct Araki relative-entropy inequality cannot be stated without the rendered HTML or a readable PDF. Task 1 is partially open until CF26 full text is accessed.

---

## Task 2 — Comparison of CF26 to v6.0.4

### Exact overlaps

| Feature | v6.0.4 | CF26 |
|---|---|---|
| Algebra type | Type-II∞ crossed-product (CLPW/DEHK observer algebra A_R) | Type-II∞ horizon-cut subalgebra (null-surface cut algebras A(λ)) |
| Half-sided modular inclusion | Used implicitly via Ceyhan-Faulkner 2020 Thm 1.2 for the Pinsker step | Used explicitly as the central algebraic mechanism (proven theorem) |
| GSL direction | Upper bound on dS_gen/dτ_R (modular time) | Lower bound dS_gen/dλ ≥ 0 (null affine parameter) |
| Relative entropy monotonicity | Pinsker-style step: −dS_rel/dτ_R ≤ |d⟨K_R⟩/dτ_R| (cited CF 2020) | Direct monotonicity under inclusion map (basis of QFC proof) |
| Source term | κ_R C_k Θ (complexity + topological activator, under M1-M3) | None — proves focusing without a complexity source |
| Proof status | Inequality under three postulates (M1 POSTULATE, M2 ANSATZ, M3 CONJECTURAL) | Theorem (in perturbative QG) |

### Exact divergences

1. **v6 adds the complexity source κ_R C_k Θ; CF26 does not.** CF26 proves QFC as dΘ/dλ ≤ 0 without any complexity bound on the RHS. v6 proves dS_gen/dτ_R ≤ κ_R C_k Θ. These are different inequalities on different parameters.

2. **v6 is modular-time differential (∂/∂τ_R); CF26 is null-affine differential (∂/∂λ).** These are different derivation parameters. A dictionary between τ_R and λ is not automatic and is the central technical gap for any unification (see Task 4c).

3. **v6 operates on the full CLPW crossed-product algebra A_R; CF26 operates on horizon-cut subalgebras A(λ).** The A(λ) of CF26 are subalgebras of an ambient type-III₁ algebra on the full Cauchy slice; the CLPW A_R is constructed by crossing with the observer's reference frame. Whether A(λ) ⊂ A_R or A_R ⊂ A(λ) or neither is not established.

4. **v6 proves an upper bound on entropy growth; CF26 proves a lower bound (GSL) and an upper bound on focusing (QFC).** The QFC (d²S_gen/dλ² ≤ 0) and the v6 bound (dS_gen/dτ_R ≤ κ_R C_k Θ) are on different observables (second derivative vs first derivative, different parameters). They are not directly comparable without the τ_R ↔ λ dictionary.

5. **Proof robustness:** CF26 is a 111-page theorem with full proofs; v6 is a 7-page inequality under three labelled postulates, two of which are ANSATZ or CONJECTURAL status.

---

## Task 3 — Unification Statement

### Candidate v7 theorem (template, per task brief)

> **Candidate Theorem (v7 template, NOT YET PROVED).**
> Let A_R be the type-II∞ crossed-product algebra of CLPW/DEHK with modular flow σ^R_{τ_R}, and let {A(λ)} be the one-parameter family of horizon-cut subalgebras of CF26 (Chandrasekaran-Flanagan 2026, arXiv:2601.07915), each of type-II∞ and equipped with their natural trace. Suppose there exists a monotone embedding j_λ : A(λ) → A_R compatible with the modular flow in the sense that j_λ ∘ σ^{A(λ)}_{τ_R} = σ^R_{τ_R} ∘ j_λ, and a dictionary τ_R = f(λ) between the null affine parameter and the modular time parameter. Then:
>
> (i) (Complexity-bounded QFC) dS_gen[R]/dτ_R ≤ κ_R C_k[ρ_R(τ_R)] Θ(PH_k[δn(τ_R)]), and
>
> (ii) (Refined focusing) d²S_gen/dλ² ≤ κ_R C_k (df/dλ)² Θ,
>
> under assumptions M1-M3 of v6 plus the CF26 perturbative QG regime and the embedding hypothesis.

### Honest assessment of this candidate

**This is not a unification theorem — it is a co-conditional statement.** Both conclusions (i) and (ii) require independent hypotheses:
- (i) requires M1 (POSTULATE), M2 (ANSATZ), M3 (CONJECTURAL).
- (ii) requires (i) plus the τ_R ↔ λ dictionary (not established) plus the embedding j_λ (not established).
- CF26's QFC proof (d²S_gen/dλ² ≤ 0) does not logically imply or require C_k Θ.
- v6's complexity bound (dS_gen/dτ_R ≤ κ_R C_k Θ) does not logically imply or require the CF26 QFC.

The "unification" is a conjunction of two results in a common framework, not a structural theorem that neither alone provides. Rule 12 applies: do not claim this is a unification without proving the embedding j_λ and the dictionary τ_R = f(λ) first.

### What WOULD make this a genuine theorem

A structural v7 theorem requires:
1. The embedding j_λ : A(λ) → A_R is a half-sided modular inclusion in the Borchers sense.
2. The null affine parameter λ is proportional to modular time: τ_R = c · λ for some c depending on the surface gravity (Bisognano-Wichmann type relation).
3. The complexity source κ_R C_k in v6 is compatible with — meaning it upper-bounds — the CF26 QFC focusing condition, so that the complexity bound does not contradict focusing.

If 1-3 hold, the v7 statement becomes: "under the CF26 perturbative QG regime, the complexity-bounded GSL of v6 implies a complexity-bounded QFC." This is a non-trivial refinement because CF26 has dΘ/dλ ≤ 0 as a theorem (no RHS source), while v7 would have dΘ/dλ ≤ κ_R C_k Θ (f'(λ))² as a complexity-sourced refinement.

**This is the minimum viable v7 theorem** (see Task 6).

---

## Task 4 — The Proof Gap

Three candidate bridge steps, assessed honestly:

### 4a — Identify CF26 QFC hypothesis with special case of M1

**Assessment: viable but circular.** M1 is the Brown-Susskind-style ansatz that internal entropy production is bounded by κ_R C_k. CF26 proves QFC without any complexity source; it uses monotonicity of relative entropy under half-sided modular inclusion. One could identify CF26's hypothesis (perturbative QG, linearised around Killing horizon) as a regime where M1 holds with a specific C_k value determined by the background geometry. However:
- This would make M1 a theorem in the perturbative QG regime of CF26, which would be progress.
- The route requires showing that the modular Hamiltonian generator K_R, restricted to the CF26 background, has operator growth controlled by C_k at the rate κ_R. This is a non-trivial operator-algebraic claim not established in either paper.
- Risk: this is the same gap as v6 A1 (A1 = M1 as type-II theorem), which v6_gap_analysis identifies as the highest-priority open problem. CF26 does not close it.

### 4b — Logistic envelope compatible with QFC focusing

**Assessment: technically feasible, but not a unification.** The v6 logistic envelope dS_gen/dτ_R ≤ κ_R C_k (1 − C_k/C_k^max) Θ has the property that it goes to zero at C_k = C_k^max (scrambling saturation). The CF26 QFC is dΘ/dλ ≤ 0 (focusing). For compatibility:
- dS_gen/dτ_R → 0 as C_k → C_k^max implies entropy growth stops, which is consistent with (but does not imply) focusing.
- Focusing is a local geometric condition (null expansion decreasing); the v6 logistic bound is a global entropy-rate condition.
- Demonstrating compatibility requires the τ_R ↔ λ dictionary (step 4c). Without it, compatibility is a qualitative statement, not a theorem.

### 4c — Modular time τ_R to affine parameter λ dictionary

**Assessment: the hardest and most critical gap.** The Bisognano-Wichmann theorem gives τ_R = 2πλ/κ (surface gravity κ) for a Killing horizon Rindler observer. In the static dS patch, this identifies the CLPW modular time with the null affine parameter on the horizon. However:
- For non-stationary perturbations (the CF26 regime), the Killing vector is deformed and τ_R = f(λ) is no longer the simple linear relation.
- The CF26 algebra A(λ) is indexed by null cuts λ; the CLPW algebra A_R is indexed by a quantum reference frame R. The identification requires the QRF observer R to sit at a specific null cut, which restricts the setup.
- In compact-support terms: the v6 setup requires the GKS modular isotopy to have compact support (valid on the dS static patch horizon); the CF26 null surface has a non-compact null generator family. This is precisely the A4 gap already documented in v6_gap_analysis.md.

**Conclusion on Task 4:** The critical bridge is 4c (τ_R ↔ λ dictionary). Steps 4a and 4b both depend on it. This is the first technical item that must be resolved before any v7 theorem can be stated with content.

---

## Task 5 — Pre-Registered Paper Structure

**Proposed v7 structure (8-10 pages JHEP, hep-th, conditional on Task 4c progress):**

### §1 Introduction (1 page)
- Context: v6 complexity-bounded GSL + CF26 QFC proof both use type-II∞ algebras and half-sided modular inclusion.
- Gap: no paper combines them; the τ_R ↔ λ dictionary is the missing link.
- This paper's claim: IF the dictionary holds, THEN dΘ/dλ ≤ κ_R C_k Θ (f'(λ))² is the complexity-refined QFC. Stated as Theorem 1 (conditional).
- Honest scope: conditional theorem, not an unconditional result.

### §2 Setup (2 pages)
- CLPW/DEHK crossed-product algebra A_R and modular flow σ^R_{τ_R}.
- CF26 horizon-cut algebras A(λ) (type-II∞, null surface).
- State the embedding hypothesis: j_λ : A(λ) → A_R with modular compatibility.
- Bisognano-Wichmann dictionary for the Killing-horizon background case.
- Flag where it extends (perturbative QG) and where it fails (non-stationary).

### §3 Main Theorem (1.5 pages)
- Theorem 1 (conditional complexity-bounded QFC): under M1-M3 + CF26 regime + embedding hypothesis, d²S_gen/dλ² ≤ κ_R C_k Θ (f'(λ))².
- Corollary 1: in the M1-postulate regime without the embedding, v6 and CF26 are compatible (dS_gen/dτ_R ≤ κ_R C_k Θ and d²S_gen/dλ² ≤ 0 are jointly satisfiable).
- Corollary 1 is the minimum viable result: it shows the two results are not contradictory without requiring a full unification proof.

### §4 Proof Strategy (2 pages)
- §4.1 Half-sided modular inclusion for the embedding (what needs to be proved for j_λ).
- §4.2 Dictionary τ_R = f(λ): Bisognano-Wichmann as baseline; corrections from CF26 linearised gravity.
- §4.3 Complexity source under inclusion: operator growth in A(λ) ⊂ A_R and why C_k on A_R upper-bounds C_k on A(λ).
- §4.4 Logistic envelope and QFC: saturation C_k → C_k^max implies dS_gen/dτ_R → 0, consistent with late-time focusing.

### §5 Relation to v6 and CF26 (1 page)
- v6 limit: remove the A(λ) structure (set λ = const), recover v6 main bound.
- CF26 limit: remove complexity source (C_k → ∞, M1 saturated), recover CF26 GSL/QFC.
- No claim that v7 subsumes either paper: v7 adds the conditional bridge, not the theorems themselves.

### §6 Open Questions (0.5 page)
- M1 as a type-II theorem (inherited from v6).
- τ_R ↔ λ beyond perturbative QG.
- Extension to FLRW (inherited from v6 A4 gap).
- Operational measurement of C_k along modular flow.

### Appendix A Computational Realisation (0.5-1 page)
- Toy bipartite type-II₁ factor (inherited from v6 derivations).
- Numerical check: in the CLPW nested inclusion A_R ⊆ A_R', does C_k[ρ_R'] ≤ C_k[ρ_R] · C_k[ρ_{R'∖R}]? (Already verified in v6 Lemma.)
- Add: is there a null-affine labelling consistent with the modular time? (New computation needed.)

---

## Task 6 — Feasibility Assessment

### Timeline

**Minimum viable v7 (solo, 6-9 months):**
- Confirm τ_R = f(λ) at the Bisognano-Wichmann level (well-established for static Killing horizons; 1-2 months of reading + 1 page of prose).
- State Corollary 1 (compatibility, not unification) as the main result.
- Correct the bib key Liu2026Subregion → ChandrasekFlanagan2026 (immediate).
- Add CF26 citation to v6 §3 properly (already partially done; fix is minimal).
- This yields a 4-6 page letter, not a 10-page paper.

**Full v7 (12-18 months, requires expert input):**
- Prove the embedding j_λ : A(λ) → A_R as a half-sided modular inclusion for the perturbative QG regime of CF26. This requires mastering the CF26 111-page construction (1-3 months) plus proving a new algebraic lemma (3-6 months with expert collaboration).
- Resolve τ_R ↔ λ for non-stationary perturbations (3-6 months, likely requires Flanagan or Kirklin collaboration).
- Upgrade M1 to a theorem in the CF26 regime (likely 6-12 months if possible at all; it is the highest-priority open problem in v6_gap_analysis A1).

**External help:**
- **Chandrasekaran or Flanagan (CF26 authors):** most natural collaborators. They have the null-surface algebra machinery; v6 adds the complexity source. A joint paper would be the natural outcome if they find the complexity refinement interesting.
- **Kirklin (Cambridge, already cited in v6):** has expertise in non-semiclassical GSL and QRF-based horizon cuts. Likely interested in the τ_R ↔ λ dictionary for non-stationary perturbations.
- Emailing either author with a preprint of v6 + a one-page Piste B summary is the first practical step.

### Minimum viable v7 theorem (solo work, 6 months)

> **MVT (Minimum Viable Theorem, Piste B).**
> For a Killing-horizon observer in the CLPW/DEHK setup with modular time τ_R = 2πλ/κ (Bisognano-Wichmann), the v6 inequality dS_gen/dτ_R ≤ κ_R C_k Θ and the CF26 QFC d²S_gen/dλ² ≤ 0 are jointly satisfiable (not contradictory). Specifically, any trajectory satisfying the logistic envelope (Prop. 1 of v6) automatically has d(dS_gen/dλ)/dλ ≤ 0 in the scrambling-saturation limit C_k → C_k^max, consistent with QFC focusing.

This is modest: it is a **compatibility lemma**, not a combined theorem. It has genuine content (shows the two results are not in tension in the Killing-horizon regime) and could be published as a companion note to v6 or as a brief §5 remark added to v6.0.5 before JHEP submission.

---

## Task 7 — Risk Assessment

### Risk R1: Trivial reduction to CF26

**Likelihood: HIGH if the τ_R ↔ λ dictionary is just Bisognano-Wichmann.**
If τ_R = 2πλ/κ is exact (static Killing horizon), then the "v7 theorem" reduces to: "substitute v6 with τ_R replaced by 2πλ/κ." This is a notation change, not a new theorem. The new content would require either (a) the non-stationary correction to the dictionary, or (b) a non-trivial algebraic statement about A(λ) ⊆ A_R. Without these, v7 is an empty paper.

**Mitigation:** focus on the non-stationary regime (CF26's actual contribution) and explicitly show where Bisognano-Wichmann breaks down, making the problem non-trivial.

### Risk R2: Trivial reduction to v6

**Likelihood: MEDIUM.** If the CF26 horizon-cut algebra A(λ) is simply a sub-algebra of the CLPW A_R with no additional structure, then v7 adds nothing to v6: the submultiplicativity Lemma already handles nested algebras A_R ⊆ A_{R'}. The CF26 structure must provide genuinely new algebraic input (the null-cut family with non-trivial focusing condition) for v7 to have content.

**Mitigation:** verify that the CF26 QFC proof (d²S_gen/dλ² ≤ 0) cannot be reproduced from v6's Lemma alone. If it can, then Piste B fails and should be recorded in FAILED.md.

### Risk R3: Incompatible frameworks (F-N entry risk)

**Likelihood: MEDIUM.** The v6 algebra is a crossed-product (observer-dependent, requires a clock QRF); the CF26 algebra is a null-surface cut algebra (geometric, no observer clock needed). The two frameworks solve different problems:
- CLPW/DEHK crossed-product: resolves the type-III problem for a QRF observer in dS.
- CF26 null-cut algebras: resolves the type-III problem for null-surface cuts via gravitational edge modes.
These are parallel constructions for different observables. The embedding j_λ may not exist as a morphism in the category of type-II algebras with trace (it would need to preserve the specific Connes cocycle structure of each).

**If R3 materialises:** Piste B must be recorded in FAILED.md as F-20 with verdict "incompatible frameworks — CLPW crossed-product and CF26 null-cut algebra do not embed into a common type-II category without new construction." The compatibility claim (MVT above) would still stand as a weaker result.

### Risk R4: Genuine new content — optimistic scenario

**Likelihood: LOW but non-zero.** If (a) j_λ exists and is provably a half-sided modular inclusion, AND (b) τ_R = f(λ) can be computed in the perturbative QG correction to Bisognano-Wichmann from CF26, then v7 provides:
- A complexity-bounded refinement of the QFC (dΘ/dλ ≤ κ_R C_k Θ (f')²).
- A new structural connection between the CLPW observer algebra and CF26 null-cut algebras.
- A modular-time anchor for the null affine parameter in the CF26 construction.

This would be a JHEP-worthy 10-page paper. The probability of this outcome is estimated at <20% based on the current assessment of the τ_R ↔ λ gap.

### On FAILED.md F-6 (terminological conflation warning)

F-6 warns against conflating similar-sounding concepts (PH ↔ HP). The analogous risk here is:
- Conflating "half-sided modular inclusion in CF26" (used to prove QFC) with "half-sided modular inclusion in Ceyhan-Faulkner" (used in v6 Pinsker step). These are the same mathematical structure (Borchers half-sided inclusion) applied in different contexts. This is a **legitimate shared tool**, not a conflation — but the v7 write-up must be precise about which inclusion is invoked in which step.
- Conflating "complexity-bounded GSL" (v6: dS_gen/dτ_R ≤ κ_R C_k Θ) with "complexity-bounded QFC" (v7 candidate: d²S_gen/dλ² ≤ κ_R C_k Θ (f')²). These are genuinely different statements. The v7 paper must state which one it proves and not present the other as a corollary without proof.

---

## Action Plan — First Month

### Immediate (week 1)

1. **Fix bib key:** replace `Liu2026Subregion` with `ChandrasekFlanagan2026` in v6_jhep.tex and v6.bib. Update all prose references. This is a rule 1 fix (honesty gate), required before v6 arXiv submission regardless of Piste B.

2. **Access CF26 full text:** the HTML version at arxiv.org/html/2601.07915 returned 404; try the direct PDF at a readable viewer (e.g. semantic scholar, or request via collaborator access) to extract §§3-4 theorem statements. This is prerequisite for Tasks 1, 4a, 4c.

### Month 1 priorities

3. **Verify Bisognano-Wichmann dictionary:** establish whether τ_R = 2πλ/κ holds exactly in the CLPW setup for the dS static patch. This is documented in the literature (Connes cocycle for KMS states at Hawking temperature); confirm it with a literature trace through Haag-Hugenholtz-Winnink and CLPW §§4-5.

4. **Check embedding existence:** in the static dS case, does A(λ) (CF26 null-cut) embed into A_R (CLPW) as a von Neumann subalgebra? Answer requires knowing both constructions in detail. Kirklin (Cambridge) is the right person to ask; he knows DEHK and has studied Killing-horizon cuts.

5. **State the MVT (§6 minimum viable theorem)** as a remark in v6.0.5 and test it: in the scrambling-saturation limit C_k → C_k^max, does Prop. 1 (logistic envelope) imply dS_gen/dτ_R → 0, and does the Bisognano-Wichmann dictionary convert this to d(dS_gen/dλ)/dλ ≤ 0? This computation is within scope for a solo afternoon's work.

---

## Recommended First Action

**Recommended first-month action (priority order):**
1. Fix the Liu/CF26 bib error in v6 immediately (1 hour).
2. Access CF26 §§3-4 rendered text via an alternative reader and extract exact theorem statements (1-2 days).
3. Compute the MVT compatibility check in the static dS Bisognano-Wichmann regime (1 day of algebra + 1 day of sympy verification).
4. Contact Kirklin with a preprint of v6 + a one-page Piste B summary to assess his interest in the τ_R ↔ λ non-stationary extension.

---

## Three Most Critical Unknowns

**U1 — Is the τ_R ↔ λ dictionary beyond Bisognano-Wichmann accessible in the CF26 perturbative QG regime?**
If yes: the core technical gap for the full v7 theorem is closable (12-18 months, likely with CF/Kirklin collaboration). If no (i.e., the non-stationary correction breaks the simple proportionality): v7 reduces to the MVT compatibility remark, not a new theorem.

**U2 — Does the CF26 null-cut algebra A(λ) embed into the CLPW crossed-product algebra A_R?**
This is the embedding hypothesis j_λ : A(λ) → A_R. It determines whether "unification" is algebraically possible. It could fail if the two constructions use incompatible Connes cocycles (CF26 uses gravitational edge modes; CLPW uses a clock QRF). Answering this requires reading CF26 §§2-3 and CLPW §§3-4 in parallel.

**U3 — Does CF26 use a Pinsker step, and if so, is it the same as the Ceyhan-Faulkner step in v6?**
If CF26's QFC proof uses the same Pinsker-style inequality as v6, the two proofs share a common layer and v7 can cite both papers as using the same mechanism. If CF26 uses a different technique (direct relative entropy decrease, or Connes-Narnhofer-Thirring type), then the proof strategies diverge and the "shared mechanism" claim must be weakened. This requires rendered §§3-4 text of CF26.

---

## Summary Verdict (Piste B, as of 2026-04-22)

**Piste B is not a unification — it is a programme.** The two papers (v6 and CF26) share the half-sided modular inclusion machinery as a common tool, but they prove different things in different parameter spaces (modular time vs null affine; upper bound on rate vs focusing condition). A genuine combined theorem requires the τ_R ↔ λ dictionary and the embedding j_λ, neither of which is currently available.

The minimum viable output (MVT: compatibility remark in the Killing-horizon regime) is achievable in solo work within 4-6 weeks and should be added to v6.0.5 as a remark or §5 observation before JHEP submission.

The full v7 paper (8-10 pages JHEP) is a 12-18 month programme conditional on (U1), (U2), (U3) being positively resolved. It is not a guaranteed project; R1 (trivial reduction) and R3 (incompatible frameworks) are real risks. Piste B should not be opened as a v7 draft until U2 is resolved.

**Immediate deliverable:** fix the Liu → Chandrasekaran-Flanagan bib attribution in v6 (mandatory, independent of Piste B outcome).

---

*File: paper/_internal_rag/piste_B_v7_liu_unification_plan.md | Lines: ~400 | Do not commit without bib-DOI verification of CF26 entry.*
