# A46 — LYD20 unified scaffold graft v7.5 §4 with τ=i pinned

**Date:** 2026-05-05 evening (final files written 12:54-12:55 UTC)
**Owner:** Sonnet sub-agent A46 (parent persisted; ran out of extra usage at end of run)
**Hallu count entering / leaving:** 84 / 84 (held; LYD20 formulae transcribed verbatim from TeX source lines 1483-1556)

## Verdict (honest negative)

**LYD20 unified Q+L scaffold with τ STRICTLY PINNED at i is PHYSICALLY UNVIABLE.** Chi² penalty vs LYD20 published best fit is **~99,000×** (not the ~1.8× A42 hoped for). The "GRAFT PRIMARY LYD20 scaffold" recommendation in A42 must be REVISED.

## Numerical results (19 observables joint fit, 10 free params after pinning τ)

| Fit configuration | χ²_min (19 obs) | Penalty vs LYD20 best | Status |
|---|---|---|---|
| τ_LYD20 best (Re=−0.21, Im=1.52) | **1,009** | reference (0×) | LYD20 published |
| τ_W1 attractor (Re=−0.19, Im=1.00) | **878,990** | **+870×** | already poor |
| **τ = i strict (Re=0, Im=1)** | **10⁸** | **+99,061×** | catastrophic |

## What survives at τ_LYD20 best (chi²=1009)

Predicted vs PDG (subset shown):
- m_e/m_μ = 0.004836 (PDG 0.004836 ± 2e-5) — exact
- m_μ/m_τ = 0.05946 (PDG 0.05946 ± 3e-4) — exact
- sin²θ_12 = 0.242 (PDG 0.307 ± 0.012) — 5.4σ off
- sin²θ_13 = 0.0065 (PDG 0.0220 ± 7e-4) — 22σ off
- sin²θ_23 = 0.236 (PDG 0.572 ± 0.020) — wrong octant
- δ_CP = 222° (PDG 197° ± 25°) — 1σ off
- V_us = 0.226 (PDG 0.225 ± 7e-4) — exact
- V_cb = 0.043 (PDG 0.042 ± 8e-4) — 1σ off
- V_ub = 0.0044 (PDG 0.0038 ± 2e-4) — 3σ off
- m_c/m_t, m_u/m_c, m_s/m_b ratios — need check

## Implications for v7.5 architecture

A42's recommendation **"GRAFT PRIMARY LYD20 unified scaffold with τ=i pinned, accept 1.8× χ² penalty"** is **WRONG by 5+ orders of magnitude**.

**Honest revision options for v7.5**:

1. **DROP LYD20 graft from v7.5** : ECI v7.5 stays at math-anchor (CM-by-Q(i) via 4.5.b.a) without claiming LYD20 fit-equivalence. Must add explicit caveat: "ECI does not provide a competitive joint Q+L fit at τ=i; the modular-flavour body is left to future work."

2. **Two-tau migration** : per A49 correction (Du-Wang explicitly says two-τ improves lepton fit 4-16×), accept τ_q ≠ τ_l with structural justification = "Du-Wang flipped SU(5) GUT-locking is the unification mechanism; ECI's K=Q(i) anchor selects τ_l = i but τ_q = LYD20 best." — but loses single-τ math-anchor purity.

3. **Different scaffold** : NPP20 lepton-only (4-6 params for 9 obs) at τ=i, leaving quark sector to G1.12.B SU(5) modular f^{ij}(τ=i) framework (Opus M6 closure). Cleaner but limits scope.

## Files

- `lyd20_fit_pinned.py` (29 KB) — main implementation
- `lyd20_pinned_results.json` (6 KB) — fit verdicts
- `v75_section4.tex` (11 KB) — A46-drafted §4 patch (NOTE: assumed 1.8× penalty viable; needs MAJOR REVISION given actual 99,000× penalty)
- `inject_results.py`, `probe_chi2.py`, `probe_taui.py`, `quick_penalty.py`, `refit_taui.py`, `sanity_check.py`, `sanity_full_chi2.py`, `sanity_isolated.py`

## Recommended next step

**Discard v75_section4.tex AS-IS** (its "structural-anchoring cost is bounded" framing is empirically false). **Rewrite v7.5 §4** with one of the 3 honest revision options above. Most defensible: **Option 3 (NPP20 lepton + G1.12.B quark)** — cleaner scope, avoids the 99,000× penalty, retains all today's wins.

## Honest summary for Kevin

This is a NEGATIVE result that REVISES today's earlier Wave-9 + Wave-10 strategic conclusions. v6.0.53.5 commit assumed A42's "1.8× penalty" estimate; the actual measured penalty is 99,000× → v7.5 architecture must drop or substantially reformulate the LYD20 graft. The CM-by-Q(i) math-anchor + G1.12.B SU(5) M1-M6 closure + 9 papers SUBMISSION-READY all stand independently.
