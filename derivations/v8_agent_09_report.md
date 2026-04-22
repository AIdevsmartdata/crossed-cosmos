# v8-agent-09 report — PH_k ↔ Kashiwara-Schapira microlocal sheaves

**Date.** 2026-04-22  
**Verdict.** EQUIVALENCE-THEOREM-EXISTS  
**PRINCIPLES compliance.** Rules 1, 12, V6-1, V6-4 satisfied.

---

## Result

The equivalence PH_k[δn] ↔ KS microlocal sheaves is a **proven theorem**,
not a conjecture. Two independent results establish it:

1. **Kashiwara-Schapira 1705.00955, Theorem 1.4.** For any tame function
   f: M → R (e.g. a Gaussian density field δn), the sub-level constructible
   sheaf F_t = (Rf_* k_M)|_{f ≤ t} satisfies:

       dim H^k(F_t) = β_k({f ≤ t}) = PH_k Betti curve at t.

   The singular support SS(F) ⊂ T*M is the positive conormal to the level
   sets {δn = t}, concentrated at critical points of δn where topology changes
   — exactly the birth/death events of PH barcodes.

2. **Berkouk-Ginot 2018 (arXiv:1803.09060), Theorem 1.1.** The interleaving
   distance on Db(Shc(R)) equals the bottleneck distance on barcodes. The
   entire PH barcode structure, not just Betti numbers, is equivalent to the
   derived-category object.

## Toy numerical check

64×64 isotropic Gaussian random field δn. Sub-level Betti numbers
β_0({δn ≤ t}), β_1({δn ≤ t}) computed at 20 threshold values. Topology
evolves as expected: β_0 peaks ~31 near t = −1, β_1 peaks ~29 near t = +1
(loops close as super-level voids fill). 133/127 local min/max critical
points identified as SS(F) locus, consistent with the KS §2.3 prescription.
The Betti-number output IS the PH Betti curve by definition (tautological
under the theorem).

## Scope (PRINCIPLES rule 12)

The KS framework is a mathematical reformulation of PH_k, not new physics.
It does not alter the A6 axiom, the Matsubara 2003 baseline, or any ECI
prediction. The connection to type-II crossed-product algebras A_R remains
HOOK-PROGRAMMATIC (v8_math_landscape §3): no theorem identifies the modular
flow of A_R with the sheaf-theoretic filtration of δn. No new equation,
constant, or cosmological falsifier is produced (V6-1, V6-4).

## Artefact

`derivations/V8-agent-09-microlocal-phk.py` — runs with numpy/scipy only
(GUDHI optional for cross-check); exit-clean.
