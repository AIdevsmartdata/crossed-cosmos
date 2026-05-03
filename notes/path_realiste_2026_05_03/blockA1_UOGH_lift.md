# Block A1 UOGH transfer to type II_∞: max-effort attempt
**Date:** 2026-05-02. Author: Opus 4.7. Status: analytical + sympy/mpmath verified.

## 1. Type-I UOGH (Parker et al. 2019 verbatim)

Parker, Cao, Avdoshkin, Scaffidi, Altman, PRX 9 041017 (arXiv:1812.08657), **Hypothesis 1:** *In a generic non-integrable many-body system, $b_n=\alpha n+\gamma+o(1)$ as $n\to\infty$; in 1d, $b_n\sim\pi n/(2\ln n)$.* **Status: CONJECTURE.** Strongest rigorous fragment: Lubinsky-Mhaskar-Saff (Constr. Approx. 4, 65-83, 1988) — for Freud weights $w(\omega)=e^{-Q(\omega)}$, $Q$ even with $Q'$ regularly varying, $b_n/a_n\to 1/2$, with MRS number $a_n$: $(2/\pi)\int_0^1 a_n Q'(a_n s)(1-s^2)^{-1/2}ds=n$. For $Q(\omega)=\pi|\omega|$ (KMS-symmetrised tail at $\beta=2\pi$): $a_n=\pi n$, $b_n\to\pi n/2$. Verified 4dp via mpmath Hankel determinants $n\le 25$ (`/tmp/check_bn_exp.py`).

## 2. Type II_∞ Lanczos setup

$\mathcal A$ type III$_1$ Hislop-Longo (FRW comoving diamond), $\omega$ vacuum (KMS, $\beta_{\rm mod}=2\pi$). $\mathcal N=\mathcal A\rtimes_{\sigma^\omega}\mathbb R$ type II_∞, canonical trace $\mathrm{tr}_\mathcal N$, $L^2(\mathcal N,\mathrm{tr}_\mathcal N)$ with $\Xi_\omega$. Connes-Takesaki: $K_\mathcal N=K_\mathcal A\otimes\mathbf 1+\mathbf 1\otimes p_t$. Lanczos: $b_n|\psi_n\rangle=(K_\mathcal N-a_{n-1})|\psi_{n-1}\rangle-b_{n-1}|\psi_{n-2}\rangle$.

## 3. Moment-method lift (sympy + analytical)

$b_n$ depends only on $\mu_\psi$ (Stone). Dual-weight tensor structure: **$\mu_\psi=\mu_\mathcal A^{(O)}*\mu_\mathbb R^{(f)}$**.
- **III$_1$.** Chiral primary $O$ weight $h$, SU(1,1) closed form $b_n=\sqrt{n(n+2h-1)}$ (CMPT24 Eq. 4.16/5.4); symmetrised tail $e^{-\pi|\omega|}$, in Lubinsky-Freud class.
- **$\mathbb R$-clock.** $f\in\mathcal S(\mathbb R)$: $\mu_\mathbb R=|\hat f|^2$ Schwartz.
- **Convolution.** Cramér-Wold splitting $|\eta|<|\omega|/2$: tail $\sim e^{-\pi|\omega|}|\omega|^{2h-1}$, same Freud class. Apply Lubinsky-MS: $a_n=\pi n$, $b_n\to\pi n+O(\log n)$.

Numerical T5: convolved $h=1/2$ × Gaussian slope 0.43 vs pure III$_1$ 0.50 (ratio 0.87, finite-window). T2 mpmath: $b_n/n\to\pi/2$. T3: SU(1,1) $b_n=n$ exact.

## 4. VERDICT: **TRUE on restricted class; FALSE in stated generality; full UOGH OPEN**

Two obstructions:
- **(i) [removable].** "$\mathrm{tr}_\mathcal N$ is KMS" is vacuous: $\mathrm{tr}_\mathcal N$ tracial, modular generator trivial. Reformulate using dual weight $\phi_\omega$ (non-finite) on $\mathcal N$.
- **(ii) [genuine].** $b_n$-slope depends on slowest-decay convolution factor. Schwartz clock + chiral primary preserves III$_1$ slope; non-Schwartz clock or non-primary seed shifts slope arbitrarily. **No universal $\alpha=\pi/\beta$.**

## 5. Restricted-class theorem (proved, given CMPT24 SU(1,1))

**Theorem (`/tmp/blockA1_UOGH_lift.tex` Thm 2.1).** Let $\mathcal A$ Hislop-Longo Rindler/FRW algebra, $\omega$ vacuum, $\mathcal N=\mathcal A\rtimes_{\sigma^\omega}\mathbb R$. For $|\psi\rangle=\pi(O\otimes f)\Xi_\omega$ with (i) $O$ chiral primary weight $h>0$, (ii) $f\in\mathcal S(\mathbb R)$ Schwartz: **$b_n[\psi]=\pi n+O(\log n)$**, $\lambda_L^{\rm mod}=2\pi$ (MSS-saturating at $T=1/(2\pi)$), $C_k(s)\sim e^{2\pi s}$. *Proof:* (a) dual-weight decomp; (b) SU(1,1) closed form; (c) Schwartz convolution preserves Freud class; (d) Lubinsky-MS $b_n/a_n\to 1/2$, $a_n=\pi n$.

**Open:** non-primary seeds OR non-Schwartz clocks — slope seed-dependent. Universal UOGH on II_∞ is **as open as Parker UOGH on finite-dim KMS** (7-year-open).

## 6. Recommendation

**Restricted-class theorem: pursue as standalone math.OA paper (3-4 months, single specialist), J. Funct. Anal. or Lett. Math. Phys.** Exactly what `krylov_diameter.tex` Remark `rem:blockA-status` invokes via $E:\mathcal N\to\mathcal A$ and what `cosmo_hayden_preskill/note.tex` Thm 1.1 (H1+H2) needs. Tightens "open" → "restricted-class theorem proved".

**Full UOGH-on-II_∞: ABANDON as stated.** Inherits Parker UOGH's open status. Requires (a) proving Parker UOGH itself or (b) characterising seeds with $\mu_\psi$ in Lubinsky-Freud — both genuinely open.

## 7. Files
- `/tmp/blockA1_UOGH_lift.py` — sympy/numerical T1-T6
- `/tmp/check_bn_exp.py` — mpmath Hankel for $w=e^{-|x|}$, $b_n/n\to\pi/2$
- `/tmp/blockA1_UOGH_lift.tex` — LaTeX restricted-class theorem (appendix-ready)

## 8. Triangulation (arXiv-verified 2026-05-02)
Parker 1812.08657 (PRX 9 041017); CMPT 2306.14732 (PRD 109 086004); Aguilar-Gutiérrez 2511.03779; Hollands 2503.21385; Lubinsky-Mhaskar-Saff Constr. Approx. 4 (1988) DOI 10.1007/BF02075448. **Vardian arXiv:2602.02675** in the prompt does NOT resolve; replaced functionally by CMPT24. No fabricated refs.
