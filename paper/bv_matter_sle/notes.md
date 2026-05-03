# D2 — Bianchi V Matter: Residual Gaps and Time-to-Publication Notes

Generated: 2026-05-03  
Status: Draft v0.1 — all sympy/numerical checks passed.

---

## 1. VERIFIED RESULTS (no residual gaps)

| # | Claim | Status |
|---|-------|--------|
| 1 | BV Lie algebra: [e3,e1]=e1, [e3,e2]=e2; Tr(ad_e3)=2, class B | VERIFIED by sympy (Task 1) |
| 2 | Vacuum BV = Minkowski via T=t cosh χ, R=t sinh χ | VERIFIED by sympy (Task 2) |
| 3 | K-L eigenfunction φ_ρ(χ) = sin(ρχ)/(ρ sinh χ), eigenvalue ρ²+1 | VERIFIED by sympy (Task 3) |
| 4 | Plancherel measure ρ² dρ on [0,∞) | STANDARD (Helgason, Faraut) |
| 5 | Spectral gap inf σ(−Δ_{H³}) = 1 | VERIFIED by sympy (Task 8) |
| 6 | V_eff(τ) = 2/τ² for dust matter + conformal coupling on H³ | VERIFIED by sympy (Task 4) |
| 7 | ω²_ρ(τ₀) > 0 for all ρ ≥ 0 when τ₀ > √2 | VERIFIED analytically (Prop 1) |
| 8 | Wronskian conservation for RK45 modes | VERIFIED numerically (Task 9) |
| 9 | BN23 arXiv:2305.11388 exists, J.Math.Phys. 64:113503 (2023) | arXiv-VERIFIED |
| 10 | Radzikowski 1996 CMP 179:529-553 | Journal-VERIFIED (Project Euclid) |
| 11 | Brunetti-Fredenhagen-Köhler arXiv:gr-qc/9510056 | arXiv-VERIFIED |
| 12 | Goldfeld-Kontorovich arXiv:1102.5086 (K-L Plancherel) | arXiv-VERIFIED |
| 13 | Lebedev 1965 monograph existence | VERIFIED via Internet Archive |

---

## 2. CRITICAL CORRECTION FROM SYMPY

**V_eff ≠ 0 for dust matter on H³.**

An earlier summary (propagated from the context block) claimed
"Liouville transform removes the friction term → S''(t) + ω²(t) S(t) = 0 with ω²(t) = ρ²+1."
This is INCORRECT for k=−1 (H³) in conformal time.

The correct result is:
- Mode equation (conformal time): u'' + [ρ² + 1 − 2/τ²] u = 0
- V_eff(τ) = a''/a = 2/τ² ≠ 0

This does NOT break the Hadamard argument. The spectral gap +1 ensures
ω²_eff ≥ 1 − 2/τ₀² > 0 for τ₀ > √2 (all ρ ≥ 0).
The role of the spectral gap is precisely to absorb this potential.

Without the gap (Bianchi I, k=0), the mode equation would be u'' + [ρ² − 2/τ²] u = 0,
and the ρ=0 mode has ω²_eff = −2/τ² < 0 for all τ: tachyonic, never positive-frequency.
With the gap (k=−1), ω²_eff(ρ=0) = 1 − 2/τ₀² > 0 for τ₀ > √2.

**Action required in note.tex:** Remark 3.5 already documents this correction.
The proof of Theorem 1 uses the correct V_eff = 2/τ² throughout.

---

## 3. RESIDUAL GAPS (ordered by severity)

### GAP A (MEDIUM): Mehler-Sonine uniform pointwise bound
**What is needed:** A uniform bound
  |K_{iρ}(x)|² · ρ · sinh(πρ) ≤ C(x)   for all ρ ≥ 0, x > 0

**What is available:** Lebedev §6.5 gives the L² identity (eq. 6.5.1).
The asymptotic K_{iρ}(x) ~ sqrt(π/(2ρ sinh(πρ))) · cos(ρ ln(2/x) + φ_ρ) for ρ→∞
implies the integrand is bounded by a constant × (1 + ρ·oscillation).

**Path to closure:** Either:
(a) Check Lebedev §5.7 and §6.5 in the physical library for explicit uniform bounds, or
(b) Prove directly: for large ρ the bound follows from the asymptotic formula;
    for small ρ, K_{iρ}(x) → K_0(x) which is bounded in ρ.
    This is a straightforward 2-page lemma.

**Impact on main theorem:** GAP A affects only the diagonal UV control at
coincident points. It does not affect the wavefront set argument
(which is a WF, not a pointwise bound). The Hadamard criterion
via WF set (Theorem 4.3) is unaffected.

### GAP B (LOW): Joseph (1966) Phys. Lett. 20:281 citation
**Status:** Pre-arXiv, cannot verify on arXiv.
DOI: 10.1016/0031-9163(66)90537-4

**Path to closure:** Access via Elsevier ScienceDirect (Physics Letters archive).
The result is independently proven by sympy in note.tex Prop 2.2 and
cited also via Ellis-MacCallum (1969) CMP 12:108.

**Action:** Keep in references with explicit flag. Note that Prop 2.2 is
self-contained and does not logically depend on Joseph (1966).

### GAP C (LOW): Faraut (1979) H^n Plancherel reference
**Status:** Pre-arXiv book chapter in Springer Lecture Notes 739.
Used only to support the Plancherel formula, which is also covered by Helgason (1984).

**Path to closure:** Replace sole citation with Helgason (1984), which is more
accessible and covers the same material. Keep Faraut as secondary reference.

### GAP D (MEDIUM): Full BN23 §3.3 compactness argument for V_eff ≠ 0
**What is needed:** BN23 §3.3 proves SLE existence via minimization over
a finite time interval. The present paper uses the instantaneous version
(β_ρ = 0, Prop 4.2). For the full time-averaged SLE, BN23 compactness
argument requires ω_ρ(t) > 0 on the full interval, not just at τ₀.

**Path to closure:** Since V_eff(τ) = 2/τ² → 0 as τ → ∞, for any finite
interval [τ₀, τ₁] with τ₀ > √2, inf ω²_ρ(τ) = ρ² + 1 − 2/τ₀² > 0.
This suffices for BN23 §3.3. State this explicitly in the paper as Lemma 4.3.

### GAP E (LOW): Radzikowski WF analysis for V_eff = 2/τ² potential
**What is needed:** The propagation-of-singularities argument must handle
the non-zero potential V_eff ∈ L¹.

**Path to closure:** Standard: for Schrödinger equation with L¹ potential,
the scattering operator is a bounded perturbation of the free evolution,
so WF(W) = WF(W_free). See Reed-Simon vol II, §XI.3.
Add a one-paragraph remark in the proof of Theorem 4.3.

---

## 4. TIME-TO-PUBLICATION ESTIMATE

### Tasks remaining (from v6.0.24 estimate: 4-6 weeks)

| Task | Time | Status |
|------|------|--------|
| Fix V_eff correction throughout | 0.5 days | In note.tex already |
| Close GAP A (Mehler-Sonine bound) | 3-5 days | Lemma to write |
| Close GAP D (BN23 compactness, Lemma 4.3) | 1-2 days | Straightforward |
| Close GAP E (WF + L¹ potential remark) | 1 day | Standard ref |
| Physical library check: Joseph (1966) | 0.5 days | Low priority |
| Full proof of Theorem 4.3 (expand sketch) | 1 week | Core work |
| Section 5 extensions: BIX, anisotropic BV | 1 week | New material |
| Referee-quality literature cross-check | 3 days | Standard |
| LaTeX polish + notation consistency | 2 days | Standard |

**Total: 3-4 weeks** to a submittable arXiv preprint.
This is within the v6.0.24 estimate of 4-6 weeks;
the simplification from V_eff=0→V_eff=2/τ² (GAP A correction) actually
makes the paper *more interesting* because it showcases the spectral gap
as the mechanism, not a trivial V=0 coincidence.

---

## 5. CITATION INTEGRITY SUMMARY

All arXiv-verifiable citations have been checked:

| Citation | arXiv ID | Status |
|----------|----------|--------|
| BN23 | 2305.11388 | VERIFIED |
| GK11 (Goldfeld-Kontorovich) | 1102.5086 | VERIFIED |
| BFK95 (Brunetti-Fredenhagen-Köhler) | gr-qc/9510056 | VERIFIED |
| Olbermann 2007 | 0704.2986 | arXiv exists |

Pre-arXiv references requiring library access:
- Joseph (1966) Phys.Lett.20:281 — DOI 10.1016/0031-9163(66)90537-4
- Ellis-MacCallum (1969) CMP 12:108 — DOI 10.1007/BF01645908
- Radzikowski (1996) CMP 179:529 — Project Euclid confirmed
- Lebedev (1965) — Internet Archive confirmed
- Faraut (1979) — book chapter, no independent verification
- Parker-Toms (2009) — standard textbook
- BKL (1982) Adv.Phys.31:639 — DOI 10.1080/00018738200101428
- Lüders-Roberts (1990) CMP 134:29 — DOI 10.1007/BF02102088
- Helgason (1984) — standard textbook
- Duistermaat-Guillemin (1975) — standard reference

**Hallucination risk assessment:** NONE of the arXiv citations appear fabricated.
All non-arXiv citations have plausible DOIs or journal references.
Joseph (1966) is the highest-risk citation (pre-arXiv, unusual title),
but is rendered non-essential by the self-contained Proposition 2.2.

---

## 6. KEY STRUCTURAL INSIGHT (for the abstract / introduction revision)

The Hadamard property on BV-matter rests on a single algebraic identity:

  For H³ (k=−1) FLRW with conformal coupling:
    ω²_ρ(τ) = ρ² + 1 − a''(τ)/a(τ)
                    \_____/ \_________/
                spectral   potential
                  gap

  For dust: a''(τ)/a(τ) = 2/τ² → 0 as τ → ∞.
  The spectral gap 1 dominates for τ > √2.

  For T³ (k=0) FLRW with conformal coupling:
    ω²_ρ(τ) = ρ² − a''(τ)/a(τ)

  For dust: ω²_0(τ) = −2/τ² < 0 always. IR obstruction permanent.

This is the cleanest possible statement of why BV-matter is Hadamard
and BN-I-matter is not (for massless conformal scalar).
It should appear as a display equation in the Introduction.

---

## 7. DELIVERABLES CHECKLIST

- [x] /tmp/agents_2026_05_03_lecture_abc/D2_BV_matter/sympy_check.py
- [x] /tmp/agents_2026_05_03_lecture_abc/D2_BV_matter/note.tex
- [x] /tmp/agents_2026_05_03_lecture_abc/D2_BV_matter/notes.md

All three files created and verified.
