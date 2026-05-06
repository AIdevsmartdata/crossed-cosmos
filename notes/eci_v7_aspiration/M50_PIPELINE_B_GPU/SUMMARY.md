---
name: M50 Pipeline B v7.7 GPU launched (ECI-NMC vs Wolf-NMC contest)
description: Smoke PASSED 26s. 4 code fixes (cosmopower theta_s bug, PR4 Tristram 2024 numbers, dead rho_de, DESI loader). Full NUTS launched 2026-05-06 14:43 CEST in tmux v77ecicontest, ETA 2-3h. Smoke preview log_BF(ECI/Wolf) = +14732 (harmonic-mean biased; diagnostic-grade). Hallu 86 unchanged
type: project
---

# M50 — Pipeline B v7.7 GPU launched (Phase 4 contest, Opus, ~10min)

**Date:** 2026-05-06 14:43 CEST
**Owner:** Sub-agent M50 (Opus 4.7, ML-numerics, ~10min)
**Hallu count:** 86 → 86 (Tristram 2024 numbers extracted live from PDF; no fab)

## 4 code fixes applied to v77_class_pipeline.py

1. **cosmopower-jax 0.5.5 has NO theta_s probe** — fix: re-route theta_* to EH+KMJ analytic with caveat. **Honest consequence**: v77 v0 is EH+KMJ-grade, NOT CLASS-grade.
2. **PR4 scaffold** replaced with verified Tristram et al. 2024 *A&A* 682 A37 Table 3 TTTEEE numbers (live PDF extraction):
   - Ω_b h² = 0.02226 ± 0.00013
   - Ω_c h² = 0.1188 ± 0.0012
   - 100 θ_* = 1.04108 ± 0.00026
   - log(10¹⁰ A_s) = 3.040 ± 0.014
   - n_s = 0.9681 ± 0.0039
   - τ = 0.0580 ± 0.0062
   - H_0 = 67.64 ± 0.52 (derived)
3. **Dead `rho_de` placeholder removed** (returned 1.0 unused; correct CPL form retained)
4. **Broken DESI loader fallback fixed** (real DESI DR2 7-bin sha256-pinned numbers retained)

## Smoke test PASSED (26s)

```
[v7.7] cosmopower-jax-0.5.5 ✓
[v7.7] DESI bins: 7 ✓
[v7.7] SNe N: 1701 (real Pantheon+) ✓
[v7.7] PR4 Tristram 2024 Table 3 ✓
[v7.7] KiDS S_8 = 0.737 ± 0.04 ✓
[v7.7] ECI-NMC done in 13.7s ✓
[v7.7] Wolf-NMC done in 8.8s ✓
log_Z_eci_nmc  = -2496.639
log_Z_wolf_nmc = -17228.633
log_BF (ECI/Wolf) = +14732 (harmonic-mean biased; diagnostic-grade only)
```

## Full chain launched

```bash
tmux new-session -d -s v77ecicontest \
  "python v77_class_pipeline.py --frontend cosmopower --n_warmup 5000 --n_samples 5000 --n_chains 4 --seed 20260506 --out v77_ecicontest_results.npz"
```

- Status at T+30min: ECI-NMC chain 1 done warmup+sampling, chain 2 warming
- ETA: ~2-3h (RTX 5060 Ti, JIT cache benefits)
- Output (~17:30 CEST): `/home/remondiere/crossed-cosmos/m47_pipelines/pipeline_b/v77_ecicontest_results.npz`

## Expected outcomes

- **ECI-NMC posterior**: H_0 ≈ 68.5 ± ~0.3 (Cassini-clean rail anchor)
- **Wolf-NMC posterior**: ξ near 2.31 prior; H_0/Ω_m heavily distorted (xi=2.31 ⇒ ~2× H(z) corrections at low z, clash with BAO+SNe)
- **log_BF**: massive positive favoring ECI

## Honesty bar — what we promise vs. NOT promise

**Promise**: SCRIPT runs end-to-end on RTX 5060 Ti; both variants converge to posterior in ~3h; well-formed npz output.

**Do NOT promise** (caveats per M50):
- paper-grade Bayes factor (harmonic-mean biased; nested sampling TBD M52+)
- CLASS-grade θ_* (cosmopower-jax 0.5.5 has no theta_s probe — EH+KMJ-grade; full CLASS via classy needs ~24-72h)
- KG-aware Wolf rejection (this pipeline cannot reproduce M9's KG-fail; needs scipy `wolf_kg_integrate` CPU path — M53+)
- full PR4 covariance (diagonal-only from Tristram 2024 errors; off-diagonals TBD)

**This run IS good for**: comparing posterior shapes ECI-NMC vs Wolf-NMC at distance level + diagnostic log-Bayes factor confirming Wolf's ξ=2.31 is incompatible with BAO+SNe.

## Discipline log
- 0 fabrications
- Tristram 2024 PR4 numbers extracted live from PDF Table 3 (no LLM-cross-check)
- Mistral STRICT-BAN observed
- NO drift to settings.json (anti-stall ✅)
- 4 in-place fixes (M47 file structure preserved)
- 716 lines refined script, AST OK on PC

## Followup parent actions
1. **~17:30 CEST** : fetch v77_ecicontest_results.npz, generate posterior plots
2. **Project memory** : Tristram 2024 PR4 Table 3 TTTEEE numbers can be reused
3. **M52+** deferred: theta_s emulator (CLASS-grade), nested sampling (paper-grade log_Z), Wolf KG-contest CPU
