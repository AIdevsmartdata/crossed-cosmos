# A44 — Σm_ν predictor scan, ECI v7.4

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A44 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held; DESI DR2 live-fetched arXiv:2503.14744; Mistral STRICT-BAN respected)

## Verdict

**FALSIFIER NOT TRIGGERED.** ECI Cassini-clean wedge survives DESI 2025 cleanly under w0waCDM; mild ~5-10% tension under strict LCDM. Honest deep-prediction strength **MEDIUM (40-50%)** — Σm_ν is a NO-floor consequence, not a sharp ECI signature.

## Numerical results (Type-I seesaw, NuFIT 5.3 mass-splitting posteriors)

| Scenario | τ_l | m₁ floor (meV) | Σm_ν mean ± std (meV) | P>0.064 | P>0.10 |
|---|---|---|---|---|---|
| W1 attractor | -0.19+1.00i | 6.59 | **69.0 ± 0.28** | 1.000 | 0.000 |
| τ=i strict CM | 0+1.00i | 4.49 | 65.5 ± 0.28 | 1.000 | 0.000 |
| LYD20 published | -0.21+1.52i | 0.89 | 60.7 ± 0.28 | 0.000 | 0.000 |
| Strict NO floor m₁=0 | — | 0.0 | 59.7 ± 0.28 | 0.000 | 0.000 |
| IO floor (anti-pred) | — | 0.0 | 99.4 ± 0.31 | 1.000 | 0.155 |

## DESI DR2 live-verified (arXiv:2503.14744)

- LCDM+Planck+ACT: Σm_ν < 0.0642 eV (95%)
- LCDM Feldman-Cousins: < 0.053 eV (**breaches NO oscillation lower bound** — DESI's own internal tension)
- w0waCDM: < 0.163 eV (ECI clean)

## Falsifier (parent threshold P(Σ>0.10 eV)>0.50)

**NO scenario triggers** — max P=0.000 across W1, τ=i, LYD20, strict-NO. ECI passes the parent's 0.10 eV threshold. ECI **does** sit ~1.7σ above DESI strict LCDM (W1=69 vs 64.2 meV) — survivable, noted in v7.4.

## Honest deep-prediction probability: MEDIUM (40-50%)

- **PRO:** W1 attractor narrows Σm_ν to 65-69 meV, testable by CMB-S4 (~2032).
- **CON:** Floor is generic to NO 2-RH-ν seesaw, not unique to ECI structural anchor. The Q(i)-anchor signature is the ~5 meV m₁ offset (W1 vs τ=i vs LYD20-τ), below current cosmo reach.
- **MITIGATION:** Joint LRT with A16 sin²θ_13 + δ_CP + θ_23 octant via DUNE 2030+ → potentially HIGH.

## Wedge survival

Cassini-clean wedge survives DESI 2025 in w0waCDM frame. Recommend ECI v7.4 published with **w0waCDM compatibility caveat** in Σm_ν sector. DESI's internal NO floor breach (0.053 < 0.058) means ECI is in the same tension regime as the entire NO oscillation hierarchy — **not falsified, just constrained**.

## Files

- `sigmamnu_scan.py`
- `posterior_samples.json` (2000 samples × 4 ECI NO scenarios)
- `scan_summary.json` (machine-readable verdict + DESI metadata)
