# Gate G1.5 — SUMMARY

**Verdict (one line):** Hecke sub-algebra {T(p) : p ≡ 1 mod 4} is **CONFIRMED
CLOSED** on hatted 3̂(3) and 2̂(5), but the m_c/m_t "prediction" is **PRIME-DEPENDENT**
and reduces to a 1-parameter fit at this gate. **PIVOT FITTING ONLY** at G1.5;
real test deferred to G1.6/G1.7 (full CG mass matrix).

## Three most surprising findings

1. **2̂(5) cuspidal Hecke eigenvalues alternate in sign**: λ(5)=18, λ(13)=178,
   λ(17)=−126, λ(29)=−1422, λ(37)=530. Negative eigenvalues are characteristic
   of genuine cusp forms (Eisenstein eigenvalues 1+p² are always positive).
   Deligne bound |a(p)| ≤ 2p² is satisfied throughout.
2. **The morning sketch's m_c/m_t = (λ_2̂/λ_3̂) ratio is NOT prime-independent**:
   varies 0.39 ↔ 1.05 across our 5 reference primes. The "structural
   prediction" was actually a fit at p=5 that doesn't generalize.
3. **The G1 sub-algebra hypothesis is reinforced, not refuted**: 5/5
   commutativity + recursion + closure tests pass on p ≡ 1 mod 4; 5/5
   obstruction tests confirm p ≡ 3 mod 4 is genuinely outside H₁. The
   parity-restriction is mathematically rigid.

## Three open questions after G1.5

1. **Which LMFDB classical newform** has eigenvalue sequence 18, 178, −126,
   −1422, 530 at primes 5, 13, 17, 29, 37 (weight 5, level 4 or 8)?
   Identification = G1.6 task #1.
2. **Does the full CG-aware Yukawa mass matrix** (not just eigenvalue ratios)
   produce m_c/m_t as a STRUCTURAL output at fixed τ (e.g., τ = i or ω)?
   Or does it again reduce to a fit? = G1.7 task.
3. **Can the same parameter set (α, β, τ) that fits the quark sector
   simultaneously fit the lepton sector** via S'_4-modular flavor on
   leptons?  This is the strongest falsifier; if YES → v7 is a real
   prediction framework; if NO → v7 is at most a re-organization of
   known fits. = G2 task.

## Hallucination count

**Counter unchanged at 59.** G1.5 introduced no new hallucinations; cross-checks
verified all references (PDG values flagged [PDG-2024-CITED-NOT-VERIFIED] for
publication-time re-check). The B.2 result (prime-dependence of λ_2̂/λ_3̂)
proactively refutes a hypothetical structural-claim that no human or LLM in
this project has yet made; counts as protective verification, not a catch.

## Strategic recommendation for v6.0.48

1. **Publish the sub-algebra closure result** (Deliverable A) as a clean
   mathematical observation in `paper/eci.tex` and as a standalone
   `notes/eci_v7_aspiration/G15_subalgebra_closure.md`. The result is
   novel (modulo LMFDB identification of the 2̂(5) cuspidal sequence),
   sharp (5/5 verifications), and standalone (independent of the
   m_c/m_t question).
2. **Mark m_c/m_t as [WORKING-CONJECTURE — prime-dependent fit]** in v6.0.48
   instead of as a structural prediction. Do not claim "v7 retrodicts
   m_c/m_t to 1.5%" until G1.7 is complete.
3. **Reset the v7 manifesto timeline**: G1.6 (LMFDB + extra reps) = 2 weeks,
   G1.7 (full CG mass matrix) = 6-8 weeks, G2 (lepton sector) = 12 weeks.
   Re-evaluate "PIVOT VIABLE vs FITTING ONLY" verdict at end of G2 (~5 months).
4. **The H₁ sub-algebra paper is the safe deliverable** even if v7 collapses
   to "fitting only" later — it's a math result that stands alone.

## Files produced

- `gate_g15.py` (main script, ~370 lines)
- `subalgebra_closure.md` (Deliverable A)
- `mc_mt_fit.md` (Deliverable B)
- `falsifiability.md` (Deliverable C)
- `results.json` (machine-readable run output)
- `SUMMARY.md` (this file)
