# Transfert de Gross 1979 (Thm 3, (4.1), (4.7), (4.8), (4.11)) au lien de Wilson SU(2), d=4.
# Potentiel centre phi_p = -(beta/2) Re Tr U_p (sup|phi_p| = beta, minimal parmi les phi_p + cte).
# ||phi||_1 = sup_a sum_{A ni a} sup|phi_A| = 6 beta ; zeta(a,b) = beta pour les 18 voisins, 0 sinon.
from mpmath import mp, findroot, exp, log
mp.dps=30
# Thm 3 (d=0) : alpha_0 = 2 e^{4||phi||_1} sum_b zeta = 36 beta e^{24 beta} < 1
b1=findroot(lambda b: 36*b*exp(24*b)-1, 0.02)
print("Gross Thm 3 (alpha_0<1, unicite + (4.9)) : beta_W <", mp.nstr(b1,10))
# via (4.11) directement dans (2.3),(2.5) (Thm 1, d=0) : rho <= (e^{4 zeta}-1)/2, 18 voisins
b2=log(mp.mpf(10)/9)/4
print("Gross Thm 1 + Lemme 4.1 (4.11) : 18 (e^{4beta}-1)/2 < 1  <=> beta_W <", mp.nstr(b2,10))
