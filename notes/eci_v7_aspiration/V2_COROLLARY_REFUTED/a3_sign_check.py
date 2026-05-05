"""Numerical verification of |cos|^2 between c^c row and t^c row of M_u
   at tau=i, using the correct real-seed signs from Dedekind eta evaluation."""
import math

# From v2_audit.py output at tau=i:
#   Y1 has phase +45° and |Y1|=1.1803  -> a1 = +1.1803  (a := Y / e^{i pi/4})
#   Y2 has phase -135° and |Y2|=0.2653 -> a2 = -0.2653  (sign flip)
#   Y3 has phase +45° and |Y3|=2.6260  -> a3 = +2.6260
a1, a2, a3 = 1.1803, -0.2653, 2.6260
print(f"a1={a1}  a2={a2}  a3={a3}")
print(f"constraint a1^2 + 2 a2 a3 = {a1**2 + 2*a2*a3:.4e}  (should be ~0)")

# Real direction vector b for c^c row (weight-2 triplet 3)
b3 = 2*a1**2 - 2*a2*a3
b5 = 2*a2**2 - 2*a1*a3
b4 = 2*a3**2 - 2*a1*a2
b = (b3, b5, b4)
print(f"\nb (c^c real direction) = {b}")

# Real direction vector c for t^c row (weight-5 triplet 3̂)
c3 = 18*a1**2*(-a2**3 + a3**3)
c5 = (-4*a1**4*a3 - 4*a1*(a3**4 - 5*a2**3*a3)
      - 14*a1**3*a2**2 + 4*a2**2*(a2**3 + a3**3)
      - 6*a1**2*a2*a3**2)
c4 = (4*a1**4*a2 + 4*a1*(a2**4 - 5*a2*a3**3)
      + 14*a1**3*a3**2 - 4*a3**2*(a2**3 + a3**3)
      + 6*a1**2*a2**2*a3)
c = (c3, c5, c4)
print(f"c (t^c real direction) = {c}")

dot = b3*c3 + b5*c5 + b4*c4
nb = math.sqrt(b3**2 + b5**2 + b4**2)
nc = math.sqrt(c3**2 + c5**2 + c4**2)
print(f"\nb . c     = {dot:.6f}")
print(f"||b||*||c|| = {nb*nc:.6f}")
cos = dot / (nb * nc)
print(f"|cos|     = {abs(cos):.10f}")
print(f"|cos|^2   = {cos**2:.10f}")
print(f"theta     = {math.degrees(math.acos(min(abs(cos),1.0))):.6f} deg")
