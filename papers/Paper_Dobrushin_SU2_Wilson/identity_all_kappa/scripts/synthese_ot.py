#!/usr/bin/env python3
"""synthese_ot.py -- [numerique] confronte le transport optimal direct (ot_controle.py) aux bornes de la preuve :
      Low(kappa,alpha) = E x2^2 - cos^2(alpha) Delta   <=   L_OT(kappa,alpha)   <=   B(kappa,alpha) = E x2^2 + cos^2(alpha) Xi/6   <=   E x2^2.
L_OT : extrapolation de Richardson en 1/nth^2 (nth = 60, 90) comme dans l'audit BB26 v4.  Verdicts CALCULES (tolerances = ecart de convergence).
Usage : python synthese_ot.py ot_controle.json sortie.json  (lit aussi flux_champ_exact.py pour Xi, Delta, E x2^2).
"""
import json, sys, math, os, hashlib
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flux_champ_exact import tabule, flux

def main():
    res = json.load(open(sys.argv[1]))['resultats']
    by = {}
    for r in res:
        by.setdefault((round(r['kappa'], 6), r['alpha_deg']), {})[r['nth']] = r
    ks = sorted({k for k, _ in by})
    lignes = []
    tols = dict(refl=2e-6, borne=2e-5)
    v_refl = True; v_max90 = True; v_B = True; v_Low = True; v_F = True
    pire_refl = 0.0; pire_B = -1e9; pire_Low = 1e9; pire_conv = 0.0; pire_F = -1e9
    tab = {}
    print("| kappa | alpha | L_OT (Richardson) | Low | B | E x2^2 | B - L_OT |")
    print("|---|---|---|---|---|---|---|")
    for k in ks:
        if k == 0:
            Ex22 = 0.25; Xi = 0.0; Delta = 0.0
        else:
            if k not in tab:
                tab[k] = tabule(k)
            Ex22, Xi, Delta = tab[k]['Ex22'], tab[k]['Xi'], tab[k]['Delta']
        Ls = {}
        for (kk, ad), d in by.items():
            if kk != k:
                continue
            L60, L90 = d[60]['L_ot'], d[90]['L_ot']
            LR = (8100 * L90 - 3600 * L60) / 4500.0
            pire_conv = max(pire_conv, abs(L90 - L60))
            Ls[ad] = LR
            c2 = math.cos(math.radians(ad)) ** 2
            B = Ex22 + c2 * Xi / 6
            Low = Ex22 - c2 * Delta
            F_ = None
            if k > 0:
                F_ = flux(tab[k], math.radians(ad))
                v_B = v_B and (LR <= B + tols['borne'])
                v_Low = v_Low and (LR >= Low - tols['borne'])
                v_F = v_F and (LR <= F_ + tols['borne'])
                pire_B = max(pire_B, LR - B)
                pire_Low = min(pire_Low, LR - Low)
                pire_F = max(pire_F, LR - F_)
            lignes.append(dict(kappa=k, alpha_deg=ad, L_ot=LR, Low=Low, B=B, F=F_, Ex22=Ex22, B_moins_L=B - LR))
        # reflexion et maximum en alpha = 90
        if 90.0 in Ls:
            e = abs(Ls[90.0] - Ex22)
            pire_refl = max(pire_refl, e)
            v_refl = v_refl and (e <= tols['refl'])
            v_max90 = v_max90 and (max(Ls.values()) <= Ls[90.0] + tols['refl'])
    for l in lignes:
        if l['alpha_deg'] in (0.0, 45.0, 90.0):
            print(f"| {l['kappa']:g} | {l['alpha_deg']:g}° | {l['L_ot']:.6f} | {l['Low']:.6f} | {l['B']:.6f} | {l['Ex22']:.6f} | {l['B_moins_L']:+.2e} |")
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), tolerances=tols, lignes=lignes,
               pire_ecart_reflexion=pire_refl, pire_L_moins_B=pire_B, pire_L_moins_Low=pire_Low, pire_ecart_nth60_90=pire_conv,
               verdict_reflexion_L90_egale_Ex22=bool(v_refl), verdict_max_en_alpha_90=bool(v_max90),
               verdict_L_le_B=bool(v_B), verdict_Low_le_L=bool(v_Low), verdict_L_le_F=bool(v_F), pire_L_moins_F=pire_F)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print()
    print(f"VERDICTS (calcules) : L_OT(90°) = E x2^2 a {tols['refl']:g} pres : {v_refl} (pire ecart {pire_refl:.1e}) ; max_alpha L_OT atteint en 90° : {v_max90} ; "
          f"L_OT <= B + {tols['borne']:g} : {v_B} (pire L-B = {pire_B:+.2e}) ; Low <= L_OT + {tols['borne']:g} : {v_Low} (pire L-Low = {pire_Low:+.2e}) ; "
          f"L_OT <= F + {tols['borne']:g} : {v_F} (pire L-F = {pire_F:+.2e}) ; ecart de convergence |L90-L60| max = {pire_conv:.1e}")
    sys.exit(0 if (v_refl and v_max90 and v_B and v_Low and v_F) else 1)

if __name__ == "__main__":
    main()
