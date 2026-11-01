#!/usr/bin/env python3
"""Exploration [numerique] : rayon RELATIF de l'enclosure de A~(t) (polynome de Taylor en t, recursion descendante) quand kappa est une boule de largeur w :
montre pourquoi la methode par boites de cert_xi_arb.py cesse de fonctionner vers kappa ~ 20 (inflation de dependance + annulations)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from fractions import Fraction
from flint import arb, arb_poly, ctx
import cert_xi_arb as C
ctx.prec = 256; ctx.cap = 400
for kc, w, N in [(7, '0.01', 100), (10, '0.01', 120), (15, '0.01', 150), (20, '0.01', 180), (20, '0.0001', 180)]:
    Kb = C.ball_interval(Fraction(kc) - Fraction(w) / 2, Fraction(kc) + Fraction(w) / 2)
    m1, Zb, q, a = C.coefficients(Kb, N)
    P = arb_poly(a)
    out = []
    for t0 in ['-0.5', '0', '0.3', '0.6', '0.9', '0.99']:
        fr = Fraction(t0)
        t = arb(fr.numerator) / fr.denominator
        v = P(t)
        out.append(f"t={t0}: rel.rad={float((v.rad() / abs(v.mid())) if v.mid() != 0 else 0):.1e}")
    print(f"kappa={kc} w={w} N={N}  m1 rad={float(m1.rad()):.1e} ; " + " ; ".join(out))
