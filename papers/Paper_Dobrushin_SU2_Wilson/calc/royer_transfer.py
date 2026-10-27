# Transfert DIRECT des bornes PUBLIEES de Royer (Ann. IHP A 44 (1986) 29-38, lues sur les images Numdam,
# PDF sha256 6e07d7b5...) au lien de Wilson SU(2) ~ S^3 (n = 3, N = 4).  [calcul exact / numerique]
#  Royer Lemma 1.2 + preuve (3)-(4) p.31 : R(v(K z1 + zeta), v(K z2 + zeta)) <= |K| (C(n)/(n+1))^{1/2} r(z1, z2),
#     C(n) = sup_h C(n,h), C(n,h) = meilleure constante de var(f, v(h)) <= C (Lip f)^2 ; v(h) ∝ exp(x.h) sur S^n.
#  Lien de Wilson : p_l = v(beta*s), s = somme des 6 agrafes ; changer un voisin y deplace UNE agrafe par isometrie
#     => K = beta, r(z1,z2) = rho(y1,y2) ; 18 voisins.
#  Cor. 2.3 p.34 : C(n) <= (n-2)^{-1}           -> n=3 : C <= 1
#  Thm 3.6  p.37 : C(n) <  v_n + v_{n-1} = 2 sum_{k>=n} k^{-2}   -> n=3 : pi^2/3 - 5/2
#  Cor 3.5  p.37 : C(n,0) = v_n ; v_3 = pi^2/12 - 1/2   (h = 0 seulement, pas uniforme)
import sympy as sp
pi = sp.pi
n = 3
res = {}
C_cor23 = sp.Integer(1) / (n - 2)
C_thm36 = 2 * (pi**2 / 6 - 1 - sp.Rational(1, 4))
v3 = pi**2 / 12 - sp.Rational(1, 2)
v2 = pi**2 / 4 - 2
assert sp.simplify(C_thm36 - (v3 + v2)) == 0
for name, C in [("Royer Cor 2.3 (C<=1)", C_cor23), ("Royer Thm 3.6 (C<v3+v2)", C_thm36), ("Royer h=0 seulement (C(3,0)=v3), NON uniforme", v3)]:
    coef = sp.sqrt(C / (n + 1))          # coefficient par voisin / beta
    thr = 1 / (18 * coef)
    print(f"{name:48s} coef/beta = {sp.N(coef, 10)}  seuil beta_W > {sp.N(thr, 10)}  ('t Hooft {sp.N(thr/4, 6)})")
    res[name] = thr
sharp = sp.Rational(8, 9) / pi
print(f"{'note (W1 exact, D(0)=8/(9pi))':48s} coef/beta = {sp.N(sharp, 10)}  seuil beta_W > {sp.N(pi/16, 10)}")
print(f"{'TV exact ordre 1 (4/(3pi))':48s} coef/beta = {sp.N(sp.Rational(4,3)/pi, 10)}  seuil ~ {sp.N(pi/24, 10)}")
print(f"{'SZZ':48s} seuil beta_W < {sp.N(sp.Rational(1,12), 10)}")
print("gain note / Royer Thm 3.6 :", sp.N((pi / 16) / res["Royer Thm 3.6 (C<v3+v2)"], 10))
print("gain note / Royer Cor 2.3 :", sp.N((pi / 16) / res["Royer Cor 2.3 (C<=1)"], 10))
print("ecart relatif h=0 : sqrt(v3/4) / (8/(9pi)) - 1 =", sp.N(sp.sqrt(v3 / 4) / sharp - 1, 6))
print("Royer Thm 3.6 > 1/12 ?", bool(res["Royer Thm 3.6 (C<v3+v2)"] > sp.Rational(1, 12)), "; > 1/8 ?", bool(res["Royer Thm 3.6 (C<v3+v2)"] > sp.Rational(1, 8)))
