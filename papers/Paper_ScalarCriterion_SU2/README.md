# A scalar finite-volume criterion for a continuum mass gap in SU(2) lattice gauge theory

Version 1.0 (12 November 2026; first deposit). Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

A technical note that transposes the two-dimensional finite-volume doubling criterion of OpenAI (Proposition 2.2 of *Sharp mass bounds for the two-dimensional O(4) model*, 23 September 2026) to SU(2) lattice gauge theories in dimensions four and three, with a conditional continuum assembly and a converse. It is predominantly a transposition, not a new mass-gap mechanism.

## What the note says, and does not say
- Under symmetry and a positive trace-class transfer representation (hypothesis, not formalised), `Δ(n) = 16 log Z(n⁴) − log Z((2n)⁴) ≤ 2⁻⁹` implies `Δ(2n) ≤ 256 Δ(n)²` and `(λᵢ/λ₀)ⁿ ≤ 256 Δ(n) ≤ ½` on every spatial torus `(2ʲn)³` (dimension 3: `2⁻⁷`, 64).
- If `Δ_{β_k}(n_k) ≤ η ≤ 2⁻⁹` along lattices of spacing `ℓ/n_k` and the lattice Osterwalder–Schrader forms converge (existence of the continuum limit: **assumed**), the limit has the q-form of the gap with `q = 256η`; under OS reconstruction (**assumed**) a mass gap `≥ (log 2)/ℓ` and a unique vacuum. This implication is formalised in Lean 4 against the author's statement ClayYM v1.1, with named hypotheses.
- A converse (finite-volume gap with flux sectors, plus a trace bound) is proved on paper at fixed physical size.
- **Not claimed**: any estimate of `Δ` at weak coupling; existence or non-triviality of the continuum limit; reconstruction; application to the formalised construction of OpenAI (Section 9); equivalence with the Yang–Mills mass-gap problem. The Rényi-2 reading of `Δ` is a reformulation. The strong-coupling instance (`β ≤ 0.005`) is conditional on computational inputs reported from one program. The Maxwell witness is conditional on a model identification not derived; the massive-scalar thresholds are numerical.
- **Relation to earlier public work**: version 5.0.0 of the series of Bhattacharjee et al. (doi:10.5281/zenodo.24147967; record created on 11 November 2026, before this note was released; read by us after the note was written) contains, for four-dimensional tori, the same doubling defect, its bracket by thermal traces, the purity reading, and a one-scale criterion whose hypothesis (a family of inequalities between partition functions of finite tori) implies ours and whose conclusion is wider. For the Wilson theory in dimension four the lattice part of this note is a variant of their criterion with a weaker hypothesis and a narrower conclusion (dyadic cubes only). No priority is claimed (Section 1.4 of the note).
- Written by AI models and read by other AI models (roles in the note); not refereed; no human has checked the proofs.

## Contents
- `note/` : `scalar_criterion_su2_v1_0.tex` and `.pdf` (23 pages).
- `lean/` : `CritereScalaire.lean` (35 declarations), `main.lean` (`import Mathlib` + ClayYM v1.1 + `CritereScalaire.lean`; sha256 `944a99f6…`), `MANIFEST.txt`, build outputs, mutants, and `reconstruction_non_auteur_2026-11-11/` (reconstruction (b), from hashed copies).
- `ClayYM_v1_1_extrait/` : six files of ClayYM v1.1, verbatim, with their licence.
- `rejeu_depuis_arbre_git_2026-11-12/` : reconstruction (c) from the git archive of this folder (script, scaffolding, log, tree ids).
- `reproduction/` : programs and outputs for the constants, the witnesses and the strong-coupling instance.
- `SHA256SUMS` : `sha256sum -c SHA256SUMS`.

Lean: Lean 4 v4.34.0, Mathlib commit `5ed2965`; outside the sandbox, `lake env lean lean/main.lean` in a project depending on that Mathlib. The three reconstructions and what they used are described in Appendix A of the note.
