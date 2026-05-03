"""
sympy_check.py  --  R5 Spectral Correspondence: Operator Verification
=======================================================================
ECI v6.0.25  /  D3_R5_spectral  /  2026-05-03

VERIFIED against:
  - Hartnoll-Yang 2025, arXiv:2502.02661 (eq.37, eq.43)
  - Connes-Consani-Moscovici 2025, arXiv:2511.22755 (eq.5.14, Thm 1.1(i))

CONCLUSIONS (run to see):
  1. D_HY eigenfunctions: psi_t(x) = x^{-Delta-it},  D_HY psi_t = t psi_t  [OK]
  2. D_CCM eigenfunctions: phi_t(u) = u^{it},          D_CCM phi_t = t phi_t  [OK]
  3. Under u=e^x substitution:  D_CCM -> -i d/dx  (MOMENTUM, not dilatation)
  4. D_HY = i*(x d/dx + Delta)  (DILATATION + shift)
  5. The v6.0.23 identity "D_HY = -D_CCM + i*Delta*id" is INCORRECT as
     a pointwise operator identity.  What holds:
       (a) Both operators have the same continuous spectrum R.
       (b) Both are unitarily equivalent to multiplication by t on L^2(R, dt).
       (c) D_HY = D_sa - epsilon where D_sa = i*(x d/dx + 1/2) is self-adjoint.
  6. The correct framing for R5 is SPECTRAL TYPE EQUIVALENCE (unitary
     equivalence via Mellin/Plancherel), NOT a pointwise algebraic identity.

CORRECTED STATEMENT for R5 paper:
  "D_HY and D_CCM are unitarily equivalent to the same multiplication
   operator on L^2(R, dt); they generate isomorphic von Neumann algebras.
   The substitution u = e^x intertwines their respective Hilbert spaces
   and maps D_CCM to -i d/dx, which differs from D_HY by the factor x
   in the leading term: D_HY - (-D_CCM + i*Delta) = i*(x-1)*d/dx."
"""

import sympy as sp

print("=" * 68)
print("  R5 Spectral Correspondence: Sympy Operator Verification")
print("  ECI v6.0.25  |  2026-05-03")
print("=" * 68)

# ---------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------
x = sp.Symbol('x', positive=True)
u = sp.Symbol('u', positive=True)
n = sp.Symbol('n')
t_param = sp.Symbol('t', real=True)
epsilon = sp.Symbol('epsilon', real=True)
Delta = sp.Rational(1, 2) + sp.I * epsilon   # conformal weight, HY eq.(37)

print(f"\nConformal weight: Delta = {Delta}")
print("(Delta = 1/2 + i*epsilon from Hartnoll-Yang eq.(37))\n")

# ---------------------------------------------------------------
# BLOCK 1: D_HY eigenvalue verification
# ---------------------------------------------------------------
print("-" * 60)
print("BLOCK 1: D_HY eigenvalue verification (HY eq.37, eq.43)")
print("-" * 60)

# D_HY f = i*(x*df/dx + Delta*f)
def D_HY(f, var=x):
    return sp.I * (var * sp.diff(f, var) + Delta * f)

# Eigenfunction: psi_t = x^{-Delta - it}   (HY eq.43)
psi_t = x ** (-Delta - sp.I * t_param)
D_HY_psi = D_HY(psi_t)
eigenvalue = sp.simplify(D_HY_psi / psi_t)

print(f"  psi_t(x) = x^(-Delta - it)")
print(f"  D_HY psi_t / psi_t = {eigenvalue}")
assert eigenvalue == t_param, f"FAIL: eigenvalue is {eigenvalue}, expected t"
print(f"  PASS: D_HY psi_t = t * psi_t  (eigenvalue = t)")

# Also check on monomial x^n
mono = x**n
D_HY_mono = sp.simplify(D_HY(mono))
expected_mono = sp.I * (n + Delta) * x**n
diff_mono = sp.simplify(D_HY_mono - expected_mono)
print(f"\n  D_HY(x^n) = {D_HY_mono}")
print(f"  Expected:   {expected_mono}")
print(f"  Difference: {diff_mono}")
assert diff_mono == 0, f"FAIL on monomial: {diff_mono}"
print(f"  PASS: D_HY(x^n) = i*(n + Delta) * x^n")

# ---------------------------------------------------------------
# BLOCK 2: D_CCM eigenvalue verification
# ---------------------------------------------------------------
print()
print("-" * 60)
print("BLOCK 2: D_CCM eigenvalue verification (CCM eq.5.14)")
print("-" * 60)

# D_CCM g = -i * u * dg/du   (CCM eq.5.14)
def D_CCM(g, var=u):
    return -sp.I * var * sp.diff(g, var)

# Eigenfunction: phi_t = u^{it}
phi_t = u ** (sp.I * t_param)
D_CCM_phi = D_CCM(phi_t)
eigenvalue_CCM = sp.simplify(D_CCM_phi / phi_t)

print(f"  phi_t(u) = u^(it)")
print(f"  D_CCM phi_t / phi_t = {eigenvalue_CCM}")
assert eigenvalue_CCM == t_param, f"FAIL: eigenvalue is {eigenvalue_CCM}, expected t"
print(f"  PASS: D_CCM phi_t = t * phi_t  (eigenvalue = t)")

print(f"\n  REMARK: sigma(D_HY) = sigma(D_CCM) = R (continuous spectrum)")

# ---------------------------------------------------------------
# BLOCK 3: Substitution u = e^x analysis
# ---------------------------------------------------------------
print()
print("-" * 60)
print("BLOCK 3: Substitution u = e^x  =>  D_CCM -> -i d/dx")
print("-" * 60)

# Under u = e^x:  g(u) = f(x),  dg/du = (df/dx)*(dx/du) = (1/u)*(df/dx)
# D_CCM g(u) = -i * u * dg/du = -i * u * (1/u) * df/dx = -i * df/dx
# So: V D_CCM V^{-1} = -i d/dx   (momentum operator P)

f_sym = sp.Function('f')
f_x = f_sym(x)

# Compute D_CCM on g(e^x) by chain rule
# d/du g(u)|_{u=exp(x)} = (1/u)*d/dx g(e^x) = e^{-x} f'(x)
# D_CCM g(u)|_{u=exp(x)} = -i*e^x * e^{-x} * f'(x) = -i*f'(x)
D_CCM_pulled_back = -sp.I * sp.diff(f_x, x)  # -i d/dx

print(f"  D_CCM g(u) |_{{u=exp(x)}} = -i * d/dx f(x)  [MOMENTUM OPERATOR]")
print(f"  This is: {D_CCM_pulled_back}")
print()

# Compare with D_HY on f(x):
D_HY_f = sp.I * (x * sp.diff(f_x, x) + Delta * f_x)
difference = sp.expand(D_HY_f - (-D_CCM_pulled_back + sp.I * Delta * f_x))

print(f"  D_HY f(x) = i*(x*f'(x) + Delta*f(x))")
print(f"  -D_CCM_pb + i*Delta*f = i*f'(x) + i*Delta*f(x)")
print()
print(f"  Difference: D_HY - (-D_CCM_pb + i*Delta) = {difference}")
print()
print(f"  The difference = i*(x-1)*f'(x)")
print(f"  This vanishes ONLY when x = 1 (i.e., u = e^1 = e).")
print()
print(f"  CONCLUSION: The v6.0.23 identity 'D_HY = -D_CCM + i*Delta*id'")
print(f"  is INCORRECT as a pointwise operator identity.")
print(f"  It is valid only at x=1.")

# ---------------------------------------------------------------
# BLOCK 4: What DOES hold -- D_HY = D_sa - epsilon
# ---------------------------------------------------------------
print()
print("-" * 60)
print("BLOCK 4: D_HY = D_sa - epsilon  (correct decomposition)")
print("-" * 60)

# D_sa = i*(x d/dx + 1/2)  [self-adjoint dilatation on L^2(R+, dx)]
def D_sa(f, var=x):
    return sp.I * (var * sp.diff(f, var) + sp.Rational(1, 2) * f)

mono = x**n
D_sa_mono = sp.simplify(D_sa(mono))
D_HY_mono2 = sp.simplify(D_HY(mono))

diff_check = sp.simplify(D_HY_mono2 - D_sa_mono + epsilon * mono)
print(f"  D_sa(x^n) = {D_sa_mono}")
print(f"  D_HY(x^n) = {D_HY_mono2}")
print(f"  D_HY(x^n) - D_sa(x^n) + epsilon*x^n = {diff_check}")
assert diff_check == 0, f"FAIL: {diff_check}"
print(f"  PASS: D_HY = D_sa - epsilon * id  (on monomials)")
print()
print(f"  D_sa is self-adjoint; D_HY is a non-self-adjoint shift of D_sa.")
print(f"  With Delta = 1/2 + i*epsilon:  D_HY = D_sa + i*(Delta - 1/2)*id = D_sa - epsilon*id")

# ---------------------------------------------------------------
# BLOCK 5: Spectral equivalence (both ~ multiplication by t)
# ---------------------------------------------------------------
print()
print("-" * 60)
print("BLOCK 5: Spectral type equivalence via Mellin / Plancherel")
print("-" * 60)
print()
print("  Mellin transform M: L^2(R+, du/u) -> L^2(R, dt)")
print("  M[g](t) = int_0^infty g(u) u^{-it} du/u")
print()
print("  Claim: M D_CCM M^{-1} = T  (multiplication by t on L^2(R, dt))")
print("  Proof: M[D_CCM g](t) = M[-i u dg/du](t)")
print("       = -i * int u * (dg/du) * u^{-it} du/u")
print("       = -i * int (dg/du) * u^{-it} du")
print("       = -i * [u^{-it} g(u)]_0^infty + (-it) * int g(u) u^{-it} du/u * (-i)")
print("       (integration by parts, boundary terms vanish)")
print("       = t * M[g](t)")
print("  QED")
print()
print("  Similarly: the Mellin-type transform for D_HY diagonalizes it")
print("  via psi_t(x) = x^{-Delta-it}, giving eigenvalue t.")
print()
print("  BOTH operators generate the same type of von Neumann algebra:")
print("  L^infty(R, dt) acting as multiplication operators.")
print("  => They are SPECTRALLY EQUIVALENT (unitarily equivalent to M_t).")

# ---------------------------------------------------------------
# BLOCK 6: Corrected statement for R5 paper
# ---------------------------------------------------------------
print()
print("=" * 68)
print("CORRECTED STATEMENT FOR R5 PAPER:")
print("=" * 68)
print("""
  PROPOSITION (Spectral Type Equivalence, sympy-verified 2026-05-03):

  Let D_HY = i*(x d/dx + Delta) on L^2(R+, dx) with Delta = 1/2 + i*epsilon,
  and D_CCM = -i*u*d/du on L^2([lambda^{-1}, lambda], du/u).

  (1) [Eigenvalue check, VERIFIED]:
      D_HY psi_t = t * psi_t   for  psi_t(x) = x^{-Delta-it},   t in R
      D_CCM phi_t = t * phi_t  for  phi_t(u) = u^{it},           t in R

  (2) [Substitution check, VERIFIED]:
      Under u = e^x, D_CCM pulls back to -i*d/dx (momentum operator).
      D_HY = i*(x*d/dx + Delta)  differs from  -D_CCM_pb + i*Delta*id
      by the operator  i*(x-1)*d/dx.
      The v6.0.23 identity is INCORRECT as a pointwise identity.

  (3) [Decomposition, VERIFIED]:
      D_HY = D_sa - epsilon * id,
      where D_sa = i*(x*d/dx + 1/2) is self-adjoint and epsilon = Im(Delta).

  (4) [Spectral equivalence, ARGUED]:
      sigma(D_HY) = sigma(D_CCM) = R  (continuous).
      Both operators are unitarily equivalent to multiplication by t
      on L^2(R, dt) via Mellin/Plancherel.
      They generate isomorphic maximal abelian subalgebras of B(L^2).

  (5) [What R5 claims]:
      The R5 correspondence is at the level of operator ALGEBRAS
      (spectral type equivalence), not at the level of pointwise
      operator equality.  The phrase "algebraic identity" in v6.0.23
      must be read as "spectral type identity".
""")

print("\nAll PASS / VERIFIED blocks completed.")
