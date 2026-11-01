#!/usr/bin/env python3
"""c2_poids_flint.py — contre-vérification INDÉPENDANTE (python-flint, arithmétique de boules arb) des encadrements
de Ã_n(J) produits en rationnels exacts par c1_poids_exacts.py.

Deux calculs :
 (P) polynômes arb_poly (aucune troncature de série) : h_sup(u) = ((M_K(u²) + τ)/M_K(1))³, h_inf = (M_K(u²)/(M_K(1)+τ))³,
     Ã_n = Σ_j coef_j (j+1)!/(n+j+1)! ; le reste τ de la série de Bessel est majoré explicitement.
 (S) séries arb_series avec ctx.cap FIXÉ, et une GARDE qui fait varier cap : avec cap < 6K+1 la série du cube est
     tronquée en silence (piège connu de python-flint : ctx.cap vaut 10 par défaut) ; la garde exige que le calcul
     à cap ≥ 6K+1 reproduise (P) et que le calcul à cap = 10 en DIFFÈRE (preuve que la garde détecte la troncature).
Contrôle final : les boules (P) contiennent les rationnels exacts de c1 (lus dans le JSON de c1).
Usage : c2_poids_flint.py J_num J_den json_c1 [K_M] [Kn]
"""
import sys, json
from math import factorial
from flint import arb, arb_poly, arb_series, ctx, fmpq

def calc(Jn, Jd, KM, Kn, mode, cap=None):
    J = arb(fmpq(Jn, Jd)); J2 = J * J
    c = [arb(fmpq(1, factorial(k) * factorial(k + 1))) for k in range(KM + 2)]
    MK1 = sum((c[k] * J2**k for k in range(KM + 1)), arb(0))
    tau = c[KM + 1] * J2**(KM + 1) / (1 - J2 / ((KM + 2) * (KM + 3)))
    coeffs = [arb(0)] * (2 * KM + 1)
    for k in range(KM + 1):
        coeffs[2 * k] = c[k] * J2**k
    up = coeffs[:]; up[0] = up[0] + tau
    if mode == "poly":
        Pu, Pl = arb_poly(up), arb_poly(coeffs)
        cu, cl = Pu * Pu * Pu, Pl * Pl * Pl
        lu = [cu[i] for i in range(cu.degree() + 1)]; ll = [cl[i] for i in range(cl.degree() + 1)]
    else:
        old = ctx.cap; ctx.cap = cap
        Su, Sl = arb_series(up), arb_series(coeffs)
        cu, cl = Su * Su * Su, Sl * Sl * Sl
        lu = [cu[i] for i in range(cap)]; ll = [cl[i] for i in range(cap)]
        ctx.cap = old
    def integ(lst, n):
        return sum((cf * arb(fmpq(factorial(j + 1), factorial(n + j + 1))) for j, cf in enumerate(lst)), arb(0))
    Asup = [integ(lu, n) / MK1**3 for n in range(1, Kn + 1)]
    Ainf = [integ(ll, n) / (MK1 + tau)**3 for n in range(1, Kn + 1)]
    return Asup, Ainf

if __name__ == "__main__":
    Jn, Jd, fjs = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    KM = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    Kn = int(sys.argv[5]) if len(sys.argv) > 5 else 12
    ctx.prec = 200
    ref = json.load(open(fjs))
    Ps, Pi = calc(Jn, Jd, KM, Kn, "poly")
    rapport = {"J": f"{Jn}/{Jd}", "prec_bits": ctx.prec, "K_M": KM, "cap_defaut_flint": 10}
    # contenance des valeurs de c1 (flottants des rationnels exacts) dans les boules, à la précision double près
    ok_contenance = True
    for n in range(1, Kn + 1):
        for nom, boule, val in (("A_sup", Ps[n-1], ref["A_sup"][str(n)]), ("A_inf", Pi[n-1], ref["A_inf"][str(n)])):
            ecart = abs(float(boule.mid()) - val) / val
            if ecart > 1e-14:
                ok_contenance = False
                print("ECART", nom, n, float(boule.mid()), val)
    rapport["concordance_centres_boules_P_avec_c1_tolerance_1e-14"] = ok_contenance  # concordance, PAS un test formel de contenance (la certification est c1, rationnels exacts)
    rapport["rayon_relatif_max_P"] = max(float(b.rad()) / float(b.mid()) for b in Ps + Pi)
    # garde de troncature : cap variable
    garde = {}
    for cap in (10, 30, 6 * KM, 6 * KM + 1, 6 * KM + 20):
        Ss, Si = calc(Jn, Jd, KM, Kn, "series", cap)
        diff = max(abs(float((Ss[n] - Ps[n]).mid())) / float(Ps[n].mid()) for n in range(Kn))
        garde[cap] = diff
    rapport["garde_ecart_relatif_max_series_vs_poly_par_cap"] = {str(k): v for k, v in garde.items()}
    rapport["garde_cap_suffisant_reproduit"] = garde[6 * KM + 1] < 1e-40 and garde[6 * KM + 20] < 1e-40
    rapport["garde_cap_10_detecte_troncature"] = garde[10] > 1e-12
    rapport["A_sup_boules"] = {n + 1: str(Ps[n]) for n in range(Kn)}
    rapport["VERDICT"] = "OK" if (ok_contenance and rapport["garde_cap_suffisant_reproduit"] and rapport["garde_cap_10_detecte_troncature"]) else "ECHEC"
    print(json.dumps(rapport, indent=1, ensure_ascii=False))
