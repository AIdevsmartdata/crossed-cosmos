#!/usr/bin/env python3
"""Contrôle indépendant v2 (28/09 : correctif du signe de mpf_to_F) — confronte les coefficients LEAN (commit 7a211ed ; ici lus dans le fichier Donnees.lean) et les his du JSON du certificat
aux polynômes EXACTS E_j(c) de vc_exact.py, boîte par boîte.

Pour la boîte i (α ∈ [iπ/NB, (i+1)π/NB]) et k = 0..19 (coefficient de w^k = E_{2k+2}) :
  sup_box E_{2k+2}  ≤  U_k  (borne RIGOUREUSE : cos encadré par mpmath.iv, Taylor exact en rationnels, bissection)
  sup_box E_{2k+2}  ≥  S_k  (échantillons exacts en des c rationnels intérieurs à la boîte)
Verdicts : c_k^Lean ≥ U_k (+ CST_moi pour k = 0) ⟹ borne VRAIE ; c_k^Lean < S_k ⟹ borne FAUSSE (réfutation).
Reste (ordres ≥ 42) et correction ε recalculés ICI (mpmath.iv), sans le code C2.
"""
import sys, json, re, subprocess, time, os
from fractions import Fraction as F
from math import factorial
from multiprocessing import Pool
import mpmath
from mpmath import iv

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vc_exact as VX   # MON code (séries + A_i structuré)

NB = 160; K = F(118, 100); KW = K * K; N = 16; D = 41
iv.prec = 256

def mpf_to_F(x):
    """v2 : SIGNE conservé. (v1 utilisait mpf.man_exp, dont la mantisse est NON signée : bug des boîtes 80..159.)"""
    sgn, man, e, bc = mpmath.mpf(x)._mpf_
    if man == 0:
        assert e == 0, ("mpf spécial (inf/nan)", x)
        return F(0)
    r = F(int(man)) * (F(2) ** int(e))
    return -r if sgn else r
assert mpf_to_F(mpmath.mpf(-0.75)) == F(-3, 4) and mpf_to_F(mpmath.mpf(0.75)) == F(3, 4) and mpf_to_F(mpmath.mpf(0)) == 0

def c_interval(i):
    """[lo, hi] ⊇ {cos α : α ∈ [iπ/NB, (i+1)π/NB]} (rigoureux), et [ilo, ihi] ⊆ ce même ensemble (intérieur sûr)."""
    ca = iv.cos(iv.pi * i / NB); cb = iv.cos(iv.pi * (i + 1) / NB)   # cos décroissant sur [0, π]
    lo = max(F(-1), mpf_to_F(cb.a)); hi = min(F(1), mpf_to_F(ca.b))
    ilo = mpf_to_F(cb.b); ihi = mpf_to_F(ca.a)
    assert lo <= ilo <= ihi <= hi, ("c_interval incohérent", i, lo, ilo, ihi, hi)
    return lo, hi, ilo, ihi

def dyad(q, bits=24):
    return F(round(q * 2 ** bits), 2 ** bits)

def taylor_shift(p, c0):
    """coefficients de p(c0 + d) en d (exact)."""
    b = list(p); n = len(b)
    for i in range(n):
        for j in range(n - 2, i - 1, -1):
            b[j] += c0 * b[j + 1]
    return b

def sup_upper(p, lo, hi, cible=None, prof=0, profmax=12):
    """majorant rigoureux de max_{[lo,hi]} p ; bissection tant que > cible (si cible donnée)."""
    assert lo <= hi, ("intervalle inversé", lo, hi)
    cm = dyad((lo + hi) / 2); r = max(hi - cm, cm - lo)
    assert r >= 0 and cm - r <= lo and hi <= cm + r, ("rayon", r)
    b = taylor_shift(p, cm)
    u = b[0] + sum(abs(bi) * r ** i for i, bi in enumerate(b) if i >= 1)
    if cible is None or u <= cible or prof >= profmax:
        return u, prof
    m = (lo + hi) / 2
    u1, p1 = sup_upper(p, lo, m, cible, prof + 1, profmax); u2, p2 = sup_upper(p, m, hi, cible, prof + 1, profmax)
    return max(u1, u2), max(p1, p2)

def peval(p, c):
    r = F(0)
    for a in reversed(p): r = r * c + a
    return r

def sample_max(p, ilo, ihi, n=64):
    return max(peval(p, ilo + (ihi - ilo) * F(t, n)) for t in range(n + 1))

# ---------------- reste de Taylor et ε, recalculés ici ----------------
def cst_moi():
    A, (P, H, M) = VX.build_A(N)
    # sup_{|x|,|y|,|c|,|σ| ≤ 1} |A_i| ≤ ℓ1 de tous les coefficients (préfacteurs c², cσ, σ² bornés par 1)
    S = [sum(abs(c) for poly in Ai.values() for c in poly) for Ai in A]
    Ki = iv.mpf(K.numerator) / K.denominator
    Mord = D + 1
    # Σ_{j≥M} |coef_j| κ^j ≤ Σ_i S_i κ^i · κ^{M-i} e^κ/(M-i)! ; ×4 (aire) ; /κ² ; croissant ⟹ κ = K
    tail = sum(iv.mpf(S[i].numerator) / S[i].denominator / iv.factorial(Mord - i) for i in range(2 * N + 1)) \
        * 4 * Ki ** (Mord - 2) * iv.exp(Ki)
    ONE_M_X2 = [F(1), F(0), F(-1)]
    t1 = VX.pmul(ONE_M_X2, P[N]); t2 = VX.padd(VX.pmul(ONE_M_X2, VX.pder(H[N])), VX.psc(-1, VX.pmul([F(0), F(1)], H[N])))
    rho = sum(abs(c) for c in t1) + sum(abs(c) for c in t2)
    # Z(K) = π Σ_k (K²/4)^k/(k!(k+1)!) : 40 termes + queue géométrique (rapport ≤ 1/2 au-delà)
    w4 = Ki * Ki / 4
    Zs = sum(w4 ** k / (iv.factorial(k) * iv.factorial(k + 1)) for k in range(40))
    Zs = Zs + 2 * w4 ** 40 / (iv.factorial(40) * iv.factorial(41))
    ZK = iv.pi * Zs
    eps = 2 * Ki ** (N - 1) * (iv.mpf(rho.numerator) / rho.denominator) * iv.exp(Ki) * ZK / iv.sqrt(3)
    return tail, eps, rho, ZK, S

# ---------------- données Lean ----------------
def lean_certs(source, root=".", path="KevYM/Certif/DobrushinLien/Donnees.lean"):
    # Release packaging (28/09/2026): `source` may be a path to Donnees.lean (read directly) or, as in the
    # original tool, a git commit of a repository at `root` (read by `git show`). Only this function was changed.
    if os.path.isfile(source):
        txt = open(source, encoding="utf-8").read()
    else:
        txt = subprocess.run(["git", "-C", root, "show", f"{source}:{path}"], capture_output=True, text=True, check=True).stdout
    body = txt.split("def certs : List (List ℚ) := [", 1)[1].split("\n]\n", 1)[0]
    boxes = []
    for line in body.strip().splitlines():
        line = line.strip().rstrip(',')
        assert line.startswith('[') and line.endswith(']'), line[:60]
        items = re.findall(r"\((-?\d+):ℚ\)/(\d+)", line)
        assert len(items) == line.count('/'), "élément non reconnu"
        boxes.append([F(int(a), int(b)) for a, b in items])
    kw = re.search(r"def KW : ℚ := (\d+)/(\d+)", txt)
    return boxes, F(int(kw.group(1)), int(kw.group(2))), txt

def travail(args):
    i, Ep, ck, his, CST = args
    lo, hi, ilo, ihi = c_interval(i)
    out = []
    for k in range(20):
        p = Ep[k]
        cible = ck[k] - (CST if k == 0 else 0)
        u, prof = sup_upper(p, lo, hi, cible=cible, profmax=PROFMAX)
        s = sample_max(p, ilo, ihi)
        u_tight, _ = sup_upper(p, lo, hi, cible=s + abs(s) * F(1, 10 ** 6) + F(1, 10 ** 60), profmax=8)
        out.append(dict(k=k, U=u, S=s, Utight=u_tight, prof=prof, vraie=(u <= cible), fausse=(ck[k] < s)))
    return i, out

import os
PROFMAX = int(os.environ.get('VC_PROFMAX', '12'))
CST = None
if __name__ == "__main__":
    t0 = time.time()
    E = json.load(open(sys.argv[1]))["E"]
    Ep = [[F(c) for c in E[str(2 * k + 2)]] for k in range(20)]
    # v2 : couverture de [-1, 1] par les 160 intervalles en c (boîte i : [cos((i+1)π/NB), cos(iπ/NB)])
    ivs = [c_interval(i) for i in range(NB)]
    assert ivs[0][1] == 1 and ivs[-1][0] == -1, "extrémités ±1 non couvertes"
    assert all(ivs[i + 1][1] >= ivs[i][0] for i in range(NB - 1)), "trou entre boîtes"
    print(f"# v2 : couverture [-1,1] OK ; boîtes à c<0 : {sum(1 for v in ivs if v[1] <= 0)} ; parité : E_j pair en c pour tous j pairs ≤ 40 : "
          f"{all(all(c == 0 for c in Ep[k][1::2]) for k in range(20))} (NON utilisé)")
    tail, eps, rho, ZK, S = cst_moi()
    CST = mpf_to_F(tail.b) + mpf_to_F(eps.b)
    print(f"# MON reste (ordres ≥ {D+1})/κ² ≤ {mpmath.nstr(tail.b, 6)} ; ρ_16 = {float(rho):.4e} ; εZ/κ² ≤ {mpmath.nstr(eps.b, 6)} ;"
          f" Z(K) ∈ [{mpmath.nstr(ZK.a, 10)}, {mpmath.nstr(ZK.b, 10)}] ; CST_moi = {float(CST):.6e}")
    certs, kwL, txt = lean_certs(sys.argv[2])
    assert kwL == KW, (kwL, KW)
    assert len(certs) == NB and all(len(c) == 20 for c in certs), ([len(c) for c in certs][:5], len(certs))
    J = json.load(open(sys.argv[3]))
    assert J["cap"] >= J["L"] == 42 and J["N"] == N and J["NG"] == 22 and J["NB"] == NB
    CSTJ = J["CST"]
    his = [[F(h) for h in b["his"]] for b in J["boites"]]
    # 1. Lean c_k = ceil(his·2^40)/2^40 exactement
    ecart_export = 0
    for i in range(NB):
        for k in range(20):
            up = F(-((-his[i][k] * 2 ** 40).numerator // (-his[i][k] * 2 ** 40).denominator), 2 ** 40)
            if certs[i][k] != up or certs[i][k] < his[i][k]: ecart_export += 1
    print(f"# export : Lean c_k == ceil(his_k·2^40)/2^40 et ≥ his_k : écarts = {ecart_export} / {NB*20} ; CST JSON = {CSTJ}")
    # 2. vérification boîte par boîte
    globals()["CST"] = CST
    with Pool(int(sys.argv[4]) if len(sys.argv) > 4 else 8) as pool:
        res = dict(pool.map(travail, [(i, Ep, certs[i], his[i], CST) for i in range(NB)]))
    nv = sum(r["vraie"] for i in res for r in res[i]); nf = sum(r["fausse"] for i in res for r in res[i])
    print(f"# bornes Lean VRAIES (c_k ≥ U_k [+CST_moi]) : {nv} / {NB*20} ; bornes Lean FAUSSES (c_k < échantillon exact) : {nf}")
    # marges
    worst = []
    for i in range(NB):
        for r in res[i]:
            cible = certs[i][r["k"]] - (CST if r["k"] == 0 else 0)
            worst.append((float(cible - r["U"]), float(cible - r["U"]) / max(abs(float(r["S"])), 1e-300), i, r["k"], r["prof"]))
    worst.sort()
    print("# 10 plus petites marges absolues c_k − U_k (marge, marge relative à |E|, boîte, k, profondeur bissection) :")
    for w in worst[:10]: print("   ", w)
    wr = sorted(worst, key=lambda t: t[1])[:10]
    print("# 10 plus petites marges RELATIVES :")
    for w in wr: print("   ", w)
    # 3. MA borne finale avec MES majorants serrés (sans aucune donnée C2) et bP des données Lean refait en rationnels
    def bP(cs, a, b): return sum(max(c * a ** k, c * b ** k) for k, c in enumerate(cs))
    lignes = []
    for i in range(NB):
        mine = [res[i][k]["Utight"] + (CST if k == 0 else 0) for k in range(20)]
        lignes.append((float(bP(certs[i], F(0), KW)), float(bP(mine, F(0), KW)), i))
    wl = max(lignes, key=lambda t: t[0]); wm = max(lignes, key=lambda t: t[1])
    print(f"# bP(Lean) max = {wl[0]:+.8f} (boîte {wl[2]}) ; tous < 0 : {all(l[0] < 0 for l in lignes)}")
    print(f"# bP(MES majorants exacts + CST_moi) max = {wm[1]:+.8f} (boîte {wm[2]}) ; tous < 0 : {all(l[1] < 0 for l in lignes)}")
    zk = mpf_to_F(ZK.b)
    print(f"# constante : −bP_Lean_max / Z(K)_sup = {-wl[0]/float(zk):.7f} (≥ 0.0085 : {F(-wl[0]) / zk >= F(85, 10000)}) ;"
          f" avec mes majorants : {-wm[1]/float(zk):.7f}")
    json.dump(dict(CST_moi=str(CST), lignes=lignes,
                   boites={i: [dict(k=r["k"], U=float(r["U"]), S=float(r["S"]), Ut=float(r["Utight"]), c=float(certs[i][r["k"]]),
                                    vraie=r["vraie"], fausse=r["fausse"]) for r in res[i]] for i in range(NB)}),
              open(sys.argv[5] if len(sys.argv) > 5 else "out/vc_boites.json", "w"))
    print(f"# fini en {time.time()-t0:.0f}s ; VERDICT_BOITES = {'TOUTES_VRAIES' if nv == NB*20 and nf == 0 else 'ECHEC'}")
