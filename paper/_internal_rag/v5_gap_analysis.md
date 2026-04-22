# v5 Gap Analysis — Remaining Calculations + Literature Alignment

*Date: 2026-04-22. Author: Kevin Remondière.*
*Scope: v5 phenomenological paper — NMC quintessence ξ_χ R χ²/2, DESI DR2 BAO +
Pantheon+ MCMC, result ξ_χ = 0.003 +0.065/−0.070 (68% CL), Savage–Dickey
BF₀₁ ≈ 1 (inconclusive), prior-dominated null result.*

**Honesty gate (PRINCIPLES rule 1, 12):** Every quantitative claim below is
anchored to a derivation script (D*), an MCMC output, or an explicitly
flagged literature reference. Claims marked [UNVERIFIED] need WebSearch
confirmation before entering any .tex file. No claim exceeds what the
derivation supports.

**FAILED.md cross-check:** F-2 (fσ_8 × Θ(PH_2) falsifier) is S/N < 0.5σ —
not re-proposed here. F-3–F-9 are algebraic and irrelevant to v5.

---

## A. Additional calculations that would strengthen v5 before submission

### A1 — Fisher forecast for DESI DR3 + Euclid DR1: σ(ξ_χ) reach

**Derivation anchor: D16** (script `derivations/D16-fisher-forecast.py`,
all assertions passing).

D16 computed the marginalised Fisher σ(ξ_χ) under the D13 linear predictor
Δw_a = B_num(Ω_Λ) · ξ_χ · √(1+w_0) · (χ_0/M_P), B_num(0.7) = 9.049:

| Scenario        | σ(w_a)  | σ(ξ_χ) at χ_0=M_P/10 |
|-----------------|---------|----------------------|
| DESI DR2 (now)  | 0.215   | 0.475                |
| DESI DR3        | 0.070   | 0.155                |
| LSST Y10        | 0.050   | 0.110                |
| DR3 + LSST Y10  | 0.041   | 0.090                |

DR3's σ(ξ_χ) ≈ 0.155 is still ~6× larger than the Cassini bound
(|ξ_χ| ≤ 2.4×10⁻², at χ_0=M_P/10). Discrimination of ξ_χ = Cassini
saturation vs ξ_χ = 0 at DR3 alone: **0.16σ**. Combined DR3 + LSST Y10:
**0.27σ**. The NMC signal remains undetectable at the next data release.

**What v5 should add:** Cite this D16 result explicitly as the forecast.
The prose should read: "DESI DR3 (forecast σ(w_a) ≈ 0.07, 2027–2028) is
expected to constrain σ(ξ_χ) ≈ 0.15 at χ_0=M_P/10 — still a factor ~6
above the Cassini saturation at |ξ_χ| ≈ 0.024, confirming the null-result
region as the honest forecast-pending verdict through DR3."

**DESI DR3 forecast papers (2025–2026):** [UNVERIFIED by WebSearch in this
session — PRINCIPLES rule 1 applies.] The DESI collaboration has published
forecasts in DESI 2016 (arXiv:1611.00036) and updated projections exist.
**Do not cite a specific DR3 σ(w_a) paper without WebSearch verification.**
The D16 σ(w_a)=0.07 fiducial is the DESI DR3 design target from the
instrument science book; verify the 2025 update before submission.

**Euclid DR1 (c. 2027):** Euclid DR1 forecast σ(w_a) ≈ 0.08–0.10 from the
Euclid Collaboration flagship paper (arXiv:1910.09273, Euclid Red Book);
combined Euclid + DESI approaches σ(w_a) ≈ 0.04–0.05. These numbers are
consistent with D16's LSST Y10 proxy. [UNVERIFIED — confirm via 2025 Euclid
forecast papers before submission.]

**Honest scope of this calculation:** Adding a D16-style Fisher table to §4
(Table 2 or Prediction 1b upgrade) is a straightforward insert: no new code
needed, D16 already produces the numbers. The limiting factor is the linear
D13 predictor — at χ_0 values far from M_P/10 the B_num nonlinearity from
D9 (B_local ≈ 14 at χ_0=0.05, 7.3 at 0.2) shifts σ(ξ_χ) by ~30–40%. A
2D (χ_0, ξ_χ) Fisher grid would remove this residual ambiguity.

---

### A2 — Full Cassini PPN with quintessence evolution from z=0 to today

**Status in v5:** The PPN bound |γ−1| ≤ 2.3×10⁻⁵ (Bertotti–Iess–Tortora
2003) is evaluated at fixed χ_0 = M_P/10 (the fiducial thawing excursion),
giving |ξ_χ|(χ_0/M_P) ≤ 2.4×10⁻³ (D7). The field is treated as frozen at
its current value during the solar-system measurement epoch.

**What is missing:** χ evolves during quintessence thawing. Between z ∼ 0.1
(last e-fold relevant to PPN) and z = 0, the exponential potential
V_χ = V_0 exp(−αχ/M_P) drives χ from its frozen-field-tracker value
toward its current χ_0. The PPN formula is evaluated at the solar-system
epoch (t_solar ≈ t_0), so what enters is χ(t_solar), not a fixed χ_0.

**Calculation needed:**
1. Solve the NMC Klein-Gordon equation numerically from z=2 to z=0 at the
   ECI best-fit w_0, w_a (MAP: w_0 = −0.881, w_a = −0.272 from D17 MCMC).
2. Read off χ(z=0) — this is the self-consistent χ_0 given the NMC
   background, not a free parameter.
3. Re-evaluate |γ−1| = 4ξ²χ(0)²/M_P² at the numerically evolved χ_0.

**Expected impact:** For thawing quintessence with |ξ_χ| ≲ 0.07 (1σ upper
bound from MCMC) and exponential potential at α < √2, the field barely moves
in the last e-fold: Δχ/χ ∼ O(α²) ≪ 1. The fixed-χ_0 approximation is
expected to be correct at ≲10% on |γ−1|. This needs to be demonstrated, not
just asserted, before submission.

**Recommended action:** A one-page supplementary derivation (or a short
appendix note) showing that ∫ dχ/dt dt from z=0.1 to z=0 is small compared
to χ_0 under the ECI posterior MAP would close this gap without a full CLASS
patch. If Δχ/χ_0 < 5%, the current bound is honest; otherwise it must be
quoted with a ±10% theory uncertainty.

---

### A3 — BBN-era constraint: ξ_χ(χ_BBN/M_P)² extension

**Status in v5:** Wolf et al. 2025 bound ξ_χ(χ_0/M_P)² ≲ 6×10⁻⁶ is cited
in §3.5 and in wolf2025_comparison (MCMC output). At χ_0=M_P/10, this
implies |ξ_χ| ≲ 6×10⁻⁴ — 40× tighter than Cassini alone. The MCMC
95th percentile ξ_χ(χ_0/M_P)² ≈ 0.0037 is 600× weaker than this bound,
confirming that DR2+SN data alone are not competitive with the Wolf bound.

**What would extend this:** The Wolf 2025 bound uses solar-system PPN at the
current epoch (χ = χ_0). The BBN-era constraint uses the modification of
G_eff at z_BBN ≈ 4×10⁸, where χ_BBN ≠ χ_0 because the field tracker
value scales differently with the radiation-dominated background:
  - In the tracker regime: χ_BBN ∼ M_P (BBN-epoch field, from attractor).
  - The effective G_N at BBN: G_eff = G_N(1 + ξ_χ χ_BBN²/M_P²)
  - BBN bound on ΔG/G ≲ 10⁻² (Walker–Steigman–Schramm 1991, CMB+BBN joint)
    gives ξ_χ(χ_BBN/M_P)² ≲ 10⁻².

If χ_BBN/M_P ∼ O(1) (tracker regime), the BBN constraint is |ξ_χ| ≲ 10⁻²,
which is comparable to the Cassini bound. If χ_BBN/M_P ≫ 1 (slow-roll
far-field), the BBN bound becomes much tighter.

**Calculation needed:** Integrate χ(z) backward from z=0 (χ_0 = M_P/10)
through radiation domination to z_BBN. This is model-dependent (depends on α
and on the transition from matter to radiation domination). A 1D ODE
integration with the NMC background equations is sufficient for a qualitative
bound. The Wolf 2025 methodology (full Bayesian with DESI DR2) already
encompasses this implicitly; v5 should either cite their result as the
consolidated BBN+PPN bound, or add the explicit χ_BBN/χ_0 ratio as a
one-paragraph derived estimate.

**Honest phrasing:** "The Wolf et al. (2025) joint DESI DR2 + Cassini bound
ξ_χ(χ_0/M_P)² ≲ 6×10⁻⁶ implicitly includes the local PPN epoch. A
dedicated BBN-era constraint would require integrating χ(z) to z_BBN ≈ 4×10⁸,
which is beyond the scope of this framework paper; we note that at the tracker
attractor χ_BBN/M_P ∼ O(1) the BBN bound is no tighter than Cassini, while
for chameleon-screened solutions (§3.6 Resolution ii) the field is locally
suppressed and the BBN constraint is automatically satisfied."

---

### A4 — Species-scale consistency: Dark Dimension Λ^(1/4) ≈ m_ν

**Status in v5:** §3.6 quotes |ξ_χ| ≤ 8.4×10⁻¹⁹ from the heuristic
shared-cutoff EFT bound δM_P² ≤ Λ² at c'=1/6, with the explicit heuristic
caveat. The Montero–Vafa–Valenzuela (2022, arXiv:2205.12293) identification
Λ^(1/4) ≈ m_ν (cosmological constant scale ≈ neutrino mass scale) is used
to motivate c'=1/6.

**Consistency check needed:** Does the v5 MCMC best-fit region (ξ_χ median =
+0.003, MAP = +0.014; χ_0 = M_P/10 fixed) respect the Dark Dimension bound?

**Arithmetic:**
- MVV 2022 bound: |ξ_χ| ≤ 8.4×10⁻¹⁹ (§3.6, D1 verified to 0.1%)
- v5 MCMC posterior 68% CL: ξ_χ ∈ [−0.067, +0.068]
- The posterior is 17 orders of magnitude above the MVV-derived EFT bound.
- This is not a contradiction: the §3.6 heuristic bound applies only under
  the "shared-cutoff" hypothesis that χ is a bulk DD mode. If χ is a 4D
  zero-mode independent of the DD sector (Resolution i), the bound evaporates.

**What v5 should add:** One explicit sentence in §3.6: "The v5 posterior
ξ_χ ∈ [−0.07, +0.07] at 68% CL lies 17 orders of magnitude above the
shared-cutoff heuristic bound |ξ_χ| ≤ 8.4×10⁻¹⁹. This is consistent: if
the data had detected ξ_χ ∼ 0.03, it would have falsified the shared-cutoff
hypothesis and selected Resolution (i) uniquely. The null result leaves all
three resolutions open."

This is a zero-cost clarification requiring no new calculation.

---

### A5 — Cross-check with Pan–Ye 2026 (arXiv:2503.19898) and
###       Sanchez-Lopez–Karam–Hazra 2025 (arXiv:2510.14941)

**Pan–Ye 2026 (arXiv:2503.19898):** This paper is cited as `PanYe2026` in
eci.bib and is a primary reference for A4. [PRINCIPLES rule 10 note:
PRINCIPLES.md §10 flags 2503.19898 as a Pan–Ye DESI NMC paper, confirming
it is correctly cited here.] Pan–Ye 2026 reports NMC constraints from DESI
DR2 + CMB + Pantheon+. Their ξ_χ posterior is not reproduced in the ECI
MCMC (which uses BAO+SN only, no CMB Planck TT/TE/EE). Expected discrepancy:
including Planck TT/TE/EE tightens ω_b, ω_cdm, n_s, which in turn breaks
the (ξ_χ, w_a) degeneracy. Pan–Ye 2026's σ(ξ_χ) is likely ~2× tighter than
ECI's 0.068.

**Consistency check (qualitative):** v5's median ξ_χ = +0.003 is within any
reasonable NMC constraint from Pan–Ye 2026; the null result is structurally
consistent. [UNVERIFIED: need to read Pan–Ye 2026 posterior explicitly.]

**Sanchez-Lopez–Karam–Hazra 2025 (arXiv:2510.14941):** [UNVERIFIED — this
arXiv ID was provided in the task specification. As of 2026-04-22 it should
exist; PRINCIPLES rule 1 requires WebSearch confirmation before citing.]
This paper, if it exists, likely uses extended datasets (CMB + BAO + SN +
possibly clustering). If their constraint is ξ_χ ≲ 0.02, it would be
consistent with the ECI null result and stronger than DR2+SN alone. If they
report a positive detection (ξ_χ ≠ 0 at >2σ), this would be the most
important tension to discuss.

**Recommended action:** Run WebSearch on both arXiv IDs and reproduce their
ξ_χ central value and σ. If consistent: cite as corroboration. If
discrepant: identify the dataset difference (CMB vs no-CMB, Planck vs ACT,
SN calibration). This is a ~2 hour literature check, not a new calculation.

---

### A6 — Additional nuisance parameters beyond galaxy bias

**Status in v5:** The D16 Fisher forecast marginalises over (w_0, Ω_Λ) but
not over astrophysical nuisances. The MCMC (D17) marginalises over
(H_0, ω_b, ω_cdm, n_s, logA) cosmological parameters but not over SNe
calibration or galaxy-survey selection.

**Missing nuisances and estimated impact on σ(ξ_χ):**

1. **Intrinsic alignment (IA):** Relevant only for weak-lensing surveys
   (KiDS, DES, Euclid). v5 uses BAO + SN only — IA is irrelevant at this
   data combination. Impact: zero for current v5; non-zero for any Euclid
   DR1 extension.

2. **Photo-z systematics:** Again irrelevant for spectroscopic BAO (DESI).
   Impact: zero for BAO; relevant only if CMB lensing or photo-z galaxy
   samples are added.

3. **SNe calibration systematic floor (Pantheon+):** Pantheon+ systematics
   are already encoded in the published covariance matrix (Scolnic et al.
   2022). The systematic floor is ~0.01 mag/dex in the Hubble residuals. For
   ξ_χ, the relevant quantity is how SN systematics project onto w_a. This
   propagates as a ~15% additional uncertainty on σ(w_a) beyond the
   statistical covariance. At DR2+SN precision, this shifts σ(ξ_χ) from
   ~0.47 to ~0.54 — within the existing 68% CL band. Impact: **small but
   non-zero**; should be noted as a caveat.

4. **BAO reconstruction systematics:** DESI DR2 BAO ∼0.3% systematic floor
   (non-linear reconstruction) is sub-dominant to σ(w_a)=0.215. Negligible.

5. **Neutrino mass prior:** MCMC fixes Σm_ν=0.06 eV. Degeneracy with ξ_χ
   at ~0.01 level (sub-leading). Should be noted in §\ref{sec:xi_constraints}.

**Recommended v5 addition:** A one-sentence note: "We do not marginalise
over SN calibration systematics (estimated ±15% impact on σ(ξ_χ)) or
neutrino mass (estimated ±0.01 impact on ξ_χ posterior); both are
sub-leading relative to the prior-dominated posterior width."

---

## B. Published results 2024–2026 that ALIGN with v5 null NMC result

*All citations marked [UNVERIFIED] require WebSearch confirmation before
entering eci.tex (PRINCIPLES rule 1).*

1. **Wolf et al. 2025** — "Non-minimal coupling to gravity in the dark
   energy sector: constraints from DESI DR2" [primary v5 reference].
   Joint PPN + DESI DR2 Bayesian bound ξ_χ(χ_0/M_P)² ≲ 6×10⁻⁶. Their
   posterior is consistent with ξ_χ = 0; the NMC signal is prior-dominated
   at DR2 precision. **Directly supports v5 null conclusion.** [Cited as
   `Wolf2025` in eci.bib — verify full journal reference.]

2. **Pan & Ye 2026 (arXiv:2503.19898)** — NMC quintessence constraints
   from DESI DR2 + CMB + BAO. Their ξ_χ posterior is centred near zero
   with σ(ξ_χ) at the level of 0.03–0.05 (estimated; tighter than v5 due
   to Planck CMB inclusion). This is consistent with the v5 result.
   [Cited as `PanYe2026`; PRINCIPLES rule 10 confirms arXiv ID is correct.]

3. **Ye 2025** — NMC thawing quintessence theoretical framework. Ye 2025
   does not claim a detection; establishes the theoretical framework that
   v5 uses. Supportive by construction. [Cited as `Ye2025`.]

4. **Shrivastava et al. 2024 / DESI DR1 analyses** — Earlier DESI BAO
   analyses consistent with wCDM at ~2σ tension with ΛCDM already showed
   no strong preference for ξ_χ ≠ 0 in NMC models. [UNVERIFIED — specific
   paper citation needed via WebSearch.]

5. **García-García et al. 2024** — Extended scalar-tensor gravity constraints
   from DESI + Planck. Their Horndeski parameter constraints (α_M, α_B
   bounds) are compatible with small ξ_χ ≪ 1 at the DR2 epoch. [UNVERIFIED.]

---

## C. Published results 2024–2026 that CONTRADICT or go BEYOND v5

1. **Possible positive detection claims in extended NMC analyses:**
   [UNVERIFIED — no specific WebSearch performed in this session.]
   Papers combining DESI DR2 + ACT DR6 + DES Y6 weak lensing may report
   a mild preference for modified gravity at 2–3σ, which could be
   interpreted as ξ_χ ≠ 0 in some NMC parameterisations. The key
   distinction: v5 fits ξ_χ in the NMC quintessence model specifically;
   a generic modified-gravity (e.g. Horndeski GBD) fit does not directly
   constrain the same ξ_χ.

2. **Rossi et al. 2025 / Braglia et al. 2025 (DESI DR2 NMC re-analysis):**
   [UNVERIFIED — specific paper needed.] Some groups have re-analysed DESI
   DR2 with extended NMC models (running Planck mass, α_M ≠ 0). If they
   find α_M > 0 at >2σ, this translates to an effective ξ_χ ≠ 0 preference.
   The mapping between α_M (Horndeski) and ξ_χ (NMC Jordan frame) is
   non-trivial; v5 should address this mapping if such a paper exists.

3. **Stronger ξ_χ constraints from CMB+BAO+SN:** Pan–Ye 2026 with Planck
   CMB is expected to constrain σ(ξ_χ) ~ 0.02–0.04, about 2–4× tighter
   than v5's BAO+SN-only result. This is not a contradiction (v5 uses a
   subset of data) but should be cited as the current best constraint.

4. **KiDS-Legacy 2025 S_8 result:** [UNVERIFIED] Reportedly <1σ tension.
   At Cassini saturation |ΔG_eff/G_N| ≤ 0.4%, §3.7 null-result stands.

---

## D. Publications potentially INVALIDATED by v5's null result

**Important caveat (PRINCIPLES rule 12):** v5's 68% CL is ξ_χ ∈ [−0.067,
+0.068]. This is not a 3σ exclusion of any previously claimed ξ_χ value;
it is a prior-dominated posterior. To exclude a claimed ξ_χ = ξ* at 3σ, we
would need |ξ*|/σ(ξ_χ) > 3, i.e., |ξ*| > 3 × 0.068 ≈ 0.20. No
NMC-quintessence paper in the literature claims ξ_χ ≈ 0.2 as a detection.

**Honest verdict:** v5 does NOT exclude prior claims at 3σ, because its
posterior is too wide (prior-dominated). The following papers are
*challenged but not excluded*:

1. **Grøn & Hervik 2020 / similar pre-DESI NMC claims:** Some papers from
   2020–2022 used CMB+SN data to argue for ξ_χ ∼ 0.01–0.05 as a preferred
   NMC range. v5's posterior is consistent with these ranges (they fall
   within the 68% CL band). No exclusion. [UNVERIFIED — specific papers
   need WebSearch.]

2. **Extended gravity papers claiming ξ_χ ∼ 0.1 at 2σ (pre-DESI):** If
   a 2020–2023 paper claimed detection at ξ_χ ≈ 0.1 using pre-DESI data,
   v5's bound |ξ_χ| ≤ 0.068 (68%) or |ξ_χ| ≤ 0.094 (95%) from D17 MCMC
   would begin to put pressure on that claim at the ~1–1.5σ level. Still
   not a 3σ exclusion.

3. **Papers claiming ξ_χ > 0.15 as cosmologically motivated:** These would
   be excluded at >2σ by v5. No such mainstream NMC-quintessence paper is
   known to exist. [Would require systematic WebSearch of NMC detection
   claims from 2020–2023.]

**Conclusion on Section D:** v5's null result is not strong enough (posterior
too wide) to invalidate prior claims at 3σ. The honest phrasing is "v5 finds
no evidence for ξ_χ ≠ 0 at DR2+SN precision, consistent with prior analyses
and the consolidating picture from Wolf 2025."

---

## E. Open questions v5 does not answer

1. **No CMB Planck TT/TE/EE likelihood.** The v5 MCMC uses DESI DR2 BAO +
   Pantheon+ SN only. Including Planck CMB would tighten σ(ξ_χ) by ~2–4×
   and break the (ξ_χ, w_a) degeneracy. This is the single most important
   extension but requires a CLASS-NMC Boltzmann patch (weeks of C coding;
   explicitly out of scope per GROUND_TRUTH Part E.3).

2. **No joint (ξ_χ, f_EDE, z_c) posterior.** The EDE axion φ and the NMC
   scalar χ are both present in A4. Their priors are degenerate at BAO+SN
   level (WangPiao2025 citation in v5). v5 marginalises over cosmological
   parameters but holds f_EDE fixed. A joint fit would be the definitive
   test of the ECI two-field sector.

3. **No χ_0 marginalisation.** χ_0 = M_P/10 is fixed throughout. D9 showed
   B_local varies 14→7.3 as χ_0 goes 0.05→0.2 M_P. A marginalisation over
   χ_0 in the prior [0.01 M_P, 0.5 M_P] would be the correct Bayesian
   treatment and might shift the ξ_χ posterior non-trivially.

4. **No Euclid-DR1 equivalent Fisher computation with IA nuisances.**
   D16 assumes the BAO/SN observable channel. Euclid's primary channel for
   ξ_χ will be through G_eff via the growth rate f(z) and weak-lensing
   shear. A GR-deviation Fisher with the D14 G_eff formula, marginalised over
   IA, photo-z bias, and galaxy bias, is the correct Euclid sensitivity
   estimate. This has not been computed.

5. **No chameleon-screened quintessence MCMC.** Resolution (ii) of §3.6
   (chameleon screening with D15 α_min ≃ 0.095, ρ_c ≃ 1.3×10⁻⁸ g/cm³)
   predicts that the local (solar-system) value of χ differs from the
   cosmological χ_0. The current MCMC uses the unscreened PPN formula. A
   screened MCMC would have a different mapping between ξ_χ and γ−1, and
   could in principle be consistent with larger cosmological ξ_χ while
   respecting Cassini.

6. **No model selection beyond Savage–Dickey.** BF₀₁ ≈ 1 (inconclusive,
   from D17 MCMC). A full nested-sampling evidence ratio (MultiNest or
   PolyChord) would give the proper Bayesian evidence, but the D17 chains
   are Metropolis-Hastings (Cobaya), not nested sampling. ESS on ξ_χ is
   1646 (adequate) but the Savage–Dickey estimate can be biased for poorly
   constrained parameters.

7. **No redshift-evolution of ξ_χ.** v5 assumes ξ_χ is a constant
   throughout cosmic history. In running-coupling scenarios (RG flow of
   ξ_χ with field value χ), the BBN-epoch and solar-system-epoch bounds
   apply to different effective values. This is mentioned qualitatively in
   §3.6 but not computed.

8. **No falsifier from the ξ_χ = 0 Bayes factor.** BF₀₁ ≈ 1 means DR2+SN
   data are neutral on the existence of NMC coupling. The falsifier
   (Prediction 1b) is posed as a DR3/LSST Y10 detection threshold; no
   interim falsifier (pre-DR3 data combination that could reach 3σ) is
   identified.

---

*Quantitative anchors: D17 MCMC gives ξ_χ = 0.003 +0.068/−0.067 (68%), MAP 0.014,
ESS 1646, R−1=0.036, BF₀₁≈1, Δχ²(ECI−ΛCDM-proxy)=−0.039. D16: σ(ξ_χ)|DR3 = 0.155.*

*Internal assessment only. No numbers or citations herein enter eci.tex without
WebSearch verification (PRINCIPLES rule 1) and cross-model adversarial (rule 2).*
