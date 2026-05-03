# T2 Bianchi Type B extension — III, IV, VI_h, VII_h (Opus 4.7, 1M ctx)

**Date**: 2026-05-03
**Companion to**: `/tmp/T2_bianchi_extension.{md,tex,py}` (Type A: I, IX),
`/tmp/T2_bianchi_V.{md,tex,py}` (Type B: V).
**Sympy script**: `/tmp/T2_bianchi_typeB.py` (clean run, no warnings).
**Full writeup**: `/tmp/T2_bianchi_typeB.tex`.

---

## 1. Per-type metric setup (sympy verified)

In the standard Ellis–MacCallum 1969 canonical form
`C^a_{bc} = epsilon_{bcd} n^{da} + delta^a_b a_c - delta^a_c a_b`,
class B is `a_a != 0`. The h-parameter is `h = a^2/(n_2 n_3)` (with `n_1 = 0`).

| Type | left-invariant 1-forms | nontrivial structure constants | det A |
|------|------------------------|--------------------------------|-------|
| **III (= VI_{-1})** | `omega^1=dx, omega^2=dy, omega^3=e^x dz` | `C^3_{13}=1` | `e^x` |
| **IV** | `omega^1=dx, omega^2=e^x dy, omega^3=e^x(x dy + dz)` | `C^2_{12}=1, C^2_{13}=1, C^3_{13}=1` | `e^{2x}` |
| **VI_h (h<0, !=-1)** | `omega^1=dx, omega^2=e^{p_2 x} dy, omega^3=e^{p_3 x} dz` | `C^2_{12}=p_2, C^3_{13}=p_3` | `e^{(p_2+p_3)x}` |
| **VII_h (h>0)** | `omega^1=dx, omega^{2,3}=e^{q x}(rotation)`, `q=sqrt(h)` | `C^2_{12}=C^3_{13}=q, C^3_{12}=-1, C^2_{13}=1` | `e^{2qx}` |

All sympy-verified by computing dual frames `e_a` and Lie brackets directly.

Misner–Ryan metric (orthogonal class B):
`ds^2 = -dt^2 + sum_{a=1}^3 a_a^2(t) (omega^a)^2`,
with `V(t) := a_1(t)a_2(t)a_3(t) ~ t` near the singularity (Hewitt-Wainwright 1993).

---

## 2. BKL / Hewitt–Wainwright class B asymptotic

**Hewitt & Wainwright, CQG 10 (1993) 99–124**: dynamical-systems analysis of
orthogonal class B vacuum. Past attractor for *generic* parameters is the
Kasner circle K (same as class A), with the Wainwright–Hsu expansion-normalised
variables. **Exception**: VI_{-1/9} has a bifurcation locus `B(VI_{-1/9})`
with non-Kasner past asymptotic (Hewitt–Horwood–Wainwright 2003,
gr-qc/0211071, "Asymptotic dynamics of the exceptional Bianchi cosmologies").

> **Correction to task spec**: the user cited "Hewitt–Wainwright 1990" for
> non-Kasner asymptotic on VI_h/VII_h. Verified against INSPIRE: the actual
> Hewitt–Wainwright 1990 paper (CQG 7, 2295) is on **G_2** cosmologies,
> not class B. The class B asymptotic-dynamics paper is **CQG 10 (1993) 99**.
> The "non-Kasner" claim refers to the **B(VI_{-1/9}) exceptional locus**,
> documented in Hewitt–Horwood–Wainwright 2003, not 1990.

**Generic past asymptotic**:
- Type III, IV: Kasner (Mixmaster-like bounces).
- Type VI_h (h<0, h != -1, -1/9): Kasner.
- Type VII_h (h>0): Kasner past, plane-wave **future**.
- Type VI_{-1/9}: non-Kasner past — **EXCEPTIONAL**.

So `V(t) ~ t` and `sum p_i = sum p_i^2 = 1` hold for all class B
**except** VI_{-1/9}.

---

## 3. S1 / S3 obstruction status per type

**S1 (volume-element divergence)** requires (i) `V(t) -> 0`, (ii) test
function with non-vanishing zero-mode against the spatial measure.

For all class B Lie groups, the spatial slice is **non-compact and
non-unimodular** (or hyperbolic); the spectrum of `-Delta_3` is
**continuous from a strictly positive gap**:
- III: `H^2 x R`, gap = 1/4 (Helgason 1962).
- V: `H^3`, gap = 1.
- IV, VI_h, VII_h: gap > 0 from the non-unimodular friction term
  (`tr(ad_{e_1}) != 0`).

**Consequence**: S1 is **algebraically obstructed** at the L^2 level on
*every* class B type — same caveat as Bianchi V.

**S3 (contracting-Kasner-direction tachyon)** requires `p_a < 0` for
some `a`. Generic class B Kasner: exactly one `p_a < 0` (LRS excluded).
S3 driver **survives** on all class B types except VI_{-1/9}.

---

## 4. BFV folium workaround — NEGATIVE

**BFV** (math-ph/0112041) provides locally covariant nets and Type-III_1
universality, but does **not** provide Hadamard state existence.
Fulling–Narcowich–Wald 1981 deformation gives existence on any g.h.
spacetime, but is **non-constructive** — no explicit `1/sqrt(V(t))`
normalisation for S1.

Closest substitute: **Ringström 2019** (arXiv:1808.00786, CMP 372, 599) —
rigorous KG asymptotic on all Bianchi backgrounds with silent
singularities. Provides classical-mode estimates; Hadamard upgrade
not yet attempted (est. 6-12 months expert work).

---

## 5. Per-type T2 verdict

| Type | Past attr | S1 | S3 | Hadamard | T2 verdict |
|------|-----------|----|----|----------|------------|
| **III** | Kasner | gap | OK | OPEN | **PARTIAL** (S3-conditional) |
| **IV** | Kasner | gap | OK | OPEN | **PARTIAL** (S3-conditional) |
| **VI_h** (gen) | Kasner | gap | OK | OPEN | **PARTIAL** (S3-conditional) |
| **VI_{-1/9}** | non-Kasner | ? | ? | OPEN | **BLOCKED** (exceptional locus) |
| **VII_h** | Kasner+rot. | gap | OK | OPEN | **PARTIAL** (technically hardest) |

---

## 6. Hadamard state existence on Type B — literature scan

INSPIRE searches ("Hadamard state Bianchi", "Hadamard state anisotropic
cosmology", "Hadamard Bianchi III/IV/VI_h/VII_h"): **zero hits** beyond
Bernard 1986 (B-I only), Castagnino–Harari 1984 (general formalism), and
Banerjee–Niedermaier 2023 (B-I SLE).

**Confirmed: Hadamard state existence on every Type B Bianchi (III, IV,
VI_h, VII_h) is OPEN in the literature**, same status as Bianchi V.
Partial positive indicators: Ringström 2019 (KG asymptotic), Ringström
2026 (arXiv:2101.04955, geometry of silent anisotropic singularities) —
the building blocks exist, the Hadamard construction has not been done.

---

## 7. MacCallum–Jantzen variational obstruction — does NOT block T2

The Hawking 1969 / MacCallum 1979 / Jantzen 2001 (gr-qc/0102035)
obstruction: for class B, the symmetry-reduced action is **inconsistent**
with the symmetry-reduced Einstein equations (the variational principle
yields a strict subset).

**This does NOT block T2 extension**. T2 is a QFT-on-CS algebraic
statement on the FULL Einstein-equations-satisfying background. We use
the full Einstein equations directly (via Wainwright–Hsu / Hewitt–Wainwright
expansion-normalised system), never the reduced action. The variational
obstruction is relevant for Wheeler–DeWitt quantum gravity (Jantzen's
"unified picture"), not for BFV.

---

## 8. Honest assessment + time-to-publication

| Horizon | Outcome | Effort |
|---------|---------|--------|
| **1-3 months** | CQG/JMP Comment: T2 extends to all class B *except* VI_{-1/9} with two caveats (S1 spectral-gap; Hadamard open) | tractable |
| **6-12 months** | Adapt Banerjee-Niedermaier SLE to one Type B (V or IV via Helgason-Bray); kills Hadamard gap for that type | tractable |
| **2-5 years** | Unified Type B T2: needs (a) Ringström → Hadamard; (b) B(VI_{-1/9}) resolution; (c) VII_h rotational modes | research programme |
| **Intractable** | VI_{-1/9} exceptional locus until non-Kasner attractor classified | open |

**DO** publish a Comment with the dichotomy "generic class B partial /
VI_{-1/9} blocked" — that is itself a clean finding. **DON'T** claim a
unified Type B theorem yet. Hadamard existence bottlenecks every type;
asymmetry vs. Type A (1-2 weeks for B-I) reflects Hawking's 1969
observation that class B is structurally harder.

---

## 9. References (triangulated via INSPIRE API this session)

- **Hawking 1969**, MNRAS 142, 129 — verified.
- **Ellis & MacCallum 1969**, CMP 12, 108 — classification.
- **Wainwright & Hsu 1989**, CQG 6, 1409 — class A — verified.
- **Hewitt & Wainwright 1993**, CQG 10, 99 — class B — verified
  (NOT 1990; 1990 paper is on G_2).
- **Jantzen 2001**, gr-qc/0102035 — unified Hamiltonian — verified.
- **Heinzle & Ringström 2009**, CQG 26 — B-VI_0 future — verified.
- **Hewitt, Horwood & Wainwright 2003**, gr-qc/0211071 — VI_{-1/9} — verified.
- **Ringström 2019**, CMP 372, 599 = arXiv:1808.00786 — verified.
- **Ringström 2026**, J. Diff. Geom. 132, 461 = arXiv:2101.04955 — verified.
- **Banerjee & Niedermaier 2023**, JMP 64, 113503 = arXiv:2305.11388 — verified.
- **BFV 2003**, CMP 237, 31 = math-ph/0112041 — verified.
- **Bernard 1986**, PRD 33, 3581 — only other Hadamard-Bianchi paper (B-I).

## 10. Files produced

- `/tmp/T2_bianchi_typeB.md` — this summary
- `/tmp/T2_bianchi_typeB.py` — sympy verification (clean)
- `/tmp/T2_bianchi_typeB.tex` — full writeup
