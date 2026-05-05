"""Also check the OTHER possible row-pair interpretation:
   row 1 (u^c, weight-1) vs row 3 (t^c, weight-5).
   And row 1 vs row 2."""
from sympy import symbols, expand, factor, groebner, reduced

a1, a2, a3 = symbols('a1 a2 a3', real=True)
Y1, Y2, Y3 = a1, a2, a3
constraint = a1**2 + 2*a2*a3
G = groebner([constraint], a1, a2, a3, order='lex')

# u^c row: weight-1 in column order (Y1, Y3, Y2)
u3 = Y1; u5 = Y3; u4 = Y2

# c^c row: weight-2 (Y2_3, Y2_5, Y2_4)
c3 = 2*Y1**2 - 2*Y2*Y3
c5 = 2*Y2**2 - 2*Y1*Y3
c4 = 2*Y3**2 - 2*Y1*Y2

# t^c row: weight-5 3̂ (Y5_3, Y5_5, Y5_4)
t3 = 18 * Y1**2 * (-Y2**3 + Y3**3)
t5 = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
      - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
      - 6*Y1**2*Y2*Y3**2)
t4 = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
      + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
      + 6*Y1**2*Y2**2*Y3)

print("Pair u^c (wt1) vs c^c (wt2):")
dot_uc = expand(u3*c3 + u5*c5 + u4*c4)
red = expand(reduced(dot_uc, G, order='lex')[1])
print("  reduced =", red)
print("  factor =", factor(red))

print("\nPair u^c (wt1) vs t^c (wt5):")
dot_ut = expand(u3*t3 + u5*t5 + u4*t4)
red = expand(reduced(dot_ut, G, order='lex')[1])
print("  reduced =", red)
print("  factor =", factor(red))

print("\nPair c^c (wt2) vs t^c (wt5):  (the Opus claim)")
dot_ct = expand(c3*t3 + c5*t5 + c4*t4)
red = expand(reduced(dot_ct, G, order='lex')[1])
print("  reduced =", red)
print("  factor =", factor(red))
