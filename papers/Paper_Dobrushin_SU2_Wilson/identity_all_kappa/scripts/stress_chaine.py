#!/usr/bin/env python3
"""stress_chaine.py -- [numerique] test aleatoire (graine fixee) de la chaine  Low <= F <= B <= E x2^2  sur des couples (kappa, alpha) tires au hasard
(kappa log-uniforme dans [0,05 ; 60], alpha uniforme dans [0, 90] degres).  Verdict CALCULE (tolerance de quadrature 5e-7)."""
import sys, math, os, json, random, hashlib
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flux_champ_exact import tabule, flux

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    out = sys.argv[2] if len(sys.argv) > 2 else None
    rnd = random.Random(20261101)
    pire = {"F_moins_B": -1e9, "Low_moins_F": -1e9, "B_moins_Ex": -1e9}
    ok = True
    lignes = []
    for i in range(n):
        k = math.exp(rnd.uniform(math.log(0.05), math.log(60.0)))
        tab = tabule(k, nt=240)
        for _ in range(3):
            ad = rnd.uniform(0.0, 90.0)
            al = math.radians(ad)
            c2 = math.cos(al) ** 2
            F = flux(tab, al)
            B = tab['Ex22'] + c2 * tab['Xi'] / 6
            Low = tab['Ex22'] - c2 * tab['Delta']
            pire["F_moins_B"] = max(pire["F_moins_B"], F - B)
            pire["Low_moins_F"] = max(pire["Low_moins_F"], Low - F)
            pire["B_moins_Ex"] = max(pire["B_moins_Ex"], B - tab['Ex22'])
            chaine = (Low <= F + 5e-7) and (F <= B + 5e-7) and (B <= tab['Ex22'] + 5e-7)
            ok = ok and chaine
            lignes.append(dict(kappa=k, alpha_deg=ad, Low=Low, F=F, B=B, Ex22=tab['Ex22'], ok=bool(chaine)))
    print(f"{len(lignes)} couples (kappa, alpha) aleatoires ; pires ecarts : F-B = {pire['F_moins_B']:+.2e}, Low-F = {pire['Low_moins_F']:+.2e}, B-Ex22 = {pire['B_moins_Ex']:+.2e}")
    print("VERDICT chaine Low <= F <= B <= E x2^2 : " + ("TOUT_OK" if ok else "ECHEC"))
    if out:
        json.dump(dict(script_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(), n=len(lignes), pires=pire, chaine_ok=bool(ok), lignes=lignes), open(out, 'w'), indent=1)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
