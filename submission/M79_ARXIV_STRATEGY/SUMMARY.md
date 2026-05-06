---
name: M79 arXiv submission strategy — 13-paper portfolio
description: Submission sequencing, endorser priorities, risk assessment. Hallu 91 held.
type: project
---

# M79 — arXiv Submission Strategy (2026-05-06)

**Owner:** Sub-agent M79 (Sonnet 4.6)
**Hallu count:** 91 → 91 (held; 0 fabrications)
**Builds on:** M41_FINALIZE (8-paper strategy), M45 (Bianchi IX), M70 (R-2 BK), M71 (R3-C-1)

---

## 1. Submission sequencing — 13 papers

Priority: (a) fewest blockers, (b) endorser accessibility, (c) citation dependency
(P1 before R-2; P1 before R3-C-1), (d) risk profile.

| Wave | # | Paper | Cat | Status | Blocker |
|------|---|-------|-----|--------|---------|
| W1 | P5 | Leptogenesis CSD LMP | hep-ph | READY | none |
| W1 | P6 | Cassini-Palatini PRD | gr-qc | READY | 1-sentence xi_chi note |
| W2 | P1 | P-NT BLMS | math.NT | minor fix | Cohen-Oesterle 3 lines + rm A72 from abstract |
| W2 | P2 | ER=EPR LMP | hep-th | minor fix | Prop 1 spectral-measure paragraph |
| W3 | P4 | Cardy LMP | cond-mat/hep-th | minor fix | Thm 2 Virasoro 2-para + polariton check |
| W3 | P3 | Modular Shadow v2.5 | hep-th/math-ph | fix+recompile | App A.2 + BEC caveat + 5-ID arXiv verify |
| W3 | M58 | m_bb LMP | hep-ph | assess | King same endorser as P5/P7; stagger 2 wks |
| W4 | P7 | Proton-decay PRD | hep-ph | mandatory rev | 4 fixes: affiliation, author, B-ratio, fine-tuning |
| W4 | R-6 | Lemniscate dichotomy | math.NT | assess | wait for P1 arXiv post (credibility) |
| W5 | R-2 | BK Tamagawa M70 | math.NT | NEEDS-DEEPER | 5 TBD markers; ~10-15% formal contribution |
| W5 | R3-C-1 | Geom. Langlands mini M71 | math.AG | SPECULATIVE | 30-40% conjecture; Stage 2 check needed |
| W6 | #9 | v7.6 amendment paper-2 | math.NT | future | 11 TBD; Q3 2026 target |
| GATED | Bianchi IX M45 | math-ph/gr-qc | BLOCKED | W3 gate: sec4.1 detail + F1 numerics first |

GLOBAL pre-submit gate: verify 10 future-dated IDs from M33:
  2602.02675  2603.01664  2604.02075  2604.11277  2604.01275
  2604.16226  2604.01422  2604.13854  2604.08449  2603.18502

---

## 2. Endorser map

| Cat | Endorser | Papers | Risk |
|-----|----------|--------|------|
| math.NT | Andrew Booker (Bristol) | P1, R-6, #9 | LOW-MED |
| math.NT | Tim Browning (IST Austria) | P1 backup, R-2 backup | LOW-MED |
| hep-ph | Steve King (Southampton) | P5, P7, M58 | LOW |
| gr-qc | Thomas Sotiriou (Nottingham) | P6 | LOW |
| hep-th | Nima Lashkari (Purdue) | P2, P3 (stagger 2 wks) | MED |
| cond-mat | Pasquale Calabrese (SISSA) | P4 | MED |
| math-ph | Matilde Marcolli (Caltech) | Bianchi IX | HIGH — gated W3 |
| math.NT | Daniel Kriz (MIT) | R-2 (collab ask) | HIGH |
| math.AG | Loeffler (Warwick) + Zerbes (UCL) | R3-C-1 | HIGH |

Contacts used from M41/M45 prior agents + public institutional directories:
  Booker: andrew.booker@bristol.ac.uk
  King: S.F.King@soton.ac.uk
  Sotiriou: Thomas.Sotiriou@nottingham.ac.uk
  Lashkari: nlashkari@purdue.edu
  Calabrese: calabrese@sissa.it
  Marcolli: matilde@caltech.edu
Verify currency before sending. Kriz/Loeffler/Zerbes: use MIT/Warwick/UCL directories.

---

## 3. Risk tiers

| Tier | Papers |
|------|--------|
| LOW (submit W1) | P5, P6 |
| LOW-MED (W2) | P1, P2 |
| MED (W3) | P3, P4 |
| GATED (W4) | P7, M58, R-6 |
| NEEDS-DEEPER (W5) | R-2 (honest: 10-15%) |
| SPECULATIVE (W5) | R3-C-1 (honest: 30-40%) |
| BLOCKED | Bianchi IX (W3 gate: sec4.1 + F1 numerics) |

Mistral STRICT-BAN observed. 0 fabrications. Hallu 91 held.
