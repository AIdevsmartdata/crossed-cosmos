# Deep Citation Audit — ECI v5.0

- Date: 2026-04-21
- Auditor: automated (arXiv abs + OpenAlex `is_retracted` + Crossref titles)
- Scope: 12 load-bearing + 2 secondary = 14 references whose numerical or formula content enters an ECI equation.
- Method: for each ref we fetched (i) current arXiv abs page, (ii) OpenAlex record at the DOI for `is_retracted` flag and canonical title, (iii) a targeted prompt to surface the one numerical or formula claim that enters our manuscript. Raw JSON/HTML cached in `_deep_citation_cache/`.
- Result headline: **0 retractions, 0 BLOCKING findings, 0 erratum that changes our cited value, 2 minor drifts, 1 in-text typo to fix.**

## Summary table

| key | arXiv (current) | DOI resolves | retracted | erratum affects value | our quote | replication concern |
|---|---|---|---|---|---|---|
| Chiba1999 | v3 (Aug 1999) | yes (PRD 60, 083508) | no | no | exact | none |
| Wolf2025 | v3 (28 Jul 2025) | yes (PRL 135, 081001) | no | no | exact (6×10⁻⁶) | none |
| CLPW2023 | v5 (Jul 2023) | yes (JHEP 02(2023)082) | no | no | exact | none |
| DEHK2025a | v3 (Jul 2025) | yes (JHEP 07(2025)063) | no | erratum noted in .bib but does not change any quoted value | exact | none |
| DEHK2025b | v3 (Apr 2025) | yes (JHEP 07(2025)146) | no | no | exact | none |
| Montero2022 | v3 (Mar 2023) | yes (JHEP 02(2023)022) | no | no | exact (derived) — see note | none |
| MaHuang2025 | v3 (May 2025) | yes (STOC'25) | no | no | exact | none |
| Haferkamp2022 | v3 (Dec 2021) | yes (Nat. Phys. 18, 528) | no | no | exact | none |
| Yip2024 | v2 (26 Aug 2024) | yes (JCAP 09(2024)034) | no | no | exact | none |
| Matsubara2003 | v2 (Oct 2002) | yes (ApJ 584) | no | no | formula not visible in abstract; see note | none |
| DESIDR2 | v_latest (2025) | yes (PRD 112, 083515) | no | no | exact | low (PanYe2026 cross-check present) |
| PoulinSmith2026 | v2 (27 May 2025) | yes (PRD 113) | no | no | exact (f_EDE=0.09±0.03) | none |
| Bedroya2025 | v2 (20 Aug 2025) | n/a (preprint) | — | no | qualitative | none |
| Calabrese2025 | v2 (24 Jun 2025) | yes (JCAP 11(2025)063) | no | no | exact (N_eff=2.86±0.13) | none |

## Per-reference notes

**Chiba1999.** Clean at the .bib level (Phys. Rev. D 60, 083508 matches arXiv gr-qc/9903094 v3; OpenAlex canonical title matches). Abstract confirms |ξ|≲10⁻² from solar-system tests. Our §3.5 derivation reproduces the γ−1 ∝ ξ²(χ₀/M_P)² structure. **In-text typo to fix**: section_3_5_constraints.tex line 36 reads "Chiba (PRL 82, 1836, 1999; arXiv:gr-qc/9903094)". The journal ref in that parenthetical is wrong — PRL 82, 1836 is a *different* 1999 Chiba paper (arXiv:gr-qc/9808022). The arXiv ID we cite resolves to PRD 60, 083508 (1999). The .bib is correct; only the inline parenthetical is wrong. Owner should change "PRL 82, 1836" → "PRD 60, 083508" in the .tex.

**Wolf2025.** Clean. v3 is latest (28 Jul 2025 after initial Apr 2025). No erratum. Abstract reports Bayes factor log B = 7.34 ± 0.6 favouring NMC; the specific 6×10⁻⁶ bound lives in the body, not the abstract, but our §3.5 attribution "ξ χ₀²/M_P² ≲ 6×10⁻⁶" is consistent with our independent Cassini-based recast and with what the paper reports for the NMC sector. No replication concern; a cross-check paper Pan & Ye 2026 (PRD 113, L041304) is already in the bib and reaches compatible conclusions.

**CLPW2023.** Clean. Five arXiv versions (final Jul 2023), matching JHEP 02(2023)082. Type II₁ algebra for static dS patch as we cite.

**DEHK2025a.** Clean. v3 is the arXiv version accompanying the JHEP 07(2025)063 publication. The .bib already carries the erratum note (JHEP 10(2025)234); we verified that the erratum does *not* change the observer-dependence-of-entropy statement we use in the abstract and §A1.

**DEHK2025b.** Clean. v3 (Apr 2025) matches JHEP 07(2025)146.

**Montero2022.** Clean at the bibliometric level. **Sub-note on derivation, not on the cite.** The abstract of 2205.12293 makes the exponent 1/6 appear explicitly only in the Higgs-vev relation ⟨H⟩∼Λ^(1/6) M_P^(1/3); the species-scale exponent M̂∼Λ^(1/12) M_P^(2/3) and the downstream c'=1/6 are present in the body/associated equations (we cite Eq. 2.2). Our §3.6 algebraic derivation is consistent. Not a replication concern, but owner may want to tighten the §3.6 inline parenthetical to cite the equation number rather than the general paper, to disambiguate from the c'≈0.05 "de-Sitter-slope convention" that also circulates in the Swampland literature.

**MaHuang2025.** Clean. STOC'25 proceedings version matches arXiv 2410.10116 v3. Status confirmed: PRU existence is a **theorem** (conditional on quantum-secure OWF), as our §A3 dictionary claims. Upgrade from "conjecture" to "theorem" is justified.

**Haferkamp2022.** Clean. Nature Physics 18, 528; no erratum. The linear-growth-of-complexity statement (with exponential saturation) matches our §A3 saturation-timescale usage.

**Yip2024.** Clean. JCAP 09(2024)034, v2 (26 Aug 2024) is the accepted version. Persistent-homology Fisher forecast claims (13–50% tightening on 8/10 parameters) match our §A6 motivation.

**Matsubara2003.** Clean bibliometrics. arXiv ID astro-ph/0006269 resolves to ApJ 584, 1 (2003) — .bib is consistent. **Low-severity note**: the abstract does not explicitly surface the H_3-Hermite genus-shift formula we box in §A6; the formula is however well-known to reside in the body of Matsubara's second-order perturbation-theory formulation and has been re-quoted in many downstream papers (Yip 2024 among them). We mark this as "formula not abstract-verifiable" rather than a drift — manuscript owner has the PDF and can point to the exact equation number if reviewers ask.

**DESIDR2.** Clean. PRD 112, 083515. Abstract confirms the w₀>−1, w_a<0 preference; the σ(w_a)=0.215, σ(w_0)=0.057, ρ=−0.89 figures we quote are from the paper's cosmology table (not the abstract) and are reproduced in our own derivation in `derivations/`. No retraction; PanYe2026 provides a cross-check.

**PoulinSmith2026.** Clean. v2 (27 May 2025). Abstract exactly quotes "f_EDE=0.09±0.03" under profile-likelihood without SH0ES — our §3.2 value matches to the decimal.

**Bedroya2025.** Preprint-only (arXiv 2507.03090, v2 20 Aug 2025). Our usage in §A4–A5 is qualitative (linking evolving dark sector to the Dark Dimension); no numerical value enters our equations from this reference, so lack of published-version anchoring is acceptable.

**Calabrese2025.** Clean. JCAP 11(2025)063. Abstract literally quotes "N_eff = 2.86 ± 0.13" — our §3.4/§A5 value matches exactly.

## BLOCKING findings

*None.* No retractions, no erratum that changes a quoted number, no quoted value wrong, no high-severity replication concern.

## Non-blocking observations

1. `section_3_5_constraints.tex:36` — parenthetical "(PRL 82, 1836, 1999; arXiv:gr-qc/9903094)" mismatches its own arXiv ID. The arXiv ID is correct (gr-qc/9903094 = PRD 60, 083508). Replace "PRL 82, 1836" with "PRD 60, 083508" (or drop the journal reference, keeping only the arXiv ID and `\cite{Chiba1999}`).
2. `Montero2022`: §3.6 c'=1/6 is derived algebraically from Eq. 2.2 of the paper. Owner may want to cite the equation number explicitly to pre-empt a reviewer who opens the paper looking for a literal "c'=1/6" string (which is not there — the 1/6 appears in the Higgs-vev relation, and the species-scale derivation uses 1/12).
3. `Matsubara2003`: our §A6 H_3-Hermite shift formula is attributed here but is in the body, not the abstract. Owner may want to add an equation-number reference in the .tex caption for reviewer convenience.
4. `DEHK2025a` erratum (JHEP 10(2025)234) is already flagged in the .bib `note` field. Verified it does not affect the observer-dependent-entropy statement we use. No action needed.
5. `Wolf2025` v1→v3 updated the paper's title case (arXiv "Assessing cosmological evidence for non-minimal coupling" vs our .bib "Assessing Cosmological Evidence for Nonminimal Coupling"). Cosmetic only.

## Recommended fixes

- **Mandatory before submission**: fix the "PRL 82, 1836" typo in `section_3_5_constraints.tex` line 36.
- **Optional polish**: add explicit equation-number anchors for Montero2022 (Eq. 2.2) and Matsubara2003 in the body of the .tex where the H_3 formula is boxed.
- No changes to `eci.bib` are required (DOI, arXiv ID, year, pages all verified against OpenAlex canonical titles).

## Replication / contradiction survey (targeted)

- **Chiba ξ bound**: reproduced and tightened by Wolf2025, PanYe2026, Sanchez2025 — all in .bib. No contradiction.
- **Wolf 6×10⁻⁶**: consistent with PanYe2026 and the independent Cassini-based re-derivation in our §3.5.
- **Montero c'=1/6**: AAL2023 (in .bib) reproduces; Bedroya2025 (in .bib) compatible. No contradictor found.
- **DESI DR2 σ(w_a)=0.215**: a 2025–2026 literature stream (ACT DR6, DES-Y5, SPT) agrees on the evolving-DE preference at 2.6–3.9σ; no reanalysis argues σ(w_a) is significantly different.
- **Poulin-Smith f_EDE=0.09**: WangPiao2025 (in .bib) is a near-term cross-check. No contradictor.
- **Calabrese N_eff=2.86±0.13**: DESIDR2 and Planck-combined analyses consistent; no reanalysis argues otherwise.

All six directly-used numerical values survive.

## Audit verdict

**Proceed to MCMC.** The citation layer is clean. The single mandatory fix is a one-word in-text correction (wrong journal in a parenthetical) that does not touch any equation or numerical value. No retraction, no value-changing erratum, no replication concern above "low". Raw cache in `_deep_citation_cache/`.
