#!/usr/bin/env python3
"""b7_verif11.py — VÉRIFICATEUR INDÉPENDANT (écrit séparément de cert_incline11.c) du certificat incliné, pour m <= 12.

Différences voulues avec le programme C :
  * codage des états RENVERSÉ (d_1 = chiffre de poids FAIBLE ici, de poids FORT en C) : les états sont ré-indexés et H est lu
    par permutation des chiffres ; l'état suivant est recalculé à partir des chiffres, pas par la formule du C ;
  * N(s,d) recalculé par suivi vectoriel des positions (numpy) ;
  * arithmétique EXACTE par « membres » de 22 bits en int64 (aucun entier 128 bits) : on vérifie, pour tout état s,
        Σ_d c_d p[min(N,K)] H[next(s,d)]  <=  P · 2^10 · a · b · H[s]      (c_+e1 = a², c_-e1 = b², sinon a·b),
    forme équivalente à  2^30 Σ_d … <= P · Q · a · b · H[s]  car Q = 2^40.
  * traitement par blocs (mémoire bornée) ; H lu en np.memmap.
Usage : b7_verif11.py m fichier_poids a b H.bin P [--temoin]   (--temoin : s'arrête au premier bloc qui contient une violation)
Sortie : une ligne JSON (violations, marge relative minimale approchée, Hmin, Hmax).
"""
import sys, json, numpy as np
args = [x for x in sys.argv[1:] if not x.startswith('--')]
temoin = '--temoin' in sys.argv
m, fp, a, b, fh, P = int(args[0]), args[1], int(args[2]), int(args[3]), args[4], int(args[5])
assert 1 <= a <= 1024 and 1 <= b <= 1024
t = open(fp).read().split(); Q = int(t[0]); K = int(t[1]); p = [int(x) for x in t[2:2 + K]]
assert Q == 2**40 and all(0 < x <= Q for x in p)
S = 6**m
Hc = np.memmap(fh, dtype=np.uint64, mode='r'); assert Hc.size == S
X = 1 << 22; MASK = X - 1
def membres3(v):                       # entier Python v < 2^66 -> (v2, v1, v0), v = v2 X² + v1 X + v0
    assert 0 <= v < (1 << 66)
    return (v >> 44, (v >> 22) & MASK, v & MASK)
c = [a * a, b * b, a * b, a * b, a * b, a * b]
# W[d][N] = c_d · p[min(N,K)]  (< 2^60), en trois membres ; N de 1 à m+1
Nmax = m + 1
W = np.zeros((6, Nmax + 1, 3), dtype=np.int64)
for d in range(6):
    for N in range(1, Nmax + 1):
        W[d, N] = membres3(c[d] * p[min(N, K) - 1])
Kr = P * (1 << 10) * a * b
assert Kr < (1 << 66)
K2, K1, K0 = membres3(Kr)
step = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=np.int16)
pw = [6**i for i in range(m + 1)]
viol = 0; marge_min = np.inf; Hmin = None; Hmax = None
CH = 1 << 22
for s0 in range(0, S, CH):
    s1 = min(S, s0 + CH)
    idx = np.arange(s0, s1, dtype=np.int64)
    dig = []; tmp = idx.copy()
    for i in range(m):
        dig.append((tmp % 6).astype(np.int64)); tmp //= 6        # dig[i] = d_{i+1} (d_1 = pas le plus récent)
    codeC = np.zeros(s1 - s0, dtype=np.int64)
    for i in range(m):
        codeC += dig[i] * pw[m - 1 - i]                          # codage du programme C (d_1 de poids fort)
    Hs = np.asarray(Hc[codeC]).astype(np.int64)
    hmn, hmx = int(Hs.min()), int(Hs.max())
    Hmin = hmn if Hmin is None else min(Hmin, hmn); Hmax = hmx if Hmax is None else max(Hmax, hmx)
    assert hmn >= 1 and hmx <= (1 << 40)
    pos = np.zeros((s1 - s0, 3), dtype=np.int16)
    Ncnt = np.ones((6, s1 - s0), dtype=np.int64)
    for i in range(m):
        pos -= step[dig[i]]
        for d in range(6):
            Ncnt[d] += (pos == step[d]).all(axis=1)
    # membre gauche : Σ_d W[d,N] · H[next], par membres (X = 2^22) : H = H1 X + H0 (H1 < 2^18)
    L = [np.zeros(s1 - s0, dtype=np.int64) for _ in range(4)]   # coefficients de X^0..X^3
    for d in range(6):
        cn = np.full(s1 - s0, d * pw[m - 1], dtype=np.int64)     # état suivant (d, d_1, …, d_{m-1}) en codage C
        for j in range(m - 1):
            cn += dig[j] * pw[m - 2 - j]
        Hn = np.asarray(Hc[cn]).astype(np.int64)
        H1, H0 = Hn >> 22, Hn & MASK
        w = W[d][Ncnt[d]]                                         # (n, 3) : w2, w1, w0
        w2, w1, w0 = w[:, 0], w[:, 1], w[:, 2]
        L[3] += w2 * H1; L[2] += w2 * H0 + w1 * H1; L[1] += w1 * H0 + w0 * H1; L[0] += w0 * H0
    H1, H0 = Hs >> 22, Hs & MASK
    R = [K0 * H0, K1 * H0 + K0 * H1, K2 * H0 + K1 * H1, K2 * H1]
    D = [R[i] - L[i] for i in range(4)]                           # D = R − L, coefficients signés (|·| < 2^47)
    for i in range(3):                                            # normalisation des retenues : D_i ∈ [0, X)
        q = np.floor_divide(D[i], X); D[i] -= q * X; D[i + 1] += q
    v = D[3] < 0                                                  # R − L < 0  ⟺  violation
    viol += int(v.sum())
    Rf = (R[3] * float(X)**3 + R[2] * float(X)**2 + R[1] * float(X) + R[0])
    Df = (D[3] * float(X)**3 + D[2] * float(X)**2 + D[1] * float(X) + D[0])
    marge_min = min(marge_min, float((Df / Rf).min()))
    if temoin and viol:
        break
print(json.dumps({"m": m, "a": a, "b": b, "P": P, "violations": viol, "marge_relative_min_approx": marge_min,
                  "Hmin": Hmin, "Hmax": Hmax, "etats_verifies": int(s1), "etats": S, "temoin": temoin}))
sys.exit(1 if viol else 0)
