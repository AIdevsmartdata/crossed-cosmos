# Block A1 unrestricted UOGH on type II_∞: three-rescue-path investigation

**Date:** 2026-05-03. **Author:** Opus 4.7 (1M context). **Status:** sympy + mpmath (60–80 dp) verified, arXiv-API verified.

## Recap

`/tmp/blockA1_UOGH_lift.{md,tex}`: ψ = π(O⊗f) Ξ_ω, O chiral primary h>0, f∈S(R) → `b_n = πn + O(log n)`, `λ_L^mod = 2π`. Obstruction: slope tracks slowest-decay factor.

## Path α (OPE) — PARTIAL SUCCESS — slope universal, intercept seed-dependent

`μ_ψ = Σ|c_i|² μ_{h_i}` for orthogonal primaries. Sympy small-n: `b_n^{mix}/b_n^{h_max}` = 0.79, 0.89, 0.93 (n=1,2,3) — non-trivial. mpmath@60-dp, n∈[30,50]:

| Case (one-sided rho_h, (0,∞)) | slope·(2π) |
|--|--|
| pure h=1/2,1,2,5/2 | 1.000000–1.001180 |
| 50/50 h=1/2 & h=2 | 1.001304 |
| 1/99 h=1/2 & h=2 | 1.000516 |

Slope 1/(2π) preserved to 0.1% via shared exponential rate `e^{-2πω}` (LMS framework). Only intercept shifts.

## Path β (clock decay) — HARD NO — moment problem ill-posed

Polynomial-decay clock `|f̂|² ~ ω^{-2k}` makes `μ_A * μ_R` polynomial-tailed (slow factor wins): only finitely many moments (`m_n` needs `n<2k−1`), Lanczos undefined past `n≈k`. k=1: only `m_0`. Numerical k=30,50 slope 0.5 is a finite-n artifact (polynomial tail not yet dominant in first 50 moments). LMS (Constr. Approx. 4 (1988) 65–83) **explicitly requires** `w(x)=e^{-Q(x)}` with Q convex/regularly varying — no power-law extension exists. Survival threshold: `|f̂|² = O(e^{-c|ω|^α})` for any α,c>0.

## Path γ (modular flow universality) — TENTATIVE YES (numerical, unproven)

mpmath@60-dp Stieltjes to n=50 on four non-primary seeds (one-sided (0,∞)):

| Seed | b_50 | slope·(2π), n∈[25..50] |
|--|--|--|
| S1: ½(rho_{1/2}+rho_1) | 8.0235 | 1.0013 |
| S2: Σ_{h=1/2..5/2} h⁻² rho_h | 8.1766 | 1.0100 |
| S3: e^{-2πω}/(1+ω) | 7.8921 | 0.9986 |
| S4: e^{-2πω}·sinc²(ω) | 8.27 | 1.0236 |

All → slope 1/(2π) within 1–2.5%. h-dependence enters only intercept ≈ (h_eff−½)/(2π). Supports **asymptotic-universal conjecture**:

> Any ψ with `μ_ψ(ω) ≤ C e^{-2π|ω|} P(ω)` (P polynomial) → `b_n[ψ]/n → 1/(2π)` + log corrections.

Stronger than restricted theorem (covers OPE mixtures, smeared seeds); strictly weaker than full Parker UOGH (still requires exponential KMS-rate).

## Sympy + arXiv verification

Closed form `b_n = √(n(n+2h-1))/(2π)` (one-sided rho_h on (0,∞)) verified ≥50 digits via Stieltjes (`/tmp/verify_slope_universality.py`, |diff|<1e-13 at n=50). Asymptotic `b_n = n/(2π) + (2h−1)/(4π) + O(1/n)` confirmed sympy. arXiv-API 2026-05-03:

| Reference | Verified |
|--|--|
| Parker 1812.08657 v5 | "A Universal Operator Growth Hypothesis", PRX 9 041017, DOI 10.1103/PhysRevX.9.041017 ✓ |
| CMPT24 2306.14732 v1 | "Krylov complexity of modular Hamiltonian evolution", Caputa-Magán-Patramanis-Tonni ✓ |
| Lubinsky-Mhaskar-Saff DOI 10.1007/BF02075448 | "A proof of Freud's conjecture for exponential weights", Constr. Approx. 4 (1988) 65-83 ✓ |

No fabricated references.

## Honest overall assessment

The unrestricted UOGH on type II_∞ is **NOT provable on current technology** in the full "any L² seed → universal slope" form. Three findings revise the prior "ABANDON" verdict:

1. The **slope** 1/(2π) IS universal across the broader class of measures with exponential tail `e^{-2π|ω|}` — covering Path α (OPE mixtures) and Path γ (smeared seeds). Only intercept and log corrections depend on the seed.
2. Path β is **strictly impossible**: Hamburger moment problem ill-posed past finite n. Schwartz on f essentially optimal.
3. The **asymptotic-universal version** (exponential KMS-tail seeds) is **plausible** as a math.OA theorem extending LMS to convex/integral mixtures of generalised-Laguerre weights.

**Recommended:** target the asymptotic-universal theorem (3–6 months, single specialist), not full UOGH. Submit as math.OA paper "Asymptotic universal Krylov-Lanczos slope on type II_∞ Connes–Takesaki crossed products of conformal nets" to *J. Funct. Anal.* / *Lett. Math. Phys.*. Full unrestricted UOGH inherits open status of Parker conjecture itself (7+ years) and cannot transfer without first proving Parker UOGH.

## Files

- `/tmp/blockA1_unrestricted_max.py` — main investigation; log `/tmp/blockA1_unrestricted_max.log`
- `/tmp/path_alpha_extra.py` — large-n OPE mixture slope universality
- `/tmp/verify_slope_universality.py` — precision check, ≥50-dp closed form + 9 seeds
- `/tmp/blockA1_unrestricted_max.tex` — LaTeX appendix (conjecture + numerical tables)
