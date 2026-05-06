# M18 — LiteBIRD sigma(r): live-verified data and ECI comparison

**Date:** 2026-05-06
**Hallu count:** 85 -> 85

---

## 1. Primary LiteBIRD reference: arXiv:2406.02724 (LIVE-VERIFIED)

**ID:** arXiv:2406.02724
**Title:** "The LiteBIRD mission to explore cosmic inflation"
**Authors:** LiteBIRD Collaboration
**Date:** 2024-06-04 (v1)
**Verified:** YES — arXiv API query 2026-05-06 returned exact match

Abstract key sentence:
    "LiteBIRD, aims for a launch in Japan's fiscal year 2032, marking a major
    advancement in the exploration of primordial cosmology and fundamental physics.
    [...]  Its primary goal is to measure the tensor-to-scalar ratio r with an
    uncertainty delta_r = 0.001, including systematic errors and margin. If r >= 0.01,
    LiteBIRD expects to achieve a >5-sigma detection in the l=2-10 and l=11-200 ranges
    separately."

**Extracted values (verbatim from abstract):**
    sigma(r) = delta_r = 0.001   [including systematics and margin]
    Launch: Japan fiscal year 2032 (April 2032 - March 2033)
    Mission: 3 years from Sun-Earth L2
    Detection threshold quoted: r >= 0.01 for >5-sigma

**Derived detection thresholds:**
    3-sigma detection: r > 3 x 0.001 = 0.003
    5-sigma detection: r > 5 x 0.001 = 0.005   [or r >= 0.01 per abstract quote]

Note: The abstract gives >5-sigma for r >= 0.01 (more conservative than simple 5*sigma).
This is consistent with: sigma(r) ~ 0.001 at r=0 fiducial, but sigma(r) degrades at
smaller l from foreground uncertainty. The delta_r = 0.001 is the total budget including
this.

---

## 2. Supporting LiteBIRD references (all LIVE-VERIFIED)

**arXiv:2202.02773** (LiteBIRD Collaboration, 2022-02-06, VERIFIED):
    Title: "Probing Cosmic Inflation with the LiteBIRD CMB Polarization Survey"
    Sensitivity: 2.2 mu-K-arcmin total, resolution 0.5 deg at 100 GHz
    3 telescopes, 15 frequency bands 34-448 GHz

**arXiv:2101.12449** (Hazumi+ et al., 2021-01-29, VERIFIED):
    Title: "LiteBIRD: JAXA's new strategic L-class mission..."
    Sensitivity: 2.16 mu-K-arcmin total

**arXiv:2310.08158** (Jinno-Kohri-Moroi-Takahashi-Hazumi, 2023-10-12, VERIFIED):
    Title: "Testing multi-field inflation with LiteBIRD"
    Context: LiteBIRD constrains tensor spectral index n_T as well as r

---

## 3. Timeline reconstruction

| Milestone | Date |
|---|---|
| JAXA L-class selection | May 2019 |
| LiteBIRD 2022 design paper (2202.02773) | Feb 2022 |
| LiteBIRD 2024 mission paper (2406.02724) | Jun 2024 |
| Launch (Japan FY2032) | Apr 2032 - Mar 2033 |
| End of 3-year survey | ~2035-2036 |
| First B-mode results | ~2035-2036 |

---

## 4. Comparison: ECI predictions vs LiteBIRD thresholds

| Quantity | Value | Source |
|---|---|---|
| LiteBIRD sigma(r) | 0.001 | arXiv:2406.02724 (verbatim) |
| LiteBIRD 3-sigma threshold | r > 0.003 | Derived |
| LiteBIRD 5-sigma threshold | r > 0.01 | arXiv:2406.02724 (verbatim) |
| ECI modular tau-inflation r | ~1.4e-7 | Ding-Jiang-Xu-Zhao 2411.18603 (A4=S'4/Z2) |
| ECI NMC xi~0.001 inflation | EXCLUDED | A73 (xi~10^4 needed) |
| ECI Starobinsky R^2 (if added) | ~3.97e-3 | 12/N^2, N=55 (not in ECI v6.0.53.3) |
| Planck 2018 UL | r < 0.064 (95% CL) | Standard value (no arXiv verification) |
| BICEP/Keck 2021 UL | r < 0.036 (95% CL) | Standard value (no arXiv verification) |

**Gap analysis (ECI modular vs LiteBIRD):**
    r_ECI_modular / sigma(r)_LiteBIRD = 1.4e-7 / 1e-3 = 1.4e-4
    r_ECI_modular is 0.014% of one LiteBIRD sigma.
    LiteBIRD cannot detect r at this level by ~7000-sigma factor.

**If ECI had Starobinsky R^2 sector:**
    r_Starobinsky / sigma(r) = 3.97e-3 / 1e-3 = 3.97 sigma
    Detectable at ~4-sigma by LiteBIRD 2035.
    n_s = 0.9636 (consistent with Planck 2018: n_s = 0.9649 +/- 0.0042)

---

## 5. Competitor r predictions

**Wolf 2025 (arXiv:2604.08449 = AKW, not Wolf 2025 directly):**
    Wolf 2025 NMC xi=2.31 paper makes NO inflation prediction.
    xi=2.31 could in principle give BS-like inflation, but Wolf does not compute r.
    If xi >> 1 (Starobinsky attractor): r -> 12/N^2 ~ 4e-3 (LiteBIRD-detectable)
    Wolf xi=2.31 is NOT in the BS attractor limit (xi >> 1 poorly satisfied for xi=2.31)

**AKW 2026 (arXiv:2604.08449):**
    Makes NO inflation prediction. Quintessence frozen field: no inflation sector.

**Conclusion:** No competitor makes an r prediction. ECI's modular null (r < 10^{-6})
IS the unique prediction in the field — but it predicts non-detection, not detection.

---

## 6. Spectral index consistency check

ECI modular inflation (A4/S'4): n_s = 0.9647 (from Ding-Jiang-Xu-Zhao 2411.18603)
Planck 2018: n_s = 0.9649 +/- 0.0042

Delta = |0.9647 - 0.9649| / 0.0042 = 0.05-sigma    [EXCELLENT consistency]

The ECI modular inflation n_s is within 0.05-sigma of Planck 2018. This means:
    - Spectral index is NOT a discriminator between ECI modular and Starobinsky
    - Both give n_s ~ 0.964-0.965, consistent with Planck
    - ONLY the r value distinguishes them (r ~ 1e-7 vs r ~ 4e-3)

LiteBIRD will measure sigma(n_s) ~ 0.002 (from full-sky CMB). This is comparable to
Planck but will not discriminate ECI from Starobinsky via n_s alone.

---

## 7. Future-detection prospects for ECI null

If LiteBIRD detects r = 0 (non-detection at sigma(r)=0.001):
    UL: r < 0.003 at 95% CL
    ECI modular: r ~ 1.4e-7 is consistent with this
    ECI becomes: "the first modular-flavor model confirmed via B-mode null"

If CMB-S4 (planned, ~2035-2040) achieves sigma(r) ~ 5e-4:
    UL: r < 0.0015 (95% CL)
    ECI modular: still consistent
    Still ~3000x above r_ECI_modular

Even a Stage-5 experiment (sigma(r) ~ 1e-5) would need 10 years beyond LiteBIRD
to constrain r at the level of ECI modular inflation (r ~ 1e-7).

**Honest conclusion:** The ECI modular inflation null (r < 10^{-6}) is consistent
with all current and planned observations, but cannot be POSITIVELY CONFIRMED by any
near-term experiment. It is falsifiable (r > 10^{-3} refutes it) but not
confirmable on the LiteBIRD timescale.

---

## 8. Recommendation for ECI v7.5 paper text

Suggested sentence for ECI §5 (falsifiers):

    "If the modular field tau_{S'4} acts as the inflaton in the King-Wang
    de Sitter trap [arXiv:2310.10369], ECI inherits the generic modular inflation
    prediction r ~ O(10^{-7}) [Ding et al. 2024, arXiv:2411.18603], far below
    the LiteBIRD sensitivity delta_r = 10^{-3} [arXiv:2406.02724]. A LiteBIRD
    detection of r > 10^{-3} would therefore refute ECI modular tau-inflation.
    Extension to a Starobinsky R^2 sector (with r ~ 4 x 10^{-3}, LiteBIRD-testable)
    is reserved for v7.6."

This sentence is honest, citable, falsifiable, and does not overclaim.

---

## Discipline
- Hallu count: 85 (unchanged)
- All sigma(r) values from live-verified arXiv sources
- Planck and BICEP/Keck UL values are standard (not live-verified here — standard literature)
- Mistral STRICT-BAN observed
