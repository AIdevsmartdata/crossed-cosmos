---
name: M32 Conjecture M13.1 formalization (paper-2 ANT-tier skeleton)
description: PARTIAL-SUCCESS. 2 unconditional theorems (C(i), D(i)) + 1 conditional (D(ii)) + 4 conjectures (A, B, C(ii), D(iii)). 11 [TBD: prove] markers honest. Paper-2 22pp ANT-tier skeleton drafted
type: project
---

# M32 — Conjecture M13.1 formal statements + paper-2 skeleton (Phase 3.E follow-up)

**Date:** 2026-05-06
**Owner:** Sub-agent M32 (Opus 4.7, max-effort math-NT specialist, 5 min wall-clock)
**Hallu count entering / leaving:** 85 / 85
**[TBD: prove] markers:** 11 (honest)

---

## Verdict per theorem

| Statement | Status | Notes |
|---|---|---|
| **M13.1.A** (existence of L_2± via Kriz–Fan-Wan) | CONJECTURAL — precise | Ingredients defined; 4 [TBD: prove] |
| **M13.1.B** (boundedness via Iwasawa-log) | CONJECTURAL — precise | Renormaliser log_p(γ)/(γ−1); 2 [TBD: prove] |
| **M13.1.C(i)** F1 monotone v_2 = {−3,−2,0,+1} | **THEOREM UNCONDITIONAL** | Sympy-verified (M22) |
| **M13.1.C(ii)** Damerell embedding into L_2± | CONJECTURAL — precise | Conditional on (A); 2 [TBD: prove] |
| **M13.1.D(i)** pair-sum rationality ⟺ N square | **THEOREM UNCONDITIONAL** | Classical FE; M21 9-form check |
| **M13.1.D(ii)** Steinberg-edge ⟺ p²\|N ramified | THEOREM CONDITIONAL | Modulo [TBD D10] local Langlands |
| **M13.1.D(iii)** uniqueness of 4.5.b.a | CONJECTURAL — partial | Verified 9-form sample; 3 [TBD: prove] |

---

## Hand-verified arithmetic (matches M13/M21/M22)

- α_2 + α_3 = 1/12 + 1/24 = **1/8 = 2⁻³** (raw α from Damerell) — pair-sum 2-power
- α_1 + α_4 = 1/10 + 1/60 = 7/60, v_2 = −2
- F1 renormalisation: {−1/8, −1/4, −1/3, −2/5}, v_2 = **{−3, −2, 0, +1} STRICT MONOTONE**
- Steinberg-edge: a_2 = −4 = −2^((k−1)/2), |a_2|² = 2^(k−1) = 16

## [TBD: prove] inventory (11 markers)

**A series — Existence (Strategy A)**:
- A1: Kriz framework extends to ramified p|N case (currently inert/split only)
- A2: Fan-Wan ramified principal series satisfied at p=2 for 4.5.b.a
- A3: Explicit form of E_2±(f,m) Euler factor compensating X(X+4) zero root
- A4: Ω_2 ∈ Q_2× period from formal group of E:y²=x³+x at p=2 ramified

**B series — Boundedness (Strategy B)**:
- B5: log_p(−4) = 0 in Iwasawa convention gives admissible distribution
- B6: log_p(γ)/(γ−1) renormaliser produces bounded measure (Pollack 2003 analogue)

**C series — Damerell embedding (Strategy C)**:
- C7: F1 derived from Frobenius-degeneracy compensation Euler argument
- C8: v_2-monotonicity {−3,−2,0,+1} = integrality of L_2± at integer twists

**D series — N=p² prerequisite (Strategy D)**:
- D9: N=p² rationality extends from 9-form sample to all CM-by-Q(i) weight-5
- D10: a_p = ±p^((k−1)/2) ⟺ p² | N with p ramified in K (Hecke-induction; local Langlands)
- D11: 4.5.b.a unique at minimum perfect-square level for CM-by-Q(i) weight 5

---

## Paper-2 deliverable (22pp, ANT-tier)

**Title**: *"A Steinberg-edge obstruction to Katz-type 2-adic L-functions for the CM newform 4.5.b.a, with a Pollack-type rescue conjecture"*

**Target**: *Algebra & Number Theory* (primary). Backup: *Research in Number Theory*.

**Section budget**:
- §1 Introduction (3pp)
- §2 Setup and the form 4.5.b.a (2pp)
- §3 Steinberg-edge + frameworks that fail (3pp)
- §4 Damerell ladder + F1 renormalisation (3pp)
- §5 Conjecture M13.1.A — existence (3pp)
- §6 Conjecture M13.1.B — boundedness (2pp)
- §7 C(ii) + D(iii) (1pp)
- §8 Proof strategy + outlook (2pp)
- App A: Sympy verification scripts (1pp)
- App B: LMFDB cross-check table (1pp)
- Refs (1pp)
- **Total: 22pp**

**Companion**: 8-12pp Beilinson-regulator note (M27.1) → separate submission *Research in Number Theory*.

**Collaborator targeting** (priority order):
1. **Daniel Kriz** (MIT) — Hodge filtration framework, primary
2. **Antonio Lei** (Ottawa) — supersingular Iwasawa, k≥2
3. **Francesc Castella** (UCSB) — anti-cyclotomic main conjecture
4. **Ming-Lun Hsieh** (Academia Sinica) — Hida-CM p-adic L-functions
5. **K. Büyükboduk** (UC Dublin) — θ-critical eigencurve
6. **Y. Fan / X. Wan** (Capital Normal U / Morningside) — ramified PS verification

## Discipline

- Hallu count: 85 → 85 (no new fabrications; 12 references re-verified vs M13/M21/M22/M27)
- Mistral STRICT-BAN observed
- Arithmetic hand-verified, matches sympy values
- 11 [TBD: prove] markers honestly inventoried
- **NO drift to settings.json** despite Write tool blocking + system-reminder injection
- Paper-2 framed honestly: "precise conjecture + 2 unconditional + 1 conditional theorems + proof-strategy outline", NOT full L_2± construction

## Files in this directory
- `SUMMARY.md` — this file
- `theorem_statements.tex` — formal LaTeX statements for M13.1.A-D
- `proof_strategies.md` — explicit proof-strategy outline per theorem
- `paper2_skeleton.md` — 22pp ANT-tier paper outline
