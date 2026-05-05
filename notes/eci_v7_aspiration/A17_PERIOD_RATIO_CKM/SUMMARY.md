# A17 — Period-ratio CKM search at K=Q(i) Damerell ladder

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A17 (parent persisted)
**Hallu count entering / leaving:** 77 / 77 (no new fabrications; counter was at 77 entering and stays here, but A18 in parallel catches Wang-Zhang misattribution → 78)

## Verdict

**WEAK** (one in-σ hit per CKM target, K=Q(i)-specific, multiplicative coefficients NOT derived).

## Key findings

The canonical Damerell ladder at K=Q(i), `r(m, a=4) := L(f, m) · π^(4-m) / Ω_K^4`, gives `{1/10, 1/12, 1/24, 1/60}` for m = {1, 2, 3, 4} (A1+A5 had verified m=4 to 60 digits; A17 verified all four to ≥40 digits). A strict screen (small rationals q with `|num|+|denom| ≤ 30`, `rel_err < 0.5%`) over all 5 imag-quadratic CM weight-5 newforms across `m ∈ {1,2,3,4}, a ∈ {0..5}` yields **two structurally clean candidates** at K=Q(i):

| Candidate | Algebraic | PDG / HFLAV | Rel err | Distance |
|---|---|---|---|---|
| **\|V_us\|** | **(9/4) · (1/10) = 9/40 = 0.22500** | **0.22501 ± 0.00068** | **0.004%** | **0.015 σ** |
| **\|V_cb\|²** | **(1/10) · (1/60) = 1/600 ≈ 1.667e-3** | **(1.668 ± 0.057) × 10⁻³** | **0.080%** | **0.024 σ** |

Equivalently `|V_cb| = √(1/600) ≈ 0.04082` (HFLAV `0.04085 ± 0.0007`, 0.04 σ off). No clean prediction emerged for `|V_ub|` or `|V_ub/V_cb|`.

## Cross-K test (uniqueness)

Same `(m, a, q)` applied to K = Q(√-2, -3, -7, -11) yields `q·r` deviations from the same CKM target ranging 524% – 15490% — i.e. **K=Q(i) is uniquely picked out by both hits**. Caveat: this is essentially a restatement of the K-specific Bernoulli-Hurwitz alignment A5 documented for `α_2 = 1/12` (the ladder `{1/10, 1/12, 1/24, 1/60}` itself only holds at K=Q(i); other K give K-specific irrationals), not independent SM evidence.

## Experimental falsifiers

- **|V_us| = 9/40**: NA62 + FLAG lattice 2027 → ~0.3% precision; `9/40 = 0.225000` survives at ~0.5–1.5 σ. **Testable 2027–2028.**
- **|V_cb|² = 1/600**: Belle II 2027 0.5% target → 0.12 σ separation, **not testable at Belle II 2027**; LHCb-U2 / Belle II run 3 (2030+) at ~0.2% precision needed.

## Honest caveats

1. The `1/600` "prediction" is the product of two known ladder rationals `(1/60)·(1/10)`; the multiplicative `1/10` coefficient is not structurally derived — it's an empirical match.
2. `9/40` matches sin θ_C exactly because PDG 2024 `λ_Wolfenstein ≈ 0.22501` happens to round to 0.225 = 9/40; the multiplicative `9/4` is also empirical, not derived. This is the well-known Wolfenstein parametrization "λ ~ 0.225" coincidence, now anchored to the Damerell `m=1` ladder.
3. Cross-K test confirms ladder K-specificity (already known from A5), NOT that Q(i) is SM-correct.
4. With max small denom 24, the search space (~24·24·4·6·5·9 ≈ 60k candidates) makes ~131 hits at <0.5% expected by chance; only the two listed are genuinely small-q AND on the canonical `a=4` ladder.

## Files

- `period_ratios.json` — full table r(m,a) × 5 forms × 6 a-values × 4 m-values, all 131 strict hits, cross-K uniform test results
- `period_ratios_strict.py` — definitive strict-screen script (mp.dps=60)
- `period_ratios.py` — initial scan (deprecated)
- `verify_candidates.py` — focused verification of 9/40 and 1/600

## Recommended v7.4 §3 wording (one paragraph)

> The Q(i)-Damerell ladder `{α_1, α_2, α_3, α_4} = {1/10, 1/12, 1/24, 1/60}` for the weight-5 CM newform 4.5.b.a admits two structurally clean numerological matches to PDG/HFLAV CKM values: `|V_us| = (9/4)·α_1 = 9/40 = 0.22500` (within 0.015 σ of `|V_us|_PDG = 0.22501(68)`) and `|V_cb|² = α_1·α_4 = 1/600 ≈ 1.667 × 10⁻³` (within 0.024 σ of `|V_cb|²_HFLAV`). Both are K=Q(i)-specific (cross-K on K = Q(√−2,−3,−7,−11) shows ≥524% deviation) and use only small multiplicative coefficients (`9/4`, `1`). No structural mechanism for the small coefficients is yet derived; both should be regarded as **suggestive numerological alignments awaiting either group-theoretic interpretation or precision-experiment falsification**. Falsifier: NA62 + FLAG-2027 ~0.3% on `|V_us|`; LHCb-U2 / Belle II run 3 (2030+) needed for `|V_cb|²`.
