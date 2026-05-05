# arXiv Submission Checklist — P-NT Paper

**Paper:** "Two LMFDB identifications for hatted weight-5 multiplets of the metaplectic cover S'_4"
**Author:** Kévin Remondière
**Source TeX:** `/root/crossed-cosmos/notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.tex` (884 lines, last modified 2026-05-05)
**Compiled PDF:** `/root/crossed-cosmos/notes/eci_v7_aspiration/PNT/paper_lmfdb_s4prime.pdf` (11 pages, 406 514 bytes, RC=0)
**Prepared by:** A67 (Sonnet sub-agent), 2026-05-05
**Hallu count:** 85 entering, 85 leaving (no fabrications introduced or detected)

---

## Step-by-step on arxiv.org

### 1. Login and "Start New Submission"

URL: <https://arxiv.org/submit>
Login with your registered arXiv account (kevin.remondiere@gmail.com or whichever
address is associated). If you are not yet registered, go to
<https://arxiv.org/user/register> first — registration takes ~5 minutes and is
independent from endorsement.

### 2. License selection

Choose: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
This matches the Zenodo-archived ECI repository licensing and allows
unrestricted reuse by LMFDB, PCG, Templeton reviewers.

### 3. Primary subject class

**Primary:** `math.NT` (Number Theory)

**Cross-listings (in order):**
1. `math.RT` (Representation Theory) — for the metaplectic cover S'_4 group structure
2. `hep-ph` (Phenomenology) — for the modular flavour symmetry application context
3. `hep-th` (Theory) — for the metaplectic / CFT-adjacent framing

(arXiv permits up to 4 cross-listings; use all four.)

### 4. Title (paste verbatim)

```
Two LMFDB identifications for hatted weight-5 multiplets of the metaplectic cover S'_4
```

### 5. Authors

```
Kévin Remondière
```

Affiliation field: `Independent Researcher, Tarbes, France`

(arXiv displays affiliation in author-block as "K. Remondière (Independent Researcher, Tarbes, France)".)

### 6. Abstract

Paste the contents of `arxiv_abstract.txt` (sibling file in this directory).
The abstract is plain-text (no LaTeX commands except minimal math), 1543 chars,
within arXiv's 1920-char limit.

### 7. Comments line (optional but recommended)

```
11 pages, 3 tables, amsart class. Computations performed in sympy 1.12.
LMFDB labels and arXiv references live-verified 2026-05-05.
Submission target: Bull. Lond. Math. Soc.
Audit trail: Zenodo doi:10.5281/zenodo.20034969 (concept doi:10.5281/zenodo.19686398).
```

### 8. MSC2020 classification

**Primary:** `11F11` — Holomorphic modular forms of integral weight

**Secondary:**
- `11F25` — Hecke-Petersson operators, differential operators (one variable)
- `11F30` — Fourier coefficients of automorphic forms
- (Optional, if a 4th slot is available: `11F22` for relationships to Lie algebras and finite simple groups, since S'_4 is a finite metaplectic cover)

(The paper's `\subjclass[2020]` line already declares `Primary: 11F11; Secondary: 11F25, 11F30` — match this exactly.)

### 9. Journal-ref / report-no fields

Leave **journal-ref blank** (paper has not yet been accepted at BLMS).
Leave **report-no blank** (no institutional report number).

### 10. DOI field

Leave **DOI blank**. The Zenodo audit-trail DOI is mentioned in the
Comments line and Acknowledgements; arXiv's DOI field is reserved
for the journal DOI once accepted.

### 11. ACM-class field

Skip (not applicable to math.NT).

### 12. Upload tarball

See `tarball_contents.md` for the exact file list and packaging instructions.

### 13. Preview the AutoTeX compile

arXiv's autoTeX will recompile from source. Verify:
- Page count: 11 pp
- No font-substitution warnings (Computer Modern is bundled)
- Hyperref URLs in §3.1 (LMFDB) and Acknowledgements remain clickable
- Table 1 (in §4.3) renders intact
- The abstract block renders without overflow

### 14. Endorsement check

Before submission, verify your endorsement status for `math.NT`. Go to:
<https://arxiv.org/auth/show-endorsers>

If endorsed: proceed to submit.
If NOT endorsed: see `endorsement_targets.md` for candidate endorsers
and the request workflow.

### 15. Submit

Click "Submit" once preview compiles cleanly. arXiv will send a confirmation
email within minutes. The paper enters the daily processing queue and
typically appears as `arXiv:YYMM.NNNNN` within 24–48 hours
(US business days; weekends delay).

---

## Post-submission

- The arXiv ID will be `arXiv:2605.NNNNN` (May 2026 series).
- Update the BLMS cover letter (`/root/crossed-cosmos/notes/eci_v7_aspiration/PNT/cover_letter_blms.md`)
  to reference this arXiv ID once assigned.
- Update the companion paper bibitem (`V2_no_go`) in the .tex once V2
  is also on arXiv; submit a v2 replacement to arXiv at that time.
- Update `/root/.claude/projects/-root/memory/project_crossed_cosmos.md`
  to record the arXiv ID and submission timestamp.

---

## Known minor blockers (none preventing submission this week)

| # | Item | Severity | Action |
|---|------|----------|--------|
| 1 | One cosmetic 1.29 pt overfull hbox at the LMFDB URL line 370 | very low | Acceptable; amsart norms |
| 2 | `V2_no_go` bibitem cites "in preparation" without arXiv ID | low | Submit V2 in parallel or update P-NT v2 once V2 lands |
| 3 | Zenodo DOI 20034969 is v6.0.53.1; if v6.0.53.3 (20036808) is now public, optionally update §6 acknowledgements | low | Confirm with Kevin; no impact on math content |
