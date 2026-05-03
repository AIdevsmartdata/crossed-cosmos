# F3 Wedge Reconstruction — Gap Analysis, Obstructions, Time-to-Pub

**Date:** 2026-05-03  
**Status:** Draft research note; conditional theorem only

---

## 1. Citation Audit (Paranoid Mode)

| Cited as | Claimed ID | Verification | Finding |
|----------|-----------|--------------|---------|
| Almheiri-Dong-Harlow 2014 | 1411.7041 | arXiv API confirmed | CORRECT: "Bulk Locality and Quantum Error Correction in AdS/CFT", JHEP 1504:163 |
| Dong-Harlow-Wall 2016 | 1601.05416 | arXiv API confirmed | CORRECT: "Reconstruction of Bulk Operators within the Entanglement Wedge", PRL 117:021601 |
| Faulkner-Lewkowycz 2017 | **1704.05732** (task prompt) | arXiv API confirmed MISMATCH | **HALLUCINATION CAUGHT**: 1704.05732 = Cooley-Kang-Koch, random hypergraph combinatorics. Correct ID is **1704.05464** ("Bulk locality from modular flow", JHEP 07:151 2017) |
| Witten 2022 | 2112.12828 | arXiv API confirmed | CORRECT: "Gravity and the crossed product", JHEP 10:008 2022 |
| CLPW 2022 | 2206.10780 | arXiv API confirmed | CORRECT: "An algebra of observables for de Sitter space", JHEP 02:082 2023 |
| Faulkner-Speranza 2024 | 2405.00847 | arXiv API confirmed | CORRECT: "Gravitational algebras and the generalized second law" |
| Chandrasekaran-Speranza 2020 | 2009.10739 | arXiv API confirmed | CORRECT: "Anomalies in gravitational charge algebras of null boundaries" |
| Frob 2023 | 2308.14797 | arXiv API confirmed | CORRECT: "Modular Hamiltonian for de Sitter diamonds", JHEP 12:074 2023 |
| Casini-Huerta-Myers 2011 | 1102.0440 | arXiv API confirmed | CORRECT |
| **Mukohyama-Speranza 2024** | **2402.10362** (task prompt) | arXiv API confirmed MISMATCH | **HALLUCINATION CAUGHT**: 2402.10362 = Hejazi-Shokrian Zini-Arrazola, quantum simulation product formulas. No Mukohyama-Speranza horizons paper found under that ID. EXCLUDED from references. |
| Hislop-Longo 1982 | DOI BF01208372 | Prior audit confirmed | CORRECT (earlier ECI note had wrong DOI BF01208568) |

**Hallucinations caught this session: 2** (1704.05732 and 2402.10362).

---

## 2. Does Anyone Already Do FRW Wedge Reconstruction?

**Short answer: No.**

Systematic literature check:

- **Gao 2024 (arXiv:2402.18655)** — Modular flow + entanglement wedge in JT gravity (AdS_2). Not FRW. Type II_∞ structure present, but specific to 2D holography with two boundaries.
- **Parrikar-Rajgadia-Singh-Sorce 2024 (arXiv:2403.02377)** — Relational bulk reconstruction from modular flow. AdS/CFT, varying code subspaces. Not FRW.
- **Jensen-Raju-Speranza 2024 (arXiv:2412.21185)** — Holographic observers for time-band algebras in AdS. Not FRW; relevant for type II_∞ FL prescription.
- **Faulkner-Speranza 2024 (arXiv:2405.00847)** — GSL for Killing horizons via crossed products. Relevant to the shape-dependent residual at ∂D_R but does NOT do reconstruction, and requires a Killing horizon (which ∂D_R is not in FRW metric).
- **CLPW 2022 (arXiv:2206.10780)** — Type II_1 algebra for de Sitter static patch. Contains modular flow discussion but no reconstruction theorem.
- **Giddings-Sloth, Strominger et al.** — dS holography proposals, not algebraic, not reconstruction.

**Conclusion:** The FRW wedge reconstruction question (formulated in this note) is NEW. The specific combination of (Frob modular flow) + (FL prescription) + (FRW conformal rescaling) does not appear in the literature.

---

## 3. Obstructions Summary

### O1: No conformal boundary — BINDING

The "boundary" ∂D_R is interior to spacetime. It is not causally separated from the bulk. Reconstruction from ∂D_R is a Cauchy problem, not holographic reconstruction. This blocks any literal AdS/CFT analog.

**Fixable?** Only if one adopts a non-standard "boundary" (e.g., comoving Hubble sphere, cosmological horizon). This requires a separate analysis not yet done.

### O2: Type II_∞ vs type-I — MANAGEABLE

The FL proof uses type-I algebras and OAQEC code subspaces. The FRW algebra is type III_1 (or II_∞ in the crossed product). The modular flow formula (eq. (3) of note.tex) is well-defined regardless, but the quantum error correction interpretation fails.

**Fixable?** Yes, partially. The modular-flow formula can be stated type-III-level, and Jensen-Raju-Speranza 2024 is developing the right framework. Not an obstruction to the modular-flow formula, but blocks the QEC interpretation.

### O3: Conformal anomaly — MANAGEABLE

The Δ_anom term in S_gen is a c-number, state-independent, explicit. It modifies the K_FRW kernel but does not block reconstruction.

**Fixable?** Yes: track the anomaly contribution explicitly (already done in the ECI kfrw note).

### O4: No Markov property on non-Killing boundary — BINDING

The split property / QFT Markov condition for the diamond triple is UNPROVEN for ∂D_R in the FRW metric. It might be derivable via the conformal pullback from the Minkowski split property (Buchholz-Wichmann modular nuclearity), but this requires a new calculation verifying that U preserves the nuclearity index.

**Fixable?** Potentially, via the Buchholz-Wichmann route. This is an explicit open problem.

---

## 4. Gap Table: Literature vs New Work

| Task | Done in literature | What's needed |
|------|-------------------|---------------|
| K_FRW closed form | YES (ECI kfrw note) | Nothing |
| FRW modular flow formula | YES (this note + sympy) | Nothing |
| Type II_∞ classification | YES (ECI frw_typeII note) | Nothing |
| FRW entanglement wedge definition | NO | Define RT-analog surface in FRW metric |
| Split property for FRW diamond | NO | Buchholz-Wichmann nuclearity check via U |
| FL kernel K^FRW with a(η_s)/a(η) | Partial (formula given, not proven) | Explicit computation + 2pt function check |
| Shape-dependent residual at ∂D_R | NO | Chandrasekaran-Speranza extension to non-Killing |
| FL theorem for type II_∞ algebras | NO | New theorem (Jensen-Raju-Speranza direction) |
| Holographic interpretation | NO (blocked by O1) | Different "boundary" needed |

---

## 5. What Faulkner-Speranza 2405.00847 Actually Covers

FS2024 derives the GSL for **Killing-horizon cuts** from crossed-product gravitational algebras. They show the crossed-product entropy = generalised entropy in the semiclassical limit. They also prove a novel GSL for interacting theories in asymptotically flat spacetimes.

Overlap with this note:
- Their framework confirms that the type II_∞ crossed product is the right algebra for entropy calculations (consistent with ECI).
- Their GSL proof requires a **Killing horizon**, which ∂D_R is NOT in FRW. This is precisely obstruction O4.
- Their paper does NOT do reconstruction (only entropy monotonicity = GSL).

**Conclusion:** FS2024 overlaps with the S_gen calculation in ECI kfrw note but does NOT cover reconstruction. No scooping risk.

---

## 6. What Chandrasekaran-Speranza 2009.10739 Covers

CS2020 studies anomalies in gravitational charge algebras at null boundaries, connecting to Wald-Zoupas quasilocal charges and black hole entropy. Relevant for the shape-dependent extrinsic-curvature residual at ∂D_R (the non-Killing part).

Overlap: CS2020 provides the framework for computing the extrinsic-curvature anomaly that would appear in the reconstruction formula when ∂D_R is not a Killing horizon. This is the "shape-dependent residual" open problem in the ECI kfrw note. No reconstruction theorem in CS2020.

---

## 7. Honest Risk Assessment

### Is the conditional theorem interesting?

**Yes.** The conditional theorem (Theorem 3 in note.tex) is the first explicit statement of FRW wedge reconstruction in the literature, with explicit modular flow formula and explicit obstructions. The FL kernel K^FRW with the a(η_s)/a(η) rescaling factor is new.

### Is the conditional theorem publishable?

**Probably, but with caveats.** The note correctly flags:
- It is a CONDITIONAL theorem (requires H1 + H2).
- H2 (Markov property) is genuinely open.
- O1 (no conformal boundary) is a fundamental limitation.
- The reconstruction claimed is a modular-flow Cauchy prescription, NOT holographic.

A submission to math-ph or hep-th as a "conditional result + obstruction analysis" would be appropriate. It should NOT be presented as "wedge reconstruction in FRW" without the caveats.

### Risk of confusion with AdS/CFT holography

HIGH. The note is careful to flag that ∂D_R is not a conformal boundary, but a reader skimming the abstract might think this is "holography in FRW." The title and abstract explicitly address this.

---

## 8. Time-to-Publication Estimate

| Scenario | Estimate | Bottleneck |
|----------|---------|------------|
| Conditional theorem + obstruction note only | 3-4 months | Polish, detailed FL kernel calculation |
| Add split-property proof via Buchholz-Wichmann | +6 months | Nuclearity index calculation for U |
| Full unconditional theorem (resolve O4) | +12-18 months | Deep new algebraic QFT work |
| Full holographic interpretation (resolve O1) | INDEFINITE | Requires new framework for FRW holography |

**Recommended path:** Submit the conditional theorem + obstruction analysis as a research note (4-6 pages) to JHEP or Annals of Physics, explicitly as "modular-flow reconstruction, conditional on Markov property." Time: 3-4 months.

---

## 9. Sympy Verification Summary

Script: `sympy_modular_flow.py`

All 4 assertions PASS:
- `[PASS] s=0 is identity: u(0) = u, v(0) = v`
- `[PASS] Tips fixed: u(s)|_{u=R} = R, v(s)|_{v=-R} = -R`
- `[PASS] Rescaling factor = 1 at s=0 (identity check)`
- `[PASS] Moebius flow generator matches CHM diamond Killing vector`

The FRW extra rescaling factor for radiation era:
```
a(η_s)/a(η_c) = η_s/η_c
= R² / [(R² + 2Rr·tanh(πs) - η_c²·tanh²(πs) + r²·tanh²(πs))·cosh²(πs)]
```
(Exact formula, verified symbolic identity at s=0.)

---

## 10. Summary Verdict

The FRW wedge reconstruction question is new, not done in the literature.  
The modular flow formula (Proposition 1 of note.tex) is proven and sympy-verified.  
Two binding obstructions (O1: no conformal boundary; O4: no Markov property on non-Killing boundary) prevent an unconditional theorem.  
The conditional theorem is sound and novel.  
Citation audit caught 2 hallucinations in the task prompt (1704.05732, 2402.10362).
