# ECI v7.5-P: Palatini Sub-Branch Sketch

**Author:** Sonnet sub-agent A50 (parent persisted)
**Date:** 2026-05-05 (post wave 4-5)
**Status:** OPEN FUTURE DIRECTION -- not committed in v7.4 amendment
**Lakatos tag:** Auxiliary protective belt (re-formulation), NOT new core hypothesis
**Hallucination counter:** 84 entering / 84 leaving (held)

---

## 1. Motivation (one paragraph)

ECI v7.4-metric enforces the Cassini wall `|ξ_χ|(χ₀/M_P)² ≲ 6×10⁻⁶` by
construction; the resulting NMC posterior is consistent with `ξ_χ ≈ 0`
(Levier 1B mean `≈ −3×10⁻⁵`, log B = −1.37 vs ΛCDM). Wolf et al. 2025
(arXiv:2504.07679) report `ξ ≈ 2.31` (`log B = +7.34` vs ΛCDM) under
the algebraically-identical Lagrangian `-½ξφ²R`, with NO Cassini wall
enforced. The two results cannot both describe the same Universe.

Karam-Sánchez López-Terente Díaz (KSTD, arXiv:2604.16226, 2026) prove
that in the Palatini formalism the Cassini wall on `(γ−1)` is relaxed
by up to ~10 orders of magnitude in `V₂^min` (their Fig. 2 left) for
small `A₀` and large `|A₁|`, because the Palatini screening length
`m̂_φ⁻¹ = V₂^{−1/2}` is independent of the conformal coupling. ECI v7.5-P
is the auxiliary sub-branch that swaps the metric variational principle
for the Palatini one, INHERITING all v7.4 arithmetic-modular anchors
unchanged.

## 2. What changes from v7.4-metric to v7.5-P

| Element | v7.4-metric | v7.5-P (Palatini) |
|---|---|---|
| Variational principle | metric only | metric + connection independent |
| Connection | Levi-Civita of `g_μν` | independent affine `Γ̂^α_μν` |
| Effective scalar mass | `m_φ² = 16πGA₀V₂ / (16πGA₀B₀ + 3A₁²)` | `m̂_φ² = V₂ / B₀` |
| Yukawa coupling at Solar System | `α = A₁²/(16πGA₀ + 3A₁²)` | `α̂ = A₁²/(16πGA₀)` |
| `(γ−1)` at fixed `r` | `−2α e^{−m_φ r}/(1 + α e^{−m_φ r})` | same shape, m̂_φ ≫ m_φ ⇒ stronger Yukawa suppression |
| Cassini wall on ξ_χ | `|ξ_χ|(χ₀/M_P)² ≲ 6×10⁻⁶` | RELAXED, potentially by `O(10⁵)`–`O(10¹⁰)` depending on `(A₀, V₂)` |
| Cosmological NMC posterior | `ξ_χ ≈ 0`, log B ≈ −1.4 | `ξ_χ` free, contests Wolf et al. 2025 head-to-head |
| Arithmetic-modular anchors (f_4.5.b.a, τ-attractor, Damerell ladder) | active | UNCHANGED |
| `H_5'`, `H_7'` | active | UNCHANGED |
| H7-A Damerell ladder integer hits | active | UNCHANGED |
| K = Q(i) selection (CSD `1+√6`) | active | UNCHANGED |

KEY POINT: v7.5-P is a re-formulation of the **gravitational sector only**.
The flavour, neutrino, and CFT predictions of v7.4 are not affected at the
level of the action; only the local-gravity falsifier is loosened.

## 3. New predictions (4 testables)

1. **P1 -- NMC posterior recovery of Wolf signal.**
   Under v7.5-P, re-run the Planck PR4 + DESI DR2 + Pantheon+ MCMC with
   `ξ_χ` prior `[−3, +3]` (no Cassini wall, since Palatini relaxes it).
   PREDICTION: posterior mean `ξ_χ ∈ [+1.5, +3.0]` at >2σ, **recovering
   Wolf et al. 2025 result with `log B > +5` vs ΛCDM**. If recovered,
   v7.5-P + v7.4 arithmetic anchors becomes a unified detection-compatible
   ECI. If NOT recovered (e.g. log B < +2 or ξ_χ posterior straddles 0
   with Cassini wall lifted), Wolf signal flagged as Lagrangian-fragile.

2. **P2 -- modified `G_eff(z=0)`.**
   At Palatini saturation with `ξ_χ ≈ 2`, KSTD eq. (3.41) gives
   `G_eff(z=0)/G_N ∈ [1.4, 1.8]` at cosmological scales. PREDICTION:
   detectable as a `μ(z=0)` enhancement in DESI Y3 + LSST cross-correlation
   (~2030), at the same `~4σ` level Wolf et al. 2025 see for metric. If
   v7.5-P predicts `μ(z=0) ≈ 1.0` (Yukawa over-suppression), v7.5-P fails
   independently of v7.4.

3. **P3 -- Solar-System Yukawa-fifth-force NULL.**
   Despite cosmological `ξ_χ ≈ 2`, v7.5-P predicts `(γ−1) < 10⁻⁹` at 1 AU
   (Palatini Yukawa screening length `m̂_φ⁻¹ ≪ R_⊙`). FUTURE Cassini
   improvement to `|γ−1| ≤ 10⁻⁶` does NOT falsify v7.5-P (the wall is
   physically loose), but PRACTICAL falsifier exists if `m̂_φ⁻¹` falls in
   sub-mm range and Cavendish/torsion-balance experiments at micro-meter
   scales rule it out. EOT-WASH 2030+ at `~10⁻¹⁰` test of inverse-square
   law would constrain `V₂` directly.

4. **P4 -- preserves all arithmetic-modular falsifiers of v7.4 unchanged.**
   DUNE 2030+ `δ_CP = −87° ± 15°` still applies (CSD(1+√6)).
   `|V_us| = 9/40 = 0.225` (NA62 + FLAG-2027) still applies.
   `|V_cb|² = 1/600` (Belle II 2030) still applies.
   p-decay branching ratio `B(p→e⁺π⁰)/B(p→K⁺ν̄) ∈ [0.3, 3]` (Hyper-K +
   DUNE 2030+) still applies.
   v7.5-P falls UNCHANGED if any of (A14, A17, G1.12.B M3-M6) closes negative.

## 4. What v7.5-P does NOT change

- The Damerell ladder integer hits `{1/10, 1/12, 1/24, 1/60}` -- pure
  number theory, no gravitational sector dependence.
- The W1 τ-attractor at `τ* = −0.19 + 1.00i`, χ²/dof = 1.05 -- pure
  flavour MCMC, no PPN dependence.
- The CSD(1+√6) Littlest Modular Seesaw at `τ_S = i` -- modular flavour,
  no PPN dependence.
- The H_5' attractor / H_7' integer-Damerell axiomatic structure.

## 5. Risks / known challenges

1. **Palatini coupling-to-matter consistency.** KSTD assume matter
   couples minimally to `g_μν` (their Sec. 2, footnote on metric-affine
   class). v7.5-P inherits this; metric-affine extensions with non-minimal
   matter coupling are OUT OF SCOPE.

2. **f(R̂) Palatini collapses to GR.** KSTD show in their Sec. 4.2.3
   that Palatini `f(R̂)` reduces to GR exteriors at 1PN for point-particle
   sources. v7.5-P MUST use a non-trivial scalar-tensor action (`A(Φ)R̂`
   with `A` non-constant), NOT pure `f(R̂)`. If the NMC dark-energy
   sector reduces to `f(R̂)` under any field redefinition, v7.5-P
   collapses to GR exteriors and loses observational distinguishability.

3. **Cosmological perturbations differ.** Palatini structure formation
   on linear scales differs from metric (KSTD ref. [28-36]). v7.5-P MUST
   re-run CLASS / CAMB modifications (e.g. EFCAMB) with Palatini perturbation
   equations, NOT inherit metric-NMC perturbations directly. Estimated
   compute: ~3-4 weeks dev (cf. A41 R2 dual-branch estimate).

4. **No published Palatini cosmology likelihood at present.** v7.5-P
   requires either custom code (CLASS-Palatini-NMC fork) or analytic-EFT
   approximation. RISK: 6-12 month timeline before MCMC-grade Palatini
   posteriors are available.

## 6. Lakatos status

- **Hard core preserved:** arithmetic CM newform anchor `f_4.5.b.a`, K = Q(i),
  τ-attractor near `i`, Damerell ladder.
- **Protective belt MODIFIED:** swap metric→Palatini variational principle
  in the gravitational sub-action only.
- **Predictive content INCREASED:** v7.5-P makes 4 new testable predictions
  (P1-P4) that v7.4-metric does not make, and rules out Wolf-style
  fine-tuning via the no-Vainshtein-needed mechanism.
- **NOT a degenerative shift.** The added Palatini structure is independently
  motivated (KSTD 2026, Olmo 2011 reviews) and well-defined; it is not an
  ad-hoc retreat.

## 7. Decision matrix (when to commit)

| Condition (any one of) | Action |
|---|---|
| Wolf et al. 2025 result independently confirmed by 2027 (e.g. ACT DR6 + DESI Y3) | COMMIT v7.5-P as primary cosmological branch |
| Wolf et al. 2025 result refuted (e.g. ACT DR6 finds no `4σ` enhancement) | DROP v7.5-P; v7.4-metric remains baseline |
| All v7.4 arithmetic predictions (DUNE, Belle II, Hyper-K) close NEGATIVE by 2030 | DROP entire programme; v7.5-P moot |
| EOT-WASH micro-Newton 2030+ excludes Yukawa fifth force at `m̂_φ⁻¹ ∈ [0.01, 100] mm` | REFINE v7.5-P with explicit `V₂` lower bound |

## 8. Concrete next-action checklist (not committed in this note)

1. [ ] Read KSTD App. A (connection field equations) and App. B
   (PN detailed calculations) -- estimate 4-6 hours.
2. [ ] Implement `eci.tex` Palatini sub-action with `δ_P = 1` flag in
   `section_3_5_constraints.tex` (gated, off by default).
3. [ ] Fork `axiclass` (or use `EFCAMB`) for Palatini perturbation
   equations; test against analytic Palatini de Sitter (Olmo 2011).
4. [ ] Re-run NMC MCMC with Palatini posterior; compare `log B(v7.5-P / v7.4-metric)`.
5. [ ] If decisive (`|log B| > 3`), draft v7.5-P amendment paper for LMP.
6. [ ] If indecisive, archive as auxiliary appendix in v7.4 final version.

---

**Bottom line:** v7.5-P is a SCOPED, REVERSIBLE, FALSIFIABLE Palatini
sub-branch that addresses the v7.4-metric/Wolf-2025 tension at the
level of the variational principle, while preserving all arithmetic
anchors. It is NOT committed in v7.4; it is registered as an open
research direction conditional on Wolf-signal independent confirmation
or refutation by 2027.
