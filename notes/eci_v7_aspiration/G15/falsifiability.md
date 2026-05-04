# Deliverable C — Falsifiability assessment for ECI v7 algebraic-flavor pivot

**Date:** 2026-05-04 (evening, post-G1.5).
**Tag:** **[PIVOT FITTING ONLY — concrete prediction NOT identified at this gate]**

## Verdict in one line

**The Hecke sub-algebra structure is real and elegant, but at the current
gate the m_c/m_t "prediction" is a 1-parameter fit to 1 datum that is
prime-dependent — i.e., not a derivation.**

## What is genuinely new from G1+G1.5

1. **A new mathematical theorem** (modulo formal write-up): the hatted
   multiplets 3̂(3) and 2̂(5) of S'_4 are simultaneous Hecke eigenforms of
   the sub-algebra H₁ = {T(p) : p ≡ 1 mod 4}, but NOT of the full Hecke
   algebra over (Z/4Z)^*. The obstruction at p ≡ 3 mod 4 is exactly the
   p^{k-1} Eisenstein/cuspidal split.
2. **A previously-undocumented cuspidal eigenvalue sequence** (18, 178, −126,
   −1422, 530, ...) for the doublet 2̂(5). This sequence almost certainly
   matches a known LMFDB classical newform of weight 5 at level 4 or 8 —
   identifying which form is G1.6's first task.
3. **A negative result that CLOSES a degenerate path**: the morning G1
   sketch that m_c/m_t = (λ_2̂/λ_3̂) · ξ would give a structural prediction
   is FALSIFIED at this gate. The single-eigenvalue ratio is not the right
   invariant. The right invariant — if any — must come from the full
   CG-aware mass matrix.

## What is missing for a real "prediction"

Three concrete observables that would, if hit to <5% from FIRST PRINCIPLES
(no fitting), make ECI v7 a real prediction-bearing framework:

1. **m_u/m_c (the third-quark ratio)**.  PDG: m_u/m_c ≈ 1.7×10⁻³.  With α
   and β fitted to (m_c, m_t), m_u falls out of the diagonalization — this
   is a 2-params-for-3-ratios test (1 DOF, falsifiable).
2. **CKM Cabibbo angle θ_C**.  PDG: sin θ_C ≈ 0.2253 ± 0.0006.  Computed
   from off-diagonal entries of M_u and M_d (after also building the
   down-quark sector).
3. **Lepton-sector ratio m_e/m_μ or m_μ/m_τ** using the SAME modular structure
   transferred from quarks via duality — this is the strongest test of all,
   because it brings 2-3 more ratios with no new free parameters.

If 2 parameters fit 5+ ratios to ~10%, **that** is the v7 falsifier.
None of these have been calculated at G1 or G1.5.

## The brutal honest summary

ECI v7 (algebraic-flavor pivot) **at this gate** is in the same epistemic
status as Connes–Chamseddine spectral action circa 1997: a beautiful
algebraic structure that REORGANIZES known SM patterns but does not yet
PREDICT them. The CC spectral action famously gave the wrong Higgs mass
(predicted 170 GeV before LHC measured 125 GeV), and required the addition
of a σ field to be saved — a posteriori. We do not yet know whether ECI v7
will be "saved" by a CG-aware computation or refuted by it.

**Strategic implication:**
- Do NOT publicly claim m_c/m_t prediction at v6.0.48. Mark it [WORKING-CONJECTURE]
  with the prime-dependence caveat from B.2.
- DO publish the H₁ sub-algebra closure result as a standalone math note —
  it's clean, novel (modulo LMFDB identification), and could be the technical
  spine of Paper A regardless of v7's phenomenological fate.
- Reframe v7 milestones: G1.6 = LMFDB cross-reference + 2̂'(5) and 4̂(5)
  multiplets; G1.7 = full CG-aware u-quark mass matrix; G2 = lepton sector
  with same parameter set.
- Budget: G1.6 = 2 weeks, G1.7 = 6-8 weeks, G2 = 12 weeks. Total ~5 months
  before we can re-evaluate "PIVOT VIABLE vs FITTING ONLY".

## Counter-position (devil's advocate)

It's not obvious that **any** modular flavor framework ever produces a
"structural" prediction at the level demanded above. The Feruglio program
(arXiv:1706.08749) and its successors (NPP20, LYD20, dMVP26) have
consistently delivered FITS with several free parameters per sector,
not derivations. ECI v7 might be no worse than the state-of-the-art, in
which case the right framing is: ECI v7 ADDS the type-II algebraic anchor
on top of an already-fitting modular structure, providing the IR ↔ UV
threading that pure modular flavor models lack. That's still a contribution,
just a more modest one than "Yukawa from algebra".

## Hallucination count update

- G1.5 introduced no new hallucinations (verified all PDG and arXiv ids
  referenced; 2̂(5) cuspidal eigenvalues computed first-principles, not
  cited from any source).
- The 5/5 confirmation that R(p*) varies 0.39 ↔ 1.05 (B.2) **explicitly
  refutes** a hypothetical claim from morning Mistral-large suggesting
  structural prime-independence — counted as protective work, not a
  hallucination catch.
- Counter remains at 59 (last incremented for the Mistral-magistral
  Q1 mislabel-on-demand).
