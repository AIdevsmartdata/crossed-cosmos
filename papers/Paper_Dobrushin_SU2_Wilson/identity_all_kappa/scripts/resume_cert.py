#!/usr/bin/env python3
"""resume_cert.py -- lit les JSON des certificats par boites (Arb : xi_arb_*.json ; mpmath.iv : xi_mpiv_*.json) et calcule :
  * la couverture CONTINUE de [a, b] par l'union des boites de chaque implementation (verifiee en rationnels exacts) ;
  * le nombre de boites, la plus grande marge perdue (pire rapport Xi_hi/P0) par plage ;
  * le verdict global par implementation (toutes les boites OK ET couverture continue).
Usage : python resume_cert.py a b sortie.json fichier1.json [fichier2.json ...]   (les fichiers de UNE implementation, dans n'importe quel ordre).
"""
import json, sys, hashlib
from fractions import Fraction as F

def main():
    a, b = F(sys.argv[1]), F(sys.argv[2])
    out_path = sys.argv[3]
    fichiers = sys.argv[4:]
    boites = []
    metas = []
    for fn in fichiers:
        j = json.load(open(fn))
        metas.append({k: j[k] for k in j if k not in ('boites',)})
        for bx in j['boites']:
            r = bx.get('ratio_hi_f', None)
            if r is None:
                r = float(F(bx['ratio_hi'])) if '/' in bx['ratio_hi'] else float(bx['ratio_hi'])
            boites.append((F(bx['k0']), F(bx['k1']), r, bool(bx['ok']), bx.get('mode', '')))
    boites.sort(key=lambda x: x[0])
    couverture = (boites[0][0] == a) and (boites[-1][1] == b) and all(boites[i][1] == boites[i + 1][0] for i in range(len(boites) - 1))
    toutes = all(x[3] for x in boites)
    plages = []
    bornes = [a] + [F(x) for x in (4, 8, 12, 16)] + [b]
    bornes = sorted(set(x for x in bornes if a <= x <= b))
    for lo, hi in zip(bornes[:-1], bornes[1:]):
        sel = [x for x in boites if lo <= x[0] < hi]
        if not sel:
            continue
        plages.append(dict(plage=[str(lo), str(hi)], n_boites=len(sel), pire_ratio=max(x[2] for x in sel),
                           largeur_min=float(min(x[1] - x[0] for x in sel)), largeur_max=float(max(x[1] - x[0] for x in sel)),
                           modes={m: sum(1 for x in sel if x[4] == m) for m in {x[4] for x in sel}}))
    out = dict(plage_demandee=[str(a), str(b)], n_boites=len(boites), couverture_continue=couverture, toutes_ok=toutes, verdict=bool(couverture and toutes),
               pire_ratio_global=max(x[2] for x in boites), plages=plages, fichiers=fichiers,
               sha256_fichiers={fn: hashlib.sha256(open(fn, 'rb').read()).hexdigest() for fn in fichiers})
    json.dump(out, open(out_path, 'w'), indent=1)
    print(f"[{a},{b}] : {len(boites)} boites ; couverture continue = {couverture} ; toutes OK = {toutes} ; pire Xi_hi/P0 = {out['pire_ratio_global']:+.6f}")
    for p in plages:
        print(f"   plage {p['plage']} : {p['n_boites']} boites (largeurs {p['largeur_min']:.1e}..{p['largeur_max']:.1e}), pire Xi_hi/P0 = {p['pire_ratio']:+.5f}, modes {p['modes']}")
    sys.exit(0 if out['verdict'] else 1)

if __name__ == "__main__":
    main()
