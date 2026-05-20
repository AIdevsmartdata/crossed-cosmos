# Pre-submission checklist — Paper Lemma A3-2 (Path Beta)

Target venue: **Journal of Functional Analysis** (Elsevier)
Author: Kévin Rémondière (Oloron-Sainte-Marie, France)
ORCID: 0009-0008-2443-7166
Status: **submission-ready, Path Beta scope restricted**

---

## Scope and claim discipline

- [x] Title accurately reflects content (per-character spectral decomposition).
- [x] Abstract ~200 words, no over-claims.
- [x] Theorem 1.1 (a)–(d) is the *only* main result. No §8 "Route B mass-gap closure" claim.
- [x] Future work paragraph (`§9.2 What this paper does not claim`) explicitly defers the tentative Yang–Mills mass-gap consequence to separate work, with the three blocking sub-issues named (Karamata–Stirling at sketch level; Center-Rank companion paper; transport principle).
- [x] No `PROVED UNCONDITIONAL` headline that depends on open inputs.

## Mathematical correctness

- [x] Step 4 separates Sub-claim 4a (non-vanishing $L(\psi_\chi,1)\neq 0$, unconditional, Dirichlet 1839) from Sub-claim 4b (per-$\chi$ Selberg-type spectral gap, **not used in proof of Theorem 1.1**, only mentioned in Remark with explicit open-question caveat aligned with `Paper_ECI_Survey_Clay_BullAMS` Remark `selberg_downgrade` and `Paper_PRL_Theoreme_A_LMP` Remark `noSarnak`).
- [x] Sarnak 1983 bound stated as **$\lambda_1 \geq 21/25$ on specific arithmetic 3-manifolds** (matching the canonical published phrasing in the corpus survey paper). Universal applicability to every Bianchi orbifold flagged as **open question** per Remark `selberg_downgrade`.
- [x] No numerical inconsistency. The earlier draft's typo "$3/4 \approx 0.84876$" is gone (no specific numeric value is asserted in the body; only the Remark cites Sarnak's $21/25$ honestly).
- [x] All five steps individually proved.
- [x] Hypotheses table §6 lists every named input with its published-source status.
- [x] G1, G2, G3 gap accounting addressed.

## Citations and references

- [x] All references in `refs.bib` verified against the corpus cluster register (444 STABLE entry = exit).
- [x] **No new arXiv IDs introduced.** Only inherited references.
- [x] Sarnak 1983: doi 10.1007/BF02393209 (Acta Math 151:253–295). Verified ✓.
- [x] Kim 2003: doi 10.1090/S0894-0347-02-00410-1 (JAMS 16(1):139–183). Verified ✓.
- [x] EGM 1998: ISBN 978-3-540-62745-6 (Springer SMM). Verified ✓.
- [x] Bunke–Olbrich 1995: Akademie Verlag, Math. Research vol. 83. Verified ✓.
- [x] Gangolli–Warner 1980: Nagoya Math. J. 78:1–44. CrossRef ✓.
- [x] Cox 1989: Wiley, 2nd ed. 2013. Standard. ✓.
- [x] Davenport 2000 / Dirichlet 1839: classical, no DOI needed. ✓.
- [x] Neukirch 1999: Grundlehren 322. Standard. ✓.
- [x] Rudin FA Thm 13.24, Reed–Simon I VII.2: standard. ✓.
- [x] Internal unpublished `Remondiere2026Survey` and `Remondiere2026Faltings` flagged as internal-corpus references.

## LaTeX hygiene

- [x] Document class: `amsart` (J. Functional Analysis standard).
- [x] 10 pages compiled clean (after 1× pdflatex + 1× bibtex + 2× pdflatex).
- [x] No undefined control sequences in final compile.
- [x] No missing references in bibliography.
- [x] All theorems / propositions / lemmas / remarks consistently numbered through `[section]` counter.
- [x] All equation labels referenced.
- [x] Hyperref warnings limited to harmless `Token not allowed in a PDF string` (Unicode `\backslash` in section subscripts) — no broken links.

## Author and submission metadata

- [x] Author name: **Kévin Rémondière**, accents preserved.
- [x] Affiliation: independent researcher, Oloron-Sainte-Marie, France.
- [x] Email: kevin.remondiere@gmail.com.
- [x] ORCID 0009-0008-2443-7166 in `\thanks`.
- [x] crossed-cosmos project (concept DOI 10.5281/zenodo.19686398) acknowledged in `\thanks`.
- [x] MSC 2020 codes: Primary 11F72, 58J50; Secondary 11M36, 11R65, 22E40.
- [x] Keywords: 7 keywords listed.

## Sibling paper alignment

- [x] Sarnak 1983 attribution language **identical** to `Paper_ECI_Survey_Clay_BullAMS` and `Paper_PRL_Theoreme_A_LMP` (canonical $\lambda_1\geq 21/25$ on specific 3-manifolds, universal applicability open).
- [x] No contradiction with the K_ASP Mini retraction language.
- [x] Companion-paper references (`Remondiere2026Survey`, `Remondiere2026Faltings`) bibliographed.

## Falsifiables

- [x] Three explicit PARI/GP computational falsifiables F-1/2/3 at $D\in\{-15,-84,-420\}$.
- [x] Compute estimates given (~26 h Vast A100, ~$95 bundled).
- [x] Falsification criteria explicit and quantitative.

## Adversarial review resolution

- [x] Path Beta resolution noted in `ADVERSARIAL_REVIEW.md` appendix.
- [x] §8 Theorem 8.1 dropped; cleaned to a "future work" paragraph naming the three blocking issues.
- [x] All six revision points of the adversarial review (Step 4 attribution, numerical inconsistency, Theorem 8.1, per-χ transfer, Substep (ii) mechanism, CR theorem dependency) **addressed** by scope restriction.

## What to do at submission

1. Cover letter (`cover_letter.md`).
2. Submit to JFA (Elsevier) via Editorial Manager: https://www.editorialmanager.com/jfa/.
3. Anonymise if double-blind required (JFA is single-blind: no anonymisation needed).
4. Provide ORCID at submission.
5. Suggest 3 reviewers (optional): P. Sarnak (Princeton), J. Bergeron (UMons or related Bianchi-orbifold expert), N. Bergeron (Sorbonne or related cohomology of arithmetic 3-manifolds).

## Cluster discipline

- Entry: 444 STABLE
- Exit: 444 STABLE (no new arXiv IDs introduced, zero fabrications, all references inherited verified)
- Catches in adversarial review (Sarnak universal Bianchi attribution) addressed by scope restriction, not by absorbing the catch into the paper.

— Checklist complete. Paper is submission-ready.
