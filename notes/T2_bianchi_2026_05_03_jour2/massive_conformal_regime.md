# Conformal Regime ($m\,a\,\Delta\eta\sim 1$) for Prop. 4.2 — Three-Path Investigation

**Date:** 2026-05-03 — `/tmp/massive_conformal_regime.{py,md,tex}`, sympy 1.12.

## Verdicts

| Path | Verdict | Decisive obstruction |
|---|---|---|
| **α — Dyson resummation** | **Partial** | Cocycle id. PASSes at $m^4,m^6$; spectrum invariance at $\ge m^4$ blocked by absence of Araki–Donald perturbed weight on III$_1$ with **unbounded** Wick $H_V$. |
| **β — Mode decomposition** | **Partial** | Per-$\ell$ first-order $\Gamma_\ell=\R$ holds; same obstruction sector-by-sector. Reduces problem to $\ell=0$. |
| **γ — Faulkner–Speranza WKB** | **BLOCKED** | $K_\HL$ is conformal Killing of $g_\FRW$ but with **order-1** conformal factor along the worldline; no half-sided modular inclusion; FS unavailable at any scale. |

**No path closes the conformal regime.** Most promising: α∩β at $\ell=0$, contingent on an open operator-algebra problem.

## Path α — sympy at $m^4, m^6$

Commuting-algebra cocycle identity
$\frac{(\int_0^{s+t}H)^n}{n!}=\sum_k \frac{(\int_0^s H)^k}{k!}\frac{(\int_0^t H(s+\cdot))^{n-k}}{(n-k)!}$
PASSes for $n=1,2,3$ on three profiles (poly/exp/osc). Necessary, not sufficient, for the operator T-exp identity, which lifts via interaction-picture (BFV 2003 §5).

**Existence vs spectrum.** Trotter (RS X.51): $u_t=e^{it(K_\HL+m^2H_V)}e^{-itK_\HL}$ unitary on Fock for any $m$ (Wick squares on bounded supports are infinitesimally $K_\HL^{1/2}$-bounded — Glimm–Jaffe Q-bound). Bottleneck is the Connes-1973 step: $u_t$ must be $(D\varphi^V\!:\!D\varphi^{(0)})_t$. Araki 1973 requires $H_V$ bounded; Donald 1981 (CMP 79, 367) extends to unbounded $H_V$ when $e^{-\beta H_V}$ trace-class — **false** for quadratic Wick on III$_1$. No published machinery covers our case.

## Path β — mode decomposition

Spherical separation: radial eq. $(-\partial_\eta^2+\partial_r^2-\ell(\ell+1)/r^2-V(\eta))\chi_{\ell m}=0$, $V_\ell=m^2a^2+\ell(\ell+1)/r^2$. Sympy: $K_\HL$ spherically symmetric ($[K_\HL,L^2]=0$), so each $\ell$-sector is invariant under $\sigma^\FRW_t,\sigma^{(0)}_t,u_t$. At $m=0$, $K_\HL$ is unitarily a radial boost on the worldline at the origin, commuting with $L^2$, giving $\Gamma_\ell(\sigma^{(0)})=\R$ per $\ell$. Connes 1973 sector-by-sector: **$\Gamma_\ell(\sigma^\FRW)=\R$ for every $\ell$ at first order in $m^2$** — strict refinement of Prop. 4.2.

**Per-$\ell$ Compton scale:** $\lambda_C(\ell)=(m^2+\ell(\ell+1)/R_d^2)^{-1/2}$. For $mR_d\sim 1$: $\lambda_C(0)\sim R_d$ (conformal), $\lambda_C(\ell\!\gg\!1)\sim R_d/\ell$ (always heavy). The conformal regime is **a statement about $\ell=0$ only**. Reduces the problem; same Araki–Donald obstruction recurs.

## Path γ — quasi-Killing? No.

Sympy: $K_\HL$ is true conformal Killing of $g_\FRW=a^2\eta_{\mu\nu}$ with
$\omega^\FRW(\eta,r)=\pi/\eta-2\pi\eta-\pi r^2/\eta$.
On worldline $r=0$: $\omega^\FRW/K^\eta=(2\eta^2-1)/[\eta(\eta^2-1)]$, equal to $4/3$ at $\eta=1/2$, divergent at $\eta=1$. **Not small at any scale.** Not quasi-Killing in any perturbative sense.

**Half-sided modular inclusion.** FS (arXiv:2405.00847, verified) needs Wiesbrock half-sided inclusion from a positive-generator translation along a Killing horizon. Radiation FRW comoving worldline has none of: Killing horizon; conformal-time Killing translation ($a$ non-constant); diamond-preserving comoving translation. **FS machinery unavailable**; no Compton-scale rescue.

## Honest assessment

- **Most promising:** α∩β at $\ell=0$. Closure requires Araki–Donald for unbounded Wick squares on III$_1$ — **open operator-algebra problem**, not a calculation. **6–12 months** of OA research.
- A clean **negative** (explicit cocycle-invariance failure at $m^4$ on a test diamond) achievable in **2–4 weeks** to delineate the perturbative boundary.
- Path γ is a **hard no** at all scales on this background; do not pursue further.

## References (arXiv-verified)

- Faulkner & Speranza, **arXiv:2405.00847** (May 2024) — verified.
- Brunetti–Fredenhagen–Verch, **arXiv:math-ph/0112041** (2001), CMP 237 — verified.
- Hollands–Wald, **gr-qc/0103074**, **gr-qc/0111108** (2001) — verified.
- Connes 1973, *Ann. Sci. ENS* 6, 133, Thm 1.2.4 — used in Prop. 4.2.
- Araki 1973, *Pub. RIMS* 9; *Pacific J.* 50, 309 — bounded $H$ only.
- Donald 1981, *CMP* 79, 367 — unbounded $H$, $e^{-\beta H}$ trace-class only.
- Wiesbrock 1993, *CMP* 157, 83 — half-sided modular inclusions.

## Recommendation for `frw_note.tex` (NOT applied)

Do **not** promote conformal regime to a Proposition. Add one sentence after Prop. 4.2: *"The conformal regime $m\,a\,\Delta\eta\sim 1$ admits a per-$\ell$ refinement (sympy `/tmp/massive_conformal_regime.py`) but no proven higher-order extension; the obstruction is the absence of an Araki–Donald perturbed weight for unbounded Wick $H_V$ on III$_1$. The Faulkner–Speranza quasi-Killing route is blocked by an order-1 conformal-factor obstruction sympy-computed in the same script."*
