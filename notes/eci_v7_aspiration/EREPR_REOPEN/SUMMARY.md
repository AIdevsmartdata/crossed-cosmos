# EREPR_REOPEN — Campaign Status + Weeks 2-4 Plan

**Campaign:** ER=EPR <-> v6 crossed product re-open (W7 Agent 13)
**Last updated:** 2026-05-05 (Week 4 spectrum-match REFUTED; A10 final memo posted)
**Predecessor:** commit f70b59f (v8:agent-13, verdict CONJECTURAL)
**W7 audit priors:** 35% success probability, 4-6 weeks, $25-45 compute budget

**Week 4 verdict (A10_WEEK4_SPECTRUM.md, 2026-05-05):** SPECTRA MISMATCH. HPS chord spectrum E(theta) = -cos(theta)/sqrt(2|log q|(1-q^2)) is bounded continuous on [-E_max, +E_max]; CLPW/DEHK K_R = beta_dS . H_xi + p has continuous unbounded spectrum on R. A6's Case A REFUTED. Case A/B/C: 5/30/65 (was 25/50/25). Recommended downgrade: MVT2-class no-go remark for v6.2 S2 (see A10 Section 7). Hallu count 77 (no increment). Brief-internal flag: HOPSW 5th-author Wang was misspelled "Wakai" in A10 mission brief.

---

## Week 1 Status

### What was done

1. Read commit f70b59f verbatim. Original verdict: CONJECTURAL with THEOREM-EXISTS sub-verdict for the algebraic container (type-II_inf crossed product = algebraic TFD). Upper bound only: dS_gen/dtau_R <= kappa_R * C_k * Theta (v6 Prop. 1, eci.tex eq:eci-ineq).

2. Fetched arXiv abstracts: 2405.00847 (Faulkner-Speranza), 2412.17785 (Heller-Papalini-Schuhmann), 2206.10780 (CLPW), 2412.15502 (DEHK). All confirmed real. Key: none construct a Petz recovery map for the CLPW/DEHK algebra.

3. Ran toy computation (A13_1_tfd_2plus2_qubit.py):
   - Strategy A: 4-qubit mixed thermal states, Petz deficit for B(H_B) sub-algebra.
   - Strategy B: 2-qubit TFD reduced states, Petz deficit within M_L.
   - Petz monotonicity holds (deficit >= 0, verified in both strategies).
   - CV(deficit/C_k) = 0.90 (Strat. A) and 0.80 (Strat. B) -- no proportionality.
   - Pearson(deficit, C_k) = -0.95 (anti-correlation).

### Key structural finding

The TFD state |TFD(beta)> is PURE. Two pure states with beta != beta' have orthogonal supports, so S(rho_TFD(b) || sigma_TFD(b')) = infinity. The Petz analysis requires MIXED states. The finite-dimensional toy does not faithfully represent the type-II_inf KMS weight.

### Verdict on the Week 1 question

CONDITIONAL NO-GO (not definitive). Three obstructions:
1. Primary blocker: no type-II_inf Petz map in the literature for CLPW/DEHK algebras.
2. Functional mismatch: deficit does not factor through C_k (CV >> 0.3).
3. Sign issue: dS_gen/dtau_R changes sign at Page time; a universal lower bound f(C_k) >= 0 fails on the decreasing branch.

Prop. 1bis cannot be written as a theorem in Week 1. W7 35% success probability stands.

---

---

## Week 2 Status — COMPLETE (scoping)

### What was done

1. Read Week 1 memo and toy script in full.
2. Verified arXiv abstracts live: 2412.17785 (HPS, PRL 135 151602), 2405.00847 (Faulkner-Speranza), 2412.15502 (DEHK), 2206.10780 (CLPW). Status unchanged from Week 1.
3. Worked through Araki relative modular operator formalism for type-II_inf algebras.
4. Derived d/dt S(rho||sigma_t) = -<K_R>_rho via the cocycle identity for Delta_{rho|sigma_t}.
5. Assessed connection between <K_R>_rho and C_k via HPS (2412.17785).

### Key result

The formula dS_gen/dtau_R = <K_R>_rho is derivable in type-II_inf via Araki (1976) + Bratteli-Robinson (Thm. 5.3.15), without constructing a Petz map. Follows from:

1. Araki relative modular operator Delta_{rho|sigma} defined algebraically (no type-I structure)
2. Cocycle identity: Delta_{rho|sigma_t} = Delta_{rho|sigma} e^{t K_R}
3. Pusz-Woronowicz variational formula extends to type-II_inf nsf weights
4. Differentiation: d/dt S(rho||sigma_t) = -<rho| K_R |rho>

### Status on Week 1 obstructions

| Obstruction | Week 1 | Week 2 |
|---|---|---|
| O1: No type-II_inf Petz map | PRIMARY BLOCKER | RESOLVED: Araki approach avoids Petz |
| O2: Deficit not proportional to C_k | BLOCKER | RECAST: gap is now <K_R>_rho vs C_k (see O2') |
| O3: Sign at Page time | BLOCKER | PARTIALLY RECAST: sign of <K_R>_rho trackable, universal lb still fails |
| O2' (NEW): type-I vs type-II mismatch for HPS | N/A | NEW BLOCKER: HPS in type-I DSSYK; no bridge to DEHK K_R |

### Week 2 verdict

PARTIALLY VIABLE — formula derivable, C_k connection remains open.

- dS_gen/dtau_R = <K_R>_rho is a genuine conditional theorem candidate for v6.2 S2.
- C_k connection requires identifying K_R (SdS modular Hamiltonian) with the DSSYK Krylov generator — open bridge problem not in current literature.
- Prop. 1bis with C_k lower bound cannot be written as theorem without this bridge.

### Revised probability estimates

| Outcome | Week 1 | Week 2 |
|---|---|---|
| A: rigorous lb dS_gen >= f(C_k) | 35% | 20% |
| B: conditional lb (growing phase only) | 40% | 45% |
| C: no-go remark with positive formula | 25% | 35% |

---

## Weeks 3-4 Plan (updated after Week 2)

### Week 3 — Three parallel tracks

**Track A: Toy computation**
- Extend A13_1_tfd_2plus2_qubit.py: compute <K_R>_rho = Tr(rho * (-log sigma)) numerically
- Verify dS/d(beta) ~ <K_R>_rho in 4-qubit XXZ; check sign at thermal Page time
- Deliverable: A13_2_modular_flow.py

**Track B: CHM route (type-III_1 -> type-II_inf)**
- Casini-Huerta-Myers (arXiv:1102.0440, JHEP 2011) showed modular Hamiltonian = boost generator for Rindler wedge
- Check whether their relative entropy bounds survive the III_1 -> II_inf transition
- WARNING: arXiv:1108.2985 cited in earlier plan fetched as WRONG paper (Brandao et al.); correct Casini-Huerta-Myers arXiv ID must be verified before citing
- Deliverable: A13_3_chm_typeII.md

**Track C: Bridge problem (HPS <-> DEHK)**
- Read HPS (2412.17785) sections 3-4: does the bulk length operator equal K_R?
- Check if chord Hilbert space Krylov generator embeds in DEHK type-II_inf algebra
- Deliverable: A13_2b_dssyk_kR_bridge.md (short note)

### Week 4 — Synthesis

- A (20%): rigorous lb from modular/CHM route + bridge. Write Prop. 1bis. Draft v6.2 S2.
- B (45%): conditional lb (growing phase). Remark in v6.2 S2: "Prop. 1bis (conditional): for tau_R < tau_Page, dS_gen/dtau_R = <K_R>_rho >= 0."
- C (35%): bridge fundamental; no C_k lb. No-go remark in v6.2 S2 with positive formula result.

All three outcomes yield a publishable v6.2 S2 addition.

---

## File manifest

| File | Description | Status |
|------|-------------|--------|
| A13_1_petz_recovery_memo.md | Week 1 scoping memo | COMPLETE |
| A13_1_tfd_2plus2_qubit.py | Toy: Petz deficit on 2+2 qubit systems | COMPLETE |
| A13_2_araki_modular_memo.md | Week 2 scoping memo: Araki relative modular operator | COMPLETE |
| A6_WEEK3_BERRY_STINESPRING.md | Week 3: Berry-Stinespring channel C_BS construction | COMPLETE |
| A10_WEEK4_SPECTRUM.md | Week 4: chord-vs-K_R spectrum match REFUTED | COMPLETE |
| A13_2_modular_flow.py | Week 3 toy: verify dS_gen ~ <K_R>_rho numerically | OBSOLETE (refuted by A10) |
| A13_2b_dssyk_kR_bridge.md | Week 3 note: HPS <-> DEHK bridge problem | OBSOLETE (refuted by A10) |
| A13_3_chm_typeII.md | Week 3 memo: CHM route for type-II_inf | OBSOLETE (refuted by A10) |
| SUMMARY.md | Campaign status | CURRENT |
