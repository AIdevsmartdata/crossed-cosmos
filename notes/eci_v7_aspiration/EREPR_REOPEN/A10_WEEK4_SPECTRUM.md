# A10 -- Week 4: Spectrum-matching verdict for E_n^chord = E_n(K_R)

**Agent:** A10 (Sonnet) on EREPR_REOPEN, Week 4
**Date:** 2026-05-05
**Predecessor:** A6_WEEK3_BERRY_STINESPRING.md
**Mission:** Decide the binary gate identified by A6 Week 3 -- does the chord-energy spectrum E_n^chord (HPS DSSYK) coincide with the modular-Hamiltonian spectrum E_n(K_R) of the CLPW/DEHK type-II_inf static-patch crossed product, at semiclassical 1/N -> 0 order?
**Hallu count entering:** 77

---

## 0. Verdict (TL;DR)

**SPECTRA MISMATCH at the operator level. Property (P1) state matching survives via a Krylov-rebasing identification only if rho_HPS is interpreted as an ENERGY DENSITY, not as a discrete chord population.**

In symbols (with all formulas live-verified from the paper PDFs, see Section 6):
- HPS chord spectrum (PDF p.7, eq. 22): **E(theta) = -cos(theta) / sqrt(2|log q|(1-q^2))**, theta in [0,pi]; spectrum is **bounded continuous** on the interval [-E_max, +E_max] with E_max = 1/sqrt(2|log q|(1-q^2)). Density of states rho(theta) = (q^2, e^{+/-2i theta}; q^2)_inf (HPS p.7 below eq. 28). The chord basis |n> is the Krylov/q-Hermite basis, NOT a Hamiltonian eigenbasis.
- CLPW/DEHK K_R (CLPW p.16, eq. 2.10 footnote; DEHK eq. 3.6, 3.8): **K_R = beta_dS . H + p** (the crossed-product / dressed modular Hamiltonian), where H is the bulk modular Hamiltonian (continuous spectrum on R because the bulk algebra is type III_1) and p is the clock momentum operator (continuous spectrum on R). Spectrum is **unbounded continuous on R** (or on R_>=0 if the projection Pi=Theta(q) constraint is imposed, giving Type II_1; without it, type II_inf with full R spectrum).

The two are fundamentally different operators on different Hilbert spaces:
| | HPS H_chord | CLPW/DEHK K_R |
|--|-------------|----------------|
| Spectrum support | [-E_max, +E_max] (bounded) | R (or R_>=0) (unbounded) |
| Density of states | (q^2; q^2)_inf-weighted | flat (Lebesgue) on R |
| Hilbert space | l^2(N_0) (chord basis) | H_qft (x) L^2(R) (crossed product) |
| Algebraic role | DSSYK transfer matrix T_hat | crossed-product generator |

**Therefore E_n^chord = E_n(K_R) FAILS as a literal spectrum identity.** A6's Case A (rigorous semiclassical theorem) is REFUTED. Case B survives only as a weaker "Krylov density-of-states match" statement (see Section 4).

---

## 1. Live verification of references

(All four references LIVE-VERIFIED via arXiv API + PDF download, 2026-05-05.)

- **HPS = arXiv:2412.17785v2**, Heller-Papalini-Schuhmann, "Krylov spread complexity as holographic complexity beyond JT gravity", 2024-12-23. PDF 502kB, 1262 lines after pdftotext.
- **HOPSW = arXiv:2510.13986v1**, Heller-**Ori**-Papalini-Schuhmann-**Wang**, "De Sitter holographic complexity from Krylov complexity in DSSYK", 2025-10-15. (FLAG: A6's brief had "Wakai"; correct surname is **Wang** -- Meng-Ting Wang of Ghent, A. Heller-Ori-Papalini-Schuhmann-Wang. The brief's author list is incorrect on **two** counts: Ori was missing and Wang was misspelled "Wakai".)
- **DEHK = arXiv:2412.15502v3**, **De Vuyst**-Eccles-Hoehn-Kirklin, "Crossed products and quantum reference frames: on the observer-dependence of gravitational entropy", 2024-12-20. (A6 already flagged the brief had this wrong; A10 confirms the correction stands.)
- **Vardian = arXiv:2602.02675v1**, Niloofar Vardian, "Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands", 2026-02-02. (FLAG: this paper is set in **AdS/CFT** with quantum extremal surfaces and entanglement islands; it does **NOT** reference DSSYK chord algebras and does **NOT** discuss the static-patch crossed product or the de Sitter K_R. Its applicability to the DSSYK-DEHK matching question is by analogy only -- the Lanczos / modular-Krylov methodology transfers, the explicit construction does not.)

Auxiliary refs verified for the comparison: **CLPW = arXiv:2206.10780**, Chandrasekaran-Longo-Penington-Witten, "An algebra of observables for de Sitter space" (full PDF read for K_R formula); **CMPT = arXiv:2306.14732**, Caputa-Magan-Patramanis-Tonni, modular-Lyapunov universality.

**A10 hallu increment: 0. Brief-internal mis-attributions caught: 1 new (Wang/Wakai in HOPSW), 1 reconfirmed (DEHK author list -- already known to A6).**

---

## 2. Explicit chord spectrum from HPS (semiclassical end)

From HPS PDF p.7 (Supplemental Material SM1), the gravitational/transfer-matrix Hamiltonian in chord variables is:

```
H_grav = (1/sqrt(2|log q|(1-q^2))) [-cos(P_hat) + (1/2) e^{i P_hat} e^{-L_hat}]    (eq. 21)
```

with spectrum given by eq. (22):
```
E(theta) = -cos(theta) / sqrt(2|log q|(1-q^2)),   theta in [0, pi]    (eq. 22)
```

The eigenfunctions in the L-basis are q-Hermite polynomials H_n(cos theta | q^2):
```
psi_theta(L) = <theta|L> = H_n(cos theta | q^2),   n = L / (2|log q|)   (eq. 25)
```

The chord-Krylov / chord-number basis |n> is related by ratio with q-Pochhammer norms. The transfer matrix T_hat in the chord basis acts as:
```
T_hat |n> = b_{n+1} |n+1> + b_n |n-1>,   b_n = sqrt([n]_q (1 - q^n))   (q-deformed Lanczos)
```
This is the q-Hermite recursion, a **tridiagonal Jacobi matrix** with continuous limit-point spectrum on [-1, +1] (modulo the prefactor (2|log q|(1-q^2))^{-1/2}).

**Crucial:** the |n> basis is the **Krylov (chord) basis**, NOT a Hamiltonian eigenbasis. The "discrete spectrum" {n=0,1,2,...} is a quantum-number labelling of the Krylov resolution, NOT the energy spectrum.

The TRUE Hamiltonian spectrum is **the continuous interval E in [-E_max, +E_max]** parametrized by theta in [0, pi].

**A6's brief implicitly conflated the chord-quantum-number n with an energy quantum number; this is a category error in the original Week-3 wording "E_n^chord = E_n(K_R)".** The correct comparison must be operator-spectral, not n-by-n.

### Bulk dictionary (HOPSW):

HOPSW eq. (5) and the q -> 1 limit yield:
```
L_eff = 2|log q| n_hat       (chord number = effective bulk length)   (eq. 5)
H_grav = T_hat (transfer matrix coincides with ADM gravitational H)    (eq. 4)
beta_dS(theta) = -2pi / theta   (in the dS regime theta -> pi)         (after eq. 17 / on p.4)
```

The chord-energy E(theta) is identified with the **gravitational bulk Hamiltonian H_grav of sine-dilaton dS_2**, not with the modular Hamiltonian K_R of the static patch.

This is the first crucial distinction: H_grav is the **dynamical** (boost) Hamiltonian on the dS Hilbert space, NOT the dressed-observer modular Hamiltonian K_R = beta_dS . H + p of the crossed product.

---

## 3. Explicit modular Hamiltonian K_R from CLPW/DEHK

From CLPW p.16 (eq. 2.10 and surrounding text) and DEHK Sec. 3.2:

The static-patch crossed-product algebra A_cr is:
```
A_cr = A_R [bowtie] R,   generated by {A_R, e^{i p H_mod} a e^{-i p H_mod}, q}
```
where:
- A_R is the type-III_1 von Neumann algebra of QFT operators in the static patch,
- H_mod is the modular Hamiltonian of A_R for the de Sitter (Hartle-Hawking-Bunch-Davies) state Psi_dS, with H_mod = beta_dS . H_xi (eq. 3.6 of DEHK), where H_xi is the boost generator,
- p is the observer's clock momentum operator (continuous spectrum on R, ideal clock case),
- q = -p (or formal conjugate) is the clock energy.

The dressed (crossed-product) modular Hamiltonian is, by Takesaki duality / direct construction (CLPW eq. 2.10 footnote, "X = beta_dS x"):
```
K_R = H_mod + X = beta_dS . H_xi + p     (with X = beta_dS x, x = -q)
```

Spectrum:
- H_xi has **continuous spectrum on R** (type-III_1 bulk algebra; CLPW p.36-37; "the modular Hamiltonian of a Type III algebra never has a splitting [into one-sided pieces]"; spectrum is unbounded both above and below);
- p has **continuous spectrum on R** (ideal clock, CLPW p.13-14; DEHK eq. 5.12 for non-ideal generalization);
- K_R = beta_dS . H_xi + p has **continuous spectrum on R** (sum of two commuting continuous operators with full real spectra = full real spectrum).

After the Pi = Theta(q) projection (CLPW eq. 2.9 -> Type II_1):
```
A_hat = Pi A_cr Pi,   K_R restricted to image of Pi has spectrum on R_>=0 (or R_<= 0 depending on sign convention)
```
The maximally entropic state has **flat entanglement spectrum** (CLPW p.16, "rho_max = 1, all Renyi entropies vanish").

---

## 4. Comparison: where the spectra differ

| Feature | E(theta) (HPS chord) | K_R (CLPW/DEHK) |
|---------|----------------------|-----------------|
| Operator | Transfer matrix T_hat = H_grav of sine-dilaton dS | Dressed modular Hamiltonian K_R = beta . H_xi + p |
| Spectrum support | Bounded: [-E_max, +E_max], E_max = 1/sqrt(2|log q|(1-q^2)) | Unbounded: R (or R_>= 0 with projection) |
| Spectral measure | rho(theta) = (q^2, e^{+/-2i theta}; q^2)_inf, Plancherel measure of SU_q(1,1) | Lebesgue dE on R (flat for type-II_1 trace) |
| Generator of | Krylov spread (operator complexity) on L^2(SU_q(1,1)) | Modular flow on the crossed product M_R |
| Modular role | Bulk gravitational Hamiltonian | KMS modular Hamiltonian (defines beta_dS thermal state) |
| Relation to entropy | NOT directly entropic | tau_II(e^{-K_R}) = Z_dS thermal partition |

**The two operators are NOT in the same spectral class.** E(theta) is a bounded operator (for fixed q in (0,1)); K_R is unbounded with full real spectrum.

### Possible "weaker" matches that DO survive

1. **Density-of-states match in the high-energy limit.** Both spectra exhibit a Cardy-like growth at high temperatures via the universal modular-Lyapunov 2 pi (CMPT 2306.14732). The HPS density rho(theta) ~ sin theta / |log q| near theta -> pi/2 (E -> 0 thermal regime); K_R has flat density on R; they agree in thermodynamic averages but not in operator content. **This is a thermodynamic, not operator, identification.**

2. **Krylov-Lanczos coefficient match.** The HPS chord algebra has Lanczos coefficients b_n = sqrt([n]_q (1-q^n)) ~ alpha . n + gamma at large n (linear growth, signature of operator-Lyapunov 2 pi T). For K_R, Vardian's modular-Krylov procedure (arXiv:2602.02675) yields modular Lanczos coefficients b^mod_n that also grow linearly at late modular time. **Both have lambda_L^(mod) = 2 pi**, the CMPT universality. This is a Lanczos-asymptotic match, NOT a spectrum match -- different Jacobi matrices with the SAME asymptotic linear growth.

3. **Hawking temperature match.** beta_dS in HPS (theta -> pi limit, eq. 17 of HOPSW: beta_dS = -2pi / theta, formally negative reflecting dS entropy decreasing with energy) coincides with beta_dS in CLPW/DEHK (eq. 2.8 of CLPW, beta_dS dx e^{beta_dS x} measure) at the level of the Wightman 2-point function on the cosmological horizon. **This is the weakest possible match -- only the Bekenstein-Hawking temperature agrees.**

### What does NOT match

- The **support** of the spectrum: HPS bounded vs K_R unbounded. No isometric embedding can map a bounded-spectrum self-adjoint to an unbounded-spectrum self-adjoint while preserving spectrum.
- The **degeneracy structure**: HPS spectrum is multiplicity-1 on (E_min, E_max) with q-Plancherel measure; K_R has degeneracy = dim(H_qft) (infinite for type-III_1 bulk).
- The **algebraic role**: H_grav is the GENERATOR of unitary time evolution on H_HPS (closed, unitary dynamics); K_R is the GENERATOR of the MODULAR automorphism (KMS-thermal, NOT physical time). These are distinct physical roles.

---

## 5. Implications for A6's C_BS construction

A6 Week 3 constructed an isometry V: H_HPS -> H_DEHK via V|n> = |xi_n>. Properties:

- **(P1) state-matching** Phi(rho_HPS) = rho_DEHK: REQUIRES the eigenvalue identity E_n^chord = E_n(K_R), which we have just shown FAILS. **P1 is false at the operator level.**

- **(P2) modular-flow intertwining**: REQUIRES sigma_t^HPS = e^{-i t H_grav} . . e^{i t H_grav} to map to sigma_t^DEHK = e^{-i t K_R} . . e^{i t K_R}. The two flows are generated by different operators with different spectra -- **P2 is false at the operator level.**

- **(P3) Connes-cocycle equivariance**: would follow from P1 + P2; since both fail, P3 also fails.

### What survives (the "rescue path")

What CAN be salvaged is a **Krylov-thermodynamic matching** (much weaker than A6's Case A or B):

**Theorem candidate (Krylov-thermodynamic matching, semiclassical):** Let Z_chord(beta) = int_0^pi rho(theta) e^{-beta E(theta)} d theta and Z_DEHK(beta) = tau_II(e^{-beta K_R}). Then in the regime q -> 1, theta -> pi (the dS large-N regime):
```
log Z_chord(beta_dS) = log Z_DEHK(beta_dS) + O(1/N)    (Bekenstein-Hawking match)
```
This is equivalent to **dS_BH = A_horizon / (4 G_N) at leading order**, a well-known result (CLPW Sec. 4, HOPSW eq. 27). It is NOT a new result; it does NOT promote Case B to a theorem; and it is consistent with EVERY existing dS holography proposal.

The substantive matching A6 hoped for (full operator/spectrum identity) does not exist.

---

## 6. Updated probability estimates (post-Week 4)

| Outcome | Week 1 | Week 2 | Week 3 (A6) | Week 4 (A10) |
|---------|--------|--------|-------------|--------------|
| A: Rigorous lb dS_gen >= f(C_k) (full theorem) | 35% | 20% | 25% | **5%** (refuted at semiclassical) |
| B: Conditional lb (semiclassical or growing-phase only, with explicit bridge) | 40% | 45% | 50% | **30%** (only Krylov-thermodynamic match survives) |
| C: No-go remark with positive formula only | 25% | 35% | 25% | **65%** (mass shifts B -> C) |

Net Week-4 effect: **C goes from 25% -> 65%**. The dominant outcome for the v6.2 S2 (or LMP submission) is now a **no-go remark**: the chord algebra and the crossed-product modular Hamiltonian have intrinsically different spectra; only thermodynamic / density-of-states / Lanczos-asymptotic matching survives, all of which were already implicit in the published Bekenstein-Hawking dS entropy match.

---

## 7. Recommended downgrade for v6.2 S2

**Title for the v6.2 S2 addition:**
"Spectrum non-matching of the DSSYK chord algebra and the de Sitter crossed-product modular Hamiltonian: a no-go for direct identification, with a Krylov-thermodynamic consistency note."

**Statement (verbatim suggestion):**
> Proposition 1bis-(MVT2) (no-go form). Let H_grav be the DSSYK chord (transfer-matrix) Hamiltonian acting on the chord Hilbert space H_chord = l^2(N_0), with continuous spectrum on the bounded interval [-E_max, +E_max], E_max = 1/sqrt(2|log q|(1-q^2)) (HPS arXiv:2412.17785, eq. 22). Let K_R = beta_dS . H_xi + p be the dressed modular Hamiltonian of the static-patch crossed product (CLPW arXiv:2206.10780, eq. 2.10 and DEHK arXiv:2412.15502, eq. 3.6), acting on H_qft (x) L^2(R), with continuous spectrum on R. Then no isometric V: H_chord -> H_qft (x) L^2(R) intertwines H_grav with K_R, because spec(H_grav) is bounded while spec(K_R) is unbounded. Consequently, the conjectured "chord = modular" identification fails at the operator level; only the thermodynamic identity log Z_chord(beta_dS) = log Z_DEHK(beta_dS) + O(1/N) survives, reproducing the standard Bekenstein-Hawking dS entropy A_horizon/(4 G_N).

This is a **publishable consistency note** at MVT2 level (positive formula confirmation, no new theorem).

---

## 8. Hand-off / next-steps options

If the campaign is continued past Week 4:

(a) **Type-conversion route** (long shot, ~5%): introduce a *bounded function* of K_R, e.g., F(K_R) = (2/pi) arctan(beta_dS . K_R / 2), which has bounded spectrum on (-1, +1). Investigate whether F(K_R) and a rescaled H_grav match. This is ad hoc and unlikely to have physical interpretation; flagged for completeness only.

(b) **Modular density-of-states match** (15%): formalize the Krylov-thermodynamic match (Section 4, item 1) as a rigorous statement using CMPT modular-Lyapunov universality. This would give a v6.2 S2 result of the form "the chord and crossed-product Krylov-Lanczos b_n's share leading large-n asymptotic alpha = 2 pi T_dS". Modest novelty; no impact on ER=EPR campaign.

(c) **Accept no-go and pivot** (80%): close the EREPR_REOPEN campaign at MVT2-class consistency, write up the no-go as a v6.2 S2 remark (see Section 7), and reallocate the 4-6 week campaign budget. Original W7 success probability of 35% is now **DEFINITIVELY refuted** at the operator-spectrum level.

---

## 9. Cross-checks and anti-hallucination

- All four primary refs **live-verified via arXiv API** + PDF download + pdftotext extraction.
- Brief-internal mis-attribution caught: **Wang misspelled "Wakai" in HOPSW author list** (new flag, A6 did not catch this).
- A6's brief-internal mis-attributions previously flagged (DEHK = de Vuyst-Eccles-Hoehn-Kirklin not de Boer-Engelhardt-Hertog-Kar) **reconfirmed**.
- HPS chord spectrum formula eq. (22) **directly read from PDF p.7**, not hallucinated.
- CLPW K_R formula eq. (2.10 footnote) and DEHK eq. (3.6) **directly read from PDF**.
- Vardian arXiv:2602.02675 is **AdS/CFT only**, does NOT directly support the dS DSSYK-DEHK matching; demoted to "methodological analogy" rather than "supporting evidence" (A6 implicitly overstated its applicability).
- Mistral large-latest **NOT consulted** (banned per project rules); no external LLM cross-check needed since all derivations are spectrum lookups from published formulas.

**A10 hallu increment: 0. Hallu count: 77 (unchanged).**

---

*Memo length: ~3 pages. Verdict: SPECTRA MISMATCH (operator-level). A6 Case A REFUTED, Case B downgraded to thermodynamic-only, Case C now dominant (65%). Recommended action: write v6.2 S2 no-go remark per Section 7.*
</content>
</invoke>