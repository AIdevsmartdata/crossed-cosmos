#!/usr/bin/env python3
"""s3_marches.py -- controle du lemme de marches inclinees et de la decroissance de G (note v1.5, Lemme 7.9).

Usage : python3 -I s3_marches.py <sortie.json>
(a) comptage exact N_k(x,y) des suites de pas (+-e1,+-e2,+-e3) sur le tore (Z/LZ)^3, L in {2,3,4,5}, k <= 12 :
    N_k <= 2 exp(-lam d) (2 cosh lam + 4)^k, d = min_j |R + jL|.
(b) G_L(x, x+R e1) = sum_{k>=1} c^k N_k, c = beta/4, calcule exactement par FFT sur le tore L = 48 :
    G <= 2 exp(-lam R) theta/(1-theta), theta = c (2 cosh lam + 4) < 1, pour une grille de lam ;
    taux -log G(R)/R -> m(beta) = arccosh(2/beta - 2).
Verdicts calcules ; code de retour != 0 en cas d'echec.
"""
import json
import math
import sys

import numpy as np

OK = {}
res = {}

# (a) comptage exact par programmation dynamique
viol = 0
cases = 0
worst = 0.0
for L in (2, 3, 4, 5):
    N = np.zeros((L, L, L), dtype=object)
    N[0, 0, 0] = 1
    for kk in range(1, 13):
        Nn = np.zeros_like(N)
        for ax in range(3):
            Nn = Nn + np.roll(N, 1, axis=ax) + np.roll(N, -1, axis=ax)
        N = Nn
        for R in range(0, L):
            d = min(abs(R + j * L) for j in range(-3, 4))
            cnt = int(N[R % L, 0, 0])
            for lam in (0.0, 0.2, 0.7, 1.5, 3.0):
                bound = 2 * math.exp(-lam * d) * (2 * math.cosh(lam) + 4) ** kk
                cases += 1
                if cnt > bound * (1 + 1e-12):
                    viol += 1
                if bound > 0:
                    worst = max(worst, cnt / bound)
res['a'] = {'cas': cases, 'violations': viol, 'rapport_max_N_sur_borne': worst}
OK['a_comptage_sous_borne'] = viol == 0

# (b) fonction de Green sur le tore par FFT
L = 48
p = 2 * np.pi * np.arange(L) / L
cx, cy, cz = np.meshgrid(np.cos(p), np.cos(p), np.cos(p), indexing='ij')
S = 2 * (cx + cy + cz)  # symbole de la matrice d'adjacence
tab = {}
viol_b = 0
rate_ok = True
for beta in (0.1, 0.3, 0.5, 0.6, 0.65):
    c = beta / 4
    Ghat = 1.0 / (1.0 - c * S) - 1.0
    G = np.real(np.fft.ifftn(Ghat))
    m_beta = math.acosh(2 / beta - 2)
    rows = []
    for R in range(1, L // 2 + 1):
        g = G[R, 0, 0]
        # meilleure borne sur une grille de lam dans [0, m_beta)
        best = float('inf')
        for lam in np.linspace(0, m_beta, 400, endpoint=False)[1:]:
            th = c * (2 * math.cosh(lam) + 4)
            if th < 1:
                best = min(best, 2 * math.exp(-lam * R) * th / (1 - th))
        # plancher de bruit de la FFT en double precision : on ne teste que g > 1e-12
        if g > 1e-12 and g > best * (1 + 1e-9):
            viol_b += 1
        rows.append((R, float(g), float(best)))
    # taux effectif entre R = 8 et R = 16 (loin du bord L/2 = 24), corrige du prefacteur d'Ornstein-Zernike 1/R
    g8, g16 = G[8, 0, 0], G[16, 0, 0]
    rate = -math.log((16 * g16) / (8 * g8)) / 8 if (g8 > 1e-12 and g16 > 1e-12) else float('nan')
    tab[str(beta)] = {'m_beta': m_beta, 'taux_8_16': rate,
                      'G(R)_et_borne': {str(R): [g, b] for R, g, b in rows if R in (1, 2, 4, 8, 12, 16, 24)}}
    # le taux mesure (corrige de 1/R) doit approcher m(beta) a 5 % pres, quand G est au-dessus du bruit
    if not math.isnan(rate) and not (abs(rate - m_beta) / m_beta < 0.05):
        rate_ok = False
res['b'] = tab
res['b_violations'] = viol_b
OK['b_G_sous_borne'] = viol_b == 0
OK['b_taux_proche_de_m_beta'] = rate_ok

res['verdicts'] = OK
res['tous_ok'] = all(OK.values())
out = sys.argv[1] if len(sys.argv) > 1 else 's3_marches.json'
with open(out, 'w') as f:
    json.dump(res, f, indent=1)
for k_, v in OK.items():
    print(f'{k_:30s} {v}')
print('a', res['a'])
for b_, v in tab.items():
    print('beta', b_, 'm', round(v['m_beta'], 4), 'taux(8..16)', round(v['taux_8_16'], 4),
          {R: (f"{g:.3e}", f"{bd:.3e}") for R, (g, bd) in v['G(R)_et_borne'].items()})
print('tous_ok =', res['tous_ok'])
sys.exit(0 if res['tous_ok'] else 1)
