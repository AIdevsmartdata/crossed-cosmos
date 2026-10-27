# Controle des chiffres introduits dans D7 v1 (SymPy exact + evaluation 30 chiffres).
import sympy as sp
pi=sp.pi
v3=pi**2/12-sp.Rational(1,2); v2=pi**2/4-2
assert sp.simplify(v3+v2-(pi**2/3-sp.Rational(5,2)))==0
assert sp.simplify(v3+v2-2*(pi**2/6-1-sp.Rational(1,4)))==0
D0=8/(9*pi)
thr=lambda C: 1/(9*sp.sqrt(C))
out={
 'Royer Cor2.3 seuil 1/(9*sqrt(1))':thr(1),
 'Royer Thm3.6 seuil':thr(v3+v2),
 'Royer h=0 coef sqrt(v3/4)':sp.sqrt(v3/4),
 'ecart relatif h=0':sp.sqrt(v3/4)/D0-1,
 'pi/16':pi/16,
 'gain / Thm3.6':(pi/16)/thr(v3+v2),
 'gain / Cor2.3':(pi/16)/thr(1),
 'marge Thm3.6 - 1/8':thr(v3+v2)-sp.Rational(1,8),
 'plafond local 779/(21600 pi)':sp.Rational(779,21600)/pi,
 'g0^2 seuil 16/pi':16/pi,
 'g^2 seuil 64/pi':64/pi,
 'TV ordre 1 : E|<u,e>| = 4/(3pi)':4/(3*pi),
 'rapport TV/W1 ordre 1':sp.Rational(4,3)/pi/D0,
}
for k,v in out.items(): print(f"{k:40s} {sp.N(v,15)}")
# Z(K) = 2 pi I_1(K)/K, K=59/50
K=sp.Rational(59,50); Z=2*pi*sp.besseli(1,K)/K
print(f"{'Z(59/50)':40s} {sp.N(Z,15)}")
print(f"{'plafond voie c*/Z(K) 779/(21600 Z(K))':40s} {sp.N(sp.Rational(779,21600)/Z,15)}")
# E_Haar|<u,e>| sur S^3 : densite (2/pi) sqrt(1-x^2)
x=sp.symbols('x'); print(f"{'E|x| (semi-cercle)':40s}", sp.simplify(2*sp.integrate(x*2/pi*sp.sqrt(1-x**2),(x,0,1))))
print("VERDICT OK")
