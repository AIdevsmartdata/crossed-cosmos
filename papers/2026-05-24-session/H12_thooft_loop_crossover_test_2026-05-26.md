# H12 — 't Hooft loop / Wilson loop area-law trade-off at SU(N) crossover N=4-5

**Date**: 2026-05-26
**Author**: Kevin Rémondière + Claude (Opus 4.7 1M)
**Status**: Preliminary analysis — anti-fab verified arXiv IDs

---

## 1. Theoretical framework (Polyakov 1977 + 't Hooft 1978)

'T Hooft (Nucl. Phys. B 138 (1978) 1; B 153 (1979) 141) introduced the
disorder operator T(C) dual to the Wilson loop W(C). Their algebra in
the centre Z_N gives the **commutation relation**

    W(C) · T(C') = z^{L(C,C')} · T(C') · W(C),    z = exp(2πi/N),

where L(C,C') is the linking number. The dual confinement criteria are

    Wilson area-law ⇔ 't Hooft perimeter-law    (electric confinement, magnetic Higgs)
    Wilson perimeter-law ⇔ 't Hooft area-law    (electric Coulomb, magnetic confinement)

**Refresher Polyakov-'t Hooft**: pure SU(N) Yang-Mills in 4D is conjectured to
be in the electric-confinement phase for ALL N≥2 at low temperature. Hence
W(C) has area-law (string tension σ) and T(C) has perimeter-law (chromomagnetic
screening mass μ_T = magnetic dual). The "transition" at N=4-5 is **not** a
phase transition in the Polyakov sense — both σ>0 and μ_T finite throughout.

The crossover N=4-5 in κ_EE (entanglement entropy area-law prefactor) reported
in our project is therefore *inside* the confinement phase and cannot be
explained by a duality flip W↔T at the phase-transition level. H12 must be
re-cast in terms of **sub-leading** structure (e.g. ratio σ/μ_T as a function
of N, not a discontinuity).

## 2. Literature survey (arXiv verified — anti-fab)

**VERIFIED (live arXiv 2026-05-26)**:
- **arXiv:hep-lat/0301023** — J. Greensite, *"The Confinement Problem in Lattice
  Gauge Theory"*, Prog. Part. Nucl. Phys. 51 (2003), 104 pp. Reviews Z(N) centre
  symmetry, vortex picture, Wilson + 't Hooft loops. **GOLD-STANDARD reference**.
- **arXiv:hep-lat/0211004** — P. de Forcrand & O. Jahn, *"Comparison of SO(3)
  and SU(2) lattice gauge theory"*, Nucl. Phys. B 651 (2003). Measures **electric
  twist free energy** as order parameter for deconfinement; precisely the
  observable T(C)-like that H12 needs. SU(2) only.
- **arXiv:hep-lat/0307017** — B. Lucini, M. Teper, U. Wenger, *"The high
  temperature phase transition in SU(N) gauge theories"*, JHEP 2004. Cross-N
  Tc/√σ for N=2..8: Tc/√σ = 0.596(4) + 0.453(30)/N². Useful for σ(N) baseline.

**FALSIFIED IDs (user's prompt — ANTI-FAB FLAG)**:
- **arXiv:hep-lat/0205049** — User cited as "Greensite-Olejnik". **WRONG**.
  Actual paper: Allton-Blythe-Clowser, *"Spectral Functions, MEM and
  Unconventional Methods in Lattice Field Theory"*. Not about 't Hooft loops.
- **arXiv:hep-lat/0202024** — User cited as "de Forcrand-Jahn". **WRONG**.
  Actual paper: Frezzotti-Hasenbusch-Heitger-Jansen-Wolff, *"Comparative
  Benchmarks of full QCD Algorithms"*. Not 't Hooft loop study.
- **arXiv:hep-lat/0405044** — User cited as "Greensite-Olejnik". **404 Not
  Found on live arXiv 2026-05-26**. Unverified, likely fabricated by upstream LLM.

**Recommendation**: replace the 3 falsified IDs by hep-lat/0211004 (Forcrand-Jahn)
+ hep-lat/0301023 (Greensite review) + hep-lat/0307017 (LTW). Search arXiv directly
for further Greensite-Olejnik twist papers; do **not** cite uncomfirmed IDs.

## 3. Lattice protocol (using existing 't Hooft twist code)

**Existing code**: `papers/2026-05-24-session/scripts/jax_su3_tHooft_lattice_PROPER_FIX_2026-05-26.py`
(1351 lines, validated SU(3) twist 2026-05-26 — paper Twist-Mode-Zero LMP). Provides:
- twisted-boundary similarity transport (`gather_link_twist`)
- twisted Wilson action with z_{μν} centre phase on corner plaquette
- twist-aware Metropolis sweep (FIX 2026-05-26: K vs K† convention)
- expected ⟨P⟩_twisted vs ⟨P⟩_periodic difference proportional to L^{D-2}/L^D

**Adaptation for H12** (≈ 300 lines new code):

1. **Generalise N**: replace hard-coded N_GROUP=3 by parameter ∈ {3,4,5,6}.
   Use Gell-Mann analogues T_GEN^{(N)} (generic basis from `scipy.linalg.expm`).
   Twist matrices Ω_1 = diag(1, ω, ω², …, ω^{N-1}), Ω_2 = cyclic shift, ω=exp(2πi/N).

2. **'t Hooft loop measurement** via twist free-energy ratio
   (Forcrand-Jahn hep-lat/0211004):

       ⟨T(C)⟩ = Z_twist(C) / Z_periodic
              ≈ exp(-F_twist(C))

   where the twist is supported on a 2-surface bounded by C. Practical
   implementation: switch z_{μν} on a sub-region (rectangular box R×T inside
   the lattice) — measure free-energy difference via integration in β
   (Forcrand-Jahn method) OR snake algorithm (de Forcrand 2001).

3. **Wilson loop W(C)** standard observable (already in any pure-gauge code).
   Use APE smearing 4 levels α=0.5 → noise reduction at large R×T.

4. **Cross-N parameter scan**:
   - L = 8 (fixed, modest)
   - β tuned for fixed lattice spacing a·√σ ≈ 0.20:
     * SU(3): β = 6.0
     * SU(4): β ≈ 10.6 (Lucini-Teper-Wenger scaling)
     * SU(5): β ≈ 16.8
     * SU(6): β ≈ 24.5
   - Loop sizes R×T ∈ {2×2, 2×4, 4×4, 4×6, 6×6} → extract σ from Creutz ratio
   - Twist-region sizes same → extract μ_T via -ln Z_twist/L^{D-2}

5. **Falsifiable observable**: ratio σ/μ_T(N) cross-N.

**Predictions**:
- 't Hooft large-N: σ ∝ N²·a^{-2}, μ_T ∝ N²·a^{-2} → σ/μ_T → const.
- If H12 (subleading flip at N=4-5): expect kink Δ(σ/μ_T)/σ ≥ 10% between N=4 and N=5.
- Null hypothesis (smooth large-N): σ/μ_T(N) smooth in 1/N², matches κ_EE smooth
  in 1/N² (the 1-1/N² law) → H12 falsified.

## 4. Computational estimate (RTX 5060 Ti, JAX)

Existing code: SU(3) L=8 thermalisation 6k sweeps + 200 configs measure on RTX 5060 Ti ≈ 25 min/β.

Scaling: thermalisation cost ∝ N²·L⁴. Twist Z-ratio integration in β with K=10 β-points
multiplies cost by ~10. Wilson + 't Hooft loops cheap.

| N | β | Therm | Z-integration | Total (1 β) |
|---|---|---|---|---|
| 3 | 6.0 | 25 min | 4 h | ~5 h |
| 4 | 10.6 | 45 min | 7 h | ~8 h |
| 5 | 16.8 | 70 min | 12 h | ~13 h |
| 6 | 24.5 | 110 min | 18 h | ~20 h |

**Total H12 minimal scan** N=3,4,5,6 single β each: ≈ 46 h on RTX 5060 Ti. Multi-volume
L=8,12 to extrapolate σ in continuum: ×3-4 → ~150 h. Realistic: 1 week wallclock.

## 5. Verdict preliminary

- **Theoretical**: H12 in the strong form ("phase transition at N=4-5") is
  **disfavoured** by standard Polyakov-'t Hooft: confinement persists for all
  N≥2 in 4D pure YM. Sub-leading reformulation viable.
- **Computational**: feasible with existing code + ~300 LOC adaptation + 150h GPU.
- **Coupling to κ_EE crossover**: speculative. Prior 1-1/N² fit is smooth; a
  discontinuity in σ/μ_T at N=4-5 would be surprising and would require an
  underlying centre-symmetry restructure not predicted by any known mechanism.
- **Recommendation**: **deprioritise H12** unless an additional theoretical
  argument (e.g. centre-vortex percolation threshold N* arising from β-function
  RG analysis) is provided. P(H12 supported) preliminary **5-15%**.

P(measurement feasible Phase 2) = 80% (clear protocol + verified code).
P(H12 confirmed numerically) = 5-15% (against theoretical prior).

**Anti-fab summary**: 3 of 4 arXiv IDs in user's prompt were falsified (one wrong content,
one wrong content, one 404). Verified replacement IDs given above.

---
**Files referenced** (all absolute):
- `/root/cc-private/papers/2026-05-24-session/scripts/jax_su3_tHooft_lattice_PROPER_FIX_2026-05-26.py`
- `/root/cc-private/papers/2026-05-24-session/scripts/README_tHooft_lattice_2026-05-26.md`
- `/root/cc-private/papers/Paper_tHooft_Twist_Mode_Zero_LMP/main.tex`
