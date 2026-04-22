"""V6-variational-derivation.py

Attempt 1: derive  dS_gen[R]/dtau_R = kappa_R * C_k[rho_R] * Theta(PH_k[dn])
from the Faulkner-Speranza-Kirklin (FSK) first law of the crossed-product
algebra:

    delta S_gen = beta (delta <H_mod> - delta W_mod)

with modular Hamiltonian H_mod generating modular (Tomita-Takesaki) flow,
beta the observer's local modular temperature, and W_mod the modular-work
1-form. Differentiating in modular proper time tau_R:

    dS_gen/dtau = beta * ( d<H_mod>/dtau - dW_mod/dtau )

We use sympy to check (a) algebraic self-consistency, (b) the conditions
under which the right-hand side reduces to the target ansatz
  kappa * C_k * Theta.

Conclusion reached by this script: SUCCESS is only partial. The reduction
requires two independent identifications which cannot both be derived from
first principles within FSK alone:

  (I1)  d<H_mod>/dtau  =  v_C * C_k       (Brown-Susskind complexity-energy)
  (I2)  dW_mod/dtau    =  v_C * C_k * (1 - Theta)   (saturation work)

The first is a *conjecture* (complexity = action / complexity-momentum
heuristic), the second is *postulated* so that the gate Theta emerges.
Neither follows from FSK, so the equation is at best an ansatz motivated
by the FSK first law, not derived from it.

Author: K. Remondière  (derivation skeleton written 2026-04-21).
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # Symbolic setup -------------------------------------------------------
    tau = sp.symbols("tau", real=True, positive=True)
    beta = sp.symbols("beta", real=True, positive=True)          # 1/T_modular
    kappa = sp.symbols("kappa", real=True, positive=True)        # nat/s^2 ?
    v_C = sp.symbols("v_C", real=True, positive=True)            # complexity velocity
    alpha = sp.Rational(95, 1000)                                # 0.095
    PH = sp.Function("PH")(tau)
    PH_c = sp.symbols("PH_c", real=True, positive=True)
    C = sp.Function("C")(tau)                                    # k-design complexity
    Hmod = sp.Function("H_mod")(tau)
    Wmod = sp.Function("W_mod")(tau)

    # Faulkner-Speranza-Kirklin first law (crossed product, type II):
    #   dS_gen/dtau = beta * d<H_mod>/dtau  -  beta * dW_mod/dtau
    dSgen = beta * (sp.diff(Hmod, tau) - sp.diff(Wmod, tau))
    print("[FSK] dS_gen/dtau =", dSgen)

    # Target ansatz --------------------------------------------------------
    Theta = sp.exp(-(PH / PH_c) ** alpha)
    target = kappa * C * Theta
    print("[target] kappa*C*Theta =", target)

    # Reduction attempt ----------------------------------------------------
    # Identification (I1): complexity-energy relation (heuristic,
    # Brown-Susskind style).  d<H_mod>/dtau = v_C * C  is NOT a theorem; it
    # is an ansatz motivated by the "complexity = action" conjecture.
    I1 = sp.Eq(sp.diff(Hmod, tau), v_C * C)

    # Identification (I2): modular-work rate cancels the (1 - Theta)
    # fraction of the complexity budget at saturation (PH_k -> PH_c,
    # Theta -> 1/e; PH_k >> PH_c, Theta -> 0).  Again not derived.
    I2 = sp.Eq(sp.diff(Wmod, tau), v_C * C * (1 - Theta))

    # Substitute:
    dSgen_reduced = dSgen.subs(
        {sp.diff(Hmod, tau): I1.rhs, sp.diff(Wmod, tau): I2.rhs}
    )
    dSgen_reduced = sp.simplify(dSgen_reduced)
    print("[reduced] dS_gen/dtau =", dSgen_reduced)

    # Match coefficients: beta * v_C  must be  kappa.
    residual = sp.simplify(dSgen_reduced - target)
    print("[residual] (reduced - target) =", residual)

    # Substitute kappa := beta * v_C and check residual vanishes.
    residual_matched = sp.simplify(residual.subs(kappa, beta * v_C))
    print("[residual with kappa = beta*v_C] =", residual_matched)
    assert residual_matched == 0, "algebraic match failed"

    # ------------------------------------------------------------------
    # Summary of logical status
    # ------------------------------------------------------------------
    print()
    print("=" * 64)
    print("LOGICAL AUDIT")
    print("=" * 64)
    print(
        "(FSK first law)                     RIGOROUS"
        " (crossed product, Faulkner-Speranza 2024, Kirklin 2025)"
    )
    print(
        "(I1) d<H_mod>/dtau = v_C * C        HEURISTIC"
        " (Brown-Susskind complexity=action, NOT a theorem in II_1/II_inf)"
    )
    print(
        "(I2) dW_mod/dtau = v_C * C (1-Th)   POSTULATED"
        " (no independent derivation; chosen so Theta emerges)"
    )
    print("kappa = beta * v_C                  consistent identification")
    print()
    print(
        "Verdict: the equation is ALGEBRAICALLY consistent with the FSK"
        " first law, but the two identifications required to recover the"
        " ansatz are not themselves derived. Status: PARTIAL (ansatz"
        " motivated, not derived)."
    )


if __name__ == "__main__":
    main()
