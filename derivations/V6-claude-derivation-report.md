# V6 Derivation Report — ECI Composite Entropy-Rate Equation

**Target.** `dS_gen[R]/dtau_R = kappa_R * C_k[rho_R(tau)] * Theta(PH_k[delta n(tau)])`
with `Theta = exp[-(PH_k/PH_c)^alpha]`, `alpha = 0.095`.

**Cross-reference.** External Claude.ai audit archived at
`paper/_internal_rag/v6_audit.md` (read 2026-04-21). This report disagrees
with the audit on one dimensional claim (see §3 below).

---

## 1. Attempt 1 — variational / FSK first law. Status: **PARTIAL**

Script: `derivations/V6-variational-derivation.py`.

Starting from Faulkner-Speranza-Kirklin (FSK) first law for the
type-II crossed product,
`delta S_gen = beta (delta <H_mod> - delta W_mod)`, differentiation in
modular proper time gives
`dS_gen/dtau = beta (d<H_mod>/dtau - dW_mod/dtau)`.

The target is recovered under two identifications:

- **(I1)** `d<H_mod>/dtau = v_C * C_k` — *heuristic*, Brown-Susskind
  "complexity = action/momentum" analogy, NOT a theorem on type II_1 /
  II_inf algebras.
- **(I2)** `dW_mod/dtau = v_C * C_k * (1 - Theta)` — *postulated* to make
  the gate `Theta` emerge; no independent derivation.

With these, sympy verifies the algebraic match: residual = 0 under
`kappa = beta * v_C` (see script output, `assert` passes). The FSK anchor
is rigorous; the two identifications are not. **Ansatz motivated, not
derived.**

## 2. Attempt 2 — Fan-2022 Krylov bridge. Status: **FAIL**

Script: `derivations/V6-krylov-to-kdesign.py`.

Fan 2022 (`|dot S_K| <= 2 b_1 Delta S_K`) combined with the
post-scrambling heuristic `S_K ~ log C_K` (Barbón-Rabinovici-Shir-Sinha
2019) yields `dS_K/dt ~ dot C_K / C_K` — **logarithmic** in complexity.
The target wants a **linear** dependence `dS/dt ~ C_k`. Bridging further
requires (a) `S_K -> S_gen` promotion (different entropies) and (b)
`C_K -> C_k` identification (Krylov vs. k-design; only O(poly) related in
specific random-circuit models, Haferkamp 2022). Neither is licensed by
Fan 2022. This is the component the audit itself flags as highest
scoop-risk (3.5/5) and highest derivational risk.

## 3. Dimensional analysis. Status: **CONSISTENT (with caveat)**

Script: `derivations/V6-dimensional.py`.

`[S_gen] = nat`, `[tau_R] = s`, `[C_k] = [Theta] = 1`
`=>  [kappa_R] = nat / s` (i.e. `nat * t^-1`).

**Discrepancy with `v6_audit.md §2`**, which lists `[kappa_R] = nat * t^-2`.
That row is dimensionally inconsistent with the equation as written: the
left-hand side is a first derivative in `tau_R`, so an inverse-time (not
inverse-time-squared) is required on the right. This is a load-bearing
typo in the audit; flagging it here for the owner.

The external-review suggestion identifying `kappa_R` with the chameleon
exponent `alpha = 0.095` is a **dimensional category error**
(dimensionless vs. rate) — already noted in `v6_ideas.md §3(b)` and
reconfirmed here. Defensible first-principles forms:
`kappa_R ~ 2 pi T_R` (de Sitter modular temperature, with a "nat per
modular e-fold" convention supplying the information unit) or
`kappa_R ~ v_Haferkamp` (linear-growth rate for random local circuits).

## 4. Self-consistency with §3-4 predictions. Status: **PRESERVES (by non-overlap)**

The equation lives in the QRF / type-II / complexity sector (A1+A3+A6).
It does not enter the §3 DESI-DR2 pipeline, the §3.5 `xi_chi` posterior,
the D7 Cassini bound `|xi_chi| <= 2.4e-2`, the D14 `G_eff(a)/G_N - 1`
scaling, or the §3.6 Swampland bound. None of these depend on `S_gen`,
`C_k`, or `PH_k`. So the equation neither reproduces nor contradicts them
at the present level of articulation — it simply doesn't reach them.
That is the *core weakness*: as currently written, the equation has **no
D7/D14/D17 testable consequence**. The only quantitative falsifier within
reach would be the `Theta(PH_k)` gate imprint on CMB low-`ell`
(A6, speculative; see `v6_ideas.md §3(c)`).

---

## Overall verdict

**ANSATZ (publishable as a postulate, not as a theorem).**

The equation is algebraically consistent with the FSK first law under two
unproved identifications, fails the Fan-2022 Krylov route (wrong
functional form, log vs. linear), has a clean dimensional check once the
`nat * t^-2` typo in the audit is corrected to `nat * t^-1`, and does not
currently connect to the v5.0 falsifier table.

- **Strongest step (least attackable):** the FSK first-law skeleton
  (`dS_gen/dtau = beta d<H_mod>/dtau - beta dW_mod/dtau`). Wall 2011,
  Faulkner-Speranza 2024, Kirklin 2025 all license this.
- **Weakest step (most attackable):** identification (I1)
  `d<H_mod>/dtau = v_C * C_k`. Brown-Susskind style, no type-II proof.
  Expected referee point of attack.
- **Hidden issue:** the audit's `[kappa_R] = nat * t^-2` is wrong; should
  be `nat * t^-1`. Must be fixed before any `eci.tex` line is written.

**Recommendation.** Present the equation as an *ansatz* extending
Eling-Guedens-Jacobson's `d_i S` schema, not as a derivation. Demarcate
explicitly from Fan 2022 (log vs. linear). Do not reuse `alpha = 0.095`
from D15 screening. Do not promote to v5.0; v6 companion paper only, and
only if a concrete CMB-S4 / LiteBIRD falsifier for the `Theta(PH_k)` gate
can be specified.

## Three questions only the owner can resolve

1. Do you want to commit to the "nat per modular e-fold" convention that
   converts `kappa_R = 2 pi T_R` to the correct `nat/s` units, or
   introduce `kappa_R = v_Haferkamp` as a distinct dimensionful rate?
2. Is (I1) `d<H_mod>/dtau = v_C * C_k` an acceptable *postulate* for the
   v6 paper, or do you want to seek a stronger derivation from
   Caputa-Magán-Patramanis-Tonni 2024 (modular Krylov, `lambda_L^mod =
   2 pi`) before drafting?
3. Which falsifier anchors v6: CMB low-`ell` via `PH_k` (Yip 2024), or a
   laboratory analogue (Barrow `Delta ~ 0.1`)? Without at least one, v6
   is not publishable as a physics paper.

---

*Scripts executed under `.venv-compute/` (sympy 1.14.0, numpy 2.4.2).
All three scripts exit 0; V6-variational passes its `assert`.
Commit SHAs appended at push time.*
