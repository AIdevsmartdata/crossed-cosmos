# A50 — Karam-Palatini cite + ECI v7.5-P sub-branch

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A50 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held; under budget at ~25/60 min)

## arXiv:2604.16226 — LIVE-VERIFIED

- arXiv API (HTTPS, 2026-05-05 12:14:31 UTC): 1 entry
- Authors: Alexandros Karam (KBFI Tallinn), Samuel Sánchez López (IAP), José Jaime Terente Díaz (Coimbra)
- Title: "Post-Newtonian Constraints on Scalar-Tensor Gravity"
- 2026-04-17, gr-qc + astro-ph.CO, 42 pp + 5 appendices
- Abstract confirms: BOTH metric AND Palatini formalisms; analytical γ, β, m_eff, G_eff; Palatini gives "weaker local bounds because of stronger Yukawa suppression"

## Key formulas extracted (direct PDF page reads, pp. 11-22)

- Eq. (3.38): m_φ² = 16πGA₀V₂ / [16πGA₀B₀ + 3A₁²(1−δ_P)]
- Eq. (3.41): G_eff(r) = (G/A₀)[1 + A₁²e^{−m_φr}/(16πGA₀B₀ + 3A₁²(1−δ_P))]
- Eq. (3.42): γ(r) = 1 − 2A₁²e^{−m_φr} / [16πGA₀B₀ + 3A₁²(1−δ_P) + A₁²e^{−m_φr}]
- Eq. (3.67): full β(r) expression (Ei(−x) integrals)
- Eqs. (4.31)/(4.32): NMC with B₀=1, B₁=0 → α=A₁²/(16πGA₀+3A₁²) metric vs α̂=A₁²/(16πGA₀) Palatini
- δ_P=0 metric, δ_P=1 Palatini

## Consistency check (in patch)

ECI Lagrangian `-½ξ_χRχ²` → `A₀ = 1−ξ_χ(χ₀/M_P)²`, `A₁ = −ξ_χχ₀/M_P`. Strong-Yukawa metric limit gives `|γ−1| ≈ 8ξ_χ²(χ₀/M_P)²`, so Cassini `≤ 2.3×10⁻⁵` ⇒ **`|ξ_χ|(χ₀/M_P)² ≲ 6×10⁻⁶`**. Matches v7.4 wall (A4_wolf line 134). v7.4 mean ξ_χ=−3×10⁻⁵ sits ~10² OoM inside.

## Deliverables on disk

- `section2_patch.tex` — ~85 lines, stand-alone `\section{Cassini wall and Palatini formulation}` with KSTD26 + Bertotti03 `\bibitem` suggestions appended as comments. NOT live-edited into v74_amendment_v2.tex.
- `v75P_sketch.md` — ~150 lines, full Palatini sub-branch outline: 4 testables (P1–P4), risks, decision matrix conditional on Wolf-signal confirmation by 2027.

## v7.5-P sketch — 4 new predictions

- **P1**: under Palatini NMC posterior, predicted ξ_χ ∈ [+1.5,+3.0], log B > +5 vs ΛCDM (recovers Wolf 2025)
- **P2**: G_eff(z=0)/G_N ∈ [1.4, 1.8] testable in DESI Y3 + LSST 2030
- **P3**: Solar-System Yukawa NULL `|γ−1| < 10⁻⁹` at 1 AU
- **P4**: ALL v7.4 arithmetic-modular falsifiers preserved (DUNE δ_CP, Belle II V_cb, Hyper-K p-decay, CSD(1+√6), Damerell ladder)

Lakatos: protective-belt re-formulation (gravitational sector only), arithmetic core unchanged, predictive content INCREASED. Not committed in v7.4; conditional commit per decision matrix §7.

## Anti-hallu flags for parent

1. The figure `6×10⁻⁶` is NOT in KSTD; it is the ECI-internal restatement of Cassini bound on `(γ−1)` — patch states this clearly.
2. KSTD use Faraoni convention `(−+++)`, `G/A(Φ)` coupling — matches Wolf 2025 App. A and ECI `section_3_5_constraints.tex` line 17.
3. Two suggested bibitems (KSTD26, Bertotti03) provided as comments in patch — parent decides placement.
4. Recommended placement: stand-alone section between `\section{Open questions...}` (line 774) and `\section{Falsifiers}` (line 838) of v74_amendment_v2.tex.
