#!/usr/bin/env python3
"""cert_delta_boites.py -- certificat par intervalles (Arb) de  Delta(kappa) = m1^2 + 4 m1/kappa - 1 > 0  sur une plage de kappa.

Equivalence : Delta > 0  <=>  m1 > ell,  ell(kappa) = (sqrt(kappa^2 + 4) - 2)/kappa  (racine positive de r^2 + 4 r/kappa - 1).
m1 = I2/I1 est CROISSANTE (m1' = Var x1 > 0) et ell est croissante (ell' = 2(s-2)/(s kappa^2) > 0, s = sqrt(kappa^2+4)) :
sur une boite [k0,k1], m1(k0) > ell(k1)  =>  m1 > ell sur toute la boite.  Bissection adaptative.
Le meme fait est DEMONTRE analytiquement pour tout kappa > 0 (comparaison de Riccati, RAPPORT §2.4) ; ici : controle par intervalles.
Etiquette : [certifie par intervalles] sur la plage couverte (couverture continue verifiee).
"""
import argparse, json, hashlib, sys, time
from fractions import Fraction
from flint import arb, ctx, fmpq
import flint

def aq(fr):
    fr = Fraction(fr)
    return arb(fmpq(fr.numerator, fr.denominator))

def m1_pt(k):
    return k.bessel_i(2) / k.bessel_i(1)

def ell(k):
    return ((k * k + 4).sqrt() - 2) / k

def verifie(lo, hi):
    return bool(m1_pt(aq(lo)).lower() > ell(aq(hi)).upper())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prec", type=int, required=True)
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--k0", type=str, required=True)
    ap.add_argument("--k1", type=str, required=True)
    ap.add_argument("--maxdepth", type=int, default=60)
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    ctx.prec = a.prec; ctx.cap = a.cap
    assert ctx.prec == a.prec and ctx.cap == a.cap
    lo0, hi0 = Fraction(a.k0), Fraction(a.k1)
    boites = []
    echecs = []
    # pile : on traite de gauche a droite (ordre garanti)
    stack = [(lo0, hi0, 0)]
    # initialisation en boites geometriques de rapport 2 pour limiter la profondeur
    pieces = []
    x = lo0
    while x < hi0:
        y = min(hi0, 2 * x)
        pieces.append((x, y)); x = y
    stack = [(x0, y0, 0) for (x0, y0) in reversed(pieces)]
    while stack:
        lo, hi, d = stack.pop()
        if verifie(lo, hi):
            boites.append((lo, hi))
        elif d >= a.maxdepth:
            echecs.append((lo, hi))
        else:
            mid = (lo + hi) / 2
            stack.append((mid, hi, d + 1)); stack.append((lo, mid, d + 1))
    couverture = all(boites[i][1] == boites[i + 1][0] for i in range(len(boites) - 1)) and boites[0][0] == lo0 and boites[-1][1] == hi0 and not echecs
    # marge minimale (m1(k0) - ell(k1)) rapportee a ell : indicateur
    pire = min(boites, key=lambda b: float(((m1_pt(aq(b[0])) - ell(aq(b[1]))) / ell(aq(b[1]))).mid()))
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python_flint=flint.__version__, prec=ctx.prec, cap=ctx.cap,
               k0=a.k0, k1=a.k1, n_boites=len(boites), n_echecs=len(echecs), couverture_continue=couverture,
               pire_marge_relative=float(((m1_pt(aq(pire[0])) - ell(aq(pire[1]))) / ell(aq(pire[1]))).mid()),
               secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"Delta>0 : {len(boites)} boites, {len(echecs)} echecs, couverture continue [{a.k0},{a.k1}] = {couverture} ; pire marge relative (m1(k0)-ell(k1))/ell = "
          f"{out['pire_marge_relative']:.3e} ; {out['secondes']} s")
    sys.exit(0 if couverture else 1)

if __name__ == "__main__":
    main()
