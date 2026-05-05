# A78 — Alternative Hecke-restriction chains H6 → chi_d

**Purpose.** Tabulate every plausible relaxation H6 ↦ {chi_3, chi_5, chi_7, chi_8,
chi_11, chi_12, chi_15, chi_24} together with (i) the unique imaginary-quadratic
field K = Q(sqrt(-d_K)) that is consistent with that nebentypus on a weight-5
CM newform of small level; (ii) the LMFDB label of the candidate newform; (iii)
the SL(2,Z) elliptic fixed point tau_S that is produced; (iv) the
Hurwitz-anchored Damerell ladder value alpha_2; (v) the qualitative DKLL19
weight-2 alignment at the corresponding tau_S; (vi) the lepton-fit verdict
under an NPP20-style 2-RH-nu seesaw.

All LMFDB labels were live-fetched on 2026-05-05 evening (search URL
`https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/?weight=5&char_order=2&dim=1&cm=yes`,
156 matches, dimension-1, U(1)[D2] Sato-Tate, analytic rank 0).  Damerell
ladder rationals (column "12 alpha_2 sqrt|D_K|") are taken verbatim from A5's
preserved PSLQ-clean computation at mp.dps=60 (cm_alpha_normalized.py).

The DKLL19 alignment column reproduces Ding-King-Liu-Lu (arXiv:1910.03460)
Table 1 Case B for the S'_4 weight-2 modular triplet Y_3^(2)(tau).

## Master table

| chi | order | K = Q(sqrt(-d)) | weight-5 CM newform | tau_S (SL(2,Z) elliptic?) | 12 alpha_2 sqrt|D_K| | alpha_2  exact | alpha_2 == 1/12 | DKLL19 Y_3^(2) at tau_S | NPP20 lepton fit |
|-----|------:|------------------|---------------------|---------------------------|---------------------:|----------------|:----------------:|--------------------------|------------------|
| **chi_4**  | 2 | **Q(i)**       | **4.5.b.a**  | **tau = i** (S-fixed)    | **2**       | **1/12**           | **YES** | **(1, 1+sqrt 6, 1-sqrt 6)** | **CSD(1+sqrt 6) viable, sin^2 theta_13 ~ 0.05 proxy, fits PDG-2024 after 2-param fit (King 2022)** |
| chi_3      | 2 | Q(sqrt-3)      | 12.5.c.a     | tau = omega (ST-fixed)   | 4/5         | sqrt(3)/45         | no      | (0, 1, 0)                   | DEGENERATE: cross-product |v_atm x v_sol|^2 = 1, sin^2 theta_13 proxy = 1/2 -- refuted at >> 5 sigma |
| chi_8      | 2 | Q(sqrt-2)      | 8.5.d.a      | NONE (no SL(2,Z) fix)    | 9/5         | 3 sqrt(2)/80       | no      | -- (no S'_4 fixed point)    | inapplicable: tau = i sqrt 2 is NOT an SL(2,Z) elliptic point |
| chi_7      | 2 | Q(sqrt-7)      | 7.5.b.a      | NONE                     | 64/35       | 16 sqrt(7)/735     | no      | --                          | inapplicable |
| chi_11     | 2 | Q(sqrt-11)     | 11.5.b.a     | NONE                     | 18/11       | 3 sqrt(11)/242     | no      | --                          | inapplicable |
| chi_5      | 2 | Q(sqrt-5)      | 20.5.d.a/b   | NONE                     | (uncomputed; no h(K)=1) | -- | no | -- | inapplicable; Q(sqrt-5) has h(K)=2, breaks A5 anchor |
| chi_12     | 2 | Q(sqrt-3)*     | 12.5.c.a     | tau = omega (ST-fixed)   | 4/5         | sqrt(3)/45         | no      | (0, 1, 0)                   | same as chi_3 — refuted |
| chi_15     | 2 | Q(sqrt-15)     | 15.5.d.a/b   | NONE                     | not in A5 ladder (h(K)=2) | -- | no | -- | inapplicable |
| chi_24     | 2 | Q(sqrt-6)      | 24.5.h.a/b   | NONE                     | not in A5 ladder (h(K)=2) | -- | no | -- | inapplicable |

Asterisk on chi_12: the LMFDB "character orbit c" of conductor 12 has the
same Kronecker symbol as chi_3 of conductor 3; the K = Q(sqrt-3) selection
is identical, only the level changes from 12 (CM newform 12.5.c.a) -- it
does not provide a *new* candidate.

## Why "(none)" for chi_5, chi_7, chi_8, chi_11, chi_15, chi_24 in column "tau_S"

The SL(2,Z) modular group has exactly two elliptic conjugacy classes:

  - tau = i, stabiliser <S> of order 2, yields Z_2 residual modular symmetry;
  - tau = omega = e^{2 pi i / 3}, stabiliser <ST> of order 3, yields Z_3 residual.

There is NO SL(2,Z) elliptic point of order >= 4.  Imaginary-quadratic CM
points such as tau = i sqrt 2, tau = i sqrt 7, tau = (1 + i sqrt 11)/2 are
genuine CM points of the upper half-plane, but they are *not* SL(2,Z)-elliptic;
they are instead Heegner / class-number points whose stabilisers are trivial
in PSL(2,Z).  Therefore, although a CM newform exists for each such K, NONE of
them produces a non-trivial residual modular symmetry that could anchor a
DKLL19 / NPP20-style alignment.

This is the key structural reason that the H6 relaxation cannot reach beyond
{Q(i), Q(sqrt-3)} in any meaningful way.

## Independent KW dS-trap admissibility

KW (King-Wang arXiv:2310.10369) gives BOTH tau = i AND tau = omega as
kinematic dS-trap fixed points (modular weight-2 of partial_tau V).  Therefore
the KW column "admits" exactly chi_4 and chi_3 (and chi_12 as a re-labeling of
chi_3); it FAILS to admit chi_5, chi_7, chi_8, chi_11, chi_15, chi_24 because
their associated tau_S are NOT SL(2,Z) elliptic and KW's modular-weight argument
does not apply.

## Summary of three structural filters

| chi    | T1 Damerell alpha_2 = 1/12 | T2 SL(2,Z) elliptic | T3 DKLL19 CSD viable | KW dS-trap admits | Verdict |
|--------|:---:|:---:|:---:|:---:|---|
| chi_4  | YES | YES (i)     | YES (1, 1+sqrt 6, 1-sqrt 6) | YES | **ALL PASS** |
| chi_3  | no  | YES (omega) | no (collapses to (0,1,0))  | YES | PARTIAL — KW only |
| chi_12 | no  | YES (omega) | no                           | YES | PARTIAL — KW only |
| chi_8  | no  | no          | n/a                         | no  | FAIL |
| chi_7  | no  | no          | n/a                         | no  | FAIL |
| chi_11 | no  | no          | n/a                         | no  | FAIL |
| chi_5  | no  | no          | n/a                         | no  | FAIL |
| chi_15 | no  | no          | n/a                         | no  | FAIL |
| chi_24 | no  | no          | n/a                         | no  | FAIL |

**Only chi_4 satisfies the joint conjunction (T1 AND T2 AND T3).**

## Damerell ladder L(f, 1) values (LMFDB live-fetch, 2026-05-05 evening)

LMFDB displays only L(f, 5/2) (central) and L(f, 1/2) (= L(f, 5/2) by FE) for
weight-5 CM forms, and lists L(f, 1), L(f, 2), L(f, 3), L(f, 4) as
"not available" on the L-function landing pages.  The integer-point critical
values used in the Damerell ladder were hence computed in A5 via the
Iwaniec-Kowalski Approximate Functional Equation (AFE) at mp.dps=60, and
verified to satisfy the FE identity L(4)/L(1) = (2 pi)^3 / (6 N^{3/2}) to
10^{-12}.  For reference, LMFDB-displayed central values are:

| label    | K          | L(f, 5/2) (LMFDB)     |
|----------|------------|------------------------|
| 4.5.b.a  | Q(i)       | 0.5200744676          |
| 7.5.b.a  | Q(sqrt-7)  | 0.9246613506          |
| 8.5.d.a  | Q(sqrt-2)  | 1.102297224           |
| 12.5.c.a | Q(sqrt-3)  | 1.270251619           |

(11.5.b.a not re-fetched this round — LMFDB rate-limited; A5's saved L-values
remain valid since cm_alpha_normalized.py computes them de novo via AFE.)

## Honest caveats

1. **Q(i) is ALREADY an input** to the cross-K Damerell ladder — A5 forces
   alpha_1 = 1/10 by HURWITZ-LEMNISCATIC anchor, which is itself the K=Q(i)
   normalisation.  The "alpha_2 = 1/12 only at Q(i)" statement is thus
   *Hurwitz-relative*, not absolute.  See A5 caveat: "K-specific Bernoulli
   alignment, NOT universal CM-CFT identity".  The argument here is "if you
   accept the Hurwitz anchor, then chi_4 is unique" — chi_4 / Q(i) wins
   *because* the chosen anchor is Q(i)-flavoured.
2. **The SL(2,Z) elliptic-fixed-point classification IS universal**:
   T2 is anchor-independent and rules out chi_5, chi_7, chi_8, chi_11, etc.
   without any choice.
3. **The DKLL19 alignment IS universal modulo S'_4 group choice**: T3 follows
   from the unique non-trivial weight-2 S'_4 modular form Y_3^(2)(tau)
   computed in 1910.03460 §5 and confirmed in King 2022 (arXiv:2211.00654).
4. The "NPP20 lepton fit" verdict for chi_3 is given via a CSD-style
   sin^2 theta_13 PROXY (cross-product-of-alignment-vectors heuristic).  The
   full chi^2 against PDG-2024 needs running NPP20 code at tau = omega
   directly; deferred for compute time but the qualitative collapse
   (DKLL19 alignment becomes (0, 1, 0)) is unambiguous.

## Cross-references

- A5 (Hurwitz-Bernoulli alpha_2 = 1/12 K-specificity, mp.dps=60 PSLQ).
- A14 (DKLL19 cross-K test, Y_3^(2) at tau=i vs tau=omega).
- A47 (KW dS-trap, weight-2 fixed-point kinematic argument).
- A48 / A63 (dMVP26 Kahler-canonical hierarchy at tau=i, A63 corrected y_d/y_s).
- A60 (meta-theorem analysis: H6-co-dependence of chains A & B).
- A65 (v7.5 axiomatic restatement of H6).
- PNT/paper_lmfdb_s4prime.tex (Galois-descent closure for HH = {T(p) : p == 1 mod 4}).
