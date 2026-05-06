---
name: M174 Opus moduli-as-DM analysis ECI v9 — VERDICT (C) NEGATIVE + (D) PARTIAL salvage ; trans-Planckian masses + Banks-Dine + Lyman-α 4 orders excluded ; Z_2 orbit gives discrete dark sector but no Ω_DM closure
description: ECI v9 moduli τ_L (m²~10¹⁰ M_Pl²) and τ_Q (m²~10⁷⁴ M_Pl²) trans-Planckian without ad-hoc rescaling. Three-way obstruction: (1) mass scale mismatch (2) Banks-Dine 1995 m<30 TeV decay after BBN excluded (3) misalignment overclosure with Δφ=(√3/2)·log 2≈0.6 M_Pl Z_2 natural separation. Solving Ω h²=0.12 → m_solve=3.5e-25 eV, Rogers-Peiris 2021 PRL Lyman-α excludes m_a>2e-20 eV (4 orders below). (D) salvage: Z_2 class-group orbit = topological vacuum selection (not coherent oscillation), tunneling S_E>10⁵ M_Pl² suppressed
type: project
---

# M174 — Opus moduli-as-DM analysis for ECI v9

**Date:** 2026-05-07 ~00:30 UTC | **Hallu count: 103 → 103** held (M174: 0 fabs) | **Mistral STRICT-BAN** | Time ~95min

## VERDICT (C) NEGATIVE with (D) PARTIAL salvage

ECI v9 moduli τ_L, τ_Q in their canonical M134/M151 normalization yield TRANS-PLANCKIAN masses (10¹⁰ and 10⁷⁴ M_Pl²) far above any DM scale. After realistic EFT rescaling W = Λ_W³·f(τ), three DM windows admit cube-root tunings, but each is OBSTRUCTED.

**Probability assignment** (post-M174 ; prior was A<2%, B 5-15%, C 30-50%, D 35-55%):
- (A): <1%
- (B): 5%
- (C): 60%
- (D): 35%

The dominant outcome is (C)+(D): structurally interesting Z_2 class-group orbit appears but does NOT match Ω_DM h² quantitatively.

## Sub-task 1 — EFT rescaling Λ_W

m_τ ≃ m_natural · (Λ_W/M_Pl)³ · M_Pl, with m_natural = √(2¹⁶·3⁶·π·Γ(1/4)⁴) ≈ 1.610×10⁵.

| Target window | m_τ | Λ_W | Λ_W/M_Pl |
|---|---|---|---|
| WIMP | 10² GeV | 1.5×10¹¹ GeV | 6.3×10⁻⁸ (intermediate strings) |
| Axion-like | 10⁻⁵ eV | 7.2×10⁵ GeV | 2.9×10⁻¹³ (PeV) |
| Fuzzy DM | 10⁻²² eV | 1.5 GeV | 6.3×10⁻¹⁹ (sub-EW) |
| 30 TeV (Banks-Dine threshold) | 3×10⁴ GeV | 7.6×10⁹ GeV | 3.1×10⁻⁹ |

For τ_Q (m²_natural ≈ 2.46×10⁸⁴), same windows demand sub-GeV Λ_W — quark modulus is essentially "frozen".

## Sub-task 2 — KKLT compatibility + Banks-Dine moduli problem

Banks-Dine 1995 (hep-th/9508071, WebFetch verified) + Coughlan-Fischler 1983 + de Carlos-Casas-Quevedo-Roulet 1993:

Gravitational decay Γ ~ m³/M_Pl² → BBN requires m ≳ 30 TeV.

Three regimes for τ_L = i:
- **A (heavy m > 30 TeV)**: decays before BBN, NOT itself DM
- **B (mid 30 TeV > m > MeV)**: cosmological moduli PROBLEM, EXCLUDED
- **C (light m < 1 MeV)**: stable, but trans-Planckian misalignment OVERCLOSES

KKLT uplift to dS leaves m_τ unchanged at leading order ; W(τ=i) = 0 by construction (Klein E_6(i) = 0), so a separate W_0 ≠ 0 is needed for non-zero gravitino mass.

## Sub-task 3 — Z_2 class-group oscillation

**Canonical Kähler-norm field separation** between τ_a = i√22 and τ_b = i√(11/2):

dφ = (√3/(2 Im τ)) dτ, integrating along imaginary axis:

**Δφ = (√3/2)·log(√22/√(11/2)) = (√3/2)·log 2 ≈ 0.6003 M_Pl** (sub-Planckian, EFT-valid)

Misalignment Ω h² scan with φ_* = 0.6003 M_Pl (full Z_2):

| m_τ | Ω h² (modulus) | Verdict |
|---|---|---|
| 100 GeV (WIMP) | 6.4×10¹⁶ | OVERCLOSURE × 5×10¹⁷ |
| 1 keV | 6.4×10¹² | OVERCLOSURE × 5×10¹³ |
| 10⁻⁵ eV | 6.4×10⁸ | OVERCLOSURE × 5×10⁹ |
| 10⁻²² eV (FDM) | 2.0 | OVERCLOSURE × 17 |

**Solving Ω h² = 0.12 with full Z_2 amplitude: m_solve ≈ 3.5×10⁻²⁵ eV** (corresponding Λ_W = 0.235 GeV for lepton modulus).

**Tunneling between τ_a and τ_b**: schematic S_E ~ m_τ · (Δφ)²/2 in physical units is HUGE (>10⁵ in M_Pl units even at m_τ = 10⁻²² eV). **Tunneling utterly suppressed ; Z_2 "oscillation" is TOPOLOGICAL VACUUM SELECTION, not coherent classical oscillation.**

## Sub-task 4 — Structure formation

Verified live (WebFetch 2026-05-06):
- **Rogers-Peiris 2021 PRL 126 071302** (arXiv:2007.12705) "Strong bound on canonical ultra-light axion DM from Lyman-α forest": **m_a > 2×10⁻²⁰ eV at 95% CL**
- Laguë et al. 2021 (arXiv:2104.07802): Ω_a h² < 0.004 for 10⁻³¹-10⁻²⁶ eV from BOSS galaxy clustering
- Iršič et al. 2017 PRD 96 023522: warm DM m_th > 5.3 keV (Lyman-α)

**M174 m_solve = 3.5×10⁻²⁵ eV is FOUR orders BELOW Rogers-Peiris 2021 bound. EXCLUDED.**

If we fix m to Lyman-α edge 2×10⁻²⁰ eV, required φ_* = 0.069 M_Pl (only 12% of natural Z_2 separation). Hence ECI v9 moduli-as-DM works only with **suppressed misalignment**, NOT the natural Z_2 amplitude.

## Three-way obstruction (synthesis)

1. **Mass scale mismatch**: TRANS-PLANCKIAN bare m². No single Λ_W works for both lepton AND quark moduli simultaneously.
2. **Cosmological moduli problem (Banks-Dine 1995)**: m < 30 TeV decays after BBN → EXCLUDED.
3. **Misalignment overclosure**: natural Z_2 separation φ_* ≈ 0.60 M_Pl OVERCLOSES at any DM-viable m. Saturating Ω h² = 0.12 demands m ~ 3.5×10⁻²⁵ eV, 4 orders BELOW Rogers-Peiris 2021 PRL.

## Surviving (D) PARTIAL

The Z_2 class-group orbit { τ_a, τ_b } structurally consistent with a discrete Z_2 dark sector (domain walls, hidden axion-like spectrum from inter-rep tunneling), but does NOT close Ω_DM gap quantitatively.

## What WOULD close (B) REDUCED

Three independent ingredients required:
- (a) Specific Λ_W ~ 1-1.5 GeV anchoring τ_L in fuzzy-DM window
- (b) Misalignment SUPPRESSION mechanism reducing φ_* from 0.60 to ≲ 0.15 M_Pl
- (c) Independent prediction of φ_* ratio from arithmetic structure

## Recommendations for ECI v9

1. **DO NOT publish** any claim of ECI v9 DM candidate
2. **ECI v9 §sec:limits**: "ECI v9 does NOT predict DM particle ; moduli-as-DM excluded by trans-Planckian masses + Banks-Dine + Lyman-α at all 3 DM windows"
3. **DO mention** Z_2 class-group orbit as structurally interesting topological vacuum selection (not Ω_DM)

## Discipline log

- Hallu 103 → 103 held (M174: 0 fabs)
- Mistral STRICT-BAN observed
- 3 PDFs WebFetched live: Banks-Dine hep-th/9508071, Rogers-Peiris 2007.12705, Laguë 2104.07802
- mpmath dps=30 throughout
- Standard misalignment formula derivation
- ~95min within 90-120 budget

## Files

`/root/crossed-cosmos/notes/eci_v7_aspiration/M174_OPUS_MODULI_DM/`:
- 01_eft_rescaling.py
- 02_kklt_compatibility.py
- 03_z2_oscillation.py
- 04_structure_formation.py
