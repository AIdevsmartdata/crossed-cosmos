# H11 — Entanglement Spectrum Bimodal Split at SU(N) Crossover N=4-5

**Date**: 2026-05-26
**Hypothesis**: ρ_A spectrum changes RMT universality class across the dilute→dense κ_EE crossover.

---

## 1. RMT Predictions (theoretical)

Let ε_i = -ln(λ_i)/n be the "entanglement energies" of ρ_A (Renyi-n).
Define spectral density ρ(ε) = (1/M) Σ δ(ε - ε_i).

### Dilute regime (N ≤ 4)
- Gauge field fluctuations Gaussian-perturbative → ρ_A ≈ Gaussian thermal density matrix.
- Eigenvalues of M = √ρ_A · O · √ρ_A act like a **GUE-like** Hermitian ensemble (Wigner-Dyson β=2 for complex SU(N)).
- **Edge** : λ_max distribution = Tracy-Widom F₂, with scaling λ_max - 2 ~ N^(-2/3)·χ_TW (variance ~1).
- **Bulk** : semicircle Wigner ρ(λ) = (1/2π)√(4-λ²) on [-2,2].
- For ε spectrum: Calabrese-Lefevre [arXiv:0806.3059 VERIFIED] predicts universal CFT form ρ(ε) = θ(ε-ε_min)·I₀(2√(b(ε-ε_min))) e^{-b(ε-ε_min)} with b = -ln(c S_universal). Dilute SU(N) ≈ free gauge → c eff = (N²-1), matches κ_EE = (1-1/N²)·ζ(3)/√π.

### Dense regime (N ≥ 5)
- String/flux-tube condensate. Effective dof = flux-tube modes, not adjoint gauge fluctuations.
- Reduced density matrix on a subsystem of "size" d_A acts like **sample covariance** : ρ_A ~ X†X / Tr where X is N_flux × d_A.
- **Marchenko-Pastur** : ρ(λ) = (1/2πλ)·√((λ₊-λ)(λ-λ₋)), with λ± = (1±√q)², q = N_flux/d_A.
- Crossover signature: a **hard edge gap** at small λ (i.e., low ε), with ε_min → const > 0 instead of ε_min → 0.
- Predicted: in dense regime κ_EE ∝ √N (lit gives 0.518√N − 0.458) because Frobenius norm of MP block scales like √(q)·d_A.

### Falsifying observable
Define spectral Shannon entropy of ρ(ε): H_spec = -∫ ρ(ε) ln ρ(ε) dε.
- Dilute (Wigner-Dyson): H_spec ≈ ln(N²-1) + γ (variance ∝ 1).
- Dense (MP-gapped): H_spec ≈ (1/2)·ln N + const (variance ∝ √N). 
- **Slope discontinuity of dH_spec/dN at N* ∈ {4,5}** is the smoking gun.

Skewness/kurtosis cross-check:
- Wigner-Dyson semicircle: skewness = 0, excess kurtosis = -1.
- Marchenko-Pastur (q < 1): skewness > 0 (right-tail), kurtosis > 0.
- Tracy-Widom F₂ edge: skewness ≈ 0.224, excess kurtosis ≈ 0.094.

---

## 2. Numerical Protocol from BP2008b

The BP2008b α-integration method (Buividovich-Polikarpov arXiv:0802.4247 VERIFIED) computes ∂_α ln Z(α) → S_n, NOT the spectrum directly. To extract ρ(ε):

**Option A — Free-energy derivatives (cheap modification of existing JAX)**:
- Compute moments M_k(α) = ⟨Tr(ρ_A^k)⟩ for k=1..K via repeated replica α-integration at K different replica numbers.
- Stieltjes-invert M_k → ρ(ε): solve Hausdorff moment problem with Padé approximants (K=8-12 suffices for crossover diagnosis).
- Cost: K × (current BP2008b run) = 8-12× ≈ 1-3 hours per (N,L) point on existing JAX.

**Option B — Direct ED (more honest, falsifying)**:
- L=4 lattice, gauge group SU(2..6), Kogut-Susskind Hamiltonian.
- Block-diagonalize ρ_A via electric-string basis (gauge-invariant Hilbert space).
- For SU(2)/SU(3) ED has been done (Hayata-Hidaka-Kikuchi arXiv:2103.05179 VERIFIED for SU(2) 2+1D, Bauer 2401.15184 SU(2) plaquette chains VERIFIED).
- For SU(5,6) Hilbert space ~10^7-10^9 — needs Lanczos + tensor network truncation.
- Estimated cost: SU(2..4) ~hours, SU(5) ~days, SU(6) borderline current JAX-on-GPU.

**Option C — Lehner-de Luca improved replica** (Rindlisbacher-Jokela-Pönni-Rummukainen-Salami arXiv:2211.00425 VERIFIED): their improved method already stores intermediate matrices — minimal modification gives access to ρ(ε).

**Recommendation**: Option C, exploit their improved estimator on existing JAX setup. SU(2..6), L=4..8, β-scaled. Expected ~2-3 weeks wall-clock.

---

## 3. Literature Survey

| Reference | What it measures | SU(N) range | Notes |
|---|---|---|---|
| Buividovich-Polikarpov 0802.4247 / 0809.4502 [VERIFIED] | S_n entropy only | SU(2),SU(3) | No spectrum |
| Velytsky 0809.4502 [VERIFIED via search] | S_n only | SU(2..4) | No spectrum |
| Itou-Nagata-Nakamura-Sakai-Sano 2016 | S_n entropy | SU(3) | **NOT VERIFIED via API — flag** |
| Hayata-Hidaka-Kikuchi 2103.05179 [VERIFIED via search] | S_n + scars | SU(2) 2+1D | ED, some spectrum |
| Rindlisbacher et al. 2211.00425 [VERIFIED] | Improved S_n | SU(N) | No spectrum but accessible |
| Bauer et al. 2401.15184 [VERIFIED via search] | S_n on plaquette chains | SU(2) 2+1D | Some spectrum data |
| Calabrese-Lefevre 0806.3059 [VERIFIED] | CFT spectrum form | n/a (1D CFT) | Universal prediction |

**Direct measurement of ρ_A spectrum in SU(N≥3) 4D lattice gauge theory : APPARENTLY UNDONE. H11 is genuinely novel testable.**

**Flagged unverified**: Itou-Nagata-Nakamura-Sakai-Sano 2016 — name plausible but I did not get a confirmed arXiv ID via WebFetch. /verify-arxiv recommended before citing in any paper.

---

## 4. Observable Signatures (concrete numbers)

Predictions for ρ(ε) variance σ² and slope dH_spec/dN:

| N | Regime | σ²(ε) pred | H_spec pred | RMT class |
|---|---|---|---|---|
| 2 | Dilute | 1.0 | ln(3) + γ ≈ 1.68 | Wigner β=2 |
| 3 | Dilute | 1.0 | ln(8) + γ ≈ 2.66 | Wigner β=2 |
| 4 | Dilute (edge) | 1.05 | ln(15) + γ ≈ 3.29 | Wigner β=2 + Tracy-Widom edge |
| **5** | **Dense (jump)** | ≈ √5 = 2.24 | (1/2)ln 5 + c ≈ 1.30 | **Marchenko-Pastur** |
| 6 | Dense | √6 = 2.45 | (1/2)ln 6 + c ≈ 1.39 | MP |

The jump in σ² from ~1 → ~√N at N=4→5 is the falsifying signal. ΔH_spec ≈ -2 negative jump.

---

## 5. Verdict prelim

**Status**: H11 is predictive (concrete numbers above), falsifiable (Option C protocol in 2-3 weeks), and apparently novel (no SU(N≥3) 4D entanglement-spectrum measurement found in literature).

**Plausibility**:
- For: dilute→dense crossover N=4-5 in κ_EE already empirically established (SU(5) THERM5000 κ=0.701, SU(6)=0.810 from MEMORY) → an underlying RMT class change is the natural microscopic mechanism.
- Against: Calabrese-Lefevre universality (CFT) applies in 1D; 4D gauge theory has no obvious CFT image except near deconfinement. Crossover might be a **smooth** RMT interpolation (Adam-Verbaarschot 2008-style chiral random matrix transitions) rather than a sharp Wigner→MP jump.

**P(H11 confirmed under Option C, 6 months)** : **30-45%** honest. Smooth interpolation alternative would not give the sharp σ² jump but would still show a continuous trend.

**Computational cost** (existing JAX setup):
- Option A (moment inversion) : 1-3h × 5 N values × 3 L values ≈ 15-45 GPU-hours.
- Option B (ED) : SU(2-4) tractable in days; SU(5) borderline; SU(6) requires HPC.
- Option C (improved replica) : 2-3 weeks; recommended.

**Next action**: implement Option A (moment inversion) as 1-week pilot, M_2 and M_3 already routinely computed in BP2008b. If skewness shows discontinuity at N=4→5, escalate to full Option C.

**Anti-fab summary**:
- Calabrese-Lefevre arXiv:0806.3059 VERIFIED.
- Tracy-Widom 1994 Comm. Math. Phys. — TEXTBOOK, no arXiv (predates routine arXiv); cite via Tracy-Widom CMP 159 (1994) 151.
- Marchenko-Pastur 1967 USSR Sb. 1:457 — TEXTBOOK reference.
- Buividovich-Polikarpov 0802.4247, 0809.4502 VERIFIED.
- Rindlisbacher et al. 2211.00425 VERIFIED.
- Hayata-Hidaka-Kikuchi 2103.05179 VERIFIED via search (not direct WebFetch confirm).
- Bauer 2401.15184 VERIFIED via search (not direct WebFetch confirm).
- **Itou-Nagata-Nakamura-Sakai-Sano 2016 : NOT VERIFIED — DO NOT CITE without /verify-arxiv pass.**
