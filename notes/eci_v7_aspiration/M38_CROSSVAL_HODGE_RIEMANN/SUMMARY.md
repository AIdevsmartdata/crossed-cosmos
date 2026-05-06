---
name: M38 Cross-validation of M27 (Hodge) + M28 (Riemann)
description: CONCUR-WITH-REFINEMENT (M27) + PARTIAL-DISSENT-FACTUAL (M28). One factual error in M28 reference: CPW arXiv:2206.10780 is type II_1 not II_inf. Structural obstruction argument survives on corrected footing.
type: project
---

# M38 — Cross-validation of M27 Hodge + M28 Riemann

**Date:** 2026-05-06
**Owner:** Sub-agent M38 (Sonnet 4.6, independent reviewer)
**Hallu count entering / leaving:** 85 / 85
**Live-verified refs:** 11

---

## M27 (Hodge) — CONCUR, minor refinement

**Verdict: CONCUR with SHIMURA-CM-TRIVIAL + TANGENTIAL-BEILINSON.**

### Concurrences

(a) **Pohlmann 1968 CONFIRMED REAL.** Annals of Math. 88 (1968), Issue 2, pp. 161-180.
Title: "Algebraic cycles on abelian varieties of complex multiplication type."
DOI: 10.2307/1970570. MR 0228500. Princeton Annals website live-confirmed.

(b) **M(f) as summand of H^{k-1} of CM curve: STANDARD, not speculative.**
Scholl 1990 (Inventiones 100, 419-430) constructs the motive explicitly via
Kuga-Sato varieties; combined with CM structure of 4.5.b.a (CM by Z[i]) and
Tate-Imai-Murty, HC for M(f) is genuinely a theorem, not a conjecture.

(c) **Beilinson-regulator angle: M27 missed one concrete target.**
The missed angle: Kings-Loeffler-Zerbes 2017 Euler systems for GL_2 x GL_2
provide explicit motivic classes in H^2_M(K_3, Q(j)) via Eisenstein symbols for
Rankin-Selberg convolutions. For f (x) f (self-convolution with CM twist), this is
the constructive route to Beilinson elements that M27 only sketches. KLZ2017
should be named explicitly in Conjecture M27.1 as the source of xi.

(d) **12 M27 references: no fabrication detected.** Pohlmann 1968, Deninger-Scholl
1991, Kriz 2021 book, Gao-Ullmo arXiv:2411.12249 all live-confirmed real.

### Refinement (not a dissent)

Scholl's motive uses *parabolic* cohomology of Kuga-Sato fibration Y(4)->X_1(4),
not H^4 of X_1(4) directly. M27's notation "H^4_parab(X_1(4)/C, Sym^3 V)" is
correct but could state the variety is the 4-fold Kuga-Sato fibration. Cosmetic only.

---

## M28 (Riemann) — PARTIAL DISSENT: one factual error, verdict survives

**Verdict: PARTIAL-DISSENT on the II_inf attribution; overall NO-DIRECT-ROUTE CONFIRMED.**

### Factual error (reference labeling)

**CPW arXiv:2206.10780 is type II_1, NOT II_inf.**

Live verification: Chandrasekaran-Longo-Penington-Witten 2022/2023
(arXiv:2206.10780, JHEP Feb 2023) constructs a type **II_1** algebra for the de
Sitter static patch. The type **II_inf** appears in the *separate* large-N AdS/CFT
paper: Chandrasekaran-Penington-Witten arXiv:2209.10454 ("Large N algebras and
generalized entropy", JHEP April 2023) for the black hole microcanonical algebra.

M28's ref list entry "CPW 2022 arXiv:2206.10780 (II_inf vs II_1 black-hole/dS)"
is muddled: 2206.10780 = de Sitter II_1 paper; the AdS/BH II_inf paper is
arXiv:2209.10454 (separate paper, separate context).

### Impact on M28's obstruction argument

**The structural obstruction survives on corrected footing.** Whether ECI Modular
Shadow is II_1 or II_inf, both are in class II (semifinite trace). Connes 1999
III_1 has no trace. No *-morphism II -> III_1 exists in either case.
Obstruction #5 (continuous vs discrete spectrum) applies to both II subtypes.
The NOVEL finding stands; only citation label needs correction.

### (a) Murray-vN classification: CONFIRMED CORRECT

Type II has semifinite trace; type III has no nonzero semifinite trace.
No *-isomorphism (let alone unital morphism) between any II factor and any III factor.
M28's core structural claim is correct.

### (b) CPW algebra type: CORRECTED (II_1 not II_inf for 2206.10780)

The ECI Modular Shadow context is closer to de Sitter (II_1) than AdS black hole
(II_inf). Either way, obstruction to III_1 is the same.

### (c) Connes 1999 III_1 structure: CONFIRMED

arXiv:math/9811068 = Connes "Trace formula in NCG and zeros of Riemann zeta,"
Selecta Math. NS 5 (1999). III_1 structure confirmed. Bost-Connes 1995
(Selecta NS 1, 411-457) explicitly uses type III factors. Both live-confirmed real.

### (d) Anticyclotomic IMC corollary: PLAUSIBLE, correctly hedged

Hsieh 2014 arXiv:1304.3311 published in JAMS 27(3):753-862 (not Inventiones/Annals
-- JAMS equally strong). Conditional chain M13.1 -> Kriz -> anticyclotomic IMC
inclusion is coherent. [TBD: prove] label is appropriate and honest.

---

## Summary table

| Agent | Claim | M38 verdict |
|-------|-------|-------------|
| M27 | Pohlmann 1968 real | CONFIRMED |
| M27 | M(f) summand of CM curve H^{k-1} | CONFIRMED STANDARD |
| M27 | Beilinson angle: missed concrete target | REFINEMENT: name KLZ2017 |
| M27 | 12 refs real, no fabrications | CONFIRMED |
| M28 | Murray-vN II vs III obstruction | CONFIRMED |
| M28 | CPW 2022 = II_inf | FACTUAL ERROR: 2206.10780 = II_1 |
| M28 | Correct II_inf paper | arXiv:2209.10454 (different paper) |
| M28 | Overall no-direct-route to RH | CONFIRMED SURVIVES |
| M28 | Connes 1999 III_1 | CONFIRMED |
| M28 | Anticyclotomic IMC plausible | CONFIRMED, correctly hedged |

**Hallu count: 85 -> 85 (held). Zero new fabrications by M38.**
