import sympy as sp

a = sp.Rational(1,3)
XQ   =  a; Xuc  = -4*a; Xdc  =  2*a; XL   = -3*a; Xec  =  6*a; XN   =  0
YQ   = sp.Rational(1,6); Yuc  = -sp.Rational(2,3); Ydc  = sp.Rational(1,3); YL   = -sp.Rational(1,2); Yec  = sp.Rational(1,1)
mult_Q  = 6; mult_uc = 3; mult_dc = 3; mult_L  = 2; mult_ec = 1; mult_N  = 1

A331 = XQ + sp.Rational(1,2)*Xuc + sp.Rational(1,2)*Xdc
A221 = sp.Rational(3,2)*XQ + sp.Rational(1,2)*XL
A112 = (mult_Q * YQ**2 * XQ + mult_uc * Yuc**2 * Xuc + mult_dc * Ydc**2 * Xdc + mult_L * YL**2 * XL + mult_ec * Yec**2 * Xec)
A211 = (mult_Q * YQ * XQ**2 + mult_uc * Yuc * Xuc**2 + mult_dc * Ydc * Xdc**2 + mult_L * YL * XL**2 + mult_ec * Yec * Xec**2)
A111 = (mult_Q * XQ**3 + mult_uc * Xuc**3 + mult_dc * Xdc**3 + mult_L * XL**3 + mult_ec * Xec**3)
AG1 = (mult_Q * XQ + mult_uc * Xuc + mult_dc * Xdc + mult_L * XL + mult_ec * Xec + mult_N * XN)

print("A_331 =", A331)
print("A_221 =", A221)
print("A_112 =", A112)
print("A_211 =", A211)
print("A_111 =", A111)
print("A_G1  =", AG1)
print("All zero?", all(sp.simplify(v) == 0 for v in [A331,A221,A112,A211,A111,AG1]))
