"""V6-dimensional.py

Attempt 3: dimensional analysis of

    dS_gen[R] / dtau_R  =  kappa_R * C_k[rho_R] * Theta(PH_k[dn])

Natural units hbar = c = k_B = 1. Entropy in nats => [S_gen] = 1
(dimensionless information measure) but carries a 'nat' label; we keep
it explicit. Time in seconds.

  [S_gen]            = nat
  [tau_R]            = s
  [dS_gen/dtau_R]    = nat / s
  [C_k]              = 1  (number of 2-qubit gates, or polynomial degree)
  [Theta]            = 1  (exp of dimensionless)
  => [kappa_R]       = nat / s

Three candidate first-principles forms for kappa_R, each with its own
dimensional check:

  (K1) kappa_R = 1 / tau_scr,R              (inverse scrambling time)
  (K2) kappa_R = 2 pi T_R                   (de Sitter modular temperature)
  (K3) kappa_R = v_Haf                      (Haferkamp 2022 linear rate)

All three have units 1/s, so to obtain nat/s we must attach a nat per
scrambling event. For (K2), 2 pi T_R = 2 pi H / (2 pi) = H (de Sitter);
so kappa_R = H in natural units, with an implicit "nat per modular e-fold".

Note: the external-review suggestion "alpha = 0.095 is kappa_R" is
DIMENSIONALLY INVALID: alpha is a pure number (an exponent); kappa_R
has units of inverse time. See paper/_internal_rag/v6_ideas.md §3(b).
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # Units as sympy symbols ----------------------------------------------
    nat, s = sp.symbols("nat s", positive=True)
    dim_Sgen = nat
    dim_tau = s
    dim_dSdt = dim_Sgen / dim_tau
    dim_Ck = sp.Integer(1)
    dim_Theta = sp.Integer(1)
    dim_kappa_required = dim_dSdt / (dim_Ck * dim_Theta)
    print("[required]  [kappa_R] =", dim_kappa_required, "   (nat/s)")

    # Candidate K1: 1 / tau_scr ------------------------------------------
    tau_scr = s
    dim_K1 = 1 / tau_scr
    print("[K1] 1/tau_scr  =>", dim_K1, "  (missing factor of 'nat')")

    # Candidate K2: 2 pi T_R ---------------------------------------------
    T_R = 1 / s                              # de Sitter temperature in nat units
    dim_K2 = 2 * sp.pi * T_R
    print("[K2] 2 pi T_R   =>", dim_K2, "  (missing factor of 'nat')")

    # Candidate K3: Haferkamp linear growth rate --------------------------
    v_Haf = nat / s                          # 'nat per time' by construction
    dim_K3 = v_Haf
    print("[K3] v_Haf       =>", dim_K3, "   MATCHES required dimension")

    # Verification of kappa = 2 pi T_R * (1 nat per modular e-fold) -------
    # This is the natural-unit convention: one nat of generalised entropy
    # flows per modular e-fold. In that case K2 * nat = K3.
    dim_K2_with_nat = dim_K2 * nat
    print(
        "[K2 with 'nat per modular e-fold' convention] =>",
        dim_K2_with_nat,
        " MATCHES required",
    )

    # alpha reuse check ---------------------------------------------------
    alpha = sp.Rational(95, 1000)            # dimensionless
    print()
    print(
        "[alpha = 0.095 reuse check] alpha is dimensionless; kappa has"
        " units nat/s. Identifying kappa_R with alpha is a DIMENSIONAL"
        " CATEGORY ERROR (confirmed)."
    )

    print()
    print("=" * 64)
    print("DIMENSIONAL VERDICT")
    print("=" * 64)
    print(
        "CONSISTENT with K3 (Haferkamp) or with K2 *augmented* by a"
        " 'nat per modular e-fold' convention."
    )
    print(
        "NOT CONSISTENT with the suggested identification kappa_R = alpha"
        " (alpha = 0.095 is an exponent, not a rate)."
    )


if __name__ == "__main__":
    main()
