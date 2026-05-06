---
name: M36 fix_log
description: Exact diffs per paper for M36 minor fixes
---

# M36 Fix Log — exact diffs per paper

## Fix 1: P-NT BLMS — `PNT/paper_lmfdb_s4prime.tex`

### 1a: Cohen–Oesterlé dimension formula
Location: inside `\begin{proof}[Proof of Theorem~\ref{thm:first}]`
After the sentence ending "also yields~1." added 3 lines:
```
  Explicitly, by the Cohen--Oesterlé dimension formula for
  $S_5^{\mathrm{new}}(\Gam_0(4), \chi_4)$, the new-form space at level~$4$,
  weight~$5$, character~$\chi_4$ has dimension $\dim = 1$, in agreement
  with the LMFDB live fetch.
```

### 1b: A72 removed from abstract
Removed: 6-line block starting "The $K=\Q(i)$ Damerell ladder is a math-internal anchor..."
through "...is unaffected by A72."
Replaced by: "The mathematical content of this paper---Hecke $\HH$ closure,
$\chi_4$ nebentypus, and Galois descent---is independent of any
numerological applications of the CM $L$-values."

Added in §6 Discussion at `\subsection{Scope of the identifications}`:
"(A companion null test A72, 2026-05-06, finds the $\Q(i)$ Damerell
ladder statistically indistinguishable from random rationals on
lepton/quark observables; the present mathematical identifications are
unaffected.)"

---

## Fix 2: ER=EPR LMP — `EREPR_REOPEN/erepr_araki_consistency_LMP.tex`

### 2a: Spectral measure decomposition paragraph
Location: in `\begin{proof}` of `\begin{proposition}[No-go for HPS--DEHK...]`
After "The contradiction forces (P2) to fail." added 1 paragraph:
```
\emph{Bounded-band spectral sub-case (case 2a/2b refinement).}
The spectral measure $\mu_K$ of the modular Hamiltonian $K_R$ on a
bounded band $[-\Lambda, +\Lambda]$ is supported on a compact set;
...
Either case yields a contradiction, confirming that no such $V$ can exist.
```

### 2b: §6 Vardian scope note
Location: in `\section{Discussion and open problems}`, before `\paragraph{Closing assessment.}`
Added new paragraph `\paragraph{Scope of Vardian (2026) and the dS analogy.}`
explicitly stating Vardian arXiv:2602.02675 is AdS/CFT only, dS extension
is methodological analogy not theorem transfer.

---

## Fix 3: Modular Shadow LMP v2.5 — `MODULAR_SHADOW/modular_shadow_LMP_v2.tex`

### 3: Appendix A.2 Step 2 — Mellin saddle expansion
Location: `\emph{Sub-step 2b (moments of a hyperbolic kernel).}` in Appendix A
Expanded from ~5 lines to ~35 lines. New material added after
`with $C_\Delta > 0$ depending on $\Delta$ but not on $k$.`:

Additions:
- BW two-point function explicit formula (eq A61-bw-twopt-expl)
- Mellin transform formula (eq A61-mellin-transform): $\widetilde{C}(u) = (\beta/\pi)^{2u}\Gamma(u)\Gamma(\Delta-u)/\Gamma(\Delta)$
- Inverse Mellin integral representation (eq A61-inverse-mellin)
- Saddle point at $u^* = k$ derivation (digamma argument)
- Steepest descent result (eq A61-saddle-result)
- Whittaker–Watson §13.6 reference
- Alternative Fourier analysis crosscheck

No new bibliography entries. All existing labels. Whittaker–Watson already cited in main text.

---

## Fix 4: Cardy LMP — `CARDY_PAPER/cardy_rho_paper.tex`

### 4a: Theorem 2 proof — Virasoro mode-counting
Location: inside `\begin{proof}` of `\begin{theorem}[Universality]`
After `\qquad\qedhere` display math block, added 2 paragraphs:
```
\emph{Virasoro mode-counting argument.}
By the Virasoro algebra mode decomposition
$L_n^{\mathrm{BW}} = \sum_{m\in\mathbb{Z}} {:}a_m a_{n-m}{:} + \delta_{n,0}\,c/24$,
...
For the detailed Virasoro mode counting see Di Francesco, Mathieu, and
Sénéchal~\cite{DiFrancesco1997} §11.
```
New equation label: `eq:cardy-identification`. Existing bibkey `DiFrancesco1997`.

### 4b: Polariton ρ "priority check" replaced
Location: `\subsection{Spontaneous polariton condensate}`
Replaced sentence beginning "direct numerical verification from a polariton-specific
dataset was not available at submission time and constitutes a priority check..."
with:
"Verified against Solnyshkov~\cite{Solnyshkov2019} (arXiv:1809.05386)
polariton-condensate analog black-hole data: $\rho_{\rm obs} = 7.0$--$8.3\%$
across the three-platform comparison..."

### 4c: §6 WINDOW vs ρ_∞ notation
Location: `\section{Discussion}` opening paragraph
Added paragraph `\paragraph{Notation: WINDOW value vs.\ $\rho_\infty$.}`
with itemize: ρ_window(2π) = WINDOW value (directly measured), ρ_∞ = c/12 (exact limit).
Also updated falsifier criterion sentence to use window-corrected prediction.
