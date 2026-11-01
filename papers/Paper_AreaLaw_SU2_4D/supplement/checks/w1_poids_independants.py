#!/usr/bin/env python3
"""w1_poids_independants.py — vérification adverse (Opus), INDÉPENDANTE de c1/c2.

Méthode différente de c1 (troncature de M_J à l'ordre 10 + reste tau, puis cube d'un polynôme) :
  rho(x) := M_J(x)/M_J(1),  x = u^2,  u = 1 - lambda,  M_J(x) = sum_k c_k J^{2k} x^k,  c_k = 1/(k!(k+1)!).
  h = rho(x)^3 = sum_k e_k x^k  avec e_k >= 0 et  sum_k e_k = rho(1)^3 = 1  EXACTEMENT.
  int_0^1 f_n(lambda) u^{2k} dlambda = beta_{n,k} := (2k+1)!/(n+2k+1)!  (bêta), décroissant en k.
  Donc  A_n in [ S_n , S_n + (1 - E) * beta_{n,len} ],  S_n = sum_{k<len} e_k beta_{n,k},  E = sum_{k<len} e_k.
  M_J(1) = I_1(2J)/J est pris par la fonction de Bessel d'arb (rigoureuse), PAS par la série tronquée.
Les e_k sont obtenus de DEUX façons : (i) arb_series avec ctx.cap FIXÉ ; (ii) convolution explicite en arb (sans
séries). La GARDE : on exige len(coeffs) == K et l'accord (i) = (ii) ; à cap = 10 la garde doit DÉTECTER la troncature.
Contrôle flottant : quadrature mpmath (50 chiffres) avec la vraie fonction de Bessel.
Sortie : encadrements de A_n, de r(N), et comparaison avec les p_n/2^40 du fichier de poids du certificat.
Usage : w1_poids_independants.py J_num J_den fichier_poids sortie_json
"""
import sys, json
from math import factorial
from flint import arb, arb_series, ctx, fmpq
import mpmath as mp

def e_coeffs_series(J, K, cap):
    ctx.cap = cap
    J2 = J * J
    base = arb_series([arb(fmpq(1, factorial(k) * factorial(k + 1))) * J2**k for k in range(K)])
    cube = base * base * base
    co = cube.coeffs()
    return co

def e_coeffs_conv(J, K):
    J2 = J * J
    a = [arb(fmpq(1, factorial(k) * factorial(k + 1))) * J2**k for k in range(K)]
    b = [arb(0)] * K
    for i in range(K):
        for j in range(K - i):
            b[i + j] += a[i] * a[j]
    c = [arb(0)] * K
    for i in range(K):
        for j in range(K - i):
            c[i + j] += b[i] * a[j]
    return c

def enclosures(Jn, Jd, K=40, cap=None, prec=256, nmax=40):
    ctx.prec = prec
    J = arb(fmpq(Jn, Jd))
    M1 = (2 * J).bessel_i(1) / J            # M_J(1) = I_1(2J)/J, rigoureux
    M1c = M1 ** 3
    if cap is None:
        cap = K
    co = e_coeffs_series(J, K, cap)
    length = len(co)
    garde = {"cap": cap, "K_demande": K, "len_obtenu": length, "troncature_detectee": length != K}
    conv = e_coeffs_conv(J, K)
    # accord série/convolution sur les termes communs
    ecart = max(abs(float((co[k] - conv[k]).mid())) for k in range(min(length, K)))
    garde["ecart_max_serie_vs_convolution"] = ecart
    e = [x / M1c for x in co]                # e_k = [x^k] rho^3 ; on utilise la longueur RÉELLE
    E = sum(e, arb(0))
    reste = 1 - E
    A_lo, A_hi = {}, {}
    for n in range(1, nmax + 1):
        beta = [arb(fmpq(factorial(2 * k + 1), factorial(n + 2 * k + 1))) for k in range(length + 1)]
        S = sum((e[k] * beta[k] for k in range(length)), arb(0))
        lo = S.lower()
        hi = (S + reste * beta[length]).upper()
        A_lo[n], A_hi[n] = lo, hi
    return A_lo, A_hi, garde, float(reste.mid())

def mpmath_A(Jn, Jd, nmax=14):
    mp.mp.dps = 50
    J = mp.mpf(Jn) / Jd
    M = lambda x: (mp.besseli(1, 2 * J * mp.sqrt(x)) / (J * mp.sqrt(x))) if x > 0 else mp.mpf(1)
    M1 = M(1)
    h = lambda lam: (M((1 - lam) ** 2) / M1) ** 3
    A = {}
    for n in range(1, nmax + 1):
        A[n] = mp.quad(lambda l: l ** (n - 1) * (1 - l) / mp.factorial(n - 1) * h(l), [0, 0.5, 1])
    return A

if __name__ == "__main__":
    Jn, Jd = int(sys.argv[1]), int(sys.argv[2])
    fpoids, fout = sys.argv[3], sys.argv[4]
    with open(fpoids) as f:
        tok = f.read().split()
    Q, Kw = int(tok[0]), int(tok[1]); p = [None] + [int(t) for t in tok[2:2 + Kw]]
    res = {"J": f"{Jn}/{Jd}", "Q": Q, "K_fichier": Kw}
    # garde de cap : cap = 10 (défaut piégé) puis cap = K
    A_lo10, A_hi10, garde10, reste10 = enclosures(Jn, Jd, K=40, cap=10)
    A_lo, A_hi, garde, reste = enclosures(Jn, Jd, K=40, cap=40)
    A_lo60, A_hi60, garde60, reste60 = enclosures(Jn, Jd, K=60, cap=60)
    res["garde_cap10"] = garde10; res["garde_cap40"] = garde; res["garde_cap60"] = garde60
    res["reste_1_moins_E"] = {"cap10": reste10, "cap40": reste, "cap60": reste60}
    # les encadrements doivent être emboîtés / compatibles
    compat = all(A_lo60[n] <= A_hi[n] and A_lo[n] <= A_hi60[n] and A_lo10[n] <= A_hi[n] for n in range(1, 41))
    res["encadrements_compatibles_cap10_40_60"] = compat
    largeur10 = max(float((A_hi10[n] - A_lo10[n]) / A_lo10[n]) for n in range(1, 14))
    largeur60 = max(float((A_hi60[n] - A_lo60[n]) / A_lo60[n]) for n in range(1, 14))
    res["largeur_relative_max_n<=13"] = {"cap10": largeur10, "cap60": largeur60}
    # bornes sup rigoureuses de r(N) (cap 60), N = 1..40 ; queue N > 40 : r(N) <= 1/(N+1) <= 1/42
    r_sup = {1: A_hi60[1].upper()}
    for N in range(2, 41):
        a = (A_hi60[N] / A_lo60[N - 1]).upper()     # point exact
        b = arb(fmpq(1, N + 1)).upper()             # point exact
        r_sup[N] = a if bool(a <= b) else b
    # contrôle mpmath (flottant)
    Am = mpmath_A(Jn, Jd, 14)
    r_mp = {1: Am[1]}
    for N in range(2, 15):
        r_mp[N] = Am[N] / Am[N - 1]
    res["A_mpmath"] = {n: float(Am[n]) for n in Am}
    res["A_arb_cap60_bas"] = {n: float(A_lo60[n]) for n in range(1, 15)}
    res["A_arb_cap60_haut"] = {n: float(A_hi60[n]) for n in range(1, 15)}
    res["mpmath_dans_encadrement"] = all(float(A_lo60[n]) <= float(Am[n]) * (1 + 1e-30) and
                                         float(Am[n]) <= float(A_hi60[n]) * (1 + 1e-30) for n in range(1, 15))
    res["r_mpmath"] = {N: float(r_mp[N]) for N in r_mp}
    res["r_BS_1_sur_N_plus_1"] = {N: 1.0 / (N + 1) for N in range(1, 15)}
    # vérification : p_n/Q >= sup_{N' >= n} r(N')  (N' <= 40 rigoureux, N' > 40 : 1/(N'+1) <= 1/42)
    verdicts = {}
    ok_all = True
    for n in range(1, Kw + 1):
        cands = [r_sup[N] for N in range(n, 41)] + [arb(fmpq(1, 42)).upper()]
        borne = cands[0]
        for c_ in cands[1:]:
            if bool(c_ > borne):
                borne = c_
        # cas n = Kw : le poids p_Kw sert pour TOUT N >= Kw (queue N > 40 : 1/(N+1) <= 1/42)
        pn = arb(fmpq(p[n], Q))
        ok = bool(pn >= borne)            # comparaison rigoureuse arb (vrai seulement si certain)
        marge = float(((pn - borne) / borne).mid())
        verdicts[n] = {"p_n_sur_Q": p[n] / Q, "sup_r_rigoureux": float(borne.mid()),
                       "OK": ok, "marge_relative": marge}
        ok_all = ok_all and ok
    res["controle_p_n"] = verdicts
    res["TOUS_LES_p_n_SONT_DES_MAJORANTS"] = ok_all
    # non-croissance des p_n
    res["p_non_croissant"] = all(p[n] >= p[n + 1] for n in range(1, Kw))
    with open(fout, "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps({k: res[k] for k in ["garde_cap10", "garde_cap40", "garde_cap60", "encadrements_compatibles_cap10_40_60",
                                          "largeur_relative_max_n<=13", "mpmath_dans_encadrement",
                                          "TOUS_LES_p_n_SONT_DES_MAJORANTS", "p_non_croissant"]}, indent=1, ensure_ascii=False))
    for n in range(1, Kw + 1):
        v = verdicts[n]
        print(f"n={n:2d}  p_n/Q={v['p_n_sur_Q']:.12f}  sup r={v['sup_r_rigoureux']:.12f}  OK={v['OK']}  marge={v['marge_relative']:.3e}")
