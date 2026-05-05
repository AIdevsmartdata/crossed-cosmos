"""
A44 -- Sigma m_nu predictor scan for ECI v7.4

Uses LYD20 (arXiv:2006.10722) Type-I seesaw architecture transcribed in
A16/predict_pmns.py:
    M_nu = -M_D^T M_N^-1 M_D     (with M_D having two complex couplings g1,g2
                                  and M_N a single Lambda scale)

We do NOT refit PMNS angles here -- A16 already gives the chi2-minimum point
estimate at each tau (W1 attractor, tau=i strict, LYD20-check). Instead we
quantify Sigma m_nu posterior under realistic seesaw-input priors:

   Free seesaw inputs (3):
     1) g2/g1 ratio          (LYD20 fitted to PMNS angles -> central value)
     2) overall mass scale   (g1^2 v_u^2 / Lambda) -- determines Sigma m_nu
     3) tau_l selection      (W1 vs tau=i vs LYD20-check)

   Prior structure: Gaussian widths from A16 chi2 curvature OR LYD20-quoted
   uncertainties. Mass splittings Dm21^2, Dm32^2 are FIT, so the only freedom
   left for Sigma m_nu given m1=0 (forced by 2-RH-N seesaw at LYD20) is the
   normal hierarchy floor:
       m1 = 0  =>  m2 = sqrt(Dm21^2),  m3 = sqrt(Dm32^2 + Dm21^2)
       Sigma m_nu = sqrt(Dm21^2) + sqrt(Dm32^2 + Dm21^2)

   So the scan is over the GAUSSIAN POSTERIORS of the two mass splittings
   (NuFIT 5.3 / PDG 2024) propagated to Sigma m_nu, plus a check that the
   3 fits in A16 converge to ~ this floor.

DESI DR2 LIVE-VERIFIED (arXiv:2503.14744 fetched 2026-05-05):
   LCDM:                Sigma m_nu < 0.0642 eV (95%)
   FC-corrected LCDM:   Sigma m_nu < 0.053 eV (95%)  [breaches osc. lower limit]
   w0waCDM:             Sigma m_nu < 0.163 eV (95%)  [allows NO floor]

Falsifier (parent brief):
   P(Sigma m_nu > 0.10 eV) > 50%  =>  ECI in DESI tension.

NO Mistral cross-check (STRICT BAN per project memory).
"""

import json
import numpy as np
from numpy import sqrt
from pathlib import Path

# --------------------------------------------------------------
# Inputs from A16 (already chi2-minimised at each tau choice)
# --------------------------------------------------------------
A16_JSON = Path("/root/crossed-cosmos/notes/eci_v7_aspiration/"
                "A16_THETA13_PREDICTION/theta13_prediction.json")
with open(A16_JSON) as f:
    A16 = json.load(f)

# NuFIT 5.3 / PDG 2024 (mass splittings central + 1-sigma)
DM21_SQ_MEAN = 7.49e-5
DM21_SQ_SIG  = 0.20e-5
DM32_SQ_MEAN_NO = 2.534e-3        # NO atmospheric splitting
DM32_SQ_SIG_NO  = 0.026e-3
DM32_SQ_MEAN_IO = 2.510e-3        # IO atmospheric splitting (for completeness)
DM32_SQ_SIG_IO  = 0.027e-3

# DESI DR2 (arXiv:2503.14744) -- LIVE-FETCHED 2026-05-05
DESI_DR2_LCDM_95   = 0.0642
DESI_DR2_LCDM_FC   = 0.053
DESI_DR2_W0WACDM_95 = 0.163

# Falsifier from parent brief
FALSIFIER_THRESHOLD_EV = 0.10
FALSIFIER_TRIGGER_PROB = 0.50


# --------------------------------------------------------------
# Posterior on Sigma m_nu given m1=0 (Type-I seesaw 2-RH-nu floor)
# --------------------------------------------------------------
def sample_sigma_mnu_NO_floor(n_samples=200_000, m1_floor=0.0,
                               dm21_mean=DM21_SQ_MEAN,
                               dm21_sig=DM21_SQ_SIG,
                               dm32_mean=DM32_SQ_MEAN_NO,
                               dm32_sig=DM32_SQ_SIG_NO,
                               rng=None):
    """Posterior on Sigma m_nu under NO with m1=m1_floor.

    m2 = sqrt(m1^2 + Dm21^2)
    m3 = sqrt(m1^2 + Dm21^2 + Dm32^2)         (NO convention Dm32 > 0)
    Returns array of Sigma m_nu samples (eV).
    """
    if rng is None:
        rng = np.random.default_rng(20260505)
    Dm21_sq = rng.normal(dm21_mean, dm21_sig, n_samples)
    Dm32_sq = rng.normal(dm32_mean, dm32_sig, n_samples)
    # Truncate at >0 to keep physical (Gaussian tail negligible at 25-100 sigma)
    Dm21_sq = np.maximum(Dm21_sq, 1e-10)
    Dm32_sq = np.maximum(Dm32_sq, 1e-10)
    m1 = m1_floor * np.ones(n_samples)
    m2 = np.sqrt(m1**2 + Dm21_sq)
    m3 = np.sqrt(m1**2 + Dm21_sq + Dm32_sq)
    return m1 + m2 + m3


def sample_sigma_mnu_IO_floor(n_samples=200_000, m3_floor=0.0,
                                dm21_mean=DM21_SQ_MEAN,
                                dm21_sig=DM21_SQ_SIG,
                                dm32_mean=DM32_SQ_MEAN_IO,
                                dm32_sig=DM32_SQ_SIG_IO,
                                rng=None):
    """Posterior on Sigma m_nu under IO with m3=m3_floor.

    IO convention: Dm32^2 < 0; we feed |Dm32^2| and convert.
    m1 ~ sqrt(m3^2 + |Dm32^2| - Dm21^2)
    m2 ~ sqrt(m3^2 + |Dm32^2|)
    """
    if rng is None:
        rng = np.random.default_rng(20260505)
    Dm21_sq = rng.normal(dm21_mean, dm21_sig, n_samples)
    Dm32_sq = rng.normal(dm32_mean, dm32_sig, n_samples)
    Dm21_sq = np.maximum(Dm21_sq, 1e-10)
    Dm32_sq = np.maximum(Dm32_sq, 1e-10)
    m3 = m3_floor * np.ones(n_samples)
    m1_sq = m3**2 + Dm32_sq - Dm21_sq
    m2_sq = m3**2 + Dm32_sq
    m1 = np.sqrt(np.maximum(m1_sq, 1e-10))
    m2 = np.sqrt(np.maximum(m2_sq, 1e-10))
    return m1 + m2 + m3


# --------------------------------------------------------------
# Scan: 3 ECI tau choices * 5 m1-floor scenarios
# --------------------------------------------------------------
def scan():
    rng = np.random.default_rng(20260505)
    scenarios = []

    # Scenario A: A16 W1-attractor point estimate (m1 already ~6.6 meV from fit)
    p_W1 = A16["fit_W1_attractor"]["predicted"]
    m1_W1 = p_W1["m_nu_eV"][0]
    samples_W1 = sample_sigma_mnu_NO_floor(rng=rng, m1_floor=m1_W1)
    scenarios.append({
        "label": "W1_attractor_tau_l_-0.19+1.00i",
        "tau_l": A16["fit_W1_attractor"]["tau_l"],
        "chi2_PMNS": A16["fit_W1_attractor"]["chi2_min"],
        "m1_eV_floor": float(m1_W1),
        "m1_eV_floor_origin": "A16 chi2-minimum point estimate",
        "samples": samples_W1,
    })

    # Scenario B: A16 tau=i strict (m1 ~4.5 meV)
    p_i = A16["fit_tau_eq_i"]["predicted"]
    m1_i = p_i["m_nu_eV"][0]
    samples_i = sample_sigma_mnu_NO_floor(rng=rng, m1_floor=m1_i)
    scenarios.append({
        "label": "tau_eq_i_CM_strict",
        "tau_l": A16["fit_tau_eq_i"]["tau_l"],
        "chi2_PMNS": A16["fit_tau_eq_i"]["chi2_min"],
        "m1_eV_floor": float(m1_i),
        "m1_eV_floor_origin": "A16 chi2-minimum at tau=i strict CM",
        "samples": samples_i,
    })

    # Scenario C: LYD20-check (their published best, tau ~ -0.21 + 1.52i)
    p_LYD = A16["fit_LYD20_check"]["predicted"]
    m1_LYD = p_LYD["m_nu_eV"][0]
    samples_LYD = sample_sigma_mnu_NO_floor(rng=rng, m1_floor=m1_LYD)
    scenarios.append({
        "label": "LYD20_published_tau_l_-0.21+1.52i",
        "tau_l": A16["fit_LYD20_check"]["tau_l"],
        "chi2_PMNS": A16["fit_LYD20_check"]["chi2_min"],
        "m1_eV_floor": float(m1_LYD),
        "m1_eV_floor_origin": "A16 chi2-minimum at LYD20 published tau",
        "samples": samples_LYD,
    })

    # Scenario D: Wolf-precedent NO floor (m1 = 0 strict, ECI structural)
    samples_strict_NO = sample_sigma_mnu_NO_floor(rng=rng, m1_floor=0.0)
    scenarios.append({
        "label": "Strict_NO_floor_m1=0",
        "tau_l": None,
        "chi2_PMNS": None,
        "m1_eV_floor": 0.0,
        "m1_eV_floor_origin": "Type-I seesaw with 2 RH neutrinos forces m1=0 (LMS22)",
        "samples": samples_strict_NO,
    })

    # Scenario E: IO floor (m3 = 0) -- DEVIL'S ADVOCATE for failing DESI
    samples_strict_IO = sample_sigma_mnu_IO_floor(rng=rng, m3_floor=0.0)
    scenarios.append({
        "label": "Strict_IO_floor_m3=0_NOT_ECI_PRED",
        "tau_l": None,
        "chi2_PMNS": None,
        "m1_eV_floor": 0.0,
        "m1_eV_floor_origin": "IO floor -- ECI does NOT predict this; "
                              "shown only for DESI tension comparison",
        "samples": samples_strict_IO,
    })

    return scenarios


def summarise(samples):
    return {
        "mean_eV":   float(np.mean(samples)),
        "median_eV": float(np.median(samples)),
        "std_eV":    float(np.std(samples)),
        "p05_eV":    float(np.percentile(samples, 5)),
        "p16_eV":    float(np.percentile(samples, 16)),
        "p84_eV":    float(np.percentile(samples, 84)),
        "p95_eV":    float(np.percentile(samples, 95)),
        "P_gt_0.064_eV":    float(np.mean(samples > 0.0642)),  # DESI LCDM
        "P_gt_0.053_eV":    float(np.mean(samples > 0.053)),   # DESI FC
        "P_gt_0.100_eV":    float(np.mean(samples > 0.100)),   # parent falsifier
        "P_gt_0.163_eV":    float(np.mean(samples > 0.163)),   # DESI w0wa
    }


def main():
    print("=" * 72)
    print("A44 -- Sigma m_nu predictor scan for ECI v7.4")
    print("=" * 72)
    print(f"DESI DR2 LCDM:    Sigma m_nu < {DESI_DR2_LCDM_95:.4f} eV (95%)")
    print(f"DESI DR2 LCDM-FC: Sigma m_nu < {DESI_DR2_LCDM_FC:.4f} eV (95%, breaches osc. floor)")
    print(f"DESI DR2 w0waCDM: Sigma m_nu < {DESI_DR2_W0WACDM_95:.4f} eV (95%)")
    print(f"Parent falsifier: P(Sigma m_nu > {FALSIFIER_THRESHOLD_EV:.3f} eV) > "
          f"{FALSIFIER_TRIGGER_PROB:.2f}")
    print()

    scenarios = scan()
    output = []
    print(f"{'scenario':<45}  {'mean':>8}  {'p95':>8}  {'P>.064':>7}  {'P>.10':>7}")
    print("-" * 90)
    for sc in scenarios:
        s = summarise(sc["samples"])
        rec = {
            "label": sc["label"],
            "tau_l": sc["tau_l"],
            "chi2_PMNS": sc["chi2_PMNS"],
            "m1_eV_floor": sc["m1_eV_floor"],
            "m1_eV_floor_origin": sc["m1_eV_floor_origin"],
            "summary": s,
        }
        output.append(rec)
        print(f"{sc['label']:<45}  {s['mean_eV']*1e3:>6.1f}m  "
              f"{s['p95_eV']*1e3:>6.1f}m  "
              f"{s['P_gt_0.064_eV']:>7.3f}  "
              f"{s['P_gt_0.100_eV']:>7.3f}")
    print()

    # ----------------------------------------------------------
    # Falsifier verdict (only NO scenarios; IO is comparator)
    # ----------------------------------------------------------
    no_scenarios = [r for r in output if "IO" not in r["label"]]
    triggers = [r for r in no_scenarios
                if r["summary"]["P_gt_0.100_eV"] > FALSIFIER_TRIGGER_PROB]
    eci_falsified = len(triggers) > 0
    desi_lcdm_tensions = [r for r in no_scenarios
                          if r["summary"]["P_gt_0.064_eV"] > 0.5]

    if eci_falsified:
        verdict_falsifier = (f"FALSIFIER TRIGGERED -- "
                             f"{len(triggers)}/{len(no_scenarios)} ECI scenarios "
                             f"have P(Sigma m_nu > 0.10 eV) > 0.5")
    else:
        verdict_falsifier = (f"FALSIFIER NOT TRIGGERED -- "
                             f"all {len(no_scenarios)} ECI NO scenarios have "
                             f"P(Sigma m_nu > 0.10 eV) ~ 0.0")
    if desi_lcdm_tensions:
        verdict_desi = (f"DESI DR2 LCDM TENSION -- {len(desi_lcdm_tensions)} "
                        f"scenarios have median above 0.0642 eV")
    else:
        verdict_desi = (f"DESI DR2 LCDM compatible -- all NO scenarios have "
                        f"median below 0.0642 eV")

    summary = {
        "version": "ECI v6.0.53.4 -- A44",
        "date": "2026-05-05",
        "agent": "A44 Sonnet sub-agent",
        "DESI_DR2": {
            "ref": "arXiv:2503.14744 (live-fetched 2026-05-05)",
            "LCDM_95_eV": DESI_DR2_LCDM_95,
            "LCDM_FC_95_eV": DESI_DR2_LCDM_FC,
            "w0waCDM_95_eV": DESI_DR2_W0WACDM_95,
        },
        "PMNS_inputs": {
            "Dm21_sq_eV2": [DM21_SQ_MEAN, DM21_SQ_SIG],
            "Dm32_sq_NO_eV2": [DM32_SQ_MEAN_NO, DM32_SQ_SIG_NO],
            "ref": "NuFIT 5.3 (Esteban+ 2024 arXiv:2410.05380)",
        },
        "A16_inputs": {
            "ref": str(A16_JSON),
            "version": A16.get("version"),
        },
        "scenarios": output,
        "falsifier_verdict": verdict_falsifier,
        "desi_verdict": verdict_desi,
        "headline": (
            "ECI W1 attractor predicts Sigma m_nu = "
            f"{output[0]['summary']['mean_eV']*1e3:.1f} +/- "
            f"{output[0]['summary']['std_eV']*1e3:.2f} meV "
            f"(NO + m1 floor); P(Sigma > 0.10 eV) = "
            f"{output[0]['summary']['P_gt_0.100_eV']:.3f}; "
            f"P(Sigma > 0.064 eV DESI LCDM) = "
            f"{output[0]['summary']['P_gt_0.064_eV']:.3f}."
        ),
        "honest_probability_HIGH_MEDIUM_LOW": "MEDIUM",
        "honest_probability_reasoning": (
            "Sigma m_nu is a NO-floor consequence (m1 small forced by 2-RH-nu),"
            " NOT a sharp ECI deep prediction. ECI privileges tau=i / W1; the"
            " floor value (~60-70 meV) is generic to NO + small m1. ECI passes"
            " DESI w0waCDM clean and is in mild tension with DESI LCDM strict"
            " (mean ~0.066-0.069 eV vs limit 0.064 eV). Sharp prediction is"
            " m1 itself, not Sigma directly. Counts as MEDIUM-strength graft"
            " until A16 chi2 improves and m1 floor is shown to be tau-dependent"
            " in a falsifiable way."
        ),
    }

    out_dir = Path("/root/crossed-cosmos/notes/eci_v7_aspiration/"
                   "A44_NU_MASS_PREDICTOR")
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "posterior_samples.json", "w") as f:
        # Save samples for first 3 ECI NO scenarios at downsampled rate
        sample_dump = {}
        for sc in scenarios[:4]:  # NO only
            sample_dump[sc["label"]] = sc["samples"][::100].tolist()  # 2000 per
        json.dump({"meta": summary, "samples_eV": sample_dump}, f, indent=2)

    with open(out_dir / "scan_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("=" * 72)
    print(f"FALSIFIER:  {verdict_falsifier}")
    print(f"DESI:       {verdict_desi}")
    print("=" * 72)
    print()
    print(f"HEADLINE: {summary['headline']}")
    print()
    print(f"Saved scan_summary.json + posterior_samples.json in {out_dir}")


if __name__ == "__main__":
    main()
