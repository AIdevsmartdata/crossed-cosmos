#!/usr/bin/env python3
r"""V2 : controle du mecanisme du Lemme Y dans la partie purement gaussienne.
Boite B_n = {|x|_inf <= n} de Z^4 ; R_n = d(1-formes portees par I'_n), I'_n = liens ayant une extremite dans B_{n-1}.
Pour la fonctionnelle v = Y = F_12(0) - F_12(e_1) (et sa translatee v_t de t e_0), on calcule
<v, P_n v> et <v, P_n v_t> (P_n projecteur orthogonal sur R_n dans l^2(plaquettes)), par moindres carres
(|v|^2 - min_w |v - d w|^2 = <v, P v>).  Attendu : croissance en n (R_n croissant) et convergence vers
c(0) = 1.13774949..., c(1) = 0.13774949... (champ libre, P_infini).  Code independant de la v1.
"""
import itertools, json, time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg, LinearOperator

def boite(n):
    R = range(-n, n + 1)
    return [x for x in itertools.product(R, R, R, R)]

def calcule(n, ts=(0, 1, 2)):
    t0 = time.time()
    Bn = set(boite(n))
    inner = lambda x: max(abs(c) for c in x) <= n - 1
    # liens (x, mu) de x a x+e_mu, dans B_n, avec une extremite dans B_{n-1}
    liens = {}
    for x in Bn:
        for mu in range(4):
            y = list(x); y[mu] += 1; y = tuple(y)
            if y in Bn and (inner(x) or inner(y)):
                liens[(x, mu)] = len(liens)
    # plaquettes (x; mu<nu) de B_n touchant ces liens
    plaq = {}
    rows, cols, vals = [], [], []
    for x in Bn:
        for mu, nu in itertools.combinations(range(4), 2):
            xm = list(x); xm[mu] += 1; xm = tuple(xm)
            xn = list(x); xn[nu] += 1; xn = tuple(xn)
            xmn = list(xm); xmn[nu] += 1; xmn = tuple(xmn)
            if not all(z in Bn for z in (xm, xn, xmn)):
                continue
            bords = [((x, mu), 1), ((xm, nu), 1), ((xn, mu), -1), ((x, nu), -1)]
            if not any(l in liens for l, _ in bords):
                continue
            p = plaq.setdefault((x, mu, nu), len(plaq))
            for l, sg in bords:
                if l in liens:
                    rows.append(p); cols.append(liens[l]); vals.append(sg)
    D = sp.coo_matrix((vals, (rows, cols)), shape=(len(plaq), len(liens))).tocsr()
    def vec(t):
        v = np.zeros(len(plaq))
        a = (t, 0, 0, 0); b = (t, 1, 0, 0)   # coordonnee 0 = temps ; plaquettes (1,2) aux points a et a+e_1
        v[plaq[(a, 1, 2)]] += 1.0; v[plaq[(b, 1, 2)]] -= 1.0
        return v
    v0 = vec(0)
    A = (D.T @ D).tocsr()
    rhs = D.T @ v0
    w, info = cg(A, rhs, rtol=1e-12, maxiter=20000)
    Pv0 = D @ w
    out = {"n": n, "liens": len(liens), "plaquettes": len(plaq), "cg_info": int(info)}
    for t in ts:
        out[f"cov_t{t}"] = float(vec(t) @ Pv0)
    out["residu_normal"] = float(np.linalg.norm(D.T @ (v0 - Pv0)))
    out["temps_s"] = round(time.time() - t0, 1)
    return out

if __name__ == "__main__":
    res = []
    for n in [2, 3, 4, 5, 6]:
        r = calcule(n, ts=tuple(t for t in (0, 1, 2) if t <= n - 1))
        res.append(r); print(json.dumps(r), flush=True)
    print(json.dumps({"attendu_c0": 1.1377494917, "attendu_c1": 0.1377494917, "attendu_c2": 0.0183638, "boites": res}, indent=1))
