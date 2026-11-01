#!/usr/bin/env python3
"""ot_controle.py -- [numerique] controle INDEPENDANT par transport optimal DIRECT de  L(kappa, alpha) = D_ch(kappa, alpha).

Par dualite de Kantorovich-Rubinstein, L(kappa, alpha) = sup{Cov_{q_kappa}(g, <v,x>) : g 1-lipschitzienne pour la distance euclidienne de R^4 restreinte a S^3}
est le cout de transport optimal (cout = distance euclidienne) entre u^+ sigma et u^- sigma, u = (<v,x> - E<v,x>) e^{kappa x1}/Zb, v = cos(alpha) e1 + sin(alpha) e2.
Reduction exacte (u et sigma invariantes par les rotations du plan (x3,x4)) : les g peuvent etre prises invariantes ; la condition de Lipschitz devient la
distance euclidienne de R^3 sur le demi-hemisphere {(x1,x2,r), r >= 0} ; mesure image (1/pi) sin^2(theta) sin(psi) dtheta dpsi,
x1 = cos theta, x2 = sin theta cos psi, r = sin theta sin psi.
Discretisation : anneaux en theta (raffines pres du pole pour kappa grand), cellules ~carrees en psi, Gauss 4x4 par cellule, parties + et - separees
(barycentres projetes sur la sphere) ; OT exact du probleme discret : POT (ot.emd2).  Methode du controle de l'audit BB26 v4 (nos propres scripts,
chantiers/audit_bb26_v4_2026-11/scripts/ot_rate_direct.py) ; script ECRIT DE NOUVEAU ici.  Aucun code de tiers.
Reperes exacts : kappa = 0 -> 1/4 pour tout alpha ; alpha = pi/2 -> E x2^2 = I2/(kappa I1) (reflexion).
"""
import argparse, json, hashlib, math, os, sys, time
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
from multiprocessing import Pool
import numpy as np
import ot
from scipy.special import ive

GL_X, GL_W = np.polynomial.legendre.leggauss(4)

def A_of(k):
    return 0.0 if k == 0 else float(ive(2, k) / ive(1, k))

def mesure_discrete(kappa, alpha, nth):
    A = A_of(kappa)
    pref = 1.0 if kappa == 0 else kappa / (2.0 * float(ive(1, kappa)))   # e^kappa / Zb
    if kappa <= 3.0:
        edges = np.linspace(0.0, np.pi, nth + 1)
    else:
        thc = min(np.pi, 9.0 / np.sqrt(kappa))
        e1 = np.linspace(0.0, thc, nth + 1)
        if thc < np.pi:
            n2 = max(4, int(nth * (np.pi - thc) / thc / 6))
            e2 = np.linspace(thc, np.pi, n2 + 1)[1:]
            edges = np.concatenate([e1, e2])
        else:
            edges = e1
    cp, cm = [], []
    for i in range(len(edges) - 1):
        t0, t1 = edges[i], edges[i + 1]
        dth = t1 - t0
        tm = 0.5 * (t0 + t1)
        npsi = max(4, int(round(np.pi * np.sin(tm) / dth)))
        pe = np.linspace(0.0, np.pi, npsi + 1)
        th = t0 + (GL_X + 1) * dth / 2
        wth = GL_W * dth / 2
        for j in range(npsi):
            p0, p1 = pe[j], pe[j + 1]
            ps = p0 + (GL_X + 1) * (p1 - p0) / 2
            wps = GL_W * (p1 - p0) / 2
            TH, PS = np.meshgrid(th, ps, indexing="ij")
            W = np.outer(wth, wps)
            x1 = np.cos(TH)
            x2 = np.sin(TH) * np.cos(PS)
            r = np.sin(TH) * np.sin(PS)
            dens = (np.cos(alpha) * x1 + np.sin(alpha) * x2 - np.cos(alpha) * A) * pref * np.exp(kappa * (x1 - 1.0))
            dm = dens * W * np.sin(TH) ** 2 * np.sin(PS) / np.pi
            pos = dm > 0
            for sel, store in ((pos, cp), (~pos, cm)):
                m = np.abs(dm[sel]).sum()
                if m > 0:
                    P = np.array([(np.abs(dm[sel]) * c[sel]).sum() / m for c in (x1, x2, r)])
                    P /= np.linalg.norm(P)
                    store.append((P, m))
    Pp = np.array([c[0] for c in cp]); mp_ = np.array([c[1] for c in cp])
    Pm = np.array([c[0] for c in cm]); mm_ = np.array([c[1] for c in cm])
    return Pp, mp_, Pm, mm_

def L_ot(args):
    kappa, alpha, nth = args
    Pp, a, Pm, b = mesure_discrete(kappa, alpha, nth)
    tot_a, tot_b = a.sum(), b.sum()
    b2 = b * (tot_a / tot_b)
    M = np.sqrt(((Pp[:, None, :] - Pm[None, :, :]) ** 2).sum(-1))
    cost = ot.emd2(a, b2, M, numItermax=50_000_000)
    return {"kappa": kappa, "alpha_deg": round(float(np.degrees(alpha)), 3), "nth": nth, "L_ot": float(cost),
            "desequilibre_rel": float(abs(tot_a - tot_b) / tot_a), "n_plus": int(len(a)), "n_moins": int(len(b)),
            "Ex22": (0.25 if kappa == 0 else A_of(kappa) / kappa)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kappas", type=str, default="0,0.1,0.25,0.5,0.75,1,1.3333333333333333,1.5,2,2.5,3,3.5,4,5,6,7,8,10,12,15,20,25,30,40,50")
    ap.add_argument("--alphas", type=str, default="0,10,20,30,40,50,60,70,80,90")
    ap.add_argument("--nths", type=str, default="60,90")
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    t0 = time.time()
    ks = [float(x) for x in a.kappas.split(",")]
    als = [math.radians(float(x)) for x in a.alphas.split(",")]
    nths = [int(x) for x in a.nths.split(",")]
    jobs = [(k, al, n) for k in ks for al in als for n in nths]
    with Pool(a.procs) as pool:
        res = pool.map(L_ot, jobs, chunksize=1)
    for r in res:
        print(f"kappa={r['kappa']:7.3f} alpha={r['alpha_deg']:6.1f} nth={r['nth']:3d} L_ot={r['L_ot']:.6f} Ex22={r['Ex22']:.6f} n+={r['n_plus']} n-={r['n_moins']} des={r['desequilibre_rel']:.1e}")
    out = dict(script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), POT=ot.__version__, numpy=np.__version__, resultats=res,
               secondes=round(time.time() - t0, 1))
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"{len(res)} calculs OT en {out['secondes']} s")

if __name__ == "__main__":
    main()
