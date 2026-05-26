# H62 — d_s = 7/3 decoder rescue (weak H58)

**Verdict** : d_s = 7/3 EXACT rescue both anchors {κ_FP, ξ★} simultaneously. P(weak H58) 10% → **25-40%**.

## Pole structure d_s = 7/3 (half-integer step manifold-with-boundary)

Pour `d_s = 7/3` avec convention half-integer step (naturelle pour Gribov region ∂Ω boundary) :

$$s_k = d_s/2 - k/2 = 7/6 - k/2$$

```
k=0 : s_0 = 7/6
k=1 : s_1 = 2/3 = ξ★ EXACT ★
k=2 : s_2 = 1/6 = κ_FP EXACT ★
k=3 : s_3 = -1/3
k=4 : s_4 = -5/6
```

**Les DEUX ancres {κ_FP, ξ★} landent EXACTEMENT sur poles ζ_Δ_FP**.

## Lattice α consistency

`d_s = 7/3 ⇒ α = d_s/2 - 1 = 7/6 - 1 = 1/6 ≈ 0.1667`

| Source | α measured | α=1/6 fit |
|--------|------------|-----------|
| Nakagawa hep-lat/0702002 SU(3) Coulomb | 0.15(10) | **0.17σ ✓** |
| GOZ hep-lat/0509054 SU(2) subleading | 0.16 | **4% match ✓** |
| Sternbeck hep-lat/0510109 SU(3) Landau | 0.16-0.45 | compat (large scatter) |

## Discrimination des candidats

| d_s | pole pour 2/3 | pole pour 1/6 | α prédit | ✓ ? |
|-----|---------------|----------------|----------|-----|
| 2.0 | 0.5 (diff 0.167) | 0.0 (diff 0.167) | 0 | ✗ |
| 2.30 | 0.65 (0.017) | 0.15 (0.017) | 0.15 | ~ |
| **7/3 = 2.333** | **2/3 EXACT** | **1/6 EXACT** | **1/6** | ★★★ |
| 2.40 | 0.70 (0.033) | 0.20 (0.033) | 0.20 | ~ |
| 2.50 | 0.75 (0.083) | 0.25 (0.083) | 0.25 | ✗ |
| 10/3 = 3.333 | OK k=2 deeper | OK k=3 deeper | 2/3 | ✗ falsifié lattice |

**d_s = 7/3 est l'UNIQUE rationnel simple dans [2.3, 2.5] avec alignement EXACT des 2 anchors**.

## Status littérature

**d_s = 7/3 PAS connu dans literature YM**. Recherches multiples (arXiv + INSPIRE + Google Scholar) :
- "spectral dimension 7/3 Yang-Mills" : 0 hit
- "alpha = 1/6 Gribov" : 0 hit
- Eichmann-Pawlowski-Silva 1909.12207 trouve d_s variable selon scale (IR → 1 pour propagateur, pas 7/3)

**Proposer d_s = 7/3 serait NEW conjecture**.

## Coïncidences intéressantes

- **Anderson-localization mobility-edge fractal dim ≈ 2.33 en 3D** (cond-mat/9707147) — exactement 7/3 ! Possible analogie : near-zero modes FP ↔ localized states near mobility edge.
- 7/3 = 2 + 1/3 : interpretation possible "2D smooth Gribov boundary + 1/3 codim drift bulk"
- Scaling solution Kondo 0909.4866 : α_D + 2α_G = (D-4)/2 ; α_G=1/6 ⇒ α_D=-1/3

## Tests discriminants

1. **Re-analyse GOZ + Nakagawa raw data** : extract α avec proper error bar. 1-2 days, $0. Email Olejnik/Nakagawa.
2. **Heat trace Z(t) ~ t^{-7/6}** prediction (vs t^{-1} free, t^{-5/3} 10/3). 1 week JAX. $5.
3. **New SU(2) sim** β=2.40, L=16,20,24 continuum extrap, Lanczos low-λ. d_s=7/3 → α=0.167±0.01 robust. 2 weeks. $50.
4. **Théorique** : Bałaban block-spin on Gribov region + Anderson mobility-edge analogy.

## Refs verified (PDF/abs)

- hep-lat/0509054 GOZ ✓
- hep-lat/0702002 Nakagawa ✓
- hep-lat/0510109 Sternbeck ✓
- 1909.12207 Eichmann-Pawlowski-Silva ✓
- 1003.4792 ✓
- 1001.0784 Greensite ✓
- hep-th/0005133 Vassilevich spectral functions ✓
- 0909.4866 Kondo ✓
- 0904.2380 ✓
- Ammann lecture notes spectral zeta ✓

## Verdict final

- d_s = 7/3 **arithmétiquement + empiriquement consistent** (1σ Nakagawa, 4% GOZ subleading)
- Rescue weak H58 : **κ_FP + ξ★ EXACTEMENT poles** sous half-integer step
- **d_s = 7/3 PAS connu** dans YM lit → nouvelle conjecture
- Anderson-localization 2.33 = potentiellement physical motivation
- **P(weak H58 with d_s = 7/3)** : 25-40% (up from 10% at 10/3)
- Action prioritaire : raw ρ(λ) tables from Olejnik/Nakagawa

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[H58_zeta_FP_poles_meromorphic_2026-05-26]]
[[H60_lanczos_dS_lattice_survey_2026-05-26]]
[[spectral_decoder_validated_2026-05-26]]
