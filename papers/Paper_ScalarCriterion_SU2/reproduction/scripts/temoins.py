"""Témoins F1 du critère scalaire (chantier critere_scalaire_2026-11-11). Bac qlab, CPU, quelques minutes.

Tous les Δ sont calculés par la décomposition EXACTE (D) : Δ_d(n) = Σ_j 2^{d-1-j} a_j, a_j = p(section_j, période n),
section_j = (2n)^j n^{d-1-j}, p = 2 log Tr K̂^n − log Tr K̂^{2n} (le vide se simplifie : aucune annulation numérique).

Modèles (spectre de transfert EXACT, produit de facteurs indépendants) :
 (S)  scalaire massif non compact : oscillateurs ω_k = arccosh(1 + (m² + λ_k)/2) ;
 (M4) Maxwell 4D = U(1) de Villain SANS monopôles (holonomies compactes, tous les flux) : 2 photons par k_s ≠ 0,
      3 rotors (flux électrique) E = k² L_i²/(2β V_s), 3 flux magnétiques E = 2π²β m² L_l/(L_i L_j) ;
 (B4) boson compact sans masse (XY de Villain sans vortex) : 1 oscillateur par k_s ≠ 0, rotor E = k²/(2J V_s),
      enroulements E = 2π²J w² V_s/L_i² ;
 (M3) Maxwell 3D gaussien (Villain sans monopôles) : 1 photon par k_s ≠ 0, 2 rotors E = k² L_i/(2β L_j),
      1 flux magnétique E = 2π²β m²/(L_1 L_2).
Contrôle H2 : la formule euclidienne complète (produit des modes 4D/3D + volumes d'orbites + sommes thêta) doit
redonner EXACTEMENT p du transfert (constante de prise de trace nulle) ; contrôle de méthode : Villain 2D exact.
"""
import json, math, itertools
import numpy as np
import mpmath as mp

mp.mp.dps = 40
ETA4, ETA3 = 2.0 ** -9, 2.0 ** -7
OUT = {}

def p_osc_arr(om, N):
    """Σ log coth(Nω/2) = Σ log1p(2u/(1−u)), u = e^{−Nω}."""
    u = np.exp(-N * np.asarray(om, dtype=float))
    return float(np.sum(np.log1p(2 * u / (1 - u))))

def log_theta(a):
    """log Σ_{k∈ℤ} e^{−a k²} (a > 0), par la série directe ou duale (Poisson) selon a."""
    if a >= 1.0:
        s, k = 1.0, 1
        while True:
            t = 2 * math.exp(-a * k * k)
            s += t
            if t < 1e-18 * s:
                break
            k += 1
        return math.log(s)
    b = math.pi ** 2 / a
    s, k = 1.0, 1
    while True:
        t = 2 * math.exp(-b * k * k)
        s += t
        if t < 1e-18 * s:
            break
        k += 1
    return 0.5 * math.log(math.pi / a) + math.log(s)

def p_theta(E, N):
    return 2 * log_theta(N * E) - log_theta(2 * N * E)

def lam_grid(sides):
    g = np.meshgrid(*[4 * np.sin(np.pi * np.arange(L) / L) ** 2 for L in sides], indexing="ij")
    return sum(g).ravel()

# ---------------- p(section, N) pour chaque modèle (réseau) ----------------
def p_scal(sides, N, m2):
    lam = lam_grid(sides) + m2
    om = np.arccosh(1 + lam / 2)
    return p_osc_arr(om, N)

def p_maxwell4(sides, N, beta):
    lam = lam_grid(sides)[1:]          # k_s ≠ 0 (le premier élément est k = 0)
    om = 2 * np.arcsinh(np.sqrt(lam) / 2)
    p = 2 * p_osc_arr(om, N)
    L1, L2, L3 = sides; Vs = L1 * L2 * L3
    for Li in sides:
        p += p_theta(Li * Li / (2 * beta * Vs), N)
    for (i, j, l) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
        p += p_theta(2 * math.pi ** 2 * beta * sides[l] / (sides[i] * sides[j]), N)
    return p

def p_boson4(sides, N, J):
    lam = lam_grid(sides)[1:]
    om = 2 * np.arcsinh(np.sqrt(lam) / 2)
    p = p_osc_arr(om, N)
    Vs = sides[0] * sides[1] * sides[2]
    p += p_theta(1 / (2 * J * Vs), N)
    for Li in sides:
        p += p_theta(2 * math.pi ** 2 * J * Vs / (Li * Li), N)
    return p

def p_maxwell3(sides, N, beta):
    lam = lam_grid(sides)[1:]
    om = 2 * np.arcsinh(np.sqrt(lam) / 2)
    p = p_osc_arr(om, N)
    L1, L2 = sides
    p += p_theta(L1 / (2 * beta * L2), N) + p_theta(L2 / (2 * beta * L1), N)
    p += p_theta(2 * math.pi ** 2 * beta / (L1 * L2), N)
    return p

def Delta(pfun, d, n, *args):
    a = []
    for j in range(d):
        sec = tuple([2 * n] * j + [n] * (d - 1 - j))
        a.append(pfun(sec, n, *args))
    return sum(2 ** (d - 1 - j) * a[j] for j in range(d)), a

# ---------------- contrôle de méthode : Villain 2D exact ----------------
def ctrl_villain2d():
    res = []
    for beta in [mp.mpf('0.3'), mp.mpf(1), mp.mpf(3)]:
        for (n1, n2) in [(1, 1), (2, 3), (4, 4), (5, 7)]:
            V = n1 * n2
            exact = (2 * mp.pi * beta) ** (-mp.mpf(V) / 2) * mp.nsum(lambda r: mp.e ** (-r * r * V / (2 * beta)), [-mp.inf, mp.inf])
            theta = mp.nsum(lambda m: mp.e ** (-2 * mp.pi ** 2 * beta * m * m / V), [-mp.inf, mp.inf])
            form = (2 * mp.pi * beta) ** ((1 - mp.mpf(V)) / 2) * V ** mp.mpf(-0.5) * theta
            res.append(float(abs(exact / form - 1)))
    return max(res)

# ---------------- contrôle H2 : formule euclidienne complète vs transfert ----------------
def logdetp_mp(sides):
    tot = mp.mpf(0)
    for k in itertools.product(*[range(L) for L in sides]):
        if all(x == 0 for x in k):
            continue
        tot += mp.log(sum(4 * mp.sin(mp.pi * ki / L) ** 2 for ki, L in zip(k, sides)))
    return tot

def logtheta_mp(a):
    return mp.log(mp.nsum(lambda m: mp.e ** (-a * m * m), [-mp.inf, mp.inf]))

def logZ_maxwell4_eucl(n4, beta):
    V = n4[0] * n4[1] * n4[2] * n4[3]
    lz = (3 - 3 * V) * mp.log(2 * mp.pi) + mp.log(V) / 2 - logdetp_mp(n4) + mp.mpf(3 * (V - 1)) / 2 * mp.log(2 * mp.pi / beta)
    for mu, nu in itertools.combinations(range(4), 2):
        rs = [x for x in range(4) if x not in (mu, nu)]
        lz += logtheta_mp(2 * mp.pi ** 2 * beta * n4[rs[0]] * n4[rs[1]] / (n4[mu] * n4[nu]))
    return lz

def logZ_maxwell3_eucl(n3, beta):
    V = n3[0] * n3[1] * n3[2]
    lz = (2 - 2 * V) * mp.log(2 * mp.pi) - logdetp_mp(n3) / 2 + (V - 1) * mp.log(2 * mp.pi / beta)
    for mu, nu in itertools.combinations(range(3), 2):
        r = [x for x in range(3) if x not in (mu, nu)][0]
        lz += logtheta_mp(2 * mp.pi ** 2 * beta * n3[r] / (n3[mu] * n3[nu]))
    return lz

def logZ_boson4_eucl(n4, J):
    V = n4[0] * n4[1] * n4[2] * n4[3]
    lz = (1 - V) * mp.log(2 * mp.pi) + mp.log(V) / 2 + mp.mpf(V - 1) / 2 * mp.log(2 * mp.pi / J) - logdetp_mp(n4) / 2
    for mu in range(4):
        lz += logtheta_mp(2 * mp.pi ** 2 * J * V / n4[mu] ** 2)
    return lz

def ctrl_H2():
    out = {}
    worst = 0.0
    for beta in [mp.mpf('0.2'), mp.mpf('1.3')]:
        for sec in [(2, 2, 2), (2, 3, 2), (3, 2, 4)]:
            for N in [2, 3]:
                pe = 2 * logZ_maxwell4_eucl(sec + (N,), beta) - logZ_maxwell4_eucl(sec + (2 * N,), beta)
                pt = p_maxwell4(sec, N, float(beta))
                worst = max(worst, abs(float(pe) - pt) / max(1.0, abs(pt)))
    out["maxwell4_ecart_rel_max"] = worst
    worst = 0.0
    for beta in [mp.mpf('0.2'), mp.mpf('1.3'), mp.mpf(4)]:
        for sec in [(2, 2), (2, 3), (3, 4), (5, 2)]:
            for N in [2, 3, 4]:
                pe = 2 * logZ_maxwell3_eucl(sec + (N,), beta) - logZ_maxwell3_eucl(sec + (2 * N,), beta)
                pt = p_maxwell3(sec, N, float(beta))
                worst = max(worst, abs(float(pe) - pt) / max(1.0, abs(pt)))
    out["maxwell3_ecart_rel_max"] = worst
    worst = 0.0
    for J in [mp.mpf('0.05'), mp.mpf('0.7')]:
        for sec in [(2, 2, 2), (2, 3, 2)]:
            for N in [2, 3]:
                pe = 2 * logZ_boson4_eucl(sec + (N,), J) - logZ_boson4_eucl(sec + (2 * N,), J)
                pt = p_boson4(sec, N, float(J))
                worst = max(worst, abs(float(pe) - pt) / max(1.0, abs(pt)))
    out["boson4_ecart_rel_max"] = worst
    # symétrie H1 : log Z euclidien invariant par permutation des axes (Maxwell 4D, tore 2×3×2×4)
    a = logZ_maxwell4_eucl((2, 3, 2, 4), mp.mpf('0.7')); b = logZ_maxwell4_eucl((4, 2, 3, 2), mp.mpf('0.7'))
    out["maxwell4_H1_ecart"] = float(abs(a - b))
    return out

# ---------------- continuum : spectre à taille physique fixée ----------------
def p_cont_scal(lams, x, d):
    """Section de côtés λ_i ∈ {1,2} (unités ℓ), temps T = 1, masse x = Mℓ."""
    K = 40
    grids = np.meshgrid(*[2 * np.pi * np.arange(-K, K + 1) / lam for lam in lams], indexing="ij")
    k2 = sum(g ** 2 for g in grids).ravel()
    om = np.sqrt(x * x + k2)
    om = om[om < 80]
    return p_osc_arr(om, 1.0)

def Delta_cont_scal(x, d):
    a = []
    for j in range(d):
        lams = [2] * j + [1] * (d - 1 - j)
        a.append(p_cont_scal(lams, x, d))
    return sum(2 ** (d - 1 - j) * a[j] for j in range(d))

def seuil(f, eta, lo, hi):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) > eta:
            lo = mid
        else:
            hi = mid
    return hi

if __name__ == "__main__":
    OUT["ctrl_villain2d_ecart_rel_max"] = ctrl_villain2d()
    OUT["ctrl_H2"] = ctrl_H2()
    print("contrôles :", OUT["ctrl_villain2d_ecart_rel_max"], OUT["ctrl_H2"], flush=True)

    # borne universelle (photons de plus petite impulsion) : Δ₄ ≥ 8 log(1+12 e^{-2π}), Δ₃ ≥ 4 log(1+4 e^{-2π})
    OUT["borne_M4"] = 8 * math.log1p(12 * math.exp(-2 * math.pi))
    OUT["borne_B4"] = 8 * math.log1p(6 * math.exp(-2 * math.pi))
    OUT["borne_M3"] = 4 * math.log1p(4 * math.exp(-2 * math.pi))

    # (M4) Maxwell 4D : Δ₄(n; β)
    tab = {}
    for beta in [0.02, 0.05, 0.1, 1 / (2 * math.pi), 0.3, 0.5, 1.0, 2.0, 5.0]:
        row = {}
        for n in [2, 3, 4, 6, 8, 12, 16, 24, 32]:
            D, a = Delta(p_maxwell4, 4, n, beta)
            row[n] = D
        tab[f"{beta:.5g}"] = row
    OUT["M4_Delta"] = tab
    # zéro-modes seuls (n-indépendant pour profils homothétiques) : minimum sur β
    def zm4(beta, n=8):
        tot = 0.0
        for j in range(4):
            sec = tuple([2 * n] * j + [n] * (3 - j)); Vs = sec[0] * sec[1] * sec[2]
            pz = sum(p_theta(Li * Li / (2 * beta * Vs), n) for Li in sec)
            pz += sum(p_theta(2 * math.pi ** 2 * beta * sec[l] / (sec[i] * sec[j2]), n)
                      for (i, j2, l) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)])
            tot += 2 ** (3 - j) * pz
        return tot
    bs = np.exp(np.linspace(np.log(0.01), np.log(10), 400))
    zs = [zm4(b) for b in bs]
    i = int(np.argmin(zs))
    OUT["M4_zero_modes_min"] = {"beta": float(bs[i]), "valeur": float(zs[i]), "beta_autodual": 1 / (2 * math.pi),
                                "valeur_autodual": zm4(1 / (2 * math.pi))}
    print("M4 fait", flush=True)

    # (B4) boson compact 4D : J = (fℓ)²/n² (taille physique fixée)
    tabb = {}
    for fl in [0.3, 1.0, 3.0]:
        row = {}
        for n in [3, 4, 8, 16, 32]:
            D, _ = Delta(p_boson4, 4, n, fl * fl / n ** 2)
            row[n] = D
        tabb[f"fl={fl}"] = row
    OUT["B4_Delta"] = tabb
    print("B4 fait", flush=True)

    # (S) scalaire massif 4D et 3D, taille physique fixée x = Mℓ, m_lat = x/n
    ts = {}
    for d in [4, 3]:
        for x in [0.1, 1.0, 5.0, 10.0, 15.0]:
            row = {}
            for n in ([4, 8, 16, 32, 64] if d == 4 else [4, 8, 16, 32, 64, 128]):
                D, _ = Delta(p_scal, d, n, (x / n) ** 2)
                row[n] = D
            row["continuum"] = Delta_cont_scal(x, d)
            ts[f"d={d},x={x}"] = row
    OUT["S_Delta"] = ts
    OUT["S_seuils"] = {
        "x*_4(2^-9)": seuil(lambda x: Delta_cont_scal(x, 4), ETA4, 0.1, 40),
        "x*_4(2^-12)": seuil(lambda x: Delta_cont_scal(x, 4), 2.0 ** -12, 0.1, 40),
        "x*_3(2^-7)": seuil(lambda x: Delta_cont_scal(x, 3), ETA3, 0.1, 40),
    }
    OUT["S_petit_x"] = {f"{x}": [Delta_cont_scal(x, 4), Delta_cont_scal(x, 3)] for x in [1e-1, 1e-2, 1e-3, 1e-4]}
    print("S fait", OUT["S_seuils"], flush=True)

    # (M3) Maxwell 3D : β = n/x, x = e²ℓ (taille physique fixée)
    t3 = {}
    for x in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]:
        row = {}
        for n in [3, 4, 8, 16, 32, 64]:
            D, _ = Delta(p_maxwell3, 3, n, n / x)
            row[n] = D
        t3[f"x={x}"] = row
    OUT["M3_Delta"] = t3
    xs = np.exp(np.linspace(np.log(0.01), np.log(300), 300))
    v = [Delta(p_maxwell3, 3, 32, 32 / x)[0] for x in xs]
    i = int(np.argmin(v))
    OUT["M3_min_n32"] = {"x": float(xs[i]), "Delta3": float(v[i])}
    print("M3 fait", flush=True)

    # (Z) scalaire sans masse NON compact, mode zéro 4D retiré (convention euclidienne) : Δ devient négatif
    zr = {}
    for n in [2, 3, 4, 6, 8, 12, 16]:
        def ld(s):
            l = lam_grid(s)[1:]
            return float(np.sum(np.log(l)))
        D = -0.5 * (16 * ld((n,) * 4) - ld((2 * n,) * 4))
        zr[n] = D
    OUT["Z_sans_masse_mode_zero_retire"] = zr
    json.dump(OUT, open("temoins.json", "w"), indent=1)
    print(json.dumps(OUT, indent=1))
