# Paper Lemma A3-2 — Per-character Selberg pretrace decomposition on Bianchi 3-orbifolds (target J. Functional Analysis)

**Status**: **SUBMISSION-READY — Path Beta scope restricted (2026-05-20)**.

## Description

A 10-page paper proving a single technical lemma about the Selberg pretrace formula on the Bianchi 3-orbifold $Y_K = \mathrm{PSL}_2(\mathcal{O}_K)\backslash\mathbb{H}^3$: namely, that $L^2(Y_K)$ admits a canonical orthogonal decomposition along the Pontryagin dual of the genus character group $g(K) = \mathrm{Cl}(K)/\mathrm{Cl}(K)^2$, the heat semigroup block-diagonalises, the pretrace identity factorises into one absolutely convergent identity per character, and the cuspidal–continuous splitting is preserved per character.

The proof rests on a five-step pipeline (Hecke commutation, character projectors, self-adjointness via bounded Borel functional calculus, non-vanishing $L(\psi_\chi,1)\neq 0$ via Dirichlet 1839, per-$\chi$ trace separation via Bunke–Olbrich + Gangolli–Warner). All steps are proved unconditionally; no universal Selberg-type bound is invoked.

Three explicit PARI/GP falsifiables at $D\in\{-15,-84,-420\}$ are stated.

## Target

**Journal of Functional Analysis** (Elsevier), primary.

Alternates considered: J. Number Theory, Trans. AMS, Compositio Math.

## Files

- `main.tex` — LaTeX source (amsart, 10pp typeset)
- `refs.bib` — bibliography (12 verified entries, no new arXiv IDs)
- `main.pdf` — compiled PDF (10 pages)
- `cover_letter.md` — cover letter for JFA submission
- `pre_submission_checklist.md` — complete pre-submission audit
- `ADVERSARIAL_REVIEW.md` — original adversarial review (REJECT verdict on §8 Theorem 8.1 over-claim) + Path Beta resolution appendix
- `README.md` — this file

## Path Beta resolution

The adversarial review of the earlier 20-page draft (`/root/notes/PAPER_LEMMA_A3_2_FORMAL_PROOF_2026-05-19.md`) identified two issues:

1. **Finding 1 (Step 4 attribution)**: Resolved by aligning Sarnak 1983 attribution language with the canonical published phrasing in sibling papers (`Paper_ECI_Survey_Clay_BullAMS` Remark `selberg_downgrade`, `Paper_PRL_Theoreme_A_LMP` Remark `noSarnak`): Sarnak gives $\lambda_1 \geq 21/25$ on **specific** arithmetic 3-manifolds; universal applicability is OPEN. In the present paper, the Selberg spectral gap is **not invoked** in the proof of Theorem 1.1 (a)–(d) at all; it is only mentioned in Remark 4.6 for completeness, with the open-question caveat.

2. **Finding 2 (§8 Theorem 8.1 over-claim)**: Resolved by **dropping §8 entirely** (Path Beta restrict-scope). The tentative "Route B mass-gap formula closure" is moved to a single "future work" paragraph that names the three blocking sub-issues (Karamata–Stirling at sketch level; Center-Rank companion paper; transport principle from arithmetic to physical spectrum).

The present paper is the maximal honest unconditional content: a clean spectral-theory lemma in 10 pages.

## Compile

```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf` (10 pages, ~550 KB).

## Cluster discipline

- Entry: 444 STABLE
- Exit: 444 STABLE
- Zero new arXiv IDs introduced
- Zero fabrications
- All references inherited from corpus cluster register

## Author

Kévin Rémondière (independent researcher, Oloron-Sainte-Marie, France).
ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166).
crossed-cosmos project (concept DOI [10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398)).
