# V8-agent-14: BC β=1 ↔ Hagedorn — Universality verdict

**Date.** 2026-04-22.
**Verdict.** DIFFERENT-BUT-USEFUL.

---

## What was computed

Two canonical partition functions normalised to the same critical point
(β_c = 1):

| System | Z(β) | Divergence exponent ν |
|--------|------|-----------------------|
| Bost-Connes (BC95) | ζ(β) ~ (β−1)^{−1} | ν = 1 |
| Hagedorn (H65) | Γ(α+1)·(β−β_H)^{−(α+1)}, α≈2 | ν = α+1 ≈ 3 |

The overlay table shows Z_H/Z_BC ≈ 20 000 at ε=0.01 and ≈ 1.3 at
ε=1.0, confirming **different divergence rates** at all scales, not
only different asymptotic exponents.

---

## Universality class

**BC β=1**: Galois-symmetry-breaking. Order parameter = KMS state
selection ↔ Frobenius element σ_p ∈ Gal(Q^ab/Q). Flat density of
states ρ_BC(n) = 1. Atick-Witten (1988) identifies the Hagedorn
transition as first-order string condensation; BC is a KMS-simplex
collapse in operator algebra — topologically distinct.

**Hagedorn β_H**: Exponential density of states ρ(E) ~ E^α exp(β_H E).
No order parameter, no symmetry broken; threshold for new degrees
of freedom. No arithmetic content.

Conclusion: ν_BC = 1 ≠ ν_H ≈ 3, different mechanisms, different
operator-algebraic structures. **DIFFERENT-UNIVERSALITY confirmed.**

---

## Cross-fertilisation for v6 (F-6 compliance)

v6 saturation (dS_gen/dτ_R → κ_R·C_k·Θ(PH_k), V6-1 inequality) is
neither a Galois-symmetry event nor an exponential-DoS event.
F-6 flag stands: the β=1 identification is **nominal only**.

One structural export from BC that is internally consistent (but
not a theorem for v6): the low-β (high-T) BC phase has **no
equilibrium KMS state**. In v6 terms, C_k well above saturation
may correspond to a regime where the modular Hamiltonian has no
stable thermal state at the relevant temperature. This is a
MOTIVATION, not a derivation; rule 1 and rule 12 prohibit inserting
it into v6 prose without Tomita-Takesaki proof for the boundary CFT.

**v6 paper change: none warranted.**

---

## References

- BC95: Bost & Connes, Selecta Math. 1, 411 (1995)
- H65: Hagedorn, Nuovo Cim. Suppl. 3, 147 (1965)
- Atick-Witten, Nucl. Phys. B310, 291 (1988)
- Susskind, hep-th/9309145 (1993)
