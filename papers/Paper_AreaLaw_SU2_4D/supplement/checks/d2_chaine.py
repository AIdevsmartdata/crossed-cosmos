#!/usr/bin/env python3
"""d2_chaine.py — vérification adverse (Opus) : cas soluble 2D (tranches = chaîne Z, 2 liens par site).

Exact : E[s_0.s_R] = u^R, u = I_2(2J)/I_1(2J)  (modèle O(4) sur une chaîne = arbre ; dans la tranche d'une théorie de
jauge 2D le rapport Z(J^lambda)/Z(J) vaut exactement prod_l rho(s_l) sur un arbre).
Développement en marches (2.1) : E[s_0.s_R] = 2 * G(R),  G(R) = sum_{w: 0->R} J^|w| int prod_z f_{n_z}(l_z) c(l) dl.
 - G_exact : c(l) = prod_{arêtes e} rho(s_e) EXACT (pas de Cauchy–Schwarz) ; doit donner 2 G_exact = u^R EXACTEMENT
   (teste la normalisation de (2.1) : 1/2 global, J par pas, f_n, facteur (1-l)).
 - G_CS : c(l) <= prod_z rho((1-l_z)^2) (Cauchy–Schwarz, 2 demi-liens par site) ; doit vérifier 2 G_CS >= u^R.
Somme sur les marches calculée SANS troncature en longueur : une marche de 0 à R sur Z est déterminée par ses nombres
de traversées d'arêtes k_e et, en chaque site, l'ordre de ses sorties (théorème BEST sur la droite) :
   k_e = 2 t_e + 1 si 0 <= e <= R-1, 2 t_e sinon ; r_z = montées de (z,z+1), l_z = descentes de (z-1,z) ;
   n_z = r_z + l_z + [z = R] ; nombre d'ordres : C(r+l-1, l) si z < R, C(r+l, l) si z = R, C(r+l-1, r) si z > R.
 -> matrice de transfert le long de z sur l'état t_e (et j_e, indice du développement rho(s) = sum_j g_j s^j, pour
    G_exact ; l'intégrale en l_z donne B(n, e) = int f_n (1-l)^e = (e+1)!/(n+e+1)!).
Contrôle du comptage : énumération brute des marches (longueur <= 14) avec les poids de BS a_n = 1/(n+1)!.
"""
import sys, json, itertools
from math import comb, factorial
import mpmath as mp

mp.mp.dps = 40

def gammas(J, jmax):
    m0 = mp.besseli(1, 2 * J) / J
    return [mp.mpf(J) ** (2 * j) / (mp.factorial(j) * mp.factorial(j + 1)) / m0 for j in range(jmax + 1)]

def Bnf(n, e):
    return mp.factorial(e + 1) / mp.factorial(n + e + 1)

def site_count(z, R, r, l):
    if z == R:
        return comb(r + l, l)          # inclut r = l = 0 : une seule visite (l'arrivée), 1 ordre
    if r + l == 0:
        return 1                       # site non visité
    if z < R:
        if r == 0: return 0
        return comb(r + l - 1, l)
    if z == R:
        return comb(r + l, l)
    if l == 0: return 0
    return comb(r + l - 1, r)

def rl(z, R, t_prev, t_cur):
    r = t_cur + 1 if 0 <= z <= R - 1 else t_cur
    l = t_prev
    return r, l

def kedge(z, R, t):
    return 2 * t + 1 if 0 <= z <= R - 1 else 2 * t

def G_transfer(J, R, weight_site, tmax=22, marge=30):
    """somme sur les marches 0->R de J^|w| prod_z weight_site(n_z) (poids factorisé par site)."""
    J = mp.mpf(J)
    zs = list(range(-marge, R + marge + 1))
    v = {0: mp.mpf(1)}   # état : t de l'arête (z-1, z)
    for z in zs:
        nv = {}
        for tp, val in v.items():
            for tc in range(tmax + 1):
                if z == zs[-1] and tc != 0:
                    continue
                r, l = rl(z, R, tp, tc)
                n = r + l + (1 if z == R else 0)
                cnt = site_count(z, R, r, l)
                if cnt == 0:
                    continue
                w = cnt * (weight_site(n) if n > 0 else 1) * J ** kedge(z, R, tc)
                if w == 0:
                    continue
                nv[tc] = nv.get(tc, 0) + val * w
        v = nv
    return v.get(0, mp.mpf(0))

def G_exact_transfer(J, R, tmax=16, jmax=10, marge=12):
    """somme avec le facteur EXACT c(l) = prod_e rho(s_e), développé en j_e par arête."""
    J = mp.mpf(J); g = gammas(J, jmax)
    zs = list(range(-marge, R + marge + 1))
    v = {(0, j): g[j] for j in range(jmax + 1)}   # arête (z0-1, z0) : t = 0, rho développé
    for z in zs:
        nv = {}
        for (tp, jp), val in v.items():
            for tc in range(tmax + 1):
                if z == zs[-1] and tc != 0:
                    continue
                r, l = rl(z, R, tp, tc)
                n = r + l + (1 if z == R else 0)
                cnt = site_count(z, R, r, l)
                if cnt == 0:
                    continue
                for jc in range(jmax + 1):
                    sf = Bnf(n, jp + jc) if n > 0 else mp.mpf(1)
                    w = cnt * sf * J ** kedge(z, R, tc) * g[jc]
                    key = (tc, jc)
                    nv[key] = nv.get(key, 0) + val * w
        v = nv
    return sum(val for (t, j), val in v.items() if t == 0)

def brute(J, R, Lmax, weight_site):
    tot = mp.mpf(0)
    for L in range(R, Lmax + 1, 2):
        for steps in itertools.product((1, -1), repeat=L):
            if sum(steps) != R: continue
            pos = 0; cnt = {0: 1}
            for s in steps:
                pos += s; cnt[pos] = cnt.get(pos, 0) + 1
            w = mp.mpf(J) ** L
            for n in cnt.values(): w *= weight_site(n)
            tot += w
    return tot

if __name__ == "__main__":
    out = {}
    # 1) contrôle du comptage BEST contre l'énumération brute (poids BS)
    aBS = lambda n: mp.mpf(1) / mp.factorial(n + 1)
    ctl = {}
    for R in (1, 2, 3):
        gt = G_transfer(0.05, R, aBS, tmax=12, marge=10)
        gb = brute(0.05, R, 14 if R != 2 else 14, aBS)
        ctl[R] = {"transfert": float(gt), "brut_L<=14": float(gb), "ecart_rel": float(abs(gt - gb) / gt)}
    out["controle_comptage_J0.05"] = ctl
    print("comptage :", ctl, flush=True)
    # 2) identité exacte 2 G_exact = u^R et borne CS
    res = {}
    for J in ("0.2", "0.4", "0.6"):
        Jm = mp.mpf(J); g = gammas(Jm, 40)
        u = mp.besseli(2, 2 * Jm) / mp.besseli(1, 2 * Jm)
        # poids CS 2D : A2_n = int f_n rho((1-l)^2) = sum_j g_j B(n, 2j)
        A2 = lambda n, g=g: sum(g[j] * Bnf(n, 2 * j) for j in range(len(g)))
        for R in (1, 2, 3, 4):
            ge = G_exact_transfer(Jm, R)
            gc = G_transfer(Jm, R, A2)
            res[f"J={J},R={R}"] = {"u^R": float(u ** R), "2G_exact": float(2 * ge),
                                   "ecart_rel_exact": float(abs(2 * ge - u ** R) / u ** R),
                                   "2G_CS": float(2 * gc), "rapport_2G_CS_sur_u^R": float(2 * gc / u ** R),
                                   "borne_respectee": bool(2 * gc >= u ** R)}
            print(J, R, res[f"J={J},R={R}"], flush=True)
    out["chaine"] = res
    json.dump(out, open(sys.argv[1], "w"), indent=1)
