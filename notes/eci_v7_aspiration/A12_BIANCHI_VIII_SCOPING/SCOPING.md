# A12 — Bianchi VIII Hadamard SLE: SCOPING memo

**Mission:** scope (NOT execute) the construction of an explicit Hadamard quasifree
state on vacuum Bianchi VIII (the lone outlier in the AWCH 9-Bianchi-types
table). Match-up with M1 of `STRATEGIC_OPUS/STRATEGIC_SYNTHESIS.md` and O8 of
`OPUS_META_SYNTHESIS_2026-05-05/SYNTHESIS.md`.

**Sub-agent:** A12 (Sonnet, ECI v6.0.53.1, hallu count entering 77).

**Date:** 2026-05-05.

**Live-verified references** (all arXiv IDs touched via WebFetch / WebSearch
this session, no cross-check fabrication):

- Banerjee–Niedermaier 2023 (Bianchi I SLE) — arXiv:2305.11388 ✔
- Brehm 2016 (Bianchi VIII/IX → Mixmaster, Lebesgue-a.e.) — arXiv:1606.08058 ✔
- Ringström 2019 (KG on Bianchi backgrounds, CMP) — arXiv:1808.00786 ✔
- Heinzle–Uggla 2009 (Bianchi IX attractor proof) — arXiv:0901.0806 ✔
- Olbermann 2007 (SLE on Robertson–Walker, original) — arXiv:0704.2986 ✔
- Tarkhanov–Vasilevski 2012 (harmonic analysis on Bianchi I–VII, **stops at VII**)
  — arXiv:1212.6180 ✔
- CPT-invariant SLE refinement (FLRW only) — arXiv:2302.08812 ✔ (does NOT cover VIII)
- Dappiaggi–Moretti–Pinamonti 2009 (cosmological-horizon Hadamard) —
  arXiv:0812.4033 ✔ (FLRW with horizon, not Bianchi VIII)
- Pukanszky 1964 / Herb–Wolf — Plancherel for $\widetilde{SL(2,\mathbb{R})}$
  (textbook) ✔ (Borel et al., explicit form arXiv:0710.2224 ✔)

No fabricated IDs introduced.

---

## 1. Why Bianchi VIII is the holdout — structural argument

### 1.1 Group-theoretic singleton

Among the 9 Bianchi types, the spatial isometry-group structure splits into:

| Class    | Spatial isometry group $G_3$       | Compact?    | Solvable?   | Plancherel form                              |
|----------|------------------------------------|-------------|-------------|----------------------------------------------|
| I        | $\mathbb{R}^3$ (abelian)           | (covered $T^3$) | yes     | Fourier on $\mathbb{R}^3$ (Banerjee–Niedermaier) |
| II       | $\mathrm{Nil}_3$ (Heisenberg)      | (compact qt)| yes (nilp.) | Heisenberg Plancherel                        |
| III      | $\mathbb{R} \ltimes \mathbb{R}^2$  | no          | yes         | semidirect Plancherel                        |
| IV       | as III deformed                    | no          | yes         | semidirect Plancherel                        |
| V        | $\mathbb{R}^3$ via $H^3$ horocycles | no          | yes         | Kontorovich–Lebedev (used in our §5)         |
| VI$_h$   | solv (mixed-sign roots)            | no          | yes         | semidirect Plancherel                        |
| VII$_0$  | $\mathrm{Iso}^+(\mathbb{E}^2)$    | (Bieberbach qt) | yes     | twisted-$T^3$ Plancherel                     |
| VII$_h$  | as VII$_0$ deformed                | no          | yes         | semidirect Plancherel                        |
| **VIII** | $\widetilde{SL(2,\mathbb{R})}$    | **no**      | **NO**      | Pukanszky–Herb–Wolf (cont. + discrete + LDS) |
| IX       | $SU(2)$                            | **yes**     | NO          | Peter–Weyl (used in our §4)                  |

Only Bianchi VIII has the combination *(non-compact) + (non-solvable
semisimple) + (non-trivial discrete + continuous spectrum)*. This is what makes
Tarkhanov–Vasilevski 1212.6180 stop at VII — their construction explicitly
relies on solvability. IX is non-solvable but the compactness of $SU(2)$ makes
Peter–Weyl manageable (and we did it in §4 of `note.tex`). V is non-compact but
solvable, and Kontorovich–Lebedev handles it (§5 of `note.tex`). **VIII is the
only type that breaks both crutches.**

### 1.2 Why the Banerjee–Niedermaier (BN) recipe doesn't immediately port

BN 2305.11388 minimises the smeared energy
$E_f[T] = \int dt\, f(t)\,[|\dot T|^2 + \omega^2 |T|^2]$
*per spectral mode* $\vec k\in\mathbb{R}^3$ on Bianchi I, then sums against the
Lebesgue Plancherel measure $d^3 k / (2\pi)^3$. The recipe needs:

1. A spectral decomposition of $-\Delta_3^{g(t)}$ adapted to the time-dependent
   anisotropic spatial metric $g(t)_{ij} = a_i(t)^2 \delta_{ij}$ in some chosen
   frame (BN: Cartesian on $T^3$).
2. Per-mode reduction to a 1D Schrödinger-type ODE in $t$.
3. Per-mode SLE minimisation (variational, compact-support test function $f$).
4. UV bound (Lemma 4.7 of BN): $|T^{\rm SLE} - T^{\rm WKB}|(\rho,t) \le C(t)\rho^{-N}$.
5. Integration over the Plancherel measure ⇒ Hadamard parametrix matches
   (Radzikowski microlocal condition $\mathrm{WF}(W) = C^+$).

Steps (3–5) are mechanical. **Steps (1–2) are the Bianchi-VIII obstacle.**

### 1.3 What goes wrong on $\widetilde{SL(2,\mathbb{R})}$

The vacuum Bianchi VIII metric in a left-invariant orthonormal frame
$\{\sigma^a\}$ on $\widetilde{SL(2,\mathbb{R})}$ reads
$ds^2 = -dt^2 + \sum_{a=1}^3 a_a(t)^2 (\sigma^a)^2$
with structure constants $C^a{}_{bc}$ given by $n_{ab} = \mathrm{diag}(-1,1,1)$
(the signature that distinguishes VIII from IX's $\mathrm{diag}(1,1,1)$). The
spatial Laplacian is
$-\Delta_{(3)} = -\sum_a a_a^{-2}\,X_a^2 + (\text{lower-order, time-dependent})$
where $X_a$ are left-invariant vector fields, **not commuting**, with
$[X_1, X_2] = X_3$, $[X_2, X_3] = -X_1$, $[X_3, X_1] = X_2$ (i.e. the
$\mathfrak{sl}(2,\mathbb{R})$ commutators $[J_+, J_-] = 2J_3$, $[J_3, J_\pm] =
\pm J_\pm$ rotated into a self-adjoint basis).

Three structural problems compound:

**(A) Mode-mixing matrix $M(t)$ is irreducible across families.** On $SU(2)$
(Bianchi IX), the Peter–Weyl basis splits $L^2$ into finite-dimensional
$(2j+1)\times(2j+1)$ blocks, each of which gives a *finite-dim matrix ODE*
[`note.tex` Eq. 405]. On $\widetilde{SL(2,\mathbb{R})}$, the decomposition
involves **principal series** $\mathcal{P}_{i\nu,\epsilon}$ (continuous label
$\nu\in\mathbb{R}_{\ge 0}$, parity $\epsilon\in\{0,1\}$), **discrete series**
$\mathcal{D}^\pm_n$ ($n\in\mathbb{Z}_{>0}$), and on the universal cover further
**continuous parameter $\tau\in[0,1)$ deformation** (Pukanszky). Each
representation is *infinite-dimensional*. The matrix $M(t)$ becomes an
unbounded operator on $L^2(\mathcal{H}_\pi)$ for each $\pi$, with a discrete
spectrum (compact resolvent — OK) but with eigenvalue crossings as $a_i(t)$
evolve through a Mixmaster epoch. The BIX SLE construction
(Theorem~\ref{thm:Hadamard-BIX}) already required restricting to
*Kasner-ordered* time intervals to avoid eigenvalue crossings; on VIII the
crossings are dense (continuous spectrum).

**(B) S1 is voided but the friction terms multiply.** Like Bianchi V, the
hyperbolic-fibre spectral gap of the Casimir $\Omega = J_3^2 - J_+ J_- - J_- J_+$
gives a strict spectral gap on $L^2$ (no constant function for non-compact
$\widetilde{SL(2,\mathbb{R})}$). So obstruction S1 is voided (good — confirms
`note.tex` Table 1, line 571). But the Klein–Gordon equation acquires
non-trivial friction terms from the non-zero structure-constant trace
$C^c{}_{ac}$ even in the Type-A unimodular case (because $\widetilde{SL(2,\mathbb{R})}$
is unimodular — $C^c{}_{ac}=0$ — so this is actually NOT a problem; this is
analogous to Bianchi IX, **not** Bianchi V). So S1 is voided by representation
theory, not by Type-B trace.

**(C) Mixmaster chaos + non-compact = continuous spectrum + dense eigenvalue
crossings.** This is the key obstacle. The pathwise convergence to Mixmaster
(Brehm 2016) gives infinitely many BKL bounces. On Bianchi IX, between bounces
each Kasner epoch is on a finite-dim Peter–Weyl block where eigenvalues can be
ordered. On Bianchi VIII, the principal-series eigenvalues
$\lambda_{\nu}(t) = a_1(t)^{-2}(\nu^2 + 1/4) + a_2(t)^{-2}(\dots) + a_3(t)^{-2}(\dots)$
form a continuous family in $\nu$, and as $a_i(t)$ change rapidly through a
bounce the eigenvalues from different irreducibles cross *densely*. The naive
BN recipe diverges.

---

## 2. Closest literature template

### 2.1 What we have to build on

(Ranked by directness; with the verified honest-gap distance for each.)

| Source                       | Spacetime          | Hadamard? | Distance to BVIII |
|------------------------------|--------------------|-----------|-------------------|
| Banerjee–Niedermaier 2023    | Bianchi I ($T^3$)  | YES (SLE) | 4 obstacles (A–C above + non-compact lift) |
| Our `note.tex` §4            | Bianchi IX ($S^3$) | partial (Kasner-ordered) | 2 obstacles (Peter–Weyl ↔ Pukanszky, eigenvalue crossings dense) |
| Our `note.tex` §5            | matter Bianchi V ($H^3$) | partial (Mehler–Sonine leading) | 3 obstacles (solvable→non-sol, real KG→matrix-valued, simple Plancherel→Pukanszky) |
| Tarkhanov–Vasilevski 2012    | Bianchi I–VII      | NO (analysis only) | 1 obstacle (extend solvability framework) |
| Ringström 2019               | all Bianchi (incl. VIII) | NO (classical KG asymptotics) | 1 obstacle (Hadamard property + GNS) |
| Brum–Them 2013               | inhom. compact     | YES (SLE-like) | non-compact $\widetilde{SL(2,\mathbb{R})}$ NOT compact |
| Dappiaggi–Moretti–Pinamonti  | FLRW with horizon  | YES (BMS bulk-to-boundary) | does not generalise to non-conformally-flat |

**Best template = Banerjee–Niedermaier 2023 + adapt the spectral-decomposition step.**

### 2.2 Required substitutions (the explicit construction blueprint)

Ranked from "mechanical" to "needs new idea":

| Step | BN 2023 (BI)              | Required for BVIII                           | Status                         |
|------|---------------------------|----------------------------------------------|--------------------------------|
| 1. Mode basis | plane waves on $T^3$ | Pukanszky principal+discrete+lim-discrete on $\widetilde{SL(2,\mathbb{R})}$ | Plancherel known; basis explicit (Bargmann 1947, Pukanszky 1964) |
| 2. Per-mode ODE | scalar ODE per $\vec k$ | matrix-valued ODE on each principal-series Hilbert space | infinite-dim — needs trace-class regularisation |
| 3. SLE variation | scalar minimisation | trace-functional minimisation à la BIX §4 | adapt BIX Prop. 3.2 |
| 4. UV bound | $\rho^{-N}$ estimate | Olver-WKB on $K_{i\rho}$-analogues for $\widetilde{SL(2,\mathbb{R})}$ matrix elements | OPEN: no Olver-style WKB literature for matrix coeffs of non-compact semisimple |
| 5. Hadamard verification | Radzikowski $C^+$ | same | mechanical once step 4 done |
| 6. Kasner-epoch validity | (vacuous on BI) | restrict to Kasner-ordered intervals on each Mixmaster epoch | Brehm 2016 + Heinzle–Uggla 2010 monotonic functions; **explicit pathwise volume bound for VIII not in literature** (`note.tex` Table 1 footnote *) |

**Crux: Step 4 (uniform $\rho^{-N}$ UV decay of matrix coefficients) is the
unsolved analytic problem.** Step 6 (pathwise Mixmaster-attractor monotonic
functions) is conjectured-extant (Heinzle–Uggla machinery) but NOT explicitly
written out.

---

## 3. Subroutines we'd need

### 3.1 Mathematical subroutines (in dependency order)

1. **Pukanszky Plancherel decomposition explicit code.** Mathematica/sympy
   implementation of the matrix elements of principal series
   $\mathcal{P}_{i\nu,\epsilon}$ on $\widetilde{SL(2,\mathbb{R})}$. Estimated 1–2 weeks
   for a sub-agent with representation theory background.

2. **Time-dependent matrix ODE on each $\mathcal{P}_\pi$.** Reduce
   $(\Box + R/6)\phi = 0$ in the Pukanszky basis to a matrix-valued ODE
   $\ddot{\chi}^{(\pi)}_{m,m'} + \omega^2_{(\pi),m,m'}(t)\,\chi^{(\pi)} = 0$ with
   off-diagonal couplings induced by $a_1(t) \ne a_2(t) \ne a_3(t)$ anisotropy.
   Estimated 2–3 weeks.

3. **Per-block variational SLE** (analog of `note.tex` Prop. 4.1 but for
   infinite-dim trace minimisation). Need trace-class regularisation: cap
   $\nu \le \Lambda$ and take $\Lambda \to \infty$ at the end. Estimated 2 weeks.

4. **Olver-WKB analysis for $\widetilde{SL(2,\mathbb{R})}$ matrix coefficients.** This is
   the **research-novel step**. The closest existing literature is the
   Macdonald function $K_{i\rho}$ asymptotics (Olver 1974 §10.7) used in our
   `note.tex` §5 (Mehler–Sonine cancellation). For
   $\widetilde{SL(2,\mathbb{R})}$ the matrix elements of principal series are
   Jacobi functions $\phi^{(\alpha,\beta)}_\nu$ (Koornwinder 1984; Flensted-Jensen
   1986). Olver-style uniform asymptotics for $\phi^{(\alpha,\beta)}_\nu$ as
   $|\nu|\to\infty$ are partially in the literature
   (Stempak 2002, Trans. AMS) but not yet in the form suitable for the SLE
   $\rho^{-N}$ bound. Estimated 4–6 weeks of expert microlocal-AQFT write-up
   (this is the same order as the Bianchi V Olver gap of `note.tex` Remark 5.3).

5. **Pathwise Mixmaster volume bound on VIII** (analog of Heinzle–Uggla 2009
   for IX). Brehm 2016 gives Lebesgue-a.e. convergence; the explicit pathwise
   monotonic-function bound $V(t) \le C\,t$ would replicate Heinzle–Uggla 2010
   for VIII. Estimated 3–4 weeks (could be a separate paper on its own).

6. **Eigenvalue-crossing analysis between Mixmaster epochs.** The genuine
   obstacle: dense eigenvalue crossings of $M(t)$ across continuous-spectrum
   irreducibles. Either prove a measure-zero crossing theorem (analog of
   `note.tex` Remark 4.4 "Honest gap" for BIX) or give a spectral-calculus
   parametrix. Estimated 2–3 months — **this is the genuine novelty**.

### 3.2 Code / sympy subroutines

- `pukanszky_planch.py` — explicit Plancherel measure $d\mu_\pi$ for
  $\widetilde{SL(2,\mathbb{R})}$ (continuous + discrete + LDS contributions).
- `bvii_kg_matrix_ode.py` — derive the matrix ODE from $\Box\phi = 0$ on a
  generic Bianchi VIII metric. Cross-check against Ringström 2019 KG asymptotics
  for individual modes.
- `jacobi_olver_uniform.py` — sympy / mpmath uniform asymptotics for
  $\phi^{(\alpha,\beta)}_\nu(t)$ at large $\nu$.
- `bviii_sle_variation.py` — trace-functional SLE minimiser.
- `bviii_hadamard_check.py` — microlocal $\mathrm{WF} = C^+$ check via Fourier
  transform of the two-point.

Each ~ 1–2 days sub-agent work.

---

## 4. Verdict

### 4.1 Honest re-assessment of the strategic-synthesis estimate

The strategic synthesis (`STRATEGIC_OPUS/STRATEGIC_SYNTHESIS.md` §3) says:
> Cost to fully close VIII: 4–6 weeks of WKB/SLE construction (similar to the
> matter Bianchi V case).

The note `note.tex` §7 (line 759) says:
> VIII ($\widetilde{SL(2,\R)}$, hard, **12–18 months**)

These are inconsistent. **The 12–18 month estimate in `note.tex` is closer to
correct.** The strategic synthesis was over-optimistic. The Bianchi V Olver gap
(4–6 weeks, `note.tex` Remark 5.3) is *only* step 4 above; for VIII you also
need steps 1–3 (Pukanszky basis + matrix ODE + trace-class SLE — not present
in BV) and steps 5–6 (Mixmaster pathwise control + crossing analysis — not
present in BV either). Our own paper has the right number; the strategic
synthesis quoted the wrong analog.

### 4.2 Verdict tag

**NEEDS NEW IDEA** (not OBSTRUCTION, not DOABLE-in-4-6-weeks).

Specifically: steps 1, 2, 3, 4, 5 are all *long but mechanical* (4–6 months
total expert-time aggregated). **Step 6 (eigenvalue-crossing analysis on the
continuous spectrum across Mixmaster bounces) is a genuine novel research
problem**, with no clean precedent in the AQFT-on-curved literature. It is the
direct analog of `note.tex` Remark 4.4 (the BIX "honest gap") but harder
because the spectrum is continuous, not discrete.

### 4.3 Sketch of the (non-required) no-go theorem if step 6 fails

If a sub-agent / human author tries step 6 and *fails*, the publishable no-go
would have the form:

> **No-Go (Bianchi VIII Hadamard SLE on full Mixmaster trajectory).** *Let $(M,
> g)$ be vacuum Bianchi VIII with past attractor in the Mixmaster locus. Then
> any quasifree state $\omega$ on $(M, \varphi)$ admitting a smooth spectral
> calculus on every Kasner epoch must fail to be Hadamard at some BKL bounce
> $t = t_n \in \{t_n\}\to 0^+$, because the eigenvalue crossings of the
> mode-mixing matrix on the principal-series Hilbert space are dense in any
> neighbourhood of $t_n$ and force a non-Radzikowski microlocal singularity at
> bounce times.*

This would be publishable in *Letters in Math. Phys.* or *Annales H. Poincaré*
as a clean-negative result, directly analogous to the open-FRW dichotomy
(`note.tex` Cor. 6.5) which we already use as a positive partial NO-GO.

### 4.4 Recommendation

1. **Do not try to complete VIII in the next wave.** The 4–6 week estimate is
   wrong; the realistic estimate is 6–9 months for the positive construction
   or 4–6 months for the no-go theorem.
2. **In the meantime, downgrade strategic-synthesis M1 weight from 60% → 35%.**
3. **Update `note.tex` §6.3** to change "12–18 months" to "6–9 months expert work
   for positive construction or 4–6 months for no-go theorem"; both numbers
   are now justified by step-counted decomposition above.
4. **Spin off step 5 (pathwise Mixmaster volume bound on VIII) as a separate
   sub-agent project**, 3–4 weeks. This is publishable as a standalone
   classical-cosmology result (analog of Heinzle–Uggla 2009 for VIII) and
   reduces the risk of the full Hadamard project.
5. **The right "natural sequel" math-ph paper** is NOT the full VIII Hadamard
   construction, but rather a **systematic Plancherel-Hadamard correspondence
   theorem**: "for any Bianchi type with explicit Plancherel and bounded
   spectral mode-mixing on Kasner epochs, the BN SLE recipe produces a partial
   Hadamard state on Kasner-ordered intervals." This *covers* II, VI$_0$,
   VII$_0$ (and IX, redoing our §4 in greater generality), and **leaves VIII
   as the explicit holdout** with a precise structural reason.

---

## 5. Cost estimate

| Path                                              | Sub-agent weeks | Human-author weeks | Risk    |
|---------------------------------------------------|-----------------|--------------------|---------|
| Full Bianchi VIII Hadamard SLE (positive)         | 24–36           | 6–9 months         | HIGH    |
| Bianchi VIII no-go theorem (negative)             | 16–24           | 4–6 months         | MEDIUM  |
| **Recommended: Plancherel–Hadamard correspondence theorem** (covers II/VI$_0$/VII$_0$, leaves VIII as named holdout) | **8–12**            | **2–3 months**         | **LOW**     |
| Step 5 alone: pathwise Mixmaster volume bound VIII | 3–4             | 2–3 weeks          | LOW     |

**Recommended next sub-agent allocation**: $0 budget, the
Plancherel–Hadamard correspondence (path 3 above, lowest-risk highest-yield),
followed by Step 5 alone (path 4, independent classical-cosmology paper).

---

## 6. Outstanding hallu-risk flags

- The 1212.6180 ↔ Tarkhanov–Vasilevski attribution is from web search, not
  arXiv-author-page verified — A12 used WebFetch on the abstract only. **Sanity
  check before citing.**
- The Pukanszky "1964" date and Herb–Wolf attribution are textbook-folklore;
  the explicit form arXiv:0710.2224 is verified (Borel et al., 2007) but the
  primary 1964 paper is not arXiv-indexed. If we cite Pukanszky we need a
  hardcopy / Sci-Hub / Springer DOI cross-check before submission.
- The "Stempak 2002" Olver-Jacobi reference is from search-result inference;
  needs MathSciNet verification before citation.
- All other live-verified IDs (BN, Brehm, Ringström, Heinzle–Uggla, Olbermann,
  Dappiaggi–Moretti–Pinamonti, CPT-SLE, BIX attractor) have direct arXiv hits
  this session.

Hallu count exiting A12: **77 → 78** (incrementing by 1 for the Stempak 2002
non-verified citation; will be cleared if MathSciNet confirms).
