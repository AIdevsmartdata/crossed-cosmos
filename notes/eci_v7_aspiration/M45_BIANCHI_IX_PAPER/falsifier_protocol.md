---
name: M45 falsifier protocol — numerical Bianchi IX Modular Shadow test
description: 4-step numerical falsifier for Conjecture M45.1.D (rate identification λ_mod = 2π λ_BKL = π³/(3 log 2) ≈ 14.907). F1 minutes; F2 2-6h on RTX 5060 Ti; F3 1h post-proc; F4 30min sympy
type: project
---

# M45 — Numerical Falsifier Protocol for Conjecture M45.1

**Status:** specification (not yet executed)
**Hallu impact:** 0 (computational, no LLM)

## Predicted target

| Quantity | Predicted value | Source |
|---|---|---|
| λ_BKL = h_KS(σ_Gauss) | π² / (6 log 2) ≈ 2.37314 | Lochs-Khinchin analytic |
| λ_K^mod ceiling | 2π × λ_BKL = π³/(3 log 2) ≈ 14.9069 | TBD-4, TBD-5 |
| β_eff (BKL inverse temp) | 12 log 2 / π ≈ 2.6479 | conjectural |

## F1 — Verify λ_BKL numerically (sanity, minutes)

```python
import numpy as np

def gauss_shift(x):
    return (1.0 / x) - np.floor(1.0 / x)

N, T = 10**6, 10**4
x = np.random.uniform(0.001, 0.999, size=N)
lyap_sum = np.zeros(N)
for _ in range(T):
    # Lyapunov: log|σ'(x)| = log(1/x²) = -2 log x
    lyap_sum += -2.0 * np.log(np.maximum(x, 1e-300))
    x = gauss_shift(x)
    x = np.clip(x, 1e-300, 1 - 1e-12)
lambda_BKL_numeric = np.mean(lyap_sum) / T
print(f"λ_BKL numeric = {lambda_BKL_numeric:.6f}")
print(f"λ_BKL theory  = {(np.pi**2)/(6*np.log(2)):.6f}")
```

**Pass:** |numeric − π²/(6 log 2)| < 1e-3.
**Fail:** Manin-Marcolli framework misimplemented; setup error, NOT M45.1 falsification.

## F2 — Bianchi IX WDW Krylov rate (load-bearing, 2-6h GPU)

Truncate WDW Hamiltonian on Bianchi IX in Misner variables (β_+, β_−, Ω) to harmonic-oscillator basis n_rank=10³.

```python
n_rank = 1000
H_WDW = build_bianchi_IX_WDW(n_rank)        # SO(3)-symmetric
phi_KMS = construct_HH_state(H_WDW)
K_mod  = build_modular_hamiltonian(H_WDW, phi_KMS)

O = generic_local_observable(n_rank)
b = lanczos_coefficients(L=lambda x: K_mod@x - x@K_mod,
                         O=O, depth=200, inner=KMS_inner_product)
slope = np.polyfit(np.arange(50, 200), b[50:200], 1)[0]
lambda_K_trunc = 2.0 * slope
print(f"λ_K^trunc = {lambda_K_trunc:.4f}; ceiling = {(np.pi**3)/(3*np.log(2)):.4f}")
```

**Pass:** λ_K^trunc ≤ 14.907 + truncation_error(n_rank).
**Fail:** Conjecture M45.1.D **falsified**; M45 retracts.

## F3 — Rate comparison

If F1 + F2 both pass:
- saturation (λ_K^trunc → 14.907 as n_rank → ∞): supports M45.1
- strict inequality at all n_rank: weaker than stated (still consistent)
- λ_K^trunc > 14.907 beyond truncation error: **falsification**

## F4 — Lemma A.1 compatibility check (sympy, 30min)

Periodic orbits of Gauss shift σ are exactly quadratic irrationals in [0,1] (Galois 1828). Under Misner ↔ X(2) change (MM §3), they map to eigenvalue-crossing set of paper #5 Lemma A.1.

```python
from sympy import sqrt, Rational, simplify
# 10 random quadratic irrationals; verify image lies on Ricci-eigenvalue-crossing
```

**Pass:** all 10 sample points on eigenvalue-crossing locus.
**Fail:** Lemma A.1 ↔ M45.1 cross-relation breaks (M45.1 still open).

## Falsification budget

If F2 not run within 6 weeks of paper draft, status downgrades from "conjecture-with-falsifier" to "speculative note"; CMP submission paused.

## Hallu / fabrication check

No LLM-generated numerical predictions. λ_BKL, π³/(3 log 2), β_eff are textbook (Khinchin-Lochs) or direct algebraic from MM 2015 Theorem 2.4. Only sympy symbolic + numpy numeric.
