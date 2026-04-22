# V8-agent-11: BH 1/4 factor — KMS vs Euclidean Action

**Verdict: CIRCULAR-IDENTIFICATION**

---

## Setup

Starting from the Gibbons-Hawking (1977) Euclidean path integral for Schwarzschild
and the Bisognano-Wichmann / KMS theorem, we track every factor in S_BH = A/(4G).

---

## Derivation Chain

**Step 1 — Regularity (KMS period).**
Near the Euclidean horizon, the metric becomes Rindler-like with
κ = 1/(4GM) (surface gravity). Absence of conical singularity requires
periodicity β_H = 2π/κ = 8πGM. This is identical to the KMS inverse
temperature for the modular flow associated with the Killing horizon.
*KMS fixes T_H = κ/(2π) kinematically, without the action.*

**Step 2 — On-shell Euclidean action.**
The Einstein-Hilbert action (1/(16πG)) + Gibbons-Hawking boundary term gives:

    I_E^{on-shell} = β_H² / (16πG)

Verified symbolically: β_H·M/2 = β_H²/(16πG) with M = β_H/(8πG). ✓

**Step 3 — Entropy via Legendre transform.**

    S = β_H · (∂I_E/∂β_H) − I_E = β_H²/(16πG)

Sympy confirms S/[A/(4G)] = 1 for A = 16πG²M². ✓

**Step 4 — Factor accounting.**
Expressing everything in terms of κ:

    S = (2π/κ)² / (16πG) = 4π² / (16π · Gκ²) = (π/4) / (Gκ²)
    A = π/κ²
    → S = A/(4G)  ✓

The factor of 1/4 = 4π²/(16π) = π/4 per (Gκ²)⁻¹ comes from:
- Numerator 4π² = (2π)²: **KMS period squared**
- Denominator 16πG: **EH action prefactor 1/(16πG)**

Both are necessary.

---

## Why F-3's "2π/8π" claim is circular

F-3 wrote 1/4 = 2π/8π, with 8π from β_H = 8πGM.
But:
1. 8πGM is the *value* of β_H for mass M — a dynamical output, not a KMS input.
2. KMS alone gives β_H = 2π/κ; the identification κ = 1/(4GM) requires the
   Schwarzschild solution.
3. Even granting β_H = 8πGM, the ratio 2π/(8πGM) = 1/(4GM) ≠ 1/4 dimensionally.
4. The entropy coefficient (1/4 in A/4G) needs the 1/(16πG) EH prefactor.
   Without it, KMS yields only a KMS temperature, not an entropy.

---

## Verdict

| Claim | Status |
|---|---|
| KMS identifies T_H = κ/(2π) | **TRUE — kinematic** |
| KMS alone derives S = A/(4G) | **FALSE** |
| 1/4 = 2π/8π is a derivation | **CIRCULAR** |
| 1/4 requires EH action 1/(16πG) | **TRUE** |

**CIRCULAR-IDENTIFICATION**: The KMS modular period provides the factor (2π)²
in the numerator; the EH action prefactor 1/(16πG) provides the denominator.
The 1/4 is their ratio (π/4) combined with geometric factors. It cannot be
derived from KMS structure alone and F-3's 2π/8π claim is a circular
re-labelling of known results, not an independent derivation.

---

*Script*: `derivations/V8-agent-11-bh-factor.py` (sympy, all checks pass)
*Lines*: 192
