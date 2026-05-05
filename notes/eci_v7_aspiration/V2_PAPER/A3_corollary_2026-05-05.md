# A3 — Verification of Opus' "exact orthogonality in M_u" claim
**Date:** 2026-05-05
**Verifier:** A3 (Sonnet)
**Target:** v2_no_go_paper.tex Corollary 3.4 candidate

## Door verdict
**CLOSED.** The cosine of the angle between the c^c-row (weight-2) and the
t^c-row (weight-5 3̂) of LYD20 Model VI M_u at τ=i is *not* exactly zero. It
is numerically ~5×10⁻⁵, and the symbolic Groebner reduction modulo the S'_4
algebra constraint Y_1²+2 Y_2 Y_3 = 0 yields a nonzero residual polynomial.

## Computed cos value
After stripping the row phases (Y_j^(k) = e^{ikπ/4}·a_j with a_j∈ℝ at τ=i),
the *real* dot product b·c that controls |cos θ| equals, modulo
the algebra constraint a₁²+2a₂a₃=0:
```
b·c = 8·(a₂ − a₃) · (11 a₁ a₂⁴ a₃ + 12 a₁ a₂³ a₃² + 12 a₁ a₂² a₃³
                   + 11 a₁ a₂ a₃⁴ + a₂⁶ + 3 a₂⁵ a₃ − 24 a₂⁴ a₃²
                   − 24 a₂² a₃⁴ + 3 a₂ a₃⁵ + a₃⁶)
```
This is a degree-7 polynomial in (a₁,a₂,a₃) that does **not** belong to the
ideal ⟨a₁²+2a₂a₃⟩, hence b·c ≠ 0 in ℝ[a₁,a₂,a₃]/⟨a₁²+2a₂a₃⟩.

Numerical evaluation at the Dedekind-eta seeds (a₁=1.18034, a₂=−0.26528,
a₃=2.62590, satisfying constraint to 1e-16):
- b·c                     = +0.4950
- ‖b‖·‖c‖                 = 9010.9
- |cos θ|                 = 5.49×10⁻⁵
- θ                       = 89.9969°

The two row-direction vectors are *almost*, but not exactly, orthogonal in
ℝ³.

## Why the claim almost holds (and why it ultimately fails)
At τ=i the (a₂−a₃) prefactor in b·c is small but not zero: numerically
a₂−a₃ ≈ −2.89, so the prefactor itself contributes nothing tight; the
near-vanishing of |cos| comes from the *residual* sextic vanishing to ~10⁻⁴
at the specific (a₁,a₂,a₃) that satisfy a₁²+2a₂a₃=0. There is no symmetry
forcing it to be zero — only the Y_1²+2Y_2Y_3=0 constraint, which is too
weak to eliminate the residual.

Cross-check: the analogous dot products for the other row pairs are also
non-vanishing (all reduced under the same Groebner basis):
- u^c·c^c reduced: −2(a₁a₂² + 3a₁a₂a₃ + a₁a₃² − a₂²a₃ − a₂a₃²)  ≠ 0
- u^c·t^c reduced: 4(a₂−a₃)(a₁a₂⁴+10a₁a₂³a₃+22a₁a₂²a₃²+10a₁a₂a₃³+a₁a₃⁴+…) ≠ 0
- c^c·t^c reduced: as above ≠ 0

The fact that *all* three cosines are O(10⁻⁴–10⁻²) but none is exactly zero
suggests the smallness is a numerical coincidence at the τ=i CM point, not
a structural symmetry. This is consistent with the V2 paper's own
"near-rank-1" wording for the d-block (rather than "exact rank-1").

## Caveats
- LYD20 Model VI column convention (Q₁,Q₂,Q₃) → (Y_1,Y_3,Y_2) is taken from
  v2_audit.py / v2_no_go_paper.tex eq. (Mq_6) lines 1379-1390; if a different
  permutation is used in some Opus draft, the residual changes but is still
  a nonzero element of the quotient ring (verified for cyclic permutation).
- The row "phase" stripping uses the convention Y_j^(k)(i) = e^{ikπ/4}·a_j;
  this is exactly Lemma 1 of v2_no_go_paper.tex (line 150), independent of
  basis choices for the multiplet.
- Multiplet basis ambiguity: the {3̂',I, 3̂',II} weight-5 doublet is not
  unique up to GL(2). I tested only the canonical LYD20 basis (lines
  1872-1875) which is what M_u uses. The c^c-vs-t^c pair examined here is
  basis-free since it only involves the {3} (weight 2) and {3̂} (weight 5)
  *single* multiplets.
- Numerical value 5.5×10⁻⁵ is so small that floating-point SVD diagnostics
  could not distinguish it from "exact zero"; only symbolic computation
  resolves the question.

## Sources
- V2 paper Lemma 1 + M_u definition: `/root/crossed-cosmos/notes/eci_v7_aspiration/V2_PAPER/v2_no_go_paper.tex`
  lines 99-145 (Mq_6 transcription), 150-172 (S-fixed-point lemma).
- LYD20 (arXiv:2006.10722) modular form polynomials: `/tmp/agents_v647_evening/H3/lyd20_src/modular_symmetry_S4prime.tex`
  lines 1865-1876 (Y^(5)_3̂ definition), 341-353 (constraint Y_1²+2Y_2Y_3=0
  and Y^(2)_3 components).
- Numerical seeds & polynomial transcription cross-check:
  `/root/crossed-cosmos/notes/eci_v7_aspiration/V2/v2_audit.py` lines 99-148.
- Verification script: `/root/crossed-cosmos/notes/eci_v7_aspiration/V2_PAPER/A3_up_corollary_verify.py`
- Hallu counter unchanged at 76 (no fabricated references; LYD20 = 2006.10722
  re-verified, not 1907.04299 UAV paper).

## Recommendation for V2 paper
Do **not** add a "Corollary 3.4 (exact M_u orthogonality)" claim. The V2 paper as
currently drafted is correct and complete: the no-go theorem rests on the
M_d {d,s}-block near-rank-1 alone, and the M_u rows being *near* (but not
exactly) orthogonal at τ=i is consistent with — but does not strengthen —
the existing structural argument. Promoting the small numerical |cos|≈10⁻⁴
to "exactly zero" would be incorrect and would need to be retracted on
referee scrutiny.
