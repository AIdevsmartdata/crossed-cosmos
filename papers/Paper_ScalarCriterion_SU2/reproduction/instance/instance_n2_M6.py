#!/usr/bin/env python3
"""Instance inconditionnelle du critère scalaire pour SU(2) Wilson 4D, n = 2 (brouillon 11/11/2026).

Borne élémentaire (aucun développement en amas) :
  Δ₄(2) = 16 log Z(2⁴) − log Z(4⁴) = 16 log Ẑ(2⁴) − log Ẑ(4⁴)        (16·96 = 1536 plaquettes : c₀ et e^{−βN_p} s'annulent)
  Ẑ(Λ) = Σ_{P ⊂ plaquettes} w(P),  w(P) = ∫ Π_{p∈P} f(U_p) dU,  f = e^{(β/2)Tr U}/c₀ − 1,  |f| ≤ ε := e^β/c₀ − 1 ≤ e^β − 1 ≤ β + β².
  w(P) = 0 si un lien de P n'est que dans une plaquette de P (invariance de Haar) ; P fermé = union disjointe (en liens) de
  composantes connexes fermées γ, w(P) = Π w(γ), |w(γ)| ≤ ε^{|γ|}.
  ⇒ log Ẑ(2⁴) ≤ S₂,  Ẑ(4⁴) ≥ 2 − e^{S₄},  S_L := Σ_{γ connexe fermé ⊂ tore L⁴} ε^{|γ|}.
Ce script (1) construit les tores 2⁴ et 4⁴, (2) énumère (Redelmeier) les ensembles connexes de plaquettes contenant une
plaquette racine jusqu'à la taille M et compte les fermés, (3) majore S₂, S₄ en arithmétique rationnelle exacte
(Fraction) et cherche le plus grand β d'une grille rationnelle tel que la borne soit ≤ 2⁻⁹ (et ≤ 2⁻¹²).
Stdlib seulement. À exécuter dans le bac qlab (pas en root, pas sur l'acemagic).
"""
import itertools, json, sys, time
from fractions import Fraction
from math import comb

def construire(L):
    sites = list(itertools.product(range(L), repeat=4))
    sidx = {s: i for i, s in enumerate(sites)}
    def dec(s, mu):
        t = list(s); t[mu] = (t[mu] + 1) % L; return tuple(t)
    def lien(s, mu):
        return sidx[s] * 4 + mu
    plans = [(m, n) for m in range(4) for n in range(m + 1, 4)]
    plaq, orient = [], []
    for s in sites:
        for k, (m, n) in enumerate(plans):
            ls = [lien(s, m), lien(dec(s, m), n), lien(dec(s, n), m), lien(s, n)]
            assert len(set(ls)) == 4, "plaquette à liens répétés"
            plaq.append(ls); orient.append(k)
    nl = len(sites) * 4
    lp = [[] for _ in range(nl)]
    for i, ls in enumerate(plaq):
        for l in ls:
            lp[l].append(i)
    assert all(len(x) == 6 for x in lp), "chaque lien doit être dans 6 plaquettes"
    nb = [sorted(set(j for l in plaq[i] for j in lp[l] if j != i)) for i in range(len(plaq))]
    return plaq, orient, nl, nb

def enumerer(racine, plaq, nl, nb, M, garder_fermes=False, elaguer=True):
    """Redelmeier : chaque ensemble connexe (adjacence = lien commun) contenant la racine, de taille ≤ M, une fois.
    Élagage (elaguer=True) : ajouter une plaquette fait baisser d'au plus 4 le nombre u de liens de multiplicité 1 ;
    un ensemble de taille k avec u > 4(M − k) n'a donc aucun sur-ensemble FERMÉ de taille ≤ M : on coupe la branche.
    Les comptes de fermés sont exacts ; les comptes « tous » ne le sont que si elaguer=False."""
    tous = [0] * (M + 1); fermes = [0] * (M + 1); liste = []
    lc = [0] * nl
    etat = {"uns": 0}
    S = []
    vu = {racine}
    sys.setrecursionlimit(10000)
    def rec(nonessayes):
        nonessayes = list(nonessayes)
        while nonessayes:
            v = nonessayes.pop()
            for l in plaq[v]:
                c = lc[l]
                if c == 0: etat["uns"] += 1
                elif c == 1: etat["uns"] -= 1
                lc[l] = c + 1
            S.append(v); k = len(S)
            tous[k] += 1
            if etat["uns"] == 0:
                fermes[k] += 1
                if garder_fermes: liste.append(sorted(S))
            if k < M and not (elaguer and etat["uns"] > 4 * (M - k)):
                nouveaux = [u for u in nb[v] if u not in vu]
                vu.update(nouveaux)
                rec(nonessayes + nouveaux)
                vu.difference_update(nouveaux)
            S.pop()
            for l in plaq[v]:
                c = lc[l]
                if c == 1: etat["uns"] -= 1
                elif c == 2: etat["uns"] += 1
                lc[l] = c - 1
    rec([racine])
    return tous, fermes, liste

def borne_exp_moins_un(b):
    """majorant rationnel de e^b − 1 pour 0 ≤ b ≤ 1 : b + b² (|e^x − 1 − x| ≤ x² pour |x| ≤ 1)."""
    return b + b * b

E_SUP = Fraction(2719, 1000)   # e < 2,719

def S2_borne(eps, N2, M2, Np2=96):
    s = sum(Fraction(N2[m]) * eps ** m for m in range(1, M2 + 1))
    queue = sum(comb(Np2, m) * eps ** m for m in range(M2 + 1, Np2 + 1))   # nombre de parties de taille m ≤ C(96, m)
    return s + queue

def S4_borne(eps, N4, M4, Np4=1536, D=20):
    s = sum(Fraction(N4[m]) * eps ** m for m in range(1, M4 + 1))
    # queue : N_m ≤ (Np/m)·C(Dm, m−1) (codage BFS) ≤ (Np/m)·e·(D e)^{m−1} ; somme géométrique de raison x = D·e·ε
    x = D * E_SUP * eps
    assert x < 1
    m0 = M4 + 1
    queue = Fraction(Np4, m0) * E_SUP * (D * E_SUP) ** (m0 - 1) * eps ** m0 / (1 - x)
    return s + queue

def borne_delta(beta, N2, M2, N4, M4):
    eps = borne_exp_moins_un(beta)
    S2 = S2_borne(eps, N2, M2); S4 = S4_borne(eps, N4, M4)
    y = borne_exp_moins_un(S4)            # e^{S4} − 1 ≤ S4 + S4²  (S4 ≤ 1)
    assert y < 1
    # −log(2 − e^{S4}) = −log(1 − y) ≤ y/(1 − y)
    return 16 * S2 + y / (1 - y), S2, S4

def main():
    M2 = 6
    M4 = 6
    out = {"M2": M2, "M4": M4}
    for L, M in ((2, M2), (4, M4)):
        t0 = time.time()
        plaq, orient, nl, nb = construire(L)
        Np = len(plaq)
        degs = sorted(set(len(x) for x in nb))
        # contrôles sans élagage (comptes complets) jusqu'à la taille 3 : 1, deg, ...
        tous3, _, _ = enumerer(0, plaq, nl, nb, 3, elaguer=False)
        # une racine par orientation (contrôle de la symétrie hypercubique), fermés jusqu'à min(M, 5)
        par_orient = {}
        for o in range(6):
            r = orient.index(o)
            _, fermes_o, liste = enumerer(r, plaq, nl, nb, min(M, 5), garder_fermes=(L == 2 and o == 0))
            par_orient[o] = fermes_o
            if L == 2 and o == 0:
                out["fermes_racine0_L2_taille_le5"] = liste
        _, fermes, _ = enumerer(0, plaq, nl, nb, M)
        # N_m = (Np/m) × (nombre de fermés connexes de taille m contenant une racine fixée), par transitivité
        N = [0] + [Fraction(Np * fermes[m], m) for m in range(1, M + 1)]
        assert all(x.denominator == 1 for x in N[1:]), "N_m non entier : symétrie mal utilisée"
        assert all(par_orient[o][:6] == fermes[:min(M, 5) + 1] for o in range(6)), "orientations non équivalentes"
        out[f"L{L}"] = {"Np": Np, "nl": nl, "degres": degs, "racine0_tous_le3_sans_elagage": tous3,
                        "racine0_fermes": fermes,
                        "N_m_fermes_connexes": [int(x) for x in N], "fermes_par_orientation_le5": par_orient,
                        "borne_BFS_C(20m,m-1)": [comb(20 * m, m - 1) for m in range(1, M + 1)],
                        "secondes": round(time.time() - t0, 1)}
        print(f"L={L}: Np={Np} degrés={degs} tous(≤3)={tous3} fermés(racine)={fermes} N={[int(x) for x in N]} ({time.time()-t0:.1f}s)", flush=True)
    N2 = [int(x) for x in out["L2"]["N_m_fermes_connexes"]]
    N4 = [int(x) for x in out["L4"]["N_m_fermes_connexes"]]
    res = {}
    for nom, eta in (("2^-9", Fraction(1, 512)), ("2^-12", Fraction(1, 4096))):
        meilleur = None
        for k in range(1, 400):
            beta = Fraction(k, 10000)
            try:
                b, S2, S4 = borne_delta(beta, N2, M2, N4, M4)
            except AssertionError:
                break
            if b <= eta:
                meilleur = (beta, b, S2, S4)
            else:
                break
        if meilleur:
            beta, b, S2, S4 = meilleur
            res[nom] = {"beta_star": str(beta), "beta_star_float": float(beta), "borne_delta": float(b),
                        "borne_delta_exacte": str(b) if len(str(b)) < 400 else None,
                        "S2": float(S2), "S4": float(S4), "eps_borne": float(borne_exp_moins_un(beta))}
            # monotonie : la borne est croissante en β (polynômes à coefficients ≥ 0 en ε, ε croissant)
            b_next, _, _ = borne_delta(beta + Fraction(1, 10000), N2, M2, N4, M4)
            res[nom]["borne_au_pas_suivant"] = float(b_next)
        print(nom, res.get(nom), flush=True)
    out["resultats"] = res
    # table de la borne à quelques β
    table = {}
    for bs in ("1/1000", "2/1000", "3/1000", "4/1000", "5/1000", "6/1000", "7/1000", "8/1000"):
        beta = Fraction(bs)
        try:
            b, S2, S4 = borne_delta(beta, N2, M2, N4, M4)
            table[bs] = {"borne": float(b), "16S2": float(16 * S2), "S4": float(S4)}
        except AssertionError:
            table[bs] = "hors domaine"
    out["table"] = table
    print(json.dumps(table), flush=True)
    json.dump(out, open("instance_n2_sortie.json", "w"), indent=1, default=str)
    print("RESULTAT_JSON " + json.dumps({"N2": N2, "N4": N4, "res": res}), flush=True)

if __name__ == "__main__":
    main()
