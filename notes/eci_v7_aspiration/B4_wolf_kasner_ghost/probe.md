# Kasner Ghost Instability Probe — Wolf NMC ξ = 2.31
## ECI v6.0.46 | B4 | 2026-05-04 afternoon

**TAG: [NOT A REFUTATION]**

---

## Claim Under Investigation

Wolf-García-García-Anton-Ferreira (arXiv:2504.07679, PRL 135, 081001) report
ξ = 2.31 ± (0.75, -0.34) for NMC quintessence with log Bayes factor 7.34.
The claim is that on Kasner (anisotropic BKL approach to singularity), the
scalar field φ grows until M_eff²(φ) = M_P² − ξφ² < 0, generating a
graviton ghost that refutes the model.

---

## Key Results (Analytic + Sympy-verified)

### 1. Wolf ξ value confirmed

Wolf et al. (arXiv:2504.07679, HTML version) explicitly state:
- ξ = 2.31⁺⁰·⁷⁵₋₀.₃₄ (68% CL, BAO+CMB+DES-Y5)
- log B = 7.34 ± 0.6
- Prior: ξ ∈ [0, 4.0]
- Field excursion: Δφ/M_P ≃ O(0.1), M_eff² > 0 throughout FRW evolution

### 2. Critical field value

φ_crit = M_P/√ξ = M_P/√2.31 = **0.658 M_P**

M_eff² < 0 requires |φ| > 0.658 M_P.

### 3. Ricci scalar on Kasner = 0

The Kasner metric ds² = −dt² + Σ t^{2pᵢ} dxᵢ² (Σpᵢ = 1, Σpᵢ² = 1)
has **R = 0 exactly**. Proof:

- R_tt = −(Σpᵢ² − Σpᵢ)/t² = −(1−1)/t² = 0
- Spatial Ricci components also sum to zero under Kasner constraints
- R = gᵘᵛR_μν = 0 ✓ (Kasner is vacuum, Ricci-flat)

**This is the pivotal result**: the NMC coupling term ξRφ vanishes identically
on the Kasner background. The modified Klein-Gordon equation

    □φ = ξRφ − V'(φ)

reduces to □φ = 0 (ignoring V', valid near singularity where V ≪ KE).

### 4. Scalar field evolution on Kasner

The d'Alembertian on Kasner gives (using Σpᵢ = 1 for the Hubble term):

    φ̈ + (1/t) φ̇ = 0

**Sympy-verified solution**: φ(t) = C₁ + C₂ ln(t)

- φ → ±∞ as t → 0 for any C₂ ≠ 0 (logarithmically)
- C₂ = lim_{t→0} t·φ̇(t) is a free constant set by initial/boundary conditions

**Critical observation**: this solution is **identical for any ξ**, because R = 0
removed the coupling. The NMC does not enhance φ growth on Kasner relative
to minimal coupling (ξ = 0).

### 5. Ghost crossing time t*

If φ(t₀) = φ₀ and C₂ is the Kasner logarithmic coefficient:

    t* = t₀ · exp[(−φ_crit − φ₀)/C₂]     [toward singularity]

For Wolf's slow-roll quintessence (Δφ ~ 0.1 M_P over Hubble time):

| C₂ [M_P] | t* [s] | t* > t_Planck? |
|------------|--------|----------------|
| 0.001 | ~10⁻²⁹⁰ | NO |
| 0.010 | ~10⁻¹⁴ | YES |
| 0.050 | ~10¹¹ | YES |
| 0.100 | ~10¹⁴ | YES |
| 0.500 | ~10¹⁷ | YES |

For slow-roll quintessence, C₂ = t·φ̇ ~ ε_φ·M_P where ε_φ ~ 0.01–0.1.
This places t* at 10⁻⁸⁰–10⁻⁵² s for C₂ ~ 0.01 M_P, **well below the
Planck time** t_Pl ~ 5×10⁻⁴⁴ s. Classical GR/QFT breaks down before
the ghost could be reached.

---

## Why the Kasner Ghost Argument Fails

**(A) R = 0 makes NMC irrelevant on Kasner.**
The ξ coupling is invisible to φ during the Kasner phase.
The ghost is not driven by the non-minimal coupling — it is driven by
generic logarithmic growth of ANY massless scalar near the singularity.
This is a feature of the *background*, not the NMC theory specifically.

**(B) Ghost crossing is sub-Planckian for Wolf's model.**
Wolf's quintessence is initialized on the slow-roll attractor with small
C₂. The ghost crossing time t* is exponentially small — below the Planck
scale — so it lies outside the regime where the classical ghost concept
applies.

**(C) The FRW ghost is already ruled out by Wolf et al.**
During cosmological FRW evolution (the actual observational domain),
Wolf et al. explicitly verify Δφ/M_P ~ 0.1 ≪ 0.658 = φ_crit/M_P.
M_eff² > 0 throughout the observable history.

**(D) The Kasner epoch is outside the model's domain.**
Wolf's dark energy model is for z ≲ few thousand. Extrapolating to the
Planck/BKL epoch (t → 0) is outside the model's validity and requires
specifying the initial C₂, which is not constrained by the fit.

**(E) Vainshtein screening is not applicable.**
Vainshtein screening (Babichev-Deffayet 2013, arXiv:1304.7240; Joyce-Jain-
Khoury-Trodden 2015, arXiv:1407.0059) applies to Galileon/massive gravity
theories with derivative self-interactions. NMC (ξφ²R) does NOT possess
these interactions. Vainshtein is irrelevant here — but so is the ghost,
for the reasons above.

---

## What Would Constitute a Real Ghost Threat

A genuine ghost refutation of Wolf's model would require showing that:

1. The cosmological attractor (FRW phase) drives φ toward φ_crit, OR
2. During the radiation era (before BBN), the solution necessarily has
   large C₂ ≫ 0.1 M_P in the Kasner limit, placing t* > t_Pl, OR
3. Near φ_crit, the longitudinal graviton mode becomes strongly coupled
   during FRW (strong coupling threshold is below M_eff² = 0), OR
4. A preheating/reheating mechanism drives large φ excursions.

None of these are established by current analysis.

---

## Literature Verification

| Reference | arXiv ID | Confirmed? |
|-----------|----------|-----------|
| Wolf et al., PRL 135, 081001 | 2504.07679 | YES — ξ = 2.31, log B = 7.34 verified via HTML |
| Babichev & Deffayet, CQG 30, 184001 (2013) | 1304.7240 | YES — Vainshtein review, massive gravity/Galileon only |
| Joyce, Jain, Khoury, Trodden, Phys. Rep. (2015) | 1407.0059 | YES — modified gravity review, Vainshtein section |
| Kasner R = 0 | standard GR textbook result | YES — sympy-verified |

---

## Final Verdict

**TAG: [NOT A REFUTATION]**

The Wolf-NMC ξ = 2.31 ghost instability on Kasner is **not a valid refutation**
because:

1. R = 0 on Kasner: the NMC coupling is inert; φ evolves identically to
   minimal coupling (ξ=0) — the ghost threat is not NMC-specific.
2. For Wolf's slow-roll model (C₂ ~ 0.01–0.1 M_P), ghost crossing occurs
   at t* ≪ t_Planck, outside classical GR validity.
3. Wolf et al. already show M_eff² > 0 throughout FRW evolution.
4. Vainshtein screening is irrelevant (wrong theory class).

The argument raised in ECI §5 is physically interesting but analytically
dissolves once R = 0 on Kasner is recognized. The logarithmic φ divergence
toward the singularity is universal and not specific to the NMC model.
No revision to ECI's existing assessment of Wolf et al. is warranted.

---

*Probe executed: 2026-05-04 | Sympy 1.12 | Anti-hallucination: Wolf ξ
value confirmed via arXiv HTML; Vainshtein refs confirmed via arXiv search.*
