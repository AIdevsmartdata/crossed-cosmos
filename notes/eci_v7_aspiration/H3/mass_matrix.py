"""
H3.C — Symbolic construction of M_u(τ) in S'_4 for LYD20 Model VI

Source citations:
  - Rep assignment: LYD20 arXiv:2006.10722, Table I (tab:quark_mod) Model VI,
    Eq. (Wq6) for superpotential, Eq. (Mq_6) for mass matrix.
  - Modular forms: LYD20 Appendix (sec:higher weight-app), lines 1850-1894 in TeX.
  - Weight-1 seed: LYD20 lines 317-330.
  - Weight-2 forms: LYD20 lines 346-352.
  - Weight-3 forms: LYD20 lines 354-360.
  - Weight-5 forms: LYD20 lines 1865-1876.
  - CG coefficients: NPP20 arXiv:2006.03058, Appendix C (app:CGCs) Tables tab:1r, tab:33.

Model VI assignment (LYD20 Table I):
  Q ~ 3 (triplet), k_Q
  u^c ~ 1̂ (hat-1), weight 1 - k_Q
  c^c ~ 1 (trivial), weight 2 - k_Q
  t^c ~ 1̂' (hat-1-prime), weight 5 - k_Q
  H_u ~ 1 (trivial), weight 0

Up-sector mass matrix M_u (LYD20 Eq. Mq_6):
  Row u^c: α_u [Y^(1)_1, Y^(1)_3, Y^(1)_2]
  Row c^c: β_u [Y^(2)_3, Y^(2)_5, Y^(2)_4]
  Row t^c: γ_u [Y^(5)_3, Y^(5)_5, Y^(5)_4]

where Y^(k)_i uses LYD20 component notation (Eq. lines 379-395):
  Y^(1)_{3̂'} ≡ (Y^(1)_1, Y^(1)_2, Y^(1)_3) [weight-1, transforms as 3̂']
  Y^(2)_{3}  ≡ (Y^(2)_3, Y^(2)_4, Y^(2)_5) [weight-2, transforms as 3]
  Y^(5)_{3̂} ≡ (Y^(5)_3, Y^(5)_4, Y^(5)_5) [weight-5, transforms as 3̂]

ANTI-HALLUCINATION NOTE: All modular form polynomial expressions below are
TRANSCRIBED DIRECTLY from LYD20 TeX source lines 317-395 and 1850-1876.
The polynomials are in Y_1, Y_2, Y_3 satisfying the constraint Y_1^2 + 2*Y_2*Y_3 = 0.
"""

import numpy as np
from numpy import pi, sqrt, exp

# ─────────────────────────────────────────────────────────────────
# 1. WEIGHT-1 MODULAR FORMS  (LYD20 lines 296-330)
# ─────────────────────────────────────────────────────────────────
# Basis functions via Dedekind eta:
#   e_1(τ) = η^4(4τ) / η^2(2τ)
#   e_2(τ) = η^10(2τ) / [η^4(4τ) η^4(τ)]
#   e_3(τ) = η^4(2τ) / η^2(2τ)   ← Note: LYD20 typo; should be η^4(2τ)/η^2(τ)
#
# Y_1 = 4√2 e_1 + √2 i e_2 + 2√2(1-i) e_3
# Y_2 = -2√2(1+√3) ω² e_1 - (1-√3)/√2 i ω² e_2 + 2√2(1-i) ω² e_3
# Y_3 = 2√2(√3-1) ω  e_1 - (1+√3)/√2 i ω  e_2 + 2√2(1-i) ω  e_3
# where ω = exp(2πi/3)
#
# For numerical evaluation we use the Jacobi theta function representation.
# θ_2(τ) and θ_3(τ) via their q-series with q_4 = exp(πiτ/2):

def eta(tau, n_terms=50):
    """Dedekind eta function via q-product. q = exp(2πiτ)."""
    q = exp(2j * pi * tau)
    result = q**(1/24)
    for n in range(1, n_terms):
        result *= (1 - q**n)
    return result

def modular_forms_weight1(tau, n_terms=50):
    """
    Compute Y_1, Y_2, Y_3 (weight-1 3̂' of S'_4) via eta functions.
    LYD20 lines 296-330.
    Uses e_1(τ) = η^4(4τ)/η^2(2τ), etc.
    """
    e1 = eta(4*tau, n_terms)**4 / eta(2*tau, n_terms)**2
    e2 = eta(2*tau, n_terms)**10 / (eta(4*tau, n_terms)**4 * eta(tau, n_terms)**4)
    e3 = eta(2*tau, n_terms)**4 / eta(tau, n_terms)**2

    omega = exp(2j * pi / 3)
    s2 = sqrt(2)
    s3 = sqrt(3)

    Y1 = 4*s2*e1 + s2*1j*e2 + 2*s2*(1-1j)*e3
    Y2 = (-2*s2*(1+s3)*omega**2*e1
          - (1-s3)/s2*1j*omega**2*e2
          + 2*s2*(1-1j)*omega**2*e3)
    Y3 = (2*s2*(s3-1)*omega*e1
          - (1+s3)/s2*1j*omega*e2
          + 2*s2*(1-1j)*omega*e3)

    return Y1, Y2, Y3

# ─────────────────────────────────────────────────────────────────
# 2. HIGHER-WEIGHT MODULAR FORMS  (LYD20 Appendix lines 346-395, 1850-1876)
# All expressed as polynomials in Y1, Y2, Y3.
# TRANSCRIBED verbatim from LYD20 TeX source.
# ─────────────────────────────────────────────────────────────────

def modular_forms_all(Y1, Y2, Y3):
    """
    Compute all needed modular form components from (Y1, Y2, Y3).
    Returns dict keyed by LYD20 component index notation Y^(k)_i.
    """
    forms = {}

    # -- Weight 1 (LYD20 Eq. modular_space, line 317) --
    # Y^(1)_{3̂'} = (Y1, Y2, Y3)  [LYD20 notation: Y^(1)_1, Y^(1)_2, Y^(1)_3]
    forms['Y1_1'] = Y1   # first component of Y^(1)_{3̂'}
    forms['Y1_2'] = Y2
    forms['Y1_3'] = Y3

    # -- Weight 2 (LYD20 lines 347-351) --
    # Y^(2)_{2} = (-Y2^2 - 2Y1Y3, Y3^2 + 2Y1Y2)  → components Y^(2)_1, Y^(2)_2
    forms['Y2_1'] = -Y2**2 - 2*Y1*Y3
    forms['Y2_2'] =  Y3**2 + 2*Y1*Y2

    # Y^(2)_{3} = (2Y1^2-2Y2Y3, 2Y3^2-2Y1Y2, 2Y2^2-2Y1Y3)  → Y^(2)_3, Y^(2)_4, Y^(2)_5
    forms['Y2_3'] = 2*Y1**2 - 2*Y2*Y3
    forms['Y2_4'] = 2*Y3**2 - 2*Y1*Y2
    forms['Y2_5'] = 2*Y2**2 - 2*Y1*Y3

    # -- Weight 3 (LYD20 lines 355-360) --
    # Y^(3)_{1̂'} = 2(Y1^3 + Y2^3 + Y3^3 - 3Y1Y2Y3)  → Y^(3)_1
    forms['Y3_1'] = 2*(Y1**3 + Y2**3 + Y3**3 - 3*Y1*Y2*Y3)

    # Y^(3)_{3̂} = (2(2Y1^3-Y2^3-Y3^3), 6Y3(Y2^2-Y1Y3), 6Y2(Y3^2-Y1Y2))
    #           → Y^(3)_2, Y^(3)_3, Y^(3)_4
    forms['Y3_2'] = 2*(2*Y1**3 - Y2**3 - Y3**3)
    forms['Y3_3'] = 6*Y3*(Y2**2 - Y1*Y3)
    forms['Y3_4'] = 6*Y2*(Y3**2 - Y1*Y2)

    # Y^(3)_{3̂'} = (2(Y2^3-Y3^3), 2(-2Y1^2Y2+Y2^2Y3+Y1Y3^2), 2(2Y1^2Y3-Y1Y2^2-Y2Y3^2))
    #            → Y^(3)_5, Y^(3)_6, Y^(3)_7
    forms['Y3_5'] = 2*(Y2**3 - Y3**3)
    forms['Y3_6'] = 2*(-2*Y1**2*Y2 + Y2**2*Y3 + Y1*Y3**2)
    forms['Y3_7'] = 2*(2*Y1**2*Y3 - Y1*Y2**2 - Y2*Y3**2)

    # -- Weight 4 (LYD20 Appendix lines 1854-1863) --
    # Y^(4)_1 = 4(Y1^4 - 2Y1(Y2^3+Y3^3) + 3Y2^2Y3^2)
    forms['Y4_1'] = 4*(Y1**4 - 2*Y1*(Y2**3 + Y3**3) + 3*Y2**2*Y3**2)

    # Y^(4)_{2} = (-2Y3^4+4Y1^3Y3+4Y2^3Y3-6Y1^2Y2^2,
    #              -2Y2^4+4Y1^3Y2+4Y2Y3^3-6Y1^2Y3^2)  → Y^(4)_2, Y^(4)_3
    forms['Y4_2'] = -2*Y3**4 + 4*Y1**3*Y3 + 4*Y2**3*Y3 - 6*Y1**2*Y2**2
    forms['Y4_3'] = -2*Y2**4 + 4*Y1**3*Y2 + 4*Y2*Y3**3 - 6*Y1**2*Y3**2

    # Y^(4)_{3} = (6Y1(-Y2^3+Y3^3),
    #              6Y1Y3(Y2^2-Y1Y3)+2Y2(-2Y1^3+Y2^3+Y3^3),
    #              6Y1Y2(Y1Y2-Y3^2)-2Y3(-2Y1^3+Y2^3+Y3^3))
    #           → Y^(4)_4, Y^(4)_5, Y^(4)_6
    forms['Y4_4'] = 6*Y1*(-Y2**3 + Y3**3)
    forms['Y4_5'] = (6*Y1*Y3*(Y2**2 - Y1*Y3)
                     + 2*Y2*(-2*Y1**3 + Y2**3 + Y3**3))
    forms['Y4_6'] = (6*Y1*Y2*(Y1*Y2 - Y3**2)
                     - 2*Y3*(-2*Y1**3 + Y2**3 + Y3**3))

    # Y^(4)_{3'} = (2(4Y1^4-6Y2^2Y3^2+Y1(Y2^3+Y3^3)),
    #               2(Y2^4-2Y1^3Y2+7Y2Y3^3+3Y1^2Y3^2-9Y1Y2^2Y3),
    #               2(Y3^4-2Y1^3Y3+7Y2^3Y3+3Y1^2Y2^2-9Y1Y2Y3^2))
    #            → Y^(4)_7, Y^(4)_8, Y^(4)_9
    forms['Y4_7'] = 2*(4*Y1**4 - 6*Y2**2*Y3**2 + Y1*(Y2**3 + Y3**3))
    forms['Y4_8'] = 2*(Y2**4 - 2*Y1**3*Y2 + 7*Y2*Y3**3 + 3*Y1**2*Y3**2
                       - 9*Y1*Y2**2*Y3)
    forms['Y4_9'] = 2*(Y3**4 - 2*Y1**3*Y3 + 7*Y2**3*Y3 + 3*Y1**2*Y2**2
                       - 9*Y1*Y2*Y3**2)

    # -- Weight 5 (LYD20 Appendix lines 1866-1876) --
    # Y^(5)_{2̂} → Y^(5)_1, Y^(5)_2
    forms['Y5_1'] = 2*(Y2**5 + 2*Y1**4*Y3 + 2*Y1*Y3**4 + Y2**2*Y3**3
                       + Y1**3*Y2**2 - Y1*Y2**3*Y3 - 6*Y1**2*Y2*Y3**2)
    forms['Y5_2'] = 2*(Y3**5 + 2*Y1**4*Y2 + 2*Y1*Y2**4 + Y1**3*Y3**2
                       + Y2**3*Y3**2 - Y1*Y2*Y3**3 - 6*Y1**2*Y2**2*Y3)

    # Y^(5)_{3̂} → Y^(5)_3, Y^(5)_4, Y^(5)_5
    forms['Y5_3'] = 18*Y1**2*(-Y2**3 + Y3**3)
    forms['Y5_4'] = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
                     + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
                     + 6*Y1**2*Y2**2*Y3)
    forms['Y5_5'] = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
                     - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
                     - 6*Y1**2*Y2*Y3**2)

    # Y^(5)_{3̂',I} → Y^(5)_6, Y^(5)_7, Y^(5)_8
    forms['Y5_6'] = (8*Y1**3*Y2*Y3 - 6*Y1**2*(Y2**3 + Y3**3)
                     + 2*Y2*Y3*(Y2**3 + Y3**3))
    forms['Y5_7'] = (4*Y1**4*Y2 - 2*Y1*Y2**4 - 6*Y1**2*Y2**2*Y3
                     - 2*Y1**3*Y3**2 + 4*Y2**3*Y3**2 + 4*Y1*Y2*Y3**3
                     - 2*Y3**5)
    forms['Y5_8'] = -2*(Y1**3*Y2**2 + Y2**5 - 2*Y1**4*Y3
                        + 3*Y1**2*Y2*Y3**2 - 2*Y2**2*Y3**3
                        + Y1*(-2*Y2**3*Y3 + Y3**4))

    # Y^(5)_{3̂',II} → Y^(5)_9, Y^(5)_10, Y^(5)_11
    D = Y1**4 + 3*Y2**2*Y3**2 - 2*Y1*(Y2**3 + Y3**3)  # common factor
    forms['Y5_9']  = 4*Y1*D
    forms['Y5_10'] = 4*Y2*D
    forms['Y5_11'] = 4*Y3*D

    return forms

# ─────────────────────────────────────────────────────────────────
# 3. MASS MATRIX M_u(τ; α_u, β_u, γ_u)  (LYD20 Eq. Mq_6)
# ─────────────────────────────────────────────────────────────────

def M_u(tau, alpha_u, beta_u, gamma_u, n_terms=50):
    """
    Up-type quark Yukawa mass matrix for LYD20 Model VI.
    Source: LYD20 arXiv:2006.10722, Eq. (Mq_6) lines 1380-1384 in TeX.

    Structure (TRANSCRIBED from LYD20):
      Row 0 (u^c coupling, Q ~ 3, u^c ~ 1̂, Y^(1)_{3̂'}):
        M_u[0,:] = α_u * [Y^(1)_1, Y^(1)_3, Y^(1)_2]

      Row 1 (c^c coupling, Q ~ 3, c^c ~ 1, Y^(2)_{3}):
        M_u[1,:] = β_u * [Y^(2)_3, Y^(2)_5, Y^(2)_4]

      Row 2 (t^c coupling, Q ~ 3, t^c ~ 1̂', Y^(5)_{3̂}):
        M_u[2,:] = γ_u * [Y^(5)_3, Y^(5)_5, Y^(5)_4]

    The column index runs over Q = (Q_1, Q_2, Q_3).
    v_u (Higgs VEV) is absorbed into the coupling constants.

    Parameters
    ----------
    tau : complex
        Modulus value (Im(τ) > 0 for upper half-plane)
    alpha_u, beta_u, gamma_u : complex
        Yukawa couplings (real under gCP symmetry)
    n_terms : int
        Number of terms for eta function series

    Returns
    -------
    M : (3,3) complex numpy array
    """
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    f = modular_forms_all(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)

    # Row 0: u^c — uses weight-1 forms Y^(1)_1, Y^(1)_3, Y^(1)_2
    M[0, 0] = alpha_u * f['Y1_1']
    M[0, 1] = alpha_u * f['Y1_3']
    M[0, 2] = alpha_u * f['Y1_2']

    # Row 1: c^c — uses weight-2 forms Y^(2)_3, Y^(2)_5, Y^(2)_4
    M[1, 0] = beta_u * f['Y2_3']
    M[1, 1] = beta_u * f['Y2_5']
    M[1, 2] = beta_u * f['Y2_4']

    # Row 2: t^c — uses weight-5 forms Y^(5)_3, Y^(5)_5, Y^(5)_4
    M[2, 0] = gamma_u * f['Y5_3']
    M[2, 1] = gamma_u * f['Y5_5']
    M[2, 2] = gamma_u * f['Y5_4']

    return M

def M_d(tau, alpha_d, beta_d, gamma_d1, gamma_d2, n_terms=50):
    """
    Down-type quark Yukawa mass matrix for LYD20 Model VI.
    Source: LYD20 arXiv:2006.10722, Eq. (Mq_6) lines 1385-1389 in TeX.

    Structure (TRANSCRIBED from LYD20):
      Row 0 (d^c coupling, Q ~ 3, d^c ~ 1̂, Y^(1)_{3̂'}):
        M_d[0,:] = α_d * [Y^(1)_1, Y^(1)_3, Y^(1)_2]

      Row 1 (s^c coupling, Q ~ 3, s^c ~ 1̂', Y^(5)_{3̂}):
        M_d[1,:] = β_d * [Y^(5)_3, Y^(5)_5, Y^(5)_4]

      Row 2 (b^c coupling, Q ~ 3, b^c ~ 1̂, uses two 3̂' forms at weight 5):
        M_d[2,:] = γ_{d1}*[Y^(5)_6, Y^(5)_8, Y^(5)_7]
                 + γ_{d2}*[Y^(5)_9, Y^(5)_11, Y^(5)_10]
    """
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    f = modular_forms_all(Y1, Y2, Y3)

    M = np.zeros((3, 3), dtype=complex)

    # Row 0: d^c
    M[0, 0] = alpha_d * f['Y1_1']
    M[0, 1] = alpha_d * f['Y1_3']
    M[0, 2] = alpha_d * f['Y1_2']

    # Row 1: s^c
    M[1, 0] = beta_d * f['Y5_3']
    M[1, 1] = beta_d * f['Y5_5']
    M[1, 2] = beta_d * f['Y5_4']

    # Row 2: b^c (two weight-5 3̂' contributions)
    M[2, 0] = gamma_d1 * f['Y5_6'] + gamma_d2 * f['Y5_9']
    M[2, 1] = gamma_d1 * f['Y5_8'] + gamma_d2 * f['Y5_11']
    M[2, 2] = gamma_d1 * f['Y5_7'] + gamma_d2 * f['Y5_10']

    return M

# ─────────────────────────────────────────────────────────────────
# 4. PARAMETER COUNT SUMMARY
# ─────────────────────────────────────────────────────────────────
PARAMETER_COUNT = """
LYD20 Model VI parameter count:

Up-sector (fitting m_u, m_c, m_t):
  α_u, β_u, γ_u  — 3 real couplings (phases absorbed via gCP or field redefs)
  Re(τ), Im(τ)    — 2 real parameters for modulus
  α_u * v_u       — 1 overall mass scale (sets |m_t|)
  = 6 real parameters → minus 1 (only ratios β_u/α_u, γ_u/α_u matter for mass ratios)
  = 5 independent parameters fitting {m_u/m_c, m_c/m_t} = 2 mass ratios + τ context

Down-sector (fitting m_d, m_s, m_b + CKM):
  α_d, β_d, γ_{d1}   — 3 real couplings
  γ_{d2}              — 1 complex coupling (2 real without gCP) or 1 real (with gCP)
  α_d * v_d           — 1 overall scale
  = 6-7 real parameters

Total (Model VI without gCP per LYD20): 10 free real parameters
  Fitting: 3 up masses + 3 down masses + 4 CKM (3 angles + 1 phase) = 10 observables
  DOF = 10 obs - 10 params + 2 (τ already in params) = effectively 0 genuine predictions

  HOWEVER: With gCP (restricting γ_{d2} to real), params = 9, and θ_23 is predicted
  to be ~0.049 (LYD20 reports it comes out ~25% too large for Model VI).

Note: The up-sector ALONE has 3 couplings + τ = 5 free params fitting 3 up masses.
  → 5 params, 3 observables → 2 continuous free parameters remain after fitting
  → m_u/m_c IS predictable given τ and β_u/α_u, γ_u/α_u, but only after fitting m_c/m_t.
"""

# ─────────────────────────────────────────────────────────────────
# 5. VERIFICATION: check constraint Y_1^2 + 2*Y_2*Y_3 = 0
# ─────────────────────────────────────────────────────────────────

def check_constraint(tau, n_terms=50):
    """Verify the modular form constraint Y1^2 + 2*Y2*Y3 = 0 (LYD20 Eq. MF-constraint)."""
    Y1, Y2, Y3 = modular_forms_weight1(tau, n_terms)
    residual = Y1**2 + 2*Y2*Y3
    print(f"Constraint Y1^2 + 2*Y2*Y3 at τ={tau}: {abs(residual):.2e} (should be ~0)")
    return residual

if __name__ == "__main__":
    print("=" * 60)
    print("H3.C — S'_4 Up-Quark Yukawa Mass Matrix (LYD20 Model VI)")
    print("=" * 60)

    print("\n1. Checking modular form constraint at τ = i:")
    check_constraint(1j)

    print("\n2. Checking modular form constraint at τ = -0.4999 + 0.8958i (LYD20 best fit):")
    tau_bf = -0.4999 + 0.8958j
    check_constraint(tau_bf)

    print("\n3. Mass matrix structure at τ = i (square fixed point):")
    tau = 1j
    alpha_u, beta_u, gamma_u = 1.0, 62.2142, 0.00104  # LYD20 best-fit ratios
    M = M_u(tau, alpha_u, beta_u, gamma_u)
    print("M_u(τ=i) with α=1, β=62.21, γ=0.00104:")
    print(M)
    print("|M_u|:")
    print(np.abs(M))

    print("\n4. Mass matrix structure at LYD20 best-fit τ:")
    M_bf = M_u(tau_bf, alpha_u, beta_u, gamma_u)
    print(f"M_u(τ={tau_bf}):")
    print(np.abs(M_bf))

    print(f"\n5. Parameter count summary:")
    print(PARAMETER_COUNT)
