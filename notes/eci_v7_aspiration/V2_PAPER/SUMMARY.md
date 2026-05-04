# V2_PAPER — Status and remaining tasks

**Date**: 2026-05-04

## What is done

Full draft written as `v2_no_go_paper.tex` (plain article, ~487 lines).

Sections:
- Abstract: bound sin theta_C <= 0.005, convention-independence, two-tau escape.
- Sec 1 Setup: LYD20 Model VI assignments (TeX lines 1372-1390), M_u and M_d.
- Sec 2 S-fixed-point lemma: Lemma proven (S acts as i^k on weight-k forms at tau=i).
- Sec 3 Collinearity: Theorem 2, near-rank-1 {d,s}-block, ratios from code comments.
- Sec 4 Cabibbo suppression: Theorem 3 (sin theta_C <= 0.005), phase-factoring proof,
  MC paragraph citing I2_corrected.py (5000-sample) + v2_audit.py (independent).
- Sec 5 Convention independence: reversed Q, CC forms, right-SVD CKM.
- Sec 6 Implications: scope, two-tau escape arXiv:2209.08796 / 2212.10666, open question.
- References: 6 refs with anti-hallucination inline flags.

## Remaining before submission (critical)

1. RUN v2_audit.py: get exact values for eqs (6)-(7):
   Y3/Y1, Y2/Y1, Y5_5/Y5_3, Y5_4/Y5_3 at tau=i; exact epsilon; best sin theta_C.

2. VERIFY arXiv IDs live:
   - 2002.03817 (NPP20), 1706.08749 (Feruglio): check.
   - dMVP26: PLACEHOLDER — arXiv ID unknown, must find.
   - 2209.08796 (TanYam22), 2212.10666 (DingTwo22): check.

3. VERIFY Delta = D_u† D_d in Sec 4 (b^c phase depends on Y5 multiplet mix).

4. CONVERT to journal style (JHEP: jheppub.sty; PRD: revtex4-2).

## Target venue

| Venue | Format |
|-------|--------|
| JHEP | Short letter 4-6 pp — recommended |
| PRD | Comment/Brief report (same journal as LYD20 PRD 103) |
| arXiv math-ph | Preprint alongside journal submission |
