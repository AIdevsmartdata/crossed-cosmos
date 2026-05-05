# A47 — KW dS-trap × ECI K=Q(i) compatibility

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A47 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held; arXiv abstract + HTML fetched live)

## Verdict

**COMPATIBLE — GRAFT RECOMMENDED as v7.4 §3.5.**

## KW paper (live-verified)

**arXiv:2310.10369**, S.F. King & X. Wang, *"Modulus stabilisation in the multiple-modulus framework"*, **JCAP 07 (2025) 011**. Parent brief title "modular cosmology" was approximate; correct title noted (NOT counted as hallu — no fabricated bibdata produced).

## Mechanism (1 paragraph)

N=1 SUGRA, flavour modulus τ + dilaton S. Superpotential $W=\Lambda_W^3\,\Omega(S)\,H(\tau)/\eta^6(\tau)$ with $H(\tau)=(j-1728)^{m/2}j^{n/3}P(j)$; tree-level $K\propto-\log(S+\bar S)$ + Shenker-like $O(e^{-1/g_s})$ corrections. **Key kinematic fact**: $\partial_\tau V$ has modular weight 2, so under $S$-action at τ=i, $(\partial_\tau V)|_i=(-i)^2(\partial_\tau V)|_i \Rightarrow \partial_\tau V \equiv 0$ at τ=i. Same logic via $ST$ (order 3) at τ=ω. Hessian positive (KW App. C). **Result: dS minima precisely at τ=i and τ=ω**.

## Compatibility checks

- **(a) CM-by-Q(i) requirement?** NO — KW is purely modular-kinematic, makes no reference to CM points, Heegner values, periods, or Q(i). KW gives both i and ω vacua; ECI's A14 cross-K test selects τ=i uniquely.
- **(b) Add CM-anchor without contradiction?** YES — KW shapes V(τ,S); CM-anchor selects which KW minimum is realised. Disjoint mathematical objects, no double-counting.
- **(c) Cassini-clean ξ→0⁺ survival?** YES — KW τ is a SUGRA modulus, $m_\tau \sim m_{3/2}$ (TeV–10¹² GeV); fifth-force/Cassini constrains scalars with $m<10^{-12}$ eV. Different scalar from ECI's NMC cosmological one. Trivially evades.

## How A47 closes A14's "WHY τ=i?" gap

A14 deferred: *"modular-flavor literature does NOT motivate τ=i from CM number theory"*. KW supplies a string-cosmo (physical) reason for τ→i,ω; ECI's CM-by-Q(i) anchor selects between {i,ω} via cross-K test. **Empirical-deepness assessment: upgrade ~20% → ~35–40%**.

## Honest deficits in KW (not blockers)

1. No numerical $m_\tau$ or $\Lambda_W$ (Λ_W left free).
2. No CM/class-field-theory connection (ECI fills unilaterally; OK).
3. No ξ/kinetic-mixing discussion (assumed zero; consistent with ECI ξ→0⁺).
4. dS uplift Shenker-type, not KKLT-tuned, but no strict no-tuning theorem.

## v7.4 §3.5 LaTeX patch (insertion point)

Insert between `v74_amendment_v2.tex` line 298 (close of $H_7'$ BDP axiom) and line 300 (start of §4). New `\subsection{Physical mechanism for the τ=i fixed point: the King-Wang multi-modulus dS-trap}` containing: (i) the W,K,H formulas; (ii) the weight-2 fixed-point kinematic argument; (iii) three bullets — *independent of arithmetic*, *different scalar from NMC sector*, *two-vacuum testable prediction*; (iv) explicit deficit notes. Bibitem `KW23` to add after `BDP13` block.
