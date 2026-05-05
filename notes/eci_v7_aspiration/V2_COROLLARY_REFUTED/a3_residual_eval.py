"""Evaluate the symbolic Groebner-reduced (b.c) residual polynomial at the
   actual (a1,a2,a3) seed values from Dedekind eta at tau=i."""
from sympy import symbols, Rational, sqrt, simplify, N, Symbol
import math
a1s, a2s, a3s = symbols('a1 a2 a3', real=True)

# From sympy run above:
# b . c reduced mod (a1^2 + 2 a2 a3):
expr = (88*a1s*a2s**5*a3s + 8*a1s*a2s**4*a3s**2 - 8*a1s*a2s**2*a3s**4
        - 88*a1s*a2s*a3s**5 + 8*a2s**7 + 16*a2s**6*a3s
        - 216*a2s**5*a3s**2 + 192*a2s**4*a3s**3
        - 192*a2s**3*a3s**4 + 216*a2s**2*a3s**5
        - 16*a2s*a3s**6 - 8*a3s**7)

# High-precision real seeds at tau=i (from Dedekind eta to 200 terms,
# extracted by stripping e^{i pi/4}):
# Y1 = 0.834627+0.834627j -> |Y1| = 1.18034 -> a1 = +1.180339887...
# Y2 = -0.187578-0.187578j -> phase -135 -> a2 = -0.265281...
# Y3 = +1.856832+1.856832j -> a3 = +2.626014...
# These are: a1 = sqrt(2*0.834627^2)*sign(re), but more cleanly
# a1 = Y1 * exp(-i pi/4) which is real:
# Actually let's use the analytic forms:
# Y2/Y1 ≈ -0.22474487 = -(sqrt(3)-1) maybe? sqrt(3)-1 = 0.7320..., no
# Y2/Y1 ≈ -1 + sqrt(3)/2? Not obvious. Just use numerical.

# Use high-precision seeds (more digits):
a1_v = 1.180339887498949
a2_v = -0.265281383454862
a3_v = 2.626014116617432   # need to recompute

# Better: re-derive from Y constraint a1^2 + 2 a2 a3 = 0
# So a3 = -a1^2/(2*a2). Then we have 2 free params a1, a2.
# Numerically from v2_audit: |Y1|=1.1803, |Y2|=0.2653 -> a1=1.1803, a2=-0.2653
# a3 = -1.1803^2 / (2*(-0.2653)) = 1.3931/0.5306 = 2.6256
import math
a1v = 1.180339887498949
a2v = -0.265281383454862
a3v = -a1v**2/(2*a2v)
print(f"a1={a1v}  a2={a2v}  a3={a3v}")
print(f"check a1^2+2a2a3 = {a1v**2+2*a2v*a3v:.3e}")

residual_val = float(expr.subs({a1s: a1v, a2s: a2v, a3s: a3v}))
print(f"\nResidual polynomial value (b.c reduced) = {residual_val:.6e}")

# Compare to direct b.c (which should differ only by a multiple of constraint)
b3 = 2*a1v**2 - 2*a2v*a3v
b5 = 2*a2v**2 - 2*a1v*a3v
b4 = 2*a3v**2 - 2*a1v*a2v
c3 = 18*a1v**2*(-a2v**3 + a3v**3)
c5 = (-4*a1v**4*a3v - 4*a1v*(a3v**4 - 5*a2v**3*a3v)
      - 14*a1v**3*a2v**2 + 4*a2v**2*(a2v**3 + a3v**3)
      - 6*a1v**2*a2v*a3v**2)
c4 = (4*a1v**4*a2v + 4*a1v*(a2v**4 - 5*a2v*a3v**3)
      + 14*a1v**3*a3v**2 - 4*a3v**2*(a2v**3 + a3v**3)
      + 6*a1v**2*a2v**2*a3v)
direct = b3*c3 + b5*c5 + b4*c4
print(f"Direct b.c                              = {direct:.6e}")
print(f"||b||*||c|| = {math.sqrt(b3**2+b5**2+b4**2)*math.sqrt(c3**2+c5**2+c4**2):.6e}")
print(f"|cos|       = {abs(direct)/(math.sqrt(b3**2+b5**2+b4**2)*math.sqrt(c3**2+c5**2+c4**2)):.6e}")

# Check if residual is identically zero
print(f"\nIs residual symbolically zero? {expr == 0}")
print(f"factored: {expr.factor()}")
