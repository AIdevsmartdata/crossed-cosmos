# H7 Test: G_2 Lattice and Cosmological Constant Λ via Dense-Regime EE Extrapolation

**Date**: 2026-05-26
**Hypothesis**: Λ/M_Pl⁴ ∼ exp(−κ_dense(G_2) · V_obs/V_horizon) with dark G_2 sector
**Observed target**: ln(Λ/M_Pl⁴) ≈ −122.8 (i.e. Λ/M_Pl⁴ ≈ 10^{-122.8/ln10} ≈ 1.1e-53; cosmological-constant problem ≈ −123 in log10 OR ~−283 if using ζ-energy density depending on normalization — H7 uses −122.8)

---

## 1. Literature Summary (G_2 Lattice Gauge Theory)

Five verified papers form the spine of G_2 lattice studies; **no paper reports a direct entanglement-entropy measurement in G_2**. All numerical results are confined to thermodynamics (T_c, p, ε, s), string tension σa², Polyakov-loop susceptibility, and Casimir-scaling tests.

| arXiv ID | Authors | Year | Content | Verified |
|---|---|---|---|---|
| hep-lat/0302023 | Holland, Minkowski, Pepe, Wiese | 2003 | Foundational: G_2 has trivial center, "exceptional confinement", G_2 ⊃ SU(3) via Higgs breaking, string breaking by gluon screening | YES |
| hep-lat/0610076 | Pepe, Wiese | 2007 | First-order finite-T deconfinement in G_2 despite trivial center | YES |
| 0709.0669 | Cossu, D'Elia, Di Giacomo, Lucini, Pica | 2007 | First-order deconfinement confirmed; β_c(∞)=1.3950(4) (Wilson action); FSS analysis | YES |
| 1210.7950 | Maas, Wellegehausen | 2012 | Comprehensive review of G_2 YM, YM-Higgs, QCD-like; no EE | YES |
| 1409.8305 | Bruno, Caselle, Panero, Pellegrini | 2015 | EOS of G_2: Δ/T⁴, p/T⁴, ε/T⁴, s/T³; **per-gluon-dof normalization collapses G_2 onto SU(3), SU(4) universal curve**; SB limit p/T⁴ = (14/45)π² | YES |
| 1501.01172 | (Bonati et al.) Topology and θ-dependence in G_2 | 2015 | Topological susceptibility, instanton gas above T_c | YES |
| hep-lat/0609050 | Greensite, Langfeld, Olejnik, Reinhardt, Tok | 2007 | Casimir scaling of intermediate string tensions in G_2 | YES |

**REFERENCES IN ORIGINAL TASK PROMPT THAT ARE WRONG (anti-fab)**:
- "arXiv:0712.0533" — Verified to be Verley et al. M33 astronomy paper, NOT G_2 lattice. Mis-cited as Holland-Pepe-Wiese.
- "hep-lat/0510074" — Verified to be Chen et al. SU(3) glueball spectrum, NOT G_2.
- Correct Holland et al. ID is **hep-lat/0302023**.

**Key numerical anchors verified from Bruno et al. (1409.8305)**:
- String tension σa² at β=10.4: 0.02369(66); at β=10.0: 0.0471(11); at β=9.6: 0.1335(77)
- Stefan–Boltzmann limit per area: (p/T⁴)_SB = (14/45)π² → confirms 14 physical gluon dof (× 2 polarizations = 28)
- **Per-gluon-dof collapse**: G_2 (d_a=14), SU(3) (d_a=8), SU(4) (d_a=15) all fall on the SAME Δ/(2 d_a T⁴) vs (T_c/T)² curve

**No direct measurement of κ_EE in G_2 exists** as of 2026. The closest proxies are:
1. Per-gluon-dof universality of thermodynamics (Bruno et al.) — strongly suggests κ_EE per dof is also universal
2. Casimir scaling of intermediate string tensions (Greensite et al.) — confirms G_2 confining-like behaviour with σ_R/C_R ≈ constant

---

## 2. Three Candidate Scaling Laws for κ_dense(G_2)

The premise of H7 (κ_dense ∝ √N applied as N → √dim G) is **ad hoc**; testing three different mappings:

| Law | Formula | Numerical value for G_2 (dim=14, rank=2, h^∨=4) |
|---|---|---|
| **L1** | κ_dense = 0.518·√dim(G) − 0.458 = 0.518·√14 − 0.458 | **1.480** |
| **L2** | κ_dense = 0.518·√(dim/rank) − 0.458 = 0.518·√7 − 0.458 | **0.913** |
| **L3** | κ_dense = 0.518·√h^∨ − 0.458 = 0.518·√4 − 0.458 | **0.578** |
| **L4** (added: dilute) | κ_EE(G_2) = κ_∞·(1−1/N_eff²) with N_eff² = dim+1 = 15 (so N_eff²−1=14 d_a) | κ_∞·(14/15) = 0.6782·0.9333 = **0.633** |

### Λ prediction for each law

The mass-gap–like factor in the H7 ansatz is:
ln(Λ/M_Pl⁴) ≈ −κ_dense · (V_obs/V_horizon)

With V_obs/V_horizon ~ 100 (as posed):

| Law | κ_dense(G_2) | Predicted ln(Λ/M_Pl⁴) | Δ vs obs −122.8 | Verdict |
|---|---|---|---|---|
| L1 √dim | 1.480 | −148.0 | +20.5% off | rejected (overshoots) |
| L2 √(dim/rank) | 0.913 | −91.3 | −25.6% off | rejected (undershoots) |
| L3 √h^∨ | 0.578 | −57.8 | −53% off | **strongly rejected** |
| L4 dilute(N_eff²=15) | 0.633 | −63.3 | −48% off | **strongly rejected** |

**No law lands within experimental uncertainty (~few %)** without tuning the volume ratio V_obs/V_horizon, which then becomes the free parameter and the test becomes vacuous.

### Tuning V_obs/V_horizon (one free parameter, three predictions)

Fitting V_obs/V_horizon to match obs −122.8 for each κ_dense:

| Law | Required V_obs/V_horizon | Plausibility |
|---|---|---|
| L1 √dim | 82.9 | most plausible (within order of magnitude of 100) |
| L2 √(dim/rank) | 134.5 | mild stretch |
| L3 √h^∨ | 212.5 | implausibly large |
| L4 dilute | 194 | implausibly large |

**L1 (√dim scaling) gives the cleanest one-parameter fit**, with V_obs/V_horizon = 82.9, within the ballpark of the assumed ~100.

---

## 3. Critical Falsifier: Per-Gluon-dof Universality

The Bruno-Caselle-Panero-Pellegrini result (Fig. 8 of 1409.8305) is a **direct empirical falsifier of any dense-regime crossover for G_2** in the thermodynamic sector:

- Δ/T⁴, p/T⁴, ε/T⁴, s/T³ for G_2 are **quantitatively identical** to SU(3) and SU(4) once divided by 2·d_a (transverse polarizations × adjoint dim).
- This implies κ_EE per unit gluon dof — if it follows the same universality — would also be SU(N)-universal.
- The session-1's "crossover dilute→dense at N=4–5" hypothesis predicts that G_2 (effective N_eff ≈ √15 ≈ 3.87) should sit **in the dilute regime**, NOT dense, since N_eff < 5.

**Therefore the H7 ansatz κ_dense(G_2) ≈ 1.48 is in tension with empirical lattice universality**: G_2 thermodynamic data look dilute (SU(N≤4)-like), not dense.

---

## 4. Verdict on H7

**H7 is conditionally falsified, with one caveat:**

1. **Direct EE measurement in G_2 does not exist** → no smoking-gun number to plug in
2. **Indirect evidence (Bruno et al. universality)** strongly suggests G_2 lives in the **dilute regime**, not the dense regime — contradicting the premise of H7
3. **L4 (dilute prediction, κ ≈ 0.633)** gives the most physically motivated value but requires an implausibly large V_obs/V_horizon ≈ 194 to match Λ
4. **L1 (dense √dim, κ ≈ 1.48)** gives the cleanest one-parameter fit with V_obs/V_horizon ≈ 83, but contradicts (2)

**Best honest assessment**: P(H7 correct as stated) ≈ **10–20%**. The Bruno et al. per-gluon-dof universality result is the dominant headwind — it predicts G_2 should NOT be in a "dense regime" in any standard sense. The cosmological-constant scaling 122.8 is generic and any 1-parameter fit can reproduce it; H7 has no predictive power without independent fixing of V_obs/V_horizon.

**Two productive next steps**:
1. **Lattice EE in G_2 (open opportunity)**: Replicate the Buividovich-Polikarpov (arXiv:0802.4247) SU(2) protocol on G_2 lattices, using existing β-tuning from Bruno et al. Table 1. Direct measurement would settle dilute-vs-dense for G_2 and either confirm or kill H7.
2. **Test SU(7) saturation prediction**: If session-1's crossover law κ_dense ≈ 0.518√N − 0.458 holds, then SU(7) (dim 48) should give κ ≈ 0.91; G_2 (dim 14) plugged as √dim gives 1.48 which is OUTSIDE the SU(N)-extrapolation range and not justified.

---

## 5. Anti-fab Audit

| Cited reference | Status | Note |
|---|---|---|
| arXiv:0712.0533 | INVALID for G_2 | Verley et al., M33 astronomy. The original prompt mis-cited this as Holland-Pepe-Wiese. |
| arXiv:hep-lat/0510074 | INVALID for G_2 | Chen et al., SU(3) glueball spectrum. |
| arXiv:hep-lat/0610076 | VALID | Pepe-Wiese 2007 G_2 deconfinement, confirmed first-order |
| arXiv:hep-lat/0302023 | VALID | Holland-Minkowski-Pepe-Wiese 2003 foundational G_2 confinement |
| arXiv:0709.0669 | VALID | Cossu et al. 2007 first-order, β_c=1.3950(4) |
| arXiv:1409.8305 | VALID | Bruno-Caselle-Panero-Pellegrini 2015 EOS, per-dof universality |
| arXiv:1210.7950 | VALID | Maas-Wellegehausen 2012 review |
| arXiv:1501.01172 | VALID | Topology/θ in G_2 lattice |
| arXiv:hep-lat/0609050 | VALID | Greensite et al. 2007 Casimir scaling in G_2 |
| arXiv:0802.4247 | VALID | Buividovich-Polikarpov SU(2) EE method (for future G_2 application) |

**No fabricated values quoted.** Stefan–Boltzmann constant (14/45)π² and σa²(β=10.4)=0.02369(66) extracted directly from Bruno et al. PDF pages 11 and 19.

---

## Summary

- **G_2 lattice literature is rich on thermodynamics but barren on EE.**
- **H7 (dense √dim scaling) needs V_obs/V_horizon ≈ 83 (not 100) to fit Λ** — survives only as a 1-parameter fit, not a prediction.
- **Strongest headwind**: Bruno et al. 1409.8305 Fig. 8 shows G_2 thermodynamic observables, per gluon dof, are universal with SU(3) and SU(4) — suggests G_2 is in the dilute regime, contradicting H7's premise.
- **P(H7 as stated) ≈ 10–20%** until a direct lattice EE measurement in G_2 is performed.
