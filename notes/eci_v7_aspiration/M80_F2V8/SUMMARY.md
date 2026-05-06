---
name: M80 F2 v8 — 21/32 and 11/15 are GENUINE closed forms for R-6 Conjecture 3.3(c)
description: Chowla-Selberg convention analysis for K=Q(sqrt(-7)), Q(sqrt(-11)). R(f) is Omega-independent; 21/32 and 11/15 confirmed exact. Bootstrap Damerell ladders computed. Hallu 91->91.
type: project
---

# M80 — F2 v8: Chowla-Selberg convention analysis for d=7, d=11

**Date:** 2026-05-06 | **Sub-agent:** M80 (Sonnet) | **Hallu:** 91->91

## VERDICT: 21/32 and 11/15 ARE GENUINE — not Omega artifacts

R(f) = pi*L(f,1)/L(f,2) is OMEGA-INDEPENDENT. No Omega convention can change it.
Conventions tested: Chowla-Selberg (M62), Damerell-Hurwitz, half-period, double-period,
bootstrap. ALL give identical R(f). 21/32 and 11/15 ARE the exact closed forms.

## T1 — Chowla-Selberg conventions (from lemniscate_note.tex + f2_v7_pari.py)

  Omega_7  = [Gamma(1/7)*Gamma(2/7)*Gamma(4/7)/(Gamma(3/7)*Gamma(5/7)*Gamma(6/7))]*(7/(4pi^2))^(1/4)
  Omega_11 = [Gamma(1/11)*Gamma(3/11)*Gamma(4/11)*Gamma(5/11)*Gamma(9/11)/
               (Gamma(2/11)*Gamma(6/11)*Gamma(7/11)*Gamma(8/11)*Gamma(10/11))]*(11/(4pi^2))^(1/4)
  chi_{-7}:  +1 at QR mod 7 = {1,2,4}; -1 at {3,5,6}
  chi_{-11}: +1 at QR mod 11 = {1,3,4,5,9}; -1 at {2,6,7,8,10}
  Effect on R(f): NONE (R(f) is Omega-free by construction).

## T2 — Bootstrap Damerell ladders (Omega-free, from M62 PC 80-digit data)

  alpha_m^boot = L(f,m)*pi^(4-m)/L(f,4). Identity: R(f) = alpha_1^boot/alpha_2^boot [exact].

  7.5.b.a (d=7):  L-values L1=0.4563, L2=0.8257, L3=0.9804, L4=1.0186
    ladder: ( (21/4)*sqrt(7),  8,  (8/7)*sqrt(7),  1 )
    parity: m=1,3 in Q(sqrt(7))\Q; m=2,4 in Q. CONFIRMS Conj.3.3(c).
    R(f) = (21/4)*sqrt(7) / 8 = (21/32)*sqrt(7) = 1.73627... [exact]

  11.5.b.a (d=11): L-values L1=0.9482, L2=1.2248, L3=1.1602, L4=1.0745
    ladder: ( (33/4)*sqrt(11),  45/4,  (45/44)*sqrt(11),  1 )
    parity: m=1,3 in Q(sqrt(11))\Q; m=2,4 in Q. CONFIRMS Conj.3.3(c).
    R(f) = (33/4)*sqrt(11) / (45/4) = (11/15)*sqrt(11) = 2.43219... [exact]

  For reference (d=3): ladder = (243/4*sqrt(3), 81/4, 9/4*sqrt(3), 1) -> R(f) = 3*sqrt(3) ✓

## T3 — Why M62's CS alpha_m had large denominators (not dirty structure)

  Omega_CS(d=7) = 7.149, so Omega^4 ~ 2607 >> Omega_boot^4 = L4 ~ 1.018.
  Ratio ~ 2559 (irrational) => alpha_m_CS = alpha_m^boot/2559 => bestappr gives large
  denominators (e.g., 10682/3424131). This is a normalization artifact, NOT dirty arithmetic.
  BOOTSTRAP normalization reveals the clean ladder.

## T4 — Algebraic identity R(f) = alpha_1^boot / alpha_2^boot [proof]

  alpha_1^boot/alpha_2^boot = [L1*pi^3/L4] / [L2*pi^2/L4] = pi*L1/L2 = R(f)  QED.

## T5 — Structural analysis of q_d = R(f)/sqrt(d)

  d=3:  (alpha_1/sqd, alpha_2) = (243/4, 81/4)  -> q_3 = 243/81 = 3
  d=7:  (alpha_1/sqd, alpha_2) = (21/4, 8)       -> q_7 = (21/4)/8 = 21/32
  d=11: (alpha_1/sqd, alpha_2) = (33/4, 45/4)    -> q_11 = 33/45 = 11/15

  Factorizations:
    21/32 = (3*d) / 2^5      [numerator contains conductor d=7; denom = 2^5]
    11/15 = d / (3*5)        [numerator = conductor d=11; denom from alpha_2=45/4]
  gcd(21,32)=1; gcd(11,15)=1 -> IRREDUCIBLE. No simpler form exists.

## Implications for R-6 paper

  1. Table tab:d711 and tab:ratios in lemniscate_note.tex are CORRECT. No revision.
  2. Optional remark: "Under bootstrap normalization, the Damerell ladder for d=7 is
     (21/4*sqrt(7), 8, 8/7*sqrt(7), 1) and for d=11 is (33/4*sqrt(11), 45/4,
     45/44*sqrt(11), 1), with parity split alpha_m in Q(sqrt(d))\Q for m odd."
  3. For future work: the alpha_2^boot values 8 (d=7) and 45/4 (d=11) encode the
     arithmetic of the CM Hecke character and may have a closed-form description via
     Bernoulli numbers or class group data.

## Files
  - SUMMARY.md (this), f2_v8_pari.py, f2_v8_results.csv

## Discipline log
  - 0 fabrications | all values from M62 CSV (80-digit PARI PC) | Hallu 91->91
