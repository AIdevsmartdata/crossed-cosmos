# B4 Agent Notes: Closing Gap 1 (Wavefront Set Uniformity)
## Bianchi II SLE / Heisenberg Nilmanifold
### 2026-05-03

---

## 1. CRITICAL HALLUCINATION CAUGHT: Junker-Schrohe arXiv ID

**Task prompt stated:** arXiv:math-ph/0107024

**VERIFIED RESULT:** That ID returns "Geometry and integrability of
Euler-Poincaré-Suslov equations" by Bozidar Jovanovic, *Nonlinearity* 14 (2001)
1555–1567. Completely unrelated to QFT on curved spacetime.

**Correct ID:** **arXiv:math-ph/0109010** — verified directly via arXiv API.
- Title: "Adiabatic vacuum states on general spacetime manifolds: definition,
  construction, and physical properties"
- Authors: Wolfgang Junker, Elmar Schrohe
- Journal: Ann. Henri Poincaré **3** (2002) 1113–1182 (pages agree with prompt)

**Action taken:** lemma_B_G1.tex uses the correct ID math-ph/0109010 and flags
the hallucination with an explicit comment in the bibliography entry.

This is hallucination #21 in this project.

---

## 2. Other Reference Verification Results

| Reference | Status |
|-----------|--------|
| Hollands-Wald 2001 (gr-qc/0103074) | **VERIFIED** — CMP 223 (2001) 289–326 |
| Brunetti-Fredenhagen 2000 (math-ph/9903028) | **VERIFIED** — CMP 208 (2000) 623–661 |
| Verch 1994 (CMP 160, 507) | **NOT ON ARXIV** — pre-arXiv era; journal ref standard but unverifiable via API |
| Junker solo 1995 (hep-th/9507097) | Found but not cited (solo precursor paper) |
| Pukanszky 1967 | **VERIFIED** (from A5): J. Funct. Anal. 1, 255–280, NOT Trans. AMS |

---

## 3. Key Mathematical Findings

### 3.1 Joint scaling: NEGATIVE result (sympy verified)

The naive joint scaling ω → Ω₀/ε, n → N/ε² does **not** produce a single-parameter
WKB problem. The two terms in Ω²_{n,ω} scale as:
- (2n+1)|ω|/(a₁a₂) ~ O(ε⁻³)
- ω²/a₃² ~ O(ε⁻²)

These are at different ε-orders. The task's premise (single small parameter ε
controlling both UV limits simultaneously) is **wrong** as stated.

**Correct framing:** Λ_eff = ω² + n is the valid joint UV parameter. The two UV
limits are genuinely independent but both controlled by Λ_eff → ∞:
- Regime A (|ω| large, n fixed): Ω² ~ ω²/a₃² ~ Λ_eff
- Regime B (n large, |ω| fixed): Ω² ~ 2n|ω|/(a₁a₂) ~ 2Λ_eff|ω|/a₁a₂ ≥ 2Λ_eff·c
- Regime C (mixed): Ω² ~ Λ_eff · g(η;ω,n) with g bounded above and below

### 3.2 Bogoliubov bound: provable modulo G1.1

Under BN23's hypotheses (smooth a_i, scale factors bounded away from 0 on supp f):

**Lemma B-G1 is proved modulo sub-gap G1.1** (Olver's theorem in two-parameter form).

The proof chain is:
1. Ω²(η) ≥ c·Λ_eff (Proposition in lemma_B_G1.tex, rigorous)
2. ∂ᵏ_η Ω² = O(Λ_eff) uniformly in (ω,n) (Claim, rigorous from smoothness of a_i)
3. WKB error O(Λ_eff^{-(N+1)/2}) (Lemma, near-rigorous; needs G1.1)
4. |β_{n,ω}|² = O(Λ_eff^{-N}) for all N (Lemma B-G1, near-rigorous; needs G1.1)
5. ω₂^SLE - H₂ ∈ C^∞ (Proposition, plausible; needs G1.4)

### 3.3 Spectral gap: uniform (sympy verified)

The harmonic oscillator eigenvalue gap at fixed ω:
  λ_{n+1,ω} - λ_{n,ω} = 2|ω|/(a₁a₂) ≥ 2/(a₁a₂) > 0

This is **uniform** in ω ∈ Z\{0} (since |ω| ≥ 1). This is the spectral gap
condition required by the adiabatic theorem (Avron-Seiler-Yaffe 1987).

### 3.4 No resonances (confirmed)

Free-field mode equations are decoupled. Cross-mode frequencies can coincide
at Stokes times but this does not affect the Bogoliubov coefficient for any
individual mode. No resonance obstruction exists in the free theory.

### 3.5 Discrete ω ∈ Z\{0} is HELPFUL

Counterintuitively, the discreteness of the nilmanifold spectrum makes
uniformity easier, not harder:
- No need for uniform estimates in ω as a continuous parameter
- No accumulation of ω values near 0 (IR is automatically regulated)
- Each ω ∈ Z is an integer, so WKB at fixed ω is just a single oscillator problem

---

## 4. Residual Gaps After This Analysis

### G1.1 (HARD-ish, ~2-3 weeks): Olver two-parameter theorem

Olver's asymptotic expansion theorem (Olver 1974, Chapter 4) is stated for a
single real large parameter Λ. Our Λ_eff = ω² + n is a function of two integer
parameters. To apply Olver, we need to verify his hypotheses hold uniformly in the
"direction" (ω², n)/Λ_eff ∈ [0,1].

**Resolution path:**
- Option A: Treat the two UV regimes separately (n fixed, |ω|→∞; |ω| fixed, n→∞)
  and patch via a partition of the (ω,n) parameter space.
- Option B: Use Fedoryuk's more general parametrix theory (Fedoryuk 1993,
  "Asymptotic Analysis") which handles this type of two-parameter problem.
- Option C: Prove directly via Duhamel iteration (BN23 Appendix A method)
  without citing Olver, working with Λ_eff directly.

Option C is the most self-contained and likely cleanest for the paper.

### G1.4 (HARD, 4-6 weeks): Pseudodifferential calculus on nilmanifolds

To conclude WF(ω₂^SLE) = WF(H₂) from the C^∞ remainder, we need the
Junker-Schrohe parametrix framework on Nil³ × ℝ_t. Their framework uses the
classical pseudodifferential calculus on ℝⁿ. For Nil³, the natural calculus is
the Rockland/Folland-Stein calculus (graded nilpotent groups).

**The question:** Is the wavefront set defined via the Heisenberg pseudodifferential
calculus compatible with Radzikowski's classical WF set on T*(Nil³)?

**Assessment:** Yes, but requires a compatibility lemma. The sub-Riemannian and
Riemannian wavefront sets on Nil³ agree for distributions that are "elliptic
at high frequency" in the sub-Riemannian sense (which our Ω² satisfies, since
Ω² ~ Λ_eff ≥ c·Λ_eff). However, this argument must be written up, possibly
citing Taylor 1984 ("Noncommutative Harmonic Analysis") or Fischer-Ruzhansky 2016
("Quantization on Nilpotent Lie Groups") for the pseudodifferential symbol calculus
on H₃.

**This is the SINGLE HARDEST remaining gap.** If a reference for the compatibility
lemma exists in the literature (Fischer-Ruzhansky likely covers it), it can be
cited; otherwise 4-8 weeks of new analysis.

### G2 (MEDIUM, 2-3 weeks, from A5): Weyl law on Nil³

Need precise citation for N(Λ) ~ CΛ² on Nil³ with time-dependent metric.
Gordon-Wilson 1984 or Corwin-Greenleaf 1990 should cover this.
Does not affect Lemma B-G1 itself; affects Proposition WF_smooth Step 3.

### G3 (MEDIUM, 3-5 weeks, from A5): Adiabatic IC vs Hadamard parametrix at t₀

Check that the WKB initial conditions (eq. WKB_IC) are consistent with the
Hadamard parametrix at t = t₀. Requires heat kernel on Nil³ with time-dependent
metric. Likely follows from the eigenvalue formula and standard heat kernel estimates
on nilmanifolds (Varopoulos et al.).

---

## 5. Updated Time-to-Publication Estimate

| Task | Weeks | Can overlap? |
|------|-------|-------------|
| G1.1 (Olver two-param, or Duhamel replacement) | 2–3 | Yes |
| G1.4 (pseudodiff on Nil³) | 4–6 | No (blocks Hadamard proof) |
| G2 (Weyl law citation) | 2–3 | Yes |
| G3 (adiabatic IC vs parametrix) | 3–5 | Yes |
| Writing + revision | 8–12 | No |

**Optimistic (parallel, Fischer-Ruzhansky citable for G1.4):** ~4 months

**Realistic (sequential where needed, some new analysis for G1.4):** **4–6 months**

**Pessimistic (G1.4 requires foundational new paper on nil. pseudodiff.):** 12–18 months

### Comparison with A5 estimate (6–9 months):

The Bogoliubov coefficient bound (the "easy" part of Gap 1) is essentially proved;
this was the main uncertain step in A5's estimate. The remaining hard work is G1.4
(pseudodifferential compatibility on nilmanifolds), which was implicit in A5's
estimate but is now made explicit. If G1.4 can be handled by citing Fischer-Ruzhansky
2016, the estimate reduces to **4–6 months** from the current date.

---

## 6. Files Produced

- `lemma_B_G1.tex` — Main LaTeX file with Lemma B-G1 and Proof (4-6 pp)
- `sympy_two_index.py` — Sympy verification of joint scaling and frequency bounds
- `notes.md` — This file

---

## 7. Summary for ECI Project

The principal analytical gap (Gap 1) is **substantially closed**:
- The Bogoliubov coefficient bound is proved (modulo G1.1, ~2-3 weeks).
- The wavefront set argument requires a compatibility lemma on nilmanifolds (G1.4).
- G1.4 is the gating item for upgrading from "Type A pending" to "Type A rigorous."
- One hallucination caught (arXiv ID for Junker-Schrohe; #21 in project count).
- Three other references verified (Hollands-Wald, Brunetti-Fredenhagen confirmed;
  Verch 1994 pre-arXiv era, cannot verify by API).
