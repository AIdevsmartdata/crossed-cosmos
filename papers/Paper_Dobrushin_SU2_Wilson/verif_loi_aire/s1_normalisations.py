#!/usr/bin/env python3
"""s1_normalisations.py -- controles mecaniques des normalisations (loi d'aire SU(2) 4D).

Usage : python3 -I s1_normalisations.py <sortie.json>
Verdicts calcules (aucun verdict ecrit en dur) ; code de retour != 0 si un controle echoue.

(a) parametrisation de Durhuus-Frohlich (DF79 p.48, (5.1)) : tr(phi(S1)^{-1} phi(S2)) = 2 S1.S2 (et non S1.S2).
(b) quaternions : 1/2 ReTr(phi(u)^dag phi(w)) = <u,w>, phi(u)phi(w) = phi(u*w), ||phi(h)||_op = |h|.
(c) plaquette verticale : 1/2 ReTr(A Qy B^{-1} Qx^{-1}) = <qx, O_{A,B} qy>, O_{A,B} : w -> A w Bbar dans SO(4).
(d) identite de DF79 p.49 sur un tore (Z/3Z)^3 (nu-1 = 3) avec b, t, g aleatoires :
    T1 = sum_{liens} tr(g_i^{-1} b_ij g_j t_ij^{-1}),  T2 = sum_{liens} <S_i, O(b_ij,t_ij) S_j>,
    T3 = -(S, Delta S) + 2(nu-1)|Lambda|, (Delta X)_i = sum_{j~i} (X_i - O_ij X_j)   [DF (5.3)].
    Attendu : T1 = T3 (identite externe juste, liens comptes une fois) et T1 = 2 T2 (membre central faux d'un facteur 2).
(e) tore 4D L = 3 : l'action de Wilson des plaquettes verticales d'une tranche = beta_W sum_{x,mu} <q_x, O q_{x+e_mu}>,
    et chaque lien vertical a exactement 6 liens de la tranche comme voisins (z = 2(d-1)).
(f) table de conversion des seuils (fractions exactes).
"""
import json
import sys
from fractions import Fraction as Fr

import numpy as np

rng = np.random.default_rng(20261101)
OK = {}


def phi(S):
    """Parametrisation de DF79 (5.1) : S=(S0,S1,S2,S3) -> [[S0+iS3, -S1+iS2],[S1+iS2, S0-iS3]]."""
    S0, S1, S2, S3 = S
    return np.array([[S0 + 1j * S3, -S1 + 1j * S2], [S1 + 1j * S2, S0 - 1j * S3]])


def phi_inv(M):
    """Inverse de phi sur les matrices de la forme [[a,-conj(b)],[b,conj(a)]] (a = S0+iS3, b = S1+iS2)."""
    a, b = M[0, 0], M[1, 0]
    return np.array([a.real, b.real, b.imag, a.imag])


def unit4():
    v = rng.normal(size=4)
    return v / np.linalg.norm(v)


def qmul(p, q):
    """Produit de quaternions dans la base de phi (verifie numeriquement en (b) via phi(p)phi(q) = phi(p*q))."""
    return phi_inv(phi(p) @ phi(q))


def O_of(A, B):
    """Matrice 4x4 de w -> phi^{-1}(A phi(w) B^{-1})."""
    cols = []
    for k in range(4):
        e = np.zeros(4)
        e[k] = 1.0
        cols.append(phi_inv(A @ phi(e) @ np.linalg.inv(B)))
    return np.array(cols).T


res = {}
# (a)
ratios = []
for _ in range(2000):
    S1, S2 = unit4(), unit4()
    t = np.trace(np.linalg.inv(phi(S1)) @ phi(S2)).real
    d = float(S1 @ S2)
    if abs(d) > 1e-3:
        ratios.append(t / d)
ratios = np.array(ratios)
res['a_ratio_tr_sur_produit_scalaire'] = [float(ratios.min()), float(ratios.max())]
OK['a_tr_egale_2_fois_produit_scalaire'] = bool(np.allclose(ratios, 2.0, atol=1e-9))

# (b)
errs = []
for _ in range(2000):
    u, w = unit4(), unit4()
    U, W = phi(u), phi(w)
    errs.append(abs(0.5 * np.trace(U.conj().T @ W).real - u @ w))
    errs.append(abs(np.linalg.det(U) - 1))
    errs.append(np.abs(U.conj().T @ U - np.eye(2)).max())
    h = rng.normal(size=4) * 3
    errs.append(abs(np.linalg.norm(phi(h), 2) - np.linalg.norm(h)))
res['b_err_max'] = float(max(errs))
OK['b_quaternions'] = bool(max(errs) < 1e-12)

# (c)
errs, dets, orth = [], [], []
for _ in range(2000):
    A, B = phi(unit4()), phi(unit4())
    qx, qy = unit4(), unit4()
    Qx, Qy = phi(qx), phi(qy)
    lhs = 0.5 * np.trace(A @ Qy @ np.linalg.inv(B) @ np.linalg.inv(Qx)).real
    O = O_of(A, B)
    rhs = qx @ (O @ qy)
    errs.append(abs(lhs - rhs))
    dets.append(np.linalg.det(O))
    orth.append(np.abs(O.T @ O - np.eye(4)).max())
res['c_err_max'] = float(max(errs))
res['c_det_min_max'] = [float(min(dets)), float(max(dets))]
OK['c_plaquette_verticale'] = bool(max(errs) < 1e-12 and max(orth) < 1e-12 and np.allclose(dets, 1.0))

# (d) identite DF79 p.49 sur (Z/3Z)^3
L, D = 3, 3
sites = [(i, j, k) for i in range(L) for j in range(L) for k in range(L)]
idx = {s: n for n, s in enumerate(sites)}
links = []  # (i, j, mu) avec j = i + e_mu (chaque lien une fois)
for s in sites:
    for mu in range(D):
        t_ = list(s)
        t_[mu] = (t_[mu] + 1) % L
        links.append((idx[s], idx[tuple(t_)], mu))
g = [phi(unit4()) for _ in sites]
S = np.array([phi_inv(G) for G in g])
bmat = {l: phi(unit4()) for l in links}
tmat = {l: phi(unit4()) for l in links}
T1 = T2 = 0.0
Ofor = {}
for l in links:
    i, j, mu = l
    b, t = bmat[l], tmat[l]
    T1 += np.trace(np.linalg.inv(g[i]) @ b @ g[j] @ np.linalg.inv(t)).real
    O = O_of(b, t)  # phi^{-1}(b g t^{-1}) = O(b,t) phi^{-1}(g)   [DF (5.2)]
    Ofor[l] = O
    T2 += S[i] @ (O @ S[j])
# (Delta X)_i = sum_{j~i} (X_i - O_ij X_j), avec O_ji = O_ij^{-1} = O_ij^T
DS = np.zeros_like(S)
for l in links:
    i, j, mu = l
    O = Ofor[l]
    DS[i] += S[i] - O @ S[j]
    DS[j] += S[j] - O.T @ S[i]
SDS = float(np.sum(S * DS))
T3 = -SDS + 2 * D * len(sites)
sum_sq = float(sum(np.sum((S[l[0]] - Ofor[l] @ S[l[1]]) ** 2) for l in links))
res['d'] = {'T1_sum_tr': float(T1), 'T2_sum_produit_scalaire': float(T2), 'T3_moins_SDS_plus_2(nu-1)Lambda': float(T3),
            'SDS': SDS, 'somme_liens_|S_i-O S_j|^2': sum_sq, 'nb_liens': len(links), 'nb_sites': len(sites)}
OK['d_T1_egale_T3'] = bool(abs(T1 - T3) < 1e-9)
OK['d_T1_egale_2T2'] = bool(abs(T1 - 2 * T2) < 1e-9)
OK['d_T1_different_de_T2'] = bool(abs(T1 - T2) > 1e-3)
OK['d_SDS_egale_somme_carres'] = bool(abs(SDS - sum_sq) < 1e-9)

# (e) tore 4D L=3 : plaquettes verticales d'une tranche
L4 = 3
dirs = 4
U = {}
sites4 = [(a, b_, c, d_) for a in range(L4) for b_ in range(L4) for c in range(L4) for d_ in range(L4)]
for s in sites4:
    for mu in range(dirs):
        U[(s, mu)] = phi(unit4())


def shift(s, mu, k=1):
    t_ = list(s)
    t_[mu] = (t_[mu] + k) % L4
    return tuple(t_)


def plaq(s, mu, nu):
    return U[(s, mu)] @ U[(shift(s, mu), nu)] @ np.linalg.inv(U[(shift(s, nu), mu)]) @ np.linalg.inv(U[(s, nu)])


beta = 0.6
k0 = 1
act_wilson = 0.0
act_slice = 0.0
for x in [(a, b_, c) for a in range(L4) for b_ in range(L4) for c in range(L4)]:
    s = x + (k0,)
    for mu in range(3):
        act_wilson += beta * 0.5 * np.trace(plaq(s, mu, 3)).real
        # slice model : <q_x, A q_{x+e_mu} Bbar> avec A = U_{(x,k),mu}, B = U_{(x,k+1),mu}, Q_x = U_{(x,k),4}
        A = U[(s, mu)]
        B = U[(shift(s, 3), mu)]
        qx = phi_inv(U[(s, 3)])
        qy = phi_inv(U[(shift(s, mu), 3)])
        act_slice += beta * (qx @ (O_of(A, B) @ qy))
# voisins d'un lien vertical dans sa tranche : liens verticaux partageant une plaquette
s0 = (0, 0, 0, k0)
voisins = set()
for mu in range(3):
    voisins.add((shift(s0, mu), 3))
    voisins.add((shift(s0, mu, -1), 3))
res['e'] = {'action_wilson_tranche': float(act_wilson), 'action_sigma_modele': float(act_slice),
            'nb_voisins_dans_la_tranche': len(voisins)}
OK['e_tranche_J_egale_betaW'] = bool(abs(act_wilson - act_slice) < 1e-9)
OK['e_six_voisins'] = len(voisins) == 6

# (f) conversions (SU(2), d = 4)
conv = {}
for nom, bw in [('2/3 (ce travail)', Fr(2, 3)), ('1/3', Fr(1, 3)), ('2/9 (D7, BB26 Th.E)', Fr(2, 9)),
                ('1/6 (CNS)', Fr(1, 6)), ('1/12 (SZZ)', Fr(1, 12))]:
    conv[nom] = {'beta_W': str(bw), 'beta_tHooft = beta_W/4': str(bw / 4), 'beta_trace_brute = beta_W/2': str(bw / 2),
                 'g^2 = 4/beta_W': str(4 / bw)}
res['f_conversions'] = conv
# DF80 : beta_DF (trace brute) ; modele de l'appendice : J_app = beta_app ; modele de tranche vrai : J = 2 beta_DF = beta_W
nu = 4
df = {
    'enonce_prouve_beta_DF_lt': str(Fr(1, 2 * (nu - 1))),
    'enonce_annonce_beta_DF_lt': str(Fr(1, nu - 1)),
    'lecture_litterale_beta_W_prouve': str(2 * Fr(1, 2 * (nu - 1))),
    'lecture_litterale_beta_W_annonce': str(2 * Fr(1, nu - 1)),
    'ce_que_le_calcul_etablit_beta_W (J_app = beta_W)': str(Fr(1, 2 * (nu - 1))),
    'annonce_corrigee_beta_W': str(Fr(1, nu - 1)),
}
res['f_DF80'] = df
OK['f_DF_litteral_annonce_egale_2_3'] = (2 * Fr(1, nu - 1) == Fr(2, 3))
OK['f_DF_etabli_egale_1_6'] = (Fr(1, 2 * (nu - 1)) == Fr(1, 6))
# seuil de Dobrushin de la tranche : 2(d-1) * beta_W * (1/4) < 1
z = 2 * (nu - 1)
res['f_seuil_tranche_beta_W'] = str(Fr(4, z))
OK['f_seuil_tranche_2_3'] = (Fr(4, z) == Fr(2, 3))

res['verdicts'] = OK
res['tous_ok'] = all(OK.values())
out = sys.argv[1] if len(sys.argv) > 1 else 's1_normalisations.json'
with open(out, 'w') as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
for k, v in OK.items():
    print(f'{k:45s} {v}')
print('(d)', res['d'])
print('(e)', res['e'])
print('tous_ok =', res['tous_ok'])
sys.exit(0 if res['tous_ok'] else 1)
