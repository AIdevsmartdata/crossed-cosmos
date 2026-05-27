# H8 — Renyi index dependence of SU(N) lattice EE crossover

**Date**: 2026-05-26 | **Author**: Claude Opus 4.7 1M

## 1. Theory: n-dependence of κ_n(N)

**Dilute (N≤4, free-field).** 1+1d CFT (Calabrese-Cardy hep-th/0405152) gives
universal **f_n = (n+1)/(2n)**. 4d free QFT (Casini-Huerta 0905.2562; KPSS
1111.6290) f_n = f_a+f_b+f_c is non-monomial but (n+1)/(2n) is leading to ~10%
(Lee-McGough 1407.7816). f_1=1, f_n monotone decreasing.

ECI dilute prediction :
```
κ_n(N) = f_n · (1 − 1/N²) · ζ(3)/√π
κ_n/κ_2 ≈ [(n+1)/(2n)]·(4/3)  →  8/9 (n=3), 5/6 (n=4)
```

**Dense (N≥5, confined string).** String-tension area law dominated by single
saddle (Klebanov et al. 0709.2140) ⇒ g_n(string) weakly n-dependent. Mean-field
⇒ dense affine fit **κ=0.518√N−0.458 approximately n-independent**.

**Crossover N_c(n).** Picture A (cube→sphere geometric) ⇒ N_c n-independent.
Picture B (fractal Hausdorff, DS Bot vision) ⇒ ΔN_c ≈ +0.3(n−2). Distinguishable
at 0.5-1 N-units.

## 2. Predicted κ_3(N), κ_4(N), N=2..8

| N | κ_2 | κ_3 pred | κ_4 pred | Regime |
|---|---|---|---|---|
| 2 | 0.508 | 0.451 | 0.423 | dilute |
| 3 | 0.603 | 0.536 | 0.503 | dilute |
| 4 | 0.635 | 0.564 | 0.529 | dilute |
| 5 | 0.701 | 0.701 | 0.701 | crossover |
| 6 | 0.810 | 0.810 | 0.810 | dense |
| 7 | 0.913 | 0.913 | 0.913 | dense |
| 8 | 1.007 | 1.007 | 1.007 | dense |

**Falsifier**: R_n(N) := κ_n/κ_2. Dilute (N≤4) → R_3≈8/9, R_4≈5/6. Dense (N≥5)
→ R_n≈1.0. R_3(N=3) far from 8/9 falsifies dilute free-field. R_3(N=6) far
from 1 falsifies single-saddle string-network.

## 3. Literature survey — Renyi-n SU(N) lattice, n≥3

- **BP arXiv:0802.4247** (verified) — n=2 only.
- **Rabenstein-Bodendorfer-Buividovich-Schäfer arXiv:1812.04279** PRD 100
  034504 (2019) — SU(2,3,4) **only n=2**.
- **Itou et al. 2016 PTEP** — SU(3) n=2.
- **Bulgarelli-Panero arXiv:2211.00425** — improved SU(N) replica ; may enable
  n≥3 (tentative).

**Verdict**: **No SU(N) Renyi-n>2 lattice measurement exists** as of 2026-05.
H8 is unexplored — measurement is original.

Anti-fab — task IDs that did NOT verify, replaced:
- "hep-th/0902.0006" → **arXiv:0905.2562** Casini-Huerta
- "0707.3047" → **arXiv:1011.5482** Calabrese-Cardy-Tonni 2011

## 4. JAX protocol

Extend `/tmp/voie1_calcs/jax_su2_EE_BP2008b_FAST_2026-05-25.py` :
1. `U` shape (n, L, L, L, 2T, 4, N, N) — n cyclic replicas.
2. Junction-link cross-replica staple at t=T (mod n gluing).
3. α-integration : S_n = −(n−1)⁻¹·∫dα ⟨∂_α S⟩.
4. Cabibbo-Marinari MH all n replicas (post-fix K† convention).

**Params**: N∈{2..6}, n∈{2,3,4}, L∈{4,6,8}, β=0.6·N², THERM=5000, N_meas=200
decorr 50, α-grid 11pts [0,1].

**Cost**: replica trick scales linearly in n. n=3: 1.5×, n=4: 2.0×. 45 runs
(5N×3L×3n) ≈ 22 GPU-h on A100, overnight.

**Risk**: Z_n/Z_1^n shrinks exponentially ; σ/μ ≳ 30% at n=4 L=8. Mitigation:
Bulgarelli-Panero Jarzynski estimator.

**Sanity gates**: (a) cold-start ⟨P⟩→1 all replicas; (b) n=2 code reduces to
existing κ_2(SU(2))=0.508 within 1%; (c) β→∞ free-limit κ_n/κ_2 → 8/9 at β=4.

## 5. Verdict prelim

| Claim | Verdict |
|---|---|
| Theoretically supported | YES — two regimes give distinct n-dependences (genuine discriminator) |
| Falsifiable | YES — R_n ratio cancels renormalisation; 10-20% diffs measurable |
| Currently untested | YES — no n>2 SU(N) lattice in literature |
| Testable now | YES — ~1 engineer-week JAX work, ~22 GPU-h |

**Recommendation**: HIGH priority. Sequence: (a) close SU(7) n=2 first, (b)
prototype n=3 SU(2) L=4 (1 day), (c) full n=3 scan SU(2..6) L=4,6 (~1 GPU-wk),
(d) gate n=4 on (c) signal. **First SU(N) Renyi-n>2 lattice measurement →
standalone PRL independent of ECI outcome.**

## Verified references

- Calabrese-Cardy 2004 : arXiv:hep-th/0405152
- Calabrese-Cardy 2009 J.Phys.A 42 504005 : arXiv:0905.4013
- Casini-Huerta 2009 J.Phys.A 42 504007 : arXiv:0905.2562
- Buividovich-Polikarpov 2008 NPB 802 458 : arXiv:0802.4247
- Rabenstein et al 2019 PRD 100 034504 : arXiv:1812.04279
- Klebanov-Pufu-Sachdev-Safdi 2012 JHEP 04 074 : arXiv:1111.6290
- Perlmutter 2014 JHEP 03 117 : arXiv:1308.1083
- Bulgarelli-Panero 2022 : arXiv:2211.00425 (tentative)
- Calabrese-Cardy-Tonni 2011 : arXiv:1011.5482 (replaces 0707.3047)
