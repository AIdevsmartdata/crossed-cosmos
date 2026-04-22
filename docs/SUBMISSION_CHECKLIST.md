# EPJ C submission checklist — tick off before clicking "Submit"

Pre-press checklist the repository owner works through immediately before
uploading the v5.0 submission to the EPJ C Editorial Manager.

## Release plumbing

- [ ] `v5.0.0` tag has been cut and pushed (`git tag v5.0.0 && git push --tags`).
- [ ] Zenodo DOI for v5.0 has been minted — check
      <https://zenodo.org/account/settings/github/> that the
      `AIdevsmartdata/crossed-cosmos` → Zenodo integration fired and returned
      a concrete `10.5281/zenodo.XXXXXXX` ID.
- [ ] The new Zenodo DOI is referenced in the cover letter (alongside, not
      replacing, the existing `10.5281/zenodo.19686399` which remains the v4
      archive).
- [ ] `CITATION.cff` at the repo root points at the v5.0 DOI.

## Manuscript build

- [ ] `eci_svjour3.pdf` compiles with **0 undefined references** — rerun
      `latexmk -pdf -interaction=nonstopmode eci_svjour3.tex` inside
      `submission/epjc/` and confirm the `.log` is clean.
- [ ] BibTeX produces 0 warnings (no orphan entries, no missing citations).
- [ ] Cover letter has **today's date** substituted in —
      `sed -i "s/\\\\today/$(date +'%B %-d, %Y')/" submission/epjc/cover_letter.tex`
      then recompile.
- [ ] `eci_svjour3.pdf` and `cover_letter.pdf` are the most recent builds
      (mtimes newer than the tex sources).
- [ ] Author list, ORCID, and affiliation ("Independent Researcher") are
      identical in the manuscript title block, the cover letter, and the
      Editorial Manager metadata form.

## Editorial content

- [ ] `submission/epjc/suggested_referees.md` lists 5 names, all currently
      reachable at the stated institution (last verified within 30 days).
- [ ] `docs/AUTHOR_STATUS.md` is included as a metadata note or pasted into
      the EM "Comments to the Editor" box.
- [ ] `AI_USE.md` is referenced from the cover letter (per journal
      transparency policy).
- [ ] §5 (A3 toy dictionary) is still quarantined to Appendix A and the
      abstract matches the body on A3's "working conjecture" status.
- [ ] The MCMC $\xi_\chi$ posterior numbers in §3.5 / §4 row 1b match the
      actual chain outputs; no forecast-era placeholder remains.

## Reproducibility bundle

- [ ] MCMC chains tarball (`.tar.zst`, chains + `.paramnames` + `input.yaml`
      + `getdist` summary) has been uploaded to the v5.0 Zenodo record as
      supplementary material.
- [ ] `mcmc/nmc_patch/hi_class_nmc/` builds cleanly from a fresh clone
      against upstream hi_class_public 50f447c.
- [ ] `mcmc/cobaya-nmc/` Python theory plugin imports without error on a
      vanilla Python 3.12 + classy + cobaya environment.

## Review artefacts

- [ ] `paper/_adversarial_review_v5_0_0.md` exists (V12 adversarial pass on
      the MCMC-integrated manuscript).
- [ ] `paper/_internal_rag/INDEX.md`, `DECISIONS.md`, `GROUND_TRUTH.md`, and
      `PRINCIPLES.md` are synced with the final v5.0 content.

## The click

- [ ] Submission type: "Regular Article".
- [ ] Section: "Theoretical Physics" (or the editor-assigned section).
- [ ] Competing interests declaration: none.
- [ ] Funding declaration: none.
- [ ] ORCID linked on the Editorial Manager profile.
- [ ] Final zip uploaded: `eci_svjour3.tex`, `eci.bib`, all `section_*.tex`
      and figure files, `cover_letter.pdf`, svjour3 `_vendor/` bundle,
      `AI_USE.md`, `docs/AUTHOR_STATUS.md`.
- [ ] Confirmation email from EM received and archived.
