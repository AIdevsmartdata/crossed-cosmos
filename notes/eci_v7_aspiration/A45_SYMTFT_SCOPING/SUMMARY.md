# A45 — SymTFT Z(Rep S'_4) scoping for v7.4 modular flavour

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A45 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held)

## Verdict

**WEAK** — mention in v7.4 amendment, do **not** commit to a 4-8 week LMP companion paper. SymTFT is the correct *abstract* home for the H_1 sub-algebra closure, but Z(Rep S'_4) on its own does not produce the p ≡ 1 (mod 4) congruence selection (that lives at the Galois / nebentypus χ_4 layer, one level above the categorical SymTFT data).

## Live-verified literature

| Ref | Verified | Relevance |
|---|---|---|
| Antinucci–Copetti–Schäfer-Nameki, **arXiv:2408.05585** (Aug 2024, rev Feb 2025) "SymTFT for (3+1)d Gapless SPTs" | WebFetch ✓ | (3+1)d SymTFT framework; **no** double-cover / metaplectic / Hecke content |
| Bergman–Heckman–Hübner et al., **arXiv:2603.12323** (Mar 2026) "On the SymTFTs of Finite Non-Abelian Symmetries" | WebFetch ✓ | General DW-bulk / Drinfeld-centre framework for finite non-abelian G; **no S_4 / 2T worked example** |
| Bhardwaj–Schäfer-Nameki, **SciPost Phys. 19 (2025) 098** "Generalized charges, part II" | WebSearch snippet | "Topological defects of SymTFT form the Drinfeld center of the symmetry category" |
| Freed–Moore–Teleman, **arXiv:2209.07471** (rev Jul 2024) "Topological symmetry in QFT" | WebSearch ✓ | Foundational; agnostic to metaplectic |
| Jia–Luo–Tian–Wang–Zhang, **arXiv:2604.25821** (Apr 2026) "Categorical Symmetries via Operator Algebras" | WebFetch ✓ | Symmetry-cat ↔ groupoid C*-algebra bridge; **no** type-II / modular flow / Hecke |

## Why WEAK and not GRAFT

1. **Categorical level matches automatically**: Z(Rep S'_4) ≅ Rep(D(S'_4)) is the topological-defect data of the 3d Dijkgraaf-Witten theory with gauge group S'_4. No new theorem.
2. **Arithmetic mismatch**: H_1 = ⟨T(p) : p ≡ 1 mod 4⟩ is selected by Galois / χ_4 nebentypus action; Z(Rep S'_4) is purely categorical and does **not** isolate H_1.
3. **A11 Modular Shadow connection: NULL**. A11's bound theorem lives on the Tomita-Takesaki / Parker-bound side; no verified 2024-26 SymTFT paper bridges to type-II crossed products.
4. **Honest sub-bridge that would need to be built**: Galois-equivariant fusion-category framework where Z₁(Rep S'_4) ⊂ Z(Rep S'_4) is the χ_4-equivariant sub-MTC. This formalism is **not** in any of the 5 verified papers — would need Theo Johnson-Freyd-class math.CT.

## v7.4 amendment text (drop-in, ~80 words)

> *Categorical reformulation (open).* Theorem 3 admits a tentative SymTFT re-reading: the topological defects of Z(Rep S'_4) — equivalently of the (2+1)d Dijkgraaf-Witten theory for S'_4 (Bhardwaj-Schäfer-Nameki SciPost Phys. **19** (2025) 098; Bergman et al. arXiv:2603.12323) — carry a natural action of a Galois-twisted endomorphism algebra. We conjecture H_1 is the χ_4-equivariant part. A rigorous formulation requires Galois-equivariant fusion-category data not currently developed; we leave it as an open problem.

## Suggested contacts (only after P-NT paper on arXiv)

Sakura Schäfer-Nameki (Oxford, SymTFT PI), Lakshya Bhardwaj (IAS/Oxford), Jonathan Heckman (Penn), **Theo Johnson-Freyd (Dalhousie, Galois-equivariant tensor categories — the missing piece)**, André Henriques (Oxford).

## Files referenced

- `/root/crossed-cosmos/notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.tex` (Thm 3 closure, lines 200-216)
- `/root/crossed-cosmos/notes/eci_v7_aspiration/A11_MODULAR_SHADOW_THEOREM/SUMMARY.md`
- `/root/crossed-cosmos/notes/eci_v7_aspiration/STRATEGIC_OPUS/STRATEGIC_SYNTHESIS.md` lines 161-165 (§3.1.3 SPECULATIVE, §3.1.4 BLOCKED)
