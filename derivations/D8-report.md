# D8 — Swampland × NMC cross-constraint (2026-04-21 night session)

## Question
If the thawing scalar χ of A4 and the KK tower of A5 share the same EFT
cutoff Λ (as they must if both are bulk modes of one higher-dimensional
sector), does imposing that shared cutoff tighten the D7 Cassini bound
|ξ_χ| ≤ 2.4×10⁻²?

## Derivation (summary)
User-supplied cutoff: Λ ~ M_P (H/M_P)^c' (Bedroya et al., 2503.19898).
EFT self-consistency of the operator ξ_χ R χ²/2 demands the coupling-induced
shift of the Planck mass not exceed the cutoff squared:
  δM_P²  ≡  ξ_χ χ₀²  ≤  Λ²
  ⇒  ξ_χ (χ₀/M_P)²  ≤  (H_0/M_P)^(2c').
Combined with D7 Cassini: |ξ_χ|(χ₀/M_P) ≤ 2.4×10⁻³.
Limits verified symbolically:
 • ξ_χ→0: operator vanishes — GR recovered.
 • c'→0: Λ→M_P, EFT reduces to the no-ghost A4 condition; only Cassini
   survives ⇒ D7 bound 2.4×10⁻² recovered exactly.

## Numerical outcome (χ₀ = M_P/10, fiducial)

| c'    | Cassini |ξ|  | Swampland-EFT |ξ| | joint        | tightening |
|-------|-------------|-------------------|--------------|------------|
| 0.01  | 2.4×10⁻²    | 6.2               | 2.4×10⁻²     |  0 %       |
| 0.05  | 2.4×10⁻²    | 9.5×10⁻⁵          | 9.5×10⁻⁵     | 99.6 %     |
| 0.10  | 2.4×10⁻²    | 9.0×10⁻¹¹         | 9.0×10⁻¹¹    | ~100 %     |
| 0.50  | 2.4×10⁻²    | 5.9×10⁻⁵⁹         | 5.9×10⁻⁵⁹    | ~100 %     |

At the paper's A5 fiducial c' = 0.05 ± 0.01, the cross-constraint tightens
|ξ_χ| from 2.4×10⁻² (D7) to **9.5×10⁻⁵** (range 5.9×10⁻⁶ – 1.5×10⁻³), i.e.
a **factor ~250 tightening**.

## Phenomenological compatibility
A far more dramatic tension appears in the reverse direction. Thawing DE
requires χ₀/M_P ~ 0.1–1 to drive acceleration today. The EFT-bulk condition
at |ξ_χ| = 2.4×10⁻² and c' = 0.05 forces χ₀/M_P ≤ 6.3×10⁻³ — already
an order of magnitude below what A4 needs. Using the literal Dark-Dimension
cutoff Λ ~ meV (rather than the c' = 0.05 value of the user's formula,
which actually gives Λ ~ 10¹⁵ GeV; the meV scale corresponds to
c' ≃ 0.505), the bound collapses to χ₀/M_P ≤ 3×10⁻³⁰ and thawing
quintessence is excluded outright.

## Verdict
**A4 and A5 are mutually consistent only if χ is NOT a bulk mode of the
Dark Dimension sector.** Under the shared-cutoff hypothesis either
(i) the Cassini-admissible |ξ_χ| shrinks by ~250×, or (ii) the thawing DE
phenomenology is killed at the meV cutoff. The cross-constraint is genuine
new physics in the sense that it forces a *model-building choice* the paper
did not previously make explicit: χ must live as a 4D zero-mode, in a
separate sector from the A5 tower, or must be screened locally.

## Is it a new paper section?
**Yes** — the tightening >99% at the paper's fiducial c' is well above the
30% threshold, and the "A4-χ cannot be a bulk mode of A5" conclusion is a
substantive, falsifiable architectural statement. A new §3.6 is drafted
and \input in eci.tex.

## Caveats
1. The EFT condition δM_P² ≤ Λ² is order-of-magnitude; an O(1)
   coefficient could shift the tightening by a factor 2 but not the
   qualitative conclusion (still ≫30%).
2. Screening (chameleon/symmetron) would decouple local χ₀ from the
   cosmological background and weaken the Cassini leg; the cross-bound
   then applies at cosmological χ₀, still giving a strong tightening.
3. The formula Λ = M_P(H/M_P)^c' is the user's statement; the literature
   Bedroya form involves the CC density directly and gives c'≃0.5 for
   meV. We quote both in the script; results of the sign of the tightening
   are independent of this choice.

## Deliverables
- `derivations/D8-plan.md`
- `derivations/D8-swampland-nmc-cross.py` (sympy + matplotlib, self-verified)
- `derivations/figures/D8-c-xi-overlap.{pdf,png}`
- `derivations/D8-report.md` (this file)
- `paper/section_3_6_swampland_cross.tex` (drafted, \input in eci.tex)
