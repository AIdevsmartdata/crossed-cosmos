# V6-F2 report — JT / Killing-horizon consistency of v6 Eq.(1) against Faulkner–Speranza 2024

Status: **PASS** (v6 consistent with FS24 in the JT / Killing-horizon setting).
Saturation: at τ_R = 0 in the classical regime (Θ = 1), v6 RHS touches the FS24 value.
Elsewhere, v6 strictly exceeds the FS24 admissible rate.

Script: `derivations/V6-F2-JT-consistency.py`
RAG source: `paper/_rag/FaulknerSperanza2024.txt` (fetched from arXiv:2405.00847,
JHEP 11 (2024) 099; PDF cached at `paper/_rag/FaulknerSperanza2024.pdf`).

---

## 1. Honesty-gate disclosure

**FS24 does NOT contain a labeled "Theorem 3.1".** A verbatim search of the
paper (`grep '^(Theorem|Proposition|...)'`) returns zero matches. The paper's
central result for the JT / Killing-horizon GSL is an **inequality**, not a
labeled theorem. Per PRINCIPLES.md honesty gate, we do not paraphrase a
"Theorem 3.1" from memory. Instead we quote the actual equations verbatim
and treat them as the FS24 bound.

## 2. FS24 main GSL inequality — verbatim from the RAG cache

From `paper/_rag/FaulknerSperanza2024.txt`, section 3.3 (AdS black hole
horizon cuts), Eq. (3.57):

> Sλ̃ − Sλ = −S_rel^{C_λ̃}(Φ‖Ω) + S_rel^{C_λ}(Φ‖Ω) ≥ 0

Eq. (3.58), the generalized-entropy form:

> ⟨A_λ̃ / 4 G_N⟩ + S_λ̃^out − ⟨A_λ / 4 G_N⟩ − S_λ^out ≥ 0

Section 4.2 (asymptotically flat, Hartle–Hawking), Eq. (4.31):

> S(ρ_λ̃) − S(ρ_λ) = −S_rel^{C0_λ̃}(Φ‖Ω) + S_rel^{C0_λ}(Φ‖Ω) ≥ 0

All three are **one-sided monotonicity** statements:
dS_gen/dτ_R ≥ 0. FS24 fixes a lower bound (zero floor); it does **not**
set a numerical upper bound on dS_gen/dτ_R. The natural upper envelope in
this framework is the modular-chaos saturation of Fan 2022 (arXiv:2202.10480,
already in RAG as `Fan2022.txt`): (dS/dτ)_max ≤ 2π ⟨K_ξ⟩, i.e. O(S_BH) in a
scrambling regime.

## 3. v6 Eq.(1) vs FS24 — side by side

| Quantity | FS24 | v6 Eq.(1) |
|---|---|---|
| Bound direction | lower: dS_gen/dτ ≥ 0 | upper: dS_gen/dτ ≤ κ_R · C_k · Θ |
| Classical (Θ=1) RHS | a_K · S_rel0 · exp(−a_K τ_R) (actual value ≥ 0) | κ_R · C_k (= a_K · S_rel0 with calibration κ_R=2π, C_k=a_K S_rel0/(2π)) |
| Scrambling envelope | 2π · S_BH (Fan 2022) | κ_R · C_k · exp(S_BH) |

"v6 looser than FS24" in this opposite-sided comparison means: the v6
**upper** ceiling never falls below the FS24 **admissible maximum** (either
the current monotonicity value in a specific ansatz, or the Fan-2022
scrambling saturation).

## 4. Numerical check — 5 τ_R test points

With a_K = 1, S_rel0 = 1, S_BH = 10, κ_R = 2π:

| τ_R  | R_v6 (classical) | R_FS (classical) | ratio_cl | R_v6 (scrambling) | R_FS (Fan-2022) | ratio_sc |
|------|------------------|------------------|----------|-------------------|------------------|----------|
| 0.00 | 1.0000           | 1.0000           | 1.0000   | 2.2026e+04        | 62.83            | 350.6    |
| 0.25 | 1.0000           | 0.7788           | 1.284    | 2.2026e+04        | 62.83            | 350.6    |
| 0.50 | 1.0000           | 0.6065           | 1.649    | 2.2026e+04        | 62.83            | 350.6    |
| 1.00 | 1.0000           | 0.3679           | 2.718    | 2.2026e+04        | 62.83            | 350.6    |
| 2.00 | 1.0000           | 0.1353           | 7.389    | 2.2026e+04        | 62.83            | 350.6    |

All ratios ≥ 1 → v6 upper bound is ≥ FS24 admissible rate at every test point.

## 5. Saturation flag

The classical regime with Θ = 1 and the minimal calibration
C_k = a_K·S_rel0/(2π) saturates at **τ_R = 0**: v6 RHS = FS24 floor exactly.
This is the only point where v6 "touches" FS24. No configuration examined
makes v6 *stricter* than FS24.

## 6. Caveats

- FS24 treats Killing horizons generally (AdS black hole §3, asymptotically
  flat §4). It does not specialize to JT gravity by name. JT gravity enters
  as a 2D instance of the same Killing-horizon modular-algebra machinery
  (crossed product with the boost). The calculation above is therefore a
  consistency check in the FS24 class of spacetimes that **contains** JT,
  not a JT-specific theorem.
- C_k, Θ and κ_R are taken with the calibration κ_R = 2π (modular surface
  gravity). A different calibration could in principle let v6 fall below
  FS24; this is a **required calibration constraint** on v6: any admissible
  choice must satisfy κ_R · C_k · Θ(0) ≥ a_K · S_rel0 at τ_R = 0.
- The Fan-2022 envelope is an upper saturation; FS24 itself only guarantees
  monotonicity. The comparison in Regime 2 therefore tests v6 against a
  *separately-sourced* upper bound in the same modular-flow framework, not
  against FS24 directly.

## 7. Verdict

**PASS.** In the FS24 Killing-horizon / JT setting, the v6 main inequality
is consistent with FS24: v6 provides an upper bound on dS_gen/dτ_R that
never falls below the FS24-admissible rate, with a single saturation point
at τ_R = 0 in the minimally-calibrated classical regime.
