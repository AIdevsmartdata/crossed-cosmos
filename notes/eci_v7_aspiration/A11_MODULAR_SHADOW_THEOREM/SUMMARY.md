# A11 — Modular Shadow finite-rank theorem (bound vs saturation split)

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A11 (parent persisted; harness blocked Sonnet's direct write)
**Hallu count entering / leaving:** 77 / 77 (no fresh fabrications; counter-examples to saturation found)

## Verdict (one line)

**PROVABLE TODAY at finite-rank as a *bound* (λ_L^modular ≤ 2π/β); NOT provable as a *saturation* theorem** — the saturation step requires extra chaotic/holographic input. The strong "MSS bound IS the modular shadow of type-II_∞" claim must be downgraded: free-QFT counter-examples refute the converse.

## Live-verified references (5/5 confirmed via WebFetch)

| Tag | arXiv | Verified content |
|---|---|---|
| MSS2015 | 1503.01409 | "A bound on chaos", λ_L ≤ 2π k_B T/ℏ |
| Caputa2024 | 2306.14732 | "Krylov complexity of modular Hamiltonian evolution", PRD 109 086004; λ^mod_L = 2π in 2D CFT |
| FaulknerSperanza2024 | 2405.00847 | "Gravitational algebras and the GSL"; crossed-product entropy = S_gen via Wall monotonicity. **Does NOT explicitly identify S_gen with C_K^mod** — ECI's §sec:mss-shadow over-attributes here. |
| HellerPapalini2024 | 2412.17785 | "Krylov spread complexity as holographic complexity beyond JT gravity"; DSSYK / sine-dilaton, C_K = C_V at finite T |
| Parker2019 | 1812.08657 | rigorous λ_K ≤ 2α bound (sharper than MSS); workhorse for the finite-rank theorem |

## NEW competing/related reference (potential SCOOP — must cite)

**Vardian, "Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands"**, arXiv:**2602.02675** (2026-02-02). Single-author hep-th. Reconstructs QES area operator from boundary modular Lanczos coefficients — overlaps significantly with ECI's modular shadow framing. Does not explicitly state the MSS-saturation theorem (per abstract), but ECI v7+ must cite it to establish novelty boundary.

**Live-verified arXiv ID 2602.02675 ✓** (parent re-verified post-A11). **Caveat (per A10 catch):** Vardian focuses on AdS/CFT boundary reconstruction, NOT on DSSYK or de Sitter K_R. So the threat to our framing is REAL but BOUNDED — Vardian doesn't cover the dS / type-II_∞ angle.

## Counter-examples (3 — strong)

1. **Free QFT / scalar fields** have linear b_n and exponential C_K despite integrability (Avdoshkin–Dymarsky arXiv:1911.09672; Camargo et al. 2212.14702). Refutes "saturation ⇒ chaos" and a fortiori the strong "saturation ⇔ type-II_∞" converse.
2. **Initial-state dependence** (Sreeram, Kannan, Modak, Aravinda, PRE 112 L032203, 2025; arXiv:2503.03400): Krylov saturation depends on IPR of initial operator; "universal" Lyapunov is operator-dependent at finite N.
3. **Integrable saddle-point models** mimic exponential Krylov (false-positive chaos).

## Theorem (provable today, finite rank)

> **Theorem (Modular Lyapunov Bound on Finite-Rank Type-II_∞ Truncation).**
> Let M_R ⊗ B(H_n) be a finite-rank truncation of the type-II_∞ crossed-product algebra at KMS inverse temperature β = 2π. Let K_R be the modular Hamiltonian and C_K(s) the spread complexity of an operator O ∈ M_R under modular flow s ↦ e^{i K_R s} O e^{-i K_R s}. Then:
> (i) C_K(s) ≤ A · cosh(2 b_1 s) for some operator-dependent A > 0;
> (ii) the Lanczos coefficients satisfy b_n ≤ n · π/β + o(n), giving λ_K^mod ≤ 2π/β;
> (iii) saturation b_n = n · π/β requires the modular two-point function to have the universal hyperbolic form C(s) = (2 sinh(πs/β))^{-Δ} for some Δ > 0 — a *kinematic* (BW-type) condition equivalent to geometric modular flow on the truncation.

**Proof sketch (1-2 pages, methods)**:
- (i) Standard tridiagonal-Lanczos inequality (Parker et al. 2019, eq. (1.2)) applied to the modular Liouvillian L = [K_R, ·] instead of physical [H, ·]. Inner product is the KMS state on the truncation; Tomita-Takesaki on a finite II_∞ matrix factor reduces to standard GNS.
- (ii) On the truncation, BW theorem (still valid: Bisognano-Wichmann holds in the wedge restriction at every UV cutoff) gives modular boost generator with spectrum scaling at most linearly in n. Direct computation of b_n via the Hankel determinant of modular two-point moments yields the universal slope π/β.
- (iii) Saturation step: equality b_n = n·π/β is the "universal operator growth hypothesis" condition. The two-point function constraint follows by inverse Lanczos (Parker et al. Theorem 2). For type-II_∞ truncations of *Bisognano-Wichmann modular flow* it is automatic; for *generic* modular flow on the truncation it may fail (free-QFT counter-example).
- The ECI saturation identity (1/S_gen) dS_gen/dτ|_sat = 2π T_H/ℏ enters only as the *interpretation* of (ii) under the conjectural bridge S_gen ↔ C_K^mod. The bridge itself is **not** proven by FS24 — it is a working identification.

## Counter-example check (do we know any case where this fails?)

Yes — the **inequality** (parts i, ii) does NOT fail (it's Parker et al. for any KMS inner product). The **saturation** (part iii) **fails for free QFT** in the sense that integrable systems also saturate, breaking the "saturation ⇔ chaos / type-II_∞" reading. So the *theorem* as stated is robust; the *physical interpretation as a chaos diagnostic* is not.

## Files relevant to the work

- `/root/crossed-cosmos/notes/eci_v7_aspiration/MODULAR_SHADOW/modular_shadow_LMP.tex` (existing 553-line draft, v6.0.44 era — uses "[CONJECTURE]" tag throughout, internally consistent but does **not** distinguish bound vs saturation, and does **not** cite Vardian 2602.02675).
- `/root/crossed-cosmos/paper/eci.tex` lines 406–440 (§sec:mss-shadow, the in-paper version flagged as "working conjecture").

## Recommended next step

**Option A (recommended, ~1 day)**: edit `eci.tex` §sec:mss-shadow to (a) cite Vardian 2602.02675, (b) split the conjecture into "bound form (provable, this work)" vs "saturation form (open, free-QFT counter-example precludes converse)", (c) state the finite-rank bound theorem as a proper theorem with proof referenced to Parker et al. + BW.

**Option B (4-6 weeks math-ph)**: full LMP submission of *only* the bound theorem. Title: "A Modular Lyapunov Bound for Finite-Rank Type-II_∞ Crossed-Product Algebras". Math-ph only, no cosmology, no ρ. Cite Vardian as concurrent independent work on the area-operator side.

**Option C (fallback if Vardian scooped us)**: drop modular shadow from ECI v7+ entirely; keep only qualitative remark on shared 2π BW prefactor.

## Discipline log

- 5 arXiv refs live-verified (no Mistral usage).
- 1 new competing reference discovered (Vardian 2602.02675, parent re-verified ✓).
- 1 strong counter-example class identified (free QFT / Avdoshkin-Dymarsky 1911.09672 + Camargo 2212.14702 + Sreeram 2503.03400).
- No fabrications introduced.
- **Hallu exit count: 77** (held; net -2 if Vardian discovery + downgrade survive triangulation).
