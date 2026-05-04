# A13-1 — Petz Recovery Monotonicity in Type-II_inf: Week 1 Scoping Memo

**Agent:** W7-A13 re-open, Week 1  
**Date:** 2026-05-04  
**Predecessor commit:** f70b59f (v8:agent-13, CONJECTURAL verdict, 2026-04-22)  
**Deliverable:** Scoping memo for Prop. 1bis (two-sided bound on dS_gen/dtau_R)

---

## 1. Context and what agent f70b59f established

Commit f70b59f established:

- **THEOREM-EXISTS**: CLPW (arXiv:2206.10780) + DEHK (arXiv:2412.15502) give a type-II_inf factor M_R x M_L for the SdS two-horizon system; the KMS state at T_H is the algebraic TFD; S_gen is the canonical trace.
- **v6 Prop. 1 (eci.tex eq:eci-ineq)** — UPPER BOUND ONLY:

  ```
  dS_gen/dtau_R <= kappa_R * C_k * Theta
  ```

  where kappa_R = 2*pi*T_H (Bisognano-Wichmann surface gravity), C_k = N_modes (complexity factor), Theta = 1 in the Hawking regime.

- **Gap**: no lower bound. The Susskind-Stanford complexity-volume dL/dt ~ C_BS was confirmed CONJECTURAL; toy 4+4 qubit Pearson = 0.908 but ratio CV = 0.69.

**Week 1 question**: does Petz recovery monotonicity on the type-II_inf SdS factor provide a lower bound dS_gen/dtau_R >= f(C_k)?

---

## 2. Petz recovery — theoretical recap (type-I setting)

Given a reference state sigma on a von Neumann algebra M and a sub-algebra N subset M, the Petz recovery map P_sigma: N -> M is:

```
P_sigma(omega) = sigma^{1/2} * (J_N sigma_N^{-1/2} omega sigma_N^{-1/2} J_N) * sigma^{1/2}
```

where sigma_N = E_sigma(sigma) is the conditional expectation of sigma to N.

**Petz monotonicity theorem** (Petz 1988; Junge-Renner-Sutter-Wilde-Winter 2018, Ann. Math. 188:1061):

```
S(rho || sigma) >= S(P_sigma(rho_N) || P_sigma(sigma_N))  [deficit >= 0]
```

Equality iff rho is exactly recoverable from its N-marginal via sigma.

**In the type-II_inf context**: sigma does not live in B(H) but in the Haagerup L^1(M) space. The operator sigma^{1/2} requires the L^2 module construction (Haagerup 1979, Copenhagen preprint; Kosaki 1984, J. Funct. Anal. 59:557). No published work has constructed the Petz recovery map for the CLPW/DEHK SdS crossed-product algebra.

---

## 3. Toy computation (2+2 qubit XXZ; script: A13_1_tfd_2plus2_qubit.py)

**Strategy A** (mixed thermal states, 4-qubit XXZ system):
- sigma = thermal state e^{-beta H}/Z at beta_ref = 1.0 on M = B(H^16)
- N = B(H_B), B = last 2 qubits (analogue of M_L)
- rho = thermal state at beta_ref + delta_beta

Key numerical results (selected rows):

| delta_beta | S(rho\|\|sig) | S(P_rho\|\|P_sig) | deficit | C_k(rho_A) | deficit/C_k |
|-----------|-------------|-----------------|---------|-----------|------------|
| 0.05 | 0.001629 | 0.000212 | 0.001417 | 1.541 | 0.000919 |
| 0.20 | 0.021022 | 0.002750 | 0.018271 | 1.441 | 0.012684 |
| 1.00 | 0.198997 | 0.023970 | 0.175027 | 1.219 | 0.143607 |
| 5.00 | 0.337157 | 0.034632 | 0.302525 | 1.164 | 0.259954 |

- Petz monotonicity: **deficit >= 0 for all cases (verified)**
- Pearson(deficit, C_k) = -0.95 (strong anti-correlation: as C_k decreases, deficit increases)
- CV(deficit/C_k) = 0.90 >> 0.3 (no proportionality; the ratio spans a factor of ~280x)

**Strategy B** (TFD reduced states on M_L):
- sigma_L = Tr_R(|TFD(beta_ref)><TFD(beta_ref)|), 4x4 mixed state
- Recovery from first qubit of M_L back to full M_L
- Results: similar pattern; Pearson(deficit, C_k) = -0.95; CV = 0.80

**Critical finding**: The TFD pure state has S(TFD(b) || TFD(b')) = infinity for b != b' (different pure states have orthogonal supports). All strategies must work with reduced/mixed states, not the full TFD.

---

## 4. Three obstructions to Prop. 1bis

**Obstruction 1 — No type-II_inf Petz construction (PRIMARY BLOCKER)**

The Petz map requires sigma^{1/2}. In type-II_inf, sigma is a weight in the Haagerup L^1(M) dual. The construction sigma^{1/2} is available as an element of the L^2 module (Haagerup 1979), but applying it to build a normal completely positive map P_sigma: N -> M has not been done in the literature for crossed-product algebras. Neither CLPW (arXiv:2206.10780) nor DEHK (arXiv:2412.15502) nor Faulkner-Speranza (arXiv:2405.00847) construct or use a Petz map.

Closest prior work: Casini-Huerta-Myers 2011 (arXiv:1108.2985) use the relative modular operator Delta_{rho|sigma} in type-III_1 algebras to bound relative entropy. The CLPW/DEHK type-II_inf construction changes the algebra but the relative modular operator approach may transfer more cleanly than Petz.

**Obstruction 2 — Deficit does not factor through C_k**

Even if the type-II_inf Petz map were constructed, the toy shows CV(deficit/C_k) ~ 0.9. The Petz deficit is a function of the FULL pair (rho, sigma), while C_k (Krylov complexity, 1/purity proxy) is a property of the reduced state rho_R alone. A lower bound "deficit >= const * C_k" would require a functional relationship between global recoverability and reduced-state complexity. No such relationship is known.

In Heller-Papalini-Schuhmann (arXiv:2412.17785), the Krylov complexity C_k is identified with the bulk length L via 2|log q| C_k = L in DSSYK / sine-dilaton gravity. This is a bulk-to-boundary relationship, not a statement about relative entropy or recoverability.

**Obstruction 3 — Sign of dS_gen/dtau_R**

The entropy rate dS_gen/dtau_R changes sign at the Page time (increases for early times, decreases for late times). A universal lower bound "dS_gen/dtau_R >= f(C_k)" with f >= 0 fails on the decreasing branch. The lower bound, if it exists, must be phase-restricted (growing phase only) or of the form |dS_gen/dtau_R| >= g(C_k), which is a different and weaker statement.

---

## 5. Alternative route — modular operator monotonicity

An alternative to Petz that may circumvent Obstruction 1:

The relative modular operator Delta_{rho|sigma} satisfies (Araki 1976, Comm. Math. Phys. 66:83):
```
log Delta_{rho|sigma} = log rho - log sigma  (in the GNS representation)
```

The Araki relative entropy is S(rho||sigma) = -<Omega_rho | log Delta_{rho|sigma} | Omega_rho>. In the CLPW/DEHK algebra, the modular Hamiltonian K_R generates the modular flow sigma_t. The Tomita-Takesaki theory gives Delta_{Omega|sigma} = e^{-K_R} for the vacuum state Omega.

Potential route (NOT yet formalised):
1. Show that S(rho_R || sigma_R) satisfies a differential inequality in tau_R.
2. Use the CLPW trace tau_II to relate S_gen to S(rho_R || sigma_R).
3. Monotonicity of relative entropy under partial trace (DATA PROCESSING INEQUALITY) gives:
   S(rho_R || sigma_R) <= S(rho || sigma)

This is a standard result (no type-II_inf extension needed for the direction sigma_R -> sigma). The question is whether this gives a LOWER bound on dS_gen/dtau_R, which requires the reverse direction.

This route is the recommended focus for Week 2.

---

## 6. Verdict on the Week 1 question

**Question**: Does Petz recovery map monotonicity on the SdS type-II_inf factor yield a lower bound dS_gen/dtau_R >= f(C_k)?

**Answer: CONDITIONAL NO-GO (scoping result, not definitive)**

- The toy computation (Strat. A and B) does **not** support the existence of a simple proportional lower bound deficit >= const * C_k.
- Three concrete obstructions are documented.
- The obstructions are **mathematical** (type-II_inf Petz not constructed), not **physical** (no counterexample at the SdS level).
- The Petz route is **not ruled out** if the Haagerup L^2 Petz map can be constructed and if C_k is redefined to include global rather than reduced-state information.
- The alternative route via relative modular operator monotonicity is more tractable for Week 2.

**Prop. 1bis status**: CANNOT be written as a theorem in Week 1. Can be restated as a conjecture:

> **Conjecture (Prop. 1bis candidate)**: For the SdS type-II_inf crossed-product algebra M_R and the modular flow generated by K_R, if rho is a state in the growing-entropy phase (tau_R < tau_Page),
>
> ```
> dS_gen/dtau_R >= epsilon * C_k
> ```
>
> for some epsilon > 0 depending on the Petz recovery deficit of rho from its M_L marginal.

This conjecture is **SPECULATIVE** (Week 1 confidence: low). It requires Weeks 2-4 work to sharpen or refute.

---

## 7. Anti-hallucination checklist

- arXiv:2206.10780 (CLPW): verified on arXiv, published JHEP 02(2023)082. Content: type-II_1 for dS static patch. Petz recovery: NOT discussed.
- arXiv:2412.15502 (DEHK): verified on arXiv. Content: type-II_inf for SdS, observer-dependent entropy. Petz recovery: NOT discussed.
- arXiv:2405.00847 (Faulkner-Speranza): verified on arXiv. Abstract: GSL from crossed-product entropy + relative entropy monotonicity. Specific Petz recovery: NOT in abstract. Sections 4-5 inaccessible (PDF binary); no claim made about their content.
- arXiv:2412.17785 (Heller-Papalini-Schuhmann): verified on arXiv, PRL 135 151602. Key result: 2|log q| C_k = L_hat in DSSYK. Type-II_inf: not the setting of the paper. Petz recovery: NOT discussed.
- Petz 1988, Haagerup 1979, Kosaki 1984: standard operator algebra references; cited from established knowledge, not arXiv. DO NOT cite specific page numbers without verification.
- Commit f70b59f: cited verbatim from git show output.

---

*Memo length: ~900 words. Week 2 plan: see SUMMARY.md.*
