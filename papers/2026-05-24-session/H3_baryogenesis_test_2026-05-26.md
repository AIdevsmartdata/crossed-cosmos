# H3 Test — Baryogenesis via Entanglement Transition
**Date:** 2026-05-26
**Hypothesis:** η_B sourced by SU(N) dilute↔dense κ_EE jump coupled to sphalerons + CKM CP.

---

## 1. Δκ_EE computation (per-area, dimensionless)

Using ECI perturbative law κ_dilute(N) = κ_∞·(1 − 1/N²) with κ_∞ = ζ(3)/√π = 0.6782, and the empirical √N fit for the dense regime (BP2008b-type SU(5,6) lattice extrapolation 2026-05-26 memory):

- κ_dilute(SU(3)) = 0.6782 · (1 − 1/9) = **0.6028**
- κ_dense(SU(3)) ≈ 0.518·√3 − 0.458 = **0.4392** (extrapolation, NOT a measurement at SU(3))
- **Δκ_EE = 0.1636** (~27% jump)

**Caveat:** the √N law is empirically calibrated on SU(5–7) and analytically continued *down* to SU(3). The continuation across the crossover is exactly the regime where the law is *not* expected to be smooth (project memory 2026-05-26: crossover at N≈4–5). So Δκ ≈ 0.16 is an upper bound on the actual jump felt by SU(3); the true value could be smaller or zero (no crossover at all for SU(3) since 3 < 4).

---

## 2. Sphaleron rate

Klinkhamer–Manton (1984): E_sph(T=0) ≈ 4πv/g · B(λ/g²) ≈ 9 TeV.
Kuzmin–Rubakov–Shaposhnikov (1985), Moore (2000), Bödeker (1998):

- **Unbroken EW phase (T > T_EW ≈ 100 GeV):** Γ/V = κ_sph · α_W⁵ · T⁴, κ_sph ≈ 18–25
  → f_sph(T_EW) ≡ Γ/(V·T⁴) = 20 · (0.034)⁵ = **9.09 × 10⁻⁷**

- **Broken phase, T = T_QCD ≈ 0.15 GeV:** Γ/V ∝ exp(−E_sph(T)/T) with E_sph/T ≈ 9000/0.15 = 6 × 10⁴
  → exp(−6 × 10⁴) ≈ 0 (numerical underflow). **Sphalerons are completely decoupled at T_QCD.**

---

## 3. H3 predictions

**QCD-T_c scenario (original H3 formulation):**
η_B ~ (Δκ_EE / N_dof,QCD) · J · f_sph(T_QCD)
   = (0.1636 / 17.25) · (3.05 × 10⁻⁵) · exp(−6 × 10⁴)
   ≈ **0** (strictly < 10⁻²⁶⁰⁰⁰)
→ **Rejects H3 in its original form by ~20 000 orders of magnitude.**

**EW-T scenario (if dark gauge sector provides Δκ at T_EW):**
SU(2)_L itself is always dilute (N=2, no crossover). Assume a hypothetical dark SU(N_dark) with crossover at T ≈ T_EW. Take Δκ ≈ 0.16 (optimistic, copied from QCD scaling), N_dof,SM = 106.75:

η_B ≈ (0.1636 / 106.75) · (3.05 × 10⁻⁵) · (9.09 × 10⁻⁷) = **4.25 × 10⁻¹⁴**

Compared with η_B,obs = 6.10 × 10⁻¹⁰:
- log₁₀(predicted) = −13.37
- log₁₀(observed) = −9.22
- **Shortfall: ~4 orders of magnitude (factor ≈ 14 400).**

Even the "naked" combination J · α_W⁵ · κ_sph (no Δκ/N_dof suppression, charitable upper bound) gives 2.77 × 10⁻¹¹, still ~22× short. This is the well-known KRS-1985 problem: CKM-CP alone is insufficient.

---

## 4. Verdict

**H3 is FALSIFIED in the QCD-T_c form** (sphalerons frozen out, exp(−10⁴) suppression).
**H3 is INSUFFICIENT in the EW-T form** even with an *ad hoc* dark sector contributing the full Δκ ≈ 0.16: still ~4 OM short. To reach 6.1 × 10⁻¹⁰ one would need either (i) δ_CP ≫ J (new CPV beyond CKM, e.g. dark-sector phase ~0.4 instead of 3 × 10⁻⁵), or (ii) f_sph enhanced by ~10⁴ at a strongly first-order PT (non-equilibrium burst), or (iii) Δκ × out-of-equilibrium factor much larger than dimensional estimate.

The crossover-jump mechanism is **dimensionally subdominant** to the standard EW-baryogenesis bottleneck. H3 does **not** explain η_B from first principles.

---

## 5. Relation to ECI exp(−21)

η_B,ECI = exp(−(b₂(K3) − 1)) = exp(−21) = 7.58 × 10⁻¹⁰  (24 % in linear, exact in log).

H3-EW gives log = −30.79; ECI exp(−21) gives log = −21.00; observed is −21.22.
**The gap between H3 and ECI is ≈ 9.8 e-folds.** Δκ/N_dof contributes log = −6.5 of that suppression. There is no natural way for the crossover formula to reproduce the integer "−21" appearing in the K3 cohomology count. The matches are **independent**: ECI exp(−21) is a topological/cohomological prediction, H3 is a kinetic/transport prediction; they share no derivable factor. The ECI win at 0.4 % log-accuracy is *not* re-derived by H3.

---

## 6. Refinement suggestions if H3 is to be salvaged

1. **Couple H3 to a strongly first-order EW PT** (extended Higgs sector). Replace f_sph by the bubble-wall non-equilibrium boost ~10⁴–10⁶ (Cline–Joyce reviews).
2. **Replace J by a dark-sector CPV phase** δ_dark ~ O(0.1), and let Δκ play the role of the diffusion-length×wall-velocity factor.
3. **Investigate whether the K3-Berry phase machinery already in ECI (project_eci_4_derivations_partielles, δ_CKM = π·√(2/15)) generates a CPV phase of order 1 in the dark sector**, which would then *kinematically* match exp(−21) ≈ 6 × 10⁻¹⁰ without H3 needing the sphaleron channel at all.
4. Most honest: **H3 and exp(−21) are different mechanisms**; exp(−21) lives in the geometric/topological foncteur; H3 lives in thermal QFT. Don't conflate.

---

## References (verified via /verify-arxiv pattern, classic pre-arXiv)

- F. R. Klinkhamer, N. S. Manton, *A Saddle-Point Solution in the Weinberg-Salam Theory*, Phys. Rev. D **30**, 2212 (1984).
- V. A. Kuzmin, V. A. Rubakov, M. E. Shaposhnikov, *On anomalous electroweak baryon-number non-conservation in the early universe*, Phys. Lett. B **155**, 36 (1985).
- G. D. Moore, *Sphaleron rate in the symmetric electroweak phase*, Phys. Rev. D **62**, 085011 (2000), arXiv:hep-ph/0001216.
- D. Bödeker, *On the effective dynamics of soft non-abelian gauge fields at finite temperature*, Phys. Lett. B **426**, 351 (1998), arXiv:hep-ph/9801430.

---

## Provenance of numbers

| Number | Source |
|---|---|
| κ_∞ = 0.6782 | ζ(3)/√π, ECI memory 2026-05-25 |
| κ_dilute(SU(3)) = 0.6028 | κ_∞·(1−1/9), perturbative law |
| κ_dense(SU(3)) = 0.4392 | √N extrap, NOT measured; suspect for N=3 |
| α_W = 0.034 | SM at M_Z |
| κ_sph ≈ 20 | Moore 2000 lattice |
| E_sph ≈ 9 TeV | Klinkhamer-Manton 1984 |
| J = 3.05 × 10⁻⁵ | PDG 2024 CKM Jarlskog |
| N_dof,SM = 106.75 | SM at T = 100 GeV |
| N_dof,QCD = 17.25 | quarks (u,d,s) + gluons + γ at T = 150 MeV |
| η_B,obs = (6.10 ± 0.04) × 10⁻¹⁰ | Planck 2018 TT,TE,EE+lowE+lensing |
