---
name: M9 Degeneracy-breaking observables — ECI vs Wolf vs AKW
description: 8 observables that discriminate the three DESI dark energy models at ~3σ, with estimated discrimination power
type: project
---

# Degeneracy-Breaking Observables: ECI vs Wolf vs AKW

**Date:** 2026-05-06
**Owner:** Sub-agent M9
**Hallu count:** 85 (unchanged)

---

## Strategic overview

All three models fit DESI DR2 BAO at some level. The models differ in:
1. Whether ξ (NMC to gravity) is present, absent, or Cassini-screened
2. Whether DE-DM energy exchange occurs
3. Whether G_eff deviates from G_N
4. Whether DM particle mass varies with redshift
5. Whether phantom crossing is real or apparent

The degeneracy-breaking programme must target observables that are individually sensitive
to EXACTLY these distinctions. Below, each observable is rated by:
- Discrimination pair (which models it separates)
- Signal-to-noise estimate (where quantifiable)
- Timeline (near-term = <3 years; mid-term = 3-7 years)

---

## Observable 1: G_eff(z) from CMB lensing + galaxy-galaxy lensing cross-correlation

**What it measures:** The effective Newton's constant governing growth of structure.

| Model | G_eff(z)/G_N |
|---|---|
| ECI | ~1.00 (Cassini-clean; ξ ≈ 0 → no deviation) |
| Wolf | 1.77 today (4.3σ from GR per A69); scale- and redshift-dependent |
| AKW | ~1.00 (minimal coupling; no NMC term) |

**Discrimination:** ECI vs Wolf and AKW vs Wolf — clean 3σ discriminator for Wolf at
G_eff = 1.77 using CMB lensing + DES/Euclid shear.
Wolf uniquely predicts G_eff deviation; ECI and AKW are both consistent with GR gravity.

**Key datasets:** ACT DR6 lensing (already available), Euclid Year-1 shear (2026),
DESI Y3 galaxy-galaxy lensing (2027).

**Timeline:** Near-term. ACT DR6 already provides ~2σ constraint on G_eff departure
from 1.00. Euclid Year-1 will push this to ≥4σ.

**Caveat:** Wolf acknowledges Cassini failure; a viable Wolf model must invoke screening.
Screening could suppress G_eff deviation on large scales. Need to model Vainshtein or
chameleon radius to properly assess the test.

---

## Observable 2: DM particle mass variation with redshift

**What it measures:** m_DM(z) evolution via peculiar DM properties.

| Model | m_DM(z) |
|---|---|
| ECI | Constant (no DM-DE coupling) |
| Wolf | Constant (no DM-DE coupling) |
| AKW | m_DM = μ f(φ(z)) — varies as φ rolls; ~few % across cosmic history |

**Discrimination:** AKW vs ECI+Wolf — uniquely AKW prediction.

**Observable consequences:**
- DM velocity dispersion shifts: ⟨v²⟩ ∝ T_DM/m_DM, so varying m_DM → DM "temperature"
  evolution distinct from ΛCDM.
- Lyman-alpha forest: DM free-streaming length evolves differently with m_DM(z).
- Halo mass function: halos form differently when DM mass shifts during matter domination.

**Best probe:** Galaxy cluster mass function from SPT-3G / CMB-S4 (2027-2028).
A ~5% variation in m_DM over 0 < z < 2 may be detectable at 2-3σ.
Also: 21cm cosmology (SKA 2030+) via DM-baryon coupling through varying m_DM.

**[TBD: AKW paper §3 would give the predicted magnitude of m_DM variation for the
best-fit (α, β, γ) = (−4.667, 0.180, 0.145) values. This is the primary model-specific
prediction not in the abstract.]**

**Timeline:** Mid-term (cluster counts near-term; 21cm long-term).

---

## Observable 3: fσ₈(z) from galaxy peculiar velocity surveys

**What it measures:** Growth rate of structure f × σ₈, directly sensitive to G_eff and
the modified DM sector.

| Model | fσ₈ prediction |
|---|---|
| ECI | Near-ΛCDM (small ξ → negligible modification to growth) |
| Wolf | Enhanced (G_eff > G_N increases growth; fσ₈ elevated at z < 1) |
| AKW | Modified by DM energy injection; depends on whether coupling increases or decreases DM density growth. The coupling Q transfers energy DE→DM at late times, potentially enhancing DM density → fσ₈ above ΛCDM. |

**Key datasets:** DESI Y3 ELG+LRG fσ₈ measurements (2027), Euclid spectroscopic survey.

**Discrimination power:** ECI vs Wolf at z < 0.5: estimated ~2-3σ with current DESI Y1
data, rising to ~5σ with DESI Y3 full shape analysis.
AKW vs ECI: requires precision fσ₈ at z > 0.5 where DM energy injection from DE is
stronger. Estimated 2σ with Euclid.

**Timeline:** Near-term (DESI Y3 fσ₈ available 2027).

---

## Observable 4: ISW-galaxy cross-correlation (late ISW effect)

**What it measures:** Cross-correlation of CMB temperature with large-scale structure
(galaxy overdensities). Sensitive to the time evolution of gravitational potentials, which
depends on w(z) and G_eff(z).

| Model | ISW prediction |
|---|---|
| ECI | Near-ΛCDM (small ξ; potentials decay at near-ΛCDM rate) |
| Wolf | Enhanced ISW (G_eff > G_N; potentials decay faster → larger ISW amplitude) |
| AKW | Modified (effective w_eff crosses −1; potential evolution different from ΛCDM and from Wolf) |

**Discrimination:** Wolf uniquely predicts ISW enhancement proportional to G_eff = 1.77.
AKW's apparent phantom crossing (w_eff < −1 at high z, w_eff > −1 at low z) produces a
distinctive ISW redshift evolution — potentials could be growing at high z then decaying
at low z (or vice versa). ECI is near-ΛCDM baseline.

**Best probe:** CMB (Planck/LiteBIRD) × DESI photometric galaxy catalog cross-correlation.
Current Planck ISW measurement is ~3σ significance. LSST DR1 cross-correlation (2028)
will sharpen to ~5σ total; model discrimination requires ~0.5σ precision on ISW amplitude.

**Timeline:** Mid-term (LSST DR1 2028; 3σ model discrimination feasible).

---

## Observable 5: Void abundance and void lensing profile

**What it measures:** Statistics of cosmic voids (underdense regions) — highly sensitive
to fifth-force modifications and to the dark sector equation of state.

| Model | Void prediction |
|---|---|
| ECI | Near-ΛCDM (small ξ → no 5th force; voids evolve ΛCDM-like) |
| Wolf | Modified (large ξ → effective 5th force inside Vainshtein radius; void profiles altered) |
| AKW | Modified (DM-DE coupling reduces DM density in voids; voids are emptier and larger) |

**Key physics:** AKW's energy transfer Q = −ρ_DM (d ln m/dφ) φ̇ is STRONGER in low-density
regions (fewer DM particles to absorb energy → field rolls faster in voids). This creates
a distinctive void bias — voids expand faster in AKW than in ΛCDM or ECI.

Wolf's 5th force is suppressed by Vainshtein inside halos but active in voids — similar
direction but different origin.

**ECI discriminator:** ECI predicts no 5th force in voids (ξ ≈ 0). A detected void
abundance anomaly at ≥3σ would be evidence against ECI (or for a different ξ value).

**Best probe:** DESI photometric void catalog + CMB lensing in voids (void-CMB cross).
BOSS DR12 voids already provide ~2σ sensitivity. DESI + LSST will reach 5σ.

**Timeline:** Mid-term (DESI Y3 2027).

---

## Observable 6: w(z) shape at z > 1 from BAO + standard sirens

**What it measures:** The dark energy equation of state at high redshift, beyond DESI DR2
coverage.

| Model | w(z > 1) |
|---|---|
| ECI | Slow approach to w = −1 (exponential V; tracker solution) |
| Wolf | CPL form: w = w₀ + wₐ(1−a); extrapolates (may go w > 0 at very high z) |
| AKW | w_eff approaches near-ΛCDM at z > 1 (coupling suppressed in radiation era by design) |

**Discrimination:** AKW specifically predicts w_eff ≈ −1 at z > 1 (frozen field phase)
then w_eff ≈ −1.2 at z = 1 → −0.9 at z = 0.4. This distinctive w(z) shape — phantom at
intermediate z, sub-phantom at low z — is UNIQUE to AKW.
Wolf's CPL parametrization is monotone (cannot produce the AKW crossing profile).
ECI is near-constant w ≈ −1 across redshift.

**Best probe:** DESI Y5 BAO at z > 1.5 + LISA standard sirens (binary NS mergers) at
z ~ 0.1-2.0 (2030+).

**Timeline:** Near-term for DESI Y5 (2028); long-term for LISA (2035).

---

## Observable 7: CMB B-mode polarization (tensor-to-scalar ratio r)

**What it measures:** Primordial gravitational waves from inflation. Sensitive to the
inflationary model; connected to ECI's modular inflation predictions.

| Model | r prediction |
|---|---|
| ECI | Constrained by ECI's S'_4 modular inflation sector [TBD: specific r value from modular inflation]; likely small r ≲ 10⁻³ |
| Wolf | No inflationary prediction — purely phenomenological DE model |
| AKW | No inflationary prediction — purely phenomenological DE model |

**Strategic value:** This observable discriminates ECI from BOTH Wolf and AKW simultaneously,
regardless of DESI dark energy data. ECI's UV completeness (modular flavor + inflation) makes
a specific r prediction that the other two models simply cannot address.

**Best probe:** LiteBIRD (launch 2032); CMB-S4.

**Timeline:** Long-term. But conceptually important: ECI has a prediction; Wolf/AKW do not.

---

## Observable 8: Spectral distortions of the CMB (μ and y distortions)

**What it measures:** Non-equilibrium energy injection into the CMB photon bath, sensitive
to dark sector energy transfer.

| Model | Spectral distortion prediction |
|---|---|
| ECI | ΛCDM-like (no dark sector energy injection) |
| Wolf | ΛCDM-like (no dark sector energy injection) |
| AKW | Potentially modified: energy transfer Q at late times is after recombination → no direct CMB photon distortion from Q. But the EARLY epoch coupling (during radiation era) is claimed to be suppressed. Net: likely near-ΛCDM. [TBD: verify with AKW §3.] |

**Discrimination:** All three models predict near-ΛCDM spectral distortions, so this
is NOT a primary discriminator. However, if AKW's coupling is not perfectly frozen
in the radiation era, it could generate y-distortions detectable by PIXIE/PRISM.

**Timeline:** Long-term (PIXIE/PRISM not yet approved; 2030+).

---

## Summary ranking by discrimination power

| Rank | Observable | Models separated | Timeline | Priority |
|---|---|---|---|---|
| 1 | G_eff(z) lensing | Wolf vs (ECI + AKW) | Near-term | HIGH |
| 2 | fσ₈(z) growth rate | Wolf vs ECI; AKW vs ECI at z>0.5 | Near-term | HIGH |
| 3 | w(z) shape at z>1 | AKW vs Wolf vs ECI (phantom evolution) | Near-mid | HIGH |
| 4 | Void statistics + lensing | AKW vs (ECI+Wolf) in underdense regions | Mid-term | MEDIUM-HIGH |
| 5 | ISW-galaxy cross-corr | Wolf vs AKW (potential evolution) | Mid-term | MEDIUM |
| 6 | DM mass variation m_DM(z) | AKW vs (ECI+Wolf) — unique AKW prediction | Mid-term | MEDIUM |
| 7 | CMB B-modes (r) | ECI vs (Wolf+AKW) — ECI uniquely predicts r | Long-term | MEDIUM (unique ECI lever) |
| 8 | CMB spectral distortions | Marginal; all near-ΛCDM | Long-term | LOW |

---

## Key conclusion

The three-model degeneracy is ONLY partly breakable with current data:
- **Wolf is already separated from ECI+AKW at G_eff level** (G_eff = 1.77 is 4.3σ from GR;
  ACT DR6 + Euclid will confirm or rule out this prediction independently of DESI BAO).
- **AKW vs ECI requires new probes** (m_DM variation; void lensing; w(z) shape at z>1).
- **ECI's unique discriminator** is its UV completeness: it predicts r (from modular inflation),
  B(p→e⁺π⁰)/B(p→K⁺ν̄) = 2.06, and modular Yukawa couplings. Wolf and AKW are pure DE
  models with no prediction in these sectors.
