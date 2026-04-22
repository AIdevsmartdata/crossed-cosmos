# v8 — Claude-app coïncidences cartography (audit)

**Date.** 2026-04-22.
**Source.** Claude-app memo « Coïncidences physiques 2023-2026 ».
**Audit.** CLI + Python numerical verification + WebSearch spot-checks.

## Verdict global : **MOST HONEST CLAUDE-APP DOC SO FAR.**

Claude-app explicitly rejects the coincidences that have collapsed by
2026 (g-2 muon under WP25, W-CDF under CMS 2024, Cabibbo ≈ π/14 as
weak numerology, LK-99 refuted, vacuum impedance Z₀ ≈ 120π as SI-2019
artefact, CMB cold spot / axis of evil under mask-sensitivity, JWST
"impossible galaxies" mostly re-classified). This is the first
Claude-app cartography to **deprioritise** more than it prioritises,
which is the rigorous direction.

## Numerical spot-checks

| Claim | Verified? | Note |
|---|---|---|
| Koide Q = 0.666661(7) at 2×10⁻⁵ | ✓ | My calc: Q = 0.6666605 ± 6.77×10⁻⁶ (m_τ uncertainty), consistent with 2/3 at ~1σ. Precision 10⁻⁵ real. |
| a₀ = cH₀/(2π) at 5% | ⚠ | With SH0ES H₀=73: 6.3% off. With Planck H₀=67.4: 15% off. Doc implicitly assumes SH0ES without stating it. |
| Cohen-Kaplan-Nelson Λ ~ M_Pl²H² at 10% | ⚠ | Valid at **fourth root**: (M_Pl H)^(1/2) ≈ 4.19 meV vs observed ρ_Λ^(1/4) ≈ 2.24 meV (factor 2). In energy *density*: ratio 0.08, i.e. factor 12. Doc's "10%" exaggerated in density units. |
| Dabholkar-Murthy-Zagier arXiv:1208.4074 | ✓ | "Quantum Black Holes, Wall Crossing, and Mock Modular Forms". Mock Jacobi decomposition of N=4 quarter-BPS counting. Real theorem, solid. |
| g-2 muon resolved under WP25 | ✓ | Fermilab Run 1-6 final June 2025 + WP25 Theory Initiative lattice QCD → ~1σ consistency. Anomaly gone at current precision. Doc's depriorisation correct. |
| CMS W boson 80360.2 ± 9.9 MeV | ✓ | Verified earlier in this repo (bib entry CMSWmass2024). |

## The 5 « pivot » coincidences retained

All 5 survive after the caveats above:

1. **Koide 2/3** — most precise numerical coincidence without SM mechanism. 40-year robustness. Priority 5 confirmed.
2. **BTFR + a₀ ≈ cH₀/(2π)** — at 6% with SH0ES, 15% with Planck. Scatter < 0.1 dex in SPARC is real. Priority 5 with Hubble-scheme-dependent caveat.
3. **Hubble tension** — 4-5σ post-JWST stable (Riess 2024 arXiv:2408.11770 gives 72.6±2.0 on JWST sample). CCHP internal TRGB/JAGB vs Cepheids tension unresolved. Priority 5.
4. **Cosmological constant problem + CKN** — at factor-2 in energy scale (not density), Λ^(1/4) ≈ 2.24 meV ≈ ν mass. Priority 5 with "factor-2 in scale" caveat.
5. **Dabholkar-Murthy-Zagier 2012** — rigorous theorem. Priority 5 as model of "coincidence-turned-theorem".

## The 4 pistes de théorèmisation

The doc proposes 4 pistes each with a « premier calcul ≤ 1 semaine » :

### Piste 1 — Koide via motives / 3-point moduli
**Assessment.** Concrete test proposed (reverse prediction with 2 masses + Q=2/3). Worth doing **outside our v5/v6 scope**; not currently relevant to JHEP/EPJ C tracks. DEFER.

### Piste 2 — BTFR + a₀ via equipartition theorem
**Assessment.** Tests MOND-adjacent phenomenology via SPARC data, possibly via Bost-Connes KMS framework (which we've flagged type-III vs our type-II, F-6). Interesting but diverges from our focus. DEFER; interesting for a separate independent project.

### Piste 3 — Mock modular forms extended to NMC quintessence horizon
**Assessment.** **THE MOST RELEVANT PISTE TO OUR v5+v6 WORK.** It proposes an explicit bridge: write Z(τ) for the quintessence-NMC horizon partition function in slow-roll, test whether it admits a mock Jacobi decomposition à la D-M-Z 2012, and check whether Zwegers' harmonic completion produces the GSL type-II violation term of v6.

**Why this is interesting:**
- Agent 6 / Claude-app v3 / v5↔v6 bridge attempt via Jacobson-EGJ failed (F-14, BRIDGE-FAILURE). Piste 3 proposes a **different bridge**: via mock modular partition function rather than d_iS saturation.
- D-M-Z is a proven theorem in the specific N=4 string setting. Extrapolation to quintessence horizon is a real leap, but bounded.
- Binary outcome: Z(τ) is mock Jacobi (SUCCESS → v8 paper) or it isn't (F-19 logged).

**Risk.** NMC quintessence horizon doesn't have the BPS / AdS₃/CFT₂ structure D-M-Z rely on. The mock Jacobi property is holomorphic-specific; cosmological (non-BPS, non-holomorphic) horizons are not obvious candidates. The test is almost certainly NEGATIVE — but a clean negative is diagnostic value.

**Recommendation.** **Launch one bounded Sonnet agent to test Piste 3.** Pre-register in `REGISTRY_FALSIFIERS.md` as V8-Piste3-MockJacobi. Budget 45 min wall-clock.

### Piste 4 — α-RuCl₃ c=1/2 via TDA / microlocal sheaves
**Assessment.** Material-physics side-project, unrelated to v5/v6. DEFER.

## Recommendation

- Commit this audit
- Launch ONE bounded agent on Piste 3
- Expect negative result; log as F-19 if so
- Do not touch v5 or v6
- Pistes 1, 2, 4 documented but not pursued

The methodological message of the Claude-app doc is **correct**: « la rigueur exige de déprioriter plus que de prioritiser ». Of the 4 pistes, only Piste 3 is within our scope; the other 3 are worth watching but not investing.
