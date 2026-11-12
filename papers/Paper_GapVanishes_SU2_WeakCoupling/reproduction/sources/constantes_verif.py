# Verification arithmetique des constantes explicites de la note (v1.0) : 123.73, 6.35e-5 -> c_* = 6e-5
# (ecrit par l'agent d'empaquetage du 11/11/2026 ; calcul exact en mpmath, 30 chiffres)
import mpmath as mp
mp.mp.dps = 30
c3p = mp.pi**mp.mpf('2.5') / (4*mp.sqrt(2))
e = 96 + 6*mp.log(3*mp.pi**3/8) + 6*(mp.mpf(3)/2*mp.log(2) + mp.log(c3p))
print("c3' =", mp.nstr(c3p, 15))
print("energy constant 96+6log(3pi^3/8)+6(3/2 log2+log c3') =", mp.nstr(e, 15))
lb = 8*(2*mp.pi)**-3*(2/mp.pi)**4*mp.e**(-mp.sqrt(3))*mp.mpf(14)/45/(mp.mpf('2.65')*mp.sqrt(3))
print("lower bound constant on c(t) t^6 =", mp.nstr(lb, 15))
print("check 123.73 <= e < 123.74 :", mp.mpf('123.73') <= e < mp.mpf('123.74'))
print("check lb >= 6e-5 :", lb >= mp.mpf('6e-5'))
