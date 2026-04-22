"""
V8-agent-14: Bost-Connes β=1 phase transition ↔ Hagedorn/v6-saturation
Analogy verdict: DIFFERENT-BUT-USEFUL

References
----------
BC95  : Bost & Connes, Selecta Math. 1, 411 (1995).
H65   : Hagedorn, Nuovo Cim. Suppl. 3, 147 (1965).
PRINCIPLES rules 1, 12, 16; V6-1, V6-4.
F-6 flag: BC β=1 is Galois-symmetry-breaking; v6 saturation is GSL-monotonicity.
"""

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# 1. BOST-CONNES partition function
# ---------------------------------------------------------------------------
# The BC system (C*(Q/Z ⋊ N^×)) has KMS states at inverse temperature β.
# Partition function = Riemann zeta (proven in BC95 §4):
#
#   Z_BC(β) = ζ(β) = Σ_{n≥1} n^{-β}
#
# Phase structure (BC95 Theorem 5.1 + §7):
#   β > 1  : unique KMS_β state, symmetry group Ẑ×  acts freely
#             → symmetry group = Gal(Q^{ab}/Q) via class-field theory
#   β = 1  : KMS_1 set is non-trivial (simplex), boundary of unique phase
#             ζ(β) diverges as (β-1)^{-1} (simple pole of zeta)
#   β < 1  : no KMS_β states (partition function diverges, no equilibrium)
#
# Near β=1^+:  Z_BC(β) ~ 1/(β-1)  [Laurent expansion of ζ]
#
# The β=1 transition = spontaneous breaking of the arithmetic Galois symmetry
# Ẑ× = Gal(Q^{ab}/Q).  Below β=1 Galois symmetry is UNBROKEN (no ground state).
# Above β=1 it is BROKEN to a unique vacuum selected by each Galois element.

beta_sym = sp.Symbol('beta', positive=True)
# Laurent expansion of ζ(β) near β=1
# ζ(s) = 1/(s-1) + γ_0 + γ_1(s-1)/1! + ...  (Stieltjes expansion)
gamma0 = 0.5772156649  # Euler-Mascheroni constant (leading Stieltjes)
# Z_BC(β) ~ 1/(β-1) + γ_0 + O(β-1)
eps_values = np.linspace(0.01, 1.5, 300)
Z_BC = np.where(eps_values > 0, 1.0/eps_values + gamma0, np.inf)
# eps = β - 1

print("=== Bost-Connes partition function ===")
print("Z_BC(β) = ζ(β);  pole at β=1: Z_BC ~ 1/(β-1) as β→1^+")
print(f"  At β=1.01: Z_BC ~ {1/0.01 + gamma0:.2f}")
print(f"  At β=1.10: Z_BC ~ {1/0.10 + gamma0:.2f}")
print(f"  At β=2.00: ζ(2) = π²/6 = {np.pi**2/6:.6f}")

# ---------------------------------------------------------------------------
# 2. HAGEDORN partition function
# ---------------------------------------------------------------------------
# Hagedorn (1965): exponential density of states ρ(E) ~ A · E^α · exp(β_H E)
# with Hagedorn temperature T_H = 1/β_H.
#
# For a system of free strings with exponential degeneracy:
#   Z_H(β) = ∫_0^∞ dE · ρ(E) · e^{-β E}
#           = A ∫_0^∞ dE · E^α · e^{-(β - β_H)E}
#           = A · Γ(α+1) / (β - β_H)^{α+1}     for β > β_H
#
# At β = β_H the integral diverges → Hagedorn transition.
#
# In string theory:  β_H = 2π√(2α') (bosonic), 2π√(α') (superstring).
# The transition is a THERMODYNAMIC singularity in the density of states.
# It has NO arithmetic Galois interpretation.

alpha_H = 2.0          # exponent (bosonic string, α≈2 in 4D effective)
beta_H  = 1.0          # normalise to β_H = 1 for overlay comparison

eps_arr = np.linspace(0.01, 1.5, 300)   # ε = β - β_H
Z_H = np.where(eps_arr > 0,
               sp.gamma(alpha_H + 1) / eps_arr**(alpha_H + 1),
               np.inf)

print("\n=== Hagedorn partition function ===")
print(f"Z_H(β) = Γ(α+1)/(β-β_H)^{{α+1}};  power-law divergence, α={alpha_H}")
print(f"  At ε=0.01: Z_H ~ {float(sp.gamma(alpha_H+1))/0.01**(alpha_H+1):.2e}")
print(f"  At ε=0.10: Z_H ~ {float(sp.gamma(alpha_H+1))/0.10**(alpha_H+1):.2e}")
print(f"  At ε=1.50: Z_H ~ {float(sp.gamma(alpha_H+1))/1.50**(alpha_H+1):.4f}")

# ---------------------------------------------------------------------------
# 3. OVERLAY COMPARISON near β=1 (both normalised: β_H = 1 ≡ BC pole)
# ---------------------------------------------------------------------------
# BC:      Z_BC ~ (β-1)^{-1}          → simple pole (exponent = 1)
# Hagedorn: Z_H ~ (β-β_H)^{-(α+1)}   → pole of order α+1 (α≈2 → order 3)
#
# Different divergence exponents → different universality class already
# at the level of the pole order.

print("\n=== Overlay near β=1 ===")
print(f"{'ε=β-1':>8}  {'Z_BC':>14}  {'Z_H(α=2)':>14}  {'Ratio Z_H/Z_BC':>16}")
for e in [0.01, 0.05, 0.10, 0.20, 0.50, 1.00]:
    zbc = 1.0/e + gamma0
    zh  = float(sp.gamma(alpha_H+1)) / e**(alpha_H+1)
    print(f"{e:>8.2f}  {zbc:>14.4f}  {zh:>14.4f}  {zh/zbc:>16.4f}")

# ---------------------------------------------------------------------------
# 4. UNIVERSALITY CLASS ANALYSIS
# ---------------------------------------------------------------------------
print("""
=== Universality class analysis ===

BOST-CONNES β=1
  Mechanism : spontaneous breaking of arithmetic Galois symmetry Ẑ×
  Order parameter : KMS state selection ↔ Frobenius element σ_p ∈ Gal(Q^ab/Q)
  Density of states : ρ_BC(n) = 1 (flat, arithmetic — one state per integer n)
  Divergence type : simple pole of ζ(β) → exponent ν_BC = 1
  Physical analogue : number-theoretic analogue of Bose-Einstein condensation
                      onto arithmetic vacuum (Galois orbit collapses)
  Rigorous statement : BC95 Theorem 7.1, Corollary 7.2

HAGEDORN β_H
  Mechanism : exponential density of states ρ(E) ~ exp(β_H E)
  Order parameter : None (no symmetry broken) — onset of new degrees of freedom
  Density of states : ρ_H(E) ~ E^α exp(β_H E), α≈2 in 4D
  Divergence type : pole of order α+1 in Z(β) → exponent ν_H = α+1 ≈ 3
  Physical analogue : string proliferation / black-hole formation threshold
  Rigorous statement : Hagedorn 1965; Atick-Witten 1988 (hep-th/88);
                       Susskind 1993 (hep-th/9309145)

COMPARISON
  ν_BC = 1  vs  ν_H ≈ 3  → DIFFERENT critical exponents
  BC : Galois lattice (arithmetic), not thermodynamic density of states
  H  : exponential DoS (combinatoric), no arithmetic / number-theoretic content
  Cross-check : Atick-Witten showed the Hagedorn transition is 1st-order
                in a canonical ensemble (string field condensation), while
                the BC transition is a KMS-simplex collapse — topologically
                distinct in operator-algebra terms.

VERDICT : DIFFERENT-UNIVERSALITY
""")

# ---------------------------------------------------------------------------
# 5. RELEVANCE FOR v6
# ---------------------------------------------------------------------------
print("""
=== Cross-fertilisation for v6 (F-6 compliance) ===

v6 saturation event: dS_gen/dτ_R = κ_R · C_k · Θ(PH_k) approaching
inequality saturation is a GSL-monotonicity event (V6-1: inequality,
not equality).  It is NOT:
  - a Galois-symmetry-breaking event (no number field structure)
  - an exponential-density-of-states event (no Hagedorn divergence)

The analogy "β=1 threshold" is NOMINAL only (F-6 confirmed).

HOWEVER, one structural insight from BC IS transferable WITHOUT
making a false identification:

  BC Insight : the low-β (high-temperature) phase has NO equilibrium
               KMS state — the system has no thermodynamic ground state
               below T_H^{-1}.

  v6 Implication : the regime C_k >> C_k^{(saturation)} (complexity well
                   above saturation) corresponds to the phase where the
                   modular Hamiltonian has no stable KMS thermal state
                   at the given temperature.  This is CONSISTENT with
                   the v6 inequality becoming degenerate (saturating
                   direction is ill-defined at very high complexity).

  CAVEAT (rule 12 / V6-1) : this is a structural MOTIVATION, not a
  theorem.  Cannot be cited as a derivation in v6 prose without
  an explicit proof that the v6 modular Hamiltonian satisfies BC
  KMS axioms — which would require the full Tomita-Takesaki machinery
  for the boundary CFT state, well beyond current scope.

DELIVERABLE FOR v6 : None (no prose change warranted).
  The BC↔Hagedorn↔v6 triangle is a useful orientation map for the
  author, but rule 1 (honesty gate) prohibits inserting this into
  the paper without a derivation that does not yet exist.
""")

print("Script complete.  Verdict: DIFFERENT-BUT-USEFUL")
