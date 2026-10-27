# Transfert de Levin 1980, Remarque 3.6, (3.49), au lien de Wilson SU(2)=S^3 (N=4), d=4.
# Poids exp((beta/2) Re Tr U_p) = exp(beta <u_1 u_2 u_3^* u_4^*, 1>) : fonction multilineaire des 4 vecteurs de S^3,
# |X|=4, J_X = sup |beta <.,1>| = beta ; 6 plaquettes par lien. Critere (3.49) a T=1 :
#   sum_{X ni a} (|X|-1) J_X sqrt(5)/N < 1  <=>  6*3*beta*sqrt(5)/4 < 1.
import sympy as sp
b=sp.symbols('beta',positive=True)
thr=sp.solve(sp.Eq(6*3*b*sp.sqrt(5)/4,1),b)[0]
print("seuil Levin transfere beta_W <", sp.nsimplify(thr), "=", sp.N(thr,12))
print("comparaisons: 1/12 =",sp.N(sp.Rational(1,12),8)," Royer Thm3.6 transf. =",sp.N(1/(9*sp.sqrt(sp.pi**2/3-sp.Rational(5,2))),10)," pi/16 =",sp.N(sp.pi/16,10))
print("ratio pi/16 / Levin =",sp.N(sp.pi/16/thr,8))
# si la conjecture de Levin (Rem. 3.7) valait pour N=4 : facteur sqrt5 -> 1
thr2=sp.Rational(4,18)
print("si conjecture Levin 3.7 (facteur 1 au lieu de sqrt5): beta_W <",thr2,"=",sp.N(thr2,8))
