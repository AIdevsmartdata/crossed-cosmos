#!/usr/bin/env python3
"""Exploration (NUMERIQUE) : borne de Cauchy-Schwarz PAR TRANCHE y1 du flux du champ de D7.

|V|^2 = c^2 A^2 + (s E - c a y2)^2 + c^2 a^2 rho^2  (a = A'/3), donc par tranche (boule 3D de rayon R = sqrt(1-y1^2)) :
   int_slice |V| dz <= vol sqrt( c^2 A^2 + s^2 E^2 + c^2 A'^2 R^2/15 ),   vol = (4 pi/3) R^3.
F_CS(alpha) = (2/(3 pi)) int R^3 sqrt( E^2 + c^2 (B - E^2) ) dt,  B = A^2 + A'^2 R^2 / 15.
Integrande concave en c^2  =>  F_CS(alpha) <= E x2^2 pour tout alpha  <=>  (*) int R^3 (B - E^2)/E dt <= 0.
"""
import sys, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from flux_exact_field import tabule

def star(tab):
    T, S, wt, A, Ap, E = tab['T'], tab['S'], tab['wt'], tab['A'], tab['Ap'], tab['E']
    R = S
    B = A ** 2 + Ap ** 2 * R ** 2 / 15
    integrand = R ** 3 * (B - E ** 2) / E
    val = np.sum(wt * S * integrand)         # dt = sin(th) dth
    # normalisations : mass  int R^3 E dt
    mass = np.sum(wt * S * R ** 3 * E)
    pos = np.sum(wt * S * R ** 3 * np.maximum(B - E ** 2, 0) / E)
    return val, mass, pos

def fcs(tab, alpha):
    T, S, wt, A, Ap, E = tab['T'], tab['S'], tab['wt'], tab['A'], tab['Ap'], tab['E']
    R = S
    c2 = math.cos(alpha) ** 2
    B = A ** 2 + Ap ** 2 * R ** 2 / 15
    return 2 / (3 * math.pi) * np.sum(wt * S * R ** 3 * np.sqrt(E ** 2 + c2 * (B - E ** 2)))

if __name__ == "__main__":
    ks = [float(v) for v in sys.argv[1:]] or [0.25, 0.5, 1, 4 / 3, 2, 3, 4, 6, 8, 10, 15, 20, 30, 50]
    for kk in ks:
        tab = tabule(kk, nt=300)
        val, mass, pos = star(tab)
        ex22 = tab['m1'] / kk
        f0 = fcs(tab, math.pi / 2)
        fm = max(fcs(tab, math.pi / 2 * j / 24) for j in range(25))
        print(f"kappa={kk:8.4f}  (*)= {val:+.6e}   (*)/mass = {val / mass:+.5f}   E x2^2={ex22:.6f} (F_CS(pi/2)={f0:.6f})  max_alpha F_CS - E x2^2 = {fm - ex22:+.3e}", flush=True)
