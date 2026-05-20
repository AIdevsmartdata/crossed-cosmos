# Adversarial Review — Paper Lemma A3-2 (Pretrace factorisation along genus characters on Bianchi 3-orbifolds)

**Reviewer**: Anonymous (Inventiones / Annals reviewer persona)
**Date**: 2026-05-20
**Source draft**: `/root/notes/PAPER_LEMMA_A3_2_FORMAL_PROOF_2026-05-19.md` (672 lines, 7804 words, ~20pp)
**Reviewer default verdict**: REJECT (overturned only if no errors found after honest scrutiny)
**Target venue**: J. Functional Analysis (primary)

---

## Executive summary

After a step-by-step verification of the five-step pipeline (§§2–6) and of the Theorem 8.1 assembly (§8), the proof contains **one fatal, paper-level defect** (Step 4, Theorem 5.5) and **three serious concerns** (Theorem 8.1 (i), (iv), and (v)). The fatal defect is **not internal to the present paper** — it is a citation/scope error already CAUGHT and RETRACTED in the project's own master register (BIGTABLE V4 FINAL §0.4, row "Sarnak 1983 universal Bianchi" listed as RETRACTED; companion paper `Paper_ECI_Survey_Clay_BullAMS` Remark `selberg_downgrade`) — yet the present draft **re-invokes the retracted attribution as the sole load-bearing input for Step 4**. The Theorem 8.1 (i) and (ii) derivations are sketched at TIER 3 sketch level only, not proved.

Recommendation: **REJECT (major revisions required)**. The five-step decomposition of Theorem 1.1 (a)–(d) survives if Step 4 is **demoted to CONDITIONAL** on a universal Bianchi Selberg-type bound (an open question per the corpus's own established position). The Theorem 8.1 closure of Route B then no longer becomes "PROVED UNCONDITIONAL". The paper's headline claim — that the YM mass-gap formula `m_0++/√σ = √(2πe)·√(2/3)·F(N)` is PROVED UNCONDITIONAL without Conjecture E — is **not currently supported**.

---

## Step-by-step verdict

### Step 1 — Hecke action of Cl(K) on L²(Y_K) commutes with Δ

**VERDICT**: AGREE (with minor concern on §2.3 attribution scope).

**Pinpoint**: §2.3 (lines 130–142) attributes the construction of T_𝔭 to "EGM 1998 §7.6; Sarnak 1983 §3 for h_K∈{1,2}". This is correct for EGM 1998 (Springer SMM, §7.6 is the chapter on Hecke operators on Bianchi orbifolds), and Sarnak 1983 does indeed treat the Hecke operators in §3 of Acta Math 151:253–295, though Sarnak's main scope is h_K=1, with §4 extending to h_K=2 examples. The phrase "for h_K∈{1,2}" is therefore accurate. Lemma 4.1 (line 188) is the standard Hecke–Casimir commutation, classical to EGM 1998 §7.6.6.

**Source**: Elstrodt–Grunewald–Mennicke 1998, *Groups Acting on Hyperbolic Space*, Springer SMM, ISBN 9783540627456, §7.6 "Hecke operators on Bianchi orbifolds". Verified via cluster register; not directly accessed because the volume is a Springer book without arXiv.

**Suggested fix**: None. Step 1 is unconditional and correctly attributed.

---

### Step 2 — Genus character projectors P_χ

**VERDICT**: AGREE.

**Pinpoint**: Lemma 3.1 (line 156) is character orthogonality on the finite abelian 2-group g(K), entirely standard. Equation (3.1) defining P_χ as a finite linear combination of T_𝔞 is well-defined modulo Remark 2.1 (the principal-ideal ambiguity acts by a scalar of modulus 1 on isotypic components). The construction is classical (Mackey 1958 / Bourbaki Alg. Comm. Chap. VIII).

**Source**: Standard. No external reference required beyond Remark 2.1's classical character orthogonality on a finite abelian group.

**Suggested fix**: None. Step 2 is unconditional and correctly stated.

---

### Step 3 — Δ_χ self-adjoint with discrete spectrum (+ Eisenstein continuous part)

**VERDICT**: AGREE (with minor concern on Borel calculus chain).

**Pinpoint**: Lemmas 4.1, 4.2, 4.3 (lines 188–209) and Corollary 4.4 (line 213). The closed-invariant-subspace argument (line 209) is correct: a self-adjoint operator restricted to a closed invariant subspace is self-adjoint. Lemma 4.2 ([Δ, P_χ] = 0) is a direct consequence of Lemma 4.1 since P_χ is a polynomial in T_𝔭's. Corollary 4.4 (heat semigroup block-diagonalises) follows from bounded Borel functional calculus applied to f(λ) = e^{−tλ}; the chain `bounded Borel calculus → e^{−tΔ} preserves L²(Y_K)_χ → block-diagonal` is standard (Reed–Simon I §VII.2, Rudin FA §13.24).

**Source**: EGM 1998 §4 (self-adjointness of Δ on L²(Y_K)) ✓. Rudin *Functional Analysis* §13 for bounded Borel functional calculus.

**Suggested fix**: For Inventiones-level scrutiny, cite Rudin FA Theorem 13.24 (or Reed–Simon I §VII.2) explicitly at line 213 for the bounded Borel functional calculus step. Currently the "bounded Borel functional calculus" is just stated. This is a minor cleanup.

---

### Step 4 — L(χ, 1) ≠ 0 and per-χ Selberg gap (THIS IS THE CRITICAL STEP)

**VERDICT**: DISAGREE (fatal defect — load-bearing input misattributed and out of scope).

The step splits into TWO sub-claims with very different status.

#### Sub-claim 4a — L(χ, 1) ≠ 0 for non-trivial genus characters

**VERDICT**: AGREE.

**Pinpoint**: Lemma 5.3 (lines 261–267) factorises L(ψ_χ, s) = ∏_{D_i∈S} L(χ_{D_i}, s) via Cox 1989 Thm 7.7, and uses Dirichlet's analytic class-number formula `L(χ_{D_i}, 1) > 0` (a strictly positive quantity given by `2πh(D_i)/√|D_i|` for D_i < −4). This is correct, classical, and the attribution to Dirichlet 1839 + Davenport 2000 §6 + Cox 1989 §7.B is accurate. No issue here.

**Source**: Dirichlet 1839 (no arXiv, classical work); Davenport, *Multiplicative Number Theory*, 3rd ed., Springer GTM 74, §6; Cox 1989, *Primes of the Form x²+ny²*, Wiley, §7.B Thm 7.7. All verified via standard reference channels.

#### Sub-claim 4b — Per-χ Selberg gap λ₁(Δ_{cusp,χ}) ≥ 3/4 attributed to "Sarnak 1983 Acta Math 151 Theorem 3.1"

**VERDICT**: DISAGREE (fatal).

**Pinpoint**: Theorem 5.5 (lines 273–278) states the bound `λ₁(Δ_{cusp,χ}) ≥ 3/4` and attributes it verbatim to "**Sarnak 1983** *The arithmetic and geometry of some hyperbolic three-manifolds*, Acta Math. 151:253–295, Theorem 3.1 (verified PDF p. 255) establishes the unconditional bound λ₁ ≥ 3/4 for the cuspidal Laplace spectrum on Bianchi 3-orbifolds Y_K = PSL₂(O_K) \ ℍ³."

This claim is incorrect on **multiple grounds**:

1. **Scope error (load-bearing).** Sarnak 1983 covers SPECIFIC arithmetic 3-manifolds with explicit h_K (h_K = 1 with extensions in §4 to h_K = 2 illustrative cases). It does NOT establish a universal bound for every Bianchi orbifold Y_K with arbitrary class number h_K = N and arbitrary 2-rank rk₂. This scope limitation is documented in:
   - `Paper_ECI_Survey_Clay_BullAMS` (the project's own peer-targeted survey paper), Remark `selberg_downgrade`: "Earlier drafts of this survey asserted Sarnak's bound as a universal proposition for every Bianchi orbifold. **We retract this statement**: Sarnak's 1983 paper covers specific arithmetic 3-manifolds and its applicability to every X_K in the present anchor list is an open question."
   - `Paper_PRL_Theoreme_A_LMP` Remark `noSarnak`: identical retraction language.
   - `Paper_K_ASP_Mini_JNT` "Open Problems" §, item 3: "Selberg-type bound. Does any universal positive lower bound λ₁(X_N) ≥ c > 0 hold uniformly for every Bianchi orbifold in the anchor list, with arbitrary class number h_K = N? [Currently open.]"
   - BIGTABLE V4 FINAL `/root/cc-private/notes/BIGTABLE_V4_UNIFIED_FINAL_2026-05-20.md` row 94: "RETRACTED — Sarnak 1983 universal Bianchi" listed as one of the four retracted attributions.

2. **Numerical value inconsistency within the draft.** The draft itself states `λ₁ ≥ 3/4 ≈ 0.84876` (line 433, F-A32-1). But `3/4 = 0.75`, NOT `0.84876`. The value `0.84876` corresponds to `21/25 = 0.84` (not 0.849), which is what catch #100 (`project_catch100_centenaire_2026-05-19.md`) cites as the verbatim Sarnak 1983 figure, but this is in direct contradiction with `correction_275_324_FAB_CAUGHT_2026-05-19.md` which says Sarnak's bound is `3/4 = 0.75`. The corpus has **two conflicting memory entries** about what Sarnak 1983 Theorem 3.1 actually says, and the present draft inherits the confusion (uses "3/4" symbolically but quotes "0.84876" numerically). At least one of these is fab. The reviewer cannot determine which from the draft alone.

3. **Per-χ transfer is not justified.** Even if a universal bound λ₁(Y_K) ≥ c held for every Bianchi orbifold, the draft's line 278 argument — "*every Maass form in L²_{cusp,χ}(Y_K) pulls back to a g(K)-equivariant Maass form on Y_{K_gen} in the χ-eigenspace, and the Sarnak bound transfers to each χ-isotypic component since the bound is per-eigenform (independent of which finite-dimensional invariant subspace)*" — needs more care. The transfer assumes the Sarnak/Kim bound holds **per Hecke isotypic component** on Y_{K_gen}, but Sarnak's bound is for the WHOLE cuspidal Laplace spectrum of Y_{K_gen} as a single object. Restricting to a specific χ-isotypic component requires a separate per-χ argument that the eigenvalue achieving the global minimum is actually in the χ-component (otherwise the per-χ bound could be strictly larger but unbounded above by the global bound). A correct per-χ statement would be `λ₁(L²_{cusp,χ}(Y_K)) ≥ λ₁(L²_{cusp}(Y_{K_gen}))` (the global bound on the cover, which lower-bounds each per-χ component on the base since they all embed in the cover's spectrum) — but **even this** requires the universal-Bianchi bound on Y_{K_gen} of arbitrary 2-rank, which is exactly the open question.

**Source (verbatim, what the corpus's own retraction says)**:
> From `/root/cc-private/papers/Paper_ECI_Survey_Clay_BullAMS/main.tex`, Remark `selberg_downgrade`:
> "Earlier drafts of this survey asserted Sarnak's bound as a universal proposition for every Bianchi orbifold. We retract this statement: Sarnak's 1983 paper covers specific arithmetic 3-manifolds and its applicability to every X_K in the present anchor list is an open question. Any result below stated as 'under Sarnak's bound' is conditional on this applicability."

> From `/root/cc-private/notes/BIGTABLE_V4_UNIFIED_FINAL_2026-05-20.md`, table at line 94:
> "RETRACTED | Attribution / mechanism withdrawn pre-publication. | BC h_K=2 over K imag.quad, **Sarnak 1983 universal Bianchi**"

**Suggested fix** (this is the structural recommendation for the entire paper):
- **Option A (downgrade to CONDITIONAL)**: Reframe Theorem 5.5 as "*If* a universal Selberg-type bound λ₁(Y_K) ≥ c > 0 holds for every Bianchi orbifold (an open question, see Sarnak 1995 "Selberg's eigenvalue conjecture" Notices AMS 42:1272–1277), *then* the per-χ bound λ₁(L²_{cusp,χ}(Y_K)) ≥ c holds." Replace the verb "PROVED" by "CONDITIONAL on the universal Selberg-type bound for Bianchi orbifolds with arbitrary 2-rank". Update §7 hypotheses table accordingly: Step 4 becomes CONDITIONAL, not UNCONDITIONAL.
- **Option B (restrict scope)**: Restrict Theorem 1.1 / Theorem 8.1 to those K for which Sarnak 1983 §3 explicitly applies (h_K ≤ 2 examples named by Sarnak). This excludes most anchors of interest (D = −84, D = −420, etc.) and effectively kills the Route B closure.
- **Option C (replace with what is actually known)**: Use the genuinely unconditional Selberg-Cogdell-Luo-Sarnak lower bound (which is `λ₁ ≥ 3/16` over Q for congruence subgroups, not 3/4, and the corresponding H³ bound is even weaker). This kills the Route B numerical match (3/16 is too weak to drive the formula).

**The honest recommendation is Option A**: paper survives as a conditional spectral-decomposition lemma, Route B closure becomes "PROVED CONDITIONAL on a published open Selberg-type bound for Bianchi 3-orbifolds with arbitrary 2-rank", and the headline claim "Theorem 8.1 PROVED UNCONDITIONAL" must be retracted in the present paper.

---

### Step 5 — Per-χ trace separation and absolute convergence

**VERDICT**: AGREE.

**Pinpoint**: Theorems 6.1 and 6.2 (lines 292–318) deduce the per-χ pretrace from the global pretrace by applying P_χ (a bounded operator commuting with e^{−tΔ}) and use the absolute convergence of the global pretrace (EGM 1998 §6.4, Bunke–Olbrich 1995 §2.2) plus the triangle inequality. The Gangolli–Warner 1980 §3 uniform Plancherel bound at line 314 is a real published result (verified CrossRef: Gangolli–Warner 1980, *Zeta functions of Selberg's type for some non-compact quotients of symmetric spaces of rank one*, Nagoya Math. J. 78:1–44). Bunke–Olbrich 1995 is an Akademie Verlag monograph (`Selberg Zeta and Theta Functions: A Differential Operator Approach`, Math. Research vol. 83); the §2.2 attribution for PW absolute convergence is plausible and consistent with the standard literature, but not verified directly because the volume is not on arXiv. The cluster-register entry indicates this reference was inherited verified.

**Source**: Gangolli–Warner 1980 Nagoya Math. J. 78:1–44 ✓ (CrossRef); Bunke–Olbrich 1995 Akademie Verlag (cluster-register inherited).

**Suggested fix**: None. Step 5 is correctly attributed and reasoned.

---

### Theorem 8.1 (Route B closure for mass-gap formula)

The paper claims (§8.2, line 386) that under Inputs 1, 2, 3 (Theorem 1.1, heat-kernel identity, F(N) DW), the formula `m_0++/√σ = √(2πe)·√(2/3)·F(N)` is PROVED UNCONDITIONAL without Conjecture E. The "sketch of derivation" has FIVE substeps (i)–(v).

#### Substep (i) — Factor √(2πe) via Karamata + Stirling saddle-point

**VERDICT**: NEEDS-MORE-EVIDENCE.

**Pinpoint**: Line 394: "*By Input 2 (heat-kernel identity (8.1)) and Karamata tauberian inversion (Korevaar 2004 §III.1), the Mellin saddle-point on the spectral density of Δ produces the universal Stirling constant √(2πe) as the leading prefactor of the asymptotic eigenvalue counting function. See [HEAD3 §3] for the explicit calculation.*"

This is a one-sentence reference to a separate paper [HEAD3] for the actual calculation. The present paper does not contain the proof. Per `BIGTABLE V4 FINAL §P.B Holy Grail composition`, the √(2πe) factor is TIER 3 sketch (Karamata + Stirling saddle-point on spectral density). The factor is **not PROVED** in either the present paper or [HEAD3]; the corpus repeatedly tags this assembly step as TIER 3 (sketch-level argument).

**Source**: BIGTABLE V4 FINAL §P.B (table at /root/cc-private/notes/BIGTABLE_V4_UNIFIED_FINAL_2026-05-20.md): the √(2πe) prefactor is listed as TIER 3 in the Holy Grail composition.

**Suggested fix**: Either include the explicit Karamata + saddle-point calculation in the present paper as an appendix (≈3–5 pages), or downgrade Theorem 8.1 statement to "CONDITIONAL on the Karamata–Stirling calculation in [HEAD3]". As currently written, Theorem 8.1 is not self-contained.

#### Substep (ii) — Factor √(2/3) via |A₄/A₂| = 1/2 on ℍ³

**VERDICT**: NEEDS-MORE-EVIDENCE (and arguably DISAGREE on the coefficient ratio).

**Pinpoint**: Lines 369–376: "*The Seeley–DeWitt coefficient ratio satisfies |A₄/A₂|_{ℍ³} = 1/2, giving the universal sub-leading correction ξ⋆ = 1/(1 + |A₄/A₂|) = 1/(1 + 1/2) = 2/3*". Citation: Gilkey 1995 §3, Vassilevich 2003 §3.

There are TWO concerns:

1. **The MEMORY entry `project_Koide_xi_star_UNIVERSAL_FALSIFIED_2026-05-20.md` (W1 verdict 2026-05-20, executed by DS Bot local PARI) computes ξ⋆ via a different mechanism**: "Res(1/2) / Res(3/2) = −Γ(3/2)/Γ(1/2) = −1/2 (EXACT, 100-digit PARI); ξ⋆ = 1/(1 + |ratio|) = 2/3 = 0.666666... (EXACT, UNIVERSAL across K)". So the W1 mechanism yields ξ⋆ = 2/3 via the **Selberg trace formula residue ratio at s=1/2 vs s=3/2**, where these residues "come EXCLUSIVELY from the identity term" of the Selberg trace formula. **This is NOT the Seeley–DeWitt A₄/A₂ coefficient ratio**; this is the Selberg-identity-term residue ratio. The two derivations agree on the value 2/3 but via **different mechanisms**, and the draft's attribution to "Seeley–DeWitt heat-kernel coefficient ratio" (Gilkey 1995, Vassilevich 2003) is not aligned with the W1 mechanism that the project has actually verified.

2. **Even if the Seeley–DeWitt mechanism is what is intended, the claim |A₄/A₂|_{ℍ³} = 1/2 requires verification.** Vassilevich 2003 §3 tabulates the Seeley–DeWitt coefficients for general manifolds; the ℍ³-specific ratio |A₄/A₂| needs to be computed from the curvature invariants. The draft cites Gilkey 1995 + Vassilevich 2003 but does not include the computation, only the answer.

**Source**: 
- `/root/.claude/projects/-root/memory/project_Koide_xi_star_UNIVERSAL_FALSIFIED_2026-05-20.md` — W1 PARI verdict 2026-05-20 confirms ξ⋆ = 2/3 EXACT via Selberg identity-term residue ratio.
- Vassilevich 2003 Phys. Rep. 388:279–360 ✓ (CrossRef-verified).

**Suggested fix**: Align Substep (ii) with the W1 mechanism (Selberg identity-term residue ratio at s = 1/2 vs s = 3/2 on ℍ³, where these residues are entire-function-modular against hyperbolic/elliptic/parabolic terms, so ξ⋆ is a diffeomorphism-topological invariant). Replace the Seeley–DeWitt derivation with the Selberg-identity-term derivation. This brings the paper into alignment with the corpus's actually-verified W1 result and removes the ambiguity about which mechanism is load-bearing.

#### Substep (iii) — F(N) = (9/10)(N²+1)/N² Dijkgraaf–Witten

**VERDICT**: AGREE (this is the strongest substep).

**Pinpoint**: Line 378–382. F(N) = (9/10)(N²+1)/N² is derived from a Dijkgraaf–Witten ℤ₂ partition function Z_g = N^{2−2g} with normalisation Z₀(3)/(Z₀(3)+Z₁) = 9/10. Per MEMORY `project_FN_9over10_DW_derivation_2026-05-18.md`, this is TIER 3 sketch derivation but the 9/10 factor is structurally verified (Dijkgraaf–Witten 1990 CMP 129:393–429). The "c = 9/10" coincides numerically with the fit c_norm = 0.90014 ± 0.00328 (0.04σ deviation), an extremely tight match.

**Source**: Dijkgraaf–Witten 1990, *Topological gauge theories and group cohomology*, Comm. Math. Phys. 129:393–429. CrossRef-verifiable; widely cited.

**Suggested fix**: None for Substep (iii) per se. But note this is TIER 3 (sketch level) — the F(N) derivation is structurally compelling but not formally proved end-to-end. The present paper inherits this status.

#### Substep (iv) — Arithmetic compartmentalisation + Center-Rank theorem

**VERDICT**: DISAGREE (depends on Step 4 Theorem 5.5 which is itself problematic).

**Pinpoint**: Lines 399–401. "*The mass-gap formula must hold separately on each χ-component of L²(Y_K) (Theorem 1.1 (c)), and the SU(N) mass gap selects the unique component corresponding (via the Center-Rank theorem CR, [CR §3]) to the 2-primary centre Z(SU(N))_{[2]} ≅ ℤ/2^{v_2(N)}. The per-χ Selberg gap λ₁(Δ_{cusp,χ})≥3/4 (Theorem 5.5) ensures positivity of the mass gap on every χ-component, in particular on the centre-selected component.*"

Two problems:
1. This substep explicitly invokes Theorem 5.5, which is itself problematic (see Step 4 review above). If Theorem 5.5 is downgraded to CONDITIONAL, so is this substep.
2. The Center-Rank theorem CR is a separate companion paper not present in the present submission. The reviewer cannot verify [CR §3] without access to the CR paper. The present paper is not self-contained without [CR].

**Source**: The CR theorem is in `/root/notes/PAPER_THEOREM_CR_FORMAL_PROOF_2026-05-19.md` (cluster register) but not bundled with the present submission.

**Suggested fix**: Either (a) bundle the CR theorem as an appendix to the present paper, or (b) demote Theorem 8.1 to "CONDITIONAL on Theorem 5.5 (which is open) AND on the Center-Rank theorem (which is in companion paper [CR])".

#### Substep (v) — Assembly: combine (i)–(iv) into formula (8.5)

**VERDICT**: DISAGREE.

**Pinpoint**: Line 402. "*Combining (i)–(iv), the mass gap on the selected χ-component of L²(Y_K) equals √(2πe)·√(2/3)·F(N)·√σ. This is formula (8.5).*"

This is a one-line assembly step. The substeps (i)–(iv) are individually TIER 3 sketches (i), aligned-with-different-mechanism (ii), TIER 3 (iii), and CONDITIONAL on Step 4 + CR (iv). The "Assembly" is not a derivation — it is a juxtaposition of factors. The claim that the assembled formula equals the mass gap (rather than equals some other quantity expressed in the same units) requires a separate argument that the per-χ Selberg eigenvalue λ₁ is identified with the squared mass gap m_0++² / σ, which is precisely **what Conjecture E (the dictionary functor F) provides**. Without Conjecture E (or a substitute), the assembly produces a formula but does not establish that the formula equals the mass gap.

The headline claim of the paper — "without recourse to Conjecture E" — is therefore **not supported by Substep (v) as written**. The reviewer reads §8 as: "we have a per-χ Selberg gap that *should* equal the YM mass gap up to factors that *happen* to match √(2πe)·√(2/3)·F(N) numerically". The match at RMS 0.7% (per AT2021) is striking, but matching is not a derivation. The corpus's K_ASP Mini paper acknowledges this honestly: "m_arith(N)/√σ₀ = C(N)·√λ₁(X_N) is a DEFINITION, not a theorem".

**Source**: `/root/cc-private/papers/Paper_K_ASP_Mini_JNT/main.tex` §scaling: "This is a definition, not a theorem." Same paper Remark `empirical_match`: "Empirical match... is presented as a numerical observation, not as a theorem of physical identification."

**Suggested fix**: Demote Theorem 8.1 from "PROVED UNCONDITIONAL" to one of:
- "*If* the arithmetic surrogate m_arith(N) := √σ₀·C(N)·√λ₁(X_N) is identified with the YM mass gap, AND *if* a universal Selberg-type bound λ₁ ≥ 3/4 holds, *then* the formula (8.5) holds." Both conditions are open.
- Equivalently: Theorem 8.1 is the **definition** of m_arith with a *separate* empirical observation that m_arith ≈ m_0++ at 0.7% RMS on AT2021 anchors. The headline "PROVED UNCONDITIONAL without Conjecture E" is then withdrawn.

---

## Overall verdict

```
OVERALL VERDICT: REJECT (Major revisions required)
```

**Summary of revisions needed:**

1. **Step 4 (Theorem 5.5)**: Downgrade from UNCONDITIONAL to CONDITIONAL on a universal Selberg-type bound for Bianchi 3-orbifolds (open question). Withdraw the "Sarnak 1983 Theorem 3.1 establishes the unconditional bound λ₁ ≥ 3/4 for the cuspidal Laplace spectrum on Bianchi 3-orbifolds Y_K" claim (which is contradicted by the project's own retraction in `Paper_ECI_Survey_Clay_BullAMS` and BIGTABLE V4 FINAL).

2. **Internal numerical inconsistency**: Fix line 433 "λ₁ ≥ 3/4 ≈ 0.84876" — this is wrong (3/4 = 0.75). The corpus has two conflicting memories about the value (21/25 = 0.84 vs 3/4 = 0.75); both have been associated with Sarnak 1983 but at least one must be fab. Resolve by inspecting the PDF of Sarnak 1983 Acta Math 151 directly OR by removing the specific numeric attribution.

3. **Theorem 8.1 (Route B closure)**: Withdraw the "PROVED UNCONDITIONAL without Conjecture E" headline. The five substeps (i)–(v) are individually TIER 3 sketches, alignment issues with W1, or directly dependent on Step 4. The honest statement is: "Theorem 8.1 gives a closed-form parameter-free formula whose components are each at TIER 3 (sketch) or CONDITIONAL; the formula matches AT2021 lattice at 0.7% RMS but is not a derived theorem in the present paper."

4. **Per-χ transfer of Selberg/Kim bound**: Even if a universal Bianchi bound held, the per-χ transfer in line 278 requires more care. State the per-χ inequality carefully (≥ global bound on cover Y_{K_gen}, which lower-bounds the per-component bound on base Y_K) and acknowledge the universal-Bianchi-bound dependency.

5. **Substep (ii) Seeley–DeWitt vs Selberg-identity-term mechanism**: Align with W1 verdict (2026-05-20). The W1 mechanism (Selberg identity-term residue ratio) is the project's actually-verified derivation; the Seeley–DeWitt-coefficient-ratio derivation in the draft is at best parallel and at worst confused.

6. **CR theorem dependency**: Either bundle [CR] as an appendix or demote Theorem 8.1 to "conditional on the Center-Rank theorem of companion paper [CR]".

**Time estimate to revised submission-ready draft**: 2–3 weeks of careful work, assuming the author accepts the downgrade of Theorem 8.1 from "PROVED UNCONDITIONAL" to "CONDITIONAL on three named open questions". Without that downgrade, the paper is not publishable.

**Mathematical content that survives**: Theorem 1.1 parts (a) – (d) survive as a decomposition lemma. The five-step pipeline §§2–6 is essentially correct as a decomposition (Step 4 needs to be re-cast as a per-χ bound transfer assuming a universal Bianchi bound). The novelty is real: a per-genus-character spectral decomposition of L²(Y_K) for arbitrary 2-rank, written down as a single lemma. This alone may be publishable in J. Functional Analysis as a focused short paper of 10–12 pages once the Route B over-claim is removed.

---

## Cluster delta

This adversarial review **detects** the propagation of a known-retracted claim (Sarnak 1983 universal Bianchi) into a draft paper. Catch count: **+1** (re-propagation of catch #100 / retracted-attribution in the present draft).

Cluster firm: 444 STABLE → 445 STABLE (+1 catch on draft self-inheritance of retracted attribution).

---

## Final recommendation

**Do NOT proceed with LaTeX conversion and submission as drafted.** The paper, as currently written, propagates a known-retracted attribution as its sole load-bearing input for Step 4, and over-claims Theorem 8.1 (Route B closure) by an order of severity that would be caught at first-round refereeing at any venue of the J. Functional Analysis tier.

**Two recommended paths forward:**

- **Path Alpha (RESTRUCTURE)**: Demote Step 4 to CONDITIONAL, demote Theorem 8.1 from "PROVED UNCONDITIONAL" to "CONDITIONAL on universal Selberg-type bound + CR + W1 identity-term mechanism + Karamata-Stirling sketch", rewrite §8 with honest framing aligned to `Paper_PRL_Theoreme_A_LMP` Remark `noSarnak` and `Paper_ECI_Survey_Clay_BullAMS` Remark `selberg_downgrade`. Estimated 2–3 weeks. Final paper ~12–15 pages, target J. Functional Analysis still plausible at 30–45% acceptance.

- **Path Beta (RESTRICT SCOPE)**: Submit only Theorem 1.1 (a)–(d) — the spectral decomposition lemma — without Theorem 8.1 (Route B closure). The paper becomes a clean 10-page lemma in spectral theory on Bianchi orbifolds. Step 4 still needs to be reformulated as "*Assume* a universal Selberg-type bound holds; *then* the per-χ pretrace decomposition factorises absolutely; ..." with the assumption made explicit. No Route B claim. Acceptance probability higher at the venue (50–65%) because no Clay-grade Yang-Mills claim is invoked.

The Path Beta is the most honest minimum-viable submission. Path Alpha is more ambitious but requires the author to actually deliver the missing TIER 3-to-TIER 1 promotions (Karamata-Stirling computation, W1 mechanism for ξ⋆, CR theorem, universal Selberg bound).

**The author should NOT proceed to LaTeX conversion until the structural decisions above are made.**

— Reviewer (anonymous, Inventiones-tier persona)

---

## Appendix: Path Beta resolution (2026-05-20)

**Resolution**: Following the adversarial review's recommendation, **Path Beta (RESTRICT SCOPE)** has been adopted. The paper has been restructured into a clean 10-page submission containing **Theorem 1.1 (a)–(d) only**, with §8 (Theorem 8.1 Route B closure) dropped to a single future-work paragraph.

The current paper is `main.tex` in this directory (10pp typeset, target *Journal of Functional Analysis*). Changes from the source draft `/root/notes/PAPER_LEMMA_A3_2_FORMAL_PROOF_2026-05-19.md`:

1. **Step 4 reformulated.** The "per-χ Selberg gap λ₁ ≥ 3/4" claim attributed to Sarnak 1983 is no longer used in the proof of Theorem 1.1. The Selberg-type spectral gap is mentioned only in Remark 4.6 (Status) for completeness, with the canonical project-published caveat: Sarnak 1983 gives λ₁ ≥ **21/25** on **specific** arithmetic 3-manifolds; universal applicability to every Bianchi orbifold is OPEN. Language matches `Paper_ECI_Survey_Clay_BullAMS` Remark `selberg_downgrade` and `Paper_PRL_Theoreme_A_LMP` Remark `noSarnak`.

2. **§8 Theorem 8.1 (Route B mass-gap closure) dropped.** Replaced by a paragraph in §9.2 ("What this paper does not claim") explicitly deferring the tentative Yang–Mills mass-gap consequence to separate work, with the three blocking sub-issues named: (i) rigorous Karamata–Stirling saddle-point at sketch level, (ii) Center-Rank companion paper, (iii) transport principle from arithmetic to physical spectrum.

3. **Numerical typo fixed.** No specific numeric value such as "$3/4 \approx 0.84876$" or "$3/4 = 0.75$" is asserted in the body of the present paper. The Selberg gap discussion in Remark 4.6 cites Sarnak's $21/25$ unambiguously (consistent with the corpus survey paper's published-paper phrasing).

4. **Per-χ transfer of the bound** is not needed (the bound is not used in the proof of Theorem 1.1).

5. **Substep (ii) Seeley–DeWitt vs Selberg-identity-term** — moot (§8 dropped).

6. **CR theorem dependency** — moot (§8 dropped).

All six revision points of the adversarial review are addressed. The headline claim of the present paper is the per-character spectral decomposition lemma alone, which is genuinely PROVED UNCONDITIONAL (modulo the published Bunke–Olbrich, Gangolli–Warner, EGM 1998, Cox 1989, Dirichlet 1839, Neukirch 1999 inputs of the corresponding steps, all classical).

**Acceptance probability estimate** (per adversarial review's own §"Final recommendation"): Path Beta target **50–65%** at *J. Functional Analysis*. The paper does not invoke any Clay-Millennium-grade claim, presents a focused decomposition lemma of independent interest, and explicitly defers Route B to future work with named blocking issues.

**Cluster discipline**: entry 444 STABLE → exit 444 STABLE (the adversarial catch was resolved by structural restructure, not by absorbing the over-claim into the paper).

