#!/usr/bin/env python3
"""s4_tension.py -- borne inferieure de la tension de corde contre la serie de couplage fort (controle de coherence).

Usage : python3 -I s4_tension.py <sortie.json>

Borne de la note : sigma(beta) >= m(beta) = arccosh(2/beta - 2), 0 < beta < 2/3 (beta = beta_W).
Borne grossiere (sans marches inclinees) : -log(3 beta/2).
Valeurs connues : serie de couplage fort de Drouffe-Zuber, Nucl. Phys. B180 [FS2] (1981) 264, Table 1 (lue sur
l'image, ligne SU(2)) : (-k - ln t)/(2(d-2)) = sum_n k_n t^n, d = 4, t = u = I_2(beta)/I_1(beta) (beta = beta_W) :
k_4 = 1, k_8 = 9d - 64/3, k_10 = 8d - 10226/405, k_12 = 364/3 d^2 - 1754/3 d + 865771/1215,
k_14 = 712/3 d^2 - 400081/270 d + 116040611/51030 ; coefficients impairs nuls, k_5 = k_6 = k_7 = 0.
Verdicts calcules : m(beta) < sigma_SC(beta) sur une grille fine de (0, 2/3) ; code de retour != 0 sinon.
"""
import json
import math
import sys
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 30
d = 4
kn = {4: Fr(1), 8: 9 * d - Fr(64, 3), 10: 8 * d - Fr(10226, 405),
      12: Fr(364, 3) * d**2 - Fr(1754, 3) * d + Fr(865771, 1215),
      14: Fr(712, 3) * d**2 - Fr(400081, 270) * d + Fr(116040611, 51030)}


def u_of(b):
    return mp.besseli(2, b) / mp.besseli(1, b)


def sigma_sc(b, nmax=14):
    t = u_of(b)
    s = -mp.log(t)
    for n, c in kn.items():
        if n <= nmax:
            s -= 2 * (d - 2) * mp.mpf(c.numerator) / c.denominator * t**n
    return s


def m_of(b):
    return mp.acosh(2 / mp.mpf(b) - 2)


res = {'k_n_d4': {str(n): str(c) for n, c in kn.items()}}
OK = {}
table = []
for b in ['0.01', '0.05', '0.1', '0.2', str(Fr(2, 9)), '0.3', str(Fr(1, 3)), '0.4', '0.5', '0.55', '0.6', '0.65']:
    bf = mp.mpf(Fr(b).numerator) / Fr(b).denominator
    u = u_of(bf)
    row = {
        'beta_W': b,
        'u=I2/I1': float(u),
        'm(beta)=arccosh(2/beta-2)': float(m_of(bf)),
        '-log(3beta/2)': float(-mp.log(3 * bf / 2)),
        '-ln u': float(-mp.log(u)),
        'sigma_SC (DZ81, ordre 14)': float(sigma_sc(bf)),
        'sigma_SC - m': float(sigma_sc(bf) - m_of(bf)),
        'dernier terme (u^14)': float(2 * (d - 2) * mp.mpf(kn[14].numerator) / kn[14].denominator * u**14),
    }
    table.append(row)
res['table'] = table
# grille fine
grid = [mp.mpf(i) / 1000 for i in range(1, 667)]
marg = [sigma_sc(b) - m_of(b) for b in grid]
res['marge_min'] = float(min(marg))
res['beta_marge_min'] = float(grid[marg.index(min(marg))])
OK['m_sous_sigma_SC_partout'] = min(marg) > 0
# petit beta : sigma_SC - m ~ beta (m ~ log(4/beta) - beta, -ln u ~ log(4/beta) + beta^2/24)
small = [(float(b), float((sigma_sc(b) - m_of(b)) / b)) for b in (mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.05'))]
res['petit_beta_(sigma_SC-m)/beta'] = small
OK['asymptotique_petit_beta'] = all(abs(r - 1) < 0.06 for _, r in small)
# troncature de la serie : |dernier terme| petit devant la marge sur [0, 0.6]
OK['troncature_negligeable_beta_le_0.6'] = all(r['dernier terme (u^14)'] < 1e-6 * r['sigma_SC - m'] for r in table
                                               if float(Fr(r['beta_W'])) <= 0.6)
# plafonds de la methode de tranche (valeurs de la litterature, normalisation J = beta_W par lien)
res['plafonds'] = {
    'champ_moyen_O(4)_z=6 : J z / 4 = 1': 2 / 3,
    'K_c Ising Z^3 (Ferrenberg-Xu-Landau 2018)': 0.221654626,
    'K_c O(4) Z^3 (Kanaya-Kaya 1995, E = sum(1 - s.s))': 0.9360,
}
OK['seuil_sous_Jc_O4'] = 2 / 3 < 0.9360
res['verdicts'] = OK
res['tous_ok'] = all(OK.values())
out = sys.argv[1] if len(sys.argv) > 1 else 's4_tension.json'
with open(out, 'w') as f:
    json.dump(res, f, indent=1)
hdr = ['beta_W', 'u=I2/I1', 'm(beta)=arccosh(2/beta-2)', '-log(3beta/2)', '-ln u', 'sigma_SC (DZ81, ordre 14)', 'sigma_SC - m']
print(' | '.join(hdr))
for r in table:
    print(' | '.join(str(r[h]) if h == 'beta_W' else f'{r[h]:.6f}' for h in hdr))
print('marge min', res['marge_min'], 'en beta =', res['beta_marge_min'])
print('petit beta', small)
for k_, v in OK.items():
    print(f'{k_:40s} {v}')
print('tous_ok =', res['tous_ok'])
sys.exit(0 if res['tous_ok'] else 1)
