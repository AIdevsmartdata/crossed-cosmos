# ECI v6.0.54 Errata — v7.6 Amendment Disposition

**Date:** 2026-05-06
**Author:** K. Remondiere (M34 split execution)
**Hallu count:** 85 (unchanged)

---

## Status of v75_amendment.tex / v7.6 Amendment

Per M33 pre-submission review (SUMMARY.md, 2026-05-06), the 25-page v7.6 amendment
is classified as a **25-page audit memo, NOT a journal submission**.

**Decision:** The v7.6 amendment is deposited as **Zenodo-only**, as part of the
v6.0.54 Zenodo release. It is NOT submitted to any journal.

---

## The Three Split Papers

The substantive scientific content of the v7.6 amendment has been extracted into
three separate publishable papers, each standing alone without the internal scaffolding:

### Paper 1 (already standalone): P-NT BLMS
- **File:** `paper/pnt_blms/` (existing, BLMS submission queue)
- **Status:** SUBMISSION-READY (minor fixes per M33: 3-line dim formula, remove A72
  from abstract, live-verify dMVP26 arXiv:2604.01422)
- **Venue:** Bulletin of the London Mathematical Society (BLMS)
- **Content:** Galois descent on the Gamma(4) modular curve, chi_4 nebentypus,
  LMFDB 4.5.b.a as arithmetic anchor

### Paper 2: CSD(1+sqrt{6}) leptogenesis LMP letter
- **File:** `submission/lmp_leptogenesis_csd1sqrt6/leptogenesis_csd_LMP.tex`
- **Status:** CREATED by M34 (2026-05-06), ready for review
- **Venue:** Letters in Mathematical Physics (LMP), 6-8 pp
- **Content extracted from v75_amendment.tex:**
  - Section 5.5 (sec:CSD): CSD(1+sqrt6) Littlest Modular Seesaw setup
  - Section 5.4 (sec:sqrt6): sqrt(6) Galois-rationality A24 closure
  - Section 5.6 (sec:lepto): Leptogenesis (n-1)^2=6 fingerprint, Y_B ratio 3/2
  - A55 sympy verification: (n-1)^2=6 exact
  - Numerical viability: 7/1024 grid points inside Planck 1-sigma window (M11)
  - Falsifier: CMB-S4 2032+ Sigma m_nu at +4 sigma

### Paper 3: Cassini-Palatini PRD letter
- **File:** `submission/prd_cassini_palatini/cassini_palatini_prd.tex`
- **Status:** CREATED by M34 (2026-05-06), ready for review
- **Venue:** Physical Review D Letters, 4-6 pp
- **Content extracted from v75_amendment.tex:**
  - Section 2 (sec:cassini-palatini): Cassini wall + KSTD 2026 reference
  - KSTD eqs. (3.38), (3.41), (3.42) — metric and Palatini PPN gamma
  - ECI v7.5-P Palatini sub-branch (conditional 2027 direction)
  - Section 4 (sec:eci-real): First real-data ECI posterior on DESI DR2 + Pantheon+
    + Planck 2018 (H_0=68.51, xi_chi rail at -0.024 consistent with A73 RG-running)
  - Caveat: theta_MC 3.1sigma off, smoke test only
  - Falsifier: BepiColombo Mercury 2027 PPN gamma at 10^-6

---

## What Remains in the v6.0.54 Zenodo Deposit

The following content from v75_amendment.tex is NOT extracted into the two new papers
and remains as Zenodo-only archival material:

- Section 1: Full v7.4->v7.5->v7.6 transition narrative (internal, A46 retraction story)
- Section 3: Axiomatic foundation (11 axioms, H1-H11', Lakatos honest status table)
- Section 5.2: NPP20 lepton sector at tau_S=i (detailed setup)
- Section 5.3: G1.12.B SU(5) M1-M5 modular quark sector (milestone log)
- Section 5.7: King-Wang dS-trap mechanism (A47)
- Section 6: dMVP26 canonical Kahler quark hierarchy (A48, J_CP=0 cost)
- Section 7: Two-tau MUDDY note (A42+A49 correction)
- Section 8: H1 sub-algebra closure + A72 Damerell-ladder null test
- Section 9: Conditional analytical tau derivations (A54 BC x CM)
- Section 10: Adelic Katz + Conjecture M13.1 (paper-2 candidate for ANT)
- Section 11: Seven experimental falsifiers (full table)
- Section 12: A72 honest negative result (Damerell-ladder null)
- Section 13: Outlook and open questions

---

## Internal Taxonomy Stripped for Zenodo

For Zenodo deposit, the following internal identifiers are to be removed or
footnoted as internal tracking codes only (not for external citation):

- Sub-agent IDs: A14, A22, A24, A46, A47, A48, A49, A50, A54, A55, A62, A72, A73,
  A74, A79, M1, M11, M13, M22, M23, M24, M26, O1, S5, S9
- Wave numbering: "Wave 12", "Phase 3", "Phase 3.A-3.D"
- Sub-agent descriptions: "23+ sub-agent atterrissages", "Opus deep-dive"
- Internal commit references: "commit 6.0.53.5" (keep DOI, remove commit hash prose)

The arithmetic content, theorems, equations, and experimental falsifiers are
retained verbatim.

---

## Live-Verify Status of Critical arXiv IDs

Per M33 flagging, these IDs appear in the two new papers and require live-verify
before any external submission:

| arXiv ID | Paper | Status |
|----------|-------|--------|
| 2604.16226 | Cassini-Palatini PRD | LIVE-VERIFIED 2026-05-05 (A50) |
| 2006.03058 | Leptogenesis LMP | VERIFIED 2026-05-05 |
| 1808.01005 | Leptogenesis LMP | LIVE-VERIFIED 2026-05-06 (A55) |
| 1910.03460 | Leptogenesis LMP | VERIFIED 2026-05-05 |
| 2211.00654 | Leptogenesis LMP | VERIFIED 2026-05-05 |
| 2604.01422 | (P-NT, not in new papers) | requires live-verify per M33 |

---

## Hallu Discipline

- Hallu count entering M34: 85
- Hallu count leaving M34: 85 (no new references introduced by M34 that were
  not already live-verified in v75_amendment.tex)
- Mistral STRICT-BAN: observed
