---
name: M175 Opus H_0 from ECI arithmetic — VERDICT (C)/(D) NEGATIVE confirmed ; ECI v9 does NOT derive H_0 ; best (D) coincidence Γ(1/4)⁴/√(2π) = 68.934 is ad-hoc with no ECI motivation for divisor √(2π) ; recommend retain MCMC fit H_0 = 68.84±1.16 as parameter status
description: M175 verified ECI v9 cannot derive H_0 in [67,73] km/s/Mpc. All 5 candidate routes (BC π/4 residue, λ_BKL, 6/5 Damerell, M134 m_τ², M161B.2 c) fail at dimensional bridge. Connes-Rovelli 1994 thermal time gives σ_t=Friedmann time but no H_0 magnitude (still requires ρ_tot input). Best numerical coincidence Γ(1/4)⁴/√(2π) = 68.934 close to LCDM 68.84 (diff 0.09) but ad-hoc. Brief 71.18 typo caught (true Γ(1/4)⁴=172.79) pre-propagation, hallu 103 held. Recommend ECI v9 §limits: NOT a battlefield
type: project
---

# M175 — Opus H_0 from ECI arithmetic

**Date:** 2026-05-07 ~00:30 UTC | **Hallu count: 103 → 103** held (M175: 0 fabs, brief 71→173 typo caught pre-propagation) | **Mistral STRICT-BAN** | Time ~110min

## VERDICT (C)/(D) NEGATIVE confirmed

ECI v9 arithmetic structure does **NOT** derive H_0 ∈ [67, 73] km/s/Mpc. All 5 candidate routes fail at dimensional bridge: arithmetic invariants are dimensionless, H_0 has dimension [T⁻¹], and there is no ECI-internal length/time scale to convert.

Probability:
- (A) PROVED: 0% (was <0.5%)
- (B) REDUCED: 0% (was <3%) — no near-miss with closeable gap
- (C) NEGATIVE: 60%
- (D) PARTIAL: 40% — Γ(1/4)⁴/√(2π) coincidence only

## Brief auto-correction

Brief stated **"Γ(1/4)⁴ ≈ 71.18"**. True value via mpmath dps=30: **Γ(1/4)⁴ = 172.7923**.

The "≈ 71" intuition the brief was reaching for is the derived combination **Γ(1/4)⁴/√(2π) = 68.9341**, which IS close to C6 v3 LCDM 68.84.

Caught pre-propagation by M175. **Hallu count 103 held** (no propagation = no fab).

## Hubble tension status (May 2026)

- **SH0ES** (Cepheids + JWST late 2025): H_0 = 73.04 ± 1.04 km/s/Mpc
- **Planck 2018 + DESI BAO 2024-2025**: H_0 = 67.4 ± 0.5 km/s/Mpc
- **Freedman-Madore CCHP 2024** (arXiv:2408.06153): H_0 = 70.39 ± 1.22 ± 1.33 (TRGB/JWST) — splits difference
- Tension ~5σ ; ~100+ BSM proposals ; **NONE from arithmetic side**

## Numerical evaluation (mpmath dps=30)

| Candidate | Value | dist Planck 67.4 | dist SH0ES 73.04 |
|---|---:|---:|---:|
| Γ(1/4)⁴ | 172.7923 | 105.39 | 99.75 |
| **Γ(1/4)⁴ / √(2π)** | **68.9341** | **1.53** | **4.11** |
| 25π | 78.5398 | 11.14 | 5.50 |
| π²/(6 log 2) [λ_BKL] | 2.3731 | 65.03 | 70.67 |
| **λ_BKL × 30** | **71.1941** | **3.79** | **1.85** |
| 6/5 [Damerell] | 1.2000 | 66.20 | 71.84 |
| (6/5) × 100/√3 | 69.2820 | 1.88 | 3.76 |
| π/4 [BC residue Q(i)] | 0.7854 | 66.61 | 72.25 |
| Γ(1/4)⁴ × 2/5 | 69.1169 | 1.72 | 3.92 |
| Γ(1/4)⁴ / e | 63.5667 | 3.83 | 9.47 |

Sensitivity test on best route: any divisor in [2.48, 2.52] produces value in [68.6, 69.7]. Loose fit ; ad-hoc.

## Per-route verdict

**Route 1 — BC residue π/4 (Q(i))**: ress=1 ζ_K(s) for K=Q(i) = 2π/(w_K·√|d_K|) = 2π/(4·2) = π/4 (verified ; w_K=4, |d_K|=4). β in BC dimensionless (Hecke σ_t scales Q-lattice covolumes). **No physical second/Mpc**. **(C) NEGATIVE.**

**Route 2 — λ_BKL = π²/(6 log 2) ≈ 2.371**: Lyapunov rate of mixmaster bouncing near Bianchi IX singularity (Khinchin-Lévy for Gauss map on Kasner exponents). BKL applies to t→0+ regime ; H_0 is late-time observable ; RG flow opposite. λ_BKL × t_universe dimensionally meaningless. H_0·t_age ≈ 0.95-0.99 ≠ λ_BKL = 2.37. **(C) NEGATIVE.**

**Route 3 — 6/5 Damerell ratio**: H_0_Planck/H_0_SH0ES = 0.9228 ; 5/6 = 0.833 — does NOT match (10% off). Closer ratios 12/13 = 0.9231 and √0.85 = 0.9220 lack ECI structural origin. Even ratio match wouldn't fix absolute H_0. **(C) NEGATIVE.**

**Route 4 — M134 m_τ_L² = 2¹⁶·3⁶·π·Γ(1/4)⁴**: Verified value = 2.5935·10¹⁰ M_Pl². m_τ²/H_0² ratio in natural units = 1.18·10⁴² with no clean arithmetic fingerprint. **Best numerical coincidence**: Γ(1/4)⁴/√(2π) = 68.934 vs C6 v3 LCDM 68.84 (diff +0.09, within 1σ MCMC error 1.16). Identity Γ(1/4)⁴/√(2π) = 8√(2π)·ϖ² with ϖ = Γ(1/4)²/(2√(2π)) ≈ 2.622. **No ECI-derived motivation for divisor √(2π)**. Equivalent ad-hoc Γ(1/4)⁴ × 2/5 = 69.12 fits as well. **(D) PARTIAL — coincidence, no derivation.**

**Route 5 — M161B.2 c-dichotomy**: c (CFT central charge) is dimensionless. To produce km/s/Mpc requires pairing with Planck length and bare cosmological time, neither fixed by ECI v9 internally. **(C) NEGATIVE.**

## Connes-Marcolli BC + cosmology

Per Connes-Marcolli 2008 *NCG, QFT and Motives* and Connes-Rovelli 1994 (gr-qc/9406019) :

In FRW universe with CMB photon gas as KMS_β state at T_γ, modular flow σ_t **coincides with Friedmann coordinate time** (up to rescaling). This solves "problem of time" but **does NOT predict H_0 magnitude** — Friedmann H² = (8πG/3)ρ_tot still requires ρ_tot input ; arithmetic gives no constraint on Ω_m, Ω_Λ.

BC system uses Hecke algebra of GL_1(A_f) for Q-lattices ; cosmological thermal time uses photon C* algebra in curved spacetime. **Two distinct examples of thermal time hypothesis ; no functor connecting them is published.**

**Speranza 2504.07630**: KMS at β=2π Bunch-Davies on de Sitter static patch. Recovers Gibbons-Hawking T_dS = H_dS/(2π) which is *temperature given H_dS*, not arithmetic determination of H_0.

## Modular shadow flow + late-time

λ_BKL strong-coupling near-singularity ; FRW late-time IR-trivial ; **no published mechanism** for λ_BKL re-emergence as late-time observable.

## Recommendation for ECI v9

1. **Do NOT publish** any claim of arithmetic H_0 derivation
2. **ECI v9 cosmology** retain MCMC-fit H_0 = 68.84 ± 1.16 km/s/Mpc with **parameter status** (not arithmetic-locked)
3. **Hubble tension is NOT ECI v9 comparative-advantage battlefield** — F2-F8 lepton sector and M40-M45 Bianchi IX modular shadow remain dominant
4. If user wants cosmological prediction, target **r_s, σ_8/S_8, or n_s** where inflation-modular structure (M48 doublon, M49 inter-domain) has formal hooks
5. ECI v9 §sec:limits item: "ECI v9 does NOT predict H_0 ; cosmology fit retained as parameter input"

## Discipline log

- Hallu count 103 → 103 held (M175 0 fabs, brief 71→173 typo caught pre-propagation)
- Mistral STRICT-BAN observed
- 5 routes evaluated quantitatively + Connes-Marcolli BC cosmology framework reviewed
- Verde-Treu-Riess 2019 verified ; Freedman-Madore CCHP 2024 cited correctly
- Time ~110min within 90-120 budget

## Files

- /tmp/h0_arith_check.py + /tmp/h0_lambda_bkl.py (numerical verification scripts)
