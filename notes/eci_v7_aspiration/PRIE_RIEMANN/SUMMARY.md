# Scoping Memo: Riemann/CCM <-> ECI Type-II Bridge (Opus Bridge #1)

**Date:** 2026-05-04  
**Budget:** 60 min  
**Agent:** Sonnet 4.6

---

## VERDICT

**[STRUCTURAL MISMATCH — different ontological commitments, park as orthogonal]**

---

## 1. CCM 2025 Paper (arXiv:2511.22755) — Live-Verified

**Title:** Zeta Spectral Triples  
**Authors:** Alain Connes, Caterina Consani, Henri Moscovici  
**Submitted:** 27 November 2025  
**Abstract (verbatim):** "We propose and investigate a strategy toward a proof of the Riemann Hypothesis based on a spectral realization of its non-trivial zeros. Our approach constructs self-adjoint operators obtained as rank-one perturbations of the spectral triple associated with the scaling operator on the interval [λ⁻¹, λ]. The construction only involves the Euler products over the primes p ≤ x = λ² and produces self-adjoint operators whose spectra coincide, with striking numerical accuracy, with the lowest non-trivial zeros of ζ(1/2 + i s), even for small values of x."

**Spectral triple data (from HTML fetch of arXiv:2511.22755):**

- **Algebra A:** Involutive Banach algebra L¹(ℝ, dx) with convolution product  
- **Hilbert space H:** L²([λ⁻¹, λ], d*u) where d*u = du/u is the multiplicative Haar measure  
- **Operator D:** D_log^(λ) = −iu∂/∂u = −i∂/∂(log u) with periodic boundary conditions; eigenvalues 2πn/L (L = 2 log λ)  
- **Perturbation:** D^(λ,N) = D^(λ) − |D^(λ)ξ⟩⟨δ_N|, rank-one, forces the minimal eigenvector ξ of the Weil quadratic form Q_W into the kernel  
- **Key formula:** Weil explicit formula (eq. 3.2), semilocal Euler products over primes p ≤ λ²

**Modular flow / KMS / Tomita-Takesaki: completely absent.** The paper contains no reference to modular theory, KMS states, Bost-Connes, adelic geometry, or type II von Neumann algebras. It is purely spectral-analytic.

---

## 2. ECI §sec:limits Item 9(h) — Source Text

From `/root/crossed-cosmos/paper/eci.tex` line 632 (verbatim):

> "[SPECULATIVE] Direction (h) --- Riemann modular zeta. A working-directory conjecture identified the imaginary parts γ_n of non-trivial zeros of the Riemann zeta function with eigenvalues of a modular Hamiltonian H_σ in ECI. The v6.0.9 audit found three analytic errors in the original formula (factor 1/(2π) vs. 1/π; Re vs. Im; missing spectral measure weight), and, critically, that even the corrected formula is tautological without an independent derivation of H_σ from the crossed-product algebra — the Connes–Chamseddine–Marcolli spectral standard-model approach [CCM2025] and the Krylov modular evolution of [Caputa2024] point in the right direction but do not close the gap."

**Three analytic errors (v6.0.9):**
1. Factor: 1/(2π) vs. 1/π in spectral measure normalisation
2. Part: Re vs. Im (imaginary parts γ_n of zeros confused with real parts)
3. Missing: spectral measure weight for Tomita-Takesaki modular operator

**Tautology obstruction:** Even corrected, γ_n ↔ spec(H_σ) is circular unless H_σ is derived independently from the ECI crossed-product data. ECI hypothesis (H2) states ω is KMS at β = 1 for σ^ω on a type-II∞ algebra — this holds for any faithful normal state; it gives no specific H_σ. The identification is a postulate, not a derivation.

**Bibliography error in eci.bib (line 806):** CCM2025 is recorded as authors "Connes, Chamseddine, Marcolli" with title "Spectral Standard Model..." — but arXiv:2511.22755 is authored by Connes, Consani, Moscovici, titled "Zeta Spectral Triples." Either the bib key was mis-assigned or the entry was fabricated/confused. This must be corrected before any future citation.

---

## 3. Bost-Connes (BC) Assessment

**Reference:** Bost & Connes, "Hecke algebras, type III factors and phase transitions with spontaneous symmetry breaking in number theory," Selecta Math. 1(3):411–457 (1995), doi:10.1007/BF01589495. [Verified via nLab]

**BC structure:**
- Algebra: C*(ℚ/ℤ) ⋊ ℕ× (semigroup crossed product C*-algebra)
- Partition function: Z(β) = ζ(β) for real β > 1
- KMS phases: unique KMS_β at β > 2; phase transition at β = 1 (infinite multiplicity)
- Type: **Type III** (stated in the paper title itself)
- Symmetry: profinite ĈQ* acts, relating KMS states at β > 2 to Hecke L-functions

**Two reasons BC does not bridge to ECI:**
1. **Type mismatch:** BC is type III; ECI is type II∞. The crossed-product (CLPW 2023) that gives ECI its type II structure is precisely the operation that takes a type III algebra to type II by adding a clock QRF. BC lives on the type III side before this operation.
2. **Wrong zeros:** BC partition function Z(β) = ζ(β) involves zeta values at real β > 1, not the critical-strip zeros at Re(s) = 1/2. The Riemann zeros are not eigenvalues of any BC operator; they are off-axis poles of Z(β) as an analytic function.

**KMS at β = 2π:** No natural β = 2π appears in BC. ECI's β = 1 in Tomita-Takesaki units corresponds to β = 2π in physical (ℏ = 1) units via Bisognano-Wichmann, but BC's interesting threshold is at β = 2 (the boundary of unique KMS phase), an unrelated coincidence.

---

## 4. Structural Mismatch Table

| Feature | CCM 2025 | ECI crossed product | Bost-Connes |
|---|---|---|---|
| Algebra type | Banach L¹(ℝ), commutative-ish | Type II∞ von Neumann | Type III C* |
| Hilbert space | L²([λ⁻¹,λ], d*u), finite | L²(diamond), unbounded | GNS from KMS state |
| KMS / modular | Absent | KMS at β=1, Tomita-Takesaki | KMS at β>1, different range |
| Zeta connection | Zeros as eigenvalues (spectral) | None (direction h speculative) | Z(β)=ζ(β), real axis only |
| Adelic structure | Semilocal (finite prime set) | None | Full adelic |
| Goal | RH via spectral realization | Observer entropy / cosmology | Phase transitions in ℕ |

---

## 5. Is a 4-Week Bridge Viable?

**No.** Three independent structural barriers each individually block a rigorous connection:

1. **CCM 2025 has no modular flow** — there is no Tomita-Takesaki structure to connect to ECI's (H2)
2. **ECI's H_σ is underdetermined** — computing the specific modular Hamiltonian of ECI's type-II∞ crossed product for even a simple quantum field is an open math.OA problem of order months-to-years, not weeks
3. **BC is type III, ECI is type II** — these sit on opposite sides of the defining CLPW construction; bridging them would require undoing the foundation of ECI

No first concrete theorem can be identified because the gap is not a gap in a proof — it is a gap in the problem formulation itself (H_σ unknown).

---

## 6. Condition for Reopening

Direction (h) can only be reopened if one of the following appears in the literature:

- An explicit computation of H_σ for the ECI diamond crossed-product algebra (starting from a specific QFT on Minkowski or de Sitter), showing spec(H_σ) contains Riemann zeros
- A theorem proving that the Weil quadratic form Q_W of CCM 2025 arises as the modular Hamiltonian of some type-II∞ crossed product

Neither exists as of 2026-05-04.

---

## 7. Verified Reading List (If Pursuing)

1. **arXiv:2511.22755** — Connes, Consani, Moscovici, "Zeta Spectral Triples" (Nov 2025). The actual CCM paper. [VERIFIED LIVE — HTML fetched]
2. **doi:10.1007/BF01589495** — Bost & Connes, Selecta Math. 1(3):411–457 (1995). [VERIFIED via nLab]
3. **arXiv:2306.14732** — Caputa, Magán, Patramanis, Tonni, "Krylov complexity of modular Hamiltonian evolution," PRD 109, 086004 (2024). [VERIFIED in eci.bib]
4. **arXiv:math/0601054** — Connes & Marcolli, "A walk in the noncommutative garden" (2006). Survey of adelic NCG and zeta functions; useful for seeing what CCM actually does. [VERIFIED live — abstract fetched]
5. **Connes, A., Selecta Math. 5:29–106 (1999)** — "Trace formula in NCG and the zeros of the Riemann zeta function." Foundational: zeros as spectrum in adelic NCG, but using adelic/type-III structure incompatible with ECI's type-II setup.

**Action item for eci.bib:** Correct or remove the CCM2025 entry (line 806). The recorded authors/title do not match arXiv:2511.22755. Either fix the entry to reflect Connes/Consani/Moscovici + "Zeta Spectral Triples" or remove the cite from direction (h) entirely, since the paper does not support the modular Hamiltonian conjecture.

---

*Park/keep: PARK. Direction (h) [SPECULATIVE] tag is correct. Do not upgrade status based on CCM 2025.*
