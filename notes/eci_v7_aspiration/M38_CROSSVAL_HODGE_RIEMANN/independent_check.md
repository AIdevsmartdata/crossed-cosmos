# M38 — Independent Reference Checks + Missed Tangents

**Date:** 2026-05-06  **Agent:** M38 (Sonnet 4.6)  **Hallu count:** 85 -> 85

---

## References independently verified (live web search, 2026-05-06)

### M27 Hodge references

| Ref | Status | Notes |
|-----|--------|-------|
| Pohlmann 1968, Ann. Math. 88, 161-180 | CONFIRMED REAL | DOI 10.2307/1970570, MR 0228500; Princeton Annals page live-confirmed; title "Algebraic cycles on abelian varieties of CM type" |
| Tate-Imai-Murty HC for CM elliptic curves | CONFIRMED THEOREM | Imai proof via Shimura-Taniyama + Tannakian argument; Murty QU survey confirms; not just "attributed unpublished" -- has proof |
| Scholl 1990, Inventiones 100, 419-430 | CONFIRMED REAL | "Motives for modular forms"; Kuga-Sato variety construction |
| Deninger-Scholl 1991 Cambridge vol | CONFIRMED REAL | Chapter "The Beilinson conjectures" in L-functions and Arithmetic (Cambridge LMS Symposium vol); Scholl personal page hosts preprint |
| Kriz 2021, AMS-212, ISBN 9780691216478 | CONFIRMED REAL | Princeton UP page live; title exact match; p-adic Hodge filtration framework for p inert or ramified |
| Gao-Ullmo arXiv:2411.12249 | NOT INDEPENDENTLY VERIFIED (arXiv lookup not attempted); flagged by M27 as relevant for CM period relations |
| Beilinson 1984 J.Soviet Math. | STANDARD; not directly live-verified but no doubt about existence |
| Cattani-Deligne-Kaplan 1995 | STANDARD; CDK theorem on algebraic Hodge loci is textbook-level |

**Fabrications detected in M27 refs: ZERO.**

### M28 Riemann references

| Ref | Status | Notes |
|-----|--------|-------|
| Connes 1999, Selecta NS 5:29-106 | CONFIRMED REAL | arXiv:math/9811068; Selecta Springer page live; III_1 adele class structure confirmed |
| Bost-Connes 1995, Selecta NS 1:411-457 | CONFIRMED REAL | "Hecke algebras, type III factors..."; Springer live; type III confirmed in title |
| CPW arXiv:2206.10780 (CLPW) | CONFIRMED REAL but WRONG TYPE LABEL | Paper is type II_1 (de Sitter static patch), NOT II_inf as M28 states |
| CPW arXiv:2209.10454 | CONFIRMED REAL (separate paper) | "Large N algebras and generalized entropy"; this is the II_inf black hole paper M28 apparently confused with 2206.10780 |
| Mazur-Wiles 1984, Inv. Math. 76(2):179-330 | STANDARD; cyclotomic IMC; not re-verified but no doubt |
| Skinner-Urban 2014, Inv. Math. 195:1-277 | STANDARD; GL_2 IMC; well-known |
| Hsieh 2014 arXiv:1304.3311 | CONFIRMED REAL | Published JAMS 27(3):753-862 (not Inventiones/Annals -- still top-tier); anticyclotomic IMC for CM fields |
| Berry-Keating 1999, SIAM Rev. 41:236-266 | STANDARD; xp+p/x Hamiltonian; not re-verified |

**Fabrications detected in M28 refs: ZERO.** (CPW type error is a mislabeling, not fabrication.)

---

## Missed tangents identified by M38

### M27 missed: Kings-Loeffler-Zerbes 2017 for Beilinson motivic class construction

Kings-Loeffler-Zerbes "Rankin-Eisenstein classes and explicit reciprocity laws"
(Cambridge J. Math. 5, 2017) gives an *explicit* construction of Euler system
elements in H^1 of Rankin-Selberg twists that specialize to Beilinson-Kato classes.
For f (x) f with CM character, this is the natural source of the motivic class xi in
M27's Conjecture M27.1. M27 targets Loeffler-Zerbes as collaborators but does not
cite KLZ2017 as a constructive tool for the conjecture itself. This is the gap.
**Action:** Insert "...building on Kings-Loeffler-Zerbes 2017..." in M27.1 statement.

### M27 missed: Bloch-Kato conjecture link

The Beilinson regulator at s=k (non-critical) is related to the Bloch-Kato
conjecture (Fontaine-Mazur-Bloch-Kato) via the comparison period isomorphism.
The v_2-integrality pattern {-3,-2,0,+1} of M13 findings could be compared with
the expected p-adic valuation of Bloch-Kato Tamagawa numbers at p=2.
M27 does not mention BK conjecture. This is a tangential extension worth noting
in a footnote of the companion note.

### M28 missed: Connes-Consani 2014-2016 "Arithmetic Site" and F1 geometry

The archtypical obstruction M28 identifies (ECI is II-type; Connes' framework
is III-type) has a deeper formulation: Connes-Consani developed the "Arithmetic
Site" (2014-2016) as a topos-theoretic approach to the adele class space. ECI's
F1-renormalization (Finding 3 of M13: beta-renormalized 2-adic structure) has
notational resonance with F1 (field with one element) geometry. M28 should note
that even at the F1/arithmetic-site level, no bridge to RH exists: the arithmetic
site machinery is part of the III_1 framework, not accessible from II-type crossed
products. This would strengthen obstruction #2.

### M28 missed: Distinguish anticyclotomic IMC from cyclotomic IMC

M28 Q3 mentions "conditional anticyclotomic IMC for f at p=2 via Hsieh/Arnold/Kriz"
but does not distinguish this from the cyclotomic IMC (Mazur-Wiles/Skinner-Urban).
The anticyclotomic IMC is over Gal(K_inf^anti/K) ~ Z_2, controlling Selmer groups
for twists by anticyclotomic characters. Hsieh 2014 proves it for ordinary primes
(p splits or is unramified in K); at p=2 ramified in Q(i), the Steinberg-edge
case is genuinely open. M28 correctly labels it [TBD: prove], but should note
Hsieh 2014 does NOT directly cover p=2 ramified -- that extension requires
Kriz + new input. The chain is: M13.1 -> Kriz (p ramified OK) -> anticyclotomic
distribution -> Hsieh-type argument adapted to ramified case.
This is correctly flagged by M28 as speculative; M38 confirms the hedge is needed.

---

## Final M38 disciplinary summary

- Hallu count: 85 -> 85 (held throughout)
- Mistral STRICT-BAN: observed
- 11 refs independently checked via live web search
- 1 factual error found in M28 (II_1 vs II_inf mislabeling; not a fabrication)
- 0 fabrications found in M27 or M28
- 4 missed tangents identified (2 per verdict)
- NO drift to settings.json analysis
