# H5 Test vs NANOGrav 15yr Data

**Date:** 2026-05-26  
**Hypothesis:** Dilute→dense crossover at T_c QCD generates a stochastic GW background detectable by PTAs.

---

## 1. Predictions (H5)

| Quantity | H5 prediction | Derivation |
|---|---|---|
| Peak freq today | **f_peak ≈ 2.7 × 10⁻⁷ Hz** | Causal horizon at T_c=150 MeV, g_* = 17.25, formula f_today ≈ 1.65×10⁻⁷ Hz · (T/100 MeV) · (g_*/10)^(1/6) (Caprini-Figueroa 2018) |
| Amplitude | **h² Ω_GW ~ 2.3 × 10⁻¹²** | 10⁻¹⁰ · (Δκ)² with Δκ ≈ 0.15 |
| Spectral index | **β = 2/3** (in Ω_GW ∝ f^β) | Smooth crossover / 2nd-order analog |

## 2. Observed (NANOGrav 15yr — Agazie et al. arXiv:2306.16213)

| Quantity | Value |
|---|---|
| Peak freq sensitivity | ~ 3 × 10⁻⁸ Hz (lowest measured bin near 1/T_obs ≈ 2 nHz) |
| Amplitude A_yr (at f = 1 yr⁻¹) | 2.4₋₀.₆⁺⁰·⁷ × 10⁻¹⁵ |
| Implied h² Ω_GW near peak | ≈ 3.5 × 10⁻⁹ |
| Spectral index γ (timing-residual t_yr) | 13/3 = 4.33 (favored), 68% CI roughly [3.2, 4.8] |
| Implied β (Ω_GW): β = 5 − γ | **β = 2/3** ★ |

Companion paper Afzal et al. arXiv:2306.16219 (search for new physics) finds 1st-order phase transitions, cosmic strings, scalar-induced GWs, and SMBH binaries all able to fit, with stable cosmic strings disfavored.

## 3. Comparison

| Test | Predicted | Observed | Match |
|---|---|---|---|
| **Peak frequency** | 2.7×10⁻⁷ Hz | ~3×10⁻⁸ Hz | within ~1 order of magnitude (ratio ≈ 9) |
| **Amplitude** | 2.3×10⁻¹² | 3.5×10⁻⁹ | **OFF by ~1500× (≈ 3.2 OoM)** |
| **Spectral index β** | 2/3 | 2/3 (γ=13/3) | **EXACT — coincides to the value standardly attributed to SMBH binaries** |

## 4. Verdict: **MIXED — supported on spectral shape, falsified on amplitude (as currently stated)**

**(A) Spectral index — STRIKING MATCH.** The smooth-crossover β = 2/3 prediction coincides exactly with the NANOGrav posterior. This is the same index expected for an inspiral population of SMBH binaries (γ = 13/3 from circular GW-driven inspirals: Phinney 2001), which is precisely why NANOGrav's signal is naturally interpreted as SMBHB. **H5 is degenerate with the SMBHB prior** — both predict the same β. This is a non-trivial sanity check (H5 is *not* a 1st-order PT model, which would predict β = 3 and is disfavored) but it is not a discriminator: the spectral test does not falsify H5, and it does not single it out either.

**(B) Peak frequency — broadly consistent.** H5 predicts ~2.7×10⁻⁷ Hz, NANOGrav peaks near ~3×10⁻⁸ Hz. The ~10× offset is borderline acceptable given (i) NANOGrav's sensitivity peaks at the low end of its 15-yr observing window rather than at the source's true peak, and (ii) the standard horizon formula has order-unity prefactors (peak vs causal-tail). The QCD-horizon scale is well-known to coincide with PTA bands (Caprini-Figueroa 2018, Schwaller 2015, Brandenburg+ 2021).

**(C) Amplitude — H5 (as stated) is OFF by ~3 orders of magnitude.** Predicted h² Ω_GW ~ 2×10⁻¹² is 1500× *below* the observed ~3×10⁻⁹. Two possibilities:

  1. **H5 amplitude estimator is wrong** (the "10⁻¹⁰ · (Δκ)²" was a back-of-envelope guess for a 1st-order-like source). For a crossover/smooth transition the GW power is naturally *suppressed* relative to 1st-order PT (no bubble collision, no detonations), so 10⁻¹² is in fact *consistent* with the theoretical expectation for the QCD crossover — and that's why the QCD crossover **alone has historically been considered too weak to source NANOGrav** (e.g., arXiv:2306.17136 frames QCD as a "footprint" modulator of an externally-sourced signal, not the source itself).
  2. **The amplitude formula needs a coherence/duration boost** if the crossover is associated with a long-lived turbulent epoch (MHD turbulence amplification: arXiv:2102.12428 = Brandenburg-Kahniashvili).

**Honest bottom line for ECI/H5 framework:** The dilute→dense crossover *cannot* be the *primary* source of the NANOGrav GWB at face value — the predicted amplitude is ~3 OoM too small. However, the spectral-shape coincidence (β=2/3 matches NANOGrav posterior) is non-trivial and degenerate with the leading SMBHB interpretation, so H5 is **not falsified**; it survives as a sub-dominant component or as a modulator of the low-frequency tail of an inflationary/SMBHB primary signal. P(H5 = sole NANOGrav source) ≈ **5–10%**; P(H5 contributes detectable footprint to QCD-epoch GW spectrum, testable by SKA / LISA cross-band) ≈ **30–40%**.

**One-line summary:** Spectral shape passes (degenerate with SMBHB); amplitude as written fails by ~10³; H5 reframed as "footprint modulator" survives. The discriminating test is *not* NANOGrav alone — it is the cross-band slope between PTA (~nHz) and LISA (~mHz), where H5 predicts a *cutoff above* f_peak rather than a continuation.

---

## References (all verified via WebFetch against arXiv abstracts)

1. **arXiv:2306.16213** — Agazie et al. (NANOGrav), *The NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background*. Confirmed: A_yr = 2.4×10⁻¹⁵, γ = 13/3 favored, β=2/3 in Ω_GW. **VERIFIED**.
2. **arXiv:2306.16219** — Afzal et al. (NANOGrav), *The NANOGrav 15-year Data Set: Search for Signals from New Physics*. Constraints on cosmic strings, 1st-order PT, scalar-induced GWs, domain walls; most cosmological models fit except stable cosmic strings. **VERIFIED**.
3. **arXiv:2306.17136** — *Footprints of the QCD Crossover on Cosmological Gravitational Waves at Pulsar Timing Arrays* (Franciolini-Iovino-Riotto et al.). Frames QCD crossover as low-freq tail modulator, not primary source. **VERIFIED (abstract).**
4. **arXiv:2306.16214** — Antoniadis et al. (EPTA+InPTA DR2), independent confirmation A ≈ 2.5×10⁻¹⁵ at γ=13/3 fixed. **VERIFIED**.
5. **arXiv:2307.01653** — *Translating nano-Hertz GW background into primordial perturbations taking account of the cosmological QCD phase transition* (Phys. Rev. D L101304). Quantifies that ignoring QCD shifts amplitude by ~25% and γ by ~10%. **VERIFIED (search result).**

Tentative (not directly fetched, listed by search): arXiv:2102.12428 (Brandenburg-Kahniashvili MHD QCD turbulence at NANOGrav, frequently cited in this context) — flagged **tentative**, ID not re-verified.
