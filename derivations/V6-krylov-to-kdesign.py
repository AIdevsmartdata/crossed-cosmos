"""V6-krylov-to-kdesign.py

Attempt 2: statistical-mechanics bridge.

Starting point (Fan 2022, PRR 4 L012027, "Universal relation between
entropy of Krylov space and operator complexity"):

    dS_K/dt  <=  2 * b_1 * sqrt( <K^2> - <K>^2 )

with b_1 the first Lanczos coefficient, S_K = -sum p_n log p_n the Krylov
entropy, and C_K = <K> the Krylov (operator) complexity.  Fan's bound is
*logarithmic* in complexity in the post-scrambling regime:

    S_K(t)  ~  log C_K(t)   (after scrambling, before saturation)

We want the target form  dS/dtau ~ C_k * Theta  with C_k a *k-design*
complexity (Ma-Huang 2025, Haferkamp 2022), not a Krylov complexity. We
use sympy to make the substitution chain explicit and flag each step.

Steps tested:
  S1. Fan bound  dS_K/dt <= 2 b_1 Delta S_K                       [RIGOROUS]
  S2. Post-scrambling:  S_K ~ log C_K                             [HEURISTIC]
  S3. C_K <-> C_k (Krylov <-> k-design) identification            [NOT PROVEN]
  S4. Saturation gate Theta kills contribution outside chaotic
      regime  (C_k near-max => dS/dt -> 0)                        [AD HOC]

Differentiating S2:  dS_K/dt ~ (1/C_K) * dC_K/dt , which is LOGARITHMIC in
complexity, not linear.  To recover dS/dtau ~ C_k one must (i) replace S_K
by S_gen (a distinct entropy) and (ii) postulate that the growth *rate*
of S_gen tracks C_k itself, not log C_k. Neither is justified by Fan 2022.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    t = sp.symbols("t", real=True, positive=True)
    b1 = sp.symbols("b_1", real=True, positive=True)
    CK = sp.Function("C_K")(t)
    Ck = sp.Function("C_k")(t)                # k-design complexity
    SK = sp.Function("S_K")(t)
    Sgen = sp.Function("S_gen")(t)

    # S1: Fan 2022 rigorous bound (Cauchy-Schwarz on Krylov probabilities)
    DeltaSK = sp.sqrt(sp.Function("VarK")(t))
    fan_bound = sp.Le(sp.diff(SK, t), 2 * b1 * DeltaSK)
    print("[S1] Fan 2022 bound:", fan_bound)

    # S2: post-scrambling heuristic  S_K ~ log C_K
    SK_approx = sp.log(CK)
    dSK_dt = sp.diff(SK_approx, t)
    print("[S2] dS_K/dt under S_K ~ log C_K:", sp.simplify(dSK_dt))
    # => logarithmic dependence on complexity, not linear.

    # S3: Krylov complexity <-> k-design complexity bridge
    # Haferkamp 2022 shows linear growth of C_k for random local circuits,
    # but C_K (Lanczos chain length) and C_k (min # of 2-qubit gates for
    # eps-approximate k-design) differ by an O(poly) factor only in
    # specific models. No universal identity.
    print(
        "[S3] C_K vs C_k: related by an O(poly) factor in specific"
        " random-circuit models (Haferkamp 2022), NOT in general."
    )

    # S4: saturation gate
    alpha = sp.Rational(95, 1000)
    PH = sp.symbols("PH", positive=True)
    PH_c = sp.symbols("PH_c", positive=True)
    Theta = sp.exp(-(PH / PH_c) ** alpha)
    print("[S4] saturation gate Theta =", Theta)

    # Target after identifications:
    # Replace S_K by S_gen (physical entropy for crossed-product algebra),
    # drop the log (assert rate scales with C_k not log C_k), multiply by
    # Theta to kill post-saturation contribution.
    kappa = sp.symbols("kappa", positive=True)
    target = sp.Eq(sp.diff(Sgen, t), kappa * Ck * Theta)
    print("[target]", target)

    # Residual between Fan-derived bound and target (order-of-magnitude):
    print()
    print(
        "Residual of bridging: Fan gives  dS_K/dt <= 2 b_1 sqrt(Var_K),"
        " which after S_K ~ log C_K becomes  dS_K/dt ~ d(log C_K)/dt."
        " The target wants  dS_gen/dt ~ C_k.  To move from log C_K to"
        " C_k we need to (a) promote S_K -> S_gen and (b) promote the"
        " log to a linear factor.  Neither move is licensed by Fan 2022."
    )

    print()
    print("=" * 64)
    print("Step status summary")
    print("=" * 64)
    print("S1 Fan bound                 RIGOROUS")
    print("S2 S_K ~ log C_K             HEURISTIC (post-scrambling only)")
    print("S3 C_K -> C_k                NOT PROVEN in general")
    print("S4 Theta gate                AD HOC (matches phenomenology)")
    print()
    print(
        "Verdict: FAIL as a derivation. The Fan 2022 bound gives a"
        " *logarithmic* relation between entropy rate and complexity,"
        " not the *linear* relation postulated in the target ansatz."
    )


if __name__ == "__main__":
    main()
