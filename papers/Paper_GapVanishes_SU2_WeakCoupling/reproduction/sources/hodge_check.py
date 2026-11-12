#!/usr/bin/env python3
r"""V2, controle (H2) : le laplacien de Hodge des 2-formes du complexe cubique (tore Z_L1 x ... x Z_L4) est
le laplacien scalaire composante par composante.  Code ecrit independamment de la v1 et de Qwen.

Construction : cellules [x; S] (x site, S sous-ensemble ordonne de {0,1,2,3}), bord cubique standard
  d[x; e_{i1}..e_{ik}] = sum_j (-1)^j ( [x+e_{ij}; S \ ij] - [x; S \ ij] ).
Cobords = transposees. Delta_2 = d1 d1^T + d2^T d2 (d1 : liens -> plaquettes, d2 : plaquettes -> cubes),
compare EXACTEMENT (entiers) a (laplacien scalaire du tore) (x) Id_6, la composante (mu,nu) de la 2-forme
etant sa valeur sur la plaquette [x; mu<nu] de point de base x.  Memes tests pour Delta_0, Delta_1, Delta_3,
et d o d = 0.  Tores non cubiques pour eviter les symetries accidentelles.
"""
import itertools, json
import numpy as np
import scipy.sparse as sp

def cellules(L, k):
    sites = list(itertools.product(*[range(l) for l in L]))
    subs = list(itertools.combinations(range(4), k))
    idx = {}
    for x in sites:
        for S in subs:
            idx[(x, S)] = len(idx)
    return idx, sites, subs

MUTANT = False
def bord(L, k, idx_k, idx_km1):
    """matrice de bord C_k -> C_{k-1} (lignes : (k-1)-cellules)"""
    rows, cols, vals = [], [], []
    for (x, S), c in idx_k.items():
        for j, i in enumerate(S):
            T = tuple(s for s in S if s != i)
            xp = list(x); xp[i] = (xp[i] + 1) % L[i]; xp = tuple(xp)
            sgn = (-1) ** j
            if MUTANT and k == 2 and j == 1:
                sgn = -sgn   # mutant : orientation fausse d'une face des plaquettes
            rows += [idx_km1[(xp, T)], idx_km1[(x, T)]]; cols += [c, c]; vals += [sgn, -sgn]
    M = sp.coo_matrix((vals, (rows, cols)), shape=(len(idx_km1), len(idx_k)), dtype=np.int64).tocsr()
    M.sum_duplicates()
    return M

def lap_scalaire(L, sites):
    pos = {x: i for i, x in enumerate(sites)}
    rows, cols, vals = [], [], []
    for x in sites:
        i = pos[x]
        rows.append(i); cols.append(i); vals.append(8)
        for mu in range(4):
            for s in (1, -1):
                y = list(x); y[mu] = (y[mu] + s) % L[mu]
                rows.append(i); cols.append(pos[tuple(y)]); vals.append(-1)
    M = sp.coo_matrix((vals, (rows, cols)), shape=(len(sites), len(sites)), dtype=np.int64).tocsr()
    M.sum_duplicates()
    return M

def test(L):
    idx = {}
    for k in range(5):
        idx[k], sites, subs = cellules(L, k)
    D = {k: bord(L, k, idx[k], idx[k - 1]) for k in range(1, 5)}   # D[k] : C_k -> C_{k-1}
    d = {k: D[k + 1].T.tocsr() for k in range(0, 4)}               # d[k] : C^k -> C^{k+1}
    out = {"L": L}
    out["dd_nul"] = all(abs(d[k + 1] @ d[k]).sum() == 0 for k in range(3))
    lapS = lap_scalaire(L, sites)
    pos = {x: i for i, x in enumerate(sites)}
    for k in range(0, 5):
        Dk = sp.csr_matrix((len(idx[k]), len(idx[k])), dtype=np.int64)
        if k <= 3:
            Dk = Dk + d[k].T @ d[k]
        if k >= 1:
            Dk = Dk + d[k - 1] @ d[k - 1].T
        subs_k = list(itertools.combinations(range(4), k))
        # matrice attendue : lapS (x) Id sur les composantes S
        rows, cols, vals = [], [], []
        lc = lapS.tocoo()
        for S in subs_k:
            for i, j, v in zip(lc.row, lc.col, lc.data):
                rows.append(idx[k][(sites[i], S)]); cols.append(idx[k][(sites[j], S)]); vals.append(v)
        E = sp.coo_matrix((vals, (rows, cols)), shape=Dk.shape, dtype=np.int64).tocsr()
        E.sum_duplicates()
        diff = (Dk - E)
        out[f"Delta_{k}_moins_lapscal_max_abs"] = int(abs(diff).max()) if diff.nnz else 0
        out[f"Delta_{k}_taille"] = Dk.shape[0]
    return out

if __name__ == "__main__":
    res = [test(L) for L in [(3, 3, 3, 3), (3, 4, 5, 3), (4, 4, 4, 4), (5, 3, 4, 6)]]
    # temoin negatif : une orientation fausse dans le bord des plaquettes doit etre detectee
    MUTANT = True
    mut = test((3, 4, 5, 3))
    print(json.dumps({"resultats": res, "mutant_attendu_detecte": mut}, indent=1))
